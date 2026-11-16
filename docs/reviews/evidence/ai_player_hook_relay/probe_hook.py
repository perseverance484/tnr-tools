"""A probe of Claude Code's hooks for the relay (2026-11-13). Run by the hooks of .claude/agents/tnr-probe.md.
Every hook input is kept under probe/. It lets one Bash command through, stamped; one read of this session's own
details through a harmless MCP tool, with its input replaced and its output replaced; and, only when the file
probe/LIVE_OK exists, exactly one read of my own profile status through the TNR connector."""
import json, os, sys
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "probe")
event = sys.argv[1]
raw = sys.stdin.read()
try:
    inp = json.loads(raw)
except ValueError:
    inp = {"unparsed": raw}
tool, ti = inp.get("tool_name", ""), inp.get("tool_input") or {}
# Registered in the project's settings for the length of the probe, so it also runs for the main conversation:
# it does nothing at all unless the probe is armed and the call is a subagent's.
if not os.path.exists(os.path.join(D, "ARMED")) or not inp.get("agent_id"):
    sys.exit(0)
n = len([f for f in os.listdir(D) if f.startswith(event + "-") and not f.endswith(".out.json")]) + 1
with open(os.path.join(D, f"{event}-{n}.json"), "w") as f:
    json.dump(inp, f, indent=1)

def out(obj):
    with open(os.path.join(D, f"{event}-{n}.out.json"), "w") as f:
        json.dump(obj, f, indent=1)
    print(json.dumps(obj))
    sys.exit(0)

def pre(decision, reason, updated=None):
    h = {"hookEventName": "PreToolUse", "permissionDecision": decision, "permissionDecisionReason": reason}
    if updated is not None:
        h["updatedInput"] = updated
    out({"hookSpecificOutput": h})

def once(name):
    try:
        os.close(os.open(os.path.join(D, name), os.O_CREAT | os.O_EXCL | os.O_WRONLY))
        return True
    except FileExistsError:
        return False

if event == "pre":
    if tool == "Bash":
        if ti.get("command") == "echo probe-1":
            pre("allow", "probe: the listed command", dict(ti, command=f"echo probe-1 stamped:{inp.get('agent_id')}:{inp.get('agent_type')}"))
        pre("deny", "probe: not the listed command")
    if tool.endswith("get_session"):
        if ti == {"session_id": "probe-1"}:
            pre("allow", "probe: call 1", {})
        pre("deny", "probe: not in the batch")
    if tool.endswith("callEndpoint"):
        if ti.get("endpointName") == "relay" and ti.get("input") == {"t": "probe", "n": 1} \
                and os.path.exists(os.path.join(D, "LIVE_OK")) and once("LIVE_DONE"):
            pre("allow", "probe: the one read", {"endpointName": "profile.getUser", "input": {}, "select": ["userData.status"]})
        pre("deny", "probe: not in the batch")
    pre("deny", "probe: not a tool of the probe")

if event == "post":
    r = inp.get("tool_response")
    shape = open(os.path.join(D, "SHAPE")).read().strip() if os.path.exists(os.path.join(D, "SHAPE")) else "auto"
    text = f"stub {n}"
    if shape == "str" or (shape == "auto" and isinstance(r, str)):
        stub = text
    elif shape == "blocks" or (shape == "auto" and isinstance(r, list)):
        stub = [{"type": "text", "text": text}]
    elif shape == "content" or (shape == "auto" and isinstance(r, dict) and "content" in r):
        stub = {"content": [{"type": "text", "text": text}]}
    else:
        stub = {"result": text}
    out({"hookSpecificOutput": {"hookEventName": "PostToolUse", "updatedToolOutput": stub}})
sys.exit(0)
