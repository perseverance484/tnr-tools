# AI player: the brain turns a relay without hooks away. Handoff for review

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md`. Written 2026-11-14.

**Corrected after review** (`chatgpt/review-ai-player-relay-refusal-20261114` @ 64f7d87a; the correction's
note is `docs/reviews/AI_PLAYER_RELAY_REFUSAL_REREVIEW1_HANDOFF.md`). Two things this note says were not so at
this head: that the director's word is asked for "where a batch is printed, every time" (it was asked for
when `brain next` began, and a batch was printed after the word had gone); and that the batch of a relay
turned away after it was let in "is held until the operator says `stopped`" (a relay with hooks has to take
over first). This note is otherwise kept as it was written.

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-relay-refusal
Base: fable/ai-player-hook-proof @ 071ba1b1dcf6f28f7fadcf25b05af62d102daedd (under re-review; it holds the hook
      relay's approved head, bf2231f6). That head is not moved: this work is a branch on it.
Commits: f45c6aa9 (the ruling), b170be16 (the change)
Head: the commit that adds this note (FROZEN; the exact SHA is in the handoff message)
Authority: RUL-2026-11-14-161 (on this branch)
```

The diff to review is `git diff 071ba1b1 HEAD`. Unlike the two heads before it, this one **changes the
player's code**: `player/hooked.py`, one line of `player/brain/client.py`, the director's settings.

If the re-review of 071ba1b1 asks for changes there, they are made on `fable/ai-player-hook-proof` and merged
into this branch; this note's diff then starts at the head that review approves.

## The director's word

RUL-2026-11-14-161, his answers to the three decisions the proof left:

1. The live relay is started as a **subagent**.
2. The brain **refuses** a relay without hooks.
3. The live gate is played from `fable/ai-player-hook-proof`, at a head that holds everything review has
   approved.

2 is the code here. 1 is a paragraph of the operator's guide. 3 changes no file.

## What it was

When no hook ran in front of a relay's `brain next`, the brain was not told otherwise and printed the relay
the calls themselves, as before the hooks. It did so without a word: the operator's guide called it "a relay
without hooks plays as before".

The proof on Claude Code 2.1.325 found that such a relay is not the relay that was proven. It stopped of its
own accord in 7 sessions of 17: it made one call of a batch of five and went on, or it read the calls it was
carrying and refused one. A relay with hooks did so in none of 58 (`PROOF.md`, "A relay without hooks").

## What was built

**`hooked.bare(live, state, token, hooks)`**, called first in `next_batch`, before `_greet`:

```python
    mine = token is not None and token == state.get("token") and not state.get("hooks")
    if hooks or not (token is None or mine):
        return None
    said = relay.read(os.path.join(live, "control.json"))
    return None if isinstance(said, dict) and said.get("relay_without_hooks") is True else BARE
```

- A relay that comes **with no token and no hook** is new. It is told
  `STOP this relay's hooks are not running, and the brain does not play through a relay without them`, and
  nothing else happens: no name, no change to `client.json`, no request to the brain. So it replaces no relay
  that is running. Had the refusal been the brain's, the newcomer would have been named first, and a running
  relay's batch would have been gone with it.
- A relay **without hooks that comes for the batch it was named for** is told the same. That is one that was
  let in while the director's word stood, or was named before this code. Nothing is taken from it; the batch
  it had is held until the operator says `stopped`, as for any relay that does not come back.
- **Not changed:** a relay that was named with hooks and comes without them is told what it was told before
  (`hooked.stop`, `STOP the relay's hooks are not running`). A relay that was replaced is told so, and its
  batch is over, as before.

**The director's word.** `python3 -m player.brain set relay_without_hooks=true`. It is a setting like the
others (`console.SETTINGS`, true or false; the world model begins with false), so the brain applies it and
writes the event. `brain next` reads it where it runs, from `live/control.json`, and takes `true` and nothing
else: not `"true"`, not 1, not a file it cannot read.

