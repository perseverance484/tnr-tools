"""A stand-in for the game's connector, for proving the relay's hooks on Claude Code itself.

    {"mcpServers": {"Tnr": {"command": "python3",
                            "args": ["docs/reviews/evidence/ai_player_hook_relay/fake_connector.py"]}}}

An MCP server on standard input and output with one tool, callEndpoint, as the game's connector has. It makes
no request of anything. What it answers is the suite's stand-in for the game (player/tests/support.py). Under
the name Tnr in an MCP config, Claude Code calls its tool mcp__Tnr__callEndpoint: the tool the relay's agent
file names. So the relay, its hooks and the brain run as they are, and nothing they send leaves the machine.

Every call it is given is written to the file TNR_FAKE_LOG names, when it comes and when it is answered, so a
run shows what reached "the game", in which order, and whether two calls were out at once.

TNR_FAKE_CONTROL names a JSON file, read at every call, that makes it misbehave on purpose:

    {"fail": ["profile.getUser"]}          a call of that endpoint fails
    {"slow": {"profile.getUser": 4}}       it is answered after so many seconds
    {"large": ["profile.getUser"]}         its answer is too large for a conversation
    {"hang": ["profile.getUser"]}          it is never answered
    {"broken": ["profile.getUser"]}        the connector itself answers with an error, not the tool
    {"only": {"profile.getUser": [2]}}     with any of those: only the second call of that endpoint
    {"unseen": true}                       it answers and writes nothing down, as if something else had answered:
                                           the proof's guard must end the session (proof.py)
    {"status": "ASLEEP"}                   my profile says so (with `brain set end_session=true`, the brain
                                           then tells its relay to stop)

    python3 docs/reviews/evidence/ai_player_hook_relay/fake_connector.py --selftest
"""
import json
import os
import subprocess
import sys
import threading
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, ROOT)

from player.tests.support import fixture, user  # noqa: E402

TOOL = {"name": "callEndpoint",
        "description": "Call one endpoint of the game. A stand-in: it answers from fixtures and reaches nothing.",
        "inputSchema": {"type": "object", "required": ["endpointName"],
                        "properties": {"endpointName": {"type": "string"}, "input": {"type": "object"},
                                       "select": {"type": "array", "items": {"type": "string"}}}}}
OUT = threading.Lock()
SEEN = {}


def say(message):
    with OUT:
        sys.stdout.write(json.dumps(message) + "\n")
        sys.stdout.flush()


def note(row):
    path = os.environ.get("TNR_FAKE_LOG")
    if path and not (control().get("unseen") and row.get("at") != "connected"):
        with OUT, open(path, "a", encoding="utf8") as f:
            f.write(json.dumps(row) + "\n")


