# Forge full-capture persistence — independent review

**Review status:** CHANGES REQUIRED — integration blocked  
**Date:** 2026-09-10  
**Repository:** `perseverance484/tnr-tools`  
**Implementation branch:** `claude/prompt-forge-full-capture-8sxvli`  
**Intended base / frozen brief:** `b99747f4bebaf2b2b23a7511310efbe1b227ec75`  
**Reviewed head:** `090b6dc78c8eecec3ca4d40e7bdea13cfcc3a7a2`  
**Live `main` during review:** `bceb3a880b01048be51c4c9a462d9dcfb8f92fcf`  
**Reviewer:** ChatGPT — Engineering Auditor  
**Safety envelope:** repository/source/test evidence only; zero live-game requests, writes, or credentials used by this review

## Verdict

Do not integrate `090b6dc78c8eecec3ca4d40e7bdea13cfcc3a7a2` yet.

The implementation is strong on the normal after-only point-read case and satisfies most of the frozen brief, but the full-capture storage identity is mutable. A full capture does not durably identify the body produced by *that specific read*; it points at the ordinary cache slot for `path + id`. A later read or same-entity write can overwrite or invalidate that slot before export.

This breaks the core full-capture invariant and, in the before/after case, can produce silently false repository evidence while reporting `persistOk: true`.

## FFC-1 — HIGH — full captures alias the mutable canonical cache instead of an immutable per-read snapshot

**Classification:** Confirmed defect / merge blocker  
**Severity:** High for auditability and evidence correctness; it does not itself create a live-game mutation.

### Governing invariant

The frozen brief requires that `persist: "full"` durably include **the exact decoded successful response body of the read Forge already performed**, with no second read, for capture entries under both `capture.before[]` and `capture.after[]`. The localStorage journal must remain compact, but the requested full body must remain materializable from IndexedDB.

A full capture therefore needs an immutable identity for the specific read that produced it. `path + id` is only the identity of a mutable cache slot, not of a capture event.

### Implementation evidence

At the reviewed head:

1. `CaptureCache` keys ordinary read cache records as `captureKey(path, id)`, i.e. `${path}:${id}`. `put()` writes with IndexedDB `put`, so another successful read of the same path/id replaces the record at that key.
2. The same cache is deliberately invalidated by writes. `invalidateRecord(entity, id)` deletes the record's point-read cache entry; `invalidateEntity(entity)` removes all captures for that entity.
3. `Runner._captures()` performs the read and, for full mode, `_persistFull()` journals only the canonical `cacheKey(path, id)` plus `persistOk`, `persistError`, and size. It does not preserve a snapshot key unique to the capture occurrence.
4. `App._materialize()` later retrieves `cache.getByKey(capture.cacheKey)` and exports whatever body is currently stored there.
5. Asset writes use `cacheEntity: "asset"`, so a full `gameAsset.get` before an asset update is directly in the invalidation path.

### Deterministic reproduction

A manifest can legally ask for the same record before and after a write:

```text
capture.before: gameAsset.get A, persist full
item: update asset A
capture.after: gameAsset.get A, persist full
```

Execution at the reviewed head is:

1. BEFORE read stores the old body at `gameAsset.get:A`; the before capture journals `cacheKey = gameAsset.get:A`.
2. The asset update invalidates that cache record.
3. AFTER read stores the new body at the same `gameAsset.get:A`; the after capture journals the same cache key.
4. Export materializes both entries by reading `gameAsset.get:A`.
5. Both capture entries can therefore export the **new** body and report `persistOk: true`.

The bundle then claims to contain two exact full captures, but the first body is not the body of the first read. A reviewer can be shown a false before-state with a green persistence verdict.

A simpler before-only same-entity-write case loses the before body entirely and degrades to non-success at export. That is fail-closed, but still does not satisfy the brief's durable-before-capture contract.

Repeated full reads of the same path/id without a write have the same identity problem: the later `put()` replaces the earlier body, so both full captures materialize from the same newest cache slot.

### Why current tests do not close it

The new full-capture tests correctly cover a single after-only asset read, distinct-ID resume, missing-cache failure, oversize failure, summary compatibility, the allowlist, and compact-journal behavior.

The writing-job persistence test captures an asset but writes a **jutsu**, so the asset cache is not invalidated. The incremental resume test uses two distinct asset IDs. There is no test for repeated `path + id`, or for full before/after capture of the same record around a same-entity write.

### Practical consequence

