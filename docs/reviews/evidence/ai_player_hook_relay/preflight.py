"""Before the first live session on a machine: are the hooks of the relay's agent file run here?
(RUL-2026-11-14-160, point 1; PROOF.md, "The agent file's own hooks, and trust".)

    python3 docs/reviews/evidence/ai_player_hook_relay/preflight.py [OUT] [--form main|subagent]
            [--try [--control JSON] [--hold]] [--bare-env]

Run it from a terminal in the repository's root, on the machine and in the folder the relay will be started
in. OUT must not exist or must be empty; with none, a new temporary folder is made.

It starts the relay's agent as it is in this folder (.claude/agents/tnr-relay.md), once as a session's main
agent and once as a subagent of one, each against the stand-in for the game's connector (fake_connector.py),
for three reads of my own profile. For each form it says whether the agent file's hooks ran for every one of
those calls, and it ends with 0 only when they did in every form it was asked for. Where Claude Code skipped
them because the folder's trust dialog has not been accepted, it says so: open Claude Code in this folder
once, accept the dialog, and run this again. Do not start a live session while it says no.

RUL-2026-11-14-160 asks that it make no request of the game. What stands in front of a call, and what only
sees one after it has gone, are different things (review of 65974c02), so they are listed apart.

In front of every call:

1. Each session is given one MCP server, the stand-in, and told to load no other (--strict-mcp-config). This
   is what the check rests on. Nothing below was needed in any session that has been run.
2. Before any relay is started, a session with no tools of Claude Code's own, and whose every tool call the
   gate refuses, is started with the same options in the same folder. It must list one MCP server, and under
   its name exactly the stand-in's two tools. One of the two is named after this run, so no other server can
   have it: the name `Tnr` in a session started this way is this stand-in. It must also have run the hooks
   given on the command line, which the gate is. If not, nothing is started.
3. The gate (preflight_gate.py) is in front of every tool call of a relay's session. It refuses everything
   until this program has read the session's first event and found there one MCP server, no MCP tool but the
   connector's, the stand-in started by that session for this run, and the gate's own mark. After that it lets
   through `brain next`, in the subagent form one start of the relay's agent, and three reads of my own
   profile; it refuses the fourth call, and any call that is not such a read, whatever the brain asked for.

After a call has gone, which cannot take it back:

4. A call that the session shows an answer for and the stand-in did not write down, or a call the stand-in
   was given that the gate did not let through, ends the session and fails the check. So does a call the gate
   let through that has neither after 20 seconds, a first event that does not come within 45 seconds, a line
   of the session's output or of a log that cannot be read, and 150 seconds.
5. The session's processes are ended as a group and the stand-in is seen to be gone.

The relay's `brain next` is run by the session's shell. It plays in the check's own folder because the
session is given TNR_PLAYER_LIVE; a shell on that machine that sets the variable itself would send it to the
player's real folder. Before anything is started, a login shell with the check's variables is asked what it
has; if it is not the check's folder, nothing is started. That asks a shell like the session's, not the
session's own.

So if 1 failed on some machine, and 2 did not catch it, the most that could reach the game is three reads of
my own profile for each form, and 4 would say so. That would be a request of the game where none is allowed:
it is to be reported, not passed over.

--try: the relay's hooks are given on the command line as an agent's own, not read from the agent file. That
shows nothing about the machine, and the check ends with 1 whatever comes of it. It is for trying the check
where nobody can accept the dialog. With it, to try the gate: --control JSON is what the stand-in is told to do
(fake_connector.py: a profile that says HOSPITALIZED makes the brain ask for more than a read), and --hold
never opens the gate. --bare-env: the sessions are started with a path, a home and the proxy's
variables only, not with the terminal's own: the cloud session this was built in needs that.
"""
import json
import os
import secrets
import shutil
import signal
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
KEEP = ("PATH", "HOME", "LANG", "TERM", "HTTPS_PROXY", "https_proxy", "NO_PROXY", "no_proxy", "NODE_EXTRA_CA_CERTS",
        "SSL_CERT_FILE", "NIX_SSL_CERT_FILE")
