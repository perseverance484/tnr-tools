# Bloodright Structural Rollout — Director Priority and Two Separate Art Workflows

**Status:** DIRECTOR PRIORITY APPROVED, 2026-10-17. Operational plan; **not approval to change mechanics, execute live writes, or publish.**
**Working roles:** Content Designer / Release Auditor with Art Director and Engineering Auditor lenses.
**Implementation baseline:** `perseverance484/tnr-tools main@362ef7dfa0a7c99890a8359c253ec1651702fe6c` (verified 2026-10-17).
**Director decision:** `docs/RULINGS.md` RUL-2026-10-17-003 on this branch.
**Visual studio authority:** `chatgpt/bloodright-icon-studio-20261016@792742c264c70c29733306f22962d7b4aad48fad`, `docs/workflows/BLOODRIGHT_ICON_STUDIO.md` and `docs/design/bloodright/ICON_PRODUCTION_TRACKER.md`.
**Import authority:** `forge/bloodright/README.md` and `forge/src/bloodright/{compiler,validate,collection}.mjs` on live main, plus pinned source and reviewed Forge tests.
**Legacy planning roster:** `fable/bloodright-planning-20261003@7c1dfdd5e3ee163b90c22694dbb2de94ede08866`. Its old draft mechanics are not silently adopted as current import sources.

## 1. Critical distinction — do not blend these workstreams

| Workstream | Output and purpose | Reference inputs | Priority |
| --- | --- | --- | --- |
| **Bloodright TIER EMBLEMS** | **Exactly three images per bloodline**: Foundation, Hidden Art, Advanced Art. Reuse the same image on **every skill of that tier in that bloodline's tree**. Fixed universal tier silhouettes are reskinned in bloodline-specific color/material; user-approved **opaque solid black background**. Initial art queue: 29 public A/S/H bloodlines, **87 emblem images**. | Existing jutsu art (supplied as one bloodline ZIP), optionally bloodline identity image; reference evidence only. | **P0 — active.** Art supports prompt structural Bloodright import. |
| **Existing BLOODLINE JUTSU-ICON REWORKS** | Distinct individual illustrations **per jutsu technique**. BBE, BEE, Vaporia jutsu-art projects are examples. Use technique-specific silhouettes and separate approval/production registers; not interchangeable with the tier emblems. | Original jutsu assets + actual technique behavior. | **Deferred relative to Bloodright structural rollout.** Resume independently when director chooses. |

The Bloodright art ZIP at the beginning of a **Bloodright tier-emblem session** is **only a visual source pack**. Its original jutsu icons provide palette, material, glow and identity. The job is to render **three consistent, locked silhouettes**, **not** to remake the ZIP's five/eight/twelve existing technique icons. The studio inspects the ZIP and selects one or two individual references for each isolated image-generation attempt. A ZIP upload alone does not prove a generator saw its contents.

Bloodright poster showcases / structural SVGs are also separate presentation work, **not** an icon-workstream prerequisite.

## 2. Release priority — hidden, structural Bloodright trees first

**Director objective:** put complete Bloodright **skill trees** into the existing game structurally, prioritizing the real **skill names, categories, three tier visuals, prerequisite connections, per-node Seichi Silver costs, and effect durations**. The separate jutsu-icon redesign program **must not hold up Bloodright**.

**Preferred production rhythm: one bloodline at a time, end-to-end.** Avoid waiting for all 29 art sets to finish before reviewing the first structurally complete import. Each bloodline is a coherent package with:
1. **Approved complete skill-tree source:** exact nodes, tier classification, canonical names, intended 5-BP topology, explicit ALL prerequisites and one point per skill, plus actual potency effects required by the current Forge compiler. Do **not** treat a structural shell as approval of potency amounts or live behavior.
2. **Three director-approved Bloodright emblems:** Foundation / Hidden Art / Advanced Art (one per tier), with original accepted source bytes preserved, verified exports, and explicit per-node/category image binding in the Forge package. No reworked individual jutsu art required.
3. **Explicit per-node economics and effect lifetime:** `seichiSilverCost` and `rounds`. **RUL-2026-10-08-002 authorizes 20 Seichi Silver / 99 rounds for BEE's twelve nodes ONLY.** No global 20/99 default exists for the other bloodlines. Secure separate director approval or preserve clearly blocked placeholders for each other tree.
4. **Forge preview and validation:** exact source SHA; no missing nodes/settings/icons, wrong/duplicate names, invalid effects, broken prerequisite links, stale inventory or unverifiable image packs. Review complete create/edit/reuse previews and effects. New skills remain `hidden:true`. User approves and operates any production import; no agent touches the live game.
5. **After operator-run hidden import:** export results, check per-record success and fresh read-back, ensure intended names, icons, silver costs, effect durations, parent links and folder/bloodline scope actually persisted. **Publishing is separately authorized** and not implied by structural completion.

