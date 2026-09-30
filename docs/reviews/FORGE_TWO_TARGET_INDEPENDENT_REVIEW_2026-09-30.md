# Forge two target independent review

**Target A: PASS WITH NOTES. Target B: PASS WITH NOTES. No blocking defect found.**

Independent reviewer: ChatGPT, Engineering Auditor. Review date: 2026-09-30.
Repository: `perseverance484/tnr-tools`. Scope: Target A’s synchronization delta and Target B’s test-path correction at the exact frozen commits below.

The proposed integration order is sound: integrate B, merge fresh main into the Phase 1 branch without rebasing, return the resulting SHA with current gates and canonical CI, then integrate Phase 1 after verification. A narrow verification is sufficient under the conditions recorded below. These verdicts do not approve a release or an unseen future merge.

Neither implementation branch nor main was modified. All integration work was confined to detached scratch trees and local Git objects. No remote repository writes, live-game requests, live-game writes, browser/session operations, or credential acquisition occurred.

## Exact targets and references

| Role | Verified SHA |
| --- | --- |
| Target A, frozen code and budget | `36dc359ebdf503f56dca2bb16994a627c362f44c` |
| A merge commit | `99ec81e146755e7d6869e1e6bd86b37855bf90a6` |
| A merge first parent | `c7bdd2d2e7e5688d09361e4c665ca735277a03a6` |
| A merge second parent, historical main | `18c6a2554c1bf9231e00e46108a5a7faf66387aa` |
| Previously reviewed Phase 1 code | `9133145c1e626eb1611ac6a23302b58885c33fe6` |
| Both Phase 1 branch tips | `0016994b61858c6409dfa9fcd920e5291f4bb6c4` |
| Target B, frozen test fix | `57bceddb31bfaf97a9379e41e67dd501aa223aaa` |
| B base | `1601f072af839402395eeab1326b1228747e0009` |
| B branch tip | `aa5f49927eaff1995577e3877806738bb097bbde` |
| Main, verified at start and finish | `06b66b085c92216accd7913b32126a7a10413603` |
| Retained game-source pin | `345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9` |

The two Phase 1 refs are `fable/forge-next-phase1` and `claude/forge-next-phase1-uwhcn1`. B’s ref is `ccr-d998b825-q58zf8`. Differences above both frozen targets are documentation only. The second-correction review is present at A’s documentation tip `0016994`; it is not present at the earlier frozen code commit `36dc359`. Its absence there is expected, not a missing-code finding.

The governing `state/prompt_forge_next_phase1.md` is unchanged. Repository operating/review guidance, the contract, both handoffs, the previous correction review, relevant rulings, code, tests, fixtures, build tools, and pinned asset source were inspected. Stale operational state was treated as orientation, not evidence that implementation was absent.

## Target A verdict and synchronization audit

**PASS WITH NOTES at `36dc359ebdf503f56dca2bb16994a627c362f44c`.** No synchronization regression requiring correction was found.

Both parent-relative changes and `git diff 18c6a25...36dc359` were inspected. `git show --remerge-diff 99ec81e` independently identifies the eight conflicted paths and makes the resolutions distinguishable from automatic merges and additional semantic repairs.

| Conflicted path, under `forge/` unless stated | Assessment |
| --- | --- |
| `src/runner/manifest.mjs` | Main’s normalized execution policy, body/manifest identity, and image-pack identity survive. Phase 1’s full-capture and per-tier counts are placed on the returned manifest rather than inside policy. Independent comparisons against main preserve existing manifest hashes, including the real archived image-pack manifest. |
| `src/runner/runner.mjs` | Image-pack upload/provenance imports and behavior coexist with Phase 1’s mode-dispatched capture path. The previous parallel input bookkeeping is safely superseded; see below. |
| `src/ui/screens.mjs` | Both import groups survive. Image-pack and research screen scenarios remain present. |
| `test/fakegame.mjs` | Asset object-required validation, type filtering and folder prefixes coexist with both combat response implementations. |
| `test/screen_scenarios.mjs` | Both research scenarios and both image-pack scenarios survive. All 16 screen fixtures reproduce. |
| `tools/check_boundaries.mjs` | Main’s property 4 presentation containment remains intact. Phase 1’s view restriction becomes property 5. Registry/fields/nested pin agreement remains checked. Positive and deliberately failing synthetic cases pass in the suite. |
| `tools/check_bundle_budget.mjs` | Merge keeps main’s ceiling. The next commit isolates the measured raise; obsolete Phase 1 ceilings are not restored. |
| Root `forge_bundle.js` | Regenerates byte-for-byte from the merged source and main’s build pipeline. |

