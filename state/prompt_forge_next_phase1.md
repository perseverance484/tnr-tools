# Forge Next Phase 1 — research capture tiers and audited research registry

**Status:** READY / FROZEN LANE-A IMPLEMENTATION CONTRACT  
**Date:** 2026-09-17  
**Repository:** `perseverance484/tnr-tools`  
**Implementation owner:** Fable / Claude Code  
**Independent reviewer:** ChatGPT  
**Suggested implementation branch:** `fable/forge-next-phase1`  
**Draft/freeze base:** `b0bae3bcd6e3d9cf76de48237892ac099fa7a60c`  
**Phase 0 integrated implementation:** `3130f9433810cca4f8eca78b80aeb4dc8eb7ddb0`  
**Accepted planning source:** `claude/forge-next-planning-reconciled@ba51a28a99a7748e61de0c2768bd73ab9c65c856`  
**Accepted Quest Studio reference:** `chatgpt/forge-quest-studio-foundation@5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15` — reference only; do not merge in Phase 1  
**Current Forge generated-contract pin:** `345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9`  
**Upstream game-source head observed at freeze:** `studie-tech/TheNinjaRPG@1fd355ab92cec78148130e02c8d38834836c3181` — reverify at implementation start  
**Live-game policy:** ZERO LIVE REQUESTS / ZERO LIVE WRITES

This brief is the Phase 1 implementation contract. The director decisions that previously blocked it are now settled by `RUL-2026-09-17-001` and `RUL-2026-09-17-002`.

---

## 1. Objective

Make Forge a safe, bounded research/evidence tool for approved paged and non-content reads without turning the UI into an ad-hoc API client and without allowing arbitrary raw game data to leak into the public repository.

At Phase 1 completion:

1. captures carry an explicit persistence tier;
2. approved non-content research procedures are enumerated in a reviewed registry rather than inferred from endpoint existence;
3. paged/filtered reads bind cache identity and provenance to the exact canonical input actually sent;
4. exported evidence distinguishes repo-safe full bodies, local-only full bodies, and selected-field projections;
5. missing, oversize, failed or unpersistable data is represented honestly as non-success evidence rather than silently downgraded, truncated or omitted;
6. no screen constructs transport calls or reads raw capture storage directly;
7. no background polling or generic API browsing is introduced;
8. Phase 0 execution, recovery, auth, rate-budget, bundle, import-direction and live-safety invariants remain green.

This is a capability/evidence phase, not the visual-shell redesign.

---

## 2. Director-set policy

### 2.1 Capture persistence tiers — ruled

`RUL-2026-09-17-001` fixes these three classes:

#### `repo-safe`

- exact response body may enter repository/export evidence only for explicitly audited classes approved for that treatment;
- current audited content-record point reads already allowed for full persistence remain repo-safe unless separately reclassified;
- existing byte ceilings and honest failure semantics remain enforced;
- a missing snapshot, failed read, oversize body or persistence failure is never converted into a green result.

#### `local-only`

- exact body may be retained in local IndexedDB for operator/research use;
- raw body must not enter repository results, GitHub commits, clipboard/export payloads, public diagnostic dumps, error serialization, or another public-repository path;
- newly approved non-content research reads default to this tier;
- failure to retain the local body is visible as a persistence failure, not silently ignored.

#### `projected`

- raw body remains local;
- repository/export evidence may contain only explicitly declared, validated field paths plus provenance/verdict metadata;
- no wildcard, arbitrary object spread, implicit nested passthrough, or full-body fallback is allowed;
- absent/invalid projected paths produce projection failure/drift evidence rather than substituting the full body.

Tier widening requires a deliberate reviewed policy/registry edit.

### 2.2 Research-read registry — ruled

`RUL-2026-09-17-002` fixes a demand-driven, fail-closed registry:

- add a non-content procedure only when a committed, reviewed research manifest/work package actually needs it;
- Phase 1 research rows are queries only;
- no generic endpoint explorer;
- do not bulk-enable all public queries;
- unknown/unapproved non-content paths fail before transport;
- each row records procedure path, kind, auth class, limiter status, exact relevant input/pagination contract, default persistence tier and source-pin/provenance;
- non-content rows default to `local-only` unless separately approved otherwise.

These policies are settled. Do not re-ask K-06 or K-17.

---

## 3. Mandatory task start

Before implementation:

1. verify live `main` and record the exact base SHA;
2. read `state/active-context.md`, `state/status.json`, `docs/00_INDEX.md`, `docs/RULINGS.md`, `CLAUDE.md`, `CHATGPT.md`, `docs/DEVELOPMENT_WORKFLOW.md`, `docs/agents/README.md`, `docs/workflows/IMPLEMENTATION_HANDOFF.md`, and this brief;
3. read the selectively consolidated Forge Next planning sources under `docs/forge_next/` and the relevant Forge implementation/tests from integrated Phase 0;
4. verify `studie-tech/TheNinjaRPG` current `main` and compare the specific research procedures you intend to add against Forge's declared generated-contract pin;
5. do not silently adopt a new game-source pin or regenerated contract inside this task.

