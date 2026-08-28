> **STALE - archived 2026-08-28 (rollout Stage 2).** Superseded by the skill references and generated data under /skills/, and by /docs/ENGINE_LAWS.md. Do not build from this file.

# TNR COMBAT FACTS (extracted from TheNinjaRPG-main.zip, app/src/, uploaded 2026-07-04)

## Damage formula (calculation: "formula") - tags.ts powerEffect/damageCalc
- atkStats = sum over effect.statTypes of sqrt(origin.<stat>Offence); defStats = sqrt(target.<stat>Defence)
  - "Highest" resolves attacker highestOffence vs TARGET highestDefence (stored on effect at cast)
- generals via getLowerGenerals(effect.generalTypes, origin.highestGenerals); atkGens/defGens = sum sqrt(value)
- totalAtk = stats_scaling*atkStats + gen_weight*atkGens ; same for def
- epScale = effect.power / ep_normalization
- baseline = calcHP(attackerLevel) / base_hits ; calcHP(level) = 100 + HP_PER_LVL*(level-1)
- advantageRatio = totalAtk / max(1, totalDef); advantageMod = clamp(1 + amplitude*(ratio^curve - 1), advantage_min, advantage_max); bypass (=1) if both powers 0
- dmg = baseline * epScale * advantageMod
- then: residualModifier (if not castThisRound), dmgModifier, weakness dmgModifier (biggest applicable)
- calculation "static": dmg = power directly

## Constants (drizzle/constants.ts)
- DMG_STATS_SCALING=1, DMG_BASE_HITS=10, DMG_CURVE=1.6, DMG_AMPLITUDE=0.75,
  DMG_EP_NORMALIZATION=40, DMG_GEN_WEIGHT=2.0, DMG_ADVANTAGE_MIN=0.01, DMG_ADVANTAGE_MAX=10.0
- DMG_REDUCTION_CAP=0.9 (min 10% of damage always lands)
- MAX_STATS_CAP=450000, MAX_GENS_CAP=200000
- USER_CAPS: STUDENT 20k/20k L10; GENIN 60k/60k L30; CHUNIN/JONIN/ELITE JONIN/ELDER/NONE = 450k/200k L100
- Damage-modifier staging: boosts (increasedamagetaken, increasedamagegiven) BEFORE reductions (decreasedamagetaken, decreasedamagegiven)
- POST_PIERCE_TAGS order group: lifesteal, drain, poison, afterburn, absorb, recoil, reflect, wound, decreaseheal, increaseheal
- BARRIER_DAMAGE_TAG_TYPES = {damage, pierce}
- Grid borders L2 R2 T2 B0; COMBAT_SECONDS=60/round

## CAPS APPLY TO AIs (combat.ts initiateBattle per-user loop -> capUserStats(user))
- The Endless Night record (868k offences / 434k generals) is clamped to 450k/200k at battle init.
- CONSEQUENCE: AI record stats beyond caps are dead weight; boss effectively fights at player-equal caps.
- AI battle stats are in privateState (not exposed via getBattle for opponents).



