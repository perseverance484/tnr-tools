# AI player overhaul, phase AP2, first part: correction handoff after the review of 988c56cc

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md` section 5. Written 2026-11-13, in answer to the review of
`988c56cc` ("changes requested": two high findings, two medium).

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-ap2
Reviewed: 988c56ccbff9f153a0fa546e9cae3a2d99c696b6
Review: docs/reviews/AI_PLAYER_AP2_LANE_A_REVIEW.md, with its script and observations, on
        chatgpt/review-ai-player-ap2 @ 12bf61d3 (evidence; not merged)
Base of this correction: 988c56cc. Not rebased. On it, in order:
        241a0f1f  RUL-2026-11-13-155 (three documents; no code)
        025c89f1  a merge of fable/ai-player-ap1 at 62e1aab1, AP1's correction after its own review
        the code commit of this correction
        the commit that adds this note
Head: the commit that adds this note (FROZEN; the exact SHA is in the correction message)
```

## What to review

- **AP2's correction is `git diff 025c89f1 HEAD`**: the four findings, their tests, and this note.
- `git diff 988c56cc 025c89f1` is not AP2's: it is a ruling's three documents and AP1's correction, which has a
  review of its own (`docs/reviews/AI_PLAYER_AP1_REREVIEW13_HANDOFF.md`). The merge had one conflict, in
  `Brain.__init__`: AP2's run lock argument and AP1's count of a left save are both kept.

## Disposition

All four findings are **confirmed and corrected**. The review's script, on the reviewed head and now. It
asserts the defects, so now it stops at its first assertion; the figures below are from a wrapper of ten lines
that calls the script's own functions and prints what they return.

| Finding | The review's case | On `988c56cc` | Now |
|---|---|---|---|
| H1 high | a hunt batch planned 65 s before the lease's end, the renewal failing | 4 calls printed 56 s before the end | no call |
| | the same, paced behind twenty world calls | 3 calls, 4.5 s before the end | no call |
| | its `brain next` resumes 150 s late | 3 calls, 145.5 s after the end | no call |
| | a crash in the wait, the batch printed 5 s after it was ready | 3 calls, 0.5 s after the end | no call |
| | a crash before the batch is written down, given again from the receipt | 3 calls, 71 s after the end; one decision | no call; one decision |
| | control: the renewal succeeds | 3 calls, inside the new lease | the same |
| | control: asked after the cutoff, the claim failing | no call | no call |
| H2 high | Panacea empty and Chakra Pills missing, 170,000 ryo of the day's allowance left | 180,000 admitted (3 and 15), nobody asked | 170,000 (3 and 5), nobody asked |
| | control: 180,000 left | 180,000 (3 and 15) | the same |
| H3 medium | a training fill leaves 9,400,000 in the pocket, the energy is worth the trip | training sets off for the village | the bank's deposit; the trip after it |
| | a session ends away from home with 9,400,000 | the session sets off for home | no trip; the deposit, then home |
| | control: no energy | the bank's deposit | the same |
| H4 medium | the PvP 1 loadouts are selected; they equip another thrown weapon | the batch has no item read; the hunt is next; the feed names the old weapon | the batch reads my items; the hunt waits for that read |

`player/tests/test_ap2_review.py` has the findings as five classes, 38 tests. On `988c56cc`, in a throwaway
worktree with that file copied in: **28 fail, 4 error, 6 pass**. The four errors are tests that ask for
something the old code does not have at all (a cutoff on a batch, the stale mark). The six that pass are
controls that held before and must still hold: a call due before the cutoff goes though the renewal failed, a
renewed lease carries the paced batch, a crash inside the lease prints the batch, a pass buys everything when
it fits, a profile read behind the purchases counts what was spent, and what AP1's head made is another
version's (there by its number, 5 against that head's 4). To load on `988c56cc` the tests need six names of
the new code; they were set in the test process to what the old code did, and no file of that checkout was
changed.

