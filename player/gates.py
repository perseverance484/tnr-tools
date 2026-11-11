"""Safety in code (design 4.5): every call the brain wants to send is checked here first.

The rules of record are state/prompt_ai_player_overhaul.md section 2 and data/player_allowlist.json (approved,
RUL-2026-11-11-149). A call is sent only when:
  1. its endpoint is on the allowlist, for the activity that asks (world and dossier reads are shared);
  2. no never rule covers it (a second lock: the list alone already refuses everything else);
  3. it carries nothing that looks like a credential;
  4. every call-level gate on its entry passes (no Flee, do not attack, no snipe, spend caps, ...);
  5. it is not an ask-first call, or the director has said yes to this one.

A refused call is logged as a finding and is not sent; the brain carries on with something else and does not look
for another way to do the same thing. An ask-first call becomes a pending decision for the director.
"""
import collections
import datetime as dt
import json
import re

from . import config as C

Verdict = collections.namedtuple("Verdict", "ok kind rule reason")
"""kind: "allow", "refuse" or "ask". rule: the rule or gate that decided. reason: one line for the finding."""

ALLOW = Verdict(True, "allow", None, "")
SHARED = ("world", "dossier")          # feeds every activity may read (data/player_allowlist.json, fields.activity)
CREDENTIAL = re.compile(r"(?i)(pass(word|wd)?|secret|token|cookie|authori[sz]ation|bearer|api[_-]?key|session[_-]?id"
                        r"|credential|oauth)")


def refuse(rule, reason):
    return Verdict(False, "refuse", rule, reason)


def ask(rule, reason):
    return Verdict(False, "ask", rule, reason)


def rule_hits(rule, name, kind=None):
    """Whether a never / ask-first rule covers an endpoint. Same test as scripts/player_allowlist.py rule_hits
    (player/tests/test_gates.py holds the two together on the whole captured surface)."""
    if name in rule.get("except", ()):
        return False
    if rule.get("kind") and kind and rule["kind"] != kind:
        return False
    if name.split(".", 1)[0] in rule.get("routers", ()) or name in rule.get("endpoints", ()):
        return True
    return any(re.search(p, name) for p in rule.get("patterns", ()))


# ---------------------------------------------------------------- do_not_attack.md
HOLD = re.compile(r"^-\s*(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2})\s*(?:-|UTC\s+to\s+(\d{4}-\d{2}-\d{2})\s+)"
                  r"(\d{2}:\d{2})\s*UTC:\s*([^.]*)\.")
"""A temporary hold, as the file writes them: "- 2026-11-10 16:22-16:52 UTC: Luka and 4qua. Why." or, with its
own end date, "- 2026-11-11 17:10 UTC to 2026-11-12 17:10 UTC: Slyrak (user_...). Why."."""


def _held(line, now):
    """The names and user ids a temporary-hold line keeps off the target list right now. A hold counts until its
    window closes. With no end date, an end at or before the start is on the next day. A line that cannot be
    read, or whose end is before its start, is taken to be open, for every name-like word on it."""
    m = HOLD.match(line.strip())
    try:
        day, start, end_day, end, names = m.groups()
        opens = dt.datetime.fromisoformat(f"{day}T{start}:00+00:00")
        closes = dt.datetime.fromisoformat(f"{end_day or day}T{end}:00+00:00")
        if closes <= opens:
            if end_day:
                raise ValueError("the hold ends before it starts")
            closes += dt.timedelta(days=1)
    except (AttributeError, ValueError):
        return {w.lower() for w in re.findall(r"user_\w+|\b[A-Z0-9][A-Za-z0-9_]{2,}\b", line)}
    if now is not None and now > closes.timestamp():
        return set()                                # the window has closed
    return {n.lower() for n in re.findall(r"[^\s,()]+", names)} - {"and"}


def do_not_attack(path=None, now=None):
    """({names and user ids never attacked}, {names never sniped}) from do_not_attack.md, lower-cased.

    Both tables count as never attack, as in the pilot (a 'do not snipe' player is simply left alone), and so do
    the temporary holds whose window is open. (None, None) when the file cannot be read: the gate then refuses
    every attack."""
    never, snipe, section = set(), set(), "attack"
    try:
        with open(path or C.DO_NOT_ATTACK, encoding="utf8") as f:
            lines = f.read().splitlines()
    except OSError:
        return None, None
    for line in lines:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if line.startswith("## "):
            section = "snipe" if "snipe" in line.lower() else "hold" if "temporary" in line.lower() else "attack"
        elif section == "hold":
            never |= _held(line, now) if line.strip().startswith("-") else set()
        elif line.startswith("|") and cells[0] not in ("Player", "") and not cells[0].startswith("-"):
            names = {cells[0].lower()} | {c.lower() for c in cells if c.startswith("user_")}
            never |= names
            snipe |= names if section == "snipe" else set()
    return never, snipe