## Pass 2 additions
- HP_PER_LVL=50 (calcHP(100)=5,050 matches player; boss 11,100 = calcHP(110)=5,550 x poolsMultiplier 2)
- getPower: power + level*powerPerLevel; percentage calc caps at 100
- getEfficiencyRatio (modifier scoping): binary 1/0 - modifier applies if ANY tag overlaps (statTypes with Highest resolved, generals lowered, elements or implicit "None"). Pierce always 1. NOT fractional; "multiplicative buckets" = separate effects each multiplying.
- computeDamagePacket staged order: (1) stage1 pre-battle pct increases -> (2) x(1 + (60 OOC base + gear inc pts)/100) -> (3) in-battle pct increases (each multiplicative) -> [floor snapshot] -> (4) x(1 - (50 OOC base + gear DR pts)/100) -> (5) stage1 pre-battle pct DR -> (6) in-battle pct DR (each multiplicative) -> min-damage floor = afterBoosts x 0.5 x (1-0.9) -> (7) static inc adds, static DR subtracts (seal-checkable) -> (8) keystone inc/DR -> (9) bloodline pct inc/DR (seal-checkable). Every DR clamped by the 10% floor.
- OUT_OF_COMBAT_BASE_DAMAGE_INCREASE=60, OUT_OF_COMBAT_BASE_DAMAGE_REDUCTION=50 (always-on system points)
- ai threshold semantics (ai_v2.ts): has_effect/target_has_effect SUM matching effects' power and compare >= threshold; threshold 0 = unconditionally true. So threshold "1" = presence; "100" IDG = summed magnitude 100. CONFIRMS our rule design.
- preventCheck (stun/seal/buffprevent family): power = percent CHANCE (RNG roll), not binary; prevent only applies to effects created after it; castThisRound prevents are inert that round.
- residual (DoT) damage skips barrierAbsorb; instant = castThisRound && rounds===0; residual = !castThisRound && rounds>0


