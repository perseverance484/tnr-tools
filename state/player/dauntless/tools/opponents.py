#!/usr/bin/env python3
"""Opponent models from every logged fight (director 2026-11-11: "Pull every log you can, model as many opponents as
possible as thoroughly as possible and play them. It's like you're playing back replays and trying to find the
right moves").

Source: every battle log in entries form under fights/ (my fights, the director's, observed ones under
fights/observed/). Per opponent (by user id, merged across fights):
  kit       every action he used (+ his saved equipped kit when we have it), compiled from catalog records
  profile   bloodline / rank / boost / elements (opp_profile)
  habits    how often each action shows up, on which rounds, his opening, what follows what (transitions), his full
            bundles per round, how many AP he spends
  results   fights, rounds, my wins / losses against him
The bot (fightsim) plays him by his own simulated score plus these habits, so he repeats his real rotation where
the log shows one and still reacts to the board where it does not. `opponents.py check` measures that: how often
the bot's first choice equals his real bundle in the logged positions.

Usage: opponents.py build | list | check [NAME]
"""
import collections
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIGHTS = os.path.join(HERE, "..", "fights")
MODELS = os.path.join(HERE, "..", "fights", "opponents.json")
sys.path.insert(0, HERE)
from ingest import ME  # noqa: E402

NAME_RE = re.compile(r"^(.+?) (?:takes|damage|will|cannot|is|was|marked|heals|absorbs|copies|steals|vamps|loses|"
                     r"resists|uses|moves|pierced|dodges)\b")


def load_logs():
    """[(battle id, rows oldest-first [(round, user, action, texts)])] for every entries-form log."""
    out = []
    paths = glob.glob(os.path.join(FIGHTS, "*.json")) + glob.glob(os.path.join(FIGHTS, "observed", "*.json"))
    for p in sorted(paths):
        try:
            d = json.load(open(p))
        except (OSError, ValueError):
            continue
        if not isinstance(d, dict) or "*.battleRound" not in d:
            continue
        rows = list(zip(d["*.battleRound"], d["*.userId"], d["*.actionId"],
                        d.get("*.appliedEffects.*.txt") or [None] * len(d["*.battleRound"])))[::-1]
        bid = os.path.basename(p).split("_")[0].replace(".json", "")
        out.append((bid, p, rows, d.get("_meta") or {}))
    return out


def names_in(rows, uid, me_name="dauntless"):
    """His name as the log writes it: the most common subject of his own effect lines; failing that, whoever
    takes damage from my actions (a masked or terse opponent may have no self-lines)."""
    c = collections.Counter()
    for r, u, a, ts in rows:
        if u == uid:
            continue
        for t in ts or []:
            m = re.match(r"^(.+?) takes [\d.]+ (?:damage|afterburn damage)$", (t or "").strip())
            if m and m.group(1) != me_name:
                c[m.group(1)] += 3
    for r, u, a, ts in rows:
        if u != uid:
            continue
        for t in ts or []:
            m = NAME_RE.match((t or "").strip())
            if m and m.group(1) != me_name:
                c[m.group(1)] += 1
    return c.most_common(1)[0][0] if c else uid


def turns_of(rows, uid):
    """His turns: [(round, (action ids...))] in order, waits and moves dropped."""
    out, cur, cur_r = [], [], None
    for r, u, a, ts in rows:
        if u != uid:
            if cur:
                out.append((cur_r, tuple(cur))); cur = []
            continue
        if cur_r is not None and r != cur_r and cur:
            out.append((cur_r, tuple(cur))); cur = []
        cur_r = r
        if a not in ("wait", "move"):
            cur.append(a)
    if cur:
        out.append((cur_r, tuple(cur)))
    return out


_LOGS = None
_EXCL = None


