# Shiroi Youso — Bloodright kit dossier

**Review id:** BR-067 · **Bloodline id:** `vv45N2En3p8VrNcU2acd8` · **Rank:** S · **Stat classification:** Highest · **Traits:** Burst, Defensive Control, Combo Playmaking · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 25 | 0.15 | INHERIT | Earth, Fire, Lightning, Water, Wind | — | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Lightning Release | public | BLOODLINE | B | OTHER_USER | 4 | 60 | 7 | SINGLE | — | BOTH | 2 / 4 |
| Wind Release | public | BLOODLINE | A | EMPTY_GROUND | 5 | 40 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 2 / 3 |
| Element Divine | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 3 / 3 |
| Fire Release | public | BLOODLINE | C | OTHER_USER | 5 | 40 | 7 | SINGLE | — | BOTH | 2 / 4 |
| Water Release | public | BLOODLINE | B | SELF | 0 | 40 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 1 / 3 |
| Earth Release | public | BLOODLINE | D | EMPTY_GROUND | 1 | 40 | 7 | AOE_CIRCLE_SHOOT | — | BOTH | 1 / 2 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Stat / general filter | Friendly fire | Recipient | Role | ✓ | Adverse | Ally hazard | Enemy hazard |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|---|---|---|---|
| Lightning Release | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Lightning | Highest / Highest | none (=ALL) | enemy | DAMAGE | ✓ |  |  |  |
| Lightning Release | 1 | stun | static | 100 | 90 + 0.4/lvl | 2 | None | — | none (=ALL) | enemy | ENEMY DEBUFF |  |  |  |  |
| Lightning Release | 2 | injectjutsus | static | 100 | 100 + 0/lvl | 2 | None | — | none (=ALL) | self | SELF BUFF |  |  |  |  |
| Lightning Release | 3 | afterburn | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Taijutsu, Genjutsu, Ninjutsu | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  |  |  |
| Wind Release | 0 | decreasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | self | SELF BUFF | ✓ |  |  |  |
| Wind Release | 1 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | Earth, Fire, Lightning, Water, Wind | — | none (=ALL) | self | SELF BUFF | ✓ |  |  |  |
| Wind Release | 2 | move | static | 1 | 1 + 0/lvl | — | None | — | none (=ALL) | self | SELF BUFF |  |  |  | **yes** |
| Element Divine | 0 | damage | formula | 45 | 35 + 0.4/lvl | 0 | Fire | Highest / Highest | ENEMIES | enemy | DAMAGE | ✓ |  |  |  |
| Element Divine | 1 | afterburn | percentage | 30% | 20 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  | **yes** |  |
| Element Divine | 2 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | Earth, Fire, Lightning, Water, Wind | — | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  | **yes** |  |
| Fire Release | 0 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | Earth, Fire, Lightning, Water, Wind | — | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  |  |  |
| Fire Release | 1 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | Earth, Fire, Lightning, Water, Wind | — | none (=ALL) | self | SELF BUFF | ✓ |  |  |  |
| Fire Release | 2 | injectjutsus | static | 100 | 100 + 0/lvl | 2 | None | — | none (=ALL) | self | SELF BUFF |  |  |  |  |
| Fire Release | 3 | timedilation | percentage | 100% | 100 + 0/lvl | 1 | Fire, Water, Wind, Earth, Lightning | — | none (=ALL) | self | SELF BUFF |  |  |  |  |
| Water Release | 0 | heal | static | 25 | 15 + 0.4/lvl | 2 | None | — | none (=ALL) | self | SELF BUFF | ✓ |  |  |  |
| Water Release | 1 | absorb | percentage | 35% | 25 + 0.4/lvl | 2 | Water | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | self | SELF BUFF |  |  |  |  |
| Water Release | 2 | injectjutsus | static | 110 | 100 + 0.4/lvl | 2 | None | — | none (=ALL) | self | SELF BUFF |  |  |  |  |
| Earth Release | 0 | decreasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | self | SELF BUFF | ✓ |  |  |  |
| Earth Release | 1 | barrier | static | 100 | 90 + 0.4/lvl | 2 | None | — | none (=ALL) | self | SELF BUFF |  |  |  | **yes** |

