# AI player AP2, first part — independent Lane A review

**Verdict: changes requested.** Two high and two medium findings remain at the frozen target. The existing
480 player tests pass; the independent reproductions below expose gaps between the activities and between
planning and delivery.

- Repository: `perseverance484/tnr-tools`
- Implementation branch: `fable/ai-player-ap2`
- Frozen target: `988c56ccbff9f153a0fa546e9cae3a2d99c696b6`
- Diff base: `ce1be6e98eb39550e79806c5c8f9da87f67fa4eb`
- Superseded handoff: `c720743a005a1fd2c5833b7549f6055d83f34f43`
- Review branch: `chatgpt/review-ai-player-ap2`
- Reviewed: 2026-11-13, Lane A

Read `AI_PLAYER_AP2_HANDOFF.md`, `IMPLEMENTATION_HANDOFF.md`, and the target's
RUL-2026-11-12-153 and -154. Scope is the built upkeep activities, their integration, and the run lock.
**This is not an AP1 acceptance or re-review of the takeover correction at `ce1be6e9`.** In particular, H1
below concerns AP2's new lease requirement on delivery paths that AP2 reuses, not AP1's call-ledger verdict.
Deferred AP2 work and live acceptance remain outside this review.

## H1 — High: the lease is checked before pacing, but not when the calls are delivered

Locations: `player/brain/core.py:278–284`, `player/runlock.py:86–112`; delivery through
`player/brain/client.py:150–168, 225–229, 249–257` and `player/brain/resident.py:50–56`.

`_paced` checks `lock.held()` at the current time, then schedules calls for a later time. Neither the resulting
batch nor the pending client record carries a lease deadline. The client sleeps and prints the calls without
checking the lease again. An answer reused from a receipt also bypasses `hold()` and `held()` entirely.

This contradicts the run-lock workflow's requirement that every call stop a minute before the last confirmed
expiry, and the handoff and OPERATOR page's claim that calls stop there after a failed renewal. It is observable
without a slow game response:

| Offline case | Calls printed | Printing time relative to the original lease expiry |
|---|---:|---:|
| Failed renewal; ordinary hunt hold, no crowded budget | 4 | −56 s (already inside the forbidden final minute) |
| Failed renewal; 20 recent world calls cause pacing | 3 | −4.5 s |
| Same paced batch; interrupt in the wait and retry the pending batch 5 s after its ready time | 3 | +0.5 s |
| Interrupt just before saving the pending batch; retry from the saved receipt after expiry | 3 | +71 s |
| Paced client resumes 150 s late | 3 | +145.5 s |

These use the real `next_batch`, client records, receipt handling, pacing and brain, with a scripted lock tool
and clock. The pending retry is still inside the client's 10-second stale-outbox allowance. The receipt retry
does not run `Brain.handle` twice: it correctly preserves result idempotence, but incorrectly reauthorizes
delivery under an expired lease. No second heartbeat or claim occurs in either retry. At +71 s another runner
can already have claimed after the tool's 65-second quiet period.

Controls: successful renewal permits the same paced batch under a newly extended lease; a fresh decision
started after the cutoff emits no calls when claiming fails. Thus the check works for current decisions and
fails at the later delivery boundary.

**Required correction:** make the confirmed lease govern the scheduled and actual delivery of every batch,
including pending and receipt paths. An expired authorization must not be revived by retrying the batch.
Preserve result idempotence and call-ledger accounting when withholding or replacing that delivery. Include
waits inside batches and the relay's obligation before executing delayed calls in the corrected contract.

## H2 — High: a restock batch can exceed the daily allowance without asking

Locations: `player/activities/restock.py:194–210`, with `player/gates.py:162–178, 290–305`.

The shop planner decrements its local pocket purse after each purchase, but each purchase independently uses
the same `daily - spent_today()` amount. `Gates.screen` also checks every call against the unchanged world;
it does not reserve the preceding calls' costs. The final profile read is after all the purchases.

Reproduction: pocket 200,000; bank 900,000,000; today's recorded spend 49,830,000. With Panacea empty and
Chakra Pills missing, one admitted batch contains:

- 3 Panacea at the catalog price: 165,000 ryo;
- 15 Chakra Pills: 15,000 ryo.

The batch admits **180,000 against 170,000 remaining**, with zero pending decisions. At the prices used by
the planner this takes the day to 50,010,000, contrary to the existing ask-first daily cap retained by RUL-153.
The pocket limit is respected in this example, so that separate restriction does not prevent the defect.
Control: the same batch fits exactly when the day's remaining allowance is 180,000.

This is a new AP2 multi-purchase path exposing a limitation of the pre-existing per-call gate; it is not a
request to reopen unrelated AP1 behavior. The observation establishes admission above the planner's declared
cost limit, not a claim that a live shop purchase was made or its final price measured.

**Required correction:** share the remaining allowance across the whole admitted purchase batch, including
shop and auction combinations, and carry reservations safely across outstanding delivery and restart. Check
the aggregate reserve as well. Unknown training costs also need a defensible shared bound; multiplying a
per-call pocket estimate is not a substitute for accounting for the funds those calls share.

