# AI player overhaul: light reads on his turn. Implementation handoff

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md`. Written 2026-11-13.

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-light-polls
Base: 661f3f63f9bd51887c402ce00f76e8e9735cb2ea (fable/ai-player-ap2: AP2's first part, approved on
      chatgpt/review-ai-player-ap2-rereview2 @ 6bf7d297). Not rebased: this head is three commits on it.
Code: 4ad93aae33b31efd010f936c5ec86a23813cd0ab. No file under player/ has changed since.
Supersedes: 6016624e82158162f39242d46b1aba7a85eba8d6, the first handoff of this change, which no review had begun on
Head: the commit that changes this note for RUL-2026-11-13-156 (FROZEN; the exact SHA is in the handoff message)
Intended integration: the AI player line, behind AP2's first part. Not `main`, and not before the director says.
Authority: RUL-2026-11-12-154 (light polls on his turn, approved as the live-session handoff proposed them);
           RUL-2026-11-13-155 (the state his turn starts on stays in the fight's archive);
           RUL-2026-11-13-156 (the tokens to save are the ones the plan's limits count)
```

The diff to review is `git diff 661f3f63 HEAD`. Objective: in a fight against a player, read the full state
twice a round and watch the rest of his turn with a light read, without losing a turn.

## Read this first: what it buys, by the count the director has named

This note supersedes the one at `6016624e`. That one said the saving depended on how tokens are counted and
that I did not know which count was the director's. He has said (RUL-2026-11-13-156): the cost is usage
against the plan's limits on this account. The code is the same as at `6016624e`; what changed is this
section, the evidence script, the design's section 4.7 and the ruling.

**How the plan counts.** Anthropic's pages say that what a request reads again from the prompt cache counts
at the cached rate and less than new content. The plan's weights are not published, so the API's price ratios
stand in for them: a tenth for what is read from the cache, 1.25 for what a request adds, 5 for its output.
The relay's model, Haiku 5.5, costs five times as much for a request whose prompt is over 100,000 tokens. The
ruling quotes the pages.

**What the change does to the reads.** Full reads fall to two a round. It adds a batch to each of my turns:
the light read that shows the turn, then the full one, where one full poll did both. In the stand-in fight of
the tests:

| Fight (stand-in) | Full reads a round: base | now | Batches a round: base | now | First action after the turn is seen: base | now |
|---|---|---|---|---|---|---|
| his turn 20 s, the relay 3 s a batch | 3.6 | 2.0 | 4.6 | 6.0 | at once | 3.5 s |
| his turn 40 s, the relay 3 s a batch | 7.0 | 2.0 | 7.0 | 8.0 | at once | 3.5 s |
| his turn 30 s, the relay 10 s a batch | 4.1 | 2.0 | 4.1 | 4.8 | at once | 9.7 s |
| his turn 6 s, the relay 10 s a batch | 2.0 | 2.1 | 2.0 | 3.1 | at once | 10.1 s |

Every turn was played in every row, on both sides. The latest first action was 10.8 s into the turn; the rule
is 20 s.

**What it does to the plan's count.** The clean stretch of the live session is its first relay's 27 batches:
the walk to the fight and rounds 1 to 5. On it, 18 full reads as it ran become 10, with 13 light reads and
five more batches.

