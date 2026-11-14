# AI player, the check for the operator's machine: correction handoff, after the review of 65974c02

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md` section 5. Written 2026-11-14, in answer to the review of
`65974c02` ("request changes before running this preflight on the operator's connected machine": B1 to B4,
and the overstatements in the five guards). A, `fable/ai-player-hook-relay` @ bf2231f6, was approved and is
not touched.

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-hook-proof
Reviewed: 65974c0259f01afdfc8ccc20fa448af06009a0f5
Review: docs/reviews/AI_PLAYER_RELAY_PREFLIGHT_REVIEW_20261114.md on
        chatgpt/review-ai-player-relay-preflight-20261114 @ 5d46d7ef (evidence; not merged)
Base of this correction: 65974c02. Not rebased: this head is three commits on it.
Code: 4eb2f15d, and the commit after it (two tests made tighter)
Head: the commit that adds this note (FROZEN; the exact SHA is in the correction message)
Holds: fable/ai-player-hook-relay @ bf2231f6 (approved), unchanged
Authority: RUL-2026-11-14-160, point 1
```

The diff to review is `git diff 65974c02 HEAD`. It changes nothing of the player: `git diff bf2231f6 HEAD --
player .claude` is still the one file of text, `player/OPERATOR.md`.

## Disposition

