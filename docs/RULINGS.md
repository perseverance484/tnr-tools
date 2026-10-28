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

**Amendment 2 (2026-10-23):** from round 2 the director favors R2-2, R2-4 and R2-6 but found the silhouette unclear; direction for round 3 is **the rising star** (a four-point star core with chakra wings swept upward into a chevron), the chevron **subtle** (user: "Subtler"). Prompt: `docs/handoffs/CHAKRA_OVERFLOW_ROUND3_SESSION_PROMPT.md`.

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

## RUL-2026-10-23-006 — Lane A approved: Forge dungeon recipe

**Date:** 2026-10-23

**Domain:** Forge / tooling (Lane A)

**Status:** ACTIVE

**Supersedes:** the in-game-editor option for building the Skyglass Wreck dungeon (design doc §8).

**Ruling:** Lane A tooling work is approved to build the dungeon: a scoped dungeon contract derived from the pinned game source, a Forge `dungeon` recipe with validation and read-back, the `validate.py` bridge, and tests, on a `fable/*` branch with independent ChatGPT review.

**Evidence:** User, 2026-10-23: "Lane A tooling work is approved for building the dungeon".

**Canonical destination:** `state/prompt_forge_dungeon_recipe.md` (the build contract).

**Boundary:** No live request; the reward-package recipe is a separate follow-up.

## RUL-2026-10-23-007 — Forge bundle budget raised to 435,000 raw / 105,000 gzip for the dungeon recipe

**Date:** 2026-10-23

**Domain:** Forge / bundle size budget

**Status:** ACTIVE

**Supersedes:** the 420,000 / 100,000 ceiling (RUL-2026-10-19-006).

**Ruling:** The Forge bundle ceiling is raised to **435,000 raw / 105,000 gzip** to carry the dungeon recipe (RUL-2026-10-23-006). Measured with the recipe: 425,490 raw / 102,323 gzip, from a base of 412,173 / 98,680. Trimming and whitespace minification were offered and declined.

**Evidence:** User, 2026-10-23, choosing "Raise to 435k / 105k (Recommended)" over "Trim to fit" and "Whitespace minify".

**Canonical destination:** `forge/tools/check_bundle_budget.mjs` (`BUDGET`).

## RUL-2026-10-23-008 — Jutsu icon overhaul: one batch; 15 of our reverted icons go back unchanged

**Date:** 2026-10-23

**Domain:** Art direction / jutsu icons

**Status:** ACTIVE (staff review open; rework not started)

**Supersedes:** the "one icon at a time" pacing stated with the push/227 revert

**Ruling:** After the push/227 revert, the director scored all 51 reverted icons and opened a staff review. The overhaul ships **all at once in one batch**, not one icon at a time. That batch also puts back, unchanged, our icons for all eight Blood-Enchanted Eyes jutsu (Unholy Enhancement included, although one staff member could not tell what it shows), all five Crystal Essence jutsu, Blazing Fang Strike and Celestial Dew. Reworked icons show no people; people renders are the Jutsu Masters' job.

**Evidence:** User, 2026-10-23: "No, we'll do it all at once."; Discord thread: "BEE, CE, Blazing fang strike and Celestial Dew are getting no changes"; "Are we removing the people from everything?" / "I *think* so. I do have a Jutsu Master for each offense for people renders"; on putting the no-change icons back in the batch and keeping Unholy Enhancement: "Yes to both, include them in the batch".

**Canonical destination:** `docs/design/icon_overhaul/ICON_SCORES.md`, `STAFF_FEEDBACK.md`, `BATCH_PLAN.md`.

