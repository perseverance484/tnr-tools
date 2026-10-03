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

**Canonical destination:** `docs/design/FORGE_NEXT_QUEST_STUDIO.md` and the eventual approved Forge Next architecture/implementation brief. `docs/design/FORGE_NEXT_MISSION_STUDIO.md` remains useful Mission-subtype detail but no longer owns the parent product scope.

---

## RUL-2026-09-12-002 — Forge is the human translation layer over repository authority

**Date:** 2026-09-12  
**Domain:** Forge Next / product architecture  
**Status:** ACTIVE  
**Supersedes:** none

**Ruling:** Forge Next functions as the operator-facing **translation, orchestration and presentation layer** over `tnr-tools`. The operator should be able to remain inside Forge for normal content design work, while the repository continues to own durable facts, contracts, profiles, evidence, scripts, validators and generated build artifacts. Forge may keep local/generated projections for responsive editing, but those projections do not become competing canonical sources. Repository/build operations must be approved typed operations rather than arbitrary remote command execution. Compile/build automation remains separate from live-game execution and publishing, which stay explicit user-owned actions.

**Rationale:** This gives the user one coherent creative workspace while preserving TNR Tools' authority, reproducibility and safety model. Repository improvements can flow into Forge through adapters/generated contracts instead of requiring the same rule to be manually maintained twice.

**Canonical destination:** `docs/design/FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md`, `docs/design/FORGE_NEXT_QUEST_STUDIO.md`, and approved Forge Next implementation briefs.

---

## RUL-2026-09-16-001 — One Perfect Crop hidden core manifest may precede art/admin finalization

**Date:** 2026-09-16  
**Domain:** One Perfect Crop / content delivery  
**Status:** ACTIVE  
**Supersedes:** none

**Ruling:** One Perfect Crop may proceed to a validated, independently reviewed **hidden core manifest** before final art and content-admin values are complete. Missing art may use the current builder/game create-path placeholder rather than blocking the core build. Rewards, Cabbage Seed type/rarity/economics, repeatability, and eligibility may be deferred; implementation must not guess them. The core manifest therefore omits Cabbage Seed creation/reward and does not author final reward/gating values. Everything remains hidden, and publishing/unhiding still waits on a later launch-finalization pass and clean hidden-state readback.

**Rationale:** The finished route, prose, and combat contracts can be implemented and reviewed independently of presentation assets and launch economics. Separating a reversible hidden core build from launch-final art/admin work allows progress without converting temporary placeholders into accidental canon.

**Canonical destination:** `state/one_perfect_crop_core_manifest_override.md`, `state/prompt_one_perfect_crop.md`, and `state/workstreams/one_perfect_crop/roadmap.json`.

---

## RUL-2026-09-16-002 — Quest Studio repository builds use source-push with Contents-only browser credentials

**Date:** 2026-09-16  
**Domain:** Forge Next / repository build security  
**Status:** ACTIVE  
**Supersedes:** none

**Ruling:** Quest Studio's initial repository build transport uses **source-push** rather than browser `workflow_dispatch`. Forge may hold a fine-grained GitHub credential with **Contents: write only** for `tnr-tools`; Quest Studio must not require Actions or Workflows write permission on the operator device. Pressing Compile persists a fresh exact Quest Source revision on its dedicated `studio/quest/*` branch, and that source write triggers the trusted repository worker. The worker executes compiler code from trusted `main`, treats the request branch as authored data only, and writes generated results back only to that request branch. Compile remains separate from all live-game execution.

**Rationale:** This keeps the one-stop repository-backed Studio workflow while reducing the blast radius of a browser-stored repository credential. **Security invariant:** the browser credential must never hold GitHub Workflows write permission, because push-triggered workflow definitions are resolved from the pushed request ref; granting Workflows write would allow that credential to replace the worker definition on a request branch and defeat the trusted-main compiler boundary.

**Canonical destination:** `docs/design/FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md`, the accepted Quest Studio implementation contract/handoff, and later unified Forge implementation briefs.

---

## RUL-2026-09-17-001 — Forge research captures use three persistence tiers

**Date:** 2026-09-17  
**Domain:** Forge Next / research capture privacy and evidence  
**Status:** ACTIVE  
**Supersedes:** none

**Ruling:** Forge Phase 1 uses three explicit capture persistence classes:

