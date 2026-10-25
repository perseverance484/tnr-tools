# Art request: Headless Rider Horror! scene backgrounds (3)

- **For:** the art director and the image-generation sessions
- **From:** Fable / Claude, at dauntless's request (2026-10-25)
- **Status:** PROPOSAL. Scene list, motifs and prompts await director approval. Background 1
  locks the set's look once approved.
- **Quest:** Headless Rider Horror! (`0lNDtE_VYJOCy8JZQI_sI`), Halloween event.
- **Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md` (one asset per generation session).
  Spec authority: `skills/producing-tnr-art/data/25x_DATA_art_spec.json`, target `SCENE_BACKGROUND`.
  House style: `spec.house_style.clauses`, scoped by `spec.prompt_scaffolds.style_clause_scope`
  (backgrounds take `rendering` and `lighting` only).
- **Node mapping:** pending `push/255_headless_rider_horror_capture.json`. Once its results land,
  `scripts/shotlist.py` regenerates this list from the quest graph and is authoritative over the
  table below if they disagree (a node may already carry a live background worth reusing).
- **Live-game requests/writes:** 0. Nothing here uploads anything.

## 1. Why

The Halloween quest needs its scene backgrounds. The Headless Rider avatar is already done
(dauntless-made, 640x640 lossless WebP, artpreflight 0 errors) and sets the event palette: near-black
riders and horse armor, one accent of hellfire orange-red, bone, a jack-o-lantern head.

## 2. Targets

| # | Scene | Delivery filename |
|---|---|---|
| 1 | Pumpkin-field road at night (approach / opener) | `scene_bg_headless_rider_pumpkin_road.webp` |
| 2 | Covered bridge over a dark creek (pursuit / encounter) | `scene_bg_headless_rider_covered_bridge.webp` |
| 3 | Village graveyard with scorched hoofprints (aftermath / closer) | `scene_bg_headless_rider_graveyard.webp` |

## 3. Spec values (`targets.SCENE_BACKGROUND`)

| Field | Value |
|---|---|
| aspect | 3:2, tolerance 2% (the client stretches backgrounds; non-3:2 distorts) |
| recommended source | 1536x1024 (or 1024x683); minimum 512 wide |
| delivered width | 512 px |
| format | WebP, lossy q85 |
| byte ceiling | 460,800 bytes |
| chroma key / padding | none. Compose to 3:2 at generation; do not crop to fit |
| composition | lower LEFT 40% kept open: the scene character renders bottom-left over it |
| exposure | match the set (live anchors: median luma about 15, 63-68% of pixels under 20). Reject median under 8 or over 90% under 20; repair with gamma 0.75-0.82 |

## 4. Style lock

- `crisp pixel lineart, flat cel shading, limited palette` + `soft even lighting` (spec clauses, verbatim).
- Night, low overall value, cool moonlit blue base.
- **One accent: warm jack-o-lantern / lantern orange**, small and local, never a field or halo.
  It ties the backgrounds to the Rider's hellfire without competing with him.
- No people, horses, riders, ghosts or creatures in any background: the Rider appears as the scene
  character and avatar, never painted into the set.

**References per session (pass the actual image bytes, individually, never a collage):**
1. `art/ghost_ship_skyglass/scene_bg_ghost_ship_exterior_keel_walk.webp`: **style only** (pixel
   rendering, night value range, moon treatment, open lower-left floor). Not its subject, palette
   accent or banners.
2. From background 2 on: approved background 1, **style only**.

## 5. Prompts

The scaffold is `spec.prompt_scaffolds.scaffolds.SCENE_BACKGROUND`; only `[SUBJECT]` changes per session.

**Positive (fill `[SUBJECT]`):**
`wide game scene background, [SUBJECT], crisp pixel lineart, flat cel shading, limited palette, soft even lighting, atmospheric depth, foreground lower left kept open and unobstructed, no characters`

**Negative (scaffold negative + shared negatives + event additions):**
`no people, no characters, no creatures, no horse, no rider, no ghosts, no character panels, no asset sheet, no grid, no collage, no UI frame, no text, no labels, no watermark, no franchise insignia, no glow halo, no light disc`

**Subjects:**

| # | Subject |
|---|---|
| 1 | a dirt road through a moonlit pumpkin field at night, a few carved jack-o-lanterns along a broken wooden fence, bare crooked trees, low ground fog, full moon |
| 2 | an old wooden covered bridge over a dark creek at night, one small lit lantern hanging at the bridge mouth, dense misty forest behind, full moon behind clouds |
| 3 | an overgrown village graveyard at night, leaning stone tombstones, a dead oak, smashed pumpkins in the grass, a trail of scorched hoofprints, low fog, full moon |

Aspect line for the generator: `landscape 3:2, 1536x1024`.

### Copy-ready isolated-session brief (one per background)

~~~text
Repository: perseverance484/tnr-tools
Workstream: Halloween / Headless Rider Horror!
Target: <filename from section 2>
Lead: Image Production; supporting lens Art Director
Session: ISOLATED GENERATION — one asset only
State: exploratory until director approves
Live-game requests/writes: 0
Credentials: none

Initialize from live repository; verify main and read TNR art authorities.
Read docs/handoffs/HEADLESS_RIDER_HORROR_BACKGROUNDS_ART_REQUEST.md for this one target.
Target type: SCENE_BACKGROUND, landscape 3:2, 1536x1024.
Subject: <subject row from section 5>
Rendering lock: crisp pixel lineart, flat cel shading, limited palette, soft even lighting; night, cool moonlit blue base, one small warm orange lantern accent.
References attached: <ref 1 style-only; from bg 2 on, approved bg 1 style-only>
Composition: lower left 40% open and unobstructed floor/ground for the scene character; focal interest centre-right; atmospheric depth.
Exclusions: no people, characters, creatures, horse, rider or ghosts; no text, UI, frame, watermark, grid, collage, franchise insignia; no glow halo or light disc.

Generate exactly ONE background candidate for review.
Do not generate other scenes or a collage.
Do not process or upload the image.
Return the original asset after director visual approval.
~~~

## 6. Process

1. **Background 1 first.** One image per session; director approval locks the set's look.
2. Backgrounds 2 and 3 each get ref 1 plus approved background 1, nothing else.
3. Two wrong-subject results in one session: close it and start clean (protocol section 3).
4. **Raw QC before processing:** `scripts/rawqc.py <file> --scaffold SCENE_BACKGROUND --record`. 3:2,
   no figures or creatures, no text, lower left open.
5. **Processing at intake:** resize to 3:2 target, lossy q85 WebP, exposure check against the band,
   then `scripts/artpreflight.py <file>` with 0 errors.

## 7. Delivery and next step

- Return each approved original with its filename exactly as in section 2. A correction gets a
  fresh name (`_b`, `_c`).
- Ledger row per file: filename, type `SCENE_BACKGROUND`, pixel size, bytes.
- After intake, Fable wires the three as `@img` refs into a quest edit built from the 255 capture
  (whole-record re-assertion, ships hidden).

## 8. Director decisions

1. Scene list and node mapping (confirm against the 255 capture).
2. The orange lantern accent as the set's single accent.
3. Reference 1 as the style-only anchor.
