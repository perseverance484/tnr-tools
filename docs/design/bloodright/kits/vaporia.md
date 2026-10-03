# Vaporia — Bloodright kit dossier

**Review id:** BR-090 · **Bloodline id:** `f7IgtcsLqomqmmBgAYS1O` · **Rank:** A · **Stat classification:** Taijutsu · **Traits:** High movement, Rush, Consistent Damage · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 25 | 0.15 | INHERIT | Fire, Water, Boil, None | — | percentage |
| decreasedamagetaken | 15 | 0 | INHERIT | Water | — | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Liquid Ember Shell | public | BLOODLINE | B | OTHER_USER | 4 | 40 | 7 | SINGLE | — | BOTH | 3 / 3 |
| Drowning Strike | public | BLOODLINE | D | GROUND | 4 | 60 | 7 | AOE_SPIRAL_SHOOT | — | BOTH | 2 / 2 |
| Surfing Strike | public | BLOODLINE | A | EMPTY_GROUND | 5 | 60 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 2 / 3 |
| Scorch Break | public | BLOODLINE | B | OTHER_USER | 4 | 60 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 2 / 2 |
| Azure Dragon Palm | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | SINGLE | — | BOTH | 1 / 2 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Recipient | Role | ✓ | Adverse |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|
| Liquid Ember Shell | 0 | lifesteal | percentage | 40% | 30 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Liquid Ember Shell | 1 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Liquid Ember Shell | 2 | afterburn | percentage | 35% | 25 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF | ✓ |  |
| Drowning Strike | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Boil | enemy | DAMAGE | ✓ |  |
| Drowning Strike | 1 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF | ✓ |  |
| Surfing Strike | 0 | damage | formula | 45 | 35 + 0.4/lvl | 0 | Boil | enemy | DAMAGE | ✓ |  |
| Surfing Strike | 1 | decreasedamagetaken | percentage | 30% | 20 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Surfing Strike | 2 | move | static | 1 | 1 + 0/lvl | 0 | None | self | SELF BUFF |  |  |
| Scorch Break | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Boil | enemy | DAMAGE | ✓ |  |
| Scorch Break | 1 | reflect | percentage | 40% | 30 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Azure Dragon Palm | 0 | pierce | formula | 58 | 48 + 0.4/lvl | 0 | Boil | enemy | ENEMY DEBUFF |  |  |
| Azure Dragon Palm | 1 | heal | static | 25 | 15 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 3 | Drowning Strike, Scorch Break, Surfing Strike | DAMAGE | 40, 45 | — | 0 | 0 | 0 | — |
| Increase Damage Given | 1 | Liquid Ember Shell | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Increase Damage Taken | 1 | Drowning Strike | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |
| Decrease Damage Taken | 1 | Surfing Strike | SELF BUFF | 30 | — | 0 | 0 | 0 | — |
| Afterburn | 1 | Liquid Ember Shell | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |
| Lifesteal | 1 | Liquid Ember Shell | SELF BUFF | 40 | — | 0 | 0 | 0 | — |
| Reflect | 1 | Scorch Break | SELF BUFF | 40 | — | 0 | 0 | 0 | — |
| Heal | 1 | Azure Dragon Palm | SELF BUFF | 25 | — | 0 | 0 | 0 | — |

Supported rows total: **10**. Unsupported tags present (no potency): move, pierce.

## Selector / classification audit

- Signature elements on damage/pierce rows: Boil
- Proposed potency classification label: **Boil** (element)
- Single signature element on the kit's damage/pierce rows; usable as the classification label under the proposed whole-kit classification, provided the classification is bloodline-scoped (see census collisions) rather than a bare element match.
- Current resolver with `affectedElements=['Boil']`: 3 of 10 supported rows match directly; 7 fall back to None; 0 carry other elements only. Exclusive under current resolver: no.
- Census collisions on signature elements: none among the 95 captured bloodline kits.
- Normal-jutsu collision: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). Whether NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu carry this element needs a read-only public jutsu listing capture requested from dauntless.
- Item-gated jutsu: none
- Mode-restricted jutsu: none
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

## Afterburn and downstream notes

Application rows: Liquid Ember Shell row 2 (35%, 2 rounds).
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

