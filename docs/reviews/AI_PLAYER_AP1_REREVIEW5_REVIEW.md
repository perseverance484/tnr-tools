# AP1 independent re-review 5 — Lane A

**Verdict: request changes.** D1–D3 are closed by their unchanged reproductions. Two further migration defects survive refutation: a queued request from the real `442a6311` package can release an unreturned relay's calls; and the operator cannot selectively release a numeric legacy batch ID from the CLI.

Repository: `perseverance484/tnr-tools`. Reviewed exactly `426a9fbabc5d25247f53d808d297412840a85e26` (code `bd5cc575`), against `efa79808e740811fa562466d332fd01171068cb7`. Review date: 2026-11-12. Review branch: `chatgpt/review-ai-player-ap1-rereview5`.

Read the new handoff first, then Implementation Handoff §5. Repeated the full relevant evidence, retry and migration scope, rather than only the changed tests. The changes to persistent classification and operator evidence justify that scope. RUL-2026-11-11-149 through -152 remain settled; the director's three open token decisions are not findings. No token-use improvement is claimed or measured here.

## Findings

### 1. E1 — High: the resident brain accepts an old queued replacement request as proof that the old batch returned

Location: `player/brain.py:127`–128 (`Brain._ledger`), reached through `answer` at line 413 and the resident `run` request loop.

`442a6311` writes replacement requests containing `lost: true` and no `held` field. The new client normally clears leftover request files before asking the brain, but starting the resident brain itself consumes an existing request first. `answer` forwards the old request unchanged. `_ledger` interprets **absence of `held` as a returned batch**, an accommodation documented there for direct test callers. This also applies to real old request files.

I produced this state with the actual old package, without constructing either its client file or request file by hand: A receives four calls; B replaces A; B's `brain next` dies after writing its request and before waiting for the answer. A has not returned or been stopped. Starting the new resident brain converts all four old `out` entries to settled entries. Sixty-two seconds later, A can execute its four calls and the current budget can admit another 30 recovery calls or 20 world calls: **34 total / 24 world calls in a minute**.

Refutation checks:

- The old request really says `lost: true`; this is not an invented malformed client or a direct `Brain.handle` test without ownership fields.
- Running the same queued-request setup through the old package leaves all four calls loose. The new resident path releases them.
- The ordinary upgrade through the new `next_batch` path retains all four calls. That is the path the handoff and the committed migration test cover. It does not establish safety of resident startup with queued files.
- Pausing the new decision keeps its output empty and isolates the old reservation. Pause does not stop the replaced relay or supply completion evidence.
- The minute counts below come from the old relay's four simulated executions and the new pacer's returned waits/calls. No game request is made.

Required correction: treat production requests missing modern ownership evidence conservatively. Safely retire old-format queued requests, or normalize them without treating missing fields as completion evidence; do not let the direct-test convenience bypass the production request boundary. Add a real old-package queued-request upgrade test through `run`, including the case where a replacement requested the batch. Retain the existing receipt/retry and normal-return controls.

Runnable reproduction from the frozen repository root (requires the old commit object; uses only temporary files, fixture data and local Python):

