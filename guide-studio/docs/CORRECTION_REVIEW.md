# Astra correction handoff: findings 01–04

Status: corrections implemented, pending narrow independent re-review. This is not integration, deployment, publication, or director acceptance of copy/art.

- Repository: `perseverance484/tnr-tools`
- Implementation branch: `astra/guide-studio-implementation`
- Exact base / integration target `main`: `6848a7805d912378f7f8eb27f52c9625dd10ac54`
- Previous reviewed implementation / correction parent: `ceb786763cd73e7bc1f42e98ffa7c43ae3d5ed40`
- Design contract: `87fb673938d915c0732351d2efb208d05ef38c7c`
- Pinned TNR source: `studie-tech/TheNinjaRPG@36c5873b7b6ee5fd3af717008d7c51b0f185b756`

The correction's exact frozen SHA is the commit containing this report, returned in the handoff response and verified against the remote branch. Main and the design branch are untouched. No synchronization/rebase was needed. Astra remains the sole implementation writer by director assignment.

## Accepted findings and changes

| Finding | Correction | Evidence |
|---|---|---|
| 01 | Declared production `entities: 8.0.0`; lockfile updated. `scripts/install-smoke.mjs`, invoked by the build gate, creates an isolated production-only install outside the checkout and loads the actual pinned sanitizer/heading/validator/constants/artifact modules. | Original `--omit=dev` failure reproduced after a clean install. New offline production smoke passes; jsdom is absent and exact entities 8.0.0 is asserted. |
| 02 | Generator emits `catalog/browser.v1.json`, preserving canonical records/version and replacing inline bytes with an official asset hash index. App uses that projection. Preview loads only its required same-origin art, checks SHA-256, shares successful/in-flight loads and allows retry. Server/export retains self-contained SVGs. JS/CSS have content-hashed filenames; immutable static/art cache headers and HTML/config revalidation added. | Public JS: 960,923 → 229,505 bytes gzip (76.1% reduction), measured in the same workspace. No embedded official WebP bytes or full catalog dependency. Gate caps all public JS at 250,000 gzip bytes, under 10% headroom over this measured baseline. New tests prove exact browser/server artifact identity for both fixtures, empty-foundation independence, no excess art fetches, failures/retry and off-origin refusal. |
| 03 | Deleted handwritten `GuideArticleValidator` and category/slug lists from `src/schema.mjs`. Artifact creation and verification import `compatibility/runtime/guide-validator.mjs` directly. Constants now compile into their own runtime entry through the existing pinned-source producer. | Test matrix reads pinned `GuideCategories`/`GUIDE_RESERVED_SLUGS`; production verification rejects invalid native fields even after all package hashes are recomputed. Exact pinned source hashes and other runtimes remain unchanged. |
| 04 | `.masthead-right > a` is an inline-flex target with at least 44×44 px and 10px/8px padding. | CSS correction inspected. Prior independent Chromium evidence establishes the original defect; fresh 360px/390px geometry/browser confirmation belongs in narrow re-review. No new browser measurement is claimed here. |

No finding was rejected. The approval state machine, package format/signature, importer transport and mutation/recovery model were not changed. Public asset loading is confined to immutable Studio paths with omitted credentials and refused redirects; the public app still performs zero TNR requests.

Changed scope: `guide-studio/package*.json`, `public/_headers`, browser catalog projection, generated runtime constants, build/catalog/compatibility/install-smoke scripts, App/preview loader/renderer guard/template validation/schema/artifact import/CSS, focused tests, and review/provenance/deployment documentation. No unrelated repository content or doctrine changed.

## Verification

Exact final command output is in [review/correction-verification.log](review/correction-verification.log). Commands run from `guide-studio/`:

- `npm ci --ignore-scripts` — clean exact-lock install.
- `npm run gate` — pinned compatibility/runtime; reproducible canonical and browser catalogs; fixture inputs; 38 tests; production builds; bundle/size/boundary checks; isolated offline production install smoke.
- `npm run fixtures` — both original fixture package hashes reproduced exactly.
- `npx --no-install prettier --check 'src/**/*.{jsx,mjs,css}' 'templates/*.mjs' 'server/*.mjs' 'scripts/*.mjs' 'importer/*.mjs' 'test/*.mjs' package.json wrangler.jsonc` — formatting.
- `git diff --check` and final staged whitespace check — correction whitespace.

Focused native-contract, editor/staff DOM and preview-asset tests also pass (12/12). New assertions verify cached reuse on prose edits, missing/tampered images and retry, no fetch for an unapproved URL, and that unresolved browser art cannot enter the final renderer. Official images/cards themselves were not edited, so static galleries were not regenerated.

| Fixture | Assets | Exact unchanged package hash |
|---|---|---|
| Aerathiel | 21 | `fc893d47ce2b60c106579b75f66240ab8cb6eacc9c82717d511a44bf9c1491bc` |
| Night Parade | 29 | `32c72b6f78b72ce6a94b2884c9594266e67e1fa38d527d697f5caba356e7a554` |

Catalog remains `catalog-1caefb53206168966f10`, both templates v1, normalizer v1, 35 jutsu, four summons and 41 official images. Canonical catalog, templates, fixture inputs and art bytes are unchanged. The new delivery projection is mechanically generated by `scripts/catalog.mjs`; no catalog refresh was performed.

## Remaining scope and review request

Please recheck the four findings and the new preview art-loading/build path. The reviewer determines whether the correction surface supports a narrow recheck. Existing mobile Chromium passes apply to the previous frozen SHA, not automatically to this correction. Physical-device behavior, new image-cache behavior, 360px header geometry, production CSP/edge caching and actual downloads remain unverified here.

Cloudflare remains Pages + Worker + R2 + Turnstile + Access + D1, unconfigured/undeployed. Worker routes/bindings and staging runtime checks remain operator work. The separate native importer remains built and mock-tested, with production trust configuration required and no live installation. Imported assets retain the documented permanent Studio-origin dependency.

The [received review](review/independent-review-ceb7867.md) retains the lower-severity observations: draft controls/resume step, optional moderation mirror, mechanical harvest-projection derivation, target `CHARACTER`, routes, and director art/retention decisions. Staff import receipts remain attestations, and native cross-device create idempotency remains an upstream limit. These were not silently broadened into the four-finding correction pass.

Repository-wide `checks: null` parity failure is unchanged baseline debt, previously reproduced by author and reviewer. Its inputs and validator are untouched; no claim that the repository-wide gate passes is made.

## Live activity

Correction pass: zero live TNR requests, zero game writes, zero game credentials/cookies/session material, zero deployment/publication. Tests use local files, in-process transports and mock staff/Turnstile/native mutations. Normal npm installation reads the package registry; the install-shape gate uses only the populated offline cache. GitHub reads and branch persistence use the existing repository connector, without a PAT. The original implementation's six authorized public catalog GETs and CDN reads remain historical provenance, not new correction activity.
