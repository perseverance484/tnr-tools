# Pet catalogue capture reads: petSpecies.getAll and PETS jutsu.getAll as full-persist captures at TheNinjaRPG@3314d122 — 2026-10-31

**Lane:** A (Forge capture policy). **Approval:** director-approved 2026-10-31. Forge must capture the live pet catalogue with full records, so the Skyglass Little Horror kit can be balanced against live pets and its default loadout can include live PETS jutsu. Forge 0.12.1 kept only a row count for every list except `item.getVariantNames`. It refused `petSpecies.getAll` in full mode, and it could not read `jutsu.getAll` as a capture (`reader.list()` refuses a paged input).
**Branch:** `fable/forge-pet-catalogue-reads`, cut from `main@47d2977cf74cfc7387e9cc47ee5b69a526e58f91` (Forge 0.12.1 released: loader `@version 0.12.1`, `@require` pinned to `002c240f`). The frozen head is reported with the push; this file is the handoff for it.
**Game source:** `studie-tech/TheNinjaRPG@3314d122c93e036618483d18229a793ad7ad21fd` (the current contract pin). It was read only, through `git show 3314d122:<path>` and a detached local worktree at that SHA, and never executed.
**Live requests / writes:** 0 / 0. **Credentials:** none. `state/` and `docs/RULINGS.md` are untouched. The draft capture `push/345_*` is on this branch (see below).

## Audit (source at 3314d122)

| Read | Declaration | Query | Persist verdict |
|---|---|---|---|
| `petSpecies.getAll` | `routers/petSpecies.ts:32` `publicProcedure.query(({ ctx }) => listPetSpeciesForGetAll(ctx.drizzle))`: **no `.input()`** | `queries/petSpecies.ts:10` `petSpecies.findMany({ orderBy: asc(petSpecies.name) })`, with no `where`, so retired (`isActive: false`) species are included | **Content only.** PetSpecies columns (`drizzle/schema.ts:3004`): `id, name, description, artDirection, rankConcepts, rarity, role, preferredDamageElement, defaultJutsuIds, aiRules, includeDefaultRules, effects, isActive, createdAt, updatedAt`. It takes no `ctx.userId`. Ownership lives in `UserPet`, which this query never touches. It is admitted as a second input-less list. |
| `jutsu.getAll` | `routers/jutsu.ts:404` `publicProcedure`, mcp meta, `.input(jutsuFilteringSchema.extend({ cursor: z.number().nullish(), limit: z.number().min(1).max(1000), hideAi }))` | `queries/jutsu.ts:219` `listJutsuForGetAll`: `jutsu.findMany({ where: and(...jutsuDatabaseFilter(input)), orderBy: updatedAt desc, offset: cursor*limit, limit, with: { bloodline: { columns: { name: true } } } })`, then `filterByEffectConstraints`. It answers `{ data, nextCursor }`, with `nextCursor = results.length < limit ? null : cursor + 1` (computed on the unfiltered page) | **Content only:** whole Jutsu rows (every column is authored content, `requiredPetSpeciesId` and `hidden` included) plus `bloodline.name`. It has no `ctx`, and no user table appears in the query. It is admitted as a **paged** list, only as the pet catalogue (below). |

Both are `publicProcedure` and rate-limited in Forge's registry (`limited: true`). Neither row changed: `auth_pin_diff` finds 0 disagreements.

Source facts the policy rests on:
- `jutsuDatabaseFilter` (`routers/jutsu.ts:2433-2436`) adds `eq(jutsu.hidden, input.hidden)` when `hidden` is sent, and `eq(jutsu.hidden, false)` otherwise. **An absent `hidden` silently drops every hidden jutsu**, so a complete census takes two captures. (Observed: a public caller can list hidden jutsu with `hidden: true`. This is not a new class of data for Forge, since `jutsu.get` already full-persists hidden records. It is noted for the reviewer.)
- `jutsuType` is `inArray(jutsu.jutsuType, input.jutsuType)` (`:2352`); `JutsuTypes` includes `PETS` (`drizzle/constants.ts:839`).
- `filterByEffectConstraints` (`:2577`) returns every row unless `stat/effect/element/appear/static/disappear` is sent. With none of them, `data` is exactly the page and `nextCursor` is exact.

### Why the paged exception is narrow, and why it is one page

The capture policy refuses full persistence on lists unless a reviewed change widens it (captures.mjs header; RUL-2026-09-17-001). This change adds two things:

1. `petSpecies.getAll` joins `FULL_PERSIST_LIST_PATHS` on the same terms as `item.getVariantNames`: no input, content columns only, and a full request carrying any input is refused.
2. `FULL_PERSIST_PAGED_PATHS = ["jutsu.getAll"]`. In full mode the input must be **exactly** `{jutsuType: ["PETS"], hidden: true|false}`, checked at parse time with `stableStringify` equality. Any other member is refused (`limit`, `cursor`, `effect`, `rarity`, ...), as is another type, a second type, or a missing or non-boolean `hidden`. This keeps the read to the pet catalogue (not a dump of every jutsu), makes the hidden half explicit, and keeps the post-filter inert.

