---
name: producing-tnr-art
description: Makes and processes all art for The Ninja RPG (TNR) - item, jutsu and bloodline icons, AI avatars, scene backgrounds and characters, and combat animations and ground tiles - from brief and generation through chroma keying, strip assembly, game-accurate board previews and pre-upload QC to the hidden upload. Use whenever the user asks for any TNR image, icon, avatar, sprite, portrait, scene, jutsu animation, battle effect or ground effect, uploads generated art, or mentions chroma, transparency, frames, animationScale, the image picker or the byte ceiling.
---

# Producing TNR art

Art is generated outside (an image model or the director's art partner), processed here with Pillow, judged by eye
against the game's real rendering, and uploaded hidden through Forge or the builder. No manifests or schema
validators on this side; the shared contract with content is the `@img` filename (`building-tnr-content` pipeline).

## Doctrine (rendered)

<!-- doctrine:begin @b614200 target=skill-art - RENDERED from docs/DOCTRINE.md; edit there, then render_doctrine.py --write -->

TNR is a live browser game with no staging environment: a bad push lands on
players. Every rule in the mounted project instructions and in this block
exists because a push failed, or because a record went live wrong and someone
had to repair it by hand on a phone.

**Doctrine rides the mounted project instructions.** docs/DOCTRINE.md is the
single source; this block carries only what the mounted paste does not. If
this skill is ever run without the mounted instructions, read
docs/DOCTRINE.md before building anything.

<!-- doctrine:end -->

## Start every job the same way

1. **Name the target** and its client field: `ICON`, `JUTSU_ICON`, `AVATAR`, `SCENE_BACKGROUND`,
   `SCENE_CHARACTER`, `ANIMATION`, `STATIC` (ground image).
2. **Read the target block in `data/25x_DATA_art_spec.json`.** It owns every number: aspect, delivered width, minimum
   width, format, byte ceiling, key, padding. Never restate a number from memory or from this file. Scripts find the
   spec in the working directory or `TNR_ART_SPEC`.
3. **Look at references before prompting:** `python3 scripts/style_refs.py select --target <T> [--register NINJA|
   CIVILIAN] [--family ..] [--tag ..]`, then open the pixels. For an existing record, read it live (TNR connector with
   `select`) or with `scripts/jutsu_art.py` at the repo root.
4. **Route** by asset class:

| Asset | Read | Tools |
|---|---|---|
| Icons, avatars, scenes | `references/prompts.md` (scaffolds, house style, generator failures), `references/processing.md` (format, packaging, gameAsset write, scene wiring) | `rawqc.py`, `chroma.py`, `artpreflight.py`, `shotlist.py` |
| Jutsu-icon families, studio sessions, art lookup, outside art requests | `references/studio.md` | `jutsu_studio.py`, `style_refs.py` |
| Combat animations, ground tiles, battle FX | `references/combat_fx.md` | `fx_board.py`, a per-job `build_strips.py` |

## How the game shows art (what makes this hard)

- **Icons, avatars and backgrounds are stretched** to their box (no `object-fit`): a wrong ratio distorts.
  **Scene characters are width-scaled**: a wrong aspect makes them short, and tall art is clipped. The asset editor
  previews everything as a square avatar, so judge non-square art on a dark composite at the target aspect.
- **Source above the delivered width is discarded by the CDN**; battle clips arrive as a 50 px-wide rendition.
- **Battle clips are squares sized from the tile's height** (`animationScale` 1-3) on a board squashed 2:1, and every
  hit tile plays at once. Preview on the real board (`fx_board.py board`), never on a square tile.
- **Hidden assets never render.** Create hidden, unhide by edit, check in a battle.

So get the composition right at generation (processing cannot fix it) and the canvas right (the client will not).

## Production rhythm

One asset at a time, QC between each; batches bake one prompt fault into every image.

1. **Raw QC before processing** (`rawqc.py --scaffold <id> --record`): right mode and aspect; no text, labels,
   watermarks, UI, borders or grids; no people in backgrounds; characters on a flat full-canvas chroma field; no
   franchise insignia, headbands or clan symbols ever. Regenerate, do not repair, a painted glow block or a subject
   resting on a surface.
2. **Process:** `chroma.py in.png out.webp --target <T> [--frame full|bust] [--key magenta] --qc qc.png` (keys, crops,
   pads, exports per spec; refuses wrong extensions and undersized sources). `JUTSU_ICON` may keep a designed opaque
   background: never key it. Animations: assemble strips by script from painted layers (`combat_fx.md` section 5).
3. **QC on dark, mid and bright grounds** (spill and chewed edges hide on white); FX on the board preview.
4. **Preflight:** `artpreflight.py out.webp [--manifest m.json] [--max-bytes N]`, zero errors, and say what you ran.
5. **Record** slug, type, filename, pixels and bytes (the picker fallback reads the byte ledger).

## Prompting in one breath

Short concrete prompts beat long ones; objects work, phenomena and amorphous chunks fail, and after three failed
re-descriptions switch to reference-image prompting. Glow is rim light on edges only (auras and discs get keyed away)
and leads the negatives. Enclosed spaces are explicitly the key colour. One subject per clean generation context:
leftover context once turned an icon into a Forge screenshot. For animations, ask for painted layers or key poses,
not frame sheets.

## Scripts

| Script | Use |
|---|---|
| `rawqc.py` | mechanical raw QC (aspect, chroma coverage, ring purity); `--record` ledger, `--stats`, `--selftest` |
| `chroma.py` | key, crop, pad, export, all spec-driven via `--target` |
| `artpreflight.py` | acceptance gate per type; `--index` audits the live library; `artpreflight_selftest.py` |
| `shotlist.py` | every asset a quest needs, generated from a `quests.get` capture with filenames and prompts |
| `style_refs.py` | the approved reference pack: `select`, `list`, `verify --repo-root .` (provenance), `--selftest` |
| `jutsu_studio.py` | ZIP-first jutsu-icon family studio: `doctor`, `intake`, `lock-check`, `attempts`, `compare`, `finalize`, `audit-gallery` |
| `fx_board.py` | combat FX: `board` (real board GIF), `ground-box` (tile inside a clip frame), `strip-info`, `--selftest` |

## Contracts

- **Filenames are the contract:** deliver `@img` names exactly as the manifest references them, in a code block. A
  corrected image gets a **fresh** filename (`_b`, `_c`); caches serve the old bytes under a reused one.
- **gameAsset writes:** non-empty `licenseDetails`, alphanumeric `folder`; create `hidden: true`, then unhide every
  battle asset by edit with the literal id from the results bundle (law 16).
- **Art onto a record never changes its mechanics.** Jutsu edits are full-record `jutsu.update` (Forge `livePatch`
  for bulk art fields); a jutsu an AI equips needs law 18. Live writes only on the director's go for that job.

## What belongs to the director

Art direction, palette, scale, framing, whether a stock asset is replaced, and final acceptance. Propose, show the
real-geometry preview, and wait.