# ---------------------------------------------------------------- the call-level gates
def _target(step):
    t = (step.get("meta") or {}).get("target") or {}
    return {str(t.get("userId") or step["input"].get("userId") or "").lower(), str(t.get("username") or "").lower()} - {""}


def g_no_flee(step, world, gates):
    if "flee" in str(step["input"].get("actionId", "")).lower():
        return refuse("no_flee", "Flee is never used")
    return None


def g_do_not_attack(step, world, gates):
    never, _ = do_not_attack(gates.dna_path, world.now)
    if never is None:
        return refuse("do_not_attack", "do_not_attack.md cannot be read, so nobody is attacked")
    who = _target(step)
    if not who:
        return refuse("do_not_attack", "an attack call without a target to check")
    if who & (never | {str(x).lower() for x in world["control"]["do_not_attack"]}):
        return refuse("do_not_attack", "the target is on the do-not-attack list")
    return None


def g_no_snipe(step, world, gates):
    _, snipe = do_not_attack(gates.dna_path, world.now)
    if snipe is None:
        return refuse("no_snipe", "do_not_attack.md cannot be read")
    if _target(step) & snipe:
        return refuse("no_snipe", "the target is under 'Do not snipe'")
    return None


def g_fair_target(step, world, gates):
    t = (step.get("meta") or {}).get("target") or {}
    uid = t.get("userId") or step["input"].get("userId")
    if uid == C.ME:
        return refuse("fair_target", "the target is me")
    if world["opponents"]["lost_to"].get(uid, 0) > world.now:
        return refuse("fair_target", "this player beat me in the last hours")
    if world["opponents"]["skip"].get(uid, 0) > world.now:
        return refuse("fair_target", "the game refused this target a moment ago")
    if t.get("level") is not None and t["level"] < C.MIN_LEVEL:
        return refuse("fair_target", "the target is too low a level to farm")
    if t.get("villageId") and t["villageId"] == C.HOME_VILLAGE:
        return refuse("fair_target", "the target is in my village")
    return None


def g_ryo_only(step, world, gates):
    meta = step.get("meta") or {}
    entry = gates.endpoints[step["call"]]
    cur = step["input"].get("currencyType") or meta.get("currency")
    if cur is not None and cur != "MONEY":
        return ask("premium_currency", f"{step['call']} would pay in {cur}")
    if cur is None and not str(entry.get("currency", "")).strip():
        return refuse("ryo_only", "the call does not show that it pays in ryo")
    return None


def g_spend_cap(step, world, gates):
    """The call's price against the day's allowance and the reserve. A call that carries no price is taken to
    cost all the money in pocket: the game pays a purchase from the pocket, so that is the most it can take.
    With no profile read yet the pocket is not known either, and the director is asked."""
    caps = {"daily": C.DAILY_CAP, "reserve": C.RESERVE, **world["control"]["spend_caps"]}
    pocket, ryo = world.me.get("money"), (step.get("meta") or {}).get("ryo")
    if pocket is None:
        return ask("spend_cap", f"{step['call']}: the money in hand is not known yet")
    ryo = float(pocket if ryo is None else ryo)
    if world.spent_today() + ryo > caps["daily"]:
        return ask("spend_cap", f"{step['call']} could pass the daily cap of {caps['daily']:,.0f} ryo")
    if float(pocket) + float(world.me.get("bank") or 0) - ryo < caps["reserve"]:
        return ask("spend_cap", f"{step['call']} could cut into the reserve of {caps['reserve']:,.0f} ryo")
    return None


def g_player_visible_only(step, world, gates):
    inp = step["input"]
    if inp.get("hidden") is True:
        return refuse("player_visible_only", "a read of hidden records")
    if "ip" in inp:
        return refuse("player_visible_only", "the ip filter is a staff tool")
    return None


def g_study_only(step, world, gates):
    if world.in_battle() and step["input"].get("battleId") != (world["battle"] or {}).get("bid"):
        return refuse("study_only", "other players' fights are read between fights only")
    return None


def g_own_account_only(step, world, gates):
    if step["input"].get("userId") not in (None, C.ME):
        return refuse("own_account_only", "the call names another player's account")
    return None


def g_auction_only(step, world, gates):
    inp = step["input"]
    if inp.get("listingType") != "AUCTION" or inp.get("currencyType") != "MONEY" or inp.get("targetUserId"):
        return refuse("auction_only", "a listing must be a public auction in ryo, never direct to a player")
    return None