**One page, not a cursor walk.** Forge sends `cursor: 0, limit: 1000` (the source maximum) and accepts the answer only when `nextCursor === null`. A second page could never be persisted. The names of a Jutsu row's 50 columns alone are about 1.1 KB of JSON, so 1000 rows exceed `MAX_FULL_CAPTURE_BYTES` (512 KiB) before any value is counted. The checkout-gated test computes this from the schema. A multi-page walk with a two-scan agreement check (the skill-inventory pattern) was implemented first. It was dropped as unreachable code because it could never yield a persistable body, and it also pushed the bundle over budget (raw 466,276, gzip 112,162). The page is also rejected (`BAD_PAGE`, a failed read, nothing persisted) if any row lacks an id, repeats an id, or does not match the filter it was asked for (`jutsuType` in the list, `hidden` equal). So a server that ignored the filter cannot produce a body that claims to be the PETS catalogue.

**Field projection: deliberately not done.** The brief lists the fields needed: ids, names, rarity/rank, effects, cooldowns, costs, requirements, publish/hidden state. Every Jutsu column is authored content of the same class `jutsu.get` already persists whole. Forge has no projected-persistence tier, and the bundle had 11 gzip bytes of headroom left. The body is therefore the page's rows as decoded, without the `{data, nextCursor}` envelope, within the existing 512 KiB ceiling. If the reviewer wants projection, it is a separate change and needs budget.

## What changed

**Forge 0.12.2 (`@x-release-pending 0.12.2`; the loader keeps the released `@version 0.12.1` and its `@require` pin `002c240f`).**
- `src/storage/captures.mjs`: `FULL_PERSIST_LIST_PATHS` gains `petSpecies.getAll`. A new `FULL_PERSIST_PAGED_PATHS = ["jutsu.getAll"]` is added, and `canPersistFull` accepts all three lists. Both changes carry their audit citations.
- `src/runner/manifest.mjs` `normalizeCapture`: the exact-input rule for the paged path. Its message is `persist "full" needs input exactly {jutsuType: ["PETS"], hidden: true|false}`.
- `src/budget/reader.mjs`: a new `PAGE_LIMIT = 1000` and `CachedReader.page(path, input)`: one budget token, uncached, `{...input, limit, cursor: 0}`, with the acceptance rule above. On failure it returns `{ok: false, error: {code: "BAD_PAGE"}}` (classified SERVER, so it is journaled as a failed read and does not pause).
- `src/runner/runner.mjs` `_captures`: a full capture of a paged path reads through `reader.page()`. Its journal `input` is `{jutsuType, hidden, limit: 1000, cursor: 0}`, exactly what was sent. A summary `jutsu.getAll` capture behaves as before (`reader.list()` refuses it).
- `package.json` / `main.mjs` VERSION 0.12.2; `forge_bundle.js` rebuilt; `forge_loader_user.js` gains `// @x-release-pending 0.12.2` only.
- There is no new procedure row, no write path, and no budget change.

**Docs / skill.** `skills/building-tnr-content/references/pipeline.md`: a §2.2 `jutsu.getAll` note and a §2.8 "Capturing the pet catalogue" bullet. Packs and `_toc/pipeline.json` were re-rendered (`build_packs.py --write`; only hash stamps and offsets changed). `docs/BUILDER_APP_NOTES.md` gains a 0.12.2 section.

**Tests (socket-free).**
- `test/fakegame.mjs`: `jutsu.getAll` answered as the source does for the members Forge sends: jutsuType/hidden (hidden defaults to false), updatedAt desc, offset paging, `bloodline {name}`, and `nextCursor` null on a short page.
- `test/capture.full.test.mjs`: the allowlist expectations now include the new list and paged entries, and `jutsu.getAll` as a dump is still refused. Four new tests:
  - **Parse rules:** 13 refused `jutsu.getAll` inputs, `petSpecies.getAll` input refusal, summary unchanged.
  - **FakeGame census:** exact wire inputs, exported species including a retired one, visible and hidden PETS rows in source order with the envelope stripped, compact journal, no read-cache slot.
  - **Five bent server answers:** second page, filter ignored, repeated id, bare array, missing `nextCursor`. Each yields `BAD_PAGE` with one read, no next page, and no snapshot.
  - **Rate limit:** a rate-limited `jutsu.getAll` pauses the pass; the earlier species body is kept.
