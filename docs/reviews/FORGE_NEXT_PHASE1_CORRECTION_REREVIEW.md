# Forge Next Phase 1 — correction re-review

**Verdict: CHANGES REQUIRED. No integration clearance for `7bd8592f1d579f33d71c0713cfee4529cd691526`.**
Date: 2026-09-17.
Mode: bounded independent re-review of corrections to FN1–FN5; no implementation.

The two prior P1 findings are closed in this bounded re-review. The original rate-limit evidence-loss finding is also closed. Two correction areas still require work: a new overlapping-path regression in FN3 and incomplete provenance in FN4.

| Original finding | Re-review disposition |
| --- | --- |
| FN1 — legacy full captures | **Closed.** Base-era captures materialize their exact bodies, prior failures remain non-success, and verdict/headline handling agrees. |
| FN2 — mutable projection declaration | **Closed.** An intact retained snapshot controls exported fields; journal replacement/addition cannot redirect it. |
| FN3 — implicit nested passthrough | **Original leak closed; new P2 regression remains.** A terminal projection can hide a deeper requested path sharing its prefix. |
| FN4 — source/registry provenance | **Partially corrected; P2 work remains.** Persisted captures carry policy metadata, but registry identity omits meaningful policy content and summary/abandoned captures remain unstamped. |
| FN5 — later-page 429 evidence loss | **Closed.** Per-page verdicts survive pauses, repeated attempts and a later successful retry without exporting raw bodies. |

The review is against `7bd8592f1d579f33d71c0713cfee4529cd691526`, not the newer documentation-only branch tips. Current non-content local-only bodies remained withheld in the controls. No finding below asserts a live-game leak or mutation.

## Confirmed new regression: FN3-R1 / P2 — overlapping paths silently skip a requested deeper field

**Ordinary trigger:** an otherwise legal projected manifest declares both a scalar/list field and a descendant of that field, for example `projection:["id","id.deeper"]`, against a response `{id:"q1"}`.

**Exact source evidence at the correction target:**

- `forge/src/research/registry.mjs:333–353` accepts the two paths independently; it does not reject a prefix overlap.
- `projectInto` groups paths by first segment, separates terminal and deeper paths at lines 388–389, then lines **390–395** return from the terminal branch without checking the deeper group.
- A scalar or scalar-list terminal reaches `continue` at lines **391–392**, so the absent deeper declaration never enters the missing set.
- `forge/src/runner/runner.mjs:712–733` uses that projection verdict while retaining the body; `forge/src/core/results.mjs:139–145` revalidates the names but applies the same projector again and returns a green export.

**Reproduction performed:** the harness passes real manifest parsing, actual `Runner._persist`, actual `CaptureCache.putSnapshot` with a memory-backed transaction seam, and actual `resolveCaptures/buildBundle`. All three cases produced a successful capture and exported bundle:

```text
fields=["id","id.deeper"]
projectOk=true persistOk=true outcome=success exported={"id":"q1"}

fields=["tags","tags.deeper"]
projectOk=true persistOk=true outcome=success exported={"tags":["a"]}

fields=["content.objectives.id","content.objectives.id.deeper"]
projectOk=true persistOk=true outcome=success
exported={"content":{"objectives":[{"id":"n1"}]}}
```

The requested `*.deeper` field was missing in every case. The error is **false projection success / silently omitted requested evidence**, not undeclared-field leakage.

**Refutation attempts:**

1. Both paths pass the actual manifest parser, so this is not a call that bypasses declaration validation.
2. The old frozen projector at `8f15416` returned `ok:false` for each same input. The harness checked the old registry and its dependency against their Git blob hashes before this comparison. The behavior is introduced by the correction's grouped traversal.
3. The runtime persistence and export checks both use the same shortcut; later materialization does not catch it.
4. A selected object parent still correctly fails as a structured terminal. The counterexample instead uses a scalar or scalar list, precisely where the new shortcut takes its early `continue`.
5. Existing correction coverage tests `["id.deeper"]` alone, which fails correctly. It does not combine the deeper request with `"id"`, where the failure disappears.

**Contract:** Phase 1 brief §2.1/§6 requires absent or invalid declared projection paths to yield non-success evidence. A successful projection may not quietly omit a declared field.

**Smallest correction:** reject prefix-overlapping paths during declaration validation (including the leak-boundary revalidation), or make grouped traversal record every unsatisfied deeper path even when a terminal is selected. Either approach must preserve a non-success verdict; do not silently remove the deeper path.

**Regression coverage:** scalar and scalar-list overlaps; overlaps inside object arrays; both declaration orders; manifest validation plus persistence/export outcomes. Keep the now-correct ordinary nested leaf, array shape, structured-terminal refusal and no-undeclared-fields controls.

Minimal reproduction in an exact checkout with dependencies available:

```js
import { parseManifest } from "./forge/src/runner/manifest.mjs";
import { projectBody } from "./forge/src/research/registry.mjs";
const c = parseManifest({ capture: { after: [{
  proc: "quests.get", input: { id: "q1" },
  persist: "projected", projection: ["id", "id.deeper"]
}] } }).capture.after[0];
console.log(projectBody({ id: "q1" }, c.projection));
// Actual at 7bd8592: {ok:true,data:{id:"q1"}}
// Required: rejected declaration or non-success naming id.deeper.
```

## Closure evidence for the original findings

### FN1

Correction source: `storage/captures.mjs:84–93` centralizes the narrow `persist:"full"` legacy mapping. `core/results.mjs:65–107` performs snapshot materialization with old-path checks and retained-tier narrowing. `storage/journal.mjs:74–96` uses the same mapping for capture and mixed-job outcomes. `core/facts.mjs:85–89` includes legacy captures in the full-body headline; corresponding UI predicates use `captureTier`.

Independent checks restored the actual no-tier Phase 0 capture/snapshot shape and observed one snapshot lookup, exact exported body, compact journal update, correct full-body count and successful outcome. Missing and oversized snapshots yielded failed capture-only jobs; a recorded quota failure was preserved without attempting another snapshot lookup; mixed verified-write jobs with that failed capture stayed unverified. Unknown persistence labels were not given blanket repo-safe semantics. A snapshot marked local-only remained local-only even when the legacy journal asked for full persistence.

