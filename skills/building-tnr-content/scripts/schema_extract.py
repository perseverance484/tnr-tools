#!/usr/bin/env python3
"""Extract write shapes AND constructors from TNR's zod validators.

Two outputs, one pass:

  45b_DATA_write_shapes.json   field -> {type, optional, enum, default, ...}
                               the original guard table, unchanged in shape

  45c_DATA_constructors.json   every TAGGED UNION member as a complete
                               constructor: the discriminant literal, every
                               field, its prefault default, and its resolved
                               enum values

Why constructors: a hand-authored payload shape is a hallucination surface.
The AI rule shape was documented in file 45 and still got authored wrong from
memory as a flat {action, condition, conditionValue} triple, when the source
is {conditions: Condition[], action: Action} with tagged objects on both
sides. A constructor table lets the builder BUILD the object from an intent
form so the shape is never typed by hand.

Usage:
  python3 schema_extract.py /path/to/TheNinjaRPG-main --shapes  > 45b_DATA_write_shapes.json
  python3 schema_extract.py /path/to/TheNinjaRPG-main --ctors   > 45c_DATA_constructors.json
  python3 schema_extract.py /path/to/TheNinjaRPG-main --report          # human summary
  python3 schema_extract.py /path/to/TheNinjaRPG-main --gaps            # every diagnostic, as JSON

Source fidelity (QW-0A slice A): array spreads ([...A, "x"]) in constants and
z.enum, object spreads ({...A, ...B.shape}) across modules with JS precedence
(the later entry wins), multi-line fields and `z\n.object(` heads, imported
helpers (tsconfig `@/` aliases) and block-bodied helpers such as msg()/type(),
outer-chain modifiers only, explicit 0/false/null facts, and preprocess
omission semantics. An unresolved or cyclic spread is an `error`: the run exits
1 and writes nothing to stdout, so a `>` redirect cannot capture a partial
contract. Forms outside these constructs that lose a field are `gap`
diagnostics, reported by --gaps. Tests: test_schema_extract.py.
"""
import json, re, sys, os

# ---------------------------------------------------------------- inputs

SHAPE_FILES = [
    "app/src/validators/objectives.ts",
    "app/src/validators/rewards.ts",
]

# files scanned for tagged-union constructors
CTOR_FILES = [
    "app/src/validators/ai.ts",
    "app/src/validators/objectives.ts",
    "app/src/validators/combat.ts",
    "app/src/validators/quest.ts",
    "app/src/validators/jutsu.ts",
    "app/src/validators/item.ts",
    "app/src/validators/asset.ts",
    "app/src/validators/bloodline.ts",
]

CONST_FILE = "app/drizzle/constants.ts"
CONST_FILE_COMBAT = "app/src/libs/combat/constants.ts"

KIND = {
    "string": "string", "number": "number", "boolean": "boolean",
    "array": "array", "object": "object", "enum": "enum",
    "union": "union", "literal": "literal", "any": "any", "record": "record",
}

FIELD_RE = re.compile(r"^\s{2,}([A-Za-z_][A-Za-z0-9_]*)\s*:\s*(.+?),?\s*$")
BLOCK_RE = re.compile(r"(?:export )?const (\w+)\s*=\s*\{")
SCHEMA_RE = re.compile(r"export const (\w+)\s*=\s*z\.object\(\{")
SPREAD_RE = re.compile(r"^\s{2,}\.\.\.(\w+)[,)]?\s*$")
UNION_RE = re.compile(r"export const (\w+)\s*=\s*z\.(?:union|discriminatedUnion)\(")
ARRCONST_RE = re.compile(r"(?:export )?const (\w+)\s*=\s*\[")


def parse_expr(expr: str) -> dict:
    """Parse a single zod expression into a rule dict."""
    e = " ".join(expr.split())
    out = {"raw": e}
    m = re.search(r"z\.(?:coerce\.)?(\w+)", e)
    if m:
        out["type"] = KIND.get(m.group(1), m.group(1))
    out["coerce"] = bool(re.match(r"z\s*\.\s*coerce\s*\.", e))
    # modifiers, defaults and bounds belong to the OUTER chain only; a nested
    # item schema's .optional()/.max()/.prefault() says nothing about the field
    calls = _outer_chain(e)
    names = [n for n, _ in calls]
    out["optional"] = "optional" in names or "nullish" in names
    out["nullable"] = "nullable" in names or "nullish" in names
    defaults = [a for n, a in calls if n in ("prefault", "default")]
    if defaults:
        raw = defaults[-1].strip()
        try:
            out["default"] = json.loads(raw.replace("'", '"'))
        except Exception:
            out["default"] = raw.strip("\"'")
    lit = re.search(r"z\.literal\(\s*[\"'](.+?)[\"']\s*\)", e)
    if lit:
        out["literal"] = lit.group(1)
    en = re.search(r"z\.enum\(\[(.*?)\]\)", e)
    if en:
        out["enum"] = [x.strip().strip("\"'") for x in en.group(1).split(",")
                       if x.strip() and "..." not in x]
        sp = re.search(r"z\.enum\(\[\s*\.\.\.(\w+)", e)
        if sp:
            out["enum_ref"] = sp.group(1)
    else:
        ref = re.search(r"z\.enum\((\w+)\)", e)
        if ref:
            out["enum_ref"] = ref.group(1)
    if e.startswith("z.array") or ".array(" in e[:12]:
        out["type"] = "array"
        inner = re.search(r"z\.array\(\s*(\w+)", e)
        if inner and inner.group(1) not in ("z",):
            out["items_ref"] = inner.group(1)
    if "int" in names:
        out["int"] = True
    if "positive" in names:
        out["min"] = 1
    if "nonnegative" in names:
        out["min"] = 0
    for name, arg in calls:
        if name in ("min", "max") and re.fullmatch(r"\s*-?\d[\d_]*(?:\.\d+)?\s*", arg):
            out[name] = _num(arg.strip())
    return out


def _outer_chain(e):
    """[(method, args)] for the calls on the expression's outermost chain:
    `z.coerce.number().int().min(0).prefault(1)` -> number, int, min, prefault.
    Calls inside arguments (a nested item schema) are not part of the chain."""
    calls, depth, i = [], 0, 0
    while i < len(e):
        sk = _skip(e, i)
        if sk is not None:
            i = sk
            continue
        c = e[i]
        if c in "{[(":
            depth += 1
        elif c in "}])":
            depth -= 1
        elif c == "." and depth == 0:
            m = re.match(r"\.\s*([A-Za-z_]\w*)\s*(<[^()]*>)?\s*\(", e[i:])
            if m:
                start = i + m.end() - 1
                _o, close = balanced(e, start, "(", ")")
                calls.append((m.group(1), e[start + 1:close]))
                i = close + 1
                continue
        i += 1
    return calls


def _num(text):
    text = text.replace("_", "")
    return float(text) if "." in text else int(text)


def parse_objects(path: str) -> dict:
    """Every `export const X = z.object({...})` in a file."""
    blocks, cur, depth = {}, None, 0
    lines = _read(path).splitlines(True)
    for line in lines:
        if cur is None:
            m = BLOCK_RE.match(line) or SCHEMA_RE.match(line)
            if m:
                cur, depth = m.group(1), 1
                blocks[cur] = {}
            continue
        depth += line.count("{") - line.count("}")
        if depth <= 0:
            cur = None
            continue
        sp = SPREAD_RE.match(line.rstrip())
        if sp:
            blocks[cur].setdefault("__spreads__", []).append(sp.group(1))
            continue
        fm = FIELD_RE.match(line.rstrip())
        if fm and "z." in fm.group(2):
            blocks[cur][fm.group(1)] = parse_expr(fm.group(2))
        elif fm:
            bare = fm.group(2).rstrip(",").strip()
            cm = re.match(r"([A-Za-z_]\w*)([.(].*)?$", bare)
            if cm:
                # cross-module ref, plain or chained (attackers: idsWithNumberField,
                # opponentAIs: idsWithNumberField.optional()); resolved against
                # REF_FILES in build_constructors, else dropped
                blocks[cur][fm.group(1)] = {"raw": bare, "_bare": True,
                                            "_base": cm.group(1),
                                            "_chain": cm.group(2) or ""}
    # flatten spreads so composed members carry their inherited fields
    for _ in range(4):
        for name, fields in blocks.items():
            for src_name in list(fields.get("__spreads__", [])):
                base = blocks.get(src_name, {})
                for f, r in base.items():
                    if f != "__spreads__":
                        fields.setdefault(f, dict(r, _from=src_name))
    for fields in blocks.values():
        fields.pop("__spreads__", None)
    return blocks


