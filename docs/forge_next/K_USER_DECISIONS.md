# K. Open user-decision register

**Status:** planning. Nothing here is settled by this package. Each entry follows `docs/workflows/DIRECTOR_DECISIONS.md`: what must be chosen, why it matters, the evidence, the options with consequences, an advisory recommendation where one is justified, whether the decision can be deferred, and which roadmap phase (section G) it blocks. Once ruled, an entry is recorded in `docs/RULINGS.md` and the operative rule moves to its canonical owner.

The brief reserves eleven decisions in its section 14; they are carried here as K-01 to K-05 and K-07 to K-12, each keeping the brief's wording. K-06 (capture data classification and what may persist to the public repository) is not one of the eleven: it was surfaced by the deep dive and is numbered in that run for continuity. K-18 and K-19 are not used: the numbering jumped when the register was split between the brief's reserved set and the questions the evidence raised, and the gap is left rather than renumbering entries other sections already cite. K-13 onward were surfaced by the deep dive and the design panel. Section K.0 records the questions the director ruled during the pass, so that this register never presents them as open again; section K.20 onward records the questions the director explicitly left open after those rulings.

Abbreviations used in citations, all resolving to `docs/design/*.md` or `state/*.md` at `chatgpt/forge-quest-studio-foundation@824c4d58` unless a path is spelled out: SSC = FORGE_NEXT_SAFETY_STATE_PRESENTATION_CONTRACT.md; MOB = FORGE_NEXT_MOBILE_ACCESSIBILITY_AUDIT.md; WCM = FORGE_NEXT_WORKFLOW_COMPONENT_MAP.md; WFA = FORGE_NEXT_WIREFRAME_ANATOMY.md; SCR = FORGE_NEXT_SCREEN_CONTENT_REQUIREMENTS.md; IRM = FORGE_NEXT_INTERACTION_RISK_MATRIX.md; CPY = FORGE_NEXT_UI_COPY_AND_STATE_LANGUAGE.md; ICN = FORGE_NEXT_ICON_MOTION_SEMANTICS.md; SCN = FORGE_NEXT_UX_SCENARIO_MATRIX.md; ACC = FORGE_NEXT_DESIGN_ACCEPTANCE_CHECKLIST.md; COL = FORGE_NEXT_COLOR_SEMANTICS.md; VD = FORGE_NEXT_VISUAL_DIRECTION.md; QS = FORGE_NEXT_QUEST_STUDIO.md; RB = FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md; HND = FORGE_NEXT_UI_CONTEXT_HANDOFF.md; IDX = FORGE_NEXT_UI_DESIGN_INPUT_INDEX.md; MS = FORGE_NEXT_MISSION_STUDIO.md; SBI = FORGE_NEXT_STYLE_BOARD_INVENTORY.md; RCM = FORGE_NEXT_DESIGN_RECONCILIATION_MATRIX.md; DS = FORGE_NEXT_DESIGN_SYSTEM_V0_1.md; EXP = FORGE_NEXT_CONTENT_STUDIO_EXPANSION.md; WSP = FORGE_NEXT_CONTENT_PROJECT_WORKSPACE.md; BRF = state/prompt_forge_next_planning_resume_after_ui_recovery.md; FBRF = state/prompt_forge_quest_studio_foundation.md. `ABBR:line` cites a line; `ABBR §n` cites a section. Paths prefixed `824c4d58:` exist only on that branch. Unprefixed `forge/src/*`, `skills/*`, `scripts/*`, `docs/*` and `.github/*` paths resolve at `main@305a28f`. Row ids such as `foundation-impl C5` or `product-proposals O-16` refer to the consolidated readings in the reconciliation evidence; `RM-nn` and `CF-nn` refer to the reconciliation plan's roadmap implications and conflicts. Evidence tiers follow `docs/00_INDEX.md`; a tier stated by a reading is never upgraded here. Entries whose one-line row carries "(pending predecessor-transcript reconciliation)" wait on the export described in HND §5 and are listed as such in the handoff (BRF:165).

## K.0 Ruled during the pass (not open)

**Provenance of these rulings.** None of them is recorded in `docs/RULINGS.md` on `main@305a28f`, which ends at `RUL-2026-09-08-007`. The visual north star was ruled to the planning owner directly and is documented in `docs/design/FORGE_NEXT_VISUAL_DIRECTION.md` at `chatgpt/forge-next-planning@0bb5a54b`; `RUL-2026-09-12-001` and `RUL-2026-09-12-002` are recorded in `docs/RULINGS.md` on `chatgpt/forge-quest-studio-foundation@824c4d58`, a branch that has not merged. Recording all three in the repository's own ruling history is therefore an outstanding step, and it belongs to whoever integrates that branch, not to this package (`CLAUDE.md` section 10).

| Ruling | What is settled | Canonical owner | What stays open under it |
|---|---|---|---|
| Visual north star (2026-09-12, `chatgpt/forge-next-planning@0bb5a54b`) | TNR-specific dark operations console, crimson/gold/cool-blue over deep navy/charcoal, strong Forge branding, Command Center home, content lanes, first-class Content Admin, controlled motion, explicit operation contexts | `docs/design/FORGE_NEXT_VISUAL_DIRECTION.md` §12 | exact labels, destinations, lane taxonomy, tokens, type scale, geometry (K-01, K-02, K-20 to K-24) |
| `RUL-2026-09-12-001` Quest Studio (`chatgpt/forge-quest-studio-foundation@824c4d58`) | One shared Quest Studio; subtype/recipe adapters for Mission, Event, Story, Raid/Boss, Battle Pyramid, Daily and later audited types; Mission is a subtype, not a parent product; routine compile needs no chat or file relay; live execution stays an explicit user action | `docs/design/FORGE_NEXT_QUEST_STUDIO.md` | Quest Source schema/versioning (K-25), worker trigger/auth/branch architecture (K-26), subtype rollout order beyond Mission-first (K-27) |
| `RUL-2026-09-12-002` Forge over repository authority (same SHA) | Forge is the human translation, orchestration and presentation layer; `tnr-tools` owns durable facts, contracts, profiles, scripts, validators, provenance and generated artifacts; Forge calls approved typed repository operations, never arbitrary remote execution; local projections are never a second canon; compile is separate from live execution and publishing | `docs/design/FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md` | how much repository-backed project state Forge may edit directly (K-28); whether Guide Studio and the infographic lane become official production lanes (K-29) |
| `RUL-2026-09-12-002`, applied to Expansion D1 (same SHA) | Forge is the primary human content-development workspace: the operator remains inside Forge for normal content design work, and project/authoring workflows are product scope rather than helper utilities around the runner (`docs/RULINGS.md:163-165` at `chatgpt/forge-quest-studio-foundation@824c4d58`; RB:15-25; EXP:1145-1149 asked the question and the ruling answers it) | `docs/design/FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md` §1 | how much repository project state Forge may edit (K-28); whether Guide Studio and the infographic lane become official lanes (K-29); the lane taxonomy those workflows sit under (K-24) |

The architecture recommendation (section F) and the roadmap (section G) take these rulings as fixed inputs; the fourth row is the same ruling read against the expansion study's D1, recorded so that D1 is never re-asked. The Quest Studio foundation slice on `chatgpt/forge-quest-studio-foundation` is an active ChatGPT-owned Lane A implementation; under the one-writer rule this package does not patch it and the roadmap plans around its independent review rather than re-planning the same seam.

| ID | Decision | Blocks |
|---|---|---|
| K-01 | Final visual style and degree of "flashiness" | Phase 2 (new shell) |
| K-02 | Top-level navigation model | Phase 2 |
| K-03 | Content Admin permission scope | Phase 4 |
| K-04 | Admin executes arbitrary content writes, or only review / editorial / publish | Phase 4 |
| K-05 | Which content types get first-class forms and previews in v1 | Phase 4 |
| K-06 | Capture data classification and what may persist to the public repository | Phase 1 |
| K-07 | Which operations are eligible for one- or few-tap publish | Phase 5 |
| K-08 | Admin edits go to hidden live records directly, or through a staged package first | Phase 4 |
| K-09 | Where approval state lives, given the game has no native approval field | Phase 4 |
| K-10 | Whether any TheNinjaRPG source change is acceptable | Phase 4 dependencies |
| K-11 | Timing of Builder deprecation and removal | Phase 6 |
| K-12 | Final publishing UX and confirmation level; the wording half (pending predecessor-transcript reconciliation) | Phase 5 |
| K-13 | Authorize a game-source pin move before Forge Next implementation | Phase 0 |
| K-14 | Ship a minified bundle | Phase 0 |
| K-15 | GitHub credential model for the repository bridge on the admin's device | Phase 3 |
| K-16 | Deletion policy for placeholders and orphans | Phase 4 |
| K-17 | Research-read registry expansion (which non-content procedures Forge may call) | Phase 1 |
| K-20 | Exact desktop and mobile destination lists and labels, with the phone-shell sub-points (K-20a) (pending predecessor-transcript reconciliation) | Phase 2 |
| K-21 | Final operation-mode taxonomy, including whether Review is a mode or a workflow category; sub-decision K-33 (pending predecessor-transcript reconciliation) | Phase 2 |
| K-22 | Exact operation-mode colours, tokens and hex values where the style board differs from design system v0.1, including the board's Critical tier (pending predecessor-transcript reconciliation) | Phase 2 |
| K-23 | Typography scale where the latest style board tightens v0.1 (button variants moved to K-32) (pending predecessor-transcript reconciliation) | Phase 2 |
| K-24 | Final content-lane taxonomy (pending predecessor-transcript reconciliation) | Phase 2 |
| K-25 | Quest Source schema and versioning beyond the foundation's v1 | Studio phase |
| K-26 | Repository worker trigger, authentication and branch architecture: ratify the implemented dispatch model or revert to source-push; PAT scope | Studio phase; K-15 |
| K-27 | Subtype adapter rollout order after Mission | Studio phase |
| K-28 | How much repository-backed project state Forge may edit directly | Workspace phase |
| K-29 | Whether Guide Studio and the infographic/visual-communication lane become official production lanes | not scheduled |
| K-30 | Late Content Admin and publish visual details, and instructions to Fable never committed (pending predecessor-transcript reconciliation) | Phase 5 |
| K-31 | Background and lane art in v1: CSS-drawn atmosphere with small inline SVG, or a funded opt-in art pack | Phase 2 (Command Center hero) |
| K-32 | Semantic Success/Warning button variants as production variants (split from K-23) (pending predecessor-transcript reconciliation) | Phase 2 |
| K-33 | Mode selectable by the user vs derived from the work package (sub-decision of K-21) (pending predecessor-transcript reconciliation) | Phase 2 |
| K-34 | Distinguish authorization (role) denial from other HTTP-200 refusals; source audit before any NOT AUTHORIZED lamp | Phase 4 (admin) |
| K-35 | ABORTED: introduce a producer or drop it from the human vocabulary | none |
| K-36 | Canonical enforcement of the mission profile shape in `mission.py` vs advisory-only | Studio phase |
| K-37 | `studio/*` branch namespace, retention, cleanup and conflict handling | Studio phase (before broad use) |
| K-38 | Worker refusal and cancellation observability | Studio phase |
| K-39 | Artifact promotion gate and the journaled Studio to runner contract | Studio phase |
| K-40 | How workstream state references a Studio draft or build without duplication | Workspace phase |
| K-41 | How art files enter packaging under the manual-art boundary, and whether to record that boundary as a ruling | Studio phase (packaging) |
| K-42 | Flagship end-to-end workflow confirmation (Mission brief to verified hidden build) | section G ordering |
| K-43 | Project creation scope and intake class taxonomy | Workspace phase |
| K-44 | Project lifecycle vocabulary (human stage names; navigation vs summary) | Workspace phase |
| K-45 | When post-launch feedback becomes a formal workstream task | none |
| K-46 | Graph editing depth in Studio v1 | Studio phase (v1.5) |
| K-47 | Review annotations store | Phase 4 |
| K-48 | Reuse search placement | Studio v2 |
| K-49 | Policy override workflow | Studio phase (decision cards) |
| K-50 | Adapter boundary between the shared quest compiler and subtype logic | Studio phase (second adapter) |
| K-51 | AI assistance layer inside the Studio | none |
| K-52 | How the admin surface learns the signed-in account's role | Phase 4 (admin read) |
| K-53 | Whether balance-bearing classes appear in a Content Admin surface at all | Phase 4 |
| K-54 | Whether the product says plainly that hidden does not mean secret, and whether an embargo requirement exists | Phase 5 (publish copy) |

