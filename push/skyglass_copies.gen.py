#!/usr/bin/env python3
"""Generate push/344: the Skyglass AI copies (new AI records derived from live AIs), all HIDDEN.

    python3 push/skyglass_copies.gen.py                         # 344_skyglass_copies_1.json (runnable now)
    python3 push/skyglass_copies.gen.py --summon <344_1 bundle>  # 344_skyglass_copies_2.json, AFTER part 1 has run
    python3 push/skyglass_copies.gen.py --blocked               # 344_skyglass_copies_3.json: the blocked copies,
                                                                #   written for review only (Forge refuses it today)
    --library <342 bundle> reads the library ids from another bundle (default: push/342's run).

Sources (state/skyglass_build/, provenance in its README; zero live requests):
  - charts_spec.json `newAIs`: the chart-run copies (common, rare and tainted copies, the Sealed Reliquary's three
    Lingering Echo hazards, the Fall's Arsenal Keeper, the Steeping Horror), each created from its `fullRow` and
    `fullProfile` (the row and rules the harness fought; final pass + RUL-2026-10-30-060 item 2, -062 item 1).
    Two copies are NOT built: chart-c-wayfinder (only the Low Tide Run's press-on room) and chart-r-oathkeeper (only
    the Sealed Reliquary's press-on room); RUL-2026-10-30-060 item 6 cut both rooms.
  - haul_spec.json `records`: the 15 Haul guard copies (the 6ad2a102 fit), from `fullRow` / `fullProfile`.
  - build_spec.json `endgame` / `lvl50`: the Wreck dungeon's party-tuned copies and the level-50 (easy Wreck) copies
    (SKYGLASS_BOSS_FIGHTS.md section 5), each the shared kit (`sharedKits`, lvl50 `ruleVariants`) on the live
    record's chassis with the version's level, multipliers, stats and innate effects.
  - the Crown Stonebound summon: a copy of the live Crown Stonebound (push/272 D3.REG4) whose Erupting Ground is the
    library's enemies-only Echo of Erupting Ground (RUL-2026-10-30-060 item 7, RUL-2026-10-28-026 items 2-3). The live
    record is a Crownhold D3 regular and stays as it is; part 2 points Stonebound Summons at the copy.

Every rule set is the harness's (includeDefaultRules false; the fallback fix of RUL-2026-10-29-046 item 2 / RUL-060
item 7 is already in it: no use_highest_power_* / use_random_jutsu / use_combo_action rule, and the last free pick is
the named basic attack `basicAttack`, which ai_v2.ts resolves from the available actions at theninjarpg@3314d122
libs/combat/ai_v2.ts ~494 and actions.ts ~512). The generator re-checks that and refuses otherwise. Two changes that
do not change behaviour: rules below an unconditional end_turn are dropped (never reached), and a chain that does not
end on an unconditional end_turn / move gets the unconditional end_turn the engine appends anyway (ai_v2.ts ~273-281).

Three gates decide where a copy goes:
  - AI_PROFILE_MAX_RULES = 20 (app/drizzle/constants.ts:1933, enforced in routers/ai.ts:87): a longer simulated rule
    set is BLOCKED (which rules to cut changes the tuned fight: director).
  - Forge's pre-send kit lint (forge/src/runner/pool.mjs kitProblems, run at manifest parse, so one bad AI refuses the
    whole manifest): a rule firing `basicAttack` reads as "not equipped", and a distance gate other than range+1 on a
    pool jutsu is refused. The harness rule sets use both (gates at range: safe under law 40 but not the exact
    range+1). A copy that trips either is BLOCKED until the director chooses the fix (see push/README.md 344).
  - everything else is part 1.

Literal ids (law 17): library placeholders (lib-*, hunt-*, dg-*, chart-embers-*) resolve through push/342's results
bundle (idmap keys sg342_<spec id>). Live jutsu ids are used as they are. Art (RUL-2026-10-30-059): each copy keeps its
source's live sprite. Usernames (law 66: unique across all UserData) are PLACEHOLDERS, listed in `_usernames`, for the
director to rename (an AI edit; reversible).

Order (law 18): Stonebound Summons must name the copy BEFORE anything equips it, and the copy's id exists only after
part 1 runs, so part 2 (the summon edit, literal id from part 1's bundle) runs before any holder of the summon is
created; its three copy holders (the rare and tainted Sealwright copies, the Haul's Sealwright's Echo) are blocked
copies and come after it.

Later builders (chart runs, Haul quests, steeping, Wreck floors) read 344's results bundles: idmap keys sg344_<spec id>.
Do not hand-edit the output.
"""
import copy
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.path.join(ROOT, "state/skyglass_build")
NUM = 344
PFX = "sg344_"
LIB_PFX = "sg342_"
LIB_BUNDLE = os.path.join(ROOT, "harvests/inbox/tnr_results_1793426982231.json")  # push/342, 41/41 VERIFIED
NANO = re.compile(r"^[A-Za-z0-9_-]{21}$")
PLACEHOLDER = re.compile(r"^(lib-|hunt-|dg-|chart-embers-)")
BASIC = "basicAttack"  # the engine's basic attack action id (actions.ts ~512)
# Server cap on an AI profile's rules: theninjarpg@3314d122 app/drizzle/constants.ts:1933 AI_PROFILE_MAX_RULES = 20,
# enforced by ai.updateAiProfile (server/api/routers/ai.ts:87, "Maximum of 20 rules allowed"). The harness did not
# enforce it; a copy whose simulated rule set is longer is NOT built (director decision: which rules to cut changes
# the tuned fight), and is listed in `_blocked`.
MAX_RULES = 20
DEAD = []  # unreachable rules dropped (no behaviour change), reported in the manifests
TAIL = []  # records whose engine-appended end_turn tail is written out (no behaviour change)
POOL = json.load(open(os.path.join(ROOT, "32b_DATA_pool.json")))["records"]
POOL_BY_ID = {r["id"]: r for r in POOL.values()}
BANNED_ACTIONS = {"use_highest_power_action", "use_highest_power_jutsu", "use_highest_power_item", "use_random_jutsu",
                  "use_combo_action"}

