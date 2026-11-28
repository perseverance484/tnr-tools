# Independent review — Forge repo-backed image packs

**Verdict: CORRECTIONS REQUIRED.**

| Field | Value |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Review target | `claude/repo-backed-image-packs-qke6mb@fbb4fb49ad49a9ef3063067fe3350fbce50fd265` |
| Intended base / merge-base | `28bba70d0e14f74a768193881b592b92326f2867` |
| Base relation | target is 1 commit ahead, 0 behind |
| Governing handoff | `docs/handoffs/FORGE_REPO_BACKED_IMAGE_PACKS.md` |
| Live requests / writes during review | **none** |
| Repair manifest run | no |

## 1. Summary

The design is strong in the places that caused the original Godstorm failure: immutable commit refs, SHA-256 binding, content-addressed cache, fail-closed parse rules, content-keyed upload reuse, and a separate repository fetch path.

Two safety findings survive adversarial review, both on the feature's central invariant: **the bytes that Start eventually uploads must still be the exact bytes that were verified for the selected manifest.**

The first is a direct Start-gate bypass for same-size replacement. The second is an asynchronous selection race that can repopulate stale File/provenance state after a new manifest has already scoped it away.

Both should be corrected before integration.

---

## 2. F1 — HIGH — Start does not bind provenance to the actual File object

### Location

- `forge/src/core/imagepack.mjs` → `prepareImagePack()` / `packGateProblems()`
- `forge/src/runner/runner.mjs` → `_imgPreflight()` / `_resolved()`
- `forge/test/imgpack.test.mjs` → test “packGateProblems refuses provenance that no longer matches the pack”

### Invariant

For a bound image, the File/Blob uploaded by `_resolved()` must be the exact verified object (or be re-verified) at the moment Start/run uses it.

### What the code currently proves

`prepareImagePack()` verifies SHA-256 and then writes two independent map entries:

```js
runner.files.set(want.name, file);
runner.imgProvenance.set(want.name, {
  sha256: want.sha256,
  path: want.path,
  ref: want.ref,
  bytes: want.bytes,
  at: now()
});
```

At Start, `packGateProblems()` checks:

- provenance exists;
- provenance digest/ref/path equal the manifest;
- current `file.size` equals `want.bytes`.

It does **not** verify the digest of the current File and does not prove that the File object currently in `runner.files` is the same immutable File created by the verified preparation.

The existing test only swaps in a **3-byte** File, so the size check catches it:

```js
core.runner.files.set(name, new File([new Uint8Array(3)], ...));
```

That does not exercise the dangerous case the feature exists to prevent: different bytes with the **same length**.

### Reproduction

After a successful preparation:

1. leave `runner.imgProvenance.get(name)` untouched;
2. replace `runner.files.get(name)` with a different File of the same expected byte length and compatible MIME;
3. `imagePicks()` passes (size/type match);
4. `packGateProblems()` passes (provenance metadata + size match);
5. `Runner._imgPreflight()` returns immediately because provenance exists and `files.has(name)`;
6. `Runner._resolved()` uploads the replacement File;
7. `recordAssetUpload()` records that upload URL under the **original expected SHA-256** from provenance.

So a same-size replacement can both upload the wrong image **and poison `tnr_forge_asset_uploads_v1`**, causing future jobs for the legitimate digest to reuse the wrong URL.

### Why this matters

The handoff explicitly claims:

> Start refuses “a File swapped under a still-valid record.”

The implementation only refuses a swapped File when its size changes.

The proposal's purpose is specifically to move from “size is not identity” to content identity. Allowing same-size replacement after verification reintroduces the size-only trust boundary at the final gate.

### Smallest robust correction

Do not re-hash on every Start if that is unnecessarily expensive. A browser File/Blob is immutable, so bind provenance to the exact verified object identity.

For example, provenance can store an unexported in-memory object reference or token:

```js
runner.imgProvenance.set(name, {
  ...,
  file
});
```

and `packGateProblems()` must require:

```js
prov.file === runner.files.get(name)
```

