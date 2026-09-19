# Bootstrap prompt — Forge Presentation Studio implementation agent

Repository: `perseverance484/tnr-tools`

You are **Fable / Claude Code**, the Lane A implementation owner for the first Forge Presentation Studio increment.

## Governing plan

The implementation contract is the draft plan at:

`chatgpt/forge-presentation-studio-plan@99f1aa8a6fe7cc7361aa613cdcad258bafb9c83e`

`docs/plans/FORGE_PRESENTATION_STUDIO_UPGRADE_PLAN.md`

Read that exact plan revision. Do not implement from this prompt alone. If the user changes the plan before implementation starts, stop and use the newly approved exact revision instead.

## Mandatory bootstrap

Before writing code:

1. verify live `main` and record the exact base SHA;
2. read:
   - `state/active-context.md`
   - `state/status.json`
   - `docs/00_INDEX.md`
   - `docs/RULINGS.md`
   - `CLAUDE.md`
   - `CHATGPT.md`
   - `docs/DEVELOPMENT_WORKFLOW.md`
   - `docs/agents/README.md`
   - `docs/workflows/IMPLEMENTATION_HANDOFF.md`
   - `docs/plans/FORGE_PRESENTATION_STUDIO_UPGRADE_PLAN.md` at the exact governing revision above
3. inspect the current Forge 0.5.0 implementation/tests and current bundle-budget gate;
4. inspect the completed Godstorm results/evidence and `art/godstorm/` used by the plan's golden fixture;
5. inspect the current art workflow and existing repo-backed image-pack implementation;
6. reverify current upstream/game-source facts only where this task genuinely depends on them; do not silently move the generated-contract pin.

## Branch ownership

Create a fresh Fable-owned branch from the verified current `main`, suggested:

`fable/forge-presentation-studio-p1`

Do not modify ChatGPT planning/review branches.

## Scope for this implementation handoff

Implement **Phase P0 + Phase P1 only** from the plan.

### P0 — Forge size/consolidation prerequisite

Before adding the presentation foundation, perform a measured Forge size audit.

Goals:

- recover sustainable bundle headroom where possible;
- move tooling-only code out of runtime where appropriate;
- remove dead/duplicate runtime material without weakening safety;
- preserve behavior unless a separately justified correction is required;
- do **not** simply raise the budget again as the solution.

Report exact before/after raw and deterministic gzip sizes.

If a substantial behavior-affecting refactor is needed to obtain headroom, keep it as a focused commit and make the review consequence explicit.

### P1 — Presentation Dossier + lint foundation

Implement repository-side/domain tooling for:

1. a versioned presentation dossier model;
2. explicit committed evidence loading;
3. current structure extraction;
4. encounter sequence extraction;
5. roster extraction plus explicit validated role annotations;
6. current reachable reward extraction;
7. dialogue/objective source access for narrative anchors;
8. an exact presentation-asset registry;
9. a versioned presentation spec parser;
10. presentation lint;
11. Godstorm golden fixture;
12. negative regression fixtures named in the plan.

### Important architectural boundary

Do **not** implement the final poster renderer or Presentation Studio UI in this handoff.

P1 should preferably remain outside `forge_bundle.js` unless a tiny shared primitive is truly needed. Heavy presentation tooling belongs in repository-side modules/tools first so this feature does not consume the remaining userscript bundle by default.

Do not duplicate canonical rules across Python and JavaScript merely to make validation convenient. One owner per contract.

## Required Godstorm golden assertions

The fixture must derive, from selected repository evidence rather than handwritten expected presentation prose:

- two top-level structures: Marrow Vaults and Stormcourt;
- 25 battles each / 50 total;
- five keeper fights each / 10 total;
- encounter cadence represented as four normal/ascendant encounters followed by one keeper, repeated five times;
- 18 distinct AI records;
- complete current roster;
- exact art coverage for all 18 roster entries, with provenance;
- Marrow full clear: 125000 ryo / 25 tokens / 10 prestige / no reward item;
- Stormcourt full clear: 250000 ryo / 150 tokens / 60 prestige / no reward item;
- zero intermediate cash-out nodes;
- top-level locations are Marrow Vaults and Stormcourt, not scene-background variant names;
- narrative source IDs resolve against current quest dialogue.

The dossier may carry more facts, but these must be explicit test assertions.

## Negative/adversarial fixtures

At minimum prove refusal or warning for:

- old floor cash-out/chest table trying to override current rewards;
- one missing keeper under `coverage:"all"`;
- swapped/wrong AI image;
- same-size wrong image;
- a scene background being declared a top-level location without explicit presentation semantics;
- nonexistent/stale dialogue objective id;
- old Tower/Dawnless wording supplied as current narrative source;
- unverified/missing evidence source;
- historical-only art selected where exact-current is required.

## Safety and provenance

- ZERO LIVE REQUESTS / ZERO LIVE WRITES.
- No game credential/session material.
- Tests use repository evidence, fixtures and local/in-process tooling only.
- Hard facts must carry enough provenance for review to identify the source record/capture.
- Current capture/live evidence wins over old planning tables for current-state facts.
- A presentation dossier/spec is a derivative; it must not become a second content database.

## Testing/gates

Run all relevant existing Forge gates in addition to focused tests.

At minimum report:

- `npm test`;
- bundle build and reproducibility;
- bundle budget before/after;
- import/boundary checks;
- release-pin check;
- fixture status;
- any presentation-tool-specific selftests;
- exact Godstorm golden output summary.

Do not weaken existing gates to make the feature fit.

## Handoff

When P0/P1 is complete:

1. freeze the exact SHA;
2. do not merge;
3. provide a compact implementation handoff with:
   - Repository
   - Branch
   - Base
   - Merge-base
   - Frozen Head
   - Changed files/surfaces
   - P0 size measurements
   - P1 contract/model summary
   - Godstorm golden results
   - Tests/gates
   - Known debt
   - Live requests/writes
   - Source pins
   - Explicitly not begun
4. request independent ChatGPT review against the frozen SHA.

## Explicitly not begun in this handoff

- P2 deterministic poster/staff-brief renderer;
- P3 Presentation Studio UI;
- new publish actions;
- arbitrary WYSIWYG designer;
- LLM narrative generation inside Forge;
- generative replacement art;
- changes to `state/prompt_forge_next_phase1.md`;
- Quest Studio integration;
- live-game operation.

The separate ChatGPT design/review session may elaborate P2/P3 design in parallel. Treat that as a design contract source after it is committed/reviewed; do not write into its branch.