## What was built

### H1. The lease holds for when a call is made

`player/runlock.py` `RunLock.until`, `within`, `lapsed`, `given_up`, `too_short`; `player/brain/core.py`
`Brain._paced`, `_record`, `_wire`; `player/brain/client.py` `next_batch`, `_owed`, `_exchange`,
`_a_waiting_batch`; `player/budget.py` `Budget.unsend`.

- **The cutoff.** `RunLock.until()` is a minute before the last expiry the tool confirmed: the moment from
  which no call is made. A rehearsal has none. With no claim it is 0.
- **The brain puts no call in a batch that is due at or after it.** `_paced` paces as before and then cuts
  the batch at the first call that would be made at or after the cutoff, with everything behind it
  (`within`). What is cut is taken out of the ledger again (`unsend`): it was never sent. The brain says so
  once for each lease. This one rule replaces the check that was there (is the lock held now): with no claim
  the cutoff is 0 and nothing goes.
- **Every answer carries the cutoff it was made under**, and so does the receipt, which is the answer.
- **`brain next` prints nothing of a batch whose last call would be made at or after its cutoff** (`lapsed`):
  after its own wait, and for a batch that is waiting in its file when it starts. Such a batch is given up
  (`given_up`): the relay is sent straight back, the next request tells the brain the batch was not printed,
  and the brain counts its calls from then and decides afresh. That is the path a batch that grew too old
  already took, so the ledger's accounting and the answer's idempotence are what they were: a request made
  again is still answered from its receipt and nothing is run twice; the receipt's batch is then not printed.
- **The waits inside a batch count.** A batch's calls are timed with the waits in front of them, at the brain
  and at `brain next`. The relay spends those waits.
- **The relay's part.** The relay decides nothing and is told nothing new. It makes a batch's calls at once
  and in order. The minute between the cutoff and the lease's end is its time to finish a batch that was
  printed just before the cutoff. `player/OPERATOR.md` ("The run lock") says this, and what to do with a
  relay that sits on a printed batch.
- **The number is 6** (`player/relay.py`): a batch with no cutoff on record is another version's. Two tests
  hold it to that with the packages out of the repository's history: `988c56cc`, and AP1's head `62e1aab1`,
  whose number is the one before this. The second is there because a planted defect showed that nothing else
  was: with AP2's number put back to AP1's, every other test passed, and a batch out of a receipt of AP1's,
  which has no cutoff, would have been given again as one that needs none.

### H2. One allowance for a batch, and for the batches that are out

`player/gates.py` `g_spend_cap`, `Gates.price`, `Gates.reserve`, `Gates.screen`; `player/world.py`
`World.reserved`, `_paid`, `absorb`; `player/activities/restock.py` `_short`, `_shop`, `_auction`, `_best`;
`player/brain/core.py` `Brain._compose`.

- **The gate.** A call is held against the day's allowance and the reserve together with what is admitted
  and not yet paid: the calls before it in its batch, and the batches that are still out.
- **The reservation.** When a batch is made, what its calls may cost is written into the world model under
  the batch's id (`records.spend.out`), in the same save as the batch. It is dropped when a profile read has
  shown what was spent and the batch is over: none of its calls out or loose in the ledger, and, for the
  batch the read came with, the read made after every other call of it. So it outlives a restart, and a batch
  that went with a replaced relay keeps it until that batch comes back or is confirmed stopped.
- **The planner.** A restock pass spends out of what the pass has left, in three purses: the pocket, the
  day's allowance, and what is above the reserve. Shop and auction purchases draw on the same three.
- **Calls with no price** (a place in the training queue) were each taken to cost the whole pocket. They are
  all paid from the pocket, so together they are taken to cost it once.
