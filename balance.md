# Balance doctrine and quest tiers

> Migrated from `30_DOCTRINE_balance.md` + `33_DOCTRINE_quest_tiers.md` (Phase 3, 2026-08-26).


Cross-cutting design philosophy the per-domain guides defer to. This file owns the rules that are not specific to one content type: the hard combat rules, the two damage-tier scopes, timing, keystone philosophy, item doctrine, reserved decisions, and the canon-promotion gate. When a domain guide and this file agree, follow either; when a domain guide specifies something narrower for its type (for example the AI-enemy damage curve in `21_GUIDE_ai_enemy.md`), the domain guide wins for that type.

---

## 1. Hard rules

These hold across all combat content:
- **Action cost is 40 or 60 only.** Nothing else is a valid AP value.
- **Damage counts as a tag.** It occupies one of the tag slots.
- **Maximum 3 tags per ability**, 2 preferred. Tags are an identity, not a kitchen sink.
- **No inferred mechanics.** If a behavior or value is not confirmed, it is `NOT_RECORDED`, not a guess.
- **Preserve exact values.** Do not silently round or "improve" canon numbers.

## 2. Damage tiers (two separate scopes, do not mix)

There are two damage-tier systems. They share words like "light" and "nuke" but the numbers are different and they apply to different content. Keep them straight.

**Player jutsu tiers** (used in `20_GUIDE_jutsu.md`):

| Tier | Value |
|---|---|
| Light | 38 |
| Normal | 40 |
| High | 45 |
| Nuke | 50 |