UPKEEP = ("restock", "repair", "training", "equipment", "bank")
TOOL, PROBE = "mcp__Tnr__callEndpoint", "profile.getUser"
BOUND, STARTUP, LATE, CLOCK, AFTER = 3, 45.0, 20.0, 150.0, 3.0
STOPPED = "stopped after the check's calls"
TRUST = ("Claude Code skipped the agent file's hooks: this folder's trust dialog has not been accepted. Open "
         "Claude Code in this folder once, accept it, and run this again")


class Failed(Exception):
    """The check cannot go on: what it reads is missing, unreadable or not as it must be."""


# ---------------------------------------------------------------- what was written down
def rows(path):
    """A log of the check's own, row by row. A file that is not there yet has no rows; one that cannot be read,
    or a finished line that is not a row, fails the check (review of 65974c02, B2: a log that could not be
    opened was read as a log with nothing in it, and a call that had gone was not missed)."""
    try:
        with open(path, encoding="utf8") as f:
            text = f.read()
    except FileNotFoundError:
        return []
    except OSError as err:
        raise Failed(f"{os.path.basename(path)} cannot be read: {err}") from err
    out = []
    for line in text.split("\n")[:-1]:                           # (a last line with no end is still being written)
        try:
            row = json.loads(line)
        except ValueError as err:
            raise Failed(f"{os.path.basename(path)} has a line that is no row") from err
        if not isinstance(row, dict):
            raise Failed(f"{os.path.basename(path)} has a line that is no row")
        out.append(row)
    return out


def events(path):
    """What the session printed, as far as it is JSON objects. Claude Code prints other lines too (warnings);
    those are passed over. A finished line that begins as an object and is none fails the check."""
    try:
        with open(path, encoding="utf8", errors="replace") as f:
            text = f.read()
    except FileNotFoundError:
        return []
    except OSError as err:
        raise Failed(f"the session's output cannot be read: {err}") from err
    out = []
    for line in text.split("\n")[:-1]:
        if line.lstrip().startswith("{"):
            try:
                out.append(json.loads(line))
            except ValueError as err:
                raise Failed("the session printed a line that cannot be read") from err
    return [e for e in out if isinstance(e, dict)]


def first_event(stream):
    """The session's first event of its own: what it has. Told by its fields, however it is written out
    (B3: it was looked for by the bytes a line began with)."""
    return next((e for e in stream if e.get("type") == "system" and e.get("subtype") == "init"), None)


def inventory(init, tools):
    """Why a session's first event is not that of a session with the stand-in alone; None when it is.
    tools: the MCP tools it must list, exactly."""
    servers = init.get("mcp_servers")
    if not (isinstance(servers, list) and len(servers) == 1 and isinstance(servers[0], dict)
            and servers[0].get("name") == "Tnr" and servers[0].get("status") == "connected"):
        return f"its MCP servers are not the stand-in alone: {json.dumps(servers)[:200]}"
    listed = init.get("tools")
    if not isinstance(listed, list) or not all(isinstance(t, str) for t in listed):
        return "it does not list its tools"
    has = sorted(t for t in listed if t.startswith("mcp__"))
    if has != sorted(tools):
        return f"its MCP tools are {has}, not {sorted(tools)}"
    return None


def admission(init, game, gate, nonce, tools):
    """Why this session may not be let through the gate yet, or ever: (why, final). (None, False) when it may."""
    why = inventory(init, tools)
    if why:
        return why, True
    session = init.get("session_id")
    if not isinstance(session, str) or not session:
        return "its first event has no session id", True
    here = [g for g in game if g.get("at") == "connected"]
    if any(g.get("nonce") != nonce for g in here) or len(here) > 1:
        return "the stand-in's log is not this run's", True
    if not here:
        return "the stand-in has not been started by the session", False
    if not any(g.get("kind") == "start" and g.get("session") == session for g in gate):
        return "the hooks given on the command line have not run in the session", False
    return None, False


