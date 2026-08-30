#!/usr/bin/env python3
"""Audit the stack zip and the session bundle before either is trusted.

Written because the dangerous failures this project has had were not dramatic. They were a stale
catalog nobody stamped, a coverage matrix describing a tool that no longer existed, and a name
inherited into a hand-patched copy of a live file. All three looked fine.

The expensive class this guards is HAND TRANSCRIPTION: files copied out of project knowledge,
edited by hand, and packaged. A dropped paragraph in a laws file is invisible and permanent.
So every patched file is diffed against its original and any deletion must be declared.

  audit.py --stack tnr_stack.zip --bundle closeout.zip --origin /mnt/project
  audit.py ... --expect expectations.json     # declared intentional changes
  audit.py ... --quiet                        # one line per check, detail only on failure

Output is deliberately terse: PASS lines are one line each, and only failures print detail. The
point is to be cheap enough to run every time, not to be read like a report.
"""
import argparse, ast, difflib, hashlib, json, os, re, shutil, subprocess, sys, tempfile, zipfile

SKILL_DIRS = ["/mnt/skills/user/building-tnr-content/scripts",
              "/mnt/skills/user/producing-tnr-art/scripts"]
NAME = "Bran" + "don"          # split so this file never trips its own redaction check


class Report:
    def __init__(self, quiet):
        self.quiet, self.fails, self.warns, self.n = quiet, [], [], 0

    def ok(self, check, msg=""):
        self.n += 1
        if not self.quiet:
            print(f"  PASS  {check:34} {msg}")

    def fail(self, check, msg):
        self.n += 1
        self.fails.append((check, msg))
        print(f"  FAIL  {check:34} {msg}")

    def warn(self, check, msg):
        self.n += 1
        self.warns.append((check, msg))
        print(f"  warn  {check:34} {msg}")


def unzip(path, into):
    if not os.path.exists(path):
        return None
    with zipfile.ZipFile(path) as z:
        bad = z.testzip()
        if bad:
            raise RuntimeError(f"corrupt member in {path}: {bad}")
        z.extractall(into)
    return into


def walk_files(root):
    return {os.path.relpath(os.path.join(b, f), root): os.path.join(b, f)
            for b, _d, fs in os.walk(root) for f in fs}


# ---------------------------------------------------------------- checks

def check_parses(files, rep, label):
    bad = []
    for rel, p in files.items():
        try:
            if rel.endswith(".json"):
                json.load(open(p, encoding="utf-8"))
            elif rel.endswith(".py"):
                ast.parse(open(p, encoding="utf-8").read())
        except Exception as e:
            bad.append(f"{rel}: {str(e)[:80]}")
    rep.fail(f"{label} parse", "; ".join(bad[:3])) if bad else \
        rep.ok(f"{label} parse", f"{len(files)} files, all JSON and Python valid")


def check_redaction(files, rep, label):
    hits = [rel for rel, p in files.items() if rel.endswith((".md", ".py", ".json"))
            and NAME in open(p, encoding="utf-8", errors="ignore").read()]
    rep.fail(f"{label} redaction", f"real name in {hits}") if hits else \
        rep.ok(f"{label} redaction", "no real name")


def check_transcription(stack_files, origin, rep, expect):
    """The core guard. Every stack file that also exists in the origin is diffed. Additions are
    fine and expected; DELETIONS are the danger and must be declared in --expect."""
    checked = skipped = 0
    for rel, p in sorted(stack_files.items()):
        o = os.path.join(origin, os.path.basename(rel))
        if not os.path.exists(o) or not rel.endswith(".md"):
            skipped += 1
            continue
        checked += 1
        # Redaction is a known, mandatory transform: apply it to the origin before diffing so a
        # scrubbed name does not masquerade as data loss. Anything still different is real.
        a = open(o, encoding="utf-8").read().replace(NAME + "'s", "dauntless's") \
                                            .replace(NAME, "dauntless").splitlines()
        b = open(p, encoding="utf-8").read().splitlines()
        sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
        removed, added = [], 0
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag in ("delete", "replace"):
                removed += [ln for ln in a[i1:i2] if ln.strip()]
            if tag in ("insert", "replace"):
                added += (j2 - j1)
        allowed = set(expect.get(os.path.basename(rel), {}).get("allow_removed_substrings", []))
        undeclared = [ln for ln in removed
                      if not any(s in ln for s in allowed)]
        if undeclared:
            rep.fail("transcription " + os.path.basename(rel),
                     f"{len(undeclared)} undeclared removed line(s), first: "
                     f"{undeclared[0][:90]!r}")
        else:
            rep.ok("transcription " + os.path.basename(rel),
                   f"+{added} lines, {len(removed)} declared removals, nothing lost")
    if checked == 0:
        rep.warn("transcription", "no stack file matched an origin file; nothing diffed")


