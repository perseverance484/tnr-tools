#!/usr/bin/env python3
"""Generate push/344: every new Skyglass AI record of the RUL-2026-10-31-077 structure, all HIDDEN.

    python3 push/skyglass_copies.gen.py                          # 344_skyglass_copies_1.json and _3.json
    python3 push/skyglass_copies.gen.py --summon <part 1 bundle>  # 344_skyglass_copies_2.json, AFTER part 1 has run
    --library <342 bundle> reads the library ids from another bundle (default: push/342's run).

Record list: state/skyglass_build/records_spec.json (harness/skyglass_wreck_sim/tools/records.py; one record per
measured tuning; keys and usernames in push/skyglass_aikeys.py KEYS). Every record of kind "copy" is created here with
srcId `sg344_<key with ':' -> '-'>` (push/skyglass_aikeys.py src_id); the live records (base:, live:) are not:
push/361 edits the nine base records in place to the endgame Wreck version.
  - veteran:, common:, rot:, haul:, oneoff:, copy: records: created from the `fullRow` / `fullProfile` of their
    source spec entry (hunts_spec ais, charts_spec newAIs / liveRecords, haul_spec records): the row and rules the
    harness fought. Records shared by several fights have identical rows and rules (tools/records.py checks it).
  - faded: the level-50 Wreck copies, the shared kit (`sharedKits`, lvl50 `ruleVariants`) on the live record's chassis
    with the version's level, multipliers, stats and innate effects (build_spec.json lvl50).
  - oneoff:crown-stonebound: a copy of the live Crown Stonebound (push/272 D3.REG4) whose Erupting Ground is the
    library's enemies-only Echo of Erupting Ground (RUL-2026-10-30-060 item 7, RUL-2026-10-28-026 items 2-3). Part 2
    points Stonebound Summons at it.

Every rule set is the harness's (includeDefaultRules false; the fallback fix is in it: no use_highest_power_* /
use_random_jutsu / use_combo_action rule; the last free pick is the named basic attack `basicAttack`, accepted by Forge
0.12.3 and validate.py, RUL-2026-10-31-071 item 1). The generator refuses: more than 20 rules (AI_PROFILE_MAX_RULES,
app/drizzle/constants.ts:1933), a banned action, a rule firing a jutsu outside the kit, a pool-jutsu distance gate that
is not range+1 (law 40, Forge kitProblems), a duplicate username. Two changes that do not change behaviour: rules
below an unconditional end_turn are dropped (never reached), and a chain that does not end on an unconditional
end_turn / move gets the end_turn the engine appends anyway (ai_v2.ts ~273-281) when the cap leaves room.

Literal ids (law 17): library placeholders (lib-*, hunt-*, dg-*, chart-embers-*) resolve through push/342's results
bundle (idmap keys sg342_<spec id>). Art (RUL-2026-10-30-059): each copy keeps its source's live sprite. Usernames
(law 66; unique, theninjarpg@3314d122 UserData_username_key): push/skyglass_aikeys.py KEYS.

Order (law 18): Stonebound Summons must name the copy BEFORE anything equips it, and the copy's id exists only after
part 1 runs. So: part 1 (every copy except the four holders of the summon, and the Stonebound copy) -> part 2 (the
summon edit, literal id from part 1's bundle) -> part 3 (the four holders: veteran:sealwright, veteran:sealwright-echo,
rot:sealwright, haul:sealwright).

Later builders resolve 344's records by AI key from these runs' bundles (push/skyglass_aikeys.py Resolver).
Do not hand-edit the output.
"""
import copy
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "push"))
import skyglass_aikeys as K  # noqa: E402

