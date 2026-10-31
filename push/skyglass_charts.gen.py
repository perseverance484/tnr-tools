#!/usr/bin/env python3
"""Generate the six new Skyglass chart runs (isolated Battle Pyramids entered with a chart), all HIDDEN.

    python3 push/skyglass_charts.gen.py --keys                    # print the AI keys this generator needs from 344
    python3 push/skyglass_charts.gen.py --copies <344 part 1 bundle> --copies <344 part 3 bundle>
                                                                  # write push/354 and push/355 (AFTER 344 has run)
        [--keymap <json>]        # optional {key: srcId} overrides, if 344 names a copy differently
        [--out-dir <dir>]        # default push/
    python3 push/skyglass_charts.gen.py --stand-in <path>         # TEST ONLY: a fake 344 bundle with made-up ids

  354  the two Common runs: The Low Tide Run (Tide Chart) and The Night Watch (Watch Roster).
  355  the two Epic runs and the two tainted runs: The Sealed Reliquary (Reliquary Seal), The Fall (The Last Heading),
       The Rotted Reliquary (Rotted Reliquary Seal), The Burning Heading (The Rotted Heading).

Neither manifest is committed before push/344 (the RUL-2026-10-31-077 records) has run: every enemy is named by
literal id (L01; Forge's offline plan keeps no idmap), and every record these runs fight is a 344 copy.

AI keys (push/skyglass_aikeys.py; the table is state/skyglass_build/records_spec.json; `--keys` prints them):
  common:<crew>           the Common runs' scaled copies (RUL-2026-10-31-077 item 2b).
  veteran:<crew>[-<use>]  the Epic runs, fixed level 100 (item 2c): the Sealed Reliquary echoes (veteran:foundry-warden,
                          veteran:<crew>-echo), the Fall's crew (veteran:deck-warden / seal-charge, the hunts' records),
                          its break (veteran:core-horror) and helm (veteran:the-captain-fall); the Burning Heading's
                          Deck Warden and Wayfinder and its ally (veteran:the-captain-ally).
  rot:<crew>              Rot-Touched, the tainted runs.
  oneoff:<name>           the three Lingering Echo hazards and the Fall's Arsenal Keeper.
Each key resolves to srcId sg344_<key> in the 344 bundle(s), checked to be an ok AI create named as the table names it
(push/skyglass_aikeys.py Resolver). The cross-check below also requires every fight's spec record (charts_spec runs) to
be the record the table assigns to that key.

Design of record (zero live requests): docs/design/SKYGLASS_TEXT.md section 2 (all player text, node ids, scenes;
read verbatim through push/skyglass_text.py), SKYGLASS_LOOT_TABLES.md 4 / 4a / 5 / 5d (ladder, picks, ending drops),
SKYGLASS_BOSS_FIGHTS.md 8 (twists), state/skyglass_build/charts_spec.json (fights, scaling, givePools, debuffs,
allies; cross-checked below), RUL-2026-10-30-060 item 6 (press-on rooms: kept on the Night Watch, The Fall and the
Rotted Reliquary; cut on the Low Tide Run, the Sealed Reliquary and the Burning Heading), RUL-2026-10-31-067 (tiers),
RUL-2026-10-31-072 (playthrough review: F01 claim line, F03 consolation on a dialog, F17 Core Rot as an ending drop).
Item ids: push/329's results bundle (charts, Core Rot, Galley Stores, Skyglass Token, variant tokens) and
state/skyglass_design/design_data.json; quest icons are the chart icons already uploaded by push/352 (its bundle's
idmap URLs), so nothing is uploaded. Do not hand-edit the output.
"""
import argparse
import importlib.util
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace(".", "_"), os.path.join(ROOT, "push", name))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


T = load("skyglass_text.py")
G = load("skyglass_hunts.gen.py")  # SCENE, STEP_EXP, STEP_N (the hunts' ladder; read only)
sys.path.insert(0, os.path.join(ROOT, "push"))
import skyglass_aikeys as K  # noqa: E402

