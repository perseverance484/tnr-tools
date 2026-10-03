# Primal Radiance — Bloodright kit dossier

**Review id:** BR-055 · **Bloodline id:** `ZewrhKT-qBQxT1eNoBWFP` · **Rank:** C · **Stat classification:** Highest · **Traits:** — · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 15 | 0.15 | INHERIT | Fire | — | percentage |
| increasedamagetaken | 10 | 0 | INHERIT | Water | — | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Primal Incineration | public | BLOODLINE | D | OTHER_USER | 4 | 40 | 7 | SINGLE | — | BOTH | 2 / 2 |
| Fire Style: Beast | public | BLOODLINE | D | OTHER_USER | 4 | 60 | 7 | SINGLE | — | BOTH | 2 / 3 |
| Fire Style: Squirrel | public | BLOODLINE | B | EMPTY_GROUND | 4 | 60 | 6 | AOE_CIRCLE_SPAWN | — | BOTH | 2 / 3 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Stat / general filter | Friendly fire | Recipient | Role | ✓ | Adverse | Ally hazard | Enemy hazard |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|---|---|---|---|
| Primal Incineration | 0 | afterburn | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  |  |  |
| Primal Incineration | 1 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | Fire | Highest | ENEMIES | enemy | ENEMY DEBUFF | ✓ |  |  |  |
| Fire Style: Beast | 0 | damage | formula | 50 | 40 + 0.4/lvl | 0 | Fire | Highest / Highest | ENEMIES | enemy | DAMAGE | ✓ |  |  |  |
| Fire Style: Beast | 1 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | Fire | Highest / Highest | ALL | self | SELF BUFF | ✓ |  |  |  |
| Fire Style: Beast | 2 | wound | percentage | 25% | 15 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF |  |  |  |  |
| Fire Style: Squirrel | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Fire | Highest / Highest | ENEMIES | enemy | DAMAGE | ✓ |  |  |  |
| Fire Style: Squirrel | 1 | move | static | 1 | 1 + 0/lvl | 0 | None | — | none (=ALL) | self | SELF BUFF |  |  |  | **yes** |
| Fire Style: Squirrel | 2 | decreasedamagetaken | percentage | 30% | 20 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ALL | self | SELF BUFF | ✓ |  |  |  |

Stat/general filters on an element-less row are not binding at the pin: `getEfficiencyRatio` pushes `None` for an empty element list on both sides, so such a row matches every element-less damage effect of any stat type (basic attacks, non-elemental jutsu) and excludes only elemental damage of a non-listed stat type (SOURCE_MECHANICS.md §3). `Ally hazard` marks harmful INHERIT rows delivered by an area method or ground target with friendly fire none/ALL: allies inside the area also receive them (checkFriendlyFire treats an absent value as ALL); on OTHER_USER-target area jutsu the caster is never a target, on GROUND/EMPTY_GROUND spawns the ground effect is re-applied each round to whoever stands on the tiles, the caster included. `Enemy hazard` marks positive INHERIT rows on GROUND/EMPTY_GROUND spawns with friendly fire none/ALL: enemies standing on the tiles receive the buff too. SELF-target rows on ground actions are realized on the caster at cast time (actions.ts 980-1004), not through the tiles.

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 2 | Fire Style: Beast, Fire Style: Squirrel | DAMAGE | 40, 50 | — | 0 | 0 | 0 | — |
| Increase Damage Given | 1 | Fire Style: Beast | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Increase Damage Taken | 1 | Primal Incineration | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |
| Decrease Damage Taken | 1 | Fire Style: Squirrel | SELF BUFF | 30 | — | 0 | 0 | 0 | — |
| Afterburn | 1 | Primal Incineration | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |

Supported rows total: **6**. Unsupported tags present (no potency): move, wound.

## Selector / classification audit

- Signature elements on damage/pierce rows: Fire
- Proposed potency classification label: **Primal Radiance** (bloodline-keyed extension)
- Single signature element Fire is a basic element carried on rows of many bloodlines and ordinary jutsu; using it as the classification label would leak broadly. A bloodline-keyed classification label is required; the element is kept as the display element only.
- Current resolver with `affectedElements=['Fire']`: 4 of 6 supported rows match directly; 2 fall back to None; 0 carry other elements only. Exclusive under current resolver: no.
- Census collisions on signature elements (other bloodlines carrying the element on any row): Adorable Shadow of Death [DEFER] (Fire: 1 rows, 0 damage); Amaterasu [DEFER] (Fire: 1 rows, 0 damage); Architect of the Hollow Script [DEFER] (Fire: 2 rows, 0 damage); Blissoo [DEFER] (Fire: 8 rows, 2 damage); Blood-Enchanted Eyes [INCLUDE] (Fire: 1 rows, 0 damage); Blood-Enthralled Eyes [EXCLUDE] (Fire: 1 rows, 0 damage); Crust Almighty [DEFER] (Fire: 2 rows, 0 damage); Crystal Essence [INCLUDE] (Fire: 2 rows, 0 damage); Extinction Herald [DEFER] (Fire: 1 rows, 0 damage); Eyes of the Forsaken Heir [EXCLUDE] (Fire: 3 rows, 0 damage); Eyes of the Forsaken King [INCLUDE] (Fire: 3 rows, 0 damage); Infernal Reaper [DEFER] (Fire: 1 rows, 0 damage); Manhattan Project [DEFER] (Fire: 1 rows, 0 damage); Oblivion Seal [INCLUDE] (Fire: 1 rows, 0 damage); Otaku of the Dark Maiden [DEFER] (Fire: 1 rows, 0 damage); Sea-Maiden’s Kiss [DEFER] (Fire: 1 rows, 0 damage); Shadow Weaver [INCLUDE] (Fire: 2 rows, 0 damage); Shakunetsu Sakura [INCLUDE] (Fire: 1 rows, 0 damage); Shiroi Youso [INCLUDE] (Fire: 6 rows, 1 damage); Solar Soul [DEFER] (Fire: 3 rows, 0 damage); Suragu [INCLUDE] (Fire: 1 rows, 0 damage); Taiyo Kami [REFERENCE] (Fire: 1 rows, 0 damage); Tenohira Musei [INCLUDE] (Fire: 1 rows, 0 damage); Testing Dummy 2.0 [DEFER] (Fire: 2 rows, 1 damage); Tetsugan [INCLUDE] (Fire: 1 rows, 0 damage); Timeforged Enigma [DEFER] (Fire: 2 rows, 0 damage); Traveling Sun Praiser [DEFER] (Fire: 5 rows, 1 damage); Youso Shiroi [EXCLUDE] (Fire: 6 rows, 1 damage); Yūhi Ryūjin (夕陽竜神) [DEFER] (Fire: 4 rows, 1 damage)
- Normal-jutsu collision: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). Whether NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu carry this element needs a read-only public jutsu listing capture requested from dauntless.
- Item-gated jutsu: none
- Mode-restricted jutsu: none
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

## Afterburn and downstream notes

Application rows: Primal Incineration row 0 (35%, 2 rounds).
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

