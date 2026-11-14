"""Before the first live session on a machine: are the hooks of the relay's agent file run here?
(RUL-2026-11-14-160, point 1; PROOF.md, "The agent file's own hooks, and trust".)

    python3 docs/reviews/evidence/ai_player_hook_relay/preflight.py [OUT] [--form main|subagent]
            [--hooks settings] [--bare-env]

Run it from a terminal in the repository's root, on the machine and in the folder the relay will be started
in. It starts the relay's agent as it is in this folder (.claude/agents/tnr-relay.md), once as a session's
main agent and once as a subagent of one. Each is a relay of three batches against the stand-in for the game's
connector (fake_connector.py), about half a minute.

It makes no request of the game, and it does not rest on one thing for that:

- each session is given one MCP server, the stand-in, and told to load no other (--strict-mcp-config);
- before any relay is started, a session that may call nothing is asked which MCP servers and tools it has.
  The stand-in has one tool and the game's connector has several, so a connector that had taken the
  stand-in's name would show. Anything but the stand-in, and nothing is started;
- a relay's session is ended at once if its first event lists anything else, and again if a call that a hook
  released is not in the stand-in's log within two seconds;
- the brain behind the relay is a rehearsal in a folder of the run's own, in guard mode. It asks for nothing
  but reads of my own profile, and the session is ended from outside, so no other call is ever released.

So if every one of those failed together, what would have reached the game is a read of my own profile.

For each form it prints whether the agent file's hooks ran, and it ends with 0 only when they ran in every
form it was asked for. Where Claude Code skipped them because the folder's trust dialog has not been accepted,
it says so: open Claude Code in this folder once, accept the dialog, and run this again. Do not start a live
session while it says no: a relay without its hooks is not the relay that was proven.

--hooks settings: the hooks are given on the command line, not read from the agent file. That shows nothing
about the machine. It is for trying this check where nobody can accept the dialog. --bare-env: the sessions
are started with a path, a home and the proxy's variables only, not with the terminal's own: the cloud session
this was built in needs that.
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TRUST = ("Claude Code skipped the agent file's hooks: this folder's trust dialog has not been accepted. Open "
         "Claude Code in this folder once, accept it, and run this again")


def proof(*args):
    env = [] if "--bare-env" in sys.argv else ["--own-env"]
    return subprocess.run([sys.executable, os.path.join(HERE, "proof.py"), *args, *env], capture_output=True, text=True)


def rows(path):
    try:
        with open(path, encoding="utf8") as f:
            return [json.loads(x) for x in f if x.strip().startswith("{")]
    except OSError:
        return []


def form(out, name, hooks):
    """One relay in one form. -> (the agent file's hooks ran for every call, what is printed of it)."""
    done = proof(out, "--hooks", hooks, "--mode", "guard", "--end", "kill", "--batches", "3", "--seconds",
                 "150", *(["--as-subagent"] if name == "subagent" else []))
    ended = next((s["ended"] for s in rows_of(done.stdout) if "ended" in s), None)
    log = rows(os.path.join(out, "live", "hook", "log.jsonl"))
    game = [g for g in rows(os.path.join(out, "game.jsonl")) if g.get("at") == "came"]
    passed = {k: sum(1 for h in log if h["hook"] == k and not h.get("refused")) for k in ("bash", "pre", "post")}
    try:
        with open(os.path.join(out, "debug.log"), encoding="utf8", errors="replace") as f:
            skipped = "Skipping frontmatter hooks" in f.read()
    except OSError:
        skipped = False
    ran = (not ended and all(passed.values()) and 0 < len(game) <= passed["pre"]
           and {g["endpoint"] for g in game} == {"profile.getUser"})
    why = None if ran else ended or (TRUST if skipped and not log else "the hooks did not run for every call: see " + out)
    return ran, {"form": name, ("the agent file's hooks ran" if hooks == "agent" else "the hooks that were supplied ran"): ran,
                 "before `brain next`": passed["bash"],
                 "before a call": passed["pre"], "behind a call": passed["post"],
                 "calls the stand-in was given": len(game), "why not": why}


def rows_of(text):
    out = []
    for line in text.splitlines():
        try:
            out.append(json.loads(line))
        except ValueError:
            continue
    return [x for x in out if isinstance(x, dict)]


def main():
    named = [a for i, a in enumerate(sys.argv[1:], 1) if not a.startswith("--") and sys.argv[i - 1] not in ("--form", "--hooks")]
    out = os.path.abspath(named[0]) if named else tempfile.mkdtemp(prefix="tnr_preflight_")
    forms = [sys.argv[sys.argv.index("--form") + 1]] if "--form" in sys.argv else ["main", "subagent"]
    hooks = sys.argv[sys.argv.index("--hooks") + 1] if "--hooks" in sys.argv else "agent"
    if subprocess.run([sys.executable, os.path.join(HERE, "fake_connector.py"), "--selftest"],
                      capture_output=True, text=True).returncode:
        print(json.dumps({"started": False, "why": "the stand-in does not answer on this machine"}))
        return 2
    look = proof(os.path.join(out, "look"), "--look")
    seen = (rows_of(look.stdout) or [{}])[-1]
    servers = [m.get("name") for m in seen.get("mcp_servers") or []]
    if servers != ["Tnr"] or seen.get("mcp_tools") != []:
        print(json.dumps({"started": False, "why": "a session here has more than the stand-in, or could not be asked",
                          "servers": servers, "tools": seen.get("mcp_tools"), "said": (look.stdout + look.stderr)[-300:]}))
        return 2
    good = True
    for name in forms:
        ran, said = form(os.path.join(out, name), name, hooks)
        print(json.dumps(said))
        good = good and ran
    print(json.dumps({"the agent file's hooks are run on this machine": good and hooks == "agent", "kept in": out}))
    return 0 if good and hooks == "agent" else 1


if __name__ == "__main__":
    sys.exit(main())
