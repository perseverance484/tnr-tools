# Forge Next — unified content operations & Content Admin planning brief

**Status:** PLANNING / DISCOVERY CONTRACT — NO IMPLEMENTATION YET  
**Date:** 2026-09-12  
**Repository:** `perseverance484/tnr-tools`  
**Baseline main:** `305a28f992e33194fbba279a3f32e698dfb2b67f`  
**Lane:** A — code/tooling/infrastructure  
**Planning / architecture owner:** Fable / Claude Code UltraCode  
**Independent reviewer:** ChatGPT — Release Auditor, with UI/UX Reviewer + Engineering Auditor lenses  
**User:** project director/operator and final authority on product UX, publishing authority, live-game actions, and final acceptance

## 0. Assignment

Perform a **comprehensive current-state analysis and product/architecture deep dive** for the next major Forge generation, then return a durable, phased execution roadmap for user review.

**Do not implement the redesign in this planning pass.** Do not begin a UI rewrite, change manifest contracts, modify game code, deprecate Builder, or perform live-game requests/writes. The output of this task is evidence-backed architecture/product planning that is strong enough to become one or more later implementation briefs after the user approves the direction.

The desired end state is a single polished Forge application that can replace Builder for all normal TNR content work and that adds a human-friendly Content Admin experience for review/edit/preview/publish workflows.

This is not permission to bypass TNR's authentication/authorization model or the repository's live-game safety boundary. Repository access is not live-game authorization.

## 1. Product vision

Forge should become the **single content-operations workspace** for TNR.

The user wants:

1. a modern, responsive UI that is intuitive, fast, polished and a little flashy;
2. full Builder capability parity so Builder can be retired rather than maintained in parallel;
3. all reads/captures/writes/uploads/reconciliation/results workflows required for real content work;
4. clear lanes/workspaces for different kinds of content work instead of one undifferentiated technical console;
5. a seamless manifest experience — discover/select/import, understand, preflight, run, verify and sync with minimal friction;
6. first-class capture workflows, including full captures where safe/appropriate;
7. a **Content Admin** panel that lets an authorized content administrator review, edit, preview and publish content — especially hidden/staged content — in a few clear taps without needing the operator to translate manifests/results back and forth;
8. strong recovery, auditability and safety despite the simpler surface;
9. mobile-first usability on the user's real userscript/browser workflow plus a strong desktop/tablet experience;
10. one coherent product rather than Builder and Forge having overlapping responsibilities.

The goal is **less operator friction without weakening mutation safety or authority clarity**.

## 2. Repository / authority boot sequence

Before analysis, reconstruct current context from the live repository rather than prior chat memory.

At minimum verify/read:

- current `main` and exact SHA;
- `state/active-context.md`;
- `state/status.json`;
- `docs/00_INDEX.md`;
- `docs/RULINGS.md`;
- `CHATGPT.md`;
- `CLAUDE.md`;
- `docs/DEVELOPMENT_WORKFLOW.md`;
- `docs/agents/README.md`;
- `docs/agents/UI_UX_REVIEWER.md`;
- `docs/agents/ENGINEERING_AUDITOR.md`;
- `docs/workflows/IMPLEMENTATION_HANDOFF.md`;
- this brief.

Also read the current and historical sources that explain Builder/Forge behavior, including at least:

- `docs/PLAN_2026-09-03_builder_app.md`;
- `docs/BUILDER_APP_NOTES.md`;
- `docs/handoffs/BUILDER_APP_READINESS_HANDOFF.md`;
- `docs/handoffs/FORGE_PROTECTED_AUTH_PIN_RECONCILIATION.md`;
- `state/prompt_forge_full_capture.md`;
- `state/prompt_forge_protected_auth.md`;
- `docs/workflows/CONTENT_WORKSTREAM.md`;
- the routed content-building skill/reference material required by `docs/00_INDEX.md`.

Inspect the actual current implementation and tests — do not infer current capability from old plans alone.

## 3. Current architectural surfaces that must be analyzed

Forge is already modular. The planning pass must determine which parts are sound enough to preserve and which need replacement/refactoring.

Inspect at minimum:

### Core / entry
- `forge/src/main.mjs`
- `forge/build.mjs`
- `forge_loader_user.js`
- `forge_bundle.js`

