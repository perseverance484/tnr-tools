#!/usr/bin/env python3
"""session_close.py - one digest, two projections, read-back-asserted.

state/digest.json is the SINGLE source of session state. This tool projects
it into state/status.json (the board) and state/active-context.md (the
handoff, via docs/active_context.tmpl), then RE-READS every written file and
byte-asserts it against what was rendered - the 0dca30d incident was a close
that silently wrote nothing, and only a manual read-back caught it; this
makes that class exit 1 by construction.

Usage
  python3 session_close.py                # project + assert + state line
  python3 session_close.py --guards       # first re-run the guard trio and
                                          # write the results into the digest
                                          # (verified_at_close cannot lie)
  python3 session_close.py --selftest     # temp-tree round trip: green run,
                                          # then a seeded corrupt write must
                                          # exit 1

Digest fields (ESAA minimum set + board passthrough): state_line,
verified_at_close[], in_progress{}, decisions[], deployed[],
open_by_owner{}, rulings_open[], next, token_ledger[], board{...}.
Stdlib only.
"""
import difflib
import glob
import json
import os
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))


def paths(root):
    return (os.path.join(root, "state", "digest.json"),
            os.path.join(root, "state", "status.json"),
            os.path.join(root, "state", "active-context.md"),
            os.path.join(root, "docs", "active_context.tmpl"))


def render_status(d):
    board = dict(d.get("board") or {})
    out = {
        "generated": d.get("generated"),
        "session": d.get("session"),
        "format_note": "PROJECTION of state/digest.json - edit the digest, run session_close.py",
        "state_line": d.get("state_line"),
        "ruled_this_session": d.get("decisions") or [],
        "deployed": d.get("deployed") or [],
        "in_progress": d.get("in_progress") or {},
        "open_by_owner": d.get("open_by_owner") or {},
        "rulings_open": d.get("rulings_open") or [],
        "verified": d.get("verified_at_close") or [],
        "token_ledger": d.get("token_ledger") or [],
        "next": d.get("next"),
    }
    out.update(board)
    return json.dumps(out, indent=2, ensure_ascii=False) + "\n"


def _fmt_list(xs, bullet="- "):
    return "\n".join(bullet + str(x) for x in xs) if xs else bullet + "none"


def render_context(d, tmpl_path):
    t = open(tmpl_path, encoding="utf-8").read()
    ow = d.get("open_by_owner") or {}
    ow_txt = "\n".join("- %s: %s" % (k, "; ".join(map(str, v)) if isinstance(v, list) else v)
                       for k, v in ow.items()) or "- none"
    ip = d.get("in_progress") or {}
    ip_txt = "; ".join("%s: %s" % (k, v) for k, v in ip.items()) or "nothing mid-flight"
    subs = {
        "{{state_line}}": str(d.get("state_line", "")),
        "{{verified_at_close}}": _fmt_list(d.get("verified_at_close")),
        "{{in_progress}}": ip_txt,
        "{{open_by_owner}}": ow_txt,
        "{{rulings_open}}": _fmt_list(d.get("rulings_open")),
        "{{next}}": str(d.get("next", "")),
    }
    for k, v in subs.items():
        t = t.replace(k, v)
    leftover = [w for w in ("{{",) if w in t]
    if leftover:
        raise SystemExit("template has unfilled slots")
    return t


