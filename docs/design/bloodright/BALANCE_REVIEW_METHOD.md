# Bloodright balance review method

**Status:** working director-approved review method; intentionally iterative while the roster is reviewed.
**Date:** 2026-10-04
**Owner:** content-design method. Exact balance values remain director-owned.

This method supplements the structural validator and balance matrix. It does not replace source mechanics, tree JSON, `docs/RULINGS.md`, or director approval.

## Core rule

Bloodright is balanced around **meaningful opportunity cost**, not equal-looking printed totals.

A route is healthy when a player can explain why they would choose it over its siblings and when its strongest legal 4-BP allocation does not become automatic because one tag's real leverage was hidden behind a tidy numerical ceiling.

The global +5 / +10 / +15 bands are **guardrails and warning thresholds, not targets**.

## Review the real kit before the tree

For every supported potency tag, record:

- distinct eligible jutsu;
- eligible effect-row count;
- base values;
- delivery and duration;
- whether the effect is instant or delayed;
- whether rows stack or reinforce one another;
- item/mode restrictions;
- known classification-wide reach beyond the bloodline kit;
- engine-specific leverage that row count does not represent.

Do not treat one point of Damage, Heal, Lifesteal, IDG, IDT, DDT, DDG, Afterburn, Reflect, etc. as interchangeable.

### Damage tier check

Player-jutsu damage tiers are a required review lens:

- 38 = Light
- 40 = Normal
- 45 = High / semi-nuke
- 50 = Nuke

Flat Damage must be evaluated as **base -> final** on every affected jutsu. Crossing a tier is a qualitative change. A 50 -> 55 result is an explicit red flag because it exceeds the current player-jutsu tier ladder.

## Foundation Sentence Test

Each Foundation should describe a coherent family of choices.

Write one sentence that accurately describes both children. If one child does not fit, the tree is probably wired incorrectly.

Examples established during review:

- Shakunetsu Sakura / Ember Dragon's Roots: “How do I increase my killing pressure?”
- Shakunetsu Sakura / Falling Ember Petals: “How do I control the exchange?”
- Blood-Enchanted Eyes / Scarlet Gaze: “How do I win offensively: amplify myself or expose them?”
- Blood-Enchanted Eyes / Iron in the Blood: “How do I win defensively: protect myself or suppress them?”

## Every Advanced Art owns an idea

Hide the names and read only the mechanics. Each Advanced Art must answer a different player need in one sentence.

If two routes can be summarized the same way, one has lost its identity even if their row-weighted totals differ.

An eligible tag does not deserve a path merely because it exists.

## Tier jobs

A useful default:

- **Foundation:** establishes the axis/family of the choice.
- **Hidden Art:** commitment, setup, or directional lean.
- **Advanced Art:** payoff, transformation, or high-leverage effect.

This is not a hard schema rule, but unusually high-leverage effects such as flat Damage should be questioned when they appear too early.

## Impact Envelope

Coverage-weighting is diagnostic only. For each route evaluate:

### Coverage
How many rows and distinct jutsu are affected?

### Magnitude
What does every affected base value become?

### Thresholds
Does the route cross damage tiers, caps, or other meaningful breakpoints?

### Uptime and delivery
How often can the enhanced effect matter, and does it drive later actions?

### Synergy
Do the route's modifiers reinforce or multiply one another? Does setup enhance its own payoff? Does one application affect many downstream hits?

A simple `bonus x row count` score may expose suspicious disparities, but it must never be used to add filler effects merely to make paths equal on paper.

## Narrow coverage rule

When a primary tag has narrow coverage, do **not** automatically raise its magnitude to an extreme number.

First consider an identity-compatible secondary effect.

## Fourth-BP audit

An Advanced route normally consumes 3 BP. The fourth point is part of the build.

For every Advanced Art, enumerate:

- the three-node path package;
- every legal fourth purchase;
- the strongest realistic fourth purchase;
- the resulting complete modifiers.

A route that looks fair at 3 BP can become dominant when its obvious fourth purchase stacks another high-leverage effect.

## Visual review is part of balance review

Render an exact, mechanically faithful SVG before final acceptance.

The SVG is a design tool, not merely presentation. It should expose:

- siblings that visibly offer “more stuff”;
- repeated filler effects;
- confusing Foundation relationships;
- Advanced Arts that read as the same choice;
- unclear progression from Hidden to Advanced.

Revise mechanics before final poster art when the visualization exposes a weak choice.

## Approval discipline

- Fable trees are proposals until director-approved.
- Structural validity is necessary but not balance approval.
- Classification-wide scope means off-kit coverage can increase leverage; unknown non-bloodline coverage must remain explicitly unverified.
- Director-approved tree values should be recorded through the repository's ruling/canonical-source process.
- This method is expected to evolve as additional bloodlines expose new leverage patterns.

## Regression cases

- **Shakunetsu Sakura:** +5 flat Damage on two attacks was too strong because 40 -> 45 and 50 -> 55 crossed/extended damage tiers. The accepted redesign uses route identity, narrower flat Damage, and secondary effects instead of equalized filler.
- **Blood-Enchanted Eyes:** the original +5 Damage route affects four Shadow Damage rows (40/40/40/50), demonstrating why the nominal +5 ceiling cannot be treated as the default destination. The current working revision keeps paired buff/debuff Foundations and lets sibling routes lean toward different sides of those axes; final revised values remain subject to director lock.
