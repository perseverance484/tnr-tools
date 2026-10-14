# Fable brief — QW-0A continuation: extractor fidelity and diff-gate hardening

**Status:** ORCHESTRATOR-ISSUED, 2026-10-14. **Slice A is ready for Fable implementation. Slice B is specified but queued behind A's review/integration.** ChatGPT authors and issues this bounded engineering assignment under the user's instruction to plan and orchestrate the remaining pass. This is not a new director ruling or contract-adoption approval.

**Repository:** `perseverance484/tnr-tools`

**Implementation owner:** Fable / Claude Code, on its own `fable/*` branches.

**Independent reviewer/orchestrator:** ChatGPT, Release Auditor with Engineering Auditor review.

**Outcome boundary:** repair the tools that produce and compare evidence. QW-0A alignment remains `BLOCKED_BY_SOURCE_ADOPTION`; neither slice changes the adopted contracts.

## 1. Authority and exact starting evidence

| Source | Reference |
| --- | --- |
| Verified main, 2026-10-14 | `1da18301e8e4660cedf3daa3e80893a2ac918f2b` |
| Documentation base for this brief | `chatgpt/qw1-integration-checkpoint-20261014@7a9578d42dfff0e0cbb61c6430c84f3bc30436eb` |
| Approved plan, original QW-0A brief, RUL-016 | `chatgpt/quest-workflow-skyglass-retrospective-20261012@c34f7de572337b0d2cfe397b9331502aa6548e27` |
| Integrated QW-0A report | `5fefb70b88f140c3212d0b9d94209e70be44f2bb` |
| Integrated QW-0A independent review | `e2c10ee1717d1311951bc8a7f6e621229ebf4b5f` |
| Existing stamped game-source pin | `studie-tech/TheNinjaRPG@bdec2883748f029a0ecb93505adfdcbae6851fe9` |
| Release-tested comparison pin | `studie-tech/TheNinjaRPG@585534d7eb21d6f0dd678d5c3eb92662f611d39b` |

Reverify remote refs before starting; record the actual base and merge-base. Create `fable/qw0a-extractor-fidelity-20261014` from fresh main. Read this brief at its committed SHA without merging the separate planning branch. Do not repurpose the frozen QW-0A report or QW-1 branches.

Read `docs/00_INDEX.md`, `CLAUDE.md`, `CHATGPT.md`, `docs/DEVELOPMENT_WORKFLOW.md`, `docs/agents/README.md`, the review/handoff workflows, and the routed D-adopt-gate/D-tool-canon rules. Read the approved plan, original QW-0A brief and RUL-2026-10-12-013 through -016 with `git show c34f7de572337b0d2cfe397b9331502aa6548e27:<path>` where absent from main. Then read:

- `docs/reviews/QW0A_CONTRACT_ALIGNMENT_REPORT.md`;
- `docs/reviews/QW0A_CONTRACT_ALIGNMENT_INDEPENDENT_REVIEW_2026-10-12.md`, especially R1/R2;
- their committed evidence directories, `schema_extract.py`, `schema_diff.py`, and their consumers/fixtures;
- `.github/workflows/regen_schemas.yml`, `.github/workflows/skillpack.yml`, and `.github/scripts/pack_skills.py`.

The old report's “only element correction” / “only G1-G4” limits are withdrawn. Its section 9 is evidence, not a competing implementation contract. This brief carries the accepted review refinements and divides the continuation into separately reviewable slices.

## 2. Sequence and ownership

1. **A — extractor fidelity:** Fable implements the source-reading repairs and complete correction inventory below; freezes one SHA. ChatGPT independently reviews code, pinned source, tests, inventory and generated evidence. Corrections return a new frozen SHA.
2. **A integration:** prepare the concrete merge/checkpoint after review passes and obtain the applicable acceptance/integration authorization. Recheck main and review-head identity immediately before integration. Do not rebase a frozen target without returning a new SHA for review.
3. **B — diff-gate hardening:** after A's accepted integration, ChatGPT issues the next start instruction against that fresh base. Fable uses a new branch and the B requirements below. B gets its own frozen review, correction loop and integration checkpoint.
4. **Adoption decision packet:** use the corrected tools to present the complete prospective contract delta, remaining incompatibilities and a concrete D-adopt-gate proposal if needed. ChatGPT prepares this for the user; no policy is selected by the tooling implementation.
5. **Later alignment slice:** only after the source-selection/adoption decisions are resolved, write a separate bounded contract/validator/factory/Forge-parity brief. Its acceptance must prove agreement at the chosen pin, preserve historical exception evidence and cover new/legacy payload compatibility. Passing A and B alone cannot close QW-0A.