## H3 — Medium: training and session travel can bypass the 200,000 pocket limit

Locations: `player/activities/bank.py:70–71`, `player/activities/training.py:181–188`, and
`player/activities/session.py:23–38, 45–50`.

Banking excess cash is an upkeep activity with value 2. Training has value 4, and session end is in the higher
`deadlines` class. Neither travel path requires the excess to have been banked.

The reproduction performs the normal queue-read → bank withdrawal → queue-fill sequence. After the fill,
the profile reports 9,400,000 remaining in pocket and 2,500 energy outside the village. The next chosen
activity is **training**, which sends `travel.startGlobalMove`, `travel.finishGlobalMove`, and a profile read.
Bank is available at that exact decision, and the training draw wish has already been cleared. With energy
zero, the control chooses `bank.toBank` as intended. Separately, ending a session away from home with the
same pocket balance chooses session travel before the available deposit.

RUL-153 expressly permits a larger withdrawal for training and limits money carried while running around
to 200,000. This is not a disagreement with the documented 100,000 target or 20,000 refill interpretation:
the character leaves with 9.4 million after the training fill is over.

**Required correction:** make an excess pocket balance block voluntary travel until the deposit is confirmed,
including training trips and the trip home at session end. Keep it effective when a deposit is refused or
waiting for retry; merely raising the bank's normal ranking would not cover that case. Preserve urgent battle
and recovery handling.

## H4 — Medium: selecting a loadout leaves the equipment model and planner feed stale

Locations: `player/activities/equipment.py:56–75, 90–91`.

The initial restock pass reads items and writes `equipped.json`. Equipment then selects the PvP 1 loadouts,
but follows the mutations only with `profile.getUser`. Successful selection neither refreshes nor invalidates
the inventory/equipped feed, nor schedules an item read. Restock has just put its next normal read 900 seconds
away. The next chosen activity can already be the hunt.

In the reproduction, selection succeeds and the hunt resumes while `equipped.json` still names the thrown
weapon from the pre-selection read. Supplying an item read reflecting a different selected loadout immediately
updates the feed, which is the passing control. The fixture models two loadouts with different thrown weapons;
it does not claim to know the live account's current PvP 1 contents.

`state/player/dauntless/tools/turn.py:_equipped_thrown` uses that feed to select the actual kunai action ID and
damage assumptions. A successful switch to a different thrown weapon can therefore leave the next fight
using the old weapon ID/model until an unrelated read refreshes it. Inventory-based repair and restock also
continue to see the old slots.

**Required correction:** refresh the equipped items after selecting an item loadout, and make that refresh
part of completing the switch before dependent planning proceeds. Cover a change of weapon and a failed or
unusable refresh; the existing successful backup-equip path already includes an item read.

## Checks that passed and limits of the evidence

- All **480 player tests** passed, none skipped, including 43 upkeep tests and 12 run-lock tests. They cover
  restock sources/currency restrictions, repair ordering and cooldowns, queue filling/refusals, energy and
  experience allocation, backup equipment and partial loadout answers, transfers/reserve, and final upkeep.
- The three `TheRealTool` tests use temporary local bare repositories. Claim/refusal, token ownership,
  heartbeat, release, another instance's quiet period, same-instance reclaim, session release, and an
  unreachable repository passed. No real main-branch lock was claimed or changed.
- Ordinary lock-state restart, rehearsal folder handling, token omission from status, lost-renewal refusal,
  pause/end-session release and relay rotation controls passed. H1 adds the missing delivery-time cases.
- **46 allowlist/catalog tests** passed. Allowlist check and generated report, rulings index, large-file gate,
  and whitespace check passed. The captured endpoint shapes were inspected for the new calls; no game source
  or live response was obtained to validate the handoff's stated experience-assignment assumptions.
- RUL-154's brain ownership and first/second AP2 scope split are represented in the code and handoff. H1
  prevents accepting the claimed lease enforcement. RUL-153's numeric settings are correct; H3 prevents
  accepting their enforcement across activities. OPERATOR's run-lock cutoff claim needs the H1 correction.
- Existing tests and the independent observations exercise temporary worlds and fake game results. Passing
  them is not evidence of live endpoint success or the deferred live-session acceptance.

Commands rerun on the frozen implementation:

```sh
python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .
python3 -W ignore::ResourceWarning -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py
python3 scripts/player_allowlist.py check
python3 scripts/player_allowlist.py report --check
python3 scripts/rulings_index.py --check
python3 scripts/check_large_files.py
git diff --check
PYTHONPATH=. python3 docs/reviews/evidence/ap2_lane_a/reproduce.py
```

The last command is added by this review. [Reproducer](evidence/ap2_lane_a/reproduce.py) and
[captured observations](evidence/ap2_lane_a/observations.json) are published with the report. Its assertions
confirm the observed defects and controls on this frozen target; they are not tests asserting the desired
fixed behavior. All lock-tool responses in that script are scripted, and all state is in temporary folders.

**Live requests: zero. Game writes: zero. Live credentials/session material used: none.** No browser or live
session checks were performed. Only this report and its evidence are added on the review branch; no `fable/*`
branch or implementation file is modified. AP1's separate verdict remains outstanding.
