# Teno Yuki — Bloodright kit dossier

**Review id:** BR-077 · **Bloodline id:** `clh4d6qjs000gtb0hr357gjvv` · **Rank:** A · **Stat classification:** Genjutsu · **Traits:** Control, Defensive · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 25 | 0.15 | INHERIT | Water, Wind, Ice, None | — | percentage |
| decreasedamagetaken | 15 | 0 | INHERIT | Water | — | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Cryostorm Aegis | public | BLOODLINE | A | SELF | 0 | 40 | 7 | SINGLE | — | BOTH | 2 / 2 |
| Imperial Freeze | public | BLOODLINE | B | OTHER_USER | 4 | 60 | 7 | SINGLE | — | BOTH | 1 / 2 |
| Ice Coffin | public | BLOODLINE | B | OTHER_USER | 4 | 60 | 7 | SINGLE | — | BOTH | 2 / 2 |
| Frostbound Ascendancy | public | BLOODLINE | D | EMPTY_GROUND | 4 | 40 | 7 | AOE_SPIRAL_SHOOT | — | BOTH | 1 / 3 |
| Ice Palace | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 2 / 2 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Recipient | Role | ✓ | Adverse |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|
| Cryostorm Aegis | 0 | decreasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Cryostorm Aegis | 1 | heal | static | 25 | 15 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Imperial Freeze | 0 | damage | formula | 45 | 35 + 0.4/lvl | 0 | Ice | enemy | DAMAGE | ✓ |  |
| Imperial Freeze | 1 | stun | static | 100 | 90 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF |  |  |
| Ice Coffin | 0 | decreasedamagegiven | percentage | 30% | 20 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF | ✓ |  |
| Ice Coffin | 1 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Ice | enemy | DAMAGE | ✓ |  |
| Frostbound Ascendancy | 0 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | Ice, None, Water, Wind | self | SELF BUFF | ✓ |  |
| Frostbound Ascendancy | 1 | absorb | percentage | 35% | 25 + 0.4/lvl | 2 | None | self | SELF BUFF |  |  |
| Frostbound Ascendancy | 2 | recoil | percentage | 40% | 30 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF |  |  |
| Ice Palace | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Ice | enemy | DAMAGE | ✓ |  |
| Ice Palace | 1 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | Ice, None, Water, Wind | enemy | ENEMY DEBUFF | ✓ |  |

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 3 | Ice Coffin, Ice Palace, Imperial Freeze | DAMAGE | 40, 45 | — | 0 | 0 | 0 | — |
| Increase Damage Given | 1 | Frostbound Ascendancy | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Decrease Damage Given | 1 | Ice Coffin | ENEMY DEBUFF | 30 | — | 0 | 0 | 0 | — |
| Increase Damage Taken | 1 | Ice Palace | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |
| Decrease Damage Taken | 1 | Cryostorm Aegis | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Heal | 1 | Cryostorm Aegis | SELF BUFF | 25 | — | 0 | 0 | 0 | — |

Supported rows total: **8**. Unsupported tags present (no potency): absorb, recoil, stun.

## Selector / classification audit

- Signature elements on damage/pierce rows: Ice
- Proposed potency classification label: **Ice** (element)
- Single signature element on the kit's damage/pierce rows; usable as the classification label under the proposed whole-kit classification, provided the classification is bloodline-scoped (see census collisions) rather than a bare element match.
- Current resolver with `affectedElements=['Ice']`: 5 of 8 supported rows match directly; 3 fall back to None; 0 carry other elements only. Exclusive under current resolver: no.
- Census collisions on signature elements (other bloodlines carrying the element on any row): Blue Blade Eyes [INCLUDE] (Ice: 8 rows, 5 damage); Blue Edge Eyes [EXCLUDE] (Ice: 8 rows, 5 damage); First Flame [DEFER] (Ice: 8 rows, 5 damage); Hyouga Yui [INCLUDE] (Ice: 4 rows, 3 damage); Itzehecayan [DEFER] (Ice: 4 rows, 3 damage); The Abbynomaly [DEFER] (Ice: 3 rows, 2 damage); True North [DEFER] (Ice: 4 rows, 3 damage)
- Normal-jutsu collision: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). Whether NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu carry this element needs a read-only public jutsu listing capture requested from dauntless.
- Item-gated jutsu: none
- Mode-restricted jutsu: none
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

## Afterburn and downstream notes

No Afterburn application rows in this kit.
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

