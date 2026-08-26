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

Fill `<...>` from the design sheet. Keep the negative blocks: they are doing more work than the
positive ones. `[STYLE]` means paste the five clauses from `spec.house_style.clauses` verbatim.

### 3a. Battle sprite / AI avatar
Target `AI_AVATAR`. Exports square, because the avatar box has no `object-fit` and stretches
anything else.

`single ninja character, full body, dynamic combat stance, [STYLE], one restrained elemental glow accent as rim light on edges only, centered, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard, no shadow cast onto the green`

`SUBJECT: <enemy description + element>`

`NEGATIVE: no text, no UI, no watermark, no chibi, no blur, no soft pastel, no muddy dither, no background scenery, no aura, no halo, no light field, no glow disc, no lime spill on the character, no multiple characters, no checkerboard background, no transparent-preview background, no white or grey background, no gradient green, no asset sheet, no grid, no labels, no franchise insignia, no desk, no table, no furniture, no props, nothing resting on a surface`

### 3b. Scene character
Target `SCENE_CHARACTER`. **Framing picks the aspect** - read
`spec.targets.SCENE_CHARACTER.aspect` before prompting, and read the `render` block once so the
reason sticks:

- **Full body → 2:3.** Stands at ~90% of scene height.
- **Bust to waist → 1:1.** Reads at 60% of scene height, which is right for a portrait.

The client width-scales these and never letterboxes them, so a wrong aspect makes the figure
**short, not distorted**. And never judge one by the asset-editor preview: that preview goes
through `AvatarImage`, which is `aspect-square` with no `object-fit`, so a correct 2:3 file is
genuinely stretched there and nowhere else. See
`spec.targets.SCENE_CHARACTER.editor_preview_warning`.

Full body:

`single ninja character, full body standing figure, head to feet visible, 2:3 portrait canvas, calm but intimidating characterful pose, [STYLE], one restrained elemental glow accent as rim light on edges only, centered, on a true solid flat lime-green chroma key background (#00FF00), not transparent, not checkerboard`

Bust:

`single ninja character, BUST-TO-WAIST PORTRAIT ONLY, square canvas, head shoulders and torso visible, no legs or feet, calm but intimidating characterful pose, facing 3/4 or slightly forward, [STYLE], one restrained elemental glow accent as rim light on edges only, centered, on a true solid flat lime-green chroma key background (#00FF00), not transparent, not checkerboard`

`SUBJECT: <character description + element>`

`NEGATIVE: no text, no UI, no watermark, no chibi, no blur, no soft pastel, no muddy dither, no background scenery, no aura, no halo, no light field, no glow disc, no lime spill, no multiple characters, no checkerboard background, no transparent-preview background, no asset sheet, no grid, no labels, no franchise insignia, no desk, no table, no furniture, no props, nothing resting on a surface, no low camera angle, no foreshortening`

Costume grammar and the headband ban: `spec.house_style.costume_grammar` and `hard_negatives`.

### 3c. Scene background
Target `SCENE_BACKGROUND`. Exactly 3:2 - this one **is** stretched by the client, because
`aspect-3/2` sits on the `<img>` with no `object-fit`.

`wide game scene background, <location + motifs + palette>, [STYLE], atmospheric depth, foreground lower left kept open and unobstructed, no characters`

`NEGATIVE: no people, no characters, no creatures, no character panels, no asset sheet, no grid, no collage, no UI frame, no text, no labels, no watermark`

Two rules with mechanisms behind them, both in `spec.targets.SCENE_BACKGROUND`:

- **Reserve the lower left.** The scene character renders at `absolute bottom-0 w-2/5` with no
  horizontal offset, so it lands bottom-left over the left 40%. Prompt it or the character sits
  on the subject.
- **Match the set's exposure band.** Measure median luma and the share under 20 against the live
  anchors before accepting. A generation that comes back a black rectangle needs a shadow lift,
  not a redraw: gamma 0.75–0.82 opens the shadows without blowing the light source. Numbers and
  the reject threshold: `spec.targets.SCENE_BACKGROUND.exposure_band`.

### 3d. Item and jutsu icon
Target `ICON`. Square, with a small margin so the rarity frame behind it reads.

`open square pixel-art <subject> icon, <colours + motion>, [STYLE], dark background, strong readable silhouette, no frame, no text`

`NEGATIVE: no asset sheet, no grid, no circular medal frame unless asked, no labels, no title text, no UI caption, no multiple icons, no franchise insignia`

Lock the style on the first approved icon and generate the rest to match. **Short concrete
prompts beat long multi-clause ones.** The generator reliably produces holdable objects and
reliably fails on packaging formats, phenomena and amorphous material chunks. After three failed
blind re-descriptions, switch to reference-image prompting rather than writing a fourth.

### 3e. Map pin
Target `STATIC`. The hardest constraint in the set and the least obvious:
`spec.targets.STATIC.design_rule`.

It renders at **50px inside a circular alpha mask**, over a plate the engine already tints by
task. So colour cannot carry meaning and the corners are thrown away. Silhouette only.

`single centered emblem, <object>, [STYLE], bold simple silhouette readable at very small size, thick forms, no thin lines, no interior detail, no text, on a true solid flat lime-green chroma key background (#00FF00)`

`NEGATIVE: no text, no labels, no frame, no border, no fine detail, no thin lines, no gradient, no scene, no background, no multiple objects, no franchise insignia`

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

When Brandon approves an image ("perfect", "A", "this set", "use this"), mark that processed file
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
