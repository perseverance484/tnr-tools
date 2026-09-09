# Builder app production-readiness re-review — 5ffb735

## Target

- Repository: `perseverance484/tnr-tools`
- Implementation branch: `claude/builder-app-production-readiness-kelsib`
- Exact reviewed remote head: `5ffb73511be091ebc221c405e4dd70334d918aa0`
- Prior rejected head: `c388ea65e0783f4e8ad0670949f23dfc420b205f`
- Shared baseline observed during review: `main` @ `4a506dff0af7dd499c8b580af4f0c14fdfc48c1c`
- Governing readiness brief: `state/prompt_builder_app_readiness.md` @ `b8f9dbf533dd51c119eb8d530e9c2fe3506e43b4`
- Prior review: `docs/reviews/BUILDER_APP_READINESS_C388EA6_REVIEW.md` @ `06392fbbe1d2893a98ff16ee4f430e9ee0218297`
- Review mode: narrow re-check of the two accepted blockers plus regression/source-drift checks.

The implementation branch was re-read immediately before review and pointed exactly at `5ffb735...`. The correction delta from `c388ea6` is four commits and is limited to `harvest.py`, its Forge regression tests, `pin_relevance.mjs`, notes/handoff, and the expected skillpack zip rebuilds. `forge_bundle.js` did not change in this correction round.

## Verdict

**APPROVED FOR INTEGRATION.**

Both blockers from the `c388ea6` review are closed on the exact frozen SHA. I found no new production-safety blocker in the correction surface.

This is deliberately not the same as declaring Forge fully production-ready today. The readiness brief's release/browser gates still require:

1. install the staged release-pin workflow before the `main` integration that changes `forge_bundle.js`;
2. integrate the reviewed implementation and verify the resulting loader pin is immutable;
3. dauntless performs the later browser smoke and alone decides when/what first live manifest to run.

No live-game request, game write, session cookie, or live credential was used in this review.

## Prior finding 1 — CLOSED — Forge skipped/pending bundles can no longer verify green

### Invariant

A Forge result bundle may return repository verification exit 0 only when Forge itself reports a verified `success` and no write entry remains skipped, pending, failed, drifted, or unread.

### Inspected correction

`skills/building-tnr-content/scripts/harvest.py::cmd_verify()` now identifies Forge bundles by `cfg == "forge"` or the presence of `forgeState` and applies fail-closed semantics only to Forge:

- `state: skipped` and `state: pending` are emitted as `UNVERIFIED` and increment the failure count;
- Forge's top-level `outcome` must equal `success`, otherwise verification fails even if per-entry arithmetic would otherwise pass;
- legacy builder bundles retain their previous non-Forge handling.

That preserves the correct authority direction: repository verification may add a failure, but cannot override Forge's own `unverified`/`open`/`failed` verdict into success.

### Regression evidence

`forge/test/harvest.test.mjs` now exercises the real paths rather than a hand-edited fixture:

- a create is driven into an ambiguous reconciliation result, becomes `ORPHANED`, is resolved through the real `Runner.skip()`, exported through the real Forge export path, and the real `harvest.py verify` must print `UNVERIFIED` and exit 1 while the fake-game row remains present;
- a job exported while its create remains `SENT`/in flight must verify non-zero;
- a legacy-shaped bundle with an unattempted pending row retains the old exit-0 skip semantics;
- the same shape marked Forge with no top-level outcome fails closed;
- the existing clean Forge control still exits 0.

The false-green path reported in the prior review no longer survives the current control flow.

## Prior finding 2 — CLOSED — current-source relevance is now proven against actual game `main`

At review time the public game repository still resolves to:

`studie-tech/TheNinjaRPG/main` @ `62af1b3405b10183b31f838c9a5f131d790460f1`

which matches the exact head used by Fable's correction proof.

The Forge pin remains:

`studie-tech/TheNinjaRPG@345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9`.

Independent repository comparison from the pin to current game `main` confirms the reported shape:

