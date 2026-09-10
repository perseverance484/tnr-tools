# Forge full-capture persistence task brief

**Status:** FROZEN implementation contract for Fable / Claude Code  
**Date:** 2026-09-10  
**Repository:** `perseverance484/tnr-tools`  
**Baseline main:** `bceb3a880b01048be51c4c9a462d9dcfb8f92fcf`  
**Lane:** A, code/tooling/infrastructure  
**Implementation owner:** Fable / Claude Code  
**Independent reviewer:** ChatGPT, Engineering Auditor  
**Integration target:** `main` after exact-SHA independent review

## Objective

Add an explicit, durable **full capture** mode to Forge while preserving the current compact capture mode as the default. Full mode exists so asset/content compatibility reviews can analyze the exact fresh record body Forge read instead of receiving only a row-count summary.

This task is repository/browser tooling only. It authorizes **zero live-game requests, zero live-game writes, and zero use of live credentials/session material during implementation or tests**. The user remains the only live-game actor.

## Problem being fixed

Forge's `CachedReader` already stores successful decoded read bodies in IndexedDB. However, `Runner._captures()` journals only compact metadata (`phase`, `proc`, `input`, `ok`, `rows`, `error`), and `App.exportJob()` exports those compact journal entries. The repository therefore loses the response body even when Forge successfully read and cached it.

For a fresh compatibility review, that prevents the repository evidence from proving fields such as an asset's current image URL, type, folder, hidden state, or other record data. A fresh existence/read success plus an older catalog is not equivalent to a fresh full record capture.

Do **not** solve this by putting arbitrary response bodies in the localStorage journal. The journal is deliberately small/synchronous write-ahead state; full capture bodies already belong in IndexedDB.

## Required manifest contract

Each entry under `capture.before[]` or `capture.after[]` may carry:

```json
{
  "proc": "gameAsset.get",
  "input": { "id": "..." },
  "persist": "full"
}
```

Rules:

- Omitted `persist` means the existing compact behavior.
- Explicit `"persist": "summary"` is equivalent to omission.
- `"persist": "full"` requests durable inclusion of the exact decoded successful response body in the exported results bundle.
- Any other `persist` value is a manifest error before a job opens.
- Existing manifests with no `persist` key must parse and run exactly as before.
- Manifest hashing must include the persistence request so changing summary/full cannot silently resume an old job under a different contract.

## Full-mode safety boundary

The results bundle is committed to the repository when GitHub sync is enabled. Full persistence therefore must be fail-closed rather than allowing arbitrary query bodies into a public repository.

For this first version, permit `persist: "full"` only for audited TNR **content-record point reads**:

- `gameAsset.get`
- `jutsu.get`
- `item.get`
- `bloodline.get`
- `quests.get`
- `profile.getAi`
- `ai.getAiProfile`

Do not allow full persistence for list/name-list procedures, mutation procedures, unknown procedures, arbitrary protected/user/account/session data, or future procedures merely because they are queries. Extending the allowlist later is a separate reviewed change.

Validate this restriction before a job opens. Reuse the existing audited procedure registry rather than creating a second contradictory source of procedure kind where practical.

## Runtime and storage behavior

1. The network/read behavior stays the same. Full mode does not add a second game read.
2. Successful reads continue to be cached in IndexedDB through the existing `CaptureCache`/`CachedReader` path.
3. The localStorage journal continues to store only compact capture metadata. It may add small fields such as `persist`, canonical path/id, and a cache lookup key/status, but it must not store the full response body.
4. For a successful `persist: "full"` capture, the exported bundle's corresponding capture entry includes:
   - all existing compact fields;
   - `persist: "full"`;
   - the exact decoded successful response as `data`.
5. Summary captures do not gain a `data` body.
6. A failed server read does not fabricate `data`.
7. Export must materialize a requested full body from IndexedDB, using the already-cached result. It must not perform another live read merely to export.
8. If a requested full body cannot be materialized from IndexedDB at export time, the bundle and UI must not claim complete success. Surface an explicit persistence failure such as `persistOk: false` / `persistError`, and make the capture-only job outcome non-successful.
9. Do not silently truncate full bodies. If a defensive serialized-size ceiling is added, exceeding it must be explicit non-success, not a shortened body presented as full. Keep the ceiling as a named/tested constant rather than an unexplained magic number.
10. Existing capture resumability must remain incremental: a pause after N captures must not re-run those N reads on resume simply because full persistence was requested.

