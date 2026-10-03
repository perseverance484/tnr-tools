# Shinseina Ki — Bloodright kit dossier

**Review id:** BR-066 · **Bloodline id:** `vA8I_7iBNgvkuKOpnG1yD` · **Rank:** A · **Stat classification:** Highest · **Traits:** Burst · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 25 | 0.15 | INHERIT | Water, Earth, Wood, None | — | percentage |
| decreasedamagetaken | 15 | 0 | INHERIT | Water | — | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Exploding Wood Serpent | public | BLOODLINE | B | OTHER_USER | 4 | 60 | 7 | SINGLE | — | BOTH | 1 / 2 |
| Guardian's Grove | public | BLOODLINE | B | OTHER_USER | 4 | 60 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 2 / 3 |
| Forest Wisdom | public | BLOODLINE | D | SELF | 0 | 40 | 7 | SINGLE | — | BOTH | 2 / 3 |
| Wood Style: Wood Warrior Summon | public | BLOODLINE | A | EMPTY_GROUND | 4 | 60 | 7 | SINGLE | — | PVP | 0 / 2 |
| Eternal Forest | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | SINGLE | — | BOTH | 1 / 2 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Recipient | Role | ✓ | Adverse |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|
| Exploding Wood Serpent | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Wood | enemy | DAMAGE | ✓ |  |
| Exploding Wood Serpent | 1 | recoil | percentage | 40% | 30 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF |  |  |
| Guardian's Grove | 0 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF | ✓ |  |
| Guardian's Grove | 1 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Wood | enemy | DAMAGE | ✓ |  |
| Guardian's Grove | 2 | poison | percentage | 50% | 40 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF |  |  |
| Forest Wisdom | 0 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Forest Wisdom | 1 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | Earth, None, Water, Wood | self | SELF BUFF | ✓ |  |
| Forest Wisdom | 2 | visual | static | 1 | 1 + 0/lvl | 0 | None | self | SELF DEBUFF |  | **yes** |
| Wood Style: Wood Warrior Summon | 0 | summon | percentage | 70% | 60 + 0.4/lvl | 3 | None | enemy | ENEMY BUFF |  | **yes** |
| Wood Style: Wood Warrior Summon | 1 | visual | static | 1 | 1 + 0/lvl | 0 | None | self | SELF DEBUFF |  | **yes** |
| Eternal Forest | 0 | damage | formula | 50 | 40 + 0.4/lvl | 0 | Wood | enemy | DAMAGE | ✓ |  |
| Eternal Forest | 1 | wound | percentage | 25% | 15 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF |  |  |

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 3 | Eternal Forest, Exploding Wood Serpent, Guardian's Grove | DAMAGE | 40, 50 | — | 0 | 0 | 0 | — |
| Increase Damage Given | 2 | Forest Wisdom | SELF BUFF | 35 | Forest Wisdom | 0 | 0 | 0 | — |
| Increase Damage Taken | 1 | Guardian's Grove | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |

Supported rows total: **6**. Unsupported tags present (no potency): poison, recoil, summon, visual, wound.

## Selector / classification audit

- Signature elements on damage/pierce rows: Wood
- Proposed potency classification label: **Wood** (element)
- Single signature element on the kit's damage/pierce rows; usable as the classification label under the proposed whole-kit classification, provided the classification is bloodline-scoped (see census collisions) rather than a bare element match.
- Current resolver with `affectedElements=['Wood']`: 4 of 6 supported rows match directly; 2 fall back to None; 0 carry other elements only. Exclusive under current resolver: no.
- Census collisions on signature elements (other bloodlines carrying the element on any row): Nature's Blessing [INCLUDE] (Wood: 2 rows, 2 damage)
- Normal-jutsu collision: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). Whether NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu carry this element needs a read-only public jutsu listing capture requested from dauntless.
- Item-gated jutsu: none
- Mode-restricted jutsu: Wood Style: Wood Warrior Summon (PVP)
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

## Afterburn and downstream notes

No Afterburn application rows in this kit.
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

