#!/usr/bin/env python3
"""The AI player's endpoint allowlist: capture the game's MCP surface, check the list, print the review.

    python3 scripts/player_allowlist.py surface --transcript PATH [PATH ...]
        Read the results of the connector's listGameRouters / listRouterEndpoints / getEndpointSchema
        calls out of Claude Code session transcripts and write data/mcp_surface.json. Nothing is
        retyped: what the game returned is what is stored (the raw text is kept beside the parsed form).
    python3 scripts/player_allowlist.py surface --from-source skills/building-tnr-content/data/45f_DATA_procedures.json
        A stand-in built from the pinned source extract, labelled as not live. For dry runs only.
    python3 scripts/player_allowlist.py check
        The gates on data/player_allowlist.json (exit 1 on any violation):
          1. shape     every entry has a kind, activities, a phase, a status, prerequisites and a cooldown note;
          2. never     no entry falls under a never rule (payments, account control, moderation, staff and
                       content editing, communication, deletes);
          3. ask first every entry an ask-first rule covers says so, or states why it cannot spend premium currency;
          4. gates     the call-level gates each rule demands are named on the entry (no Flee, do not attack, ...);
          5. surface   every entry exists on the captured surface with the same kind (read = query, action = mutation);
          6. code      every endpoint the player code can send is on the list.
    python3 scripts/player_allowlist.py report [--out FILE] [--check]
        The review tables for the director: the list by activity, and the surface by router.
        --check: exit 1 unless docs/design/AI_PLAYER_ALLOWLIST_REVIEW.md is what a fresh render gives.

The runner refuses any endpoint that is not on the list (state/prompt_playing_tnr.md section 4.2), so a rule here
is a second lock, not the only one. The rules of record are state/prompt_ai_player_overhaul.md section 2,
state/prompt_playing_tnr.md sections 3 and 5 and CLAUDE.md section 6; the JSON cites them.

Stdlib only. It reads files and makes no network or game call.
"""
import argparse
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ALLOWLIST = os.path.join(ROOT, "data", "player_allowlist.json")
SURFACE = os.path.join(ROOT, "data", "mcp_surface.json")
REVIEW = os.path.join(ROOT, "docs", "design", "AI_PLAYER_ALLOWLIST_REVIEW.md")
CODE_DIRS = [os.path.join(ROOT, "state", "player", "dauntless", "tools"), os.path.join(ROOT, "player")]

KINDS = {"read": "query", "action": "mutation"}
PHASES = ("AP1", "AP2", "AP3", "AP4", "AP5")
STATUSES = ("in_use", "documented", "proposed")
# design section 4.3 (the activities), the two AP1 core activities, and the shared feeds every activity reads
ACTIVITIES = ("battle", "pvp_hunt", "pvp_ranked", "tournament", "war", "bounty", "shrine", "missions", "errands",
              "dailies", "hunting", "farming", "training", "restock", "repair", "equipment", "recovery", "bank",
              "session", "world", "dossier", "harvest")
META_TOOLS = ("listGameRouters", "listRouterEndpoints", "getEndpointSchema")


def _read(path):
    with open(path, encoding="utf8") as f:
        return f.read()


def _load(path):
    return json.loads(_read(path))


# ---------------------------------------------------------------- surface: from session transcripts
SAVED = re.compile(r"^Error: result \(([\d,]+) characters[^)]*\) exceeds maximum allowed tokens\. "
                   r"Output has been saved to (\S+?\.txt)\.")
PERSISTED = re.compile(r"^<persisted-output>\s*\nOutput too large \([^)]*\)\. Full output saved to: (\S+?\.json)\s*\n")