## Results-bundle and UI requirements

- Existing compact `captures` consumers must remain compatible with summary captures.
- Full capture data should be inline on its matching exported capture entry unless a demonstrably safer/simple compatible structure is necessary; any deviation must be called out in the handoff.
- The embedded `journal` in the result bundle must remain compact and must not duplicate full bodies.
- The selected-manifest UI must make full persistence visible before execution, for example by distinguishing `5 captures` from `5 full captures` or an equivalent unambiguous presentation.
- The run/result UI for a capture-only job must distinguish read success from full-body persistence success when full mode is requested.
- Existing wording that a capture-only job sends zero mutations must remain true.

## One Perfect Crop first consumer

Update `push/02_one_perfect_crop_asset_probe.json` as the first real consumer, but **do not run it**.

Required changes:

- request `"persist": "full"` on all five point reads;
- use the canonical audited asset procedure `gameAsset.get` rather than the current `asset.get` spelling if the existing parser/reader does not intentionally normalize that alias;
- keep it capture-only with `items: []`;
- keep the note explicit that it is read-only and zero-mutation.

The branch may include this manifest edit so that, after reviewed integration and a correctly versioned Forge release, the user can run it as the first production proof. Fable must not contact the game to validate it.

## Tests and gates

Add focused tests covering at least:

1. legacy capture with no `persist` parses/runs/exports unchanged and contains no `data` body;
2. explicit `persist: "summary"` behaves like legacy summary;
3. `persist: "full"` on `gameAsset.get` exports the exact decoded fixture body;
4. full mode performs one read only, not an export-time re-read;
5. the localStorage journal contains no full body while IndexedDB contains it;
6. invalid `persist` values fail manifest parsing before a job opens;
7. full persistence on non-allowlisted/list/mutation/unknown procedures is refused before execution;
8. full capture resume after a partial pass does not re-read completed captures;
9. missing IndexedDB body at export produces explicit non-success rather than a green/full claim;
10. failed read has no fabricated `data`;
11. capture-only job outcome/UI accounts for requested full persistence, not just `capture.ok`;
12. results-bundle `journal` stays compact and does not duplicate `data`;
13. `push/02_one_perfect_crop_asset_probe.json` parses under the new contract and remains zero-item/read-only;
14. existing Forge capture/storage/runner/UI tests remain green.

Run the full Forge test suite and rebuild the checked-in bundle. Verify the rebuilt `forge_bundle.js` matches a fresh build. Follow the repository's Forge release/pin process rather than manually advancing immutable loader pins on the feature branch.

No game/browser live-session smoke is authorized by this brief. Any browser-only behavior not covered by fixtures/in-process tests must be reported as unverified in the handoff.

## Acceptance criteria

The implementation is acceptable when all of the following are true:

- old summary manifests are backward-compatible;
- full mode is explicit per capture and fail-closed;
- only the approved content-record point-read allowlist can be durably persisted in v1;
- full data is sourced from the single already-performed read and existing IndexedDB cache;
- no full body is stored in the localStorage journal;
- exported full entries contain the exact decoded body with no silent projection/truncation;
- missing/failed persistence cannot produce a successful full-capture claim;
- `push/02_one_perfect_crop_asset_probe.json` is ready but unrun;
- tests/gates/build are green;
- no live request, write, or credential/session use occurred.

## Out of scope

Do not add in this task:

- arbitrary full-query persistence;
- full `getAll` / name-list dumps;
- field-projection/query-language mode such as `persist: "fields"`;
- automatic redaction heuristics for unknown procedures;
- changes to game APIs or TNR source;
- live execution of the One Perfect Crop probe;
- asset reuse/reject decisions themselves;
- unrelated Forge refactors or UI redesign.

A future projected/selected-fields mode may be useful for large records, but it is not required here.

## Fable handoff requirements

Implement on a Fable-owned branch, normally `fable/forge-full-capture` or an equivalently specific name. At handoff, freeze the exact SHA and provide the fields required by `docs/workflows/IMPLEMENTATION_HANDOFF.md`, including:

- exact base and head SHAs;
- changed files;
- exact tests/gates/build commands and results;
- bundle regeneration/provenance;
- deviations from this brief;
- known debt or browser-only uncertainty;
- explicit statement that no live requests/writes/credentials were used;
- explicit statement that `push/02_one_perfect_crop_asset_probe.json` was not run.

ChatGPT will independently review the frozen SHA under the Engineering Auditor role before integration is recommended.