NUM_COMMON, NUM_EPIC = 354, 355
PFX = {NUM_COMMON: "sg354_", NUM_EPIC: "sg355_"}
COPIES_PFX = "sg344_"
BUNDLE_329 = "harvests/inbox/tnr_results_1793424666625.json"  # push/329, the 22 Skyglass item creates
BUNDLE_352 = "harvests/inbox/tnr_results_1793463647707.json"  # push/352, the chart icons (uploaded URLs)
SPEC = json.load(open(os.path.join(ROOT, "state/skyglass_build/charts_spec.json")))
DESIGN = json.load(open(os.path.join(ROOT, "state/skyglass_design/design_data.json")))
NANO = re.compile(r"^[A-Za-z0-9_-]{21}$")

# ---------------------------------------------------------------------------------------------------------------
# Crew and AI keys
# ---------------------------------------------------------------------------------------------------------------
CREW = {"deck-warden": "Deck Warden", "seal-charge": "Seal Charge", "arsenal-keeper": "Arsenal Keeper",
        "skyglass-sentinel": "Skyglass Sentinel", "oathkeeper": "Oathkeeper", "first-blade": "First Blade",
        "foundry-warden": "Foundry Warden", "sealwright": "Sealwright", "core-horror": "Core Horror",
        "the-captain": "The Captain", "wayfinder": "Wayfinder", "replicant-zero": "Replicant Zero"}
ONEOFF_NAME = {"lingering-echo-i": "Lingering Echo", "lingering-echo-ii": "Lingering Echo",
               "lingering-echo-iii": "Lingering Echo", "fall-arsenal-keeper": "Arsenal Keeper"}


def key_name(key):
    """The crew name a key fights as (for the cross-check against the spec's fight labels)."""
    tier, slug = key.split(":")
    if tier == "oneoff":
        return ONEOFF_NAME[slug]
    return CREW[re.sub(r"-(echo|fall|ally)$", "", slug)]


# ---------------------------------------------------------------------------------------------------------------
# Items
# ---------------------------------------------------------------------------------------------------------------
def _bundle(path):
    return json.load(open(os.path.join(ROOT, path)))


_B329 = {e["srcId"]: e for e in _bundle(BUNDLE_329)["entries"] if e.get("srcId")}


def item329(src):
    e = _B329["sg329_" + src]
    assert e["state"] == "ok" and NANO.match(e["id"]), src
    return e["id"]


DI = {k: v for k, v in DESIGN["items"].items()}


def design(key):
    i = DI[key]["id"]
    assert i and NANO.match(i), key
    return i


ITEM = {
    "Tide Chart": item329("tide_chart"), "Watch Roster": item329("watch_roster"),
    "Reliquary Seal": item329("reliquary_seal"), "The Last Heading": item329("last_heading"),
    "Rotted Reliquary Seal": item329("rotted_reliquary_seal"), "The Rotted Heading": item329("rotted_heading"),
    "Core Rot": item329("core_rot"), "Galley Stores": item329("galley_stores"),
    "Skyglass Token": item329("skyglass_token"),
    "Warden's Forge-Fists": item329("vt_warden"), "Sealwright's Seal": item329("vt_sealwright"),
    "The First Blade": item329("vt_first_blade"), "Wayfinder's Heading": item329("vt_wayfinder"),
    "Medicine Inro": design("medicine_inro"), "Skyglass Coffer": design("skyglass_coffer"),
    "Sealed Treasury": design("sealed_treasury"), "Archive Chart Case": design("archive_chart_case"),
    "Lastlight Lantern": design("lastlight_lantern"), "Chart of the Buried Cache": design("chart_buried_cache"),
}
# The design data records the 329 ids it knows; they must agree with the bundle.
for k, n in (("chart_tide", "Tide Chart"), ("chart_watch_roster", "Watch Roster"), ("galley_stores", "Galley Stores"),
             ("skyglass_token", "Skyglass Token"), ("chart_reliquary_seal", "Reliquary Seal"),
             ("chart_last_heading", "The Last Heading"), ("chart_rotted_reliquary", "Rotted Reliquary Seal"),
             ("chart_burning_heading", "The Rotted Heading")):
    assert DI[k]["id"] == ITEM[n], k

