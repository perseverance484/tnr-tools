# AP1 independent re-review, Lane A — 29797ba0

Reviewed repository: `perseverance484/tnr-tools`. Frozen target: `29797ba0f769152381e71710f812605be9e0bfea`; code: `cc58d4762c54da6b21bf2705eec5900b0b463c6b`; base: `06358ca539372cae12d41b086a465719f403aba7`. Review date: 2026-11-12.

**Verdict: request changes for the disclosed migration safeguard, known limit 2. G1 is closed.** I found no additional undisclosed defect in the request-namespace or wait-loop correction. The remaining acceptance condition is the decision this handoff explicitly asks the reviewer to make: require safe admission after an untrusted legacy migration. Merely documenting known limit 1 does not preserve the call limits.

This is a focused re-review of the changed request publication/wait assumptions and the migration/delivery scope, with earlier reproductions retained as controls. It is not a fresh review of all AP1. I read the correction handoff and Implementation Handoff section 5 first. RUL-2026-11-11-149 through -152 remain settled; no token-use decision is reopened. The brain split remains after acceptance and before AP2.

## G1: closed, including the unchanged reproducer

I ran `old_resident_actual.py` from the previous review, unchanged, against this frozen head. It stops at the expected assertion inside `sleep`:

```python
assert not relay.pending_requests(live)
```

The request is still waiting after five real seconds. There is no normal summary output before this assertion. An exit status of 1 here is the old defect assertion being refuted, not a surviving defect.

I then ran a separate copy with exactly the handoff's adaptations: remove that assertion and the assertion that the four rows are settled, wait for the old brain only once, and print request/ledger state. These are the minimum changes needed to continue observing the corrected path; the original remains unchanged. Result:

- The request still waits; the old resident's four rows remain `out` while it owns `brain.lock`.
- After ending the old resident, this version answers. The four calls become `loose`, with no known holder, rather than being taken as returned.
- The simulated peaks are **30 total and 20 world**, formerly 34 and 24.

The new regression module passes all eight tests. Placing that module on `06358ca5` gives **six failures and two passes**, with no errors. The passes are the stop-first control and the other-protocol-name control. The busy-loop guard is one of the six failures. Its assertion is behavioral: the loop must wait, not repeatedly acquire a lock while its clock cannot advance.

## Required acceptance condition: known limit 2

**High impact; disclosed limitation, not a new finding about G1.** Relevant locations at this head: `player/OPERATOR.md:59` (update order), `player/brain.py:597` (admission through `next_batch`), `player/brain.py:769` and `:802` (`stopped`/held inventory), and `player/budget.py:98` (migration can preserve only rows that still exist).

The documentation correctly says that old ledger damage cannot be undone. Its proposed operator order does not cover all of that damage: it starts the new relay before the operator confirms old relays have stopped. More importantly, even moving `stopped all` earlier is insufficient when the old ledger is already empty. There is no row to settle, so that command establishes no sixty-second accounting tail for forgotten calls.

I reproduced this using the **real `442a6311` package**, without deleting or inventing ledger rows. Relay A receives four calls. Relay B replaces it. The old package is allowed to count again after its 900-second hold expires, so it writes an empty ledger despite A never having returned. The old program then exits, before the new version starts: the documentation's stop-old-brain-first condition is satisfied. This head immediately issues four calls and can subsequently admit enough calls for these peaks:

| Migration boundary | Total calls in a minute | World calls in a minute |
|---|---:|---:|
| No operator acknowledgement | 34 | 24 |
| Acknowledgement, old relay's last calls just before it | 34 | 24 |
| Acknowledgement followed by 60 seconds without new calls | 30 | 20 |

In the last two cases `stopped all` prints `{"stopped": [], "all": true, "not_held": [], "still_held": []}`. An empty inventory is not evidence of an empty real minute. The counts are simulated executions of emitted/paced calls, never game requests. The first four old calls are assigned just before the boundary independently of the ledger; that is legal for an outstanding batch whose holder has not reported. In the acknowledgement cases the holder is assumed actually stopped at the boundary.

