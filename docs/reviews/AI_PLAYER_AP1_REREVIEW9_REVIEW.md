# AP1 independent re-review, Lane A — c412de4d

Repository: `perseverance484/tnr-tools`. Frozen target: `c412de4df43baf4f11fbd817efb0f7ae95c08226`. Code commit: `fbdf40101695b216e023aad99f444c6300e28c89`. Base: `29797ba0f769152381e71710f812605be9e0bfea`. Review date: 2026-11-12.

**Verdict: request changes. One high finding.** The previous report's unchanged reproducer passes its safety cases, but the required migration boundary is not closed: output produced by the immediate predecessor can still bypass the hold. This is an implementation defect in the accepted requirement, not another policy decision.

I read `AI_PLAYER_AP1_REREVIEW9_HANDOFF.md` and Implementation Handoff section 5 first. The scope was the migration admission boundary, persistence/retries, actual predecessor upgrades and current pending/receipt delivery, retaining the earlier controls. No full AP1 redesign or policy re-review was undertaken. RUL-2026-11-11-149 through -152 remain settled. This report makes no AP2 change; the agreed brain split remains after acceptance and before AP2.

## Previous acceptance condition: partly implemented, not closed

The previous report's `known_limit_repro.py` ran **unchanged** on the frozen target:

| Case | Result on c412de4d |
|---|---|
| No acknowledgement | No new calls; simulated peaks 4 total / 4 world, representing the old relay's four calls only |
| Acknowledgement immediately before startup | Update hold is named; first batch waits; peaks 30 / 20 |
| Acknowledgement followed by 60 seconds | Update hold is named; peaks 30 / 20 |

The new thirty-call reservation works when a request goes through the new brain's admission path. It persists across ordinary retries/restarts and is separate from individually named holds. The operator's word settles that reservation with a minute of accounting after it. Those claims survive the tests.

## 1. High — predecessor output bypasses the migration hold (H1)

Locations at the frozen target:

- `player/brain.py:80`: `_take_over` installs the hold when this version's Brain starts.
- `player/brain.py:701`: `_exchange` can instead reuse `_owed` pending output without asking that Brain.
- `player/brain.py:427`: `_answered` replays a protocol-compatible receipt's batch without pacing it through the new hold.
- `player/relay.py:27`: `PROTOCOL` remains 1, shared with `29797ba0`; request names and accepted answers are therefore still compatible with that resident.
- `player/OPERATOR.md:60`, `:67`, `:77`: promises contradicted by these paths.

**Invariant:** after taking over an untrusted ledger, this version must publish no call before confirmation that the old actors cannot execute, and no call during the following minute. The last review explicitly included pending delivery and receipts in that boundary.

I extracted and ran the actual `29797ba0` package. It wrote its own world, client, pending batch and receipt. The only injected failure was process death at the client-file write; no ledger or batch was fabricated. Its process exits before the new version runs.

The current `brain stopped` correctly lists an `update-…` hold. Nevertheless, a **new relay**, created by the current code, inherits the old pending batch and prints four calls without any acknowledgement. Acknowledging immediately before starting the relay still prints those four calls after **8 seconds**, not after a minute. Starting and saving the new Brain first also does not prevent publication: the thirty-call hold is on disk, but `_owed` still bypasses it.

A second crash position, just before the old client writes down the batch, leaves a receipt instead. Retrying through current `brain next` replays that receipt's four calls after 8 seconds, also without acknowledgement. Here the new Brain has been constructed, but `_answered` returns the old batch rather than applying the new admission boundary. Receipt idempotence must preserve the accepted results, not grant an exemption to an old batch's calls.

Finally, a real `29797ba0` resident kept alive under `brain.lock` reads the current `p1-req-…` request and answers it. Current `brain next` prints three calls without acknowledgement; the saved ledger still has no protocol marker. This last case intentionally omits the operator's stop-old-brain step. It refutes the claimed fallback that an old resident yields no answer; the pending cases above already reproduce after that old process has ended, and the `ack` case follows the documented stop/acknowledge/start order.

These paths share one compatibility mistake: a protocol-1 batch was admitted under the preceding rules, which did not require a migration hold, but it remains acceptable under the new rules. The ledger's new marker alone does not invalidate that batch or isolate the request from its old maker. The accepted no-call boundary is therefore not enforced for all publications; forgotten old calls can still overlap newly printed calls. I am not claiming a new measured live rate violation.

### Refutation and positive controls

