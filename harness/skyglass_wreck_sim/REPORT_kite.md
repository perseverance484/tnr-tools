# Skyglass Wreck boss floor, solo kiter: old vs fixed Captain (2026-10-31, `fable/skyglass-kite-sim`)

Lane A, offline only: zero live requests, no credentials. Engine: `git archive` export of theninjarpg at
**3314d122** (`TNR_ENGINE_PIN=3314d122c93e036618483d18229a793ad7ad21fd`; the harness default is still c86f43f4), run
socket-denied by `run.sh`. Branch base: `origin/fable/skyglass-rule-cap` @ 990d0aa4.

## 1. Question

The director's live battle `lIKSZTazonCWc7MgJNHZ6`: a level-100 solo player with two pets stayed 5+ hexes away. The
Captain's rule 8 (Hold the Line = Unbroken Command, cooldown 2, +80% damage given and +30% offence for 99 rounds,
stacking) fired 11 times, Keelbind went 4,407 → 400,930, and he one-shot the player in round 27. Between casts he ended
his turn, never fell below 50%, and phase 2 never started. The 3-player harness had predicted a 9-round boss wave with
one Hold the Line. This pass measures a SOLO player who kites, before and after the RUL-2026-10-31-091 fix
(push/398-400, `push/skyglass_captain_fix.gen.py` on origin/main).

## 2. What was built (all harness-side; no spec or generated file edited)

- **`engine/sim.ts` `KiteOpts`** (`runFloor({ kite })`): a harness auto-player stance, applied after the dodge (a
  dodge step always wins) on human turns in the listed waves. Distances are hex distances to the nearest living
  opponent unit (pets/summons count).
  - `kite` (strict): nearer than 5 → step (engine Move, 10 AP, one hex) to the free unmarked neighbour farthest from
    every opponent (ties: more free neighbours, away from corners); otherwise hold. Self buffs and any attack whose
    range reaches from where it stands still fire. The close-in rule, the basic-attack fallback and the engine's
    appended backup moves are replaced by an explicit end of turn.
  - `poke` (hit and run): once per turn, if an attack jutsu is ready and the AP cover the steps in plus the cast,
    step in (unmarked hexes) to that jutsu's range, cast, then retreat as `kite` with the AP left.
  - `close` = the existing auto-player (casts in range, closes in, dodges marks).
- **`engine/kite.ts`**: floor 5 (index 4) of `overrides/kits_endgame.json` (wave 1: three Deck Wardens; wave 2: The
  Captain + the Sealwright), ONE player, two pets. The stance applies in wave 2 only (`--kite-waves 2`); wave 1 is
  played close-in and the player carries its pools into the boss wave (median 91% HP for elite, 44% for average).
- **The fix, in memory** (`--rules new`), restating the generator on the harness copy `dg-the-captain` (whose 20
  rules match the live push/361 list index for index; set pieces are the harness `lib-*` ids):
  1. rule 13 (Stolen Form) deleted; the last rule (basic attack) gated `player_within_range 0..1`;
     `move_towards_opponent` CLOSEST_OPPONENT (no conditions) appended: 20 rules;
  2. innate `stunprevent` 100 / 99 rounds appended to his effects;
  3. Unbroken Command (`0Y10JpChssDwFUxNRk6p3`, captured cooldown 2) cooldown → 99.
  `--uc-cooldown N` and `--stunprevent on|off` can isolate parts 2-3 (not run in this pass). Old = the override as
  generated. Both cells set the Captain's `poolsMultiplier` to **9** (the live record, push/361) through the same
  `aiEdit` / `scaleEditedAi` path; the generated override still says 7.5. The override file is read, never written.
- **Pets:** the engine spawns at most one active pet per owner (`pets.ts addPetsToBattle`). The first pet enters
  through the engine path (`model.ts petFor`, rank 5, 1,550 HP); the second is a **harness clone** of that battle
  actor (own id, nearest free cell, shared pet profile). Not an engine path.