- **A step the brain adds to a batch** (recovery's, in front of a fight's closing batch; a rider's) is held
  against what is already in the batch.

### H3. No trip by choice with more than the pocket may hold

`player/world.py` `World.overfull`; `player/gates.py` `Gates._road`; `player/activities/training.py`,
`session.py`, `pvp_hunt.py`.

- **The rule.** While the pocket holds more than 200,000 ryo no trip is started by choice: not training's to
  the village, not a session's home, not the hunt's to the next sector. It holds whether the deposit is still
  to come, was refused, or waits to be tried again.
- **Where it is kept.** The three activities do not plan such a trip: training has no trip to offer, the
  session waits, the hunt stays where it is, fights who is there and scans. Behind them the gates refuse
  `travel.startGlobalMove` for every activity but the fight and recovery (rule `pocket_limit`), so an
  activity that is written later is held too.
- **At home**, a session's end lets the bank have its turn before the character sleeps.

### H4. A selection is finished by a read of my items

`player/activities/equipment.py`; `pvp_hunt.py`, `restock.py`, `repair.py` (`available`).

- The selection's batch reads my items behind the two selections.
- From the moment a selection is planned the items are `stale` (`world["inventory"]`). While they are, the
  hunt, restock and repair do not act. A read of my items that the world model could use ends it.
- A read that did not come back, failed, or could not be used is asked for again every 30 seconds, by
  itself: the loadouts are not selected again.
- The backup thrown weapon's swap is read back the same way.

## Found while correcting

- **The same question, put to the other gate that counts.** One level transfer in 24 hours
  (`g_one_transfer_a_day`) is written down when a batch is made, so two transfers in one plan were each held
  against a day with none in it. Nothing plans a transfer yet. The gate now refuses the second.
- **One planted defect of the first handoff is no longer one.** "The place where every batch is paced does
  not ask" removed a check that the cutoff has made redundant. The check is gone, and the defect is planted in
  the cut itself.
- **The first run of the planted defects left two standing.** That one, and "repair goes on before the items
  are read": the test had no worn item, so repair had nothing to do either way. It has one now.
- **Three tests of the first handoff changed** (`test_upkeep.py`, equipment): they answered a selection
  without an item read. They answer with one now; what they assert is unchanged, and one asserts the read.
- **`Budget.pace` is as AP1 has it.** My first cut was inside its loop. It is beside it now, so the pacing
  that AP1's reviews went through is untouched.

## Did a wider assumption change?

Yes, two.

1. **"What is checked when a batch is planned holds when its calls are made."** Between the two lie the
   brain's hold, the pacing, the wait in `brain next`, a crash, and a receipt. The lock is now checked at
   both ends. The other things checked at planning are the gates on a target (a fair target, the
   do-not-attack list) and the pacing. A batch that waits for a relay is given up when a later `brain next`
   finds it more than ten seconds old, and that was so before. Two paths have no such bound: a `brain next`
   that wakes late from its own wait, and a batch given again from a receipt. With a lease both are now
   stopped at the cutoff. For the gates and the pacing they are not, and I name it under the limits.
2. **"A call can be judged by itself."** Spending shares an allowance, and the gate judged each call against
   a world that the calls before it had not changed. I went through the gates for others of the kind: the
   transfer gate was one (above). The rest judge a call by its own input or its own target.

I recommend this scope: the four corrections; the lock at delivery on every path a batch can take to a relay
(the wait, the waiting batch, the receipt, a replaced relay, a restart); the reservation's life (made, kept
through a restart, kept for a loose batch, dropped); and the three places a trip is planned.

## Readings of mine, for the director

Each is the least I needed to settle to build the correction. Each is his to change.

1. **With the bank activity switched off, the pocket's limit is not minded.** Then nothing the player does
   can bring the pocket down, and a rule that stopped every trip would stop the player. It would be a
   one-line change to mind it all the same.
2. **The hunt stays too.** The review names training's trip and the session's. "Running around" is the
   hunt's circuit before anything else, so it is held as well.
