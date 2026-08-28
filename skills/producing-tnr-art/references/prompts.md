# Prompt scaffolds and generator failure modes

> Rewritten 2026-08-26 against `25x_DATA_art_spec.json`. Every number, aspect, format and byte
> ceiling lives in the spec; this file cites it and never restates it. The painterly clause that
> section 2.0 flagged as a contradiction has been **deleted** from every scaffold rather than
> reworded, because a struck clause that survives anywhere gets copied forward.

## 1. Production contract

One asset per generation. Never generate asset sheets, grids, multi-panel layouts, concept
boards, labelled collections, UI cards, or images containing text unless asked.

Generate one, QC it, process it, show it, wait. Batch generation feels faster and is not: a
systematic prompt fault gets baked into eight images before anyone looks, and regenerating eight
costs more than checking one.

### Raw QC, before processing

Processing a bad generation wastes the processing. Check first and state the failure in one line
rather than salvaging:

- Correct mode and aspect for the type (`spec.targets.<TYPE>.aspect`).
- No text, labels, watermarks, UI, panels, borders or grids.
- No extra characters unless the subject requires them.
- Backgrounds contain no people, characters or creatures.
- Keyed subjects sit on a true solid flat chroma field covering the whole canvas: not
  transparent, not a checkerboard preview, no shadow cast onto the key.
- Icons are complete single square images, not crops from a sheet.

**No franchise insignia, ever.** No forehead protectors, village headbands, clan symbols or
real-world logos. Generic masks, wraps, hoods and blank plates only, carrying no symbols.

Two failures are unprocessable and need a regeneration, not a repair. Both are in
`spec.chroma.unprocessable` with the mechanism:

- **Painted glow blocks.** A solid pale disc rendered as "glow" is art in the subject's own
  palette. Keying it eats content.
- **A subject resting on a surface.** Nothing to key, and it cannot be composited onto any other
  background.

---

## 2. House style

**`spec.house_style` is the authority.** Read it and paste its clauses; do not paraphrase them
into a prompt, because a paraphrase is how the painterly clause got in.

Ratified 2026-08-26 as **painted figures with pixel discipline**, measured across seven
exemplars (median value 0.13, 81% of pixels under 0.25 value, median saturation 0.20, soft-edge
share under 5%). The five load-bearing clauses are `rendering`, `lighting`, `camera`,
`silhouette` and `accent` in that block.

**Struck, permanently: "smooth painterly shading" and "rim lighting".** They contradict flat cel
shading and appear in none of the seven exemplars. `spec.house_style.struck_clauses` records
them so they are not re-derived from an old file. If either phrase turns up in a scaffold, it is
a regression.

Rejected registers and the four policy defects needing regeneration regardless of register are
in `spec.house_style.rejected_registers` and `spec.house_style.policy_defects`.

---

## 3. Scaffolds

**The scaffolds are no longer here.** They live in `spec.prompt_scaffolds`, one entry per
target, and `shotlist.py` renders them: `[STYLE]` expands from `spec.house_style.clauses`
verbatim, scoped per target by `spec.prompt_scaffolds.style_clause_scope`, and `[SUBJECT]` is
the only slot a human fills.

They were moved for the reason section 2 gives about the painterly clause. Ratified wording
kept in two places is ratified wording that will diverge, and the copy a generator actually
receives is the one that matters. A file that restates a scaffold is a file that will be edited
without the spec being edited.

To see a rendered prompt, ask the tool rather than reading a scaffold:

```
python3 shotlist.py quest_capture.json          # every shot, prompt included
python3 mission.py sheet.json --spec 25x_DATA_art_spec.json
```

`mission.py` additionally raises an `AI_AVATAR` shot per roster enemy, because an enemy is not
in the quest graph - the graph holds only its id - so the avatar would otherwise have no shot
and drift into a different register from the scene art beside it.

What each target still needs a human to know, none of it restated from the spec:

- **`SCENE_CHARACTER`** - framing picks the aspect, and that is a content decision the tool
  cannot make. Full body reads as a standing figure, bust to waist as a portrait. Pass
  `frame`. The client width-scales and never letterboxes, so a wrong choice makes the figure
  short rather than distorted, and the asset-editor preview lies about it either way
  (`spec.targets.SCENE_CHARACTER.editor_preview_warning`).
- **`SCENE_BACKGROUND`** - the lower left is reserved because the scene character lands there,
  and the exposure band is measured, not judged. Both are in the target block.
- **`ICON`** - lock the style on the first approved icon and generate the rest to match. Short
  concrete prompts beat long ones; after three failed blind re-descriptions switch to
  reference-image prompting rather than writing a fourth.
- **`STATIC`** - 50px inside a circular alpha mask over an engine-tinted plate. Colour cannot
  carry meaning and the corners are discarded. Silhouette only.

---

## 4. Glow, and why the negatives lead with it

Generators paint the key colour into subjects. The keyer's stage-1 flood crosses **diluted** key
pixels as well as pure ones, so a glow that bridges from the subject out to the background is
reached by the flood and keyed away with it. That is not a bug to route around: a glow touching
the background is indistinguishable from spill.

Hence three prompt rules, all of which have to be in the prompt rather than fixed afterwards:

- **Glow is rim light on edges only.** Lead the negative block with auras, halos, light fields
  and discs.
- **Enclosed spaces must be explicitly the key colour**, or a ring interior comes back grey and
  cannot be told from the subject.
- **One accent, restrained.** Two glow sources is the fastest route to a bridged glow.

---

## 5. Candidate lock register

When dauntless approves an image ("perfect", "A", "this set", "use this"), mark that processed file
LOCKED immediately. Do not replace a locked asset later unless he asks to swap or regenerate it.
If only one valid candidate exists, it is the default final. Show only valid candidates; skip
raw, failed and sheet images; never ask him to re-choose assets he already locked.

---

## 6. Production order

Order exists to stop two specific drifts: a late quest-icon correction, and a jutsu-icon style
swap after half the set is done.

1. Quest icon, to establish the visual brand.
2. One character prototype, to establish rendering.
3. Remaining characters, one at a time.
4. Scene characters, generated from the locked character identity.
5. Scene backgrounds, one at a time, strict no-character check.
6. Two item or jutsu icons, to lock the icon style.
7. Remaining icons in the locked style.
8. Map pins.
9. Package.

**The shot list is generated, not authored.** `scripts/shotlist.py <quest-capture>` reads the
quest graph and emits every asset it needs with its exact aspect, minimum width, format, byte
ceiling, filename and `@img` ref. Hand-authoring that list is where assets go missing, land at
the wrong aspect, or get a filename the manifest does not reference.
