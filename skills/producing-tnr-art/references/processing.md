# Processing, packaging and QC

> Rewritten 2026-08-26 against `25x_DATA_art_spec.json`. Every number, format, aspect and byte
> ceiling lives in the spec; this file cites it and never restates it. The PNG and JPG export
> instructions that survived here from `25_GUIDE_assets.md` have been **deleted** rather than
> corrected, for the same reason the painterly clause was: a struck instruction that survives
> anywhere gets copied forward.

## 1. Run the tool, do not re-author the pipeline

`scripts/chroma.py --target <TYPE>` is the processing path. The target block decides the key,
the pad ratio, the export format and mode, the byte ceiling and the minimum width, so an export
cannot come out wrong on any of them, because none of them are typed by hand.

```
python3 scripts/chroma.py in.png out.webp --target SCENE_CHARACTER --frame full --qc qc.png
python3 scripts/artpreflight.py out.webp --manifest manifest.json
```

`--frame` is `SCENE_CHARACTER` only and it is a framing decision, not a size one: `full` pads to
2:3, `bust` to 1:1, and both are correct for what they contain. See
`spec.targets.SCENE_CHARACTER.aspect`, which is `measured` over the live population, and the
`render` block above it for why a wrong aspect makes a figure short rather than distorted.

The four keying stages and the reason global colour-keying was retired are in the `chroma.py`
docstring. Read them there. Restating them here is how they drift.

The legacy flags (`--pad-2-3`, `--square`, `--max-kb`) still work and still export PNG. They
exist for scripts written before the spec. Do not use them for new work.

---

## 2. Format

**Struck, permanently: "export a transparent PNG" and "backgrounds and icons are JPGs".** Both
were carried over from the guide and both are now wrong. `spec.format_ruling` is `measured` over
325 live assets and ratified: webp lossless for keyed pixel art, webp lossy for backgrounds. The
per-type value is in each `spec.targets.<TYPE>.format`, and `chroma.py` reads it, so the correct
answer is to pass `--target` rather than to choose.

Lossless is not a preference. Lossy webp rings around hard edges, and hard edges are the entire
content of this style.

The upload ceiling and the working margin under it are in `spec.upload`. The margin exists
because the presign returns nothing useful at the cap, so a file that lands just under the hard
cap fails opaquely on a phone.

Source resolution above the delivered width buys nothing at all: `spec.delivery` records that
the image optimizer is off and exactly one CDN rendition is fetched per image, at the width the
component asks for. Extra pixels are paid for at upload and discarded at delivery. The floor
still matters, since the CDN cannot resize up; that is `spec.targets.<TYPE>.min_width_px`.

---

## 3. Two failures that are regenerations, not repairs

`spec.chroma.unprocessable` names them with the mechanism: painted glow blocks, and a subject
drawn resting on a surface. A third entry, `bridging_glow`, explains why the scaffolds ban auras
and light fields: the border flood crosses diluted key pixels, so a glow that reaches the
background is keyed away with it.

Processing a bad generation wastes the processing. State the failure in one line and regenerate.

---

## 4. QC and acceptance

- Always pass `--qc` and look at the composite. Spill and chewed edges are invisible on white
  and obvious on dark.
- `artpreflight.py` is the acceptance gate, and nothing is handed over without it. It is to art
  what `validate.py` is to a manifest: aspect, dimensions, format, bytes, alpha and the manifest
  `@img` join, checked by the tool rather than by eye.
- `--manifest` checks the delivery against the refs the manifest will actually resolve.
  `--index <art_index.json>` audits the whole live library instead of a folder.
- Show every processed asset in chat as an image plus a download link plus a one-line status:
  name, dimensions, KB, format, verdict. Never a bare file path.

---

## 5. Filenames and the ledger

`spec.filenames` is the contract. Three things it fixes:

- `@img:<file>` resolves by **exact** filename, so delivery filenames go inside a code block and
  get copied, never retyped.
- A corrected image takes a **fresh** filename (`_b`, `_c`). A reused name serves the old bytes
  out of the CDN and the picker cache, and the failure looks like the processing did not work.
- Record slug, type, filename, pixel dimensions and KB for every asset. That ledger is what the
  Android picker size-fallback reads.

---

## 6. Packaging and upload paths

Deliver a flat pack, root level, no folders, with the locked finals and a manifest listing.

The split that matters:

- **Per-record images** (jutsu icons, AI avatars and sprites, the quest icon) reach the game
  through the builder. Their `@img` refs sit in the manifest and the files are loaded with the
  builder's img button when the manifest runs. Filename or byte-size match handles the Android
  picker rename (`10_TECH` 1.4).
