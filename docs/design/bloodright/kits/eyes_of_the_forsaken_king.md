# Eyes of the Forsaken King — Bloodright kit dossier

**Review id:** BR-027 · **Bloodline id:** `r3nBY_Th4_ZAIUfhx1jdy` · **Rank:** S · **Stat classification:** Highest · **Traits:** Burst · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 25 | 0.15 | SELF | Fire, Lightning, Wind, Light, None | Highest | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Shattered Reflection | public | BLOODLINE | B | OTHER_USER | 4 | 60 | 7 | SINGLE | — | BOTH | 1 / 2 |
| Lux | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | AOE_LINE_SHOOT | — | BOTH | 2 / 2 |
| illuminance | public | BLOODLINE | C | EMPTY_GROUND | 5 | 40 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 2 / 3 |
| Chrono Stasis | public | BLOODLINE | A | OTHER_USER | 5 | 40 | 7 | SINGLE | — | BOTH | 2 / 3 |
| Imperial Swords | public | BLOODLINE | D | OTHER_USER | 4 | 60 | 7 | SINGLE | — | BOTH | 3 / 3 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Stat / general filter | Friendly fire | Recipient | Role | ✓ | Adverse | Ally hazard |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|---|---|---|
| Shattered Reflection | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Light | Highest / Highest | ALL | enemy | DAMAGE | ✓ |  |  |
| Shattered Reflection | 1 | mirror | percentage | 100% | 90 + 0.4/lvl | 2 | None | — | ALL | enemy | ENEMY DEBUFF |  |  |  |
| Lux | 0 | damage | formula | 50 | 40 + 0.4/lvl | 0 | Light | Highest / Highest | none (=ALL) | enemy | DAMAGE | ✓ |  | **yes** |
| Lux | 1 | reflect | percentage | 40% | 30 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ALL | self | SELF BUFF | ✓ |  |  |
| illuminance | 0 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | Fire, Light, Lightning, None, Wind | — | none (=ALL) | self | SELF BUFF | ✓ |  |  |
| illuminance | 1 | decreasedamagetaken | percentage | 30% | 20 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | self | SELF BUFF | ✓ |  |  |
| illuminance | 2 | move | static | 1 | 1 + 0/lvl | — | None | — | none (=ALL) | self | SELF BUFF |  |  |  |
| Chrono Stasis | 0 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  |  |
| Chrono Stasis | 1 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | Fire, Light, Lightning, None, Wind | — | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  |  |
| Chrono Stasis | 2 | timedilation | percentage | 100% | 90 + 0.4/lvl | 1 | Fire, Light, Lightning, None, Wind | — | none (=ALL) | self | SELF BUFF |  |  |  |
| Imperial Swords | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Light | Highest / Highest | ENEMIES | enemy | DAMAGE | ✓ |  |  |
| Imperial Swords | 1 | afterburn | percentage | 25% | 15 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  |  |
| Imperial Swords | 2 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  |  |

Stat/general filters on an element-less row are not binding at the pin: `getEfficiencyRatio` pushes `None` for an empty element list on both sides, so such a row matches every element-less damage effect of any stat type (basic attacks, non-elemental jutsu) and excludes only elemental damage of a non-listed stat type (SOURCE_MECHANICS.md §3). `Ally hazard` marks harmful rows delivered by an area method or ground target with friendly fire none/ALL: allies and the caster inside the area also receive them (checkFriendlyFire treats an absent value as ALL).

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 3 | Imperial Swords, Lux, Shattered Reflection | DAMAGE | 40, 50 | — | 0 | 0 | 0 | — |
| Increase Damage Given | 1 | illuminance | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Increase Damage Taken | 3 | Chrono Stasis, Imperial Swords | ENEMY DEBUFF | 35 | Chrono Stasis | 0 | 0 | 0 | — |
| Decrease Damage Taken | 1 | illuminance | SELF BUFF | 30 | — | 0 | 0 | 0 | — |
| Afterburn | 1 | Imperial Swords | ENEMY DEBUFF | 25 | — | 0 | 0 | 0 | — |
| Reflect | 1 | Lux | SELF BUFF | 40 | — | 0 | 0 | 0 | — |

Supported rows total: **10**. Unsupported tags present (no potency): mirror, move, timedilation.

> **Ally-hazard rows (area delivery, friendly fire none/ALL):** Lux row 0 (damage, AOE_LINE_SHOOT, target OTHER_USER). Potency on these tags also raises what allies standing in the area receive; positioning, not the node, decides.

## Selector / classification audit

- Signature elements on damage/pierce rows: Light
- Proposed potency classification label: **Light** (element)
- Single signature element on the kit's damage/pierce rows; usable as the classification label under the proposed whole-kit classification, provided the classification is bloodline-scoped (see census collisions) rather than a bare element match.
- Current resolver with `affectedElements=['Light']`: 5 of 10 supported rows match directly; 5 fall back to None; 0 carry other elements only. Exclusive under current resolver: no.
- Census collisions on signature elements (other bloodlines carrying the element on any row): Architect of the Hollow Script [DEFER] (Light: 5 rows, 3 damage); Crust Almighty [DEFER] (Light: 4 rows, 2 damage); Eyes of the Forsaken Heir [EXCLUDE] (Light: 6 rows, 3 damage); Radiant Valor [DEFER] (Light: 5 rows, 4 damage); Solar Soul [DEFER] (Light: 6 rows, 3 damage); Timeforged Enigma [DEFER] (Light: 6 rows, 3 damage)
- Normal-jutsu collision: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). Whether NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu carry this element needs a read-only public jutsu listing capture requested from dauntless.
- Item-gated jutsu: none
- Mode-restricted jutsu: none
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

## Afterburn and downstream notes

Application rows: Imperial Swords row 1 (25%, 2 rounds).
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