| Relay | Born with | As it ran | Built here | | Requests over 100,000: as it ran | built |
|---|---|---|---|---|---|---|
| one for the stretch (what the code does in a fight) | 118,190 (the session's) | 4.84M | 4.54M | -6% | 27 of 27 | 32 of 32 |
| one for the stretch | 5,000 | 2.42M | 1.65M | -32% | 10 of 27 | 9 of 32 |
| replaced past 60,000 | 5,000 | 0.41M | 0.35M | -15% | none | none |
| a fresh one every round | 5,000 | 0.39M | 0.29M | -27% | none | none |

- **The change saves on every relay**: 6% on the one the session had, 15 to 32% on a small one.
- **The relay's size is worth far more than this change.** The session's relay was born with 118,190 tokens,
  so every request it made was over 100,000 and paid five-fold. The same stretch on a relay born with 5,000
  and kept under the line costs about a twelfth: 0.41M against 4.84M, before any light read. The small relay
  (`.claude/agents/tnr-relay.md`) is prepared and has not been tried.
- **In a fight a relay is not replaced** (`player/relay.py`, `should_rotate`). A small relay kept for five
  rounds still crosses 100,000: on 10 of its 27 requests as it ran, on 9 of 32 with this change. The two last
  rows are what replacing it inside a fight would give. That is not built.
- **Each of my turns starts one relay round trip later.** In the live session a round trip was 7 to 13 s.
- **Against an opponent who moves before my first poll it is a small loss**: the same two full reads a round
  as before and one batch more. The last row of the first table.
- **Keeping the state his turn starts on (RUL-2026-11-13-155)** is the difference to the proposal's one full
  read a round, which the script prints as well: 12 points on the session's relay, 29 on a small one kept for
  the stretch, 4 or none where the relay is replaced.

**What I said before, and why it was wrong.** In the live-session handoff I put this change at about half of
a fight's relay tokens. That was in the raw count, every token of every request alike, which is what the
token log keeps; it was for one full read a round; and it was taken over the whole session, most of which
after the first relay is that session's defects. In the raw count this change comes out between 35% less and
18% more on the stretch above, because the batch it adds weighs as much as the reads it saves. The raw count
is not what the plan counts. I no longer have the script behind the old table and cannot make it again.

It is an estimate from 27 batches of one fight against one opponent, with a light read put at 2,000 tokens.
It is a reason to measure, not a result.

**What I recommend.** Review it and take it: by the plan's count it saves on any relay. Try the small relay
first, in whatever session comes next: it is the larger saving by far and costs no code. Then decide about
replacing a relay inside a fight, which needs the director's word and Duet's machine.

`docs/reviews/evidence/ai_player_light_polls/tokens_recomputed.py` makes the second table from the session's
log on `duet/ai-player-ap1-live` @ 112aadbd. Its notes give the model and what is guessed in it. `duel.py`
beside it makes the first table, on this head and on the base.

## What was built

`player/activities/battle.py`; `player/budget.py` `planner_seconds`; `player/config.py` (two constants).

### The reads of a round

A full read is the fighters, the whole live effect list, the ground and the log's last lines. On `661f3f63`
every poll of a fight is one. Now, against a player:

1. **Behind my actions: full**, as it was. It shows the state his turn starts on, which the archive keeps
   (RUL-155). It is still a watching read, which the budget may leave out.
2. **His turn: light**, once that state is on record for this round. A light read is the plain read the fight
   already used for its retries: the version, the round, whose turn it is, and the fighters' eight columns. No
   effect list, no ground, and no log read beside it. It is one call where a poll was two. His kit read still
   rides it. The holds between polls are the same.
3. **Until it is on record, his turn is read in full** (the read behind my actions was left out, was lost, or
   came back without the effect list). So the archive's two states a round do not depend on one read arriving.
4. **My turn: a light read that shows it starts the turn's clock, and the full read is asked for at once**, with
   the log's last 20 lines where a poll reads 8. It is not a watching read: the budget does not leave it out.
   When it comes, the turn is planned on it and the state is archived as my turn's.

### When my turn's full read does not come

Nothing here is new; these are AP1's rules, and the light read is the last good read they fall back on.

- **Refused:** the turn is played at once from the light read: its version, the fighters and where they
  stand. The effect list at this version is not known, so the planner works from the log.
- **No answer:** a plain read and the log are asked for again, and at T+12 s the turn is played from the last
  good read.
- **It comes back without the effect list:** it is planned on as it is. The full read is asked for once a
  version, so where the effect list cannot be had the fight does not go back and forth between the two reads.
- **The version did not move** (he let his turn run out): the state of my last full read is still exact, and
  no read is asked for.

### The planner's time

The planner is cut off at T+15 s. A turn that waited for its full read has lost a round trip of that. So a
turn's first plan gets 3 s whatever is left (`PLAN_AT_LEAST`); a plan that replaces a refused one gets what is
left, as before. On `661f3f63` a first plan was never late outside director mode, which has its own figure:
the turn was planned in the tick that first showed it. So the 3 s touch no turn that does not wait for a
read. With a round trip of 14 s the actions go out by T+17 s; the rule is T+20 s.

### The log

His turn is watched without the log, so all of it is read when my turn starts.

- **20 lines with my turn's read** (`ENTRIES_TURN`), and with the read that follows one that was lost.
- **A read that brings as many lines as it asked for, none of them known, may have left lines out.** The next
  log read asks for the whole log (200 lines), once.
- **Lines are kept in the game's order.** A read is the log's newest lines, so what is kept and is not in it
  is older, and the read follows. On `661f3f63` new lines went to the end, which was the same thing while no
  read could bring a line older than one in hand. The tools replay the log in order.
- **The count of lines that the last HP read already includes** (`n_at_battle`, which the fight's result is
  told from when no read shows its end) is set on a turn played from the last good read too. His turn's lines
  can now come in without the full read asked for beside them; left uncounted, his whole turn would be taken
  off my HP a second time.

### Against an AI, and in the director's window

- **An AI's turn is not watched.** It is over with the nudge, so the read behind the nudge is the one my turn
  starts with. It stays full. Nothing changes against an AI.
- **The director's window** (director mode: 40 s of each of my turns are his) is watched light. The exact read
  at its start now goes through the same code as every full read, so it carries the ground and minds the
  refusals. When he acts, the version moves and the full read is asked for once.

### What did not change

The turn's clock and its deadlines. What a refused, an empty or an unusable read does. The archive: two states
a round, each once. The budget and the lanes. The gates. The run lock and its cutoff. What the relay is given
and hands in.

**The protocol number stays 7.** No record between `brain next` and the brain changes its meaning, and no rule
by which a batch's calls are admitted changes. A batch that `661f3f63` made is one this version could have
made: a full poll of his turn is what this version asks for too, until his state is on record. A fight's
state that `661f3f63` saved is read as it stands. If the reviewer reads the rule in `player/relay.py`
otherwise, the number is one line.

## Found while building

Five things the first cut had wrong. Each has a test and a planted defect now, and each is a place to look.

- **An AI's turn was watched light.** Every round against an AI would have cost a round trip and saved
  nothing.
- **In the director's window, where the effect list could not be had, every light read asked for the full
  read again.** It is asked for once a version.
- **Lines recovered by a read of the whole log were put behind newer ones.**
- **His turn's lines, come in without their read, would have been taken off my HP twice** when the log is
  asked how a fight ended.
- **The planner's 3 s went to every plan of a turn that had waited**, so a refused plan was replaced past the
  fifteen seconds with a planner run where a basic action used to go at once. Only the first plan gets them.

## Readings of mine

The director's to change. None is settled by a ruling.

1. **A light read is the plain read**, not five fields: the fighters' columns come with it. The fight's end is
   seen on it, and a turn played from the last good read knows where the fighters stand. It is a shape the
   fight already used, so no new select meets the game.
2. **No log on a light read**, as proposed. The cost is in "Known limits", 2. The other way is one more call
   a poll (two, as before) and about a thousand tokens.
3. **20 lines, 3 seconds.** `ENTRIES_TURN` and `PLAN_AT_LEAST` are my figures.
4. **The director's window is watched light.**
5. **An AI's turn keeps its full read.**

## Tests

`player/tests/test_light_polls.py` (new, 28 tests): the reads of a round case by case, and whole fights
against a stand-in that answers turn by turn (`Duel`): two full reads a round and every turn played; both
states of every round on record; every log line kept, in order, through a turn of his with more lines than the
read asks for; a relay that takes 10 s a batch; every third full read refused.

On `661f3f63`, in a throwaway worktree with that file copied in: **of 28, 18 fail and 10 pass**. The ones
that pass are controls: they hold on both sides (an AI's turn, the fight's end, a state already in hand, a
refused read, a plan that replaces another, the archive, the log in an ordinary fight). The two constants the
file names were set in the test process only; the base's code reads neither.

Tests of the base that changed, each because the rule did:

- `test_battle.py` `test_his_turn`: the batch is the pilot's with the effect list, the ground and the log
  taken out. `test_an_ai_turn_is_nudged` is unchanged.
- `test_battle.py`, six empty reads in a row: they now answer light reads, which ask for nothing rich, so
  nothing is dropped from the full read; and the budget may leave the log read of a retry for later, as it may
  any watching read.
- `test_live.py`, the log with a short column: the select is checked on my turn's read; his turn has no log
  read.
- `test_review.py`, the ground: the full read that asks for it is my turn's. The stand-in there gave the
  opening log to any log read of more than 8 lines; it now gives it to a read of the whole log.

## Verification on the head's parent (the code commit)

The suite, the walks and the planted defects were run on a local commit with the code commit's `player/`,
`scripts/` and `state/` byte for byte; `git diff --quiet` says so. What differs is the design's sentence and
one of the two evidence scripts, which were finished afterwards. The gates on files were run again on the
code commit.

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 576 tests`, `OK`, three runs in a row, none skipped (`661f3f63`: 548) |
| `test_light_polls.py` on `661f3f63` (a throwaway worktree) | of 28: 18 fail, 10 pass |
| Thirty-five planted defects in the code of this change, in throwaway worktrees | below |
| `python3 -m player.tests.test_walk 200 300` | 200 walks, 5,481 calls, no problem: the figures of the base |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 46 tests`, `OK` |
| `python3 scripts/player_allowlist.py check`, and `report --check` | exit 0, both |
| The four pilot tests (`state/player/dauntless/tools/tests/`) | exit 0 each |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files and commits), `git diff --check` | exit 0 each |
| The two evidence scripts | exit 0; the tables at the top |
| After RUL-156: `rulings_index.py --check` and the other gates on files, on this head | exit 0 each |
| Two fuzz scripts of mine, not in the repository: 1,128 broken battle and log reads, 380 broken profiles and action answers | the results of the base: none bad, and the one case known from AP1 |