def results(stream):
    """What the session shows for its tool calls so far: {the call's id: it was an error}."""
    out = {}
    for e in stream:
        content = (e.get("message") or {}).get("content") if e.get("type") == "user" else None
        for c in content if isinstance(content, list) else []:
            if isinstance(c, dict) and c.get("type") == "tool_result" and isinstance(c.get("tool_use_id"), str):
                out[c["tool_use_id"]] = bool(c.get("is_error"))
    return out


def astray(gate, game, shown, now):
    """Why what went to a connector and what the stand-in was given are not the same calls; None while they
    are. shown: results(), read before the stand-in's log was.

    The gate lets a call through by not refusing it. The relay's hook, or the session's permissions, may still
    refuse it, and then it has an error for its result and never went. A call that has a result which is no
    error went somewhere: if the stand-in did not write it down, something else answered it. A call with no
    result has LATE seconds to be written down by the stand-in."""
    through = [g for g in gate if g.get("kind") == "call" and not g.get("refused")]
    came = [g for g in game if g.get("at") == "came"]
    if any(g.get("endpoint") != PROBE or g.get("input") not in ({}, None) for g in came):
        return "the stand-in was given a call that is not a read of my own profile"
    ids = [g.get("use") for g in came]
    if not all(isinstance(i, str) and i for i in ids) or len(set(ids)) != len(ids):
        return "the stand-in's rows do not name their tool calls: this Claude Code is not one the check knows"
    if set(ids) - {g.get("use") for g in through}:
        return "the stand-in was given a call the gate did not let through"
    for g in through:
        if g.get("use") in ids or shown.get(g.get("use")) is True:
            continue
        if shown.get(g.get("use")) is False:
            return "a call was answered, and not by the stand-in"
        if now - g["at"] > LATE:
            return f"a call the gate let through is not in the stand-in's log and has no result after {LATE:.0f} seconds"
    return None


def verdict(form, how, session, gate, hooks, game, reaped):
    """Did the relay's hooks run for every one of the check's calls? -> why not, or None.
    (B4: any hook of each kind and any call of the stand-in's was taken for all of it; a session that had run
    out of time, or had failed to start, could pass on what an earlier one left behind.)"""
    if how != STOPPED:
        return f"the session was not stopped after its calls: {how}"
    if not reaped:
        return "the session's processes could not be seen to end"
    through = [g for g in gate if g.get("kind") == "call" and not g.get("refused")]
    uses = [g.get("use") for g in through]
    if len(through) != BOUND or len(set(uses)) != BOUND or not all(isinstance(u, str) and u for u in uses):
        return f"the gate let {len(through)} calls through, not {BOUND}"
    if any(g.get("session") != session for g in gate):
        return "the gate's rows are not all this session's"
    who = {g.get("by") for g in through}
    if len(who) != 1 or (who == {session}) != (form == "main"):
        return "the calls were not made by one relay of this form"
    relay = who.pop()
    over = {g.get("use") for g in gate if g.get("refused") == "the check's calls have been made"}
    for h in hooks:
        if h.get("by") != relay:
            return "a hook ran for another than the relay"
        if h.get("refused") and h.get("use") not in over:
            return f"a hook refused: {h.get('refused')}"
    for use in uses:
        for kind in ("pre", "post"):
            if sum(1 for h in hooks if h.get("hook") == kind and h.get("use") == use and not h.get("refused")) != 1:
                return f"the hook {'before' if kind == 'pre' else 'behind'} a call did not run once for each call"
    if any(h.get("hook") in ("pre", "post", "fail") and h.get("use") not in set(uses) | over for h in hooks):
        return "a hook ran for a call the gate did not let through"
    if sum(1 for h in hooks if h.get("hook") == "bash" and not h.get("refused")) < BOUND:
        return "the hook before `brain next` did not run for every batch"
    came, done = ([g for g in game if g.get("at") == k] for k in ("came", "answered"))
    if len(came) != BOUND or len(done) != BOUND or any(g.get("failed") for g in done):
        return f"the stand-in was given {len(came)} calls and answered {len(done)}, not {BOUND}"
    if sorted(str(g.get("use")) for g in came) != sorted(uses) or sorted(str(g.get("use")) for g in done) != sorted(uses):
        return "the stand-in's calls are not the ones the gate let through"
    return None


