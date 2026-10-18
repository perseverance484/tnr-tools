#!/usr/bin/env python3
"""Generate the Bloodright kit-classification edit manifests (RUL-2026-10-18-003). Do not hand-edit outputs.

Inputs (all committed):
  - docs/design/bloodright/balance/kits_from_reference_captures.json  (kit jutsu per tree)
  - harvests/inbox/tnr_results_1792352813119.json, tnr_results_1792352829484.json
    (push/109-110: fresh profile.getAi before-image of the 46 AIs that equip a kit jutsu)

Each AI-linked manifest is one self-contained group of AIs and the kit jutsu they equip, run in
strict phases (laws 18, 60):
  phase 1  unequip: each AI's kit minus the affected jutsu (nothing else sent; Forge re-sends items)
  phase 2  edit:    each affected jutsu, elementClassification "None" -> tree element (only field)
  phase 3  re-equip: each AI's exact original kit, original order
Manifests:
  111  probe: the smallest group (1 AI, 1 jutsu). Run first; check the AI's stats are unchanged.
  then the remaining AI-linked groups, packed into batches of at most 41 entries,
  then the 84 kit jutsu no AI equips, phase-2 edits only, 28 per batch.

  python3 push/111_bloodright_classification.gen.py [--check]
"""
import collections
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KITS = ROOT / "docs/design/bloodright/balance/kits_from_reference_captures.json"
BEFORE = ["harvests/inbox/tnr_results_1792352813119.json", "harvests/inbox/tnr_results_1792352829484.json"]
FIRST = 111
CONVERT_BATCH = 28
LINKED_MAX = 41


def load():
    kits = json.loads(KITS.read_text())
    target = {}
    for slug, k in kits.items():
        if len(k["elements"]) != 1 or k["elements"][0] == "None":
            continue  # Cosmic Ascendant / Shiroi Youso keep None (RUL-2026-10-18-004)
        for j in k["jutsu"]:
            if j.get("elementClassification") not in (None, "None"):
                raise SystemExit(f"{j['name']} already classified {j['elementClassification']}")
            if not isinstance(j.get("injectableInBattle"), bool):
                raise SystemExit(f"{j['name']}: captured injectableInBattle missing")
            target[j["id"]] = {"slug": slug, "element": k["elements"][0], "name": j["name"],
                               "injectable": j["injectableInBattle"]}
    ais = {}
    for f in BEFORE:
        for c in json.loads((ROOT / f).read_text())["captures"]:
            if c.get("proc") == "profile.getAi" and c.get("ok") and c.get("persistOk"):
                a = c["data"]
                ais[a["userId"]] = {"name": a["username"].strip(), "kit": [r["jutsuId"] for r in a["jutsus"]]}
    return target, ais


def groups(target, ais):
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    for u, a in ais.items():
        for j in a["kit"]:
            if j in target:
                parent[find("A" + u)] = find("J" + j)
    comp = collections.defaultdict(set)
    for n in list(parent):
        comp[find(n)].add(n)
    out = []
    for nodes in comp.values():
        us = sorted((n[1:] for n in nodes if n[0] == "A"), key=lambda u: (ais[u]["name"].lower(), u))
        js = sorted((n[1:] for n in nodes if n[0] == "J"), key=lambda j: (target[j]["name"].lower(), j))
        out.append((us, js))
    return sorted(out, key=lambda g: (len(g[0]) + len(g[1]), g[0]))


def edit_entry(j, target):
    t = target[j]
    return {"entity": "jutsu", "slot": "edit", "phase": 2, "targetId": j,
            "name": f"{t['name']}: elementClassification None -> {t['element']}",
            # injectableInBattle re-sent at its captured value (law 20: omitted means false).
            "data": {"elementClassification": t["element"], "injectableInBattle": t["injectable"]}}


def ai_entries(us, js, ais):
    js = set(js)
    un, re = [], []
    for u in us:
        kit = ais[u]["kit"]
        un.append({"entity": "ai", "slot": "edit", "phase": 1, "targetId": u,
                   "name": f"{ais[u]['name']}: unequip Bloodright kit jutsu before classification edit (law 60)",
                   "data": {"jutsus": [j for j in kit if j not in js]}})
        re.append({"entity": "ai", "slot": "edit", "phase": 3, "targetId": u,
                   "name": f"{ais[u]['name']}: re-equip original kit after classification edit",
                   "data": {"jutsus": list(kit)}})
    return un, re


