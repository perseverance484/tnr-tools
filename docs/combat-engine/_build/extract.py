#!/usr/bin/env python3
"""Resolve every tag schema in validators/combat.ts AllTags into its full field list.

Usage: python3 extract.py GAME_REPO_ROOT OUT_JSON [--legacy-raw TAGS_RAW_JSON]

GAME_REPO_ROOT is the TheNinjaRPG checkout (the directory holding app/). For each schema in
the AllTags union this follows helper constructors (simpleTag, basicActionTag,
masteryModifierTag, any arrow-function helper that returns a schema), object spreads
(...BaseAttributes and friends, recursively, across imports), .extend()/.merge()/.omit()/.pick()
chains, and multi-line field expressions. A later key overrides an earlier one but keeps
the first position, as in JavaScript object spreads and zod .extend().

Each tag in OUT_JSON has: schema, line, helper, type, description, fields
{name: {expr, from, line, via}} and calculation (the allowed values of the resolved
calculation field, read from its z.enum / z.literal) plus calculation_default. Nothing is
guessed: an expression the resolver cannot read is listed under `unresolved` and the run exits 1.

--legacy-raw writes the tags_raw.json shape that _build/data.py reads (type, desc, fields,
spreads, helper, block), so the old ad-hoc extractor is no longer needed. Stdlib only.
"""
import json
import os
import re
import subprocess
import sys

COMBAT = "app/src/validators/combat.ts"
IDENT = re.compile(r"[A-Za-z_$][\w$]*")


class ExtractError(Exception):
    pass


# --------------------------------------------------------------------------- lexing helpers
def strip_comments(src):
    """Blank out // and /* */ comments, keeping every offset and newline in place."""
    out = list(src)
    i, n = 0, len(src)
    prev_sig = ""  # last significant char, to tell a regex literal from a division

    def blank(a, b):
        for k in range(a, b):
            if out[k] != "\n":
                out[k] = " "

    while i < n:
        c = src[i]
        if c in "\"'`":
            j = skip_string(src, i)
            prev_sig = c
            i = j
            continue
        if c == "/" and i + 1 < n and src[i + 1] == "/":
            j = src.find("\n", i)
            j = n if j < 0 else j
            blank(i, j)
            i = j
            continue
        if c == "/" and i + 1 < n and src[i + 1] == "*":
            j = src.find("*/", i + 2)
            j = n if j < 0 else j + 2
            blank(i, j)
            i = j
            continue
        if c == "/" and (prev_sig == "" or prev_sig in "(,=:[!&|?{};+-*%<>~^"):
            # regex literal
            j = i + 1
            in_class = False
            while j < n and src[j] != "\n":
                if src[j] == "\\":
                    j += 2
                    continue
                if src[j] == "[":
                    in_class = True
                elif src[j] == "]":
                    in_class = False
                elif src[j] == "/" and not in_class:
                    break
                j += 1
            j += 1
            while j < n and src[j].isalpha():
                j += 1
            prev_sig = "/"
            i = j
            continue
        if not c.isspace():
            prev_sig = c
        i += 1
    return "".join(out)


def skip_string(s, i):
    """s[i] is a quote; return the index just past the closing quote."""
    q = s[i]
    j = i + 1
    n = len(s)
    while j < n:
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if q == "`" and c == "$" and j + 1 < n and s[j + 1] == "{":
            j = match_close(s, j + 1) + 1
            continue
        if c == q:
            return j + 1
        j += 1
    raise ExtractError(f"unterminated string at offset {i}")


PAIRS = {"(": ")", "[": "]", "{": "}"}


def match_close(s, i):
    """s[i] is an opening bracket; return the index of its matching closer."""
    stack = [PAIRS[s[i]]]
    j = i + 1
    n = len(s)
    while j < n:
        c = s[j]
        if c in "\"'`":
            j = skip_string(s, j)
            continue
        if c in PAIRS:
            stack.append(PAIRS[c])
        elif c in ")]}":
            if c != stack[-1]:
                raise ExtractError(f"bracket mismatch at offset {j}")
            stack.pop()
            if not stack:
                return j
        j += 1
    raise ExtractError(f"unclosed bracket at offset {i}")


