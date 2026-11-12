# AP1 independent re-review 7 — Lane A

**Verdict: request changes. F1 is closed.** One high-severity finding remains in the newly scoped older-resident case: rejecting an old brain's answer does not prevent that brain from releasing outstanding reservations in the shared world file. Reproduced with the real `442a6311` resident process: 34 total calls or 24 world calls become possible in a minute.

Repository: `perseverance484/tnr-tools`. Frozen target: **`06358ca539372cae12d41b086a465719f403aba7`**. Code: `ad62b72687df61f29f05c09f6ab197afc297329d`. Base: `60a28a84fb9b47910827c234b2e64e760ddcaa81`. Date: 2026-11-12. Report branch: `chatgpt/review-ai-player-ap1-rereview7`.

Read the handoff first, then Implementation Handoff §5. Reviewed legacy queued/pending upgrades, outstanding holds, selective release, current pending/receipt delivery, and both changed assumptions: rejecting the entire older client file and checking protocol numbers on answers and receipts. RUL-2026-11-11-149 through -152 remain settled. The brain split stays after acceptance and before AP2.

## Finding

### 1. G1 — High: an incompatible resident consumes the new request and releases calls before its answer is rejected

Location: **`player/brain.py:696`–697**, `_exchange`, with the compatibility check delayed until `_await` at **line 742**. Related claim: handoff's older-brain section and known limit 2; `player/OPERATOR.md:64`–66.

The new client publishes its request into the shared inbox before establishing that the resident holding `brain.lock` understands the new protocol. The still-running `442a6311` brain consumes that request. It does not understand `held`, `gone` or the protocol number; it interprets absence of its old `lost` flag as the last relay returning. It settles outstanding calls and saves `world.json`. The new client does not accept its answer, but that does not undo the ledger mutation.

Reproduction:

1. The actual `442a6311` package issues four world calls to relay A. A keeps the batch and never returns or is confirmed stopped. Its real resident `brain.run` starts and holds the one-brain lock.
2. The new client starts a replacement. The old client file is rejected as intended. The new request has no held batch and no `lost` flag.
3. The old resident consumes it. All four old reservations become settled `[time, "world"]` entries. The new client waits and prints only its retry command, so the answer-rejection behaviour looks correct.
4. End the old resident and retry with the new brain. Its receipt path emits no old batch and does not reapply results, but the four settled reservations remain settled. No record identifies them as still held.
5. After their accounting minute, A can execute its four calls while the current pacer admits 30 recovery calls or 20 world calls: **34 total / 24 world calls** in a minute.

This directly refutes the claim that an older brain left running produces only a stall while the calls remain held. No old batch needs to be printed by the new version for the guarantee to fail.

Refutation controls:

- This is not a downgrade after the update. The old process starts first and retains the actual brain lock; only the new client runs afterwards. It uses the old package's original `brain.run`, `Brain.handle` and ledger implementation. The constructor wrapper only announces when the resident has acquired the lock and loaded its world.
- Neither client nor ledger files are manufactured by the reproducer. The old package creates the batch; the new client creates its own request. The only control setting written is `paused: true`, which isolates the four existing reservations by keeping the old resident's new decision empty. Pausing is not completion evidence for A.
- The first new response contains no call, and the subsequent receipt retry contains no old call. The protocol checks work; they act too late to protect shared accounting.
- Ending the old resident **before** the first new request, with the same setup, leaves four loose reservations and gives maxima **30 / 20**. This is the working control.
- The existing real-old-brain receipt test hands back a batch from the same relay. In that setup the old brain's implicit “returned” interpretation is true. It does not exercise a new replacement while a different old relay still owns its batch.

Required correction: enforce a safe resident handoff before publishing work that an incompatible brain can consume. Preserve the outstanding reservations across that handoff. Rejecting the response afterwards is insufficient. Add the real old-resident/new-replacement case with an unreturned batch, and retain same-relay receipt and stop-first controls. The operator instructions should require the safe ordering and should not describe an incompatible resident as an accounting-safe stall until the implementation establishes that.

Runnable reproduction from the frozen repository root. It uses the test helper only to extract the exact historical package; the separate process runs that package's real resident loop. Requires `442a6311` in repository history. All game calls are simulated; the client timeout is advanced by a test clock.

