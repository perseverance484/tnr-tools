#!/usr/bin/env python3
"""lawmap.py - mechanical audit of the engine-law stack.

The 12b matrix once claimed nine validate-class laws that the shipped validator
did not implement; law 14 reached a push because of it. This tool exists so that
"verify against the code, not this file" is a command instead of a discipline.

    python3 lawmap.py <repo-root> [--full]

It cross-checks three surfaces:
  1. docs/ENGINE_LAWS.md          - the numbered text of record
  2. skills/.../12b_LAWS_coverage.md - the claimed enforcement class per law
  3. code                          - `law NN` citations in both skills' scripts
                                     and builder_bundle.js

ERRORS (exit 1):
  - a code citation of a law id that does not exist in ENGINE_LAWS
  - a matrix row whose law id does not exist in ENGINE_LAWS (or vice versa)
  - duplicate law ids or duplicate `## N.` section numbers in ENGINE_LAWS

WARNS (exit 0):
  - matrix class `validate` with no citation in validate.py or artpreflight.py
    (claimed but unauditable by grep - annotate the enforcing site or reclass)
  - matrix class `knowledge` that IS cited in validator code
    (coded beyond the matrix - reclassification candidate)

A citation is the literal `law NN` (any case, `# law NN` comments included).
References restate law text by design and are deliberately NOT scanned; this
audits code, not prose.
"""
# --strict-provenance (WO-07): claimed-validate with no resolvable citation
# becomes an ERROR instead of a warn. Default OFF pending the Phase-3 ruling.
import re, sys
from pathlib import Path

LAW_ITEM = re.compile(r"^(\d{1,3}[a-z]?)\.\s+\*\*")
SECTION = re.compile(r"^##\s+(\d{1,3})[.\s]")
CITE = re.compile(r"(?i)\blaws?[\s:_-]*#?\s*("
                  r"\d{1,3}[a-z]?(?:\s*-\s*\d{1,3})?"
                  r"(?:\s*,\s*\d{1,3}[a-z]?(?:\s*-\s*\d{1,3})?)*)")
MATRIX_ROW = re.compile(r"^\|\s*(\d{1,3}[a-z]?)\s*\|\s*([\w()-]+)\s*\|")


def parse_laws(path):
    ids, sections, in_body = [], [], False
    for line in path.read_text(encoding="utf-8").splitlines():
        m = SECTION.match(line)
        if m:
            in_body = True
            sections.append(m.group(1))
            continue
        if in_body:
            m = LAW_ITEM.match(line)
            if m:
                ids.append(m.group(1))
    return ids, sections


def parse_matrix(path):
    rows = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        m = MATRIX_ROW.match(line)
        if m:
            rows[m.group(1)] = m.group(2).lower()
    return rows


def scan_code(files):
    cites = {}  # law id -> sorted set of file basenames
    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for m in CITE.finditer(text):
            for part in m.group(1).split(","):
                part = part.strip()
                if "-" in part:
                    a, b = part.split("-", 1)
                    try:
                        for n in range(int(a), int(b.strip()) + 1):
                            cites.setdefault(str(n), set()).add(f.name)
                    except ValueError:
                        pass
                elif part:
                    cites.setdefault(part, set()).add(f.name)
    return cites


STRICT_PROV = "--strict-provenance" in sys.argv


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    root = Path(args[0]) if args else Path(__file__).resolve().parents[3]
    full = "--full" in sys.argv
    laws_p = root / "docs/ENGINE_LAWS.md"
    matrix_p = root / "skills/building-tnr-content/12b_LAWS_coverage.md"
    code = sorted(root.glob("skills/*/scripts/*.py")) + [root / "builder_bundle.js"]
    code = [f for f in code if f.name != "lawmap.py"]

    ids, sections = parse_laws(laws_p)
    matrix = parse_matrix(matrix_p)
    cites = scan_code(code)

    errs, warns = [], []

    dup_ids = sorted({i for i in ids if ids.count(i) > 1})
    if dup_ids:
        errs.append(f"duplicate law ids in ENGINE_LAWS: {dup_ids}")
    dup_sec = sorted({s for s in sections if sections.count(s) > 1})
    if dup_sec:
        errs.append(f"duplicate section numbers in ENGINE_LAWS: {dup_sec}")
    nums = sorted({int(re.match(r"\d+", i).group()) for i in ids})
    gaps = [n for n in range(nums[0], nums[-1] + 1) if n not in nums]
    if gaps:
        errs.append(f"gaps in law numbering: {gaps}")

    known = set(ids)
    for i in sorted(set(matrix) - known, key=str):
        errs.append(f"matrix row law {i} has no law text in ENGINE_LAWS")
    for i in sorted(known - set(matrix), key=str):
        errs.append(f"law {i} has text but no matrix row")
    for i in sorted(set(cites) - known, key=str):
        errs.append(f"code cites law {i} which does not exist: {sorted(cites[i])}")

    VALIDATORS = {"validate.py", "artpreflight.py"}
    for i, cls in sorted(matrix.items(), key=lambda kv: (int(re.match(r"\d+", kv[0]).group()), kv[0])):
        where = cites.get(i, set())
        base = cls.split("(")[0]  # validate(warn)/validate(partial) are validate-class
        if base == "validate" and not (where & VALIDATORS):
            (errs if STRICT_PROV else warns).append(
                f"law {i}: matrix says validate, no citation in {sorted(VALIDATORS)}"
                + (" [strict-provenance]" if STRICT_PROV else ""))
        if base == "knowledge" and (where & VALIDATORS):
            warns.append(f"law {i}: matrix says knowledge, but cited by {sorted(where & VALIDATORS)} - reclass candidate")

    if full:
        print(f"{'law':>4}  {'class':<10} cited by")
        for i in sorted(known, key=lambda x: (int(re.match(r'\d+', x).group()), x)):
            print(f"{i:>4}  {matrix.get(i, '-'):<10} {', '.join(sorted(cites.get(i, []))) or '-'}")
        print()

    for e in errs:
        print("ERROR ", e)
    for w in warns:
        print("warn  ", w)
    print(f"\n{len(ids)} laws, {len(matrix)} matrix rows, "
          f"{sum(len(v) for v in cites.values())} citations across {len(code)} files; "
          f"{len(errs)} errors, {len(warns)} warnings")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
