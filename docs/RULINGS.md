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

## RUL-2026-09-15-001 — Godstorm two-pyramid planning scope

**Date:** 2026-09-15 (recorded from the current planning conversation)  
**Domain:** Godstorm / Tower of Endless Night release planning  
**Status:** ACTIVE  
**Supersedes:** none; replaces the earlier three-pyramid release assumption for this workstream

**Ruling:** Cut Dawnless Crown from release scope and plan around the two retained pyramids, Marrow Vaults and Stormcourt. Maximize reuse of artwork already made. No new keystone assets are needed. Perform a full planning phase before execution. Leave chest contents and reward values open for Content Admin, accompanied by recommendations; dauntless retains final project authority and every live-game action.

**Rationale:** Reduce unfinished release scope and avoid commissioning artwork that existing assets can cover.

**Canonical destination:** `docs/plans/GODSTORM_TWO_PYRAMID_RELEASE_PLAN.md` owns the task plan and separates observed inventory, user-set scope, recommendations and open decisions. Subsequent approved build briefs and existing workstream coordination will point to it. This entry does not amend general doctrine or engine laws.

**Not approved by this ruling:** a particular battle count, exact reward/cadence values, an unlock mechanism, a fixed number of new paintings, destructive live deletion, automatic publishing, or implementation before plan acceptance. The plan's five-avatar completion / ten-keeper portrait / four-background reuse proposal remains a proposal, not a ruling.

---

## RUL-2026-09-15-002 — Separate Godstorm pyramids from Tower of Endless Night

**Date:** 2026-09-15  
**Domain:** Godstorm structure / identity / completion model  
**Status:** ACTIVE  
**Supersedes:** RUL-2026-09-15-001 only where it left the battle count and structure unapproved; that ruling's two-location scope, reuse-first direction, no-keystone requirement and open Content Admin decisions remain in force. Supersedes the earlier plan's Tower identity and paid-withdrawal model for the retained quests.

**Ruling:** The user approved the retained structure and directed that Marrow Vaults and Stormcourt each contain 25 battles without Tower of Endless Night branding or concept framing. Remove their early cash-out system. Tower of Endless Night and its early cash-out mechanic are a separate concept, outside this release. The retained five-keeper structures and finales remain the plan baseline; each pyramid succeeds through its full clear, not an early paid exit. Dawnless Crown remains excluded.

**Rationale:** Keep Godstorm's two battle pyramids distinct from the separate Tower concept instead of preserving its name and reward-choice mechanic inside them. Reuse existing art and combat content rather than rebuilding the encounters.

**Canonical destination:** `docs/plans/GODSTORM_TWO_PYRAMID_RELEASE_PLAN.md`. The plan specifies the graph simplification, detached copy requirements, revised asset-wiring targets, implementation ownership and verification gates. No general doctrine or engine-law change is created.

**Boundary:** Structural approval is not approval of exact reward values, repeat limits, final prose, unseen artwork, a global rename of the shared Endless Night Chest, retrospective removal of player completions, new checkpoint/retry mechanics, destructive record deletion, publication or live operation. Chest/reward decisions remain with Content Admin and dauntless. This ruling reserves the separate Tower concept; it does not authorize its implementation or release.

---

## RUL-2026-09-15-003 — Marrow Vaults below Stormcourt in one structure

**Date:** 2026-09-15  
**Domain:** Godstorm setting / narrative progression  
**Status:** ACTIVE  
**Supersedes:** none as to the approved 25+25 structure, no cash-out, Crown exclusion and separation from Tower of Endless Night. Clarifies RUL-2026-09-15-002; supersedes Draft 1's interpretation of Marrow and Stormcourt as geographically separate sites linked by discovered records.

**Ruling:** Marrow Vaults and Stormcourt are thematically and narratively connected as one structure, with the Vaults below and the Court above. The player enters through the Vaults, then gains entry to the Court. Retain the two 25-battle pyramid quests, their sequence and existing encounter scope, without the Tower of Endless Night identity or early cash-out mechanic.

**Rationale:** Separating Godstorm from the Tower concept does not require separating its lower and upper locations. The final vault threshold should open the way upstairs, not send the player to another site.

**Canonical destination:** `docs/plans/GODSTORM_TWO_PYRAMID_RELEASE_PLAN.md` owns the connected setting and unchanged delivery scope. `docs/plans/GODSTORM_STANDALONE_COPY_AND_SCENE_MAP.md`, Draft 2, owns the proposed revised descriptions, introductions and transition; its filename is retained for reference stability.

**Boundary:** This approves the spatial/narrative relationship, not every sentence of new copy, the exact storm-binding resolution, artwork not inspected, reward values, automatic quest launch, a new travel task, merged progress/resource/reward trackers, retrospective player-state changes or live operation. Content Admin reward decisions and final acceptance remain open. No new asset commission or overall building name is implied.

---

## RUL-2026-09-15-004 — StormCourtyard excluded from Godstorm artwork

**Date:** 2026-09-15  
**Domain:** Godstorm art reuse / scene backgrounds  
**Status:** ACTIVE  
**Supersedes:** no earlier accepted art choice; withdraws the unapproved StormCourtyard/S1 reuse proposal in the release plan and Draft 2 scene map.

**Ruling:** StormCourtyard (`cKHhHoboreP88iH5WjDe7`) is not approved for Godstorm because it belongs to a different artwork/quest set. Exclude it from the Stormcourt background selection and the proposed S1 scene bindings. A successful capture or image download does not confer art approval.

**Rationale:** Preserve the intended visual identity of the connected Marrow Vaults/Stormcourt setting rather than adopting unrelated SkychainMonastery scenery on the basis of its name.

**Canonical destination:** `docs/plans/GODSTORM_ART_REUSE_DECISIONS.md`, AR-001, owns this asset's exclusion, withdrawal of the 26 S1 bindings, corrected planning counts and archive treatment. Read it alongside the release plan and copy/scene map; their prior S1 proposal is superseded, not pending reapproval.

**Boundary:** Keep original captured records and recovered bytes as rejected-reference evidence. Do not delete or modify the shared game asset, repurpose it through cosmetic changes, or automatically substitute other assets from its quest set. This does not reject Stormcourt's own listing image or enemy portraits, approve any replacement/new-painting count, or authorize a live-game change.
