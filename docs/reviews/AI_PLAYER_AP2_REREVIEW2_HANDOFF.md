# AI player overhaul, phase AP2, first part: correction handoff after the re-review of 87e497a6

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md` section 5. Written 2026-11-13, in answer to the re-review
of `87e497a6` ("changes requested": H1 closed; H2 high and H3, H4 medium still open in the cases it gives).

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-ap2
Reviewed: 87e497a6efa781fb1b43ef809cce3a3bd48b1842
Review: docs/reviews/AI_PLAYER_AP2_REREVIEW1_LANE_A_REVIEW.md, with its scripts and observations, on
        chatgpt/review-ai-player-ap2-rereview1 @ 89a18dc3 (evidence; not merged)
Base of this correction: 87e497a6. Not rebased: this head is two commits on it.
Head: the commit that adds this note (FROZEN; the exact SHA is in the correction message)
Stands on: AP1 at 62e1aab1, which is accepted (chatgpt/review-ai-player-ap1-rereview13-lane-a @ 46b85411)
```

The diff to review is `git diff 87e497a6 HEAD`.

## Disposition

All three findings are **confirmed and corrected**. H1 is closed in the re-review and is not touched.

The re-review's `overlap.py`, unchanged, on the reviewed head and now. It asserts the defects, so now it stops
at its first assertion; the figures are from a wrapper that calls its functions and prints what they return.

| Finding | The re-review's case | On `87e497a6` | Now |
|---|---|---|---|
| H2 high | relay B reads the profile before relay A buys, and hands the read in with the word that A is back | A's reservation is dropped; nothing is measured; 180,000 more are admitted: 360,000 against 180,000 left | A's reservation stays; nothing more is bought; the next batch is the bank's deposit |
| | control: B's read is made after A has bought | 50,000,000 measured; the reservation dropped; no purchase | 50,000,000 measured; no purchase; the reservation stays for one more read |
| H3 medium | the bank activity switched off, 9,400,000 in the pocket: training, a session's end, the hunt | each sets off; the gate allows it | none sets off; the gate refuses it for all three; the session's end waits and says why |
| H4 medium | B reads my items before A selects, while A's selection is loose | the stale mark is gone; the hunt is next; the feed names the old weapon | the mark stays; the hunt waits; the feed names what was equipped at that read |
| | control: A selects and is back before B's read is made | the mark gone; the feed names the new weapon; the hunt next | the feed names the new weapon; one more read is asked for at once, and the hunt follows it |

In both controls the brain is given a read together with the word that the other relay is back. It cannot
tell that read from the one in the case above it: both were asked for before it knew. So in both it waits for
a read that was asked for afterwards. The control costs one read more than it did; the case is closed.

`player/tests/test_ap2_rereview1.py` has the findings as six classes, 16 tests, on the re-review's harness: the
real `brain next` and `brain put`, one relay replacing another, the saved files, a brain made afresh for
every request. On `87e497a6`, in a throwaway worktree with that file copied in: **10 fail, 3 error, 3 pass**.
The three errors are the H4 tests: they look for the stale mark's row, and the old code had taken the mark
away (the finding). The three that pass are a control (at the limit the trips go) and two tests of the new
module by itself. That module does not exist on `87e497a6`; it was loaded in the test process from this tree,
and no file of that checkout was changed.

## What was built

### H2 and H4. What a batch owes is paid off by a read that is known to follow it

`player/owed.py` (new, 54 lines); `player/world.py` `absorb`, `_profile`, `reserved`; `player/gates.py`
`Gates.reserve`; `player/activities/equipment.py`; `player/brain/core.py` `Brain.handle` (one line).

The two findings are one mistake made twice. A batch can leave two things owing: the ryo its calls may cost,
and that it changes what is equipped. I dropped each as soon as the batch was over and a read had come. That
a batch is over, and that a read shows what it did, are two facts.

- **The rows.** Each is kept by the batch that owes it, in the world model: `records.spend.out` and
  `inventory.stale` (which was one flag, and is now a row for each batch). A row gets a mark once the brain
  knew, before the request at hand, that its batch is over.
