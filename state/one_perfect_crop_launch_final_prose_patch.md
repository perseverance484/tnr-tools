# One Perfect Crop — launch-final prose patch

**Status:** QUEUED FOR `launch.finalization`; do not apply as a separate hidden-core hotfix.  
**Recorded:** 2026-09-23  
**Scope:** G1 and G4 wording only. Graph edges, objective IDs, battle routing, rewards, art, and all other prose remain unchanged unless separately approved.

## Director-approved intent

### G1 — The Cart

The choice must feel like **taking time to repair the cart properly** versus **sacrificing the cart to keep moving immediately**.

Do not frame the repair as obviously safer for the cabbages. The consequence of the repair branch is the **time spent**, which causes the later missed crossing.

Queued draft:

```text
G1 — The Cart

"I can repair the wheel properly, but it will take time."

<Ittetsu checks the broken rim, then the road ahead. The cart can be made sound again if you stop here and do the job right. Or the good timber can be stripped down into a rough drag-sled and the shipment can start moving immediately.>

Choices:
- Strip it down. We keep moving.
- Take the time to repair it properly.
```

Queued G1 PASS draft:

```text
G1 PASS — Sacrifice the Cart

<Ittetsu breaks down the damaged wheel, using the sound timber and ironwork to brace a crude sled. It is ugly, but it is ready now.>

"Good enough."

"We can replace a cart. We cannot replace the hours."
```

Queued F1.1 setup draft:

```text
F1.1 — A Proper Repair

<Ittetsu works carefully. By the time the wheel is straight and the axle turns cleanly, the cart is in excellent shape again.>

"There. That will hold."

<The repair is good. The day, however, has kept moving.>
```

The existing F1.2 missed-crossing consequence remains the structural payoff.

## G4 — The Perfect Cabbage

Ittetsu must react more strongly when the perfect cabbage rolls away so the player is genuinely tempted to chase it.

The intended distinction is **one exceptional cabbage versus the entire harvest**. The shifting load and slipping rope are the clue that chasing the cabbage risks everything else. Ittetsu may hate losing it while still recognizing that one cabbage is not worth the crop.

Queued draft:

```text
G4 — The Perfect Cabbage

<The market road is finally visible ahead when one side restraint snaps loose. A single flawless cabbage slips free, bounces once, and begins rolling toward the irrigation ditch below.>

Ittetsu freezes.

"No—no, not that one."

<For the first time all day, real alarm enters his voice.>

"That was the best head in the whole harvest."

<Behind you, the main load shifts with a long wooden creak. One of the remaining ropes is sliding steadily through its knot. Nothing else has fallen yet.>

Ittetsu looks from the runaway cabbage to the load.

"...Damn it."

Choices:
- Hold the load.
- Go after the cabbage.
```

Queued G4 PASS draft:

```text
G4 PASS — Hold the Shipment

<You seize the slipping rope and haul the main load back into place. Below, the perfect cabbage rolls through the grass and disappears into the irrigation ditch.>

Ittetsu watches it go.

"...That was a beautiful cabbage."

<He tightens the rope beside you, still staring downhill.>

"But one cabbage is not a harvest."

"Keep moving."
```

## Final-manifest application rule

When `launch.finalization` builds the final quest edit:

1. apply only the approved G1/G4 prose and choice-label deltas from this packet;
2. preserve all current objective IDs and edges;
3. preserve all four decision gates and sealed failure wings;
4. preserve Road Bandit as F2-wing-only content;
5. preserve Harvest Boar as the mandatory success-route battle;
6. structurally diff the final quest against the hidden-core live/readback graph so no unrelated prose or routing drift is introduced.
