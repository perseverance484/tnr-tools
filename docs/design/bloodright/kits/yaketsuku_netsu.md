# Yaketsuku Netsu — Bloodright kit dossier

**Review id:** BR-092 · **Bloodline id:** `clh4d6qfn000etb0hydj4cdpl` · **Rank:** B · **Stat classification:** Bukijutsu · **Traits:** Sustained DPS · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| reflect | 5 | 0 | INHERIT | — | Bukijutsu, Genjutsu, Highest, Ninjutsu, Taijutsu | percentage |
| increasedamagegiven | 22 | 0.15 | INHERIT | — | Bukijutsu | percentage |
| increasedamagetaken | 10 | 0 | INHERIT | — | Ninjutsu | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Forgotten Ember Blade | public | BLOODLINE | C | OTHER_USER | 4 | 60 | 6 | SINGLE | — | BOTH | 2 / 2 |
| Forbidden Chakra Fury | public | BLOODLINE | C | OTHER_USER | 4 | 60 | 7 | SINGLE | — | BOTH | 2 / 2 |
| Chakra Shield | public | BLOODLINE | A | SELF | 0 | 40 | 7 | SINGLE | — | BOTH | 0 / 2 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Recipient | Role | ✓ | Adverse |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|
| Forgotten Ember Blade | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | None | enemy | DAMAGE | ✓ |  |
| Forgotten Ember Blade | 1 | increasedamagegiven | percentage | 30% | 20 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Forbidden Chakra Fury | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | None | enemy | DAMAGE | ✓ |  |
| Forbidden Chakra Fury | 1 | increasedamagetaken | percentage | 30% | 20 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF | ✓ |  |
| Chakra Shield | 0 | absorb | percentage | 30% | 20 + 0.4/lvl | 3 | None | self | SELF BUFF |  |  |
| Chakra Shield | 1 | shield | static | 100 | 90 + 0.4/lvl | 2 | None | self | SELF BUFF |  |  |

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 2 | Forbidden Chakra Fury, Forgotten Ember Blade | DAMAGE | 40 | — | 0 | 0 | 0 | — |
| Increase Damage Given | 1 | Forgotten Ember Blade | SELF BUFF | 30 | — | 0 | 0 | 0 | — |
| Increase Damage Taken | 1 | Forbidden Chakra Fury | ENEMY DEBUFF | 30 | — | 0 | 0 | 0 | — |

Supported rows total: **4**. Unsupported tags present (no potency): absorb, shield.

## Selector / classification audit

- Signature elements on damage/pierce rows: none
- Proposed potency classification label: **Yaketsuku Netsu** (bloodline-keyed extension)
- No non-None element on any damage/pierce row. No existing element can isolate this kit; a bloodline-keyed classification label (extension of the proposed resolver change) is required. Targeting 'None' would reach every non-elemental row in the game.
- Current resolver with `affectedElements=['None']`: 4 of 4 supported rows match directly; 4 fall back to None; 0 carry other elements only. Exclusive under current resolver: no.
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

