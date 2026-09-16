# One Perfect Crop core manifest — Forge 0.4.1 revision-2 re-review

**Verdict:** PASS — the Forge 0.4.1 compatibility blocker is closed. No blocking finding survived the narrow re-review.  
**Review target:** `6cce22e3fad0e08344cb2f3252bdf04909632983`  
**Implementation base / current `main` during review:** `a45b576428d21bd7f24889a4965cf626d8dbf18a`  
**Implementation branch:** `claude/one-perfect-crop-manifest-9wsry6`  
**Reviewer:** ChatGPT / Engineering Auditor  
**Live-game requests/writes during review:** none.

## Scope

This is the narrow correction review requested after Forge 0.4.1 refused revision 1 at manifest selection. Revision 1 (`af0efc6cb7657ea8bf95f6aae414ea2ff5391a2f`) is superseded for execution.

The reviewed target is the exact frozen SHA above, not the moving branch tip. The branch later received automated commit `1f514b392707926c76b08a005c992b7848f7fa8e`, which changes only `dist/building-tnr-content.zip`; that generated commit is outside this audit target.

Reviewed correction surface:

- `push/47_one_perfect_crop_core_manifest.json`
- `push/47_one_perfect_crop_core_manifest.gen.py`
- `skills/building-tnr-content/scripts/validate.py`
- `skills/building-tnr-content/scripts/selfcheck.py`
- `forge/tools/check_manifest.mjs`
- `forge/test/runner.test.mjs`
- revision-2 handoff and workstream evidence
- the unchanged Forge 0.4.1 parser, recipes, runner, validator and release-loader test at the implementation base.

The previous content/graph/combat audit remains applicable only where the correction left those payloads unchanged. The re-review specifically attacked the manifest-shape change and the repository gates added to prevent recurrence.

## Result

### Forge contract mismatch is closed

Forge 0.4.1 itself rejects `aiProfile` with `slot:create` in `parseManifest()` before a job exists. Revision 2 removes both standalone profile-create items. The manifest now plans as exactly:

1. Road Bandit — `ai` create carrying `rules` and `includeDefaultRules:true`
2. Harvest Boar — `ai` create carrying `rules` and `includeDefaultRules:true`
3. One Perfect Crop — `quest` create

This is the runner-supported path. `rules` and `includeDefaultRules` are legal AI manifest keys, are omitted from the `profile.updateAi` record payload, and cause the runner to enter its `rules` phase. That phase reads the AI, toggles/creates the AiProfile row when absent, writes `ai.updateAiProfile`, and then the verification path reads the AiProfile separately. The two AiProfile records therefore still exist as intended; they are created through the owning AI workflow rather than represented as standalone create items.

The exact corrected manifest contains zero `aiProfile` manifest entries. Both AI items carry the approved three rules in approved kit order with gate value 6 and `includeDefaultRules:true`. The quest remains the same hidden-core quest payload; no new art/admin value was introduced.

### Offline Forge gate is materially coupled to production code

`forge/tools/check_manifest.mjs` imports Forge's actual `parseManifest`, `planOrder`, and pinned `Validator` rather than reimplementing those contracts. It opens no runner, transport client, job or socket. The staged-manifest test now uses that same helper, so the handoff gate and Forge test gate share the same parser/planner/validator path.

The focused regression tests cover both sides of the incident:

- standalone `aiProfile` create is refused;
- an AI create carrying rules remains valid and routes to the rules phase;
- `aiProfile` edit remains parseable;
- push/47 specifically plans as two AI-rule items plus one quest.

The existing runner test for an AI with rules exercises the full fake-game sequence through `profile.create`, `profile.updateAi`, profile toggle, `ai.updateAiProfile`, and separate profile verification, so the new manifest shape is not supported only by a display-only phase label.

### Python validator gap is closed

The content validator now rejects only `aiProfile` + create, with guidance to carry the rules on the owning AI. It does not reject the supported `aiProfile` edit/update path or AI creates carrying the rules envelope. `selfcheck.py` adds fixtures for all three cases.

### Test-suite exception is pre-existing and non-blocking for this correction

The handoff records `npm test` as 310 tests / 309 pass / 1 fail. I did not independently execute Node or Python commands in this connector-only review, so those counts remain handoff evidence rather than independently rerun evidence.

I did independently verify the surviving failure's premise against the exact base: `forge/test/release_loader.test.mjs` asserts that the development loader has exactly one `@x-release-pending` marker, while `main @ a45b576...` has no such marker after release-pin promotion. The correction diff does not touch `forge_loader_user.js`, `forge/package.json`, the release-pin script or staged workflow. This is therefore a pre-existing release-loader test-state mismatch, not a regression introduced by revision 2 and not a reason to alter the live loader inside this manifest correction.

It should be repaired separately by the release-plumbing owner so `npm test` can return fully green on `main` again.

## Minor documentation debt

`state/prompt_one_perfect_crop.md` still describes the semantic target as two AI records, two AiProfiles and one quest and uses the older five-item wording in parts of its implementation checklist. The semantic target is still met: Forge creates the two AiProfile rows through each AI's rules phase. The revision-2 handoff explicitly records the source-verified manifest-shape correction. This wording is stale implementation detail, not a hidden-run blocker, but should be updated the next time the brief is reopened so future implementers do not reproduce the retired standalone-create convention.

## Integration / production boundary

The reviewed SHA is a clean three-commit descendant of `main @ a45b576428d21bd7f24889a4965cf626d8dbf18a` with no divergence at review time.

**Approved next step:** integrate the exact reviewed target `6cce22e3fad0e08344cb2f3252bdf04909632983` to `main`, allow normal repository automation to rebuild generated skillpack output, then let dauntless reselect `push/47_one_perfect_crop_core_manifest.json` in Forge 0.4.1.

Selecting/preflighting remains non-mutating. The actual Forge run remains user-owned. After the hidden run, export and commit the Forge result/read-back evidence before treating the created records as verified. This PASS does not authorize publish/unhide and does not settle deferred art, rewards, Cabbage Seed economics, repeatability or eligibility.
