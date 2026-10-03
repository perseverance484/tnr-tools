# Ha Yanagi — Bloodright kit dossier

**Review id:** BR-030 · **Bloodline id:** `uNZ2UMfA3BuX-J_1g0fHU` · **Rank:** D · **Stat classification:** Genjutsu · **Traits:** — · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 15 | 0 | INHERIT | — | Genjutsu | percentage |
| increasestat | 10 | 0 | INHERIT | — | Genjutsu | percentage |
| increasedamagetaken | 5 | 0 | INHERIT | — | Taijutsu, Bukijutsu | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Wailing Bark | public | BLOODLINE | B | OTHER_USER | 5 | 40 | 6 | SINGLE | — | BOTH | 2 / 2 |
| Blighted Tree | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | SINGLE | — | BOTH | 2 / 2 |
| Petal Nightmare | public | BLOODLINE | D | OTHER_USER | 4 | 60 | 6 | SINGLE | — | BOTH | 2 / 2 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Recipient | Role | ✓ | Adverse |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|
| Wailing Bark | 0 | decreasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF | ✓ |  |
| Wailing Bark | 1 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Blighted Tree | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | None | enemy | DAMAGE | ✓ |  |
| Blighted Tree | 1 | increasedamagetaken | percentage | 30% | 20 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF | ✓ |  |
| Petal Nightmare | 0 | damage | static | 40 | 30 + 0.4/lvl | 0 | None | enemy | DAMAGE | ✓ |  |
| Petal Nightmare | 1 | decreasedamagegiven | percentage | 30% | 20 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF | ✓ |  |

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 2 | Blighted Tree, Petal Nightmare | DAMAGE | 40 | — | 0 | 0 | 0 | — |
| Increase Damage Given | 1 | Wailing Bark | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Decrease Damage Given | 2 | Petal Nightmare, Wailing Bark | ENEMY DEBUFF | 30, 35 | — | 0 | 0 | 0 | — |
| Increase Damage Taken | 1 | Blighted Tree | ENEMY DEBUFF | 30 | — | 0 | 0 | 0 | — |

Supported rows total: **6**. Unsupported tags present (no potency): none.

## Selector / classification audit

- Signature elements on damage/pierce rows: none
- Proposed potency classification label: **Ha Yanagi** (bloodline-keyed extension)
- No non-None element on any damage/pierce row. No existing element can isolate this kit; a bloodline-keyed classification label (extension of the proposed resolver change) is required. Targeting 'None' would reach every non-elemental row in the game.
- Current resolver with `affectedElements=['None']`: 6 of 6 supported rows match directly; 6 fall back to None; 0 carry other elements only. Exclusive under current resolver: no.
- Census collisions on signature elements: none among the 95 captured bloodline kits.
- Normal-jutsu collision: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). Whether NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu carry this element needs a read-only public jutsu listing capture requested from dauntless.
- Item-gated jutsu: none
- Mode-restricted jutsu: none
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

## Afterburn and downstream notes

No Afterburn application rows in this kit.
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

