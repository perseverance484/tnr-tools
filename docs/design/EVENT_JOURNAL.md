# The event journal: a weekly roadmap quest

**Status:** ACTIVE (RUL-2026-11-08-139: every order open at once; RUL-2026-11-05-120; D1-D6 settled by RUL-2026-11-05-121; landing, close time and the Wreck Sighted tutorial by RUL-2026-11-05-122). The idea, the decisions and the
Week 1 rewards are the director's; the shape, the pages and the text are Claude's drafts. Open: the page image (QI01) and the
tutorial's text (section 6a).
**Date:** 2026-11-05. **Repository baseline:** `perseverance484/tnr-tools` main at `213ffabf`. **Game-source pin:**
`studie-tech/TheNinjaRPG` at `3314d122` (read with `git show`, not run). Zero live requests.
**Framework:** `docs/design/EVENT_STRUCTURE.md` (P5 legibility, P6 diegetic progression). **First build:**
`push/490_skyglass_journal_week1.json` from `push/skyglass_journal.gen.py` (HIDDEN, not run).

## 0. Source

Director, 2026-11-05, verbatim:

> "Design that tracker thing. That journal is how each weekend differs. You take that at the start and it defines your weekend or something. Lets work that out its a great idea. Its like an event roadmap and we can write a new one for each event. Like challenge players to do the rotted heading this weekend, or use a lastlight lantern, etc etc. It doesnt have to map every piece of content because that wouldnt be possible but like a good first one would involve doing the wreck sighted, 3 skyglass wreck dungeons, etc."

## 1. What a journal is

One quest per weekend, taken at the start of the weekend. Its entries are tracker objectives that count while the
quest is active, in any order, as the player plays the event normally. It answers three of the four P5 questions in
one place, the Logbook: **what can I do now** (this weekend's orders), **what is ahead** (the entries point up the
ladder), and **what have I done** (each entry's progress bar, and the claimed rewards). A new page each weekend makes
each weekend different without new content.

**In the fiction (P6)** the journal is an object that belongs to the event's world, never "Weekly Challenge 1". For
Skyglass it is a page of **the Ghost Ship's watch log**: the salvager on the shore dries one page a weekend, and each
page is one watch's orders in the officer's brush, with the player's name written in at the top (the Watch Roster
already "has your name on it"). Each entry is an order in the crew's voice, followed by a plain line saying what
counts. The page is gone when the tide turns at the end of the weekend.

## 2. Engine facts that shape it (source-verified at `3314d122`)