ICONS = _bundle(BUNDLE_352)["idmap"]
ICON = {"Tide Chart": "icon-tide-chart.webp", "Watch Roster": "icon-watch-roster.webp",
        "Reliquary Seal": "icon-reliquary-seal.webp", "The Last Heading": "icon-the-last-heading.webp",
        "Rotted Reliquary Seal": "icon-rotted-reliquary-seal.webp", "The Rotted Heading": "icon-the-rotted-heading.webp"}


def drop(name, chance, quantity=1):
    return {"ids": [ITEM[name]], "number": chance, "quantity": quantity}


# ---------------------------------------------------------------------------------------------------------------
# Rewards (loot tables 4, 4a, 5, 5d; RUL-2026-10-31-072 F03 / F17)
# ---------------------------------------------------------------------------------------------------------------
# Ladder per ending (loot tables 4): Low Tide I; Night Watch II (III if pressed on); Sealed Reliquary, The Fall and
# the tainted runs VI. Exp from the hunts' STEP_EXP; Sealed Treasury at the step number %.
PICK = {
    "lowtide": [("Medicine Inro", 1), ("Galley Stores", 1), ("Watch Roster", 1)],
    "nightwatch": [("Medicine Inro", 1), ("Galley Stores", 1), ("Tide Chart", 1)],
    "reliquary": [("Skyglass Coffer", 2), ("Sealed Treasury", 1), ("Skyglass Token", 2), ("Archive Chart Case", 2)],
    "fall": [("Skyglass Coffer", 2), ("Sealed Treasury", 1), ("Skyglass Token", 2), ("Galley Stores", 3)],
}
PICK["rotted"], PICK["burning"] = PICK["reliquary"], PICK["fall"]  # pick 2 from their Epic run's options
COMMON_END = [drop("Chart of the Buried Cache", 10), drop("Core Rot", 15)]            # loot tables 5 ladder; Core Rot
EPIC_END = [drop("Lastlight Lantern", 15)]                                              # Sealed Reliquary / Fall ending
TAINTED_END = [drop("Lastlight Lantern", 30), drop("Core Rot", 40)]                     # 4a tainted row
# Boss variant tokens (5d): "2% rares, 4% tainted" (the 5d table's "rares" are the Epic runs), each on his own runs.
RELIQUARY_TOKENS = ["Warden's Forge-Fists", "Sealwright's Seal", "The First Blade"]
ENDING = {
    "lowtide": COMMON_END,
    "nightwatch": COMMON_END,
    "reliquary": EPIC_END + [drop(t, 2) for t in RELIQUARY_TOKENS],
    # F17 (RUL-2026-10-31-072 item 8): the Core Horror's 40% Core Rot is an ending drop on The Fall, the Rotted
    # Reliquary and the Burning Heading (battles carry no rewards, RUL-2026-10-28-022).
    "fall": EPIC_END + [drop("Core Rot", 40)],
    "rotted": TAINTED_END + [drop(t, 4) for t in RELIQUARY_TOKENS],
    "burning": TAINTED_END + [drop("Wayfinder's Heading", 4)],
}
# A won press-on room: the Night Watch climbs one ladder step (II -> III); The Fall's room drops its tainted chart 5%
# (loot tables 5, "Pressing on"). The Rotted Reliquary's Replicant Zero room is cut (RUL-2026-10-31-075).
PRESS_STEP = {"nightwatch": "III", "fall": "VI"}
PRESS_EXTRA = {"nightwatch": [], "fall": [drop("The Rotted Heading", 5)]}
# F03 (RUL-2026-10-31-072 item 3): a failed Epic run's 1 Core Rot (RUL-2026-10-28-019) is paid on a dialog step the
# fail route reaches before the fail ending (the engine pays nothing on fail_quest, theninjarpg@3314d122
# libs/quest.ts ~1514-1525). Only the Epic runs: the text doc marks only their f_lost "(pays 1 Core Rot)".
CONSOLATION = {}  # cut by RUL-2026-10-31-080 (director 2026-10-31: failed Epic runs pay nothing); F03 code kept inert