All four findings are **confirmed and corrected**, and so are the limits the review's table gives for guards
2 to 5. I did not find one I would argue with. The fallback claim of the first note ("what would reach the
game is one read of my own profile") was wrong, and is withdrawn.

| | What the review found | Now |
|---|---|---|
| B1 | Guard mode is no ceiling: with a profile in hospital, travelling or in a fight the brain asks for `hospital.npcHeal`, `travel.finishGlobalMove`, the fight's reads | A gate in front of every tool call lets through reads of my own profile and nothing else, three at most, whatever the brain asks for. The player's guard mode is not changed |
| B2 | With no log of the stand-in's, the watcher of released calls reset both its counts and never fired | Each log is read by itself. One that is not there has no rows; one that cannot be read fails the check. A call that the session shows an answer for and the stand-in did not write down ends the session, with a log or without |
| B3 | The first event was looked for by the bytes its line began with; a missing or unreadable one was passed over; and the watcher stood in front of nothing | The first event is told by its fields. The gate refuses every call until it has been read and found right; if it does not come in 45 seconds, or a line cannot be read, the session is ended and was never let through |
| B4 | Yes on any hook of each kind; a timed-out or failed session could pass; a folder used again passed on its old logs | Yes needs: stopped by the check after exactly three calls; each let through by the gate, made by one relay of the form asked for, with one hook before and one behind it, and written down and answered by the stand-in, all matched by the tool call's id; a folder nothing was written into before |

## What was built

**`preflight_gate.py` (new).** A hook the check gives each of its sessions on the command line
(`--settings`): `PreToolUse` on every tool, with `onFailure: block`, and `SessionStart` to write down that
such hooks run. It is not one of the relay's hooks and does not rest on them. It never allows; it refuses or
says nothing.

- Before the check has read the session's first event and written the session's id into `OUT/admitted`: it
  refuses everything. It waits ten seconds for that.
- After: `python3 -m player.brain next` with a token or none, and nothing else of Bash; in the subagent
  form, one start of the relay's agent by the main agent; a connector call that is a read of my own profile,
  three at most; nothing else.
- What a stand-in line stands for it looks up in the batch the relay holds (`live/client.json`), as the
  relay's hook does. What it cannot look up it refuses.

That a refusal of the gate wins over the relay's hook's "allow" was seen under Claude Code (runs c to f).

**`preflight.py` (rewritten; it no longer calls `proof.py`).**

- *Guard 2, the session that may call nothing.* It has no tools of Claude Code's own (`--tools ""`), the
  gate refuses all it could call, and it is started in the repository's root with the same options as the
  relays. The check reads its first event while it runs. It must list one server and exactly the stand-in's
  two tools. One of the two is named after the run (`standIn_<nonce>`), so a session that lists it under
  `Tnr` has this stand-in behind that name; the review is right that a displayed name alone is no identity.
- *Being let through.* The first event must list one connected server `Tnr` and no MCP tool beyond what
  that form's session lists; the stand-in's log must have this run's `connected` row; the gate's own mark
  must be there for that session. Only then is `OUT/admitted` written.
- *After a call.* Claude Code sends the tool call's id to the server, and the stand-in writes it down. So
  the gate's rows, the relay's hooks' rows and the stand-in's rows are matched by id, not counted.
- *Ending.* The session is started in a process group of its own and ended as a group; the stand-in's
  process id is in its log, and it is seen to be gone, or the check fails.
- *The shell.* `brain next` is run by the session's shell. A login shell with the check's variables is
  asked for `TNR_PLAYER_LIVE` first; if it is not the check's folder, nothing is started.
- *What it says.* One line a form with how the session ended, and "why not" in words; 0 only when every
  form passed with the agent file's own hooks; 2 when nothing was started.

**`fake_connector.py`.** The tool named after the run; the tool call's id and the stand-in's process id in
its rows; its text now says it answers any endpoint and is no firewall. Three more things it can be told for
trying the gate.

**`proof.py`.** It says it is for a machine with no connector, and why. `--own-env` is gone. Its two
watchers read through `preflight.py`'s readers, so B2 and B3 are closed there too; its text says they stand
in front of nothing.

**The texts.** `preflight.py`'s own text lists what is in front of a call and what only sees one
afterwards, apart. `player/OPERATOR.md` sends the operator to the check "at a head whose review has passed
the check itself", from a terminal and not from inside a Claude session, and says what to do if it ever
reports a call answered by something else. `PROOF.md`'s section on the check is rewritten. The first note is
marked superseded and otherwise kept.

## What is in front of a call, and what is not

Prevention: `--strict-mcp-config` (what the check rests on, as the review says); the session that may call
nothing; the gate.

Detection, after a call has gone, which cannot take it back: the match of calls by id; the clocks.

If `--strict-mcp-config` failed on some machine and the session that may call nothing did not show it, the
gate still bounds what could reach the game at three reads of my own profile for each form. RUL-160 allows
none, so that would be a breach to report, and the check says so in those words. I do not claim it cannot
happen; I claim nothing else can go.

## Tried under Claude Code 2.1.325, against the stand-in

`proof_runs/preflight2/`. No request of the game.

| | What was done | What came of it |
|---|---|---|
| a | the relay's hooks supplied on the command line (`--try`), both forms | both pass: three calls each, a hook before and behind each; it ends with 1, as it must without the file's own hooks |
| b | as the operator runs it, here | "no" for both forms: the trust dialog. Nothing was let through |
| c | the stand-in's profile says HOSPITALIZED | the gate refused `hospital.npcHeal` though the relay's hook had allowed it; the stand-in was given profile reads only |
| d | TRAVEL, as a subagent | the same for `travel.finishGlobalMove` |
| e | BATTLE with a fight's id | the same for `combat.getBattle` and `combat.getBattleEntries` |
| f | the gate never opened | every `brain next` refused though the relay's hook allowed it; nothing ran |
| g | the stand-in answers and writes no call down | ended after one call: "a call was answered, and not by the stand-in" |
| h | the stand-in writes nothing down at all | never let through; nothing sent |
| i | a folder that had a file in it | not started |

## Verification

| Command | Result |
|---|---|
| `python3 -m unittest docs/reviews/evidence/ai_player_hook_relay/test_preflight.py` | `Ran 30 tests`, `OK`. No session is started: the brain's batches are the suite's rig's, the logs are written by hand, and Claude Code is a stub with a clock the test moves |
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 636 tests`, `OK`, as at bf2231f6 |
| `python3 docs/reviews/evidence/ai_player_hook_relay/fake_connector.py --selftest` | exit 0 |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files, and `--commits 65974c02..HEAD`), `git diff --check 65974c02` | exit 0 each; 330 rulings |

The review's reproductions are among the tests: B1's table of four profiles
(`test_what_the_brain_asks_for_in_guard_mode_is_no_ceiling_and_the_gate_is`), B2's missing and unreadable
log, B3's event written with spaces, with other key order, missing and broken, B4's one hook for three calls,
the timed-out session, and the folder used again.

### Planted defects

28, each in a throwaway worktree, the 30 tests run on each. 27 failed a test as planted. One did not: with
the line removed that waits for the stand-in's `connected` row, every test passed, because two tests asked
only whether the refusal was final and not whether there was one. Those two tests are tighter now, and the
defect fails both.

| Planted | Tests that fail |
|---|---|
| B1: the gate lets any call of the batch through; takes a line it cannot look up for a read; has no bound; passes a read of another's profile | 4, 2, 1, 1 |
| B3: the gate lets through a session that was not looked at; is open to any session once one was | 2, 1 |
| The gate lets any command through; one that only begins as `brain next`; any other tool; a second subagent | 1 each |
| B2: an unreadable log is read as empty; an answered call the stand-in did not write down is passed over; a call with neither is never missed; a call at the stand-in that the gate did not let through is passed over | 2, 2, 1, 1 |
| B3: the first event is looked for by its bytes; a session that never shows it is not ended; another server beside the stand-in; the connector's other tools; before the stand-in was started; a stand-in of another run | 1, 2, 2, 1, 2, 1 |
| B4: one hook behind is enough for three; a timed-out session passes; another session's rows pass; a used folder; fewer than three calls; the stand-in's calls need not be the gate's | 1 each |
| A relay of the other form passes; the shell's own live folder is not looked at | 1 each |

## What is not shown

- **The terminal's own variables.** The check was run here with `--bare-env`. A session started from this
  cloud session needs that; the operator's does not.
- **A machine that has the game's connector.** Nothing here could show what `--strict-mcp-config` does
  with one, and I did not try to.
- **A yes for the agent file's own hooks.** Nobody can accept the dialog here.
- **Windows.** The ending of the process group and the check of the shell are written for it and not run.
- **`proof.py`'s watchers** have no tests of their own; they read through the tested readers, and `proof.py`
  is no longer what the operator is sent to.
- **The gate under a Claude Code that does not send the tool call's id to the server.** The check then fails,
  and says that it does not know that Claude Code.

## On A

Unchanged at bf2231f6. The review is right that the hooks do lean on the reader, through `hooked._look`, and
that the first note's "results come through hooks" did not cover that; its own run of the 86 hook tests on
typed transcripts with copies in them does. A test of that in the suite belongs with the next change to that
line.

## Live-game statement

Zero live requests. Every session started on this branch had the stand-in for its only MCP server. The one
live request of the whole line is the first probe's read. No gameplay action, no write, no credential.

## Open, for the director

As in the first note: how the live relay is started; whether the brain should refuse a relay without hooks;
which head the live gate is played from.

## Not begun

Running the check on the operator's machine. AP1's live gate.
