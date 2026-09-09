#!/usr/bin/env python3
"""Project state/digest.json into the session handoff and board."""

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
    return (
        os.path.join(root, "state", "digest.json"),
        os.path.join(root, "state", "status.json"),
        os.path.join(root, "state", "active-context.md"),
        os.path.join(root, "docs", "active_context.tmpl"),
    )


def render_status(d):
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
    out.update(d.get("board") or {})
    return json.dumps(out, indent=2, ensure_ascii=False) + "\n"


def format_list(values):
    return "\n".join("- " + str(value) for value in values) if values else "- none"


def render_context(d, template_path):
    text = open(template_path, encoding="utf-8").read()
    open_by_owner = d.get("open_by_owner") or {}
    owner_text = "\n".join(
        "- %s: %s" % (owner, "; ".join(map(str, items)) if isinstance(items, list) else items)
        for owner, items in open_by_owner.items()
    ) or "- none"
    in_progress = d.get("in_progress") or {}
    progress_text = "; ".join("%s: %s" % item for item in in_progress.items()) or "nothing mid-flight"

    replacements = {
        "{{state_line}}": str(d.get("state_line", "")),
        "{{verified_at_close}}": format_list(d.get("verified_at_close") or []),
        "{{in_progress}}": progress_text,
        "{{open_by_owner}}": owner_text,
        "{{rulings_open}}": format_list(d.get("rulings_open") or []),
        "{{next}}": str(d.get("next", "")),
    }
    for key, value in replacements.items():
        text = text.replace(key, value)
    if "{{" in text:
        raise SystemExit("template has unfilled slots")
    return text


def run_guards(root, d):
    results = []
    data_dir = os.path.join(root, "skills", "building-tnr-content", "data")

    def run(name, command, cwd):
        proc = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
        tail = (proc.stdout.strip().splitlines() or ["(no output)"])[-1]
        results.append((name, proc.returncode, tail))

    run("lawmap", ["python3", os.path.join(HERE, "lawmap.py"), root], root)
    run("doctrine projections", ["python3", os.path.join(HERE, "render_doctrine.py"), "--check"], root)
    run("packs/TOCs", ["python3", os.path.join(HERE, "build_packs.py"), "--check"], root)

    in_progress = (d.get("in_progress") or {}).get("file")
    if in_progress and os.path.exists(os.path.join(root, in_progress)):
        run(
            "validate " + in_progress,
            ["python3", os.path.join(HERE, "validate.py"), os.path.join(root, in_progress)],
            data_dir,
        )

    bundles = sorted(glob.glob(os.path.join(root, "harvests", "inbox", "*.json")))
    if bundles:
        bundle = bundles[-1]
        run(
            "parity " + os.path.basename(bundle),
            ["python3", os.path.join(HERE, "validate.py"), "--parity", bundle],
            data_dir,
        )

    d["verified_at_close"] = [
        "%s -> %s%s" % (name, tail, "" if code == 0 else " (EXIT %d)" % code)
        for name, code, tail in results
    ]
    return [name for name, code, _ in results if code != 0]


def write_verified(path, text):
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(text)
    if open(path, encoding="utf-8").read() != text:
        raise OSError(f"{path} did not read back byte-equal")


def close(root, guards=False):
    digest_path, status_path, context_path, template_path = paths(root)
    digest = json.load(open(digest_path, encoding="utf-8"))
    digest["generated"] = time.strftime("%Y-%m-%d")

    if guards:
        failures = run_guards(root, digest)
        if failures:
            print("GUARDS RED: %s - fix before closing" % ", ".join(failures))
            for line in digest["verified_at_close"]:
                print("  " + line)
            return 1

    rendered = {
        digest_path: json.dumps(digest, indent=2, ensure_ascii=False) + "\n",
        status_path: render_status(digest),
        context_path: render_context(digest, template_path),
    }
    try:
        for path, text in rendered.items():
            write_verified(path, text)
    except OSError as error:
        print("CLOSE FAILED: " + str(error))
        return 1

    ledger = digest.get("token_ledger") or []
    print(digest.get("state_line", "(no state line)"))
    print(
        "closed: 3 file(s) projected + byte-verified; ledger %d read(s), %d bytes"
        % (len(ledger), sum(item.get("bytes", 0) for item in ledger))
    )
    return 0


def selftest():
    with tempfile.TemporaryDirectory() as root:
        os.makedirs(os.path.join(root, "state"))
        os.makedirs(os.path.join(root, "docs"))
        with open(os.path.join(root, "docs", "active_context.tmpl"), "w", encoding="utf-8") as handle:
            handle.write(
                "# ctx\n{{state_line}}\n{{verified_at_close}}\n{{in_progress}}\n"
                "{{open_by_owner}}\n{{rulings_open}}\n{{next}}\n"
            )
        digest = {
            "state_line": "test state",
            "verified_at_close": ["g -> ok"],
            "in_progress": {"wave": "t"},
            "open_by_owner": {"x": ["y"]},
            "rulings_open": [],
            "next": "n",
            "token_ledger": [],
            "deployed": [],
            "decisions": [],
            "board": {},
        }
        with open(os.path.join(root, "state", "digest.json"), "w", encoding="utf-8") as handle:
            json.dump(digest, handle)
        if close(root) != 0:
            print("selftest FAIL")
            return 1
        print("selftest OK")
        return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(selftest())
    raise SystemExit(close(ROOT, guards="--guards" in sys.argv))