# ---------------------------------------------------------------------------------------------------------------
# Runs: node order follows SKYGLASS_TEXT.md section 2; fights follow charts_spec.json `runs` (cross-checked).
# ---------------------------------------------------------------------------------------------------------------
RUNS = {
    "lowtide": {
        "quest": "The Low Tide Run", "chart": "Tide Chart", "num": NUM_COMMON, "rank": "C", "scaled": True,
        "step": "I", "pickCount": 1,
        "nodes": [("d_breach", "b1"), ("d_hold", "b2"), ("d_beach", "b3")],
        "fights": {"b1": ["common:deck-warden", "common:seal-charge"], "b2": ["common:arsenal-keeper"],
                   "b3": ["common:skyglass-sentinel"]},
        "spec": "lowtide", "press": None},
    "nightwatch": {
        "quest": "The Night Watch", "chart": "Watch Roster", "num": NUM_COMMON, "rank": "C", "scaled": True,
        "step": "II", "pickCount": 1,
        "nodes": [("d_post", "b1"), ("d_middle", "b2"), ("d_last", "b3")],
        "fights": {"b1": ["common:deck-warden", "common:seal-charge"], "b2": ["common:oathkeeper"],
                   "b3": ["common:deck-warden", "common:oathkeeper"], "b_press": ["common:first-blade"]},
        "spec": "nightwatch", "press": "b_press"},
    "reliquary": {
        "quest": "The Sealed Reliquary", "chart": "Reliquary Seal", "num": NUM_EPIC, "rank": "S", "scaled": False,
        "step": "VI", "pickCount": 1,
        "nodes": [("d_open", "b1"), ("d_after1", "b2"), ("d_after2", "b3"), ("d_after3", "b4")],
        "fights": {"b1": ["veteran:foundry-warden"], "b2": ["veteran:sealwright-echo", "oneoff:lingering-echo-i"],
                   "b3": ["veteran:skyglass-sentinel-echo", "oneoff:lingering-echo-ii"],
                   "b4": ["veteran:first-blade-echo", "oneoff:lingering-echo-iii"]},
        "spec": "reliquary", "press": None},
    "fall": {
        "quest": "The Fall", "chart": "The Last Heading", "num": NUM_EPIC, "rank": "S", "scaled": False,
        "step": "VI", "pickCount": 1,
        "nodes": [("d_aboard", "b1"), ("d_gundeck", "b2"), ("d_break", "b3")],
        "fights": {"b1": ["veteran:deck-warden", "veteran:seal-charge"],
                   "b2": ["oneoff:fall-arsenal-keeper", "veteran:deck-warden"], "b3": ["veteran:core-horror"],
                   "b_press": ["veteran:the-captain-fall"]},
        "spec": "fall", "press": "b_press"},
    "rotted": {
        "quest": "The Rotted Reliquary", "chart": "Rotted Reliquary Seal", "num": NUM_EPIC, "rank": "S",
        "scaled": False, "step": "VI", "pickCount": 2,
        "nodes": [("d_open", "b1"), ("d_pair2", "b2")],
        "fights": {"b1": ["rot:foundry-warden", "rot:sealwright"],
                   "b2": ["rot:skyglass-sentinel", "rot:first-blade", "oneoff:lingering-echo-i"]},
        "spec": "rotted", "press": None},  # Replicant Zero's room cut (RUL-2026-10-31-075)
    "burning": {
        "quest": "The Burning Heading", "chart": "The Rotted Heading", "num": NUM_EPIC, "rank": "S", "scaled": False,
        "step": "VI", "pickCount": 2,
        "nodes": [("d_break", "b1"), ("d_captain", "b2"), ("d_gangway", "b3")],
        "fights": {"b1": ["rot:core-horror"], "b2": ["oneoff:fall-arsenal-keeper", "veteran:deck-warden"],
                   "b3": ["veteran:wayfinder"]},
        "allies": {"b2": ["veteran:the-captain-ally"], "b3": ["veteran:the-captain-ally"]},
        "spec": "burning", "press": None},
}
# Tainted twists (charts_spec objectiveShape; Boss Fights 8; loot tables 5): entry at 70% pools on the FIRST fight only
# (a later givePools would replace the carried pools), and the run's debuff on every fight.
TAINT = SPEC["params"]["tainted"]
GIVE_POOLS = {"rotted": TAINT["givePools"], "burning": TAINT["givePools"]}
DEBUFF = {r: SPEC["runs"][r]["fights"][0]["debuffs"] for r in ("rotted", "burning")}
assert DEBUFF["rotted"][0]["type"] == "elementalseal" and DEBUFF["rotted"][0]["rounds"] == TAINT["sealRounds"]
assert DEBUFF["burning"][0]["type"] == "afterburn" and DEBUFF["burning"][0]["power"] == TAINT["afterburn"]
assert DEBUFF["burning"][0]["rounds"] == TAINT["afterburnRounds"] == 7  # RUL-2026-10-30-062 item 1
assert GIVE_POOLS["rotted"] == 70
# Press-on rooms cut by RUL-2026-10-30-060 item 6 (the spec still lists them as "(proposed)", review F20): never built.
CUT_PRESS_ON = {"lowtide", "reliquary", "burning", "rotted"}  # rotted: RUL-2026-10-31-075

