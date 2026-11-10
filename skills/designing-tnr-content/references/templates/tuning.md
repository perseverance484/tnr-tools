# Stage 5: Tuning

Numbers meet the design here, and the numbers are the director's.

## What to do

1. Fast checks first, no simulation: damage maths with the build skill's `calc.py`, the rule
   count, distance gates (engine law 40), and that no rule depends on an effect landing the
   round it is cast (engine law 75).
2. State the calibration anchor: the declared loadout the numbers are tuned against (engine
   law 13).
3. Put each target in `tuning.targets` with its source, or leave it `AWAITING_RULING`. Report
   what was measured beside it. Never report pass or fail against a target nobody ruled.
4. Check every payout against its owner. Currency is a reward package or a slot
   (`references/sheet.md` section 6).

## Exit checklist

- [ ] The anchor is written in the design doc.
- [ ] Every target has a source or is a slot.
- [ ] Measured results are reported as measured, with how they were measured.
- [ ] Gaps between result and target are listed, not tuned away silently.

## Decision for the director

One card per target that has no ruling, with the measured value and two or three options.
