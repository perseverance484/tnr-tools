# Tenohira Musei — Bloodright kit dossier

**Review id:** BR-078 · **Bloodline id:** `18Byy1tMXkQETmB88JLl5` · **Rank:** A · **Stat classification:** Highest · **Traits:** Defensive and Control · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 25 | 0.15 | INHERIT | Fire, Lightning, Yin-Yang, None | — | percentage |
| decreasedamagetaken | 15 | 0 | INHERIT | Fire | — | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Moonlit Inferno | public | BLOODLINE | A | OTHER_USER | 4 | 40 | 7 | SINGLE | — | BOTH | 2 / 2 |
| Silent Rift | public | BLOODLINE | A | EMPTY_GROUND | 5 | 60 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 2 / 3 |
| Yin-Yang Cascade | public | BLOODLINE | B | OTHER_USER | 4 | 60 | 7 | SINGLE | — | BOTH | 3 / 3 |
| Silent Palm Strike | public | BLOODLINE | D | OTHER_USER | 4 | 60 | 7 | SINGLE | — | BOTH | 1 / 2 |
| Eternal Stillness | public | BLOODLINE | B | OTHER_USER | 5 | 40 | 7 | SINGLE | — | BOTH | 0 / 2 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Stat / general filter | Friendly fire | Recipient | Role | ✓ | Adverse | Ally hazard | Enemy hazard |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|---|---|---|---|
| Moonlit Inferno | 0 | decreasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  |  |  |
| Moonlit Inferno | 1 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Ninjutsu, Taijutsu, Genjutsu, Bukijutsu | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  |  |  |
| Silent Rift | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Yin-Yang | Highest / Highest | ENEMIES | enemy | DAMAGE | ✓ |  |  |  |
| Silent Rift | 1 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | Highest | none (=ALL) | self | SELF BUFF | ✓ |  |  |  |
| Silent Rift | 2 | move | static | 1 | 1 + 0/lvl | 0 | None | — | none (=ALL) | self | SELF BUFF |  |  |  | **yes** |
| Yin-Yang Cascade | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Yin-Yang | Highest / Highest | ENEMIES | enemy | DAMAGE | ✓ |  |  |  |
| Yin-Yang Cascade | 1 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Highest | ENEMIES | enemy | ENEMY DEBUFF | ✓ |  |  |  |
| Yin-Yang Cascade | 2 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | Fire, Lightning, None, Yin-Yang | — | none (=ALL) | self | SELF BUFF | ✓ |  |  |  |
| Silent Palm Strike | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Yin-Yang | Highest / Highest | ENEMIES | enemy | DAMAGE | ✓ |  |  |  |
| Silent Palm Strike | 1 | seal | static | 100 | 90 + 0.4/lvl | 2 | None | — | none (=ALL) | enemy | ENEMY DEBUFF |  |  |  |  |
| Eternal Stillness | 0 | debuffprevent | static | 100 | 90 + 0.4/lvl | 2 | None | — | ALL | self | SELF BUFF |  |  |  |  |
| Eternal Stillness | 1 | buffprevent | static | 100 | 90 + 0.4/lvl | 2 | None | — | ALL | enemy | ENEMY DEBUFF |  |  |  |  |

Stat/general filters on an element-less row are not binding at the pin: `getEfficiencyRatio` pushes `None` for an empty element list on both sides, so such a row matches every element-less damage effect of any stat type (basic attacks, non-elemental jutsu) and excludes only elemental damage of a non-listed stat type (SOURCE_MECHANICS.md §3). `Ally hazard` marks harmful INHERIT rows delivered by an area method or ground target with friendly fire none/ALL: allies inside the area also receive them (checkFriendlyFire treats an absent value as ALL); on OTHER_USER-target area jutsu the caster is never a target, on GROUND/EMPTY_GROUND spawns the ground effect is re-applied each round to whoever stands on the tiles, the caster included. `Enemy hazard` marks positive INHERIT rows on GROUND/EMPTY_GROUND spawns with friendly fire none/ALL: enemies standing on the tiles receive the buff too. SELF-target rows on ground actions are realized on the caster at cast time (actions.ts 980-1004), not through the tiles.

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 3 | Silent Palm Strike, Silent Rift, Yin-Yang Cascade | DAMAGE | 40 | — | 0 | 0 | 0 | — |
| Increase Damage Given | 2 | Silent Rift, Yin-Yang Cascade | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Decrease Damage Given | 1 | Moonlit Inferno | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |
| Increase Damage Taken | 2 | Moonlit Inferno, Yin-Yang Cascade | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |

Supported rows total: **8**. Unsupported tags present (no potency): buffprevent, debuffprevent, move, seal.

## Potency classification audit (element-wide, RUL-2026-10-03-005)

- Signature elements on damage/pierce rows: Yin-Yang
- Proposed potency classification: **Yin-Yang** (element; status: element)
- Qualifying elements: Yin-Yang
- Single signature element Yin-Yang on the kit's damage/pierce rows. Potency reaches matching supported tags on every Yin-Yang jutsu: this kit, other bloodlines' Yin-Yang jutsu and any NORMAL/SPECIAL/EVENT/FORBIDDEN or injected Yin-Yang jutsu. Sharing the element with other bloodlines is expected, not a collision.
- Not selectors: bloodline id or bloodline ownership; equipment / required bloodline item (castability gate only); injected-child provenance; jutsu names (examples only).
- Kit jutsu of the qualifying element by their own rows (derived, train.ts checkJutsuElements union): Silent Rift, Yin-Yang Cascade, Silent Palm Strike
- Kit jutsu in scope only by authored jutsu classification (no qualifying element on any row): Moonlit Inferno (None), Eternal Stillness (None)
- Current resolver with `affectedElements=['Yin-Yang']`: 4 of 8 supported rows match directly; 4 fall back to None; 0 carry other elements only. Current resolver matches each effect row's own elements (absent list -> ['None']); it has no jutsu-level classification. Rows on a qualifying jutsu that do not carry the element are unreachable today: ENGINE GAP, not a design question.
- Other captured bloodlines with jutsu of the qualifying element (expected sharing): Celestial Mage [DEFER] (Yin-Yang: 4 rows, 4 damage); DvEM [DEFER] (Yin-Yang: 3 rows, 3 damage); Ethereal Monarch [INCLUDE] (Yin-Yang: 3 rows, 3 damage); Ethereal Regent [EXCLUDE] (Yin-Yang: 4 rows, 4 damage); Heavenly Sonata [INCLUDE] (Yin-Yang: 3 rows, 3 damage); Manhattan Project [DEFER] (Yin-Yang: 5 rows, 4 damage); Tenryūseigan [DEFER] (Yin-Yang: 4 rows, 4 damage); Tenshin Shoden Yami-Ryu [DEFER] (Yin-Yang: 4 rows, 4 damage)
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

