# Blue Blade Eyes — Bloodright kit dossier

**Review id:** BR-015 · **Bloodline id:** `clh4d6qo4000itb0hrx8t06wq` · **Rank:** S · **Stat classification:** Highest · **Traits:** Control, Burst · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 25 | 0.15 | INHERIT | Water, Wind, Ice, Earth, None | Highest | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Icebound Might | public | BLOODLINE | B | OTHER_USER | 4 | 60 | 7 | AOE_CIRCLE_SPAWN | rGyfKFH3GVLk0NP_6CxL6 | BOTH | 2 / 3 |
| Glacial Volley | public | BLOODLINE | B | OTHER_USER | 4 | 60 | 7 | SINGLE | rGyfKFH3GVLk0NP_6CxL6 | BOTH | 2 / 3 |
| Ice Shackles | public | BLOODLINE | C | OTHER_USER | 4 | 60 | 7 | SINGLE | rGyfKFH3GVLk0NP_6CxL6 | BOTH | 1 / 2 |
| Blade Resonance | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | SINGLE | 8-JfO5cZX_n6rfnCTF2jW | BOTH | 2 / 2 |
| Blue Crimson | public | BLOODLINE | C | OTHER_USER | 4 | 60 | 7 | AOE_CIRCLE_SPAWN | 8-JfO5cZX_n6rfnCTF2jW | BOTH | 2 / 3 |
| Quintessential Flake | public | BLOODLINE | C | EMPTY_GROUND | 5 | 40 | 7 | SINGLE | — | BOTH | 2 / 3 |
| Sapphire Command | public | BLOODLINE | C | OTHER_USER | 5 | 40 | 7 | SINGLE | — | BOTH | 2 / 3 |
| Arctic Frost | public | BLOODLINE | A | OTHER_USER | 5 | 40 | 7 | SINGLE | 8-JfO5cZX_n6rfnCTF2jW | BOTH | 3 / 3 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Stat / general filter | Friendly fire | Recipient | Role | ✓ | Adverse | Ally hazard | Enemy hazard |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|---|---|---|---|
| Icebound Might | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Ice | Highest / Highest | none (=ALL) | enemy | DAMAGE | ✓ |  | **yes** |  |
| Icebound Might | 1 | shield | static | 100 | 100 + 0/lvl | 2 | None | — | ALL | self | SELF BUFF |  |  |  |  |
| Icebound Might | 2 | decreasedamagegiven | percentage | 30% | 20 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ENEMIES | enemy | ENEMY DEBUFF | ✓ |  |  |  |
| Glacial Volley | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Ice | Highest / Highest | none (=ALL) | enemy | DAMAGE | ✓ |  |  |  |
| Glacial Volley | 1 | buffprevent | static | 100 | 100 + 0/lvl | 2 | None | — | ENEMIES | enemy | ENEMY DEBUFF |  |  |  |  |
| Glacial Volley | 2 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | Highest | ALL | self | SELF BUFF | ✓ |  |  |  |
| Ice Shackles | 0 | damage | formula | 45 | 35 + 0.4/lvl | 0 | Ice | Highest / Highest | none (=ALL) | enemy | DAMAGE | ✓ |  |  |  |
| Ice Shackles | 1 | stun | static | 100 | 100 + 0/lvl | 2 | None | — | ENEMIES | enemy | ENEMY DEBUFF |  |  |  |  |
| Blade Resonance | 0 | damage | formula | 45 | 35 + 0.4/lvl | 0 | Ice | Highest / Highest | ENEMIES | enemy | DAMAGE | ✓ |  |  |  |
| Blade Resonance | 1 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | Earth, Ice, None, Water, Wind | — | ENEMIES | enemy | ENEMY DEBUFF | ✓ |  |  |  |
| Blue Crimson | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Ice | Highest / Highest | ENEMIES | enemy | DAMAGE | ✓ |  |  |  |
| Blue Crimson | 1 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | self | SELF BUFF | ✓ |  |  |  |
| Blue Crimson | 2 | wound | percentage | 35% | 25 + 0.4/lvl | 2 | Ice | Highest / Highest | none (=ALL) | enemy | ENEMY DEBUFF |  |  | **yes** |  |
| Quintessential Flake | 0 | decreasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | FRIENDLY | self | SELF BUFF | ✓ |  |  |  |
| Quintessential Flake | 1 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | self | SELF BUFF | ✓ |  |  |  |
| Quintessential Flake | 2 | move | static | 1 | 1 + 0/lvl | — | None | — | none (=ALL) | self | SELF BUFF |  |  |  | **yes** |
| Sapphire Command | 0 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  |  |  |
| Sapphire Command | 1 | decreasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | self | SELF BUFF | ✓ |  |  |  |
| Sapphire Command | 2 | redirection | static | 3 | 3 + 0/lvl | 0 | None | — | none (=ALL) | enemy | ENEMY DEBUFF |  |  |  |  |
| Arctic Frost | 0 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | Earth, Ice, None, Water, Wind | — | ALL | self | SELF BUFF | ✓ |  |  |  |
| Arctic Frost | 1 | lifesteal | percentage | 40% | 30 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ALL | self | SELF BUFF | ✓ |  |  |  |
| Arctic Frost | 2 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ENEMIES | enemy | ENEMY DEBUFF | ✓ |  |  |  |

