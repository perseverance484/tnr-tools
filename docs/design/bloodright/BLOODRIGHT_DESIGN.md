# Bloodright — system design and balance brief

**Status:** FOUNDATION DRAFT for balance-team review packaging  
**Date:** 2026-10-04  
**Authority:** design support only; exact balance values remain director-owned  
**Canonical mechanics:** existing Bloodright tree sources, `docs/RULINGS.md`, `docs/design/bloodright/BALANCE_REVIEW_METHOD.md`, and pinned source-mechanics evidence

> This document explains what Bloodright is trying to accomplish and how the balance team should reason about it. It is not a substitute for the canonical tree JSON and does not approve any new numbers by itself.

## 1. Product concept

Bloodright is a bloodline-focused **horizontal specialization system**. It does not primarily give the player new attacks. Instead, it lets a player spend a very small permanent budget to deepen selected properties of jutsu that already belong to the bloodline's qualifying potency classification.

The intended player question is not:

> “How do I buy everything?”

It is:

> “Which part of this bloodline do I want to become exceptionally good at?”

A Bloodright tree therefore succeeds when its routes create distinct, credible playstyles and the four-point budget forces a real opportunity cost.

## 2. Core player experience goals

Bloodright should:

1. **Deepen bloodline identity.** The tree should make the bloodline's existing combat language more expressive rather than layering an unrelated system over it.
2. **Create horizontal choices.** Different Advanced Arts should change what the build is best at, not merely provide progressively larger universal power.
3. **Preserve scarcity.** Four Bloodright Points must remain meaningfully insufficient to complete the tree.
4. **Reward commitment without creating one mandatory route.** A route may be strong, but its strength should come with a real opportunity cost.
5. **Remain readable.** A player should be able to look at the tree and understand why they would choose one branch over another.
6. **Respect the real kit.** Balance is based on actual eligible tags, base values, delivery, duration, coverage and downstream mechanics—not tag names alone.

## 3. Current structural model

The normal Bloodright tree uses:

- 2 Foundations
- 4 Hidden Arts
- 4 Advanced Arts
- 10 total skills
- 1 BP per skill
- 4 BP maximum
- at most 1 Advanced Art in a legal build

A normal full specialization is:

`Foundation -> Hidden -> Advanced = 3 BP`

The fourth BP is part of the actual build and must be reviewed as seriously as the named three-node route.

## 4. Potency scope

Bloodright potency is **classification/element-wide**, not bloodline-ID scoped.

A Bloodright modifier applies to matching supported tags on every qualifying jutsu of the Bloodright classification, subject to the implemented resolver contract. Bloodline ownership, equipment provenance and jutsu names are not additional potency selectors.

Equipment may still gate whether a jutsu can be cast.

This matters for balance because an effect with modest native-kit coverage may gain additional value from off-kit jutsu of the same classification.

## 5. What the tiers mean

The tier names should carry design meaning.

### Foundation
Defines the family or axis of the choice.

A Foundation should answer a broad question such as:

- How do I increase killing pressure?
- How do I control the exchange?
- Do I win by protecting myself or weakening the opponent?

Both child branches should make sense as answers to the same Foundation question.

### Hidden Art
Signals commitment and direction.

The Hidden Art should make the route's intended playstyle clearer. It may be setup, a directional lean, or the first part of a specialization.

### Advanced Art
Delivers the payoff.

The Advanced Art should feel like the route became something meaningfully different. High-leverage effects are often better placed here than on the Hidden Art.

## 6. Advanced-Art identity rule

Each Advanced Art should own an idea.

When names are hidden and only mechanics remain, each route should still answer a different player need.

Possible identities include:

- burst / execution
- sustained amplification
- sustain offense
- exposure
- combat dominance
- fortress
- suppression
- retaliation
- attrition
- other bloodline-specific identities

An eligible tag does not deserve a route merely because it exists.

## 7. Balance philosophy

Bloodright is balanced around **meaningful opportunity cost**, not equal-looking printed totals.

The existing +5 / +10 / +15 bands are guardrails and review thresholds, not targets.

Two routes with identical nominal totals can have radically different combat value because tags differ in:

- coverage;
- base value;
- duration;
- delivery;
- downstream leverage;
- threshold effects;
- synergy with the rest of the kit.

The balance team therefore uses two parallel views:

### Nominal Balance Units
A simple, editable common currency used to make the roster easy to compare.

