# Content Workstream Bootstrap — independent review

**Repository:** `perseverance484/tnr-tools`  
**Implementation branch:** `fable/content-workstream-bootstrap`  
**Base:** `9ab4666a7b1ed5835807b56e7f2aac98e2c0cb10`  
**Reviewed target:** `e35b84e2290d1a00e298a58344a3eb0b4da58905` (frozen)  
**Review branch:** `chatgpt/review-content-workstream-bootstrap`  
**Review mode:** Lane A, Engineering Auditor with Art Director lens  
**Live-game activity:** none; no TNR API/game-page/Forge requests or writes were made by this review.

## Verdict

**REJECT / correction required before integration.**

The implementation is structurally strong and stays inside the two approved briefs, but two fail-closed guarantees that are central to those briefs are not actually enforced by the code:

1. the visual-reference materializer/validator can accept a result file without proving it is the single successful committed result for the approved read-only capture; and
2. a workstream task can be marked `COMPLETE` using an unverified prose claim as its only evidence.

A third status-coherence invariant should be fixed in the same narrow correction because otherwise a workstream can advertise itself as globally `COMPLETE` while unfinished tasks remain.

The current One Perfect Crop migration itself is conservative and correctly surfaces missing chat-side art bytes as a blocker rather than pretending they are durable repository inputs.

---

## CWB-1 — CONFIRMED DEFECT / integration blocker

### Reference-pack provenance is not fail-closed during materialization or verification

**Governing contract**

`state/prompt_tnr_art_reference_pack.md` requires the implementation to locate the committed result by `journal.manifestPath == push/03_tnr_art_style_reference_capture.json`, fail closed unless there is exactly one suitable successful result, require the expected full bodies, and use only that committed read-only capture as the source of reference bytes. The pack is meant to preserve provenance, not merely hashes of whatever file was supplied.

**What the target does**

`skills/producing-tnr-art/scripts/style_refs.py::materialize()` chooses either an arbitrary `--result` path or `index["source_capture"]["result"]`, loads it directly, extracts successful `gameAsset.get` captures by asset id, checks captured type/name, downloads `data.image`, and rewrites the index.

It does **not** verify the loaded result's:

- `journal.manifestPath`;
- `journal.jobId` / manifest hash against the indexed provenance;
- top-level `state == DONE` and `outcome == success`;
- zero mutation items from the actual journal;
- exact expected capture count/set;
- `persist == "full"` and `persistOk == true` for every expected capture;
- uniqueness of the intended successful result when using the normal maintainer path.

The `verify` command checks the index's *claim* that `source_capture.mutations` is zero, plus local byte/hash/dimension/format properties, but it does not cross-check the indexed provenance and per-reference source fields against the committed result file.

`--result` also accepts an arbitrary path object; an absolute path can escape the repository root when joined with `repo_root`, so the maintainer path is not restricted to a committed repository result.

**Refutation attempt**

The currently checked-in pack appears to have been materialized from the correct capture. `harvests/inbox/tnr_results_1789061570022.json` is `DONE / success`, its journal names `push/03_tnr_art_style_reference_capture.json`, job `3-mtvt26pp`, manifest hash `fb11961a`, `items: []`, and the inspected captures are successful `persist:"full"` records. The defect is therefore not evidence that the current image bytes came from the wrong capture.

That does not close the invariant: the durable maintainer/verification tool can later accept a wrong or crafted result containing matching asset records and rewrite a green-looking pack with false provenance.

**Practical consequence**

A future refresh can silently sever the pack from the approved capture while `style_refs.py verify` still reports byte-level integrity. Because the reference pack is specifically intended to make visual calibration reproducible across sessions, provenance is part of the safety contract rather than optional metadata.

**Smallest robust correction**

Add one shared socket-free result-validation path used by both `verify` and `materialize`:

1. Resolve the default result from committed `harvests/inbox/` by `journal.manifestPath`; require exactly one suitable successful result for the manifest, or otherwise fail with an actionable ambiguity/error. If retaining `--result`, require a repository-relative committed-style path and still validate it against the expected manifest/provenance.
2. Require `state == DONE`, `outcome == success`, expected journal manifest path, and zero journal mutation items.
3. Require exactly the 18 expected `gameAsset.get` captures with no duplicate/missing/extra expected ids, each `ok`, `rows == 1`, `persist == "full"`, `persistOk == true`, and carrying the expected id/type/name/image URL.
4. Cross-check index-level and per-reference provenance fields against that result during `verify`, not only during download.
5. Add socket-free fixtures for wrong manifest path, non-success result, non-empty mutation items, missing/duplicate/extra expected capture, non-full or failed persistence, and an absolute/external `--result` path.

No reference image or selection-policy change is required to close this finding.

---

## CWB-2 — CONFIRMED DEFECT / integration blocker

### `COMPLETE` can be satisfied by an unverified claim

**Governing contract**

The content-workstream brief and generated workflow make a central promise: **`COMPLETE` needs evidence, not a claim**, and downstream sessions should be able to rely on a completed task from repository-verifiable evidence.

**What the target does**

`content_workstream.py` defines evidence kinds including `note`, `decision`, `validator`, `approval`, `sha`, `path`, and `capture`. For a `COMPLETE` task the validator checks only that the evidence array is non-empty. It validates filesystem existence only for `path` and `capture`; it does not require any repository-verifiable evidence kind and does not validate a `sha` as an exact commit id.

Therefore a task equivalent to:

`status = COMPLETE`, `evidence = [{"kind":"note","ref":"done"}]`

passes the intended closing-evidence gate even though it is precisely a claim with no verifiable backing. The current selftest checks only the empty-evidence case and therefore does not exercise this bypass.

**Refutation attempt**