BUILD = os.environ.get("SKYGLASS_BUILD") or os.path.join(ROOT, "state/skyglass_build")
OUT = os.environ.get("SKYGLASS_OUT") or os.path.join(ROOT, "push")  # stand-in runs write elsewhere (never commit)
NUM = 344
PFX = K.PFX
LIB_PFX = "sg342_"
LIB_BUNDLE = os.path.join(ROOT, "harvests/inbox/tnr_results_1793426982231.json")  # push/342, 41/41 VERIFIED
NANO = re.compile(r"^[A-Za-z0-9_-]{21}$")
PLACEHOLDER = re.compile(r"^(lib-|hunt-|dg-|chart-embers-)")
BASIC = "basicAttack"  # the engine's basic attack action id (actions.ts ~512); Forge 0.12.3 accepts it (RUL-071)
MAX_RULES = 20  # AI_PROFILE_MAX_RULES, app/drizzle/constants.ts:1933, enforced by routers/ai.ts:87
DEAD = []  # unreachable rules dropped (no behaviour change), reported in the manifests
TAIL = []  # records whose engine-appended end_turn tail is written out (no behaviour change)
NOROOM = []  # records at the cap whose chain has no closing end turn (law 41; the engine appends it)
POOL = json.load(open(os.path.join(ROOT, "32b_DATA_pool.json")))["records"]
POOL_BY_ID = {r["id"]: r for r in POOL.values()}
BANNED_ACTIONS = {"use_highest_power_action", "use_highest_power_jutsu", "use_highest_power_item", "use_random_jutsu",
                  "use_combo_action"}

SUMMON_JUTSU = "bcbOllIWqHEopmQGHKDED"  # Stonebound Summons (push/342 sg342_hunt-called-to-the-archive; 343 text)
SUMMON_SRC = "hunt-called-to-the-archive"
STONEBOUND_LIVE = "jqxu13kNHhfNY-NF68Ftb"  # Crown Stonebound, push/272 crownhold_d3.reg4
ERUPTING_GROUND = "jBRyl7F4UjTyxG5nnzLqj"
ECHO_SRC = "hunt-stonebound-erupting-ground"  # Echo of Erupting Ground (push/342)
STONEBOUND_KEY = "oneoff:crown-stonebound"
SUMMON_HOLDERS = ("veteran:sealwright", "veteran:sealwright-echo", "rot:sealwright", "haul:sealwright")
CREW_272 = os.path.join(ROOT, "archive/spent-manifests/push-2026-10-25/272_crownhold_ais.json")

AI_KEYS = ("username", "hidden", "level", "rank", "poolsMultiplier", "statsMultiplier", "regeneration", "gender",
           "preferredGeneral1", "preferredGeneral2", "primaryElement", "secondaryElement", "isSummon", "avatarFacing",
           "ninjutsuMastery", "genjutsuMastery", "taijutsuMastery", "bukijutsuMastery", "bloodlineMastery",
           "sageMastery", "offence", "defence", "strength", "intelligence", "willpower", "speed", "avatar")
STATS6 = ("offence", "defence", "strength", "intelligence", "willpower", "speed")
MASTERIES = ("ninjutsuMastery", "genjutsuMastery", "taijutsuMastery", "bukijutsuMastery", "bloodlineMastery",
             "sageMastery")


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


def kit_problems(jutsus, rules):
    """forge/src/runner/pool.mjs kitProblems (0.12.3, basicAttack exception RUL-2026-10-31-071 item 1), ported, and the
    20-rule cap. A chain at the cap that does not end on an end turn is allowed (the engine appends one, ai_v2.ts
    ~273-281); it is listed in `_at_cap_no_end_turn` (validate.py law 41)."""
    eq = set(jutsus)
    out = []
    if len(rules) > MAX_RULES:
        out.append(f"{len(rules)} rules > {MAX_RULES} (AI_PROFILE_MAX_RULES)")
    for i, r in enumerate(rules):
        jid = r["action"].get("jutsuId")
        if not jid or jid == BASIC:
            continue
        if jid not in eq:
            out.append(f"rules[{i}]: fires {jid} (not in jutsus)")
        rec = POOL_BY_ID.get(jid)
        if not rec:
            continue
        for c in r["conditions"]:
            if c.get("type") == "distance_lower_than" and rec.get("gate") is not None and c.get("value") != rec["gate"]:
                out.append(f"rules[{i}]: {rec['name']} gate {c.get('value')} != range+1 {rec['gate']}")
    return out


