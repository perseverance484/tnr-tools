# Heavenly Sonata — Music of the Spheres

**Bloodline:** Heavenly Sonata (BR-032, rank A, `clh4d6q6s000atb0h0qdqdh1z`) · **Revision:** Fable proposal — 2026-10-04 batch rebalance (roster pass) / Yin-Yang classification / forked tree · **Classification:** Yin-Yang (element) · **Engine status:** proposal_requires_jutsu_classification_resolver

**Emphasis:** primary Defense from Harmonic Balance: Celestial Harmony Shield fortress (Decrease Damage Taken) or Harmonic Chamber suppression (Decrease Damage Given) · secondary Offense from Opening Measure: Lullaby's self buff into a controlled +2 Damage burst, or Foreboding Interlude exposure on every attacker's Genjutsu and element-less hits · tertiary Paired +2% Foundation glue on each side's two rows.

Heavenly Sonata is a Defensive/Tank Genjutsu kit with one supported row on each of four percentage tags and three Yin-Yang Damage rows (Foreboding Interlude 40, Frozen Melody 45, Lullaby 40 EP at jutsu level 25). Harmonic Balance answers "How do I win defensively: shelter myself or silence them?": Celestial Sanctum takes the Shield's self reduction 35 → 45%, Final Rest takes Harmonic Chamber's suppression 35 → 45%. Opening Measure answers "How do I win offensively: amplify my own song or expose the target?": Rising Crescendo lifts Lullaby's self buff and Fortissimo Finale pays off with +2 Damage (40 → 42, 45 → 47, no tier crossing), while Prelude to Ruin takes Interlude's exposure 35 → 45% on every attacker's Genjutsu and element-less hits. The earlier +5 Damage route (40 → 45 twice, Frozen Melody 45 → 50) is retired. No Afterburn, Lifesteal, Reflect or Heal row exists, so none is invented. Potency reaches matching supported tags on all Yin-Yang jutsu (RUL-2026-10-03-005).

**Review status:** Fable proposal (2026-10-04 batch rebalance, roster pass); not director-approved

| Node | Tier | Foundation sentence / route identity |
|---|---|---|
| Opening Measure | Foundation | How do I win offensively: amplify my own song or expose the target? |
| Harmonic Balance | Foundation | How do I win defensively: shelter myself or silence them? |
| Fortissimo Finale | Advanced Art | burst: self-amplification setup on Lullaby, controlled +2 Damage payoff on all three Yin-Yang strikes |
| Prelude to Ruin | Advanced Art | exposure: team-wide mark on one target |
| Celestial Sanctum | Advanced Art | fortress: self damage reduction on the Shield |
| Final Rest | Advanced Art | suppression: the Chamber's target deals less to everyone |

**Director review recommended:** Roster questions: DQ-B (Prelude to Ruin +10% Increase Damage Taken on one row, Foreboding Interlude 35 → 45%, ×1.074: the same as Shakunetsu Sakura's two-row +5% at ×1.075, below Blood-Enchanted Eyes' ×1.115).

- Concern: Prelude to Ruin is the tree's highest-leverage route in group play. Solo it only matches Burst (Interlude → Lullaby → Frozen Melody at 3 BP: ≈ 187 against ≈ 190 EP-equivalent). A trim to +8% (Dissonant Chord +2%, Prelude to Ruin +4%: Interlude 43%, ≈ ×1.059) would leave it a +4% top-up over Burst + Dissonant Chord (39%), which also carries the +2 Damage; at ≈ ×1.074 it is level with Shakunetsu Sakura's ×1.075, so the magnitude stays with the director (DQ-B).
- Concern: The two all-offense 4-BP builds (Burst plus Dissonant Chord, Exposure plus Rising Crescendo) both stack Lullaby's 40% buff with Interlude's exposure; they differ by +2 Damage against +5% more exposure (≈ 193 against ≈ 189 EP-equivalent on the solo rotation).
- Concern: Fortress and Suppression with their sibling Hidden Art mirror each other (45/42% and 42/45%), as Blood-Enchanted Eyes' defensive half does with +3% riders; Arashima's Fortress uses a Lifesteal rider instead, which this kit lacks.
- Concern: Until the jutsu-level resolver (G1) exists, only Fortissimo Finale's +2 Damage reaches a row; the Burst/Exposure parity and both tank routes assume it.

