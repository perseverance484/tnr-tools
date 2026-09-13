# Astra implementation review handoff

Historical first handoff: frozen `ceb786763cd73e7bc1f42e98ffa7c43ae3d5ed40`. The independent review subsequently returned **Changes required**. Current status and the four scoped fixes are in [CORRECTION_REVIEW.md](CORRECTION_REVIEW.md); the remainder of this document records the original handoff.

Repository: `perseverance484/tnr-tools`
Implementation branch: `astra/guide-studio-implementation`
Exact base: `6848a7805d912378f7f8eb27f52c9625dd10ac54`
Integration target: `main`, independently reverified at that same SHA before freeze
Design contract: `chatgpt/guide-studio-spec@87fb673938d915c0732351d2efb208d05ef38c7c`
Pinned game: `studie-tech/TheNinjaRPG@36c5873b7b6ee5fd3af717008d7c51b0f185b756`

The original frozen implementation SHA is `ceb786763cd73e7bc1f42e98ffa7c43ae3d5ed40`, verified against the remote branch at that handoff. The design branch and main were not modified. Astra owns this implementation by explicit director assignment; independent review remains required before integration. This is not a production-completion or live-session claim.

## Implemented scope

The complete bloodline foundation precedes player strategy and is independent of loadout selection. The mobile-responsive editorial UI supplies two illustrated templates, static search, ordering, inline autosaved notes, thematic manuscript chapters, optional processed screenshots, recovery/backups and a sandboxed final-content preview. Staff reviews that same server snapshot, requests linked revisions, approves/freeze-signs the exact package, and records the isolated native import receipt. The actual tRPC adapter implements one-action unpublished create/update with strict readback, persistent ambiguity state, and explicit recovery.

Changed directories: `guide-studio/` (implementation, catalogs, fixtures, official cached art, tests, operator/review docs). Also added the exact handoff copies at `docs/design/GUIDE_STUDIO_PRODUCT_SPEC.md` and `state/prompt_guide_studio.md`, which were absent on main. Unrelated repository state and mission work are untouched.

## Verification

Commands run from `guide-studio/` unless stated otherwise:

| Command | Result |
|---|---|
| `npm ci --ignore-scripts` | Reinstalls exact package lock; final gate uses the clean install |
| `npm run gate` | Pinned-source/runtime check; reproducible catalog; fixture check; 32 tests; public/Worker/importer builds; bundle boundary and no-harness checks |
| `npm run fixtures` | Rebuilt both complete fixture artifacts and self-contained previews |
| `python3 scripts/card-gallery.py` | Regenerated/inspected 360px SVG card samples; no browser claims |
| `npx --no-install prettier --check 'src/**/*.{jsx,mjs,css}' 'templates/*.mjs' 'server/*.mjs' 'scripts/*.mjs' 'importer/*.mjs' 'test/*.mjs' package.json wrangler.jsonc` | Source formatting checked |
| `git diff --cached --check -- guide-studio state/prompt_guide_studio.md` | Implementation whitespace clean; the full diff retains four intentional Markdown hard breaks in the byte-exact design-spec copy |

Final command output is retained in `docs/review/verification.log`. Tests cover: complete core kits and summon sets; Black Thorn Rose; unknown mechanics; required notes; template version/shape rejection; optional/hidden/reordered chapters; escaping; image size/type validation; deterministic hashes and ZIPs; preview/export agreement; actual React author/staff DOM flows; autosave and recovery; zero TNR calls in the authoring harness; Access JWT signature/audience/expiry; Turnstile hostname/action; public request validation/origin; atomic reviewer races; exact immutable approval/export; actual SQLite schema/D1 SQL; actual tRPC transport through a local fetch handler; failed/lost native responses; duplicate prevention; published destination refusal; signature/tamper rejection; and journal failure/reconciliation.

Repository startup gate, run from repository root: `python3 skills/building-tnr-content/scripts/session_open.py`. Baseline result was exit 1: lawmap 0 errors/5 warnings, doctrine projections current, packs/TOCs current, existing parity capture failed. Isolated reproduction: from `skills/building-tnr-content/data`, `python3 ../scripts/validate.py --parity ../../../harvests/inbox/tnr_results_1789273598969.json` raises `TypeError` at `set(None)` because that pre-existing capture has `checks: null`. No engine-law/doctrine/generated-contract changes are made by this implementation. The baseline defect is not represented as a passing repository gate.

## Fixture status

- Aerathiel: complete 5-jutsu core; 15 authored build choices and inline notes; eight chapters; native validator/sanitizer/heading parity; exact package determinism. 21 generated assets.
- Night Parade: complete 5-jutsu core; all three Gate summon techniques; three patron cards; four patron ability cards; one shared departure routine; 12 choices/notes; eight thematic chapters. 29 generated assets. All captured equipped summon jutsu are accounted for.
- Both fixtures derive from the supplied real guides. Their generated previews live under `test-output/fixtures/` after `npm run fixtures`; inspection galleries are committed under `docs/review/`. The UI is designed around these two bloodlines, with no generic placeholder templates exposed.

