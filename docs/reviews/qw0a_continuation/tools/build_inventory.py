#!/usr/bin/env python3
"""QW-0A slice A evidence: two-pin extractor correction inventory.

Runs the baseline and the corrected schema_extract.py over two exact game-source
checkouts, then writes an untruncated, source-cited, machine-readable inventory
of every contract fact that differs:

  A  baseline vs corrected extractor at the old pin   (extractor corrections)
  B  baseline vs corrected extractor at the new pin   (extractor corrections)
  C  corrected old pin vs corrected new pin           (actual upstream changes)

It also records commands, exit codes, full-file and structural hashes (the
structural hash drops `_provenance`, whose date/label/source hashes vary by
run), source-file hashes, extractor gaps and the UNCHANGED schema_diff gate's
results for each candidate. Nothing is adopted; candidate 45x files stay in the
scratch directory. Static and local: no network, no game, no source execution.

  python3 build_inventory.py --old-src DIR --old-sha SHA --new-src DIR --new-sha SHA \\
      --baseline OLD_schema_extract.py --corrected schema_extract.py \\
      --stamped skills/building-tnr-content/data --scratch DIR --out FILE.json
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys

MODES = [("ctors", "45c_DATA_constructors"), ("entities", "45d_DATA_entity_schemas"),
         ("constants", "45e_DATA_constants"), ("checks", "45g_DATA_checks")]

CLASSES = {
    "X1_ARRAY_SPREAD": "array spread resolved ([...A, \"x\"] in a constant or z.enum)",
    "X2_MULTILINE": "multi-line field expression or schema head now parsed",
    "X3_HELPER": "helper call inlined (block-bodied msg()/type(), cross-file arrow helper, exact helper extent)",
    "X4_MODULE_SPREAD": "object spread resolved from another module (rewardFields, *.shape, ...)",
    "X5_SPREAD_PRECEDENCE": "JS spread precedence: the later spread or field wins",
    "X6_FALSY_METADATA": "explicit 0 / false / null default or 0 bound no longer dropped",
    "X7_OUTER_CHAIN": "a nested schema's fields/modifiers no longer attributed to the outer field",
    "X8_NUMERIC": "numeric literal with separators/decimals, or a constant-name bound/default resolved",
    "X9_OMISSION": "preprocess unwrapped: inner type, omission mechanism and nullability",
    "X10_ENUM_REF_LABEL": "enum_ref spelling follows where the resolved list is declared",
    "D_DERIVED_45G": "45g block recomputed from the corrected 45c/45d/45e facts",
    "U_UPSTREAM": "actual source change between the two pins (corrected extractor on both)",
}


def sha256(data):
    return hashlib.sha256(data if isinstance(data, bytes) else data.encode()).hexdigest()


def structural(doc):
    doc = {k: v for k, v in doc.items() if k != "_provenance"}
    return json.dumps(doc, sort_keys=True, separators=(",", ":"))


def run(cmd):
    p = subprocess.run(cmd, capture_output=True)
    return p.returncode, p.stdout, p.stderr.decode(errors="replace")


def load_module(path):
    spec = importlib.util.spec_from_file_location("qw0a_corrected_extract", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------- flattening

def facts(kind, doc):
    """{path_tuple: value}. Union-member and entity fields are kept whole when
    added/removed; their keys are compared one by one otherwise."""
    out = {}
    if kind == "ctors":
        for u, variants in doc.get("unions", {}).items():
            for v, spec in variants.items():
                for k, val in spec.items():
                    if k == "fields":
                        for f, rule in val.items():
                            out[("unions", u, v, "fields", f)] = rule
                    else:
                        out[("unions", u, v, k)] = val
    elif kind == "entities":
        for e, spec in doc.get("entities", {}).items():
            for k, val in spec.items():
                if k == "fields":
                    for f, rule in val.items():
                        out[("entities", e, "fields", f)] = rule
                else:
                    out[("entities", e, k)] = val
    elif kind == "constants":
        for c, spec in doc.get("constants", {}).items():
            out[("constants", c)] = spec
        out[("count",)] = doc.get("count")
    else:
        for block, spec in doc.items():
            if block == "_provenance":
                continue
            if isinstance(spec, dict) and isinstance(spec.get("fields"), dict):
                for k, val in spec.items():
                    if k == "fields":
                        for ent, v in val.items():
                            out[(block, "fields", ent)] = v
                    else:
                        out[(block, k)] = val
            else:
                out[(block,)] = spec
    return out


def changes(kind, before, after):
    a, b = facts(kind, before), facts(kind, after)
    rows = []
    for path in sorted(set(a) | set(b), key=lambda t: tuple(map(str, t))):
        va, vb = a.get(path, "<absent>"), b.get(path, "<absent>")
        if va == vb:
            continue
        if va == "<absent>" or vb == "<absent>" or not (isinstance(va, dict) and isinstance(vb, dict)):
            rows.append({"path": list(path), "key": None, "before": va, "after": vb})
            continue
        for k in sorted(set(va) | set(vb)):
            ka, kb = va.get(k, "<absent>"), vb.get(k, "<absent>")
            if ka != kb:
                rows.append({"path": list(path), "key": k, "before": ka, "after": kb})
    return rows


# ------------------------------------------------------------- source context

class Context:
    """Source facts for one pin, read through the corrected extractor's index."""

    def __init__(self, ext, src, sha):
        self.ext, self.src, self.sha = ext, src, sha
        self.index = ext.SourceIndex(src)
        self.member_rel = {}
        for rel in ext.CTOR_FILES:
            mod = self.index.module(rel)
            if mod is None:
                continue
            for name, d in mod.decls.items():
                self.member_rel.setdefault(name, rel)
        self.entities = {label: (rel, name) for label, rel, name in ext.ENTITY_TARGETS}

    def field_line(self, owner, decl_line, field):
        lines = owner.src.splitlines()
        pat = re.compile(r"^\s*%s\s*:" % re.escape(field))
        for i in range(max(0, decl_line - 1), len(lines)):
            if pat.match(lines[i]):
                return i + 1, lines[i]
        return decl_line, ""

    def definitions(self, mod, name, field, seen=()):
        """Every definition of `field` reached while resolving `name`, in JS order."""
        hit = mod.lookup(name)
        if hit is None or (hit[0].rel, hit[1]) in seen:
            return []
        owner, real = hit
        text = owner.decls[real]["text"]
        head = re.match(r"^(?:z\s*\.\s*object\s*\(\s*)?\{", text)
        if not head:
            return []
        i, j = self.ext.balanced(text, head.end() - 1, "{", "}")
        out = []
        for _doc, entry in self.ext.split_entries(text[i + 1:j]):
            if entry.startswith("..."):
                ref = re.fullmatch(r"\.\.\.(\w+)(?:\.shape)?", entry)
                if ref:
                    out += self.definitions(owner, ref.group(1), field, seen + ((owner.rel, real),))
                continue
            f, expr = self.ext.split_field(entry)
            if f and f.strip("\"'") == field:
                out.append((owner, real, expr))
        return out

    def field(self, rel, schema, field):
        mod = self.index.module(rel)
        if mod is None:
            return None
        got = (self.index.object_fields(mod, schema) or {}).get(field)
        if got is None:
            return {"rel": rel, "schema": schema, "defs": []}
        expr, owner, own, _doc, where = got
        decl_name = where.split(" ", 1)[1] if " " in where else schema
        decl_line = owner.decls.get(decl_name, {}).get("line", 1)
        line, text = self.field_line(owner, decl_line, field)
        text = self.ext._strip_comments(text)
        depth = sum(text.count(c) for c in "([{") - sum(text.count(c) for c in ")]}")
        # a field line that does not close with a top-level comma continues below
        multiline = depth > 0 or not text.rstrip().endswith(",")
        expanded, emod, notes = self.index.expand(owner, expr)
        return {"rel": rel, "schema": schema, "owner": owner.rel, "decl": decl_name,
                "line": line, "expr": expr, "expanded": expanded, "helper": notes.get("_helper"),
                "own": own, "multiline": multiline,
                "defs": self.definitions(mod, schema, field)}

    def anchor(self, ctx):
        if not ctx or not ctx.get("owner"):
            return {"sha": self.sha, "file": ctx["rel"] if ctx else None,
                    "declaration": ctx["schema"] if ctx else None, "line": None}
        return {"sha": self.sha, "file": ctx["owner"], "declaration": ctx["decl"], "line": ctx["line"]}

    def const_anchor(self, name, spec):
        rel = spec.get("source") if isinstance(spec, dict) else None
        for cand in ([rel] if rel else []) + [self.ext.CONST_FILE, self.ext.CONST_FILE_COMBAT] + self.ext.LOCAL_ENUM_FILES:
            mod = self.index.module(cand)
            if mod is not None and name in mod.decls:
                return {"sha": self.sha, "file": cand, "declaration": name, "line": mod.decls[name]["line"]}
        return {"sha": self.sha, "file": rel, "declaration": name, "line": None}