---

### K-01 Final visual style and degree of flashiness: RULED mid-pass

**Ruling:** the director approved the Forge concept as the visual north star (`docs/design/FORGE_NEXT_VISUAL_DIRECTION.md` at `chatgpt/forge-next-planning@0bb5a54b1025ba49ff6b09aa9606f23102f4dca3`): TNR-specific dark operations console, crimson/gold/cool-blue accents over deep navy/charcoal, strong Forge branding, controlled motion and depth. Its section 12 lists what stays binding and what Fable may change with rationale.
**What remains open under the ruling:** exact hex tokens, logo treatment, background illustration, icon set and card geometry (illustrative per §12); these are proposed in `D_VISUAL_SYSTEM.md` and the wireframe style tile, and are accepted or adjusted by the user at the phase-2 design freeze. Directions A "Instrument panel" and B "Workbench" were explored by the design panel before the ruling arrived; they are kept in `D_VISUAL_SYSTEM.md` §D2.9 only as sources of grafted ideas (contrast tables, density rules), not as alternatives to the ruling.
**Not negotiable regardless of tokens:** the state rules in amendment §9 and `D_VISUAL_SYSTEM.md` §D2.4 (mutation, publish, SENT, paused and auth states are never colour-only and never animated); and the colour-semantics ruling that operation-mode colours and semantic outcome colours are separate systems, which superseded the first board's red PUBLISH and amber LIVE WRITE pairings (COL:11-13, user-approved, Tier A) while leaving exact hex open (COL:64; K-22).
**Can defer:** the remaining token acceptance can wait until phase 2; phases 0 and 1 are shell-independent.

### K-02 Top-level navigation model, constrained by the approved north star

**Why it matters:** decides what the operator sees first on a phone and how Content Operations and Content Admin are separated. The amendment fixes the shell (Command Center home, persistent rail on desktop, bottom navigation plus a More surface on phone, visual content lanes, first-class Content Admin) and leaves the destination set, the lane taxonomy and the grouping to evidence.
**Evidence:** real workflow mix in `C_WORKFLOW_INVENTORY.md`; the current five screens (`forge/src/ui/screens.mjs`); the three candidate models scored in `D_IA_AND_JOURNEYS.md` §D.1; the mockup-element reconciliation table in §D.2.
**Options:** operation-oriented destinations with content lanes as entry points; content-type-oriented destinations; two-axis (goal first, content type second). All three are rendered inside the approved shell; the choice is which axis the bottom navigation and the rail carry.
**Recommendation:** the panel's recommendation and rationale are in §D.1; the alternatives are kept there in full. Any element of the mockup that the recommendation renames, regroups or drops is listed in §D.2 with the capability row that justifies it, and any departure from the approved character itself is listed in §D.7 for the director.
**Can defer:** yes, until phase 2.

### K-03 Content Admin permission scope