All nodes cost 1 BP; the budget is 4 BP acquired with silver; each skill is bought once; forks only. Bonuses apply to matching supported tags on all Yin-Yang jutsu. Bonuses are static additions under the proposed element-wide classification; no row's combat scope, recipient or filters change. Bloodline id, equipment, injected-child provenance and jutsu names are not selectors. Baselines at jutsu level 25.

## Skills

| ID | Skill | Tier | Requires | Exact bonus and recipient | Kit coverage (example jutsu / rows) |
|---|---|---|---|---|---|
| 01 | Opening Measure | Foundation | None | +2% Increase Damage Given (self buff); +2% Increase Damage Taken (enemy debuff) | Foreboding Interlude, Lullaby / 2 |
| 02 | Rising Crescendo | Hidden Art | Opening Measure | +3% Increase Damage Given (self buff) | Lullaby / 1 |
| 03 | Fortissimo Finale | Advanced Art | Rising Crescendo | +2 Damage (damage) | Foreboding Interlude, Frozen Melody, Lullaby / 3 |
| 04 | Dissonant Chord | Hidden Art | Opening Measure | +3% Increase Damage Taken (enemy debuff) | Foreboding Interlude / 1 |
| 05 | Prelude to Ruin | Advanced Art | Dissonant Chord | +5% Increase Damage Taken (enemy debuff) | Foreboding Interlude / 1 |
| 06 | Harmonic Balance | Foundation | None | +2% Decrease Damage Taken (self buff); +2% Decrease Damage Given (enemy debuff) | Celestial Harmony Shield, Harmonic Chamber / 2 |
| 07 | Wall of Sound | Hidden Art | Harmonic Balance | +3% Decrease Damage Taken (self buff) | Celestial Harmony Shield / 1 |
| 08 | Celestial Sanctum | Advanced Art | Wall of Sound | +5% Decrease Damage Taken (self buff); +2% Decrease Damage Given (enemy debuff) | Celestial Harmony Shield, Harmonic Chamber / 2 |
| 09 | Muted Strings | Hidden Art | Harmonic Balance | +3% Decrease Damage Given (enemy debuff) | Harmonic Chamber / 1 |
| 10 | Final Rest | Advanced Art | Muted Strings | +5% Decrease Damage Given (enemy debuff); +2% Decrease Damage Taken (self buff) | Celestial Harmony Shield, Harmonic Chamber / 2 |

Connections: 01→02, 02→03, 01→04, 04→05, 06→07, 07→08, 06→09, 09→10. Advanced Arts: 4; any two cost at least 5 BP including prerequisites (cap 4); maximum affordable Advanced Arts: 1.

