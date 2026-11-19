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
  - `--selftest`: no network; asymmetric synthetic sheets (rotated frame, overlapping prefixes, natural frame
    order, stem/prefix mismatch, an orphan plist) through every reader, the catalogue, find, hue_swap, delays,
    strip-height limits and the contact-sheet schedule.
- `skills/producing-tnr-art/data/duelyst_catalog.json` (new, generated): 904 sheets (208 fx, 696 units), 1 skipped
  (`fx_f2BK`, no atlas in the cache), 506 KB.
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
python3 .github/scripts/pack_skills.py                          # producing-tnr-art.zip ~227-228 KB, under 2 MiB (the bot-built dist is authoritative)
python3 scripts/check_no_real_name.py                           # 0 hits
python3 skills/producing-tnr-art/scripts/fx_board.py --selftest # PASS
python3 skills/producing-tnr-art/scripts/duelyst_kit.py --selftest  # PASS
TNR_DUELYST=<cache> python3 skills/producing-tnr-art/scripts/duelyst_kit.py catalog   # 904 sheets, 1 skipped
# a second catalog --out /tmp/cat2.json run is byte-identical (sha256 5b010cf766d75746...)
# selftest also passes with socket.socket and subprocess.Popen replaced by raisers
```

## Known debt / open

- `art/duelyst_fx/duelyst_fx.py` (main, used by the committed Rengoku/Thalmyr build scripts) duplicates the
  reader; those job scripts stay pinned to it. New work imports the kit; folding the old module in is a follow-up.
- Hue buckets and shapes are coarse heuristics for search, not truth: the doc says judge by eye.
- Units -> Sprite Studio sheets (8 x 2/3 grid, Bunny-hosted) is described, not built.
- Phase 2 (recipe composer) and phase 3 (procedural pieces) not begun.
- `references/combat_fx.md` section 3 still says "about 80 frames (mobile 4096 px texture limit)", which assumes the
  50 px Bunny rendition. Native-hosted strips need frame px x frames <= 4096 (now stated in the Duelyst section and
  enforced by the kit). Section 3 is renumbered by `fable/combat-fx-design-rules`, so the fix lands with that
  integration rather than here.
- **Integration with `fable/combat-fx-design-rules`:** that branch adds its own section 7. Merging both textually
  succeeds but yields two section 7 headings: renumber Duelyst to section 8 and update the SKILL.md routing row and
  cross-references at integration.

## Review round 1 (ChatGPT, against 95c41ab1): corrections

1. P2 delays: `parse_delays` reads each `{...}` entry whole (any property order, multiline, single or double
   quotes). 715 sequence timings corrected (e.g. `fx_bloodbig_` 40 ms, `fx_shadowcreep_idle_` 1,000 ms); 32 of
   4,582 sequences have no source timing and are marked `"msFrom": "default"` (80 ms). Docs no longer say all
   frames are 80 ms.
2. P2 prefixes: `frames` matches the exact prefix (`prefix_of(key) == prefix`) and refuses a prefix that is not one
   of the sheet's animations. `neutral_ion:neutral_ion_attack_` is 19 frames.
3. P2 contact sheets: duration = the longest match's play plus its gap (cap 20 s). `fx_f5_bbs_egg` plays all 62
   frames. (Round 2 replaced the fixed sampling step; see below.)
4. P2 actions: with several animations the action is what follows their shared prefix (cut at `_`), so
   `f2_hammonnladeseeker` (frames `f2_hammonbladeseeker_*`) and `neutral_dilotas_attack` (holds `_idle_`, `_hit_`...)
   resolve; 64 action labels changed. One animation keeps the stem rule or `main`.
5. P3 strip size: refused before encoding when frame px x frames > 4096 (phones; found live on Rengoku Rō
   2026-11-17) or > 16,383 with `--allow-tall` (WebP), with the largest size that fits.
6. P3 `catalog --out bare.json`: parent defaults to `.`.
7. P3 selftest: the rotated fixture has a red top-left pixel checked after reconstruction; overlapping prefixes,
   natural order (2 before 10) and partial-prefix refusal are covered. Mutants (`rotate(-90)`, `startswith`) fail it.
8. P3 skips: plists without an atlas, unreadable or empty plists are listed in the catalogue's `skipped` and on
   stderr. The earlier `manaspring` claim was wrong (it is in the excluded `particles/` folder); the real skip is
   `fx_f2BK`.

## Not done

No live calls, uploads or browser checks. No connector writes.

## Review round 2 (ChatGPT, against 33db6375): correction

P2 fast animations: the 40 ms sampling step dropped frames from fast clips (`fx_fluid_puff`, 54 frames at 10 ms,
showed 14). `contact_plan` now schedules shots on every clip's source-frame boundaries (rounded to 10 ms, GIF
centiseconds) with per-shot durations, so every frame gets a slot. A clip faster than 20 ms/frame (the GIF/browser
floor) slows the whole sheet by one factor, and the sheet prints that (`slowed x2: the fastest clip runs 10 ms/frame`);
a sheet longer than 20 s prints that it was cut. Checks:

- selftest: synthetic `[(10, 54), (80, 12), (33, 7)]` shows every frame of every clip; durations are whole 10 ms;
  the slow-down and cut notes appear. With a cache present (`$TNR_DUELYST`), the real `fx_fluid_puff` (54 x 10 ms)
  is read and every frame is scheduled; without a cache that case is skipped and says so.
- `sheet fluid_puff --out puff.gif` decodes to 55 GIF frames (54 at 20 ms, the gap 120 ms); `sheet --kind fx
  --limit 40` renders in about 7 s.