The feature exists specifically to turn a fresh capture into durable repository evidence. In a before/after audit, silently exporting the after body as both before and after is worse than omitting the body: it can make an incorrect conclusion look behaviour-proven.

The immediate One Perfect Crop asset probe is after-only and uses five distinct IDs, so this defect does **not** make that particular manifest's intended read pattern ambiguous. It does, however, make the general Forge 0.3.0 contract unsafe to release as implemented.

### Required correction

Preserve an **immutable IndexedDB snapshot per full-capture occurrence**. The snapshot identity must not be the ordinary mutable `path:id` cache key.

A suitable design is a per-capture key incorporating stable job/capture identity, for example `jobId + phase + ordinal`, whose record stores the exact decoded body, read timestamp, and size. The localStorage journal should retain only this small snapshot key and persistence verdict. Ordinary entity cache invalidation must not delete or overwrite these durable capture snapshots. Export then materializes the body from the immutable snapshot key and performs no network read.

A separate IndexedDB object store is conceptually clean; a dedicated snapshot namespace in the existing database can also work if invalidation and listing semantics remain unambiguous. The implementation choice remains Fable's.

A body hash attached to the canonical cache record is not sufficient by itself. It could detect aliasing and fail closed, but it would still lose a legal `capture.before persist:"full"` body across same-entity writes, so it would not fulfill the frozen contract.

### Required regression tests

Add at least these cases:

1. `capture.before full A -> update A -> capture.after full A` exports the old body first and new body second, both with `persistOk: true`, with exactly one read per capture and no export-time read.
2. Two full captures of the same path/id with different fake responses preserve their respective bodies rather than both exporting the newest body.
3. A before-only full capture survives later same-entity cache invalidation/write and remains exportable.
4. Snapshot bodies never enter the localStorage journal or the embedded compact journal.
5. Immutable full snapshots survive the intended browser/app restart path when the job/export is resumed from persisted state.
6. Existing partial-capture resume still does not reissue already completed reads.
7. Missing/oversized immutable snapshot remains explicit non-success without truncation or re-read.

## Verified strengths at the reviewed SHA

The following parts held under review and should be preserved in the correction:

- `persist` is explicit, with omitted/`summary` maintaining compact behavior and invalid modes rejected before a job opens.
- Full persistence is fail-closed to the approved content-record point-read allowlist and the canonical `gameAsset.get` spelling.
- Manifest hashing includes the raw persistence request while preserving the legacy no-`persist` hash behavior.
- Full bodies are not written to the synchronous localStorage journal.
- The happy-path exporter does not make a second network read.
- Missing or oversized bodies do not get truncated or mislabeled as full success.
- Capture-only and mixed-job outcomes account for persistence failure rather than relying only on read success.
- The operator UI visibly distinguishes full captures before execution and distinguishes read success from body-persistence success afterward.
- `push/02_one_perfect_crop_asset_probe.json` is correctly converted to five distinct, after-only `gameAsset.get` point reads with `persist: "full"`, `items: []`, and explicit zero-mutation wording. It remains unrun in the handoff.
- Release staging keeps the existing immutable loader `@require` pin and adds `@x-release-pending 0.3.0` rather than prematurely promoting the loader.

## Verification evidence

The reviewed branch head was verified remotely as `090b6dc78c8eecec3ca4d40e7bdea13cfcc3a7a2`, directly parented by the frozen brief commit `b99747f4bebaf2b2b23a7511310efbe1b227ec75`.

GitHub Actions on the exact reviewed head completed successfully for both `verify` and `gate`. The Forge workflow's verify job runs `npm ci`, production dependency audit, `npm test`, fixture regeneration with a clean diff requirement, and a fresh bundle build with `git diff --exit-code` against `forge_bundle.js`.

This review independently inspected the task brief, capture cache/storage code, manifest normalization/hash behavior, runner capture path, write invalidation path, export/materialization path, journal outcome logic, UI presentation, asset recipe, full-capture tests, probe manifest, release loader, and the checked workflow.

No live/browser smoke was performed because the task brief explicitly authorizes zero live requests during implementation/review. Browser-only behavior therefore remains unverified until a reviewed version is integrated and the user elects to run the production proof.

## Next step

Fable should correct FFC-1 on its own implementation branch and return a new exact frozen SHA with the new regression tests and regenerated bundle. If the correction is limited to immutable full-snapshot storage/materialization, corresponding tests/docs, and generated bundle output without wider architectural changes, a narrow re-review is appropriate.
