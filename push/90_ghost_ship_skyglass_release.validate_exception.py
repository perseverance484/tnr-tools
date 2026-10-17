#!/usr/bin/env python3
"""
Release-specific validate.py exception for push/90 (RUL-2026-10-12-013; independent re-review GS-R5).

    python3 push/90_ghost_ship_skyglass_release.validate_exception.py           # check (default)
    python3 push/90_ghost_ship_skyglass_release.validate_exception.py --write   # (re)write the ledger

Doctrine D-validate-always requires `python3 scripts/validate.py manifest.json` to report zero
errors, run from the skill data/ directory. For push/90 it reports errors that come from:
- generated contracts lagging the pinned engine (45c/45d at bdec2883 vs 585534d7);
- validator rules the pinned server no longer enforces;
- director-approved graph structure.

The director ruled a release-specific exception instead of reverting correct payloads (RUL-2026-10-12-013).
This tool turns the exception into a gate, not a waiver:
- It runs validate.py exactly as the doctrine says (cwd = skills/building-tnr-content/data, no --strict).
- It classifies EVERY diagnostic line into an approved class. An unclassified line fails.
- It pins the manifest SHA-256, validate.py and every contract file it reads.
- Check mode passes only when the manifest hash, the tool and contract hashes, and the exact multiset of
  diagnostic lines all equal the committed ledger
  (state/ghost_ship_skyglass_release_validate_exception.json).

Any new, changed or missing diagnostic, any manifest change and any validator change therefore voids the
exception and needs a new ruling. The exception covers only this manifest SHA. It does not change
the doctrine, and it is not a precedent.
"""
from __future__ import annotations

import collections
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "skills", "building-tnr-content", "data")
VALIDATE = os.path.join(ROOT, "skills", "building-tnr-content", "scripts", "validate.py")
MANIFEST = "push/90_ghost_ship_skyglass_release.json"
LEDGER = "state/ghost_ship_skyglass_release_validate_exception.json"
CONTRACTS = ["45c_DATA_constructors.json", "45d_DATA_entity_schemas.json", "45g_DATA_checks.json",
             "45h_DATA_lints.json", "32b_DATA_pool.json"]

# Every approved class, with the source evidence that the flagged payload is what the pinned server
# accepts (or what the director approved). A diagnostic matching none of these fails the gate.
CLASSES = [
    ("stale_effect_fields", r"\]\.effects\[\d+\]: [a-z]+: unknown field '",
     "45c (bdec2883) predates the pinned tag schemas. At 585534d7 these keys (direction, description and the noncombatconsumereward reward_* fields) are canonical. Evidence: Forge nested.json and the derive_nested key sets at 585534d7; ItemValidator parse in CONTRACT and the reviewer's source replay; insertAiSchema.effects fixed point in STATS."),
    ("stattypes_none_enum", r"\.statTypes='None' not in enum",
     "IncludeStats.statTypes maps the legacy \"Highest\" to \"None\" at 585534d7 (validators/combat.ts:140), so \"None\" is the stored canonical value. Evidence: STATS effects fixed point; the Katana record is a live push/85 row."),
    ("consume_companion_rule", r"law 78: 'consume' requires a damage or pierce effect",
     "At 585534d7 SuperRefineEffects requires the companion only when rounds === 0. The Crystal's Consume is rounds 2 (RUL-2026-10-11-005/006). Evidence: CONTRACT full ItemValidator accepts the Crystal; the instant negative control still rejects."),
    ("idg_power_cap", r"(law 6: effect 'increasedamagegiven' power \d+ exceeds the cap of 100|increasedamagegiven\.power=\d+ above max 100)",
     "45g tag_power_max is not a server bound: PowerAttributes.power is z.coerce.number().min(0) with no maximum, and Forge deliberately does not wire this check (forge/src/runner/validate.mjs). The 375 and 450 values are RUL-2026-10-12-004; STATS parses them unchanged."),
    ("preferredstat_l05", r"law 14: AI create missing required field 'preferredStat'",
     "Migration 0056 dropped the preferredStat column. Forge 0.5.2 L05 no longer requires it (review correction GS-R3); restoring it would reintroduce the create/read-back conflict."),
    ("approved_shared_menu_target", r"\.(d_parley|d_recon_test): two or more options in this menu share a target",
     "d_parley is the live riddle (two wrong answers lead to the duel; retheme invariant: preserve edges). d_recon_test's two wrong seals lead to the approved lockout (RUL-2026-10-10-003)."),
    ("law60_build_order", r"^manifest: build order: jutsu appears after a later phase$",
     "Law 18/60 requires the AI unequip before the jutsu edits. Forge executes by phase; the dry run verifies the order."),
    ("stale_farm_nullability", r"law 72: 'farm(YieldItemId|ExtractSeedItemId)' is null but is not a field of the item write validator",
     "45d (bdec2883) lacks the farm* keys; Forge's pinned ItemValidator field set includes them and requires farmYieldItemId (forge/src/runner/validate.mjs)."),
    ("captured_selftarget_gate", r"\.rules\[\d+\]: [A-Za-z ]+ is self/ground targeted; a distance gate is meaningless on it",
     "These are captured rule conditions kept under RUL-2026-10-12-003. They are harmless: the gate never restricts a SELF action."),
]


