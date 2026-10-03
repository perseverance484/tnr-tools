# Blood-Enchanted Eyes — Bloodright kit dossier

**Review id:** BR-011 · **Bloodline id:** `ovZIWu28ANn-Cij5TjT8S` · **Rank:** S · **Stat classification:** Highest · **Traits:** Burst Healing, Sustained Damage · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 25 | 0.15 | INHERIT | Water, Fire, Lightning, None, Shadow | Highest | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Ring of Spilled Blood | public | BLOODLINE | A | GROUND | 4 | 60 | 7 | AOE_SPIRAL_SHOOT | 1wJsQWvK2L0fhziIE4gnA | BOTH | 2 / 2 |
| Crimson Tithe | public | BLOODLINE | A | OPPONENT | 4 | 60 | 7 | SINGLE | 1wJsQWvK2L0fhziIE4gnA | BOTH | 1 / 3 |
| Sanguine Plague | public | BLOODLINE | C | OTHER_USER | 5 | 40 | 7 | SINGLE | 1wJsQWvK2L0fhziIE4gnA | BOTH | 2 / 3 |
| Reaper's Embrace | public | BLOODLINE | A | EMPTY_GROUND | 5 | 60 | 7 | AOE_CIRCLE_SPAWN | heZTbHCjEACrJ-_Vrulq4 | BOTH | 2 / 4 |
| Unholy Enhancement | public | BLOODLINE | C | OTHER_USER | 5 | 40 | 7 | SINGLE | — | BOTH | 2 / 2 |
| Crimson Impact | public | BLOODLINE | B | OTHER_USER | 4 | 60 | 7 | AOE_CIRCLE_SPAWN | heZTbHCjEACrJ-_Vrulq4 | BOTH | 3 / 4 |
| Hemocure | public | BLOODLINE | B | SELF | 0 | 40 | 7 | SINGLE | — | BOTH | 2 / 3 |
| Thousand Strike | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | SINGLE | heZTbHCjEACrJ-_Vrulq4 | BOTH | 1 / 2 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Stat / general filter | Friendly fire | Recipient | Role | ✓ | Adverse | Ally hazard | Enemy hazard |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|---|---|---|---|
| Ring of Spilled Blood | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Shadow | Highest / Highest | ENEMIES | enemy | DAMAGE | ✓ |  |  |  |
| Ring of Spilled Blood | 1 | decreasedamagegiven | percentage | 30% | 20 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  | **yes** |  |
| Crimson Tithe | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Shadow | Highest / Highest | none (=ALL) | enemy | DAMAGE | ✓ |  |  |  |
| Crimson Tithe | 1 | stun | static | 100 | 100 + 0/lvl | 2 | None | — | none (=ALL) | enemy | ENEMY DEBUFF |  |  |  |  |
| Crimson Tithe | 2 | timecompression | percentage | 100% | 100 + 0/lvl | 1 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ENEMIES | enemy | ENEMY DEBUFF |  |  |  |  |
| Sanguine Plague | 0 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | Fire, Lightning, None, Shadow, Water | — | ENEMIES | enemy | ENEMY DEBUFF | ✓ |  |  |  |
| Sanguine Plague | 1 | afterburn | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ENEMIES | enemy | ENEMY DEBUFF | ✓ |  |  |  |
| Sanguine Plague | 2 | debuffprevent | static | 100 | 100 + 0/lvl | 1 | None | — | FRIENDLY | self | SELF BUFF |  |  |  |  |
| Reaper's Embrace | 0 | damage | formula | 50 | 40 + 0.4/lvl | 0 | Shadow | Highest / Highest | ENEMIES | enemy | DAMAGE | ✓ |  |  |  |
| Reaper's Embrace | 1 | move | static | 1 | 1 + 0/lvl | — | None | — | none (=ALL) | self | SELF BUFF |  |  |  | **yes** |
| Reaper's Embrace | 2 | vamp | percentage | 25% | 15 + 0.4/lvl | 0 | None | — | FRIENDLY | self | SELF BUFF |  |  |  |  |
| Reaper's Embrace | 3 | decreasedamagetaken | percentage | 15% | 5 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | FRIENDLY | self | SELF BUFF | ✓ |  |  |  |
| Unholy Enhancement | 0 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ALL | self | SELF BUFF | ✓ |  |  |  |
| Unholy Enhancement | 1 | decreasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  |  |  |
| Crimson Impact | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Shadow | Highest / Highest | ENEMIES | enemy | DAMAGE | ✓ |  |  |  |
| Crimson Impact | 1 | lifesteal | percentage | 20% | 10 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | self | SELF BUFF | ✓ |  |  |  |
| Crimson Impact | 2 | shield | static | 100 | 90 + 0.4/lvl | 2 | None | — | ALL | self | SELF BUFF |  |  |  |  |
| Crimson Impact | 3 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  | **yes** |  |
| Hemocure | 0 | absorb | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | self | SELF BUFF |  |  |  |  |
| Hemocure | 1 | decreasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | self | SELF BUFF | ✓ |  |  |  |
| Hemocure | 2 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | self | SELF BUFF | ✓ |  |  |  |
| Thousand Strike | 0 | pierce | formula | 70 | 60 + 0.4/lvl | 0 | Shadow | Highest / Highest | ENEMIES | enemy | ENEMY DEBUFF |  |  |  |  |
| Thousand Strike | 1 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  |  |  |

