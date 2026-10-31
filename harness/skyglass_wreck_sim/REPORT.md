# Skyglass offline simulation

## Rule cap and law-40 gates (2026-10-31, `fable/skyglass-rule-cap`): current

This section supersedes the final pass below for every AI rule list. It covers RUL-2026-10-31-066 item 1 (the 20-rule
cap), the director's law-40 gate decision of 2026-10-31, and RUL-2026-10-31-067 (the consolidation: Faded tier applied,
the rest measured for feasibility in §6). Zero live requests, no credentials; offline engine at the harness pin
`c86f43f4`.

### 1. The cap, and what the harness now enforces

- **Cap:** `AI_PROFILE_MAX_RULES = 20` (theninjarpg@3314d122 `app/drizzle/constants.ts:1933`).
  - Enforced in `ai.updateAiProfile` (`app/src/server/api/routers/ai.ts:87`: `input.rules.length >
    AI_PROFILE_MAX_RULES` returns "Maximum of 20 rules allowed"). Both builders push behaviour through that route
    (`builder_bundle.js` `aiProfPush`, Forge `profileUpdate`).
  - The same constant caps pet instructions (`validators/pets.ts:141`).
  - It counts the authored list only. The engine's backup rules and its appended end turn (`ai_v2.ts`) are added at
    battle time.
  - `createAiProfile` has no cap, but it only creates an empty profile.
  - Rule evaluation in `ai_v2.ts` is unchanged between the harness pin and 3314d122 (the only diff is the raid-boss
    give-up path).
- **Harness (`engine/rulecap.ts`):**
  - `assembleFloor` (every runner) throws on any enemy, ally or summon template over the cap.
  - Every spec writer checks its output before writing.
  - The static fallback audit reports `ruleCount` and flags a violation over the cap.
  - `--allow-over-cap` downgrades the failure to a warning, only to reproduce pre-trim rule sets.
  - Outputs carry a `ruleCap` block.
- **Law-40 gates (`engine/gates.ts`):**
  - Every `distance_lower_than` on a rule casting a shared-pool jutsu is set to the pool's `gate` (range + 1, from
    `32b_DATA_pool.json`), the value Forge's `kitProblems` requires.
  - Applied at battle assembly and in every spec writer, including the `{when, do}` summaries.
  - `--old-gates` keeps the old values. Outputs carry a `gates` block.
  - Non-pool jutsu keep their gates, as Forge does.
