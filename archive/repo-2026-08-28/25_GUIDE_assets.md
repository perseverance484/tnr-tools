> **STALE - archived 2026-08-28 (rollout Stage 2).** Superseded by the skill references and generated data under /skills/, and by /docs/ENGINE_LAWS.md. Do not build from this file.

# 25 - GUIDE: Asset and Image Generation

Owner doc for generating, processing, packaging, and delivering the image assets an event needs: enemy sprites, boss scene characters, scene backgrounds, jutsu icons, and the quest icon. It also states how each image reaches the game. The image-upload contract and the combined manifest are in `10_TECH_pipeline.md` (1.4 and 1.5). Palette and per-event art direction come from the event roadmap. This guide is the how of image production; follow it whenever an event needs art.

---

## 1. Production contract (read first)

Default to ONE asset per generation. Never generate asset sheets, grids, multi-panel layouts, concept boards, labeled collections, UI cards, or images containing text unless the user explicitly asks.

Every generated image must pass RAW QC before processing:
- Correct mode and aspect for its type (section 2).
- No text, labels, watermarks, UI, panels, borders, or grids.
- No extra characters unless the subject requires them.
- Backgrounds contain no people, characters, or creatures.
- Sprites and scene characters use a true solid flat lime-green chroma background (`#00FF00`) covering the whole canvas: not transparent, not checkerboard, not a preview grid, no shadow cast onto the green.
- Jutsu icons and the quest icon are complete single square images, not crops from a sheet.

If RAW QC fails, do not process. State the failure in one line and regenerate.

**No franchise insignia.** Never include Naruto forehead protectors, metal village headbands, hidden-village symbols, leaf symbols, real-world logos, or recognizable franchise marks. Generic ninja masks, cloth wraps, hoods, and blank metal plates are allowed only if they carry no symbols.

---

## 2. Asset types and prompt scaffolds

Fill `<...>` from the event roadmap. Keep the negative blocks. Sprites and scene characters are keyed to transparent PNG; backgrounds and all icons are JPG with no transparency.

### 2.0 House style correction (2026-08-26, ratified against live scene characters)

The scaffolds below say "smooth painterly shading, rim lighting". The actual house look, read off the live
scene characters and confirmed by dauntless, is **crisp pixel lineart with flat cel shading and a limited
palette, soft even lighting**. Use that phrasing in place of the painterly clause on every character prompt.
Two further clauses are load-bearing and must appear on every character:

- **camera at eye level, flat 3/4 view, no low angle and no foreshortening** (a low angle reads as another game)
- **both arms held within the subject's own silhouette and touching nothing**, plus a negative block banning
  desks, tables, furniture, props and anything resting on a surface. A scene character drawn leaning on a desk
  cannot be composited onto any other background.

Costume grammar for shinobi characters: dark layered wrap robe, neck cowl or scarf, one accent colour as
piping, wrapped forearms, plain buckled belt. No headband, no forehead protector, no clan symbol, ever.

**Backgrounds: match the set's exposure band.** Measure median luma and the share of pixels under 20 before
accepting one, against the live anchors (Safehouse Room median 16.3 / 63% under 20; Back Alley Night 14.7 /
68%). A generation that comes back at 5.3 median and 95% under 20 is a black rectangle and needs a shadow
lift, not a redraw: a gamma of about 0.75 to 0.82 on the whole image opens the shadows without blowing the
light source. Deliberate variance is fine when the fiction demands it (a market lit by many lamps sits at 22
median because being seen is the point), but state the intent.

**Reserve the lower left of every background.** The client renders the scene character at `w-2/5`, bottom
anchored, with no horizontal offset. Prompt "foreground lower left kept open and unobstructed" or the
character lands on top of the subject.

