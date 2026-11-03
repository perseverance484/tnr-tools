# Guide Studio: continuation to private testing and launch

Recorded by Astra on 2026-09-13. This is a continuation record, not a replacement implementation contract or a declaration that deployment has passed.

## Completed work is in GitHub

- Repository: `perseverance484/tnr-tools`.
- Implementation owner: Astra, explicitly assigned by the project director for Guide Studio.
- [PR #13](https://github.com/perseverance484/tnr-tools/pull/13) is merged. GitHub independently rechecked for this record: `merged: true`.
- Verified current `main` and merge commit: `24a88d377ba19669ad9d267f4f1512944226bb37`.
- Reviewed implementation: `8ef59a19e129657184f703044cd8fe1e7555c8f1`, branch `astra/guide-studio-implementation`.
- Original implementation base: `6848a7805d912378f7f8eb27f52c9625dd10ac54`.
- Reviewed application tree, also the merge tree: `debd9083daee50d1da80d30c247f03483f7b4133`.
- Design handoff: `chatgpt/guide-studio-spec` at `87fb673938d915c0732351d2efb208d05ef38c7c`.
- Pinned game source: `studie-tech/TheNinjaRPG@36c5873b7b6ee5fd3af717008d7c51b0f185b756`.

The director supplied the recommendation to integrate `8ef59a19...` and treat the deployment checklist as a separate live-operation gate. Historical review documents describe their own earlier freeze points; their "pending review" language does not undo PR #13's integration. Preserve those historical records.

This documentation change uses `astra/guide-studio-staging-handoff`, based exactly on the verified merge above. It changes no application code. New implementation should start from freshly verified current `main` on a dedicated Astra-owned branch. Do not edit the frozen implementation or ChatGPT design branch.

## Read to resume

Read `state/active-context.md`, `state/status.json`, `docs/00_INDEX.md`, `docs/RULINGS.md`, `CHATGPT.md`, `CLAUDE.md`, `docs/DEVELOPMENT_WORKFLOW.md`, `docs/agents/README.md`, and `docs/workflows/IMPLEMENTATION_HANDOFF.md` first.

The implementation contract remains these two files at the exact design SHA above:

- `docs/design/GUIDE_STUDIO_PRODUCT_SPEC.md`
- `state/prompt_guide_studio.md`

Then inspect `guide-studio/README.md`, [DEPLOYMENT.md](DEPLOYMENT.md), [CORRECTION_REVIEW.md](CORRECTION_REVIEW.md), [IMPLEMENTATION_REVIEW.md](IMPLEMENTATION_REVIEW.md), [CATALOG_PROVENANCE.md](CATALOG_PROVENANCE.md), [the recorded independent review](review/independent-review-ceb7867.md), and the implementation itself.

## Verified baseline and limits

The existing verification log is [review/correction-verification.log](review/correction-verification.log). It records `npm ci --ignore-scripts`, `npm run gate` (38 tests passing, compatibility/catalog/fixture checks, builds, public bundle boundaries, gzip budget, and isolated production-install smoke), fixture generation, and formatting. The latest session also rebuilt the unchanged reviewed application with `npm run build`: exit 0; importer disabled because no operator trust configuration was supplied. These are local results, not evidence of a deployed Cloudflare environment. The documentation-only continuation does not rerun the application gate.

The four confirmed review findings were corrected: exact production `entities: 8.0.0`; official art removed from bundled catalog with verified same-origin loading and cacheable hashed assets; production artifact validation uses the pinned generated validator; header staff link has a minimum 44 by 44 pixel target. Public JS measured 229,505 gzip bytes against a 250,000-byte gate.

Catalog: `catalog-1caefb53206168966f10`; templates v1; normalizer v1. The canonical catalog, 35 jutsu, four summons, 41 official images, fixture inputs, and template versions are unchanged. Canonical/browser projections have a reproducibility check. See the provenance record for source captures and image hashes.

| Fixture | Assets | Package hash |
| --- | --- | --- |
| Aerathiel | 21 | `fc893d47ce2b60c106579b75f66240ab8cb6eacc9c82717d511a44bf9c1491bc` |
| Night Parade | 29 | `32c72b6f78b72ce6a94b2884c9594266e67e1fa38d527d697f5caba356e7a554` |

Use the fixture producer and original verification log as evidence; do not manually revise generated contracts, catalogs, or fixture output. The unrelated repository-wide parity failure on a baseline capture with `checks: null` remains disclosed debt.

## Current account and deployment state

The user has a Cloudflare account and wants a test link usable on their phone. A ChatGPT Cloudflare plugin installation prompt was accepted, but this session exposed no Cloudflare account tools. Installation is not verified account access. No Cloudflare account ID, domain, project, bindings, Access policy, Turnstile configuration, or deployment has been verified or created by this session.

A new chat is optional for continuing the engineering work: the repository contains the implementation and evidence. If a fresh session loads the plugin, inspect its actual capabilities and use a read-only account check before claiming account access. Do not assume that a plugin containing Cloudflare guidance can perform authenticated deployments. If no suitable account tools are available, continue with the user through Cloudflare's dashboard and GitHub integration. Do not request pasted passwords, session cookies, or API tokens.

Current deployment inputs are intentionally incomplete. `wrangler.jsonc` has placeholder bindings/origin and does not declare the required routes. `dist/` contains the static application; `dist-worker/worker.js` contains the separate API. Uploading `dist/` alone does not establish submission, approval, or import readiness. `npm run dev` is a localhost harness with mock staff and Turnstile, ephemeral approval keys, and in-memory storage: never expose it or remove its localhost guard.

## Finish in this order

1. **Prepare and deploy the private test environment.** Verify available account/project resources, choose the test hostname, and complete the configuration in DEPLOYMENT.md: same-origin API/assets routing, private R2, D1/schema, staff Access, Turnstile, and approval signing/public trust. Codify the concrete hosting configuration on the new Astra branch. Resolve routing against the chosen hostname and current Cloudflare documentation; do not assume a separate Worker route can attach to any Pages hostname. Preserve the security headers and static caching. Verify who can access every reachable test hostname before describing the link as private.

2. **Let the director test the player experience on a phone.** Exercise both Aerathiel and Night Parade: select bloodline, inspect the always-complete foundation, choose/reorder jutsu, edit HOW I USE IT notes, write chapters, preview, reload/recover, and upload/download optional content. Check keyboard/focus, scrolling, touch targets, artwork loading, and actual storage/file behavior. An early authoring-only preview can support this step, but identify its missing server capabilities explicitly.

3. **Pass the deployed content-admin workflow.** Use the real Cloudflare staging service to submit, review the exact frozen render, request revisions, approve, and download the immutable package. Verify Access rejection, Turnstile, D1 revision races, R2 asset availability, signatures/hashes, CSP/cache behavior, and workerd CPU at maximum supported submission size. Confirm the required JSON/HTML/manifest/provenance files and exact approved byte identity. Keep game mutations in the local mock/native-transport harness.

4. **Finish the native importer and launch decisions.** Prepare the configured TNR-side/Forge importer, confirm the supported staff operating environment, and return the reviewable installation/import procedure. Approval freezes the artifact; import uses native `guide.create`/`guide.update`, reports guide ID and mutation results, and retains `category: "bloodlines"`, `published: false`, and the selected `relatedBloodlineId`. Any live game action belongs to the user and requires their separate explicit action. Publication is a separate staff decision. Do not declare the product complete at submission or static preview.

For deployment work, reproduce the existing gate in the new environment and add only checks needed for the changed configuration/runtime. Preserve the complete locked kit regardless of loadout, the two acceptance fixtures, and Black Thorn Rose's self DAMAGE TAKEN reduction plus enemy HEALING REDUCTION with no offensive DAMAGE classification. Ordinary public authoring must continue making zero TNR API requests.

## Remaining disclosures

Physical-phone acceptance, live Cloudflare behavior, and a real authenticated TNR importer session remain unverified. The independent reviewer exercised headless mobile Chromium and a local service; those results do not establish physical-device or deployed-runtime behavior. Copy/art final acceptance belongs to the director.

Keep the known limits visible: staff-uploaded import receipts are attestations; the pinned parameterless create has an unresolved cross-device race; approved art depends on retention of the Studio origin/assets; catalog breadth is limited to the two proven templates; lower-severity review observations remain in the review record. Do not silently turn these into launch approval or broaden the implementation contract.

Continuation/deployment preparation: zero live TNR requests, zero game writes, zero game credentials/session material, zero Cloudflare deployments or publication. Historical initial catalog refresh provenance records six separately authorized credential-free public GETs and CDN image reads; do not misreport those as new activity or claim none ever occurred.

## Dashboard path if account tools are unavailable

Cloudflare supports connecting this GitHub repository from **Workers & Pages > Create application > Pages > Connect to Git**. For the existing static build, root directory is `guide-studio`, build command is `npm run build`, and output directory is `dist`. Complete the API/binding configuration above for the full workflow. Do not deploy the local harness.

Preview URLs are public by default. Cloudflare's preview Access switch does not automatically protect the production Pages hostname or custom domains. Configure the intended test policy and verify all reachable origins. Relevant official references checked for this record:

- [Git integration and build settings](https://developers.cloudflare.com/pages/get-started/git-integration/)
- [Preview deployments and Access](https://developers.cloudflare.com/pages/configuration/preview-deployments/)
- [Access on the production Pages hostname](https://developers.cloudflare.com/pages/platform/known-issues/#enable-access-on-your-pagesdev-domain)

## Compact restart prompt

```text
Resume TNR Guide Studio from perseverance484/tnr-tools. Astra remains the
explicitly assigned implementation owner. The reviewed implementation is
already merged through PR #13 at 24a88d377ba19669ad9d267f4f1512944226bb37;
the reviewed head is 8ef59a19e129657184f703044cd8fe1e7555c8f1.

Read guide-studio/docs/STAGING_HANDOFF.md on
astra/guide-studio-staging-handoff, then follow its read-first sources.
Verify current main and begin any code changes on a new Astra-owned branch.
Preserve the pinned design contract and game source. Continue toward a
private Cloudflare phone-test link, then deployed admin-flow verification.
Check actual Cloudflare account access; use dashboard/GitHub setup with the
user if the plugin has no authenticated tools. Do not restart implementation,
expose the local harness, perform live game writes, or equate import with
publication. Report the remaining live-operation gates accurately.
```