**What I require before live acceptance:** an untrusted legacy migration must admit no call until the operator confirms the old actors can no longer execute, and admission must respect a full minute since their last possible call. A durable startup hold plus a sixty-second quiet period from that confirmation is one sufficient design; verified evidence that the quiet period already elapsed is another. An acknowledgement alone, or a quiet period while the old relay can still execute, is not sufficient. Preserve existing known holds and normal receipt delivery. Bind the acknowledgement to this migration, so a retry or later restart cannot reuse an older acknowledgement to bypass it. Do not make a replayable wildcard release.

This need not burden every ordinary restart with a trusted current ledger. It is required where migration cannot trust the predecessor's completeness. Update the operator instructions to match the implemented boundary. This is the requested review recommendation on an open decision, not a new ruling or an amendment to settled policy.

### Runnable evidence for the disclosed limit

From the repository root at the reviewed SHA, save the following as `/tmp/ap1-known-limit.py` and run `PYTHONPATH=. python3 /tmp/ap1-known-limit.py`. Git must contain `442a63119d2fa3fe033877bedc86f5df8cd9be00`, as for the real-package regression tests. The helper extracts that package into temporary storage. The program uses only local files, fake clocks and simulated calls.

```python
import io,json,os,time
from unittest.mock import patch
from player import brain,relay,calls as K
from player.tests.test_relay import token_of
from player.tests.test_rereview5 import by_the_version_before
from player.tests.test_rereview2 import most_in_a_minute
OLD=r'''
import io,json,os,time
from unittest.mock import patch
from player import brain,relay
from player.tests.support import Rig,user
from player.tests.test_relay import token_of
r=Rig();r.world.absorb([user()._replace(at=r.t)]);r.world.save()
now=[r.t];real=brain.Brain
def nxt(token=None):
 out=io.StringIO();brain.next_batch(r.dir,token,out,lambda t:now.__setitem__(0,now[0]+max(t,0)));return out.getvalue().splitlines()
with patch.dict(os.environ,{'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':r.dir+'/none','TNR_PLAYER_FIGHTS':r.dir+'/fights'}),patch.object(time,'time',lambda:now[0]),patch.object(brain,'Brain',lambda live:real(live,clock=lambda:now[0])):
 a=token_of(nxt(token_of(nxt()[0]))[-1])
 b=token_of(nxt(token_of(nxt()[0]))[-1])
 relay.write(r.dir+'/control.json',{'version':1,'paused':True})
 b=token_of(nxt(b)[-1])
 now[0]+=1000
 nxt(b)
 print(json.dumps({'live':r.dir,'now':now[0],'holder':a,'ledger':relay.read(r.dir+'/world.json')['budget']['calls']}))
'''
def scenario(mode):
 print("CASE:",mode)
 live,made=by_the_version_before(OLD);assert made['ledger']==[]
 print('old package expired all ledger entries; A never returned:',made['holder'])
 now=[made['now']];real=brain.Brain
 relay.write(live+'/control.json',{'version':2,'paused':False})
 def nxt(token=None):
  out=io.StringIO();brain.next_batch(live,token,out,lambda t:now.__setitem__(0,now[0]+max(t,0)));return out.getvalue().splitlines()
 with patch.dict(os.environ,{'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':live+'/none','TNR_PLAYER_FIGHTS':live+'/fights'}),patch.object(time,'time',lambda:now[0]),patch.object(brain,'Brain',lambda live:real(live,clock=lambda:now[0])):
  last_old_call=now[0]-.1
  if mode!='no acknowledgment':
   out=io.StringIO();brain.stopped(live,['all'],out);print('stopped all:',out.getvalue().strip())
  if mode=='acknowledgment plus 60 seconds':now[0]+=60
  lines=nxt(token_of(nxt()[0]));calls=[json.loads(s)['call'] for s in lines if s.startswith('{') and 'call' in json.loads(s)]
  print('new calls issued:',len(calls),'new calls; saved loose:',[c for c in relay.read(live+'/world.json')['budget']['calls'] if c[2:3]==['loose']])
  for lane,n in [('recovery',15),('world',10)]:
   clock=[now[0]];budget=real(live,clock=lambda:clock[0]).budget
   made_times=[last_old_call]*4+[clock[0]]*len(calls) # A makes its last four calls just before the boundary.
   for _ in range(n):
    steps,_=budget.pace([K.user(),K.user()],lane)
    for s in steps:
     if 'wait' in s:clock[0]+=s['wait']
     else:made_times.append(clock[0]);clock[0]+=.01
   print(lane,most_in_a_minute(made_times))

for mode in ("no acknowledgment", "acknowledgment only", "acknowledgment plus 60 seconds"):
 scenario(mode)
```

