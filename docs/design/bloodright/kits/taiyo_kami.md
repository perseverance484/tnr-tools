# Taiyo Kami — Bloodright kit dossier

**Review id:** BR-075 · **Bloodline id:** `6C2t3jK35hvPoVocLiHEl` · **Rank:** A · **Stat classification:** Highest · **Traits:** Burst · **Disposition:** REFERENCE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 25 | 0.15 | INHERIT | Fire, Wind, Scorch, None | — | percentage |
| decreasedamagetaken | 15 | 0 | INHERIT | Fire | — | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Solar Reverb | public | BLOODLINE | A | GROUND | 4 | 60 | 7 | AOE_SPIRAL_SHOOT | — | BOTH | 2 / 2 |
| Incandescent Nova | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | SINGLE | — | BOTH | 1 / 2 |
| Celestial Ignition | public | BLOODLINE | B | SELF | 0 | 40 | 7 | SINGLE | — | BOTH | 3 / 3 |
| Radiant Embers | public | BLOODLINE | C | OTHER_USER | 4 | 40 | 7 | SINGLE | — | BOTH | 1 / 2 |
| Stellar Inferno | public | BLOODLINE | D | OTHER_USER | 4 | 60 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 2 / 2 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Stat / general filter | Friendly fire | Recipient | Role | ✓ | Adverse | Ally hazard |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|---|---|---|
| Solar Reverb | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Scorch | Highest / Highest | none (=ALL) | enemy | DAMAGE | ✓ |  | **yes** |
| Solar Reverb | 1 | afterburn | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ENEMIES | enemy | ENEMY DEBUFF | ✓ |  |  |
| Incandescent Nova | 0 | damage | formula | 50 | 40 + 0.4/lvl | 0 | Scorch | Highest / Highest | ALL | enemy | DAMAGE | ✓ |  |  |
| Incandescent Nova | 1 | wound | percentage | 25% | 15 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF |  |  |  |
| Celestial Ignition | 0 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ALL | self | SELF BUFF | ✓ |  |  |
| Celestial Ignition | 1 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | Fire, None, Scorch, Wind | — | none (=ALL) | self | SELF BUFF | ✓ |  |  |
| Celestial Ignition | 2 | decreasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | self | SELF BUFF | ✓ |  |  |
| Radiant Embers | 0 | decreasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  |  |
| Radiant Embers | 1 | shield | static | 100 | 90 + 0.4/lvl | 2 | None | — | none (=ALL) | self | SELF BUFF |  |  |  |
| Stellar Inferno | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Scorch | Highest / Highest | ENEMIES | enemy | DAMAGE | ✓ |  |  |
| Stellar Inferno | 1 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  | **yes** |

Stat/general filters on an element-less row are not binding at the pin: `getEfficiencyRatio` pushes `None` for an empty element list on both sides, so such a row matches every element-less damage effect of any stat type (basic attacks, non-elemental jutsu) and excludes only elemental damage of a non-listed stat type (SOURCE_MECHANICS.md §3). `Ally hazard` marks harmful rows delivered by an area method or ground target with friendly fire none/ALL: allies and the caster inside the area also receive them (checkFriendlyFire treats an absent value as ALL).

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 3 | Incandescent Nova, Solar Reverb, Stellar Inferno | DAMAGE | 40, 50 | — | 0 | 0 | 0 | — |
| Increase Damage Given | 2 | Celestial Ignition | SELF BUFF | 35 | Celestial Ignition | 0 | 0 | 0 | — |
| Decrease Damage Given | 1 | Radiant Embers | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |
| Increase Damage Taken | 1 | Stellar Inferno | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |
| Decrease Damage Taken | 1 | Celestial Ignition | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Afterburn | 1 | Solar Reverb | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |

Supported rows total: **9**. Unsupported tags present (no potency): shield, wound.

> **Ally-hazard rows (area delivery, friendly fire none/ALL):** Solar Reverb row 0 (damage, AOE_SPIRAL_SHOOT, target GROUND); Stellar Inferno row 1 (increasedamagetaken, AOE_CIRCLE_SPAWN, target OTHER_USER). Potency on these tags also raises what allies standing in the area receive; positioning, not the node, decides.

## Selector / classification audit

- Signature elements on damage/pierce rows: Scorch
- Proposed potency classification label: **Scorch** (element)
- Single signature element on the kit's damage/pierce rows; usable as the classification label under the proposed whole-kit classification, provided the classification is bloodline-scoped (see census collisions) rather than a bare element match.
- Current resolver with `affectedElements=['Scorch']`: 4 of 9 supported rows match directly; 5 fall back to None; 0 carry other elements only. Exclusive under current resolver: no.
- Census collisions on signature elements (other bloodlines carrying the element on any row): Shakunetsu Sakura [INCLUDE] (Scorch: 4 rows, 3 damage)
- Normal-jutsu collision: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). Whether NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu carry this element needs a read-only public jutsu listing capture requested from dauntless.
- Item-gated jutsu: none
- Mode-restricted jutsu: none
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

## Afterburn and downstream notes

Application rows: Solar Reverb row 1 (35%, 2 rounds).
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

