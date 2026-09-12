# Forge Quest Studio foundation — implementation handoff

**Status:** FROZEN IMPLEMENTATION HANDOFF — INDEPENDENT REVIEW REQUIRED  
**Date:** 2026-09-12  
**Repository:** `perseverance484/tnr-tools`  
**Implementation branch:** `chatgpt/forge-quest-studio-foundation`  
**Implementation owner:** ChatGPT, explicitly assigned by the director for this slice  
**Independent reviewer:** Fable / another independent reviewer; ChatGPT must not self-approve this implementation  
**Approved design base:** `88680fb52e208747bb353ce1e37e7d33e3f41231`  
**Shared operational baseline inspected:** `main@305a28f992e33194fbba279a3f32e698dfb2b67f`  
**Fully verified implementation parent:** `bcb3a47e7c516b20f5a51c5aa195364d32eb6b73`  
**Live-game requests/writes:** none; prohibited throughout this implementation pass

## 1. Objective

Implement the first real repository-backed Quest Studio seam:

> Forge-authored Quest Source → approved repository operation → canonical repository compiler → structured build result → Forge-readable authoring/result surface.

Forge remains the human-facing translation/orchestration layer. The repository remains the durable authority for profiles, contracts, scripts, validators, provenance and generated artifacts. `Compile` is deliberately separate from any live-game mutation.

The governing implementation contract is `state/prompt_forge_quest_studio_foundation.md`. The director-approved parent product and authority boundary are in `docs/design/FORGE_NEXT_QUEST_STUDIO.md` and `docs/design/FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md`.

## 2. Intended scope completed

This slice implements:

1. a versioned Quest Source envelope for human-authored drafts;
2. a repository-owned quest subtype registry with maturity/adapter metadata;
3. canonical `quest_compile.py` orchestration;
4. a real Mission adapter that delegates to existing `mission.py`, mission profiles and repository validation rather than reimplementing mission policy in JavaScript;
5. a machine-readable `valid | blocked | failed` build-result envelope with provenance and `liveGameTouched:false`;
6. a hardened GitHub Actions worker for repository compilation;
7. Forge GitHub primitives for explicit branch-scoped Studio source writes, branch creation, workflow dispatch and result reads while preserving legacy `main` defaults for existing callers;
8. a Forge-side Quest Studio repository adapter with stale-result detection and generated-artifact confinement;
9. a first operator-facing Quest Studio shell with repository-backed subtype availability and Mission profiles;
10. a no-combat Mission authoring slice covering brief/prose, storyboard beats, local draft persistence, compile, canonical blockers/results, provenance and generated-manifest inspection;
11. adversarial and regression coverage for branch/path isolation, worker trust, multiline draft restoration, compile/live separation and generated-artifact path traversal;
12. reproducibly regenerated checked `forge_bundle.js` with parity verification.

## 3. Explicitly out of scope / not begun

This handoff does **not** claim completion of:

- the full Forge Next visual/shell/navigation redesign;
- Encounter / AI authoring or combat-Mission support in the Studio UI;
- Event, Story, Battle Pyramid, Raid/Boss or Daily compiler adapters;
- the full semantic quest graph editor / route playback experience;
- AI-assisted prose or content generation;
- Content Admin editing/review/publish architecture;
- Guide Studio or infographic/visual-communication implementation;
- Studio build-result promotion into the existing live Forge runner;
- automatic publication or any live-game operation;
- Builder retirement;
- game-source changes.

Unsupported quest recipes remain visible only as repository-declared future capabilities and are deliberately not presented as executable.

## 4. Important implementation files

### Repository worker / compiler

- `.github/workflows/quest_studio.yml`
- `.github/workflows/quest_studio_ci.yml`
- `skills/building-tnr-content/data/49_DATA_quest_studio_subtypes.json`
- `skills/building-tnr-content/scripts/quest_compile.py`
- `skills/building-tnr-content/scripts/quest_compile_integration_test.py`
- `skills/building-tnr-content/scripts/quest_worker_contract_test.py`

