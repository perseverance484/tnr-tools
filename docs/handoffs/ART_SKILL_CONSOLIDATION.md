# Handoff: one art skill (producing-tnr-art consolidation)

Lane A. Branch `fable/art-skill-consolidation`, base main `9166690`.

Director 2026-11-16: "combine all the scattered tools and documentation for art asset creation for tnr into one
compact useful claude skill."

## What changed
- `skills/producing-tnr-art/SKILL.md` rewritten as a compact router (15.2 KB -> 7.2 KB): every job starts the same
  way (target, spec block, references, route), one routing table by asset class (icons/avatars/scenes; jutsu-icon
  studio and lookup; combat FX), the client-rendering facts, the production rhythm, scripts table, contracts, director
  decisions. Description widened to combat animations and ground tiles. The rendered doctrine block is byte-identical.
- `references/combat_fx.md` (new): the four effect slots, `animationScale` 1-3 shared per effect, `visual` tags for
  art without balance change, real board geometry (2:1 hexes, clip from tile height, tile box inside a frame),
  delivery and the 50 px rendition, gotchas (2-3x appear overdraw, ground disappear repeating on occupants, invisible
  decrease* tags, hidden assets, law 18), and the production pipeline (brief -> painted layers -> script assembly ->
  board preview -> hidden upload -> art-only full-record edit). Condenses COMBAT_ANIMATION_ENGINE.md, the art
  requests, the MoE and FCF work; the size rule re-checked at game source `f6a51fac5`.
- `references/studio.md` (new): routing summary of ISOLATED_ART_GENERATION, BLOODLINE_JUTSU_ICON_STUDIO,
  JUTSU_ICON_SHOWCASE, JUTSU_ART_LOOKUP and the outside-art-request pattern; command lines checked against
  `jutsu_studio.py --help`. The full protocols stay authoritative (ruling-backed).
- `references/processing.md`: the JUTSU_ICON naming-inference rules moved here verbatim from the old SKILL.md.
- `scripts/fx_board.py` (new, Pillow only): `board` (real-board GIF: appear, loop, end, ground image, scale, pattern),
  `ground-box`, `strip-info`, `--selftest`. Generalises the Headless Rider fxkit board without its art dependency.
- `docs/00_INDEX.md`: art row names the skill as the single entry point; new combat-FX row.
  `docs/design/COMBAT_ANIMATION_ENGINE.md`: banner that its fixed 2.5 clip size is superseded.

## Review round 1 (ChatGPT at f2e37351): six P2s fixed
1. Timing: combat_fx.md gotcha 6 now states the f6a51fac5 playback (actions replay in order with windup, strike,
   ~120 ms hold, 4 s cutoff, 8-action backlog; the result screen waits for the final action, so the killing blow is
   animated; one action's effects start together). The engine doc banner now covers timing as well as size.
2. fx_board.py board samples appear, loop and end from one elapsed clock, loop drawn over appear (zIndex 2 over 1);
   selftest asserts a red appear under a blue loop shows blue at t=0.
3. Ground images: new `fx_board.py ground-check` gate (WebP, aspect 1.4-2.6, width >= 128, real alpha, feathered
   edges, byte ceiling); SKILL.md and combat_fx.md route ground images there and away from `artpreflight --type STATIC`.
4. `AVATAR` -> `AI_AVATAR` (the spec identifier).
5. Reference step is conditional again: style_refs covers SCENE_CHARACTER, SCENE_BACKGROUND, JUTSU_ICON only.
6. studio.md keeps PASS / FAIL / NON_CANONICAL (ran, unpinned tool) / NOT_RUN (did not execute) distinct, matching
   jutsu_studio.py's CANONICAL_PREFLIGHT states.

## Review round 2 (ChatGPT at 8c5992d0): two P2s fixed
1. `board` no longer samples a fixed 40 ms tick: it renders one GIF frame at every instant any clip changes frame on the
   shared clock, with that frame's real duration (clamped to GIF's 20 ms floor, with a printed note when a clip is
   faster). Selftest: a two-frame red/blue loop at 20 ms/frame shows both colours.
2. `ground-check` reads the WebP codec chunk through `artpreflight.webp_mode` (VP8X-aware) and refuses anything not
   VP8L. Selftest: a 256x128 transparent-edged lossy (quality 35) image is refused on codec.
Gates: fx_board selftest PASS; FCF ground image 0 errors; FCF board preview 67 frames; doctrinemap /
render_doctrine --check / build_packs --check clean; pack 179,862 bytes.

## Gates (exact)
- `python3 skills/building-tnr-content/scripts/doctrinemap.py` -> 0 errors, 0 warnings
- `python3 skills/building-tnr-content/scripts/render_doctrine.py --check` -> all projections current
- `python3 skills/building-tnr-content/scripts/build_packs.py --check` -> all packs and TOCs current
- `python3 .github/scripts/pack_skills.py` -> producing-tnr-art.zip 168,305 bytes (2 MiB guard); dist not committed
  (the skillpack workflow rebuilds it)
- round 1: `fx_board.py --selftest` PASS (now with the occlusion and ground-check cases); `fx_board.py ground-check` on
  the FCF ground image: 0 errors; pack 179,131 bytes; doctrinemap / render_doctrine --check / build_packs --check clean.
- round 0: `fx_board.py --selftest` PASS; `style_refs.py --selftest` pass; `rawqc.py --selftest` OK;
  `artpreflight_selftest.py` (spec in cwd) 98 passed; `jutsu_studio_selftest.py` 191 passed
- `fx_board.py board` on the FCF v2 clips: 73 frames, 19 tiles, scale 3

## Not done / deferred
- Workflow docs under docs/workflows are routed, not merged or deleted (they carry director rulings).
- No live requests. The claude.ai copy of the skill updates when the director saves the proposal card.
