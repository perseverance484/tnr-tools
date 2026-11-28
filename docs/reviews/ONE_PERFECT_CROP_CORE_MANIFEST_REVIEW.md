# One Perfect Crop hidden core manifest — independent review

**Verdict:** PASS — no blocking findings on the frozen implementation SHA.  
**Review target:** `af0efc6cb7657ea8bf95f6aae414ea2ff5391a2f`  
**Implementation base:** `e35633160bdb7bb03238e30c22faf9f2b4af057c`  
**Implementation branch at handoff:** `claude/one-perfect-crop-manifest-9wsry6`  
**Reviewer:** ChatGPT / Engineering Auditor  
**Live-game requests/writes during review:** none.

## Scope reviewed

The audit targeted the frozen SHA, not the moving branch tip. The branch later advanced by an automated skillpack commit; that generated commit is not part of this audit target.

Reviewed the actual implementation and supporting evidence rather than relying on the handoff summary alone:

- `push/47_one_perfect_crop_core_manifest.json`
- `push/47_one_perfect_crop_core_manifest.gen.py`
- `docs/handoffs/ONE_PERFECT_CROP_CORE_MANIFEST_HANDOFF.md`
- `state/prompt_one_perfect_crop.md`
- `state/one_perfect_crop_core_manifest_override.md`
- `state/one_perfect_crop_prose_graph.md`
- `state/one_perfect_crop_combat_spec.md`
- modified `validate.py`, `factory.py`, and law-coverage row
- current builder behavior on the implementation base
- pinned game source `studie-tech/TheNinjaRPG@bdec2883` for AI defaults, quest defaults/rewards, AI default-rule behavior, and relevant validator semantics.

## Findings

No blocking correctness, safety, contract, or graph findings survived review.

### Manifest inventory and safety

The manifest contains exactly five creates: two AI records, two AiProfiles, and one quest. It creates no assets, items, or jutsu; contains no `@img` references; carries `dedupNames: true`; carries no `skipPreflight`; and contains no publish/unhide operation.

The quest is explicitly `hidden: true`. AI `hidden: true` is only a repository/builder safety marker because the AI user table has no hidden column; pinned source confirms the real arena-exposure field `inArena` defaults to `false`, and `profile.create` does not override that default. The hidden quest therefore remains the only reference path to the new AIs until a later launch decision.

### Combat contract

Both AI records match the frozen combat specification:

- JONIN, level 100
- regeneration 60
- stats/pools multipliers 1
- uniform twelve-stat ratio
- element None
- Strength / Speed preferred generals
- Road Bandit `preferredStat: Bukijutsu`
- Harvest Boar `preferredStat: Taijutsu`
- exact three-jutsu shared-pool kits in the frozen order
- no new jutsu, items, avatar, passive effects, or shared-AI edit.

Each AiProfile carries exactly the three frozen authored rules at distance gate 6 and `includeDefaultRules: true`. Pinned `ai_v2.ts` confirms that `includeDefaultRules` causes the engine backup rules to be appended, so a bespoke authored movement/highest-power fallback is correctly absent.

### Quest graph

The manifest implements the frozen 36-objective zero-travel graph with one start and no dangling or authored reset/retry path. Both encounters are dialog-gated `start_battle` nodes, one enemy each, scaled to the user, and each battle loss hard-routes to its dedicated `fail_quest` terminal. F1-F4 remain sealed away from the PASS spine.

All dialog forward edges are choice arrays. `consecutiveObjectives: true` is at quest data level. Delivery acceptance precedes the cabbage catastrophe and the win node.

### Deferred placeholders

The hidden-core deferral is implemented rather than silently resolved:

- no Cabbage Seed item or grant
- no final Ryo/XP/token reward choice
- no Farming-level substitution
- no final repeatability policy
- no asset entries or art uploads
- no final scene wiring.

Pinned quest source confirms `quests.create` seeds `image` with `IMG_AVATAR_DEFAULT`, so omitting the listing-image field preserves an actual create-path placeholder. Pinned reward validators confirm an empty `content.reward` parses to zero/empty prefault values. Blank scene fields are schema-valid and are explicitly permitted for this hidden-core stage by the director override.

### Shared-tooling changes

The task necessarily touched shared tooling; those changes were reviewed as Lane A surface within this exact SHA:

- `validate.py` now scopes law 41's terminal-rule requirement to `includeDefaultRules: false`. This matches the canonical law text and pinned AI source behavior. The dead-rule-above-terminal check remains intact.
- `factory.py` renames the first `objective()` parameter from `task` to `member`, allowing shared union members such as `InstantWinLoseObjective` to receive their actual `task` enum value. Existing positional callers are unaffected; the generated terminal objective shapes are correct.
- the law-coverage row was updated consistently.

No separate generated contract was regenerated or adopted.

## Validator and gate evidence

The handoff records the exact commands and results at the frozen SHA: manifest validation `0 errors, 2 warnings`, parity `16/16`, law tests `4/4`, factory self-test `20/20`, repository selfcheck `0 errors`, lawmap `0 errors` with five pre-existing warnings, doctrinemap `0/0`, and doctrine/pack checks current.

The two manifest warnings are the known all-60-AP kit warning for each AI. They are not an implementation defect: the frozen combat contract deliberately specifies those kits and relies on `includeDefaultRules: true`; changing the kit would violate the approved content contract.

This connector-only review did not independently execute the shell commands. I independently inspected the actual payload, generator, tooling diff, builder behavior, and pinned server source; the recorded executable gate results are corroborating handoff evidence rather than the sole basis for this verdict.

## Integration note

After the frozen handoff, the branch received automated commit `8f4298b74978beaad5d1cf169c0ea56a5a6b9285`, which changes only `dist/building-tnr-content.zip` via the repository `skillpack` workflow. Do not substitute the moving branch tip for the audited implementation SHA. If integrating this review lineage, preserve `af0efc6cb7657ea8bf95f6aae414ea2ff5391a2f` as the reviewed implementation target; the normal main-branch skillpack workflow can regenerate the deterministic ZIP after the reviewed source changes land.

## Production boundary

PASS means the hidden core manifest is repository-integration ready and may proceed to the user-owned hidden Forge execution/readback step if the user chooses. It is **not launch-final** and must not be published/unhidden. Art, Cabbage Seed, rewards/economics, repeatability, eligibility, final scene wiring, and the eventual publish decision remain deferred under `launch.finalization`.