def _result_text(body, transcript):
    """The text of a tool result. A result too large for the conversation is replaced by a notice naming the file
    that holds it; that file is read, but only from under the transcript's own folder."""
    text = body if isinstance(body, str) else "".join(
        x.get("text", "") for x in body or [] if isinstance(x, dict) and x.get("type") == "text")
    home = os.path.realpath(os.path.dirname(transcript))
    m = SAVED.match(text)
    if m:
        path = os.path.realpath(m.group(2))
        if not path.startswith(home + os.sep):
            raise ValueError(f"saved output outside the transcript folder: {m.group(2)}")
        saved = _read(path)
        if len(saved) != int(m.group(1).replace(",", "")):
            raise ValueError(f"saved output {m.group(2)} is not the stated length")
        return saved
    m = PERSISTED.match(text)
    if m:
        path = os.path.realpath(m.group(1))
        if not path.startswith(home + os.sep):
            raise ValueError(f"saved output outside the transcript folder: {m.group(1)}")
        blocks = _load(path)
        if not (isinstance(blocks, list) and blocks and all(b.get("type") == "text" for b in blocks)):
            raise ValueError(f"saved output {m.group(1)} is not a list of text blocks")
        return "".join(b["text"] for b in blocks)
    return text


def read_transcripts(paths):
    """[(tool, input, text, timestamp)] for every answered meta-tool call, oldest first. A failed call (is_error, or
    the connector's own error text) is returned with text None so the caller can count it."""
    out = []
    for path in paths:
        asked = {}
        with open(path, encoding="utf8", errors="replace") as f:
            for line in f:
                try:
                    d = json.loads(line)
                except ValueError:
                    continue
                content = (d.get("message") or {}).get("content")
                if not isinstance(content, list):
                    continue
                for c in content:
                    if not isinstance(c, dict):
                        continue
                    if c.get("type") == "tool_use":
                        tool = c.get("name", "").rsplit("__", 1)[-1]
                        if tool in META_TOOLS and c.get("name", "").startswith("mcp__"):
                            asked[c["id"]] = (tool, c.get("input") or {})
                    elif c.get("type") == "tool_result" and c.get("tool_use_id") in asked:
                        tool, inp = asked[c["tool_use_id"]]
                        text = None if c.get("is_error") else _result_text(c.get("content"), path)
                        if text is not None and re.match(r"^\s*(Error|MCP error)\b", text):
                            text = None
                        out.append((tool, inp, text, d.get("timestamp", "")))
    return sorted(out, key=lambda r: r[3])


def _json_or_none(text):
    try:
        return json.loads(text)
    except (TypeError, ValueError):
        return None


def parse_routers(text):
    """listGameRouters -> {router: endpointCount}. The server answers a JSON list of {name, endpointCount}."""
    rows = _json_or_none(text)
    if not isinstance(rows, list) or not all(isinstance(r, dict) and r.get("name") for r in rows):
        return {}
    return {r["name"]: r.get("endpointCount") for r in rows}


FALLBACK = re.compile(r"^(query|mutation) ([A-Za-z]+(?:\.[A-Za-z0-9]+)+)$")


def parse_endpoints(text, router):
    """listRouterEndpoints -> {endpoint: {description, type, type_source}}, the router prefix taken off the names.
    The server answers a JSON list of {name: "router.endpoint", description}. It does not say query or mutation,
    except in the stand-in description it writes for a procedure that has none ("query combat.listOngoingBattles")."""
    rows = _json_or_none(text)
    if not isinstance(rows, list):
        return None
    out = {}
    for r in rows:
        name = (r.get("name") or "") if isinstance(r, dict) else ""
        if not name.startswith(router + "."):
            return None
        desc = r.get("description") or ""
        m = FALLBACK.match(desc)
        kind = m.group(1) if m and m.group(2) == name else None
        out[name[len(router) + 1:]] = {"description": desc, "type": kind,
                                      "type_source": "the server's stand-in description" if kind else None}
    return out


def source_kinds(path):
    """({router lowercased: {endpoint: kind}}, {endpoint: {kinds}}, label) from the pinned source extract (45f)."""
    d = _load(path)
    by_router, by_name = {}, {}
    for router, procs in d["routers"].items():
        for ep, row in procs.items():
            if row.get("kind") in ("query", "mutation"):
                by_router.setdefault(router.lower(), {})[ep] = row["kind"]
                by_name.setdefault(ep, set()).add(row["kind"])
    return by_router, by_name, f"{os.path.relpath(path, ROOT)} ({d['_provenance'].get('source_drop')})"


