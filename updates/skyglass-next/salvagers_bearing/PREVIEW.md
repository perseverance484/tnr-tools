# Salvager's Bearing (working name): preview

Status: **crew hunt, delivered through the Wreck Sighted prerequisite (the director's follow-up, 2026-11-17 01:23Z),
validated, awaiting the director.** Nothing has been written to the game. Every live step waits for his typed go.
Earlier versions (a board order to the Wreck tile; a Friday hand-out to every logbook) are in git history.

## What the player sees

- **After finishing Wreck Sighted for their band:** Salvager's Bearing is on the Administration Building board every
  day of the weekend. They take it from there; once taken, the world map marks sector 210 until the third win.
- **Name:** Salvager's Bearing (working name), two copies: (Levels 30 to 80) and (Level 81 and up), matching the two
  Wreck Sighted copies.
- **Description:** The Quartermaster's crew have come ashore in sector 210. They walk the sand around the Skyglass
  Wrecks as if they were still on watch, and the salvager wants three of them put down before they strip the beach
  bare. **Beat 3 of the crew on the beach in sector 210.** Once a day, after Wreck Sighted. They fight at your level.
- **Orders, in order:**
  1. The Skyglass Wrecks lie in sector 210, and the crew walk the sand around them. Beat one. (1 of 3)
  2. Beat another of the crew on the beach in sector 210. (2 of 3)
  3. One more of the crew in sector 210. (3 of 3)
- **How a fight starts:** walk up to a wandering crew member on the beach and attack. While the quest is open, the
  fight is the quest's fight, scaled to the player's level.
- **Win:** "Three of the crew lie in the sand. The salvager will hear about it." Pays the reward.
- **Loss, flee or draw:** that try ends ("The crew drive you off the sand. Take it from the board again and go back.").
  A loss isn't a completion, so the daily limit doesn't block a second try.
- **Reward: proposed 3 Wreck Salvage a day** (the same pay as a Watch Log order and the proposed Short Rations).
  Fallback: 1,000 ryo.

## How it reaches players (pinned source TheNinjaRPG@94b585ea)

- **The prerequisite works as he described, with one difference:** it puts the quest on the board, not in the logbook.
  The Administration Building lists event quests the player can take right now, and that check includes the
  prerequisite, level, dates and the once-a-day limit (libs/quest/availability.ts 248-277). After each 6 PM Central
  reset it is back on the board for everyone who finished their Wreck Sighted. Nothing in the source drops a quest into
  logbooks because a prerequisite was met.
- **Two copies:** a quest has one prerequisite id, and Wreck Sighted is two quests (one per band), so the Bearing is two
  quests too, each tied to its band's Wreck Sighted.
- **Weekly:** Wreck Sighted is re-cloned every week with new ids, so each re-arm points the two Bearings at that week's
  copies.
- **Not the game's "daily" type:** the midnight daily hand-out picks one random daily per rank, village and level from
  all of them and never checks a prerequisite (api/daily-quest/route.ts 75-95).
- **Weekend close:** endsAt is Monday 6 PM Central. An expired or hidden quest drops off the board and stops advancing
  in any logbook it's open in (libs/quest.ts 59-73). The close step also hides both copies.
- **No under-30 spill:** the Friday hand-out version reached every active player by rank. This one reaches only players
  who finished Wreck Sighted, which already needs level 30.

## How it ships (each step waits for the director's go)

0. `salvagers_bearing_00_clone_plan.json`: clone the original Wreck Sighted twice. A clone of a hidden event stays a
   hidden event, so nobody gets it. Never Forge-create it: turning a new quest into an event hands it to every active
   player.
1. `salvagers_bearing_build`: edit both clones into the two Bearings, hidden, each needing its band's Wreck Sighted.
   **Needs the beach raider placements first** (each fight takes its opponent from one) and that weekend's two Wreck
   Sighted copies.
2. `salvagers_bearing_release`, Friday 6 PM Central: unhide both, with the Wreck Sighted copies.
3. `salvagers_bearing_close`, after Monday's close: hide both.
4. Each later week: regenerate step 1 with the new dates and that week's Wreck Sighted ids, run it hidden, then 2 and 3.

Regenerate with real ids: `python3 salvagers_bearing.gen.py --weekend 2026-11-21 --quest-low <id> --quest-high <id>
--ws-low <id> --ws-high <id> --crew <placement>` (one `--crew` for all three fights, or three for a mix).

## Checks

- `validate.py`: build 0 errors, 0 warnings; release and close 0 errors, 2 warnings each (partial hide/unhide edits,
  the same warning as `stolen_stores_pages/02_release_flips.json`).
- Each order has sector 210 and no hidden location, so the map marker shows once taken (layout/Map.tsx 73-95).
- `defeat_opponents` has no kill count, so "beat 3" is three orders. Each tied fight is one opponent
  (libs/overworldAi.ts 642-668), and completes only through its crew placement (libs/quest.ts 286-301).
- Lifetime cap: 100 starts per player per copy (the editor's maximum), about 30 weekends at a try a day. The live
  Salvager dailies carry the same cap.

## Open for the director

1. Reward: 3 Wreck Salvage, or 1,000 ryo.
2. Does this replace Short Rations? It is the same job: a beach-fight daily paying salvage.
3. The name.
4. Which crew it counts: any one crew placement, or a set mix.
5. Go for each step, once the raiders exist.

## Icon prompt (attach ref_style_skyglass_icons.png)

Salvager's Bearing. Game item icon in the same hand-painted style as the attached icons: a torn strip of weathered
sailcloth, loosely rolled, with three short scratched tally marks and a small arrowhead burned into it, a tarnished
brass compass needle tied to its corner with twine. A few pale cyan skyglass flecks in the weave; one faint green rot
stain at the frayed edge. Thick dark ink outlines, cel shading with a few highlight steps, weathered texture, cool
blue-black and sun-bleached canvas palette with one pale cyan accent. Single object, centered, small even margin,
square 1024x1024, transparent background. No readable text, letters or numbers, no UI, no frame, no surface or shadow,
no glow halo, no second object.