# ------------------------------------------------------------------ records
def items_of(row):
    # AI items: {ids, number} with number = dropChancePerc (law 69). The live crew carry kit items at 0%.
    return [{"ids": [it["itemId"]], "number": 0} for it in (row.get("items") or [])]


def drop_dead_tail(rules, where):
    """Rules below an unconditional end_turn never run (end_turn always executes, ai_v2.ts ~556): drop them."""
    for i, r in enumerate(rules[:-1]):
        if r["action"]["type"] == "end_turn" and not r["conditions"]:
            gone = [x["action"].get("description", x["action"]["type"]) for x in rules[i + 1:]]
            DEAD.append(f"{where}: dropped {len(gone)} unreachable rule(s) below an unconditional end turn: {gone}")
            return rules[:i + 1]
    return rules


def entry(key, data, rules, note):
    data = dict(data)
    rules = drop_dead_tail(rules, key)
    last = rules[-1]
    if last["conditions"] or last["action"]["type"] not in ("end_turn", "move_towards_opponent"):
        if len(rules) < MAX_RULES:
            # ai_v2.ts ~273-281 (3314d122): the engine appends this exact rule to every AI profile that has an effect
            # action available (basic attack always is), so writing it changes nothing and satisfies law 41.
            rules = rules + [{"conditions": [], "action": {"type": "end_turn", "description": "End turn"}}]
            TAIL.append(key)
        else:
            NOROOM.append(key)
    data["hidden"] = True
    data["includeDefaultRules"] = False
    data["rules"] = rules
    probs = kit_problems(data["jutsus"], rules)
    if probs:
        raise SystemExit(f"{key}: Forge would refuse the manifest: {probs}")
    rec = K.RECORDS[key]
    return {"entity": "ai", "slot": "create", "phase": 1, "name": data["username"], "srcId": K.src_id(key),
            "_tier": rec["tier"], "_note": note, "data": data}


def from_full(key, src, lib):
    row, prof = src["fullRow"], src["fullProfile"]
    if prof.get("includeDefaultRules"):
        raise SystemExit(f"{key}: includeDefaultRules on (fallback fix)")
    data = {k: copy.deepcopy(row.get(k)) for k in AI_KEYS}
    data["username"] = K.KEYS[key]
    data["jutsus"] = [lib.jutsu(j, key) for j in row["jutsus"]]
    data["items"] = items_of(row)
    data["effects"] = copy.deepcopy(row.get("effects") or [])
    rules = [rule(r, lib, key) for r in prof["rules"]]
    return data, rules


def source_entry(rec, specs):
    s = rec["source"]
    node = specs[s["spec"]]
    section, sid = s["path"]
    if s["spec"] == "hunts_spec.json":
        return next(a for a in node["ais"] if a["liveId"] == sid)
    return node[section][sid]


def chassis_rows(specs):
    """Live source -> chassis row (the harness's fullRow of a chart copy of that source: avatar, generals, masteries)."""
    rows = {}
    for rec in specs["charts_spec.json"]["newAIs"].values():
        rows.setdefault(rec["username"], rec["fullRow"])
    return rows


