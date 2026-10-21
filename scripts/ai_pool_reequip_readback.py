#!/usr/bin/env python3
"""Check the read-backs of the AI pool battle-line pass (push/162-177) against the before-image.

Before-image: push/157 (82 jutsu) and push/158-161 (AIs), the inputs of push/162_ai_pool_reequip.gen.py.
The step is read from each results bundle's own manifest path:

  unequip  (162-169)  kit = before-image minus the EQUIPPED pool rows; every other kit row unchanged
  edit     (170)      each jutsu differs from the before-image only in the fields 170 sent, with the
                      values it sent
  re-equip (171-177)  kit = before-image, row for row (jutsuId, level, experience, equipped)

For AIs it also compares every other column and the items (itemId, quantity, dropChancePerc), using
the same rules as scripts/bloodright_classification_readback.py: volatile columns are skipped,
masteries may round by at most 0.005 on a save (scaleUserStats), and effect keys the pinned
validators no longer define are ignored.

  python3 scripts/ai_pool_reequip_readback.py harvests/inbox/tnr_results_<after>.json [...]

Exit 1 when anything differs from what the step should leave behind.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from bloodright_classification_readback import VOLATILE, items, pinned  # noqa: E402

JUTSU_BEFORE = "harvests/inbox/tnr_results_1792551342555.json"
AI_BEFORE = ["harvests/inbox/tnr_results_1792551456483.json", "harvests/inbox/tnr_results_1792551557783.json",
             "harvests/inbox/tnr_results_1792551619150.json", "harvests/inbox/tnr_results_1792551674258.json"]
EDIT_MANIFEST = "push/170_ai_pool_battle_lines_edit.json"
MASTERIES = {"ninjutsuMastery", "genjutsuMastery", "taijutsuMastery", "bukijutsuMastery", "bloodlineMastery", "sageMastery"}
MASTERY_ROUNDING = 0.005 + 1e-9


def effects_key(effects):
    """Effects on the keys allowed at the pin, with the server's own statTypes normalisation applied.

    The schema rewrites statTypes "Highest" to "None" on every save (validators/combat.ts IncludeStats,
    studie-tech/TheNinjaRPG@dcf1cea), and realizeTag (libs/combat/tags.ts:105-110) maps a stored
    "Highest" to "None" before any effect, passive ones included, enters a battle. So the two are the
    same in combat, and a save that turns one into the other is not a difference.
    """
    out = []
    for e in pinned(effects)[0]:
        e = dict(e)
        if isinstance(e.get("statTypes"), list):
            e["statTypes"] = ["None" if t == "Highest" else t for t in e["statTypes"]]
        if e.get("statTypes") is None:
            e.pop("statTypes", None)
        if e.get("generalTypes") in (None, []):
            e.pop("generalTypes", None)
        out.append(e)
    return out


def bodies(paths, proc, key):
    out = {}
    for f in paths:
        for c in json.loads((ROOT / f).read_text() if not Path(f).is_absolute() else Path(f).read_text())["captures"]:
            if c.get("proc") == proc and c.get("ok") and c.get("persistOk") and isinstance(c.get("data"), dict):
                out[c["data"][key]] = c["data"]
    return out


def kit(a):
    return {r["jutsuId"]: (r.get("level"), r.get("experience"), r.get("equipped")) for r in a.get("jutsus") or []}


def compare_columns(before, after):
    problems = []
    for k in sorted(set(before) | set(after)):
        if k in VOLATILE or k in ("jutsus", "items"):
            continue
        b, a = before.get(k), after.get(k)
        if k == "effects":
            if effects_key(b) != effects_key(a):
                problems.append(f"effects differ: {json.dumps(effects_key(b))[:100]} -> {json.dumps(effects_key(a))[:100]}")
            continue
        if k in MASTERIES and isinstance(a, (int, float)) and isinstance(b, (int, float)) and abs(a - b) <= MASTERY_ROUNDING:
            continue
        if b != a:
            problems.append(f"{k}: {json.dumps(b)[:80]} -> {json.dumps(a)[:80]}")
    return problems


def check_ai(step, before, after, pool_ids):
    problems = compare_columns(before, after)
    kb, ka = kit(before), kit(after)
    if step == "unequip":
        expect = {j: v for j, v in kb.items() if not (j in pool_ids and v[2] is True)}
    else:
        expect = kb
    for j in sorted(set(expect) | set(ka)):
        if expect.get(j) != ka.get(j):
            problems.append(f"jutsu {j}: expected {expect.get(j)}, read {ka.get(j)}")
    if items(before) != items(after):
        problems.append(f"items: {items(before)} -> {items(after)}")
    return problems


def check_jutsu(before, after, sent):
    problems = []
    for k in sorted(set(before) | set(after)):
        if k in ("updatedAt",):
            continue
        if k == "effects" and k in sent:
            # The server drops effect keys its validators no longer define, so compare on the pinned keys.
            if effects_key(after.get(k)) != effects_key(sent[k]):
                problems.append(f"effects: sent {json.dumps(effects_key(sent[k]))[:100]}, read {json.dumps(effects_key(after.get(k)))[:100]}")
        elif k in sent:
            if after.get(k) != sent[k]:
                problems.append(f"{k}: sent {json.dumps(sent[k])[:80]}, read {json.dumps(after.get(k))[:80]}")
        elif k == "effects":
            if effects_key(before.get(k)) != effects_key(after.get(k)):
                problems.append(f"effects changed although 170 does not send them: {json.dumps(effects_key(before.get(k)))[:100]} -> {json.dumps(effects_key(after.get(k)))[:100]}")
        elif before.get(k) != after.get(k):
            problems.append(f"{k} changed although 170 does not send it: {json.dumps(before.get(k))[:60]} -> {json.dumps(after.get(k))[:60]}")
    return problems


def step_of(bundle):
    path = (bundle.get("journal") or {}).get("manifestPath") or ""
    if "_ai_pool_unequip" in path:
        return "unequip", path
    if "_ai_pool_reequip_" in path:
        return "reequip", path
    if "_ai_pool_battle_lines_edit" in path:
        return "edit", path
    return None, path


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    pool_ids = {r["id"] for r in json.loads((ROOT / "32b_DATA_pool.json").read_text())["records"].values()}
    ai_before = bodies(AI_BEFORE, "profile.getAi", "userId")
    jutsu_before = bodies([JUTSU_BEFORE], "jutsu.get", "id")
    sent = {it["targetId"]: it["data"] for it in json.loads((ROOT / EDIT_MANIFEST).read_text())["items"]}
    bad = total = 0
    for f in argv:
        bundle = json.loads(Path(f).read_text())
        step, path = step_of(bundle)
        print(f"== {Path(f).name}: {path or '?'} -> step {step}, state {bundle.get('state')}, outcome {bundle.get('outcome')}")
        if step is None:
            print("   not a push/162-177 bundle")
            bad += 1
            continue
        # Forge's own verify compares raw values, so it reports the Highest -> None save rewrite as drift.
        # The read-back below is the authority; an entry only fails here if it did not save.
        failed = [it for it in bundle.get("entries") or [] if it.get("state") != "ok"]
        for it in bundle.get("entries") or []:
            if it.get("state") == "ok" and it.get("verdict") not in (None, "match"):
                print(f"   note {it.get('name')}: Forge verdict {it.get('verdict')} (checked against the read-back below)")
        for it in failed:
            print(f"   ENTRY {it.get('name')}: state {it.get('state')}, verdict {it.get('verdict')}")
        bad += len(failed)
        caps = [c for c in bundle.get("captures") or [] if c.get("phase") == "after"]
        if not caps or any(not (c.get("ok") and c.get("persistOk")) for c in caps):
            print(f"   read-back incomplete: {sum(1 for c in caps if c.get('ok') and c.get('persistOk'))}/{len(caps)} reads persisted")
            bad += 1
        for c in caps:
            a = c.get("data")
            if not isinstance(a, dict):
                continue
            total += 1
            if step == "edit":
                j = a["id"]
                problems = check_jutsu(jutsu_before[j], a, sent[j]) if j in jutsu_before and j in sent else ["no before-image or not in 170"]
                label = f"{a.get('name')} ({j})"
            else:
                u = a["userId"]
                problems = check_ai(step, ai_before[u], a, pool_ids) if u in ai_before else ["no before-image"]
                label = f"{a.get('username')} ({u})"
            print(f"   {'ok  ' if not problems else 'DIFF'} {label}")
            for p in problems:
                print("        " + p)
            bad += bool(problems)
    print(f"{total} record(s) read back, {bad} problem(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