- `test/storage.captures.test.mjs`: the boundary test asserts both lists and the paged list exactly, with their registry rows, and still asserts that nothing else in the audited surface is persistable.
- `test/pets.test.mjs`: a checkout-gated test pins both declarations, both queries, the cursor/limit/nextCursor arithmetic, the hidden default, the post-filter guard and the PetSpecies column list, and checks that 1000 × the Jutsu column-name JSON exceeds the ceiling.

## Gates (exact)

| Gate | Result |
|---|---|
| `npm test` (forge/) | exit 1: 786 tests, 770 pass, **1 fail (pre-existing, push/337; debt 6)**, 15 skipped (checkout-gated). Base `47d2977c`: exit 1, 781 / 766 / 1 (the same test) / 14. |
| `TNR_GAME_CHECKOUT=<3314d122 worktree> npm test` | exit 1: 786 / 785 pass / 1 fail (the same push/337 test) / 0 skipped. All new source pins pass. |
| `npm run build` twice | exit 0 both times, byte-identical, sha256 `c213ca00ef77a83c5bb3aa8efb616cd5ecf0385676f19d6d969738ebb559dfd5` |
| `npm run fixtures`, then `git status` | exit 0; no fixture changed |
| `check_boundaries` / `check_imports` / `check_release_pin` | exit 0: 0 violations (pin 3314d122) / exit 0: 0 / exit 0: release pin ok |
| `check_bundle_budget` | exit 0: **raw 465,508 / 466,000 (99.9%), gzip 111,989 / 112,000 (100.0%)**. Base 464,150 / 111,645 (+1,358 / +344). Not raised. |
| `node tools/auth_pin_diff.mjs <3314d122> <3314d122>` | exit 0: 0 disagreements across 60 Forge paths |
| `check_manifest.mjs`, `validate.py` and `validate.py --strict` (cwd skill `data/`) on all 129 base `push/*.json`, base tree vs head tree | full output and every exit code identical (7 pre-existing `check_manifest` refusals on both) |
| `check_manifest.mjs` / `validate.py --strict` on `push/345_pet_catalogue_capture.json` | head: exit 0, 0 problems / exit 0, 0 errors 0 warnings. At base 0.12.1, `check_manifest` exits 1, refusing `petSpecies.getAll` full (fail-closed) |
| `doctrinemap.py .` / `render_doctrine.py --check` / `build_packs.py --check` (after `--write`) | exit 0: 0 errors 0 warnings / exit 0: all projections current / exit 0: all packs and TOCs current |
| `lawmap.py .` | exit 0: 93 laws, 0 errors, 5 pre-existing warnings |

No Python validator change: `validate.py` checks only that a capture entry has `proc` and an object `input`.

## Draft capture manifest (push/345)

`push/345_pet_catalogue_capture.gen.py` writes `push/345_pet_catalogue_capture.json`, which makes three full reads: `petSpecies.getAll`, then `jutsu.getAll` PETS with `hidden: false`, then with `hidden: true`. `--report <bundle>` lists species and jutsu. It fails on an unpersisted read, an unknown default jutsu, or an unknown species lock. Results: `validate.py --strict` 0 errors, 0 warnings; `check_manifest.mjs` 0 problems at 0.12.2; refused at parse time by 0.12.1 (fail-closed). The README section marks it DRAFT, NOT RUNNABLE until 0.12.2 is released. It lands on `main` only through the reviewed merge of this branch.

## Known debt, deviations, open decisions

1. **Policy widening** (reviewer: attack it). This adds a second whole list and the first paged list. The paged list is fenced to one exact input.
2. **No field projection** (see above). Full rows are persisted.
3. **One page only.** More than 1000 PETS rows in one hidden state fails as `BAD_PAGE` rather than being walked. A body that large could not be persisted anyway.
4. **Offset paging over `updatedAt desc`.** A single page is one SQL statement, so it is consistent. The two hidden halves are separate reads, so a jutsu whose `hidden` flips between them could appear in both or in neither. The report keys rows by id.
5. **Bundle at 99.9% / 100.0%**: raw 465,508 / 466,000, gzip 111,989 / 112,000, with 492 / 11 bytes of headroom. The budget was not raised. The next Forge change of any size will need a director budget ruling or a size pass.
6. **Pre-existing on base, not touched:** `npm test` on `main@47d2977c` has 1 failure, `runner.test.mjs` "compatibility: staged manifests parse, plan and pass Forge pre-send validation". It is caused by `push/337_voth_scale_to_player.json` (`@ai:pz_boss is unknown`), which is Lane B content from `82eadd97`. It fails identically on head.

## Not done / not begun

- No browser, live or session checks. No Forge release: the release workflow promotes 0.12.2 after merge.
- The 345 capture has not been run. No Little Horror balance or loadout work has begun. No answers/ catalogue of pets. `docs/RULINGS.md` and `state/` were not edited.
