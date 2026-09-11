# Implementation brief — fail-closed art generation preflight and reference hydration

**Repository:** `perseverance484/tnr-tools`  
**Lane:** A — art/workstream tooling and collaboration infrastructure  
**Implementation owner:** Fable / Claude Code  
**Independent reviewer:** ChatGPT  
**Planning owner:** ChatGPT, Art Director lead with Engineering Auditor supporting lens  
**Base SHA at plan freeze:** `4b1cfd9a5ab1906009b37c82be7f7c4896c6194f`  
**Suggested Fable branch after this brief is integrated:** `fable/art-generation-preflight`  
**Live-game policy:** repository-only. No TNR API/tRPC/game-page requests, no Forge, no fresh live capture, and no game writes.

## Problem proven by the One Perfect Crop Road Bandit failure

The repository now has a provenance-checked visual reference pack and deterministic reference selection, but a fresh ChatGPT art session can still reach image generation without the selected reference pixels becoming usable visual context.

The failed Road Bandit generation demonstrated the consequence: the output was a photorealistic/cinematic roadside ninja scene instead of a TNR `SCENE_CHARACTER`. It violated the canonical generation contract simultaneously on rendering register, background mode, lighting, camera/perspective and composition.

A follow-up generation-preflight diagnostic at live `main@4b1cfd9a5ab1906009b37c82be7f7c4896c6194f` established:

- `state/workstreams/one_perfect_crop/roadmap.json` correctly marks `art.scene_characters` READY at the repository layer;
- the deterministic NINJA reference selection is `commander_okabe`, `winter_crow`, `pale_fang`, `old_ghost`;
- the session could read the reference metadata, hashes, paths, provenance and URLs;
- it had **not visually inspected any selected reference pixels**;
- repository connector access to metadata/base64 is not the same as rendering the pixels into the assistant's visual context;
- those repo files were not actual image attachments available to the image-generation surface;
- the canonical `SCENE_CHARACTER` prompt can be reconstructed exactly from `25x_DATA_art_spec.json` through `shotlist.py::render_prompt`, but ChatGPT's image-generation tool does not expose a repository-file argument or a durable exact-prompt transport owned by this repository. The product infers generation instructions from conversation context.

The current art workflow already says URLs are not evidence that pixels were ingested and already requires visual inspection. The defect is that the workstream/session tooling does not represent or enforce the runtime boundary strongly enough, and no operator-friendly hydration fallback exists.

## Objective

Make production art sessions fail closed at the point between **repository readiness** and **image generation**.

A fresh art session must be able to determine, before any generation call:

1. the exact canonical target/frame/prompt contract;
2. the exact selected style references and their hashes;
3. whether the selected reference pixels have actually been visually inspected in the current session;
4. whether the generation surface has the selected individual images as real image inputs, or only a text-grounded description;
5. whether the generation context is clean for the current asset class;
6. which user-owned art-direction decisions remain unresolved;
7. whether generation is allowed now or must stop.

The implementation must make an unmet runtime gate visible and actionable. It must never turn a URL, file path, base64 blob, or metadata record into a false claim that the assistant or generator saw the pixels.

## Governing authority

Read before implementation:

- `state/active-context.md`
- `state/status.json`
- `docs/00_INDEX.md`
- `docs/RULINGS.md`
- `CLAUDE.md`
- `CHATGPT.md`
- `docs/DEVELOPMENT_WORKFLOW.md`
- `docs/workflows/CONTENT_WORKSTREAM.md`
- `docs/workflows/ART_PRODUCTION.md`
- `docs/agents/README.md`
- `docs/agents/ART_DIRECTOR.md`
- `docs/agents/IMAGE_PRODUCTION.md`
- `skills/producing-tnr-art/SKILL.md`
- `skills/producing-tnr-art/references/prompts.md`
- `skills/producing-tnr-art/data/25x_DATA_art_spec.json`
- `skills/producing-tnr-art/data/style_refs.json`
- `skills/producing-tnr-art/scripts/style_refs.py`
- `skills/producing-tnr-art/scripts/shotlist.py`
- `scripts/content_workstream.py`
- `state/workstreams/one_perfect_crop/roadmap.json`

Authority boundaries:

- `25x_DATA_art_spec.json` remains the sole owner of house-style clauses, target contracts and prompt scaffolds.
- `style_refs.json` remains calibration/provenance/selection metadata, not art doctrine.
- workstream roadmaps remain coordination state, not art canon.
- the user retains final art direction and final acceptance.
- this task must not rewrite art style, balance, content or live-game rules to make the tooling convenient.

## Design principle — repository-ready is not the same as action-ready

Do **not** add another global task status enum for every runtime circumstance.

Keep the existing workstream status model. `READY` means the durable repository prerequisites and dependencies are complete enough for the session to initialize and begin the task.

Add a separate, explicit concept of **session/runtime gates** for actions that depend on capabilities of the current execution surface. For art generation, a task may be repository-READY while image generation is still action-gated until the current conversation actually hydrates the required pixels and settles enough visual direction.

The initializer must make this distinction unmistakable, for example:

```text
TASK STATUS       : READY (repository prerequisites satisfied)
ACTION READINESS  : GATED
SESSION GATES:
  [ ] selected style-reference pixels visibly inspected in this session
  [ ] reference mode declared: ATTACHED or ASSISTANT_GROUNDED
  [ ] clean asset-class generation context confirmed
  [ ] canonical generation contract staged
```

A runtime gate is not a fake blocker in `roadmap.json`, and satisfying it is normally session-local rather than permanent repository evidence. Permanent outputs/acceptance still close the task through the existing evidence rules.

## Phase A — workstream session gates

Extend `scripts/content_workstream.py` and `docs/workflows/CONTENT_WORKSTREAM.md` with an optional task-level field named `session_gates`.

### v1 `session_gates` shape

Use a small explicit object form rather than free-text-only strings:

```json
"session_gates": [
  {
    "id": "visual_reference_hydration",
    "before": "image_generation",
    "requirement": "Selected individual style-reference pixels are rendered and visually inspected in the current session; metadata, URL text and unrendered base64 do not satisfy this.",
    "on_fail": "STOP"
  }
]
```

Required fields:

- `id` — stable within the task;
- `before` — concise action name such as `image_generation`;
- `requirement` — what the current session must prove;
- `on_fail` — v1 supports `STOP` only. Do not invent a warning-only bypass for a required runtime gate.

Validator requirements:

- `session_gates`, when present, is an array of objects;
- ids are nonempty and unique inside the task;
- `before` and `requirement` are nonempty strings;
- `on_fail` must be `STOP` in v1;
- session gates do not count as durable blockers and do not change dependency satisfaction;
- a READY/IN_PROGRESS task may carry session gates;
- a BLOCKED task still uses `blockers` / `open_decisions` for durable prerequisite failures exactly as today.

Initializer requirements:

- print a distinct `SESSION GATES / ACTION READINESS` section before deliverables;
- if gates exist, say explicitly that the task is repository-ready but the named action must not occur until the current session proves the gates;
- never print `GENERATION READY` merely because the roadmap status is READY;
- preserve deterministic output.

Add selftests for malformed gates, duplicate ids, supported/unsupported `on_fail`, deterministic init output and the distinction between repository READY and action-gated READY.

Also fix the already-reviewed low-severity projection bug while touching this script: `progress_line()` must count `SUPERSEDED` as settled, matching the validator's terminal-state rule.

## Phase B — deterministic art generation preflight helper

Add:

```text
skills/producing-tnr-art/scripts/generation_preflight.py
```

This is a **contract renderer**, not an image generator and not a second prompt authority.

It must import/reuse the existing canonical functions/data rather than copy prompt wording:

- use `shotlist.py::render_prompt` for the canonical prompt scaffold;
- use `style_refs.py` selection logic for reference selection;
- load `25x_DATA_art_spec.json` for target/frame/house-style authority;
- load `style_refs.json` for reference metadata/provenance.

Do not duplicate house-style clauses or scaffold strings in this new script.

### Required command

Support a deterministic invocation similar to:

```bash
python3 skills/producing-tnr-art/scripts/generation_preflight.py prepare \
  --repo-root . \
  --target SCENE_CHARACTER \
  --register NINJA \
  --frame full \
  --subject "generic Road Bandit; lone adult male roadside shinobi ambusher; anonymous and unbranded" \
  --repo-ref <EXACT_MAIN_SHA>
```

Support human-readable stdout plus `--json`.

### Packet content

At minimum emit:

