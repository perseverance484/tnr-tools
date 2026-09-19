#!/usr/bin/env python3
"""Build push/49_godstorm_two_pyramid_final_update.json.

Inputs are repository evidence, not hand-transcribed live records:
- push/48_godstorm_current_manifest.json: 3 accepted Stormcourt background
  creates, first four accepted Marrow avatar edits, and 18 audited profile
  safety edits.
- harvests/inbox/tnr_results_1789401726302.json: captured live quest records.
- docs/plans/GODSTORM_STANDALONE_COPY_AND_SCENE_MAP.md: current connected
  50-row dialog copy table.

Director finalization on 2026-09-19 freezes the current connected-setting copy
for this push. Existing numeric completion rewards and quest cadence/attempt
fields are preserved. Obsolete Godstorm item grants are removed because the
keystones are excluded and the shared Endless Night Chest is Tower-branded.

Scene-character arrays remain empty/deferred: no accepted keeper/blank
SCENE_CHARACTER records exist yet. This generator never invents ids.

No live request or write occurs here.
"""
from __future__ import annotations
import copy
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE_MANIFEST = ROOT / "push/48_godstorm_current_manifest.json"
QUEST_CAPTURE = ROOT / "harvests/inbox/tnr_results_1789401726302.json"
COPY_SOURCE = ROOT / "docs/plans/GODSTORM_STANDALONE_COPY_AND_SCENE_MAP.md"
OUT = ROOT / "push/49_godstorm_two_pyramid_final_update.json"

MARROW = "2yvE9PUQqlD8lbYNfgX-b"
STORM = "OSADdXqostbyVliCxWk6k"
M_BG = {
    "M1": "7EmVo6GH5GL4YtQTDrbDR",
    "M2": "oc0cXiMrcG_6kTUwNWRkn",
    "M3": "IykL5XxwFF14BosCblZj8",
}
REMOVE = {
    "d1_choice","d1_cash","d2_choice","d2_cash","d3_choice","d3_cash",
    "d4_choice","d4_cash","d6_choice","d6_cash","d7_choice","d7_cash",
    "d8_choice","d8_cash","d9_choice","d9_cash",
}
REROUTE = {
    "b1_boss":"d2_1","b2_boss":"d3_1","b3_boss":"d4_1","b4_boss":"d5_1",
    "b6_boss":"d7_1","b7_boss":"d8_1","b8_boss":"d9_1","b9_boss":"d10_1",
}
TOP = {
    MARROW: {
        "name":"Marrow Vaults",
        "description":"Beneath Stormcourt lie the Marrow Vaults, where the Unbroken Thread confined the elder sister and studied her light-devouring blood. Enter through the lower vaults and defeat all twenty-five enemies, including the five keepers, to open the passage to the court above.",
        "successDescription":"Marrow Vaults is cleared. The passage to Stormcourt above is open.",
    },
    STORM: {
        "name":"Stormcourt",
        "description":"Above the Marrow Vaults lies Stormcourt, where the Unbroken Thread bound the younger sister's storm. Enter from the cleared vaults below and defeat all twenty-five enemies, including the five keepers. Bring down the Sovereign Echo of the Godstorm to end the binding.",
        "successDescription":"Stormcourt is cleared. The Sovereign Echo is defeated, and the binding is broken.",
    },
}
VICTORY = {
    MARROW: {
        "id":"d5_victory",
        "description":"The Warden of the Half Eclipse falls, leaving the stair beyond the divided threshold unguarded. Thunder rolls down from Stormcourt above. The elder sister's prison is cleared, but the younger sister's storm is still bound in the court overhead. The way up is open.",
        "choice":"Complete Marrow Vaults",
        "winDescription":"The stair to Stormcourt is open.",
        "winSuccess":"Marrow Vaults is cleared. The passage to Stormcourt above is open.",
        "fallDescription":"This attempt ends before Marrow Vaults is cleared.",
    },
    STORM: {
        "id":"d10_victory",
        "description":"The Sovereign Echo collapses. Lightning leaves the empty armor, and the binding instruments fall silent. Rain crosses the upper court without being drawn back toward the dais. For the first time since you entered the vaults below, the thunder carries no voice. The Thread's prison beneath the court and its storm binding above are both broken.",
        "choice":"Leave Stormcourt",
        "winDescription":"You leave Stormcourt as the rain settles over the silent court.",
        "winSuccess":"Stormcourt is cleared. The binding is broken.",
        "fallDescription":"This attempt ends before Stormcourt is cleared.",
    },
}
WARDEN_AVATAR = {
    "name":"Warden of the First Dark avatar",
    "entity":"ai",
    "slot":"edit",
    "targetId":"oi4bHe3upEhLkI-ElJuMX",
    "data":{"avatar":"@img:ai_godstorm_marrow_warden_of_the_first_dark.webp"},
}
WARDEN_FILE = "ai_godstorm_marrow_warden_of_the_first_dark.webp"
WARDEN_BYTES = 238510


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def parse_rows(text: str):
    rows = {}
    rx = re.compile(
        r"^\|\s*(d(?:[1-9]|10)_(?:[1-4]|boss))\s*\|\s*(\d+)\s*/\s*"
        r"([^|]+?)\s*\|\s*([A-Z0-9]+)\s*\|\s*([A-Z0-9]+)\s*\|\s*(.*?)\s*\|\s*$"
    )
    for line in text.splitlines():
        m = rx.match(line)
        if m:
            dialog, num, enemy, bg, char, desc = m.groups()
            rows[dialog] = {
                "number": int(num), "enemy": enemy.strip(), "bg": bg,
                "char": char, "desc": desc.strip(),
            }
    if len(rows) != 50:
        raise SystemExit(f"expected 50 dialog rows, got {len(rows)}")
    return rows