```bash
python3 - <<'PY_REPRO'
# Run from the frozen repository root. Only temporary files and fixture calls.
import json, os, subprocess, tempfile
from pathlib import Path
from player import brain, calls as K, relay
from player.tests.test_rereview2 import most_in_a_minute
repo = Path.cwd()
old_sha = '442a63119d2fa3fe033877bedc86f5df8cd9be00'
old_program = r'''
import io,json,os
from unittest.mock import patch
from player import brain,relay
from player.tests.support import Rig,user
from player.tests.test_relay import token_of
r=Rig();r.world.absorb([user()._replace(at=r.t)]);r.world.save()
def nxt(token=None):
    out=io.StringIO();brain.next_batch(r.dir,token,out,lambda _:None)
    return out.getvalue().splitlines()
with patch.dict(os.environ,{'TNR_PLAYER_NO_DAEMON':'1',
                           'TNR_TRANSCRIPT':os.path.join(r.dir,'missing'),
                           'TNR_PLAYER_FIGHTS':os.path.join(r.dir,'fights')}):
    a=token_of(nxt(token_of(nxt()[0]))[-1])
    n=len(relay.read(os.path.join(r.dir,'world.json'))['budget']['calls'])
    b=token_of(nxt()[0])
    with patch.object(brain,'_await',side_effect=RuntimeError('killed after request write')):
        try:nxt(b)
        except RuntimeError:pass
    relay.write(os.path.join(r.dir,'control.json'),{'version':1,'paused':True})
    print(json.dumps({'live':r.dir,'old':a,'n':n}))
'''
with tempfile.TemporaryDirectory() as tmp:
    old_root=Path(tmp)
    paths=subprocess.check_output(['git','ls-tree','-r','--name-only',old_sha,'--','player'],text=True).splitlines()
    for name in paths:
        p=old_root/name;p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes(subprocess.check_output(['git','show',old_sha+':'+name]))
    for name in ('state','data','docs','scripts','harness','.claude'):
        (old_root/name).symlink_to(repo/name,target_is_directory=True)
    old=json.loads(subprocess.check_output(['python3','-c',old_program],cwd=old_root,
                      env={**os.environ,'PYTHONPATH':str(old_root)},text=True))
    live=old['live']
    request=relay.read(relay.pending_requests(live)[0])
    print('legacy request:',request)
    assert request['lost'] and 'held' not in request
    brain.run(live,forever=False)  # The actual new resident entry point.
    saved=relay.read(os.path.join(live,'world.json'))['budget']['calls']
    print('old relay never returned; ledger:',saved)
    assert len(saved)==old['n']==4 and all(len(c)==2 for c in saved)
    for lane,batches in [('recovery',15),('world',10)]:
        now=[max(c[0] for c in saved)+62]
        budget=brain.Brain(live,clock=lambda:now[0]).budget
        made=[now[0]]*old['n']  # A now performs the four calls it still holds.
        for _ in range(batches):
            steps,_=budget.pace([K.user(),K.user()],lane)
            for s in steps:
                if 'wait' in s:now[0]+=s['wait']
                else:made.append(now[0]);now[0]+=.01
        print(lane,most_in_a_minute(made))
PY_REPRO
```

Observed final lines: `recovery 34`, `world 24`; the four old entries have only `[time, "world"]`, with no outstanding/loose state. This script asserts the defect; a corrected implementation should retain those reservations or refuse the legacy request safely.

### 2. E2 — Medium: `stopped BATCH` cannot name a numeric legacy batch ID

Location: `player/brain.py:704` and line 712 (`stopped`); numeric IDs are retained by `player/budget.py:_shape` / `settle` and returned by `_held`.

In the successful ordinary upgrade from the real `442a6311` package, the old batch is held under integer ID `1`, with no relay token. Listing shows `batch 1`. The documented CLI command `python3 -m player.brain stopped 1` passes the string `"1"`; it fails both membership tests against integer keys, reports `not_held: ["1"]`, and queues no evidence. That batch remains held indefinitely.

This is a selective recovery defect, not an overspend by itself. `stopped all` works, but is not a valid substitute when another replaced relay may still run. The operator should be able to release the one batch known to be stopped while retaining the other.

Refutation: passing native integer `1` directly to `stopped` releases exactly this batch, leaves another held batch untouched and preserves the sixty-second accounting tail. The ID is valid; CLI-to-ID matching is the failure. The existing ID test uses a newly generated string ID and misses the migration case.

Required correction: make the documented textual ID resolve the saved numeric batch without broadening the evidence set, and make `not_held` use the same resolution. Test actual CLI string input against a migrated numeric ID alongside an unrelated held batch.

Runnable isolated reproduction from the frozen repository root:

```bash
python3 - <<'PY_REPRO'
import contextlib,io,json,os
from unittest.mock import patch
from player import brain,relay
from player.tests.support import Rig
r=Rig()
# A numeric batch id, as the real 442a6311 package writes; another replaced relay remains live.
r.world['budget']['calls']=[[r.t,'world','loose',1,r.t,None],
                            [r.t,'world','loose','other',r.t,'still-running-2']]
r.world.save()
def cli(*names):
    out=io.StringIO()
    with patch.dict(os.environ,{'TNR_PLAYER_LIVE':r.dir}),contextlib.redirect_stdout(out):
        brain.main(['stopped',*names])
    return json.loads(out.getvalue())
print('listing:',cli())
reply=cli('1');print('stopped 1:',reply)
assert reply['stopped']==[] and reply['not_held']==['1']
assert not (relay.read(os.path.join(r.dir,'client.json')) or {}).get('ended')
# Refutation control: the native numeric id is valid and settles exactly that batch.
out=io.StringIO();brain.stopped(r.dir,[1],out);print('native integer control:',out.getvalue().strip())
r.brain.evidence(brain._who(os.path.join(r.dir,'client.json')))
assert r.world['budget']['calls'][0][2:]==[]
assert r.world['budget']['calls'][1][2]=='loose'
assert r.brain.budget.used()==2
r.t+=61
assert r.brain.budget.used()==1
print('native id releases only batch 1; sixty-second tail preserved')
PY_REPRO
```

Observed: listing contains `batch 1`; `stopped 1` returns no stopped batches and `not_held: ["1"]`. The native-integer control releases only batch 1, with the other call still held after 61 seconds.

## Previous cases, rerun unchanged

The original scratch scripts were used, not replacements derived from the new regression tests. C1, C2, C5 and the controls retain exactly the adaptations already used for the previous review. The new code required no further edits to them.

| Case | Disposition | Evidence on this head |
|---|---|---|
| D1: replay of `stopped all` widens its scope | Closed | Active relay's three reservations remain three after the first request and after its retry. |
| D2: missing ownership means never printed | Closed for the unchanged case | Four old calls stay loose; independent execution peaks are 30 total and 20 world. E1 is the additional resident/legacy-request route. |
| D3: no-room last resort spins | Closed | First crash holds 1 s; requests 2–5 each hold 6 s, with no call. |
| Retention: timeout and death before receipt | Pass | Token/held/handed state unchanged on timeout; put result retained through timeout/death; retry applies sector 77 and removes the result. |
| Adapted C5: foreign answer/request ownership | Closed | Only the replacement's profile call is printed; its receipt owns the response; genuine completion evidence is applied and cleared. |
| Adapted C1: held calls expire by time | Closed | Original call remains held; peaks 30 total / 20 world across the old expiry boundary. |
| Adapted C2: relay that never received a batch releases another | Closed | Both superseded responses say STOP; no evidence queued; all four calls remain loose. |
| C3: repeated tick failure, including restarted brain | Closed | Both resident and new-brain-per-request cases send fallback actions; completed-fight profile sends none; learned sector 77 and receipt survive restart. |
| C3b: real in-process fallback client | Closed | The repeated-crash client emits action batches and read batches rather than treating every crash as the first. |
| C4: falsey action answers count as accepted | Closed | False, zero, empty string/list, null and an invalid string produce zero accepted/unknown actions; fallback still fires. |
| Prior controls | Pass | Completion accounting peaks at 30; ordinary replacement gets its own profile decision/receipt; normal closure sends no old-fight action. |
| A1: watchdog/outstanding-call accounting | Closed | Outstanding calls remain counted; independent actual peak 29. |
| A2: unusable read defeats turn clock | Closed | Defensive fallback occurs; stored good active user is retained; null coordinate does not produce an unsendable action. |
| A3: stale pending batch | Closed | Old waiter emits no old calls; fresh pending batch emits the fresh profile call. |
| B1: malformed action in battle log wedges the turn | Closed | `{}` action produces defensive actions and zero crashes. The unchanged script exits at its old defect assertion (`assert not any(...)`) because actions now occur. Separately running its existing valid-action control also produces actions and zero crashes. |
| B2: abandoned calls / timestamp skew | Closed | Abandoned-call maximum 30; both timestamp-skew cases peak at 20. |
| B3: results reapplied after client death | Closed | Results applied once: `[1]`. |

Ordinary real upgrade was repeated using the `442a6311` package's own `brain next`: four calls held before and after the new client takes over, no operator evidence invented. Old relay return says STOP and does not release the unknown holder. Listing shows `batch 1`; `stopped all` settles it. E2 describes the selective-ID failure in that same upgrade.

