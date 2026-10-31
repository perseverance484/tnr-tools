"""Shared helpers for the Skyglass wave-2 generators (not a generator itself; nothing here writes a manifest).

Used by push/skyglass_wreck.gen.py, push/skyglass_crew_upgrade.gen.py, push/skyglass_crownhold_rework.gen.py and
push/skyglass_archive_seal.py. Zero live requests: everything is read from repository files.

Inputs
  - state/skyglass_build/ (harness specs; provenance in its README). Set SKYGLASS_BUILD=<dir> to read another copy,
    e.g. the trimmed specs on fable/skyglass-rule-cap before they reach main (testing only; never commit output built
    from a directory that is not state/skyglass_build/).
  - push/342's results bundle (library jutsu: idmap sg342_<spec id>), law 17: an AI's jutsu array and rules carry
    literal ids.

AI keys (one name per record a dungeon wave or an edit can point at):
  base:<slug>    the live crew record itself, upgraded in place for the endgame Wreck (RUL-2026-10-31-067 item 1).
                 Ids: build_spec.json `endgame.ais[].copyOf.liveAiId`, cross-checked against LIVE_CREW below (push/249
                 capture, push/skyglass_hunts.gen.py AI table).
  faded:<slug>   the easy (level-45) Wreck tier (RUL-2026-10-31-067 item 6), created by the rebuilt push/344. Ids come
                 from 344's results bundle, srcId sg344_faded-<slug>, checked to be an ok AI create named
                 "Faded <Name>" (the convention push/skyglass_charts.gen.py uses for veteran:/rot:).
  <slug> is the harness id without its dg- prefix / -l50 suffix: deck-warden, seal-charge, skyglass-sentinel,
  first-blade, oathkeeper, wayfinder, core-horror, the-captain, sealwright (Faded has no Sealwright).
"""
import copy
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD = os.environ.get("SKYGLASS_BUILD") or os.path.join(ROOT, "state/skyglass_build")
OUT = os.environ.get("SKYGLASS_OUT") or os.path.join(ROOT, "push")  # stand-in runs write elsewhere (never commit)

# Planned push numbers (coordinator 2026-10-31: 361-369 for this block).
NUM = {"crew": 361, "wreck": 362, "cc_jutsu": 363, "cc_ai": 364, "topup": 365, "easy": 366, "unequip": 367}
NANO = re.compile(r"^[A-Za-z0-9_-]{21}$")
BASIC = "basicAttack"  # the engine's basic attack (theninjarpg@3314d122 libs/combat/ai_v2.ts ~494, actions.ts ~512)
MAX_RULES = 20  # AI_PROFILE_MAX_RULES, app/drizzle/constants.ts:1933, enforced by routers/ai.ts:87
BANNED_ACTIONS = {"use_highest_power_action", "use_highest_power_jutsu", "use_highest_power_item", "use_random_jutsu",
                  "use_combo_action"}  # fallback fix, RUL-2026-10-29-046 item 2 / RUL-2026-10-30-060 item 7

LIB_PFX = "sg342_"
LIB_BUNDLE = os.path.join(ROOT, "harvests/inbox/tnr_results_1793426982231.json")  # push/342, 41/41 VERIFIED
LIB_PLACEHOLDER = re.compile(r"^(lib-|hunt-|dg-|chart-embers-)")
COPIES_PFX = "sg344_"
CREW_CAPTURE = os.path.join(ROOT, "harvests/inbox/tnr_results_1792900120886.json")  # push/249 profile.getAi reads

# The live crew (push/249 capture; push/skyglass_hunts.gen.py AI table). base:<slug> -> live AI id.
LIVE_CREW = {
    "deck-warden": "texZaFi42S3EvJZBwQ8cd", "seal-charge": "wTgO-Q32caSSd0is1QIS7",
    "skyglass-sentinel": "3V_gdHYaclMB1gTyOPAbV", "first-blade": "d6g0mOM7RBSsYI1hrUVT9",
    "oathkeeper": "0PZU_FvlbM3ErYGlD5r56", "wayfinder": "v7T9_XdGMfP46em0dPuBc",
    "core-horror": "AQi-bHJ-5tHXtxrnc0P9E", "the-captain": "QY69h271Nx9uHrBeR6jwW",
    "sealwright": "RBW5KsIXmTGR710D2y2Y7",
}
FADED_SLUGS = ("deck-warden", "seal-charge", "skyglass-sentinel", "first-blade", "oathkeeper", "wayfinder",
               "core-horror", "the-captain")