**AI enemy attack weights** (used in `21_GUIDE_ai_enemy.md`, then scaled by the enemy's level and rank): baseline Light 40 / Normal 50 / Heavy 60, with a standard level-50 enemy sitting below baseline (about 38 / 40 / 45) and an endgame level-100 boss well above it (about 50 to 60 / 65 to 70 / 75 plus). Piercing damage uses its own higher curve. The full table and scaling live in guide 21.

The collision is only in the labels. A "nuke" player jutsu is 50; an AI "heavy" baseline is 60 before scaling. Always say which scope you mean.

## 3. Combat timing

- **Damage** resolves immediately on use.
- **Buffs and debuffs** queue and activate at the start of the next round.
- **Cleanse** is instant and removes queued negative effects.
- **Clear** removes positive effects from the target.
- **Stun** is minus 40 AP on the stunned user's next turn.

## 4. Jutsu generation doctrine

- **40 AP is setup or utility with no damage by default.** 60 AP is where damage is expected.
- **Three tags are an identity, not a maximum to fill.** Prefer two.
- **Movement targets ground or self,** not direct enemy debuffs. (This is a player-side rule; AI enemies do not take self-reposition movement jutsu at all, see guide 21.)

## 5. Keystone philosophy

- A keystone exists to enable an **alternate playstyle, not a raw power upgrade.** It should change how a kit plays, not simply make it stronger.
- The B-rank shape is: a base kit, plus a cornerstone, plus two alternate keystone jutsu.
- **Weakness-swap rule:** changing a weakness must introduce a new weakness. You may move where a kit is vulnerable, but you may not remove vulnerability for free.

## 6. Item and weapon doctrine

- **Default to Legendary rarity** for new gear; most active players have outgrown Epic and below. Overridable per request.
- **Damage is multiplicative, all the way down (corrected 2026-07-18).** Not only do separate Increased-Damage-Given buckets (stat-scoped versus element-scoped) multiply together, SAME-TYPE percentage rows within one scope ALSO multiply: total = product of (1 + p_i) across every row, tag and item alike. The earlier "same-scope sums" reading was a small-power measurement artifact (30+30 vs x1.69 is indistinguishable in one fight log); at scale the truth explodes (thirty 100-rows = x2^30, observed live as trillion-damage hits). Build all AI damage tuning as row products (12_TECH law 9), and never exceed ~4 same-type 100-rows on one record without doing the product math first. DDT rows likewise multiply as (1 - p_i) products.
- **Pierce bypasses damage modifiers.** Pierce-type hits ignore DDT and read outside the IDG amplification; they sit at raw-base values amid otherwise amplified numbers. NEVER use a pierce hit as a calibration reference; it will mislead the diagnosis (it did). **Design consequence (banked 2026-08-01):** pierce is FLAT - it cannot be scaled by any bucket the player or the AI stacks, so it is a floor-breaker/finisher tool, never the scaling spine of a kit; a boss concept built on scaling pierce is dead on arrival (one already was). Precise exemption map per R16: pierce skips recoil and afterburn but triggers lifesteal and is always reflectable/absorbable.
- **Ramps compound.** A x1.2-per-cast stacking self-buff is exponential over a fight; round-gate or cap every ramp.
- **Calibration protocol.** One sniffer anchor fight against a DECLARED dummy loadout (state it in the design doc); derive the base swing; build per-tier row products toward per-hit targets; verify with one fight per tier. Player DDT is nonlinear: numbers tuned against tank-endgame mitigation land 2-3x harder on normal players. Reference precedent (Crimson Masquerade, vs endgame armor): crew 800-1000, mid 1500-1800, boss 2400+ per hit.
- **Weapon riders stay light.** A weapon costs about 40 AP and deals guaranteed damage, so it should carry at most one modest damage-increase bucket. The multiplicative payoff is meant to come from the player's own stacked sources, not from the weapon stacking buckets by itself. The reference anchor is a weapon at roughly damage 30 plus a 20% increased-damage-taken rider.

## 7. Reserved decisions and standing rules

- **Custom user-owned bloodlines are off-limits** for edits without explicit reason or permission. Ownership cannot be determined from jutsu data alone, so ask when unsure.
- **Reward and balance decisions are Brandon's:** drop rates, enemy counts, stat tuning, reward values, difficulty gates. Fill the structure and mechanics and propose options, but do not finalize these.
- **Generated content is candidate** until explicitly accepted.
- **Capture before inferring.** Every contract in this stack was confirmed against a real save. If an endpoint or field is unconfirmed, capture it (see `10_TECH_pipeline.md`) rather than emitting a guess as verified.

## 8. Canon promotion gate

Before content is treated as canon (rather than candidate), it should clear every gate:
- It is an approved entry.
- Its exact behavior is defined, or marked `NOT_RECORDED`.
- Its values are defined, or marked `NOT_RECORDED`.
- Its allowed use cases are defined.
- Its restrictions or counterplay are defined.
- It appears in active canon or is user-approved.
- It was intentionally promoted (not promoted by accident of being mentioned).


## Addendum (Jul 10 2026): multiplicative-bucket doctrine SOURCE-CONFIRMED

`computeDamagePacket` (app/src/libs/combat/process.ts) applies every percentage IDG/IDT effect as its own `x(1 + power/100)` multiplier, scoped by stat/general/element match. The ruled weapon doctrine (one modest bucket per weapon; stacking belongs to the player across separate sources) is engine-accurate. Additive exceptions: gear/system/keystone POINT pools (summed, then one multiplier) and static-calculation effects. Full pipeline below.

---

## The damage pipeline, in order

> Migrated from `50_DATA_combat_facts.md` on its retirement, 2026-08-26. The VALUES are generated
> into `45e_DATA_constants.json` and are deliberately not repeated here; what follows is the SHAPE,
> which no generated file expresses. Read law 83 before trusting any figure you derive from it.

Sources: `libs/combat/tags.ts` (damageCalc, powerEffect, getPower, getEfficiencyRatio),
`libs/combat/process.ts` (computeDamagePacket), `libs/combat/constants.ts`, `drizzle/constants.ts`,
`libs/profile.ts`.

### Raw damage

```
power     = effect.power + level * powerPerLevel     (capped at 100 when calculation=percentage)
atkPower  = stats_scaling * SUM(sqrt(attacker offence stat)) + gen_weight * SUM(sqrt(attacker general))
defPower  = stats_scaling * SUM(sqrt(target defence stat))   + gen_weight * SUM(sqrt(target general))
epScale   = power / ep_normalization
baseline  = calcHP(attackerLevel) / base_hits
advRatio  = atkPower / max(1, defPower)
advantage = clamp(1 + amplitude * (advRatio^curve - 1), advantage_min, advantage_max)
rawDamage = baseline * epScale * advantage
          * residualModifier (rounds after cast only) * dmgModifier * weakness dmgModifier
```

`"Highest"` resolves to the attacker's `highestOffence` against the TARGET's `highestDefence`,
fixed on the effect at cast; for generals it expands to the user's `highestGenerals` list.
`static` and `percentage` calculations use `power` directly and skip the whole block above.

### The packet, exact order

**Scoping comes first.** A modifier applies only when `getEfficiencyRatio` is 1, meaning it shares at
least one statType, general or element with the damage effect. Elements default to `None` when
empty, so a `None`-scoped modifier does hit `None`-element damage. Pierce forces ratio 1 for reflect
purposes.

1. Stage-1 pre-battle percentage increases: **each effect multiplies** (`damage *= 1 + power/100`).
2. System and gear increase POINTS POOL: additive into one multiplier -
   `OUT_OF_COMBAT_BASE_DAMAGE_INCREASE + gear IDG(attacker) + gear IDT(defender)`, then
   `damage *= 1 + pool/100`.
3. In-battle percentage increases: **each effect multiplies**.
4. Reductions, after boosts, never before.

The stage order is the whole reason the multiplicative-bucket doctrine holds: separate sources land
in separate multiplying stages, while one large source lands in one.

### Afterburn stack cap

Afterburn stacks to **60% total, maximum** (ruled by Brandon, 2026-07-06). This is a design ruling,
not an engine bound - nothing in the source enforces it, so it has to be held in the design.

---

## Reward class and farm-layer doctrine (added 2026-07-27, the Ashen Concord cycle)

**1. Uncapped records pay materials only.** A record with `retryDelay: "none"` and `maxCompletes > 1` can be run without limit, so it must pay zero experience, zero currency, and nothing rare. Materials and profession experience only. An uncapped record that pays a hub wage is an infinite fountain, and one that carries a 1.2% chase drop hands that chase out in an evening.

**2. The reward ladder.** Story chapters pay the full band for their rank. A capped daily pays one unit of that band. Reference, directory, and onboarding records pay a token or nothing. Uncapped lanes pay materials only. Anything that pays a full unit for zero risk is a bug: a five-click directory quest was found paying a complete hub wage.

**3. No item may exist solely to be shown at a door.** Prefer prerequisite chaining, which is free and unlosable. A possession check is a last resort; whatever it gates must be renewable, and the item must be untradeable at cost 0 so it cannot be sold out from under a player. In a linear campaign the completed quest is the proof, and a key layer on top of it is ceremony.

**4. Reveal discipline: at most two open records per beat.** One next story step, and at most one area. Records gated behind a profession rank are exempt, since their audience self-selects. Nine simultaneous reveals is the failure mode this rule exists to prevent.

**5. Profession-exclusive materials come only from rank-gated records.** Never from an open record, never from an item chest table. Everyone else trades for them, which is the point: it is the trade pressure that makes professions worth having. The same applies to materials sourced outside the campaign entirely; name them in the launch post so nobody discovers the dependency mid-build.

**6. Choice rewards offer standouts in different slots.** Three of the same slot in three colors is not a choice, because a player who already has a good one of those gets nothing. Offer pieces that fill different gaps, vary the slots across the tiers of a ladder, and let the lines mix so the question is "what is my weakest slot" rather than "what colour am I".

**7. Aim, do not multiply.** Ten near-identical daily records expressing one idea is worse than one record with a choice at the door, even when the ten pay more in total. Collapse them and raise the per-run pay: a player who can aim a run at the material they need finishes faster in practice than one who must clear a chore list, and the campaign becomes explicable in a sentence.

## Addendum: harvest Stage 1 doctrine facts (2026-08-01)

- **H14. Round gating is AI-rule-only.** There is NO round-gating mechanism anywhere in the player-side item/jutsu vocabulary. AP floors: items floor at 1 AP, jutsu at 10. `timedilation`/`timecompression` carry fixed 10 AP semantics. Any design that says "this player ability activates on round N" is inexpressible.
- **H17. Level-cap doctrine, stated in words:** `JUTSU_TRAIN_LEVEL_CAP = 25` (45b constant). House rule: `powerPerLevel: 0` with the intended MAXIMUM values written directly on the record - what you write is what a maxed jutsu does, no growth curve to model. Guide 20 inherits this.

---


## Observed template (our 13 shipped D-missions)

Median 4 nodes, exactly 1 dialog, 1 to 2 scene characters, 2 backgrounds, 0 to 2 travel stops, zero branches. Shapes in use:

- **Errand:** dialog, move, collect, win (Well Rounds, Cartographer pair, Misfiled Board)
- **Rounds:** dialog, move, move, collect, win (Lantern Rounds, Runaway Goat)
- **Contract fight:** dialog, defeat_opponents, reset_quest, win (Night Watch Shadow, Poachers' Due, Case Contract Intercept and Site Sweep)

Rewards are flat per tier: exp 173, ryo 1100, tokens 100, prestige 14, clan 100, with the Case Contracts adding an item drop group.

## Node budgets [RETIRED 2026-08-26]

The table that used to sit here (D 10 / C 15 / B 20 / A 20+) was a ballpark estimate written before the new
missions existed, and shipped work immediately broke it: Copies, Not Thefts is 25 nodes at B, Witness Detail
is 21, while the D set runs 3 to 6 against a nominal cap of 10. D missions come in well under, B missions run
over. Ruling: **node count is not a constraint.** A mission is as large as its idea needs.

New bands will be derived from shipped data once there are four or five B builds to average, not estimated
again. Until then the only structural rules are the counting rule below and the quality bar.

Counting rule: every node in `objectives` counts, including `reset_quest` and the `win_quest` terminator. A
`reset_quest` node carrying `resetObjectiveId` rewinds the tracker to that objective. Branch nodes count once
each, so a two-way choice that merges costs two nodes, not one.

## Quality bar, independent of size

Node count is the budget, not the goal. Within any tier:

- Every dialog beat carries voice, not instructions. "Fetch the thing" is a task line, not a scene.
- Travel legs exist because the story moves, never to pad the count.
- Art per quest: at least one scene character and one background, ideally a background change when the location changes.
- A branch is worth a node only when the choices read differently. Two flavors of yes is filler.
- Rewards stay at the tier's flat scale unless ruled otherwise.

## Client display laws (learned in play, 2026-08-24)

- `reset_quest` and `win_quest` descriptions are **never shown**. Both need a dialog node immediately before them: one to tell the player the choice was wrong before the rewind, one to play the payoff before the quest closes.
- Only one scene character renders per node. Multiple entries stack at the same position.
- Node-level `image` is the **sector map pin art** (`libs/threejs/sector.ts` drawQuest). No image means no pin. The pin is tinted by task: travel yellow, collect and deliver purple, defeat red, dialog purple.
- A scene character's apparent size is its share of its own canvas. Small subjects need transparent padding or they render at human scale.

## Art doctrine (ratified 2026-08-24)

**Village neutral by default.** No more village-restricted scene art. A village quest uses interiors and neutral exteriors that could belong to any village: mission counters, offices, archives, storerooms, corridors, courtyards seen tight. Avoid climate extremes in anything a player might see from more than one village.

Outdoor illustration with real character is saved for **global map travel**, away from the village, where the location is genuinely somewhere specific.

The Hyorin set (Village Street, Outskirts, Hollow Pine, Elder Yukino, Mochi) stays in use for One White Ear, but no further village skins get produced. The village art system plan is superseded.