- **Players:** `average` = the harness's level-100 JONIN endgame member (stats at the JONIN caps, Kitsune set, 9-jutsu
  Fire/Wind endgame kit, 6,250 HP). Solo it dies within ~3-5 rounds of the boss wave in every cell, so a second
  player, `elite` (existing tier: JONIN caps, 30,300 HP, -75% damage taken, +400% damage given, default 8-jutsu
  kit), carries the long-fight comparison. Every player jutsu has range 4 (the endgame kit) or less, so a strict
  kiter at 5+ hexes cannot hit anything; its damage comes from pets and from turns it is cornered.
- **`tools/kite_tables.py`** renders the tables below from `results/kite_<player>_<rules>_<mode>.json`.

Seeded (seeds 1-30 per cell), 150-round floor cap, dodge on, live damage config. Reproducibility: elite/new/poke
seeds 1-3 re-run identically.

## 3. Results (30 runs per cell)

"Idle" = a Captain turn whose only actions were end turn / nothing; "(player 2+ away)" = of those, turns where at his
first decision the player stood 2+ hexes away. Max hit = largest single-step HP loss of the player from an enemy
action. "Own turn" deaths = HP lost during the player's own step (a damage-over-time tick, e.g. Keelbind's drain, or
Counter Stance's reflect). No cell won: the solo player never kills the Captain.

| Cell (player / rules / mode) | Won / wiped / stalled at 150 rounds | Boss wave reached % | Wave 2 rounds median (p90) | UC casts per fight median (mean, max) | Max hit on player median (max, by) | Phase 2 reached % | Captain min HP % median | Sealwright killed % | Captain idle turns (player 2+ away) / turns | Captain move turns | Deaths: main cause |
|---|---|---|---|---|---|---|---|---|---|---|---|
| average / old / close | 0 / 30 / 0 | 90 | 3 (5) | 1 (0.9, 2) | 1,221 (2,036, Sovereign Fetters) | 0 | 100 | 0 | 0 (0) / 51 | 0 | Sealwright 21 (top: Sovereign Fetters); The Captain 4 (top: Unraveling Strike); Deck Warden 3 (top: Chain Hook); own turn (DoT tick or reflect) 2 |
| average / new / close | 0 / 30 / 0 | 90 | 3 (5) | 1 (0.8, 1) | 1,221 (1,890, Sovereign Fetters) | 0 | 100 | 0 | 0 (0) / 48 | 2 | Sealwright 19 (top: Sovereign Fetters); own turn (DoT tick or reflect) 5; The Captain 3 (top: Keelbind); Deck Warden 3 (top: Chain Hook) |
| average / old / kite | 0 / 30 / 0 | 90 | 5 (13) | 2 (2.7, 6) | 1,454 (1,890, Sovereign Fetters) | 0 | 100 | 0 | 60 (60) / 139 | 0 | Sealwright 27 (top: Sovereign Fetters); Deck Warden 3 (top: Chain Hook) |
| average / new / kite | 0 / 30 / 0 | 90 | 3 (6) | 1 (1, 1) | 1,425 (1,890, Sovereign Fetters) | 0 | 100 | 0 | 0 (0) / 65 | 46 | Sealwright 12 (top: Sovereign Fetters); The Captain 10 (top: Explosive Tag Cataclysm); own turn (DoT tick or reflect) 5; Deck Warden 3 (top: Chain Hook) |
| average / old / poke | 0 / 30 / 0 | 90 | 3 (5) | 1 (1.2, 2) | 1,363 (2,036, Sovereign Fetters) | 0 | 100 | 0 | 4 (4) / 58 | 0 | Sealwright 15 (top: Sovereign Fetters); The Captain 10 (top: Final Command); Deck Warden 3 (top: Chain Hook); own turn (DoT tick or reflect) 2 |
| average / new / poke | 0 / 30 / 0 | 90 | 3 (5) | 1 (0.9, 1) | 1,363 (2,036, Sovereign Fetters) | 0 | 100 | 0 | 0 (0) / 55 | 16 | Sealwright 16 (top: Sovereign Fetters); The Captain 9 (top: Final Command); Deck Warden 3 (top: Chain Hook); own turn (DoT tick or reflect) 2 |
| elite / old / close | 0 / 30 / 0 | 100 | 29 (55) | 2 (2.2, 6) | 2,385 (6,658, Explosive Tag Cataclysm) | 3 | 95 | 40 | 1 (1) / 980 | 0 | The Captain 20 (top: Explosive Tag Cataclysm); Sealwright 6 (top: basic attack); own turn (DoT tick or reflect) 4 |
| elite / new / close | 0 / 29 / 1 | 100 | 54 (71) | 1 (1, 1) | 679 (867, Eruption: Splash) | 17 | 68 | 67 | 0 (0) / 1701 | 14 | The Captain 16 (top: Final Command); own turn (DoT tick or reflect) 9; Sealwright 4 (top: basic attack) |
| elite / old / kite | 0 / 4 / 26 | 100 | 142 (146) | 70 (65.3, 73) | 504 (27,201, Explosive Tag Cataclysm) | 0 | 100 | 0 | 1908 (1908) / 3903 | 0 | The Captain 3 (top: Explosive Tag Cataclysm); Sealwright 1 (top: Weakening Strike) |
| elite / new / kite | 0 / 30 / 0 | 100 | 56 (60) | 1 (1, 1) | 679 (867, Eruption: Splash) | 0 | 97 | 0 | 0 (0) / 1649 | 228 | own turn (DoT tick or reflect) 13; Sealwright 9 (top: Weakening Strike); The Captain 8 (top: Final Command) |
| elite / old / poke | 0 / 30 / 0 | 100 | 17 (21) | 7 (7.6, 12) | 10,219 (19,815, Explosive Tag Cataclysm) | 0 | 100 | 0 | 80 (80) / 500 | 0 | The Captain 29 (top: Final Command); Sealwright 1 (top: Weakening Strike) |
| elite / new / poke | 0 / 30 / 0 | 100 | 56 (59) | 1 (1, 1) | 679 (867, Eruption: Splash) | 0 | 97 | 0 | 0 (0) / 1627 | 183 | own turn (DoT tick or reflect) 11; The Captain 11 (top: Final Command); Sealwright 8 (top: Weakening Strike) |


