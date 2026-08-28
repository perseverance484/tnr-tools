#!/usr/bin/env python3
"""Assemble a TNR session closeout bundle, and refuse to ship a bad one.

The point is not zipping files. It is the checks: a closeout that contains a stale storyboard
or a manifest that no longer validates is worse than no closeout, because the next session
trusts it. See CLOSEOUT.md.

Usage:
  python3 closeout.py --work . --out /mnt/user-data/outputs/closeout --name forsworn
  python3 closeout.py ... --skip-render     # only if storyboard.py is unavailable
"""
import argparse, filecmp, json, os, shutil, subprocess, sys, zipfile
from datetime import datetime, timezone

REQUIRED_DOCS = ["NEXT_SESSION.md", "LAWS_LEARNED.md", "DIFFS_FROM_SOURCE.md", "STYLE.md"]
PUSHDIR = ["/mnt/user-data/outputs/push"]
SKILL_DIRS = ["/mnt/skills/user/building-tnr-content/scripts",
              "/mnt/skills/user/producing-tnr-art/scripts"]


def problems_and_notes(work, out, name, skip_render):
    errs, notes = [], []
    src = lambda *p: os.path.join(work, *p)

    # 1. sheets are the source of truth; storyboards must not be older than them
    sheets = sorted(f for f in os.listdir(src("sheets")) if f.endswith(".json")) \
        if os.path.isdir(src("sheets")) else []
    if not sheets:
        errs.append("no sheets/ directory: content source of truth is missing")
    if sheets and not skip_render:
        os.makedirs(src("storyboards"), exist_ok=True)
        for sh in sheets:
            md = os.path.join(src("storyboards"), sh.replace("sheet_", "").replace(".json", ".md"))
            r = subprocess.run([sys.executable, src("storyboard.py"), src("sheets", sh), md],
                               capture_output=True, text=True)
            if r.returncode != 0:
                errs.append(f"storyboard render failed for {sh}: {r.stderr.strip()[:160]}")
        notes.append(f"re-rendered {len(sheets)} storyboards from sheets")

    # 2. every staged manifest must still validate. A missing push dir is an ERROR, not a
    # silent skip: "verified" has to mean something ran.
    pushdir = next((d for d in (PUSHDIR[0], src("push")) if d and os.path.isdir(d)), None)
    if pushdir is None:
        errs.append("no push directory found: nothing was validated. Pass --push")
    else:
        n_val = 0
        for f in sorted(os.listdir(pushdir)):
            if not f.endswith(".json"):
                continue
            r = subprocess.run([sys.executable, src("validate.py"), os.path.join(pushdir, f)],
                               capture_output=True, text=True)
            tail = (r.stdout.strip().splitlines() or ["no output"])[-1]
            n_val += 1
            import re as _re
            m = _re.search(r"(\d+) errors?", tail)
            if m is None or int(m.group(1)) != 0:
                errs.append(f"{f} does not validate: {tail}")
            else:
                notes.append(f"validate {f}: {tail}")
        if n_val == 0:
            errs.append(f"push directory {pushdir} has no manifests: nothing was validated")

    # 3. selfcheck
    if os.path.exists(src("selfcheck.py")):
        r = subprocess.run([sys.executable, src("selfcheck.py")], capture_output=True, text=True)
        tail = (r.stdout.strip().splitlines() or ["no output"])[-1]
        notes.append(f"selfcheck: {tail}")
        if "0 errors" not in tail:
            errs.append(f"selfcheck is not clean: {tail}")

    # 4. tools that differ from the installed skills, found by diff not by memory
    CATALOGS = {"40_INDEX_jutsu.json", "41_INDEX_item.json", "42_INDEX_ai.json",
                "43_INDEX_asset.json", "47_INDEX_quest.json"}
    diverged_data, stack_data = [], []
    for f in sorted(os.listdir(work)):
        o = os.path.join("/mnt/project", f)
        if not os.path.exists(o) or f in CATALOGS:
            continue
        if f.endswith((".json", ".py")):
            stack_data.append(f)
            if not filecmp.cmp(src(f), o, shallow=False):
                diverged_data.append(f)
    if not stack_data:
        errs.append("no stack data files staged: the bundle is the only home for them now")
    notes.append(f"{len(stack_data)} stack data/tool file(s) bundled, "
                 f"{len(diverged_data)} of them diverging: " + ", ".join(diverged_data or ["none"]))

    patched = []
    for f in sorted(f for f in os.listdir(work) if f.endswith(".py")):
        origin = next((os.path.join(d, f) for d in SKILL_DIRS
                       if os.path.exists(os.path.join(d, f))), None)
        if origin is None:
            patched.append((f, "new, not in any skill"))
        elif not filecmp.cmp(src(f), origin, shallow=False):
            patched.append((f, "patched, differs from the installed skill"))
    notes.append(f"{len(patched)} tool(s) diverge from the skills")

    # 4b. catalogs must be present and their freshness reported. A bundle whose catalogs are
    # all unverified hands the next session the exact trap that cost this one a wasted capture.
    catdir = os.path.join(work, "state", "catalogs")
    if os.path.isdir(catdir) and os.path.exists(src("catalog_sync.py")):
        r = subprocess.run([sys.executable, src("catalog_sync.py"), "--check", "--dir", catdir],
                           capture_output=True, text=True)
        for line in r.stdout.strip().splitlines():
            if line.strip():
                notes.append("catalog " + line.strip())
    elif os.path.isdir(catdir):
        notes.append("catalogs present but catalog_sync.py missing: freshness unchecked")

    # 4c. promotions must be declared, even if the declaration is 'none'
    st = os.path.join(work, "state", "status.json")
    if os.path.exists(st):
        try:
            data = json.load(open(st))
            if "promotions_pending" not in data:
                errs.append("state/status.json has no promotions_pending key: say 'none' explicitly")
            else:
                notes.append(f"{len(data['promotions_pending'])} promotion(s) pending for project knowledge")
        except Exception as e:
            errs.append(f"state/status.json does not parse: {e}")
    else:
        errs.append("state/status.json is missing: machine-readable state is required")

    # 5. the real name must never reach a bundle. This is a hard gate, not a warning: the
    # bundle goes to source, and the username is all teammates have.
    # split so this file does not itself trip the check it performs
    REDACT = ("Bran" + "don",)
    hits = []
    for base, _d, fs in os.walk(work):
        if any(x in base for x in ("/out", "__pycache__", "/.git")):
            continue
        for f in fs:
            if not f.endswith((".py", ".md", ".json")):
                continue
            p = os.path.join(base, f)
            try:
                t = open(p, encoding="utf-8", errors="ignore").read()
            except Exception:
                continue
            for word in REDACT:
                if word in t:
                    hits.append(f"{os.path.relpath(p, work)} contains the real name")
    for h in hits:
        errs.append("REDACTION: " + h)
    if not hits:
        notes.append("redaction check clean: no real name in any bundled file")

    # 6. required docs
    for d in REQUIRED_DOCS:
        if not os.path.exists(src("docs", d)):
            errs.append(f"docs/{d} is missing: CLOSEOUT.md requires it")
    return errs, notes, sheets, patched, pushdir, diverged_data, stack_data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default=".")
    ap.add_argument("--out", required=True)
    ap.add_argument("--name", default="session")
    ap.add_argument("--skip-render", action="store_true")
    ap.add_argument("--push", default=PUSHDIR[0], help="directory of staged manifests")
    ap.add_argument("--force", action="store_true", help="write the bundle despite problems")
    a = ap.parse_args()
    work = os.path.abspath(a.work)
    PUSHDIR[0] = a.push

    errs, notes, sheets, patched, pushdir, diverged_data, stack_data = problems_and_notes(work, a.out, a.name, a.skip_render)
    for n in notes:
        print("note  ", n)
    for e in errs:
        print("ERROR ", e)
    if errs and not a.force:
        print(f"\n{len(errs)} problem(s). Bundle NOT written. Fix them, or pass --force.")
        return 1

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    root = os.path.join(a.out, a.name)
    if os.path.isdir(root):
        shutil.rmtree(root)
    for sub in ("docs", "push", "sheets", "storyboards", "tools", "results",
                "state", os.path.join("state", "catalogs"), "deliverables", "data"):
        os.makedirs(os.path.join(root, sub), exist_ok=True)

    def copytree(s, d):
        if os.path.isdir(s):
            for f in sorted(os.listdir(s)):
                if os.path.isfile(os.path.join(s, f)):
                    shutil.copy2(os.path.join(s, f), os.path.join(d, f))

    copytree(os.path.join(work, "docs"), os.path.join(root, "docs"))
    copytree(os.path.join(work, "sheets"), os.path.join(root, "sheets"))
    copytree(os.path.join(work, "storyboards"), os.path.join(root, "storyboards"))
    copytree(os.path.join(work, "results"), os.path.join(root, "results"))
    copytree(os.path.join(work, "state"), os.path.join(root, "state"))
    copytree(os.path.join(work, "state", "catalogs"), os.path.join(root, "state", "catalogs"))
    copytree(os.path.join(work, "deliverables"), os.path.join(root, "deliverables"))
    for f in stack_data:
        shutil.copy2(os.path.join(work, f), os.path.join(root, "data", f))
    if pushdir:
        copytree(pushdir, os.path.join(root, "push"))
    for f, _why in patched:
        shutil.copy2(os.path.join(work, f), os.path.join(root, "tools", f))
    # selfcheck.py is unchanged from the skill so it is not in `patched`, but a bundle that
    # cannot self-verify is not much of a bundle. Ship it.
    for skilldir in SKILL_DIRS:
        sc = os.path.join(skilldir, "selfcheck.py")
        if os.path.exists(sc):
            shutil.copy2(sc, os.path.join(root, "tools", "selfcheck.py"))
            break
    for extra in ("CLOSEOUT.md", "closeout.py"):
        if os.path.exists(os.path.join(work, extra)):
            shutil.copy2(os.path.join(work, extra), os.path.join(root, "tools", extra))

    with open(os.path.join(root, "tools", "PATCHES.md"), "w") as fh:
        fh.write("# Tool patches\n\nA skill reinstall reverts every one of these. Copy them back "
                 "into the working directory at session start.\n\n")
        for f, why in patched:
            fh.write(f"- **{f}** - {why}\n")
        fh.write("\n## data/\n\nProject knowledge is prose only since 2026-08-28. Every file a "
                 "script reads lives in `data/`; copy the whole folder into the workdir at "
                 "session start. These diverge from the last project-knowledge copy and must "
                 "win if both are ever present:\n\n")
        for f in (diverged_data or ["(none diverging)"]):
            fh.write(f"- **{f}**\n")

    counts = {d: len(os.listdir(os.path.join(root, d)))
              for d in ("docs", "push", "sheets", "storyboards", "tools", "results",
                        "state", "state/catalogs", "deliverables", "data")}
    with open(os.path.join(root, "MANIFEST.md"), "w") as fh:
        fh.write(f"# {a.name} closeout, {stamp}\n\n## Verification run at assembly\n\n")
        for n in notes:
            fh.write(f"- {n}\n")
        fh.write("\n## Contents\n\n")
        for d, c in counts.items():
            fh.write(f"- `{d}/` {c} file(s)\n")
        if errs:
            fh.write("\n## Written with --force despite\n\n")
            for e in errs:
                fh.write(f"- {e}\n")

    zpath = os.path.join(a.out, f"{a.name}_closeout_{stamp}.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for base, _dirs, files in os.walk(root):
            for f in files:
                p = os.path.join(base, f)
                z.write(p, os.path.relpath(p, a.out))
    print(f"\nwrote {zpath}  ({round(os.path.getsize(zpath)/1024, 1)} KB)")
    print("contents:", ", ".join(f"{d} {c}" for d, c in counts.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