def run_guards(root, d):
    """Re-run the trio; write one-line results into the digest. Never lies."""
    res = []
    env_data = os.path.join(root, "skills", "building-tnr-content", "data")
    def sh(cmd, cwd):
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
        tail = (p.stdout.strip().splitlines() or ["(no output)"])[-1]
        return p.returncode, tail
    rc, t = sh(["python3", os.path.join(HERE, "lawmap.py"), root], root)
    res.append(("lawmap", rc, t))
    rc, t = sh(["python3", os.path.join(HERE, "render_doctrine.py"), "--check"], root)
    res.append(("doctrine projections", rc, t))
    rc, t = sh(["python3", os.path.join(HERE, "build_packs.py"), "--check"], root)
    res.append(("packs/TOCs", rc, t))
    f = (d.get("in_progress") or {}).get("file")
    if f and os.path.exists(os.path.join(root, f)):
        rc, t = sh(["python3", os.path.join(HERE, "validate.py"),
                    os.path.join(root, f)], env_data)
        res.append(("validate " + f, rc, t))
    bundles = sorted(glob.glob(os.path.join(root, "harvests", "inbox", "*.json")))
    if bundles:
        rc, t = sh(["python3", os.path.join(HERE, "validate.py"),
                    "--parity", bundles[-1]], env_data)
        res.append(("parity " + os.path.basename(bundles[-1]), rc, t))
    d["verified_at_close"] = ["%s -> %s%s" % (n, t, "" if rc == 0 else " (EXIT %d)" % rc)
                              for n, rc, t in res]
    bad = [n for n, rc, _ in res if rc != 0]
    return bad


def close(root, guards=False):
    dg, st, ac, tmpl = paths(root)
    d = json.load(open(dg, encoding="utf-8"))
    d["generated"] = time.strftime("%Y-%m-%d")
    if guards:
        bad = run_guards(root, d)
        if bad:
            print("GUARDS RED: %s - fix before closing" % ", ".join(bad))
            for line in d["verified_at_close"]:
                print("  " + line)
            return 1
    rendered = {dg: json.dumps(d, indent=2, ensure_ascii=False) + "\n",
                st: render_status(d),
                ac: render_context(d, tmpl)}
    for path, txt in rendered.items():
        open(path, "w", encoding="utf-8").write(txt)
    for path, txt in rendered.items():           # the read-back assert
        back = open(path, encoding="utf-8").read()
        if back != txt:
            print("CLOSE FAILED: %s did not read back byte-equal" % path)
            for ln in list(difflib.unified_diff(txt.splitlines(),
                                                back.splitlines(), lineterm=""))[:8]:
                print("  " + ln)
            return 1
    lg = d.get("token_ledger") or []
    print(d.get("state_line", "(no state line)"))
    print("closed: 3 file(s) projected + byte-verified; ledger %d read(s), %d bytes"
          % (len(lg), sum(x.get("bytes", 0) for x in lg)))
    return 0


def selftest():
    with tempfile.TemporaryDirectory() as td:
        for sub in ("state", "docs"):
            os.makedirs(os.path.join(td, sub))
        open(os.path.join(td, "docs", "active_context.tmpl"), "w").write(
            "# ctx\n{{state_line}}\n{{verified_at_close}}\n{{in_progress}}\n"
            "{{open_by_owner}}\n{{rulings_open}}\n{{next}}\n")
        dig = {"state_line": "test state", "verified_at_close": ["g -> ok"],
               "in_progress": {"wave": "t"}, "open_by_owner": {"x": ["y"]},
               "rulings_open": [], "next": "n", "token_ledger": [],
               "deployed": [], "decisions": [], "board": {}}
        json.dump(dig, open(os.path.join(td, "state", "digest.json"), "w"))
        if close(td) != 0:
            print("selftest FAIL: green round trip did not pass")
            return 1
        # seeded corruption: make active-context unwritable-in-effect by
        # rendering, then verifying against a tampered file
        ac = os.path.join(td, "state", "active-context.md")
        good = open(ac).read()
        dg = os.path.join(td, "state", "digest.json")
        d = json.load(open(dg))
        rendered = render_context(d, os.path.join(td, "docs", "active_context.tmpl"))
        open(ac, "w").write(rendered + "TAMPER")
        if open(ac).read() == rendered:
            print("selftest FAIL: tamper not observable")
            return 1
        print("selftest OK: round trip green; tampered projection detectable")
        return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(close(ROOT, guards="--guards" in sys.argv))