- **Independent check** (Python, Forge's rule): 122 rule lists in the specs and Wreck overrides, 0 over the cap, 0
  gate errors.

### 2. Every AI, old → new rule count

| AI (where it fights) | Old → new | What was merged or cut | Behaviour change |
|---|---|---|---|
| Core Horror, shared kit (endgame Wreck F4; Archive descent; Fall / Burning Heading copies; Steeping Horror) | 32 → 20 | Final-pass order kept; cut only follow-ups that (almost) never fired: Twin Kunai as the third follow-up after Collapse's and the Maw's marks (0 + 2 casts in 70 endgame appearances); the plain attacks after the two Rupture Field marks (6 casts: Rupture Field A is laid with Second Wind, leaving 20 AP), whose end turns stay; the three plain attacks below the marks (0 casts: a mark is always ready); the explicit end turn (the engine appends the same rule) | With no mark ready he ends his turn. Endgame signature 91.2% (old rules 91.8%). **Steeping fight:** his follow-ups carried that fight's damage: 5,464 → 2,331 dealt per fight, clear 77.5% → 95% (retune in §4) |
| Faded Core Horror (level-50 Wreck) | 32 → 20 | His follow-ups are spread over all four marks (final pass: Bilge Spit after Rupture Field A 53 times). So the plain attacks are hoisted above one end turn per mark; his first mark, Omen: Last Light (no condition), stays above them | All attacks are 60 AP and all marks 40 AP: at most one attack and one mark per turn, never two marks. For the other marks the attack now comes first (same pair). A Second Wind turn is Second Wind + Last Light, or Second Wind + an attack while Last Light cools down. Signature 100%, no idle turns |
| The Captain, shared kit (endgame Wreck boss; Captain's Watch; Fall press-on copy; Burning Heading ally) | 28 → 20 | The two after-mark blocks (Battle Trance, Second Wind, Final Command, Keelbind, end turn, once per mark) are folded into one tail below the marks, closed by the two mark end turns. Dropped "Second Wind (no mark ready)" (the tail's Second Wind serves it) and "close in (duel)" (3 casts in 70) | Phase 1 order exact. Transition exact: Steady + Gunwale + first mark in one round 95% (as before); 0 Broadside in phase 1. In a later mark turn Hold the Line can be the follow-up when the party stands 3+ hexes away (4 casts in phase 2 over 20 audited appearances). A phase-2 turn with no mark ready may open with Battle Trance. If a blast is lost (stunned to 80 AP) he may lay the other mark |
| Wayfinder, hunt variant (Watch duel; common-chart copy; Burning Heading duel) — *not in the ruling's list* | 23 → 20 | The minor-mark blast was stated three times with identical conditions, so the two repeats could never fire; they are removed. Also dropped the third Chart Mark focus (LOWEST_HEALTH_OPPONENT; 0 casts in 70). The shared Wayfinder kit (Wreck, Haul) is unchanged | Essentially none |
| Foundry Warden (Drowned Foundry; Reliquary / Rotted copies) | 21 → 20 | Explicit last end turn removed (the engine appends the same unconditioned rule) | None (exact) |
| The Crowned Captain (Crownhold D5) | 40 → 20 | Kept the phase structure, all four blasts, the throne walk and an end turn after each mark. Shardstorm B is phase 3's last mark, and the phase-3 end turn follows it, so it needs no end turn of its own. Cuts follow 22 traced solo fights with the old rules. Never cast: Keelbind, Ruin Refrain, Scorching Rend, Devouring Grasp, Wind Spear, Veilstep, Solar Bow. Also cut: all three Purging Stance rules, both Countermand rules, Stolen Form (15 casts, no damage), Cursed Thread Weave (6 casts), the after-mark basic attacks, the explicit end turn | No Purging, Countermand, Stolen Form or Hexweave. Solo 100% / 50% won (dodge on / off; old rules 100% / 48.3%). Phases begin at rounds [6, 10] (old [4, 12]) |
| Crown Armsmaster (Crownhold D2) | 30 → 20 | The turn ends after Whirlwind's and Racks Fall A's marks (their plain-attack follow-ups are cut). Racks Fall B is his last mark: it needs no end turn, and his own list follows it. The round-1 Racks Fall A rule goes: after the opening Fetters only 40-AP rules fit, and the plain Racks Fall A mark is the first of them. Also cut: the push/272 "Cataclysm on a debuffed player" rule (its plain Cataclysm stays); the explicit end turn | No plain attack in those two mark turns. After Racks Fall B: Cataclysm, Backlash Palm, Fighter's Poise or Shuriken Storm (was Backlash Palm / Shuriken Storm). Cataclysm no longer jumps ahead on a debuffed player |
| The Second (Crownhold D4) | 28 → 20 | After the Rows A mark: Sovereign Undertow, else end turn. Rows B is his last mark: no end turn, and his own list follows it (his push/272 Undertow drags a player 4+ hexes away). Cut: Piercing Judgment and Cataclysm as after-mark follow-ups; "Cataclysm on a stunned player" (the plain Cataclysm right below covers every case: exact); the explicit end turn | After Rows B, a player within 3 hexes is no longer dragged (already in the rows) |

Unchanged and within the cap: every other AI the harness builds.
- Hunt Skyglass Sentinel: **20** (at the cap).
- Replicant Zero 19; Sealwright (hunt and copies) 17; First Blade 16.
- Haul guards ≤ 17; Wreck crew 4-13; Crownhold regulars ≤ 18.
- The level-50 (Faded) Captain uses the shared Captain kit (20).

**Two trims that failed and were replaced** (results kept as `results/rulecap_Tfirst_*` and `_Tsecond_*`):
- **Core Horror, plain attacks hoisted above one end turn per mark.** Every Second Wind turn became Second Wind + a
  plain attack instead of Second Wind + a mark, and the short endgame fight lost its Maw: signature 92% → 28%, and
  53% with his first mark kept on top. The Second Wind heal lifts him back above 70%, so the phase-2 mark's condition
  fails. The level-50 version keeps this form, because his first mark has no condition.
- **Crowned Captain, cuts chosen from an older tuning file.** That trim kept the duel fillers he never casts, merged
  phase 2 into phase 1 and dropped Crownfall's end turn. Solo win (dodge on) fell 100% → 72%, and every clean and
  alert Crownhold chain was lost at him in about 5 rounds.

### 3. Measurements (same seeds and method as the final pass)

Columns:
- **Final pass:** d5957e79 at its params.
- **Gates only:** law-40 gates, pre-trim rules (`--allow-over-cap`).
- **Gates + trims:** this branch.

The last two columns use the RUL-2026-10-30-060 params: Watch Captain pools 3, Reliquary Sealwright 2 rows, War
top-up at D4/D5. Where RUL-060 changed a fight, a run with old gates and old rules at the RUL-060 params separates its
effect (in brackets). Watch phase-2 rounds are from the solo Watch.

TABLE_MAIN

**Haul** (no trims touch a Haul guard, so this is the law-40 gate effect alone). Exact runs, 40 seeds; "fit" = the
6ad2a102 payout fit (`results/fit_haul_summary.json`).

TABLE_HAUL

**Determinism and set pieces:**
- Wreck `--probe-check` on the endgame boss floor with pets: 2 seeds identical, also with the rule probe removed.
- Charts `--repro` on `burning@L100@3` (208 steps) and `steeping@L100@1` (58 steps), and Haul `--repro
  trophy@CLLCL@5` (170 lines): identical.
- **Unmarked set pieces: 0** in every run of this pass (`fallbackGuard`).

### 4. Verdicts and proposed retunes (for the director; not applied to design docs)

VERDICTS

### 5. Specs for the builders

`state/skyglass_build/` on this branch (its README gives provenance) holds:
- `build_spec.json`, `hunts_spec.json`, `hunts.params.json`;
- `charts_spec.json`, `charts.params.rul060.json`, `haul_spec.json`;
- `crowned_captain_spec.json`, `crownhold_spec.json`, `library_spec.json`.

All are at most 20 rules per AI and carry law-40 gates. `charts_spec.json` and `haul_spec.json` carry `fullRow` /
`fullProfile` (the former `specout_full.patch`, now committed). The level-50 copies are named "Faded <Name>".

**On `main`, replace every `state/skyglass_build/*.json` except `library_spec.json` and `charts.params.rul060.json`.**
None carries the proposed retunes (§4).

CONSOLIDATION

---

## Final pass (2026-10-30, `fable/skyglass-final-sim`) (superseded for rule lists by the rule-cap section above)

This section supersedes the per-harness reports (`REPORT_hunts.md`, `REPORT_charts.md`, `REPORT_crowned_captain.md`,
the Haul section of `README.md` and report 2 below) wherever they differ.

**Sources:**
- Merged branches: `origin/main` 87c96edd (rulings to RUL-2026-10-29-058), Wreck ce25fac8, hunts aac4a221, Crownhold
  035212ef, Haul b973ff28, charts f7694676.
- Engine: pin `c86f43f4`, live damage settings.
- Zero live requests, no credentials.
- Tables: `python3 tools/final_tables.py`. Raw: `results/final_*.json`.
- Player: L100 Kitsune JONIN + one modelled pet, dodge on/off. L50 for the level-50 Wreck and the commons.
- Every runner's output carries a `fallbackGuard` block: set-piece casts, and how many were cast without their marker.

### 1. Library-wide fallback fix (RUL-2026-10-29-046)

**Code:**
- `engine/fallback.ts`: `fixFallback`, the static per-phase audit `--audit-fallback`, the runtime guard, and
  `--no-fallback-fix` for the before case.
- Shared kits (`engine/kits.ts`, rebuilt `overrides/kits_*.json`): the last rule is the named basic attack.
- Profiles built from live rules (Haul guards, chart copies, the live Arsenal Keeper):
  - every `use_highest_power_*`, `use_random_jutsu` or `use_combo_action` damage rule becomes the basic attack;
  - `includeDefaultRules` is off, and the engine backup rules are restated without their highest-power rows.

**Static audit** (`results/final_fallback_audit.json`): enemies with a rule that can cast a set piece or blast
unmarked, before → after.

| Set | Before → after |
|---|---|
| Wreck endgame | 3/9 → **0** |
| Wreck L50 | 3/8 → **0** |
| Rare charts | 5/12 → **0** |
| Other charts | 13/30 → **0** |
| Haul | 11/15 → **0** |
| Crownhold | 0/21 → 0 |

No last rule is a free pick any more.

**Runtime:** 0 unmarked of about 11,300 set-piece casts across all final runs.

**Not changed (flagged).** These end on an end of turn with no basic attack: the immobile fuses and hazards, the Core
Horror, the Foundry Warden, Replicant Zero, the Steeping Horror, and every Crownhold record (push/272 rules end "move
→ end turn"). None has a free pick. Adding a basic attack would change tuned fights.

### 2-3. Wreck and the Captain's Watch with the fix

**Wreck:**
- **Endgame** (60 runs, pets, dodge): 60/60 cleared, **16.7%** runs with a wipe, **22.3 min** median (24.1 with AI
  animation). The boss wave wipes 10 of 70.
- **Level 50:** **10%** runs with a wipe, 18.5 min.
- **Dodge off:** endgame 0/30 (unchanged); L50 46.7% runs with a wipe.

**Captain's Watch** (40 seeds; shared Captain record with Steady the Helm and the basic-attack fallback):
- **No terms: 97.5% clear.**
- **Phase 2:** median **7 rounds** (p90 11). Phase 1: median 8.
- Reaches phase 2 in 97.5% of fights.
- With the Captain's term: 65-90%.
- Dodge off: 0%.
- **Transition order** (`results/final_audit_captain_endgame.json`: the endgame Wreck boss wave, 20 runs with pets):
  - Steady the Helm, Raise the Gunwale and the first Omen fire in one round in 95% of appearances.
  - Broadside is never cast in phase 1 (0 of 19 casts).
  - Phase 1 ends on the basic attack (63 casts).
  - Wreck phase 2: median 6 rounds (p90 8).

**Determinism:** same-seed reruns are identical, positions and pets included:
- charts `--repro` on `burning@L100@3`, `fall@L100@2` and `steeping@L100@1`;
- Haul `--repro trophy@CLLCL@5`;
- Wreck `--probe-check` on the endgame boss floor with pets: 2 seeds identical, and identical with the rule probe
  removed.

### 4. Rare charts (40 seeds, dodge on)

| Run | Clear |
|---|---|
| Buried Cache | **95%** (boss ~16% HP) |
| Foundry | **75%** |
| Archive, clean | **95%** |
| Archive, alarm 1 | **78%** |
| Archive, alarm 3 | **30%** |
| Watch | **97.5%** |

The Archive's Stonebound summon runs at 40% power (`echoPower` 40) with its own enemies-only Erupting Ground copy
`hunt-stonebound-erupting-ground`. The shared live jutsu is untouched (RUL-2026-10-28-026 items 2-3).

### 5. Common, Epic and Legendary charts

L100, 40 seeds, dodge on. Dodge off at 30 seeds in brackets.

| Run | Clear (dodge off) | Press-on won / reached | Base minutes |
|---|---|---|---|
| Low Tide | 100% (100%) | 40/40 | 2 |
| Night Watch | 100% (100%) | 40/40 | 2 |
| Sealed Reliquary | **92.5%** (40%) | 35/37 | 9 |
| The Fall | **85%** (0%) | 17/34 | 7 |
| Rotted Reliquary | **55%** (20%) | 8/22 | 5.9 |
| Burning Heading | **47.5%** (0%) | 19/19 | 6 |
| Steeping fight | **77.5%** (0%) | n/a | 2.3 |

At L50 (dodge on / off): Low Tide 100% / 100%, press-on 40/40 / 39/40; Night Watch 100% / 97.5%, press-on 36/40 /
16/39.

**The Fall: the Arsenal Keeper is the only fire source** (RUL-2026-10-29-057 item 5). The "Burning Deck" hazard is
removed.
- `chart-arsenal-keeper` is a copy of the live Keeper: his live kit with the fallback fix, immobile, pools 4.
- **30% innate damage reduction** (new).
- Three ember bands (drain 5% max HP per action) at rounds 1, 4 and 7, in the powder-magazine fight.
- He dies in a median round 16, after about 7 ember hits (~35% HP).
- Without his fire, the Fall is 100%.
- Damage reduction sweep (20 seeds): 0 → 95%, 20-25 → 90%, 30 → 75%. At 40 seeds, 30 gives 85%.

**Burning Heading made harder** (~68% → target ~55%).
- With the fire gone from its opening Core Horror fight, the old copy (pools 5.5, 2 rows) cleared 100%.
- At 2 rows the duel is a deterministic race: pools 6 gives 0%, and 5.75 is not storable.
- Adopted: **pools 5.5, 3 rows, 65% damage given down → 47.5%**.
- At 40 seeds: 60% → 35%, 70% → 72.5%, 80% → 100%.
- Sweeps: `results/final_charts_sweeps.json`.
- The no-dodge file ran the 60% build.

**Steeping** (RUL-2026-10-29-055): one Steeping Horror fight, scaled to the player, at full pools. **77.5%**.

**Crownhold with heal top-ups** (16 chains per route, pet, reads 0.85; Healing full, clean +35%, War +20% with whole-
fight War Rite, alarm +15%):

| Route | Clear | Where runs end |
|---|---|---|
| Healing | **93.8%** | |
| Clean | **56.3%** | the Crowned Captain |
| Alarm | **37.5%** | the Crowned Captain |
| War | **6.3%** | the D4/D5 fourth regulars, before the top-up |

**Press-on verdicts** (keep only if a player would notice it gone, RUL-2026-10-28-026 item 10):

| Run | Room | Won / reached | Verdict |
|---|---|---|---|
| Low Tide | proposed room | 100% everywhere | **cut** |
| Night Watch | the Second Watch | L50 90%, L50 no dodge 41% | **keep** |
| Archive | probe: Crown Archivist + Seal Charge | 92%, ~27% HP | **cut** (or harden) |
| Watch | probe: Wayfinder + Deck Warden | 87% from ~22% HP | **keep** |
| Sealed Reliquary | First Blade echo | 95% | **cut** (or harden) |
| The Fall | the Captain | 50% | **keep** |
| Rotted Reliquary | Replicant Zero | 36% | **keep** |
| Burning Heading | First Blade | 100%, ~0 HP | **cut** |

### 6. The Haul, no steeping (RUL-2026-10-29-056)

`results/final_haul_exact_dodge.json`: exact runs, 40 seeds, after the fallback fix.

| Page | Sensible CLC: clear / EV M | Greedy clears (LLLCC / CLLLC) | Best named route vs sensible |
|---|---|---|---|
| Trophy Hold | 95% / 7.98 | 30% / 25% | CCCCC **122%** |
| Bone Store | 90% / 7.56 | 25% / n/a | CCCCC 109% |
| Snare Room | 80% / 8.24 | 27.5% / 30% | LCC 109% |
| Overgrown Stores | 92.5% / 7.49 | 37.5% / 30% | LLLCC 105% |
| Ore Vault | 70% / 7.35 | 17.5% / 32.5% | CCCCC 110% |
| Bloom Cellar | 92.5% / 7.49 | 32.5% / 30% | sensible is best |

- Sensible mean **7.69M**.
- Greedy clears are 25-37.5%. The exception is the Ore Vault's LLLCC at 17.5%; its CLLLC is 32.5%.

**Every legal path** (`results/final_haul_base_dodge.json`, state-merged, 24 seeds). Its top routes were re-run
exactly, 40 seeds (`results/final_haul_exact_top_a.json`, `_b.json`). Routes above 120% of sensible:

| Page | Route | Clear | EV | % of sensible |
|---|---|---|---|---|
| Trophy Hold | CLLCC | 62.5% | 11.0 | **138%** |
| Trophy Hold | CCCCC | 80% | 9.8 | 122% |
| Snare Room | LCXLC | 65% | 11.4 | **139%** |
| Snare Room | LLL | 65% | 10.2 | 124% |
| Bloom Cellar | LLL | 97.5% | 10.2 | **137%** |
| Bloom Cellar | LLCC | 72.5% | 9.9 | 133% |

The Bone Store (best 116%), Overgrown Stores (115% merged) and Ore Vault (110%) stay inside.

**Cause:** the fallback fix took the guards' free picks (`use_highest_power_action` could cast their blasts), so the
locker-heavy fights got easier.

**Fix:** re-fit the payout points with `tools/haul_payout_fit.py` against the exact top routes. A first offline fit
moves the Snare Room to 120% (steps 4.4/1.0/0.9/0.9/3.5, locker 2.4), but cannot pull the Trophy Hold's CLLCC or the
Bloom Cellar's LLL under 120% with points alone. Those two need step-2/3 locker fights hardened by one guard, as on
the Snare Room (RUL-2026-10-29-045). Not adopted: payout is the director's.

### 7. Economy: dedicated player, 12-hour weekend

Built by `tools/economy.py` from `results/final_economy_inputs.json`. Output: `results/final_economy.json`.
- Loot tables §2-§5d.
- Players press on half the time, and every Epic chart is steeped while Rot allows.
- Picks are spread evenly over the non-token cards; "typical" takes the token on half of the picks that offer it.

**Typical weekend:**
- **23.3 Wreck clears** (30.9-minute cycle with their charts).
- Chart runs: 8.7 Common, 15.2 Rare, 0.07 Epic (the rest are steeped), 1.56 tainted, 0.99 Crownhold.
- **1.26 Haul runs.**
- Core Rot: 5.9 gained, all spent on about 2 steeps.
- **Skyglass Tokens 3.0**, from 5.1 opportunities. A player who always takes the token gets **5.5**; one who never
  does, 0.08.
- Boss-variant tokens (1 / 2 / 4%): **0.15**.
- Without steeping: 1.54 Epic runs, 3.5 tokens.

**Haul pages:** for 1.5 runs a weekend, use **Wreck 2.4% / Rare-chart endings 1.5% per page** (both ×1.19), or the
Wreck alone at 2.5%.

**Not modelled:** breaking the Archive seal (Rot ×2), and the once-per-player Wreck drops.

### 8. Hit / miss and recommended fixes

| Item | Target | Measured | Verdict | Fix |
|---|---|---|---|---|
| Fallback fix | 0 unmarked | 0 violations, 0 of ~11,300 casts | hit | optional: basic attack before end turn on bosses and Crownhold |
| Endgame Wreck | ~22 min, ~17% | 22.3 min, 16.7% | hit | none |
| L50 Wreck | ~10% | 10% | hit | none |
| Watch phase 2 | ≥6-7 rounds | 7 (p90 11) | hit | none |
| Watch clear | ~80% | 97.5% | over | Captain pools 2.5 → 3, or drop givenDown 10 |
| Buried Cache | boss ~20% HP | ~16% | hit | none |
| Foundry | ~80% | 75% | hit | none |
| Archive routes | clean > alarm | 95 / 78 / 30% | hit | none |
| Sealed Reliquary | ~80% | 92.5% | over | Sealwright copy rows 1 → 2 |
| The Fall | ~80% | 85% | hit | Keeper 30% DR adopted |
| Rotted Reliquary | ~55% | 55% | hit | none |
| Burning Heading | ~55% | 47.5% | hit (40-seed noise ±15) | adopted 3 rows + 65% |
| Steeping | ~75% | 77.5% | hit | none |
| Crownhold | all routes clear | War 6.3% | miss | War Rite top-up at D4 and D5, or no fourth regular on the War route |
| Haul sensible / greedy | ~7.5M / 22-38% | 7.69M / 25-37.5% | hit | none |
| Haul max path | ≤ ~120% | Trophy CLLCC 138%, Snare LCXLC 139%, Bloom LLL 137% | miss | re-fit points; one more guard on the Trophy/Bloom step-2/3 lockers |
| Haul per weekend | ~1.5 | 1.26 | miss | Wreck 2.4%, Rare endings 1.5% per page |
| Tokens | 2-3 / ~5 | 3.0 / 5.5 | hit | none |

---

# Skyglass Wreck offline simulation: report 2 (2026-10-28)

All fights are engine-native and offline: the game source at origin/main `c86f43f4`, an exported copy, battles in memory.
There were zero live requests. Inputs are committed captures plus two values the director read in game: the live damage
settings and the solo-Captain anchor. Raw numbers are in `results/live_*.json`, `results/calibration_solo_captain.json`
and `results/probe_mechanics.json`. Report 1's runs (code-default damage settings, gear stand-ins) remain in
`results/` without the `live_` prefix; they are superseded.

## What changed since report 1

- **Live damage settings** are the default for every battle (`data/dmg_config_live.json`, written to
  `battle.extraState.dmgConfig`). The values are curve 2, gen_weight 1, advantage_min 0; the code defaults are 1.6, 2
  and 0.01.
- **Real player build** (director's "average", the endgame party member):
  - Level-100 JONIN with stats at the JONIN caps.
  - The **full Kitsune armour set**: all 6 slots, from push/204 (`tnr_results_1792629744565.json`). The capture holds
    every set piece (Mask, Armor, Gauntlets, Belt, Pants, Tabi-Shoes; Pants-F is an identical alternate), so no piece
    is missing.
  - The set is worn as real item rows through the engine's item path. Realised in battle: +50 points damage given and
    +30 points damage reduction in the pre-battle gear pools, +1,200 max HP (static, 20 rounds), 4× increasestat 20%,
    and absorb 30% for 5 rounds.
  - **9 PvE-usable jutsu at the Jonin level cap 25.** The Elite Jonin cap of 30 applies only to ELITE JONIN-rank jutsu,
    so it does not apply here. All 9 load in battle (none gated); Fire/Wind elements:
    - Chakra Overflow
    - Typhon Burst (AOE)
    - Tempestual Fury (AOE)
    - Burning Coil
    - Gale Force Blast
    - Scorching Sun Strike
    - Wind Style: Sky Dragon
    - Phoenix Flame Strike
    - Stunning Jab
  - The strongest raw PvE entries are not used:
    - Torturing Flame Coil needs Scorch, a bloodline element.
    - Sonic Slash and Soul Shackles deal a flat (static) 100 damage, which is weak at endgame.
- **Reference build:** `noarmor` is the same build without the set.

## Solo-Captain anchor check (60 seeds; one player vs the live The Captain; plain QUEST battle)

Director anchor: "good players beat it in 8-10 rounds, some fewer; a tough fight".

| Build | Wins | Rounds (wins) | HP left at the win | Losses |
|---|---:|---:|---:|---|
| **average (Kitsune set)** | **60/60** | **8** (every seed) | **71.6%** | none |
| noarmor | 0/60 | - | - | dies in round 3; Captain at 81% HP |

- **Speed:** the real build matches the anchor's 8-10 rounds, at the fast end.
- **Survival:** it is more comfortable than "a tough fight", ending at ~72% HP. That makes it mildly stronger than the
  anchor on survival, not far stronger. It was not tuned down.
- **Why there is no spread:** the solo fight is almost deterministic. The only randomness is the spawn tile.
- **What the set does:** the Captain's hits drop to about 1/5. The set's +30 damage reduction stacks linearly with the
  engine's base 50, so 80% of damage is removed.

## Endgame runs (live settings; 30 seeded runs per party)

Minutes are medians at 10 / 15 / 20 s per player turn. AI turns cost 0 s, plus 30 s per floor battle. For runs that never
clear, minutes are the time until the run is abandoned after 4 wipes.

| Layout | Party | Clears | Runs with a wipe | Rounds (median) | Min @10 / 15 / 20 s |
|---|---|---:|---:|---:|---|
| Live 16 waves (push/263) | average | 0/30 | 100% | 40.5 | dies on F1W2 (118/120 attempts) |
| | noarmor | 0/30 | 100% | 8 | dies on F1W1 |
| candidate_target20 (5 waves of 2, crew pools 1.5, Crowned pools 4) | average | 30/30 | 10% | 21.5 | 12.0 / 16.8 / 21.5 |
| candidate_target20_soft (+ crew bonus damage +150%) | average | 30/30 | 0% | 21 | 12.0 / 16.8 / 21.5 |
| director_layout (as given, crew unchanged) | average | 0/30 | 100% | 84 | dies on F3W1 (62/62) |
| director_layout_v2 (RUL-2026-10-28-003 + Core Rupture edit) | average | 0/30 | 100% | 91 | dies on F3W1 (81/82) |
| | noarmor | 0/30 | 100% | 8 | dies on F1W1 |
| **dense_a** (mine: 1 wave of 3-4 per floor) | **average** | **30/30** | **13%** | **30** | **16.1 / 22.9 / 29.7** |
| dense_b (director layout + dense_a stats) | average | 30/30 | 10% | 41 | 21.7 / 31.3 / 40.8 |
| **dense_b_v2** (director_layout_v2 + dense_a stats) | **average** | **30/30** | **0%** | **38.5** | **20.9 / 30.1 / 39.3** |
| | noarmor | 0/30 | 100% | 36 | dies on F2W2 / F3 |

`noarmor` fails every layout.

**Stat changes in dense_a and dense_b, all storable values:**
- Crew AIs: `poolsMultiplier` 1.5 (7,575 HP), and the innate damage given replaced by a single +150%. Captured is
  +350-450% across stacked rows.
- Crowned Captain: pools 4.
- Sealwright: pools 2.5 (12,625 HP).

### Per-wave rounds, average party (median [min-max]; clears / attempts; wipes)

**director_layout_v2** (crew as live):

| Wave | Enemies | Result |
|---|---|---|
| F1W1 | DW x3 + Seal Charge | 9 [3-13]; 112/118; 6 wipes |
| F2W1 | DW + Seal Charge x2 | 4 [3-6]; 112/112 |
| F2W2 | DW x3 | 8 [4-13]; 82/112; 30 wipes |
| F3W1 | Sentinel + First Blade + DW | 6; 1/82; **81 wipes** |
| F4W1 | DW x2 + Oathkeeper | 9; 3/3 |
| F4W2 | Wayfinder + Core Horror | 0/3 |

Unchanged crew stats end the run at floor 3. The party reaches it on ~31% HP, because pools refill only between floors.

**dense_b_v2** (same layout, tuned crew stats):

| Wave | Rounds | Party HP lost % |
|---|---|---:|
| F1W1 | 6 [3-7] | 24 |
| F2W1 | 3 [3-4] | 3 |
| F2W2 | 7 [4-8] | 15 |
| F3W1 | 5 [4-6] | 33 |
| F4W1 | 5 [4-6] | 26 |
| F4W2 | 5 [3-6] | 11 |
| F5W1 | 6 [4-8] | 16 |
| F5W2 | 5 [4-6] | 31 |

Floor totals are 6 / 9 / 5 / 9 / 11 rounds. All 30 runs clear, with no wipe.

**dense_a:**

| Wave | Enemies | Rounds | Wipes |
|---|---|---|---:|
| F1 | DW x3 + Seal Charge | 6 [3-8] | 0 |
| F2 | Oathkeeper + DW x2 + Seal Charge | 6 [3-8] | 0 |
| F3 | Sentinel + First Blade + DW | 5 [3-6] | 0 |
| F4 | The Captain + Wayfinder + DW | 4 [3-6] | 0 |
| F5 | Crowned + Sealwright + Core Canister x2 | 9 [6-11] | 4 |

13% of runs wipe once.

### Reading against the target (15-20 min, about 1 run in 5 wipes once)

- **dense_a:** 23 min at 15 s per turn and 16 min at 10 s; 13% of runs wipe. Closest to target on both time and risk.
- **The director's layout** (8 waves) costs ~38-41 rounds even when tuned (dense_b_v2 ≈ 30 min at 15 s, 21 at 10 s),
  and it is safe at that tuning (0% wipes). Reaching 15-20 min at 15 s per turn needs ≈20-27 rounds, i.e. 5-6 waves or
  lower crew HP.
- **"Two-enemy waves are light work" is confirmed:** in target20 they take 3-4 rounds each. 3-enemy waves take 5-7 rounds
  at pools 1.5.

## Wave-2 opener fix (`round_lower_than 2` rules on wave-2 units)

Windlash Focus has cooldown 4. Fire counts are per appearance of the wave-2 unit.

| Variant | F2W2 Deck Warden x3: never / once / 2+ | F4W2 Wayfinder: never / once / 2+ |
|---|---|---|
| as live (round < 2) | 100% / 0 / 0 (303 of 303 never) | 100% never (dense_b) |
| (a) first, no condition | 0 / 32-49% / 51-68% | 0 / 100% / 0 |
| (b) first, gated distance_higher_than 5 to CLOSEST_OPPONENT | 92-94% / 6-8% / 0 | 100% never |

- **(a)** always fires on arrival, then again every 4 rounds while the unit lives. Waves last 5-7 rounds, so Deck Wardens
  usually cast it twice.
- **(b)** almost never fires. Wave-2 units spawn after the players have advanced to within 5 hexes.
- To get "exactly once on arrival", (a) needs a cooldown at least as long as the wave. Alternatively, gate it on the
  unit not yet having the buff (`has_effect increasedamagegiven` below its total), since the opener is self-buff IDG.

Data: `results/live_director_layout_opener_*.json`, `results/live_dense_b_opener_*.json`, field
`ruleFireDist`. On the as-given director layout the party never reaches F4, which is why dense_b carries the Wayfinder test.

## Mechanics probes (`results/probe_mechanics.json`, `engine/probe_mechanics.ts`; 3 seeds each)

The setup is one average player vs one probe enemy, with the Deck Warden row carrying only the probe jutsu. Rule 0 casts
the probe jutsu; the engine backup rules stay on. All jutsu are real captured records.

### 1. Movement jutsu on an AI

**Verdict: AIs can use movement jutsu.**
- The `ai_v2.ts` filter that drops move/summon jutsu applies only to ids containing `user_`, i.e. auto-combat humans.
- **Replacement Technique** (range 1, cd 2):
  - At EMPTY_GROUND_CLOSEST_TO_OPPONENT it fires every time it is off cooldown (3 casts in 6 rounds) and hops one hex.
  - At CLOSEST_OPPONENT it **never** fires: the player's occupied tile is not EMPTY_GROUND, and the engine rejects the
    pick and falls through to the next rule.
- **Body Flicker** (range 5, move + AOE damage 20):
  - At EMPTY_GROUND_CLOSEST_TO_OPPONENT it fires (2 per 6 rounds), crosses up to 5 hexes and lands beside the player
    (one cast hit the player for 245).
  - At CLOSEST_OPPONENT it fires once and **lands on the player's own tile** (3/3 seeds). On its next turn the enemy finds
    no valid action and the engine's give-up path kills it (`curHealth = 0`, `ai_v2.ts` "exhausted and has to give up").
  - Cause: the `move` tag (`tags.ts` `move`, ~l.2439-2443) sets the target coordinates unconditionally. Its comment
    promises a nearest-free-tile fallback that the code does not do.
  - **Do not target movement jutsu at an occupant.**

### 2. Summon jutsu on an AI

**Verdict: AI summons work** (the captured Hell Hound record, aiId changed to Seal Charge / Core Canister, cast at
EMPTY_GROUND_CLOSEST_TO_OPPONENT).
- **Firing:** fires once in round 1 and spawns 1 unit on the chosen empty tile in range, which was 1 hex from the
  player in these seeds.
- **The summon:** HP = the effect's `aiHp` (3,000). It lives `rounds` = 2 rounds, then leaves.
- **It acts on its own AI profile:**
  - The summoned Seal Charge waited 2 rounds, then fired Core Rupture in round 3. That dealt 5,234 to the player plus a
    stun, and destroyed itself.
  - The Core Canister only waited, since its own rule gate never held.
- The engine loads summon templates through `processUsersForBattle`'s `summonTemplateCache` (a DB read live). The
  harness pre-seeds that cache from the captured AI rows.

### 3. Ground AOE with a damage effect lasting 2+ rounds

Jutsu: Drowning Mire (PvE: damage 15 + IDT 15, 2 rounds, circle). Toxic Pool is PVP-only and the engine filters it out
of QUEST battles even for AIs.

**Timing:**
- Damage lands **in the cast round** on everyone on the 14 cells, the caster included: the AI hurt itself for 1,842.
- It then ticks **at the start of each affected unit's turn** while the unit stands on it: rounds +1 and +2 for
  `rounds 2`.
- Stepping onto another cell of the pool applies it again.

**Leaving the pool:**
- **Stepping off stops it.** The player who walked off in round 3 took no tick in round 4. The ground effect does not
  follow the unit.
- A COORDINATE target on the player's tile behaves the same as EMPTY_GROUND_CLOSEST_TO_OPPONENT once the caster is in
  range.

### 4. Barrier

Jutsu: Adamantine Fortress (AOE_LARGE_WALL_SHOOT, range 1).
- **Casting:** the AI casts it when gated to a player within 2. The wall is a 6-9 cell line through the targeted empty
  tile, lasting 2 rounds; seed 1 drew a full column.
- **Player response:** the players' auto-combat profile never attacked a barrier in these seeds. It kept attacking the
  enemy, which stayed reachable around or beside the wall.
- Players do carry the engine's backup rule (attack BARRIER_BLOCKING_CLOSEST_OPPONENT), but it is last in the list.

### 5. Clone

Jutsu: Clone Technique (range 2, rounds 2).
- **Appearance:** the clone appears on the tile with the caster's full HP (12,625).
- **Behaviour:** it acts on the caster's rule list (walked in, basic-attacked).
- **Damage:** it deals very little in this probe (31 per basic attack). The cause was not traced.
- **Lifetime:** it expires on schedule, absent from round 4 on.

## Faithful vs approximated (changes from report 1)

**Now engine-faithful:**
- Live damage settings.
- Real armour through the item path and the engine's gear pools.
- Real level-25 PvE kit with element gating.
- Summons through the engine's own template cache.
- Mini-boss retry rule (a wipe on F4 retries F4).

**Still approximated:**
- Players are driven by auto-combat with a declared rotation.
- No bloodline, keystone or weapon on the player.
- Seeded spawn tiles.
- The hazards' new rules from the encounters doc are not applied; v2 changes only the layout and Core Rupture.
- The old reference tiers' gear knobs go through one synthetic ARMOR row. The engine realises percentage damage-given
  above 100 on that row as 100, so `strong`/`elite` damage given is effectively +100. Reference only.
- Per-wave rounds count the spawn round, so neighbouring waves overlap by one round. Floor totals are exact.

---

# Addendum (2026-10-28, later): the 6-wave cut, the engine's damage-row cap, telegraph probes

## A finding that changes how "bonus damage" is set

**The engine caps every percentage effect row at 100.** `app/src/libs/combat/power.ts:4-7` (`getEffectPower`) returns
100 for any `calculation: "percentage"` effect above 100.

- A single innate `increasedamagegiven` row above +100% gives exactly the same damage as +100%. A Deck Warden's Tide
  Bolt hit for 95 / 191 / 191 with a row of 0 / +150% / +1000%. Whole runs with +150%, +250% and +350% rows were
  identical to the decimal.
- Several rows multiply, because each applies as `damage *= 1 + p/100` (`process.ts` damage packet, in-battle increases).
- The captured crew's "+350-450%" was really 4-5 stacked rows: ×2 ×2 ×2 ×1.5 ≈ ×12.
- The "single +150%" trims used above (target20_soft, dense_a/b, dense_b_v2) were therefore effectively one +100% row.
- Design rule: **express bonus damage as a number of +100% rows** (×2 each), or a final partial row.

## director_6wave (final layout; live damage settings; average party)

Layout: F1 Deck Warden x3 + Seal Charge; F2 Skyglass Sentinel + First Blade + Deck Warden; F3 Oathkeeper + Wayfinder +
Deck Warden; F4 Core Horror solo (stage boss, mini-boss room); F5 wave 1 Deck Warden x3, wave 2 The Captain + Sealwright.
Core Rupture v2 (AOE_CIRCLE_SPAWN, range 5, pierce 180; self-destruct and 2-round stun kept).

| Run | Clears | Runs with a wipe | Rounds median [range] | Min @10 / 15 / 20 s (+30 s per floor) |
|---|---:|---:|---|---|
| 1. dense_b_v2 trims as they are; Core Horror pools 3 (`overrides/director_6wave.json`) | 30/30 | 0% | 29 [27-31] | 16.0 / 22.8 / 29.5 |
| **2. tuned (`overrides/director_6wave_tuned.json`, 40 runs)** | **40/40** | **15%** (every wipe on F5W2) | **26 [23-51]**, 25 when no wipe | **13.9 / 19.6 / 25.3** |

**Rounds per wave:**

| Wave | Run 1 | Run 2 | Run 2 party HP lost % |
|---|---:|---:|---:|
| F1 | 6 | 4 | 21 |
| F2 | 5 | 4 | 35 |
| F3 | 5 | 4 | 28 |
| F4 Core Horror | 4 | 5 [5-6] | 24 |
| F5W1 | 4.5 | 4 | 18 |
| F5W2 Captain + Sealwright | 6 | 6 [3-8] | **87** |

In run 2 the boss wave is the hardest by far and holds all 7 wipes in 47 attempts.

The superseded first 6-wave layout (F2 Deck Warden x2 + Seal Charge x2; F4 Oathkeeper + Wayfinder + Core Horror) is in
`overrides/director_6wave_layout1.json` / `results/live_director_6wave_layout1.json`. It ran with the dense_b_v2 trims:
30 rounds, 23.1 min at 15 s, no wipes.

**Settled figures (run 2; all storable, applied through `scaleEditedAi`):**

| Enemy | poolsMultiplier | HP | Bonus damage (innate increasedamagegiven rows) |
|---|---:|---:|---|
| Deck Warden, Skyglass Sentinel, First Blade, Oathkeeper, Wayfinder | 1.0 | 5,050 | 2 rows of +100% (×4) |
| Core Horror (stage boss) | 5 | 25,250 | 2 rows of +100% (×4) |
| The Captain | 2.5 | 12,625 | 3 rows of +100% (×8) |
| Sealwright | 2.5 | 12,625 | 3 rows of +100% (×8) |
| Seal Charge | as captured (level 70) | 3,550 | none; Core Rupture v2 |

Stats and kits are as captured.

**Tuning path** (scratch runs, 30-40 each; minutes at 15 s):

| Crew pools | Crew rows | Boss wave rows | Wipe rate | Rounds | Min @15 s |
|---:|---:|---:|---:|---:|---:|
| 1.0-1.25 | 1-2 | 2 | 0% | 24-26 | 19-20.5 |
| 1.0 | 2 | 2 + 0.5 | 5% | - | - |
| 1.0 | 2 | **3** | **15%** | - | - |
| 1.0 | 2 | 4 | 33% | - | - |
| 1.0 | 3 | 3 | 43% | - | - |
| 1.0 | 3 | 3, boss pools 3 | 70% | - | - |

Core Horror at pools 3 fell in 4 rounds; pools 5 gives the asked-for 5-6.

## Telegraph probes (`engine/probe_telegraph.ts`, `results/probe_telegraph.json`)

Setup: a stationary probe boss (Deck Warden row, includeDefaultRules false, rules end in end_turn) and one player who
only ends turns. Positions are set after assembly.
- The synthetic jutsu use the captured Drowning Mire record as the shape donor, changing only target, method, range,
  cooldown, AP and effects.
- Damage tags carry `friendlyFire: "ENEMIES"`.

### 1. Ground-only telegraph

**Visual-only.** A GROUND / AOE_CIRCLE_SPAWN jutsu with only a `visual` tag (rounds 2):
- It lays a persistent ground effect on all 7 cells, with its `staticAnimation` kept, counting down 2 → 1 → gone.
- It creates no user effect on the player standing in it, and causes no HP change to the player or the caster.

**Zero-impact tag.** `increasepoolcost` at power 1, or 0, behaves the same: a 2-round ground effect, no HP change, no
persistent user effect.

So a pure `visual` telegraph works.

### 2. Two-step sequencing

**The marker type matters.** `decreasepoolcost` is stored with a negative power (−1 in battle). `has_effect` sums power
and needs `>= threshold` (`ai_v2.ts`, `has_effect` branch), so a decreasepoolcost marker **never** matches; the
detonation never fired. A positive marker works: `increasepoolcost` 1 on SELF.

**Timing.**
- **If the telegraph leaves AP:** the marker is present immediately, so the detonation fired **in the same turn**. That
  is not a telegraph.
- **If the telegraph and the detonation each cost 100 AP:**
  - Round N: telegraph and marker.
  - Round N+1, on the boss's turn: the marker is still present (`increasepoolcost:1:r1`) and the detonation fires.
  - This holds for marker rounds 1 and 2.
- **Why a 1-round marker survives:** it is applied `castThisRound`, so the first round transition does not count it down
  (`util.ts` `alignBattle`, the round-progress block).
- **A 2-round marker** stays one more round; the boss would detonate again unless the detonation's cooldown is ≥ 2.
- **Ground mark:** the 2-round visual is still on the ground when the detonation lands.

### 3. COORDINATES patterns

**CASTER origin, ALL selection, radius-2 ring:**
- The AI cast both the telegraph and the detonation with rule target **SELF or CLOSEST_OPPONENT, and jutsu range 0 or 5**.
  All four combinations fired; a CASTER-origin pattern ignores the clicked tile.
- Telegraph and detonation hit the **identical 12 cells** when the caster has not moved.
- **The caster's own hex is not hit:** it is not in the offsets.

**Offsets are column/row, not hex** (`targeting.ts` getTargetTiles, COORDINATES branch: `coordinate + origin.col/row`).
- A ring computed for a caster on row 5 stays a true ring on any column of an odd row, i.e. at (7,5) as well.
- On an even row (6,4) the same offsets give hex distances 1 and 3 for 4 of the 12 cells.
- Store one offset set per row parity, or keep the boss on rows of one parity.

**BATTLEFIELD origin, EXCLUDE 3 safe tiles:**
- It hit all 117 other tiles.
- A player on a safe tile (2,2) took nothing; a player on an unsafe tile was hit.
- The caster's tile **is** in the pattern, but the caster took no damage (`friendlyFire: ENEMIES`).

### 4. Grid and spawns

**Grid:** a dungeon floor battle (`QUEST`) at level ≥ 50 is **12 × 10** (`util.ts` `getDefaultBattleSizes`).

**Spawn cells** (`participants.ts` `getBattleSpawnLocations`):

| Side | Cells | Count |
|---|---|---:|
| Players | columns 3-4, rows 1-7 | 14 |
| Enemies | columns 8-9, rows 1-7 | 14 |

**Placement:**
- The opening placement is random among those cells (`routers/combat.ts` processUsersForBattle, `secureRandomInt`).
- Later waves take the **free enemy spawn cells in list order**: column 8 rows 1 → 7, then column 9. If those are full
  they use any free cell (`encounters.ts` `advanceEncounterWave`).

### 5. Summoning an existing AI record

Test unit: the Crownhold Proving Proctor (`1iJF8VBietrfvxJd_ZhFS`). It is built from the push/272 manifest data, with
its combat stats from the live readback in `tnr_results_1792984876132.json` (695,650 each) and jutsu records from the
captures.

**It works:**
- The summon appears with **HP = the effect's `aiHp`** (6,000 in the probe).
- It lasts the effect's `rounds` (3), then leaves.
- It acts on **its own rule list**: rule 0 Minor Overflow, then rules 1, 2, 3 in order, hitting the player.
- Its stats are its record's, rescaled to the caster's level and multiplied by the summon power %
  (`tags.ts` `summon`: `scaleUserStats(newAi, "ai")`, then `* perc`).

**Only one at a time:**
- **Two summon tags in one cast still give one summon.**
- **Recasting while it lives gives nothing;** a new one appeared only after the first expired.
- Cause: the one-live-summon-per-controller cap in `summon()` (`hasLiveSummon`).
- So the Crowned Captain's Recall can field one summoned regular at a time. Two at once need two casters, or a wave
  spawn.

# Report 3, part A (2026-10-28): the real endgame kits, tuned

Scope: every endgame dungeon copy built with the kit and priority rules from `SKYGLASS_WRECK_ENCOUNTERS.md` and
`SKYGLASS_BOSS_FIGHTS.md` sections 1-2 (The Captain, the Core Horror), the new dungeon-only jutsu, a dodging auto-player,
and tuning to the director's targets. Part C (Crowned Captain) moved to a separate agent; nothing Crownhold-related was
edited. Offline only, zero live requests; engine pin c86f43f4.

Files: `engine/kitlib.ts` (builders; every jutsu through the live `JutsuValidator`, every rule through `AiRule`),
`engine/kits.ts` (the kits), `engine/build_kits.ts` (writes `overrides/kits_endgame.json` and `build_spec.json`),
`overrides/kits_endgame.params.json` (the tuned knobs), `engine/probe_boss.ts` + `results/probe_boss.json` (new probes),
`results/kits_endgame.json` (60 runs, dodging on), `results/kits_endgame_nododge.json` (30 runs, dodging off).

## Result (average party, live damage settings, 60 seeded runs, dodging on)

| Runs | Cleared | Runs with a wipe | Wipes | Rounds median [p10-p90] | Clean clear | Min @10 s | Min @15 s | Min @20 s | @15 s + AI 1.5 s |
|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|
| 60 | 60 | 21.7% (13 runs) | 17: 16 on the boss wave, 1 on floor 1 | 26 [23-53] | 25 | 14.2 | 20.0 | 25.8 | 21.3 |

| Wave | Enemies | Rounds median [min-max] | Wiped here / reached | Party HP lost | HP left at the end |
|---|---|---|---:|---:|---:|
| F1 | Deck Warden x3 + Seal Charge | 3 [1-5] | 1/77 | 45% | 79% |
| F2 | Skyglass Sentinel + First Blade + Deck Warden | 3 [2-5] | 0/76 | 26% | 98% |
| F3 | Oathkeeper + Wayfinder + Deck Warden | 3 [2-6] | 0/76 | 30% | 94% |
| F4 | Core Horror (stage boss) | 5 [4-5] | 0/76 | 5% | 119% (Kitsune pools) |
| F5 W1 | Deck Warden x3 | 3 [2-4] | 0/76 | 26% | 98% |
| F5 W2 | The Captain + Sealwright | 7.5 [5-17] | 16/76 | 43% | 56% |

**Dodging off** (same records, 30 runs): 2 of 30 runs clear within 3 wipes; the boss wave wipes the party in 115 of 117
attempts (party HP lost 97%), and the Core Horror takes 31% of the party's HP instead of 5%. The marks are the fight.

**Dodging** (harness auto-player): 579 turns started on a marked hex (or off a star during the Maw); 526 (91%) reached
safety with at most 3 one-hex moves; 50 had no free safe hex within 3 steps (mostly the Maw's three stars); 3 were rooted
or stunned.

## Tuned figures (`overrides/kits_endgame.params.json`)

| Dungeon copy | Pools | HP | +100% damage rows | Notes |
|---|---:|---:|---:|---|
| Deck Warden, Skyglass Sentinel, First Blade, Oathkeeper, Wayfinder | x1.0 | 5,050 | 2 | unchanged from the 6-wave tuning |
| Seal Charge | as live | 3,550 | none | Core Rupture v2 (live record) |
| Core Horror | x4 | 20,200 | 2 | was x5: about 5 rounds, as the fight doc says |
| The Captain | x2.5 | 12,625 | 4 | was 3 rows |
| Sealwright | x2.4 | 12,120 | 3 | below the Captain, so ally targeting picks him (below) |

Move powers: Collapse 160, Rupture Field 140 (+30 pool), Maw of the Deep 200 + 1-round stun, Splintered Grasp 100 + wound,
Bilge Spit 70 + poison, Broadside 110, Ship's Bell 50 + push 3 + 1-round stun, Ward of Command 80% damage reduction
(2 rounds, recast every 2), Chain Hook 45, Oath of Stillness 35, Skyglass Aegis 1,500-HP shield + 20% absorb, Mending Seal
heal 20% + cleanse, The Core Rebuilds heal 20% + 50% damage, once. Wipe lever: Ward of Command's reduction (70% gave
12% of runs wiping, 80% gave 22%).

## Acceptance checks

| Enemy | Signature rule(s) | Fired in % of appearances | Idle turns after round 2 |
|---|---|---:|---:|
| Deck Warden | Chain Hook | 76 | 0% |
| Seal Charge | Core Rupture (either rule) | 88 | 0% |
| Skyglass Sentinel | Skyglass Aegis | 92 | 0% |
| First Blade | Raijin's Spear / Shuriken Storm / Numbing Senbon on the lowest-health player | 85 | **96%** |
| Oathkeeper | Oath of Stillness | 96 | 0% |
| Wayfinder | Chart Mark | 90 | 0% |
| Core Horror | Maw of the Deep (mark or detonation) | 82 | 0% |
| The Captain | Broadside (any) | 97 | 0% |
| Sealwright | Ward of Command | 100 | 1% |

Idle turn = a turn with nothing but moves or an end of turn, from the enemy's third round in its wave. First Blade fails
by the letter: it usually dies in round 2, and the few turns it reaches round 3 with are spent walking to the
lowest-health player across the deck. Openers fire once per appearance (cooldown 99, unconditional first rule).
The doc's "no floor wipes the party more than 1 run in 10" conflicts with the director's "about 1 run in 5 wipes, on
the boss wave": the boss wave wipes 16 of 76 attempts (21%). Each wipe also sends the party back to floor 1, so the p90
time is 39 min.

## Answers to the fight-design probes (`results/probe_boss.json`)

1. **Two-marker chain: yes, in order**, once the markers are a type outside the shared cooldown (below). Round N: a 60 AP
   mark (marker A), then in the same turn the 40 AP follow-up on `has_effect A` (pull 3, marker B); round N+1 the 100 AP
   detonation on `has_effect A+B`; round N+2 a plain beat on the detonation's beat marker. Used for Undertow.
2. **Weakness on SELF: yes, a 1-round window.** `weakness` x3 on every stat and general type, 1 round, cast by the boss:
   the player's next hit did 8,809 against 2,457 for the same jutsu outside the window (x3 on top of the increased
   damage taken); the window covers each player's next turn only. A `cleanse` on SELF in the same jutsu strips it, so
   Exposed Seam's detonation carries no cleanse. Used: Maw of the Deep applies it (ch_exposed).
5. **Barriers: only when fully blocked.** With a gap in the wall, the auto-player walks around. With the path fully
   blocked, the engine's appended backup rule (highest-damage action on `BARRIER_BLOCKING_CLOSEST_OPPONENT`) basic-attacks
   the wall (3,000 HP fell to 1,340 in 5 rounds), while ranged jutsu still reach the boss through it at 50% absorb. Live
   players will do better; in the harness Raise the Gunwale is a speed bump.

Also probed: **Chain Hook's same-cast root does not cancel the pull** (pulled 3 hexes and rooted, in either row order),
so it stays one jutsu.

## Engine findings that change the recipes

- **Shared cooldown (GCD).** A jutsu whose effects include a `SHARED_COOLDOWN_TAGS` type (barrier, buffprevent, cleanse,
  cleanseprevent, clear, clearprevent, consume, siphon, debuffprevent, drain, increasepoolcost, moveprevent, pierce, poison,
  seal, stun, summon, vamp) locks every other jutsu of the caster sharing that type for 3 rounds (`applyActionCooldowns`,
  `SHARED_COOLDOWN_ROUNDS = 3`). So:
  - the approved `increasepoolcost` self marker works for **one** marker jutsu per boss; a second marked set piece is then
    locked. The kits use `increasecooldown` with no `actionsAffected` (no effect on play; not a GCD type; storable at
    1 round, which `increasepoolcost` is not: its schema minimum is 2 rounds). A 1-round marker is present on the
    boss's next turn only, so no stale marker re-fires a detonation;
  - the beat after a phase-1 detonation uses a second marker family (`increaserange`, no actions affected);
  - stun moves lock each other: Ship's Bell, Final Command, Ruin Refrain, Sovereign Fetters; pierce moves too: Raijin's
    Spear and Shuriken Storm (First Blade got Numbing Senbon as a third option).
- **GROUND jutsu land only their damage.** A stun or push row on a GROUND AoE does nothing; on target `CHARACTER`
  (rule target SELF) the same pattern stuns and pushes players, spares the caster and the safe hexes. Detonations that
  stun or push are `CHARACTER`; Rupture Field's phase-2 eruption stays GROUND so it can leave a lingering pool.
- **Rings are `AOE_SPIRAL_SHOOT`** (disc of radius `range` minus the caster) and arena patterns are BATTLEFIELD
  coordinates, so **no pattern depends on row parity**.
- **Visual marks last 1 round:** cast in the boss's turn, shown through every player's turn, gone as he detonates. A
  2-round mark outlives its detonation and misleads. Visual ground effects at 0 rounds stay in the battle state
  (harmless to play; worth checking how the client draws them).
- **Range is capped at 5** by the validator: Chain Hook (doc 6) and Chart Mark (doc 7) are range 5.
- **`increasecooldown` only touches basic actions.** Oath of Stillness is +2 cooldown on Move and Replacement Technique
  for 2 rounds; it cannot slow jutsu.
- **Mid-battle ids were unseeded.** Clones, summons and effects get nanoid ids (crypto.getRandomValues), and with a clone
  on the field (Afterimage Decoy) the battle's course depended on them: the same seed gave different outcomes, and
  `--probe-check` failed. The harness now seeds that entropy per run (`seedEntropy` in `sim.ts`: its own generator, not
  Math.random, and a fresh nanoid pool), and `--probe-check` passes on `kits_endgame.json` (both seeds identical, with
  the rule probe on and off). Results committed before this point were produced without it (their layouts had no
  clone; their probe-checks passed).
- **Ally targets tie-break on turn order.** `HIGHEST_MAX_HEALTH_ALLY` takes the first unit on a tie, so Ward of Command
  and Mending Seal reach the Captain only while his maximum HP is above the Sealwright's (hence x2.4).

## Doesn't work as designed / deviations

- **The Captain:** Battle Trance and Great Bell Toll are not in the 11-jutsu kit. Last Stand at the Helm is a dungeon
  copy of Battle Trance; Ship's Bell (the doc's newer move) takes Great Bell Toll's place. His kit is 27 jutsu (the 11
  plus copies with his battle lines and the set pieces); whether the Forge caps an AI's equipped jutsu is untested.
  In a 7-round fight his lower duel rules (Stolen Form, Suppression Writ, Second Wind, Counter Stance, Ruin Refrain,
  Unraveling Strike, Explosive Tag Cataclysm, Windlash Focus) almost never fire.