That there is a switch at all is my reading of "Refuse", from the recommendation he answered ("refuse unless
you switch that on"). The ruling says so. Without the switch the fallback would be gone for good, and with it
the only way to play at all on a machine where the hooks cannot be made to run.

**The suite's rigs.** Most of the suite hands its batches to a relay without hooks: 162 tests failed with the
refusal in. Their rigs now say, as the director would, that such a relay may play:

- `support.Rig(bare=True)` writes the word into `control.json` at version 0, which is where a world model
  begins, and sets it in the world model as already applied. So `brain next` reads it, and no brain, of this
  version or an older one, has anything new to apply: no event is added, and the walk, the fuzz and the
  simulated fights print what they printed at `184ce648`, to the byte.
- Twelve set-ups, in seven test files, make or take their live folder themselves; `support.bare(live)` does
  the same for them.
- Five tests write `control.json` whole, where `brain set` would change one setting and keep the others;
  `support.and_bare({...})` keeps the word in what they write.
- One program that is run by an old version's code (`test_rereview9.OLD_ASLEEP`) writes the word before the
  new code's relay starts in it. A sixth write of `control.json` is inside another such program, and is left
  as it was: the old code has no `support.and_bare`, and does not refuse.

The new tests say nothing of such a relay, and see it turned away
(`test_hook_relay.ARelayWithoutHooksIsTurnedAway`, nine tests).

**The operator's guide** (`player/OPERATOR.md`, "Hooks"): start the relay as a subagent, and why; the check
is run for that form; what a relay that is turned away is told, and that it replaces nobody; how the director
lets one play, and what happens when the word is taken back.

**The proof's kit.** `proof.py --hooks none` sets the word for its run, as the director would; `--no-word`
leaves it out. `PROOF.md` has a paragraph saying its runs without hooks were made before the ruling.

## The protocol number is not changed, and why

`player/relay.py` says to change it "whenever the meaning of one of these records changes, or the rules by
which the brain admits a batch's calls", and when in doubt.

No record's meaning changes: `client.json`, a request, an answer, a waiting batch, a receipt and the ledger
are written and read as at 10. The brain admits a batch's calls by the same rules. What changes is whom
`brain next` prints a batch to, and that is asked where a batch is printed, every time: a batch that was made
or left waiting before this code is not printed to a relay without hooks either. So there is no record made
under the old rule that this code would act on as if it had been made under the new one, which is what the
number is for. A new number would also hold a minute's calls after the update for no batch that needs it.

That is my reading. If the review reads "when in doubt" the other way, it is one number and its line.

## Under Claude Code itself, against the stand-in

`docs/reviews/evidence/ai_player_hook_relay/proof_runs/refusal/runs.jsonl`. No request of the game.

| Relay | What happened |
|---|---|
| Without hooks, and no word of the director's | its first `brain next` printed the STOP line; it ended and replied with that line; no relay on record; the stand-in was given nothing |
| Without hooks, with the word | it was named and played, the calls themselves; after six calls it stopped itself over a mistake of its own, as such relays did in the proof |
| With hooks of its own, as a subagent, no word | it played to the session's end, as before |
| The check for the operator's machine, hooks supplied, as a subagent | it passed, as before |

## Verification on the code commit (b170be16)

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 645 tests`, `OK`, three runs in a row, none skipped (`071ba1b1`: 636) |
| `python3 -m unittest -v player.tests.test_hook_relay` | `Ran 95 tests`, `OK` (86) |
| `python3 -m unittest docs/reviews/evidence/ai_player_hook_relay/test_preflight.py` | `Ran 30 tests`, `OK`, as at `071ba1b1` |
| `python3 docs/reviews/evidence/ai_player_hook_relay/together.py 30` | 30 runs, each as before |
| `python3 -m player.tests.test_walk 200 300` | the output of `184ce648`, to the byte |
| Two fuzz scripts and three simulated fights of mine, not in the repository | the output of `184ce648`, to the byte |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 46 tests`, `OK` |
| `python3 scripts/player_allowlist.py check`, and `report --check` | exit 0, both |
| The four pilot tests (`state/player/dauntless/tools/tests/`) | exit 0 each |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files, and `--commits 071ba1b1..HEAD`), `git diff --check 071ba1b1` | exit 0 each; 331 rulings |

### Planted defects

Eleven, each in a throwaway worktree of the code commit, the whole suite run on each. Every one fails a test.

| Planted defect | Tests that fail |
|---|---|
| A relay without hooks is never turned away | 4 |
| It is turned away when it is new, and not when it comes for a batch | `test_when_the_word_is_taken_back_the_relay_it_let_in_is_told_to_stop` |
| It is named first and turned away after | 3, among them `test_it_replaces_no_relay_that_is_running` |
| Any word that is not empty lets it play | `test_the_word_is_true_and_nothing_else` |
| With no settings file it plays | 3 |
| A relay with hooks is asked for the word too | 3, among them `test_a_relay_with_hooks_is_not_asked_for_the_word` |
| One named with hooks that comes without is told the new line | `test_one_that_was_named_with_hooks_and_comes_without_is_told_what_it_was_told_before` |
| One that was replaced is told the new line | 2, among them `test_one_that_was_replaced_is_told_so_as_before` |
| It is not a setting the director can change | 2 |
| A world does not begin with the setting | `test_it_is_a_setting_of_the_directors` |
| The setting takes any value | the same |

## Size

The player's code is 6,373 lines in 32 files (`bf2231f6`: 6,351): `player/hooked.py` 381 (361),
`player/brain/client.py` 400, as it was. The same two files are over 400 lines, the same 17 functions over
12 branches. The tests are 12,044 lines (11,899).

## Known limits

- **The brain writes no event for a relay it turns away.** The refusal is `brain next`'s, before the brain
  is asked. What says so is the STOP line, which the relay ends on and replies with.
- **A relay without hooks that was running when this code arrives** is turned away at its next
  `brain next`, and its batch is held until the operator says `stopped`. No live session is running.
- **`brain put`**, by which a relay with no transcript hands a result in, is as it was. It prints no batch.
- **With the word, a relay without hooks is what it was in the proof**: unreliable on this Claude Code. The
  guide says so where it says how to give the word.

## Live-game statement

Zero live requests. Every session started here had the stand-in for its only MCP server. No gameplay action,
no write, no credential.

## Not begun

Running the check on the operator's machine. AP1's live gate, which waits for the re-review of 071ba1b1, for
this review, and for the check.
