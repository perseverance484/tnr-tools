# Loup-Garou — Bloodright kit dossier

**Review id:** BR-042 · **Bloodline id:** `C4q1pAltRIEaI5WrNVAAC` · **Rank:** D · **Stat classification:** Taijutsu · **Traits:** — · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 15 | 0 | SELF | — | Taijutsu | percentage |
| increasedamagetaken | 5 | 0 | SELF | Fire | — | percentage |
| increaseheal | 10 | 0 | SELF | — | — | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Nature's Hunter | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 6 | SINGLE | — | BOTH | 3 / 3 |
| Summon Wolf Companion | public | BLOODLINE | C | EMPTY_GROUND | 1 | 60 | 10 | SINGLE | — | BOTH | 0 / 1 |
| Life reaver | public | BLOODLINE | C | OTHER_USER | 4 | 40 | 6 | SINGLE | — | BOTH | 1 / 2 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Stat / general filter | Friendly fire | Recipient | Role | ✓ | Adverse | Ally hazard | Enemy hazard |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|---|---|---|---|
| Nature's Hunter | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | None | Taijutsu / Speed, Strength | ALL | enemy | DAMAGE | ✓ |  |  |  |
| Nature's Hunter | 1 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | Taijutsu | ALL | self | SELF BUFF | ✓ |  |  |  |
| Nature's Hunter | 2 | heal | static | 25 | 20 + 0.2/lvl | 2 | None | — | ALL | self | SELF BUFF | ✓ |  |  |  |
| Summon Wolf Companion | 0 | summon | percentage | 75% | 65 + 0.4/lvl | 4 | None | — | ENEMIES | enemy | ENEMY BUFF |  | **yes** |  |  |
| Life reaver | 0 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Taijutsu | ALL | enemy | ENEMY DEBUFF | ✓ |  |  |  |
| Life reaver | 1 | absorb | percentage | 30% | 20 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ALL | self | SELF BUFF |  |  |  |  |

Stat/general filters on an element-less row are not binding at the pin: `getEfficiencyRatio` pushes `None` for an empty element list on both sides, so such a row matches every element-less damage effect of any stat type (basic attacks, non-elemental jutsu) and excludes only elemental damage of a non-listed stat type (SOURCE_MECHANICS.md §3). `Ally hazard` marks harmful INHERIT rows delivered by an area method or ground target with friendly fire none/ALL: allies inside the area also receive them (checkFriendlyFire treats an absent value as ALL); on OTHER_USER-target area jutsu the caster is never a target, on GROUND/EMPTY_GROUND spawns the ground effect is re-applied each round to whoever stands on the tiles, the caster included. `Enemy hazard` marks positive INHERIT rows on GROUND/EMPTY_GROUND spawns with friendly fire none/ALL: enemies standing on the tiles receive the buff too. SELF-target rows on ground actions are realized on the caster at cast time (actions.ts 980-1004), not through the tiles.

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 1 | Nature's Hunter | DAMAGE | 40 | — | 0 | 0 | 0 | — |
| Increase Damage Given | 1 | Nature's Hunter | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Increase Damage Taken | 1 | Life reaver | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |
| Heal | 1 | Nature's Hunter | SELF BUFF | 25 | — | 0 | 0 | 0 | — |

Supported rows total: **4**. Unsupported tags present (no potency): absorb, summon.

## Potency classification audit (element-wide, RUL-2026-10-03-005)

- Signature elements on damage/pierce rows: none
- Proposed potency classification: **Loup-Garou** (classification extension; status: requires classification extension)
- Qualifying elements: none (requires classification extension)
- No non-None element on any damage/pierce row, so no existing element identifies this kit. Requires a classification extension: a new jutsu classification (placeholder name 'Loup-Garou') assigned to jutsu records. It is not a bloodline-id selector; which jutsu carry it is a director/engine decision. Targeting 'None' would reach every non-elemental row in the game.
- Not selectors: bloodline id or bloodline ownership; equipment / required bloodline item (castability gate only); injected-child provenance; jutsu names (examples only).
- Kit jutsu of the qualifying element by their own rows (derived, train.ts checkJutsuElements union): none
- Kit jutsu in scope only by authored jutsu classification (no qualifying element on any row): Nature's Hunter (None), Summon Wolf Companion (None), Life reaver (None)
- Current resolver with `affectedElements=['None']`: 4 of 4 supported rows match directly; 4 fall back to None; 0 carry other elements only. Current resolver matches each effect row's own elements (absent list -> ['None']); it has no jutsu-level classification. Rows on a qualifying jutsu that do not carry the element are unreachable today: ENGINE GAP, not a design question.
- Off-kit coverage: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu of the qualifying element are in scope by rule; how many exist needs a read-only public jutsu listing capture.
- Item-gated jutsu (castability only, not a potency selector): none
- Mode-restricted jutsu: none
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

## Afterburn and downstream notes

No Afterburn application rows in this kit.
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

