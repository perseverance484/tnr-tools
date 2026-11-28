# Stranded rulings: sorted by recommendation (read-only pass, 2026-11-28)

**What this is.** A sort of the 66 ruling entries listed in `docs/reviews/REPO_REVIEW_2026-11-27/evidence/stranded_rulings_dedup.md`. Each entry was read in full on its branch (`git show origin/<branch>:docs/RULINGS.md`, or `docs/rulings/2026-11.md` for the November ones). Its substance was then searched for on `origin/main` @ `c0d7bd5b1`. No live requests were made and no repo files were changed. Line numbers like `2026-10.md:NNNN` point into `origin/main:docs/rulings/2026-10.md`, and the same pattern applies to the other months.

**Main ids that are free but get cited anyway.** Many of these ids have no heading on main, yet main's own files cite them as authority: `push/crownhold.gen.py`, `state/crownhold/package/**`, the Bloodright `trees/*.json`, `art/crafting_caches/README.md`, the Headless Rider handoffs and `state/headless_rider/build_fx_289.py`. When this file says **"land"** for one of those, it mainly means **fix the dangling references**. The entry should go in with an honest status line (ACTIVE / PARTLY SUPERSEDED / SUPERSEDED, plus the main id that superseded it). Do not present it as a fresh decision.

**Rules for renumbering.**
- An entry that collides with a main id needs a new id: the next free suffix for its date in `docs/rulings/<YYYY-MM>.md`.
- Add a "Formerly `RUL-…` on `<branch>`" line, so the old citations can still be traced.
- Seven ids are also reused *between branches* (two different rulings, same id): 09-15-001, 10-15-001, 10-16-001, 10-16-004, 10-20-002, 10-20-006 and 10-26-009. In each pair, the entry that main already cites keeps the id, and the other one is renumbered.
- After landing, run `python3 scripts/rulings_index.py`.

## Flag: dangling reference at main `docs/rulings/2026-10.md:2211`

RUL-2026-10-24-009 says it supersedes "the Skyglass Signal Beacon's '10% per Ghost Ship clear' source (RUL-2026-10-16-010)". **RUL-2026-10-16-010 does not exist on main.** It exists only on these branches:
- `claude/silent-bastion-authoring-69za5u`
- `chatgpt/review-silent-bastion-authoring-20261016`
- `chatgpt/review-silent-bastion-authoring-r2-20261017`

Main also cites it 18 more times in `state/crownhold/package/state/silent_bastion_authoring/` (for example `decision_docket.md:23,61-63` and `design/entry_and_rewards.json:4,34,59`).

The entry is superseded on main in three steps:
1. Its Beacon source was replaced by 2026-10.md:2211 (RUL-2026-10-24-009).
2. Its caches were dropped by 2026-10.md:2253 (RUL-2026-10-24-011).
3. The Beacon itself was renamed the Lastlight Lantern by RUL-2026-10-25-005 and RUL-2026-10-25-007 (2026-10.md:2623, :2653).

**Fix:** land RUL-2026-10-16-010 under its own id (free on main), with status SUPERSEDED (by 10-24-009, 10-24-011 and 10-25-005/-007) and the full text kept as history. See row S3.

**A related ambiguity.** Main's `state/crownhold/package/.../design/protocols.json:3,6` cites "RUL-2026-10-14-001" to mean the *Silent Bastion Medical100* ruling. On main, that id is the *isolated-art* ruling (2026-10.md:813). The package's own `decision_docket.md:38` already notes the collision. See row L6.

**Other dangling citations on main that this sort resolves:**

| Id | Cited on main at | Row |
|---|---|---|
| RUL-2026-10-26-009 | `docs/handoffs/HEADLESS_RIDER_ANIMATIONS_ART_SESSION_PROMPT.md:12`, `…_BATCH_PROMPT.md:7`, `state/headless_rider/build_fx_289.py:44` | L2 |
| RUL-2026-10-15-001 and RUL-2026-10-16-* | 2026-10.md:2236, `push/crownhold.gen.py:6` | L6–L16, A10, S1–S3 |
| RUL-2026-10-04-001..003 | `docs/design/bloodright/trees/*.json` | L18–L20 |
| RUL-2026-10-13-001..004 | `art/crafting_caches/README.md:3`, `push/96`–`98` notes | L17, L21, L22, S4 |
| RUL-2026-10-12-016 | `docs/reviews/QW*` | L5 |