Stat/general filters on an element-less row are not binding at the pin: `getEfficiencyRatio` pushes `None` for an empty element list on both sides, so such a row matches every element-less damage effect of any stat type (basic attacks, non-elemental jutsu) and excludes only elemental damage of a non-listed stat type (SOURCE_MECHANICS.md §3). `Ally hazard` marks harmful INHERIT rows delivered by an area method or ground target with friendly fire none/ALL: allies inside the area also receive them (checkFriendlyFire treats an absent value as ALL); on OTHER_USER-target area jutsu the caster is never a target, on GROUND/EMPTY_GROUND spawns the ground effect is re-applied each round to whoever stands on the tiles, the caster included. `Enemy hazard` marks positive INHERIT rows on GROUND/EMPTY_GROUND spawns with friendly fire none/ALL: enemies standing on the tiles receive the buff too. SELF-target rows on ground actions are realized on the caster at cast time (actions.ts 980-1004), not through the tiles.

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 4 | Crimson Impact, Crimson Tithe, Reaper's Embrace, Ring of Spilled Blood | DAMAGE | 40, 50 | — | 0 | 4 | 0 | — |
| Increase Damage Given | 2 | Hemocure, Unholy Enhancement | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Decrease Damage Given | 2 | Ring of Spilled Blood, Unholy Enhancement | ENEMY DEBUFF | 30, 35 | — | 0 | 1 | 0 | — |
| Increase Damage Taken | 3 | Crimson Impact, Sanguine Plague, Thousand Strike | ENEMY DEBUFF | 35 | — | 0 | 3 | 0 | — |
| Decrease Damage Taken | 2 | Hemocure, Reaper's Embrace | SELF BUFF | 15, 35 | — | 0 | 1 | 0 | — |
| Afterburn | 1 | Sanguine Plague | ENEMY DEBUFF | 35 | — | 0 | 1 | 0 | — |
| Lifesteal | 1 | Crimson Impact | SELF BUFF | 20 | — | 0 | 1 | 0 | — |

Supported rows total: **15**. Unsupported tags present (no potency): absorb, debuffprevent, move, pierce, shield, stun, timecompression, vamp.

> **Ally-hazard rows (area delivery, friendly fire none/ALL):** Ring of Spilled Blood row 1 (decreasedamagegiven, AOE_SPIRAL_SHOOT, target GROUND); Crimson Impact row 3 (increasedamagetaken, AOE_CIRCLE_SPAWN, target OTHER_USER). Potency on these tags also raises what allies standing in the area receive; positioning, not the node, decides.

## Potency classification audit (element-wide, RUL-2026-10-03-005)

- Signature elements on damage/pierce rows: Shadow
- Proposed potency classification: **Shadow** (element; status: element)
- Qualifying elements: Shadow
- Single signature element Shadow on the kit's damage/pierce rows. Potency reaches matching supported tags on every Shadow jutsu: this kit, other bloodlines' Shadow jutsu and any NORMAL/SPECIAL/EVENT/FORBIDDEN or injected Shadow jutsu. Sharing the element with other bloodlines is expected, not a collision.
- Not selectors: bloodline id or bloodline ownership; equipment / required bloodline item (castability gate only); injected-child provenance; jutsu names (examples only).
- Kit jutsu of the qualifying element by their own rows (derived, train.ts checkJutsuElements union): Ring of Spilled Blood, Crimson Tithe, Sanguine Plague, Reaper's Embrace, Crimson Impact, Thousand Strike
- Kit jutsu in scope only by authored jutsu classification (no qualifying element on any row): Unholy Enhancement (None), Hemocure (None)
- Current resolver with `affectedElements=['Shadow']`: 5 of 15 supported rows match directly; 10 fall back to None; 0 carry other elements only. Current resolver matches each effect row's own elements (absent list -> ['None']); it has no jutsu-level classification. Rows on a qualifying jutsu that do not carry the element are unreachable today: ENGINE GAP, not a design question.
- Other captured bloodlines with jutsu of the qualifying element (expected sharing): Adorable Shadow of Death [DEFER] (Shadow: 6 rows, 4 damage); Blood-Enshrined Eyes [EXCLUDE] (Shadow: 3 rows, 3 damage); Blood-Enthralled Eyes [EXCLUDE] (Shadow: 6 rows, 5 damage); Extinction Herald [DEFER] (Shadow: 5 rows, 4 damage); Godstorm Eclipse [INCLUDE] (Shadow: 4 rows, 4 damage); Infernal Reaper [DEFER] (Shadow: 4 rows, 3 damage); Kusamochi: Mashumaro Executioner [DEFER] (Shadow: 3 rows, 3 damage); Lilac Seductress [DEFER] (Shadow: 3 rows, 3 damage); Night Parade of A Thousand Demons [INCLUDE] (Shadow: 2 rows, 2 damage); Oblivion Seal [INCLUDE] (Shadow: 5 rows, 4 damage); Otaku of the Dark Maiden [DEFER] (Shadow: 5 rows, 4 damage); Sacrament of Crimson Hunger [DEFER] (Shadow: 3 rows, 3 damage); Shadow Weaver [INCLUDE] (Shadow: 6 rows, 4 damage)
  - Other captured bloodlines with jutsu of the qualifying element. Sharing is expected. Their bloodline jutsu are castable only by their own bloodline's owners (checkJutsuBloodline, app/src/libs/train.ts 185-188), so they do not widen what one owner can amplify; NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu of the element can.
- Off-kit coverage: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu of the qualifying element are in scope by rule; how many exist needs a read-only public jutsu listing capture.
- Item-gated jutsu (castability only, not a potency selector): Crimson Impact, Crimson Tithe, Reaper's Embrace, Ring of Spilled Blood, Sanguine Plague, Thousand Strike
- Mode-restricted jutsu: none
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

## Afterburn and downstream notes

Application rows: Sanguine Plague row 1 (35%, 2 rounds).
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