def update_quest(q, qid, rows):
    marrow = qid == MARROW
    q = copy.deepcopy(q)
    q.update(TOP[qid])
    objs = [o for o in q["content"]["objectives"] if o["id"] not in REMOVE]
    by_id = {o["id"]: o for o in objs}
    if len(objs) != 53:
        raise SystemExit(f"{qid}: expected 53 objectives, got {len(objs)}")

    for dialog, row in rows.items():
        belongs = bool(re.match(r"^d[1-5]_", dialog)) if marrow else bool(
            re.match(r"^d(?:6|7|8|9|10)_", dialog)
        )
        if not belongs:
            continue
        d = by_id[dialog]
        d["description"] = row["desc"]
        d["successDescription"] = ""
        d["sceneCharacters"] = []
        if marrow:
            code = "M3" if dialog == "d1_1" else row["bg"]
            d["sceneBackground"] = M_BG[code]
        else:
            d["sceneBackground"] = (
                "@scene:godstorm_sc_dais_active"
                if dialog.startswith("d10_")
                else "@scene:godstorm_sc_upper"
            )

        battle_id = "b" + dialog[1:]
        b = by_id[battle_id]
        b["description"] = f"Battle {row['number']}/25: {row['enemy']}."
        if battle_id.endswith("_boss"):
            b["successDescription"] = (
                "The last keeper falls."
                if battle_id in {"b5_boss", "b10_boss"}
                else "The keeper falls. The next passage is clear."
            )
        else:
            b["successDescription"] = "The guardian falls. You can advance."
        if marrow:
            b["failDescription"] = "You are defeated. Marrow Vaults remains uncleared."
            b["drawDescription"] = "The battle ends in a draw. Marrow Vaults remains uncleared."
            b["fleeDescription"] = "You disengage before clearing Marrow Vaults."
        else:
            b["failDescription"] = "You are defeated. Stormcourt remains uncleared."
            b["drawDescription"] = "The battle ends in a draw. Stormcourt remains uncleared."
            b["fleeDescription"] = "You disengage before clearing Stormcourt."
        if battle_id in REROUTE:
            b["nextObjectiveId"] = REROUTE[battle_id]

    v = VICTORY[qid]
    vd, win, fall = by_id[v["id"]], by_id["win"], by_id["fall"]
    vd["description"] = v["description"]
    vd["successDescription"] = ""
    vd["nextObjectiveId"] = [{"text":v["choice"], "nextObjectiveId":"win"}]
    vd["reward_items"] = []
    vd["sceneCharacters"] = []
    vd["sceneBackground"] = (
        M_BG["M2"] if marrow else "@scene:godstorm_sc_dais_released"
    )
    win["description"], win["successDescription"] = v["winDescription"], v["winSuccess"]
    fall["description"], fall["successDescription"] = v["fallDescription"], ""
    q["content"]["objectives"] = objs
    return q


