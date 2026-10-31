# Skyglass event: simulated playthrough review (flow)

**Date:** 2026-10-31. **Lane B review, review only:** no manifest, generator, design doc or ruling was changed.
**Repository:** `perseverance484/tnr-tools` main at `bd373bcb`. **Engine:** theninjarpg pin `3314d122`, read-only (`git archive` to a scratch folder).
**Live requests:** 0. **Credentials:** none.
**Scope:** flow only: getting stuck, wasting items, understanding mechanics, inconsistencies between records, and the economy at player level. Item description wording and drop-rate listings belong to the parallel audit (`docs/reviews/SKYGLASS_ITEM_DESCRIPTION_AUDIT.md`) and are not repeated here.

**Records walked**
- Built manifests: push/329, 342, 343, 346, 347, 348, 349, 352.
- push/339 go-live: regenerated into a scratch file from 329's real results bundle (`python3 push/skyglass_update.gen.py --golive harvests/inbox/tnr_results_1793424666625.json`, 24 items). It was moved out of `push/` and not committed.
- Live Wreck: the archived push/263.
- Not-yet-built content: `state/skyglass_build/*` (charts, haul, crownhold, hunts and library specs) and `docs/design/SKYGLASS_*.md` (loot tables, the Haul, pets, text).
- Rulings: RUL-2026-10-29-040 through RUL-2026-10-31-071.

**How claims are marked**
- **[V-src]**: verified in engine source at `3314d122`. Paths are relative to `app/src/`.
- **[V-rec]**: verified in the built records or the scratch 339.
- **[INF]**: inferred and not verified. Each one names the check that would settle it.

No live behaviour was observed.

## Summary

| Severity | Count | In built records / 339 | Not yet built | Docs / ops only |
|---|---|---|---|---|
| BLOCKER (stuck, lost item, broken) | **3** | 2 (F01 also applies to future runs) | 1 | 0 |
| MAJOR (confusing or inconsistent) | **14** | 8 | 5 | 1 |
| MINOR (polish) | **14** | 9 | 3 | 2 |

IDs run F01 to F32, with F23 withdrawn while drafting, so 31 findings. Some findings apply to built and future records at once; each is counted where its fix lands first.

The three blockers:
1. **The pending-pick trap (F01).** A player can start a chart run again while that run's previous completion pick is still unclaimed. The new isolated run then cannot complete. Inside the run the player cannot claim the old pick, so the only way out is to abandon, which loses the chart. The Lantern's text warns about this. No chart's text does.
2. **The Buried Cache is not scaled (F02).** RUL-2026-10-28-010 item 7, the loot tables and the chart's own text ("scaled to you") all say it scales to the player. The go-live record fights unscaled endgame base records, and level-45 players get this chart from the easy Wreck.
3. **Consolation rewards on a fail ending never pay (F03).** The spec puts the consolation on the fail ending: 1 Core Rot for a failed Epic run, and the chart handed back after a lost steeping. The engine never pays rewards on a `fail_quest` objective.

**Verified sound:**
- Every built quest graph (the four go-live runs, Crownhold, Wreck Sighted) and all six Haul graphs in the spec have no dead ends, no unreachable nodes and no dangling references. Every battle has a fail route.
- A draw or a flee takes the fail route, the same as a loss.
- An isolated defeat leaves the player at 1 HP and not in hospital, so a lost press-on fight still reaches its step's ending and can be claimed.
- Entry items are charged when the run starts, never at the first battle. If an item-started quest's entry items fall short, the item use is rolled back.
- Using an Epic chart before the steeping effect exists does nothing: the item has no Consume button.
- A variant token cannot be wasted: ownership and "already unlocked" are both checked before the token is spent.
- The Little Horror's Jar refuses to open into a full collection.

## Journey 1: a new level-45 player who has never seen the event

1. **Finds Wreck Sighted.** It is an `event` quest, rank D, level 1-100, one attempt [V-rec]. Event quests start only at the Admin Building (`libs/quest.ts` 3016-3040, `questStructureRoute` 3115-3130) [V-src]. Nothing tells the player to go there, so an announcement is needed.
   - Publishing is blocked until the salvager portrait exists (RUL-2026-10-31-066 item 4; push/348 note) [V-rec].
