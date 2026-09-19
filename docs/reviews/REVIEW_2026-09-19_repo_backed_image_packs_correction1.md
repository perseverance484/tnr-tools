# Independent narrow re-review — Forge repo-backed image packs correction 1

**Verdict: APPROVED FOR INTEGRATION.**

| Field | Value |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Correction target | `claude/repo-backed-image-packs-qke6mb@dcaa1465eb0eb58001ced42ac4b3f60f2a12d6db` |
| Previous reviewed target | `fbb4fb49ad49a9ef3063067fe3350fbce50fd265` |
| Previous review | `chatgpt/review-repo-backed-image-packs@2618043433e06519fbfad450cbd06a3314822c7a` |
| Intended base / merge-base | `28bba70d0e14f74a768193881b592b92326f2867` |
| Base relation | correction target is 2 commits ahead of base and 1 commit ahead of prior target |
| Live requests / writes during review | **none** |
| Godstorm image pack staged | no |
| Manifest 53 run | no |

## 1. Scope

This was a narrow correction review over the two accepted findings from the first independent review:

- **F1:** a different File with the same length could replace the verified File and still pass the Start gate;
- **F2:** an in-flight preparation for manifest A could mutate runner state after manifest B had become authoritative.

No pack-rule, manifest-identity, UI-contract, authoring-tool or content changes were in review scope except where the fixes necessarily touched the same runtime seams.

## 2. F1 — CLOSED

### Previous defect

The first implementation kept verified provenance metadata and the current File in separate maps, then checked only provenance + current file size. A same-size/same-MIME replacement could therefore pass Start and later be uploaded under the expected digest.

### Correction reviewed

`forge/src/core/imagepack.mjs` now commits the exact verified File onto the provenance record:

```js
runner.files.set(name, file);
runner.imgProvenance.set(name, { ...prov, file });
```

`packGateProblems()` requires:

```js
file === prov.file
```

rather than accepting size equality.

`forge/src/runner/runner.mjs` repeats the same identity requirement in both:

- `_imgPreflight()`;
- `_imgBytes()`.

The final upload path then re-hashes the File immediately before upload:

```js
const hex = toHex(await this.digest(await file.arrayBuffer()));
if (hex !== prov.sha256) throw ...
```

Only after that check can `uploader.upload(file)` run and only after a successful upload can the content-keyed upload ledger be written.

### Adversarial conclusion

The original same-size swap no longer has a route to upload:

1. replacing `runner.files[name]` leaves `prov.file` pointing at the originally verified immutable object;
2. Start rejects the replacement on object identity;
3. even if a caller bypassed Start and called the resolver directly, `_imgBytes()` rejects it;
4. even if provenance itself were incorrectly paired with another File object, the immediate pre-upload SHA-256 check rejects bytes not matching the expected digest;
5. no URL is recorded under `ASSET_UPLOADS_KEY` until after these checks and a successful upload.

The additional re-hash is conservative rather than harmful. It is not required for browser File immutability once identity is enforced, but it protects the actual send boundary and covers future/custom file-like hosts. At the current 512 KB upload ceiling, the cost is acceptable for this safety-sensitive path.

### Regression coverage

The correction adds a same-size, same-MIME, same-filename replacement test and separately exercises direct resolver/send-path refusal. That is the missing test from the first review.

**F1 status: CLOSED.**

## 3. F2 — CLOSED

### Previous defect

`prepareImagePack()` mutated `runner.files` and `runner.imgProvenance` before the caller checked whether the originating manifest selection was still current. A stale fetch could therefore finish after a selection change and write state into the newer manifest.

### Correction reviewed

Preparation is now side-effect free with respect to runner state:

```js
prepareImagePack(...) -> { entries, staged, ... }
```

The staged File/provenance pairs are only installed by the synchronous:

`commitImagePack()`.

The core now carries a monotonic `_packEpoch`.

Selecting/resuming a different authoritative pack calls `_scopePackProvenance()`, which increments that epoch.

