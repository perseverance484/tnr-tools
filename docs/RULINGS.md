# TNR Rulings Ledger

**Status:** durable historical ledger of user/dauntless rulings that materially affect future work.

This file records **what was ruled and why**. It is not a replacement for the canonical owner of a rule.

- Cross-surface doctrine still belongs in `docs/DOCTRINE.md`.
- Engine-law text still belongs in `docs/ENGINE_LAWS.md` through the repository law process.
- Generated contracts/specs remain authoritative for the shapes and numbers they own.
- Current operational state still belongs in `state/`.
- Task-specific decisions may also be reflected in their governing plan/brief.

When a ruling establishes or changes a durable rule, the ruling entry points to the canonical destination. A later ruling supersedes an earlier one by ID; historical entries are not silently rewritten.

## Entry format

Each entry carries:

- **ID** — stable identifier.
- **Date** — ruling date.
- **Domain** — affected workstream.
- **Ruling** — the approved decision.
- **Rationale** — why this option was chosen.
- **Canonical destination** — where the operative rule belongs, if anywhere beyond this ledger.
- **Supersedes** — earlier ruling IDs replaced by this one, or `none`.
- **Status** — `ACTIVE`, `SUPERSEDED`, or `DEFERRED`.

---

## RUL-2026-09-08-001 — Repository credentials

**Date:** 2026-09-08  
**Domain:** repository access / collaboration security  
**Status:** ACTIVE
**Supersedes:** none

**Ruling:** ChatGPT will not use a personal access token for `tnr-tools`. ChatGPT repository writes use the repository-scoped ChatGPT Codex Connector. The old `tnr-container` PAT exposed in the retired Claude-project instruction surface should be rotated/revoked as part of the restructure. Claude Code should use a non-pasted native GitHub authentication path where its environment supports one; do not place repository credentials in committed files or prompt text.

**Rationale:** Long-lived pasted credentials add exposure without benefit when repository-scoped app/native authentication is available. ChatGPT now has the needed branch/write capability through the Codex Connector.

**Canonical destination:** collaboration/security workflow; credential mechanics remain environment-specific and must not be committed. Whether Claude Code's current environment can push without a PAT is an implementation/setup fact to verify, not a design assumption.

---

## RUL-2026-09-08-002 — Historical extraction scope

**Date:** 2026-09-08  
**Domain:** project-history extraction  
**Status:** ACTIVE
**Supersedes:** none

**Ruling:** Do not fully reconstruct the pre-Forsworn conversation era. Salvage selectively: extract material only when it defines a reusable design principle, constrains current/future work, or prevents repetition of an expensive mistake. Shipped specifics and rejected iterations are not automatically worth preserving.

**Rationale:** The repository should preserve useful design memory without turning the handoff into unbounded historical archaeology.

**Canonical destination:** reusable principles go to their proper design/doctrine/reference owner; historical rationale may remain here or in a dedicated design-history note when genuinely useful.

---

## RUL-2026-09-08-003 — Ruling ledger format

**Date:** 2026-09-08  
**Domain:** project memory / governance  
**Status:** ACTIVE
**Supersedes:** none

**Ruling:** Maintain one flat committed ruling ledger at `docs/RULINGS.md`. Entries are append-oriented and carry stable IDs, date, domain, ruling, rationale, status, canonical destination, and a `supersedes` reference when applicable.

**Rationale:** A single searchable ledger preserves decision history and rejected alternatives without scattering rulings across domain files or burying them inside generated/current-state machinery.

**Canonical destination:** this file is the historical ledger. It does not replace doctrine, engine laws, specs, plans, or `state/` as the operative source for the rules/state they own.

---

## RUL-2026-09-08-004 — Engine-law reconciliation sequence

**Date:** 2026-09-08  
**Domain:** engine-law provenance  
**Status:** ACTIVE
**Supersedes:** none

