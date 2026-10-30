# Variant capture reads: item.getItemVariants and item.getVariantNames as full-persist captures at TheNinjaRPG@3314d122 — 2026-10-30

**Lane:** A (Forge capture policy). **Ruling:** RUL-2026-10-29-054 item 2: before any Skyglass Token ships, every live `VARIANT_TOKEN` variant is captured read-only, and any without a required unlock item is bound to a token. The Skyglass Token (`unlockitemvariant`, `variantId: null`) would otherwise also unlock every token variant whose `requiredItemId` is null. Forge 0.12.0 could not persist variant rows in a capture.
**Branch:** `fable/variant-capture-reads`, cut from `main@87c96edd` (Forge 0.12.0 released: loader `@version 0.12.0`, `@require` pinned to `179c3399`). The frozen head is reported with the push; this file is the handoff for it.
**Game source:** `studie-tech/TheNinjaRPG@3314d122c93e036618483d18229a793ad7ad21fd` (the current contract pin), read only from a local worktree of `origin/main`, never executed.
**Live requests / writes:** 0 / 0. **Credentials:** none. No capture manifest is on this branch; `push/`, `state/`, `docs/RULINGS.md` are untouched.

## Audit (source at 3314d122)

| Read | Declaration | Query | Persist verdict |
|---|---|---|---|
| `item.getItemVariants` | `routers/item.ts:1153` `protectedProcedure.input(z.object({ itemId: z.string() })).output(z.array(ItemVariantResponseSchema))` | `queries/item.ts:933` `listItemVariantForGetItemVariants`: `itemVariant.findMany({ where: itemId = input.itemId, orderBy: order })` | **Content rows of one record's children.** Columns (`validators/item.ts:120`): `id, itemId, name, image, requiredItemId, costType, cost, order, createdAt, updatedAt, description, battleDescription, furnitureData`. No `ctx.userId`; per-player unlocks live in `UserItemVariant`, which this query does not touch (`getUserUnlockedVariants` reads them and is not admitted). Full-persist point read keyed by `itemId`. |
| `item.getVariantNames` | `routers/item.ts:1150` `protectedProcedure.query(({ ctx }) => listVariantNames(ctx.drizzle))`: **no `.input()`** | `queries/item.ts:2350` `listVariantNames`: `select { id: itemVariant.id, name: concat(item.name, ": ", itemVariant.name) } from ItemVariant inner join Item on item.id = itemVariant.itemId where costType = "VARIANT_TOKEN"` | **Content only:** a variant id and two content names. No `ctx.userId` (only `ctx.drizzle`), no user table, no counts, no `ORDER BY`. Admitted as the one input-less list whose rows persist. |

Both are `protectedProcedure` (`trpc.ts:332`: `enforceUserIsAuthed`, pyramid isolation for mutations, bot id, sentry): any signed-in user, no rate limiter, no mcp meta. Neither checks a staff role. The join does not filter `item.hidden`, so a hidden base item's NAME can appear in the list; `item.get` (already full-persist) persists hidden items' whole records, so this is no new class of data.

### Why a list exception, and why it is narrow

The policy (captures.mjs header; `state/prompt_forge_full_capture.md` "Full-mode safety boundary"; RUL-2026-09-17-001: widening a tier needs an explicit reviewed change) refuses full persistence on list procedures. A list capture records `rows` only. The census needs every token variant id, and the only read that enumerates them without one read per item is `getVariantNames`. The alternatives:

- a `getItemVariants` read for every item: 873 live items, about 107 of which no repository file names (push/323 `item.getAllNames` count vs the 766-row seed), so it is not complete and costs 873 reads;
- a projected tier: not implemented in Forge, and the rows have only two fields anyway.

So the widening is one path, in its own list (`FULL_PERSIST_LIST_PATHS`), not added to `FULL_PERSIST_PATHS`, and only with no input: there is no filter, so a list with an input would be a misunderstanding (and "a filtered call's silence is not evidence of absence" cannot arise). Every other list stays a row count; the boundary test asserts the list is exactly `["item.getVariantNames"]` and that its procedure row is a protected query.

## What changed

**Forge 0.12.1 (`@x-release-pending 0.12.1`; the loader keeps the released `@version 0.12.0` and its `@require` pin `179c3399`).**
- `src/transport/procedures.mjs`: `item.getVariantNames` `{kind: query, limited: false, mcp: false, auth: protected}`, cited. Table 71 -> 72 paths; protected 46 -> 47; limited unchanged (26).
- `src/storage/captures.mjs`: `item.getItemVariants` joins `FULL_PERSIST_PATHS`; new `PERSIST_RECORD_KEY = {"item.getItemVariants": "itemId"}` (the record key of a point read that is not `id`/`userId`); new `FULL_PERSIST_LIST_PATHS = ["item.getVariantNames"]`; `canPersistFull` accepts both lists.
- `src/runner/manifest.mjs` `normalizeCapture`: the id is `input[PERSIST_RECORD_KEY[proc]]` when declared (else `id ?? userId`, unchanged). Full on `getItemVariants` needs a non-empty string `input.itemId` ("needs input.itemId naming one record"); full on `getVariantNames` refuses any input except absent/null/`{}` ("takes no input"). The existing messages for the other paths are unchanged.
- `src/runner/runner.mjs` `_captures`: a path in `PERSIST_RECORD_KEY` is read through `reader.list(path, {fresh, input})` with the manifest's own input, not `reader.get(path, id)` (which would send `{id}` and write a read-cache slot that a variant edit does not invalidate). `sentInput` follows the same branch. For a summary `getItemVariants` capture the wire call and journal entry are what 0.12.0 produced.
- `src/budget/reader.mjs` `list()`: accepts `item.getVariantNames`. Its id-`""` slot is entity `item`; every item write (`invalidateRecord("item", id)` drops id-less slots) and every variant create/edit (`cacheEntity: "item"`) drops it.
- `package.json` / `main.mjs` VERSION 0.12.1; `forge_bundle.js` rebuilt; `forge_loader_user.js` gains `// @x-release-pending 0.12.1` only.