If current upstream materially changes a procedure fact required by this phase, split a source-pin/adoption task rather than blending source versions.

---

## 4. Scope

### In scope

- capture-tier model and validation;
- tier-aware capture materialization and result shaping;
- explicit audited research-read registry;
- bounded filtered/paged query support required by approved research manifests;
- exact request-input canonicalization used consistently for cache identity, transport and provenance;
- local-only and projected persistence safeguards;
- exact source/registry provenance;
- honest capture/parity verdicts;
- minimal ForgeCore/action/UI plumbing needed to expose the capability without redesigning the shell;
- tests, fixtures, checked bundle, static gates and canonical Forge CI changes required by the capability.

### Explicitly out of scope

- Quest Studio integration;
- Phase 2 visual shell/design system;
- Phase 3 manifest UX/recovery redesign;
- Content Admin;
- Publish;
- Project Workspace;
- Builder retirement;
- broad endpoint discovery;
- generic API explorer;
- background polling/watchers;
- automatic game-source pin movement;
- live-game requests or writes.

---

## 5. Architecture and trust boundaries

### 5.1 ForgeCore remains the orchestration boundary

Research/capture workflow state belongs behind ForgeCore actions/facts. Screens may render state and invoke actions; they may not:

- construct raw tRPC requests;
- call `fetch` directly;
- bypass the audited reader/client/budget path;
- query IndexedDB directly for raw research data.

The Phase 0 core API/state golden remains a ratchet. Any widening required by Phase 1 must be explicit, tested and reviewed.

### 5.2 Source facts and persistence policy remain separate

`forge/src/transport/procedures.mjs` owns source-derived transport facts such as procedure kind, auth and limiter status.

The research/persistence registry owns product/privacy admission and default tier. Do not infer repo-safety from `publicProcedure`, lack of auth, endpoint naming, or source discoverability.

### 5.3 Evidence-backed admission only

A research row exists only when a committed/reviewed work package needs it and the procedure contract has been audited at the declared pin.

No mutation may be admitted to the Phase 1 research registry.

### 5.4 No hidden background activity

Reads occur only from explicit operator/research actions represented in the manifest/work package. No interval polling, continuous watcher, subscription emulation or hidden refresh loop.

---

## 6. Capture contract

Every research capture must retain enough provenance to reconstruct the request and policy decision:

- procedure path;
- exact canonical input sent;
- capture tier;
- projection declaration when applicable;
- job/capture occurrence identity;
- timestamp;
- persistence verdict/error;
- registry/source provenance sufficient to identify the audited contract.

### Repository/export safety

The implementation must prove that local-only/projected raw bodies cannot leak through:

- result bundles;
- journal/result serialization;
- GitHub sync;
- clipboard/export helpers;
- debug/error objects;
- UI diagnostic payloads;
- projection fallback paths.

No re-read is allowed merely to make an export greener after an earlier capture/persistence failure.

---

## 7. Filtered and paged read contract

The current generic list-cache identity is insufficient for arbitrary filters/pages. Phase 1 makes query/list caching input-aware.

Required properties:

1. two reads with different transport inputs never alias in cache;
2. equivalent canonical inputs may reuse a cache entry only when their serialized transport meaning is equivalent;
3. the input used for cache identity, provenance and transport derives from one canonical representation;
4. exact stored provenance equals exact input sent;
5. second-page requests cannot be satisfied by first-page cache identity;
6. bounds are explicit; no unbounded crawl;
7. budget acquire/observe remains on the existing audited path;
8. partial, failed or rate-limited pages retain honest per-page evidence and may not be reported as complete;
9. implement only audited procedure-specific cursor/offset/filter/search shapes required by approved manifests — do not create a generic abstraction that hides procedure-specific contracts.

---

## 8. Allowed implementation surface

This phase may make focused, reviewable changes in:

- `forge/src/transport/procedures.mjs` — additive audited procedure facts only;
- `forge/src/budget/reader.mjs` — input-aware filtered/paged query support;
- `forge/src/storage/captures.mjs` — tier/provenance storage primitives as required;
- `forge/src/runner/manifest.mjs` — capture grammar for tier/projection/paging declarations;
- `forge/src/runner/runner.mjs` — bounded capture execution and verdict shaping only;
- `forge/src/core/**` — research/capture orchestration/action/fact surface;
- `forge/src/ui/**` — minimal plumbing only, no visual redesign;
- `forge/tools/**`, `forge/test/**`, fixtures, `forge_bundle.js`, canonical Forge CI;
- concise registry/policy documentation or generated descriptors needed for provenance.

No unrelated execution-core, auth, transport, reconciliation, journal or release-loader redesign is authorized.

Do not modify Quest Studio implementation in this phase.

---

## 9. Required tests and adversarial cases

Start from integrated Phase 0: canonical Forge CI completed with 343/343 tests, 12 byte-identical screen fixtures, zero import/static-boundary violations, raw bundle 417,370 bytes and deterministic gzip 79,294 bytes.