This is a **hidden structural rollout**, not a promise that the proposed element-wide potency resolver or cross-roster balance is implemented and live-correct. The source audit identifies an engine gap where existing row-element matching may differ from the approved classification-wide intent. Surface the gap rather than silently narrowing the design. Any later release/publishing depends on its own evidence and user approval.

**No automatic placeholder import.** Current Forge compiler constructs skill effects from `nodes[].bonuses`, requires the approved five-BP structural format and validates each effect. Without actual approved mechanics/structure, Fable may prepare a draft but must not fabricate a supposedly final structural import.

## 3. Reality check from checked-in evidence

- **Forge importer exists and is integrated.** `forge/bloodright/README.md` documents single-tree and `bloodrightCollection` imports, three per-tier `icons` defaults, per-node overrides, `imgSizes` + immutable `imagePack`, hidden creates, and operator-controlled preview/import. A collection is **sequential**, not transactional: earlier completed bloodlines are not rolled back when later trees stop.
- **Actual art-input gap:** historical tier-emblem approvals include BEE and Blue Blade Eyes (**6/87** recorded approved); their original sources/exports are not pinned as immutable Git binaries. Visual approval is not upload/preflight proof. The Bloodright-specific **opaque black** `skillTree.image` acceptance/preflight path still needs evidence; do **not** equate the new `JUTSU_ICON` rule for `jutsu.image` with a Bloodright skill-icon contract.
- **Tree source gap:** `forge/bloodright/collection.readiness.json` (2026-10-16) reports **44 old four-BP `modifiers` trees** and only **one updated five-BP structural source** (BEE). It reports **0 production-ready packages**. Do not turn legacy trees into five-BP imports by automatic reinterpretation.
- **BEE is the first importer pilot**, with 12 named nodes, explicit 20 Silver / 99 rounds, a known existing folder and one existing hidden skill binding. The current BEE collection template is **BLOCKED** because the actual tier-emblem bytes/immutable pack are missing.
- **Ethereal Monarch is the next Bloodright tier-emblem art target.** The director reports that its read-only capture ran and has a ZIP containing all original jutsu icons. This ZIP is the **reference input**; generate only the three Bloodright tier symbols in this workstream. Independently, its updated 5-BP tree, approved prices/durations, and viable Forge bindings must be prepared before a hidden import is executable.
- **Master reference-library ZIP automation is optional/deferred:** the approved `state/prompt_bloodright_reference_library.md` on `chatgpt/bloodright-reference-library-brief-20261016@1b3b93b3ac939afc2fed1c63390fe68ed0d261d6` remains a distinct archival/convenience task. With an individual reference ZIP supplied per bloodline, do not require a 29-pack downloader or additional full-roster Forge captures before starting Bloodright production.

## 4. Immediate lanes

**Bloodright Art Studio / ChatGPT (director-guided):**
- On receipt of `BR-023_Ethereal_Monarch.zip` (or any exact Ethereal Monarch ZIP), inspect actual file bytes and jutsu mapping; inspect the actual images; prepare the teal/cyan bloodline treatment card for director approval.
- Create / approve the universal-shape **Foundation**, **Hidden Art**, **Advanced Art** icons separately; record original source hashes, export/alpha/codec/thumbnail QC, exact immutable bindings. No unrelated jutsu icon redesign.
- Repeat for approved bloodlines in a sequence driven by import readiness and director choice.

**Structural preparation / Fable (sole normal technical writer):**
- Reconcile current intended per-bloodline structural sources with the importer contract and source evidence; do not base unverified tree rewrites on old four-BP `modifiers` JSON.
- Prepare a compact per-bloodline or small-batch readiness table: 5-BP source and names/topology, mechanics/engine-gap review, selected `seichiSilverCost` and `rounds`, 3 icons and their source/pack, folder/bindings and hidden probe, Forge preview/validate, user authorization and read-back.
- Start with the BEE template already supported and subsequent Ethereal Monarch once assets and tree fields exist. Stage nothing as production-ready until both the art and content gates close.
- If art upload acceptance for opaque Bloodright `skillTree.image` requires a narrow spec/validator adaptation, follow normal Fable Lane A implementation and independent review. Never change the jutsu-specific validator to solve the wrong field.
- Do not contact the game or execute read-only captures on the user's behalf. Only the user runs approved live-game operations.

## 5. Progress and stop conditions

Keep three distinct statuses: **ART VISUAL APPROVED** → **ASSET MECHANICALLY VALID/BOUND** → **HIDDEN TREE IMPORT VERIFIED**. A tree can be structurally prepared without being uploaded, and a hidden import is not published or balance-final.

**No new game reads/writes or publications authorized by this document.** No ZIP was attached to this decision conversation; Ethereal Monarch ZIP file content has not been independently inspected here.
