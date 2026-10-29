# Badge and title builder support + badge/title capture reads at TheNinjaRPG@2af4b320 — 2026-10-29

**Lane:** A (builder/forge, validators, generated contracts). **Rulings:** RUL-2026-10-29-039 item 3 (title capture, "on `fable/badge-builder`"); the Skyglass event needs the Crownbreaker badge and six titles.
**Branch:** `fable/badge-builder`, rebased onto `main@d1c95609` (it was cut from `75890122`; main has since released Forge 0.10.1 through the recipe-capture merge `5a20f3b9`). The frozen head is reported with the push; this file is the handoff for it.
**Game source:** `studie-tech/TheNinjaRPG@2af4b32066c39e2868efae5dba6b339278701dca` (the current contract pin, unchanged), read only, never executed.
**Live requests / writes:** 0 / 0. **Credentials:** none. No Skyglass badge/title manifest and no capture manifest were written; `push/`, `docs/design/` and `state/` are untouched.

## What changed

**Builder (Forge 0.11.0, `@x-release-pending 0.11.0`; the loader keeps the released 0.10.1 `@version` and its `@require` pin `5a20f3b9`).**
- New manifest entities `badge` and `title`; ref prefixes `@badge:` / `@title:` (usable in `reward_badges` / `reward_titles`). Recipe (`recipes.mjs catalogRecipe`): two-phase like jutsu/items. `badge.create` / `title.create` take no input and insert `New Badge - <id>` / `New Title - <id>`, id in `message`; `update {id, data}` saves the whole record, so Forge fetch-merges over the `fields.json` set; read-back `get`; names `getAllNames`.
- Procedure rows (transcribed from the routers, all nine agree with `parseRouterDecls` at the pin): `badge.create/update` protected, `badge.get/getAllNames` public (limited, mcp); `title.create/update/get/getAll` protected, `title.getAllNames` public (limited). Table 60 -> 69 paths, limited 23 -> 26, protected 38 -> 44 (with the base's own).
- `src/runner/catalog.mjs`: neither table has a `hidden` column (`HIDDENLESS` replaces the petSpecies-only strip; the pinned-field merge drops `hidden`, read-back never diffs it). Required on create: badge `name`, `image`, `description`; title `name` and an explicit `archived`. Validator bounds checked BEFORE the create, because zod refuses them only at the update, after a listed placeholder exists: name 1-191 trimmed; badge description 1-500 (the column is varchar(500), the validator allows 512); title description <= 512; image an `@img` ref or a URL <= 191 (column); <= 20 effects; power finite >= 0; `masteryTypes` 1+ of `MasteryTypes` (mirrored from `constants.ts:413`, compared by the checkout-gated test).
- Title effects are checked against a new `nested.json` `titleEffects` section (TitleEffectSchema's two inline strict members), never the combat tag table (combat's `increasemastery` has `rounds`/`target`/...). No `titleEffects` section -> title effects refused (fail closed).
- Lint `TITLE`: a manifest that archives a title and rewards it is refused (`server/utils/titleRewards.ts`: quest and item saves refuse `reward_titles` naming an archived title).
- Reconciler: a lost badge/title create is ORPHANED with its candidates (each marked placeholder or not); only the operator's adopt binds a row, which then continues at the update; the create is never re-sent.
- **Captures:** `badge.get` and `title.get` join `FULL_PERSIST_PATHS` (content-record point reads keyed by `{id}`; `title.get` is staff-only and NOT_FOUND for per-player legacy labels). `reader.list()` accepts `title.getAll` (no input, every catalog title including archived; staff-only) like `petSpecies.getAll`. List captures remain summary-only (row count).
- `derive_fields.mjs` badge/title targets; `derive_nested.mjs` `inlineFamily()` for inline-member discriminated unions (only emitted when `TitleEffectSchema` exists at the pin); `pin_relevance.mjs` gains the two routers, two validators and `titleRewards.ts`.

**Skill.**
- `schema_extract.py`: `badge`/`title` entity targets; `validators/title.ts` in the constructor files; `parse_inline_unions` (inline `z.object` union members -> synthetic `Union[i]` objects); `.nonnegative()` -> min 0. 45c gains `TitleEffectSchema`; 45d gains `badge`/`title`; 45g gains their rows (required_on_create, booleans, null_strip_exempt, empty sets elsewhere). 45e/45f unchanged in content. Root 45c/45g equal skill `data/`.
- `validate.py` + new `catalog_checks.py`: keys, hidden, required-on-create, lengths (badge description 500), image form/length, TitleEffectSchema membership via 45c, power/masteryTypes, effects cap from 45d, the archived-and-rewarded refusal, a note on `archived:false`; title effects skip the combat-tag laws; `@badge`/`@title` refs; build order puts badge/title first.
- `references/pipeline.md` §2.9 (labelled source-verified, NOT behaviour-proven); packs/TOC re-rendered (hash stamps only).

## Capture route for the title-bonus sizing (RUL-2026-10-29-039 item 3)

- **Lists (row count only):** `title.getAll` (staff session; every catalog title, archived included — the complete count), `title.getAllNames` (public; unarchived only), `badge.getAllNames` (public; every badge). No Forge capture exports list ids: a list capture records `rows`, never the rows.
- **Point reads (`persist: "full"`, input `{id}`):** `title.get` (staff session; returns `id, name, description, effects, legacyOwnerId, archived, createdAt, updatedAt`), `badge.get` (public; `id, image, name, description, createdAt, updatedAt`).
- **Ids:** no repository file holds a title id (every captured `reward_titles` is empty). The operator can read them from the game's staff page `/manual/title` (it lists every catalog title, archived included, via `title.getAll`; each edit link is `/manual/title/edit/<id>`).
- Shape: `{"capture": {"before": [{"proc": "title.getAll"}, {"proc": "title.get", "input": {"id": "<id>"}, "persist": "full"}, ...]}, "items": []}`. Needs Forge 0.11.0 released and a signed-in staff session.

## Gates (exact)

- `npm test` (forge/): 755 tests, 743 pass, **1 fail**, 11 skipped. The one failure is `gates.test.mjs` "the checked bundle is inside its raw and gzip budget" (below). Base `d1c95609`: 741 / 731 / 0 / 10. `TNR_GAME_CHECKOUT=<2af4b320> node --test test/catalog.test.mjs test/pets.test.mjs`: 28/28.
- `npm run build` twice: byte-identical (sha256 `a906a2bd4eb6f5fc...`). `npm run fixtures` then `git diff --exit-code`: clean (run with a real `node_modules` copy; a symlinked one rewrites stack-trace paths in five envelope fixtures).
- `check_boundaries` 0 violations, `check_imports` 0, `check_release_pin` ok.
- **`check_bundle_budget` exit 1:** raw 450,415 / 446,000 (101.0%), gzip 108,305 / 108,000 (100.3%). Base 445,900 / 107,332. Growth +4,515 raw / +973 gzip.
- `check_manifest.mjs` and `validate.py` (cwd skill `data/`) on all 120 `push/*.json`: per-file exit codes, output digest (check_manifest) and error/warning counts (validate.py) identical to base.
- `schema_extract.py <2af4b320> --ctors/--entities/--constants/--procedures/--checks`: identical to the committed files except the `extracted` date stamp. `schema_diff.py --invariants`: 145 variants, 0 errors. `schema_diff.py diff OLD NEW` per file: exit 0 for all five (45c 13 additions, 45d 7, 45g 8, 45e/45f 0) — no ledger needed.
- `derive_fields.mjs` / `derive_nested.mjs` at the pin: byte-identical to the committed `fields.json` / `nested.json`. 45d badge/title fields equal `fields.json`.
- `test_pet_species.py` + `test_schema_diff.py`: 19 OK; `selfcheck.py --generated` 0 errors; `factory.py --selftest` 20/20; `doctrinemap.py .` 0/0; `render_doctrine.py --check` current; `build_packs.py --check` current (after `--write`); `lawmap.py .` 0 errors, 5 pre-existing warnings.

## Budget: raised to 455,000 / 109,500 by the director (RUL-2026-10-29-043)

After the raise:
- `check_bundle_budget` exits 0: raw 450,415 / 455,000 (99.0%), gzip 108,305 / 109,500 (98.9%).
- `npm test`: 755 tests, 744 pass, 0 fail, 11 skipped.
- `npm run build` is byte-identical, sha256 `a906a2bd4eb6f5fc...`, so the bundle is unchanged.

The original analysis, kept for the record:

Smallest raise that passes: **raw 451,000 / gzip 108,500** (585 / 195 bytes of headroom). Any later Forge change will need another step at that ceiling; 455,000 / 109,500 would leave ~4.5 KB / ~1.2 KB. No trim inside this feature closes a 4.4 KB raw gap: dropping the pre-create bounds in `catalog.mjs` saves ~1.1 KB and re-opens the stray-placeholder case; dropping `title.getAll` saves ~0.15 KB.

## Known debt, deviations, open decisions

1. **Bundle budget: resolved.** The director raised it to 455,000 / 109,500 (RUL-2026-10-29-043).
2. **Decision, deferred (the Skyglass titles are out of this release, RUL-2026-10-29-041): title visibility on create.** A title has no hidden column; `archived` is its only switch. This branch requires `archived` to be stated on every create and does not choose. `archived:true` (the hidden-on-create analogue) makes every quest/item save that rewards it fail until the director unarchives it — a publish step between the title create and the reward edits. `archived:false` lists the name in the public `title.getAllNames` at once (nothing grants it until a published reward names it).
3. **Decision: badges are player-visible from the create.** The public `/manual/badge` page lists every badge (the placeholder too, for the instant between create and update). There is no switch to hide one.
4. Badge names are unique (the update refuses a duplicate); title names are not checked by the server.
5. The Forge `MasteryTypes` list is hand-held (no Forge contract carries enum values); the checkout-gated test compares it with `constants.ts`.
6. Behaviour not proven: the first badge and title pushes are the proof.

## Not done / not begun

- No browser, live or session checks; no Forge release; the old builder (`builder_bundle.js`) was not extended.
- No Crownbreaker badge or Skyglass title manifests, no title/badge capture manifest, no answers/ catalogue for badges or titles.

## Review round 1 (ChatGPT on `778bdda3`; fixed on top of `800f6660`)

| Finding | Fix |
|---|---|
| **F1 (P2)** a malformed image URL (`https://[`) or an `@img` upload whose URL exceeds `Badge.image` varchar(191) passed preflight and failed only at `badge.update`, after the placeholder existed | `catalog.mjs`: the image check is now the regex AND a `new URL()` parse (`BadgeValidator.image` is `z.url()`; zod 4.6.7, the `app/bun.lock` version, trims then `URL.canParse`s, so http(s) with no whitespace is a strict subset with an unchanged saved value). `runner.mjs _create`: a badge resolves its `@img` refs (the upload) BEFORE `badge.create`, like the one-step entities, and re-runs the pre-create checks on the resolved data, so the uploaded URL's length is checked before a placeholder exists. Titles have no image/URL field. |
| **F2 (P2)** the validators trim `name`; a padded name was accepted and read back as drift | Forge and `validate.py` refuse a badge/title `name` with leading/trailing whitespace before any write (create and edit). The other trimmed field is `Badge.image` (`z.url()` trims and strips tab/CR/LF); both sides already refuse any whitespace in a URL. Descriptions and title effects are not trimmed. |
| **F3 (P3)** `validate.py` required title `description`/`effects` on create (45g); Forge requires `name` + explicit `archived` | `catalog_checks.py` takes required-on-create from a `REQUIRED_ON_CREATE` table equal to Forge's `REQUIRED` (badge `name`/`image`/`description` — unchanged, already equal to 45g; title `name`/`archived`). 45g is left as derived (Title.description/effects have column defaults `""`/`[]`, `drizzle/schema.ts:4713-4714`, and Forge fetch-merges over them). |
| **F4 (P3)** `validate.py` accepted a nonfinite title effect `power` (`1e309`) | `catalog_checks.py`: `math.isfinite(power) and power >= 0` (TitleEffectSchema `.finite().nonnegative()`); Forge already checked `Number.isFinite`. |

Tests: `forge/test/catalog.test.mjs` (validator cases for malformed URLs and padded names on both entities and on an edit; a runner case where a malformed URL, an over-long uploaded URL and a padded name each fail with zero `badge.create` calls and no row); new `scripts/test_catalog_checks.py` (5 tests, one per finding plus baselines). The finding cases fail against `800f6660`'s `catalog.mjs`/`runner.mjs`/`catalog_checks.py` (the over-long-URL case needs the `runner.mjs` change).

Not changed: `factory.py` still requires title `description` on a create (it skips `effects`); it builds manifests and is stricter, not unsafe.

### Gates (round 1, exact)

- `npm test` (forge/): 756 tests, 745 pass, 0 fail, 11 skipped. `TNR_GAME_CHECKOUT=<2af4b320> node --test test/catalog.test.mjs test/pets.test.mjs`: 29/29.
- `npm run build` twice: byte-identical, sha256 `e7cdaff2d8e9efe289ba3adec93f66f25d438275e90f446b507045916a6f78fc`. `npm run fixtures` then `git diff --exit-code`: clean (real `node_modules` copy).
- `check_boundaries` 0 violations, `check_imports` 0, `check_release_pin` ok, `check_bundle_budget` exit 0: **raw 450,662 / 455,000 (99.0%), gzip 108,381 / 109,500 (99.0%)** (+247 / +76 over round 0).
- `check_manifest.mjs` and `validate.py` (cwd skill `data/`) on all 120 `push/*.json`: per-file exit codes, check_manifest output digest and validate.py error/warning counts identical to `800f6660`.
- `python3 -m unittest scripts/test_pet_species.py scripts/test_schema_diff.py scripts/test_catalog_checks.py`: 24 OK. `selfcheck.py --generated data` 0 errors; `factory.py --selftest` 20/20; `doctrinemap.py .` 0/0; `render_doctrine.py --check` current; `build_packs.py --check` current; `lawmap.py .` 0 errors, 5 pre-existing warnings.
- Live requests / writes: 0 / 0. No browser or session checks. `dist/building-tnr-content.zip` is left to the skillpack workflow.
