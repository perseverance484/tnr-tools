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

---

## RUL-2026-10-08-001 — White structural SVG standard for Bloodright trees

**Date:** 2026-10-08  
**Domain:** Bloodright / structural SVG presentation  
**Status:** ACTIVE

**Evidence:** “No path names at all, no colored theme, let the image gen handle creativity.” The user then confirmed: “Alright nvm im accepting your white one as the standard format. Lets commit that to repo so all sessions can use it as an example.”

**Ruling:** The accepted white BEE structural SVG is the reusable input-format example. Use neutral layout and blank illustration spaces, omit all path labels, and retain only functional role-marker colors. The user handles image generation. This settles structural SVG presentation, not a global balance budget or a finished-poster art style.

**Canonical destination:** `docs/workflows/BLOODRIGHT_POSTERS.md#standard-structural-svg-input`, with the persistent SVG and BEE-specific mechanical snapshot in `docs/design/bloodright/examples/blood_enchanted_eyes_structural.{svg,json}`.

---

## RUL-2026-10-08-002 — BEE pilot prices and durations

**Date:** 2026-10-08

**Domain:** Bloodright / Blood-Enchanted Eyes pilot

**Status:** ACTIVE

**Supersedes:** none

**Ruling:** Set every one of the 12 BEE pilot nodes to **20 Seichi Silver** and every compiled potency effect to **99 rounds**. This fills the eleven previously unresolved settings and retains Hungry Pulse's existing values.

**Evidence:** “Just do 20 silver for all and 99 rounds for all.”

**Rationale:** The user supplied the outstanding pilot pricing and duration decision. This applies to the current BEE package; it does not establish prices for other bloodlines or approve descriptions, folder visibility, release, or live execution.

**Canonical destination:** `forge/bloodright/bee.pilot.json`.

---

## RUL-2026-10-10-001 — Skyglass Ghost Ship drop stats and hidden-release assumption

**Date:** 2026-10-10  
**Domain:** Ghost Ship / Skyglass Project expansion / rewards and release  
**Status:** SUPERSEDED (see RUL-2026-10-10-002; historical Katana Consume spec, Crystal and visibility context retained below)  
**Supersedes:** earlier uncommitted Katana concept based on Night's Testament + shield potency; no prior RUL id

**Ruling:** The new **Skyglass Katana** is a **Legendary** weapon with **30 EP Damage** and **40% Consume**, using an approved *Legendary baseline* for other weapon fields such as cooldown, pool costs and AP (exact baseline numbers still need source identification and director sign-off). It drops independently at **3%** from the **Crowned Captain**. This supersedes the earlier Night's Testament exact-copy / shield-potency +X plan.

The new **Skyglass Crystal** is a **weapon-only** imbue with **30% Consume**, obtained via the previously approved Skyglass Reliquary hybrid chest loop (including a 3% direct Crystal roll and the 12-Filament crafting route). These are director-approved effect and source values, **not** proof of engine validity: current Consume validation/imbuement behavior must be resolved without altering the promised mechanic.

**Operational clarification:** The director reports both Ghost Ship profession quests currently **hidden**; the earlier October 1 capture's `hidden:false` state is historical, not current. A fresh read-only capture is required before edits. The implementation must retain hidden state; publication is separately director-owned and not authorized by this ruling.

**Rationale:** Fix the two new reward identities and rates without allowing the earlier concept placeholder to survive into manifests, and prevent a stale public-visibility capture from driving an unnecessary or dangerous live cutover.

**Canonical destination:** `state/ghost_ship_skyglass_reward_decisions.md` for operative task-specific values and technical gates; `docs/design/GHOST_SHIP_SKYGLASS_FULL_MANIFEST_ROADMAP.md` for the release workplan. Generated schemas, actual game source, and new operator-readback captures retain their separate authority for contracts and current storage state.

---

## RUL-2026-10-10-002 — Skyglass Katana three-effect final direction

**Date:** 2026-10-10  
**Domain:** Ghost Ship / Skyglass Project expansion / Skyglass Katana rewards  
**Status:** SUPERSEDED by RUL-2026-10-10-007 (historical 30 EP Damage + Shield version)  
**Supersedes:** RUL-2026-10-10-001

**Ruling:** **Skyglass Katana** is a **Legendary WEAPON** dropped by the **Crowned Captain at 3%** independently of his **20% Skyglass Crown fragment**. The exact weapon effects are **30 EP Damage**, **300 HP Shield for 2 rounds** on the wielder, and **Immunity to Buff Prevent for 2 rounds** on the wielder. The previous **40% Consume** effect on the Katana is REMOVED; do not include both. These are three effects, at TNR's normal maximum. The shield is an on-use temporary self shield, not shield-potency scaling.

The effect intent maps to `damage` (raw power 30), `shield` (`health:300`, `rounds:2`, `target:SELF`, `power:100` to guarantee creation), and `immunity` (`blocks:buffprevent`, `rounds:2`, `target:SELF`). The immunity blocks **new Buff Prevent effects** during its duration; it does not clear already-active Buff Prevent or immunize against every debuff. This mapping is supported by `45c_DATA_constructors.json` and pinned game source `studie-tech/TheNinjaRPG@4774560eb6e8c9a5ef156d66b953dcb6aeeba4d6`; offline integration behavior and remaining Legendary weapon cooldown/AP/pool baseline values must still be checked before manifest freeze.

**Unchanged:** The **Skyglass Crystal** remains a Ghost Ship-exclusive **weapon-only 30% Consume** imbue, sourced from the approved Reliquary hybrid rewards (including its 3% direct opening roll and 12-Filament recipe). Both Ghost Ship profession quests remain hidden per director report, requiring a fresh read-only capture before edits. No live-game writes or publishing are authorized.

**Rationale:** Give the Crowned Captain's command blade a fixed, predictable defensive identity instead of the prior damage-conversion mechanic, without silently changing the separate Crystal's Consume chase or any protected production-release decisions.

**Canonical destination:** `state/ghost_ship_skyglass_reward_decisions.md` is the operative design/reward record; `docs/design/GHOST_SHIP_SKYGLASS_FULL_MANIFEST_ROADMAP.md` governs task/release sequencing. Item effect schemas and engine behavior remain owned by generated contracts/pinned source, not this ruling.

---

## RUL-2026-10-10-003 — Ghost Ship Skyglass Expedition 83-node structure approved

**Date:** 2026-10-10  
**Domain:** Ghost Ship / Skyglass Project / expanded quest structure  
**Status:** ACTIVE (structural approval; prose, combat, art and build not frozen)  
**Supersedes:** the preserve-57-nodes / preserve-all-original-edges constraint in the base Ghost Ship retheme patch for expansion planning only; no earlier RUL ID is changed.

**Ruling:** The director APPROVED **Model B: Skyglass Expedition** as represented by the six-ending **83-objective design** in `state/ghost_ship_skyglass_expansion_design.md` and `state/ghost_ship_skyglass_graph_patch.json`, both at the design-branch freeze candidate `7ac886b845b88e76a9fd7206ce0e025d2cfce230`. Both existing Gather/Hunt quests preserve all 57 original objective IDs and five established endings, rewire 12 original forward paths, and introduce 26 nodes including a **mutually exclusive sixth `w_secret` ending** that guarantees one Skyglass Reliquary. The newly added route proceeds via hull infiltration, Core Horror, optional reconstruction/chamber investigation, the fixed quarantine-seal puzzle, the Quarantined Archive, and the new **Sealwright** elite encounter.

Wrong quarantine-seal answers **close the secret route for that quest run**, returning the player to the normal adventure rather than failing the quest; the correct answer reaches the archive. The Oathkeeper `Time` solution retains the short **two-battle Crowned Captain farming route** with optional, bypassable lore. The extra crew-history dialogs, ordinary-Captain gallery/aftermath, visible shore-puzzle feedback, and preserved nine-beat Skyglass reveal are part of the accepted structural shape. No additional battle is mandatory on the oathbound route. New combat balancing, final dialogue wording, item mechanics, art, and user-run execution remain separate approvals.

**Rationale:** Expands the airborne ship's exploration, investigation and rewards without discarding working quest IDs, making the Crown farm slower, or creating a generic new series of battles. The graph's offline structural checks passed for both October 1 profession captures, but do not establish full manifest validity or current live state.

**Canonical destination:** `state/ghost_ship_skyglass_expansion_design.md` is the expanded content-design owner and `state/ghost_ship_skyglass_graph_patch.json` its machine-readable structural proposal; `docs/design/GHOST_SHIP_SKYGLASS_FULL_MANIFEST_ROADMAP.md` coordinates the next content/combat/art tasks. Original `state/ghost_ship_retheme_patch.json` remains the authority for unchanged base retheme text and identities. Schemas, engine laws, captures, and live state retain independent authority.

---

## RUL-2026-10-10-004 — Sealwright is a regular-Captain-tier boss using boss-pool jutsu

**Date:** 2026-10-10  
**Domain:** Ghost Ship / Skyglass Expedition / Sealwright combat
**Status:** ACTIVE (combat-tier direction approved; exact kit and runtime parity still under review)  
**Supersedes:** the earlier 2.5× stats / 3.0× pools mid-tier Sealwright combat draft (unruled). Refines Sealwright combat tier under RUL-2026-10-10-003 without changing the approved 83-node structural graph.

**Ruling:** Sealwright must be **on par with the regular Captain** in practical battle difficulty, not a lesser elite, and must use meaningful **boss-pool abilities** from the existing shared AI jutsu pool. The current captured regular Captain profile is Level 100 / JONIN, **3.0× stats, 2.5× pools, regeneration 60**; matching those values is the recommended initial numeric parity baseline, subject to real-equipment/effective-combat comparison. Do not silently make Sealwright Crowned-Captain tier or add another phase, separate chest drop, or non-pool jutsu. He remains the solitary Quarantined Archive guardian on the already approved mutually exclusive secret route.

**Candidate, NOT yet frozen by this ruling:** the revised six-move proposal uses boss-grade **B14 Cataclysm Detonation** and **B16 Sovereign Fetters**, supported by **B22 Compression Barrier**, **B33 Piercing Judgment**, **S27 Weakening Strike**, and **S31 Unraveling Strike**. B16's two-round Stun plus Seal requires special comparative balance testing. The director approved the **tier and boss-pool inclusion direction**, not this exact kit, AI rules, or eventual battle results.

**Rationale:** The secret Reliquary ending deserves a proper boss encounter of comparable difficulty to the regular Captain while retaining a technically distinct defensive containment identity. Mirroring raw multipliers without analyzing cooldowns, control windows and Captain equipment would overstate parity.

**Canonical destination:** `state/ghost_ship_skyglass_sealwright_combat_draft.md` owns the current technical combat proposal; `state/ghost_ship_skyglass_expansion_design.md` owns the approved quest narrative/graph; `docs/design/GHOST_SHIP_SKYGLASS_FULL_MANIFEST_ROADMAP.md` owns sequencing. The shared pool and captured AI profiles retain their evidence authority.

---

## RUL-2026-10-10-005 — Sealwright reserves Nullifying Wave against excessive IDG

**Date:** 2026-10-10  
**Domain:** Ghost Ship / Skyglass Expedition / Sealwright AI behavior  
**Status:** ACTIVE (specific seventh-jutsu and trigger approved; remaining rotation under review)  
**Supersedes:** none; refines the provisional six-move kit discussed under RUL-2026-10-10-004

**Ruling:** Equip **Nullifying Wave (B32, shared-pool ID `JWZYiHKPNwYziWEFjw4Fn`)** as the **seventh jutsu** on Sealwright. **Do not cast it during ordinary rotation.** Use it **only when the opponent's summed Increased Damage Given (IDG) exceeds 70**, and only when cooldown, action points, targeting and range permit. It has a **100% Clear** effect, **60 AP cost**, **8-round cooldown** and **range 5**. Place the conditional response first; if unavailable, fall through to the six normal moves.

**Source-backed rule encoding:** `target_has_effect` with `effectType:"increasedamagegiven"`, `target:"CLOSEST_OPPONENT"`, and `threshold:71`, AND `distance_lower_than` with `target:"CLOSEST_OPPONENT"`, `value:6`; action `use_specific_jutsu` with matching target and B32's ID. The game engine tests **sum(effect.power) >= threshold**. Because the threshold is integer, totals between 70 and 71 are not expressible as strict >70 without engine change. `clear 100` removes all removable positive effects, not IDG selectively; `clearprevent` may block it.

**Rationale:** Prevent extreme offensive buff stacking from trivializing a Captain-tier encounter without turning Nullifying Wave into a routine dispel. The six rotating techniques and their effective difficulty remain independently reviewable.

**Canonical destination:** `state/ghost_ship_skyglass_sealwright_combat_draft.md` owns detailed implementation and source-backed AI rule; `docs/design/GHOST_SHIP_SKYGLASS_FULL_MANIFEST_ROADMAP.md` tracks next work. Current upstream code for the condition is `studie-tech/TheNinjaRPG@4774560eb6e8c9a5ef156d66b953dcb6aeeba4d6` in `app/src/libs/combat/ai_v2.ts`.

---

## RUL-2026-10-10-006 — Sealwright dual-Clear overlap is intentional core playstyle

**Date:** 2026-10-10  
**Domain:** Ghost Ship / Skyglass Expedition / Sealwright combat identity  
**Status:** ACTIVE (seven-jutsu design accepted; effective parity and final rule order still require offline validation)  
**Supersedes:** the concern that regular Unraveling Strike could make the B32 reserve redundant; refines RUL-2026-10-10-004/005 without superseding their combat tier or trigger.

**Ruling:** The director explicitly wants the Sealwright to **constantly strip removable positive buffs**. Regular **S31 Unraveling Strike** (Damage 40 plus Clear 100, range 3, cooldown 5) is his routine, high-priority damaging dispel and must remain in the normal rotation; **B32 Nullifying Wave** (Clear 100, range 5, cooldown 8) remains **equipped as the seventh jutsu**, used **only** when the same targeted opponent's total Increased Damage Given (IDG) is strictly above 70 (source-backed integer threshold 71), with normal range/AP/cooldown constraints. **Overlapping Clear effects are intentional, not a flaw to eliminate**. S31 may remove IDG before the emergency threshold is reached; that is desired, not cause to weaken either effect. Both jutsu remove *all removable positive buffs*, not only IDG. `clearprevent` and other existing game rules still apply.

The working seven-technique roster is **B22 Compression Barrier, B16 Sovereign Fetters, B14 Cataclysm Detonation, B33 Piercing Judgment, S27 Weakening Strike, S31 Unraveling Strike, B32 Nullifying Wave**. Captain-tier parity, other pool jutsu and no independent Sealwright loot remain as previously directed. Specific AI priority/positioning and measured difficulty need offline tests before final manifest freeze; no new jutsu, game modifications or publications are authorized.

**Rationale:** Make buff denial the core active Sealwright identity instead of an optional response, while preserving a separately threshold-gated emergency purge when players push IDG exceptionally high. The deliberate double-Clear distinguishes the archive custodian from the regular Captain.

**Canonical destination:** `state/ghost_ship_skyglass_sealwright_combat_draft.md` owns this design; `state/ghost_ship_skyglass_sealwright_rule_contract.json` owns the source-backed AI-rule proposal and tests; `docs/design/GHOST_SHIP_SKYGLASS_FULL_MANIFEST_ROADMAP.md` owns sequencing.

---

## RUL-2026-10-10-007 — Skyglass Katana Pierce/Consume Sword and Crystal 20% Consume

**Date:** 2026-10-10  
**Domain:** Ghost Ship / Skyglass Project / final intended item identities  
**Status:** ACTIVE (item effects and category approved; unprovided baseline/engine validation still open)  
**Supersedes:** RUL-2026-10-10-002 for all prior Katana effects; supersedes the earlier Crystal Consume 30% design in RUL-2026-10-10-001/002. Quest, Sealwright and other reward decisions remain in force.

**Ruling:** The new **Skyglass Katana** is a **LEGENDARY WEAPON of weapon type SWORD** that **cannot be imbued**. Exactly three item effects are authorized: **50 EP Pierce** (one `pierce` effect), **Buff Prevent immunity on SELF for 2 rounds** (one `immunity` tag with `blocks:"buffprevent"`), and **40% Consume** (one `consume` tag). No separate flat Shield, no standard Damage tag, no historical shield-potency modifier, and no additional imbuement slot are authorized. The `canBeImbued:false` field enforces no imbuement; do not try setting the schema's minimum-one `maxImbueNumber` to zero. Cooldown, AP, pool costs, range, equip slot and other Legendary Sword baseline fields have not been numerically selected and remain subject to captured-reference review.

The new **Skyglass Crystal** remains a **CRYSTAL**, restricted to `crystalTargetTypes:"WEAPON"`, with **exactly one Consume 20% effect** (changed from 30%). The Crystal cannot be applied to the Katana since the Katana forbids imbuing. Crystal rarity/trading and one-tag validation/activation are not settled by this ruling.

**Reward sourcing unchanged:** Skyglass Katana drops independently at **3%** from Crowned Captain, whose Skyglass Crown fragment independently drops at **20%**. The secret route guarantees **one Skyglass Reliquary**. The Reliquary retains a **3% independent Crystal roll** and the **12-Skyglass-Filaments-to-one-Crystal** crafting route and other already approved chest outcomes.

**Technical consequence:** In current TNR source `studie-tech/TheNinjaRPG@cddd7d91c9e6bdebc978ddcb61e5b8a305bd0f93`, a WEAPON effect array containing **Pierce plus Consume** meets `SuperRefineEffects` companion-tag conditions, and damage calculations for Pierce create outgoing damage eligible for Consume's conversion. This supports, but does not replace, offline validator and combat testing. Conversely, a **Consume-only CRYSTAL** fails item-level validation because the crystal's **own** effects array lacks Damage/Pierce, even when the target weapon provides an attack effect after imbuing. An upstream corrective change, if warranted, needs a separately approved technical implementation and tests. Do not add unrequested filler damage/pierce.

**Rationale:** Give the Crowned Captain's personal Sword a penetrating attack and damage-to-shield defensive loop that is powerful but cannot accept further imbuements, while offering a distinct weaker Consume bonus as a Ghost Ship-exclusive weapon crystal. Historical posters or numeric examples are not authoritative after this ruling.

**Canonical destination:** `state/ghost_ship_skyglass_reward_decisions.md` (operative item design), `docs/design/GHOST_SHIP_SKYGLASS_FULL_MANIFEST_ROADMAP.md` (release gates), and `state/prompt_ghost_ship_skyglass_stage2_feasibility.md` (offline technical study). Schemas/source and fresh readbacks retain independent authority for mechanics/live state.

---

## RUL-2026-10-11-001 — Selectively preserve distinctive Ghost Ship legacy jutsu

**Date:** 2026-10-11

**Domain:** Ghost Ship combat identity and shared-pool migration

**Status:** ACTIVE DIRECTION; exact retained roster and revised hybrid kits still require selection.

**Supersedes:** wholesale replacement/retirement of all legacy-only Ghost Ship jutsu and the automatic new-record clone of Explosion in `state/ghost_ship_shared_pool_migration.json`. It does not change the approved quest graph, rewards/items or Sealwright's seven-jutsu identity.

