# AI player, the hooks' proof: the check for the operator's machine. Handoff for review

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md`. Written 2026-11-14.

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-hook-proof
Holds: fable/ai-player-hook-relay @ bf2231f6 (merged in; that head has its own note,
       docs/reviews/AI_PLAYER_RELAY_PROMPT_HANDOFF.md)
Head: the commit that adds this note (FROZEN; the exact SHA is in the handoff message)
Authority: RUL-2026-11-14-158 (prove the hook relay), RUL-2026-11-14-160, point 1 (the check before the live gate)
```

Nothing on this branch has been reviewed. Against `fable/ai-player-hook-relay` @ bf2231f6 it differs in:

- `docs/reviews/evidence/ai_player_hook_relay/`: the proof's kit, its findings and what is kept of its runs;
- `player/OPERATOR.md`, "Hooks": the step for the operator, and one sentence on a relay without hooks;
- `docs/rulings/2026-11.md` and the index: RUL-2026-11-14-158, -159, -160;
- this note.

No code of the player differs: `git diff bf2231f6 HEAD -- player .claude` is that one file of text.

## What I ask to have reviewed

**`preflight.py`, and what it leans on in `proof.py` and `fake_connector.py`.** The rest of the kit made the
proof in this cloud session, where there is no game to reach. `preflight.py` is different: the operator runs
it on a machine that has the game's connector, before a live session. It starts Claude Code sessions there.
If it could reach the game it would be making gameplay calls nobody authorized. So the question for review is
one: **can it reach the game?**

What it does: the stand-in's self-test; a session that may call nothing is asked what MCP servers and tools it
has; then the relay's agent, as the file in that folder declares it, is started twice against the stand-in,
as a session's main agent and as a subagent of one, three batches each; it says for each whether the agent
file's hooks ran, and ends with 0 only when they did in both.

What keeps it from the game, and what each rests on:

| | What it is | Tried here |
|---|---|---|
| 1 | Every session is started with `--strict-mcp-config --mcp-config <file>`, and the file names one server, the stand-in | every session of the proof lists that one server |
| 2 | Before any relay: a session with the connector's tool disallowed is asked for its first event. Its MCP servers must be `["Tnr"]` and its MCP tools none. The stand-in has one tool; the game's connector has four. A connector that had taken the stand-in's name would show three more | `proof_runs/pf1`, `pf2`: passes with the stand-in. Not tried against a session that has the game's connector: there is none here that a started session inherits |
| 3 | A relay's session is ended as soon as its first event lists any MCP server but `Tnr` or any MCP tool but `mcp__Tnr__callEndpoint` | passes with the stand-in; the ending itself is not tried, for the same reason |
| 4 | A call that a hook released (`live/hook/log.jsonl`) and that is not in the stand-in's log within two seconds ends the session | run 14c: the stand-in was told to write nothing down; the session was ended after one call |
| 5 | The brain is a rehearsal in a folder of the run's own (`TNR_PLAYER_LIVE`), in guard mode, and the session is ended from outside. It releases nothing but `profile.getUser` | run 14b, and both forms of `pf2`: three calls each, all `profile.getUser` |

So if 1 to 4 all failed on some machine, what would reach the game is one read of my own profile, which
`CLAUDE.md` section 6 allows as a live read, and no gameplay call. I would rather say that than "it cannot".

**What was not tried.** `--own-env`, which is how the operator runs it (the sessions get the terminal's own
variables). In this cloud session a started session must be given a bare environment or it does not start
alone, so `preflight.py` was run here with `--bare-env`. And the pass itself: here nobody can accept the
trust dialog, so the true answer here is "no", for both forms, and that is what it says (`pf1`). With the
hooks supplied on the command line (`--hooks settings`) both forms pass (`pf2`); that tries the check, and
says nothing of a machine.

**It has no tests of its own** beyond the stand-in's self-test. It is 117 lines; `proof.py` is 235.

## What the proof found

`PROOF.md` beside the kit. 86 relay sessions against the stand-in on Claude Code 2.1.325. In short:

- The agent file's hooks are skipped in a folder whose trust dialog has not been accepted, for a main agent
  and for a subagent, and nothing is sent then. Given on the command line they ran for every call.
- `PostToolUseFailure`, a result too large for the conversation, `onFailure: block`, a slow call: each as
  the code expects.
- The tool calls of one message are run one after another. The hooks' waits are not reached unless a hook
  dies.
- A batch of a relay with hooks: 3,890 to 4,100 by the plan's count as a main agent, 3,500 to 3,630 as a
  subagent. The estimate's 97% under the live session's relay stands.
- Low effort: no difference that can be measured. Left unset (RUL-2026-11-14-160, point 3).
- A relay without hooks stopped itself in 7 sessions of 17. No relay with hooks did, in 58.

## Verification

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` on this branch | `Ran 636 tests`, `OK` |
| `python3 docs/reviews/evidence/ai_player_hook_relay/fake_connector.py --selftest` | exit 0 |
| `python3 docs/reviews/evidence/ai_player_hook_relay/preflight.py OUT --bare-env` | both forms "no", for the trust dialog; exit 1 (`proof_runs/pf1/said.txt`) |
| the same with `--hooks settings` | both forms ran: 5 hooks before `brain next`, 3 before a call, 3 behind; exit 1, as it must without the file's own hooks (`proof_runs/pf2/said.txt`) |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files and commits) | exit 0 each; 330 rulings on this branch |

## Live-game statement

Zero live requests on this branch. Every session it started had the stand-in for its only MCP server.

## Open, for the director

In the handoff message: how the live relay is started; whether the brain should refuse a relay without
hooks; which head the live gate is played from (this branch holds the hook relay's head and the check, and
differs from it in no code).

## Not begun

AP1's live gate. Running `preflight.py` on the operator's machine.