def build(exclude=None, save=True):
    """exclude: a battle id left out (leave-one-fight-out checks); save=False returns the models without writing."""
    global _LOGS
    models = {}
    if _LOGS is None or save:
        _LOGS = load_logs()
    for bid, path, rows, meta in _LOGS:
        if exclude and bid == exclude:
            continue
        users = {u for _, u, _, _ in rows if (u or "").startswith("user_")}
        # my fights: model the other side; observed fights between others (harvest.py): model both sides
        sides = users - {ME} if ME in users else (users if len(users) == 2 else set())
        for uid in sides:
            if len(users) > 3:
                continue
            m = models.setdefault(uid, {"userId": uid, "names": [], "fights": [], "ids": {}, "rounds": {},
                                        "openings": [], "bundles": [], "trans": {}, "won": 0, "lost": 0})
            nm = (meta.get("names") or {}).get(uid) or names_in(rows, uid)
            if nm not in m["names"]:
                m["names"].append(nm)
            m["fights"].append(bid)
            prev = None
            for k, (r, b) in enumerate(turns_of(rows, uid)):
                if k == 0:
                    m["openings"].append(list(b))
                m["bundles"].append([r, list(b)])
                for a in b:
                    m["ids"][a] = m["ids"].get(a, 0) + 1
                    m["rounds"].setdefault(a, []).append(r)
                    if prev:
                        for p in prev:
                            t = m["trans"].setdefault(p, {})
                            t[a] = t.get(a, 0) + 1
                prev = b
            if meta.get("winner"):
                m["won" if meta["winner"] == uid else "lost"] += 1
    if save:
        json.dump(models, open(MODELS, "w"), indent=0)
    return models


def load():
    ex = os.environ.get("TNR_OM_EXCLUDE")
    if ex:                                              # leave-one-fight-out view (postmortem.py)
        global _EXCL
        if _EXCL is None or _EXCL[0] != ex:
            _EXCL = (ex, build(exclude=ex, save=False))
        return _EXCL[1]
    try:
        return json.load(open(MODELS))
    except (OSError, ValueError):
        return build()


HABIT_SCALE = float(os.environ.get("TNR_HABIT", "4.0"))   # validate.py --policy: x4 best (LOO 7% exact, 25% overlap)


def habit_fn(model, scale=None):
    scale = HABIT_SCALE if scale is None else scale
    """habit(bundle, round, previous bundle) -> HP-equivalent bonus for doing what he does in the logs:
    share of his turns that use the action, a bonus when he used it on this round number, a bonus for what usually
    follows his last bundle, and a bonus for a whole bundle he has played on this round."""
    n_turns = max(1, len(model.get("bundles", [])))
    freq = {a: c / n_turns for a, c in model.get("ids", {}).items()}
    by_round = {a: collections.Counter(rs) for a, rs in model.get("rounds", {}).items()}
    trans = model.get("trans", {})
    seen = collections.defaultdict(set)
    for r, b in model.get("bundles", []):
        seen[r].add(tuple(sorted(b)))
    opening = collections.Counter(tuple(sorted(b)) for b in model.get("openings", []))
    p_role, p_next, racts = rotation_fn(model)
    hist = collections.Counter(tuple(sorted(b)) for r, b in model.get("bundles", []))

    def habit(hb, rnd, prev=None, first_turn=False, prev2=None):
        v = 0.0
        for a in hb:
            v += 350 * freq.get(a, 0.0)
            if by_round.get(a, {}).get(rnd):
                v += 150
            if prev:
                tot = sum(sum(trans.get(p, {}).values()) for p in prev) or 0
                if tot:
                    v += 300 * sum(trans.get(p, {}).get(a, 0) for p in prev) / tot
        key = tuple(sorted(hb))
        if key in seen.get(rnd, ()):
            v += 250
        if first_turn and opening.get(key):
            v += 500
        # his rotation: setup -> payoff -> ... (role of this turn given his last two), and his exact follow-ups
        v += ROLE_W * p_role(role_of(hb, racts), prev, prev2)
        v += BIGRAM_W * p_next(hb, prev)
        v += HIST_W * hist.get(key, 0) / n_turns
        return v * scale
    return habit


ROLE_W = float(os.environ.get("TNR_ROLE_W", "600"))      # HP-equivalent for P(this turn's role | his last roles)
BIGRAM_W = float(os.environ.get("TNR_BIGRAM_W", "500"))  # for P(this exact bundle | his last bundle)
HIST_W = float(os.environ.get("TNR_HIST_W", "0"))        # for the share of his turns that were exactly this bundle
PAYOFF_DMG = 800.0


def role_of(bundle, acts):
    """His turn's job in a rotation, from the compiled kit (spec perspective "en" = him, "me" = his target):
    payoff  >= 800 base damage (the burst)
    setup   less damage, and more of it goes to buffing himself or debuffing me than to defending
    defend  mostly his own DR / shield / heal / cleanse / absorb
    poke    the rest"""
    dmg = up = guard = 0.0
    for a in bundle:
        v = acts.get(a)
        if not v:
            continue
        spec = v[4]
        dmg += float(spec[0] or 0)
        for t in spec[1]:
            who, kind = t[0], t[1]
            if (who == "en" and kind in ("given", "lifesteal")) or (who == "me" and kind in ("taken", "wound", "recoil",
                                                                                                 "afterburn", "drain")):
                up += 1
            elif who == "en" and kind in ("dr", "shield", "heal", "cleanse", "absorb", "reflect", "parry"):
                guard += 1
            elif who == "me" and kind == "given" and t[2] < 0:
                guard += 1
    if dmg >= PAYOFF_DMG:
        return "payoff"
    if up and up >= guard:
        return "setup"
    if guard:
        return "defend"
    return "poke"


