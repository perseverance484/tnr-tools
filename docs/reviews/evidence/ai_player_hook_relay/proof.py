"""One run of the proof (PROOF_PLAN.md): the relay's agent under Claude Code itself, against the stand-in for the
game's connector. It makes no request of the game: the session it starts has one MCP server, fake_connector.py.

    python3 docs/reviews/evidence/ai_player_hook_relay/proof.py OUT [--batches N] [--control JSON]
            [--effort LEVEL] [--hooks agent|settings|agents] [--break WHICH:NTH:HOW[:TIMEOUT]] [--no-block]
            [--rule TEXT] [--own-env] [--seconds N] [--look]

OUT: a folder for the run: the rehearsal's live folder (live/), what the stand-in was asked (game.jsonl), what
Claude Code printed (stream.jsonl), its debug log (debug.log).
--look: only start a session with the stand-in and no agent, ask it for one word, and print which MCP servers
and tools it has. That is looked at before anything else is run.

The session is started with none of this session's own variables: a path, a home, and the proxy's. --own-env:
with the variables of the terminal it is started from, for a machine where it is started by hand. Either way
its only MCP server is the stand-in (--strict-mcp-config), and the run is ended at once if its first event
lists any other.

--hooks agent (the default): the hooks are the ones the agent file declares. Claude Code runs those only in a
folder whose trust dialog has been accepted on that machine. --hooks settings: the same four hooks, read out of
the agent file, are given to the session on its command line (--settings), as the one who starts it may. That
is for a machine where nobody can accept the dialog; it does not show that the agent file's own are run.
--hooks agents: the agent file's whole definition, hooks and all, is given on the command line (--agents) under
the name tnr-relay-proof: an agent's own hooks, from a place Claude Code takes without the dialog.

--break pre:3:exit1: the third run of the hook before a connector call ends with 1 (proof_hook.sh). sleep for
exit1: it runs past its timeout, which :TIMEOUT sets in seconds. post,fail:0:look: neither fails, and each
writes down what it was given. --no-block: the hooks are declared without onFailure: block, to see what that
line is worth. Both need --hooks settings or agents.

--rule TEXT: with --hooks agents, one more line under the agent's Rules: a wording that is tried, not one the
agent file has.
"""
import json
import os
import re
import subprocess
import sys
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
KEEP = ("PATH", "HOME", "LANG", "TERM", "HTTPS_PROXY", "https_proxy", "NO_PROXY", "no_proxy", "NODE_EXTRA_CA_CERTS",
        "SSL_CERT_FILE", "NIX_SSL_CERT_FILE")
UPKEEP = ("restock", "repair", "training", "equipment", "bank")


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def hooks_of_the_agent():
    """The four hooks the relay's agent file declares, as a settings document."""
    with open(os.path.join(ROOT, ".claude", "agents", "tnr-relay.md"), encoding="utf8") as f:
        head = f.read().split("---\n", 2)[1]
    out = {}
    for event, body in re.findall(r"^  (\w+):\n((?:    .*\n)+)", head[head.index("hooks:"):], re.M):
        for matcher, rest in re.findall(r'- matcher: "([^"]*)"\n((?:      .*\n|        .*\n|          .*\n)+)', body):
            hook = {"type": "command", "command": json.loads(re.search(r'command: ("(?:[^"\\]|\\.)*")', rest).group(1)),
                    "timeout": int(re.search(r"timeout: (\d+)", rest).group(1))}
            if "onFailure: block" in rest:
                hook["onFailure"] = "block"
            out.setdefault(event, []).append({"matcher": matcher, "hooks": [hook]})
    return {"hooks": out}


def broken(doc, how, count, block):
    """The hooks, with one that fails on one of its runs (how: WHICH:NTH:HOW[:TIMEOUT]), and without
    onFailure: block where block is false."""
    which, nth, kind, *timeout = (how or "::").split(":")
    for entries in doc["hooks"].values():
        for entry in entries:
            for hook in entry["hooks"]:
                mine = hook["command"].rsplit(" ", 1)[-1]          # (bash, pre, post or fail)
                if how and mine in which.split(","):
                    hook["command"] = f'sh "{os.path.join(HERE, "proof_hook.sh")}" {mine} {nth} {kind} "{count}.{mine}"'
                    hook["timeout"] = int(timeout[0]) if timeout else hook["timeout"]
                if not block:
                    hook.pop("onFailure", None)
    return doc


def the_agent(hooks, rule=None):
    """The relay's agent file as --agents takes one, under a name of the proof's own."""
    with open(os.path.join(ROOT, ".claude", "agents", "tnr-relay.md"), encoding="utf8") as f:
        _, head, body = f.read().split("---\n", 2)
    if rule:
        at = body.index("\n\n## A batch with `put` lines")
        body = body[:at] + "\n- " + rule + body[at:]
    return {"tnr-relay-proof": {"description": re.search(r"^description: (.*)$", head, re.M).group(1), "prompt": body,
                                "tools": re.search(r"^tools: (.*)$", head, re.M).group(1).split(", "), "model": "haiku",
                                "omitClaudeMd": True, "hooks": hooks["hooks"]}}


