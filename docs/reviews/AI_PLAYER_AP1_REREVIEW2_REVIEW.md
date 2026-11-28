# AP1 independent re-review, Lane A — c0006266

Repository: `perseverance484/tnr-tools`  
Target: `fable/ai-player-ap1` at **c0006266a128cca68296e4fc77863c8bd62f3096** (frozen)  
Correction code: `4e0461af`; base: `0d10b7c66fd40fc6c3404e030984f1c5cf7ec059`  
Review date: 2026-11-12  
**Verdict: request changes.**

The three specific reproductions reported against 0d10b7c6 are closed. The full relevant review nevertheless found a new persistent battle-log failure, and confirmed two remaining boundaries to the broader budget and client guarantees. These are separated below from the original three cases. No implementation changes are proposed for integration by this review.

I read `AI_PLAYER_AP1_REREVIEW2_HANDOFF.md` first, followed by `IMPLEMENTATION_HANDOFF.md` section 5. A narrow check is insufficient: the correction changes outstanding-call lifetime, client receipt/generation state, and accepted input shapes. I repeated the relevant budget, relay-client and read-intake review, including `calls.py` and the `combat.py` effect change. RUL-2026-11-11-149 through -152 remain settled. The three token decisions remain the director's; this review makes no claim about measured live token consumption.

## Disposition of the previous three findings

These are the **original scripts, unchanged**, not the author's replacements. They are included in Appendix A so the evidence is now available remotely.

| Previous finding | Outcome at c0006266 | Evidence |
|---|---|---|
| 1. Watchdog/status drops outstanding ledger entries during a long batch | **Closed for that reproduced defect.** | The real watchdog retains three outstanding entries. At return, two real calls remain within the minute and the ledger conservatively counts three. Subsequent paced traffic peaks at **30**, previously 31. The broader cap qualifications in finding 2 below remain. |
| 2. Unknown active fighter / null coordinate accepted as usable | **Closed for both reproduced defects.** | The saved active fighter remains ME and the open turn is not falsely closed. The original script observes Defensive Stance at T+15 and T+60; its initial T+1 response is not printed. The null-coordinate case now sends the last good position `(8, 2)`, version 11, rather than null. G2 separately confirms stance at T+1 and End Turn at T+12 when each fallback is refused and the bad read is repeated. |
| 3. Expired pending batch shares its replacement's identity and wins publication | **Closed.** | The real two-thread client computes the old hunt batch under seq 2 and the fresh guard/profile batch under seq 3. The older waiter emits no calls; only the fresh profile batch is published. |

The previously closed immediate-next-fight case remains closed: a third-party fight opens without a potion; the old open turn is recorded as unresolved or acted according to its actual evidence; an older pending result is retained.

## Surviving findings

### 1. High — a new malformed log row permanently poisons the resident battle tick

**Confirmed defect.** Locations at the frozen SHA: `player/calls.py:115`, `player/activities/battle.py:140`, `player/activities/battle.py:410`; recovery interaction at `player/brain.py:78`.

`log_rows` validates the id, fighter and round, but accepts an object or list as `actionId`. `_log` appends that new row to `state['entries']` before the brain takes its rollback snapshot. `_absorb` then builds a set of enemy action IDs and raises `TypeError: unhashable type: 'dict'`. The exception restores a snapshot that already contains the poisonous row. Dropping the inbox after two crashes does not remove it; planning from the last good read hits the same row again.

**Reproduction:** Appendix B1 starts the saved fixture fight, refuses the first plan, and supplies one otherwise aligned log row with a new id and `actionId: {}`. It calls the real `brain.answer`, including its exception handler. At T+1, +2, +12, +15, +20 and +60, the relay receives **no action** and the brain records six crashes. This defeats both the two-crash escape and the never-lose-a-turn fallback.

**Refutation/control:** changing only that value to `'valid-action'` yields actions and zero errors. No malformed battle-state columns, planner exception, live request or simulated rate refusal is involved. A separate direct `Brain.handle` probe confirms the row remains in `entries` after every failure.

**Why the sweep misses it:** `SweptEveryShapeOfARead.play` (`test_rereview.py:498`) starts a fight with the fixture entries already ingested, then mutates those same entries. For the malformed action-column cases the IDs remain known, and `_log` does not replace their action IDs. The test therefore does not exercise insertion of those malformed values. Its passing action assertions do not prove new malformed log rows are safe.

