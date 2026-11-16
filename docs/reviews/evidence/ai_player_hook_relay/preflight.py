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
   was given that the gate did not let through, ends the session and fails the check. So does a call that
   came back as an error and is not in the stand-in's log, unless the relay's own hook refused it on record:
   an error does not say whether a call went. So does a call the gate let through that has neither result
   nor row after 20 seconds, a first event that does not come within 45 seconds, a line of the session's
   output or of a log that cannot be read, and 150 seconds.
5. The session is the leader of a process group of its own. When the check ends it, the group is ended,
   whatever its leader has done by then, with what descends from it and the stand-in it started: asked to
   end, and ended after five seconds if it has not. The system is asked what runs every tenth of a second
   until none of them does, and every answer is kept: a process that was once seen with a parent of the
   session is looked for by its own id from then on, wherever it goes. The check passes only if none of
   them is left running. What it cannot find is a process that left the group and lost its parent between
   two such looks, without ever being seen in one; the stand-in is found by its log all the same.

Yes also means that the session was running when the check first asked it to end, which is asked after the
system has said what runs and in the moment before the signal. One that had ended by itself, with whatever
code and whatever it left behind, is not one the check stopped after its calls, and does not pass.

It is written for a POSIX system (Linux, macOS). On another it starts nothing and says so.

The relay's `brain next` is run by the session's shell. It plays in the check's own folder because the
session is given TNR_PLAYER_LIVE; a shell on that machine that sets the variable itself would send it to the
player's real folder. Before anything is started, a login shell with the check's variables is asked what it
has; if it is not the check's folder, nothing is started. That asks a shell like the session's, not the
session's own.

So if 1 failed on some machine, and 2 did not catch it, the most that could reach the game is three reads of
my own profile for each form. 4 would say so for a call that was answered; for one that came back as an
error it says that it cannot be told. That would be a request of the game where none is allowed:
it is to be reported, not passed over.

