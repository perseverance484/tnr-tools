# AP2 second correction — independent Lane A re-review

**Verdict: approved for the requested correction scope. H2, H3 and H4 are closed.** No new blocking finding
was reproduced. H1 remains closed; AP1 remains accepted at `62e1aab1`, as specified in the handoff request.
This is an offline implementation verdict, not live-session acceptance or approval of deferred AP2 work.

- Repository: `perseverance484/tnr-tools`
- Implementation branch: `fable/ai-player-ap2`
- Frozen target: `661f3f63f9bd51887c402ce00f76e8e9735cb2ea`
- Reviewed diff: `87e497a6..661f3f63`
- Previous review: `chatgpt/review-ai-player-ap2-rereview1` at `89a18dc3104c4a4b93989efdb2f2891aba1af5ce`
- Publication branch: `chatgpt/review-ai-player-ap2-rereview2`
- Date: 2026-11-13

Read `AI_PLAYER_AP2_REREVIEW2_HANDOFF.md` first, then `IMPLEMENTATION_HANDOFF.md` section 5. Reviewed
`owed.py`, its spending and equipment integrations, request ordering, persistence, the pocket rule and the
session wait. The client/resident delivery code, run-lock implementation and call-budget implementation are
unchanged in this diff. Their previous verdicts are not reopened.

## H2 and H4: completion and verification are now separate

`player/owed.py` keeps obligations under the batch that created them. An unmarked row remains owing until
either its own batch returns a qualifying read, or the batch has been marked complete and a subsequent
request supplies a read. The distinction is persisted in the world file.

The ordering of the integrations is correct for the reviewed paths:

1. The brain takes in call-ledger completion evidence.
2. `World.absorb` applies the current request's profile reads to the existing spending rows, then marks
   completed rows with `owed.settle`. It does not mark between profile reads in that request. The profile's
   `closes` flag prevents a read preceding other results in its own batch from paying that batch off.
3. Equipment updates the feed from a usable item read and applies `owed.read` to its existing stale rows.
   Only after processing the results does it mark completed equipment rows. Newly marked rows make the next
   item read due immediately.

Thus a read that arrives in the same request as another relay's completion cannot pay off that relay's
newly completed obligation. The ordering remains intact when a new Brain loads the world for each request.
A receipt retry returns the existing answer rather than processing the reads or marking the rows again.

The ordinary case still works: the batch's own trailing read clears its obligation without requiring a
replacement-relay round trip. Item selection and backup-equipment plans place their item read after the
mutation. The new protocol number, 7, also separates these admission rules from the reviewed predecessor.

### Unchanged overlap reproductions

The previous review's `overlap.py` was rerun unchanged. Its direct execution now fails at the assertion of
the old H2 defect, as expected: the second 180,000 purchase batch is no longer admitted. A wrapper calls its
unchanged observation functions and records these results:

| Case | Result at the frozen target |
|---|---|
| B reads before A buys, then returns that read with A's completion | A's 180,000 reservation remains, marked complete; measured spend stays 49,820,000; zero additional purchases |
| Spending control: B reads after A buys, but its read was requested before the brain knew A was back | Measured spend reaches 50,000,000; zero additional purchases; the reservation remains for a subsequent read |
| B reads items before A selects, while A is still loose | A's stale row remains unmarked; the hunt waits; the feed describes the equipment at the time of that read |
| Equipment control: A finishes before B reads, but the read arrives with the completion evidence | The feed names the new weapon; A's stale row remains marked complete; a new item read is requested immediately |

**Both controls now intentionally require one additional qualifying read.** This is conservative and correct:
the brain cannot infer execution order merely from the order in which the completion word and results arrived.
The correction tests follow both controls through that next read and verify that the reservation/stale row
clears, with spending still at the cap and the hunt resuming on the refreshed equipment.

Additional independent checks passed:

- For both spending orderings, a failed subsequent profile read preserves the marked reservation. A later
  successful profile clears it, records total spend as 50,000,000, and admits no further purchase.
- An equipment completion request interrupted before the client saves its pending answer survives receipt
  retry with the same stale row. A failed refresh preserves it; a later successful refresh clears it and
  permits the hunt.
- A seeded two-batch ledger exercises selective release: the request completing A marks A without clearing
  it; the next request's read clears A while completing and marking B; the following read clears B. Spending
  and equipment rows follow the same order, including a saved-world restart between requests.

These checks address the premature releases reported in H2 and H4. Keeping an obligation while its relay
remains loose, and sometimes keeping a measured reservation for one more read, are deliberate conservative
holds rather than remaining defects.

## H3: the limit holds with banking disabled, and the session explains its wait

`World.overfull` now depends on the pocket balance alone. The unchanged reproduction confirms that training,
session-end and hunt paths issue no global trip with 9,400,000 in pocket when banking is disabled. The gate
refuses the trip for all three activities as well.

The session now emits a profile-read batch with at least a 30-second hold when it is away from home and
cannot deposit. Its note distinguishes a disabled bank activity from a deposit waiting for retry, and states
the balance and 200,000 limit. When a deposit is available, banking gets its turn first. The independent
refusal case stayed in this wait through a restart, then allowed the trip home at **exactly 200,000**.
Existing correction tests also cover banking by hand and the disabled-bank explanation.

The OPERATOR additions describe the pocket rule and the extra obligations held by an outstanding batch
consistently with these paths. The bank-switch exception identified in the previous review is gone.

## Evidence and verification

Published evidence:

- [overlap.py](evidence/ap2_rereview2_lane_a/overlap.py): unchanged from `89a18dc3`;
  SHA-256 `ed5471c8fad1b51764ea3008440a0d526d9671cd69808a1de38176d9d3869995`.
- [run_prior.py](evidence/ap2_rereview2_lane_a/run_prior.py) and
  [observations.json](evidence/ap2_rereview2_lane_a/observations.json): the old observation functions with
  checks for the corrected behavior, without the old script's assertions that the defects must occur.
- [independent.py](evidence/ap2_rereview2_lane_a/independent.py): four additional checks, including both
  spending-order subcases, equipment receipt/failure handling, selective release, and the session wait.
  The two-batch case seeds ledger state explicitly; the overlap and retry cases use the real `next`/`put`
  client paths in temporary worlds. All lock behavior used by these added checks is rehearsal behavior.

Commands rerun:

```sh
python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .
# 548 tests, OK, none skipped; includes all 16 new correction tests
python3 -W ignore::ResourceWarning -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py
# 46 tests, OK
PYTHONPATH=. python3 docs/reviews/evidence/ap2_rereview2_lane_a/run_prior.py
PYTHONPATH=. python3 -W ignore::ResourceWarning docs/reviews/evidence/ap2_rereview2_lane_a/independent.py -v
# corrected observations reproduced; 4 independent tests, OK
python3 scripts/player_allowlist.py check
python3 scripts/player_allowlist.py report --check
python3 scripts/rulings_index.py --check
python3 scripts/check_large_files.py
git diff --check
# all passed
```

The support fixture's default pocket was reduced from 2,000,000 to 150,000 so ordinary trip tests model a
permitted balance. This does not replace the explicit over-limit tests above, which still use 9,400,000.
The changed existing tests now expect the corrected holds and supply the required readbacks.

**Zero live requests, game writes, or live credentials/session material used.** The suite's real lock-tool
tests use temporary local repositories; no real main-branch lock was claimed or changed. Only this report
and its evidence are published. No implementation file or `fable/*` branch is modified. Live-session
acceptance and the unbuilt part of AP2 remain outside this verdict.