- **What pays a row off.** A read that is known to have been made after the batch's calls. There are two:
  - the batch's own read, made behind its other calls and handed in with it (the ordinary case);
  - a read of a batch that was made after the brain knew the batch was over: that is, any read once the row
    has its mark.
- **What does not.** A read handed in together with the word that the batch is over. It was asked for before
  the brain knew, and may have been made before the batch's calls. The rows are marked after the request's
  reads have been taken in, never before.
- **Getting the read.** For the ryo, the hunt, the bank, restock, training, equipment and the session's wait
  each read the profile in their batches, so the next batch that is not an idle one measures. For the items,
  the read is asked for at once when the batch is known to be over, and every 30 seconds while the wait lasts.
- **Through a restart and a receipt.** The rows and their marks are in the world model, saved with
  everything else a request changed. A request answered again from its receipt runs nothing and marks
  nothing.
- **While a selection is loose** the items are still read every 30 seconds. No such read ends the wait. Each
  brings the feed up to what is equipped at that moment, which is what a fight that comes unasked is planned
  on.

### H3. The pocket's limit does not hang on the bank's switch

`player/world.py` `World.overfull`; `player/activities/session.py`.

- `overfull` is the pocket over 200,000, and nothing else. The exception for a bank that is switched off was
  mine, I named it as a reading, and nobody had ruled it. It is gone.
- With the pocket over the limit and no deposit to be had (the bank switched off, or its deposit refused and
  waiting), a session's end no longer goes quiet. It waits where it is, reads the profile every 30 seconds,
  and its note says how much is in the pocket, what the limit is, and which of the two it is waiting on. When
  the pocket is down, by whatever hand, it goes home.
- The hunt already said why it stays. Training has no trip to offer and nothing to say; its other work goes
  on.
- `player/OPERATOR.md` has a section for it: "The pocket".

### The number is 7

`player/relay.py`. All three change which batches are made: a second batch of purchases, a hunt's attack, a
trip. By the rule the number changes. One test holds `87e497a6` to that with its own package.

## Found while correcting

- **The test character carried 2,000,000 ryo**, ten times what the pocket may hold, in every test that did not
  say otherwise (`player/tests/support.py`). With the limit minded whatever the bank's switch, three of AP1's
  tests and one of AP2's had it set off on a trip it may not make. It carries 150,000 now. No test asserted
  the sum. What changed is that one line of the fixture, and the pocket in one training test.
- **Three of the last handoff's tests changed with the rules**: the bank-off line of the gate's test now
  expects the refusal; the loose batch's reservation goes with the read after the word, not with the word;
  and a selection whose read did not come is asked for again at once, not after 30 seconds. One older test
  (a session's end) answers the selection's item read, which it had left unanswered.
- **The re-review's script reads the reservation's rows by position.** I had made them records with names.
  They are lists again, with the mark as a third place, so the script runs unchanged and a world model that
  `87e497a6` saved is read as it stands.

## Did a wider assumption change?

Yes: **"when a batch is over, the next read shows what it did."** It holds when there is one relay. With a
relay that was replaced there are two orders in play: the order in which batches were made, and the order in
which their calls ran. The brain knows the first. Of the second it knows only what is handed in.

The same question, put to everything else the brain concludes from a read:

- **The call ledger** does not conclude from reads: a loose batch is counted until it comes back or is
  confirmed stopped. That is AP1's, accepted, and not touched.
- **The spend that is measured** is the fall of pocket and bank between two reads. A read that is older than
  the one before it shows a rise, and a rise is not counted: it cannot make spending disappear. The read
  after it would then count the same fall a second time, which errs on the side of spending less. It takes
  a read handed in after a newer one, which one relay replacing another does not produce.
- **What is equipped, my position, my pools** are taken from the newest read handed in. After a replaced relay
  comes back late they can be older than the brain thinks, until the next read. For the feed that is what
  the stale mark is for. For position and pools nothing is kept; the hunt reads the profile in every batch.
- **The fight** is one relay's by construction: a replaced relay's fight batch is loose and the turn's clock
  decides.

I recommend this scope: the three corrections; `player/owed.py` as the one place the rule lives; the order of
marking and reading inside one request; the two controls, which now cost a read; and the session's wait.

## Readings of mine

The last handoff listed four. The re-review took the first as H3; it is withdrawn. The other three stand as
they were, and are the director's to change: the hunt stays too; a batch is cut at the cutoff, not dropped;
the item read is asked for again every 30 seconds.

## Verification on the head's parent (the code commit)

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 548 tests`, `OK`, three runs in a row, none skipped |
| The re-review's `overlap.py`, unchanged | stops at its first assertion; its observations are the table above |
| The re-review's `prior.py` (the first review's script) and `delivery_controls.py`, unchanged | `prior.py`: what the re-review recorded, but for one line: after a selection whose item read did not come the next activity is `equipment` (the read, asked for again at once) where it was `watch` (the 30 seconds' wait). `delivery_controls.py`: 3 tests, `OK` |
| `test_ap2_rereview1.py` on `87e497a6` (a throwaway worktree) | of 16: 10 fail, 3 error, 3 pass |
| One hundred and twenty-seven planted defects in the AP2 code, in throwaway worktrees | below |
| Eight of AP1's planted defects (its last correction's seven, and the number), on this code | every one fails at least one test |
| `python3 -m player.tests.test_walk 200 300` | 200 walks, 5,481 calls, no problem: the figures of the base |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 46 tests`, `OK` |
| `python3 scripts/player_allowlist.py check`, and `report --check` | exit 0, both |
| The four pilot tests | exit 0 each |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files and commits), `git diff --check` | exit 0 each |