def split_top(s, start, end, sep=","):
    """Split s[start:end] at depth-0 separators; return [(a, b)] spans, empty ones dropped."""
    spans = []
    depth = 0
    j = start
    seg = start
    while j < end:
        c = s[j]
        if c in "\"'`":
            j = skip_string(s, j)
            continue
        if c in PAIRS:
            depth += 1
        elif c in ")]}":
            depth -= 1
        elif c == sep and depth == 0:
            spans.append((seg, j))
            seg = j + 1
        j += 1
    spans.append((seg, end))
    out = []
    for a, b in spans:
        while a < b and s[a].isspace():
            a += 1
        while b > a and s[b - 1].isspace():
            b -= 1
        if a < b:
            out.append((a, b))
    return out


def expr_end(s, i, stops=";"):
    """Index of the first depth-0 character in stops at or after i (or len(s))."""
    depth = 0
    n = len(s)
    j = i
    while j < n:
        c = s[j]
        if c in "\"'`":
            j = skip_string(s, j)
            continue
        if c in PAIRS:
            depth += 1
        elif c in ")]}":
            if depth == 0:
                return j
            depth -= 1
        elif c in stops and depth == 0:
            return j
        j += 1
    return n


def collapse(expr):
    """Collapse whitespace outside strings; drop layout-only spaces and trailing commas."""
    out = []
    i, n = 0, len(expr)
    while i < n:
        c = expr[i]
        if c in "\"'`":
            j = skip_string(expr, i)
            lit = expr[i:j]
            if c == "`":
                lit = re.sub(r"\s+", " ", lit)
            out.append(lit)
            i = j
            continue
        if c.isspace():
            while i < n and expr[i].isspace():
                i += 1
            out.append(" ")
            continue
        out.append(c)
        i += 1
    s = "".join(out).strip()
    # Layout-only whitespace around member access and brackets, outside strings.
    parts = re.split(r"(\"(?:\\.|[^\"\\])*\"|'(?:\\.|[^'\\])*'|`(?:\\.|[^`\\])*`)", s)
    for k in range(0, len(parts), 2):
        p = parts[k]
        p = re.sub(r"\s+\.(?!\.)", ".", p)
        p = re.sub(r"([(\[{])\s+", r"\1", p)
        p = re.sub(r"\s+([)\]}])", r"\1", p)
        p = re.sub(r",\s*([)\]}])", r"\1", p)
        parts[k] = p
    return "".join(parts)


def string_value(lit):
    lit = lit.strip()
    if len(lit) >= 2 and lit[0] in "\"'`" and lit[-1] == lit[0]:
        body = lit[1:-1]
        if lit[0] == "`":
            return re.sub(r"\s+", " ", body).strip()
        return bytes(body, "utf-8").decode("unicode_escape") if "\\" in body else body
    return None


def subst(expr, bindings):
    """Replace free identifiers named in bindings (not member names, not keys, not in strings)."""
    if not bindings:
        return expr
    out = []
    i, n = 0, len(expr)
    while i < n:
        c = expr[i]
        if c in "\"'`":
            j = skip_string(expr, i)
            out.append(expr[i:j])
            i = j
            continue
        m = IDENT.match(expr, i)
        if m and (i == 0 or not (expr[i - 1].isalnum() or expr[i - 1] in "_$")):
            name = m.group(0)
            before = expr[:i].rstrip()
            after = expr[m.end():].lstrip()
            is_member = before.endswith(".") and not before.endswith("...")
            is_key = after.startswith(":") and not after.startswith("::")
            if name in bindings and not is_member and not is_key:
                out.append(bindings[name])
            else:
                out.append(name)
            i = m.end()
            continue
        out.append(c)
        i += 1
    return "".join(out)


