# Forge dungeon recipe: independent review prompt

~~~text
You are the independent reviewer for a Lane A code change in perseverance484/tnr-tools. Review only; do not patch the
Fable branch. Follow docs/workflows/FABLE_REVIEW.md.

TARGET
- Branch: fable/forge-dungeon-recipe (frozen)
- Head (audit target): aef88c3e3bb99c7dac465f5e35b5e13e20c253b3
- Base: 991a58c80cae9737a447e61c2c615f5cd970078e
- Brief (the contract): state/prompt_forge_dungeon_recipe.md (RUL-2026-10-23-006); budget RUL-2026-10-23-007
- Handoff: docs/handoffs/FORGE_DUNGEON_RECIPE_HANDOFF.md (on main)
- Game source pin: studie-tech/theninjarpg@107d7a86894f806a4c9cec89effef5992118a0ed (read only, never run)

Verify the head SHA before anything else. If the branch has moved, stop and report.

SAFETY
Zero live-game requests. No credentials, cookies or session material. Use the pinned source, the repo, fixtures and the
in-process fake game only.

WHAT IT DOES
Adds a Forge recipe for the game's dungeon definitions: a contract derived from the pinned source
(forge/tools/derive_dungeon.mjs -> forge/src/dungeon/contract.json), a client-side validator
(forge/src/dungeon/validate.mjs), a one-step create through dungeon.save {content} with the id read from the response,
update {id, content}, read-back through dungeon.getAll, journal/reconcile support, a 30-write cap, routing from
validate.py --strict to the Node validator, Forge 0.9.0 release staging and a bundle budget of 435,000 / 105,000.

READ IN THIS ORDER
1. docs/00_INDEX.md, state/active-context.md, state/status.json
2. state/prompt_forge_dungeon_recipe.md, then the handoff
3. At the pin: app/src/validators/dungeon.ts (or wherever the content schema lives), app/src/server/api/routers/dungeon.ts,
   app/src/libs/dungeon*.ts, app/drizzle/constants.ts
4. The diff: git diff 991a58c..aef88c3

GATES TO REPRODUCE (Node 24, full-history clone, TNR_GAME_CHECKOUT pointing at the pin)
- cd forge && npm test                                  (expected 667/667)
- node tools/derive_dungeon.mjs <checkout> --check       (expected "dungeon contract current")
- npm run build && git diff --quiet -- forge_bundle.js   (bundle reproducible)
- node tools/check_bundle_budget.mjs                     (425,490 / 102,323 against 435,000 / 105,000)
- node forge/tools/check_release_pin.mjs
- validate.py --strict (from skills/building-tnr-content/data) and node forge/tools/check_manifest.mjs (from forge/)
  on a valid and a broken dungeon manifest
Report exact commands and exit codes. Do not pipe a gate in a way that hides its exit code.

ATTACK THESE FIRST (the handoff's risk list)
1. Composed limiter: dungeon.save is the first mutation marked limited:true. Prove no code path treats "limited" as
   "query" (budget metering, retries, read-only modes, procedure tables).
2. Lost-create adoption: after an ambiguous create, Forge adopts the single new row since the snapshot only if it matches
   every asserted key. Try to make it adopt the wrong row, or adopt when it should stop. Is skipping operator binding
   (which Bloodright requires) justified?
3. Whole-content replace: every edit re-sends the full live content read from dungeon.getAll. Check server-side
   defaults and package snapshots on drops, fields the read adds or drops, and a live row that no longer parses at the
   pin. Could an edit silently change or lose live data?
4. Dates: expiresAt round-trips as a Date; the diff uses eqLoose. Check time zones, string versus Date, and null.
5. Bounds the client cannot check (package contents, referenced row existence, weighted-cache drops): confirm they
   surface as clear refusals, not silent success.
Then check the derive tool fails closed on every pattern, the validator mirrors every refinement in the pinned schema,
and the floor/wave/drop rules match source (exactly 3 players, tiers x 5 floors, boss and mini-boss floors, waves,
first-wave delay, structureAssetId as a mapAsset).

CONTEXT
main has advanced since the base (docs, results, two skill reference edits and rebuilt dist zips). That is expected.
Do not rebase or merge the target. Note any conflict risk for integration.

REPORT
For each finding: severity (blocker / should-fix / note), file:line, the invariant broken, a reproduction, and a
suggested fix. List what you checked and found clean. Say explicitly what you could not verify without a live session.
End with a verdict: approve, approve with fixes, or reject.
~~~