def control():
    try:
        with open(os.environ.get("TNR_FAKE_CONTROL") or "", encoding="utf8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


def game(endpoint, select):
    """What the stand-in for the game answers: as player/tests/test_hook_relay.py, Hooks.answer."""
    battle, log = fixture()
    if endpoint == "profile.getUser":
        return dict(user().data, **({"userData.status": control()["status"]} if control().get("status") else {}))
    if endpoint == "combat.getBattle":
        return dict(battle, **({"battle.usersEffects": []} if "battle.usersEffects" in (select or []) else {}))
    if endpoint == "combat.getBattleEntries":
        return log
    return {"success": True}


def call(rid, args):
    endpoint, how = args.get("endpointName"), control()
    row = {"endpoint": endpoint, "input": args.get("input"), "select": args.get("select"), "came": round(time.time(), 3)}
    with OUT:
        SEEN[endpoint] = SEEN.get(endpoint, 0) + 1
        if endpoint in (how.get("only") or {}) and SEEN[endpoint] not in how["only"][endpoint]:
            how = {"status": how.get("status")}                   # (not this one: it is answered as it is meant)
    note(dict(row, at="came"))
    if endpoint in (how.get("hang") or []):
        return
    time.sleep(float((how.get("slow") or {}).get(endpoint, 0)))
    if endpoint in (how.get("broken") or []):
        note(dict(row, at="answered", answered=round(time.time(), 3), failed=True, broken=True))
        return say({"jsonrpc": "2.0", "id": rid, "error": {"code": -32000, "message": "the stand-in was told to break"}})
    if endpoint in (how.get("fail") or []):
        result = {"content": [{"type": "text", "text": "the stand-in was told to fail this call"}], "isError": True}
    else:
        data = game(endpoint, args.get("select"))
        if endpoint in (how.get("large") or []):
            data = dict(data, pad="x" * 400_000)
        result = {"content": [{"type": "text", "text": json.dumps(data)}], "isError": False}
    note(dict(row, at="answered", answered=round(time.time(), 3), failed=result["isError"]))
    say({"jsonrpc": "2.0", "id": rid, "result": result})


def serve(lines=sys.stdin):
    for line in lines:
        try:
            message = json.loads(line)
        except ValueError:
            continue
        rid, method, params = message.get("id"), message.get("method"), message.get("params") or {}
        if method == "initialize":
            note({"at": "connected", "client": params.get("clientInfo"), "came": round(time.time(), 3)})
            say({"jsonrpc": "2.0", "id": rid, "result": {
                "protocolVersion": params.get("protocolVersion") or "2024-11-05", "capabilities": {"tools": {}},
                "serverInfo": {"name": "tnr-stand-in", "version": "1"}}})
        elif method == "tools/list":
            say({"jsonrpc": "2.0", "id": rid, "result": {"tools": [TOOL]}})
        elif method == "tools/call" and params.get("name") == "callEndpoint":
            threading.Thread(target=call, args=(rid, params.get("arguments") or {}), daemon=True).start()
        elif method == "ping":
            say({"jsonrpc": "2.0", "id": rid, "result": {}})
        elif rid is not None:                                     # (a notification gets no answer)
            say({"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": f"no such method: {method}"}})


def selftest():
    """Start it as Claude Code would, speak to it, and see what it says."""
    log = os.path.join(os.environ.get("TMPDIR") or "/tmp", f"fake_connector_selftest_{os.getpid()}.jsonl")
    p = subprocess.Popen([sys.executable, os.path.abspath(__file__)], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                         text=True, env=dict(os.environ, TNR_FAKE_LOG=log))

    def ask(rid, method, params=None):
        p.stdin.write(json.dumps({"jsonrpc": "2.0", "id": rid, "method": method, "params": params or {}}) + "\n")
        p.stdin.flush()
        return json.loads(p.stdout.readline())
    try:
        assert ask(1, "initialize", {"protocolVersion": "2025-06-18"})["result"]["serverInfo"]["name"] == "tnr-stand-in"
        p.stdin.write(json.dumps({"jsonrpc": "2.0", "method": "notifications/initialized"}) + "\n")
        assert [t["name"] for t in ask(2, "tools/list")["result"]["tools"]] == ["callEndpoint"]
        got = ask(3, "tools/call", {"name": "callEndpoint", "arguments": {"endpointName": "profile.getUser", "input": {}}})
        assert got["result"]["isError"] is False and json.loads(got["result"]["content"][0]["text"]) == user().data
        assert ask(4, "tools/call", {"name": "item.buy", "arguments": {}})["error"]["code"] == -32601
        with open(log, encoding="utf8") as f:
            rows = [json.loads(x) for x in f]
        assert [(r.get("endpoint"), r["at"]) for r in rows] == [(None, "connected"), ("profile.getUser", "came"),
                                                                 ("profile.getUser", "answered")]
    finally:
        p.kill()
        if os.path.exists(log):
            os.unlink(log)
    print("the stand-in answers as a connector does, with the suite's game, and writes down what it was asked")


if __name__ == "__main__":
    selftest() if sys.argv[1:] == ["--selftest"] else serve()