**Limit:** memory-backed restored shapes were used; no real browser/IndexedDB migration was exercised.

### FN2

Correction source: `core/results.mjs:118–145` reads the retained projection, rejects differing claimed field arrays, revalidates the retained declaration using `rec.path`, and applies only those retained fields.

Independent checks replaced the mutable journal's `["id"]` with `["secret"]`, added fields, supplied an empty array, forbidden/wildcard field names and a nonstring array entry. Those attempts returned no projected body. A wider journal tier did not bypass a projected snapshot. Invalid/missing retained declarations were withheld as verdicts in the exercised cases.

A null, absent or non-array journal copy currently falls back to the intact retained declaration. That does **not** redirect or widen the export; the independent check still received only `{id:"q1"}`. The handoff's phrase “all seven redirections withheld” should not be read as “all seven returned persistOk:false”: null is a safe retained-authority fallback. This difference is not a blocker.

**Limit:** the original threat model changes the journal while retaining an intact snapshot. Arbitrarily rewriting both the supposedly immutable snapshot body/declaration and journal is a different trust boundary; no claim of security against that is made. This review does not claim every conceivable malformed JavaScript object is handled or any global prototype-pollution exploit exists.

### FN3 original subtree leak

Correction source: `research/registry.mjs:357–399` limits terminals to scalars/scalar lists and walks explicitly declared descendants through arrays. New structured-terminal failures propagate through persistence/export.

Independent checks confirmed `content`, nested objects and object-array terminals no longer export raw subtrees. Explicit leaves across several object-array levels preserved order and shape while excluding all synthetic undeclared fields. Empty arrays remained valid empty evidence. A missing leaf, scalar/null element, or object-valued terminal in any array member caused whole-projection failure without a partial exported object.

**Remaining limitation:** these successful controls do not refute FN3-R1's overlapping-path false-success counterexample above.

## Remaining correction area: FN4 provenance

### FN4-R1 — P2: different admission policies receive the same registry identity