def faded(key, rec, lib, specs):
    b = specs["build_spec.json"]
    hid = rec["source"]["path"][2]
    a = next(x for x in b["lvl50"]["ais"] if x["harnessId"] == hid)
    live = a["copyOf"]["liveAi"]
    kit = b["sharedKits"][live]
    assert kit["liveAiId"] == a["copyOf"]["liveAiId"] == rec["copyOf"], key
    row = chassis_rows(specs)[live]
    data = {k: copy.deepcopy(row.get(k)) for k in AI_KEYS}
    data.update({"username": K.KEYS[key], "level": a["level"], "rank": a["rank"],
                 "statsMultiplier": a["statsMultiplier"], "poolsMultiplier": a["poolsMultiplier"]})
    # Stats are ratio weights (law 15): send the version's six stats and the chassis masteries at the same scale, so the
    # ratio is the live one and the server's scaleUserStats lands where the harness did.
    factor = a["stats"]["offence"] / row["offence"]
    for k in STATS6:
        data[k] = a["stats"][k]
    for k in MASTERIES:
        data[k] = max(10, round(row[k] * factor, 2)) if row[k] > 10 else row[k]
    variants = b["lvl50"].get("ruleVariants") or {}
    src_rules = (variants.get(live) or {}).get("rules") or kit["rules"]
    # The kit the harness fought is the jutsu its rules fire (engine/kits.ts kitOf): for a lvl50 rule variant (the
    # Faded Core Horror's hoisted plain attacks) that is not sharedKits' list.
    fought = list(dict.fromkeys(r["action"].get("jutsuId") for r in src_rules
                                if r["action"].get("jutsuId") and r["action"]["jutsuId"] != BASIC))
    if live not in variants:
        assert fought == [j["id"] if isinstance(j, dict) else j for j in kit["jutsu"]], key
    data["jutsus"] = [lib.jutsu(j, hid) for j in fought]
    data["items"] = items_of(row)
    data["effects"] = copy.deepcopy(a["effects"])
    return data, [rule(r, lib, hid) for r in src_rules]


def stonebound(lib, specs):
    m = json.load(open(CREW_272))
    src = next(e for e in m["items"] if e.get("srcId") == "crownhold_d3.reg4")["data"]
    h = next(a for a in specs["hunts_spec.json"]["ais"] if a["liveId"] == STONEBOUND_LIVE)
    swap = {ERUPTING_GROUND: ECHO_SRC}
    # the hunts spec's summon template = push/272 as stored with Erupting Ground swapped for its library copy
    assert [j["id"] for j in h["jutsu"]] == [swap.get(j, j) for j in src["jutsus"]], (h["jutsu"], src["jutsus"])
    data = {k: copy.deepcopy(src.get(k)) for k in AI_KEYS}
    data["username"] = K.KEYS[STONEBOUND_KEY]
    data["jutsus"] = [lib.jutsu(swap.get(j, j), STONEBOUND_KEY) for j in src["jutsus"]]
    data["items"] = []
    data["effects"] = copy.deepcopy(src.get("effects") or [])
    return data, [rule(r, lib, STONEBOUND_KEY, swap) for r in src["rules"]]


def note_of(rec):
    t = rec["tuning"]
    tune = ", ".join(f"{k} {v}" for k, v in t.items() if k != "maxHealth")
    return f"{rec['tier']}; {tune}; used by: " + "; ".join(rec["usedBy"])


def all_copies(lib):
    specs = {n: spec(n) for n in ("build_spec.json", "hunts_spec.json", "charts_spec.json", "haul_spec.json")}
    ents = []
    for key in K.created_keys():
        rec = K.RECORDS[key]
        if key == STONEBOUND_KEY:
            data, rules = stonebound(lib, specs)
        elif key.startswith("faded:"):
            data, rules = faded(key, rec, lib, specs)
        else:
            src = source_entry(rec, specs)
            for alt in rec["source"].get("also", []):  # merged records: the table says identical; re-check
                o = source_entry({"source": alt}, specs)
                strip_ids = lambda r: {k: v for k, v in r.items() if k not in ("userId", "username", "aiProfileId")}
                assert strip_ids(o["fullRow"]) == strip_ids(src["fullRow"]) and \
                    o["fullProfile"]["rules"] == src["fullProfile"]["rules"], (key, alt)
            data, rules = from_full(key, src, lib)
        ents.append(entry(key, data, rules, note_of(rec)))
    names = [e["data"]["username"] for e in ents]
    dup = sorted({n for n in names if names.count(n) > 1})
    if dup:
        raise SystemExit(f"duplicate usernames: {dup}")
    summon = lib.jutsu(SUMMON_SRC, "summon")
    held = tuple(K.src_id(k) for k in SUMMON_HOLDERS)
    holders = tuple(e["srcId"] for e in ents if summon in e["data"]["jutsus"])
    assert sorted(holders) == sorted(held), holders
    return ents, held