```bash
python3 - <<'PY_REPRO'
import io,json,os,subprocess,sys,time
from pathlib import Path
from unittest.mock import patch
from player import brain,relay,calls as K
from player.tests.test_relay import token_of
from player.tests.test_rereview5 import the_package_before
from player.tests.test_rereview2 import most_in_a_minute
old_program=r'''
import io,json,os,time
from unittest.mock import patch
from player import brain,relay
from player.tests.support import Rig,user
from player.tests.test_relay import token_of
r=Rig();r.world.absorb([user()._replace(at=r.t)]);r.world.save()
def nxt(token=None):
 out=io.StringIO();brain.next_batch(r.dir,token,out,lambda _:None);return out.getvalue().splitlines()
with patch.dict(os.environ,{'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':r.dir+'/none','TNR_PLAYER_FIGHTS':r.dir+'/fights'}):
 a=token_of(nxt(token_of(nxt()[0]))[-1])
 real=brain.Brain
 def started(live):
  home=real(live)
  print(json.dumps({'live':r.dir,'token':a,'out':len(home.world['budget']['calls'])}),flush=True)
  return home
 with patch.object(brain,'Brain',started):
  brain.run(r.dir)
'''
root=the_package_before();assert root
old=subprocess.Popen([sys.executable,'-c',old_program],cwd=root,env={**os.environ,'PYTHONPATH':root},text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
try:
 made=json.loads(old.stdout.readline());live=made['live']
 assert made['out']==4
 now=[time.time()];real_brain=brain.Brain;real_sleep=time.sleep
 relay.write(live+'/control.json',{'version':1,'paused':True})
 def sleep(t):
  if relay.pending_requests(live):
   for _ in range(500):
    if not relay.pending_requests(live):break
    real_sleep(.01)
   assert not relay.pending_requests(live)
  now[0]+=max(t,1.0)
 def nxt(token=None):
  out=io.StringIO();brain.next_batch(live,token,out,sleep);return out.getvalue().splitlines()
 with patch.dict(os.environ,{'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':live+'/none','TNR_PLAYER_FIGHTS':live+'/fights'}),patch.object(time,'time',lambda:now[0]),patch.object(brain,'Brain',lambda live:real_brain(live,clock=lambda:now[0])):
  token=token_of(nxt()[0]);lines=nxt(token)
  print('new client while old resident holds lock:',lines)
  calls=relay.read(live+'/world.json')['budget']['calls']
  print('old relay has not returned; ledger:',calls)
  assert len(calls)==4 and all(len(c)==2 for c in calls)
  old.terminate();old.wait(timeout=5)
  print('new brain receipt retry:',nxt(token))
  for lane,n in [('recovery',15),('world',10)]:
   clock=[now[0]+62];budget=real_brain(live,clock=lambda:clock[0]).budget;made_times=[clock[0]]*4
   for _ in range(n):
    steps,_=budget.pace([K.user(),K.user()],lane)
    for s in steps:
     if 'wait' in s:clock[0]+=s['wait']
     else:made_times.append(clock[0]);clock[0]+=.01
   print(lane,'real calls in a minute:',most_in_a_minute(made_times))
finally:
 if old.poll() is None:old.kill()
 old.wait();old.stdout.close();old.stderr.close()
PY_REPRO
```

Observed: the first new response and receipt retry contain only `brain next` lines; the four ledger rows have no `out`/`loose` state; final maxima are `recovery 34`, `world 24`. The script asserts that the four calls were wrongly settled. For the stop-first control, end the child immediately before the first `token=token_of(nxt()[0])`, and expect four `loose` entries instead: the maxima become 30 / 20.

## F1 unchanged: closed

Reran `/workspace/scratch/ap1-rereview6/pending_upgrade_repro.py` unchanged. Before its defect assertion fails, it prints:

```text
old loose calls: 21
legacy pending accepted: False
new code printed: [] served requests: 1
old calls in preceding minute: 20 with new calls: 20
current budget would admit: []
```

The final `assert actual > 20` fails because the violation no longer occurs. The current pending-upgrade regression also verifies that the 21 previously loose calls and two waiting calls remain held, including twenty minutes of retries; operator acknowledgement is followed by the extra sixty seconds before capacity returns. The old waiting process, when allowed to wake after takeover, says STOP rather than printing its batch.

## Changed assumptions and current-protocol controls

**Client file.** A missing, different or incorrectly typed protocol number makes `_who` read the file as no file. Its old relay names, pending batch, ownership and queued operator evidence are not imported. An old token is told STOP; `put` cannot attach results to it. Listing remains read-only. A new handshake creates a fresh protocol-tagged file, and the current brain conservatively holds otherwise unclassified reservations. The decision to ignore even a previously queued operator word is documented: the operator must say it again after update. This is conservative, not a release by omission.

