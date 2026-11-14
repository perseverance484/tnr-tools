# The relay's hooks under Claude Code itself: what the proof found, 2026-11-14

The plan is `PROOF_PLAN.md` beside this file. The code is the hook relay as approved at `51fac81d`
(`fable/ai-player-hook-relay`), merged into `fable/ai-player-hook-proof`. Claude Code 2.1.325, in the cloud
session this work was done in. The relay's model was `claude-haiku-5-5` in every session.

**No request of the game was made.** Every session had one MCP server, the stand-in (`fake_connector.py`), and
one MCP tool, `mcp__Tnr__callEndpoint`. That is in the first event of each of the 36 sessions (`proof_runs/*/read.txt`,
first line), and `proof.py` now ends a session at once if its first event lists anything else.

36 relay sessions were run: 35 of ten batches each, and one that could send nothing. Between them the model
wrote 1,061 connector calls. Every one was a stand-in line, copied exactly. 1,055 reached the stand-in; the
other 6 were blocked on purpose (runs 5b to 5e). Together the sessions count 1.78 million fresh input tokens
of Haiku by the plan's count, and Claude Code reports $0.20 for them at the API's prices.

## In short

| What no review could verify | What the proof found |
|---|---|
| Hooks declared in the agent file's front matter | **Not shown here, and it fails closed.** In a folder whose trust dialog nobody has accepted, Claude Code skips them. `brain next` then asks for approval, and nothing is sent. Given to the session another way, the same four hooks ran for every call: on the command line as settings, and as the hooks of an agent defined on the command line. What is left is one step on the operator's machine (below) |
| `PostToolUseFailure` | It runs, for a tool that reports failure and for a connector that answers with an error. The brain is handed the error as the call's result and carries on |
| A result too large for the conversation | Claude Code saves it to a file under the transcript's folder and gives the hook a notice that names the file. The hook reads the file. The brain has the whole result; the model is shown `ok` |
| The tool calls of one message | Claude Code runs them one after another, in the order written. No two calls were out at once in any session, and no hook waited for another line. `brain next` in the same message runs last |
| `onFailure: block` | A hook that ends with 1, or runs past its timeout, blocks its call. Without that line the call is not blocked by the hook; it then needs a permission the hook would have given |
| When the transcript has a result | Not needed in ordinary running: the hooks hand results in. Where a result hook failed (run 5g), `brain next` found the result in the transcript and nothing was lost |
| What a batch costs | 4,200 to 4,400 by the plan's count when the model writes the batch and `brain next` in one message, 5,300 to 5,500 when it writes `brain next` in a message of its own. The estimate stands: 97 to 98% under the live session's relay |

Low effort (RUL-2026-11-14-159, point 3) made no difference that can be measured. It is below.

The director has since answered the three decisions this left (RUL-2026-11-14-160). What was done about them,
and what 50 more sessions found, is the last part of this note, "After the director's word": the wording that
was put into the relay's prompt, the relay as a subagent, a relay without hooks, and the check for the
operator's machine.

## The agent file's own hooks, and trust

Run 0 used the agent file as it is (`--agent tnr-relay`, hooks from its front matter). Claude Code's debug log:

```text
[ERROR] Skipping frontmatter hooks for main-thread agent 'tnr-relay': the folder its definition file came
from is not trusted (source: projectSettings). Run Claude Code in that folder once and accept the trust
dialog, or set projects["/home/user/tnr-tools"].hasTrustDialogAccepted: true in /root/.claude.json.
```

