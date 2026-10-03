# Godstorm Eclipse — Bloodright kit dossier

**Review id:** BR-029 · **Bloodline id:** `szai-IgtB7PLubojIIlh-` · **Rank:** H · **Stat classification:** Highest · **Traits:** Sustain / Burst Heavy / Tank · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 25 | 0.15 | SELF | Fire, Lightning, None, Shadow, Storm, Water, Wind | — | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Event Horizon Gate | public | BLOODLINE | C | OTHER_USER | 5 | 40 | 7 | AOE_CIRCLE_SPAWN | ZaTCUYIgRUoB2CBRo7pLY | BOTH | 2 / 3 |
| Godstorm Mantle: Storm-God's Heart | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | AOE_CIRCLE_SPAWN | g0hPGnF9lLYauTsjxqpAZ | BOTH | 2 / 2 |
| Godstorm Mantle: Heavenbreaker Verdict | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | SINGLE | g0hPGnF9lLYauTsjxqpAZ | BOTH | 0 / 2 |
| Godstorm Mantle: Raijin's Cage | public | BLOODLINE | C | OTHER_USER | 4 | 60 | 7 | SINGLE | g0hPGnF9lLYauTsjxqpAZ | BOTH | 1 / 2 |
| Godstorm Mantle: Tempest | public | BLOODLINE | C | OTHER_USER | 4 | 40 | 7 | SINGLE | g0hPGnF9lLYauTsjxqpAZ | BOTH | 3 / 3 |
| Godstorm Mantle: Sky-Splitting Wall | public | BLOODLINE | C | OTHER_USER | 5 | 40 | 7 | SINGLE | g0hPGnF9lLYauTsjxqpAZ | BOTH | 2 / 3 |
| Godstorm Mantle: Thunder-Crowned Bulwark | public | BLOODLINE | D | EMPTY_GROUND | 5 | 40 | 7 | AOE_CIRCLE_SPAWN | g0hPGnF9lLYauTsjxqpAZ | BOTH | 2 / 3 |
| Obsidian Tomb | public | BLOODLINE | C | OTHER_USER | 4 | 60 | 7 | SINGLE | ZaTCUYIgRUoB2CBRo7pLY | BOTH | 1 / 3 |
| Midnight Verdict | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | AOE_CIRCLE_SPAWN | ZaTCUYIgRUoB2CBRo7pLY | BOTH | 0 / 2 |
| Corona Devourer Palm | public | BLOODLINE | A | GROUND | 4 | 60 | 7 | AOE_SPIRAL_SHOOT | ZaTCUYIgRUoB2CBRo7pLY | BOTH | 1 / 2 |
| Marrow Eclipse Mantle | public | BLOODLINE | D | SELF | 0 | 40 | 7 | SINGLE | ZaTCUYIgRUoB2CBRo7pLY | BOTH | 1 / 2 |
| Black Sun Cataract | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | AOE_CIRCLE_SPAWN | ZaTCUYIgRUoB2CBRo7pLY | BOTH | 1 / 3 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Stat / general filter | Friendly fire | Recipient | Role | ✓ | Adverse | Ally hazard |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|---|---|---|
| Event Horizon Gate | 0 | decreasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | FRIENDLY | self | SELF BUFF | ✓ |  |  |
| Event Horizon Gate | 1 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  | **yes** |
| Event Horizon Gate | 2 | redirection | static | 4 | 4 + 0/lvl | 0 | None | — | none (=ALL) | enemy | ENEMY DEBUFF |  |  | **yes** |
| Godstorm Mantle: Storm-God's Heart | 0 | damage | formula | 45 | 35 + 0.4/lvl | 0 | Storm | Highest / Highest | ENEMIES | enemy | DAMAGE | ✓ |  |  |
| Godstorm Mantle: Storm-God's Heart | 1 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ENEMIES | enemy | ENEMY DEBUFF | ✓ |  |  |
| Godstorm Mantle: Heavenbreaker Verdict | 0 | pierce | formula | 60 | 50 + 0.4/lvl | 0 | Storm | Highest / Highest | ENEMIES | enemy | ENEMY DEBUFF |  |  |  |
| Godstorm Mantle: Heavenbreaker Verdict | 1 | wound | percentage | 30% | 20 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF |  |  |  |
| Godstorm Mantle: Raijin's Cage | 0 | damage | formula | 50 | 40 + 0.4/lvl | 0 | Storm | Highest / Highest | ENEMIES | enemy | DAMAGE | ✓ |  |  |
| Godstorm Mantle: Raijin's Cage | 1 | stun | static | 100 | 90 + 0.4/lvl | 2 | None | — | ENEMIES | enemy | ENEMY DEBUFF |  |  |  |
| Godstorm Mantle: Tempest | 0 | afterburn | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  |  |
| Godstorm Mantle: Tempest | 1 | lifesteal | percentage | 40% | 30 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | self | SELF BUFF | ✓ |  |  |
| Godstorm Mantle: Tempest | 2 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | Highest | none (=ALL) | self | SELF BUFF | ✓ |  |  |
| Godstorm Mantle: Sky-Splitting Wall | 0 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | Highest | none (=ALL) | self | SELF BUFF | ✓ |  |  |
| Godstorm Mantle: Sky-Splitting Wall | 1 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  |  |
| Godstorm Mantle: Sky-Splitting Wall | 2 | debuffprevent | static | 100 | 90 + 0.4/lvl | 1 | None | — | none (=ALL) | self | SELF BUFF |  |  |  |
| Godstorm Mantle: Thunder-Crowned Bulwark | 0 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | self | SELF BUFF | ✓ |  |  |
| Godstorm Mantle: Thunder-Crowned Bulwark | 1 | decreasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | self | SELF BUFF | ✓ |  |  |
| Godstorm Mantle: Thunder-Crowned Bulwark | 2 | move | static | 1 | 1 + 0/lvl | — | None | — | none (=ALL) | self | SELF BUFF |  |  |  |
| Obsidian Tomb | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Shadow | Highest / Highest | none (=ALL) | enemy | DAMAGE | ✓ |  |  |
| Obsidian Tomb | 1 | buffprevent | static | 100 | 90 + 0.4/lvl | 2 | None | — | none (=ALL) | enemy | ENEMY DEBUFF |  |  |  |
| Obsidian Tomb | 2 | debuffprevent | static | 100 | 90 + 0.4/lvl | 1 | None | — | none (=ALL) | self | SELF BUFF |  |  |  |
| Midnight Verdict | 0 | pierce | formula | 66 | 56 + 0.4/lvl | 0 | Shadow | Highest / Highest | ENEMIES | enemy | ENEMY DEBUFF |  |  |  |
| Midnight Verdict | 1 | stun | static | 100 | 90 + 0.4/lvl | 2 | None | — | ENEMIES | enemy | ENEMY DEBUFF |  |  |  |
| Corona Devourer Palm | 0 | damage | formula | 45 | 35 + 0.4/lvl | 0 | Shadow | Highest / Highest | none (=ALL) | enemy | DAMAGE | ✓ |  | **yes** |
| Corona Devourer Palm | 1 | recoil | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF |  |  | **yes** |
| Marrow Eclipse Mantle | 0 | absorb | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | self | SELF BUFF |  |  |  |
| Marrow Eclipse Mantle | 1 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | Highest | none (=ALL) | self | SELF BUFF | ✓ |  |  |
| Black Sun Cataract | 0 | damage | formula | 45 | 35 + 0.4/lvl | 0 | Shadow | Highest / Highest | ENEMIES | enemy | DAMAGE | ✓ |  |  |
| Black Sun Cataract | 1 | drain | static | 250 | 250 + 0/lvl | 2 | None | — | none (=ALL) | enemy | ENEMY DEBUFF |  |  | **yes** |
| Black Sun Cataract | 2 | wound | percentage | 30% | 20 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ENEMIES | enemy | ENEMY DEBUFF |  |  |  |