SUMMON_JUTSU = "bcbOllIWqHEopmQGHKDED"  # Stonebound Summons (push/342 sg342_hunt-called-to-the-archive; 343 text)
SUMMON_SRC = "hunt-called-to-the-archive"
STONEBOUND_LIVE = "jqxu13kNHhfNY-NF68Ftb"  # Crown Stonebound, push/272 crownhold_d3.reg4
ERUPTING_GROUND = "jBRyl7F4UjTyxG5nnzLqj"
ECHO_SRC = "hunt-stonebound-erupting-ground"  # Echo of Erupting Ground (push/342)
STONEBOUND_KEY = "crown-stonebound-summon"
CREW_272 = os.path.join(ROOT, "archive/spent-manifests/push-2026-10-25/272_crownhold_ais.json")

CUT_PRESS_ON = {"chart-c-wayfinder": "Low Tide Run press-on room (cut, RUL-2026-10-30-060 item 6)",
                "chart-r-oathkeeper": "Sealed Reliquary press-on room (cut, RUL-2026-10-30-060 item 6)"}

AI_KEYS = ("username", "hidden", "level", "rank", "poolsMultiplier", "statsMultiplier", "regeneration", "gender",
           "preferredGeneral1", "preferredGeneral2", "primaryElement", "secondaryElement", "isSummon", "avatarFacing",
           "ninjutsuMastery", "genjutsuMastery", "taijutsuMastery", "bukijutsuMastery", "bloodlineMastery",
           "sageMastery", "offence", "defence", "strength", "intelligence", "willpower", "speed", "avatar")
STATS6 = ("offence", "defence", "strength", "intelligence", "willpower", "speed")
MASTERIES = ("ninjutsuMastery", "genjutsuMastery", "taijutsuMastery", "bukijutsuMastery", "bloodlineMastery",
             "sageMastery")