Begin A now. Do not wait for the adoption decision to repair evidence production. Do not implement B in the same branch or start it automatically. Routine implementation details within this brief belong to Fable; a necessary expansion beyond these boundaries returns as a specific, evidenced proposal.

## 3. Slice A — extractor fidelity

Primary owner: `skills/building-tnr-content/scripts/schema_extract.py`. Prefer extending its existing balanced parsing/resolution helpers. Keep extraction static and local; do not run the game, evaluate TypeScript, add a general interpreter or introduce a new parser/runtime dependency.

Cover the constructs proved relevant at **both exact pins**:

1. Resolve array spreads in exported/local constants and inline `z.enum(...)` expressions, including transitive references. This includes `ElementNames`, `allState` (`publicState`/`privateState`) and `damageModifierTypes` (`damageReductionTypes`/`damageBoostTypes`). Preserve semantic source ordering; do not sort source enums to simplify comparison.
2. Parse multiline field expressions and multiline `z` / `.object(...)` schema heads without truncating the next field or declaration. Respect strings, comments and balanced delimiters.
3. Resolve the referenced, source-verified helper definitions from `app/src/validators/base.ts`, including the actual omission/nullability behavior of `makeCappedNullableNumber`. Do not describe all mastery inputs as `.prefault(...)`.
4. Handle the relevant `msg()` and `type()` helpers, including inherited description/direction fields, without mistaking an adjacent helper's body for the current one.
5. Resolve `...rewardFields` and other object spreads required by these constructor/entity outputs, including cross-module references, local overrides and transitive dependencies.
6. Preserve the existing contract structure and accurately represent supported type, literal, enum/reference, default/prefault, optionality, nullability and bound facts. Distinguish absent metadata from explicit `false`, `0` or `null`; justify each changed fact against source. Omission acceptance and its mechanism must be separately clear in the inventory.

Unresolved/cyclic dependencies in these supported constructs must produce a named diagnostic and a nonzero extraction result rather than silently dropping fields or emitting `...Name` as an enum member. Do not claim arbitrary Zod/TypeScript coverage. Any additional unresolved source form affecting the audited outputs must be listed with its source location and consequence; unresolved material semantics block a claim of complete fidelity/adoption. If representing a fact requires a consumer-visible format extension, propose it with the exact consumer impact rather than quietly adding a second contract format.

### A evidence and regression requirements

Add focused, socket-free tests and minimal fixtures for the constructs above. Include cross-file resolution, nested spreads, precedence, missing references, cycles, multiline delimiters and omission-vs-nullability cases. Assertions must check expected fields/values and refusal behavior, not merely compare the implementation with its own freshly generated output. Demonstrate that the known-bug cases fail with the baseline extractor for the intended reason.

For **each** pinned source, run constructors first, then entities/constants/checks, in scratch. Record source SHA, source-file hashes, commands, exit codes and output hashes. Source may be retrieved from public Git/source archives; never substitute moving upstream HEAD or infer deployed production from either pin.

Commit a complete source-cited inventory with three separate comparisons:

- baseline extractor versus corrected extractor on `bdec2883`;
- baseline extractor versus corrected extractor on `585534d7`;
- corrected old-pin output versus corrected release-pin output (actual upstream changes).

For every structural correction, identify contract path, before/after value, classification, and source SHA + file + declaration/line anchor. Inventory **full payload changes**, including fields that today's atom diff misses: existence, type, enum members/references, defaults, literals, bounds, optionality and nullability. Explain metadata/provenance changes separately. Keep an untruncated machine-readable inventory; a phone-sized diff excerpt is insufficient. Do not force the inventory back into the old G1-G4 list.