Captain rule fires (all runs of the cell; phase-2 rules are 0-6). Old and new lists differ after index 12.

- **average / old / close**: 8 Hold the Line: 23; 9 Final Command: 24; 10 Keelbind: 16; 13 Stolen Form: 3; 14 Counter Stance: 16; 15 Suppression Writ: 7; 16 Unraveling Strike: 3; 17 Explosive Tag Cataclysm: 1; 18 Windlash Focus: 4; end turn (engine-appended rule): 4
- **average / new / close**: 8 Hold the Line: 21; 9 Final Command: 24; 10 Keelbind: 16; 13 Counter Stance: 17; 14 Suppression Writ: 7; 15 Unraveling Strike: 5; 16 Explosive Tag Cataclysm: 1; 17 Windlash Focus: 2; 19 Close on the nearest player: 3; end turn (engine-appended rule): 1
- **average / old / kite**: 8 Hold the Line: 74; 9 Final Command: 1; 10 Keelbind: 1; 14 Counter Stance: 1; 15 Suppression Writ: 1; 16 Unraveling Strike: 8; 17 Explosive Tag Cataclysm: 6; 19 basic attack: 1; end turn (engine-appended rule): 126
- **average / new / kite**: 8 Hold the Line: 26; 9 Final Command: 6; 10 Keelbind: 14; 13 Counter Stance: 1; 14 Suppression Writ: 3; 15 Unraveling Strike: 8; 16 Explosive Tag Cataclysm: 20; 17 Windlash Focus: 15; 19 Close on the nearest player: 146; end turn (engine-appended rule): 2
- **average / old / poke**: 8 Hold the Line: 32; 9 Final Command: 21; 10 Keelbind: 9; 14 Counter Stance: 9; 15 Suppression Writ: 6; 16 Unraveling Strike: 7; 17 Explosive Tag Cataclysm: 9; 18 Windlash Focus: 1; 19 basic attack: 1; end turn (engine-appended rule): 14
- **average / new / poke**: 8 Hold the Line: 25; 9 Final Command: 21; 10 Keelbind: 8; 13 Counter Stance: 9; 14 Suppression Writ: 6; 15 Unraveling Strike: 7; 16 Explosive Tag Cataclysm: 11; 17 Windlash Focus: 9; 19 Close on the nearest player: 44; end turn (engine-appended rule): 2
- **elite / old / close**: 0 Broadside: 5; 1 Ship's Bell: 5; 2 Steady the Helm: 1; 3 Raise the Gunwale: 1; 4 Omen: Binding Ring: 6; 5 Omen: Rows A: 5; 6 Last Stand at the Helm: 5; 7 Second Wind: 1; 8 Hold the Line: 67; 9 Final Command: 173; 10 Keelbind: 130; 11 after lib-omen-rows-a: end turn: 5; 12 after lib-omen-binding-ring: end turn: 5; 13 Stolen Form: 110; 14 Counter Stance: 237; 15 Suppression Writ: 160; 16 Unraveling Strike: 160; 17 Explosive Tag Cataclysm: 103; 18 Windlash Focus: 205; 19 basic attack: 487; end turn (engine-appended rule): 414
- **elite / new / close**: 0 Broadside: 47; 1 Ship's Bell: 48; 2 Steady the Helm: 5; 3 Raise the Gunwale: 5; 4 Omen: Binding Ring: 53; 5 Omen: Rows A: 52; 6 Last Stand at the Helm: 36; 7 Second Wind: 11; 8 Hold the Line: 29; 9 Final Command: 291; 10 Keelbind: 211; 11 after lib-omen-rows-a: end turn: 38; 12 after lib-omen-binding-ring: end turn: 29; 13 Counter Stance: 377; 14 Suppression Writ: 247; 15 Unraveling Strike: 251; 16 Explosive Tag Cataclysm: 172; 17 Windlash Focus: 363; 18 basic attack: 865; 19 Close on the nearest player: 23; end turn (engine-appended rule): 845
- **elite / old / kite**: 8 Hold the Line: 1958; 9 Final Command: 3; 10 Keelbind: 4; 13 Stolen Form: 1; 15 Suppression Writ: 2; 16 Unraveling Strike: 7; 17 Explosive Tag Cataclysm: 60; 18 Windlash Focus: 2; 19 basic attack: 3; end turn (engine-appended rule): 3861
- **elite / new / kite**: 8 Hold the Line: 30; 9 Final Command: 272; 10 Keelbind: 212; 13 Counter Stance: 389; 14 Suppression Writ: 265; 15 Unraveling Strike: 265; 16 Explosive Tag Cataclysm: 192; 17 Windlash Focus: 393; 18 basic attack: 949; 19 Close on the nearest player: 744; end turn (engine-appended rule): 856
- **elite / old / poke**: 8 Hold the Line: 228; 9 Final Command: 58; 10 Keelbind: 65; 13 Stolen Form: 34; 14 Counter Stance: 40; 15 Suppression Writ: 44; 16 Unraveling Strike: 45; 17 Explosive Tag Cataclysm: 55; 18 Windlash Focus: 66; 19 basic attack: 30; end turn (engine-appended rule): 271
- **elite / new / poke**: 8 Hold the Line: 30; 9 Final Command: 274; 10 Keelbind: 208; 13 Counter Stance: 386; 14 Suppression Writ: 266; 15 Unraveling Strike: 273; 16 Explosive Tag Cataclysm: 189; 17 Windlash Focus: 395; 18 basic attack: 942; 19 Close on the nearest player: 570; end turn (engine-appended rule): 869


