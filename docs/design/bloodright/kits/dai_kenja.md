# Dai Kenja — Bloodright kit dossier

**Review id:** BR-021 · **Bloodline id:** `Dqqw3zcIGDserD-qEE9QW` · **Rank:** D · **Stat classification:** Ninjutsu · **Traits:** — · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 15 | 0 | INHERIT | — | Ninjutsu | percentage |
| increasedamagetaken | 5 | 0 | INHERIT | — | Taijutsu, Bukijutsu | percentage |
| decreasepoolcost | 50 | 0 | INHERIT | — | — | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Overloaded Impact | public | BLOODLINE | B | OTHER_USER | 4 | 60 | 6 | SINGLE | — | BOTH | 3 / 3 |
| Chakra Overload | public | BLOODLINE | C | OTHER_USER | 4 | 40 | 6 | SINGLE | — | BOTH | 2 / 3 |
| Chakra Cannon | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 1 / 2 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Stat / general filter | Friendly fire | Recipient | Role | ✓ | Adverse | Ally hazard |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|---|---|---|
| Overloaded Impact | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | None | Ninjutsu / Intelligence, Willpower | ALL | enemy | DAMAGE | ✓ |  |  |
| Overloaded Impact | 1 | increasedamagegiven | percentage | 30% | 20 + 0.4/lvl | 2 | None | Ninjutsu | ALL | self | SELF BUFF | ✓ |  |  |
| Overloaded Impact | 2 | increasedamagetaken | percentage | 25% | 20 + 0.2/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ALL | self | SELF DEBUFF | ✓ | **yes** |  |
| Chakra Overload | 0 | decreasedamagegiven | percentage | 25% | 15 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ENEMIES | enemy | ENEMY DEBUFF | ✓ |  |  |
| Chakra Overload | 1 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Ninjutsu | ALL | enemy | ENEMY DEBUFF | ✓ |  |  |
| Chakra Overload | 2 | increasepoolcost | percentage | 100% | 80 + 0.8/lvl | 2 | None | — | ALL | enemy | ENEMY DEBUFF |  |  |  |
| Chakra Cannon | 0 | pierce | formula | 58 | 48 + 0.4/lvl | 0 | None | Ninjutsu / Intelligence, Willpower | ALL | enemy | ENEMY DEBUFF |  |  | **yes** |
| Chakra Cannon | 1 | decreasedamagegiven | percentage | 30% | 20 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ALL | enemy | ENEMY DEBUFF | ✓ |  | **yes** |

Stat/general filters on an element-less row are not binding at the pin: `getEfficiencyRatio` pushes `None` for an empty element list on both sides, so such a row matches every element-less damage effect of any stat type (basic attacks, non-elemental jutsu) and excludes only elemental damage of a non-listed stat type (SOURCE_MECHANICS.md §3). `Ally hazard` marks harmful rows delivered by an area method or ground target with friendly fire none/ALL: allies and the caster inside the area also receive them (checkFriendlyFire treats an absent value as ALL).

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 1 | Overloaded Impact | DAMAGE | 40 | — | 0 | 0 | 0 | — |
| Increase Damage Given | 1 | Overloaded Impact | SELF BUFF | 30 | — | 0 | 0 | 0 | — |
| Decrease Damage Given | 2 | Chakra Cannon, Chakra Overload | ENEMY DEBUFF | 25, 30 | — | 0 | 0 | 0 | — |
| Increase Damage Taken | 2 | Chakra Overload, Overloaded Impact | ENEMY DEBUFF, SELF DEBUFF | 25, 35 | — | 0 | 0 | 0 | Overloaded Impact#2 |

Supported rows total: **6**. Unsupported tags present (no potency): increasepoolcost, pierce.

> **Ally-hazard rows (area delivery, friendly fire none/ALL):** Chakra Cannon row 1 (decreasedamagegiven, AOE_CIRCLE_SPAWN, target OTHER_USER). Potency on these tags also raises what allies standing in the area receive; positioning, not the node, decides.

> **Adverse rows:** Overloaded Impact row 2 (increasedamagetaken on self, SELF DEBUFF). A potency node on that tag also raises these rows; the resolver cannot exclude a row by jutsu.

## Selector / classification audit

- Signature elements on damage/pierce rows: none
- Proposed potency classification label: **Dai Kenja** (bloodline-keyed extension)
- No non-None element on any damage/pierce row. No existing element can isolate this kit; a bloodline-keyed classification label (extension of the proposed resolver change) is required. Targeting 'None' would reach every non-elemental row in the game.
- Current resolver with `affectedElements=['None']`: 6 of 6 supported rows match directly; 6 fall back to None; 0 carry other elements only. Exclusive under current resolver: no.
- Census collisions on signature elements: none among the 95 captured bloodline kits.
- Normal-jutsu collision: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). Whether NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu carry this element needs a read-only public jutsu listing capture requested from dauntless.
- Item-gated jutsu: none
- Mode-restricted jutsu: none
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

## Afterburn and downstream notes

No Afterburn application rows in this kit.
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