Catalog and image hashes, capture provenance, exact levels, source differences and producer commands are documented in `CATALOG_PROVENANCE.md`. The committed catalog is `catalog-1caefb53206168966f10`, templates v1, normalizer v1. Unknown tags fail generation. Catalog/template versions are pinned in every submission and package.

## Native compatibility and importer status

Inspected pinned `app/src/server/api/routers/guide.ts`, `app/src/validators/guide.ts`, `app/src/libs/guide/html.ts`, `app/drizzle/constants.ts`, `app/src/utils/sanitize.ts`, `app/src/utils/parse.ts`, `app/src/layout/GuideArticleView.tsx`, the guide editor/hooks, tRPC provider and image configuration. Small exact source copies and a constant extract are in `compatibility/`, attributed and hashed; esbuild produces their runtime. Parity uses the actual copied validator, sanitizer and heading preparer, not a permissive invented export schema.

The game sanitizes classes and most image attributes. Premium mechanics/hero art therefore uses deterministic self-contained SVG assets, with semantic native HTML headings and authored prose. Player notes remain native text for accessibility and game moderation. The preview embeds the same asset bytes and uses the game's 512px fallback body-image width. The native optional cover field is null to avoid duplicating the ordered body hero. The surrounding game title/TOC/application chrome is not reproduced pixel-for-pixel; native browser layout remains a staging check. Native img alt stripping is an upstream limitation; captions and native prose preserve context.

Normal import is implemented and tested through the actual tRPC HTTP batch transport with every fetch intercepted by a local server adapter. No request escapes to TNR. `category: bloodlines`, `published: false`, `relatedBloodlineId` and every approved content field are verified. Package approval/import does not publish. The independent userscript/Forge mount is buildable; it is not installed into a live staff session. Production importer trust must be supplied by the operator.

## Debt, deviations and required independent checks

- Cloudflare is not deployed. D1 and Access are additions to the preferred Pages/Worker/R2/Turnstile layout, needed for concurrent approval and staff identity. Binding, route, CPU-budget, storage, key rotation, retention and staging checks are in `DEPLOYMENT.md`.
- Real browser/mobile testing is blocked in this environment: Chrome rejected localhost preview access; its file URL policy also rejected the self-contained fixture. No alternate browser or bypass was used. DOM tests and static SVG inspection cannot establish touch scrolling, focus trapping, virtual-keyboard behavior, browser storage quotas, real screenshots/downloads, CSP, or image decoding in Android/iOS.
- Independent reviewer should test 360px/390px authoring, jutsu ordering and notes across reload, hidden/optional chapter navigation, preview at phone/desktop sizes, screenshot conversion/captions, backups, receipt feedback/revision, staff approve/export, and target-browser importer ZIP/receipt interactions. Real Access/Turnstile and TNR sessions remain unverified.
- Template copy/art treatment is proposed for director review. No new generated art or invented mechanic values are required. Catalog breadth is deliberately limited to both complete fixture bloodlines and their reference support selections; expansion is a separate refresh/template review.
- Captured Gate link ownership conflicts with older poster labels; source records win. Equipped lists do not establish exact AI rotation timing, so no cadence is invented.
- Cross-device simultaneous first imports cannot be fully transactionally deduplicated around the pinned parameterless `guide.create`; a rejected duplicate slug can leave a placeholder. One assigned operator, deterministic slug lookup, browser locks, durable journals and explicit empty-draft reconciliation limit this. No automatic destructive cleanup or publication path exists.
- Submitted revisions are new snapshots. Catalog upgrades require retaining the old version for old-draft editing or explicitly migrating a backup; no silent migration. Import receipt recording is an authenticated staff attestation, not a TNR-signed callback.
- Existing parity `checks: null` failure is unrelated baseline debt. No independent review has yet occurred.

## Live activity statement

Six credential-free public TNR GETs were used only for the separately authorized static refresh: one Aerathiel `bloodline.get`, one Death's March `jutsu.get`, then `bloodline.get`/`jutsu.getAll` for each fixture bloodline. Official image CDN reads/retries acquired 41 cached assets. Existing reference files/captures and pinned GitHub source were read. Public authoring, fixtures, server tests and all native mutation harnesses make zero live TNR requests.

No live game write, publication, deployment, staff sign-in, game cookie/token/password or session material was used. Test signing keys are locally generated and disposable. GitHub repository persistence uses the existing connector; no PAT or raw token was requested or handled.
