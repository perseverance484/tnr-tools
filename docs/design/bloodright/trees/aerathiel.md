# Aerathiel — Litany of Dust

**Bloodline:** Aerathiel (BR-002, rank A, `1C34syOOEKp6k3UKweYT6`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance (roster pass) / Dust classification / forked tree · **Classification:** Dust (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Atomic Shield: sustained self amplification of every Dust strike in its window, or retaliation (Scouring Veil) · secondary Enemy decay: exposure or suppression from Windshear Decay and Death's March (Entropic Grasp) · tertiary Damage unamplified: no node adds flat Damage (Particle Cannon stays 50, Death's March and Decaying Touch 40).

The tree splits by cast. Scouring Veil answers "How do I turn my Atomic Shield into the weapon: strike harder, or strike back?": Particle Collapse and Total Disintegration lift the Shield's two compounding damage buffs 35 → 43% (sustained amplification, ≈ ×1.122 on each Dust strike in the window), while Atomic Reprisal lifts the Shield's Reflect to 50% (retaliation). Entropic Grasp answers "How do I make the enemy decay: open them to every blow, or too weak to land their own?": Terminal Decay lifts both exposure debuffs to 43% (exposure, ≈ ×1.122 from any attacker), Requiem of Dust lifts Windshear Decay's suppression to 45%. Damage is left unamplified: the trait is sustained damage over time, not burst, and Particle Cannon shares the 60 AP, cooldown-7 profile of the two 40 strikes, so no build lifts it past the Nuke tier. Potency reaches matching supported tags on all Dust jutsu (RUL-2026-10-03-005).

**Review status:** Fable proposal (2026-10-04 batch rebalance, roster pass); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Scouring Veil | Foundation | How do I turn my Atomic Shield into the weapon: strike harder, or strike back? |
| Entropic Grasp | Foundation | How do I make the enemy decay: open them to every blow, or too weak to land their own? |
| Total Disintegration | Advanced Art | sustained amplification: the Shield's two compounding damage buffs on every Dust strike in its window |
| Atomic Reprisal | Advanced Art | retaliation: the Shield returns half of every blow in its window |
| Terminal Decay | Advanced Art | exposure: team-wide pressure on a marked target |
| Requiem of Dust | Advanced Art | suppression: everything in the circle deals less |

**Director review recommended:** Roster questions: DQ-B (Terminal Decay +8% exposure on two compounding rows, 35 → 43%, ≈ ×1.122); DQ-H (self/enemy root axis: Scouring Veil owns the Atomic Shield self cast and Entropic Grasp the enemy debuffs, in place of the anchors' offence/defence roots, so the amplification commit is never Terminal Decay's fourth purchase).

- Concern: Damage is unamplified (R1′): the trait is sustained damage over time and Particle Cannon shares the strikes' 60 AP and cooldown 7, so no dossier fact makes it a signature finisher. If the kit is read as strike-led, the R1′ alternative is a percentage setup on Particle Collapse and a +2 Damage payoff on Total Disintegration, past the Nuke tier on Particle Cannon.
- Concern: Terminal Decay keeps exposure 35 → 43% on two compounding team-wide rows (≈ ×1.122), just above Blood-Enchanted Eyes' ×1.115 exposure maximum and at the proposal's ≈ ×1.12 ceiling.
- Concern: The two offensive capstones match on paper: each is +8% on two compounding rows (≈ ×1.122) and reaches ≈ ×1.156 with its strongest fourth. They separate by delivery: Total Disintegration from one 40 AP self cast on the caster's own Dust strikes, Terminal Decay from two casts (100 AP) on a target every attacker hits, allies included. Uptime was not simulated.
- Concern: Atomic Reprisal and Requiem of Dust are single-tag, lighter than the anchors' defensive riders. The kit has no Decrease Damage Taken, Heal or Lifesteal row; the only rider candidates are the Shield damage buffs and exposure, which would blur them into Total Disintegration and Terminal Decay as Draft 5's riders did.
- Concern: Suppression and half of Exposure depend on Windshear Decay being classified Dust by authored jutsu classification (G1); one of the amplification route's two rows needs the proposed resolver.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Dust jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 06 | Scouring Veil | Foundation | None | +2% Increase Damage Given (self buff); +2% Reflect (self buff) | Atomic Shield / 3 |
| 02 | Particle Collapse | Hidden Art | Scouring Veil | +2% Increase Damage Given (self buff) | Atomic Shield / 2 |
| 03 | Total Disintegration | Advanced Art | Particle Collapse | +4% Increase Damage Given (self buff) | Atomic Shield / 2 |
| 07 | Particulate Ward | Hidden Art | Scouring Veil | +3% Reflect (self buff) | Atomic Shield / 1 |
| 08 | Atomic Reprisal | Advanced Art | Particulate Ward | +5% Reflect (self buff) | Atomic Shield / 1 |
| 01 | Entropic Grasp | Foundation | None | +2% Increase Damage Taken (enemy debuff); +2% Decrease Damage Given (enemy debuff) | Death's March, Windshear Decay / 3 |
| 04 | Hollowing Wind | Hidden Art | Entropic Grasp | +2% Increase Damage Taken (enemy debuff) | Death's March, Windshear Decay / 2 |
| 05 | Terminal Decay | Advanced Art | Hollowing Wind | +4% Increase Damage Taken (enemy debuff) | Death's March, Windshear Decay / 2 |
| 09 | Withering Gale | Hidden Art | Entropic Grasp | +3% Decrease Damage Given (enemy debuff) | Windshear Decay / 1 |
| 10 | Requiem of Dust | Advanced Art | Withering Gale | +5% Decrease Damage Given (enemy debuff) | Windshear Decay / 1 |

Connections: 06→02, 02→03, 06→07, 07→08, 01→04, 04→05, 01→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Scouring Veil** — A veil of grit that drives each blow home and bites back at theirs. All three Atomic Shield rows: both self damage buffs 35 → 37% and Reflect 40 → 42% (one 40 AP self cast, 2 rounds).
- **Particle Collapse** — The shield's gathered dust collapses into every strike. Commit: Atomic Shield's two damage buffs 37 → 39% with Scouring Veil; both apply to each Dust strike in the window and compound (×1.39 × 1.39 ≈ ×1.93 against ×1.82 unmodified).
- **Total Disintegration** — Nothing remains to bury. Sustained amplification: Atomic Shield's two damage buffs 35 → 43% on the full route; each Dust strike in the two rounds after the cast takes ×1.43 × 1.43 ≈ ×2.04 instead of ×1.82 (≈ ×1.122). No flat Damage.
- **Particulate Ward** — Dust thickens into a shell that remembers every strike. Atomic Shield Reflect 42 → 45% with Scouring Veil (one row, 2 rounds per cast).
- **Atomic Reprisal** — What strikes the shield returns to its sender. Retaliation: Atomic Shield Reflect 40 → 50% on the full route, under the 60% per-hit cap.
- **Entropic Grasp** — Every touch loosens the bonds that hold a body together. Windshear Decay exposure and suppression 35 → 37% and Death's March exposure 35 → 37% (enemy debuffs, 2 rounds).
- **Hollowing Wind** — The gale scours away whatever once turned a blade. Commit: Windshear Decay and Death's March Increase Damage Taken 37 → 39% with Entropic Grasp.
- **Terminal Decay** — Once decay begins, it does not stop. Exposure: both exposure debuffs 35 → 43% on the full route; a matching hit from any attacker on a target under both takes ×1.43 × 1.43 ≈ ×2.04 instead of ×1.82 (≈ ×1.122, against Blood-Enchanted Eyes' ×1.115 exposure maximum).
- **Withering Gale** — Arms grow heavy in the dust-laden wind. Windshear Decay Decrease Damage Given 37 → 40% with Entropic Grasp (one AOE row; its redirection row is unsupported).
- **Requiem of Dust** — The march ends where the wind lays everything down. Suppression: Windshear Decay Decrease Damage Given 35 → 45% on the full route; a debuffed enemy's matching hits deal ×0.55 instead of ×0.65.

## Complete four-purchase examples

| Build | Purchases | IDG | DDG | IDT | REF |
|---|---|---:|---:|---:|---:|
| Total Disintegration (Sustained amplification) | Scouring Veil, Particle Collapse, Total Disintegration, Entropic Grasp | +8% | +2% | +2% | +2% |
| Atomic Reprisal (Retaliation) | Scouring Veil, Particulate Ward, Atomic Reprisal, Particle Collapse | +4% | — | — | +10% |
| Terminal Decay (Exposure) | Entropic Grasp, Hollowing Wind, Terminal Decay, Scouring Veil | +2% | +2% | +8% | +2% |
| Requiem of Dust (Suppression) | Entropic Grasp, Withering Gale, Requiem of Dust, Hollowing Wind | — | +10% | +4% | — |

Abbreviations: IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken · REF = Reflect. Values are per-matching-row static additions, not final combat percentages.

- **Total Disintegration:** Both Atomic Shield damage buffs 35 → 43%, so each Dust strike in the two rounds after one 40 AP cast takes ×1.43 × 1.43 ≈ ×2.04 (×1.82 unmodified, ≈ ×1.122); no flat Damage, so Particle Cannon stays 50. Entropic Grasp is the fourth purchase (both exposure debuffs and Windshear suppression 37%; ≈ ×1.156 into a target under both exposure debuffs inside the Shield window); Particulate Ward (Reflect 45%) is the defensive alternative.
- **Atomic Reprisal:** Atomic Shield Reflect 40 → 50% for the two rounds after one 40 AP cast, under the 60% per-hit cap. Particle Collapse is the fourth purchase, lifting the same cast's damage buffs to 39% (the amplification commit without its capstone); Entropic Grasp (exposure and suppression 37%) is the alternative.
- **Terminal Decay:** Windshear Decay and Death's March exposure 35 → 43%: a matching hit from any attacker on a target under both takes ×1.43 × 1.43 ≈ ×2.04 (×1.82 unmodified, ≈ ×1.122), with Windshear suppression 37%. Scouring Veil is the fourth purchase (Shield damage buffs 37%, Reflect 42%); Withering Gale (suppression 40%) is the control alternative.
- **Requiem of Dust:** Windshear Decay Decrease Damage Given 35 → 45% on everyone in its circle (allies there too). Hollowing Wind is the fourth purchase, lifting both exposure debuffs to 39%, so one 40 AP Windshear cast both weakens and opens the target; Scouring Veil is the defensive alternative.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Sustained amplification | Retaliation | Exposure | Suppression |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Windshear Decay | 0 | Increase Damage Taken | enemy | 35% | 37% (+2) | 35% | 43% (+8) | 39% (+4) |
| Windshear Decay | 1 | Decrease Damage Given | enemy | 35% | 37% (+2) | 35% | 37% (+2) | 45% (+10) |
| Windshear Decay | 2 | redirection (unsupported) | enemy | 4 | 4 | 4 | 4 | 4 |
| Death's March | 0 | Damage | enemy | 40 | 40 | 40 | 40 | 40 |
| Death's March | 1 | Increase Damage Taken | enemy | 35% | 37% (+2) | 35% | 43% (+8) | 39% (+4) |
| Atomic Shield | 0 | Increase Damage Given | self | 35% | 43% (+8) | 39% (+4) | 37% (+2) | 35% |
| Atomic Shield | 1 | Reflect | self | 40% | 42% (+2) | 50% (+10) | 42% (+2) | 40% |
| Atomic Shield | 2 | Increase Damage Given | self | 35% | 43% (+8) | 39% (+4) | 37% (+2) | 35% |
| Decaying Touch | 0 | Damage | enemy | 40 | 40 | 40 | 40 | 40 |
| Decaying Touch | 1 | recoil (unsupported) | enemy | 40% | 40% | 40% | 40% | 40% |
| Particle Cannon | 0 | Damage | enemy | 50 | 50 | 50 | 50 | 50 |
| Particle Cannon | 1 | wound (unsupported) | enemy | 25% | 25% | 25% | 25% | 25% |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +8% Increase Damage Given, +10% Decrease Damage Given, +8% Increase Damage Taken, +10% Reflect (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Total Disintegration: +8% Increase Damage Given (2 + 2 + 4; off band)
  - Route Terminal Decay: +8% Increase Damage Taken (2 + 2 + 4; off band)
  - Route Atomic Reprisal: +10% Reflect (2 + 3 + 5; on band)
  - Route Requiem of Dust: +10% Decrease Damage Given (2 + 3 + 5; on band)
- Supported rows in kit: 9 (DMG 3, DDG 1, IDG 2, IDT 2, REF 1)
- Supported tags present but not targeted: damage
- Strongest full build by row-weighted total: Entropic Grasp, Particle Collapse, Total Disintegration, Scouring Veil (raw +14, row-weighted 24)
- Lowest row-weighted node: Particulate Ward (3)

Validator warnings:

- ally-hazard area rows amplified (friendly fire none/ALL): Death's March#1, Windshear Decay#0, Windshear Decay#1
- supported tags present in kit but not targeted by any node: damage

### Damage tiers (base → final)

No node adds flat Damage; every Damage row keeps its base (Death's March 40 (Normal), Decaying Touch 40 (Normal), Particle Cannon 50 (Nuke)).

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Total Disintegration | +8% IDG, +2% REF | Entropic Grasp *(highest diagnostic)* | +8% IDG, +2% DDG, +2% IDT, +2% REF | 24 |
| Total Disintegration | +8% IDG, +2% REF | Particulate Ward | +8% IDG, +5% REF | 21 |
| Terminal Decay | +2% DDG, +8% IDT | Scouring Veil *(highest diagnostic)* | +2% IDG, +2% DDG, +8% IDT, +2% REF | 24 |
| Terminal Decay | +2% DDG, +8% IDT | Withering Gale | +5% DDG, +8% IDT | 21 |
| Atomic Reprisal | +2% IDG, +10% REF | Entropic Grasp *(highest diagnostic)* | +2% IDG, +2% DDG, +2% IDT, +10% REF | 20 |
| Atomic Reprisal | +2% IDG, +10% REF | Particle Collapse | +4% IDG, +10% REF | 18 |
| Requiem of Dust | +10% DDG, +2% IDT | Hollowing Wind | +10% DDG, +4% IDT | 18 |
| Requiem of Dust | +10% DDG, +2% IDT | Scouring Veil *(highest diagnostic)* | +2% IDG, +10% DDG, +2% IDT, +2% REF | 20 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Entropic Grasp, Particle Collapse, Total Disintegration, Scouring Veil | +8% IDG, +2% DDG, +2% IDT, +2% REF |
| 2 | Entropic Grasp, Particle Collapse, Hollowing Wind, Scouring Veil | +4% IDG, +2% DDG, +4% IDT, +2% REF |
| 3 | Entropic Grasp, Particle Collapse, Scouring Veil, Particulate Ward | +4% IDG, +2% DDG, +2% IDT, +5% REF |
| 4 | Entropic Grasp, Particle Collapse, Scouring Veil, Withering Gale | +4% IDG, +5% DDG, +2% IDT, +2% REF |
| 5 | Entropic Grasp, Hollowing Wind, Terminal Decay, Scouring Veil | +2% IDG, +2% DDG, +8% IDT, +2% REF |
| 6 | Entropic Grasp, Hollowing Wind, Terminal Decay, Withering Gale | +5% DDG, +8% IDT |
| 7 | Entropic Grasp, Hollowing Wind, Scouring Veil, Particulate Ward | +2% IDG, +2% DDG, +4% IDT, +5% REF |
| 8 | Entropic Grasp, Hollowing Wind, Scouring Veil, Withering Gale | +2% IDG, +5% DDG, +4% IDT, +2% REF |
| 9 | Entropic Grasp, Hollowing Wind, Withering Gale, Requiem of Dust | +10% DDG, +4% IDT |
| 10 | Entropic Grasp, Scouring Veil, Particulate Ward, Atomic Reprisal | +2% IDG, +2% DDG, +2% IDT, +10% REF |
| 11 | Entropic Grasp, Scouring Veil, Particulate Ward, Withering Gale | +2% IDG, +5% DDG, +2% IDT, +5% REF |
| 12 | Entropic Grasp, Scouring Veil, Withering Gale, Requiem of Dust | +2% IDG, +10% DDG, +2% IDT, +2% REF |
| 13 | Particle Collapse, Total Disintegration, Scouring Veil, Particulate Ward | +8% IDG, +5% REF |
| 14 | Particle Collapse, Scouring Veil, Particulate Ward, Atomic Reprisal | +4% IDG, +10% REF |

## Design notes

- Structure (rewired from Draft 5, edges 06→02→03, 06→07→08, 01→04→05, 01→09→10): Scouring Veil owns the Atomic Shield self cast and forks into Sustained amplification (Particle Collapse → Total Disintegration, Increase Damage Given) and Retaliation (Particulate Ward → Atomic Reprisal, Reflect); Entropic Grasp owns the enemy debuffs on Windshear Decay and Death's March and forks into Exposure (Hollowing Wind → Terminal Decay) and Suppression (Withering Gale → Requiem of Dust). Draft 5 placed both damage multipliers and flat Damage under one Foundation, so either offensive capstone plus its sibling Hidden Art stacked them on the same strike (Terminal Decay plus Particle Collapse: +10% exposure, +5% amplification and +2 Damage). Here amplification and exposure sit under different Foundations, so neither offensive commit is a fourth purchase for the other offensive capstone.
- Damage (final cleanup, R1′): left unamplified. The trait is 'Sustained Damage over time', not Burst, and Particle Cannon is not a signature finisher: it shares 60 AP and cooldown 7 with Death's March and Decaying Touch. Earlier drafts lifted Particle Cannon past the Nuke tier (Draft 5's +5 route, the roster pass's +2 payoff). Total Disintegration now holds the self amplification slot, so every strike keeps its tier (Particle Cannon 50 Nuke, the others 40 Normal). Self amplification does not twin Terminal Decay (enemy exposure from two casts, every attacker), Atomic Reprisal (Reflect) or Requiem of Dust (suppression).
- Magnitudes follow R3. Atomic Shield's two Increase Damage Given rows come from one 40 AP cast and compound on each Dust strike, so the amplification route stops at +8% in 2/2/4 steps (×1.43² / ×1.35² ≈ ×1.122, inside the window only). The two exposure rows sit on separate casts (100 AP together) and compound only while both are up, so Exposure also stops at +8% in 2/2/4 steps (≈ ×1.122 with both, ≈ ×1.06 with one), against the Shakunetsu Sakura ×1.075 and Blood-Enchanted Eyes ×1.115 exposure anchors; its reach includes every attacker. Reflect and Decrease Damage Given each have one row and take the +10% route (suppression ×0.55 / ×0.65 ≈ ×0.846). Maxima over every legal allocation: Increase Damage Given +8%, Increase Damage Taken +8%, Reflect +10%, Decrease Damage Given +10%; no Damage.
- Filters (§3, register G15): Atomic Shield row 0 (Highest stat, no element) matches the caster's highest-offence-stat and element-less hits; row 2 matches Dust/Earth/Wind and element-less hits, so each Dust strike takes both buffs. Windshear Decay rows 0–1 match any stat-based or element-less hit; Death's March row 1 only Dust/Earth/Wind or element-less hits. The passive Increase Damage Given multiplies last.
- Delivery and timing (§3b): every cast has cooldown 7. Atomic Shield and Windshear Decay cost 40 AP; Death's March, Decaying Touch and Particle Cannon 60 AP. Each buff or debuff row is live in the two rounds after its cast round, never in it, so Death's March's exposure never boosts its own hit. No rotation was simulated.
- Fourth purchase: Total Disintegration takes Entropic Grasp (both exposure debuffs 37%: ≈ ×1.122 × 1.030 ≈ ×1.156 on a Dust strike into a doubly exposed target inside the Shield window) or Particulate Ward (Reflect 45%). Atomic Reprisal takes Particle Collapse (Shield damage buffs 39%), so Atomic Reprisal + Particle Collapse and Total Disintegration + Particulate Ward share three nodes and trade +5% Reflect against +4% amplification. Terminal Decay takes Scouring Veil (≈ ×1.122 × 1.030 ≈ ×1.156 inside the Shield window) or Withering Gale (suppression 40%). Requiem of Dust takes Hollowing Wind (exposure 39%) or Scouring Veil. The no-capstone hybrid Entropic Grasp + Hollowing Wind + Scouring Veil + Particle Collapse (amplify and exposure 39%, ≈ ×1.124 with every window live) gives up both 43% values. Top offensive package ≈ ×1.156, under Blood-Enchanted Eyes' ×1.234.

## Risks and unproven interactions

- Classification: Dust is shared with Kyuko-sei and Nejireru Funjin (expected under RUL-2026-10-03-005). Windshear Decay carries no Dust row, so all of Suppression and half of Exposure need an authored Dust jutsu classification (ENGINE_GAP_REGISTER G1); Atomic Shield rows 0–1 (one damage buff and Reflect) need the proposed jutsu-classification resolver, so without it the amplification route reaches only row 2 (+8% on one row, ≈ ×1.06). Off-kit Dust coverage is unverified.
- Ally hazard (validator WARN accepted): Windshear Decay and Death's March are OTHER_USER circle spawns with friendly fire none/ALL, so exposure up to 43% and suppression up to 45% also land on allies in the radius-1 circle; the caster is never a target.
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

