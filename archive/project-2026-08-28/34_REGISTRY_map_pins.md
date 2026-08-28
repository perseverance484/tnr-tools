> **STALE - archived 2026-08-28 (rollout Stage 1).** working copy is 34b_DATA_pins.json in skill data/.
> Do not build from this file.

# Shared map pin library

## Why

Node `image` is the sector map pin (`libs/threejs/sector.ts` drawQuest). No image means no pin at all, so every quest that wants map guidance has been inventing one-off art. That is backwards: a pin is UI, not story. Players should learn a small fixed vocabulary of pins and read any mission at a glance, the way they already read the task badges.

## What the engine gives us for free

The renderer already tints the marker behind the icon by task:

| task | marker tint |
|---|---|
| move_to_location | yellow |
| collect_item, deliver_item | purple |
| defeat_opponents | red |
| dialog | purple |

So pins must not carry meaning through colour, the marker already does that. Pins carry the **verb**. They are drawn small through an alpha mask, so they need bold silhouettes and almost no interior detail.

## The mechanic that makes this worth doing

`collect_item` supports `collect_time_minutes` (0 to 60): the player stands on the tile and the objective completes after the timer, with the message "You started collecting. This will take X minutes." Nothing else in the task vocabulary is timed. That means a pin can promise a duration, and the promise is enforced by the engine.

## Proposed library, 11 pins

Standard durations are conventions we enforce by always pairing the pin with the same `collect_time_minutes`. Instant means the objective resolves on arrival.

| pin | task | collect_time_minutes | felt duration | used for |
|---|---|---|---|---|
| Travel | move_to_location | n/a | instant | go here, nothing else |
| Search | collect_item | 0.2 | 12 sec | look for something in place: tracks, signs, a hidden thing |
| Gather | collect_item | 0.25 | 15 sec | pick, cut, draw water, harvest |
| Repair | collect_item | 0.4 | 24 sec | fix, mend, shore up |
| Dig | collect_item | 0.5 | 30 sec | excavate, unbury, break ground |
| Watch | collect_item | 0.5 | 30 sec | stand a post, observe, wait out a patrol |
| Deliver | deliver_item | n/a | instant | hand over what you carry |
| Fight | defeat_opponents | n/a | instant | someone is here and will not |
| Climb | collect_item | 0.3 | 18 sec | scale a wall, crawl a duct, squeeze through |
| Pick | collect_item | 0.2 | 12 sec | locks, seals, wired drawers |
| Listen | collect_item | 0.15 | 9 sec | eavesdrop, wait out a patrol |

Nothing over 30 seconds. `collect_time_minutes` is a float (`z.coerce.number().min(0).max(60)`, no integer constraint) and the engine compares `secondsPassed / 60` against it, so 0.1 is 6 seconds and the scale is ours to use.

Two engine notes before we commit:
- The notification prints the raw value: "This will take 0.5 minutes." Ugly but harmless. A one line source fix could render seconds under a minute; worth a PR alongside the trainer leak fix.
- Completion is evaluated on a quest check, not a timer callback. Test whether a 12 second wait resolves on its own or needs the player to move off and back on. If it needs a nudge, floor the set at whatever actually self-resolves.

Eleven covers every mission we have shipped or earmarked. Anything that does not fit is a signal the objective is unusual enough to deserve bespoke art.

## Style spec

- Square, 256 px, JPG, dark neutral background so the mask reads cleanly
- One object, centred, filling roughly 70 percent of the frame
- Heavy silhouette, two or three values, no fine texture, no text
- Cool neutral palette with a single warm accent, so pins sit on any village skin without clashing
- Test at 40 px before approving: if the verb is not readable, redraw

## Naming and storage

Folder `pins`, names `Pin Travel`, `Pin Search`, `Pin Dig`, and so on. Ids go in the registry so any manifest can reference them without a lookup. One record per pin, reused across every mission in the game.

## Cost

Ten generations once, then zero per mission forever. Compare with the current path, which is two bespoke pins for One White Ear alone.

## Open questions

1. Are the durations right? Search 12s, Gather 15s, Repair 24s, Dig 30s, Watch 30s.
2. Does a 12 second wait self-resolve, or does the player need to re-enter the tile?
3. Should Shrine exist, or is it just Travel with different flavour text?
4. Do we add Escort or Track later, or keep the set at ten until a mission actually needs more?

Dialog nodes and plain shrine visits take no pin: dialog draws no map marker worth guiding to, and a shrine visit is a Travel.