**Correction needed:** validate the log action identifier before appending the row, preserving any legitimate sentinel allowed by the real contract, and ensure rejected intake cannot become durable planning state. Add an unseen-row-id regression that goes through `brain.answer` across the T+12/T+20 deadlines and repeated failures.

### 2. High — the hard call limits still rely on an unproved completion time

**Confirmed remaining defect, not introduced by 4e0461af.** Locations: `player/budget.py:76`, especially `:87–88`, and `:123`; replacement path `player/brain.py:360`.

Retaining `out` entries in `_hist` fixes the watchdog case. However, settlement still treats a given-up batch as complete now and accepts past transcript timestamps without establishing that they bound the real execution time. It then removes the outstanding marker. Two cases from the prior local report remain reproducible:

1. **Abandoned relay continues:** reserve one call, give its batch up at T+1, then let the old relay execute at T+62 while replacement traffic uses the budget. The independent clock counts **31 calls in a rolling minute; the ledger counts 30**. Replacement ownership only stops future `brain next` publication; it does not cancel calls already printed to the old relay. This is the earlier handoff's acknowledged abandoned-relay limit, now experimentally confirmed again.
2. **Wrong but parseable past result timestamps:** five-call world batches, initially slow then fast, with result times 100 seconds behind the actual execution clock produce **24 real world calls in a minute**. The otherwise identical run with correct timestamps stays at **20**. `max(admitted, min(now, answer_time))` merely falls back to an optimistic admission time when the timestamp is too early. `relay.read_batch` passes the transcript result timestamp through to this calculation.

**Runnable reproduction:** Appendix B2. It executes every returned wait and records dispatch times independently of the ledger. The abandoned case uses recovery-lane load to exercise the total-cap scheduler; it is a scheduler test, not a claim that a particular live fight issued that exact series of profile reads.

**Refutation:** the honest-clock control stays at 20. The unchanged watchdog reproducer now stays at 30. Existing independent `Game.made` tests pass, and 3,000 additional serial mixed-lane batches with varied waits/latencies, status reads and saved-world restarts stayed within both caps. Those successful cases establish the ordinary serial/honest-time behavior; they do not fence an old executing relay or make a bad timestamp trustworthy. Missing timestamps conservatively use return time; the issue is a parseable but incorrect past value.

**Correction needed:** retain unresolved work until completion or effective cancellation is established, and use a conservative verified completion bound when a result timestamp cannot be trusted. The module's unconditional “never sooner”/“however slow” claim at `budget.py:20–26` is not supported under these cases. This is an implementation constraint on the already-settled cap, not a request to reopen budget policy.

### 3. Medium — results can still be applied twice if the client dies before its receipt is saved

**Confirmed known limit, not a newly undisclosed regression.** Locations: `player/brain.py:382–391`, with application at `:232`.

The `handed` check fixes a normal repeated `next` and a restart after `pending` has been saved. It is written only **after** the real brain has applied results and returned the next batch. If the client dies before that write, the transcript remains available and the previous client token still has no receipt. Retrying it applies the same results again; the brain has no durable deduplication keyed to the submitted result batch.

**Reproduction:** Appendix B3 uses a real transcript, first-call handshake, client and in-process brain. It injects termination at the `client.json` pending write, after `Brain.handle` has completed. Retrying the same token produces **`results applied per attempt [1, 1]`**. This is a fault-injection cut, not a claim that the real-time duration of the window was measured.

**Refutation/control:** removing just the injected failure gives **`[1]`**, even though the same token is called again. The committed Swept regression kills the client later, during its hold, after the receipt already exists; that scenario correctly gives `[1, 0]`. The advisory lock serializes access but does not make brain application and client receipt atomic. This exactly confirms known limit 5 in the new handoff.

**Consequence:** result application is not universally idempotent. For example, battle `_acted` increments answered/accepted counters (`battle.py:151,164`), and activities emit events on successful results. The reproducer proves duplicate application with a profile result; it does not claim two connector mutations occurred.

