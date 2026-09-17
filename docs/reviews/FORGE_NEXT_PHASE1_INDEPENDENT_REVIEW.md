# Forge Next Phase 1 — independent review

Status: **CHANGES REQUIRED — no integration clearance.**
Date: 2026-09-17
Repository: perseverance484/tnr-tools
Mode: PLAN_ONLY / independent review; no implementation or repository mutations.


The independent review returned five findings. The two priority checks both fail at the frozen target.

| ID | Severity | Finding |
| --- | --- | --- |
| FN1 | P1 / High | Legacy full-capture bodies can be omitted while the export reports success; old persistence failures can also become success. |
| FN2 | P1 / High | A changed journal declaration can override a snapshot's original projection and bypass field validation. |
| FN3 | P2 / Medium | Selecting an object or object array implicitly exports undeclared nested fields. |
| FN4 | P2 / Medium | Saved captures lack immutable source-pin / registry-policy provenance. |
| FN5 | P2 / Medium | A later-page 429 loses the walk's per-page evidence. |

Evidence: 26 frozen source/data copies verified by Git blob hash; 11 targeted offline checks, comprising eight defect demonstrations and three controls. The full product suite/build was not rerun. Existing executable-equivalent CI is green. Current non-content local-only restrictions held.

Next: return these findings to Fable for the bounded correction pass under the existing Phase 1 contract, followed by a new frozen SHA and independent re-review. No corrections were applied in this review. Phase 2 and Studio integration remain outside scope.

## Assignment and authority

The user requested a bounded Phase 1 independent review. The independent reviewer was assigned the exact frozen code target, with priority on legacy full captures and the immutable projection boundary. The coordinator independently checked repository refs, governing documents, existing CI, and the pinned source contracts. This report is review evidence and a correction handoff; it is not an approved contract for a later phase.

