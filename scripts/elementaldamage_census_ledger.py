#!/usr/bin/env python3
"""Affected-candidate ledger from a Forge `item.weapon.elementaldamage` census results bundle.

Brief: docs/handoffs/ELEMENTALDAMAGE_WEAPON_CENSUS_CAPTURE_IMPLEMENTATION_20261020.md section 5.
Operator guide: docs/workflows/ELEMENTALDAMAGE_WEAPON_CENSUS.md.

    python3 scripts/elementaldamage_census_ledger.py harvests/inbox/tnr_results_<n>.json
    python3 scripts/elementaldamage_census_ledger.py <bundle> --out-dir reports/elementaldamage_census

Reads ONE committed bundle and nothing else: no network, no game, no seed catalog. Writes a
deterministic item-ID-keyed JSON ledger and a readable Markdown summary next to each other.

It does not trust the bundle's own verdict. It re-derives the inventory counts, the target set
(exact parsed `type == "elementaldamage"` on WEAPON rows) and every per-point acceptance from the
exported rows and bodies, and reports any disagreement as a ledger error.

Exit status: 0 only when the census is COMPLETE and every independent check passes; 1 when the
ledger was written but the census is not complete (the ledger then says so on its first line);
2 when the bundle cannot be read as a census at all.

Classification is OBSERVED EVIDENCE, never a repair decision. A missing selector is a candidate
for the director's review, not proof of unintended design, and nothing here approves a repair.

Engine facts the classifier relies on (studie-tech/TheNinjaRPG@6524d0fbd7c0b80ecfd28ca63e9c4becdfb210eb; re-checked at
85cecae, the contract pin since PR #76: combat.ts and elementalDamage.ts unchanged, tags.ts changed only in
Clear/Cleanse, which moves the damageCalc lines below by +4):
  - validators/combat.ts:156-169   statTypes accepts "Highest" and stores it as "None"; any
                                   NONEMPTY statTypes (["None"] included) is stat-scaling-positive.
  - libs/combat/tags.ts:1438-1447  damageCalc adds the offence/defence term only when
                                   statTypes is nonempty, and only for calculation "formula".
  - generalTypes ["Highest"] contributes the user's highest generals dynamically.
  - validators/combat.ts:559-562   ElementalDamageTag = DamageTag minus `elements`; the element
                                   is resolved at runtime (libs/combat/elementalDamage.ts):
                                   preferredDamageElement, else a basic primary element, else Fire.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

KIND = "item.weapon.elementaldamage"
TAG = "elementaldamage"
STORMRENDER_ID = "cLXXf8RJv5l9B_gGsYN2a"
STORMRENDER_NOTE = "ALREADY STAGED: push/131_stormrender_highest_scaling_suggestion.json (integrated by PR #76, which superseded PR #73); do not submit a duplicate repair"
GAME_PIN = "studie-tech/TheNinjaRPG@6524d0fbd7c0b80ecfd28ca63e9c4becdfb210eb"
PROJECTION_KEYS = {"id", "name", "itemType", "hidden", "updatedAt", "effectTypes", "effectsMalformed"}

C_MISS_STATS = "formula / missing statTypes"
C_MISS_GENS = "formula / missing generalTypes"
C_MISS_BOTH = "formula / both missing"
C_BOTH = "formula / both present"
C_NONFORMULA = "non-formula / scaling not applicable"
C_MALFORMED = "malformed or ambiguous"
C_STORMRENDER = "already-staged Stormrender"
CANDIDATE_CLASSES = (C_MISS_STATS, C_MISS_GENS, C_MISS_BOTH)
ALL_CLASSES = (C_MISS_STATS, C_MISS_GENS, C_MISS_BOTH, C_BOTH, C_NONFORMULA, C_MALFORMED, C_STORMRENDER)


class NotACensus(Exception):
    pass


def canon(v) -> str:
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def effect_type(e):
    """A member's type when it is an object with a non-empty string `type`, else None (as Forge's
    census.mjs effectType). A member without one cannot be ruled out as the tag."""
    return e["type"] if isinstance(e, dict) and isinstance(e.get("type"), str) and e["type"] else None


def row_malformed(row: dict) -> bool:
    """Recomputed from the projection itself: effects not an array, or any member untyped."""
    types = row.get("effectTypes")
    return not isinstance(types, list) or any(not isinstance(t, str) or not t for t in types)


def selector(effect: dict, key: str):
    """'present' (nonempty list), 'missing' (absent, null or []), or 'malformed' (anything else)."""
    if key not in effect or effect[key] is None:
        return "missing"
    v = effect[key]
    if not isinstance(v, list) or not all(isinstance(x, str) for x in v):
        return "malformed"
    return "present" if v else "missing"


def classify(effect) -> tuple[str, list[str]]:
    """One elementaldamage effect -> (classification, notes)."""
    if not isinstance(effect, dict):
        return C_MALFORMED, ["effect is not an object"]
    notes = []
    calc = effect.get("calculation")
    if "elements" in effect:
        notes.append("carries an `elements` key, which ElementalDamageTag omits; the element is chosen at runtime regardless")
    if not isinstance(calc, str):
        return C_MALFORMED, notes + ["calculation is absent or not a string (the schema prefault is formula; the stored value does not say)"]
    st, gt = selector(effect, "statTypes"), selector(effect, "generalTypes")
    if calc != "formula":
        return C_NONFORMULA, notes + [f"calculation {calc}: stat/general scaling does not apply to this defect"]
    if "malformed" in (st, gt):
        return C_MALFORMED, notes + [f"statTypes {st}, generalTypes {gt}"]
    if st == "present" and effect["statTypes"] == ["None"]:
        notes.append('statTypes ["None"] is nonempty: stat-scaling POSITIVE (legacy "Highest" is stored as "None")')
    if gt == "present" and "Highest" in effect["generalTypes"]:
        notes.append('generalTypes includes "Highest": the user\'s highest generals contribute dynamically')
    if st == "present" and gt == "present":
        return C_BOTH, notes
    if st == "missing" and gt == "missing":
        return C_MISS_BOTH, notes
    return (C_MISS_STATS if st == "missing" else C_MISS_GENS), notes


def effect_record(pos: int, effect) -> dict:
    cls, notes = classify(effect)
    e = effect if isinstance(effect, dict) else {}
    return {
        "position": pos,
        "classification": cls,
        "calculation": e.get("calculation"),
        "power": e.get("power"),
        "powerPerLevel": e.get("powerPerLevel"),
        "statTypes": e.get("statTypes", "<absent>"),
        "generalTypes": e.get("generalTypes", "<absent>"),
        "allowBloodlineDamageIncrease": e.get("allowBloodlineDamageIncrease", "<absent>"),
        "allowBloodlineDamageDecrease": e.get("allowBloodlineDamageDecrease", "<absent>"),
        "elementSelection": "runtime: preferredDamageElement -> basic primary element -> Fire (ElementalDamageTag has no elements field)",
        "notes": notes,
        "effectSha256": sha256(canon(effect)),
        "original": effect,
    }


def context_record(pos: int, effect) -> dict:
    e = effect if isinstance(effect, dict) else {}
    out = {"position": pos, "type": e.get("type"), "calculation": e.get("calculation"), "power": e.get("power")}
    if e.get("type") == "damage":  # ordinary damage: a contextual control, never an automatic candidate
        out["statTypes"] = selector(e, "statTypes")
        out["generalTypes"] = selector(e, "generalTypes")
    return out


def build_ledger(bundle: dict, *, bundle_path: str, bundle_sha256: str) -> dict:
    census = bundle.get("census")
    if not isinstance(census, dict) or census.get("kind") != KIND:
        raise NotACensus(f"bundle has no census block of kind {KIND}")
    errors: list[str] = []
    journal = bundle.get("journal") or {}
    rows = census.get("rows")
    if not isinstance(rows, list):
        raise NotACensus("census.rows (the inventory projection) is missing; " + str(census.get("inventoryError") or "no reason recorded"))

    # ---- independent re-derivation of Stage A
    for r in rows:
        extra = set(r) - PROJECTION_KEYS
        if extra:
            errors.append(f"inventory row {r.get('id')} carries non-projection fields {sorted(extra)}")
        if r.get("itemType") != "WEAPON":
            errors.append(f"inventory row {r.get('id')} is {r.get('itemType')}, not WEAPON")
    ids = [r.get("id") for r in rows]
    if len(set(ids)) != len(ids):
        errors.append("inventory repeats an id")
    counts = {"hidden:false": sum(1 for r in rows if r.get("hidden") is False),
              "hidden:true": sum(1 for r in rows if r.get("hidden") is True)}
    counts["total"] = len(rows)
    for k, v in counts.items():
        if (census.get("counts") or {}).get(k) != v:
            errors.append(f"census.counts[{k}] = {(census.get('counts') or {}).get(k)} but the rows give {v}")
    if counts["hidden:false"] + counts["hidden:true"] != counts["total"]:
        errors.append("a row has a non-boolean hidden")
    for r in rows:
        if bool(r.get("effectsMalformed")) != row_malformed(r):
            errors.append(f"inventory row {r.get('id')}: effectsMalformed={r.get('effectsMalformed')} but its effectTypes say {row_malformed(r)}")
    # The target set, each target's reason and its updatedAt are recomputed from the rows, not
    # taken from Forge (census review F2): a malformed row is a target too (review F1).
    expected = {r["id"]: ("effectsMalformed" if row_malformed(r) else TAG) for r in rows
                if row_malformed(r) or TAG in (r.get("effectTypes") or [])}
    targets = census.get("targets") or []
    tids = [t.get("id") for t in targets]
    if len(set(tids)) != len(tids):
        errors.append("census.targets repeats an id")
    if sorted(set(tids)) != sorted(expected):
        errors.append("census.targets is not exactly the tagged + malformed inventory rows")
    inv_rows = {r.get("id"): r for r in rows}
    for t in targets:
        r = inv_rows.get(t.get("id"))
        if r is None:
            continue
        if t.get("reason") != expected.get(t.get("id")):
            errors.append(f"target {t.get('id')}: reason {t.get('reason')!r} but its inventory row gives {expected.get(t.get('id'))!r}")
        if t.get("updatedAt") != r.get("updatedAt"):
            errors.append(f"target {t.get('id')}: updatedAt {t.get('updatedAt')} but its inventory row has {r.get('updatedAt')}")
    scans = census.get("scans") or []
    if census.get("inventory") == "COMPLETE" and (len(scans) != 2 or scans[0].get("digest") != scans[1].get("digest")):
        errors.append("inventory claims COMPLETE without two agreeing scans")
    for s in scans:
        parts = {p.get("hidden") for p in s.get("pages") or []}
        if census.get("inventory") == "COMPLETE" and parts != {False, True}:
            errors.append("a scan did not page both hidden partitions")
        for hidden in (False, True):
            ps = [p for p in s.get("pages") or [] if p.get("hidden") is hidden]
            if ps and ps[-1].get("nextCursor") is not None:
                errors.append(f"scan of hidden:{hidden} did not end on nextCursor:null")
            if [p.get("cursor") for p in ps] != list(range(len(ps))):
                errors.append(f"scan of hidden:{hidden} cursors are not 0..n in order")

    # ---- Stage B, per point
    points = {}
    for c in bundle.get("captures") or []:
        if c.get("phase") != "census":
            continue
        pid = (c.get("input") or {}).get("id")
        if pid in points:
            errors.append(f"two census captures for {pid}")
        points[pid] = c
    for pid in sorted(set(points) - set(tids), key=str):
        errors.append(f"census capture for {pid}, which is not a census target")
    inv = {r["id"]: r for r in rows}
    stale, missing, failed = [], [], []
    records = {}
    for t in sorted(targets, key=lambda t: t["id"]):
        tid = t["id"]
        c = points.get(tid)
        row = inv.get(tid, {})
        reason = expected.get(tid, t.get("reason"))   # the ledger's own reason, not Forge's
        rec = {
            "id": tid, "name": row.get("name"), "hidden": row.get("hidden"),
            "inventoryUpdatedAt": row.get("updatedAt", t.get("updatedAt")), "targetReason": reason,
        }
        problems = []
        data = c.get("data") if c else None
        if c is None:
            problems.append("no census point capture in the bundle")
            missing.append(tid)
        else:
            if c.get("ok") is not True or c.get("rows") != 1:
                problems.append(f"read not ok (ok {c.get('ok')}, rows {c.get('rows')}, error {c.get('error')})")
            if c.get("persist") != "full" or c.get("persistOk") is not True or not isinstance(data, dict):
                problems.append(f"full body not persisted: {c.get('persistError')}")
            if isinstance(data, dict):
                if data.get("id") != tid:
                    problems.append(f"body id {data.get('id')}")
                if data.get("itemType") != "WEAPON":
                    problems.append(f"body itemType {data.get('itemType')}")
                fx = data.get("effects")
                if reason != "effectsMalformed":
                    # same acceptance as Forge acceptPoint: an array with the exact tag
                    if not isinstance(fx, list):
                        problems.append("body effects is not an array")
                    elif not any(effect_type(e) == TAG for e in fx):
                        problems.append(f"no {TAG} effect in the captured body")
                is_stale = data.get("updatedAt") != row.get("updatedAt", t.get("updatedAt"))
                if is_stale:
                    problems.append(f"STALE: captured updatedAt {data.get('updatedAt')} != inventoried {row.get('updatedAt', t.get('updatedAt'))}; RECAPTURE REQUIRED")
                    stale.append(tid)
                elif row:
                    # Same record, same updatedAt: item.getAll and item.get both return the stored
                    # row, so the body's effect types must be exactly the projected ones. A
                    # disagreement means the bundle is inconsistent (corrupted or edited).
                    body_types = [effect_type(e) for e in fx] if isinstance(fx, list) else None
                    if body_types != row.get("effectTypes"):
                        errors.append(f"{tid}: body effect types {body_types} != inventory projection {row.get('effectTypes')} at the same updatedAt")
            if bool(c.get("accepted")) != (not problems):
                errors.append(f"{tid}: bundle says accepted={c.get('accepted')} but the ledger's own check {'found ' + '; '.join(problems) if problems else 'passes'}")
            rec["provenance"] = {
                "bundle": bundle_path, "bundleSha256": bundle_sha256, "bundleAt": bundle.get("at"),
                "builder": bundle.get("builder"), "jobId": journal.get("jobId"),
                "manifestPath": journal.get("manifestPath"), "manifestHash": journal.get("manifestHash"),
                "snapshotKey": c.get("snapshotKey"), "capturedAt": c.get("at"), "bodyBytes": c.get("bytes"),
                "bodySha256": sha256(canon(data)) if isinstance(data, dict) else None,
            }
        if problems and tid not in stale and tid not in missing:
            failed.append(tid)
        rec["captureProblems"] = problems
        effects = data.get("effects") if isinstance(data, dict) and isinstance(data.get("effects"), list) else []
        if isinstance(data, dict):
            rec["rarity"] = data.get("rarity")
            rec["capturedUpdatedAt"] = data.get("updatedAt")
            rec["hidden"] = data.get("hidden", rec["hidden"])
            rec["name"] = data.get("name", rec["name"])
        dyn = [effect_record(i, e) for i, e in enumerate(effects) if isinstance(e, dict) and e.get("type") == TAG]
        dyn += [effect_record(i, e) for i, e in enumerate(effects) if not isinstance(e, dict)]
        dyn.sort(key=lambda d: d["position"])
        rec["elementaldamageEffects"] = dyn
        rec["otherEffects"] = [context_record(i, e) for i, e in enumerate(effects) if isinstance(e, dict) and e.get("type") != TAG]
        classes = sorted({d["classification"] for d in dyn}, key=ALL_CLASSES.index)
        if tid == STORMRENDER_ID:
            classes.append(C_STORMRENDER)
        rec["classifications"] = classes
        if problems:
            rec["status"] = "RECAPTURE REQUIRED" if tid in stale else "NOT CAPTURED / FAILED"
        elif tid == STORMRENDER_ID:
            rec["status"] = STORMRENDER_NOTE
        elif any(c in CANDIDATE_CLASSES for c in classes):
            rec["status"] = "CANDIDATE: director review (observed evidence only; no repair proposed or approved)"
        elif reason == "effectsMalformed" or C_MALFORMED in classes or not dyn:
            rec["status"] = "MANUAL REVIEW: malformed or ambiguous"
        else:
            rec["status"] = "CONTROL: no formula-scaling gap observed"
        records[tid] = rec

    # ---- zero-mutation evidence, from the bundle itself
    items = journal.get("items")
    procs = sorted({c.get("proc") for c in bundle.get("captures") or []})
    zero = {
        "journalItems": len(items) if isinstance(items, list) else None,
        "harvestEntries": len(bundle.get("entries") or []),
        "captureProcedures": procs,
        "ok": items == [] and not bundle.get("entries") and set(procs) <= {"item.get"},
    }
    if not zero["ok"]:
        errors.append("the bundle is not a pure read: it carries items, entries, or a non item.get capture")

    verdict = census.get("verdict")
    ambiguous = sorted(tid for tid, why in expected.items() if why == "effectsMalformed")
    # The ledger's own verdict. A malformed target can never be COMPLETE (Forge reports AMBIGUOUS):
    # it was captured, but nobody has resolved whether it is the tag (census review F1).
    own = ("INCOMPLETE" if missing else "STALE" if stale else "FAILED" if failed
           else "AMBIGUOUS" if ambiguous else "COMPLETE")
    if census.get("inventory") == "COMPLETE" and verdict != own:
        errors.append(f"bundle census verdict {verdict} but the ledger derives {own}")
    complete = own == "COMPLETE" and verdict == "COMPLETE" and not errors
    by_class = {k: sorted(tid for tid, r in records.items() if k in r["classifications"]) for k in ALL_CLASSES}
    effect_counts = {k: sum(1 for r in records.values() for d in r["elementaldamageEffects"] if d["classification"] == k) for k in ALL_CLASSES}
    return {
        "ledger": "elementaldamage WEAPON census",
        "status": "COMPLETE" if complete else f"NOT COMPLETE (census verdict {verdict}, ledger verdict {own}; {len(errors)} ledger error(s), {len(stale)} stale, {len(missing)} missing, {len(failed)} failed, {len(ambiguous)} ambiguous)",
        "reviewGate": "STOP: observed evidence only. Every candidate needs an ID-level director decision before any suggest/edit manifest is prepared; Stormrender is already staged (push/131, integrated by PR #76).",
        "gamePin": GAME_PIN,
        "source": {
            "bundle": bundle_path, "bundleSha256": bundle_sha256, "bundleAt": bundle.get("at"), "builder": bundle.get("builder"),
            "jobId": journal.get("jobId"), "manifestPath": journal.get("manifestPath"), "manifestHash": journal.get("manifestHash"),
            "censusVerdict": verdict, "inventory": census.get("inventory"), "inventoryDigest": census.get("digest"),
            "inventorySha256": sha256(canon(rows)), "pageLimit": census.get("pageLimit"), "inventoriedAt": census.get("at"),
        },
        "counts": {
            "inventory": counts,
            "dynamicWeapons": len(targets),
            "captured": sum(1 for r in records.values() if not r["captureProblems"]),
            "recordsByClassification": {k: len(v) for k, v in by_class.items()},
            "effectsByClassification": effect_counts,
        },
        "candidates": sorted(tid for tid, r in records.items() if r["status"].startswith("CANDIDATE")),
        "controls": sorted(tid for tid, r in records.items() if r["status"].startswith("CONTROL")),
        "manualReview": sorted(tid for tid, r in records.items() if r["status"].startswith("MANUAL")),
        "alreadyStaged": sorted(tid for tid, r in records.items() if C_STORMRENDER in r["classifications"]),
        "byClassification": by_class,
        "stale": sorted(stale), "missing": sorted(missing), "failed": sorted(failed), "ambiguous": ambiguous,
        "ledgerVerdict": own,
        "crossCheck": census.get("crossCheck"),
        "censusProblems": census.get("problems") or [],
        "ledgerErrors": errors,
        "zeroMutation": zero,
        "records": records,
    }


def render_md(L: dict) -> str:
    s, c = L["source"], L["counts"]
    out = [
        "# elementaldamage WEAPON census ledger", "",
        f"**Status:** {L['status']}", "",
        f"**Review gate:** {L['reviewGate']}", "",
        f"- Bundle: `{s['bundle']}` (sha256 `{s['bundleSha256']}`), exported {s['bundleAt']} by {s['builder']}",
        f"- Job `{s['jobId']}` from `{s['manifestPath']}` (hash {s['manifestHash']}); census verdict **{s['censusVerdict']}**",
        f"- Inventory: {c['inventory']['total']} WEAPON records ({c['inventory']['hidden:false']} visible, {c['inventory']['hidden:true']} hidden), page size {s['pageLimit']}, digest {s['inventoryDigest']}, sha256 `{s['inventorySha256']}`",
        f"- Dynamic-element weapons: {c['dynamicWeapons']}; full bodies captured and accepted: {c['captured']}",
        f"- Zero-mutation evidence: journal items {L['zeroMutation']['journalItems']}, entries {L['zeroMutation']['harvestEntries']}, procedures {', '.join(L['zeroMutation']['captureProcedures']) or 'none'} -> {'OK' if L['zeroMutation']['ok'] else 'NOT A PURE READ'}",
        f"- Game source pin for the classification rules: `{L['gamePin']}`", "",
        "## Counts by classification", "", "| Classification | Records | Effects |", "| --- | ---: | ---: |",
    ]
    for k in ALL_CLASSES:
        out.append(f"| {k} | {c['recordsByClassification'][k]} | {c['effectsByClassification'][k] if k != C_STORMRENDER else '-'} |")
    for title, key in (("Candidates for director review", "candidates"), ("Already staged", "alreadyStaged"),
                       ("Manual review", "manualReview"), ("Controls", "controls"),
                       ("Stale (recapture required)", "stale"), ("Missing", "missing"), ("Failed", "failed"),
                       ("Ambiguous (malformed effects; the census cannot be COMPLETE)", "ambiguous")):
        out += ["", f"## {title} ({len(L[key])})", ""]
        out += [f"- `{tid}` {L['records'][tid]['name'] if tid in L['records'] else ''}" for tid in L[key]] or ["- none"]
    for title, key in (("Census problems", "censusProblems"), ("Ledger errors", "ledgerErrors")):
        if L[key]:
            out += ["", f"## {title}", ""] + [f"- {p}" for p in L[key]]
    out += ["", "## Records", "", "| ID | Name | Hidden | Rarity | Effect | Calc | Power | statTypes | generalTypes | Classification | Status |",
            "| --- | --- | --- | --- | ---: | --- | ---: | --- | --- | --- | --- |"]
    for tid, r in L["records"].items():
        effs = r["elementaldamageEffects"] or [None]
        for d in effs:
            cell = (lambda v: "`" + canon(v) + "`" if v != "<absent>" else "absent")
            out.append("| `{}` | {} | {} | {} | {} | {} | {} | {} | {} | {} | {} |".format(
                tid, r.get("name"), r.get("hidden"), r.get("rarity"),
                d["position"] if d else "-", d["calculation"] if d else "-", d["power"] if d else "-",
                cell(d["statTypes"]) if d else "-", cell(d["generalTypes"]) if d else "-",
                d["classification"] if d else "-", r["status"]))
    out += ["", "Observed evidence vs proposed repair: this ledger records only what was captured. A missing selector is a candidate, not proof of unintended design; nothing here proposes or approves a value.", ""]
    return "\n".join(out)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("bundle")
    ap.add_argument("--out-dir", default="reports/elementaldamage_census")
    a = ap.parse_args(argv)
    p = Path(a.bundle)
    raw = p.read_bytes()
    try:
        L = build_ledger(json.loads(raw), bundle_path=p.as_posix(), bundle_sha256=hashlib.sha256(raw).hexdigest())
    except (NotACensus, json.JSONDecodeError) as e:
        print(f"REFUSED: {e}", file=sys.stderr)
        return 2
    out = Path(a.out_dir)
    out.mkdir(parents=True, exist_ok=True)
    stem = p.stem
    (out / f"{stem}.ledger.json").write_text(json.dumps(L, indent=1, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    (out / f"{stem}.ledger.md").write_text(render_md(L), encoding="utf-8")
    print(f"{L['status']}: {L['counts']['dynamicWeapons']} dynamic weapon(s), {len(L['candidates'])} candidate(s), {len(L['controls'])} control(s) -> {out}/{stem}.ledger.json")
    return 0 if L["status"] == "COMPLETE" else 1


if __name__ == "__main__":
    sys.exit(main())
