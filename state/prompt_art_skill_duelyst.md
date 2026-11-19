# Art skill redesign around the Duelyst library (Lane A brief)

Director, 2026-11-19: "I'd like a full skill redesign utilizing the Duelyst assets." Builds on
`fable/combat-fx-design-rules` (d6285df7, house design rules) and `fable/duelyst-kit` (bf6f4fd2, the library kit,
review round 3 pending), both merged into `fable/art-skill-duelyst`, which supersedes them as the review target.

## Scope (reading taken: the request is about battle animations; still-art targets keep their method)

1. Battle animations become **library-first**: find a Duelyst piece, write a recipe, build strips and a real-board
   preview by script; painted art is the fallback.
2. New `scripts/fx_recipe.py`: JSON recipe -> strips (4096 px rule, auto size), board preview with stand-in fighters
   at engine geometry, `recipe.lock.json` for the upload job. Golden test: the White Tiger recipe reproduces the
   live strips pixel for pixel. Shipped recipes in `data/fx_recipes/`.
3. New `references/duelyst.md` (setup, find, recipes, recolour, areas/caster/target, custom scripts, provenance).
4. `references/combat_fx.md`: fighter-placement geometry; design rules 9-11 (one visual tag and one caster clip,
   RUL-165; cast-only buffs, RUL-166; travel told by timing); delivery rewritten around the host table and the
   4096 px height rule (replacing "about 80 frames"); pipeline rewritten library-first; the Duelyst section moves
   to duelyst.md.
5. `SKILL.md`: framing, routing, scripts table, production rhythm, prompting line; `docs/00_INDEX.md` route row.

## Not in scope

Icons, avatars, scenes, jutsu-icon studio (unchanged). Unit sprites as AI sheets (director's call, noted only).
No live calls, uploads or connector writes. Harness phase 3 (procedural pieces) not begun.