**Ruling:** Reconcile engine laws in this order: (1) correct the known contradictions in laws 19 and 23 and re-derive dependent law 37; (2) move the identified doctrine-class laws to their proper doctrine/design owner; (3) source-cite the verified ENGINE class; (4) split PARTIAL laws clause-by-clause so verified and unverified claims do not share one assertion; (5) investigate NOT_IN_SOURCE entries individually and classify them by evidence rather than retaining them as presumed engine facts.

The separately deferred mission-shape doctrine rewrite remains deferred pending player feedback and must not be smuggled into the law-reconciliation pass.

**Rationale:** Known false statements should be removed from the active law surface first, while keeping source verification, doctrine, behaviour evidence, and deferred design decisions distinct.

**Canonical destination:** `docs/ENGINE_LAWS.md`, `docs/DOCTRINE.md`, and the existing law-provenance/reconciliation process. Implementation belongs to Claude Code after an approved brief/handoff.

---

## RUL-2026-09-08-005 — Art-pipeline dependency policy

**Date:** 2026-09-08  
**Domain:** visual asset production / tooling  
**Status:** ACTIVE
**Supersedes:** none

**Ruling:** Pillow is an approved dependency of the TNR art-production pipeline. Do not force image processing back to pure Python stdlib merely to satisfy an outdated "stdlib-only" framing. Port old ad-hoc NumPy-dependent compositing to Pillow where reasonable; do not add NumPy as a standing dependency unless a concrete operation justifies it and is separately reviewed.

**Rationale:** The live art skill already describes and implements a PIL/Pillow pipeline. Reimplementing mature image operations in pure stdlib would increase code, test burden, and asset-corruption risk without player benefit.

**Canonical destination:** `skills/producing-tnr-art/` dependency/setup documentation and tooling, implemented by Claude Code through normal review.

---

## RUL-2026-09-08-006 — ChatGPT to Claude Code communication contract

**Date:** 2026-09-08  
**Domain:** collaboration workflow  
**Status:** ACTIVE
**Supersedes:** none

**Ruling:** For substantial implementation work, ChatGPT and dauntless settle the design/requirements first. The approved implementation contract is committed as a concise task brief, following the existing `state/prompt_<task>.md` pattern where appropriate. dauntless hands that brief to Claude Code. Claude Code implements on its own branch and returns an exact-SHA handoff with tests/gates/deviations. ChatGPT independently reviews the frozen SHA. Issues may track work but are not the implementation contract; manifests are outputs, not communication documents.

Small low-risk fixes may use a lighter handoff when the required behaviour and review surface are unambiguous.

**Rationale:** The pattern separates director decisions, implementation ownership, and independent review while making work reconstructable from the repository rather than chat history.

**Canonical destination:** `docs/DEVELOPMENT_WORKFLOW.md`, `docs/workflows/IMPLEMENTATION_HANDOFF.md`, and `docs/workflows/FABLE_REVIEW.md`.

---

## RUL-2026-09-08-007 — Claude-project retirement gate

**Date:** 2026-09-08  
**Domain:** project migration / knowledge preservation  
**Status:** ACTIVE
**Supersedes:** none

**Ruling:** Retirement of the old Claude content project is gated by unique-information loss risk, not completion of every improvement that originated there. Before retirement: rotate/revoke the exposed old credential; salvage the unique reusable principles from its memory layer; extract important unresolved/durable rulings; preserve genuinely irreplaceable artifacts that dauntless wants kept; and verify that no active work depends on project-only information.

A full pre-Forsworn transcript reconstruction is not required. Porting the art compositing pipeline is implementation work that may occur later from a committed brief and does not block retirement.

**Rationale:** Once unique knowledge is safely transferred, keeping an obsolete project alive as shadow memory creates more drift risk than value.

**Canonical destination:** handoff/extraction plan and relevant canonical design/reference files for any salvaged principles.

---

## RUL-2026-09-12-001 — Forge uses one Quest Studio with subtype adapters

**Date:** 2026-09-12  
**Domain:** Forge Next / content authoring UX  
**Status:** ACTIVE
**Supersedes:** none

