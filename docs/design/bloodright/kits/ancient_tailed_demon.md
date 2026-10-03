# Ancient Tailed Demon — Bloodright kit dossier

**Review id:** BR-004 · **Bloodline id:** `Au5rBnnukEqUv_lRrk1yO` · **Rank:** B · **Stat classification:** Highest · **Traits:** Sustained Damage · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 20 | 0.15 | INHERIT | — | Ninjutsu, Genjutsu, Taijutsu, Bukijutsu | percentage |
| increasedamagetaken | 5 | 0 | INHERIT | — | Ninjutsu, Genjutsu, Taijutsu, Bukijutsu | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Demonic Vitae | public | BLOODLINE | C | SELF | 0 | 40 | 7 | SINGLE | — | BOTH | 2 / 2 |
| Demonic Embrace | public | BLOODLINE | B | OTHER_USER | 4 | 40 | 7 | SINGLE | — | BOTH | 2 / 2 |
| Ancient Demon Roar | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 1 / 2 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Recipient | Role | ✓ | Adverse |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|
| Demonic Vitae | 0 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 3 | None | self | SELF BUFF | ✓ |  |
| Demonic Vitae | 1 | decreasedamagetaken | percentage | 25% | 25 + 0/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Demonic Embrace | 0 | afterburn | percentage | 35% | 25 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF | ✓ |  |
| Demonic Embrace | 1 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF | ✓ |  |
| Ancient Demon Roar | 0 | wound | percentage | 35% | 25 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF |  |  |
| Ancient Demon Roar | 1 | damage | formula | 45 | 35 + 0.4/lvl | 0 | None | enemy | DAMAGE | ✓ |  |

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 1 | Ancient Demon Roar | DAMAGE | 45 | — | 0 | 0 | 0 | — |
| Increase Damage Given | 1 | Demonic Vitae | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Increase Damage Taken | 1 | Demonic Embrace | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |
| Decrease Damage Taken | 1 | Demonic Vitae | SELF BUFF | 25 | — | 0 | 0 | 0 | — |
| Afterburn | 1 | Demonic Embrace | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |

Supported rows total: **5**. Unsupported tags present (no potency): wound.

## Selector / classification audit

- Signature elements on damage/pierce rows: none
- Proposed potency classification label: **Ancient Tailed Demon** (bloodline-keyed extension)
- No non-None element on any damage/pierce row. No existing element can isolate this kit; a bloodline-keyed classification label (extension of the proposed resolver change) is required. Targeting 'None' would reach every non-elemental row in the game.
- Current resolver with `affectedElements=['None']`: 5 of 5 supported rows match directly; 5 fall back to None; 0 carry other elements only. Exclusive under current resolver: no.
- Census collisions on signature elements: none among the 95 captured bloodline kits.
- Normal-jutsu collision: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). Whether NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu carry this element needs a read-only public jutsu listing capture requested from dauntless.
- Item-gated jutsu: none
- Mode-restricted jutsu: none
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

## Afterburn and downstream notes

Application rows: Demonic Embrace row 0 (35%, 2 rounds).
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

