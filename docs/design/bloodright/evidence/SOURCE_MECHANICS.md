# Bloodright source mechanics dossier

**Source pin:** `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050` (the supplied review pin). Read locally from a shallow checkout of that exact commit on 2026-10-03; at read time `origin/main` of the game repository resolved to the same SHA, so there is no pin-to-main drift for the files below. A source read proves what the code does, not what is deployed.

Every claim here is **source-verified** (file and line cited) unless marked otherwise. Nothing here was executed; no live request was made.

## 1. Potency resolver — `app/src/libs/combat/potency.ts`

| Fact | Lines |
|---|---|
| Supported tags are `PotencyTagTypes` from `app/src/validators/combat.ts`: damage, increasedamagegiven, decreasedamagegiven, increasedamagetaken, decreasedamagetaken, afterburn, lifesteal, reflect, increaseheal, heal. | potency.ts 51; validators/combat.ts 152–163 |
| Modifiers are `increasepotency` / `decreasepotency` **user effects on the caster** (`effect.targetId === casterId`), not new, still active, not sealed. Ground potency on the caster's tile is projected in as well. | potency.ts 74–83; actions.ts 950–971 |
| Only `action.type === "jutsu"` is modified; item and basic actions return untouched clones. | potency.ts 63–64 |
| A modifier carries `affectedTag` (`none`, `all`, or one supported tag), `affectedElements` (list of `ElementNames`), `calculation` (`static` or `percentage`), `rounds` 1–100 (default 3), `target` default SELF. | validators/combat.ts 166–188 |
| Per supported row: `elements = row.elements if non-empty else ["None"]`. A modifier matches when (`affectedTag === "none"` and an element matches) or ((`affectedTag === "all"` or equals the row tag) and (modifier has no elements or an element matches)). | potency.ts 107–120 |
| Arithmetic: `base = power + level × powerPerLevel`; `power = max(0, base + Σflat) × max(0, 1 + Σpct/100)`; percentage-valued rows are then capped at 100; `powerPerLevel` is set to 0 on the clone so ticks/transfers do not re-scale. | potency.ts 122–128 |
| Static modifiers therefore add raw power (Damage/Heal rows) or percentage points (percentage rows) before the row's own calculation runs. A 35% row with +5 static becomes 40%. | potency.ts 101–127 |
| Stacking: `BATTLE_TAG_STACKING = true` at this pin, so duplicate potency keys are **not** collapsed; the dedup branch only runs when stacking is off, and even then bloodline, sage-mode and pre-battle gear (armor/accessory) sources bypass it. Stack key includes type, creator, target, fromType, affectedTag, calculation and sorted elements. | potency.ts 84–95; app/drizzle/constants.ts 1562, 3108–3112; util.ts 1103–1110 |
| Modifier percentage amounts are clamped to 100 before use; flat amounts are not clamped. | potency.ts 101–104 |

**Consequence for Bloodright:** a skill-tree entry whose `effects` hold an `increasepotency` tag is exactly the existing delivery vehicle. What does **not** exist is a whole-kit classification: the resolver reads each row's own `elements`, so a Taiyo Kami buff row with no elements is reachable only through `None`, which also reaches every other non-elemental row on any jutsu the player casts. The brief's "classification inheritance" is the proposed resolver change.

## 2. Skill tree — purchase, prerequisites, realization

| Fact | Lines |
|---|---|
| `SkillTree` table: `name` **unique index**, `effects` JSON, `target` (SELF/ENEMIES/ALLIES), `tier` tinyint, `requiredSkillIds` JSON list, `costSkillPoints` int default 1, `hidden`, `skillType` (DEFAULT/SPECIAL), `folderId`. `UserSkill` has a unique (userId, skillId) index and an `activated` flag. | app/drizzle/schema.ts 600–660, 668–690; constants.ts 646, 655 |
| `purchaseSkill` requires **every** id in `requiredSkillIds` to be an activated user skill, computes available points as `user.skillPoints − Σ activated costSkillPoints`, and refuses when the cost exceeds that. SPECIAL skills must already be owned (unlocked) before activation. | skillTree.ts 170–251 |
| There is no separate Bloodright Point ledger, silver purchase path or current-bloodline gate in this router; folders are presentation only. | skillTree.ts (whole file, 949 lines) |
| Reset: `resetSkillPoints` deletes all user skills and refunds; paid in reputation unless staff/GOLD monthly free. | skillTree.ts 413–500 |
| At battle init, every activated skill's SELF-target effects are realized onto the bearer with `isNew=false`, `castThisRound=false`, `fromType="skill"`; ALLIES/ENEMIES targets are applied after `usersState` exists. Skill-tree (and bloodline) effects are skipped in `RANKED_PVP` and `RANKED_SPARRING`. | combat.ts 3072–3115, 3435–3461; 3053–3054, 3076–3078 |
| Because the realized potency effect is not new, it is already eligible on the first cast of the battle (the resolver skips only `isNew` modifiers). | potency.ts 78; combat.ts 3098–3099 |
| `fromType="skill"` is a Stage 1 (pre-battle) damage-modifier source; bloodline/jutsu are Stage 2. This staging concerns IDG/IDT-type modifiers themselves, not potency. | util.ts 1121–1130 |