def build_surface(calls, kinds_from=None):
    """The surface capture from the transcript calls. The newest answer to each call wins."""
    raw = {"listGameRouters": None, "listRouterEndpoints": {}, "getEndpointSchema": {}}
    failed, stamps = [], []
    for tool, inp, text, ts in calls:
        key = inp.get("routerName") if tool == "listRouterEndpoints" else inp.get("endpointName")
        if text is None:
            failed.append(f"{tool} {key or ''}".strip())
            continue
        stamps.append(ts)
        if tool == "listGameRouters":
            raw[tool] = text
        else:
            raw[tool][key] = text
    if raw["listGameRouters"] is None:
        raise SystemExit("no listGameRouters result in the transcripts")
    names = parse_routers(raw["listGameRouters"])
    if not names:
        raise SystemExit("listGameRouters result did not parse; raw text:\n" + raw["listGameRouters"][:400])
    by_router, by_name, label = source_kinds(kinds_from) if kinds_from else ({}, {}, None)
    routers, missing, miscount, bad_schema = {}, [], [], []
    for name, count in names.items():
        text = raw["listRouterEndpoints"].get(name)
        eps = parse_endpoints(text, name) if text is not None else None
        if eps is None:
            missing.append(name)
            routers[name] = {"endpointCount": count, "endpoints": None}
            continue
        if count is not None and count != len(eps):
            miscount.append(f"{name} ({len(eps)} listed, {count} counted)")
        for ep, row in eps.items():
            if row["type"] is None and kinds_from:
                kind = by_router.get(name.lower(), {}).get(ep)
                if kind:
                    row["type"], row["type_source"] = kind, f"source extract: {label}"
                elif len(by_name.get(ep, ())) == 1:
                    row["type"] = next(iter(by_name[ep]))
                    row["type_source"] = f"source extract, by endpoint name under another router: {label}"
            row["schema"] = None
            text = raw["getEndpointSchema"].get(f"{name}.{ep}")
            if text is not None:
                d = _json_or_none(text)
                if isinstance(d, dict) and d.get("endpointName") == f"{name}.{ep}" and "inputSchema" in d:
                    row["schema"] = d["inputSchema"]
                else:
                    bad_schema.append(f"{name}.{ep}")
        routers[name] = {"endpointCount": count, "endpoints": eps}
    known = {f"listRouterEndpoints {n}" for n in names if n not in missing} | \
        {f"getEndpointSchema {k}" for k in raw["getEndpointSchema"]}
    all_eps = [e for r in routers.values() for e in (r["endpoints"] or {}).values()]
    return {"_meta": {
        "origin": "live: the TNR connector's own listGameRouters / listRouterEndpoints / getEndpointSchema results, "
                  "read out of the session transcripts by scripts/player_allowlist.py surface",
        "live": True,
        "captured": {"first": min(stamps) if stamps else None, "last": max(stamps) if stamps else None},
        "answered_calls": {"listGameRouters": 1, "listRouterEndpoints": len(raw["listRouterEndpoints"]),
                           "getEndpointSchema": len(raw["getEndpointSchema"])},
        "counts": {"routers": len(routers), "endpoints": len(all_eps),
                   "schemas": sum(1 for e in all_eps if e["schema"] is not None),
                   "typed": sum(1 for e in all_eps if e["type"]),
                   "untyped": sum(1 for e in all_eps if not e["type"])},
        "type_note": "The server does not say whether an endpoint is a query or a mutation. 'type' comes from "
                     "'type_source': the server's own stand-in description, or the pinned source extract, which is "
                     "older than the live server. An endpoint with neither has type null.",
        "routers_without_endpoint_list": missing,
        "endpoint_count_mismatch": miscount,
        "schemas_that_did_not_parse": bad_schema,
        "failed_calls_not_answered_later": sorted(set(failed) - known),
        "contract": "GENERATED capture. Do not hand-edit; re-run the surface command."},
        "routers": routers}