The planted defects: the last handoff's 111, brought up to the code as it is now, and 16 for this correction
(seven under "owed", two under "spend", three under "equipment", one under "brain", three under "session").
One of the 111 changed sides: "the limit is minded with the bank
switched off" was a defect then and is the rule now, so its opposite is planted. All were planted in throwaway
worktrees made from a local commit with the tree of the code commit, never in the repository's own tree. The
worktrees were clean after the runs and are removed. The unchanged code passes.

| Planted defect | Tests that fail |
|---|---|
| restock: a purchase is not held to what the pocket can pay | 7 fail |
| restock: the reserve is not held against pocket and bank | 3 fail |
| restock: the day's cap does not bound a purchase | 12 fail |
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
| training: energy is trained wherever the character stands | 4 fail |
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
| equipment: a refused selection is tried again at once | 4 fail |
| equipment: one loadout answered counts as both selected | 1 fails |
| equipment: what is equipped is not written for the planners | 8 fail, 5 errors |
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
| run lock: a brain on any folder claims | 73 fail, 33 errors |
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
| lease: the hunt's own batches carry a cutoff in a rehearsal | 50 fail, 39 errors |
| spend: the gate holds each call against the allowance alone (H2) | 3 fail |
| spend: what is still out is not counted by the gate | 1 fails |
| spend: calls with no price each take the whole pocket | 10 fail, 1 error |
| spend: a call the spend gate is not on counts too | 11 fail |
| spend: nothing is reserved for a batch that is made | 8 fail |
| spend: a reservation is dropped by a profile read from before the purchases | 1 fails |
| spend: a loose batch's reservation is dropped | 6 fail, 3 errors |
| spend: a reservation is never dropped | 8 fail |
| spend: a screen's tally is left standing for the next check | 1 fails |
| spend: a step added to a batch is not held against what is in it | 1 fails |
| restock: two purchases of one pass are each sized by the whole allowance (H2) | 1 fails |
| restock: what is still out does not count against the pass | 5 fail |
| gates: two level transfers go in one batch | 1 fails |
| pocket: training sets off for the village with a full pocket (H3) | 3 fail |
| pocket: a session sets off for home with a full pocket (H3) | 3 fail |
| pocket: the hunt goes on to the next sector with a full pocket | 2 fail |
| pocket: the gate lets a trip by choice go | 2 fail |
| pocket: the gate stops a fight's and recovery's trips too | 2 fail |
| pocket: the limit is not minded with the bank switched off (re-review, H3) | 5 fail |
| pocket: the limit itself counts as over it | 2 fail |
| session: at home the character sleeps on a full pocket | 1 fails |
| equipment: a selection is followed by a profile read only (H4) | 8 fail |
| equipment: a selection does not mark the items stale | 3 fail, 3 errors |
| equipment: the hunt goes on before the items are read | 3 fail |
| equipment: restock goes on before the items are read | 2 fail |
| equipment: repair goes on before the items are read | 1 fails |
| equipment: a read that did not come is not asked for again | 5 fail |
| equipment: the read is asked for again at every tick | 8 fail, 1 error |
| equipment: a read that cannot be used ends the wait | 1 error |
| equipment: the read ends nothing | 9 fail |
| equipment: a backup that goes in does not mark the items stale | 1 error |
| owed: a batch that is over is paid off by a read that comes with the word (re-review, H2 and H4) | 8 fail, 1 error |
| owed: a read from before the batch's other calls pays it off | 2 fail |
| owed: the batch's own read pays off a batch that is still loose | 2 fail |
| owed: a row is never marked, so only a batch's own read pays it off | 11 fail |
| owed: a row is marked while its batch can still run | 6 fail, 3 errors |
| owed: the batch that is out counts as over | 2 fail |
| owed: what the version before kept for the items is read as nothing owed | 1 fails |
| spend: the rows are not marked when a request has been taken in | 7 fail |
| spend: the rows are marked before the request's reads, not after | 6 fail |
| equipment: the rows are marked before the request's reads, not after | 2 fail, 1 error |
| equipment: the read is not asked for at once when the batch is over | 3 fail |
| equipment: the stale row names no batch | 3 errors |
| brain: the activities are not told which batch is being made | 3 errors |
| session: it waits for a bank that is switched off, and says nothing | 3 fail |
| session: the wait for the pocket is no wait | 1 fails |
| session: the note does not say that the bank is switched off | 1 fails |

