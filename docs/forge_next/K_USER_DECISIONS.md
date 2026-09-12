# K. Open user-decision register

**Status:** planning. Nothing here is settled by this package. Each entry follows `docs/workflows/DIRECTOR_DECISIONS.md`: what must be chosen, why it matters, the evidence, the options with consequences, an advisory recommendation where one is justified, whether the decision can be deferred, and which roadmap phase (section G) it blocks. Once ruled, an entry is recorded in `docs/RULINGS.md` and the operative rule moves to its canonical owner.

Entries K-01 to K-12 are the decisions the brief reserves in §14. K-13 onward were surfaced by the deep dive and the design panel.

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
| K-12 | Final publishing UX and confirmation level | Phase 5 |
| K-13 | Authorize a game-source pin move before Forge Next implementation | Phase 0 |
| K-14 | Ship a minified bundle | Phase 0 |
| K-15 | GitHub credential model for the repository bridge on the admin's device | Phase 3 |
| K-16 | Deletion policy for placeholders and orphans | Phase 4 |
| K-17 | Research-read registry expansion (which non-content procedures Forge may call) | Phase 1 |

---

### K-01 Final visual style and degree of flashiness

**Why it matters:** the user asked for "modern, polished, a little flashy"; the brief forbids letting Fable choose silently. The choice sets every token and animation budget for the redesign.
**Evidence:** current stylesheet is 60 lines, dark-only, scoped (`forge/src/ui/styles.mjs`); three candidate directions with computed contrast and token tables are in `D_IA_AND_JOURNEYS.md` §D.6 and the style tiles in `wireframes/index.html`.
**Options:** A "Instrument panel" (dark-first, dense, restrained motion); B "Workbench" (light/dark adaptive, calm cards, one accent per authority lane); C "Forge" (ember/steel, glow on live-write and publish, animated progress rings).
**Recommendation:** advisory only; see the design panel's synthesized recommendation in §D.6. Whatever is chosen, the risk-state rules in §D.5 (mutation, publish, SENT, paused are never colour-only and never animated) are not optional.
**Can defer:** yes, until phase 2 starts; phases 0 and 1 are shell-independent.

### K-02 Top-level navigation model

**Why it matters:** decides what the operator sees first on a phone and how Content Operations and Content Admin are separated.
**Evidence:** real workflow mix in `C_WORKFLOW_INVENTORY.md`; the current five screens (`forge/src/ui/screens.mjs`); the three candidate models scored in `D_IA_AND_JOURNEYS.md` §D.1.
**Options:** operation-oriented workspaces; content-type-oriented workspaces; two-axis (goal first, content type second).
**Recommendation:** the panel's recommendation and rationale are in §D.1; the alternatives are kept there in full.
**Can defer:** yes, until phase 2.

### K-03 Content Admin permission scope

**Why it matters:** the admin surface must expose only what the signed-in game role permits, but the user can choose to expose less than the game allows (for example, no delete, no clone, no bulk edit).
**Evidence:** `E_CONTENT_ADMIN_FEASIBILITY.md` lists per class which procedures a `canChangeContent` role can call and which lifecycle flips exist; the game enforces role checks in resolvers, so Forge cannot widen them, only narrow the UI.
**Options:** (a) review / edit permitted fields / preview / publish only; (b) (a) plus creating new records from templates; (c) everything the role allows, including delete and clone.
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
**Evidence:** `FULL_PERSIST_PATHS` allowlist and 512 KiB ceiling (`forge/src/storage/captures.mjs:58-84`); Builder writes any body (`builder_bundle.js:372-375`); `push/05` and `push/06` capture `combat.getBattleHistory` and `combat.getBattleEntries` with player names, and the guide pass anonymizes them by hand; `F_ARCHITECTURE_RECOMMENDATION.md` §F.5 proposes tiers.
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
**Evidence:** today every consequential action is a native `confirm()` (`forge/src/ui/app.mjs:172`); the tiered confirmation model is in `D_IA_AND_JOURNEYS.md` §D.4.
**Options:** (a) one in-UI confirmation naming the record and its visibility change, plus read-back shown before the screen is left; (b) (a) with a typed record name or a press-and-hold; (c) two-step (approve, then publish) by two different people.
**Recommendation:** (a) for single records, (b) for package publish, (c) only if the user wants separation of duties.
**Can defer:** no, before phase 5.

### K-13 Authorize a game-source pin move before Forge Next implementation

**Why it matters:** Forge's field sets come from `345d18ac`; the game head has changed item and quest validators (farm fields, `requiredFarmingLevel`); an admin edit form built on stale sets would be refused or would reset live counters.
**Evidence:** `docs/DRIFT.md`; `evidence/drift.json`; `docs/BUILDER_APP_NOTES.md` "Source pin".
**Options:** (a) a dedicated Lane A pin-move pass (derive tools, `pin_relevance`, `schema_diff` adoption gate, regenerate 45x) before phase 1; (b) move the pin inside phase 1; (c) stay on the pin and refuse item/quest edits that touch the new fields.
**Recommendation:** (a); it is the smallest reviewable unit and every later phase depends on it.
**Can defer:** no.

### K-14 Ship a minified bundle

**Why it matters:** minification cuts the shipped bundle by about 42% (398 KB to 233 KB measured), but the checked-in bundle becomes unreadable for a reviewer who diffs it, and the reproducibility gate must compare minified output.
**Evidence:** `A_ARCHITECTURE_MAP.md` §A.9; `forge.yml` verifies bundle parity by rebuild.
**Options:** (a) minify with the CI rebuild gate as the fidelity proof; (b) stay unminified and reduce size by lazy-loading contract data instead; (c) both.
**Recommendation:** (c), in phase 0 for minification only after the reviewer confirms the rebuild gate is the accepted proof.
**Can defer:** yes.

### K-15 GitHub credential model on the admin's device

**Why it matters:** results sync and approval-state writes need a fine-grained PAT stored in the browser (`tnr_bk_gh_v1`); the admin may not have or want one; RUL-2026-09-08-001 discourages pasted long-lived credentials.
**Evidence:** `forge/src/github.mjs`; `docs/RULINGS.md` RUL-2026-09-08-001.
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
