# Suragu — Bloodright kit dossier

**Review id:** BR-074 · **Bloodline id:** `Ksb6ogNqc5mp4l_hRgPuW` · **Rank:** A · **Stat classification:** Highest · **Traits:** Sustained DPS · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 25 | 0.15 | INHERIT | Lava, Earth, Fire, None | — | percentage |
| decreasedamagetaken | 15 | 0 | INHERIT | Fire | — | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Lava Wave | public | BLOODLINE | A | EMPTY_GROUND | 5 | 40 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 2 / 3 |
| Blow of Devastation | public | BLOODLINE | D | OTHER_USER | 4 | 40 | 7 | SINGLE | — | BOTH | 1 / 2 |
| Eruption Strike | public | BLOODLINE | B | OTHER_USER | 4 | 60 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 1 / 2 |
| Magma Slayer | public | BLOODLINE | B | OTHER_USER | 4 | 60 | 7 | SINGLE | — | PVP | 1 / 2 |
| Infernal Stream | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | SINGLE | — | BOTH | 2 / 3 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Recipient | Role | ✓ | Adverse |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|
| Lava Wave | 0 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | Earth, Fire, Lava, None | self | SELF BUFF | ✓ |  |
| Lava Wave | 1 | decreasedamagetaken | percentage | 30% | 20 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Lava Wave | 2 | move | static | 1 | 1 + 0/lvl | — | None | self | SELF BUFF |  |  |
| Blow of Devastation | 0 | recoil | percentage | 40% | 30 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF |  |  |
| Blow of Devastation | 1 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF | ✓ |  |
| Eruption Strike | 0 | pierce | formula | 58 | 48 + 0.4/lvl | 0 | Lava | enemy | ENEMY DEBUFF |  |  |
| Eruption Strike | 1 | afterburn | percentage | 35% | 25 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF | ✓ |  |
| Magma Slayer | 0 | damage | formula | 45 | 35 + 0.4/lvl | 0 | Lava | enemy | DAMAGE | ✓ |  |
| Magma Slayer | 1 | wound | percentage | 30% | 20 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF |  |  |
| Infernal Stream | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Lava | enemy | DAMAGE | ✓ |  |
| Infernal Stream | 1 | lifesteal | percentage | 40% | 30 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Infernal Stream | 2 | poison | percentage | 50% | 40 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF |  |  |

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 2 | Infernal Stream, Magma Slayer | DAMAGE | 40, 45 | — | 0 | 0 | 1 | — |
| Increase Damage Given | 1 | Lava Wave | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Increase Damage Taken | 1 | Blow of Devastation | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |
| Decrease Damage Taken | 1 | Lava Wave | SELF BUFF | 30 | — | 0 | 0 | 0 | — |
| Afterburn | 1 | Eruption Strike | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |
| Lifesteal | 1 | Infernal Stream | SELF BUFF | 40 | — | 0 | 0 | 0 | — |

Supported rows total: **7**. Unsupported tags present (no potency): move, pierce, poison, recoil, wound.

## Selector / classification audit

- Signature elements on damage/pierce rows: Lava
- Proposed potency classification label: **Lava** (element)
- Single signature element on the kit's damage/pierce rows; usable as the classification label under the proposed whole-kit classification, provided the classification is bloodline-scoped (see census collisions) rather than a bare element match.
- Current resolver with `affectedElements=['Lava']`: 3 of 7 supported rows match directly; 4 fall back to None; 0 carry other elements only. Exclusive under current resolver: no.
- Census collisions on signature elements (other bloodlines carrying the element on any row): Amaterasu [DEFER] (Lava: 3 rows, 2 damage)
- Normal-jutsu collision: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). Whether NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu carry this element needs a read-only public jutsu listing capture requested from dauntless.
- Item-gated jutsu: none
- Mode-restricted jutsu: Magma Slayer (PVP)
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

## Afterburn and downstream notes

Application rows: Eruption Strike row 1 (35%, 2 rounds).
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

