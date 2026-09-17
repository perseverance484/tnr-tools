# Forge Next Phase 1 — research capture tiers and audited research registry

**Status:** DRAFT — blocked only on director rulings K-06 and K-17. Do not implement from this draft until both rulings are settled and this file is frozen as READY.

**Repository:** `perseverance484/tnr-tools`  
**Draft base:** `b0bae3bcd6e3d9cf76de48237892ac099fa7a60c`  
**Phase 0 integrated implementation:** `3130f9433810cca4f8eca78b80aeb4dc8eb7ddb0`  
**Accepted planning source:** `claude/forge-next-planning-reconciled@ba51a28a99a7748e61de0c2768bd73ab9c65c856`  
**Accepted Quest Studio reference:** `chatgpt/forge-quest-studio-foundation@5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15` — reference only; do not merge in Phase 1.  
**Current Forge generated-contract pin:** `345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9`  
**Current upstream game-source head observed while drafting:** `studie-tech/TheNinjaRPG@1fd355ab92cec78148130e02c8d38834836c3181` — reverify at implementation start.

---

## 1. Objective

Make Forge a safe, bounded research/evidence tool for approved paged and non-content reads without turning the UI into an ad-hoc API client and without allowing arbitrary raw game data to leak into the public repository.

At Phase 1 completion:

1. captures carry an explicit persistence tier;
2. approved non-content research procedures are enumerated in a reviewed registry rather than inferred from endpoint existence;
3. paged/filtered reads bind cache identity and provenance to the exact input actually sent;
4. exported evidence distinguishes repo-safe full bodies, local-only full bodies, and selected-field projections according to the director-approved policy;
5. missing/oversize/unpersistable data is represented honestly as non-success evidence rather than silently downgraded or omitted;
6. no screen constructs transport calls or reads raw capture storage directly;
7. no background polling is introduced;
8. Phase 0 execution, recovery, auth, rate-budget, bundle, import-direction, and live-safety invariants remain green.

This is a capability/evidence phase. It is not the visual-shell redesign.

---

## 2. Director decisions required before freeze

### K-06 — capture persistence tiers

**Question:** Which capture classes may persist to the public repository?

**Planning recommendation:** adopt three tiers:

- **`repo-safe`** — an explicitly audited class whose exact body may be included in repository evidence;
- **`local-only`** — the exact body may be retained in local IndexedDB for operator/research use, but the raw body must never enter a repository result, clipboard/export payload, public diagnostic dump, or GitHub commit;
- **`projected`** — raw body remains local; repository evidence may contain only an explicitly declared allowlist of selected fields plus provenance/verdict metadata.

Recommended policy if approved:

- existing audited content-record point reads currently allowed for full persistence remain `repo-safe` unless separately reclassified;
- newly approved non-content research reads default to `local-only`;
- `projected` exports are fail-closed field projections: no wildcard, no implicit nested passthrough, and no fallback to a full body when projection fails;
- tier widening requires a deliberate reviewed registry/policy change.

### K-17 — approved research-read registry

**Question:** Which non-content procedures may Forge read for research/parity?

**Planning recommendation:** add only procedures that a committed, reviewed research manifest actually needs. Do not create a broad catalog merely because endpoints exist.

Every approved row must record at least:

- procedure path;
- query/mutation kind — Phase 1 research registry is reads only;
- auth requirement;
- limiter status;
- exact input/pagination contract relevant to Forge;
- default capture tier;
- source pin/provenance used to audit the row.

Recommended default if approved: non-content research rows are `local-only` unless K-06 explicitly grants a broader class.

**Implementation remains blocked until the director rules both K-06 and K-17.**

---

## 3. Scope

### In scope

- capture-tier model and validation;
- tier-aware capture materialization and result shaping;
- explicit audited research-read registry;
- bounded filtered/paged query support required by approved research manifests;
- cache identity derived from canonical exact request input;
- exact provenance of sent input, path, capture tier and timestamp;
- honest capture/parity verdicts;
- tests, fixtures, checked bundle, static gates and canonical Forge CI updates required by the capability;
- minimal core/action/UI plumbing required to expose the capability without redesigning the shell.

### Explicitly out of scope

- Quest Studio integration;
- Phase 2 visual shell/design system;
- Phase 3 manifest UX/recovery redesign;
- Content Admin;
- Publish;
- Project Workspace;
- Builder retirement;
- broad endpoint discovery or generic API explorer;
- background polling/watchers;
- adopting upstream game-source drift merely because it exists;
- any live-game request or write during implementation or review.

---

## 4. Architecture and trust boundaries

### 4.1 Core remains the orchestration boundary

