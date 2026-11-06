# The event journal: a weekly roadmap quest

**Status:** ACTIVE (RUL-2026-11-05-120; decisions D1-D6 settled by RUL-2026-11-05-121). The idea, the decisions and the
Week 1 rewards are the director's; the shape, the pages and the text are Claude's drafts. Open: the landing proposal
(section 6, for approval) and the image.
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
| Forge L03 refuses a quest create without `consecutiveObjectives: true` | `forge/src/runner/lints.mjs` 77 | The entries form one chain. Availability walks the chain's links and never checks done; a non-dialog node links on to the next on its first touch (`libs/objectives.ts` 151-186; `libs/quest.ts` 1655-1662), and `profile.getUser` touches every active quest on each load (`routers/profile.ts` 3396-3403). So the whole chain is live within a load or two and counts in any order. **Behaviour to confirm** in the staff test (section 8) |
| **No ending step can wait for the entries.** For the same reason a final dialog or `win_quest` after the chain is live from the start, not after the entries | as above | The ending is the engine's own (section 4): the claim that completes the page |
| Each objective's rewards pay once, when the player claims it (the gift icon); the quest-level reward pays on completion | `libs/quest.ts` 494-520; `layout/Objective.tsx` 99-112 | Per-entry and completion rewards are both native |
| The Logbook shows each entry as the engine's fixed task title ("Complete Specific Quest") with a Goal x/N bar; the entry's own text is behind a (?) icon, and a non-location entry's reward is not listed | `layout/Objective.tsx` 142-180, 184-214; ENGINE_LAWS law 53 | The quest description carries the whole page; each entry's text names its own reward |
| `startsAt`/`endsAt` are SQL `DATE`s with no time. Starting compares the date string with the current UTC ISO time; the active set uses `new Date(date)`, which is UTC midnight | `drizzle/schema.ts` 4333-4334; `routers/quests.ts` 2682-2687; `libs/quest.ts` 2456-2459, 140-153; `queries/quests.ts` 1384-1385 | A page opens **00:00 UTC on its Friday** and closes **00:00 UTC on its Monday** (Sunday 19:00 US Eastern). **Inferred:** an expired page stops counting and its unclaimed rewards cannot be claimed; it may still hold one of the four event slots until abandoned |
| An item can start only a `special` quest; special quests list nowhere and have no completion caps | `server/api/routers/item.ts` 1995-2022; `libs/quest.ts` 2518-2520 | Option for handing the page over as an object (D2), and the route for the Wreck tally (D1) |
| Editing a live event quest does not restart open attempts (only pyramids and isolated runs restart) | `libs/questRun.ts` 22-30 | A typo fix on a live page is safe |

## 3. Skyglass: what a page can count

| Content (`SKYGLASS_EVENT_MAP.md` §1) | Task | Ids (harvested bundles) |
|---|---|---|
| N0 Wreck Sighted | `complete_specific_quest` new players only; use `move_to_location` sector 210 for everyone | `v7kKhLXsX9aofQfc7BnGx` |
| N1/N2 the party Wrecks | **not trackable** (section 2); D1 | — |
| N3/N4 commons | `complete_specific_quest` | Low Tide `pFQBaJxU_8RSvSi4Kir1Z`, Night Watch `dnzL-bDrAEVXrKB5xariu` |
| N5-N8 Rare runs | `complete_specific_quest` | Buried Cache `CgwAVCyZLgNQtEnqgLxxv`, Foundry `UGHSuhi83C3wRtH3FD4Eu`, Archive `-bZ_ZoI6yrUJ_LKT9R5zm`, Captain's Watch `liljq0yVXWTSna4X6dZE1` |
| N9/N10 Epic runs | `complete_specific_quest` | Sealed Reliquary `yZoR_dPSdg8ksO77gDH_A`, The Fall `H9YInJtnzKCOEMv-sNgzP` |
| N11 steeping | **avoid**: "Take it back" ends in a win and refunds the chart, so it would credit a steep that never happened (`push/skyglass_steeping.gen.py` header). Count the tainted runs instead | — |
| N12/N13 tainted runs ("the Rotted Heading this weekend") | `complete_specific_quest` | Rotted Reliquary `FsuXzvaqr_R25p8cEkxoK`, Burning Heading `ozDN-G6nGFXGgKuPZ04Gr` |
| N14 the Haul | `complete_specific_quest`, any of six | Trophy Hold `0_wTZMTqvxM-gvl_s1s7c`, Bone Store `ww_baSsbBet0mx7MK52yI`, Snare Room `vMh6SDID0XTrVJ0f1QmFD`, Overgrown Stores `5y9wAYELSdNa8Jgim1sgD`, Ore Vault `C1JPScsgSMcVXQUfuFgcs`, Bloom Cellar `UO65dN640MgAbNBBopTVI` |
| N15 Crownhold ("use a Lastlight Lantern") | `complete_specific_quest`; the Lantern is an entry item, consumed at the start, not "used", so winning Crownhold is the honest proxy | `fqqpkcp_L4oOsC6yyodlk` |
| Lastlight jutsu (Crownhold pick) | `use_specific_jutsu_combat` | `0F-68bxOXW_LkJnXV0lwT` |
| Skyglass Serum | `use_specific_item_combat` (counts in chart runs, never in the Wreck); confirm it is usable in battle before using it | `XhilCv1Hq4eNt-Wddok-m` |
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
**Window (D4):** 2026-11-06 00:00 UTC to 2026-11-09 00:00 UTC, with the release; it is hidden until published, so in
practice it opens at publish.

