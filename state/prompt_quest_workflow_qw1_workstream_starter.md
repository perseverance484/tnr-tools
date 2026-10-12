# Fable brief — QW-1: deterministic quest workstream starter

**Status:** DIRECTOR-APPROVED IMPLEMENTATION-PLANNING PASS (2026-10-12; RUL-2026-10-12-016). Bounded Lane A scope, queued after QW-0A's reviewed handoff/integration unless the director deliberately reorders work.  
**Repository:** perseverance484/tnr-tools  
**Design source:** `docs/design/QUEST_CREATION_WORKFLOW_IMPROVEMENT_PLAN_2026-10-12.md`, QW-1; read at the approved `chatgpt/quest-workflow-skyglass-retrospective-20261012` frozen planning SHA.  
**Baseline at planning:** main@4de2668bb947368113683b5cb97e197abc87df27; verify fresh `main` and prior QW-0A outcome before beginning.  
**Owner:** Fable / Claude Code on its own new `fable/*` implementation branch; independent exact-SHA review by ChatGPT.  
**Live boundary:** zero live requests, zero live writes, no credentials, no publication.

## Outcome / operator experience

A future content coordinator can initialize an **optional multi-session quest or event project from one command**, receive a valid, reproducible starter roadmap with realistic stage dependencies and explicit missing-input blockers, and open another session using the existing `init <slug> --task <id>` ritual. The next session requires no predecessor transcript. **Simple one-session quests remain possible through the existing content skill without any workstream.**

This is **repository coordination only**, not a new quest authoring schema, Quest Studio, lore/design template, reward calculator, art generator or source of gameplay rules.

## Required reconstruction

1. Verify repository/main/pending implementation refs; read `CLAUDE.md`, `CHATGPT.md`, `docs/00_INDEX.md`, `docs/DEVELOPMENT_WORKFLOW.md`, `docs/workflows/CONTENT_WORKSTREAM.md`, `docs/RULINGS.md` (including RUL-2026-10-12-016) and the approved roadmap/this brief.
2. Inspect `scripts/content_workstream.py` (`validate`, `render`, `list`, `next`, `init`, `--selftest`), `state/workstreams/one_perfect_crop/roadmap.json`, its generated projections, `docs/workflows/ART_PRODUCTION.md`, `docs/workflows/DIRECTOR_DECISIONS.md`, `docs/workflows/IMPLEMENTATION_HANDOFF.md` and `skills/building-tnr-content/SKILL.md`. Read the actual schema validation before introducing templates.
3. Preserve the existing `roadmap.json` as canonical coordination data, `ROADMAP.md` and `INDEX.md` as generated projections, and the authoritative ownership of content sources, approved art, engine mechanics, captures, global session status and game actions.

## Scope and desired CLI

Extend `scripts/content_workstream.py` with a new deterministic `new`/scaffold subcommand (Fable may choose exact option names if they fit current argparse style), supporting:

- slug, readable title and content class (`quest` / `event`) as explicit input; no guessed gameplay settings;
- safe preview/dry-run and explicit commit-time creation, rejecting an existing target instead of overwriting it;
- a small versioned template/recipe **for task coordination**, not a quest or manifest blueprint;
- deterministic initial `state/workstreams/<slug>/roadmap.json` plus `ROADMAP.md` and shared `INDEX.md` through the existing renderer, not by hand;
- a short final CLI output showing created paths, next missing inputs/decision gates and how to use `validate`/`next`/`init`.

The template may contain task-stage skeletons for: design/quest graph, source/capture inventory, AI/items/reward decisions, prose/art production, build/validation, independent review when tooling scope calls for it, hidden operator execution/readback, calibration, and separate publication decision. Keep sensible task-sized groupings; no one-task-per-image explosion.

**Missing inputs stay blocked/planned.** A scaffold must not invent repository paths, completed approvals, source pins, artwork files, item/AI IDs, source timestamps or user-owned balance values. It must not assign `READY` unless all `required_resources` exist and the current readiness checks pass; `COMPLETE` requires verifiable evidence under the current validator. If the proposed template references a missing task source, it must make it an explicit blocker or omit the pointer until committed.

Retain a single roadmap owner: `state/workstreams/<slug>/roadmap.json`. Avoid extra YAML/JSON status boards, duplicate approval ledgers, or a rival task-status model. Human approval/provenance is a link to existing canonical sources/rulings/captures. Historical handoff bundles can be noted but cannot silently make tasks ready.

## Operational safety / compatibility

- Do not touch `state/digest.json`, `state/active-context.md` or `state/status.json`, or invoke `session_close.py` as part of scaffolding. Those global generated surfaces are not workstream status.
- Never overwrite or silently modify an existing workstream, including One Perfect Crop. Repeated `new` on the same slug must fail clearly with no collateral change.
- Validate input slug/path traversal, safe filenames, content class and shell-escaped titles. No unchecked absolute paths, hidden temporary references, `sandbox:` or external attachment markers in durable `required_resources`.
- Keep Git one-writer rules: Fable may commit implementation and fixtures to its own branch. The scaffold must not push to GitHub or the live game. No implicit background/remote activity.
- Do not alter `validate`/`render`/`next`/`init` behavior to make the new template pass. If the valid task schema cannot express a desired marker, prefer a future scoped schema proposal over a bypass.

## Tests / acceptance

1. `python3 scripts/content_workstream.py --selftest`: extend to cover creation, dry-run/no writes, idempotent/reproducible byte output and negative/error paths.
2. `python3 scripts/content_workstream.py validate --all` and `render --check`: existing One Perfect Crop projections unchanged in an unmodified checkout; generated sample roadmap validates and its projections re-render byte-for-byte. Test in a disposable isolated repo tree so normal tests never create sample state under `main`.
3. Negative controls: duplicate slug, traversal, empty/invalid title, unsupported type, failed/provisional resource references, unanchored `COMPLETE`, cycles/unmet dependencies, and missing/art-only ephemeral assets. The validator must continue to refuse false `READY` claims.
4. End-to-end clean-checkout rehearsal of one multi-session sample modeled on Ghost Ship scale **without recreating historical gameplay data**: instantiate the template, add only real fixture resources, mark a legitimately `READY` task, render, `init` it, record evidence and progress to `COMPLETE`. Prove stale or superseded inputs are clearly surfaced.
5. A simple single-session quest path must remain unaffected. Document how to opt in to the workstream scaffold; do **not** impose it on routine one-session Lane B production.
6. Run relevant existing coherence checks only when affected sources are changed (`doctrinemap` / `render_doctrine --check` / `build_packs --check` / `lawmap`); no generated-art/build step without an actual art change.

## Deliverables

- Focused implementation in `scripts/content_workstream.py` and necessary versioned template/test files, plus focused documentation update to `docs/workflows/CONTENT_WORKSTREAM.md` and the shortest appropriate `docs/00_INDEX.md` routing reference **only if** the router actually needs updating.
- A clear sample/fixture, exact command examples, test results, regression evidence for existing workstreams, and a compact handoff pointing at the new CLI.
- Exact base, merge-base, frozen head SHA, changed paths, test/negative-test commands, generated hashes, compatibility notes and any open director decisions. Stop after review handoff, without integration or a follow-on task starting automatically.

**Explicit exclusions:** general Quest Source/graph compiler (QW-2), new Forge UI/Project Workspace (QW-5), player-facing narrative/rewards, real content edits, historical Ghost Ship release rewriting, unauthorized policy change making roadmaps mandatory for all quests, and any live-game operation.
