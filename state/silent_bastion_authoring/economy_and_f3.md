# Silent Bastion — candidate balance scenarios, reward economy and F3 farm impact

**Status: CANDIDATE ANALYSIS.** Nothing here is a balance freeze. The director owns stats, multipliers, reward values, rarity, tradability and economy.

The mechanics are LOCKED, and the native proofs pass on `studie-tech/TheNinjaRPG@0651b039`:

- Beacon at `startQuest`, once per attempt, never refunded.
- One-of-two cache choice after completion.
- 50% recovery fights.
- Medical sets 100%.
- Arakane defeat hard-fails the attempt.

## 1. Candidate stat ladder (all units level 100, rank JONIN)

Pools are not authored. The engine rewrites them as `(100 + 50·(level−1)) · poolsMultiplier` = **5,050 × poolsMultiplier** at level 100 (references/ai.md law 15). Stats are ratio weights scaled to the level-100 budget, multiplied by `statsMultiplier`, and capped in battle by rank.

| Tier | Units | statsMultiplier | poolsMultiplier | HP/CP/SP each | Regen |
| --- | --- | ---: | ---: | ---: | ---: |
| Division I regulars | Proving Proctor, Quartermaster, Prototype Lancer | 1.50 | 1.00 | 5,050 | 40 |
| Division I REG4 (elite, optional) | Calibration Duelist | 1.75 | 1.25 | 6,313 | 40 |
| Division II regulars | Archive Keeper, Containment Warden, Echo Subject | 1.75 | 1.25 | 6,313 | 40 |
| Division II REG4 | Failed Reconstruction Prototype | 2.00 | 1.50 | 7,575 | 40 |
| Division III regulars | Signal Adjutant, Staff Tactician, Honor Guard Commandant | 2.00 | 1.50 | 7,575 | 40 |
| Division III REG4 | Strategist's Aide-de-Camp | 2.25 | 1.75 | 8,838 | 40 |
| Division IV regulars | Sanctum Vanguard, Directive Herald, Last Watch Executor | 2.25 | 1.75 | 8,838 | 40 |
| Division IV REG4 | Order-Bearer of the Sanctum | 2.50 | 2.00 | 10,100 | 40 |
| Commander I | Master of Arms | 3.00 | 2.50 | 12,625 | 60 |
| Commander II | Replicant Zero | 3.00 | 3.00 | 15,150 | 60 |
| Commander III | The Grand Marshal | 3.25 | 3.00 | 15,150 | 60 |
| Commander IV | Supreme Commander Arakane | 3.50 | 3.50 | 17,675 | 60 |

**Anchor.** Master of Arms is set at Ghost Ship Captain parity (L100 JONIN, 3.0× stats, 2.5× pools, regen 60; the Sealwright precedent in `docs/RULINGS.md`). Each division then escalates. Arakane gets the largest pools so that The Last Directive (below 30% HP) actually fires; the director explicitly requires this. The combat-time stat cap means `statsMultiplier` is a weak lever at endgame (law 16); pools and kits do most of the work.

**Not done (per balance doctrine):** the calibration protocol (one declared-dummy anchor fight, then tier row-products; references/balance.md law 13). Gate A runs the real AI decision engine with real jutsu records but imposes no damage outcomes, so it is **not** a difficulty measurement.

**Attrition across a run (illustrative).** Pools carry between fights, so a 16–20 fight run should be winnable by an endgame build without full recovery: regulars chip, commanders spike. The only heals are Medical (100% at the chosen commander) and the 50% recovery checkpoint after a loss. That structure is approved; the numbers above are tuning knobs.

## 2. Completion reward (one of two caches)

- Proven natively, on the separate reward-proof branch (`docs/reviews/RECIPE_ALIGNED_CACHE_NATIVE_OFFLINE_RESULTS.md`):
  - one frozen offer per successful completion;
  - exactly one claim, under replay and concurrency;
  - coherent single-recipe bundles with receipt idempotency;
  - no offer on failure, abandonment or recovery loops.