def _sequences(model):
    """His turns split into fights (a round number that does not rise starts a new fight)."""
    seqs, cur, last = [], [], None
    for r, b in model.get("bundles", []):
        if last is not None and r <= last and cur:
            seqs.append(cur); cur = []
        cur.append((r, tuple(b)))
        last = r
    if cur:
        seqs.append(cur)
    return seqs


_PRIOR = None


def role_prior():
    """Role transitions pooled over every modelled opponent: the shape of a PvP rotation in general."""
    global _PRIOR
    if _PRIOR is None:
        c1, c2 = collections.defaultdict(collections.Counter), collections.defaultdict(collections.Counter)
        for m in load().values():
            acts = acts_for(m)
            for seq in _sequences(m):
                rs = ["start", "start"] + [role_of(b, acts) for _, b in seq]
                for i in range(2, len(rs)):
                    c1[rs[i - 1]][rs[i]] += 1
                    c2[(rs[i - 2], rs[i - 1])][rs[i]] += 1
        _PRIOR = (c1, c2)
    return _PRIOR


def rotation_fn(model, acts=None):
    """P(role | his last two roles) for this opponent, shrunk toward the pooled prior; P(bundle | last bundle)."""
    acts = acts or acts_for(model)
    m1, m2 = collections.defaultdict(collections.Counter), collections.defaultdict(collections.Counter)
    big = collections.defaultdict(collections.Counter)
    for seq in _sequences(model):
        rs = ["start", "start"] + [role_of(b, acts) for _, b in seq]
        keys = [None] + [tuple(sorted(b)) for _, b in seq]
        for i in range(2, len(rs)):
            m1[rs[i - 1]][rs[i]] += 1
            m2[(rs[i - 2], rs[i - 1])][rs[i]] += 1
        for i in range(1, len(keys) - 1):
            big[keys[i]][keys[i + 1]] += 1
    p1, p2 = role_prior()

    def p_role(role, prev, prev2):
        r1 = acts and role_of(prev, acts) if prev else "start"
        r2 = role_of(prev2, acts) if prev2 else ("start" if not prev else "start")
        out, wsum = 0.0, 0.0
        for cnt, w in ((m2.get((r2, r1)), 3.0), (m1.get(r1), 2.0), (p2.get((r2, r1)), 1.0), (p1.get(r1), 0.5)):
            if cnt:
                tot = sum(cnt.values())
                n = tot / (tot + 2.0)                       # trust grows with samples
                out += w * n * cnt.get(role, 0) / tot
                wsum += w * n
        return out / wsum if wsum else 0.25

    def p_next(hb, prev):
        c = big.get(tuple(sorted(prev))) if prev else None
        if not c:
            return 0.0
        tot = sum(c.values())
        return c.get(tuple(sorted(hb)), 0) / tot * tot / (tot + 1.0)

    return p_role, p_next, acts


def acts_for(model):
    import clock
    import engine_bridge as EB
    kit = EB.opponent_kit(model["userId"]) or {}
    ids = list(kit.get("jutsu", [])) + list(kit.get("weapons", [])) + [a for a in model.get("ids", {}) if a not in ("wait", "move")]
    acts = clock.acts_from_ids(ids, kit.get("jutsuLevels", {}), kit)
    # the basics already in acts use the engine's own ids: map his logged basic ids onto them
    return acts


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "build":
        ms = build()
        print(f"{len(ms)} opponents from {len(load_logs())} logs")
    ms = load()
    if cmd in ("build", "list"):
        for uid, m in sorted(ms.items(), key=lambda kv: -len(kv[1]["bundles"])):
            top = sorted(m["ids"].items(), key=lambda kv: -kv[1])[:4]
            print(f"{'/'.join(m['names'])[:20]:20} fights {len(m['fights']):2}  turns {len(m['bundles']):3}  "
                  f"actions {len(m['ids']):2}  opening {'+'.join(x[:6] for x in m['openings'][0]) if m['openings'] else '-'}")


if __name__ == "__main__":
    main()
