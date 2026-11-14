# Proving the relay's hooks on Claude Code itself: the plan

Written 2026-11-14 (RUL-2026-11-14-158: "Prepare to move on to proving the hook relay when the review
returns"). Nothing here has been run but the stand-in's self-test. It is run when the review of
`fable/ai-player-hook-relay` @ b5624861 has returned.

## What it is for

Three reviews have judged the hooks through tests that call them as functions, and through `together.py`,
which runs them as processes. None has run them under Claude Code's own hook engine. Each review lists the
same things as unverified:

- hooks declared in an agent file's front matter (the first probe's were in the project's settings file);
- `PostToolUseFailure`: whether it runs, and with what;
- a result too large for the conversation: what the hook behind the call is given;
- the tool calls of one message: whether Claude Code starts them together, and `brain next` with them;
- `onFailure: block` when a hook fails or runs out of time;
- when the relay's transcript has a tool's result: before `brain next` runs, or after;
- what a batch of a relay with hooks costs. The estimate (`estimate.py`) is put together from single requests.

## What it cannot reach

The game. The relay is run with one MCP server, `fake_connector.py` beside this file, which answers from the
suite's fixtures and makes no request of anything:

- `--strict-mcp-config --mcp-config <file>`: Claude Code loads the servers of that file and no others. The
  file names the stand-in as `Tnr`, so its tool is `mcp__Tnr__callEndpoint`, the tool the relay's agent names.
- Before anything is sent, the session's first event is read: it lists the MCP servers and tools the session
  has. If it lists anything but the stand-in, the run is ended there.
- `TNR_PLAYER_LIVE` points at a folder of the run's own. The brain there is a rehearsal: it claims no run
  lock and has no lease (`player/runlock.py`).
- The stand-in writes down every call it is given (`TNR_FAKE_LOG`). That log is the proof's record of what
  "the game" saw.

So it is not a play session, and it is no live request. It does use the plan: each run is a Haiku relay.

## The runs

Each is `claude -p` with `--agent tnr-relay`, the stand-in, `--output-format stream-json --verbose`, and a
debug file for the hooks. Each is ended by the brain's own stop word after a set number of batches, and by
a clock if that does not come.

| Run | The stand-in is told | What is read off |
|---|---|---|
| 1. As it is meant | nothing | `live/hook/log.jsonl`: the four hooks ran for every call, from the agent file. The stand-in's log: the calls the brain made, in order, each once. Whether two calls were out at once, and where `brain next` came. The relay's transcript: each stand-in, `ok`, no call and no result. `live/tokens.jsonl`: read from the cache, written, output, per batch |
| 2. A call fails | `fail` | whether the hook behind a failed call runs, what it is given, what the brain is handed |
| 3. A large result | `large` | what the hook behind the call is given: the result, or the notice that stands for it; whether the brain has the result |
| 4. A slow call | `slow`, under and over two minutes | the closing waits; over two minutes the batch is held and the late result ends it |
| 5. A hook that fails | an agent of the proof's own (`--agents`), the same but for one hook that exits 1, and one that sleeps past its timeout | whether the call is blocked (`onFailure: block`), and what the relay is told |
| 6. Low effort | nothing, with `--effort low` | the tokens of run 1 again, and whether a line was copied wrong: the difference the director asked to have measured (RUL-2026-11-14-159, point 3). Whether it is set is his to say |

What each run found goes into `PROOF.md` beside this file, with the stand-in's log and the hooks' log, as the
first probe's findings went into `PROBE.md`.

## What it costs

By the estimate, a batch of a relay with hooks counts about 5,000 fresh-input tokens of Haiku against the
plan. Six runs of some twenty batches are well under a million. The session that drives them costs more than
they do. The first run is made alone and read before the others, so a wrong estimate shows early.

## What it does not show

- Duet's machine: its Claude Code version, its trust dialog, the connector's tool name there.
- The real connector: how long its calls take, how it fails.
- A fight. The stand-in's game is the suite's, which does not fight back.

Those are the first live session's to show. That session is AP1's gate (one live PvP session on a Haiku relay
with zero missed turns and the token figures recorded). It is run on the head of the hook relay, with the
upkeep activities switched off, on Duet's machine, and the director starts it (RUL-2026-11-14-159, point 5).
It also counts what lands in `live/hook/late/` (point 1).