- packet schema/version;
- target;
- register/tag selection inputs where relevant;
- frame;
- subject text exactly as supplied;
- spec path and a SHA-256 of the spec bytes;
- exact selected reference keys in deterministic order;
- for each reference: local repo path, file SHA-256, target/register, calibration note, `do_not_use_for` note when present, and a raw GitHub URL pinned to the supplied exact repo ref rather than floating `main`;
- exact canonical prompt object returned by `shotlist.render_prompt` (`positive`, `negative`, `subject_line`, costume grammar/hard negatives and other canonical fields when present);
- a SHA-256 over the canonical generation-contract JSON using a documented canonical JSON serialization;
- explicit runtime state fields initialized as **unverified**, for example:
  - `visual_reference_pixels_inspected: false`
  - `reference_mode: "UNDECLARED"`
  - `clean_asset_context_confirmed: false`
  - `generation_allowed: false`
- explicit instruction that the helper cannot prove ChatGPT conversation/image-tool state and therefore cannot flip those runtime fields by itself.

### Fail-closed checks

For a repository checkout:

- selected reference pack verification/provenance must pass before the packet is emitted;
- requested target/register/frame must exist;
- selected reference files must exist and hash-match the index;
- no selected reference may be excluded/deprecated;
- exact prompt rendering must match `shotlist.render_prompt` byte-for-byte/field-for-field in tests.

The helper must be socket-free.

### Prompt-contract observations

The diagnostic exposed two Road Bandit-specific tensions:

- the AI/content intent has `element: None`, while the generic `SCENE_CHARACTER` scaffold contains a literal required elemental glow phrase in addition to the house-style clause saying **at most one** accent;
- the Road Bandit has Bukijutsu combat flavor, while the generic scene-character negative contains `no props`.

Do **not** silently change the global art spec in this implementation. The helper may surface a neutral `direction_review_required` note when the selected workstream task carries open art-direction decisions, but it must not infer an override.

Any change to the global prompt scaffold/style semantics requires a separate user art-direction ruling or an explicitly approved follow-up brief.

## Phase C — reference hydration fallback for mobile/fresh ChatGPT sessions

Extend `skills/producing-tnr-art/scripts/style_refs.py` with a socket-free deterministic bundle command.

Suggested interface:

```bash
python3 skills/producing-tnr-art/scripts/style_refs.py bundle \
  --repo-root . \
  --output art/style_refs/tnr_style_reference_pack.zip
```

The bundle is an **operator transfer artifact**, not a generator collage.

Requirements:

- verification/provenance must pass before bundling;
- include the exact individual reference image bytes unchanged;
- include `style_refs.json` and a small generated `README.txt`/manifest listing file keys, SHA-256s and the rule that selected images must be uploaded/used individually;
- never create a contact sheet for generator use;
- deterministic file order, timestamps/permissions and ZIP bytes across repeated builds;
- no network access;
- no transcoding;
- report total archive bytes and SHA-256;
- add a `--check` mode that compares the committed bundle with a fresh deterministic build and fails on drift.

Commit the generated archive under `art/style_refs/` or a sibling `art/style_ref_bundles/` location outside `skills/`, so it does not inflate `dist/producing-tnr-art.zip`.

The purpose is to let the operator download one durable pack to a phone, extract it once, and multi-select the exact individual reference images named by a future session.

The documentation must say clearly:

- uploading the ZIP itself is not sufficient image-reference hydration;
- the selected individual images must become rendered conversation images/attachments when the ChatGPT generation surface needs actual image inputs;
- if the assistant can visually inspect selected images through another real rendered-image path but the generator cannot take image references, the session may use `ASSISTANT_GROUNDED` mode only when the workflow permits it and must say that the generator did not receive the images;
- metadata/URLs/base64 without visual rendering are `NOT_HYDRATED` and generation must stop.

Add selftests for exact bundle membership, unchanged image hashes, exclusion of unselected/deprecated content where selection-specific bundle mode is supported, deterministic ZIP hash and drift checking.

## Phase D — ChatGPT/art workflow generation gate

Update, without restating numerical art contracts:

- `skills/producing-tnr-art/SKILL.md`
- `skills/producing-tnr-art/references/prompts.md`
- `docs/workflows/ART_PRODUCTION.md`
- `CHATGPT.md` art/workstream guidance where the ChatGPT-specific bridge belongs

### Reference modes

