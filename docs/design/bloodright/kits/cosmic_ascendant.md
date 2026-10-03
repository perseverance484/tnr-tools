# Cosmic Ascendant — Bloodright kit dossier

**Review id:** BR-018 · **Bloodline id:** `osVXxtyW61gr-bx5v5ys2` · **Rank:** S · **Stat classification:** Highest · **Traits:** Burst, Defensive  · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 25 | 0.15 | INHERIT | Earth, Fire, Lightning, None, Wind | Highest | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Cosmic Intent | public | BLOODLINE | A | OTHER_USER | 5 | 40 | 7 | SINGLE | — | BOTH | 3 / 3 |
| Cosmic Explosion | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | SINGLE | — | BOTH | 1 / 2 |
| Cosmic Chains | public | BLOODLINE | C | OTHER_USER | 4 | 40 | 7 | SINGLE | — | BOTH | 2 / 2 |
| Cosmic Energy | public | BLOODLINE | D | EMPTY_GROUND | 5 | 40 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 2 / 3 |
| Cosmic Aura | public | BLOODLINE | C | OTHER_USER | 4 | 40 | 7 | SINGLE | — | BOTH | 2 / 3 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Recipient | Role | ✓ | Adverse |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|
| Cosmic Intent | 0 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF | ✓ |  |
| Cosmic Intent | 1 | afterburn | percentage | 35% | 25 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF | ✓ |  |
| Cosmic Intent | 2 | lifesteal | percentage | 40% | 30 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Cosmic Explosion | 0 | damage | formula | 50 | 40 + 0.4/lvl | 0 | None | enemy | DAMAGE | ✓ |  |
| Cosmic Explosion | 1 | wound | percentage | 25% | 15 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF |  |  |
| Cosmic Chains | 0 | decreasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Cosmic Chains | 1 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF | ✓ |  |
| Cosmic Energy | 0 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Cosmic Energy | 1 | decreasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Cosmic Energy | 2 | move | static | 1 | 1 + 0/lvl | 0 | None | self | SELF BUFF |  |  |
| Cosmic Aura | 0 | decreasedamagegiven | percentage | 30% | 20 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF | ✓ |  |
| Cosmic Aura | 1 | decreasedamagetaken | percentage | 30% | 20 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Cosmic Aura | 2 | shield | static | 100 | 90 + 0.4/lvl | 2 | None | self | SELF BUFF |  |  |

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 1 | Cosmic Explosion | DAMAGE | 50 | — | 0 | 0 | 0 | — |
| Increase Damage Given | 1 | Cosmic Energy | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Decrease Damage Given | 1 | Cosmic Aura | ENEMY DEBUFF | 30 | — | 0 | 0 | 0 | — |
| Increase Damage Taken | 2 | Cosmic Chains, Cosmic Intent | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |
| Decrease Damage Taken | 3 | Cosmic Aura, Cosmic Chains, Cosmic Energy | SELF BUFF | 30, 35 | — | 0 | 0 | 0 | — |
| Afterburn | 1 | Cosmic Intent | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |
| Lifesteal | 1 | Cosmic Intent | SELF BUFF | 40 | — | 0 | 0 | 0 | — |

Supported rows total: **10**. Unsupported tags present (no potency): move, shield, wound.

## Selector / classification audit

- Signature elements on damage/pierce rows: none
- Proposed potency classification label: **Cosmic Ascendant** (bloodline-keyed extension)
- No non-None element on any damage/pierce row. No existing element can isolate this kit; a bloodline-keyed classification label (extension of the proposed resolver change) is required. Targeting 'None' would reach every non-elemental row in the game.
- Current resolver with `affectedElements=['None']`: 10 of 10 supported rows match directly; 10 fall back to None; 0 carry other elements only. Exclusive under current resolver: no.
- Census collisions on signature elements: none among the 95 captured bloodline kits.
- Normal-jutsu collision: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). Whether NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu carry this element needs a read-only public jutsu listing capture requested from dauntless.
- Item-gated jutsu: none
- Mode-restricted jutsu: none
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

## Afterburn and downstream notes

Application rows: Cosmic Intent row 1 (35%, 2 rounds).
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