2. **Reads Wreck Sighted.** The text explains charts, the Battle Arena, carried health and chakra, and press-on. Gaps:
   - It never says **where the Wreck is**: sector 210, 15/6 (push/263). The dungeon list only shows dungeons in the player's current sector (`validators/dungeon.ts` `dungeonSectorSchema`) [V-src]. → **F07**
   - The salvager says "A chart only works while it still holds that shape. Don't sit on it." Charts never expire. → **F24**
   - It receives the Tide Chart (`H1s2IwtZ5JqgPEoJ55IVj`) [V-rec]. Its run, the Low Tide Run, is not built yet. 339 precondition 2 covers this.
3. **Runs the Tide Chart.** The item says "Bring it to the Battle Arena". The run is actually in the Battle Arena's **Battle Pyramid** tab (`app/[shell]/battlearena/page.tsx` 166-185) [V-src]. The picker shows "x/1 owned. Consumed on entry." and the isolation warning (`layout/QuestPicker.tsx` 237-250) [V-src]. → **F25**
   - Battle Pyramid runs are one at a time. A second start is refused with "Already in active battle pyramid" (`libs/quest.ts` 2929-2934) [V-src]. Nothing is lost.
   - The Low Tide Run is scaled and has no press-on room (text §2.1). The charts spec still lists a "PRESS ON (proposed)" room on this run. → **F20**
4. **Tries the Wreck.** A dungeon needs **exactly 3 players** (`server/api/routers/combat.ts` 1891-1895) [V-src]. A solo player cannot enter it at all. Wreck Sighted does say "a dungeon for three".
   - Dungeons have no level gate (`validators/dungeon.ts` has no level field) [V-src]. A level-45 player can join an endgame party and be carried, and a level-100 player can farm the easy Wreck. → **F31**
   - The easy Wreck drops the Buried Cache chart at 5% (loot tables §2; not built).
5. **Runs the Buried Cache from that drop.** **BLOCKER F02.** In 339 every Buried Cache battle has `opponent_scaled_to_user: false` and fights the base Deck Warden, Seal Charge and Skyglass Sentinel [V-rec]. Under RUL-2026-10-31-067 those base records are tuned for the endgame Wreck. A level-45 player is very likely to lose and the chart is gone.
6. **Takes a pick.** The Buried Cache pick offers a Foundry chart. The Foundry, Archive and Watch quests are `questRank` A, which needs Jonin rank or higher (`libs/train.ts` 123-139) [V-src]. The Buried Cache is rank B. If a level-45 player can still be Chunin, they are given a chart they cannot run (it is tradeable). → **F14** [INF: rank at level 45 not checked]
7. **Repeats a run while a pick is unclaimed.** **BLOCKER F01**: see Journey 2, step 6.
8. **The common loop works for a solo player.**
   - The Low Tide Run's pick offers a Watch Roster, and the Night Watch's pick offers a Tide Chart (loot tables §4a).
   - Each ending also rolls Core Rot 15% and a Buried Cache chart 10%.
   - So a solo player who always takes the chart can keep running, at the cost of the Inro or Galley Stores. This is a healthy loop.

## Journey 2: a level-100 endgame player

1. **Endgame Wreck clear.**
   - Rewards are paid only after a full clear (`server/api/routers/dungeon.ts` 433-437) [V-src].
   - Each member rolls every drop separately [V-src].
   - The Jar and the Captain's and Core Horror's variant tokens are `onlyOnce`. That is once per player per **dungeon id**, for life (`libs/dungeonRewards.ts` 29-37; `dungeon.ts` 446-452) [V-src]. → **F28**
   - Pets **do** fight in the Wreck. Dungeon floors start battles with type `"QUEST"` (`server/api/routers/dungeon.ts` ~357-378), and pets load for QUEST battles (`combat.ts` 1990-1995; `libs/combat/pets.ts` 29-30) [V-src]. The final-sim harness modelled exactly this (`engine/sim.ts` 208). RUL-2026-10-31-070's note and SKYGLASS_PETS.md say the opposite. → **F08**