## Planted defects

Thirty-five, one at a time, each in a throwaway worktree made from a local commit with the code commit's
`player/`, never in the repository's own tree. The whole player suite was run for each. Every one fails at
least one test. The worktrees were clean after the runs and are removed. The unchanged code passes: the
three runs of the suite above.

A first run, on an earlier cut, let two through. One had no test: a log read that brings as many lines as it
asked for and reaches a known line was not held to be whole; it has one now. The other could not be told
from the code as it was: a flag that a turn had waited for its read changed nothing, because a turn's first
plan is late only when it waited. The flag is gone.

| Planted defect | Tests that fail |
|---|---|
| his turn: every poll is a full read, as it was | 17 fail, 1 error |
| his turn: it is watched light before the state it began on is on record | 3 fail |
| his turn: the record of any round stands for this one | 1 fails |
| his turn: my state of the round stands for his | 4 fail |
| his turn: an AI's turn is watched light too | 2 fail |
| his turn: the read behind my actions is a light one | 27 fail |
| light read: it asks for the log too | 9 fail, 1 error |
| light read: it asks for the effect list | 10 fail |
| light read: it is not a watching read | 1 fails |
| light read: his kit read does not ride it | 2 fail |
| light read: an empty answer to it counts against the full reads | 2 fail |
| light read: nothing says that a read was a light one | 11 fail |
| light read: that it was asked for is forgotten when its answer is empty | 1 fails |
| my turn: a light read is planned on at once | 11 fail |
| my turn: the full read is asked for though the state at this version is in hand | 3 fail |
| my turn: the full read is asked for again at a version it was asked for | 1 fails |
| my turn: its full read is a watching read, which the budget may drop | 1 fails |
| my turn: its full read brings a poll's eight lines of the log | 4 fail |
| my turn: its full read is a plain one | 8 fail |
| my turn: its full read does not say what it asked for | 2 fail |
| my turn: that the full read was asked for at this version is not kept | 1 fails |
| my turn: the clock starts when the full read is in, not on the light read | 6 fail, 1 error |
| planner: the wait for the read is taken out of its time whole | 1 fails |
| planner: a plan that replaces the first is given three seconds too | 4 fail |
| log: a read that is all new is never taken for a gap | 2 fail |
| log: a short read that is all new is taken for a gap | 1 fails |
| log: a read with one known line in it is taken for a gap | 1 fails |
| log: after a gap the next read is no longer than any other | 2 fail |
| log: the read after one that was lost brings a poll's eight lines | 2 fail |
| log: lines that a shorter read left out are put behind the newer ones | 2 fail |
| log: the lines of a read are kept newest first | 5 fail |
| log: a line that came without its texts never gets them | 1 fails |
| result: his turn's lines that came without their read are taken off my HP again | 1 fails |
| director: his window is polled in full | 2 fail |
| director: the one exact read is a plain one | 1 fails |