def has_spread_list(v):
    return isinstance(v, list) and any(isinstance(x, str) and x.startswith("...") for x in v)


def classify(kind, row, ctx, pin_ctx):
    """Reasons a baseline->corrected fact changed, from the corrected source view."""
    key, before, after = row["key"], row["before"], row["after"]
    path = row["path"]
    reasons = []
    if kind == "checks":
        return ["D_DERIVED_45G"]
    if kind == "constants":
        if has_spread_list(before):
            return ["X1_ARRAY_SPREAD"]
        anchor = pin_ctx.const_anchor(path[-1], {}) if path[0] == "constants" else None
        if anchor and anchor["file"]:
            mod = pin_ctx.index.module(anchor["file"])
            text = mod.decls.get(path[-1], {}).get("text", "") if mod else ""
            if "..." in pin_ctx.ext._strip_comments(text):
                return ["X1_ARRAY_SPREAD"]
        return []
    if path[-2:] and path[-2] != "fields":
        # variant/entity top-level keys
        if kind == "entities" and before == "<absent>":
            return ["X2_MULTILINE"]
        return []
    f = ctx
    if f is None:
        return []
    if key is None:  # whole field added or removed
        if after == "<absent>":
            return ["X7_OUTER_CHAIN"] if not f.get("defs") else ["X5_SPREAD_PRECEDENCE"]
        if f.get("helper"):
            reasons.append("X3_HELPER")
        if f.get("owner") and f["owner"] != f["rel"]:
            reasons.append("X4_MODULE_SPREAD")
        if f.get("multiline"):
            reasons.append("X2_MULTILINE")
        if kind == "entities" and path[1] == "aiRule":
            reasons.append("X2_MULTILINE")
        return reasons
    defs = f.get("defs") or []
    expanded = f.get("expanded") or ""
    nested = "z.object(" in expanded or re.search(r"z\.array\(\s*z\.", expanded)
    if len(defs) > 1 and key in ("default", "min", "max", "optional", "nullable", "type", "enum", "literal", "int"):
        reasons.append("X5_SPREAD_PRECEDENCE")
    if key in ("enum", "enum_ref"):
        if has_spread_list(before) or "..." in expanded or (isinstance(after, list) and before == "<absent>"):
            reasons.append("X1_ARRAY_SPREAD")
        if key == "enum_ref" and isinstance(before, str) and isinstance(after, str) and before.split("@")[0] == after.split("@")[0]:
            reasons.append("X10_ENUM_REF_LABEL")
        if key == "enum_ref" and after == "<absent>" and f.get("helper"):
            reasons.append("X3_HELPER")
    if key in ("raw", "_helper", "coerce", "max_ref", "min_ref") and f.get("helper"):
        reasons.append("X3_HELPER")
    if key in ("_preprocess", "_omission") or (key in ("type", "optional", "raw", "nullable") and before == "preprocess") \
            or (kind == "entities" and key in ("type", "optional", "raw", "coerce", "nullable", "int", "min") and "z.preprocess(" in expanded):
        reasons.append("X9_OMISSION")
    if key in ("max", "min") and f.get("helper") and before == "<absent>":
        reasons.append("X3_HELPER")
    calls = {"max": r"max", "min": r"min", "default": r"(?:prefault|default)"}
    if key in ("default_ref", "max_ref", "min_ref") or (
            key in calls and isinstance(after, (int, float)) and not isinstance(after, bool)
            and re.search(r"\.%s\(\s*(?:[A-Z_]\w*|\d[\d_]*_[\d_]*\d|\d+\.\d+)\s*\)" % calls[key], expanded)):
        reasons.append("X8_NUMERIC")
    if key in ("default", "min") and before == "<absent>" and (after in (0, False, None) and not isinstance(after, list)):
        reasons.append("X6_FALSY_METADATA")
    if f.get("multiline") and key in ("type", "default", "min", "max", "int", "optional", "enum", "enum_ref", "nullable"):
        reasons.append("X2_MULTILINE")
    if nested and key in ("optional", "nullable", "default", "type", "int", "min", "max"):
        reasons.append("X7_OUTER_CHAIN")
    return list(dict.fromkeys(reasons))


