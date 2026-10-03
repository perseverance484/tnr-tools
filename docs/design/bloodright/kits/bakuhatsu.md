# Bakuhatsu — Bloodright kit dossier

**Review id:** BR-008 · **Bloodline id:** `RNUcHSH2c00IhOLc2C9aJ` · **Rank:** A · **Stat classification:** Highest · **Traits:** AoE Control  · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 25 | 0.15 | INHERIT | Lightning, Earth, Explosion, None | — | percentage |
| decreasedamagetaken | 15 | 0 | INHERIT | Earth | — | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Inferno Cataclysm | public | BLOODLINE | A | GROUND | 4 | 60 | 7 | AOE_SPIRAL_SHOOT | — | BOTH | 1 / 2 |
| Kinetic Nova | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 1 / 2 |
| Blast Shield | public | BLOODLINE | D | EMPTY_GROUND | 1 | 40 | 7 | AOE_CIRCLE_SHOOT | — | BOTH | 1 / 2 |
| Charge 4 Explosion | public | BLOODLINE | C | OTHER_USER | 4 | 40 | 7 | SINGLE | — | BOTH | 3 / 3 |
| Howitzer Crash | public | BLOODLINE | B | EMPTY_GROUND | 5 | 60 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 2 / 3 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Stat / general filter | Friendly fire | Recipient | Role | ✓ | Adverse | Ally hazard | Enemy hazard |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|---|---|---|---|
| Inferno Cataclysm | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Explosion | Highest / Highest | ENEMIES | enemy | DAMAGE | ✓ |  |  |  |
| Inferno Cataclysm | 1 | recoil | percentage | 40% | 30 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ENEMIES | enemy | ENEMY DEBUFF |  |  |  |  |
| Kinetic Nova | 0 | damage | formula | 50 | 40 + 0.4/lvl | 0 | Explosion | Highest / Highest | ENEMIES | enemy | DAMAGE | ✓ |  |  |  |
| Kinetic Nova | 1 | wound | percentage | 25% | 15 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF |  |  | **yes** |  |
| Blast Shield | 0 | decreasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ALL | self | SELF BUFF | ✓ |  |  |  |
| Blast Shield | 1 | barrier | static | 100 | 100 + 0/lvl | 2 | None | — | ALL | self | SELF BUFF |  |  |  | **yes** |
| Charge 4 Explosion | 0 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | Highest | none (=ALL) | self | SELF BUFF | ✓ |  |  |  |
| Charge 4 Explosion | 1 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | Earth, Explosion, Lightning, None | — | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  |  |  |
| Charge 4 Explosion | 2 | afterburn | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  |  |  |
| Howitzer Crash | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Explosion | Highest / Highest | ENEMIES | enemy | DAMAGE | ✓ |  |  |  |
| Howitzer Crash | 1 | move | static | 1 | 1 + 0/lvl | 0 | None | — | none (=ALL) | self | SELF BUFF |  |  |  | **yes** |
| Howitzer Crash | 2 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | Highest | none (=ALL) | self | SELF BUFF | ✓ |  |  |  |

Stat/general filters on an element-less row are not binding at the pin: `getEfficiencyRatio` pushes `None` for an empty element list on both sides, so such a row matches every element-less damage effect of any stat type (basic attacks, non-elemental jutsu) and excludes only elemental damage of a non-listed stat type (SOURCE_MECHANICS.md §3). `Ally hazard` marks harmful INHERIT rows delivered by an area method or ground target with friendly fire none/ALL: allies inside the area also receive them (checkFriendlyFire treats an absent value as ALL); on OTHER_USER-target area jutsu the caster is never a target, on GROUND/EMPTY_GROUND spawns the ground effect is re-applied each round to whoever stands on the tiles, the caster included. `Enemy hazard` marks positive INHERIT rows on GROUND/EMPTY_GROUND spawns with friendly fire none/ALL: enemies standing on the tiles receive the buff too. SELF-target rows on ground actions are realized on the caster at cast time (actions.ts 980-1004), not through the tiles.

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 3 | Howitzer Crash, Inferno Cataclysm, Kinetic Nova | DAMAGE | 40, 50 | — | 0 | 0 | 0 | — |
| Increase Damage Given | 2 | Charge 4 Explosion, Howitzer Crash | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Increase Damage Taken | 1 | Charge 4 Explosion | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |
| Decrease Damage Taken | 1 | Blast Shield | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Afterburn | 1 | Charge 4 Explosion | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |

Supported rows total: **8**. Unsupported tags present (no potency): barrier, move, recoil, wound.

## Potency classification audit (element-wide, RUL-2026-10-03-005)

- Signature elements on damage/pierce rows: Explosion
- Proposed potency classification: **Explosion** (element; status: element)
- Qualifying elements: Explosion
- Single signature element Explosion on the kit's damage/pierce rows. Potency reaches matching supported tags on every Explosion jutsu: this kit, other bloodlines' Explosion jutsu and any NORMAL/SPECIAL/EVENT/FORBIDDEN or injected Explosion jutsu. Sharing the element with other bloodlines is expected, not a collision.
- Not selectors: bloodline id or bloodline ownership; equipment / required bloodline item (castability gate only); injected-child provenance; jutsu names (examples only).
- Kit jutsu of the qualifying element by their own rows (derived, train.ts checkJutsuElements union): Inferno Cataclysm, Kinetic Nova, Charge 4 Explosion, Howitzer Crash
- Kit jutsu in scope only by authored jutsu classification (no qualifying element on any row): Blast Shield (None)
- Current resolver with `affectedElements=['Explosion']`: 4 of 8 supported rows match directly; 4 fall back to None; 0 carry other elements only. Current resolver matches each effect row's own elements (absent list -> ['None']); it has no jutsu-level classification. Rows on a qualifying jutsu that do not carry the element are unreachable today: ENGINE GAP, not a design question.
- Other captured bloodlines with jutsu of the qualifying element (expected sharing): Bakuhatsu Suru Nendo [DEFER] (Explosion: 4 rows, 4 damage)
  - Other captured bloodlines with jutsu of the qualifying element. Sharing is expected. Their bloodline jutsu are castable only by their own bloodline's owners (checkJutsuBloodline, app/src/libs/train.ts 185-188), so they do not widen what one owner can amplify; NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu of the element can.
- Off-kit coverage: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu of the qualifying element are in scope by rule; how many exist needs a read-only public jutsu listing capture.
- Item-gated jutsu (castability only, not a potency selector): none
- Mode-restricted jutsu: none
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

## Afterburn and downstream notes

Application rows: Charge 4 Explosion row 2 (35%, 2 rounds).
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