Automatic merges were also inspected. Main’s core image-pack wiring, entry point, build/comment-strip pipeline, workflow and package version remain present; Phase 1’s headline/tier additions coexist with them. The source-derived transport table is byte-identical to the previously reviewed Phase 1 table. No registry row was added, removed, or retiered.

### Asset input contract and capture provenance

The corrected row is supported by [asset.ts at the declared pin](https://github.com/studie-tech/TheNinjaRPG/blob/345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9/app/src/server/api/routers/asset.ts#L50): the input is a required object whose `type` and `folderPrefix` members are optional. The complete `getAllNames` procedure block compares byte-identically with the handoff’s [upstream checkpoint](https://github.com/studie-tech/TheNinjaRPG/blob/b78eadb9e817fd95ab6207768846fda0ea121019/app/src/server/api/routers/asset.ts). The six enum members were independently read from pinned `app/drizzle/constants.ts`. This does not assert equivalence to an unexamined newer upstream head.

The [registry correction](https://github.com/perseverance484/tnr-tools/blob/36dc359ebdf503f56dca2bb16994a627c362f44c/forge/src/research/registry.mjs#L139) and [derived list input](https://github.com/perseverance484/tnr-tools/blob/36dc359ebdf503f56dca2bb16994a627c362f44c/forge/src/budget/reader.mjs#L32) are sound:

- An omitted asset filter canonicalizes to `{}`. No member is defaulted, so safety name reads keep plain, unfiltered names.
- Asset captures now use the query mode derived from the row. Filters participate in cache identity and are validated before transport.
- The five input-free lists still send `undefined`; nonempty unaudited input keys remain inadmissible.
- Revision `0657385d` becomes `2b643a51`. An independent comparison verifies identical path membership and tier policy, and identical other rows.
- Invalid types, invalid booleans, unaudited keys, and requests to widen the asset list to repo-safe/projected are refused before any fake transport call.

Main’s `capInput` and `sentInput` were functional on main; they become redundant after adopting the [new capture dispatch](https://github.com/perseverance484/tnr-tools/blob/36dc359ebdf503f56dca2bb16994a627c362f44c/forge/src/runner/runner.mjs#L695). Their deletion is safe because parsing, query transport, cache keys, journal entries and snapshots derive from the canonical representation. Independent before/after capture probes confirm exact input and page-key agreement, including `folderPrefix: false`, a true folder prefix, and filtered asset types. Seeded stale cache entries cannot satisfy these fresh captures. Local-only response names remain absent from journal/export payloads.

A runner probe also performs an entirely in-process asset create between before/after captures. Deduplication and reconciliation send plain `{}`; create/fill invalidation clears stale list/query entries; the immutable before snapshot excludes the new record and the after snapshot includes it. No live transport was used.

### A notes, none blocking

**A-N1 — duplicate caches are efficiency debt, not stale-evidence behavior.** `CachedReader.list()` and `query()` retain separate slots for the unfiltered asset list. Independent probes observe both slots and filtered slots, verify separate cache hits, and verify that both `invalidateRecord('asset', id)` and `invalidateEntity('asset')` remove them all. Captures are fresh. Consolidation may save a redundant read/cache copy, but is not required for this integration.

**A-N2 — the intermediate merge is intentionally over budget.** The bundle is identical at `99ec81e` and `36dc359`. At the former it exceeds `354,000 / 78,000`; at the latter it fits `380,000 / 85,000`. Only the budget tool changes between these commits. Interpret “red on budget alone” as one underlying cause: the same budget assertion is also embedded in `npm test`, so that intermediate commit is not a green test target. Review/integrate the frozen pair, not `99ec81e` alone.

**A-N3 — state reconciliation remains separate work.** Main’s generated state still describes Phase 1 as not begun. Update it through its existing digest/session projection workflow at the appropriate integration closeout. This stale state must not trigger reimplementation. It was not changed by this review.

The two deferred policy choices remain deferred: player-identifying projections for battle history and widening name lists to repo-safe. This synchronization changes neither permission.

## Target B verdict and fixture audit

**PASS WITH NOTES at `57bceddb31bfaf97a9379e41e67dd501aa223aaa`.** The archive path is the correct current home. No assertion or expectation was weakened.

The entire changed test file equals the base file after removing the two added comment lines and reversing the single path replacement. The OPC test still asserts deduplication, the quest phase, the exact planner order `[0, 1, 3, 4, 2]`, and journal/attach agreement under all four retained-idmap states.

All four inspected references resolve to the same full Git blob:

`cb9da51493057632c367ec0389223df83f4cbfb5`

| Reference | Manifest path |
| --- | --- |
| `ce748f6` | `push/54_one_perfect_crop_launch_final.json` |
| `abcb248~1` | `push/54_one_perfect_crop_launch_final.json` |
| Frozen B `57bcedd` | `archive/spent-manifests/push-2026-09-28/54_one_perfect_crop_launch_final.json` |
| Verified main `06b66b0` | The same archive path |

History confirms `418874a` added the archived copy and `abcb248` removed the active copy. `push/README.md` explicitly reserves staging for operator-use manifests and directs archiving after use. Pointing the test to committed history preserves that rule and avoids returning a spent write manifest to the picker. It also avoids copying an additional 821-line fixture. A future archive relocation would still require updating the test; the current correction fails loudly if the file disappears.

On B’s base, the focused runner suite independently reproduces **25 pass / 1 fail**, with the exact missing `push/54` path. Frozen B passes the full **523/523** suite. Its source bundle and generated fixtures are unchanged and reproducible.

### B notes, none blocking

**B-N1 — confirmed pre-existing coverage debt in manifest 53.** At [godstorm.repair.test.mjs:40](https://github.com/perseverance484/tnr-tools/blob/57bceddb31bfaf97a9379e41e67dd501aa223aaa/forge/test/godstorm.repair.test.mjs#L40), `REPAIR_53` still points to absent `push/53`. The helper at line 71 therefore takes its fallback at line 83. Its eight-file byte ledger currently equals the archived ledger, so the manual-picker rejection behavior remains covered; it no longer checks the actual nine-item committed manifest’s composition. This debt predates B and is not caused by its one-line correction.

Small follow-up: resolve the archived 53, preserve the deliberate removal of `imagePack` for this manual-picker test, and fail if the real fixture cannot be found. A shared resolver is reasonable separately, but is unnecessary to approve B. `imgpack.test.mjs` is unaffected: its `findManifest()` currently returns the real archived 53, and the corresponding end-to-end tests pass.

**B-N2 — fixture dependencies are missing from Forge workflow path filters.** The [workflow filters](https://github.com/perseverance484/tnr-tools/blob/57bceddb31bfaf97a9379e41e67dd501aa223aaa/.github/workflows/forge.yml#L3) include neither `push/**` nor `archive/spent-manifests/**`, despite tests reading files there. An archive-only change can therefore bypass Forge CI. This is pre-existing, consistent with how the original failure escaped the Forge trigger, and does not block the present correction. A separate change should include the relevant external fixture dependencies in the trigger filters or otherwise guarantee that such changes run the dependent tests.

Branch naming is not a blocker: the session-assigned implementation ref is explicit and its exact code SHA is verified.

## Independently reproduced verification

Runtime: Node `v24.19.0`, npm `11.9.0`, matching the CI workflow’s Node 24 major. Dependencies installed from the frozen lockfile. That lockfile is identical at A, B, B’s base and the Phase 1 tip. Runtime audit reports **0 vulnerabilities**.

Tests, probes and generators ran with a preload that refuses real `fetch`, socket, HTTP(S), TLS and datagram creation. Product test transport and the tRPC fixture adapter remain in-process. No game application was executed.

| Check | A `36dc359` | B `57bcedd` | Scratch combined tree |
| --- | --- | --- | --- |
| Full product suite | **581/581** | **523/523** | **582/582** |
| Independent synchronization probes | **6/6** | Not applicable | Not repeated; runtime source equals A |
| Import gate | 41 modules, 78 edges, 0 violations | 40 modules, 71 edges, 0 violations | 41 modules, 78 edges, 0 violations |
| Boundary gate | 41 src + 13 presentation, 0 violations | 40 src + 13 presentation, 0 violations | 41 src + 13 presentation, 0 violations |
| Envelope and screen fixtures | Byte-identical | Byte-identical | Byte-identical |
| Checked bundle rebuild | Byte-identical | Byte-identical | Byte-identical |
| Generated registry descriptor | Byte-identical | Not applicable | Byte-identical |
| Raw bytes / ceiling | 368,514 / 380,000 | 339,669 / 354,000 | 368,514 / 380,000 |
| Gzip bytes / ceiling | 82,479 / 85,000 | 74,926 / 78,000 | 82,479 / 85,000 |

Phase 1’s measured increment over main is **28,845 raw / 7,553 gzip**, leaving **11,486 raw / 2,521 gzip** under the new limits. The release-pin check remains clean, with the existing 0.5.1 loader and its immutable `13b313d8` pin unchanged.

Commands included:

```sh
# From the relevant checkout's forge directory; REVIEW_GUARD points to the appended preload.
NODE_OPTIONS="--import=$REVIEW_GUARD" npm test
# Complete captured runs for A and the combined tree used the same suite serially:
NODE_OPTIONS="--import=$REVIEW_GUARD" node --test --test-concurrency=1 --test-reporter=tap 'test/**/*.test.mjs'
node tools/check_imports.mjs
node tools/check_boundaries.mjs
npm run fixtures
git diff --exit-code -- test/fixtures
npm run build
git diff --exit-code -- ../forge_bundle.js
node tools/derive_registry.mjs
git diff --exit-code -- RESEARCH_REGISTRY.md
node tools/check_bundle_budget.mjs
npm audit --omit=dev --audit-level=high
```

Environment corrections were not counted as product failures: an initial parallel A invocation returned an incomplete log and was excluded from the pass count; the serial run provides all 581 results. An initial B fixture regeneration used symlinked dependencies and exposed their absolute paths in normalized stack traces; installing the identical lockfile locally in B restored exact fixture reproduction. All final reviewed trees are clean.

CI was independently read, not merely repeated from the handoffs:

- **A:** [Forge run 35518539978](https://github.com/perseverance484/tnr-tools/actions/runs/35518539978), exact head `36dc359`, job `106098496934`: success, all 15 listed steps successful.
- **B:** [Forge run 36670880858](https://github.com/perseverance484/tnr-tools/actions/runs/36670880858), exact head `57bcedd`, job `109745409660`: success, all 15 listed steps successful. This is additional evidence beyond B’s handoff, which said CI had not been run. No rerun was requested by this reviewer.

## Combined integration and the next verification

Scratch Git merges used the proposed order: B into verified main, then that merged tree into Phase 1 tip `0016994`. Both merge-tree operations are clean. No implementation branch was checked out for writing or advanced.

- B + current main tree: `2a05d9441ec1b2f75bef7715faac5273675dd03b`.
- Combined tree: `46d9c5ffd164e0081dcc5c47a1f204654c5a2d03`.
- Local scratch combined commit: `31ed000a72a6dbd4c91c18167726fc30c27fd3e2`. This is not a published or approved integration SHA.

Within `forge/`, the workflow, root bundle and loader, the only difference between frozen A and this combined tree is `forge/test/runner.test.mjs`: main’s OPC test plus B’s corrected path. Runtime sources, generated contracts, package lock, fixtures, registry and bundle are unchanged. A separately computed combined tree without B differs only by B’s four-line test patch. The full without-B combined suite was not rerun; the missing-file control was reproduced on B’s base and the exact tree difference was checked.

The broader ancestry contains 81 reachable commits from historical main `18c6a25` to verified main `06b66b0`; the approximate “57 commits” is not used as a scope guarantee. The claimed Forge changed-path scope is correct: only `ce748f6` changes `forge/` in that interval.

**A narrow verification is sufficient for step 2 if all of the following remain true:**

1. Merge B into main, then merge fresh main into Phase 1 without rebasing. Preserve both frozen targets and the reviewed Phase 1 history as ancestors.
2. Return the exact new head, both merge parents, fresh main SHA, changed-path inventory and canonical Forge CI run at that head. Documentation-only commits above a CI head must be identified explicitly.
3. Re-run the full suite and required gates, fixture/bundle/registry reproduction, budget and release-pin check. Current combined expectation is 582 tests; explain any later change in that count.
4. The refreshed delta contains only the expected main/B changes and documentation/state reconciliation. Runtime, admission/persistence policy, source pin, generated contracts, loader and release version remain as reviewed.

Unexpected runtime changes, new conflict resolutions, pin movement, weakened tests or unexplained generated output require reviewing the additional affected surfaces. The narrow check is not permission to skip the new merge’s gates or CI. Phase 2 and the separate operator release to 0.5.2 do not begin through this review.

No installed Android userscript, real browser IndexedDB, Clerk session, production transport or live export/share behavior was exercised. Those limitations remain explicit and are not needed to prove a local test-path fix or the bounded synchronization claims assessed here.

## Reproducible independent probes

The appendix contains the network guard and six probes used for A. Save each code block under the indicated filename outside either implementation checkout. Use detached checkouts at frozen A and B’s base, with their lockfile dependencies installed. Run:

```sh
REVIEW_TREE=/absolute/path/to/target-a \
REVIEW_MAIN_TREE=/absolute/path/to/base-b \
NODE_OPTIONS=--import=/absolute/path/to/no-network.mjs \
node --test --test-reporter=tap /absolute/path/to/reconciliation-probes.mjs
```


### no-network.mjs

```javascript
import net from 'node:net';
import tls from 'node:tls';
import http from 'node:http';
import https from 'node:https';
import dgram from 'node:dgram';
import { syncBuiltinESMExports } from 'node:module';
const refuse = () => { throw new Error('Independent review: network access forbidden'); };
globalThis.fetch = refuse;
net.Socket.prototype.connect = refuse;
net.connect = refuse;
net.createConnection = refuse;
tls.connect = refuse;
http.request = refuse;
http.get = refuse;
https.request = refuse;
https.get = refuse;
dgram.createSocket = refuse;
syncBuiltinESMExports();
```

### reconciliation-probes.mjs

```javascript
import test from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import { resolve } from 'node:path';

const root = resolve(process.env.REVIEW_TREE || '/workspace/scratch/11ab29bf02fa/target-a');
const mod = (p) => import(pathToFileURL(resolve(root, p)).href);
const registry = await mod('forge/src/research/registry.mjs');
const { parseManifest } = await mod('forge/src/runner/manifest.mjs');
const { listInput } = await mod('forge/src/budget/reader.mjs');
const { composeForTest } = await mod('forge/test/compose.mjs');
const { resolveCaptures } = await mod('forge/src/core/results.mjs');
const { jobOutcome } = await mod('forge/src/storage/journal.mjs');
const { snapshotKey } = await mod('forge/src/storage/captures.mjs');
const path = 'gameAsset.getAllNames';
const types = ['STATIC', 'ANIMATION', 'SCENE_BACKGROUND', 'SCENE_CHARACTER', 'SFX', 'MUSIC'];
function seeded() {
  const h = composeForTest();
  for (const [i, type] of types.entries()) h.game.seed('asset', {
    id: `asset-${i}`, name: `PRIVATE-${type}`, type, folder: 'folder', image: 'x', url: 'x', hidden: true,
  });
  return h;
}
const inputs = (h) => h.game.calls.filter(c => c.path === path).map(c => c.input);

test('registry delta is confined to asset input facts; tiers and transport remain unchanged', async () => {
  let oldText = execFileSync('git', ['show', '9133145:forge/src/research/registry.mjs'], { cwd: root, encoding: 'utf8' });
  for (const [rel, full] of [['../transport/procedures.mjs', 'forge/src/transport/procedures.mjs'], ['../storage/hash.mjs', 'forge/src/storage/hash.mjs']]) {
    oldText = oldText.replace(JSON.stringify(rel), JSON.stringify(pathToFileURL(resolve(root, full)).href));
  }
  const old = await import('data:text/javascript;base64,' + Buffer.from(oldText).toString('base64'));
  assert.equal(old.REGISTRY_REVISION, '0657385d');
  assert.equal(registry.REGISTRY_REVISION, '2b643a51');
  assert.deepEqual([...registry.RESEARCH_PATHS].sort(), [...old.RESEARCH_PATHS].sort());
  for (const p of registry.RESEARCH_PATHS) {
    assert.equal(registry.RESEARCH_READS[p].tier, old.RESEARCH_READS[p].tier);
    if (p !== path) assert.deepEqual(registry.RESEARCH_READS[p], old.RESEARCH_READS[p]);
  }
  assert.equal(execFileSync('git', ['diff', '9133145', '36dc359', '--', 'forge/src/transport/procedures.mjs'], { cwd: root, encoding: 'utf8' }), '');
});

test('optional members retain their meaning, invalid filters and wider tiers fail before any transport', () => {
  assert.deepEqual(listInput(path), {});
  assert.equal(registry.readMode(path), 'query');
  for (const type of types) for (const folderPrefix of [false, true]) {
    assert.deepEqual(registry.canonicalInput(path, { folderPrefix, type }), { type, folderPrefix });
  }
  const h = seeded();
  for (const input of [{ type: 'WRONG' }, { folderPrefix: 'true' }, { id: 'asset-0' }, []]) {
    assert.throws(() => h.runner.plan({ items: [], capture: { after: [{ proc: path, input }] } }));
  }
  for (const persist of ['full', 'repo-safe', 'projected']) {
    assert.throws(() => h.runner.plan({ items: [], capture: { after: [{ proc: path, input: {}, persist, projection: ['name'] }] } }));
  }
  assert.equal(h.game.calls.length, 0);
  for (const p of ['jutsu.getAllNames', 'quests.getAllNames', 'item.getAllNames', 'bloodline.getAllNames', 'profile.getAllAiNames']) {
    assert.equal(listInput(p), undefined);
    assert.equal(registry.readMode(p), 'list');
  }
  h.cache.close();
});

test('fresh asset captures preserve exact sent inputs, page keys, snapshots and local-only exports in both phases', async () => {
  const h = seeded();
  const filters = [{}, { type: 'SFX' }, { folderPrefix: false, type: 'STATIC' }, { folderPrefix: true, type: 'MUSIC' }];
  await h.cache.put({ path, id: '', input: {}, data: [{ name: 'STALE-BARE' }] });
  for (const input of filters) {
    const canonical = registry.canonicalInput(path, input);
    await h.cache.putQuery({ path, queryKey: registry.canonicalKey(canonical), input: canonical, data: [{ name: 'STALE-QUERY' }] });
  }
  const captures = filters.map(input => ({ proc: path, input, persist: 'local-only' }));
  h.runner.plan({ items: [], capture: { before: captures, after: captures } }, { jobId: 'inputs' });
  await h.runner.run('inputs');
  assert.equal(jobOutcome(h.journal.get('inputs')), 'success');
  const sent = inputs(h);
  assert.equal(sent.length, 8, 'each capture is fresh despite both cache slots being populated');
  const exported = await resolveCaptures(h, 'inputs');
  for (const [n, cap] of exported.entries()) {
    assert.deepEqual(cap.input, sent[n]);
    assert.deepEqual(cap.pages[0].input, sent[n]);
    assert.equal(cap.pages[0].key, registry.canonicalKey(sent[n]));
    assert.equal(cap.policy.registry, '2b643a51');
    assert.equal(cap.persistOk, true);
    assert.equal(cap.complete, true);
    assert.equal(cap.localOnly, true);
    assert.ok(!('data' in cap));
    const snap = await h.cache.getSnapshot(snapshotKey('inputs', n < 4 ? 'before' : 'after', n % 4));
    assert.deepEqual(snap.input, sent[n]);
    assert.ok(snap.data.every(x => !x.name.startsWith('STALE')));
    assert.equal(snap.data.length, n % 4 === 0 ? 6 : 1);
    if (n % 4 === 3) assert.equal(snap.data[0].name, 'folder/PRIVATE-MUSIC');
  }
  assert.ok(!JSON.stringify({ exported, journal: h.journal.get('inputs') }).includes('PRIVATE-'));
  h.cache.close();
});

test('bare and filtered query caches remain distinct, and record/entity invalidation clears every slot', async () => {
  const h = seeded();
  await h.reader.list(path);
  await h.reader.query(path, {});
  await h.reader.query(path, { type: 'SFX' });
  assert.equal(inputs(h).length, 3);
  assert.equal((await h.cache.list()).filter(x => x.path === path).length, 3);
  await h.reader.list(path);
  await h.reader.query(path, {});
  await h.reader.query(path, { type: 'SFX' });
  assert.equal(inputs(h).length, 3, 'each slot hits independently');
  assert.equal(await h.cache.invalidateRecord('asset', 'asset-0'), 3);
  assert.equal((await h.cache.list()).length, 0);
  await h.reader.list(path);
  await h.reader.query(path, {});
  await h.reader.query(path, { type: 'SFX' });
  assert.equal(await h.cache.invalidateEntity('asset'), 3);
  assert.equal((await h.cache.list()).length, 0);
  h.cache.close();
});

test('real runner create keeps plain name safety reads and immutable before/after capture bodies', async () => {
  const h = seeded();
  await h.reader.list(path);
  await h.reader.query(path, { type: 'SFX' });
  h.runner.plan({
    dedupNames: true,
    items: [{ entity: 'asset', slot: 'create', name: 'NEW-REVIEW', srcId: 'new-review', data: { name: 'NEW-REVIEW', hidden: true, type: 'STATIC', url: 'u' } }],
    capture: { before: [{ proc: path, persist: 'local-only' }], after: [{ proc: path, persist: 'local-only' }] },
  }, { jobId: 'write' });
  await h.runner.run('write');
  assert.equal(jobOutcome(h.journal.get('write')), 'success');
  assert.equal(h.game.calls.filter(c => c.path === 'gameAsset.create').length, 1);
  const freshInputs = inputs(h).slice(2);
  assert.ok(freshInputs.length >= 4, 'before, dedup, reconciler and after reads occur');
  assert.ok(freshInputs.every(x => JSON.stringify(x) === '{}'));
  assert.equal(await h.cache.get(path, ''), null, 'create/fill invalidated the bare-list cache');
  assert.equal(await h.cache.getQuery(path, registry.canonicalKey({ type: 'SFX' })), null);
  const before = await h.cache.getSnapshot(snapshotKey('write', 'before', 0));
  const after = await h.cache.getSnapshot(snapshotKey('write', 'after', 0));
  assert.equal(before.data.length, 6);
  assert.equal(after.data.length, 7);
  assert.ok(!before.data.some(x => x.name === 'NEW-REVIEW'));
  assert.ok(after.data.some(x => x.name === 'NEW-REVIEW'));
  h.cache.close();
});

test('merge preserves main manifest policy/image-pack identity alongside tier counts', async () => {
  const mainTree = resolve(process.env.REVIEW_MAIN_TREE || resolve(root, '../base-b'));
  const { parseManifest: mainParse } = await import(pathToFileURL(resolve(mainTree, 'forge/src/runner/manifest.mjs')).href);
  for (const policy of [{}, { dedupNames: true }, { readBack: false }, { skipPreflight: true }, { imgSizes: { 'icon.webp': 4 } }]) {
    const input = { ...policy, items: [], capture: { after: [{ proc: 'gameAsset.get', input: { id: 'asset-0' }, persist: 'full' }] } };
    assert.equal(parseManifest(input).hash, mainParse(input).hash);
    assert.deepEqual(parseManifest(input).policy, mainParse(input).policy);
    assert.equal(parseManifest(input).tiers['repo-safe'], 1);
    assert.equal(parseManifest(input).fullCaptures, 1);
  }
  const pack = JSON.parse(readFileSync(resolve(root, 'archive/spent-manifests/push-2026-09-19/53_godstorm_failed_items_repair.json'), 'utf8'));
  const a = parseManifest(pack), b = mainParse(pack);
  assert.equal(a.hash, b.hash);
  assert.deepEqual(a.imagePack, b.imagePack);
  assert.deepEqual(a.policy, b.policy);
  const first = Object.keys(pack.imagePack.files)[0];
  pack.imagePack.files[first].sha256 = 'f'.repeat(64);
  assert.notEqual(parseManifest(pack).hash, a.hash);
  assert.equal(parseManifest(pack).hash, mainParse(pack).hash);
});
```