---

## 1. Land (26)

| # | Branch id | Title | Branch (others) | Collides with main? | Evidence | Proposed action |
|---|---|---|---|---|---|---|
| L1 | RUL-2026-11-12-153 | AP6 simplifies the implementation of required behavior | chatgpt/ap6-simplification-clarification | **YES** (main 2026-11.md:1454 = 200k ryo carry rule) | Main `state/prompt_ai_player_overhaul.md` AP6 §2 still says "Ablate, then delete", which is the deletion-first wording this ruling replaces. The branch commit `bb86ed535` is not an ancestor of main. | Land with a new 2026-11-12 id, together with the branch's prompt and `AI_PLAYER_OVERHAUL.md` §10 edits. |
| L2 | RUL-2026-10-26-009 | Aura of Despair: restrained lantern-mist field art | chatgpt/aura-of-despair-art-lock-20261026 | no (but the branch-to-branch clash with L3) | Cited by `HEADLESS_RIDER_ANIMATIONS_BATCH_PROMPT.md:7` and `build_fx_289.py:44`. Main's `AURA_OF_DESPAIR_ANIMATION_ART_REQUEST.md:5` still reads "PROPOSAL". | Land under 10-26-009 (main cites this one). Update the request status line. |
| L3 | RUL-2026-10-26-009 | Hellfire Harvest: field animation art direction approved; Smoulder deferred | chatgpt/hellfire-harvest-art-approval-20261026 | no (branch-to-branch clash with L2) | Main's `HELLFIRE_HARVEST_ANIMATION_ART_REQUEST.md:5` reads "PROPOSAL"; §6 item 3 (Smoulder) is still open there. The FX shipped (push/289–291). | Land with a new 2026-10-26 id. Update the request status. |
| L4 | RUL-2026-10-02-002 | Bloodright Afterburn semantics and card presentation | chatgpt/bloodright-planning-handoff-20261002 (+fable/bloodright-planning-20261003) | no | The card half is on main in `docs/workflows/BLOODRIGHT_POSTERS.md:69-80` (one shared legend, the "40 EP … becomes 45 EP" and "35% … 40%" lines). The Afterburn mechanic clause (it is a debuff, and potency scales its percentage, not its duration) is not stated on main. | Land as history. Point the card part at BLOODRIGHT_POSTERS.md. |
| L5 | RUL-2026-10-12-016 | Approve Ghost Ship quest-workflow roadmap; QW-0 and QW-1 first | chatgpt/quest-workflow-skyglass-retrospective-20261012 | no | Cited as the approving ruling by `docs/handoffs/QUEST_WORKFLOW_SESSION_HANDOFF_2026-10-12.md:19`, `docs/reviews/QW0A_CONTRACT_ALIGNMENT_REPORT.md:5` and `QW1_*_REVIEW*.md`. The QW-0A/QW-1 work was done. The plan doc and the QW briefs are not on main. | Land, plus `docs/design/QUEST_CREATION_WORKFLOW_IMPROVEMENT_PLAN_2026-10-12.md` as history. |
| L6 | RUL-2026-10-14-001 | Silent Bastion protocol chosen after the fourth fight; Medical is a full heal | chatgpt/silent-bastion-content-execution-plan-20261014 (+10 SB branches) | **YES** (main 2026-10.md:813 = isolated art sessions) | Cited by `state/crownhold/package/.../design/protocols.json:3,6`. Crownhold shipped this structure: `push/crownhold.gen.py:494` sets `givePools` 100, and :198 renames "Medical Protocol" to "Healing Rite". The 50% retry checkpoint was superseded by RUL-2026-10-25-010 (2026-10.md:2699). | Land with a new 2026-10-14 id, as PARTLY SUPERSEDED. Add an alias note so the protocols.json citations resolve. |
| L7 | RUL-2026-10-15-001 | Silent Bastion starts inside the deserted facility; four full divisions selected | chatgpt/silent-bastion-node-budget-20261015 (+8) | no (branch-to-branch clash with A3) | Cited at 2026-10.md:2236 (RUL-2026-10-24-010 item 1) and `push/crownhold.gen.py:6`. Renamed Crownhold by 10-25-005 (:2623). The recovery loop was removed by 10-25-010 (:2709). Four divisions, 16–20 fights and the puzzles shipped (`crownhold.gen.py:584-585`). | Land under this id, as PARTLY SUPERSEDED. |
| L8 | RUL-2026-10-16-002 | Silent Bastion selects native-tested alt99_f4gate | chatgpt/silent-bastion-alt99-approval-20261016 (+5) | no | Cited by `state/crownhold/package/.../compiled/quest.candidate.json:8`. The shipped graph drops the recovery lane and the reset nodes (`crownhold.gen.py:424`, per RUL-2026-10-25-010). | Land, as PARTLY SUPERSEDED (its recovery topology goes, per 10-25-010). |
| L9 | RUL-2026-10-16-004 | Arakane's Extermination Order cooldown is 4 (AR1 content mitigation) | claude/silent-bastion-authoring-69za5u (+2) | no (branch-to-branch clash with A6) | Cited at `push/crownhold.gen.py:543` and `push/README.md:837`. Extermination Order was created hidden in push/271. Arakane was later retired as the D5 boss (`crownhold.gen.py:27`; RUL-2026-10-28-003/-004). | Land under this id (main cites the SB entry). Give the Bloodright-studio entry (A6) a new id only if it is ever landed. |
| L10 | RUL-2026-10-16-006 | The Grand Marshal's 12-move kit and AI priorities are ratified | claude/silent-bastion-authoring-69za5u (+2) | no | Cited at `state/crownhold/package/.../design/commanders.json:517-518` and `compiled/ai_profiles.candidate.json:1706-1707`. | Land. |
| L11 | RUL-2026-10-16-007 | Veilstep is used with its captured record (Stealth 1 round, cooldown 5) | claude/silent-bastion-authoring-69za5u (+2) | no | `state/crownhold/source_check_2026-10-25.md:21`: "RUL-2026-10-16-007 holds as authored". | Land. |
| L12 | RUL-2026-10-16-008 | Division IV Combat Protocol is Debuff Prevent 100 / 3 rounds | claude/silent-bastion-authoring-69za5u (+2) | no | Cited at `state/crownhold/package/.../design/protocols.json:79`. The protocols ship as "War Rite" (`crownhold.gen.py:498-500`). | Land. |
| L13 | RUL-2026-10-16-009 | RC1 accepted with warning copy | claude/silent-bastion-authoring-69za5u (+2) | no | Cited at `decision_docket.md:60`. The caches it concerned were dropped (2026-10.md:2253), but Crownhold still ends in a pick (1 of 4, RUL-2026-10-24-011). | Land as history. When landing, ask the director whether "claim your pick before setting out" still applies to the pick-1-of-4. |
| L14 | RUL-2026-10-16-011 | Silent Bastion combat values and written content accepted for launch | claude/silent-bastion-authoring-69za5u (+2) | no | 68 citations on main, including `push/crownhold.gen.py:33,544`. Its ladder was scaled ×5/3 by RUL-2026-10-25-013 (2026-10.md:2774). | Land, noting the 10-25-013 amendment. |
| L15 | RUL-2026-10-16-012 | Silent Bastion puzzle validator exception and accepted text exposure | claude/silent-bastion-authoring-69za5u (+2) | no | Cited at `decision_docket.md:31,70-71`. The puzzles shipped (`crownhold.gen.py:255-356`). | Land. |
| L16 | RUL-2026-10-16-013 | Extermination Order stats and Arakane weapon selections approved | claude/silent-bastion-authoring-69za5u (+2) | no | Cited at `decision_docket.md:16,72-73` and `commanders.json:816,1196`. | Land. Note that the Arakane loadout was overtaken by the D5 boss change (RUL-2026-10-28-003/-004). |
| L17 | RUL-2026-10-13-001 | Crafting caches: consumable-family scope, Bloodthorn out, names | claude/crafting-recipe-census-pln5za | no | Cited at `art/crafting_caches/README.md:3`, `push/96`/`97`/`98` notes and 2026-10.md:1990. The names Medicine Inro, Shinobi Tool Pouch and Sage's Strongbox still stand on main. Their contents were superseded by RUL-2026-10-23-005 (:1982), which says "family scope stays". | Land, as PARTLY SUPERSEDED (contents, per 10-23-005). |
| L18 | RUL-2026-10-04-001 | Blood-Enchanted Eyes Burst route re-cut (exposure into controlled Damage) | fable/bloodright-planning-20261003 | no | Cited throughout `docs/design/bloodright/trees/blood_enchanted_eyes.json` (:3, :16, :2147, :2577). The tree's node values match this ruling exactly (Opened Veins IDT 3, Rite of Exsanguination Damage 2, …). | Land. |
| L19 | RUL-2026-10-04-002 | Shakunetsu Sakura director-approved structure | fable/bloodright-planning-20261003 | no | Cited at `trees/shakunetsu_sakura.json:3,43`, and as precedent by other trees. | Land. |
| L20 | RUL-2026-10-04-003 | Arashima director-approved structure and names | fable/bloodright-planning-20261003 | no | Cited at `trees/arashima.json:3,46,1332,1704`. | Land. |
| L21 | RUL-2026-10-13-002 | Chest loot lines use 5s, 10s and 20s | claude/crafting-recipe-census-pln5za | no | Cited by range ("RUL-2026-10-13-001..004") in `art/crafting_caches/README.md:3` and the push/98 note. Main later adopted the same intent for profession chests: RUL-2026-10-31-074 item 2 (2026-10.md:4702) and `SKYGLASS_PROFESSION_CHESTS.md:22-24`. | Land as history. Cross-reference 10-31-074. |
| L22 | RUL-2026-10-13-004 | Crafting caches: two-step release, item text, push/97 validate.py exception | claude/crafting-recipe-census-pln5za | no | Cited by range, as in L21. push/97 ran (commit `88096098c`; results in `harvests/inbox/tnr_results_17919*.json`). Step B (the vault lines) was superseded by RUL-2026-10-23-005. | Land as history (a manifest-specific exception; step B superseded). |
| L23 | RUL-2026-11-04-116 | Early-game levelling spine approved (shape) | fable/early-game-sim | no | The brief `state/prompt_early_game_sim.md` is on main. `docs/design/early_game/LEVELLING_DESIGN.md` and this ruling are not. No later ruling on main contradicts it. | Land, with `LEVELLING_DESIGN.md` from `fable/early-game-sim@88b3440`. |
| L24 | RUL-2026-11-16-165 | Battle art: at most one visual tag per jutsu | fable/combat-fx-design-rules (+fable/art-skill-duelyst) | no | It quotes the director directly. `skills/producing-tnr-art/references/combat_fx.md:93` on main says only "use the existing tag or a `visual` tag", with no ceiling. Its sibling rule, RUL-2026-11-17-166 (no lingering loops on buffs), is on main. | Land the ruling. Adopting the wider Duelyst redesign stays the repo review's separate director call D11. |
| L25 | RUL-2026-11-17-165 | AI player: begin the next phases; the director's fight rules … | fable/ai-player-run2-followup (+fable/ai-player-ap4, chatgpt/review-…-20261117) | no | Main's `player/config.py:47` still has `HEAL_BELOW = 0.95`. The branch sets 1.0 ("never start a fight missing HP"). | Land, with the `player/config.py` change. |
| L26 | RUL-2026-11-17-166 | AI player: AP4 before AP3; planner changes judged by measurement; gear repaired under 25%; relay cost accepted | fable/ai-player-ap4 | **YES** (main 2026-11.md:1948 = no lingering buff loops) | Main's `state/prompt_ai_player_overhaul.md` still lists AP3 (:122) before AP4 (:130). The repair rule already matches main (`player/activities/repair.py:12`, `BELOW = 0.25`). | Land with a new 2026-11-17 id, plus the brief's §3 order change. |

