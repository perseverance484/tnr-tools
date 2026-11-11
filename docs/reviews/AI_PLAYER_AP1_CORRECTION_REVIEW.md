# AI player AP1 correction — independent review

**Verdict: REQUEST CHANGES.** Three confirmed defects remain at the frozen correction. The supplied regression suites pass; they do not establish the claimed execution-time rate limits or cover the two recovery cases below.

Repository: `perseverance484/tnr-tools`. Lane A; Engineering Auditor; review only.

- Target: `fable/ai-player-ap1` @ `39f30ead2b23575fa9bac1ebe85c6d1873ce3808`.
- Previous reviewed target: `583fe35390e4701eea50f331ae2bc10013f150c9`.
- AP0 base: `40788e78d4159777a47e0b317fe13d83fa1819b3`.
- Observed remote `main`: `6559fe192640dc05cd76210863d766a08b230965`; not substituted for the frozen target.
- Handoff: `docs/reviews/AI_PLAYER_AP1_CORRECTION_HANDOFF.md`.
- Prior report: `docs/reviews/AI_PLAYER_AP1_REVIEW.md` on `chatgpt/review-ai-player-ap1`, commit `e94bf21c23701d576d06d4116ceb5d753c7d8ce6`.

The correction changes budget scheduling, relay identity and result collection, turn recovery and outcome tracking, and wiring tests. Those assumptions warranted renewed adversarial review, beyond rerunning the original examples. Every finding below was reproduced at the target and checked against a control or the existing recovery tests. No live-game request was made.

## Findings

### 1. High — predicted call times still allow both rate limits to be exceeded

**Location:** `player/budget.py:113` (predicted timestamps), `:53` (expiry); test oracle `player/tests/support.py:165` (`Ledger`).

The history records each call at its predicted execution time using `CALL_COST = 0.4`, then expires that entry after 60 seconds. Neither collected result timestamps nor actual relay progress reconcile this history. Calls later in a slow batch can execute well after their recorded times. Subsequent faster batches spend capacity before those earlier calls actually leave the rolling minute.

**Reproduced:** eleven batches of two actions separated by the required 1.2-second wait, followed by the two normal watching reads. Execute every returned wait and call in order, with per-call latencies `[8, 3, .4, 1, .2, .2, .4, 3, .4, 1, 3]` seconds by batch and 0.5 seconds between batches. The supplied `Ledger` reports a maximum of **30**; independently recording the time each call is issued yields **31** in the minute ending at 83.2 seconds. Five-call world batches, with latency 8 seconds in the first batch and .4 seconds in the next seven, yield **24 actual world calls**, while the ledger reports **20**.

**Refutation:** every emitted wait, including budget waits, was honored. No oversized battle batch or unrequested extra call was introduced. Holding latency at the assumed .4 seconds gives 30 actual calls, confirming the mismatch is execution timing. This is an allocator reproduction, not a claim about a completed live fight. The handoff's simulated fights use the same predicted-time ledger, so their green limit assertions do not refute it.

**Correction needed:** account conservatively for actual completion/dispatch of issued batches, including delayed and uncertain calls, before releasing capacity. Validate with an independent execution-time ledger under variable latency. Merely adding another fixed latency allowance does not establish either hard cap.

### 2. High — malformed reads bypass the last-good-read deadline and lose an owed turn

**Location:** `player/activities/battle.py:152`, `:191–195`; fallback is only reached through `_no_read` at `:166`.

A decoded dictionary is treated as a read before its fighter columns are validated. When those columns are misaligned, `_tick` always requests another read. It never consults the open turn's deadline or the valid last read. Thus a sequence of unusable reads prevents the corrected fallback from running even after all issued actions were explicitly refused.

**Reproduced:** start the supplied logged fight on our turn; return `Action not valid anymore` for both planned actions. Supply battle reads with the two fighter IDs intact but only one `curHealth` value at T+1, T+12, T+15, T+20 and T+60. Every batch contains reads and **zero actions**. The original turn remains `sent=2, answered=2, accepted=0`; a valid next-round read closes it as **missed**. A valid last read and unbanned emergency actions remain available throughout.

**Refutation:** replace those malformed reads with rate-limit refusals and the corrected code sends `defensiveStance`, then `wait` if that action is also refused. The failure therefore survives the original missing/refused-read fix. Rejecting misaligned columns is appropriate; indefinitely bypassing the T+12 fallback is not required to reject them.

**Correction needed:** treat an unusable read as unavailable for the turn clock, preserving the last valid read and the sent/answered evidence. Add this case to chaos tests and enforce the deadline through that path.

### 3. Medium — a waiting old client can undo relay replacement

**Location:** `player/brain.py:286–311`, especially the unconditional write after `_await` and the hold.