With no hook to allow it, `python3 -m player.brain next` got "This command requires approval", twice. The relay
made no connector call and ended. The stand-in was connected and was asked nothing. That is the right way to
fail, and it is what `player/OPERATOR.md` tells the operator ("in a folder whose trust dialog you have
accepted").

Accepting the dialog is the operator's own act. I tried to set that flag in a copy of the settings made for
the proof; the session's permission layer refused, and I did not go round it. So the hooks were given two
other ways, both of which Claude Code takes without the dialog because the one who starts the session gives
them:

- `--settings`: the four hooks, read out of the agent file by `proof.py`, as a settings document. 17 sessions.
- `--agents`: the agent file's whole definition (prompt, tools, model, hooks) under the name
  `tnr-relay-proof`. These are an agent's own hooks, as the file declares them. 18 sessions.

Both ran all four hooks for every call. What neither shows is that the same hooks, read from the file in a
trusted folder, are registered. That needs a session on a machine where the dialog has been accepted. The
check for it is `preflight.py` ("After the director's word", below). `proof.py` is not for such a machine: it
has nothing in front of a relay's calls but the one MCP server it is given.

## The runs

"Requests" are requests of the model. "The plan's count" is `0.1 x read from the cache + 1.25 x written to it +
fresh input + 5 x output`, in fresh input tokens of Haiku, over the whole session, divided by its batches
(RUL-2026-11-13-156). `proof_runs/table.jsonl` has every figure; `proof_runs/<run>/read.txt` is each session
as `proof_read.py` read it.

| Run | What | Hooks given by | Requests | Batches | Calls written, reached the stand-in | Hooks that passed: before `next`, before a call, behind a call, behind a failed call | The plan's count a batch |
|---|---|---|---|---|---|---|---|
| 0 | the agent file as it is, folder not trusted | the file | 3 | 0 | 0, 0 | none ran | |
| 1 | as it is meant | `--settings` | 12 | 10 | 30, 30 | 11, 30, 30, 0 | 4,212 |
| 1b | as it is meant, again | `--settings` | 21 | 10 | 30, 30 | 11, 30, 30, 0 | 5,432 |
| 1c | as it is meant, again | `--settings` | 20 | 10 | 30, 30 | 11, 30, 30, 0 | 5,403 |
| 2a | a call fails: the tool says so | `--settings` | 21 | 10 | 30, 30 | 11, 30, 29, 1 | 5,465 |
| 2b | a call fails: the connector says so | `--settings` | 21 | 10 | 30, 30 | 11, 30, 29, 1 | 5,381 |
| 3 | a result of 400,386 characters | `--settings` | 21 | 10 | 30, 30 | 11, 30, 30, 0 | 5,507 |
| 4a | a call that takes 20 s | `--settings` | 21 | 10 | 31, 31 | 11, 31, 31, 0 | 5,528 |
| 4b | a call that takes 150 s | `--settings` | 21 | 10 | 32, 32 | 11, 32, 32, 0 | 5,624 |
| 5a | as it is meant | `--agents` | 21 | 10 | 30, 30 | 11, 30, 30, 0 | 6,125 |
| 5b | the hook before a call ends with 1 | `--settings` | 21 | 10 | 30, 29 | 11, 29, 29, 0 | 5,499 |
| 5c | the same, without `onFailure: block` | `--settings` | 21 | 10 | 30, 29 | 11, 29, 29, 0 | 5,470 |
| 5d | the hook before a call runs past its timeout (5 s) | `--settings` | 21 | 10 | 33, 31 | 11, 31, 31, 0 | 5,823 |
| 5e | the same, without `onFailure: block` | `--settings` | 21 | 10 | 33, 31 | 11, 31, 31, 0 | 5,682 |
| 5f | the hook before `brain next` ends with 1 | `--settings` | 13 | 10 | 30, 30 | 11, 30, 30, 0 | 4,657 |
| 5g | the hook behind a call ends with 1 | `--settings` | 21 | 10 | 31, 31 | 11, 31, 30, 0 | 5,589 |
| 5h | a large result and a failed call, the hooks' inputs written down | `--settings` | 21 | 10 | 30, 30 | 11, 30, 29, 1 | 5,384 |
| 6a | low effort | `--settings` | 20 | 10 | 31, 31 | 11, 31, 31, 0 | 5,400 |
| 6b | low effort | `--settings` | 21 | 10 | 30, 30 | 11, 30, 30, 0 | 5,353 |
| 7a | with the rule that is tried | `--agents` | 12 | 10 | 30, 30 | 11, 30, 30, 0 | 5,057 |
| 7b | with the rule that is tried | `--agents` | 12 | 10 | 30, 30 | 11, 30, 30, 0 | 5,049 |
| 7c | with the rule that is tried | `--agents` | 12 | 10 | 30, 30 | 11, 30, 30, 0 | 5,076 |
| 7d | as it is meant | `--agents` | 12 | 10 | 30, 30 | 11, 30, 30, 0 | 4,365 |
| 7e | as it is meant | `--agents` | 12 | 10 | 30, 30 | 11, 30, 30, 0 | 4,410 |
| 8a | with the rule that is tried | `--agents` | 12 | 10 | 30, 30 | 11, 30, 30, 0 | 4,400 |
| 8b | as it is meant | `--agents` | 12 | 10 | 30, 30 | 11, 30, 30, 0 | 4,425 |
| 8c | with the rule that is tried | `--agents` | 12 | 10 | 30, 30 | 11, 30, 30, 0 | 4,379 |
| 8d | as it is meant | `--agents` | 21 | 10 | 30, 30 | 11, 30, 30, 0 | 5,419 |
| 8e | with the rule that is tried | `--agents` | 12 | 10 | 30, 30 | 11, 30, 30, 0 | 4,249 |
| 8f | as it is meant | `--agents` | 21 | 10 | 30, 30 | 11, 30, 30, 0 | 5,355 |
| 8g | with the rule that is tried | `--agents` | 12 | 10 | 30, 30 | 11, 30, 30, 0 | 4,301 |
| 8h | as it is meant | `--agents` | 21 | 10 | 30, 30 | 11, 30, 30, 0 | 5,320 |
| 8i | with the rule that is tried | `--agents` | 12 | 10 | 30, 30 | 11, 30, 30, 0 | 4,347 |
| 8j | as it is meant | `--agents` | 21 | 10 | 30, 30 | 11, 30, 30, 0 | 5,515 |
| 8k | with the rule that is tried | `--agents` | 12 | 10 | 30, 30 | 11, 30, 30, 0 | 4,295 |
| 8l | as it is meant | `--agents` | 12 | 10 | 30, 30 | 11, 30, 30, 0 | 4,317 |

Every session but run 0 ended with the brain's own word, `STOP session ended by the director: asleep at home`,
with nothing held, nothing gone and nothing owed in `client.json`, and an empty inbox. The model ran no command
but `brain next` in any of them.

## What each hook is given, and what the model is shown

Run 5h wrote down the input of the two result hooks (`proof_runs/run5h/hook_runs.*.seen`).

- **Before a call.** The model's stand-in, `{"endpointName": "player.relay", "input": {"b": T, "n": k}}`. The
  hook answers `allow` with the real call as `updatedInput`. The session's permission mode was `default` and
  it had no permission rule: the hook's `allow` is what lets the call go (RUL-2026-11-14-159, point 2).
- **Behind a call.** `tool_input` is the real call, after the swap. `tool_response` is the result's content.
  The hook's `updatedToolOutput` replaces it, and the model is shown `ok`.
- **Behind a failed call** (`PostToolUseFailure`). `error` is the failure's text, `is_interrupt` false,
  `tool_input` the real call. There is no `tool_response`. The hook cannot replace what the model is shown, so
  the model sees the error text (39 characters here). It carried on, as its rules say.
- **A result of 400,386 characters.** `tool_response` is not the result but
  `"Error: result (400,386 characters across 1 line) exceeds maximum allowed tokens. Output has been saved to
  <the transcript's folder>/tool-results/mcp-Tnr-callEndpoint-<n>.txt. ..."`. `relay._text` knows that notice
  and reads the file. The brain had the result and reported nothing wrong.

The model's conversation holds stand-ins and `ok`, and nothing of the game: no endpoint's name and no field of
a result is in any message of run 1's transcript. The transcript file on disk does keep each hook's output in
rows of its own (`hook_success`), which are not sent to the model. So the real calls are on the operator's
disk in the relay's transcript; the results are not.

## The tool calls of one message

In all 35 sessions a message held several tool calls: up to five connector calls, and in 17 sessions
`brain next` with them. Claude Code started each only when the one before had its result and the hook behind
it had ended. The stand-in never had two calls at once. The hook before a call ran in 26 to 640 milliseconds
(33 in the middle, of 1,020), except once a session where it spent the brain's own pacing (five to ten
seconds; 34 in run 5g, after the wait described below). None waited for a line before it.