| Cell | Marks: Binding Ring / Ship's Bell / Rows A / Broadside | Stuns landed on the Captain (player Stunning Jab casts, wave 2) | Kite: retreat / approach steps, cornered turns, pokes, steps inside range / kite steps | Captain decisions: nearest player 5+ away / pet adjacent while player 2+ away / all | Unmarked set pieces (whole floor) |
|---|---|---|---|---|---|
| average / old / close | 0 / 0 / 0 / 0 | 0 (0) | - | 0 / 13 / 101 | 0/92 |
| average / new / close | 0 / 0 / 0 / 0 | 0 (0) | - | 0 / 14 / 97 | 0/92 |
| average / old / kite | 0 / 0 / 0 / 0 | 0 (0) | 143 / 0, 10, 0, 158 / 316 | 213 / 6 / 219 | 0/92 |
| average / new / kite | 0 / 0 / 0 / 0 | 0 (0) | 125 / 0, 5, 0, 138 / 206 | 126 / 3 / 241 | 0/92 |
| average / old / poke | 0 / 0 / 0 / 0 | 0 (0) | 97 / 99, 1, 39, 245 / 266 | 47 / 9 / 109 | 0/92 |
| average / new / poke | 0 / 0 / 0 / 0 | 0 (0) | 99 / 86, 1, 39, 232 / 253 | 59 / 5 / 142 | 0/92 |
| elite / old / close | 6 / 5 / 5 / 5 | 62 (113) | - | 0 / 12 / 2285 | 0/131 |
| elite / new / close | 53 / 48 / 52 / 47 | 7 (214) | - | 7 / 8 / 3998 | 0/216 |
| elite / old / kite | 0 / 0 / 0 / 0 | 0 (2) | 296 / 0, 3618, 0, 4979 / 5355 | 5868 / 8 / 5901 | 0/121 |
| elite / new / kite | 0 / 0 / 0 / 0 | 0 (177) | 647 / 0, 1442, 0, 2894 / 3049 | 269 / 6 / 4567 | 0/121 |
| elite / old / poke | 0 / 0 / 0 / 0 | 4 (43) | 676 / 644, 6, 302, 1796 / 1884 | 282 / 10 / 936 | 0/121 |
| elite / new / poke | 0 / 0 / 0 / 0 | 0 (178) | 596 / 130, 654, 1055, 3019 / 3086 | 201 / 4 / 4402 | 0/121 |

