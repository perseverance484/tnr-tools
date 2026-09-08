# BUILDER APP READINESS - Claude Code implementation brief

Drafted 2026-09-08 for dauntless. This is the implementation contract for bringing the existing
Forge / builder app to production-ready parity before TNR resumes new content work through it.

Work in `perseverance484/tnr-tools` on the existing Fable-owned `builder-app` branch. Do not
modify `chatgpt/*`. Do not merge to `main`. Return an exact frozen SHA for independent review.

## 0. Verified starting point

At brief creation:

- shared baseline: `main` @ `4a506dff0af7dd499c8b580af4f0c14fdfc48c1c`
- implementation branch: `builder-app` @ `4062268f433ffd4d1f9b7b1e2678367ecad9119c`
- prior independent review evidence: branch `chatgpt/review-builder-app-4062268`, review commit
  `08382eebcffcbcc464c93d348f83598fc219dd76`, file
  `docs/reviews/BUILDER_APP_4062268_REVIEW.md`
- original builder design: `docs/PLAN_2026-09-03_builder_app.md`
- original build brief: `state/prompt_builder_app_build.md`
- current implementation notes: `docs/BUILDER_APP_NOTES.md` on `builder-app`
- original game-source pin: `studie-tech/TheNinjaRPG@345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9`
- current sentinel upstream observed on `main`:
  `studie-tech/TheNinjaRPG@e02f815954c14eeb8c2fcbc4a589a506971e0ed7`

Verify every ref again before editing. If any moved, report the new exact values and assess whether
that changes this brief before implementing.

## 1. Safety envelope and ownership

1. **Zero live requests to theninja-rpg.com.** Do not open the game, call its APIs, run the game
   source, request/synthesise session material, or perform any production experiment.
2. **Zero game writes.** dauntless remains the only live-game actor.
3. **One writer.** `builder-app` remains Fable-owned. Do not modify the ChatGPT review/brief branches.
4. **Do not merge to main.** Finish, push, freeze an exact SHA, and hand off for independent review.
5. **Do not use the old builder bundle as an engine-contract authority.** It is valid evidence for
   TNR project semantics/features that intentionally need parity, but source contracts come from the
   pinned/current game source and generated/verified contracts under repository precedence.
6. **Do not refactor unrelated architecture.** This is a production-readiness hardening pass.
7. Preserve the existing write-ahead journal, no-retry-on-ambiguous-mutation invariant, per-path
   budget safety, single composition root, and zero-network test design.

Read `CLAUDE.md`, `docs/DEVELOPMENT_WORKFLOW.md`, `docs/00_INDEX.md`, current state, relevant
rulings, this brief, the prior review, implementation/tests/fixtures, and the exact source pins before
changing code.

## 2. Definition of production-ready for this pass

Forge is not ready merely because the test suite is green. For this pass, production-ready means:

- an ambiguous mutation response can never become a definite negative verdict;
- deterministic manifest mistakes are rejected before an irreversible create/update where knowable;
- safety semantics relied on by current Lane B manifests are not silently lost in the Forge rewrite;
- a job cannot present a green/complete state when mutation read-back is unread or drifted;
- source-derived validation used for live writes is demonstrated relevant to the current upstream
  contract or refreshed deliberately;
- the installed userscript can be pinned reproducibly to an immutable reviewed bundle;
- Forge result bundles are proven ingestible by the repository harvest path without contacting the game;
- all checked-in generated/bundled artifacts reproduce from their producers;
- remaining browser/live-only uncertainties are explicit and safe to test later by dauntless without
  pretending they were verified in code review.

## 3. P0 - close the surviving independent-review blocker

The review at `4062268` left F4 open.

### Invariant

If any per-index mutation response element is not the exact audited tRPC error/result shape, the
request is ambiguous. The item must stay `SENT` and route through pause/reconciliation. It must never
be converted into a normal server failure merely because `el.error` is truthy.

### Current defect