2. **Rare chart runs (339).**
   - The Foundry, Archive and Watch graphs are clean [V-rec]. Every lost, drawn or fled fight goes to `f_lost` (`libs/quest.ts` 1840-1872) [V-src].
   - The ladder drops match loot tables §4a/§5 [V-rec]:
     - Foundry: Archive chart 10%, Warden token 1%, Treasury 5%.
     - Archive: Reliquary Seal 25%, Rotted Reliquary Seal 1%, Sealwright token 1%, Treasury 5% clean / 3% alarm.
     - Watch: Last Heading 25% (45% after a won dawn watch), Rotted Heading 1%, Wayfinder token 1%, Treasury 4/5/6%.
     - Each ending: Haul pages 1.5% each.
   - **Archive "break the seal"** (a guaranteed Core Rot ×2 source in loot tables §5) has no text, no generator and no node. 339 re-sends the Archive whole, so a separately built version would be overwritten. → **F15**
3. **Watch press-on.** A lost dawn watch goes through `failObjectiveId` to the step's own win ending [V-rec]. An isolated defeat clamps HP to at least 1 (`libs/combat/database.ts` 1324-1326) [V-src], so the ending can be claimed. Correct.
4. **Epic charts (Reliquary Seal, The Last Heading).**
   - Today they are CONSUMABLE with `effects: []` [V-rec]. Use is refused ("Not consumable") and no Consume button is shown (`libs/item.ts` 52-82; `items/page.tsx` 1259) [V-src]. They cannot be wasted before steeping exists.
   - The Sealed Reliquary and The Fall are not built. Their item text promises "A lost fight … leaves you 1 Core Rot". → **F03**
5. **Crownhold (349).**
   - Entry: the Lantern. Rank S, which is Jonin or higher. 82 nodes, clean graph, two fail endings [V-rec].
   - The pick: Crown's Hoard / Coffer ×3 / Crown Fragment / Lastlight / Crownbreaker badge. The badge and the jutsu grey out once owned (RUL-2026-10-29-051, `libs/rewardChoice.ts`).
   - The ending pays Treasury 6% and two independent 25% Epic-chart lines, matching RUL-2026-10-31-064 item 5 [V-rec].
   - The Lantern text and Crownhold's description warn about an unclaimed earlier pick [V-rec]. Good, but see F01.
   - The description says "Health carries" and leaves out chakra. → **F29**
6. **Repeating a run.** **BLOCKER F01.**
   - Restarting a run reuses its quest-history row. The restart does not clear `pendingRewardChoice` (`queries/quests.ts` 1573-1604; `server/api/routers/quests.ts` 3074-3100) [V-src].
   - Starting is never blocked by a pending pick (`isAvailableUserQuests`, `libs/quest.ts` 2329-2560; `assignQuestToUser` 2560-3060) [V-src].
   - At the win ending, completion requires `pendingRewardChoice IS NULL`. Otherwise the player gets "Choose your reward from the previous completion of this quest first" (`quests.ts` 3578, 3635, 1480; `libs/rewardChoice.ts` 360) [V-src].
   - `quests.claimRewardChoice` is not on the isolated-run allow-list (`libs/questRun.ts` 58-71; `server/api/trpc.ts` 316-329) [V-src]. The client also forces the player back to `/combat` (`layout/PyramidRunBoundary.tsx` 16-22) [V-src].
   - So the only way out is to abandon. The chart was spent at entry and anything won in the run is lost.
7. **Week after week: lifetime caps.** Every Battle Pyramid run in 339/349 has `maxAttempts 100` / `maxCompletes 100` with `retryDelay: none` [V-rec].
   - For `battlepyramid` the attempt cap is a lifetime cap, with no exception for a retry period (`libs/quest.ts` 2505-2516). The schema maximum is 100 (`validators/objectives.ts` 911-912) [V-src].
   - The Battle Pyramid list ignores attempts (`quests.ts` 498), so after the 100th start the run is still listed but refused. → **F04**

## Journey 3: a crafter or gatherer (the Haul and the profession chests)

1. **Getting a page.**
   - Endgame Wreck 2.4% (not built). Every Rare-chart ending 1.5% each [V-rec in 339]. Pages are tradeable [V-rec].
   - The page text describes crates, lockers, cut-through, leaving and alertness. It mentions no rank gate [V-rec].