**Records.** Inspected the protocol write/read sites for client, pending batch, request, answer and receipt. `relay.ours` requires the exact integer; booleans, floats and strings do not count. A compatible container does not make an untagged nested pending batch acceptable. A request still needs its required fields, and an answer still needs its request ID. The revised foreign-request-answer test carries the protocol number, so it continues to test request identity rather than merely failing the new protocol check.

**Receipts.** A foreign receipt for the same relay/sequence prevents reapplication of already-saved results, but returns only the fallback response, not the old batch. Current receipts still deliver their original batch without re-running `handle`. Current pending batches still reach either their original relay or a replacement exactly once. The three positive delivery/receipt controls pass.

**Limits of those checks.** No older client/pending/answer/receipt batch was printed by this version in the tested upgrade paths. G1 violates the other half of the requirement: an older process can change shared reservations while the new client is refusing its output. The protocol tag is not a boundary around the old resident's writes to `world.json`.

**Operator page.** The update section correctly explains old relay rejection, conservative holds and repeating operator acknowledgement. Its old-resident instruction must be considered together with G1. Stopping that resident before any new request is the verified safe ordering; waiting for it to produce rejected answers is not established as safe. No change to the trusted meaning of `stopped` is requested.

The manual requirement to increment `relay.PROTOCOL` when record meanings or admission rules change is clearly documented. It remains a maintenance obligation, not an additional finding in this correction.

## Fixture and real-package verification

Generated a fresh pending-upgrade state with the actual `442a6311` package and compared it with `player/tests/fixtures/upgrade_442a6311_pending`.

- Full `client.json` and `world.json` structures and non-generated values match. At the fixture's fixed clock, world values match except the generated receipt relay name; client differences are the generated relay/token references and pending ID.
- All seven printed batches have identical call names, inputs, selectors and internal waits. Transport lines differ in temporary package paths and generated tokens.
- The clock and eight-relay count agree. `made.json` records provenance (`by`/`how`) while the fresh helper additionally reports its temporary `live` path and wake result; this is metadata, not a different runtime state.

All three requested historical-package tests **ran and passed without skipping**, both within the full suite and in an explicit verbose run:

1. `N1ABatchTheVersionBeforeLeftWaiting.test_the_version_before_itself`
2. `N1ABatchTheVersionBeforeLeftWaiting.test_the_old_brain_next_was_not_killed_and_wakes`
3. `N1NothingOfAnotherProtocolIsUsed.test_a_receipt_of_the_version_before_itself`

The fixture genuinely covers the stored-pending case, including an old client process still waiting. It does not cover an incompatible resident settling a different relay's outstanding batch, which is why G1 survives these tests.

## Earlier cases retained

Original E/D/A/B/C scripts were rerun unchanged. C1, C2, C5 and controls retain the previously recorded adaptations; none required a new adaptation for this target.

| Case | Disposition and evidence |
|---|---|
| E1 | Closed: old queued request is removed unanswered; four rows stay `out`; unchanged defect assertion fails as expected. |
| E2 | Closed: `stopped 1` selects only `batch 1`, reports no unknown name and retains the unrelated held batch; unchanged defect assertion fails as expected. |
| D1 | Closed: operator-word replay leaves the later active reservations at 3, then 3. |
| D2 | Closed: four calls remain loose; current-client missing-history case peaks at 30 total / 20 world. |
| D3 | Closed: first crash holds 1 s, subsequent four requests each hold 6 s. |
| Retention | Pass: timeout leaves token/held/handed unchanged; put result survives timeout/death, applies sector 77 once and is removed. |
| Adapted C5 | Closed: replacement gets its own profile batch and receipt; genuine completion evidence is applied. |
| Adapted C1 | Closed: no release by elapsed time; peaks 30 / 20. |
| Adapted C2 | Closed: a relay that never got a batch queues no completion evidence; four calls remain held. |
| C3 / C3b | Closed: repeated-crash fallback acts with resident/restarted brains and the actual fallback client; learned state and receipt survive; completed fight sends no action. |
| C4 | Closed: falsey/malformed answers count as zero accepted/unknown actions and do not block fallback. |
| Earlier controls | Pass: completion accounting peaks at 30; ordinary replacement gets a new decision/receipt; normal closure sends no old-fight action. |
| A1 | Closed: outstanding accounting survives watchdog; actual peak 29. |
| A2 | Closed: unusable reads preserve the good state and allow defensive fallback. |
| A3 | Closed: old pending waiter emits no stale calls; fresh pending batch emits the new profile read. |
| B1 | Closed: malformed log action produces defensive actions and zero crashes; old defect assertion fails. Existing valid-action control also acts without crashing. |
| B2 | Closed: abandoned-call peak 30; both timestamp-skew cases peak 20. |
| B3 | Closed: results applied once (`[1]`). |