`forge/src/transport/envelope.mjs::decodeElement()` accepts any truthy `el.error`, while
`isTrpcErrorBody()` already defines the stricter adapter error shape. For example
`[{"error":{}}]` becomes `UNKNOWN` instead of a fatal mutation decode ambiguity.

### Required correction

Validate a per-element error against the same audited adapter shape before decoding it. A malformed
mutation element must cause `decodeResponse(..., {mutation:true})` to throw a `TransportError` so the
runner preserves `SENT`. Query sibling salvage remains allowed.

At minimum pin regressions for:

- mutation `[{"error":{}}]` => transport ambiguity; runner remains `SENT` and pauses;
- mutation error missing numeric JSON-RPC `code` => ambiguity;
- mutation error missing `data.code` => ambiguity;
- malformed query element => `MALFORMED_ELEMENT`, with valid siblings retained;
- valid recorded adapter error fixtures still decode identically.

Rebuild the bundle and correct `docs/BUILDER_APP_NOTES.md`; it currently says all four prior HIGH
findings are closed when F4 is not.

## 4. P0 - honest terminal and verification semantics

The current runner can annotate a verify attempt as `unread` or `drift`, leave the item
`CONFIRMED` at phase `verify`, continue the loop, then mark the whole job `DONE`. The UI styles `DONE`
as success and auto-exports it. `readBack:false` is also converted into `VERIFIED`/`skipped` for a
mutation item.

That is not acceptable for production use. TNR doctrine requires read-back evidence; a push echo is
not verification.

### Required invariants

- A mutation item with `verify:unread` remains resumable at **read-only verify** and can never cause a
  mutation resend.
- A mutation item with `verify:drift` remains visibly unresolved and resumable/re-checkable without
  resending the mutation.
- A job with any unresolved verify item must not become a green terminal success.
- A job containing `FAILED` items may be execution-terminal, but the UI/summary must not present it as
  an all-good success.
- Parser compatibility with `readBack:false` may be retained, but a mutation manifest must not gain a
  false `VERIFIED`/green result merely by opting out. Prefer failing closed before start unless a
  repository-backed compatibility reason requires a distinct, explicitly unverified terminal result.
- Capture-only/no-mutation manifests may remain able to complete without mutation read-back.
- Auto-exporting a failure/incomplete bundle as evidence is fine; auto-export must not imply success.

Choose the smallest state/UI change that satisfies those invariants. Add tests covering resume after
`unread` and `drift` and proving no mutation is resent.

## 5. P0 - restore Lane B safety parity that Forge knowingly omitted

`docs/BUILDER_APP_NOTES.md` explicitly records that important current-builder protections are not
ported. Before Forge becomes the normal content path, close these gaps.

### 5a. Pool-code resolution / TNR-01 protection

Port the current v4.32 project semantics for pool-code resolution and its stuck/leftover-code guard.
The state records the TNR-01 lesson: an unresolved pool code can be sent as a literal and be stripped
server-side, leaving an empty kit while the row otherwise looks successful.

Requirements:

- resolve supported pool codes before any irreversible side effect, including image upload/create;
- if any pool code remains unresolved where a live id is required, fail closed locally;
- AI-kit manifests must never send a literal pool code as a jutsu/item id;
- add a regression reproducing the empty-kit failure mechanism and proving Forge rejects it pre-send;
- port the applicable current lint protections (the v4.32 L09-L22 set) that are safety/content-integrity
  checks, using current repo sources rather than remembered copies.

Do not infer server field shapes from the old bundle while porting these project semantics.

### 5b. `dedupNames`

`parseManifest()` preserves `dedupNames`, but Forge currently does not enforce it.

When `dedupNames:true`, perform the intended live-name collision check through the budgeted/cache-first
read layer before the relevant create. A collision must fail before placeholder creation. Pin tests for
collision, no collision, rate-limit pause, and restart/resume behaviour. Do not silently force the check
on manifests that did not request it unless current doctrine/canon already requires that.

## 6. P0 - nested unknown-key refusal

