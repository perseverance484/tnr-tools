# Recipe-aligned cache — native offline proof of the Silent Bastion one-of-two reward

**Verdict: PASS, with one integration finding (RC1) for the director.** On the current upstream engine, the approved `alt99_f4gate` Battle Pyramid, a quest-level one-of-two reward choice and native Weighted Cache opening work together offline. One cache offer appears after a real completion, exactly one card can be claimed, and it pays once under replay and concurrency. Opening the claimed cache grants one complete recipe-shaped bundle with a stored receipt. Failed, abandoned and recovering attempts create no offer and no cache. The Beacon is charged once, at `startQuest`, and never refunded (RUL-2026-10-16-003). No engine change was needed or made.

**Not approved by this proof:** the recipe shortlist, quantities, tier/roll weights, cache rarity/tradability, names, art and economy. Every cache, ingredient, bundle and weight below is **synthetic**.

- **Brief:** `docs/handoffs/RECIPE_ALIGNED_CACHE_NATIVE_OFFLINE_PROOF_BRIEF_20261016.md` at `chatgpt/silent-bastion-caches-claude-handoff-20261016@25d2b2e159d9fb9b0769db5483571e0db87991f6`.
- **Engine:** `studie-tech/TheNinjaRPG@0651b039a466516a8fe24fc13b56f60dea11b7eb`. This was upstream `main` when the proof ran, the same commit the brief names. It is 53 commits after the C99 topology pin `13d40c4`.
- **Graph:** `harness/silent_bastion_condensed99/graphs/alt99_f4gate.json`, sha256 `c70fad7a…ee20`, as in the coordination lock. It is used unchanged: 99 objectives, no reward-selection objective.
- **Harness:** `harness/recipe_cache_native_proof/` (README there). **Evidence:** `harness/recipe_cache_native_proof/results/`.
- **Live requests/writes:** 0/0. **Credentials:** none. **Engine modifications:** none.

## 1. What runs

The isolation is the same as the C99 proof: `git archive` export of the pin, frozen lockfile without lifecycle scripts, socket-only MySQL with `--network none` (upstream CI image), tests inside `unshare -rn`, placeholder environment. The fixture compiler, driver and checking runner are the committed C99 ones. The one harness change: `run99.ts` now starts a later attempt from the hero's carried pools instead of assuming full pools. The battle settles through the upstream test pattern.

Fixture (`engine/lib/cachefix.ts`):

- Two synthetic `CONSUMABLE` caches, `destroyOnUse:true`, `preventBattleUsage:true`, each with one `noncombatconsumereward`, `rewardMode:"weightedCache"`.
- Each cache has two tiers (Epic 75% / Legendary 25%, illustrative) and one roll.
- The bundles are 1–2 recipe-shaped entries per tier, built from six scratch `MATERIAL` ingredients.
- The quest is the `alt99_f4gate` record with **quest-level** `rewardMode:"choose"` and `rewardPickCount:1`. `content.reward.reward_items` holds two entries `{ids:[cache], number:100, quantity:1}`. **Nothing** is on `w.complete`.

| Gate | Command | Result |
| --- | --- | --- |
| Upstream preflight (12 suites: reward choice ×3, weighted cache ×2, Pyramid consequences, entry charge, run state, isolation, quest reset, quest run, persistent battle) | `run.sh` step 5a | **168 / 168 pass** |
| **S** — pure (`engine/rc_static.test.ts`) | `run.sh static` | **25 checks, 0 failed** |
| **F** — routers + MySQL (`engine/rc_flow.test.ts`) | `run.sh flow` | **2,229 checks, 0 failed** (8 tests) |
| C99 regression: the frozen `alt99_f4gate` S/D/R/E gates at this pin | `run.sh` step 5c | **52/52 tests; S 30, D 543, R 7,033, E 592 checks, 0 failed** |
| Deterministic re-run (fresh DB, `TNR_OUT=<scratch>`) | second full `run.sh` | **exit 0; all 6 evidence files byte-identical** |

## 2. Results against the brief

