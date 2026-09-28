# One Perfect Crop launch-final — independent review round 1

**Review target:** `6757e0c2130d39a35753380ec4bcc8af85e765b8`  
**Manifest:** `push/54_one_perfect_crop_launch_final.json`  
**Reviewed manifest hash:** `fedebd24`  
**Verdict:** BLOCKED / DO NOT EXECUTE  
**Live requests / writes during review:** 0 / 0  
**Forge execution during review:** none

## Blocking findings

### F1 — planner order depends on the retained idmap

The reviewed manifest contains two scene-asset creates and a quest edit that references both
scene `srcId` values. Forge's `planOrder()` treats a reference already present in the retained
idmap as satisfied rather than as a dependency. The journal, however, is positional after a job
is opened.

At the reviewed SHA, the quest and both scene creates used the default planner phase. Therefore
the initial empty-idmap plan and a later attach after one or both scene ids had been persisted
could produce different item orderings. A resumed positional journal could then be paired with
the wrong planned payload.

**Required correction:** make the planner order invariant across empty, partial and full scene
idmap states. The chosen correction is an explicit later planner phase on the quest edit
(`phase: 6`) while the preceding edits/creates retain the default phase. Add a regression that
plans the committed launch-final manifest under empty/partial/full scene-idmap states and proves
re-attach preserves the journal-to-plan positional mapping.

### F2 — create-name deduplication was disabled

The reviewed manifest contains two gameAsset creates while top-level `dedupNames` was false.
A live name collision can therefore be discovered only after a create placeholder exists. Since
a created scene id is also persisted under its `srcId`, a later quest edit could resolve its
`@scene` reference to a bad placeholder row.

**Required correction:** set top-level `dedupNames: true` so Forge performs its live-name
collision gate before creates are sent.

## Scope that already passed review

The review found no other surviving issue: five intended items; two hidden SCENE_CHARACTER
creates; two AI edits; one quest edit; 36/36 objectives reachable; no dangling edges or routing
drift; approved prose/admin exact; 27/27 dialogs with exactly one scene character; art
bytes/hash/dimensions exact.

The corrected candidate must rerun generator exactness, repository content validation, Forge
offline manifest validation, art preflight, workstream validation/render/selftest, the new
planner/re-attach regression, and repository scrub before a new exact-SHA handoff.

The reviewed SHA `6757e0c2130d39a35753380ec4bcc8af85e765b8` and the earlier
`70a82ad7891064ba9e4718ecca4d8cdd143fce58` candidate are both non-executable.