## Pass 3: CALIBRATION RESULTS (vs live PvE fight GBq4gDfUEUyYcuGcrpdmx)
- PIERCE: model exact to the cent (Death's Storm 732.25 = observed 732.25, constant all fight).
  Pierce bypasses the ENTIRE modifier pipeline: no OOC points, no pct/static DR, no -400, no floor.
- In-battle percentage increasestat CANNOT push stats past the 450k/200k caps (Death's Storm constant
  despite armor +20% stacks proves effective stats stay pinned at cap). Sim clamps adjusted stats.
- EVERY boss hit on the player rode the 10% MINIMUM DAMAGE FLOOR (DMG_REDUCTION_CAP):
  observed = raw x 1.6 (OOC inc) x [1.3 if Crown IDG up] x 0.5 (OOC DR) x 0.1 (floor), verified to 0.68%
  on all 10 distinct hit magnitudes. The player's stacked DR (gear pts + armor stats + bloodline DDT)
  exceeds the 90% cap, so ALL boss damage floors.
  -> ROOT CAUSE "AI deals too little": endgame players breach the DR cap; every boss hit is floored.
  -> The floor scales with boosts (floor = post-boost base x 0.5 x 0.1), so IDG passives lift floored
     damage 1:1. The +60% passive we shipped raises every floored hit by exactly +60%.
- The residual 0.68%: unmodeled small constant (suspect gear inc-damage-taken pts or level detail); park it.
- Player -> boss non-pierce hits: shaped by the -400 static DR item + player seal state gating bloodline
  IDG (sealCheck skips bloodline modifiers while sealed). Not yet locked to <5%; needs gear-point
  extraction from item records + per-round seal timing. Next calibration target.
- Boss level 110 record -> 100 in battle (LVL_CAP). Boss maxHealth 11,100 observed.

## Balance levers proven by the model (for 30_DOCTRINE)
1. vs capped endgame players, boss damage = FLOOR damage; only EP (jutsu power), IDG passives/steroids,
   and increasedamagetaken debuffs on the player move it. Raw stats, level >100: dead weight.
2. Flat static DR items (like the boss's -400) are the anti-player mirror: they force pierce/drain meta.
3. Pierce is the universal wall-breaker both directions (bypasses floor AND flat DR).

## Pass 4: kitchen-sink integration fight (2026-07-06 capture)
CLOSED (live-verified):
- Combo threshold: Law+Unravel fired r4 (stack crossed 100) AND re-armed r11 after strip. Summed-power semantics confirmed.
- Edict stun apReduction 40 live (-40 AP observed); player Boulder Crush stuns -60.
- Element scoping is ONE-SIDED implicit-None: an effect with no elements matches anything; an element-scoped
  effect only matches intersecting damage elements. Proof: boss 2x100% passives (Highest + Shadow scoped) do NOT
  multiply its None-element basic attacks (28.4 constant vs jutsu hits x4).
- OOC system points (60 inc / 50 DR) bind in BOTH directions (variant test unambiguous).
- Gear modifiers (PreBattleGearModifiers) are INVISIBLE in usersEffects; a defender whose gear+system DR breaches
  the 90% cap takes exactly floor damage = post-boost x0.5 x0.1 (matches isolation fights at 0.68%).
- Determinism: identical (jutsu, state) pairs reproduce to the decimal across fights.
- Afterburn = % of the triggering hit POST-mitigation, per source stack (30% Star, 20% Answers verified).
- Stances (default AI rules) are a real modifier lane (~±30%) visible as hit-value splits.

OPEN (calibration debt, not physics):
- Player->boss per-hit replay needs per-VERSION effect timing (same-round isNew semantics) instead of
  per-round pre-states; kitchen fights stack buffs mid-turn.
- Basic attack effective EP unresolved (boss floored basic 28.4 implies ~30 EP or reduced gens weight, not 40).
- Boss 20% DR item: possibly inert in combat (no armor-fromType modifier ever observed on the boss); needs
  one item.get capture or an equip check.
- Player gear DR points: read item records once to replace the breach assumption with the real number.

Calibration scorecard vs gates: fixtures PASS; pierce exact; floored-defender regime exact (0.68%);
boss->player median 25% (basics dominate error); player->boss pending timing fix. NOT yet at the 5% gate.


## Pass 5: stage-1 constants closed (kitchen residual fit, 2026-07-06)
The full pipeline collapses to: dmg = raw(formula) x in-battle scoped multipliers x k, with
k(player->boss jutsu)=1.0467, k(player basic)=0.3209, k(boss->player jutsu)=0.0749, k(boss basic)=0.0281
for THIS matchup (player slotted build vs The Endless Night). Constancy: 15/23 hits exact to <2%,
armor-break explains 2 more (x1.43 regime shift), 3 outliers are same-turn buff timing (harness, not physics).
Basics ride ~x0.31 of the jutsu constant per side (basic-attack modifier).
Boss item confirmed REAL: AI Heavy Armor 20% DDT + 30% increasestat Highest (stats capped -> DDT is the live part).
Player slotted gear: DDT 69 pts (Mask15+Armor30+Claw4+Pill20), IDG 55 BGNT + 10 Highest, Belt 30% absorb,
Aetherion 20% IDT on-target (not observed in-fight; parked). Gear points NEVER appear in usersEffects.
Remaining to 5%-gate: per-version isNew timing in the replay harness; then TTK/turn-engine validation.


## Pass 6: turn engine (sim_turns.py) validated vs kitchen fight
Boss-turn reproduction 9/11 (r12 excluded: boss died, no turn). Engine facts proven:
- The boss evaluates its rules against the POST-player-turn state (buffs you stack in a round are visible to it that round).
- Stun integrates as AP reduction on the boss's next turn(s): -60 from player Boulder Crush suppressed r2-3 and r8-9 kit casts entirely (40 AP < any 60 AP rule).
- Cooldown bookkeeping + the 14-rule cascade otherwise reproduces every observed cast: Crown r1, Edict r5, Chains r6, Star r7, Testament r10.
OPEN: combo-threshold sum semantics: at r4 the Law+Unravel combo fired with visible in-battle IDG < 100,
implying server-side effect sums include an invisible lane (gear IDG 65 pts suspected). One capture can settle it:
a fight where in-battle IDG stays provably < 35 total; if the combo still fires, gear counts.
TTK: engine + stage-1 constants pending final assembly into whole-fight simulation (gate 5).


## CALIBRATION COMPLETE: all five gates (2026-07-06)
1. Repo damage_formula fixtures: PASS (6/6)
2. Per-hit median error <=5%: PASS (1.18% median, kitchen fight, real gear lanes + per-version states)
3. Independent-fight cross-check: PASS (stage-1 anchors uniform across isolation fights, e.g. b->p jutsu 0.2995)
4. Boss rule reproduction: 9/11 (r12 = boss death, no turn); one open semantic: combo-threshold sums appear
   to include invisible gear lanes (settle with one low-IDG live fight)
5. Whole-fight TTK: PASS EXACT (predicted r12 = observed r12; totals -2.0% / +5.2%)

VERDICT AUTHORITY [RULED]: the sim (sim_damage.py + stage1_constants.json + sim_turns.py) now grades
kit/rule/tuning changes offline. Live fights are spot-checks: one per accepted change, plus any mechanic
the sim flags as unmodeled (new tag types, ground effects, summons) which always earns a capture first.
Scope caveat: k constants fitted to this player build vs this boss; recompute per build/enemy from records
(decomposition documented in stage1_constants.json), first novel matchup gets a confirming spot-check.

## Afterburn stack cap (dauntless, 2026-07-06): afterburn stacks to 60% MAX total.
Design consequence: afterburn is a rider, never a primary damage lane.

## AI rule executability law (live-confirmed 2026-07-06, deadlock incident)
Rule selection is CONDITION-ONLY. A matched rule whose action cannot execute (out of range,
moveprevented, combo members unavailable) hard-loops the AI turn with error toasts until the
round timer, and poisons the player's own performAction calls (AI turn runs inside them).
If NO rule matches, the turn ends cleanly ("stands and does nothing") - the only safe terminal.
Consequences: every distance gate must guarantee range; move rules are unsafe vs moveprevent;
unconditional highest_power fallbacks are unsafe beyond melee; combo range semantics unverified
beyond the live-proven Law+Unravel; default rules can contain unsafe basics -> includeDefaultRules false
for lane bosses. d=5 is reachable ONLY by method ALL (range cap 5, single-target kit tops at 4),
so far-lane gates are distance_higher_than 4. Rule cap: 20.

## AI distance-condition semantics (source: ai_v2.ts 253-256, 538-551)
- Comparators INCLUSIVE: higher_than v => distance >= v; lower_than v => distance <= v.
- distance = A* path length boss->target on the obstacle grid; NO PATH => 0 (bug: reads as adjacent).
- Selection metric != execution range check => blocked paths make the AI select unexecutable jutsu => toast deadlock.
- Player-placed barriers (e.g. Earth kit) can induce it. Upstream fix: no-path => Infinity + skip-and-continue on failed execution.

## AI equip fact (live capture 2026-07-06): ai-edit 'jutsus' additions create userjutsu links with
equipped:false. Combat availActions includes ONLY equipped:true. Rules referencing unequipped jutsu
skip silently (no toast). Fix: equip in admin UI, or unequip/re-equip cycle. Original-creation links equip true.


## Addendum (Jul 10 2026, source extraction): the damage pipeline (AUTHORITATIVE)

Sources: `app/src/libs/combat/tags.ts` (damageCalc, powerEffect, getPower, getEfficiencyRatio), `app/src/libs/combat/process.ts` (computeDamagePacket), `app/src/libs/combat/constants.ts`, `app/drizzle/constants.ts`, `app/src/libs/profile.ts`. Supersedes conflicting earlier claims. NOTE: the DMG_* values below are code DEFAULTS; the live values are read from the gameSetting table at runtime (`libs/gamesettings.ts`), which is why the sim's live-fitted overlay remains valid alongside these.

### Raw damage (damageCalc -> powerEffect)
```
power       = effect.power + level * powerPerLevel        (capped at 100 if calculation=percentage)
atkPower    = stats_scaling * SUM(sqrt(attacker offence stat)) + gen_weight * SUM(sqrt(attacker general))
defPower    = stats_scaling * SUM(sqrt(target  defence stat)) + gen_weight * SUM(sqrt(target  general))
              (per statTypes entry; "Highest" resolves to highestOffence vs targetHighestDefence;
               generals: "Highest" expands to the user's highestGenerals list)
epScale     = power / ep_normalization
baseline    = calcHP(attackerLevel) / base_hits            where calcHP(level) = 100 + 50*(level-1)
advRatio    = atkPower / max(1, defPower)
advantage   = clamp(1 + amplitude * (advRatio^curve - 1), advantage_min, advantage_max)
rawDamage   = baseline * epScale * advantage               (formula calculation; static/percentage use power directly)
            * residualModifier (rounds after cast only) * dmgModifier * weakness dmgModifier (largest matching, default 1)
```
Defaults: stats_scaling 1, base_hits 10, curve 1.6, amplitude 0.75, ep_normalization 40, gen_weight 2.0, advantage clamp [0.01, 10.0].

### The packet pipeline (computeDamagePacket, exact order)
Scoping first: every modifier applies only if `getEfficiencyRatio` = 1, i.e. it shares at least one statType / general / element with the damage effect (elements default to "None" when empty, so None-scoped modifiers hit None-element damage). Pierce forces ratio 1 for reflect purposes.
1. Stage-1 pre-battle percentage increases: **each effect multiplies** `damage *= 1 + power/100`.
2. System + gear increase POINTS POOL (additive points, one multiplier): `OUT_OF_COMBAT_BASE_DAMAGE_INCREASE + gear IDG(attacker) + gear IDT(defender)` -> `damage *= 1 + pool/100`.
3. In-battle percentage increases (cast in combat): **each effect multiplies**.
4. -> snapshot `baseDamageAfterBoosts`.
5. DR points pool (system `OUT_OF_COMBAT_BASE_DAMAGE_REDUCTION = 50` + gear DR both sides) -> one DR multiplier.
6. Stage-1 pre-battle DR effects: per-effect DR multiplier. 7. In-combat DR effects: per-effect DR multiplier.
8. **THE FLOOR**: `minDamage = (baseDamageAfterBoosts reduced by system DR) * (1 - DMG_REDUCTION_CAP)` with `DMG_REDUCTION_CAP = 0.9`: 10% of post-boost damage always lands. Applied from here on at every step.
9. Static-calculation increases: ADDITIVE sum, then static reductions: ADDITIVE, floored.
10. Keystone points pools (inc then DR), each an additive pool -> one multiplier, floored.
11. **Bloodline percentage increases: per-effect multiplicative**, then bloodline DR per-effect, final floor.

### Doctrine confirmations and corrections
- **CONFIRMED (30_DOCTRINE ruled)**: separate percentage IDG/IDT sources are per-effect MULTIPLICATIVE in the packet pipeline; stacking distinct scoped sources beats one large source. Gear/system/keystone points are the additive exceptions (pooled before one multiplier).
- **Pierce**: excluded from the damage-modifier pass entirely and processed after it, before post-damage tags; POST_PIERCE_TAGS = [lifesteal, drain, poison, afterburn, absorb, recoil, reflect, wound, decreaseheal, increaseheal] are ordered after pierce because they read pierce's consequences. This matches the fitted "pierce bypasses everything" note.
- **Bloodline modifiers** respect the damage tag's `allowBloodlineDamageIncrease/Decrease` flags (new levers on damage/pierce tags).
- Barrier absorb applies to INSTANT damage only, never residual DOT.
- Seal suppresses static and bloodline modifier effects in the packet pass (sealCheck).

### stage1 sim status
The live-fitted `stage1_constants.json` values remain the sim's calibration (they capture the LIVE gameSetting dmgConfig plus fight-specific gear regimes); source extraction confirms the fitted STRUCTURE exactly (OOC 50 pts, 90% cap floor off post-boost, per-effect multiplicative scoped modifiers, pierce bypass). No recalibration required until a live fight contradicts.

## Cross-references (2026-07-18)
Row stacking is multiplicative (12_TECH law 9); pierce bypasses damage modifiers (law 11); AI stat generation and caps: 12_TECH laws 14-16.