Stat/general filters on an element-less row are not binding at the pin: `getEfficiencyRatio` pushes `None` for an empty element list on both sides, so such a row matches every element-less damage effect of any stat type (basic attacks, non-elemental jutsu) and excludes only elemental damage of a non-listed stat type (SOURCE_MECHANICS.md §3). `Ally hazard` marks harmful INHERIT rows delivered by an area method or ground target with friendly fire none/ALL: allies inside the area also receive them (checkFriendlyFire treats an absent value as ALL); on OTHER_USER-target area jutsu the caster is never a target, on GROUND/EMPTY_GROUND spawns the ground effect is re-applied each round to whoever stands on the tiles, the caster included. `Enemy hazard` marks positive INHERIT rows on GROUND/EMPTY_GROUND spawns with friendly fire none/ALL: enemies standing on the tiles receive the buff too. SELF-target rows on ground actions are realized on the caster at cast time (actions.ts 980-1004), not through the tiles.

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 5 | Blade Resonance, Blue Crimson, Glacial Volley, Ice Shackles, Icebound Might | DAMAGE | 40, 45 | — | 0 | 5 | 0 | — |
| Increase Damage Given | 4 | Arctic Frost, Blue Crimson, Glacial Volley, Quintessential Flake | SELF BUFF | 35 | — | 0 | 3 | 0 | — |
| Decrease Damage Given | 1 | Icebound Might | ENEMY DEBUFF | 30 | — | 0 | 1 | 0 | — |
| Increase Damage Taken | 3 | Arctic Frost, Blade Resonance, Sapphire Command | ENEMY DEBUFF | 35 | — | 0 | 2 | 0 | — |
| Decrease Damage Taken | 2 | Quintessential Flake, Sapphire Command | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Lifesteal | 1 | Arctic Frost | SELF BUFF | 40 | — | 0 | 1 | 0 | — |

Supported rows total: **16**. Unsupported tags present (no potency): buffprevent, move, redirection, shield, stun, wound.

> **Ally-hazard rows (area delivery, friendly fire none/ALL):** Icebound Might row 0 (damage, AOE_CIRCLE_SPAWN, target OTHER_USER). Potency on these tags also raises what allies standing in the area receive; positioning, not the node, decides.

## Potency classification audit (element-wide, RUL-2026-10-03-005)

- Signature elements on damage/pierce rows: Ice
- Proposed potency classification: **Ice** (element; status: element)
- Qualifying elements: Ice
- Single signature element Ice on the kit's damage/pierce rows. Potency reaches matching supported tags on every Ice jutsu: this kit, other bloodlines' Ice jutsu and any NORMAL/SPECIAL/EVENT/FORBIDDEN or injected Ice jutsu. Sharing the element with other bloodlines is expected, not a collision.
- Not selectors: bloodline id or bloodline ownership; equipment / required bloodline item (castability gate only); injected-child provenance; jutsu names (examples only).
- Kit jutsu of the qualifying element by their own rows (derived, train.ts checkJutsuElements union): Icebound Might, Glacial Volley, Ice Shackles, Blade Resonance, Blue Crimson, Arctic Frost
- Kit jutsu in scope only by authored jutsu classification (no qualifying element on any row): Quintessential Flake (None), Sapphire Command (None)
- Current resolver with `affectedElements=['Ice']`: 7 of 16 supported rows match directly; 9 fall back to None; 0 carry other elements only. Current resolver matches each effect row's own elements (absent list -> ['None']); it has no jutsu-level classification. Rows on a qualifying jutsu that do not carry the element are unreachable today: ENGINE GAP, not a design question.
- Other captured bloodlines with jutsu of the qualifying element (expected sharing): Blue Edge Eyes [EXCLUDE] (Ice: 8 rows, 5 damage); First Flame [DEFER] (Ice: 8 rows, 5 damage); Hyouga Yui [INCLUDE] (Ice: 4 rows, 3 damage); Itzehecayan [DEFER] (Ice: 4 rows, 3 damage); Teno Yuki [INCLUDE] (Ice: 5 rows, 3 damage); The Abbynomaly [DEFER] (Ice: 3 rows, 2 damage); True North [DEFER] (Ice: 4 rows, 3 damage)
  - Other captured bloodlines with jutsu of the qualifying element. Sharing is expected. Their bloodline jutsu are castable only by their own bloodline's owners (checkJutsuBloodline, app/src/libs/train.ts 185-188), so they do not widen what one owner can amplify; NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu of the element can.
- Off-kit coverage: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu of the qualifying element are in scope by rule; how many exist needs a read-only public jutsu listing capture.
- Item-gated jutsu (castability only, not a potency selector): Arctic Frost, Blade Resonance, Blue Crimson, Glacial Volley, Ice Shackles, Icebound Might
- Mode-restricted jutsu: none
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

## Afterburn and downstream notes

No Afterburn application rows in this kit.
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

