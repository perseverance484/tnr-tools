# Namikaze — Bloodright kit dossier

**Review id:** BR-048 · **Bloodline id:** `0Uc2Nfgg08kqGm78QAwZ4` · **Rank:** C · **Stat classification:** Highest · **Traits:** — · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 15 | 0.15 | INHERIT | Wind | — | percentage |
| increasedamagetaken | 10 | 0 | INHERIT | Fire | — | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Wind Step | public | BLOODLINE | D | EMPTY_GROUND | 5 | 60 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 2 / 3 |
| Tempest Shroud | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 3 / 3 |
| Cutting Tempest | public | BLOODLINE | C | OTHER_USER | 4 | 60 | 6 | SINGLE | — | BOTH | 2 / 2 |
| Soaring Fujin | hidden | NORMAL | D | SELF | 0 | 60 | 6 | SINGLE | — | BOTH | 1 / 2 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Stat / general filter | Friendly fire | Recipient | Role | ✓ | Adverse | Ally hazard |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|---|---|---|
| Wind Step | 0 | move | static | 1 | 1 + 0/lvl | — | None | — | none (=ALL) | self | SELF BUFF |  |  |  |
| Wind Step | 1 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Wind | Highest / Highest | ENEMIES | enemy | DAMAGE | ✓ |  |  |
| Wind Step | 2 | decreasedamagegiven | percentage | 30% | 20 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ENEMIES | enemy | ENEMY DEBUFF | ✓ |  |  |
| Tempest Shroud | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Wind | Highest / Highest | ENEMIES | enemy | DAMAGE | ✓ |  |  |
| Tempest Shroud | 1 | decreasedamagetaken | percentage | 30% | 20 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ALL | self | SELF BUFF | ✓ |  |  |
| Tempest Shroud | 2 | afterburn | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  | **yes** |
| Cutting Tempest | 0 | damage | formula | 45 | 35 + 0.4/lvl | 0 | Wind | Highest / Highest | ENEMIES | enemy | DAMAGE | ✓ |  |  |
| Cutting Tempest | 1 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | Wind | — | ALL | self | SELF BUFF | ✓ |  |  |
| Soaring Fujin | 0 | increasedamagegiven | percentage | 21.25% | 15 + 0.25/lvl | 2 | Wind | Highest / Speed, Strength, Intelligence, Willpower | ALL | self | SELF BUFF | ✓ |  |  |
| Soaring Fujin | 1 | decreasepoolcost | percentage | 18.75% | 15 + 0.15/lvl | 3 | None | — | ALL | self | SELF BUFF |  |  |  |

Stat/general filters on an element-less row are not binding at the pin: `getEfficiencyRatio` pushes `None` for an empty element list on both sides, so such a row matches every element-less damage effect of any stat type (basic attacks, non-elemental jutsu) and excludes only elemental damage of a non-listed stat type (SOURCE_MECHANICS.md §3). `Ally hazard` marks harmful rows delivered by an area method or ground target with friendly fire none/ALL: allies and the caster inside the area also receive them (checkFriendlyFire treats an absent value as ALL).

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 3 | Cutting Tempest, Tempest Shroud, Wind Step | DAMAGE | 40, 45 | — | 0 | 0 | 0 | — |
| Increase Damage Given | 2 | Cutting Tempest, Soaring Fujin | SELF BUFF | 21.25, 35 | — | 1 | 0 | 0 | — |
| Decrease Damage Given | 1 | Wind Step | ENEMY DEBUFF | 30 | — | 0 | 0 | 0 | — |
| Decrease Damage Taken | 1 | Tempest Shroud | SELF BUFF | 30 | — | 0 | 0 | 0 | — |
| Afterburn | 1 | Tempest Shroud | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |

Supported rows total: **8**. Unsupported tags present (no potency): decreasepoolcost, move.

> **Ally-hazard rows (area delivery, friendly fire none/ALL):** Tempest Shroud row 2 (afterburn, AOE_CIRCLE_SPAWN, target OTHER_USER). Potency on these tags also raises what allies standing in the area receive; positioning, not the node, decides.

## Selector / classification audit

- Signature elements on damage/pierce rows: Wind
- Proposed potency classification label: **Namikaze** (bloodline-keyed extension)
- Single signature element Wind is a basic element carried on rows of many bloodlines and ordinary jutsu; using it as the classification label would leak broadly. A bloodline-keyed classification label is required; the element is kept as the display element only.
- Current resolver with `affectedElements=['Wind']`: 5 of 8 supported rows match directly; 3 fall back to None; 0 carry other elements only. Exclusive under current resolver: no.
- Census collisions on signature elements (other bloodlines carrying the element on any row): Aerathiel [INCLUDE] (Wind: 2 rows, 0 damage); Architect of the Hollow Script [DEFER] (Wind: 2 rows, 0 damage); Blissoo [DEFER] (Wind: 6 rows, 1 damage); Blue Blade Eyes [INCLUDE] (Wind: 2 rows, 0 damage); Blue Edge Eyes [EXCLUDE] (Wind: 2 rows, 0 damage); Crust Almighty [DEFER] (Wind: 2 rows, 0 damage); Eyes of the Forsaken Heir [EXCLUDE] (Wind: 3 rows, 0 damage); Eyes of the Forsaken King [INCLUDE] (Wind: 3 rows, 0 damage); First Flame [DEFER] (Wind: 2 rows, 0 damage); Houkyuken [INCLUDE] (Wind: 2 rows, 0 damage); Hyouga Yui [INCLUDE] (Wind: 1 rows, 0 damage); Itojinsei [INCLUDE] (Wind: 2 rows, 0 damage); Itzehecayan [DEFER] (Wind: 1 rows, 0 damage); Kyuko-sei [INCLUDE] (Wind: 1 rows, 0 damage); Manhattan Project [DEFER] (Wind: 1 rows, 0 damage); Sands of Time [INCLUDE] (Wind: 1 rows, 0 damage); Shakunetsu Sakura [INCLUDE] (Wind: 1 rows, 0 damage); Shiroi Youso [INCLUDE] (Wind: 5 rows, 0 damage); Solar Soul [DEFER] (Wind: 3 rows, 0 damage); Taiyo Kami [REFERENCE] (Wind: 1 rows, 0 damage); Teno Yuki [INCLUDE] (Wind: 2 rows, 0 damage); Testing Dummy 2.0 [DEFER] (Wind: 1 rows, 0 damage); The Abbynomaly [DEFER] (Wind: 1 rows, 0 damage); Timeforged Enigma [DEFER] (Wind: 1 rows, 0 damage); Traveling Sun Praiser [DEFER] (Wind: 5 rows, 1 damage); True North [DEFER] (Wind: 1 rows, 0 damage); Youso Shiroi [EXCLUDE] (Wind: 5 rows, 0 damage); Yūhi Ryūjin (夕陽竜神) [DEFER] (Wind: 5 rows, 1 damage)
- Normal-jutsu collision: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). Whether NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu carry this element needs a read-only public jutsu listing capture requested from dauntless.
- Item-gated jutsu: none
- Mode-restricted jutsu: none
- Hidden jutsu in kit: Soaring Fujin
- Non-BLOODLINE jutsu types in kit: Soaring Fujin (NORMAL)

## Afterburn and downstream notes

Application rows: Tempest Shroud row 2 (35%, 2 rounds).
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