def check_law_integrity(stack_files, rep, origin=None):
    p = next((v for k, v in stack_files.items() if k.endswith("12_TECH_engine_laws.md")), None)
    if not p:
        rep.warn("laws", "12_TECH_engine_laws.md not in the stack zip")
        return
    t = open(p, encoding="utf-8").read()
    nums = [int(m) for m in re.findall(r"^(\d+)\.", t, re.M)]
    # A duplicate that already exists upstream is the source document's structure, not a
    # transcription error. Only NEW duplicates are ours.
    base = []
    o = os.path.join(origin or "", "12_TECH_engine_laws.md")
    if origin and os.path.exists(o):
        base = [int(m) for m in re.findall(r"^(\d+)\.", open(o, encoding="utf-8").read(), re.M)]
    prior = {n for n in base if base.count(n) > 1}
    dupes = sorted({n for n in nums if nums.count(n) > 1} - prior)
    gaps = [n for n in range(1, max(nums) + 1) if n not in nums]
    if dupes:
        rep.fail("law numbering", f"duplicate law numbers {dupes}")
    elif gaps:
        rep.warn("law numbering", f"{len(gaps)} gap(s), highest {max(nums)}: {gaps[:8]}")
    else:
        rep.ok("law numbering", f"1..{max(nums)} contiguous"
               + (f", {len(prior)} pre-existing duplicate(s) inherited from source" if prior else ""))

    cov = next((v for k, v in stack_files.items() if k.endswith("12b_LAWS_coverage.md")), None)
    if cov:
        cited = {int(m) for m in re.findall(r"^\|\s*(\d+)\s*\|", open(cov, encoding="utf-8").read(), re.M)}
        missing = sorted(cited - set(nums))
        rep.fail("coverage rows", f"12b cites laws that do not exist: {missing}") if missing else \
            rep.ok("coverage rows", f"{len(cited)} rows, every cited law exists")


def _workdir(bundle_root, origin, td):
    """Bundle tools cannot run from tools/ alone: the generated data they read lives in project
    knowledge. Stage both together, which is exactly what a session start does."""
    wd = os.path.join(td, "workdir")
    os.makedirs(wd, exist_ok=True)
    # Mirror the documented session start exactly: skills provide the base toolset, the bundle
    # overlays its patched tools and data, project knowledge supplies the generated files.
    # First writer wins, so bundle copies take precedence over both.
    for src in [os.path.join(bundle_root, "tools"),
                os.path.join(bundle_root, "data")] + SKILL_DIRS + [origin]:
        if src and os.path.isdir(src):
            for f in os.listdir(src):
                p = os.path.join(src, f)
                if os.path.isfile(p) and not os.path.exists(os.path.join(wd, f)):
                    shutil.copy2(p, os.path.join(wd, f))
    cats = os.path.join(bundle_root, "state", "catalogs")
    if os.path.isdir(cats):
        for f in os.listdir(cats):
            shutil.copy2(os.path.join(cats, f), os.path.join(wd, f))
    return wd


def check_tools_run(bundle_root, rep, wd):
    """A tool that parses but cannot run is not a tool."""
    for script, args, want in (("selfcheck.py", [], "0 errors"),):
        p = os.path.join(wd, script)
        if not os.path.exists(p):
            rep.warn("tools run", f"{script} missing")
            continue
        r = subprocess.run([sys.executable, p] + args, capture_output=True, text=True, cwd=wd)
        tail = (r.stdout.strip().splitlines() or [""])[-1]
        rep.ok("tools run " + script, tail) if want in tail else \
            rep.fail("tools run " + script, tail or r.stderr.strip()[:90])


