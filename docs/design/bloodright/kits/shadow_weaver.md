# Shadow Weaver — Bloodright kit dossier

**Review id:** BR-063 · **Bloodline id:** `d0WYPbbsVx7Y_i0fddwxc` · **Rank:** A · **Stat classification:** Bukijutsu · **Traits:** Sustained Dps · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 25 | 0.15 | INHERIT | Fire, Lightning, Shadow, None | — | percentage |
| decreasedamagetaken | 15 | 0 | INHERIT | Lightning | — | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Shadow Domain | public | BLOODLINE | A | GROUND | 4 | 60 | 7 | AOE_SPIRAL_SHOOT | — | BOTH | 2 / 3 |
| Shadow Severance | public | BLOODLINE | A | OTHER_USER | 4 | 60 | 7 | SINGLE | — | BOTH | 2 / 3 |
| Shadow Step | public | BLOODLINE | B | EMPTY_GROUND | 5 | 60 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 2 / 3 |
| Shadow Shell | public | BLOODLINE | C | SELF | 0 | 40 | 7 | SINGLE | — | BOTH | 2 / 3 |
| Shadow Dance | public | BLOODLINE | B | OTHER_USER | 4 | 60 | 7 | SINGLE | — | BOTH | 1 / 2 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Stat / general filter | Friendly fire | Recipient | Role | ✓ | Adverse | Ally hazard | Enemy hazard |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|---|---|---|---|
| Shadow Domain | 0 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | Fire, Lightning, None, Shadow | — | none (=ALL) | self | SELF BUFF | ✓ |  |  |  |
| Shadow Domain | 1 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Shadow | Bukijutsu / Speed, Strength | ENEMIES | enemy | DAMAGE | ✓ |  |  |  |
| Shadow Domain | 2 | clearprevent | static | 100 | 90 + 0.4/lvl | 1 | None | — | none (=ALL) | self | SELF BUFF |  |  |  |  |
| Shadow Severance | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Shadow | Bukijutsu / Speed, Strength | ENEMIES | enemy | DAMAGE | ✓ |  |  |  |
| Shadow Severance | 1 | decreasedamagegiven | percentage | 30% | 20 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | enemy | ENEMY DEBUFF | ✓ |  |  |  |
| Shadow Severance | 2 | debuffprevent | static | 100 | 90 + 0.4/lvl | 1 | None | — | none (=ALL) | self | SELF BUFF |  |  |  |  |
| Shadow Step | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Shadow | Bukijutsu / Speed, Strength | ENEMIES | enemy | DAMAGE | ✓ |  |  |  |
| Shadow Step | 1 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | Fire, Lightning, None, Shadow | — | none (=ALL) | self | SELF BUFF | ✓ |  |  |  |
| Shadow Step | 2 | move | static | 1 | 1 + 0/lvl | 0 | None | — | none (=ALL) | self | SELF BUFF |  |  |  | **yes** |
| Shadow Shell | 0 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu | none (=ALL) | self | SELF BUFF | ✓ |  |  |  |
| Shadow Shell | 1 | decreasedamagetaken | percentage | 35% | 25 + 0.4/lvl | 2 | None | Bukijutsu, Genjutsu, Ninjutsu, Taijutsu | none (=ALL) | self | SELF BUFF | ✓ |  |  |  |
| Shadow Shell | 2 | visual | static | 1 | 1 + 0/lvl | 0 | None | — | none (=ALL) | self | SELF DEBUFF |  | **yes** |  |  |
| Shadow Dance | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Shadow | Bukijutsu / Speed, Strength | ENEMIES | enemy | DAMAGE | ✓ |  |  |  |
| Shadow Dance | 1 | copy | percentage | 100% | 90 + 0.4/lvl | 2 | None | — | none (=ALL) | enemy | ENEMY DEBUFF |  |  |  |  |

