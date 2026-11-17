# Skyglass next update: everything in one place

The next Skyglass weekend is **weekend 3, Stolen Stores**, releasing **Friday 2026-11-20, 6 PM Central**. Weeks 2 and 3
of the run (the Stolen Stores twist, Her Invitation) and the Mother of Echoes finale follow. This folder is the one
place to see, review and add to that work.

Rules for this folder:

- **Nothing here is live, and nothing here is approved unless its row says so.** Every live write (Forge run,
  connector write, map publish, Discord post) waits for the director's typed go.
- Files copied in from the shared project folder are the working copies from now on; the originals stay where they
  were as of the date shown. Repo files that already have a home (`push/`, `docs/design/`, `state/`) are linked, not
  copied, so there is one copy to edit.
- Claude Docs stay canonical for the design docs (they are edited in place); `designs/` holds a dated snapshot only.
- Add a piece by adding a row below and a folder or file beside this README. Keep the status column honest.

Status words: **approved** (director said yes), **awaiting director** (built or written, needs his decision or go),
**draft** (still being worked), **live** (in the game already, listed for reference).

## Index

| # | Piece | Status | Where | Open decisions |
| --- | --- | --- | --- | --- |
| 1 | **Wreck signpost in the Watch Log page descriptions**: one bold line under each page's hook, "The Faded Skyglass Wreck is in sector 210, tile 7, 1." (30-80 page) and "The Skyglass Wreck is in sector 210, tile 21, 6." (81+ page). The Logbook shows a held page's description under "Read briefing" all weekend (director's direction Nov 17 01:39Z and 01:46Z) | awaiting director | built into `stolen_stores_pages/` (`stolen_stores_band.gen.py`, `01_stolen_stores_band_build.json`) | the wording; a map marker is held back (a travel step marks the map only until arrival); later pages (Her Invitation, push/519) need the same line |
| 2 | **"Sector 210" text lines** for Wreck Salvage and chart items (the Watch Log line is now built into row 1) | awaiting director | `TEXT_ADDITIONS.md` | which lines to ship; drop the chart line? |
| 3 | **Discord patch notes**, weekend 3 | draft | `PATCH_NOTES.md` | ⏳ lines follow the decisions in rows 5, 8 and 10 |
| 4 | **Stolen Stores Watch Log pages + Wreck Sighted copies** (81+ page, new 30-80 page, two Wreck Sighted copies, Wreck gate repoint; now carry the row 1 signpost) | awaiting director (built Nov 14, not run) | `stolen_stores_pages/` (copied from project files `tnr/manifests/skyglass_nov20/`, Nov 14); repo push/517-518, `state/skyglass_schedule.json`, `docs/design/EVENT_JOURNAL.md` §5 | run the flips Wednesday or Friday; gate repoint by connector direct save (Forge refuses dungeons); the 30-80 challenge mix. `TUNING_PROPOSAL.md` there was **rejected** Nov 14 ("Nah, none of that"), kept for reference only |
| 5 | **Stolen Stores full update design** (beach raiders as hostile AI, The Quartermaster's Stores run + the Mascot, Short Rations, the Fire's "This weekend" topic, 10 art prompts) | awaiting director | Claude Doc "Stolen Stores: full update design" https://claude.ai/artifact/AZZtxsZahaubm2rwiC3cva (snapshot `designs/stolen_stores_full_update.rev15.snapshot.md`); "Skyglass patch 3: direction" https://claude.ai/artifact/Q2DqHZmxQiAvpGkiLubfzh | test placement go; Short Rations home; numbers; reward found below; chart hand-out; 81+ page swap; beach publish; names (8 decisions, listed in the doc) |
| 6 | **Weeks 2-3 design** (Stolen Stores twist, Her Invitation, the Quartermaster ~10k HP, "Your Own Voice" echoes) | draft | Claude Doc https://claude.ai/artifact/9sAvsEiubZRbe3kkcJkFTx (rev 26) | chart hand-out via Wreck Sighted; Her Invitation #5 (MoE win vs 5 dailies); names |
| 7 | **Her Invitation**, Watch Log page 4 | awaiting director | push/519 (created hidden, `I_cEOGSfFuahaJlR3FnWC`), push/520 (publish); run_queue 520 | go; its orders carry no "3 Wreck Salvage" unlike pages 2-3 |
| 8 | **Sector 210 beach remake** (Tiled hex) | awaiting director (draft saved, not published) | `map210/` (v7 JSON + build/render scripts, copied from project files `tnr/map210/`, Nov 16); live draft `sJNdkYbBy6YGBsYTzvOIg` v6; prop uploads on branch `duet/moe-uploadthing` | publish (replaces the live map); ocean-tile spawn/pools check; sand reads as desert arena |
| 9 | **Heist chart** (Captain's Strongroom, ~82 nodes) | draft | Claude Doc https://claude.ai/artifact/WATfkMGAZB7npFZxqRH6YK (rev 9) | crew trio; band (clashes with epic+ = 81+); grand prize; Watch Log challenge; chart expiry |
| 10 | **Wreck fixes from PvP + event data** | partly live | Claude Doc https://claude.ai/artifact/RfkoFELCR6VtYdUj3JJs1p; Maw one-hit KO live Nov 16 (project files `tnr/manifests/skyglass_maw_ko/`, rollback in its README) | reflect-stance animation ("not yet"); Faded patch line for 30-80; solo boss clear before release |
| 11 | **Mother of Echoes finale** | live (design records) | `docs/design/MOTHER_OF_ECHOES_*.md` | the shards topic is held back (RUL-2026-11-09-140) |
| 12 | **Weekly jobs**: Friday Wreck window, weekly Lantern trade copy | live, recurring | run_queue 515, 595 | |
| 13 | **Art prompts**: raider/Quartermaster (in the doc, #5), page icons (`stolen_stores_pages/README.md`), wreck props (done) | awaiting art | as listed; older icon prompts `tnr/art/prompt_refs/skyglass_icon_prompts_v1.md`; structure prompts `docs/handoffs/SKYGLASS_WRECK_STRUCTURE_ART_SESSION_PROMPTS.md` | where reference 1 for the props comes from |

## Dropped

- **Salvager's Bearing** (a daily signpost quest; versions: a board order to the Wreck tile, a 3-fight crew hunt handed
  to every logbook at release, then a daily unlocked by Wreck Sighted). Dropped Nov 17 01:39Z: the director's word was
  "that doesnt solve anything. I want something that clearly indicates where the wreck is." A board daily only points
  the way after a player has found the board and taken it, and the source has no way to put a fresh quest in every
  logbook each day. The Watch Log pages already sit in the logbook all weekend, so their descriptions carry the signpost (row 1). The
  Bearing's files are in this branch's git history (`updates/skyglass-next/salvagers_bearing/`, commit 5c918d30).

## Source contradictions found while gathering

- **Wreck tiles.** `docs/design/SKYGLASS_EVENT_MAP.md` (N1/N2), push/366 and `push/skyglass_wreck.gen.py` say 16/6 and
  15/6. The live dungeons (read 2026-11-16), the live Wreck Sighted text (push/615) and the beach build (`map210/build3.py`)
  say Faded **7/1**, Skyglass **21/6**. The live tiles win; the design doc is pre-remake history. The row 1 signpost names the live tiles; both read as walkable on the live sector 210
  map (worldMap.getSectorWindow, 2026-11-17).
- **Maw of the Deep.** The design doc's Discord draft says the Maw "hits for a fixed amount"; it has been a one-hit KO
  on all five Core Horrors since Nov 16.
- **Faded band.** The Faded Wreck's push/366 description says "For level 45 and up"; the band is 30-80. The live
  description no longer says it (live read 2026-11-16), so only the old manifest is stale.
- **Mother of Echoes.** run_queue rows 477/597 still read "waiting", but MoE is live.

## Gates run for this folder

- `skills/building-tnr-content/scripts/validate.py` on `stolen_stores_pages/01_stolen_stores_band_build.json`: 0 errors,
  2 warnings, both there before the signpost (the pages have no win/fail node; they finish when every step is done).
- `scripts/check_no_real_name.py`: 0 hits in this folder (copied files had the old name in notes; replaced with "the director"). The check still reports 6 older hits elsewhere on main.