`next_batch` checks ownership once, then keeps its private copy of `client.json` across potentially long waits. A replacement relay can acquire a new identity during that wait. When the old invocation resumes, it overwrites the replacement's identity and prints its batch. The replacement is subsequently told to stop. The one-brain lock protects the resident world model, not this client-state transition.

**Reproduced with the real client and in-process answer path:** create a relay, obtain its profile-read batch, and submit the offline fixture using `put`. While its next invocation spends the ordinary eight-second hunt hold, perform a new relay handshake. Resume the original invocation. It prints its profile/scan/sensory/harvest batch and stores the old relay ID again; the newly created relay receives `STOP superseded: another relay has taken over`.

**Refutation:** the existing sequential supersession test passes, and an old invocation started after replacement is correctly stopped. The defect requires replacement while an already-running invocation is waiting. Reproduction also succeeded without mocking `_await`, `_collect`, the brain lock or the state writer. Only time sleeping was replaced with a deterministic interleaving; all game responses were offline fixtures.

**Correction needed:** serialize ownership transitions and revalidate ownership atomically before committing client state or publishing a batch. A retired invocation must not overwrite or emit work after a replacement has acquired ownership. Test replacement during both the response wait and the brain-side hold.

## Reproduction commands

Run these snippets from the frozen repository root. They use temporary folders and fixtures, make no network calls, and change no tracked files.

### Execution-time rate limits

```bash
python3 - <<'PY'
from player.tests.support import Rig, Ledger
from player import calls as K
from player.activities.battle import watching

for lane, lags in [('battle', [8,3,.4,1,.2,.2,.4,3,.4,1,3]),
                   ('battle', [.4]*11), ('world', [8]+[.4]*7)]:
    r = Rig(); origin = r.t; ledger = Ledger(r); actual = []
    for lag in lags:
        steps = ([K.user()]*5 if lane == 'world' else
                 [K.act('B','a',0,0,1), K.wait(1.2), K.act('B','b',0,0,2)] +
                 watching([K.battle('B'), K.entries('B',8)]))
        out, _ = r.brain.budget.pace(steps, lane)
        for s in out:
            if 'wait' in s: r.t += s['wait']
            else: actual.append(r.t-origin); r.t += lag
        r.t += .5
    worst = max(sum(t-60 < u <= t for u in actual) for t in actual)
    print(lane, 'predicted', ledger.worst(lane), 'executed', worst)
PY
```

Expected: `battle predicted 30 executed 31`; control `30 / 30`; `world predicted 20 executed 24`.

### Malformed-read recovery

```bash
python3 - <<'PY'
from player.tests.support import Rig, start_fight, battle_read
from player.tests.test_review import answers, NOT_VALID, acts, turns
r = Rig(); b, _, out = start_fight(r); T = r.t
bad = dict(b); bad['battle.usersState.*.curHealth'] = [123]
for t in [1,12,15,20,60]:
    out = r.tick(*answers(out, NOT_VALID), battle_read('B1', bad), dt=T+t-r.t)
    print(t, acts(out))
next_read = dict(b)
next_read['battle.round'] += 1; next_read['battle.version'] += 4
r.tick(battle_read('B1', next_read))
print(turns(r)[0]['outcome'])
PY
```

Expected: no actions at any timestamp; `missed`.

### Relay replacement during the normal hunt hold

```bash
python3 - <<'PY'
import io, os, json
from unittest.mock import patch
from player import brain, relay, config as C
from player.tests.support import Rig, user
from player.tests.test_relay import token_of
r = Rig(); r.world.save()
def nxt(token=None, sleep=lambda _: None):
    out = io.StringIO(); brain.next_batch(r.dir, token, out, sleep)
    return out.getvalue().splitlines()
with patch.dict(os.environ, {'TNR_PLAYER_NO_DAEMON':'1',
        'TNR_TRANSCRIPT':os.path.join(r.dir,'missing.jsonl'),
        'TNR_PLAYER_LIVE':r.dir, 'TNR_PLAYER_FIGHTS':os.path.join(r.dir,'fights')}):
    t0 = token_of(nxt()[0]); t1 = token_of(nxt(t0)[-1])
    brain.put(r.dir, t1, 1, json.dumps(user().data))
    replacement = []
    def replace(delay):
        if delay == C.HUNT_WAIT: replacement.append(token_of(nxt()[0]))
    old_output = nxt(t1, replace)
    print('old/new/stored', t1, replacement[0],
          relay.read(os.path.join(r.dir,'client.json'))['token'])
    print('old emitted calls', [json.loads(x)['call'] for x in old_output
                               if x.startswith('{') and 'call' in json.loads(x)])
    print('replacement output', nxt(replacement[0]))
PY
```