**Ruling:** The previously proposed Mission Studio is not a standalone top-level authoring product. Forge Next should provide one broader **Quest Studio** in which the creator selects a human-facing quest subtype/recipe such as Mission, Event, Story, Raid/Boss, Battle Pyramid, Daily, or another supported quest family. Mission-specific profile/storyboard behavior becomes one subtype adapter within that shared Studio. The intended end state is that supported quest types can be authored, compiled and validated through the repository's canonical scripts from the Forge interface without requiring routine chat/agent/file relay between design and build. Live-game execution remains an explicit user action and is not part of automatic compile.

**Rationale:** TNR quest families share one objective-graph/data-model foundation, while subtype-specific correctness belongs in separate policy/build recipes. A single Studio gives the operator one consistent authoring workflow and lets the repository remain the compiler authority instead of duplicating mission/event logic in separate UIs.

**Canonical destination:** `docs/design/FORGE_NEXT_QUEST_STUDIO.md` and the eventual approved Forge Next architecture/implementation brief. `docs/design/FORGE_NEXT_MISSION_STUDIO.md` remains a useful Mission-subtype detail document but no longer owns the parent product scope.

---

## RUL-2026-09-12-002 — Forge is the human translation layer over repository authority

**Date:** 2026-09-12  
**Domain:** Forge Next / product architecture  
**Status:** ACTIVE
**Supersedes:** none

**Ruling:** Forge Next should function as the operator-facing **translation, orchestration and presentation layer** over `tnr-tools`. The operator should be able to remain inside Forge for normal content design work, while the repository continues to own durable facts, contracts, profiles, evidence, scripts, validators and generated build artifacts. Forge does not need independent copies of all repository knowledge; it should read/generated-project/source those facts with provenance and call approved repository operations when canonical compilation or validation is required. Quest subtypes such as Mission, Story Quest and Battle Pyramid should therefore share one Studio rather than forcing the user through multiple manual interfaces or file/script relays.

Forge may keep local/generated projections for responsive editing, but those projections do not become competing canonical sources. Repository/build operations must be approved typed operations rather than arbitrary remote command execution. Compile/build automation remains separate from live-game execution and publishing, which stay explicit user-owned actions.

**Rationale:** This gives the user one coherent creative workspace while preserving TNR Tools' existing authority, reproducibility and safety model. Repository improvements can flow into Forge through adapters/generated contracts instead of requiring the same rule to be manually maintained twice.

**Canonical destination:** `docs/design/FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md`, `docs/design/FORGE_NEXT_QUEST_STUDIO.md`, and the eventual approved Forge Next architecture/implementation brief.

---

## RUL-2026-09-16-002 — Quest Studio repository builds use source-push with Contents-only browser credentials

**Date:** 2026-09-16
**Domain:** Forge Next / repository build security
**Status:** ACTIVE
**Supersedes:** none

**Ruling:** Quest Studio's initial repository build transport uses **source-push** rather than browser `workflow_dispatch`. Forge may hold a fine-grained GitHub credential with **Contents: write only** for `tnr-tools`; Quest Studio must not require Actions or Workflows write permission on the operator device. Pressing Compile persists a fresh exact Quest Source revision on its dedicated `studio/quest/*` branch, and that source write triggers the trusted repository worker. The worker executes compiler code from trusted `main`, treats the request branch as authored data only, and writes generated results back only to that request branch. Compile remains separate from all live-game execution.

**Rationale:** This keeps the one-stop repository-backed Studio workflow while reducing the blast radius of a browser-stored repository credential. A stolen Contents-only token can alter repository content within its granted scope but cannot use Quest Studio's required permission set to dispatch unrelated Actions workflows. **Security invariant:** the browser credential must never hold GitHub Workflows write permission, because push-triggered workflow definitions are resolved from the pushed request ref; granting Workflows write would allow that credential to replace the worker definition on a request branch and defeat the trusted-main compiler boundary.

**Canonical destination:** `docs/design/FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md`, the accepted Quest Studio implementation contract/handoff, and the eventual unified Forge implementation brief. Branch retention/cleanup and later transport replacement remain engineering decisions.
