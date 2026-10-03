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

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Recipient | Role | ✓ | Adverse |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|
| Icebound Might | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Ice | enemy | DAMAGE | ✓ |  |
| Icebound Might | 1 | shield | static | 100 | 100 + 0/lvl | 2 | None | self | SELF BUFF |  |  |
| Icebound Might | 2 | decreasedamagegiven | percentage | 30% | 20 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF | ✓ |  |
| Glacial Volley | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Ice | enemy | DAMAGE | ✓ |  |
| Glacial Volley | 1 | buffprevent | static | 100 | 100 + 0/lvl | 2 | None | enemy | ENEMY DEBUFF |  |  |
| Glacial Volley | 2 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Ice Shackles | 0 | damage | formula | 45 | 35 + 0.4/lvl | 0 | Ice | enemy | DAMAGE | ✓ |  |
| Ice Shackles | 1 | stun | static | 100 | 100 + 0/lvl | 2 | None | enemy | ENEMY DEBUFF |  |  |
| Blade Resonance | 0 | damage | formula | 45 | 35 + 0.4/lvl | 0 | Ice | enemy | DAMAGE | ✓ |  |
| Blade Resonance | 1 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | Earth, Ice, None, Water, Wind | enemy | ENEMY DEBUFF | ✓ |  |
| Blue Crimson | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Ice | enemy | DAMAGE | ✓ |  |
| Blue Crimson | 1 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Blue Crimson | 2 | wound | percentage | 35% | 25 + 0.4/lvl | 2 | Ice | enemy | ENEMY DEBUFF |  |  |
| Quintessential Flake | 0 | decreasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Quintessential Flake | 1 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Quintessential Flake | 2 | move | static | 1 | 1 + 0/lvl | — | None | self | SELF BUFF |  |  |
| Sapphire Command | 0 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF | ✓ |  |
| Sapphire Command | 1 | decreasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Sapphire Command | 2 | redirection | static | 3 | 3 + 0/lvl | 0 | None | enemy | ENEMY DEBUFF |  |  |
| Arctic Frost | 0 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | Earth, Ice, None, Water, Wind | self | SELF BUFF | ✓ |  |
| Arctic Frost | 1 | lifesteal | percentage | 40% | 30 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Arctic Frost | 2 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF | ✓ |  |

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

## Selector / classification audit

- Signature elements on damage/pierce rows: Ice
- Proposed potency classification label: **Ice** (element)
- Single signature element on the kit's damage/pierce rows; usable as the classification label under the proposed whole-kit classification, provided the classification is bloodline-scoped (see census collisions) rather than a bare element match.
- Current resolver with `affectedElements=['Ice']`: 7 of 16 supported rows match directly; 9 fall back to None; 0 carry other elements only. Exclusive under current resolver: no.
- Census collisions on signature elements (other bloodlines carrying the element on any row): Blue Edge Eyes [EXCLUDE] (Ice: 8 rows, 5 damage); First Flame [DEFER] (Ice: 8 rows, 5 damage); Hyouga Yui [INCLUDE] (Ice: 4 rows, 3 damage); Itzehecayan [DEFER] (Ice: 4 rows, 3 damage); Teno Yuki [INCLUDE] (Ice: 5 rows, 3 damage); The Abbynomaly [DEFER] (Ice: 3 rows, 2 damage); True North [DEFER] (Ice: 4 rows, 3 damage)
- Normal-jutsu collision: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). Whether NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu carry this element needs a read-only public jutsu listing capture requested from dauntless.
- Item-gated jutsu: Arctic Frost, Blade Resonance, Blue Crimson, Glacial Volley, Ice Shackles, Icebound Might
- Mode-restricted jutsu: none
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

## Afterburn and downstream notes

No Afterburn application rows in this kit.
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