| Control | Observed result |
|---|---|
| Old pending batch; fresh replacement relay | Four calls without acknowledgement |
| Old receipt; retry after death before client receipt write | Four calls without acknowledgement |
| Old pending batch; `stopped all` before fresh relay | Four calls after 8 seconds; violates the sixty-second tail |
| Old pending batch; current Brain explicitly saves its hold first | Four calls despite the saved update reservation |
| Old pending batch advanced to 11 seconds after its `ready_at` | Batch is retired; no calls; migration path installs its hold |
| Same pending-death/replacement scenario made entirely by c412de4d | Four calls normally; no update hold, as required |
| The original 442a6311 upgrade/queued/pending controls | Held correctly; do not expose the protocol-1 predecessor paths |

The stale-output guard therefore helps only once that particular batch is stale. It does not enforce the acknowledgement or the quiet minute. No old process remains alive in the pending/receipt cases. The current-only control rules out treating every pending delivery as invalid.

**Required correction:** make the changed admission rules a compatibility boundary across requests, client/pending records, answers and receipts, or enforce an equivalent migration gate on every publication path. The existing protocol mechanism is specifically documented as identifying the rules under which a batch was made; `player/relay.py:40` explicitly says to change the number when call-admission rules change. A protocol transition is a plausible narrow correction, but it needs verification across all these paths. Keep accepted results idempotent, retain outstanding holds, and preserve ordinary delivery for records made under the new rules. Do not solve this by silently dropping ownership evidence or by merely telling the operator to wait while code still claims to enforce the boundary.

### Runnable reproducer: pending, receipt and controls

Save this block as `/tmp/ap1-h1.py`; run it from the frozen repository root with `PYTHONPATH=.`. It uses local package extraction and simulated clocks only. Both the target and base commits must be present in Git history.

```sh
PYTHONPATH=. python3 /tmp/ap1-h1.py pending
PYTHONPATH=. python3 /tmp/ap1-h1.py receipt
PYTHONPATH=. python3 /tmp/ap1-h1.py ack
PYTHONPATH=. python3 /tmp/ap1-h1.py installed
PYTHONPATH=. python3 /tmp/ap1-h1.py expired
PYTHONPATH=. python3 /tmp/ap1-h1.py trusted
```

The assertions describe the observed defect/control outcomes; correcting the first four should make those assertions fail. `ack` assumes all old actors really have ended: the old program has exited. Each mode makes a fresh live folder.

```python
import io,json,os,time,sys
from unittest.mock import patch
from player import brain,relay
from player.tests import test_rereview5 as old
from player.tests.test_relay import token_of
mode=sys.argv[1] if len(sys.argv)>1 else 'pending'
old.BEFORE=('c412de4df43baf4f11fbd817efb0f7ae95c08226' if mode=='trusted' else '29797ba0f769152381e71710f812605be9e0bfea')
OLD=r'''
import io,json,os,time
from unittest.mock import patch
from player import brain,relay
from player.tests.support import Rig,user
from player.tests.test_relay import token_of
r=Rig(); r.world.absorb([user()._replace(at=r.t)]);r.world.save()
now=[time.time()];real=brain.Brain;write=relay.write
class Killed(Exception):pass
def saving(path,obj):
 write(path,obj)
 if path==r.dir+'/client.json' and obj.get('pending'):raise Killed
def nxt(token=None):
 out=io.StringIO();brain.next_batch(r.dir,token,out,lambda t:now.__setitem__(0,now[0]+max(t,0)));return out.getvalue().splitlines()
with patch.dict(os.environ,{'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':r.dir+'/none','TNR_PLAYER_FIGHTS':r.dir+'/fights'}),patch.object(time,'time',lambda:now[0]),patch.object(brain,'Brain',lambda live:real(live,clock=lambda:now[0])):
 token=token_of(nxt()[0])
 with patch.object(relay,'write',saving):
  try:nxt(token)
  except Killed:pass
 print(json.dumps({'live':r.dir,'now':now[0]}))
'''
if mode=='receipt':
 OLD=OLD.replace(" write(path,obj)\n if path==r.dir+'/client.json' and obj.get('pending'):raise Killed"," if path==r.dir+'/client.json' and obj.get('pending'):raise Killed\n write(path,obj)")
live,made=old.by_the_version_before(OLD)
now=[made['now']];real=brain.Brain
with patch.dict(os.environ,{'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':live+'/none','TNR_PLAYER_FIGHTS':live+'/fights'}),patch.object(time,'time',lambda:now[0]),patch.object(brain,'Brain',lambda live:real(live,clock=lambda:now[0])):
 def nxt(token=None):
  out=io.StringIO();brain.next_batch(live,token,out,lambda t:now.__setitem__(0,now[0]+max(t,0)));return out.getvalue().splitlines()
 out=io.StringIO();brain.stopped(live,[],out);print('listing before:',out.getvalue().strip())
 pending=relay.read(live+'/client.json').get('pending')
 print('pending wait:',pending['ready_at']-now[0] if pending else None)
 if mode=='expired':now[0]=pending['ready_at']+11
 started=now[0]
 if mode=='ack':brain.stopped(live,['all'],io.StringIO())
 if mode=='installed':real(live,clock=lambda:now[0])._save()
 lines=nxt(relay.read(live+'/client.json')['token'] if mode=='receipt' else token_of(nxt()[0]));calls=[json.loads(s)['call'] for s in lines if s.startswith('{') and 'call' in json.loads(s)]
 print('mode:',mode,'calls:',calls,'elapsed:',now[0]-started)
 print('saved ledger protocol:',relay.read(live+'/world.json')['budget'].get('protocol'))
 assert bool(calls)==(mode!='expired'), 'unexpected control result'
```

