# AP1 independent re-review 6 — Lane A

**Verdict: request changes. E1 and E2 are closed.** One additional pending-batch migration defect survives refutation: a real `442a6311` batch already waiting in `client.json` bypasses the new request boundary and the current budget, permitting 22 world calls in a minute.

Repository: `perseverance484/tnr-tools`. Target: **`60a28a84fb9b47910827c234b2e64e760ddcaa81`**, code `d7364237`, base `426a9fbabc5d25247f53d808d297412840a85e26`. Date: 2026-11-12. Report branch: `chatgpt/review-ai-player-ap1-rereview6`.

Read the handoff first, then Implementation Handoff §5. Used the focused scope agreed in the previous report: persisted requests, ordinary and pending upgrade state, selective legacy-ID recovery, and receipt/evidence controls. RUL-2026-11-11-149 through -152 remain settled. No policy question or token decision is reopened.

## Finding

### 1. F1 — Medium: a real legacy pending batch is printed without applying the corrected budget

Location: **`player/brain.py:548` and `:567`–570**, `_who` / `_a_waiting_batch`; publication path through `_exchange` at lines 668–669 and `next_batch`.

The new pending-batch predicate checks field types but does not distinguish the real `442a6311` pending format: that version already wrote a string `id`, integer `seq`, list `steps`, numeric `ready_at`, and `stop`. Therefore its batch survives `_who`. `_greet` transfers it to a replacement; `_exchange` sees a waiting batch and skips the request/brain/pacing path entirely. `serve` receives no request.

This matters because that old version scheduled calls on the assumption that loose calls expire after 900 seconds. The corrected player must retain those calls until evidence establishes completion. Adopting the old precomputed batch carries its obsolete admission decision across the upgrade. The pending shortcut predates this correction; the new shape check does not close this historical migration route.

Reproduction uses the actual old package, not a hand-constructed pending file:

1. Give batches to successive relays using old `brain next`, replacing each without handing it back. The first seven relays retain 21 world calls.
2. The eighth old request makes a two-call batch with a long brain-side wait, scheduled just after the first hold's old expiry. Kill that `brain next` at the wait, after it has saved `pending` and before printing it.
3. Upgrade to the frozen target and start a replacement with new `brain next`. The old pending batch passes `_a_waiting_batch`, waits until its old scheduled time, and prints `profile.getUser` and `travel.getSectorData`. No request reaches `serve`.
4. The earlier relays can resume just before this publication, following their own call/wait order. Twenty old calls fit in the preceding minute (the twenty-first has an internal wait). The two newly printed calls bring the world lane to **22**. The current budget, given these retained holds, admits **no** new world call.

The measured breach is the world cap of 20; this reproduction does not exceed the account-wide cap of 30. The consequence is loss of the promised world-lane bound and reserved capacity during migration. No live calls were made.

Refutation and controls:

- The old package itself writes every client, world and pending record. Its pending shape genuinely passes the new predicate; this is not the malformed missing-ID example in the new test.
- The new code's original `Brain` loads that same ledger and retains 21 loose calls. Its budget refuses a further world call. Publication still proceeds through the pending shortcut.
- The batch is waiting for a future `ready_at`; it is not stale under `_owed`. Its previous wait policy, rather than an expired outbox, is the issue.
- An isolated diagnostic that rejects only this old pending ID causes a new request, prints no call, and leaves the simulated minute at 20. Modern pending batches are otherwise preserved in that control. This is evidence of the bypass, not a proposed production patch.
- The ordinary upgrade and E1's queued-request upgrade both remain correct. This is a separate saved-pending state. No operator has confirmed the old relays stopped, so `stopped all` would not be a valid prerequisite or workaround in this scenario.

Required correction: identify and retire or safely revalidate pending batches from an incompatible client/ledger protocol before publication. A matching set of field types is insufficient. Preserve the holds and evidence for printed old batches, and preserve current-protocol pending delivery and receipt retries. Add a real old-package upgrade that dies **after pending is stored, during the hold**, alongside the existing before-answer fixture.

Runnable reproduction from the frozen repository root; needs commit `442a6311` in Git history and writes only temporary files:

```bash
python3 - <<'PY_REPRO'
# Run from the frozen repository root; no game connector is used.
import io, json, os, re, subprocess, tempfile, time
from pathlib import Path
from unittest.mock import patch
from player import brain, relay
from player.tests.test_relay import token_of
repo = Path.cwd()
old_sha = '442a63119d2fa3fe033877bedc86f5df8cd9be00'
old_program = r'''
import io,os,json,time
from unittest.mock import patch
from player import brain,relay
from player.tests.support import Rig,user
from player.tests.test_relay import token_of
r=Rig();r.world.absorb([user()._replace(at=r.t)]);r.world.save()
now=[r.t]; real=brain.Brain; printed=[]
class Died(Exception):pass
def sleep(t):
 if t>100:raise Died
 now[0]+=t
def nxt(token=None):
 out=io.StringIO();brain.next_batch(r.dir,token,out,sleep);return out.getvalue().splitlines()
with patch.dict(os.environ,{'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':os.path.join(r.dir,'none'),'TNR_PLAYER_FIGHTS':os.path.join(r.dir,'fights')}),patch.object(time,'time',lambda:now[0]),patch.object(brain,'Brain',lambda live:real(live,clock=lambda:now[0])):
 for i in range(15):
  token=token_of(nxt()[0])
  try:printed.append(nxt(token))
  except Died:break
 state=relay.read(os.path.join(r.dir,'client.json'));world=relay.read(os.path.join(r.dir,'world.json'))
 print(json.dumps({'live':r.dir,'now':now[0],'count':i+1,'pending':state.get('pending'),'calls':world['budget']['calls'],'printed':printed}))
'''
with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)
    names = subprocess.check_output(['git','ls-tree','-r','--name-only',old_sha,'--','player'],text=True).splitlines()
    for name in names:
        p = root/name; p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes(subprocess.check_output(['git','show',old_sha+':'+name]))
    for name in ('state','data','docs','scripts','harness','.claude'):
        (root/name).symlink_to(repo/name,target_is_directory=True)
    old = json.loads(subprocess.check_output(['python3','-c',old_program],cwd=root,
                     env={**os.environ,'PYTHONPATH':str(root)},text=True))
    live, now = old['live'], [old['now']]
    original_brain = brain.Brain
    def nxt(token=None):
        out = io.StringIO()
        brain.next_batch(live,token,out,lambda t:now.__setitem__(0,now[0]+max(0,t)))
        return out.getvalue().splitlines()
    with patch.dict(os.environ,{'TNR_PLAYER_NO_DAEMON':'1','TNR_TRANSCRIPT':live+'/none',
                               'TNR_PLAYER_FIGHTS':live+'/fights'}), \
         patch.object(time,'time',lambda:now[0]), \
         patch.object(brain,'Brain',lambda live:original_brain(live,clock=lambda:now[0])), \
         patch.object(brain,'serve',wraps=brain.serve) as served:
        ledger = original_brain(live,clock=lambda:now[0]).budget
        print('old loose calls:',sum(x[2] for x in ledger.loose()))
        print('legacy pending accepted:',brain._a_waiting_batch(old['pending']))
        lines = nxt(token_of(nxt()[0]))
        published = now[0]
        calls = [json.loads(s)['call'] for s in lines if s.startswith('{') and 'call' in json.loads(s)]
        print('new code printed:',calls,'served requests:',served.call_count)
        # Each old relay resumes half a second before publication. It follows its own
        # call/wait order and may pause before handing the completed batch in.
        made = []
        for batch in old['printed']:
            t = published-.5
            for line in batch:
                step = json.loads(line)
                if 'call' in step:
                    made.append(t); t += .001
                elif 'bash' in step and 'sleep(' in step['bash']:
                    t += float(re.search(r'sleep\((.*?)\)',step['bash'])[1])
        before = sum(published-60<t<=published for t in made)
        actual = before+len(calls)
        print('old calls in preceding minute:',before,'with new calls:',actual)
        print('current budget would admit:',ledger.pace([{'call':'profile.getUser','input':{},'select':[]}],'world')[0])
        assert actual > 20
PY_REPRO
```

Observed output:

```text
old loose calls: 21
legacy pending accepted: True
new code printed: ['profile.getUser', 'travel.getSectorData'] served requests: 0
old calls in preceding minute: 20 with new calls: 22
current budget would admit: []
```

## E1 and E2, unchanged

Both original scripts assert the defect, so their assertion failures are expected evidence of closure here. Neither script was edited.

| Case | What it prints before stopping | Disposition |
|---|---|---|
| E1, queued old replacement request on resident startup | Old request has `lost: true`, no `held`; all four ledger rows retain `"out"`. The assertion expecting four settled rows fails. | **Closed.** The old request is removed, not answered. Follow-up tests show the new client retains the four calls as unknown loose holds and stays within 30/20. |
| E2, numeric CLI ID beside another held batch | Listing contains `batch 1` and `still-running-2`; `stopped 1` returns `stopped: ["batch 1"]`, `not_held: []`, `still_held: ["still-running-2"]`. Its old-answer assertion fails. | **Closed.** The specific ID is queued as integer 1; the unrelated hold remains. The regression verifies application and the extra sixty seconds. |