# --------------------------------------------------------------------------- modules
class Module:
    def __init__(self, root, rel):
        self.root = root
        self.rel = rel
        path = os.path.join(root, rel)
        self.raw = open(path, encoding="utf-8").read()
        self.src = strip_comments(self.raw)
        self.line_starts = [0] + [m.end() for m in re.finditer(r"\n", self.raw)]
        self.decls = {}
        self.imports = {}
        self._scan()

    def line(self, off):
        lo, hi = 0, len(self.line_starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if self.line_starts[mid] <= off:
                lo = mid
            else:
                hi = mid - 1
        return lo + 1

    def _scan(self):
        s = self.src
        for m in re.finditer(r"^(?:export\s+)?const\s+([A-Za-z_$][\w$]*)\s*(?::[^=]+)?=\s*", s, re.M):
            name = m.group(1)
            a = m.end()
            b = expr_end(s, a, ";")
            self.decls.setdefault(name, (a, b, self.line(m.start())))
        for m in re.finditer(r"^import\s+(?:type\s+)?\{([^}]*)\}\s*from\s*\"([^\"]+)\"", s, re.M):
            for part in m.group(1).split(","):
                part = part.strip()
                if not part or part.startswith("type "):
                    continue
                if " as " in part:
                    orig, alias = [x.strip() for x in part.split(" as ")]
                else:
                    orig = alias = part
                self.imports[alias] = (orig, m.group(2))

    def text(self, name):
        a, b, _ = self.decls[name]
        return self.src[a:b]


class Resolver:
    def __init__(self, root):
        self.root = root
        self.modules = {}
        self.unresolved = []

    def module(self, rel):
        if rel not in self.modules:
            self.modules[rel] = Module(self.root, rel)
        return self.modules[rel]

    def aliases(self):
        """tsconfig `paths` (e.g. @/drizzle/* -> ./drizzle/*), longest prefix first."""
        if not hasattr(self, "_aliases"):
            self._aliases = []
            try:
                cfg = open(os.path.join(self.root, "app/tsconfig.json"), encoding="utf-8").read()
                for pre, tgt in re.findall(r"\"(@/[^\"*]*)\*\"\s*:\s*\[\s*\"\./([^\"*]*)\*\"", cfg):
                    self._aliases.append((pre, os.path.join("app", tgt)))
            except OSError:
                pass
            self._aliases.append(("@/", "app/src/"))
            self._aliases.sort(key=lambda p: -len(p[0]))
        return self._aliases

    def import_path(self, spec, from_rel=None):
        base = None
        if spec.startswith(".") and from_rel:
            base = os.path.normpath(os.path.join(os.path.dirname(from_rel), spec))
        else:
            for pre, tgt in self.aliases():
                if spec.startswith(pre):
                    base = tgt + spec[len(pre):]
                    break
        if base is None:
            return None
        for ext in (".ts", ".tsx", "/index.ts"):
            if os.path.exists(os.path.join(self.root, base + ext)):
                return base + ext
        return None

    def lookup(self, mod, name):
        """Return (module, name) where `name` is declared, following imports."""
        if name in mod.decls:
            return mod, name
        if name in mod.imports:
            orig, spec = mod.imports[name]
            rel = self.import_path(spec, mod.rel)
            if rel:
                m2 = self.module(rel)
                if orig in m2.decls:
                    return m2, orig
                if orig in m2.imports:
                    return self.lookup(m2, orig)
        return None, None

    # ---- call chains -------------------------------------------------------------
    def chain(self, s, a, b):
        """Parse s[a:b] as `ident(.ident | (args))*`; return segments [(name, args_span|None)]."""
        segs = []
        i = a
        while i < b and s[i].isspace():
            i += 1
        m = IDENT.match(s, i)
        if not m:
            return None, i
        segs.append([m.group(0), None])
        i = m.end()
        while i < b:
            j = i
            while j < b and s[j].isspace():
                j += 1
            if j < b and s[j] == "." and s[j:j + 3] != "...":
                j += 1
                while j < b and s[j].isspace():
                    j += 1
                m = IDENT.match(s, j)
                if not m:
                    break
                segs.append([m.group(0), None])
                i = m.end()
            elif j < b and s[j] == "(":
                k = match_close(s, j)
                segs[-1][1] = (j + 1, k)
                i = k + 1
            elif j < b and s[j] == "<" and segs and segs[-1][1] is None:
                # generic call site: name<...>(...)
                depth, k = 0, j
                while k < b:
                    if s[k] == "<":
                        depth += 1
                    elif s[k] == ">":
                        depth -= 1
                        if depth == 0:
                            break
                    k += 1
                i = k + 1
            else:
                break
        rest = s[i:b].strip()
        if rest.startswith("as "):
            rest = ""
        return segs, (None if rest else i)

    # ---- objects -------------------------------------------------------------------
    def object_fields(self, mod, s, a, b, owner, bindings, via, line_mod=None):
        """Fields of the object literal whose braces are s[a] .. s[b-1]."""
        if s[a] != "{":
            raise ExtractError(f"{owner}: expected object literal")
        fields = {}
        spreads = []
        lm = line_mod or mod
        for x, y in split_top(s, a + 1, b - 1):
            ent = s[x:y]
            if ent.startswith("..."):
                ref = collapse(subst(ent[3:], bindings))
                spreads.append(ref)
                sub = self.object_ref(mod, ref, via + [owner])
                if sub is None:
                    self.unresolved.append(f"{owner}: spread ...{ref}")
                    continue
                for k, v in sub.items():
                    fields[k] = v
                continue
            km = re.match(r"(?:\"([^\"]+)\"|'([^']+)'|([A-Za-z_$][\w$]*))\s*(:)?", ent)
            if not km:
                self.unresolved.append(f"{owner}: entry {collapse(ent)[:60]}")
                continue
            key = km.group(1) or km.group(2) or km.group(3)
            if km.group(4):
                expr = ent[km.end():]
            else:
                expr = key  # shorthand
            fields[key] = {
                "expr": collapse(subst(expr, bindings)),
                "from": owner,
                "file": lm.rel,
                "line": lm.line(x),
                "via": list(via),
            }
        return fields, spreads

    def object_ref(self, mod, ref, via):
        """Fields of an object-valued reference: a const object literal or `Schema.shape`."""
        ref = ref.strip()
        m = re.fullmatch(r"([A-Za-z_$][\w$]*)(?:\.shape)?", ref)
        if not m:
            return None
        m2, name = self.lookup(mod, m.group(1))
        if not m2:
            return None
        t = m2.text(name).strip()
        off = m2.decls[name][0] + (len(m2.text(name)) - len(m2.text(name).lstrip()))
        if t.startswith("{"):
            end = match_close(m2.src, off)
            f, _ = self.object_fields(m2, m2.src, off, end + 1, name, {}, via)
            return f
        if ref.endswith(".shape"):
            r = self.schema(m2, name, via)
            return r["fields"]
        return None

    # ---- schemas -------------------------------------------------------------------
    def schema(self, mod, name, via=None):
        via = via or []
        a, b, line = mod.decls[name]
        res = self.schema_expr(mod, mod.src, a, b, name, {}, via)
        res.setdefault("line", line)
        return res

    def schema_expr(self, mod, s, a, b, owner, bindings, via):
        segs, _ = self.chain(s, a, b)
        if not segs:
            raise ExtractError(f"{owner}: cannot read schema expression")
        res = {"fields": {}, "helper": None, "wrappers": [], "spreads": [], "base": None}
        k = 0
        head = segs[0][0]
        if head == "z" and len(segs) > 1 and segs[1][0] == "object":
            x, y = segs[1][1]
            obj_a = x
            while s[obj_a].isspace():
                obj_a += 1
            obj_b = match_close(s, obj_a) + 1
            res["fields"], res["spreads"] = self.object_fields(mod, s, obj_a, obj_b, owner, bindings, via)
            k = 2
        else:
            m2, target = self.lookup(mod, head)
            if not m2:
                raise ExtractError(f"{owner}: unknown schema or helper {head}")
            body = m2.text(target)
            helper = re.match(r"\s*(?:<[^>]*>)?\s*\(([^)]*)\)\s*(?::[^=]*)?=>\s*", body)
            if helper and segs[0][1] is not None:
                params = [IDENT.match(p.strip()).group(0) for p in helper.group(1).split(",") if p.strip()]
                x, y = segs[0][1]
                args = [collapse(subst(s[p:q], bindings)) for p, q in split_top(s, x, y)]
                bind = dict(zip(params, args))
                hb = m2.decls[target][0] + helper.end()
                he = m2.decls[target][1]
                inner = self.schema_expr(m2, m2.src, hb, he, target, bind, via + [owner])
                res = inner
                res["helper"] = target
                res["helper_args"] = args
            elif segs[0][1] is None:
                inner = self.schema(m2, target, via + [owner])
                res = {
                    "fields": {kk: dict(v, via=v["via"]) for kk, v in inner["fields"].items()},
                    "helper": inner.get("helper"),
                    "wrappers": list(inner["wrappers"]),
                    "spreads": list(inner["spreads"]),
                    "base": target,
                }
            else:
                raise ExtractError(f"{owner}: {head}(...) is not a schema helper")
            k = 1
        for seg_name, span in segs[k:]:
            if span is None:
                res["wrappers"].append(seg_name)
                continue
            x, y = span
            arg = s[x:y].strip()
            ax = x + (len(s[x:y]) - len(s[x:y].lstrip()))
            if seg_name == "extend" and arg.startswith("{"):
                ae = match_close(s, ax) + 1
                ext, sp = self.object_fields(mod, s, ax, ae, owner, bindings, via)
                res["spreads"] += sp
                for kk, v in ext.items():
                    res["fields"][kk] = v
            elif seg_name in ("merge", "extend"):
                ref = collapse(arg)
                other = self.object_ref(mod, ref if ref.endswith(".shape") else ref + ".shape", via + [owner])
                if other is None:
                    self.unresolved.append(f"{owner}: .{seg_name}({collapse(arg)[:40]})")
                    continue
                for kk, v in other.items():
                    res["fields"][kk] = v
            elif seg_name in ("omit", "pick"):
                keys = re.findall(r"([A-Za-z_$][\w$]*)\s*:\s*true", arg)
                if seg_name == "omit":
                    for kk in keys:
                        res["fields"].pop(kk, None)
                else:
                    res["fields"] = {kk: v for kk, v in res["fields"].items() if kk in keys}
                res["wrappers"].append(f"{seg_name}({', '.join(keys)})")
            else:
                res["wrappers"].append(seg_name)
        return res

    # ---- values --------------------------------------------------------------------
    def string_array(self, mod, expr):
        """String values of an array literal or a const array name (spreads followed)."""
        expr = expr.strip()
        expr = re.sub(r"\s+as\s+const$", "", expr)
        if expr.startswith("["):
            out = []
            end = match_close(expr, 0)
            for p, q in split_top(expr, 1, end):
                item = expr[p:q]
                if item.startswith("..."):
                    sub = self.string_array(mod, item[3:])
                    if sub is None:
                        return None
                    out += sub
                else:
                    v = string_value(item)
                    if v is None:
                        return None
                    out.append(v)
            return out
        m = re.fullmatch(r"([A-Za-z_$][\w$]*)", expr)
        if m:
            m2, name = self.lookup(mod, m.group(1))
            if m2:
                return self.string_array(m2, collapse(m2.text(name)))
        return None

    def enum_values(self, mod, expr, fields_ctx=None):
        """Allowed values and default of a z.enum / z.literal expression (or a reference to one)."""
        e = expr.strip()
        m = re.match(r"([A-Za-z_$][\w$]*)\.([A-Za-z_$][\w$]*)", e)
        if m and m.group(1) != "z":
            sub = self.object_ref(mod, m.group(1), [])
            if sub and m.group(2) in sub:
                vals, dflt = self.enum_values(mod, sub[m.group(2)]["expr"])
                d2 = re.search(r"\.(?:prefault|default)\((\"[^\"]*\"|'[^']*')\)", e[m.end():])
                return vals, (string_value(d2.group(1)) if d2 else dflt)
            return None, None
        vals = None
        m = re.match(r"z\.enum\(", e)
        if m:
            end = match_close(e, m.end() - 1)
            vals = self.string_array(mod, e[m.end():end])
        m = re.match(r"z\.literal\(", e)
        if m:
            end = match_close(e, m.end() - 1)
            v = string_value(e[m.end():end])
            vals = [v] if v is not None else None
        d = re.search(r"\.(?:prefault|default)\((\"[^\"]*\"|'[^']*')\)", e)
        return vals, (string_value(d.group(1)) if d else None)


def literal_arg(expr):
    """First string-literal argument of a call expression such as msg("...") or tagType("x")."""
    m = re.match(r"[A-Za-z_$][\w$.]*\(\s*", expr)
    if not m:
        return None
    rest = expr[m.end():]
    if rest[:1] in "\"'`":
        j = skip_string(rest, 0)
        return string_value(rest[:j])
    return None


def git_head(root):
    try:
        return subprocess.run(["git", "-C", root, "rev-parse", "--short", "HEAD"], capture_output=True,
                              text=True, check=True).stdout.strip()
    except Exception:
        return None


def extract(root):
    r = Resolver(root)
    mod = r.module(COMBAT)
    s = mod.src
    if "AllTags" not in mod.decls:
        raise ExtractError("AllTags not found")
    a, b, _ = mod.decls["AllTags"]
    m = re.match(r"\s*z\.union\(\s*\[", s[a:b])
    if not m:
        raise ExtractError("AllTags is not z.union([...])")
    arr = a + m.end() - 1
    names = []
    for p, q in split_top(s, arr + 1, match_close(s, arr)):
        segs, _ = r.chain(s, p, q)
        names.append(segs[0][0])
    tags = {}
    for name in names:
        res = r.schema(mod, name)
        f = res["fields"]
        typ = literal_arg(f["type"]["expr"]) if "type" in f else None
        desc = literal_arg(f["description"]["expr"]) if "description" in f else None
        if not typ:
            r.unresolved.append(f"{name}: type")
            continue
        calc = calc_default = None
        if "calculation" in f:
            calc, calc_default = r.enum_values(r.module(f["calculation"]["file"]), f["calculation"]["expr"])
            if calc is None:
                r.unresolved.append(f"{name}: calculation {f['calculation']['expr']}")
        a2, b2, line = mod.decls[name]
        tags[typ] = {
            "schema": name,
            "line": line,
            "helper": res.get("helper"),
            "base_schema": res.get("base"),
            "type": typ,
            "description": desc,
            "calculation": calc,
            "calculation_default": calc_default,
            "fields": {k: {"expr": v["expr"], "from": v["from"], "file": v["file"], "line": v["line"],
                           "via": [x for x in v["via"] if x != name]} for k, v in f.items()},
            "wrappers": res["wrappers"],
            "_spreads": res["spreads"],
            "_block": s[a2:b2],
        }
    if len(tags) != len(names):
        r.unresolved.append(f"AllTags has {len(names)} schemas, resolved {len(tags)} types")
    return {
        "game_repo_head": git_head(root),
        "schema_file": COMBAT,
        "all_tags_count": len(names),
        "tags": tags,
        "unresolved": r.unresolved,
    }


def legacy_raw(result):
    """The tags_raw.json shape _build/data.py reads, keyed by schema const name."""
    out = {}
    for t in result["tags"].values():
        own = [k for k, v in t["fields"].items()
               if k not in ("type", "description") and v["from"] not in ("BaseAttributes", "PowerAttributes")]
        out[t["schema"]] = {
            "type": t["type"],
            "desc": t["description"] or "",
            "fields": own,
            "spreads": [x for x in t["_spreads"] if re.fullmatch(r"\w+", x)],
            "helper": t["helper"],
            "block": t["_block"][:1500],
        }
    return out


def main(argv):
    args = argv[1:]
    legacy = None
    if "--legacy-raw" in args:
        i = args.index("--legacy-raw")
        legacy = args[i + 1]
        del args[i:i + 2]
    if len(args) != 2:
        print(__doc__.strip().split("\n\n")[1], file=sys.stderr)
        return 2
    root, out = args
    result = extract(root)
    clean = dict(result)
    clean["tags"] = {k: {kk: vv for kk, vv in v.items() if not kk.startswith("_")}
                     for k, v in sorted(result["tags"].items())}
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w") as fh:
        json.dump(clean, fh, indent=1)
        fh.write("\n")
    if legacy:
        with open(legacy, "w") as fh:
            json.dump(legacy_raw(result), fh, indent=1)
    print(f"{len(result['tags'])} tags from {result['all_tags_count']} AllTags schemas -> {out}")
    if result["unresolved"]:
        print("UNRESOLVED:", *result["unresolved"], sep="\n  ", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
