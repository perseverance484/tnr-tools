# TNR combat engine: how a fight resolves

Pinned to `studie-tech/TheNinjaRPG` @ `29cd91b` (2026-11-21). Paths are under `app/`. Every claim here is
**source-verified** (file and line cited) unless marked otherwise. Per-tag detail is in `tags/<tag>.yaml`;
tag-to-tag links are in `interactions.json`. `docs/ENGINE_LAWS.md` stays the law text of record; this file
agrees with laws 9, 10, 11, 75 and 76 and gives their mechanism.

## 1. Round and turn

| Step | What happens | Source |
|---|---|---|
| R1 round start | Every fighter's AP refills to 100. `battle.round` advances. | `src/libs/combat/turn.ts:64` (`alignBattle` :25) |
| R2 order | Fixed cyclic initiative ring (`calcActiveUser`). No tag reads or changes initiative; summons take their summoner's initiative. | `turn.ts` `calcActiveUser`; `tags.ts:2666` summon |
| R3 turn clock | 60 s per turn. | `src/libs/combat/constants.ts:62` |
| R4 what you may use | `availableUserActions` filters: stealth hides every jutsu and basic attack/heal/clear/cleanse/stances/flee (move, replacement, items stay); disarm hides weapons and weapon jutsu; moveprevent hides move, replacement and move-tag jutsu; summonprevent hides summon jutsu; elementalseal hides 60-AP elemental jutsu; injectjutsus adds jutsu; mastery, cooldown and battle-type gates. | `src/libs/combat/actions.ts:111` |
| R5 AP | Available AP = AP left − strongest stun `apReduction` (incl. stun ground effects on the tile). Jutsu AP ± 10 under timecompression/timedilation (`TEMPORAL_AP_DELTA`). | `actions.ts:1577`, `turn.ts:160`, `drizzle/constants.ts:4581` |
| R6 each action | Cast → effects created (`isNew`, `castThisRound`) → `applyEffects` resolves **all live effects** (section 2). Runs after every action, not once a round. | `src/libs/combat/process.ts:357` |
| R7 round end | For every user and ground effect not cast this round: `rounds = max(0, rounds-1)`; then `isNew=false`, `castThisRound=false`. Curses with 1 round left settle (pay stored heal) if an enemy is still in the fight. Ground effects expire. Masteries refresh. Sage exhaustion applies. | `turn.ts:58-121` |

## 2. One action: applyEffects stages

Order inside `applyEffects` (`process.ts:357`) and `EFFECT_SORT_RANK` (`src/libs/combat/util.ts:1062`).
Tags with no rank sort last in the main pass.

| Stage | Contents |
|---|---|
| A0 cast prep | `elementaldamage` becomes `damage` with the caster's element (`elementalDamage.ts`); potency changes cast tags' power (`potency.ts resolvePotencyTags`); barriers on the path set `barrierAbsorb`; stealthed enemies are skipped as targets (`actions.ts:1157`). |
| A1 | `copy`, `mirror` run first. |
| A2 prevents | stealth, buffprevent, cleanseprevent, clearprevent, debuffprevent, fleeprevent, healprevent, moveprevent, onehitkillprevent, robprevent, sealprevent, stunprevent, summonprevent, disarm, weakness |
| A3 pre-modifiers | elementalseal, injectjutsus, activatesagemode, cleanse, clear, increaseaggro, decreaseaggro, increasepotency, decreasepotency, decreasepoolcost, decreasestat, decreasemastery, increasepoolcost, increasestat, increasemastery |
| A4 mid-modifiers | barrier, shield, finalstand, diffuse, clone, redirection, damage (raw written), flee, heal, onehitkill, rob, seal, stun, summon |
| A5 late main pass | timecompression, timedilation, move, visual, then unranked: vamp, curse, consume, siphon, immunity, increase/decreasemaxpools, increaserange, increase/decreasecooldown |
| A6 | Instant kills resolve; consume/siphon conversions registered (after activation, Clear and prevents, before damage). |
| A7 diffuse | `applyDiffuseToConsequences` (`damagePipeline.ts:381`, called `process.ts:643`) defers each holder's share of non-lethal hits. |
| A8 damage pipeline | `applyDamageModifierPipelineToConsequences` (`process.ts:525`) runs `computeDamagePacket` on every damage/residual consequence (section 4). |
| A9 pierce | Pierce resolves after the pipeline (`process.ts:616`), so no damage modifier touches it. |
| A10 post-damage | Parry split (`process.ts:625`), then `POST_PIERCE_TAGS` (`constants.ts:266`): lifesteal, drain, poison, afterburn, absorb, recoil, reflect, parry, wound, decreaseheal, increaseheal; parry returns; diffuse repayment; heal adjustments. |
| A11 curse | Live curses add half power% of hits dealt and taken to `storedHealing`. A new curse starts collecting on the next action. |
| A12 soak and apply | `mitigateConsequence` (`process.ts:956`): shields soak (pierce destroys all shields; reflect- or wound-typed packets skip them), then Final Stand floors HP at 1 (`tags.ts:2209`); `applyConsequence` changes pools; consume/siphon shields granted. |

