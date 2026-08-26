---
name: producing-tnr-art
description: Generates and processes pixel art for The Ninja RPG (TNR) - item and jutsu icons, AI avatars, scene backgrounds and scene characters - including prompt scaffolds, chroma keying, alpha cleanup, aspect-ratio padding and pre-upload QC. Use this skill whenever the user asks for an icon, avatar, sprite, portrait or scene asset, uploads generated art for processing, or mentions chroma, keying, transparency, spill, the image picker or the upload byte ceiling, even if they do not mention art directly.
---

# Producing TNR art

Art for TNR is generated externally, processed here, and uploaded through the builder as `@img`
references. This is a different working mode from building content: no manifests, no schema
validators, a PIL pipeline and visual judgement instead. The two sides share exactly one contract -
the `@img` filename - which lives in `references/pipeline.md` on the content side and is cited from
both.

## The one thing to internalise

**`25x_DATA_art_spec.json` is the authority for every number, and the client field decides which
number applies.** Aspect, delivered width, minimum width, format, byte ceiling, chroma key and
padding rule all live there per target, each carrying either a source citation or a rationale. Do
not restate a number from this file or from a scaffold; read the spec.

## What makes this hard

The client handles each art field differently, and only one of the four leaves the image alone:

- **AI avatars, item and jutsu icons, and scene backgrounds are STRETCHED.** `aspect-square` or
  `aspect-3/2` sits on the `<img>` with no `object-fit`. A wrong ratio is visibly distorted.
- **Scene characters are WIDTH-SCALED.** The wrapper has no height, so `object-contain` is a no-op
  and the box is intrinsically sized. A wrong aspect makes the figure SHORT, not distorted, and
  past a certain height the client clips the top.
- **The asset editor previews every type through the square avatar widget, so for anything
  non-square the editor preview is a lie.** This has already cost one wrong re-export of a correct
  file. Judge art on a dark composite at the target aspect, never in the editor.
- **Source resolution above the delivered width is discarded by the CDN**, so a 640px scene
  character and a 341px one look identical to the player and only differ in upload budget.

So the work is: get the generation right at the source, because processing cannot fix composition,
and get the canvas right, because the client will not.

## Production order

Generate one asset at a time and QC between each. Batch generation feels faster and is not: a
systematic prompt fault gets baked into eight images before anyone looks, and regenerating eight
costs more than checking one.

1. Raw QC the generation before touching it (below).
2. Process: key, crop, pad to the target ratio, quantize if over budget.
3. Dark-background composite QC - spill and chewed edges are invisible on white.
4. Record slug, type, output filename, pixel dimensions and KB. Packaging needs a source of truth,
   and the byte ledger is what the Android picker fallback reads.

## Raw QC - reject before processing

Processing a bad generation wastes the processing, so check first and state the failure in one line
rather than salvaging:

- Correct mode and aspect for the asset type.
- No text, labels, watermarks, UI, panels, borders or grids.
- Backgrounds contain no people, characters or creatures.
- Characters sit on a true solid flat chroma field covering the whole canvas - not transparent, not
  a checkerboard preview, no shadow cast onto the key.
- No franchise insignia, ever. No forehead protectors, village headbands, clan symbols or
  real-world logos. Generic masks, wraps, hoods and blank plates only.

Two failures are unprocessable and need a regeneration, not a repair:

- **Painted glow blocks.** A solid pale disc or rectangle rendered as "glow" is art in the same
  palette as the subject. Keying it eats content.
- **A subject resting on a surface.** A character leaning on a desk cannot be composited onto any
  other background, and there is nothing to key.

## Prompting

Read `references/prompts.md` for the per-type scaffolds and the house style. The short version of
what generators get wrong:

- **Short, concrete prompts beat long multi-clause ones.** The generator reliably produces
  holdable objects and reliably fails on packaging formats, phenomena and amorphous material
  chunks. If three blind re-descriptions have failed, switch to reference-image prompting rather
  than writing a fourth.
- **Glow must be rim light on edges only.** Auras, halos, light fields and discs get painted in the
  key colour and then keyed away with the background - see the note in `scripts/chroma.py`. Lead
  the negative block with them.
- **Enclosed spaces must be explicitly the key colour**, or a ring interior comes back as grey and
  cannot be told from the subject.

## Processing

Run the bundled pipeline rather than re-authoring it. This script exists because the keying logic
was being rebuilt from the guide every session, and small drift in the thresholds produces art that
looks fine in chat and wrong in game.

```
python3 scripts/chroma.py in.png out_scene_char.webp --target SCENE_CHARACTER --frame full --qc qc.png
python3 scripts/artpreflight.py out_scene_char.webp --manifest manifest.json
```

- `--target` is the path to use. It reads the spec and derives the key, pad ratio, export format,
  byte ceiling and minimum width, so none of them is a flag anyone can type wrong. It refuses a
  wrong output extension, because the `@img` filename is the contract, and refuses an undersized
  source rather than hiding a generation fault behind a silent upscale.
- `--frame full` pads to 2:3 for a standing figure, `--frame bust` to 1:1 for a portrait. Framing
  picks the aspect; both are ratified.
- `--key magenta` overrides the spec for green-conflicting subjects, anything with foliage, jade or
  green cloth. GPT native transparency is preferred over either when available.
- Always pass `--qc` and actually look at the composite.

Nothing is handed over unchecked. `artpreflight.py` is to art what `validate.py` is to a manifest:
zero errors before handover, and you say what you ran.

`references/processing.md` covers packaging, filenames, the gameAsset write validator and the
upload paths.

## Bundled scripts

| Script | Use |
|---|---|
| `scripts/chroma.py` | Key, crop, pad, export. Spec-driven via `--target`. |
| `scripts/artpreflight.py` | Acceptance check before handover. `--index <art_index.json>` audits the whole live library instead of files. |
| `scripts/shotlist.py` | **Generate the shot list from the quest graph, never author it.** Takes a `quests.get` capture and emits every asset the quest needs with its exact numbers, filename and `@img` ref. Hand-authoring that list is where assets go missing or land with a filename the manifest does not reference. |
| `scripts/artpreflight_selftest.py` | Exit test: one correct and one deliberately wrong export per asset type. |

All of them read `25x_DATA_art_spec.json` from the working directory. Copy it in at session start,
or set `TNR_ART_SPEC`.

## Filenames are a contract

The manifest's `@img:<file>` references resolve by exact filename. So:

- Filenames in the delivery must match the manifest references character for character. Put them
  in a code block so they can be copied rather than retyped.
- **A corrected image gets a fresh filename** (`_b`, `_c`), never a reused one. CDN and picker
  caching mean a reused name serves the old bytes, and the failure looks like the processing did
  not work.

## What belongs to the user

Art direction, palette and final acceptance are theirs. Propose, show, and wait - one image at a
time, with QC between each, is the ratified working rhythm and it exists so that a wrong direction
costs one generation instead of a set.