The ordinary upgrade was repeated from the real `442a6311` package through new `brain next`: four calls remain held, no completion evidence is invented, old relay return says STOP and leaves the unknown hold, listing shows `batch 1`, and `stopped 1` now names it successfully.

## Earlier cases and controls

Original D/A/B/C scripts were rerun unchanged. C1/C2/C5 and their controls use the same adaptations already accepted in the earlier review; no new adaptation was required.

| Case | Result |
|---|---|
| D1 | Closed: active reservations remain 3 after first request and retry; the earlier operator word does not expand. |
| D2 | Closed: four calls remain loose; maxima 30 total / 20 world. |
| D3 | Closed: first crash hold 1 s; subsequent four holds 6 s; no empty hot loop. |
| Retention controls | Pass: timeout leaves token/held/handed unchanged; put result survives timeout/death; retry applies sector 77 once and removes the result. |
| Adapted C5 | Closed: only replacement profile call printed; correct receipt owner; real completion evidence applied and cleared. |
| Adapted C1 | Closed: time alone does not release the held call; maxima 30 / 20. |
| Adapted C2 | Closed: relay that never received a batch queues no completion evidence; all four calls remain held. |
| C3 | Closed: repeated-crash fallback acts both in one brain and with a new brain per request; completed-fight profile sends no action; sector 77 and receipt survive restart. |
| C3b | Closed: actual in-process fallback client emits actions and reads. |
| C4 | Closed: tested falsey/malformed answers count as zero accepted/unknown actions; fallback still fires. |
| Prior controls | Pass: completion accounting peaks at 30; ordinary replacement has its own decision/receipt; normal closure sends no old-fight action. |
| A1 | Closed: outstanding calls remain counted; actual peak 29. |
| A2 | Closed: unusable active-user/coordinate reads do not replace the good state or prevent defensive fallback. |
| A3 | Closed: stale pending waiter emits no old calls; fresh batch emits the new profile read. |
| B1 | Closed: malformed `{}` action in a log produces defensive actions with zero crashes. Unchanged script stops at its old defect assertion. Its existing valid-action control was also run separately and acts without crashing. |
| B2 | Closed: abandoned-call case peaks at 30; both timestamp-skew cases peak at 20. |
| B3 | Closed: results are applied once (`[1]`). |

Additional ownership controls still pass: two replacements leave only the final relay's calls; a response wait blocks a competing handshake; killing the client process releases its lock and lets the waiting handshake finish.

## Focused scope assessment

**Request boundary.** Both resident `run` and fallback `_await` now call `serve`. A real `442a6311` request lacks required ownership fields and is removed without answering or settling its batch. Independently removed each of the seven `REQUEST` fields from a captured current request: each was removed unanswered, with the ledger unchanged. A complete current request is answered; its exact retry uses the saved receipt without calling `handle` again. The committed restart/retry test also passes.

`REQUEST` is a structural compatibility check, not proof of authorship or a validator of every nested value. A dictionary carrying all seven keys passes it; compatible earlier requests using that same protocol also pass. I did not treat this as authentication of arbitrary edited local files. The actual unsafe old request from E1 is rejected. F1 bypasses this request boundary through saved pending state.

**Ledger and pacing.** A direct old-format `lost: true` request no longer means returned. `_paced` moves a still-unclassified out batch to an unknown hold before the budget's standalone pacing fallback can settle it. In ordinary operation `_ledger` has already classified it, so this adds no extra hold. The unchanged simulated fights retain their prior counts and action pacing; the injected ledger-failure test keeps the old calls held. Neither helper protects the legacy pending shortcut that never asks the brain.

**Client predicates.** `_a_relay` rejects unusable names/tokens/numbers; `_a_batch` filters old string/numeric ownership records; `_a_word` preserves current exact-ID completion rows and rejects the older short evidence shape. Non-object client files are reset. The ordinary migration and committed malformed-file cases run successfully. `_a_waiting_batch` rejects missing fields, but accepts the genuine older pending format: F1 is the limitation that matters in an actual historical upgrade. These are format checks, not exhaustive validation of every possible edited JSON value.

**Selective release.** CLI comparison and `not_held` now use the same printed representation, while queued evidence retains the saved ID's native type. Numeric batch 1, string batch IDs, relay tokens, unknown names and `all` are covered. The unrelated hold and sixty-second tail remain intact.

The operator page now contains the requested saved-ledger timing instruction: let the relay ask once more and list again if an expected hold is not yet visible. The director still owns including it in the session brief.

## Upgrade fixture fidelity and regression discrimination