### UI / takeover
- `forge/src/ui/app.mjs`
- `forge/src/ui/screens.mjs`
- `forge/src/ui/styles.mjs`
- `forge/src/ui/dom.mjs`
- `forge/src/ui/takeover.mjs`

### Manifest / execution
- `forge/src/runner/manifest.mjs`
- `forge/src/runner/runner.mjs`
- `forge/src/runner/validate.mjs`
- `forge/src/runner/lints.mjs`
- `forge/src/runner/pool.mjs`
- `forge/src/runner/recipes.mjs`
- `forge/src/runner/refs.mjs`
- generated field/nested contracts

### Transport / auth / procedure registry
- `forge/src/transport/client.mjs`
- `forge/src/transport/session.mjs`
- `forge/src/transport/auth.mjs`
- `forge/src/transport/procedures.mjs`
- `forge/src/transport/envelope.mjs`
- `forge/src/transport/outcome.mjs`
- `forge/src/transport/upload.mjs`

### Persistence / recovery
- `forge/src/storage/journal.mjs`
- `forge/src/storage/captures.mjs`
- `forge/src/reconcile/reconciler.mjs`
- budget/cache components

### GitHub / repository bridge
- `forge/src/github.mjs`
- current manifest browsing/picker behavior
- results export/sync
- `harvests/inbox/` compatibility
- release/pin workflow

### Tests / evidence
Read the full relevant Forge suite, especially:
- adversarial;
- runner;
- auth;
- transport/envelope;
- storage;
- capture/full capture;
- reconcile;
- UI;
- release-loader;
- harvest compatibility.

Also inspect `builder_bundle.js` and Builder notes/fixtures enough to establish **actual Builder parity**, not remembered parity.

## 4. Builder retirement is an evidence problem

Create a complete **Builder → Forge capability parity matrix**.

For every meaningful Builder capability, record:

- capability / workflow;
- Builder behavior and evidence;
- current Forge behavior and evidence;
- parity status (`PARITY`, `FORGE BETTER`, `GAP`, `INTENTIONAL DIFFERENCE`);
- safety/compatibility notes;
- retirement blocker yes/no;
- proposed disposition.

Inventory at least:

- repository/manifest picker;
- manifest parsing and compatibility;
- read-only / capture-only runs;
- arbitrary supported `get*` / `list*` research reads;
- summary captures;
- full captures;
- selected/projected capture needs if relevant;
- create/update/edit workflows;
- uploads / asset handling;
- two-phase creates and orphan recovery;
- read-back verification;
- pause/resume after eviction/navigation/error;
- ambiguous `SENT` handling;
- preflight validators/lints;
- pool/reference resolution;
- rate-budget behavior;
- GitHub result sync;
- result bundle format / harvest compatibility;
- repo browsing/search/filtering;
- settings/auth configuration;
- job history/export;
- any Builder-only convenience or escape hatch currently relied on in real content work.

Do not retire Builder because Forge is newer. Define **objective retirement gates**.

The roadmap must propose a migration/retirement sequence that preserves an escape path until parity is proven. Consider whether Builder should first become read-only/deprecated before removal, but do not decide this without evidence.

## 5. Safety invariants to preserve or strengthen

The new UI may simplify the operator experience, but it must not blur the underlying lifecycle.

Preserve or improve:

- write-ahead journal semantics;
- explicit `PLANNED` / `SENT` / `CONFIRMED` / verified-or-equivalent states;
- ambiguous `SENT` writes are reconciled, not blindly retried;
- two-phase create recovery and orphan visibility;
- no automatic deletion;
- pre-send validation fails closed for contract errors;
- server verdict comes from decoded application outcome, not HTTP success alone;
- read-back verification of asserted fields;
- rate-budget discipline and no 429 retry loops;
- game cookies/session material never enter repo artifacts/logs;
- GitHub credentials remain separate from game auth;
- live writes require an authenticated, authorized human action;
- publishing is explicit;
- hidden/staged-by-default policy remains visible where it applies;
- result/capture sync must not accidentally publish sensitive protected/user/session data to a public repository.

Current full-capture persistence is deliberately allowlisted because exported results may sync to a public repository. If broader capture capability is required for Builder parity, design a **data-classification/persistence model** rather than simply removing the allowlist. Evaluate tiers such as repo-safe captures, local-only protected captures, and selected/projected captures. This is a design question for the roadmap, not an authorization to broaden capture persistence now.

## 6. UX / information architecture deep dive

The user wants a modern responsive product, not a prettier technical console.

