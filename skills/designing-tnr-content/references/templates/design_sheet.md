# Stage 3: Design sheet

The machine-readable design. `references/sheet.md` explains every block.

## Steps

1. `design.py new <kind> --id <slug> --title "<name>" -o sheet.json`
2. Fill the kind's block. Name behaviour, structure and loadouts by library id; give kits as
   pool codes; give levels and roles, never stats.
3. Leave every undecided value as its slot word. Add a `decisions` entry for each question the
   director must answer, with real options.
4. `design.py check sheet.json` until there are no errors.
5. `design.py explain sheet.json -o design.md` and read the generated doc as the director will.

## Exit checklist

- [ ] `check` reports 0 errors.
- [ ] Every open slot is one the director must fill, not one you could have filled from an
      owner.
- [ ] Every number in `payout` and `tuning` carries its source, or is a reward package, or is a
      slot.
- [ ] Every enemy has a combat role (for the designer) and a tactical read (for the player).
- [ ] The generated design doc was read end to end.

## Decision for the director

The design doc, with its open slots and decision cards. Nothing is compiled until they are
closed.