## 3. Effect lifecycle rules

- **Two apply groups** (`process.ts:1514` and `:1595`). *Ticking* tags (damage residual, heal, drain, clear, cleanse, flee, rob, seal, stun, wound, onehitkill, pool cost, aggro) apply when new and then only when the effect's holder is the actor, so once a round on the holder's turn. *Always-apply* tags (stats, mastery, damage and heal modifiers, potency, absorb, reflect, parry, recoil, afterburn, lifesteal, vamp, prevents, shield, curse, copy, mirror, time shift, redirection, finalstand) run on every action resolution.
- **Live next round.** Damage modifiers need `!isNew && startRound !== curRound` (`damagePipeline.ts:154`); stats, mastery, absorb, reflect, parry, recoil, afterburn, lifesteal and heal modifiers gate on `!isNew && !castThisRound`; potency skips `isNew`. Law 75. `damage`, `heal`, `pierce` with rounds 0 are instant.
- **rounds**: 0 = instant. N = lasts N round changes after the cast round. No tag changes another effect's rounds; effects end early only by removal (`rounds = 0`) or a failed land roll.
- **Land rolls.** Many tags roll `power%` once on landing and set `rounds = 0` on a miss: prevents, stun, seal, stealth, elementalseal, weakness, shield, finalstand, copy, mirror, timecompression, timedilation. Clear, cleanse and flee re-roll every tick until they hit.
- **Prevents** (`tags.ts:2991 preventCheck`, `:338 applyPreventTag`). A prevent rolls power% to land; on success its power becomes 100, so every later check is certain. It blocks only effects with `createdRound` **later** than its own: effects already on the holder, and effects cast the same round, get through. Immunity cancels a *new* prevent of its `blocks` type (`tags.ts:230`).
- **Polarity** (`validators/combat.ts:1298` positive, `:1332` negative). Clear removes all positive, Cleanse all negative, except effects from persistent sources: pre-battle gear, keystones, skill, village, ranked, elementalMastery, bloodline, sageMode, sageModeAfter (`drizzle/constants.ts:4659`). Clear is itself negative, so Cleanse removes a pending Clear. Unclassified (neither can touch): clearprevent, cleanseprevent, injectjutsus, finalstand, diffuse, barrier, clone, copy, mirror, vamp, activatesagemode.
- **Seal** disables every bloodline-sourced effect on the holder once the seal is no longer new (`util.ts:921 isEffectEnabled`, `:943 sealCheck`).

## 4. Damage formula (one packet)

`tags.ts:1352 damageCalc` then `damagePipeline.ts:501 computeDamagePacket`.