def build():
    target, ais = load()
    gs = groups(target, ais)
    linked = {j for _, js in gs for j in js}
    probe, rest = gs[0], gs[1:]
    cost = lambda g: 2 * len(g[0]) + len(g[1])  # unequip + re-equip per AI, one edit per jutsu
    bins = []
    for g in sorted(rest, key=cost, reverse=True):  # first-fit decreasing, <= LINKED_MAX entries
        for b in bins:
            if sum(map(cost, b)) + cost(g) <= LINKED_MAX:
                b.append(g)
                break
        else:
            bins.append([g])
    manifests = []

    def linked_manifest(gl, label, readback=True):
        un, ed, re = [], [], []
        for us, js in gl:
            a, b = ai_entries(us, js, ais)
            un += a
            re += b
            ed += [edit_entry(j, target) for j in js]
        n_ai = sum(len(us) for us, _ in gl)
        n_j = sum(len(js) for _, js in gl)
        note = (f"Bloodright kit-classification edit, {label}: {n_ai} AI(s) and the {n_j} kit jutsu they equip "
                "(RUL-2026-10-18-003). Phases: 1 unequip the affected jutsu, 2 set elementClassification "
                "(the only field), 3 re-equip each AI's exact original kit (laws 18, 60). Before-image: push/109-110 "
                "results. Generated by push/111_bloodright_classification.gen.py; do not hand-edit. Operator-run only.")
        m = {"_note": note, "items": un + ed + re}
        if readback:
            # Full read-back of every AI after phase 3, compared offline against the push/109-110
            # before-image (stats, pools, kit order). Forge's own verify covers only asserted keys.
            m["capture"] = {"before": [], "after": [{"proc": "profile.getAi", "input": {"id": u}, "persist": "full"}
                                                  for us, _ in gl for u in us]}
        return m
    # 111 was run before read-back was added (2026-10-18); it is left byte-identical, and its
    # read-back is the separate read-only manifest below.
    manifests.append(("probe", linked_manifest([probe], "PROBE - run first, then return the results before running the rest", readback=False)))
    for n, b in enumerate(bins, 1):
        manifests.append((f"ai_linked_{n}", linked_manifest(b, f"AI-linked batch {n} of {len(bins)}")))
    free = sorted((j for j in target if j not in linked), key=lambda j: (target[j]["slug"], target[j]["name"].lower(), j))
    batches = [free[i:i + CONVERT_BATCH] for i in range(0, len(free), CONVERT_BATCH)]
    for n, b in enumerate(batches, 1):
        manifests.append((f"unequipped_{n}", {"_note": (f"Bloodright kit-classification edit, unequipped kit jutsu batch {n} of {len(batches)}: "
                                    f"{len(b)} jutsu no AI equips (per push/109-110 and the 2026-10-12 census); "
                                    "elementClassification is the only field (RUL-2026-10-18-003). Generated by "
                                    "push/111_bloodright_classification.gen.py; do not hand-edit. Operator-run only."),
                          "items": [edit_entry(j, target) for j in b]}))
    out = {}
    for i, (label, m) in enumerate(manifests):
        out[f"push/{FIRST + i}_bloodright_classification_{label}.json"] = m
    out[f"push/{FIRST + len(manifests)}_bloodright_classification_probe_readback.json"] = {
        "_note": ("READ-ONLY read-back of the push/111 probe AI after its unequip -> edit -> re-equip, compared offline "
                  "against the push/109-110 before-image. Zero items, zero mutations. Generated by "
                  "push/111_bloodright_classification.gen.py; do not hand-edit. Operator-run only."),
        "capture": {"before": [{"proc": "profile.getAi", "input": {"id": u}, "persist": "full"} for u in probe[0]],
                    "after": []},
        "items": []}
    assert sum(1 for m in out.values() for it in m["items"] if it["entity"] == "jutsu") == len(target)
    return out


def main():
    stale = []
    for path, m in build().items():
        text = json.dumps(m, indent=1, ensure_ascii=False) + "\n"
        p = ROOT / path
        if "--check" in sys.argv:
            if not p.is_file() or p.read_text() != text:
                stale.append(path)
        else:
            p.write_text(text)
        kinds = collections.Counter((it["entity"], it["phase"]) for it in m["items"])
        reads = sum(len(v) for v in (m.get("capture") or {}).values())
        print(path, len(m["items"]), dict(kinds), "reads", reads)
    if stale:
        print("stale:", *stale)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