# ------------------------------------------------------------------ placeholder usernames (law 66; director to rename)
TIER = {"c": "Chart", "r": "Rare Chart", "t": "Tainted"}
HAUL_NAMES = {
    "h-wayfinder": "Wayfinder (Hunter)", "h-blade": "First Blade (Hunter)", "h-warden": "Deck Warden (Hunter)",
    "h-veteran": "First Blade (Veteran)", "h-lookout": "Deck Warden (Hunt Lookout)", "trophy-warden": "Trophy Warden",
    "h-keeper": "Arsenal Keeper (Haul)", "g-warden": "Deck Warden (Stores)", "g-sentinel": "Skyglass Sentinel (Stores)",
    "g-veteran": "Skyglass Sentinel (Veteran)", "g-lookout": "Deck Warden (Stores Lookout)",
    "g-charge": "Seal Charge (Haul)", "g-canister": "Core Canister (Haul)", "stores-ward": "Stores Ward",
    "g-sealwright": "Sealwright's Echo"}
SPECIAL_NAMES = {"chart-lingering-echo-2": "Lingering Echo I", "chart-lingering-echo-3": "Lingering Echo II",
                 "chart-lingering-echo-4": "Lingering Echo III", "chart-arsenal-keeper": "Arsenal Keeper (Magazine)",
                 "chart-steeping-horror": "Steeping Horror", STONEBOUND_KEY: "Crown Stonebound (Summoned)"}


def chart_name(key, rec):
    if key in SPECIAL_NAMES:
        return SPECIAL_NAMES[key]
    m = re.match(r"^chart-([crt])-", key)
    assert m, key
    return f"{rec['username']} ({TIER[m.group(1)]})"


def spec(name):
    return json.load(open(os.path.join(BUILD, name)))


class Lib:
    """Library placeholder -> live id from push/342's results bundle."""

    def __init__(self, bundle):
        self.bundle = bundle
        self.idmap = json.load(open(bundle)).get("idmap") or {}

    def jutsu(self, jid, where):
        if jid == BASIC:
            return jid
        if PLACEHOLDER.match(jid):
            lid = self.idmap.get(LIB_PFX + jid)
            if not lid:
                raise SystemExit(f"{where}: {jid} has no {LIB_PFX}{jid} in {os.path.basename(self.bundle)}")
            return lid
        if not NANO.match(jid):
            raise SystemExit(f"{where}: {jid!r} is neither a library placeholder nor a live id")
        return jid


# ------------------------------------------------------------------ rules
def rule(r, lib, where, swap=None):
    a = copy.deepcopy(r.get("action") or r.get("do"))
    conds = copy.deepcopy(r.get("conditions") if "conditions" in r else r.get("when"))
    if a["type"] in BANNED_ACTIONS:
        raise SystemExit(f"{where}: {a['type']} rule (fallback fix, RUL-2026-10-30-060 item 7)")
    if "jutsuId" in a:
        j = (swap or {}).get(a["jutsuId"], a["jutsuId"])
        a["jutsuId"] = lib.jutsu(j, where)
    out = {"conditions": conds, "action": a}
    if r.get("priority") is not None:
        out["priority"] = r["priority"]
    return out


def check_rules(rules, kit, where):
    """Every jutsu a rule fires is equipped; the chain ends unconditionally; basic attack is the last free pick."""
    for r in rules:
        j = r["action"].get("jutsuId")
        if j and j != BASIC and j not in kit:
            raise SystemExit(f"{where}: rule fires {j}, which is not in the kit")
    last = rules[-1]
    if last["action"]["type"] not in ("end_turn", "move_towards_opponent") and not (
            last["action"].get("jutsuId") == BASIC and not last["conditions"]):
        raise SystemExit(f"{where}: chain does not end on basic attack / end turn")


# ------------------------------------------------------------------ records
def items_of(row):
    # AI items: {ids, number} with number = dropChancePerc (law 69). The live crew carry kit items at 0%.
    return [{"ids": [it["itemId"]], "number": 0} for it in (row.get("items") or [])]