Run the unchanged invariants/diff gate on scratch candidates and record each unmasked exit. A nonzero adoption diff is expected evidence, not a failing extractor test to “fix” by suppressing removals. A zero result still has the known R2 blind spots until B. Investigate an invariant failure; do not present it as a passing candidate.

Reproduce outputs with identical source and declared provenance inputs. The current extractor's date/source-drop metadata can vary; report full-file hashes and structural-payload hashes separately, explicitly naming excluded metadata. Do not promise byte identity across different provenance dates/labels or delete provenance to manufacture it. Include the transitive helper/source files in the evidence provenance.

### A permitted changes

- The extractor, focused test modules beside it, and new minimal fixtures under `skills/building-tnr-content/data/fixtures/qw0a/`.
- Task reports/evidence under `docs/reviews/`, with a clearly separate continuation directory, and narrowly necessary usage documentation.
- Reproducibly generated skill ZIP changes required by the existing pack workflow; no hand-edited ZIPs. Explain any generated delta outside the changed skill.

`schema_diff.py` is unchanged in A. Existing negative fixtures are preserved; new fixtures must not replace an old failing example with an easier one. Large temporary source exports and candidate 45x contracts stay in scratch; commit the reproduction recipe, compact relevant fixtures, hashes and complete correction inventory, not a second adopted contract tree.

## 4. Slice B — diff-gate hardening (queued)

Primary owner: `skills/building-tnr-content/scripts/schema_diff.py`, with focused tests/new fixtures/report and required skill packaging. Consume A's reviewed output semantics. Keep existing removal/type prohibitions; no ignore flag, exception allowlist, removal ledger implementation or weakened exit policy belongs here.

Required behavior:

| Probe | Required outcome |
| --- | --- |
| Remove `AllTags.damage.power`, including a non-enum union field | exit 1; name the removed field |
| Change that field from `number` to `string` | exit 1; name old/new type |
| Tighten `item.requiredStrength.nullable` true to false | exit 1; name the nullability tightening |
| Tighten an existing union field's nullability | exit 1, using the same semantics |
| Add a genuinely required input to an existing entity/variant | exit 1; describe a newly required input, not a prior optional field |
| Make an existing omissible input required | exit 1; distinguish this tightening from a new field |
| Add an explicitly optional input, or relax requiredness/nullability | exit 0 when no other break exists; describe the change |
| Remove/replace enum members, including equal-size replacements; remove a variant or existing field; change an entity field type | retain exit 1 |

Use complete, unambiguous paths for entity and union-variant fields. Preserve source-member order in extraction; gate comparison remains by member value. Type information disappearing from an existing typed field must not silently bypass the type check. Missing/ambiguous optionality or nullability facts are not proof of safety; expose an explicit unresolved/blocking result where source semantics cannot be established.

Classify omission from supported contract facts verified in A, including defaults/prefaults and proven preprocessors. Nullable does not mean omissible. A new genuinely required field must keep failing even after the misleading `now-required` label is fixed. Add positive and negative fixtures for optional, required, defaulted and preprocessed cases. If the emitted format cannot prove an addition safe, keep the gate conservative and state the limitation; do not guess from raw source snippets or from absence in the old contract.

Preserve established additive cases, including new enum members/variants, and all existing negative fixtures. Distinguish adding an entirely new variant from adding a required input to an existing variant. Report any discovered conflict between existing new-entity behavior and its documented additive claim before relaxing a refusal; that ambiguity is not permission for a broad gate redesign.

Reproduce the three R2 baseline false negatives independently, then show the repaired gate rejects each. Demonstrate the genuine-required-input test already fails on baseline and still fails with the corrected diagnostic. Check useful positive controls so “reject everything” cannot pass the suite. Run the corrected gate over A's full two-pin evidence; report the actual delta and remaining adoption blockers without changing contracts.

## 5. Shared verification, packaging and freeze

Record actual commands and unmasked exits. Keep expected-negative outcomes distinct from unexpected failures.

