# Art generation preflight / reference hydration — independent review

**Repository:** `perseverance484/tnr-tools`  
**Implementation branch:** `fable/art-generation-preflight`  
**Alias verified at same head:** `claude/art-generation-preflight-sq6j3n`  
**Intended base / live main during review:** `c5f8faaf2ddafe687b0dfb764ad5974e05823f86`  
**Frozen target:** `05c43de9eba065a59605d84378f45b7badca4664`  
**Review role:** Engineering Auditor, with Art Director supporting lens  
**Verdict:** **CHANGES REQUIRED — do not integrate this SHA.**

## Scope and authority

Reviewed against `state/prompt_art_generation_preflight_hydration.md`, the collaboration workflow, current workstream/art authorities, the frozen implementation, generated One Perfect Crop projections, the committed reference-bundle sidecar, and the final auto-built skill ZIP metadata.

The review made no TNR API/tRPC/game-page request, ran no Forge action, made no live-game write, and did not modify the Fable branch.

## AGP-1 — confirmed defect / integration blocker: production preflight can be redirected to noncanonical spec/index files

### Invariant

`generation_preflight.py` exists to render the **canonical current** generation contract and reference selection. The brief requires it to reuse the repository's current `25x_DATA_art_spec.json`, current `style_refs.json`, `shotlist.render_prompt`, and `style_refs` selection/provenance rather than creating another art authority.

A successful preflight must therefore mean that the contract came from those canonical repository owners, not from an arbitrary caller-selected JSON file.

### Evidence

The public CLI exposes both:

- `--spec <path>`
- `--index <path>`

and then resolves them as:

- `spec_path = args.spec or default_spec_path()`
- `index_path = args.index or style_refs.default_index_path()`

`prepare()` hashes and loads whatever files were supplied. `build_packet()` verifies the supplied index's bytes/capture provenance and renders from the supplied spec, but it never proves either path is the canonical repository owner.

This is not only theoretical test injection:

- a copied/edited art spec can change the positive/negative scaffold while still producing a successful packet and a new contract hash;
- a copied/edited reference index can change `priority`, `order`, tags or other selection metadata while retaining the same captured asset ids and exact reference bytes, because those calibration/selection fields are not capture-derived provenance fields;
- `raw_url()` also accepts the index's `raw_url_template`, so an alternate verified index can change the URLs emitted to the operator without changing the underlying captured bytes.

The packet can therefore say the reference pack is verified and present a "canonical generation contract" even though the production CLI was pointed at a noncanonical spec or index.

### Practical consequence

This recreates the class of false-green the task was built to eliminate. A fresh art session could stage the wrong prompt or wrong selected references after a successful preflight and believe the repository had proven the contract.

### Smallest robust correction

For the production CLI:

1. remove public `--spec` and `--index` overrides, **or** require any supplied value to resolve exactly to the canonical repository paths for this checkout and fail closed otherwise;
2. apply the same restriction to both `prepare` and `check` CLI commands;
3. keep injectable `spec_path` / `index_path` function parameters for socket-free synthesized selftests if useful — test injection does not need to be a production escape hatch;
4. add negative CLI/selftests proving alternate spec/index paths are rejected before a packet is emitted.

Do not change `25x_DATA_art_spec.json`, `style_refs.json`, the 18 reference bytes, or their current selection metadata as part of this correction.

## AGP-2 — needs refinement before integration: One Perfect Crop gate duplicates the selector's exact key set in free text

### Invariant

The workstream is coordination state, not art canon. `style_refs.json` plus the deterministic selector / generation preflight own which references are selected for a target. The roadmap should route a session to that result, not create a second static copy of dynamic selection state.

### Evidence

`art.scene_characters.session_gates.visual_reference_hydration.requirement` states that the deterministic selection is exactly:

`commander_okabe, winter_crow, pale_fang, old_ghost`

At the reviewed SHA that happens to agree with `style_refs.select`, so there is no present mismatch.

However, `content_workstream.py` validates only the shape/text of a session gate. It does not and should not interpret that sentence or cross-check the embedded names against `style_refs.select`. A later approved reference-pack selection change can therefore leave the roadmap sentence stale while both the workstream validator and reference-pack verifier remain green.

### Practical consequence

A future session can receive two conflicting instructions: the roadmap gate names one four-image set while the deterministic preflight names another. That is exactly the sort of cross-session drift the workstream/reference-pack architecture is intended to remove.

### Smallest robust correction

Do not hard-code selector output in the gate requirement. Change it to require:

> every individual reference named by the deterministic generation-preflight packet for this target/register is rendered and visually inspected in the current session

The preflight packet itself should continue to print the exact current keys. The fresh-session Smoke A requirement to "name the exact four selected references" is then satisfied from the selector output rather than from duplicated roadmap prose.