def parse_unions(path: str) -> dict:
    """Every `export const X = z.union([A, B, ...])` -> member names."""
    out, cur, buf, depth = {}, None, "", 0
    src = _read(path)
    for m in UNION_RE.finditer(src):
        name = m.group(1)
        i = src.index("[", m.end() - 1)   # first [ after the call opens
        depth, j = 0, i
        while j < len(src):
            if src[j] == "[":
                depth += 1
            elif src[j] == "]":
                depth -= 1
                if depth == 0:
                    break
            j += 1
        body = src[i + 1:j]
        members = [re.sub(r"\..*$", "", x.strip()) for x in body.split(",")]
        members = [x for x in members if re.match(r"^\w+$", x)]
        members = list(dict.fromkeys(members))
        if members:
            out[name] = members
    return out


REF_FILES = ["app/src/validators/base.ts"]
POST_DOCS = {  # hand-won semantics that ride the generated shape; law-cited, survives regen
    ("idsWithNumberField", "number"):
        "HEADCOUNT in opponentAIs/attackers; DROP CHANCE % in reward arrays. Same shape, opposite meaning.",
}


def parse_ref_schemas(repo: str) -> dict:
    """Exported z.array(z.object({...})) schemas in REF_FILES, inlined as derived
    field shapes so cross-module refs like `attackers: idsWithNumberField` resolve
    instead of vanishing (the gap the 45c `_recovered` blocks documented)."""
    out = {}
    for rel in REF_FILES:
        p = os.path.join(repo, rel)
        if not os.path.exists(p):
            continue
        src = _read(p)
        for m in re.finditer(r"export const (\w+)\s*=\s*z([\s\S]*?)(?=\nexport const |\Z)", src):
            name, body = m.group(1), m.group(2)
            if ".array(" not in body or "z.object({" not in body:
                continue
            item = {}
            inner = body[body.index("z.object({") + len("z.object({"):]
            for line in inner.splitlines():
                if line.strip().startswith("})"):
                    break
                fm = FIELD_RE.match(line)
                if not fm:
                    continue
                r = parse_expr(fm.group(2))
                fs = {"type": r.get("type", "unknown")}
                if r.get("default") is not None:
                    fs["default"] = r["default"]
                if fs["type"] == "array" and "z.array(z.string()" in " ".join(fm.group(2).split()):
                    fs["item"] = "string"
                doc = POST_DOCS.get((name, fm.group(1)))
                if doc:
                    fs["doc"] = doc
                item[fm.group(1)] = fs
            shape = {"type": "array", "_class": "derived",
                     "_source": rel + " -> " + name, "item": item}
            if re.search(r"\)\s*\.prefault\(\s*\[\s*\]\s*\)", body) or ".default([])" in body:
                shape["default"] = []
            out[name] = shape
    return out


_INDEXES = {}


def get_index(repo):
    if repo not in _INDEXES:
        _INDEXES[repo] = SourceIndex(repo)
    return _INDEXES[repo]


def ctor_field_rule(index, owner, expr, where):
    """One union-member field as a parse_expr rule, after helper expansion and
    enum-spread resolution in the module that defines the field."""
    expanded, mod, notes = index.expand(owner, expr)
    if "z." not in expanded:
        cm = re.match(r"([A-Za-z_]\w*)([.(].*)?$", expanded)
        if cm:
            return {"raw": expanded, "_bare": True, "_base": cm.group(1),
                    "_chain": cm.group(2) or "", "_where": where}
        return None
    r = index.resolve_numbers(mod, parse_expr(expanded), expanded)
    r.update(notes)
    members, lead = index.enum_members(mod, expanded, where)
    r["_members"] = members
    r["_enum_ref"] = lead
    r["_label"] = enum_ref_label(index, mod, lead) if lead else None
    return r


def index_objects(index, rel):
    """Every top-level object literal / z.object in `rel`, spreads resolved."""
    mod = index.module(rel)
    out = {}
    if mod is None:
        return out
    for name, d in mod.decls.items():
        if not re.match(r"^(?:z\s*\.\s*object\s*\(\s*)?\{", d["text"]):
            continue
        fields = index.object_fields(mod, name)
        rules = {}
        for f, (expr, owner, own, _doc, fwhere) in (fields or {}).items():
            r = ctor_field_rule(index, owner, expr, "%s field %s" % (fwhere, f))
            if r is not None:
                rules[f] = r
        out[name] = rules
    return out


def build_constructors(repo: str) -> dict:
    index = get_index(repo)
    objects, unions, obj_src = {}, {}, {}
    for rel in CTOR_FILES:
        p = os.path.join(repo, rel)
        if not os.path.exists(p):
            continue
        for k, v in index_objects(index, rel).items():
            if v:
                objects.setdefault(k, {}).update(v)
                obj_src.setdefault(k, rel)
        unions.update(parse_unions(p))
    derived = parse_ref_schemas(repo)

    ctors = {}
    for uname, members in unions.items():
        entries = {}
        for mem in members:
            fields = objects.get(mem)
            if not fields:
                continue
            disc = None
            if (fields.get("type") or {}).get("literal"):
                disc = {"field": "type", "value": fields["type"]["literal"]}
            for f, r in fields.items():
                if disc is None and r.get("literal"):
                    disc = {"field": f, "value": r["literal"]}
                    break
            spec = {"schema": mem, "fields": {}}
            if disc:
                spec["discriminant"] = disc
            for f, r in fields.items():
                base = r.get("_base") or (r.get("raw", "") if re.fullmatch(r"[A-Za-z_]\w*", r.get("raw", "")) else "")
                if base and base in derived:
                    shape = json.loads(json.dumps(derived[base]))
                    chain = r.get("_chain", "")
                    if ".optional()" in chain or ".nullish()" in chain:
                        shape["optional"] = True
                    if ".nullable()" in chain or ".nullish()" in chain:
                        shape["nullable"] = True
                    if re.search(r"\.(?:prefault|default)\(\s*\[\s*\]\s*\)", chain):
                        shape["default"] = []
                    if ".refine(" in chain and re.search(r"length\s*>\s*0", chain):
                        shape["min_items"] = 1
                        shape["_refine"] = "length > 0 (source .refine)" 
                    spec["fields"][f] = shape
                    continue
                if r.get("_bare"):
                    # a schema reference this extractor does not inline: omitted,
                    # but recorded so the loss is visible
                    diag("gap", "G_FIELD_SCHEMA_REF", r.get("_where", mem),
                         "%s.%s = %s is not inlined; the field is absent from 45c"
                         % (uname, f, r.get("raw", "")[:80]))
                    continue
                fs = {"type": r.get("type", "unknown")}
                # absent metadata stays absent; an explicit 0, false or null is a fact
                if "default" in r:
                    fs["default"] = r["default"]
                for k in ("literal", "min", "max"):
                    if r.get(k) is not None:
                        fs[k] = r[k]
                for k in ("int", "optional", "nullable"):
                    if r.get(k) is True:
                        fs[k] = True
                members, ref = r.get("_members"), r.get("_enum_ref")
                if ref:
                    if r.get("_label"):
                        fs["enum_ref"] = r["_label"]
                    if members is not None:
                        fs["enum"] = sorted(set(members))
                elif members is not None:
                    fs["enum"] = list(dict.fromkeys(members))
                spec["fields"][f] = fs
            key = disc["value"] if disc else mem
            entries[key] = spec
        if entries:
            ctors[uname] = entries

    return {"unions": ctors,
            "objects": {k: {f: r for f, r in v.items() if not r.get("_bare")}
                        for k, v in objects.items()}}


def emit_shapes(repo: str) -> dict:
    all_blocks = {}
    for rel in SHAPE_FILES:
        p = os.path.join(repo, rel)
        if not os.path.exists(p):
            continue
        for name, fields in parse_objects(p).items():
            if fields:
                all_blocks.setdefault(name, {}).update(fields)
    booleans, enums, optional_no_null, arrays, numbers = [], {}, [], [], []
    for block, fields in all_blocks.items():
        for f, r in fields.items():
            t = r.get("type")
            if t == "boolean" and f not in booleans:
                booleans.append(f)
            if (r.get("enum") or r.get("enum_ref")) and f not in enums:
                enums[f] = r.get("enum") or {"ref": r["enum_ref"]}
            if r.get("optional") and not r.get("nullable") and f not in optional_no_null:
                optional_no_null.append(f)
            if t == "array" and f not in arrays:
                arrays.append(f)
            if t == "number" and f not in numbers:
                numbers.append(f)
    return {
        "_generated_from": SHAPE_FILES,
        "_guards": {
            "booleans": sorted(booleans),
            "optional_omit_when_null": sorted(optional_no_null),
            "arrays": sorted(arrays),
            "numbers": sorted(numbers),
            "enums": {k: v for k, v in sorted(enums.items())},
        },
        "blocks": all_blocks,
    }