Research/capture workflow state belongs behind ForgeCore actions/facts. Screens may render state and invoke actions; they may not construct tRPC requests, call `fetch`, bypass the audited reader/client, or query IndexedDB directly for raw research data.

The Phase 0 core API/state golden remains a ratchet. Any required Phase 1 widening must be explicit and reviewed.

### 4.2 Source facts and persistence policy stay distinct

`forge/src/transport/procedures.mjs` continues to own audited transport facts such as kind/auth/limiter status.

Do not silently turn those source facts into product/privacy policy. If a separate research/capture policy registry is useful, it may reference approved procedure rows and assign default tier/projection metadata. Its provenance and purpose must be explicit.

### 4.3 Registry grows only by evidence-backed need

An endpoint does not become approved because it is useful or discoverable. A Phase 1 row exists only when an approved committed research manifest requires it and its source contract has been audited.

Unknown/unapproved non-content paths fail closed before any request.

### 4.4 No background polling

Phase 1 reads occur only from explicit operator/research actions represented in the work package/manifest. No interval polling, hidden refresh loop, subscription emulation, or continuous watcher is allowed.

---

## 5. Capture-tier contract

The final enum/naming follows the director ruling, but if K-06 adopts the recommendation the required semantics are:

### `repo-safe`

- exact body may be materialized into repository/export evidence;
- current full-capture byte ceiling remains enforced;
- missing snapshot, failed read, oversize body, or storage failure remains explicit non-success evidence;
- never re-read merely to make an export greener.

### `local-only`

- exact body may be stored locally in the dedicated capture storage path;
- exported/repository evidence contains provenance and verdict metadata, not the body;
- no clipboard/export helper, result bundle, GitHub sync path, diagnostic dump or error object may accidentally serialize the raw body;
- inability to retain the local body is reported honestly.

### `projected`

- raw body may remain local;
- public/repository output includes only declared field paths;
- projection field paths are explicit and validated before the request where possible;
- no wildcard (`*`), arbitrary spread, implicit object copy, or nested fallback;
- absent requested fields are represented as projection failure/drift according to the final result contract, never replaced by the full record.

### Provenance required for every tier

Repository/local evidence must preserve enough information to reconstruct what was asked and what policy applied, including:

- procedure path;
- exact canonical input sent;
- capture tier;
- projection declaration when applicable;
- capture occurrence identity / job identity;
- read timestamp;
- persistence verdict/error;
- source/registry provenance necessary to identify the approved procedure contract.

---

## 6. Filtered and paged read contract

The current reader list cache uses a generic list identity and is not sufficient for arbitrary filters/pages. Phase 1 must make list/query caching input-aware.

Required properties:

1. two list reads with different inputs can never alias in cache;
2. equivalent canonical inputs may share a cache key only when their serialized transport meaning is equivalent;
3. capture/journal provenance records the exact input that the transport sends;
4. the input used for cache identity, provenance and transport must derive from one canonical representation rather than three independently rebuilt objects;
5. paging must not silently duplicate or skip data because a helper reused an earlier page's cache entry;
6. bounded page limits must be explicit; no unbounded crawl;
7. rate-budget acquisition/observation continues through the existing audited budget/client path;
8. partial/rate-limited/error pages retain honest per-page evidence and do not fabricate completeness.

If the game procedure uses cursor, offset, page number, limit, filter, search, or compound input, implement only the audited shape needed by approved manifests. Do not invent a generic pagination abstraction that obscures procedure-specific contracts.

---

## 7. Source/version discipline

Phase 1 does not silently refresh Forge's generated/source pin.

At implementation start:

1. reverify `main` and current upstream `studie-tech/TheNinjaRPG` head;
2. preserve the existing Forge declared pin unless a separately reviewed adoption task changes it;
3. audit every additive research procedure at the declared pin and inspect current upstream for relevant drift;
4. record file/line/source evidence for kind, auth, limiter and required input/result/pagination facts;
5. if current upstream materially changes one of those facts, stop and split a pin-refresh/adoption task rather than blending source versions inside Phase 1.

Generated contracts remain generated evidence; do not hand-edit around a source disagreement.

---

## 8. Allowed implementation surface

Phase 1 is an approved capability phase, so the generic planning shorthand that an execution-core seam should be empty does **not** mean these required lower-layer edits are forbidden. The allowed change surface is narrow and explicit:

- `forge/src/transport/procedures.mjs` — additive audited procedure facts only;
- `forge/src/budget/reader.mjs` — input-aware filtered/paged query support;
- `forge/src/storage/captures.mjs` — capture tier/provenance storage primitives where required;
- `forge/src/runner/manifest.mjs` — capture grammar for tier/projection/paging declarations where required;
- `forge/src/runner/runner.mjs` — bounded capture execution and verdict shaping only;
- `forge/src/core/**` — research/capture orchestration/action/fact surface where required;
- `forge/src/ui/**` — minimal plumbing only; no visual redesign;
- `forge/tools/**`, `forge/test/**`, fixtures, `forge_bundle.js`, and canonical Forge CI as required;
- concise policy/registry documentation or generated descriptors as required by provenance.

