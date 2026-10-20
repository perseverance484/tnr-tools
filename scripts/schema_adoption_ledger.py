#!/usr/bin/env python3
"""Build (or check) the reviewed-removal ledger for one 45c/45d/45e/45f/45g adoption.

    python3 scripts/schema_adoption_ledger.py OLD_SRC NEW_SRC OLD_DIR NEW_DIR --write state/LEDGER.json
    python3 scripts/schema_adoption_ledger.py OLD_SRC NEW_SRC OLD_DIR NEW_DIR --check state/LEDGER.json

OLD_SRC / NEW_SRC  read-only TheNinjaRPG checkouts the committed and the regenerated files were
                   extracted from (bdec2883 and 6524d0fb for the 2026-10-20 adoption).
OLD_DIR / NEW_DIR  the 45x files before and after, named as in skill data/
                   (45c_DATA_constructors.json, ...). Before adoption OLD_DIR is skill data/;
                   after it, extract the pre-adoption files with `git show <base>:<path>`.

`schema_diff.py diff OLD NEW` fails closed on every removal. Some removals are genuine (a
migration dropped a column) and some are the extractor correcting itself (a "...Name" spread
marker that was never a value). Neither may be waved through by hand, so this tool CLASSIFIES
every breaking atom and re-checks each class against the source with a method independent of
schema_extract.py:

  - field / tag-key removals: Forge's own derive_fields.mjs / derive_nested.mjs run at both pins;
  - constant members and procedures: the declaration text read at both pins;
  - consequences (an enum member, nullable or required entry of a removed field) only when the
    field itself is a verified removal;
  - extractor corrections: a mechanical property of the old value (a "..." marker; an enum the
    old raw expression never declared; a power cap the old file took from the wrong spread).

An atom no rule verifies makes the tool exit 1 and is printed. `schema_diff.py diff OLD NEW
--accept LEDGER` then passes only for these exact files and this exact breaking set.
No network; the checkouts are read, never executed (Forge's derivation tools are run with node).
"""
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "skills", "building-tnr-content", "scripts"))
import schema_diff as sd  # noqa: E402

FILES = [("45c_DATA_constructors.json", None), ("45d_DATA_entity_schemas.json", None),
         ("45e_DATA_constants.json", None), ("45f_DATA_procedures.json", None),
         ("45g_DATA_checks.json", None)]

CLASSES = {
    "upstream_field_removed": (
        "A key the validator no longer declares at the new pin. Verified independently: Forge "
        "tools/derive_fields.mjs (entity columns) or tools/derive_nested.mjs (tag/objective/AI "
        "keys) lists it at the old pin and not at the new one. Examples: migration 0056 dropped "
        "required{Ninjutsu,...}{Offence,Defence}; ten tags stopped spreading IncludeStats."),
    "upstream_const_member_removed": (
        "A member the constant's declaration no longer contains at the new pin (comments "
        "stripped, spreads followed), present at the old pin. E.g. StatTypes lost \"Highest\" "
        "(IncludeStats maps legacy Highest to None), UserStatuses lost KAGE_QUEUED."),
    "upstream_procedure_removed": (
        "A router procedure no longer declared in its router file at the new pin "
        "(kage challenges, train.stopTraining -> stopMasteryTraining, ...); its guard/kind atoms "
        "go with it."),
    "consequence_of_removal": (
        "An enum member, or a 45g nullable/required/enum/null-strip entry, that belonged to a "
        "field verified as removed in this same ledger, or to a constant member verified as "
        "removed (statClassification lost \"Highest\" because StatTypes did)."),
    "extractor_spread_marker": (
        "The old file carried a literal \"...Name\" spread marker as if it were a value "
        "(ElementNames held \"...BasicElementName\" instead of Fire/Water/...). The fixed "
        "extractor expands the spread; the marker was never a value the server accepts."),
    "extractor_nested_key": (
        "The old line-based parser attributed a key of an inline nested z.object to the outer "
        "variant (dialog.text came from nextObjectiveId: z.array(z.object({text, ...}))). Forge "
        "derive_nested at the old pin confirms it was never a dialog key."),
    "extractor_helper_overreach": (
        "The old helper collector read a fixed 600-character window past a helper, so "
        "z.enum(WeaponTypes) from unrelated code became the enum of every stat requirement "
        "(requiredStrength...). The old field's own raw expression declares no enum."),
    "extractor_spread_precedence": (
        "The old flattener let the FIRST spread win; zod lets the LAST win. BaseAttributes.power "
        "(max 100) was reported for tags whose PowerAttributes.power (min 0, no max) overrides "
        "it: the 45g tag_power_max mistake Forge validate.mjs documents. The new 45c field for "
        "that tag has no max."),
    "extractor_ref_resolution": (
        "A field typed by a named schema was recorded as an opaque object; the fixed extractor "
        "resolves the name (aiRule.action: ZodAllAiActions is a z.union)."),
}