def field_ctx(kind, row, ctx, after_doc, before_doc):
    path = row["path"]
    if kind == "ctors" and len(path) == 5:
        spec = after_doc.get("unions", {}).get(path[1], {}).get(path[2]) or \
            before_doc.get("unions", {}).get(path[1], {}).get(path[2]) or {}
        schema = spec.get("schema")
        rel = ctx.member_rel.get(schema)
        return ctx.field(rel, schema, path[4]) if rel else None
    if kind == "entities" and len(path) == 4:
        rel, schema = ctx.entities.get(path[1], (None, None))
        return ctx.field(rel, schema, path[3]) if rel else None
    return None


def anchor_for(kind, row, ctx, fctx, doc):
    if fctx:
        return ctx.anchor(fctx)
    path = row["path"]
    if kind == "constants" and path[0] == "constants":
        spec = doc.get("constants", {}).get(path[1], {})
        return ctx.const_anchor(path[1], spec)
    if kind == "entities":
        rel, schema = ctx.entities.get(path[1], (None, None))
        mod = ctx.index.module(rel) if rel else None
        line = mod.decls.get(schema, {}).get("line") if mod else None
        return {"sha": ctx.sha, "file": rel, "declaration": schema, "line": line}
    if kind == "ctors":
        spec = doc.get("unions", {}).get(path[1], {}).get(path[2], {})
        schema = spec.get("schema")
        rel = ctx.member_rel.get(schema)
        mod = ctx.index.module(rel) if rel else None
        line = mod.decls.get(schema, {}).get("line") if mod else None
        return {"sha": ctx.sha, "file": rel, "declaration": schema, "line": line}
    return {"sha": ctx.sha, "file": None, "declaration": "/".join(map(str, path)), "line": None}


