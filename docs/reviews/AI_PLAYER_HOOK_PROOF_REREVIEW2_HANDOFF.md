# AI player, the check for the operator's machine: second correction handoff, after the re-review of 071ba1b1

**Sent back in part** (`chatgpt/review-ai-player-preflight-rereview2-20261116` @ eefb063e): C3 and the refusal
to start on a system the check was not written for stand. C1 and C2 were open at narrower places than this
note covers: what was seen in the wait was not kept, and "running" was asked before a look that takes time,
not "before it sends the first signal" as this note says. The correction and its note:
`docs/reviews/AI_PLAYER_HOOK_PROOF_REREVIEW3_HANDOFF.md`. This note is kept as it was written.

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md` section 5. Written 2026-11-16, in answer to the re-review
of `071ba1b1` ("request changes": C1 and C2, medium, block; C3, low, does not).

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-hook-proof
Reviewed: 071ba1b1dcf6f28f7fadcf25b05af62d102daedd
Review: docs/reviews/AI_PLAYER_PREFLIGHT_REREVIEW1_REVIEW_20261116.md on
        chatgpt/review-ai-player-preflight-rereview1-20261116 @ 1e238719 (evidence; not merged)
Base of this correction: aa73867c53b1f7ab7a8577d0402e7195d43f0824, the head of fable/ai-player-relay-refusal,
        approved (chatgpt/review-ai-player-relay-refusal-rereview1-20261115 @ 10e8d928). It is 071ba1b1 and
        the refusal on it; the check's four files are the same bytes in both.
Code: 34c2d2c7 (C1 to C3), 72c772e8 and the commit after it (three more tests)
Head: the commit that adds this note (FROZEN; the exact SHA is in the correction message)
Authority: RUL-2026-11-14-160, point 1; RUL-2026-11-14-161, point 3
```

**The branch was brought forward, not rebased.** `fable/ai-player-hook-proof` stood at 071ba1b1. Its review had
returned, and the refusal that was built on that head had been approved meanwhile, so the branch was moved to
aa73867c by fast-forward and the correction made there. The diff to review is `git diff aa73867c HEAD`. For
the check's own files it is the same as `git diff 071ba1b1 HEAD`.

So this head holds the hook relay (bf2231f6, approved), the refusal (aa73867c, approved) and this correction.
Once it is approved it is the head RUL-2026-11-14-161, point 3, means: the one the live gate is played from.

It changes nothing of the player's code. `git diff aa73867c HEAD -- player .claude` is one sentence of
`player/OPERATOR.md`.

## Disposition

All three are **confirmed and corrected**. The review's two schedules for C1 and its session for C2 are tests
now, and each fails on 071ba1b1's code.

| | What the re-review found | Now |
|---|---|---|
| C1 | The process group was signalled only while its leader lived, and the wait was for the leader alone. A child that did not end when asked was never ended and never looked for; the check said the session was gone | The group is ended whatever its leader has done, with what descends from it and the stand-in: asked, then ended. True only when none of them is left running |
| C2 | What a session had left was looked at before whether it still ran. One that had ended by itself and left every row of a passing one was put down as "stopped after the check's calls" | The process is looked at first, and again in the moment it is stopped. Yes needs a session that was running when the check ended it |
| C3 | An error for a call the stand-in had not written down was read as "refused before it went" | Such a call ends the session, unless the relay's own hook refused it on record. The texts say that an error does not tell |

## C1: the ending

```python
def end(p, game):
    known = {the stand-in's process id, from its log}
    for sig in (signal.SIGTERM, signal.SIGKILL):
        listed = processes()                    # `ps`: every process, with its parent, its group and its state
        if listed is None: return False
        left = family(listed, p.pid, known)     # the group, what descends from it or from one seen before, those
        known |= left
        signal the group, and each of `left` that is outside it
        for PATIENCE seconds:
            if the leader has ended and family(...) is empty: return True
    return False
```