## Changed assumptions and attempts to refute them

### Publication and the older processes

I inspected `pending_requests` and `_lock` in all **27 ancestor commits containing the player**, from `3b3b4170` through `06358ca5`, including the live-session version. Each earlier request reader globbed `inbox/req-*.json`; each resident used `brain.lock`. Thus `p1-req-…` is outside those readers' namespace. This is a checked property of that history, not a claim about arbitrary forks.

At this head, `relay.request_path`, `is_request` and `pending_requests` agree on the current namespace. `brain.serve` checks the namespace as well as the record protocol and required fields. Old-name requests are removed unanswered. Another protocol's requests are neither opened nor removed by `serve`. `_sweep` clears abandoned requests across the name variants while the client lock serializes active callers; it does not license an older resident to consume a current request.

The real old-resident cases pass with the resident left running, terminated during the wait, and terminated before the request. I also reran the old `brain next` waking after replacement, queued upgrade and pending-upgrade controls. The stale caller prints no old batch, current delivery resumes, and reservations that remain in the saved ledger stay held. Shared-file ownership and receipt identity remain checked; the protocol checks from the preceding correction still apply.

This does **not** prevent an older process from servicing its own old requests or applying its own expiry rules. The locks serialize writers, but do not retrofit their rules. That is precisely the known limit above. Nor does it establish safe downgrade behavior or compatibility with an unknown branch.

### Waiting, current pending delivery and receipts

`brain._await` now sleeps when there is no request left to answer and starts at most one resident within that invocation. It still takes the brain lock before using the in-process fallback, checks the answer's request identity and protocol, and can answer the waiting request as soon as an old resident releases the lock. I found no new lost-result or duplicate-publication path from this change.

The existing receipt/retry and pending-ownership tests remain green. Independent retention controls keep the same token, held batch and handed-in data after a timeout; a saved `put` survives process death and is applied once on retry (sector 77, no remaining put). Two replacements during delivery give the batch to the final owner, and the response-wait/client-lock and process-death controls pass.

The three real-package tests in `test_rereview6.py` all **ran, none skipped**. The queued and pending upgrade fixtures remain controls, and the actual `442a6311` upgrade preserves its four outstanding calls. Selective release of numeric legacy id `1` works without releasing the unrelated batch. The revised real-package receipt test is now correctly an isolation/delivery test: an old brain cannot produce a receipt for a request it cannot find. The synthetic unnumbered-receipt tests still cover rejection and avoidance of double application.

### Additional correction and test strength

The empty-request busy loop was a real defect, and the sleep/one-start change is narrow. The test checks observable waiting and process-start count. Updating the real-package receipt test was forced by the namespace correction. Bounding its fake-clock loop prevents a defect from hanging that test.

As an independent mutation, I restored the old `req-` prefix in `request_path` in an isolated process, without changing tracked files. All three real-resident tests failed: the old resident took the request, the stop-first path failed to establish the held reservations, and termination during the wait failed to invoke the current handler. An attempted whole-module mutation run was stopped when it did not finish promptly; I do not claim a whole-module mutation count. The three-test result alone establishes detection of the planted regression.

The random walk still models one code version. It supports ownership/accounting regression checks, but does not model historical programs, already-forgotten ledger rows or an operator's migration confirmation. Its passing result cannot refute the disclosed migration limit.

## Retained earlier reproductions

Original scripts were rerun unchanged except for the C-series adaptations already accepted in earlier reviews. Their previous cases remain closed:

| Case | Evidence on this head |
|---|---|
| A1 | Independent execution clock peaks at 29; pending accounting retained. |
| A2 | Last good read retained; defensive fallback issued rather than losing the turn. |
| A3 | Replaced relay emits no stale pending batch; current relay gets its own batch. |
| B1 | Original defect assertion fails because malformed log input now produces fallback actions with zero crashes; valid-action control also passes. |
| B2 | Abandoned batch stays counted; peak 30. Timestamp-skew controls peak at 20 world. |
| B3 | Results applied once: `[1]`. |
| C1, adapted | Outstanding calls do not expire; peaks 30/20. |
| C2, adapted | A relay never given the batch cannot release it; all four original holds remain. |
| C3 and C3b | Repeated tick failure produces fallback actions in resident and restarted execution; accepted state/receipt survive the failed tick. |
| C4 | Falsey/malformed action replies are not accepted as successful actions; fallback remains available. |
| C5, adapted | Replacement receives its own response; queued completion evidence is applied and retained as required. |
| D1 | Operator acknowledgement excludes the active batch; its three reservations remain after retry. |
| D2 | Four unresolved calls remain loose; peaks 30/20. |
| D3 | No-call path returns waits (1 second, then 6), rather than an empty busy loop. |
| E1 | Unchanged defect assertion fails: queued old request leaves four calls outstanding rather than settling them. |
| E2 | Unchanged defect assertion fails: legacy numeric id releases the selected batch only. |
| F1 | Unchanged defect assertion fails: old pending batch is not printed; calls remain within 20 world. |
| Retention/closure controls | Timeout/death preserve results; completion peaks at 30; ordinary replacement gets a new receipt; closed fight produces no action. |

The retained fixtures test what is still present in the old saved state. They cannot establish that a predecessor has never removed a reservation; the new known-limit reproducer tests that separate boundary.

## Verification

At exactly `29797ba0f769152381e71710f812605be9e0bfea`:

| Command/check | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | 354 tests, OK, none skipped |
| `python3 -m player.tests.test_walk 200 300` | 200 walks, 6,948 calls, zero problems |
| `python3 -m unittest player.tests.test_rereview7` | 8 tests, OK |
| Current `test_rereview7.py` against production code at `06358ca5` | 6 failures, 2 passes; no errors |
| Three actual-old-package tests in `test_rereview6.py` | 3 tests, OK, none skipped |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | 46 tests, OK; existing ResourceWarnings |
| `python3 scripts/player_allowlist.py check` | Clean, zero never-list violations |
| `python3 scripts/player_allowlist.py report --check` | Current |
| `python3 scripts/rulings_index.py --check` | 322 rulings, index current |
| `python3 scripts/check_large_files.py` | Clean |
| `python3 scripts/check_no_real_name.py --commits 06358ca5..29797ba0` | Zero hits, files and commit messages |
| `tests/test_planner2.py`, `tests/test_pilot.py`, `tests/test_integration.py`, `tests/test_nearkill.py`, run with Python from `state/player/dauntless/tools` | All exit 0; planner 4,000/4,000 |
| Three retained simulated fights | 14/9/13 turns; peaks 23/27/24; no action delayed by budget |
| `python3 scripts/player_size.py` | 4,017 player lines / 19 files; 6,482 test lines; brain 859, battle 685; 16 functions over 12 branches |
| `git diff --check` | Clean |

I independently checked the namespace history and ran the mutation described above; I did not rerun all 41 author-reported mutations. Simulations and unit tests do not measure live token use or prove live relay behavior.

## Next handoff and review boundary

G1 does not need another redesign. Implement the selected migration admission boundary, document its acknowledgement and quiet-period semantics, and return a frozen head. The next relevant scope should be that boundary, its persistence/retries and old-package upgrade controls, plus current pending/receipt delivery. A general AP1 restart or a pre-acceptance brain split is not warranted by this result.

No existing tracked file changed in the review checkout, and no `fable/*` branch was modified. Temporary scripts, historical-package extractions and test artifacts stayed outside the reviewed source changes; legacy tests' untracked outputs were moved out of the checkout. The only published addition is this report on `chatgpt/review-ai-player-ap1-rereview8`.

**Zero live-game requests, game writes or live credentials used.** No live relay or browser session was exercised.
