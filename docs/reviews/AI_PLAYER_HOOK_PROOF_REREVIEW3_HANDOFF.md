# AI player, the check for the operator's machine: third correction handoff, after the re-review of c2efaaa2

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md` section 5. Written 2026-11-16, in answer to the second
re-review ("request changes": C1 and C2 open at narrower places, both medium; C3 closed; the refusal to start
on a system the check was not written for sound).

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-hook-proof
Reviewed: c2efaaa266c8668a3440cb9340f98aeeea6bb3c5
Review: docs/reviews/AI_PLAYER_PREFLIGHT_REREVIEW2_REVIEW_20261116.md on
        chatgpt/review-ai-player-preflight-rereview2-20261116 @ eefb063e (evidence; not merged)
Base of this correction: c2efaaa2. Not rebased: this head is four commits on it.
Code: 6768d464 (C1, C2), b75a6136 and the commit after it (tests)
Head: the commit that adds this note (FROZEN; the exact SHA is in the correction message)
Holds: the hook relay (bf2231f6, approved) and the refusal (aa73867c, approved)
Authority: RUL-2026-11-14-160, point 1; RUL-2026-11-14-161, point 3
```

The diff to review is `git diff c2efaaa2 HEAD`: `end` and `family` in `preflight.py`, three lines of `session`,
the tests, and the texts. `preflight_gate.py`, `fake_connector.py`, `proof.py`, the player's code and `.claude`
are not touched.

## Disposition

Both are **confirmed and corrected**. Each was a place where the last correction did less than its note
said: it said "seen gone" of a family it did not keep up, and "before it sends the first signal" of a look
that came before a wait.

| | What the review found | Now |
|---|---|---|
| C1 | Only the look before each signal was kept. A child that appeared after it, was seen in the wait while its parent was of the session, left the group and then lost that parent was looked for no more: gone, with the child running | Every look is kept, the looks in the wait too. What is newly seen is asked to end, or ended, at once |
| C2 | Whether the session was running was asked before the system was asked what runs, which can take seconds. A session that ended by itself in that time was put down as stopped by the check | It is asked inside the ending, after the first look and in the moment before the first signal. That answer is the one the verdict has |

## C1: what was built

`end` is one loop for each of the two signals, and every round of it does the same four things:

```python
            listed = processes()
            left = family(listed, p.pid, known)
            known |= left                              # every look, not only the first of a round
            if running is None: running = p.poll() is None
            if p.poll() is not None and not left: return True, running
            signal: the group, once a round; and each of `left` that has not had this round's signal
```

- **Kept.** A process that is once seen with a parent of the family is in `known` from then on, and is found
  by its own id whatever becomes of its parent or its group.
- **Asked at once.** One that is first seen in the wait is sent the round's signal then, and not left for the
  round that ends by force. The test holds that too.
- **Gone** is: the leader has ended, and nothing of the family as kept is running.

**What it still cannot find**, said as narrowly as I can: a process that leaves the group and loses its parent
between two looks, which are a tenth of a second and one `ps` apart, and is in neither. The review calls that
limit distinct from this finding, and I agree it is. The stand-in is found by the process id in its own log
whatever it does.

## C2: what was built

`end` gives back two things: that the family was seen gone, and that the session was running when it was
first asked to end. The second is asked after the first look at what runs, on the line before the signals
are sent. `session` takes it from there; the loop's own flag and its look before the ending are gone, since
neither was at the signal.

```python
            gone, running = end(p, last)
    stopped = how == STOPPED and running
    return Ended(BY_ITSELF if how == STOPPED and not running else how, whose, gone, stopped, p.poll())
```

Between that look at the process and the signal there is no call that waits. What is left is the moment
between two lines of one function, which the review does not ask to have closed.

The check still does not ask for an exit code of 0. A session it ends says 143 under Claude Code, and -15
where the process does nothing with the signal; both are printed.

## One thing the review did not ask for

`family` finds what `end` then signals. It starts from the leader and from the process ids in the stand-in's
log. It now never contains this program, a process this program descends from, or the system's first
process, and does not go through them to what descends from them, whatever a log names. Nothing writes such
an id there: the stand-in writes its own. But a log is a file, and what would follow from a wrong number in
it is every process of the machine asked to end. I came on it writing the test for C2, where the rows of a
session are written by hand.

