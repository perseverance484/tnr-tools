# AP1 independent re-review, Lane A — efa79808

Repository: `perseverance484/tnr-tools`  
Frozen target: `fable/ai-player-ap1` at **efa79808e740811fa562466d332fd01171068cb7**  
Code commit: `7cfe3b35`; correction base: `442a63119d2fa3fe033877bedc86f5df8cd9be00`  
Review date: 2026-11-12  
**Verdict: request changes.**

The original six findings close in their reproduced scenarios, with the required representation changes described below. The wider review finds two remaining unsafe releases of reservations and one empty-batch retry loop. The standard suite and the requested random walk pass; an independently planted defect also passes both, demonstrating a specific coverage gap rather than negating the checks that do hold.

I read `AI_PLAYER_AP1_REREVIEW4_HANDOFF.md` first, followed by `IMPLEMENTATION_HANDOFF.md` section 5. I repeated the ownership, request/receipt, ledger, crash-persistence and battle-close scope. No policy question settled by RUL-2026-11-11-149 through -152 is reopened. No live game or real connector session was used.

## Reproducer disposition and adaptations

Original scripts are in the prior reports: [A1–A3/B1–B3 at c9e7a1e6](https://github.com/perseverance484/tnr-tools/blob/c9e7a1e680d450347638fa9b3e06682c40755f74/docs/reviews/AI_PLAYER_AP1_REREVIEW2_REVIEW.md), and [C1–C5/controls at 592ba138](https://github.com/perseverance484/tnr-tools/blob/592ba138306d247f88c8d279388a4483f03f4018/docs/reviews/AI_PLAYER_AP1_REREVIEW3_REVIEW.md). The original files were run unchanged first; adapted copies were kept outside the checkout.

| Script | Unchanged run | Adapted run / disposition |
|---|---|---|
| C1 | `AttributeError: config.LOOSE_FOR` | With `LOOSE_ALERT` substituted: **30 total / 20 world**, previously 31/21. **Closed for the old expiry case.** The constant now only chooses the probe's elapsed time; it does not release anything. |
| C2 | Shows `ended queued: []`, but incorrectly counts zero loose entries both before and after because it compares the old numeric field | With `c[5] == token`: **4 before / 4 after**; the relay that never received a batch releases none. **Closed.** |
| C3 | Runs unchanged | Restarted and resident cases agree: saved line at T+2/T+20; received sector 77 and receipt survive restart. Closure case sends no old-fight action. **Findings 3 and 6 closed in these cases.** |
| C3b | Runs unchanged | Actual in-process client sends the saved line on the second request, rather than six empty batches. **Closed.** |
| C4 | Runs unchanged | False, 0, empty string, empty list and null all leave accepted=0, with retries at T+12/T+20. **Closed.** |
| C5 | Old filename rendezvous times out; parent asserts waiting for the worker, which also reports `TimeoutError` | With request-id-aware lookup and answer matching: only the replacement's profile batch is printed, receipt names it, its request is answered and completion evidence clears the holder's reservations. **Closed.** |
| Controls | Stops at missing `LOOSE_FOR` | Renamed time constant: peak 30; normal replacement has its own profile/receipt; normal closure has no action and no remaining fight. |
| A1 | Runs unchanged | Three unresolved entries retained through watchdog; peak **29** actual calls. **Closed.** |
| A2 | Runs unchanged | Last good active fighter and position preserved; turn not falsely closed; fallback actions still go. **Closed.** |
| A3 | Runs unchanged | Old seq 2 emits no calls; fresh seq 3 emits the profile batch. **Closed.** |
| B1 | Old failure assertion now raises | Malformed new log row yields actions at T+1/T+12/T+20 and zero crashes. The assertion expecting no actions is obsolete. **Closed.** |
| B2 | Runs unchanged | Abandoned-call case peaks at 30; honest and −100-second transcript clocks both peak at 20 world calls. **Closed for those cases.** |
| B3 | Runs unchanged | Results applied once: `[1]`. **Closed.** |

**Are the edits the least forced?** C1/controls require only the constant rename; C2 requires only the ownership-field replacement. C5 necessarily needs dynamic discovery of the request-id filename at both rendezvous points and an answer-path prefix match. The glob must be reevaluated while waiting, since the replacement's file may not exist at the first lookup. This preserves the original process interleaving and original behavior checks.

Dropping C5's final numeric `c[3] == 1` filter, as proposed, broadens it to all loose batches; it is not the smallest semantic edit. Replacing it with `c[5] == holder` keeps the original target. I ran **both** forms: both report no remaining loose holder calls and the same correct replacement output. The broader zero-loose check does not hide the old failure in this fixture. No production code was changed to make a reproducer pass.

## Surviving findings

### 1. High — replaying `stopped all` can release a relay excluded from the operator's statement

**Locations:** `player/brain.py:669`, `:129–138`, `:388–390`; `player/budget.py:160`.

`stopped all` records `['*', time, ..., 'stopped']`, rather than the set of batches covered by the statement. `evidence` says applying evidence twice changes nothing, but a wildcard is evaluated against the *current* loose set each time. That set can grow between first application and replay from a receipt.

**Reproducer D1:** R has been replaced and stopped; A is the active relay and still holds its batch. The operator truthfully issues `stopped all`: output lists R and **excludes A**. B then replaces A. B's first request applies the wildcard to R and classifies A's batch as loose. Kill the client immediately before its pending answer is stored. On B's retry, the request is answered from its receipt, but the old wildcard evidence is applied again. **A's three loose reservations become zero**, although A never returned and was never confirmed stopped.

**Refutation:** at the first application A remains correctly held. Replacing only `stopped all` with `stopped R_TOKEN` leaves A's three reservations intact after the identical crash/retry. The operator made no false assertion and no relay violated the ordered-batch contract. This is not the disclosed trust limitation of an operator claiming that a live relay is dead.

**Consequence:** after the prematurely settled minute elapses, A can execute calls no longer reserved by the ledger. The implementation violates both “all never includes the running relay” and “evidence is replay-safe.”

**Required correction:** bind an operator statement to an immutable set of affected batch identities, including any explicitly supported orphan reservations, and persist that scope. Replaying evidence must never expand its scope to batches replaced later. Retain the 60-second accounting tail for each genuinely covered batch.

### 2. High — missing/legacy ownership is treated as proof that a printed batch was never printed

**Locations:** `player/brain.py:494–495`, `:123–127`.

`_who` discards absent or old-shape ownership information. `_ledger` then classifies an outstanding batch missing from both `held` and `gone` as never printed and settles it now. Missing ownership evidence does not establish non-publication. A live relay can still have those printed calls.

**Reproducer D2:** use the real current client to publish four calls to A, remove only `held` to reproduce the absent field in the preceding client format, and start replacement B. A has not returned. Nevertheless its calls become settled, with **zero loose reservations**. After 62 seconds, let A execute those calls and run all waits from newly paced traffic: **34 actual total calls** or **24 actual world calls** in a rolling minute.

I also verified a genuine upgrade, without manufacturing a client record: an isolated copy of the **442a6311 player package** created `client.json` and `world.json` through its real `next_batch`. The new target resumed that same temporary live directory with a replacement. The old relay's **four calls became settled, zero loose**, and no ended/operator evidence existed. D2 is the smaller single-head reproduction of the same inference failure.

**Refutation:** retaining the correct `held` field in the otherwise identical D2 run leaves four loose reservations and keeps the peaks at **30 total / 20 world**. The existing malformed-client test has the original current relay return with its token, which really does establish completion; it does not test replacement while the original relay remains active. This finding is about an old-format or missing record, not a requirement to defend against an attacker forging arbitrary valid local files.

**Required correction:** distinguish “known never published” from “ownership unknown.” Migrate recognized prior state conservatively, or retain uncertain outstanding reservations and require completion/confirmed-stop evidence before releasing them. If upgrade with outstanding work is unsupported, fail closed with a clear operator recovery path rather than silently treating that work as completed.

### 3. Medium — the last-resort path spins empty batches when held calls consume the whole budget

**Location:** `player/brain.py:181–185`; compare the nonempty-plan/no-admitted-call backoff in `_decide` at `:243–247`.

The normal decision path adds `RATE_BACKOFF` when budget pacing admits no call. `_last_resort` has no equivalent guard: it passes hold 0 into `_lead`, then publishes that empty batch.

**Reproducer D3:** begin a valid fight; account for 30 calls held for a replaced relay; make battle availability raise on every tick. The first crash response waits one second. Requests 2–5 then each return **zero calls and hold 0.0**. A relay following its instructions immediately runs `brain next` again, repeatedly generating errors, stall events, model turns and requests without game progress.

**Refutation:** without the injected battle failure, the same full ledger returns zero calls with a **6-second hold on every tick**. The same calls remain reserved in both runs. This is the interaction of the generic crash fallback and full held capacity, not a failure to respect the call cap or a demand to act despite exhausted capacity.

**Required correction:** apply the no-admitted-call backoff to every output path, including last resort. Keep the visible stall; do not replace a budget block with an unbounded immediate retry loop. The handoff explicitly promises a wait rather than an immediate empty batch in this situation.

## Ruling implementation and the operator command

The old time-based release is gone. `LOOSE_ALERT` raises a stall; it does not expire calls. Ordinary exact-token return and `stopped TOKEN` release only the intended reservations and retain the final 60 seconds. A minute filled with held calls admits no action, recovery or world call. Held batches are visible in `status.json` with relay/call-count/since, in the initial finding, and in the later stall. These parts of the ruling are implemented and tested.

The ruling is **not yet fully satisfied** because findings 1 and 2 allow settlement without the required evidence. Finding 3 breaks the promised behavior while waiting for such evidence.

**Trusting `brain stopped` is acceptable** as the one explicit operator attestation, as ruled in the previous review. The operator must first establish that the specified relay cannot execute further calls. Its current valid-state visibility is adequate: command output enumerates affected tokens, evidence is durably queued in `client.json`, and the brain records a `setting_changed` event when it applies the release. Listing with no tokens is read-only on the unmodified target; I verified four holds remain four. A current active token is not eligible for an ordinary specific-token acknowledgement.

This acceptance of the trust boundary does not authorize the wildcard to cover future relays or missing metadata to count as a stop. The next live-session brief must include the command, when it is safe to use, the 60-second tail, and what held capacity looks like. The handoff explicitly says that brief update is still pending; no live run was performed or approved by this review.

## The three items found while correcting

| Item | Assessment |
|---|---|
| `brain put` results deleted before the brain answered | Real defect; retaining the current token's put files through collection and deleting via `_taken` after the client records an answer is a narrow correction. An independent interrupted-client probe retained the put file and later applied sector 77 exactly through recovery, then removed the file. |
| Timeout acknowledges fabricated empty batch and loses evidence | Real defect; returning the same next token without moving `held`/`handed` or clearing queued evidence is appropriate. With `_await` returning no answer, the independent control preserves the token, held ownership and put result. A later retry applies it. It does not pretend a timeout was an acknowledgement. |
| Old/edited client shape can imply ownership | The concern is real; rejecting malformed ownership *as positive evidence* is reasonable. **The fix is incomplete:** discarding it must not become positive evidence of non-publication (finding 2). The broader claim of safe old-format recovery is not supported. |

No regression of valid typed profiles, falsey-answer rejection, saved crash counters or ordinary archival-failure closure was found in the requested reproductions. `_close` now records an unarchived sidecar/error and closes despite a books failure; last resort respects confirmed profile departure. The earlier no-old-fight-action case remains fixed.

## Assessment of the seven walk checks

The walk is useful: it drives real client decisions, executes returned waits, keeps an independent call clock and tests several interruption points. Its successful run is meaningful evidence for the scenarios it generates. The seven checks are not a complete protocol model:

| Check | What it establishes, and its limit |
|---|---|
| `cap` | Independent execution times respect the world cap. All generated calls are world-lane calls, so it does not exercise the total-cap boundary with battle/recovery traffic. |
| `ledger` | The saved ledger's aggregate count is no smaller than recent actual calls. Surplus reservations can mask a missing individual call; this alone is not a per-call accounting proof. |
| `evidence` | A generated batch remains reserved while its modeled relay has not completed/stopped. The model marks completion before calling `next`, so this is narrower than proving what evidence the brain durably received at every crash seam. |
| `heard` | Specific completion evidence that the walk tracks is not silently lost once handed in. The generator uses `stopped TOKEN`, not `stopped all`, and does not model wildcard scope/replay (finding 1). |
| `real` | Loose reservations correspond to a batch printed **or marked as printed** in the model. The latter deliberately includes the state-write/stdout seam, where no delivery may have occurred; this is the conservative reservation behavior the handoff documents. |
| `once` | Nonempty result batches with a `held` identity reach `Brain.handle` no more than once. It does not establish delivery of every result, semantic correctness/freshness of results, or a universal at-least-once property. |
| `alone` | A batch ID is not attributed to two relay names. It does not forbid repeated publication of the same batch to the same relay. |

Not modeled: battle turns and fallback/closure, mixed lanes, transcript collection and timestamps, `stopped all`, listing-only operator calls, legacy/malformed client migration, arbitrary world-save failures, real worker scheduling or lock contention, and the late-writer/timeout paths in their full process form. Its deaths are injected exceptions in one process and most responses use the put path with fixed synthetic data. The separate process reproductions remain necessary.

### Independent planted defect that both test layers miss

I changed only the in-memory implementation of `brain.stopped` in a separate Python process: its two `all` conditions were widened to include **no tokens**. This makes the advertised listing-only command queue a wildcard release while its output still looks like a listing.

The mutation is a real defect: issuing `brain stopped` with no token changed an old relay's reservations from **4 to 0** after the next request. The unmodified target keeps **4 to 4**.

Results with that mutation active:

- **305 player tests: OK.**
- **200 walks × 300 steps: 11,212 calls, zero reported problems.**

The mutation script is included below. No repository source file was edited; the mutation ceased with its process. This is **not a fourth product finding**—the unmodified listing command behaves correctly. It proves a missing test of the read-only operator path and shows why the author's fourteen detected mutations cannot establish coverage of every ownership/ledger defect. I did not independently rerun all fourteen of the author's mutations; I independently reproduced this additional survivor instead.

## Negative control and required verification

The exact new `test_rereview3.py` was run against the isolated, unmodified player package from **442a6311**, with the required shared fixtures. Result: **23 tests; 13 failures, 6 errors, 4 passes**, as claimed.

All six errors are missing API/fields, not direct proof of old behavior:

- `holder` argument to `Budget.settle`: **two** errors.
- Missing `brain.stopped`: **one**.
- Missing `held`: **two**.
- Missing request `id`: **one**.

The four passes are the ordinary object-action response and in-fight-last-resort controls, plus the never-printed batch and abandoned-request cases the handoff identifies. The late-writer and confirmed-profile-exit tests fail on their behavioral outputs on the base. The new suites improve the earlier coverage, while the gaps above remain.

| Check at frozen target | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | **305 OK** |
| `python3 -m player.tests.test_walk 200 300` | **11,212 calls; 0 walks with a problem** |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | **46 OK** |
| `python3 scripts/player_allowlist.py check` | Clean, 93 entries, zero never-rule violations |
| `python3 scripts/player_allowlist.py report --check` | Current |
| `python3 scripts/rulings_index.py --check` | Current, 322 rulings |
| `python3 scripts/check_large_files.py` | Exit 0 |
| `python3 scripts/check_no_real_name.py --commits 442a631..efa7980` | Zero hits |
| `python3 scripts/player_size.py` | 3,815 code lines / 19 files; 5,096 test lines; brain 724, battle 685; 15 functions over 12 branches |
| `git diff --check` | Clean |
| In `state/player/dauntless/tools`: `tests/test_planner2.py`, `tests/test_pilot.py`, `tests/test_integration.py`, `tests/test_nearkill.py`, each with `python3` | All exit 0; planner parity 4,000/4,000 |

The same independent steady/burst/AI simulations reproduce **14/9/13 turns**, **23/27/24** maximum real calls per minute, and no action holds or internal budget waits before actions. New-call counts are 78/48/82 and longest unread intervals 16.4/36.6/21.4 seconds. These are offline measurements, not live token or throughput evidence. The three director token decisions remain open.

This was a sparse checkout containing all correction files, necessary fixtures and `.claude/agents/tnr-relay.md`. Large-file/real-name checks inspect populated tracked files (and the correction commit messages), not omitted historical artwork/content. The review does not claim a new full-tree scan of those omitted files.

## Split timing and next step

**Split `brain.py` after correctness acceptance, before AP2, as a separate behavior-preserving change.** Fix the three surviving paths and add their independent regression cases first. Mixing the extraction with these ownership corrections would make their next review harder to attribute. The client/brain boundary is now clear enough to extract; it should carry explicit ownership/evidence invariants and the same tests rather than merely moving complexity out of the size count. The split itself still needs a focused move/diff review and the relevant suite/walk checks.

Return a new exact frozen SHA for the corrections. Repeat the evidence/retry and migration scope; a narrow run of the old C scripts alone is insufficient.

The frozen checkout's tracked files were not modified. The isolated base package, adapted scripts and mutation process were external scratch; test-generated untracked pilot/archive files were moved there as well. The reviewer adds **only this report** on a `chatgpt/review-*` branch anchored to efa79808. No `fable/*` branch changed. **Zero live-game requests, game actions or credential requests were made.**

## Reproducer instructions

Save the blocks outside the checkout and run from the frozen repository root with `PYTHONPATH=. python3 /absolute/path/to/script.py`. All live directories are temporary test folders. No connector is invoked. D2 deliberately removes a field in its temporary client file to isolate the legacy-format inference; it does not edit repository or actual session state. The mutation experiment changes only a Python function in its own process.

## D1 — wildcard completion evidence replay

```python
import io,os,json
from unittest.mock import patch
from player import brain,relay
from player.tests.support import Rig,user
from player.tests.test_relay import token_of
r=Rig();r.world.absorb([user()._replace(at=r.t)]);r.world.save();client=os.path.join(r.dir,'client.json')
def nxt(token=None):
 out=io.StringIO();brain.next_batch(r.dir,token,out,lambda _:None);return out.getvalue().splitlines()
def new():return token_of(nxt(token_of(nxt()[0]))[-1])
def loose(token):
 return [c for c in relay.read(os.path.join(r.dir,'world.json'))['budget']['calls'] if c[2:3]==['loose'] and c[5]==token]
class Killed(Exception):pass
with patch.dict(os.environ,{'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':os.path.join(r.dir,'missing'),'TNR_PLAYER_FIGHTS':os.path.join(r.dir,'fights')}):
 retired=new();active=new()  # retired has been stopped; active still holds its printed calls
 out=io.StringIO();brain.stopped(r.dir,['all'],out)
 print('operator acknowledgement:',out.getvalue().strip(),'active excluded:',active not in json.loads(out.getvalue())['stopped'])
 b=token_of(nxt()[0])  # active is replaced AFTER the operator's statement, and can still execute
 real=relay.write
 def killed(path,obj):
  if path==client and obj.get('pending'):raise Killed()
  return real(path,obj)
 with patch.object(relay,'write',killed):
  try:nxt(b)
  except Killed:pass
 print('active reservations after first request:',len(loose(active)))
 nxt(b)  # same result request; its receipt is used, and the wildcard evidence is replayed
 print('active reservations after retry:',len(loose(active)))
 print('active never returned or was confirmed stopped')
```

## D2 — missing ownership and actual call caps

```python
import io,os,time,copy
from unittest.mock import patch
from player import brain,relay,calls as K
from player.tests.support import Rig,user
from player.tests.test_relay import token_of
r=Rig();r.world.absorb([user()._replace(at=r.t)]);r.world.save();client=os.path.join(r.dir,'client.json')
def nxt(token=None):
 out=io.StringIO();brain.next_batch(r.dir,token,out,lambda _:None);return out.getvalue().splitlines()
with patch.dict(os.environ,{'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':os.path.join(r.dir,'missing'),'TNR_PLAYER_FIGHTS':os.path.join(r.dir,'fights')}):
 a=token_of(nxt(token_of(nxt()[0]))[-1]);n=len(relay.read(client)['calls'])
 state=relay.read(client);state.pop('held');relay.write(client,state)  # field absent in the previous client format
 b=token_of(nxt()[0]);nxt(b)
 saved=relay.read(os.path.join(r.dir,'world.json'))
 print('A has not returned; its calls:',n,'loose:',sum(c[2:3]==['loose']for c in saved['budget']['calls']))
 # Finish the replacement's calls now. A still holds its original printed batch.
 r.new_brain();r.t=time.time()+30;r.brain.budget.settle(asked=());settled=copy.deepcopy(r.world.d);finished=r.t
 for lane,batches in (('recovery',15),('world',10)):
  r.world.d=copy.deepcopy(settled);r.t=finished+62
  made=[r.t]*n  # the old A executes its calls after their premature settlement has expired
  for _ in range(batches):
   out,_=r.brain.budget.pace([K.user(),K.user()],lane)
   for s in out:
    if 'wait' in s:r.t+=s['wait']
    else:made.append(r.t);r.t+=.01
  print(lane,'maximum real calls:',max(sum(t-60<u<=t for u in made)for t in made))
```

## D3 — empty crash fallback with a full held budget

```python
from unittest.mock import patch
from player.tests.support import Rig,start_fight,battle_read
from player.tests.test_rereview2 import ask
r=Rig();b,_,out=start_fight(r);T=r.t
r.world['budget']['calls']=[[r.t,'battle','loose','old-request',r.t,'old-relay-1'] for _ in range(30)]
r.world['battle']['inbox']=dict(b)
fight=type(r.brain.reg.activities['battle'])
with patch.object(fight,'available',side_effect=RuntimeError('persistent tick fault')):
 for seq in range(1,6):
  out=ask(r,seq,at=T+seq,relay='offline')
  print(seq,'calls',r.calls(out),'hold',out['hold'])
```

## Independent mutation experiment — listing becomes release

```python
import inspect,unittest,io
from player import brain,relay
from player.tests.test_walk import Walk
from player.tests.test_rereview3 import Client
src=inspect.getsource(brain.stopped)
src=src.replace('if said or "all" in tokens:', 'if said or "all" in tokens or not tokens:')
src=src.replace('if "all" in tokens else', 'if "all" in tokens or not tokens else')
exec(compile(src,'<review-only in-memory mutation>','exec'),brain.__dict__)
# Prove this planted defect has a real effect: listing queues a wildcard release.
c=Client();c.setUp()
try:
 old=c.new_relay_with_a_batch();current=c.new_relay_with_a_batch()
 before=len(c.loose(old));out=io.StringIO();brain.stopped(c.rig.dir,[],out)
 c.next(current)
 print('MUTANT no-argument listing releases held calls:',before,'->',len(c.loose(old)),flush=True)
finally:c.doCleanups()
suite=unittest.defaultTestLoader.discover('player/tests',top_level_dir='.')
result=unittest.TextTestRunner(verbosity=0).run(suite)
print('MUTANT suite:',result.testsRun,'success:',result.wasSuccessful(),flush=True)
problems=[];made=0
for seed in range(200):
 w=Walk(seed);found=w.run(300);made+=len(w.made)
 if found:problems.append((seed,found))
print('MUTANT walk:',200,'walks,',made,'calls, problems:',problems[:3],flush=True)
raise SystemExit(not result.wasSuccessful() or bool(problems))
```

## Retention controls — timeout and put-result interruption

```python
import io,os,json,glob
from unittest.mock import patch
from player import brain,relay
from player.tests.support import Rig,user
from player.tests.test_relay import token_of
r=Rig();r.world.save();client=os.path.join(r.dir,'client.json')
def nxt(token=None):
 out=io.StringIO();brain.next_batch(r.dir,token,out,lambda _:None);return out.getvalue().splitlines()
with patch.dict(os.environ,{'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':os.path.join(r.dir,'missing'),'TNR_PLAYER_FIGHTS':os.path.join(r.dir,'fights')}):
 token=token_of(nxt(token_of(nxt()[0]))[-1]);brain.put(r.dir,token,1,json.dumps(user(sector=77).data))
 before=relay.read(client)
 with patch.object(brain,'_await',return_value=None):out=nxt(token)
 after=relay.read(client)
 print('timeout same token:',token_of(out[-1])==token,'held unchanged:',before['held']==after['held'],'handed unchanged:',before.get('handed')==after.get('handed'),'puts retained:',len(glob.glob(os.path.join(r.dir,'inbox','put-*'))))
 with patch.object(brain,'_await',side_effect=InterruptedError('client dies')):
  try:nxt(token)
  except InterruptedError:pass
 print('death puts retained:',len(glob.glob(os.path.join(r.dir,'inbox','put-*'))))
 nxt(token)
 print('after retry sector:',relay.read(os.path.join(r.dir,'world.json'))['character']['sector'],'puts remaining:',len(glob.glob(os.path.join(r.dir,'inbox','put-*'))))
```

## Adapted C5 — minimum ownership-preserving filter

```python
import io,json,os,time,multiprocessing as mp,glob
from unittest.mock import patch
from player import brain,relay
from player.tests.support import Rig,user
from player.tests.test_relay import token_of
r=Rig();r.world.absorb([user()._replace(at=r.t)]);r.world.save()
ready,release=mp.Event(),mp.Event();q=mp.Queue()
def nxt(token=None):
 out=io.StringIO();brain.next_batch(r.dir,token,out,lambda _:None);return out.getvalue().splitlines()
def wait_for(fn):
 end=time.monotonic()+4
 while not fn():
  if time.monotonic()>end:raise TimeoutError('test rendezvous')
  time.sleep(.01)
def resident():
 lock=brain._lock(r.dir);assert lock
 pattern=relay.request_path(r.dir,2)[:-5]+'*.json'
 wait_for(lambda:glob.glob(pattern))
 path=glob.glob(pattern)[0]
 real=relay.write
 def held(path_,obj):
  if path_.startswith(relay.batch_path(r.dir,2)[:-5]):
   ready.set();assert release.wait(5)
  return real(path_,obj)
 with patch.object(relay,'write',held):brain.answer(brain.Brain(r.dir),r.dir,path)
 lock.close()
def client(token):q.put(nxt(token))
env={'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':os.path.join(r.dir,'missing'),'TNR_PLAYER_LIVE':r.dir,'TNR_PLAYER_FIGHTS':os.path.join(r.dir,'fights')}
with patch.dict(os.environ,env):
 holder=token_of(nxt(token_of(nxt()[0]))[-1])
 a=token_of(nxt()[0]);worker=mp.Process(target=resident);worker.start()
 old=mp.Process(target=client,args=(a,));old.start();assert ready.wait(4)
 old.terminate();old.join(3)
 b=token_of(nxt()[0])
 assert nxt(holder)==[brain.SUPERSEDED]
 print('genuine completed batch queued:',relay.read(os.path.join(r.dir,'client.json'))['ended'])
 relay.write(os.path.join(r.dir,'control.json'),{'version':1,'mode':'guard'})
 new=mp.Process(target=client,args=(b,));new.start()
 pattern=relay.request_path(r.dir,2)[:-5]+'*.json'
 wait_for(lambda:any((relay.read(p) or {}).get('relay')==b.split('-')[0] for p in glob.glob(pattern)))
 req=next(p for p in glob.glob(pattern) if (relay.read(p) or {}).get('relay')==b.split('-')[0])
 release.set();printed=q.get(timeout=5);new.join(3);worker.join(3)
 print('old relay:',a.split('-')[0], 'new relay:',b.split('-')[0])
 print('printed calls:',[json.loads(s)['call'] for s in printed if s.startswith('{') and 'call' in json.loads(s)])
 print('saved receipt owner:',relay.read(os.path.join(r.dir,'world.json'))['relay']['answered']['relay'])
 print('replacement request remains:',os.path.exists(req))
 print('client ended after publication:',relay.read(os.path.join(r.dir,'client.json'))['ended'])
 nxt(token_of(printed[-1]))
 print('completed holder still loose:',[c for c in relay.read(os.path.join(r.dir,'world.json'))['budget']['calls'] if c[2:3]==['loose'] and c[5]==holder])
```
