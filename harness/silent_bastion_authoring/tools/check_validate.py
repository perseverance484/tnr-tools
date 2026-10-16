#!/usr/bin/env python3
"""Run skills/building-tnr-content/scripts/validate.py on the composer's VALIDATION-ONLY manifest and
require that the error set is exactly the documented one (each explained in the results report).
Any new error, or any documented error that disappears, fails the gate. Output is kept verbatim.
    python3 tools/check_validate.py <out dir>
"""
import os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "../../.."))
MANIFEST = "state/silent_bastion_authoring/compiled/validation_manifest.candidate.json"
EXPECTED = {
    # Two-phase requirement: exclusive jutsu must exist live before Arakane can equip them by literal id (law 17).
    "[ai:Supreme Commander Arakane]: unresolved ref @jutsu:extermination_order in AI jutsus array": "two-phase build: create exclusives first, then substitute literal ids",
    "[ai:Supreme Commander Arakane]: unresolved ref @jutsu:last_directive in AI jutsus array": "two-phase build: create exclusives first, then substitute literal ids",
    # Locked topology (alt99_f4gate, RUL-2026-10-16-002): both wrong answers lead to the Security Alert approach.
    "[quest:Ghost Ship: The Last Directive].d2.n.puzzle: two or more options in this menu share a target": "locked graph: 1 correct + 2 wrong -> alert",
    "[quest:Ghost Ship: The Last Directive].d3.n.puzzle: two or more options in this menu share a target": "locked graph",
    "[quest:Ghost Ship: The Last Directive].d4.n.puzzle: two or more options in this menu share a target": "locked graph",
    "[quest:Ghost Ship: The Last Directive].d5.n.puzzle: two or more options in this menu share a target": "locked graph",
    # Tooling finding VAL1: gate A shows Countermand's item Clear strips player buffs at 0651b039; the lint is stale.
    'lint Countermand: L18 item effect "clear" excluded from item union': "stale lint vs engine (gate A6 countermandClearResult)",
}

def main():
    out = sys.argv[1]
    r = subprocess.run([sys.executable, os.path.join(REPO, "skills/building-tnr-content/scripts/validate.py"), os.path.join(REPO, MANIFEST)],
                       capture_output=True, text=True, cwd=REPO)
    text = r.stdout + r.stderr
    open(os.path.join(out, "validate_py.txt"), "w").write(text)
    errors = [re.sub(r"^ERROR\s+", "", l).split(": refs are silently")[0].split(", so the menu")[0] for l in text.splitlines() if l.startswith("ERROR")]
    got, want = set(errors), set(EXPECTED)
    unexpected, vanished = sorted(got - want), sorted(want - got)
    summary = re.findall(r"(\d+) errors, (\d+) warnings", text)
    print(f"validate.py: exit {r.returncode}; {summary[-1] if summary else '?'}; documented errors {len(got & want)}/{len(want)}")
    for e in unexpected: print(f"  UNEXPECTED ERROR {e}")
    for e in vanished: print(f"  DOCUMENTED ERROR NO LONGER RAISED {e}")
    return 1 if unexpected or vanished else 0

if __name__ == "__main__":
    sys.exit(main())