- **`repo-safe`** — exact response bodies may enter repository/export evidence only for explicitly audited classes approved for that treatment;
- **`local-only`** — exact bodies may be retained in local IndexedDB for operator/research use, but raw bodies must not enter repository results, clipboard/export payloads, public diagnostics, GitHub commits, or other public-repository paths;
- **`projected`** — the raw body remains local while repository/export evidence may contain only explicitly declared, validated field paths plus provenance/verdict metadata.

Existing audited content-record point reads already approved for full persistence remain repo-safe unless separately reclassified. Newly approved non-content research reads default to local-only. Projected exports fail closed: no wildcard, implicit nested passthrough, arbitrary object spread, or fallback from a failed projection to the full body. Widening a tier requires an explicit reviewed policy/registry change.

**Rationale:** Forge needs research parity without making public-repository persistence the default consequence of a read. The three-tier model preserves useful exact local evidence and narrow shareable projections while keeping raw non-content/player-shaped data out of public Git history by default.

**Canonical destination:** `state/prompt_forge_next_phase1.md` and the Phase 1 capture-policy/registry implementation. This is a product/privacy boundary, not engine doctrine.

---

## RUL-2026-09-17-002 — Forge research-read registry is demand-driven and fail-closed

**Date:** 2026-09-17  
**Domain:** Forge Next / research capability  
**Status:** ACTIVE  
**Supersedes:** none

**Ruling:** Forge may add non-content research reads only when a committed, reviewed research manifest/work package actually requires them. Do not expose a generic endpoint browser or bulk-enable all public queries merely because they exist. Every approved research row must record the procedure path, query kind, authentication class, limiter status, exact relevant input/pagination contract, default persistence tier, and source-pin/provenance used to audit it. Phase 1 research registry entries are reads only; unknown or unapproved non-content paths fail closed before transport. New non-content rows default to `local-only` under `RUL-2026-09-17-001` unless separately approved otherwise.

**Rationale:** Demand-driven admission closes real research gaps while minimizing data exposure, rate-limit surface, accidental API creep, and future contract-drift burden.

**Canonical destination:** `state/prompt_forge_next_phase1.md` and the Phase 1 audited research registry/source-provenance implementation.

---

## RUL-2026-09-17-003 — Forge branch cleanup uses selective consolidation, not wholesale merges

**Date:** 2026-09-17  
**Domain:** Forge Next / repository maintenance  
**Status:** ACTIVE  
**Supersedes:** none

**Ruling:** Clean up Forge Next historical branches by selectively preserving accepted planning/design/review documents on a fresh `main`-based documentation branch, retaining the accepted Quest Studio implementation branch as the future Phase-S source, and deleting redundant review/temp/workspace/completed implementation refs only after their unique durable evidence is represented elsewhere. Do **not** merge old planning, review, audit, or temporary branches wholesale merely to remove branch clutter, and do not merge Quest Studio implementation as part of cleanup.

**Rationale:** Historical Forge branches contain useful accepted planning alongside stale operational state, generated snapshots and superseded implementation. Wholesale merges would manufacture false integration history and risk reintroducing stale state. Selective consolidation preserves knowledge while keeping current `main` authoritative.

**Canonical destination:** `docs/forge_next/README.md`, `docs/reviews/FORGE_NEXT_BRANCH_CONSOLIDATION_AUDIT.md`, and the approved branch-cleanup record.
---

## RUL-2026-09-20-001 — Presentation Studio design contract accepted as proposed

**Date:** 2026-09-20  
**Domain:** Forge Presentation Studio / design acceptance  
**Status:** ACTIVE  
**Supersedes:** none

**Ruling:** The design contract at `chatgpt/forge-presentation-studio-design@4532ef917a1dfb40d00c554fd7f065e13216afc7` is accepted as proposed, with its stated defaults: the product is named **Presentation Studio**; the first two templates are **Event poster** and **Staff brief**; the proposed mobile acceptance floor (360 CSS-pixel portrait, 16px body text, 44×44px targets, no hover-only detail, no required dragging), the 1080-pixel PNG master geometry, the full-event-overview poster treatment and the example Godstorm blurbs are accepted as the P2 basis.

**Rationale:** The contract elaborates requirements the governing plan already imposed rather than inventing new ones, and P1 shipped the dossier/spec/registry/lint surface it assumes. Accepting it as a whole removes the last design gate on writing a concrete P2 brief.

**Canonical destination:** `docs/design/FORGE_PRESENTATION_STUDIO_DESIGN_CONTRACT.md` and its Godstorm reference remain the design source; the eventual P2 implementation brief is written against them. Acceptance is of the design, not of any renderer, artifact or Android behaviour, none of which exists yet.

---

