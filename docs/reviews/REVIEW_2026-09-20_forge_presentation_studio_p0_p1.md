# Forge Presentation Studio P0/P1 — independent review

**Verdict: changes requested for P1. P0 passes this review. Do not integrate the combined frozen head or start P2 from this foundation yet.**

Reviewed on 2026-09-20, using repository evidence and local tests. Live-game requests: **0**. Live-game writes: **0**. Asset-CDN requests: **0**. No implementation files, captures, art, manifests, or Fable branch refs were changed by the reviewer.

| Ref | Independently verified value |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Current `origin/main` and intended base | `eefefd1afd67111a90c332951a8dd9f83cb99cbd` |
| Implementation branch | `claude/forge-presentation-studio-p1-y1wbiq` |
| Merge-base | `eefefd1afd67111a90c332951a8dd9f83cb99cbd` |
| Frozen remote/local head | `8830443977122253a956fb77392a7d2925d6cb6f` |
| Two implementation commits | P0 `05e71564d693a8505f98df4400502abee7517a3c`; P1 `8830443977122253a956fb77392a7d2925d6cb6f` |
| ChatGPT review branch, based on frozen head | `chatgpt/review-forge-presentation-studio-p1` |
| Governing plan | `chatgpt/forge-presentation-studio-plan@99f1aa8a6fe7cc7361aa613cdcad258bafb9c83e`, `docs/plans/FORGE_PRESENTATION_STUDIO_UPGRADE_PLAN.md` |
| Design proposal, separate ownership/acceptance | `chatgpt/forge-presentation-studio-design@4532ef917a1dfb40d00c554fd7f065e13216afc7` |
| Pinned game source inspected | `studie-tech/TheNinjaRPG@345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9` |

The design branch remains a proposal awaiting director acceptance. Findings below rest on the governing plan, supported parser behavior, and pinned source; draft layout preferences are not merge gates. The review followed `CHATGPT.md`, `docs/DEVELOPMENT_WORKFLOW.md`, and `docs/workflows/FABLE_REVIEW.md` after reconstructing current main. Content Designer remains the task's lead lens, with Engineering Auditor applied to the frozen implementation and UI/UX and Art Director checks on the contracts it exposes.

## Findings

All seven findings survive reproduction against the frozen tree. High means a core evidence/art integrity gate accepts unverified or stale material. Medium means incorrect derived content or an advertised validation surface that silently loses information. These are repository-tool defects; no production mutation occurred.

### F1 — High: an unreadable immutable asset blob still becomes renderable exact art

