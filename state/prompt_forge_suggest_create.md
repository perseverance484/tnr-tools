# Build brief: Forge suggest mode sends new records (Lane A)

- **Ruling:** RUL-2026-10-25-001 (director, 2026-10-25: option 2, "add new-record suggestions to Forge").
- **Branch:** `fable/forge-suggest-create` from `main`. One writer (Fable). Independent ChatGPT review on a frozen SHA.
- **Game source:** `studie-tech/theninjarpg@2aed7e4903cc68e18c01e0adb7aec8f39ddffc64` (the pin of
  `forge/src/review/contract.json`); upstream `2af4b320` unchanged for the cited paths. Read, never run.
- **Live-game requests:** 0. No credentials.

## Why

push/254 (ten hidden Skyglass items) is to go in as review-desk suggestions, not direct writes. Forge's suggest mode
refuses creates ("suggest mode can only change existing records"). The game's desk already accepts them:
`staffCreateProposalSchema.entityId` is `.nullable()` and `createStaffProposal` (libs/contentReview/submit.ts) stores a
change with `operation: "CREATE"`, `entityId: null`, no basis; `applyProposal` calls `createEntity` on approval.

## Scope

1. **Manifest policy** (`forge/src/runner/manifest.mjs`, `suggestPolicy`):
   - accept `slot: "create"` items in suggest mode for desk entity types, except `ai` (the desk keeps only
     `aiEditableKeys`, so a suggested AI would be created without its kit) and `notSuggestible` types (quest);
   - refuse a suggested create that any other item references (`@srcId` in data or targetId): it has no id until a
     reviewer approves it, so nothing in the same manifest can point at it (the standing rule "suggest mode refuses
     creates that other records reference");
   - everything else unchanged (title/rationale/category checks, no captures, no Bloodright import).
2. **Runner** (`forge/src/runner/runner.mjs`, `_suggestItem`, `_findSuggestion`):
   - a create sends `contentReview.create {entityType, entityId: null, category, title, rationale, data}` where `data`
     is the manifest data after ref/image resolution, filtered to the validator's known fields exactly as a direct
     create would send it, with no live read; client-side validation runs with no live row;
   - journal: SENT at phase `suggest` with `entityId: null`; CONFIRMED `suggest-find`; VERIFIED `suggested`;
   - the queue match for a create is: tagged title, and a target with `entityId === null`, `operation === "CREATE"`
     and the item's desk entity type (an edit keeps today's id match);
   - lost response / resume behaves as for edits: found means landed, a fully searched queue without it means resend,
     an incomplete search finishes without the id rather than risk a duplicate;
   - `dedupNames` still runs before any send (live-name collision fails that item).
3. **Tests** (`forge/test/suggest.test.mjs`, `forge/test/review.game.mjs`): the fake desk takes `entityId: null`
   as a CREATE; tests for: a create is suggested and nothing is created; images resolve; a referenced suggested
   create is refused at parse; `ai` and quest creates refused; lost-response resume finds a CREATE by title; a live
   name collision fails the item before any send; edits unchanged.
4. **Release staging:** version bump, rebuilt bundle within budget, loader pending marker, rebuilt skill zip,
   `docs/BUILDER_APP_NOTES.md` note. Contract pin unchanged; add a citation for the CREATE path.

## Out of scope

Multi-change proposals; bulk approve; editing a suggested create; dungeon recipe (separate branch
`fable/forge-dungeon-recipe`, frozen for review); any live request.

## Gates

`npm test` (Node 24, full history, `TNR_GAME_CHECKOUT` at the dungeon pin for its one check), `npm run build` +
`git diff --quiet -- forge_bundle.js`, `check_bundle_budget.mjs`, `check_release_pin.mjs`, doctrine gates as routed,
`validate.py --strict` and `check_manifest.mjs` on push/254 in suggest mode. Handoff per
`docs/workflows/IMPLEMENTATION_HANDOFF.md`.