### Forge repository bridge / UI

- `forge/src/github.mjs`
- `forge/src/studio/repository.mjs`
- `forge/src/studio/ui.mjs`
- `forge/src/ui/dom.mjs`
- `forge/src/main.mjs`
- `forge/test/github.studio.test.mjs`
- `forge/test/quest.studio.ui.test.mjs`
- `forge_bundle.js`

### Governing records

- `state/prompt_forge_quest_studio_foundation.md`
- `docs/design/FORGE_NEXT_QUEST_STUDIO.md`
- `docs/design/FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md`
- `docs/design/FORGE_NEXT_UI_DESIGN_INPUT_INDEX.md`
- relevant Forge Next design/support documents already present on the branch
- `docs/RULINGS.md` entries preserving the director-set Quest Studio and repository-backed Studio direction

## 5. Safety / trust-boundary behavior

The repository worker:

- must be dispatched from `main`;
- checks out trusted compiler code separately from authored request content;
- accepts only `studio/quest/<requestId>` request branches;
- accepts only `studio/requests/<requestId>.quest.json` source paths;
- pins the exact request-source SHA;
- rejects unsafe request ids, mismatched branches/paths and symlinked Studio paths;
- executes the compiler only from the trusted tools checkout;
- keeps untrusted workflow inputs out of shell interpolation;
- persists only request-scoped result/build paths;
- contains no live-game URL or generic shell network path;
- records source/compiler provenance in the build result.

The Forge repository layer:

- leaves existing default `main` writes unchanged for legacy callers;
- requires Quest Studio to opt into an explicit request branch;
- dispatches the canonical worker on `main`;
- marks results from older source revisions stale rather than presenting them as current;
- refuses repository results that do not state `liveGameTouched:false`;
- confines generated-manifest reads to the exact request's `studio/builds/<requestId>/...` directory and rejects traversal segments/backslashes.

No new route bypasses the existing Forge live-operation authentication, journaling, reconciliation or read-back machinery because this slice does not connect compiled Studio output to that runner yet.

## 6. Verification evidence

The final clean read-only Quest Studio CI run against the fully verified implementation parent was:

- workflow run: `34723093835`
- job: `103632390318`
- conclusion: **success**
- token permission during the final gate: repository contents **read-only**

Exact gate results:

- static worker/compiler zero-live-network guard: **PASS**;
- `quest_worker_contract_test.py`: **PASS** — trusted compiler/request checkout separation, main-only dispatch, exact request identity, request code not executed, untrusted inputs out of shell interpolation, request-scoped persistence, no live-game path;
- `quest_compile.py --selftest`: **9 passed, 0 failed**;
- Mission adapter integration: **PASS** — current D Mission compiles through `mission.py` + canonical validation and preserves provenance/live-game boundary;
- Forge Node suite: **308 tests, 308 passed, 0 failed**;
- fixture regeneration + checked fixture diff: **PASS**;
- canonical Forge build: **PASS**, generated bundle approximately 427.2 KB;
- checked `forge_bundle.js` parity: **PASS**.

The generated bundle artifact from that run was `10306304235`.

The checked bundle was regenerated only through the canonical Forge build. A temporary branch-local write-enabled workflow was used solely to commit the exact generated bundle, then removed before this review target; the final verification workflow has `contents: read` only.

## 7. Important defects found and corrected during hardening

### Multiline draft restoration

The shared DOM helper assigned string form values as HTML attributes. That is insufficient for `<textarea>` state after a Studio rerender. It now assigns `value` as a DOM property. A regression test verifies multiline Mission description, success prose and storyboard beats survive repeated rendering.

### Generated-artifact path traversal

The initial `generatedManifest()` check only asserted a string prefix such as `studio/builds/<id>/`. A tampered result could therefore contain `studio/builds/<id>/../other/manifest.json`, pass the prefix check and rely on URL normalization to escape the request build directory.