## RUL-2026-09-20-002 — No generated decorative art in presentation output

**Date:** 2026-09-20  
**Domain:** Forge Presentation Studio / art policy  
**Status:** ACTIVE  
**Supersedes:** none

**Ruling:** Optional generated decoration stays **off**. No generative step exists anywhere in the presentation renderer. This resolves the policy the design contract left pending and the governing plan listed as a user decision.

**Rationale:** The plan permitted isolated, opt-in decoration; declining it is stricter and simpler. It removes an entire class of failure — a generative path that could be pointed at a named entity, supply text, or quietly fill a missing art slot — rather than containing it with metadata and lint. The Godstorm poster's redrawn portraits are exactly what a renderer with no generative step cannot reproduce.

**Canonical destination:** the design contract's exact-art section and the P2 renderer brief. `skills/producing-tnr-art/` continues to own game-upload art production, which is a separate pipeline.

---

## RUL-2026-09-20-003 — Presentation binaries are generated deliverables, not repository content

**Date:** 2026-09-20  
**Domain:** Forge Presentation Studio / repository policy  
**Status:** ACTIVE  
**Supersedes:** none

**Ruling:** Rendered posters, briefs and export packages are **not** committed. The repository keeps the evidence package, source lock, presentation spec and asset bindings, which reproduce the artifact; the PNG/package itself is a deliverable the operator saves or shares.

**Rationale:** The spec and its bindings are the source of truth, and a committed binary is a second thing that can drift from them. It also keeps the repository from accumulating image weight for every revision of every poster. A build that cannot be reproduced from its committed spec is a defect to fix, not a reason to store the output.

**Canonical destination:** the design contract's export section and the P2 brief. Committing a specific artifact remains available as a deliberate one-off decision.

---

## RUL-2026-09-20-004 — Forge Next Phase 1 precedes Presentation Studio P2

**Date:** 2026-09-20  
**Domain:** Forge roadmap / scheduling  
**Status:** ACTIVE  
**Supersedes:** none

**Ruling:** Forge Next Phase 1 is the next implementation work. Presentation Studio P2 (the deterministic renderer) and P3 (the Studio UI) wait behind it. The P2 brief may be written at any time; it is queued, not blocked.

**Rationale:** Phase 1's contract at `state/prompt_forge_next_phase1.md` has been READY/FROZEN and unstarted the longest. The P1 presentation tooling is already integrated and useful on its own through `forge/tools/presentation.mjs`, so deferring the renderer costs no capability that exists today.

**Canonical destination:** `state/digest.json` in-progress ordering and the Forge Next / Presentation Studio briefs. The art prerequisites recorded in `docs/reviews/FORGE_PRESENTATION_STUDIO_P0_P1_CLOSEOUT.md` still gate P2 whenever it starts.


---

## RUL-2026-10-03-001 — Ethereal Monarch is the Bloodright poster presentation reference

**Date:** 2026-10-03  
**Domain:** Bloodright / poster presentation  
**Status:** SUPERSEDED  
**Supersedes:** none

**Ruling:** The user-approved **Ethereal Monarch — Mandate of Heaven** poster is the primary ("holy grail") presentation reference for future Bloodright posters. Future Bloodright showcase posters should follow its overall visual language: integrated bloodline-driven hero art, vertical top-down skill flow, restrained dark cards with selective glow and ornament, the BLOODRIGHT → bloodline name → epithet title convention, generous spacing and readable statistics. The presentation standard also preserves the later refinements from the approval sequence: one tagline maximum, lean reference notes, scope mentioned once, and no visible source SHA, bloodline ID, `forked tree` label or generic tag primers.

The approved reference is preserved in the user's persistent Library as `/TNR/Bloodright References/Ethereal_Monarch_Mandate_of_Heaven_Holy_Grail.png`. It is visual/presentation evidence only; pinned tree JSON and its validation remain mechanical authority for names, values, roles and prerequisites.

**Rationale:** The Ethereal Monarch poster best matched the desired Bloodright identity and readability after iterative comparison with the earlier Taiyo Kami and Aerathiel work. Making it the explicit presentation reference prevents future sessions from drifting back toward side-to-side diagrams, generic infographic art or excess explanatory copy while keeping mechanics source-driven.

**Canonical destination:** `docs/workflows/BLOODRIGHT_POSTERS.md`, routed from `docs/workflows/ART_PRODUCTION.md`.


---

## RUL-2026-10-03-002 — Ethereal Monarch reference governs information presentation, not universal art style