**Location:** [assets.mjs:173](https://github.com/perseverance484/tnr-tools/blob/8830443977122253a956fb77392a7d2925d6cb6f/forge/presentation/assets.mjs#L173), with the success assignment at line 213 and lint's status-only acceptance. **Contract:** plan §§4.3–4.5, P1 missing/unverified art refusal.

When `blobAtRef()` returns null, the registry sets `refVerified: false` and adds a note, then continues through the URL comparison to `exact-current-bytes`. `RENDERABLE` includes that status; lint never checks `refVerified`.

**Reproduced:** `scenario({blobAtRef: () => null})` passes lint and marks all five bound portraits exact-current-bytes with `refVerified: false`. The stronger witness replaces Umbral Reaver with Starless Monk bytes padded to the original **161,650-byte** length, updates the local pack digest, and gives the pack an unavailable all-zero 40-hex ref. The normal git reader returns null. Lint still passes and the wrong image is exact-current-bytes. No injected reader is needed for that witness.

**Correction:** inability to resolve/verify the named immutable blob must stop promotion to exact/renderable status and produce a fatal finding when that asset is required. An absent verifier must not imply verification either. Add the unavailable-ref variant to the existing same-size wrong-image test. A note is insufficient because both readiness counts and the future renderer consume status.

### F2 — High: invalid captures and arbitrary nested objects can satisfy complete evidence

**Location:** [evidence.mjs:90](https://github.com/perseverance484/tnr-tools/blob/8830443977122253a956fb77392a7d2925d6cb6f/forge/presentation/evidence.mjs#L90), quest admission at line 144 and AI loading at line 154; [structure.mjs:104](https://github.com/perseverance484/tnr-tools/blob/8830443977122253a956fb77392a7d2925d6cb6f/forge/presentation/structure.mjs#L104). **Contract:** plan §4.5 required sources verified; P1 complete roster and publication provenance.

`collectAiRecords()` recursively searches the entire JSON document for `{userId, username, avatar}`. It does not require a successful `profile.getAi` capture, matching request identity, `isAi`, or persisted full data. The quest path checks `ok` and quest ID but ignores persistence and required factual fields.

**Reproduced, each with zero lint fatals:**

- Set Warden of the Half Eclipse's only capture to `ok:false`, `persist:"none"`, `persistOk:false`, and change its input userId to another entity. The keeper remains resolved and coverage remains 18/18.
- Remove that keeper's avatar/name from the actual capture and put its old record only in top-level `debugSnapshot`. The complete roster passes again.
- Set the Stormcourt quest capture to `persist:"none", persistOk:false`; it still supplies current structure/rewards.
- Remove Marrow's `hidden` field; the dossier emits `hidden:false` and loses the unpublished warning instead of reporting unknown/incomplete evidence.

**Correction:** admit only supported, individually validated capture records; require the correct procedure, identity, full persistence, and required field types. Preserve unknown status rather than coercing missing evidence to false. Keep the valid Marrow capture from the overall failed run eligible: its individual read-back is successful and fully persisted. Rejecting whole failed bundles would discard valid evidence and would not fix the admission boundary.

### F3 — High: current capture selection is neither immutable nor conflict-aware

**Location:** [evidence.mjs:38](https://github.com/perseverance484/tnr-tools/blob/8830443977122253a956fb77392a7d2925d6cb6f/forge/presentation/evidence.mjs#L38), working-file loading at line 119, quest selection at line 139; [roster.mjs:36](https://github.com/perseverance484/tnr-tools/blob/8830443977122253a956fb77392a7d2925d6cb6f/forge/presentation/roster.mjs#L36). **Contract:** plan §§4.1, 5.3–5.4, source-lock flow and P1 explicit committed captures.

The package cannot express a commit, expected digest, phase, snapshot key, or exact capture selector. Quest loading chooses the first matching capture. AI freshness uses the **bundle export timestamp**, then keeps the first object on ties. The resulting dossier has no `sources.repoCommit`. Computing a new digest after reading a working file records what was consumed but does not verify the selected source lock.

**Reproduced:** prepend an earlier successful `before` Marrow capture, retaining the valid `after` capture, and give the earlier victory node 1 ryo. Lint passes with **1 ryo as current full clear**. Prepend an older before-capture of the final Marrow keeper in the same AI bundle: `Stale Keeper` wins over the newer capture, with the export time falsely reported as its capture time. Separately, changing only the working copy of Marrow's reward to 7 produces a passing dossier, a newly computed hash, and no warning that its source bytes differ from the frozen repository.

**Correction:** bind the evidence package/dossier to immutable source bytes and precise eligible capture identities, retaining per-capture timestamps and provenance. Resolve overlapping observations by an explicit selection/freshness rule and refuse unresolved conflicting candidates; do not use array order or export time as authority. A supported draft mode can expose uncommitted evidence explicitly, but must not silently present it as verified current evidence. F2 is about admissibility; this finding is about choosing and preserving the right version among otherwise eligible records.

### F4 — Medium: encounter order and entry detection follow storage order instead of the quest graph

**Location:** [structure.mjs:70](https://github.com/perseverance484/tnr-tools/blob/8830443977122253a956fb77392a7d2925d6cb6f/forge/presentation/structure.mjs#L70). **Contract:** plan §5.1 graph-derived structure and encounter sequence.

The extractor chooses `objectives[0]` as entry and filters the original array to create the battle sequence. Its comment claiming this is how the engine walks is contradicted by the pinned source: [objectives.ts:153](https://github.com/studie-tech/TheNinjaRPG/blob/345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9/app/src/libs/objectives.ts#L153) finds the objective with no predecessor and traverses selected links; [quest.ts:1969](https://github.com/studie-tech/TheNinjaRPG/blob/345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9/app/src/libs/quest.ts#L1969) validates a unique unreferenced start.

**Reproduced:** swap the array positions of `b1_1` and `b1_boss`, changing no IDs or edges. Lint passes, but the first reported encounter becomes the keeper and cadence becomes “1 keeper then 8 recurring…” instead of the unchanged real 4+1 pattern. Moving `d1_1` from the front to the end of the array makes that reachable opening dialogue appear unreachable and falsely invalidates its story anchor.

**Correction:** derive the entry and ordering from validated graph semantics. For branching/non-consecutive structures, represent that structure or refuse an unsupported single-sequence/cadence claim. Do not flatten it according to array order. Regression: reordering storage without changing edges must preserve the derived content.

### F5 — Medium: an optional exit reward can replace the successful full-clear reward

**Location:** [rewards.mjs:63](https://github.com/perseverance484/tnr-tools/blob/8830443977122253a956fb77392a7d2925d6cb6f/forge/presentation/rewards.mjs#L63). **Contract:** plan §5.3 current reward semantics and separation of full clear from intermediate cash-outs.

`fullClear` is the last reward visited by a general DFS, not a reward proven to be on the completion path. Every earlier reachable reward becomes an intermediate cash-out, and `total` sums mutually exclusive paths.

**Reproduced:** retain the complete current Marrow route, add an opening optional exit dialogue paying 20,000 ryo and leading to `fall`, and put that choice before “Advance”. Lint passes. `fullClear` becomes the **20,000-ryo exit**, the actual `d5_victory` reward becomes an “intermediate cash-out”, and `total.money` becomes **145,000**, although the two routes are exclusive. Merely adding a reward to `fall` also reports it as an intermediate reward and adds it to the total.

**Correction:** classify rewards against successful versus failed/optional paths. When the graph does not support one unambiguous full-clear amount, expose alternatives or fail the unsupported claim. Totals must have a defined path basis. Preserve Godstorm's reward-bearing victory dialogue before the zero-reward `win_quest`; requiring the reward to sit directly on a terminal would be wrong.

### F6 — Medium: narrative validation accepts known stale wording and changed source meanings

**Location:** [narrative.mjs:40](https://github.com/perseverance484/tnr-tools/blob/8830443977122253a956fb77392a7d2925d6cb6f/forge/presentation/narrative.mjs#L40), anchor resolution at line 98 and emitted anchors at line 120. **Contract:** plan §5.4 and §8's stale Tower/Dawnless negative fixture.

All sentence-initial words are exempt from the proper-name check. The emitted anchors carry IDs/tasks but no reviewed source-field version; words from any known roster name also satisfy the vocabulary check.

**Reproduced:** set Marrow's summary to `Dawnless awaits below. Tower rises above.` while keeping the existing three anchors. Lint passes. Independently, change `d5_victory.description` so the stair remains closed and the player leaves by the entrance. The old summary still claims the stair stands open, and passes with no narrative warning because the IDs remain and the Warden's name is allowed elsewhere.

**Correction:** cover known unsupported names at sentence starts as well as elsewhere. Bind reviewed summaries to the selected objective fields/source version and invalidate or require explicit editorial re-review when those fields change. A source-content fingerprint is one small way to do that; this does not require automatic semantic judging or an LLM. Existing-ID validation alone is not evidence that retained prose summarizes the current dialogue.

### F7 — Medium: declared quest and scene image bindings are silently ignored

**Location:** [spec.mjs:122](https://github.com/perseverance484/tnr-tools/blob/8830443977122253a956fb77392a7d2925d6cb6f/forge/presentation/spec.mjs#L122), [assets.mjs:112](https://github.com/perseverance484/tnr-tools/blob/8830443977122253a956fb77392a7d2925d6cb6f/forge/presentation/assets.mjs#L112). **Contract:** plan §4.3 registry for `avatar`, quest `image`, and game-asset images, with required-asset lint.

The parser advertises `ai:`, `quest:`, and `asset:` bindings. Registry construction only iterates roster AIs, and lint only requires those AI entries. Other accepted bindings never reach validation or the output.

**Reproduced:** bind `quest:2yvE9PUQqlD8lbYNfgX-b` and `asset:7xVJ55rsqarfRmPqLdv98` to `art/does-not-exist.webp`. Parsing and lint pass, registry total stays 18, and neither binding appears in it. This is separate from correctly refusing scene IDs in `spec.locations`.

**Correction:** every accepted binding must be resolved and checked, or explicitly refused as unsupported in P1. Keep scene artwork separate from semantic locations while doing so. A future renderer must not receive a spec whose selected named art escaped lint.

## Reproduced gates and bounded positives

Environment: Node `v24.19.0`, npm `11.9.0`; dependencies installed from the unchanged lockfile with `npm ci --ignore-scripts`. Repository/dependency network access was used; game and image-CDN endpoints were not contacted.

| Check | Independent result |
| --- | --- |
| `cd forge && npm test` | **481 passed, 0 failed, 0 skipped** |
| `npm run build`; diff `forge_bundle.js` | Exit 0; checked artifact byte-identical |
| `npm run fixtures`; diffs of envelope/screens fixtures | Exit 0; no generated drift; 14 screen fixtures rebuilt |
| `node tools/check_imports.mjs` | 40 modules / 71 cross-layer imports; 0 violations |
| `node tools/check_boundaries.mjs` | 40 source + 13 presentation modules; 0 violations |
| `node tools/check_bundle_budget.mjs` | 339,669 / 354,000 raw; 74,926 / 78,000 gzip |
| Runtime dependency audit | `npm audit --omit=dev --audit-level=high`: 0 vulnerabilities |
| Release-pin check | Clean |
| P0 nested contract regeneration | Exact pinned validator files read from Git; `derive_nested.mjs` output byte-equal to committed `nested.json` |
| Independent expanded-contract comparison | `expandNested(current)` deeply equals main's pre-compaction contract after omitting metadata; 53 shared key sets |
| Default Godstorm CLI | Exit 0; 0 fatal / 17 warnings; correct unmodified golden facts |
| Godstorm `--require-exact-bytes` | Exit 1; **13 fatal / 4 warnings**; expected current implementation limitation, not a successful complete-art build |
| Session source guards | Lawmap 0 errors / 5 existing warnings; doctrine/packs current; baseline parity adapter remains red as described below |

P0 reduces raw bytes from **451,847 to 339,669 (24.8%)**, and gzip from **88,356 to 74,926 (15.2%)**. It lowers the ratchet, preserves the expanded validation surface, retains source comments, and proves stripped/unstripped build equivalence with the esbuild normalization gate. P1 adds no code to the runtime artifact: the bundle is identical between the P0 and P1 commits. No P0 correction is requested; this is not approval to merge the combined head with P1 blockers.

The unmodified Godstorm dossier correctly derives two pyramids, 25 battles and five keepers each, 18 distinct AIs, the 4+1 cadence, 125,000/25/10 and 250,000/150/60 full-clear rewards, zero intermediate cash-outs/items, and both subjects hidden. Existing negative tests correctly reject an actually absent keeper, explicit roster omission, ordinary asset swaps, same-size swaps when the immutable blob is available, nonexistent story IDs, and scene IDs used as top-level locations. Those positives do not cover the bypasses above.

The session bootstrap parity adapter crashes on the already-committed Forge results bundle because `validate.py` treats `checks:null` as iterable. This occurs on base main and is outside the P0/P1 diff; it is **not** attributed to this implementation and no green session guard is claimed. The dedicated harvest verifier and committed read-back evidence establish the completed Godstorm run independently. No live re-verification was performed.

## Art readiness and design alignment

The registry currently proves bytes for five portraits, and exposes thirteen URL observations. The README/golden test's claim that the other thirteen require future live materialization overlooks committed source-art evidence.

Reverified during this review at `1bca57eeb0c1836a49334dc2f49196a5a3db24c7`:

- `art/godstorm_sources/capture-2026-09-14/index.json` and its 19 files: SHA-256, length, dimensions, and image decoding all pass.
- Both indexed source-bundle digests match the frozen implementation's evidence files.
- All **13** portraits omitted from byte resolution join by entity ID and captured avatar URL to this archive; both quest listing images also join to their selected current captures.
- The other five portraits remain bound to the verified push/53 pack at `10fb25704dff1bab8105cd83631e0d524193ef0d`.

Use these immutable pointers and the separate [Godstorm design reference](https://github.com/perseverance484/tnr-tools/blob/4532ef917a1dfb40d00c554fd7f065e13216afc7/docs/design/FORGE_PRESENTATION_STUDIO_GODSTORM_REFERENCE.md) for archive resolution. No binary duplication, generative redraw, or CDN request is needed. These are exact bytes tied to the selected captured URLs, not a claim that remote content was freshly fetched today. Historical filenames/names in an archive must not become current presentation copy.

Before P2, align the registry with the plan's factual classes (`exact-current`, `approved-derivative`, `historical-only`, `missing`) and model byte availability/verification separately if needed. The current schema has no approved-derivative path and omits MIME/dimensions and location-image coverage. Those are explicit contract follow-ups; the review does not demand a renderer, Android browser test, or final poster in P1. The concrete ignored-binding defect is F7.

## Reproduction method

Scratch attacks used `forge/test/presentation.scenario.mjs` from the frozen tree. It creates temporary roots, copies only changed evidence, unlinks per-file art symlinks before replacement, and deletes each root. All production-tree art hashes and generated artifacts remained unchanged. Scratch files were not committed, per the review workflow.

Original command: `node /workspace/scratch/9b09e6cf21d0/evidence/p1-review-attacks.mjs`; 17 control/adversarial cases completed without runtime errors. The important false acceptances are recorded above. The following compact witnesses are reproducible from the repository root at the frozen SHA; they log observed behavior, not assertions that the incorrect behavior is desirable.

```sh
node --input-type=module <<'JS'
import { scenario, editQuest, dropAi, AI, MARROW, STORMCOURT }
  from './forge/test/presentation.scenario.mjs';
const M = 'harvests/inbox/tnr_results_1789829183863.json';
const S = 'harvests/inbox/tnr_results_1789842714086.json';
const A = 'harvests/inbox/tnr_results_1789402842027.json';
const show = (name, opts, pick) => {
  const r = scenario(opts);
  console.log(name, r.ok ? {lintOK:r.built.lint.ok,
    fatal:r.built.lint.fatal, observed:pick(r.built.dossier)} : String(r.error));
};
show('F1 unavailable blob', {blobAtRef:()=>null}, d =>
  d.assets.entries.filter(e=>e.repoPath).map(e=>[e.status,e.refVerified]));
show('F2 failed AI', {files:{[A]:b=>{
  const c=b.captures.find(c=>c.input?.userId===AI.wardenHalfEclipse);
  c.ok=false; c.persist='none'; c.persistOk=false;
  c.input.userId='different-entity'; return b;
}}}, d=>d.roster.find(e=>e.aiId===AI.wardenHalfEclipse));
show('F2 metadata-only keeper', {files:{[A]:b=>{
  const record=structuredClone(b.captures.find(
    c=>c.input?.userId===AI.wardenHalfEclipse).data);
  b=dropAi(AI.wardenHalfEclipse)(b); b.debugSnapshot=record; return b;
}}}, d=>d.roster.find(e=>e.aiId===AI.wardenHalfEclipse));
show('F3 stale before capture', {files:{[M]:b=>{
  const c=structuredClone(b.captures.find(c=>c.input?.id===MARROW));
  c.phase='before'; c.at='2026-09-19T14:40:00.000Z';
  c.snapshotKey='52-mu8i2pd8::before::2';
  c.data.content.objectives.find(o=>o.id==='d5_victory').reward_money=1;
  b.captures.unshift(c); return b;
}}}, d=>d.rewards[MARROW].fullClear);
show('F4 unchanged graph', {files:{[M]:editQuest(MARROW,q=>{
  const a=q.content.objectives;
  const x=a.findIndex(o=>o.id==='b1_1'), y=a.findIndex(o=>o.id==='b1_boss');
  [a[x],a[y]]=[a[y],a[x]]; return q;
})}}, d=>d.encounters.find(e=>e.questId===MARROW).cadenceText);
show('F5 optional exit', {files:{[M]:editQuest(MARROW,q=>{
  const o=structuredClone(q.content.objectives.find(o=>o.id==='d5_victory'));
  o.id='optional_exit_reward'; o.description='Leave with a partial reward.';
  o.reward_money=20000; o.reward_tokens=0; o.reward_prestige=0;
  o.nextObjectiveId=[{text:'Leave',nextObjectiveId:'fall'}];
  q.content.objectives.push(o);
  q.content.objectives[0].nextObjectiveId.unshift(
    {text:'Leave early',nextObjectiveId:o.id}); return q;
})}}, d=>d.rewards[MARROW]);
show('F6 stale vocabulary', {spec:s=>{
  s.story.marrow.text='Dawnless awaits below. Tower rises above.'; return s;
}}, d=>d.narrative[0]);
show('F6 changed ending', {files:{[M]:editQuest(MARROW,q=>{
  q.content.objectives.find(o=>o.id==='d5_victory').description=
    'The stair remains closed. You leave by the entrance.'; return q;
})}}, d=>d.narrative[0]);
show('F7 ignored art', {spec:s=>{
  s.assets[`quest:${MARROW}`]='art/does-not-exist.webp';
  s.assets['asset:7xVJ55rsqarfRmPqLdv98']='art/does-not-exist.webp'; return s;
}}, d=>d.assets.entries.filter(e=>!e.entity.startsWith('ai:')));
JS
```

## Correction handoff

Fable should correct F1–F7 on its own branch and return a new frozen SHA with base/merge-base/head and the rerun gates. Preserve the good Godstorm facts and zero-live-request test boundary. Add negative coverage for unavailable asset refs; failed/misidentified/non-capture records; before/after and equal-time conflicts; uncommitted evidence; graph permutations; optional-exit rewards; changed same-ID dialogue; and non-AI bindings.

Re-review the P1 source/model/lint/spec/asset surface and its tests as a unit because the source-selection corrections affect multiple consumers. P0 needs regeneration and its usual gates, with a deeper re-review only if its code changes. No director choice blocks these engineering corrections. P2/P3 product and design acceptance decisions remain deferred. The review branch is evidence, not an integration candidate for the implementation or a replacement for Fable's branch.