| Brief requirement | Result | Evidence |
| --- | --- | --- |
| Save and validate through real paths | **PASS.** `QuestValidator` and `verifyRewardChoiceForSave` accept the record (2 cards for 1 pick). The real editor `quests.update` saves it hidden, with 99 objectives, `choose` and pick 1. Both stored cache items pass `ItemValidator`. **Negative:** a single cache card for one pick is rejected at save. | S, F1 |
| No reward before completion; no auto-grant | **PASS.** After every division, and at `d.aftermath`, there is no offer and no cache. `w.complete` resolves the quest and writes **one** frozen offer: `pickCount:1`, cards `reward_items:0:<arsenal>` and `reward_items:1:<research>`. No cache is granted. | F2 |
| Claim Arsenal; replay and switch rejected | **PASS.** Picking both cards is rejected. The Arsenal claim grants 1 Arsenal, 0 Research, and consumes the offer. A replayed claim and a switched claim are both rejected and the totals stay unchanged. | F2 |
| Parallel claims; inverse pick | **PASS.** 5 parallel Research claims on a fresh completion: exactly one succeeds, giving 0 Arsenal and 1 Research. | F3 |
| Player-facing API view | **PASS (API).** `getPendingRewardChoices` returns both card names with amount and rarity. **Source-inspected only:** the Logbook and the Profile dashboard render `PendingRewardChoices` for any quest type (`app/src/layout/Logbook.tsx:78`, `ProfileDashboard.tsx:776`). Isolation is released at completion, so the claim can be made outside the run. No browser or Android check was performed. | F2 |
| Weighted opening: coherent bundle, receipt replay | **PASS.** `item.consume` with a `requestId` destroys one cache and grants exactly one configured bundle: all of that entry's items, nothing from another recipe or the other cache. A replay with the same `requestId` returns the stored response byte for byte and grants nothing more. One audit receipt records roll count, tier, entry index and the exact items. A new request on the emptied stack fails. **S:** 20,000 seeded draws per cache give one whole bundle each time, the Epic share within ±2% of 75%, and every entry reachable. A two-roll config sums two whole bundles. | F4, S |
| Concurrency, rollback, invalid config | **PASS.** Two distinct concurrent requests on one cache: one succeeds and grants one bundle. An injected grant failure rolls back (cache kept, nothing granted) and the retry succeeds once. A stored roll sum of 9,999 and a missing ingredient reference are both refused **before** consuming. **S:** roll ≠ 10,000, tier ≠ 10,000, a positive tier with zero entries, an entry with no items, 11 items in a bundle, quantity 101, more than 2,000 items worst case, and an empty display name are all rejected. | F4, S |
| Not usable in battle or inside the run | **PASS.** A claimed cache cannot be opened inside a later isolated attempt, either between floors or in a battle: "Complete or abandon your isolated Battle Pyramid…". | F4 |
| Failure and abandonment isolation | **PASS.** An Arakane loss closes the attempt uncompleted with no offer and no cache. Abandonment gives no offer and no cache. Neither refunds the Beacon. An attempt with recovery losses and resets in all four divisions (including two recovery losses) produces **no** offer before completion and **one** offer at completion. | F5 |
| Beacon at start (B1, approved) | **PASS.** Each attempt charges exactly one Beacon at `startQuest`, checked at every battle start of every attempt. No charge at the first battle or on retries. No refund on failure or abandonment, including an abandon before any fight. Three attempts used exactly three Beacons. | F2–F6, regression E2 |
| Negative control: cache on `w.complete` | **Confirmed hazard.** With both caches on `w.complete.reward_items` (mode `all`), completion grants **both** caches with no offer. This is why the brief forbids it. | F7 |
| Graph unchanged / no extra objective | **PASS.** 99 objectives, flow and save checks pass, no objective carries `reward_items`. The full C99 S/D/R/E suite still passes on `alt99_f4gate` at `0651b039`. | S, regression |

## 3. Finding for the director

**RC1 — a re-run started while a cache choice is unclaimed gets stuck, and its Beacon is lost (engine behaviour, content-only mitigation).**

Reproduction (F6):

1. Complete the Pyramid and leave the cache choice unclaimed.
2. `startQuest` admits a new attempt and charges a Beacon.
3. The player plays all four divisions. At `w.complete` the engine refuses with "Choose your reward from the previous completion of this quest first" (`REWARD_CHOICE_PENDING_MESSAGE`). The run stays at `d.aftermath`.
4. Claiming the first offer is refused while isolated: "Complete or abandon your isolated Battle Pyramid before starting outside activities."
5. The only way out is to **abandon** the second attempt. Its Beacon is not refunded (RUL-2026-10-16-003). The first offer can then be claimed exactly once.

No reward is duplicated and nothing is lost except that Beacon.

Content-only mitigations, for the director:

- (a) Entry and Logbook copy that says: "Claim your previous cache choice before starting a new expedition."
- (b) Accept the behaviour as is.

An engine-side fix (refuse `startQuest` while the same quest has a pending offer) would need a separate Lane A ruling. It is not proposed here.

## 4. Fixture limits and what was not tested

- Every cache, ingredient, bundle, weight and quantity is synthetic. The real shortlist in `docs/design/RECIPE_ALIGNED_CACHE_CANDIDATE_POOLS_20261016.json` was **not** used or validated. Its ingredient IDs are from an Oct-13 capture and need a fresh capture plus director approval.
- Battles are settled with imposed outcomes and pools, following the upstream pattern. No combat or AI was simulated here.
- Not tested: production data, browser/Android reward-choice UI, Pusher delivery, real item art, `validate.py` on a manifest (no manifest was produced), and anything live.
- Existing upstream unit and SQL suites are reported separately (preflight) from the new Bastion × choice × cache integration (S, F).

## 5. Reproduce

```bash
harness/recipe_cache_native_proof/run.sh        # needs git, bun 1.4.x, python3, unshare, docker
TNR_ENGINE_WORK=<existing export> harness/recipe_cache_native_proof/run.sh
```

Provenance is in `results/provenance.json`: engine pin, `bun.lock` and 11 engine source files by SHA-256, graph and brief SHA-256, every harness file's SHA-256, runtime versions and exit statuses. Raw random draws and receipts go to `*.timings.json` only.