def drop_dead_tail(rules, where, notes):
    """Rules below an unconditional end_turn never run (end_turn always executes, ai_v2.ts ~556): drop them."""
    for i, r in enumerate(rules[:-1]):
        if r["action"]["type"] == "end_turn" and not r["conditions"]:
            gone = [x["action"].get("description", x["action"]["type"]) for x in rules[i + 1:]]
            notes.append(f"{where}: dropped {len(gone)} unreachable rule(s) below an unconditional end turn: {gone}")
            return rules[:i + 1]
    return rules


def entry(key, data, rules, group, notes):
    data = dict(data)
    rules = drop_dead_tail(rules, key, DEAD)
    last = rules[-1]
    if (last["conditions"] or last["action"]["type"] not in ("end_turn", "move_towards_opponent")) and len(rules) < MAX_RULES:
        # ai_v2.ts ~273-281 (3314d122): the engine appends this exact rule to every AI profile that has an effect
        # action available (basic attack always is), so writing it changes nothing and satisfies law 41.
        rules = rules + [{"conditions": [], "action": {"type": "end_turn", "description": "End turn"}}]
        TAIL.append(key)
    data["hidden"] = True
    data["includeDefaultRules"] = False
    data["rules"] = rules
    check_rules(rules, set(data["jutsus"]), key)
    return {"entity": "ai", "slot": "create", "phase": 1, "name": data["username"], "srcId": PFX + key,
            "_group": group, "_note": notes, "data": data}


def from_full(key, rec, lib, username, group, note):
    row, prof = rec["fullRow"], rec["fullProfile"]
    if prof.get("includeDefaultRules"):
        raise SystemExit(f"{key}: includeDefaultRules on (fallback fix)")
    data = {k: copy.deepcopy(row.get(k)) for k in AI_KEYS}
    data["username"] = username
    data["jutsus"] = [lib.jutsu(j, key) for j in row["jutsus"]]
    data["items"] = items_of(row)
    data["effects"] = copy.deepcopy(row.get("effects") or [])
    rules = [rule(r, lib, key) for r in prof["rules"]]
    return entry(key, data, rules, group, note)


def charts(lib, skipped):
    c = spec("charts_spec.json")
    out = []
    for key, rec in c["newAIs"].items():
        if key in CUT_PRESS_ON:
            skipped.append(f"{key} ({rec['username']}): not built; used only by the {CUT_PRESS_ON[key]}")
            continue
        out.append(from_full(key, rec, lib, chart_name(key, rec), "chart", rec["note"]))
    return out


def haul(lib):
    h = spec("haul_spec.json")
    out = []
    for rk, rec in h["records"].items():
        key = rec["key"]
        assert rk == "haul-" + key, rk
        note = f"{rec['role']}; copy of {rec['copyOf']['name']} ({rec['copyOf']['id']}); {rec['rulesNote']}"
        out.append(from_full(rk, rec, lib, HAUL_NAMES[key], "haul", note))
    return out


def chassis_rows():
    """Live source -> chassis row (the harness's fullRow of a chart copy of that source: avatar, generals, masteries)."""
    c = spec("charts_spec.json")
    rows = {}
    for key, rec in c["newAIs"].items():
        rows.setdefault(rec["username"], rec["fullRow"])
    return rows