--try: the relay's hooks are given on the command line as an agent's own, not read from the agent file. That
shows nothing about the machine, and the check ends with 1 whatever comes of it. It is for trying the check
where nobody can accept the dialog. With it, to try the gate: --control JSON is what the stand-in is told to do
(fake_connector.py: a profile that says HOSPITALIZED makes the brain ask for more than a read), and --hold
never opens the gate. --bare-env: the sessions are started with a path, a home and the proxy's
variables only, not with the terminal's own: the cloud session this was built in needs that.
"""
import collections
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
BOUND, STARTUP, LATE, CLOCK, AFTER, PATIENCE = 3, 45.0, 20.0, 150.0, 3.0, 5.0
STOPPED, BY_ITSELF = "stopped after the check's calls", "the session ended by itself"
Ended = collections.namedtuple("Ended", "how session gone running code")
"""How a session ended: in words; its first event's session id; its processes were all seen to be gone; it was
still running when the check ended it; what it ended with."""
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


def astray(gate, game, shown, hooks, now):
    """Why what went to a connector and what the stand-in was given are not the same calls, or cannot be told
    to be; None while they are. shown: results(), read before the logs were. hooks: the relay's hooks' log.

    The gate lets a call through by not refusing it. For one the stand-in has not written down:
    - the relay's own hook refused it, on record, before it went: it never went;
    - the session shows an answer for it that is no error: something else answered it;
    - the session shows an error for it: the session's permissions may have refused it, or it may have gone to
      something that answered with an error. An error does not say which (review of 071ba1b1, C3: it was read
      as "never went"), so it is not passed over;
    - nothing yet: it has LATE seconds to be written down by the stand-in."""
    through = [g for g in gate if g.get("kind") == "call" and not g.get("refused")]
    came = [g for g in game if g.get("at") == "came"]
    if any(g.get("endpoint") != PROBE or g.get("input") not in ({}, None) for g in came):
        return "the stand-in was given a call that is not a read of my own profile"
    ids = [g.get("use") for g in came]
    if not all(isinstance(i, str) and i for i in ids) or len(set(ids)) != len(ids):
        return "the stand-in's rows do not name their tool calls: this Claude Code is not one the check knows"
    if set(ids) - {g.get("use") for g in through}:
        return "the stand-in was given a call the gate did not let through"
    refused = {h.get("use") for h in hooks if h.get("hook") == "pre" and h.get("refused")}
    for g in through:
        if g.get("use") in ids or g.get("use") in refused:
            continue
        if shown.get(g.get("use")) is False:
            return "a call was answered, and not by the stand-in"
        if shown.get(g.get("use")) is True:
            return ("a call the gate let through came back as an error and is not in the stand-in's log: "
                    "whether it went cannot be told")
        if now - g["at"] > LATE:
            return f"a call the gate let through is not in the stand-in's log and has no result after {LATE:.0f} seconds"
    return None


def verdict(form, ended, gate, hooks, game):
    """Did the relay's hooks run for every one of the check's calls? -> why not, or None.
    (B4: any hook of each kind and any call of the stand-in's was taken for all of it; a session that had run
    out of time, or had failed to start, could pass on what an earlier one left behind.)"""
    session = ended.session
    if ended.how != STOPPED or not ended.running:
        return f"the session was not stopped after its calls: {ended.how}" + (
            f" (with {ended.code})" if ended.how == BY_ITSELF else "")
    if not ended.gone:
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


def processes():
    """Every process the system lists: {pid: (its parent, its process group, its state)}. None where the
    system cannot be asked (`ps`, as POSIX has it): the check then cannot say that a session has ended."""
    try:
        said = subprocess.run(["ps", "-A", "-o", "pid=", "-o", "ppid=", "-o", "pgid=", "-o", "stat="],
                              capture_output=True, text=True, timeout=20, stdin=subprocess.DEVNULL)
    except (OSError, subprocess.TimeoutExpired):
        return None
    listed = {}
    for line in said.stdout.splitlines() if said.returncode == 0 else []:
        f = line.split()
        if len(f) >= 4 and all(x.isdigit() for x in f[:3]):
            listed[int(f[0])] = (int(f[1]), int(f[2]), f[3])
    return listed or None


def family(listed, leader, known):
    """The session's processes that are still running: the ones in its process group, the ones that descend
    from one of them or from one that was seen before (known), and those. One that has ended and waits to
    be collected (state Z) runs nothing, and is not counted.

    Never this program, nor one it descends from, nor the system's first process, whatever a log names: what
    is found here is asked to end, and then ended."""
    mine, at = {0, 1}, os.getpid()
    while at in listed and at not in mine:
        mine.add(at)
        at = listed[at][0]
    kin, more = set(), ({leader} | set(known)) - mine
    while more - kin:
        kin |= more
        more = {pid for pid, (parent, group, _) in listed.items() if parent in kin or group == leader} - mine
    return {pid for pid in kin if pid in listed and not listed[pid][2].startswith("Z")}


def end(p, game):
    """End the session's processes, and see that they are gone.
    -> (they were all seen to be gone, the session was running when it was first asked to end).

    The session is started as the leader of a process group of its own. That group is ended, whatever has
    become of its leader, with what descends from it and the stand-in the session started: asked to end,
    then, after PATIENCE seconds, ended; and it is gone only when none of them is left running (review of
    071ba1b1, C1: the group was signalled only while its leader lived, and the wait was for the leader alone,
    so a child that did not end when asked was never ended, and was not looked for).

    Every look at what runs is kept, the looks in the wait too: a process that is seen while its parent is of
    the family is looked for by its own id from then on, and is asked to end, or ended, as soon as it is seen
    (review of c2efaaa2, C1: only the look before each signal was kept, so a child that appeared after it,
    left the group, and lost its parent was no longer looked for, and the session was called gone).

    Whether the session was running is asked here, after the first look at what runs and before the first
    signal, and not before the look, which takes its time (review of c2efaaa2, C2: a session that ended by
    itself while the system was being asked was put down as stopped by the check)."""
    known = {g.get("pid") for g in game if g.get("at") == "connected" and isinstance(g.get("pid"), int)}
    running = None
    for sig in (signal.SIGTERM, signal.SIGKILL):
        told, until = set(), None
        while until is None or time.time() < until:
            listed = processes()
            if listed is None:
                return False, bool(running)
            left = family(listed, p.pid, known)
            known |= left
            if running is None:
                running = p.poll() is None
            if p.poll() is not None and not left:
                return True, running
            for target, send in ([(p.pid, os.killpg)] if until is None else []) + [
                    (pid, os.kill) for pid in sorted(left - told) if until is not None or listed[pid][1] != p.pid]:
                try:
                    send(target, sig)
                except (ProcessLookupError, PermissionError):
                    pass
            told |= left
            until = until or time.time() + PATIENCE
            time.sleep(0.1)
    return False, bool(running)


def session(out, form, start, tools, done):
    """Start one session and watch it. -> Ended.
    done(gate, hooks, game): the session has done what it was started for, and is stopped. A session that has
    ended by itself is never taken for one that was stopped, whatever it left behind (review of 071ba1b1, C2:
    what it had done was looked at first, and a session that had failed was put down as stopped)."""
    with open(os.path.join(out, "run.json"), encoding="utf8") as f:
        nonce = json.load(f)["nonce"]
    env = environment(out)
    paths = {k: os.path.join(out, v) for k, v in (("stream", "stream.jsonl"), ("gate", "gate.jsonl"), ("game", "game.jsonl"),
                                                  ("hooks", os.path.join("live", "hook", "log.jsonl")))}
    how, whose, begun, since = None, None, time.time(), None
    with open(paths["stream"], "w", encoding="utf8") as stream:
        p = subprocess.Popen(command(out, env) + start, cwd=ROOT, env=env, stdout=stream, stderr=subprocess.STDOUT,
                             stdin=subprocess.DEVNULL, start_new_session=True)
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
                lost = astray(gate, game, results(said), hooks, now)
                if how is None and lost:
                    how = "ended: " + lost
                if how is None and p.poll() is not None:          # before anything is made of what it left:
                    how = BY_ITSELF                               # a session that ended was not stopped (C2)
                elif how is None and done(gate, hooks, game):
                    since = since or now
                    if now - since >= 0.2:
                        how = STOPPED
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
            gone, running = end(p, last)                          # (running: at the first signal, as end saw it)
    stopped = how == STOPPED and running
    return Ended(BY_ITSELF if how == STOPPED and not running else how, whose, gone, stopped, p.poll())


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
    ended = session(out, name, more + start, tools, done)
    gate, game = rows(os.path.join(out, "gate.jsonl")), rows(os.path.join(out, "game.jsonl"))
    hooks = rows(os.path.join(out, "live", "hook", "log.jsonl"))
    why = verdict(name, ended, gate, hooks, game)
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
                         "how the session ended": ended.how, "it ended with": ended.code, "why not": why}


def shell_keeps(out):
    """Why the session's shell would not run `brain next` in the check's folder; None when a login shell with
    the check's variables has that folder for TNR_PLAYER_LIVE."""
    env = environment(out)
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
    ended = session(out, "look", ["--tools", "", "--", "Reply with the single word: ready"],
                    [TOOL, f"mcp__Tnr__standIn_{nonce}"], lambda gate, hooks, game: False)
    gate, game = rows(os.path.join(out, "gate.jsonl")), rows(os.path.join(out, "game.jsonl"))
    if ended.how != BY_ITSELF or ended.code != 0 or ended.session is None:
        return f"a session with the stand-in alone could not be looked at: {ended.how} (with {ended.code})"
    if any(g.get("kind") != "start" and not g.get("refused") for g in gate) or any(g.get("at") != "connected" for g in game):
        return "the session that may call nothing made a call"
    return None if ended.gone else "its processes could not be seen to end"


def main():
    skip = {sys.argv[i + 1] for i, a in enumerate(sys.argv[:-1]) if a in ("--form", "--control")}
    named = [a for a in sys.argv[1:] if not a.startswith("--") and a not in skip]
    forms = [sys.argv[sys.argv.index("--form") + 1]] if "--form" in sys.argv else ["main", "subagent"]
    agent, more = "tnr-relay", []
    try:
        if os.name != "posix":
            raise Failed("the check is written for a POSIX system (Linux, macOS): how it ends a session's "
                         "processes and sees them gone is not made for this one")
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