2. **Starting the Haul.**
   - The Haul spec still carries `gate: "huntingRank S RANK"` / `"gatheringRank S RANK"` on all six graphs [V-rec, `haul_spec.json`]. That gate is superseded by RUL-2026-10-29-052.
   - If the builder copies it, `isAvailableUserQuests` refuses non-professionals (`libs/quest.ts` 2391-2400, 2478-2479) [V-src], and they would hold pages they cannot use. → **F11**
3. **The step graph** (spec; 55-80 objectives per page, under the ~90 limit) [V-rec].
   - Every battle routes to `fail` on a loss.
   - "Leave" is offered at every step from 2 on, except straight after a cut-through. That exception is by rule: a cut must be followed by a fight (RUL-2026-10-29-044 item 5).
   - Step 1 has no "leave", which is right because there is nothing to leave with.
   - No dangling references, no unreferenced nodes. The endings pay chests as `reward_items` (locker bonus chests as chance lines).
   - There is no pick, so the F01 trap does not apply. Concurrency is one Battle Pyramid at a time [V-src].
4. **Chests.** The 8 profession chests are ordinary caches (339 phase 1). Anyone can open them [V-rec].
5. **Pets in the Haul.** The Haul fights are QUEST battles, so the Little Horror fights (`libs/combat/pets.ts` 29-30) [V-src].

## Journey 4: a returning player on week 2 (Friday to Sunday)

1. **What does not reset (by the engine):**
   - Wreck Sighted: one attempt, one completion, lifetime.
   - The Jar and the two Wreck variant tokens: `onlyOnce`, per dungeon id, lifetime.
   - Chart runs: lifetime attempts toward 100 (F04).
   - An unclaimed pick (F01).
   - Charts in the inventory: no expiry anywhere.
   - Achievements: none in this release (RUL-2026-10-31-069).
2. **What closes on Monday:** nothing in the records. → **F06**
   - A dungeon has one `expiresAt` and quests have one `startsAt`/`endsAt` window. Neither repeats (`validators/dungeon.ts` 67; `libs/quest.ts` 2457-2460) [V-src].
   - No doc says how the Friday-to-Sunday weekend is enforced: hide and unhide each week, or edit the dates.
   - **Hiding a run pauses any attempt in progress.** It resumes once the run is visible again (`layout/PyramidRunBoundary.tsx` 23-29; `quests.ts` 1408-1415) [V-src].
   - **Re-sending a run's content restarts it**: a changed `updatedAt` fails `hasQuestContentChanged` (`libs/questRun.ts` 23-30), so the player must abandon and pay again (`quests.ts` 2733-2745) [V-src]. → **F05**
3. **Steeping on week 2** (not built).
   - Special quests are exempt from completion caps (`libs/quest.ts` 2518-2526).
   - Using a second chart while a steeping attempt is open is refused before anything is spent (`server/api/routers/item.ts` 1996-2025) [V-src].
   - If the 3 Core Rot are `entryItems`, the engine charges them at the start. A shortfall rolls the chart use back with "You need 3× Core Rot in your inventory to enter." (`quests.ts` 2733-2760, 2786-2815; `item.ts` 2156-2160 and the receipt rollback) [V-src]. This settles loot tables §5's "To verify before building". → **F13, F22**
   - If the Rot is instead taken by `deliver_item`, the whole Core Rot stack is deleted (`quests.ts` 4170-4200; RUL-2026-10-29-055 item 6) [V-src]. → **F13**
   - A lost steeping fight in a non-isolated special quest sends the player to hospital, because only isolated runs clamp HP (`libs/combat/database.ts` 1324-1326) [V-src]. The step that returns the chart then waits until they are awake (`libs/quest.ts` 2983-3000). → **F32**
4. **Variants and tokens.**
   - All 19 variants have been visible on their base weapons since push/329 ran. They show as "Need …" (`items/page.tsx` 1966-1981) [V-src], while every token is hidden. → **F27**
   - Crownbreaker (Thornsilver) says "Proof you walked every deck." It has no source until the upstream fix (RUL-2026-10-31-069). → **F09**
   - Tokens have no Consume button. Unlocking happens from the weapon's **Variants** button, then "Use <token>" (`items/page.tsx` 1259, 1279-1290; `item.ts` 1458-1525) [V-src]. The token text says "Use it". → **F12**