| Fact | Citation | Consequence |
|---|---|---|
| Tracker tasks: `craft_specific_item`, `train_specific_jutsu`, `complete_specific_quest`, `buy_item` (NPC shop only), `use_specific_item_combat`, `use_specific_jutsu_combat`, `tag_usage_win`, `damage_dealt`; each has a `value` (a count) | `validators/objectives.ts` 288-297, 695-773 | "3 times" is native. There is no "obtain an item" task: only craft, buy and use |
| `complete_specific_quest` credits +1 once per active -> completed transition of any listed quest; repeats count again; a failed run never resolves | `libs/quest.ts` 677-693 (emit), 1584-1595 (match), 1884 (done at `value`) | "Win the Low Tide Run or the Night Watch 2 times in total" is one entry |
| Progress counts only while the journal is active: trackers are built for active quests only | `libs/quest.ts` 1038-1074 (`getNewTrackers` over `getUserQuests`) | Nothing done before taking the page counts; say so on the page |
| **Dungeons cannot be tracked** (pages leave the Wreck off until upstream adds it, D1). Dungeon battles return before any tracker task; the dungeon reward claim emits none; `dungeons_completed` is a lifetime count of every dungeon | `libs/combat/database.ts` 1206; `server/api/routers/dungeon.ts` 466-472; `libs/quest.ts` 1403-1406; `server/utils/achievementObjectives.ts` 56-61 | "3 Skyglass Wreck dungeons" is left off (D1). Item and jutsu use inside the Wreck does not count either |
| A one-shot quest cannot be re-credited: Wreck Sighted is `maxCompletes: 1` | `push/374_skyglass_wreck_sighted_salvager.json` | A veteran can never satisfy "complete Wreck Sighted"; the page uses "go to the Wreck" (`move_to_location`) instead |
| Battlepyramid chart runs are ordinary quests and do credit it; a journal (`event`) and a run (`battlepyramid`) can be active together (event limit 4, pyramid limit 1) | `libs/quest.ts` 2910-2930; `drizzle/constants.ts` 1072 | Chart runs, tainted runs, Crownhold, the Haul and the Mother of Echoes are all trackable by quest id |
| A non-consecutive quest completes when every objective is done; a consecutive one when every node on the walked path is done | `libs/objectives.ts` 110-140 | No win node is needed |
| Forge L03 refuses a quest create without `consecutiveObjectives: true`, **but a consecutive page shows only its first order** | `forge/src/runner/lints.mjs` 77; TheNinjaRPG `libs/objectives.ts` (`isQuestObjectiveAvailable`, `selectedObjectivePath`); `libs/quest.ts` (the availability skip before task matching) | The earlier reading here (the whole chain goes live within a load or two) was wrong. The engine links a consecutive chain one step per tracker pass and skips every order off the walked path, so players saw only order 1 and later orders did not count. Week 1 went live that way on 2026-11-06; the director set it to `false` in the editor on 2026-11-07. **Pages now create with `true` (L03) and publish with `false`** (RUL-2026-11-08-139). Safe: a page has no win, dialog or battle node (law 23's danger), and a non-consecutive quest completes when every objective is done |
| **No ending step can wait for the entries.** For the same reason a final dialog or `win_quest` after the chain is live from the start, not after the entries | as above | The ending is the engine's own (section 4): the claim that completes the page |
| Each objective's rewards pay once, when the player claims it (the gift icon); the quest-level reward pays on completion | `libs/quest.ts` 494-520; `layout/Objective.tsx` 99-112 | Per-entry and completion rewards are both native |
| The Logbook shows each entry as the engine's fixed task title ("Complete Specific Quest") with a Goal x/N bar; the entry's own text is behind a (?) icon, and a non-location entry's reward is not listed | `layout/Objective.tsx` 142-180, 184-214; ENGINE_LAWS law 53 | The quest description carries the whole page; each entry's text names its own reward |
| `startsAt`/`endsAt` are SQL `DATE`s with no time. Starting compares the date string with the current UTC ISO time; the active set uses `new Date(date)`, which is UTC midnight | `drizzle/schema.ts` 4333-4334; `routers/quests.ts` 2682-2687; `libs/quest.ts` 2456-2459, 140-153; `queries/quests.ts` 1384-1385 | A page opens **00:00 UTC on its startsAt** and closes **00:00 UTC on its endsAt**. Pages set endsAt to the Tuesday, so they close at the end of Monday UTC (Monday 18:00 US Central, RUL-2026-11-05-122 item 2). **Inferred:** an expired page stops counting and its unclaimed rewards cannot be claimed; it may still hold one of the four event slots until abandoned |
| An item can start only a `special` quest; special quests list nowhere and have no completion caps | `server/api/routers/item.ts` 1995-2022; `libs/quest.ts` 2518-2520 | Option for handing the page over as an object (D2), and the route for the Wreck tally (D1) |
| Editing a live event quest does not restart open attempts (only pyramids and isolated runs restart) | `libs/questRun.ts` 22-30 | A typo fix on a live page is safe |

## 3. Skyglass: what a page can count

| Content (`SKYGLASS_EVENT_MAP.md` §1) | Task | Ids (harvested bundles) |
|---|---|---|
| N0 Wreck Sighted | not used: one-time per player; use `move_to_location` sector 210 for everyone | old `v7kKhLXsX9aofQfc7BnGx` (to be deleted); new from push/497 |
| N1/N2 the party Wrecks | **not trackable** (section 2); D1 | — |
| N3/N4 commons | `complete_specific_quest` | Low Tide `pFQBaJxU_8RSvSi4Kir1Z`, Night Watch `dnzL-bDrAEVXrKB5xariu` |
| N5-N8 Rare runs | `complete_specific_quest` | Buried Cache `CgwAVCyZLgNQtEnqgLxxv`, Foundry `UGHSuhi83C3wRtH3FD4Eu`, Archive `-bZ_ZoI6yrUJ_LKT9R5zm`, Captain's Watch `liljq0yVXWTSna4X6dZE1` |
| N9/N10 Epic runs | `complete_specific_quest` | Sealed Reliquary `yZoR_dPSdg8ksO77gDH_A`, The Fall `H9YInJtnzKCOEMv-sNgzP` |
| N11 steeping | **avoid**: "Take it back" ends in a win and refunds the chart, so it would credit a steep that never happened (`push/skyglass_steeping.gen.py` header). Count the tainted runs instead | — |
| N12/N13 tainted runs ("the Rotted Heading this weekend") | `complete_specific_quest` | Rotted Reliquary `FsuXzvaqr_R25p8cEkxoK`, Burning Heading `ozDN-G6nGFXGgKuPZ04Gr` |
| N14 the Haul | `complete_specific_quest`, any of six | Trophy Hold `0_wTZMTqvxM-gvl_s1s7c`, Bone Store `ww_baSsbBet0mx7MK52yI`, Snare Room `vMh6SDID0XTrVJ0f1QmFD`, Overgrown Stores `5y9wAYELSdNa8Jgim1sgD`, Ore Vault `C1JPScsgSMcVXQUfuFgcs`, Bloom Cellar `UO65dN640MgAbNBBopTVI` |
| N15 Crownhold ("use a Lastlight Lantern") | `complete_specific_quest`; the Lantern is an entry item, consumed at the start, not "used", so winning Crownhold is the honest proxy | `fqqpkcp_L4oOsC6yyodlk` |
| Lastlight jutsu (Crownhold pick) | `use_specific_jutsu_combat` | `0F-68bxOXW_LkJnXV0lwT` |
| Skyglass Serum | not usable: `preventBattleUsage` is true (item.get 2026-11-08), so no in-battle order can count it. Check that flag before any `use_specific_item_combat` order | `XhilCv1Hq4eNt-Wddok-m` |
| N16 the Mother of Echoes | `complete_specific_quest` (exclude the practice quest) | `IBPNwhAzlAJPXoeEnp8gW` |
| Holding shards, charts, tokens | **not trackable** (no "obtain" task) | — |

## 4. Week 1: "The Watch Log: First Page" (built: push/490)

The page climbs the ladder from the shore to Crownhold (rungs 0-5), so a new player sees the whole spine in one read
and a veteran has a full weekend. Casual players (~3 h) earn the first entries; the last two are the stretch.

> *The salvager has dried a page of the Ghost Ship's watch log and weighted it under a stone for you. It is one
> watch's orders, in the officer's brush. Your name is written in at the top, in the same ink.*

| # | Order (in voice) | Plain line | Counts | Reward on claim (approved, D3) |
|---|---|---|---|---|
| 1 | Walk the tideline where she lies. The page's first order is only to look at her. | Go to the Skyglass Wreck (sector 210) | `move_to_location` | Tide Chart |
| 2 | Stand two low watches: the breach the low tide opens, and the night roster with your name on it. | Win the Low Tide Run or the Night Watch, 2 times in total | 2 | Medicine Inro |
| 3 | Follow one of the crew's own charts below the waterline: what they buried, the works, the archive or the helm. | Win one Rare run once | 1 | Archive Chart Case |
| 4 | Go down where the Core could not hold them: to the reliquary, or to the night she fell. | Win the Sealed Reliquary, The Fall or a rotted run once | 1 | Skyglass Coffer |
| 5 | Carry the last light home. The lantern still points the way to Crownhold. | Win Crownhold once (its way in is a Lastlight Lantern) | 1 | Sealed Treasury |
| — | **Page complete.** *Every order is answered, and the salvager folds the page into her coat with the others. "The next tide brings the next page."* | claim the last order | — | Skyglass Token |

**The ending (D6).** No objective can wait for the others (section 2), so the page ends the way every TNR quest ends:
the player's claim. The last order's gift icon in the Logbook is the claim button; that claim completes the page and
the game shows "Finished: The Watch Log: First Page" with the "Page complete" line above and the Token
(`layout/Logbook.tsx` 903-931; `libs/quest.ts` 436-497). The page's description ends "Claiming the last order completes
the page." A dialog ending was rejected: it would be clickable from the first minute and say "Page complete" early.
**Window (D4, RUL-2026-11-05-122 item 2):** 2026-11-06 00:00 UTC to 2026-11-10 00:00 UTC (the end of Monday UTC), with the release; it is hidden until published, so in
practice it opens at publish.

Reward rationale: every reward is an existing event item that feeds the next rung or the shared containers (P1), none
is a gate item (no Lantern, shard or Epic chart), and the page pays at most one Token and one Coffer a weekend, below
one Crownhold pick. The values are the director's (`[[D-reserved-dauntless]]`).

## 5. Rotation and template

**Rotation.** One quest record per weekend, `startsAt` the Saturday, `endsAt` the Tuesday, so it opens 00:00 UTC Saturday
(Friday 6 PM Central, the same instant the weekly routine reopens both Wrecks; director 2026-11-08: "Friday for both")
and closes 00:00 UTC Tuesday (Monday 6 PM Central). Pages 1 and 2 opened on the Friday's date; page 2 was re-timed by
push/516. The Friday routine and the Wednesday hide read `state/skyglass_schedule.json` through
`scripts/skyglass_weekly.py` (the event runs Friday-Sunday, RUL-2026-11-01-096 item 4; Monday is grace, RUL-2026-11-05-122), `maxCompletes: 1`, `retryDelay: none`. Last weekend's page expires on its own; the new page
is a new record ("Second Page", "Third Page"). Only one page is ever in its window, so only one can be taken. Pages are
reusable: an old page can return later as a new record with new dates.

| Page | Theme | Entries (sketch) |
|---|---|---|
| Second: "The Rotted Heading" (built: push/512, rewards a draft for the director) | the rot | The Captain's Watch ×1 (Archive Chart Case); the Low Tide Run or the Night Watch ×1 (Medicine Inro; replaced the Serum order 2026-11-08, the Serum can't be used in battle); The Fall ×1 (Galley Stores); The Rotted Reliquary ×1 (Skyglass Coffer); The Burning Heading ×1 (Sealed Treasury); all five: Skyglass Token. Window 2026-11-13 to 2026-11-17 00:00 UTC |
| Third: "The Stores" (built: push/517, rewards a draft) | the Haul | a common run ×2 (Tide Chart); a Rare run ×2 (Archive Chart Case); any Haul room ×2 (Galley Stores); The Sealed Reliquary or The Fall ×1 (Skyglass Coffer); all four: Skyglass Token. Window 2026-11-21 to 2026-11-24 00:00 UTC |
| Fourth: "Her Invitation" (built: push/519, rewards a draft) | the finale | a common run ×1 (Medicine Inro); a Rare run ×1 (Archive Chart Case); a Haul room ×1 (Galley Stores); an Epic or tainted run ×2 (Skyglass Coffer); Crownhold ×1 (Sealed Treasury); the Mother of Echoes ×1 as the stretch (Sealed Treasury; director 2026-11-08, needs her live by 2026-11-28); all six: Skyglass Token. The Lastlight jutsu stays off (only a Crownhold pick has it). Window 2026-11-28 to 2026-12-01 00:00 UTC |
| Fifth: "Every Deck" | a full tour | one entry per Rare run, ×1 each; raise the Lastlight in battle ×1 |

