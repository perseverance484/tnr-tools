> **STALE - archived 2026-08-28 (rollout Stage 2).** Superseded by the skill references and generated data under /skills/, and by /docs/ENGINE_LAWS.md. Do not build from this file.

# 30 - DOCTRINE: Combat and Balance

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
- **Reward and balance decisions are dauntless's:** drop rates, enemy counts, stat tuning, reward values, difficulty gates. Fill the structure and mechanics and propose options, but do not finalize these.
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

`computeDamagePacket` (app/src/libs/combat/process.ts) applies every percentage IDG/IDT effect as its own `x(1 + power/100)` multiplier, scoped by stat/general/element match. The ruled weapon doctrine (one modest bucket per weapon; stacking belongs to the player across separate sources) is engine-accurate. Additive exceptions: gear/system/keystone POINT pools (summed, then one multiplier) and static-calculation effects. Full pipeline: 50_DATA addendum Jul 10.

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