**Amendment 1 (2026-10-24), roles:** the art director only makes the art (raw images). Claude Code handles everything else: processing, previews and sheets, export and preflight, text rewrites (drafted for the director's approval), and the batch manifest. User: "You're handling text rewrites, manifests, processing, etc. Art Director just makes the art". Recorded in `docs/handoffs/ICON_OVERHAUL_ART_DIRECTION.md`.

**Amendment 2 (2026-10-24), people:** the five jutsu where staff asked for people (Poisonous Senbon, Blast Shield, Decaying Touch, Ethereal Nexus, Crystal Sphere) each get a people and a no-people version for the director to compare; Crystal Sphere's no-people version is the kept icon. User: "Lets do a people vs no people version for those jutsu". The general no-people lean stands elsewhere until the director decides.

**Amendment 3 (2026-10-24), pilot first:** before the batch, exactly one icon is worked until it is the best premium pixel-art icon we can make, and the rest follow from it. Pilot: Tempest Cleave (director's choice). User: "I think we need to start with exactly one icon and just work it to death. Make it the best most fitting premium pixel art icon we can, and go from there." Project: `docs/design/icon_overhaul/tempest_cleave/PILOT.md`.

## RUL-2026-10-24-001 — Jutsu icons depict the move, not abstractions

**Date:** 2026-10-24

**Domain:** Art direction / jutsu icons

**Status:** SUSPENDED 2026-10-24 by RUL-2026-10-24-002 (abstract emblems for now; the question is open)

**Supersedes:** the "one bold emblem that is the ability's metaphor" direction used for the 2026-10 jutsu icon passes (for example the Chakra Overflow and starter briefs), for future jutsu icon work

**Ruling:** Jutsu icons depict the actual move: who does it, what they do, to whom, with what, at the moment it lands, taken from the jutsu's battle text and lore. Abstract emblems (energy swirls, bursts, orbs, halos) are not a subject. Visual design must pass a 45 px name test (a player can say what is happening), with a silhouette-first composition, one peak moment, concrete objects and bodies, big and few shapes, one line of action, and a dark simple background.

**Evidence:** User, 2026-10-24: "A big mistake we've made with all our icons is they are too abstract. They don't convey the move at all. They compress down to the same amorphous blobs at size. They need to depict the actual move, the lore, the actual thing being done. Visual design needs to be better."

**Canonical destination:** `docs/handoffs/ICON_OVERHAUL_ART_DIRECTION.md` section 2. People appear wherever the move needs them (director, 2026-10-24: "Confirmed, show people wherever the move needs them."), superseding the earlier no-people lean of RUL-2026-10-23-008.

## RUL-2026-10-24-002 — Icon overhaul: abstract emblems for now; visual design and processing decisions

**Date:** 2026-10-24

**Domain:** Art direction / jutsu icons; art tooling

**Status:** SUPERSEDED 2026-10-24 by RUL-2026-10-24-003 (direction); its C1–C3 decisions stand

**Supersedes:** suspends RUL-2026-10-24-001

**Ruling:** The 35 reworked icons are abstract emblems for now, designed to read at 45 px under the visual design rules of `docs/handoffs/ICON_OVERHAUL_ART_DIRECTION.md` section 2 (recognition test, distinct silhouettes per family, specific over generic, big and few shapes, dark simple backgrounds, one light and one glow). From the visual design deep dive: icons are authored at about 48–64 art pixels across and judged at 45 px (C1); a snap-to-grid and palette-quantise processing tool is to be built as Lane A tooling (C2); figure candidates use a dark figure backlit against the brightest energy (C3). C4 (raising the game's abstract icon prompt with the game team) is moot while abstract is the direction.

**Evidence:** User, 2026-10-24: "All approved. Abstract icons is up in the air. We'll do abstract for now"; asked whether this covered only the game's prompt or the rework too, the user chose "Our rework too".

**Canonical destination:** `docs/handoffs/ICON_OVERHAUL_ART_DIRECTION.md`; `docs/design/icon_overhaul/VISUAL_DESIGN_DEEP_DIVE.md`.

## RUL-2026-10-24-003 — Icon overhaul: premium upgrades of the originals, keeping the people

**Date:** 2026-10-24

**Domain:** Art direction / jutsu icons

**Status:** ACTIVE

**Supersedes:** RUL-2026-10-24-002's "abstract emblems for now" direction (its C1–C3 decisions on grid density, the pixelsnap tool and backlit figures stand) and RUL-2026-10-24-001

**Ruling:** Each reworked jutsu icon is a premium upgrade of its **original** icon: it keeps the people and the scene's identity, takes its colour palette from the original, and is rebuilt to read as an icon at thumbnail size (a clear silhouette, the figure large in the frame, a calm background, premium TNR pixel art). The visual design rules for size (45 px recognition, silhouette first, big and few shapes, dark simple background, one glow) still apply. Ethereal Rebirth is prepared next. The Tempest Cleave pilot (round 1 written from an older version without people) is open for the director to reconcile with this ruling.

**Evidence:** User, 2026-10-24: "I've identified the middle ground. We keep the people but make it read well as an icon at thumbnail size. give each a clear silhouette and color palette based on the original. This way players get to see their favorite skills with a premium upgrade AND our icons read well at size. Let's prepare ethereal rebirth next"

**Canonical destination:** `docs/design/icon_overhaul/ethereal_rebirth/PROJECT.md` (first project under this ruling); `docs/handoffs/ICON_OVERHAUL_ART_DIRECTION.md` (header note).

## RUL-2026-10-24-004 — Jutsu text and icon show the same moment

**Date:** 2026-10-24

**Domain:** Jutsu text / art direction

**Status:** ACTIVE

**Supersedes:** none (adds to RUL-2026-10-24-003)

**Ruling:** Reworked jutsu get premium text alongside their icon, and the two tie together: the battle line describes one key moment and the icon draws that moment; the description sums the jutsu up in the same images. Texts are drafted by Claude Code against the live effects and approved by the director; each jutsu's text and icon ship together in one suggestion. First pair: Tempest Cleave and Ethereal Rebirth (`docs/design/icon_overhaul/TEXT_AND_ICON_ROUND1.md`).

**Evidence:** User, 2026-10-24: "I want to look at upgrading both jutsu descriptions to be more premium, and I want our icons to show those descriptions in action. That should be the goal, they should clearly tie in to one another."

**Canonical destination:** `docs/design/icon_overhaul/TEXT_AND_ICON_ROUND1.md`; the Tempest Cleave and Ethereal Rebirth round-1 prompts.

**Amendment 1 (2026-10-24), Ethereal Rebirth is non-elemental:** its damage has element `None`, so neither its text nor its icon may show elements; the approved fire, water and lightning text is withdrawn and rewritten (`docs/design/icon_overhaul/ethereal_rebirth/TEXT_V2.md`). Text and icon must match the jutsu's actual element. User: "Old one was misaligned, this is a non-elemental attack so using elements is a no-go. We will rewrite its descriptions as well".

## RUL-2026-10-24-005 — Jutsu icons: no pixel conversion

**Date:** 2026-10-24

**Domain:** Art processing / jutsu icons

**Status:** ACTIVE

**Supersedes:** RUL-2026-10-24-002 C1 (48–64 art pixels across) and C2 (build and use the snap-and-quantise tool) for jutsu icons

**Ruling:** Approved jutsu icon raws are exported without pixel conversion: the raw is resized to 256 px and exported as lossless WebP, then checked with `artpreflight.py --type JUTSU_ICON`. The pixelsnap tool (`fable/pixel-art-snap`, frozen at b3382d71, never merged) is parked; it needs no review unless revived. Tested on Ethereal Rebirth round 1: snapping at 64, 96 or 128 art pixels across made the figure blocky and lost the face; at the full 256 grid it only reduced colours and flattened the face's shading; at 45 px every version looked the same.

**Evidence:** User, 2026-10-24: "I think we shouldn't convert at all. Looks too blocky. Unless you can get higher definition out of it". Sheets: `docs/design/icon_overhaul/ethereal_rebirth/round1_grid_density.png`, `round1_hd_test.png`.

**Canonical destination:** `docs/design/icon_overhaul/ethereal_rebirth/ROUND1_REVIEW.md`; the intake steps of the icon session prompts.

## RUL-2026-10-24-006 — Battle assets must not be hidden (law 16c corrected)

**Date:** 2026-10-24

**Domain:** Engine laws / game assets

**Status:** ACTIVE

**Supersedes:** law 16c as written 2026-08-26 ("gameAsset hidden affects listing only, never rendering")

**Ruling:** A hidden game asset does not play in battle. Every animation (and any other asset a battle uses) must end `hidden: false`. Creates still ship `hidden: true` (law 16b, enforced by lint L13 in Forge and validate.py), so each battle asset create is followed by an unhide edit with a literal `targetId`, built from the create's results bundle. Changing the gates so battle-asset creates may ship `hidden: false` directly would be Lane A tooling work and is not done here.

**Evidence:** User, 2026-10-24: "You keep putting animations as hidden which as you would expect... hides them during combat. So they dont play. Stop doing that, I have to manually unhide them each time." Source: `app/src/server/api/routers/misc.ts:660` (`fetchGameAssets` filters `hidden = false`), called via `misc.getAllGameAssetNames` from `app/src/layout/Combat.tsx:316`; `combat.ts:2206` filters the same way.

**Canonical destination:** `docs/ENGINE_LAWS.md` law 16c (corrected), with its hand-kept copies in `references/pipeline.md` (packs re-rendered), `producing-tnr-art/references/processing.md` and `12b_LAWS_coverage.md`; push/230 + push/232; push/226's generator.

## RUL-2026-10-24-007 — The Forbidden Master: one masked character for every Forbidden jutsu

**Date:** 2026-10-24

**Domain:** Art direction / jutsu icons / recurring characters

**Status:** ACTIVE (the character's design is open until the director approves a model sheet)

**Supersedes:** for jutsu of type FORBIDDEN only, RUL-2026-10-24-003's "keeps the people" of the original icon (the
Forbidden Master replaces each original's figure; palette and the moment still come from the original and the text,
RUL-2026-10-24-004). Pauses the Ethereal Rebirth round-4 icon prompt, which kept the white-haired warrior.

**Ruling:**
1. Our recurring characters wear **silhouetted ninja masks at all times**: the mask is the silhouette (it replaces the
   Weapon Master's shadowed void face with glowing eyes).
2. One character, the **Forbidden Master**, is used for **every Forbidden jutsu render**: intimidating, imposing, a
   talented and dangerous practitioner wielding top-tier forbidden arts.
3. **Identity reference:** the Tempest Cleave original's masked fighter (fox mask, dark segmented armour, white scarf,
   glowing eyes). **Rendering goal:** the Weapon Master renders. Same type of character as the Weapon Master, but masked.
4. The design is fixed by a model sheet the director approves before any Forbidden jutsu icon is drawn with it.

**Evidence:** User, 2026-10-24: "I want our characters to wear silhouetted ninja masks at all times. I want to define this
character as the forbidden jutsu master and the one we use for all forbidden jutsu renders. They need to be intimidating
and imposing, as they will be using all the top of the line forbidden level skills. Need to look like a talented and
dangerous practitioner. The tempest Cleave subject is the identity reference and the weapon Master is the rendering goal.
We want the same type of character but with a mask instead of a silhouette face. The mask is the silhouette now. Let's
make our forbidden master"

**Canonical destination:** `docs/design/characters/FORBIDDEN_MASTER.md` (character brief); references in
`art/characters/forbidden_master/refs/`; model-sheet prompt `docs/handoffs/FORBIDDEN_MASTER_MODEL_SHEET_SESSION_PROMPT.md`.

## RUL-2026-10-24-008 — Skyglass Wreck: access, availability, difficulty, placement

**Date:** 2026-10-24

**Domain:** Ghost Ship / Skyglass Wreck dungeon

**Status:** ACTIVE (floor roster to be confirmed by a hidden test run; exact sector and tile open)

**Supersedes:** none (refines RUL-2026-10-23-003)

**Ruling:**
1. **Party of exactly three**, as the game requires (`DUNGEON_PARTY_SIZE`); no request for 1–3 support. Solo players reach the hunts through traded maps.
2. **Permanent**: no event window (`expiresAt: null`).
3. **Two waves per floor**, the roster in `docs/design/SKYGLASS_DUNGEON_AND_TREASURE_HUNTS.md` §3, tuned by a test run while hidden. Enemies do not scale to the party and the ten crew AIs already sit at the JONIN caps, so enemy count and waves are the only difficulty levers.
4. **Placement: a sector near Wake Island** (222). PvP can no longer be switched off there (director, 2026-10-24); the earlier note offering that is withdrawn.

**Evidence:** User, 2026-10-24: "Accept 3-only", "Permanent", "Two waves per floor", "We'll put it in a sector near Wake Island. Pvp can't be turned off there anymore btw".

**Canonical destination:** `docs/design/SKYGLASS_DUNGEON_AND_TREASURE_HUNTS.md` §3.

## RUL-2026-10-24-009 — Skyglass Wreck payout split, chest trade, map rates and names

**Date:** 2026-10-24

**Domain:** Ghost Ship / Skyglass Wreck rewards

**Status:** ACTIVE. Map rates, split, chest trade and map names are ruled. The other chest lines and the completion amounts are the presented proposal, not objected to; they stay tunable until the content manifest is reviewed.

**Supersedes:** the Skyglass Signal Beacon's "10% per Ghost Ship clear" source (RUL-2026-10-16-010) for the Silent Bastion's map, which now drops from the chest at 6%.

**Ruling:**
1. **Split payout:** exp, tokens and prestige on completion to each player; ryo and items in the chest.
2. **The chest is not tradable.** One per player per clear.
3. **Map lines in the chest:** Drowned Foundry **12%**, Quarantine Vault **6%**, Silent Bastion **6%**, Skyglass Expedition **3%**, each an independent line on top of the regular loot.
4. **Map names:** "Chart of the …" (Chart of the Drowned Foundry, Chart of the Quarantine Vault, Chart of the Silent Bastion, Chart of the Skyglass Expedition).

Presented with it (proposal): completion 15,000 exp / 1,000 tokens / 1,000 prestige; chest guaranteed 50,000 ryo and Skyglass Serum ×2; supplies, valuables, caches and a 1% Lion Token as in the design doc §4. Maps are OTHER items, tradable, stackable, consumed at hunt start; rarity Foundry RARE, Vault and Bastion EPIC, Expedition LEGENDARY.

**Evidence:** User, 2026-10-24: "Split", "12 / 6 / 6 / 3", "Not tradable", "Chart of the …".

**Canonical destination:** `docs/design/SKYGLASS_DUNGEON_AND_TREASURE_HUNTS.md` §4.

## RUL-2026-10-24-010 — Treasure hunts: Silent Bastion whole with its Beacon; Foundry losses retry; event-wide loot review

**Date:** 2026-10-24

**Domain:** Ghost Ship / Skyglass treasure hunts

**Status:** ACTIVE. Hunt outlines for Foundry, Vault and Expedition are the presented proposals (design doc §6); rewards are under review.

**Supersedes:** the "cut Bastion to one or two divisions" hunt format (RUL-2026-10-23-004, design doc §6) and the "Chart of the Silent Bastion" name (RUL-2026-10-24-009 item 4) for Bastion only.

**Ruling:**
1. **Silent Bastion ships whole**: the authored 99-node, 20-AI design on `claude/silent-bastion-authoring-69za5u@6271e1f` (RUL-2026-10-15-001, RUL-2026-10-16-*).
2. **Its entry item stays the Skyglass Signal Beacon**, which takes the Bastion map line in the Skyglass Wreck chest (6%). The other three maps keep "Chart of the …".
3. **Drowned Foundry:** a lost fight on the way down is retried (the Pyramid retry); greed costs time, never the haul.
4. **Rewards for the whole event are reviewed together**, built on the game's weighted caches and reward packages; Bastion's Arsenal/Research ingredient caches are decided in that review.

**Evidence:** User, 2026-10-24: "Keep it whole", "Keep the Beacon", "Retry, keep the haul", "We need to review loot tables and rewards for the entire event. There are reward packages and Caches in the game now."

**Canonical destination:** `docs/design/SKYGLASS_DUNGEON_AND_TREASURE_HUNTS.md` §6.

## RUL-2026-10-24-011 — Event reward structure: hybrid chest, weighted caches, pick 1 of 4

**Date:** 2026-10-24

**Domain:** Ghost Ship / Skyglass rewards

**Status:** ACTIVE (structure). Every line, tier weight, quantity and package content is a proposal under review (`docs/design/SKYGLASS_LOOT_TABLES.md`).

**Supersedes:** the standard-only chest table (RUL-2026-10-24-009 presentation); Silent Bastion's Arsenal and Research ingredient caches (RUL-2026-10-16-001/-010) are dropped.

**Ruling:**
1. **The Wreck chest is a hybrid item**: a standard part (guaranteed ryo, the map and Beacon bonus lines, Lion Token) and a weighted part (two salvage rolls).
2. **Medicine Inro, Shinobi Tool Pouch and Sage's Strongbox are weighted caches of finished items.**
3. **Every hunt's completion is a pick of 1 from 4 reward-package cards**: three universal hauls plus that hunt's own card.
4. **Silent Bastion's ingredient caches are dropped**; its own card is a finished-item haul like the others.

**Evidence:** User, 2026-10-24: "Hybrid", "1 of 4", "Drop them" (Bastion's ingredient caches), "Weighted".

**Canonical destination:** `docs/design/SKYGLASS_LOOT_TABLES.md`.

## RUL-2026-10-24-012 — Elemental Tool Pouches, cache-only salvage, War Caches dropped

**Date:** 2026-10-24

**Domain:** Ghost Ship / Skyglass rewards

**Status:** ACTIVE (structure). Pouch contents, the salvage weights and every quantity stay proposals (`docs/design/SKYGLASS_LOOT_TABLES.md`). The hunt that offers the pouches is read as the Silent Bastion; confirm.

**Supersedes:** the single Shinobi Tool Pouch and the "Shinobi's Haul" card (RUL-2026-10-24-011 item 3: picks are no longer a uniform 1 of 4); the supply and valuables salvage tiers in the chest; the five elemental War Caches as the source of elemental kunai.

**Ruling:**
1. **Five elemental Tool Pouches** (Katon, Wave, Ikazuchi, Stonefall, Zephyrfang), one element each plus shared tools. They **drop only from one hunt**, whose completion pick offers all five so each player takes their own element. Every other hunt's pick drops the Shinobi card.
2. **The elemental War Caches are dropped**; the pouches replace them. Retirement mechanism and timing are the director's; no captured quest pays them.
3. **The chest's salvage rolls give caches only** (Medicine Inro, Ornate Chest, Sage's Strongbox), which resolve into items when opened. The supply and valuables bundles leave the chest.

**Evidence:** User, 2026-10-24: "Let's do 4. Then that specific hunt has a choice of 5 kunai pouches. We'll drop the elemental kunai Caches. And the shinobi tool pouches only drop from that hunt, so players can choose the one they want. Also, remove the excessive salvage drops from the initial Skyglass salvage cache. Allow the items it drops to resolve that, like medicine inro".

**Canonical destination:** `docs/design/SKYGLASS_LOOT_TABLES.md`.

## RUL-2026-10-24-013 — Sage's Strongbox and cache quantities

**Date:** 2026-10-24

**Domain:** Ghost Ship / Skyglass rewards

**Status:** ACTIVE. Tier weights remain proposals; contents of uncaptured items (Solider Pill, Enemy Pill, Mona's Mermaid Song, Saki, Senbon Needles, Paper Bombs, Pill Pack) are confirmed by capture before the manifest.

**Ruling:**
1. **Cache stacks are ×10**, except **Pill Pack ×5** and jutsu scrolls ×1; this covers the Medicine Inro, Sage's Strongbox and the five elemental pouches.
2. **Store-bought items sit in a cache's Common tier**, except Dr. Kim's Miracle Potion (Rare). Chakra Pill II and Stamina Pill II are Epic, Panacea Rare, Pill Pack Legendary. Energy Potion and Full Potion are not in the Inro.
3. **Sage's Strongbox**: one roll; Common (shop) Dr. Kim Disaster Potion, Chakra Disrupting Needles; Epic Infernum, Bashōsen, Dr. Kim's Poison Potion; Legendary Pill Pack, Solider Pill, Enemy Pill, Mona's Mermaid Song; jackpot the two Forbidden Jutsu Scrolls.
4. **Infernum and Bashōsen move from the pouches to the Strongbox.**

**Evidence:** User, 2026-10-24: "Chakra Pill II and Stamina Pill II should be Epic. Panacea should be rate. Pill pack should be legendary."; "Store bought items should be in the common tier except for dr. Kims pink which should be rare"; "X10 for everything but pill pack which is x5."; "Forbidden scrolls", "Move to Strongbox", "1 roll", "Yes, ×10 everywhere".

**Canonical destination:** `docs/design/SKYGLASS_LOOT_TABLES.md` §3.

**Amendment (2026-10-24):** Sage's Strongbox stacks follow its tiers: **Common ×20, Epic ×10, Legendary ×5, Forbidden ×1** (user: "Do x20 common, x10 epic, x5 legendary and x1 forbidden"). The Medicine Inro and pouches keep item 1's ×10 / Pill Pack ×5.

**Amendment (2026-10-24):** each elemental pouch adds its element's kunai **×20 in Rare** and **×30 in Epic**, beside the ×10 guarantee and the ×10 Common entry (user: "Put a x20 roll in rare and a x30 roll in epic of the kunai for the kunai pouches").

## RUL-2026-10-24-014 — Skyglass Coffer replaces the Ornate Chest; hunts lose unique drops; Armory Requisition

**Date:** 2026-10-24

**Domain:** Ghost Ship / Skyglass rewards

**Status:** ACTIVE (structure). Coffer contents, ending payouts and quantities are proposals (`docs/design/SKYGLASS_LOOT_TABLES.md`).

**Supersedes:** "Katana and Crown fragment are Expedition-only" (RUL-2026-10-23-004); the Expedition's bespoke ending lines; the Foundry and Vault signature cards and the Bastion's five pouch cards (RUL-2026-10-24-012 item 1, the 1-of-7 pick); the Ornate Chest's place in the event.

**Ruling:**
1. **Skyglass Coffer**, a new chest, **replaces the Ornate Chest** in the event and is the **only home of Skyglass loot**: Serum, Filament, Reliquary, Crown fragment, Crystal and the **Skyglass Katana**. It drops from the Wreck's salvage rolls and from hunt endings.
2. **No hunt has unique drops.** Hunts pay ryo, exp and Coffers or caches by ending; they differ by mechanic. The Skyglass Expedition is converted to this system.
3. **Every hunt's pick is 1 of 3: Medic's Haul, Sage's Haul, Skyglass Coffer.** The Silent Bastion swaps the Coffer for the **Armory Requisition**, a tradable token whose use starts a one-node Special quest ending in a pick of 1 of 5 elemental pouches (`noncombatquest` item effect; Special quests take no completion caps). Pouches stay Bastion-only.

**Evidence:** User, 2026-10-24: "I think we should do away with the skyglass expedition having its own unique drops ... the silent Bastion shouldn't have 7 choices ... I think we should make a new chest instead of the ornate chest"; then "In the Coffer", "Requisition token", "Same three everywhere", "Skyglass Coffer".

**Canonical destination:** `docs/design/SKYGLASS_LOOT_TABLES.md`.

## RUL-2026-10-24-015 — No salvage chest; Wreck clear rolls drops directly; Coffer holds no Reliquary; rebalance

**Date:** 2026-10-24

**Domain:** Ghost Ship / Skyglass rewards

**Status:** ACTIVE (structure). The rebalanced rates on `docs/design/SKYGLASS_LOOT_TABLES.md` are a proposal; the map rates of RUL-2026-10-24-009 stand.

**Supersedes:** the Wreck chest (RUL-2026-10-23-003 "exactly one treasure chest", RUL-2026-10-24-009 items 2 and the chest table, RUL-2026-10-24-011 item 1, RUL-2026-10-24-012 item 3); the Skyglass Reliquary as Coffer content (RUL-2026-10-24-014 item 1).

**Ruling:**
1. **No salvage chest.** A Wreck clear pays its rolls directly as dungeon completion drops, each rolled by every member: ryo on completion, caches, maps and the Beacon as independent drop lines.
2. **The Skyglass Coffer does not contain the Skyglass Reliquary**: a chest that yields a chest defeats the purpose.
3. **Rates were too rewarding**: everything is rebalanced down (proposal on the loot tables page).

**Evidence:** User, 2026-10-24: "Your drop rates are too rewarding and not balanced in some cases. The salvage chest can be done away with, just give players the rolls for clearing the dungeon. Skyglass Coffer giving Skyglass Reliquary defeats the purpose."

**Canonical destination:** `docs/design/SKYGLASS_LOOT_TABLES.md`.

## RUL-2026-10-24-016 — Ryo and exp paid only on completion

**Date:** 2026-10-24

**Domain:** Ghost Ship / Skyglass rewards

**Status:** ACTIVE. The balance pass that accompanies it is a proposal for review. Where a hunt's endings paid different amounts (Foundry 25k/50k/100k, Expedition 25k–75k), the top ending's amount was carried to completion.

**Supersedes:** ryo and exp on hunt endings; the Coffer's guaranteed ryo; an earlier request about per-ending picks (withdrawn: "it's fine").

**Ruling:** **Ryo and exp are paid only on completion**: removed from every other node, amounts not otherwise adjusted. Hunt endings pay items only.

**Engine note:** in a `choose` quest, completion ryo and exp become pick cards of their own (`buildRewardChoiceCards`), so a fixed completion payout is carried inside each pick card (a reward package per card); every player receives it whatever they pick. The choose offer is built only from the quest-level reward, so per-ending picks would need a token per ending (Requisition pattern).

**Evidence:** User, 2026-10-24: "OK, you know what, it's fine. Do one more balance pass of the drop rates and show them to me for review. Exp and ryo only paid on completion, just remove the rewards from the other nodes and dont adjust numbers".

**Canonical destination:** `docs/design/SKYGLASS_LOOT_TABLES.md`.

## RUL-2026-10-24-017 — One reward ladder for every hunt ending

**Date:** 2026-10-24

**Domain:** Ghost Ship / Skyglass rewards

**Status:** ACTIVE.

**Supersedes:** the per-ending cache assignments of RUL-2026-10-24-016's balance pass.

**Ruling:** Every ending in every hunt pays from one six-step ladder, chosen by its **final opponent and gating**; a higher step always pays more and no two Expedition endings pay the same.

| Step | Pays | Endings |
|---|---|---|
| I | Medicine Inro | Expedition w_B1 accessible hold; Foundry leave after fight 1 |
| II | Medicine Inro + Sage's Strongbox 50% | Expedition w_A buried shore cache |
| III | Sage's Strongbox | Expedition w_B2 restricted vault; Foundry leave after fight 2; Vault alarm tripped |
| IV | Sage's Strongbox + Skyglass Coffer 50% | Expedition w_C direct Captain |
| V | Skyglass Coffer + Sage's Strongbox | Expedition w_secret (Sealwright); Foundry Warden; Vault clean run |
| VI | Skyglass Coffer ×2 | Expedition w_Co (Crowned Captain); Silent Bastion (Arakane) |

**Evidence:** User, 2026-10-24: "Endings in the Skyglass Expedition having the same drops defeats the purpose of them. Accessible crates is a quick finish compared to the buried cache yet they pay the same. The sealwright fight and direct captain fight having the same drops defeats the purpose of them."; then "Yes, apply that ladder." Route data from the push/98 capture: every regular Expedition route is 3 fights; w_secret and w_Co are 2 fights behind a puzzle.

**Canonical destination:** `docs/design/SKYGLASS_LOOT_TABLES.md` §4.

## RUL-2026-10-24-018 — Exp ladder 1,000 to 5,000; pouch swap; packages from the catalog

**Date:** 2026-10-24

**Domain:** Ghost Ship / Skyglass rewards

**Status:** ACTIVE. The Wreck clear's exp step is read as the cap (its boss is the Crowned Captain); confirm.

**Supersedes:** hunt exp on completion and the Wreck clear's 15,000 exp (RUL-2026-10-24-009 / -016); exp moves onto the ending ladder (RUL-2026-10-24-017), so exp varies by ending; ryo stays on completion inside the pick cards.

**Ruling:**
1. **Exp is capped at 5,000 with 1,000 the low end.** Ladder steps pay I 1,000, II 2,000, III 3,000, IV 4,000, V 5,000, VI 5,000 exp. A Wreck clear pays 5,000 exp. Ryo, tokens and prestige are not changed by this ruling.
2. **Elemental pouches:** Venom Cask moves to Common and Elite Smoke Bomb to Rare.
3. **Ending rewards use the game's existing reward packages where they fit**, new ones proposed only for gaps. The director supplies the catalog from Manual → Rewards; `rewardPackages.getCatalog` is not in Forge's audited procedures.

**Evidence:** User, 2026-10-24: "Swap venom cask and smoke bomb in shinobi tool pouch."; "There are reward packages already made we can use for the ending rewards. Lets examine and use those, or perhaps propose our own. The reward amounts are a bit excessive. 5,000 should be the cap. 1,000 being the low end. 1/2/3/4/5000 should be the ladder."; then "Hunt and Wreck exp", "VI also pays 5,000", "I'll paste or screenshot".

**Canonical destination:** `docs/design/SKYGLASS_LOOT_TABLES.md`.

## RUL-2026-10-24-019 — Reward amounts are set by the director in game; content design begins

**Date:** 2026-10-24

**Domain:** Ghost Ship / Skyglass rewards and content

**Status:** ACTIVE.

**Ruling:** The director sets the reward amounts himself in the in-game editor from the game's reward-package catalog (content-type × rank packages such as S-Rank Dungeons Level 100 and S-Rank Battle Pyramid Level 100). `docs/design/SKYGLASS_LOOT_TABLES.md` is the map of where each reward goes (ladder steps, pick cards, caches, drops); its currency figures are guidance, not values to enforce. Manifests leave currency fields to the director unless he supplies values. Work moves to content design.

**Evidence:** User, 2026-10-24 (with screenshots of the Manual → Rewards catalog): "Tell you what, I'll set the rewards myself since its so easy to do. You've got them mapped out. Now we need to design the content".

**Canonical destination:** `docs/design/SKYGLASS_LOOT_TABLES.md` (status line) and this ruling.

## RUL-2026-10-24-020 — The Skyglass Expedition is dropped; its content is borrowed by the hunts

**Date:** 2026-10-24

**Domain:** Ghost Ship / Skyglass content

**Status:** ACTIVE.

**Supersedes:** the Skyglass Expedition hunt and its Chart (RUL-2026-10-23-004 slate, RUL-2026-10-24-009 3% map line, RUL-2026-10-24-017 Expedition ladder rows); the Archivist as the Vault's boss.

**Ruling:**
1. **No Skyglass Expedition hunt.** The original 83-node quest is not rebuilt; its scenes, dialog, puzzles and AIs are borrowed.
2. **The Quarantine Vault becomes "The Quarantined Archive"**, borrowing the Expedition's secret route (Lower Hull, Core Horror, Reconstruction Chamber seal puzzle, Quarantined Archive records) with the **Sealwright** as its boss; two more seals reuse the Oathkeeper's time riddle and the Wayfinder's charts.
3. **The Drowned Foundry moves aboard the wreck** (the keel works), borrowing the Exterior Keel Walk, Lower Hull and Hold scenes; the Foundry Warden stays its one new boss.
4. **The Skyglass Wreck** borrows the crew, the lore (in its description) and the Crowned Captain; a dungeon shows no scenes or dialog.
5. **At least one more hunt** is designed from the remaining assets (Deck, Chart Room, Helm, Command Observation Gallery, Cache Site, the Captain and Oathkeeper portraits).

**Evidence:** User, 2026-10-24: "Why dont we forego the skyglass expedition. The hunt structure of these is better. Let's just borrow what content we need. The skyglass wreck dungeon can use some of the scenes and dialog/art perhaps?"; then "This works. And we can design at least 1 more hunt with the assets remaining".

**Canonical destination:** `docs/design/SKYGLASS_DUNGEON_AND_TREASURE_HUNTS.md` §6.

## RUL-2026-10-24-021 — The Captain's Watch; final map lines

**Date:** 2026-10-24

**Domain:** Ghost Ship / Skyglass content and rewards

**Status:** ACTIVE.

**Supersedes:** the map lines of RUL-2026-10-24-009 item 3 (Expedition and Vault charts, Beacon 6%).

**Ruling:**
1. **The Captain's Watch** is the third designed hunt: Chart Room, Deck, Helm and Command Observation Gallery, landing at the Cache Site; fights Wayfinder, First Blade, The Captain; the Oathkeeper as keeper of the wager. **Wager ladder:** before each fight the player may accept a term (start that fight with a debuff); no terms pays step IV, one or two step V, all three step VI. A lost fight is retried with the same terms.
2. **Wreck clear map lines:** Chart of the Drowned Foundry **12%**, Chart of the Quarantined Archive **6%**, Chart of the Captain's Watch **6%**, Skyglass Signal Beacon **3%**.

**Evidence:** User, 2026-10-24: "This works. And we can design at least 1 more hunt with the assets remaining"; then, on the Watch proposal with Watch 3% / Beacon 6%: "Swap watch and beacon".

**Canonical destination:** `docs/design/SKYGLASS_LOOT_TABLES.md`; hunt designs in `docs/design/SKYGLASS_DUNGEON_AND_TREASURE_HUNTS.md` §6.

## RUL-2026-10-24-022 — Skyglass Wreck map structure art

**Date:** 2026-10-24

**Domain:** Ghost Ship / Skyglass art direction

**Status:** ACTIVE.

**Ruling:** The Skyglass Wreck dungeon entrance uses the **Beached wreck** structure sprite (concept 1): the ghost ship heeled over on a sand-and-rock spit with the cracked Skyglass Core half-buried beside the hull.

**Evidence:** User, 2026-10-24, after the three-concept review sheet (Beached, Hovering, Rising): "Beached".

**Canonical destination:** `art/ghost_ship_skyglass/structure/` (README, raw, export, hashes).

## RUL-2026-10-24-023 — Skyglass Wreck entrance placement

**Date:** 2026-10-24

**Domain:** Ghost Ship / Skyglass content

**Status:** ACTIVE.

**Supersedes:** the candidate sectors (221, 223, 294) in RUL-2026-10-24-008's placement note.

**Ruling:** The Skyglass Wreck dungeon entrance is at **sector 210, longitude 15, latitude 6**, using the "Skyglass Wreck" structure artwork at entrance size multiplier **5**, battle background **default**, no expiration, unpublished until release. Name "Skyglass Wreck"; description is the short version supplied 2026-10-24.

**Evidence:** User, 2026-10-24, screenshot of the dungeon editor (preview, name, artwork, multiplier 5, sector 210, longitude 15, latitude 6): "This is the information needed to set the ships spawn location, size, etc for the dungeon entrance when making the manifest you'll need this."

**Canonical destination:** `docs/design/SKYGLASS_DUNGEON_AND_TREASURE_HUNTS.md` §3 Placement.

## RUL-2026-10-24-024 — Old Ghost Ship chests become relics

**Date:** 2026-10-24

**Domain:** Ghost Ship / Skyglass rewards

**Status:** ACTIVE.

**Ruling:** The Skyglass Reliquary and every other old Ghost Ship chest are relics: no new content drops or references them. They are not edited, hidden or deleted, so unopened copies in player inventories still work.

**Evidence:** User, 2026-10-24: "The skyglass reliquary and all the other old chests will just be relics. We won't use them anymore. But we'll leave them be in case players have unopened ones."

**Clarification (2026-10-24):** the Mystery Chest is one of these retired chests; its drop lines (including 10% Reliquary) are left untouched. User: "Mystery chest drops dont matter its a retired item alongside skyglass reliquary."

**Canonical destination:** `docs/design/SKYGLASS_LOOT_TABLES.md` open items (Reliquary closed).

## RUL-2026-10-24-025 — Skyglass Wreck: five floors, more waves

**Date:** 2026-10-24

**Domain:** Ghost Ship / Skyglass content

**Status:** ACTIVE.

**Supersedes:** the two-tier, ten-floor, two-waves-per-floor shape of RUL-2026-10-24-008.

**Ruling:** The Skyglass Wreck is one tier of five floors (floor 5 the boss), with three to five waves per floor. Each floor's elite or boss arrives in its last wave; Seal Charges and Core Canisters never spawn without a real enemy in the same wave; wave delays are 0 between add waves and 1 before an elite or boss wave.

**Evidence:** User, 2026-10-24: "Make sure we decide how many rounds between reinforcements. Also, enemies will probably need more health or we need to spawn bosses in last or something."; "Seal Charges and Core Cannisters shouldn't appear on their own. They are extra enemies/hazards, not threats on their own."; "Make it 5 floors but increase the number of waves instead".

**Canonical destination:** `docs/design/SKYGLASS_DUNGEON_AND_TREASURE_HUNTS.md` §3.

## RUL-2026-10-24-026 — The Charts are maps of the wreck itself

**Date:** 2026-10-24

**Domain:** Ghost Ship / Skyglass lore and art direction

**Status:** ACTIVE.

**Ruling:** The three hunt Charts are charts of the Skyglass wreck's own interior, not maps of outside places. The ship's layout is always shifting, but charts of parts of its interior sometimes turn up: the keel and lower decks (Drowned Foundry), a sealed chamber amidships (Quarantined Archive) and the upper command decks (Captain's Watch). Chart icons show a side-on plan of the ship with that section picked out in skyglass ink; item descriptions follow.

**Evidence:** User, 2026-10-24: "Have decided to make the charts like maps of the wreck itself. The ships layout is always changing but sometimes charts mapping its interior can be found."

**Canonical destination:** `docs/handoffs/SKYGLASS_EVENT_ITEM_ICONS_ART_REQUEST.md` §7-9; descriptions in push/254 (on hold).

## RUL-2026-10-25-001 — Forge suggest mode may send new records (Lane A approved)

**Date:** 2026-10-25

**Domain:** Forge / content review

**Status:** ACTIVE.

**Ruling:** Forge's suggest mode is extended to send new records to the game's review desk as CREATE suggestions (the desk already accepts `entityId: null`). AI creates and quests stay refused, and a suggested create that another item in the same manifest references is refused. Built on `fable/forge-suggest-create` under Lane A with independent review. push/254 (the Skyglass event items) goes in as suggestions once this ships.

**Evidence:** User, 2026-10-25, choosing between creating hidden then releasing by suggestion, or adding new-record suggestions to Forge: "2".

**Canonical destination:** `state/prompt_forge_suggest_create.md`; implementation on `fable/forge-suggest-create`.

## RUL-2026-10-25-002 — Headless Rider is level 110; quest maxLevel 110 stands

**Date:** 2026-10-25

**Domain:** Halloween / Headless Rider Horror! (`0lNDtE_VYJOCy8JZQI_sI`)

**Status:** ACTIVE.

**Ruling:** The Headless Rider boss is level 110, fought in a new `start_battle` before the quest's `win_quest`. Upstream raised the player level cap: `MAX_PLAYER_LEVEL = 110` and quest `maxLevel` is bounded by it (TheNinjaRPG `f381b7f`, `app/drizzle/constants.ts:203`, `app/src/validators/objectives.ts:905`), and only `ELITE JONIN` carries `LVL_CAP: MAX_PLAYER_LEVEL` with the max stat caps, so the rider is written at that rank. The live quest already holds `maxLevel: 110`. validate.py law 8 (cap 100) is stale against that source; push/256 runs under the recorded exception `state/headless_rider_battle_validate_exception.json` until the pinned contracts are re-extracted.

**Evidence:** User, 2026-10-25: "Level 110. We'll need to make the rider, his rules and the battle node." Capture `harvests/inbox/tnr_results_1792954275867.json`.

**Canonical destination:** `push/256_headless_rider_battle.json`.

## RUL-2026-10-25-002 — Skyglass reward restructure: one home per item, a pick per hunt

**Date:** 2026-10-25

**Domain:** Ghost Ship / Skyglass rewards

**Status:** ACTIVE (structure). Quantities, currency amounts, the badge and the jutsu are open.

**Supersedes:** the shared hunt pick (Medic's Haul / Sage's Haul / Coffer) and the Armory Requisition of RUL-2026-10-24-014; the caches on the reward ladder (RUL-2026-10-24-017, the exp ladder itself stays); the Wreck's Inro, Strongbox, Coffer and Lion Token drop lines (RUL-2026-10-24-015/-021, map lines unchanged).

**Ruling:**
1. **One home per item.** A reward appears in more than one source only as the same container. Skyglass items come only from the Skyglass Coffer, which becomes pure Skyglass (its jewels, gold and unobtanium move to the Crew Footlocker). Pill Pack leaves the Strongbox; Chakra Disrupting Needles leave the Tool Pouches.
2. **Wreck:** currency package, the four map lines, and the **Crew Footlocker at 3%**.
3. **Crew Footlocker** (new, premium valuables: Rare Jewels / Imperial Gold / Unobtanium) drops at **3%** on the Wreck clear and on every hunt ending.
4. **Each hunt is an isolated Battle Pyramid with its own completion pick:** Foundry - the five Tool Pouches; Archive - **Archive Chart Case** (new; one roll: Foundry 60 / Archive 25 / Watch 12 / Beacon 3), Sage's Strongbox, The Records (exp); Captain's Watch - Skyglass Coffer, Captain's Purse (ryo), Medicine Inro; Silent Bastion - Skyglass Coffer ×2, Bastion's Honor (village tokens), a **Bastion badge** and a **Bastion jutsu** (take-once picks, so two clears are needed for both).
5. Hunt endings pay the exp ladder, currency and the Footlocker chance; no caches.
6. **Shelved:** the Armory Requisition and its Special quest; the Lion Token.

**Evidence:** User, 2026-10-25: "the wreck should have generic rewards and then the chance to drop the treasure maps ... each hunt is an isolated battle pyramid with the choose nodes"; "reward overlap ... a lot of Skyglass items outside the Skyglass Coffer"; "the footlocker ... a rare drop only on completion of the Wreck or any hunt. Lets say 3% chance"; "adding a chest that drops from the archives that can roll the charts ... move medicine inro to Bastion and drop the lions tokens"; "drop captains commendation for medicine inro"; "We'll keep your weights"; "Let's do both the badge and the jutsu ... repeat runs can net them skyglass coffers or the bastion honor node".

**Canonical destination:** `docs/design/SKYGLASS_LOOT_TABLES.md`.

## RUL-2026-10-25-003 — The premium valuables chest is the Sealed Treasury

**Date:** 2026-10-25

**Domain:** Ghost Ship / Skyglass rewards

**Status:** ACTIVE.

**Ruling:** The 3% premium chest of RUL-2026-10-25-002 (Rare Jewels / Imperial Gold / Unobtanium) is named **Sealed Treasury** (was "Crew Footlocker").

**Evidence:** User, 2026-10-25: "Crew Footlocker is a pretty lackluster name for a rare drop with even rarer items"; then, from the proposed names: "Sealed Treasury".

**Canonical destination:** `docs/design/SKYGLASS_LOOT_TABLES.md`.

## RUL-2026-10-25-004 — Skyglass balance pass

**Date:** 2026-10-25

**Domain:** Ghost Ship / Skyglass rewards and hunts

**Status:** ACTIVE.

**Supersedes:** the Coffer's Legendary tier (Katana or Crystal, 1%) and the Treasury's flat 3% on hunt endings (RUL-2026-10-25-002 items 1 and 3); the Drowned Foundry's leave-early endings (hunt content draft).

**Ruling:**
1. **Drowned Foundry** is always fought to the Foundry Warden: the two leave-early endings are removed (they paid the same completion pick as a full clear). Ladder step V.
2. **Skyglass Coffer Legendary tier is the Skyglass Katana alone at 2%** (Common drops to 69). The Skyglass Crystal leaves the Coffer and comes only from crafting 12 Filaments, which the director confirms is live.
3. The Sealwright's doubled health (push/252) also makes the Quarantined Archive's solo final fight harder; **accepted**.
4. **Sealed Treasury on hunt endings scales with the ladder: 1% per step** (I 1% … VI 6%), on every hunt's endings. The Wreck clear stays 3%.
5. **Captain's Watch pick: Medicine Inro ×3.** Bastion's Honor's token amount must be large enough to compete with Coffer ×2 (director sets it).
6. **Sealed Treasury contents:** **100,000 ryo** every opening (standard reward effect) plus one weighted roll: Rare Jewels ×10 (70) / Imperial Gold ×5 (24) / Unobtanium ×5 (6).

**Open:** the `battlepyramid` lifetime attempt cap (at most 100 runs per player per hunt): accept, switch hunts to special quests, or ask the game owner.

**Evidence:** User, 2026-10-25, on the final review: "1. Approved. 2. Approved. 3. Accept the harder archive 4. Approved. Do this for all scaling endings. 1% drop rate of the treasury per stage on completion. 5. Approved and noted. 6. Approved. Add 100,000 ryo to the chest as well. Filament crafting is live and works."

**Canonical destination:** `docs/design/SKYGLASS_LOOT_TABLES.md`; `docs/design/SKYGLASS_HUNTS_CONTENT.md` (Foundry).

## RUL-2026-10-25-005 — The pinnacle hunt is Crownhold; its key is the Lastlight

**Date:** 2026-10-25

**Domain:** Ghost Ship / Skyglass lore and naming

**Status:** ACTIVE.

**Supersedes:** the names "Silent Bastion" (the hunt) and "Skyglass Signal Beacon" (its entry item) everywhere in the event; the item's icon is unchanged.

**Ruling:** The pinnacle hunt is **Crownhold**: the fortress the Skyglass Project was commanded from, seat of the Crown, source of the last directive the ship still obeys; Supreme Commander Arakane holds it. Its entry item is the **Lastlight**: Crownhold's final signal caught in a skyglass lantern, still burning with that order; following it leads home to Crownhold. Story: Crownhold went dark, but its Lastlight kept burning, and the wreck's afterimages still obey it. Derived names: Crownhold's Honor (village-token pick), Crownhold badge, Crownhold jutsu.

**Evidence:** User, 2026-10-25: "Need a better name for Silent Bastion"; "I want to be short, on theme and really pop"; "Crownhold and Lastlight are good... any way we can tie the theme of the entire thing into the name and the item that unlocks it?"; then "Perfect. Approved both renames".

**Canonical destination:** `docs/design/SKYGLASS_LOOT_TABLES.md`, `docs/design/SKYGLASS_DUNGEON_AND_TREASURE_HUNTS.md`; item name and draft description in push/254 (on hold).

## RUL-2026-10-25-006 — Lastlight, the Crownhold jutsu

**Date:** 2026-10-25

**Domain:** Ghost Ship / Skyglass rewards; jutsu

**Status:** ACTIVE (spec). Costs and art open.

**Ruling:** Crownhold's take-once jutsu pick is **Lastlight**: an EVENT jutsu, **PvE only** (`battleUsageType: PVE`), no element, line attack (AOE_LINE_SHOOT), cooldown **8**. Effects scale **0.4 per level** and start 10 below their targets so they reach them at level 25: damage 40 (→50), wound 20 (→30%) for **2 rounds**, decreaseheal 30 (→40%) for **3 rounds**.

**Evidence:** User, 2026-10-25: "I like it as Lastlight, a line nuke that does 50 damage, 30% wound and 40% heal cut. PvE only though. Dont wanna upset the balance of PvP"; then "Cooldown 8, wound 2 rounds, heal cut 3 rounds, element none, jutsu type event. Scaling will be .4 per level so we need to take 10 off every value so that it can scale to the proposed values at max level."

**Canonical destination:** `docs/design/CROWNHOLD_LASTLIGHT_JUTSU.md`.

## RUL-2026-10-25-007 — The key item is the Lastlight Lantern

**Date:** 2026-10-25

**Domain:** Ghost Ship / Skyglass naming

**Status:** ACTIVE.

**Supersedes:** the item name "Lastlight" of RUL-2026-10-25-005; the jutsu keeps the name **Lastlight** (RUL-2026-10-25-006).

**Ruling:** Crownhold's entry item is the **Lastlight Lantern**, so the item and the jutsu are told apart.

**Evidence:** User, 2026-10-25: "Lastlight Lantern to differentiate from the jutsu."

**Canonical destination:** `docs/design/SKYGLASS_LOOT_TABLES.md`; push/254 (on hold).

## RUL-2026-10-25-008 — validate.py exception for push/261 (Lastlight)

**Date:** 2026-10-25

**Domain:** validation; D-validate-always (`docs/DOCTRINE.md`)

**Status:** ACTIVE. Manifest-specific; not a precedent.

**Ruling:** push/261 (the Lastlight jutsu) may run although `validate.py --strict` reports one diagnostic: L06 "wound missing statTypes/generalTypes". The game's `WoundTag` (`validators/combat.ts`) has `generalTypes` but no `statTypes`, the server drops the key, and Forge's pre-send check refuses it, so the lint is stale for `wound`. The exception holds only while `python3 scripts/validate_exception.py state/validate_exceptions/261_lastlight_jutsu.json` passes (exact manifest SHA-256 and exactly that diagnostic). The lint itself is to be corrected under Lane A.

**Evidence:** User, 2026-10-25, choosing between a one-off exception (A) and the Lane A lint fix (B): "A now."

**Canonical destination:** `state/validate_exceptions/261_lastlight_jutsu.json`; gate `scripts/validate_exception.py`.

## RUL-2026-10-25-009 — validate.py exception for push/262 (Foundry Warden); stale-rule fix to Lane A

**Date:** 2026-10-25

**Domain:** validation; D-validate-always (`docs/DOCTRINE.md`); engine law 14

**Status:** ACTIVE. The exception is manifest-specific; the fix is approved as a separate Lane A task.

**Ruling:**
1. push/262 (the Foundry Warden AI create) may run although `validate.py --strict` reports law 14 / L05 "AI create missing required field 'preferredStat'". Upstream migration 0056 dropped `preferredStat` (Forge's lints and `forge/test/post0056.test.mjs` already reflect this) and Forge refuses the key. The exception holds only while `python3 scripts/validate_exception.py state/validate_exceptions/262_foundry_warden.json` passes.
2. The two stale rules behind RUL-2026-10-25-008 and this ruling (wound `statTypes` under L06; `preferredStat` under law 14 / L05) are to be corrected on a separate Lane A branch by a separate agent, independently reviewed; the law-14 text change goes through the law-reconciliation process (RUL-2026-09-08-004). Brief: `state/prompt_validate_stale_rules.md`.

**Evidence:** User, 2026-10-25: "Approved on exception. Write request for a separate agent to do code branch for review".

**Canonical destination:** `state/validate_exceptions/262_foundry_warden.json`; `state/prompt_validate_stale_rules.md`.

## RUL-2026-10-25-010 — Treasure hunts: a lost fight fails the hunt; Captain's Purse 100,000 ryo

**Date:** 2026-10-25

**Domain:** quest structure (isolated Battle Pyramids); rewards

**Status:** ACTIVE.

**Ruling:**
1. In every Skyglass treasure hunt (Drowned Foundry, Quarantined Archive, Captain's Watch, Crownhold), a lost, drawn or fled fight fails the hunt: each `start_battle` routes `failObjectiveId` to a `fail_quest` objective, which closes the isolated run. No retry or recovery path. The entry item is spent at start either way.
2. Why: an isolated pyramid keeps a defeated player in the run at a minimum of 1 HP and freezes outside recovery (`libs/combat/database.ts`, `validators/objectives.ts` `isolated`), so a reset-and-retry starts the fight at 1 HP. This replaces Crownhold's 50%-pool recovery loop and reset bridges (RUL-2026-10-15-001 / -10-16-002 topology), which existed only to handle that case; Crownhold's node count is re-derived without them.
3. The Captain's Watch "Captain's Purse" pick is **100,000 ryo** (was the 50,000 proposal).

**Evidence:** User, 2026-10-25: "100,000 for ryo pick"; "The obvious solution is that failing a fight fails the quest. Otherwise we're figuring out how to deal with 1hp players. This would allow crownhold to shrink in size massively".

**Canonical destination:** `push/skyglass_hunts.gen.py` (push/268); `docs/design/SKYGLASS_LOOT_TABLES.md` (purse amount); Crownhold build.

## RUL-2026-10-25-011 — Crownhold badge "Crownbreaker"; Arakane's Command Crown

**Date:** 2026-10-25

**Domain:** content naming; lore; art direction

**Status:** ACTIVE (name, concept). Final art is approved image by image.

**Ruling:**
1. The Crownhold badge is **Crownbreaker**.
2. Supreme Commander Arakane wears a **Command Crown**, grander than the Crowned Captain's Skyglass Crown. It is how the
   commanders control the other afterimages.
3. The Crownbreaker badge icon is that crown breaking. Art request: `docs/handoffs/CROWNHOLD_CROWN_ART_REQUEST.md`
   (avatar first, which locks the crown; badge second).

**Evidence:** User, 2026-10-25: "Crownbreaker. And now Arakane needs a cool Crown, and the badge is that Crown breaking. So
he needs a better Crown than the captain. Its how they control the other afterimages".

**Canonical destination:** Crownhold build (badge item, Arakane avatar, story text); the art request above.

## RUL-2026-10-25-012 — The Buried Cache (fifth hunt); Medicine Inro two rolls

**Date:** 2026-10-25

**Domain:** content (treasure hunts); rewards; loot tables

**Status:** ACTIVE. questRank B and no level gate are proposals.

**Ruling:**
1. A fifth treasure hunt, **The Buried Cache**: the original Ghost Ship's buried-cache ending (`w_A`) rebuilt as an
   isolated Battle Pyramid. Entry: **Chart of the Buried Cache** (OTHER, COMMON, tradable), dropping from the Wreck at
   **20%** (the most common chart). Right cove: Skyglass Sentinel, ladder II. Wrong cove: a buried Deck Warden and Seal
   Charge, then the Sentinel, ladder I. No loop back to the riddle. A lost fight fails the hunt (RUL-2026-10-25-010).
2. Completion pick 1: **50,000 ryo / 5,000 exp / Medicine Inro ×1**.
3. The **Medicine Inro opens with two rolls** (was one); contents and weights unchanged.

**Evidence:** User, 2026-10-25: "May as well make one more map that drops at a higher drop rate that leads to that buried
cache on the beach"; on the proposal (20% drop, ladder II/I, pick): "50,000 ryo/5000 exp/1 Medicine Inro. Buff Medicine
inro to 2 rolls".

**Canonical destination:** `push/skyglass_hunts.gen.py` (push/270); `docs/design/SKYGLASS_LOOT_TABLES.md`; push/263 drop
table once the chart's id exists.

## RUL-2026-10-25-013 — Crownhold build: validate exceptions (push/271, push/272); enemy stat ladder ×5/3

**Date:** 2026-10-25

**Domain:** validation (D-validate-always); balance (Crownhold enemies)

**Status:** ACTIVE. Exceptions are manifest-specific; the stat scale is a launch value the hidden calibration fight tunes.

**Ruling:**
1. push/271 may run with the one `validate.py --strict` error L18 "item effect clear excluded from item union": the game's
   item schema takes `z.array(AllTags)`, which includes `ClearTag`. Gate:
   `scripts/validate_exception.py state/validate_exceptions/271_crownhold_exclusives.json`.
2. push/272 (the 20 Crownhold AIs) may run with exactly the 20 law 14 / L05 "missing preferredStat" errors (field removed
   by migration 0056; RUL-2026-10-25-009). Gate: `state/validate_exceptions/272_crownhold_ais.json`, written when the
   manifest is generated.
3. The package's enemy stat ladder (RUL-2026-10-16-011) is multiplied by **5/3** to keep its place against the crew after
   the 2026-10-21 pool pass moved the crew from statsMultiplier 3 to 5: regulars 2.5 to 4.17, commanders 5.0 to 5.83. Pools
   stay as approved.
4. L18 `clear` joins the stale rules for the Lane A validator fix (`fable/validate-stale-rules`, in review) as a follow-up.

**Evidence:** User, 2026-10-25, on the three-point request (exceptions, ×5/3 ladder, hand-made badge): "Proceed."

**Canonical destination:** the two ledgers above; `push/crownhold.gen.py` (`STAT_SCALE`).

## RUL-2026-10-25-014 — The Wreck's chest of chests; the Armory Requisition lives in it

**Date:** 2026-10-25

**Domain:** rewards; loot tables

**Status:** ACTIVE. The 10% Wreck line is the proposal the director adjusted without changing.

**Ruling:**
1. A new chest (replacing the retired Mystery Chest's role; the old item stays a relic) is a weighted cache with **one
   roll**: Common **50** Medicine Inro; Rare **30** Sage's Strongbox or Armory Requisition; Epic **15** Skyglass Coffer or
   Archive Chart Case; Legendary **5** Sealed Treasury. Named **Unmarked Cargo**; **not tradable**. It drops from Wreck clears (10% line).
2. The **Armory Requisition** returns here (it was shelved with the 2026-10-25 reward restructure) so players can still
   pick their Tool Pouch: an untradeable token whose use starts a one-node Special quest ending in a pick of 1 of the five
   Tool Pouches.

**Evidence:** User, 2026-10-25, on the chest-of-chests proposal: "This is where the requisition token goes, so the players
can still pick their tool pouch. Adjustment: Medicine Inro, common, 50 / Sage's Strongbox + Requisition Token, rare, 30
/ Skyglass Coffer + Archive Chart Case, epic, 15 / Sealed Treasury, legendary 5. Need a better name for it"; then "Not
tradeable on the token or chest. Unmarked Cargo it is".

**Canonical destination:** `push/skyglass_mystery.gen.py` (push/274); `docs/design/SKYGLASS_LOOT_TABLES.md`.

## RUL-2026-10-26-001 — Forge bundle budget raised to 436,000 raw / 105,500 gzip for the dungeon mount path

**Date:** 2026-10-26

**Domain:** Forge / bundle size budget

**Status:** ACTIVE

**Supersedes:** the 435,000 / 105,000 ceiling (RUL-2026-10-23-007).

**Ruling:** The Forge bundle ceiling is raised to **436,000 raw / 105,500 gzip** for Forge 0.9.1 (`fable/forge-dungeon-coop-path`: dungeon procedures at `coop.dungeon.*`). Measured 435,145 raw / 105,126 gzip, over the old ceiling by 145 / 126, mostly the two new source hashes the bundled dungeon contract carries. Trimming `_meta.sources` from the bundled contract was offered and declined.

**Evidence:** User, 2026-10-26, answering the independent review's required correction 3, choosing "Raise to 436,000 / 105,500 (Recommended)" over "Trim bundled contract" and "Raise more (437,000 / 106,000)".

**Canonical destination:** `forge/tools/check_bundle_budget.mjs` (`BUDGET`).

## RUL-2026-10-26-002 — Accept the residual dungeon-extractor guard gaps; integrate Forge 0.9.1

**Date:** 2026-10-26

**Domain:** Forge / dungeon contract extractor (`forge/tools/derive_dungeon.mjs`); Lane A integration

**Status:** ACTIVE. The acceptance is limited to these two findings at the reviewed head; the follow-up below stays open.

**Ruling:** The independent review of `fable/forge-dungeon-coop-path@3feea9715cc6c703c2f6406daa0ddfa6bac2125b` returned APPROVE WITH FIXES, with integration conditional on closing two extractor findings or on the director's explicit acceptance. The director accepts both residual risks and directs integration now:
1. `dungeonExport()` accepts an initializer that substitutes an empty object for the router argument (for example `createTRPCRouter({ ... } && {});`) while still deriving `coop.dungeon.getAll` / `coop.dungeon.save`.
2. The bracket scanner reads a regex literal containing a quote as a string, which can hide a trailing `.save` export and a following statement. The correction 3 handoff's statement that "a mis-scan ... fails closed" is false and is withdrawn.

Neither finding is a runtime defect. Forge's runtime source, bundle and loader are unchanged by every correction round (byte-identical to c45fbb93), and the extractor runs only when the game pin is re-pinned. Between re-pins, the committed contract is protected by the CLI's exact-pin and dirty-source checks and by the `_meta.sources` hashes.

**Follow-up (open, Lane A):** before the next re-pin of the dungeon contract, replace the extractor's text scanning of the three mount files (`root.ts`, `routers/coop.ts`, `routers/dungeon.ts`) with a syntax-aware check: a TypeScript AST with a pinned, explicitly declared dev dependency, reviewed as its own change. Until then, any re-pin's diff of those three files must be read by a person, not trusted to the extractor alone.

**Evidence:** User, 2026-10-26, choosing "Accept risk, integrate (Recommended)" over "Real parser, then review" and "Patch both, then review".

**Canonical destination:** `docs/handoffs/FORGE_DUNGEON_COOP_PATH_HANDOFF.md` (integration disposition); the follow-up is owned by Fable.


## RUL-2026-10-26-001 — Crownhold officers are chakra-impression ninjas in the Ghost Ship crew's look; no control thread

**Date:** 2026-10-26

**Domain:** Art direction / Crownhold AI avatars (art batch #8-#26)

**Status:** ACTIVE

**Supersedes:** the Crownhold continuity of the art batch bible (luminous cyan seams, translucency, flicker, the control thread) and Arakane as the officers' style reference; the 11 avatars already made under it (#8-#11, #14-#20) are redone.

**Ruling:**
1. Crownhold officers are shinobi recalled as chakra impressions, drawn in the Ghost Ship crew's outfit language: practical ninja gear (dark indigo and stone-grey cloth, rope and leather wraps, plain lacquered plates, a cloth mask or headwrap), worn and grounded. The impression shows only as chakra-lit eyes and a faint haze at the cloth's edges. No glowing seams, no translucent or crystal bodies, no gold filigree or tassels, no crowns (Arakane's Command Crown is his alone), no technology.
2. Style reference: the Deck Warden for regulars, the Captain for commanders. Arakane is a reference only for his own crown and belt seal.
3. The sci-fi subjects are re-grounded as ninja roles under their live names (Lancer, Replicant Zero, Containment Warden, Echo Subject, Failed Reconstruction Prototype, and lighter edits to the rest).
4. No thread, wire or line rising from the head: cut off at the frame edge it reads as an antenna on the moving combat sprite.

**Evidence:** User, 2026-10-26: "the command line will look silly in game since it cuts off at the edge ... It'll just look like a weird antenna"; "we've drifted into sci-fi too much with these. I wanted like, chakra impression ninjas not blue energy ghosts"; after comparing the live Ghost Ship avatars, on redoing all 11: "Yeah let's redo".

**Canonical destination:** `state/skyglass_art/build_art_batch.py` (`CROWN_THREAD`, `AVATARS`, officer style refs) and the regenerated `docs/handoffs/SKYGLASS_CROWNHOLD_ART_BATCH.md`.

## RUL-2026-10-26-002 — Ghost Ship rebrand: Edo-era Japanese fantasy ninja pixel art, anchored on the original crew

**Date:** 2026-10-26

**Domain:** Art direction / every Ghost Ship, Skyglass Wreck, treasure-hunt and Crownhold image

**Status:** ACTIVE

**Supersedes:** art bible draft v0.1 (it measured newer art as on-model); extends RUL-2026-10-26-001.

**Ruling:**
1. The collection is branded **Edo-era Japanese fantasy ninja pixel art**.
2. The palette and rendering anchor is the original Skyglass crew, **Deck Warden to the Crowned Captain**, with their
   portraits and the ship scenes. Characters are adjusted toward Edo-period shinobi (kimono, haori, hakama, obi, kyahan,
   tabi, sode and kote plates, hoods, tenugui, kasa, jingasa, kabuto with menpo, period weapons).
3. Newer approved art that veers from the anchor is not a reference and joins a redo queue: **Arakane** (gold, ornate),
   **Master of Arms** (samurai, heavy orange), **Foundry Warden** (brown, off-palette), **Crownbreaker badge** (smooth gold
   medal). Item icons #1-#4 are kept.
4. Prompt text lives in `docs/design/ghost_ship_art_bible/blocks.json` and is pasted verbatim by the batch builder.

**Evidence:** User, 2026-10-26: "I want to rebrand it as Edo era Japanese fantasy ninja pixel art. The actual art used for
the initial ghost ship has the correct color palette and rendering style, we just need to adjust our characters some";
"Like deck warden - crowned captain. Our newer approved art veers in the wrong direction"; on the proposed anchor, Edo
vocabulary and the four veering images (icons #1-#4 kept): "Yep, correct. Let's proceed based on this."

**Canonical destination:** `docs/design/ghost_ship_art_bible/ART_BIBLE.md` (v0.2) and `blocks.json`;
`state/skyglass_art/build_art_batch.py`.

## RUL-2026-10-26-003 — Crownhold enemy names; character silhouette, pose and colour

**Date:** 2026-10-26

**Domain:** Content naming (Crownhold AIs, quest text); art direction (Ghost Ship art bible v0.3)

**Status:** ACTIVE

**Ruling:**
1. **Names.** Short ninja-world titles. Live usernames (law 66: unique across all users) carry a "Crown " prefix on the
   one-word titles: Crown Armsmaster, Crown Trialmaster, Crown Tagwright, Crown Lancer, Crown Duelist, Crown Archivist,
   Crown Binder, Crown Echo, Crown Stonebound, Crown Signaller, Crown Tactician, Crown Runner, Crown Vanguard, Crown
   Herald, Crown Sealbearer; two-word titles stay bare: The Second, Honor Guard, Last Watch. **Replicant Zero** and
   **Supreme Commander Arakane** keep their names. Quest prose and art prompts use the titles without the prefix ("the
   Armsmaster"); art avoids the word "Crown" because it draws crowns.
2. **Characters** (bible v0.3 section 6.0): lean, tall, agile; commanders taller not wider; battle-ready with the weapon
   drawn; near-black and indigo cloth with skyglass cyan on the blade edge and eyes, brass on one or two fittings, rope
   only at the belt; trailing cloth; the prompt carries four costume marks, not the full vocabulary.

**Evidence:** User, 2026-10-26: "All the names need to be better. Shorter, more concise, fit in a ninja world"; on the
proposed list: "Replicant Zero can change. Rest approved"; on the Grand Marshal v1 ("Just isn't doing it for me"), the
five prompt changes and the "Crown" prefix: "Approved, Replicant Zero stays the same."

**Canonical destination:** `push/crownhold.gen.py` (USERNAME, PROSE; push/276 rename, push/273 text);
`docs/design/ghost_ship_art_bible/` (ART_BIBLE.md v0.3, blocks.json 0.3); `state/skyglass_art/build_art_batch.py`.

## RUL-2026-10-26-004 — Command shrines, not terminals; one shared Skyglass seal

**Date:** 2026-10-26

**Domain:** Crownhold quest text; art direction (Ghost Ship art bible)

**Status:** ACTIVE

**Ruling:**
1. **Terminal renamed.** Crownhold's "Military Command Terminal" / "command terminal" / "the terminal" is a **command
   shrine** in the quest text and the art. Quest node ids (`d2.n.terminal` ... `d5.n.terminal`) are ids and stay.
2. **One shared seal.** The ship and the castle use one mark: the **Skyglass emblem**, a four-point star in a diamond or
   circle. It replaces the "plain circled-cross seal" and the "one simple geometric seal" placeholders wherever a seal is
   drawn (Countermand, the Sealbearer's tablet, banners, chests).

**Evidence:** User, 2026-10-26, on the two open questions of the v0.4 review handoff: "Rename terminal, one shared seal."

**Canonical destination:** `push/crownhold.gen.py` (`PROSE`; push/273 regenerated); art bible v0.4 on
`fable/skyglass-art-bible-v04` (`roster.json`, `build_art_batch.py`, `ART_BIBLE.md`).

## RUL-2026-10-26-005 — Crownhold quest text: Edo pass

**Date:** 2026-10-26

**Domain:** Crownhold quest text (push/273)

**Status:** ACTIVE

**Ruling:** The quest text is rewritten in Edo craft to match the art bible, with mechanics, routes, answers, effects and
node ids unchanged: Medical/Combat Protocol become the **Healing Rite** / **War Rite**; Security Alert becomes **Alarm
Raised**; "protocol access" becomes **proper passage**; maintenance passages become hidden passages, stairs and channels;
specimen tanks, the reconstruction theatre, relay boards and the Lancer's firing rig become sealing jars, the recall
chamber, bell-cords and a spear gallery; the Armoury puzzle's COOLANT/CHARGE/SEAL become DOUSE/DRAIN/SEAL (same answer
order); the Research puzzle's Subjects A-C become Jars A-C (same answer); the Command Crown is described as the v0.4 iron
crown with no gold and no threads. Officers are named by their new titles throughout.

**Evidence:** User, 2026-10-26, on whether to give the quest text the same Edo pass as the art: "Yes".

**Canonical destination:** `push/crownhold.gen.py` (`PROSE`, `LABEL`, `CROWN`, `OVERRIDE`, effect descriptions);
push/273 regenerated.

## RUL-2026-10-26-006 — Skyglass Wreck: design-led encounter tuning; targets

**Date:** 2026-10-26

**Domain:** dungeon encounter design; balance

**Status:** ACTIVE (targets). The encounter redesign itself is pending, built and tuned in the offline engine harness
(`harness/skyglass_wreck_sim/`, in progress) before any live edit.

**Ruling:**
1. The dungeon's AI behaviour and waves are designed for a fun, engaging run and tuned closely in the offline harness,
   not assembled and measured afterwards.
2. Targets: an **average party** (three level-100 Jonin with a normal kit) clears in **15 to 20 minutes**, and the run is
   **clearable with few wipes** (about one run in five wipes once).
3. The live 16-wave definition (push/263, `RHqzYdY4EAQA9HwsBKWDS`) is the baseline to measure, not the design; it is
   expected to be cut sharply (5 floors are fixed by the engine).

**Evidence:** User, 2026-10-26: "we should design our AI specifically around making a fun and engaging dungeon now that we
have a test harness. Not just throw them in and see what happens. I want the behavior of the AIs and the waves tuned
closely"; targets chosen: "15-20 min", "Clearable, few wipes", "Level 100 Jonin, normal kit".

**Canonical destination:** the dungeon encounter design doc (to be written) and the harness's target checks.

## RUL-2026-10-26-007 — Skyglass Wreck in two versions: a level 40-60 run and the endgame run

**Date:** 2026-10-26

**Domain:** dungeon design; rewards

**Status:** ACTIVE (structure). Both encounter designs are built and tuned in the offline harness (RUL-2026-10-26-006).

**Ruling:**
1. Two separate dungeon records. The engine has no level or rank gate on dungeons (validators/dungeon.ts content schema;
   routers/dungeon.ts lobby create), so either version is open to anyone at the entrance; rewards carry the separation.
2. **Easier version:** tuned for a party of level **40-60**; its own lower-level copies of the crew (enemy strength comes from
   the AI's own level, with no party scaling); target clear **10-15 minutes**.
3. **Endgame version:** the existing level-100 Skyglass Wreck (`RHqzYdY4EAQA9HwsBKWDS`), redesigned; target **15-20
   minutes** (RUL-2026-10-26-006).
4. **Loot split:** the easier version drops only the entry tier (Chart of the Buried Cache and Unmarked Cargo) at lower odds;
   the endgame version keeps the full table (every chart, the Lastlight Lantern, the Sealed Treasury).
5. Both: clearable with few wipes for their target party.

**Evidence:** User, 2026-10-26: "We could do a lower level easier one, and a harder end game one"; choices: "Level 40-60",
"Easy: entry tier only", "Easy 10-15, endgame 15-20".

**Canonical destination:** the dungeon encounter design doc (to be written); the harness targets.

## RUL-2026-10-26-008 — Editing an AI-held item severs it too (law 18 extends to items)

**Date:** 2026-10-26

**Domain:** Engine behaviour / AI items (Headless Rider Horror!, Zombie Villager)

**Status:** ACTIVE (observation; law text reconciliation pending).

**Ruling:** Law 18 (editing an equipped jutsu severs the AI's combat link) also holds for items. The push/264 edit of Zombie Claws (`mMl6P4B7v6-_CyDo3HVG7`) left the Zombie Villager (`nqL-uL-Z_7I0iuowlpBDx`) unable to use them: its push/268 rules fell through to End Turn every round. Treat an item an AI holds like an equipped jutsu: take it off the AI, edit the item, put it back. The numbered law text in `docs/ENGINE_LAWS.md` is updated through the law-reconciliation pass, not here.

**Evidence:** User, 2026-10-26: "I figured it out. When we updated the claws it severed the link." Live fight log the same day (zombies adjacent to Carbon and Kitsu, End Turn each round, no claw or move).

**Canonical destination:** `docs/ENGINE_LAWS.md` law 18 (pending reconciliation).

## RUL-2026-10-28-001 — Skyglass Wreck hazards: a small, heavy blast; dungeon kit additions approved

**Date:** 2026-10-28

**Domain:** TNR content balance / Skyglass Wreck dungeon and treasure hunts

**Status:** ACTIVE.

**Ruling:**
1. Core Rupture (`nCQETf-HNnbRec1OSY2-R`, held only by Seal Charge and Core Canister) stops hitting every player on the board (`method: ALL`). It now hits a small area (AOE circle spawn: the target hex and the six around it, range 5) for more damage (pierce 120 -> 180, a reversible starting value). The hazard's self-destruct (`onehitkill` on SELF) and the 2-round stun stay. The change is made to the live record, so it applies to the hunts and the dungeon alike (push/316-317).
2. Dungeon-only jutsu approved as designed in `docs/design/SKYGLASS_WRECK_ENCOUNTERS.md`: Chain Hook (now a pull, then a 1-round root), Long Barrage, Oath of Stillness, Skyglass Aegis, Mending Seal, and the per-enemy rules and Crowned Captain phases. Numbers are starting values for the harness to tune.
3. Chart Mark (settled 2026-10-28, "Both approved"): increasedamagetaken 40 / 2 rounds, cooldown 4, plus a marker row of increasepoolcost 5 / 2 rounds that no crew jutsu applies; the crew's focus rules key on the marker, not on damage taken. Cleansable. Mark sigil animation.

**Evidence:** Director, 2026-10-28: "We can make them smaller AoE blasts that do large amounts of damage instead I suppose. Rest looks pretty good"; "Chain Hook … sounds more like a move for a pull which would also be approved. Long barrage approved. Oath of stillness approved. Chart mark could be better executed. 20% is low … it will make any increased damage taken set the crew off. Needs more thought. Rest is approved. Yes change the hunts too."

**Canonical destination:** `docs/design/SKYGLASS_WRECK_ENCOUNTERS.md`; `push/core_rupture.gen.py`.

## RUL-2026-10-28-002 — validate.py exception for push/317 (Core Rupture pierce 180)

**Date:** 2026-10-28

**Domain:** validation; D-validate-always (`docs/DOCTRINE.md`); engine law 6

**Status:** ACTIVE (approved 2026-10-28). Moved with the change into push/319: the ledger is
`state/validate_exceptions/319_skyglass_update.json`, which also lists push/319's seven build-order warnings (the lint
orders entities by type and ignores explicit phases; law 18's kit-off / edit / kit-on sequence needs AI edits on both
sides of the jutsu and item edits).

**Evidence:** Director, 2026-10-28: "Both approved. Dont bother creating a lot of small separate pushes, we'll do this as one large update."

**Ruling:** push/317 (now push/319) may run although `validate.py --strict` reports law 6 "pierce power 180 exceeds the cap of 100". The game's `PierceTag` power has no maximum (`validators/combat.ts` `PowerAttributes`: `min(0)`), and the live Core Rupture already carries 120. Law 6's flat cap is already listed for law reconciliation (RUL-2026-10-20-001, Boundary). The exception holds only while `python3 scripts/validate_exception.py state/validate_exceptions/317_core_rupture_blast.json` passes.

**Canonical destination:** `state/validate_exceptions/319_skyglass_update.json`.

## RUL-2026-10-28-003 — Crowned Captain to Crownhold; the Captain is the Wreck's boss; one elemental kunai pouch

**Date:** 2026-10-28

**Domain:** Skyglass Wreck / Crownhold story, encounters and rewards

**Status:** ACTIVE. The Crownhold story rewrite is drafted for approval separately.

**Ruling:**
1. **Crownhold's final boss is the Crowned Captain.** Arakane's AI record (D5.BOSS, `7QofodAiUwIoM-voiA2p6`) is converted: it keeps his Crownhold stats, kit and Countermand, takes the Crowned Captain's name and the original crew portrait. Arakane is retired from the story (his art redo is cancelled).
2. **The Captain is the Skyglass Wreck's final boss.** Endgame floor 5 wave 2: The Captain + Sealwright. Floor 4 wave 2: Wayfinder + Core Horror, the Core Horror reworked as a gimmick minion whose attacks are broadcast a round ahead.
3. **Crownhold's completion pick gains one Fragment of the Skyglass Crown** (`ayiRmSjWs05lMPyL3G-1d`), a guaranteed route for players farming it. Coffers still drop fragments.
4. **One elemental kunai pouch.** The five elemental kunai are down to Elemental Kunai, so the five Tool Pouches become one, the Elemental Tool Pouch (the Katon pouch record, re-pointed). The Armory Requisition and the Drowned Foundry pick 1 of: Elemental Tool Pouch / Medicine Inro / 50,000 ryo.

**Evidence:** Director, 2026-10-28: "For Crownhold and the character we put the Crowned Captain. Then the regular captain is the boss of the skyglass wreck. Then one of the rewards for beating crowhold is a guaranteed crown fragment … this simplifies the story a lot"; "adjust the armory to only drop one kind of elemental kunai pouch now since we're down to 1 … needs 2 more rewards now, perhaps medicine inro for one". Answers: "Convert Arakane"; floor 4: "Work in Core Horror. Make him a gimmicky minions, lots of broadcasted attacks"; pouch: "Elemental Kunai"; picks: "Inro + 50,000 ryo".

**Canonical destination:** `docs/design/SKYGLASS_WRECK_ENCOUNTERS.md`; `docs/design/SKYGLASS_LOOT_TABLES.md`; `push/elemental_pouch.gen.py` (push/318); `push/crownhold.gen.py`.

## RUL-2026-10-28-004 — Crownhold story: the Crowned Captain's crown holds every afterimage; one large update

**Date:** 2026-10-28

**Domain:** Crownhold quest text and records; push staging

**Status:** ACTIVE

**Ruling:**
1. The Captain commands the Skyglass ship; the Wreck is his last stand. The Crowned Captain rules Crownhold; his Command Crown holds every afterimage in his service, the ship's crew and the castle's officers alike. The Lastlight Lantern leads to him.
2. Ending: the crown breaks; across the mountain and out on the wreck every afterimage lets go; the blades lie scattered as the Fragments of the Skyglass Crown. The "something else is still giving orders" hook is dropped.
3. Every "Supreme Commander Arakane" / "the Supreme Commander" in the quest text becomes the Crowned Captain (puzzle answers unchanged). The boss's username is **The Crowned Captain**, since the legacy Ghost Ship boss holds "Crowned Captain" (law 66).
4. The Skyglass / Crownhold changes ship as one manifest (push/319), not a series of small pushes.

**Evidence:** Director, 2026-10-28, on the outline, the name and the two open items: "Both approved. Dont bother creating a lot of small separate pushes, we'll do this as one large update."

**Canonical destination:** `push/crownhold.gen.py` (`BOSS_PROSE`, `OVERRIDE["d.aftermath"]`, `CROWN`, `WIN_TEXT`); `push/skyglass_update.gen.py`.

## RUL-2026-10-28-005 — The Crowned Captain commands his echoes from afar

**Date:** 2026-10-28

**Domain:** Crownhold story and boss presentation

**Status:** ACTIVE

**Ruling:** The Crowned Captain uses the original crew avatar unchanged. He never sailed: he controls the afterimages from afar, and the Crowned Captain players beat aboard the Ghost Ship was one of his echoes, which explains the likeness. On every route to the final fight, the player says "I defeated you once!" and he answers "I control... many echoes." before the fight starts. The rite route gains an intro beat so it meets him too.

**Evidence:** Director, 2026-10-28: "The Crowned Captain will use the same avatar and everything. We'll update the lore to be that he controls the afterimages from afar, the player can even exclaim at him 'I defeated you once!', to which he could reply 'I control... many echoes' and then the fight starts. That would explain the similar appearance, ties into the afterimpression plot and deepens it".

**Canonical destination:** `push/crownhold.gen.py` (`ECHO_LINE`, `ECHO_BEAT`, `PROTOCOL_INTRO`); push/319.

## RUL-2026-10-28-006 — Boss kits: the old Crowned Captain's kit to the Captain; the Crowned Captain as the showcase boss

**Date:** 2026-10-28

**Domain:** Skyglass Wreck / Crownhold boss design

**Status:** ACTIVE. Set-piece mechanics and numbers pending harness probes and tuning.

**Ruling:**
1. The Captain's dungeon copy takes the old Crowned Captain's full kit.
2. The Crowned Captain (Crownhold) keeps Arakane's kit minus three fillers. He gains Final Command, Keelbind and Ruin Refrain, and fights in three phases.
3. He gets "a little more juice": he is the event's hardest fight and the showcase for the PoE-style marked set pieces (Seven Blades, Recall, Command Absolute, Shardstorm), in `docs/design/SKYGLASS_WRECK_ENCOUNTERS.md`.

**Evidence:** Director, 2026-10-28, on the kit split and three phases: "Approved but give the Crowned Captain a little more juice. Hes the shaper of our experience".

**Canonical destination:** `docs/design/SKYGLASS_WRECK_ENCOUNTERS.md`.

## RUL-2026-10-28-007 — Tuned 6-wave numbers approved; the story fits the existing art

**Date:** 2026-10-28

**Domain:** Skyglass Wreck balance; Skyglass story and art direction

**Status:** ACTIVE

**Ruling:**
1. The tuned 6-wave dungeon numbers are approved as the dungeon copies' starting values (harness `fable/skyglass-wreck-sim` 0d3534c2; `docs/design/SKYGLASS_WRECK_ENCOUNTERS.md`). The figures: regulars 5,050 HP with two +100% rows; Core Horror 25,250 HP with two rows; Captain and Sealwright 12,625 HP with three rows.
2. No existing art is redrawn; the story bends to it (story bible, "Locked to the existing art"). The Captain and the Crowned Captain share the white mask ("I wear his mask"). The Command Crown is the frost-pointed skyglass crown of the existing avatar. The Deck Warden's young eyes show above his cloth mask. The ship scenes are the Core holding the wreck's interior as it was. Arakane's avatar is retired, and the Crownbreaker badge stays as drawn. The "Seven Blades" set piece becomes **Crownfall**.

**Evidence:** Director, 2026-10-28, on the tuned numbers and the telegraph findings: "Perfect. Approved, one minor edit. I dont want to regenerate pre-existing art so let's update our story around that".

**Canonical destination:** `docs/design/SKYGLASS_STORY_BIBLE.md`; `push/crownhold.gen.py`; `state/skyglass_hunts/hunts.py`.

## RUL-2026-10-28-008 — Kit tuning decisions: Core Horror teeth, First Blade buff, Crowned Captain HP doubled

**Date:** 2026-10-28

**Domain:** Skyglass Wreck / Crownhold balance

**Status:** ACTIVE. The harness retunes are in progress.

**Ruling:**
1. **Core Horror:** stronger normal attacks, a set piece every other turn, and an earlier phase 2 so his pools appear. He must cost a dodging party real HP.
2. **First Blade:** buffed so it survives past round 2 and gets its signature turns.
3. **Level 40-60 version:** left as tuned. A real level-50 player capture to retune against may come later.
4. **Crowned Captain:** HP doubled (pools 2.5 to 5, about 25,250) for a longer phase 1 and a longer fight; the Recall echo is kept as is.

**Evidence:** Director, 2026-10-28: "Problems: 1. Approved 2. Buff him / Decisions: 1. Leave as is 2. OK, maybe in a bit 3. Yeah give him more HP, double it. 4. Yes, approved." Read against the open lists: problem 1 is the Core Horror fix; "Buff him" is read as the First Blade (problem 3, which dies in round 2), since problem 2 was the Captain's jutsu count. Decision 1 is the level range; decision 2 is the level-50 capture; decision 3 is the Crowned Captain; decision 4 is the Core Horror.

**Canonical destination:** `docs/design/SKYGLASS_WRECK_ENCOUNTERS.md`, `docs/design/SKYGLASS_BOSS_FIGHTS.md`; harness `fable/skyglass-wreck-sim`, `fable/crowned-captain-sim`.


## RUL-2026-10-28-009 — Skyglass charts: the map system, tainted rares, Core Rot, titles and trophies

**Date:** 2026-10-28

**Domain:** Skyglass event / rewards

**Status:** ACTIVE. Design approved; manifests not yet built.

**Ruling:**
1. **Chart runs are high-stakes.** The chart is spent at entry, any loss fails the run, pools carry between fights, rewards bank per fight, and a final press-on room is lost on a fall.
2. **Two new common charts:** Tide Chart and Watch Roster. They scale to the player and drop from both Wreck versions.
3. **Two new rare charts:** Reliquary Seal and The Last Heading. They drop from the Archive and the Watch.
4. **The chart ladder drop rates are approved as proposed.**
5. **Tainted versions exist for the rares only:** the Rotted Reliquary and the Burning Heading, with the twists in the loot tables doc. They are obtained by steeping, breaking the seal, pressing on, or a 1% natural drop.
6. **Core Rot** is a reagent: 15% from the Core Horror in the Wreck, more common in his runs.
7. **Trophies are cut to two:** The Warden's Ladle and Wayfinder's Compass. **Titles are cut to five.**

**Evidence:** Director, 2026-10-28: "1. Yes, rares only. Add a few more twists that make these charts unique harder upgrades of their counterpart. Propose methods to obtain, prefer creativity here 2. Approved. 3. Draft them". Then: "Cut the trophies, inventing that many items will be difficult. Perhaps 1-2 well designed ones. Cut number of titles in half. Core Rot as a reagent that drops rarely from Core Horror in the wreck(15%) and more commonly in his hunts".

**Canonical destination:** `docs/design/SKYGLASS_LOOT_TABLES.md` §5.

## RUL-2026-10-28-010 — Skyglass reward review: rare chart rates, tainted balance, steeping, new-run picks

**Date:** 2026-10-28

**Domain:** Skyglass event / rewards

**Status:** ACTIVE.

**Ruling:**
1. **Rare chart rates:**
   - 25% from the Archive and Watch endings, +20% from their press-on rooms.
   - Crownhold's ending drops one of the two rares at 50%.
   - Target: one rare chart per 30-40 Wreck clears. The 8% rate would have taken about 211-257 clears.
2. **Burning Heading:** entry at 70% pools. The Captain ally joins only after the Core Horror falls.
3. **Rotted Reliquary:** its Core Horror room becomes the press-on room.
4. **Tainted rewards:**
   - The rare's pick at ×2, a guaranteed Sealed Treasury, Lantern 30% and Core Rot 40%.
   - Target clear rate about 55%, against about 80% for the base rare.
5. **Steeping:**
   - A loss spends only the Core Rot; the chart is returned through a fail step.
   - The fight is tuned to about a 75% solo win rate.
6. **Completion picks for the four new runs**, as listed in the loot tables §5.
7. **The Buried Cache scales to the player**, so the easy Wreck's Cache chart is usable.
8. **The Cache/Foundry ryo parity is to be fixed.**
9. **The Crownhold Crown Fragment pick is recorded as an explicit exception** to "Skyglass items come only from the Coffer". This is the director's own guaranteed-fragment ruling.
10. **Stale doc sections are corrected.**

**Evidence:** Director, 2026-10-28, after the reward review and the steeping explanation: "Yeah, the version above is approved. All approved..."

**Canonical destination:** `docs/design/SKYGLASS_LOOT_TABLES.md` §5.

## RUL-2026-10-28-011 — Skyglass pets: Galley Stores and the Echo Jar

**Date:** 2026-10-28

**Domain:** Skyglass event / rewards

**Status:** ACTIVE. Pet kits are pending approval.

**Ruling:**
1. **No materials or crystals as event rewards.** The hunts are open to all players, and these would undercut the profession markets and crafting effort.
2. **The Treasury change is pending:** more rolls, weighted to Imperial Gold. The Footlocker and the Shore Leave Purse are not adopted.
3. **Two pet chests:**
   - Galley Stores: pet experience, with no meals.
   - The Echo Jar: rolls one of five jar items, each granting a reward-only (inactive) ghost-ship species. The roster and placement are as in loot tables §5b.

**Evidence:** Director, 2026-10-28:
- "No materials and no crystals. Ruins the profession market for both..."
- "Your 2 new chest ideas are kinda dull but you did stumble upon a gold mine... pets... Perhaps 1 for pet progression and 1 for rolling from a pool of ghost ship exclusive pets?"
- On the roster and placement: "Yes, approved".

**Canonical destination:** `docs/design/SKYGLASS_LOOT_TABLES.md` §5b; `docs/design/SKYGLASS_PETS.md`.

## RUL-2026-10-28-012 — Sealed Treasury rework; pets get builder support

**Date:** 2026-10-28

**Domain:** Skyglass event / rewards; builder (Lane A)

**Status:** ACTIVE.

**Ruling:**
1. **The Sealed Treasury pays more gold.** 150,000 ryo, then 3 rolls (60%), 4 rolls (30%) or 6 rolls (10%), weighted toward Imperial Gold. Table in loot tables §3.
2. **The five pet kits are approved as proposed** in `SKYGLASS_PETS.md`, with numbers provisional until the live pet catalogue is captured.
3. **Pet species are built through the builder.** Pet-species support and the PETS jutsu `requiredPetSpeciesId` field are added on a `fable/*` branch under Lane A, followed by independent review. The species are not hand-entered.

**Evidence:** Director, 2026-10-28: "Approved. Builder route ok."

**Canonical destination:** `docs/design/SKYGLASS_LOOT_TABLES.md` §3, `docs/design/SKYGLASS_PETS.md`.

## RUL-2026-10-28-013 — Structure review fixes; Crownhold carries HP; Archive guard; Sealwright's bruiser

**Date:** 2026-10-28

**Domain:** Skyglass event / economy and encounters

**Status:** ACTIVE. Harness re-runs are pending.

**Ruling:**
1. **The structure review's fixes are approved:**
   - Pets are added to the Wreck and hunt harnesses.
   - An upstream proposal goes in to exempt entry-item Pyramid runs from the lifetime 100-start cap. The cap stays at 100 for launch.
   - The Rotted Reliquary's press-on room becomes Replicant Zero.
   - The Sealed Reliquary's last echo is the First Blade.
   - The common runs end with Core Rot at 15%.
   - The Archive Chart Case's Legendary tier becomes Lantern 3 / rare chart 5.
   - The Buried Cache pays 25,000 ryo.
   - Titles get small values, proposed for approval; their effects are permanent mastery or regeneration bonuses.
   - The easy Wreck gets Galley Stores at 10%.
   - The Core Horror carries Core Rot as an AI drop in quest battles. The steeping fight uses its own copy, with no Rot drop.
   - Tainted runs and Crownhold use pick 2 (`rewardPickCount`) instead of ×2 quantities.
   - The Crown's Hoard is one item opening the Coffer, Treasury and Echo Jar caches.
   - The common runs get mixed package cards.
   - Titles move to one-time first-clear achievements.
   - The harness confirms objective rewards bank mid-run.
2. **Crownhold keeps carrying HP between fights.** Its routes (shortcut, War Rite buff, Healing Rite) only mean something if HP carries. The commanders are retuned for the chain, since they are never fought alone. Targets: every route clears; Healing Rite highest, alarm lowest.
3. **The Archive alarm guard gets its own record:** Crown Archivist (the Skyglass Archive Keeper), not the Sentinel. The Cache Sentinel is unchanged.
4. **The Sealwright keeps Ward of Command.** "Called to the Archive" summons a lighter bruiser, Crown Stonebound, and the ward lands on it as the highest-health ally.

**Evidence:** Director, 2026-10-28: "Approve fixes. If we refill their HP what's the point of the separate nodes and all the extra work we put in on the shortcut vs buff vs heal? Archive alarm guard can have a separate record. We have a bunch of ghost ship AI, can use a Crownhold one if needed. Keep the Sealwright's ward and give him a lighter bruiser than the Crowned Captain to work with".

**Canonical destination:** `docs/design/SKYGLASS_LOOT_TABLES.md`, `docs/design/SKYGLASS_BOSS_FIGHTS.md`; harness `fable/skyglass-wreck-sim`, `fable/crowned-captain-sim`, `fable/skyglass-hunts-sim`.
