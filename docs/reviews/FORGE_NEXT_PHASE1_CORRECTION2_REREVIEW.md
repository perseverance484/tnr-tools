# Forge Next Phase 1 — second correction pass re-review

**Verdict: PASS for the frozen correction target. FN3-R1, FN4-R1 and FN4-R2 are CLOSED.**

Date: 2026-09-20. Independent reviewer: ChatGPT, Engineering Auditor.

No blocking code defect remains in this bounded correction review. FN1, FN2 and FN5 remain closed. The frozen checkout passes 401 product tests and all 11 independent probe groups; generated artifacts reproduce byte-for-byte. The prior target fails eight of those probe groups, reproducing the three outstanding findings, while its three controls pass.

**This verdict closes the correction review at the exact SHA below. It is not verification of a merge with today's `main`. Nothing was merged, rebased, committed, pushed or released.** Current `main` and upstream game source have advanced since the handoff. Phase 1 remains unintegrated, and Phase 2 does not begin automatically.

## 1. Verified refs and scope

| Role | Verified value |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Frozen audit target | `9133145c1e626eb1611ac6a23302b58885c33fe6` |
| Prior correction target | `7bd8592f1d579f33d71c0713cfee4529cd691526` |
| Both implementation branch tips | `c7bdd2d2e7e5688d09361e4c665ca735277a03a6` |
| Branches | `fable/forge-next-phase1`, `claude/forge-next-phase1-uwhcn1` |
| Base / merge-base with current main | `77f02c30f7714eb8506ace8802904cb351a70d34` |
| Current main | `18c6a2554c1bf9231e00e46108a5a7faf66387aa` |
| Budget-only commit | `c12d693010db1a99c40c5c167a1592864d6fa7d7` |
| Canonical CI head | `dccd6274c27df9d4eb32becbf9cd4ebd69b48bd3` |
| Retained generated-contract / registry pin | `345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9` |
| Current upstream game main | `b78eadb9e817fd95ab6207768846fda0ea121019` |

Both branch tips were checked again after testing and remain at the handoff's tip. `9133145` to the CI head and to either branch tip changes only the second-correction handoff and the prior re-review Markdown files. The executable audit target is therefore also the executable CI target.

`c12d693` changes only `forge/tools/check_bundle_budget.mjs`. `9133145` changes the registry, runner, two test files, generated registry descriptor and root bundle. The additional changes since `7bd8592` include the already-reported documentation commits.

The governing `state/prompt_forge_next_phase1.md` and the operating/review documents checked against current `main` are unchanged. Initialization read current operational state, the router, relevant rulings, collaboration guides, Engineering Auditor role, review workflow, governing brief and handoffs. The session-open script was run in a separate checkout of current `main` so its ledger write did not alter the frozen target.

## 2. Closure evidence

| Finding | Disposition | Evidence |
| --- | --- | --- |
| FN3-R1 | **Closed** | Prefix overlaps fail actual manifest parsing and retained-declaration revalidation. Direct projection records the unsatisfied descendant instead of returning partial green evidence. |
| FN4-R1 | **Closed** | Identity includes full declared input types and enum members, global bounds/defaults/tier order, per-row paging descriptors and projection allowlists. Actual source-declaration variants change behavior and identity together. |
| FN4-R2 | **Closed** | New summary, persisted, failed and abandoned records retain policy through journal/export. Both phases and interrupted/retried queries pass. Existing saved provenance is preserved and unstamped legacy records remain unstamped. |

### FN3-R1 — overlapping projections