def sha(path: str) -> str:
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def run_validate() -> tuple[int, list[dict], str]:
    proc = subprocess.run([sys.executable, VALIDATE, os.path.join(ROOT, MANIFEST)], cwd=DATA,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, check=False)
    diags = []
    for line in proc.stdout.splitlines():
        m = re.match(r"^(ERROR|warn)\s+(.*)$", line)
        if not m:
            continue
        text = m.group(2)
        cls = next((name for name, rx, _ in CLASSES if re.search(rx, text)), None)
        diags.append({"level": "error" if m.group(1) == "ERROR" else "warning", "class": cls, "text": text})
    summary = next((l for l in proc.stdout.splitlines() if re.match(r"^\d+ errors, \d+ warnings$", l)), "")
    return proc.returncode, diags, summary


def build() -> dict:
    rc, diags, summary = run_validate()
    unclassified = [d["text"] for d in diags if d["class"] is None]
    if unclassified:
        raise SystemExit("REFUSED: diagnostics outside every approved class:\n" + "\n".join(unclassified))
    counts = collections.Counter((d["class"], d["level"]) for d in diags)
    return {
        "schema": "tnr.release_validate_exception",
        "ruling": "RUL-2026-10-12-013",
        "scope": "push/90 only, at exactly this manifest SHA-256; not a doctrine change and not a precedent",
        "command": "cd skills/building-tnr-content/data && python3 ../scripts/validate.py ../../../push/90_ghost_ship_skyglass_release.json",
        "manifest": {"path": MANIFEST, "sha256": sha(os.path.join(ROOT, MANIFEST))},
        "validator": {"validate.py": sha(VALIDATE), **{c: sha(os.path.join(DATA, c)) for c in CONTRACTS}},
        "exitCode": rc,
        "summary": summary,
        "classes": [{"class": name, "evidence": ev,
                     "errors": counts.get((name, "error"), 0), "warnings": counts.get((name, "warning"), 0)}
                    for name, _, ev in CLASSES],
        "diagnostics": sorted(diags, key=lambda d: (d["class"], d["level"], d["text"])),
    }


def main() -> int:
    doc = build()
    text = json.dumps(doc, indent=1, ensure_ascii=False) + "\n"
    path = os.path.join(ROOT, LEDGER)
    if "--write" in sys.argv[1:]:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"wrote {LEDGER}: {doc['summary']} in {sum(1 for c in doc['classes'] if c['errors'] or c['warnings'])} approved classes")
        return 0
    if not os.path.exists(path):
        print(f"EXCEPTION VOID: {LEDGER} missing", file=sys.stderr)
        return 1
    want = json.load(open(path, encoding="utf-8"))
    problems = []
    for key in ("manifest", "validator", "exitCode", "summary"):
        if want.get(key) != doc[key]:
            problems.append(f"{key}: ledger {want.get(key)} != now {doc[key]}")
    if want.get("diagnostics") != doc["diagnostics"]:
        a = collections.Counter(json.dumps(d, sort_keys=True) for d in want.get("diagnostics", []))
        b = collections.Counter(json.dumps(d, sort_keys=True) for d in doc["diagnostics"])
        problems.append(f"diagnostics differ: {len(list((b - a).elements()))} new, {len(list((a - b).elements()))} gone")
    if problems:
        print(f"EXCEPTION VOID ({doc['ruling']} does not cover this state):\n  " + "\n  ".join(problems), file=sys.stderr)
        return 1
    print(f"EXCEPTION HOLDS: validate.py '{doc['summary']}' (exit {doc['exitCode']}) is exactly the ledger approved by "
          f"{doc['ruling']} for {MANIFEST} sha256 {doc['manifest']['sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