def emit_ctors(repo: str) -> dict:
    c = build_constructors(repo)
    ai = c["unions"]
    # union members are complete under `unions`; keeping a second copy in
    # `objects` tripled the file for no addressable gain
    members = {m["schema"] for u in ai.values() for m in u.values()}
    c["objects"] = {k: v for k, v in c["objects"].items()
                    if k not in members and any(t in k for t in
                    ("Objective", "Quest", "Reward", "Attributes", "Stats"))}
    return {
        "_generated_from": CTOR_FILES + [CONST_FILE],
        "_contract": {
            "purpose": "Build payload objects from these; never hand-author a tagged shape.",
            "usage": ("Pick the union, pick the member by its discriminant value, emit every field. "
                      "Fields carrying `default` may be omitted but emitting them is safer, since "
                      "prefault strings (descriptions) are what a human would otherwise invent."),
            "scope": ("Unions only. Enum values are inlined per field, which is the only place any "
                      "consumer (70_TOOL_validate.py ctor checks, builder ctorBad) reads them; the old "
                      "top-level enums/objects blocks had no consumer and are no longer emitted."),
        },
        "unions": ai,
    }


def report(repo: str):
    c = emit_ctors(repo)
    print("unions found: %d" % len(c["unions"]))
    for u, members in sorted(c["unions"].items()):
        print("\n  %s  (%d members)" % (u, len(members)))
        for k, spec in sorted(members.items()):
            fields = ", ".join(sorted(spec["fields"]))
            print("    %-34s %s" % (k, fields[:96]))
    total = sum(len(m) for m in c["unions"].values())
    print("\nunion members total: %d" % total)




# ==================================================================== v2
# Phase 1 additions: balanced-expression parsing, entity schemas,
# constants, procedures, provenance. Everything above this line is v1
# and is preserved so 45c regeneration stays byte-comparable.

VERSION = "2.0"

ENTITY_TARGETS = [
    ("jutsu",      "app/src/validators/combat.ts",     "JutsuValidatorRawSchema"),
    ("item",       "app/src/validators/combat.ts",     "ItemValidatorRawSchema"),
    ("bloodline",  "app/src/validators/combat.ts",     "BloodlineValidator"),
    ("quest",      "app/src/validators/objectives.ts", "QuestValidatorRawSchema"),
    ("gameAsset",  "app/src/validators/asset.ts",      "gameAssetValidator"),
    ("aiRule",     "app/src/validators/ai.ts",         "AiRule"),
]

ROUTER_DIR = "app/src/server/api/routers"


def _skip(src, i):
    """Advance past a string or comment starting at i. Returns new i or None."""
    c = src[i]
    if c in "\"'`":
        j = i + 1
        while j < len(src):
            if src[j] == "\\":
                j += 2
                continue
            if src[j] == c:
                return j + 1
            j += 1
        return len(src)
    if src.startswith("//", i):
        j = src.find("\n", i)
        return len(src) if j < 0 else j
    if src.startswith("/*", i):
        j = src.find("*/", i)
        return len(src) if j < 0 else j + 2
    return None


def balanced(src, i, opener="{", closer="}"):
    """Index of the matching closer for the opener at/after i. Strings and
    comments do not count toward depth."""
    while i < len(src) and src[i] != opener:
        i += 1
    depth, j = 0, i
    while j < len(src):
        s = _skip(src, j)
        if s is not None:
            j = s
            continue
        if src[j] == opener:
            depth += 1
        elif src[j] == closer:
            depth -= 1
            if depth == 0:
                return i, j
        j += 1
    return i, len(src)


def split_entries(body):
    """Split an object body on top-level commas. Returns [(doc, text)]."""
    out, depth, start, i = [], 0, 0, 0
    while i < len(body):
        s = _skip(body, i)
        if s is not None:
            i = s
            continue
        c = body[i]
        if c in "{[(":
            depth += 1
        elif c in "}])":
            depth -= 1
        elif c == "," and depth == 0:
            out.append(body[start:i])
            start = i + 1
        i += 1
    if body[start:].strip():
        out.append(body[start:])
    res = []
    for chunk in out:
        doc = " ".join(
            re.sub(r"^\s*[/*]+\s?|\s*\*/\s*$", "", ln).strip()
            for ln in re.findall(r"^\s*(?://.*|/\*.*?\*/|\*.*)$", chunk, re.M | re.S)
        ).strip()
        text = re.sub(r"/\*.*?\*/", " ", chunk, flags=re.S)
        text = re.sub(r"^\s*//.*$", "", text, flags=re.M)
        res.append((doc, normalize_expr(" ".join(text.split()))))
    return res


def normalize_expr(text):
    """Collapse whitespace around method dots so a multi-line zod chain reads
    like a single-line one. String literals are copied verbatim."""
    out, i = [], 0
    while i < len(text):
        sk = _skip(text, i)
        if sk is not None:
            out.append(text[i:sk])
            i = sk
            continue
        out.append(text[i])
        i += 1
    joined = "".join(out)
    parts, i = [], 0
    while i < len(joined):
        sk = _skip(joined, i)
        if sk is not None:
            parts.append(joined[i:sk])
            i = sk
            continue
        j = i
        while j < len(joined) and _skip(joined, j) is None:
            j += 1
        seg = joined[i:j]
        seg = re.sub(r"\s*\.\s*(?=[A-Za-z_])", ".", seg)
        parts.append(seg)
        i = j
    return "".join(parts)


def split_field(text):
    """`name: expr` -> (name, expr) splitting at the first top-level colon."""
    depth, i = 0, 0
    while i < len(text):
        s = _skip(text, i)
        if s is not None:
            i = s
            continue
        c = text[i]
        if c in "{[(":
            depth += 1
        elif c in "}])":
            depth -= 1
        elif c == ":" and depth == 0:
            return text[:i].strip(), text[i + 1:].strip()
        i += 1
    return None, None


def parse_expr2(expr, helpers=None, consts=None):
    """parse_expr plus helper-call resolution, preprocess unwrapping, and
    constant-name bound resolution."""
    helpers, consts = helpers or {}, consts or {}
    note = {}
    m = re.match(r"^(\w+)\((.*)\)$", expr)
    if m and m.group(1) in helpers:
        params, body = helpers[m.group(1)]
        args = [a.strip() for a in split_top_args(m.group(2))]
        for p, a in zip(params, args):
            body = re.sub(r"\b%s\b" % re.escape(p), a, body)
        note["_helper"] = m.group(1)
        expr = body
    pp = re.match(r"^z\.preprocess\((.*)\)$", expr)
    if pp:
        args = [a for a in split_top_args(pp.group(1)) if a.strip()]
        if len(args) == 2:
            # the inner schema states what the field accepts; the preprocess step
            # is recorded as the mechanism, not as the type
            note["_preprocess"] = True
            expr = args[1].strip()
    out = parse_expr(expr)
    out.update(note)
    outer = _outer_chain(" ".join(expr.split()))
    for name in ("min", "max"):
        if name not in out:
            for call, arg in outer:
                b = re.fullmatch(r"\s*([A-Z][A-Z0-9_]*)\s*", arg) if call == name else None
                if b:
                    ref = b.group(1)
                    out[name + "_ref"] = ref
                    if isinstance(consts.get(ref), (int, float)):
                        out[name] = consts[ref]
    if "nullish" in [n for n, _ in _outer_chain(" ".join(expr.split()))]:
        out["optional"] = out["nullable"] = True
    if ".transform(" in expr:
        out["_transform"] = True
    sr = re.search(r"\.superRefine\((\w+)\)", expr)
    if sr:
        out["_superRefine"] = sr.group(1)
    arr = re.search(r"z\.array\(\s*(\w+)", expr)
    if arr and arr.group(1) != "z":
        out["type"] = "array"
        out["items_ref"] = arr.group(1)
    out["raw"] = expr[:240]
    return out


def split_top_args(s):
    out, depth, start, i = [], 0, 0, 0
    while i < len(s):
        sk = _skip(s, i)
        if sk is not None:
            i = sk
            continue
        c = s[i]
        if c in "{[(":
            depth += 1
        elif c in "}])":
            depth -= 1
        elif c == "," and depth == 0:
            out.append(s[start:i])
            start = i + 1
        i += 1
    out.append(s[start:])
    return out