So the hooks' waits (two seconds for a line to be taken, two minutes for one to end) are not reached in
ordinary running. A call that took 20 seconds, and one that took 150 (runs 4a, 4b), were simply waited for by
Claude Code; nothing timed out and the batch went on in order. The waits were reached three times, each by a
hook that was made to fail:

- **Run 5g, the hook behind a call ends with 1.** Claude Code goes on: the model keeps the result (17
  characters here; in a fight it would be a whole battle read). The result is not on record, so the next
  `brain next` waited the two minutes, then found the result in the relay's transcript and handed it in. The
  brain missed nothing.
- **Runs 5d and 5e, by accident.** I had set that hook's timeout to five seconds. Its fifth run was the one
  made to sleep, as meant. Later the real hook spent ten seconds of the brain's pacing, and Claude Code ended
  it too, with the line taken and no call made. The next `brain next` waited the two minutes and handed the
  batch in without that call. Nothing was sent twice and nothing was sent wrong. The agent file gives that
  hook 300 seconds.

Two minutes is long inside a fight. Both cases need a hook to die, which did not happen in any session where
I did not cause it.

## A hook that fails

| Run | The hook | Declared with `onFailure: block` | What Claude Code did | What the model was shown |
|---|---|---|---|---|
| 5b | before a call, ends with 1 | yes | `PreToolUse command hook failed; blocking (onFailure: "block")`. The call did not go | `PreToolUse:mcp__Tnr__callEndpoint hook error: [...]: failed; blocking ...` |
| 5d | before a call, runs past its timeout | yes | `PreToolUse command hook timed out; blocking (onFailure: "block")`. The call did not go | the same, `timed out` |
| 5f | before `brain next`, ends with 1 | yes | blocked | the hook error. It ran `brain next` again, which passed |
| 5c | before a call, ends with 1 | no | the hook's failure blocks nothing. The call then asks for permission; in a session with nobody to ask it is refused | `Claude requested permissions to use mcp__Tnr__callEndpoint, but you haven't granted it yet.` |
| 5e | before a call, runs past its timeout | no | the same | the same |

In 5c and 5e the stand-in line was not sent, but only because that session had no permission for the tool. On
a machine where the connector's tool is allowed in settings, the line would go to the connector as the model
wrote it, with the endpoint `player.relay`, which the game does not have. With `onFailure: block` it cannot
go, whatever the machine allows. The line is doing its work.

After a blocked call the relay carried on with the rest of the batch. The brain was handed the batch without
that call and made what it still needed in the batches after. No session stalled.

## What a batch costs

Run 1, batch by batch (`proof_runs/run1/tokens.jsonl`), fits these to within a few tokens:

| | Measured | The estimate took (`estimate.py`) |
|---|---|---|
| The conversation a relay is born with | 7,887 | 5,000 |
| Added by one call and its `ok` | 137 | 270 |
| Added by one line of the next batch, as printed | 28 | 30 |
| Added by `brain next` and the rest | 196 | 100 |
| Output for one call | 98 | 100 |
| Output for `brain next` | 104 | 60 |
| Thinking | one to four times a session | 150 a batch |
| Requests a batch | 1 or 2 (below) | 1 |

Ten batches took a relay's conversation from 7,900 tokens to about 15,000: about 700 a batch.

By the plan's count a batch cost:

- **4,212 to 4,425** in the 11 undisturbed sessions, born warm, where the model wrote the batch's calls and
  `brain next` in one message (one request a batch);
- **5,320 to 5,515** in the 6 undisturbed sessions, born warm and at the usual effort, where it wrote
  `brain next` in a message of its own (two requests a batch: the conversation is read once more, and a
  little more is written).

A relay born cold writes the conversation it is born with instead of reading it. Runs 5a and 7a to 7c were
the first with their prompt: about 700 more a batch over their ten batches, once.

The estimate's stretch (the first relay's 27 batches of the live session, 4.96 million as it ran) comes to
0.11 million with the measured figures and one request a batch, 0.16 million with two; the estimate said
0.14 million. That is 98 and 97% under the session's relay, where the estimate said 97%.

What this does not measure: a fight. The stand-in's game does not fight back, so these are batches of one to
five reads and moves. What the model holds for a call does not depend on what the call returns, so the figure
for a call should carry over; how many calls a fight's batch has is the live session's to show.

## `brain next` in a message of its own

The agent file says "Do every line, in order, as tool calls in ONE message", and that the last line is the
next `brain next`. Haiku did that in 6 of the 26 sessions that had the file's wording (and for a single
batch in two more), and in the others sent the calls, waited for their results, and then sent `brain next`
alone. Either is correct. The second costs a quarter more.

I tried one more line under the agent's Rules, on the proof's own copy of the agent (`--rule`), not in the
agent file:

> The last line of a batch, the `brain next`, goes in the same message as the calls of the batch. Never wait
> for the results of the calls before you send it: you do not read them.

With it, 9 sessions of 9 wrote every batch in one message. Run side by side with them, 4 of 8 sessions
without it did. No session with the rule copied a line wrong or sent anything it should not.

The agent file is reviewed code, so I did not change it then. The director has since said to
(RUL-2026-11-14-160, point 2): see "After the director's word".

## Low effort

RUL-2026-11-14-159, point 3: measured here, not set.

| | Requests | Output tokens | The plan's count a batch | Thinking | A line copied wrong |
|---|---|---|---|---|---|
| Low effort (6a, 6b) | 20, 21 | 4,394, 4,230 | 5,400, 5,353 | 1, 1 | none |
| As it is (1b, 1c) | 21, 20 | 4,382, 4,432 | 5,432, 5,403 | 3, 1 | none |

The difference is about one part in a hundred, less than the difference between two sessions of the same
setting. The relay already thinks next to nothing: there is nothing for low effort to save. The director said
yes "if the saving is high". It is not, so I would leave it unset. It is his to say.

## What the proof does not show

- The agent file's own hooks in a trusted folder (above): `preflight.py` on the operator's machine.
- The real connector: how long its calls take and how it fails.
- A fight, and the count of calls in its batches.
- A Claude Code that starts the tool calls of a message together. This one does not. The hooks' ordering
  for that case is held by the suite and by `together.py`, not by this proof.

## To run it again

```text
python3 docs/reviews/evidence/ai_player_hook_relay/fake_connector.py --selftest
python3 docs/reviews/evidence/ai_player_hook_relay/proof.py OUT --look
python3 docs/reviews/evidence/ai_player_hook_relay/proof.py OUT --hooks settings --batches 8
python3 docs/reviews/evidence/ai_player_hook_relay/proof_read.py OUT
```

`proof.py`'s own text lists the rest: `--control` for the stand-in, `--break` for a hook that fails,
`--no-block`, `--effort`, `--hooks agents`, `--rule`. Each session is a Haiku relay of about ninety seconds.

## Kept from the runs

`proof_runs/table.jsonl`, one line a session. `proof_runs/<run>/read.txt` for every session. For runs 1, 2a,
3, 5b, 5g and 5h also the stand-in's log (`game.jsonl`), the hooks' log (`hook_log.jsonl`), the brain's token
log and events, and the hooks as they were given. This session's own paths are taken out. Claude Code's
streams and debug logs are not kept; the lines quoted here are from them.

## After the director's word

RUL-2026-11-14-160: the trust check before the live gate, the one-message rule before it, low effort unset.
50 more sessions, against the stand-in as before; no request of the game. `proof_runs/table2.jsonl` has them;
runs 9 to 14.

### The wording that went into the prompt

`fable/ai-player-hook-relay` @ 995625fe changes one sentence of step 2 of `player/RELAY.md` (and the agent
file, which is that prompt):

> The last line is always the next `brain next`. Run it exactly as printed, in that same message: never wait
> for the results of the calls first.

It is in the step, not under Rules as the wording tried above was, so that the section on a batch with `put`
lines, which comes after and says "one line at a time, not in one message", reads as the exception it is.

With it, every session with hooks wrote every batch in one message: 23 of 23 (runs 10a to 10f with the prompt
given to the kit; 11a to 11j with the files as committed; 13a to 13c and 13e to 13h as a subagent). No line
was copied wrong. A relay that is printed `put` lines still did them one at a time, call then `put`, in 3
sessions of 3 (10g to 10i), as it did before (9b to 9d).

### The relay as a subagent

Every session above ran the relay as its session's main agent. A session that is doing other work starts it
with the Agent tool, as a subagent. Runs 13a to 13h did that (`--as-subagent`):

| | As the main agent | As a subagent |
|---|---|---|
| The hooks ran for every call | yes | yes: given as the agent's own (13a to 13c), and as settings beside the agent file (13e, 13f) |
| The agent file's hooks, folder not trusted | skipped, nothing sent (run 0) | skipped, nothing sent (13d) |
| Who the hooks take the relay for | the session's id | the subagent's id |
| A large result, a failed call (13g) | as above | the same |
| A hook before a call that ends with 1 (13h) | blocked | blocked |
| The conversation it is born with | 7,900 tokens | 4,090 |
| A batch, by the brain's token log | 3,890 to 4,100 | 3,500 to 3,630 |

The difference at birth is the repository's `CLAUDE.md`. The agent file says `omitClaudeMd: true`. Claude Code
leaves the file out for a subagent and not for a main agent: a main-agent relay had `CLAUDE.md` in front of
it in every session here (it is in its transcript, and one quoted it; below). So a subagent is the cheaper
relay by about a tenth, and the one that reads nothing but its own prompt.

### A relay without hooks

Not the relay that is to be played. It is what the brain falls back to when no hook runs: it prints the
calls themselves and reads the results in the relay's transcript. 17 sessions (9a, 10j, 10k, 11k, 11l, 12a to
12l), started with the two tools allowed on the command line.

- **It stopped itself in 7 sessions of 17**, within five batches. In 4 it made one call of a batch of five,
  ran `brain next`, saw what it had done and stopped. In 3 it read the calls it was carrying, took
  `combat.getBattleHistory` of another player for "other players' data" under `CLAUDE.md` section 6, and
  refused to go on. The old wording and the new did the same: 3 of 6 each, side by side (runs 12).
- **No relay with hooks stopped itself**, in 58 sessions that ran to their end. It is printed five stand-ins
  where the other is printed five calls with their fields, and it has nothing to judge.
- **Its calls were counted twice.** Fixed at f4d042d0 (`fable/ai-player-hook-relay`). With a debug file this
  Claude Code keeps beside each message a copy of what it sent the API, tool calls and all; the brain's
  reader took a tool call from any row, so every batch had as many "calls the batch did not ask for" as it
  had calls, and the call budget was charged for them (9a: seven findings in eight batches). After the fix:
  none (11k, 12a to 12l).
- **The `put` fallback cannot run with nobody to ask.** Where the brain finds no transcript it asks for each
  result by a `put` line. Claude Code's permission check does not pass that command by a rule ("Contains
  brace with quote character"); it asks each time (9b to 9d, 10g to 10i).

So a relay whose hooks are not running is not merely dearer on this Claude Code: it is not reliable. That is
what makes the next check a condition of the live session and not a courtesy.

The director has since ruled that the brain turns such a relay away (RUL-2026-11-14-161): it is given no name
and no batch unless he has said it may play. The runs above were made before that; `proof.py --hooks none`
now says so for the run, as he would.

### The check for the operator's machine

`preflight.py`, beside this file, with its gate `preflight_gate.py`. It starts the agent file as it is, as a
main agent and as a subagent, against the stand-in, for three reads of my own profile each, and says for each
form whether the file's hooks ran for every one of those calls.

The first version of it (at 65974c02) was reviewed and sent back
(`chatgpt/review-ai-player-relay-preflight-20261114` @ 5d46d7ef, B1 to B4). It leaned on the brain's guard
mode to ask for nothing but profile reads, which guard mode does not promise; on two watchers that looked at
a session after it had started, one of which could not see a missing log and the other a first event written
with a space in it; and it said yes on any hook of each kind. What is said of it above ("So a relay whose
hooks are not running...") stands; what was said of its safety did not.

As it is now, its own text says what stands in front of a call and what only sees one afterwards. In short:

- **In front.** One MCP server and no other (`--strict-mcp-config`), which is what it rests on. A session
  that has no tools of Claude Code's own and whose every call is refused is started first with the same
  options: it must list the stand-in's two tools and no other under the one server's name, and one of the two
  is named after the run, so it cannot be another server's. Then a gate, given on the command line, in front
  of every tool call of a relay's session: it refuses everything until the session's first event has been
  read and found right, and after that everything but `brain next`, one start of the relay's agent, and three
  reads of my own profile, whatever the brain asks for.
- **Afterwards.** Claude Code names each tool call to the server, so the gate's rows, the relay's hooks' rows
  and the stand-in's rows are matched call by call. A call that the session shows an answer for and the
  stand-in did not write down ends the session.
- **Yes** means: stopped by the check after exactly three calls; each let through by the gate, made by one
  relay of the form asked for, with one hook before it and one behind it, and written down and answered by
  the stand-in; in a folder nothing was written into before.

Tried under Claude Code, against the stand-in (`proof_runs/preflight2/`):

| | What was done | What came of it |
|---|---|---|
| a | the relay's hooks supplied on the command line, both forms | both forms pass: three calls each, a hook before and behind each |
| b | as the operator runs it | "no" for both forms: the trust dialog. Nothing was let through |
| c | the stand-in's profile says HOSPITALIZED | the brain asked for `hospital.npcHeal`; the gate refused it though the relay's hook had allowed it; the stand-in was given a profile read and nothing else |
| d | TRAVEL, as a subagent | the same for `travel.finishGlobalMove` |
| e | BATTLE | the same for `combat.getBattle` and `combat.getBattleEntries` |
| f | the gate never opened | every `brain next` refused; nothing ran |
| g | the stand-in answers and writes no call down | ended after one call: "a call was answered, and not by the stand-in" |
| h | the stand-in writes nothing down at all | the session was never let through; nothing was sent |
| i | a folder that something was written into before | not started |

In c to e the check says no and gives a reason that is about the calls that followed the refused one; that is
right for a session in which something asked for more than a read.

30 tests run it off line (`test_preflight.py`): the review's four findings as it ran them, the gate's every
refusal, and the watching loop with a clock the test moves.

It has not been run with the terminal's own variables, which is how the operator runs it: a session started
from this cloud session needs a bare environment. And it has not said yes for the agent file's own hooks
anywhere, since nobody can accept the dialog here.

### What is still not shown

The agent file's hooks in a trusted folder, which is what `preflight.py` is for; the real connector; a fight.