### Required characteristics

- mobile-first; excellent at phone widths used in Firefox/Chrome + userscript environments;
- strong tablet/desktop layout that uses available space rather than merely stretching mobile cards;
- touch targets and interaction patterns that do not depend on hover;
- clear hierarchy and visual polish;
- tasteful motion/animation/status feedback is welcome, but never at the cost of legibility or mutation-state clarity;
- obvious distinction between safe research/read flows and live mutation/publish flows;
- no raw JSON required for ordinary operator/admin tasks;
- advanced/raw manifest/detail views remain available for debugging and expert inspection;
- important errors explain what happened, whether a request may have left the device, and what the next safe action is;
- job state survives/reconstructs across tab eviction/navigation as current architecture intends.

### Do not pre-decide the navigation model

Evaluate whether the primary IA should be:

- operation-oriented workspaces (`Capture`, `Create`, `Update`, `Review`, `Publish`);
- content-type-oriented workspaces (`Jutsu`, `Items`, `Bloodlines`, `AI`, `Quests/Missions`, `Guides`, `Assets`, etc.);
- or a two-axis model where the first level represents the user's goal and the second the content type.

The roadmap must recommend one with rationale based on actual workflows, frequency, risk and mobile ergonomics.

### Candidate workspaces to evaluate

These are prompts, not mandated tabs:

- **Dashboard / Home** — current work, resumable jobs, blockers, recent results, pending admin review;
- **Research & Capture** — point reads, lists, full/projected captures, capture library;
- **Create / Build** — new content manifests and two-phase creates;
- **Update / Repair** — edit existing records with live read/diff/preflight;
- **Assets & Media** — uploads, reuse, image/asset association;
- **Review & Verify** — manifests/results/read-back/diffs before or after writes;
- **Content Admin** — human review/edit/preview/approval/publish;
- **Jobs / Recovery** — history, paused runs, ambiguous writes, orphan resolution, export;
- **Settings / Diagnostics** — auth/session/GitHub/storage/build/pin information.

Fable should simplify this if fewer surfaces produce a clearer product.

## 7. Manifest experience — target user journey

The planning pass must design a first-class manifest workflow where a manifest feels like a job/package, not a JSON file the user manually shepherds.

Evaluate a flow such as:

1. discover from repo / recent workstream / `push/`;
2. drag/drop/paste/import if local input is appropriate;
3. parse and classify automatically;
4. display title, provenance, content type(s), entity count and operations;
5. show validation blockers and advisories;
6. show captures/reads/writes/uploads distinctly;
7. show live-state diff/preflight where safe and useful;
8. clearly state whether execution is zero-mutation or mutation-capable;
9. explicit operator action to run;
10. live per-item/per-phase progress;
11. safe pause/resume/reconcile;
12. read-back/result summary;
13. sync/export/archive handoff with no manual copy/paste.

The roadmap should identify which steps already exist and which need new capability.

Avoid confirmation fatigue. Low-risk reads should be easy. High-consequence writes/deletes/publishing should be unmistakable and explicit.

## 8. Content Admin product requirement

A major new requirement is a **Content Admin** experience suitable for the user's boss/content administrator.

The admin should not need to understand raw manifests or act as a relay through the operator for routine review/publish work.

### Desired outcomes

For supported content classes, an authorized admin should be able to:

- see content waiting for review;
- understand what changed in human terms;
- inspect relevant metadata/mechanics/assets;
- edit permitted fields through usable controls;
- preview the player-facing result where the game has a meaningful preview/render path;
- approve/reject/request changes or otherwise communicate disposition;
- publish/unhide approved content with a small number of deliberate actions;
- see whether the action actually succeeded/read back correctly;
- inspect history/audit information sufficient to answer what changed and who initiated it.

### Mandatory deep dive before proposing architecture

Inspect the **current pinned/current game source** for existing staff/content panels, routers, validators, auth/role checks and publish/hidden semantics. At minimum inventory the content classes Forge currently touches plus guides and other existing staff-managed content relevant to this product.

Determine, with source evidence:

- which procedures already permit authenticated staff review/edit/publish;
- what roles each requires;
- which content types use `hidden`, `published`, another lifecycle field, or no equivalent;
- what previews/renderers already exist client-side;
- whether an external Forge surface can call those same protected procedures safely through the user's/admin's own same-origin session;
- what the admin can do without any modification to TheNinjaRPG code;
- what would require game-source changes and therefore needs separate user authorization and a separate workstream.

