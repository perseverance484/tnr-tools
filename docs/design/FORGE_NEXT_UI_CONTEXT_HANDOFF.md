# Forge Next — UI context recovery handoff

**Status:** ACTIVE RECOVERY SCAFFOLD — TRANSCRIPT RECONCILIATION PENDING  
**Date:** 2026-09-12  
**Branch:** `chatgpt/forge-next-planning`  
**Lead lens:** UI/UX Reviewer  
**Supporting lens:** Art Director  
**Purpose:** recover the current Forge Next UI/design state without making the predecessor chat a permanent dependency

## 1. Why this file exists

The prior Forge UI/design conversation reached the chat-length limit. Repository policy says chat history is not the permanent project record, so this file provides a durable bridge into the replacement conversation.

The recovery method is deliberately selective. It does **not** attempt to reconstruct every rejected mockup or every conversational turn. It recovers only material that changes current/future work: approved direction, later corrections, rejected patterns worth avoiding, unresolved director decisions, and any chat-only delta that never reached the repository.

## 2. Verified repository baseline

At recovery start:

- repository: `perseverance484/tnr-tools`;
- shared `main`: `305a28f992e33194fbba279a3f32e698dfb2b67f`;
- UI/design planning branch before this handoff: `e0081afab544afeeed01a54240672f2781b5479d`;
- the planning branch was four commits ahead of that `main` baseline and contained the current durable Forge Next design-support package.

The governing collaboration and authority files remain `docs/00_INDEX.md`, `docs/RULINGS.md`, `CHATGPT.md`, `docs/DEVELOPMENT_WORKFLOW.md`, `docs/agents/README.md`, `docs/agents/UI_UX_REVIEWER.md`, and `docs/workflows/DIRECTOR_DECISIONS.md`.

## 3. Durable Forge Next sources already recovered

### `state/prompt_forge_next_planning.md`

Planning/discovery contract for the next Forge generation. It requires an evidence-backed product/architecture deep dive before implementation and keeps final product UX with the project director/operator.

### `docs/design/FORGE_NEXT_VISUAL_DIRECTION.md`

User-approved visual north star. It establishes the product character: a professional TNR content-operations application, dark/atmospheric/premium, game-specific without becoming a battle-screen imitation, clear under production pressure, and genuinely responsive/mobile-first.

It also establishes the broad direction for a persistent app shell, Command Center, human-facing content lanes, first-class Content Admin, explicit operation context, strong state visualization, controlled motion, and readable operational typography.

### `docs/design/FORGE_NEXT_DESIGN_SYSTEM_V0_1.md`

Design-support proposal for foundations and reusable component language. It is intentionally not the final information architecture or implementation contract. It defines the early palette/token system, typography/density/shape rules, component vocabulary, state language, mobile/desktop constraints, accessibility baseline, and motion guidance.

### `docs/design/FORGE_NEXT_COLOR_SEMANTICS.md`

User-directed correction separating operation-mode color from semantic outcome color. Its binding principle is that action context and result/status must remain visually distinct and must never rely on color alone.

The specific reference palette in this file remains subject to later user correction; meaning separation is the durable rule.

## 4. Latest chat-side visual evidence

The replacement conversation began with a newly supplied **Forge Design System v0.1** style-board image. It is the newest visual artifact currently available to ChatGPT, but it is **not yet treated as repository-canonical or fully approved** because the predecessor transcript has not been reconciled.

Observed characteristics of the supplied board include:

- a TNR Forge masthead over a moonlit/ninja-world landscape;
- a dark navy/black application foundation with crimson, gold, bright blue and ivory brand accents;
- explicit semantic success/info/warning/error/critical/muted families;
- a separate operation-mode palette;
- an operation-mode set shown as **Read Only / Write / Review / Publish / Recovery**;
- visually distinct desktop and mobile navigation examples;
- content-lane cards for Combat, Items, Quests & Events, Locations, Characters and Systems;
- reusable examples for buttons, status indicators, form elements, dialogs, notifications, progress, empty/error states, panels and icon style;
- a strong preference for labeled icon + color state communication rather than color alone.

The most important apparent delta is that this board's operation-mode taxonomy/palette does **not** exactly match the earlier repository amendment: it introduces a visible `Review` mode and uses a different mapping for the mode colors. Until transcript reconciliation establishes chronology and approval, this is recorded as **latest proposed visual evidence**, not as a silent supersession of `FORGE_NEXT_COLOR_SEMANTICS.md`.

## 5. Recovery protocol for the predecessor chat

When the predecessor conversation export is supplied, process it as a delta against the repository instead of rereading it as undifferentiated history.

For each material design statement, classify it into exactly one of these buckets:

1. **ALREADY DURABLE** — already represented correctly in repository design/planning sources.
2. **LATER USER RULING** — a user decision that postdates and supersedes an older repository proposal/ruling.
3. **EXPLORATORY** — assistant/mockup proposal discussed but never accepted as direction.
4. **REJECTED / DO NOT REPEAT** — a direction the user explicitly rejected or corrected and whose reappearance would waste time.
5. **OPEN** — a genuine unresolved director decision or design question.

Chronology matters only where it determines supersession. Do not preserve dead iteration history merely because it exists.

## 6. What to extract from the transcript

Prioritize turns concerning:

- explicit approvals, rejections and corrections;
- operation-mode taxonomy and color semantics;
- core palette and brand colors;
- navigation/shell decisions for desktop and phone;
- content-lane grouping and visual treatment;
- typography and density;
- buttons, panels, status chips, notifications and dialogs;
- Content Admin treatment;
- Command Center/dashboard composition;
- mobile behavior and touch/scroll constraints;
- motion, glow, depth and illustration limits;
- accessibility/readability corrections;
- exact statements about which generated style boards/mockups became the preferred direction;
- any instruction to Fable that was discussed but never committed.

For every extracted item, record: topic, chronological position, user decision, whether it supersedes something, repository coverage, and required durable update.

## 7. Reconciliation rules

- Repository authority and precedence remain governed by `docs/00_INDEX.md`; do not let transcript chronology override an unrelated canonical owner.
- A later explicit director ruling may supersede an earlier design proposal, but that supersession should be made durable rather than left implicit in this handoff.
- `docs/RULINGS.md` is used only when the recovered choice materially affects future work and deserves durable decision history; the operative design rule should live in the appropriate Forge design/brief source.
- Do not convert a visually appealing assistant proposal into canon unless the transcript shows user acceptance or the user settles it now.
- Do not infer that the latest supplied board is approved in every detail. It is evidence to reconcile.
- Do not modify Fable's active branches during this process.

## 8. Expected post-export deliverable

After transcript reconciliation, update this handoff with a compact **Recovered Current State** section containing:

- final approved visual character;
- current operation-mode taxonomy and color rule;
- final known navigation/shell constraints;
- current component/style-board direction;
- explicit rejected patterns worth remembering;
- unresolved director decisions;
- exact canonical files updated as a result.

Then update the actual owning design files and, where warranted, append a ruling entry. The goal is that a future Forge UI conversation can start from repository evidence without needing this predecessor transcript again.

## 9. Current safe working assumption

Until the export is reconciled, continue design discussion from the **latest supplied board plus the durable visual-direction/design-system documents**, but treat conflicts between them as open chronology questions rather than silently choosing one.

No Forge production UI implementation is authorized by this recovery file. Fable remains the normal implementation owner after requirements/planning are settled and handed off under the existing Lane A workflow.