# ---------------------------------------------------------------- one session
def fresh(path):
    """A folder for one session that nothing was written into before (B4: a folder used again kept its logs)."""
    if os.path.exists(path) and (not os.path.isdir(path) or os.listdir(path)):
        raise Failed(f"{path} is not empty: the check writes into a folder of its own")
    os.makedirs(path, exist_ok=True)
    return path


def prepare(out, form, agent):
    """The session's files: its MCP config (the stand-in alone), the gate's settings, what the gate goes by."""
    nonce, told = secrets.token_hex(6), {}
    if "--try" in sys.argv and "--control" in sys.argv and form != "look":
        with open(os.path.join(out, "control.json"), "w", encoding="utf8") as f:
            json.dump(json.loads(sys.argv[sys.argv.index("--control") + 1]), f)
        told = {"TNR_FAKE_CONTROL": os.path.join(out, "control.json")}
    with open(os.path.join(out, "mcp.json"), "w", encoding="utf8") as f:
        json.dump({"mcpServers": {"Tnr": {"command": sys.executable, "args": [os.path.join(HERE, "fake_connector.py")],
                                          "env": dict(told, TNR_FAKE_LOG=os.path.join(out, "game.jsonl"),
                                                      TNR_FAKE_NONCE=nonce)}}}, f)
    gate = f'"{sys.executable}" "{os.path.join(HERE, "preflight_gate.py")}"'
    with open(os.path.join(out, "gate.json"), "w", encoding="utf8") as f:
        json.dump({"hooks": {
            "SessionStart": [{"hooks": [{"type": "command", "command": gate + " start", "timeout": 20}]}],
            "PreToolUse": [{"matcher": ".*", "hooks": [{"type": "command", "command": gate + " tool", "timeout": 30,
                                                        "onFailure": "block"}]}]}}, f)
    with open(os.path.join(out, "run.json"), "w", encoding="utf8") as f:
        json.dump({"form": form, "agent": agent, "bound": BOUND if form != "look" else 0, "nonce": nonce}, f)
    return nonce


def environment(out):
    env = {k: os.environ[k] for k in KEEP if os.environ.get(k)} if "--bare-env" in sys.argv else dict(os.environ)
    env.pop("TNR_TRANSCRIPT", None)
    env.update(TNR_PLAYER_LIVE=os.path.join(out, "live"), TNR_PLAYER_FIGHTS=os.path.join(out, "fights"),
               TNR_PLAYER_NO_DAEMON="1", TNR_PREFLIGHT_OUT=out)
    return env


def command(out, env):
    return [shutil.which("claude", path=env.get("PATH")) or "claude", "-p", "--model", "haiku", "--strict-mcp-config",
            "--mcp-config", os.path.join(out, "mcp.json"), "--settings", os.path.join(out, "gate.json"),
            "--output-format", "stream-json", "--verbose", "--debug-file", os.path.join(out, "debug.log")]


def end(p, game):
    """End the session's processes as a group. -> the session and the stand-in it started are gone."""
    if p.poll() is None:
        if os.name == "nt":
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)], capture_output=True)
        else:
            for sig in (signal.SIGTERM, signal.SIGKILL):
                try:
                    os.killpg(p.pid, sig)
                except ProcessLookupError:
                    break
                try:
                    p.wait(timeout=5)
                    break
                except subprocess.TimeoutExpired:
                    continue
    try:
        p.wait(timeout=10)
    except subprocess.TimeoutExpired:
        return False
    if os.name == "nt":
        return True
    for pid in [g.get("pid") for g in game if g.get("at") == "connected" and isinstance(g.get("pid"), int)]:
        for _ in range(60):
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                break
            except PermissionError:
                return False
            time.sleep(0.05)
        else:
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
            return False
    return True