**Correction needed:** make processing of a submitted result batch idempotent at the brain's durable request/receipt boundary, so retry can return the prior answer without applying its results again. Simply writing the client marker earlier trades duplication for loss if processing then fails.

## The eight items found while correcting

All eight correspond to real defects in the old implementation. The local changes address their stated examples; their coverage is narrower than “every shape” or crash-safe exactly-once processing.

| Item | Reality, scope and behavior assessment |
|---|---|
| Unasked calls not counted | Real: old head reports zero stray calls; new head counts three and delays an action when they fill the account's remaining room. `Budget.stray` is local and uses a separate lane as specified. Counting at return is conservative for calls already completed. It cannot retroactively prevent a rogue extra call. |
| Scalar fighter/log/ground column | Real old-head exceptions reproduced by the sweep. `columns`, `ground_cols`, and `_tick` reject these non-list containers locally. Aligned fixture columns remain accepted, including reordered fighter columns. No valid fixture regression found. |
| Log row lacks id/fighter/round | Real: the old head ingests the bad rows; the new head drops the read and continues. The check is local, but incomplete for action-ID values: finding 1. Rejecting an entire malformed batch rather than retaining its valid rows is a conservative tradeoff, not separately reported as a defect. |
| Non-list effects/ground or scalar `timeTracker` | Real old-head exceptions; the new guards treat unavailable containers as absent and skip the invalid tracker. This preserves ordinary fixture behavior. It is container validation, not proof that every nested field is semantically valid. |
| Malformed planner action | Real: old code raises or sends malformed coordinates; new code uses a fallback. `_sendable` locally checks the tested action fields and fixes those examples. The tests assert actual fallback actions. |
| One activity's result handler interrupts others | Real: injected failure prevents later handling on the base; current code logs it and battle handling continues. The local per-activity catch is appropriate for that defect. It does not roll back partial mutation by the failing activity or guard the earlier world/combat absorb calls. |
| Crashing world plan stalls player | Real malformed scan reproduction. The current primary activity is blocked for 60 seconds and other work, including a new fight, proceeds. This deliberately changes error behavior; no correct normal-plan behavior was shown to regress. The protection is for primary `_plan`, not every possible rider/availability failure. |
| Same batch's results handed twice | Real on the base; fixed after the client receipt has been stored, including hold interruption and expiry. The fix is local but not crash-safe before that store: finding 3. |

## Regression-test quality and negative control

At c0006266, **257 player tests pass**. I copied the exact new `test_rereview.py` outside the checkout, ran G1–G3 and both Swept classes with the unmodified 0d10b7c6 implementation, and returned the detached checkout to c0006266. Result: **16 tests; 9 assertion failures, 6 errors, 1 pass**. This matches the claimed 15 of 16.

The tests are useful, but the answer to “are they all behavior tests?” is **no**:

- G1's rolling-real-call assertion and status count are useful. `assertTrue(watchdog() or True)` itself is tautological; the later independent cap assertion still detects the defect. Some subsidiary checks inspect ledger representation/timestamps.
- G2 checks outgoing actions, preserved usable state and turn closure. Its good-read case is the single passing base control.
- G3's older-waiter test checks observable publication but sets up the replacement by writing a fabricated `pending.id` directly. The number-retirement test fails on the base first with **`KeyError: 'id'`**, before its sequence/publication assertions. My unchanged two-thread reproducer independently exercises real expiry and recomputation, so closure does not depend on that setup error.
- The Swept tests check actual action output, errors, onward activity and duplicate handling. The three shape-test errors on the base are real old failure paths, not missing-test-API errors. However, the reused-log-ID blind spot described in finding 1 invalidates the broad log-intake assurance.

The previous regression groups (`test_review.py`, `test_wiring.py`, `test_live.py`) all pass within the full suite. I did not infer universal closure solely from their count.

## Other relevant checks and limits