def main():
    out = os.path.abspath(sys.argv[1])
    live, game, ctl = os.path.join(out, "live"), os.path.join(out, "game.jsonl"), os.path.join(out, "control.json")
    os.makedirs(live, exist_ok=True)
    told = json.loads(arg("--control", "{}"))
    with open(ctl, "w", encoding="utf8") as f:
        json.dump(told, f)
    with open(os.path.join(out, "mcp.json"), "w", encoding="utf8") as f:
        json.dump({"mcpServers": {"Tnr": {"command": "python3", "args": [os.path.join(HERE, "fake_connector.py")],
                                          "env": {"TNR_FAKE_LOG": game, "TNR_FAKE_CONTROL": ctl}}}}, f)
    env = dict(os.environ) if "--own-env" in sys.argv else {k: os.environ[k] for k in KEEP if os.environ.get(k)}
    env.update(TNR_PLAYER_LIVE=live, TNR_PLAYER_FIGHTS=os.path.join(out, "fights"), TNR_PLAYER_NO_DAEMON="1")
    claude = ["claude", "-p", "--model", "haiku", "--strict-mcp-config", "--mcp-config", os.path.join(out, "mcp.json"),
              "--output-format", "stream-json", "--verbose", "--debug-file", os.path.join(out, "debug.log")]
    if "--look" in sys.argv:
        done = subprocess.run(claude + ["Reply with the single word: ready"], cwd=out, env=env, capture_output=True,
                              text=True, timeout=120)
        first = json.loads(done.stdout.splitlines()[0])
        print(json.dumps({"mcp_servers": first.get("mcp_servers"), "mcp_tools": [t for t in first.get("tools", []) if t.startswith("mcp__")],
                          "tools": len(first.get("tools", [])), "model": first.get("model")}))
        return 0
    brain = [sys.executable, "-m", "player.brain", "set"]
    subprocess.run(brain + ["mode=hunt", "activities=" + json.dumps({a: False for a in UPKEEP})], cwd=ROOT, env=env,
                   check=True, capture_output=True)
    if arg("--effort"):
        claude += ["--effort", arg("--effort")]
    how, agent = arg("--hooks", "agent"), "tnr-relay"
    if how != "agent":
        hooks = broken(hooks_of_the_agent(), arg("--break"), os.path.join(out, "hook_runs"), "--no-block" not in sys.argv)
        with open(os.path.join(out, "hooks.json"), "w", encoding="utf8") as f:
            json.dump(hooks, f, indent=1)
        if how == "settings":
            claude += ["--settings", json.dumps(hooks)]
        else:
            agent = "tnr-relay-proof"
            claude += ["--agents", json.dumps(the_agent(hooks, arg("--rule")))]
    batches, begun = int(arg("--batches", "12")), time.time()
    with open(os.path.join(out, "stream.jsonl"), "w", encoding="utf8") as stream:
        p = subprocess.Popen(claude + ["--agent", agent, "Begin."], cwd=ROOT, env=env, stdout=stream,
                             stderr=subprocess.STDOUT)

        def only_the_stand_in():
            """The session's first event lists its MCP servers and tools. Anything but the stand-in: it is ended."""
            while p.poll() is None:
                with open(os.path.join(out, "stream.jsonl"), encoding="utf8") as f:
                    first = [json.loads(x) for x in f if x.startswith('{"type":"system","subtype":"init"') and x.endswith("\n")]
                if first:
                    servers = [m.get("name") for m in first[0].get("mcp_servers") or []]
                    tools = [t for t in first[0].get("tools") or [] if t.startswith("mcp__")]
                    if servers != ["Tnr"] or tools != ["mcp__Tnr__callEndpoint"]:
                        p.kill()
                        print(json.dumps({"ended": "the session has more than the stand-in", "servers": servers, "tools": tools}))
                    return
                time.sleep(0.05)

        def enough():
            """After so many reads of my profile (one a batch), the game says I am asleep and the director ends
            the session: the brain tells the relay to stop."""
            while p.poll() is None:
                try:
                    with open(game, encoding="utf8") as f:
                        seen = sum(1 for x in f if '"profile.getUser"' in x and '"answered"' in x)
                except OSError:
                    seen = 0
                if seen >= batches:
                    with open(ctl, "w", encoding="utf8") as f:
                        json.dump(dict(told, status="ASLEEP"), f)
                    subprocess.run(brain + ["end_session=true"], cwd=ROOT, env=env, capture_output=True)
                    return
                time.sleep(1)
        threading.Thread(target=only_the_stand_in, daemon=True).start()
        threading.Thread(target=enough, daemon=True).start()
        try:
            code = p.wait(timeout=float(arg("--seconds", "900")))
        except subprocess.TimeoutExpired:
            p.kill()
            code = "ended by the clock"
    print(json.dumps({"exit": code, "seconds": round(time.time() - begun, 1)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