Reward rationale: every reward is an existing event item that feeds the next rung or the shared containers (P1), none
is a gate item (no Lantern, shard or Epic chart), and the page pays at most one Token and one Coffer a weekend, below
one Crownhold pick. The values are the director's (`[[D-reserved-dauntless]]`).

## 5. Rotation and template

**Rotation.** One quest record per weekend, `startsAt` the Friday, `endsAt` the Monday (the event runs Friday-Sunday,
RUL-2026-11-01-096 item 4), `maxCompletes: 1`, `retryDelay: none`. Last weekend's page expires on its own; the new page
is a new record ("Second Page", "Third Page"). Only one page is ever in its window, so only one can be taken. Pages are
reusable: an old page can return later as a new record with new dates.

| Page | Theme | Entries (sketch) |
|---|---|---|
| Second: "The Rotted Heading" | the rot | The Captain's Watch ×1; The Fall ×1; The Burning Heading ×1; The Rotted Reliquary ×1; drink a Skyglass Serum in a run ×1 |
| Third: "The Stores" | the Haul | any Haul run ×2; any Rare run ×2 (the pages drop there); a common run ×2 |
| Fourth: "Her Invitation" | the finale | an Epic or tainted run ×2 (Tide shard); a Haul run ×1 (Ledger); Crownhold ×1 (Crown); the Mother of Echoes ×1 as the stretch (the Keel shard's Wreck stays off, D1) |
| Fifth: "Every Deck" | a full tour | one entry per Rare run, ×1 each; raise the Lastlight in battle ×1 |

**Template for any event** (an event sheet adds this as part of item 9, legibility):
1. **The object:** what the page is in the world, who hands it over, why it lasts one weekend.
2. **Entries:** 4-7, from the event's trackable actions (section 2's list); every entry is a quest id set, a jutsu or
   an item use, or a location. Climb the ladder from the entry rung; the last entry is the stretch.
3. **Each entry's text:** one line in voice, then one plain line naming exactly what counts and its reward.
4. **The quest description** carries the whole page (voice lines, the numbered plain list, the rules: counts only
   while held, any order, claim before the weekend ends).
5. **Rewards:** event items only, nothing that is a gate or finale input, values set by the director.
6. **No per-page badge:** one badge for the whole event keeps it exclusive (D5).
7. **Checks:** no entry depends on a once-only quest, a dungeon, steeping's refund path, or "obtain"; every listed
   quest id is live; the page passes `validate.py` (ledgered win-node lint), `check_manifest`, the event's own check.

## 6. Landing: how players find the page (D2 proposal, for approval)

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

**Recommendation (the "weekend challenge pass"):**
1. Keep the dated `event` quest. It lands on the Information Board and, more importantly, as an Events card on every
   player's profile dashboard, with its own image, for exactly the weekend.
2. Make it read as a weekly pass where players see it first: a distinct page image (a torn log page with the bell
   mark; art request), and a card description whose first line is plain: "This weekend's orders: 5 to claim, a Skyglass
   Token for all five." The voice follows.
3. Point to it from the event's own entry points (text edits, built only on approval): Wreck Sighted's last line ("Each
   weekend I dry another page of their watch log. It will be on the Information Board."), and the same line on the
   salvager's Haul or chart rules text where it fits. Announce each page in the weekend post.
4. Later, if the director wants the page handed over at the Wreck: an `overworld` quest at a salvager placement.

## 7. Director decisions (RUL-2026-11-05-121)

| # | Decision |
|---|---|
| D1 | No Wreck tally. Wreck dungeon clears stay off the pages; the director asks upstream for dungeon-clear tracking |
| D2 | A dated quest, YES. The landing is section 6's proposal, awaiting approval |
| D3 | Week 1 rewards approved as drafted |
| D4 | Week 1 opens with the fight: Friday 2026-11-06, closing Monday 2026-11-09 (00:00 UTC both) |
| D5 | No badge per page; one badge for the whole event |
| D6 | The two validator diagnostics accepted; an ending players can see (section 4) |

## 8. Staff test before any publish

On a staff character, with push/490 run (hidden): take "The Watch Log: First Page"; reload; win a Low Tide Run. The
Logbook should show entry 2 at 1/2 (this confirms the chain is all live and counts in any order). Walk to sector 210:
entry 1 completes; claim it and receive the Tide Chart. Not yet checked: what the Logbook does with an expired page.