def wreck(lib):
    b = spec("build_spec.json")
    rows = chassis_rows()
    out = []
    for version, label, group in (("endgame", "Wreck", "wreck"), ("lvl50", "Easy Wreck", "wreck50")):
        variants = b[version].get("ruleVariants") or {}
        for a in b[version]["ais"]:
            live = a["copyOf"]["liveAi"]
            kit = b["sharedKits"][live]
            assert kit["liveAiId"] == a["copyOf"]["liveAiId"], a["harnessId"]
            row = rows[live]
            data = {k: copy.deepcopy(row.get(k)) for k in AI_KEYS}
            data.update({"username": f"{live} ({label})", "level": a["level"], "rank": a["rank"],
                         "statsMultiplier": a["statsMultiplier"], "poolsMultiplier": a["poolsMultiplier"]})
            # Stats are ratio weights (law 15): send the version's six stats and the chassis masteries at the same
            # scale, so the ratio is the live one and the server's scaleUserStats lands where the harness did.
            factor = a["stats"]["offence"] / row["offence"]
            for k in STATS6:
                data[k] = a["stats"][k]
            for k in MASTERIES:
                data[k] = max(10, round(row[k] * factor, 2)) if row[k] > 10 else row[k]
            data["jutsus"] = [lib.jutsu(j["id"] if isinstance(j, dict) else j, a["harnessId"]) for j in kit["jutsu"]]
            data["items"] = items_of(row)
            data["effects"] = copy.deepcopy(a["effects"])
            src_rules = (variants.get(live) or {}).get("rules") or kit["rules"]
            rules = [rule(r, lib, a["harnessId"]) for r in src_rules]
            note = (f"{version} copy of {live} ({a['copyOf']['liveAiId']}): shared kit"
                    f"{' (lvl50 rule variant)' if live in variants else ''}; level {a['level']}, stats x"
                    f"{a['statsMultiplier']}, pools x{a['poolsMultiplier']}; " + "; ".join(a.get("scaleEditedAiNotes", [])))
            out.append(entry(a["harnessId"], data, rules, group, note))
    return out


def stonebound(lib):
    m = json.load(open(CREW_272))
    src = next(e for e in m["items"] if e.get("srcId") == "crownhold_d3.reg4")["data"]
    h = next(a for a in spec("hunts_spec.json")["ais"] if a["liveId"] == STONEBOUND_LIVE)
    live_kit = [j["liveId"] for j in h["jutsu"]]
    assert live_kit == src["jutsus"], (live_kit, src["jutsus"])  # push/272 as stored = the hunts spec's live kit
    swap = {ERUPTING_GROUND: ECHO_SRC}
    data = {k: copy.deepcopy(src.get(k)) for k in AI_KEYS}
    data["username"] = SPECIAL_NAMES[STONEBOUND_KEY]
    data["jutsus"] = [lib.jutsu(swap.get(j, j), STONEBOUND_KEY) for j in src["jutsus"]]
    data["items"] = []
    data["effects"] = copy.deepcopy(src.get("effects") or [])
    rules = [rule(r, lib, STONEBOUND_KEY, swap) for r in src["rules"]]
    note = ("copy of Crown Stonebound (jqxu13kNHhfNY-NF68Ftb, push/272 D3.REG4 as stored, hunts_spec: 'only summoned "
            "by Called to the Archive') with Erupting Ground replaced by Echo of Erupting Ground (enemies-only damage). "
            "Summoned at 40% power / 15000 HP by Stonebound Summons (part 3 points the summon here). Crownhold record: "
            "rules unchanged (RUL-2026-10-30-060 item 7 leaves Crownhold's end-turn chains as they are).")
    return entry(STONEBOUND_KEY, data, rules, "summon", note)


SUMMON_HOLDERS = ("chart-r-sealwright", "chart-t-sealwright", "haul-g-sealwright")


def holds_summon(e, lib):
    return lib.jutsu(SUMMON_SRC, "summon") in e["data"]["jutsus"]


def all_copies(lib):
    skipped = []
    ents = charts(lib, skipped) + haul(lib) + wreck(lib) + [stonebound(lib)]
    names = [e["data"]["username"] for e in ents]
    dup = {n for n in names if names.count(n) > 1}
    if dup:
        raise SystemExit(f"duplicate placeholder usernames: {sorted(dup)}")
    held = [e["srcId"][len(PFX):] for e in ents if holds_summon(e, lib)]
    assert tuple(held) == SUMMON_HOLDERS, held
    blocked = [f"{e['srcId']} ({e['data']['username']}): {len(e['data']['rules'])} rules in the simulated rule set, "
               f"above the server's AI_PROFILE_MAX_RULES = {MAX_RULES}; not built until the director rules which rules to cut"
               for e in ents if len(e["data"]["rules"]) > MAX_RULES]
    ents = [e for e in ents if len(e["data"]["rules"]) <= MAX_RULES]
    return ents, skipped, blocked