Phase 1 must add evidence for at least:

### Registry/source facts

- every new research path is explicitly present in the approved registry;
- an unapproved non-content path is refused before transport;
- every added transport row has evidence/tests for query kind, auth and limiter status;
- no mutation can enter the research registry;
- registry provenance names the source pin used for audit.

### Cache/paging

- different filter/page inputs produce distinct cache identities;
- identical canonical inputs reuse only the intended cached result;
- exact capture/journal input equals exact sent transport input;
- page 2 cannot reuse page 1;
- 429/partial/error page cannot become a complete-success result;
- configured limits prevent unbounded crawl.

### Persistence tiers

- `repo-safe`: exact body round-trips into evidence only when the path/class is approved;
- `local-only`: raw body is locally retained but absent from every repository/export path;
- `projected`: only declared fields export, including nested-path tests;
- no local-only/projected raw-body leak through errors/debug/clipboard/bundle/GitHub sync;
- missing snapshot/storage failure is explicit non-success;
- oversize body is explicit non-success and never truncates to green;
- widening persistence class requires a registry/policy change visible to tests;
- wildcard/implicit projection is rejected.

### Existing Phase 0 safety nets

- all journal/recovery/auth/reconcile/budget suites remain green;
- core API/state golden remains explicit;
- import-direction and static network boundaries remain zero violations;
- no new live-host path outside the existing reviewed transport boundary;
- envelope fixtures remain reproducible;
- 12 screen fixtures remain byte-identical unless a separately approved operator-visible change is made;
- checked `forge_bundle.js` remains reproducible;
- runtime dependency audit remains green;
- release pin remains clean.

Do not weaken a Phase 0 gate to make Phase 1 fit.

---

## 10. Bundle budget

Phase 0 completed at:

- raw `417,370 / 430,000` bytes (97.1%);
- deterministic gzip `79,294 / 81,000` bytes (97.9%).

Phase 1 may exhaust the remaining headroom. Do not silently raise or delete the gate.

If a raise is required:

1. measure the feature delta first;
2. put the budget change in a separate focused commit;
3. justify the new ceiling from the measured product, not a round number chosen in advance;
4. keep a tight ratchet above the measured result;
5. report before/after raw and gzip measurements and the budget-ratchet commit SHA.

This is an engineering control unless it creates a material product/distribution consequence.

---

## 11. Source/version discipline

At implementation start:

- reverify live `main`;
- reverify current upstream game-source head;
- preserve Forge's declared generated-contract pin unless a separately reviewed adoption task changes it;
- audit every added research procedure at the declared pin;
- inspect current upstream for relevant drift;
- record source evidence for kind, auth, limiter and exact input/pagination facts;
- stop and split source adoption if current upstream materially disagrees with the declared-pin contract needed by this task.

Generated contracts remain generated evidence. Do not hand-edit around a disagreement.

---

## 12. Live-game boundary

Implementation and independent review are **ZERO LIVE REQUESTS / ZERO LIVE WRITES**.

Use pinned/public source, repository fixtures, committed captures/results, fake/in-process transport, local IndexedDB substitutes and static gates.

Do not contact production merely to prove a research endpoint or pagination path.

---

## 13. Quest Studio carry-forward only

Quest Studio remains accepted at:

`chatgpt/forge-quest-studio-foundation@5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15`

Do not merge it into Phase 1.

Preserve for later Phase S:

- source-push build model;
- Contents-write-only browser credential;
- no Actions write;
- no Workflows write;
- trusted-main compiler boundary;
- exact source revision;
- `generated.manifestSha256` binding;
- request-scoped persistence;
- stale-result refusal;
- zero-live compiler boundary.

The final Studio review's N1–N4 follow-ups remain Phase-S/integration work, not Phase 1 scope.

---

## 14. Completion / handoff

When implementation is complete, Fable freezes the exact SHA and returns a compact handoff containing:

- Repository
- Branch
- Base
- Merge-base
- Frozen Head
- Changed surfaces
- Research registry additions and source evidence
- Final tier policy implementation
- Pagination/cache-key contract
- Test counts and commands
- Fixture status
- Bundle/build reproducibility
- Raw/gzip before/after and any budget-ratchet commit
- Canonical Forge CI run/job
- Game-source pin inspected and current upstream head inspected
- Known debt / unsupported shapes
- Browser checks not performed
- Live requests: none
- Live writes: none
- What explicitly has not begun

ChatGPT independently reviews the frozen SHA before integration.

Do not begin Phase 2 automatically. Phase 1 closes only after reviewed integration to fresh `main` and green canonical CI.

---

## 15. Freeze statement

K-06 and K-17 are settled by `RUL-2026-09-17-001` and `RUL-2026-09-17-002`. The accepted planning sources needed for future phases are selectively consolidated under `docs/forge_next/` and `docs/design/` without merging stale operational state. This brief is therefore **READY / FROZEN** for Fable implementation from a newly verified `main`.