No unrelated execution-core redesign is authorized. Keep lower-layer edits focused and separately reviewable.

Do not modify Quest Studio code in this phase.

---

## 9. Acceptance tests and adversarial cases

Start from the integrated Phase 0 baseline: canonical Forge CI is green with 343/343 tests at Phase 0 completion.

Phase 1 must add evidence for at least:

### Registry / source facts

- every new research path is explicitly approved by the registry;
- an unapproved non-content path is refused before transport;
- every added transport row has pinned tests/evidence for kind, auth and limiter status;
- no mutation is admitted to the research-read registry.

### Cache/paging

- two list/filter/page calls with different inputs produce distinct cache entries;
- identical canonical inputs reuse only the intended cached result;
- exact journal/capture input equals exact sent transport input;
- second-page requests cannot be satisfied by first-page cache identity;
- a 429 or partial page cannot be reported as a complete research capture;
- configured bounds prevent an accidental unbounded crawl.

### Tier behavior

If K-06 adopts the recommended three tiers:

- `repo-safe`: exact body round-trips into evidence when allowed;
- `local-only`: raw body is retained locally but absent from every export/repository path;
- `projected`: only the declared fields are exported, including nested-path tests;
- local-only/projected raw bodies cannot leak through errors, debug metadata, clipboard/export, bundle journal, or GitHub sync;
- missing snapshot/storage failure remains explicit non-success;
- over-cap raw body remains explicit non-success and is never truncated into a green result;
- changing a tier to a broader persistence class requires a registry/policy edit that tests can see.

### Existing safety nets

- all Phase 0 state/recovery/auth/reconcile/budget tests remain green;
- core API/state golden remains explicit;
- import-direction and static network boundaries remain zero violations;
- no new source reaches a live host outside the existing transport boundary;
- envelope fixtures remain reproducible;
- screen fixtures remain byte-identical unless the director separately approves an intentional Phase 1 operator-visible change;
- checked `forge_bundle.js` is reproducible;
- runtime dependency audit remains green;
- release pin remains clean.

---

## 10. Bundle budget

Phase 0 finished at approximately:

- raw: `417,370 / 430,000` bytes (97.1%);
- deterministic gzip: `79,294 / 81,000` bytes (97.9%).

Phase 1 will probably exhaust the existing gzip headroom. Do not weaken or delete the budget gate to make the feature fit.

If a raise is required:

- measure the feature delta first;
- put the budget change in a separate focused commit;
- justify the new ceiling from the measured Phase 1 product, not a round number chosen in advance;
- keep a tight ratchet above the measured result;
- report old/new raw and gzip measurements in the handoff.

This is an engineering control, not a director product decision, unless the change creates a material operator/distribution consequence.

---

## 11. Live-game boundary

Phase 1 implementation and independent review are **ZERO LIVE REQUESTS / ZERO LIVE WRITES**.

Use:

- pinned/public game source;
- repository fixtures;
- committed captures/results;
- fake/in-process transport;
- local IndexedDB substitutes;
- static gates.

Do not test a research endpoint against production merely to prove the registry works.

---

## 12. Completion / handoff contract

After K-06 and K-17 are ruled and this brief is frozen, Fable implements from a fresh branch based on the then-current `main`.

At completion Fable returns an exact-SHA handoff containing at minimum:

- repository;
- implementation branch;
- exact base and merge-base;
- frozen head;
- changed surfaces;
- source/game pin inspected and current upstream head inspected;
- exact research registry additions and their evidence;
- final capture-tier policy implemented;
- pagination/cache-key contract implemented;
- test counts and commands;
- fixture/build/bundle reproducibility;
- raw/gzip before/after and any budget-ratchet commit;
- canonical Forge CI run/job;
- known debt and intentionally unsupported research shapes;
- browser checks not performed;
- live requests: none;
- live writes: none;
- what explicitly has not begun.

ChatGPT independently reviews the frozen SHA before integration.

Do not begin Phase 2 automatically after implementation. Phase 1 closes only after reviewed integration to `main` and green canonical CI.

---

## 13. Freeze gate

This draft may become **READY / FROZEN** only after:

1. director ruling K-06 is recorded durably;
2. director ruling K-17 is recorded durably;
3. this brief is updated to replace conditional/recommended tier language with the ruled policy;
4. `main` is reverified and recorded as the implementation base target;
5. any accepted Forge planning references required for future phases are preserved without merging stale operational snapshots.
