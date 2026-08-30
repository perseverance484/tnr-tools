#!/usr/bin/env python3
"""schema_diff.py - the mechanical adoption gate for regenerated 45x contracts.

The SECTOR_TYPES corruption was an enum whose member SET silently changed while
its size did not: a naive regen would have shipped a wrong union into both
validate.py and the builder. This gate makes that class impossible to adopt:
no regenerated 45c/45d/45e file is adopted unless `schema_diff.py diff OLD NEW`
exits 0.

Rules (buf / json-schema-diff-validator shaped, fail-closed):

  BREAKING (exit 1)                        ADDITIVE (listed, exit 0)
  - constant enum member removed           - new constant / new member
  - union variant removed                  - new union / new variant
  - inline enum member removed             - new field, new entity
  - entity field removed                   - field became optional
  - field type changed
  - field optional -> required

Member sets are compared BY VALUE, never by count. Output is a phone-readable
ADDITIONS / REMOVALS / CHANGES list.

Invariants mode audits a single 45c so the extractor fails loudly instead of
emitting plausible wrongness:

  python3 schema_diff.py --invariants 45c.json --constants 45e.json

  I1  every variant's discriminator literal equals its variant key, and is
      unique within its union (the invariant that catches SECTOR_TYPES-class
      collisions at the source)
  I2  every enum_ref resolves: bare name (qualifier after '@' stripped) must
      exist in 45e constants or as a 45c union
  I3  every enum-typed field carries members inline OR by enum_ref
      (reference-only members are legitimate; memberless AND refless is not)

Emission order of enum members is NOT audited: TNR enum order is semantic
(LetterRanks D..H). Order-independence for review comes from this gate
comparing sets, not from sorting the source of truth.

Usage
  python3 schema_diff.py diff OLD.json NEW.json
  python3 schema_diff.py --invariants 45c.json [--constants 45e.json]

Adoption flow (docs/00_INDEX.md): extract -> --invariants -> diff old new ->
adopt only on exit 0. Runs anywhere; stdlib only.
"""
import json
import sys


# ---------------------------------------------------------------- atom walks

def atoms(doc):
    """Flatten a 45x file into (kind, *path) contract atoms.

    Kinds: const-member, union-variant, enum-member, field, ftype, required.
    File kind is sniffed from top-level keys; a file may carry several.
    """
    out = set()
    consts = doc.get("constants")
    if isinstance(consts, dict):
        for name, spec in consts.items():
            vals = spec.get("value") if isinstance(spec, dict) else spec
            if isinstance(vals, list):
                for v in vals:
                    if isinstance(v, (str, int, float, bool)):
                        out.add(("const-member", name, str(v)))
    unions = doc.get("unions")
    if isinstance(unions, dict):
        for uname, variants in unions.items():
            if not isinstance(variants, dict):
                continue
            for vkey, var in variants.items():
                out.add(("union-variant", uname, vkey))
                for fname, f in (var.get("fields") or {}).items() if isinstance(var, dict) else []:
                    if isinstance(f, dict) and isinstance(f.get("enum"), list):
                        for m in f["enum"]:
                            out.add(("enum-member", uname + "." + vkey + "." + fname, str(m)))
    ents = doc.get("entities")
    if isinstance(ents, dict):
        for ename, ent in ents.items():
            for fname, f in (ent.get("fields") or {}).items() if isinstance(ent, dict) else []:
                if not isinstance(f, dict):
                    continue
                out.add(("field", ename, fname))
                if f.get("type"):
                    out.add(("ftype", ename, fname, str(f["type"])))
                if f.get("optional") is False:
                    out.add(("required", ename, fname))
                if isinstance(f.get("enum"), list):
                    for m in f["enum"]:
                        out.add(("enum-member", ename + "." + fname, str(m)))
    return out


BREAK_ON_REMOVE = {"const-member", "union-variant", "enum-member", "field"}


