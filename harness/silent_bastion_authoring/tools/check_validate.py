#!/usr/bin/env python3
"""Run skills/building-tnr-content/scripts/validate.py on the composer's VALIDATION-ONLY manifest and
require that its diagnostics are exactly the documented ones (each explained in the results report).

Locked, per review F3: every ERROR line verbatim with its multiplicity (a Counter, not a set), the
summary error and warning counts, and validate.py's exit status (1 = errors reported; a crash, kill
or a clean 0 all fail this gate). Any new, missing, duplicated or reworded error fails the gate.
This is NOT a clean validate.py result: no manifest built from this may be described as validate-clean.
Output is kept verbatim.
    python3 tools/check_validate.py <out dir>
"""
import os, re, subprocess, sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "../../.."))
MANIFEST = "state/silent_bastion_authoring/compiled/validation_manifest.candidate.json"
EXPECTED_EXIT = 1
EXPECTED_WARNINGS = 9  # engagement-gated self-buffs on 9 regulars (intentional)

_VALID = ("Valid: appearAnimation, appearSfx, calculation, disappearAnimation, disappearSfx, friendlyFire, power, "
          "powerPerLevel, rounds, staticAnimation, staticAssetPath, target, timeTracker, type")
_STRIP = "refs are silently STRIPPED server-side and the AI stands naked (law 17). Substitute literal ids"
_SHARE = "two or more options in this menu share a target, so the menu is narrower than it looks. Give each option its own node"
# (exact ERROR line after the "ERROR  " prefix, rationale). Listed once per expected occurrence.
EXPECTED = [
    # Two-phase requirement: exclusive jutsu must exist live before Arakane can equip them by literal id (law 17).
    (f"[ai:Supreme Commander Arakane]: unresolved ref @jutsu:extermination_order in AI jutsus array: {_STRIP}", "two-phase build"),
    (f"[ai:Supreme Commander Arakane]: unresolved ref @jutsu:last_directive in AI jutsus array: {_STRIP}", "two-phase build"),
    # Locked topology (alt99_f4gate, RUL-2026-10-16-002): both wrong answers lead to the Security Alert approach.
    # Validator exception granted by RUL-2026-10-16-012.
    *[(f"[quest:Ghost Ship: The Last Directive].d{d}.n.puzzle: {_SHARE}", "RUL-2026-10-16-012 exception") for d in (2, 3, 4, 5)],
    # Tooling finding VAL1: gate A shows Countermand's item Clear strips player buffs at 0651b039; the lint is stale.
    ('lint Countermand: L18 item effect "clear" excluded from item union', "VAL1 stale lint (gate A6)"),
    # Tooling finding VAL2: data/46_DATA_tag_schemas.json was extracted 2026-07-10, before NonCombatConsumeRewardTag gained
    # rewardMode/weightedCache. At 0651b039 the engine accepts both (gate C: NonCombatConsumeRewardTag, ItemValidator, real openings).
    *[(f"[item:Bastion {fam} Cache [provisional]].effects[0]: noncombatconsumereward: unknown field '{fld}'. {_VALID}", "VAL2 stale tag schema")
      for fam in ("Arsenal", "Research") for fld in ("rewardMode", "weightedCache")],
]


def judge(text, returncode):
    """Pure comparison of one validate.py run against the documented diagnostics: (summary, problems)."""
    got = Counter(re.sub(r"^ERROR\s+", "", l) for l in text.splitlines() if l.startswith("ERROR"))
    want = Counter(line for line, _ in EXPECTED)
    summary = re.findall(r"^(\d+) errors, (\d+) warnings$", text, re.M)
    n_err, n_warn = (int(summary[-1][0]), int(summary[-1][1])) if summary else (None, None)
    problems = []
    if returncode != EXPECTED_EXIT:
        problems.append(f"validate.py exit {returncode}, expected {EXPECTED_EXIT}")
    if n_err != sum(want.values()):
        problems.append(f"summary reports {n_err} errors, expected {sum(want.values())}")
    if n_warn != EXPECTED_WARNINGS:
        problems.append(f"summary reports {n_warn} warnings, expected {EXPECTED_WARNINGS}")
    if sum(got.values()) != n_err:
        problems.append(f"{sum(got.values())} ERROR lines parsed but summary says {n_err}")
    for line in sorted(set(got) | set(want)):
        if got[line] != want[line]:
            problems.append(f"{'UNEXPECTED' if not want[line] else 'MISSING' if not got[line] else 'COUNT'} "
                            f"x{got[line]} (want x{want[line]}): {line[:160]}")
    summary_line = (f"validate.py: exit {returncode}; {n_err} errors, {n_warn} warnings; "
                    f"documented errors {sum((got & want).values())}/{sum(want.values())}")
    return summary_line, problems


def main():
    out = sys.argv[1]
    r = subprocess.run([sys.executable, os.path.join(REPO, "skills/building-tnr-content/scripts/validate.py"), os.path.join(REPO, MANIFEST)],
                       capture_output=True, text=True, cwd=REPO)
    text = r.stdout + r.stderr
    open(os.path.join(out, "validate_py.txt"), "w").write(text)
    summary_line, problems = judge(text, r.returncode)
    print(summary_line)
    for p in problems:
        print(f"  {p}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