- **Scene backgrounds and scene characters** ride the manifest as `entity: "asset"` entries. The
  art uploads via `@img`, the quest references the created id via `@scene:<srcId>` (`10_TECH`
  1.5, 2.7).

Not everything needs a record. `spec.reference_kinds` is the authority on which fields take a
gameAsset id and which take a raw URL; `quest.image` and `objectives[].image` are raw URLs, so a
quest icon or a map pin needs no gameAsset record at all.

---

## 7. gameAsset write

`spec.gameAsset_write` carries the validator, derived from `45d_DATA_entity_schemas.json`
(`app/src/validators/asset.ts`). The two that actually bite:

- `licenseDetails` is required and non-empty, with no default. An empty string fails the save.
- `folder` is strictly alphanumeric. No hyphens, no underscores, no spaces.

`hidden` affects **listing only, never rendering** (law 16c). Live public quests render hidden
assets today. Assets ship `hidden: true` and there is no unhide step at publish; do not build
one.

---

## 8. QA checklist, before delivering the pack

- [ ] `artpreflight.py` run over the pack, zero errors, and the command stated in the handover.
- [ ] Every required slug exists; optional assets only if requested.
- [ ] Flat structure, filenames matching the manifest `@img` refs character for character.
- [ ] No raw, failed or sheet images; no text or labels unless approved.
- [ ] No franchise insignia anywhere.
- [ ] Corrections carry fresh filenames, and no locked candidate was replaced later.
- [ ] Byte ledger captured for `imgSizes`.
- [ ] Every `asset` entry has non-empty `licenseDetails` and an alphanumeric `folder`.

---

## 9. Scene wiring note

The travel-page quest popup shows the quest's **top-level** `sceneBackground`; per-node scenes
show in the quest view (`23` 3.4b). Wire both, or the popup renders empty while the quest looks
correct.

Scene characters stack: the client renders every entry at `absolute bottom-0 w-2/5` (law 48), so
two characters on one node occupy the same spot. `shotlist.py` raises this against a real graph;
do not discover it at review.


## Relocated engine laws (2026-08-28)

Verbatim law text moved out of project knowledge. Stage 3 splices these into the
owning skill reference. Numbers stay canonical against /docs/ENGINE_LAWS.md.

33. **Component-based keying is the standard:** flood background from canvas borders over magenta-ish pixels; remaining magenta components classified by size (>= ~1200 px or border-touching = background/enclosed background -> transparent); small pockets: HARD key color = holes/openwork -> transparent, diluted blends = glow/content -> luminance-matched remap. Handles rings, loops, lace, and glow-heavy subjects.

34. **Generators paint the key color INTO subjects** (glows, smoke). Prompts must demand: glow as rim light on edges only, no auras/halos/light fields/discs, enclosed spaces explicitly the key color; and painted pale-blue "glow blocks" are ART, not chroma - unkeyable; regenerate, do not process.

35. **Spill clamp +15; 512KB upload cap (FASTOCTREE quantize over); dark-test QC before handoff; byte ledger keyed to @img filenames.**

50. **[CORRECTED 2026-08-26, source-verified] Three fields, three different mechanisms. Only ONE of them stretches, and it is not the one the old law named.** The three are read off `QuestDialogScene` (`layout/Logbook.tsx`), `AvatarImage` (`layout/Avatar.tsx`) and `ContentImage` (`layout/ContentImage.tsx`).

    - **Scene characters are WIDTH-SCALED, never letterboxed and never stretched.** The wrapper is `absolute bottom-0 w-2/5` with no height, so `max-h-full` is a percentage against an auto-height containing block and CSS resolves it to `none`; Tailwind v4 preflight (`img { max-width:100%; height:auto }`) overrides the `height={512}` attribute hint; the box is therefore intrinsically sized and `object-contain` is a **no-op**. Displayed width is always 40% of the scene and displayed height follows the FILE's aspect. A wrong aspect makes the figure SHORT, not distorted. The old law's conclusion (target 2:3) survives; its stated mechanism was wrong and had been used to justify re-exports.
    - **AI avatars ARE stretched.** `aspect-square` sits on the `<img>` with no `object-fit`. Non-square is distorted. Unchanged.
    - **Item, jutsu and bloodline icons ARE stretched**, same mechanism (`aspect-square h-full w-full`, no `object-fit`). This field was never covered by the old law.
    - **Scene backgrounds ARE stretched.** `aspect-3/2` on the `<img>`, no `object-fit`. Must be exactly 3:2.

    WHY THE POPULATION SPLIT NEVER RESOLVED: because both camps render acceptably. A 2:3 scene character stands at ~90% of scene height, a 1:1 at 60%. Framing decides which is right, and the guide only ever named one. Aspects, dimensions, formats and byte ceilings per field are generated into `25x_DATA_art_spec.json` and are not restated here.

