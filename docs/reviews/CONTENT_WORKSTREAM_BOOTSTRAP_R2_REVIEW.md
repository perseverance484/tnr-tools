# Content Workstream Bootstrap — round-2 correction review

**Repository:** `perseverance484/tnr-tools`  
**Implementation branch:** `fable/content-workstream-bootstrap`  
**Original implementation base:** `9ab4666a7b1ed5835807b56e7f2aac98e2c0cb10`  
**Previous rejected target:** `e35b84e2290d1a00e298a58344a3eb0b4da58905`  
**Reviewed target:** `3212969a562e1d7b6e11cb3c5cc21821ab8bc7c4` (frozen)  
**Review branch:** `chatgpt/review-content-workstream-bootstrap-r2`  
**Review mode:** Lane A narrow correction review, Engineering Auditor  
**Live-game activity:** none; no TNR API/game-page/Forge requests or writes were made by this review.

## Verdict

**APPROVE for integration.**

The new target is three commits ahead of the rejected SHA and remains inside the explicitly authorized correction surface. The two round-1 integration blockers (CWB-1 and CWB-2) and the requested status-coherence correction (CWB-3) are closed in the implementation. No reference bytes, reference selection metadata/registers, One Perfect Crop roadmap/task semantics, doctrine, engine laws, or wider workflow architecture changed.

One low-severity projection-count inconsistency remains: `progress_line()` counts `COMPLETE` + `SKIPPED` as settled but does not count `SUPERSEDED`, even though `SUPERSEDED` is a satisfied terminal state and is now allowed inside a top-level `COMPLETE` workstream. A workstream containing a superseded task could therefore validate as `COMPLETE` while rendering, for example, `4/5 settled`. This is an operator-display cleanup, not a task-readiness, evidence, provenance, or production-safety blocker. It does not affect the current One Perfect Crop roadmap, which has no superseded task.

---

## CWB-1 — CLOSED

### Reference-pack provenance now fails closed

`skills/producing-tnr-art/scripts/style_refs.py` now has one shared provenance path used by verification and materialization.

The v1 approved capture manifest is pinned in code as `push/03_tnr_art_style_reference_capture.json` with an expected 18 reads. Default resolution scans committed `harvests/inbox/*.json` results for that journal manifest and only considers `DONE` / `success` candidates, requiring exactly one successful match. Zero matches and multiple successful matches both fail closed.

An explicit `--result` no longer escapes the repository: path traversal is rejected and an absolute path outside the repository is rejected. The named file still has to pass the same provenance checks; the override does not bypass the approved manifest.

The actual result is checked for:

- top-level `DONE` / `success`;
- approved `journal.manifestPath`;
- indexed `jobId` and `manifestHash` agreement when indexed;
- empty journal mutation items;
- exact expected capture count;
- exactly the indexed reference asset set, with missing, duplicate and unexpected captures rejected;
- `gameAsset.get` procedure;
- `ok == true`, `rows == 1`, `persist == "full"`, `persistOk == true`;
- expected record id/type/name and nonempty captured image URL.

`verify` additionally checks each reference's `source_capture`, captured image URL and snapshot key against the resolved committed result, alongside the existing local SHA-256/dimension/format checks. The index's recorded top-level result path is also checked against the uniquely resolved result on the normal verification path.

The new socket-free fixtures exercise the round-1 adversarial cases: wrong manifest, non-DONE/non-success state including through explicit override, mutation items, job/hash disagreement, missing/duplicate/extra captures, persistence failures, failed/no-row reads, wrong type/name, missing/mismatched image URL, snapshot mismatch, stale index result, outside/traversing override, duplicate successful results, and no matching result.

The correction does not alter the 18 materialized reference files or their selection metadata.

### Minor residual observations, not blockers

Two provenance checks could be tightened in a later maintenance pass without changing the current safety conclusion: the capture request's `input.id` is not separately compared with the returned record id, and a missing `snapshotKey` is tolerated even though a present snapshot key is cross-checked. The committed approved result carries the expected inputs and snapshot keys, and the required record ids/source URLs/full-body persistence are independently checked, so neither creates a current false-green path to a different asset/capture under the approved manifest.

---

## CWB-2 — CLOSED

### `COMPLETE` now requires a verifiable anchor

`scripts/content_workstream.py` now distinguishes explanatory evidence from an anchor that can close a task.

A `COMPLETE` task requires at least one of:

- `path` / `capture` whose repository-relative path exists;
- an exact lowercase 40-hex `sha`; or
- `decision`, `validator`, or `approval` with a durable repository `source` path that exists.

`note` never anchors completion by itself. Malformed SHAs are rejected, and `source` paths receive the same ephemeral/absolute/traversal/missing-path checks as other durable paths.

The selftest additions cover note-only rejection, free-text decision/validator/approval rejection, sourced acceptance and missing/sandbox-source rejection, mixed note + real anchor acceptance, malformed SHA forms, exact SHA, existing path/capture, and the original empty-evidence rule.

