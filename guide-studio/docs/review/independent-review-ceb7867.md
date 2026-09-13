# Independent review received: changes required

Recorded by Astra from the independent review supplied by the project director on 2026-09-13. Findings below retain the review's scope and severity; area verdicts and observations are condensed. This is evidence about the original frozen implementation, not independent approval of subsequent corrections.

- Repository: `perseverance484/tnr-tools`
- Reviewed implementation: `ceb786763cd73e7bc1f42e98ffa7c43ae3d5ed40`
- Base/main: `6848a7805d912378f7f8eb27f52c9625dd10ac54`, independently fetched with no drift
- Design handoff: `87fb673938d915c0732351d2efb208d05ef38c7c`; spec/brief blobs identical in the implementation
- Pinned game: `studie-tech/TheNinjaRPG@36c5873b7b6ee5fd3af717008d7c51b0f185b756`

## Verdict and requested corrections

**Changes required.** Four scoped corrections; one breaks a production install. The review found no compromise of the approve-once/import safety model and no need to revisit the architecture. Recommended next handoff: findings 01–04, then narrow re-review.

| Finding | Severity | Reproduction / correction requested |
|---|---|---|
| 01: undeclared `entities` dependency | Medium-High | The compatibility runtime imports `entities`, but only jsdom's hoisted dev dependency supplied it (6.0.1). `npm ci --omit=dev` cannot load the sanitizer. Declare runtime `entities: 8.0.0`, matching pinned game `app/package.json:112`; add an install-shape gate. |
| 02: oversized phone JavaScript | Medium-High | App statically imports all catalog `imageData` while the same art is also emitted in `/assets`. Reviewer measured ~940 KB gzip; unversioned App.js and missing cache headers worsen repeat visits. Exclude inline image bytes or split catalog delivery; add a gzip-size budget. |
| 03: production validator is a handwritten restatement | Medium | `src/artifact.mjs` uses `src/schema.mjs`'s duplicate instead of the authoritative compiled pinned validator. Categories/reserved slugs are duplicated, and the differential test draws cases from the duplicate. Presently identical and not exploitable, but a provenance/maintenance defect. Use the pinned runtime directly and derive cases from extracted constants. |
| 04: phone header touch target | Low-Medium | Chromium 360×740 measures “Staff review ↗” at 69×13 px. Other measured controls are acceptable. Give this link button-sized padding. |

## Independently reported verification

`npm ci --ignore-scripts`, `npm run gate` (32/32), reproducible catalog and fixtures all passed. The production-only module import failed as finding 01. The existing repository parity failure at `validate.py:201` (`checks: null`) was verified on base and is not a regression.

The reviewer reports real headless Chromium mobile emulation at 360×740 and 390px, local Studio/service testing, and a real browser driving the importer against local mocks. No branch was modified, no commit/push/merge/deployment/publication occurred, and no live TNR request, write, credential or session material was used.

Reported area verdicts:

- Mechanics/provenance: pass. Black Thorn Rose correctly preserves raw offence as stat axis while showing enemy healing reduction and self damage-taken reduction, with no offensive damage classification.
- Aerathiel: pass, 5 core jutsu, 15 build choices/notes, 8 chapters, 21 assets.
- Night Parade: pass, 5 core, 3 Gate links, 3 patrons, 4 abilities, shared departure routine, 12 choices/notes, 8 thematic chapters, 29 assets.
- Core-kit independence: pass, empirically unchanged with empty/unrelated loadouts.
- Mobile/recovery: pass with findings 02/04. No horizontal overflow or console/page errors; editing, ordering, notes, preview and byte-exact restore exercised. Editorial treatment meets the reviewer's bar; final art/copy acceptance belongs to the director.
- Public boundary: pass; complete authoring flow made zero off-host requests.
- Approval identity: pass; review skip/stale revision/origin rejected; assets unavailable before approval; 9/9 tampered cases rejected and the control accepted.
- Native compatibility: pass; exact pinned source copies, validator, route/transport inputs, and sanitizer/heading idempotence checked. The production duplicate remains finding 03.
- Importer: pass with local mocks, verified upload, explicit import, unpublished result/readback, receipt, idempotent repeat, and no second create.
- Cloudflare: implementation sound, deployment unproven. Missing configuration fails closed; Node timings do not prove workerd behavior.

## Retained observations and limits

Lower-severity observations, not part of the four requested corrections:

- Draft backup/recovery/clear controls consume substantial phone space; consider overflow disclosure.
- Reload restores content but resumes at step 01.
- Native profanity moderation has no pre-submission mirror; rejection can occur at import.
- Harvest projections reuse original filenames with different bytes. Original hashes are documented, but faithful derivation is not mechanically rechecked.
- Worker routes remain an operator setup requirement; wrangler bindings remain placeholders.
- Imported art permanently depends on the Studio origin/retention policy; director-level decision.
- Effect target `CHARACTER` is absent from the normalizer's explicit target mapping; unknown targets lowercase instead of failing. Not reached by current catalog.

Disclosures verified as accurate: an authenticated staff member can attest a fabricated import receipt; this is not a game-signed callback. Native parameterless create lacks cross-device idempotency; journaling, ambiguity handling and placeholder fingerprints mitigate it without publication or destructive cleanup. Breadth remains two complete bloodlines.

Unproven: physical phones, virtual keyboards, iOS Safari, real touch/focus trapping, quotas/downloads; deployed Access/Turnstile/D1/R2/Pages/CSP/workerd; installation in a real TNR staff session and observed native readback; cross-device creation races. Six earlier credential-free TNR catalog-refresh GETs and official CDN reads are corroborated only through author provenance, not independently observed.