## Size

Player code 5,727 lines in 30 files (`661f3f63`: 5,666); tests 10,770 lines (10,270). `activities/battle.py`
is 740 lines (685) and `budget.py` 420 (416): both were over the AP6 budget of 400, and are further over.
Seventeen functions branch more than 12 ways: the same seventeen, with the same counts. Config constants 53
(51). Nothing ships switched off.

## Source, generated files, and what else changed

- **No game source was read.** No capture was made. The allowlist is untouched: a light read is
  `combat.getBattle` with fewer fields.
- **`docs/design/AI_PLAYER_OVERHAUL.md`** section 4.7: the sentence on when the effect list is read, and
  what is counted (RUL-156).
- **`docs/rulings/2026-11.md`, `docs/RULINGS.md`**: RUL-2026-11-13-156.
- **`docs/reviews/evidence/ai_player_light_polls/`**: the two scripts named above.
- **The approved brief** (`state/prompt_ai_player_overhaul.md`, AP1 step 1) says to keep "every poll a full
  read" when the pilot is ported. That was done in AP1. RUL-154 is later and governs; the brief is not edited.
- **`docs/reviews/AI_PLAYER_AP1_LIVE_HANDOFF.md`** still carries the table this note corrects. It is that
  handoff's record and is not edited.

## Known limits