def _find_assign(src, i):
    """Index of the `=` that opens a top-level assignment, skipping any TS
    type annotation (which may carry <>, {}, () and newlines)."""
    depth = 0
    while i < len(src):
        sk = _skip(src, i)
        if sk is not None:
            i = sk
            continue
        c = src[i]
        if c in "<{[(":
            depth += 1
        elif c in ">}])":
            if c == ">" and src[i - 1:i] == "=":
                pass
            else:
                depth -= 1
        elif c == "=" and depth <= 0:
            if src[i + 1:i + 2] == ">" or src[i - 1:i] in "=!<>":
                i += 1
                continue
            return i
        elif c == ";" and depth <= 0:
            return None
        i += 1
    return None


# ------------------------------------------------------- source index
# QW-0A slice A. One static, local view of the validator modules: imports,
# top-level declarations with their exact extent, arrow helpers, and
# transitive resolution of array spreads ([...A, "x"]) and object spreads
# ({...A, ...B.shape, f: ...}). Nothing is executed. An unresolved or cyclic
# reference inside these supported constructs is an `error` diagnostic and
# makes the extraction exit nonzero; a source form outside them that loses a
# field is recorded as a `gap` so the loss is visible instead of silent.

DIAGNOSTICS = []

# Every source file this process reads, by absolute path; `--reads` reports them
# repository-relative so evidence can hash the complete read-set.
SOURCE_READS = set()


def _read(path, binary=False):
    SOURCE_READS.add(os.path.abspath(path))
    with open(path, "rb" if binary else "r") as fh:
        return fh.read()

# tsconfig "paths" aliases used by the validator modules (identical at
# bdec2883 and 585534d7: app/tsconfig.json).
ALIASES = [("@/drizzle/", "app/drizzle/"), ("@/validators/", "app/src/validators/"),
           ("@/libs/", "app/src/libs/"), ("@/utils/", "app/src/utils/"),
           ("@/server/", "app/src/server/"), ("@/data/", "app/src/data/")]


def diag(severity, code, where, detail):
    entry = {"severity": severity, "code": code, "where": where, "detail": detail}
    if entry not in DIAGNOSTICS:
        DIAGNOSTICS.append(entry)


def diagnostics_errors():
    return [d for d in DIAGNOSTICS if d["severity"] == "error"]


def _strip_comments(text):
    out, i = [], 0
    while i < len(text):
        if text.startswith("//", i):
            j = text.find("\n", i)
            i = len(text) if j < 0 else j
            continue
        if text.startswith("/*", i):
            j = text.find("*/", i)
            i = len(text) if j < 0 else j + 2
            out.append(" ")
            continue
        sk = _skip(text, i)
        if sk is not None:
            out.append(text[i:sk])
            i = sk
            continue
        out.append(text[i])
        i += 1
    return "".join(out)


def _statement_end(src, i):
    """End index (exclusive) of the expression that starts at i: the first
    top-level `;`, or a top-level newline followed by a new declaration."""
    depth, j = 0, i
    while j < len(src):
        sk = _skip(src, j)
        if sk is not None:
            j = sk
            continue
        c = src[j]
        if c in "{[(":
            depth += 1
        elif c in "}])":
            depth -= 1
        elif depth <= 0 and c == ";":
            return j
        elif depth <= 0 and c == "\n" and re.match(
                r"\n(?:export\s|const\s|let\s|function\s|type\s|interface\s|import\s)", src[j:j + 12]):
            return j
        j += 1
    return len(src)


class Module:
    def __init__(self, index, rel, src):
        self.index, self.rel, self.src = index, rel, src
        self.imports = {}
        for m in re.finditer(r"import\s+(type\s+)?\{([^}]*)\}\s*from\s*[\"']([^\"']+)[\"']", src):
            if m.group(1):
                continue
            target = index.resolve_path(m.group(3))
            for item in m.group(2).split(","):
                item = item.strip()
                if not item or item.startswith("type "):
                    continue
                parts = re.split(r"\s+as\s+", item)
                self.imports[parts[-1].strip()] = (target, parts[0].strip())
        self.decls = {}
        for m in re.finditer(r"^(?:export\s+)?const\s+(\w+)\b", src, re.M):
            eq = _find_assign(src, m.end())
            if eq is None:
                continue
            start = eq + 1
            while start < len(src) and src[start].isspace():
                start += 1
            end = _statement_end(src, start)
            text = src[start:end].strip()
            text = re.sub(r"\s+as\s+const\s*$", "", text)
            line = src.count("\n", 0, m.start()) + 1
            self.decls.setdefault(m.group(1), {"text": text, "line": line})

    def where(self, name):
        d = self.decls.get(name)
        return "%s:%s" % (self.rel, d["line"] if d else "?")

    def lookup(self, name):
        """(module, name) that defines `name` as seen from this module, or None."""
        if name in self.decls:
            return self, name
        if name in self.imports:
            target, orig = self.imports[name]
            mod = self.index.module(target) if target else None
            if mod is not None:
                return mod.lookup(orig)
        return None