STATS6 = ("offence", "defence", "strength", "intelligence", "willpower", "speed")
MASTERIES = ("ninjutsuMastery", "genjutsuMastery", "taijutsuMastery", "bukijutsuMastery", "bloodlineMastery",
             "sageMastery")

POOL = json.load(open(os.path.join(ROOT, "32b_DATA_pool.json")))["records"]
POOL_BY_ID = {r["id"]: r for r in POOL.values()}


def spec(name):
    return json.load(open(os.path.join(BUILD, name)))


def build_dir_note():
    rel = os.path.relpath(BUILD, ROOT)
    return rel if not rel.startswith("..") else BUILD


def idmap(bundle):
    return json.load(open(bundle)).get("idmap") or {}


def slug(harness_id):
    m = re.match(r"^dg-(.+?)(-l50)?$", harness_id)
    if not m:
        raise SystemExit(f"{harness_id}: not a dg-<slug>[-l50] harness id")
    return m.group(1)


class Ids:
    """Resolves library placeholders (push/342 bundle) and extra placeholder families (e.g. cc-* from another run)."""

    def __init__(self, lib_bundle=LIB_BUNDLE, extra=None):
        self.lib_bundle = lib_bundle
        self.lib = idmap(lib_bundle)
        self.extra = extra or {}  # placeholder -> literal id

    def jutsu(self, jid, where):
        if jid == BASIC:
            return jid
        if jid in self.extra:
            return self.extra[jid]
        if LIB_PLACEHOLDER.match(jid):
            lid = self.lib.get(LIB_PFX + jid)
            if not lid:
                raise SystemExit(f"{where}: {jid} has no {LIB_PFX}{jid} in {os.path.basename(self.lib_bundle)}")
            return lid
        if not NANO.match(jid):
            raise SystemExit(f"{where}: {jid!r} is neither a known placeholder nor a live id")
        return jid


# ------------------------------------------------------------------ AI keys
def base_key_map():
    """base:<slug> -> live id, from build_spec endgame.ais (cross-checked with LIVE_CREW)."""
    out = {}
    for a in spec("build_spec.json")["endgame"]["ais"]:
        s = slug(a["harnessId"])
        lid = a["copyOf"]["liveAiId"]
        if LIVE_CREW.get(s) != lid:
            raise SystemExit(f"build_spec endgame {a['harnessId']}: live id {lid} != LIVE_CREW[{s}] {LIVE_CREW.get(s)}")
        out["base:" + s] = lid
    return out


CREW_NAME = {"deck-warden": "Deck Warden", "seal-charge": "Seal Charge", "skyglass-sentinel": "Skyglass Sentinel",
             "first-blade": "First Blade", "oathkeeper": "Oathkeeper", "wayfinder": "Wayfinder",
             "core-horror": "Core Horror", "the-captain": "The Captain", "sealwright": "Sealwright"}


def faded_name_ok(s, name):
    """RUL-2026-10-31-067 items 5-6: "Faded <Name>"; a leading "The" may be dropped (as push/skyglass_charts.gen.py)."""
    n = CREW_NAME[s]
    return name in ("Faded " + n, "Faded " + re.sub(r"^The ", "", n))