**Ruling:** Keep approximately twelve legacy jutsu that the shared global pool cannot genuinely replace, explicitly including Explosion and prioritizing most of the awakened/Crowned Captain's distinctive moves. Update retained jutsu names/descriptions for the Skyglass retheme while keeping their existing mechanics. Replace redundant jutsu with genuinely suitable shared-pool techniques. Do not equate matching effect labels with equivalent AP economy, target scope, control duration or behavior.

**Not yet decided:** the exact roster/count, final names/descriptions, per-enemy hybrid kits and rule order, or any mechanical repair. The eleven-record review is a recommendation, not a newly approved roster. Removal from Ghost Ship kits is not proof that a record has no other consumers; database deletion remains dependency-gated.

**Consequence:** the regular-Captain comparison kit used for Sealwright parity must be reconciled with the retained legacy selection before it is frozen. Katana/Crystal feasibility work and Sealwright's approved seven moves remain in scope unchanged.

**Canonical destination:** `state/ghost_ship_legacy_retention_review.md` owns the new retention policy and candidate comparison; `state/ghost_ship_shared_pool_migration.json` is explicitly marked superseded for final kit selection; the Stage 2 brief and full roadmap point at this gate.

---

## RUL-2026-10-11-002 — Approve the eleven retained jutsu and perform Skyglass conversion

**Date:** 2026-10-11
**Domain:** Ghost Ship / Skyglass jutsu identity
**Status:** ACTIVE; retained roster approved and presentation conversion authorized. Final authored copy and hybrid AI kits remain subject to acceptance.
**Supersedes:** the pending exact-roster selection in RUL-2026-10-11-001; its mechanical-preservation, shared-replacement and dependency requirements remain active.

**Ruling:** dauntless approved the recommended eleven legacy records and requested their conversion to fit the new quest theme. Retain their existing IDs and all mechanics; author new top-level `name`, `description` and `battleDescription` only. The approved roster is Explosion! (`nCQETf-HNnbRec1OSY2-R`), Ghostly Deep Six (`ddbIyVtoxdPQwLRXxSBq8`), Ghostly Final Fathom (`X2P22h8ApDmTZHjWpNO87`), Death's Grasp (`PdD44PGaNv4MN5fOALhAF`), Ghostly Shipwreck Delusion (`EQ93LX8wvuIAd5u75q_i1`), Counter Stance (`T3glZGcSd-jS8G-NB43GR`), Death's Door (`0Y10JpChssDwFUxNRk6p3`), Ghostly Crossed Out (`wMcoazoyXaEXViSCn5weF`), Ghostly Rigging Snare (`1jXfTgrtGUaSfqTPSSa83`), Ghostly Strangling Weed (`Jz4Lb55NcpwZn3nUK5PrJ`) and Battle Trance (`MG9ZujAV8lK7--YxThVbQ`). Eleven satisfies the approximate twelve target; no quota padding is requested.

**Conversion scope:** Use Skyglass command seals, preserved combat patterns and damaged ship reconstruction. This does not authorize mechanical repairs, changes to nested effect fields, new records, shared-global jutsu renames, art replacement, live-game actions or a full implementation manifest. Explosion is retained on its original ID; the former clone plan remains superseded. Fresh operator captures and dependency review precede eventual edits, including checks for external consumers. Fable remains the implementation owner.

**Remaining gates:** The newly authored names/descriptions/battle text have not yet received separate final presentation acceptance. Per-enemy hybrid kits and AI rules remain open; final Sealwright parity must use the revised regular Captain. The quest graph, rewards/items, locked art and Sealwright's seven shared jutsu, including intentional double Clear, are unchanged.

**Rationale:** Preserve the distinctive actions already selected while making their presentation native to the approved Skyglass setting, without turning a thematic conversion into a balance change.

**Canonical destination:** `state/ghost_ship_legacy_retention_review.md` owns the approved selection. `state/ghost_ship_legacy_jutsu_conversion.json` owns the authored before/after text and preservation evidence; its `.md` companion supports review. The full roadmap, retheme design and Stage 2 brief record the resulting scope and comparator gates.

---

## RUL-2026-10-11-003 — Accept hybrid kits as the Stage 2 test baseline

**Date:** 2026-10-11

**Domain:** Ghost Ship / Skyglass combat membership and offline validation

**Status:** ACTIVE; membership and substitution direction accepted for offline tests. Final rule behavior and measured balance remain pending.

**Supersedes:** pending kit-selection approval in RUL-2026-10-11-001/002 and the corresponding proposal status in `state/ghost_ship_hybrid_kit_proposal.json`. The historical wholesale shared-pool migration remains superseded.

**Ruling:** dauntless approved the complete hybrid-kit direction presented at `89fa921c839a9830fd66bb64aa267c470e8dd678` and requested the next task. Accept all eleven existing-enemy memberships, shared substitutions and consolidations in that packet as the baseline for Fable's offline tests: 65 equipped memberships, eleven retained legacy IDs and eighteen shared IDs. Preserve every original retained/shared membership. Sentinel's new Rigging Snare and Hollow Timber assignments are explicitly accepted, including disclosed element/range/cooldown differences. First Blade's EL04 Ion Lance replacement and its disclosed Lightning/power/cadence differences are accepted. Shared ordinary-attack and stance potency/cooldown differences are accepted for testing without an equal-difficulty claim.

**Captain comparator:** Preserve the regular Captain's five captured moves: Unbroken Command, Remembered Form, Keelbind, B14 Cataclysm Detonation and B17 Worldbreaker Chorus. Crowned Captain keeps eleven moves with Sharpened Focus replaced by EA03 Windlash Focus. The six-move all-shared regular-Captain comparator is not operative. Preserve full numeric profiles and innate effects; do not add filler or silently tune retained records.

**Still open:** Fable's exact AI rules and measured parity; any test-driven adjustment; whether Crowned Captain should actively rotate its equipped but unselected heal/copy/reflect support; final presentation acceptance. The approval does not authorize those behavior changes, engine modifications, art changes, live requests/writes, publication or a full implementation manifest. Sealwright's seven moves and deliberate double Clear, item contracts and quest/reward structure remain unchanged.

**Next task and ownership:** Fable performs the already-authorized offline Stage 2 technical work on a separate owned branch and returns a frozen exact-SHA report/tests for independent review. ChatGPT records the acceptance and prepares the concrete handoff; the director retains final balance and release authority.

**Canonical destination:** `state/ghost_ship_hybrid_kit_proposal.json` / `.md` own the accepted kit baseline under their stable historical filenames. `state/prompt_ghost_ship_skyglass_stage2_feasibility.md` remains the exact test brief; `state/prompt_ghost_ship_skyglass_stage2_start.md` supplies the acceptance and delivery handoff.


---

## RUL-2026-10-11-004 — Skyglass Katana baseline: Night's Testament, Crystal Pierce, drop-only, tradable

**Date:** 2026-10-11

**Domain:** Ghost Ship / Skyglass rewards: Skyglass Katana non-effect fields

**Status:** ACTIVE. Settles the "Legendary Sword baseline" gate left open by RUL-2026-10-10-007.

**Supersedes:** nothing in RUL-2026-10-10-007's effects or sourcing. It fills that ruling's unselected baseline fields. The superseded "exact Night's Testament clone with shield-potency swap" variant stays superseded; this ruling uses Night's Testament only for non-effect fields and existing shared effect fields.

**Evidence:** operator read-only capture push/85, `harvests/inbox/tnr_results_1791727479372.json` (job `85-mv3wa2l9`). Night's Testament `osJq3k77YPGoFWgof12FQ` is a full LEGENDARY WEAPON/SWORD record. The comparison is in `docs/reviews/GHOST_SHIP_SKYGLASS_CAPTURES_85_86_2026-10-11.md`.

**Ruling:** dauntless chose **Night's Testament as the Skyglass Katana baseline**. Every non-presentation field copies the captured row, with these exceptions:

1. Effects are exactly RUL-2026-10-10-007's three: Pierce 50 (Night's Testament's own Pierce tag), SELF Buff Prevent immunity for 2 rounds (Night's Testament's own immunity tag), and Consume 40%. The Pierce's element is **Crystal**, replacing Shadow.
2. `canBeImbued:false` (RUL-2026-10-10-007).
3. **Drop-only:** `canBeCrafted:false`, `craftingExperience:0`. The 3% independent Crowned Captain drop stays the sole source.
4. **Tradable:** `canBeTraded:true`, as on Night's Testament.
5. Created `hidden:true` per creation doctrine; publication is separate.

The resulting values are:
- AP 40, cooldown 6, range 4, OTHER_USER / SINGLE;
- chakra 40, stamina 40, health 0, no per-level reducers;
- slot HAND, maxEquips 1, durability 100, required level 1, no stat or mastery requirements;
- battle usage BOTH, cost 1 ryo, not in shop, stack 1, xpToLevel 1000.

**Not settled here:** description, battle description, image, and the effect animation/SFX asset IDs. These are presentation and art, are not copied from Night's Testament, and remain pending. No write manifest, art or publication is authorized.

**Canonical destination:** `state/ghost_ship_skyglass_reward_decisions.md` owns the operative Katana specification. `state/ghost_ship_skyglass_katana_record.json` holds the derived field-level record, produced by `harness/ghost_ship_stage2/tools/build_katana_record.py` from the capture. Offline gate C3 validates it.

---

## RUL-2026-10-11-005 — Active Consume: Katana 15%, Crystal 10%

**Date:** 2026-10-11

**Domain:** Ghost Ship / Skyglass item effects

**Status:** ACTIVE; revised rates and active-buff behavior approved. Timing and updated runtime validation remain pending.

**Supersedes:** the Katana40 / Crystal20 Consume rates and instant-only interpretation in RUL-2026-10-10-007, the derived r4 records and RUL-2026-10-11-004's historical effect reference. All other accepted effect, baseline, economy and acquisition fields remain unchanged.

**Ruling:** dauntless reports the engine's changed Consume behavior: Consume grants an active buff and qualifying hits while active grant shield, rather than conversion being tied directly to a single damage instance. Set Skyglass Katana Consume to **15%** and Skyglass Crystal Consume to **10%** using that behavior.

Katana remains exactly Pierce50 (Crystal element), SELF Buff Prevent immunity2r and Consume15; LEGENDARY WEAPON/SWORD, `canBeImbued:false`, with the accepted Night's Testament non-effect baseline, drop-only/tradable economy and independent 3% Crowned Captain drop. Crystal remains a WEAPON-only CRYSTAL with exactly Consume10 and no added Damage/Pierce. Its 3% Reliquary drop and 12-Filament recipe are unchanged. All other rewards, quest structure, AI/jutsu decisions and art locks remain unchanged.

**Source boundary:** reviewed upstream `studie-tech/TheNinjaRPG@585534d7eb21d6f0dd678d5c3eb92662f611d39b` implements active Consume. Its validator requires a same-array Damage/Pierce companion only for instant Consume (`rounds === 0`); positive-duration standalone Consume is source-admissible. This source check is not exact revised-item runtime validation or verification of deployment. The old Crystal correction proposal is historical, not an automatic implementation requirement.

**Timing not selected:** active Consume duration and generated-shield lifetime are separate fields. Source defaults are 3/3; these may be labelled offline test carriers, not assumed balance approval. Do not carry forward the old explicit `rounds:0`. Weapon actions grant the buff; this ruling does not turn the weapon into permanent on-equip Consume.

**Implementation boundary:** preserve frozen r4 old-pin evidence, including the former Katana record, builder and harness. Fable owns the next derived-record and offline test revision; old PASS results do not validate this change. No engine modification, live request/write, art change, full manifest or publication is authorized by this adjustment.

**Canonical destination:** `state/ghost_ship_skyglass_reward_decisions.md` owns the operative specification. `state/ghost_ship_skyglass_consume_revision.json` is the machine-readable design delta, not a full record. `state/prompt_ghost_ship_skyglass_consume_revalidation.md` supplies the bounded Fable test brief; the full roadmap points to these current gates.

---

## RUL-2026-10-11-006 — Consume 2/2; Legendary, tradable, non-craftable Crystal

**Date:** 2026-10-11

**Domain:** Ghost Ship / Skyglass item timing and Crystal economy

**Status:** ACTIVE design approval. Final-record offline tests and independent acceptance remain required.

**Supersedes:** unresolved Consume timing and Crystal rarity/trading/crafting in RUL005 and earlier decisions; removes the previously approved12-Filament Crystal recipe. Does not change rates, other effects, Katana baseline/economy, independent drop chances or the Reliquary contents.

**Ruling:** dauntless selected “2/2 for Consume”: **both Skyglass Katana and Skyglass Crystal use active Consume `rounds:2` and generated-shield `shieldRounds:2`**. Katana remains15%; Crystal remains10%. The Crystal is **LEGENDARY**, **tradable** (`canBeTraded:true`) and **not craftable** (`canBeCrafted:false`). Its independent3% Reliquary roll remains; the12-Filament crafting route is removed from future construction. This does not remove Filament drops or invent a replacement use/trading decision for them. Native imbuement access remains engine-governed.

**Explicit deferral:** Consume overlap need not be resolved now. It is not a blocking director decision for this pass. Preserve native behavior and technical evidence; do not implement stacking changes or new restrictions.

**Combat request:** dauntless also requested Sealwright combat behavior design. This authorizes a concrete proposal; it does not constitute acceptance of the newly authored priority/movement/filler plan or numerical parity. The already approved seven jutsu, double-Clear intent and Captain-tier target remain locked.

**Evidence boundary:** the active-Consume package `fcd79e5a3401dc8d95abbdaa05d0d4664c04a6e2` tests3/3 carriers at engine `585534d7eb21d6f0dd678d5c3eb92662f611d39b`. Preserve it and r4 as historical evidence. Fable must deliberately produce/test2/2 records and the selected Crystal economy; no old PASS is relabelled. No engine change, live request/write, art, full manifest or publication is authorized.

**Canonical destination:** `state/ghost_ship_skyglass_reward_decisions.md`; companion `state/ghost_ship_skyglass_final_item_contract.json`; bounded Fable brief `state/prompt_ghost_ship_skyglass_final_item_revalidation.md`. Sealwright's new proposal is linked from its existing combat draft to `state/ghost_ship_skyglass_sealwright_behavior_proposal.md`.

---

## RUL-2026-10-11-007 — Activate Crowned Captain healing, conditional Copy and regular Reflect

**Date:** 2026-10-11

**Domain:** Ghost Ship / Skyglass / Crowned Captain support behavior

**Status:** ACTIVE design direction. Exact Copy threshold, native heal boundary, final order and balance acceptance remain pending.

**Supersedes:** the unresolved choice of whether to activate Crowned Captain's equipped Second Wind, Stolen Form and Rebounding Form in RUL003 and the hybrid-kit review. Does not approve the old experiment's heal50/Copy30/Reflect-distance3 values.

**Ruling:** dauntless directed that Crowned Captain **heal at 40% health**, **copy when enemies have high IDG**, and **use Reflect as part of his regular rotation**. Activate the already equipped S35 Second Wind, B07 Stolen Form and retained Rebounding Form accordingly. Preserve their original mechanics and IDs, all eleven accepted memberships, profile/innates and approved rewards/farming route. No extra technique or stat tuning is implied.

**Unresolved details:** “high IDG” has no director-selected number. The companion proposes threshold71 on CLOSEST_OPPONENT with native distance gate5, ahead of routine Clear; this number/selector/order is not accepted by this ruling. Native `health_below:40` is strictly below40%, not inclusive of exactly40; disclose and obtain acceptance of that boundary rather than silently substituting41. The candidate uses ordinary SELF Reflect without a health/distance condition, subject to existing AP/cooldown rules. Final priority and measured consequences remain test/review work.

**Canonical destination:** `state/ghost_ship_skyglass_crowned_support_behavior.md` owns the activation direction and bounded Fable test brief. `state/ghost_ship_hybrid_kit_proposal.md` points to it; unchanged JSON and historical A1 results retain their original membership/test scope. No engine change, live request/write, art, manifest or publication is authorized.

---

## RUL-2026-10-11-008 — Accept Crowned Captain IDG71 and strict-below40 healing

**Date:** 2026-10-11

**Domain:** Ghost Ship / Skyglass / Crowned Captain support triggers

**Status:** ACTIVE design approval; runtime validation and final measured balance remain pending.

**Supersedes:** the unresolved Copy number and native heal-boundary questions in RUL007. Preserves regular Reflect and all approved memberships/mechanics/rewards.

**Ruling:** dauntless approved the explicit clarification: **Copy at summed IDG 71 or higher**, and **heal using the native `health_below:40` condition**, strictly below 40% of effective maximum health. Exactly 40% does not trigger healing. Do not replace the threshold with41 or introduce inclusive-boundary engine changes. The historical Copy30/heal50 experiment remains superseded for new behavior construction.

**Scope:** these two numerical/boundary decisions are closed. The companion's Heal → conditional Copy → Reflect → existing offense order and same-target native selector remain the implementation candidate for Fable's tests; this approval is not a runtime PASS or final balance acceptance. No live requests/writes, engine changes, art, manifest or publication.

**Canonical destination:** `state/ghost_ship_skyglass_crowned_support_behavior.md`; the hybrid-kit readable companion and full roadmap track the closed trigger decisions. Preserve historical JSON, harnesses and results unchanged.

---

## RUL-2026-10-12-001 — Accept Crowned Captain support behavior as tested

**Date:** 2026-10-12

**Domain:** Ghost Ship / Skyglass / Crowned Captain support behavior

**Status:** ACTIVE.

**Supersedes:** the open order/selector and measured-balance questions left by RUL-2026-10-11-007/008.

**Evidence:** Fable offline package `perseverance484/tnr-tools@4369f404dbfd83563d11508c2bcc2e0e17f9a786` (`harness/ghost_ship_final/`, CROWNED 36/0; `docs/reviews/GHOST_SHIP_FINAL_ITEMS_CROWNED_OFFLINE_RESULTS.md` §5). On engine `585534d7…`, the Captain won 66/66 test fights. Support lowers offensive AP from about 92 to 70 per round and raises survivability when hurt (forced 45% start: 52.0% left vs 37.4%).

**Ruling:** dauntless accepted the tested behavior: S35 Second Wind (`health_below:40`, SELF) → B07 Stolen Form (`target_has_effect` IDG ≥ 71, CLOSEST_OPPONENT, `distance_lower_than:5`, same target) → Rebounding Form (SELF, no condition) → the prior candidate-remapped chain with `includeDefaultRules` unchanged. The slower, more attritional fights are accepted. The regular Captain is not given these rules.

**Canonical destination:** `state/ghost_ship_skyglass_crowned_support_behavior.md`. Boss innate IDG is changed separately by RUL-2026-10-12-004.

---

## RUL-2026-10-12-002 — Accept the Sealwright behavior proposal as final, without new-pin testing

**Date:** 2026-10-12

**Domain:** Ghost Ship / Skyglass / Sealwright combat behavior

**Status:** ACTIVE.

**Supersedes:** the pending acceptance and the requested four-variant new-pin comparison in `state/ghost_ship_skyglass_sealwright_behavior_proposal.md`.

