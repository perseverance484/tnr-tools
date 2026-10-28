# Skyglass Wreck: encounter design (draft for director review)

Status: DRAFT (roles, behaviour and floor arcs). Every number is set and checked in the offline harness
(`harness/skyglass_wreck_sim/`, branch `fable/skyglass-wreck-sim`) against RUL-2026-10-26-006 / -007 before any live edit.
Calibration: live damage settings (director, 2026-10-28: curve 2, gen_weight 1, advantage_min 0; the rest match code
defaults) and the solo anchor "good level-100 players beat The Captain solo in 8-10 rounds; a tough fight".

## Principles

1. **Every enemy has one job players can read and answer.** No enemy is just a health pool with a big hit.
2. **Each floor teaches one idea; the boss floor combines them.**
3. **One wave per floor, two at most.** Pools refill only between floors, a wave spawns on the far side (1-2 rounds of
   walking), and a floor battle's round counter is shared by its waves: one-wave floors keep openers (`round_lower_than`)
   working and keep each floor to about 4-5 rounds.
4. **Dungeon-only copies.** The live crew also fight in the hunts and quests; the dungeon gets its own records (an
   endgame set and a level-50 set), so tuning here never moves the hunts.
5. **Threat from mechanics, not stacked damage.** The live crew carry +350-470% damage given; the copies trade most of
   that for behaviour (focus fire, protection, telegraphed bursts).

## Rule vocabulary available (validators/ai.ts)

Targets: CLOSEST_OPPONENT, RANDOM_OPPONENT, LOWEST_HEALTH_OPPONENT, HIGHEST_MAX_HEALTH_OPPONENT, HIGHEST/LOWEST_ENMITY_OPPONENT,
CLOSEST_ALLY, RANDOM_ALLY, LOWEST_MAX_HEALTH_ALLY, HIGHEST_MAX_HEALTH_ALLY, SELF, empty-ground targets, barrier targets.
Conditions: health_below (self), distance_lower/higher_than (to the rule's target), player_within_range, round_lower/greater_than,
specific_round, has_effect (self), target_has_effect. Actions: specific/random/highest-power jutsu or item, combo, move, end turn.
Not available: "an ally is below X% health" and "I do not have effect X"; designs avoid needing them.

## Roles

| Enemy | Role | Behaviour players learn |
|---|---|---|
| Deck Warden | Line holder | Closes in and pins the closest player (root/snare), then grinds. Easy to kill; punishes standing still. |
| Seal Charge | Fuse | Walks at the nearest player and detonates on a fixed round of the floor. Kill it or step away. |
| Core Canister | Area denial | Plants itself; erupts around itself on a fixed rhythm. Fight away from it. |
| Core Horror | Bruiser | Slow; huge hits on whoever is closest; hits harder under 50% health. Kite it. |
| Wayfinder | Controller | Keeps distance, displaces and slows players, marks a target that the rest focus. |
| Arsenal Keeper | Artillery | Stays back; long-range volleys; arms Seal Charges (wave pairing). Reach him first. |
| Skyglass Sentinel | Guardian | Shields or buffs the closest ally every few rounds; taunts. Kill order matters. |
| First Blade | Assassin | Ignores the front line and hunts the LOWEST_HEALTH_OPPONENT; burst on low targets. Protect the weak. |
| Oathkeeper | Duelist | Debuffs (seal/disarm-style) whoever has the highest enmity; punishes the party's main damage dealer. |
| The Captain | Mini-boss | Command buffs on allies, a heavy combo at range 5; mid-fight surge at 50%. |
| Sealwright | Support | Seals and slows players, cleanses/heals allies (via ally targets); kill first or the fight drags. |
| Crowned Captain | Final boss | Three phases by health (100-60 / 60-30 / under 30): duelist, then calls hazards, then a desperate burst with Final-Stand-style protection. |

## Endgame floor arcs (level 100, 15-20 min, few wipes)

| Floor | Idea | Wave (single wave unless noted) |
|---|---|---|
| 1 | Movement matters | Deck Warden x2 + Seal Charge |
| 2 | Reach the back line | Arsenal Keeper + Deck Warden + Seal Charge |
| 3 | Kill order | Skyglass Sentinel + First Blade |
| 4 (mini-boss) | Protect your damage dealer | The Captain + Oathkeeper |
| 5 (boss) | Everything at once | Crowned Captain + Sealwright + 2 Core Canisters, the Canisters dormant until a fixed round (a later wave cannot join mid-fight: waves spawn only after the previous one is dead) |

Floors 1-4 aim for ~4 rounds each, the boss floor ~8-9: about 25 rounds, ~19 minutes at 15 s per player turn.

## Level 40-60 version (10-15 min)

Same arcs with level-50 copies and lighter kits: floors 1-4 at two enemies, the boss floor without Sealwright; the
Crowned Captain keeps two phases. Target ~18-20 rounds. Loot: entry tier only (RUL-2026-10-26-007).

## Harness acceptance checks (per version)

- Average party: full clear in the target minutes at 15 s per turn; about 1 run in 5 wipes once; no floor wipes the party
  more than 1 run in 10.
- Every enemy's signature rule fires in at least 70% of fights it appears in; no enemy spends more than 25% of its
  actions idle or walking after round 2.
- Top damage share per floor matches the floor's idea (e.g. First Blade's damage lands on the lowest-health player).

## Open (director)

Role assignments and floor ideas above; the boss's phase moves; whether hazards (Seal Charge, Core Canister) stay in the
easy version.
