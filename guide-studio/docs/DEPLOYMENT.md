# Cloudflare deployment and operator boundaries

No deployment or live import was performed. Use Pages for `dist/`, a Worker for same-origin `/api/*` and `/guide-assets/*`, private R2, Turnstile, Access, and D1. D1 provides atomic review transitions; an R2 object alone cannot enforce a compare-and-swap revision. `wrangler.jsonc` intentionally contains unconfigured bindings.

## Operator configuration

1. Provision private R2 and D1. Apply `server/schema.sql`. Bind `ARTIFACTS` and `DB`; keep the R2 public endpoint disabled.
2. Assign a permanent HTTPS Studio origin and Worker routes for `/api/*` and `/guide-assets/*` on the Pages domain. Set exact `PUBLIC_ORIGIN` without trailing slash. Approved content pins asset URLs; preserve that origin and the referenced assets across upgrades.
3. Configure an Access application covering `/staff` and `/api/staff/*`, restricted to content staff. Set `ACCESS_DOMAIN` and `ACCESS_AUDIENCE`. The Worker independently verifies signature, issuer, audience, expiry and subject ([Access JWT validation](https://developers.cloudflare.com/cloudflare-one/access-controls/applications/http-apps/authorization-cookie/validating-json/)).
4. Configure Turnstile for that hostname; store `TURNSTILE_SECRET` as a Worker secret. The service also checks hostname and action `guide-submit` ([Turnstile validation](https://developers.cloudflare.com/turnstile/get-started/server-side-validation/)). Configure edge abuse limits and monitor rejected requests.
5. Generate an Ed25519 approval key in the operator's secret manager. Store the private JWK as Worker secret `APPROVAL_PRIVATE_JWK`, with a key ID. Only its public JWK belongs in build variable `APPROVAL_PUBLIC_JWK`. Preserve old trusted public keys/importer builds for prior approvals during rotation. Compromised-key revocation requires explicit operator handling.
6. Build with `STUDIO_ORIGIN` equal to `PUBLIC_ORIGIN`, `TURNSTILE_SITE_KEY`, and the public JWK. `npm run build` generates `dist/` and `dist-worker/worker.js`. Private JWK field `d` is rejected; missing public trust leaves the importer disabled. No TNR cookies, tokens or passwords belong in any build variable or Worker binding.
7. Deploy Pages/Worker, preserve `_headers`, and configure the Pages SPA fallback for `/staff`. Budget Worker CPU for SVG generation and ZIP compression; measure maximum-size submissions/exports in staging before launch. No Cloudflare performance claim is established by the Node harness.
8. Review the built staff userscript and install it in the authorized staff browser on `https://www.theninja-rpg.com/guide*`, or mount `mountImporter` within a TNR/Forge-owned surface. The adapter uses the game page's existing same-origin session only on explicit import, without reading/storing session material. The game enforces content-staff permission. The public app/Worker cannot invoke this transport.

D1 uses `meta.changes` to identify the one successful revision update ([D1 results](https://developers.cloudflare.com/d1/worker-api/return-object/)). R2 stores frozen snapshots and assets ([R2 Worker API](https://developers.cloudflare.com/r2/api/workers/workers-api-reference/)). Assets are served only after their owner has won approval. Their unlisted immutable URLs then become readable by the native game; this does not publish an article.

## Static delivery cache

The build derives `/static/App-<hash>.js` and `.css` filenames from esbuild output metadata and writes those exact paths into HTML. Preserve `dist/_headers`: `/static/*` and `/assets/*` cache for one year with `immutable`; `/`, `/staff`, `/index.html`, `/config.js`, and the unversioned importer userscript revalidate with `no-cache`. The existing security-header rule applies to all of them. Pages must deploy the HTML and its referenced assets together. Actual edge headers/cache behavior remain a deployment check.

`npm run gate` rejects embedded official WebP data in public JS, any dependency on the server's full catalog, and total public JS above 250,000 bytes gzip. It also creates a clean temporary `npm ci --omit=dev --ignore-scripts --offline` install outside the checkout and loads the pinned contract/sanitizer/heading/artifact modules. Run the normal `npm ci` first to populate the local npm cache; the gate does not contact the package registry or game.

## Recovery and limitations

- Back up D1 and R2 together. Retain assets used by approved/imported guides. Define unapproved/orphan retention before launch; no destructive cleanup job is installed.
- A lost create response stops import. Inspect the newly created TNR placeholder and creation time, then attach its ID through the recovery panel. Only an untouched native placeholder is accepted; the next explicit import click resumes it. Create is never blindly retried.
- Lost update responses are read back. Exact success completes; otherwise retry uses the saved ID. Published or repurposed guides are refused. Moderation/sanitizer differences remain unverified.
- Web Locks serialize one browser's tabs; deterministic slug lookup recognizes completed imports across browsers. The pinned parameterless create cannot be made transactionally idempotent across staff devices. Simultaneous initial imports can leave an extra empty placeholder before duplicate-slug rejection. Assign one importer operator per submission and reconcile exceptions explicitly.
- Private receipts are bearer capabilities, not TNR credentials. Imported status is a staff-uploaded importer receipt: an operator attestation, not a game-signed callback.
- Catalog/template version mismatches preserve backups and fail explicitly. No silent balance migration is attempted.
- Publication, deployment, staff access membership and live operation remain operator decisions. The importer contains no publishing operation.

Before launch, complete real staging Access/Turnstile, D1/R2, CSP, image-loading, mobile scrolling/focus/upload/download/storage and native userscript checks listed in `IMPLEMENTATION_REVIEW.md`. Unit/DOM tests are not live-session evidence.