1. **None of it has met the game.** What a light read and 20 log lines weigh in a relay's context is not
   measured.
2. **What he does on his turn is first seen when my turn starts.** The fight's base damages are worked out
   again when he shows an action for the first time; that now starts with my turn's read, beside the planner,
   where it often started during his turn. For that one turn the planner may work from the bases as they
   were.
3. **A refused full read costs more than it did.** The turn is then planned without the effect list, and
   without the log of his turn when the log read beside it is refused too. Before, all but the end of his
   turn was in hand.
4. **A state is archived when its read arrives.** My turn's state is missing for a round whose full read was
   lost; his for a round in which no full read came on his turn.
5. **More than 200 new log lines between two reads are not all recovered**, as before.
6. **The count in "The log", last point, is exact for the case named there.** A whole-log read that arrives
   without the fight's read beside it, after a gap, moves lines in front of counted ones, and the count is
   not moved with them. It matters only if the fight then ends unseen. Lines added at the end, as before,
   were no better counted.
7. **One fast opponent on a slow relay is the worst case**, as the first table shows. Nothing here adapts to
   him.
8. The limits of AP1's and AP2's handoffs stand.

## Live-game statement

Zero live requests: no connector call, no game write, no credential or session material. The token log was
read from the repository.

## Open

- For the director: whether this goes on the head a live session runs from (the recommendation above); the
  five readings; whether a relay may be replaced inside a fight.
- From before, unchanged: AP1's live gate and which head it runs on; AP2's three readings; whether the line
  goes to `main`.

## Not begun

AP2's second part; the script that starts short-lived relays; a live run. Also not begun, and not proposed
without the director's word: replacing a relay inside a fight; a token log that keeps cache reads, cache
writes and output apart, so that a session's log gives the plan's count without a model; and anything that
would make the choice between light and full polls depend on the opponent.