## 3. Tag handlers relevant to the ten supported tags — `app/src/libs/combat/tags.ts`

| Tag | Behaviour at the pin | Lines |
|---|---|---|
| `getPower` | `power + level × powerPerLevel`; percentage calculation hard-capped at 100. | 3437–3446 |
| damage (`damageCalc`/`damageUser`) | formula → `powerEffect(atk, def, level, power, config)` with sqrt stat/general scaling; static → raw power; residual rounds use `residualModifier`; `dmgModifier` (weakness) multiplies. Instant hits write `consequence.damage` and `baseDamageForModifiers`; residual ticks write `consequence.residual`. | 1465–1535, 1560–1615 |
| increase/decreaseDamageGiven | buff/debuff-prevent gated; percentage change = `power/100 × baseDamageForModifiers` (staged base), **added** to the consequence, multiplied by `getEfficiencyRatio` (1 when stat/general/element tags overlap, else 0; pierce always 1). Bloodline-sourced modifiers multiply instead and honour `allowBloodlineDamageIncrease/Decrease`. | 917–1000; util.ts 1137–1150; 3477–3510 |
| increase/decreaseDamageTaken | same arithmetic on the target side; applies to direct and residual damage. | 1004–1085 |
| **afterburn** | Enemy-side debuff. On following rounds, for every `consequence.damage` the debuffed target receives (any attacker, **pierce excluded**): `convert = floor(damage × power/100) × ratio`; cumulative Afterburn per hit capped at `floor(damage × 0.6)`. Applied as extra damage to the target after the hit. **Not a standalone hit; potency changes the percentage only.** | 1982–2026; process.ts 896–904 |
| lifesteal | Caster-side buff (effect.targetId is the one dealing damage): `floor(damage × power/100) × ratio` healed to the attacker; shares one **60% of pre-shield damage** leech budget with vamp (`DAMAGE_LEECH_CAP_RATIO = 0.6`); requires target and attacker alive; healprevent on the caster blocks it. | 2028–2056; process.ts 730–735, 905–925; constants.ts 26 |
| reflect | Buff on the one receiving damage: `floor(damage × power/100) × ratio` returned to the attacker, final reflect capped at 60% of pre-shield damage; bypasses shield absorption. | 1828–1860; process.ts 876–887, 638–642 |
| heal | Static heal = `power × applyTimes × 10` HP (the ×10 is hard-coded); percentage heal = `maxPool × power/100`; rounds=0 applies on the cast round, rounds>0 only on following rounds. Pools selectable. | 1721–1775 |
| increaseheal / decreaseheal | Run after the post-damage family; adjust `heal_hp`, `lifesteal_hp`, `vampRatio` (percentage of the value, or flat), and `absorb_hp`. | 1110–1195; process.ts 418–445, 598–612 |
| wound / shield / stun / pierce / absorb / poison / drain / summon / recoil / seal / prevent family | Not potency targets; unchanged by any Bloodright node. Recoil and afterburn skip pierce damage. | validators/combat.ts 152–163; 1944–1980 |

Ordering (`process.ts` 415–612): non-damage-modifier effects → damage modifiers → pierce → post-damage family (wound, afterburn, reflect, recoil, lifesteal, absorb) → heal adjusters → consequences applied.

## 4. Injected jutsu and action level

| Fact | Lines |
|---|---|
| `injectjutsus` grants temporary `jutsu` actions for its rounds; the injected jutsu's **level is the inject effect's `power` (default 1)**, not the user's jutsu level. Injected actions are jutsu actions and therefore pass through the resolver. | actions.ts 793–880 (`handleInjectedJutsus`), 877 |
| Ordinary equipped jutsu actions carry `level: userjutsu.level`. | actions.ts 787 |

**Consequence:** baselines for injected children must be evaluated at level = inject power (100 or 110 in the captured kits, via `power + powerPerLevel × level` of the inject row), not at the planning level 25. Whether an injected child whose `bloodlineId` is empty inherits the bloodline's potency classification is an engine decision (gap register).

## 5. Bloodline passives (context, not potency targets)

Bloodline `effects` are realized onto the bearer at battle init with `fromType="bloodline"` and are suppressed in ranked modes (combat.ts 3053–3069). They are not jutsu rows and are not reached by Bloodright potency; they do interact with enhanced rows downstream (e.g. a bloodline IDG passive multiplies the damage that an enhanced Damage row produces).

## 6. Validators consulted

- `app/src/validators/bloodline.ts` (44 lines): filtering/reskin/pool schemas only; `element` is a string-array filter. No potency classification field exists on bloodlines at the pin.
- `app/src/validators/combat.ts` 1458–1474 (`SkillTreeValidator`): name, description, effects, target, tier, requiredSkillIds, costSkillPoints, hidden, skillType, folderId.

## 7. What was not verified

- Live deployment state (no live request).
- Whether any NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu carries the elements used as classification labels (no full non-bloodline catalog with effect rows exists in the repository).
- Combat outcomes: no simulation of uptime, delivery, caps in practice, or interaction with the main tree beyond the mechanics above.
