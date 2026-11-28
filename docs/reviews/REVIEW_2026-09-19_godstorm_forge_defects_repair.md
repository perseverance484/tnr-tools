# Independent review — Godstorm Forge defects repair

**Verdict: APPROVED FOR INTEGRATION, with non-blocking debt noted below.**

| Field | Value |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Review target | `claude/forge-godstorm-defects-repair-rxxwky@82afbba8d44b7a41c2bba122ef62280eddee812d` |
| Branch tip at review time | `7d5153377c41738c34ade93f4d1dda6fc8e4b8f2` — stamp-only child of the reviewed target |
| Intended base / merge-base | `8c47d52cbabd8bf712f8bb0f76da0f4ff9383dc3` |
| Base relation | reviewed target is 3 commits ahead, 0 behind |
| Governing build contract | `chatgpt/godstorm-two-pyramid-plan@4d5ee40c62dad55b30854f8bfa242cf6ef0936fb` → `docs/handoffs/GODSTORM_FORGE_DEFECTS_REPAIR_HANDOFF.md` |
| Authoritative incident result | `harvests/inbox/tnr_results_1789829183863.json` |
| Game source checked independently | `studie-tech/TheNinjaRPG@a670c9aaa741157dc66eacc949600ff2db0b48cd` |
| Live requests / writes during review | **none** |
| Source pin moved | no |
| Repair manifest run | no |

## 1. Review scope

This review attacked the four incident defects and the specific failure seams named in the build contract:

1. list-query input contract and asset-create reconciliation safety;
2. manifest execution-policy identity;
3. AI-profile rules verification and resume/reconciliation;
4. image-picker binding to the manifest's physical-byte contract;
5. repair-manifest dependency/idempotence implications;
6. release/promotion path required before the operator can safely retry.

The review was performed against the exact frozen implementation SHA, not the moving branch tip. The later branch-tip stamp commit changes only the implementation-handoff document.

## 2. Finding summary

**No merge-blocking defect survived review.**

The four implemented corrections address the actual causes recorded in the committed production result, without bypassing the safety mechanisms that failed.

### A — list input / create snapshot: APPROVED

The implementation fixes the input shape centrally in `CachedReader.list()` through an explicit path adapter:

```
gameAsset.getAllNames -> {}
other supported name lists -> undefined
```

This repairs both consumers of the broken contract:

- `Runner._dedupNames()`
- `Reconciler.beforeCreate()`

The second path matters most. Disabling name dedup alone could never have repaired manifest 52 because reconciliation still required the pre-create name-list snapshot.

The implementation preserves the fail-closed create model. It does **not** skip snapshots, continue after a failed snapshot, or weaken ambiguous-create reconciliation.

#### Independent current-upstream audit

The implementation owner could not inspect current upstream directly, so I closed that gap independently against:

`studie-tech/TheNinjaRPG@a670c9aaa741157dc66eacc949600ff2db0b48cd`.

Forge-supported name-list procedures at that exact source:

| Forge path | Current source input |
| --- | --- |
| `jutsu.getAllNames` | no `.input()` |
| `item.getAllNames` | no `.input()` |
| `bloodline.getAllNames` | no `.input()` |
| `quests.getAllNames` | no `.input()` |
| `profile.getAllAiNames` | no `.input()` |
| `gameAsset.getAllNames` | required `z.object({type?: ..., folderPrefix?: ...})` |

So the new adapter table is correct at current upstream: **asset is the only supported name list presently requiring an input object**.

This closes handoff debt item 6 for the current source SHA. Future route drift still needs normal contract-regeneration discipline.

The added filtered-list handling is also sound: non-default filter inputs bypass the single default-list cache entry instead of contaminating evidence with a differently filtered answer.

### B — manifest identity: APPROVED

The incident proved that the old hash meant "same items/captures" rather than "same execution contract":

- manifest 50: `dedupNames:true`
- manifest 51: `dedupNames:false`
- old hash for both: `d5164ee3`

The repair includes normalized execution policy in identity:

- `dedupNames`
- `readBack`
- `skipPreflight`
- `imgSizes`

while leaving prose `_note` outside identity.

The compatibility rule is conservative:

- default policy retains the historical body hash;
- a non-default policy receives a distinct identity;
- an old job whose stored body-only hash matches a now-policy-bearing manifest is **refused for resume**, rather than silently treated as compatible.