- **Core Horror:** with dodging he is the safest floor (5% party HP), and 5 rounds show 2-3 set pieces: Collapse (and
  Undertow) whenever players hug him, Maw of the Deep from round 3, then The Core Rebuilds. Rupture Field, its
  phase-2 pools and Maw II rarely appear before he dies. He stays where he spawns (columns 8-9), not mid-hold. Bilge
  Spit is range 5 (doc 4) so he always has a reply.
- **Undertow** pulls a random player at least 4 hexes away (there is no "farthest" target).
- **Mending Seal** is cast on cooldown even at full health (no ally-health condition exists).
- **Seal Charge walks** (doc rule 3), although the floor note says hazards do not move.
- **Captured ids:** Core Rupture v2 is referenced as the live record (`nCQETf-HNnbRec1OSY2-R`); every other changed or new
  move is a `dg-*` dungeon copy. The `dg-*` ids are placeholders; `build_spec.json` says to remap rule `jutsuId`s.

## build_spec.json (endgame section)

9 AIs (stats, pools, level, multipliers, effect rows, jutsu list, ordered rules with notes, signature rules,
`insertAiSchema` check: all ok) and 60 jutsu records (59 new or copied, plus Core Rupture v2 referenced), each with
target, method, coordinateTargeting, range, cooldown, actionCostPerc, effects, battleDescription (the fight doc's
battle-log lines) and animation placeholder ids (tg_heavy, tg_control, tg_linger, tg_safe, dt_linger, ch_collapse,
ch_rupture, ch_maw, ch_bile_spit, ch_claw, ch_enrage, ch_undertow, ch_exposed, cp_bell_toll, cp_command, cp_broadside,
cp_gunwale, plus mark-sigil, chain-hook-hit and skyglass-pane for crew moves with no id in the animation spec). All 60
pass `JutsuValidator`. Images are placeholders copied from the shape donors.