**Template for any event** (an event sheet adds this as part of item 9, legibility):
1. **The object:** what the page is in the world, who hands it over, why it lasts one weekend.
2. **Entries:** 4-7, from the event's trackable actions (section 2's list); every entry is a quest id set, a jutsu or
   an item use, or a location. Climb the ladder from the entry rung; the last entry is the stretch.
3. **Each entry's text:** one line in voice, then one plain line naming exactly what counts and its reward.
4. **The quest description** opens with one plain line for the dashboard card ("This weekend's orders: N to claim,
   <reward> for all N."), then carries the whole page (voice lines, the numbered plain list, the rules: counts only
   while held, any order, claim before it closes).
4a. **Orders first** (pages 3 on, director 2026-11-08): the Logbook titles each card by its task ("1. Complete Specific Quest") and keeps the order's own text behind the card's ?, so the page text opens with the numbered orders, matching the card numbers.
5. **Dates:** startsAt the Saturday, endsAt the Tuesday (open 00:00 UTC Saturday = Friday 6 PM Central with the Wrecks,
   closed 00:00 UTC Tuesday). Hide the Wednesday after (`push/skyglass_journal.gen.py hide`, hidden true only).
5a. **Two jobs per page** (RUL-2026-11-08-139): `push/skyglass_journal.gen.py --page N` creates it hidden with
   `consecutiveObjectives: true` (Forge L03); `... publish --page N --from <bundle>` re-sends it with `hidden: false`
   and `consecutiveObjectives: false`, so every order is open at once. The page still lists only from its startsAt, so
   the publish can run any day before. Pages after the first reuse the live QI01 icon, so both jobs run over the
   connector. **Do not re-run push/507**: it re-sends Week 1 with `consecutiveObjectives: true` and would undo the
   director's fix.
