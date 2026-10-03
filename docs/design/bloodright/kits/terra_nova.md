# Terra Nova — Bloodright kit dossier

**Review id:** BR-081 · **Bloodline id:** `AohWgMy9uYF14ivDlE-xq` · **Rank:** C · **Stat classification:** Highest · **Traits:** — · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 15 | 0.15 | INHERIT | Earth | — | percentage |
| increasedamagetaken | 10 | 0 | INHERIT | Lightning | — | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Earthen Fortitude | public | BLOODLINE | D | OTHER_USER | 4 | 60 | 7 | SINGLE | — | BOTH | 2 / 2 |
| Terra Spire | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | AOE_SPIRAL_SHOOT | — | BOTH | 1 / 3 |
| Earth Wall | public | BLOODLINE | D | SELF | 0 | 40 | 7 | SINGLE | — | BOTH | 2 / 2 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Stat / general filter | Friendly fire | Recipient | Role | ✓ | Adverse | Ally hazard | Enemy hazard |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|---|---|---|---|
| Earthen Fortitude | 0 | damage | formula | 38 | 28 + 0.4/lvl | 0 | Earth | Highest / Highest | ENEMIES | enemy | DAMAGE | ✓ |  |  |  |
| Earthen Fortitude | 1 | decreasedamagegiven | percentage | 30% | 20 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ENEMIES | enemy | ENEMY DEBUFF | ✓ |  |  |  |
| Terra Spire | 0 | damage | formula | 38 | 28 + 0.4/lvl | 0 | Earth | Highest / Highest | ENEMIES | enemy | DAMAGE | ✓ |  |  |  |
| Terra Spire | 1 | recoil | percentage | 40% | 30 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ENEMIES | enemy | ENEMY DEBUFF |  |  |  |  |
| Terra Spire | 2 | wound | percentage | 30% | 20 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF |  |  | **yes** |  |
| Earth Wall | 0 | decreasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ALL | self | SELF BUFF | ✓ |  |  |  |
| Earth Wall | 1 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | Earth | — | ALL | self | SELF BUFF | ✓ |  |  |  |

Stat/general filters on an element-less row are not binding at the pin: `getEfficiencyRatio` pushes `None` for an empty element list on both sides, so such a row matches every element-less damage effect of any stat type (basic attacks, non-elemental jutsu) and excludes only elemental damage of a non-listed stat type (SOURCE_MECHANICS.md §3). `Ally hazard` marks harmful INHERIT rows delivered by an area method or ground target with friendly fire none/ALL: allies inside the area also receive them (checkFriendlyFire treats an absent value as ALL); on OTHER_USER-target area jutsu the caster is never a target, on GROUND/EMPTY_GROUND spawns the ground effect is re-applied each round to whoever stands on the tiles, the caster included. `Enemy hazard` marks positive INHERIT rows on GROUND/EMPTY_GROUND spawns with friendly fire none/ALL: enemies standing on the tiles receive the buff too. SELF-target rows on ground actions are realized on the caster at cast time (actions.ts 980-1004), not through the tiles.

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 2 | Earthen Fortitude, Terra Spire | DAMAGE | 38 | — | 0 | 0 | 0 | — |
| Increase Damage Given | 1 | Earth Wall | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Decrease Damage Given | 1 | Earthen Fortitude | ENEMY DEBUFF | 30 | — | 0 | 0 | 0 | — |
| Decrease Damage Taken | 1 | Earth Wall | SELF BUFF | 35 | — | 0 | 0 | 0 | — |

Supported rows total: **5**. Unsupported tags present (no potency): recoil, wound.

## Potency classification audit (element-wide, RUL-2026-10-03-005)

- Signature elements on damage/pierce rows: Earth
- Proposed potency classification: **Earth** (element; status: element)
- Qualifying elements: Earth
- Single signature element Earth on the kit's damage/pierce rows. Potency reaches matching supported tags on every Earth jutsu: this kit, other bloodlines' Earth jutsu and any NORMAL/SPECIAL/EVENT/FORBIDDEN or injected Earth jutsu. Sharing the element with other bloodlines is expected, not a collision.
- Not selectors: bloodline id or bloodline ownership; equipment / required bloodline item (castability gate only); injected-child provenance; jutsu names (examples only).
- Kit jutsu of the qualifying element by their own rows (derived, train.ts checkJutsuElements union): Earthen Fortitude, Terra Spire, Earth Wall
- Kit jutsu in scope only by authored jutsu classification (no qualifying element on any row): none
- Current resolver with `affectedElements=['Earth']`: 3 of 5 supported rows match directly; 2 fall back to None; 0 carry other elements only. Current resolver matches each effect row's own elements (absent list -> ['None']); it has no jutsu-level classification. Rows on a qualifying jutsu that do not carry the element are unreachable today: ENGINE GAP, not a design question.
- Other captured bloodlines with jutsu of the qualifying element (expected sharing): Aerathiel [INCLUDE] (Earth: 2 rows, 0 damage); Amaterasu [DEFER] (Earth: 1 rows, 0 damage); Bakuhatsu [INCLUDE] (Earth: 1 rows, 0 damage); Blissoo [DEFER] (Earth: 8 rows, 1 damage); Blue Blade Eyes [INCLUDE] (Earth: 2 rows, 0 damage); Blue Edge Eyes [EXCLUDE] (Earth: 2 rows, 0 damage); Crust Almighty [DEFER] (Earth: 2 rows, 0 damage); Crystal Essence [INCLUDE] (Earth: 2 rows, 0 damage); First Flame [DEFER] (Earth: 2 rows, 0 damage); Kyuko-sei [INCLUDE] (Earth: 1 rows, 0 damage); Sands of Time [INCLUDE] (Earth: 1 rows, 0 damage); Sea-Maiden’s Kiss [DEFER] (Earth: 1 rows, 0 damage); Shinseina Ki [INCLUDE] (Earth: 1 rows, 0 damage); Shiroi Youso [INCLUDE] (Earth: 5 rows, 0 damage); Suragu [INCLUDE] (Earth: 1 rows, 0 damage); Testing Dummy 2.0 [DEFER] (Earth: 1 rows, 0 damage); Tetsugan [INCLUDE] (Earth: 1 rows, 0 damage); The Abbynomaly [DEFER] (Earth: 1 rows, 0 damage); Timeforged Enigma [DEFER] (Earth: 1 rows, 0 damage); Traveling Sun Praiser [DEFER] (Earth: 5 rows, 1 damage); Yamauba Chigiri [DEFER] (Earth: 2 rows, 1 damage); Youso Shiroi [EXCLUDE] (Earth: 5 rows, 0 damage); Yūhi Ryūjin (夕陽竜神) [DEFER] (Earth: 4 rows, 1 damage)
  - Other captured bloodlines with jutsu of the qualifying element. Sharing is expected. Their bloodline jutsu are castable only by their own bloodline's owners (checkJutsuBloodline, app/src/libs/train.ts 185-188), so they do not widen what one owner can amplify; NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu of the element can.
- Off-kit coverage: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu of the qualifying element are in scope by rule; how many exist needs a read-only public jutsu listing capture.
- Item-gated jutsu (castability only, not a potency selector): none
- Mode-restricted jutsu: none
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

## Afterburn and downstream notes

No Afterburn application rows in this kit.
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

