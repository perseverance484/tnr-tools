# Handoff: combat FX design rules (producing-tnr-art)

Lane A, branch `fable/combat-fx-design-rules`, base `9f4f7720` (main). Docs and skill text only; no code.

## Why

The director, 2026-11-16: "Current animation quality is all over the place." FCF v4 (a 3x clip on every spiral tile)
turned to mush on the board; v5 (one tile-wide through-cut per tile plus one caster hero clip) fixed it. This pass
writes the lessons, plus research on shipped grid-tactics games, into the art skill so future clips start from one
house style.

## Changes

- `skills/producing-tnr-art/references/combat_fx.md`
  - New section 3 "Design rules (house style)": hero piece once vs applied piece per tile; tessellation through hex
    edge midpoints; three beats; 70-80 ms default with held frames; author for about 40 CSS px; bake layers and reuse
    primitives; engine budget (quiet loop lead-in, dark ground image); clear stock clips (director decides).
  - Section 2: scale 2 = one tile wide; area tags use 2 and tessellate. Replaces "merge into one picture at about 3",
    which v4 disproved on the board.
  - Section 1: at most one visual tag per jutsu (new ruling below).
  - Pipeline step 1: plan against section 3. Sections renumbered 3-7; the one outside reference updated.
- `skills/producing-tnr-art/SKILL.md`: routing row points at section 3; section reference fixed (5 -> 6).
- `docs/rulings/2026-11.md` + `docs/RULINGS.md` (regenerated): RUL-2026-11-16-165, at most one visual tag per jutsu.

## Evidence for the research claims

- OpenDuelyst (CC0, `github.com/open-duelyst/duelyst`), read from a sparse clone: `app/data/fx.js` has 206
  `SpellCastFX` and 102 `SpellAppliedFX` blocks; area spells (Tempest, Plasma Storm, Flaming Stampede) pair one cast
  effect with one to three small applied sprites. `app/data/resources.js`: 4,198 of 5,288 `frameDelay` entries are
  0.08 s. `app/resources/fx/*.plist` (209 sheets): median 25 frames; applied pieces 8-13 frames at 52-80 px
  (`fx_explosionblueelectrical` 52x56, `fx_searingchasm` 80x80, `fx_smoke2` 80x25) against `TILESIZE` 95 at
  `SCALE` 2; cast pieces 196-350 px.
- TNR geometry: hex width from `fx_board.py hex_board` (360 CSS px / 9.25 = about 39 px).

## Gates (all exit 0)

```
python3 skills/building-tnr-content/scripts/doctrinemap.py      # 0 errors, 0 warnings
python3 skills/building-tnr-content/scripts/render_doctrine.py --check
python3 skills/building-tnr-content/scripts/build_packs.py --check
python3 .github/scripts/pack_skills.py                          # producing-tnr-art.zip 182,611 bytes (dist reverted; the bot rebuilds)
python3 scripts/check_no_real_name.py                           # 0 hits
python3 skills/producing-tnr-art/scripts/fx_board.py --selftest # PASS
```

## Not done / open

- No reusable primitive library yet (rule 6 asks for one); proposed as the next Lane A task.
- FCF v5 still runs at 42 ms; re-timing to rule 4 is a director call on the art.
- Using Duelyst's CC0 sheets as actual TNR assets (not just study) is the director's art-direction decision.
- No browser, live or connector writes. One connector read (`jutsu.get` FCF) confirmed spiral range 4.
