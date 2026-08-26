# Quest tier budgets and the D-mission template

## Observed template (our 13 shipped D-missions)

Median 4 nodes, exactly 1 dialog, 1 to 2 scene characters, 2 backgrounds, 0 to 2 travel stops, zero branches. Shapes in use:

- **Errand:** dialog, move, collect, win (Well Rounds, Cartographer pair, Misfiled Board)
- **Rounds:** dialog, move, move, collect, win (Lantern Rounds, Runaway Goat)
- **Contract fight:** dialog, defeat_opponents, reset_quest, win (Night Watch Shadow, Poachers' Due, Case Contract Intercept and Site Sweep)

Rewards are flat per tier: exp 173, ryo 1100, tokens 100, prestige 14, clan 100, with the Case Contracts adding an item drop group.

## Node budgets [RETIRED 2026-08-26]

The table that used to sit here (D 10 / C 15 / B 20 / A 20+) was a ballpark estimate written before the new
missions existed, and shipped work immediately broke it: Copies, Not Thefts is 25 nodes at B, Witness Detail
is 21, while the D set runs 3 to 6 against a nominal cap of 10. D missions come in well under, B missions run
over. Ruling: **node count is not a constraint.** A mission is as large as its idea needs.

New bands will be derived from shipped data once there are four or five B builds to average, not estimated
again. Until then the only structural rules are the counting rule below and the quality bar.

Counting rule: every node in `objectives` counts, including `reset_quest` and the `win_quest` terminator. A
`reset_quest` node carrying `resetObjectiveId` rewinds the tracker to that objective. Branch nodes count once
each, so a two-way choice that merges costs two nodes, not one.

## Quality bar, independent of size

Node count is the budget, not the goal. Within any tier:

- Every dialog beat carries voice, not instructions. "Fetch the thing" is a task line, not a scene.
- Travel legs exist because the story moves, never to pad the count.
- Art per quest: at least one scene character and one background, ideally a background change when the location changes.
- A branch is worth a node only when the choices read differently. Two flavors of yes is filler.
- Rewards stay at the tier's flat scale unless ruled otherwise.

## Client display laws (learned in play, 2026-08-24)

- `reset_quest` and `win_quest` descriptions are **never shown**. Both need a dialog node immediately before them: one to tell the player the choice was wrong before the rewind, one to play the payoff before the quest closes.
- Only one scene character renders per node. Multiple entries stack at the same position.
- Node-level `image` is the **sector map pin art** (`libs/threejs/sector.ts` drawQuest). No image means no pin. The pin is tinted by task: travel yellow, collect and deliver purple, defeat red, dialog purple.
- A scene character's apparent size is its share of its own canvas. Small subjects need transparent padding or they render at human scale.

## Art doctrine (ratified 2026-08-24)

**Village neutral by default.** No more village-restricted scene art. A village quest uses interiors and neutral exteriors that could belong to any village: mission counters, offices, archives, storerooms, corridors, courtyards seen tight. Avoid climate extremes in anything a player might see from more than one village.

Outdoor illustration with real character is saved for **global map travel**, away from the village, where the location is genuinely somewhere specific.

The Hyorin set (Village Street, Outskirts, Hollow Pine, Elder Yukino, Mochi) stays in use for One White Ear, but no further village skins get produced. The village art system plan is superseded.