class SourceIndex:
    def __init__(self, repo):
        self.repo, self._mods = repo, {}

    def resolve_path(self, spec):
        for alias, real in ALIASES:
            if spec.startswith(alias):
                return real + spec[len(alias):] + ".ts"
        return None

    def module(self, rel):
        if rel not in self._mods:
            p = os.path.join(self.repo, rel) if rel else None
            self._mods[rel] = Module(self, rel, _read(p)) if p and os.path.exists(p) else None
        return self._mods[rel]

    # ---- arrays: [...A, "x", ...B]
    def list_values(self, mod, name, stack=()):
        """Resolved member list for const `name` seen from `mod`, or None when the
        declaration is not a static string list. Order is source order."""
        hit = mod.lookup(name)
        if hit is None:
            return None
        owner, real = hit
        key = (owner.rel, real)
        if key in stack:
            diag("error", "E_CYCLE", owner.where(real),
                 "cyclic array spread: " + " -> ".join("%s:%s" % k for k in stack + (key,)))
            return []
        text = _strip_comments(owner.decls[real]["text"]).strip()
        if not text.startswith("["):
            return None
        i, j = balanced(text, 0, "[", "]")
        return self.list_items(owner, text[i + 1:j], owner.where(real), stack + (key,))

    def list_items(self, mod, body, where, stack=()):
        vals = []
        for item in split_top_args(_strip_comments(body)):
            item = item.strip()
            if not item:
                continue
            if item.startswith("..."):
                ref = item[3:].strip()
                got = self.list_values(mod, ref, stack) if re.fullmatch(r"\w+", ref) else None
                if got is None:
                    diag("error", "E_UNRESOLVED_SPREAD", where,
                         "array spread ...%s does not resolve to a static string list" % ref)
                    continue
                vals.extend(got)
            elif re.fullmatch(r"\"[^\"]*\"|'[^']*'", item):
                vals.append(item[1:-1])
            else:
                return None
        return vals

    def number_value(self, mod, name):
        hit = mod.lookup(name)
        if hit is None:
            return None
        owner, real = hit
        text = _strip_comments(owner.decls[real]["text"]).strip()
        if re.fullmatch(r"-?\d[\d_]*(?:\.\d+)?", text):
            return _num(text)
        return None

    def resolve_numbers(self, mod, rule, expr):
        """Constant-name bounds/defaults (`.max(MAX_X)`, `.prefault(DEFAULT_X)`) as
        numbers, keeping the name in <key>_ref."""
        outer = _outer_chain(" ".join(expr.split()))
        for key in ("min", "max"):
            if rule.get(key) is None:
                for call, arg in outer:
                    b = re.fullmatch(r"\s*([A-Za-z_]\w*)\s*", arg) if call == key else None
                    if b:
                        v = self.number_value(mod, b.group(1))
                        if v is not None:
                            rule[key] = v
                            rule[key + "_ref"] = b.group(1)
        d = rule.get("default")
        if isinstance(d, str) and re.fullmatch(r"[A-Za-z_]\w*", d) and \
                any(call in ("prefault", "default") and arg.strip() == d for call, arg in outer):
            v = self.number_value(mod, d)
            if v is not None:
                rule["default"] = v
                rule["default_ref"] = d
        return rule

    # ---- objects: {...A, ...B.shape, f: expr}
    def object_fields(self, mod, name, stack=()):
        """Ordered {field: (expr, defining_module, own, doc, "file:line Decl")} for an object literal or
        z.object({...}) declaration, with JS spread precedence (later wins)."""
        hit = mod.lookup(name)
        if hit is None:
            return None
        owner, real = hit
        key = (owner.rel, real)
        if key in stack:
            diag("error", "E_CYCLE", owner.where(real),
                 "cyclic object spread: " + " -> ".join("%s:%s" % k for k in stack + (key,)))
            return {}
        text = owner.decls[real]["text"]
        head = re.match(r"^(?:z\s*\.\s*object\s*\(\s*)?\{", text)
        if not head:
            return None
        i, j = balanced(text, head.end() - 1, "{", "}")
        return self.object_body(owner, text[i + 1:j], "%s %s" % (owner.where(real), real), stack + (key,))

    def object_body(self, mod, body, where, stack=()):
        result = {}
        for _doc, entry in split_entries(body):
            if entry.startswith("..."):
                ref = re.fullmatch(r"\.\.\.(\w+)(?:\.shape)?", entry)
                got = self.object_fields(mod, ref.group(1), stack) if ref else None
                if got is None:
                    diag("error", "E_UNRESOLVED_SPREAD", where,
                         "object spread %s does not resolve to an object literal or z.object" % entry)
                    continue
                for f, (expr, owner, _own, doc, fwhere) in got.items():
                    result.pop(f, None)
                    result[f] = (expr, owner, False, doc, fwhere)
                continue
            f, expr = split_field(entry)
            if not f or not expr:
                continue
            f = f.strip("\"'")
            result.pop(f, None)
            result[f] = (expr, mod, True, _doc, where)
        own = [f for f, v in result.items() if v[2]]
        return {f: result[f] for f in own + [f for f in result if f not in own]}

    # ---- helpers: const f = (a) => z...   |   const f = (a) => { return z...; }
    def helper(self, mod, name):
        hit = mod.lookup(name)
        if hit is None:
            return None
        owner, real = hit
        text = owner.decls[real]["text"]
        m = re.match(r"^\(([^)]*)\)\s*(?::[^=]*)?=>\s*", text)
        if not m:
            return None
        body = text[m.end():].strip()
        if body.startswith("{"):
            r = re.match(r"^\{\s*return\s+([\s\S]*?);?\s*\}$", body)
            if not r:
                return None
            body = r.group(1)
        body = normalize_expr(" ".join(_strip_comments(body).split()))
        if not body.startswith("z."):
            return None
        params = [p.split(":")[0].strip() for p in m.group(1).split(",") if p.strip()]
        return owner, params, body

    def expand(self, mod, expr, depth=0):
        """Inline a top-level helper call (`msg("x")`, `makeCapped(N).nullish()`)
        and resolve enum spreads, in the defining module's context. Returns
        (expr, module, notes)."""
        notes = {}
        m = re.match(r"^(\w+)\(", expr)
        if m and depth < 4:
            i, j = balanced(expr, m.end() - 1, "(", ")")
            got = self.helper(mod, m.group(1))
            if got is not None:
                owner, params, body = got
                args = [a.strip() for a in split_top_args(expr[i + 1:j])]
                for p, a in zip(params, args):
                    # identifiers only: `max` the parameter, never `.max(` the method
                    body = re.sub(r"(?<![.\w$])%s(?![\w$])" % re.escape(p), lambda _m, a=a: a, body)
                notes["_helper"] = m.group(1)
                inner, mod2, more = self.expand(owner, body + expr[j + 1:], depth + 1)
                more.update(notes)
                return inner, mod2, more
        return expr, mod, notes

    def enum_members(self, mod, expr, where):
        """Resolved members of the first z.enum(...) in expr: (members, lead_ref)
        or (None, None) when there is no z.enum or it is not static."""
        m = re.search(r"z\.enum\(\s*", expr)
        if not m:
            return None, None
        rest = expr[m.end():]
        if rest.startswith("["):
            i, j = balanced(rest, 0, "[", "]")
            body = rest[i + 1:j]
            lead = re.match(r"\s*\.\.\.(\w+)", body)
            vals = self.list_items(mod, body, where)
            return vals, lead.group(1) if lead else None
        ref = re.match(r"(\w+)\s*\)", rest)
        if ref:
            vals = self.list_values(mod, ref.group(1))
            if vals is None and mod.lookup(ref.group(1)) is None:
                diag("gap", "G_ENUM_REF_UNRESOLVED", where,
                     "z.enum(%s): no static declaration found" % ref.group(1))
            return vals, ref.group(1)
        return None, None


def enum_ref_label(index, mod, ref):
    """45c/45d enum_ref spelling: bare for a constants-module or non-static
    name (as v1 emitted it), 'Name@validators/x.ts' for a static list local to
    a validator file 45e folds in, None for a static list 45e does not carry."""
    hit = mod.lookup(ref)
    if hit is None:
        return ref
    owner, real = hit
    if owner.rel in (CONST_FILE, CONST_FILE_COMBAT):
        return real
    if index.list_values(owner, real) is None:
        return real
    if owner.rel in LOCAL_ENUM_FILES:
        return real + "@" + owner.rel.replace("app/src/", "")
    return None


_EQ_ATOM = re.compile(r"^(?:(?P<a>\w+)\s*(?P<op>===|==)\s*(?P<lit>undefined|null|\"\"|'')"
                      r"|(?P<lit2>undefined|null|\"\"|'')\s*(?P<op2>===|==)\s*(?P<a2>\w+))$")


def _strip_wrapping_parens(text):
    text = text.strip()
    while text.startswith("(") and balanced(text, 0, "(", ")")[1] == len(text) - 1:
        text = text[1:-1].strip()
    return text


def preprocess_omission(expr):
    """Omission semantics of a top-level z.preprocess(fn, inner).

    Returns (omit, mechanism, via):
      (True, why, "null")            undefined becomes null and the inner schema
                                     accepts null: omission yields null
      (True, why, "inner_optional")  undefined passes through to an inner
                                     .optional()/.nullish()
      (True, why, "inner_default")   undefined passes through to an inner
                                     .default()/.prefault(), which supplies the value
      (False, why, None)             omission is proven rejected
      (None, reason, None)           callback outside the bounded forms below
      (None, None, None)             not a top-level preprocess

    Recognised callback: `(v) => (A1 || A2 ... ? null : v)` where every atom is
    an exact equality of the parameter with undefined, null or "" (`===` or
    loose `==`, either operand order). No negation, `&&`, nesting or other
    operands. `v == null` and `v == undefined` are true for undefined; strict
    `v === null` and `v === ""` are not. The inner schema's acceptance is read
    from its OUTER chain, never from a nested schema. An inner optional/default
    only ever sees undefined, so it cannot rescue a callback that turns
    undefined into null."""
    pp = re.match(r"^z\.preprocess\((.*)\)$", expr)
    if not pp:
        return None, None, None
    args = [a for a in split_top_args(pp.group(1)) if a.strip()]
    if len(args) != 2:
        return None, "preprocess with %d arguments" % len(args), None
    fn, inner = " ".join(args[0].split()), " ".join(args[1].split())
    head = re.match(r"^\(?\s*(\w+)\s*(?::[^)]*)?\)?\s*=>\s*", fn)
    if not head:
        return None, "preprocess callback is not a one-parameter arrow function", None
    param = head.group(1)
    body = _strip_wrapping_parens(fn[head.end():])
    tern = re.fullmatch(r"([^?]*)\?\s*null\s*:\s*%s" % re.escape(param), body)
    if not tern:
        return None, "preprocess callback is not `COND ? null : %s`" % param, None
    cond = tern.group(1).strip()
    if re.search(r"&&|!|\(|\)", cond):
        return None, "preprocess condition uses an operator outside the bounded || of equalities", None
    maps_undefined = False
    for atom in cond.split("||"):
        m = _EQ_ATOM.fullmatch(atom.strip())
        if not m or (m.group("a") or m.group("a2")) != param:
            return None, "preprocess condition atom %r is not an equality of %s" % (atom.strip(), param), None
        op, lit = (m.group("op") or m.group("op2")), (m.group("lit") or m.group("lit2"))
        if lit == "undefined" or (lit == "null" and op == "=="):
            maps_undefined = True
    names = [n for n, _ in _outer_chain(inner)]
    if maps_undefined:
        if "nullable" in names or "nullish" in names:
            return True, "preprocess maps undefined to null and the inner schema is nullable", "null"
        return False, ("preprocess maps undefined to null but the inner schema is not nullable "
                       "(an inner optional/default applies to undefined only)"), None
    if "optional" in names or "nullish" in names:
        return True, "preprocess passes undefined through and the inner schema is optional/nullish", "inner_optional"
    if "default" in names or "prefault" in names:
        return True, "preprocess passes undefined through to the inner schema's default", "inner_default"
    return False, "preprocess passes undefined through and the inner schema neither accepts nor defaults it", None


