# Salvager's Bearing: preview

Status: **built and validated, awaiting the director.** Nothing has been written to the game. Every live step below
waits for his typed go.

## What the player sees

On the Wake Island board (Administration Building), during the Wreck weekend only:

| | Shallows copy (levels 30 to 80) | 81+ copy (levels 81 to 100) |
| --- | --- | --- |
| Name | Salvager's Bearing (Shallows) | Salvager's Bearing |
| Description | The salvager has scratched a bearing on a strip of sailcloth: a line from wherever you stand to the beach where the Ghost Ship came down. Carry it, and your map will show you the way.<br><br>**Go to the Faded Skyglass Wreck in sector 210.** Once a day. | Same, ending **Go to the Skyglass Wreck in sector 210.** Once a day. |
| Objective (the director's words) | The Skyglass Wrecks lie in sector 210. Gather a crew of three and board. | Same |
| Goes to | sector 210, tile 7/1 (Faded Skyglass Wreck entrance) | sector 210, tile 21/6 (Skyglass Wreck entrance) |
| On arrival | "You stand in the shadow of the Faded Skyglass Wreck." | "You stand in the shadow of the Skyglass Wreck." |
| Reward | **Proposed: 1,000 ryo** (awaiting the director) | Same |

While the quest is active, the world map draws a marker on sector 210. Hovering it shows the quest name, "Travel" and
the objective line (2 lines max). The marker goes away once the player reaches the tile, since the order is done.

## Schedule

- Opens with the Wrecks: Friday 6 PM Central (startsAt Saturday, 00:00 UTC). Closes with them: Monday 6 PM Central
  (endsAt Tuesday, 00:00 UTC). First window in the build: 2026-11-21 to 2026-11-24 (weekend 3, Stolen Stores).
- Daily: once per UTC day (resets 6 PM Central), so up to 3 runs per weekend. Lifetime cap 100 attempts.
- Each later weekend needs a re-date edit (`--redate`). It fits beside the Friday Wreck window job (run_queue 515).
  The other way, one window from the first weekend to the event's end, would leave it on the board midweek, which
  breaks "nothing live midweek".

## How it ships (no step runs without the director's go)

1. STEP 0, live: `quests.clone` of the hidden event quest `jUQYz9zyMdJIRdLbucYjm` **twice** (one per band). A clone
   keeps questType event and hidden, and hands it to nobody. Building it fresh would bulk-assign it to every active
   player (pinned source, routers/quests.ts 990-1001).
2. Rerun `python3 salvagers_bearing.gen.py --weekend 2026-11-21 --id-shallows <A> --id-deep <B>` and validate.
3. Run the two edits. They land hidden.
4. Unhide at the Friday release with the rest of the weekend.

## Why two copies instead of one

The spec put both Wrecks side by side at 15/6 and 16/6 (docs/design/SKYGLASS_EVENT_MAP.md). The live dungeon records
(read 2026-11-16) put them far apart after the beach remake: Faded at 7/1, Skyglass at 21/6. One order can complete on
one tile only, so each band gets the Wreck it can enter. Both copies still light up sector 210. If the director wants
one quest, the fallback is a single 30-100 copy pointing at one Wreck.

## Checks

- `validate.py salvagers_bearing.TEMPLATE.json`: **0 errors, 3 warnings**, all reviewed:
  - "no win_quest node" (both copies): a one-objective consecutive quest completes when that objective is done
    (libs/objectives.ts 146-164), same as the live Salvager dailies.
  - "law 54: latitude 1 inside the 2-tile margin" (Shallows): 7/1 is where the live Faded Wreck entrance already
    sits and players reach it every weekend. Moving the order off that tile would mean it no longer completes at the
    door.
- maxAttempts: upstream allows unlimited (-1), but our contract (45d) has min 0, so it's 100, as on the dailies.

## Icon prompt (attach ref_style_skyglass_icons.png)

Salvager's Bearing. Game item icon in the same hand-painted style as the attached icons: a torn strip of weathered
sailcloth, loosely rolled, with one long scratched bearing line and a small arrowhead burned into it, a tarnished brass
compass needle tied to its corner with twine. A few pale cyan skyglass flecks in the weave; one faint green rot stain
at the frayed edge. Thick dark ink outlines, cel shading with a few highlight steps, weathered texture, cool blue-black
and sun-bleached canvas palette with one pale cyan accent. Single object, centered, small even margin, square
1024x1024, transparent background. No readable text, letters or numbers, no UI, no frame, no surface or shadow, no
glow halo, no second object.

Until the icon exists, the build reuses the Watch Log page icon.
