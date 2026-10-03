# Crystal Essence — Bloodright kit dossier

**Review id:** BR-020 · **Bloodline id:** `ssevlOGQ4JjPn2sHZtq0c` · **Rank:** A · **Stat classification:** Ninjutsu · **Traits:** Defensive, Sustained Damage · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 25 | 0.15 | INHERIT | Fire, Earth, Crystal, None | — | percentage |
| decreasedamagetaken | 15 | 0 | INHERIT | Earth | — | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Summoning: Jade | public | BLOODLINE | A | EMPTY_GROUND | 3 | 70 | 10 | SINGLE | — | PVP | 0 / 1 |
| Kōsai Shippū | public | BLOODLINE | D | OTHER_USER | 4 | 60 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 2 / 2 |
| Prism | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | SINGLE | — | BOTH | 1 / 2 |
| Crystal Sphere | public | BLOODLINE | C | OTHER_USER | 4 | 40 | 7 | SINGLE | — | BOTH | 2 / 2 |
| Crystal Cave | public | BLOODLINE | B | OTHER_USER | 4 | 60 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 3 / 3 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Stat / general filter | Friendly fire | Recipient | Role | ✓ | Adverse | Ally hazard | Enemy hazard |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|---|---|---|---|
| Summoning: Jade | 0 | summon | percentage | 60% | 50 + 0.4/lvl | 4 | None | — | ALL | self | SELF BUFF |  |  |  | **yes** |
| Kōsai Shippū | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Crystal | Ninjutsu / Intelligence, Willpower | ENEMIES | enemy | DAMAGE | ✓ |  |  |  |
| Kōsai Shippū | 1 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | Crystal, Earth, Fire, None | Ninjutsu | none (=ALL) | self | SELF BUFF | ✓ |  |  |  |
| Prism | 0 | damage | formula | 50 | 40 + 0.4/lvl | 0 | Crystal | Ninjutsu / Intelligence, Willpower | ALL | enemy | DAMAGE | ✓ |  |  |  |
| Prism | 1 | wound | percentage | 25% | 15 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF |  |  |  |  |
| Crystal Sphere | 0 | decreasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | ALL | self | SELF BUFF | ✓ |  |  |  |
| Crystal Sphere | 1 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Ninjutsu | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  |  |  |
| Crystal Cave | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Crystal | Ninjutsu / Intelligence, Willpower | ENEMIES | enemy | DAMAGE | ✓ |  |  |  |
| Crystal Cave | 1 | increasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | Crystal, Earth, Fire, None | — | ENEMIES | enemy | ENEMY DEBUFF | ✓ |  |  |  |
| Crystal Cave | 2 | reflect | percentage | 40% | 30 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | self | SELF BUFF | ✓ |  |  |  |

Stat/general filters on an element-less row are not binding at the pin: `getEfficiencyRatio` pushes `None` for an empty element list on both sides, so such a row matches every element-less damage effect of any stat type (basic attacks, non-elemental jutsu) and excludes only elemental damage of a non-listed stat type (SOURCE_MECHANICS.md §3). `Ally hazard` marks harmful INHERIT rows delivered by an area method or ground target with friendly fire none/ALL: allies inside the area also receive them (checkFriendlyFire treats an absent value as ALL); on OTHER_USER-target area jutsu the caster is never a target, on GROUND/EMPTY_GROUND spawns the ground effect is re-applied each round to whoever stands on the tiles, the caster included. `Enemy hazard` marks positive INHERIT rows on GROUND/EMPTY_GROUND spawns with friendly fire none/ALL: enemies standing on the tiles receive the buff too. SELF-target rows on ground actions are realized on the caster at cast time (actions.ts 980-1004), not through the tiles.

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 3 | Crystal Cave, Kōsai Shippū, Prism | DAMAGE | 40, 50 | — | 0 | 0 | 0 | — |
| Increase Damage Given | 1 | Kōsai Shippū | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Increase Damage Taken | 2 | Crystal Cave, Crystal Sphere | ENEMY DEBUFF | 35 | — | 0 | 0 | 0 | — |
| Decrease Damage Taken | 1 | Crystal Sphere | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Reflect | 1 | Crystal Cave | SELF BUFF | 40 | — | 0 | 0 | 0 | — |

Supported rows total: **8**. Unsupported tags present (no potency): summon, wound.

## Potency classification audit (element-wide, RUL-2026-10-03-005)

- Signature elements on damage/pierce rows: Crystal
- Proposed potency classification: **Crystal** (element; status: element)
- Qualifying elements: Crystal
- Single signature element Crystal on the kit's damage/pierce rows. Potency reaches matching supported tags on every Crystal jutsu: this kit, other bloodlines' Crystal jutsu and any NORMAL/SPECIAL/EVENT/FORBIDDEN or injected Crystal jutsu. Sharing the element with other bloodlines is expected, not a collision.
- Not selectors: bloodline id or bloodline ownership; equipment / required bloodline item (castability gate only); injected-child provenance; jutsu names (examples only).
- Kit jutsu of the qualifying element by their own rows (derived, train.ts checkJutsuElements union): Kōsai Shippū, Prism, Crystal Cave
- Kit jutsu in scope only by authored jutsu classification (no qualifying element on any row): Summoning: Jade (None), Crystal Sphere (None)
- Current resolver with `affectedElements=['Crystal']`: 5 of 8 supported rows match directly; 3 fall back to None; 0 carry other elements only. Current resolver matches each effect row's own elements (absent list -> ['None']); it has no jutsu-level classification. Rows on a qualifying jutsu that do not carry the element are unreachable today: ENGINE GAP, not a design question.
- Other captured bloodlines with jutsu of the qualifying element (expected sharing): Sea-Maiden’s Kiss [DEFER] (Crystal: 5 rows, 3 damage)
  - Other captured bloodlines with jutsu of the qualifying element. Sharing is expected. Their bloodline jutsu are castable only by their own bloodline's owners (checkJutsuBloodline, app/src/libs/train.ts 185-188), so they do not widen what one owner can amplify; NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu of the element can.
- Off-kit coverage: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu of the qualifying element are in scope by rule; how many exist needs a read-only public jutsu listing capture.
- Item-gated jutsu (castability only, not a potency selector): none
- Mode-restricted jutsu: Summoning: Jade (PVP)
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

## Afterburn and downstream notes

No Afterburn application rows in this kit.
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