Define these terms consistently:

**ATTACHED**
- selected individual reference images are actual rendered image attachments/input images in the current generation conversation;
- preferred for ChatGPT production generation when selected references exist.

**ASSISTANT_GROUNDED**
- the assistant actually visually inspected the selected pixels, but the generation surface cannot receive the reference images as image inputs;
- the session uses the canonical text generation contract grounded by that inspection;
- it must not claim reference-image conditioning.

**NOT_HYDRATED**
- only metadata, paths, URLs or unrendered bytes/base64 are available;
- image generation is forbidden until hydration occurs.

### ChatGPT-specific staging rule

The repository cannot add a binary argument to ChatGPT's image-generation product surface. Do not pretend otherwise.

For ChatGPT image generation, document the collaboration rule:

1. initialize the workstream task;
2. render the deterministic generation preflight packet;
3. hydrate and visually inspect the selected individual references;
4. prefer `ATTACHED` when ChatGPT can use those conversation images as references;
5. settle enough user-owned visual direction for one meaningful candidate;
6. immediately before the image-generation tool call, stage the canonical generation contract in the conversation from the preflight packet so the product's context-inferred image generation is grounded in the exact target/scaffold/subject/negative contract;
7. only then generate one candidate.

Do not claim the repository can prove what internal prompt representation the product used. The repository can prove what contract was staged and what references were present.

### Candidate state

Change the workflow language so a returned generation is a **PROVISIONAL RAW CANDIDATE**, not an implied accepted asset.

Immediately after generation:

- run/perform raw QC before processing;
- a wrong visual register, scenery on a keyed character target, wrong aspect/mode, prohibited insignia, wrong framing/camera, or other canonical raw failure is a REJECT and must not be processed;
- only a raw-QC pass proceeds to chroma/processing, dark-composite QC and art preflight;
- final acceptance remains user-owned.

## Phase E — One Perfect Crop pilot migration

Update `state/workstreams/one_perfect_crop/roadmap.json` and regenerate its projections.

Do not change the frozen prose, encounter graph, combat spec or content-admin decisions.

For `art.scene_characters`:

- keep status `READY` if repository dependencies/resources remain complete;
- add session gates at least for:
  - selected reference pixel hydration/visual inspection before image generation;
  - reference mode declaration (`ATTACHED` preferred for ChatGPT, otherwise explicit `ASSISTANT_GROUNDED` only if pixels were actually inspected);
  - clean SCENE_CHARACTER-only generation context;
  - deterministic canonical generation preflight packet staged before the generation call;
- add `generation_preflight.py` and the durable reference bundle/index to required resources after they exist;
- preserve the existing final-art-direction/final-acceptance user ownership;
- surface, but do not settle, the Road Bandit glow/weapon prompt tensions described above if they remain unresolved.

Do not mark `art.scene_characters` BLOCKED merely because one runtime lacks hydrated images. The durable inputs exist; the action gate is session/runtime state. If the actual reference files ever disappear from the repository, that is a real repository blocker and the existing READY validation should fail.

Apply the generic art-session gate pattern to other One Perfect Crop art-generation tasks only where it is semantically correct. Do not claim an AI-avatar/icon reference pack exists if v1 contains only scene-character/background references.

Regenerate:

- `state/workstreams/one_perfect_crop/ROADMAP.md`
- `state/workstreams/INDEX.md`

## Manual acceptance test — required before integration recommendation

Automated tests cannot prove ChatGPT product image attachment behavior. After Fable's branch passes source/tests and ChatGPT reviews it, run one explicit operator-facing smoke in a fresh ChatGPT conversation before declaring the workflow behavior-proven.

### Smoke A — no hydrated references

Start:

```text
Initialize session from repo. Workstream: One Perfect Crop. Task: art.scene_characters.
```

With no selected images attached/visually rendered, the session must:

- load the task;
- report repository status READY;
- report image generation ACTION GATED / NOT_HYDRATED;
- name the exact four selected references;
- provide the durable bundle/raw paths needed to hydrate them;
- **not call image generation**.

### Smoke B — hydrated references

Then provide the exact selected individual images to the conversation.

The session must:

- visually inspect all four;
- where file access permits, hash-check uploaded bytes against `style_refs.json`; otherwise state that hash equivalence is unverified rather than assuming;
- declare reference mode;
- present/surface the still-user-owned Road Bandit direction choices that materially affect the first candidate;
- stage the deterministic generation contract from the canonical packet;
- generate exactly one provisional candidate only after the user authorizes the direction/generation step;
- immediately raw-QC it against the TNR contract before any processing.

The first candidate need not be user-accepted for the tooling smoke to pass, but the session must prove the new fail-closed sequence and must not reproduce the old silent URL/metadata→generation jump.

Record the smoke result durably before final workflow acceptance.

## Tests and gates

At minimum run:

```text
python3 scripts/content_workstream.py --selftest
python3 scripts/content_workstream.py validate --all
python3 scripts/content_workstream.py render --check
python3 scripts/content_workstream.py init one_perfect_crop --task art.scene_characters

python3 skills/producing-tnr-art/scripts/style_refs.py --selftest
python3 skills/producing-tnr-art/scripts/style_refs.py verify --repo-root .
python3 skills/producing-tnr-art/scripts/style_refs.py bundle --repo-root . --output <temp-a.zip>
python3 skills/producing-tnr-art/scripts/style_refs.py bundle --repo-root . --output <temp-b.zip>
# assert temp-a.zip and temp-b.zip are byte-identical

python3 skills/producing-tnr-art/scripts/generation_preflight.py --selftest
# include an exact Road Bandit prepare fixture and assert selected keys/order + canonical prompt equality

python3 skills/producing-tnr-art/scripts/rawqc.py --selftest
python3 skills/producing-tnr-art/scripts/artpreflight_selftest.py
python3 scripts/doctrinemap.py
python3 scripts/render_doctrine.py --check
python3 scripts/build_packs.py --check
python3 .github/scripts/pack_skills.py
# run twice and compare hashes/bytes

git diff --check
```

Also verify:

- `dist/producing-tnr-art.zip` stays below the existing 2 MiB guard;
- the committed reference bundle is outside `skills/` and therefore not packaged into the skill ZIP;
- no visual reference file bytes or selection metadata are silently changed by this task unless a separate approved reason is documented;
- no network is used by `generation_preflight.py`, `style_refs.py verify`, bundle or selftests;
- no TNR live requests or writes occur.

Because `skills/**` changes trigger packaging automation, wait for the branch automation to settle and hand off the final remote SHA including any generated-package commit.

## Scope / non-goals

Do not:

- implement a fake automatic ChatGPT image-attachment bridge the repository cannot actually provide;
- treat URL text or base64 as visual inspection;
- change the 18 approved reference source images merely to make the test pass;
- create a collage/contact sheet and pass it to the generator as a reference;
- rewrite the ratified house-style clauses or global prompt scaffold semantics without a separate user ruling;
- decide Road Bandit face, hair, armor/robe, mask, accent, weapon visibility or final direction for the user;
- modify One Perfect Crop prose/graph/combat content/admin values;
- run Forge or contact the live game;
- broaden this into a general ChatGPT product integration project.

## Suggested commit structure

Keep review surfaces separable:

1. workstream `session_gates` validation/render/init + tests, including the `SUPERSEDED` progress-count cleanup;
2. `generation_preflight.py` + socket-free tests;
3. deterministic reference hydration bundle command/artifact + tests;
4. art/ChatGPT/content-workstream workflow documentation;
5. One Perfect Crop pilot roadmap migration + generated projections;
6. rebuilt skill ZIP/generated outputs if automation does not commit them separately.

## Handoff

Use `docs/workflows/IMPLEMENTATION_HANDOFF.md` and freeze the exact final remote Fable SHA.

Include:

- repository/branch/base/frozen head;
- commits grouped by phases above;
- changed files;
- exact tests/gates/results;
- generated reference-bundle filename, byte size and SHA-256;
- final `producing-tnr-art.zip` byte size and deterministic hash evidence;
- sample `generation_preflight.py prepare` output for Road Bandit;
- sample `content_workstream.py init one_perfect_crop --task art.scene_characters` output proving ACTION GATED messaging;
- confirmation the 18 source reference bytes and selection metadata were unchanged unless explicitly authorized;
- confirmation no global art-spec semantic decision was made;
- any limitation that remains product/runtime-specific;
- explicit statement that no TNR API/live-game/Forge requests or writes occurred.

Do not merge to `main`. Freeze the implementation SHA for independent ChatGPT review.