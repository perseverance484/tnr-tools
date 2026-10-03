# Voltara Divine — Bloodright kit dossier

**Review id:** BR-091 · **Bloodline id:** `zOGMXO1nnBTEE0sAJRCuD` · **Rank:** C · **Stat classification:** Highest · **Traits:** — · **Disposition:** INCLUDE

Evidence: public kit snapshot 2026-10-01T14:58:45.422376+00:00; hidden inventory 2026-09-30. Baselines evaluated at **jutsu level 25** (power + powerPerLevel × level). Mechanics read at `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. This is a projection of captured records, not a live readback.

## Passive bloodline effects (context only; not potency targets)

| Type | Power | Per level | Target | Elements | Stat types | Calc |
|---|---:|---:|---|---|---|---|
| increasedamagegiven | 15 | 0.15 | INHERIT | Lightning | — | percentage |
| increasedamagetaken | 10 | 0 | INHERIT | Wind | — | percentage |

## Jutsu in kit

| Jutsu | Vis | Type | Rank | Target | Range | AP% | CD | Method | Item gate | Usage | Supported rows / total |
|---|---|---|---|---|---:|---:|---:|---|---|---|---|
| Voltara Blitz | public | BLOODLINE | D | EMPTY_GROUND | 4 | 60 | 7 | AOE_CIRCLE_SPAWN | — | BOTH | 1 / 3 |
| Luminous Illusion Bind | public | BLOODLINE | D | OTHER_USER | 4 | 60 | 6 | SINGLE | — | BOTH | 2 / 3 |
| Ethereal Dragon's Whispers | public | BLOODLINE | B | OTHER_USER | 3 | 60 | 7 | SINGLE | — | BOTH | 2 / 2 |

## Effect rows

Supported rows are marked ✓. `Elements (eff.)` shows the resolver's effective element list (absent → None). Recipient/role are derived from the row target, the jutsu target, friendly fire and engine polarity; **adverse** rows are ones potency would make worse for the caster.

| Jutsu | Row | Tag | Calc | Base @L | Power + per level | Rounds | Elements (eff.) | Recipient | Role | ✓ | Adverse |
|---|---:|---|---|---:|---|---:|---|---|---|---|---|
| Voltara Blitz | 0 | move | static | 1 | 1 + 0/lvl | — | None | self | SELF BUFF |  |  |
| Voltara Blitz | 1 | decreasedamagetaken | percentage | 30% | 20 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |
| Voltara Blitz | 2 | pierce | formula | 56 | 46 + 0.4/lvl | 0 | None | enemy | ENEMY DEBUFF |  |  |
| Luminous Illusion Bind | 0 | damage | formula | 40 | 30 + 0.4/lvl | 0 | Lightning | enemy | DAMAGE | ✓ |  |
| Luminous Illusion Bind | 1 | stun | static | 100 | 90 + 0.4/lvl | 2 | None | enemy | ENEMY DEBUFF |  |  |
| Luminous Illusion Bind | 2 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | Lightning | self | SELF BUFF | ✓ |  |
| Ethereal Dragon's Whispers | 0 | damage | formula | 50 | 40 + 0.4/lvl | 0 | Lightning | enemy | DAMAGE | ✓ |  |
| Ethereal Dragon's Whispers | 1 | increasedamagegiven | percentage | 35% | 25 + 0.4/lvl | 2 | None | self | SELF BUFF | ✓ |  |

## Supported-row summary by tag

| Tag | Rows | Jutsu | Roles | Bases @L | Repeated on one jutsu | Hidden | Item-gated | Mode-restricted | Adverse |
|---|---:|---|---|---|---|---:|---:|---:|---|
| Damage | 2 | Ethereal Dragon's Whispers, Luminous Illusion Bind | DAMAGE | 40, 50 | — | 0 | 0 | 0 | — |
| Increase Damage Given | 2 | Ethereal Dragon's Whispers, Luminous Illusion Bind | SELF BUFF | 35 | — | 0 | 0 | 0 | — |
| Decrease Damage Taken | 1 | Voltara Blitz | SELF BUFF | 30 | — | 0 | 0 | 0 | — |

Supported rows total: **5**. Unsupported tags present (no potency): move, pierce, stun.

## Selector / classification audit

- Signature elements on damage/pierce rows: Lightning
- Proposed potency classification label: **Voltara Divine** (bloodline-keyed extension)
- Single signature element Lightning is a basic element carried on rows of many bloodlines and ordinary jutsu; using it as the classification label would leak broadly. A bloodline-keyed classification label is required; the element is kept as the display element only.
- Current resolver with `affectedElements=['Lightning']`: 3 of 5 supported rows match directly; 2 fall back to None; 0 carry other elements only. Exclusive under current resolver: no.
- Census collisions on signature elements (other bloodlines carrying the element on any row): Adorable Shadow of Death [DEFER] (Lightning: 1 rows, 0 damage); Architect of the Hollow Script [DEFER] (Lightning: 2 rows, 0 damage); Bakuhatsu [INCLUDE] (Lightning: 1 rows, 0 damage); Blissoo [DEFER] (Lightning: 9 rows, 2 damage); Blood-Enchanted Eyes [INCLUDE] (Lightning: 1 rows, 0 damage); Blood-Enthralled Eyes [EXCLUDE] (Lightning: 1 rows, 0 damage); Extinction Herald [DEFER] (Lightning: 1 rows, 0 damage); Eyes of the Forsaken Heir [EXCLUDE] (Lightning: 3 rows, 0 damage); Eyes of the Forsaken King [INCLUDE] (Lightning: 3 rows, 0 damage); Houkyuken [INCLUDE] (Lightning: 2 rows, 0 damage); Infernal Reaper [DEFER] (Lightning: 1 rows, 0 damage); Itojinsei [INCLUDE] (Lightning: 2 rows, 0 damage); Oblivion Seal [INCLUDE] (Lightning: 1 rows, 0 damage); Otaku of the Dark Maiden [DEFER] (Lightning: 1 rows, 0 damage); Shadow Weaver [INCLUDE] (Lightning: 2 rows, 0 damage); Shinrai Ou [INCLUDE] (Lightning: 2 rows, 0 damage); Shiroi Youso [INCLUDE] (Lightning: 6 rows, 1 damage); Solar Soul [DEFER] (Lightning: 3 rows, 0 damage); Tenohira Musei [INCLUDE] (Lightning: 1 rows, 0 damage); Testing Dummy 2.0 [DEFER] (Lightning: 2 rows, 1 damage); Timeforged Enigma [DEFER] (Lightning: 2 rows, 0 damage); Traveling Sun Praiser [DEFER] (Lightning: 6 rows, 2 damage); Youso Shiroi [EXCLUDE] (Lightning: 6 rows, 1 damage); Yūhi Ryūjin (夕陽竜神) [DEFER] (Lightning: 4 rows, 1 damage)
- Normal-jutsu collision: UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows (harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu only). Whether NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu carry this element needs a read-only public jutsu listing capture requested from dauntless.
- Item-gated jutsu: none
- Mode-restricted jutsu: none
- Hidden jutsu in kit: none
- Non-BLOODLINE jutsu types in kit: none

## Afterburn and downstream notes

No Afterburn application rows in this kit.
Afterburn is an enemy debuff (tags.ts afterburn handler at the pin): while active on following rounds, every instant damage consequence the debuffed target receives (any source, pierce excluded) adds floor(damage x percent) Afterburn damage, with the cumulative Afterburn on one hit capped at 60% of that hit. Potency raises the percent, not the duration. Downstream coverage is therefore every non-pierce hit landed on the target during the debuff, including normal jutsu, weapons and allies; it is not measured by the application-row count and was not simulated.

Lifesteal and vamp share one 60%-of-pre-shield-damage leech budget per hit; Reflect and Absorb are each capped at 60% of pre-shield damage; static Heal power is ×10 HP per tick; percentage-valued tags are hard-capped at 100 by `getPower`. See `evidence/SOURCE_MECHANICS.md`.

