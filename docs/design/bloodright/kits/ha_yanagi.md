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

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Stat / general filter | Friendly fire | Recipient | Role | ✓ | Adverse | Ally hazard | Enemy hazard |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|---|---|---|---|
| Wailing Bark | 0 | decreasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ALL | enemy | ENEMY DEBUFF | ✓ |  |  |  |
| Wailing Bark | 1 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | self | SELF BUFF | ✓ |  |  |  |
| Blighted Tree | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | None | Genjutsu / Intelligence, Willpower | ALL | enemy | DAMAGE | ✓ |  |  |  |
| Blighted Tree | 1 | increasedamagetaken | percentage | 30% | 20 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  |  |  |
| Petal Nightmare | 0 | damage | static | 40 | 30 + 0.4/lvl | 0 | None | Genjutsu / Intelligence, Willpower | ALL | enemy | DAMAGE | ✓ |  |  |  |
| Petal Nightmare | 1 | decreasedamagegiven | percentage | 30% | 20 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ALL | enemy | ENEMY DEBUFF | ✓ |  |  |  |

Stat/general filters on an element-less row are not binding at the pin: `getEfficiencyRatio` pushes `None` for an empty element list on both sides, so such a row matches every element-less damage effect of any stat type (basic attacks, non-elemental jutsu) and excludes only elemental damage of a non-listed stat type (SOURCE_MECHANICS.md §3). `Ally hazard` marks harmful INHERIT rows delivered by an area method or ground target with friendly fire none/ALL: allies inside the area also receive them (checkFriendlyFire treats an absent value as ALL); on OTHER_USER-target area jutsu the caster is never a target, on GROUND/EMPTY_GROUND spawns the ground effect is re-applied each round to whoever stands on the tiles, the caster included. `Enemy hazard` marks positive INHERIT rows on GROUND/EMPTY_GROUND spawns with friendly fire none/ALL: enemies standing on the tiles receive the buff too. SELF-target rows on ground actions are realized on the caster at cast time (actions.ts 980-1004), not through the tiles.

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 2 | Blighted Tree, Petal Nightmare | DAMAGE | 40 | — | 0 | 0 | 0 | — |
| Increase Damage Given | 1 | Wailing Bark | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Decrease Damage Given | 2 | Petal Nightmare, Wailing Bark | ENEMY DEBUFF | 30, 35 | — | 0 | 0 | 0 | — |
| Increase Damage Taken | 1 | Blighted Tree | ENEMY DEBUFF | 30 | — | 0 | 0 | 0 | — |

Supported rows total: **6**. Unsupported tags present (no potency): none.

## Potency classification audit (element-wide, RUL-2026-10-03-005)

- Signature elements on damage/pierce rows: none
- Proposed potency classification: **Ha Yanagi** (classification extension; status: requires classification extension)
- Qualifying elements: none (requires classification extension)
- No non-None element on any damage/pierce row, so no existing element identifies this kit. Requires a classification extension: a new jutsu classification (placeholder name 'Ha Yanagi') assigned to jutsu records. It is not a bloodline-id selector; which jutsu carry it is a director/engine decision. Targeting 'None' would reach every non-elemental row in the game.
- Not selectors: bloodline id or bloodline ownership; equipment / required bloodline item (castability gate only); injected-child provenance; jutsu names (examples only).
- Kit jutsu of the qualifying element by their own rows (derived, train.ts checkJutsuElements union): none
- Kit jutsu in scope only by authored jutsu classification (no qualifying element on any row): Wailing Bark (None), Blighted Tree (None), Petal Nightmare (None)
- Current resolver with `affectedElements=['None']`: 6 of 6 supported rows match directly; 6 fall back to None; 0 carry other elements only. Current resolver matches each effect row's own elements (absent list -> ['None']); it has no jutsu-level classification. Rows on a qualifying jutsu that do not carry the element are unreachable today: ENGINE GAP, not a design question.
- Off-kit coverage: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu of the qualifying element are in scope by rule; how many exist needs a read-only public jutsu listing capture.
- Item-gated jutsu (castability only, not a potency selector): none
- Mode-restricted jutsu: none
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

## Afterburn and downstream notes

No Afterburn application rows in this kit.
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

