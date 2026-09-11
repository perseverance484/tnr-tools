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

## Doctrine (rendered)

<!-- doctrine:begin @17d6a71 target=skill-art - RENDERED from docs/DOCTRINE.md; edit there, then render_doctrine.py --write -->

TNR is a live browser game with no staging environment: a bad push lands on
players. Every rule in the mounted project instructions and in this block
exists because a push failed, or because a record went live wrong and someone
had to repair it by hand on a phone.

**Doctrine rides the mounted project instructions.** docs/DOCTRINE.md is the
single source; this block carries only what the mounted paste does not. If
this skill is ever run without the mounted instructions, read
docs/DOCTRINE.md before building anything.

<!-- doctrine:end -->

## The one thing to internalise

**`25x_DATA_art_spec.json` is the authority for every number, and the client field decides which
number applies.** Aspect, delivered width, minimum width, format, byte ceiling, chroma key and
padding rule all live there per target, each carrying either a source citation or a rationale. Do
not restate a number from this file or from a scaffold; read the spec.

## Before you generate: look at the references

**References calibrate; the spec governs.** `art/style_refs/` holds exact copies of approved live
TNR scene art, materialized from a committed read-only capture with per-file SHA-256s.
`data/style_refs.json` indexes them and `scripts/style_refs.py` selects them. The pack does not
replace `spec.house_style` and restates none of its clauses or numbers - it is the calibration
layer that stops a session reconstructing "TNR style" from prose and memory.

Where references exist for the target, this order is required before any production generation:

1. Identify the target/type and, for a scene character, the register (`NINJA` or `CIVILIAN`).
2. Read the current `25x_DATA_art_spec.json` target block and `house_style`. That is the authority.
3. Run the selector:
   ```
   python3 scripts/style_refs.py select --target SCENE_CHARACTER --register NINJA --limit 4
   python3 scripts/style_refs.py select --target SCENE_BACKGROUND --tag interior
   ```
4. **Open and actually look at each selected image.** Not the filenames, not the notes - the pixels.
5. Only then compose the prompt and generate.

Three things this order exists to prevent:

- **Prose-only starts.** A prompt assembled from clauses alone drifts, because the clauses were
  measured from images nobody re-read.
- **Collage contamination.** When the generation surface accepts real image references, pass the
  selected **individual images**. A contact sheet or collage puts several subjects in one frame and
  the generator blends them.
- **Context contamination.** Start a new asset class in a clean generation context carrying only
  its own references. Forge UI screenshots once displaced an icon request, and a previously
  generated cabbage displaced an Ittetsu character request; both were carried-over context.

When the surface does **not** accept image references, a URL in the prompt proves nothing about
what the generator ingested. Inspect the images yourself and ground the art-direction wording in
what you actually see.

### Repository-ready is not generation-ready

A workstream task can be `READY` - spec, index, hashes and files all committed - while this
session has never rendered one selected reference pixel. The Road Bandit failure was exactly
that: metadata and URLs were read, nothing was looked at, and the generator returned a cinematic
roadside scene instead of a TNR scene character. So before any production generation the session
answers, from what it actually did, which **reference mode** applies. Exactly one:

- **`ATTACHED`** - the selected individual reference images are real rendered image attachments /
  input images in the current generation conversation. Preferred for ChatGPT production
  generation whenever selected references exist.
- **`ASSISTANT_GROUNDED`** - the assistant actually visually inspected the selected pixels, but the
  generation surface cannot take them as image inputs. The canonical text contract is used,
  grounded by that inspection, and the session says plainly that the generator received no
  reference images. It never claims reference-image conditioning.
- **`NOT_HYDRATED`** - only metadata, paths, URLs or unrendered bytes/base64 are available. Image
  generation is forbidden until hydration occurs.

A path, a raw URL, a hash, a base64 blob, an uploaded ZIP or a collage is never hydration. Only
individual images rendered into the conversation and looked at are.

**Generation preflight.** `scripts/generation_preflight.py prepare` renders, deterministically,
everything the repository can prove about one generation - target/register/frame, the subject
exactly as supplied, spec and index hashes, the exact reference selection with per-file SHA-256s
and raw URLs pinned to an exact commit, the exact prompt object from `shotlist.render_prompt`
and a hash over the canonical generation contract - and initialises everything it cannot prove as
unverified: pixels inspected `false`, reference mode `UNDECLARED`, clean context `false`,
`generation_allowed: false`. It cannot see the conversation or the image tool and never flips
those fields; the session does, by stating what it did. It fails closed if the pack, the
target/register/frame or the rendered prompt does not validate.