### Runnable companion: preceding resident still running

Save as `/tmp/ap1-h1-resident.py` and run `PYTHONPATH=. python3 /tmp/ap1-h1-resident.py`. It terminates its temporary resident in `finally`. Expected on this head: old resident alive, three calls printed, saved ledger protocol `None`.

```python
import io,json,os,subprocess,sys,time
from unittest.mock import patch
from player import brain,relay
from player.tests import test_rereview5 as old
from player.tests.test_rereview7 import OLD_RESIDENT
from player.tests.test_relay import token_of
old.BEFORE='29797ba0f769152381e71710f812605be9e0bfea'
root=old.the_package_before()
p=subprocess.Popen([sys.executable,'-W','ignore','-c',OLD_RESIDENT],cwd=root,env={**os.environ,'PYTHONPATH':root},stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
try:
 made=json.loads(p.stdout.readline());live=made['live']
 with patch.dict(os.environ,{'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':live+'/none','TNR_PLAYER_FIGHTS':live+'/fights'}):
  def nxt(token=None):
   out=io.StringIO();brain.next_batch(live,token,out);return out.getvalue().splitlines()
  lines=nxt(token_of(nxt()[0]));calls=[json.loads(s)['call'] for s in lines if s.startswith('{') and 'call' in json.loads(s)]
  print('old resident alive:',p.poll() is None,'calls without acknowledgement:',calls)
  print('saved ledger protocol:',relay.read(live+'/world.json')['budget'].get('protocol'))
  assert calls
finally:
 p.terminate();p.wait(timeout=5);p.stdout.close();p.stderr.close()
```

## Other correction checks

The thirty-call hold itself is sound on the exercised new-brain path. It blocks world, recovery and battle actions; it is visible in the held inventory/status and stall event; the acknowledgement targets its concrete id; replay does not release unrelated holds. The first-start and ordinary-current-ledger restart controls pass. The changed handling of a non-object world file is a narrow improvement: it now enters the untrusted-ledger path instead of raising while loading that top-level shape. This is not a claim of arbitrary corrupt-file recovery.

The forgotten-ledger fixture agrees with a fresh run of the real `442a6311` package on the relevant state: ledger `{"batch": 4, "calls": []}`, one unreturned holder, client sequence 4, handed sequence 3, no pending batch/calls. I checked the structural and control fields, excluding generated relay ids and timestamps. The real-package test ran without skipping. The queued and pending fixtures and their real-package tests also ran in the full suite.

The edits to earlier tests are justified in separating actual batch holds from the synthetic thirty-call update reservation. The two tests that explicitly settle just the update reservation in the past are component controls for retention of the known old batch; they are not end-to-end evidence of truthful operator acknowledgement. New Q1 tests cover the acknowledgement path separately.

The walk's new legacy-ledger event is useful: it removes the marker and some old holds while old relays continue. Its relaxed per-batch checks are appropriate where the update reservation represents calls whose identities are gone. However, the walk still executes one code version and checks call counts; it does not establish that *no new batch is printed before migration acknowledgement*. It does not reproduce a real protocol-1 predecessor resident or its saved pending/receipt artifacts. The passing suite therefore does not refute H1. Add real immediate-predecessor upgrade tests at these seams, in addition to retaining the older 442a6311 fixtures.

`OPERATOR.md` now describes the intended acknowledgement and sixty-second tail clearly, including selective release, trust in the operator, first-start exception and ordinary restart. Its assertions that an old resident supplies no answer and an earlier pending batch is not used are false for `29797ba0`; the permitted step-3/step-4 swap and the post-word minute are also not enforced for H1. Fix the implementation and keep the page aligned with the verified behavior.

The disclosed limits concerning a genuinely new live folder, deliberately running old code again on a marked ledger, and an operator's false confirmation are not new findings. A hold stopping a fight is the accepted consequence of “no call”; the page should remain in the session instructions. The intended first start and ordinary restart still work. No new token or loadout ruling is needed.

## Regression evidence

### New tests against the previous head