5. **The pet.**
   - Galley Stores' 20,000 experience lands only if the active pet is battle-enabled, has its appearance generated for its **current** rank, and is not on a task. Otherwise the experience is lost, and nothing stops the item being consumed (`libs/pets/experience.ts` 13-38) [V-src]. → **F10**
   - The Little Horror's default jutsu is frozen into the pet when the Jar is opened (`item.ts` ~2115-2125, "Freeze identity, traits and defaults") [V-src]. → **F16**

## Findings

"Built" means the finding is in records that have run or will run unchanged (329/342-352, and 339 as generated). "Not built" means a spec or design doc for content still to be built.

| ID | Sev | Where | What happens | Why (source) | Proposed fix | Built? |
|---|---|---|---|---|---|---|
| F01 | **BLOCKER** | 339 four runs; every future chart run (`rewardMode: choose`) | A run is started again while its previous completion pick is unclaimed. It reaches its win ending but cannot complete. The old pick cannot be claimed inside an isolated run, so the player must abandon, losing the chart and the run's haul. | [V-src] `queries/quests.ts` 1573-1604 (restart keeps `pendingRewardChoice`); `quests.ts` 3578/3635/1480 (`choice_pending`); `libs/questRun.ts` 58-71 (allow-list has no `quests.claimRewardChoice`); `PyramidRunBoundary.tsx` 16-22 | (1) Now: add the Lantern's sentence ("Claim any reward choice still waiting from an earlier run before you set out") to every chart's item text and every chart run's quest description. (2) Upstream: refuse the start while a pick is pending, before entry is charged, or allow `quests.claimRewardChoice` during isolation. | Built + not built |
| F02 | **BLOCKER** | 339 The Buried Cache (`push/skyglass_update.gen.py` `cache()`, from `G.cache()`) | Every battle is unscaled, against the base records that RUL-067 tunes for the endgame Wreck. Level-45 players get the chart from the easy Wreck (5%) and from the common endings (10%), and lose a run the text calls "scaled to you". | [V-rec] scratch 339: `b_ambush1/2`, `b_guardian(_late)` `opponent_scaled_to_user: false`; RUL-2026-10-28-010 item 7; loot tables §2; 339 item text | Set `opponent_scaled_to_user: true` on the four battles (re-check the Sentinel's tuning once scaled), or drop "scaled to you" and take the chart out of the easy Wreck. Decide before 339 is regenerated. | Built (339) |
| F03 | **BLOCKER** | Charts spec `objectiveShape`; text §2.3/§2.7 (`f_spat`); Reliquary Seal / Last Heading item text | The spec puts consolation rewards on the fail ending: "failObjectiveId -> fail ending (the run's consolation, e.g. 1 Core Rot)", and the steeping loss "returns the chart". A `fail_quest` objective is never marked done, so its `reward_items` are never paid. The chart (steeping) or the Rot (Epic run) is lost. Routing the Epic run's loss to a `win_quest` instead would pay the full completion pick. | [V-src] `libs/quest.ts` 1514-1525 (`win_quest` sets done; `fail_quest` only pushes the consequence); 494-522 (only done objectives pay) | Put the consolation on a **dialog** objective that the fail route reaches and that leads on to `fail_quest` (the dialog's reward is paid when it completes). In the special steeping quests, which have no quest-level pick, `f_spat` may instead be a `win_quest` carrying the chart. | Not built |
| F04 | MAJOR | 339 four runs, Crownhold; future runs | `maxAttempts 100`, `retryDelay none`: after 100 lifetime starts a run is closed to that player for good. On a weekly event this is reachable: commons and the Buried Cache at ~5-10 a weekend → 10-20 weekends [INF on volume]. The run stays listed but every start is refused. | [V-src] `libs/quest.ts` 2505-2516 (attempt cap ignores `retryDelay`), `validators/objectives.ts` 911-912 (max 100), `quests.ts` 498 (listing ignores attempts) | Track attempts per player. Plan a reset, for example re-creating runs per season. Raise an upstream request for an unlimited or period-based attempt cap on Battle Pyramid runs. | Built + not built |
| F05 | MAJOR | 339 go-live; any later re-send of a live run | (a) 339 re-sends the four runs with `hidden: true`. If the event is published before 339 runs, 339 hides them again. (b) Any content re-send while players are mid-run forces them to abandon and pay a new chart. | [V-rec] scratch 339 quest `hidden: True`; [V-src] `libs/questRun.ts` 23-30, `quests.ts` 1408-1415, 2733-2745 | Write "339 runs **before** the publish step" into its preconditions. Do every later run edit while the event is closed, and announce it. | Built |
| F06 | MAJOR | Design (none exists) | No mechanism is designed for "Friday to Sunday, every weekend". Dungeons have one `expiresAt` and quests one window, with no repeat. Charts never expire, so unless the runs are hidden on weekdays they can be run all week. | [V-src] `validators/dungeon.ts` 67, `libs/quest.ts` 2457-2460; [V-rec] no doc covers it | Decide the weekly operation: hide/unhide the Wreck and runs (a visibility-only edit pauses attempts safely) or edit the dates, who does it, and whether chart runs stay open on weekdays. Record it in a ruling. | Not built (ops) |
| F07 | MAJOR | push/348 Wreck Sighted; push/263 | No player text says where the Wreck is (sector 210, 15/6). The dungeon list only shows the player's current sector. | [V-rec] Wreck Sighted text; push/263; [V-src] `validators/dungeon.ts` `dungeonSectorSchema` | Add the sector and the landmark to `d_chart` / `w_done` (and to the announcement). | Built (hidden) |
| F08 | MAJOR | RUL-2026-10-31-070 note; SKYGLASS_PETS.md l.63 | Both say pets do not fight in the Wreck. They do: dungeon floors start battles as `"QUEST"`. The harness matched the engine; the docs are wrong, and future decisions could rest on them. | [V-src] `server/api/routers/dungeon.ts` ~357-378 (`initiateBattle(..., "QUEST")`), `combat.ts` 1990-1995, `libs/combat/pets.ts` 29-30 | Correct the note through a ruling correction and SKYGLASS_PETS.md. Loot tables §5b ("hunts, pyramid, dungeons") is right. | Docs |
| F09 | MAJOR | push/329 variant "Crownbreaker" (Thornsilver) | Visible to everyone today as "Need Crownbreaker", described as "Proof you walked every deck." There is no source until Walked Every Deck exists (RUL-069), possibly for many weekends. | [V-rec] 329; [V-src] `items/page.tsx` 1966-1981; README: variants have no hidden state | Delete or re-describe the variant until Walked Every Deck ships, or accept it and say "coming later" in the announcement. | Built (live now) |
| F10 | MAJOR | push/329 Galley Stores | It is consumed even when no pet can take the experience. A just-opened Little Horror with no generated appearance, or a pet whose art is behind its rank, gets nothing. The text covers "ready for battle, not on a task" but not the appearance. | [V-src] `libs/pets/experience.ts` 13-38 (`artRank = rank`, avatar set, `battleEnabled`) | Add "and its appearance generated for its current rank" to the text. Upstream: refuse the consume when no pet is eligible. | Built (hidden) |
| F11 | MAJOR | `haul_spec.json` (all six graphs `gate`) | The spec still carries the S-rank hunting or gathering gate that RUL-052 removed. Copied into the quests, it would leave every non-professional holding unusable pages. | [V-rec] spec; [V-src] `libs/quest.ts` 2391-2400, 2478-2479 | Haul generator: drop `huntingRank`/`gatheringRank`. Add a check to `skyglass_check.py`. | Not built |
| F12 | MAJOR | push/329 Skyglass Token and 7 boss tokens | The text says "Use it to unlock …". The inventory shows no Use/Consume button for tokens. Unlocking is only from the weapon: Variants → "Use <token>". | [V-src] `libs/item.ts` 52-82 (no `unlockitemvariant`), `items/page.tsx` 1259, 1279-1290, 1966-1981 | Text: "Open the weapon in your inventory, choose **Variants**, then **Use Skyglass Token**." | Built (hidden) |
| F13 | MAJOR | Steeping spec (loot tables §5; RUL-055) | How the 3 Core Rot are taken is not specified. `deliver_item` would delete the whole tradeable Rot stack. | [V-src] `quests.ts` 4170-4200 (one row per id removed); `server/utils/questEntry.ts` 98-130 (`entryItems` charge exact quantities) | Specify `entryItems: [{ids:[Core Rot], number: 3}]`. "Take it back" then refunds the chart **and** 3 Rot. | Not built |
| F14 | MAJOR [INF] | 339 Foundry/Archive/Watch `questRank` A; Buried Cache B; Crownhold S | Rank A needs Jonin or higher. If level-45 players can be Chunin, the easy-Wreck audience is offered Foundry charts (Buried Cache pick) it cannot run, and new commons need rank ≤B. | [V-src] `libs/train.ts` 123-139, `libs/quest.ts` 3169-3179, `quests.ts` 2667-2669; rank-by-level not checked | Confirm the rank of a typical level-45 player. If Chunin is possible, set the commons to ≤B and say "Jonin" in the Rare chart text, or lower the ranks. | Built + not built |
| F15 | MAJOR | Loot tables §5 "Breaking the seal"; 339 `archive()` | The guaranteed Core Rot ×2 echo fight has no text, generator or node. 339 re-sends the Archive whole, so a separately built version would be erased at go-live. | [V-rec] scratch 339 Archive (36 nodes, none of them break-the-seal); `grep` of the generators and the text | Build it inside `skyglass_update.gen.py archive()` (text in SKYGLASS_TEXT.md), or remove it from the loot tables and re-count the Rot supply. | Not built |
| F16 | MAJOR | push/347 order vs 339 / publish | The Little Horror's defaults are frozen when the Jar is opened. A Jar opened before 347 runs gives a pet without Little Maw. | [V-src] `item.ts` ~2115-2125 | Add "347 has run" to 339's preconditions. push/353 publishes Little Maw, RUL-071. [INF: whether a player can add the signature later] | Built (ordering) |
| F17 | MAJOR | Loot tables §5 Core Rot sources; §4a tainted runs | (a) "The Core Horror's hunt runs: 40% in The Fall, the Rotted Reliquary and the Burning Heading … as an AI drop". The Rotted Reliquary has no Core Horror. (b) An AI drop goes against RUL-2026-10-28-022 and the charts spec: battles carry no rewards. | [V-rec] charts spec `rotted` fights; objectiveShape | Make it a 40% ending drop on those three runs, as §4a already reads ("Core Rot 40%"). | Not built |
| F18 | MINOR | push/329 Reliquary Seal / Last Heading text; text §2.7 | "Short of 3 Core Rot? Take it back." With Rot as entry items the engine refuses the use and keeps the chart, so this path never appears. The real message, "You need 3× Core Rot in your inventory to enter.", is not what the text prepares the player for. | [V-src] `quests.ts` 2733-2760; `item.ts` consume rollback | Text: "Without 3 Core Rot the chart will not go in; nothing is spent. Changed your mind? Take it back at the start." | Built (hidden) + not built |
| F19 | MINOR | Spec and text: the Archive's Stonebound summon, Little Maw, and the rest of the set-piece library | (Grouped as an ordering reminder.) Several public runs depend on hidden library records: push/342 jutsu and AI copies. Battle assets must be unhidden or they do not play (law 16c). | [V-rec] 342 `hidden`; ENGINE_LAWS 16c | Add "library animations unhidden (push/321 path) and AI copies built" to 339's preconditions. | Built (ordering) |
| F20 | MINOR | `charts_spec.json` lowtide / reliquary / burning | Still lists "PRESS ON (proposed)" rooms that RUL-060 cut. The text doc is correct. | [V-rec] | The run generator ignores `pressOn` on these three. Add a gate. | Not built |
| F21 | MINOR | Loot tables §5 "Every chart run" | "Rewards bank at each fight" contradicts RUL-2026-10-28-022 and the built graphs, which pay at the ending. | [V-rec] | Doc edit through its owner. | Docs |
| F22 | MINOR | Loot tables §5 "To verify before building" | Answered: entry items are charged at the start, and a shortfall rolls back the item use. | [V-src] `quests.ts` 2733-2760, 2786-2815 | Close the item. | Docs |
| F24 | MINOR | push/348 Wreck Sighted | "A chart only works while it still holds that shape. Don't sit on it." Charts never expire. | [V-rec] | Reword the flavour so it does not imply expiry. | Built (hidden) |
| F25 | MINOR | Every chart text | "Bring it to the Battle Arena": the run is under the arena's **Battle Pyramid** tab. | [V-src] `battlearena/page.tsx` 166-185 | "Battle Arena → Battle Pyramid". | Built + not built |
| F26 | MINOR | 339 The Buried Cache quest image | Uses `icon-chart-drowned-foundry.webp`. | [V-rec] | Confirm this is intended (the Buried Cache export is held back, art audit D2). | Built |
| F27 | MINOR | push/329 variants (the other 18) | Visible live with "Need Skyglass Token" / "Need <token>" while every token is hidden. Pre-launch leak. | [V-src] `items/page.tsx` 1966-1981 | Accept, or time the announcement. | Built (live now) |
| F28 | MINOR | Loot tables §5b; Jar text | `onlyOnce` is per player per dungeon id, for life. A released Little Horror can never be re-earned, and a re-created Wreck dungeon would reset every once-per-player drop. | [V-src] `libs/dungeonRewards.ts` 29-37, `dungeon.ts` 446-452 | Jar text: "You can earn it only once." Never re-create the Wreck; edit it in place. | Built + not built |
| F29 | MINOR | 339 Lantern text, Crownhold description | "Health carries" leaves out chakra. Every other run says both. | [V-rec] | Add "and chakra" if Crownhold carries chakra too. Check `keepOriginalPools` / `givePools` intent. | Built |
| F30 | MINOR | push/340 badge "Crownbreaker" vs token and variant "Crownbreaker" | Same name, different sources: Crownhold pick vs Walked Every Deck. Badge holders will expect the variant. | [V-rec] | Mention the difference in the announcement, or rename one. | Built |
| F31 | MINOR | Wreck (both versions) | No level gate exists on dungeons: carries and level-100 easy-Wreck farming are possible. | [V-src] `validators/dungeon.ts` | Accept (rewards are lower on the easy Wreck), or say "level 45-60" in its description. | Not built |
| F32 | MINOR | Steeping spec | A lost steeping fight hospitalizes the player if the special quest is not isolated, so the chart-return step waits until they heal. | [V-src] `libs/combat/database.ts` 1324-1326, `libs/quest.ts` 2983-3000 | Set `isolated: true` on the steeping quests, or say "heal, then collect your chart from the Logbook". | Not built |