# Report 3, part B (2026-10-28): the level 40-60 version

Same arcs as the endgame, with level-50 copies (ids `dg-*-l50`) and lighter kits. Built by the same code:
`build_kits.ts --version lvl50 --params overrides/kits_lvl50.params.json` writes `overrides/kits_lvl50.json` and the
`lvl50` section of `build_spec.json`. Results: `results/kits_lvl50.json` (60 runs), `kits_lvl50_nododge.json` (30),
`kits_lvl50_bounds.json` (level-40 and level-60 parties, 30 each).

## Player model (level 50) and its assumptions

The committed harvests hold no player at levels 35-65 (I searched every capture), so the model comes from the engine's
own formulas rather than a recorded player:
- CHUNIN, level 50.
- Stats: the level-50 budget from `scaleUserStats(..., "player")`, spread evenly: 106,177 offence, defence and each
  general.
- Pools: `calcHP/CP/SP(50)` = 2,550 each.
- Kit: 8 CHUNIN PvE-usable jutsu at jutsu level 15 (Harden Fist, Aqua Barrier, Rejuvenating Chakra, Stunning Jab,
  Shattering Strike, Chakra Palm, Resounding Crescendo, Iron Fist).
- No gear, no elements, no bloodline.
- The same dodge rule as the endgame party.
- Bounds: level 40 (jutsu level 12) and level 60 (jutsu level 18) use the same model.