def session(out, form, start, tools, done):
    """Start one session and watch it. -> (how it ended, its first event's session id, the group was seen to end).
    done(gate, hooks, game): the session has done what it was started for, and is stopped."""
    with open(os.path.join(out, "run.json"), encoding="utf8") as f:
        nonce = json.load(f)["nonce"]
    env = environment(out)
    paths = {k: os.path.join(out, v) for k, v in (("stream", "stream.jsonl"), ("gate", "gate.jsonl"), ("game", "game.jsonl"),
                                                  ("hooks", os.path.join("live", "hook", "log.jsonl")))}
    how, whose, begun, since = None, None, time.time(), None
    with open(paths["stream"], "w", encoding="utf8") as stream:
        p = subprocess.Popen(command(out, env) + start, cwd=ROOT, env=env, stdout=stream, stderr=subprocess.STDOUT,
                             stdin=subprocess.DEVNULL, **({"start_new_session": True} if os.name != "nt" else
                                                         {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP}))
        try:
            while how is None:
                now = time.time()
                said = events(paths["stream"])                    # (first: a result it shows is in the logs read after)
                gate, game, hooks = rows(paths["gate"]), rows(paths["game"]), rows(paths["hooks"])
                init = first_event(said)
                if whose is None and init is not None:
                    why, final = admission(init, game, gate, nonce, tools)
                    if why is None and form != "look" and not ("--try" in sys.argv and "--hold" in sys.argv):
                        whose = init["session_id"]
                        with open(os.path.join(out, "admitted.tmp"), "w", encoding="utf8") as f:
                            f.write(whose)
                        os.replace(os.path.join(out, "admitted.tmp"), os.path.join(out, "admitted"))
                    elif why is None:
                        whose = init["session_id"]
                    elif final:
                        how = "ended: " + why
                if how is None and whose is None and now - begun > STARTUP:
                    how = "ended: the session did not show what it has in time"
                lost = astray(gate, game, results(said), now)
                if how is None and lost:
                    how = "ended: " + lost
                if how is None and done(gate, hooks, game):
                    since = since or now
                    if now - since >= 0.2:
                        how = STOPPED
                elif how is None and p.poll() is not None:
                    how = "the session ended by itself"
                elif how is None and now - begun > CLOCK:
                    how = "ended: the clock ran out"
                time.sleep(0.05)
        except Failed as err:
            how = f"ended: {err}"
        finally:
            try:
                last = rows(paths["game"])
            except Failed:
                last = []                                         # (it is ended all the same; how says why)
            reaped = end(p, last)
    return how, whose, reaped


def form(out, name, agent, more):
    """One relay in one form. -> (the agent file's hooks ran for every call, what is printed of it)."""
    nonce = prepare(fresh(out), name, agent)
    env = environment(out)
    subprocess.run([sys.executable, "-m", "player.brain", "set", "mode=guard",
                    "activities=" + json.dumps({a: False for a in UPKEEP})], cwd=ROOT, env=env, check=True, capture_output=True)
    start = ["--agent", agent, "Begin."] if name == "main" else [
        "--allowedTools", "Agent", "Task", "--",
        f"Start the subagent `{agent}` once with the Agent tool: subagent_type \"{agent}\", prompt \"Begin.\", "
        "run_in_background false. Do nothing else yourself: run no command and call no other tool. When it "
        "returns, reply with its last line only."]

    def done(gate, hooks, game):
        """The three calls are answered, and the hook behind the third has had its time."""
        answered = [g for g in game if g.get("at") == "answered"]
        if len(answered) < BOUND:
            return False
        uses = {g.get("use") for g in gate if g.get("kind") == "call" and not g.get("refused")}
        behind = {h.get("use") for h in hooks if h.get("hook") == "post"}
        return uses <= behind or time.time() - answered[BOUND - 1]["answered"] > AFTER
    # (a main agent's session lists the agent's own tools; one that starts a subagent lists all it has)
    tools = [TOOL] if name == "main" else [TOOL, f"mcp__Tnr__standIn_{nonce}"]
    how, whose, reaped = session(out, name, more + start, tools, done)
    gate, game = rows(os.path.join(out, "gate.jsonl")), rows(os.path.join(out, "game.jsonl"))
    hooks = rows(os.path.join(out, "live", "hook", "log.jsonl"))
    why = verdict(name, how, whose, gate, hooks, game, reaped)
    try:
        with open(os.path.join(out, "debug.log"), encoding="utf8", errors="replace") as f:
            skipped = "Skipping frontmatter hooks" in f.read()
    except OSError:
        skipped = False
    if why and skipped and not hooks:
        why = TRUST
    count = {k: sum(1 for h in hooks if h.get("hook") == k and not h.get("refused")) for k in ("bash", "pre", "post")}
    return why is None, {"form": name, "the relay's hooks ran for every call": why is None,
                         "calls the gate let through": sum(1 for g in gate if g.get("kind") == "call" and not g.get("refused")),
                         "calls the stand-in was given": sum(1 for g in game if g.get("at") == "came"),
                         "hooks before `brain next`, before a call, behind a call": [count[k] for k in ("bash", "pre", "post")],
                         "how the session ended": how, "why not": why}