1. Run the slice's focused regression tests, existing sector-removal/additive/bad-invariant fixtures, and Python compilation with bytecode outside the checkout.
2. Run each historical exception gate separately in check mode: `python3 push/90_ghost_ship_skyglass_release.validate_exception.py`, `python3 push/93_ghost_ship_guardian_repair.validate_exception.py`, and `python3 push/94_ghost_ship_skyglass_sentinel_repair.validate_exception.py`. All must retain exit 0 and their exact historical ledgers. Do not regenerate the ledgers.
3. From the skill's `data/` directory, run `factory.py --selftest` and `validate.py --laws` through their script paths. Run `build_packs.py --check`, `lawmap.py <repo>`, `doctrinemap.py <repo>`, and `render_doctrine.py --check` from `skills/building-tnr-content/scripts/`. Explain baseline warnings rather than rewriting unrelated doctrine.
4. Build skill ZIPs using `.github/scripts/pack_skills.py` with all intended source/test/fixture files tracked. Verify repeated-build hashes, the 2 MiB bounds and that the changed skill's shipped scripts match reviewed source. Do not run contract-regeneration/adoption workflows to obtain a green bundle.
5. Compare protected paths against the actual fresh-main base. Canonical 45x files/root mirrors, validator/factory/Forge sources, historical manifests/ledgers/gates, existing workstreams and global session projections must be unchanged. If a background workflow changes a protected path, investigate it before freezing.

The active schema-sentinel workflow extracts scratch candidates and commits only drift signals; it does **not** adopt contracts. The skillpack workflow runs on `skills/**` pushes and can commit ZIPs/root mirrors. Leave both workflows unchanged. After push, account for any generated commits, rerun affected checks as necessary, then verify the **actual remote head** and freeze it. Any subsequent change requires a new handoff SHA. Do not call a pre-packaging SHA the final review target.

Forge code is out of scope, so no Forge version bump, loader repin or gameplay release is part of this pass. Unrelated art/browser/Android/live tests are not required. Do not broaden verification without a concrete changed dependency or required repository gate.

## 6. Protected boundaries and known debt

Do not modify adopted `45c/45d/45e/45f/45g/45h` contracts (or other canonical 45x artifacts), root mirrors, `validate.py`, `factory.py`, Forge field tables/preflight, doctrine/rulings, historical `push/90/93/94` manifests or exception ledgers/gates. Contract regeneration in scratch is evidence only. Repairs to extraction/comparison do not adopt contracts, resolve Python-versus-Forge source-pin divergence or certify deployed behavior.

No game requests, game writes, credentials, source execution, publication or reward/gameplay changes. Do not run `session_open.py` or `session_close.py` against the global September state; preserve `state/digest.json`, `state/active-context.md`, `state/status.json` and existing workstreams. Use the committed Lane A brief/reports/handoff; do not create a second task authority or a real quest roadmap.

Keep separate: QW-0B version correction; crafting-relation capture; spent-manifest archive/audit; One Perfect Crop's removed push/54 evidence pointer; Rare Jewels canonical/live reconciliation; mandatory-workstream policy; QW-2 through QW-5 and Quest Studio. QW-1 is already closed. Its known nontransactional write/piped-next behavior is not a continuation defect. Repository-wide workstream validation is not green because of the pre-existing One Perfect Crop pointer; do not repair it or add a bypass here.

## 7. Required frozen handoff and next review

Follow `docs/workflows/IMPLEMENTATION_HANDOFF.md`. Include:

- implementation branch, exact base/merge-base/head, verified current main and committed brief SHA;
- source pins, changed paths, behavior, source inventory, fixture/generator commands, full and structural hashes, and any provenance normalization;
- positive/negative test results, gate exits, baseline comparison, package fidelity and unchanged protected-path evidence;
- remaining unsupported source forms, justified deviations and the exact questions the reviewer should attack;
- `EXTRACTOR_REVIEW_READY` for A or `DIFF_GATE_REVIEW_READY` for B only when supported by evidence, alongside the overall `BLOCKED_BY_SOURCE_ADOPTION` status;
- no adoption/integration/later-slice claim, and explicit live requests/writes/credentials: `0 / 0 / none`.

ChatGPT reviews the frozen code and independently reproduces the important claims, records PASS or actionable findings on `chatgpt/*`, then drives the next correction/integration instruction. The author never resolves its own independent-review gate. Final integration uses a fresh-main check, preserves one-writer ownership and existing acceptance authority, and records the resulting merge SHA plus bounded post-merge verification.