def strip(e):
    return {k: v for k, v in e.items() if not k.startswith("_")}


def write(path, m):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(m, fh, indent=1, ensure_ascii=False)
        fh.write("\n")


def ledger(ents):
    return [f"{e['srcId']}: {e['data']['username']} ({e['_group']}; {e['_note']})" for e in ents]


def forge_kit_problems(data):
    """forge/src/runner/pool.mjs kitProblems errors, ported (same 32b_DATA_pool.json)."""
    eq = set(data["jutsus"])
    out = []
    for i, r in enumerate(data["rules"]):
        jid = r["action"].get("jutsuId")
        if not jid:
            continue
        if eq and jid not in eq:
            out.append(f"rules[{i}]: fires {jid} (not in jutsus)")
        rec = POOL_BY_ID.get(jid)
        if not rec:
            continue
        for c in r["conditions"]:
            if c.get("type") == "distance_lower_than" and rec.get("gate") is not None and c.get("value") != rec["gate"]:
                out.append(f"rules[{i}]: {rec['name']} gate {c.get('value')} != range+1 {rec['gate']}")
    return out


def partition(lib):
    ents, skipped, blocked = all_copies(lib)
    ready, held = [], []
    for e in ents:
        probs = forge_kit_problems(e["data"])
        if probs or holds_summon(e, lib):
            basic = sum("basicAttack" in p for p in probs)
            gates = sum("range+1" in p for p in probs)
            why = []
            if basic:
                why.append(f"{basic} basicAttack rule(s)")
            if gates:
                why.append(f"{gates} gate(s) at range, not range+1")
            if holds_summon(e, lib):
                why.append("holds Stonebound Summons (after part 2)")
            e["_blocked_by"] = "; ".join(why)
            held.append(e)
        else:
            ready.append(e)
    return ready, held, skipped, blocked


def counts_of(sel):
    c = {}
    for e in sel:
        c[e["_group"]] = c.get(e["_group"], 0) + 1
    return c


def main_ready(lib):
    ready, held, skipped, blocked = partition(lib)
    counts = counts_of(ready)
    note = (f"push/{NUM} part 1 (RUL-2026-10-30-059: hidden, live sprites). Skyglass AI copies that Forge accepts today: "
            + ", ".join(f"{n} {g}" for g, n in counts.items())
            + f" = {len(ready)} AI creates, all hidden, includeDefaultRules false, rows and rules as the harness fought them "
              "(state/skyglass_build). The Crown Stonebound copy is here: part 2 (Stonebound Summons -> the copy) is built "
              f"from THIS run's bundle (python3 push/skyglass_copies.gen.py --summon <bundle>). {len(held)} further copies "
              f"are blocked on Forge's kit lint and {len(blocked)} on the server's 20-rule cap (push/README.md 344). "
              "Library jutsu by literal id from push/342's bundle "
              f"{os.path.basename(lib.bundle)} (law 17). Usernames are placeholders (`_usernames`). Later builders read this "
              f"run's bundle (idmap {PFX}<spec id>). Generated by push/skyglass_copies.gen.py; do not hand-edit.")
    keys = {e["srcId"] for e in ready}
    m = {"_note": note, "dedupNames": True,
         "_usernames": [f"{e['srcId']}: {e['data']['username']}" for e in ready],
         "_records": ledger(ready),
         "_tail_restated": [k for k in TAIL if PFX + k in keys],
         "_dead_rules_dropped": [d for d in DEAD if PFX + d.split(":")[0] in keys],
         "_blocked_forge_kit_lint": [f"{e['srcId']} ({e['data']['username']}): {e['_blocked_by']}" for e in held],
         "_blocked_rule_cap": blocked,
         "_not_built": skipped,
         "items": [strip(e) for e in ready]}
    path = os.path.join(ROOT, "push", f"{NUM}_skyglass_copies_1.json")
    write(path, m)
    print(f"push/{os.path.basename(path)}: {len(ready)} AI creates {counts}")
    print(f"blocked: {len(held)} (Forge kit lint / after part 2) {counts_of(held)}; {len(blocked)} (20-rule cap); "
          f"not built: {len(skipped)} (cut press-on rooms)")