6. **Rewards:** event items only, nothing that is a gate or finale input, values set by the director.
7. **No per-page badge:** one badge for the whole event keeps it exclusive (D5).
8. **Checks:** no entry depends on a once-only quest, a dungeon, steeping's refund path, or "obtain"; every listed
   quest id is live; the page passes `validate.py` (ledgered win-node lint), `check_manifest`, the event's own check.

## 6. Landing: how players find the page (APPROVED, RUL-2026-11-05-122 item 1)

What the engine offers (theninjarpg@3314d122):

| Surface | What it does for an `event` quest | Citation |
|---|---|---|
| Administration Building, "Information Board" | lists every available event quest in the player's village; this is where it is started | `app/[shell]/adminbuilding/page.tsx` 26-35; `routers/quests.ts` 403-435; `libs/quest.ts` 3115-3121 |
| **Profile dashboard, Events cards** | the closest thing to "featured on login": the profile's content cards list available event quests (name, description, image, "Administration Building", Auto Travel), second after missions; the card appears and disappears on its dates. The end date is not shown | `libs/profileDashboard.ts` 587-641, 684-700; `layout/ProfileDashboard.tsx` 216-240 |
| Logbook | the page once taken: the five bars, gift claims, the "Finished" toast | `layout/Objective.tsx`; `layout/Logbook.tsx` 903-931 |
| Login notification / pinned quest | none found for quests | searched `app/src` for featured / pinned quest surfaces: none |
| Start at an NPC | only the NPC-only `overworld` type is started from an overworld placement; a later option for "the salvager at the Wreck hands you the page", but it needs a placement made in the game's overworld editor and loses the Information Board and dashboard listing | `drizzle/constants.ts` 1071; `routers/quests.ts` 394-398 |
| Started by an item | `special` quests only, listed nowhere | `routers/item.ts` 1995-2022 |
| Text in existing entry points | any quest, dialog or item text can name the page; Wreck Sighted is the first thing a new player reads | `push/374_skyglass_wreck_sighted_salvager.json` |