**Ruling:** dauntless accepted the proposal's exact priority list as final Sealwright behavior: B32 (IDG ≥ 71, CLOSEST_OPPONENT, `distance_lower_than:6`) → S31 (`distance_lower_than:4`) → B22 SELF → B16 / B14 / B33 / S27 (`distance_lower_than:6`) → singleton basic attack when adjacent → late `move_towards_opponent` (`distance_higher_than:3`) → `end_turn`, with `includeDefaultRules:false`. The seven jutsu and double-Clear identity stay unchanged.

**Explicitly declined:** a new-pin verification run. dauntless chose to skip it. The last measured evidence is old-pin (`cddd7d91…`): Sealwright lost the durable-striker fixture 0/5. No new parity claim is made. Sealwright's innate IDG is changed by RUL-2026-10-12-004, which postdates that evidence.

**Canonical destination:** `state/ghost_ship_skyglass_sealwright_behavior_proposal.md` (now the accepted behavior) and `state/ghost_ship_skyglass_sealwright_combat_draft.md`.

---

## RUL-2026-10-12-003 — Approve the candidate rule remap for the nine other Ghost Ship AIs

**Date:** 2026-10-12

**Domain:** Ghost Ship / Skyglass / AI rules

**Status:** ACTIVE.

**Ruling:** dauntless approved the mechanical candidate remap: each captured rule's jutsu IDs and combo IDs are remapped through the accepted RUL-2026-10-11-003 kit mapping, with consecutive duplicates collapsed in combos. Nothing else changes: conditions, targets, ordering and `includeDefaultRules` stay as captured. The regular Captain needs no remap. Crowned uses RUL-2026-10-12-001 on top of its remap. Sealwright has its own rules (RUL-2026-10-12-002). The ledger is `harness/ghost_ship_stage2/results/a1.json` `ruleChangeLedger` (produced by `F.remappedRules`).

**Canonical destination:** `state/ghost_ship_hybrid_kit_proposal.md`.

---

## RUL-2026-10-12-004 — Keep minion innate IDG; bosses get proportionally higher innate IDG

**Date:** 2026-10-12

**Domain:** Ghost Ship / Skyglass / AI innate effects (tuning)

**Status:** ACTIVE design decision. Fresh new-pin measurement is recommended before manifest construction.

**Supersedes:** the open "minion duplicate innate IDG" decision. Narrows the RUL-2026-10-11-003/007 instruction "no stat adjustments / preserve innate arrays", for the three bosses only.

**Ruling:** dauntless kept the seven minions' captured duplicate innate IDG unchanged (sustained 99-round totals 200–350%, opening peaks up to 420%). The bosses must sit slightly above the minions, so their sustained innate IDG becomes:

- **Regular Captain: +375%** (new; keeps its captured increasestat 30% innate);
- **Sealwright: +375%** (new; Captain-tier pair);
- **Crowned Captain: +450% total** (his captured 60% 99-round entry is replaced by 450%).