### 2a. Battle sprite (transparent PNG)
`fusion pixel art, single ninja character, full body, dynamic combat stance, crisp clean pixel rendering with smooth painterly shading, rim lighting, one restrained elemental glow accent, centered, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard, no shadow cast onto the green`
`SUBJECT: <enemy description + element>`
`NEGATIVE: no text, no UI, no watermark, no chibi, no blur, no soft pastel, no muddy dither, no background scenery, no lime spill on the character, no multiple characters, no checkerboard background, no transparent-preview background, no white or grey background, no gradient green, no asset sheet, no grid, no labels, no franchise insignia`

### 2b. Scene character (transparent PNG, boss dialog portrait)
Bust-to-waist portrait, NOT a full-body pose. Match the character to their battle sprite identity.
`fusion pixel art, single ninja character, BUST-TO-WAIST PORTRAIT ONLY, 2:3 portrait canvas, head shoulders and torso visible, no legs or feet, calm but intimidating characterful pose, facing 3/4 or slightly forward, crisp clean pixel rendering with smooth painterly shading, rim lighting, one restrained elemental glow accent, centered, on a true solid flat lime-green chroma key background (#00FF00), not transparent, not checkerboard`
`SUBJECT: <character description + element>`
`NEGATIVE: no text, no UI, no watermark, no chibi, no blur, no soft pastel, no muddy dither, no background scenery, no lime spill, no full body action pose, no legs, no feet, no multiple characters, no checkerboard background, no transparent-preview background, no asset sheet, no grid, no labels, no franchise insignia`

### 2c. Scene background (JPG, no characters)
`fusion pixel art painterly game background, wide scene, <location + motifs + palette>, atmospheric depth, dramatic lighting, no characters`
`NEGATIVE: no people, no characters, no creatures, no character panels, no asset sheet, no grid, no collage, no UI frame, no text, no labels, no watermark`

### 2d. Jutsu icon (JPG, square FX)
Square dark-background FX icon in one locked style; prefer pure FX.
`open square pixel-art <effect> FX, <colors + motion>, dark background, no frame, no text`
`NEGATIVE: no asset sheet, no grid, no circular medal frame unless asked, no labels, no title text, no UI caption, no multiple icons, no anonymous silhouette unless the jutsu meaning needs it, no franchise insignia`
Lock the style on the first approved icon and generate the rest to match. Include a small anonymous hooded silhouette (no headband) only where the jutsu meaning requires it.

### 2e. Quest icon (JPG, bespoke square emblem)
A bespoke listing emblem, NOT a crop from the asset pack.
`fusion pixel art painterly game quest icon, single square emblem composition, dark dramatic background, ornate circular or crest frame if requested, strong readable silhouette, <quest emblem description + palette>, no text`
`NEGATIVE: no asset sheet, no grid, no panels, no text, no labels, no cropped pack image, no multiple icons, no people unless specified, no franchise insignia`

---

## 3. Processing (run in code interpreter)

- **Sprites and scene characters:** chroma-key the flat lime background to alpha, crop to the subject, export a transparent PNG under the sprite budget. Never process a character raw that failed the chroma check in section 1.
- **Backgrounds, jutsu icons, quest icon:** export JPG (no transparency) under budget.
- After each processed asset, record its slug, type, output filename, pixel dimensions, and KB, so packaging has a reliable source of truth.

---

## 4. Candidate lock register

When the user approves an image ("perfect", "A", "this set", "use this"), immediately mark that processed file LOCKED. Do not replace a locked asset later unless the user asks to swap or regenerate it. If only one valid candidate exists, it is the default final. Show only valid candidates; skip raw, failed, and sheet images; do not ask the user to re-choose assets they already locked.

---

## 5. Production order (fastest, least drift)

1. Quest icon, to establish the visual brand.
2. One battle sprite prototype, to establish rendering.
3. Remaining battle sprites, one at a time.
4. Scene characters, generated from the locked boss sprite identity.
5. Scene backgrounds, one at a time, strict no-character check.
6. Two jutsu icons, to lock the icon style.
7. Remaining jutsu icons in the locked style.
8. Package.

