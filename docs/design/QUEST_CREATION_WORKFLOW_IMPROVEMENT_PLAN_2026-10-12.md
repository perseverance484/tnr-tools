# Quest creation workflow improvement plan — Ghost Ship / Skyglass retrospective

**Status:** PROPOSED for director review. This is an advisory design/workflow plan, not implementation authority or new gameplay canon.  
**Repository:** perseverance484/tnr-tools  
**Reviewed baseline:** main@4de2668bb947368113683b5cb97e197abc87df27 (2026-10-12).  
**Roles:** ChatGPT — independent workflow audit / Content Designer; Fable — normal Lane A tooling implementation; director — final scope, content, rewards, art and live-game decisions.  
**Safety:** Repository evidence and supplied offline closeout archives only; zero agent live-game requests/writes, zero publication; no credentials.

## Goal

Make it easier to create a new TNR quest or multi-session quest expansion without repeatedly reconstructing the same decisions, copying engine fields by hand, missing an art dependency, trusting stale contracts, or discovering partial release failure only after an operator push. A normal small quest must remain lightweight; the richer process is for content that actually needs it.

**Do not add a second quest engine, source of truth, Studio, validator or session dashboard.** Extend what already exists: `docs/00_INDEX.md` and `docs/DOCTRINE.md` (authority), `docs/workflows/CONTENT_WORKSTREAM.md` and `scripts/content_workstream.py` (multi-session coordination), the content skill's `factory.py` / `validate.py` / `mission.py` / `storyboard.py` (construction and checks), canonical captures and source-generated contracts, Forge's current runner/reconciler, and the accepted-but-unintegrated Quest Studio foundation.

## Findings and evidence from seven unique closeouts