## Size

Player code 5,666 lines in 30 files (`87e497a6`: 5,578 in 29); tests 10,270 lines (9,900). The new file,
`owed.py`, is 54 lines. `world.py` is 392 lines (397), `brain/core.py` 396 (396), `brain/client.py` 400
(400). Over the AP6 budget of 400, as before: `activities/battle.py` 685 and `budget.py` 416. Seventeen
functions branch more than 12 ways, the same seventeen. Config constants 51. Nothing ships switched off.

## Source, generated files, and what else changed

- **No game source was read.** No capture was made. The allowlist is untouched, and its review page is
  current.
- **`player/OPERATOR.md`**: what a held batch holds besides its calls (what it may have cost, what it may have
  equipped), and "The pocket".

## Known limits

1. **None of it has met the game**, as before.
2. **With relays overlapping, the player buys less and hunts later than it could.** A reservation and a stale
   mark each wait for one read more than a brain that could see the order of the calls would need. Near the
   day's allowance a call that carries no price can be put to the director that a read later would have gone
   by itself.
3. **A relay that was replaced and is never ended** keeps its batch loose. Its purchases stay reserved and,
   if it selected a loadout, the hunt, restock and repair wait, until the operator says it is stopped. The
   operator's page says so. The call ledger already held that relay's calls for as long.
4. **A fight that starts while my items are stale** is planned on the feed as the last read left it. The
   fight is not made to wait.
5. **A read is known to be new by the time it was taken in.** Two usable item reads in one second are one to
   the equipment activity. No relay is that fast.
6. **With the bank switched off and the pocket over its limit the player stays where it is**, by the rule.
   Training's energy is not spent and the hunt does not move on until someone banks.
7. The limits of the two handoffs before stand: a batch can be printed long after it was planned and only the
   run lock's cutoff stops it; code cannot stop a batch that is printed; the reservation is the plan's
   price, not the game's.

## Live-game statement

Zero live requests: no connector call, no game write, no credential or session material. The run lock tool was
run only by the existing tests, against a repository made in a temporary folder.

## Open

- For the director: AP1 is accepted in review at `62e1aab1`. What is left of AP1's gate is his: a live session
  on a Haiku relay. Which head it runs on is his to say; this one carries AP2's upkeep as well.
- The three readings above.

## Not begun

As before: AP2's second part; light polls on his turn; the script that starts short-lived relays; a live run.