**Do not design around bypassing role checks.** Forge should expose only what the logged-in account is authorized to do and must fail clearly when permissions are insufficient.

### Important product distinction

Keep **Content Operations** and **Content Admin** conceptually distinct even if they live in one application:

- Content Operations is manifest/job-oriented creation, capture, mutation, verification and recovery.
- Content Admin is human review, editorial adjustment, preview, approval and publishing.

The roadmap should explain how data moves between them without forcing the admin to understand execution internals.

## 9. Review queue / staging model — investigate, do not invent silently

The user wants the boss to review/publish content without relying on verbal handoffs. Determine what durable queue can truthfully represent “ready for admin review.”

Evaluate options such as:

- repository-backed manifests/results/workstream state;
- live hidden records discovered through authorized reads;
- a hybrid linking a repo package to a hidden live record;
- existing game staff-list endpoints if they already provide the necessary lifecycle.

Do not invent a second canonical content database merely for UI convenience.

If approval state does not exist in the game, recommend where approval metadata should live and how it avoids pretending to be live state/canon.

## 10. Auth, permissions and session robustness

Forge already has protected-procedure work and source-pinned auth evidence. Re-evaluate against current game source before roadmap claims.

The deep dive must cover:

- same-origin Clerk/session continuity;
- public vs protected procedure registry and drift handling;
- staff/admin role requirements;
- root/carrier route and takeover lifecycle;
- the prior class of navigation/redirect failures where Forge appeared briefly and the game reclaimed the page;
- userscript activation markers and persistence across client-side routing;
- session expiry mid-job;
- multiple tabs competing for rate-limited reads;
- permission changes or role misses during an admin workflow;
- how the UI communicates “not authenticated,” “authenticated but unauthorized,” and “request may be ambiguous.”

No live credentials/session material should be requested, committed or used during this planning task.

## 11. Responsive design / visual direction deliverable

The user owns final visual acceptance. Fable should propose, not silently choose, the final aesthetic.

Deliver enough design exploration to make an informed decision:

- one recommended information architecture;
- 2–3 concise visual-direction concepts or a clearly justified single direction if alternatives add no value;
- mobile and desktop wireframes for the highest-value flows;
- dashboard;
- manifest preflight/run;
- capture/research;
- recovery/ambiguous state;
- Content Admin queue/detail/edit/preview/publish.

Static wireframes/mock HTML or screenshots are acceptable planning artifacts. Do not build the production redesign in this pass.

“A little flashy” should be interpreted as polish — depth, motion, transitions, status visualization, responsive cards/panels, strong typography and deliberate color — not distracting effects or hidden state.

Risk states should become **more visually obvious** than they are today.

## 12. Technical architecture questions Fable must answer

The roadmap must make evidence-backed recommendations on at least:

1. evolve current Forge UI in place vs replace the UI layer while preserving runner/storage/transport;
2. whether current vanilla DOM/CSSOM build constraints remain desirable/required or whether a component strategy can improve maintainability without breaking userscript/takeover behavior;
3. how to keep the execution core UI-independent enough for future shell/native hosting;
4. manifest schema compatibility and versioning strategy;
5. storage migration/compatibility for existing journals/capture cache/settings;
6. capture data classification and persistence/export rules;
7. procedure registry expansion and source-drift gates;
8. content-type adapters/forms for admin editing;
9. preview strategy per content class;
10. GitHub repository bridge and PAT handling;
11. workstream integration and discovery;
12. result/harvest contract evolution;
13. audit/history model;
14. bundle size/performance/startup on mobile;
15. release/pin/install strategy;
16. recovery after tab eviction/crash/network loss;
17. accessibility/touch/keyboard behavior;
18. test architecture for a much larger UI and capability surface.

## 13. Required Fable deliverables

Return a durable planning package, committed on a Fable-owned planning branch, containing at minimum:

### A. Current-state architecture map
Explain Forge's modules/data flow/lifecycle and where Builder still differs.

### B. Builder → Forge parity/retirement matrix
Complete enough that “Builder can be retired” is testable.

### C. Workflow inventory
Map the real content workflows Forge must support: research/capture, create, update/repair, assets, verification, admin review/publish, recovery.

### D. Proposed information architecture and user journeys
Mobile + desktop. Include the Content Admin workflow.