def strip(e):
    return {k: v for k, v in e.items() if not k.startswith("_")}


def write(path, m):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(m, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(os.path.relpath(path, ROOT) if path.startswith(ROOT) else path, len(m["items"]), "items")


def counts_of(sel):
    c = {}
    for e in sel:
        c[e["_tier"]] = c.get(e["_tier"], 0) + 1
    return c


def main_parts(lib):
    ents, held = all_copies(lib)
    part1 = [e for e in ents if e["srcId"] not in held]
    part3 = [e for e in ents if e["srcId"] in held]
    common = {"dedupNames": True}
    for n, sel, note in (
            (1, part1, (f"push/{NUM} part 1 (RUL-2026-10-31-077 record structure; RUL-2026-10-30-059 / -066 item 4: hidden, "
                        "live sprites). Every new Skyglass AI record except the four holders of Stonebound Summons: "
                        + ", ".join(f"{c} {t}" for t, c in counts_of(part1).items())
                        + f" = {len(part1)} AI creates, all hidden, includeDefaultRules false, rows and rules as the "
                        "harness fought them (state/skyglass_build/records_spec.json and its source specs). Includes the "
                        "Crown Stonebound copy: part 2 (Stonebound Summons -> the copy) is built from THIS run's bundle "
                        "(python3 push/skyglass_copies.gen.py --summon <bundle>). Library jutsu by literal id from "
                        f"push/342's bundle {os.path.basename(lib.bundle)} (law 17). Usernames: push/skyglass_aikeys.py "
                        "KEYS. Later builders resolve these records by AI key from this run's bundle "
                        "(push/skyglass_aikeys.py). Generated by push/skyglass_copies.gen.py; do not hand-edit.")),
            (3, part3, (f"push/{NUM} part 3: the four records that hold Stonebound Summons ("
                        + ", ".join(e["data"]["username"] for e in part3)
                        + "). RUN ONLY AFTER part 2 (law 18: Stonebound Summons is edited by part 2 and nothing may "
                        "equip it before). All hidden, rows and rules as the harness fought them. Generated by "
                        "push/skyglass_copies.gen.py; do not hand-edit."))):
        keys = {e["srcId"] for e in sel}
        m = {"_note": note, **common,
             "_records": [f"{e['srcId']}: {e['data']['username']} ({e['_note']})" for e in sel],
             "_tail_restated": [k for k in TAIL if K.src_id(k) in keys],
             "_at_cap_no_end_turn": [k for k in NOROOM if K.src_id(k) in keys],
             "_dead_rules_dropped": [d for d in DEAD if K.src_id(d.split(":", 2)[0] + ":" + d.split(":", 2)[1]) in keys],
             "items": [strip(e) for e in sel]}
        write(os.path.join(OUT, f"{NUM}_skyglass_copies_{n}.json"), m)
    print(f"total {len(ents)} new records: part 1 {len(part1)} {counts_of(part1)}; part 3 {len(part3)}")


def summon_edit(lib, bundle):
    """Part 2: Stonebound Summons -> the Stonebound copy (literal id from part 1's bundle)."""
    copy_id = K.Resolver([bundle])(STONEBOUND_KEY)
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
                   "Nothing holds the summon yet, and nothing may until this has run (law 18): part 3 (the four "
                   "Sealwright records) equips it AFTER. Generated by push/skyglass_copies.gen.py --summon; do not "
                   "hand-edit."),
         "items": [edit]}
    write(os.path.join(OUT, f"{NUM}_skyglass_copies_2.json"), m)


def main():
    args = sys.argv[1:]
    bundle = LIB_BUNDLE
    if "--library" in args:
        bundle = args[args.index("--library") + 1]
    lib = Lib(bundle)
    if "--summon" in args:
        return summon_edit(lib, args[args.index("--summon") + 1])
    if [a for a in args if a not in ("--library", bundle)]:
        raise SystemExit(__doc__)
    main_parts(lib)


if __name__ == "__main__":
    main()