3. **A batch is cut at the cutoff, not dropped whole.** The calls due before the cutoff go; the rest do not.
4. **The hunt, restock and repair wait for the read**, and the read is asked for again every 30 seconds.

## Verification on the head's parent (the code commit)

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 532 tests`, `OK`, three runs in a row, none skipped |
| The review's `reproduce.py` | stops at its first assertion; its observations are the table above |
| `test_ap2_review.py` on `988c56cc` (a throwaway worktree) | of 38: 28 fail, 4 error, 6 pass |
| The suite on the merge alone (`025c89f1`) | `Ran 494 tests`, `OK` |
| One hundred and eleven planted defects in the AP2 code, in throwaway worktrees | below |
| Eight of AP1's planted defects (its correction's seven, and the number), on this code | every one fails at least one test (the number: one, the test named above) |
| AP1's reviewer's reproducer (`world_reader.py`, four modes), on this code | as on AP1's head |
| `python3 -m player.tests.test_walk 200 300` | 200 walks, 5,481 calls, no problem: the figures of the base |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 46 tests`, `OK` |
| `python3 scripts/player_allowlist.py check`, and `report --check` | exit 0, both |
| The four pilot tests | exit 0 each |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files and commits), `git diff --check` | exit 0 each |

The planted defects: the first handoff's, brought up to the code as it is now, and 46 for this correction. All
were planted in throwaway worktrees made from a local commit with the tree of the code commit, never in the
repository's own tree. The worktrees were clean after the runs and are removed. The unchanged code passes.