Ordinary actual-package upgrade through `brain next` retains the four old calls, including after the old token returns. Numeric selective acknowledgement succeeds. Additional ownership controls pass: two replacements leave only the final relay's calls; response waiting blocks a competing handshake; SIGKILL releases the client lock and lets the waiting handshake finish.

## Test discrimination and mutation

On a scratch package extracted from `60a28a84`, the new regression module gives **8 failures, 4 errors, 3 passes**, as claimed. Supplied `relay.PROTOCOL = 1` only in that test process, and copied the new historical-package extraction helpers needed by the new tests; all production modules remained the base version. The loader's repository root was directed to the real Git history. No base checkout file was edited.

The four errors are all missing `protocol` fields in records the old code writes: client-file test, receipt test, request test and every-record test. They are representation/API differences, not four additional independently reproduced old failures. The three passing tests are the unchanged current pending/receipt delivery controls; the eight failures provide the behavioural discrimination.

Planted one independent defect in an isolated process: changed `_answered` from `ours = relay.ours(done) and done["batch"]` to `ours = done["batch"]`. The full 346-test suite detects it with **three failures, no errors**: foreign receipt, actual old-package receipt, and foreign pending batch/receipt in a current client file. No tracked implementation file was changed. I did not independently rerun all 34 mutations in the handoff.

The random walk passes **200 walks, 6,948 calls, zero problems**. Its new removal-of-protocol event and model treatment are consistent with the new client rule. It still uses one protocol's running implementation; it cannot expose G1's old resident mutating the ledger. All 15 new tests also pass in a run with repository file snapshots and bytecode writes disabled, leaving no repository file additions, removals or modifications.

## Verification

| Command/check | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | 346 tests, OK; no skips reported |
| `python3 -m player.tests.test_walk 200 300` | 200 walks / 6,948 calls / zero problems |
| Three real-package tests, explicit verbose run | 3 tests, OK, none skipped |
| New regression module on base | 8 failures, 4 errors, 3 passes |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | 46 tests, OK; existing ResourceWarnings |
| `python3 scripts/player_allowlist.py check` | Exit 0; zero never-list violations |
| `python3 scripts/player_allowlist.py report --check` | Exit 0; current |
| `python3 scripts/rulings_index.py --check` | Exit 0; 322 rulings, index current |
| `python3 scripts/check_large_files.py` | Exit 0 |
| `python3 scripts/check_no_real_name.py --commits 60a28a84..06358ca5` | Exit 0; tracked files and correction messages |
| Four legacy pilot tests | All exit 0; planner parity 4,000/4,000 |
| `python3 scripts/player_size.py` | 3,986 code lines / 19 files; 6,205 test lines; brain 849, battle 685; 16 functions over 12 branches |
| `git diff --check` | Clean |

Legacy commands, from `state/player/dauntless/tools`: `python3 tests/test_planner2.py`, `python3 tests/test_pilot.py`, `python3 tests/test_integration.py`, `python3 tests/test_nearkill.py`.

Unchanged fight simulations retain 14 / 9 / 13 turns and peaks of 23 / 27 / 24 calls, with 78 / 48 / 82 total calls and no action pacing holds. Maximum unread spans are 16.4 / 36.6 / 21.4 seconds. These are offline fixture figures; no live-play or token-cost improvement was measured.

## Next step and safety statement

Correct the incompatible-resident handoff and repeat that affected scope: no current request consumed unsafely by the old owner, preserved reservations before/after it stops, and normal current pending/receipt delivery. Retain the queued/pending migration fixtures and selective-release controls. The split of `brain.py` remains after correctness acceptance and before AP2.

No live-game request, game write, live credential access or live relay connection was made. The frozen detached checkout and all pre-existing tracked files are unchanged. Legacy tests' established untracked outputs were moved to scratch. Only this report is added on a separate `chatgpt/review-*` branch; no `fable/*` branch is modified. Reproductions, extracted packages and mutations ran in temporary/scratch locations or isolated processes.