def surface_from_source(path):
    """A stand-in surface from the pinned source extract (45f). Not live: the extract is of the game source at its
    pinned commit, and it cannot tell which procedures the MCP server exposes."""
    d = _load(path)
    label = f"source extract: {os.path.relpath(path, ROOT)} ({d['_provenance'].get('source_drop')})"
    routers = {name: {"endpointCount": len(procs), "endpoints": {
        ep: {"type": row.get("kind"), "type_source": label, "description": row.get("description") or "",
             "schema": None} for ep, row in procs.items()}} for name, procs in d["routers"].items()}
    return {"_meta": {
        "origin": f"source extract, NOT live: {os.path.relpath(path, ROOT)} ({d['_provenance'].get('source_drop')})",
        "live": False,
        "captured": {"first": d["_provenance"].get("extracted"), "last": d["_provenance"].get("extracted")},
        "counts": {"routers": len(routers), "endpoints": sum(len(r["endpoints"]) for r in routers.values()),
                   "schemas": 0, "typed": sum(len(r["endpoints"]) for r in routers.values()), "untyped": 0},
        "contract": "GENERATED stand-in for dry runs. The allowlist is approved against a live capture only."},
        "routers": routers}


def cmd_surface(a):
    if a.from_source:
        surface = surface_from_source(a.from_source)
    else:
        paths = [p for pat in a.transcript for p in sorted(glob.glob(pat, recursive=True))]
        if not paths:
            raise SystemExit("no transcript matched")
        surface = build_surface(read_transcripts(paths), a.kinds_from)
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w", encoding="utf8") as f:
        json.dump(surface, f, indent=1, ensure_ascii=False, sort_keys=True)
        f.write("\n")
    m = surface["_meta"]
    print(f"wrote {os.path.relpath(a.out, ROOT)}: {m['counts']['routers']} routers, {m['counts']['endpoints']} "
          f"endpoints, {m['counts']['schemas']} schemas ({'live' if m['live'] else 'NOT live'})")
    if m["live"]:
        print(f"  query or mutation known for {m['counts']['typed']}, unknown for {m['counts']['untyped']}")
    for k in ("routers_without_endpoint_list", "endpoint_count_mismatch", "schemas_that_did_not_parse",
              "failed_calls_not_answered_later"):
        if m.get(k):
            print(f"  {k}: {', '.join(m[k])}")
    return 0


# ---------------------------------------------------------------- rules
def rule_hits(rule, name, kind=None):
    """Whether a never / ask-first rule covers an endpoint (router.endpoint). A rule may be limited to one kind."""
    if name in rule.get("except", ()):
        return False
    if rule.get("kind") and kind and rule["kind"] != kind:
        return False
    router = name.split(".", 1)[0]
    if router in rule.get("routers", ()) or name in rule.get("endpoints", ()):
        return True
    return any(re.search(p, name) for p in rule.get("patterns", ()))


def surface_kind(surface, name):
    """'read' / 'action' / None (unknown type) for an endpoint on the surface; KeyError when it is not there."""
    router, ep = name.split(".", 1)
    row = ((surface["routers"].get(router) or {}).get("endpoints") or {})[ep]
    return {"query": "read", "mutation": "action"}.get((row.get("type") or "").lower())


def code_endpoints(dirs, routers):
    """{endpoint: [files]} for every "router.endpoint" string literal in the player code whose router is a game
    router. Literals that are only response keys or select paths are listed under 'not_calls' in the allowlist."""
    found = {}
    pat = re.compile(r"""["'`]([a-zA-Z]+)\.([a-zA-Z][a-zA-Z0-9]*(?:\.[a-zA-Z][a-zA-Z0-9]*)*)["'`]""")
    for d in dirs:
        for path in sorted(glob.glob(os.path.join(d, "**", "*.py"), recursive=True)):
            if os.path.basename(path) == "pilot_good.py" or f"{os.sep}tests{os.sep}" in path:
                continue                   # the untracked fallback copy; tests name endpoints they never send
            for m in pat.finditer(_read(path)):
                if m.group(1) in routers:
                    found.setdefault(f"{m.group(1)}.{m.group(2)}", []).append(os.path.relpath(path, ROOT))
    return found