def faded_key_map(bundle, notes):
    """faded:<slug> -> id from push/344's results bundle: srcId sg344_faded-<slug>, an ok AI create named
    "Faded <Name>" (the same checks push/skyglass_charts.gen.py makes for veteran:/rot: keys)."""
    b = json.load(open(bundle))
    im = b.get("idmap") or {}
    entries = {e.get("srcId"): e for e in b.get("entries", []) if e.get("srcId")}
    out, problems = {}, []
    for s in FADED_SLUGS:
        src = f"{COPIES_PFX}faded-{s}"
        i, e = im.get(src), entries.get(src)
        if not NANO.match(i or ""):
            problems.append(f"faded:{s}: srcId {src} has no id in the idmap")
        elif not e or e.get("entity") != "ai" or e.get("slot") != "create" or e.get("state") != "ok" or e.get("id") != i:
            problems.append(f"faded:{s}: srcId {src} is not an ok AI create in the bundle entries")
        elif not faded_name_ok(s, e.get("name")):
            problems.append(f"faded:{s}: {src} is named {e.get('name')!r}, expected 'Faded {CREW_NAME[s]}'")
        else:
            out["faded:" + s] = i
            notes.append(f"faded:{s} = {i} ({e.get('name')})")
    if problems:
        raise SystemExit(f"{os.path.basename(bundle)} (push/344 results?) does not give every Faded record:\n  "
                         + "\n  ".join(problems))
    return out


# ------------------------------------------------------------------ rules
def convert_rule(r, ids, where):
    a = copy.deepcopy(r.get("action") or r.get("do"))
    conds = copy.deepcopy(r["conditions"] if "conditions" in r else r.get("when") or [])
    if a["type"] in BANNED_ACTIONS:
        raise SystemExit(f"{where}: {a['type']} rule (fallback fix, RUL-2026-10-30-060 item 7)")
    if "jutsuId" in a:
        a["jutsuId"] = ids.jutsu(a["jutsuId"], where)
    return {"conditions": conds, "action": a}


def finish_rules(rules, where, notes):
    """Drop rules below an unconditional end_turn (never reached); write out the end_turn tail the engine appends to
    every profile anyway (ai_v2.ts ~273-281 at 3314d122) when there is room under the 20-rule cap."""
    for i, r in enumerate(rules[:-1]):
        if r["action"]["type"] == "end_turn" and not r["conditions"]:
            notes.append(f"{where}: dropped {len(rules) - i - 1} unreachable rule(s) below an unconditional end turn")
            rules = rules[:i + 1]
            break
    last = rules[-1]
    if last["conditions"] or last["action"]["type"] not in ("end_turn", "move_towards_opponent"):
        # includes an unconditional basicAttack: it can fail (e.g. stealthed), and validate.py law 41 wants an
        # unconditional end_turn / move as the last rule
        if len(rules) < MAX_RULES:
            rules = rules + [{"conditions": [], "action": {"type": "end_turn", "description": "End turn"}}]
            notes.append(f"{where}: engine end-turn tail written out (no behaviour change)")
        else:
            notes.append(f"{where}: last rule is not an unconditional end_turn/move and the 20-rule cap leaves no room; "
                         "the engine appends its end-turn tail in battle (ai_v2.ts ~273-281); validate.py law 41 "
                         "flags it: needs a validate_exception ledger (director)")
    return rules


def kit_problems(jutsus, rules):
    """forge/src/runner/pool.mjs kitProblems, ported (same 32b_DATA_pool.json), with the 0.12.3 basicAttack exception
    (RUL-2026-10-31-071 item 1)."""
    eq = set(jutsus)
    out = []
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


def check_ai(where, jutsus, rules):
    if len(rules) > MAX_RULES:
        raise SystemExit(f"{where}: {len(rules)} rules > {MAX_RULES} (AI_PROFILE_MAX_RULES); refresh "
                         f"{build_dir_note()} from the rule-cap re-simulation")
    probs = kit_problems(jutsus, rules)
    if probs:
        raise SystemExit(f"{where}: Forge kit lint would refuse the manifest: {probs}")


# ------------------------------------------------------------------ live crew rows (push/249)
def crew_rows():
    b = json.load(open(CREW_CAPTURE))
    return {c["data"]["userId"]: c["data"] for c in b["captures"]
            if c["proc"] == "profile.getAi" and c.get("ok") and c.get("data")}


def items_of(row):
    # AI items: {ids, number} with number = dropChancePerc (law 69).
    return [{"ids": [it["itemId"]], "number": it.get("dropChancePerc", 0) or 0} for it in (row.get("items") or [])]


def write(path, m):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(m, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(os.path.relpath(path, ROOT), len(m.get("items", [])), "items")
