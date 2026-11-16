"""A finished fight's files, pushed to main so they outlive the container (AP test 2026-11-16, finding F8: both
fights' logs, states and post-mortems were written in the play session's checkout and lost with it; the game keeps
the log for a while, but nothing kept it for us).

    python3 -m player.keep BATTLE_ID        commit what exists of that fight's files to origin/main; one JSON line

What is kept, under state/player/<account>/fights/: <bid>_entries.json, <bid>_meta.json, live_states/<bid>.json,
live_states/<bid>.full.jsonl.gz, live_states/<bid>.plans.jsonl.gz (every planner run's choice and candidates). Not the post-mortem: it is still being written when the fight closes, and it is
made again from the log (tools/postmortem.py -- <bid>). A path outside the fights folder is refused.

How: as forge/tools/run_lock.mjs writes the lock. One commit on origin/main built in a private index from the
fetched main, so the working tree, its branch and its index are never touched; a plain fast-forward push; if main
moved, fetch and build again (4 tries). Files equal to main's are left out, and a fight with nothing new makes no
commit. The play session's checkout can push to main already (the run lock needs it, player/OPERATOR.md).

KEEP_REPO, KEEP_REMOTE, KEEP_BRANCH point it elsewhere (the tests use a local bare repository).
"""
import json
import os
import subprocess
import sys
import tempfile

from . import config as C

REPO = os.environ.get("KEEP_REPO") or C.ROOT
REMOTE = os.environ.get("KEEP_REMOTE") or "origin"
BRANCH = os.environ.get("KEEP_BRANCH") or "main"
TRIES = 4


def fight_files(bid, fights=None):
    """The fight's files that exist, as absolute paths."""
    fights = fights or C.fights_dir()
    names = [f"{bid}_entries.json", f"{bid}_meta.json", os.path.join("live_states", f"{bid}.json"),
             os.path.join("live_states", f"{bid}.full.jsonl.gz"), os.path.join("live_states", f"{bid}.plans.jsonl.gz")]
    return [p for p in (os.path.join(fights, n) for n in names) if os.path.isfile(p)]


def _git(args, env=None, data=None):
    return subprocess.run(["git", "-C", REPO, *args], input=data, capture_output=True, check=True,
                          env=env).stdout


def _rel(path):
    rel = os.path.relpath(os.path.abspath(path), REPO).replace(os.sep, "/")
    if rel.startswith("../") or not rel.startswith(f"state/player/{C.ACCOUNT}/fights/"):
        raise ValueError(f"not a fight file of this account: {rel}")
    return rel


def _commit(base, files, message):
    """One commit on top of base with these files, or None when all of them already match base."""
    with tempfile.TemporaryDirectory(prefix="keep-") as tmp:
        env = dict(os.environ, GIT_INDEX_FILE=os.path.join(tmp, "index"))
        _git(["read-tree", base], env=env)
        changed = False
        for rel, path in files:
            with open(path, "rb") as f:
                blob = _git(["hash-object", "-w", "--stdin"], data=f.read()).decode().strip()
            try:
                old = _git(["rev-parse", f"{base}:{rel}"]).decode().strip()
            except subprocess.CalledProcessError:
                old = None
            if old != blob:
                changed = True
                _git(["update-index", "--add", "--cacheinfo", f"100644,{blob},{rel}"], env=env)
        if not changed:
            return None
        tree = _git(["write-tree"], env=env).decode().strip()
        return _git(["commit-tree", tree, "-p", base, "-m", message], env=env).decode().strip()


def keep(bid, paths=None):
    """Push the fight's files to main. {"kept": [paths], "commit": sha or None} or {"error": text}."""
    paths = fight_files(bid) if paths is None else paths
    if not paths:
        return {"kept": [], "commit": None, "note": "no files for this fight"}
    try:
        files = [(_rel(p), p) for p in paths]
    except ValueError as err:
        return {"error": str(err)}
    last = None
    for _ in range(TRIES):
        try:
            _git(["fetch", "-q", REMOTE, BRANCH])
            base = _git(["rev-parse", "FETCH_HEAD"]).decode().strip()
            sha = _commit(base, files, f"fight log {bid} (player: kept at the fight's end)")
            if sha is None:
                return {"kept": [r for r, _ in files], "commit": None, "note": "already on main"}
            _git(["push", "-q", REMOTE, f"{sha}:refs/heads/{BRANCH}"])
            return {"kept": [r for r, _ in files], "commit": sha}
        except subprocess.CalledProcessError as err:
            last = (err.stderr or b"").decode(errors="replace").strip() or str(err)
    return {"error": f"could not push after {TRIES} tries: {last}"[:400]}


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print(json.dumps({"error": "usage: python3 -m player.keep BATTLE_ID"}))
        return 2
    out = keep(argv[0])
    print(json.dumps(dict(out, battle=argv[0])))
    return 1 if "error" in out else 0


if __name__ == "__main__":
    sys.exit(main())
