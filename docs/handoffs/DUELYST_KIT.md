# Handoff: Duelyst kit (producing-tnr-art)

Lane A, branch `fable/duelyst-kit`, base `ed6f7215` (main). Phase 1 of the Duelyst harness the director asked for
on 2026-11-17 ("pull all of Duelyst's assets and create some kind of harness or skill that can create
art/animations in that style"): the library, catalogue, search, contact sheets and strip export. The composer
(recipes layering several pieces) and procedural pieces in the Duelyst style are later phases.

## Changes

- `skills/producing-tnr-art/scripts/duelyst_kit.py` (new):
  - `fetch`: blobless sparse clone of `open-duelyst/duelyst` at pin `df697549ca`, effects + units + `app/data`, into
    a cache outside the repo (`$TNR_DUELYST`, default `~/.cache/tnr-duelyst`, ~70 MB). Verifies HEAD == pin.
  - `catalog`: walks every effect and unit plist; per sheet the animations (frame prefix, action, frames, ms from
    resources.js), dominant hue buckets, union-bbox shape and coverage; writes `data/duelyst_catalog.json`.
  - `find` / `sheet`: filter by kind, hue, shape, action, frame range and name terms; `sheet` renders an animated
    contact GIF of the matches.
  - `strip`: one sheet or `sheet:prefix` animation -> square TNR strip (anchor, fit, `tint`, `hue_swap`, NEAREST).
  - `--selftest`: no network; a synthetic two-animation sheet with a rotated frame through every reader, the
    catalogue, find, hue_swap and delays.
- `skills/producing-tnr-art/data/duelyst_catalog.json` (new, generated): 904 sheets (208 fx, 696 units), 396 KB
  (34 KB in the skill zip).
- `references/combat_fx.md`: new last section 7 "Duelyst library (CC0)": workflow, recolour precedent, provenance
  line, the repetition caveat (FCF `shadowcreep` trial, Coral Maelstrom rejection). Added at the end so it does not
  collide with `fable/combat-fx-design-rules` (still in review), which renumbers sections 3-7.
- `SKILL.md`: scripts-table row; routing row names the kit and section 7.

`particles/` was fetched and dropped: those plists are cocos particle-emitter configs, not frame sheets.

## Gates (all exit 0)

```
python3 skills/building-tnr-content/scripts/doctrinemap.py      # 0 errors, 0 warnings
python3 skills/building-tnr-content/scripts/render_doctrine.py --check
python3 skills/building-tnr-content/scripts/build_packs.py --check
python3 .github/scripts/pack_skills.py                          # producing-tnr-art.zip 223,766 bytes (dist reverted)
python3 scripts/check_no_real_name.py                           # 0 hits
python3 skills/producing-tnr-art/scripts/fx_board.py --selftest # PASS
python3 skills/producing-tnr-art/scripts/duelyst_kit.py --selftest  # PASS
TNR_DUELYST=<cache> python3 skills/producing-tnr-art/scripts/duelyst_kit.py catalog   # 904 sheets, 7.5 s
```

## Known debt / open

- `art/duelyst_fx/duelyst_fx.py` (main, used by the committed Rengoku/Thalmyr build scripts) duplicates the
  reader; those job scripts stay pinned to it. New work imports the kit; folding the old module in is a follow-up.
- Hue buckets and shapes are coarse heuristics for search, not truth: the doc says judge by eye.
- Units -> Sprite Studio sheets (8 x 2/3 grid, Bunny-hosted) is described, not built.
- Phase 2 (recipe composer) and phase 3 (procedural pieces) not begun.
- One malformed source plist (`manaspring`) is skipped with a warning.

## Not done

No live calls, uploads or browser checks. No connector writes.
