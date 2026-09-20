# Forge Presentation Studio P1 correction — independent re-review

**Verdict: changes requested. The original reproductions are addressed, but F3 and F4/F5 remain partially open through R1–R3 below. P0 remains sound and unchanged. Do not integrate the combined head or start P2 yet.**

Reviewed on 2026-09-20. Live-game requests **0**; live-game writes **0**; asset-CDN requests **0**. This review changes only its report and session-state records on a ChatGPT-owned branch. It changes no implementation, capture, art, manifest, or Fable branch ref.

| Ref | Independently verified value |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Live main, intended base, merge-base | `eefefd1afd67111a90c332951a8dd9f83cb99cbd` |
| Fable branch | `claude/forge-presentation-studio-p1-y1wbiq` |
| Frozen remote/local head | `ac792ef1085c8350fda7bf79050d90ca0ce41879` |
| Commits above base | `05e71564d693a8505f98df4400502abee7517a3c` (P0), `8830443977122253a956fb77392a7d2925d6cb6f` (P1), `ac792ef1085c8350fda7bf79050d90ca0ce41879` (correction) |
| Review branch, based on frozen head | `chatgpt/review-forge-presentation-studio-p1-r2` |
| Previous review | `chatgpt/review-forge-presentation-studio-p1@9a9a3ea03d56cdcd1f6cf40f75d73c5ba4b2d985` |
| Governing plan | `chatgpt/forge-presentation-studio-plan@99f1aa8a6fe7cc7361aa613cdcad258bafb9c83e`, `docs/plans/FORGE_PRESENTATION_STUDIO_UPGRADE_PLAN.md` |
| Separate design proposal | `chatgpt/forge-presentation-studio-design@4532ef917a1dfb40d00c554fd7f065e13216afc7` |
| Pinned game source | `studie-tech/TheNinjaRPG@345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9` |

Current main and its routed context were reconstructed before review. The review follows `CHATGPT.md`, `docs/DEVELOPMENT_WORKFLOW.md`, and `docs/workflows/FABLE_REVIEW.md`, with Content Designer leading and Engineering Auditor, UI/UX Reviewer, and Art Director supporting. The design contract remains a proposal awaiting director acceptance; draft layout preferences are not P1 gates.

The correction changes 17 files, all presentation modules, package documents, or presentation tests. Because selection and traversal now feed several consumers, the affected P1 surface was re-reviewed together. Runtime/build/tooling, lockfile, loader, and checked bundle are unchanged from the previously reviewed head.

## Closure of the first review

