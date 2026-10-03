# Tetsugan — Bloodright kit dossier

**Review id:** BR-083 · **Bloodline id:** `T-MyR4yQ1_aVbaJDLoI07` · **Rank:** H · **Stat classification:** Highest · **Traits:** — · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 25 | 0.15 | INHERIT | Earth, Fire, Metal, None, Water | — | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Tranquil Guard Flowing Form | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | SINGLE | eHXoPCV2QdZuKEs2ykGzS | BOTH | 2 / 3 |
| Enduring Resonance Ward | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | SINGLE | eHXoPCV2QdZuKEs2ykGzS | BOTH | 1 / 2 |
| Pivoting Fortress | public | BLOODLINE | C | OTHER_USER | 4 | 60 | 7 | SINGLE | eHXoPCV2QdZuKEs2ykGzS | BOTH | 2 / 2 |
| Phantom Slash | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | SINGLE | WoaNqRnyBBXRwmKbq8h1D | BOTH | 2 / 3 |
| Crimson Thrust | public | BLOODLINE | C | EMPTY_GROUND | 5 | 60 | 6 | AOE_CIRCLE_SPAWN | WoaNqRnyBBXRwmKbq8h1D | BOTH | 2 / 3 |
| Shadow Pierce | public | BLOODLINE | C | OTHER_USER | 4 | 60 | 7 | SINGLE | WoaNqRnyBBXRwmKbq8h1D | BOTH | 0 / 2 |
| Middle Guard Stance | public | BLOODLINE | A | SELF | 0 | 40 | 7 | SINGLE | — | BOTH | 2 / 3 |
| Equilibrium Guard Strike | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | AOE_LINE_SHOOT | Z7JM5yxPzAN7U6dyZCnMO | BOTH | 2 / 2 |
| Harmonious Slash | public | BLOODLINE | C | OTHER_USER | 4 | 60 | 7 | SINGLE | Z7JM5yxPzAN7U6dyZCnMO | BOTH | 2 / 2 |
| Vacuum Fan | public | BLOODLINE | C | OTHER_USER | 5 | 40 | 7 | AOE_SPIRAL_SHOOT | — | BOTH | 2 / 3 |
| Inner Peace | public | BLOODLINE | C | SELF | 0 | 40 | 7 | SINGLE | Z7JM5yxPzAN7U6dyZCnMO | BOTH | 3 / 3 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Recipient | Role | ✓ | Adverse |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|
| Tranquil Guard Flowing Form | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Metal | enemy | DAMAGE | ✓ |  |
| Tranquil Guard Flowing Form | 1 | decreasedamagegiven | percentage | 30% | 20 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF | ✓ |  |
| Tranquil Guard Flowing Form | 2 | shield | static | 100 | 100 + 0/lvl | 2 | None | self | SELF BUFF |  |  |
| Enduring Resonance Ward | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Metal | enemy | DAMAGE | ✓ |  |
| Enduring Resonance Ward | 1 | recoil | percentage | 40% | 30 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF |  |  |
| Pivoting Fortress | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Metal | enemy | DAMAGE | ✓ |  |
| Pivoting Fortress | 1 | decreasedamagetaken | percentage | 30% | 20 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Phantom Slash | 0 | damage | formula | 50 | 40 + 0.4/lvl | 0 | Metal | enemy | DAMAGE | ✓ |  |
| Phantom Slash | 1 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF | ✓ |  |
| Phantom Slash | 2 | recoil | percentage | 40% | 30 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF |  |  |
| Crimson Thrust | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Metal | enemy | DAMAGE | ✓ |  |
| Crimson Thrust | 1 | afterburn | percentage | 35% | 25 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF | ✓ |  |
| Crimson Thrust | 2 | move | static | 1 | 1 + 0/lvl | — | None | self | SELF BUFF |  |  |
| Shadow Pierce | 0 | pierce | formula | 60 | 50 + 0.4/lvl | 0 | Metal | enemy | ENEMY DEBUFF |  |  |
| Shadow Pierce | 1 | wound | percentage | 30% | 20 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF |  |  |
| Middle Guard Stance | 0 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Middle Guard Stance | 1 | decreasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Middle Guard Stance | 2 | debuffprevent | static | 100 | 90 + 0.4/lvl | 1 | None | self | SELF BUFF |  |  |
| Equilibrium Guard Strike | 0 | damage | formula | 45 | 35 + 0.4/lvl | 0 | Metal | enemy | DAMAGE | ✓ |  |
| Equilibrium Guard Strike | 1 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | Metal | enemy | ENEMY DEBUFF | ✓ |  |
| Harmonious Slash | 0 | damage | formula | 45 | 35 + 0.4/lvl | 0 | Metal | enemy | DAMAGE | ✓ |  |
| Harmonious Slash | 1 | reflect | percentage | 40% | 30 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Vacuum Fan | 0 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | Metal | enemy | ENEMY DEBUFF | ✓ |  |
| Vacuum Fan | 1 | redirection | static | 4 | 4 + 0/lvl | 0 | None | enemy | ENEMY DEBUFF |  |  |
| Vacuum Fan | 2 | decreasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF | ✓ |  |
| Inner Peace | 0 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Inner Peace | 1 | decreasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Inner Peace | 2 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | Earth, Fire, Metal, None, Water | self | SELF BUFF | ✓ |  |

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 7 | Crimson Thrust, Enduring Resonance Ward, Equilibrium Guard Strike, Harmonious Slash, Phantom Slash, Pivoting Fortress, Tranquil Guard Flowing Form | DAMAGE | 40, 45, 50 | — | 0 | 7 | 0 | — |
| Increase Damage Given | 3 | Inner Peace, Middle Guard Stance | SELF BUFF | 35 | Inner Peace | 0 | 2 | 0 | — |
| Decrease Damage Given | 2 | Tranquil Guard Flowing Form, Vacuum Fan | ENEMY DEBUFF | 30, 35 | — | 0 | 1 | 0 | — |
| Increase Damage Taken | 3 | Equilibrium Guard Strike, Phantom Slash, Vacuum Fan | ENEMY DEBUFF | 35 | — | 0 | 2 | 0 | — |
| Decrease Damage Taken | 3 | Inner Peace, Middle Guard Stance, Pivoting Fortress | SELF BUFF | 30, 35 | — | 0 | 2 | 0 | — |
| Afterburn | 1 | Crimson Thrust | ENEMY DEBUFF | 35 | — | 0 | 1 | 0 | — |
| Reflect | 1 | Harmonious Slash | SELF BUFF | 40 | — | 0 | 1 | 0 | — |

Supported rows total: **20**. Unsupported tags present (no potency): debuffprevent, move, pierce, recoil, redirection, shield, wound.

## Selector / classification audit

- Signature elements on damage/pierce rows: Metal
- Proposed potency classification label: **Metal** (element)
- Single signature element on the kit's damage/pierce rows; usable as the classification label under the proposed whole-kit classification, provided the classification is bloodline-scoped (see census collisions) rather than a bare element match.
- Current resolver with `affectedElements=['Metal']`: 10 of 20 supported rows match directly; 10 fall back to None; 0 carry other elements only. Exclusive under current resolver: no.
- Census collisions on signature elements: none among the 95 captured bloodline kits.
- Normal-jutsu collision: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). Whether NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu carry this element needs a read-only public jutsu listing capture requested from dauntless.
- Item-gated jutsu: Crimson Thrust, Enduring Resonance Ward, Equilibrium Guard Strike, Harmonious Slash, Inner Peace, Phantom Slash, Pivoting Fortress, Shadow Pierce, Tranquil Guard Flowing Form
- Mode-restricted jutsu: none
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

## Afterburn and downstream notes

Application rows: Crimson Thrust row 1 (35%, 2 rounds).
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