Top-level unknown keys are rejected, but the implementation notes acknowledge that misspelled keys
inside writable nested structures can pass and be silently stripped by the server. This defeats the
purpose of client-side pre-send validation.

Close this for the nested writable structures Forge supports in production, including as applicable:

- jutsu/item effect tag objects;
- quest content/objectives/nodes and their typed sub-objects;
- AI rule conditions/actions;
- any other nested manifest object the supported update validators parse non-strictly.

Requirements:

- derive/verify allowed nested keys from the pinned game validator/source contract, not hand-maintained
  guesses;
- reject an unknown nested key before any create/update for which it is knowable locally;
- preserve tagged-union/discriminator semantics and do not revive the known false `45g.tag_power_max`;
- add representative red tests per supported nested family plus valid controls;
- if one nested family cannot be safely derived in this pass, fail closed for manifests using that
  unsupported shape rather than silently sending it, and document the exact boundary.

## 7. P0 - current-source relevance gate

The original app is pinned to `345d18ac...`. Current `main` contains a sentinel report for upstream
`e02f8159...` and reports contract drift. Nothing may be adopted merely because it is newer.

Before final handoff:

1. Diff the original pin against the current sentinel upstream for **every game-source surface Forge
   relies on**: tRPC transport/adapter assumptions, content procedures, limiters, create semantics,
   validators used by `derive_fields.mjs`, AI schema/rules, host/takeover assumptions, and upload path.
2. Classify each upstream change as relevant or irrelevant to Forge with file/source evidence.
3. If no relevant contract changed, retain the old pin but record the proof in
   `docs/BUILDER_APP_NOTES.md` and the handoff.
4. If a relevant contract changed, deliberately move the Forge pin, regenerate the affected fixtures /
   field sets, rerun structural/provenance gates, update tests/notes/About text, and expect the final
   independent review to cover the widened contract surface.
5. Do not automatically adopt `docs/DRIFT.md` output. Follow `docs/00_INDEX.md` structural-diff rules.

The goal is not "latest at all costs"; it is proof that the client we are about to use still matches
production-relevant contracts.

## 8. P0 - immutable release pin

`docs/BUILDER_APP_NOTES.md` currently says the Forge loader `@require` points at a moving branch and
`release_pin.yml` only pins the legacy builder bundle. That is not an acceptable production install
for a reviewed mutation client.

Implement/stage the repository-side release-pin support so the Forge loader ultimately resolves an
immutable reviewed commit/bundle and its userscript version rises when the pin changes. Preserve the
legacy builder path until dauntless deliberately retires it.

If GitHub workflow permissions prevent Fable from installing the workflow change, commit the exact
staged workflow/file change and identify the one required dauntless GitHub action separately. Do not
work around permissions with credentials or a moving branch URL.

Add static tests/checks where practical so a Forge release cannot silently regress to a moving branch.

## 9. P0 - harvest/inbox compatibility

Forge auto-commits a result bundle to `harvests/inbox/`, but production readiness requires proof that
the repository ingestion path accepts that bundle.

Without any live request:

- generate a representative Forge result bundle from the test harness (success, failure, verify drift,
  verify unread, capture data, idmap/journal fields as applicable);
- run the current repo `harvest.py` ingestion/normalization path or the closest official local parser
  entry point against it;
- prove the normalized output preserves enough evidence to distinguish match/drift/unread/failure and
  does not misreport a green result;
- add a fixture/regression test if the current test architecture permits it cleanly;
- if compatibility requires changes outside `forge/`, keep them tightly scoped and flag them as a
  widened Lane A review surface.

Do not use a live inbox bundle as the only proof.

## 10. Required tests and build gates

Run and report exact commands/results, not only counts.

At minimum:

- `cd forge && npm test`
- `cd forge && npm run build`
- fresh bundle build compared with checked-in `forge_bundle.js` (must match the documented
  deterministic/reproducible expectation)
