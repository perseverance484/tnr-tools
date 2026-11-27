# The Gobblefather: go-live list

Generated 2026-11-25 from the results bundles of jobs 622 (`harvests/inbox/tnr_results_1795629671115.json`) and 623 (`harvests/inbox/tnr_results_1795631190552.json`). Every record below was created or edited **hidden**. Nothing is visible to players yet.

Order for the release sitting (director's go covers this list only): 1 fixes, 2 art wiring, 3 unhides (jutsu, then AI, then quest), 4 read-back, 5 announcement.

## 1. Before unhiding (open items)

- [ ] Rewards (planner item 21): the quest carries the sheet's placeholder rewards (18,000 exp, 15,000 ryo, 600 prestige, 500 tokens, 600 clan points). Confirm or replace.
- [ ] Badge 'Family Business': not built (badges are public on create, so art first), then add to `reward_badges`.
- [ ] Golden Feathered Ring (approved) and the Cane reskin: not built yet; separate job after art.
- [ ] Art: 21 shots in `state/gobblefather/art_shotlist.md` (scenes, characters, avatars, jutsu icons, quest icon, badge, ring, cane). Quest scenes are blank and every record uses the default image until then.
- [ ] Balance check: bosses are level 75 with masteries 300/150 unscaled; offline sims not run yet. Planner: tone the Final Feast down if it is too strong on launch day.

## 2. Hidden records to unhide

| Kind | Name | Live id | State |
|---|---|---|---|
| jutsu | Drumstick Release: Concrete Clobber | `Xiv4MSyDT2fy56Rs4LBpr` | VERIFIED |
| jutsu | Feather Barrage: Collection Notice | `wlHq-naZSPHTQfx8fJK9V` | VERIFIED |
| jutsu | Family Business | `0oEnb7dKvwPwte0nIU3Pj` | VERIFIED |
| jutsu | Wing Guard: Protection Payment | `O01G8frAlRC_sJvggollZ` | VERIFIED |
| jutsu | Back-Alley Counter | `X_Y-VW8eOw6LB-zrP1iZm` | VERIFIED |
| jutsu | Double Drumstick Beatdown | `XqDXmnF1iwAGoo3xmEHVv` | VERIFIED |
| jutsu | Feather Tax: Mandatory Collection | `rHCyIsqExTYQVgdmw_X3R` | VERIFIED |
| jutsu | Compound Interest | `5vHOTxBXThWnvQiXaihcd` | VERIFIED |
| jutsu | Collection Day | `K8Atx3h1KXEukkNGvN17R` | VERIFIED |
| jutsu | Thanksgiving Massacre: Flying Drumsticks | `isBBnS99pv4CmRnUjYTGA` | VERIFIED |
| jutsu | The Final Feast | `cpPFpXVNZywgmWbVggYq2` | VERIFIED |
| jutsu | Omertà: Code of Feathers | `F-b2NkVCxMlUG6u4ziogy` | VERIFIED |
| ai | Feathered Enforcer | `a9kRi7XLrMumWKuJf5jmp` | CONFIRMED |
| ai | Corn Collector | `Top0jA3EnHBOgiLYBwq4Y` | CONFIRMED |
| ai | Feathered Accountant | `lhmZ6K62JU1hxkn7aqqQT` | CONFIRMED |
| ai | Tony Drumstick | `lnclpAtgZnorHcnTBSJK0` | CONFIRMED |
| ai | Vinny Drumstick | `Z3qFXS6MuRweTBVZ2UvnV` | CONFIRMED |
| ai | Don Giblet | `FWHBYtSrHszv8G0cRwUKy` | CONFIRMED |
| ai | The Gobblefather | `dTN0I8f8sfBep45hc7F4G` | CONFIRMED |
| quest | The Gobblefather | `goJkx-CPJSYvJO71s6CpE` | VERIFIED |

Unhide in that order: the 12 jutsu, then the 7 AI, then the quest. The quest `startsAt` is 2026-11-26 and `endsAt` 2026-12-03, so it stays closed outside that week even once unhidden.

## 3. Read-back after the unhide

- [ ] Each jutsu `hidden:false`; each AI `hidden:false` and still `equipped:true` on every jutsu (law 18 check).
- [ ] Quest: hidden false, questType event, maxAttempts -1, maxCompletes 1, requiredLevel 75.
- [ ] One test fight per stage on the director's say-so.

## Done 2026-11-27

Live quest: `a0HxwG_yOapsv0g_oFvYD` (clone; original `goJkx-CPJSYvJO71s6CpE` deleted). Rewards: Single Major Event package + Family Business badge + Golden Feathered Ring + Gobblefather's Cane Token. Ring, token and the 11 scene assets unhidden. The 12 boss jutsu and 7 AI stay hidden on purpose (they fight hidden; unhiding equipped jutsu risks law 18). Record: `harvests/inbox/tnr_results_gobblefather_golive_20261127.json`.

## Genin version, 2026-11-27 (job 632)

`baWIzLpcJPnoTdPqjfVzn` The Gobblefather (Genin): live, levels 1-29, adds dropped (guard fight 1+1), +40% damage given / 40% damage taken reduction in every fight. Main quest `a0HxwG_yOapsv0g_oFvYD` now level 30+. Same rewards on both.