### E. Content Admin feasibility/source audit
For each candidate content class, state existing game API/role/publish/preview support and what can be done with **zero game-source changes**.

### F. Architecture recommendation
What should be preserved, replaced, abstracted or migrated, with rationale.

### G. Phased roadmap
Break execution into reviewable Lane A phases with dependencies and acceptance gates. Prefer vertical slices that leave Forge usable at each stage over one giant rewrite.

For each phase include:
- objective;
- files/surfaces likely affected;
- prerequisites;
- backward-compatibility needs;
- tests/evidence required;
- user decisions required before implementation;
- rollback/fallback story;
- Builder retirement impact.

### H. Risk register
At minimum cover:
- mutation ambiguity/idempotence;
- auth/session/takeover;
- rate limits;
- capture privacy/public-repo persistence;
- stale source pins/contracts;
- mobile performance;
- repo sync failures;
- admin permission/publishing mistakes;
- migration of stored jobs/captures;
- Builder retirement too early.

### I. Test / verification strategy
Unit/fixture/adversarial/UI contract tests plus the exact browser/live smoke that will eventually require user action. Keep planning and implementation tests socket-free unless a later brief explicitly authorizes otherwise.

### J. Migration and Builder retirement plan
Define the exact conditions under which Builder stops being needed, how users are informed, and what fallback exists during transition.

### K. Open user-decision register
Do not bury decisions in prose. List them explicitly with practical consequences and a recommendation where useful.

## 14. User-owned decisions that must remain open unless the user resolves them

Fable may recommend options, but do not silently decide:

- final visual style / degree of “flashiness”;
- final top-level lane/navigation model;
- exact Content Admin permission scope;
- whether the admin can execute arbitrary content writes or only review/editorial/publish actions;
- which content types get first-class forms/previews in v1;
- which operations are eligible for one/few-tap publish;
- whether admin edits go directly to hidden live records or first create/update a staged manifest/package;
- approval-state storage if the game has no native approval field;
- whether any TheNinjaRPG source change is acceptable (default assumption for this planning pass: **no game-source change**);
- timing of Builder deprecation/removal;
- final publishing UX and confirmation level.

Publishing and live-game actions remain user-owned; a delegated content administrator may exercise only permissions the user/game actually grants them.

## 15. Strong planning principles

Use these as evaluation criteria, not as a pre-written architecture:

- **One product, distinct authority lanes.** Unified Forge does not mean every action looks equally safe.
- **Friendly surface, explicit machine state.** Hide incidental technical complexity, never hide ambiguity/risk.
- **Progressive disclosure.** Admins see human content; operators can drill into manifests, procedure calls, captures and journals.
- **No duplicated canon.** Forge visualizes/contracts against repository/game evidence; it does not become a new truth source.
- **Backward compatibility first.** Existing validated manifests should continue to work unless a deliberate migration is approved.
- **Fail closed on writes and sensitive exports.** Convenience is not evidence.
- **Mobile is a primary platform.** Desktop is not the only “real” UI.
- **Recovery is a first-class screen, not an error toast.**
- **Review/publish should be fast because the evidence is clear, not because confirmation was removed.**
- **Builder retirement happens after measured parity, not by decree.**

## 16. Planning constraints / non-goals

During this task:

- no Forge production implementation;
- no Builder deletion/deprecation;
- no live game requests;
- no live game writes;
- no use/request/export of session cookies or credentials;
- no TheNinjaRPG code changes;
- no release-pin movement;
- no manifest contract migration;
- no changing repository doctrine/laws to fit a proposed UI;
- no publishing or live content changes.

If source research reveals that a desired capability genuinely requires a game-source change, record it as a dependency/option and explain why. Do not implement it.

## 17. Planning handoff format

When the deep dive is complete:

1. push the Fable planning branch;
2. report exact base and head SHAs;
3. name every planning artifact created;
4. summarize the recommended architecture/IA in plain language;
5. provide the Builder parity headline and remaining retirement blockers;
6. provide the Content Admin feasibility headline;
7. list user decisions required before implementation;
8. list evidence/source pins inspected;
9. explicitly state that no implementation/live requests/writes occurred;
10. freeze the planning SHA for ChatGPT independent review.

ChatGPT will independently audit the frozen planning package for completeness, safety, source agreement, UX coherence and whether the proposed phases are reviewable before recommending that the user approve an implementation roadmap.
