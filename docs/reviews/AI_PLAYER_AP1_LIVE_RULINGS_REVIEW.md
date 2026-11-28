# AI player AP1 — live fixes and rulings re-review

**Verdict: REQUEST CHANGES.** The three findings from the correction review still reproduce. One additional defect survives in the transition between fights. RUL-2026-11-11-152 resolves the previously open policy decisions; it does not resolve these implementation defects.

Reviewed 2026-11-12, Lane A, Engineering Auditor, review only.

- Repository: `perseverance484/tnr-tools`.
- Target: `fable/ai-player-rulings` @ `c225ed36f8ca4f1631d97d5f267546a9eb46f10d`.
- Previous frozen target: `39f30ead2b23575fa9bac1ebe85c6d1873ce3808`.
- Original AP1 target/base: `583fe35390e4701eea50f331ae2bc10013f150c9` / `40788e78d4159777a47e0b317fe13d83fa1819b3`.
- Observed remote main: `e6f9f283d8a5d3dcdf46acda04d4668da1448d15`; not used as the review target.
- Read the correction/live handoffs, updated brief/design/allowlist, RUL-152, and the changed code/tests against the existing review authority.
- Previous correction report, with runnable reproducers: [AI_PLAYER_AP1_CORRECTION_REVIEW.md at adeb7807](https://github.com/perseverance484/tnr-tools/blob/adeb780712176e8fb0ccd056066df59be38b96c5/docs/reviews/AI_PLAYER_AP1_CORRECTION_REVIEW.md).

## Confirmed findings

### 1. High — execution-time call limits remain unenforced

**Location:** `player/budget.py:113` and `:53`.

The allocator still timestamps calls using the assumed 0.4-second call cost and expires those predictions without reconciling actual execution. A slow batch followed by faster batches can therefore exceed the account limit while its own ledger remains green. RUL-152 authorizes priority and pacing policy; it does not make predicted timestamps actual account usage.

**Reproduced at c225ed36:** reran the previous report's execution-time reproducer. Eleven ordinary-size battle batches, honoring every returned wait, with per-call latencies `[8,3,.4,1,.2,.2,.4,3,.4,1,3]` and a 0.5-second inter-batch gap: predicted maximum **30**, actual maximum **31** in a rolling minute. Five-call world batches with latency 8 seconds first and .4 seconds for the next seven: predicted **20**, actual **24**.

**Refutation:** constant .4-second latency produces 30/30. The probe records issued calls independently, executes all budget waits, and adds no unrequested calls. This is an allocator test, not a claimed live fight. The existing simulated-game assertions still use the allocator's own predicted ledger, so passing them does not refute this result.

**Required correction:** retain conservative accounting for issued/uncertain calls until actual timing permits releasing capacity; test actual dispatch times under variable latency. Keep the approved priority policy.

### 2. High — misaligned battle reads still bypass T+12 fallback

**Location:** `player/activities/battle.py:179–180`, `:240–244`.

The new empty-read path is distinct from the misaligned-column path. A dictionary containing both fighters but a short health column still returns another read unconditionally, bypassing the open turn's last-good-read deadline.

**Reproduced at c225ed36:** start the logged fixture on our turn, explicitly refuse both planned actions, then return two fighter IDs but one `curHealth` value at T+1, T+12, T+15, T+20 and T+60. Every resulting batch has **zero actions**, although the last valid read and unbanned emergency actions remain. A valid next-round read closes the old turn as **missed**.

**Refutation:** replacing the malformed reads with rate-limit refusals invokes the corrected fallback and sends Defensive Stance, then End Turn if the stance is refused. The new empty-read handling does not cover this separate branch. Rejecting malformed data is appropriate; bypassing the deadline indefinitely is not necessary to reject it.

**Required correction:** route unusable reads through the deadline-aware recovery path without overwriting the last valid state. The previous report's malformed-read reproducer runs unchanged at this SHA.

### 3. Medium — a waiting client can still overwrite its replacement

**Location:** `player/brain.py:286–311`, especially `:309–312`.

Relay ownership is checked before waiting, then an old private copy of `client.json` is written after the wait. A new handshake during that interval is overwritten. The one-brain lock does not serialize this client ownership transition.

**Reproduced at c225ed36:** use the actual client, `put`, and in-process answer path with an offline profile fixture. During the normal eight-second hunt hold, create a replacement relay. When the old invocation resumes it emits its scan batch and reinstates its own ID. The replacement receives **`STOP superseded: another relay has taken over`**. Only sleeping is replaced with a deterministic interleaving; `_await`, `_collect`, state writes and the brain lock are real.

**Refutation:** sequential supersession passes. The defect requires an invocation already waiting when replacement occurs. The prior report's real-client reproducer still runs unchanged.

**Required correction:** make ownership acquisition and publication safe against overlap; atomically revalidate ownership before publishing a batch. Test replacement during the response wait and the brain-side hold before adding scripted short-lived relays.

### 4. Medium — the proof read can trigger an old fight's potion inside a new fight

**Location:** `player/activities/battle.py:74–78`, `:177–178`; `player/activities/recovery.py:84–89`.

The proof profile can say `BATTLE` with a different battle ID, for example when a rematch starts before the brain observes the interval between fights. `_profile` marks the old fight as left but cannot open the new one while the old state exists. `_close` then clears battle state and creates a normal closing recovery batch. `after_fight` checks the old fight's HP but does not reject recovery when the current profile already says a new battle is active.

**Reproduced:** start fixture battle B1, answer its actions, and return an empty battle read. The brain correctly asks for a proof profile. Answer that requested profile with `status=BATTLE, battleId=B2`. Its next batch is **`item.consume`, `profile.getUser`**, while the character model already says B2/BATTLE and `world['battle']` is `None`. No opening read of B2 goes out. This wastes a recovery call and another relay round trip during the new fight, recreating part of the live failure the fix is meant to prevent.

**Refutation:** use the identical sequence with proof `BATTLE/B1` and there is no potion; use `AWAKE` and the closing potion is appropriate. These controls isolate the different-active-battle transition. The reproducer only answers calls the brain requested and uses no concurrent operator action.

**Required correction:** distinguish leaving combat from moving directly into another fight. Close/archive the old fight, retain/open the new battle identity, and suppress world recovery while that new fight is active. Add a rematch transition test alongside the existing empty-read tests.

Run from the frozen repository root:

```bash
python3 - <<'PY'
from player.tests.support import Rig, start_fight, battle_read, user
from player.tests.test_review import answers
for status, bid in [('BATTLE','B1'), ('BATTLE','B2'), ('AWAKE',None)]:
    r = Rig(); _, _, out = start_fight(r)
    out = r.tick(*answers(out), battle_read('B1', {}))
    assert 'profile.getUser' in r.calls(out)
    out = r.tick(user(status, bid=bid, hp=1000))
    print(status, bid, r.calls(out), (r.world['battle'] or {}).get('bid'))
PY
```

Observed: B1 stays active with battle/log reads; B2 gets potion/profile and no battle state; AWAKE gets the expected potion/profile.

## Rulings verified

RUL-152 is treated as approved authority, not reopened for confirmation.

| Ruling | Verification |
|---|---|
| Shared 30-call cap; reads/world give way first | Brief updated and aligned with the intended scheduling policy. The execution-time defect is finding 1, separate from the settled wording. |
| End Turn as last resort | Fallback remains after stance; its use passes through the planner finding event. No new policy approval requested. |
| Over 50M ryo asks | Default cap is 50M. Independent boundary checks: 50M from zero allows, 50M+1 asks; 49M already spent plus 1M allows, plus 1M+1 asks. This verifies the recorded cumulative-day interpretation. The 500k reserve remains. |
| PvP 2 may change; PvP 1 selected, never edited | Present in brief/design; AP2 equipment implementation remains unbuilt. |
| One level transfer per rolling 24 hours | Gate records `last`; after saving and recreating the brain it refuses at 86,399 seconds and allows at 86,400 seconds. No transfer was performed. This checks the gate for sequential issuance, not an AP2 activity that does not yet exist. |

RUL-151's rotation-on-growth and harvested-log permissions remain settled and unchanged.

## Verification and scope

| Check at c225ed36 | Result |
|---|---|
| Player unittest discovery, ResourceWarnings ignored as requested | **224 OK** |
| Allowlist/catalog unittest command | **46 OK**; existing ResourceWarnings in catalog helpers |
| Allowlist check | 93 endpoints; zero never-list violations |
| Allowlist report `--check` | Current |
| Four legacy pilot scripts | All exit 0; planner parity **4,000/4,000** |
| `rulings_index.py --check` | Current, 322 rulings |
| `player_size.py` | **3,142** production lines, 19 files; **3,282** test lines |

The first player test attempt lacked the newly tracked `.claude/agents/tnr-relay.md` in this review's sparse checkout. Adding that path and rerunning produced 224 OK. That setup failure is not a product finding.

The live-fix tests pass for retaining an ongoing battle after an empty read, requesting proof until it answers, keeping log identities when effect texts are short and filling them from whole effects, giving later accepted plans planning time, tracking first versus last send time, honoring unfamiliar refusal text, returning home/sleeping under normal controls, and counting unseen rounds separately. The broader gates, console, production wiring/unplug, archive, relay matching and crash/restart regression tests remain green. Findings above identify gaps beyond those successful examples.

Largest file: `battle.py`, 545 lines. Largest function: `_my_turn`, 42 lines, 18 branches. Ten functions exceed 12 branches: battle `_absorb` 13, `_my_turn` 18, `_no_read` 15, `_tick` 16; brain `_compose` 14; budget `turn_closed` 14; calls `ground_cols` 15; combat `plan_turn` 16; gates `do_not_attack` 15; relay `find_transcript` 13. The live handoff's 3,140/3,280 totals precede the final ruling's two-line increases. These remain AP6 complexity debt, not a new AP1 size gate.

## Live evidence and token decisions

Read the committed session counters at `duet/ai-player-ap1-live` @ `112aadbdcd60406f3bfc2fa46459c2d20fe7835c`, without contacting the game. They describe the old `583fe353` run, not successful play of this target.

Independently summed **69 batches, 15,925,397 input-plus-output tokens**, with initial context **118,190** and maximum **383,138**. These are logged token counts, not verified billing costs. The transcript evidence needed to validate cache accounting and exact connector replies is still pending.

The handoff's approximately **1,001k per fight turn** is reproducible as 12,013,399 tokens tagged with a non-null battle round divided by 12 distinct tagged rounds. The old console's **937,607** uses 14 groups, including two `round=null` groups, and a different numerator (13,126,493). These are different denominators; they should not be presented as comparable measurements without that definition. Five batches also have `in != context`, so “every batch is one model request” is an approximation, not what every recorded aggregate says.

The projected 5k birth context, light-poll savings and per-round restart savings are scenarios, not measurements of the corrected player. The prepared two-tool agent definition exists and matches the relay prompt; its actual starting context and connector availability on Duet's machine remain unverified. No headless model or connector check was run during this review.

The three outstanding choices remain decisions for the director:

1. Light polls: plausible savings, but prove the extra full-read round trip and refusal fallback against T+12/T+15/T+20; fix finding 2 first.
2. Scripted short-lived relays: verify headless connector availability on Duet's machine and fix ownership finding 3 before relying on frequent replacement. Rotation inside a fight would also need an explicit change to the current never-in-fight ruling.
3. His-turn opening archive: dropping it trades away evidence the approved opponent-model/archive design calls for. Keep the current contract until that tradeoff is explicitly approved; distinguish reading once per side from reading full state on every poll.

The three raw relay transcripts still need preserving by Duet. This review neither requested live access nor sent a message to Duet. Exact empty-response payloads, refusal texts, headless connector behavior, projected savings and live acceptance of this corrected SHA remain unverified.

## Return to Fable

Fix findings 1–4 and return a new frozen SHA with execution-time, malformed-read, overlapping-takeover and immediate-rematch tests. The approved rulings need no further confirmation. Keep token architecture decisions separate from these correctness fixes; do not claim the old live run accepts the new code.

No existing tracked file changed in the frozen review checkout; no implementation fix was made and no `fable/*` branch was modified. Test-created untracked artifacts were moved outside the checkout. The sole repository addition is this report on a separate ChatGPT review branch. **No live-game request was made.**