- The client lock blocks replacement during the response exchange. Replacement during the hold, including two successive replacements, leaves only the final relay receiving calls. SIGKILL releases the actual process lock. Killing after pending storage permits a replacement to recover that pending batch. These offline process/thread checks were rerun on this head.
- Publication still writes `pending=None` and advances the token **before** stdout delivery (`brain.py:348–352`). A process/output failure at that seam can lose the printed batch while state says issued; subsequent recovery asks the brain again. Together with finding 3, this is not an end-to-end exactly-once delivery proof. This existing publication-acknowledgement limit is recorded separately rather than claimed fixed by batch IDs.
- The ordinary expired-batch and duplicate-token tests pass. Batch identity and retired sequence numbers fix the reproduced older-waiter race.
- `Game.made` appends times from its own execution clock and returned waits, not from ledger entries. In the same offline steady/burst/AI scenarios used previously, current results remain: 13/9/15 completed turns, 79/48/87 newly made calls, rolling maxima 22/27/24, and no action holds or internal budget waits before actions. Longest unread periods are 13.7/36.6/21.4 seconds. These are simulations, not live performance or token measurements.
- Read validation accepts the logged valid fighters after reordering aligned columns, and preserves last-good-read fallback for the tested malformed required fields. Optional container guards do not establish arbitrary nested-schema correctness.
- No no-potion transition regression was found; old fight logging and its open-turn outcome remain evidence-based. The earlier round-tag restriction in `tokens_summary` remains covered and unchanged by this correction.

## Commands and results

Run from the frozen repository root unless stated otherwise:

| Check | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | **257 OK** |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | **46 OK**; existing ResourceWarnings do not change success |
| `python3 scripts/player_allowlist.py check` | 93 allowlist entries, zero never-rule violations |
| `python3 scripts/player_allowlist.py report --check` | Current |
| `python3 scripts/rulings_index.py --check` | 322 rulings; current |
| `python3 scripts/check_large_files.py` | Exit 0 |
| `python3 scripts/check_no_real_name.py --commits 0d10b7c6..c0006266` | Zero hits, files and the correction's commit messages |
| `python3 scripts/player_size.py` | 3,322 code lines / 19 files; **3,843** test lines; battle 598, brain 473; 12 functions over 12 branches |
| `git diff --check` | Clean |
| In `state/player/dauntless/tools`: `python3 tests/test_planner2.py`, `python3 tests/test_pilot.py`, `python3 tests/test_integration.py`, `python3 tests/test_nearkill.py` | All exit 0; planner parity 4,000/4,000 |

The handoff's test-line figure is 3,840; the tool reports 3,843 at this exact head. This is a measurement note, not a gameplay finding. Complexity remains acknowledged AP6 debt, not reopened policy.

This was a sparse checkout including the relay agent file and the required fixtures. The large-file and real-name scripts inspect populated tracked files; their passing results are **not** claimed as a full scan of omitted historical artwork/content. All files changed by this correction were populated. No live game or real relay/connector session was used.

## Scope discipline and next step

The frozen checkout's tracked files were unchanged by the review. Test-generated untracked pilot/archive files were moved to external scratch. The only repository addition from the reviewer is this report on a `chatgpt/review-*` branch anchored to c0006266; no `fable/*` branch was modified. **Zero live-game requests, gameplay actions or credential requests were made.**

Fable should address the confirmed failure paths and return another exact frozen SHA with its correction handoff. The wider read intake and budget/client boundaries require relevant re-review; a green suite alone does not close these examples.

## Reproducer instructions

All scripts below are offline. Save a block outside the checkout, then run it from the frozen repository root with `PYTHONPATH=. python3 /absolute/path/to/script.py`. The test fixtures and `.claude/agents/tnr-relay.md` must be populated. No connector is invoked. They use temporary live directories and disable daemon startup where the real client is exercised.

## Appendix A1 — unchanged watchdog reproducer

