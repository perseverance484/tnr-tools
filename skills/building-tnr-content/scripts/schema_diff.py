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
  - field type changed                    (entity fields AND union-variant fields)
  - field optional -> required            (entity fields AND union-variant fields)

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

Reviewed removals (--accept LEDGER.json): a genuine upstream removal (a column a migration
dropped) can never pass the diff on its own. The ledger names, for one exact OLD/NEW file pair
(sha256), every breaking atom and the evidenced class it belongs to; the diff then exits 0 only
when the breaking set and the ledger are IDENTICAL. Any unlisted removal, stale entry or file
change fails exactly as before. 45g is covered (every removed check entry is breaking), and so
is a key removed from a union variant.

Usage
  python3 schema_diff.py diff OLD.json NEW.json [--accept LEDGER.json]
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
                    # a key leaving a tag/objective/action is a removal like any other; it was
                    # invisible here, so a regen could drop `elements` from a tag and pass
                    out.add(("variant-field", uname + "." + vkey, fname))
                    # type and required-ness of a variant's field, as for entity fields: a tag's
                    # `power` turning from number to string changed no other atom (PR #76 review F2)
                    if isinstance(f, dict) and f.get("type"):
                        out.add(("vfield-type", uname + "." + vkey, fname, str(f["type"])))
                    if isinstance(f, dict) and not f.get("optional") and "default" not in f:
                        out.add(("vfield-required", uname + "." + vkey, fname))
                    if isinstance(f, dict) and isinstance(f.get("enum"), list):
                        for m in f["enum"]:
                            out.add(("enum-member", uname + "." + vkey + "." + fname, str(m)))
    # 45c intersections (PetSpeciesEffect = AllTags.and(z.object({skillTarget}))): keys every
    # member of the base union also accepts; a key leaving one is a removal like a variant field's
    inter = doc.get("intersections")
    if isinstance(inter, dict):
        for iname, spec in inter.items():
            fields = spec.get("fields") if isinstance(spec, dict) else None
            for fname, f in (fields or {}).items():
                out.add(("variant-field", iname, fname))
                if isinstance(f, dict) and isinstance(f.get("enum"), list):
                    for m in f["enum"]:
                        out.add(("enum-member", iname + "." + fname, str(m)))
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
    # 45f procedures: router -> procedure -> {procedure guard, kind}. Also had no atoms.
    routers = doc.get("routers")
    if isinstance(routers, dict):
        for rname, procs in routers.items():
            for pname, spec in (procs or {}).items():
                out.add(("procedure", rname, pname))
                if isinstance(spec, dict):
                    for k in ("procedure", "kind"):
                        if spec.get(k):
                            out.add(("proc-" + k, rname + "." + pname, str(spec[k])))
    # 45g check config: every block is {"_class", "fields"|"values"}. It had no atoms at all, so
    # `diff OLD_45g NEW_45g` reported "0 additions, safe to adopt" whatever changed.
    if "_contract" in doc and any(isinstance(v, dict) and "_class" in v for v in doc.values()):
        for block, spec in doc.items():
            if block.startswith("_") or not isinstance(spec, dict) or "_class" not in spec:
                continue
            for key in ("fields", "values"):
                if key in spec:
                    for path, val in _leaves(spec[key], block + "." + key):
                        out.add(("check", path, val))
    return out


def _leaves(v, path):
    """(path, scalar) for every leaf of a 45g block; list members by value, so order is free."""
    if isinstance(v, dict):
        for k, x in v.items():
            yield from _leaves(x, path + "." + str(k))
    elif isinstance(v, list):
        for x in v:
            if isinstance(x, (dict, list)):
                yield from _leaves(x, path + "[]")
            else:
                yield path, json.dumps(x)
    else:
        yield path, json.dumps(v)


# 45g removals are breaking without exception: a check config is read by validate.py AND the
# builder, and a removed entry silently changes what both refuse or require.
BREAK_ON_REMOVE = {"const-member", "union-variant", "enum-member", "field", "variant-field", "check",
                   "procedure", "proc-procedure", "proc-kind"}


def _sha256(path):
    import hashlib
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


# (type atom, required atom, field atom) for entity fields and for union-variant fields
PAIRED = (("ftype", "required", "field"), ("vfield-type", "vfield-required", "variant-field"))


