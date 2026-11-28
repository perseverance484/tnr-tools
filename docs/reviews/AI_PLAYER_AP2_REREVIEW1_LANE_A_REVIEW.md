# AP2 correction — independent Lane A re-review

**Verdict: changes requested.** H1 is closed for the requested batch-delivery boundary. H2 remains high;
H3 and H4 remain medium in the cases below. The original four reproductions now show the intended fixes,
but reservation release and equipment freshness still fail when relays overlap.

- Repository: `perseverance484/tnr-tools`
- Implementation branch: `fable/ai-player-ap2`
- Frozen head: `87e497a6efa781fb1b43ef809cce3a3bd48b1842`
- Correction diff: `025c89f1..87e497a6`
- Previous review: `chatgpt/review-ai-player-ap2` at `12bf61d31e973692698c777fb19e5d0867e3f16c`
- Publication branch: `chatgpt/review-ai-player-ap2-rereview1`
- Date: 2026-11-13

Read `AI_PLAYER_AP2_REREVIEW1_HANDOFF.md` first, then `IMPLEMENTATION_HANDOFF.md` section 5. Reviewed the four
corrections and the wider reservation and delivery assumptions they introduce. The ruling documents and AP1
merge before `025c89f1` are not this correction. **No verdict on AP1 at `62e1aab1` is given here.**

## H2 — High, still open: an earlier profile read releases a completed relay's unmeasured reservation

Locations: `player/world.py:249–256, 300–308, 354–362`; completion evidence is applied first by
`player/brain/core.py:Brain._ledger`.

The shared allowance now correctly bounds purchases within a batch. Its reservation also survives a restart
and stays reserved while the old batch is loose. The remaining problem is the transition out of that state:
`_paid` treats every reservation absent from the ledger's current open batches as measured by the profile
being absorbed. `closes` establishes ordering only among results in that one request. It does not establish
that this profile was read after a different relay's purchases.

The new reproduction uses the actual `brain next`, `brain put`, replacement handshake, and saved world files.
Each decision loads a fresh Brain. No disk corruption, invented completion word, or duplicate request is
needed:

1. Today's measured spend is 49,820,000; the remaining allowance is 180,000. Pocket is 400,000, bank
   900,000,000. Restock issues relay A a 180,000 purchase batch and reserves it under A's batch ID.
2. Relay B replaces A. B receives an item/profile-read batch, executes those reads **before A purchases**,
   and stores the results with `brain put`. They show the original inventory and 400,000 pocket balance.
3. A finishes its already-issued purchases, spending 180,000, and returns with its own batch token.
   `brain next A` correctly returns `SUPERSEDED` and records that A is back. Its purchases are now over.
4. B hands in its earlier reads. The request also carries A's completion evidence. The ledger closes A,
   `_paid` removes A's reservation, and the old profile shows no balance decrease. Measured spend remains
   **49,820,000**.
5. The brain issues B another **180,000** of purchases, with **zero pending decisions**. The earlier 180,000
   reservation is gone, replaced by the new batch's reservation. Both batches can be paid from the initial
   400,000 pocket, so their combined admitted cost is 360,000 against 180,000 available that day.

The bank activity is enabled throughout. No trip is taken. This is the normal priority of an active restock
pass over banking, not the banking-off exception in H3.

**Control:** move B's reads after A finishes and report the resulting 220,000 pocket balance. Measured spend
becomes 50,000,000, A's reservation is removed, and the next batch is a bank deposit with no purchase. The
distinguishing fact is when the profile was read, not when it was handed in.

**Required correction:** completion and measurement need separate evidence. Keep a completed batch's
reservation until a profile known to cover its possible spending has arrived. If the ordering cannot be
established, obtain a fresh profile after learning that the batch is over. Preserve that obligation through
restart and receipt retry. Do not change AP1's valid completion accounting to compensate for this spending
accounting gap.

## H3 — Medium, still open: disabling bank also disables the pocket-limit gate

Location: `player/world.py:344–352`, used by all three trip planners and `Gates._road`.

With banking enabled, training, session-end and hunt trips now wait for a deposit; the gate independently
refuses an over-limit trip. Refusal/retry and exactly-200,000 controls pass. But `overfull()` returns false
whenever `control.activities.bank` is false. The reproduction switches off that one activity and observes
all three paths admit `travel.startGlobalMove` with **9,400,000 in pocket**. A direct check of the gate also
returns `allow` for each activity.

The handoff explicitly proposes this exception as an implementer's reading. RUL-2026-11-12-153 says that
200,000 is the limit while running around; it does not make that limit conditional on whether automated
bank transfers are enabled. Switching off an activity is not an explicit change to this spending rule.
The new test deliberately expects the bypass, so its passing result does not establish compliance.

**Required correction:** keep the pocket limit in force independently of the bank activity switch. If the
bank is off and the pocket is overfull, hold voluntary trips and explain why. An explicit director ruling
authorizing the exception would be an alternative basis for acceptance; the handoff's proposed reading is
not that authorization. The scoped exemptions for urgent battle/recovery handling are not this finding.

## H4 — Medium, still open: a replacement's read clears stale equipment before the outstanding selection

Location: `player/activities/equipment.py:66–73`; retry scheduling at `wants` and `plan`.

The original defect is fixed: a selection now includes an item read, and an absent, failed, or malformed
read leaves the hunt/restock/repair waiting. However, the stale flag is still a single boolean. Any usable
item read clears it, even when a selection batch is still loose and may execute afterward.