- none of Forge's content routers, validator files, `trpc.ts`, upload route, `proxy.ts`, `next.config.mjs`, `global-not-found.tsx`, or `app/package.json` changed;
- `app/src/server/api/root.ts` only adds registration for `push` and `purchases` routers;
- `app/drizzle/schema.ts` is additive in this range (338 additions, 0 deletions);
- `app/drizzle/constants.ts` is additive in this range (102 additions, 0 deletions);
- the adjacent app tRPC client change only adds `push.unregisterDevice` to the public-mutation allowlist and does not alter the server adapter/auth contract Forge talks to.

`forge/tools/pin_relevance.mjs` now also declares `app/drizzle/constants.ts` as a watched surface, so future value-list changes cannot sit outside the relevance report unnoticed.

Fable reports that `derive_fields.mjs` and `derive_nested.mjs` produce byte-identical contracts from both the Forge pin and current game head. Given the unchanged content validators and the inspected additive upstream differences, retaining `345d18ac...` is supported; no repin is required for this release.

If game `main` advances before integration, rerun the relevance gate before merging. A fresh upstream head is evidence to evaluate, not an automatic reason to move the pin.

## Other readiness claims

The prior full review already inspected and accepted the substantive Forge hardening outside these two blockers: mutation ambiguity handling, honest `INCOMPLETE` verification semantics, pool-code safety, `dedupNames`, nested-key fail-closed validation, release-pin design, and UI result semantics. The correction round does not modify those shipped Forge source paths or `forge_bundle.js`, so no wider architectural re-audit was triggered.

The two committed-manifest incompatibilities documented by Fable remain content/operator decisions, not reasons to weaken Forge validation. Forge may continue refusing those old manifests until dauntless chooses to edit/retire them.

## Tests / generated evidence

Fable's correction handoff reports:

- `npm test`: 202/202 pass;
- deterministic `forge_bundle.js` rebuild, byte-identical to checked-in output;
- adapter fixtures byte-identical;
- `fields.json` and `nested.json` byte-identical from the governing pin and also from current game `main`;
- skipped-orphan and pending-write Forge harvest regressions exit 1;
- clean Forge harvest control exits 0;
- all 12 existing inbox bundles preserve their prior verdicts;
- doctrine/render/pack/law gates unchanged and green except the repository's pre-existing TNR-03 `selfcheck.py` failure, reported byte-identical to `main`;
- no live-game host/network path added to tests.

This review environment could not independently run the npm/local-checkout suite because direct GitHub cloning is unavailable (DNS/network blocked). No GitHub commit status checks are attached to `5ffb735...`. Approval therefore rests on exact-source/test inspection, the committed end-to-end regressions, independent upstream diff inspection, and the reported command results; it does not claim an independently executed build.

## Required integration sequence

1. **Before merging Forge**, dauntless installs `state/staged_workflows/release_pin.yml` as `.github/workflows/release_pin.yml` through the approved GitHub UI path. Do not install it after the Forge bundle merge and assume it retroactively pinned that bundle.
2. Re-verify live TNR Tools `main` and public game `main` immediately before integration. If game `main` moved, rerun the relevance proof.
3. Integrate the reviewed implementation through the normal reviewable `main` path without rewriting/discarding operational main history.
4. Verify the release workflow ran for the `forge_bundle.js` change and that `forge_loader_user.js` now references an immutable commit SHA with the expected version/marker state.
5. Only then proceed to the user-owned browser smoke. Keep it no-write where possible. No production mutation is authorized by this review.

## Browser/live items still unverified by design

- Firefox Android + ViolentMonkey `document-start` timing on `/forge`;
- `window.stop()` on the real 404/global-not-found response;
- `navigator.storage.persist()` behaviour;
- Clerk refresh/expiry during a long job;
- real cookie/auth continuity;
- real server clock-skew interaction with rate limiting.

These remain acceptance gate 11 / user-owned smoke territory, not evidence against integration readiness.

## Next permitted step

The exact SHA `5ffb73511be091ebc221c405e4dd70334d918aa0` is approved for integration. The next action is the pre-integration release-pin workflow installation, followed by re-verification of `main`/game-source heads and the reviewed merge path.