Stat/general filters on an element-less row are not binding at the pin: `getEfficiencyRatio` pushes `None` for an empty element list on both sides, so such a row matches every element-less damage effect of any stat type (basic attacks, non-elemental jutsu) and excludes only elemental damage of a non-listed stat type (SOURCE_MECHANICS.md §3). `Ally hazard` marks harmful INHERIT rows delivered by an area method or ground target with friendly fire none/ALL: allies inside the area also receive them (checkFriendlyFire treats an absent value as ALL); on OTHER_USER-target area jutsu the caster is never a target, on GROUND/EMPTY_GROUND spawns the ground effect is re-applied each round to whoever stands on the tiles, the caster included. `Enemy hazard` marks positive INHERIT rows on GROUND/EMPTY_GROUND spawns with friendly fire none/ALL: enemies standing on the tiles receive the buff too. SELF-target rows on ground actions are realized on the caster at cast time (actions.ts 980-1004), not through the tiles.

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 4 | Shadow Dance, Shadow Domain, Shadow Severance, Shadow Step | DAMAGE | 40 | — | 0 | 0 | 0 | — |
| Increase Damage Given | 3 | Shadow Domain, Shadow Shell, Shadow Step | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Decrease Damage Given | 1 | Shadow Severance | ENEMY DEBUFF | 30 | — | 0 | 0 | 0 | — |
| Decrease Damage Taken | 1 | Shadow Shell | SELF BUFF | 35 | — | 0 | 0 | 0 | — |

Supported rows total: **9**. Unsupported tags present (no potency): clearprevent, copy, debuffprevent, move, visual.

## Potency classification audit (element-wide, RUL-2026-10-03-005)

- Signature elements on damage/pierce rows: Shadow
- Proposed potency classification: **Shadow** (element; status: element)
- Qualifying elements: Shadow
- Single signature element Shadow on the kit's damage/pierce rows. Potency reaches matching supported tags on every Shadow jutsu: this kit, other bloodlines' Shadow jutsu and any NORMAL/SPECIAL/EVENT/FORBIDDEN or injected Shadow jutsu. Sharing the element with other bloodlines is expected, not a collision.
- Not selectors: bloodline id or bloodline ownership; equipment / required bloodline item (castability gate only); injected-child provenance; jutsu names (examples only).
- Kit jutsu of the qualifying element by their own rows (derived, train.ts checkJutsuElements union): Shadow Domain, Shadow Severance, Shadow Step, Shadow Dance
- Kit jutsu in scope only by authored jutsu classification (no qualifying element on any row): Shadow Shell (None)
- Current resolver with `affectedElements=['Shadow']`: 6 of 9 supported rows match directly; 3 fall back to None; 0 carry other elements only. Current resolver matches each effect row's own elements (absent list -> ['None']); it has no jutsu-level classification. Rows on a qualifying jutsu that do not carry the element are unreachable today: ENGINE GAP, not a design question.
- Other captured bloodlines with jutsu of the qualifying element (expected sharing): Adorable Shadow of Death [DEFER] (Shadow: 6 rows, 4 damage); Blood-Enchanted Eyes [INCLUDE] (Shadow: 6 rows, 5 damage); Blood-Enshrined Eyes [EXCLUDE] (Shadow: 3 rows, 3 damage); Blood-Enthralled Eyes [EXCLUDE] (Shadow: 6 rows, 5 damage); Extinction Herald [DEFER] (Shadow: 5 rows, 4 damage); Godstorm Eclipse [INCLUDE] (Shadow: 4 rows, 4 damage); Infernal Reaper [DEFER] (Shadow: 4 rows, 3 damage); Kusamochi: Mashumaro Executioner [DEFER] (Shadow: 3 rows, 3 damage); Lilac Seductress [DEFER] (Shadow: 3 rows, 3 damage); Night Parade of A Thousand Demons [INCLUDE] (Shadow: 2 rows, 2 damage); Oblivion Seal [INCLUDE] (Shadow: 5 rows, 4 damage); Otaku of the Dark Maiden [DEFER] (Shadow: 5 rows, 4 damage); Sacrament of Crimson Hunger [DEFER] (Shadow: 3 rows, 3 damage)
  - Other captured bloodlines with jutsu of the qualifying element. Sharing is expected. Their bloodline jutsu are castable only by their own bloodline's owners (checkJutsuBloodline, app/src/libs/train.ts 185-188), so they do not widen what one owner can amplify; NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu of the element can.
- Off-kit coverage: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu of the qualifying element are in scope by rule; how many exist needs a read-only public jutsu listing capture.
- Item-gated jutsu (castability only, not a potency selector): none
- Mode-restricted jutsu: none
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

## Afterburn and downstream notes

No Afterburn application rows in this kit.
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

