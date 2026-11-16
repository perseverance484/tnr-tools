# The probe of Claude Code's hooks, 2026-11-13

Before the hook relay was built (RUL-2026-11-13-157). Claude Code 2.1.323, in the cloud session this work was
done in. One live request was made: a read of my own profile's status through the connector. No gameplay
action and no write.

## What was run

Hooks in the project's `.claude/settings.json`, for the length of the probe and removed after it:
`PreToolUse` on `Bash` and on `mcp__.*`, `PostToolUse` and `PostToolUseFailure` on `mcp__.*`, each running
`probe_hook.py` (beside this file). The script did nothing unless a marker file armed it and the tool call was
a subagent's, so the session's own calls went through untouched. A subagent on Haiku was then given steps to
carry out, one tool call each.

A subagent declared in a new agent file was tried first. This session did not load the file, so hooks in an
agent file's own front matter were not exercised. That is how the relay's agent declares them.

## What happened

| Step the model was given | What the hook did | What the model was shown |
|---|---|---|
| Bash `echo probe-1` | let it through with the subagent's id put behind it (`updatedInput`) | `probe-1 stamped:<id>:general-purpose` |
| Bash `ls /` | refused it | `PreToolUse:Bash hook error: probe: not the listed command` |
| a harmless MCP tool, with a made-up argument | replaced the input, then replaced the result (`updatedToolOutput`) | `stub 1` |
| the same, with another argument | refused it | `PreToolUse:… hook error: probe: not in the batch` |
| the connector's tool, `endpointName` and `input` described in words | refused all three: the model had sent `"text relay"` for `relay` | the refusal, three times |
| the connector's tool, `{"endpointName": "relay", "input": {"t": "probe", "n": 1}}` | put `profile.getUser` with `select: ["userData.status"]` in its place; replaced the result | `stub 1` |
| the same stand-in with `"n": 2` | refused it | the refusal |
| the first stand-in again | refused it: it had been used | the refusal |

The connector answered the one read with `{"userData.status":"AWAKE"}`. The two refused stand-ins and the three
miscopied ones never reached it.

## What a hook is given

`hook_inputs.json` has every input and answer, with the session's ids, paths and its own details taken out.

- Every hook: `session_id`, `transcript_path` (the session's, not the subagent's), `cwd`, `permission_mode`,
  `agent_id` and `agent_type` for a subagent's call, `hook_event_name`, `tool_name`, `tool_input`,
  `tool_use_id`; for an MCP tool also `mcp_server` (`name`, `source`).
- `PostToolUse`: `tool_input` is the input that ran, so the one the hook put in; `tool_response` is a list of
  text blocks, `[{"type": "text", "text": "…"}]`; `tool_use_id` is the one `PreToolUse` had; `duration_ms`.
- A refusal reaches the model as `PreToolUse:<tool> hook error: <the reason>`.

## What the subagent's transcript kept

For the replaced call it has the stand-in as the tool's input and `stub 1` as its result: neither the real
call nor the real result. So a relay with hooks cannot be read from its transcript, and the hooks hand the
results in.

Its token use, request by request (a general-purpose subagent, so a large conversation to begin with):

| Request | Read from the cache | Written to it | Output |
|---|---|---|---|
| the first stand-in call, with thinking | 67,267 | 2,032 | 236 |
| the next call, after the stub | 69,299 | 269 | 97 |
| the next, after a refusal | 69,568 | 166 | 97 |

So a stand-in call and its `ok` add some 170 to 270 tokens to the conversation, and take about 100 of output.

## What was not tried

- Hooks declared in an agent file (above).
- `PostToolUseFailure`: no call failed. The relay's hook for it is written from the documentation.
- A result too large for the conversation: whether the hook is given the result or the notice that replaces
  it. The relay's hook reads either.
- Several tool calls in one message, and whether Claude Code starts them together.
- `onFailure: "block"` on a hook that fails.
- Anything on Duet's machine.