def check(allow, surface=None, code_dirs=()):
    """-> (errors, notes). Every error is a violation; notes are for the reader."""
    errs, notes = [], []
    eps = allow.get("endpoints") or {}
    never, ask = allow.get("never") or [], allow.get("ask_first") or []
    gates = allow.get("call_gates") or {}
    for name, e in sorted(eps.items()):
        # 1. shape
        if not re.fullmatch(r"[a-zA-Z]+(\.[a-zA-Z][a-zA-Z0-9]*)+", name):
            errs.append(f"{name}: not a router.endpoint name")
            continue
        if e.get("kind") not in KINDS:
            errs.append(f"{name}: kind must be read or action")
        acts = e.get("activity")
        if not (isinstance(acts, list) and acts and all(x in ACTIVITIES for x in acts)):
            errs.append(f"{name}: activity must be a list drawn from {', '.join(ACTIVITIES)}")
        if e.get("phase") not in PHASES:
            errs.append(f"{name}: phase must be one of {', '.join(PHASES)}")
        if e.get("status") not in STATUSES:
            errs.append(f"{name}: status must be one of {', '.join(STATUSES)}")
        for k in ("prerequisites", "cooldown"):
            if not isinstance(e.get(k), str) or not e[k].strip():
                errs.append(f"{name}: {k} is missing (write 'none known' when there is none)")
        for g in e.get("gates", []):
            if g not in gates:
                errs.append(f"{name}: gate {g!r} is not defined under call_gates")
        # 2. never
        for r in never:
            if rule_hits(r, name, e.get("kind")):
                errs.append(f"{name}: NEVER ({r['id']}: {r['why']})")
        # 3. ask first
        for r in ask:
            if rule_hits(r, name, e.get("kind")) and e.get("ask_first") != r["id"]:
                if r.get("waiver") and str(e.get(r["waiver"], "")).strip():
                    if not set(r.get("waiver_gates", ())) <= set(e.get("gates", ())):
                        errs.append(f"{name}: {r['waiver']} is stated but the gates "
                                    f"{', '.join(r['waiver_gates'])} are not all named")
                    continue
                errs.append(f"{name}: ASK FIRST ({r['id']}: {r['why']}) is not marked on the entry")
        if e.get("ask_first") and e["ask_first"] not in {r["id"] for r in ask}:
            errs.append(f"{name}: ask_first {e['ask_first']!r} is not a rule under ask_first")
        # 4. call-level gates the rules demand
        for g, row in gates.items():
            if name in row.get("required_on", ()) and g not in e.get("gates", ()):
                errs.append(f"{name}: gate {g!r} is required on this endpoint")
        # 5. surface
        if surface is not None:
            try:
                live = surface_kind(surface, name)
            except KeyError:
                errs.append(f"{name}: not on the captured surface")
                continue
            if live is None:
                notes.append(f"{name}: the surface does not state query or mutation; kind unchecked")
            elif live != e.get("kind"):
                errs.append(f"{name}: listed as {e.get('kind')} but the surface says {live}")
    # 6. code
    if code_dirs:
        routers = set(surface["routers"]) if surface is not None else {n.split(".", 1)[0] for n in eps}
        not_calls = allow.get("not_calls") or {}
        for name, files in sorted(code_endpoints(code_dirs, routers).items()):
            if name not in eps and name not in not_calls:
                errs.append(f"{name}: sent by the player code ({', '.join(sorted(set(files)))}) but not on the list")
    if surface is not None and not surface["_meta"].get("live"):
        notes.append("the surface is the source stand-in, not a live capture: this run does not approve anything")
    return errs, notes


def disposition(allow, name, kind):
    """What the list says about one surface endpoint: allowed / ask first / never (rule id) / not listed."""
    e = (allow.get("endpoints") or {}).get(name)
    hit = next((r["id"] for r in allow.get("never") or [] if rule_hits(r, name, kind)), None)
    if e and not hit:
        return ("ask first: " + e["ask_first"]) if e.get("ask_first") else "allowed"
    if hit:
        return "never: " + hit
    return "not listed"


