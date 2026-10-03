# Sea-King's Blessing — Bloodright kit dossier

**Review id:** BR-061 · **Bloodline id:** `juZy8qwituqM2Km6cOiL4` · **Rank:** C · **Stat classification:** Highest · **Traits:** — · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 15 | 0.15 | INHERIT | Water | — | percentage |
| increasedamagetaken | 10 | 0 | INHERIT | Earth | — | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Sea King's Armor | public | BLOODLINE | D | OTHER_USER | 4 | 60 | 7 | SINGLE | — | BOTH | 2 / 3 |
| Crushing Abyss | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 2 / 2 |
| Water Dome | public | BLOODLINE | C | OTHER_USER | 4 | 40 | 6 | SINGLE | — | BOTH | 1 / 3 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Stat / general filter | Friendly fire | Recipient | Role | ✓ | Adverse | Ally hazard | Enemy hazard |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|---|---|---|---|
| Sea King's Armor | 0 | decreasedamagetaken | percentage | 30% | 20 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ALL | self | SELF BUFF | ✓ |  |  |  |
| Sea King's Armor | 1 | damage | formula | 38 | 28 + 0.4/lvl | 0 | Water | Highest / Highest | ENEMIES | enemy | DAMAGE | ✓ |  |  |  |
| Sea King's Armor | 2 | shield | static | 100 | 100 + 0/lvl | 2 | None | — | none (=ALL) | self | SELF BUFF |  |  |  |  |
| Crushing Abyss | 0 | damage | formula | 38 | 28 + 0.4/lvl | 0 | Water | Highest / Highest | ENEMIES | enemy | DAMAGE | ✓ |  |  |  |
| Crushing Abyss | 1 | increasedamagetaken | percentage | 30% | 20 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ENEMIES | enemy | ENEMY DEBUFF | ✓ |  |  |  |
| Water Dome | 0 | absorb | percentage | 35% | 25 + 0.4/lvl | 2 | Water | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ALL | self | SELF BUFF |  |  |  |  |
| Water Dome | 1 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | Water | — | ENEMIES | enemy | ENEMY DEBUFF | ✓ |  |  |  |
| Water Dome | 2 | shield | static | 100 | 100 + 0/lvl | 2 | None | — | none (=ALL) | self | SELF BUFF |  |  |  |  |

Stat/general filters on an element-less row are not binding at the pin: `getEfficiencyRatio` pushes `None` for an empty element list on both sides, so such a row matches every element-less damage effect of any stat type (basic attacks, non-elemental jutsu) and excludes only elemental damage of a non-listed stat type (SOURCE_MECHANICS.md §3). `Ally hazard` marks harmful INHERIT rows delivered by an area method or ground target with friendly fire none/ALL: allies inside the area also receive them (checkFriendlyFire treats an absent value as ALL); on OTHER_USER-target area jutsu the caster is never a target, on GROUND/EMPTY_GROUND spawns the ground effect is re-applied each round to whoever stands on the tiles, the caster included. `Enemy hazard` marks positive INHERIT rows on GROUND/EMPTY_GROUND spawns with friendly fire none/ALL: enemies standing on the tiles receive the buff too. SELF-target rows on ground actions are realized on the caster at cast time (actions.ts 980-1004), not through the tiles.

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 2 | Crushing Abyss, Sea King's Armor | DAMAGE | 38 | — | 0 | 0 | 0 | — |
| Increase Damage Taken | 2 | Crushing Abyss, Water Dome | ENEMY DEBUFF | 30, 35 | — | 0 | 0 | 0 | — |
| Decrease Damage Taken | 1 | Sea King's Armor | SELF BUFF | 30 | — | 0 | 0 | 0 | — |

Supported rows total: **5**. Unsupported tags present (no potency): absorb, shield.

## Selector / classification audit

- Signature elements on damage/pierce rows: Water
- Proposed potency classification label: **Sea-King's Blessing** (bloodline-keyed extension)
- Single signature element Water is a basic element carried on rows of many bloodlines and ordinary jutsu; using it as the classification label would leak broadly. A bloodline-keyed classification label is required; the element is kept as the display element only.
- Current resolver with `affectedElements=['Water']`: 3 of 5 supported rows match directly; 2 fall back to None; 0 carry other elements only. Exclusive under current resolver: no.
- Census collisions on signature elements (other bloodlines carrying the element on any row): Blissoo [DEFER] (Water: 8 rows, 1 damage); Blood-Enchanted Eyes [INCLUDE] (Water: 1 rows, 0 damage); Blood-Enthralled Eyes [EXCLUDE] (Water: 1 rows, 0 damage); Blue Blade Eyes [INCLUDE] (Water: 2 rows, 0 damage); Blue Edge Eyes [EXCLUDE] (Water: 2 rows, 0 damage); Crust Almighty [DEFER] (Water: 2 rows, 0 damage); First Flame [DEFER] (Water: 2 rows, 0 damage); Hyouga Yui [INCLUDE] (Water: 1 rows, 0 damage); Itzehecayan [DEFER] (Water: 1 rows, 0 damage); Manhattan Project [DEFER] (Water: 1 rows, 0 damage); Shinrai Ou [INCLUDE] (Water: 2 rows, 0 damage); Shinseina Ki [INCLUDE] (Water: 1 rows, 0 damage); Shiroi Youso [INCLUDE] (Water: 6 rows, 0 damage); Teno Yuki [INCLUDE] (Water: 2 rows, 0 damage); Testing Dummy 2.0 [DEFER] (Water: 1 rows, 0 damage); Tetsugan [INCLUDE] (Water: 1 rows, 0 damage); The Abbynomaly [DEFER] (Water: 1 rows, 0 damage); Timeforged Enigma [DEFER] (Water: 1 rows, 0 damage); Traveling Sun Praiser [DEFER] (Water: 6 rows, 1 damage); True North [DEFER] (Water: 1 rows, 0 damage); Yamauba Chigiri [DEFER] (Water: 4 rows, 2 damage); Youso Shiroi [EXCLUDE] (Water: 6 rows, 0 damage); Yūhi Ryūjin (夕陽竜神) [DEFER] (Water: 4 rows, 0 damage)
- Normal-jutsu collision: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). Whether NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu carry this element needs a read-only public jutsu listing capture requested from dauntless.
- Item-gated jutsu: none
- Mode-restricted jutsu: none
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

## Afterburn and downstream notes

No Afterburn application rows in this kit.
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