def classify(old, new):
    """(removed, added, changes, breaking) for two atom sets. One implementation, shared by
    cmd_diff and scripts/schema_adoption_ledger.py, so the gate and its ledger cannot disagree."""
    removed = sorted(old - new)
    added = sorted(new - old)

    # type changes and required-flips pair a removal with an addition on the
    # same (owner, field); report them as CHANGES, not as remove+add noise.
    def keyed(s, kind):
        return {a[1:3]: a for a in s if a[0] == kind}
    changes, hide = [], set()
    for tkind, rkind, fkind in PAIRED:
        ot, nt = keyed(set(removed), tkind), keyed(set(added), tkind)
        for k in set(ot) & set(nt):
            changes.append(("type-changed", k[0], k[1], ot[k][3] + " -> " + nt[k][3]))
            hide.add(ot[k]); hide.add(nt[k])
        for k in set(ot) - set(nt):
            hide.add(ot[k])
            if (fkind,) + k in new:            # field kept, type dropped: still a type change
                changes.append(("type-changed", k[0], k[1], ot[k][3] + " -> (none)"))
            # else the field itself went, and its removal is the breaking atom
        for k in set(nt) - set(ot):          # a field that is new, or newly typed: additive
            hide.add(nt[k])
        orq, nrq = keyed(set(removed), rkind), keyed(set(added), rkind)
        for k in set(nrq) - set(orq):          # became required = tightening
            hide.add(nrq[k])
            # only a field OLD already had can flip optional -> required; a field OLD lacked is
            # an addition (it was reported as a flip, so every newly extracted field looked breaking)
            if (fkind,) + k in old:
                changes.append(("now-required", k[0], k[1], "optional -> required"))
        for k in set(orq) - set(nrq):          # became optional = relaxation, additive
            hide.add(orq[k])

    removed = [a for a in removed if a not in hide]
    added = [a for a in added if a not in hide]
    changes.sort()   # set iteration order varies with PYTHONHASHSEED; ledgers must be stable
    breaking = [a for a in removed if a[0] in BREAK_ON_REMOVE] + changes
    return removed, added, changes, breaking


def cmd_diff(old_path, new_path, accept_path=None):
    old, new = atoms(json.load(open(old_path))), atoms(json.load(open(new_path)))
    removed, added, changes, breaking = classify(old, new)

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
    if breaking and accept_path:
        return _check_accept(accept_path, old_path, new_path, breaking, len(added))
    if breaking:
        print("\nBREAKING: %d change(s) - DO NOT ADOPT (exit 1)" % len(breaking))
        return 1
    print("\nno breaking changes: %d addition(s), safe to adopt (exit 0)" % len(added))
    return 0


def _check_accept(accept_path, old_path, new_path, breaking, n_added):
    """A reviewed-removal ledger turns a breaking diff into an adoption ONLY when it is about
    exactly these two files (sha256 of OLD and NEW) and lists exactly the breaking set: every
    breaking atom accepted under a class with source evidence, and no accepted atom that is not
    breaking. Anything else - a new removal, a changed file, a stale entry - fails as before."""
    with open(accept_path) as fh:
        led = json.load(fh)
    pair = None
    for p in led.get("files", []):
        if p.get("old_sha256") == _sha256(old_path) and p.get("new_sha256") == _sha256(new_path):
            pair = p
            break
    if pair is None:
        print("\nBREAKING: %d change(s); ledger %s covers neither this OLD nor this NEW file "
              "(sha256 mismatch) - DO NOT ADOPT (exit 1)" % (len(breaking), accept_path))
        return 1
    classes = led.get("classes", {})
    want = {json.dumps(list(a)) for a in breaking}
    have, bad = {}, []
    for row in pair.get("accepted", []):
        key = json.dumps(row.get("atom"))
        cls = row.get("class")
        if cls not in classes or not (classes[cls].get("evidence") or "").strip():
            bad.append("accepted atom with no evidenced class: %s (%s)" % (key, cls))
        have[key] = cls
    missing = sorted(want - set(have))
    stale = sorted(set(have) - want)
    for m in missing[:40]:
        print("  UNACCEPTED  " + m)
    for m in stale[:40]:
        print("  STALE       " + m)
    for b in bad[:40]:
        print("  " + b)
    if missing or stale or bad:
        print("\nBREAKING: %d change(s); ledger mismatch (%d unaccepted, %d stale, %d unevidenced)"
              " - DO NOT ADOPT (exit 1)" % (len(breaking), len(missing), len(stale), len(bad)))
        return 1
    from collections import Counter
    by = Counter(have.values())
    print("\nACCEPTED: all %d breaking change(s) are in the reviewed ledger %s (%s); %d addition(s)."
          " Adopt (exit 0)." % (len(breaking), accept_path,
                                ", ".join("%s %d" % kv for kv in sorted(by.items())), n_added))
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
        acc = a[a.index("--accept") + 1] if "--accept" in a else None
        return cmd_diff(a[1], a[2], acc)
    if a and a[0] == "--invariants":
        cp = a[a.index("--constants") + 1] if "--constants" in a else None
        return cmd_invariants(a[1], cp)
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main())
