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

## Gates (exact)
- `python3 skills/building-tnr-content/scripts/doctrinemap.py` -> 0 errors, 0 warnings
- `python3 skills/building-tnr-content/scripts/render_doctrine.py --check` -> all projections current
- `python3 skills/building-tnr-content/scripts/build_packs.py --check` -> all packs and TOCs current
- `python3 .github/scripts/pack_skills.py` -> producing-tnr-art.zip 168,305 bytes (2 MiB guard); dist not committed
  (the skillpack workflow rebuilds it)
- `fx_board.py --selftest` PASS; `style_refs.py --selftest` pass; `rawqc.py --selftest` OK;
  `artpreflight_selftest.py` (spec in cwd) 98 passed; `jutsu_studio_selftest.py` 191 passed
- `fx_board.py board` on the FCF v2 clips: 73 frames, 19 tiles, scale 3

## Not done / deferred
- Workflow docs under docs/workflows are routed, not merged or deleted (they carry director rulings).
- No live requests. The claude.ai copy of the skill updates when the director saves the proposal card.
