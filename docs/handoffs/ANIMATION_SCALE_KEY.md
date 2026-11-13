# Handoff: accept the per-effect animationScale key (Lane A)

```text
Repository: perseverance484/tnr-tools
Branch: fable/animation-scale-key
Base: ba1f5836161c2c3d6a6933cf72d76c62823b9c46
Head: aa32951df982c0d6d566d4631bef562ed000ae8b (FROZEN)
  = b39370819773c35486d69ef6f5d3c46f85198188 (the change) + aa32951d (github-actions skillpack
    rebuild: dist/building-tnr-content.zip only, triggered by the validate.py edit)
Integration target: main @ 7e4f957c (git merge-tree: clean)
```

## Objective

Let Forge and validate.py pass manifests that set `animationScale` on combat effect tags, so the
Mother of Echoes clips (drawn for 2.5 hex heights) can be sized through the normal pipeline.

Upstream 8bd670153 (studie-tech/TheNinjaRPG, 2026-11-09, "Allow animation sizing per combat effect")
added `animationScale: z.coerce.number().min(1).max(3).prefault(1)` to BaseAttributes
(app/src/validators/combat.ts), drawn at `tile.height * EFFECT_ANIMATION_HEX_RATIO (1) * animationScale`
(app/src/libs/rendering/scenes/combatEffects.ts). The live jutsu.update schema lists it on all 96 tag
variants (connector read 2026-11-13). Both of our key surfaces are pinned to 3314d122, before the key:
forge/src/runner/nested.json and 45c_DATA_constructors.json, so a manifest carrying it was refused
("unknown key").

## Changed

- forge/src/runner/validate.mjs: `EFFECT_POST_PIN_KEYS = ["animationScale"]`, appended to the allowed
  keys of every combat effect tag in nestedProblems. Not titles (TitleEffectSchema does not spread
  BaseAttributes). Keys only, like the rest of nestedProblems; bounds stay with the server.
  Same pattern as AI_POST_0056_KEYS.
- skills/building-tnr-content/scripts/validate.py: `POST_PIN_TAG_FIELDS = {"animationScale": 1..3}`.
  check_effects checks type and range, then removes the key before the 45c AllTags member check; L09
  (per-tag illegal field) exempts it.
- forge/test/animation_scale.test.mjs (new, 3 tests): accepted on jutsu and item combat tags (damage
  and increaseregeneration shapes); a misspelling (animationSize) still refused; refused on a title
  effect; the pinned nested.json still lacks the key (fails loudly at the re-pin that should retire the
  list).
- forge_bundle.js rebuilt.

## Not done / out of scope

- No re-pin of nested.json or 45c (the 2026-11-11/12 drift reports flag ~225 breaking upstream
  changes; adoption needs its own gate). Both lists retire at that re-pin.
- No generator change: push/mother_of_echoes.gen.py does not yet emit the scale. That is the Lane B
  bulk pass that follows this merge.
- No change to capture/merge: Forge edits carry `effects` whole, so a live scale survives a fetch-merge,
  but a manifest whose data.effects comes from an older capture overwrites it back to 1.

## Verification

- `cd forge && node --test test/animation_scale.test.mjs`: 3/3 pass. On main without the change
  (test file present) the accept test fails, as it should.
- `cd forge && npm test`: 822 tests, 14 failing. Same 14 failing test names as main without the
  change (diffed name lists); none new.
- `npm run build` then `node tools/check_bundle_budget.mjs`: 483,053 / 490,000 bytes. main's checked-in
  bundle equalled a fresh build before the change.
- validate.py on a real MoE jutsu from push/506 with every animated tag at 2.5: 0 errors; at 4: 1 error
  per tag ("animationScale=4 outside 1..3"); unmodified record: 0 errors.
- skills/building-tnr-content/scripts/doctrinemap.py, render_doctrine.py --check, build_packs.py --check:
  all exit 0.

## Source / provenance

- Game source: studie-tech/TheNinjaRPG main, 8bd670153 and later (read only, not run).
- Live schema: connector getEndpointSchema jutsu.update, 2026-11-13 (read only).

## Live statement

The code change was built and tested with zero live requests. Separately, on the director's go, the key
was proven live by hand over the connector: job 588 (Stillness at 2.5, law 18 on The Silence) and 589
(a hidden test AI plus the practice quest pointed at it). See state/results/588_*, 589_*.

## Attack hardest

- Whether any combat tag that should take the key is outside the `effects` check path (pet species,
  bloodline and item effects all go through nestedProblems; confirm).
- Whether validate.py removing the key before the member check could hide a real problem in the same
  tag.