- **Opening Measure** — Every sonata begins with a single measure that decides how the rest will fall. Lullaby self buff 35 → 37% (every non-pierce hit you land) and Foreboding Interlude exposure 35 → 37% (Genjutsu or element-less hits on the target); 2 rounds after each cast.
- **Rising Crescendo** — The melody swells, and every note that follows lands heavier. Lullaby self buff 37 → 40% with Opening Measure: every non-pierce hit you land in the 2 rounds after the 60 AP cast, never Lullaby's own hit.
- **Fortissimo Finale** — The last movement, played at full voice, brings the heavens down. Burst: Foreboding Interlude and Lullaby 40 → 42, Frozen Melody 45 → 47 EP; every row stays in its tier. Inside the Lullaby window (40% on this route) each hit is ×1.40.
- **Dissonant Chord** — One wrong note, held too long, and the whole piece turns against its listener. Foreboding Interlude exposure 37 → 40% with Opening Measure; live 2 rounds after each 60 AP cast; Genjutsu or element-less non-pierce hits.
- **Prelude to Ruin** — The interlude was only a warning; this is the ruin it foretold. Exposure: Foreboding Interlude 35 → 45% on the full route, ×1.45 / ×1.35 ≈ ×1.074 over the unmodified row; for 2 rounds every attacker's Genjutsu or element-less non-pierce hit on the target is ×1.45, allies' included.
- **Harmonic Balance** — Yin answers yang: every note has its silence, every blow its shelter. Celestial Harmony Shield self reduction 35 → 37%; Harmonic Chamber suppression 35 → 37% (every non-pierce hit the target deals); 2 rounds after each 40 AP cast.
- **Wall of Sound** — Layer upon layer of chorus, until no blade can find the singer. Shield self reduction 37 → 40% with Harmonic Balance: realized on the caster at cast, live 2 rounds after, any position; non-pierce.
- **Celestial Sanctum** — Within the shield's hymn the caster stands untouched, as in a chapel of light. Fortress: Shield self reduction 35 → 45% on the full route (×0.55 instead of ×0.65 on every non-pierce hit you take); Harmonic Chamber suppression 39% (42% with Muted Strings).
- **Muted Strings** — The chamber swallows the enemy's song until only a murmur escapes. Harmonic Chamber suppression 37 → 40% with Harmonic Balance; 40 AP single target, range 4; every non-pierce hit the target deals.
- **Final Rest** — The last rest in the score: no note, no breath, no strength left to strike. Suppression: Harmonic Chamber 35 → 45% on the full route (the target's non-pierce hits ×0.55, against anyone); Shield self reduction 39% (42% with Wall of Sound).

## Complete four-purchase examples

| Build | Purchases | DMG | IDG | DDG | IDT | DDT |
|---|---|---:|---:|---:|---:|---:|
| Fortissimo Finale (Burst) | Opening Measure, Rising Crescendo, Fortissimo Finale, Dissonant Chord | +2 | +5% | — | +5% | — |
| Prelude to Ruin (Exposure) | Opening Measure, Dissonant Chord, Prelude to Ruin, Harmonic Balance | — | +2% | +2% | +10% | +2% |
| Celestial Sanctum (Fortress) | Harmonic Balance, Wall of Sound, Celestial Sanctum, Muted Strings | — | — | +7% | — | +10% |
| Final Rest (Suppression) | Opening Measure, Harmonic Balance, Muted Strings, Final Rest | — | +2% | +10% | +2% | +4% |

Abbreviations: DMG = Damage · IDG = Increase Damage Given · DDG = Decrease Damage Given · IDT = Increase Damage Taken · DDT = Decrease Damage Taken. Values are per-matching-row static additions, not final combat percentages.

- **Fortissimo Finale:** Sing Lullaby first: its self buff (40% with Opening Measure and Rising Crescendo) multiplies every non-pierce hit you land in the next two rounds, and Fortissimo Finale's +2 Damage lifts Foreboding Interlude and Lullaby 40 → 42 and Frozen Melody 45 → 47 EP without crossing a tier. Dissonant Chord is the all-offense fourth (Interlude exposure 40%): Frozen Melody inside both windows takes ×1.40 × 1.40 ≈ ×1.96 on 47 EP, against ×1.35 × 1.35 ≈ ×1.82 on 45 EP at base. Harmonic Balance (01, 02, 03, 06) is the sturdier fourth: 37% Shield reduction and Chamber suppression.
- **Prelude to Ruin:** Foreboding Interlude's exposure reaches 45% (+10%): for the two rounds after the cast, every attacker's Genjutsu or element-less non-pierce hit on the target is ×1.45, allies' included. Opening Measure keeps Lullaby's self buff at 37%, and Harmonic Balance is the fourth for 37% Shield reduction and Chamber suppression. Rising Crescendo (01, 02, 04, 05) is the all-offense fourth: Lullaby 40%, so Frozen Melody inside both windows takes ×1.40 × 1.45 ≈ ×2.03 on 45 EP, level with the Burst build's ×1.96 on 47 EP but without the raw Damage.
- **Celestial Sanctum:** The pure tank: Celestial Harmony Shield's self reduction reaches 45% (+10%; ×0.55 instead of ×0.65 on every non-pierce hit you take) in the two rounds after the cast, wherever you stand, and Muted Strings takes Harmonic Chamber's suppression to 42% (+7%) so the locked target hits everyone softer. No offense; Opening Measure (01, 06, 07, 08) is the alternative fourth that keeps 37% buff and exposure at 39% suppression.
- **Final Rest:** Harmonic Chamber's suppression reaches 45% (+10%) on a 40 AP cast that also drains 210 and blocks cleansing: for the two rounds after the cast every non-pierce hit the target deals, against anyone, is ×0.55 instead of ×0.65. The capstone's +2% gives 39% Shield reduction, and Opening Measure is the fourth for 37% buff and exposure. Wall of Sound (06, 07, 09, 10) is the turtle fourth: 42% reduction, 45% suppression, no offense.

## Before/after effect rows

| Jutsu | Row | Tag | Recipient | Base | Burst | Exposure | Fortress | Suppression |
|---|---:|---|---|---:|---:|---:|---:|---:|
| Celestial Harmony Shield | 0 | Decrease Damage Taken | self | 35% | 35% | 37% (+2) | 45% (+10) | 39% (+4) |
| Celestial Harmony Shield | 1 | shield (unsupported) | self | 100 | 100 | 100 | 100 | 100 |
| Foreboding Interlude | 0 | Increase Damage Taken | enemy | 35% | 40% (+5) | 45% (+10) | 35% | 37% (+2) |
| Foreboding Interlude | 1 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Frozen Melody | 0 | Damage | enemy | 45 | 47 (+2) | 45 | 45 | 45 |
| Frozen Melody | 1 | stun (unsupported) | enemy | 100 | 100 | 100 | 100 | 100 |
| Harmonic Chamber | 0 | drain (unsupported) | enemy | 210 | 210 | 210 | 210 | 210 |
| Harmonic Chamber | 1 | Decrease Damage Given | enemy | 35% | 35% | 37% (+2) | 42% (+7) | 45% (+10) |
| Harmonic Chamber | 2 | cleanseprevent (unsupported) | enemy | 100 | 100 | 100 | 100 | 100 |
| Lullaby | 0 | Damage | enemy | 40 | 42 (+2) | 40 | 40 | 40 |
| Lullaby | 1 | Increase Damage Given | self | 35% | 40% (+5) | 37% (+2) | 35% | 37% (+2) |
| Lullaby | 2 | buffprevent (unsupported) | enemy | 100 | 100 | 100 | 100 | 100 |

## Allocation audit

- Legal prerequisite-closed allocations by size: 0: 1, 1: 2, 2: 5, 3: 10, 4: 14
- Full-budget allocations: 14; numerically non-dominated (per-tag totals): 14; all nodes appear in a non-dominated build: True
- Maximum individually achievable additions over every legal allocation: +2 Damage, +5% Increase Damage Given, +10% Decrease Damage Given, +10% Increase Damage Taken, +10% Decrease Damage Taken (not jointly attainable)
- Ceilings (RUL-2026-10-03-005): Damage +5, Lifesteal +5%, Afterburn +15% hard; other tags +10% unless a director-review exception is recorded.
  - Route Fortissimo Finale: +2 Damage (0 + 0 + 2; off band)
  - Route Prelude to Ruin: +10% Increase Damage Taken (2 + 3 + 5; on band)
  - Route Celestial Sanctum: +10% Decrease Damage Taken (2 + 3 + 5; on band)
  - Route Final Rest: +10% Decrease Damage Given (2 + 3 + 5; on band)
- Supported rows in kit: 7 (DMG 3, DDG 1, DDT 1, IDG 1, IDT 1)
- Strongest full build by row-weighted total: Opening Measure, Harmonic Balance, Wall of Sound, Celestial Sanctum (raw +18, row-weighted 18)
- Lowest row-weighted node: Rising Crescendo (3)

### Damage tiers (base → final)

Player-jutsu tiers: 38 Light, 40 Normal, 45 High, 50 Nuke; anything above 50 is past the ladder. Each column is a flat Damage total some legal allocation reaches.

| Jutsu | Row | Base (tier) | +2 Damage |
|---|---:|---|---|
| Foreboding Interlude | 1 | 40 (Normal) | 42 (Normal) |
| Frozen Melody | 0 | 45 (High) | 47 (High) |
| Lullaby | 0 | 40 (Normal) | 42 (Normal) |

### Fourth-BP audit

Each Advanced Art's three-purchase path and every legal fourth purchase. *Highest diagnostic* marks the fourth with the largest row-weighted total; it points at what to review, not at the right answer.

| Advanced Art | Path package | Fourth purchase | Full package | Row-weighted |
|---|---|---|---|---:|
| Fortissimo Finale | +2 Damage, +5% IDG, +2% IDT | Dissonant Chord | +2 Damage, +5% IDG, +5% IDT | 16 |
| Fortissimo Finale | +2 Damage, +5% IDG, +2% IDT | Harmonic Balance *(highest diagnostic)* | +2 Damage, +5% IDG, +2% DDG, +2% IDT, +2% DDT | 17 |
| Prelude to Ruin | +2% IDG, +10% IDT | Rising Crescendo | +5% IDG, +10% IDT | 15 |
| Prelude to Ruin | +2% IDG, +10% IDT | Harmonic Balance *(highest diagnostic)* | +2% IDG, +2% DDG, +10% IDT, +2% DDT | 16 |
| Celestial Sanctum | +4% DDG, +10% DDT | Opening Measure *(highest diagnostic)* | +2% IDG, +4% DDG, +2% IDT, +10% DDT | 18 |
| Celestial Sanctum | +4% DDG, +10% DDT | Muted Strings | +7% DDG, +10% DDT | 17 |
| Final Rest | +10% DDG, +4% DDT | Opening Measure *(highest diagnostic)* | +2% IDG, +10% DDG, +2% IDT, +4% DDT | 18 |
| Final Rest | +10% DDG, +4% DDT | Wall of Sound | +10% DDG, +7% DDT | 17 |

### All legal full-budget allocations

| # | Nodes | Bonuses |
|---:|---|---|
| 1 | Opening Measure, Rising Crescendo, Fortissimo Finale, Dissonant Chord | +2 Damage, +5% IDG, +5% IDT |
| 2 | Opening Measure, Rising Crescendo, Fortissimo Finale, Harmonic Balance | +2 Damage, +5% IDG, +2% DDG, +2% IDT, +2% DDT |
| 3 | Opening Measure, Rising Crescendo, Dissonant Chord, Prelude to Ruin | +5% IDG, +10% IDT |
| 4 | Opening Measure, Rising Crescendo, Dissonant Chord, Harmonic Balance | +5% IDG, +2% DDG, +5% IDT, +2% DDT |
| 5 | Opening Measure, Rising Crescendo, Harmonic Balance, Wall of Sound | +5% IDG, +2% DDG, +2% IDT, +5% DDT |
| 6 | Opening Measure, Rising Crescendo, Harmonic Balance, Muted Strings | +5% IDG, +5% DDG, +2% IDT, +2% DDT |
| 7 | Opening Measure, Dissonant Chord, Prelude to Ruin, Harmonic Balance | +2% IDG, +2% DDG, +10% IDT, +2% DDT |
| 8 | Opening Measure, Dissonant Chord, Harmonic Balance, Wall of Sound | +2% IDG, +2% DDG, +5% IDT, +5% DDT |
| 9 | Opening Measure, Dissonant Chord, Harmonic Balance, Muted Strings | +2% IDG, +5% DDG, +5% IDT, +2% DDT |
| 10 | Opening Measure, Harmonic Balance, Wall of Sound, Celestial Sanctum | +2% IDG, +4% DDG, +2% IDT, +10% DDT |
| 11 | Opening Measure, Harmonic Balance, Wall of Sound, Muted Strings | +2% IDG, +5% DDG, +2% IDT, +5% DDT |
| 12 | Opening Measure, Harmonic Balance, Muted Strings, Final Rest | +2% IDG, +10% DDG, +2% IDT, +4% DDT |
| 13 | Harmonic Balance, Wall of Sound, Celestial Sanctum, Muted Strings | +7% DDG, +10% DDT |
| 14 | Harmonic Balance, Wall of Sound, Muted Strings, Final Rest | +10% DDG, +7% DDT |

## Design notes

- Structure kept (edges 01→02→03, 01→04→05, 06→07→08, 06→09→10). Opening Measure: "How do I win offensively: amplify my own song or expose the target?" (Burst amplifies the caster through Lullaby's self buff into raw Damage; Exposure marks the target for every attacker). Harmonic Balance: "How do I win defensively: shelter myself or silence them?" (Fortress on the Shield, Suppression on the Chamber).
- 2026-10-04 rebalance: the +5 Damage route (Rising Crescendo +2, Fortissimo Finale +3) lifted Foreboding Interlude and Lullaby 40 → 45 (Normal → High) and Frozen Melody 45 → 50 (High → Nuke). Rising Crescendo is now +3% Increase Damage Given (setup on Lullaby's self buff) and Fortissimo Finale +2 Damage (payoff: 40 → 42, 45 → 47, no tier crossing). Prelude to Ruin drops its +3% Increase Damage Given rider: with Rising Crescendo on that tag, Prelude plus Rising Crescendo would stack +8% Increase Damage Given on top of +10% exposure. The defensive half is unchanged. Maxima over every legal allocation: Damage +2, Increase Damage Given +5%, Increase Damage Taken +10%, Decrease Damage Taken +10%, Decrease Damage Given +10%. Roster pass: values unchanged. The kit has no 50 EP row, and the burst route already follows the buff-led pattern of Arashima's Sundered Sky (RUL-2026-10-04-003): a percentage setup on the Hidden Art and +2 Damage on the Advanced Art (45 → 47 at most).
- Magnitudes follow multipliers, not bands. At 3 BP, Frozen Melody inside both offensive windows takes ×1.40 × 1.37 ≈ ×1.92 on 47 EP on the Burst route and ×1.37 × 1.45 ≈ ×1.99 on 45 EP on the Exposure route; over the solo Interlude → Lullaby → Melody rotation that is ≈ 190 against ≈ 187 EP-equivalent, so the choice is solo strike versus team mark. Exposure keeps +10% on its one row (35 → 45%, ≈ ×1.074, level with Shakunetsu Sakura's two-row +5% at ×1.075 and below Blood-Enchanted Eyes' ×1.115), but its team reach is not narrowed by its filter: the row has no element, so its Genjutsu filter does not bind; it raises Genjutsu hits of any element and element-less hits of every stat type, from every attacker on the one target, excluding only elemental Ninjutsu, Taijutsu and Bukijutsu hits. That leverage is left to the director (design_review). Fortress and Suppression each take +10% on one row with a +2% rider of the other tank tag. Suppression matches Arashima's Silence After Thunder (+5% Decrease Damage Given / +2% Decrease Damage Taken); the cross-tag mirror follows Blood-Enchanted Eyes, whose riders are +3%; Arashima's Fortress carries a Lifesteal rider instead, which this kit cannot offer. A reduction row moves ×0.65 → ×0.55.
- Fourth purchases: Burst adds Dissonant Chord (exposure 40%) or Harmonic Balance; Exposure adds Rising Crescendo (Lullaby 40%) or Harmonic Balance; Fortress adds Muted Strings (suppression 42%) or Opening Measure; Suppression adds Wall of Sound (reduction 42%) or Opening Measure. No fourth adds to its own capstone's primary tag. All 14 full-budget allocations are numerically non-dominated.
- Downstream reach: the bloodline passive (Increase Damage Given 25% + 0.15/level on Fire, Lightning, Yin-Yang, None) is not a potency target and applies last, after the kit rows multiply the hit in turn (computeDamagePacket, §3b), so the +2 Damage is multiplied by every window and the passive. Lullaby's buff, the Shield's reduction and Harmonic Chamber's suppression list all four stat types and no element: every non-pierce hit. Interlude's exposure lists only Genjutsu: Genjutsu hits of any element and element-less hits, not elemental Nin/Tai/Buki.
- Delivery and timing: all five jutsu are cooldown 7; Interlude, Melody and Lullaby cost 60 AP, Shield and Chamber 40 AP. Every buff/debuff row is live the two rounds after its cast round, never in it (§3b), so Interlude's exposure never raises its own hit nor Lullaby's buff its own; Interlude, then Lullaby, then Frozen Melody puts the exposure on both later hits and the buff on Melody. The Shield's SELF row is realized on the caster at cast (§4b), not via the circle tiles.

## Risks and unproven interactions

- Classification: element-wide Yin-Yang scope (RUL-2026-10-03-005): matching supported tags on all Yin-Yang jutsu, whatever their source; sharing Yin-Yang with other bloodlines is expected. Today's row-element resolver reaches only the three Yin-Yang Damage rows, so under the current engine only Fortissimo Finale's +2 Damage is live. All four percentage rows (Lullaby Increase Damage Given, Foreboding Interlude Increase Damage Taken, Celestial Harmony Shield Decrease Damage Taken, Harmonic Chamber Decrease Damage Given) are element-less and need the jutsu-level resolver (ENGINE_GAP_REGISTER G1); Lullaby and Interlude qualify by their own Yin-Yang Damage rows, while the Shield and the Chamber (no Yin-Yang row) also need an authored jutsu classification. Off-kit Yin-Yang coverage is unverified.
- Shield timing: the Decrease Damage Taken row has target SELF, so it is realized on the caster at cast, not via the circle tiles (actions.ts 980-1004; SOURCE_MECHANICS 4b): no standing-still cost, no enemy hazard. Like every modifier it skips its cast round and covers the two rounds after, so it must be cast a round ahead of the hits it should absorb.
- Tank-row breadth: 45% suppression (40 AP) lowers the target's damage against allies too for the two rounds after the cast, beside drain 210 and cleanseprevent. Same-tag effects all apply and compound (process.ts 1109-1117): two casters' Chambers on one target give ×0.55 × 0.55 ≈ ×0.30. Not simulated.
- Offense stacking: the all-offense builds put Lullaby's 40% self buff and Interlude's 40-45% exposure on the same hit (×1.96 to ×2.03), on top of other jutsu, main-tree or gear percentages; the bloodline passive applies last. Interlude's exposure also multiplies allies' Genjutsu and element-less hits on the target.
- Realized value: three 60 AP attacks on cooldown 7 mean each 2-round window reaches at most the other two attacks per rotation, never its own jutsu's hit, so per-row numbers overstate per-round value. Lullaby's self buff needs another living user in range 4; aimed at an ally, its damage (friendly fire ALL) and buffprevent land on that ally (§3b).
- Frozen Melody is an AOE_CIRCLE_SPAWN with friendly fire ENEMIES (no ally hazard) and the kit's only multi-target reach; Fortissimo Finale lifts it 45 → 47, below the 50 Nuke tier. Skill-tree effects are skipped in RANKED_PVP and RANKED_SPARRING at the pin. No combat simulation was performed.

## Limits

- Proposed element-wide potency classification; not implemented or verified in the live engine (needs a jutsu-classification resolver).
- Bonuses apply to matching supported tags on all Yin-Yang jutsu. Off-kit jutsu of the element are in scope by rule; their count is unverified. Original combat elements, recipients and stat/general/element filters stay intact.
- Bloodline id, equipment, injected-child provenance and jutsu names are not selectors; equipment only gates castability.
- Coverage counts below are this kit's rows only. Every matching row on a jutsu receives each matching modifier; repeated rows are counted separately.
- Damage values are raw power (EP), not final-damage percentages; every other modifier is shown with %. Percentage-valued tags are capped at 100.
- Afterburn is an enemy debuff: for its existing duration, damage the target takes causes extra Afterburn damage at its percentage (60% cap per hit). It is not itself a damage instance; downstream instances were not simulated.
- Unsupported tags (e.g. wound, shield, stun, pierce, absorb, poison, drain, summon) receive no bonuses.
- No combat simulation. Budget and numerical non-dominance checks do not establish equal combat strength.
- Main-tree effects, bloodline passives, equipment, AP, uptime and modifier delivery are outside this audit.