```python
from player.tests.support import Rig
from player import calls as K,relay,config as C
from player.world import Result
r=Rig();T=r.t
r.world['budget']['calls']=[[T-10,'battle'] for _ in range(24)]
steps=[K.act('B','a',0,0,1),K.wait(1.2),K.act('B','b',0,0,2),K.user()]
out,_=r.brain.budget.pace(steps,'battle')
r.world['relay'].update(issued_at=T,expect=relay.seconds(out),stalled=False)
# Execute calls at independent times; pause execution to run the resident watchdog during the last wait.
actual=[];answers=[];now=T;lags=iter([40,.1,.1]);checked=False
for s in out:
 if 'wait' in s:
  wake=now+s['wait'];deadline=T+relay.seconds(out)+C.STALE_OUTBOX+.1
  if now<deadline<wake:
   r.t=deadline;print('watchdog',r.brain.watchdog(),'remaining pending',len([c for c in r.world['budget']['calls'] if len(c)>2]));checked=True
  now=wake
 else:
  actual.append(now);now+=next(lags);answers.append(Result(s['call'],s['input'],{},None,now))
r.t=now;r.brain.budget.settle(answers,[s for s in out if 'call'in s])
print('checked',checked,'actual live',sum(t>now-60 for t in actual),'ledger live',r.brain.budget.used(),'offsets',[round(t-T,1)for t in actual], 'returned',round(now-T,1))

for i in range(15):
 out,_=r.brain.budget.pace([K.user()]*(1 if i==14 else 2),'recovery')
 for s in out:
  if 'wait'in s:r.t+=s['wait']
  else:actual.append(r.t);r.t+=.1
 r.t+=.1
print('actual worst',max(sum(t-60<u<=t for u in actual)for t in actual),'ledger',r.brain.budget.used())
```

## Appendix A2 — unchanged active-ID and coordinate reproducer

```python
from player.tests.support import Rig,start_fight,battle_read
from player.tests.test_review import answers,NOT_VALID,acts
r=Rig();b,_,out=start_fight(r);T=r.t
bad=dict(b,**{'battle.activeUserId':'not-a-fighter'})
out=r.tick(*answers(out,NOT_VALID),battle_read('B1',bad),dt=1)
for elapsed in (12,15,20,60):
 out=r.tick(dt=T+elapsed-r.t)
 print(elapsed,acts(out))
print('stored active',r.world['battle']['battle']['battle.activeUserId'])
print('turn closed',r.world['battle']['turn']['landed'])
# Another malformed value passes validation and is copied into the emergency call.
r=Rig();b,_,out=start_fight(r)
bad=dict(b);bad['battle.usersState.*.longitude']=[6,None]
out=r.tick(*answers(out,NOT_VALID),battle_read('B1',bad))
print('null coordinate action',[s['input'] for s in out['steps'] if s.get('call')=='combat.performAction'])
```

## Appendix A3 — unchanged stale-pending reproducer

```python
import io,os,json,threading
from unittest.mock import patch
from player import brain,relay,calls as K
from player.tests.support import Rig,user
from player.tests.test_relay import token_of
r=Rig();r.world.save();clock=[100.0]; outputs={};ready=[threading.Event(),threading.Event()];release=[threading.Event(),threading.Event()]
def nxt(token=None,sleep=lambda _:None):
 o=io.StringIO();brain.next_batch(r.dir,token,o,sleep);return o.getvalue().splitlines()
with patch.dict(os.environ,{'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':os.path.join(r.dir,'missing'),'TNR_PLAYER_LIVE':r.dir,'TNR_PLAYER_FIGHTS':os.path.join(r.dir,'fights')}):
 t0=token_of(nxt()[0]);t1=token_of(nxt(t0)[-1]);brain.put(r.dir,t1,1,json.dumps(user().data))
 def run(i):
  def sleep(d):ready[i].set();release[i].wait(5)
  outputs[i]=nxt(t1,sleep)
 with patch.object(brain.time,'time',side_effect=lambda:clock[0]):
  a=threading.Thread(target=run,args=(0,));a.start();assert ready[0].wait(3)
  old=relay.read(os.path.join(r.dir,'client.json'))['pending'];clock[0]=old['ready_at']+11
  # A real control change makes the replacement decision observably different.
  relay.write(os.path.join(r.dir,'control.json'),{'version':1,'mode':'guard'})
  b=threading.Thread(target=run,args=(1,));b.start();assert ready[1].wait(3)
  fresh=relay.read(os.path.join(r.dir,'client.json'))['pending']
  release[0].set();a.join(3);release[1].set();b.join(3)
 def calls(lines):return [json.loads(x)['call'] for x in lines if x.startswith('{') and 'call' in json.loads(x)]
 print('old pending',old['seq'],[s['call'] for s in old['steps'] if 'call' in s])
 print('fresh pending',fresh['seq'],[s['call'] for s in fresh['steps'] if 'call' in s])
 print('old emitted',calls(outputs[0]),'fresh emitted',calls(outputs[1]),'fresh reply',outputs[1])
```

