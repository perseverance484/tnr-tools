# Shadow Weaver — Bloodright kit dossier

**Review id:** BR-063 · **Bloodline id:** `d0WYPbbsVx7Y_i0fddwxc` · **Rank:** A · **Stat classification:** Bukijutsu · **Traits:** Sustained Dps · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 25 | 0.15 | INHERIT | Fire, Lightning, Shadow, None | — | percentage |
| decreasedamagetaken | 15 | 0 | INHERIT | Lightning | — | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Shadow Domain | public | BLOODLINE | A | GROUND | 4 | 60 | 7 | AOE_SPIRAL_SHOOT | — | BOTH | 2 / 3 |
| Shadow Severance | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | SINGLE | — | BOTH | 2 / 3 |
| Shadow Step | public | BLOODLINE | B | EMPTY_GROUND | 5 | 60 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 2 / 3 |
| Shadow Shell | public | BLOODLINE | C | SELF | 0 | 40 | 7 | SINGLE | — | BOTH | 2 / 3 |
| Shadow Dance | public | BLOODLINE | B | OTHER_USER | 4 | 60 | 7 | SINGLE | — | BOTH | 1 / 2 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Recipient | Role | ✓ | Adverse |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|
| Shadow Domain | 0 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | Fire, Lightning, None, Shadow | self | SELF BUFF | ✓ |  |
| Shadow Domain | 1 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Shadow | enemy | DAMAGE | ✓ |  |
| Shadow Domain | 2 | clearprevent | static | 100 | 90 + 0.4/lvl | 1 | None | self | SELF BUFF |  |  |
| Shadow Severance | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Shadow | enemy | DAMAGE | ✓ |  |
| Shadow Severance | 1 | decreasedamagegiven | percentage | 30% | 20 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF | ✓ |  |
| Shadow Severance | 2 | debuffprevent | static | 100 | 90 + 0.4/lvl | 1 | None | self | SELF BUFF |  |  |
| Shadow Step | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Shadow | enemy | DAMAGE | ✓ |  |
| Shadow Step | 1 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | Fire, Lightning, None, Shadow | self | SELF BUFF | ✓ |  |
| Shadow Step | 2 | move | static | 1 | 1 + 0/lvl | 0 | None | self | SELF BUFF |  |  |
| Shadow Shell | 0 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Shadow Shell | 1 | decreasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Shadow Shell | 2 | visual | static | 1 | 1 + 0/lvl | 0 | None | self | SELF DEBUFF |  | **yes** |
| Shadow Dance | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Shadow | enemy | DAMAGE | ✓ |  |
| Shadow Dance | 1 | copy | percentage | 100% | 90 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF |  |  |

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 4 | Shadow Dance, Shadow Domain, Shadow Severance, Shadow Step | DAMAGE | 40 | — | 0 | 0 | 0 | — |
| Increase Damage Given | 3 | Shadow Domain, Shadow Shell, Shadow Step | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Decrease Damage Given | 1 | Shadow Severance | ENEMY DEBUFF | 30 | — | 0 | 0 | 0 | — |
| Decrease Damage Taken | 1 | Shadow Shell | SELF BUFF | 35 | — | 0 | 0 | 0 | — |

Supported rows total: **9**. Unsupported tags present (no potency): clearprevent, copy, debuffprevent, move, visual.

## Selector / classification audit

- Signature elements on damage/pierce rows: Shadow
- Proposed potency classification label: **Shadow** (element)
- Single signature element on the kit's damage/pierce rows; usable as the classification label under the proposed whole-kit classification, provided the classification is bloodline-scoped (see census collisions) rather than a bare element match.
- Current resolver with `affectedElements=['Shadow']`: 6 of 9 supported rows match directly; 3 fall back to None; 0 carry other elements only. Exclusive under current resolver: no.
- Census collisions on signature elements (other bloodlines carrying the element on any row): Adorable Shadow of Death [DEFER] (Shadow: 6 rows, 4 damage); Blood-Enchanted Eyes [INCLUDE] (Shadow: 6 rows, 5 damage); Blood-Enshrined Eyes [EXCLUDE] (Shadow: 3 rows, 3 damage); Blood-Enthralled Eyes [EXCLUDE] (Shadow: 6 rows, 5 damage); Extinction Herald [DEFER] (Shadow: 5 rows, 4 damage); Godstorm Eclipse [INCLUDE] (Shadow: 4 rows, 4 damage); Infernal Reaper [DEFER] (Shadow: 4 rows, 3 damage); Kusamochi: Mashumaro Executioner [DEFER] (Shadow: 3 rows, 3 damage); Lilac Seductress [DEFER] (Shadow: 3 rows, 3 damage); Night Parade of A Thousand Demons [INCLUDE] (Shadow: 2 rows, 2 damage); Oblivion Seal [INCLUDE] (Shadow: 5 rows, 4 damage); Otaku of the Dark Maiden [DEFER] (Shadow: 5 rows, 4 damage); Sacrament of Crimson Hunger [DEFER] (Shadow: 3 rows, 3 damage)
- Normal-jutsu collision: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). Whether NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu carry this element needs a read-only public jutsu listing capture requested from dauntless.
- Item-gated jutsu: none
- Mode-restricted jutsu: none
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

## Afterburn and downstream notes

No Afterburn application rows in this kit.
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