SHARED = {"failDescription": "You are defeated.", "drawDescription": "The fight stalls, and the chart's way closes.",
          "fleeDescription": "You break away, and the way back closes behind you."}  # text doc section 2, shared lines
PRESS_FAIL = "You fall back, and keep only what you held."
# RUL-2026-10-31-072 item 1 (F01): every chart run's text carries the claim line. It was read from the Lantern's item
# text; RUL-2026-10-31-074 replaced that card, so the text doc now holds it as its own target (section 2).
CLAIM_LINE = "Claim any reward choice still waiting from an earlier run before you set out."
assert CLAIM_LINE == T.block("quest:<chart run>.claimLine")
# Text the doc does not have yet (F03's consolation step is new): used only while the doc lacks the target; every use
# is listed in the manifest's `_text_gaps` for the text owner.
GAP_TEXT = {
    "d_rot.choice": "Leave the wreck",
    "f_lost.after_rot": "The run is over.",
}
FAIL_ID, ROT_ID = "f_lost", "d_rot"


def cross_check():
    """The fight table above must equal the charts spec's fights (crew names per fight, in order), minus the cut
    press-on rooms, with the spec's scaling and allies. Fails loudly if the re-simulated spec changes a fight."""
    for run, r in RUNS.items():
        fights = SPEC["runs"][r["spec"]]["fights"]
        base = [f for f in fights if not f.get("pressOn")]
        press = [f for f in fights if f.get("pressOn")]
        bids = [b for _, b in r["nodes"]]
        assert len(base) == len(bids), run
        pairs = list(zip(bids, base))
        if run in CUT_PRESS_ON:
            # cut rooms: the spec marks them "(proposed)", except the Rotted Reliquary's, cut later by RUL-2026-10-31-075
            assert r["press"] is None and all("(proposed)" in f["label"] or run == "rotted" for f in press), run
        else:
            # (the spec labels The Fall's kept room "(proposed)" too; RUL-060 item 6 decides, not the label)
            assert r["press"] and len(press) == 1, run
            pairs.append((r["press"], press[0]))
        for b, f in pairs:
            ours = sorted(key_name(k) for k in r["fights"][b])
            theirs = sorted(x["name"] for x in f["ids"])
            assert ours == theirs, (run, b, ours, theirs)
            assert bool(f.get("scaled")) == r["scaled"], (run, b)
            allies = sorted(key_name(k) for k in r.get("allies", {}).get(b, []))
            assert allies == sorted(a["name"] for a in f.get("allies", [])), (run, b)
            # every fighter is the record the RUL-077 table assigns to its key (charts_spec newAIs / liveRecords)
            for side, keys, xs in (("enemy", r["fights"][b], f["ids"]), ("ally", r.get("allies", {}).get(b, []),
                                                                         f.get("allies", []))):
                spec_keys = sorted(K.key_of_source("charts_spec.json", "newAIs" if x["id"] in SPEC["newAIs"]
                                                   else "liveRecords", x["id"]) or f"(no record for {x['id']})"
                                   for x in xs)
                assert sorted(keys) == spec_keys, (run, b, side, sorted(keys), spec_keys)