## 4. Findings

1. **The old Captain against a solo kiter reproduces the live fault.** elite/old/kite: Unbroken Command 65.3 casts per
   fight on average (median 70, max 73), every second round; 49% of his turns idle (1,908 / 3,903); zero moves; 99% of
   his decisions with the player 5+ away. 26/30 fights stall at the 150-round cap (his Cataclysms land on the pets;
   the player is never in reach), 4/30 end in a one-shot or near one-shot (max single hit 27,201, Explosive Tag
   Cataclysm, after 8 casts, wave round 17). Hit-and-run (elite/old/poke) is worse: 7.6 casts per fight, max hit
   19,815, every run lost in 17 rounds (p90 21), 29/30 to the Captain. Close-in old: 2.2 casts, as the party model.
2. **The fix does what it is meant to.** Every new cell: Unbroken Command exactly once per fight (max 1), zero idle
   Captain turns, and he chases (elite/new/kite: the approach rule fired 744 times in 228 turns; elite/new/poke 570;
   average/new/kite 146). Max single hit on the player falls to 867 (elite) / 1,890-2,036 (average, the Sealwright's
   Sovereign Fetters). The kiter now loses every fight in 56 rounds (p90 60) instead of stalling or being one-shot;
   deaths are spread over the Sealwright, the Captain's duel kit and own-turn ticks.