## 2. Already on main (10)

| # | Branch id | Title | Branch (others) | Collides with main? | Evidence | Proposed action |
|---|---|---|---|---|---|---|
| A1 | RUL-2026-10-01-001 | Ghost Ship restorative renamed Skyglass Serum | chatgpt/ghost-ship-skyglass-art-20261001 | no | `docs/design/GHOST_SHIP_SKYGLASS_FULL_MANIFEST_ROADMAP.md:66`; RUL-2026-10-28-018 "Serum succeeds Dead Man's Draught" (2026-10.md:3357). | No landing needed. Optionally add a one-line history stub. |
| A2 | RUL-2026-10-14-002 | Jutsu icons use full-bleed imagery without a rarity plate | chatgpt/bbe-jutsu-art-studio-20261014 | no | Main RUL-2026-10-14-001 "designed backgrounds; transparency not required" (2026-10.md:813,822); `docs/design/blue_blade_eyes/JUTSU_ICON_REGISTER.md:15` (full-bleed, opaque). | None. |
| A3 | RUL-2026-10-15-001 | Labeled jutsu-icon showcase is the last bloodline Art Studio presentation stage | chatgpt/bee-jutsu-art-studio-20261014 (+houkyuken, vaporia studios) | no (branch-to-branch clash with L7) | `docs/workflows/JUTSU_ICON_SHOWCASE.md` (ACTIVE under RUL-2026-10-17-020 at 2026-10.md:929, and RUL-2026-10-19-003 at :1221). | None. If it is ever landed, renumber it (L7 keeps 10-15-001). |
| A4 | RUL-2026-10-15-002 | Showcase grid must adapt to each bloodline's actual jutsu roster | same as A3 | no | `JUTSU_ICON_SHOWCASE.md:8` requires the exact **N/N** roster. | None. |
| A5 | RUL-2026-10-02-001 | Bloodright public planning cohort approved | chatgpt/bloodright-planning-handoff-20261002 (+fable/bloodright-planning-20261003) | no | `docs/design/bloodright/trees/` on main holds 44 trees, including `godstorm_eclipse`, `night_parade_of_a_thousand_demons`, `sands_of_time` and `tetsugan`. None of the seven excluded bloodlines has a tree. | None. Optionally add a history stub. |
| A6 | RUL-2026-10-16-004 | Bloodright tier-icon art studio, universal silhouettes and approved opaque black background | chatgpt/bloodright-icon-studio-20261016 (+16) | no (branch-to-branch clash with L9) | The outcome landed: `art/bloodright/<family>/{foundation,hidden_art,advanced_art}.webp`. `art/bloodright/_other_bloodlines/README.md` records "Bloodright_87_Approved_Original_WebPs … All 87 passed `artpreflight.py --type JUTSU_ICON`", which resolves the alpha blocker the ruling names. `BLOODRIGHT_ICON_STUDIO.md` is not on main, but the workstream is finished. | No live rule needed. If kept as history, it needs a new id. |
| A7 | RUL-2026-10-17-003 | Prioritize Bloodright tier-emblem production and hidden structural skill-tree imports | chatgpt/bloodright-structural-priority-20261017 | **YES** (main 2026-10.md:878 = import the naming-pass trees) | Both priorities were carried out: main RUL-2026-10-17-003 imports the trees, and the 87 emblems are in `art/bloodright/`. | None. If kept as history, it needs a new id. |
| A8 | RUL-2026-10-17-004 | Approve geometry-locked Bloodright reskin factory, 4–6-family batch reviews, and contrasting pilot | chatgpt/bloodright-remainder-factory-plan-20261017 (+14) | **YES** (main 2026-10.md = Cosmic Ascendant/Shiroi Youso without element) | The factory's output is on main (`art/bloodright/*`, 29 families × 3). | None. If kept as history, it needs a new id. |
| A9 | RUL-2026-10-17-005 | Accept the first two Bloodright reskin-factory pilot trios | chatgpt/bloodright-factory-pilot-closeout-20261017 (+13) | no | `art/bloodright/taiyo_kami/*`; `art/bloodright/_other_bloodlines/br029_{foundation,hidden_art,advanced_art}_approved_v01_256.webp`. | None. |
| A10 | RUL-2026-10-16-003 | Silent Bastion Beacon consumed at expedition start | claude/silent-bastion-authoring-69za5u (+4) | no | Restated on main by RUL-2026-10-25-010 item 1: "The entry item is spent at start either way" (2026-10.md:2708). Also cited at `entry_and_rewards.json:34,56`. | Land a short history stub so the package citations resolve. Point it at 10-25-010. |