def g_one_transfer_a_day(step, world, gates):
    """One level transfer in any 24 hours, counted from the last one (RUL-2026-11-11-152 item 5)."""
    left = world["records"]["transfers"].get("last", -C.TRANSFER_EVERY) + C.TRANSFER_EVERY - world.now
    if left > 0:
        return refuse("one_transfer_a_day", f"the last level transfer was under 24 h ago ({left / 3600:.1f} h to go)")
    return None


CALL_GATES = {"no_flee": g_no_flee, "do_not_attack": g_do_not_attack, "no_snipe": g_no_snipe,
              "fair_target": g_fair_target, "ryo_only": g_ryo_only, "spend_cap": g_spend_cap,
              "player_visible_only": g_player_visible_only, "study_only": g_study_only,
              "own_account_only": g_own_account_only, "auction_only": g_auction_only,
              "one_transfer_a_day": g_one_transfer_a_day}


def _credential(value, depth=0):
    """Whether an input carries something that looks like a credential (a key name, at any depth)."""
    if isinstance(value, dict):
        return any(CREDENTIAL.search(str(k)) or _credential(v, depth + 1) for k, v in value.items())
    if isinstance(value, list):
        return any(_credential(v, depth + 1) for v in value)
    return False


class Gates:
    def __init__(self, allowlist=None, dna_path=None):
        if allowlist is None:
            with open(C.ALLOWLIST, encoding="utf8") as f:
                allowlist = json.load(f)
        self.allowlist = allowlist
        self.endpoints = allowlist.get("endpoints") or {}
        self.never = allowlist.get("never") or []
        self.ask_first = allowlist.get("ask_first") or []
        self.dna_path = dna_path
        missing = {g for e in self.endpoints.values() for g in e.get("gates", ())} - set(CALL_GATES)
        if missing:                                   # a gate named on the list that no code enforces
            raise ValueError("gates on the allowlist with no code behind them: " + ", ".join(sorted(missing)))

    def check(self, step, world, activity=None):
        """The verdict on one call step."""
        name = step.get("call")
        entry = self.endpoints.get(name)
        if entry is None:
            return refuse("allowlist", f"{name} is not on the allowlist")
        return self._fixed(step, entry, activity) or self._gated(step, entry, world) or \
            self._asked(step, entry, world) or ALLOW

    def _fixed(self, step, entry, activity):
        """The refusals that do not depend on the state of the world."""
        name = step["call"]
        hit = next((r for r in self.never if rule_hits(r, name, entry.get("kind"))), None)
        if hit:
            return refuse(hit["id"], f"{name}: {hit['why']}")
        if activity is not None and activity not in entry["activity"] and not set(entry["activity"]) & set(SHARED):
            return refuse("allowlist", f"{name} is not listed for the activity {activity}")
        if _credential(step.get("input") or {}):
            return refuse("credentials", f"{name}: the input carries something that looks like a credential")
        return None

    def _gated(self, step, entry, world):
        """The call-level gates on the entry: the first refusal, or the first question the director has not
        answered with a yes."""
        for g in entry.get("gates", ()):
            v = CALL_GATES[g](step, world, self)
            if v is not None and (v.kind == "refuse" or world.answered(self.key(step, v.rule)) != "yes"):
                return v
        return None

    def _asked(self, step, entry, world):
        """An ask-first call waits for the director's yes to this exact call."""
        name, kind = step["call"], entry.get("kind")
        rule = entry.get("ask_first") or next(
            (r["id"] for r in self.ask_first if rule_hits(r, name, kind)
             and not str(entry.get(r.get("waiver", ""), "")).strip()), None)
        if not rule or world.answered(self.key(step, rule)) == "yes":
            return None
        return ask(rule, f"{name}: " + next((r["why"] for r in self.ask_first if r["id"] == rule), rule))

    @staticmethod
    def key(step, rule):
        """What a pending decision is filed under: the rule, the endpoint and the exact input."""
        return f"{rule}:{step['call']}:{json.dumps(step.get('input') or {}, sort_keys=True)}"

    def screen(self, steps, world, activity):
        """Check a plan's call steps. Returns (ok, verdict, step): ok is False at the first call that may not be
        sent. A refusal is written down as a finding; an ask-first call becomes a pending decision. Either way the
        whole plan is dropped: the brain does something else."""
        for step in steps:
            if "call" not in step:
                continue
            v = self.check(step, world, activity)
            if v.ok:
                continue
            if v.kind == "ask":
                world.decide(self.key(step, v.rule), f"{activity}: {v.reason}. Say yes or no.", step)
            else:
                world.event("finding", f"{activity}: {v.reason}", about="gate", rule=v.rule, call=step["call"])
            return False, v, step
        return True, ALLOW, None

    def sent(self, step, world):
        """Book-keeping once a call is really issued (when the last level transfer went)."""
        if step.get("call") == "jutsu.transferLevel":
            world["records"]["transfers"] = {"last": world.now}
