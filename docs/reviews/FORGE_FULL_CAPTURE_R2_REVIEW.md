# Forge full-capture persistence — narrow re-review

**Review status:** APPROVED — integration recommended  
**Date:** 2026-09-10  
**Repository:** `perseverance484/tnr-tools`  
**Implementation branch:** `claude/prompt-forge-full-capture-8sxvli`  
**Frozen task brief / intended base:** `b99747f4bebaf2b2b23a7511310efbe1b227ec75`  
**Previous rejected head:** `090b6dc78c8eecec3ca4d40e7bdea13cfcc3a7a2`  
**Reviewed correction head:** `58323b0af0eeafc3204cfbd5c31cb068a3cf5a88`  
**Live `main` during re-review:** `bceb3a880b01048be51c4c9a462d9dcfb8f92fcf`  
**Reviewer:** ChatGPT — Engineering Auditor  
**Safety envelope:** repository/code/test evidence only; zero live-game requests or writes

## Verdict

FFC-1 is closed. The correction is narrow, directly addresses the rejected invariant, preserves the previously accepted full-capture behavior, and adds the regressions the first review required. Integration of the Fable implementation head `58323b0af0eeafc3204cfbd5c31cb068a3cf5a88` is recommended through the normal Lane A process.

No new merge-blocking findings survived the narrow re-review.

## FFC-1 closure

The rejected implementation used the mutable ordinary capture cache key `path:id` as the durable identity of a full capture. A later read of the same record or a same-entity write could therefore replace/delete the body before export and could make a before/after pair export the after body twice while reporting success.

The corrected implementation separates the two storage purposes:

- `captures` remains the mutable read cache keyed by `path:id`, and ordinary write invalidation still affects it;
- `capture_snapshots` is a new IndexedDB v2 store keyed by `jobId::phase::ordinal`, which identifies one requested full-capture occurrence rather than one mutable record cache slot;
- `Runner._persistFull()` writes `r.data` from the read that just completed directly into the snapshot store before returning `persistOk: true`;
- the localStorage journal carries only compact metadata including `snapshotKey`, size, and persistence verdict, never the body;
- `App._materialize()` exports from the immutable occurrence snapshot and never falls back to the mutable read cache or re-reads the game;
- normal `invalidateRecord`, `invalidateEntity`, and read-cache `clear` do not touch the snapshot store;
- missing snapshots still downgrade the result explicitly rather than fabricating/falling back to another body.

This closes the exact false-evidence path from the first review.

## Regression evidence

The correction adds direct tests that reproduce the rejected cases:

1. full `capture.before` of asset A -> update A -> full `capture.after` of A exports the old body first and the new body second, with distinct snapshot keys and no export-time read;
2. two full reads of the same `path + id` with different responses preserve their respective bodies;
3. a before-only full capture remains exportable after the job writes the same entity and invalidates the ordinary cache;
4. snapshot bodies reach neither localStorage nor the embedded journal;
5. snapshots survive app/tab restart and export from persisted state without another game read;
6. snapshots can be removed by job without affecting another job;
7. storage tests confirm ordinary invalidation leaves snapshots untouched, later reads do not overwrite earlier occurrence snapshots, and an existing IndexedDB v1 read cache upgrades additively to v2 without losing records.

The previously required full-mode tests also remain present for summary compatibility, invalid persistence modes, fail-closed procedure allowlisting, partial-pass resume, missing snapshot, oversize body, failed read, mixed-job outcome, UI labeling, and the One Perfect Crop probe.

## Exact-SHA CI / build evidence

GitHub Actions checked out exact head `58323b0af0eeafc3204cfbd5c31cb068a3cf5a88` and completed both repository checks successfully.

Forge `verify` evidence on that SHA:

- `npm ci` — success;
- `npm audit --omit=dev --audit-level=high` — success, 0 runtime vulnerabilities at the requested level;
- `npm test` — **241 passed, 0 failed**;
- `npm run fixtures` followed by `git diff --exit-code -- test/fixtures/envelope` — success;
- `npm run build` followed by `git diff --exit-code -- ../forge_bundle.js` — success; checked bundle reproduced from source.

The independent review environment could not clone the public repository directly because its sandbox had no DNS route to GitHub, so I did not claim a second local execution. I inspected the exact frozen source and the complete exact-SHA GitHub Actions log instead.

## Scope / safety / compatibility checks

- The correction is one commit on top of the rejected head, not a moving rewrite.
- The changed surface is limited to the capture snapshot/storage path, related UI/storage cleanup, regression tests, documentation, and regenerated `forge_bundle.js`.
- The approved fail-closed `persist: "full"` procedure allowlist is unchanged.
- Summary captures and legacy manifest hashing behavior remain unchanged from the first reviewed implementation.
- The One Perfect Crop probe remains five distinct `gameAsset.get` full point reads with `items: []`; it is still a read-only, zero-mutation consumer and has not been run by Fable/ChatGPT.
- Forge remains staged as 0.3.0; the feature branch does not prematurely replace the loader's immutable released `@require` pin.
- No live/browser production smoke was performed by this review. Browser/session behavior remains unverified until the reviewed release is integrated and the user elects to run the read-only production proof.

## Non-blocking note

The snapshot store is intentionally longer-lived than the mutable read cache and therefore can accumulate evidence until the operator deletes snapshots/jobs. The correction exposes snapshots separately and provides explicit deletion paths. That is an acceptable consequence of durable full capture and is not a correctness blocker for this task.

## Next permitted workflow step

Integrate the reviewed Fable implementation head `58323b0af0eeafc3204cfbd5c31cb068a3cf5a88` into `main` through the normal Lane A integration/release-pin process. After `main` and the Forge release pin are verified, the user may run `push/02_one_perfect_crop_asset_probe.json` as the first read-only production proof. Then inspect the committed full capture bodies before making One Perfect Crop asset reuse/reject decisions.