The [first report](https://github.com/perseverance484/tnr-tools/blob/9a9a3ea03d56cdcd1f6cf40f75d73c5ba4b2d985/docs/reviews/REVIEW_2026-09-20_forge_presentation_studio_p0_p1.md) remains evidence for that earlier SHA, not an integration source.

| Finding | Current result |
| --- | --- |
| F1: unverifiable bound art accepted | **Closed.** Unavailable blobs or a missing verifier no longer imply verified/renderable bytes; bound-but-unverified art is fatal. |
| F2: invalid/non-capture evidence accepted | **Original admission defects closed.** Selection now requires supported procedure, successful response, matching entity, full persistence, and required presentation fields; missing publication state is refused. The individually valid Marrow capture remains usable despite its failed overall run. This is not full server-schema validation. |
| F3: unpinned/stale/conflicting selection | **Partial.** Immutable commit/file hashes, explicit quest selectors, per-entity capture times, and draft refusal address the original cases. Duplicate quest selections and name-only conflicts remain: R1 and R2. |
| F4: storage order mistaken for route | **Partial.** Array permutations and moving the entry no longer change the facts. Mixed-edge traversal still produces an invalid success order and cadence: R3. |
| F5: optional exit mistaken for full clear | **Partial.** The original optional-exit/failure-payout cases are classified separately, and branching clear rewards are refused. Full-clear ordering still inherits R3. |
| F6: stale names and unchanged-ID text drift | **Closed for the original defects.** Tower/Dawnless sentence-start cases fail; changed source text under an unchanged objective ID invalidates `sourceDigest`. There is a nonblocking wording false positive below. |
| F7: ignored quest/scene bindings | **Closed.** Accepted bindings are resolved or explicitly rejected, including unsupported/missing scene records; invalid bindings cannot disappear from lint. |

## R1 — High: duplicate quest selections corrupt totals and let old captures overwrite current facts

**Confirmed defect; residual F3.** [dossier.mjs:40](https://github.com/perseverance484/tnr-tools/blob/ac792ef1085c8350fda7bf79050d90ca0ce41879/forge/presentation/dossier.mjs#L40), reward pairing at line 92, assembly/totals at lines 177–201. Plan §§4.1, 5.1, 5.3 require coherent facts from selected current evidence.

The loader ensures unique evidence-record IDs and one matching capture *within each record*. It does not ensure one selected current record per quest ID. Assembly appends every record to `structures`, encounters, locations, and totals, but overwrites the quest-ID-keyed maps and provenance. Rewards additionally use `structures.find`, which selects the first structure for the quest ID while later iterations supply later quest data.

Two reproductions require **no edits to captured bytes, immutable source refs, or source digests**:

1. Copy the `marrow-quest` package entry with another record ID. Lint passes with **3 components, 75 battles, 15 keepers, 18 AIs** and duplicate Marrow locations, while `dossier.structure` contains only two quest IDs.
2. Keep the current Stormcourt entry and add its older capture from `tnr_results_1789829183863.json`, selected by `at:2026-09-19T14:46:23.796Z` and `snapshotKey:52-mu8i2pd8::after::3`. Place the older entry last. Omit the optional Stormcourt story block so its independent digest guard does not mask selection behavior. Lint passes with the same inflated totals and current structure named **“The Tower of Endless Night: The Stormcourt”**, sourced to the older entry. Locations now contain Marrow Vaults, Stormcourt, and the old Tower name.

Keeping the golden story does catch a narrative digest mismatch, but factual source selection cannot depend on an optional summary being present. Both competing captures are otherwise individually admissible and already committed. This is not a failure of the new byte lock; it is a failure to resolve or reject overlapping selections.

**Smallest correction:** refuse multiple current quest selections for one quest ID before assembly, with both record/capture pointers in the error. If overlapping historical observations are retained, select one authoritative current record once and use that same record for structure, rewards, dialogue, images, locations, and provenance. Never count observation records as additional components. Reordering records must not change which facts win. Regress both cases above.

## R2 — Medium: equal-time name conflicts are silently resolved by array order

**Confirmed defect; residual F3.** [evidence.mjs:325](https://github.com/perseverance484/tnr-tools/blob/ac792ef1085c8350fda7bf79050d90ca0ce41879/forge/presentation/evidence.mjs#L325) and [evidence.mjs:384](https://github.com/perseverance484/tnr-tools/blob/ac792ef1085c8350fda7bf79050d90ca0ce41879/forge/presentation/evidence.mjs#L384). Plan §§4.1–4.3 require sourced entity names/identity; the correction explicitly promises conflict-aware selection.

Both within-record and across-record merging detect an equal-timestamp disagreement only when the **image URL** differs. An equally authoritative name disagreement is ignored.

**Reproduced:** duplicate Warden of the Half Eclipse's successful full capture (`3XMsIV6Yv4jy-uaJAe52f`, timestamp `2026-09-14T16:20:36.505Z`), preserve its entity ID and avatar URL, give it another snapshot key and the name `Alternate Keeper`. Put it first within the old bundle, or in the newer bundle whose AI evidence entry is selected first. In both cases lint passes, the roster remains resolved, and `Alternate Keeper` wins with no conflict. The tests simulate these changed captures as committed evidence; they do not bypass the working-file digest check.

**Smallest correction:** compare every presentation fact consumed from tied observations, including name and image URL, in both merge paths. Equivalent observations can coalesce; disagreeing observations require an explicit resolving selection or a fatal conflict. A snapshot-key or source-record ordering difference is not evidence that one name is current. Cover AI and game-asset names and ties within/across records.

## R3 — Medium: all-edge BFS is reused as success-route order and cadence

**Confirmed defect; residual F4/F5.** [structure.mjs:139](https://github.com/perseverance484/tnr-tools/blob/ac792ef1085c8350fda7bf79050d90ca0ce41879/forge/presentation/structure.mjs#L139), success-path assembly at line 201; [rewards.mjs:77](https://github.com/perseverance484/tnr-tools/blob/ac792ef1085c8350fda7bf79050d90ca0ce41879/forge/presentation/rewards.mjs#L77); [dossier.mjs:73](https://github.com/perseverance484/tnr-tools/blob/ac792ef1085c8350fda7bf79050d90ca0ce41879/forge/presentation/dossier.mjs#L73). Plan §§5.1–5.3 require graph-derived sequence and reward semantics.

`successPath` correctly filters membership to nodes that can reach a win through success edges, but preserves the traversal order of a BFS that also follows **failure** edges. Membership does not make that ordering a valid success route. `successPathLinear` checks successor counts, so it can still be true. Rewards choose the last payout in that mixed order. Separately, cadence uses all reachable encounters rather than only the supported success route.

**Reproduction A:** retain every normal Marrow success link. Set `b1_1.failObjectiveId` to `d5_victory`, and add a 20,000-ryo intermediate reward at `d3_1`. This graph still has one entry, all 53 nodes reachable, and no cycle. The actual success route visits `d3_1`, then `d5_victory`, then `win`.

Lint passes, but the reported success order starts `d1_1, b1_1, d1_2, d5_victory, b1_2, win, ...`. It calls **`d3_1` / 20,000 ryo the full-clear reward**, demotes the actual **125,000 ryo / 25 tokens / 10 prestige** victory reward to intermediate, and reports `successPathLinear:true`. The 145,000 route total is valid in this particular example; the defect is ordering and full-clear classification, not that sum.

This is an acyclic supported failure link, not a malformed dangling edge: the [pinned flow validator](https://github.com/studie-tech/TheNinjaRPG/blob/345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9/app/src/libs/quest.ts#L1881) includes `failObjectiveId` in graph edges and requires a unique start, valid references, reachability, and no cycles. An independent scratch graph check confirmed those properties. The game source was read, not executed.

**Reproduction B:** add an opening optional battle that leads only to `fall`, while preserving the normal clear route. The dossier reports `successPathLinear:true` and `cadence.exact:true`, but its sequence begins with that optional battle followed by the normal opening battles. Its cadence starts with **five** recurring fights before the first keeper, though the success route remains four. A player cannot traverse that combined sequence. The count of 26 distinct reachable battles is itself valid; it must not be presented as one playable sequence.

**Smallest correction:** derive route ordering on the success-edge graph independently of all-node reachability. Use the same explicitly supported route for full-clear classification and cadence; keep alternative/failure encounters separately identifiable. Refuse a single-sequence/full-clear claim when the graph does not support it. Preserve the existing Godstorm victory-dialogue-before-zero-reward-terminal behavior, and test both cross-route failure links and optional battles.

## Nonblocking observations and scope limits

- **Needs refinement — narrative wording:** prefixing the unchanged valid Marrow summary with `Ultimately, ` is fatal because `Ultimately` is treated as an unsupported name. The finite ordinary-word list is an editorial constraint, not a semantic guarantee. Refine this before author-facing narrative UI while preserving the stale-name and fingerprint guards. No automatic semantic judging is requested.
- **Graph hardening:** `b2_1.failObjectiveId = b1_1` creates a rooted cycle, yet lint still passes with a linear 4+1 cadence. The new rootless-cycle test does not cover it. The pinned server rejects such a cycle, so this is a malformed/historical-input limitation rather than evidence of a current Godstorm defect. Include rooted-cycle handling when repairing route validation; R3's blocking reproductions above are acyclic.
- **Exact art:** default lint is evidence inspection, not complete render readiness. The registry now includes 23 entities and verifies bytes for five portraits; 18 entries remain unbound (13 portraits, two quest listing images, three Marrow scene images). Strict exact-byte lint correctly refuses them. A requested scene without selected asset evidence is also refused. Scene assets remain separate from locations.
- The README now correctly acknowledges the committed source archive at `1bca57eeb0c1836a49334dc2f49196a5a3db24c7` and defers its resolver. The first review's 19-file hash/length/dimension/decode verification and entity/URL joins remain separately pinned evidence; this correction changes no archive/capture/art bytes. No claim of a fresh remote-image fetch is made. Archive resolution, approved-derivative handling, and MIME/dimensions remain explicit pre-renderer contract work; no new poster, renderer, Android UI, or binary duplication is requested here.
- The design proposal's acceptance and later Android export/share behavior remain outside this P1 review. No director decision blocks R1–R3.

## Verification

Node `v24.19.0`; npm `11.9.0`. Dependencies installed using `npm ci --offline --ignore-scripts` from the unchanged lockfile. Repository and dependency-audit access was used; no game or asset-CDN access was used.

| Check | Result at the frozen head |
| --- | --- |
| `cd forge && npm test` | **511 passed, 0 failed, 0 skipped** |
| `npm run build`; checked bundle diff | Pass; byte-identical artifact |
| `npm run fixtures`; envelope/screens diffs | Pass; no drift; 14 screen fixtures regenerated |
| Import gate | 40 modules, 71 cross-layer imports, 0 violations |
| Boundary gate | 40 source + 13 presentation modules, 0 violations |
| Bundle budget | **339,669 / 354,000 raw; 74,926 / 78,000 gzip** |
| Release-pin check | Clean |
| `npm audit --omit=dev --audit-level=high` | 0 vulnerabilities |
| Default Godstorm CLI | Exit 0; **0 fatal / 22 warnings** |
| Godstorm CLI `--require-exact-bytes` | Expected exit 1; **18 fatal / 4 warnings**; incomplete byte resolution |
| Independent scratch probes | 19 control/adversarial cases completed; remaining false acceptances documented above |
| `harvest.py verify harvests/inbox/tnr_results_1789842714086.json` | Verified, exit 0; 9 OK, no failed/unverified/skipped items |
| Session guards | Lawmap 0 errors / 5 existing warnings; doctrine and packs current; baseline parity adapter remains red |

The unchanged golden package still produces two pyramids, 50 battles, 18 distinct AIs, 10 keepers, 4+1 repeated five times per pyramid, rewards 125,000/25/10 and 250,000/150/60, no intermediate cash-outs or reward items, and both quests hidden. These facts describe the selected committed captures, not a new live check.

The session parity adapter still fails on the existing Forge bundle's `checks:null` (`validate.py` attempts to iterate it). This was present at base main and is outside the correction. The dedicated harvest verifier succeeds. No green global parity guard is claimed; the defect was not repaired during review.

P0's expanded-contract equivalence and pinned regeneration were established in the previous review. Its inputs and implementation did not change here; the normal build, test, fixture, budget, boundary, import, and release gates were rerun. Presentation code remains outside the runtime bundle.

## Reproduction recipes

Scratch command used: `node /workspace/scratch/9b09e6cf21d0/evidence/p1-r2-review-attacks.mjs`. Scratch files are not committed. The frozen tree's `scenario()` isolates temporary roots. Its `files` option deliberately models revised **committed** captures by repinning digests and supplying matching simulated blobs; `uncommitted` leaves the real lock intact. R1 uses unchanged real capture bytes. The following recipes reproduce the core findings from the repository root at `ac792ef` without game requests:

```sh
node --input-type=module <<'JS'
import { scenario, editQuest, aiCapture, AI, MARROW, STORMCOURT }
  from './forge/test/presentation.scenario.mjs';
const M = 'harvests/inbox/tnr_results_1789829183863.json';
const A = 'harvests/inbox/tnr_results_1789402842027.json';
const show = (name, opts, pick) => {
  const r = scenario(opts);
  console.log(name, r.ok ? { lintOK:r.built.lint.ok,
    observed:pick(r.built.dossier) } : String(r.error));
};
show('R1 duplicate current quest', {evidence:e=>{
  const r=structuredClone(e.records.find(r=>r.id==='marrow-quest'));
  r.id='marrow-duplicate'; e.records.push(r); return e;
}}, d=>({totals:d.totals, locations:d.locations}));
show('R1 older and newer Stormcourt', {evidence:e=>{
  const r=structuredClone(e.records.find(r=>r.id==='marrow-quest'));
  r.id='stormcourt-earlier'; r.questId=STORMCOURT;
  r.capture={phase:'after',at:'2026-09-19T14:46:23.796Z',
    snapshotKey:'52-mu8i2pd8::after::3'};
  e.records.push(r); return e;
},spec:s=>{delete s.story.stormcourt; return s;}}, d=>({totals:d.totals,
  name:d.structure[STORMCOURT].name, source:d.structure[STORMCOURT].source}));
show('R2 tied name conflict', {files:{[A]:b=>{
  const c=structuredClone(aiCapture(b,AI.wardenHalfEclipse));
  c.snapshotKey='different-snapshot'; c.data.username='Alternate Keeper';
  b.captures.unshift(c); return b;
}}}, d=>d.roster.find(e=>e.aiId===AI.wardenHalfEclipse));
show('R3 reward order', {files:{[M]:editQuest(MARROW,q=>{
  q.content.objectives.find(o=>o.id==='b1_1').failObjectiveId='d5_victory';
  q.content.objectives.find(o=>o.id==='d3_1').reward_money=20000; return q;
})}}, d=>({fullClear:d.rewards[MARROW].fullClear,
  intermediate:d.rewards[MARROW].intermediateCashOuts,
  successPath:d.structure[MARROW].successPath}));
show('R3 optional battle cadence', {files:{[M]:editQuest(MARROW,q=>{
  const o=structuredClone(q.content.objectives.find(o=>o.id==='b1_1'));
  o.id='optional_exit_battle'; o.nextObjectiveId='fall';
  q.content.objectives.push(o);
  q.content.objectives[0].nextObjectiveId.unshift(
    {text:'Leave after fighting',nextObjectiveId:o.id}); return q;
})}}, d=>({linear:d.structure[MARROW].successPathLinear,
  cadence:d.encounters[0].cadence, sequence:d.encounters[0].sequence.slice(0,2)}));
JS
```

## Correction handoff

Fable owns the fixes on its implementation branch. Close R1–R3 while retaining the successful F1/F2/F6/F7 corrections and the unmodified golden facts. Run the normal gates and focused regressions, then return a new frozen base/merge-base/head. Re-review source selection, dossier assembly, graph/encounter/reward consumers, and affected tests together; deeper P0 review is needed only if P0 changes. Do not merge this report branch into the implementation. No user ruling is needed for these engineering corrections.