def all_keys():
    keys = []
    for r in RUNS.values():
        for ks in list(r["fights"].values()) + list(r.get("allies", {}).values()):
            for k in ks:
                if k not in keys:
                    keys.append(k)
    return keys


# ---------------------------------------------------------------------------------------------------------------
# Resolve AI keys
# ---------------------------------------------------------------------------------------------------------------
def resolve(bundles, keymap):
    R = K.Resolver(bundles, keymap)
    ids, report = {}, []
    for k in all_keys():
        ids[k] = R(k)
        report.append((k, K.src_id(k), ids[k], K.KEYS[k]))
    return ids, report


# ---------------------------------------------------------------------------------------------------------------
# Text
# ---------------------------------------------------------------------------------------------------------------
GAPS = []


def text(quest, node, field="description"):
    return T.block(f"obj:{quest}/{node}.{field}")


def has(target):
    try:
        T.block(target)
        return True
    except KeyError:
        return False


def scene_of(quest, node, prev):
    head = "**`obj:" + quest + "/" + node + ".description`**"
    line = next(l for l in T.lines() if l.startswith(head))
    m = re.search(r"\(scene: ([a-z_]+)\)", line)
    return m.group(1) if m else prev


# ---------------------------------------------------------------------------------------------------------------
# Objectives
# ---------------------------------------------------------------------------------------------------------------
def dialog(i, scene, desc, choices, reward_items=None):
    o = {"id": i, "task": "dialog", "description": desc, "sceneBackground": G.SCENE[scene], "sceneCharacters": [],
         "nextObjectiveId": [{"text": t, "nextObjectiveId": n} for t, n in choices]}
    if reward_items:
        o["reward_items"] = reward_items
    return o


def opp(keys, ids):
    counts = {}
    for k in keys:
        counts[ids[k]] = counts.get(ids[k], 0) + 1
    return [{"ids": [i], "number": n, "quantity": 1} for i, n in counts.items()]


def battle(i, scene, desc, run, r, ids, nxt, fail, first):
    o = {"id": i, "task": "start_battle", "description": desc, "sceneBackground": G.SCENE[scene],
         "sceneCharacters": [], "opponentAIs": opp(r["fights"][i], ids), "completionOutcome": "Win", "scaleGains": 1,
         "keepOriginalPools": False, "opponent_scaled_to_user": r["scaled"], "nextObjectiveId": nxt,
         "failObjectiveId": fail, **SHARED}
    if r.get("allies", {}).get(i):
        o["allyAIs"] = [{"ids": [ids[k]], "number": 1} for k in r["allies"][i]]
    if first and run in GIVE_POOLS:
        o["givePools"] = GIVE_POOLS[run]
    if run in DEBUFF:
        o["applyDebuffs"] = json.loads(json.dumps(DEBUFF[run]))
    return o


def win(i, scene, desc, step, drops):
    return {"id": i, "task": "win_quest", "description": desc, "sceneBackground": G.SCENE[scene],
            "sceneCharacters": [], "reward_exp": G.STEP_EXP[step],
            "reward_items": [drop("Sealed Treasury", G.STEP_N[step])] + [dict(d) for d in drops]}