The 15 tests in `player/tests/test_rereview8.py` pass on the target. Against production code at `29797ba0`, with the current test helpers and only `budget.UPDATE = 'update-'` supplied in the test process so imports resolve, they give **9 failures, 4 errors, 2 passes** as stated.

The two passes are first start and ordinary restart. The four errors are:

- `test_a_ledger_says_whose_it_is_from_the_first_thing_saved`: `KeyError: 'protocol'`, because the old ledger has no marker.
- `test_the_hold_outlasts_a_brain_a_retry_and_a_new_relay`, `test_the_word_does_not_count_from_before_the_ledger_was_last_written`, and `test_the_word_is_for_this_takeover_and_no_other`: `ValueError` unpacking an absent update hold.

The latter three are consequences of the old missing behavior, not missing callable names. The suite would be clearer if it asserted a missing hold before unpacking it. The tests still discriminate this correction, but they omit the old protocol-1 artifacts in H1.

### Earlier cases retained

I reran the existing reproducer files, using the already-recorded C adaptations and no new changes to those scripts:

| Cases | Disposition and evidence |
|---|---|
| A1 / A2 / A3 | Closed: execution-clock peak 29; unusable-read fallback; stale old pending batch not printed in the original replacement case. |
| B1 / B2 / B3 | Closed: malformed-log defect assertion refuted by actions with zero crashes; abandoned/skewed-time controls stay at 30/20; results applied once. |
| C1 / C2 | Closed with existing adaptations: no expiry release; an unserved relay cannot release another batch. |
| C3 / C3b / C4 | Closed: repeated tick failure still falls back and saves state; falsey action responses not accepted as success. |
| C5 | Closed with existing adaptation: replacement receives its own response; completion evidence survives. |
| D1 / D2 / D3 | Closed: replay does not widen release; unknown-owner holds retained; no-call branch waits. |
| Retention and closure controls | Same token and handed-in data retained through timeout/death; sector 77 applied once; closed fight has no action. |
| E1 / E2 | Original defect assertions fail as expected: queued old request does not settle outstanding calls; numeric id releases only its named batch. |
| F1 | Original defect assertion fails: legacy pending batch refused, no calls printed; 51 loose rows now include the 30-call update hold. |
| G1 | Unchanged script stops at its old-request-consumed assertion, as before. Adapted observation keeps the four old calls plus the update hold; peaks 4/4 because no new call is sent. |

H1 does not contradict these original-case closures: it uses the immediate protocol-1 predecessor, whereas the retained historical migration reproductions use the earlier incompatible package.

## Verification at the frozen SHA

| Command/check | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | 369 tests, OK, none skipped |
| `python3 -W ignore::ResourceWarning -m unittest -v player.tests.test_rereview8` | 15 tests, OK, including real 442a6311 |
| Current new tests against 29797ba0 production code | 9 failures, 4 errors, 2 passes, as detailed above |
| `python3 -m player.tests.test_walk 200 300` | 200 walks, 5,393 calls, zero problems |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | 46 tests, OK; existing ResourceWarnings |
| `python3 scripts/player_allowlist.py check` and `report --check` | Clean; report current |
| `python3 scripts/rulings_index.py --check` | 322 rulings; index current |
| `python3 scripts/check_large_files.py` | Clean |
| `python3 scripts/check_no_real_name.py --commits 29797ba0..c412de4d` | Zero hits |
| Four legacy pilot test programs, run from `state/player/dauntless/tools` | All exit 0; planner parity 4,000/4,000 |
| `python3 scripts/player_size.py` | 4,083 code lines in 19 files; **6,904** test lines (handoff says 6,902); brain 882; 16 functions over 12 branches |
| `git diff --check` | Clean |

The two-line size discrepancy is informational, not a finding. I did not independently repeat all 50 author-reported mutations or the two fuzz campaigns. The actual uncovered predecessor cases above survive the passing suite. No live token-use or performance claim follows from these checks.

## Next correction boundary

Return one frozen correction covering compatibility and publication at migration: old pending, old receipt, old resident, and current-version positive controls. Keep the acknowledgement id, quiet minute, retained holds and result idempotence tests. A narrow re-check of those paths and the existing migration controls is appropriate if the fix uses the existing protocol boundary; if publication/ownership is redesigned, repeat that relevant scope. This finding does not call for another full AP1 review or moving the brain split ahead of acceptance.

Only this report is published on `chatgpt/review-ai-player-ap1-rereview9`. No existing tracked file in the review checkout changed and no `fable/*` branch was modified. Temporary packages and scripts were outside the checkout; the legacy tests' untracked output was moved out afterward.

**Zero live-game requests, game writes or live credentials used.** All executions used local files, fixtures, fake clocks or simulated relays. No live relay session was exercised.