| Planted defect | Tests that fail |
|---|---|
| restock: a purchase is not held to what the pocket can pay | 7 fail |
| restock: the reserve is not held against pocket and bank | 3 fail |
| restock: the day's cap does not bound a purchase | 8 fail |
| restock: what costs reputation counts as sold for ryo | 1 fails |
| restock: an auction listing over the item's cap is bought | 1 fails |
| restock: an auction listing in another currency is bought | 1 fails |
| restock: what is stored at home is not taken out first | 1 fails |
| restock: a carried stack is not put back in its slot | 1 fails |
| restock: a pass never ends while the shop says no | 1 fails |
| restock: a read that keeps failing is asked for without end | 1 fails |
| restock: the bank is not asked when the pocket cannot pay for one | 1 error |
| restock: the pocket is asked to hold more than its limit | 2 fail |
| restock: two purchases of one pass are each sized by the whole pocket | 1 fails |
| repair: an item at half its durability is repaired | 1 fails |
| repair: a refused repair is tried again at once | 1 fails |
| repair: ryo is tried before the kits | 10 fail |
| repair: what is carried but not equipped is repaired too | 1 fails |
| training: the highest next level is queued first | 2 fail |
| training: a target at the cap is queued | 2 fail |
| training: a refused target is asked for again at the next look | 1 fails |
| training: a refusal for want of money costs the target a day | 1 fails |
| training: energy is trained wherever the character stands | 3 fail |
| training: energy always goes to willpower | 1 fails |
| training: a fill does not wait for the bank | 3 fail |
| training: the bank is not asked before a fill | 3 fail |
| training: the wish for ten million outlives the fill | 2 fail |
| training: unspent experience all goes to intelligence | 2 fail |
| training: any crumb of experience is worth a call | 1 fails |
| training: refused experience is tried again every ten minutes | 1 fails |
| training: experience is assigned again at once while the profile still shows it | 1 fails |
| calls: a stat is left out of the experience call | 1 fails |
| calls: the profile read does not ask for unspent experience | 1 fails |
| equipment: PvP 1 is selected on guard too | 1 fails |
| equipment: an empty thrown slot does not take the backup | 2 fail |
| equipment: a refused selection is tried again at once | 2 fail |
| equipment: one loadout answered counts as both selected | 1 fails |
| equipment: what is equipped is not written for the planners | 8 fail, 3 errors |
| bank: the pocket is never brought down to its limit | 9 fail |
| bank: the surplus is banked while training still wants it | 1 fails |
| bank: the bank is taken under the reserve | 2 fail |
| bank: twenty million is drawn for training | 2 fail |
| bank: a wish is honoured after it has run out | 2 fail |
| bank: a refused transfer is tried again at once | 2 fail |
| bank: restock is not told that the pocket can pay | 1 fails, 1 error |
| bank: an empty pocket is not filled | 1 fails |
| session: the character sleeps without the last upkeep | 4 fail |
| run lock: calls are planned whether or not the lock is held | 13 fail, 3 errors |
| run lock: the claim is never renewed | 4 fail |
| run lock: a fight does not put a renewal off | 1 fails |
| run lock: a short lease is not renewed in a fight | 1 fails |
| run lock: a lock that was taken is played on | 1 fails |
| run lock: calls go right up to the lease's end | 6 fail |
| run lock: a failed renewal ends the claim | 8 fail |
| run lock: a failed renewal is tried again at every tick | 1 fails |
| run lock: the lock is kept when the session is over | 1 fails, 1 error |
| run lock: the lock is given back for a fresh relay | 1 fails |
| run lock: the lock is kept while the director has the player paused | 1 fails |
| run lock: a brain on any folder claims | 63 fail, 31 errors |
| run lock: the account's own folder is a rehearsal too | 1 fails |
| run lock: the token is written to the status file | 1 fails |
| run lock: the tool is asked at every tick while another has the lock | 1 fails |
| run lock: the wait is said again at every ask | 1 fails |
| run lock: the claim is made under another label | 3 fail |
| run lock: the claim does not name this brain's own instance | 2 fail |
| run lock: the claim is kept in memory only, and lost at a restart | 7 fail, 6 errors |
| lease: the place where every batch is paced does not ask, for now or for when its calls are due (H1) | 5 fail |
| lease: a call due exactly at the cutoff goes | 2 fail |
| lease: a call that was cut is left in the ledger as out | 4 fail |
| lease: a wait is left at the end of a batch that was cut | 3 fail |
| lease: the batch does not carry the cutoff it was made under | 3 fail |
| lease: `brain next` prints a batch that lapsed while it slept (H1) | 2 fail |
| lease: a waiting batch that lapsed is printed by the next `brain next` (H1) | 1 fails |
| lease: the waits inside a batch do not count for its cutoff | 4 fail |
| lease: a batch whose cutoff cannot be read is printed | 1 fails |
| lease: a lapsed batch is dropped and the brain is not told | 3 fail |
| lease: a short lease is said at every ask | 1 fails |
| lease: a waiting batch with no cutoff on record is taken | 1 fails |
| lease: a rehearsal's answer is written down as having a claim | 2 fail |
| lease: the brain cuts nothing that was written down, and the ledger loses the calls that go | 1 fails |
| lease: the hunt's own batches carry a cutoff in a rehearsal | 40 fail, 38 errors |
| spend: the gate holds each call against the allowance alone (H2) | 3 fail |
| spend: what is still out is not counted by the gate | 1 fails |
| spend: calls with no price each take the whole pocket | 10 fail, 1 error |
| spend: a call the spend gate is not on counts too | 6 fail |
| spend: nothing is reserved for a batch that is made | 4 fail |
| spend: a reservation is dropped by a profile read from before the purchases | 1 fails |
| spend: a loose batch's reservation is dropped | 2 fail |
| spend: a reservation is never dropped | 3 fail |
| spend: a screen's tally is left standing for the next check | 1 fails |
| spend: a step added to a batch is not held against what is in it | 1 fails |
| restock: two purchases of one pass are each sized by the whole allowance (H2) | 1 fails |
| restock: what is still out does not count against the pass | 2 fail |
| gates: two level transfers go in one batch | 1 fails |
| pocket: training sets off for the village with a full pocket (H3) | 2 fail |
| pocket: a session sets off for home with a full pocket (H3) | 2 fail |
| pocket: the hunt goes on to the next sector with a full pocket | 1 fails |
| pocket: the gate lets a trip by choice go | 1 fails |
| pocket: the gate stops a fight's and recovery's trips too | 1 fails |
| pocket: the limit is minded with the bank switched off | 4 fail |
| pocket: the limit itself counts as over it | 1 fails |
| session: at home the character sleeps on a full pocket | 1 fails |
| equipment: a selection is followed by a profile read only (H4) | 4 fail |
| equipment: a selection does not mark the items stale | 3 errors |
| equipment: the hunt goes on before the items are read | 3 fail |
| equipment: restock goes on before the items are read | 1 fails |
| equipment: repair goes on before the items are read | 1 fails |
| equipment: a read that did not come is not asked for again | 1 fails |
| equipment: the read is asked for again at every tick | 9 fail, 1 error |
| equipment: a read that cannot be used ends the wait | 1 error |
| equipment: the read ends nothing | 4 fail |
| equipment: a backup that goes in does not mark the items stale | 1 error |