That is the safe direction. In particular, the open manifest-52 job becoming non-resumable under the upgraded bundle is preferable to reintroducing the 50/51 equivalence.

The implementation does not require the operator to delete that old job in order to open manifest 53.

### C — AI-profile false drift: APPROVED

The committed result showed all 18 AI-profile writes as `CONFIRMED / verify`, with `rules` diffs whose exported `sent` and `live` documents are semantically identical.

The implementation identifies the actual cause: textual `JSON.stringify` equality was sensitive to object key order after server validation rebuilt rule objects.

`deepEqualPayload()` is appropriately narrow:

- object key order is ignored;
- object keys whose value is `undefined` are treated as absent;
- array order remains significant;
- missing real-valued keys remain drift;
- `null` remains distinct from absence;
- value types remain strict;
- target/gate changes remain detectable.

The same structural comparison is used in both ordinary verification and SENT-rules reconciliation. That closes the more dangerous crash/resume case where a landed rule write could otherwise be mislabeled ORPHANED.

I specifically do **not** recommend replacing this with JSON stringify, blanket key sorting of serialized text, or exempting `rules` from verification.

The pre-existing debt noted by the implementation owner remains valid: rule payloads carrying unresolved `@ref` strings are outside this fix.

### D — image-picker contract: APPROVED, including the documented filename deviation

The incident failure was operator-visible but too late: Forge displayed an expected logical WebP as "picked" while the physical selected object was a 1.3–1.8 MB PNG master.

The implementation now checks before job creation:

- the manifest has an `imgSizes` ledger entry;
- physical byte count matches that ledger **exactly**;
- physical bytes are under the uploader ceiling;
- reported MIME is image-compatible with the logical extension when MIME is available.

The same check is repeated in `ForgeCore.startJob()`, so a non-UI/headless caller cannot bypass it.

The UI now surfaces the actual physical filename, bytes, ledger bytes, and MIME type.

#### Filename mismatch decision

The build contract asked for "wrong filename selected -> blocked." The implementation accepts a device-renamed file when its byte ledger and type match, and surfaces the rename.

I accept that deviation.

Repository L17 explicitly documents the Android operator path as matching a physical file by size when its filename differs. Blocking all filename mismatch would conflict with that established mobile workflow. Exact byte equality plus expected image type is the repository's current identity contract; this task did not introduce a cryptographic image-hash ledger.

This remains less collision-resistant than a SHA-256 manifest, but strengthening asset identity to hashes would be a separate contract/tooling change, not a reason to reject this repair.

## 3. Create/reconciliation adversarial check

The key invariant is unchanged:

> a create must never be guessed or re-sent merely because the previous response is unavailable.

The repaired path still does:

1. fresh unfiltered name-list snapshot;
2. synchronously records the pre-create ID set;
3. only then permits create;
4. on ambiguous resume, re-lists and subtracts:
   - baseline IDs,
   - IDs already owned by this job,
   - IDs owned by other jobs;
5. adopts automatically only when one new row and one pending create make the answer unambiguous;
6. otherwise produces ORPHANED and requires operator action.

For manifest 53's three sequential asset creates, one snapshot per entity type is sufficient: previously confirmed asset IDs are removed from later reconciliation candidates. I found no new duplicate-create path introduced by the repair.

The fake-game change now models the exact asset list-input rejection and retains the existing crash/reconciliation tests. That is the correct test seam.

## 4. Repair manifest 53 review

`push/53_godstorm_failed_items_repair.json` remains on the ChatGPT planning branch and was not executed by the implementation owner.

Its scope is correct for the captured live state:

- 3 background asset creates;
- 5 avatar edits;
- 1 Stormcourt quest edit;
- **no** replay of the 18 AI-profile writes;
- **no** replay of Marrow Vaults.

The Stormcourt quest's three `@scene:` dependencies intentionally require the earlier same-job asset creates, so failure of a create leaves the quest reference unresolved rather than writing an invalid literal.

The correct five processed avatar WebPs all fit below the uploader ceiling; the new picker should reject the previously selected PNG masters before a job opens.

Manifest 53 should **not** be staged/run until this implementation is integrated and the released Forge loader actually points at the new bundle.

## 5. Release-path review

