# AP1 independent re-review, Lane A — 7cf7d73c

Repository: `perseverance484/tnr-tools`. Frozen target: `7cf7d73c5cb235801b66e4b4763cb63e1bc7b14e`; code commit: `5ab5192b382e7af069452f57b9b1550d9475d085`; base: `c412de4df43baf4f11fbd817efb0f7ae95c08226`.

**Verdict: accept. H1 is closed. No new finding in the requested scope.**

I read `AI_PLAYER_AP1_REREVIEW10_HANDOFF.md` first, then Implementation Handoff section 5. A narrow re-check is sufficient: the only production behavior change is `player/relay.py:27`, `PROTOCOL = 2`. I reviewed its consequences across the client, pending batch, request content/name, answer, receipt and ledger, using the real `29797ba0` and `c412de4d` packages and current-version controls. This is acceptance of this frozen correction, not a new review of all AP1.

## H1 closure evidence

I reran both scripts from [the previous review](https://github.com/perseverance484/tnr-tools/blob/e7e4c0f684e709753048ee219b47780df64fe217/docs/reviews/AI_PLAYER_AP1_REREVIEW9_REVIEW.md), unchanged. Their assertions describe the former defect, so an assertion failing because no calls were printed is evidence of closure.

| Original case | Result on this head |
|---|---|
| `pending`, predecessor 29797ba0 | No calls; stops at the old assertion expecting calls. Ledger marked 2. |
| `receipt`, predecessor 29797ba0 | Old relay receives STOP; no calls; old assertion fails. |
| `ack` | Two new calls after **60.5 seconds**, rather than four after 8 seconds. |
| `installed` | No calls past the already-saved hold; old assertion fails. |
| `expired` | No calls; the negative control still passes. |
| `trusted`, unchanged maker c412de4d | No calls; old assertion fails because that maker is now a predecessor. |
| Original real-29797ba0 resident script | Old resident remains alive, no calls printed; the old `assert calls` fails after the normal response timeout. |

For the current-version positive control I changed only the maker SHA to the frozen target in a separate copy: pending and receipt modes both delivered their four calls after their own **8-second** wait, with no migration hold. I also substituted `c412de4d` as the maker in the predecessor cases: pending, receipt and installed modes emitted no calls; acknowledgement allowed calls after **60.5 seconds**. These are actual extracted historical packages, not reconstructed old records.

The replacement of the maker SHA is necessary for a current-version control; leaving `c412de4d` in that control would now test rejection of a predecessor instead. None of the original scripts was edited.

## Protocol boundary, path by path

| Surface | What I verified |
|---|---|
| Client file | Protocol-1 clients are read as no client. Old relay tokens receive STOP. Their pending/ended/unprinted claims do not authorize new publication or release. |
| Pending batch | A protocol-1 batch is not printed from a predecessor client or from an otherwise current client. Both fresh and stale batches are covered, including a hold saved before the replacement asks. Outstanding calls remain held. |
| Request content and filename | Current requests use `p2-req-…`; both real predecessor residents read `req-…`/`p1-req-…` and leave them alone. Tests cover a resident left running, ended during the wait and ended first, for each predecessor. A protocol-1 request is not served as protocol 2. |
| Answer | A protocol-1 answer is discarded even at the expected answer path with matching request identity. I additionally had each real predecessor generate an answer, stopped its caller before consuming that file, and passed that actual file through the current `_await`: both were removed and refused. |
| Receipt | The predecessor's accepted results are not applied twice; its batch is withheld. Current-version receipt retries return the same batch without calling `handle` again. |
| Ledger | Both an unmarked 29797ba0 ledger and a marked protocol-1 c412de4d ledger acquire the 30-call update reservation. Current ledgers retain protocol 2 and do not acquire a hold on ordinary restart. |

The strict number check remains `type(protocol) is int`, with the predecessor's number explicitly covered by the stamp tests. The old resident is isolated before it can interpret the current request; rejecting an answer afterward is no longer the only defense. Current resident delivery still works.

The fixture tests regenerated the predecessor state from Git history and ran without skipping. The three earlier 442a6311 fixture folders are byte-for-byte unchanged from the base. The new fixture tests check structural/protocol agreement and exercise the real packages as well; I did not treat fixture shape alone as proof of compatibility.

## Migration and delivery controls retained

The existing 15 migration tests pass: a concrete acknowledgement id, no widening on replay, the full quiet minute, persistence across brains/retries, selective release of known holds, invalid/foreign ledger markers, and no lane exempt from the hold. Earlier ownership, retention and result-idempotence controls also pass in the full player suite.

I reran the previous `known_limit_repro.py` unchanged. Without acknowledgement, no new call is issued and the simulated minute contains only the four old calls. With acknowledgement, and with acknowledgement followed by sixty seconds, peaks stay at **30 total / 20 world**.

The predecessor's final batch becomes an unknown-owner hold when the new relay first asks. An acknowledgement given before that point does not silently expand to cover it. The operator page now explicitly says to list and acknowledge again. This is conservative accounting with a visible recovery step, not a remaining H1 defect.

The current-only pending, receipt and resident tests all pass. In particular, rejecting a foreign receipt does not mean reapplying its results, and rejecting a foreign client does not mean treating its outstanding calls as returned.

## Test discrimination and scope limits

On the base production code, with the current test files/fixtures copied into an isolated checkout, `test_rereview9.py` gives **17 failures, 3 passes, no errors**. All three passes are current-version delivery controls.

I agree with the handoff's qualifications: four failures treat c412de4d as its own predecessor on the base; the stale-batch case fails on retained ownership rather than publication; and the 29797ba0 stop-first case fails on the old holder's identity. These are useful boundary assertions, but not seventeen independent reproductions of H1. The remaining failures include the actual pending, receipt, acknowledgement and resident bypasses.

The strengthened walk checks that a rewritten foreign ledger becomes marked current, and its foreign-record events now include protocol 1. That closes the described test blind spot. It remains a single-version model, so the real-package tests are the relevant evidence for H1. I did not repeat the author's 200-walk campaign or 61 mutations for this one-line runtime correction; the full suite includes the walk's six deterministic regression seeds. The historical-package discrimination above was independently run.

A manually maintained protocol number is acceptable for this correction. The existing rule now clearly covers admission semantics, and the regression tests pin these predecessors as incompatible. Automatic hashing of the whole package is not required to close H1. This does not waive advancing the number when a later change invalidates older batches.

## Verification

| Command/check | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | 389 tests, OK, none skipped |
| `python3 -W ignore::ResourceWarning -m unittest -v player.tests.test_rereview9 player.tests.test_rereview8 player.tests.test_rereview6.N1NothingOfAnotherProtocolIsUsed` | 42 tests, OK, none skipped |
| Current `test_rereview9.py` on c412de4d production code | 17 failures / 3 passes; no errors |
| Original H1 scripts, predecessor substitutions, current-maker controls | Results above |
| Actual saved predecessor answers through current `_await` | Both refused and removed |
| Original forgotten-ledger reproducer | No-word 4/4 old calls only; acknowledged cases 30/20 |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | 46 tests, OK |
| `player_allowlist.py check` and `report --check` | Clean; report current |
| `rulings_index.py --check` | 322 rulings; current |
| `check_large_files.py` | Clean |
| `check_no_real_name.py --commits c412de4d..7cf7d73c` | Zero hits |
| `git diff --check` | Clean |

I did not rerun the unchanged legacy pilot programs or broaden into battle behavior, token measurements, AP2, or settled rulings. The agreed brain split remains after acceptance and before AP2. The operator instructions belong in the live-session brief; live relay behavior and token costs remain unmeasured by this review.

No existing tracked file changed in the review checkout and no `fable/*` branch was modified. Only this report was added on `chatgpt/review-ai-player-ap1-rereview10`; historical packages, altered test copies and scratch scripts stayed outside the checkout.

**Zero live-game requests, game writes or live credentials used.**