Expected: stored token returns to the old ID, old client emits calls, replacement is stopped.

## What passed, and what remains open

All originally requested commands were rerun at `39f30ead`:

| Check | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | 202 tests OK |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | 46 tests OK; existing catalog ResourceWarnings |
| `python3 scripts/player_allowlist.py check` | 93 endpoints; zero never-list violations |
| `python3 scripts/player_allowlist.py report --check` | Current |
| `python3 scripts/player_size.py` | 3,030 code lines, 19 files; 2,957 test lines |
| Legacy `test_planner2.py`, `test_pilot.py`, `test_integration.py`, `test_nearkill.py` | All exit 0; 4,000/4,000 planner parity |

The original numbered findings have this disposition:

| Original finding | Correction review |
|---|---|
| 1: shared limit | Original schedule passes its predicted ledger; actual-time defect remains, finding 1 above. |
| 2: refused/unsent plans | Original refusal and transient post-planning crash cases pass; malformed-read deadline remains, finding 2 above. Persistent non-planner tick crashes remain an explicitly disclosed limitation. |
| 3: illegal repeated fallback | Bans are respected; best prior line, stance, then wait are covered. The final wait policy remains a director decision. |
| 4: stale/foreign results | Token-bound transcript and expected-call matching pass the original cases. Relay takeover has the separate overlap defect above. |
| 5: unknown spending | Zero-allowance/no-profile cases are covered; unknown price uses the pocket upper bound. This is not independent verification of the game's debit source. |
| 6: holds across midnight | Overnight and explicit-date holds pass, including the actual 24-hour director hold. |
| 7: missed-turn evidence | Acted/missed/unresolved cases pass; the new malformed-read reproduction is correctly recorded as missed once the next round is read. |
| 8: wiring oracle | Production Combat adapter, script boundary evidence, inventory checks and unplug tests replace the original stub-only coverage. No claim that they exercise every downstream planner implementation. |
| 9: premature item events | Events follow successful answers; refusal and gate-block cases pass. |
| 10: incomplete archives | Initial seat and raw ground representation/status cases pass. |
| 11: shell quoting | Quoted heredoc/stdin fallback passes the quote, substitution and multiline cases. |

AP1 steps 1–2 are implemented but takeover recovery needs correction; step 3 remains blocked by findings 1–2 and the budget contract decision; step 4's gate checks pass; step 5's core port and ordinary parity checks pass subject to turn recovery; step 6's wiring checks are substantially stronger and pass; step 7's suite passes but needs the new recovery cases. AP7 step 1's status/events/control writers remain present, including unresolved-turn reporting and corrected item events. No correction introduces a control setting that bypasses the fixed never rules.

**Director decisions, separate from defects:** the canonical AP1 brief still says battle and recovery are “never paced.” The correction intentionally paces them when capacity is exhausted, and changes the design, not that approved contract. Recording this conflict is useful but does not authorize it. Resolve and record the policy before declaring AP1 compliant. The handoff also seeks a ruling on `wait` as the final own-turn fallback; this review does not silently grant it. AP2 spend/equipment/day-boundary decisions remain outside this review.

The two decisions already settled by RUL-2026-11-11-151 remain settled: rotation after 60k context growth or 150k absolute, never during a fight; harvested logs may inform live play. Constants, rotation logic, harvest gate and opponent-log ingestion agree with them. No new decision is requested on either.

Size figures match the handoff: largest file `battle.py` 484 lines; largest function `_tick` 40 lines. Nine functions exceed 12 branches: battle `_tick` 17, `_my_turn` 15, `_no_read` 14, `_absorb` 13; combat `plan_turn` 16; calls `ground_cols` 15; gates `do_not_attack` 15; brain `_compose` 14; relay `find_transcript` 13. These are visible AP6 debt, not an invented AP1 size gate. The correction adds 373 production lines over the original 2,657; that is not evidence of runtime token cost by itself.

**Efficiency claims remain unmeasured:** no live baseline exists for relay tokens/hour, tokens/fight, error rate or missed turns. The passing offline suites and added code cannot establish improvement in those measures. Review-tool usage and setup errors are not player runtime measurements. The director-started live session remains out of scope and has not been performed.

## Handoff to Fable

Address the three findings with focused corrections and independent regression evidence, record the required director policy decisions, then return another frozen SHA. Do not expand into AP2 or AP6 consolidation to close this review. In particular, measure calls at execution time rather than using the scheduler's own predictions as its test oracle.

The frozen review checkout remained clean: no existing tracked file changed, no implementation fix was made, and no `fable/*` branch was modified. Test-created untracked artifacts were moved outside the checkout. The only repository addition from this review is this report on a separate ChatGPT review branch. **No live-game request was made.**
