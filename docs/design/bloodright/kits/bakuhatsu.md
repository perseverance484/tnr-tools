# Bakuhatsu — Bloodright kit dossier

**Review id:** BR-008 · **Bloodline id:** `RNUcHSH2c00IhOLc2C9aJ` · **Rank:** A · **Stat classification:** Highest · **Traits:** AoE Control  · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 25 | 0.15 | INHERIT | Lightning, Earth, Explosion, None | — | percentage |
| decreasedamagetaken | 15 | 0 | INHERIT | Earth | — | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Inferno Cataclysm | public | BLOODLINE | A | GROUND | 4 | 60 | 7 | AOE_SPIRAL_SHOOT | — | BOTH | 1 / 2 |
| Kinetic Nova | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 1 / 2 |
| Blast Shield | public | BLOODLINE | D | EMPTY_GROUND | 1 | 40 | 7 | AOE_CIRCLE_SHOOT | — | BOTH | 1 / 2 |
| Charge 4 Explosion | public | BLOODLINE | C | OTHER_USER | 4 | 40 | 7 | SINGLE | — | BOTH | 3 / 3 |
| Howitzer Crash | public | BLOODLINE | B | EMPTY_GROUND | 5 | 60 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 2 / 3 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Recipient | Role | ✓ | Adverse |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|
| Inferno Cataclysm | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Explosion | enemy | DAMAGE | ✓ |  |
| Inferno Cataclysm | 1 | recoil | percentage | 40% | 30 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF |  |  |
| Kinetic Nova | 0 | damage | formula | 50 | 40 + 0.4/lvl | 0 | Explosion | enemy | DAMAGE | ✓ |  |
| Kinetic Nova | 1 | wound | percentage | 25% | 15 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF |  |  |
| Blast Shield | 0 | decreasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Blast Shield | 1 | barrier | static | 100 | 100 + 0/lvl | 2 | None | self | SELF BUFF |  |  |
| Charge 4 Explosion | 0 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Charge 4 Explosion | 1 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | Earth, Explosion, Lightning, None | enemy | ENEMY DEBUFF | ✓ |  |
| Charge 4 Explosion | 2 | afterburn | percentage | 35% | 25 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF | ✓ |  |
| Howitzer Crash | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Explosion | enemy | DAMAGE | ✓ |  |
| Howitzer Crash | 1 | move | static | 1 | 1 + 0/lvl | 0 | None | self | SELF BUFF |  |  |
| Howitzer Crash | 2 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 3 | Howitzer Crash, Inferno Cataclysm, Kinetic Nova | DAMAGE | 40, 50 | — | 0 | 0 | 0 | — |
| Increase Damage Given | 2 | Charge 4 Explosion, Howitzer Crash | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Increase Damage Taken | 1 | Charge 4 Explosion | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |
| Decrease Damage Taken | 1 | Blast Shield | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Afterburn | 1 | Charge 4 Explosion | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |

Supported rows total: **8**. Unsupported tags present (no potency): barrier, move, recoil, wound.

## Selector / classification audit

- Signature elements on damage/pierce rows: Explosion
- Proposed potency classification label: **Explosion** (element)
- Single signature element on the kit's damage/pierce rows; usable as the classification label under the proposed whole-kit classification, provided the classification is bloodline-scoped (see census collisions) rather than a bare element match.
- Current resolver with `affectedElements=['Explosion']`: 4 of 8 supported rows match directly; 4 fall back to None; 0 carry other elements only. Exclusive under current resolver: no.
- Census collisions on signature elements (other bloodlines carrying the element on any row): Bakuhatsu Suru Nendo [DEFER] (Explosion: 4 rows, 4 damage)
- Normal-jutsu collision: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). Whether NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu carry this element needs a read-only public jutsu listing capture requested from dauntless.
- Item-gated jutsu: none
- Mode-restricted jutsu: none
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

## Afterburn and downstream notes

Application rows: Charge 4 Explosion row 2 (35%, 2 rounds).
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

