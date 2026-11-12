# AP1 independent re-review, Lane A — 442a6311

Repository: `perseverance484/tnr-tools`  
Frozen target: `fable/ai-player-ap1` at **442a63119d2fa3fe033877bedc86f5df8cd9be00**  
Code commit: `2ae876d5`; correction base: `c0006266a128cca68296e4fc77863c8bd62f3096`  
Review date: 2026-11-12  
**Verdict: request changes.**

The six unchanged reproductions now show their specific cases closed. The broader review finds six surviving defects at the new boundaries: expiry of loose reservations, proof of batch ownership, persistence after a crashing tick, false success from malformed action answers, delayed foreign batch delivery, and actions after confirmed fight exit. Each finding below has a runnable offline reproducer and a refutation/control.

I read `AI_PLAYER_AP1_REREVIEW3_HANDOFF.md` first, then `IMPLEMENTATION_HANDOFF.md` section 5. **Full relevant scope was necessary and was repeated**, including the three ledger states, client request/receipt lifecycle, crash fallback, profile/log intake, and the eight additional fixes. The budget and client are still not suitable for a narrow follow-up limited to the original examples.

## Original reproductions, unchanged

The scripts are the exact ones published in [the previous report at c9e7a1e6](https://github.com/perseverance484/tnr-tools/blob/c9e7a1e680d450347638fa9b3e06682c40755f74/docs/reviews/AI_PLAYER_AP1_REREVIEW2_REVIEW.md). I ran the original external files without editing them.

| Reproducer | Disposition at 442a6311 | Observed evidence |
|---|---|---|
| B1: new malformed action ID poisons the battle log | **Closed for that case.** | Actions at T+1, T+12 and T+20; zero crashes. The script exits with `AssertionError` because its assertion expects the old failure, namely no actions. This is evidence of the fix, not a failing implementation test. |
| B2: abandoned call at T+62 and incorrect past transcript timestamps | **Closed for those cases.** | Abandoned-call maximum is **30**; world maximum is **20** with both honest timestamps and a −100-second skew. The broader loose-call guarantee remains open in findings 1 and 2. |
| B3: client dies before saving the pending receipt | **Closed for that case.** | `results applied per attempt [1]`, previously `[1, 1]`. Successful request state and its receipt survive the restart. Crashed requests have the separate persistence failure in finding 3. |
| A1: watchdog ages out an outstanding batch | **Closed.** | Watchdog retains all three outstanding entries; maximum actual calls is **29**, previously 30 at the last correction and 31 before the fix. |
| A2: invalid active fighter / null action coordinate | **Closed.** | Last good active fighter retained, turn not falsely closed; stance still goes, and the null-coordinate case sends last-good `(8, 2)`, version 11. |
| A3: older pending waiter overwrites its replacement | **Closed.** | Old batch seq 2, replacement seq 3; old waiter emits no calls, fresh waiter publishes only the profile batch. |

## Ruling on LOOSE_FOR

**Do not accept the automatic 900-second release as satisfying the settled call caps.** Keep 900 seconds as an alert/escalation threshold if useful, but retain the reservation until completion or effective cancellation is established. A local, persistent operator acknowledgement that the old relay has actually been stopped is sufficient; a connector hook is not the only possible implementation. Count the uncertain calls conservatively until **60 seconds after that trusted completion/stop bound**.

The handoff accurately discloses the risk of a relay calling after 900 seconds, but the current implementation also fails **inside** its proposed bound: a call made one second before expiry still belongs to the next minute, while its reservation disappears at expiry. Finding 1 reproduces **31 total** and **21 world** calls without an old call after the deadline.

Even adding that missing minute would only make an *assumed* 900-second execution bound internally consistent; it would not establish that a suspended relay cannot resume later. An elapsed timer is not cancellation. Accumulated unresolved work can legitimately exhaust capacity and require the operator to confirm a stopped relay. That tradeoff should be visible rather than silently relinquishing the settled cap. This ruling concerns implementation evidence for the existing limit; RUL-2026-11-11-149 through -152 are not reopened.

## Findings

### 1. High — loose-call expiry drops calls still inside the real rolling minute

**Location:** `player/budget.py:82`, `:91`, `:115`; `player/config.py:70` (`LOOSE_FOR`).

A loose reservation expires at `given_up_at + LOOSE_FOR`. `_hist` then discards it, and `_when` allows scheduling on that expiry boundary. This assumes the call ceased to matter at the last instant it could execute, rather than one minute after that instant.

**Reproduction C1:** reserve one world call, give it up, and execute it at `expiry − 1`. At `expiry + 1`, execute all waits from newly paced traffic. Recovery-lane traffic reaches **31 actual / 30 ledger**; world-lane traffic reaches **21 actual / 20 ledger**. The old call is within the proposed 900-second bound. The test records actual call times independently of the budget.

**Refutation:** a control reporting the old call through `Budget.ended` at its real completion retains it for the extra minute and peaks at 30. The original T+62 test also stays at 30. This is specifically the expiry boundary, not bad transcript time or an ignored wait.

**Required correction:** implement the ruling above. If a bounded-execution assumption is ever explicitly adopted, its last possible execution time must still be followed by a complete rolling minute of accounting.

### 2. High — a replacement that never received a batch can settle another relay's calls

**Location:** `player/brain.py:476`, `:487`, `:518`; settlement at `player/budget.py:132`.

`new=False` is written after the request exchange, before pending publication. `_greet` treats that flag as proof that the relay held its token's batch. But during the hold the token still contains the previous sequence number, which may belong to another relay. The eventual `ended` message contains only that sequence number.

**Reproduction C2, using the real client:** A holds batch 1. B replaces A and requests a batch, making A's calls loose. While B is in its hold, C replaces B. B receives STOP and no calls. When B calls again with its original token, `_greet` nevertheless queues completion for **batch 1**. C's next request applies it: A's four loose entries become settled even though **A has never returned**.

**Refutation:** the committed test covers a replacement stopped before it ever asks; that case is correctly protected by `new=True`. This case asks, reaches the hold, and receives no batch. Ordinary repeated replacement/hold tests still stop the older callers, but do not verify the false completion claim.

**Consequence:** the budget now has fabricated evidence of completion; A can still execute after the prematurely settled entries age out. The new loose-call accounting can therefore be bypassed well before its timeout.

**Required correction:** track actual publication ownership separately from handshake/exchange progress. An ended report must identify the exact relay and generation that held the published batch, and the ledger must validate that identity. A bare sequence inherited in a handshake is insufficient.

### 3. High — a crashing fallback brain loses both its failure count and received results

**Location:** `player/brain.py:119–126`, `:347–351`, `:547`.

On the first failing decision `_undo` increments `crashed` and creates a receipt in memory, then returns without saving. `answer` publishes the empty crash response and removes the request, also without saving. When the in-process fallback constructs the next `Brain`, the received state, receipt and failure count are gone. Every attempt can be the first failure again, so `last_resort` never runs.

**Reproduction C3, restart case:** save a normal active fight with a usable inbox; inject a persistent `_absorb` failure; run real `brain.answer` at T+1, +2, +12, +15, +20 and +60, constructing a fresh Brain from the live folder before each request, as `_await` does without a resident brain. Every response contains **no action** and every in-memory failure count is **1**. A separate received profile changes sector 12 to 77 and creates a receipt in memory; after restart sector is **12** and the receipt is absent.

A second test (C3b) runs the actual `next_batch`/`_await` fallback with daemon startup disabled and an already-overdue saved turn. Six requests return no calls, and the saved crash count remains absent.

**Refutation:** keeping the same resident Brain across requests reaches count 2 and emits the saved best line. This is not failure to validate the injected read: `_absorb` is deliberately made to fail regardless of shape to test the new generic crash guarantee. It reproduces the handoff's disclosed unsaved-crash boundary, with the additional consequence that the promised second-failure fallback never arrives. The H3 crashed-request test retains one Brain and misses this boundary.

**Required correction:** durably commit the post-intake state, failure count and crash receipt together before acknowledging/removing the request, or retain and recover the request under an equivalent durable protocol. Logging an error is not persistence of the world model. Do not advance the client past data the next Brain cannot recover.

### 4. High — falsey malformed action answers are treated as successful actions

**Location:** `player/activities/battle.py:159–167`.

The new guard checks `isinstance(r.data or {}, dict)`. Consequently `false`, `0`, `""`, `[]` and `null` become `{}` before validation and are treated as accepted actions. The player then suppresses its missing-read fallback because it believes the turn already landed.

**Reproduction C4:** start the fixture fight, answer both issued actions with each of those JSON values, and provide no later battle read. Each case records **accepted=2, unknown=0** and sends **no action through T+60**. No server acceptance evidence was supplied.

**Refutation:** the truthy malformed string `'x'` follows the intended unknown-answer path and actions are retried at T+12 and T+20. An actual empty object remains the existing successful-response case. The new Swept regression checks only truthy malformed values (`'x'`, `7`, `[1]`, `True`); it therefore does not cover this hole.

**Required correction:** validate the actual decoded value before applying defaults. A non-object response must remain unknown unless a source-supported response contract explicitly establishes success for that value. This is incomplete coverage of the newly claimed fix, not a regression of the original B1 scenario.

### 5. Medium — a late answer can satisfy a different relay's request and discard its completion evidence

**Location:** `player/brain.py:351–352`, `:504–517`, `:539–542`.

Request and batch files are named by sequence alone. The replacement can reuse the sequence while an earlier request is being answered. Deleting an existing leftover file before issuing the request does not prevent the earlier worker from writing its answer afterward. The response contains no relay identity to check, and the old worker unconditionally deletes the request path, which may now contain the replacement's request.

**Reproduction C5:** a real resident process holds the brain lock and pauses just before writing its answer. Terminate the old client waiting for it. A replacement submits a request under the same sequence, including a genuine `ended` report for a still-accounted older batch. Release the worker. The replacement prints the older relay's batch, the persisted receipt names the old relay, and its own request has been deleted without processing. The client clears `ended` as though the brain consumed it. Even on its following request, the genuinely completed older batch's four calls remain loose.

This is a real-process test: normal request/answer code, actual advisory locks and process termination. The injected pause selects the interleaving; no fabricated batch file is used. A guard-mode control change makes the stale decision visible as extra hunt reads, but the finding does **not** rely on forbidding intentional pending-batch transfer: the loss of the replacement's completion evidence is independently observed.

**Refutation:** a normal replacement after response publication receives its own profile-only guard decision and its own receipt. The committed leftover-file test correctly handles a file already present before `_exchange`; it does not cover an old worker writing after deletion.

**Required correction:** identify and verify the request generation, including relay ownership, in request paths, responses and receipts. An old worker must not unlink a newer request. If deliberately transferring an earlier answer, preserve and process the new request's completion/result metadata rather than acknowledging it as consumed.

### 6. Medium — last resort can act on a fight the profile has already confirmed is over

**Location:** `player/activities/battle.py:260–267`, `:274–285`.

The fallback decides that a fight is active from the old battle read's active fighter and positive HP. It ignores `state['left']` and the newer profile's departure from that battle. If closure/archival fails, `_undo` preserves the departure evidence but the last resort acts on the older battle anyway.

**Reproduction C3, closure case:** refuse the first plan and provide a valid **AWAKE** profile. Make `Combat.close_fight` raise an archival error. First request yields no action; the second emits **Defensive Stance for B1**, while `world.status()` is AWAKE.

**Refutation:** without the archival failure, the same inputs close the fight and emit no old-fight action. The H1 end-of-fight fallback test uses HP=0 in a battle read, which is correctly handled. This case uses the other authoritative ending signal, a valid profile. It is not merely the disclosed limitation of waiting for manual archival repair: an extra combat action is actually issued.

**Required correction:** honor confirmed profile departure/new battle identity before choosing any old-fight emergency action. Archival retry must not undo that evidence or make it legal to act on the closed fight.

## Assessment of the eight additional fixes

| Item | Real defect? Narrow fix and preservation assessment |
|---|---|
| Malformed profile money/bank blocks the batch | Yes. The base loses the onward action in the negative control. `_unfit` checks before replacement and retains the good profile; numeric currency strings remain accepted. `_take_in` also isolates world/combat readers. No valid fixture regression found. |
| Wrong-kind battle ID opens an unreadable fight | Yes. The new text-or-null check prevents the reproduced non-text battle ID from entering character/fight state. It is local and preserves ordinary battle/rematch profiles. |
| Spend day derived from bad transcript time | Yes. The old result at time zero assigns spending to 1970; the correction uses the brain's clock for both the spend day and read freshness. Controls with stale/zero timestamps, numeric-string money/bank and a UTC midnight boundary all behave consistently. The boundary control records 40M before midnight, zero current-day spend before the next read, then 1M on the next day's new balance decrease. It attributes changes to observation day; it does not reconstruct actual transaction dates across missing reads. No policy change to the 50M threshold/reserve is implied. |
| Non-object action answer blocks following battle read | Yes for the tested truthy values; per-answer isolation and unknown classification fix those examples. **Incomplete for falsey values: finding 4.** |
| Availability/ranking failure repeats forever | Yes. The old `ValueError('bad state')` escapes rank; current code blocks the failing primary activity for 60 seconds and a fight still runs. The catch is local, and stable ranking/tie behavior is preserved. |
| Failed status write costs the batch | Yes. The old `OSError('disk')` aborts the tick; current code logs the error and preserves action output. This protects a status-file-specific failure, not arbitrary disk failure including the world save. |
| Leftover batch under the next sequence is printed | Yes. Removing a pre-existing file fixes the exact regression test. **Not sufficient for a late old writer: finding 5.** |
| Relay with no batch can report another relay's batch over | Real underlying ownership risk. The fix is correct for a relay replaced before its first request, but **not after exchange and before publication: finding 2**. The negative-control test's failure is absence of any loose entries on the old head; that alone is not proof that the new ownership check covers the hold interleaving. |

Profile validation was pressed beyond the listed bad-value examples: optional missing pools/position/energy/money/bank remain accepted; mandatory health remains numeric; decimal currency strings and ordinary AWAKE/BATTLE profiles remain accepted. Rejecting an entire invalid profile preserves the last usable one and avoids using malformed money for the spending gate. The available evidence supports those type decisions, not universal coverage of every future game response.

The log validation now rejects an unseen row with an object/list/null action before it enters persistent entries, and sanitizes effect text shapes. I checked the **582 rows in 22 saved logs**: the round/fighter/action kinds match the new check and none has an empty action. This is useful compatibility evidence, not a live protocol measurement.

## Regression tests and negative control

At 442a6311: **281 player tests pass**. The exact `test_rereview2.py` was copied outside the checkout, run against detached **c0006266**, and the checkout returned to the frozen target. Result: **23 tests, 17 failures, 5 errors, 1 pass**.

The five errors divide exactly as follows:

- **Missing API/representation, not old behavioral proof:** missing `config.LOOSE_FOR`; missing `Budget.ended`; unexpected `own_clock` argument to old `Budget.settle`.
- **Real old failures:** `OSError('disk')` escaping the status write; `ValueError('bad state')` escaping activity availability/rank.

The lone passing control is the valid-profile test. H1's unseen-row sweep fixes the previous reused-ID blind spot and exercises `brain.answer` at the deadline checkpoints. The G1 tautology has been replaced with a real watchdog assertion; G3 now includes the real expiry/recomputation interleaving. These are meaningful improvements.

Limits remain: H1's healthy resident/repeated-failure test retains one Brain; H3's crashed-request receipt test also retains one Brain; falsey action responses are omitted; the no-batch ownership test stops before exchange; the leftover-file test has no late writer. The HP-zero fallback test's old-head failure is missing proof-read output, not proof that the old implementation emitted an action after fight exit. Test counts should not be substituted for those distinctions.

Earlier review, wiring and live-session regression groups pass in the full suite. Ordinary replacement during response wait/hold, two replacements in succession, and SIGKILL releasing the client lock were rerun. The old superseded waiters emit STOP and only the final owner gets the pending batch.

## Budget/performance checks that held

The serial, ordered-batch path now ignores all transcript times and settles on the trusted hand-in clock. The `brain put` path uses locally stamped results only within admission/now bounds. Missing results in a returned ordered batch are accounted from return time. Outstanding entries survive status queries/restarts; true completion reports preserve the final minute. The new randomized check ran 3,000 serial mixed-lane batches with waits, latencies, status reads and saved-world restarts, within both caps. This does not cover unrequested concurrent account traffic or establish that a real harness runs every batch sequentially.

Using the same independent `Game.made` clock as the prior review:

| Scenario | Completed turns | New calls | Real rolling maximum | Action holds/internal waits | Longest unread |
|---|---:|---:|---:|---|---:|
| Hunt at cap, then 240-second fight | 14 | 78 | 23 | None | 16.4 s |
| Twenty-call burst, then 180-second fight | 9 | 48 | 27 | None | 36.6 s, with finding |
| AI fight, 240 seconds | 13 | 82 | 24 | None | 21.4 s |

The handoff's comparisons are reproduced. These are offline simulations, **not measured corrected-player token consumption or live throughput**. The three token decisions remain open for the director.

## Required checks

| Command/check | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | **281 OK** |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | **46 OK** |
| `python3 scripts/player_allowlist.py check` | Clean, 93 entries, zero never-rule violations |
| `python3 scripts/player_allowlist.py report --check` | Current |
| `python3 scripts/rulings_index.py --check` | Current, 322 rulings |
| `python3 scripts/check_large_files.py` | Exit 0 |
| `python3 scripts/check_no_real_name.py --commits c0006266..442a631` | Zero hits |
| `python3 scripts/player_size.py` | 3,602 code lines / 19 files; 4,341 test lines; battle 650, brain 601; 14 functions over 12 branches |
| `git diff --check` | Clean |
| In `state/player/dauntless/tools`: `tests/test_planner2.py`, `tests/test_pilot.py`, `tests/test_integration.py`, `tests/test_nearkill.py`, each run with `python3` | All exit 0; planner parity 4,000/4,000 |

The sparse checkout includes all correction files, required fixtures and `.claude/agents/tnr-relay.md`. Large-file and real-name scans cover populated tracked files (plus correction commit messages for the latter), not omitted historical artwork/content. The size figures match the handoff; growth/splitting debt remains documented, not separately made a correctness finding.

## Scope statement and next step

No tracked file in the frozen checkout was changed. Test-generated untracked pilot/archive outputs were moved to external scratch. The reviewer adds only this report on a separate `chatgpt/review-*` branch anchored to 442a6311; no `fable/*` branch is modified. **Zero live-game requests, game actions or credential requests were made.**

Fable should address the surviving paths, including the requested LOOSE_FOR ruling, then return a new exact frozen SHA. Repeat the relevant ownership/receipt and crash-persistence scope after those changes. A green suite and closure of the six old scripts are necessary evidence, but do not close the newly reproduced paths.

## Runnable reproducers

Save each block outside the checkout and run from the frozen repository root with `PYTHONPATH=. python3 /absolute/path/to/script.py`. They use test fixtures, temporary live folders and no connector. C5 uses Linux processes and actual advisory locks; its deliberate process termination affects only its own temporary test client. C3 covers both findings 3 and 6. The original unchanged A/B scripts are linked above rather than edited or reissued as new evidence.

## C1 — loose expiry and both caps

```python
from player.tests.support import Rig
from player import calls as K, config as C
for lane,n in (('recovery',15),('world',10)):
 r=Rig();b=r.brain.budget;t=r.t
 b.pace([K.user()],'world');r.t+=1;b.settle()
 expiry=r.t+C.LOOSE_FOR
 made=[expiry-1]  # the old relay executes INSIDE the 900-second bound
 r.t=expiry+1
 for _ in range(n):
  out,_=b.pace([K.user(),K.user()],lane)
  for s in out:
   if 'wait' in s:r.t+=s['wait']
   else:made.append(r.t);r.t+=.01
  r.t+=.01
 print(lane,'old call before expiry:',expiry-made[0], 'max real:',max(sum(t-60<u<=t for u in made) for t in made), 'ledger:',b.used())
```

## C2 — a relay that never received its pending batch

```python
import io,os,json
from unittest.mock import patch
from player import brain,relay,config as C
from player.tests.support import Rig,user
from player.tests.test_relay import token_of
r=Rig();r.world.absorb([user()._replace(at=r.t)]);r.world.save()
path=os.path.join(r.dir,'client.json')
def nxt(token=None,sleep=lambda _:None):
 out=io.StringIO();brain.next_batch(r.dir,token,out,sleep);return out.getvalue().splitlines()
def ledger():return relay.read(os.path.join(r.dir,'world.json'))['budget']['calls']
def loose(token):return [c for c in ledger() if c[2:3]==['loose'] and c[3]==int(token.split('-')[1])]
with patch.dict(os.environ,{'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':os.path.join(r.dir,'missing'),'TNR_PLAYER_LIVE':r.dir,'TNR_PLAYER_FIGHTS':os.path.join(r.dir,'fights')}):
 a=token_of(nxt(token_of(nxt()[0]))[-1])
 b=token_of(nxt()[0]);cs=[]
 def take_over(wait):
  if wait == C.HUNT_WAIT: cs.append(token_of(nxt()[0]))
 print('B waiting:',nxt(b,take_over))
 print('A loose before:',len(loose(a)))
 print('B never got a batch, but returns:',nxt(b))
 print('ended queued:',relay.read(path).get('ended'))
 c=token_of(nxt(cs[-1])[-1]);nxt(c)
 print('A still has not returned; loose after:',len(loose(a)))
```

## C3 — crash persistence and confirmed fight closure

```python
from unittest.mock import patch
from player import brain,relay
from player.tests.support import Rig,start_fight,battle_read,user
from player.tests.test_review import answers,NOT_VALID,acts
from player.tests.test_rereview2 import ask
# The in-process fallback constructs a new Brain for each request.
for restart in (False,True):
 r=Rig();b,_,out=start_fight(r);T=r.t
 # Preserve incoming usable state as an inbox, like an already-saved interrupted battle.
 r.world['battle']['inbox']=dict(b);r.world['battle']['turn']['accepted']=0;r.world.save()
 fight=type(r.brain.reg.activities['battle']);rows=[]
 with patch.object(fight,'_absorb',side_effect=RuntimeError('persistent tick fault')):
  for seq,t in enumerate((1,2,12,15,20,60),100):
   if restart:r.new_brain()
   out=ask(r,seq,at=T+t,relay='offline')
   rows.append((t,acts(out),r.world['battle'].get('crashed')))
 print('new brain per request:',restart,rows)
# A confirmed AWAKE profile arrives, but final archival raises.
r=Rig();b,_,out=start_fight(r);T=r.t
with patch.object(r.combat,'close_fight',side_effect=RuntimeError('archive unavailable')):
 one=ask(r,1,answers(out,NOT_VALID)+[user('AWAKE')],at=T+1,relay='offline')
 two=ask(r,2,at=T+2,relay='offline')
 print('profile:',r.world.status(),'first:',acts(one),'second:',[(s['input']['battleId'],s['input']['actionId']) for s in two['steps'] if s.get('call')=='combat.performAction'])
# A result and the crash receipt exist only in memory; the fallback's next Brain loses both.
r=Rig();r.tick(user(sector=12));r.world.save()
with patch.object(brain.Brain,'_decide',side_effect=RuntimeError('persistent tick fault')):
 ask(r,9,[user(sector=77)],at=r.t+1,relay='offline')
 print('crashed result in memory:',r.world.me['sector'],'receipt:',bool(r.world['relay'].get('answered')))
 r.new_brain()
 print('after fallback restart:',r.world.me['sector'],'receipt:',bool(r.world['relay'].get('answered')))
```

## C3b — actual in-process fallback client

```python
import io,os,time
from unittest.mock import patch
from player import brain,relay
from player.tests.support import Rig,start_fight
from player.tests.test_relay import token_of
r=Rig();r.t=time.time()-30;b,_,out=start_fight(r)
r.world['battle']['inbox']=dict(b);r.world.save()
def nxt(token=None):
 out=io.StringIO();brain.next_batch(r.dir,token,out,lambda _:None);return out.getvalue().splitlines()
env={'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':os.path.join(r.dir,'missing'),'TNR_PLAYER_FIGHTS':os.path.join(r.dir,'fights')}
with patch.dict(os.environ,env),patch.object(type(r.brain.reg.activities['battle']),'_absorb',side_effect=RuntimeError('persistent tick fault')):
 token=token_of(nxt()[0]);seen=[]
 for _ in range(6):
  rows=nxt(token);token=token_of(rows[-1]);seen.append([x for x in rows if '"call"' in x])
 print('real fallback client calls:',seen)
 print('saved crash counter:',relay.read(os.path.join(r.dir,'world.json'))['battle'].get('crashed'))
```

## C4 — falsey action answers

```python
from player.tests.support import Rig,start_fight,res
from player.tests.test_review import acts
for data in (False,0,'',[],None,'x'):
 r=Rig();_,_,out=start_fight(r);T=r.t
 replies=[res('combat.performAction',data,inp=s['input']) for s in out['steps'] if s.get('call')=='combat.performAction']
 rows=[]
 for t in (1,12,15,20,60):
  out=r.tick(*(replies if t==1 else []),dt=T+t-r.t);rows.append((t,acts(out)))
 print(repr(data),'accepted:',r.world['battle']['turn']['accepted'],'unknown:',r.world['battle']['turn']['unknown'],'actions:',rows)
```

## C5 — late foreign answer and lost completion evidence

```python
import io,json,os,time,multiprocessing as mp
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
 path=relay.request_path(r.dir,2)
 wait_for(lambda:os.path.exists(path))
 real=relay.write
 def held(path_,obj):
  if path_==relay.batch_path(r.dir,2):
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
 req=relay.request_path(r.dir,2)
 wait_for(lambda:(relay.read(req) or {}).get('relay')==b.split('-')[0])
 release.set();printed=q.get(timeout=5);new.join(3);worker.join(3)
 print('old relay:',a.split('-')[0], 'new relay:',b.split('-')[0])
 print('printed calls:',[json.loads(s)['call'] for s in printed if s.startswith('{') and 'call' in json.loads(s)])
 print('saved receipt owner:',relay.read(os.path.join(r.dir,'world.json'))['relay']['answered']['relay'])
 print('replacement request remains:',os.path.exists(req))
 print('client ended after publication:',relay.read(os.path.join(r.dir,'client.json'))['ended'])
 nxt(token_of(printed[-1]))
 print('completed holder still loose:',[c for c in relay.read(os.path.join(r.dir,'world.json'))['budget']['calls'] if c[2:3]==['loose'] and c[3]==1])
```

## Controls — completion, normal replacement, normal closure

```python
import io,json,os,time
from unittest.mock import patch
from player import brain,relay,calls as K,config as C
from player.tests.support import Rig,user,start_fight,battle_read
from player.tests.test_review import acts,answers,NOT_VALID
from player.tests.test_rereview2 import ask
# Bound with an actual completion report: completion is held for a further minute.
r=Rig();b=r.brain.budget;t=r.t;r.world['budget']['batch']=7
b.pace([K.user()],'world');b.settle();expiry=t+C.LOOSE_FOR
r.t=expiry-1;b.ended(7,r.t);made=[r.t];r.t=expiry+1
for _ in range(15):
 out,_=b.pace([K.user(),K.user()],'recovery')
 for s in out:
  if 'wait'in s:r.t+=s['wait']
  else:made.append(r.t);r.t+=.01
print('completion report control peak:',max(sum(t-60<u<=t for u in made)for t in made))
# A normal replacement after the first response is fully delivered gets its own decision.
r=Rig();r.world.absorb([user()._replace(at=r.t)]);r.world.save()
def nxt(token=None):
 out=io.StringIO();brain.next_batch(r.dir,token,out,lambda _:None);return out.getvalue().splitlines()
with patch.dict(os.environ,{'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':os.path.join(r.dir,'missing'),'TNR_PLAYER_FIGHTS':os.path.join(r.dir,'fights')}):
 from player.tests.test_relay import token_of
 a=token_of(nxt(token_of(nxt()[0]))[-1])
 relay.write(os.path.join(r.dir,'control.json'),{'version':1,'mode':'guard'})
 b=token_of(nxt()[0]);out=nxt(b)
 print('ordinary replacement:',[json.loads(s)['call']for s in out if s.startswith('{')and'call'in json.loads(s)],'receipt is new:',relay.read(os.path.join(r.dir,'world.json'))['relay']['answered']['relay']==b.split('-')[0])
# An AWAKE profile without the archive failure closes normally, with no old-fight action.
r=Rig();b,_,out=start_fight(r)
out=ask(r,1,answers(out,NOT_VALID)+[user('AWAKE')],at=r.t+1,relay='offline')
print('normal closure actions:',acts(out),'battle:',r.world['battle'])
```