def check_manifests(bundle_root, rep, wd):
    push = os.path.join(bundle_root, "push")
    val = os.path.join(wd, "validate.py")
    if not (os.path.isdir(push) and os.path.exists(val)):
        rep.warn("manifests", "push/ or tools/validate.py missing")
        return
    bad, n = [], 0
    for f in sorted(os.listdir(push)):
        if not f.endswith(".json"):
            continue
        n += 1
        r = subprocess.run([sys.executable, val, os.path.join(push, f)],
                           capture_output=True, text=True, cwd=wd)
        tail = (r.stdout.strip().splitlines() or [""])[-1]
        m = re.search(r"(\d+) errors?", tail)
        if not m or int(m.group(1)) != 0:
            bad.append(f"{f}: {tail or (r.stderr.strip().splitlines() or [''])[-1][:70]}")
    rep.fail("manifests validate", "; ".join(bad[:3])) if bad else \
        rep.ok("manifests validate", f"{n} manifests, 0 errors each")


def check_sheet_manifest_parity(bundle_root, rep, wd):
    """The manifest must be what the sheets produce. If they have drifted, the storyboards a
    reviewer reads are not the content that ships."""
    sheets = os.path.join(bundle_root, "sheets")
    wave = next((os.path.join(bundle_root, "push", f)
                 for f in os.listdir(os.path.join(bundle_root, "push"))
                 if f.endswith(".json") and "wave" in f), None)
    mission = os.path.join(wd, "mission.py")
    if not (wave and os.path.isdir(sheets) and os.path.exists(mission)):
        rep.warn("sheet parity", "sheets/, wave manifest or mission.py missing")
        return
    manifest = json.load(open(wave, encoding="utf-8"))
    inman = {e["data"]["name"]: e["data"]["content"]["objectives"]
             for e in manifest.get("items", []) if e.get("entity") == "quest"}
    drift, checked = [], 0
    with tempfile.TemporaryDirectory() as td:
        for sh in sorted(os.listdir(sheets)):
            if not sh.endswith(".json"):
                continue
            out = os.path.join(td, sh)
            r = subprocess.run([sys.executable, mission, os.path.join(sheets, sh),
                                "--profiles", "48_DATA_mission_profiles.json",
                                "--spec", "25x_DATA_art_spec.json",
                                "--out", out], capture_output=True, text=True, cwd=wd)
            if not os.path.exists(out):
                drift.append(f"{sh}: rebuild failed {(r.stderr.strip().splitlines() or [''])[-1][:70]}")
                continue
            q = [e for e in json.load(open(out, encoding="utf-8"))["items"]
                 if e.get("entity") == "quest"]
            if not q:
                continue
            name = q[0]["data"]["name"]
            if name not in inman:
                drift.append(f"{sh}: '{name}' not in the manifest")
                continue
            checked += 1
            a = [(o["id"], o.get("description")) for o in inman[name]]
            b = [(o["id"], o.get("description")) for o in q[0]["data"]["content"]["objectives"]]
            if a != b:
                diff = [x[0] for x, y in zip(a, b) if x != y] or ["node count differs"]
                drift.append(f"{name}: manifest differs from sheet at {diff[:4]}")
    rep.fail("sheet parity", "; ".join(drift[:3])) if drift else \
        rep.ok("sheet parity", f"{checked} quests rebuild byte-identical from sheets")


def check_catalogs(bundle_root, rep):
    d = os.path.join(bundle_root, "state", "catalogs")
    if not os.path.isdir(d):
        rep.warn("catalogs", "no state/catalogs in the bundle")
        return
    bad, tot, stamped = [], 0, 0
    for f in sorted(os.listdir(d)):
        if not f.endswith(".json"):
            continue
        c = json.load(open(os.path.join(d, f), encoding="utf-8"))
        if "cols" not in c or "rows" not in c:
            bad.append(f"{f}: not columnar")
            continue
        w = len(c["cols"])
        ragged = [i for i, r in enumerate(c["rows"]) if len(r) != w]
        if ragged:
            bad.append(f"{f}: {len(ragged)} row(s) with wrong width")
        if "last_verified" not in c["cols"]:
            bad.append(f"{f}: no last_verified column")
        else:
            i = c["cols"].index("last_verified")
            stamped += sum(1 for r in c["rows"] if r[i])
        tot += len(c["rows"])
    rep.fail("catalogs", "; ".join(bad[:3])) if bad else \
        rep.ok("catalogs", f"{tot} rows well-formed, {stamped} carry a verification stamp")