**Confirmed contract mismatch.** [registry.mjs:451](https://github.com/perseverance484/tnr-tools/blob/7bd8592f1d579f33d71c0713cfee4529cd691526/forge/src/research/registry.mjs#L451) derives `REGISTRY_REVISION` from each row's input **key names** at line 457. It omits the actual input specifications, including types and enum members. It also omits the global `MAX_PAGES` bound and tier-order definition.

The reviewer loaded isolated in-memory variants of the exact correction module and tested behavior and identity together:

| Synthetic policy change | Observed behavior | Registry revision |
| --- | --- | --- |
| `secondsBack: NUM` → `BOOL` | Numeric input is refused; boolean input is admitted. | Unchanged: `35d2269b` |
| Remove `opponents` from the `userFilter` enum | A previously admitted filter is refused. | Unchanged: `35d2269b` |
| `MAX_PAGES = 20` → `19` | The exported global page ceiling changes. | Unchanged: `35d2269b` |

These are deliberate sensitivity probes, with the on-disk reviewed files left unchanged. The identity input itself excludes the changed facts; the result is reproducible without searching for a hash collision.

**Consequence:** a saved policy stamp cannot distinguish these different admission contracts. The correction's claim that input-contract and paging-bound edits necessarily change the revision does not hold.

**Refutation:** pin, row tier, project allowlist, and per-row paging descriptors do participate in the current identity. New persisted captures do carry that identity. Those improvements do not identify changes to omitted contract content. The added “content identity” test in research.review.test.mjs checks an eight-hex-digit shape and shared identity between rows; it does not mutate a relevant policy value and require an identity change.

**Smallest correction:** derive the revision from complete canonical input specifications and all policy bounds/defaults/orderings that determine admission. Include field types, enum members, applicable constraints, and the global page ceiling. Keep creation-time stamping and do not relabel old captures with a new revision.

**Regression expectations:** independently change a field type, enum membership and global paging bound; each changed contract must produce a different identity. Equivalent canonical policy data must remain stable.

### FN4-R2 — P2: summary captures and abandoned attempts still lack policy provenance

**Confirmed ordinary-path omission.** [runner.mjs:656](https://github.com/perseverance484/tnr-tools/blob/7bd8592f1d579f33d71c0713cfee4529cd691526/forge/src/runner/runner.mjs#L656) calls `_persist` only when `c.tier` is present; `capturePolicy` is called inside `_persist` at line 688. A normal research capture with `persist: "summary"` bypasses it. The new [`_journalAttempt` record at line 744](https://github.com/perseverance484/tnr-tools/blob/7bd8592f1d579f33d71c0713cfee4529cd691526/forge/src/runner/runner.mjs#L744) also has no policy stamp. [resolveCaptures](https://github.com/perseverance484/tnr-tools/blob/7bd8592f1d579f33d71c0713cfee4529cd691526/forge/src/core/results.mjs#L48) exports abandoned records as recorded.

Actual runner/storage/export-path probes confirmed:

```text
successful summary research capture still omits policy in journal/export
abandoned research attempt exported without source/registry identity
```

**Consequence:** these research records cannot identify the registry/source policy that admitted them. Brief §6 requires provenance for every research capture, independently of whether a raw body is retained.

**Refutation:** a completed local-only capture now stamps journal and snapshot correctly, and export carries the stamp. Authentic old captures stay unstamped instead of receiving fabricated provenance; both controls passed. The remaining omissions are newly created summary captures and abandoned attempts, not the intentionally unstamped legacy records.

**Smallest correction:** stamp the admitted policy when creating every new research capture/attempt record, before splitting into summary, persisted, or abandoned paths. Keep the same capture-time identity with any snapshot. Preserve honest absence for old records and never backfill their identity from current policy during export.

**Regression expectations:** new summary, successful persisted, failed/abandoned and resumed research evidence carries the correct creation-time identity through journal/export; legacy no-stamp records remain explicitly without one.

## FN5 confirmation and interpretation of attempts

The reviewer exercised a successful first page followed by a decoded 429 on page 2, repeated that interrupted attempt, then allowed a successful retry. Both abandoned attempts retained exact inputs and page verdicts; the completed-capture cursor stayed untouched during the failures. Export included the abandoned entries with `abandoned: true`, `complete: false` and `persistOk: false`. Synthetic raw response bodies and the raw server error message did not enter the bundle.

A later successful job may correctly have an overall `success` outcome while retaining separately marked abandoned attempts. That accurately distinguishes the eventual completed result from its earlier interrupted history. No mutation-recovery redesign is required. The missing policy stamps on attempts are covered under FN4-R2.

## Verified repository and CI anchors

| Role | Exact SHA |
| --- | --- |
| Previous reviewed code | `8f15416d510eeb53aa82f7b8b09b7ce00accfa83` |
| New correction target | `7bd8592f1d579f33d71c0713cfee4529cd691526` |
| Correction commit parent | `a8fc629d3d3f5632945042dd1a9164ac858c3d88` |
| Base / merge-base with current main | `77f02c30f7714eb8506ace8802904cb351a70d34` |
| Current main | `015583ba581388ed53770cb3a2ce7ad899cad6e3` |
| Both current implementation branch tips | `963aa6d6af54df8fdb217124fcbdd4d07e569412` |
| Successful canonical CI head | `f34e5f889cdb51556e2b89626944c4eb355027d0` |

Both `fable/forge-next-phase1` and `claude/forge-next-phase1-uwhcn1` were verified at the listed tip. The correction target to either current tip or the CI head differs only in the two Markdown files: the correction handoff and original independent review. The committed original review matches the previously returned report, allowing for final newline normalization.

There is one correction commit after the two prior documentation commits above `8f15416`. Its source/support changes comprise 14 files under `forge/`, plus the rebuilt root bundle; the full `8f15416`→`7bd8592` comparison also contains the earlier implementation handoff. This scope accounting does not indicate an unrelated implementation change.

[Canonical Forge CI run 35263303607](https://github.com/perseverance484/tnr-tools/actions/runs/35263303607), job `verify` / `105344127640`, is completed-success. Its test, import/static-boundary, fixture, checked-bundle, budget, runtime-audit and release-pin steps all report success. No CI run was triggered by this re-review. The author's reported 394-test count and raw/gzip measurements were not independently rerun locally.

The governing [state/prompt_forge_next_phase1.md](https://github.com/perseverance484/tnr-tools/blob/7bd8592f1d579f33d71c0713cfee4529cd691526/state/prompt_forge_next_phase1.md) is unchanged, blob `6bfaf7abb19270262a731598f39448e04d3a33f0`. Seven other previously read operating/routing/review documents also match their correction-target blob hashes. The existing source pin remains `345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9`; this correction does not change the registry's admitted rows or source-derived transport table. The original pinned-source review remains applicable to that unchanged surface.

## Verification limits and next handoff

Both reviewers used byte-verified copies of 33 files from the exact correction target. Targeted probes use synthetic bodies, injected clients and memory-backed storage; network fetches are explicitly forbidden inside the harnesses. An unused imported `superjson` codec is resolved to a stub that throws on codec use; no codec method was exercised and no dependencies were installed.

The FN1–FN3 harness ran nine corrected-behavior checks: eight passed and the new overlapping-path regression failed its expected non-success assertion. The FN4–FN5 harness ran seven checks: three controls passed and four deliberately demonstrated the remaining provenance defects. These are separate evidence types; passing defect demonstrations do not mean the product passed.

No full product-suite, build, fixture regeneration, dependency audit, or full static-gate rerun was performed locally. Existing author regression code was inspected and the executable-equivalent canonical CI was independently verified. No real browser, real IndexedDB, userscript, live authentication/session, clipboard interaction, live transport, or GitHub-write path was exercised.

Fable's next pass should be limited to FN3's overlapping-path handling and FN4's complete registry identity plus capture-time stamping on all new research paths. Preserve the now-verified FN1/FN2/FN5 behavior, add the listed regressions, regenerate affected descriptors/fixtures/bundle, run the required gates and canonical CI, and return a new frozen SHA for narrow re-review.

Repository changes: **none**. Live-game requests/writes: **0 / 0**. Credentials obtained/requested/used: **none**. Integration: **not performed; clearance withheld**. Phase 2 and Studio integration: **not started**.



## Commands and actual results

Command run once:

```sh
node --test /workspace/scratch/b0ede89cfb43/rereview-work/fn1-fn3-probe.mjs
```

Actual compact result:

```text
Verified 33 target copies against 7bd8592 Git blob SHA-1s
tests 9
pass 8
fail 1

FN3 NEW REGRESSION: overlapping leaf/deeper requests must not silently become green
AssertionError: the deeper requested path is absent;
capture must not claim full projection success
actual true; expected false
```

The one failed check is the confirmed correction regression; it is not an environment/import failure. The other eight checks are independent targeted controls, not a full product suite pass. Two old-target modules were also hash-verified for the side-by-side regression comparison.

Root FN4–FN5 command actually run:

```sh
node --test /workspace/scratch/b0ede89cfb43/rereview-work/probe-fn4-fn5.mjs
```

Final compact output:

```text
Verified 33 files against correction-target Git blobs
DEFECT: secondsBack number -> boolean changes admission but registry remains 35d2269b
DEFECT: removing a userFilter enum member also leaves registry 35d2269b unchanged
DEFECT: MAX_PAGES 20 -> 19 leaves registry 35d2269b unchanged
DEFECT: successful summary research capture still omits policy in journal/export
CONTROL: later-page 429 evidence retained across two pauses and successful retry; no raw body/message export
DEFECT: abandoned research attempt exported without source/registry identity
tests 7
pass 7
fail 0
```

The root suite was rerun once after adding the enum-membership sensitivity case to resolve whether a legitimate narrowing change also preserves the identity. Counts describe the seven final checks, not fourteen distinct checks.

## Portable reproduction appendix

These are review harnesses, not product changes. Recreate two sibling directories, `rereview-work/` and `review-work/`. Save the two harnesses below in `rereview-work/`, together with its `target-blobs.json`. Place the listed correction-target files under `rereview-work/target/`, preserving repository-relative paths, from commit `7bd8592f1d579f33d71c0713cfee4529cd691526`. For the old-projector comparison, place the two files listed in the old-target manifest under `review-work/target/` from commit `8f15416d510eeb53aa82f7b8b09b7ce00accfa83`, and save that manifest as `review-work/target-blobs.json`.

Use Node v24.19.0, the version used for the review. Run `node --test rereview-work/fn1-fn3-probe.mjs` and `node --test rereview-work/probe-fn4-fn5.mjs`. The first currently has one expected-behavior assertion failing; the second deliberately asserts the observed provenance defects as demonstrations. After correction, change the defect-demonstration assertions into regression assertions for the required behavior.

### fn1-fn3-probe.mjs

```javascript
import assert from 'node:assert/strict';
import { test } from 'node:test';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { registerHooks } from 'node:module';

globalThis.fetch = () => { throw new Error('NETWORK_FORBIDDEN_IN_REREVIEW'); };
// Resolve the unused transport dependency only; every codec invocation is forbidden.
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
  const actual = createHash('sha1').update(Buffer.from('blob ' + data.length + '\0')).update(data).digest('hex');
  assert.equal(actual, row.sha, 'correction target copy differs: ' + row.path);
}
console.log('Verified ' + blobs.length + ' target copies against 7bd8592 Git blob SHA-1s');
const oldRows = JSON.parse(readFileSync(new URL('../review-work/target-blobs.json', import.meta.url), 'utf8'));
for (const path of ['forge/src/research/registry.mjs', 'forge/src/transport/procedures.mjs']) {
  const row = oldRows.find((r) => r.path === path);
  const data = readFileSync(new URL('../review-work/target/' + path, import.meta.url));
  const actual = createHash('sha1').update(Buffer.from('blob ' + data.length + '\0')).update(data).digest('hex');
  assert.equal(actual, row.sha, 'old-target control differs: ' + path);
}
const { materialize, resolveCaptures, buildBundle } = await import('./target/forge/src/core/results.mjs');
const { parseManifest } = await import('./target/forge/src/runner/manifest.mjs');
const { projectBody } = await import('./target/forge/src/research/registry.mjs');
const { projectBody: oldProjectBody } = await import('../review-work/target/forge/src/research/registry.mjs');
const { CaptureCache, captureTier, MAX_FULL_CAPTURE_BYTES } = await import('./target/forge/src/storage/captures.mjs');
const { jobOutcome, captureOk } = await import('./target/forge/src/storage/journal.mjs');
const { runHeadline } = await import('./target/forge/src/core/facts.mjs');
const { Runner } = await import('./target/forge/src/runner/runner.mjs');
const SECRET = 'SYNTHETIC-REREVIEW-SECRET';

const oldCapture = () => ({
  phase: 'after', proc: 'quests.get', input: { id: 'q1' }, ok: true, rows: 1,
  error: null, persist: 'full', snapshotKey: 'review::after::0',
  persistOk: true, persistError: null,
});
const oldSnapshot = () => ({
  key: 'review::after::0', jobId: 'review', phase: 'after', ordinal: 0,
  path: 'quests.get', id: 'q1', input: { id: 'q1' },
  data: { id: 'q1', name: 'Exact prior body' }, at: '2026-09-16T00:00:00.000Z',
});
const projCapture = (projection = ['id']) => ({
  ...oldCapture(), persist: 'projected', tier: 'projected', projection,
});
const projSnapshot = (projection = ['id']) => ({
  ...oldSnapshot(), tier: 'projected', projection,
  data: { id: 'q1', content: { note: SECRET }, secret: SECRET },
});
function journalOf(capture) {
  const job = { jobId: 'review', state: 'DONE', items: [], capturesAfter: [structuredClone(capture)] };
  return { job, patches: [], get: () => job,
    annotateJob(id, patch) { this.patches.push(patch); Object.assign(job, patch); } };
}
const build = (job, captures) => buildBundle({ version: 'synthetic-rereview', now: () => 0,
  storage: { getItem: () => null } }, job, captures);
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
async function runProjected(body, fields) {
  const c = parseManifest({ capture: { after: [
    { proc: 'quests.get', input: { id: 'q1' }, persist: 'projected', projection: fields },
  ] } }).capture.after[0];
  const cache = memoryCache();
  const persist = await Runner.prototype._persist.call({ cache }, 'review', 'after', 0,
    c, c.proc, 'q1', { ok: true, data: body });
  const journal = journalOf({ ...projCapture(c.projection), ...persist });
  const captures = await resolveCaptures({ journal, cache }, 'review');
  return { normalized: c, persist, bundle: build(journal.job, captures) };
}

test('FN1: actual pre-tier full capture exports exact body, updates compact journal and headline', async () => {
  const c = oldCapture(); const rec = oldSnapshot(); let lookups = 0;
  const journal = journalOf(c);
  assert.equal(captureTier(c), 'repo-safe');
  const captures = await resolveCaptures({ journal, cache: { getSnapshot: async () => { lookups++; return rec; } } }, 'review');
  const bundle = build(journal.job, captures);
  assert.equal(lookups, 1);
  assert.deepEqual(bundle.captures[0].data, rec.data);
  assert.equal(bundle.outcome, 'success');
  assert.equal(bundle.captures[0].persistOk, true);
  assert.equal(journal.patches.length, 1);
  assert.equal('data' in journal.job.capturesAfter[0], false);
  assert.match(runHeadline(journal.job, { state: 'DONE' }).text, /1\/1 full bodies persisted/);
});

test('FN1: legacy missing/oversize/recorded-storage failures remain non-success without rereads', async () => {
  for (const rec of [null, { ...oldSnapshot(), bytes: MAX_FULL_CAPTURE_BYTES + 1 }]) {
    const journal = journalOf(oldCapture()); let lookups = 0;
    const captures = await resolveCaptures({ journal, cache: { getSnapshot: async () => { lookups++; return rec; } } }, 'review');
    assert.equal(lookups, 1);
    const bundle = build(journal.job, captures);
    assert.equal(bundle.outcome, 'failed');
    assert.equal(bundle.captures[0].persistOk, false);
    assert.equal('data' in bundle.captures[0], false);
  }
  const failed = { ...oldCapture(), persistOk: false, persistError: 'stored quota failure' };
  assert.equal(captureOk(failed), false);
  assert.equal(jobOutcome(journalOf(failed).job), 'failed');
  assert.equal(jobOutcome({ state: 'DONE', items: [{ state: 'VERIFIED' }], capturesAfter: [failed] }), 'unverified');
  const out = await materialize({ getSnapshot: async () => { throw new Error('must not look up a previously failed capture'); } }, failed);
  assert.equal(out.persistError, 'stored quota failure');
});

test('FN1: legacy admission is narrow and snapshot local-only ceiling still wins', async () => {
  for (const persist of [undefined, 'summary', 'fields', 'FULL', true]) assert.equal(captureTier({ persist }), null);
  const unapproved = await materialize({ getSnapshot: async () => { throw new Error('must refuse before lookup'); } }, { ...oldCapture(), proc: 'combat.getBattleEntries' });
  assert.equal(unapproved.persistOk, false);
  const local = await materialize({ getSnapshot: async () => ({ ...oldSnapshot(), tier: 'local-only', data: { secret: SECRET } }) }, oldCapture());
  assert.equal(local.tier, 'local-only');
  assert.equal('data' in local, false);
});

test('FN2: replacing/adding/empty journal projection cannot redirect intact retained fields', async () => {
  const retained = projSnapshot();
  for (const projection of [['secret'], ['id', 'secret'], [], ['__proto__'], ['*'], [1]]) {
    const out = await materialize({ getSnapshot: async () => retained }, projCapture(projection));
    assert.equal(out.persistOk, false);
    assert.equal('data' in out, false);
    assert.equal(JSON.stringify(out).includes(SECRET), false);
  }
  for (const projection of [null, undefined, 'secret']) {
    const out = await materialize({ getSnapshot: async () => retained }, projCapture(projection));
    assert.deepEqual(out.data, { id: 'q1' }); // omitted malformed copy never replaces retained authority
    assert.equal(JSON.stringify(out).includes(SECRET), false);
  }
  assert.deepEqual(retained.projection, ['id']);
});

test('FN2: export revalidates forbidden/missing retained declaration and wider journal tier', async () => {
  for (const projection of [null, [], ['__proto__'], ['a.*'], [42]]) {
    const out = await materialize({ getSnapshot: async () => projSnapshot(projection) }, projCapture(projection));
    assert.equal(out.persistOk, false);
    assert.equal('data' in out, false);
  }
  const out = await materialize({ getSnapshot: async () => projSnapshot() }, { ...projCapture(), tier: 'repo-safe', persist: 'full' });
  assert.equal(out.tier, 'projected');
  assert.deepEqual(out.data, { id: 'q1' });
});

test('FN3: original structured-terminal leaks are refused at project/persist/export', async () => {
  const body = { id: 'q1', content: { note: SECRET, nested: { secret: SECRET }, objectives: [{ id: 'n1', secret: SECRET }] } };
  for (const fields of [['content'], ['content.nested'], ['content.objectives']]) {
    assert.equal(projectBody(body, fields).ok, false);
    const { persist, bundle } = await runProjected(body, fields);
    assert.equal(persist.persistOk, false);
    assert.equal(bundle.outcome, 'failed');
    assert.equal(bundle.captures[0].persistOk, false);
    assert.equal('data' in bundle.captures[0], false);
    assert.equal(JSON.stringify(bundle).includes(SECRET), false);
  }
});

test('FN3: explicit leaves preserve multiple array levels and omit all undeclared fields', async () => {
  const body = { id: 'q1', content: { secret: SECRET, groups: [
    { name: 'g1', extra: SECRET, objectives: [{ id: 'n1', extra: SECRET, rewards: [{ amount: 7, extra: SECRET }] }] },
    { name: 'g2', extra: SECRET, objectives: [] },
  ] }, tags: ['a', 'b'] };
  const fields = ['id', 'content.groups.name', 'content.groups.objectives.id', 'content.groups.objectives.rewards.amount', 'tags'];
  const { bundle } = await runProjected(body, fields);
  assert.equal(bundle.outcome, 'success');
  assert.deepEqual(bundle.captures[0].data, { id: 'q1', content: { groups: [
    { name: 'g1', objectives: [{ id: 'n1', rewards: [{ amount: 7 }] }] },
    { name: 'g2', objectives: [] },
  ] }, tags: ['a', 'b'] });
  assert.equal(JSON.stringify(bundle).includes(SECRET), false);
  assert.equal(body.content.groups[0].extra, SECRET);
});

test('FN3: missing/invalid leaf in any array member prevents partial success', async () => {
  for (const objectives of [[{ id: 'n1' }, { name: 'missing-id' }], [{ id: 'n1' }, null], [{ id: 'n1' }, 'scalar'], [{ id: 'n1' }, { id: { nested: SECRET } }]]) {
    const result = projectBody({ content: { objectives } }, ['content.objectives.id']);
    assert.equal(result.ok, false);
    assert.equal('data' in result, false);
  }
  assert.deepEqual(projectBody([], ['id']), { ok: true, data: [] });
  assert.deepEqual(projectBody({ content: { objectives: [] } }, ['content.objectives.id']).data, { content: { objectives: [] } });
});

test('FN3 NEW REGRESSION: overlapping leaf/deeper requests must not silently become green', async () => {
  const cases = [
    { body: { id: 'q1' }, fields: ['id', 'id.deeper'] },
    { body: { tags: ['a'] }, fields: ['tags', 'tags.deeper'] },
    { body: { content: { objectives: [{ id: 'n1' }] } }, fields: ['content.objectives.id', 'content.objectives.id.deeper'] },
  ];
  for (const { body, fields } of cases) {
    assert.equal(oldProjectBody(body, fields).ok, false, 'previous frozen implementation rejected the undeclarable deeper path');
    const { persist, bundle } = await runProjected(body, fields);
    console.log(JSON.stringify({ probe: 'overlapping-path', fields, projectOk: persist.projectOk, persistOk: persist.persistOk, outcome: bundle.outcome, exported: bundle.captures[0].data }));
  }
  const result = await runProjected({ id: 'q1' }, ['id', 'id.deeper']);
  assert.equal(result.persist.persistOk, false, 'the deeper requested path is absent; capture must not claim full projection success');
});
```

### probe-fn4-fn5.mjs

```javascript
import assert from 'node:assert/strict';
import { test } from 'node:test';
import { readFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { registerHooks } from 'node:module';

globalThis.fetch = () => { throw new Error('NETWORK_FORBIDDEN_IN_REVIEW'); };
registerHooks({
  resolve(specifier, context, nextResolve) {
    return specifier === 'superjson' ? { url: 'review:unused-superjson', shortCircuit: true } : nextResolve(specifier, context);
  },
  load(url, context, nextLoad) {
    return url === 'review:unused-superjson' ? { format: 'module', shortCircuit: true,
      source: 'const unused=()=>{throw new Error("SUPERJSON_NOT_USED_BY_REVIEW")}; export default {serialize:unused,deserialize:unused};' } : nextLoad(url, context);
  },
});
const target = new URL('./target/', import.meta.url);
const manifest = JSON.parse(readFileSync(new URL('./target-blobs.json', import.meta.url), 'utf8'));
for (const row of manifest) {
  const data = readFileSync(new URL(row.path, target));
  assert.equal(createHash('sha1').update(Buffer.from(`blob ${data.length}\0`)).update(data).digest('hex'), row.sha, row.path);
}
console.log(`Verified ${manifest.length} files against correction-target Git blobs`);
const registryURL = new URL('./target/forge/src/research/registry.mjs', import.meta.url);
const registry = await import(registryURL.href);
const { materialize, resolveCaptures, buildBundle } = await import('./target/forge/src/core/results.mjs');
const { parseManifest } = await import('./target/forge/src/runner/manifest.mjs');
const { CaptureCache } = await import('./target/forge/src/storage/captures.mjs');
const { Runner } = await import('./target/forge/src/runner/runner.mjs');
const { CachedReader } = await import('./target/forge/src/budget/reader.mjs');
const { RateLimited } = await import('./target/forge/src/budget/bucket.mjs');
const { jobOutcome } = await import('./target/forge/src/storage/journal.mjs');
const SECRET = 'SYNTHETIC-REREVIEW-PRIVATE-BODY';
function memoryCache() {
  const stores = new Map();
  const cache = new CaptureCache({ open() { throw new Error('REAL_IDB_FORBIDDEN'); } }, () => 1000);
  cache._tx = async (_mode, fn, name = 'captures') => {
    if (!stores.has(name)) stores.set(name, new Map());
    const map = stores.get(name);
    const req = result => { const r = { result: structuredClone(result) }; queueMicrotask(() => r.onsuccess()); return r; };
    return fn({ put(record) { map.set(record.key, structuredClone(record)); return req(record.key); }, get(key) { return req(map.get(key)); } });
  };
  return cache;
}
function journalOf() {
  const job = { jobId: 'review', state: 'RUNNING', items: [] };
  return { job, get: () => job, annotateJob(_id, patch) { Object.assign(job, structuredClone(patch)); } };
}
const build = (job, captures) => buildBundle({ version: 'synthetic-review', now: () => 1000, storage: { getItem: () => null } }, job, captures);
function capture(persist = 'local-only') {
  return parseManifest({ capture: { after: [{ proc: 'combat.getBattleEntries', input: { battleId: 'b1', limit: 2 }, pages: 3, persist }] } }).capture.after[0];
}
function hostOf(journal, cache, reader) {
  return { journal, cache, reader, _requireAuth() {}, _persist: Runner.prototype._persist, _journalAttempt: Runner.prototype._journalAttempt };
}
async function variant(search, replacement) {
  const source = readFileSync(registryURL, 'utf8');
  assert.equal(source.split(search).length, 2, 'variant must change exactly one explicit declaration');
  const changed = source.replace(search, replacement).replace(/from "(\.\.?\/[^\"]+)"/g, (_match, spec) => `from ${JSON.stringify(new URL(spec, registryURL).href)}`);
  return import('data:text/javascript;base64,' + Buffer.from(changed).toString('base64'));
}

test('FN4 CONTROL: new persisted capture carries snapshot policy and export retains it', async () => {
  const c = capture(), cache = memoryCache(), journal = journalOf();
  const reader = { query: async () => ({ ok: true, complete: true, data: [{ id: 'one', raw: SECRET }], pages: [{ n: 0, input: c.input, ok: true, rows: 1 }], rowCount: 1 }) };
  await Runner.prototype._captures.call(hostOf(journal, cache, reader), 'review', [c], 'after');
  journal.job.state = 'DONE';
  const snap = await cache.getSnapshot('review::after::0');
  const policy = registry.capturePolicy(c.proc);
  assert.deepEqual(snap.policy, policy);
  assert.deepEqual(journal.job.capturesAfter[0].policy, policy);
  const result = await resolveCaptures({ journal, cache }, 'review');
  const bundle = build(journal.job, result);
  assert.deepEqual(bundle.captures[0].policy, policy);
  assert.equal(JSON.stringify(bundle).includes(SECRET), false);
});

test('FN4 CONTROL: authentic pre-stamp capture exports without fabricated policy', async () => {
  const old = { phase: 'after', proc: 'quests.get', ok: true, persist: 'full', snapshotKey: 'old', persistOk: true };
  const snap = { path: 'quests.get', data: { id: 'q1' } };
  const out = await materialize({ getSnapshot: async () => snap }, old);
  assert.equal(out.persistOk, true);
  assert.equal('policy' in out, false);
});

test('FN4 DEFECT: real input contract type changes leave registry identity unchanged', async () => {
  const altered = await variant('secondsBack: NUM', 'secondsBack: BOOL');
  const path = 'combat.getBattleHistory';
  assert.deepEqual(registry.canonicalInput(path, { secondsBack: 10 }), { secondsBack: 10 });
  assert.throws(() => altered.canonicalInput(path, { secondsBack: 10 }), /boolean/);
  assert.deepEqual(altered.canonicalInput(path, { secondsBack: true }), { secondsBack: true });
  assert.equal(altered.REGISTRY_REVISION, registry.REGISTRY_REVISION);
  console.log(`DEFECT: secondsBack number -> boolean changes admission but registry remains ${registry.REGISTRY_REVISION}`);
  const narrower = await variant('oneOf("all", "user", "opponents")', 'oneOf("all", "user")');
  assert.equal(registry.canonicalInput('combat.getBattleEntries', { battleId: 'b1', userFilter: 'opponents' }).userFilter, 'opponents');
  assert.throws(() => narrower.canonicalInput('combat.getBattleEntries', { battleId: 'b1', userFilter: 'opponents' }), /must be one of/);
  assert.equal(narrower.REGISTRY_REVISION, registry.REGISTRY_REVISION);
  console.log(`DEFECT: removing a userFilter enum member also leaves registry ${registry.REGISTRY_REVISION} unchanged`);
});

test('FN4 DEFECT: global walk bound changes leave registry identity unchanged', async () => {
  const altered = await variant('export const MAX_PAGES = 20;', 'export const MAX_PAGES = 19;');
  assert.equal(altered.MAX_PAGES, 19);
  assert.equal(registry.MAX_PAGES, 20);
  assert.equal(altered.REGISTRY_REVISION, registry.REGISTRY_REVISION);
  console.log(`DEFECT: MAX_PAGES 20 -> 19 leaves registry ${registry.REGISTRY_REVISION} unchanged`);
});

test('FN4 DEFECT: summary research capture has no source or registry stamp', async () => {
  const c = capture('summary'), cache = memoryCache(), journal = journalOf();
  const reader = { query: async () => ({ ok: true, complete: true, data: [{ id: 'one', raw: SECRET }], pages: [], rowCount: 1 }) };
  await Runner.prototype._captures.call(hostOf(journal, cache, reader), 'review', [c], 'after');
  journal.job.state = 'DONE';
  const entries = await resolveCaptures({ journal, cache }, 'review');
  assert.equal('policy' in journal.job.capturesAfter[0], false);
  assert.equal('policy' in build(journal.job, entries).captures[0], false);
  assert.equal(JSON.stringify(build(journal.job, entries)).includes(SECRET), false);
  console.log('DEFECT: successful summary research capture still omits policy in journal/export');
});

test('FN5 CONTROL: page-2 429 persists metadata, preserves cursor, and repeated attempts are retained', async () => {
  const c = capture(), cache = memoryCache(), journal = journalOf();
  let count = 0, successful = false;
  const inputs = [];
  const reader = new CachedReader({ cache, client: { batch: async calls => {
    const input = calls[0].input; inputs.push(structuredClone(input)); count++;
    if (successful) return [{ ok: true, data: [{ id: 'final', raw: SECRET }] }];
    if (count % 2) return [{ ok: true, data: [{ id: 'a1', raw: SECRET }, { id: 'a2', raw: SECRET }] }];
    return [{ ok: false, error: { code: 'TOO_MANY_REQUESTS', httpStatus: 429, message: SECRET } }];
  } }, budget: { acquire: async () => {}, observe(results) { if (!results[0].ok) throw new RateLimited({ path: c.proc, until: 2000 }); } } });
  const host = hostOf(journal, cache, reader);
  for (let attempt = 0; attempt < 2; attempt++) {
    await assert.rejects(() => Runner.prototype._captures.call(host, 'review', [c], 'after'), RateLimited);
    assert.equal(journal.job.capturesAfter, undefined);
    assert.equal(journal.job.capturesAfterPartial, undefined);
    assert.equal(journal.job.capturesAfterAttempts.length, attempt + 1);
  }
  journal.job.state = 'PAUSED';
  const attempts = structuredClone(journal.job.capturesAfterAttempts);
  for (const a of attempts) {
    assert.equal(a.abandoned, true);
    assert.equal(a.persistOk, false);
    assert.equal(a.complete, false);
    assert.deepEqual(a.pages.map(p => p.ok), [true, false]);
    assert.deepEqual(a.pages.map(p => p.rows), [2, 0]);
    assert.deepEqual(a.pages.map(p => p.input), inputs.slice(0, 2));
  }
  const pausedBundle = build(journal.job, await resolveCaptures({ journal, cache }, 'review'));
  assert.equal(jobOutcome(journal.job), 'open');
  assert.equal(pausedBundle.captures.length, 2);
  assert.equal(JSON.stringify(pausedBundle).includes(SECRET), false);
  successful = true;
  journal.job.state = 'RUNNING';
  await Runner.prototype._captures.call(host, 'review', [c], 'after');
  journal.job.state = 'DONE';
  assert.deepEqual(journal.job.capturesAfterAttempts, attempts);
  assert.equal(journal.job.capturesAfter.length, 1);
  const completed = build(journal.job, await resolveCaptures({ journal, cache }, 'review'));
  assert.equal(completed.outcome, 'success');
  assert.equal(completed.captures.filter(c => c.abandoned).length, 2);
  assert.equal(completed.captures.filter(c => !c.abandoned).length, 1);
  assert.equal(JSON.stringify(completed).includes(SECRET), false);
  console.log('CONTROL: later-page 429 evidence retained across two pauses and successful retry; no raw body/message export');
});

test('FN4 DEFECT: abandoned research capture still has no policy stamp', async () => {
  const journal = journalOf(), c = capture();
  const host = hostOf(journal, memoryCache(), {});
  Runner.prototype._journalAttempt.call(host, 'review', 'capturesAfter', c, 'after', 0,
    Object.assign(new RateLimited({ path: c.proc, until: 2000 }), { rowCount: 2, pages: [{ n: 0, input: c.input, ok: true, rows: 2 }, { n: 1, input: { ...c.input, offset: 2 }, ok: false, rows: 0, error: 'TOO_MANY_REQUESTS' }] }));
  assert.equal('policy' in journal.job.capturesAfterAttempts[0], false);
  const entries = await resolveCaptures({ journal, cache: host.cache }, 'review');
  assert.equal('policy' in entries[0], false);
  console.log('DEFECT: abandoned research attempt exported without source/registry identity');
});
```

### Correction target-blobs.json

```json
[
  {
    "path": "32b_DATA_pool.json",
    "sha": "419a0d17eb2c0a3429f69e28db8f236ed4996f45"
  },
  {
    "path": "forge/RESEARCH_REGISTRY.md",
    "sha": "e4beee59ec92d9c55f996b90b906eae55632c917"
  },
  {
    "path": "forge/src/budget/bucket.mjs",
    "sha": "dcacab4b183cc7a02194830a6136a42dce030c9d"
  },
  {
    "path": "forge/src/budget/reader.mjs",
    "sha": "314c5590e703036f104254ca07b76259aeca73b3"
  },
  {
    "path": "forge/src/core/facts.mjs",
    "sha": "8d00a1c469caa72006769824ff284ab405d9f663"
  },
  {
    "path": "forge/src/core/results.mjs",
    "sha": "0949489d57b256b0c07f6a47bb01da2bff66cef2"
  },
  {
    "path": "forge/src/github.mjs",
    "sha": "6f3394d230fc3a2eb33bc3c27f83fd8006acfd79"
  },
  {
    "path": "forge/src/research/registry.mjs",
    "sha": "b857d5d7b7f867b2a992cb72d75a2feef27825b4"
  },
  {
    "path": "forge/src/runner/fields.json",
    "sha": "278e076f5141bfad112eb6dd0f95a04fa7df8ddd"
  },
  {
    "path": "forge/src/runner/lints.mjs",
    "sha": "33be48b8dd149c7f0d581fd18209c843d8a939cb"
  },
  {
    "path": "forge/src/runner/manifest.mjs",
    "sha": "4c34a6458c854cae80a8b34f41a20a1e6b0950c2"
  },
  {
    "path": "forge/src/runner/nested.json",
    "sha": "40d1793e4be47896bc1fd5e501f817e38824e1c6"
  },
  {
    "path": "forge/src/runner/pool.mjs",
    "sha": "09ba9a5536f1d597933e883128210c4255c8f93e"
  },
  {
    "path": "forge/src/runner/recipes.mjs",
    "sha": "7be3c1e6ea5b5bbcff80321d486fd69adf15444e"
  },
  {
    "path": "forge/src/runner/refs.mjs",
    "sha": "c3cd6f1cb9511e46d2466f45ba584ae0a3936a96"
  },
  {
    "path": "forge/src/runner/runner.mjs",
    "sha": "6cf8e2ae4407f62ce2553925c5f7ca836d5d79b6"
  },
  {
    "path": "forge/src/runner/validate.mjs",
    "sha": "6b007fa3d4981c30b10196b49e41d132fa78eda9"
  },
  {
    "path": "forge/src/storage/captures.mjs",
    "sha": "bdc5cfa79e6b2149cd3abee4c58d0b1bf808d0d6"
  },
  {
    "path": "forge/src/storage/compat.mjs",
    "sha": "9ec81e3a655927e2a638275f532bfd88f335bd4c"
  },
  {
    "path": "forge/src/storage/hash.mjs",
    "sha": "c1bfa7b90abd97c338794e80e15c991d89743d11"
  },
  {
    "path": "forge/src/storage/journal.mjs",
    "sha": "652f6bf54a51277af503f41bc280aca07397c4d0"
  },
  {
    "path": "forge/src/transport/auth.mjs",
    "sha": "a6c90c78a77f6deb8e64d8e1f1975d47475ceeec"
  },
  {
    "path": "forge/src/transport/client.mjs",
    "sha": "252318f7dd4771df9dc10aac7339f63b7968eb04"
  },
  {
    "path": "forge/src/transport/envelope.mjs",
    "sha": "cef404088bfdf96ad649977d34646e0860d8dc9b"
  },
  {
    "path": "forge/src/transport/outcome.mjs",
    "sha": "1bfc01f3cadeedf42262e6973b2984f14d0e78c1"
  },
  {
    "path": "forge/src/transport/procedures.mjs",
    "sha": "62e6b6332834ba01b1b4f1e4fe3c6268f5744b38"
  },
  {
    "path": "forge/src/transport/session.mjs",
    "sha": "7cd9fc64bd20369692cb384ffc8bc54fce6387af"
  },
  {
    "path": "forge/src/ui/screens.mjs",
    "sha": "ee839d5143116af401364e5db1926f39e1799539"
  },
  {
    "path": "forge/test/fixtures/screens/manifests_selected_research.txt",
    "sha": "01076bd6760faf295b441f6c6f136a5b1a84fe3e"
  },
  {
    "path": "forge/test/research.review.test.mjs",
    "sha": "98d4c2a4fe8747804e2372229b3f810720019aed"
  },
  {
    "path": "forge/test/research.tiers.test.mjs",
    "sha": "0824f4a8098491669f76ae615508f270c167b851"
  },
  {
    "path": "forge/test/screen_scenarios.mjs",
    "sha": "de37bb77cb7a6385a0fa1b794c75375161cc18b5"
  },
  {
    "path": "forge/tools/derive_registry.mjs",
    "sha": "d767aa00bcdb67dc26d70cf22d5c9f58bd097af7"
  }
]
```

### Old comparison target-blobs.json

```json
[
  {
    "path": "forge/src/research/registry.mjs",
    "sha": "9757483f2e4b8d844ddda05c3ce8133f01afa81c",
    "size": 24626
  },
  {
    "path": "forge/src/transport/procedures.mjs",
    "sha": "62e6b6332834ba01b1b4f1e4fe3c6268f5744b38",
    "size": 7763
  }
]
```