- **Unapproved:** the recipe shortlist (`docs/design/RECIPE_ALIGNED_CACHE_CANDIDATE_POOLS_20261016.json`), the Controlled20 vs Strong Pyramid quantity model, tier/roll weights, cache rarity, tradability and art. The compiled candidate references the caches symbolically (`@item:bastion_arsenal_cache`, `@item:bastion_research_cache`); their weighted tables stay **BLOCKED** until the director chooses.
- **RC1 (from the reward proof):** a new expedition started with an unclaimed choice cannot be completed and must be abandoned, losing its Beacon. The candidate quest description already carries a "claim before you set out" line, which is the content-only mitigation.

## 3. F3 — repeat-farm battle income through recovery loops

**Observed natively:** C99 E9/E8 at 13d40c4, and again at 0651b039 in the reward proof's regression. Every won battle pays ordinary battle settlement (ryo + XP), including recovery fights and re-fought regulars, all on one Beacon. Loops are unlimited: losing never ends the run, except against Arakane. The quest reward is unaffected (one cache choice per completion).

Let `W` be the settlement for one ordinary win against that division's opponent. At the fixture level, one recovery win plus one REG2 win paid 64 XP plus randomised ryo (E8); real values depend on player and AI level.

| Loop (deliberate) | Fights per loop | Wins per loop | Income per loop | Notes |
| --- | ---: | ---: | --- | --- |
| **A. Checkpoint loop:** at the REG2 checkpoint, lose REG2, win the 50% recovery fight, repeat | 2 | 1 (recovery) | `W_rec` | Cheapest: two short fights. Recovery fights are REG1 copies, the weakest opponents in each division |
| **B. Commander loop:** win REG2 and REG3, lose to the commander, win recovery, repeat | 4 | 3 | `W_rec + W_reg2 + W_reg3` | Higher yield per loop, slower |
| **B′.** as B, plus REG4 (Protocol access) | 5 | 4 | `+ W_reg4` | |
| Normal clean run (reference) | 16–20 | 16–20 | `Σ W` once | One cache choice |

Because loops are unbounded per Beacon, the Beacon is an entry fee, not an income cap. Abuse is bounded only by fight time. The relevant comparison is **income per hour against other endgame farming**, and that needs real settlement values and fresh live data, which this offline package does not have.

### Options for the director (`scaleGains` is a per-battle 0–1 settlement multiplier, `validators/objectives.ts:420`)

| Option | Change | Effect on loop A | Effect on loop B | Effect on a clean run |
| --- | --- | --- | --- | --- |
| **O1** accept | none | unchanged | unchanged | unchanged |
| **O2** (minimal) | `scaleGains: 0` on the 8 recovery battles | **removed** | −1 of 3 wins | none (clean runs never fight a recovery battle) |
| **O3** | O2 + `scaleGains: 0.5` on REG2–REG4 | removed | roughly −2/3 | regulars pay half on the first pass too |
| **O4** | `scaleGains: 0` on every Bastion battle | removed | removed | no battle income at all; only the cache reward |

**Recommendation for consideration:** O2. It closes the cheapest loop without touching the intended first-pass income. Loop B stays, but it requires repeatedly beating three regulars and losing to a commander, which is slower than normal play. The compiled candidate leaves `scaleGains` unset (default 1) until the director rules. Before shipping O2–O4, the chosen value needs one native test confirming that a `scaleGains: 0` win still settles, counts as a win and pays nothing.

## 4. Other economy decisions still open

- Beacon: source (Ghost Ship), drop rate, rarity, tradability. Charge timing is locked.
- `maxAttempts` / `maxCompletes`: the validator maximum is 100. The candidate uses 100/100 so nothing blocks; lifetime repeatability is the director's call.
- Cache contents (§2) and whether non-crafters get value. See the targeting-problem analysis in `docs/design/RECIPE_ALIGNED_CACHE_PILOT_REVIEW_20261016.md`.
