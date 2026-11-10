# Stage 7: Build handoff

The sheet becomes a manifest and the job goes to the director as a go card.

## Steps

1. `design.py compile sheet.json -o push/NNN_name.json`. It refuses while anything is open and
   lists what.
2. Validate with the build skill: `validate.py`, zero errors, and say that it ran
   (`D-validate-always`). Any other gate the content needs is routed in `docs/00_INDEX.md`.
3. Write the go card in the repository's format: `docs/workflows/OPERATING_MODEL.md`
   section 2.

## Exit checklist

- [ ] The manifest came from `compile`, not from hand-written JSON.
- [ ] Everything ships hidden (`D-hidden-true`).
- [ ] Every remaining placeholder is listed on the card.
- [ ] The gates and their results are on the card.

## Decision for the director

"Go?" Nothing reaches the game without it (`D-user-pushes`).