`_prepareImages(s)` captures the current epoch, awaits repository/cache/digest work, then commits only when both remain current:

```js
if (this.state.selected !== s || this._packEpoch !== epoch) {
  return { ..., stale: true };
}
commitImagePack(...)
```

The resume path follows the same epoch discipline.

### Adversarial conclusion

The first review's race is now structurally closed:

1. manifest A begins an unresolved repository fetch;
2. manifest B becomes selected and increments the pack epoch;
3. A completes its fetch and returns staged Files, but has not mutated runner state;
4. A's currency check sees the selection/epoch mismatch and discards the staged data;
5. A cannot clear, populate or overwrite any File/provenance entry for B;
6. B's own preparation or manual fallback remains authoritative.

The synchronous commit has no await point inside the clear/install block, so a current preparation cannot be interleaved into a half-installed pack.

### Regression coverage

The correction includes:

- side-effect-free preparation test;
- deferred A-fetch / B-unbound manifest switch;
- overlapping A/B packs with the same logical name and different bytes;
- serialization/currency behavior.

These directly exercise the missing race.

**F2 status: CLOSED.**

## 4. Correction-scope discipline

The diff from `fbb4fb49...` to `dcaa1465...` is limited to:

- implementation handoff documentation;
- `core/core.mjs`;
- `core/imagepack.mjs`;
- `runner/runner.mjs`;
- focused image-pack tests;
- bundle budget;
- rebuilt `forge_bundle.js`;
- one composition-line change needed to wire the runner digest.

No pack schema, manifest identity, screen behavior or Godstorm content manifest was changed. The 14 screen fixtures are reported byte-identical.

That is appropriate for a narrow correction round.

## 5. Test / build evidence

Implementation reports, on the correction SHA:

```
npm test                                  416 pass / 0 fail
check_imports.mjs                         40 modules / 71 imports / 0 violations
check_boundaries.mjs                      40 modules / 0 violations
check_release_pin.mjs                     release pin ok
build.mjs                                 forge_bundle.js rebuilt
bundle reproducibility                    byte-identical fresh rebuild
check_bundle_budget.mjs                   451847/470000 raw; 88356/92000 gzip
derive_screens.mjs                        14 fixtures, byte-identical
```

The correction's five new focused tests are non-vacuous per the implementation's revert checks.

No GitHub Actions workflow run was associated directly with the correction SHA in the available workflow-run query. This review environment inspected the exact frozen source/test tree but did not independently execute the Node suite from a local clone.

## 6. Bundle-budget decision

The second budget raise is **not a blocker to this correction**.

The resulting bundle is ~96% of both new ceilings. The implementation correctly surfaced that this is now a recurring maintenance concern rather than hiding it.

I accept the raise for this feature because the added code sits directly on provenance, race prevention and the final upload trust boundary. Removing the pre-upload re-hash solely to recover a small amount of bundle space would trade safety clarity for budget cosmetics.

However, a separate Forge size pass should be planned before additional substantial Forge features. Two ratchet raises within one feature is a useful signal that accumulated comments/architecture may need consolidation.

## 7. Remaining non-blocking risks

Unchanged from the first review:

- no real Android Firefox / ViolentMonkey / WebCrypto / IndexedDB smoke;
- cache quota behavior is tested only through fake IndexedDB;
- the pack authoring contract is Node-owned and not duplicated in Python;
- repository path prefix policy remains intentionally open;
- Godstorm's actual eight binaries and production imagePack are not yet committed;
- bundle headroom is narrow.

None of these reopens F1 or F2.

## 8. Integration recommendation

**APPROVED FOR INTEGRATION.**

After merge and release promotion:

1. verify the operator is actually running Forge 0.5.0;
2. commit the eight approved Godstorm processed WebPs to a durable repository art path;
3. generate the pack from the commit with `make_image_pack.mjs`;
4. update manifest 53 with that generated pack;
5. run the mandatory manifest validator;
6. open manifest 53 and require Forge to show all eight repo-backed images verified;
7. only then perform the user-operated live repair run.

No live action is authorized by this review itself.
