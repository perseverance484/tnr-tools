# AP run 2: loss analysis (fight 6 vs Shisui, fight 8 vs Selaphiel)

Method: no plan was recorded live, so each round's planner input was rebuilt from `fights/live_states/<bid>.full.jsonl.gz` and planner2 was run on it offline (scratch script, no game calls). Offline picks match most live picks. Where they differ, the opponent models have since learned from these fights (Selaphiel now "1 logged fight"), so offline is not an exact replay.

## Where the bad decisions came from

| # | Defect | Evidence | Effect |
|---|---|---|---|
| 1 | **Planner kit ≠ game loadout.** cd_plan `pvp1` lists Thunder's Judgement; the game's "PvP" loadout (the one equipment selects) has 15 jutsu without it (Limit Breaker took the slot). | `jutsu.getLoadouts` read 19:50Z; thunders refused "Action not valid anymore" 6x, landed 0x in all 8 fights. | Each fight opened on a refused line. Thunders was then banned and the turn replanned under time pressure. Fight 2 R1 hit "planner failed: out of time" and fired the fallback Defensive Stance. |
| 2 | **Kunai never priced by the race in planner2.** `value_model.kunai_cost` is only called by turn.py; planner2 (default since PR 124) left `KUNAI_COST` at "leaning" (350). | Selaphiel R9 lines: kunai lines carry "reserve 350" at 1904 v 2434 HP. | Basic attack chosen over kunai in close rounds. |
| 3 | **DESPERATION ranked by the wrong number.** When every line scored below -0.6 DEATH it sorted by his HP loss *after his reply*, so his lifesteal/absorb heals counted against me; a stance that cut his hit read as "damage". It also ignored survival odds. | Selaphiel R9 with thunders banned: old code returns rebirth + basic + Defensive Stance (exactly what fired), ranked over rebirth + aetherion. | Final rounds spent on stance/jewel/weapon + kunai instead of the biggest hit. New code: R9 rebirth + aetherion, R10 Shrapnel (60 AP) + stance. |
| 4 | **Setup over payoff** (weights, not a code bug). | Shisui R2–R7 and Selaphiel R3–R7: buffs, defence, Clear/Cleanse, ~0–240 damage a round while he stacked x2–x4.6 damage given and stunned me (-20 AP) most rounds. Even fixed, Shisui R10 offline picks sealnull + jewel + panacea at 2698 v 2311. | Rounds lost to setup that is never cashed. `mypot` 0.9 / `die` 2500 / `race` 200 are director hand-set weights: not changed here. |

Also found: postmortem.py crashes on both losses (`IndexError`, postmortem.py:169), so no review was written; and nothing kept the plans (fixed: item 5 below).

## Fixes made (commit 8f06b590 on claude/ap-live-run-dauntless-goqgbz)
1. `cd_plan.LOADOUTS["pvp1"]` = the game's PvP loadout (no thunders); `pvp1_thunders` keeps the old kit for replays of older fights; `PVP1_JUTSU_IDS` pins the game's ids.
2. planner2 prices the kunai each turn with `kunai_cost` (close race 0, leaning 350, AFK / sure win / likely loss 5500), as turn.py does.
3. DESPERATION: damage = what my turn takes off him (before his reply); ranked among lines whose chance of me being dead by my next turn (his reply now + his next turn) is within 0.10 of the best.
4. (planner output) a `dead` column: that combined death chance per line.
5. Every planner run is kept in `fights/live_states/<bid>.plans.jsonl.gz` (planner, time, bans, state line, top candidates with terms, FIRE) and pushed with the fight log by player/keep.py.

## Simulator (fightsim matrix, 2 fights per opponent x turn order, offline)
| Kit | Selaphiel P1 | HikuroHatake P1 | All 140 |
|---|---|---|---|
| today's game loadout (no thunders) | 0% | 50% | 96% |
| thunders in place of Limit Breaker | 100% | 100% | 99% |

Planner fixes alone, same kit: equal win rate, equal or better HP (Selaphiel/Shisui, 16 fights each way). The simulator is optimistic (it wins Shisui 100%; we lost live), so treat these as direction, not odds.

## Gates
- `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .`: 672 run, 1 failure, the same as before any change (`test_chaos.PlannerOutOfTime.test_the_real_planner_is_cut_off_and_returns`: the planner finishes inside its 0.6 s cut on this machine).
- tools: test_loss_fixes, test_planner2 (4000/4000 parity), test_critique, test_nearkill, test_integration pass; test_pilot fails exactly as before the change (replays fight data the run updated).
- The new tests fail on the old code.
