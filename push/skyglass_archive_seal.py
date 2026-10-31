#!/usr/bin/env python3
"""The Quarantined Archive's "break the seal" echo fight (SKYGLASS_LOOT_TABLES.md section 5; RUL-2026-10-31-072
item 8 / playthrough review F15), as a function the go-live build (push/339) calls. Not a generator: it writes no
manifest. 339 re-sends the Archive whole, so the fight must be built INSIDE 339's Archive record, never as a separate
edit (a separate edit would be erased at go-live).

How push/skyglass_update.gen.py should include it (its owner applies this; this module does not edit that file):

    SEAL = load("skyglass_archive_seal.py")                       # same loader as the other push/*.py modules
    def archive():
        objs = G.archive()
        ...existing text, closing lines and drops...
        SEAL.break_the_seal(objs, echo_ai=<the echo's AI id>, core_rot=R("Core Rot"))   # before G.quest(...)
        ...

`echo_ai` is a literal id (L01). Which record fights is NOT settled (see OPEN below); until it is, pass the id the
director picks. `core_rot` is push/329's Core Rot (KuqLeFB12BdB-0s5O1udk).

Shape (both routes; the alarm route's nodes carry the suffix _a):
    d_entry   (+ choice "Break the seal")  ->  d_break      dialog: the warning (an extra fight; health and chakra carry)
                                           ->  b_break      start_battle vs the echo; a loss fails the run (the run's
                                                            fail ending, as every other fight)
                                           ->  d_break_rot  dialog paying Core Rot x2, guaranteed (reward_items 100%;
                                                            a reward on a dialog step, as RUL-2026-10-31-072 item 3 does)
                                           ->  the node d_entry's first choice led to (d_records / d_sealwright_a)
The fight is optional and costs carried health before the Sealwright, which is the trade.

Text: read from docs/design/SKYGLASS_TEXT.md under the targets below when they exist (`obj:The Quarantined
Archive/<node>.description`, choices via `- `choice[n]``). SKYGLASS_TEXT.md has none yet (F15), so the function uses
PLACEHOLDER text and reports every gap in the returned list; 339 must not go live with gaps (pass strict=True to
refuse instead).

OPEN (director): the echo's AI record (not simulated by the harness; a Veteran crew copy from the rebuilt push/344,
e.g. veteran:core-horror, is the natural candidate); the placeholder text; whether the choice is offered on the alarm
route too (built on both here, as the loot table does not restrict it).

    python3 push/skyglass_archive_seal.py --demo     # applies it to push/skyglass_hunts.gen.py's Archive, prints nodes
"""
import importlib.util
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_s = importlib.util.spec_from_file_location("skyglass_text", os.path.join(ROOT, "push/skyglass_text.py"))
T = importlib.util.module_from_spec(_s); _s.loader.exec_module(T)

RUN = "The Quarantined Archive"
CORE_ROT_QTY = 2
PLACEHOLDER = {
    "choice": "Break the seal",
    "d_break": ("Behind the last seal something older presses against the plate, an echo the Core could not hold. "
                "Breaking it will cost you before the Sealwright, and what spills out is rot."),
    "d_break.choice": "Break it",
    "b_break": "The seal splits, and the echo behind it steps out.",
    "d_break_rot": "The echo comes apart into dark, wet timber and cloudy skyglass. You gather what the rot left.",
    "d_break_rot.choice": "Go on",
}


def _text(key, gaps, strict):
    node, _, part = key.partition(".")
    target = f"obj:{RUN}/{node}.description"
    try:
        if part == "choice":
            ch = T.choices(target)
            if ch:
                return ch[0]
            raise KeyError(target)
        return T.block(target)
    except (KeyError, StopIteration):
        if strict:
            raise SystemExit(f"SKYGLASS_TEXT.md has no {target!r} ({key}); break-the-seal text is missing")
        gaps.append(f"{key}: no SKYGLASS_TEXT.md text under {target!r}; PLACEHOLDER used")
        return PLACEHOLDER[key]