Apply the same principle anywhere else a runtime gate restates dynamically selected keys.

## AGP-3 — required acceptance gate still outstanding: fresh-chat product smoke

This is **not a source-code defect**, but it blocks an integration recommendation because the implementation brief explicitly requires a manual product-level smoke before final workflow acceptance.

Automated/source review cannot prove that a new ChatGPT conversation actually stops when references are not hydrated or that real rendered image attachments flow through the intended generation sequence.

The brief's sample Smoke A prompt names only the workstream/task. Because the implementation is still on an unmerged Fable branch and `main` remains at the base, the actual pre-integration smoke must explicitly target the corrected frozen Fable SHA/branch; otherwise a fresh conversation that follows normal bootstrap would test old `main` instead of the implementation under review.

After source corrections pass narrow re-review, run:

- **Smoke A:** fresh conversation, explicitly initialize from the corrected frozen branch/SHA, no reference images attached. It must report repository READY but action GATED / NOT_HYDRATED, name the current selected references, and not call image generation.
- **Smoke B:** fresh conversation on that same exact SHA with the selected individual images attached/rendered. It must visually inspect them, declare the actual reference mode, surface user-owned Road Bandit direction choices, stage the deterministic contract, wait for user authorization, generate exactly one provisional candidate, and raw-QC it before processing.

Record the smoke result durably before integration recommendation.

## Verified sound at the frozen SHA

- `main` remained `c5f8faaf2ddafe687b0dfb764ad5974e05823f86` during review; the Fable branch remained exactly `05c43de9eba065a59605d84378f45b7badca4664`. The Claude alias was independently verified at the same head.
- The branch is six commits ahead of the intended base with no base drift in the submitted relationship.
- `session_gates` are kept separate from durable blockers/status/dependency satisfaction; validation is strict about required fields, duplicate ids, unknown fields and `STOP`-only behavior.
- `content_workstream.py` now counts `SUPERSEDED` as settled, matching the validator's terminal-state rule.
- The initializer distinctly reports repository task status vs action readiness and explicitly says unproven runtime gates forbid the action.
- `generation_preflight.py` reuses `shotlist.render_prompt` and `style_refs` rather than copying house-style/scaffold text. Runtime state starts fail-closed (`pixels_inspected=false`, `reference_mode=UNDECLARED`, `clean_asset_context_confirmed=false`, `generation_allowed=false`).
- Reference file hashes are checked; excluded/deprecated references are refused; the Road Bandit selftest source asserts the intended current NINJA selection and prompt equality.
- The operator reference bundle is outside `skills/`, uses exact source image bytes with no transcode, fixed ZIP metadata, no contact sheet, and documents that uploading the ZIP is not hydration. Its committed sidecar reports 18 image references / 21 ZIP members, 2,266,882 bytes, SHA-256 `3325848bcaab4c5197d0cd7ce465e1f4770ae32fbe35e9acc1c94900ac3818bd`, sourced from the approved 18-read/zero-mutation capture.
- The final `dist/producing-tnr-art.zip` is 124,888 bytes at the frozen SHA, far below the existing 2 MiB guard. The final frozen head is itself the skillpack automation commit.
- The implementation diff does not alter the 18 `art/style_refs/...` source images, `skills/producing-tnr-art/data/style_refs.json`, or `25x_DATA_art_spec.json`.
- One Perfect Crop prose, encounter graph, combat specification, and content-admin values were not changed. The Road Bandit glow/weapon tensions remain surfaced as user-owned decisions instead of being silently settled.

## Test / environment limitation

I could not independently execute the repository Python selftests/builds in a local checkout because outbound GitHub/DNS cloning is unavailable in this review runtime. The source contains the expected synthesized selftests, and the implementation commits state that the workstream validation/render checks and other gates passed, but those author-reported executions are not independently reproduced here.

GitHub exposes no PR-triggered workflow/status set for this frozen branch because no implementation PR exists yet. The final frozen head is an automated `skillpack: rebuild dist + sync root config [auto]` commit, and final repository metadata confirms the rebuilt art skill ZIP size noted above.

The correction handoff should rerun the complete gate list from the implementation brief and report exact results. The narrow re-review can remain focused on AGP-1/AGP-2 plus confirming no wider changes occurred.

## Next workflow step

1. Fable applies AGP-1 and AGP-2 on its existing implementation branch and returns a new frozen remote SHA.
2. ChatGPT performs a narrow source re-review if the correction stays inside the specified surface.
3. Only after source approval, run the required fresh-chat Smoke A and Smoke B against the **exact corrected frozen SHA**, and record the smoke result durably.
4. Integration may be recommended only after both source review and required product smoke pass.
