# Reptilian  — Bloodright kit dossier

**Review id:** BR-057 · **Bloodline id:** `z78aHAPRQfctiw7_qNXMx` · **Rank:** B · **Stat classification:** Ninjutsu · **Traits:** Summoning  · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 20 | 0.15 | INHERIT | — | Ninjutsu | percentage |
| increasedamagetaken | 10 | 0 | INHERIT | — | Genjutsu | percentage |
| lifesteal | 10 | 0 | INHERIT | — | Ninjutsu | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Summoning: Reptile Zoo | public | BLOODLINE | D | EMPTY_GROUND | 2 | 40 | 8 | SINGLE | — | PVP | 0 / 3 |
| Cool-Blooded Empowerment | public | BLOODLINE | D | ALLY | 4 | 40 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 2 / 3 |
| Reptile Chimera | public | BLOODLINE | A | SELF | 0 | 40 | 7 | SINGLE | — | BOTH | 2 / 2 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Stat / general filter | Friendly fire | Recipient | Role | ✓ | Adverse | Ally hazard | Enemy hazard |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|---|---|---|---|
| Summoning: Reptile Zoo | 0 | summon | percentage | 60% | 35 + 1/lvl | 3 | None | — | FRIENDLY | self | SELF BUFF |  |  |  |  |
| Summoning: Reptile Zoo | 1 | injectjutsus | static | 100 | 100 + 0/lvl | 2 | None | — | ALL | self | SELF BUFF |  |  |  |  |
| Summoning: Reptile Zoo | 2 | visual | static | 1 | 1 + 0/lvl | — | None | — | none (=ALL) | self | SELF DEBUFF |  | **yes** |  |  |
| Cool-Blooded Empowerment | 0 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | Highest | FRIENDLY | ally | ALLY BUFF | ✓ |  |  |  |
| Cool-Blooded Empowerment | 1 | lifesteal | percentage | 35% | 25 + 0.4/lvl | 2 | None | Highest | FRIENDLY | ally | ALLY BUFF | ✓ |  |  |  |
| Cool-Blooded Empowerment | 2 | visual | static | 1 | 1 + 0/lvl | — | None | — | none (=ALL) | ally | ENEMY DEBUFF |  | **yes** |  |  |
| Reptile Chimera | 0 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | Ninjutsu | none (=ALL) | self | SELF BUFF | ✓ |  |  |  |
| Reptile Chimera | 1 | decreasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | self | SELF BUFF | ✓ |  |  |  |

Stat/general filters on an element-less row are not binding at the pin: `getEfficiencyRatio` pushes `None` for an empty element list on both sides, so such a row matches every element-less damage effect of any stat type (basic attacks, non-elemental jutsu) and excludes only elemental damage of a non-listed stat type (SOURCE_MECHANICS.md §3). `Ally hazard` marks harmful INHERIT rows delivered by an area method or ground target with friendly fire none/ALL: allies inside the area also receive them (checkFriendlyFire treats an absent value as ALL); on OTHER_USER-target area jutsu the caster is never a target, on GROUND/EMPTY_GROUND spawns the ground effect is re-applied each round to whoever stands on the tiles, the caster included. `Enemy hazard` marks positive INHERIT rows on GROUND/EMPTY_GROUND spawns with friendly fire none/ALL: enemies standing on the tiles receive the buff too. SELF-target rows on ground actions are realized on the caster at cast time (actions.ts 980-1004), not through the tiles.

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Increase Damage Given | 2 | Cool-Blooded Empowerment, Reptile Chimera | ALLY BUFF, SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Decrease Damage Taken | 1 | Reptile Chimera | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Lifesteal | 1 | Cool-Blooded Empowerment | ALLY BUFF | 35 | — | 0 | 0 | 0 | — |

Supported rows total: **4**. Unsupported tags present (no potency): injectjutsus, summon, visual.

## Potency classification audit (element-wide, RUL-2026-10-03-005)

- Signature elements on damage/pierce rows: none
- Proposed potency classification: **Reptilian** (classification extension; status: requires classification extension)
- Qualifying elements: none (requires classification extension)
- No non-None element on any damage/pierce row, so no existing element identifies this kit. Requires a classification extension: a new jutsu classification (placeholder name 'Reptilian') assigned to jutsu records. It is not a bloodline-id selector; which jutsu carry it is a director/engine decision. Targeting 'None' would reach every non-elemental row in the game.
- Not selectors: bloodline id or bloodline ownership; equipment / required bloodline item (castability gate only); injected-child provenance; jutsu names (examples only).
- Kit jutsu of the qualifying element by their own rows (derived, train.ts checkJutsuElements union): none
- Kit jutsu in scope only by authored jutsu classification (no qualifying element on any row): Summoning: Reptile Zoo (None), Cool-Blooded Empowerment (None), Reptile Chimera (None)
- Current resolver with `affectedElements=['None']`: 4 of 4 supported rows match directly; 4 fall back to None; 0 carry other elements only. Current resolver matches each effect row's own elements (absent list -> ['None']); it has no jutsu-level classification. Rows on a qualifying jutsu that do not carry the element are unreachable today: ENGINE GAP, not a design question.
- Off-kit coverage: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu of the qualifying element are in scope by rule; how many exist needs a read-only public jutsu listing capture.
- Item-gated jutsu (castability only, not a potency selector): none
- Mode-restricted jutsu: Summoning: Reptile Zoo (PVP)
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

### Injected children

| Parent | Child | Child id | Child bloodlineId | Child type | Resolved | Child supported rows |
|---|---|---|---|---|---|---|
| Summoning: Reptile Zoo | Summoning: Reptile King | `VnLuKCX1hXm1Hqf0k__XB` | `` | SPECIAL | yes | — |

Injected children are cast as `jutsu` actions at the inject power as level (actions.ts handleInjectedJutsus), so the resolver would process them. Provenance is not a selector: a child qualifies when it is a jutsu of the qualifying element (its own rows, or an authored jutsu classification), like any other jutsu.


## Afterburn and downstream notes

No Afterburn application rows in this kit.
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

