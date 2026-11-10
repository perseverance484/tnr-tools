# Stage 9: Live verification

After the director's go and the run, check that what is live is what was designed.

## What to check

- The records read back as built: a push echo is not a read-back (`D-push-echo`).
- One fight, watched: the opener, each telegraph and its payoff, each phase cue, the enrage.
- The picture, at real size, once on a cold cache (`docs/workflows/OPERATING_MODEL.md`
  section 6).

Live reads go through the director's connector under the run lock; this skill makes none on
its own. The read recipes belong to the build skill.

## Exit checklist

- [ ] Every difference between the sheet and what is live is written down.
- [ ] Each finding names its owner: the sheet, a library entry, a build tool, or an engine
      behaviour to record as a law.
- [ ] The sheet is corrected first, then rebuilt; a live record is never the only place a fix
      exists.