**Date:** 2026-10-03  
**Domain:** Bloodright / poster presentation  
**Status:** SUPERSEDED  
**Supersedes:** RUL-2026-10-03-001

**Ruling:** The approved **Ethereal Monarch — Mandate of Heaven** poster remains the primary Bloodright reference for **information presentation**: top-down skill flow, tier hierarchy, prerequisite clarity, rules/legend placement, Bloodright naming hierarchy, readable full skill/effect text, lean reference notes, one scope mention and one tagline maximum. It is **not** a universal visual-style template.

Future Bloodright posters may vary their palette, typography style, card materials/shapes, ornament, glow, illustration treatment, hero-art composition, environmental motifs and other aesthetic choices according to the target bloodline's theme. In particular, celestial/thematic typography effects and dark restrained cards are not required constraints. The exact bloodline image remains the identity reference, while pinned design JSON remains mechanical authority.

**Rationale:** The user approved Ethereal Monarch because of how clearly it organizes and communicates Bloodright information, not because every bloodline should share its celestial-regal art direction. Locking theme-specific styling would flatten bloodline identity and misread the purpose of the approved reference.

**Canonical destination:** `docs/workflows/BLOODRIGHT_POSTERS.md`, routed from `docs/workflows/ART_PRODUCTION.md`.


---

## RUL-2026-10-03-003 — Bloodright Damage ceiling and rounded path-total baseline

**Date:** 2026-10-03  
**Domain:** Bloodright / balance baseline  
**Status:** SUPERSEDED  
**Supersedes:** none

**Ruling:** For the current 4-BP Bloodright model, **flat Damage potency may never exceed +5 total in any legal allocation**. The ceiling is evaluated across the complete legal 4-purchase build, not only along the advertised three-node route; fourth purchases and capstone secondaries must not push Damage above +5.

For route design generally, prefer clean cumulative totals in **5-point increments** such as +5, +10 or +15 rather than irregular maxima such as +6, +7 or +8. This is a design preference, not permission to raise every tag to the next band: the chosen band still depends on coverage, leverage, caps, recipient and delivery. Departures from a round total require a concrete balance reason rather than arithmetic convenience.

For a dedicated Damage route, the default shape is **+2 Damage on the Hidden Art and +3 Damage on the Advanced Art = +5 total**, unless an approved design has a different distribution that still respects the +5 legal-build ceiling.

**Rationale:** Flat Damage directly increases jutsu EP and scales broadly across qualifying attacks, so +10 is far beyond the intended potency budget and even the current Blood-Enchanted Eyes Draft 3 maximum of +6 is too high. Clean +5/+10/+15 route targets are easier for players to understand and easier to compare across bloodlines, while retaining room to assign different ceilings to tags with different combat leverage.

**Canonical destination:** the next Bloodright planning/balance revision and its validators. Existing frozen Fable design commits remain historical evidence and are not silently rewritten.

---

## RUL-2026-10-03-004 — Bloodright reference hierarchy: Ethereal structure, Taiyo rendering, target theme

**Date:** 2026-10-03  
**Domain:** Bloodright / poster presentation  
**Status:** ACTIVE  
**Supersedes:** RUL-2026-10-03-002

**Ruling:** Future Bloodright posters use three separate reference authorities: **Ethereal Monarch — Mandate of Heaven** for information architecture and top-down presentation; **Taiyo Kami — Covenant of the Sun** for rendering/art-style discipline; and the exact target bloodline image for the poster's theme, palette, motifs, atmosphere and identity.

Taiyo Kami's role is rendering consistency, not visual cloning. Preserve its polished stylized-anime/fantasy finish, crisp readable silhouettes, controlled detail, clean anatomy/faces, defined luminous effects and coherent saturation. Do not import its fox, solar/fire imagery, orange-gold palette, shrine setting or exact card/frame language into unrelated bloodlines. Likewise, Ethereal Monarch's celestial-regal visual language is not a universal requirement.

**Rationale:** Ethereal Monarch established the preferred way to communicate Bloodright information, while Taiyo Kami established the preferred illustration/rendering quality. Separating those functions allows each bloodline to have a distinct visual identity without letting the art style drift into photorealism, grimdark painterliness, faux pixel art or other inconsistent rendering modes.

**Canonical destination:** `docs/workflows/BLOODRIGHT_POSTERS.md`, routed from `docs/workflows/ART_PRODUCTION.md`.


---

## RUL-2026-10-03-005 — Bloodright element-wide potency scope and balance ceilings