def objectives(run, r, ids):
    q = r["quest"]
    objs, scene = [], None
    fail = ROT_ID if run in CONSOLATION else FAIL_ID
    nodes = r["nodes"]
    for n, (d, b) in enumerate(nodes):
        scene = scene_of(q, d, scene)
        ch = T.choices(f"obj:{q}/{d}.description")
        assert len(ch) == 1, (q, d, ch)
        objs.append(dialog(d, scene, text(q, d), [(ch[0], b)]))
        nxt = nodes[n + 1][0] if n + 1 < len(nodes) else ("d_landing" if r["press"] else "w_done")
        objs.append(battle(b, scene, text(q, b), run, r, ids, nxt, fail, n == 0))
    if r["press"]:
        scene = scene_of(q, "d_landing", scene)
        ch = T.choices(f"obj:{q}/d_landing.description")
        assert len(ch) == 2, (q, ch)
        objs.append(dialog("d_landing", scene, text(q, "d_landing"), [(ch[0], "w_leave"), (ch[1], "b_press")]))
        b = battle("b_press", scene, text(q, "b_press"), run, r, ids, "w_press", "w_leave", False)
        b["failDescription"] = PRESS_FAIL  # text doc section 2: the press-on loss routes to the current step's ending
        objs.append(b)
        objs.append(win("w_leave", scene, text(q, "w_leave"), r["step"], ENDING[run]))
        objs.append(win("w_press", scene, text(q, "w_press"), PRESS_STEP[run], ENDING[run] + PRESS_EXTRA[run]))
    else:
        objs.append(win("w_done", scene, text(q, "w_done"), r["step"], ENDING[run]))
    first_scene = scene_of(q, nodes[0][0], None)
    lost = text(q, FAIL_ID)
    if run in CONSOLATION:
        # The doc's f_lost text narrates the Rot being paid, so it goes on the paying dialog; the fail ending after it
        # takes the doc's own text for the new nodes once it exists.
        if has(f"obj:{q}/{ROT_ID}.description"):
            rot_desc, rot_choice = text(q, ROT_ID), T.choices(f"obj:{q}/{ROT_ID}.description")[0]
            end_desc = lost
        else:
            rot_desc, rot_choice, end_desc = lost, GAP_TEXT["d_rot.choice"], GAP_TEXT["f_lost.after_rot"]
            GAPS.append(f"obj:{q}/{ROT_ID}: description = the doc's f_lost text (pays 1 Core Rot); choice[0] "
                        f"{rot_choice!r} and f_lost {end_desc!r} are placeholders until SKYGLASS_TEXT.md has the "
                        "consolation step (RUL-2026-10-31-072 F03)")
        objs.append(dialog(ROT_ID, first_scene, rot_desc, [(rot_choice, FAIL_ID)], CONSOLATION[run]))
        objs.append({"id": FAIL_ID, "task": "fail_quest", "description": end_desc,
                     "sceneBackground": G.SCENE[first_scene], "sceneCharacters": []})
    else:
        objs.append({"id": FAIL_ID, "task": "fail_quest", "description": lost,
                     "sceneBackground": G.SCENE[first_scene], "sceneCharacters": []})
    return objs


def quest(run, r, ids):
    q = r["quest"]
    desc = T.block(f"quest:{q}.description")
    if CLAIM_LINE not in desc:
        desc += "\n\n" + CLAIM_LINE
    reward = {"reward_items": [{"ids": [ITEM[n]], "number": 100, "quantity": qn} for n, qn in PICK[run]]}
    return {"entity": "quest", "slot": "create", "srcId": PFX[r["num"]] + run, "name": q, "data": {
        "name": q, "description": desc, "image": ICONS[ICON[r["chart"]]], "questType": "battlepyramid",
        "questRank": r["rank"], "successDescription": T.block(f"quest:{q}.successDescription"),
        "retryDelay": "none", "attemptDelay": "none", "consecutiveObjectives": True, "hidden": True,
        "requiredLevel": 1, "maxLevel": 100, "maxAttempts": 100, "maxCompletes": 100, "prerequisiteQuestId": None,
        "tierLevel": None, "requiredVillage": None, "requiredBloodlineId": None, "startsAt": None, "endsAt": None,
        "content": {"objectives": objectives(run, r, ids), "sceneBackground": "", "sceneCharacters": [],
                    "entryItems": [{"ids": [ITEM[r["chart"]]], "number": 1}], "isolated": True,
                    "rewardMode": "choose", "rewardPickCount": r["pickCount"], "reward": reward}}}