- `npm run fixtures` where the source pin/adapter fixture inputs changed; prove expected fixture diff
  or byte-identical regeneration when they did not
- `derive_fields.mjs` against the governing source pin; prove `fields.json` provenance/reproducibility
- the current-source relevance diff/gates from section 7
- local harvest compatibility check from section 9
- static grep/check that no live-game host is contacted by tests and no new network test was added
- any repository coherence/selfcheck gate required by files actually changed

Every newly fixed production-safety defect needs a regression test that fails against `4062268` or a
minimal equivalent fixture and passes on the new tree.

## 11. Browser/live-only items: do not fake them

Fable must not test these against production. Leave them explicitly unverified in the handoff:

- Firefox Android + ViolentMonkey `document-start` timing on `/forge`;
- `window.stop()` takeover on the real 404/global-not-found response;
- `navigator.storage.persist()` prompt behaviour;
- Clerk session refresh/expiry during a long real job;
- real production cookie/auth continuity;
- real rate-limit clock skew relative to the server.

The code must continue to fail/pause safely when those assumptions break.

After independent code review passes, dauntless will own the browser smoke test and any live job. The
first browser smoke should be no-write where possible; no production mutation is authorized by this
brief.

## 12. Explicitly out of scope unless required to satisfy a blocker above

Do not expand this pass for polish:

- native shell;
- eliminating browser tab eviction;
- capture `select` / `scope` trimming unless harvest compatibility actually requires it;
- cosmetic redesign;
- balance/reward/content changes;
- automatic deletion of anything;
- solving Clerk refresh by adding hidden game traffic;
- broad repository cleanup unrelated to Forge readiness.

`Pause during a run` having only jsdom coverage is not by itself a release blocker; browser behaviour
stays an explicit smoke-test item. Clock-skew residual risk may remain if the current conservative
budget proof still holds and the limitation is documented.

## 13. Notes and versioning

Update `docs/BUILDER_APP_NOTES.md` so its claims match reality. In particular:

- do not claim the four independent-review findings are all closed until F4 is actually closed;
- move completed readiness items out of "Not finished";
- retain genuinely unverified browser risks;
- record source-pin relevance/update evidence;
- record release-pin state;
- state any unsupported nested-validation boundary honestly.

Bump Forge package/bundle/loader versions according to the repository release mechanism when the
bundle changes. Do not disturb the legacy builder version/path unless required for coexistence.

## 14. Final handoff

This pass is wider than the narrow F4 correction, so expect a **full relevant readiness review**, not
an automatic narrow re-check.

Return a handoff following `docs/workflows/IMPLEMENTATION_HANDOFF.md` with:

- repository and branch;
- exact base / merge-base as relevant;
- exact frozen head SHA;
- live `main` SHA observed at handoff;
- changed files grouped by blocker above;
- exact test/build/fixture/derivation/harvest commands and results;
- source pins and current-upstream relevance evidence;
- generated bundle/fields/fixture provenance and reproducibility;
- whether the release-pin workflow change is fully installed or requires a dauntless GitHub action;
- known debt/deviations;
- all unverified browser/live/session risks;
- live requests/writes/credentials used: expected **none**;
- what explicitly remains out of scope / not begun.

Freeze that SHA until ChatGPT's independent review returns.

## 15. Acceptance gate before content work resumes through Forge

Do not describe Forge as production-ready until all of these are true:

1. F4 ambiguity is closed.
2. Unread/drift verification cannot become green terminal success or trigger mutation resend.
3. Pool-code/TNR-01 safety parity is present.
4. `dedupNames` is actually enforced when requested.
5. Supported nested unknown keys fail closed pre-send.
6. Current-source relevance is proven or the pin/artifacts are refreshed.
7. The release path is immutable/review-pinned, not branch-floating.
8. Forge result bundles are locally proven harvest-compatible.
9. Required tests/builds/generated-artifact gates are green.
10. ChatGPT independently approves the exact frozen SHA.
11. dauntless completes the later browser smoke and alone decides when/what first live manifest to run.