**Approved landing (the "weekend challenge board"):**
1. The page is a dated `event` quest: it lands on the Information Board and as an Events card on every player's
   profile dashboard, with its own image, for exactly its window.
2. The card's first line is plain: "This weekend's orders: 5 to claim, a Skyglass Token for all five." (built).
3. Its own image: QI01, prompt in `docs/handoffs/SKYGLASS_ART_PROMPTS.md` §10 (register `docs/design/skyglass_art/ART_REGISTER.md`).
4. Wreck Sighted points to it (section 6a). Announce each page in the weekend post.

### 6a. The front door: Wreck Sighted, the one-time tutorial

**The event's front door is two quests with two jobs** (director, 2026-11-05: "Wreck Sighted is the tutorial one-time
quest. The pages are the repeatable challenge board."):
- **Wreck Sighted** (push/497, a NEW hidden one-time quest; the director deletes the old live one himself): six short
  salvager scenes that show the whole event through what she has seen, never as instructions (the Wreck and its crew;
  charts and the deeper runs they lead to; the lantern and Crownhold; the Haul's sealed stores; four shards and
  something beneath, hinted, never named; trade; a new page each weekend on the Information Board), a skip on the
  first scene, then the starting Tide Chart. Text of
  record: `docs/design/SKYGLASS_TEXT.md` §1a.