The adapter now rejects traversal (`.` / `..`), empty segments and backslashes before reading generated artifacts. The regression verifies no repository read occurs for escaping paths.

## 8. Known debt / deviations

1. `npm ci` currently reports **3 high-severity dependency vulnerabilities**. The Quest Studio work did not alter or conceal them. They require a separate dependency audit because `npm audit fix --force` may be breaking and is outside this feature slice.
2. npm also reports install-script review warnings for `esbuild@0.28.2` and optional native package `msgpackr-extract@3.0.4`. These were not changed here.
3. Browser/live-session smoke testing was not performed. Tests are fixture/in-process/repository CI only.
4. The first authoring UI intentionally supports no-combat Missions only. Combat profiles are disabled until an Encounter/AI authoring surface exists; they are not silently downgraded.
5. Battle Pyramid, Story, Event, Raid/Boss and Daily are registry-visible but not executable. The UI reports adapter maturity honestly.
6. There is no reviewed promotion contract yet from a Studio request-branch manifest into the existing live runner. This is intentionally withheld rather than passing a mutable request-branch artifact directly into a runner whose existing resume/discovery assumptions were built around `main`.
7. Existing `mission.py --selftest` has a stale D-combat expectation relative to the current profile/headcount policy. This slice did not change mission balance/policy merely to make that old selftest green. The Quest Studio gate instead includes a current real Mission integration test through `mission.py` + `validate.py`.
8. Generated build results live on a mutable Studio request branch. They carry exact source/compiler provenance, but independent review should still attack tamper/staleness assumptions and whether promotion to later stages needs immutable adoption evidence.
9. Forge Next planning is concurrently owned by Fable on `claude/forge-next-planning-v3frzi`. This implementation did not modify `docs/forge_next/*` or Fable's branch.

## 9. Source / generated-data notes

This implementation does not introduce a new TNR game-source execution path. Canonical Mission compilation delegates to the existing repository-owned Mission profiles, `mission.py`, factories/art tooling and validator contracts. No game source was run and no live game was contacted.

The implementation branch includes a regenerated `dist/building-tnr-content.zip` because the repository's skillpack automation projects the changed content skill. Review the source tree as authority; the zip is generated output and should be checked for provenance/parity rather than hand-edited.

## 10. Independent review focus

The reviewer should attack at least:

1. branch/path/request-id injection in the workflow and browser bridge;
2. whether any request-branch-controlled code can execute in the trusted worker;
3. whether Studio sources or generated results can accidentally write to `main`;
4. whether workflow inputs can reach shell syntax unsafely;
5. symlink/path traversal and generated-artifact confinement;
6. stale/tampered build-result handling and exact source/compiler provenance;
7. `blocked` versus `failed` classification, especially unresolved director rulings versus compiler defects;
8. whether browser-side checks accidentally duplicate or override canonical Python Mission policy;
9. whether any compile/repository path can contact the live game or weaken existing live-runner auth/journal/reconciliation/read-back safety;
10. GitHub credential scope and whether the browser repository bridge has more privilege than this design actually needs;
11. reproducibility of `forge_bundle.js` and generated skill output;
12. the dependency-vulnerability warning noted above.

## 11. Browser / production verification not performed

Not performed:

- real browser Quest Studio smoke against GitHub credentials;
- actual `workflow_dispatch` from the Forge browser UI;
- request-branch compile initiated by a production operator device;
- any live-game request, read or write;
- Studio manifest execution by the Forge runner;
- publication behavior.

These remain deliberately outside this zero-live implementation handoff.

## 12. Review / correction loop

The SHA containing this handoff is the frozen review target. ChatGPT will not modify the branch while that exact SHA is under independent review.

If the reviewer returns confirmed findings, ChatGPT may apply accepted corrections on this ChatGPT-owned implementation branch only after the review target is released, rerun the affected/full gates, and provide a new exact SHA. Fable's planning branch remains separate throughout.