The model is the weak point of this version. A real level-50 player who trains stats past the level budget, or wears
gear, is much stronger. One real level-50 capture would make this tuning trustworthy.

## Layout and kits

| Floor | Wave 1 | Wave 2 |
|---|---|---|
| 1 | Deck Warden + Seal Charge | none |
| 2 | Skyglass Sentinel + First Blade | none |
| 3 | Oathkeeper + Wayfinder | none |
| 4 (stage boss) | Core Horror, solo | none |
| 5 (boss) | Deck Warden x2 | The Captain (no Sealwright) |

Lighter kits (rules dropped from the endgame copies):
- Deck Warden: no Quick Strike.
- Sentinel: no Counter Stance, no Rigging Snare.
- First Blade: no stealth, no Shuriken Storm, no Numbing Senbon.
- Oathkeeper: no Opening Strike.
- Wayfinder: no Keelbind, no decoy. Chart Mark also falls back to the closest player, because the crew live about
  2 rounds.
- Core Horror: one phase of set pieces. No Undertow, no phase-2 cycle, no pools, no second Maw. The Core Rebuilds stays,
  and the Maw opens the fight so the short fight shows it.
- The Captain keeps two phases (Last Stand, faster Bell, three-row Broadside), with Broadside ahead of the Bell. He has
  no Gunwale (no Sealwright to protect) and keeps only Final Command, Keelbind and Second Wind from the duel kit.

The new jutsu are the endgame records (same `dg-*` ids, listed again in the `lvl50` section).

## Tuned figures (`overrides/kits_lvl50.params.json`)

| Copy | Level | statsMultiplier | Pools | HP | Rows |
|---|---:|---:|---:|---:|---|
| Crew | 50 | 1 | x1 | 2,550 | +100% damage x1; +100% damage taken x2 |
| Seal Charge | 50 | 1 | as live | 2,550 | none |
| Core Horror | 50 | 1 | x5 | 12,750 | +100% damage x2; +100% damage taken x1 |
| The Captain | 50 | 1 | x3 | 7,650 | +100% damage x3; +100% damage taken x1 |

**Why there are damage-taken rows.** `insertAiSchema` holds `statsMultiplier` and `poolsMultiplier` at 1 or more. So a
level-50 copy has at least 2,550 HP and 53,093 in every stat. That is still more than this level-50 party clears in the
target time: without the rows, crew floors take 3-8 rounds and the run takes about 35 rounds. Innate `increasedamagetaken`
rows (100% each, capped per row, rows multiply) are the remaining storable lever. The alternatives are lower-level copies
(level 40 gives 2,050 HP) or a stronger player model, and both are the director's call.

## Result (level-50 party, 60 runs, dodging on)

| Runs | Cleared | Runs with a wipe | Rounds median [p10-p90] | Min @10 s | Min @15 s | Min @20 s | @15 s + AI 1.5 s |
|---:|---:|---:|---|---:|---:|---:|---:|
| 60 | 60 | 0% | 18 [16-20] | 10.5 | 14.5 | 18.5 | 15.0 |

| Wave | Rounds median [min-max] | Party HP lost |
|---|---|---:|
| F1 Deck Warden + Seal Charge | 2.5 [1-4] | 24% |
| F2 Sentinel + First Blade | 2 [2-3] | 8% |
| F3 Oathkeeper + Wayfinder | 2 [2-3] | 7% |
| F4 Core Horror | 5 [3-10] | 16% |
| F5 W1 Deck Warden x2 | 2 [2-3] | 7% |
| F5 W2 The Captain | 5 [4-10] | 33% |

- Signature rules fire in 78-100% of appearances. Idle turns after round 2 are 0% for every enemy except the Seal
  Charge, which rarely lives into round 3.
- Dodging: 78% of the 363 threatened turns reached safety. The level-50 party has less AP to spare.
- **Dodging off:** 25/30 runs clear and 57% of runs wipe. The Core Horror wipes 41 of 66 attempts.
- **Bounds.** A level-60 party takes 13 rounds and 10.8 min, with no wipes; the Captain dies in about 2 rounds, before
  his set pieces. A level-40 party clears 3 of 30 runs: the Core Horror wipes 91 of 114 attempts and the Captain 20 of
  23. With this player model the version cannot serve both ends of 40-60. Gating it at about 45+, or a softer
  Core Horror and Captain for the low end, is a director decision.

# Report 4 (2026-10-28): shared library, one kit per enemy, pets, retune

Supersedes the tuned figures, kit notes and build_spec notes of report 3 parts A and B. It also corrects report 3's
statements that the grid is pointy-topped and that "no pattern depends on row parity" (see Geometry).

Offline only, zero live requests, engine pin c86f43f4. Commits on `fable/skyglass-wreck-sim` (local, not pushed):

| Commit | What |
|---|---|
| 4bd5356a | the library |
| 5f6c3edb | library fixes |
| ad379117 | Ward of Command and First Blade fixes, virtual clock, pets |
| c301632b | pet-placement determinism |
| 23e3a45f | minor marks, crew wiring, endgame retune |
| 422c0508 | every blast detonates once marked |
| dff3a89a | patterns on the engine's real grid |
| next | the results of this report |

## What changed

### Shared set-piece library

`engine/library.ts` writes `library_spec.json`: 34 NEW records, all passing `JutsuValidator`.

| Group | Count | Records |
|---|---:|---|
| Marks | 10 | Omen: Ring, Binding Ring, Rows A/B, Scatter A/B, Lines, Seal Lines, Last Light, Last Light Binding |
| Shared blasts | 7 | one per shared mark |
| Bespoke signatures | 6 | Maw of the Deep, Quench, Command Absolute, Crownfall, Broadside, Ship's Bell |
| Shared lowered guard | 1 | Lowered Guard |
| Crew additions | 6 | Chain Hook, Oath of Stillness, Chart Mark, Skyglass Aegis, Mending Seal, Ward of Command |
| Minor-mark pairs | 4 | Splash and Short Line (2 marks, 2 blasts) |

- Each mark puts its own 1-round primed-marker type on the caster. All 12 marker types are outside the shared-cooldown list.
- `results/probe_library.json` holds the probes:
  - each mark and its blast fire in order;
  - two marks coexist on one caster;
  - the minor pairs work as designed;
  - dodged players are not hit;
  - the engine geometry checks.

### One kit per enemy

- Both Wreck versions use the same jutsu and the same ordered rules per enemy (`build_spec.json` → `sharedKits`). Only stats, pools and damage rows differ per version.
- The Captain keeps the live Crowned Captain records unchanged. Hold the Line is live Unbroken Command; Last Stand is live Battle Trance.
- `build_spec.json` marks each jutsu LIBRARY, WRECK-NEW (Raise the Gunwale only) or LIVE (live id, unchanged).
- Counts: 24 library records used by the Wreck, 1 Wreck-new, 29 live.

### Every blast detonates once marked (422c0508)

- A CHARACTER cast is valid only when some character stands on a pattern tile (`util.ts isValidMove`).
- So with everyone stepped off, the AI had no valid cast. Ring, Ship's Bell, Rows B, Lines and Seal Lines then never went off.
- Pure-damage blasts are now GROUND:
  - Ring, Rows A/B, Lines, Crownfall, Broadside, Splash and Short Line (Scatter already was).
  - Ground damage resolves as an instant hit on whoever stands there (`process.ts`, enemies only).
  - So they erupt on the marked tiles even when nobody is left.
- Blasts with stun, lock or push rows stay CHARACTER, because GROUND lands only damage:
  - Seal Lines and Ship's Bell include the caster's own hex, so the cast is always valid. Their rows hit enemies only.
  - Maw, Quench and Command Absolute cover the whole field except the stars.
- Probe with every player dodged off: all 10 boss pairs and both minor pairs are cast and hit nobody.
- Exception: Last Light hits 2 of 5 players in that probe, because 3 stars cannot hold 5 players.
- **Side effect:** GROUND damage also strikes a barrier on an empty marked tile. The Captain's Broadside and Rows B now chip his own Raise the Gunwale when a marked row crosses it.

### Geometry (dff3a89a)