## 3. Superseded (15)

| # | Branch id | Title | Branch (others) | Collides with main? | Evidence | Proposed action |
|---|---|---|---|---|---|---|
| S1 | RUL-2026-10-16-001 | Silent Bastion launches the recipe-aligned cache pilot with a one-of-two completion choice | chatgpt/recipe-aligned-reward-caches-20261016 (+5) | no (branch-to-branch clash with D10) | Superseded by RUL-2026-10-24-011 (2026-10.md:2253: "Silent Bastion's Arsenal and Research ingredient caches (RUL-2026-10-16-001/-010) are dropped"). Main still cites it in `entry_and_rewards.json:4,59` and `cache_items.candidate.json:2`. | Land a SUPERSEDED stub under this id, since main cites it. |
| S2 | RUL-2026-10-16-005 | Silent Bastion recovery battles pay no battle settlement (F3 option O2) | claude/silent-bastion-authoring-69za5u (+2) | no | The recovery battles were removed by RUL-2026-10-25-010 (2026-10.md:2709). Main still cites it in `entry_and_rewards.json:126` and `economy_and_f3.md:82`. | Land a SUPERSEDED stub. |
| S3 | RUL-2026-10-16-010 | Silent Bastion completion caches, Beacon economy and run limits | claude/silent-bastion-authoring-69za5u (+2) | no | The **dangling reference at 2026-10.md:2211.** Superseded by RUL-2026-10-24-009 (:2211, the Beacon source), RUL-2026-10-24-011 (:2253, the caches), and RUL-2026-10-25-005/-007 (Beacon renamed Lastlight Lantern). | Land as SUPERSEDED, full text kept. This fixes :2211 and the 18 package citations. |
| S4 | RUL-2026-10-13-003 | Crafting caches drop from the Ghost Ship restricted vault | claude/crafting-recipe-census-pln5za | no | Superseded by RUL-2026-10-23-005 (2026-10.md:1990: "their planned `w_B2` placement (RUL-2026-10-13-003)"). The Ghost Ship quests were retired by RUL-2026-10-23-003 (:1946). | Land a SUPERSEDED stub (cited at :1990). |
| S5 | RUL-2026-10-01-002 | Approved Skyglass ship governs scene continuity | chatgpt/ghost-ship-skyglass-art-20261001 | no | The old Ghost Ship quests were retired (RUL-2026-10-23-003, :1946). Art was rebranded around the crew and ship scenes (RUL-2026-10-26-002, :2862). `icon_ghost_ship_skyglass_d.webp` is not on main. | Archive only. Do not land. |
| S6 | RUL-2026-10-01-003 | Ghost Ship crew were elite classified-project operatives | same | no | Replaced by Skyglass canon: `docs/design/SKYGLASS_STORY_BIBLE.md` (RUL-2026-10-28-003/-004 at :3052/:3070; RUL-2026-11-05-117), and crew art by RUL-2026-10-26-001/-002 (:2842/:2862). | Archive only. |
| S7 | RUL-2026-10-01-004 | Elite cursed-crew roster and visual treatments approved | same | no | Same as S6. The crew look is now RUL-2026-10-26-002 (Edo-era, anchored on the original crew). | Archive only. |
| S8 | RUL-2026-10-01-005 | Develop complete recurring chakra echoes | same | no | Absorbed into canon: the story bible's "Afterimages (also *echoes*, *impressions*)" (RUL-2026-10-28-004). | Archive only. |
| S9 | RUL-2026-10-01-006 | Critical incident and fractured crew continuity | same | no | Replaced by RUL-2026-10-28-004 (Crownhold's crown holds every afterimage) and the story bible's "Wreck (now)" and "Silence" canon. | Archive only. |
| S10 | RUL-2026-10-01-007 | Crystal-powered skyship and concise role-based narrative | same | no | Same as S9. The war-ship and its skyglass Core are defined in `SKYGLASS_STORY_BIBLE.md`. | Archive only. |
| S11 | RUL-2026-10-01-008 | Engineer the skyship before further generation | same | no | A work order for the retired Ghost Ship art phase. Overtaken by RUL-2026-10-23-003 and RUL-2026-10-26-002. | Archive only. |
| S12 | RUL-2026-10-20-006 | Ghost Ship chests: geometry reset and tier-specific center bindings | chatgpt/ghost-ship-chest-icon-art-studio-20261020 | no (branch-to-branch clash with D9) | The old Ghost Ship chests became relics (RUL-2026-10-24-024, :2489). Profession chests were redesigned as hunt drops (RUL-2026-10-28-023, :3470), and their new icons are on main (`art/skyglass_event_icons/exports/icon-*-{hunters,gatherers}-chest.webp`). | Archive only. If the director wants the studio's approval history, land it as SUPERSEDED with a new id. |
| S13 | RUL-2026-10-20-001 | Bundle ceiling for the read-only item census | chatgpt/review-elementaldamage-weapon-census-20261020 | **YES** (main 2026-10.md = adopt the contracts at 85cecae) | Budget superseded by RUL-2026-10-23-007 (:2016, 435k/105k) and later raises (latest RUL-2026-11-08-136, 490k/119k). The census runner (`forge/src/runner/census.mjs`) is not on main. | Do not land. It was renumbered on its own branch to S14. |
| S14 | RUL-2026-10-20-002 | Bundle ceiling for the read-only item census | claude/elemental-damage-weapon-census-235ynv (+2 reviews) | **YES** (main = Ghost Ship chest icons) | Same as S13. | Do not land. If the census is ever landed, record its budget under a new id. |
| S15 | RUL-2026-10-22-005 | Tooling update to TheNinjaRPG@107d7a8 (Lane A, separate review) | fable/contracts-107d7a8 | no | Main went 85cecae → 2af4b320 → 3314d122 (`state/schema_adoption_ledger_{85cecae,2af4b320,3314d122}.json`; skill data is stamped `TheNinjaRPG@3314d12`). There is no 107d7a8 ledger on main. | Do not land. Optionally add a SUPERSEDED stub. |

## 4. Never adopted (0)

No entry is clearly an unadopted draft. Every entry records a quoted director decision. The workstreams in §5 may have been abandoned, but nothing on main says so, so they are held for the director.

## 5. Director check (15)

| # | Branch id | Title | Branch (others) | Collides with main? | Evidence | Question for the director |
|---|---|---|---|---|---|---|
| D1 | RUL-2026-09-15-001 | Godstorm two-pyramid planning scope | chatgpt/godstorm-two-pyramid-plan (+godstorm-art-recovery, godstorm-source-art-pack) | no (two branch drafts share this id) | Nothing about the Godstorm release is on main. The live title was still "The Tower of Endless Night: The Marrow Vaults" in `docs/reviews/QA_LIVE_2026-10-20.findings.json:2043`. | Is the Godstorm two-pyramid release (Marrow Vaults + Stormcourt, Dawnless Crown cut) still planned? If yes, land D1–D5 (keeping only one of the two 09-15-001 drafts). If no, archive them. |
| D2 | RUL-2026-09-15-001 | Godstorm two-pyramid release scope | chatgpt/godstorm-two-pyramid-release-plan-20260915 | no | A competing draft of D1 (canonical destination `state/plan_godstorm_two_pyramid_release.md`, not the `docs/plans/` file). | Which of the two drafts is the record? |
| D3 | RUL-2026-09-15-002 | Separate Godstorm pyramids from Tower of Endless Night | as D1 | no | As D1. | As D1. |
| D4 | RUL-2026-09-15-003 | Marrow Vaults below Stormcourt in one structure | as D1 | no | As D1. | As D1. |
| D5 | RUL-2026-09-15-004 | StormCourtyard excluded from Godstorm artwork | chatgpt/godstorm-two-pyramid-plan | no | `StormCourtyard` appears on main only in `skills/producing-tnr-art/data/art_index_2026-08-26.json:3169`. | As D1. |
| D6 | RUL-2026-09-29-001 | Potency Chakra Mandala architecture approved | chatgpt/potency-chakra-mandala-design-20260929 | no | Self-superseded by D7. No Potency or Mandala design is on main. Bloodright, a per-bloodline potency tree, became the live potency system (RUL-2026-10-03-005). | Is the general Potency skill tree (Mandala, then card categories) still a planned system, or has Bloodright replaced it? If it is still planned, land D6–D8 with the design docs. If not, archive them. |
| D7 | RUL-2026-09-29-002 | Potency two-skill progression and five card-based categories | as D6 | no | As D6. | As D6. |
| D8 | RUL-2026-09-29-003 | Defer unsupported Absorb from the Potency design | as D6 | no | Also note that upstream added `absorb` to `PotencyTagTypes` at TheNinjaRPG `133e2c7` (2026-10.md:895), so this deferral's premise may be stale. | As D6. Also: should Absorb come back now that upstream supports it? |
| D9 | RUL-2026-10-16-001 | Houkyuken star-polarity shape-first icon correction | chatgpt/houkyuken-jutsu-art-studio-20261016 | no (branch-to-branch clash with S1) | Houkyuken does not appear in any jutsu-icon register on main (the starter register; 10-20-004 lists Vaporia, Bakuhatsu and Aerathiel). The jutsu icon overhaul (RUL-2026-10-23-008 and 10-24-001…005) came later. | Is the Houkyuken jutsu-icon studio still open, or was it folded into the 10-23 icon overhaul? If it is open, land it with a new id. |
| D10 | RUL-2026-10-20-002 | Living Lineages Kitsune visual-pilot locks | chatgpt/living-lineages-kitsune-workdesk-20261020 | **YES** (main = Ghost Ship chest icons) | Nothing about Living Lineages is on main. The pet work on main is the Little Horror (RUL-2026-10-29-047 and later). | Is the Living Lineages pet-evolution concept still live? If yes, land D10–D14 with new ids for 002–005 and the `docs/design/pets/LIVING_LINEAGES_*` files. If no, archive them. |
| D11 | RUL-2026-10-20-003 | Living Lineages proof sheet uses full Ember path and abbreviated three-variant comparison | as D10 | **YES** (main = starter jutsu icons) | As D10. | As D10. |
| D12 | RUL-2026-10-20-004 | Lock the Living Lineages Kitsune structural showcase SVG | as D10 | **YES** (main = Vaporia/Bakuhatsu/Aerathiel icons) | As D10. | As D10. |
| D13 | RUL-2026-10-20-005 | One-request per-lineage evolution batches for the Kitsune concept-art sheet | as D10 | **YES** (main = village bloodline scroll icons) | As D10. | As D10. |
| D14 | RUL-2026-10-20-006 | Approve reference-first Living Lineages V2 structure and populate it with exact-source Kitsune artwork | as D10 | no (branch-to-branch clash with S12) | As D10. | As D10. |
| D15 | RUL-2026-11-03-111 | Tatsumaki's Bellow V10.1 is the Premium Seichi item-icon benchmark | chatgpt/premium-seichi-item-icon-overhaul-v10 | **YES** (main 2026-11.md:365 = The Silence rides in Sayo's shadow) | The Tatsumaki's Bellow icon was produced on main: `state/art_produced.md:38` (push/471, 2026-11-05), "awaiting dauntless eye". `ITEM_ICON_OVERHAUL.md` and `premium_seichi_item_icons/` are not on main. | Is the Premium Seichi item-icon overhaul, with V10.1 as its benchmark, still a live standard? If yes, land it with a new 2026-11-03 id and its workflow docs. |