This order prevents the two biggest drifts: a late quest-icon correction and a jutsu-icon style swap.

---

## 6. Packaging, filenames, and upload

- Deliver a flat pack (root-level, no folders) of the locked finals, with numbered readable filenames, plus a short manifest listing.
- **Filenames must match the combined manifest's `@img` refs exactly**, and the byte size of each per-record image goes in the manifest `imgSizes` map (the picker size-fallback, `10_TECH` 1.4).
- Upload paths (this is the split that matters):
  - **Per-record images** (jutsu icons, AI avatars/sprites, the quest icon) reach the game through the builder: their `@img` refs are in the manifest, and the user loads the files with the builder's img button (Files picker) when running the manifest. Filename or byte-size match handles the Android picker rename.
  - **Scene backgrounds and scene characters** ride the manifest as `entity: "asset"` entries: art uploads via `@img`, the quest references the created id via `@scene:<srcId>` (10_TECH 1.5, 2.7).
- Show every processed asset in chat as an image plus a download link plus a one-line status (name, dimensions, KB, format, OK), never a bare file path.

---

## 6b. gameAsset write validator (source-confirmed)

The `gameAsset.update` validator, extracted from the TNR source (machine-readable in `45_DATA_field_schemas.json`): `name` 1-191 chars, `image` must be a URL, `frames` and `speed` int 1-100, `type` one of `STATIC` / `ANIMATION` / `SCENE_BACKGROUND` / `SCENE_CHARACTER` / `SFX` / `MUSIC`, `licenseDetails` **required non-empty** (1-512 chars; an empty string fails the save), `onInitialBattleField` bool required, `hidden` optional, `url` optional URL, `folder` optional but **strictly alphanumeric** (letters and numbers only; no spaces, dashes, or underscores).

---

## 7. QA checklist (before delivering the pack)

- [ ] Every required slug exists; optional assets only if requested.
- [ ] Flat structure, numbered readable filenames matching the manifest `@img` refs.
- [ ] No raw, failed, or sheet images; no text or labels on icons unless approved.
- [ ] No franchise insignia anywhere.
- [ ] Sprites and scene characters are transparent PNGs under budget; backgrounds and icons are JPGs under budget.
- [ ] Per-record image byte sizes captured for `imgSizes`.
- [ ] Locked candidates were not replaced later.
- [ ] Every `asset` manifest entry has a non-empty `licenseDetails` and an alphanumeric `folder` (6b).

## 10. Component-based chroma keying (pipeline standard, 2026-07-18)

Global color-keying is retired. The standard is component classification:
1. Flood-fill magenta-ish pixels from the canvas borders: everything reached is background.
2. Remaining magenta components classify by size: area >= ~1200 px (or border-touching) = enclosed background (ring interiors, gaps) -> transparent.
3. Small pockets split by purity: HARD key color (r>180, b>180, g<100) = openwork holes (lace, loops) -> transparent; diluted magenta BLENDS = glow/content -> luminance-matched remap (silver: L*0.88, L*0.94, L).
4. Spill clamp +15 on opaque content; 512KB cap (FASTOCTREE quantize when over); dark-test composite QC; byte ledger keyed to @img filenames.

This handles rings, loops, lace and glow-heavy subjects correctly. Two generator failure modes it CANNOT fix:
- **Key color painted INTO the subject** (magenta in smoke/glows): handled by the pipeline if blended, but prompts should forbid it.
- **Painted glow blocks** (solid pale-blue discs/rectangles rendered as "glow"): these are ART, not chroma - unkeyable without eating same-palette content. Regenerate; do not process.

Prompt scaffold constraints (add to every chroma card): glow rendered ONLY as rim light along subject edges; no auras, halos, light fields, discs or fog; all space enclosed by the subject explicitly the flat key color; negative list leads with glow discs and light fields.

Scene rendering note: the travel-page quest popup shows the quest's TOP-LEVEL sceneBackground; per-node scenes show in the quest view (see 23 3.4b). Wire both.