**Why it matters:** the admin surface must expose only what the signed-in game role permits, but the user can choose to expose less than the game allows (for example, no delete, no clone, no bulk edit).
**Evidence:** `E_CONTENT_ADMIN_FEASIBILITY.md` lists per class which procedures a `canChangeContent` role can call and which lifecycle flips exist; the game enforces role checks in resolvers, so Forge cannot widen them, only narrow the UI.
**Options:** (a) review / edit permitted fields / preview / publish only; (b) (a) plus creating new records from templates; (c) everything the role allows, including delete and clone.
- Sub-decision (from the workspace proposal's open question 4, WSP:663): whether Content Admin receives a dedicated project view or a role-filtered version of the same workspace. A dedicated view is smaller to secure; a role-filtered workspace shows the admin the same evidence the operator sees. Either way the filter is Forge policy over the game's role checks, never a widening of them.
**Recommendation:** (a) for v1: it matches the brief's stated outcomes and keeps the blast radius of a mistaken tap small; (b) as a later phase once the review loop is trusted.
**Can defer:** no, before phase 4 design freezes.

### K-04 Admin executes arbitrary writes or only editorial and publish actions

**Why it matters:** an admin who can run manifests is an operator; an admin who can only adjust permitted fields and publish never needs to understand execution internals. The brief wants the second but leaves it open.
**Evidence:** every content mutation is a whole-record `update` with non-strict validators (`E_CONTENT_ADMIN_FEASIBILITY.md`); an "editorial" edit still sends the whole merged record, so field-level permission is a Forge-side policy, not a server one.
**Options:** (a) editorial edits limited to an allowlist of fields per class (name, descriptions, images, hidden/published) plus publish; (b) any field the class validator accepts; (c) manifests too.
**Recommendation:** (a); the allowlist is a per-class adapter table the user approves (K-05).
**Can defer:** no, before phase 4.

### K-05 Which content types get first-class forms and previews in v1

**Why it matters:** each class needs an adapter (field allowlist, form controls, preview renderer). Building all nine at once delays the first usable admin surface.
**Evidence:** per-class feasibility and preview paths in `E_CONTENT_ADMIN_FEASIBILITY.md`; guides have a native published flag and a client renderer but exist only after the Forge pin; AI records have no hidden column.
**Options:** v1 = quest + gameAsset (the review loop One Perfect Crop needs now); v1 = quest + jutsu + item + gameAsset; v1 = everything including guides and AI.
**Recommendation:** quest, gameAsset and item first (they carry the hidden flag, have full-record reads, and are what the active workstream publishes), guides second (native `published`, post-pin registry work), AI last (containment is `inArena` and quest references, not a flag).
**Can defer:** partially; the adapter framework (phase 4) does not depend on the list, the first adapters do.

### K-06 Capture data classification and what may persist to the public repository

**Why it matters:** Builder parity for research reads (any procedure, full bodies, `select`) cannot be met by removing the allowlist without exposing player and session data in `harvests/inbox/`.
**Evidence:** `FULL_PERSIST_PATHS` allowlist and 512 KiB ceiling (`forge/src/storage/captures.mjs:58-84`); Builder writes any body (`builder_bundle.js:372-375`); `push/05` and `push/06` capture `combat.getBattleHistory` and `combat.getBattleEntries` with player names, and the guide pass anonymizes them by hand; `F_ARCHITECTURE_RECOMMENDATION.md` §F.5 proposes tiers. The Tier C contracts already reserve the display: the capture library must identify whether data is repo-safe, local-only, projected or another approved category once the architecture is final, and must not implement the taxonomy from the design text alone (SCR:357-359); the acceptance checklist requires the tier to be visible and forbids implying captured data is repository-safe by default (ACC:122-123).
**Options:** (a) three tiers: repo-safe (audited content point reads, exported), local-only (any audited query, stays in IndexedDB, exported only as a summary), projected (manifest-declared field list, exported); (b) two tiers without projection; (c) keep the current allowlist only and leave research reads to Builder.
**Recommendation:** (a); it is the only option that closes the research-read gap without a public-repo leak, and projection is what Builder's `select` already meant.
**Can defer:** no; it gates phase 1 and the Builder retirement gate for research reads.

### K-07 Operations eligible for one- or few-tap publish

**Why it matters:** "publish in a few clear taps" is the admin's headline request and the highest-consequence action.
**Evidence:** publish is a full `update` flipping `hidden` on jutsu/item/bloodline/quest/gameAsset and `published` on guides; AI records have no flag; publishing a quest whose referenced AI or scene assets are still hidden has class-specific effects (gameAsset hidden affects listing only, law 16c).
**Options:** (a) single-record publish only, with a dependency read that warns; (b) package publish (a quest with its assets and AI) as one deliberate action with per-record read-back; (c) bulk publish from a list.
**Recommendation:** (a) in phase 5, (b) once packages exist (K-08), never (c) in v1.
**Can defer:** no, before phase 5.

### K-08 Admin edits go directly to hidden live records or through a staged package first

**Why it matters:** direct edits are simplest and make the game the only truth; staged packages give a reviewable diff and a repo record but introduce a second representation that can drift from live.
**Evidence:** no staging environment exists; Forge's journal already records every mutation; the workstream roadmap and `push/` hold packages today; the queue model options are in `F_ARCHITECTURE_RECOMMENDATION.md` §F.6.
**Options:** (a) direct: the admin edits the hidden live record through Forge's runner (journaled, read back), the repo receives the results bundle; (b) staged: the admin's edit produces a manifest the operator runs; (c) hybrid: direct for editorial fields, staged for structural changes.
**Recommendation:** (a) with journaling and read-back; it removes the operator relay the brief wants gone, and hidden records are the staging area the game already provides. (b) keeps the relay.
**Can defer:** no, before phase 4.

### K-09 Where approval state lives

**Why it matters:** the game has no approval field for content (guides have `published`, others have `hidden`); "ready for review", "approved", "changes requested" must live somewhere without pretending to be live state.
**Evidence:** `E_CONTENT_ADMIN_FEASIBILITY.md` (no approval field on any class at head); repository consumers and their write races in `evidence/repo-consumers.json`; queue options in §F.6.
**Options:** (a) a repository file per package (`state/review/<slug>.json`) written through the contents API and rendered into the workstream roadmap; (b) an annotation on the results bundle; (c) the workstream `roadmap.json` evidence entries; (d) local-only (per device).
**Recommendation:** (a): explicit, diffable, workflow-safe path, and honest about being coordination state rather than canon (the same stance `docs/workflows/CONTENT_WORKSTREAM.md` takes).
**Can defer:** no, before phase 4.

### K-10 Whether any TheNinjaRPG source change is acceptable

**Why it matters:** several admin conveniences (a native approval state, a dedicated publish toggle, a role endpoint) would be simpler with a game change; the planning default is no change.
**Evidence:** per-class "would need game change" column in `E_CONTENT_ADMIN_FEASIBILITY.md`.
**Options:** (a) no game change (default); (b) propose a small upstream contribution later, as its own workstream with its own authorization.
**Recommendation:** (a) for the whole roadmap; record (b) items as dependencies only.
**Can defer:** yes; the roadmap assumes (a).

### K-11 Timing of Builder deprecation and removal

**Why it matters:** the brief forbids retiring Builder by decree; the roadmap proposes objective gates.
**Evidence:** `B_PARITY_MATRIX.md` gates; `J_MIGRATION_AND_RETIREMENT.md` sequence (read-only mode, deprecation banner, loader removal).
**Options:** (a) retire when all gates pass, after one full content cycle on Forge only; (b) retire Builder's write path first, keep its read path until the research-read tier ships; (c) keep both indefinitely.
**Recommendation:** (b) then (a); it removes the riskier half first while preserving the escape path the brief demands.
**Can defer:** yes, until the gates are measurable.

### K-12 Final publishing UX and confirmation level

**Why it matters:** the brief wants fewer taps for the admin and unmistakable high-consequence actions.
**Evidence:** today every consequential action is a native `confirm()` (`forge/src/ui/app.mjs:172`); the tiered confirmation model is in `D_IA_AND_JOURNEYS.md` §D.4. The structural fields of the confirmation are Tier C and may be designed before the level is ruled: publish context label, subject and count, current to resulting visibility, source-backed dependency warning, permission readiness, audience statement, cancel, explicit verb (WFA:450-461); the wording pattern is `Publish <content name>?` with the visibility change stated, and "Published" appears only after read-back, with "Publish not verified" for an unread final state (CPY:465-467, 485-493; SCN S-52); publish is never placed beside Save with identical styling and never inferred from HTTP success (IRM:335-340). The level (one in-UI confirmation vs typed name or press-and-hold vs two-person) and the final wording are user-owned; the wording half also waits on the transcript (BRF:69; RCM:148; K-30).
**Options:** (a) one in-UI confirmation naming the record and its visibility change, plus read-back shown before the screen is left; (b) (a) with a typed record name (press-and-hold was considered and withdrawn by the visual system, which rules that motion never carries state and that an armed control must be readable rather than timed: `D_VISUAL_SYSTEM.md` G-B6); (c) two-step (approve, then publish) by two different people.
**Recommendation:** (a) for single records, (b) for package publish, (c) only if the user wants separation of duties.
**Can defer:** no, before phase 5.

### K-13 Authorize a game-source pin refresh before Forge Next implementation

**Why it matters:** Forge's field sets, nested key sets and procedure registry are derived from `345d18ac`, 81 commits behind the game head read for this plan. If they had drifted, an admin edit form built on them would be refused or would reset live counters.
**Evidence:** measured in this pass (`evidence/drift.json`): the derived contracts regenerate byte-identically from head `36c5873b`, every validator file Forge reads is unchanged, and the auth table is identical for all 43 registry paths; the only differences are a provenance line (`schema.ts:2577` to `2578`), import reshuffles, additive routers and constants, and one `mcp` flag. The skill's generated 45x contracts are the ones that are genuinely stale (`docs/DRIFT.md`), and they gate `validate.py`, not Forge.
**Options:** (a) a small Lane A provenance-refresh pass in phase 0 (re-derive from the head of that day, update the pin SHA in the bundle banner, Settings and registry comments, fix the one `mcp` flag, rerun `pin_relevance.mjs`), with the 45x re-extraction through the repository's `schema_diff` adoption gate as its own reviewed pass; (b) stay on `345d18ac` and re-check drift at every phase gate; (c) fold the pin move into phase 1.
**Recommendation:** (a). It is cheap, it removes an 81-commit explanation from every review, and it is not a contract change; the 45x adoption pass is the one that needs care.
**Can defer:** yes, as long as every phase gate reruns the drift tools against the game head of the day.

### K-14 Ship a minified bundle

**Why it matters:** minification cuts the shipped bundle by about 42% (398 KB to 233 KB measured), but the checked-in bundle becomes unreadable for a reviewer who diffs it, and the reproducibility gate must compare minified output.
**Evidence:** `A_ARCHITECTURE_MAP.md` §A.9; `forge.yml` verifies bundle parity by rebuild. The Quest Studio slice adds 39,621 bytes to the unminified bundle (+10.0%, measured by the foundation reading in a scratch overlay, not re-run here), with no size budget in CI; that delta is the trigger for a budget gate in section I.
**Options:** (a) minify with the CI rebuild gate as the fidelity proof; (b) stay unminified and reduce size by lazy-loading contract data instead; (c) both.
**Recommendation:** (c), in phase 0 for minification only after the reviewer confirms the rebuild gate is the accepted proof.
**Can defer:** yes.

### K-15 GitHub credential model on the admin's device

**Why it matters:** results sync and approval-state writes need a fine-grained PAT stored in the browser (`tnr_bk_gh_v1`); the admin may not have or want one; RUL-2026-09-08-001 discourages pasted long-lived credentials.
**Evidence:** `forge/src/github.mjs`; `docs/RULINGS.md` RUL-2026-09-08-001. The Quest Studio slice widens what the operator's stored PAT must be allowed to do: create refs (`824c4d58:forge/src/github.mjs:87-91`) and dispatch workflows (`824c4d58:forge/src/github.mjs:138-142`), beyond the Contents write that harvest sync already needs; the worker itself runs under `contents: write` (`824c4d58:.github/workflows/quest_studio.yml:23-24`). The permission class of a dispatch call is an external GitHub fact (Inferred; foundation-impl W4). The scenario matrix requires that a missing PAT never make the UI imply live operation is unavailable (SCN:327-329, S-41). This entry and K-26 are decided together: K-15 is the admin's device, K-26 the operator's (RM-08).
**Options:** (a) admin device holds no PAT: approvals are recorded in the game (hidden→visible) and Forge exports a bundle for the operator to commit; (b) admin gets a read/write PAT scoped to the repo; (c) a relay: Forge writes to a `relay/*` branch and the existing `relay.yml` merges (still needs a token).
**Recommendation:** (a) for v1; the publish read-back itself is the durable evidence and the operator's device keeps the repo record.
**Can defer:** until phase 3.

### K-16 Deletion policy for placeholders and orphans

**Why it matters:** two-phase creates can leave `New Jutsu - <id>` placeholders; today nothing deletes them and the brief says no automatic deletion.
**Evidence:** no delete recipe exists in Forge (`forge/src/runner/recipes.mjs`); the game has `*.delete` procedures behind role checks (`E_CONTENT_ADMIN_FEASIBILITY.md`).
**Options:** (a) no deletion in Forge at all (status quo); (b) an explicit per-record "delete placeholder" action, gated to rows whose name still matches the placeholder pattern and that no job holds, with typed confirmation; (c) delete as a general admin action.
**Recommendation:** (a) through phase 5; revisit (b) only with evidence of placeholder accumulation.
**Can defer:** yes.

### K-17 Research-read registry expansion

**Why it matters:** committed research manifests call procedures outside Forge's 43-row registry (`combat.getBattleHistory`, `combat.getBattleEntries`, and Builder-era captures of `quests.getAll`, `gameAsset.getSceneAssets`, `profile.getPublicUsers`); each addition needs kind, auth, limiter and tier audited against the pinned source.
**Evidence:** `evidence/registry-gap.json` (every procedure in the content, guide and staff routers not in the registry, with auth class); `evidence/harvest-evidence.json` (which were used).
**Options:** (a) add only procedures a committed manifest has used, with tier local-only by default; (b) add all public queries in the content routers; (c) none, keep research reads on Builder.
**Recommendation:** (a).
**Can defer:** no, it gates phase 1's research-read slice.

### K-20 Exact desktop and mobile destination lists and labels: OPEN (pending predecessor-transcript reconciliation)

**Why it matters:** the destination set is what the operator sees on every screen. The approved north star fixes the shell (rail on desktop, bottom navigation plus More on phone) but not the destinations, and the latest board lists ten desktop rows and five phone items that the transcript may or may not have approved.
**Evidence:** board desktop rail of ten destinations, recorded as an illustrated proposal and not canonical IA (SBI:147-162, Observed); board phone set Home / Create / Capture / Admin / More with the More grouping unspecified (SBI:168-178, Observed); the reconciliation matrix marks both lists OPEN BY CONTRACT (RCM:68-69) and lists them as transcript items 3 and 4 (RCM:142-143); the mobile audit's unresolved list (MOB:361-367); the brief's pending items 3 and 4 (BRF:63-64); the package's own proposal keeps the phone bar at five or fewer items and the rail as 44 px rows with static badges (`D_VISUAL_SYSTEM.md:500-501`); board labels "Create Content", "Edit & Write", "Manifest & Deploy" have no verified capability behind them and "Validate" conflates repository validation with Forge lints (`H_RISK_REGISTER.md` R-16); SBI:427-429 flags the ten-row rail and the overlapping labels.
**Sub-points from the mobile audit (K-20a):**
- whether Admin sits in the primary phone set for every authorized user, or under More (MOB:364);
- More behaviour: a dialog sheet listing secondary destinations is the package proposal (`D_VISUAL_SYSTEM.md:502`);
- badge and attention treatment: static counts and dots, never animated (MOB:365; `D_VISUAL_SYSTEM.md:500-501`);
- whether active work or recovery alters the shell: the package recommends keeping the bottom bar visible during a run with the top-bar underline as the run signal (MOB:367; `D_VISUAL_SYSTEM.md:663`).
**Options:** (a) operation-oriented destinations with content lanes as entry points (the section D_IA panel choice); (b) content-type-oriented destinations; (c) two-axis (goal first, type second). For the phone: Admin in the primary set vs under More; badges as static counts vs none; shell unchanged during a run vs collapsed.
**Consequence:** fixes the phase-2 shell, the MOB §4 navigation acceptance tests, and which board labels are renamed or dropped. A destination with no verified capability becomes a placeholder, not a control (WFA:423 states the same rule for the admin queue).
**Recommendation (advisory):** fewer rows than the board's ten, grouped by operation; phone at five or fewer with Admin under More until K-03 rules scope; labels drawn from the copy contract's consequence vocabulary, so the board's "Deploy" wording is replaced by the CPY §15 publish pattern (CPY:465-467). Reasoning: every destination must map to a capability row in section B or be a labelled placeholder.
**Can defer:** yes, until the phase-2 design freeze; phases 0 and 1 are shell-independent (K-01).
**Blocks phase:** Phase 2.

### K-21 Operation-mode taxonomy, including whether Review is a mode: OPEN (pending predecessor-transcript reconciliation)

**Why it matters:** the mode band is the persistent statement of production consequence. Four sources disagree on the set and on the palette, and adding Review as a mode changes the band, the icon set, the consequence classes and the copy dictionary.
**Evidence:** the approved direction lists READ ONLY, LIVE WRITE, PUBLISH, RECOVERY as the exploration set (VD:154-157); the colour-semantics amendment defines the same four (COL:19-24); design system v0.1 defines the same four (DS:86-91); the latest board shows five with Review added (SBI:90-96) and flags this as a chronology question (SBI:117-121); the reconciliation matrix marks Review an APPARENT CONFLICT / ADDITION (RCM:62) and the mode selector OPEN BY CONTRACT (RCM:66); the Tier C contracts leave the question open in the same words (SSC:523-524; CPY:631-632; IRM:370; ICN:405-407); the package reserves a treatment for Review so the four modes do not change if it is added (`D_VISUAL_SYSTEM.md:117,182`); the handoff status is still TRANSCRIPT RECONCILIATION PENDING (HND:3). Reconciliation conflict CF-06 routes this question here.
**Sub-decision K-33 (mode selectable vs derived):** the board shows five selectable tiles and a Change dropdown (SBI:257-264, 272-280); the component map requires that a selector never imply permission or capability (WCM:611-613); the board inventory records the same hazard (SBI:282, 431); today's Forge derives read-only from an empty plan (`forge/src/ui/screens.mjs:120`, Source-verified). Full entry under K-33.
**Options:** (a) four modes; Review is a workflow category carried by the admin queue with no band; (b) five modes with a Review band; (c) mode is derived only, with no selector, under either (a) or (b).
**Consequence:** (b) adds a fifth ModeBand state, a fifth icon (ICN:407), a fifth palette family with new collision checks (K-22) and a fifth copy family (CPY:631-632). Review is not a consequence class in the interaction risk matrix (IRM:370), so (b) needs a definition of what a Review band promises.
**Recommendation (advisory):** (a) with (c): mode derived from the parsed plan and the account's capability, never chosen by the user; Review stays a lifecycle state on admin rows. Revisit only if the transcript shows an explicit director ruling for five modes. Reasoning: a selectable mode reads as a permission (WCM:613), and the four-mode set is the one all Tier A sources share.
**Can defer:** until the phase-2 freeze; the reserved treatment absorbs either answer.
**Blocks phase:** Phase 2; the Studio shell absorption (RM-03).

### K-22 Operation-mode colours, semantic tokens and hex values: OPEN (pending predecessor-transcript reconciliation)

**Why it matters:** four mappings exist and two of them collide with each other on the same hex. Whichever is chosen must pass the binding collision rules, and the Studio slice already ships a colour that sits on two of the mappings.
**Evidence:** the amendment's reference values are explicitly references and not locks (COL:52-64: readOnly #38BDF8, liveWrite #F97316, publish #D946EF, recovery #7C3AED); design system v0.1 uses chakra blue / crimson / gold / amber-violet (DS:86-91); the board uses Read indigo #6366F1, Write cyan #06B6D4, Review violet #8B5CF6, Publish orange #F97316, Recovery teal (SBI:98-115); the package's recommended default is READ ONLY cool blue / LIVE WRITE crimson / PUBLISH gold / RECOVERY caution-hatch #f08a3c, marked PENDING (`D_VISUAL_SYSTEM.md:72,664`); the collision rules are binding regardless (COL:41-48: PUBLISH never error red, LIVE WRITE never warning amber, colour never the sole cue); SENT prefers muted lavender when violet would collide with PUBLISH (COL:38); the Studio's compile control is #f97316 (`824c4d58:forge/src/studio/ui.mjs:39`), the same hex as COL's LIVE WRITE and the board's Publish; contrast criteria are in MOB §11 (MOB:251).
**Sub-point (Critical tier):** the board adds a dark-red Critical tier #7F1D1D labelled "System / Safety Critical" beside Error (SBI:81); the reconciliation matrix records it as an added tier to evaluate (RCM:53); no Forge state in the safety contract maps to it today, so it is either dropped or given a state before it becomes a token.
**Options:** (a) adopt the COL references; (b) adopt the board; (c) adopt the package default with PENDING rows; (d) defer every hex to the phase-2 freeze and enforce only the COL §4 collision rules now.
**Consequence:** any choice must satisfy COL:43-48 and MOB §11. The package's RECOVERY on the caution hue must be argued against COL's indigo/violet (`D_VISUAL_SYSTEM.md:72` gives the argument). The Studio's compile colour must move once the mapping is fixed (RM-03 absorption).
**Recommendation (advisory):** (d) now, expressed as token tests in section I, with the hex values PENDING; drop Critical unless a state is named for it; keep SENT on muted lavender. Reasoning: the rules survive any palette (SSC:404-415) and the tests cost nothing to keep.
**Can defer:** yes, until the phase-2 freeze.
**Blocks phase:** Phase 2; the Studio shell absorption.

### K-23 Typography scale where the board tightens v0.1: OPEN (pending predecessor-transcript reconciliation)

**Why it matters:** decides how large hero and page titles are on a phone and where the floor for consequence copy sits. The semantic button question that was bundled here has moved to K-32.
**Evidence:** v0.1 proposes a mobile-first hierarchy (DS:129-137: page title 24, section 18-20, body 14-15, meta 12-13, micro 11-12); the board shows H1 40 px / 120% in a stylized serif, H2 28, H3 20, H4 16, body 15, small 13, caption 12 (SBI:129-139); the reconciliation matrix calls this BOARD ADDS DETAIL / possible revision and item 6 for the transcript (RCM:83,145); the mobile audit forbids solving density by shrinking text and keeps consequence copy out of micro sizes (MOB:153-157); cross-check CC-M6 finds the package's D2 still lacks a stated floor for consequence copy.
**Options:** (a) v0.1 as is; (b) the board scale; (c) board display sizes for hero and page titles only, with v0.1 body and meta and a 14 px floor for consequence copy.
**Consequence:** a 40 px serif H1 costs phone chrome on every screen that carries it; the choice sizes the evidence panel and the ID regions (MOB:157).
**Recommendation (advisory):** (c). Reasoning: it keeps the board's character where it is decorative and the audit's floor where copy carries consequence; a responsive test is required whichever scale is chosen (RCM:83).
**Can defer:** yes, until the phase-2 freeze.
**Blocks phase:** Phase 2.

### K-24 Final content-lane taxonomy: OPEN (pending predecessor-transcript reconciliation)

**Why it matters:** lanes are the Command Center's entry principle. Three of the six board lanes have no verified procedure or recipe behind them, and one lane must host the Quest Studio.
**Evidence:** the board shows Combat, Items, Quests & Events, Locations, Characters, Systems as full-card lanes (SBI:182-206) and calls the labels illustrative until taxonomy is resolved (SBI:217); the reconciliation matrix treats each lane as illustration with the final taxonomy open (RCM:73-78) and lists it as transcript item 7 (RCM:146); v0.1 says the lane names remain illustrative and gives a decorative reference palette (DS:315,326-333); lane icons are illustrative (ICN:227-236) and lane colour never overrides state (ICN:238; COL:47; SCN S-66 at SCN:445-447); "Locations", "Characters" and "Systems" have no verified capability (`H_RISK_REGISTER.md` R-16); which lane hosts Quest Studio is raised by product-proposals O-02 and not settled by RUL-2026-09-12-001.
**Options:** (a) the six board lanes as visual identity, with only lanes backed by a recipe or entity enabled and the rest labelled placeholders; (b) lanes equal to Forge entities (jutsu, item, bloodline, quest, gameAsset, ai); (c) lanes as workflow classes (Quests & Events hosting Quest Studio; Encounters and AI; Items and Jutsu; Assets and Art; Guides once K-29 rules).
**Consequence:** lane art budget follows K-31; a lane without capability must read as a placeholder, not a door; the lane hosting Quest Studio determines the first phase-2 journey.
**Recommendation (advisory):** (c) with (a)'s visual identity, and Quest Studio under the Quests & Events lane. Reasoning: workflow classes map one-to-one onto section C's inventory, whereas entity lanes hide the recipes and the board's three unbacked lanes would be permanent placeholders.
**Can defer:** yes, until the phase-2 freeze.
**Blocks phase:** Phase 2 (Command Center).

### K-25 Quest Source schema and versioning beyond v1: OPEN

**Why it matters:** the authored source is the editable creative artifact above the manifest. Its v1 exists in code. How it grows decides whether Mission keeps its sheet contract untouched and whether Story, Raid and Battle Pyramid can share one compiler.
**Evidence:** v1 as implemented (foundation-impl K1): required `schemaVersion` 1, `kind` "quest", `subtype`, `requestId` matching `^[a-z0-9][a-z0-9._-]{2,63}$`, `content` object; optional `project` and `meta` objects (`824c4d58:forge/src/studio/repository.mjs:31-39`; `824c4d58:skills/building-tnr-content/scripts/quest_compile.py:68-92`, Source-verified). For Mission, `content` is the existing design sheet (FBRF:67) and the browser derives `srcId`, `slug` and `folder` from the request id and emits `meta` but never `project` (`824c4d58:forge/src/studio/ui.mjs:102-119`). The brief says `meta` is ignored by deterministic compilation (FBRF:65) but `sourceSha256` hashes the whole object including `meta` (`824c4d58:skills/building-tnr-content/scripts/quest_compile.py:64-65`, foundation-impl C6). The design lists the candidate v2 sections: project identity, brief and prose, semantic objectives and edges, encounters and reuse intent, scene and art intent, policy selection, decision slots and approved overrides, references and evidence pointers, build metadata (QS:183-195); the Mission adapter may keep consuming the sheet contract (QS:199); naming and schema are Fable's architecture decision (QS:181). The Mission Studio document frames the same three options (MS:767).
**Options:** (a) preserve the sheet schema per subtype and version only the wrapper; (b) evolve the sheet with versioned migration rules; (c) a general authored quest source that compiles down to per-subtype sheets through a shared graph compiler.
**Consequence:** (a) keeps `mission.py`'s contract untouched; (b) adds migration work per version; (c) unlocks Story, Raid and Battle Pyramid through one compiler (K-50) but changes the Mission adapter and the browser emitter. Under every option `meta` must leave the hash or the hash must be documented as covering it.
**Recommendation (advisory):** (b) for Mission now, (c) as the source for the Story family when K-27 reaches it; decision slots first, because they gate the decision cards in QS §10 (QS:356-362). Reasoning: it changes nothing the seam already proves and adds the one section that removes a relay.
**Can defer:** until the second adapter is briefed.
**Blocks phase:** Studio phase (second adapter).

### K-26 Repository worker trigger, authentication and branch architecture: OPEN, now "ratify or revert"

**Why it matters:** the foundation slice implemented the trigger model that the Tier A design did not recommend first, and that choice widens the credential the operator's phone must hold. The implementation is not the ruling. This entry asks the director to ratify it or to require reversion.
**Evidence:** the design offers two models and recommends source-push first because it is the smaller browser-permission expansion, with dispatch as the explicit-request alternative that needs an Actions permission; Fable was to choose after auditing the credential model (QS:320-340). The slice implements `workflow_dispatch` with four inputs (`824c4d58:.github/workflows/quest_studio.yml:3-21`) under `contents: write` for the worker (`824c4d58:.github/workflows/quest_studio.yml:23-24`); the browser creates refs with `POST git/refs` (`824c4d58:forge/src/github.mjs:87-91`) and dispatches with `POST actions/workflows/*/dispatches` (`824c4d58:forge/src/github.mjs:138-142`), both behind the stored PAT (Source-verified). That a dispatch call belongs to an Actions-write permission class is an external GitHub fact, Inferred (foundation-impl W4). RUL-2026-09-08-001 discourages pasted long-lived credentials for the agents and leaves operator mechanics environment-specific (`docs/RULINGS.md:30-41`). The design index still lists the trigger/auth/branch architecture as unsettled (IDX:138). The worker refuses any dispatch not from `refs/heads/main` (`824c4d58:.github/workflows/quest_studio.yml:59`) and Forge dispatches `main` (`824c4d58:forge/src/studio/repository.mjs:95`), so the seam cannot be rehearsed before integration (foundation-impl RI7). Every push to a `studio/quest/*` branch also starts `scrub.yml`, which has no branch filter (`.github/workflows/scrub.yml:2`; effect Inferred, foundation-impl W10). Reconciliation conflict CF-16 routes this question here.
**Options:** (a) ratify dispatch: accept the ref-creation and dispatch rights on the phone PAT and keep the simple run correlation; (b) revert to source-push: a push trigger on `studio/quest/*` with the generated-output paths excluded, a Contents-only PAT, correlation by branch and SHA, and a re-review of the worker; (c) hybrid: source-push by default, dispatch reserved for explicit re-runs.
**Consequence:** (a) fixes the PAT scope at the wider class for every later Studio feature (K-38 option (b) would widen it again); (b) re-opens the reviewed worker and loses the explicit-request correlation; (c) carries both permission models. All three interact with K-15, which decides whether the admin's device holds any PAT at all (RM-08).
**Recommendation (advisory):** rule before any second adapter and before the first phone rehearsal; Fable's audit of the credential model, which QS:340 assigns to Fable, is written into section F before the ruling is requested. No option is recommended here because the PAT scope is a credential decision the user owns (CLAUDE.md §10).
**Can defer:** no.
**Blocks phase:** Studio phase; K-15.

### K-27 Subtype adapter rollout order after Mission: OPEN

**Why it matters:** only Mission has an executable adapter. The next subtype is either new compiler tooling (Event) or a shared graph compiler (Story family), and the order decides which Lane A brief is written first.
**Evidence:** the registry has six entries: mission `supported`, event `needs_compiler`, story / battle_pyramid / raid / daily `needs_recipe` (`824c4d58:skills/building-tnr-content/data/49_DATA_quest_studio_subtypes.json:11,30,50,66,82,98`, Source-verified); the design's maturity vocabulary is `supported`, `experimental`, `read-only/system-managed`, `needs recipe` (QS:155), so the implemented vocabulary differs (foundation-impl K2). Each registry entry carries a `capabilities` block that neither the UI nor the compiler reads: the UI checks `maturity` and `compilerAdapter` (`824c4d58:forge/src/studio/ui.mjs:234`) and the compiler checks the same two (`824c4d58:skills/building-tnr-content/scripts/quest_compile.py:243-244`). Event is new tooling, not adapter work (QS:163). The design's sequencing is Mission, then Event, then Story / Raid / Battle Pyramid, then Daily and generic types, then system-linked types after source audit (QS:378-388); a type may be shown before it is ready only in an expert capability matrix (QS:390) and never exposed before its adapter is truthful (QS:173).
**Options:** (a) Event next, as the Tier A sequencing recommends, funded as its own compiler brief; (b) the Story family next, because one shared graph compiler unlocks three subtypes (K-50); (c) Daily next, as the smallest constraint set.
**Consequence:** (a) is a new Lane A compiler over `EVENT_SHEET.md` / 26x / `references/event.md`; (b) changes the Quest Source (K-25 option (c)); (c) proves the generic path but adds little authoring value. Under every option the vocabulary mismatch and the unread `capabilities` flags are aligned first so the UI is registry-driven (RM-03).
**Recommendation (advisory):** the director chooses the order; Fable's advisory is (b) if K-25 goes to (c), otherwise (a). Unsupported types stay in the expert matrix only. Reasoning: the compiler that unlocks the most subtypes should be built once.
**Can defer:** until the Mission promotion contract (K-39) ships.
**Blocks phase:** Studio phase (second adapter).

### K-28 How much repository-backed project state Forge may edit directly: OPEN

**Why it matters:** RUL-2026-09-12-002 makes Forge the workspace and the repository the owner of coordination state. A phone that writes `roadmap.json` to `main` races the automation that commits there and needs a validator that exists only in Python today.
**Evidence:** the workspace proposal sets the UX contract for roadmap editing (validate ids and dependencies, reject missing resources, preserve COMPLETE anchors, require a resume note, regenerate projections, preview the change) and calls a Forge-only synced copy split-brain (WSP:415-430); it sequences a read-only reader, task launchers, then controlled editing (WSP:566-589); the expansion study's D4 recommends narrow schema-validated edits through explicit user actions (EXP:1163-1167); the workstream tooling is stdlib Python, socket-free, and `render --check` is the drift gate (`docs/workflows/CONTENT_WORKSTREAM.md:126-137`); repository writes from the browser race the `[auto]` workflows (`H_RISK_REGISTER.md` R-07); the repository-side operations vocabulary is typed (RB:160-164).
**Options:** (a) read-only projection plus task launchers in the first Workspace release; (b) narrow schema-validated coordination edits behind a typed repository operation that runs the Python validator and renderer; (c) a full editor in the browser.
**Consequence:** (a) needs no new repository operation; (b) needs a "validate and render roadmap" worker operation in the RB §6 vocabulary before any write; (c) duplicates the validator in JavaScript, the pattern RB:95-97 forbids.
**Recommendation (advisory):** (a), then (b) only behind the typed operation. Reasoning: it is the order the proposal itself calls lower-risk (WSP:430) and it never lets the browser own a rule the repository owns.
**Can defer:** yes, until the Workspace phase.
**Blocks phase:** Workspace phase.

### K-29 Guide Studio and the infographic lane as official production lanes: OPEN

**Why it matters:** both would appear in navigation as lanes. Neither has a capability behind it today, and one of them is rejected by the art pipeline by design.
**Evidence:** guides are a first-class game content type at the game head with a native `published` state and role-gated create, update and delete, but Forge's generated contracts are pinned before that support and `45c_DATA_constructors.json` has no guide validator (EXP:141-164); a grep for "guide" in `45c_DATA_constructors.json`, `45f_DATA_procedures.json` and `forge/src/transport/procedures.mjs` returns zero hits (Observed in this pass); the drift report records `ContentTypes.guide` as an addition after the skill's pin (`docs/DRIFT.md:56`). Infographics have no owning workflow and need labels, text and panels that the game-art QC rejects by design (EXP:166-182, 505). The expansion study's D2 and D3 recommend both, conditionally (EXP:1151-1161). The design index lists both as unsettled (IDX:134-135).
**Options:** Guides: (a) a Forge surface after the K-13 pin move, contract regeneration and registry expansion; (b) never in Forge. Infographics: (a) an official lane with its own spec and a source-audited hosting adapter; (b) ad hoc, outside Forge.
**Consequence:** Guides (a) depends on K-13 and K-17 and cannot start earlier; infographic outputs would fail `rawqc` and `artpreflight` today, so (a) is a new spec before any lane appears; a lane shown before its capability is a placeholder (K-24).
**Recommendation (advisory):** guides (a) as a later phase after K-13; infographics decided separately, with a spec, before any lane appears in navigation. Reasoning: the guide path is credible and source-backed; the infographic path has no tooling yet.
**Can defer:** yes; not scheduled.
**Blocks phase:** none scheduled.

### K-30 Late Content Admin and publish visual details: OPEN (pending predecessor-transcript reconciliation)

**Why it matters:** the predecessor chat may hold rulings on the admin queue, the edit surface and the publish confirmation that never became durable, including instructions to Fable that were discussed but never committed (HND:98). Until they are reconciled, the admin journeys' visuals and the wording half of K-12 stay open.
**Evidence:** the handoff status is TRANSCRIPT RECONCILIATION PENDING (HND:3); its recovery protocol classifies each transcript statement as ALREADY DURABLE, LATER USER RULING, EXPLORATORY, REJECTED or OPEN (HND:71-79); the expected deliverable is a Recovered Current State section in the handoff, with the owning design files updated and a ruling appended where warranted (HND:111-123); that section does not exist at 824c4d58 (the only match at HND:113 is the instruction; Observed in this pass). The board's confirmation is a "Confirm Deployment" modal with an orange Deploy action (SBI:300-308), whereas the copy contract's pattern is `Publish <content name>?` with the visibility change stated (CPY:465-467); the matrix records the wording as open (RCM:91-93,148-149); the brief's pending items 9 and 10 (BRF:69-70).
**Options:** (a) wait for the transcript export and apply the HND protocol; (b) the director re-rules the publish confirmation now (K-12) and the visuals wait.
**Consequence:** (a) keeps K-12's wording half and the admin visuals open until the export lands; (b) unblocks phase 5's confirmation design while visuals stay PENDING. Under either, reconciled outputs land in the owning design files, and in `docs/RULINGS.md` where material, and this package re-reads them at that SHA before the phase-2 freeze.
**Recommendation (advisory):** (b). Reasoning: the confirmation level is user-owned regardless of the transcript, and asking for it now removes the only transcript dependency on phase 5.
**Can defer:** yes for the visuals; no for K-12's confirmation level.
**Blocks phase:** Phase 5.

### K-31 Background and lane art in v1

**Why it matters:** the approved mockup's painted hero and lane illustrations are the one visible element the visual synthesis could not carry into a self-contained userscript bundle without a cost the phone pays on every game page (the reference JPEG alone is 249 KB against 59.5 KB for the whole current UI layer, `A_ARCHITECTURE_MAP.md` §A.9), and text over raster cannot be contrast-guaranteed.
**Evidence:** `D_VISUAL_SYSTEM.md` §D2.5 departure 3 and §D2.10; risk R-06.
**Options:** (a) CSS-drawn atmosphere (layered radial gradients) plus at most 3 KB of inline SVG silhouette and one small SVG glyph per lane, text always on a solid scrim; (b) (a) now plus a funded, repo-committed, opt-in "rich art" pack behind a Settings toggle with a byte budget, off by default on phone; (c) embed the mockup art as data URIs (rejected: parsed on every game page).
**Recommendation:** (a) for v1 with (b) recorded as a later, separately budgeted decision. The character (dark, atmospheric, layered) survives; the painted look does not.
**Can defer:** no; it fixes the Command Center hero's height and content in phase 2.

### K-32 Semantic Success and Warning button variants: OPEN (pending predecessor-transcript reconciliation)

**Why it matters:** split from K-23. A green action button reads as "already succeeded" and an amber one reads as "paused" or "needs attention", because those hues are reserved outcome meanings.
**Evidence:** the board shows six treatments including Success and Warning buttons and says the board alone cannot settle whether they are reusable variants (SBI:221-238); the matrix marks them OPEN BY CONTRACT and transcript item 8 (RCM:90,147); v0.1 defines primary, secondary, quiet and destructive only (DS:205-221); green and yellow-amber are reserved outcome families (COL:34-35); success styling cannot be reused for anything short of a verified outcome (SSC:411); the brief's pending item 8 (BRF:68).
**Options:** (a) no semantic action buttons; outcome colours stay reserved for state; (b) Success only for acknowledgements adjacent to a verified state; (c) adopt the board set.
**Consequence:** (c) puts outcome hues on controls and defeats the mode/outcome separation the director approved (COL:11-13); (b) needs a rule for when a control may wear the verified colour.
**Recommendation (advisory):** (a). Reasoning: the reserved-colour rule is Tier A and a button that looks like a result misleads on a phone.
**Can defer:** yes, until the phase-2 freeze.
**Blocks phase:** Phase 2.

### K-33 Mode selectable by the user vs derived from the work package: OPEN (pending predecessor-transcript reconciliation; sub-decision of K-21)

**Why it matters:** a selector suggests the operator picks the consequence class. In Forge the class follows the manifest and the account, so a selector can only lie or be redundant.
**Evidence:** the board's five-tile selector and Change dropdown (SBI:257-264, 272-280); the matrix records that mode presentation is required but a selector is not (RCM:66); the component map requires that choosing Publish or Write never grants permission or changes manifest capability (WCM:611-613); the board inventory lists the same hazard (SBI:282, 431); v0.1 states the mode summarises production consequence rather than the journal state (DS:84); today READ ONLY is derived from an empty plan (`forge/src/ui/screens.mjs:120`, Source-verified).
**Options:** (a) derived only, no selector; (b) selectable with capability gating; (c) selectable without gating.
**Consequence:** (a) is always truthful; (b) needs a source-verified capability signal per mode (K-34 shows none exists for authorization); (c) violates WCM:613.
**Recommendation (advisory):** (a). Reasoning: the mode is a fact about the plan, not a preference.
**Can defer:** yes.
**Blocks phase:** Phase 2.

### K-34 Distinguish authorization (role) denial from other refusals: OPEN (director; the source audit is done)

**Why it matters:** a fifth session state, NOT AUTHORIZED, was proposed before the source had been audited. The audit has now been done and rules that state out; what remains is whether a per-action denial label may be derived from the server's message text.

**Audit status:** done. `E_CONTENT_ADMIN_FEASIBILITY.md` E.3 audited every admin-relevant procedure at the Forge pin. Result: a role denial is per procedure, not per session; the refusal carries no code field, so the only candidate signal is the server's message string; it is stable for thirteen named paths and indistinguishable for four that guard with `entry && canChangeContent`. What is left for the director is the choice below, not the evidence.
**Evidence:** the auth model has four states and none for role denial (`forge/src/transport/auth.mjs:54`, Source-verified); `classifyError` has no FORBIDDEN class (`forge/src/transport/outcome.mjs:58-73`); a mutation refusal arrives as HTTP 200 `success:false` and becomes a FAILED item (`forge/src/transport/outcome.mjs:39`; `forge/src/runner/runner.mjs:640`); role gates are resolver-level (`H_RISK_REGISTER.md` R-08). The safety contract requires the distinction only where the procedure surfaces it (SSC:83, 293-295) and the copy contract gives the wording for that case (CPY:386-396). The package's shell proposes the NOT AUTHORIZED lamp (`D_VISUAL_SYSTEM.md:499,504`). The design index forbids inventing backend capability to satisfy a mockup (IDX:145). Reconciliation conflict CF-04 routes this question here.
**Options:** (a) a pinned-source audit of resolver refusal shapes in section E; if a stable signal exists, a `classifyError` class and an auth-state extension as a Lane A deliverable, and only then the lamp; (b) never distinguish; render "Write refused" with the server message under disclosure.
**Consequence:** (a) is an execution-core change and lands under the seam rule (R-13); (b) keeps the four states and the lamp is removed from the proposal.
**Recommendation (advisory):** (a), with the lamp conditional until the audit lands. Reasoning: SSC:293 asks for the distinction where it can be proven, and nothing else.
**Can defer:** until section E lands; no admin phase starts without it.
**Blocks phase:** Phase 4 (admin).

### K-35 ABORTED: introduce a producer or drop it from the human vocabulary: OPEN (Fable, director sign-off)

**Why it matters:** the journal declares a state nothing produces, and the copy contract already specifies its human label. Either the state gets a producer or it leaves the dictionary.
**Evidence:** `JOB_STATES` includes ABORTED (`forge/src/storage/journal.mjs:34`, Source-verified); the runner only reads it (`forge/src/runner/runner.mjs:186`) and a grep of `runner.mjs` finds no transition to it (Observed in this pass); the journal screen deletes finished jobs by DONE or ABORTED (`forge/src/ui/screens.mjs:322`); the copy contract labels it "Stopped" and requires a statement about partial external effects (CPY:278-282).
**Options:** (a) add a producer for an explicit operator abort with the partial-effects statement; (b) keep it as an unreachable legacy state and omit it from the label dictionary.
**Consequence:** (a) touches the execution core (R-13) and needs its own tests; (b) leaves half of the "Delete finished jobs" predicate dead but harmless.
**Recommendation (advisory):** (b) for v1; revisit with a user-abort feature. Reasoning: no scenario in the current inventory needs an abort that pause does not cover.
**Can defer:** yes.
**Blocks phase:** none.

### K-36 Canonical enforcement of the mission profile shape in `mission.py`: OPEN (director; canonical-owner change)

**Why it matters:** the browser refuses drafts the repository accepts. The doctrine says the profile owns the shape; the compiler does not enforce it. Fixing that belongs to the canonical owner, not to the Studio.
**Evidence:** `check_headcount` caps enemies per battle node and nothing else (`skills/building-tnr-content/scripts/mission.py:156-176`, Source-verified); `objective_count` and `battle_nodes` appear in `mission.py` only in the selftest fixture (`skills/building-tnr-content/scripts/mission.py:351`; grep in this pass); the D_combat profile declares `objective_count` 4 and `battle_nodes` 1 (`skills/building-tnr-content/data/48_DATA_mission_profiles.json` `ranks.D_combat.shape`); the foundation reading measured a D_combat source with no roster compiling VALID with zero battle nodes (foundation-impl C5, Observed by that reading, not re-run here); the browser enforces both `objective_count` and `battle_nodes` (`824c4d58:forge/src/studio/ui.mjs:122-138`); the brief keeps mission policy owned by 48 and `mission.py` (FBRF:53) and asks reviewers whether browser rules duplicate canonical policy (FBRF:129); the repository architecture forbids the UI hard-coding a rule the Python owns (RB:95-97) and lists structural checks as editing aids only (RB:120-146); the legacy selftest carries a fixture that conflicts with today's profile (`824c4d58:skills/building-tnr-content/scripts/quest_compile_integration_test.py:3-7`). Reconciliation conflict CF-18 routes this question here; RM-09 makes it its own Lane A brief.
**Options:** (a) enforce in `mission.py` under a Lane A brief on the owner, with the selftest fixture repaired; (b) keep the shape advisory and delete the browser rule; (c) the profile declares an enforcement level per rank.
**Consequence:** (a) may refuse existing content that violates a profile; (b) makes "the profile owns the shape" prose only; under every option the browser rule becomes a projection of the repository rule.
**Recommendation (advisory):** (a) with a profile-declared strict flag defaulting on for new ranks; Fable drafts the brief, the director rules. Reasoning: enforcement in the owner is the only way the browser and the compiler agree by construction.
**Can defer:** until the Studio promotion contract; not beyond the second adapter.
**Blocks phase:** Studio phase.

### K-37 `studio/*` branch namespace, retention, cleanup and conflict handling: OPEN (Fable with director approval)

**Why it matters:** the seam introduces a branch namespace and a bot committer that the workflow document does not declare, creates a branch per request that nothing deletes, and compiles against `main` at dispatch time with no drift check.
**Evidence:** paths and prefix `studio/quest/`, `studio/requests`, `studio/results`, `studio/builds` (`824c4d58:forge/src/studio/repository.mjs:10-20`, Source-verified); the workflow document names `main`, `fable/*`, `chatgpt/*` and `coord/*` only (`docs/DEVELOPMENT_WORKFLOW.md:43,73,87,106`); the worker commits as `quest-studio[bot]` (`824c4d58:.github/workflows/quest_studio.yml:125-126`) and removes the previous result and build directory before writing (`824c4d58:.github/workflows/quest_studio.yml:120`); request ids are per-device clock values and each new Mission allocates a new id (`824c4d58:forge/src/studio/ui.mjs:62-64`); branches are created from `main` and never deleted (`824c4d58:forge/src/github.mjs:79-104`); profiles and the registry are read from `main` at open (`824c4d58:forge/src/studio/repository.mjs:57-66`); every push starts `scrub.yml` (`.github/workflows/scrub.yml:2`; per-branch effect Inferred, foundation-impl W10); the design lists lifecycle, cleanup and main-advances-while-open conflict as risks for Fable (QS:466-477); operating cost is `H_RISK_REGISTER.md` R-17. Reconciliation conflict CF-20 routes the declaration question here.
**Options:** (a) a TTL-based cleanup workflow; (b) delete on promotion or abandon from Forge, through a typed operation; (c) keep branches forever.
**Consequence:** (c) is branch sprawl and API quota (R-17); (a) can delete an open draft's branch; (b) needs the promotion gate (K-39) to exist first. Declaring the namespace and routing `quest_compile.py` and the registry in `docs/00_INDEX.md` and the skill are canonical-owner changes (RM-09), separate from the UI.
**Recommendation (advisory):** (b) plus a nightly TTL sweep for abandoned branches, and a compiler/profile revision drift warning in the envelope. Reasoning: the branch is a request record; its lifetime should follow the request's.
**Can defer:** until after the first rehearsal.
**Blocks phase:** Studio phase (before broad use).

### K-38 Worker refusal and cancellation observability: OPEN (Fable engineering; director if the PAT widens)

**Why it matters:** a refused, cancelled or never-started build shows the operator "Build still running". That is a state the evidence does not prove.
**Evidence:** validation refusals exit 2 or 3 before the persist step, so no result lands (`824c4d58:.github/workflows/quest_studio.yml:59-77`, Source-verified); a compiler failure persists the envelope first and then fails the run (`824c4d58:.github/workflows/quest_studio.yml:136-144`); a second compile on the same request cancels the in-flight run (`824c4d58:.github/workflows/quest_studio.yml:26-28`); Forge returns null on a 404 result (`824c4d58:forge/src/studio/repository.mjs:115-117`) and after the poll limit shows "Build still running" (`824c4d58:forge/src/studio/ui.mjs:433-450`, 385); the architecture requires distinguishable "Repository unavailable" and "Build failed" states (RB:269-282) and the safety contract forbids implying more than the evidence proves (SSC:20); cost in `H_RISK_REGISTER.md` R-17.
**Options:** (a) persist a refusal envelope (status failed, code worker_refused or worker_cancelled) before every exit path, plus poll backoff and a "check later" state; (b) give Forge an Actions-run read, which needs another PAT permission; (c) both.
**Consequence:** (b) widens the PAT again and depends on K-26 (a); (a) needs the persist step to run on refusal paths and a result for cancelled runs, which the concurrency setting currently prevents.
**Recommendation (advisory):** (a) plus backoff; (b) only if K-26 ratifies dispatch. Reasoning: the envelope is already the observation channel and needs no new credential.
**Can defer:** no; the current state violates SSC:20 and RB:280.
**Blocks phase:** Studio phase.

### K-39 Artifact promotion gate and the journaled Studio to runner contract: OPEN (Fable with director approval)

**Why it matters:** a valid build today can only reach the runner by a copy and paste step, the relay RUL-2026-09-12-001 wants removed. The promotion path must go through the same preflight as any `push/` manifest and must be journaled, and it must not add a Start control to the Studio.
**Evidence:** the Studio deliberately offers no live execution and names the missing promotion contract (`824c4d58:forge/src/studio/ui.mjs:1-4`, Source-verified); a valid build opens as text through `showExport` (`824c4d58:forge/src/studio/ui.mjs:469-474`); the picker lists the `push/` directory on `main` only (`forge/src/ui/app.mjs:190`); the design requires a valid build to open in existing preflight with the user starting the live operation (QS:306-312, 459-460) and lists "stay in work branches or promote at a package gate" as a Fable risk (QS:476); the ruling wants no routine relay (`docs/RULINGS.md:148` at `chatgpt/forge-quest-studio-foundation@824c4d58`); the envelope carries a source hash but no generated-manifest hash (`824c4d58:skills/building-tnr-content/scripts/quest_compile.py:212-233`) although the design expects one (QS:285; RB:175); the risk is `H_RISK_REGISTER.md` R-18.
**Options:** (a) promote to `push/` at an explicit package gate, through `pushpack.py`, keeping one runner ingress; (b) the runner imports directly from `studio/builds`, a second ingress; (c) both.
**Consequence:** (a) keeps one ingress and a repository history of what was run; (b) removes a step but adds a manifest source that preflight, `parseManifest`, `planOrder` and the auth gate must cover. Under every option the promotion journal records the studio branch, `sourceRevision`, `compilerRevision` and the manifest hash, and the envelope gains that hash first.
**Recommendation (advisory):** (a) for v1 with the manifest hash verified at import. Reasoning: it is the smallest change to a reviewed ingress.
**Can defer:** no; it is the largest missing piece of the no-relay bar.
**Blocks phase:** Studio phase.

### K-40 How workstream state references a Studio draft or build: OPEN (Fable)

**Why it matters:** without a pointer, the workspace cannot show build readiness for a task, and copying build state into the roadmap creates the split-brain the proposals forbid.
**Evidence:** Quest Source `project` is optional and type-checked only (`824c4d58:skills/building-tnr-content/scripts/quest_compile.py:88`, Source-verified) and the browser never sets it (`824c4d58:forge/src/studio/ui.mjs:103-119`); the design lists the reference problem as a risk (QS:477); the Mission Studio document defines what the parent project owns and what the Studio owns, and what the project receives at a stopping point (MS:544-574); the workspace proposal's non-goals exclude a Forge-owned roadmap replacement (WSP:639-650); roadmap edits are governed by K-28.
**Options:** (a) the Studio writes `project` into the source and the roadmap gains a resource pointer to `studio/requests/<id>.quest.json` and the result path, written through K-28's typed operation; (b) roadmap only; (c) Studio only.
**Consequence:** (b) and (c) each leave one side blind; (a) needs K-28 (b) to exist for the roadmap half.
**Recommendation (advisory):** (a). Reasoning: each side records only what it owns.
**Can defer:** until the Workspace phase.
**Blocks phase:** Workspace phase.

### K-41 How art files enter packaging under the manual-art boundary, and its durable citation: OPEN (director)

**Why it matters:** the expansion study cites a "standing project ruling" that keeps art submission manual, but no ruling with that content exists in the ledger. The operative text lives in a workflow document and doctrine. Packaging also needs a rule for carrying accepted bytes.
**Evidence:** the study cites a standing ruling (EXP:139, 431); the ledger's ids are RUL-2026-09-08-001 to 007 (`docs/RULINGS.md`, grep in this pass) plus RUL-2026-09-12-001 and 002 at 824c4d58, none of which is an art-submission ruling; the operative text is "Art production does not upload/write the live game" (`docs/workflows/ART_PRODUCTION.md:132-136`) and D-user-pushes (`docs/DOCTRINE.md:75-79`); the design lists art-into-packaging as a risk for Fable (QS:475) and packaging needs asset bytes available (QS:354); a live example is the `art.intake_accepted_assets` task BLOCKED because the accepted image bytes are not in the repository (`state/workstreams/one_perfect_crop/roadmap.json`, Observed in this pass); `artpreflight.py` exists in the art skill. Reconciliation conflict CF-17 routes the citation question here.
**Options:** Citation: (a) record a RUL entry that names ART_PRODUCTION.md §9 as owner; (b) leave the boundary as workflow text with no RUL id. Packaging: automatic carry of repository-committed, preflight-passed bytes vs manual attach.
**Consequence:** (a) closes the dangling citation and lets every design document cite one id; (b) keeps the study's wording inaccurate. Automatic carry never touches the live game, so it stays inside the boundary; manual attach keeps the relay.
**Recommendation (advisory):** ask the director whether to record the RUL entry; packaging carries only repository-committed bytes that passed `artpreflight.py`. Reasoning: the boundary is about live submission, not about moving bytes inside the repository.
**Can defer:** until the package composer is briefed.
**Blocks phase:** Studio phase (packaging).

### K-42 Flagship end-to-end workflow: OPEN (director confirmation)

**Why it matters:** the roadmap's first vertical slice and the first user rehearsal follow from it. The design and the foundation slice already chose Mission; the director's acceptance is implicit, not recorded.
**Evidence:** the expansion study's D5 lists four candidates and recommends a mission or event slice (EXP:1169-1178); the design's minimum architecture proof is a Mission slice (QS:448-462); the foundation implements only the Mission adapter (K-27 evidence); the study's phase order is a recommendation for Fable to reconcile (EXP:1019). Reconciliation conflict CF-21 routes this question here; RM-07 keeps the study's priorities as inputs, not the order.
**Options:** (a) Mission brief to verified hidden build; (b) event sheet to review package; (c) guide outline to published article; (d) a multi-domain project.
**Consequence:** (a) matches what exists; (b) needs the Event compiler (K-27); (c) needs K-13 and K-29; (d) needs the Workspace phase.
**Recommendation (advisory):** confirm (a). Reasoning: it is the only candidate with an executable adapter.
**Can defer:** no; one line settles it.
**Blocks phase:** section G ordering.

### K-43 Project creation scope and intake class taxonomy: OPEN (director and Fable)

**Why it matters:** decides which content classes get a full workstream and which get a lightweight package, and therefore what the intake studio asks and whether a typed "create workstream" operation must exist.
**Evidence:** the workspace proposal's intake classes (mission or arc, event or story, encounter, guide, infographic, asset-only, other) with the final taxonomy left to Fable and the director (WSP:380-390); its open question 1 (WSP:660); `content_workstream.py` has validate, render, list, next and init subcommands and no create (`scripts/content_workstream.py:1238-1256`, Source-verified).
**Options:** (a) full workstreams for multi-entity work only; (b) everything a workstream; (c) class-dependent.
**Consequence:** any creation from Forge needs a typed operation first (K-28); (b) adds a roadmap for every one-off.
**Recommendation (advisory):** (c), with the typed create operation before any Forge bootstrap. Reasoning: the workstream tooling already validates structure; it should own creation too.
**Can defer:** yes.
**Blocks phase:** Workspace phase.

### K-44 Project lifecycle vocabulary: OPEN (director)

**Why it matters:** human stage names are a derived presentation over the roadmap statuses, and putting them in navigation would make them look like a second status machine.
**Evidence:** the proposal's derived journey and the eight canonical task statuses it must not replace (WSP:63-78); its open question 5 (WSP:664); reserved terms in the copy contract (CPY §20, CPY:558).
**Options:** (a) summary only; (b) navigation; (c) both.
**Consequence:** (b) and (c) interact with K-20's destination set; all three must never create a second status machine (WSP:78).
**Recommendation (advisory):** (a) in v1. Reasoning: it is the only option that cannot be mistaken for canon.
**Can defer:** yes.
**Blocks phase:** Workspace phase.

### K-45 When post-launch feedback becomes a formal workstream task: OPEN (director)

**Why it matters:** feedback on live content either becomes a task with evidence or disappears into chat. It matters most for experiments whose doctrine change is deliberately deferred pending player feedback.
**Evidence:** the expansion study's Channel N, priority P2, wants feedback convertible into a task rather than lost (EXP:691-712); the workspace proposal's open question 6 (WSP:665) and its non-goal of not converting the Forsworn flatten into universal doctrine (WSP:645).
**Options:** (a) always a task; (b) only when it changes scope; (c) never.
**Consequence:** (a) fills roadmaps with notes; (c) loses the evidence trail the study wants.
**Recommendation (advisory):** (b), recorded as a task with evidence. Reasoning: scope changes are what the roadmap exists to track.
**Can defer:** yes.
**Blocks phase:** none.

### K-46 Graph editing depth in Studio v1: OPEN (director and Fable)

**Why it matters:** decides whether the first Studio ships a storyboard with route controls or a full semantic graph, and how much mobile testing that costs.
**Evidence:** the Mission Studio document's open question 2 (MS:768); the design's phone model uses Brief, Storyboard, focused node editor and Choices/Route controls, with the full graph as a focused pan and zoom view that is never the only way to edit routes (QS:398-410).
**Options:** (a) storyboard plus explicit route controls; (b) full graph immediately; (c) graph on desktop only.
**Consequence:** (b) makes drag wiring a phone requirement the design forbids as the sole path; (c) splits the editor by device.
**Recommendation (advisory):** (a), with the graph as a later focused view. Reasoning: it is the design's own phone model.
**Can defer:** yes.
**Blocks phase:** Studio phase (v1.5).

### K-47 Review annotations store: OPEN (director and Fable; adjacent to K-09)

**Why it matters:** review comments need a durable, anchorable home that is coordination state, not canon.
**Evidence:** comments should anchor to field, node, edge, encounter, asset or decision, and the storage model is a Fable and director decision (MS:531-540); its open question 4 (MS:770); coordination state must not be copied into a Forge-only store (WSP:59); the workspace proposal's review-state owner question (WSP:662); K-09 places approval state in a repository file.
**Options:** (a) co-locate with K-09's `state/review/<slug>.json`; (b) task notes in the roadmap; (c) none in v1.
**Consequence:** (a) gives one review file per package; (b) mixes review prose into coordination state; (c) keeps review in chat.
**Recommendation (advisory):** (a). Reasoning: one file, one owner, one diff.
**Can defer:** yes.
**Blocks phase:** Phase 4.

### K-48 Reuse search placement: OPEN (Fable and director)

**Why it matters:** search inside the Studio spends live read budget and exposes captured data to the classification rules; a shared library isolates both.
**Evidence:** the Mission Studio document's open question 5 (MS:771); rate-limit exposure of polling surfaces (`H_RISK_REGISTER.md` R-03); capture classification and registry expansion are K-06 and K-17.
**Options:** (a) embedded live and catalog search in the Studio; (b) a shared Research Library with deep links; (c) both.
**Consequence:** (a) puts budget spend and tier exposure inside an authoring surface; (b) adds a handoff.
**Recommendation (advisory):** (b), with zero-live catalog and committed-capture search embedded. Reasoning: only reads that cost nothing belong inside the editor.
**Can defer:** yes.
**Blocks phase:** Studio v2.

### K-49 Policy override workflow: OPEN (director)

**Why it matters:** an approved deviation from a mission profile must live somewhere the compiler can honour without the compiler guessing. This touches D-reserved-dauntless and profile authority.
**Evidence:** the Mission Studio document's open question 6 (MS:772); balance and rewards are proposals until the user finalises them (`docs/DOCTRINE.md:110-117`); the design keeps those decisions user-owned and wants a decision card instead of a default (QS:29); a blocker is returned and resolved in Forge, then compiled again (QS:356-362); "decision slots / approved overrides" is a candidate Quest Source section (QS:193).
**Options:** (a) a profile variant in 48; (b) a brief override recorded in `docs/RULINGS.md` and the roadmap; (c) a per-source approved-overrides slot citing a ruling id, with the compiler refusing uncited overrides.
**Consequence:** (a) multiplies profiles; (b) keeps the override outside the source the compiler reads; (c) depends on K-25's v2 slot.
**Recommendation (advisory):** (c). Reasoning: the compiler can verify a citation; it cannot verify a chat.
**Can defer:** until K-25 v2.
**Blocks phase:** Studio phase (decision cards).

### K-50 Adapter boundary between the shared quest compiler and subtype logic: OPEN (Fable)

**Why it matters:** decides what one compiler owns (graph legality, ids, hidden-first) and what each adapter owns (policy, recipe), and therefore the cost of K-27 and the shape of K-25.
**Evidence:** the design's adapter examples make Story, Raid, Battle Pyramid and Daily variations of a shared graph compiler plus policy (QS:165-171) and list the boundary as a risk for Fable (QS:474); the event recipe is an eight-step manual build order today (`skills/building-tnr-content/references/event.md:28-59`); the registry's event entry spans engine types event, story, battlepyramid and raid (`824c4d58:skills/building-tnr-content/data/49_DATA_quest_studio_subtypes.json:31`).
**Options:** (a) a thin orchestrator with fat adapters, one per subtype; (b) a shared graph compiler with policy adapters, the design's Story model.
**Consequence:** (a) repeats graph logic per subtype; (b) needs K-25 (c) for the shared source.
**Recommendation (advisory):** (b). Reasoning: three subtypes share one graph model in the design.
**Can defer:** until the second adapter brief.
**Blocks phase:** Studio phase (second adapter).

### K-51 AI assistance layer inside the Studio: OPEN (director)

**Why it matters:** the design allows a future layer that proposes prose, structure or enemies, subordinate to the same gates, and states it is not required for the one-stop workflow.
**Evidence:** QS:364.
**Options:** (a) never; (b) later, behind the decision cards; (c) now.
**Consequence:** (c) adds review burden to the first Studio; (b) waits for K-49's override mechanism so a proposal cannot bypass a gate.
**Recommendation (advisory):** not in this roadmap; record as out of scope. Reasoning: nothing in the flagship needs it.
**Can defer:** yes.
**Blocks phase:** none.

### K-52 How the admin surface learns the signed-in account's role: OPEN (director, with a cost consequence)

**Why it matters:** section E's audit concludes that the robust way to handle authorization is a role pre-check: read the role once, disable what the role cannot do, re-check on send (`E_CONTENT_ADMIN_FEASIBILITY.md` E.3, E.10). Two procedures can supply the role, and they cost differently. Neither requires any credential material beyond the session the browser already holds.
**Evidence:** `profile.getPublicUser` is public, returns `role` and the staff account, and therefore spends one unit of the sliding-window budget with the 1 % money and bank penalty on a trip (`app/src/server/api/trpc.ts:121-185`, pin). `profile.getUser` is protected, carries no limiter, and returns the full user object, which is a far heavier payload than a role check needs. Forge's budget already mirrors the limiter at margin 0.5 (`forge/src/budget/bucket.mjs`), and section H R-03 is the rate-limit risk this decision feeds.
**Options:** (a) one public `profile.getPublicUser` call per session, budgeted and shown in the readiness card; (b) one protected `profile.getUser` call per session, free of the limiter but a heavy read that also pulls data the admin surface does not need; (c) no pre-check: render every action and let the server refuse, which section E shows produces a label that is wrong some of the time.
**Consequence:** (a) is honest about cost and keeps the payload small, but it is the one read on an admin screen that spends budget; (b) spends no budget but reads more of the operator's own record than the feature needs, which is a data-minimisation question, not a capability one; (c) is the behaviour the Tier C contracts argue against, because the operator learns about the denial only after acting.
**Recommendation (advisory):** (a), cached for the session and shown as a readiness lamp, because the cost is one request and the payload is the smallest that answers the question. The choice is the director's because it trades a budget unit against reading more of the account record.
**Can defer:** no: the admin phase cannot render authority-aware actions without it.
**Blocks phase:** Phase 4 (admin read and review).

### K-53 Whether balance-bearing classes appear in a Content Admin surface at all: OPEN (director)

**Why it matters:** the source audit found staff-managed classes whose edits are balance decisions rather than content edits: ranked-season rewards, activity-streak rewards, raid damage thresholds, the global game settings and damage configuration, and the `Default` AI profile (`E_CONTENT_ADMIN_FEASIBILITY.md` E.2f, rows CA-17, CA-18, CA-19, CA-25). They are technically feasible with zero game change, which is exactly why the boundary has to be drawn deliberately rather than by capability.
**Evidence:** E.2f records each class with its procedures and role gates; `CLAUDE.md` section 10 reserves balance, reward values and rarity to the director; several of these classes are live to players the moment they are saved, with no hidden state to stage behind.
**Options:** (a) exclude them from the Content Admin surface entirely and keep them a director-only path outside Forge; (b) include them read-only, so an admin can see the current values as context for a content decision; (c) include them as editable with the same confirmation as any live write.
**Consequence:** (a) keeps the admin surface to content and leaves no path where a reviewer changes balance by accident; (b) is useful context and still cannot change anything; (c) puts a director-owned decision behind an admin's tap, which the repository's own authority rules forbid unless the director says otherwise.
**Recommendation (advisory):** (a) for v1, (b) later if a reviewer actually needs the numbers in front of them. Reasoning: nothing in the reviewed workflows requires editing them, and their live-on-save behaviour has no staging.
**Can defer:** yes, as long as the admin surface ships without them.
**Blocks phase:** Phase 4 scope.

### K-54 Whether the product says plainly that hidden does not mean secret: OPEN (director)

**Why it matters:** `hidden` gates listing and play, not readability. Any caller can read an unreleased record by id, and a caller can list unreleased records by asking for them (`H_RISK_REGISTER.md` R-31; `E_CONTENT_ADMIN_FEASIBILITY.md` cross-cutting row CC-08). Every human word the product uses around drafts and publishing depends on whether the director wants that stated, softened, or left unsaid.
**Evidence:** verified at the Forge pin: `quests.get` is public and returns the record whatever its `hidden` value, refusing only NPC-only quest types (`app/src/server/api/routers/quests.ts:215-236`); `jutsu.getAll` honours a caller-supplied `hidden` filter and only defaults to `hidden:false` (`app/src/server/api/routers/jutsu.ts:2115-2117`). The copy contract requires that a label never implies more protection than the system provides (CPY, SSC section 1).
**Options:** (a) state it plainly in the admin and publish surfaces, for example that publishing changes listing and play eligibility, not readability; (b) stay silent and describe only what the flip changes; (c) treat embargo as a real requirement and record that Forge cannot enforce it, which becomes a game-change dependency.
**Consequence:** (a) is the honest reading and costs one sentence; (b) risks an operator assuming secrecy the game does not provide; (c) turns a copy question into a dependency the game would have to satisfy, which this pass records but does not pursue.
**Recommendation (advisory):** (a), with the sentence living in the publish confirmation rather than on every screen. Reasoning: it is one sentence, it is true, and it prevents a false expectation at the only moment that matters.
**Can defer:** no for the publish copy; the rest can wait.
**Blocks phase:** Phase 6 (publish) copy, and K-07's eligibility reasoning.