### Impact context
The factual evidence that explains why equal Balance Units may still have different real combat leverage.

Balance Units are an accounting aid, not a combat simulator.

## 8. Impact Envelope

Every route should be evaluated across five dimensions.

### Coverage
How many distinct jutsu and supported rows are affected?

### Magnitude
What does every affected base value become?

### Thresholds
Does the modifier cross a designed breakpoint or cap?

### Uptime and delivery
How often can the enhanced effect matter? Is it instant, delayed, persistent, single-target, area, self-buff, enemy debuff?

### Synergy
Do multiple modifiers reinforce each other? Does one application affect many later hits? Does a native passive multiply the payoff?

A row-weighted score may surface suspicious disparities, but it does not decide balance.

## 9. Damage requires special handling

Current player-jutsu damage tiers:

| Tier | Damage |
|---|---:|
| Light | 38 |
| Normal | 40 |
| High / semi-nuke | 45 |
| Nuke | 50 |

Flat Damage must always be reviewed as `base -> final`.

Examples:

- 40 -> 45 crosses an entire tier.
- 45 -> 50 turns a high/semi-nuke into a nuke.
- 50 -> 55 exceeds the current player-jutsu ladder and is a major warning condition.

For this reason, one point of flat Damage is not interchangeable with one percentage point of IDG, IDT, DDT or DDG.

## 10. Narrow coverage

A route with only one eligible row is not automatically entitled to a very large modifier.

When narrow coverage leaves a route weak, prefer a secondary effect that reinforces its intended identity before inflating the primary tag to an extreme value.

This preserves readable numbers while creating more interesting choices.

## 11. Fourth-BP principle

The balance team must review the actual four-point build, not merely the named Advanced path.

For every Advanced Art, inspect:

- its three-node package;
- every legal fourth purchase;
- the strongest realistic fourth purchase;
- the resulting complete modifier package.

A route that looks fair at 3 BP may become mandatory after its obvious fourth purchase is added.

## 12. Balance-team review goals

The balance team is not being asked to mathematically prove perfect parity.

The team is being asked to answer:

1. Does every Foundation contain coherent sibling choices?
2. Does every Advanced Art own a distinct identity?
3. Is any route clearly mandatory?
4. Is any route clearly dead?
5. Are the assigned tag weights directionally reasonable?
6. Do Damage modifiers create unintended tier jumps?
7. Does the fourth BP create an obvious dominant hybrid?
8. Are narrow-coverage tags being overcompensated?
9. Is filler being added merely to make totals look equal?
10. Would a player understand the opportunity cost from the tree itself?

## 13. Review artifacts

The balance-team package consists of three surfaces:

1. **Bloodright Design & Balance Guide** — this document, finalized after the roster-wide Fable rebalance.
2. **Bloodright Balance Workbook** — interactive tag-weight and route-cost review.
3. **Bloodright Tree Review Pack** — visual tree pages generated from exact approved/proposed SVG structures.

The repository remains canonical. The workbook and review pack are generated review surfaces.

## 14. Workbook model

The workbook uses **Balance Units (BU)**.

Each supported tag receives an editable BU weight per unit. A skill's nominal BU is the sum of its modifiers multiplied by the current team weights.

The workbook also shows:

- eligible jutsu count;
- eligible row count;
- base values;
- Damage tier transitions;
- downstream-leverage notes;
- three-BP route totals;
- strongest legal fourth-BP package;
- reviewer comments and proposed values.

The workbook must never hide impact context behind a single score.

## 15. Approval and source-of-truth flow

Normal review flow:

`Fable proposal -> generated workbook / SVG review -> balance-team adjustments -> director decision -> canonical tree update -> regenerated outputs -> final visual poster`

The spreadsheet is not authoritative by itself.

Any accepted numeric or structural change must return to the repository source that owns that tree.

## 16. Finalization after the roster-wide Fable pass

This foundation intentionally leaves roster-dependent sections unfilled until Fable returns a frozen exact SHA.

At finalization:

- import every final/proposed tree from the frozen Fable head;
- import tag coverage and damage-threshold evidence;
- populate every workbook route and skill;
- seed the calibration sheet with the director-reviewed anchor trees;
- add the exact final roster size and classifications;
- generate the visual review pack;
- identify routes that the workbook flags for balance-team attention;
- freeze the package against the exact source SHA.

No live-game requests or writes are required for the review package.