def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def breaking(old_doc, new_doc):
    """The same breaking set schema_diff.cmd_diff computes."""
    old, new = sd.atoms(old_doc), sd.atoms(new_doc)
    removed, added = sorted(old - new), sorted(new - old)
    keyed = lambda s, k: {a[1:3]: a for a in s if a[0] == k}  # noqa: E731
    changes, hide = [], set()
    ot, nt = keyed(set(removed), "ftype"), keyed(set(added), "ftype")
    for k in set(ot) & set(nt):
        changes.append(("type-changed", k[0], k[1], ot[k][3] + " -> " + nt[k][3]))
        hide.update((ot[k], nt[k]))
    orq, nrq = keyed(set(removed), "required"), keyed(set(added), "required")
    for k in set(nrq) - set(orq):
        hide.add(nrq[k])
        if ("field",) + k in old:
            changes.append(("now-required", k[0], k[1], "optional -> required"))
    for k in set(orq) - set(nrq):
        hide.add(orq[k])
    return [a for a in removed if a not in hide and a[0] in sd.BREAK_ON_REMOVE] + changes


# ------------------------------------------------------------- independent source reads

def forge_derive(tool, src):
    out = subprocess.run(["node", os.path.join(ROOT, "forge", "tools", tool), src, "ledger"],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def nested_keys(src):
    raw = forge_derive("derive_nested.mjs", src)
    sets = raw["sets"]
    out = {}
    for sec, v in raw.items():
        if sec in ("_meta", "sets") or isinstance(v, int):
            continue
        out[sec] = {d: set(sets[i]) for d, i in v.items()}
    return out


def entity_fields(src):
    return {e: set(spec.get("fields", {})) for e, spec in forge_derive("derive_fields.mjs", src)["entities"].items()}


def _strip(s):
    return re.sub(r"//[^\n]*", "", re.sub(r"/\*.*?\*/", "", s, flags=re.S))


def _decl(src, name):
    files = [os.path.join(src, "app/drizzle/constants.ts"), os.path.join(src, "app/src/libs/combat/constants.ts")]
    vdir = os.path.join(src, "app/src/validators")
    files += sorted(os.path.join(vdir, n) for n in os.listdir(vdir) if n.endswith(".ts"))
    for f in files:
        if not os.path.exists(f):
            continue
        s = open(f).read()
        m = re.search(r"^(?:export\s+)?const\s+%s\b[^=]*=\s*" % re.escape(name), s, re.M)
        if not m:
            continue
        i = m.end()
        if s[i] in "[{":
            op, cl = s[i], "]" if s[i] == "[" else "}"
            d = 0
            for j in range(i, len(s)):
                d += (s[j] == op) - (s[j] == cl)
                if d == 0:
                    return s[i:j + 1]
        return s[i:i + 400]
    return None


def const_members(src, name, seen=()):
    raw = _decl(src, name)
    if raw is None:
        return None
    raw = _strip(raw)
    out = set(re.findall(r'"([^"]+)"', raw)) | set(re.findall(r"'([^']+)'", raw))
    out |= set(re.findall(r"^\s*([A-Za-z_]\w*)\s*:", raw, re.M))
    for sp in re.findall(r"\.\.\.([A-Za-z_]\w*)", raw):
        if sp not in seen:
            out |= const_members(src, sp, seen + (name,)) or set()
    return out


def has_procedure(src, router, proc):
    p = os.path.join(src, "app/src/server/api/routers", router + ".ts")
    return os.path.exists(p) and re.search(r"^\s+%s\s*:" % re.escape(proc), _strip(open(p).read()), re.M) is not None


# ------------------------------------------------------------------------- classify

FAMILY = {"AllTags": "effects", "AllObjectives": "objectives", "allObjectiveSchema": "objectives",
          "ZodAllAiActions": "aiActions", "ZodAllAiConditions": "aiConditions"}


def classify(name, atom, ctx):
    kind = atom[0]
    if kind in ("const-member", "enum-member") and atom[2].startswith("..."):
        return "extractor_spread_marker"
    if kind == "const-member":
        old_m, new_m = const_members(ctx["old"], atom[1]), const_members(ctx["new"], atom[1])
        if old_m and atom[2] in old_m and (new_m is None or atom[2] not in new_m):
            ctx["const_removed"].add((atom[1], atom[2]))
            return "upstream_const_member_removed"
        return None
    if kind == "variant-field":
        union, variant = atom[1].split(".", 1)
        fam = FAMILY.get(union)
        was = atom[2] in ctx["nested_old"].get(fam, {}).get(variant, set())
        now = atom[2] in ctx["nested_new"].get(fam, {}).get(variant, set())
        if was and not now:
            ctx["field_removed"].add(atom[1:3])
            return "upstream_field_removed"
        if not was and not now and variant in ctx["nested_old"].get(fam, {}):
            return "extractor_nested_key"
        return None
    if kind == "field":
        was, now = atom[2] in ctx["fields_old"].get(atom[1], set()), atom[2] in ctx["fields_new"].get(atom[1], set())
        if was and not now:
            ctx["field_removed"].add(atom[1:3])
            return "upstream_field_removed"
        return None
    if kind in ("procedure", "proc-procedure", "proc-kind"):
        router, proc = (atom[1], atom[2]) if kind == "procedure" else atom[1].split(".", 1)
        if has_procedure(ctx["old"], router, proc) and not has_procedure(ctx["new"], router, proc):
            return "upstream_procedure_removed"
        return None
    if kind in ("type-changed", "now-required") and atom[1] == "aiRule":
        old_raw = ctx["old_docs"]["45d"]["entities"]["aiRule"]["fields"][atom[2]].get("raw", "")
        if re.fullmatch(r"[A-Za-z_]\w*", old_raw):
            return "extractor_ref_resolution"
        return None
    return None


def classify_late(name, atom, ctx):
    """Classes that depend on verified removals found in the first pass."""
    kind = atom[0]
    if kind == "enum-member":
        path = atom[1].split(".")
        if name == "45c" and (".".join(path[:2]), path[2]) in ctx["field_removed"]:
            return "consequence_of_removal"
        if name == "45d" and (path[0], path[1]) in ctx["field_removed"]:
            return "consequence_of_removal"
        return None
    if kind != "check":
        return None
    parts = atom[1].split(".")
    block = parts[0]
    val = json.loads(atom[2])
    ents_old = ctx["old_docs"]["45d"]["entities"]
    ents_new = ctx["new_docs"]["45d"]["entities"]
    if block == "enums":
        ent, field = parts[2], parts[3]
        if (ent, field) in ctx["field_removed"]:
            return "consequence_of_removal"
        of, nf = ents_old.get(ent, {}).get("fields", {}).get(field), ents_new.get(ent, {}).get("fields", {}).get(field)
        if of and nf and "enum(" not in (of.get("raw") or "") and not nf.get("enum") and not nf.get("enum_ref"):
            return "extractor_helper_overreach"
        ref = (nf or {}).get("enum_ref", "")
        if nf and ref and (ref, val) in ctx["const_removed"]:
            return "consequence_of_removal"
        return None
    if block in ("nullable", "required_on_create", "cap_100", "booleans", "date_fields"):
        return "consequence_of_removal" if (parts[2], val) in ctx["field_removed"] else None
    if block == "null_strip_exempt":
        return "consequence_of_removal" if any(f == val for _e, f in ctx["field_removed"]) else None
    if block == "tag_power_max":
        tag = parts[2]
        power = ctx["new_docs"]["45c"]["unions"].get("AllTags", {}).get(tag, {}).get("fields", {}).get("power", {})
        if power and "max" not in power:
            return "extractor_spread_precedence"
        return None
    return None


def build(old_src, new_src, old_dir, new_dir):
    ctx = {"old": old_src, "new": new_src, "field_removed": set(), "const_removed": set(),
           "nested_old": nested_keys(old_src), "nested_new": nested_keys(new_src),
           "fields_old": entity_fields(old_src), "fields_new": entity_fields(new_src),
           "old_docs": {}, "new_docs": {}}
    pairs = []
    for committed, regen in FILES:
        short = committed[:3]
        op, np_ = os.path.join(old_dir, committed), os.path.join(new_dir, committed)
        ctx["old_docs"][short], ctx["new_docs"][short] = json.load(open(op)), json.load(open(np_))
        pairs.append((short, committed, op, np_))
    rows, unclassified = {}, []
    for short, committed, op, np_ in pairs:
        rows[short] = [[list(a), classify(short, a, ctx)] for a in breaking(ctx["old_docs"][short], ctx["new_docs"][short])]
    for short in rows:
        for r in rows[short]:
            if r[1] is None:
                r[1] = classify_late(short, tuple(r[0]), ctx)
            if r[1] is None:
                unclassified.append((short, r[0]))
    files = []
    for short, committed, op, np_ in pairs:
        files.append({"file": "skills/building-tnr-content/data/" + committed,
                      "old_sha256": sha256(op), "new_sha256": sha256(np_),
                      "accepted": [{"atom": a, "class": c} for a, c in rows[short] if c]})
    return files, unclassified


def main():
    a = sys.argv[1:]
    if len(a) != 6 or a[4] not in ("--write", "--check"):
        print(__doc__)
        return 2
    old_src, new_src, old_dir, new_dir, mode, ledger = a
    files, unclassified = build(old_src, new_src, old_dir, new_dir)
    for short, atom in unclassified:
        print("UNCLASSIFIED %s %s" % (short, json.dumps(atom)))
    from collections import Counter
    counts = Counter(r["class"] for f in files for r in f["accepted"])
    doc = {
        "schema": "tnr.schema_adoption_ledger",
        "ruling": "RUL-2026-10-20-001",
        "scope": "One adoption of the generated 45c/45d/45e/45f/45g contracts; each entry is bound "
                 "to the exact OLD and NEW file hashes. Not a waiver: any other file, or any "
                 "other breaking atom, fails schema_diff.py exactly as before.",
        "source": {"old": "studie-tech/TheNinjaRPG@bdec2883", "new": "studie-tech/TheNinjaRPG@6524d0fbd7c0b80ecfd28ca63e9c4becdfb210eb"},
        "regenerate": "python3 scripts/schema_adoption_ledger.py <bdec2883 checkout> <6524d0fb checkout> "
                      "<pre-adoption 45x dir> <adopted 45x dir> --write state/" + os.path.basename(ledger),
        "classes": {k: {"evidence": v, "count": counts.get(k, 0)} for k, v in CLASSES.items()},
        "files": files,
    }
    if unclassified:
        print("%d breaking atom(s) could not be verified - no ledger (exit 1)" % len(unclassified))
        return 1
    text = json.dumps(doc, indent=1, sort_keys=False) + "\n"
    if mode == "--write":
        open(ledger, "w").write(text)
        print("wrote %s: %s" % (ledger, ", ".join("%s %d" % kv for kv in sorted(counts.items()))))
        return 0
    same = os.path.exists(ledger) and open(ledger).read() == text
    print("ledger %s %s" % (ledger, "matches a fresh classification" if same else "DIFFERS from a fresh classification"))
    return 0 if same else 1


if __name__ == "__main__":
    sys.exit(main())