def main_blocked(lib):
    ready, held, skipped, blocked = partition(lib)
    m = {"_note": (f"push/{NUM} part 3, BLOCKED, DO NOT RUN: Forge refuses it at parse (kit lint: basicAttack rules and "
                   "range gates; push/README.md 344). Written for review only by push/skyglass_copies.gen.py --blocked. "
                   "When unblocked it runs AFTER part 2 (it holds Stonebound Summons) and after push/343."),
         "dedupNames": True, "_usernames": [f"{e['srcId']}: {e['data']['username']}" for e in held],
         "_records": [f"{e['srcId']}: {e['_blocked_by']}" for e in held], "items": [strip(e) for e in held]}
    path = os.path.join(ROOT, "push", f"{NUM}_skyglass_copies_3.json")
    write(path, m)
    print(f"push/{os.path.basename(path)}: {len(held)} AI creates (BLOCKED) {counts_of(held)}")


def summon_edit(lib, bundle):
    """Part 2: Stonebound Summons -> the Stonebound copy (literal id from part 1's bundle)."""
    idmap = json.load(open(bundle)).get("idmap") or {}
    copy_id = idmap.get(PFX + STONEBOUND_KEY)
    if not copy_id or not NANO.match(copy_id):
        raise SystemExit(f"{os.path.basename(bundle)} has no {PFX}{STONEBOUND_KEY}: run part 1 first")
    import importlib.util
    sp = importlib.util.spec_from_file_location("skyglass_library", os.path.join(ROOT, "push/skyglass_library.gen.py"))
    L = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(L)
    rec = next(e for e in L.all_jutsu()[0] if e["srcId"] == LIB_PFX + SUMMON_SRC)["data"]
    assert lib.jutsu(SUMMON_SRC, "summon") == SUMMON_JUTSU
    effects = copy.deepcopy(rec["effects"])  # whole array (edits reproduce whole arrays); only aiId changes
    s = [e for e in effects if e["type"] == "summon"]
    assert len(s) == 1 and s[0]["aiId"] == STONEBOUND_LIVE, s
    s[0]["aiId"] = copy_id
    edit = {"entity": "jutsu", "slot": "edit", "targetId": SUMMON_JUTSU, "name": rec["name"],
            "data": {"effects": effects, "injectableInBattle": False}}  # law 20: sent explicitly, as 342/343 did
    m = {"_note": (f"push/{NUM} part 2, built from part 1's bundle {os.path.basename(bundle)}. Stonebound Summons "
                   f"({SUMMON_JUTSU}) summons the Crown Stonebound copy {copy_id} (Echo of Erupting Ground, enemies "
                   "only; RUL-2026-10-30-060 item 7) instead of the live Crownhold record, at the same 40% / 15000 HP. "
                   "Nothing holds the summon yet, and nothing may until this has run (law 18): the live Sealwright's "
                   "hunts upgrade and the three Sealwright copies (part 3) equip it AFTER. Generated by "
                   "push/skyglass_copies.gen.py --summon; do not hand-edit."),
         "items": [edit]}
    path = os.path.join(ROOT, "push", f"{NUM}_skyglass_copies_2.json")
    write(path, m)
    print(f"push/{os.path.basename(path)}: 1 jutsu edit (Stonebound Summons -> {copy_id})")


def main():
    args = sys.argv[1:]
    bundle = LIB_BUNDLE
    if "--library" in args:
        bundle = args[args.index("--library") + 1]
    lib = Lib(bundle)
    if "--summon" in args:
        return summon_edit(lib, args[args.index("--summon") + 1])
    if "--blocked" in args:
        return main_blocked(lib)
    main_ready(lib)


if __name__ == "__main__":
    main()