Each value is one 99-round `increasedamagegiven` innate (bloodline-source, so it stacks and resists Clear like the minions' entries). Hazards (Seal Charge, Core Canister) are unchanged.

**Consequence disclosed before the decision:** minion-level IDG makes fixture players die in 1–3 rounds. All three bosses become far deadlier than measured at r3/r4 or in the 4369f404 package, and none of those measurements carries forward.

**Canonical destination:** `state/ghost_ship_hybrid_kit_proposal.md` (boss innate rows); the Sealwright combat draft for its profile.

---

## RUL-2026-10-12-005 — Restore the 12-Filament Crystal recipe; Crystal mirrors a live crystal for undecided fields

**Date:** 2026-10-12

**Domain:** Ghost Ship / Skyglass / Skyglass Crystal economy and record

**Status:** ACTIVE.

**Supersedes:** RUL-2026-10-11-006's `canBeCrafted:false` / recipe removal only. dauntless stated that removing the recipe was a mistake. Rarity LEGENDARY, `canBeTraded:true`, exactly one Consume10 with 2/2 timing, WEAPON-only, Katana exclusion and the 3% Reliquary drop are unchanged.

**Ruling:**
1. **Recipe restored:** `canBeCrafted:true`, with 12 Skyglass Filaments crafting one Crystal (`craftingRequirements` referencing the new Filament item by manifest ref). Filament drops are unchanged. Filament tradability stays undecided.
2. **Native consequence:** LEGENDARY items require Forgemaster crafting rank at the pinned engine, so the recipe is Forgemaster-only. Imbuing a LEGENDARY Crystal also requires Forgemaster. Rarity was not changed to widen access.
3. **Undecided fields mirror a live crystal:** the 14 non-ruling fields carried from the Flaming Sword template (cost, requiredLevel, action/pool costs, cooldown, durability, equips, imbue/stack/level fields, battle usage), plus craftingExperience, take the values of an existing live LEGENDARY (or nearest) weapon crystal. The values come from an operator-run read-only capture, keeping every RUL005/006/this-ruling decision.

**Canonical destination:** `state/ghost_ship_skyglass_reward_decisions.md`; companion `state/ghost_ship_skyglass_final_item_contract.json`.

---

## RUL-2026-10-12-006 — Close Consume overlap as native; presentation supplied by the director

**Date:** 2026-10-12

**Domain:** Ghost Ship / Skyglass items

**Status:** ACTIVE.

**Ruling:**
1. **Consume overlap closed:** native engine behavior is accepted with no restriction or correction. Recorded fact (4369f404, ACTIVE): at 2/2 the 3-round shared Consume cooldown outlasts the 2-round buff, so two Crystal-imbued weapons cannot overlap through separate casts. Same-action SELF dedupe is unchanged.
2. **Presentation and art:** dauntless will supply the final description, battle description, image and effect animation/SFX for both Skyglass Katana and Skyglass Crystal. Fable slots them in and validates. No text or art is drafted on the director's behalf.

**Canonical destination:** `state/ghost_ship_skyglass_reward_decisions.md`.

---

## RUL-2026-10-12-007 — Accept source-default damage settings for offline evidence; live calibration by tester

**Date:** 2026-10-12

**Domain:** Ghost Ship / Skyglass / test fidelity

**Status:** ACTIVE.

**Context:** the live damage-formula config cannot be captured through Forge 0.5.0. `persist:"full"` is limited to audited content-record reads, and summary mode stores no body (push/88 withdrawn; `archive/spent-manifests/push-2026-10-12/README.md`). No public procedure exposes the deployed engine version.

**Ruling:** dauntless accepted the limitation. Offline harnesses keep using engine source-default damage settings at the pinned upstream engine, with that boundary disclosed. Final calibration happens in-game: a tester plays the Ghost Ship quests while they are still hidden, after the manifest is applied and before any publication. No Forge allowlist change is requested.

**Canonical destination:** this ruling; the full-manifest roadmap's production gates.

---

## RUL-2026-10-12-008 — Release-manifest record and packaging decisions

**Date:** 2026-10-12

**Domain:** Ghost Ship / Skyglass release manifest

**Status:** ACTIVE.

**Ruling:**
1. **Skyglass Filament:** `itemType:"MATERIAL"`, `rarity:"RARE"`, tradable. It feeds the 12-Filament Crystal recipe (RUL-2026-10-12-005).
2. **Skyglass Reliquary:** LEGENDARY consumable loot chest, **not tradable**. Its loot table is unchanged from the reward decisions.
3. **Presentation text:** the director supplies description and battle description for all five items, Katana, Crystal, Reliquary, Filament and Skyglass Serum. Fable slots them in and validates; no item text is drafted on the director's behalf.
4. **Prose:** the drafted quest retheme, objective, dialogue/choice and jutsu conversion text is accepted as final.
5. **Sealwright record:** a new AI that copies the regular Captain's profile fields (level, rank, stat/pool multipliers, regeneration and similar), with the accepted Sealwright kit/rules and +375% innate IDG (RUL-2026-10-12-004).
6. **Packaging:** one combined Forge manifest for the whole release. Art is the last input: the director provides a zip of all finalized art assets, and the manifest is finished around it.

**Canonical destination:** `state/ghost_ship_skyglass_reward_decisions.md` (items 1–3); `docs/design/GHOST_SHIP_SKYGLASS_FULL_MANIFEST_ROADMAP.md` (items 4–6).

---

## RUL-2026-10-12-009 — Normalize remapped AI distance gates to range+1

**Date:** 2026-10-12

**Domain:** Ghost Ship / Skyglass / AI rules

**Status:** ACTIVE.

**Amends:** RUL-2026-10-12-003 ("conditions unchanged") for distance gates only.

**Context:** after the remap, 14 captured `distance_lower_than` gates on pool-jutsu rules sit below the new jutsu's range+1. Law 40's text calls such gates safe, but Forge 0.5.0 enforces exact range+1 and refuses the manifest. Affected rules:
- Oathkeeper Quick Strike 2→4.
- Arsenal Keeper Numbing Shot 3→6 and Twin Shot 5→6.
- Sentinel Twin Shot 2/3/5→6.
- Core Horror Twin Shot 2/5→6.
- First Blade Rapid Fire 2→6, Ion Lance 3→6 and Numbing Shot 4→6.
- Crowned Captain Unraveling Strike 3→4.
- Deck Warden Rapid Fire 4→6.
- Wayfinder Lunging Strike 4→5.

**Ruling:** dauntless chose Option A. Each of these gates is set to range+1. Those attacks fire from farther away. Where one jutsu had several range-banded rules, the bands collapse and the first matching rule wins. These gate values were not measured offline (RUL-007 tester calibration applies). Option B, loosening Forge's check, was declined.

**Canonical destination:** `state/ghost_ship_hybrid_kit_proposal.md`; implemented by `push/90_ghost_ship_skyglass_release.gen.py --gate-policy law40` (default; `--final` requires it).

---

## RUL-2026-10-12-010 — Leave Counter Stance and Battle Trance unedited

**Date:** 2026-10-12

**Domain:** Ghost Ship / Skyglass / retained legacy jutsu

**Status:** ACTIVE.

**Amends:** RUL-2026-10-11-002 and the conversion packet's text for two of the eleven retained jutsu. The text of the other nine is accepted as final (RUL-2026-10-12-008) and unchanged.

**Evidence:** the AI census push/81–84 (2026-10-12, 535/535 reads; `state/ghost_ship_legacy_jutsu_consumer_audit.json`). 22 AIs outside Ghost Ship equip these two jutsu: 18 hold Counter Stance `T3glZGcSd-jS8G-NB43GR` and 4 hold Battle Trance `MG9ZujAV8lK7--YxThVbQ`. No outside AI holds any of the other nine. Editing an equipped jutsu severs its combat link (law 18/60), and the Skyglass text would also show in those AIs' fights.

**Ruling:** dauntless chose Option B.
- Counter Stance and Battle Trance keep their current live names, descriptions and battle descriptions. They are not renamed to "Rebounding Form" and "Remembered Form", and push/90 neither edits nor unequips them.
- They stay in the Ghost Ship kits and rules unchanged, including Crowned's support Reflect rule (same id).
- Re-equipping the 22 outside AIs (Option A) was declined, and so was cloning the two jutsu for Ghost Ship (Option C).

**Canonical destination:** `state/ghost_ship_legacy_jutsu_edit_scope.json`, read by `push/90_ghost_ship_skyglass_release.gen.py` and `harness/ghost_ship_legacy_baseline/consumer_audit.py`. The conversion packet JSON is unchanged because the frozen harnesses pin it.

---

## RUL-2026-10-12-011 — Accept the residual consumer risk from unknown live AIs

**Date:** 2026-10-12

**Domain:** Ghost Ship / Skyglass / retained legacy jutsu edits (law 18/60)

**Status:** ACTIVE.

**Evidence:**
- The census push/81–84 read all 535 repository-known AI ids (535/535 ok, persisted): 506 live non-ELDER and 29 deleted.
- push/91 (`tnr_results_1791772372237.json`, after the census) counted **522** live non-ELDER AIs.
- So **16 live AIs** have ids the repository does not know and were not read. Forge keeps only the count of `profile.getAllAiNames`.
- Among the 506 read, no AI outside Ghost Ship holds any of the nine jutsu push/90 edits. Counter Stance and Battle Trance are not edited (RUL-2026-10-12-010).

**Ruling:** dauntless accepts the residual risk for all 16 unread AIs. If any of them equips one of the nine edited jutsu, push/90's edit severs that AI's combat link to it (law 18/60) and shows the Skyglass text in its fights. push/92 (7 candidate reads) is no longer required.

**Implementation:** `harness/ghost_ship_legacy_baseline/consumer_audit.py --accept-residual RUL-2026-10-12-011` gives verdict `ACCEPTED_RESIDUAL` only when:
- every census id was read without error;
- the count shortfall is the only gap;
- no known outside AI holds an edited jutsu.

A known outside holder still yields CONSUMERS. push/90 `--final` accepts `ACCEPTED_RESIDUAL` only under this ruling id.

**Canonical destination:** `state/ghost_ship_legacy_jutsu_consumer_audit.json`.

---

## RUL-2026-10-12-012 — Ten Ghost Ship AIs enter combat at the JONIN caps

**Date:** 2026-10-12

**Domain:** Ghost Ship / Skyglass / AI combat stats

**Status:** ACTIVE. This is the director's stat-requirement amendment, issued alongside the four independent-review corrections of `5eb75123`.

**Ruling:** against capped opponents, these must enter combat fully capped, with effective offence and defence 1,300,000 and strength, intelligence, willpower and speed 400,000 (they must reach the caps, not merely stay below them):
- Deck Warden, Core Horror, Oathkeeper, Wayfinder, Arsenal Keeper, Sentinel and First Blade;
- The Captain, Crowned Captain and Sealwright.

All ten are level-100 JONIN profiles with equal-stat distributions; `statsMultiplier: 5` reaches the caps. Stored stats may exceed the caps.

Sealwright is one full create: all six combat fields at 1,391,300 with `statsMultiplier: 5`. Its masteries, pools and regeneration equal the regular Captain's. Levels, ranks, pools, regeneration, masteries, kits, innate effects, rules, equipment, rewards and quest scaling are preserved.

**Excluded hazards:** Seal Charge keeps `statsMultiplier: 10` and Core Canister keeps 20. The earlier suggestion to raise Seal Charge to 13 is withdrawn. Their other release changes stay in scope.

**Review corrections applied with it** (independent review of `5eb75123`):
1. The obsolete item requirement columns are not sent.
2. Boss effects are canonical, equal to the server's parse.
3. `preferredStat` is not sent on the Sealwright create.
4. The incorrect two-stage Sealwright scaling is replaced by the single full create (push/93 retired). This depends on Forge 0.5.2 accepting post-0056 AI columns on a create.

**Verification:** `harness/ghost_ship_final` r3, gate STATS, executes the pinned server save path and battle scaling and clamping for every AI push/90 writes.

**Canonical destination:** `push/90_ghost_ship_skyglass_release.gen.py` (`CAPPED_AIS`, `STATS_MULTIPLIER`, `HAZARDS`) and `state/ghost_ship_hybrid_kit_proposal.md`.

---

## RUL-2026-10-12-013 — Release-specific validate.py exception for push/90

**Date:** 2026-10-12

**Domain:** Ghost Ship / Skyglass release; D-validate-always (`docs/DOCTRINE.md`)

**Status:** ACTIVE, release-specific.

**Context:** the independent re-review of `be15d7f4` (GS-R5) closed GS-R1–R4 and passed the stat requirement. It held release on the canonical gate:
- `cd skills/building-tnr-content/data && python3 ../scripts/validate.py ../../../push/90_ghost_ship_skyglass_release.json` exits 1, with 56 errors and 25 warnings.
- Every diagnostic is either a generated contract lagging the pinned engine (45c/45d at `bdec2883`), a validator rule the pinned server no longer enforces, or director-approved content.

The source gates prove the flagged payloads are what the server accepts: ItemValidator CONTRACT, the STATS effects fixed point, Forge `check_manifest` 0, and the reviewer's source-normalised replay.

**Ruling:** dauntless approved a release-specific exception in place of contract adoption first. It applies **only** to push/90 at SHA-256 `6b72054282be6a904f409333afcdf6b013e8d0c4654977d863d208d64804b0c7`, and only to the exact 81 diagnostics enumerated in `state/ghost_ship_skyglass_release_validate_exception.json`, in nine evidence-backed classes:

| Class | Errors | Warnings |
| --- | ---: | ---: |
| Stale effect fields | 42 | |
| `statTypes` `None` enum | 2 | |
| Consume companion rule | 1 | |
| IDG power cap | 6 | |
| `preferredStat` L05 | 1 | |
| Approved shared menu targets | 4 | |
| Law-60 build order | | 9 |
| Stale farm nullability | | 8 |
| Captured self-target gates | | 8 |

**Enforcement:** `python3 push/90_ghost_ship_skyglass_release.validate_exception.py` runs validate.py exactly as the doctrine prescribes. It refuses any unclassified line and passes only when the manifest hash, the validator and contract hashes, and the exact diagnostic multiset all equal the ledger. Any change voids the exception and needs a new ruling.

The doctrine is unchanged and this is not a precedent. The correct payloads stay: stat values, canonical effects, and no `preferredStat`.

**Follow-up (separate Lane A task):** bring `validate.py` and the generated contracts to 585534d7 through `schema_extract.py` and its adoption gate, with tests for the post-0056 create and the current item/effect contracts.

**Canonical destination:** `state/ghost_ship_skyglass_release_validate_exception.json` (ledger) and this ruling.

---

## RUL-2026-10-12-014 — Sentinel renamed Guardian; push/93 repair and its validate.py exception

**Date:** 2026-10-12

**Domain:** Ghost Ship / Skyglass release; AI `3V_gdHYaclMB1gTyOPAbV`; D-validate-always (`docs/DOCTRINE.md`)

**Status:** ACTIVE. The exception is manifest-specific.

**Context:** the operator ran push/90 (results `harvests/inbox/tnr_results_1791779642866.json`). 49 of 50 records completed. Item 29 failed with `Duplicate entry 'Sentinel' for key 'UserData.UserData_username_key'`: another live AI owns that name, probably one of the 16 unread AIs under RUL-2026-10-12-011. `updateAi` syncs the kit before the userData update, so the new kit landed. The name ("Ghostly Guardian"), statsMultiplier 3, avatar and behaviour rules did not change.

**Ruling:** dauntless decided:
- The AI's name is **Guardian**.
- The quest text follows it: the four objective lines per quest that name the boss (`d_guardian`, `b_guardian`, `r_dig`, `d_claim_A`) say "Guardian" instead of "Sentinel".
- push/93 (`push/93_ghost_ship_guardian_repair.gen.py`) re-sends:
  - push/90 item 29 with only the name changed and the uploaded avatar URL resolved;
  - both live quests with only those 8 lines changed.
- push/90 and its design state (`state/ghost_ship_retheme_patch.json` aiRenames/objectiveText) stay as spent release history. This ruling and the push/93 generator own the rename.

**Validator exception:** dauntless extended the RUL-2026-10-12-013 mechanism to push/93 at SHA-256 `840a80fcae45cc99e4b3f2a84861a366113f53b876eb3532e98a0a9b3c6e2753`, and only to the exact 7 diagnostics in `state/ghost_ship_guardian_repair_validate_exception.json`:

| Class | Errors | Warnings |
| --- | ---: | ---: |
| Approved shared menu targets (already live) | 4 | |
| Captured self-target gate | | 1 |
| Stale-snapshot scene character (`b_K8qdNI651fTsRn9tfkk`, created by push/90) | | 2 |

**Enforcement:** `python3 push/93_ghost_ship_guardian_repair.validate_exception.py`, as for push/90. Any change voids the exception. The doctrine is unchanged and this is not a precedent.

---

## RUL-2026-10-12-015 — "Guardian" also taken; name is Skyglass Sentinel; push/94 repair

**Date:** 2026-10-12

**Domain:** Ghost Ship / Skyglass release; AI `3V_gdHYaclMB1gTyOPAbV`; D-validate-always (`docs/DOCTRINE.md`)

**Status:** ACTIVE; supersedes the name in RUL-2026-10-12-014. The exception is manifest-specific.

**Context:** the operator ran push/93 (results `harvests/inbox/tnr_results_1791780626532.json`). The AI rename failed with `Duplicate entry 'Guardian' for key 'UserData.UserData_username_key'`, so the AI is still "Ghostly Guardian" at multiplier 3, with the new kit. Both quest edits landed, so the 8 boss lines said "Guardian".

**Ruling:** dauntless named the AI **Skyglass Sentinel**. push/94 (`push/94_ghost_ship_skyglass_sentinel_repair.gen.py`) re-sends:
- push/90 item 29 with only that name and the resolved avatar URL;
- both quests exactly as push/90 shipped them. This restores the original "the Sentinel" lines, which fit the new name. The generator proves the live quests differ from push/90 only at those 8 lines.

The `state/ghost_ship_retheme_patch.json` objective text is therefore live again, and only the AI's username departs from it (`aiRenames` says "Sentinel").

**Validator exception:** the RUL-2026-10-12-014 terms apply to push/94 at SHA-256 `a31a588488c48f99c488149bb6b4b5264f0dd43ddd2995b5b242a5a1261b1988`: the same 7 diagnostics in the same 3 classes, ledger `state/ghost_ship_skyglass_sentinel_repair_validate_exception.json`, gate `python3 push/94_ghost_ship_skyglass_sentinel_repair.validate_exception.py`.

---

## RUL-2026-10-14-001 — Isolated art-generation sessions and opaque jutsu-icon backgrounds

**Date:** 2026-10-14  
**Domain:** TNR art production / Blue Blade Eyes (BBE) jutsu icons  
**Status:** ACTIVE — approved operating method and visual presentation decision; separate tool-contract correction pending.  
**Supersedes:** no prior visual acceptance; narrows the generic transparent-ICON presumption **for jutsu icon presentation only**, without editing or superseding the validator's actual contract.

**Ruling:** dauntless approved the **Art Studio + Isolated Generation** production model. Keep one persistent workspace for art direction, silhouette registry, image-reference selection, prompt handoffs, cross-icon comparison, processing, QC and packaging. Use a **fresh generation conversation for each individual image/jutsu**, pass only one or two selected individual art references, generate one candidate at a time, and close after acceptance or a clear failure. Reference images establish *rendering and material*, not the new target's subject or composition. Accepted raw art is locked; processing must not replace or reimagine it.

**Visual presentation:** newly produced **jutsu icons have designed backgrounds**; transparency is **not required**. This choice does not affect other asset types and does not authorize retroactive changes to existing game content. BBE's approved jutsu family uses pale translucent sapphire ice, sharp crystalline facets, frosted chakra, strong technique-specific silhouettes, and no mandatory circular sigils. Blue Crimson, Sapphire Command, Ice Shackles and Icebound Might have **director-approved raw visual candidates** only; see the exact source-evidence register.

**BBE-specific delivery cap:** all BBE jutsu-icon exports must be **under 80,000 bytes**, in addition to the currently applicable square/format/size rules.

**Unresolved mechanical conflict:** the current shared **ICON** target in skills/producing-tnr-art/data/25x_DATA_art_spec.json has chroma_key=lime, and the current artpreflight.py rejects opaque RGB icons for missing alpha. The user-approved opaque-background look does **not** automatically make that preflight green. Until an independently reviewed jutsu-specific spec/preflight path (normally Fable's implementation) or an approved evidence-backed exception exists, record this mismatch explicitly and do not claim mechanical upload readiness or zero-error preflight. Do not fabricate alpha or weaken other asset-class checks.

**Canonical destinations:** docs/workflows/ISOLATED_ART_GENERATION.md (operating protocol); docs/design/blue_blade_eyes/JUTSU_ICON_REGISTER.md (collection identity/approval state); docs/design/blue_blade_eyes/SOURCE_EVIDENCE.json (hashes of conversation source files). Existing skills/producing-tnr-art/ and 25x_DATA_art_spec.json retain technical authority; docs/00_INDEX.md retains routing and precedence.

**Boundary:** no live-game request, upload, edit or publication is authorized by this ruling. The user controls all live-game actions. Separate Bloodright tier-emblem artwork is unaffected.

---

## RUL-2026-10-17-001 — Accept the Forge Bloodright bundle budgets

**Date:** 2026-10-17

**Domain:** Forge / bundle size budget

**Status:** ACTIVE

**Supersedes:** none

**Ruling:** Accept the Forge bundle ceiling of **400,000 raw / 91,000 gzip bytes** for the Bloodright collection/icon importer (PR #33), together with the earlier Bloodright importer increase from 354,000/78,000 to 386,000/88,000 (PRs #29/#30).

**Evidence:** "Merge it. Budgets are accepted. Go ahead and integrate." (after independent review of PR #33 measured 389,034 raw / 87,864 gzip and the D1/D2 follow-up measured 389,081 / 87,883).

**Rationale:** The user explicitly accepted both pending budget increases. This settles the bundle ceiling only; it does not approve Bloodright content, icons, folder visibility or live execution.

**Canonical destination:** `forge/tools/check_bundle_budget.mjs` (`BUDGET`).

---

## RUL-2026-10-17-002 — Bloodright category icons may replace Hungry Pulse's live image

**Date:** 2026-10-17

**Domain:** Bloodright / Blood-Enchanted Eyes collection import / icons

**Status:** ACTIVE

**Supersedes:** none. Clarifies the scope of RUL-2026-10-08-002, whose "retains Hungry Pulse's existing values" covers its Silver price and rounds, not its image.

**Ruling:** When the BEE collection is imported with category icons, the Foundation icon **replaces Hungry Pulse's (`p2_t1`, `HWq7986PPhl5emkAM3L4a`) existing live image**, like every other Foundation node. No per-node `image` override is needed to protect it. Single-tree packages without icons still keep existing images.

**Evidence:** "Hungry Pulse replacement is fine." (in reply to the PR #33 independent review, which flagged the replacement as conflicting with RUL-2026-10-08-002.)

**Deferred, not decided here:** the 44 remaining legacy trees need a rebalance before conversion to the five-point format, and their values are currently unsettled. Do not convert, price or stage them until the user settles those values. Silver 20 / 99 rounds stays BEE-only.

**Still open:** the actual icon bytes/URLs and immutable `imagePack`, and the `black_bg` art-direction question. The collection template remains BLOCKED until they are supplied.

**Rationale:** The user accepted consistent tier iconography over preserving Hungry Pulse's older image. This settles the replacement question only; it does not approve icon art, release, folder visibility or live execution.

**Canonical destination:** `forge/bloodright/README.md` (category-icon behaviour) and `forge/bloodright/collection.template.json`, which already applies the Foundation icon to `p2_t1`. No code change is required.

---

## RUL-2026-10-17-003 — Import the naming-pass Bloodright trees with placeholder values

**Date:** 2026-10-17

**Domain:** Bloodright / naming pass / collection import

**Status:** ACTIVE

**Supersedes:** the "Deferred" clause of RUL-2026-10-17-002 (remaining trees waiting on settled values), for the 25 bloodlines in the naming-pass CSV only; the other 19 stay deferred. The BEE pilot names and bonuses in `docs/design/bloodright/examples/blood_enchanted_eyes_structural.json` are replaced for import by the naming-pass values. RUL-2026-10-08-002's 20 Silver / 99 rounds is unchanged and now also applies, as a placeholder, to the other trees.

**Ruling:** Move forward with the Bloodright project: import the trees from the naming-pass document into the game with their names, icons and placeholder stats.

- **Source:** `docs/design/bloodright/naming_pass/review.csv` (25 bloodlines x 12 nodes; names plus bonuses). Its bonus values are **placeholders** pending a later rebalance, not approved balance.
- **Scope:** the 25 bloodlines in the CSV. The other 19 planned bloodlines are not in the document and are not covered.
- **BEE:** uses the CSV names and bonuses like every other tree. Hungry Pulse keeps its name and binding; its image is replaced per RUL-2026-10-17-002.
- **Silver and rounds:** every node gets **20 Seichi Silver** and **99 rounds** as placeholders.
- **Icons:** the user supplies the icon files.
- **Newer potency tags:** for the 41 nodes (11 bloodlines) that use pierce, absorb, poison, drain, consume or vamp, verify the game source and extend the importer rather than swapping tags. Source check: these tags were added to `PotencyTagTypes` upstream at TheNinjaRPG `133e2c7` (2026-10-08) and are applied generically by `resolvePotencyTags` at `94f9d84`. Whether the live game runs that code is unverified.

**Evidence:** "I found a document from the naming pass of the skill tree. The names of all the different skills are provided, and the values contained can be used as placeholders. We can move forward with the Bloodright project. Objective, import all trees into game with their names, icons and placeholder stats." Then, answering the open questions: icons "I'll supply icon files"; tags "Verify, then extend"; BEE "Use the CSV"; Silver/rounds "20 Silver / 99 rounds".

**Still open:** Cosmic Ascendant has no qualifying element in the game's element list, so its design cannot compile. Shiroi Youso's legacy design lists Fire + Lightning marked for director review; it is held out of the packages until the user confirms its elements. Both were first excluded; RUL-2026-10-17-004 brings them back with a placeholder. Icon art, folder visibility and publishing are not approved by this ruling.

**Rationale:** Placeholder values let the full structure, names and icons go in hidden now, so balance can be tuned later by editing the hidden records instead of blocking the import.

**Canonical destination:** `docs/design/bloodright/structural/*.json` (generated by `scripts/bloodright_from_naming.py`) and the packages `forge/bloodright/naming_pass_collection_{a,b}.json` (generated by `scripts/bloodright_collection_package.py`). The game contract stays owned by `forge/src/bloodright/contract.json`.

**Boundary:** no live-game request or write is authorized by this ruling. The user runs the import through Forge.

---

## RUL-2026-10-17-004 — Cosmic Ascendant and Shiroi Youso import without an element for now

**Date:** 2026-10-17

**Domain:** Bloodright / naming-pass collection import

**Status:** ACTIVE

**Supersedes:** the Cosmic Ascendant and Shiroi Youso exclusions in RUL-2026-10-17-003's "Still open".

**Ruling:** Build both trees without an element for now; their real classification will be resolved later. Implemented as the game element `None` in `qualifying_elements`, so the skills import with all 25 trees.

**Evidence:** "CA and SY we'll just build without an element for now, that will be resolved later. Go ahead."

**Consequence (source-verified, TheNinjaRPG `94f9d84`, `app/src/libs/combat/potency.ts` `resolvePotencyTags`):** `None` makes the bonuses apply only to jutsu tags without an element, so in practice these two trees do little until their elements are set. The alternative, an empty element list, would apply their bonuses to every jutsu of the matching tag regardless of element; that was not chosen because it would make these the strongest trees rather than neutral placeholders. Effect descriptions read "... on None jutsu ..." until resolved.

**Canonical destination:** `scripts/bloodright_from_naming.py` (`NO_ELEMENT_PLACEHOLDER`) and the generated designs `docs/design/bloodright/structural/{cosmic_ascendant,shiroi_youso}.json`.

---

## RUL-2026-10-17-020 — ZIP-first Bloodline Jutsu Art Studio and faster session/processing workflow

**Date:** 2026-10-17  
**Domain:** individual bloodline jutsu.icon artwork production / session startup speed / art processing  
**Status:** ACTIVE — director authorized consolidation and optimization; no tool implementation, live-game operation or new artwork acceptance implied.

**Ruling:** The director instructed ChatGPT to consolidate the lessons from **Blue Blade Eyes (BBE), Blood-Enchanted Eyes (BEE) and Vaporia** into a **repeatable Bloodline Jutsu Icon Art Studio**, initialized with **one concise prompt plus one source-art ZIP**. Optimize repeated start-up and processing latency, reported as 8–10-minute Bloodright turns, without replacing checks with guesses: batch live repository/authority reads where possible, inspect and hash the ZIP once, derive exact jutsu name/ID/N mapping, establish the family palette/material and an **N-jutsu technique-first silhouette ledger together**. New jutsu icons are **individually designed per move**, prioritizing distinctive thumbnail-readable shapes and appropriate supernatural chakra rendering, with actors only when genuinely necessary. They do **not** reuse Bloodright's three fixed universal tier emblems.

**Session and finalization rule:** Preserve the existing **one clean isolated generation session per jutsu** under RUL-2026-10-14-001; the persistent Studio coordinates direction, briefs, byte-accurate intake, approvals, and final processing. Generator input is only one or two *individual actual image references*, not the entire ZIP or a contact sheet. Process approved raw assets **in one family-level export/preflight/QC pass where available**, then assemble the final count-adaptive family showcase **deterministically from the actual saved WebPs** (not with image generation). Whole-family visual acceptance is a separate director gate from N individual icon acceptances; Vaporia's historical 5/5 raw approvals did **not** prove final showcase approval.

**Art/technical boundaries:** Opaque designed backgrounds are permitted for **jutsu.image**, which already has a dedicated current `JUTSU_ICON` target with alpha optional. Do not fabricate alpha, force rarity-frame accommodation, or carry legacy generic `ICON` blockers forward as current jutsu requirements. Use current spec-driven dimensions/format and record real `artpreflight.py --type JUTSU_ICON` results. **BBE's under-80,000-byte cap is BBE-specific**, and its palette quantization was a recorded quality tradeoff, not a default that can silently flatten other artwork. Director-approved raw artwork must not be silently regenerated, recolored, or replaced. Image originals, processed exports, family acceptance, canonical preflight, immutable source pins and live upload/read-back are distinct gates.

**Canonical destination:** `docs/workflows/BLOODLINE_JUTSU_ICON_STUDIO.md`, `docs/workflows/JUTSU_ICON_SHOWCASE.md`, `docs/design/jutsu_icon_studio/START_PROMPT.md`, and `GENERATION_AND_CLOSEOUT_TEMPLATES.md`, all under the existing `docs/workflows/ISOLATED_ART_GENERATION.md` and current art-skill/spec authority. `state/prompt_jutsu_icon_studio_fast_tooling_20261017.md` describes potential Fable-owned offline batch tooling; no unimplemented script may be presented as operational.

**Priority and production boundary:** Bloodright structural import remains a **separate higher-priority workstream** under user direction; this standardization does not cause jutsu icon uploads. Any Fable tooling/code follows Lane A independent review. No agent live-game requests/writes/uploads, credentials or publication authorized by this ruling.

**Operative precedence / integration note (2026-10-19):** `docs/workflows/ISOLATED_ART_GENERATION.md` (P0 A–F, RUL-2026-10-19-003) governs exact per-target locks, default anatomy restrictions, visual fail-fast and deterministic-gallery acceptance; the ZIP-first workflow specialises intake and coordination beneath it. The current CLI is `skills/producing-tnr-art/scripts/jutsu_studio.py` (P1 Option B, PR #66), not the 2026-10-17 queued tooling proposal. The historical `state/prompt_jutsu_icon_studio_fast_tooling_20261017.md` is retained at `chatgpt/bloodline-jutsu-studio-zip-first-20261017@d04a87c05999c7037af8667db2b2b79324a53d3c` as **SUPERSEDED**, not added to current main. Gallery layout, accepted-gallery evidence and archive names follow RUL-2026-10-19-005 D5–D9.

---

## RUL-2026-10-17-021 — BBE and BEE jutsu-icon finals are the approved JUTSU_ICON style library

**Date:** 2026-10-17 (recorded on `claude/bloodline-jutsu-icon-studio-3nmvc2@6bc0af4e`; integrated on main by the P1 tooling change under RUL-2026-10-19-005 D3)

**Domain:** bloodline jutsu-icon art / style references / Art Studio tooling

**Status:** ACTIVE

**Ruling:** dauntless supplied the final BBE and BEE jutsu-icon export ZIPs and directed: "Save them as the approved style library. And optimize the workflow so I *can* begin a session with a prompt and an art pack zip." The 16 WebPs are pinned byte-for-byte as the `JUTSU_ICON` style/material exemplar library.

**Scope and limits:** exemplars are STYLE/MATERIAL ONLY; each one's silhouette stays reserved by its family. The PRIMARY/SUPPORTING order in `style_refs.json` is a reversible selection default set at intake (based on a 32px readability check), not an art-direction ruling. BEE's `icon_bee_sanguine_plague_v3.webp` is not the version in the BEE closeout (which approved v2); it is pinned on this instruction, and the repository holds no individual raw approval or raw original for it, so selection output flags it `PROVENANCE_PARTIAL`. Vaporia's finals are not pinned. Nothing here uploads art, changes a jutsu record or touches the live game.

**Canonical destination:** `art/style_refs/jutsu_icons/` + `art/style_refs/jutsu_icons/INTAKE_20261017.json` (bytes and provenance); `skills/producing-tnr-art/data/style_refs.json` and `scripts/style_refs.py` (index and selection).

**Supersedes:** none. Companion RUL-2026-10-17-020 and its ZIP-first documents are now brought into the separate ChatGPT-owned D4 documentation PR under RUL-2026-10-19-005; this RUL-021 continues to govern the BBE/BEE style-exemplar pinning, not their production approvals.

---

## RUL-2026-10-18-001 — Bloodright tree standard: Taiyo Kami exemplar and clean round totals

**Date:** 2026-10-18 (decisions made in the user's Codex balance sessions, 2026-10-17/18)

**Domain:** Bloodright / tree design and balance

**Status:** ACTIVE

**Supersedes:** none. It refines the placeholder-value basis of RUL-2026-10-17-003; the values imported under that ruling already equal the round-total proposal.

**Ruling:** Bloodright trees follow the accepted **Taiyo Kami** exemplar:

- **Structure:** four independent Foundation → Hidden Art → Advanced Art paths; 1 BP per node, 5 BP total. The intended full build is one complete path plus another path's Foundation and Hidden Art (3+2).
- **Prerequisites:** one tag per Foundation and per Hidden Art, ascending along the path.
- **Capstones:** distinctive Advanced Arts with one or two related effects.
- **Percentage tags:** clean steps of +2% / +3% / +5%. A finished build must total exactly +5% or +10% of each percentage tag, so players see round numbers.
- **Damage:** clean amounts. The original ladder was +0.4 / +0.8 / +1.2. +0.2 is approved for lower tiers, and +0.6 is approved as an exception (Taiyo uses +0.2 → +0.6 → +0.8). Aggregate Damage stays within 5 across eligible jutsu rows. For reference, +0.8 equals two jutsu levels at +0.4 per level.
- **How to balance:** use tag selection, placement and capstone combinations, never odd amounts chosen by an optimizer to equalize scores. There are no fixed per-tier or per-build Weight targets; the earlier 4-Weight target was provisional and is dropped.
- **Exemplar:** Taiyo Kami's round-total version is the accepted exemplar. Path → Foundation / Hidden / Advanced:
  - Damage → +0.2 / +0.6 / +0.8 Damage +5% DDG
  - Afterburn → +2% / +3% / +0.8 Damage +5% DDT
  - DDT → +2% / +3% / +5% IDT +0.4 Damage
  - DDG → +2% / +3% / +5% DDG +5% Afterburn
- **Presentation:** for review (e.g. a Discord thread), present each tree as cumulative totals, prerequisites included. That means its four 3-BP completed Advanced Arts and its twelve 5-BP builds, labelled as total Bloodright bonuses.

**Evidence (user, in the Codex sessions):**
- "4 points was also provisional and it seems like you're throwing a lot of tags out there to try to make it work."
- "I kind of want to put damage at an even .8 here because that would translate to exactly 2 jutsu levels worth of scaling."
- "This tree looks done and usable as an exemplar."
- "I had wanted clean increments of +2/+3/+5 for tags and +.4/+.8/+1.2 for damage."
- "A lower tier damage of +.2 is approved."
- "The goal is for a finished build to have +5 or +10 of % tags, so their jutsu have a nice round number."
- "OK, looks good. Do the same for every other tree", in reply to the recommended +0.2 → +0.6 → +0.8 Taiyo rebalance with the +0.6 exception.
- "We can just present the 3 BP builds and then the 5 BP variations as finalized kit numbers in text format right?"

**Rationale:** Players read and compare clean, round totals. Balance should come from design choices, not decimal tuning.

**Canonical destination:** the generated designs in `docs/design/bloodright/structural/`. Evidence: `docs/design/bloodright/balance/round_total/` (Codex's `proposal_trees.json` and its README). Codex's `BALANCING_STANDARD.md` and scripts were not pushed to this repository.

---

## RUL-2026-10-18-002 — Round-total values are the current Bloodright placeholders; 21 trees remain drafts

**Date:** 2026-10-18

**Domain:** Bloodright / naming-pass collection import

**Status:** ACTIVE

**Supersedes:** none.

**Ruling:** Codex's round-total proposal for all 25 A/S trees (applied with "Do the same for every other tree") is the value set behind the naming-pass import. It matches the imported designs node for node. It remains a placeholder set for hidden import, not finished balance.

- **Pass Codex's normal and symmetric-pressure screens:** Taiyo Kami (accepted exemplar), Arashima, Heavenly Sonata and Teno Yuki.
- **Flagged drafts:** the other 21. They meet the structure, finished-percentage and cap rules, but keep a weaker secondary choice.
- **Constraint-limited:** six of those drafts cannot reach the 90% secondary-choice screen under the current rules, because their kits offer only four tag families: Hyouga Yui, Itojinsei, Shadow Weaver, Shinrai Ou, Shinseina Ki and Tenohira Musei. They need a kit or design-rule change.
- **BEE and BBE** keep their keystone placement rules. Their healing and coverage gaps remain open.
- **Further balance work** happens on the hidden records or in a later pass. It does not block the hidden import.

**Evidence:** "Do the same for every other tree" (user). Codex reported: "21 remain flagged drafts, not finalized balanced trees. Six cannot reach the 90% secondary-choice target within the current rules in this model."

**Canonical destination:** `docs/design/bloodright/balance/round_total/` (`PROVENANCE.md`, `proposal_trees.json`, `codex_review_README.md`).

**Boundary:** no live-game action is authorized. Publishing, final balance acceptance and the six constraint-limited kits remain user decisions.

---

## RUL-2026-10-18-003 — Set Bloodright kit jutsu classification so tree bonuses apply

**Date:** 2026-10-18

**Domain:** Bloodright / kit jutsu / live content

**Status:** ACTIVE

**Supersedes:** none. It corrects the stated consequence of RUL-2026-10-17-004.

**Ruling:** Set `elementClassification` on the Bloodright naming-pass bloodlines' kit jutsu to the bloodline's tree element, so their tree bonuses reach the kit. Balancing models the game after this edit, which is the same assumption Codex's round-total scores made.

- **Why:** engine-verified, 71 of the trees' 130 bonus tags (201 node bonuses) reach no kit jutsu today. After the edit, 2 do. Evidence: `docs/reviews/BLOODRIGHT_KIT_CLASSIFICATION.md`.
- **Scope:** 122 kit jutsu across the 23 single-element trees. Cosmic Ascendant and Shiroi Youso have no single element and are not edited.
- **Execution:** a staged live operation run by the user through Forge, because 46 AIs equip 38 of these jutsu (laws 18 and 60).
  1. Read-only capture, `push/109`–`110`.
  2. Unequip the affected AIs, after a one-AI stat-scaling probe.
  3. Convert the 122 jutsu, changing only `elementClassification`.
  4. Re-equip the AIs from the before-image, with read-back gates after each step.
- **Correction to RUL-2026-10-17-004:** the `None` placeholder does not make Cosmic Ascendant's and Shiroi Youso's bonuses "do little". `None` matches every element-less effect row on any jutsu the player casts, so it is broad. Their handling is pending a user decision.

**Evidence:** the user chose option 1 ("Set the classifications") from: (1) set the classifications, (2) balance only what works today, (3) ask the game developer to change matching.

**Canonical destination:** the live jutsu records, via the staged manifests. The analysis is in `docs/reviews/BLOODRIGHT_KIT_CLASSIFICATION.md`.

**Boundary:** agents make no live requests. The user runs every stage. Stat re-scaling found by the probe is a user decision.

---

## RUL-2026-10-18-004 — Keep Cosmic Ascendant and Shiroi Youso in the import with the `None` placeholder

**Date:** 2026-10-18

**Domain:** Bloodright / naming-pass collection import

**Status:** ACTIVE

**Supersedes:** the pending item in RUL-2026-10-18-003.

**Ruling:** Cosmic Ascendant and Shiroi Youso stay in the import packages with the `None` element placeholder, so both bloodlines have trees. Their real classification will be resolved later.

**Known consequence:** with `None`, their bonuses apply to every element-less effect row on any jutsu the player casts, so they are broad rather than neutral (RUL-2026-10-18-003). Their kit jutsu are not reclassified.

**Evidence:** "Leave CA and SY in for now so they at least have trees, we'll take it from there."

**Canonical destination:** `scripts/bloodright_from_naming.py` (`NO_ELEMENT_PLACEHOLDER`) and `forge/bloodright/naming_pass_collection_{a,b}.json`. No change is needed; both trees are already packaged.

---

## RUL-2026-10-18-005 — Restore the AIs' battle kits after the classification re-equip

**Date:** 2026-10-18

**Domain:** Bloodright / live AI kits

**Status:** ACTIVE

**Supersedes:** none. It corrects a side effect of the RUL-2026-10-18-003 execution.

**Ruling:** The AIs keep exactly the jutsu they used in battle before the classification edit. The 82 Bloodright kit jutsu that were stored as unequipped on 32 AIs, and came back equipped from the re-equip, are removed from those AIs' kits.

- **Why:** `profile.updateAi` always inserts a re-added jutsu with `equipped = true` (`profile.ts` `applyUserContentChanges` at 94f9d84), and battles load only equipped jutsu (`combat.ts` `initiateBattle`). Before push/112–115, 133 of the 46 AIs' 424 kit rows were unequipped, so those jutsu were never used. 82 of them were among the re-equipped kit jutsu and became active. `updateAi` cannot store `equipped = false`, so removing them is the only way to restore the old battle behaviour.
- **Execution:** `push/120`–`121`, generated by `push/120_bloodright_restore_unequipped.gen.py` from the before-image and the push/112–115 read-backs, with a full read-back of each AI.
- **Known consequence:** those 82 jutsu no longer appear in the AIs' kits. Re-adding one later makes it active in battle.

**Evidence:** the user chose "Restore old behaviour" from: keep them active; restore old behaviour; activate all of them.

**Canonical destination:** the live AI records, via push/120–121. The read-back comparison is `scripts/bloodright_classification_readback.py`.

---

## RUL-2026-10-18-006 — Rebalance the Bloodright trees with Claude's scorer, strict round totals

**Date:** 2026-10-18 (applied 2026-10-19)

**Domain:** Bloodright / tree balance

**Status:** SUPERSEDED by RUL-2026-10-19-001 (its values were replaced; its scorer and reasons stand)

**Supersedes:** the placeholder values of RUL-2026-10-18-002 for 24 trees. RUL-2026-10-18-001's structure and value rules stand unchanged.

**Ruling:** The Bloodright trees are rebalanced with Claude's scorer (`scripts/bloodright_balance/`) under the strict RUL-2026-10-18-001 rules: +2 / +3 / +5 percentage steps, clean Damage amounts, round finished totals and four distinct path roots. In addition:

- every completed path and every 5-BP build has its own bonus package;
- no effect sits on more than two capstones (Damage on up to three, as in Taiyo);
- each tree's average full build is pulled toward the Taiyo exemplar's strength.

- **Scorer fidelity:** an independent review found three mechanics that differed from 94f9d84 (damage modifiers multiply in turn with the system boost, system reduction and 10% floor; pierce skips the modifier pipeline; poison reads level-reduced costs). They were fixed and the search rerun before these values were written.
- **Pierce and Heal:** both bonuses are flat power. +5 Pierce adds 5 power to each pierce hit, which is Damage-like but outside the Damage budget. The trees step them +2 / +3 / +5 like the percentage effects, as Codex's trees did. This is open for a user ruling.
- **Why Claude's scorer:** Codex's scoring scripts were never pushed. Claude's scorer, rebuilt from the pinned game source, agrees with Codex on overall tree strength but not on path evenness; it rated Taiyo's paths uneven. The user chose it over waiting for Codex's tools, accepting that Taiyo and the other three passing trees change.
- **Result:** in 21 of 24 trees every finished path is within 15% of the strongest, and 17 of 24 trees sit within ±25% of the pre-rebalance Taiyo exemplar's strength (its average full build, 4.23 Weight; the search's anchor). Scores and every build: `docs/design/bloodright/balance/scorer_v1/REVIEW.md`.
- **Known limits:**
  - the add-on choice (another path's Foundation and Hidden Art) stays uneven on most trees, because the four root effects are not worth the same in each kit;
  - the kits set seven trees' strength outside ±25% of that anchor: Blue Blade Eyes (+170%), Shinseina Ki (+51%), Tenohira Musei (+41%), Bakuhatsu (+31%) and Blood-Enchanted Eyes (+27%) are stronger; Cosmic Ascendant (−43%) and Heavenly Sonata (−35%) are weaker;
  - Bakuhatsu, Hyouga Yui and Shinrai Ou keep one weak path.
  The +5/+5 root variant, which helps the add-on choice on 8 trees, was offered and declined.
- **Shiroi Youso:** unchanged. With the `None` placeholder only three effects reach its kit, too few for four distinct paths. It needs its element decided first (RUL-2026-10-18-004).
- **Names:** 112 nodes changed effects and keep their naming-pass names for now. They are listed for a naming review.

**Evidence:**
- "Use my scorer" (chosen over getting Codex's tools, or a rules-only pass).
- "Strict, tighten strength" (chosen over allowing +5/+5 starters, or showing both first).

**Canonical destination:** `docs/design/bloodright/balance/scorer_v1/trees.json`, applied by `scripts/bloodright_from_naming.py` into `docs/design/bloodright/structural/`. The scorer and search live in `scripts/bloodright_balance/`.

**Boundary:** no live-game action. The import packages stay blocked on icons, and import remains the user's step.

---

## RUL-2026-10-19-001 — Bloodright balance rules: round finished totals at today's power level

**Date:** 2026-10-19

**Domain:** Bloodright / tree design and balance

**Status:** ACTIVE (the user approved the rebalanced trees and drafted names by merging PR #53: "merge it", 2026-10-19)

**Supersedes:** RUL-2026-10-18-006's values. It amends RUL-2026-10-18-001's value rules as below; that ruling's structure (four paths, 1 BP per node, 3+2 builds, distinctive capstones) stands.

**Ruling:** Bloodright trees are balanced with Claude's scorer under these value rules:

- **Percentage effects:** every finished build totals a multiple of 5 for each effect, at most 20. That keeps capped jutsu values round, since kit rows read 30/35/40 at max jutsu level 25.
  - A path's Foundation and Hidden Art carry the same effect and step +2/+3, +4/+6 or +6/+9, so each path opens with +5, +10 or +15.
  - Capstones give +5 or +10.
- **Damage:** clean power steps of 0.2 as before, with Damage × eligible damage rows ≤ 5.
- **Pierce:** clean power steps like Damage (+0.2 to +1.6), sized to its value, with its own matching budget (Pierce × eligible pierce rows ≤ 5). It is no longer a +2/+3/+5 percentage step.
- **Power level:** trees are pulled toward today's Bloodright power: an average full build of 5.24 Weight. That is the median of a six-tree sample (Taiyo Kami, Aerathiel, Arashima, Vaporia, Oblivion Seal, Kyuko-sei) under these rules without a strength pull, not a full-roster median.
- **Round numbers apply to finished builds only.** Partial allocations (e.g. a lone Foundation, +2) can still show non-round values; making every allocation round is rule set C (every node +5/+10), which the user declined.
- **Distinct builds:** every finished path and 5-BP build stays distinct. No effect sits on more than two capstones (Damage up to three).

**Result (24 trees):**
- 21 are within ±15% of the power target.
- In 19, every finished path is within 15% of the strongest.
- The add-on choice improves on most trees but reaches 80% only on Vaporia, Teno Yuki and Oblivion Seal. Equalising it further needs every node at +5/+10 (rule set C), which doubles Bloodright power; the user declined that.
- Scores and every build: `docs/design/bloodright/balance/scorer_v1/REVIEW.md`.

**Flagged:**
- **Kyuko-sei** (+25%): just outside the power band.
- **Uneven paths:** Blue Blade Eyes (55%), Shinseina Ki (64%), Hyouga Yui (80%), Itojinsei (82%) and Kyuko-sei (84%) have a finished path below 85% of the strongest.
- **Arashima** (−54%): kit-limited. Its own shield soaks the hits damage reduction would cut, and its main hit is Pierce, so tree bonuses barely register. It is left as balanced as it can be and flagged for a later kit change.
- **Blue Blade Eyes** (+72%): kit-limited. +5% IDG alone is worth about 10 Weight there.
- **Shiroi Youso:** unchanged. Its element is still unresolved (RUL-2026-10-18-004).

**Names:** 124 nodes changed effects. Claude drafted their names at the user's request (116 new, 8 kept because they still fit), in `docs/design/bloodright/balance/scorer_v1/names.json`, each with a one-line rationale. They are unique across the roster and the kit jutsu names. Approved with the merge.

**Analysis:** the user asked for a full analysis of how to balance within the round-number constraint. Three rule sets were compared on the same scorer (jutsu level 25), first on six sample trees:
- A, strict +2/+3/+5;
- B, round finished totals;
- C, every node +5/+10.

C balanced add-ons best (about 80–90%) at about 2× today's power. B kept today's power with partial add-on balance.

**Evidence:**
- "The important part is not using weird decimals to balance weights."
- "I want all the trees to be a similar power level as well as their second path choices to be balanced."
- "Pierce values can be adjusted to reflect appropriate weights."
- Chose "B: round totals, today's power" over C and over keeping A.
- Chose "Leave it, flag it" for Arashima.

**Reproduce:** run `python3 scripts/bloodright_balance/search.py <slug> --round5 --target 5.24 --strength-weight 4 --out <dir>` once per tree (single pass, no per-tree selection between strength settings), then `python3 scripts/bloodright_balance/apply.py <dir>` and `python3 scripts/bloodright_from_naming.py`.

**Canonical destination:** the rules in `scripts/bloodright_balance/search.py` (`--round5`), the values in `docs/design/bloodright/balance/scorer_v1/trees.json`, applied into `docs/design/bloodright/structural/`.

**Boundary:** no live-game action. The import packages stay blocked on icons.

---

## RUL-2026-10-19-002 — Accept the Forge 0.7.2 bundle budget

**Date:** 2026-10-19

**Domain:** Forge / bundle size budget

**Status:** ACTIVE

**Supersedes:** RUL-2026-10-17-001 (gzip ceiling only; raw ceiling unchanged)

**Ruling:** Accept the Forge bundle ceiling of **400,000 raw / 95,000 gzip bytes** for the phone QA pass fixes (PR #56, Forge 0.7.2).

**Evidence:** "approve the budget" (after PR #56 measured 389,230 raw / 92,996 gzip against the 91,000 gzip ceiling; main measured 89,976 gzip).

**Rationale:** The user explicitly accepted the increase. This settles the bundle ceiling only.

**Canonical destination:** `forge/tools/check_bundle_budget.mjs` (`BUDGET`).

---

## RUL-2026-10-19-003 — Adopt P0 jutsu-icon accuracy and source-faithful showcase gates

**Date:** 2026-10-19

**Domain:** Art production / `jutsu.image` workflow

**Status:** ACTIVE — director-approved; canonical protocol change staged for integration.

**Supersedes:** None. Extends RUL-2026-10-14-001's isolated-art workflow; jutsu backgrounds, alpha policy, client/spec requirements and user-controlled live actions remain unchanged.

**Ruling:** Adopt Aerathiel retrospective P0 proposals A–F with the two review refinements: (A) immutable exact jutsu/bloodline identity and technique/silhouette/camera target lock; (B) composition and perspective before rendering, with a clean isolated restart after two wrong-subject/composition failures; (C) fail-fast family-distinctness checks of primary silhouette **and action** at 125/64/32 pixels; (D) default technique-first jutsu icons without anatomy, allowing narrowly director-approved target-specific exceptions only; (E) chakra structures integrated into the actual technique instead of unsupported magical ornaments or floating symbols; (F) deterministic, exact-source-asset family galleries only, never generative remakes of accepted tiles.

**Refinements:** Generator descriptions are triage hints, not proof: inspect the returned **pixels**, and do not claim hidden prompt access or control. Family distinctness is a contextual visual/art judgment on recognizable geometry and action, **not** an automatic color-similarity rejection; family members may share palette or elemental materials. A wrong-target result that auto-appears in the UI is rejected as a failed candidate, not put to the director for diagnosis.

**Evidence:** Director replied "Approved with the refinements" to the six-item P0 review and its two stated refinements on 2026-10-19. Retrospective source: `docs/design/aerathiel/JUTSU_ICON_WORKFLOW_RETROSPECTIVE_20261019.md` at `chatgpt/aerathiel-jutsu-art-studio-20261019@2994305e5cd4894953a14b7c1d8727ddfc00fdd3`.

**Canonical destination:** `docs/workflows/ISOLATED_ART_GENERATION.md` (jutsu-icon scoped amendment). Art spec/skill tooling remain in their existing canonical owners; any executable validation or batch-CLI additions are Fable-owned Lane A work subject to independent review.

**Boundary:** This accepts **P0 A–F only**, not retrospective P1 proposals or an unreviewed CLI. It does not grant acceptance of Aerathiel's still-pending deterministic gallery, a canonical artpreflight PASS, Git binary pinning, or any production upload/readback. No live-game actions are authorized.

---

## RUL-2026-10-19-004 — Move Hungry Pulse back to Blood-Enchanted Eyes; bind Ethereal Monarch's existing folder

**Date:** 2026-10-19

**Domain:** Bloodright import / push/123 (collection B)

**Status:** ACTIVE

**Supersedes:** none

**Ruling:** Hungry Pulse (`HWq7986PPhl5emkAM3L4a`), the Blood-Enchanted Eyes p2_t1 skill, was found on Aerathiel's bloodline (`1C34syOOEKp6k3UKweYT6`). No Forge job wrote to it, so it was moved by hand. The director chose to **move it back to Blood-Enchanted Eyes** in push/123. Collection B marks that binding `reassign`; Forge allows the move only for a named node, only for a hidden BLOODRIGHT skill, and only when no other skill requires it. Ethereal Monarch binds its existing folder `Z7_y_40drZY8k_ECDRLMa` (visible; the imported skills stay hidden) instead of creating a same-named second folder.

**Evidence:** Forge 0.7.7 preview of push/123: "Hungry Pulse: binding belongs to another bloodline or SKILL path (BLOODRIGHT, bloodline 1C34syOOEKp6k3UKweYT6)" and "folder "Ethereal Monarch" exists (Z7_y_40drZY8k_ECDRLMa, visible)". User answer: "Move it back to BEE".

**Canonical destination:** `scripts/bloodright_collection_package.py` (`BEE`, `EXISTING_FOLDERS`), regenerated into `forge/bloodright/naming_pass_collection_b.json` and `push/123_bloodright_collection_b.json`.

---

## RUL-2026-10-19-005 — Approve jutsu-icon P1 tooling scope (Option B) and decisions D1–D10

**Date:** 2026-10-19

**Domain:** Art production tooling / `jutsu.image` (Lane A)

**Status:** ACTIVE — director-approved; implementation by Fable, subject to independent review at an exact SHA.

**Supersedes:** none. Implements, and does not change, the P0 gates of RUL-2026-10-19-003 in `docs/workflows/ISOLATED_ART_GENERATION.md`.

**Ruling:** Adopt every recommendation in `docs/design/jutsu_icon_studio/P1_TOOLING_SCOPE_PROPOSAL_20261019.md` §8:

- **D1** Scope **Option B**: harden and integrate the prototype CLI and add P0 record support (target lock, attempt/failure log, compare sheet, anatomy exception record, rejection codes), `audit-gallery`, the K gate table, roster evidence levels, `doctor`, and export speedups. Option C items are out of scope.
- **D2** Port only the Fable code commit `6bc0af4e` onto a fresh Fable implementation branch from current main; the prototype branch stays frozen as evidence and is not merged.
- **D3** Pin the 16 BBE/BEE exemplar WebPs (RUL-2026-10-17-021), with `icon_bee_sanguine_plague_v3.webp` flagged `PROVENANCE_PARTIAL`.
- **D4** The ZIP-first studio/showcase workflow documents and RUL-2026-10-17-020 are landed by their owner (ChatGPT) as a separate PR; until then the P1 CLI cites only main authorities.
- **D5** Gallery layout for N ≥ 10: balanced rows of at most four, longer rows first (10 = 4+3+3, 11 = 4+4+3, 13 = 4+3+3+3). N ≤ 9 keeps the existing table.
- **D6** When canonical preflight is not PASS, the flat WebP ZIP is still built but named `*_webps_PREFLIGHT_NOT_RUN_*` (or `NON_CANONICAL` / `FAIL`), never `upload`.
- **D7** Gate vocabulary adopts the retrospective K names verbatim.
- **D8** Attempt log records `attempt_count`, `wrong_target_count`, `silhouette_conflict_count`, `art_style_drift_count`, `anatomy_rejection_count`, `approved_raw_after_attempt_n`; `generator_wait_ms` only where actually measured. The studio records attempts; tooling only validates and counts.
- **D9** A preflight is canonical only when the `artpreflight.py` and art-spec git blobs equal the pinned blobs of a named main commit; otherwise the verdict is `NON_CANONICAL`, never PASS.
- **D10** P1 tests use synthetic fixtures only; Aerathiel artefacts are neither consumed nor pinned.

**Evidence:** Director reply "All recommendations approved, proceed" to the P1 proposal (committed `d9252768` on `ccr-f0d2b974-k6121h`), 2026-10-19.

**Canonical destination:** `state/prompt_jutsu_icon_p1_tooling_20261019.md` (build contract); implementation in `skills/producing-tnr-art/scripts/jutsu_studio.py` and its selftest.

**Boundary:** Aerathiel gallery acceptance stays PENDING, canonical preflight NOT RUN, Git binary pinning PENDING and upload/readback NOT PERFORMED. No tool may claim to judge whether pixels depict the locked technique. No live-game actions are authorized.

## RUL-2026-10-19-006 — Build Forge suggest mode (option 1) and raise the bundle budget for it

**Date:** 2026-10-19

**Domain:** Forge / content review / bundle size budget

**Status:** ACTIVE

**Supersedes:** RUL-2026-10-19-002 (bundle ceiling only)

**Ruling:** Forge gains a suggest mode that sends edits of existing records to the game's content review desk instead of saving them (option 1 of `docs/design/FORGE_SUGGEST_MODE_SCOPE.md`). New content keeps the create-hidden path; Bloodright imports are not suggestible. The Forge bundle ceiling rises to **420,000 raw / 100,000 gzip bytes** for it (measured 407,434 / 97,814).

**Evidence:** User answer "1." to the scope's options, then "Yes, start on it. Size limit raise approved."

**Canonical destination:** `forge/src/review/contract.json`, `forge/src/runner/manifest.mjs` (`suggestPolicy`), `forge/src/runner/runner.mjs` (`_suggestItem`), `forge/tools/check_bundle_budget.mjs` (`BUDGET`).

## RUL-2026-10-19-007 — Suggest-mode rationales are specific to each record

**Date:** 2026-10-19

**Domain:** Forge suggest mode / manifest authoring

**Status:** ACTIVE

**Supersedes:** none

**Ruling:** Every item in a suggest-mode manifest carries its own `suggestion.rationale`: a short blurb telling the reviewer what is being changed on that record and why. A generic rationale shared by the whole manifest is a fallback, not the norm. Icon updates (the main planned use) say what the new art shows and why it replaces the old one.

**Evidence:** User, 2026-10-19: "I think for rationale we could try to give a more specific reason than just the generic reason. Just a short blurb for the reviewer to explain what they're reviewing and why".

**Canonical destination:** `docs/design/FORGE_SUGGEST_MODE_SCOPE.md` ("Implemented: option 1"). Forge already supports per-item rationales; no code change.

## RUL-2026-10-20-001 — Adopt the generated skill contracts at TheNinjaRPG@85cecae in one pass, under a reviewed-removal ledger

**Date:** 2026-10-20

**Domain:** Generated contracts (skill `data/` 45c/45d/45e/45f/45g) / adoption gate

**Status:** ACTIVE — Lane A; pending independent review of the frozen SHA

**Supersedes:** none. D-adopt-gate is unchanged in intent: nothing is adopted unless `schema_diff.py diff` exits 0.

**Ruling:** Fix the extractor's blind spots and adopt all five generated contracts in one pass, together with Forge's content contracts, at `85cecaebf4ada2e265a18a1405f63c9637443275` (first adopted at `6524d0fb`; moved to `85cecae` by PR #76 review F1, because that source adds `quest.publicLocations`, which a fetch-merge without it would reset to false) ("Option B"), not a push/131-only validate exception. Genuine upstream removals are adopted only through a ledger that lists, for the exact OLD/NEW file hashes, every breaking atom and the evidenced class it belongs to; `schema_diff.py diff OLD NEW --accept <ledger>` exits 0 only when the breaking set and the ledger are identical. Every ledger class is re-verified against both source pins by `scripts/schema_adoption_ledger.py`, using methods independent of `schema_extract.py`; an atom no class verifies blocks adoption.

**Evidence:** Director, 2026-10-20, answering (a) push/131-only exception vs (b) full extractor fix and adoption: "Do B, we'll have to fix more than Stormrender. We'll do one big pass and put it in for review".

**Canonical destination:** `state/schema_adoption_ledger_85cecae.json` (the ledger, OLD = `main`'s bdec2883-era files), `skills/building-tnr-content/scripts/schema_diff.py` (`--accept`), `scripts/schema_adoption_ledger.py`; handoff `docs/handoffs/STORMRENDER_FORGE_REPIN_6524D0F.md`.

**Boundary:** Not a law change. Law 4's tag list and `["Highest"]` default, and law 6's flat power cap of 100, now disagree with the source; they go to the law-reconciliation process, not into this ruling. The push/90/93/94 validate exceptions pin the old contract hashes and are voided by their own terms; every diagnostic still reported on them is one they approved.

## RUL-2026-10-20-002 — Ghost Ship chest icons: art direction approved as written

**Date:** 2026-10-20

**Domain:** TNR art production / item icons

**Status:** ACTIVE

**Supersedes:** none

**Ruling:** Twelve chests get new icons: the ten Ghost Ship (Hunt) and Ghost Ship (Gather) reward chests (Common to Legendary Hunter's and Gatherer's tiers, Ornate Chest and Mystery Chest) plus the Rusted Hunter's and Gatherer's Chests, included for set consistency. The icons follow the Ghost Ship / Skyglass style, as set out in `docs/handoffs/GHOST_SHIP_CHEST_ICONS_ART_REQUEST.md`: Hunter's chests carry claw gouges with a leather strap and fang clasp, Gatherer's chests a leaf brand with a rope binding and sprig; tiers escalate Rusted, Common, Rare, Epic, Legendary by material, ornament and crystal; the Ornate Chest may use aged gold as a second accent; the Mystery Chest is chained and sealed with no question mark. Generation follows `docs/workflows/ISOLATED_ART_GENERATION.md`; the director's visual approval of icons 1 and 2 locks the rendered style.

**Evidence:** User, 2026-10-20: "Your direction is approved as written land it on main for the art director".

**Canonical destination:** `docs/handoffs/GHOST_SHIP_CHEST_ICONS_ART_REQUEST.md`.

**Boundary:** No upload, live edit or publication is authorized. The finished icons go to the content review desk as a Forge suggest-mode ticket after intake and preflight. The chests' rarity (all COMMON) is not decided here.

## RUL-2026-10-20-003 — Starter jutsu icons follow the approved jutsu-icon standard, Academy first

**Date:** 2026-10-20

**Domain:** TNR art production / jutsu icons

**Status:** ACTIVE

**Supersedes:** none

**Ruling:** The 62 visible NORMAL jutsu learnable at Academy Student and Genin rank get new icons in the approved JUTSU_ICON standard (RUL-2026-10-17-021 exemplars): technique first, no ninja figure or anatomy, one bold silhouette per jutsu, colour by technique theme since these jutsu carry no element classification, designed dark backgrounds. Phase 1 is the six Academy Student jutsu; the Genin jutsu follow in themed batches. Each raw is approved individually by the director under `docs/workflows/ISOLATED_ART_GENERATION.md`.

**Evidence:** User, 2026-10-20, choosing "Approved icon standard (Recommended)" for making the Academy Student and Genin jutsu "look iconic".

**Canonical destination:** `docs/design/starter_jutsu_icons/JUTSU_ICON_REGISTER.md`.

**Boundary:** No upload, live edit or publication is authorized. Finished icons go to the content review desk as Forge suggest-mode tickets after intake and preflight.

## RUL-2026-10-20-004 — Vaporia, Bakuhatsu and Aerathiel jutsu icons join the approved jutsu-icon standard

**Date:** 2026-10-20

**Domain:** TNR art production / jutsu-icon style references

**Status:** ACTIVE

**Supersedes:** none. Extends RUL-2026-10-17-021 (BBE and BEE library); RUL-2026-10-20-003 is unchanged.

**Ruling (as amended 2026-10-20):** The approved Vaporia, Bakuhatsu and Aerathiel bloodline jutsu icons (five each) are approved examples of the jutsu-icon standard and may be used as style/material references. For Vaporia and Aerathiel these are the director-approved exports in `art/jutsu_icons/vaporia/` and `art/jutsu_icons/aerathiel/`, byte-identical to the live icons. For Bakuhatsu they are the five director-approved 2026-10-19 "Concussive Fracture" raws in `art/jutsu_icons/bakuhatsu/raws/`; the live Bakuhatsu icons are the superseded figure-silhouette set and are not a reference. Each icon's silhouette stays reserved by its family. Aerathiel's Decaying Touch handprint is a family-specific approval, not general licence for hands; the starter jutsu icons stay actor-free.

**Amendment (2026-10-20):** The first text approved the *live* Bakuhatsu icons and called their figure silhouettes a family exception. dauntless corrected this the same day: "No no, Bakuhatsu was this. Those are the old ones. Fix and update", with `bakuhatsu_Art_Studio_Closeout_5of5_20261020.zip` attached (sha256 `c66853c6009e4de3d5bd901b26ab10e4c1f155d88ed079b5aa63e442b6e574cc`). There is no Bakuhatsu figure exception.

**Evidence:** User, 2026-10-20: "There's also vaporia, Bakuhatsu and Aerathiel to compare to. These are also approved".

**Canonical destination:** `docs/design/starter_jutsu_icons/JUTSU_ICON_REGISTER.md` ("Approved comparison families"), which lists each pinned file. Bakuhatsu's raws, ledgers and approval evidence are in `art/jutsu_icons/bakuhatsu/` (README).

**Boundary:** The files are not indexed in `art/style_refs/jutsu_icons/` or `style_refs.json`; that is a separate change. Bakuhatsu's exports passed preflight and the director accepted the family on 2026-10-20 ("They are all approved yes"; recorded in `art/jutsu_icons/bakuhatsu/approved.json`). No upload, live edit or publication is authorized.

## RUL-2026-10-20-005 — Village bloodline scroll icons: art direction approved as written

**Date:** 2026-10-20

**Domain:** TNR art production / item icons

**Status:** ACTIVE

**Supersedes:** none

**Ruling:** The six village bloodline scrolls (Shadow Scroll: Oblivion Seal, Wood Scroll: Shinseina Ki, Storm Scroll: Arashima, Sun Scroll: Taiyo Kami, Wind Scroll: Aerathiel, Ice Scroll: Hyouga Yui), which currently share one image, get their own icons as set out in `docs/handoffs/VILLAGE_BLOODLINE_SCROLL_ICONS_ART_REQUEST.md`: one shared closed-handscroll silhouette, told apart by each bloodline's palette, cord and one element effect, with no symbols, writing or glyphs; the style follows the director-approved crafting caches icons (2026-10-13; provenance in `art/crafting_caches/README.md`). Generation follows `docs/workflows/ISOLATED_ART_GENERATION.md`; the director's visual approval of icon 1 (Oblivion Seal) locks the rendered style.

**Evidence:** User, 2026-10-20: "Approved as written, land it and give me the handoff prompt".

**Canonical destination:** `docs/handoffs/VILLAGE_BLOODLINE_SCROLL_ICONS_ART_REQUEST.md`.

**Boundary:** No upload, live edit or publication is authorized. The finished icons go to the content review desk as a Forge suggest-mode ticket after intake and preflight.

## RUL-2026-10-21-001 — Replacement Technique icon: log-swap art approved as an exception

**Date:** 2026-10-21

**Domain:** TNR art production / jutsu icons (starter jutsu, Phase 1)

**Status:** ACTIVE

**Supersedes:** none. Narrows RUL-2026-10-20-003 for this one icon.

**Ruling:** The director-supplied Replacement Technique icon (a wooden log in swirling smoke with two glowing blue chakra arrows; raw sha256 `90e98a48298c81569d169f3413962425dcc35ce7e89c7237c4c7e0a082102893`) is approved as an exception to the starter register's reserved silhouette ("a dissolving chakra afterimage outline bursting into smoke") and to its "no log-swap substitution trope" rule. The exception covers this icon only: the log and the arrows are not licence for logs, arrows or other substitution props in the remaining starter icons, and the register's rules still apply to them.

**Evidence:** User, 2026-10-21, on being told the raw uses the log trope the brief rules out: "Approve as exception".

**Canonical destination:** `docs/design/starter_jutsu_icons/JUTSU_ICON_REGISTER.md` (Phase 1 table note) and `art/jutsu_icons/starter/README.md`.

**Boundary:** No upload, live edit or publication is authorized. The icon goes to the content review desk as push/148 (suggest mode).

## RUL-2026-10-21-002 — AI pool battle-line pass: accept the residual risk from 14 unread AIs

**Date:** 2026-10-21

**Domain:** Shared AI jutsu pool / battle-line pass push/162–177 (law 18/60)

**Status:** ACTIVE

**Supersedes:** none. Same shape as RUL-2026-10-12-011, for a different pass.

**Evidence:**
- The fresh census push/157–161 read all 512 repository-known live AI ids (512/512 ok, persisted). `profile.getAllAiNames` counted **526** live non-ELDER AIs at both its start (push/157) and its end (push/161).
- So **14 live AIs** have ids the repository does not know and were not read. Forge keeps only the count of a list read.
- Among the 512 read, 345 AIs equip at least one of the 82 pool jutsu; push/162–169 unequip them and push/171–177 re-equip them.

**Ruling:** dauntless accepts the residual risk for the 14 unread AIs. If any of them equips a pool jutsu, push/170's edit severs that AI's combat link to it (law 18/60) and shows the new battle line in its fights.

**Canonical destination:** `push/README.md` (section 162–177, "Not covered").

## RUL-2026-10-21-003 — AI pool battle-line pass keeps the law order: unequip, edit, re-equip

**Date:** 2026-10-21

**Domain:** Shared AI jutsu pool / battle-line pass push/162–177 (law 18/60)

**Status:** ACTIVE

**Supersedes:** none.

**Evidence:** The user first described the pass as "update the jutsu first, then perform the unequip and re-equip of each AI". Law 60 (`docs/ENGINE_LAWS.md`) requires strictly unequip, then edit, then re-equip, and says an edit followed by a re-equip is not sufficient. The game source at `studie-tech/TheNinjaRPG@dcf1cea` (`routers/jutsu.ts` update) shows no mechanism that would make edit-first safe. Asked to choose, the user answered "keep law order".

**Ruling:** push/162–169 (unequip) run before push/170 (edit), and push/171–177 (re-equip) run after it. Law 60 is unchanged.

**Canonical destination:** `docs/ENGINE_LAWS.md` laws 18 and 60 (unchanged); the run order in `push/README.md` section 162–177.

## RUL-2026-10-21-004 — AI pool battle lines, renames and Rallying Spiral target approved

**Date:** 2026-10-21

**Domain:** Shared AI jutsu pool content (`32b_DATA_pool.json`, 82 jutsu)

**Status:** ACTIVE

**Supersedes:** the reconstructed battle text in `state/ai_pool_battle_lines/recovered/` (kept for comparison only).

**Ruling:**
- The 82 battle lines in `state/ai_pool_battle_lines/battle_lines.json` are approved as written: 2–3 sentences each, an Edo-era ninja voice, chakra-driven, describing only effects the live record carries.
- The 17 renames are approved, including B28 Recoil Slam → Backlash Palm (chosen earlier) and B04 Executioner Seal → Choking Seal.
- B31 Rallying Spiral targets `ALLY` instead of `OTHER_USER`. Its buffs used to land on the enemy. The user's instruction was "Retire rallying spiral lol, or have it target allies"; it was retargeted rather than retired.

**Evidence:** User, 2026-10-21: "approve the prose", after reviewing `state/ai_pool_battle_lines/REVIEW.md`; the B31 instruction is quoted above. The user also stated recoil's meaning: a debuff on an enemy that, while active, deals the recoil percentage of the damage they deal back to themselves. That matches `tags.ts` `recoil` at `dcf1cea`.

**Open:** B28's recoil has `rounds: 0`. `isEffectActive` (`libs/combat/util.ts`) treats a 0-round effect as expired, and recoil does not fire on the round it is applied, so as stored it never has an active round. Its duration is a balance decision, not yet made.

**Canonical destination:** `state/ai_pool_battle_lines/battle_lines.json` (source of push/170). After an operator-verified live run, the pool registry names and B31's target are updated through `32_REGISTRY_shared_ai_pool.md` → `32b_DATA_pool.json`.

**Boundary:** No live edit is authorized by this ruling. The operator runs push/162–177 through Forge.

## RUL-2026-10-21-005 — Backlash Palm's recoil lasts 2 rounds

**Date:** 2026-10-21

**Domain:** Shared AI jutsu pool balance (B28, `ElSK-RCrLjddEUm76FZrs`)

**Status:** ACTIVE

**Supersedes:** closes the "Open" item in RUL-2026-10-21-004.

**Evidence:** B28's recoil effect was stored with `rounds: 0`. Recoil is a debuff on the enemy that, while active, turns the recoil percentage of the damage they deal back on themselves (the user's statement, matching `tags.ts` `recoil` at `studie-tech/TheNinjaRPG@dcf1cea`). It does not fire on the round it is applied, and `isEffectActive` (`libs/combat/util.ts`) treats a 0-round effect as expired, so as stored it never had an active round. User, 2026-10-21: "It needs rounds: 2".

**Ruling:** B28's recoil effect gets `rounds: 2`. Its power (15%) and every other field are unchanged.

**Implementation:** `battle_lines.json` `effect_rounds: {"recoil": 2}` on B28. push/170 re-sends B28's live effects list with only that number changed, leaving out the obsolete `recoil.statTypes` key, which the server drops on any save (pinned keys: `forge/src/runner/nested.json`). The read-back check compares effects on the pinned keys.

**Canonical destination:** `state/ai_pool_battle_lines/battle_lines.json` (source of push/170).

## RUL-2026-10-21-006 — Next project: the QA ticket pipeline, with Forge Next Phase 1 as its stage one

**Date:** 2026-10-21

**Domain:** Roadmap / content QA / Forge Next

**Status:** SHELVED 2026-10-21. The director: "Let's skip this for now, seems excessive." Ticket work continues by hand as suggest-mode manifests in `push/`, as for push/132–156. RUL-2026-09-20-004 is unchanged.

**Supersedes:** none. Keeps RUL-2026-09-20-004 (Forge Next Phase 1 is the next implementation work, ahead of Presentation Studio P2) and gives Phase 1 a concrete work package.

**Evidence:** The 92 suggestions sent to the content review desk on 2026-10-19 and 2026-10-20 (push/125–156) all read `PENDING` in their committed bundles. Forge records review outcomes only in the browser journal, so the director could not see what was approved or rejected, or why. Offered (1) the ticket pipeline with Phase 1 re-scoped as its first stage, or (2) Phase 1 as originally frozen, then the pipeline, the director answered: "Ticket pipeline with Phase 1 as stage one, draft the brief".

**Ruling:** The next project is a find → fix → submit → track pipeline for content tickets. Stage one is `state/prompt_forge_next_phase1.md`, implemented as frozen, with its research-read registry's first rows being the review desk's `contentReview.getQueue` and `getProposal` (and, depending on decision D1, the paged catalog reads). Stage two is a ticket ledger. Stage three adds fix generators and the operating loop.

**Canonical destination:** `state/prompt_qa_ticket_pipeline.md` (DRAFT FOR INDEPENDENT REVIEW; its open decisions D1–D6 are listed in its §7).

**Boundary:** No implementation has begun. The brief becomes the implementation contract only after independent review and the director's answers to the stage-one decisions (D1–D4).

## RUL-2026-10-21-007 — Water's Domain overhaul: text and icon direction approved

**Date:** 2026-10-21

**Domain:** Player jutsu overhaul / jutsu text and icons

**Status:** ACTIVE

**Supersedes:** none

**Ruling:** Water's Domain (`-8W4JOqG3Cb-oPQtF9rMs`) gets the description "Within the user's domain, water answers to them alone. It rises to crush their foe, then flows back to its master, deepening their healing for a short time." and the battle line "%user spreads their domain across the field, hurling its tide at %target before the waters pool back around %user to strengthen their healing." Its new icon follows option I1: a vast whirlpool basin with a churning white-foam rim and a calm eye glowing soft restorative aqua, in the approved jutsu-icon standard (deep blue and white foam, one aqua-teal accent), Vaporia Surfing Strike as the style/material reference only. The director's visual approval of the raw still locks the art.

**Evidence:** User, 2026-10-21, after reviewing three descriptions, two battle lines and three icon options: "D2 with edits : 'Within the user's domain, water answers to them alone. It rises to crush their foe, then flows back to its master, deepening their healing for a short time.' B2 I1". Earlier the same day: "I think we need a better description for it than that, one that encompasses the technique name and it's effect better. This will be part of a larger overhaul, we will submit an art request for a new icon as well."

**Canonical destination:** `docs/design/jutsu_overhaul/JUTSU_OVERHAUL_REGISTER.md` (section 1).

**Boundary:** No upload, live edit or publication is authorized. Text and icon go to the content review desk as separate Forge suggest-mode tickets; the text ticket is built only after the push/178-181 census confirms the live record.

## RUL-2026-10-21-008 — Blazing Death Star overhaul: text and icon direction approved

**Date:** 2026-10-21

**Domain:** Player jutsu overhaul / jutsu text and icons

**Status:** ACTIVE

**Supersedes:** none

**Ruling:** Blazing Death Star (`y0fmp1QvVcQnBoVZVLFfL`) gets the description "Shuriken wreathed in fire nature chakra blaze across the field like falling stars. They strike the target and leave them smouldering, so the blows that follow burn deeper." and the battle line "%user hurls a fan of shuriken that ignite mid-flight, slamming into %target as blazing stars and leaving them smouldering." Its new icon follows option I2: three flaming four-pointed shuriken in a falling-star arc, each trailing a tail of fire, in the jutsu-icon pixel-art rendering (ember orange and molten gold on charcoal), Vaporia Scorch Break as the style/material reference only. The director's visual approval of the raw still locks the art. Drafting note from the same review: single-target reach is not announced with stock phrases such as "one foe" ("You seem to have a fixation on 'one foe' as a term.").

**Evidence:** User, 2026-10-21, after three redrafted descriptions, two battle lines and three icon options: "D1, B1, I2".

**Canonical destination:** `docs/design/jutsu_overhaul/JUTSU_OVERHAUL_REGISTER.md` (section 2).

**Boundary:** No upload, live edit or publication is authorized. Text and icon go to the content review desk as separate Forge suggest-mode tickets, the icon only after the text suggestion resolves.

## RUL-2026-10-21-009 — Divine Thunder Slap overhaul: text approved

**Date:** 2026-10-21

**Domain:** Player jutsu overhaul / jutsu text

**Status:** ACTIVE

**Supersedes:** none

**Ruling:** Divine Thunder Slap (`Je0gvHDVCm__vy2rT8YBB`) gets the description "The user claps their hands until they crackle with lightning, then delivers a thunderous open-palm slap. The charge lingers in their hands, making their next attacks hit harder." and the battle line "Lightning gathers between %user's palms and breaks across %target in one ringing slap, leaving %user crackling with power." Icons for the overhaul are paused for now: "lets skip icons for now since we cant submit icons and text fixes" (text and icon suggestions cannot both be open on one record).

**Evidence:** User, 2026-10-21, after three descriptions and two battle lines: "D1, B2".

**Canonical destination:** `docs/design/jutsu_overhaul/JUTSU_OVERHAUL_REGISTER.md` (section 3).

**Boundary:** No live edit or publication is authorized. The text goes to the content review desk as a Forge suggest-mode ticket.

## RUL-2026-10-21-010 — Fire Release: Great Fireball overhaul: text approved

**Date:** 2026-10-21

**Domain:** Player jutsu overhaul / jutsu text

**Status:** ACTIVE

**Supersedes:** none

**Ruling:** Fire Release: Great Fireball (`jwXvmSztaK81u2k98Hc1Z`) gets the description "The user draws a deep breath and exhales a towering fireball that bursts over an area. Every enemy caught in the blaze keeps burning, taking more damage over the next few rounds." and the battle line "%user draws a deep breath and unleashes a roaring fireball, engulfing %target in flames that leave lasting burns." The jutsu's name was flagged as echoing a franchise technique; no renaming decision has been made.

**Evidence:** User, 2026-10-21, after three descriptions and two battle lines: "D1, B2".

**Canonical destination:** `docs/design/jutsu_overhaul/JUTSU_OVERHAUL_REGISTER.md` (section 4).

**Boundary:** No live edit or publication is authorized. The text goes to the content review desk as a Forge suggest-mode ticket; the name is untouched.

## RUL-2026-10-21-011 — Earthshatter Strike overhaul: text approved

**Date:** 2026-10-21

**Domain:** Player jutsu overhaul / jutsu text

**Status:** ACTIVE

**Supersedes:** none

**Ruling:** Earthshatter Strike (`kw8dlRl4y5WBg8GkHSEvp`) gets the description "The user drives a chakra-packed fist into the ground, and the shockwave rolls back up through their body. For a short time they shrug off blows like bedrock and their taijutsu lands harder." and the battle line "%user splits the ground with a single punch and plants their feet in the rubble, steeling their body for the blows to come." The name ("Strike" on a jutsu that deals no damage) was flagged; no renaming or balance decision has been made.

**Evidence:** User, 2026-10-21, after three descriptions and two battle lines: "D1, B2".

**Canonical destination:** `docs/design/jutsu_overhaul/JUTSU_OVERHAUL_REGISTER.md` (section 5).

**Boundary:** No live edit or publication is authorized. The text goes to the content review desk as a Forge suggest-mode ticket; the name and effects are untouched.

## RUL-2026-10-21-012 — Suggest-mode rationales state the fix, briefly

**Date:** 2026-10-21

**Domain:** Forge suggest mode / manifest authoring

**Status:** ACTIVE

**Supersedes:** none. Narrows RUL-2026-10-19-007 (rationales stay specific to each record).

**Ruling:** A per-item `suggestion.rationale` is one to three plain sentences: what was wrong and what the fix changes. No narrative or retelling of the old text. Example (push/185): "Adds the missing user damage boost (+20% for 2 rounds) to both texts. Battle line: 'his' replaced, 'subtle hit caresses' wording removed."

**Evidence:** User, 2026-10-21: "Let's make our ticket rationale's a bit less verbose. Describe the fix without telling a story." Applied the same day to the unrun push/183, 184, 185 and 187; push/182 and 186 were already submitted.

**Canonical destination:** `docs/design/FORGE_SUGGEST_MODE_SCOPE.md` ("Implemented: option 1", rationale paragraph).

**Boundary:** No code change. The jutsu text guide (under review at `c0e9d1b`) picks this up after review, not on the frozen SHA.

## RUL-2026-10-21-013 — Earthshatter Strike reworked as Bedrock Stance

**Date:** 2026-10-21

**Domain:** Player jutsu overhaul / jutsu name and text

**Status:** ACTIVE

**Supersedes:** RUL-2026-10-21-011 (its text was never submitted; push/187 was withdrawn unrun).

**Ruling:** Jutsu `kw8dlRl4y5WBg8GkHSEvp`, live as Earthshatter Strike, is renamed "Bedrock Stance" with the description "The user roots themselves to the earth and draws its strength up through their body. For a short time they shrug off blows like bedrock and their taijutsu lands harder." and the battle line "%user sinks into a low stance as the ground hardens beneath them, their body turning stone-steady and their fists heavy." Its effects (a self buff, no damage) are unchanged.

**Evidence:** User, 2026-10-21: "Honestly earthshatter strike needs a rename as well, if it doesnt deal damage it shouldnt be called a strike. Let's rework the whole thing", then, after four names, three descriptions and two battle lines: "N1, D1, B2".

**Canonical destination:** `docs/design/jutsu_overhaul/JUTSU_OVERHAUL_REGISTER.md` (section 5).

**Boundary:** No live edit or publication is authorized. Name and text go to the content review desk as one Forge suggest-mode ticket. Name uniqueness was checked only against the 1,500 names the repository knows; the desk's save validation is the final check.

## RUL-2026-10-21-014 — Flame Barrage overhaul: text approved

**Date:** 2026-10-21

**Domain:** Player jutsu overhaul / jutsu text

**Status:** ACTIVE

**Supersedes:** none

**Ruling:** Flame Barrage (`OZp6neM54VPLXIzHc713P`) gets the description "The user looses a spiralling stream of fireballs across the field, scorching every enemy in its path. The rising heat stokes the user's own chakra, making their attacks hit harder for a short time." and the battle line "%user hurls a spiralling barrage of fireballs across the battlefield, the flames roaring back to stoke their own chakra."

**Evidence:** User, 2026-10-21, after three descriptions and two battle lines: "D1, B1".

**Canonical destination:** `docs/design/jutsu_overhaul/JUTSU_OVERHAUL_REGISTER.md` (section 6).

**Boundary:** No live edit or publication is authorized. The text goes to the content review desk as a Forge suggest-mode ticket.

## RUL-2026-10-21-015 — Kinjutsu: Black Thorn Rose overhaul: text approved

**Date:** 2026-10-21

**Domain:** Player jutsu overhaul / jutsu text

**Status:** ACTIVE

**Supersedes:** none

**Ruling:** Kinjutsu: Black Thorn Rose (`qB550OM_X-Mh0w_KlNNji`) gets the description "A forbidden art paid for in the user's own blood. Black thorn vines lash out in a spiral, choking the healing of every enemy they catch, while the rose's thorns close around the user as armour." and the battle line "%user opens their palm with a thorn and lets the blood fall. A black rose tears up through the earth, its vines spiralling outward to choke every wound they find, while its thorns curl back to armour the one who fed it." Drafting note: forbidden and high-rank jutsu get a fuller, higher-quality battle line (two sentences are fine) rather than a plain one-liner.

**Evidence:** User, 2026-10-21: "D1. Battle line needs more work, this is a forbidden jutsu it should have a high quality battle line", then, from four richer drafts: "B3".

**Canonical destination:** `docs/design/jutsu_overhaul/JUTSU_OVERHAUL_REGISTER.md` (section 7). The drafting note goes into the jutsu text guide after its review.

**Boundary:** No live edit or publication is authorized. The text goes to the content review desk as a Forge suggest-mode ticket.

## RUL-2026-10-21-016 — Static Flicker overhaul: text approved

**Date:** 2026-10-21

**Domain:** Player jutsu overhaul / jutsu text

**Status:** ACTIVE

**Supersedes:** none

**Ruling:** Static Flicker (`UwWqo_4Igdue7-unPXwne`) gets the description "The user flickers to a new position in a crack of static and discharges a burst of lightning that cuts straight through the guard of nearby enemies. The charge clings to them, so the blows that follow hurt more." and the battle line "%user vanishes in a crackle of static and reappears across the field, releasing a burst of lightning that leaves nearby enemies sparking."

**Evidence:** User, 2026-10-21, after three descriptions and two battle lines: "D1, B1".

**Canonical destination:** `docs/design/jutsu_overhaul/JUTSU_OVERHAUL_REGISTER.md` (section 8).

**Boundary:** No live edit or publication is authorized. The text goes to the content review desk as a Forge suggest-mode ticket.

## RUL-2026-10-21-017 — Martial Movement overhaul: text approved

**Date:** 2026-10-21

**Domain:** Player jutsu overhaul / jutsu text

**Status:** ACTIVE

**Supersedes:** none

**Ruling:** Martial Movement (`V34OBxnSDj6PfxT4Y3fhx`) gets the description "A measured martial step carries the user across the field. Its flowing feints unsettle every enemy close to where they land, dulling their attacks for a short while." and the battle line "%user crosses the field in a few controlled steps and settles into a flowing guard, throwing nearby enemies off their rhythm."

**Evidence:** User, 2026-10-21, after three descriptions and two battle lines: "D2, B1".

**Canonical destination:** `docs/design/jutsu_overhaul/JUTSU_OVERHAUL_REGISTER.md` (section 9).

**Boundary:** No live edit or publication is authorized. The text goes to the content review desk as a Forge suggest-mode ticket.

## RUL-2026-10-21-018 — Void Rend overhaul: text approved

**Date:** 2026-10-21

**Domain:** Player jutsu overhaul / jutsu text

**Status:** ACTIVE

**Supersedes:** none

**Ruling:** Void Rend (`_QfGq0SseWD11jHO23pr1`) gets the description "In one surging step the user closes in and tears at the space around them with raw chakra. Every enemy caught in the rend takes damage and finds their healing weakened for several rounds." and the battle line "%user lunges across the field, and a rift of unstable chakra splits open around them, rending nearby enemies and leaving wounds that refuse to close."

**Evidence:** User, 2026-10-21, after three descriptions and two battle lines: "D2, B2".

**Canonical destination:** `docs/design/jutsu_overhaul/JUTSU_OVERHAUL_REGISTER.md` (section 10).

**Boundary:** No live edit or publication is authorized. The text goes to the content review desk as a Forge suggest-mode ticket.

## RUL-2026-10-21-019 — Purgatory overhaul: text approved

**Date:** 2026-10-21

**Domain:** Player jutsu overhaul / jutsu text

**Status:** ACTIVE

**Supersedes:** none

**Ruling:** Purgatory (`_Hhz6aPpNCMc4U7hNzDqe`) gets the description "The user ignites their limbs with fire chakra and unleashes a spiralling flurry of burning strikes that scorches every enemy in its path. The blaze keeps roaring through their body, making their attacks hit harder for a short time." and the battle line "Flames burst from %user's fists and feet as they whirl through a spiral of strikes, the heat building with every blow."

**Evidence:** User, 2026-10-21, after three descriptions and two battle lines: "D1, b2".

**Canonical destination:** `docs/design/jutsu_overhaul/JUTSU_OVERHAUL_REGISTER.md` (section 11).

**Boundary:** No live edit or publication is authorized. The text goes to the content review desk as a Forge suggest-mode ticket.

## RUL-2026-10-21-020 — Blazing Edge overhaul: text approved

**Date:** 2026-10-21

**Domain:** Player jutsu overhaul / jutsu text

**Status:** ACTIVE

**Supersedes:** none

**Ruling:** Blazing Edge (`oPtg5xq6HaYgJBqzKsZUC`) gets the description "Fire chakra forms a sword in the user's hand as they surge to a new position and sweep it through nearby enemies. The scorched cuts resist healing for a short while." and the battle line "Flames take the shape of a sword in %user's hand as they surge across the field, carving through nearby enemies in a single searing arc."

**Evidence:** User, 2026-10-21, after three descriptions and two battle lines: "D2 b2".

**Canonical destination:** `docs/design/jutsu_overhaul/JUTSU_OVERHAUL_REGISTER.md` (section 12).

**Boundary:** No live edit or publication is authorized. The text goes to the content review desk as a Forge suggest-mode ticket.

## RUL-2026-10-21-021 — Liquid Palm text approved; house style derived; full-census sweep requested

**Date:** 2026-10-21

**Domain:** Player jutsu overhaul / jutsu text

**Status:** ACTIVE

**Supersedes:** none

**Ruling:** (1) Liquid Palm (`boyPcTIywrR-adY6M6ZAN`) gets the description "The user flows to a new position and unleashes rapid water-charged palm strikes on the enemies around them. The current keeps moving through their body afterwards, turning part of every blow they take into health for a short time." and the battle line "%user glides forward on a rush of water chakra and crashes into nearby enemies with rapid palm strikes, the current around them ready to drink in the next blow." (2) The director's choices so far are distilled into a house style, `docs/design/jutsu_overhaul/WRITING_STYLE.md`. (3) Every eligible jutsu in the 2026-10-21 census is checked against that style and the live effects, and the edits go out as one master suggest-mode manifest, one suggestion per jutsu (each still approved or rejected on its own at the review desk).

**Evidence:** User, 2026-10-21: "D1, B2. Analyze my choices thus far to develop a writing style. Then analyze all jutsu in the census for edits and create one master manifest to submit tickets for each."

**Canonical destination:** `docs/design/jutsu_overhaul/WRITING_STYLE.md` (style); `docs/design/jutsu_overhaul/JUTSU_OVERHAUL_REGISTER.md` (Liquid Palm, section 13).

**Boundary:** No live edit or publication is authorized. Names, effects and balance are out of scope for the sweep; name and mechanics findings are flagged to the director. This ruling is the director's go-ahead for sweep text written in the house style without one-by-one picks; the review desk remains the approval step.

## RUL-2026-10-21-022 — Jutsu text edits are targeted; American English; generic area wording

**Date:** 2026-10-21

**Domain:** Player jutsu overhaul / jutsu text

**Status:** ACTIVE

**Supersedes:** the British-spelling and "one-sentence battle line" parts of the house style derived under RUL-2026-10-21-021.

**Ruling:** Text fixes on existing jutsu are targeted: keep the length, voice and content of premium text and change only what is inaccurate or broken; full rewrites are for placeholder, stub, broken or wholly wrong text. American English only. Area wording must not assume anyone stands in the area. Single-target battle lines use %target. Avoid chance wording where power growth (powerPerLevel, cap 25) makes it untrue. Absorb reads as health first. Totem summons, custom reskins, custom or contributed jutsu, test jutsu and non-functioning jutsu are not touched; event jutsu are never simplified; villages use current names (Glacier is Hyorin).

**Evidence:** The director's review of push/196 on the content review desk, 2026-10-21: 135 applied, 207 rejected, with written reasons (e.g. "Description is good. Battle description overwrites too much, rewrite"; "No British spelling. We're English mate. American English only"; "'And the enemies around them' is not good description text for AoE attacks, there won't always be enemies in the surrounding area"; "When performing rewrites to adjust effect accuracy and grammar, we want to maintain the same quality/quantity of content, and make targetted corrections only"; "Dont rewrite totems"; "This is a custom reskin"). Exported as harvests/inbox/tnr_results_1792614808975.json.

**Canonical destination:** `docs/design/jutsu_overhaul/WRITING_STYLE.md` ("Review lessons").

**Boundary:** No live edit. The jutsu text guide under review (c0e9d1b) picks these up after its review.

## RUL-2026-10-22-001 — Two Tails armor icons: match the Kitsune set, offensive nekomata theme

**Date:** 2026-10-22

**Domain:** TNR art production / item icons

**Status:** ACTIVE

**Supersedes:** none

**Ruling:** The five Two Tails armor pieces (Zukin, Shozoku, Tekkou, Tabi, Jaki-Tabi) get new icons that read as a family with the Kitsune armor set (style reference) but with a more offensive theme. Icons only: names, text, stats and effects are unchanged. The theme is the folklore nekomata (two-tailed cat spirit), avoiding blue ghost-fire and other imagery tied to the franchise's two-tailed cat. The Kitsune icons may be downloaded from the game's image CDN as style references (image files only; no game request).

**Evidence:** User, 2026-10-22: "update the Two Tails armor set to match the Kitsune set but with a more offensive theme. We'll set up the task and pass off the image generation to the art director, then take the raw assets and process them for a ticket manifest", then "Icons only, download the Kitsune images, nekomata approved".

**Canonical destination:** `docs/handoffs/TWO_TAILS_ARMOR_ICONS_ART_REQUEST.md` (written after the push/204 capture).

**Boundary:** No upload, live edit or publication. The finished icons go to the content review desk as a Forge suggest-mode ticket after intake and preflight; the director approves each raw.

## RUL-2026-10-22-002 — Two Tails armor: new icons dropped; stats to become an offensive Kitsune counterpart

**Date:** 2026-10-22

**Domain:** Item balance / armor sets

**Status:** ACTIVE (proposal stage; numbers await the director)

**Supersedes:** RUL-2026-10-22-001 (the new Two Tails icons are not needed; push/205 withdrawn unrun; the processed art stays in `art/two_tails_armor/` unused).

**Ruling:** The Two Tails armor set's stats are reworked into an offensive version of the Kitsune set: a slightly stronger counterpart geared to offensive tags, with slightly higher pool values than Kitsune. The values are a balance decision for the director; the proposal is in `docs/design/two_tails_armor/TWO_TAILS_STATS_PROPOSAL.md`.

**Evidence:** User, 2026-10-22: "Change of plans, we dont need these new icons. We just need to adjust the stats of the Two Tails set to be an offensive version of the Kitsune set, with slightly higher pools. So we need it to be a slightly stronger counterpart to Kitsune with a more offensive theme."

**Canonical destination:** `docs/design/two_tails_armor/TWO_TAILS_STATS_PROPOSAL.md`.

**Boundary:** No manifest until a version is approved; no live edit.


## RUL-2026-10-22-003 — Tenryūseigan kit: new jutsu as exact copies of Ethereal Monarch's six

**Date:** 2026-10-22

**Domain:** Bloodline jutsu / content creation

**Status:** ACTIVE (build pending the director's open decisions below)

**Supersedes:** none

**Ruling:** Tenryūseigan (`ieDD4S_zzLMmVadUuD69s`, H rank, hidden) gets its own kit of six jutsu that are exact copies of Ethereal Monarch's six (effects and stats unchanged), under the director's new names, with the director-supplied icons (`art/jutsu_icons/tenryuseigan/`) and new text (`docs/design/jutsu_overhaul/TENRYUSEIGAN_TEXT_DRAFTS.md`). Mapping: Celestial Bind = Celestial Sealing, Heavenly Barrier = Heavenly Constructs (unlocks Void Gaze), Dragon Eye Awakening = Starlight Veil, Storm Dragon = Founder's Wrath, Void Gaze = Stardust, Skyfang Burst = Tamashī no Sakeme.

**Evidence:** push/206 (`harvests/inbox/tnr_results_1792635598196.json`): the three existing "Tenryūseigan" copies are attached to Ethereal Monarch, so Tenryūseigan has no jutsu of its own. User, 2026-10-22: "I think we'll need to make new jutsu for the bloodline", then "Exact copies, I'll figure out the rest in a bit".

**Open (director):** reuse the three existing copies or create all six; whether Skyfang Burst's `consume` moves from the target to the caster; ship as a direct builder manifest or as two suggest-mode rounds; final names and prose.

**Canonical destination:** `docs/design/jutsu_overhaul/TENRYUSEIGAN_TEXT_DRAFTS.md` (mapping, text, flags); the create manifest once the open points are settled.

**Boundary:** No live write until the director runs the manifest. Hiding or retiring the existing copies is a separate director decision.

## RUL-2026-10-22-004 — QA S1 quest items: intended or out of scope; Salt Gate Phantom may be deleted

**Date:** 2026-10-22

**Domain:** Quests / QA triage (`docs/reviews/QA_LIVE_2026-10-20.md`, S1 quest sections)

**Status:** ACTIVE

**Supersedes:** none

**Ruling:** The QA S1 quest findings are closed as follows. The Nameless Thorn (`qn36dRZfTnru7oSgjDElO`) is stranded on purpose; leave it. The Kuroganekai CHUNIN/GENIN (`iQ5tqJaUKSvqbOybqVVDy`, `iUnQO8Fek3yJ-tL4Djv99`) and Subaku Demon Castle (`Br7u84Gq7orlEpu0yqy1A`) battle-gating and fail-route findings are left alone. The achievement Kill the Creator (`g2ilVOzFys21wkEHwfTeE`) targets the game creator's account on purpose (it awards an achievement for defeating him). Salt Gate Phantom (`nwVJG9bsllGo7DefKM2ic`) is believed to be a stub and may be deleted; deletion is the director's run after a capture confirms it is a stub. Ravena Bloodsilk's Crimson Impact was repaired by the director directly, so push/128's equip step is spent.

**Evidence:** User, 2026-10-22: "Salt Gate Phantom can be deleted I believe its just a stubborn. The Namelwss Thorn is meant to be stranded, leave it be. Leave the KGK/Subaku stuff alone as well. Kill the Creator points to the game creator's account and awards an achievement for killing him. I cant check any of those, I did repair crimson impact on Ravena."

**Canonical destination:** this ruling (QA triage record); future QA passes should whitelist these ids.

**Boundary:** No quest manifest is implied except an optional Salt Gate Phantom capture and delete, run by the director.

## RUL-2026-10-22-006 — Scroll icons: one colour per scroll, KGK keeps violet, universal bloodline scroll shape

**Date:** 2026-10-22

**Domain:** TNR art production / item icons (jutsu and bloodline scrolls)

**Status:** ACTIVE

**Supersedes:** none (extends RUL-2026-10-20-005, the village bloodline scroll set)

**Ruling:** Every jutsu and bloodline scroll must read as a different scroll at icon size: one colour slot per scroll (KGK as one family keeps violet on black lacquer, and its four scrolls stay on two shared images). Oblivion Seal is recoloured away from violet. The village scroll silhouette becomes the universal bloodline scroll shape (Scroll of Metal and Scroll of Time move to it); the fat steel-capped event silhouette is the jutsu scroll shape. The live Shadows, Hollow Veil and Cleave icons (push/215, already submitted) are revisited later. Plan and colour slots: `docs/design/scroll_icons/SCROLL_ICON_ROADMAP.md`.

**Evidence:** User, 2026-10-22: "We want each scroll to clearly read as a different scroll... The KGK scrolls are already high quality so we may want to design around them rather than replace them outright"; answers: "1. Already ran, we'll worry about it later 2. Recolor 3. No 4. Village scroll, we'll make it a universal bloodline scroll shape not just villages".

**Canonical destination:** `docs/design/scroll_icons/SCROLL_ICON_ROADMAP.md`.

**Boundary:** Colour slots are proposals until the director approves each raw. No upload without a ticket.

## RUL-2026-10-23-001 — Aegis of Shadows renamed Abyss of Shadows

**Date:** 2026-10-23

**Domain:** Jutsu naming / event jutsu text and icon

**Status:** ACTIVE (texts final in `EVENT_JUTSU_STORY_TEXT.md`; icon "the black sun", replacing the engulfing wave, 2026-10-23)

**Supersedes:** none

**Ruling:** Event jutsu Aegis of Shadows (`XS08zZhUhK615Dle4j3f3`) is renamed **Abyss of Shadows**: it curses the target (deals less damage, takes more) rather than shielding the user. Its new icon shows a gaping oxblood abyss swallowing a cracked blade and shield; its texts are rewritten in premium event voice; the Scroll of Shadows description names the new jutsu. Oxblood and shadow theme approved.

**Evidence:** User, 2026-10-23: "Aegis needs a rename and jutsu description adjustment along with its icon... Its more of a curse than an Aegis now"; "The oxblood and shadow theme from the scroll is approved. The description needs to be more premium"; "Abyss of Shadows is the one. The enemy is engulfed in an abyss of shadow energy that dulls their offensive moves and cuts their defensive abilities".

**Canonical destination:** `docs/design/jutsu_overhaul/ABYSS_OF_SHADOWS_TEXT.md`; icon row in `docs/handoffs/SCROLL_JUTSU_ICONS_ART_REQUEST.md`.

**Boundary:** The rename and texts ship in the combined icon ticket, in the same suggestion as the new icon (director, 2026-10-23).

## RUL-2026-10-23-002 — Chakra Overflow icon: its own project; color C, directions D1 + D2

**Date:** 2026-10-23

**Domain:** Art direction / jutsu icons

**Status:** ACTIVE (round 1 briefed)

**Supersedes:** none

**Ruling:** Chakra Overflow (`e2eC-x4UXc5m6QexNbx8w`), the most-used jutsu in the game, gets its icon as a dedicated project, split out of jutsu upgrade batch 1. Color **C**: deep chakra blue erupting into gold and white-hot light where it overflows. Round 1 explores **D1, the breaking vessel** (an orb of chakra cracking open, light spilling over its rim) and **D2, the flare** (a white-hot core erupting upward in a crown of flame-tongues), plus their hybrid.

**Evidence:** User, 2026-10-23: "Chakra Overflow is probably the cornerstone jutsu of the game... It is in my opinion the most important icon in the game... Needs to be the best, most iconic, high quality icon we do. Nothing less will suffice... It deserves a project of its own essentially."; "C and D1 plus D2, write the art prompt".

**Canonical destination:** `docs/design/chakra_overflow/CHAKRA_OVERFLOW_ICON_PROJECT.md`; round-1 prompt `docs/handoffs/CHAKRA_OVERFLOW_ART_SESSION_PROMPT.md`.

**Boundary:** The final pick and every refinement are the director's. Text for Chakra Overflow is finalized with the icon.

**Amendment (2026-10-23):** concept is **boundless chakra**, not a vessel overflowing. User: "An item doesnt need to overflow, the chakra we're depicting is what's overflowing. You're activitating this flow of energy by using the technique. So we want to convey boundless chakra with this icon." D1 and the hybrids are retired; color C reads as intensity. Round 2 brief: `docs/design/chakra_overflow/DRAFT1_REVIEW.md` section 6.


## RUL-2026-10-23-003 — Ghost Ship becomes the Skyglass Wreck party dungeon; profession quests retired

**Date:** 2026-10-23

**Domain:** Ghost Ship / Skyglass / content structure

**Status:** ACTIVE (direction; balance, rates, placement details and art open)

**Supersedes:** the two profession-gated Ghost Ship quests (Gather `6Ri-W5TtUrEMWpyYlnf_F`, Hunt `HckXVOf-qk6ESU9t5rxLh`) as the delivery for Skyglass content. Item, AI and jutsu rulings stay in force.

**Ruling:** The Ghost Ship ensemble becomes a repeatable party dungeon of **two tiers**. Its only completion drop is **exactly one treasure chest per player**. The chest pays regular loot (ryo and themed items); treasure maps are the bonus. The dungeon is placed **in the open, between land and sea**. **Both profession quests are retired**; a brand-new Battle Pyramid carries the original adventure (RUL-2026-10-23-004). Rewards are universal: profession-locked chests leave the plan (Option 1), because the game cannot restrict a reward choice by profession.

**Evidence:** User, 2026-10-23: "Option 1 it is"; "I want a repeatable dungeon groups can run that drops exactly one treasure chest"; "1. Two is fine. 2. Yes the chest should have regular drops too like ryo and themed items, the treasure maps are the bonus ... 6. Needs to be placed in the open somewhere, between land and sea. 7. Both are retired, we make a brand new one."

**Canonical destination:** `docs/design/SKYGLASS_DUNGEON_AND_TREASURE_HUNTS.md`.

**Boundary:** Retirement mechanism and timing, the floor roster, sector, rates and art are not settled. No live write is authorized.

## RUL-2026-10-23-004 — Treasure maps open isolated Skyglass treasure-hunt Pyramids

**Date:** 2026-10-23

**Domain:** Ghost Ship / Skyglass / treasure hunts

**Status:** ACTIVE (direction and first slate; content not authored)

**Supersedes:** none

**Ruling:** The dungeon chest drops **tradable treasure maps** ("you can sell it or run it"). Each map is the entry item of one **isolated** `battlepyramid` treasure hunt: short and punchy, Skyglass Project themed. First slate approved for development: **The Silent Bastion, The Drowned Foundry, The Quarantine Vault, and The Skyglass Expedition** (the original Ghost Ship adventure preserved as the rare map). The **Skyglass Katana and Crown fragment are Expedition-only** — "that's the draw". Hunts use **new bosses with reused Ghost Ship crew**. **Map cost is the only intended limit.**

**Evidence:** User, 2026-10-23: "3. Yes, tradeable. You can sell it or run it. 4. Expedition only, that's the draw. 5. Map cost is enough."; "I like the idea of preserving the original ghost ship quest in the Skyglass expedition ... maybe we make shorter punchier 'treasure hunts' that are themed after the Skyglass Project"; "1. Your direction is approved. 2. Mixed, new bosses reuse crew. 3. Isolated. 4. Map cost is the only limit."

**Canonical destination:** `docs/design/SKYGLASS_DUNGEON_AND_TREASURE_HUNTS.md` §6.

**Open finding:** at game pin `107d7a86`, Battle Pyramids enforce a lifetime attempt cap (`maxAttempts` at most 100), so map cost alone cannot make a hunt unlimited. Design doc §2 lists the alternatives; the choice is the director's.

## RUL-2026-10-23-005 — Reward caches pay finished items; choice lives at hunt completion

**Date:** 2026-10-23

**Domain:** Rewards / caches / reward choice

**Status:** ACTIVE (direction; lines, rates and cache modes open)

**Supersedes:** the crafting-material contents of Medicine Inro, Shinobi Tool Pouch and Sage's Strongbox (push/97; RUL-2026-10-13-001 family scope stays) and their planned `w_B2` placement (RUL-2026-10-13-003).

**Ruling:** Reward caches drop **finished items, not the materials** for them. **Medicine Inro, Shinobi Tool Pouch and Sage's Strongbox are the exemplars for new item-reward setups**, following the live War Cache pattern (shared kit plus a signature line). The **"choose" option** is worked in at treasure-hunt completion, where players pick the cache that fits them.

**Evidence:** User, 2026-10-23: "we change medicine into and the other 2 to instead drop the items rather than the materials themselves"; "Medicine Inro, Shinobi Tool Pouch and Sage's Strongbox are exemplars for new item reward setups"; "Now we need good reward Caches that offer actual items ... Need to work the choose option into this. I had designed elemental kunai Caches for a war mission based on the ability to choose".

**Canonical destination:** `docs/design/SKYGLASS_DUNGEON_AND_TREASURE_HUNTS.md` §4–§5.