**Date:** 2026-10-03  
**Domain:** Bloodright / mechanics and balance baseline  
**Status:** ACTIVE  
**Supersedes:** RUL-2026-10-03-003

**Ruling:** Bloodright potency is **classification-element wide**, not bloodline-ID scoped. A Bloodright modifier applies to every jutsu of the Bloodright's qualifying element/classification that carries the matching supported tag. Jutsu names, bloodline ownership and equipment sources may describe where effects currently appear, but they are not additional potency selectors. Equipment gates continue to determine whether a jutsu can be cast; they do not narrow Bloodright eligibility.

For player-facing Bloodright modifiers, every modifier except flat Damage is displayed with a `%` sign. Flat Damage remains raw EP/power addition.

Balance ceilings for the current 4-BP model:
- **Damage:** hard maximum **+5 total** in any legal allocation.
- **Lifesteal:** hard maximum **+5% total**.
- **Afterburn:** hard maximum **+15% total**.
- **All other supported tags:** target/ceiling **+10% total where possible**. A design that needs to exceed +10% requires a concrete balance reason and director review rather than silent arithmetic drift.
- Prefer finished path totals that land cleanly on **+5 / +10 / +15** bands where the kit supports that structure.

A dedicated Damage path should normally use **+2 Damage on the Hidden Art + +3 Damage on the Advanced Art = +5 total**.

**Rationale:** The element/classification is the actual potency identity the user wants Bloodright to modify. Equipment provenance and bloodline membership should not become hidden selectors. The ceilings keep raw Damage and leech under control while allowing high-leverage single-row mechanics such as Afterburn a larger but explicit band, and rounded path totals are easier to compare and communicate.

**Canonical destination:** Bloodright design brief, tree generator/validator, balance matrix and all generated trees on the active Fable Bloodright branch. Engine implementation remains a separate future task; where the current resolver is row-element-based rather than jutsu-classification-based, document the required resolver adjustment instead of narrowing the design back to bloodline-only behavior.

---

## RUL-2026-10-03-006 — Blood-Enchanted Eyes final approved four-path structure

**Date:** 2026-10-03  
**Domain:** Bloodright / Blood-Enchanted Eyes  
**Status:** ACTIVE  
**Supersedes:** none

**Ruling:** Blood-Enchanted Eyes uses the user-approved title **Crimson Covenant**, replacing **Tithe of the Red Eye** everywhere in the design source and generated outputs.

Its final approved four-path tree is:

- **Scarlet Gaze** — Foundation — +2% Increase Damage Given; +2% Increase Damage Taken.
  - **Opened Veins** — Hidden Art — +2 Damage.
    - **Rite of Exsanguination** — Advanced Art — +3 Damage.
  - **Crimson Thirst** — Hidden Art — +2% Lifesteal.
    - **Feast of the Fallen** — Advanced Art — +3% Lifesteal; +5% Increase Damage Given.

- **Iron in the Blood** — Foundation — +2% Decrease Damage Taken; +2% Decrease Damage Given.
  - **Closed Wounds** — Hidden Art — +3% Decrease Damage Taken.
    - **Deathless Vitality** — Advanced Art — +5% Decrease Damage Taken; +3% Decrease Damage Given.
  - **Carrion Fever** — Hidden Art — +3% Decrease Damage Given.
    - **Red Pestilence** — Advanced Art — +5% Decrease Damage Given; +3% Decrease Damage Taken.

The two Scarlet Gaze branches are offensive: **Burst** and **Sustain Offense**. The two Iron in the Blood branches are defensive: **Fortress** and **Suppression**. Blood-Enchanted Eyes has **no dedicated Afterburn Bloodright path** in this revision; native Afterburn remains usable but unamplified by this tree.

Potency scope is matching supported tags on **all Shadow jutsu** under RUL-2026-10-03-005. Wraith Pendant / Reaper's Ring provenance is not printed as a skill prerequisite or potency limitation.

**Rationale:** This gives the bloodline two clearly offensive and two clearly defensive commitments, restores the intended Damage route, keeps Lifesteal as the second offensive identity, and makes the defensive half mirror cleanly: Fortress reaches +10% Decrease Damage Taken with +5% Decrease Damage Given support, while Suppression reaches +10% Decrease Damage Given with +5% Decrease Damage Taken support. It also keeps Damage and Lifesteal at the new +5 ceilings.

**Canonical destination:** `docs/design/bloodright/trees/blood_enchanted_eyes.json` and its generated Markdown/SVG/validation, plus the cross-roster balance outputs on the active Fable branch.
