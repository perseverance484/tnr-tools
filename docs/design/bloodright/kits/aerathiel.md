# Aerathiel — Bloodright kit dossier

**Review id:** BR-002 · **Bloodline id:** `1C34syOOEKp6k3UKweYT6` · **Rank:** A · **Stat classification:** Highest · **Traits:** Sustained Damage over time. · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 25 | 0.15 | INHERIT | Wind, Earth, Dust, None | — | percentage |
| decreasedamagetaken | 15 | 0 | INHERIT | Wind | — | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Windshear Decay | public | BLOODLINE | A | OTHER_USER | 5 | 40 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 2 / 3 |
| Death's March | public | BLOODLINE | B | OTHER_USER | 4 | 60 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 2 / 2 |
| Atomic Shield | public | BLOODLINE | D | SELF | 0 | 40 | 7 | SINGLE | — | BOTH | 3 / 3 |
| Decaying Touch | public | BLOODLINE | B | OTHER_USER | 4 | 60 | 7 | SINGLE | — | BOTH | 1 / 2 |
| Particle Cannon | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | SINGLE | — | BOTH | 1 / 2 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Stat / general filter | Friendly fire | Recipient | Role | ✓ | Adverse | Ally hazard |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|---|---|---|
| Windshear Decay | 0 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  | **yes** |
| Windshear Decay | 1 | decreasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  | **yes** |
| Windshear Decay | 2 | redirection | static | 4 | 4 + 0/lvl | 0 | None | — | none (=ALL) | enemy | ENEMY DEBUFF |  |  | **yes** |
| Death's March | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Dust | Highest / Highest | ALL | enemy | DAMAGE | ✓ |  | **yes** |
| Death's March | 1 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | Dust, Earth, None, Wind | — | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  | **yes** |
| Atomic Shield | 0 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | Highest | none (=ALL) | self | SELF BUFF | ✓ |  |  |
| Atomic Shield | 1 | reflect | percentage | 40% | 30 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | self | SELF BUFF | ✓ |  |  |
| Atomic Shield | 2 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | Dust, Earth, None, Wind | — | none (=ALL) | self | SELF BUFF | ✓ |  |  |
| Decaying Touch | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Dust | Highest / Highest | none (=ALL) | enemy | DAMAGE | ✓ |  |  |
| Decaying Touch | 1 | recoil | percentage | 40% | 30 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF |  |  |  |
| Particle Cannon | 0 | damage | formula | 50 | 40 + 0.4/lvl | 0 | Dust | Highest / Highest | none (=ALL) | enemy | DAMAGE | ✓ |  |  |
| Particle Cannon | 1 | wound | percentage | 25% | 15 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF |  |  |  |

Stat/general filters on an element-less row are not binding at the pin: `getEfficiencyRatio` pushes `None` for an empty element list on both sides, so such a row matches every element-less damage effect of any stat type (basic attacks, non-elemental jutsu) and excludes only elemental damage of a non-listed stat type (SOURCE_MECHANICS.md §3). `Ally hazard` marks harmful rows delivered by an area method or ground target with friendly fire none/ALL: allies and the caster inside the area also receive them (checkFriendlyFire treats an absent value as ALL).

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 3 | Death's March, Decaying Touch, Particle Cannon | DAMAGE | 40, 50 | — | 0 | 0 | 0 | — |
| Increase Damage Given | 2 | Atomic Shield | SELF BUFF | 35 | Atomic Shield | 0 | 0 | 0 | — |
| Decrease Damage Given | 1 | Windshear Decay | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |
| Increase Damage Taken | 2 | Death's March, Windshear Decay | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |
| Reflect | 1 | Atomic Shield | SELF BUFF | 40 | — | 0 | 0 | 0 | — |

Supported rows total: **9**. Unsupported tags present (no potency): recoil, redirection, wound.

> **Ally-hazard rows (area delivery, friendly fire none/ALL):** Windshear Decay row 0 (increasedamagetaken, AOE_CIRCLE_SPAWN, target OTHER_USER); Windshear Decay row 1 (decreasedamagegiven, AOE_CIRCLE_SPAWN, target OTHER_USER); Death's March row 0 (damage, AOE_CIRCLE_SPAWN, target OTHER_USER); Death's March row 1 (increasedamagetaken, AOE_CIRCLE_SPAWN, target OTHER_USER). Potency on these tags also raises what allies standing in the area receive; positioning, not the node, decides.

## Selector / classification audit

- Signature elements on damage/pierce rows: Dust
- Proposed potency classification label: **Dust** (element)
- Single signature element on the kit's damage/pierce rows; usable as the classification label under the proposed whole-kit classification, provided the classification is bloodline-scoped (see census collisions) rather than a bare element match.
- Current resolver with `affectedElements=['Dust']`: 5 of 9 supported rows match directly; 4 fall back to None; 0 carry other elements only. Exclusive under current resolver: no.
- Census collisions on signature elements (other bloodlines carrying the element on any row): Kyuko-sei [INCLUDE] (Dust: 5 rows, 4 damage); Nejireru Funjin [DEFER] (Dust: 3 rows, 3 damage)
- Normal-jutsu collision: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). Whether NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu carry this element needs a read-only public jutsu listing capture requested from dauntless.
- Item-gated jutsu: none
- Mode-restricted jutsu: none
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

## Afterburn and downstream notes

No Afterburn application rows in this kit.
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