## Economy at player level

- **The chain feeds itself.** Commons → (10%) Buried Cache → (15%) Foundry → (10%) Archive → (25%) Reliquary Seal. The Watch chart comes from the Wreck (6%) and the Chart Case (20%) → (25-45%) The Last Heading. Epic runs → (15%) Lantern → Crownhold, which pays both Epic charts at 25% each [V-rec in 339/349].
- **No loop dead-ends** if F02 and F03 are fixed. The Archive pick's Chart Case is the deliberate sustain loop (RUL-040).
- **Rewards a player may not be able to use:**
  - Galley Stores without an eligible pet (F10).
  - Untradeable Captain's / Core Horror tokens without The Unwritten / Oathbinder. The text says so; the token waits in the inventory.
  - Rank-A charts for a Chunin (F14, [INF]).
  - Pages under a copied rank gate (F11).
  - Charts past the 100-attempt cap (F04).
- **Core Rot supply at go-live** depends entirely on not-yet-built content: the Wreck drop, the commons, the Core Horror runs, break-the-seal (F15) and the Epic-run consolation (F03). None of the four 339 runs drops Rot [V-rec]. Steeping is therefore impossible until those exist; 339 precondition 2 covers this.

## Not done

- No live playtest, browser check or capture.
- No harness re-run. The press-on, scaling and damage claims rest on the records and the source.
- The rank a level-45 player usually holds (F14) and whether a pet can gain its signature after the Jar opens (F16) were not verified.