If keeping File references out of the provenance shape is preferred, maintain a private `verifiedFiles` WeakMap/Map or verification token keyed to the File object. Re-preparation/resume naturally creates a fresh verified binding.

Alternative: make the Start gate async and re-hash the current File before job open. That is stronger but probably unnecessary if exact File-object identity is held, because File objects are immutable.

### Required regression tests

- prepare a valid bound image;
- replace `runner.files[name]` with different bytes of **exactly the same length** and same MIME;
- Start must refuse and open no job;
- verify `ASSET_UPLOADS_KEY` remains untouched;
- verify `_resolved()` cannot upload the replacement;
- original verified File still starts successfully.

---

## 3. F2 — HIGH — stale asynchronous preparation can write into a newer manifest selection

### Location

- `forge/src/core/core.mjs` → `selectManifest()`, `_scopePackProvenance()`, `_queuePack()`, `_prepareImages()`
- `forge/src/core/imagepack.mjs` → `prepareImagePack()`

### Invariant

Once manifest B becomes the selected manifest, no in-flight preparation started for manifest A may populate `runner.files` or `runner.imgProvenance` in a way that survives into B.

### Current ordering

When a new manifest is selected:

```js
this.state.selected = B;
this._scopePackProvenance(B.pack);
...
if (B.pack) await this.prepareImages();
```

`_scopePackProvenance()` only clears provenance/files that **already exist at that moment**.

For a preparation of manifest A already in flight, `_prepareImages(A)` does correctly check:

```js
if (this.state.selected !== A) return null;
...
const result = await prepareImagePack(...A...);
if (this.state.selected !== A) return result;
```

But the second check happens **after** `prepareImagePack()` has already mutated the runner maps.

`prepareImagePack()` writes verified Files/provenance directly as it processes each entry. Therefore a stale A preparation can finish after B's `_scopePackProvenance()` and repopulate state B never authorized.

The promise queue serializes preparations, but it does not undo stale writes. B's queued preparation clears only **B's bound names**, not all stale names A may have written.

### Concrete race

Manifest A binds logical name `shared.webp`.

Manifest B references `shared.webp` but leaves it **unbound** (manual fallback), or binds a disjoint set.

Sequence:

1. select A → A repository fetch begins;
2. before A completes, select B;
3. B calls `_scopePackProvenance(B.pack)`; A has not written `shared.webp` yet, so nothing is cleared;
4. stale A fetch completes and `prepareImagePack(A)` writes:
   - `runner.files["shared.webp"] = AFile`
   - `runner.imgProvenance["shared.webp"] = AProvenance`
5. `_prepareImages(A)` notices selection changed and discards only the **result object**, not the side effects;
6. B's preparation runs later but does not clear `shared.webp` if B did not bind it.

B now carries A's provenance/File under a name that should be B's manual/unbound territory.

If B's size ledger happens to match (same-size different content is exactly the case SHA-256 was introduced for), Start can accept the stale File; `Runner._resolved()` sees provenance and can use the content-keyed upload path for A's bytes instead of B's intended manual file.

### Why the existing tests do not close it

The self-review test:

> “select manifest A, wait for preparation to finish, then select unbound manifest B”

is sequential. It proves stale **completed** provenance is cleared.

The concurrent-preparation test runs two preparations for the **same selected manifest** and proves serialization.

Neither tests “selection changes while the old fetch is unresolved.”

### Smallest robust correction

Make stale preparations incapable of mutating runner state.

Best shape:

1. `prepareImagePack()` should return verified Files/provenance as data and perform no writes to `runner.files` / `runner.imgProvenance`;
2. `ForgeCore._prepareImages(s)` commits that returned state only after confirming `this.state.selected === s`;
3. commit all entries atomically (or at least after every file is verified), then update `packResult`.

If preserving the current API, pass a selection generation/token into `prepareImagePack()` and check it immediately before every runner-map write. Re-checking `_scopePackProvenance()` at the start of each queued current preparation is useful, but by itself it does not prevent stale writes if the stale pass is still allowed to mutate.

### Required regression test

Use a controlled deferred repository response:

1. select packed manifest A binding `shared.webp`; hold its fetch unresolved;
2. select manifest B while A is pending; B references `shared.webp` unbound;
3. release A's fetch;
4. wait for all queued work;
5. assert B has:
   - no `imgProvenance["shared.webp"]`;
   - no A File under `runner.files["shared.webp"]`;
   - manual fallback remains missing until the operator picks B's file;
6. Start must remain blocked until B's manual file is supplied.

Repeat with A and B binding different packs and overlapping names to ensure the current selection always wins.

---

## 4. Areas reviewed that held

### Pack parse contract — sound

`forge/src/runner/imgpack.mjs` correctly rejects:

- non-commit refs;
- traversal/absolute/URL-like paths;
- malformed SHA-256;
- invalid/missing positive byte count;
- pack/imgSizes disagreement;
- extension mismatch.

Unused pack entries are advisory and excluded from fetch work.

### Manifest identity — sound

The normalized pack joins execution identity only when present. Pre-pack manifests retain their prior hashes, including non-default execution-policy manifests. This is the right compatibility direction.

### Cache identity — sound

`AssetCache` keys verified byte bodies by SHA-256, not path, commit, or logical name. Cache hits are re-verified before use. A corrupt cache body is removed and the immutable repository source is tried once.

### Repository provenance — sound

The authoring tool resolves a revision to a 40-hex commit and reads with `git cat-file blob <commit>:<path>`, so it cannot bind an uncommitted working-tree file.

### Repository fetch boundary — sound

Runtime fetches go through the existing GitHub client, not the game Session. The manifest path is constrained before it is inserted into the contents API URL.

### Upload reuse concept — sound, subject to F1

Bound-image upload reuse is content-keyed instead of filename-keyed, which correctly closes the stale-idmap problem. Once F1 prevents a wrong File from being recorded under a correct digest, this is the correct model.

### Manual fallback — sound in the non-racing case

A pack may cover a subset of images; unbound names continue through the existing picker/byte-ledger path. Bound images have no UI manual override.

---

## 5. Test/build evidence

Implementation handoff reports:

```
npm test                                  411 pass / 0 fail
check_imports.mjs                         40 modules / 71 imports / 0 violations
check_boundaries.mjs                      40 modules / 0 violations
check_release_pin.mjs                     release pin ok
build.mjs                                 forge_bundle.js rebuilt
check_bundle_budget.mjs                   447540/465000 raw; 86927/90000 gzip
derive_screens.mjs                        14 fixtures
```

No GitHub Actions workflow run is associated directly with the frozen SHA in the available workflow-run query.

This review environment did not execute the Node suite from a local checkout; the findings above are source-level invariants reproduced against the exact frozen tree. Both findings target cases the current tests do not cover.

---

## 6. Non-blocking observations

These remain secondary to F1/F2:

1. No real Android Firefox / ViolentMonkey / IndexedDB / WebCrypto smoke exists yet. The code fails closed when digest is unavailable, which is the right behavior.
2. The bundle budget is again at ~96%; future work has little headroom.
3. The image-pack authoring rules currently live only in the Node contract. That is acceptable for this phase; if Python validation learns the key later, it should invoke the canonical Node implementation rather than duplicate it.
4. Repository prefix policy (`art/` only vs any safe repo path) is a project-design choice, not a correctness blocker because digest + commit bind the bytes.
5. The eight Godstorm production files and actual `imagePack` for push/53 are still not committed. That should wait until the feature clears re-review.

---

## 7. Correction scope

A narrow correction round is appropriate. No redesign is required.

Required:

1. bind provenance to the exact verified File object (or re-hash at Start), with same-size swap regression coverage;
2. make stale/in-flight preparation unable to mutate runner state after selection changes, with a deferred-fetch manifest-switch regression test;
3. rerun the full Forge suite, screen fixtures, bundle build/budget, import/boundary/release-pin gates;
4. freeze a new SHA for narrow re-review.

Do **not** stage the Godstorm image pack or run manifest 53 until these two safety findings are closed and the corrected Forge build is integrated/released.