def shell_keeps(out):
    """Why the session's shell would not run `brain next` in the check's folder; None when a login shell with
    the check's variables has that folder for TNR_PLAYER_LIVE, or where there is no such shell to ask."""
    env = environment(out)
    if os.name == "nt":
        return None
    try:
        said = subprocess.run([env.get("SHELL") or "/bin/sh", "-lc", 'printf "%s" "$TNR_PLAYER_LIVE"'], env=env,
                              capture_output=True, text=True, timeout=30, stdin=subprocess.DEVNULL)
    except (OSError, subprocess.TimeoutExpired) as err:
        return f"the shell could not be asked for its variables: {err}"
    if said.stdout.strip().splitlines()[-1:] != [env["TNR_PLAYER_LIVE"]]:
        return "a shell on this machine sets TNR_PLAYER_LIVE itself: `brain next` would not run in the check's folder"
    return None


def look(out):
    """Guard 2: a session that can call nothing, with the same options. -> why nothing may be started, or None."""
    nonce = prepare(fresh(out), "look", None)
    how, whose, reaped = session(out, "look", ["--tools", "", "--", "Reply with the single word: ready"],
                                 [TOOL, f"mcp__Tnr__standIn_{nonce}"], lambda gate, hooks, game: False)
    gate, game = rows(os.path.join(out, "gate.jsonl")), rows(os.path.join(out, "game.jsonl"))
    if how != "the session ended by itself" or whose is None:
        return f"a session with the stand-in alone could not be looked at: {how}"
    if any(g.get("kind") != "start" and not g.get("refused") for g in gate) or any(g.get("at") != "connected" for g in game):
        return "the session that may call nothing made a call"
    return None if reaped else "its processes could not be seen to end"


def main():
    skip = {sys.argv[i + 1] for i, a in enumerate(sys.argv[:-1]) if a in ("--form", "--control")}
    named = [a for a in sys.argv[1:] if not a.startswith("--") and a not in skip]
    forms = [sys.argv[sys.argv.index("--form") + 1]] if "--form" in sys.argv else ["main", "subagent"]
    agent, more = "tnr-relay", []
    try:
        out = fresh(os.path.abspath(named[0])) if named else tempfile.mkdtemp(prefix="tnr_preflight_")
        if "--try" in sys.argv:
            sys.path.insert(0, HERE)
            import proof
            agent, more = "tnr-relay-proof", ["--agents", json.dumps(proof.the_agent(proof.hooks_of_the_agent()))]
        if subprocess.run([sys.executable, os.path.join(HERE, "fake_connector.py"), "--selftest"],
                          capture_output=True, text=True).returncode:
            raise Failed("the stand-in does not answer on this machine")
        why = shell_keeps(os.path.join(out, "look")) or look(os.path.join(out, "look"))
        if why:
            raise Failed(why)
    except Failed as err:
        print(json.dumps({"started": False, "why": str(err)}))
        return 2
    good = True
    for name in forms:
        try:
            ran, said = form(os.path.join(out, name), name, agent, more)
        except Failed as err:
            ran, said = False, {"form": name, "the relay's hooks ran for every call": False, "why not": str(err)}
        print(json.dumps(said))
        good = good and ran
    here = good and "--try" not in sys.argv
    print(json.dumps({"the agent file's hooks are run on this machine": here, "kept in": out}))
    return 0 if here else 1


if __name__ == "__main__":
    sys.exit(main())