---

## Summary

| Recommendation | Count | Of which collide with a main id |
|---|---|---|
| Land (with an honest status; renumber where needed) | 26 | 3 (L1, L6, L26) |
| Already on main | 10 | 2 (A7, A8) |
| Superseded | 15 | 2 (S13, S14) |
| Never adopted | 0 | 0 |
| Director check | 15 | 5 (D10–D13, D15) |
| **Total** | **66** | **12** |

- **Silent Bastion / Crownhold:** 15 entries. Main imported the package (`state/crownhold/package/`) and built Crownhold from it, but never imported the rulings. 11 land (L6–L16), A10 goes in as a history stub, and S1–S3 go in as SUPERSEDED stubs. Only L6 needs a new id.
- **Bloodright:** the tree rulings 10-04-001..003 are cited by main's tree JSONs and should land. The tier-emblem art rulings are already carried out on main (`art/bloodright/`).
- **Skyglass Ghost Ship art, 2026-10-01:** the old fiction and art direction, superseded by the Skyglass story bible and the 10-26 rebrand. Only the Serum rename survives, and it is already on main.
- **Highest-value fixes:**
  - the dangling RUL-2026-10-16-010 (main 2026-10.md:2211);
  - RUL-2026-10-26-009 (cited by three main files);
  - the RUL-2026-10-14-001 alias in the Crownhold package;
  - L1, L25 and L26, where main's current AI-player brief and config disagree with the director's later words.