Reproduction through the actual client paths:

1. A receives the selection batch: jutsu selection, item selection, item read, profile read. Inventory is
   marked stale. A has not yet executed the selection.
2. B replaces A. After the 30-second retry interval, B receives the standalone item/profile reads.
3. B executes and returns those reads before A selects. They correctly describe the old equipment.
4. The brain clears `inventory.stale` and resumes **`pvp_hunt`**, while the ledger still contains A's selection
   batch as **loose**. The planner feed still names the old thrown weapon.

A can now finish its already-printed selection after that read. The read that released the hunt was not
behind the mutation it was supposed to verify. This is the handoff's known limit 7, independently reproduced;
disclosing it does not close the H4 requirement. Both relays can follow the order of their own issued batches.

**Control:** A finishes and returns first; B then reads the newly selected equipment. The selection batch is
no longer loose, the feed names the new thrown weapon, and the hunt resumes correctly.

**Required correction:** bind the freshness obligation to outstanding equipment-changing batches. A read
must not discharge it while an earlier selection can still change the equipment afterward. Once those
mutations are known to be over, require a read that follows them before dependent voluntary planning resumes.
This does not require delaying an unsolicited fight, which remains the separately disclosed urgent case.

## H1 — Closed for delivery; observations and limits

The cutoff is propagated through `_record`, `_wire`, the saved receipt and the client's pending batch.
`within` cuts calls due at or after it; `Budget.unsend` removes the cut suffix from the call ledger.
`lapsed` is checked both when taking a pending batch and after the client's wait, immediately before printing.
Giving up a batch advances its sequence and reports it as unprinted, without reapplying its results.

The original script's five failing lease cases now print **zero calls**. The successful-renewal control still
prints three calls under the extended lease. Tests also cover a genuinely populated receipt/pending batch
made before cutoff, exact cutoff equality, waits inside a batch, and restarting within a valid lease. Protocol
6 rejects predecessor batches from both `988c56cc` and AP1's `62e1aab1`.

Three additional independent controls passed: a replacement relay receives the pending batch inside its
lease; it receives no calls after cutoff; and an answer written through the resident `serve` path is withheld
when the client wakes after expiry. The existing last-resort path also goes through `_paced` and `_record`.

This closes the requested **batch-to-relay delivery** finding. It does not establish a per-call runtime
interlock after printing: the relay receives no cutoff, and OPERATOR now explicitly allows completion during
the final minute and describes intervention for a stalled printed batch. Arbitrarily slow execution of an
already-printed batch remains the handoff's disclosed limit, not something these offline checks prove safe.

## Reproduction and verification

The previous report's script is copied **unchanged** as [prior.py](evidence/ap2_rereview1_lane_a/prior.py),
SHA-256 `76c9acf13761634aa292fdba97676e28d9384a5a1348b10467b318935eaab2c0`, matching `12bf61d3`.
Running it directly exits at its assertion that 180,000 exceeds the 170,000 allowance: that defect assertion
is now false. [run_prior.py](evidence/ap2_rereview1_lane_a/run_prior.py) calls the same observation functions
without those old defect assertions. [prior-results.json](evidence/ap2_rereview1_lane_a/prior-results.json)
records the results: 170,000 admitted in the constrained case, 180,000 in its control; banking before the
training trip; no session trip while overfull; and an item read behind selection with the hunt waiting.

[overlap.py](evidence/ap2_rereview1_lane_a/overlap.py) and [overlap.json](evidence/ap2_rereview1_lane_a/overlap.json)
contain the remaining H2/H3/H4 cases and controls. Their assertions establish the reported behavior on the
frozen target, not desired corrected behavior. [delivery_controls.py](evidence/ap2_rereview1_lane_a/delivery_controls.py)
contains the three additional passing H1 checks. All state is temporary; lock responses are scripted where
needed. The overlap checks use a fresh Brain for every client request and exercise persisted reservations.

Commands and results:

```sh
python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .
# 532 tests, OK, none skipped; includes 38 correction tests and the temporary-repository lock tests
python3 -W ignore::ResourceWarning -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py
# 46 tests, OK
PYTHONPATH=. python3 docs/reviews/evidence/ap2_rereview1_lane_a/run_prior.py
PYTHONPATH=. python3 docs/reviews/evidence/ap2_rereview1_lane_a/overlap.py
PYTHONPATH=. python3 -W ignore::ResourceWarning docs/reviews/evidence/ap2_rereview1_lane_a/delivery_controls.py
# observations reproduced; 3 additional delivery tests, OK
python3 scripts/player_allowlist.py check
python3 scripts/player_allowlist.py report --check
python3 scripts/rulings_index.py --check
python3 scripts/check_large_files.py
git diff --check
# all passed
```

The suite's passing reservation-release test supplies a profile in the same request as completion evidence,
but does not test a profile captured before the completed batch's purchases. Its H4 tests cover failed/missing
reads and normal successful selection, but not the still-loose selection cleared by a replacement's read.
The H3 bank-off behavior is intentional and tested; its unresolved issue is the rule it implements.

**Zero live requests, game writes, or live credentials/session material used.** The real lock tool ran only
inside existing tests against temporary local repositories. No real `main` lock was claimed or changed.
Only this report and its evidence are published; no implementation file or `fable/*` branch was modified.
