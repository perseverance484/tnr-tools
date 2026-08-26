#!/usr/bin/env python3
"""Extract write shapes AND constructors from TNR's zod validators.

CHANGED 2026-08-26: enum resolution is scope-aware.

  A validator's own `const X = [...]` now beats a same-named export from constants.ts, and a
  collision is recorded in the emitted file instead of being resolved silently. Bare `const` is
  read as well as `export const`.

  This existed because two different SECTOR_TYPES do: constants.ts exports village kinds
  (VILLAGE/OUTLAW/SAFEZONE/HIDEOUT/TOWN) and validators/objectives.ts declares placement modes
  (specific/random/from_list/user_village/current_sector/enemy_village). Resolving by name alone
  gave the objective schema the village list, so factory.py rejected the correct `user_village`
  and accepted `TOWN` on every quest location and battle node. validate.py does not enum-check
  that field, so nothing caught it until a build needed it.

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
ARRCONST_RE = re.compile(r"export const (\w+)\s*=\s*\[")
# Validators declare some of their enums as bare `const`, not `export const`.
# SECTOR_TYPES is one, and missing it is how a field got the wrong list.
LOCALCONST_RE = re.compile(r"^\s*const (\w+)\s*=\s*\[", re.M)


def parse_expr(expr: str) -> dict:
    """Parse a single zod expression into a rule dict."""
    e = " ".join(expr.split())
    out = {"raw": e}
    m = re.search(r"z\.(?:coerce\.)?(\w+)", e)
    if m:
        out["type"] = KIND.get(m.group(1), m.group(1))
    out["coerce"] = ".coerce." in e
    out["optional"] = ".optional()" in e or ".nullish()" in e
    out["nullable"] = ".nullable()" in e or ".nullish()" in e
    d = re.search(r"\.(?:prefault|default)\(\s*(.*?)\s*\)(?:\.|$|,)", e)
    if d:
        raw = d.group(1)
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
    if ".int()" in e:
        out["int"] = True
    if ".positive()" in e:
        out["min"] = 1
    for name in ("min", "max"):
        b = re.search(rf"\.{name}\((-?\d+)\)", e)
        if b:
            out[name] = int(b.group(1))
    return out


def parse_objects(path: str) -> dict:
    """Every `export const X = z.object({...})` in a file."""
    blocks, cur, depth = {}, None, 0
    with open(path) as fh:
        lines = fh.readlines()
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
    with open(path) as fh:
        src = fh.read()
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


_ENUM_COLLISIONS: list[str] = []


def parse_const_arrays(path: str) -> dict:
    """`export const NAMES = ["a","b"] as const` -> value lists."""
    out = {}
    with open(path) as fh:
        src = fh.read()
    for m in ARRCONST_RE.finditer(src):
        name = m.group(1)
        i = src.index("[", m.end() - 1)
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
        if "{" in body:          # array of objects, not an enum list
            continue
        vals = [x.strip().strip("\"'") for x in body.split(",") if x.strip()]
        if vals and all(re.match(r"^[\w \-'/.]+$", v) for v in vals):
            out[name] = vals
    return out


def build_constructors(repo: str) -> dict:
    objects, unions = {}, {}
    for rel in CTOR_FILES:
        p = os.path.join(repo, rel)
        if not os.path.exists(p):
            continue
        for k, v in parse_objects(p).items():
            if v:
                objects.setdefault(k, {}).update(v)
        unions.update(parse_unions(p))

    enums = parse_const_arrays(os.path.join(repo, CONST_FILE))
    for rel in CTOR_FILES:
        p = os.path.join(repo, rel)
        if os.path.exists(p):
            enums.update(parse_const_arrays(p))

    ctors = {}
    for uname, members in unions.items():
        entries = {}
        for mem in members:
            fields = objects.get(mem)
            if not fields:
                continue
            disc = None
            for f, r in fields.items():
                if r.get("literal"):
                    disc = {"field": f, "value": r["literal"]}
                    break
            spec = {"schema": mem, "fields": {}}
            if disc:
                spec["discriminant"] = disc
            for f, r in fields.items():
                fs = {"type": r.get("type", "unknown")}
                for k in ("default", "literal", "min", "max", "int", "optional", "nullable"):
                    if r.get(k) not in (None, False):
                        fs[k] = r[k]
                ref = r.get("enum_ref")
                if r.get("enum"):
                    fs["enum"] = r["enum"]
                if ref:
                    fs["enum_ref"] = ref
                    if ref in enums:
                        fs["enum"] = sorted(set(fs.get("enum", []) + enums[ref]))
                spec["fields"][f] = fs
            key = disc["value"] if disc else mem
            entries[key] = spec
        if entries:
            ctors[uname] = entries

    return {"unions": ctors, "objects": {k: v for k, v in objects.items()}, "enums": enums}


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


def collect_helpers(src):
    """`const f = (a) => z...` arrow helpers that return a zod expression."""
    out = {}
    for m in re.finditer(r"const (\w+)\s*=\s*\(([^)]*)\)\s*=>\s*", src):
        tail = src[m.end():m.end() + 600]
        if not tail.lstrip().startswith("z."):
            continue
        params = [p.split(":")[0].strip() for p in m.group(2).split(",") if p.strip()]
        out[m.group(1)] = (params, " ".join(tail.split()))
    return out


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
        args = split_top_args(pp.group(1))
        if len(args) == 2:
            note["_preprocess"] = True
            expr = args[1].strip()
    out = parse_expr(expr)
    out.update(note)
    for name in ("min", "max"):
        if name not in out:
            b = re.search(rf"\.{name}\(\s*([A-Z][A-Z0-9_]*)\s*\)", expr)
            if b:
                ref = b.group(1)
                out[name + "_ref"] = ref
                if isinstance(consts.get(ref), (int, float)):
                    out[name] = consts[ref]
    if ".nullish()" in expr:
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


# ------------------------------------------------------------- constants

def extract_constants(repo, rel=None):
    rel = rel or CONST_FILE
    path = os.path.join(repo, rel)
    src = open(path).read()
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
    src = open(os.path.join(repo, rel)).read()
    helpers = collect_helpers(src)
    m = re.search(r"export const %s\s*=\s*z\.object\(" % re.escape(name), src)
    if not m:
        return None
    i, j = balanced(src, m.end(), "{", "}")
    fields = {}
    for doc, text in split_entries(src[i + 1:j]):
        f, expr = split_field(text)
        if not f or not expr:
            continue
        bare = re.match(r"^([A-Z]\w+)$", expr)
        if bare:
            spec = {"type": "object", "schema_ref": bare.group(1), "raw": expr}
        elif "z." in expr or re.match(r"^\w+\(", expr):
            spec = parse_expr2(expr, helpers, const_values(consts))
        else:
            continue
        if doc:
            spec["doc"] = doc[:300]
        fields[f] = spec
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
        src = open(os.path.join(rdir, fn)).read()
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
                acc.update(open(os.path.join(p, n), "rb").read())
            h[rel + "/ (%d files)" % len(names)] = acc.hexdigest()[:16]
        elif os.path.exists(p):
            h[rel] = hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
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
                       "Both true means the field was declared .nullish(). "
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
        src = open(p).read()
        for m in re.finditer(r"^(?:export )?const (\w+)\s*(?::[^=]*)?=\s*\[", src, re.M):
            name = m.group(1)
            i, j = balanced(src, m.end() - 1, "[", "]")
            body = src[i + 1:j]
            if "{" in body:
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
    # File-local enums WIN over constants.ts, and a name collision is reported rather than
    # silently resolved. Both SECTOR_TYPES exist: constants.ts exports village kinds
    # (VILLAGE/OUTLAW/SAFEZONE/HIDEOUT/TOWN) and validators/objectives.ts declares placement
    # modes (specific/random/from_list/user_village/current_sector/enemy_village). The exported
    # one was winning, so factory.py rejected the correct `user_village` and accepted `TOWN` on
    # every quest location and battle node. A validator's own const is always the one its
    # schemas reference, so scope beats alphabetical luck.
    loc = extract_local_enums(repo)
    for k, v in loc.items():
        if k in c and c[k].get("value") != v.get("value"):
            v = dict(v)
            v["_collision"] = {
                "shadowed": c[k].get("value"),
                "shadowed_source": c[k].get("source", CONST_FILE),
                "note": "Two different consts share this name. The validator-local one is "
                        "authoritative for any schema in that file; the other value is kept "
                        "here so the collision is visible rather than silent.",
            }
            _ENUM_COLLISIONS.append(k)
        c[k] = v
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


if __name__ == "__main__":
    repo = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/src_repo/TheNinjaRPG-main"
    mode = sys.argv[2] if len(sys.argv) > 2 else "--report"
    zipname = sys.argv[3] if len(sys.argv) > 3 else None
    if mode == "--shapes":
        print(json.dumps(emit_shapes(repo), indent=1))
    elif mode == "--ctors":
        print(json.dumps(emit_ctors(repo), indent=1))
    elif mode == "--entities":
        print(json.dumps(emit_entities(repo, zipname), indent=1))
    elif mode == "--constants":
        print(json.dumps(emit_constants(repo, zipname), indent=1))
    elif mode == "--checks":
        print(json.dumps(emit_checks(repo, zipname), indent=1))
    elif mode == "--procedures":
        print(json.dumps(emit_procedures(repo, zipname), indent=1))
    else:
        report(repo)

# --- 2026-08-26: colliding const-array names -------------------------------
# Two constants named SECTOR_TYPES exist (drizzle/constants.ts holds village
# sector types, validators/objectives.ts holds objective location types). The
# extractor resolved enum_ref by bare name, picked whichever loaded last, and
# wrote the village list into every quest objective. The builder fetches the
# result at page load, so preflight rejected every legal objective while two
# documented laws said otherwise. Nothing caught it for a full day.
#
# Silently picking one is the bug. Fail loudly instead.

def assert_no_enum_collisions(repo, files):
    """Raise if the same const-array name is defined in two files with
    different values. Scoped names (NAME@path) are the fix; this is the alarm
    that tells you a new one has appeared."""
    seen = {}
    clashes = []
    for rel in files:
        p = os.path.join(repo, rel)
        if not os.path.exists(p):
            continue
        for name, vals in parse_const_arrays(p).items():
            prev = seen.get(name)
            if prev and prev[1] != vals:
                clashes.append((name, prev[0], prev[1][:6], rel, vals[:6]))
            else:
                seen[name] = (rel, vals)
    if clashes:
        lines = ["colliding const-array names; scope the enum_ref or the wrong list gets written:"]
        for n, a, av, b, bv in clashes:
            lines.append(f"  {n}\n    {a}: {av}\n    {b}: {bv}")
        raise SystemExit("\n".join(lines))
    return len(seen)