- **Whatever the leader has done.** The group is signalled by its id, which is the leader's process id for as
  long as one member lives. Nothing is skipped because the leader has ended.
- **Asked, then ended.** `SIGTERM`, five seconds, `SIGKILL`, five seconds. A process that ends when asked is
  not ended by force.
- **Seen gone.** By what the system lists, not by a wait on one process. A process that has ended and waits
  to be collected runs nothing and is not counted.
- **One that leaves the group** is still found while its parent is one of the family, and from then on by its
  id. The stand-in is found by the id in its own log, wherever it is.
- **Where the system cannot be asked**, or a process cannot be ended, it is false, and the form does not pass.

What it cannot find: a process that has left the group, whose parent has ended, and that was never seen while
either was so. Nothing the check starts does that; the stand-in, which Claude Code starts, is covered by its
log.

**POSIX only.** The first version had a branch for Windows that was written and never run. It is gone. On a
system that is not POSIX the check starts nothing and says why. The shell check had skipped Windows; it has no
such case now.

## C2: stopped, or ended by itself

The loop looked at `done(...)` first; while that held, the look at the process was in an `elif` that was not
reached. It looks at the process first now, in every round, so also in the moment's wait before it stops a
session that is done:

```python
                if how is None and p.poll() is not None:
                    how = BY_ITSELF
                elif how is None and done(gate, hooks, game):
                    since = since or now
                    if now - since >= 0.2:
                        how, running = STOPPED, p.poll() is None
```

`session` gives back how it ended as five things, not a word: the words; the session's id; that its
processes were seen gone; that it was running when the check ended it; what it ended with. It looks once more
at the process before it sends the first signal, and one that has ended in that moment is put down as ended
by itself. `verdict` passes only `STOPPED` with `running` and `gone`.

It does not ask for an exit code of 0: a session the check ends says 143 here. That is in what it prints
("it ended with"), for the operator to see.

The session that may call nothing must end by itself with 0. Before, any end by itself was taken.

## C3: an error is not a refusal

For a call the gate let through and the stand-in has not written down, `astray` now tells four cases apart:

| What is there for the call | What is made of it |
|---|---|
| A row of the relay's own hook that refused it | It never went: that hook stands in front of the call, and says so on record |
| An answer that is no error | "a call was answered, and not by the stand-in" |
| An error | "came back as an error and is not in the stand-in's log: whether it went cannot be told". The session is ended and the form fails |
| Nothing | twenty seconds, then "has no result" |

So an error that the session's permissions made, and one that a server made after it had been given the
call, are both stopped at. I did not try to tell them apart by the error's text: that text is Claude Code's to
change. The operator's guide says to tell the director of either line.

## Under Claude Code 2.1.325, against the stand-in

`proof_runs/preflight3/`. No request of the game.

| | What was done | What came of it |
|---|---|---|
| a | the relay's hooks supplied, both forms | both pass; each session was running when it was stopped, and ended with 143 |
| b | as the operator runs it, here | "no" for both forms: the trust dialog. Each session ended by itself with 0 |
| c | the stand-in's profile says HOSPITALIZED | the gate refused the heal; one read reached the stand-in; the form fails |
| f | the gate never opened | nothing ran; the session ended by itself |
| g | the stand-in answers and writes no call down | "a call was answered, and not by the stand-in", after one call |
| j | the stand-in answers with an error and writes nothing down, as a subagent | "came back as an error and is not in the stand-in's log: whether it went cannot be told", after one call |

After the check had returned, the system listed no process of any of its sessions: looked for at once and in
the seconds after, for three runs of the check (a main agent, a subagent, and a session ended early).

## Verification

