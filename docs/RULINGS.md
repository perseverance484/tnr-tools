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
