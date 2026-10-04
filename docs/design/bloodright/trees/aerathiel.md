# Aerathiel — Litany of Dust

**Bloodline:** Aerathiel (BR-002, rank A, `1C34syOOEKp6k3UKweYT6`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance (roster pass) / Dust classification / forked tree · **Classification:** Dust (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Atomic Shield: self-amplified burst into +2 Damage, or retaliation (Scouring Veil) · secondary Enemy decay: exposure or suppression from Windshear Decay and Death's March (Entropic Grasp) · tertiary Controlled flat Damage: +2 on the burst capstone only (Particle Cannon 50 → 52 on the director precedent).

The tree splits by cast. Scouring Veil answers "How do I turn my Atomic Shield into the weapon: strike harder, or strike back?": Particle Collapse lifts the Shield's two compounding damage buffs to 40% and Total Disintegration pays that setup off with +2 Damage on all three Dust strikes (burst), while Atomic Reprisal lifts the Shield's Reflect to 50% (retaliation). Entropic Grasp answers "How do I make the enemy decay: open them to every blow, or too weak to land their own?": Terminal Decay lifts both exposure debuffs to 43% (exposure), Requiem of Dust lifts Windshear Decay's suppression to 45%. Total Disintegration is the only Damage node, so no build adds more than +2 (Particle Cannon 50 → 52, past the Nuke tier on the Blood-Enchanted Eyes / Shakunetsu Sakura precedent). Potency reaches matching supported tags on all Dust jutsu (RUL-2026-10-03-005).

**Review status:** Fable proposal (2026-10-04 batch rebalance, roster pass); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Scouring Veil | Foundation | How do I turn my Atomic Shield into the weapon: strike harder, or strike back? |
| Entropic Grasp | Foundation | How do I make the enemy decay: open them to every blow, or too weak to land their own? |
| Total Disintegration | Advanced Art | burst: self amplify setup on the Shield, controlled +2 Damage payoff on all three Dust strikes |
| Atomic Reprisal | Advanced Art | retaliation: the Shield returns half of every blow in its window |
| Terminal Decay | Advanced Art | exposure: team-wide pressure on a marked target |
| Requiem of Dust | Advanced Art | suppression: everything in the circle deals less |

**Director review recommended:** Two choices recorded. (1) Particle Cannon 50 → 52 under Total Disintegration: the controlled +2 payoff after Particle Collapse's self amplify setup, restored on the Blood-Enchanted Eyes / Shakunetsu Sakura precedent (RUL-2026-10-04-001/002; see above_nuke_rationale); confirm it for this kit, or keep Damage unamplified and accept a pure +7% Increase Damage Given capstone that is sustained amplification, not burst. (2) Terminal Decay is a primary team-wide exposure route at +8% on two compounding rows (≈ ×1.12), above the anchors' +5% exposure; it should move with the roster's other two-row exposure routes, not alone.

- Concern: Particle Cannon 50 → 52 under Total Disintegration is above the Nuke tier; it rests on the director precedent, not on a ruling for this kit.
- Concern: Terminal Decay keeps exposure at +8% on two compounding team-wide rows, the batch's two-row convention and above the anchors' +5%.
- Concern: Atomic Reprisal and Requiem of Dust are single-tag, lighter than the anchors' defensive riders. The kit has no Decrease Damage Taken, Heal or Lifesteal row; the only rider candidates are the Shield damage buffs and exposure, which would blur them into Burst and Exposure as Draft 5's riders did.
- Concern: Burst + Entropic Grasp (≈ ×1.15 to ×1.16) and Exposure + Scouring Veil (≈ ×1.16) are close inside the windows; Burst leads outside them (+2 Damage), Exposure for allies' hits. Uptime was not simulated.
- Concern: Suppression and half of Exposure depend on Windshear Decay being classified Dust by authored jutsu classification (G1); one of Particle Collapse's two rows needs the proposed resolver.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Dust jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 06 | Scouring Veil | Foundation | None | +2% Increase Damage Given (self buff); +2% Reflect (self buff) | Atomic Shield / 3 |
| 02 | Particle Collapse | Hidden Art | Scouring Veil | +3% Increase Damage Given (self buff) | Atomic Shield / 2 |
| 03 | Total Disintegration | Advanced Art | Particle Collapse | +2 Damage (damage) | Death's March, Decaying Touch, Particle Cannon / 3 |
| 07 | Particulate Ward | Hidden Art | Scouring Veil | +3% Reflect (self buff) | Atomic Shield / 1 |
| 08 | Atomic Reprisal | Advanced Art | Particulate Ward | +5% Reflect (self buff) | Atomic Shield / 1 |
| 01 | Entropic Grasp | Foundation | None | +2% Increase Damage Taken (enemy debuff); +2% Decrease Damage Given (enemy debuff) | Death's March, Windshear Decay / 3 |
| 04 | Hollowing Wind | Hidden Art | Entropic Grasp | +3% Increase Damage Taken (enemy debuff) | Death's March, Windshear Decay / 2 |
| 05 | Terminal Decay | Advanced Art | Hollowing Wind | +3% Increase Damage Taken (enemy debuff) | Death's March, Windshear Decay / 2 |
| 09 | Withering Gale | Hidden Art | Entropic Grasp | +3% Decrease Damage Given (enemy debuff) | Windshear Decay / 1 |
| 10 | Requiem of Dust | Advanced Art | Withering Gale | +5% Decrease Damage Given (enemy debuff) | Windshear Decay / 1 |

Connections: 06→02, 02→03, 06→07, 07→08, 01→04, 04→05, 01→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Scouring Veil** — A veil of grit that drives each blow home and bites back at theirs. All three Atomic Shield rows: both self damage buffs 35 → 37% and Reflect 40 → 42% (one 40 AP self cast, 2 rounds).
- **Particle Collapse** — The shield's gathered dust collapses into every strike. Setup: Atomic Shield's two damage buffs 37 → 40% with Scouring Veil; both apply to each Dust strike in the window and compound (×1.40 × 1.40 ≈ ×1.96 against ×1.82 unmodified).
- **Total Disintegration** — Nothing remains to bury. Burst payoff: +2 Damage on all three Dust strikes, Particle Cannon 50 → 52 (above the 50 Nuke tier; director precedent) and Death's March and Decaying Touch 40 → 42 (still Normal).
- **Particulate Ward** — Dust thickens into a shell that remembers every strike. Atomic Shield Reflect 42 → 45% with Scouring Veil (one row, 2 rounds per cast).
- **Atomic Reprisal** — What strikes the shield returns to its sender. Retaliation: Atomic Shield Reflect 40 → 50% on the full route, under the 60% per-hit cap.
- **Entropic Grasp** — Every touch loosens the bonds that hold a body together. Windshear Decay exposure and suppression 35 → 37% and Death's March exposure 35 → 37% (enemy debuffs, 2 rounds).
- **Hollowing Wind** — The gale scours away whatever once turned a blade. Windshear Decay and Death's March Increase Damage Taken 37 → 40% with Entropic Grasp.
- **Terminal Decay** — Once decay begins, it does not stop. Exposure: both exposure debuffs 35 → 43% on the full route; a matching hit on a target under both takes ×1.43 × 1.43 ≈ ×2.04 instead of ×1.82, from any attacker.
- **Withering Gale** — Arms grow heavy in the dust-laden wind. Windshear Decay Decrease Damage Given 37 → 40% with Entropic Grasp (one AOE row; its redirection row is unsupported).
- **Requiem of Dust** — The march ends where the wind lays everything down. Suppression: Windshear Decay Decrease Damage Given 35 → 45% on the full route; a debuffed enemy's matching hits deal ×0.55 instead of ×0.65.

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | IDT | REF |
|---|---|---:|---:|---:|---:|---:|
| Total Disintegration (Burst) | Scouring Veil, Particle Collapse, Total Disintegration, Entropic Grasp | +2 | +5% | +2% | +2% | +2% |
| Atomic Reprisal (Retaliation) | Scouring Veil, Particulate Ward, Atomic Reprisal, Particle Collapse | — | +5% | — | — | +10% |
| Terminal Decay (Exposure) | Entropic Grasp, Hollowing Wind, Terminal Decay, Scouring Veil | — | +2% | +2% | +8% | +2% |
| Requiem of Dust (Suppression) | Entropic Grasp, Withering Gale, Requiem of Dust, Hollowing Wind | — | — | +10% | +5% | — |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken · REF = Reflect. Values are per-matching-row static additions, not final combat percentages.

- **Total Disintegration:** Both Atomic Shield damage buffs 35 → 40%, so a Dust strike in the two rounds after the cast takes ×1.40 × 1.40 ≈ ×1.96 (×1.82 unmodified), then +2 Damage on every Dust strike, in or out of the window: Particle Cannon 50 → 52 (past the Nuke tier, director precedent), Death's March and Decaying Touch 40 → 42. Entropic Grasp is the fourth purchase (both exposure debuffs and Windshear suppression 37%); Particulate Ward (Reflect 45%) is the defensive alternative.
- **Atomic Reprisal:** Atomic Shield Reflect 40 → 50% for the two rounds after one 40 AP cast, under the 60% per-hit cap. Particle Collapse is the fourth purchase, lifting the same cast's damage buffs to 40% (Burst's setup without its Damage payoff); Entropic Grasp (exposure and suppression 37%) is the alternative.
- **Terminal Decay:** Windshear Decay and Death's March exposure 35 → 43%: a matching hit from any attacker on a target under both takes ×1.43 × 1.43 ≈ ×2.04 (×1.82 unmodified), with Windshear suppression 37%. Scouring Veil is the fourth purchase (Shield damage buffs 37%, Reflect 42%); Withering Gale (suppression 40%) is the control alternative.
- **Requiem of Dust:** Windshear Decay Decrease Damage Given 35 → 45% on everyone in its circle (allies there too). Hollowing Wind is the fourth purchase, lifting both exposure debuffs to 40%, so one 40 AP Windshear cast both weakens and opens the target; Scouring Veil is the defensive alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Retaliation | Exposure | Suppression |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Windshear Decay | 0 | Increase Damage Taken | enemy | 35% | 37% (+2) | 35% | 43% (+8) | 40% (+5) |
| Windshear Decay | 1 | Decrease Damage Given | enemy | 35% | 37% (+2) | 35% | 37% (+2) | 45% (+10) |
| Windshear Decay | 2 | redirection (unsupported) | enemy | 4 | 4 | 4 | 4 | 4 |
| Death's March | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Death's March | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 35% | 43% (+8) | 40% (+5) |
| Atomic Shield | 0 | Increase Damage Given | self | 35% | 40% (+5) | 40% (+5) | 37% (+2) | 35% |
| Atomic Shield | 1 | Reflect | self | 40% | 42% (+2) | 50% (+10) | 42% (+2) | 40% |
| Atomic Shield | 2 | Increase Damage Given | self | 35% | 40% (+5) | 40% (+5) | 37% (+2) | 35% |
| Decaying Touch | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Decaying Touch | 1 | recoil (unsupported) | enemy | 40% | 40% | 40% | 40% | 40% |
| Particle Cannon | 0 | Damage | enemy | 50 | 52 (+2) | 50 | 50 | 50 |
| Particle Cannon | 1 | wound (unsupported) | enemy | 25% | 25% | 25% | 25% | 25% |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +2 Damage, +5% Increase Damage Given, +10% Decrease Damage Given, +8% Increase Damage Taken, +10% Reflect (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Total Disintegration: +2 Damage (0 + 0 + 2; off band)
  - Route Terminal Decay: +8% Increase Damage Taken (2 + 3 + 3; off band)
  - Route Atomic Reprisal: +10% Reflect (2 + 3 + 5; on band)
  - Route Requiem of Dust: +10% Decrease Damage Given (2 + 3 + 5; on band)
- Supported rows in kit: 9 (DMG 3, DDG 1, IDG 2, IDT 2, REF 1)
- Strongest full build by row-weighted total: Entropic Grasp, Particle Collapse, Hollowing Wind, Scouring Veil (raw +14, row-weighted 24)
- Lowest row-weighted node: Particulate Ward (3)

Validator warnings:

- Damage above the 50 Nuke tier in a legal allocation (director review): Particle Cannon 50 -> 52
- ally-hazard area rows amplified (friendly fire none/ALL): Death's March#0, Death's March#1, Windshear Decay#0, Windshear Decay#1

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +2 Damage |
|---|---:|---|---|
| Death's March | 0 | 40 (Normal) | 42 (Normal) |
| Decaying Touch | 0 | 40 (Normal) | 42 (Normal) |
| Particle Cannon | 0 | 50 (Nuke) | **52 (above Nuke)** |

Above-Nuke rationale: Fable proposal following the director precedent of RUL-2026-10-04-001 (Blood-Enchanted Eyes, Reaper's Embrace 50 → 52) and RUL-2026-10-04-002 (Shakunetsu Sakura, Sakura-ame 50 → 52): Total Disintegration's +2 Damage is the controlled payoff of Particle Collapse's self amplify setup on Atomic Shield and lifts Particle Cannon 50 → 52, past the 50 Nuke tier; Death's March and Decaying Touch go 40 → 42 and stay Normal. It is the tree's only Damage node, so no legal allocation adds more than +2 and nothing reaches 55. The pre-batch tree's burst route was +5 Damage (Particle Cannon 50 → 55) on this damage-led kit; the controlled payoff keeps the burst identity at a fraction of that tier impact. Pending director review.

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Total Disintegration | +2 Damage, +5% IDG, +2% REF | Entropic Grasp *(highest diagnostic)* | +2 Damage, +5% IDG, +2% DDG, +2% IDT, +2% REF | 24 |
| Total Disintegration | +2 Damage, +5% IDG, +2% REF | Particulate Ward | +2 Damage, +5% IDG, +5% REF | 21 |
| Terminal Decay | +2% DDG, +8% IDT | Scouring Veil *(highest diagnostic)* | +2% IDG, +2% DDG, +8% IDT, +2% REF | 24 |
| Terminal Decay | +2% DDG, +8% IDT | Withering Gale | +5% DDG, +8% IDT | 21 |
| Atomic Reprisal | +2% IDG, +10% REF | Entropic Grasp *(highest diagnostic)* | +2% IDG, +2% DDG, +2% IDT, +10% REF | 20 |
| Atomic Reprisal | +2% IDG, +10% REF | Particle Collapse | +5% IDG, +10% REF | 20 |
| Requiem of Dust | +10% DDG, +2% IDT | Hollowing Wind | +10% DDG, +5% IDT | 20 |
| Requiem of Dust | +10% DDG, +2% IDT | Scouring Veil *(highest diagnostic)* | +2% IDG, +10% DDG, +2% IDT, +2% REF | 20 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Entropic Grasp, Particle Collapse, Total Disintegration, Scouring Veil | +2 Damage, +5% IDG, +2% DDG, +2% IDT, +2% REF |
| 2 | Entropic Grasp, Particle Collapse, Hollowing Wind, Scouring Veil | +5% IDG, +2% DDG, +5% IDT, +2% REF |
| 3 | Entropic Grasp, Particle Collapse, Scouring Veil, Particulate Ward | +5% IDG, +2% DDG, +2% IDT, +5% REF |
| 4 | Entropic Grasp, Particle Collapse, Scouring Veil, Withering Gale | +5% IDG, +5% DDG, +2% IDT, +2% REF |
| 5 | Entropic Grasp, Hollowing Wind, Terminal Decay, Scouring Veil | +2% IDG, +2% DDG, +8% IDT, +2% REF |
| 6 | Entropic Grasp, Hollowing Wind, Terminal Decay, Withering Gale | +5% DDG, +8% IDT |
| 7 | Entropic Grasp, Hollowing Wind, Scouring Veil, Particulate Ward | +2% IDG, +2% DDG, +5% IDT, +5% REF |
| 8 | Entropic Grasp, Hollowing Wind, Scouring Veil, Withering Gale | +2% IDG, +5% DDG, +5% IDT, +2% REF |
| 9 | Entropic Grasp, Hollowing Wind, Withering Gale, Requiem of Dust | +10% DDG, +5% IDT |
| 10 | Entropic Grasp, Scouring Veil, Particulate Ward, Atomic Reprisal | +2% IDG, +2% DDG, +2% IDT, +10% REF |
| 11 | Entropic Grasp, Scouring Veil, Particulate Ward, Withering Gale | +2% IDG, +5% DDG, +2% IDT, +5% REF |
| 12 | Entropic Grasp, Scouring Veil, Withering Gale, Requiem of Dust | +2% IDG, +10% DDG, +2% IDT, +2% REF |
| 13 | Particle Collapse, Total Disintegration, Scouring Veil, Particulate Ward | +2 Damage, +5% IDG, +5% REF |
| 14 | Particle Collapse, Scouring Veil, Particulate Ward, Atomic Reprisal | +5% IDG, +10% REF |

## Design notes

- Structure (rewired from Draft 5, edges 06→02→03, 06→07→08, 01→04→05, 01→09→10): Scouring Veil owns the Atomic Shield self cast and forks into Burst (Particle Collapse's Increase Damage Given setup → Total Disintegration's +2 Damage) and Retaliation (Particulate Ward → Atomic Reprisal, Reflect); Entropic Grasp owns the enemy debuffs on Windshear Decay and Death's March and forks into Exposure (Hollowing Wind → Terminal Decay) and Suppression (Withering Gale → Requiem of Dust). Draft 5 placed both damage multipliers and flat Damage under one Foundation, so either offensive capstone plus its sibling Hidden Art stacked them on the same strike (Terminal Decay plus Particle Collapse: +10% exposure, +5% amplification and +2 Damage). Here Damage needs Scouring Veil and Particle Collapse, so it is never a fourth purchase for Terminal Decay.
- Damage (roster pass): Total Disintegration is the only Damage node, +2 on all three Dust strikes (Particle Cannon 50 → 52, Death's March and Decaying Touch 40 → 42). Draft 5's +5 route gave 50 → 55 and 40 → 45; the first batch pass removed Damage and left a pure +7% Increase Damage Given capstone labelled burst. The director pattern replaces both: percentage setup on the Hidden Art, controlled +2 payoff on the Advanced Art (RUL-2026-10-04-001/002; above_nuke_rationale). The setup is self amplification, not exposure, because Hollowing Wind already owns the exposure rows.
- Magnitudes follow leverage, not printed totals. Atomic Shield's two Increase Damage Given rows come from one 40 AP cast and compound on each Dust strike, so the Burst setup stops at +5% (×1.40² / ×1.35² ≈ ×1.075); with the +2 Damage the full route is ≈ ×1.12 on a Particle Cannon and ≈ ×1.13 on a 40 strike inside the Shield window, ×1.04 / ×1.05 outside it. The two exposure rows sit on separate casts (100 AP together) and compound only while both are up, so Exposure stops at +8% (≈ ×1.12 with both, ≈ ×1.06 with one), and its reach includes every attacker. Reflect and Decrease Damage Given each have one row and take the +10% route. Maxima over every legal allocation: Damage +2, Increase Damage Given +5%, Increase Damage Taken +8%, Reflect +10%, Decrease Damage Given +10%.
- Filters (§3, register G15): Atomic Shield row 0 (Highest stat, no element) matches the caster's highest-offence-stat and element-less hits; row 2 matches Dust/Earth/Wind and element-less hits, so each Dust strike takes both buffs. Windshear Decay rows 0–1 match any stat-based or element-less hit; Death's March row 1 only Dust/Earth/Wind or element-less hits. The passive Increase Damage Given multiplies last.
- Delivery and timing (§3b): every cast has cooldown 7. Atomic Shield and Windshear Decay cost 40 AP; Death's March, Decaying Touch and Particle Cannon 60 AP. Each buff or debuff row is live in the two rounds after its cast round, never in it, so Death's March's exposure never boosts its own hit; the +2 Damage is on the strike itself and needs no window. No rotation was simulated.
- Fourth purchase: Burst takes Entropic Grasp (both exposure debuffs 37%: ≈ ×1.15 on a Particle Cannon and ≈ ×1.16 on a 40 strike into a doubly exposed target inside the Shield window) or Particulate Ward (Reflect 45%). Retaliation takes Particle Collapse (Shield damage buffs 40%), so Retaliation + Particle Collapse and Burst + Particulate Ward hold the same Shield buffs and trade +5% Reflect against +2 Damage. Exposure takes Scouring Veil (≈ ×1.122 × 1.030 ≈ ×1.16 on a Dust strike into a doubly exposed target inside the Shield window) or Withering Gale (suppression 40%). Suppression takes Hollowing Wind (exposure 40%) or Scouring Veil. The no-capstone hybrid Entropic Grasp + Particle Collapse + Hollowing Wind + Scouring Veil (amplify and exposure 40%, ≈ ×1.16 with every window live) gives up the Damage and the 43% exposure.

## Risks and unproven interactions

- Classification: Dust is shared with Kyuko-sei and Nejireru Funjin (expected under RUL-2026-10-03-005). Windshear Decay carries no Dust row, so all of Suppression and half of Exposure need an authored Dust jutsu classification (ENGINE_GAP_REGISTER G1); Atomic Shield rows 0–1 (one damage buff and Reflect) need the proposed jutsu-classification resolver, so without it Particle Collapse reaches only row 2. The +2 Damage reaches three natively Dust rows. Off-kit Dust coverage is unverified.
- Ally hazard (validator WARN accepted): Windshear Decay and Death's March are OTHER_USER circle spawns with friendly fire none/ALL, so exposure up to 43%, suppression up to 45% and Death's March's 42 Damage also land on allies in the radius-1 circle; the caster is never a target.
- Exposure is team-wide: an enhanced exposure row raises every matching hit the target takes, allies' and weapons' included, so Terminal Decay's value grows with party size.
- Reflect value is downstream: it depends on hits taken in the two-round window, includes pierce hits (which bypass the row's stat filter) and is capped at 60% of each pre-shield hit; 50% stays under the cap. Not simulated.
- Unsupported rows (Windshear Decay redirection, Decaying Touch recoil, Particle Cannon wound) are unchanged; the trait 'sustained damage over time' has no supported damage-over-time row.
- Skill-tree effects are skipped in RANKED_PVP and RANKED_SPARRING. No combat simulation was performed.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Dust jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