```
raw   = baseline * (power / ep_normalization) * advantage          # tags.ts:1323 powerEffect
        baseline  = calcHP(attacker level) / base_hits
        advantage = clamp(1 + amplitude*((atk/def)^curve - 1), advantage_min, advantage_max)
        atk/def   = stats_scaling*sqrt(offence|defence) + gen_weight*sum(sqrt(general))   # increasestat/decreasestat move these
      * residualModifier (ticks only) * dmgModifier * weakness.dmgModifier (biggest match)
      # potency already changed `power` at cast
d = raw * curseBonus                                   # attacker's curse damageBonusPercent; not pierce
d *= Π(1 + p)   pre-battle % increases (gear/skill/village/ranked, stage 1)
d *= 1 + (60 + atkGearIncGiven + defGearIncTaken + elementalGearPts)/100
d *= Π(1 + p)   in-battle % increases: increasedamagegiven (attacker) and increasedamagetaken (defender); no cap
d *= 1 - (50 + defGearDR + atkGearDRgiven + elementalGearDR)/100
d *= Π(1 - p)   pre-battle % DR, then in-battle % DR: decreasedamagetaken (defender), decreasedamagegiven (attacker)
floor = (boosted d) * (1 - 0.50) * (1 - 0.9)           # never below 10% of the post-system-DR hit (DMG_REDUCTION_CAP)
d = max(d, floor) + Σ static increases ; d = max(floor, d - Σ static reductions)
d *= keystone inc ; d *= keystone DR ; d = max(d, floor)
d *= Π bloodline % inc ; d *= Π bloodline % DR         # skipped under seal; damage tag may opt out
```

Then, outside the packet: diffuse defers its share, parry splits its share (cap 100%), readers take their
cut (lifesteal+vamp 60% shared, absorb 60%, reflect 60%, afterburn 60%, `constants.ts:80-92`), shields soak,
Final Stand floors HP at 1. **Pierce** uses `raw` only (no curse bonus, no pipeline), destroys all shields,
and is ignored by parry, recoil and afterburn. **Onehitkill** sets HP to 0, skipping shields and Final Stand.
Drain, poison and wound don't use the formula.

## 5. Stacking and caps

| Rule | Value | Source |
|---|---|---|
| Same tag, same caster, same target | stacks (`BATTLE_TAG_STACKING = true`) | `drizzle/constants.ts:2437`, `util.ts:962` |
| % increases | multiply: Π(1+p) (law 9) | `damagePipeline.ts` |
| % reductions | multiply: Π(1−p), floor 10% (law 10) | `drizzle/constants.ts:4576` |
| Copy / Mirror | 4 held per caster; priority tiers; no passive or gear sources | `drizzle/constants.ts:4610-4690` |
| Lifesteal + vamp | 60% of the hit, shared, vamp first | `constants.ts:80` |
| Absorb, reflect, afterburn | 60% of the hit each | `constants.ts:86-92` |
| Parry | sums to 100% | `drizzle/constants.ts:4578` |
| Diffuse | 99%, default delay 3 rounds | `drizzle/constants.ts:4579-4580` |
| Only one counts | strongest stun; biggest weakness; one timecompression and one timedilation at a time | `turn.ts:160`, `tags.ts:1405`, `tags.ts:2499` |
| Shield HP | max 100000 | `drizzle/constants.ts:2491` |

## 6. Base fields every combat tag has

`validators/combat.ts:121 BaseAttributes`: `rounds` (int 0-100), `power` (−100..100; PowerAttributes makes it ≥0),
`powerPerLevel`, `direction`, `target` (INHERIT | SELF | COORDINATES), `coordinateTargeting`, `friendlyFire`
(ALL | FRIENDLY | ENEMIES), `calculation`, `timeTracker`, plus animation and sound fields. Effective power =
`power + level * powerPerLevel`. Each `tags/<tag>.yaml` lists only the tag's own fields.
