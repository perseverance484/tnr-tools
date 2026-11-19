# Handoff: art skill redesign around the Duelyst library

- Branch: `fable/art-skill-duelyst` (Lane A). Base: `main` a30da401. Head: the SHA reported with this handoff.
- Brief: `state/prompt_art_skill_duelyst.md` (director, 2026-11-19: "a full skill redesign utilizing the Duelyst
  assets").
- Supersedes two open review targets, merged here: `fable/combat-fx-design-rules` (74a919a2: d6285df7 + skillpack
  bot) and `fable/duelyst-kit` (bf6f4fd2, round 3 pending: contact sheets on source-frame boundaries). Review this
  branch instead; findings on either still apply to the merged code.

## What changed

- **Battle animations are library-first.** `SKILL.md` frames it (find a Duelyst piece, recipe, strips and board
  preview by script; paint only when nothing fits); routing, production rhythm, prompting line, scripts table, and
  the host-dependent delivery bullet updated. `docs/00_INDEX.md` routes duelyst.md.
- **New `scripts/fx_recipe.py`.** A JSON recipe (clips -> layers of Duelyst animations: frames, drop, reverse, flip,
  recolour `gradient`/`hue_swap`/`tint`, anchor `feet`/`body`/`top`/`centre`/number, factor, dx, start, hold; clip
  role, slot, scale, ms, lead, maxPx, upscale) builds one strip per clip sized by the 4096 px rule, a real-board
  preview GIF (phone-width 2:1 board, stand-in fighters at engine geometry, appear/loop/end on one clock), and
  `recipe.lock.json` (file, frames, speed, px, bytes, sha256, licenseDetails, rows cut) for the upload job.
  `check` validates a recipe without the cache; `example` prints White Tiger.
- **`data/fx_recipes/`**: `white_tiger.json` (the live Fury of The White Tiger clips) and `reefward_bastion.json`.
- **New `references/duelyst.md`**: setup, find, recipes, recolour table, areas/caster/target, when a custom script
  is needed (Phoenix, FCF v6, Rengoku), provenance, units (Sprite Studio noted as the director's call).
- **`references/combat_fx.md`**: fighter geometry inside a clip (feet 0.4 h below the centre, body 0.4 h above,
  head 1.2 h above; 1.9 h headroom at scale 3); design rules 9-11 (one visual tag and one caster clip,
  RUL-2026-11-16-165; cast-only buffs, RUL-2026-11-17-166; travel told by lead frames); delivery rewritten around a
  host table and the height rule frame px x frames <= 4096 (replaces "about 80 frames", which assumed the 50 px
  rendition); pipeline rewritten library-first through the upload job; the Duelyst section moved to duelyst.md
  (resolves the duplicate section 7 the kit review flagged).
- **Rulings ledger**: merge kept RUL-2026-11-16-165 (design-rules branch) before main's 166 and 167;
  `docs/RULINGS.md` regenerated.
- `duelyst_kit.py`: docstring and one comment point at duelyst.md / combat_fx.md section 4. No behaviour change.

## Gates (exact commands, all exit 0)

```
python3 skills/building-tnr-content/scripts/doctrinemap.py            # 0 errors, 0 warnings
python3 skills/building-tnr-content/scripts/render_doctrine.py --check
python3 skills/building-tnr-content/scripts/build_packs.py --check
python3 scripts/check_no_real_name.py                                 # 0 hits
python3 skills/producing-tnr-art/scripts/fx_board.py --selftest
TNR_DUELYST=<cache> python3 skills/producing-tnr-art/scripts/duelyst_kit.py --selftest
TNR_DUELYST=<cache> python3 skills/producing-tnr-art/scripts/fx_recipe.py --selftest   # golden: White Tiger strips
    # reproduced pixel for pixel against art/duelyst_fx/showcase/final/anim_white_tiger_{gates_140,tiger_102}.webp
python3 skills/producing-tnr-art/scripts/fx_recipe.py --selftest      # no cache: golden skipped, says so
(cd skills/producing-tnr-art/data && python3 ../scripts/artpreflight_selftest.py)        # 98 passed
python3 .github/scripts/pack_skills.py                                # producing-tnr-art.zip ~231 KB (dist reverted)
```

fx_recipe's selftest also passes with `socket.socket` and `subprocess.Popen` replaced by raisers.
Manual: both shipped recipes built against the pinned cache; the White Tiger board preview checked by eye (gates on
the caster's feet, tiger on the target's body after the lead).

## Known debt, deviations, open decisions

- The board preview in fx_recipe duplicates some of fx_board's hex maths; fx_board stays the tool for finished
  strips and ground images. Merging them is deferred (scope).
- Reefward's recipe uses the kit's `hue_swap`; the shipped strip (2026-11-17) also nudged lightness x1.05 and
  saturation x0.95 and was exported at 288 px before the height rule, so it is an example, not a golden.
- Custom scripts (Phoenix, FCF v6, Rengoku) still import the older `art/duelyst_fx/duelyst_fx.py` on main or the
  kit; porting them is not part of this pass.
- Earlier strips moved to the native host and not re-checked against the height rule (Mother of Echoes slices,
  possibly about 5100 px tall) are outside this branch; flagged to the director.
- Duelyst unit sprites as AI sheets: director's call; documented, not built.

## Not performed / not begun

No live calls, uploads, connector writes or browser battles. Harness phase 3 (procedural pieces) not begun. The
skillpack bot rebuilds `dist/`.