Source: [registry validation](https://github.com/perseverance484/tnr-tools/blob/9133145c1e626eb1611ac6a23302b58885c33fe6/forge/src/research/registry.mjs#L359), [projector](https://github.com/perseverance484/tnr-tools/blob/9133145c1e626eb1611ac6a23302b58885c33fe6/forge/src/research/registry.mjs#L403), and the unchanged [export revalidation](https://github.com/perseverance484/tnr-tools/blob/9133145c1e626eb1611ac6a23302b58885c33fe6/forge/src/core/results.mjs#L139).

Independent cases cover scalar leaves, scalar lists, null leaves, empty scalar lists, and leaves inside object arrays, in both declaration orders. Previously green retained snapshots with overlaps now produce failed, bodyless exports; this includes empty top-level arrays and empty nested collections, where declaration validation must enforce the rule without relying on traversal encountering a member.

Valid siblings, duplicate-path normalization, similarly named non-overlapping prefixes, explicit nested leaves and array shape remain valid. Undeclared synthetic fields never appear in the exported bundle. Structured terminals remain refused. No implementation correction is requested.

### FN4-R1 — policy identity

Source: [specification facts and policy derivation](https://github.com/perseverance484/tnr-tools/blob/9133145c1e626eb1611ac6a23302b58885c33fe6/forge/src/research/registry.mjs#L470).

The product suite's 13 fact-mutation probes pass. Independent probes additionally load isolated in-memory variants of the actual registry module, with its on-disk source unchanged. They change a numeric specification to boolean, remove an enum member, remove an enum-array member, change `MAX_PAGES`, change per-row maximum/default page limits, reorder the tier lattice and change the default tier. The altered modules exhibit the altered contract and a different revision. Reversing object key order leaves the revision stable; mutating returned policy facts does not mutate the live registry.

The identity is now `0657385d`, previously `35d2269b`. A deep comparison confirms all **15 registry rows**, tiers, defaults, page ceiling and source pin are unchanged between the two actual commits. No row was added, removed or retiered. The source-derived transport table is byte-identical. This closes the omitted-data finding without approving any privacy-policy widening.

The documented 32-bit FNV-1a limitation remains: this is a change-detection identity, not a cryptographic commitment. Passing sensitivity probes is not a proof of collision resistance. No stronger digest requirement is introduced by this review.

### FN4-R2 — capture and attempt stamps

Source: [summary/completed record creation](https://github.com/perseverance484/tnr-tools/blob/9133145c1e626eb1611ac6a23302b58885c33fe6/forge/src/runner/runner.mjs#L651) and [abandoned attempt creation](https://github.com/perseverance484/tnr-tools/blob/9133145c1e626eb1611ac6a23302b58885c33fe6/forge/src/runner/runner.mjs#L748).

Independent probes exercise successful and failed point/list/query summaries in both `before` and `after`; persisted repo-safe/projected/local-only captures; storage refusals; and actual `CachedReader` pagination interrupted by a second-page rate limit or network exception. For summary and local-only modes in both phases, two abandoned attempts keep exact page inputs and stamps, leave the completion cursor untouched, and survive a later successful retry. Raw private bodies and raw error messages remain absent from the exported evidence.

Successful persisted records agree with their retained snapshot policy. A saved `35d2269b` policy stays `35d2269b` when exported under the new build. Legacy full and summary records do not receive fabricated current provenance. The existing FN1/FN2/FN5 regression suite also passes; no closure is reopened.

## 3. Gates independently run

Runtime: Node `v24.19.0`, npm `11.9.0`; dependencies installed from the frozen lockfile with `npm ci --no-audit --no-fund`. Runtime audit was then run separately. Commands below ran from the frozen checkout's `forge/` unless stated otherwise.

| Command/check | Result |
| --- | --- |
| `npm test` | **401/401 pass**, zero failures/skips |
| Independent probe harness, frozen target | **11/11 pass** |
| Same harness, prior `7bd8592` target | **3 pass / 8 expected failures** reproducing FN3-R1/FN4-R1/FN4-R2 |
| `npm audit --omit=dev --audit-level=high` | 0 vulnerabilities |
| `node tools/check_imports.mjs` | 38 modules, 70 cross-layer imports, 0 violations |
| `node tools/check_boundaries.mjs` | 38 modules, original pin, 0 violations |
| `npm run fixtures` then `git diff --exit-code -- test/fixtures` | Clean; 14 screen fixtures and envelope fixtures byte-identical |
| `npm run build` then `git diff --exit-code -- ../forge_bundle.js` | Clean; checked bundle reproduced |
| `node tools/derive_registry.mjs` then `git diff --exit-code -- RESEARCH_REGISTRY.md` | Clean; descriptor reproduced |
| `node tools/check_bundle_budget.mjs` | Raw 453,086 / 466,000; gzip 89,296 / 92,000 |
| `checkReleasePin()` from `tools/check_release_pin.mjs` | Clean |
| Final `git status --porcelain` in frozen checkout | Empty |

[Canonical CI run 35267833732](https://github.com/perseverance484/tnr-tools/actions/runs/35267833732), job `verify` / `105359335508`, was independently read from GitHub: completed-success, all 12 listed setup/gate steps successful, none skipped. Its head is `dccd627`; only two Markdown files differ from `9133145`. No CI rerun was requested.

The independent harness uses actual product parser, runner methods, capture cache, paged reader and result materialization with `fake-indexeddb`, synthetic data and injected transport. It forbids `fetch` and socket connections. The full suite also passes its network-safety gate. Neither run used live game transport.

## 4. Non-blocking documentation correction

The handoff §5 and [budget comment](https://github.com/perseverance484/tnr-tools/blob/9133145c1e626eb1611ac6a23302b58885c33fe6/forge/tools/check_bundle_budget.mjs#L47) label **+6,714 raw / +1,846 gzip** as growth over the previous correction pass. Those are cumulative figures from the original implementation `8f15416`, not from `7bd8592`.

Measurements using the same Node gzip implementation and level 9 as the gate:

| Commit | Raw bytes | Gzip bytes |
| --- | ---: | ---: |
| `8f15416` | 446,372 | 87,450 |
| `7bd8592` | 452,000 | 88,963 |
| `c12d693` | 452,000 | 88,963 |
| `9133145` | 453,086 | 89,296 |

The second correction's actual increment is **+1,086 raw / +333 gzip**. Relabel the larger delta as cumulative from `8f15416`, or replace it with the actual second-pass delta in the next documentation update. The final size, budget-only commit isolation and stated utilization are correct. This does not reopen a code finding or require changing the frozen target.

## 5. Current-state and integration limits

The handoff's “main is `015583b`, state/archive only, no overlap” statement is historical. Current `main` is `18c6a25` and includes Forge 0.5.1 / Presentation Studio P0/P1 work. Ten paths changed on both branches since `77f02c3`:

```text
forge/src/budget/reader.mjs
forge/src/core/facts.mjs
forge/src/runner/manifest.mjs
forge/src/runner/runner.mjs
forge/src/ui/screens.mjs
forge/test/fakegame.mjs
forge/test/screen_scenarios.mjs
forge/tools/check_boundaries.mjs
forge/tools/check_bundle_budget.mjs
forge_bundle.js
```

This is a changed-path intersection, not a claim that Git necessarily reports ten textual conflicts. No trial merge was performed. In particular, the frozen bundle ceilings belong to the reviewed historical branch; this review does not authorize replacing main's newer 354,000 / 78,000 ratchet with those older, larger ceilings.

Current operational state still says Phase 1 implementation “has not begun.” The verified frozen implementation exists on both named branches. That description needs reconciliation when the workstream state is next updated; it should not cause these completed corrections to be implemented again. The current ruling placing Forge Next Phase 1 ahead of Presentation Studio P2 remains respected.

The upstream game-source head has also moved: the live ref is `b78eadb9e817fd95ab6207768846fda0ea121019`, not the handoff's `1fd355ab92cec78148130e02c8d38834836c3181`. The frozen registry still uses `345d18ac`. This narrow pass carries forward the original source audit for the unchanged admission rows and transport facts; it does **not** assert contract equivalence to the new upstream head. Recheck relevant source drift before integration and split any needed pin adoption into its own reviewed task.

The required session-open routine on current `main` remains red only on its pre-existing parity adapter: `validate.py:201` calls `set()` on an inbox bundle's `checks: null` and raises `TypeError`. Lawmap reports 0 errors / 5 existing warnings; doctrine and packs/TOCs are current. This baseline problem is separate from the frozen Forge test gates and was neither repaired nor reported green.

## 6. Open decisions and next step

The two user-owned choices remain safely deferred under the unchanged narrow policy:

1. Whether `combat.getBattleHistory` may project player-identifying fields into repository evidence.
2. Whether the name-list rows should become repo-safe.

Neither requires reopening these corrections while the rows stay local-only with no new export permission.

**Next permitted work:** Fable can record the three closures, reconcile with fresh `main`, resolve the overlapping implementation/build surfaces while preserving integrated work, check relevant upstream drift without silently moving the source pin, and return a new frozen combined SHA with current gates/CI. Review the synchronization delta before integration. The reviewed code at `9133145` needs no additional fix for FN3-R1/FN4-R1/FN4-R2.

No real browser, installed userscript, real IndexedDB, Clerk session, live clipboard interaction or production transport was exercised. Real-device and live-session behavior remains unverified. Live-game requests: **0**. Live-game writes: **0**. Live credentials acquired/requested/used: **none**. Remote repository mutations: **none**. Phase 2, Quest Studio integration, Content Admin, Publish, Project Workspace, Builder retirement and game-source pin adoption: **not performed**.

## Appendix — reproducible independent probes

The complete harness follows. Save it as `correction2-probes.mjs`, install the checkout's lockfile dependencies, and run against an absolute checkout path:

```sh
REVIEW_TREE=/absolute/path/to/tnr-tools node --test correction2-probes.mjs
```

Actual commands in this session:

```sh
REVIEW_TREE=/workspace/scratch/8d87e116afce/tnr-tools node --test /workspace/scratch/8d87e116afce/review-evidence/correction2-probes.mjs
REVIEW_TREE=/workspace/scratch/8d87e116afce/previous node --test /workspace/scratch/8d87e116afce/review-evidence/correction2-probes.mjs
```

The prior checkout used the same installed dependency tree through a local symlink. No probe modified either checkout's source. Baseline failure is intentional evidence that the checks distinguish the original defects from their correction.

```javascript
import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { pathToFileURL } from 'node:url';
import { createRequire } from 'node:module';
import { Socket } from 'node:net';

globalThis.fetch = () => { throw new Error('NETWORK_FORBIDDEN_IN_REVIEW'); };
Socket.prototype.connect = () => { throw new Error('SOCKET_FORBIDDEN_IN_REVIEW'); };
const root = pathToFileURL(process.env.REVIEW_TREE + '/');
const load = p => import(new URL('forge/' + p, root));
const registryURL = new URL('forge/src/research/registry.mjs', root);
const reg = await import(registryURL);
const { parseManifest } = await load('src/runner/manifest.mjs');
const { Runner } = await load('src/runner/runner.mjs');
const { CaptureCache } = await load('src/storage/captures.mjs');
const { CachedReader } = await load('src/budget/reader.mjs');
const { RateLimited } = await load('src/budget/bucket.mjs');
const { materialize, resolveCaptures, buildBundle } = await load('src/core/results.mjs');
const { IDBFactory } = createRequire(new URL('forge/package.json', root))('fake-indexeddb');
const SECRET = 'SYNTHETIC-PRIVATE-CORRECTION2';
const build = (job, captures) => buildBundle({version:'independent-review', now:()=>1000, storage:{getItem:()=>null}}, job, captures);
const capture = (value, phase='after') => parseManifest({capture:{[phase]:[value]}}).capture[phase][0];
function host(reader={}) {
  const job = {jobId:'review', state:'RUNNING', items:[]};
  const journal = {get:()=>job, annotateJob(_id, patch){Object.assign(job, structuredClone(patch));}};
  const cache = new CaptureCache(new IDBFactory(), ()=>1000);
  return {job, journal, cache, reader, _requireAuth(){}, _persist:Runner.prototype._persist, _journalAttempt:Runner.prototype._journalAttempt};
}
async function bundle(h) { return build(h.job, await resolveCaptures(h, 'review')); }
async function variant(search, replacement) {
  const source = readFileSync(registryURL, 'utf8');
  assert.equal(source.split(search).length, 2, 'variant must replace one real declaration');
  const changed = source.replace(search, replacement).replace(/from "(\.\.?\/[^\"]+)"/g,
    (_m,spec)=>'from '+JSON.stringify(new URL(spec,registryURL).href));
  return import('data:text/javascript;base64,'+Buffer.from(changed).toString('base64'));
}
const overlapCases = [
  [{id:'q1'}, ['id','id.deeper']],
  [{tags:['a','b']}, ['tags','tags.deeper']],
  [{content:{objectives:[{id:'n1'},{id:'n2'}]}}, ['content.objectives.id','content.objectives.id.deeper']],
  [{id:null}, ['id','id.a.b']],
  [{tags:[]}, ['tags','tags.deeper']],
];

test('FN3-R1: actual parser refuses overlaps in both orders; valid siblings and dedup survive',()=>{
  for(const [,fields] of overlapCases) for(const projection of [fields,[...fields].reverse()]) {
    assert.throws(()=>capture({proc:'quests.get',input:{id:'q1'},persist:'projected',projection}),/overlap/);
  }
  const c = capture({proc:'quests.get',input:{id:'q1'},persist:'projected',projection:['content.a','content.b','contentious','content.a']});
  assert.deepEqual(c.projection,['content.a','content.b','contentious']);
});

test('FN3-R1: direct projector reports every unsatisfied deeper path with no partial body',()=>{
  for(const [body,fields] of overlapCases) for(const projection of [fields,[...fields].reverse()]) {
    const result=reg.projectBody(body,projection);
    assert.equal(result.ok,false,JSON.stringify(projection));
    assert.deepEqual(result.missing,[fields[1]]);
    assert.equal('data' in result,false);
  }
});

test('FN3-R1: a previously green overlapping snapshot becomes a failed export including empty bodies',async()=>{
  for(const [body,projection] of [...overlapCases,[[],['id','id.deeper']],[{content:{objectives:[]}},['content.objectives.id','content.objectives.id.deeper']]]) {
    const h=host();
    const c={phase:'after',proc:'quests.get',ok:true,persist:'projected',tier:'projected',snapshotKey:'s',projection,persistOk:true};
    h.job.state='DONE'; h.job.capturesAfter=[c];
    await h.cache.putSnapshot({key:'s',jobId:'review',phase:'after',ordinal:0,path:'quests.get',data:body,tier:'projected',projection});
    const out=await bundle(h);
    assert.equal(out.captures[0].persistOk,false);
    assert.match(out.captures[0].persistError,/overlap/);
    assert.equal('data' in out.captures[0],false);
    assert.equal(out.outcome,'failed');
  }
});

test('FN3 controls: ordinary nested leaves preserve shape, no implicit subtree or secret',async()=>{
  const body={id:'q1',tags:['a'],id2:'other',content:{groups:[{name:'g1',hidden:SECRET,leaves:[{id:'l1',hidden:SECRET}]},{name:'g2',leaves:[]}]}};
  const projection=['id','id2','tags','content.groups.name','content.groups.leaves.id'];
  const c=capture({proc:'quests.get',input:{id:'q1'},persist:'projected',projection});
  const h=host({get:async()=>({ok:true,data:body})});
  await Runner.prototype._captures.call(h,'review',[c],'after'); h.job.state='DONE';
  const out=await bundle(h);
  assert.equal(out.outcome,'success');
  assert.deepEqual(out.captures[0].data,{id:'q1',id2:'other',tags:['a'],content:{groups:[{name:'g1',leaves:[{id:'l1'}]},{name:'g2',leaves:[]}]}});
  assert.equal(JSON.stringify(out).includes(SECRET),false);
  assert.equal(reg.projectBody(body,['content']).ok,false);
});

test('FN4-R1: changing the actual number specification changes both admission and revision',async()=>{
  const v=await variant('secondsBack: NUM','secondsBack: BOOL');
  assert.deepEqual(reg.canonicalInput('combat.getBattleHistory',{secondsBack:10}),{secondsBack:10});
  assert.throws(()=>v.canonicalInput('combat.getBattleHistory',{secondsBack:10}),/boolean/);
  assert.deepEqual(v.canonicalInput('combat.getBattleHistory',{secondsBack:true}),{secondsBack:true});
  assert.notEqual(v.REGISTRY_REVISION,reg.REGISTRY_REVISION);
});

test('FN4-R1: actual enum and enum-array membership changes change admission and revision',async()=>{
  const variants=[
    ['oneOf("all", "user", "opponents")','oneOf("all", "user")','combat.getBattleEntries',{battleId:'b1',userFilter:'opponents'}],
    ['"RANKED_PVP", "RANKED_SPARRING", "RAID", "OVERWORLD"','"RANKED_PVP", "RANKED_SPARRING", "RAID"','combat.getBattleHistory',{combatTypes:['OVERWORLD']}],
  ];
  for(const [search,replacement,path,input] of variants){
    const v=await variant(search,replacement);
    assert.deepEqual(reg.canonicalInput(path,input),input);
    assert.throws(()=>v.canonicalInput(path,input),/one of/);
    assert.notEqual(v.REGISTRY_REVISION,reg.REGISTRY_REVISION);
  }
});

test('FN4-R1: actual global and row bounds, defaults and tier ordering change the revision',async()=>{
  const variants=[
    ['export const MAX_PAGES = 20;','export const MAX_PAGES = 19;',v=>assert.equal(v.MAX_PAGES,19)],
    ['defaultLimit: 30, maxLimit: 500','defaultLimit: 30, maxLimit: 499',v=>assert.equal(v.pageContract('combat.getBattleEntries').maxLimit,499)],
    ['defaultLimit: 30, maxLimit: 500','defaultLimit: 31, maxLimit: 500',v=>assert.equal(v.pageSize('combat.getBattleEntries',{battleId:'b1'}),31)],
    ['Object.freeze(["local-only", "projected", "repo-safe"])','Object.freeze(["projected", "local-only", "repo-safe"])',v=>assert.equal(v.tierAtMost('projected','local-only'),true)],
    ['export const DEFAULT_RESEARCH_TIER = "local-only";','export const DEFAULT_RESEARCH_TIER = "projected";',v=>assert.equal(v.researchRow('quests.getAllNames').tier,'projected')],
  ];
  const seen=new Set([reg.REGISTRY_REVISION]);
  for(const [search,replacement,check] of variants){
    const v=await variant(search,replacement); check(v);
    assert.equal(seen.has(v.REGISTRY_REVISION),false); seen.add(v.REGISTRY_REVISION);
  }
  if(reg.policyFacts){
    const facts=reg.policyFacts();
    const reverseKeys=v=>Array.isArray(v)?v.map(reverseKeys):v&&typeof v==='object'?Object.fromEntries(Object.entries(v).reverse().map(([k,val])=>[k,reverseKeys(val)])):v;
    assert.equal(reg.revisionOf(reverseKeys(facts)),reg.REGISTRY_REVISION);
    facts.rows[0].input.required.id.t='boolean';
    assert.equal(reg.policyFacts().rows[0].input.required.id.t,'string','facts must be detached from live policy');
  }
});

test('FN4-R2: point, list and query summaries, successful and failed, carry stamps in both phases',async()=>{
  const declarations=[{proc:'quests.get',input:{id:'q1'}},{proc:'quests.getAllNames'},{proc:'combat.getBattleHistory',input:{secondsBack:10}}];
  for(const phase of ['before','after']) for(const declaration of declarations) for(const ok of [true,false]) {
    const c=capture({...declaration,persist:'summary'},phase);
    const result=ok?{ok:true,complete:true,data:[{raw:SECRET}],pages:[],rowCount:1}:{ok:false,complete:false,error:{code:'NOT_FOUND',message:SECRET},pages:[],rowCount:0};
    const h=host({get:async()=>result,list:async()=>result,query:async()=>result});
    await Runner.prototype._captures.call(h,'review',[c],phase); h.job.state='DONE';
    const out=await bundle(h);
    assert.deepEqual(h.job[phase==='before'?'capturesBefore':'capturesAfter'][0].policy,reg.capturePolicy(c.proc));
    assert.deepEqual(out.captures[0].policy,reg.capturePolicy(c.proc));
    assert.equal('data' in out.captures[0],false);
    assert.equal(JSON.stringify(out).includes(SECRET),false);
  }
});

test('FN4-R2: persisted and failed-storage records retain capture policy, export never widens',async()=>{
  for(const persist of ['repo-safe','projected','local-only']) for(const failedStore of [false,true]){
    const c=capture({proc:'quests.get',input:{id:'q1'},persist,...(persist==='projected'?{projection:['id']}:{})});
    const h=host({get:async()=>({ok:true,data:{id:'q1',other:'body'}})});
    if(failedStore) h.cache.putSnapshot=async()=>{throw new Error('synthetic quota');};
    await Runner.prototype._captures.call(h,'review',[c],'after'); h.job.state='DONE';
    const out=await bundle(h),r=out.captures[0];
    assert.deepEqual(r.policy,reg.capturePolicy(c.proc));
    if(failedStore){assert.equal(r.persistOk,false);assert.equal('data'in r,false);continue;}
    assert.deepEqual((await h.cache.getSnapshot('review::after::0')).policy,r.policy);
    assert.equal(r.persistOk,true);
    if(persist==='local-only')assert.equal('data'in r,false);
    else assert.deepEqual(r.data,persist==='projected'?{id:'q1'}:{id:'q1',other:'body'});
  }
});

test('FN4-R2/FN5: real reader late-page failures and two retries keep stamped attempts and resume cursor',async()=>{
  for(const phase of ['before','after']) for(const persist of ['summary','local-only']) for(const errorKind of ['rate','network']){
    const c=capture({proc:'combat.getBattleEntries',input:{battleId:'b1',limit:2},persist,pages:3},phase);
    const h=host(),key=phase==='before'?'capturesBefore':'capturesAfter';
    let count=0,success=false;const inputs=[];
    h.reader=new CachedReader({cache:h.cache,budget:{acquire:async()=>{},observe(r){if(!r[0].ok)throw new RateLimited({path:c.proc,until:2000});}},client:{batch:async calls=>{
      inputs.push(structuredClone(calls[0].input));count++;
      if(success)return [{ok:true,data:[{id:'final',raw:SECRET}]}];
      if(count%2)return [{ok:true,data:[{id:'one',raw:SECRET},{id:'two',raw:SECRET}]}];
      if(errorKind==='network')throw Object.assign(new Error(SECRET),{name:'NetworkFailure'});
      return [{ok:false,error:{code:'TOO_MANY_REQUESTS',httpStatus:429,message:SECRET}}];
    }}});
    for(let i=0;i<2;i++){
      await assert.rejects(()=>Runner.prototype._captures.call(h,'review',[c],phase));
      assert.equal(h.job[key],undefined);assert.equal(h.job[key+'Partial'],undefined);
      const attempts=h.job[key+'Attempts'];assert.equal(attempts.length,i+1);
      assert.deepEqual(attempts[i].policy,reg.capturePolicy(c.proc));
      assert.deepEqual(attempts[i].pages.map(p=>p.input),inputs.slice(i*2,i*2+2));
      assert.deepEqual(attempts[i].pages.map(p=>p.ok),[true,false]);
      assert.equal(attempts[i].persistOk,false);
    }
    const attempts=structuredClone(h.job[key+'Attempts']);h.job.state='PAUSED';
    const paused=await bundle(h);assert.equal(paused.outcome,'open');
    assert.equal(JSON.stringify(paused).includes(SECRET),false);
    success=true;h.job.state='RUNNING';
    await Runner.prototype._captures.call(h,'review',[c],phase);h.job.state='DONE';
    assert.deepEqual(h.job[key+'Attempts'],attempts);
    const complete=await bundle(h);assert.equal(complete.outcome,'success');
    assert.equal(complete.captures.length,3);
    for(const r of complete.captures)assert.deepEqual(r.policy,reg.capturePolicy(c.proc));
    assert.equal(JSON.stringify(complete).includes(SECRET),false);
  }
});

test('FN1/FN4: restored legacy and prior-revision records never acquire the current policy',async()=>{
  const c={phase:'after',proc:'quests.get',ok:true,persist:'full',persistOk:true,snapshotKey:'old'};
  const snap={path:'quests.get',data:{id:'q1'}};
  const old=await materialize({getSnapshot:async()=>snap},c);
  assert.deepEqual(old.data,{id:'q1'});assert.equal('policy'in old,false);
  const prior={...reg.capturePolicy('quests.get'),registry:'35d2269b'};
  const saved=await materialize({getSnapshot:async()=>({...snap,policy:prior})},{...c,policy:prior});
  assert.deepEqual(saved.policy,prior);
  const unstampedSummary={phase:'after',proc:'combat.getBattleHistory',ok:true};
  assert.equal('policy'in await materialize({},unstampedSummary),false);
});
```

### Actual frozen-target probe output

```text
✔ FN3-R1: actual parser refuses overlaps in both orders; valid siblings and dedup survive (3.103268ms)
✔ FN3-R1: direct projector reports every unsatisfied deeper path with no partial body (0.706941ms)
✔ FN3-R1: a previously green overlapping snapshot becomes a failed export including empty bodies (14.408882ms)
✔ FN3 controls: ordinary nested leaves preserve shape, no implicit subtree or secret (2.154802ms)
✔ FN4-R1: changing the actual number specification changes both admission and revision (4.901426ms)
✔ FN4-R1: actual enum and enum-array membership changes change admission and revision (7.717921ms)
✔ FN4-R1: actual global and row bounds, defaults and tier ordering change the revision (14.370145ms)
✔ FN4-R2: point, list and query summaries, successful and failed, carry stamps in both phases (2.854262ms)
✔ FN4-R2: persisted and failed-storage records retain capture policy, export never widens (4.499824ms)
✔ FN4-R2/FN5: real reader late-page failures and two retries keep stamped attempts and resume cursor (10.733662ms)
✔ FN1/FN4: restored legacy and prior-revision records never acquire the current policy (0.466056ms)
ℹ tests 11
ℹ suites 0
ℹ pass 11
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 194.2733
```

### Actual product-suite summary

```text
ℹ tests 401
ℹ suites 0
ℹ pass 401
ℹ fail 0
ℹ cancelled 0
ℹ skipped 0
ℹ todo 0
ℹ duration_ms 10451.222926
```
