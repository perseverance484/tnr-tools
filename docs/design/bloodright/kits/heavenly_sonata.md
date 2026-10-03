# Heavenly Sonata — Bloodright kit dossier

**Review id:** BR-032 · **Bloodline id:** `clh4d6q6s000atb0h0qdqdh1z` · **Rank:** A · **Stat classification:** Genjutsu · **Traits:** Defensive, Tank · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 25 | 0.15 | INHERIT | Fire, Lightning, Yin-Yang, None | — | percentage |
| decreasedamagetaken | 15 | 0 | INHERIT | Fire | — | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Celestial Harmony Shield | public | BLOODLINE | A | SELF | 0 | 40 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 1 / 2 |
| Foreboding Interlude | public | BLOODLINE | B | OTHER_USER | 4 | 60 | 7 | SINGLE | — | BOTH | 2 / 2 |
| Frozen Melody | public | BLOODLINE | B | OTHER_USER | 4 | 60 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 1 / 2 |
| Harmonic Chamber | public | BLOODLINE | A | OTHER_USER | 4 | 40 | 7 | SINGLE | — | BOTH | 1 / 3 |
| Lullaby | public | BLOODLINE | D | OTHER_USER | 4 | 60 | 7 | SINGLE | — | BOTH | 2 / 3 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Recipient | Role | ✓ | Adverse |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|
| Celestial Harmony Shield | 0 | decreasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Celestial Harmony Shield | 1 | shield | static | 100 | 100 + 0/lvl | 2 | None | self | SELF BUFF |  |  |
| Foreboding Interlude | 0 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF | ✓ |  |
| Foreboding Interlude | 1 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Yin-Yang | enemy | DAMAGE | ✓ |  |
| Frozen Melody | 0 | damage | formula | 45 | 35 + 0.4/lvl | 0 | Yin-Yang | enemy | DAMAGE | ✓ |  |
| Frozen Melody | 1 | stun | static | 100 | 90 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF |  |  |
| Harmonic Chamber | 0 | drain | static | 210 | 200 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF |  |  |
| Harmonic Chamber | 1 | decreasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF | ✓ |  |
| Harmonic Chamber | 2 | cleanseprevent | static | 100 | 90 + 0.4/lvl | 1 | None | enemy | ENEMY DEBUFF |  |  |
| Lullaby | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Yin-Yang | enemy | DAMAGE | ✓ |  |
| Lullaby | 1 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Lullaby | 2 | buffprevent | static | 100 | 100 + 0/lvl | 1 | None | enemy | ENEMY DEBUFF |  |  |

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 3 | Foreboding Interlude, Frozen Melody, Lullaby | DAMAGE | 40, 45 | — | 0 | 0 | 0 | — |
| Increase Damage Given | 1 | Lullaby | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Decrease Damage Given | 1 | Harmonic Chamber | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |
| Increase Damage Taken | 1 | Foreboding Interlude | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |
| Decrease Damage Taken | 1 | Celestial Harmony Shield | SELF BUFF | 35 | — | 0 | 0 | 0 | — |

Supported rows total: **7**. Unsupported tags present (no potency): buffprevent, cleanseprevent, drain, shield, stun.

## Selector / classification audit

- Signature elements on damage/pierce rows: Yin-Yang
- Proposed potency classification label: **Yin-Yang** (element)
- Single signature element on the kit's damage/pierce rows; usable as the classification label under the proposed whole-kit classification, provided the classification is bloodline-scoped (see census collisions) rather than a bare element match.
- Current resolver with `affectedElements=['Yin-Yang']`: 3 of 7 supported rows match directly; 4 fall back to None; 0 carry other elements only. Exclusive under current resolver: no.
- Census collisions on signature elements (other bloodlines carrying the element on any row): Celestial Mage [DEFER] (Yin-Yang: 4 rows, 4 damage); DvEM [DEFER] (Yin-Yang: 3 rows, 3 damage); Ethereal Monarch [INCLUDE] (Yin-Yang: 3 rows, 3 damage); Ethereal Regent [EXCLUDE] (Yin-Yang: 4 rows, 4 damage); Manhattan Project [DEFER] (Yin-Yang: 5 rows, 4 damage); Tenohira Musei [INCLUDE] (Yin-Yang: 4 rows, 3 damage); Tenryūseigan [DEFER] (Yin-Yang: 4 rows, 4 damage); Tenshin Shoden Yami-Ryu [DEFER] (Yin-Yang: 4 rows, 4 damage)
- Normal-jutsu collision: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). Whether NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu carry this element needs a read-only public jutsu listing capture requested from dauntless.
- Item-gated jutsu: none
- Mode-restricted jutsu: none
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

## Afterburn and downstream notes

No Afterburn application rows in this kit.
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