Stat/general filters on an element-less row are not binding at the pin: `getEfficiencyRatio` pushes `None` for an empty element list on both sides, so such a row matches every element-less damage effect of any stat type (basic attacks, non-elemental jutsu) and excludes only elemental damage of a non-listed stat type (SOURCE_MECHANICS.md §3). `Ally hazard` marks harmful rows delivered by an area method or ground target with friendly fire none/ALL: allies and the caster inside the area also receive them (checkFriendlyFire treats an absent value as ALL).

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 5 | Black Sun Cataract, Corona Devourer Palm, Godstorm Mantle: Raijin's Cage, Godstorm Mantle: Storm-God's Heart, Obsidian Tomb | DAMAGE | 40, 45, 50 | — | 0 | 5 | 0 | — |
| Increase Damage Given | 4 | Godstorm Mantle: Sky-Splitting Wall, Godstorm Mantle: Tempest, Godstorm Mantle: Thunder-Crowned Bulwark, Marrow Eclipse Mantle | SELF BUFF | 35 | — | 0 | 4 | 0 | — |
| Increase Damage Taken | 3 | Event Horizon Gate, Godstorm Mantle: Sky-Splitting Wall, Godstorm Mantle: Storm-God's Heart | ENEMY DEBUFF | 35 | — | 0 | 3 | 0 | — |
| Decrease Damage Taken | 2 | Event Horizon Gate, Godstorm Mantle: Thunder-Crowned Bulwark | SELF BUFF | 35 | — | 0 | 2 | 0 | — |
| Afterburn | 1 | Godstorm Mantle: Tempest | ENEMY DEBUFF | 35 | — | 0 | 1 | 0 | — |
| Lifesteal | 1 | Godstorm Mantle: Tempest | SELF BUFF | 40 | — | 0 | 1 | 0 | — |