def cmd_check(a):
    allow = _load(a.allowlist)
    surface = _load(a.surface) if os.path.exists(a.surface) else None
    dirs = [d for d in (CODE_DIRS if a.code is None else a.code) if os.path.isdir(d)]
    errs, notes = check(allow, surface, dirs)
    eps = allow.get("endpoints") or {}
    print(f"allowlist: {len(eps)} endpoints "
          f"({sum(1 for e in eps.values() if e.get('kind') == 'read')} read, "
          f"{sum(1 for e in eps.values() if e.get('kind') == 'action')} action; "
          f"{sum(1 for e in eps.values() if e.get('ask_first'))} ask first), "
          f"{len(allow.get('never') or [])} never rules, {len(allow.get('ask_first') or [])} ask-first rules")
    if surface is None:
        print(f"surface: none at {os.path.relpath(a.surface, ROOT)} (surface checks skipped)")
    else:
        m = surface["_meta"]
        tally = {}
        for router, row in surface["routers"].items():
            for ep, e in (row.get("endpoints") or {}).items():
                kind = {"query": "read", "mutation": "action"}.get((e.get("type") or "").lower())
                d = disposition(allow, f"{router}.{ep}", kind).split(":")[0]
                tally[d] = tally.get(d, 0) + 1
        print(f"surface: {m['counts']['routers']} routers, {m['counts']['endpoints']} endpoints "
              f"({'live' if m.get('live') else 'NOT live'}, {m['captured'].get('last')}): "
              + ", ".join(f"{n} {k}" for k, n in sorted(tally.items())))
    for n in notes:
        print("note: " + n)
    for e in errs:
        print("FAIL: " + e)
    print("never-list check: " + ("FAILED" if errs else "clean") + f" ({len(errs)} violation(s))")
    return 1 if errs else 0