# ------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    for k in ("old-src", "old-sha", "new-src", "new-sha", "baseline", "corrected", "stamped", "scratch", "out"):
        ap.add_argument("--" + k, required=True)
    ap.add_argument("--baseline-label", default="baseline schema_extract.py")
    ap.add_argument("--corrected-label", default="corrected schema_extract.py")
    a = ap.parse_args()
    os.makedirs(a.scratch, exist_ok=True)
    ext = load_module(a.corrected)
    diff_tool = os.path.join(os.path.dirname(os.path.abspath(a.corrected)), "schema_diff.py")
    pins = {"old": (a.old_src, a.old_sha), "new": (a.new_src, a.new_sha)}
    tools = {"baseline": a.baseline, "corrected": a.corrected}

    runs, docs = [], {}
    for pin, (src, sha) in pins.items():
        for tool, path in tools.items():
            for mode, label in MODES:
                cmd = [sys.executable, path, src, "--" + mode]
                code, out, err = run(cmd)
                dest = os.path.join(a.scratch, "%s_%s_%s.json" % (tool, sha[:7], label))
                with open(dest, "wb") as fh:
                    fh.write(out)
                doc = json.loads(out) if code == 0 and out else {}
                docs[(pin, tool, mode)] = doc
                runs.append({"pin": sha, "extractor": tool, "mode": "--" + mode, "exit": code,
                             "command": "python3 <%s> <TheNinjaRPG@%s> --%s > <scratch>/%s_%s_%s.json"
                                        % (tool, sha, mode, tool, sha[:7], label),
                             "stderr": err.strip()[:400], "bytes": len(out),
                             "sha256_full": sha256(out), "sha256_structural": sha256(structural(doc)) if doc else None,
                             "structural_excludes": ["_provenance"]})

    # repeat the corrected run to show identical inputs give identical bytes
    repeat = []
    for pin, (src, sha) in pins.items():
        for mode, _label in MODES:
            outs = [run([sys.executable, a.corrected, src, "--" + mode])[1] for _ in range(2)]
            repeat.append({"pin": sha, "mode": "--" + mode, "identical": outs[0] == outs[1],
                           "sha256_full": sha256(outs[0])})

    gaps = {}
    for pin, (src, sha) in pins.items():
        code, out, err = run([sys.executable, a.corrected, src, "--gaps"])
        gaps[sha] = {"exit": code, "diagnostics": json.loads(out)["diagnostics"] if out else [], "stderr": err[:400]}

    gates = []
    for pin, (src, sha) in pins.items():
        for tool in tools:
            c = os.path.join(a.scratch, "%s_%s_45c_DATA_constructors.json" % (tool, sha[:7]))
            k = os.path.join(a.scratch, "%s_%s_45e_DATA_constants.json" % (tool, sha[:7]))
            code, out, _ = run([sys.executable, diff_tool, "--invariants", c, "--constants", k])
            gates.append({"pin": sha, "extractor": tool, "check": "invariants", "exit": code,
                          "command": "python3 schema_diff.py --invariants <%s 45c> --constants <%s 45e>" % (tool, tool),
                          "result": out.decode().strip().splitlines()[-1], "output": out.decode()})
            for mode, label in MODES[:3]:
                cand = os.path.join(a.scratch, "%s_%s_%s.json" % (tool, sha[:7], label))
                code, out, _ = run([sys.executable, diff_tool, "diff", os.path.join(a.stamped, label + ".json"), cand])
                gates.append({"pin": sha, "extractor": tool, "check": "diff stamped %s" % label, "exit": code,
                              "command": "python3 schema_diff.py diff data/%s.json <%s candidate>" % (label, tool),
                              "result": out.decode().strip().splitlines()[-1], "output": out.decode()})

    contexts = {pin: Context(ext, src, sha) for pin, (src, sha) in pins.items()}
    comparisons = {}
    specs = {"A": ("old", "baseline", "old", "corrected", "extractor correction at the old pin"),
             "B": ("new", "baseline", "new", "corrected", "extractor correction at the new pin"),
             "C": ("old", "corrected", "new", "corrected", "actual upstream change (corrected extractor on both pins)")}
    for cid, (p1, t1, p2, t2, label) in specs.items():
        rows_all, summary = [], {}
        for mode, flabel in MODES:
            before, after = docs[(p1, t1, mode)], docs[(p2, t2, mode)]
            for row in changes(mode, before, after):
                ctx = contexts[p2] if row["after"] != "<absent>" else contexts[p1]
                doc = after if row["after"] != "<absent>" else before
                fctx = field_ctx(mode, row, ctx, after, before)
                if cid == "C":
                    reasons = ["U_UPSTREAM"]
                else:
                    reasons = classify(mode, row, fctx, ctx) or ["UNCLASSIFIED"]
                row = dict(row, file=flabel, classes=reasons, anchor=anchor_for(mode, row, ctx, fctx, doc))
                rows_all.append(row)
                for r in reasons:
                    summary.setdefault(flabel, {}).setdefault(r, 0)
                    summary[flabel][r] += 1
        comparisons[cid] = {"label": label, "before": {"pin": pins[p1][1], "extractor": t1},
                            "after": {"pin": pins[p2][1], "extractor": t2},
                            "changes": len(rows_all), "summary": summary, "rows": rows_all}

    src_hashes = {}
    for pin, ctx in contexts.items():
        files = {}
        for rel, mod in sorted(ctx.index._mods.items()):
            if mod is not None:
                files[rel] = sha256(open(os.path.join(ctx.src, rel), "rb").read())
        for rel in [ext.CONST_FILE, ext.CONST_FILE_COMBAT] + ext.LOCAL_ENUM_FILES + ext.CTOR_FILES:
            p = os.path.join(ctx.src, rel)
            if os.path.exists(p):
                files[rel] = sha256(open(p, "rb").read())
        src_hashes[ctx.sha] = dict(sorted(files.items()))

    inventory = {
        "schema": "tnr.qw0a.extractor_inventory", "version": 1,
        "classes": CLASSES,
        "extractors": {"baseline": {"source": a.baseline_label, "sha256": sha256(open(a.baseline, "rb").read())},
                       "corrected": {"source": a.corrected_label, "sha256": sha256(open(a.corrected, "rb").read())},
                       "schema_diff": {"source": "skills/building-tnr-content/scripts/schema_diff.py (unchanged)",
                                       "sha256": sha256(open(diff_tool, "rb").read())}},
        "pins": {pin: sha for pin, (_src, sha) in pins.items()},
        "source_file_sha256": src_hashes,
        "runs": runs, "repeat_runs": repeat, "gaps": gaps, "gates": gates,
        "metadata_note": ("Full-file hashes include `_provenance` (extraction date, source_drop label and "
                          "16-hex source hashes), which varies with run date and the source path label; "
                          "structural hashes exclude it and use sorted keys. List order is preserved."),
        "comparisons": comparisons,
    }
    with open(a.out, "w") as fh:
        json.dump(inventory, fh, indent=1, sort_keys=False)
        fh.write("\n")
    unclassified = sum(c["summary"].get(f, {}).get("UNCLASSIFIED", 0)
                       for c in comparisons.values() for f in c["summary"])
    for cid, c in comparisons.items():
        print("%s %-60s %5d change(s)" % (cid, c["label"], c["changes"]))
    print("unclassified:", unclassified)
    return 1 if unclassified else 0


if __name__ == "__main__":
    sys.exit(main())