The engine grid is FLAT-topped with odd columns shifted down (`getBattleGrid`, honeycomb `Orientation.FLAT`, checked with the engine's own `grid.distance`).

| Column | N | S | NW | NE | SW | SE |
|---|---|---|---|---|---|---|
| even | (0,-1) | (0,+1) | (-1,-1) | (+1,-1) | (-1,0) | (+1,0) |
| odd | (0,-1) | (0,+1) | (-1,0) | (+1,0) | (-1,+1) | (+1,+1) |

- Diagonal neighbours depend on **column** parity.
- There is no straight west; a row is a zigzag chain of neighbours.
- Report 3 and library 5f6c3edb assumed pointy-topped hexes with row parity. The Crowned Captain harness found the result: Lines / Crownfall and Seal Lines ran near-vertical, and the Binding Ring disc was skewed.
- Rays and discs are rebuilt on column parity. Records use the union of both parities; exact per-parity sets are exported (`PATTERNS.linesByColumnParity`, `sealLinesByColumnParity`).
- `probe_library` lists the exact hexes each pattern covers from thrones (8,4), (8,5), (9,4) and (9,5), using the engine's `getTargetTiles`. Every ray step is an engine neighbour.
- From (8,5), Lines / Crownfall covers 19 hexes: the row west of the throne plus the NW and SW rays.

### Library fixes (5f6c3edb)

- Scatter A and B are complementary halves that cover the arena outside the three stars.
- Every blast has cooldown 2. Seal Lines hits enemies only.
- **LOCK replaces stun and seal** on Command Absolute, Ship's Bell and the Seal Lines blast:
  - elemental seal;
  - +10 AP per action (timecompression);
  - +2 cooldown on Move and Replacement Technique.
- None of these types is in the shared-cooldown list, so the Captain's own stun and seal moves can no longer lock his signature. The signatures no longer stun, so **this needs director confirmation.**

### Ward of Command fix

- Found by the hunts harness: the damage-reduction row resolved to the caster, so the Sealwright warded herself and never the Captain.
- The row now targets the chosen ally (`INHERIT`). A trace shows `decreasedamagetaken@The Captain`.
- Report 3's part-A wipe rate came from an 80%-reduced Sealwright, not from the intended kill-order puzzle.
- With the fix, the same parameters wiped **5%** of runs instead of 22.5%: players kill the Sealwright (round 6), then the Captain.
- The boss wave was retuned: the Captain has 4 damage rows and x2.8 pools.

### First Blade

His shared rules end with an explicit end turn, so a turn with nothing usable never reaches the engine's give-up path.

### Pets (`--pets`)

- No pet record exists in the committed captures. Each player brings a modelled mid-rank companion:
  - pet rank is half the owner's maximum: a JONIN owner gets rank 5 (level 30), a CHUNIN owner rank 3 (level 15);
  - stats at half the caps of the matching character rank;
  - COMMON / ASSAULT, no jutsu, the engine's default pet rules;
  - they enter through the engine's own pet path and sit beside their owner.
- An endgame companion has 1,550 HP and basic attacks of about 22. Pets mostly add bodies: they absorb hits and stand on marks. They do not dodge.

### Determinism

- **Virtual clock.** The engine's 60 s round timer (`calcActiveUser`) and its `updatedAt` stamps read the wall clock. On a loaded machine the same seed could end a round early. The harness now runs a virtual clock: a fixed epoch per run, +1 s per action.
- **Pet placement.** The engine draws spawn cells with unseeded node:crypto. A pet not yet re-seated kept its engine-derived cell and could block another pet's hex. All pet cells are now cleared first.
- **`--probe-check`** now also compares positions. It passes with pets on both versions (seeds 1 and 2 identical, also with the rule probe removed).

## Minor marks (RUL-2026-10-28-024)

| Pair | Mark / blast ids | Pattern (caster-anchored) | Marker | Power | Player / modelled pet hit |
|---|---|---|---|---:|---|
| Splash | `lib-omen-splash` / `lib-blast-splash` | 3 x 3 block centred two hexes west of the caster | increaseheal 1% | 58 | 143 / 1,025 of 1,550 (66%) |
| Short Line | `lib-omen-short-line` / `lib-blast-short-line` | the row, 3 hexes west of the caster | lifesteal 1% | 65 | 161 / 1,149 (74%) |

**Recipe.**
- Mark: 40 AP, cooldown 3, GROUND, tg_heavy visual.
- Blast: 100 AP, cooldown 2, GROUND damage (enemies only), dt_heavy visual.
- No floor coverage, no safe tiles.

**Rules.**
- Blast when primed.
- Mark when a player is within 3.
- Hold position while primed (the patterns move with the caster).

**Wiring.**
- Deck Warden: Splash.
- Skyglass Sentinel and Wayfinder: Short Line.
- Every endgame floor 1-3 has one.

| Enemy | Marks (% of appearances) | Blasts (% of appearances) |
|---|---:|---:|
| Deck Warden | 85 | 41 (often dies before its next turn) |
| Sentinel | 97 | 81 |
| Wayfinder | 94 | 72 |

**Why caster-anchored, not target-anchored as the ruling asked.**
- The blast is a new cast on the caster's next turn, and the AI aims it at the target's current hex.
- In the probe, a player who stepped off a target-anchored Splash or Short Line was still hit.
- COORDINATES with origin TARGET behaves the same.
- Caster-anchored patterns stay where they were marked: standing in one is hit; one step off avoids it, and the blast still erupts on the empty tiles.

## Ground probe (`engine/probe_ground.ts`, `results/probe_ground.json`)

| Ground effect | What happens |
|---|---|
| elementaldamage | resolves to damage at cast |
| damage with rounds 2 | hits occupants at cast, then each occupant at the start of their later turns |
| poison, afterburn | nothing on the ground |
| wound | applies only with a damage row on the same action |
| drain | nothing at cast, then drains the occupant on their next action, including the move that takes them out |

- Whoever stood inside at cast cannot avoid drain.
- No type gives "nothing on cast, hits whoever stands there next round". Mark then blast stays the way to do it.

## Endgame result (`overrides/kits_endgame.params.json`; average party, live damage settings)

Tuned figures:

| Copy | Pools | HP | +100% damage rows |
|---|---:|---:|---:|
| Crew | x1 | 5,050 | 2 (+70% damage taken) |
| Core Horror | x5 | 25,250 | 4 (phase 2 at 70%) |
| The Captain | x2.8 | 14,140 | 4 |
| Sealwright | x2.6 | 13,130 | 3 (below the Captain, so the ally rules pick him) |

| Runs | Cleared | Runs with a wipe | Rounds median [p10-p90] | Min @10 s | Min @15 s [p10-p90] | @15 s + AI 1.5 s |
|---|---:|---:|---|---:|---|---:|
| 60, pets, dodging | 60 | **18.3%** (12 wipes, all on the boss wave) | 26 [24-54] | 13.8 | **19.4** [18.3-37.5] | 21.2 |
| 40, no pets, dodging | 40 | 20% (5 boss wave, 2 Core Horror) | 26 [24-55] | 13.8 | 19.4 | 20.4 |
| 30, pets, no dodging | 0 | 100% | n/a | n/a | n/a | n/a |

Without dodging, the Core Horror wipes every attempt (120 of 120). The marks are the fight.

| Wave (pets, dodging) | Rounds median [min-max] | Wiped / reached | Party HP lost |
|---|---|---:|---:|
| F1 Deck Warden x3 + Seal Charge | 3 [1-5] | 0/72 | 25% |
| F2 Sentinel + First Blade + Deck Warden | 3 [3-4] | 0/72 | 6% |
| F3 Oathkeeper + Wayfinder + Deck Warden | 3 [2-4] | 0/72 | 9% |
| F4 Core Horror | 6 [4-11] | 0/72 | **28%** |
| F5 W1 Deck Warden x3 | 3 [2-5] | 0/72 | 11% |
| F5 W2 The Captain + Sealwright | 8 [6-14] | 12/72 | 64% |

- Signature rules fire in 62-100% of appearances; the Core Horror's in 89%.
- Idle turns after round 2: 0% for the crew and the Core Horror, 6% for the Captain.
- Dodging: 86% of 1,096 threatened turns reached safety.
- Pets change little here (18.3% of runs wipe vs 20% without), because the boss wave decides the run.

## Level 40-60 result (`overrides/kits_lvl50.params.json`, unchanged; level-50 party)

| Runs | Cleared | Runs with a wipe | Rounds median [p10-p90] | Min @10 s | Min @15 s | @15 s + AI 1.5 s |
|---|---:|---:|---|---:|---:|---:|
| 60, pets, dodging | 60 | 0% | 19 [16-22] | 11.3 | **15.8** | 17.1 |
| 40, no pets, dodging | 40 | 5% (2 wipes, Core Horror) | 20 [17-26] | 11.3 | 15.8 | 16.3 |
| 30, pets, no dodging | 30 | 0% | 17 [16-18] | n/a | 14.0 | n/a |
| Level 40, pets | 29/30 | 50% (Core Horror 21 of 56 attempts, Captain 6 of 35) | 51 [36-99] | n/a | 31.8 | n/a |
| Level 60, pets | 30 | 0% | 14 [12-16] | n/a | 12.0 | n/a |

Signature rates (pets, dodging):

| Enemy | Fired in % of appearances |
|---|---:|
| Core Horror | 37 |
| The Captain | 70 |
| Deck Warden | 49 |
| First Blade | 62 |
| Oathkeeper | 68 |
| Seal Charge | 80 |
| Sentinel | 92 |
| Wayfinder | 100 |

## Decisions for the director

1. **LOCK instead of stun/seal** on Command Absolute, Ship's Bell and the Seal Lines blast.
2. **Minor marks are caster-anchored.** Target-anchored ones cannot be stepped out of in this engine.
3. **GROUND Broadside / Rows B damage the Captain's own Gunwale.** The alternative is to keep Broadside CHARACTER, but then it cannot detonate on empty rows.
4. **Shared rules cost level-50 signature turns.**
   - With one rule list per enemy, the level-50 fights are short: Core Horror 37%, Deck Warden 49% (table above).
   - Several crew rules never fire before the crew dies.
   - A level-50-only rule order would fix this but break "one kit per enemy".
5. **Level-40 bound.** The level-40 party wipes in half its runs. Gate the version at about 45+, or soften it for the low end.
6. **The Captain's lower duel rules (17-29) never fire** in an 8-round fight.
7. **Pet model.** The modelled pets are fragile and have no jutsu. Real pet data would change every floor's figures.

## Not done / incidents

- No browser, live-game or session checks. Nothing pushed, `main` untouched, game checkout unmodified.
- **Incident:** during tuning I ran `pkill -f "skyglass_wreck_sim/run.sh"`, which may have stopped other agents' harness runs. It was reported at the time. Since then I only stop processes by PID or task id from this worktree.

# Report 4b (2026-10-28): director rulings RUL-2026-10-28-025 / -026, Captain rule audit

Branch `fable/skyglass-wreck-sim`, built on 41436bdb. Offline, zero live requests.

## Changes

1. **Minor marks back to their original power:** Splash 80, Short Line 90.
   - In `probe_library`, a player standing in the blast takes 198 / 222.
   - A modelled pet (1,550 HP) takes 1,414 / 1,550, so Short Line kills it. This is accepted collateral.
2. **Level-50 Core Horror shows his signature first.**
   - New param `horrorMawFirst` (level-50 params only) moves Omen: Last Light (Maw of the Deep) to the head of his marks, with no round gate.
   - The Maw's x3 window then shortened his fight to 3 rounds and the run to 13.6 min, so his level-50 pools went from x4 to **x6** (15,300 HP). At x6 the fight lasts 6 rounds.
   - Signature rate: **100% of appearances** (was 37%).
   - `build_spec.json` keeps the base order under `sharedKits`. The level-50 order is listed under `lvl50.ruleVariants["Core Horror"]`: same jutsu, different order.
3. **Captain rule audit:** below. Nothing was cut.
4. **Broadside / Rows B and the Captain's own Gunwale.** friendlyFire **cannot** stop this in the engine:
   - `process.ts`: when ground damage lands on a tile with no unit, it is forwarded to any barrier there (`if (!user && e.type === "damage") findBarrier(...)`). `damageBarrier` then applies it. Neither step consults `friendlyFire` or the barrier's `creatorId`.
   - `checkFriendlyFire` is only called for units.
   - In the Wreck the question is currently moot: Raise the Gunwale fires in **0%** of appearances (audit below).
   - Alternatives if the Gunwale is brought back:
     - (a) accept the chip, as flavour: "his own broadside splinters the rail";
     - (b) make Broadside / Rows B CHARACTER blasts again: no chip, but they do not detonate on empty rows;
     - (c) place the Gunwale away from rows 2/3 and 5/6. That is not controllable: it is an `AOE_WALL_SHOOT` at `EMPTY_GROUND_CLOSEST_TO_OPPONENT`.
5. **Ward of Command is clear-proof.**
   - New row: `clearprevent` 100, 2 rounds, on the warded ally (`INHERIT`, FRIENDLY).
   - The engine's `clear` checks `clearprevent` first (`tags.ts clear → preventCheck`). Power 100 always blocks.
   - A trace shows `clearprevent@The Captain,decreasedamagetaken@The Captain` on each cast.
   - `clearprevent` is a shared-cooldown type, but the Sealwright has no other clearprevent jutsu.
6. **`hunt-stonebound-erupting-ground`** "Erupting Ground", added to `library_spec.json` (group "Skyglass-only copy of a live jutsu").
   - It is a copy of live `jBRyl7F4UjTyxG5nnzLqj` (Crown Stonebound) with one change: the damage row is `friendlyFire: ENEMIES` (live: unset).
   - Its `copyOf` field gives the source and the change.
   - Library total: 35 NEW records, all pass `JutsuValidator`.

`probe_library` (rerun):
- all 10 boss pairs fire in order;
- both minor pairs fire;
- every blast still detonates with all players stepped off, hitting nobody (Last Light 2 of 5, star capacity);
- the engine geometry checks are unchanged.

## The Captain: rule audit (`engine/audit_rules.ts`, `results/audit_captain_endgame.json`)

Method:
- Endgame boss wave (Captain + Sealwright), 30 seeded runs, pets and dodging on, 400 Captain decisions, wave median 9 rounds.
- A read-only hook inspects the battle before each AI decision and classifies every rule as:
  - fired;
  - **preempted** (usable, conditions met, but a higher rule fired);
  - **condition** (conditions false);
  - **cooldown** (on its own cooldown);
  - **locked** (shared-cooldown lock from another jutsu);
  - **AP** (not enough action points left).
- Distances use hex distance, an approximation of the engine's path length.

**The Captain record is shared by the Watch and The Fall,** so "cut" below means cutting from the Wreck's rule order. The moves themselves stay on the record.

**Main finding: the set-piece loop fills every turn.**
- Each turn is either a mark (40 AP, then the after-mark end turn) or a blast (100 AP).
- Rows A and the Binding Ring each have cooldown 4, so they alternate and leave no free turn.
- So nothing below rule 16 ever acts.

| # | Rule (move) | Fired in % of appearances | Cause when not firing | Recommendation |
|---:|---|---:|---|---|
| 0 | Hold the Line (live Unbroken Command), `far 5` | 3 | condition: players are within 5 when the wave opens | reorder/condition: make it the opener (`round_lower_than 2`) or cut |
| 1 | Last Stand at the Helm (live Battle Trance), under 50% | 93 | n/a | keep |
| 2 | Broadside (signature) | 97 | n/a | keep |
| 3 | Rows B blast (second volley) | 0 | its mark (16) never fires | cut, with 16 and 8-10 |
| 4 | Ship's Bell (signature) | 100 | n/a | keep |
| 5-6 | after Rows A: Final Command / Keelbind | 43 / 47 | their own cooldowns | keep: the duel moves land here |
| 7 | after Rows A: end turn | 83 | n/a | keep (structural) |
| 8-10 | after Rows B: Final Command / Keelbind / end turn | 0 | Rows B is never marked | cut with Rows B |
| 11-12 | after the Binding Ring: Final Command / Keelbind | 67 / 57 | own cooldowns | keep |
| 13 | after the Binding Ring: end turn | 93 | n/a | keep |
| 14 | Omen: Binding Ring (a player within 2) | 100 | n/a | keep |
| 15 | Omen: Rows A | 100 | n/a | keep |
| 16 | Omen: Rows B | 0 | preempted (381 of 400 decisions): Rows A has the same condition and cooldown and sits above it, and Rows A plus the Binding Ring fill every mark turn | cut in the Wreck, or alternate (e.g. Rows A cooldown 6 so Rows B fills the gap) |
| 17 | Raise the Gunwale (round > 2) | 0 | preempted (365): no turn is free | reorder above the marks with a gate (e.g. health below 70, or Sealwright alive) if the director wants it; then see item 4 |
| 18-19 | Final Command / Keelbind (standalone) | 0 | duplicates of 5-6 / 11-12: on cooldown from those (227 / 250) or preempted | cut (duplicates) |
| 20 | Stolen Form (target buffed) | 0 | condition (176: no target with +25% damage given) and preempted | cut from the Wreck order (keep for Watch / Fall) |
| 21 | Suppression Writ | 0 | preempted (364) | move into an after-mark slot for variety, or cut |
| 22 | Second Wind (under 40%) | 0 | condition (328): he rarely lives long below 40%; Last Stand at 50% comes first | reorder above the marks if a heal is wanted; else cut |
| 23 | Counter Stance (player adjacent) | 0 | condition (211) and preempted (177) | cut from the Wreck order |
| 24 | Ruin Refrain | 0 | preempted (271), and **locked** (112) by Final Command's shared stun cooldown | cut in the Wreck (stun overlap with Final Command) |
| 25-27 | Unraveling Strike / Explosive Tag Cataclysm / Windlash Focus | 0 | preempted (369 / 369 / 380) | optional: rotate into after-mark slots; else cut |
| 28 | patrol: close in (`far 4`) | 0 | condition (399): players are always within 4 | keep (fallback) |
| 29 | highest-power damage | 0 | preempted (400) | keep (fallback) |

Level 50 (same order, no Sealwright): the Captain's signature fires in 85% of appearances. Rules 17-28 never fire, for the same reason.

## Final runs (this build)

| Version, runs | Cleared | Runs with a wipe | Rounds median [p10-p90] | Min @15 s (+ AI 1.5 s) | Notes |
|---|---:|---:|---|---|---|
| Endgame, 60, pets, dodging | 60 | **18.3%** (13 wipes, all on the boss wave) | 26 [24-55] | **19.3** (21.2) | Core Horror 32.5% party HP, no floor-4 wipes; signatures: Horror 90%, Captain 100% |
| Endgame, 40, no pets | 40 | 25% (9 boss wave, 2 Core Horror) | 26.5 [24-55] | 19.5 (20.5) | |
| Endgame, 30, pets, no dodging | 0 | 100% | n/a | n/a | the Core Horror wipes 120 of 120 attempts |
| Level 50, 60, pets, dodging | 60 | 1.7% (1 Core Horror wipe) | 19 [16-22] | **15.3** (16.4) | Horror 6 rounds, signature **100%**; Captain 85% |
| Level 50, 40, no pets | 40 | 0% | 21 [18-26] | 16.9 (17.5) | |
| Level 50, 30, pets, no dodging | 30 | 20% (5 Core Horror, 1 Captain) | 19 [16-30] | 15.1 | |
| Level 40, 30, pets | 0 | 100% | 105 | n/a | the Core Horror wipes 118 of 120 attempts |
| Level 60, 30, pets | 30 | 0% | 14 [13-16] | 11.8 | |

- The level-40 bound is now worse than in report 4 (was 50%). The x6, Maw-first Core Horror is a wall for this level-40 model.
- That reinforces the earlier recommendation: gate this version at about level 45+, or give the low end its own Horror.

**Determinism.**
- `--probe-check` with pets passes on both versions: endgame seeds 1-4, run alone and under parallel load; level 50 seeds 1-2.
- **One unexplained failure:** the endgame probe-check, run once in parallel with two other final-run jobs, reported a different Sealwright action right after a Ward of Command in seed 1's boss floor.
- Under similar load the failure did not reproduce, alone or in-process across all floors.
- No unseeded source was found: Math.random, getRandomValues and Date are all seeded or virtual, `preventCheck` uses the seeded Math.random, and enemy rows are cloned per floor.
- Logged as an open item.

# Report 4c (2026-10-28): the Captain rebuilt in two phases (RUL-2026-10-28-031)

Branch `fable/skyglass-wreck-sim`, built on c519601b. Offline, zero live requests.

## The new rule order (`engine/kits.ts`; `build_spec.json` → `sharedKits["The Captain"]`)

| # | Rule | Gate |
|---:|---|---|
| 0 | Raise the Gunwale | health below 50. Record cooldown 8 → **99**, so it fires once per fight: the rail goes up between him and the party. |
| 1 | Last Stand at the Helm (live Battle Trance) | health below 50 |
| 2 | Second Wind | health below 25 |
| 3-4 | Broadside / Ship's Bell blasts | their primed markers |
| 5-10 | after each mark: Final Command, Keelbind, end turn | the 60 AP left after the mark |
| 11-12 | Omen: Binding Ring, Omen: Rows A | health below 50. Each has cooldown 4 and each set piece takes two turns, so they alternate. |
| 13 | Hold the Line (live Unbroken Command), the duel opener | the party is 3+ hexes away (the boss wave starts mid-battle, and no condition can detect the wave's first round) |
| 14-17 | Final Command, Keelbind, Stolen Form (top threat has any damage-given buff, was 25%+), Counter Stance (a player within 2, was adjacent) | duel |
| 18-21 | Suppression Writ, Unraveling Strike, Explosive Tag Cataclysm, Windlash Focus | duel fillers (not cut) |
| 22-23 | close in, highest-power damage | fallbacks |

**Cut from the order:**
- Rows B: its mark, blast and after-mark rules.
- The duplicate standalone Final Command / Keelbind. Each now appears once as a phase-1 duel move, plus in the after-mark slots.
- Ruin Refrain.

**Not exactly as ruled:**
- "Once" holds only for the Gunwale (my record).
- Battle Trance (cooldown 5) and Second Wind (cooldown 6) are live records, and the engine has no "has not used" condition. They fire once per cooldown while under their gate; in a 2-3-round phase 2 that is effectively once.
- Broadside chipping the Gunwale is accepted.
- The Sealwright / Ward of Command puzzle is unchanged.

**Tuning:** the duel phase hits far harder than the old set-piece loop.
- With 4 Captain damage rows, the boss wave wiped 44 of 56 attempts.
- Rows 1 / 2 / 3 gave 5% / 20% / 52.5% of runs wiping. **Captain rows 2** (pools x2.8 unchanged, still above the Sealwright).

## Results (this build)

| Version, runs | Cleared | Runs with a wipe | Min @15 s (+ AI 1.5 s) | Notes |
|---|---:|---:|---|---|
| Endgame, 60, pets, dodging | 60 | **21.7%** (16 wipes, all on the boss wave) | **19.8** (21.6) | Core Horror 32.5% party HP, no floor-4 wipes |
| Endgame, 40, no pets | 40 | 22.5% (10 boss wave, 1 Core Horror) | 19.3 (20.2) | |
| Endgame, 30, no dodging | 0 | 100% | n/a | Core Horror 120 of 120 |
| Level 50, 60, pets | 60 | 1.7% | 15.4 (16.6) | the Captain costs 31.5% party HP (was 11%) |
| Level 50, 40, no pets | 40 | 0% | 16.8 | |
| Level 50, 30, no dodging | 30 | 16.7% (Core Horror) | 15.5 | |
| Level 40 / level 60 | 0 / 30 | 100% / 0% | n/a / 11.6 | the easy version is now marked "for level 45+" (`build_spec.json` → `lvl50.dungeonNotes`) |

`--probe-check` with pets passes on both versions (seeds 1-2).

## Phase lengths and per-move fire rates (`audit_rules.ts`; 30 runs, pets, dodging)

| | Endgame boss wave | Level 50 boss wave |
|---|---|---|
| Wave rounds (median) | 7 | 5 |
| Phase 1 (above 50%), median [range] | **6** [1-9] | 2 [1-4] |
| Reached phase 2 | 80% of appearances | 97% |
| Phase 2, median [range] | **2** [1-9] | 3 [1-5] |

Fired in % of appearances (endgame / level 50):

| Move | Endgame | Level 50 | Main reason when not firing (endgame) |
|---|---:|---:|---|
| Raise the Gunwale (transition) | 80 | 97 | phase 2 not reached |
| Last Stand (Battle Trance) | 80 | 73 | phase 2 not reached |
| Second Wind (under 25%) | 33 | 73 | rarely under 25% while alive |
| Omen: Binding Ring → Ship's Bell | 27 → 17 | 43 → 20 | phase 2 is short; the transition turn spends 100 AP on Gunwale + Trance |
| Omen: Rows A → Broadside | 10 → 7 | 0 → 0 | the Bell comes first; there is rarely a second mark turn |
| After a mark: Final Command / Keelbind | 3 / 7 | 0 / 13 | own cooldowns, often already used in phase 1 |
| Hold the Line (opener) | 37 | 20 | the party is often within 3 hexes when the wave opens |
| Final Command (duel) | 93 | 77 | own cooldown |
| Keelbind (duel) | 100 | 47 | own cooldown |
| Stolen Form (duel) | 50 | 0 | condition: the top threat carries no damage-given buff |
| Counter Stance (duel) | 100 | 67 | own cooldown |
| Suppression Writ / Unraveling / Cataclysm / Windlash | 93 / 100 / 93 / 97 | 23 / 30 / 0 / 3 | own cooldowns (at level 50: preempted, the fight is short) |

Full tallies by phase: `results/audit_captain_endgame.json`, `results/audit_captain_lvl50.json`.

**Reading.** The duel now carries the fight. In the endgame, phase 2 is short (2 rounds) for three reasons:
- he melts once the Ward is gone (the Sealwright usually dies in phase 1);
- the transition turn uses all 100 AP on the Gunwale and Battle Trance;
- 20% of the time he dies or wipes the party before 50%.

So the deck set pieces show in only 17-27% of appearances.

**Options for the director** (none applied):
1. **Gunwale with the first mark, Trance on the spare AP after a mark** (tested, 40 runs):
   - wipes 22.5%, 19.8 min;
   - Bell mark 55%, Rows A mark 25%;
   - but Battle Trance falls to about 20% of appearances.
2. **Raise the phase threshold to about 60-65%**, so phase 2 gets more of his HP.
3. **Give phase 2 its own damage reduction** (a phase-2 Ward or rail absorb), so the deck phase lasts.

## What would affect the Watch and The Fall (the record is shared)

- **Kit list.** The kit is derived from the rule list, so **Ruin Refrain and Omen: Rows B / its blast leave his jutsu list.** The list now carries the library's lib-omen-binding-ring / lib-omen-rows-a, Broadside, Ship's Bell and Raise the Gunwale.
- **Raise the Gunwale is now once per fight** (cooldown 99).
- **Phase 2 is gated only on health below 50.** In a solo fight he switches to the deck set pieces at 50%:
  - Broadside's rows are fixed battlefield rows (2 and 5);
  - the Bell is a radius-2 disc around him.
  - Both are dodgeable by one player, but the fight's feel changes.
- **Hold the Line needs the party 3+ hexes away.** If the Watch / Fall start the player adjacent, it never fires.
- **Battle Trance and Second Wind repeat on cooldown** (5 / 6 rounds). A long solo fight sees them more than once.
- **Stolen Form needs a buffed top threat.** It never fires against a player who uses no damage-given buffs (level 50: 0%).
- The per-version stats (rows, pools) are not part of the shared record.

# Report 4d (2026-10-29): the Captain's transition turn and a longer phase 2 (RUL-2026-10-28-032)

Branch `fable/skyglass-wreck-sim`, built on ff9ca6ff. Offline, zero live requests. Engine pin c86f43f4.

## The transition turn

At his first turn below 50% the Captain spends **80 AP in one turn**:

| Order | Move | AP | Notes |
|---:|---|---:|---|
| 1 | **Steady the Helm** (new, `lib-steady-the-helm`; name approved in RUL-2026-10-29-045) | 20 | self: cleanse, 40% less damage taken, 40% absorb, clear-proof; cooldown 99 (once) |
| 2 | Raise the Gunwale | 20 (was 60, then 30) | cooldown 99 (once) |
| 3 | First deck mark (Omen: Binding Ring → Ship's Bell) | 40 | library mark |
| - | after-mark end turn | | the 20 AP left fit nothing (every after-mark move costs 40+) |

- **80, not 100.** A player stun (Stunning Jab, `apReduction` 20) leaves him 80 AP, and the engine's cleanse cannot lift a stun (`isNegativeUserEffect` does not list `stun`). With 30 + 30 + 40 the level-50 transition split in 80% of appearances (the level-50 party stuns him often); with 20 + 20 + 40 it holds in 100%.
- **Battle Trance follows on a later turn.** It now ranks first in the 60 AP after each later mark (above Second Wind). The turn after the transition is the first blast (100 AP), so it lands on the second phase-2 turn: 2 rounds after the transition in 51 of 55 endgame appearances, 1 round after in the 4 split cases; never on the transition turn (`--together "Steady the Helm|Last Stand"`: same round 0%).
- **Remaining split (endgame 5%).** The rule engine has no action-point condition. When he crosses 50% *during* his own turn (a wound / afterburn tick or reflect on his first action, e.g. seed 1: Keelbind, then a 755 HP wound tick), he has 40-60 AP left: Steady and the Gunwale fire, and the mark opens his next turn. Fixing this needs an AP-aware condition in the engine.

## Steady the Helm: tags and engine semantics (pinned source)

| Tag | Setting | Engine behaviour |
|---|---|---|
| `cleanse` | power 100, rounds 0, SELF | `tags.ts` `cleanse` → `removeEffects(..., "negative")`: removes his non-persistent negative tags at once (seen: wound, increasedamagetaken). Does not remove `stun` (not in the negative list). Shared-cooldown tag (3 rounds); nothing else in his kit carries it. |
| `decreasedamagetaken` | 40%, rounds 2, SELF | applies only from the round after the cast (`passesTiming`: not new, not the cast round). Rounds tick at each round change, except in the cast round, so it covers **the two full rounds after the transition**. |
| `absorb` | 40%, rounds 2, SELF, pools Health | `tags.ts` `absorb`: converts 40% of each incoming damage packet into health, from the round after the cast (same timing as the DR). It is a heal: `healprevent` blocks it. Chosen over `shield` (a flat HP bubble with a power-% creation roll) and `lifesteal` / `vamp` (heal from damage *dealt*). |
| `clearprevent` | power 100, rounds 2, SELF | `clear` checks it (`preventCheck(..., "clearprevent")`): the party's clears cannot strip his DR, absorb or Battle Trance. Shared-cooldown tag. |

## Tuning (`overrides/kits_*.params.json`)

Phase 2 barely responded to HP at first. The party's burst rounds reach 7,000-14,000 damage, so he often makes his first phase-2 decision well below 50% (median 41-44%, down to 4%). At the old HP, 20% of appearances never reached phase 2.

Sweep, endgame boss wave, 30-60 runs each (`audit_rules.ts`, pets, dodging):

| Captain pools / damage rows / Steady DR-absorb-rounds | HP | Phase 1 med | Phase 2 med (p90) | Wave wipes per attempt |
|---|---:|---:|---:|---:|
| 2.8 / 2 / 40-40-2 (start) | 14,140 | 6 | 4 (7) | 10% |
| 4.4 / 2 / 40-40-2 | 22,220 | 7 | 4 | 23% |
| 6.0 / 2 / 40-40-2 | 30,300 | 8 | 5 | 43% |
| 4.0 / 1 / 40-40-**4** | 20,200 | 6 | 4 (6) | 3% |
| 5.0 / 1 / **60-60-3** | 25,250 | 7 | 5 (8) | 3% |
| 7.0 / 1 / 40-40-2 (60 runs) | 35,350 | 7 | 6 (9) | 15% |
| **7.5 / 1 / 40-40-2 (60 runs, chosen)** | **37,875** | **8** | **6 (10)** | **17%** |
| 8.0 / 1 / 40-40-2 (60 runs) | 40,400 | 8 | 7 (10) | 22% |

- The sweep rows except the chosen one ran with the 30 + 30 AP transition, before the 20 + 20 change.
- **Chosen: pools 7.5, damage rows 2 → 1, Steady exactly as ruled (40/40/2).** Longer or stronger defence did less than HP, so the ruled numbers stand.
- **Level 50: pools 2.5 → 4** (10,200 HP, rows 3 unchanged): phase 2 4 → 7 rounds. Pools 3.5 gives 5.

## Results (this build, `results/`)

Phase lengths (`audit_rules.ts`, pets, dodging; phase 2 = from his first decision below 50% to his death or the wipe):

| | Endgame (60 runs) | Level 50 (30 runs) |
|---|---|---|
| Phase 1, median / p90 [range] | **8 / 12** [5-18] | 3 / 4 [2-6] |
| Phase 2, median / p90 [range] | **6 / 10** [3-18] | **7 / 9** [4-16] |
| Reached phase 2 | 95% | 100% |
| Health at first phase-2 decision (median) | 44% | 44% |
| Mark + Gunwale + Steady in one turn | **95%** of transitions | **100%** |
| Battle Trance in phase 2 | 92% of appearances, never on the transition turn | 100% |
| Broadside / Ship's Bell blast fired | 72% / 93% (were 7% / 17%) | 63% / 97% |

Full dungeon (`main.ts`):

| Version, runs | Cleared | Runs with a wipe | Boss wave wipes / attempts | Boss wave rounds med / p90 | Min @15 s (+ AI 1.5 s) | Was (report 4c) |
|---|---:|---:|---:|---|---|---|
| Endgame, 60, pets, dodging | 60 | **26.7%** | 18 / 78 (23%), plus 1 Core Horror | 12 / 17 | **23.1** (25.2) | 21.7%, 7.5 rounds, 19.8 min |
| Endgame, 30, pets, no dodging | 0 | 100% | n/a | n/a | n/a | unchanged: the Core Horror wipes 120 of 120 |
| Level 50, 60, pets, dodging | 60 | **10%** | 7 / 67, plus 1 Core Horror | 9 / 12 | **18.5** (19.9) | 1.7%, 4 rounds, 15.4 min |
| Level 50, 30, pets, no dodging | 30 | 46.7% | 13 / 43, plus 8 Core Horror | 8 / 10 | 19.4 | 16.7% (Core Horror only) |

The no-pets results (`kits_*_nopets.json`) are from the previous build and were not re-run.

**Reading.**
- **Endgame.** Phase 2 meets the median 6. Wipes and time are over the earlier targets:
  - wave wipes are 17% in the audit seeds and 23% in the full runs (seed noise is about ±5 points at 78 attempts);
  - runs with a wipe are 26.7%, against ~22%;
  - the run takes 23.1 min, against ~20.
- **The time cannot be recovered with the Captain alone.** A 6-7 round phase 2 plus an 8-round duel makes a 12-14 round wave, against 7.5 before. Phase 1 and phase 2 share one health pool, and the transition defence did less than HP.
- **Level 50.** The easier version's Captain now costs wipes: 10% of runs with dodging, and 13 of 43 attempts without dodging. Pools 3.5 (phase 2 5 rounds) or the old 2.5 are the alternatives.

## Determinism

- `--probe-check` with pets passes on both versions (seeds 1-2; rule probe on/off and repeat identical).
- `main.ts` endgame, 8 runs, run twice concurrently: identical results.
- `trace_floor.ts` endgame seed 42, three times (two concurrently): byte-identical.
- **Open item:** `audit_rules.ts` runs all its seeds in one process. Between invocations, 2-4 of 45-60 seeds differ (e.g. seeds 20, 24, 42), although each seed reproduces alone in a fresh process. The medians, p90s and kill rates matched in all four audit invocations. Unexplained; the earlier parallel-load probe-check failure (report 4b) may share the cause. The `main.ts` figures above are unaffected.

## Also seen (not changed)

- **A stunned Captain cannot fire a 100 AP blast.** Stunning Jab (apReduction 20) leaves him 80 AP, so a primed Broadside / Bell is skipped that turn and the after-mark slot fires instead (seed 1, round 17). This holds for every library blast (all 100 AP).
- **Unmarked Broadside in phase 1.** The fallback `highest-power damage` (use_highest_power_action) can pick Broadside without its mark (1 of 8 fallback picks in traced seeds). This is a phase-1 set piece, against RUL-2026-10-28-031. Replacing the fallback with a named duel move would close it.
- **Second Wind now heals 15% of 37,875** (about 5,700 HP) once below 25%.

## What the Watch / The Fall re-run needs (shared record)

- **New jutsu in his kit:** Steady the Helm (`lib-steady-the-helm`, 20 AP, cooldown 99, once per fight). The kit is 17 jutsu (was 16).
- **Raise the Gunwale is 20 AP** (was 30 in the uncommitted draft, 60 in 4c), still once per fight.
- **The rule order changed:**
  - Steady → Gunwale → mark sit below the blasts and the after-mark slots;
  - Battle Trance moved into the after-mark slots, above Second Wind, so it fires only after a later mark (in a long solo fight: on the cooldown-5 cadence after marks);
  - Second Wind also fires on a phase-2 turn with no mark ready.
- **A solo player's own stun or cleanse play changes the transition:**
  - one stun (apReduction ≤ 20) still fits it;
  - a stronger stun (apReduction > 20) splits it;
  - his clearprevent blocks the player's clears for 2 rounds.
- **Health and damage rows are per-version stats** (endgame pools 7.5 / rows 1, level 50 pools 4 / rows 3), not part of the shared record. The Watch's own Captain row needs its own phase-2 check: DR / absorb cover the 2 rounds after the transition whatever his HP.
- **Hold the Line / Stolen Form caveats from 4c are unchanged.**

# Report 4e (2026-10-29): RUL-2026-10-29-045 follow-up: phase-1 fallback, earlier-floor trim

Branch `fable/skyglass-wreck-sim`, built on 9ce90151. Offline, zero live requests. The Captain's numbers are unchanged (endgame pools 7.5 / rows 1; level 50 pools 4 / rows 3; Steady the Helm 40/40/2 at 20 AP). Steady the Helm is the approved name.

## Phase 1 is a duel only: the fallback fix

- **The problem.** The Captain's last rule was `use_highest_power_action` (damage). The engine ranks every available action by its damage tag's power, so whenever his duel moves were on cooldown it picked **Broadside (140)**, unmarked, in phase 1.
- **The fix.** That rule is now `use_specific_jutsu` naming the engine's basic attack (`actions.ts`: id `basicAttack`, range 1, 20 AP; `ai_v2` matches a use_specific_jutsu action by id). With nothing in reach he ends his turn.
- **Kit and server.** `basicAttack` is not a jutsu record, so it is kept out of his kit list and the build_spec counts. The server's profile save only looks up jutsu ids to reject move/summon effects, so an unknown id passes.
- **For the builder.** The rule's `jutsuId` is the literal `basicAttack`; it must not be remapped like the placeholder ids.

Verified with `audit_rules.ts` `actionsByPhase` (endgame, 60 runs, same seeds):

| | Broadside in phase 1 | Basic attacks in phase 1 | Boss wave killed (audit) |
|---|---:|---:|---:|
| Before (9ce90151) | **36** | 147 | 83% |
| After | **0** | 176 | 90% |

- Level 50 has 0 Broadsides in phase 1.
- Level 50's dodging battery is byte-for-byte the same as 9ce90151 (10% runs with a wipe, 18.5 min). Without dodging it moves by one boss-wave wipe (12 / 42, was 13 / 43). **Level 50 is left as it was.**

## Trimming an earlier floor

Endgame time per wave, human turns (median) at 9ce90151 + the fix:

| F1 | F2 | F3 | F4 Core Horror | F5 wave 1 (3 Wardens) | F5 the Captain |
|---:|---:|---:|---:|---:|---:|
| 9 | 8 | 8 | 16 | 8 | 31 |

- Each turn is 15 s, and each floor battle adds 30 s.
- Floors 1-3 already clear in 3 rounds each.
- **The Captain wave alone is about 8 minutes.**

Options tested (40 runs, pets, dodging, with the fallback fix):

| Layout | Runs with a wipe | Min @15 s | Change |
|---|---:|---:|---|
| Fix only, layout unchanged | 20% | 23.3 | |
| **B (applied): drop the filler Deck Warden on floors 1, 2 and 3** | 17.5% | 22.3 | −1.0 min |
| A: drop floor 5's 3-Warden wave | 12.5% | 22.9 | −0.4 min |
| A + B | 12.5% | 21.8 | −1.5 min |

- **Why B.**
  - The three Wardens it removes are a Deck Warden wave's worth.
  - On floors 2 and 3 the Warden was a repeated add-on to each floor's own crew pair (Sentinel + First Blade, Oathkeeper + Wayfinder).
  - Floor 1 keeps two Wardens + the Seal Charge, and the boss floor keeps its Warden lead-in.
  - Earlier floors restore the party on a win, so it does not touch the boss wipes.
- **Why not A.**
  - It cuts the deck crew's lead-in to the Captain.
  - It saves little: with the Captain as the floor's first wave, the party starts at spawn distance, and his wave takes about 8 more human turns. The time moves into his wave.
  - It drops wipes to about 12%.

**One wave is not enough.** About −3 minutes would mean removing a whole earlier floor battle, and the engine fixes five floors per tier. Other options (not applied):
1. **Lighter crew health.** Crew pools x1.0 → x0.6: 20.3 min, but 0% runs with a wipe (40 runs).
   - Floor 5's Wardens are the same record, and the party reaches the Captain fresher.
   - Pools below x1 also fail `insertAiSchema` (`poolsMultiplier >= 1`), so it would need a level / stat route.
   - Lightening only the floor 2-3 crews (separate records) is worth about −1 min.
2. **A + B:** 21.8 min, about 12% wipes.
3. **Accept about 22 minutes** with B (applied).
4. Anything shorter has to come from the Captain wave itself (phase 1 length), which the ruling keeps.

## Results (this build, `results/`)

Phase lengths and the transition (`audit_rules.ts`):

| | Endgame (60) | Level 50 (30) |
|---|---|---|
| Phase 1 median / p90 | 8 / 11 | 3 / 4 |
| Phase 2 median / p90 | **6 / 8** | **7 / 9** |
| Mark + Gunwale + Steady in one turn | 95% | 100% |

Full dungeon, before and after:

| Version, runs | 4c (ff9ca6ff) | 4d (9ce90151) | **4e (this build)** |
|---|---|---|---|
| Endgame, 60, pets, dodging: runs with a wipe | 21.7% | 26.7% | **16.7%** (boss wave 10 / 70; Core Horror 1 / 71) |
| Endgame: min @15 s (+ AI 1.5 s) | 19.8 (21.6) | 23.1 (25.2) | **22.3** (24.1) |
| Endgame: boss wave rounds median / p90 | 7.5 / 14 | 12 / 17 | 12.5 / 16 |
| Endgame, 30, no dodging | 0 cleared (Core Horror) | 0 cleared | 0 cleared (Core Horror 120 / 120) |
| Level 50, 60, pets, dodging | 1.7%, 15.4 min | 10%, 18.5 min | **10%, 18.5 min** (unchanged) |
| Level 50, 30, no dodging | 16.7% | 46.7% | 46.7% (Captain 12 / 42, Core Horror 8 / 50) |

The endgame wipe rate fell below the ~22% target because the phase-1 Broadside is gone. Restoring it would mean raising the Captain's damage or health, which the ruling keeps fixed.

## Determinism

- `--probe-check` with pets passes on both versions (seeds 1-2).
- The `audit_rules.ts` in-process seed drift from 4d is still open. The `main.ts` batteries are seed-deterministic.

## For the Watch re-run

- His last rule is now the named basic attack. A solo Watch Captain also stops casting unmarked Broadsides.
- **Other enemies still end on `use_highest_power_action`.** It ranks every available action by power, so it can also cast unmarked library blasts. The Wreck crew and the Core Horror were not audited for this; the Captain's fix is the pattern if they need it.

### 8. The Haul payout fit (RUL-2026-10-30-060 item 4), `fable/skyglass-haul-fit`

Offline: the fights do not depend on the payout. The Trophy Hold and the Bloom Cellar gained one guard on their step-2 and
step-3 lockers, as on the Snare Room (`engine/haul.ts`: Trophy step 2 + Wayfinder copy, step 3 + Blade copy; Bloom step 2 +
Warden copy, step 3 + Sentinel copy), and were re-run: every legal path state-merged, 24 seeds
(`results/fit_haul_base_dodge.json`, merged with the four unchanged pages into `results/fit_haul_base_merged.json`), then
the top routes exactly, 40 seeds (`results/fit_haul_exact_*.json`). The exact runs also covered the Bone Store's, Ore
Vault's, Snare Room's and Overgrown Stores' top routes that had only merged rates: the Bone Store's CLXCC is **157%** and
the Ore Vault's CCCL **124%** at the old points (the final pass had not run them exactly).

`tools/haul_payout_fit.py` keeps the greedy band ahead of the ceiling and its local search cannot leave its start on the
Ore Vault, so the points were fitted with `tools/haul_payout_minmax.py` (global search, the ruling's 120% ceiling first,
then sensible about 7.5M, timid CC under 75%, the greedy band, the same layout floors). Points: `results/fit_haul_points.json`;
every route above the sensible route: `results/fit_haul_summary.json`. `haul_spec.json` is regenerated with them.

| Page | Old points (steps / locker) | Fitted points | Sensible | Worst route (vs sensible) | Greedy: best-clearing 5-step 3+L route |
|---|---|---|---|---|---|
| Trophy Hold | 4.2 / 0.9 / 1.3 / 3 / 5.4, 2.4 | 4.2 / 0.9 / 1.3 / 3.0 / 2.7, 3.3 | LCC 7.77M | CL **108.1%** (merged, at 100% clear, so no higher) | CLXLL 13.4% clear, pays 21.8M |
| Bone Store | 4.2 / 0.9 / 1.3 / 1.2 / 7.3, 2.5 | 4.2 / 0.9 / 1.3 / 1.1 / 2.1, 2.5 | LCC 7.98M | LCL **109.7%** (exact) | LLLCC 25% clear, pays 15.7M |
| Snare Room | 5.2 / 0.9 / 1.5 / 1.2 / 3.5, 3.3 | 5.1 / 0.9 / 1.5 / 1.0 / 3.5, 1.7 | CCL 7.35M | LXL **119.1%** (exact) | CLLLC 30% clear, pays 15.7M |
| Overgrown Stores | 3.7 / 1.4 / 1.9 / 2.5 / 8.6, 1.1 | unchanged | CLC 7.49M | LLL **117.7%** (exact) | LLLCC 37.5% clear, pays 21.0M |
| Ore Vault | 4.5 / 1.9 / 2.2 / 0.6 / 0.6, 1.9 | unchanged | LCC 7.61M | CCCL **124.1%** (exact) | CLCLL 55% clear, pays 15.4M |
| Bloom Cellar | 4.1 / 0.9 / 1.9 / 4.2 / 5.7, 1.4 | unchanged | LCC 7.29M | LLCC **112.8%** (exact) | LLCCL 27.5% clear, pays 21.0M |

- **Ore Vault: 124%, points cannot reach 120%.** CCCL and LCC always reach the same rung (CCCL has every LCC point plus
  step 4's), and CCCL clears 90% against LCC's 72.5% (the step-4 locker lost a guard, RUL-2026-10-29-045), so the ratio
  is 90 / 72.5 whatever the points. Inside the ~125% stop line; reported, not changed.
- **Greedy clears pay less on three pages.** Holding the ceiling and a ~7.5M sensible route caps the greedy clear at
  15.7M (about 2.1x) on the Bone Store and the Snare Room (was 21.8M, ~3x, RUL-2026-10-29-045). On the Trophy Hold the extra
  guards drop the best greedy route to about 13-16% clears (merged), though it still pays 21.8M. Not adopted as balance:
  the director's.