The One Perfect Crop roadmap was not changed; its existing COMPLETE tasks already use path/capture anchors.

---

## CWB-3 — CLOSED

A top-level workstream marked `COMPLETE` now rejects every task whose status is not one of `COMPLETE`, `SKIPPED`, or `SUPERSEDED`, and names the unsettled tasks in the error. `ACTIVE` and `BLOCKED` workstreams remain intentionally unconstrained so they can contain a mix of ready and blocked work.

The selftest covers both rejection of a COMPLETE workstream with READY/PLANNED work and acceptance of all-terminal COMPLETE state, plus an ACTIVE mixed READY/BLOCKED case.

The only residual display issue is the non-blocking `SUPERSEDED` progress count noted in the verdict.

---

## Scope and target integrity

- The Fable branch was verified at exactly `3212969a562e1d7b6e11cb3c5cc21821ab8bc7c4`.
- `e35b84e... -> 3212969...` is a straight three-commit advance, zero behind, with the rejected SHA as merge base.
- `9ab4666... -> 3212969...` is a straight eight-commit implementation history with the intended original base as merge base.
- Round-2 changed only:
  - `skills/producing-tnr-art/scripts/style_refs.py`
  - `skills/producing-tnr-art/SKILL.md`
  - `scripts/content_workstream.py`
  - `docs/workflows/CONTENT_WORKSTREAM.md`
  - `dist/producing-tnr-art.zip`
- No file under `art/style_refs/`, `skills/producing-tnr-art/data/style_refs.json`, or `state/workstreams/one_perfect_crop/` changed in the correction.

This is inside the round-1 narrow re-review boundary.

---

## Gates and generated artifact evidence

The final-head GitHub Actions `skillpack` run `34600651523` completed successfully at exact SHA `3212969a562e1d7b6e11cb3c5cc21821ab8bc7c4`.

Its inspected logs show:

- doctrine map: 21 assertions, 18 referenced, 16 surfaces; 0 errors, 0 warnings;
- doctrine projections current;
- content packs and TOCs current;
- catalog-sync selftest green;
- two consecutive skill builds byte-identical;
- `dist/building-tnr-content.zip`: 382,104 bytes, SHA prefix `68bad1157ba5` both runs;
- `dist/producing-tnr-art.zip`: 102,801 bytes, SHA prefix `325a2b1c2065` both runs;
- generated-file commit step reported `no generated changes`.

The final-head privacy/scrub workflow also completed successfully.

The review environment could inspect repository source, diffs, commits, committed capture data and GitHub Actions logs, but could not clone/execute the branch locally because the review runtime had no outbound GitHub/DNS path. Therefore Fable's script-local `style_refs.py --selftest`, production `style_refs.py verify`, `content_workstream.py --selftest`, workstream init/refusal examples, raw-QC/art-preflight selftests and `git diff --check` were not independently re-executed by ChatGPT. The added negative fixtures and relevant implementation paths were inspected directly; the final-head repository workflows above were independently verified.

No browser/live/session verification is required for this repository-only task, and none was performed.

---

## Review-side repository incident

While creating this round-2 review branch, ChatGPT mistakenly invoked a repository file-create operation without the intended `chatgpt/*` branch parameter. That created a temporary root file `noop` directly on `main` in commit `23a0a9d91cd0820ec71d6690e5e3fb16b284b221`.

ChatGPT immediately deleted that file in commit `3ed18740db160103746dcf2b13b69c34f80f5ae4` rather than rewriting history or force-moving `main`.

The restored `main` commit has tree SHA `84b25472c5ffca72a9095b3266bfcbe11c6d7441`, exactly the same tree SHA as the original integration base `9ab4666a7b1ed5835807b56e7f2aac98e2c0cb10`. A commit comparison from `9ab4666...` to `3ed1874...` reports two commits and **zero net changed files**.

Therefore the incident changed `main` history/SHA but not repository content. The current integration baseline is now `main@3ed18740db160103746dcf2b13b69c34f80f5ae4`, content-identical to the originally reviewed base. Do not force-push or rewrite `main` to erase the incident.

Because the current `main` tree is byte-for-byte identical to the original base tree, this history-only drift does not invalidate the implementation review. A normal merge/PR of the exact reviewed Fable target into current `main` preserves the reviewed implementation content without requiring a Fable rebase solely for this incident.

---

## Next permitted step

The implementation may proceed to integration of exact Fable SHA `3212969a562e1d7b6e11cb3c5cc21821ab8bc7c4` into the current `main`, after one immediate re-check that the branch still points at that target and `main` still points at `3ed18740db160103746dcf2b13b69c34f80f5ae4` (or, if `main` has moved again, that any new drift is reviewed before integration).

Use the normal reviewed Lane A integration path. Do not treat integration as authorization for any live-game action.

After integration, the content-workstream system can be used for the already-ready One Perfect Crop art tasks. The blocked accepted-art intake and user-owned balance/eligibility decisions remain blocked exactly as represented by the unchanged pilot roadmap.