def cmd_diff(old_path, new_path):
    old, new = atoms(json.load(open(old_path))), atoms(json.load(open(new_path)))
    removed = sorted(old - new)
    added = sorted(new - old)

    # type changes and required-flips pair a removal with an addition on the
    # same (entity, field); report them as CHANGES, not as remove+add noise.
    def keyed(s, kind):
        return {a[1:3]: a for a in s if a[0] == kind}
    changes, hide = [], set()
    ot, nt = keyed(set(removed), "ftype"), keyed(set(added), "ftype")
    for k in set(ot) & set(nt):
        changes.append(("type-changed", k[0], k[1], ot[k][3] + " -> " + nt[k][3]))
        hide.add(ot[k]); hide.add(nt[k])
    orq, nrq = keyed(set(removed), "required"), keyed(set(added), "required")
    for k in set(nrq) - set(orq):          # became required = tightening
        changes.append(("now-required", k[0], k[1], "optional -> required"))
        hide.add(nrq[k])
    for k in set(orq) - set(nrq):          # became optional = relaxation, additive
        hide.add(orq[k])

    removed = [a for a in removed if a not in hide]
    added = [a for a in added if a not in hide]
    breaking = [a for a in removed if a[0] in BREAK_ON_REMOVE] + changes

    def show(label, rows):
        if rows:
            print(label)
            for r in rows[:60]:
                print("  " + "  ".join(str(x) for x in r))
            if len(rows) > 60:
                print("  ... %d more" % (len(rows) - 60))
    show("REMOVALS", removed)
    show("CHANGES", changes)
    show("ADDITIONS", added)
    if breaking:
        print("\nBREAKING: %d change(s) - DO NOT ADOPT (exit 1)" % len(breaking))
        return 1
    print("\nno breaking changes: %d addition(s), safe to adopt (exit 0)" % len(added))
    return 0


# ---------------------------------------------------------------- invariants

def cmd_invariants(ctor_path, const_path=None):
    doc = json.load(open(ctor_path))
    consts = {}
    if const_path:
        consts = json.load(open(const_path)).get("constants") or {}
    unions = doc.get("unions") or {}
    errs = []
    for uname, variants in unions.items():
        if not isinstance(variants, dict):
            continue
        seen = {}
        for vkey, var in variants.items():
            fields = (var.get("fields") or {}) if isinstance(var, dict) else {}
            tf = fields.get("type") or {}
            lit = tf.get("literal")
            if lit is not None and lit != vkey:
                errs.append("I1 %s.%s: discriminator literal %r != variant key" % (uname, vkey, lit))
            if lit is not None:
                if lit in seen:
                    errs.append("I1 %s: duplicate discriminator %r (%s, %s)" % (uname, lit, seen[lit], vkey))
                seen[lit] = vkey
            for fname, f in fields.items():
                if not isinstance(f, dict):
                    continue
                ref = f.get("enum_ref")
                if ref:
                    bare = ref.split("@", 1)[0]
                    if bare not in consts and bare not in unions:
                        errs.append("I2 %s.%s.%s: enum_ref %r unresolved" % (uname, vkey, fname, ref))
                if f.get("type") == "enum" and not f.get("enum") and not ref:
                    errs.append("I3 %s.%s.%s: enum-typed with no members and no enum_ref" % (uname, vkey, fname))
    for e in errs[:40]:
        print(e)
    n_var = sum(len(v) for v in unions.values() if isinstance(v, dict))
    print("invariants: %d union(s), %d variant(s) audited; %d error(s)" % (len(unions), n_var, len(errs)))
    return 1 if errs else 0


def main():
    a = sys.argv[1:]
    if len(a) >= 3 and a[0] == "diff":
        return cmd_diff(a[1], a[2])
    if a and a[0] == "--invariants":
        cp = a[a.index("--constants") + 1] if "--constants" in a else None
        return cmd_invariants(a[1], cp)
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