3. **Solo, phase 2 is not reachable while the Sealwright lives.** Its first two rules, Ward of Command (80% damage
   taken down, cooldown 2, 2 rounds) and Mending Seal (20% heal, cleanse), target the Captain unconditionally. The
   solo auto-player targets the closest opponent and no kiting cell ever killed the Sealwright (0%); the Captain's
   median low point is 97-100% HP in every kiting cell. Only elite close-in kills the Sealwright (old 40%, new 67%, at
   wave round 26) and then reaches phase 2 (old 3%, new 17%). In elite/new/close the whole phase-2 chain runs:
   Steady + Gunwale 5/5 transitions, Binding Ring → Ship's Bell 53 → 48, Rows A → Broadside 52 → 47, Last Stand 36,
   Second Wind 11. The average solo player never reaches phase 2 in any cell (dies to the Sealwright first, 12-27 of
   30 per cell). The solo players are harness tiers, not calibrated to the live player (whose log shows Keelbind
   4,407 → 400,930 over 11 casts); absolute hit sizes here are not comparable with the live numbers.

## 5. Other things seen in the traces

- **Move semantics.** `move_towards_opponent` CLOSEST_OPPONENT stops beside its target and does nothing when the
  target is within 1 hex. That target can be a pet, while his basic attack is gated on a PLAYER within 1. This
  happened in only 3-14 of up to ~5,900 decisions per cell (third table, "pet adjacent while player 2+ away"). Idle turns
  stayed 0 because his ranged duel rules (Final Command, Keelbind and Cataclysm, ranges 4-6) fire first. Not a
  practical fault in these runs.
- **Stun immunity expires on long fights.** stunprevent is 99 rounds. Stuns landed on the new Captain only in the two
  elite/new/close fights longer than ~100 rounds (seed 11: 142 rounds, 5 stuns; seed 27: 116 rounds, 2 stuns). The
  old Captain took 62 stuns in elite close. Seed 11 is also the only run with more than one mark not followed by its
  blast (Ring 23 / Bell 20). Every other mark-without-blast gap is the single mark laid in the turn the fight ended.
  (I inferred the expiry from round counts; I did not trace it step by step.) Unbroken Command's own 99-round buff
  also expires on the same clock. No other stunprevent side effect was seen (no Skyglass marker uses stunprevent).
- **Unmarked set pieces: 0** in every cell (`fallbackGuard`; the counts include wave 1's Deck Warden blasts).
- **Hold the Line still fires once in close-in fights** (0.8-1.0 per fight). That is the opener, now once per fight.
- **The strict kiter is cornered most turns.** The arena is 12×10 (`getDefaultBattleSizes`, QUEST, level 50+). The
  Sealwright closes only when 6+ away and casts from 5, so "5+ from every enemy" is rarely possible: elite/old/kite
  spent 4,979 of 5,355 kite steps inside 5 hexes and was cornered in 3,618 turns. Kiting from the Captain alone
  (ignoring the Sealwright) was not modelled.
- **Engine pin.** 3314d122 differs from the harness default c86f43f4 in copy/mirror (Stolen Form) and raid-only paths.
  Stolen Form fired 110 times in elite/old/close, and that rule is gone after the fix.

## 6. Not modelled

- The live player's build, the pets' real records (no pet capture exists), and a second engine pet (the engine allows
  one per owner; the second here is a harness clone).
- Target priority. The auto-player shoots the closest opponent; a person would focus the Sealwright.
- Kiting relative to the Captain only. The wave-1 Deck Wardens are fought close-in.
- The 60-minute dungeon clock. Stalls stop at the harness's 150-round cap.
- Factor isolation. The `--uc-cooldown` and `--stunprevent` flags exist but were not run separately.

## 7. Commands

```bash
# 12 cells (variant x rules x mode), each:
TNR_ENGINE_PIN=3314d122c93e036618483d18229a793ad7ad21fd TNR_SCRIPT=kite.ts harness/skyglass_wreck_sim/run.sh \
    --variant {average|elite} --rules {old|new} --mode {close|kite|poke} --runs 30 --seed 1 --pets 2 \
    --out harness/skyglass_wreck_sim/results/kite_<variant>_<rules>_<mode>.json
python3 harness/skyglass_wreck_sim/tools/kite_tables.py
```