| Command | Result |
|---|---|
| `python3 -m unittest docs/reviews/evidence/ai_player_hook_relay/test_preflight.py` | `Ran 41 tests`, `OK` (071ba1b1: 30). Six of them start processes of this machine: five that do nothing, and the stand-in. None starts Claude Code |
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 651 tests`, `OK`, as at aa73867c |
| `python3 docs/reviews/evidence/ai_player_hook_relay/fake_connector.py --selftest` | exit 0 |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files, and `--commits aa73867c..HEAD`), `git diff --check aa73867c` | exit 0 each; 331 rulings |

The eleven tests that are new:

| Test | What it holds |
|---|---|
| `TheSessionIsEnded` (6) | C1, with a leader of its own process group and a child that does not hear a request to end: the leader alive; the leader ended and collected before; a child that left the group; the stand-in by its log; signals that go nowhere, and a system that cannot be asked, are not "gone"; a process that ends when asked is not ended by force; what the system lists, and who is of the family |
| `test_a_session_that_ended_by_itself_is_not_one_the_check_stopped_whatever_it_left` | C2, through `form`: every row of a passing session, and a process that ended with 1 or 0, at once or in the wait before the stop; and the same rows with a process that runs, which passes |
| `test_the_loop_looks_at_the_process_before_it_looks_at_what_was_done` | C2, in the loop alone |
| `test_an_error_for_a_call_does_not_say_that_it_never_went` | C3, as the review ran it: the stand-in itself, told to fail and to write nothing down |
| `test_on_a_system_it_was_not_written_for_nothing_is_started` | the POSIX refusal |
| `test_the_session_that_may_call_nothing_ends_by_itself_and_well_or_nothing_is_started` | `look`: it must end by itself, with 0, having made no call |

The loop's tests put a stub in place of `end`, as the review notes; `TheSessionIsEnded` runs the real one.
A fault of my own tests came out on the way: the loop's tests began again inside one test and restored what
they had replaced to what an earlier beginning had put there, so a later test could meet a stub. They
restore to what was there when the file was loaded.

### Planted defects

Sixteen, each in a throwaway worktree, the offline tests run on each. Fourteen failed a test as planted. Two
did not, and showed two things no test asked: the second place where the system is asked what runs, inside
the wait, and what the session that may call nothing ended with. Each has a test now, and each of the two
defects fails it.

| Planted | Tests that fail |
|---|---|
| C1: the group is ended only while its leader lives | 2 |
| C1: the wait is for the leader alone | 4 |
| C1: what does not end when asked is not ended | 4 |
| C1: a child that left the group is not looked for | 2 |
| C1: the stand-in's process is not looked for | 1 |
| C1: where the system cannot be asked in the wait, the session is called gone | 0 at first; 1 now |
| C1: a process that has ended and waits to be collected is counted as running | 5 |
| C1: a session whose processes were not seen gone passes | 1 |
| C2: what the session left is looked at before whether it runs | 1 |
| C2: a session said to be stopped is not asked whether it was running | 1 |
| C2: one that ended in the moment it was stopped keeps the word | 2 |
| C3: an error for a call is passed over | 2 |
| C3: a refusal of another call lets this one's error pass | 1 |
| C3: a hook that passed is taken for one that refused | 1 |
| The session that may call nothing may end with an error | 0 at first; 1 now |
| On a system it was not written for it starts all the same | 1 |

## What is not shown

- **The terminal's own variables.** Run here with `--bare-env`, as before.
- **A machine that has the game's connector**, and **a yes for the agent file's own hooks**. As before.
- **macOS.** `ps -A -o pid= -o ppid= -o pgid= -o stat=` is POSIX; it was run on Linux.
- **Windows.** The check does not run there. If the operator's machine is Windows, that is a thing to settle
  before the check, not after.
- **`proof.py`'s watchers** still end a session with one signal to one process. `proof.py` says it is for a
  machine with no connector, and is not what the operator is sent to.

## Live-game statement

Zero live requests. Every session started on this branch had the stand-in for its only MCP server. No
gameplay action, no write, no credential.

## Not begun

Running the check on the operator's machine. AP1's live gate.