Generated the upgrade files again with the actual `442a6311` package and compared the complete JSON structures/values against `player/tests/fixtures/upgrade_442a6311`, rather than comparing only request keys.

All non-volatile values and structures agree. Differences are limited to generated relay identities/tokens and timestamps: request `at`, sensory timestamp, four call admission times, relay `issued_at`, and receipt `at`. `made.json`'s source SHA, four-call count and holder/replacement relationships agree. The recorded `pending` is null, explaining why it cannot exercise F1.

**`test_the_version_before_itself` ran and passed; it did not skip.** It ran in the 331-test suite and was also run explicitly with verbose output.

On an external package extracted from `426a9fba`, this head's unchanged `test_rereview5.py` and fixtures give **6 failures, 3 errors, 2 passes**. For that extracted package, the historical loader's repository root was pointed at the real checkout so it could find `442a6311`; implementation modules remained the old package.

- Missing-name error: `brain.REQUEST` does not exist on the base, in the current-request restart test.
- Real old failure: list-valued `client.json` raises `AttributeError` in `_who`.
- Real old failure: list-valued request raises `AttributeError` in `_answered` via resident `run`.
- Passing controls: unknown names release nothing; the other existing ways to name a batch still work.

The new tests check externally visible replies, ledger preservation, actual paced calls, selective evidence and receipt use. Some persistence assertions depend on concrete field names, but they do not substitute for the behavioural checks. The pending-format test uses a missing-ID example, while the historical fixture stops before an answer exists; neither covers an authentic legacy pending batch.

I also snapshot-compared repository files before and after running all 11 new tests with bytecode writes disabled: **no additions, removals or modifications**. The full player suite and mutation run likewise left no runtime artifact visible in Git status before the separately requested legacy pilot tests. The latter create their established untracked outputs; those were moved to scratch before completion.

## Planted defect

In an isolated Python process, replaced the `serve` condition:

```python
isinstance(req, dict) and all(k in req for k in REQUEST)
```

with:

```python
isinstance(req, dict) and "seq" in req and "relay" in req
```

Asserted that the text replacement matched once. No tracked source was edited. The full suite ran 331 tests and produced **three failures, zero errors**: recorded old-file startup, real old-package startup, and rejection of non-current request shapes. The separate `lost`/pacing safeguards still prevented the old overspend, but the suite correctly detected that obsolete requests were answered at all. This mutation is caught. The walk does not model upgrades; its passing result cannot establish migration safety.

## Verification

| Command/check | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | 331 tests, OK; no skips reported |
| `python3 -m player.tests.test_walk 200 300` | 200 walks / 6,957 calls / zero problems |
| New regression module on the base | 6 failures, 3 errors, 2 passes |
| New regression module with repository file snapshots | 11 tests, OK; no file changes |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | 46 tests, OK; existing ResourceWarnings |
| `python3 scripts/player_allowlist.py check` | Exit 0; zero never-list violations |
| `python3 scripts/player_allowlist.py report --check` | Exit 0; current |
| `python3 scripts/rulings_index.py --check` | Exit 0; 322 rulings, index current |
| `python3 scripts/check_large_files.py` | Exit 0 |
| `python3 scripts/check_no_real_name.py --commits 426a9fba..60a28a84` | Exit 0; scans tracked files and correction commit messages |
| Four legacy pilot tests | All exit 0; planner parity 4,000/4,000 |
| `python3 scripts/player_size.py` | 3,951 code lines, 19 files; 5,721 test lines; brain 832, battle 685; 16 functions over 12 branches |
| `git diff --check` | Clean |

Legacy commands, from `state/player/dauntless/tools`: `python3 tests/test_planner2.py`, `python3 tests/test_pilot.py`, `python3 tests/test_integration.py`, `python3 tests/test_nearkill.py`.

Unchanged offline fight simulations: steady 14 turns / 78 calls / peak 23; burst 9 / 48 / 27; AI 13 / 82 / 24. No action pacing holds in those scenarios; maximum unread spans 16.4 / 36.6 / 21.4 seconds. These are fixture results, not live-play or token-cost measurements.

## Next step and safety statement

Correct F1 within pending-state migration. The next check can remain focused on legacy queued/pending upgrades, preserved outstanding holds, selective release, and current pending/receipt delivery, provided no wider assumption changes. Include a real old-package stop during the pending hold, and retain all existing controls. Keep the mechanical brain split after correctness acceptance and before AP2.

No live-game request, game write, live credential access or live relay connection was made. The frozen detached checkout and all pre-existing tracked files are unchanged. Only this report is added on a separate `chatgpt/review-*` branch; no `fable/*` branch is modified. Scratch packages, reproductions and process-local mutations stayed outside tracked implementation files.