def apply_preprocess_omission(spec, omit, why, via):
    """Make the outer field's emitted facts agree with the omission result.

    parse_expr2 copied the inner schema's facts; an inner optional/default is
    only true of the outer field when undefined actually reaches it. A default
    that omission cannot reach moves to `_inner_default` (fact kept, claim dropped)."""
    def demote_default():
        if "default" in spec:
            spec["_inner_default"] = spec.pop("default")
        if "default_ref" in spec:
            spec["_inner_default_ref"] = spec.pop("default_ref")
    if omit is True:
        spec["_omission"] = why
        if via == "null":
            spec["optional"] = True
            demote_default()          # omission yields null, never the inner default
        elif via == "inner_optional":
            spec["optional"] = True
        # via == "inner_default": the default is the omission fallback; keep it
    else:
        # proven rejected, or unclassified (conservative): never advertise omission
        spec["optional"] = False
        demote_default()


# ------------------------------------------------------------- constants

def extract_constants(repo, rel=None):
    rel = rel or CONST_FILE
    path = os.path.join(repo, rel)
    src = _read(path)
    out, order = {}, 0
    for m in re.finditer(r"^export const (\w+)\b", src, re.M):
        name = m.group(1)
        eq = _find_assign(src, m.end())
        if eq is None:
            continue
        ann = src[m.end():eq].strip().lstrip(":").strip()
        head = src[:m.start()]
        doc = ""
        tail = head.rstrip()
        if tail.endswith("*/"):
            k = tail.rfind("/**")
            if k < 0:
                k = tail.rfind("/*")
            if k >= 0:
                doc = " ".join(
                    re.sub(r"^\s*\*+\s?", "", ln).strip()
                    for ln in tail[k:].splitlines()
                ).strip("/*  ").strip()
        else:
            lines = tail.splitlines()
            buf = []
            for ln in reversed(lines):
                if ln.strip().startswith("//"):
                    buf.append(ln.strip()[2:].strip())
                else:
                    break
            doc = " ".join(reversed(buf))
        rest = src[eq + 1:]
        if rest.lstrip().startswith("["):
            i, j = balanced(rest, 0, "[", "]")
            raw = rest[i:j + 1]
        elif rest.lstrip().startswith("{"):
            i, j = balanced(rest, 0, "{", "}")
            raw = rest[i:j + 1]
        else:
            k = rest.find(";")
            raw = rest[:k if k > 0 else 200]
        raw = raw.replace(" as const", "").strip().rstrip(";").strip()
        entry = {"raw": raw[:4000], "order": order}
        if len(raw) > 4000:
            entry["truncated"] = True
        order += 1
        if ann:
            entry["ts_type"] = " ".join(ann.split())[:200]
        if doc:
            entry["doc"] = doc[:400]
        num = re.match(r"^-?[\d_]+(\.\d+)?$", raw)
        if num:
            entry["value"] = float(raw.replace("_", "")) if "." in raw else int(raw.replace("_", ""))
            entry["kind"] = "number"
        elif re.match(r'^["\'].*["\']$', raw):
            entry["value"] = raw[1:-1]
            entry["kind"] = "string"
        elif raw in ("true", "false"):
            entry["value"] = raw == "true"
            entry["kind"] = "boolean"
        elif raw.startswith("[") and "..." in _strip_comments(raw):
            index = get_index(repo)
            mod = index.module(rel)
            vals = index.list_values(mod, name) if mod is not None else None
            if vals is None:
                diag("error", "E_UNRESOLVED_SPREAD", "%s:%s" % (rel, name),
                     "list constant with spreads is not a static string list")
                entry["kind"] = "array_expr"
            else:
                entry["value"] = vals
                entry["kind"] = "list"
        elif raw.startswith("["):
            inner = raw[1:-1]
            if "{" not in inner and "(" not in inner:
                vals = [v.strip().strip("\"'") for v in split_top_args(inner) if v.strip()]
                if vals:
                    entry["value"] = vals
                    entry["kind"] = "list"
            entry.setdefault("kind", "array_expr")
        else:
            entry["kind"] = "expr"
        out[name] = entry
    # second pass: resolve numeric aliases (X = Y) and simple arithmetic
    for _ in range(3):
        for name, e in out.items():
            if e["kind"] != "expr":
                continue
            r = e["raw"]
            if r in out and out[r].get("kind") == "number":
                e["value"], e["kind"], e["alias_of"] = out[r]["value"], "number", r
            elif re.match(r"^[\w\s*/+\-().]+$", r) and re.search(r"[A-Z_]{2,}", r):
                expr = r
                for ref in sorted(set(re.findall(r"[A-Z][A-Z0-9_]+", r)), key=len, reverse=True):
                    v = out.get(ref, {}).get("value")
                    if isinstance(v, (int, float)):
                        expr = expr.replace(ref, str(v))
                if re.match(r"^[\d\s*/+\-().]+$", expr):
                    try:
                        e["value"] = eval(expr)  # numeric literals only
                        e["kind"] = "number"
                        e["derived_from"] = r
                    except Exception:
                        pass
    return out


def const_values(consts):
    return {k: v["value"] for k, v in consts.items() if "value" in v}


# ---------------------------------------------------------- entity schemas

def extract_entity(repo, rel, name, consts):
    index = get_index(repo)
    mod = index.module(rel)
    if mod is None:
        return None
    src = mod.src
    if name not in mod.decls or not re.match(r"^z\s*\.\s*object\s*\(", mod.decls[name]["text"]):
        return None
    cvals = const_values(consts)
    fields = {}
    for f, (expr, owner, _own, doc, fwhere) in (index.object_fields(mod, name) or {}).items():
        where = "%s field %s" % (fwhere, f)
        bare = re.match(r"^([A-Z]\w+)$", expr)
        if bare:
            spec = {"type": "object", "schema_ref": bare.group(1), "raw": expr}
        elif "z." in expr or re.match(r"^\w+\(", expr):
            expanded, emod, notes = index.expand(owner, expr)
            if "z." not in expanded:
                diag("gap", "G_FIELD_UNRESOLVED_CALL", where,
                     "%s.%s = %s is not a resolvable helper; recorded raw" % (name, f, expr[:80]))
            spec = index.resolve_numbers(emod, parse_expr2(expanded, {}, cvals), expanded)
            spec.update(notes)
            if re.search(r"\.superRefine\(\s*\(", expanded):
                diag("gap", "G_INLINE_REFINE", where,
                     "%s.%s carries an inline superRefine; its rule is not represented" % (name, f))
            omit, why, via = preprocess_omission(expanded)
            if why is not None:
                apply_preprocess_omission(spec, omit, why, via)
            if omit is None and why:
                # unsupported callback: treated as required (conservative), and
                # the loss of certainty is reported rather than guessed
                diag("gap", "G_PREPROCESS_UNCLASSIFIED", where, why)
            members, lead = index.enum_members(emod, expanded, where)
            if lead and "enum_ref" in spec:
                label = enum_ref_label(index, emod, lead)
                if label:
                    spec["enum_ref"] = label
                else:
                    spec.pop("enum_ref")
            if members is not None and "enum" in spec:
                spec["enum"] = list(dict.fromkeys(members))
        else:
            diag("gap", "G_FIELD_SCHEMA_REF", where,
                 "%s.%s = %s is not inlined; the field is absent from 45d" % (name, f, expr[:80]))
            continue
        if doc:
            spec["doc"] = doc[:300]
        fields[f] = spec
    if re.search(r"\)\s*\.superRefine\(\s*\(", mod.decls[name]["text"]):
        diag("gap", "G_INLINE_REFINE", mod.where(name),
             "%s has an inline superRefine callback; superRefine lists named functions only" % name)
    refines = re.findall(
        r"export const %s\s*=\s*%s((?:\.superRefine\(\w+\))+)"
        % (re.escape(name.replace("RawSchema", "")), re.escape(name)), src)
    return {
        "source": rel,
        "schema": name,
        "superRefine": re.findall(r"\.superRefine\((\w+)\)", refines[0]) if refines else [],
        "fields": fields,
    }


# -------------------------------------------------------------- procedures