def assert_quest(q, qid):
    objs = q["content"]["objectives"]
    ids = {o["id"] for o in objs}
    battles = [o for o in objs if o["task"] == "start_battle"]
    dialogs = [o for o in objs if o["task"] == "dialog"]
    if (len(objs), len(battles), len(dialogs)) != (53, 25, 26):
        raise SystemExit(f"{qid}: bad objective counts")
    if ids & REMOVE:
        raise SystemExit(f"{qid}: removed objective survived")
    edges = {}
    for o in objs:
        dest = []
        nxt = o.get("nextObjectiveId")
        if isinstance(nxt, str):
            dest.append(nxt)
        elif isinstance(nxt, list):
            dest.extend(c["nextObjectiveId"] for c in nxt if c.get("nextObjectiveId"))
        if o.get("failObjectiveId"):
            dest.append(o["failObjectiveId"])
        edges[o["id"]] = dest
        for d in dest:
            if d not in ids:
                raise SystemExit(f"{qid}: {o['id']} dangling -> {d}")
    seen, stack = set(), [objs[0]["id"]]
    while stack:
        cur = stack.pop()
        if cur in seen:
            continue
        seen.add(cur)
        stack.extend(edges[cur])
    if seen != ids:
        raise SystemExit(f"{qid}: unreachable objectives {sorted(ids-seen)}")
    text = json.dumps(q)
    for bad in ("Tower of Endless Night", "Dawnless Crown", "cKHhHoboreP88iH5WjDe7"):
        if bad in text:
            raise SystemExit(f"{qid}: forbidden stale token {bad}")
    if re.search(r"Floor \d|cash.?out", text, re.I):
        raise SystemExit(f"{qid}: stale floor/cashout wording")


def main():
    base = load(BASE_MANIFEST)
    cap = load(QUEST_CAPTURE)
    rows = parse_rows(COPY_SOURCE.read_text(encoding="utf-8"))
    qmap = {
        c["data"]["id"]: c["data"]
        for c in cap["captures"]
        if c.get("proc") == "quests.get" and isinstance(c.get("data"), dict)
    }
    marrow = update_quest(qmap[MARROW], MARROW, rows)
    storm = update_quest(qmap[STORM], STORM, rows)
    assert_quest(marrow, MARROW)
    assert_quest(storm, STORM)

    m = copy.deepcopy(base)
    m["_note"] = (
        "Godstorm two-pyramid FINAL UPDATE manifest, 2026-09-19. Push-ready "
        "current release update: creates the three accepted Stormcourt backgrounds; "
        "updates all five missing Marrow AI avatars; applies the audited target/range "
        "safety correction to all 18 retained AI profiles; and updates Marrow Vaults "
        "+ Stormcourt to the approved connected 25+25 structure with all 16 cash-out "
        "dialogs removed, eight keeper reroutes, no Tower/Dawnless identity, revised "
        "battle/outcome copy, approved background wiring, and no keystone/Tower-chest "
        "item grants. Existing numeric completion rewards and quest cadence/attempt "
        "fields are preserved from captured live records. Scene-character arrays "
        "remain empty/deferred because no accepted keeper/blank SCENE_CHARACTER "
        "records exist yet. No live operation is performed by this repository file."
    )
    m["imgSizes"][WARDEN_FILE] = WARDEN_BYTES
    if not any(
        i.get("entity") == "ai" and i.get("targetId") == WARDEN_AVATAR["targetId"]
        for i in m["items"]
    ):
        first_profile = next(
            (n for n,i in enumerate(m["items"]) if i.get("entity") == "aiProfile"),
            len(m["items"]),
        )
        m["items"].insert(first_profile, WARDEN_AVATAR)

    m["items"] = [i for i in m["items"] if i.get("entity") != "quest"]
    m["items"].extend([
        {
            "name":"Marrow Vaults final update", "entity":"quest", "slot":"edit",
            "targetId":MARROW,
            "data":{
                "name":marrow["name"], "description":marrow["description"],
                "successDescription":marrow["successDescription"],
                "content":marrow["content"],
            },
        },
        {
            "name":"Stormcourt final update", "entity":"quest", "slot":"edit",
            "targetId":STORM,
            "data":{
                "name":storm["name"], "description":storm["description"],
                "successDescription":storm["successDescription"],
                "content":storm["content"],
            },
        },
    ])
    m["capture"] = {"after":[
        {"proc":"quests.get","input":{"id":MARROW},"persist":"full"},
        {"proc":"quests.get","input":{"id":STORM},"persist":"full"},
    ]}
    if len(m["items"]) != 28:
        raise SystemExit(f"expected 28 items, got {len(m['items'])}")
    OUT.write_text(json.dumps(m, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {OUT}: 28 items, 8 images, 2 full quest readbacks")


if __name__ == "__main__":
    main()