Supported rows total: **16**. Unsupported tags present (no potency): absorb, buffprevent, debuffprevent, drain, move, pierce, recoil, redirection, stun, wound.

> **Ally-hazard rows (area delivery, friendly fire none/ALL):** Event Horizon Gate row 1 (increasedamagetaken, AOE_CIRCLE_SPAWN, target OTHER_USER); Corona Devourer Palm row 0 (damage, AOE_SPIRAL_SHOOT, target GROUND). Potency on these tags also raises what allies standing in the area receive; positioning, not the node, decides.

## Selector / classification audit

- Signature elements on damage/pierce rows: Shadow, Storm
- Proposed potency classification label: **Godstorm Eclipse** (bloodline-keyed extension)
- Multiple signature elements (Shadow, Storm) on damage/pierce rows; no single element isolates the kit. A bloodline-keyed classification label is required unless the user accepts one element as the classification key and documents the uncovered rows.
- Current resolver with `affectedElements=['Shadow']`: 3 of 16 supported rows match directly; 11 fall back to None; 2 carry other elements only. Exclusive under current resolver: no.
- Current resolver with `affectedElements=['Storm']`: 2 of 16 supported rows match directly; 11 fall back to None; 3 carry other elements only. Exclusive under current resolver: no.
- Census collisions on signature elements (other bloodlines carrying the element on any row): Adorable Shadow of Death [DEFER] (Shadow: 6 rows, 4 damage); Blood-Enchanted Eyes [INCLUDE] (Shadow: 6 rows, 5 damage); Blood-Enshrined Eyes [EXCLUDE] (Shadow: 3 rows, 3 damage); Blood-Enthralled Eyes [EXCLUDE] (Shadow: 6 rows, 5 damage); Extinction Herald [DEFER] (Shadow: 5 rows, 4 damage); Infernal Reaper [DEFER] (Shadow: 4 rows, 3 damage); Kusamochi: Mashumaro Executioner [DEFER] (Shadow: 3 rows, 3 damage); Lilac Seductress [DEFER] (Shadow: 3 rows, 3 damage); Night Parade of A Thousand Demons [INCLUDE] (Shadow: 2 rows, 2 damage); Oblivion Seal [INCLUDE] (Shadow: 5 rows, 4 damage); Otaku of the Dark Maiden [DEFER] (Shadow: 5 rows, 4 damage); Sacrament of Crimson Hunger [DEFER] (Shadow: 3 rows, 3 damage); Shadow Weaver [INCLUDE] (Shadow: 6 rows, 4 damage); Arashima [INCLUDE] (Storm: 3 rows, 3 damage); Shinrai Ou [INCLUDE] (Storm: 6 rows, 4 damage); Stormboat Willy [DEFER] (Storm: 3 rows, 3 damage)
- Normal-jutsu collision: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). Whether NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu carry this element needs a read-only public jutsu listing capture requested from dauntless.
- Item-gated jutsu: Black Sun Cataract, Corona Devourer Palm, Event Horizon Gate, Godstorm Mantle: Heavenbreaker Verdict, Godstorm Mantle: Raijin's Cage, Godstorm Mantle: Sky-Splitting Wall, Godstorm Mantle: Storm-God's Heart, Godstorm Mantle: Tempest, Godstorm Mantle: Thunder-Crowned Bulwark, Marrow Eclipse Mantle, Midnight Verdict, Obsidian Tomb
- Mode-restricted jutsu: none
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

## Afterburn and downstream notes

Application rows: Godstorm Mantle: Tempest row 0 (35%, 2 rounds).
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