# ---------------------------------------------------------------- report
def render_report(allow, surface):
    """The review document as text. It depends on the two files only, so a fresh render of unchanged files is
    byte-identical to the committed one (report --check)."""
    eps = allow.get("endpoints") or {}
    out = []
    w = out.append
    w("# AI player endpoint allowlist: review")
    w("")
    w("Generated by `scripts/player_allowlist.py report` from `data/player_allowlist.json`"
      + (f" and `data/mcp_surface.json` (captured {surface['_meta']['captured']['first']} to "
         f"{surface['_meta']['captured']['last']}; {surface['_meta']['origin']})." if surface else "."))
    w("Do not edit this file; edit the allowlist and run the report again.")
    w("")
    w(f"Status: {allow['_meta']['status']}")
    w("")
    w("## The list, by activity")
    for act in ACTIVITIES:
        rows = sorted((n, e) for n, e in eps.items() if e["activity"][0] == act)
        if not rows:
            continue
        w("")
        w(f"### {act}")
        w("")
        w("| Endpoint | Kind | Phase | Status | Prerequisites | Cooldown or rate | Gates |")
        w("|---|---|---|---|---|---|---|")
        for n, e in rows:
            g = ", ".join(e.get("gates", [])) + (("; " if e.get("gates") else "") + "ASK FIRST: " + e["ask_first"]
                                                 if e.get("ask_first") else "")
            also = f" (also: {', '.join(e['activity'][1:])})" if len(e["activity"]) > 1 else ""
            w(f"| `{n}`{also} | {e['kind']} | {e['phase']} | {e['status'].replace('_', ' ')} | "
              f"{e['prerequisites']} | {e['cooldown']} | {g or '-'} |")
    w("")
    w("## Never rules")
    w("")
    w("| Rule | Covers | Why | Source |")
    w("|---|---|---|---|")
    for r in allow.get("never") or []:
        cov = "; ".join(x for x in ("routers: " + ", ".join(r["routers"]) if r.get("routers") else "",
                                    "endpoints: " + ", ".join(r["endpoints"]) if r.get("endpoints") else "",
                                    "patterns: " + ", ".join(f"`{p}`" for p in r["patterns"]) if r.get("patterns") else "",
                                    "actions only" if r.get("kind") == "action" else "") if x)
        w(f"| {r['id']} | {cov} | {r['why']} | {r['source']} |")
    w("")
    w("## Ask-first rules")
    w("")
    w("| Rule | Covers | Why | Source |")
    w("|---|---|---|---|")
    for r in allow.get("ask_first") or []:
        cov = "; ".join(x for x in ("routers: " + ", ".join(r["routers"]) if r.get("routers") else "",
                                    "endpoints: " + ", ".join(r["endpoints"]) if r.get("endpoints") else "",
                                    "patterns: " + ", ".join(f"`{p}`" for p in r["patterns"]) if r.get("patterns") else "",
                                    "actions only" if r.get("kind") == "action" else "") if x)
        w(f"| {r['id']} | {cov} | {r['why']} | {r['source']} |")
    w("")
    w("## Call-level gates")
    w("")
    w("An endpoint on the list can still be refused for what a call carries. `player/gates.py` (AP1) enforces these.")
    w("")
    w("| Gate | Rule | Required on |")
    w("|---|---|---|")
    for g, row in (allow.get("call_gates") or {}).items():
        w(f"| {g} | {row['rule']} | {', '.join(f'`{x}`' for x in row.get('required_on', [])) or '-'} |")
    if surface is not None:
        w("")
        w("## The surface, by router")
        w("")
        w("Every endpoint the capture lists, and what the allowlist says about it. `not listed` is refused.")
        w("")
        w("| Router | Endpoints | Allowed | Ask first | Never | Not listed |")
        w("|---|---|---|---|---|---|")
        for router in sorted(surface["routers"]):
            row = surface["routers"][router]
            t = {"allowed": [], "ask first": [], "never": [], "not listed": []}
            for ep, e in sorted((row.get("endpoints") or {}).items()):
                kind = {"query": "read", "mutation": "action"}.get((e.get("type") or "").lower())
                t[disposition(allow, f"{router}.{ep}", kind).split(":")[0]].append(ep)
            n = len(row.get("endpoints") or {})
            w(f"| {router} | {n} | {', '.join(t['allowed']) or '-'} | {', '.join(t['ask first']) or '-'} | "
              f"{len(t['never']) or '-'} | {len(t['not listed']) or '-'} |")
    return "\n".join(out) + "\n"


def cmd_report(a):
    text = render_report(_load(a.allowlist), _load(a.surface) if os.path.exists(a.surface) else None)
    if a.check:
        same = os.path.exists(a.out or REVIEW) and _read(a.out or REVIEW) == text
        print(f"{os.path.relpath(a.out or REVIEW, ROOT)}: " + ("current" if same else "STALE: run the report again"))
        return 0 if same else 1
    if a.out:
        with open(a.out, "w", encoding="utf8") as f:
            f.write(text)
        print(f"wrote {os.path.relpath(a.out, ROOT)}")
    else:
        sys.stdout.write(text)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("surface")
    s.add_argument("--transcript", nargs="+", default=[])
    s.add_argument("--from-source")
    s.add_argument("--kinds-from", help="the pinned source extract (45f) to take query / mutation from, labelled")
    s.add_argument("--out", default=SURFACE)
    for name in ("check", "report"):
        c = sub.add_parser(name)
        c.add_argument("--allowlist", default=ALLOWLIST)
        c.add_argument("--surface", default=SURFACE)
        if name == "check":
            c.add_argument("--code", nargs="*", help="code folders to scan (default: the player code); none = no scan")
        else:
            c.add_argument("--out")
            c.add_argument("--check", action="store_true", help="exit 1 unless the committed review is current")
    a = ap.parse_args(argv)
    if a.cmd == "surface" and bool(a.transcript) == bool(a.from_source):
        ap.error("surface needs --transcript PATH... or --from-source FILE")
    return {"surface": cmd_surface, "check": cmd_check, "report": cmd_report}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main())