The governing build contract is [state/prompt_forge_next_phase1.md](https://github.com/perseverance484/tnr-tools/blob/8f15416d510eeb53aa82f7b8b09b7ce00accfa83/state/prompt_forge_next_phase1.md), including §§2.1, 6, 7, 9, and 12. Its blob `6bfaf7abb19270262a731598f39448e04d3a33f0` is identical at current main and the frozen target. Relevant durable rulings are RUL-2026-09-17-001 and RUL-2026-09-17-002. Review method follows CHATGPT.md, docs/DEVELOPMENT_WORKFLOW.md, docs/workflows/FABLE_REVIEW.md, and docs/agents/ENGINEERING_AUDITOR.md.

The two named uncommitted drafts, FORGE_NEXT_RECONCILIATION_AND_ROADMAP_DRAFT.md and CHATGPT_FORGE_NEXT_WORK_MODE_PROMPT.md, were not retrieved and were not treated as build contracts. The committed brief and frozen implementation handoff supplied the bounded review scope.

## Verified anchors

| Role | Exact SHA |
| --- | --- |
| Current main | `015583ba581388ed53770cb3a2ce7ad899cad6e3` |
| Accepted planning | `ba51a28a99a7748e61de0c2768bd73ab9c65c856` |
| Phase 1 base / merge-base | `77f02c30f7714eb8506ace8802904cb351a70d34` |
| Frozen code target | `8f15416d510eeb53aa82f7b8b09b7ce00accfa83` |
| Both implementation branch tips | `a8fc629d3d3f5632945042dd1a9164ac858c3d88` |
| Existing canonical CI head | `31559fe794f6e92c21d3a08c3d11ce0fd3d8a244` |
| Retained Studio source; excluded from review | `5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15` |
| Generated-contract / registry game-source pin | `345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9` |
| Current upstream game-source main | `1fd355ab92cec78148130e02c8d38834836c3181` |

Both `fable/forge-next-phase1` and `claude/forge-next-phase1-uwhcn1` were verified at the listed tip. The base-to-target comparison contains two commits and 27 changed files. The frozen target to branch-tip comparison changes only docs/handoffs/FORGE_NEXT_PHASE1_IMPLEMENTATION_HANDOFF.md. The frozen target to CI-head comparison likewise changes only that Markdown handoff.

Main's two commits above the base touch state/active-context.md, state/digest.json, state/status.json, and archive/state/digest_2026-09-08_pre_forge_closeout.json. These do not overlap the Phase 1 changed paths. This is a scope check, not integration approval or an executed merge check. Main's state snapshot still describes Phase 1 before implementation; the frozen implementation handoff provides the newer implementation evidence.

## Existing CI and pinned-source checks

[Canonical Forge CI run 35255548523](https://github.com/perseverance484/tnr-tools/actions/runs/35255548523), job `verify` / `105318155721`, completed successfully on `31559fe794f6e92c21d3a08c3d11ce0fd3d8a244`. Its tests, import and static boundaries, generated-fixture check, checked-bundle check, bundle-budget check, runtime dependency audit, and release-pin check all report success. No CI run was triggered in this review. The reported 381-test count comes from the author handoff; it is not a locally rerun full-suite count.

The coordinator read both new procedures at the exact declared source pin:

- [combat.ts:382](https://github.com/studie-tech/TheNinjaRPG/blob/345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9/app/src/server/api/routers/combat.ts#L382): getBattleEntries is a protected query with the declared input fields and limit/offset pagination. Source uses `input.limit ?? 30` and `input.offset ?? 0`.
- [combat.ts:530](https://github.com/studie-tech/TheNinjaRPG/blob/345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9/app/src/server/api/routers/combat.ts#L530): getBattleHistory is a protected, non-paginated query. Its attacker/defender joins include username, userId, and avatar. Source treats secondsBack as a truthy switch for a fixed three-hour cutoff; this review does not claim arbitrary-duration filtering.
- [trpc.ts:230](https://github.com/studie-tech/TheNinjaRPG/blob/345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9/app/src/server/api/trpc.ts#L230): protectedProcedure composes auth and sentry middleware without the rate limiter. Neither new procedure adds the rate limiter at its call site.
- The relevant combat source slices are byte-identical at the current upstream head. The BattleTypes declaration is also byte-identical; it moved from pinned line 539 to upstream line 608.

These checks support the new rows' source facts and local-only classification. They do not authorize additional projections or wider registry admission.

## Findings

### P1 / High — FN1: Phase 0 full-capture evidence silently disappears and previous failures become success

**Confirmed regression. Ordinary trigger:** upgrade Forge while the existing v1 local journal contains retained Phase 0 capture entries with `persist: "full"` and no `tier`.

Evidence at the frozen target:

- `forge/src/core/results.mjs:58` returns any no-tier capture immediately, without reading its immutable snapshot. `resolveCaptures` also only updates capture verdicts when `capture.tier` is present at lines 38–39.
- `forge/src/storage/journal.mjs:71–78` treats any successful read without `tier` as fully successful, regardless of `persistOk`. The mixed write/capture outcome has the same regression at line 91.
- The base runner actually generated this old shape: `forge/src/runner/runner.mjs:649` at `77f02c3` records `{persist:"full",snapshotKey,persistOk,persistError}`, with no tier. The journal remains version 1; `validateJobShape` has no capture migration.
- Fresh manifest alias parsing is not the same as restoring old journals. `normalizeCapture` maps a newly parsed full request to repo-safe, but does not modify already completed capture records.

Observed offline reproduction:

```text
legacy full: omittedBody=true, lookups=0, persistOk=true, outcome=success
legacy persistOk=false is classified success for both capture-only and verified-write jobs
```

A valid old snapshot containing the exact body was never read, the export omitted `data`, and both capture and bundle remained green. An old `persistOk:false` / quota-failed capture also received a successful outcome. No malicious edits are required.

**Refutation attempted:** newly parsing/running `persist:"full"` still works; its control passed. The defect survives because completed capture entries bypass parsing. The base materializer explicitly handled `capture.persist === "full"`, so this is new rather than inherited. Existing full-capture tests create fresh jobs under Phase 1 and therefore do not cover the upgrade shape.

**Contract:** brief §2.1 keeps existing approved full captures; objectives 4–5 and §6 require honest evidence and missing/persistence-failed bodies to remain non-success.

**Smallest correction:** centrally resolve a legacy full capture to its approved repo-safe semantics in restoration/materialization/outcome/UI predicates, with conservative snapshot/path validation for old records. Do not fix this by adding a blanket default to arbitrary unknown capture records. Keep snapshot-local tier restrictions authoritative. Export must recheck old snapshots without new game reads, and prior failures must remain failures.

**Regression coverage:** restore serialized base-era full captures and snapshots, including valid body, missing snapshot, oversized body, recorded storage failure, and mixed verified-write/capture jobs; assert exact body or explicit non-success, truthful counts, and zero rereads.

### P1 / High — FN2: A journal projection overrides the immutable capture declaration

**Confirmed export-boundary defect. Conditional trigger:** a stale or edited journal changes the projection fields for a previously retained projected snapshot.

Evidence:

- `forge/src/storage/captures.mjs:278–295` saves the original declaration beside the body; line 288 copies the projection.
- `forge/src/core/results.mjs:94` nevertheless prefers any nonempty `capture.projection` from the mutable journal over `rec.projection`.
- Lines 96–100 apply that replacement directly with `projectBody`, without calling `validateProjection`.
- The normal export path `forge/src/core/core.mjs:259–282` serializes this result for GitHub sync/export.

Observed reproduction: a snapshot with original `projection:["id"]` and raw `{id:"q1",secret:SECRET}` was materialized against the same capture whose journal says `projection:["secret"]`. It emitted `{secret:SECRET}`, `persistOk:true`, and bundle outcome `success`.

```text
snapshot projection=[id], journal projection=[secret], exported secret, outcome=success
edited journal bypasses field-path validation; exported projection object prototype was replaced
```

The second probe changed the journal field to `__proto__` against a synthetic body with that own property. Manifest parsing rejects that field, but materialization accepted it and replaced the result object's prototype. This demonstrates bypassed field validation; it does **not** demonstrate global `Object.prototype` pollution.

**Refutation attempted:** the narrower snapshot/journal *tier* comparison at line 78 works. The control confirms a local-only snapshot stays local-only despite a repo-safe journal tier. It does not constrain fields within the projected tier. Current combat and other non-content rows have no projection admission and remain local-only. These are projected-capture boundary violations on admitted content rows, not a demonstration that the currently admitted combat bodies export.

**Contract:** RUL-2026-09-17-001 and brief §2.1/§6 require explicitly declared validated paths with raw bodies remaining local; the user prioritized an immutable projection boundary against stale/edited journal state.

**Smallest correction:** bind export to the original validated snapshot declaration. Refuse missing/malformed/mismatched journal declarations (or permit only explicitly specified safe narrowing, without silently turning missing requested evidence green). Validate declaration syntax/policy at the leak boundary and return a non-success verdict for invalid declarations instead of throwing into an export fallback. Never use a journal declaration to widen/replace the retained one.

**Regression coverage:** change/replace/add journal projection paths, remove the declaration, insert malformed/prototype paths, widen the tier, and ensure the body does not export outside its retained declaration. Include the complete export/sync payload plus embedded journal and verify no automatic reread.

### P2 / Medium — FN3: Legal projected object paths implicitly export whole nested subtrees

**Confirmed contract violation. Ordinary trigger:** use an accepted projected manifest selecting an object-valued field, or an array of objects.

Evidence:

- `forge/src/research/registry.mjs:332–352` validates path spelling/admission but not a projected terminal's shape.
- `projectOne`, lines 381–385, assigns `r.value` directly at line 384. An object or array is passed through wholesale.
- `forge/test/research.tiers.test.mjs:145–169` currently codifies this behavior: selecting `content.objectives` exports each complete objective object.

The ordinary manifest `projection:["content"]` passes parsing. Given `content:{title:"Public",note:SECRET,nested:{hidden:SECRET}}`, both undeclared nested secret fields export with a green verdict. Selecting `content.objectives` likewise includes a newly added `unseen` field on each objective.

```text
projection=[content] admitted; undeclared content.note and content.nested.hidden exported intact
```

**Refutation attempted:** selecting a parent path could ordinarily be defined as selecting a whole subtree, and the tests clearly expect that interpretation. The governing ruling explicitly disallows **implicit nested passthrough**, so that interpretation is unavailable here. Selecting scalar dotted leaves works without this issue. The currently projectable rows are repo-safe content rows; the finding is a violated per-capture narrowing contract, not evidence of a current combat-data export.

**Smallest correction:** make unsupported structured terminal values an explicit projection failure. Support any nested/object-array projection only by enumerating and validating its permitted leaf fields; do not add an implicit subtree/wildcard escape hatch. A narrowly scoped scalar/nested-scalar implementation with honest unsupported-shape failures is sufficient; no new generic projection language is needed for this correction.

**Regression coverage:** object leaves, arrays containing objects, newly introduced response fields inside a selected parent, missing/invalid leaves, and ordinary scalar/nested-scalar success. The existing objective-array test must cease blessing implicit raw nested passthrough.

### P2 / Medium — FN4: Captures do not retain the source/registry identity used for admission

**Confirmed contract mismatch. Ordinary trigger:** create/export any new research capture and later inspect it independently of the running bundle.

Evidence:

- `forge/src/runner/runner.mjs:637–646,674–710` records request/tier/projection/page/persistence metadata, but no source pin or registry-policy identity.
- The actual snapshot record built by `forge/src/storage/captures.mjs:278–294` has the same omission.
- `REGISTRY_PIN` exists at `forge/src/research/registry.mjs:54` but is not consumed by capture persistence.
- `forge/src/core/results.mjs:109–119` exports these records without adding their capture-time policy provenance.
- `forge/src/main.mjs:25` only identifies the product as `forge 0.4.1`; it does not bind this individual capture to an exact registry revision. Materializing old jobs under a later build must not fabricate their original policy identity.

The probe exercised actual `_captures`, `_persist`, and `CaptureCache.putSnapshot` with a synthetic successful local-only result. Journal and snapshot contained ordinary metadata, but neither source pin nor a source/registry/contract provenance identity.

```text
actual _captures/_persist/putSnapshot output has no source pin or registry revision
```

**Refutation attempted:** registry documentation and the static pin gate correctly identify the current source audit. That does not retain which registry/source contract governed an individual old capture. The existing provenance test only compares the current module constant with generated JSON, not persisted capture evidence.

**Contract:** brief §6 explicitly requires every research capture to retain registry/source provenance sufficient to identify its audited contract.

**Smallest correction:** stamp the source pin and explicit immutable registry/policy revision (or equivalent content identity) when the capture is created; retain/propagate it in snapshot, journal and exported evidence. Do not stamp old records with the current revision as if it were their original one.

**Regression coverage:** exact current-capture provenance in journal/snapshot/export; older records lacking provenance represented honestly; later policy/build changes do not relabel earlier evidence.

### P2 / Medium — FN5: A later rate-limited page erases the walk's per-page evidence

**Confirmed evidence-loss defect. Conditional ordinary trigger:** page 1 succeeds, then page 2 returns 429.

Evidence:

- `forge/src/budget/reader.mjs:108–112` invokes `budget.observe`, which can throw before returning the failed page.
- `query` awaits that call at line 148, before appending its per-page record at line 150; prior page metadata only exists in local variables.
- `forge/src/runner/runner.mjs:623–648` writes any capture/page journal evidence only after the whole query returns.
- The existing pause path at lines 262/324 saves path/until, not the page history.
- `forge/test/research.paging.test.mjs:177–189` tests a rate limit on the first page and explicitly expects no finished capture, so it does not verify retained evidence for a partially completed walk.

The probe sent an in-process successful first page and a 429 second page. The thrown `RateLimited` carried no pages. Neither `capturesAfter` nor `capturesAfterPartial` existed; the successful page's query-cache row is mutable and is not durable per-capture evidence.

```text
page1 ok and page2 429 were sent, but no capture/page record survives in journal or thrown error
```

**Refutation attempted:** the job does pause and is not falsely classified complete; this safety behavior holds. An ordinary non-429 error returned by the reader also retains its pages. The defect is the missing required per-page evidence at the exceptional 429 seam, not a false-success claim. The parent catch preserves a pause reason only. A later retry using `fresh:true` can replace the earlier mutable cache response, so that cache is not a substitute for occurrence evidence.

**Contract:** brief §7.8 requires partial, failed or rate-limited pages to retain honest per-page evidence and never become complete-success evidence.

**Smallest correction:** preserve per-page metadata, including the unsuccessful page, at the point of pause; retain the existing rate-limit stop and non-success semantics. A bounded error payload or per-page journaling seam is sufficient; do not redesign mutation recovery. Make any resumed attempt explicitly distinct or safely continue from retained evidence, without silently rewriting the earlier partial attempt.

**Regression coverage:** a 429 on page 2 or later, exported paused evidence, repeated/resumed attempts, and zero further calls after the limit. Assert exact inputs and observed per-page verdicts survive; incomplete bodies cannot become whole-answer success.

## What held in this bounded review

- Fresh `persist:"full"` requests normalize to repo-safe and can materialize the exact content body.
- The snapshot's local-only tier cannot be widened by changing only the journal tier.
- Canonically equivalent input orders reuse the intended query cache entry; a different page input has a distinct entry.
- An unapproved query path is refused before the injected client sends anything.
- The coordinator separately verified pinned/current game-source facts for the two added combat rows, their no-limiter protected query classification, and no relevant current-source drift.
- The coordinator separately verified successful existing CI run `35255548523` on documentation-only descendant `31559fe794f6e92c21d3a08c3d11ce0fd3d8a244`. This independent review did not rerun that CI or infer the untested upgrade/projection cases from its success.

No finding asserts that new non-content local-only bodies currently escape. No finding asserts live exploitation, game mutation, global prototype pollution, or a full-suite failure.

## Reproduction and limitations

Scratch harness:
`/workspace/scratch/b0ede89cfb43/review-work/probe-phase1.mjs`

Frozen source/data copies:
`/workspace/scratch/b0ede89cfb43/review-work/target/`

Expected Git object identities:
`/workspace/scratch/b0ede89cfb43/review-work/target-blobs.json`

Command actually run:

```sh
node --test /workspace/scratch/b0ede89cfb43/review-work/probe-phase1.mjs
```

Final result on Node v24.19.0:

```text
Verified 26 target copies against frozen Git blob SHA-1s
tests 11
pass 11
fail 0
```

These were **11 targeted checks: eight asserting reproduced defects and three controls**, not 11 product regression tests proving the product passes. The harness verifies every target copy's Git blob SHA before import. It uses only synthetic data, memory-backed stores and an injected client. An initial attempt stopped at import because `superjson` was unavailable. No dependencies were installed: the final harness uses a Node loader replacement for that unused imported codec which throws if serialization/deserialization is attempted. No codec method or real transport was used. All actual reviewed source files stayed byte-identical to their frozen blobs.

No full repository test suite, build/bundle regeneration, fixture regeneration, dependency audit or full static-gate rerun was performed independently. Existing test code and gate changes were read. No real-browser/real-IDB, userscript, authentication/session, clipboard integration or live network behavior was exercised. The privacy reproductions demonstrate the central export materializer/bundle path and the unchanged export/sync call chain was inspected; no external GitHub write was issued.

## Narrow next step

Fable receives these findings only after this review returns, corrects the bounded Phase 1 surfaces and adds the specified regressions, then supplies a new frozen SHA and fresh canonical CI evidence. Re-review the correction diff, capture upgrade/export/projection/provenance behavior and the exceptional paging seam; broaden only if corrections change other assumptions. Do not integrate `8f15416`; do not begin Phase 2 or Studio integration.

## Portable reproduction appendix

The following harness and Git-blob manifest make the review probes reproducible without relying on this session’s temporary files. In an isolated review directory, save the harness as `probe-phase1.mjs` and the JSON manifest as `target-blobs.json`. Put the listed repository files from frozen commit `8f15416d510eeb53aa82f7b8b09b7ce00accfa83` under the sibling `target/` directory, preserving their repository-relative paths. Use Node v24.19.0 (the version actually used here) and run `node --test probe-phase1.mjs`. These assertions describe the defective frozen behavior; after a correction they must be replaced with regression expectations for the desired behavior.

### Harness

```javascript
import assert from 'node:assert/strict';
import { test } from 'node:test';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { registerHooks } from 'node:module';

// No live transport is constructed. Deny accidental network calls before importing target code.
globalThis.fetch = () => { throw new Error('NETWORK_FORBIDDEN_IN_REVIEW'); };
// The target imports superjson through the unused transport module. No packages are installed.
// Refuse every codec call, so only the independent storage/reader paths can be exercised.
registerHooks({
  resolve(specifier, context, nextResolve) {
    return specifier === 'superjson' ? { url: 'review:unused-superjson', shortCircuit: true } : nextResolve(specifier, context);
  },
  load(url, context, nextLoad) {
    return url === 'review:unused-superjson' ? { format: 'module', shortCircuit: true,
      source: 'const unused=()=>{throw new Error("SUPERJSON_NOT_USED_BY_REVIEW")}; export default {serialize:unused,deserialize:unused};' } : nextLoad(url, context);
  },
});
const root = new URL('./target/', import.meta.url);
const blobs = JSON.parse(readFileSync(new URL('./target-blobs.json', import.meta.url), 'utf8'));
for (const row of blobs) {
  const data = readFileSync(new URL(row.path, root));
  const actual = createHash('sha1').update(Buffer.from(`blob ${data.length}\0`)).update(data).digest('hex');
  assert.equal(actual, row.sha, `target copy differs: ${row.path}`);
}
console.log(`Verified ${blobs.length} target copies against frozen Git blob SHA-1s`);

const { materialize, resolveCaptures, buildBundle } = await import('./target/forge/src/core/results.mjs');
const { parseManifest } = await import('./target/forge/src/runner/manifest.mjs');
const { projectBody, REGISTRY_PIN } = await import('./target/forge/src/research/registry.mjs');
const { CaptureCache } = await import('./target/forge/src/storage/captures.mjs');
const { jobOutcome } = await import('./target/forge/src/storage/journal.mjs');
const { Runner } = await import('./target/forge/src/runner/runner.mjs');
const { CachedReader } = await import('./target/forge/src/budget/reader.mjs');
const { RateLimited } = await import('./target/forge/src/budget/bucket.mjs');

const SECRET = 'SYNTHETIC-REVIEW-SECRET-7ea4';
const stamp = '2026-09-17T00:00:00.000Z';
function cap(patch = {}) {
  return { phase: 'after', proc: 'quests.get', input: { id: 'q1' }, ok: true, rows: 1,
    error: null, persist: 'projected', tier: 'projected', projection: ['id'],
    snapshotKey: 'review::after::0', persistOk: true, persistError: null, ...patch };
}
function snap(patch = {}) {
  return { key: 'review::after::0', jobId: 'review', phase: 'after', ordinal: 0,
    path: 'quests.get', input: { id: 'q1' }, tier: 'projected', projection: ['id'],
    at: stamp, data: { id: 'q1', content: { note: SECRET }, secret: SECRET }, ...patch };
}
function journalOf(capture) {
  const job = { jobId: 'review', state: 'DONE', items: [], capturesAfter: [capture] };
  return { job, patches: [], get: () => job,
    annotateJob(id, patch) { this.patches.push(patch); Object.assign(job, patch); } };
}
const build = (job, captures) => buildBundle({ version: 'synthetic-review', now: () => 0,
  storage: { getItem: () => null } }, job, captures);

test('CONTROL: newly parsed persist full is still a repo-safe alias', async () => {
  const c = parseManifest({ capture: { after: [{ proc: 'quests.get', input: { id: 'q1' }, persist: 'full' }] } }).capture.after[0];
  assert.equal(c.tier, 'repo-safe');
  const body = { id: 'q1', name: 'Synthetic' };
  const actual = await materialize({ getSnapshot: async () => snap({ tier: 'repo-safe', projection: null, data: body }) }, cap({ ...c }));
  assert.deepEqual(actual.data, body);
});

test('DEFECT legacy: Phase 0 full snapshot is never looked up and body silently omitted', async () => {
  const capture = cap({ persist: 'full' }); delete capture.tier; delete capture.projection;
  const journal = journalOf(capture); let lookups = 0;
  const legacySnapshot = snap({ data: { id: 'q1', name: 'Exact prior body' } });
  delete legacySnapshot.tier; delete legacySnapshot.projection;
  const captures = await resolveCaptures({ journal, cache: { getSnapshot: async () => { lookups++; return legacySnapshot; } } }, 'review');
  const bundle = build(journal.job, captures);
  assert.equal(lookups, 0);
  assert.equal('data' in bundle.captures[0], false);
  assert.equal(bundle.captures[0].persistOk, true);
  assert.equal(bundle.outcome, 'success');
  assert.equal(journal.patches.length, 0);
  console.log('legacy full: omittedBody=true, lookups=0, persistOk=true, outcome=success');
});

test('DEFECT legacy: previously failed persistence is upgraded to successful outcome', async () => {
  const capture = cap({ persist: 'full', persistOk: false, persistError: 'storage quota refused' });
  delete capture.tier; delete capture.projection;
  assert.equal(jobOutcome(journalOf(capture).job), 'success');
  assert.equal(jobOutcome({ state: 'DONE', items: [{ state: 'VERIFIED' }], capturesAfter: [capture] }), 'success');
  console.log('legacy persistOk=false is classified success for both capture-only and verified-write jobs');
});

test('CONTROL: snapshot local-only ceiling survives a wider journal tier', async () => {
  const actual = await materialize({ getSnapshot: async () => snap({ tier: 'local-only', projection: null }) }, cap({ tier: 'repo-safe' }));
  assert.equal(actual.tier, 'local-only');
  assert.equal('data' in actual, false);
  assert.equal(JSON.stringify(actual).includes(SECRET), false);
});

test('DEFECT projection: edited journal overrides immutable projection and exports undeclared secret', async () => {
  const journal = journalOf(cap({ projection: ['secret'] }));
  const captures = await resolveCaptures({ journal, cache: { getSnapshot: async () => snap() } }, 'review');
  const bundle = build(journal.job, captures);
  assert.deepEqual(bundle.captures[0].data, { secret: SECRET });
  assert.equal(bundle.outcome, 'success');
  assert.deepEqual(bundle.captures[0].projection, ['secret']);
  assert.deepEqual(snap().projection, ['id']);
  console.log('snapshot projection=[id], journal projection=[secret], exported secret, outcome=success');
});

test('DEFECT projection: export trusts prototype path that manifest validation rejects', async () => {
  assert.throws(() => parseManifest({ capture: { after: [{ proc: 'quests.get', input: { id: 'q1' }, persist: 'projected', projection: ['__proto__'] }] } }), /refused/);
  const body = JSON.parse('{"id":"q1","__proto__":{"polluted":"SYNTHETIC"}}');
  const actual = await materialize({ getSnapshot: async () => snap({ data: body }) }, cap({ projection: ['__proto__'] }));
  assert.equal(actual.persistOk, true);
  assert.equal(Object.getPrototypeOf(actual.data).polluted, 'SYNTHETIC');
  console.log('edited journal bypasses field-path validation; exported projection object prototype was replaced');
});

test('DEFECT projection: ordinary legal object path passes all nested raw fields through', async () => {
  const normalized = parseManifest({ capture: { after: [{ proc: 'quests.get', input: { id: 'q1' }, persist: 'projected', projection: ['content'] }] } }).capture.after[0];
  const body = { id: 'q1', content: { title: 'Public', note: SECRET, nested: { hidden: SECRET } } };
  const result = projectBody(body, normalized.projection);
  assert.equal(result.ok, true);
  assert.equal(result.data.content, body.content);
  assert.equal(JSON.stringify(result.data).includes(SECRET), true);
  const actual = await materialize({ getSnapshot: async () => snap({ projection: ['content'], data: body }) }, cap({ projection: normalized.projection }));
  assert.equal(actual.persistOk, true);
  assert.equal(actual.data.content.nested.hidden, SECRET);
  console.log('projection=[content] admitted; undeclared content.note and content.nested.hidden exported intact');
});

test('DEFECT projection: ordinary array-object path passes new nested fields through', () => {
  const normalized = parseManifest({ capture: { after: [{ proc: 'quests.get', input: { id: 'q1' }, persist: 'projected', projection: ['content.objectives'] }] } }).capture.after[0];
  const body = { content: { objectives: [{ id: 'n1', unseen: SECRET }] } };
  const result = projectBody(body, normalized.projection);
  assert.equal(result.ok, true);
  assert.equal(result.data.content.objectives[0].unseen, SECRET);
});

function memoryCache() {
  const stores = new Map();
  const cache = new CaptureCache({ open() { throw new Error('real IDB not used'); } }, () => 0);
  cache._tx = async (mode, fn, name = 'captures') => {
    if (!stores.has(name)) stores.set(name, new Map());
    const map = stores.get(name);
    const req = (result) => { const r = { result: structuredClone(result) }; queueMicrotask(() => r.onsuccess()); return r; };
    return fn({ put(record) { map.set(record.key, structuredClone(record)); return req(record.key); }, get(key) { return req(map.get(key)); } });
  };
  return cache;
}

test('DEFECT provenance: successful research journal and snapshot omit registry/source pin', async () => {
  const c = parseManifest({ capture: { after: [{ proc: 'combat.getBattleEntries', input: { battleId: 'b1' }, persist: 'local-only' }] } }).capture.after[0];
  const cache = memoryCache();
  const journal = journalOf(null); delete journal.job.capturesAfter;
  const reader = { query: async () => ({ ok: true, complete: true, rowCount: 1,
    data: [{ id: 'a1' }], pages: [{ n: 0, input: c.input, ok: true, rows: 1 }] }) };
  const host = { journal, reader, cache, _requireAuth() {}, _persist: Runner.prototype._persist };
  await Runner.prototype._captures.call(host, 'review', [c], 'after');
  const record = await cache.getSnapshot('review::after::0');
  const text = JSON.stringify({ job: journal.job, record });
  assert.equal(text.includes(REGISTRY_PIN), false);
  assert.equal(/source|registry|contract|provenance/i.test(text), false);
  assert.equal(record.tier, 'local-only');
  console.log('actual _captures/_persist/putSnapshot output has no source pin or registry revision');
});

test('DEFECT paging: page-2 429 loses page-1 and failure per-page evidence', async () => {
  const path = 'combat.getBattleEntries'; const sent = [];
  const client = { batch: async (calls) => { sent.push(calls[0].input); return sent.length === 1
    ? [{ ok: true, data: [{ id: 'a1' }, { id: 'a2' }] }]
    : [{ ok: false, error: { code: 'TOO_MANY_REQUESTS', httpStatus: 429 } }]; } };
  const cache = memoryCache();
  const budget = { acquire: async () => {}, observe(results) { if (!results[0].ok) throw new RateLimited({ path, until: 1 }); } };
  const reader = new CachedReader({ client, cache, budget });
  const c = parseManifest({ capture: { after: [{ proc: path, input: { battleId: 'b1', limit: 2 }, pages: 3, persist: 'local-only' }] } }).capture.after[0];
  const journal = journalOf(null); delete journal.job.capturesAfter;
  const host = { journal, reader, cache, _requireAuth() {}, _persist: Runner.prototype._persist };
  let caught;
  try { await Runner.prototype._captures.call(host, 'review', [c], 'after'); } catch (e) { caught = e; }
  assert.ok(caught instanceof RateLimited);
  assert.equal(sent.length, 2);
  assert.equal(journal.job.capturesAfter, undefined);
  assert.equal(journal.job.capturesAfterPartial, undefined);
  assert.equal(caught.pages, undefined);
  console.log('page1 ok and page2 429 were sent, but no capture/page record survives in journal or thrown error');
});

test('CONTROL: distinct filters/page inputs use distinct cache entries and unknown path is refused', async () => {
  let calls = 0;
  const reader = new CachedReader({ cache: memoryCache(), client: { batch: async () => { calls++; return [{ ok: true, data: [] }]; } }, budget: { acquire: async () => {}, observe() {} } });
  await reader.query('combat.getBattleEntries', { battleId: 'b1', limit: 2 });
  await reader.query('combat.getBattleEntries', { limit: 2, battleId: 'b1' });
  assert.equal(calls, 1);
  await reader.query('combat.getBattleEntries', { battleId: 'b1', limit: 2, offset: 2 });
  assert.equal(calls, 2);
  await assert.rejects(() => reader.query('combat.getGraph', {}), /not in the audited/);
  assert.equal(calls, 2);
});
```

### Frozen Git blob manifest

```json
[{"path":"32b_DATA_pool.json","sha":"419a0d17eb2c0a3429f69e28db8f236ed4996f45","size":18166},{"path":"forge/src/budget/bucket.mjs","sha":"dcacab4b183cc7a02194830a6136a42dce030c9d","size":10006},{"path":"forge/src/budget/reader.mjs","sha":"14593ee112213cd98885e6bebf6eff12943921ed","size":9453},{"path":"forge/src/core/facts.mjs","sha":"78220c4033e8298a0252c4b1b9ce5ea881df2dcc","size":6568},{"path":"forge/src/core/results.mjs","sha":"8226124912382286bf5fd6f3dd4084f6681fefdd","size":7306},{"path":"forge/src/github.mjs","sha":"6f3394d230fc3a2eb33bc3c27f83fd8006acfd79","size":4563},{"path":"forge/src/research/registry.mjs","sha":"9757483f2e4b8d844ddda05c3ce8133f01afa81c","size":24626},{"path":"forge/src/runner/fields.json","sha":"278e076f5141bfad112eb6dd0f95a04fa7df8ddd","size":10349},{"path":"forge/src/runner/lints.mjs","sha":"33be48b8dd149c7f0d581fd18209c843d8a939cb","size":8629},{"path":"forge/src/runner/manifest.mjs","sha":"4c34a6458c854cae80a8b34f41a20a1e6b0950c2","size":17187},{"path":"forge/src/runner/nested.json","sha":"40d1793e4be47896bc1fd5e501f817e38824e1c6","size":96267},{"path":"forge/src/runner/pool.mjs","sha":"09ba9a5536f1d597933e883128210c4255c8f93e","size":6658},{"path":"forge/src/runner/recipes.mjs","sha":"7be3c1e6ea5b5bbcff80321d486fd69adf15444e","size":6150},{"path":"forge/src/runner/refs.mjs","sha":"c3cd6f1cb9511e46d2466f45ba584ae0a3936a96","size":2461},{"path":"forge/src/runner/runner.mjs","sha":"eca11ac6b95d9f5965daaff92a9e17fc62cc30fb","size":48097},{"path":"forge/src/runner/validate.mjs","sha":"6b007fa3d4981c30b10196b49e41d132fa78eda9","size":15989},{"path":"forge/src/storage/captures.mjs","sha":"7def0896d89f6ba0025f516d26f2ee1ce5d5a002","size":15594},{"path":"forge/src/storage/compat.mjs","sha":"9ec81e3a655927e2a638275f532bfd88f335bd4c","size":1137},{"path":"forge/src/storage/hash.mjs","sha":"c1bfa7b90abd97c338794e80e15c991d89743d11","size":1202},{"path":"forge/src/storage/journal.mjs","sha":"ee58135db868c6cfcaa31f26cd823465e374d6ae","size":21145},{"path":"forge/src/transport/auth.mjs","sha":"a6c90c78a77f6deb8e64d8e1f1975d47475ceeec","size":11693},{"path":"forge/src/transport/client.mjs","sha":"252318f7dd4771df9dc10aac7339f63b7968eb04","size":6422},{"path":"forge/src/transport/envelope.mjs","sha":"cef404088bfdf96ad649977d34646e0860d8dc9b","size":7588},{"path":"forge/src/transport/outcome.mjs","sha":"1bfc01f3cadeedf42262e6973b2984f14d0e78c1","size":3820},{"path":"forge/src/transport/procedures.mjs","sha":"62e6b6332834ba01b1b4f1e4fe3c6268f5744b38","size":7763},{"path":"forge/src/transport/session.mjs","sha":"7cd9fc64bd20369692cb384ffc8bc54fce6387af","size":2740}]
```