Stat/general filters on an element-less row are not binding at the pin: `getEfficiencyRatio` pushes `None` for an empty element list on both sides, so such a row matches every element-less damage effect of any stat type (basic attacks, non-elemental jutsu) and excludes only elemental damage of a non-listed stat type (SOURCE_MECHANICS.md §3). `Ally hazard` marks harmful INHERIT rows delivered by an area method or ground target with friendly fire none/ALL: allies inside the area also receive them (checkFriendlyFire treats an absent value as ALL); on OTHER_USER-target area jutsu the caster is never a target, on GROUND/EMPTY_GROUND spawns the ground effect is re-applied each round to whoever stands on the tiles, the caster included. `Enemy hazard` marks positive INHERIT rows on GROUND/EMPTY_GROUND spawns with friendly fire none/ALL: enemies standing on the tiles receive the buff too. SELF-target rows on ground actions are realized on the caster at cast time (actions.ts 980-1004), not through the tiles.

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 2 | Element Divine, Lightning Release | DAMAGE | 40, 45 | — | 0 | 0 | 0 | — |
| Increase Damage Given | 2 | Fire Release, Wind Release | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Increase Damage Taken | 2 | Element Divine, Fire Release | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |
| Decrease Damage Taken | 2 | Earth Release, Wind Release | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Afterburn | 2 | Element Divine, Lightning Release | ENEMY DEBUFF | 30, 35 | — | 0 | 0 | 0 | — |
| Heal | 1 | Water Release | SELF BUFF | 25 | — | 0 | 0 | 0 | — |

Supported rows total: **11**. Unsupported tags present (no potency): absorb, barrier, injectjutsus, move, stun, timedilation.

> **Ally-hazard rows (area delivery, friendly fire none/ALL):** Element Divine row 1 (afterburn, AOE_CIRCLE_SPAWN, target OTHER_USER); Element Divine row 2 (increasedamagetaken, AOE_CIRCLE_SPAWN, target OTHER_USER). Potency on these tags also raises what allies standing in the area receive; positioning, not the node, decides.

## Potency classification audit (element-wide, RUL-2026-10-03-005)

- Signature elements on damage/pierce rows: Fire, Lightning
- Proposed potency classification: **Fire + Lightning** (multi-element; status: multi-element: director review)
- Qualifying elements: Fire, Lightning
- Several signature elements (Fire, Lightning) on damage/pierce rows. The proposal lists every signature element as qualifying, which reaches every jutsu of any of them; choosing one element, all of them, or a classification extension is a director decision.
- Not selectors: bloodline id or bloodline ownership; equipment / required bloodline item (castability gate only); injected-child provenance; jutsu names (examples only).
- Kit jutsu of the qualifying element by their own rows (derived, train.ts checkJutsuElements union): Lightning Release, Wind Release, Element Divine, Fire Release
- Kit jutsu in scope only by authored jutsu classification (no qualifying element on any row): Water Release (Water), Earth Release (None)
- Current resolver with `affectedElements=['Fire']`: 5 of 11 supported rows match directly; 5 fall back to None; 1 carry other elements only. Current resolver matches each effect row's own elements (absent list -> ['None']); it has no jutsu-level classification. Rows on a qualifying jutsu that do not carry the element are unreachable today: ENGINE GAP, not a design question.
- Current resolver with `affectedElements=['Lightning']`: 5 of 11 supported rows match directly; 5 fall back to None; 1 carry other elements only. Current resolver matches each effect row's own elements (absent list -> ['None']); it has no jutsu-level classification. Rows on a qualifying jutsu that do not carry the element are unreachable today: ENGINE GAP, not a design question.
- Other captured bloodlines with jutsu of the qualifying element (expected sharing): Adorable Shadow of Death [DEFER] (Fire: 1 rows, 0 damage); Amaterasu [DEFER] (Fire: 1 rows, 0 damage); Architect of the Hollow Script [DEFER] (Fire: 2 rows, 0 damage); Blissoo [DEFER] (Fire: 8 rows, 2 damage); Blood-Enchanted Eyes [INCLUDE] (Fire: 1 rows, 0 damage); Blood-Enthralled Eyes [EXCLUDE] (Fire: 1 rows, 0 damage); Crust Almighty [DEFER] (Fire: 2 rows, 0 damage); Crystal Essence [INCLUDE] (Fire: 2 rows, 0 damage); Extinction Herald [DEFER] (Fire: 1 rows, 0 damage); Eyes of the Forsaken Heir [EXCLUDE] (Fire: 3 rows, 0 damage); Eyes of the Forsaken King [INCLUDE] (Fire: 3 rows, 0 damage); Infernal Reaper [DEFER] (Fire: 1 rows, 0 damage); Manhattan Project [DEFER] (Fire: 1 rows, 0 damage); Oblivion Seal [INCLUDE] (Fire: 1 rows, 0 damage); Otaku of the Dark Maiden [DEFER] (Fire: 1 rows, 0 damage); Primal Radiance [INCLUDE] (Fire: 4 rows, 2 damage); Sea-Maiden’s Kiss [DEFER] (Fire: 1 rows, 0 damage); Shadow Weaver [INCLUDE] (Fire: 2 rows, 0 damage); Shakunetsu Sakura [INCLUDE] (Fire: 1 rows, 0 damage); Solar Soul [DEFER] (Fire: 3 rows, 0 damage); Suragu [INCLUDE] (Fire: 1 rows, 0 damage); Taiyo Kami [REFERENCE] (Fire: 1 rows, 0 damage); Tenohira Musei [INCLUDE] (Fire: 1 rows, 0 damage); Testing Dummy 2.0 [DEFER] (Fire: 2 rows, 1 damage); Tetsugan [INCLUDE] (Fire: 1 rows, 0 damage); Timeforged Enigma [DEFER] (Fire: 2 rows, 0 damage); Traveling Sun Praiser [DEFER] (Fire: 5 rows, 1 damage); Youso Shiroi [EXCLUDE] (Fire: 6 rows, 1 damage); Yūhi Ryūjin (夕陽竜神) [DEFER] (Fire: 4 rows, 1 damage); Adorable Shadow of Death [DEFER] (Lightning: 1 rows, 0 damage); Architect of the Hollow Script [DEFER] (Lightning: 2 rows, 0 damage); Bakuhatsu [INCLUDE] (Lightning: 1 rows, 0 damage); Blissoo [DEFER] (Lightning: 9 rows, 2 damage); Blood-Enchanted Eyes [INCLUDE] (Lightning: 1 rows, 0 damage); Blood-Enthralled Eyes [EXCLUDE] (Lightning: 1 rows, 0 damage); Extinction Herald [DEFER] (Lightning: 1 rows, 0 damage); Eyes of the Forsaken Heir [EXCLUDE] (Lightning: 3 rows, 0 damage); Eyes of the Forsaken King [INCLUDE] (Lightning: 3 rows, 0 damage); Houkyuken [INCLUDE] (Lightning: 2 rows, 0 damage); Infernal Reaper [DEFER] (Lightning: 1 rows, 0 damage); Itojinsei [INCLUDE] (Lightning: 2 rows, 0 damage); Oblivion Seal [INCLUDE] (Lightning: 1 rows, 0 damage); Otaku of the Dark Maiden [DEFER] (Lightning: 1 rows, 0 damage); Shadow Weaver [INCLUDE] (Lightning: 2 rows, 0 damage); Shinrai Ou [INCLUDE] (Lightning: 2 rows, 0 damage); Solar Soul [DEFER] (Lightning: 3 rows, 0 damage); Tenohira Musei [INCLUDE] (Lightning: 1 rows, 0 damage); Testing Dummy 2.0 [DEFER] (Lightning: 2 rows, 1 damage); Timeforged Enigma [DEFER] (Lightning: 2 rows, 0 damage); Traveling Sun Praiser [DEFER] (Lightning: 6 rows, 2 damage); Voltara Divine [INCLUDE] (Lightning: 3 rows, 2 damage); Youso Shiroi [EXCLUDE] (Lightning: 6 rows, 1 damage); Yūhi Ryūjin (夕陽竜神) [DEFER] (Lightning: 4 rows, 1 damage)
  - Other captured bloodlines with jutsu of the qualifying element. Sharing is expected. Their bloodline jutsu are castable only by their own bloodline's owners (checkJutsuBloodline, app/src/libs/train.ts 185-188), so they do not widen what one owner can amplify; NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu of the element can.