79. **[NEW] A component's `width` prop IS the delivered pixel width. Source resolution above it is discarded before any player sees it.** `next.config.mjs` sets `images.unoptimized: true`, so next/image emits no srcset and fetches exactly one URL; `layout/Image.tsx` rewrites every Bunny-hosted src to `?width={props.width}`, and only width is sent because Bunny preserves aspect. Delivered widths: scene character 341, scene background 512, AI avatar 320 (`AVATAR_FULL_WIDTH`), item/jutsu icon 125, map pin and combat STATIC 50 (`loadTexture` default), animation sheet 50. Consequences: a 640px scene character and a 341px one are byte-identical to the player; source width buys nothing except headroom against a component change, and costs upload budget. COROLLARY: an asset on a NON-Bunny host (`theninja-user-uploads.s3.*`, `assets.cdndn.com`) gets no rendition and ships at full size on every render. Numbers live in `25x_DATA_art_spec.json`.

80. **[NEW] The asset editor previews EVERY gameAsset type through `AvatarImage`, which is `aspect-square` with no `object-fit`. For any non-square type the editor preview is a lie.** `hooks/asset.ts` declares `size: "portrait"` for SCENE_CHARACTER and `size: "landscape"` for SCENE_BACKGROUND, but those values only steer the AI generator; the preview widget beneath them is the square avatar. A correct 2:3 scene character is genuinely stretched THERE and nowhere else. This is the whole of the 2026-08-22 "renders stretched" finding: the observation was accurate, the surface was wrong, and the re-export to 1:1 that followed made the editor right and the game short. Never accept or reject a scene character on the editor preview; use a dark composite at the target aspect.

81. **[NEW] Scene characters clip above h/w 5/3.** The scene container is `aspect-3/2` with `overflow-hidden`, so scene height is two thirds of scene width; a character at 40% scene width reaches scene height once h/w exceeds 5/3, and is then cut off at the top because the wrapper is bottom-anchored. 2:3 sits at 1.5, about 10% inside the bound. Anything narrower than 3:5 loses its head.

82. **[NEW] The engine's own art pipeline derives 341x512; it was never a chosen number.** `libs/replicate.ts` requests aspect ratio `2:3` for portrait, `3:2` for landscape, `1:1` for square, then `sharp().resize({width: maxDim, height: maxDim, fit: "inside"}).webp({quality: 70})`. `hooks/asset.ts` passes `maxDim: 512` for both scene types; every other content image field (item, jutsu, bloodline, quest node image, sageMode, skillTree) falls through to `maxDim ?? 256`. So 2:3 inside 512 is 341x512 and 3:2 inside 512 is 512x341. The native output format is **webp**, not PNG.

84. **[NEW] A Bunny rendition is not guaranteed. On an EXTENSIONLESS key the CDN engages only when `optimizer=image` is present, and the three.js texture path deliberately never sends it, so those assets are served WHOLE: no resize, no re-encode, and the `width` parameter is inert.** `app/src/utils/image.ts` adds the hint only when the pathname carries no file extension (`if (!/\.[a-z0-9]+$/i.test(url.pathname)) url.searchParams.set("optimizer", "image")`), and `textureImageUrl` omits it on purpose: forcing it on extensionless UploadThing keys made Bunny cache a processed rendition instead of the original, which is what broke travel-map portraits (`app/src/libs/threejs/util.ts`).

    The engine has since fixed the root cause for new uploads. `extensionCustomId` gives every upload a customId carrying its extension and `servedUfsUrl` prefers that path, so a new URL carries an extension and the optimizer engages. The exposure is legacy records only.

    Measured 2026-08-26: **52 STATIC assets, 3619KB, delivered whole to draw 50px sprites.** Half were already webp, so a format-only sweep would have missed the heaviest of them; the lever is resolution, not encoding.

    CONSEQUENCE, and it supersedes the earlier wording in `spec.delivery`: the component's `width` prop is the delivered pixel width only where a rendition is actually generated. For this class the source bytes reach the player unmodified, and it is the only class where they do. `25x_DATA_art_spec.json` carries the same finding as `delivery.cdn_rendition.rendition_precondition` with an explicit `supersedes` note, so the two cannot drift.
