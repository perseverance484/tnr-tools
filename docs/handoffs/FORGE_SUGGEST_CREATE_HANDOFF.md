# Forge suggest-mode creates — implementation handoff (Lane A)

```text
Repository: perseverance484/tnr-tools
Branch: fable/forge-suggest-create
Base: 02d8b438d9fb21fe1f3596b2fbcb51f05111e83e
Head: 92d8103afd5f5d2ccc5b0ca2ffcd265805d4d233 (FROZEN until review returns)
Integration target: main
Brief: state/prompt_forge_suggest_create.md (RUL-2026-10-25-001)
Reviewer: ChatGPT (independent)
```

## Objective

Let a `"mode": "suggest"` manifest send new records to the game's content review desk as CREATE suggestions, so
push/254 (ten Skyglass items) can go in through review instead of direct writes.

## Changed

- `forge/src/runner/manifest.mjs` `suggestPolicy`: accepts `slot: "create"`; refuses AI creates (desk keeps only
  `aiEditableKeys`) and any item that references a suggested create's `srcId` (`@pfx:srcId`, images excluded).
- `forge/src/runner/runner.mjs` `_suggestItem`: a create skips the live read, validates with no live row, builds the
  payload with `mergeForUpdate(entity, null, data, knownFields)`, keeps the item `expireFromStoreAt: ""` rule, and sends
  `contentReview.create` with `entityId: null`. `_findSuggestion`: an item with no id matches a target with
  `entityId == null`, `operation === "CREATE"` and the same desk type, plus the tagged title.
- `forge/src/storage/journal.mjs`: `CONFIRMED -> SENT` without an entityId is allowed only for `phase === "suggest"`
  on an `op === "create"` item (the resend after a fully searched queue shows the first send never landed).
- `forge/src/ui/screens.mjs`: suggest banner wording. `forge/src/review/contract.json`: one citation for the CREATE path
  (pin unchanged).
- Tests: `forge/test/suggest.test.mjs` (+7, first test's create-refusal assertion replaced), `review.game.mjs` fake
  desk handles `entityId: null` as CREATE.
- Release staging: `forge/package.json` 0.8.2, `@x-release-pending 0.8.2` in `forge_loader_user.js`, rebuilt
  `forge_bundle.js`, `docs/BUILDER_APP_NOTES.md` "Suggest mode: new records (0.8.2)".

## Verification (Node 24.22.1, full-history clone)

- `npm test` in `forge/` — 651 tests, 651 pass (base 644/644).
- `npm run build` then `git diff --quiet -- forge_bundle.js` — reproducible.
- `node tools/check_bundle_budget.mjs` — raw 413,654 / 420,000 (98.5%), gzip 99,092 / 100,000 (99.1%).
- `node tools/check_release_pin.mjs` — ok.
- push/254 converted to suggest mode (category NEW_CONTENT): `check_manifest.mjs` 0 pre-send problems,
  `validate.py --strict` 0 errors, 0 warnings.
- `doctrinemap.py` 0/0; `render_doctrine.py --check` 0; `build_packs.py --check` 0; `lawmap.py` 0 errors, 5
  pre-existing warnings. `pack_skills.py`: `dist/` unchanged.

## Source

`studie-tech/theninjarpg@2aed7e4903cc` (contract pin): `staffCreateProposalSchema.entityId .nullable()`;
`createStaffProposal` stores `operation: "CREATE"`, `entityId: null`, no basis; `applyProposal` -> `createEntity`;
`toSummary` targets carry `operation` and `entityId`. Read, never run.

## Risk / debt — attack these

1. **The journal exemption.** Is `phase === "suggest" && op === "create"` narrow enough? Can any other path reach
   `CONFIRMED -> SENT` with that phase and no id?
2. **Duplicate creates.** The desk does not dedupe names on a staff CREATE. Forge's guard is the tagged-title queue
   search; an incomplete search (>60 pages) finishes without resending. Is the CREATE match (no id, same type,
   operation) safe against another job's create with a different tag?
3. **Payload completeness.** A CREATE is validated by the desk on `editableOf(data)` alone. Forge sends the manifest
   data filtered to known fields with no defaults added; a manifest missing required fields is refused by the desk
   (reported as a failure), not completed by Forge.
4. **No id after approval.** `checkSuggestions` records status but not the created id; later manifests must look the
   record up by name. Not in scope.
5. **Bundle budget** at 99.1% gzip on main's 100,000 limit; the dungeon branch raises it to 105,000 (RUL-2026-10-23-007).
   Both branches bump the version and rebuild the bundle, so whichever merges second rebases and rebuilds.

## Live-game statement

Zero live requests, zero game writes, no credentials. The real desk's response to a CREATE is taken from source.