| Observation | Evidence anchor | Workflow consequence |
| --- | --- | --- |
| Scope moved from a 57-node retheme to 83-node, six-ending expansion, while an older handoff ZIP and wholesale shared-pool design remained in circulation | `state/ghost_ship_skyglass_expansion_design.md`; `state/ghost_ship_skyglass_graph_patch.json`; `state/ghost_ship_hybrid_kit_proposal.md`; RUL-2026-10-10-003 / RUL-2026-10-11-003 | Track supersession and dependencies; mark packages historical instead of treating the newest chat as canon |
| Ten approved item prose fields could be frozen independently of mechanics; optional effect presentation remained null | `state/ghost_ship_skyglass_release_presentation.json`, approved at 224ab918… | Require evidence-backed approval gates without inventing optional details |
| Thirty-four exact approved art WebPs were processed and bound; earlier art handoffs still described some assets as raw/pending. GS-B06 raw and processed hashes lack an explicit raw-to-derivative linkage in the final ledger | `art/ghost_ship_skyglass/_provenance/`; `state/ghost_ship_skyglass_release_art.json`; supplied GS-B06 raw closeout | Make lifecycle and source-to-derived identity legible; do not regenerate art already shipped |
| Historical combat Stage 2 r2 passed but produced wrong conclusions: missing battle-start caps, incomplete cadence/delayed-damage accounting and inadequate failure enforcement. r3/r4 fixed the evidence system | `docs/handoffs/GHOST_SHIP_SKYGLASS_STAGE2_OFFLINE_HANDOFF.md`; `docs/reviews/GHOST_SHIP_SKYGLASS_STAGE2_OFFLINE_RESULTS.md`; `harness/ghost_ship_stage2/` | Offline battle tests must be engine-faithful and fail closed; a green gate is bounded to what it actually proves |
| Release required an exact SHA-bound exception because generated 45c/45d and `validate.py` lagged the newer engine; the latest upstream sentinel is only a drift signal | RUL-2026-10-12-013; `state/ghost_ship_skyglass_release_validate_exception.json`; `docs/DRIFT.md`; `state/schema_sentinel.json` | Reconcile source-derived contracts through the existing mechanical adoption gate before broadening tooling; do not generalize temporary exceptions |
| push/90 had 48 matches, one unverifiable crafting-relation drift, and a name collision *after* kit synchronization. A second rename collided; push/94 fixed it with 3/3 verified readback. Both quests remained hidden | `docs/handoffs/GHOST_SHIP_SKYGLASS_RELEASE_MANIFEST_HANDOFF.md` `8; `harvests/inbox/tnr_results_1791780626532.json`; `harvests/inbox/tnr_results_1791780861916.json`; RUL-2026-10-12-014/015 | Treat composite update failure as potentially partial; improve name-coverage preflight, relation-aware readback and surgical operator-controlled recovery |
| Player showcase closeout reports a newer director change: Rare Jewels are chance-based, up to three, whereas historical push/90 and reward decisions encode three guaranteed. Graphic QC and Discord publication were not approved | Supplied `ghost_ship_skyglass_player_showcase_closeout.zip`; `state/ghost_ship_skyglass_reward_decisions.md`; `push/90_ghost_ship_skyglass_release.json` | Mark canonical/live discrepancy explicitly. Do not render disputed guarantees or publish before user-supplied confirmation |

**Evidence tiers:** release and harness outcomes above come from committed results/reports; the new Rare Jewels change is director-reported, *not* proved by a later committed full live read. Source pin `studie-tech/TheNinjaRPG@585534d7eb21d6f0dd678d5c3eb92662f611d39b` governs the Ghost Ship release checks; deployed source version is not independently established. Main advanced after release with an upstream drift sentinel at `6e4429d65f466b0df9fca3f9917b6dd427df7573`. Do not equate either sentinel or stamped contract with deployed live behavior.

## Preserve current architecture and authority

- `docs/00_INDEX.md` decides precedence. `docs/DOCTRINE.md` owns cross-surface doctrine; `docs/ENGINE_LAWS.md` the numbered engine laws; `docs/RULINGS.md` historical decisions, not operative substitute. Generated contracts describe shapes, captures describe live records, task-specific approved content sources describe intent.
- Preserve the two Git lanes, one-writer branches and exact frozen SHA reviews under `docs/DEVELOPMENT_WORKFLOW.md`. Routine Lane B quest manifests do **not** all require Lane A review.
- The operator alone runs the game and decides publication. Every new entity is hidden. No speculative live queries or credentials in offline tools.
- Global `state/active-context.md` and `state/status.json` deliberately remained at a September Forge checkpoint during Ghost Ship. Do not hand-edit or automatically overwrite these generated projections to repair a quest-specific status. Put quest coordination in `state/workstreams/<slug>/roadmap.json`, and label source freshness.
- The reviewed Quest Studio foundation `chatgpt/forge-quest-studio-foundation@5ba636d85fe2dbd4e4bf0e2baa6070cdd7321b15` is not integrated. Its Mission compiler and source-push worker are references, not evidence that Event/Story/Battle Pyramid compilation already exists on main. Respect `docs/forge_next/G_ROADMAP.md` (Phase S and Phase W) and the existing Phase 1 brief; do not preempt their prerequisites or build a second compiler/Studio.

## Proposed work packages (in delivery order)

### QW-0 — Close correctness gaps before wider use (Lane A; Fable)

1. Reconcile current `45c` / `45d` / `45g`, `validate.py` and Forge field/lint expectations against an explicitly chosen, pinned upstream source; begin with the known post-0056 Ghost Ship discrepancies. Run `schema_extract.py --ctors`, `schema_diff.py --invariants` and per-file `schema_diff.py diff`, review removals/changed types, then adopt only after the gate and tests. The latest upstream sentinel is *not* an adoption instruction. Keep SHA-scoped historical push/90/93/94 exceptions intact as audit history; do not make them a generic bypass.
2. Correct the Forge UI version constant (`forge/src/main.mjs` reports 0.5.1 while loader/package is 0.5.2) using the established release/build version source and regression checks.
3. Prepare a separate audited readback extension for `item.getItemWithCraftingRequirements` (if that procedure is permitted and sufficiently source-verified). Check persistence-policy classification under existing Forge Next Phase 1 registry/tier authority; never add a generic unrestricted endpoint.
4. Queue spent-manifest archiving and a post-release offline audit of the 8 other Ghost Ship AIs/hazards/items. Treat these as release hygiene, not as requirements to rewrite historical results.

**Acceptance:** normal new-format manifest validation and Forge preflight agree; post-0056 fixtures pass; drift/adoption and negative tests run; no runtime version ambiguity; no new source-derived field silently accepted; zero network calls. Any unresolved contract class remains explicitly blocked, not suppressed.

### QW-1 — One-command quest workstream starter (Lane A; Fable)

Extend `scripts/content_workstream.py` with a deterministic `new`/scaffold operation for a multi-session `quest`/`event`, plus small versioned template(s). Keep current `validate`, `render`, `next` and `init` semantics and current roadmap as the *only* coordination source.

Suggested task stages (only when needed): **design/graph → source/capture inventory → enemy/loot decisions → art/prose production → compile/validation → independent review where applicable → operator hidden run/readback → testing → publication decision**. Require each stage to point to actual source files; label unresolved director decisions, missing captures and superseded prior packets. Distinguish raw art approval from production acceptance, binding and readback. Link to canonical art and prose sources, never copy those sources into the roadmap.

Provide a compact handoff/freshness report: base and target SHAs, current stage, required artifacts, blockers, approval state and next executable session. `READY` must remain repository-executable, `COMPLETE` must retain a verifiable anchor, and stale ZIP-only inputs cannot make a task ready.

**Acceptance:** initialize an example Ghost Ship-scale roadmap from a clean checkout without relying on chat; simulate missing files/superseded briefs and verify fail-closed status; byte-identical generated projections; existing One Perfect Crop roadmap/tests remain green; a simple one-session quest still works without creating a roadmap.

### QW-2 — Reusable quest blueprint and variant compiler (Lane A; Fable)

Design one approved, versioned **Quest Source/blueprint** for a shared objective graph with explicit operator-approved variations (for example, Gather vs Hunt reward rows and quest-level fields). The authored model is an input to the existing `factory.py` / validator, not a competing engine schema. Extend the existing Studio compiler architecture only at its approved integration boundary, or prototype a repository-only adapter first.

Generate objectives, edges, ending-to-reward mapping, required asset slots and manifest entries deterministically from that one source. Every structural/prose/reward change produces a human-readable before/after diff, keeps original objective identities on edits, and highlights user-owned numbers instead of choosing them. Retheme-only versus expansion deltas must stay distinguishable. Built-in graph checks use the existing quest reference and validators, including dialog-gated `start_battle`, reachability, resets and one-start constraints; no copied JavaScript rulebook.

**Acceptance:** source fixture modeling the two 83-node/six-ending Ghost Ship variants compiles deterministically into two correct independent quests; the 57 original node IDs are preserved where required; source-approved endpoint/reward differences are explicit; graph failure fixtures reject wrong links, cycles, orphan resets, missing battle failure paths and accidental reward-path leaks; no edit writes are sent by the compiler.

### QW-3 — Preflight, honest readback and partial-write recovery (Lane A; Fable)

Add a **release-readiness report** over existing captures/answers, source pins, Forge preflight and planned mutations:

- Name collision checks carry evidence coverage (`collision` / `not seen in captured scope` / `unknown`), not fabricated proof of global uniqueness. If census is incomplete, require an explicit operator decision before a rename rather than claiming it is safe.
- Flag captured-record freshness, protected-field preservation, AI kit/jutsu consumer impacts, changes to approved rewards, manifest source pins and installed-Forge minimum version.
- Planned reward descriptions/infographic data can read verified authoring values, but a conflicting newer director report or unverified live relation becomes `DISPUTED`/`UNVERIFIED`, not a guaranteed value.
- After a Forge run, compare expected and captured before/after state per entity. Classify `MATCH`, `DRIFT`, `UNVERIFIED` and `FAILED/PARTIAL` without treating HTTP 200 or a pre-write kit sync as a successful whole update. For unobservable relations (e.g. recipe via `item.get`), do not assert verification.
- Generate an **offline, surgical recovery proposal** identifying residual fields and old/new hashes. It must never auto-run, auto-retry, promote or publish; director/operator confirms any live action.
- Once safely archived, spent manifests must not appear as executable work in the normal selector.

**Acceptance:** synthetic Sentinel duplicate-name fixtures, kit-applied/rename-refused partial AI edit, Guardian second collision, relation-absent recipe, partial/failed capture and stale manifest scenarios each produce truthful operator-readable statuses and safe targeted recovery options. Negative tests fail closed. No game requests/writes from tests or agents.

### QW-4 — Targeted combat evidence and art/presentation provenance (Lane A; Fable for tools, ChatGPT for content/art review)

**Combat:** make the Stage 2 r3/r4 harness corrections reusable as a small optional test recipe for bosses/custom effects, not a mandatory simulation for routine quests. Run actual battle-start preprocessing/caps, define whole-step damage and measurement windows, assert that evidence failures cause nonzero exit, distinguish negative-probe infrastructure failures from enforcement, pin engine revision and label unmeasured settings/placement/party effects. Mechanical pass ≠ balance acceptance ≠ live calibration.

**Art:** retain the existing art skill/spec, approved-reference selection and one-at-a-time QC. Add traceable raw SHA → process/spec revision → processed SHA → preflight → director acceptance → entity binding → operator readback where applicable; reconcile historical shotlists to current bindings before any new generation. Source-lock assets for player presentations; do not AI-redraw approved art or equate a contact sheet with underlying approved bytes.

**Player copy:** use a small factual QA checklist for guide/showcase artifacts: correct name, quest state, endings, chance-vs-guarantee language, secret/spoiler boundary and only exact approved art. Do not introduce a second reward canon or a universal infographic format; task-specific ratios/text limits belong in the presentation handoff. Binary posters stay generated deliverables unless existing art rules say otherwise.

**Acceptance:** altered source bytes fail hash checks; a raw-approved-but-unprocessed asset cannot pass the production gate; a misreported guaranteed Rare Jewels row is flagged given the current conflicting evidence; a rejected graphic remains pending, not published; no feature claims exceed the offline evidence.

### QW-5 — Quest Studio projection/UI (later; existing Forge Next phases)

Only after the approved Forge Next prerequisites and frozen-source reconciliation: integrate the already reviewed Quest Studio foundation into the common Forge preflight and runner, then extend supported subtype adapters one at a time. Keep Forge the mobile authoring/preview/review surface and repository tools the compiler and validation owner. Reuse the approved `studio/quest/*` source-push boundary, provenance and credential policy; do not add another run path or enable game writes from a compiler.

An initial read-only project workspace projection may expose the QW-1 roadmap in Forge per existing Phase W; it must show source SHA and freshness and store no separate task status.

**Acceptance:** Quest Studio authoring and results use one runner/validator, commit- and source-identical build artifacts, recoverable worker refusals, and a zero-live-request repository rehearsal. Rollout sequencing remains the director-owned Forge Next decision.

## Delivery sequence and gates

| Order | Slice | Initial implementation ownership | Review/acceptance |
| --- | --- | --- | --- |
| 1 | QW-0 contract/validator debt, in narrow independent changes | Fable / Lane A | ChatGPT exact-SHA audit; director resolves any source adoption exception |
| 2 | QW-1 reusable workstream starter | Fable / Lane A | ChatGPT; director judges whether creator workflow is actually simpler |
| 3 | QW-3 preflight and recovery | Fable / Lane A | ChatGPT adversarial review; operator-controlled end-to-end evidence |
| 4 | QW-2 quest blueprint / variant compile | Fable / Lane A | ChatGPT schema/graph review; director accepts authoring experience |
| 5 | QW-4 targeted combat, art and presentation checks | Split into small independent tools/reviews | Fable tooling, ChatGPT art/content QC, director final acceptance |
| Later | QW-5 Forge Quest Studio UI | Existing Forge Next roadmap owner | Existing freeze, decision and independent-review gates |

QW-1 can be designed alongside QW-0; QW-2 blueprint design can precede code but must not invent a rival Quest Source authority. Do **not** batch all six slices into one Fable implementation branch or one Forge release.

## Director decisions and current publication boundary

1. **Approval sought:** adopt the ordered QW plan as a *proposal*, then freeze each implementation pass separately in a `state/prompt_<task>.md` brief. None is approved merely by inclusion here.
2. **Recommended default:** workstream starter is optional for routine single-session quests; strongly recommended for multi-session quests/expansions. Decide if compulsory at scale.
3. **Recommended default:** incomplete name/consumer census is displayed as *unknown with explicit operator acknowledgement*, not automatically treated as absent or as a claim of uniqueness. Decide whether to make the preflight stricter for named critical edits.
4. **Separate existing content discrepancy:** director-reported Rare Jewels chance-based/up-to-3 conflicts with historical guaranteed-3 repository source. Preserve the director's correction as a reported fact; obtain an authorized fresh, relation-complete operator readback and reconcile the owning current reward record. Until then, don't issue public guaranteed-drop claims. This does not authorize a reward change.
5. **Publishing:** both Ghost Ship quests are recorded hidden after push/94; no authorization to unhide/post follows from this plan or the earlier release.

## Test and change discipline

Every implemented pass: verify new main/ref and merge base; branch under its sole owner; tests and negative controls appropriate to the touched scripts; `content_workstream.py --selftest` and `validate/render --all --check` when workstream tools change; doctrine/pack/law parity checks when their owners change; Forge tests/build/budget/release pins when Forge code changes; art preflight on actual byte changes; reproducibility checks on generated files; zero live-game requests by agents. Freeze exact SHAs for independent review and integrate only after gates and required director rulings.

**Not authorized here:** gameplay balance edits, the Rare Jewels reward change, historical manifest rewriting, modifying global generated session-state projections, publishing/unhiding, automatic game calls, unsafe contract adoption, merging the unintegrated Quest Studio branch, or modifying another agent's active branch.