PROC_RE = re.compile(r"^\s{2}(\w+)\s*:\s*(\w*[Pp]rocedure)\b", re.M)


def extract_procedures(repo):
    out, rdir = {}, os.path.join(repo, ROUTER_DIR)
    for fn in sorted(os.listdir(rdir)):
        if not fn.endswith(".ts"):
            continue
        src = _read(os.path.join(rdir, fn))
        router = fn[:-3]
        procs = {}
        for m in PROC_RE.finditer(src):
            name, ptype = m.group(1), m.group(2)
            seg = src[m.end():m.end() + 4000]
            nxt = PROC_RE.search(src, m.end())
            if nxt:
                seg = src[m.end():nxt.start()]
            entry = {"procedure": ptype}
            kind = re.search(r"\.(query|mutation|subscription)\(", seg)
            if kind:
                entry["kind"] = kind.group(1)
            mcp = re.search(r"mcp:\s*\{([^}]*)\}", seg, re.S)
            if mcp:
                blob = " ".join(mcp.group(1).split())
                entry["mcp"] = "enabled: true" in blob
                d = re.search(r'description:\s*"(.*?)"', blob)
                if d:
                    entry["description"] = d.group(1)
            inp = re.search(r"\.input\(", seg)
            if inp:
                i, j = balanced(seg, inp.end() - 1, "(", ")")
                entry["input"] = " ".join(seg[i + 1:j].split())[:600]
            procs[name] = entry
        if procs:
            out[router] = procs
    return out


# -------------------------------------------------------------- provenance

def provenance(repo, files, zipname=None):
    import hashlib
    import datetime
    h = {}
    for rel in files:
        p = os.path.join(repo, rel)
        if os.path.isdir(p):
            acc = hashlib.sha256()
            names = sorted(n for n in os.listdir(p) if n.endswith(".ts"))
            for n in names:
                acc.update(_read(os.path.join(p, n), binary=True))
            h[rel + "/ (%d files)" % len(names)] = acc.hexdigest()[:16]
        elif os.path.exists(p):
            h[rel] = hashlib.sha256(_read(p, binary=True)).hexdigest()[:16]
    return {
        "generator": "schema_extract.py v%s" % VERSION,
        "extracted": datetime.date.today().isoformat(),
        "source_drop": zipname or os.path.basename(repo.rstrip("/")),
        "source_sha256_16": h,
        "contract": ("GENERATED. Do not hand-edit. Regenerate from the source drop "
                     "with schema_extract.py. If a value here disagrees with a guide, "
                     "this file wins and the guide is stale."),
    }

# ------------------------------------------------------------------ emit

def emit_entities(repo, zipname=None):
    consts = extract_constants(repo)
    ents = {}
    for label, rel, name in ENTITY_TARGETS:
        e = extract_entity(repo, rel, name, consts)
        if e:
            ents[label] = e
    files = sorted({rel for _, rel, _ in ENTITY_TARGETS} | {CONST_FILE})
    return {
        "_provenance": provenance(repo, files, zipname),
        "_contract": {
            "purpose": "Server write validators per entity: every field, type, bound, "
                       "default, nullability. Replaces hand-authored 45_DATA_field_schemas.json.",
            "reading": "optional=key may be omitted. nullable=explicit null is accepted. "
                       "Both true means omission and null are both accepted: declared .nullish(), "
                       "or a z.preprocess whose omission mechanism is named in `_omission`. "
                       "Facts describe the field's outer schema; a nested item schema's bounds "
                       "and modifiers are not the field's. "
                       "min_ref/max_ref name the constant a bound came from; see 45e.",
            "superRefine": "Cross-field checks run after field validation; their rules are "
                           "NOT in this file. They live in the named function in source.",
        },
        "entities": ents,
    }


LOCAL_ENUM_FILES = [
    "app/src/validators/combat.ts",
    "app/src/validators/objectives.ts",
    "app/src/validators/ai.ts",
    "app/src/validators/quest.ts",
    "app/src/validators/item.ts",
]


def extract_local_enums(repo):
    """`const X = ["a","b"] as const` inside validator files. These are the
    enum lists that z.enum(X) references but that do NOT live in
    constants.ts, so without them an enum_ref cannot be resolved."""
    out = {}
    for rel in LOCAL_ENUM_FILES:
        p = os.path.join(repo, rel)
        if not os.path.exists(p):
            continue
        src = _read(p)
        for m in re.finditer(r"^(?:export )?const (\w+)\s*(?::[^=]*)?=\s*\[", src, re.M):
            name = m.group(1)
            i, j = balanced(src, m.end() - 1, "[", "]")
            body = src[i + 1:j]
            if "{" in body:
                continue
            if "..." in _strip_comments(body):
                index = get_index(repo)
                mod = index.module(rel)
                vals = index.list_values(mod, name) if mod is not None else None
                if vals is None:
                    diag("error", "E_UNRESOLVED_SPREAD", "%s:%s" % (rel, name),
                         "local list with spreads is not a static string list")
                elif vals:
                    out.setdefault(name, {"value": vals, "kind": "list", "source": rel,
                                          "exported": m.group(0).startswith("export")})
                continue
            vals = []
            for v in split_top_args(body):
                v = re.sub(r"/\*.*?\*/", " ", v, flags=re.S)
                v = re.sub(r"//.*", "", v).strip().strip("\"'")
                if v and "..." not in v:
                    vals.append(v)
            if vals and all(re.match(r"^[\w \-'/.]+$", v) for v in vals):
                out.setdefault(name, {"value": vals, "kind": "list", "source": rel,
                                      "exported": src[max(0, m.start() - 7):m.start()].endswith("export ")
                                      or m.group(0).startswith("export")})
    return out


def emit_constants(repo, zipname=None):
    c = extract_constants(repo)
    for k, v in extract_constants(repo, CONST_FILE_COMBAT).items():
        v["source"] = CONST_FILE_COMBAT
        c.setdefault(k, v)
    loc = extract_local_enums(repo)
    for k, v in loc.items():
        c.setdefault(k, v)
    # tagTypes / AvailableEffectTypes are AllTags.options, i.e. the tag
    # discriminants. Derive them so every enum_ref resolves.
    tags = sorted(build_constructors(repo)["unions"].get("AllTags", {}))
    if tags:
        for nm, src_note in (("tagTypes", "AllTags.options"),
                             ("AvailableEffectTypes", "tagTypes fallback [damage]")):
            c[nm] = {"value": tags, "kind": "list", "derived_from": src_note,
                     "source": "app/src/validators/combat.ts"}
    return {
        "_provenance": provenance(repo, [CONST_FILE, CONST_FILE_COMBAT] + LOCAL_ENUM_FILES, zipname),
        "_contract": {
            "purpose": "Every export from app/drizzle/constants.ts with its value, kind "
                       "and the doc comment above it.",
            "kinds": "number|string|boolean|list|array_expr|expr. `value` present only when "
                     "statically resolvable; `raw` is always the source text.",
            "local_enums": "Entries carrying `source` are const arrays defined inside a "
                           "validator file, not constants.ts. They are folded in here so "
                           "every enum_ref in 45c/45d resolves in one place.",
        },
        "count": len(c),
        "constants": c,
    }


def emit_procedures(repo, zipname=None):
    p = extract_procedures(repo)
    total = sum(len(v) for v in p.values())
    described = sum(1 for v in p.values() for e in v.values() if e.get("description"))
    return {
        "_provenance": provenance(repo, [ROUTER_DIR], zipname),
        "_contract": {
            "purpose": "The tRPC surface the builder replays. Router -> procedure -> "
                       "{procedure guard, query|mutation, input schema, mcp description}.",
            "input": "Verbatim source text of the .input() expression, truncated at 600 chars. "
                     "Named schema references resolve in 45d or 45c.",
            "guard": "publicProcedure = no auth. protectedProcedure = session required. "
                     "The guard is not the permission check; staff gating happens in the body.",
        },
        "counts": {"routers": len(p), "procedures": total, "described": described},
        "routers": p,
    }


def report(repo):
    c = emit_ctors(repo)
    print("unions found: %d" % len(c["unions"]))
    for u, members in sorted(c["unions"].items()):
        print("  %-24s %d members" % (u, len(members)))
    print("\nunion members total: %d" % sum(len(m) for m in c["unions"].values()))
    e = emit_entities(repo)
    print("\nentities: %d" % len(e["entities"]))
    for k, v in e["entities"].items():
        print("  %-12s %3d fields  superRefine=%s"
              % (k, len(v["fields"]), ",".join(v["superRefine"]) or "-"))
    k = emit_constants(repo)
    print("\nconstants: %d" % k["count"])
    from collections import Counter
    print("  kinds:", dict(Counter(v["kind"] for v in k["constants"].values())))
    print("  with doc comment: %d"
          % sum(1 for v in k["constants"].values() if v.get("doc")))
    p = emit_procedures(repo)
    print("\nprocedures:", p["counts"])



