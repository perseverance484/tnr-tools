# Art request: Headless Rider Horror! scene backgrounds (4)

- **For:** the art director and the image-generation sessions
- **From:** Fable / Claude, at dauntless's request (2026-10-25)
- **Status:** PROPOSAL. Scene split, accent and reference await director approval. Background 1
  locks the set's look once approved.
- **Quest:** Headless Rider Horror! (`0lNDtE_VYJOCy8JZQI_sI`), Halloween event, C rank, levels
  10 to 110, hidden.
- **Evidence:** capture `harvests/inbox/tnr_results_1792954275867.json` (push/255, 2026-10-25).
  `scripts/shotlist.py` on that capture: 24 objectives, every `sceneBackground` empty (quest-level
  and all objectives), STATIC pins all wired. It raises one required shot, the quest-level
  background (`headless_rider_horror_01_background.webp`). Backgrounds 2 to 4 are per-objective
  scenes proposed from the story, because the quest moves through four distinct places.
- **Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md` (one asset per generation session).
  Spec authority: `skills/producing-tnr-art/data/25x_DATA_art_spec.json`, target `SCENE_BACKGROUND`.
  House style: `spec.house_style.clauses`, scoped by `spec.prompt_scaffolds.style_clause_scope`
  (backgrounds take `rendering` and `lighting` only).
- **Live-game requests/writes:** 0. Nothing here uploads anything.

## 1. The story, by location

| Location | Objectives | Time | What happens |
|---|---|---|---|
| A. Country road by a harvest field (sector 666) | rfBHq, 7LCTx, RbIyk, NqUdp, 8bLHU, uAVud, i2ZMP, FXLrU | night, full moon; FXLrU ends at first light | a girl runs screaming, the rider runs her down, the player is knocked down by its laugh, smoke bomb, hoofprints left behind |
| B. A small village at sunrise (sector 736) | iAb4r, hPzkO, D3m0Q, kSn_c, o_NY4, czwsz | sunrise | mostly untouched village, warding paper on every gate, villagers peek out, the village head tells the curse |
| C. The destroyed village (sector 926) | Vah2P, jjfV9, dKZp2, BrH2S, lrII0 | just after sunset into night | ruined houses, undead everywhere, three zombie waves, escape through the gate |
| D. The river (sectors 927, 999) | iiiC8, pWxox, 43Z6w, V0IDs, 66Dq0 | night, full moon | searching the riverbank for the rider's skull; the rider materializes and charges |

## 2. Targets

| # | Location | Wire to | Delivery filename |
|---|---|---|---|
| 1 | A, country road by a harvest field | quest `content.sceneBackground` (global; travel popup) and location A objectives | `headless_rider_horror_01_background.webp` |
| 2 | B, village at sunrise | location B objectives | `headless_rider_horror_02_village_dawn.webp` |
| 3 | C, destroyed village at night | location C objectives | `headless_rider_horror_03_ruined_village.webp` |
| 4 | D, moonlit river | location D objectives | `headless_rider_horror_04_river.webp` |

Folder: `headlessriderhorror` (shotlist). Filename 1 is the shotlist's own; keep it exact.

## 3. Spec values (`targets.SCENE_BACKGROUND`)

| Field | Value |
|---|---|
| aspect | 3:2, tolerance 2% (the client stretches backgrounds; non-3:2 distorts) |
| source | 1536x1024 (or 1024x683); minimum 512 wide |
| delivered width | 512 px |
| format | WebP, lossy q85 |
| byte ceiling | 460,800 bytes |
| chroma key / padding | none. Compose to 3:2 at generation; do not crop to fit |
| composition | lower LEFT 40% kept open: the scene character renders bottom-left over it |
| exposure | match the set (live anchors: median luma about 15, 63-68% of pixels under 20). Reject median under 8 or over 90% under 20; repair with gamma 0.75-0.82 |

**Deliberate exposure variance:** background 2 is a sunrise scene and will sit brighter than the
anchors. That is intended by the fiction (spec `exposure_band.deliberate_variance`); keep it a pale,
cold dawn, not daylight.

## 4. Style lock

- `crisp pixel lineart, flat cel shading, limited palette` + `soft even lighting` (spec clauses, verbatim).
- Night scenes: low overall value, cool moonlit blue base.
- **One accent: warm orange** (a lantern, a jack-o-lantern, the dawn sky in 2). Small and local,
  never a field or halo. It ties the set to the Rider's gourd head without competing with him.
- No people, girls, villagers, horses, riders, zombies, ghosts or bodies in any background. Every
  actor in this quest belongs to scene characters and avatars, never painted into the set.

**References per session (pass the actual image bytes, individually, never a collage):**
1. `art/ghost_ship_skyglass/scene_bg_ghost_ship_exterior_keel_walk.webp`: **style only** (pixel
   rendering, night value range, moon treatment, open lower-left floor). Not its subject, its
   cyan accent or its banners.
2. From background 2 on: approved background 1, **style only**.

The Rider avatar (`art/halloween_headless_rider/headless_rider_avatar.webp`) is **not** a
reference for backgrounds: passing it invites the generator to paint the rider into the scene.

## 5. Prompts

The scaffold is `spec.prompt_scaffolds.scaffolds.SCENE_BACKGROUND` (as rendered by shotlist.py);
only `[SUBJECT]` changes per session.

**Positive:**
`wide game scene background, [SUBJECT], crisp pixel lineart, flat cel shading, limited palette, soft even lighting, atmospheric depth, foreground lower left kept open and unobstructed, no characters`

**Negative (scaffold negative + shared negatives + event additions):**
`no people, no characters, no creatures, no horse, no rider, no zombies, no ghosts, no bodies, no character panels, no asset sheet, no grid, no collage, no UI frame, no text, no labels, no watermark, no franchise insignia, no glow halo, no light disc`

**Subjects:**

| # | Subject |
|---|---|
| 1 | a dirt country road at night beside a harvest field of pumpkins and dry cornstalks, a broken wooden fence, a few crooked bare trees, deep hoofprints pressed into the road, low ground fog, full moon |
| 2 | the gate of a small rural village at sunrise, paper warding talismans pasted on the wooden gate posts and doors, shuttered wooden houses, a carved pumpkin on a step, pale cold dawn light with a thin orange horizon |
| 3 | a destroyed rural village at night, burned and collapsed wooden houses, a broken village gate, overgrown paths, scattered debris, low fog, full moon |
| 4 | a rocky riverbank at night under a full moon, a slow dark river with moonlight on the water, reeds and smooth stones along the bank, a dead tree leaning over the water, one small lit lantern left on a rock |

Aspect line for the generator: `landscape 3:2, 1536x1024`.

### Copy-ready isolated-session brief (one per background)

~~~text
Repository: perseverance484/tnr-tools
Workstream: Halloween / Headless Rider Horror!
Target: <filename from section 2>
Lead: Image Production; supporting lens Art Director
Session: ISOLATED GENERATION - one asset only
State: exploratory until director approves
Live-game requests/writes: 0
Credentials: none

Initialize from live repository; verify main and read TNR art authorities.
Read docs/handoffs/HEADLESS_RIDER_HORROR_BACKGROUNDS_ART_REQUEST.md for this one target.
Target type: SCENE_BACKGROUND, landscape 3:2, 1536x1024.
Subject: <subject row from section 5>
Rendering lock: crisp pixel lineart, flat cel shading, limited palette, soft even lighting; cool moonlit blue base (bg 2: pale cold dawn), one small warm orange accent.
References attached: <ref 1 style-only; from bg 2 on, approved bg 1 style-only>
Composition: lower left 40% open and unobstructed ground for the scene character; focal interest centre-right; atmospheric depth.
Exclusions: no people, characters, creatures, horse, rider, zombies, ghosts or bodies; no text, UI, frame, watermark, grid, collage, franchise insignia; no glow halo or light disc.

Generate exactly ONE background candidate for review.
Do not generate other scenes or a collage.
Do not process or upload the image.
Return the original asset after director visual approval.
~~~

## 6. Process

1. **Background 1 first.** It is the required shot; director approval locks the set's look.
2. Backgrounds 2 to 4 each get ref 1 plus approved background 1, nothing else.
3. Two wrong-subject results in one session: close it and start clean (protocol section 3).
4. **Raw QC before processing:** `python3 skills/producing-tnr-art/scripts/rawqc.py <file> --scaffold hrh_scene_background --record`.
   3:2, no figures or creatures, no text, lower left open.
5. **Processing at intake:** resize to the 3:2 source, lossy q85 WebP, exposure against the band
   (bg 2 excepted as above), then `python3 skills/producing-tnr-art/scripts/artpreflight.py <file>` with 0 errors.

## 7. Delivery and next step

- Return each approved original with its filename exactly as in section 2. A correction gets a
  fresh name (`_b`, `_c`).
- Ledger row per file: filename, type `SCENE_BACKGROUND`, pixel size, bytes.
- After intake, Fable builds one quest edit from the 255 capture: four gameAsset creates in folder
  `headlessriderhorror`, quest-level background = 1, each objective's background per section 1.
  Whole-record re-assertion, stays hidden.

## 8. Director decisions

1. Four backgrounds (one required, three per-location) versus the global one only.
2. The warm orange single accent.
3. Reference 1 as the style-only anchor.