## Size

Player code 5,578 lines in 29 files (`988c56cc`: 5,351); tests 9,900 lines (9,111). `brain/client.py` is
400 lines, `brain/core.py` 396, `world.py` 397, `gates.py` 348, `runlock.py` 216. Over the
AP6 budget of 400: `activities/battle.py` 685 and `budget.py` 416 (408 before: `unsend`). Seventeen
functions branch more than 12 ways: the sixteen of the base, and `next_batch`, at 13 where it was 12. Config
constants 51. Nothing ships switched off.

## Source, generated files, and what else changed

- **No game source was read.** No capture was made.
- **The allowlist's wording** changed in three places: the prerequisites of `travel.startGlobalMove` (the
  pocket rule), the rule text of `spend_cap` (counted by the batch), and the cooldown of the two loadout
  selections (the item read). Its review page (`docs/design/AI_PLAYER_ALLOWLIST_REVIEW.md`) is rendered
  again and current. No gate was added to or taken off an endpoint.
- **`player/OPERATOR.md`**, "The run lock": the last minute, and the relay's part.

## Known limits

1. **None of it has met the game**, as before.
2. **A batch can be printed long after it was planned**, by a `brain next` that wakes late from its own wait
   or from a receipt. The run lock's cutoff now stops it when the lease is over. In a rehearsal, and for
   everything else a batch was checked for when it was planned (the gates on a target, the minute it was
   paced into), nothing does. AP1's reviews went through those paths for what is counted and what is run
   twice, not for how old the batch is.
3. **A relay that is slow with a printed batch** can make calls in the lease's last minute, and after it if
   it is slower than that. Code cannot stop a batch that is printed. The watchdog writes a stall, and the
   operator's page says to end such a relay.
4. **The reservation is the plan's price, not the game's.** What a purchase costs is taken from the catalog,
   and for a call with no price it is the pocket. The measure of what was spent is the profile read, as
   before.
5. **A reservation outlives its batch until the next profile read.** A batch that was never printed is
   reserved for until then; the player may buy less in that time, never more.
6. **A fight that starts while my items are stale** is planned on the feed as it stands. The fight is not
   made to wait.
7. **A selection batch that went with a replaced relay** leaves the items stale; the next relay reads them
   again. If the old relay makes the selection after that read, the feed is behind until the next item read.
8. The limits of the first handoff stand.

## Live-game statement

Zero live requests: no connector call, no game write, no credential or session material. The run lock tool was
run only by the existing tests, against a repository made in a temporary folder.

## Open

- For the director: the four readings above.
- AP1's verdict at `62e1aab1` is separate, and this head stands on it.

## Not begun

As in the first handoff: AP2's second part; light polls on his turn; the script that starts short-lived
relays; a live run.