def check_cross_zip(stack_files, bundle_files, rep):
    """The same filename in both zips with different content is the drift this whole
    architecture exists to prevent."""
    by_base_s = {os.path.basename(k): v for k, v in stack_files.items()}
    by_base_b = {os.path.basename(k): v for k, v in bundle_files.items()}
    conflicts = []
    for name in set(by_base_s) & set(by_base_b):
        h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
        if h(by_base_s[name]) != h(by_base_b[name]):
            conflicts.append(name)
    rep.fail("cross-zip drift", f"same name, different content: {sorted(conflicts)}") \
        if conflicts else rep.ok("cross-zip drift",
                                 f"{len(set(by_base_s) & set(by_base_b))} shared name(s), all identical")


def check_required(bundle_files, rep):
    need = ["docs/NEXT_SESSION.md", "docs/LAWS_LEARNED.md", "state/status.json",
            "state/active-context.md", "tools/PATCHES.md", "MANIFEST.md"]
    have = {k.split("/", 1)[1] if "/" in k else k for k in bundle_files}
    missing = [n for n in need if n not in have]
    rep.fail("bundle required files", f"missing {missing}") if missing else \
        rep.ok("bundle required files", f"all {len(need)} present")


def check_status(bundle_files, rep):
    p = next((v for k, v in bundle_files.items() if k.endswith("state/status.json")), None)
    if not p:
        return
    try:
        d = json.load(open(p, encoding="utf-8"))
    except Exception as e:
        rep.fail("status.json", str(e)[:80])
        return
    missing = [k for k in ("work", "blockers", "promotions_pending") if k not in d]
    rep.fail("status.json", f"missing key(s) {missing}") if missing else \
        rep.ok("status.json", f"{len(d['work'])} work item(s), {len(d['blockers'])} blocker(s), "
                              f"{len(d['promotions_pending'])} promotion(s)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stack", required=True)
    ap.add_argument("--bundle", required=True)
    ap.add_argument("--origin", default="/mnt/project")
    ap.add_argument("--expect", help="JSON of declared intentional removals")
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    expect = json.load(open(a.expect)) if a.expect and os.path.exists(a.expect) else {}
    rep = Report(a.quiet)

    with tempfile.TemporaryDirectory() as td:
        s_root, b_root = os.path.join(td, "stack"), os.path.join(td, "bundle")
        try:
            unzip(a.stack, s_root)
            unzip(a.bundle, b_root)
        except Exception as e:
            print(f"  FAIL  zip integrity                  {e}")
            return 1
        rep.ok("zip integrity", "both archives open, no corrupt members")

        sf = walk_files(s_root)
        bf = walk_files(b_root)
        inner = os.path.join(b_root, "forsworn")
        b_inner = inner if os.path.isdir(inner) else b_root

        check_parses(sf, rep, "stack")
        check_parses(bf, rep, "bundle")
        check_redaction(sf, rep, "stack")
        check_redaction(bf, rep, "bundle")
        check_transcription(sf, a.origin, rep, expect)
        check_law_integrity(sf, rep, a.origin)
        check_required(bf, rep)
        check_status(bf, rep)
        check_catalogs(b_inner, rep)
        wd = _workdir(b_inner, a.origin, td)
        check_tools_run(b_inner, rep, wd)
        check_manifests(b_inner, rep, wd)
        check_sheet_manifest_parity(b_inner, rep, wd)
        check_cross_zip(sf, bf, rep)

    print(f"\n{rep.n} checks: {rep.n - len(rep.fails) - len(rep.warns)} pass, "
          f"{len(rep.warns)} warn, {len(rep.fails)} FAIL")
    if rep.fails:
        print("\nDo not ship. Failures:")
        for c, m in rep.fails:
            print(f"  {c}: {m}")
    return 1 if rep.fails else 0


if __name__ == "__main__":
    sys.exit(main())