def _choice_text(gaps, strict):
    try:
        ch = T.choices(f"obj:{RUN}/d_entry.description")
        if len(ch) >= 3:
            return ch[2]
        raise KeyError
    except (KeyError, StopIteration):
        if strict:
            raise SystemExit("SKYGLASS_TEXT.md has no break-the-seal choice under d_entry")
        gaps.append("d_entry choice: no SKYGLASS_TEXT.md text; PLACEHOLDER used")
        return PLACEHOLDER["choice"]


def break_the_seal(objs, echo_ai, core_rot, strict=False, routes=("", "_a")):
    """Insert the break-the-seal branch into the Archive's objective list `objs` (in place). Returns the text gaps."""
    by = {o["id"]: o for o in objs}
    fail = [o for o in objs if o["task"] == "fail_quest"]
    assert len(fail) == 1, [o["id"] for o in fail]
    fail_id = fail[0]["id"]
    gaps = []
    t = {k: _text(k, gaps, strict) for k in PLACEHOLDER if k != "choice"}
    choice = _choice_text(gaps, strict)
    new = []
    for sfx in routes:
        entry = by["d_entry" + sfx]
        assert entry["task"] == "dialog"
        if any(c["nextObjectiveId"] == "d_break" + sfx for c in entry["nextObjectiveId"]):
            continue  # already applied
        cont = entry["nextObjectiveId"][0]["nextObjectiveId"]
        scene = entry.get("sceneBackground", "")
        entry["nextObjectiveId"] = entry["nextObjectiveId"] + [{"text": choice, "nextObjectiveId": "d_break" + sfx}]
        new.append({"id": "d_break" + sfx, "task": "dialog", "description": t["d_break"], "sceneBackground": scene,
                    "sceneCharacters": [], "nextObjectiveId": [{"text": t["d_break.choice"],
                                                                "nextObjectiveId": "b_break" + sfx}]})
        new.append({"id": "b_break" + sfx, "task": "start_battle", "description": t["b_break"],
                    "sceneBackground": scene, "sceneCharacters": [],
                    "opponentAIs": [{"ids": [echo_ai], "number": 1, "quantity": 1}],
                    "completionOutcome": "Win", "scaleGains": 1, "keepOriginalPools": False,
                    "opponent_scaled_to_user": False, "nextObjectiveId": "d_break_rot" + sfx,
                    "failObjectiveId": fail_id, "failDescription": "You are defeated.",
                    "drawDescription": "The fight stalls and the moment is lost.",
                    "fleeDescription": "You break away, and the way back closes behind you."})
        new.append({"id": "d_break_rot" + sfx, "task": "dialog", "description": t["d_break_rot"],
                    "sceneBackground": scene, "sceneCharacters": [],
                    "reward_items": [{"ids": [core_rot], "number": 100, "quantity": CORE_ROT_QTY}],
                    "nextObjectiveId": [{"text": t["d_break_rot.choice"], "nextObjectiveId": cont}]})
    i = objs.index(fail[0])
    objs[i:i] = new  # keep the fail ending last
    return gaps


def _demo():
    s = importlib.util.spec_from_file_location("skyglass_hunts", os.path.join(ROOT, "push/skyglass_hunts.gen.py"))
    G = importlib.util.module_from_spec(s); s.loader.exec_module(G)
    objs = G.archive()
    gaps = break_the_seal(objs, echo_ai="STANDINxxxxxxxxxxxxxx", core_rot="KuqLeFB12BdB-0s5O1udk")
    for o in objs:
        nxt = o.get("nextObjectiveId")
        nxt = [c["nextObjectiveId"] for c in nxt] if isinstance(nxt, list) else nxt
        print(f"{o['id']:<16} {o['task']:<13} -> {nxt}")
    print("gaps:", *gaps, sep="\n  ")


if __name__ == "__main__":
    if sys.argv[1:] == ["--demo"]:
        _demo()
    else:
        raise SystemExit(__doc__)