## The tests

44 (c2efaaa2: 41). The three that are new start processes of this machine that do nothing, and use the real
`end`, `session`, `form` and `verdict`:

| Test | What it holds |
|---|---|
| `test_a_child_that_is_seen_in_the_wait_is_not_forgotten_when_its_parent_has_gone` | C1, as the review ran it: a leader with no child; asked to end, it starts one in a session of the child's own and ends when it is let. The system's answer in the wait is a true one, taken while the child is still the leader's and handed back after the leader has gone. The child is of the family in that answer, and it does not end when it is asked to. `end`: gone, and the child is not running, by the round that ends by force |
| `test_and_one_that_ends_when_asked_is_asked_as_soon_as_it_is_seen` | The same with a child that hears: ended in less than the wait of a round |
| `test_a_session_that_ends_by_itself_while_the_system_is_asked_what_runs_was_not_stopped` | C2, as the review ran it, through `form`: every row of a passing session, written for this run; a process in Claude Code's place that ends with 1 when it is let, and is let during the first look of the ending. Not passed: ended by itself, with 1. And the same with a process that runs until it is ended: passed, stopped, -15 |

`test_what_the_system_lists` also holds that this program, its parent and the first process are never of the
family, and that a child of this program can be.

The six tests of `TheSessionIsEnded` that were there take `end`'s two answers now: `(True, True)` for a
session that was running, `(True, False)` for one whose leader had ended before.

## Under Claude Code 2.1.325, against the stand-in

`proof_runs/preflight4/`. No request of the game.

| | What was done | What came of it |
|---|---|---|
| a | the relay's hooks supplied, both forms | both pass; stopped after the check's calls; each ended with 143 |
| b | as the operator runs it, here | "no" for both forms: the trust dialog; each ended by itself with 0 |
| g | the stand-in answers and writes no call down | "a call was answered, and not by the stand-in" |
| j | the stand-in answers with an error and writes nothing down, as a subagent | "came back as an error and is not in the stand-in's log: whether it went cannot be told" |

After the four had returned the system listed no process of any of their sessions.

## Verification

| Command | Result |
|---|---|
| `python3 -m unittest docs/reviews/evidence/ai_player_hook_relay/test_preflight.py` | `Ran 44 tests`, `OK` |
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 651 tests`, `OK`, as at aa73867c |
| `python3 docs/reviews/evidence/ai_player_hook_relay/fake_connector.py --selftest` | exit 0 |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files, and `--commits c2efaaa2..HEAD`), `git diff --check c2efaaa2` | exit 0 each; 331 rulings |

`PROOF.md` said 39 tests where the head had 41. It says 44, which is what this head has.

### Planted defects

Nine, each in a throwaway worktree, the offline tests run on each. Seven failed a test as planted. Two did
not, and the first of them was the review's own finding: with only the first look of a round kept, every
test passed. My test's child ended when it was asked to, and since what is newly seen is asked at once, it
was gone before anyone needed to remember it. The child in that test does not hear now, and a second test has
one that does. The other was a line of the new guard that no test reached. Both defects fail a test now.

| Planted | Tests that fail |
|---|---|
| C1: what is seen in the wait is not kept | 0 at first; 1 now |
| C1: what is kept is not used to see that the session is gone | 1 |
| C1: what is newly seen in the wait is not asked to end | 1 |
| C1: the round that ends by force does not reach the group | 3 |
| C2: whether it runs is asked before the system is asked what runs | 2 |
| C2: the loop's own word is kept, whatever the ending saw | 1 |
| C2: a session that was not running when asked keeps the word stopped | 1 |
| What a log names may be this program or what it descends from | 1 |
| What is in the session's group may be this program | 0 at first; 1 now |

## What is not shown

As in the second note: the terminal's own variables; a machine that has the game's connector; a yes for the
agent file's own hooks; macOS; and that the check does not run on Windows.

## Live-game statement

Zero live requests. Every session started on this branch had the stand-in for its only MCP server. No
gameplay action, no write, no credential.

## Not begun

Running the check on the operator's machine. AP1's live gate.