Additional unchanged ownership controls: two successive replacements leave only the last relay's four calls; the response wait blocks a competing handshake; SIGKILL releases the client lock and the waiting handshake completes. These are real process/lock checks, unlike the walk's exception-based deaths.

## Evidence, retry and migration assessment

- `stopped` snapshots concrete batch IDs under the client lock. There is no delayed wildcard expansion. Replaying those rows does not reach a later replacement's batch. Listing now makes no write.
- For the modern, intact client protocol, ownership is assigned immediately before output, pending batches survive replacement, and request IDs distinguish answers. `_exchange` writes the request ID to `unprinted` before publishing the request. `_owed` records an expired unpublished batch and retires its sequence before the next request. The persisted-before-publication crash cases retain positive evidence rather than guessing from absence.
- `_who` drops older ownership/evidence shapes conservatively. Modern-client requests with missing history keep calls loose under an unknown holder. However, `_who` is not a validator for request files read directly by the resident brain: E1 is the uncovered boundary.
- `_held` reads an atomic saved world file as well as replaced-client ownership. It may omit a batch becoming loose in an unsaved tick; that is a conservative, documented delay. Its ordinary `out` versus `loose` distinction excludes the running relay's batch in the reviewed intact-client paths. It is not evidence that all older records are safe: E1/E2 remain.
- `Budget._shape` retains older loose entries, gives missing IDs an explicit identity and removes the obsolete timeout interpretation. No elapsed-time path removes a loose hold. `ended` matches one exact ID; the old `"*"` operation is gone. Evidence is counted for a further minute. Unknown holders cannot be released by a guessed relay return.
- `_paced` now governs normal and last-resort output. `_record` supplies the final six-second guard for an empty decision. The D3 and ordinary-tick controls pass; no repeated zero-work/zero-wait loop was reproduced in the corrected modern-client path.
- Results retained before receipt, receipt retries, failed-tick persistence and saved learned state remain covered by the unchanged controls and full suite. No new duplicate action or duplicate application was reproduced in that protocol.

The three correction groups address real defects and are appropriately focused. The console tuple change adds batch IDs needed for operator recovery; the older regression's switch from wildcard release to a specific batch is required by the corrected contract. Neither is an unrelated behavioural expansion. The migration boundary is still incomplete as E1/E2 show.

## Operator page

`player/OPERATOR.md` supplies the requested session material: why holds exist, their status/event visibility, the four command forms, what confirmed stopped means, why silence is insufficient, the fixed scope of `all`, six-second retries when blocked, the extra minute, and when the brain applies/logs the statement. Trusting a truthful operator statement remains acceptable under the settled ruling.

The page's selective `BATCH` form must work for the legacy IDs it is intended to recover (E2). The saved-ledger timing limitation is documented in the handoff; a short instruction to list again after the next tick if a hold has not yet appeared would make the session page more complete. This last documentation suggestion is not an additional blocker. The director still owns whether the page goes into the live session brief.

## Walk and mutation assessment

The walk now exercises read-only listing, `stopped all` followed by replacement/retry, loss of the held record or entire client file, and duplicate publication to the same relay. Its eight checks are meaningful within the model:

- Actual call timestamps are recorded when simulated relay calls execute; the cap is not derived from the budget ledger.
- Ledger totals and per-batch outstanding counts check under-accounting and evidence scope.
- Heard evidence and known publication check retained/phantom holds.
- Applied-result counts and published batch IDs check repeat application/publication.
- Listing compares client state before and after a read-only operation.

`200 × 300` steps produced **6,957 calls, zero walks with a problem**. These checks still do not model migration from old request files, numeric legacy CLI IDs, resident-daemon file processing, real process scheduling/locks, partial stdout delivery, transcripts, combat/other lanes, or a relay that violates the line-order contract. The `once` counter observes nonempty results with held metadata; it is not a general proof of exactly-once processing of every ancillary field. Aggregate ledger counts alone cannot establish every call's timestamp, hence the separate evidence and boundary tests remain necessary. E1/E2 demonstrate actual coverage gaps.

I planted defects only by replacing functions in isolated Python processes; no tracked source was edited. Each source replacement was asserted to match once before running tests.

