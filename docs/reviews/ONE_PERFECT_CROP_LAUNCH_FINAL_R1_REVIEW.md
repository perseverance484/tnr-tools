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

## Correction implemented

The implementation branch now applies both required corrections:

- top-level `dedupNames: true`;
- explicit `phase: 6` on the quest edit, leaving the preceding AI edits and both scene creates
  at the default phase;
- `forge/test/runner.test.mjs` now loads the committed launch-final manifest and proves identical
  plan order under empty, Ittetsu-only, Keeper-only and full scene-idmap states, then opens the job
  under an empty idmap and re-attaches under each state to prove the positional journal still maps
  to the same planned payloads.

A correction-gate run at implementation commit
`ce748f6465fd6886e15b574ccc199d8464f95046` passed generator exactness, validate.py
(0 errors / 0 warnings), Forge offline planning (5 items / 0 pre-send problems), the full Forge
test suite (523/523), Road Bandit artpreflight (0/0), Ittetsu+Keeper artpreflight (0/0),
workstream validation/render drift, and workstream selftest. The corrected manifest hash at that
gate was `0b942400`.

This closes the implementation work for F1/F2 but does **not** convert this review to PASS.
A new frozen SHA after durable closeout records must receive a fresh independent review before
any hidden Forge execution.