# ============================================================= Phase 4
# 45g: the single check config that BOTH the builder preflight and
# 70_TOOL_validate.py read. Parity is impossible while each carries its own
# copy of the rules, so the rules live here and both sides consume them.
#
# Two provenance classes inside one file, labelled per block:
#   derived  - computed from the zod validators. Regenerating changes it.
#   law      - an engine behaviour no schema expresses (a cross-field refine,
#              or something only a live push revealed). Hand-maintained, cited
#              to a law number so it can be traced.

def emit_checks(repo, zipname=None):
    ents = emit_entities(repo, zipname)["entities"]
    ctors = emit_ctors(repo)["unions"]
    consts = extract_constants(repo)

    nullable, cap100, required, enums, dates, bools = {}, {}, {}, {}, {}, {}
    for name, spec in ents.items():
        f = spec["fields"]
        nullable[name] = sorted(k for k, v in f.items() if v.get("nullable"))
        cap100[name] = sorted(k for k, v in f.items()
                              if v.get("max") == 100 and v.get("type") == "number")
        required[name] = sorted(k for k, v in f.items()
                                if not v.get("optional") and "default" not in v)
        bools[name] = sorted(k for k, v in f.items() if v.get("type") == "boolean")
        e = {k: v.get("enum") or consts.get(v.get("enum_ref", ""), {}).get("value")
             for k, v in f.items() if v.get("enum") or v.get("enum_ref")}
        enums[name] = {k: v for k, v in e.items() if v}
        # the regex message is the only place the format is stated, so read it
        dates[name] = sorted(k for k, v in f.items()
                             if "YYYY-MM-DD" in (v.get("raw") or ""))

    # Which field names are safe to stop null-stripping by NAME alone. The
    # builder's wsNorm walks a whole request body without entity context, so a
    # field nullable on one entity and required on another cannot be exempted
    # by name: `image` is .nullish() on quest and a plain required string on
    # jutsu, item, bloodline and gameAsset. Exempt only names that are nullable
    # on EVERY entity that declares them, and record the splits so the
    # collision is visible rather than rediscovered.
    owners = {}
    for name, spec in ents.items():
        for f, v in spec["fields"].items():
            owners.setdefault(f, {})[name] = bool(v.get("nullable"))
    exempt = sorted(f for f, o in owners.items() if o and all(o.values()))
    splits = {f: o for f, o in owners.items()
              if any(o.values()) and not all(o.values())}

    tag_power = {}
    for t, spec in ctors.get("AllTags", {}).items():
        pw = spec["fields"].get("power") or {}
        if "max" in pw:
            tag_power[t] = pw["max"]

    return {
        "_provenance": provenance(
            repo, [CONST_FILE, "app/src/validators/combat.ts",
                   "app/src/validators/objectives.ts", "app/src/validators/ai.ts"], zipname),
        "_contract": {
            "purpose": "One check config, two consumers: the builder preflight and "
                       "70_TOOL_validate.py. A check that exists in one must exist in the "
                       "other, and both read their rules from here.",
            "blocks": "Each top-level block carries `_class`: 'derived' is computed from the "
                      "zod validators and changes when the source does; 'law' is hand-held "
                      "engine behaviour no schema expresses, cited to a law number.",
        },
        "nullable": {"_class": "derived",
                     "_note": "Explicit null is ACCEPTED. The builder must not strip these "
                              "(law 72). Everywhere else null must be omitted.",
                     "fields": nullable},
        "cap_100": {"_class": "derived", "_note": "law 8", "fields": cap100},
        "null_strip_exempt": {
            "_class": "derived",
            "_note": "Name-safe subset of `nullable`: these are nullable on every entity that "
                     "declares them, so a context-free normaliser (the builder's wsNorm) can "
                     "stop stripping them without breaking another entity.",
            "_splits": splits,
            "_splits_note": "Nullable on some entities and required on others. NEVER exempt "
                            "these by name; they need entity context.",
            "values": exempt},
        "required_on_create": {"_class": "derived",
                               "_note": "No schema default, so the server has nothing to fall "
                                        "back on. Absent means the create is a paper doll.",
                               "fields": required},
        "enums": {"_class": "derived", "fields": enums},
        "booleans": {"_class": "derived", "_note": "law 73: never coerce these through a "
                                                   "numeric normalisation pass", "fields": bools},
        "date_fields": {"_class": "derived", "_note": "law 7: plain YYYY-MM-DD only",
                        "fields": dates},
        "tag_power_max": {"_class": "derived", "_note": "law 6", "fields": tag_power},
        "runtime_only_tags": {
            "_class": "law", "_cites": 77,
            "_note": "Present in AllTags and constructible, but SuperRefineEffects rejects "
                     "them on every authored record. Shape checks cannot catch these.",
            "values": ["activatesagemode"]},
        "companion_required": {
            "_class": "law", "_cites": 78,
            "_note": "Tag is rejected unless one of `needs` is present on the SAME action.",
            "values": {"consume": ["damage", "pierce"],
                       "vamp": ["damage", "pierce"],
                       "wound": ["damage", "pierce"]}},
        "entity_only_tags": {
            "_class": "law", "_cites": 78,
            "values": {"rollsagemode": "item", "rollbloodline": "item",
                       "removebloodline": "item"}},
        "zero_power_per_level": {
            "_class": "law", "_cites": 78,
            "values": ["rollsagemode", "rollbloodline", "removebloodline",
                       "noncombatconsumereward"]},
        "terminal_actions": {
            "_class": "law", "_cites": "41, 41b",
            "_note": "Only these genuinely end a rule chain. An unconditional specific-jutsu "
                     "rule falls through when the jutsu is on cooldown or unaffordable, so it "
                     "is a priority device, not a terminator.",
            "values": ["move_towards_opponent", "end_turn", "use_random_jutsu"]},
        "formula_tags": {
            "_class": "law", "_cites": 4,
            "_note": "Require BOTH statTypes and generalTypes; an empty one detonates the "
                     "damage formula rather than zeroing it.",
            "values": ["damage", "pierce", "wound"]},
        "hidden_on_create": {
            "_class": "law", "_cites": "16b",
            "_note": "Every entity, every create. Where the table lacks the column the key is "
                     "stripped silently, which is harmless.",
            "values": True},
        "build_order": {
            "_class": "law", "_cites": 17,
            "values": ["jutsu", "asset", "item", "ai", "aiProfile", "quest"]},
    }


def main(argv):
    repo = argv[1] if len(argv) > 1 else "/home/claude/src_repo/TheNinjaRPG-main"
    mode = argv[2] if len(argv) > 2 else "--report"
    zipname = argv[3] if len(argv) > 3 else None
    emitters = {
        "--shapes": lambda: emit_shapes(repo),
        "--ctors": lambda: emit_ctors(repo),
        "--entities": lambda: emit_entities(repo, zipname),
        "--constants": lambda: emit_constants(repo, zipname),
        "--checks": lambda: emit_checks(repo, zipname),
        "--procedures": lambda: emit_procedures(repo, zipname),
    }
    if mode == "--reads":
        # the complete read-set of the contract modes, repository-relative
        for name in ("--ctors", "--entities", "--constants", "--checks"):
            emitters[name]()
        root = os.path.abspath(repo)
        print(json.dumps({"reads": sorted(os.path.relpath(p, root) for p in SOURCE_READS)}, indent=1))
        return 1 if diagnostics_errors() else 0
    if mode == "--gaps":
        for name in ("--ctors", "--entities", "--constants", "--checks"):
            emitters[name]()
        print(json.dumps({"diagnostics": DIAGNOSTICS}, indent=1))
        return 1 if diagnostics_errors() else 0
    if mode not in emitters:
        report(repo)
        return 1 if diagnostics_errors() else 0
    doc = emitters[mode]()
    errors = diagnostics_errors()
    if errors:
        # fail closed: no partial contract on stdout for a `>` redirect to adopt
        for d in errors:
            print("schema_extract: %s %s: %s" % (d["code"], d["where"], d["detail"]), file=sys.stderr)
        print("schema_extract: %d unresolved construct(s); no output written" % len(errors), file=sys.stderr)
        return 1
    print(json.dumps(doc, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