The One Perfect Crop tasks currently marked COMPLETE do carry real path/capture evidence, so the pilot migration is not abusing this hole. The defect is in the generic workstream invariant future projects will rely on.

**Practical consequence**

A later planning or task session can accidentally close work based on a durable but unsupported sentence in `roadmap.json`. Downstream sessions will then treat that dependency as satisfied and may skip required work, which defeats the main reason the workstream system exists.

**Smallest robust correction**

Make `COMPLETE` require at least one **verifiable anchor**. A minimal v1 rule would be:

- an existing repository `path` / `capture`; or
- a syntactically exact 40-hex `sha` (and, if practical without network, document that object existence is verified by the normal Git handoff/review rather than the stdlib validator).

`note` must never satisfy COMPLETE by itself. If `decision`, `approval`, or `validator` are intended to satisfy completion, give them a repository source/path field and validate that source rather than accepting free text alone. They may remain useful supplementary evidence.

Add selftests showing:

- note-only COMPLETE is rejected;
- malformed SHA is rejected;
- a valid existing path/capture satisfies the closing gate;
- a valid exact SHA satisfies it if SHA is retained as an anchor kind.

---

## CWB-3 — NEEDS REFINEMENT / include in narrow correction

### Overall workstream `COMPLETE` is not checked against task state

The validator checks that the top-level workstream status is a known enum, but it does not reject a workstream marked `COMPLETE` while tasks remain `PLANNED`, `READY`, `IN_PROGRESS`, `BLOCKED`, or `REVIEW`.

That permits `INDEX.md` and `ROADMAP.md` to advertise global completion while the task table visibly contradicts it.

Small correction: when workstream status is `COMPLETE`, require every task to be in a settled terminal state (`COMPLETE`, `SKIPPED`, or `SUPERSEDED`). Add one selftest. Do not overconstrain `ACTIVE`/`BLOCKED`; an active workstream may legitimately contain both READY and BLOCKED tasks.

---

## Verified sound at the reviewed SHA

- Live `main` remained exactly `9ab4666a7b1ed5835807b56e7f2aac98e2c0cb10`; the Fable branch remained frozen at `e35b84e2290d1a00e298a58344a3eb0b4da58905`. The branch is five commits ahead, zero behind, with the intended base as merge base.
- The implementation separates reference binaries (`art/style_refs/`) from the packaged skill. The index/tool stay under `skills/producing-tnr-art/`, preserving the existing 2 MiB skill ZIP policy without modifying the packer.
- The checked index contains the required 10 scene-character and 8 background references, the NINJA/CIVILIAN selection metadata, explicit Nameless Ninja exclusion, and Commander Okabe's framing/soft-edge limitation. It preserves the rule: **references calibrate; the spec governs**.
- The committed source result inspected for the current pack is `DONE / success`, journal-routed to the approved push/03 manifest, with zero journal items and full successful captures.
- Selection is deterministic in source: priority/order/key sorting, no randomness, target/register/tag/key filtering, and raw repository URLs for checkout-free callers.
- Art guidance now requires reading the spec, selecting references, visually inspecting the individual images, and using a clean generation context per asset class. It does not make URLs equivalent to consumed image references and does not recommend a collage.
- The workstream model preserves `docs/00_INDEX.md` precedence and the existing global state system; workflow docs explicitly describe roadmap state as coordination rather than canon.
- `content_workstream.py` rejects missing/unknown/self/cyclic dependencies, executable tasks with unfinished dependencies, missing durable resources, ephemeral/absolute/traversing paths, blocked tasks with no reason, executable tasks carrying blockers, COMPLETE with an empty evidence array, and IN_PROGRESS without a resume note.
- The One Perfect Crop pilot accurately marks accepted-but-uncommitted Ittetsu/Waystation Keeper/quest-icon bytes as BLOCKED instead of pretending the chat-side ZIP is durable. Splitting that intake from the otherwise READY scene-character task is a sound deviation from the approximate pilot table.
- The Road Bandit workstream state correctly points at the committed NEW-AI resolution; the unresolved Farming level 15 gate remains explicitly user-owned and is not silently mapped to character level.
- Final-head `skillpack` Actions run `34598501976` succeeded. Its logs independently show doctrine mapping at 0 errors/0 warnings, doctrine projections current, packs/TOCs current, catalog selftest green, and deterministic skill packaging. The final package sizes were 382,104 bytes for `building-tnr-content.zip` and 97,745 bytes for `producing-tnr-art.zip`; the second build matched the first, and the workflow found no generated changes.

## Review verification limits

The review environment could inspect the exact repository tree, commits, workflow logs, captures, scripts, JSON, and generated projections through the GitHub repository connector. It could not execute the branch's custom Python selftests in a local checkout. Therefore Fable's local `style_refs.py --selftest`, `style_refs.py verify`, `content_workstream.py --selftest`, workstream init/refusal examples, raw-QC selftest, art-preflight selftest, and `git diff --check` are not independently re-executed here. The final-head GitHub Actions gates listed above were independently inspected.

No live/browser/game validation is relevant or authorized for this task.

## Correction / re-review boundary

A **narrow re-review** is appropriate if Fable changes only:

- `skills/producing-tnr-art/scripts/style_refs.py` and its socket-free selftests to close CWB-1;
- `scripts/content_workstream.py` and its selftests to close CWB-2/CWB-3;
- generated/documentation text only where those corrections require it.

Do **not** change the 18 reference bytes, reference selection metadata/registers, One Perfect Crop task decomposition/content decisions, or wider workflow architecture unless a correction genuinely requires it. If any of those wider surfaces change, repeat the relevant full review.

For the correction handoff, rerun all task-required gates and explicitly include the new negative fixtures described above. Return a new exact frozen remote SHA. No live TNR requests, Forge runs, or game writes.
