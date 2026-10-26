# Lastlight (Crownhold jutsu)

**Status:** spec approved by the director 2026-10-25 (RUL-2026-10-25-006). Costs, line length and required rank follow
the proposals below unless changed; art not started; not built.

**Concept:** Crownhold's final signal turned into a weapon: a skyglass beam that burns through a line of enemies.
Earned once, as a take-once pick on Crownhold's completion (RUL-2026-10-25-002).

| Field | Value |
|---|---|
| Name | Lastlight |
| `jutsuType` | EVENT |
| `battleUsageType` | **PVE** (usable only in quest-type battles: QUEST, which includes dungeons and Battle Pyramids, plus HUNTING, RANDOM_ENCOUNTER, RAID, OVERWORLD; not in PvP, ranked, sparring, clan, Arena, Kage AI or training: `QuestBattleTypes`, `libs/combat/actions.ts`) |
| Element | none |
| `method` | AOE_LINE_SHOOT, length 5 (proposal) |
| Cooldown | **8** |
| Required rank | Jonin (proposal) |
| Costs | the standard for its rank (to fill from the pool conventions when the manifest is drafted) |

**Effects** (power at level L = power + L × powerPerLevel; `libs/combat/power.ts`). Director: scaling 0.4 per level,
10 taken off each value so it reaches the target at max level (level 25, `JUTSU_TRAIN_LEVEL_CAP`):

| Effect | power | powerPerLevel | At level 25 | Rounds |
|---|---|---|---|---|
| damage (formula; `statTypes` and `generalTypes` both `["Highest"]`, law 4) | 40 | 0.4 | **50** | instant |
| wound (formula, same types; rides the damage on the same action) | 20 | 0.4 | **30%** | **2** |
| decreaseheal (heal cut) | 30 | 0.4 | **40%** | **3** |

**Elite Jonin:** they can train jutsu to level 30 (`ELITE_JONIN_JUTSU_LEVEL_CAP`), which takes Lastlight to 52 damage /
32% wound / 42% heal cut. Director 2026-10-25: the level-25 targets stand ("its fine. Thats a worry for another day").

**Build route (director, 2026-10-25):** Lastlight is **suggested first** as a new record (Forge suggest-mode create,
`fable/forge-suggest-create`, RUL-2026-10-25-001), hidden. The Crownhold pick that offers it is added **later**, by a
separate manifest that references the jutsu's live id once the suggestion is approved (a manifest cannot reference a
record it only suggests).

**Art:** jutsu icon and a beam animation through isolated sessions (not started).