- **The pages** (push/490 and successors): the repeatable weekly board, unchanged.

**Engine facts.** One completion per player per quest id (`libs/quest.ts` 2503-2513): the new record is a new id, so
**players who finished the old Wreck Sighted will see the new one once** and get a second Tide Chart, by intent
(director: "they never got a good overview"). Deleting a quest is an in-game editor action for content roles; it also deletes every player's
history rows for that quest (`routers/quests.ts` 1090-1125). Forge cannot delete. Forge only refuses a duplicate live
name when a manifest sets `dedupNames` (`forge/src/runner/runner.mjs` 932-973); push/497 does not, so it can run
before or after the old one is deleted.

**References to the old id `v7kKhLXsX9aofQfc7BnGx`** (searched the whole repository and every harvested capture):
- live records: **none**. No captured quest names it as `prerequisiteQuestId`, `completeQuestIds` or `newQuestIds`.
  The journal pages count the Wreck by location, not by this quest. An in-game editor edit since the last capture
  would not show here.
- spent manifests (already run, history only): push/374 and push/385 (edits of the old record); their generators
  `push/skyglass_final_art2.gen.py` (`WRECK_SIGHTED_ID`), `push/skyglass_publish_quests.gen.py` and the original
  create in `push/skyglass_hoard.gen.py` (push/348). They are not re-run, so nothing breaks.
- docs: `push/README.md` (348, 385 and the 1450 phase note: history), this file's section 3 row (updated), and
  `docs/design/SKYGLASS_TEXT.md` §1 (the old text, kept as the record of what was live).
- Nothing needs a new id: no record points at Wreck Sighted. After push/497 runs, put the new id in section 3.

## 7. Director decisions (RUL-2026-11-05-121)

| # | Decision |
|---|---|
| D1 | No Wreck tally. Wreck dungeon clears stay off the pages; the director asks upstream for dungeon-clear tracking |
| D2 | A dated quest, YES. Landing approved (section 6, RUL-2026-11-05-122) |
| D3 | Week 1 rewards approved as drafted |
| D4 | Week 1 opens with the fight on Friday 2026-11-06; it now closes 2026-11-10 00:00 UTC (RUL-2026-11-05-122 item 2) |
| D5 | No badge per page; one badge for the whole event |
| D6 | The two validator diagnostics accepted; an ending players can see (section 4) |

## 8. Staff test before any publish

On a staff character, with push/490 run (hidden): take "The Watch Log: First Page"; reload; win a Low Tide Run. The
Logbook should show entry 2 at 1/2 (this confirms the chain is all live and counts in any order). Walk to sector 210:
entry 1 completes; claim it and receive the Tide Chart. Not yet checked: what the Logbook does with an expired page.