| Mutation | Full 320-test suite | Separate 40 walks × 300 steps |
|---|---|---|
| Listing also acknowledges every held batch: in `stopped`, change `if "all" in names or t in names or b in names` to `if not names or "all" in names or t in names or b in names` | 3 failures: the two focused listing/unknown-holder tests and the suite's walk test | 40/40 detect it, starting with listing changing client state |
| Unknown ownership counts as never printed: final `_ledger` branch changes `settle(holder=None)` to `settle(asked=())` | 6 failures: five focused tests and the suite's walk test | 31/40 detect it in this run |

Thus the old text mutation's no-op is not mistaken for a passed mutant. The equivalent defect is now detected. The handoff's two focused listing failures agree with my result; the full-suite count additionally includes the walk test. I independently ran these two mutations, not all twenty in the author's table.

## Regression discrimination and verification

Copied this head's `test_rereview4.py`, unchanged, into an external package extracted from `efa79808`. Result: **15 tests, 10 failures, 4 errors, 1 pass**, as claimed.

The errors are specifically:

1. `test_a_batch_whose_brain_next_died_is_known_to_be_unprinted`: missing `unprinted` key.
2. `test_two_deaths_in_a_row_are_both_remembered`: missing `unprinted` key.
3. `test_asking_what_is_held_changes_nothing`: JSON decoding of an empty captured stdout stream; the old CLI uses the function's bound default output stream. This is a capture/API difference, not proof of the listing defect by itself.
4. `test_a_ledger_in_an_older_shape_keeps_its_holds`: real old `IndexError` in `Budget.loose`, indexing fields absent in the legacy entry.

The passing control is the ordinary tick's existing wait behaviour. The new tests exercise real client operations, persistence, observed calls and holds; some additionally assert the concrete durable representation. They are not just mocks asserting that a new helper was called. They nevertheless omit the two migration cases above.

| Command/check | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | 320 tests, OK; includes original review, wiring and live-session regressions |
| `python3 -m player.tests.test_walk 200 300` | 200 walks, 6,957 calls, zero problems |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | 46 tests, OK; existing ResourceWarnings emitted |
| `python3 scripts/player_allowlist.py check` | Exit 0; no never-list violations |
| `python3 scripts/player_allowlist.py report --check` | Exit 0; report current |
| `python3 scripts/rulings_index.py --check` | Exit 0; 322 rulings, index current |
| `python3 scripts/check_large_files.py` | Exit 0 |
| `python3 scripts/check_no_real_name.py` | Exit 0 |
| `python3 scripts/check_no_real_name.py --commits efa79808..426a9fba` | Exit 0 |
| `state/player/dauntless/tools`: `python3 tests/test_planner2.py`, `test_pilot.py`, `test_integration.py`, `test_nearkill.py` | All exit 0; planner parity 4,000/4,000 |
| `python3 scripts/player_size.py` | 3,895 code lines / 19 files; 5,422 test lines; brain 776, battle 685; 15 functions over 12 branches |
| `git diff --check` | Clean |

The three unchanged offline fight simulations retain the previous figures: steady 14 turns / 78 calls / peak 23; burst 9 / 48 / 27; AI 13 / 82 / 24. No action pacing holds in those simulations; maximum unread spans 16.4 / 36.6 / 21.4 seconds respectively. These are fixture results, not live-play or token-cost measurements.

## Next handoff and safety statement

Correct E1 and E2 without redesigning the client protocol. A focused re-check should cover persisted request migration through resident startup, ordinary upgrade, selective legacy-ID CLI recovery, and their receipt/evidence controls; rerun the full required suite and walk. If the correction changes ownership or receipt assumptions again, repeat that affected scope. Keep the mechanical split of `brain.py` after correctness acceptance and before AP2, as previously agreed.

No live-game request, game write, live-game credential access or live relay connection was made. The frozen detached checkout and all pre-existing tracked files are unchanged. Legacy tests' generated untracked outputs were moved to scratch. Only this report is added on the separate `chatgpt/review-*` branch; no `fable/*` branch is modified. All reproductions, copied packages and mutations ran in temporary/scratch locations or isolated processes.