# ---------------------------------------------------------------------------------------------------------------
# Manifests
# ---------------------------------------------------------------------------------------------------------------
# Settled by the director 2026-10-31 (RUL-2026-10-31-075): questRank C for the Common runs and S for the Epic and
# tainted runs; the tainted runs pay no failed-run Core Rot; the Rotted Reliquary's press-on room is cut.
DECIDED = ["RUL-2026-10-31-075: questRank C (Common runs) / S (Epic, tainted); tainted runs pay no failed-run Core "
           "Rot; the Rotted Reliquary's press-on room is cut."]


def write(num, slug, note, items, out_dir, extra):
    m = {"_note": note + " Generated by push/skyglass_charts.gen.py; do not hand-edit.", "dedupNames": True}
    m.update(extra)
    m["items"] = items
    path = os.path.join(out_dir, f"{num}_{slug}.json")
    with open(path, "w") as f:
        json.dump(m, f, indent=1, ensure_ascii=False)
        f.write("\n")
    for it in items:
        print(f"{os.path.relpath(path, ROOT) if path.startswith(ROOT) else path}: {it['name']} "
              f"({len(it['data']['content']['objectives'])} objectives)")


def build(bundle, keymap, out_dir):
    cross_check()
    ids, report = resolve(bundle, keymap)
    src = ", ".join(os.path.basename(b) for b in bundle)
    roster = {k: {"id": i, "from": s, "name": n} for k, s, i, n in report}
    for num, slug, runs, what in (
            (NUM_COMMON, "skyglass_chart_runs_common", ("lowtide", "nightwatch"),
             "the two Common chart runs, The Low Tide Run (Tide Chart) and The Night Watch (Watch Roster): the Common "
             "copies scaled to the player (RUL-2026-10-31-077 item 2b), no press-on room on the Low Tide Run, the Second "
             "Watch on the Night Watch"),
            (NUM_EPIC, "skyglass_chart_runs_epic", ("reliquary", "fall", "rotted", "burning"),
             "the two Epic runs (The Sealed Reliquary, The Fall: Veteran records, fixed) and the two tainted runs (The "
             "Rotted Reliquary, The Burning Heading: Rot-Touched records, fixed, 70% entry pools, pick 2)")):
        GAPS.clear()
        items = [quest(r, RUNS[r], ids) for r in runs]
        used = {k for r in runs for ks in list(RUNS[r]["fights"].values()) + list(RUNS[r].get("allies", {}).values())
                for k in ks}
        extra = {"_ai_keys": {k: v for k, v in roster.items() if k in used}, "_copies_bundle": src}
        if GAPS:
            extra["_text_gaps"] = list(GAPS)
        extra["_decided"] = DECIDED
        write(num, slug, (
            f"push/{num}: {what}. All HIDDEN, isolated Battle Pyramids entered with the chart (spent at start), a lost "
            "fight fails the run, completion pick (rewardMode choose). Enemies by literal id, by AI key "
            f"(push/skyglass_aikeys.py) from push/344's results bundle {src} (L01). Text: SKYGLASS_TEXT.md "
            "section 2, plus the Lantern's claim line on every run (RUL-2026-10-31-072 item 1). Rewards: loot tables "
            "4 / 4a / 5 / 5d (ladder, picks, ending drops); F03 consolation and F17 Core Rot per RUL-2026-10-31-072."),
            items, out_dir, extra)


def stand_in(path):
    """TEST ONLY: a fake 344 results bundle naming every created key, with made-up ids."""
    K.stand_in(path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--keys", action="store_true")
    ap.add_argument("--copies", action="append", default=[], help="a push/344 results bundle (repeat: parts 1 and 3)")
    ap.add_argument("--keymap")
    ap.add_argument("--out-dir", default=os.path.join(ROOT, "push"))
    ap.add_argument("--stand-in")
    a = ap.parse_args()
    if a.keys:
        cross_check()
        for k in all_keys():
            print(f"{k:32} {K.src_id(k):40} {K.KEYS[k]}")
        return
    if a.stand_in:
        stand_in(a.stand_in)
        return
    if not a.copies:
        ap.error("needs --copies <344 results bundle> (the chart runs name 344's records by literal id), or --keys")
    keymap = json.load(open(a.keymap)) if a.keymap else {}
    build(a.copies, keymap, a.out_dir)


if __name__ == "__main__":
    main()