**Hydration bundle.** `scripts/style_refs.py bundle` builds a deterministic transfer ZIP of the
exact individual reference bytes plus the index and a manifest of keys and hashes, committed at
`art/style_ref_bundles/tnr_style_reference_pack.zip` outside this package. Download it once,
extract it once, then attach the individual images a preflight names. Uploading the ZIP itself
hydrates nothing, and `bundle --check` proves the committed archive matches the pack.

**Order, for a production generation:**

1. initialise the workstream task (`scripts/content_workstream.py init`) and read its session
   gates - repository `READY` is not action readiness;
2. render the generation-preflight packet;
3. hydrate and visually inspect each selected individual reference, and say what was seen;
4. declare the reference mode;
5. establish a clean generation context carrying only this asset class and its references;
6. settle enough user-owned art direction for one candidate; surface what remains open rather
   than settling it;
7. stage the canonical generation contract from the packet in the conversation immediately before
   the generation call, verbatim - it is the only lever on a product that infers its prompt from
   context, and the repository proves what was staged, never what the product used internally;
8. generate one candidate;
9. classify the returned image as a **PROVISIONAL RAW CANDIDATE** - not accepted, not
   production-ready, not an implied asset;
10. raw-QC it before any processing.

`select` emits raw repository URLs as well as local paths, so an installed skill ZIP with no
checkout is still usable; the binaries are deliberately outside the skill package. `verify` needs a
checkout and audits every reference's bytes, dimensions and format **and proves the pack's
provenance**: it resolves the single successful committed result for the approved capture manifest
out of `harvests/inbox/`, fails closed on zero or multiple matches, requires that result to be
`DONE`/`success` with zero journal mutation items and exactly the expected full-body captures, and
cross-checks every reference's recorded source URL, capture path and snapshot key against it.
Byte-level integrity alone would let a pack hash perfectly while being severed from the approved
capture; `materialize` runs the same check and downloads nothing until it passes.

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

A returned generation is a provisional raw candidate and nothing more. Processing a bad one wastes
the processing, so check first and state the failure in one line rather than salvaging:

- Correct rendering register. Photoreal, cinematic, soft-painterly or anime output is a REJECT,
  not a processing problem; so is scenery or a surface behind a keyed character target.
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
python3 scripts/rawqc.py in.png --scaffold <scaffold_id> --record
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
| `scripts/rawqc.py` | Mechanical raw-QC BEFORE any human look: aspect vs spec, chroma coverage band, 2px ring purity; `--record` appends the scaffold ledger, `--stats` prints accept rates and flags escalation candidates, `--selftest` synthesizes its own red/green fixtures. Run it on every generation before chroma.py. |
| `scripts/artpreflight.py` | Acceptance check before handover. `--index <art_index.json>` audits the whole live library instead of files. |
| `scripts/shotlist.py` | **Generate the shot list from the quest graph, never author it.** Takes a `quests.get` capture and emits every asset the quest needs with its exact numbers, filename, `@img` ref and its rendered generator prompt, assembled from `spec.prompt_scaffolds` with `[STYLE]` expanded verbatim and scoped per target. Hand-authoring that list is where assets go missing or land with a filename the manifest does not reference. |
| `scripts/style_refs.py` | **The visual reference pack.** `select --target ... [--register ...|--tag ...]` picks the deterministic reference set for one production target and prints local paths plus raw URLs; `list` shows the whole corpus; `verify --repo-root .` audits bytes/dimensions/format AND fail-closed capture provenance against `data/style_refs.json`; `bundle --repo-root .` builds the deterministic operator transfer ZIP of the exact individual reference bytes (committed under `art/style_ref_bundles/`, outside this package) and `bundle --check` fails on drift; `--selftest` runs socket-free. `materialize` is a maintainer-only path that proves provenance first and only then re-downloads from the captured image URLs. |
| `scripts/generation_preflight.py` | **The generation contract, rendered not composed.** `prepare --repo-root . --target ... --register ... --frame ... --subject "..." --repo-ref <exact sha>` verifies the pack, selects the references, renders the exact `shotlist.render_prompt` object, hashes the canonical contract and emits every runtime field closed (`generation_allowed: false`); `--json` for the packet, `check <packet>` re-derives a staged packet from the repository, `--selftest` runs socket-free. It never generates and never flips a runtime field. |
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