The implementation stages Forge `0.4.2` with `@x-release-pending`; the loader still points to the prior immutable release on the feature branch.

That is correct repository procedure.

Current `.github/workflows/release_pin.yml` triggers on a push to `main` changing `forge_bundle.js`, then runs `pin_release.py` and commits the pinned loader. After integration:

1. wait for the release-pin workflow to finish;
2. verify the loader commit landed;
3. ensure the operator's installed userscript updates/reinstalls as necessary;
4. **verify the Forge panel title shows 0.4.2** before trusting manifest 53.

Running 53 while the installed loader still executes the old immutable bundle would reproduce the original asset-list failure.

## 6. Test/build evidence

Implementation handoff reports:

```
npm ci                                      PASS
npm test                                    372 / 372 pass
npm run fixtures                            byte-identical envelope + 12 screens
npm run build                               PASS
check_boundaries.mjs                        37 modules, 0 violations
check_imports.mjs                           37 modules, 65 cross-layer imports, 0 violations
check_bundle_budget.mjs                     raw 424642/442000; gzip 81344/84600
check_release_pin.mjs                       PASS
check_manifest.mjs <manifest 53>            9 items, 0 pre-send problems
```

I inspected the implementation and focused tests at the exact frozen SHA, including the incident-fixture replay. No GitHub Actions run is associated with the frozen SHA, and this review environment did not provide an authenticated local repository checkout from which I could independently execute the npm suite. Therefore I treat the command outputs above as implementation evidence, not independently rerun evidence.

The checked-in implementation, tests, bundle, version staging, and handoff are internally consistent with those reported outputs.

## 7. Non-blocking debt

These do not block integration or the Godstorm repair push after release:

1. **Partial multi-entity failure fixture remains absent.** The requested broad fixture where creates fail, edits succeed, a dependent quest fails refs, and captures still complete would be valuable regression coverage. The incident bundle itself remains durable evidence.
2. **Bundle budget is tight.** The ratchet was deliberately stepped to 442,000 raw / 84,600 gzip and current output sits around 96%. Future Forge work has little headroom.
3. **Rule `@ref` resolution debt remains.** `_rules()` / rule verification still assume rule payloads do not carry unresolved reference strings. Pre-existing and not exercised by repair manifest 53.
4. **No real-browser execution evidence.** Firefox/Android picker behavior, actual userscript update timing, real Clerk session, live tRPC transport, and live rate limiter were not exercised by implementation or review.
5. **Image identity remains byte-ledger based.** Same-size/same-type wrong bytes are theoretically possible. A future hash-ledger contract could strengthen this, but it would be a separate system change.
6. **Current contract extraction remains behind upstream generally.** This review independently checked the six name-list procedures at current upstream, but did not adopt/regenerate the whole generated contract set.

## 8. Claims specifically refuted or refined

- **"Other name-list procedures might also require object inputs at current upstream."** Refuted for the six Forge-supported name-list procedures at `a670c9aaa741157dc66eacc949600ff2db0b48cd`; only `gameAsset.getAllNames` currently has an input schema.
- **"Filename mismatch must always be blocked."** Not accepted as a blocker because it conflicts with the existing Android/L17 size-ledger workflow. The repair visibly reports the rename and binds to exact expected bytes instead.
- **"Manifest 52 should remain resumable."** Refuted as a safety requirement. Its old journal identity did not record execution policy; refusing resume under the new bundle is the correct fail-closed result.

## 9. Integration recommendation

**APPROVED.**

The frozen implementation may be integrated to `main`.

After merge:

1. allow `release_pin.yml` to promote Forge 0.4.2 and pin the immutable bundle;
2. verify the operator is actually running Forge 0.4.2;
3. stage `push/53_godstorm_failed_items_repair.json` through the normal content lane;
4. use only the exact processed image files matching its ledger;
5. user runs manifest 53;
6. commit/export the resulting Forge bundle;
7. independently verify:
   - three new background IDs exist;
   - five avatar URLs changed;
   - Stormcourt is 53 objectives / 25 battles / 26 dialogs;
   - all `@scene:` references were replaced with real IDs;
   - no Tower/cash-out/keystone/chest residue remains;
   - Marrow and the 18 AI profiles remain unchanged from the already-correct live state.

No live action is authorized by this review; the user remains the live-game operator.