- Off-kit coverage: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu of the qualifying element are in scope by rule; how many exist needs a read-only public jutsu listing capture.
- Item-gated jutsu (castability only, not a potency selector): none
- Mode-restricted jutsu: none
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

### Injected children

| Parent | Child | Child id | Child bloodlineId | Child type | Resolved | Child supported rows |
|---|---|---|---|---|---|---|
| Lightning Release | Planetary Devastation | `_PT0SIUUrxc7BhCP6vgf4` | `` | SPECIAL | yes | damage(Earth), decreasedamagegiven |
| Lightning Release | Voltari | `uVRjiBKSVATMYxEqPZuFw` | `` | SPECIAL | yes | damage(Lightning), increasedamagegiven(Earth,Lightning,Water) |
| Fire Release | Great Fire Annihilation | `e2aXCoMWr08f-FX98lnzT` | `` | SPECIAL | yes | damage(Fire) |
| Fire Release | Great Vacuum Bullet | `xZb-PpWYfSdyalB9H_2Km` | `` | SPECIAL | yes | damage(Wind), lifesteal |
| Water Release | Rising Water Slicer | `fZ5U-OPvhQ6ilscJr3hru` | `` | SPECIAL | yes | damage(Water), increasedamagetaken(Earth,Fire,Lightning) |

Injected children are cast as `jutsu` actions at the inject power as level (actions.ts handleInjectedJutsus), so the resolver would process them. Provenance is not a selector: a child qualifies when it is a jutsu of the qualifying element (its own rows, or an authored jutsu classification), like any other jutsu.


## Afterburn and downstream notes

Application rows: Lightning Release row 3 (35%, 2 rounds); Element Divine row 1 (30%, 2 rounds).
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