**Docs / skill.** `skills/building-tnr-content/references/pipeline.md` §2.10 table: `getItemVariants` full-persist note; new `getVariantNames` row. Packs and `_toc/pipeline.json` re-rendered (`build_packs.py --write`; hash stamps and offsets only). `docs/BUILDER_APP_NOTES.md` gains a 0.12.1 section.

**Tests (socket-free).**
- `test/fakegame.mjs`: `item.getVariantNames` answered from the tables as `listVariantNames` does (VARIANT_TOKEN only, inner join, `"<item>: <variant>"`).
- `test/capture.full.test.mjs`: the `FULL_PERSIST_PATHS` expectation now includes `item.getItemVariants`, plus `FULL_PERSIST_LIST_PATHS` is exactly `["item.getVariantNames"]`; five new tests: parse rules (itemId required, `{id}` refused, list refuses any input, other lists still refused, summary of both unchanged); a census run against FakeGame (wire inputs `undefined` / `{itemId}`, exact exported rows incl. `requiredItemId`, snapshot id = itemId, compact journal, no read-cache slot for the filtered list); summary `getItemVariants` unchanged; signed-out census pauses on `SESSION` at the first read and persists nothing; the list slot is dropped by a variant-edit invalidation.
- `test/storage.captures.test.mjs`: the boundary test admits `getItemVariants` as a point read, asserts the list exception and `PERSIST_RECORD_KEY` exactly, and still asserts every other audited path is not persistable.
- `test/variants.test.mjs`: a checkout-gated test pins the two declarations and both queries' text at 3314d122 (no `.input()`, select of exactly `id` and the concat name, the VARIANT_TOKEN where, no `ctx`/user in the query; `getItemVariants` reads `itemVariant` by `itemId` ordered by `order`).
- `test/auth.test.mjs` (47 protected), `test/transport.client.test.mjs` (72 paths, the new row).

## Gates (exact)

| Gate | Result |
|---|---|
| `npm test` (forge/) | 781 tests, 767 pass, 0 fail, 14 skipped (checkout-gated). Base `87c96edd`: 775 / 762 / 0 / 13. |
| `TNR_GAME_CHECKOUT=<3314d122 worktree> npm test` | 781 / 781 pass, 0 skipped |
| `npm run build` twice | byte-identical, sha256 `fa9d7a316c949903e901f661220f48c85aa01828229458a399ec23e42d92ffc3` |
| `npm run fixtures` then `git status` | clean (no fixture changed) |
| `check_boundaries` / `check_imports` / `check_release_pin` | 0 violations (pin 3314d122) / 0 / release pin ok |
| `check_bundle_budget` | exit 0: **raw 464,150 / 466,000 (99.6%), gzip 111,645 / 112,000 (99.7%)**. Base 463,369 / 111,448 (+781 / +197). Not raised. Headroom 1,850 / 355. |
| `node tools/auth_pin_diff.mjs <3314d122> <3314d122>` | 0 disagreements across 60 Forge paths (59 + `item.getVariantNames`) |
| `check_manifest.mjs` and `validate.py` (cwd skill `data/`) on all 121 `push/*.json`, base vs head | full output and exit codes identical (`validate.py` output identical modulo the repo-root prefix in its path echo); `validate.py --strict` exit codes identical |
| `doctrinemap.py .` / `render_doctrine.py --check` / `build_packs.py --check` (after `--write`) | 0 errors 0 warnings / all projections current / all packs and TOCs current (all exit 0) |
| `lawmap.py .` (repo root) | 93 laws, 0 errors, 5 pre-existing warnings (same as base) |

No Python validator change: `validate.py` checks only that a capture entry has `proc` and an object `input`; it has no persist allowlist.

## Known debt, deviations, open decisions

1. **The list exception is a policy widening** (reviewer: attack it). It rests on the audit above; if the reviewer prefers, `item.getVariantNames` could instead stay summary and the census would need one `getItemVariants` per item id the repository knows (incomplete: ~107 live items are unknown offline).
2. `getVariantNames` names are `"<item>: <variant>"` with no `itemId`; item names themselves contain `": "` (e.g. `ID Card: Daigo`). Resolving base-item ids from names is the capture manifest's job (Part 2, Lane B), not Forge's. Rows are unordered at source.
3. Both reads need a signed-in session (protected), not a staff session. A signed-out run pauses at the first read.
4. The bundle is at 99.6% / 99.7% of the 466,000 / 112,000 budget.
5. `PERSIST_RECORD_KEY` routes a keyed path through `list()`; today it holds one entry. A future keyed point read that is a real `{id}`-style get would not belong there.

## Not done / not begun

- No browser, live or session checks; no Forge release (the release workflow promotes 0.12.1 after merge).
- No capture manifest on this branch. The Lane B census generator (pass 1: `getVariantNames` + `item.get` of the Lion Token and Test Variant; pass 2: `getItemVariants` per resolved base item) is prepared outside the branch and is committed to `main` only after this merges and releases.
- No binding manifest (`requiredItemId` edits); no answers/ catalogue of variants; `docs/RULINGS.md` and `state/` not edited.