## Appendix B1 — persistent malformed log, with valid control

```python
import os
from player import brain, calls as K, relay
from player.tests.support import Rig, start_fight, battle_read, log_read, FOE
from player.tests.test_review import answers, NOT_VALID, acts

def run(action):
    r = Rig()
    b, _, out = start_fight(r)
    T = r.t
    bad = dict(zip(K.ENT, (['new-row'], [b['battle.round']], [FOE], [action], [[]])))
    observed = []
    for seq, elapsed in enumerate((1, 2, 12, 15, 20, 60), 90):
        results = answers(out, NOT_VALID) + [battle_read('B1', b), log_read('B1', bad)] if elapsed == 1 else []
        r.t = T + elapsed
        path = relay.request_path(r.dir, seq)
        relay.write(path, {'seq': seq, 'results': relay.pack(results)})
        brain.answer(r.brain, r.dir, path)
        out = relay.read(relay.batch_path(r.dir, seq))
        observed.append((elapsed, acts(out)))
    print(repr(action), 'actions:', observed, 'crashes:', len(r.events('error')))
    return observed

assert not any(a for _, a in run({}))
assert any(a for _, a in run('valid-action'))
```

## Appendix B2 — abandoned work and timestamp skew, with honest control

```python
from player.tests.support import Rig
from player import calls as K
from player.world import Result

def most(a):return max((sum(t-60<u<=t for u in a) for t in a),default=0)
# A replaced relay continues one outstanding call; replacement sends paced recovery-sized batches.
r=Rig();origin=r.t;a=[];r.brain.budget.pace([K.user()],'world');r.t+=1;r.brain.budget.settle()
r.t=origin+62;a.append(r.t) # old relay finally executes its previously issued call
for _ in range(15):
 out,_=r.brain.budget.pace([K.user(),K.user()],'recovery')
 for s in out:
  if 'wait'in s:r.t+=s['wait']
  else:a.append(r.t);r.t+=.01
 r.t+=.01
print('abandoned call',most(a),'ledger',r.brain.budget.used())
# Wrong but parseable result timestamps. Identical schedule to the original world probe.
for skew in (0,-100):
 r=Rig();origin=r.t;a=[]
 for lag in [8]+[.4]*7:
  steps=[K.user()]*5;out,_=r.brain.budget.pace(steps,'world');results=[]
  for s in out:
   if 'wait'in s:r.t+=s['wait']
   else:a.append(r.t);r.t+=lag;results.append(Result(s['call'],s['input'],{},None,r.t+skew))
  r.brain.budget.settle(results,[s for s in out if 'call'in s]);r.t+=.5
 print('timestamp skew',skew,'most',most(a))
```

## Appendix B3 — client crash before receipt

```python
import io,json,os,time
from unittest.mock import patch
from player import brain,relay
from player.tests.support import Rig,user
from player.tests.test_relay import token_of,transcript,nxt
r=Rig();r.world.save();path=os.path.join(r.dir,'t.jsonl')
def next_(token=None):
 o=io.StringIO();brain.next_batch(r.dir,token,o,lambda _:None);return o.getvalue().splitlines()
with patch.dict(os.environ,{'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':path,'TNR_PLAYER_LIVE':r.dir,'TNR_PLAYER_FIGHTS':os.path.join(r.dir,'fights')}):
 t0=token_of(next_()[0]);transcript(path,[('bash','n0',nxt(t0),time.time())]);t1=token_of(next_(t0)[-1])
 transcript(path,[('bash','n0',nxt(t0),time.time()),('use','u','profile.getUser',{},time.time()),('res','u',json.dumps(user().data),time.time()),('bash','n1',nxt(t1),time.time())])
 real_write=relay.write;real_handle=brain.Brain.handle;seen=[]
 class Killed(Exception):pass
 def write(p,obj):
  if p==os.path.join(r.dir,'client.json') and obj.get('pending'):raise Killed()
  return real_write(p,obj)
 def handle(self,results,*a,**k):seen.append(len(results));return real_handle(self,results,*a,**k)
 with patch.object(brain.Brain,'handle',handle):
  with patch.object(relay,'write',write):
   try:next_(t1)
   except Killed:pass
  next_(t1)
 print('results applied per attempt',seen)
```
