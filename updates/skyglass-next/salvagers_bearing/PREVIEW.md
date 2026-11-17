# Salvager's Bearing (working name): preview

Status: **redesigned to the director's crew-hunt idea (2026-11-17), validated, awaiting the director.** Nothing has been
written to the game. Every live step waits for his typed go. The first draft (one "go to the Wreck tile" order taken
from the Wake Island board) is replaced; it's in git history.

## What the player sees

- **Friday 6 PM Central, without visiting any board:** the quest is already in their logbook, and the world map marks
  sector 210. Hover shows "Salvager's Bearing", "Defeat" and the current order.
- **Name:** Salvager's Bearing (working name)
- **Description:** The Quartermaster's crew have come ashore in sector 210. They walk the sand around the Skyglass
  Wrecks as if they were still on watch, and the salvager wants three of them put down before they strip the beach
  bare. **Beat 3 of the crew on the beach in sector 210.** Once a day. They fight at your level.
- **Orders, in order:**
  1. The Skyglass Wrecks lie in sector 210, and the crew walk the sand around them. Beat one. (1 of 3)
  2. Beat another of the crew on the beach in sector 210. (2 of 3)
  3. One more of the crew in sector 210. (3 of 3)
- **How a fight starts:** walk up to a wandering crew member on the beach and attack. While the quest is open, the
  fight is the quest's fight, scaled to the player's level.
- **Win:** "Three of the crew lie in the sand. The salvager will hear about it." Pays the reward.
- **Loss, flee or draw:** today's try ends ("The crew drive you off the sand..."), same as the live Salvager dailies.
- **Reward: proposed 3 Wreck Salvage a day** (the same pay as a Watch Log order and the proposed Short Rations).
  Fallback: 1,000 ryo.
- **Levels:** 30 to 100. **One quest for both bands**, because the crew scale to the player and the Wreck tiles
  don't matter.

## How it reaches players (pinned source TheNinjaRPG@94b585ea)

- **Day one of each weekend, no board:** when a quest is turned into an event, the game hands it to every player
  active in the last 7 days whose rank fits (routers/quests.ts 990-1001). That's the signpost. It goes by rank, not
  level, so it **also lands in logbooks below level 30**. The level gate only stops people taking it from the board.
- **Days two and three:** players take it again from the Administration Building board. The source has no way to
  auto-hand an event quest out every day:
  - event quests can't come from an NPC (overworld NPC quests exclude events);
  - a true "daily" quest is one random pick a day from every visible daily in the game. There are 7 today, and only
    one for 81+, so ours would show up about half the days and push the other daily out on those days.
- **Daily limit:** once per day, resetting 6 PM Central, so up to 3 a weekend. Window 2026-11-21 to 2026-11-24 for
  weekend 3.

## How it ships (each step waits for the director's go)

0. **Needs the beach raiders first.** Each order is tied to a crew placement, and the game fills in the opponent from
   that placement when the quest saves. So the raider placements on 210 (Stolen Stores design, test placement still
   awaiting his go) must exist before step 1.
1. `salvagers_bearing_build`: create the quest **hidden, as a mission**, so saving hands it to nobody.
2. `salvagers_bearing_release`, at the Friday release:
   - edit A turns it into an **event at rank S, unhidden**, which hands it to everyone;
   - edit B re-saves it at rank D. Without that, only Jonin and up would see it on the board. A re-save doesn't hand
     it out again.
3. `salvagers_bearing_rearm` before each later Friday: back to mission, hidden, with the new dates. Then step 2 again.
   The event flip hands it out fresh, including to players who did it the week before.

Regenerate with real ids: `python3 salvagers_bearing.gen.py --weekend 2026-11-21 --quest <id> --crew <placement>`
(one `--crew` for all three fights, or three for a mix such as Deckhand, Blade, Mate).

## Checks

- `validate.py` on all three templates: **0 errors, 0 warnings.**
- Each order has sector 210 and no hidden location, so the map marker shows (layout/Map.tsx 73-95).
- `defeat_opponents` has no kill count, so "beat 3" is three orders. Each tied fight is one opponent
  (libs/overworldAi.ts 642-668). A tied order completes only through its crew placement, never by standing on its
  stored tile (libs/quest.ts 286-301). The stored tile is the Salvager's fire, 210 14/7.

## Open for the director

1. Reward: 3 Wreck Salvage, or 1,000 ryo.
2. Fine that the Friday hand-out also reaches players under 30?
3. Does this replace Short Rations? It is the same job: a beach-fight daily paying salvage.
4. The name.
5. Which crew it counts: any one crew placement, or a set mix.
6. Go for each step, once the raiders exist.

## Icon prompt (attach ref_style_skyglass_icons.png)

Salvager's Bearing. Game item icon in the same hand-painted style as the attached icons: a torn strip of weathered
sailcloth, loosely rolled, with three short scratched tally marks and a small arrowhead burned into it, a tarnished
brass compass needle tied to its corner with twine. A few pale cyan skyglass flecks in the weave; one faint green rot
stain at the frayed edge. Thick dark ink outlines, cel shading with a few highlight steps, weathered texture, cool
blue-black and sun-bleached canvas palette with one pale cyan accent. Single object, centered, small even margin,
square 1024x1024, transparent background. No readable text, letters or numbers, no UI, no frame, no surface or shadow,
no glow halo, no second object.
