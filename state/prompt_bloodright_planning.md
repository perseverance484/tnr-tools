# Bloodright: plan the remaining eligible bloodline trees

**Recipient:** Claude on Fable 5.1 Ultracode, as requested by dauntless.  
**Status:** PLANNING BRIEF READY; ROSTER AWAITING USER SORTING.  
**Repository:** `perseverance484/tnr-tools`.  
**Reviewed main:** `03f2931297940ac29faa7c255c94bc15e477323f` (2026-10-03 UTC / 2026-10-02 America/Chicago).  
**Work:** Design proposals and local analysis only. No engine implementation, production manifests, game writes, deployment or image generation.

## Start here

Read `CLAUDE.md`, `state/active-context.md`, `state/status.json`, `docs/00_INDEX.md`, relevant `docs/RULINGS.md` entries and `docs/DEVELOPMENT_WORKFLOW.md`. Then read `docs/design/BLOODRIGHT_DESIGN_BRIEF.md`, `docs/design/bloodright/ROSTER_REVIEW.md`, `roster.json`, and the Taiyo Kami example files under `docs/design/bloodright/examples/`.

Use the supplied committed handoff as the task contract. The reviewed main's state files describe other work and do not contain this session's Bloodright design. Earlier Potency/Mandala designs, 20/30 normal-SP budgets, incremental purchases, elemental attunement schools, generic specializations and mixed Fire/Scorch trees are superseded **for this proposal**. Do not restore them from an older branch or report. Repository governance and source-evidence rules still apply.

Work on your own `fable/bloodright-planning-*` branch. Never write to the handoff's active `chatgpt/*` branch. Import only the handoff files from the final handoff SHA or branch supplied by dauntless; do not merge the old Potency implementation/design history just to obtain an example. Re-verify current refs before starting and preserve unrelated work.

## Assignment

Produce individually themed Bloodright skill-tree proposals for **every bloodline the user approves in the eligibility roster, except Taiyo Kami**, which is the reference design. Plan all approved entries, including those with narrow kits; never quietly drop a difficult bloodline. Identify unsupported or unaddressable kits as blocked with a precise reason instead of inventing mechanics.

The user explicitly delegates **draft design work** to you. You may propose node names, paths and numbers within this brief without stopping for approval on each draft. The user retains final balance acceptance. Do not promote proposals into game canon, rewrite jutsu, or implement the engine to make a proposal work.

## Phase 0: roster before trees

The supplied census contains 95 letter-ranked records: 51 visible and 44 hidden. Its public kits were captured on 2026-10-01; hidden inventory/jutsu evidence is from 2026-09-30. It is a review input, not a certified current complete roster. The listing used by the capture excludes null-rank records. Visibility and rank do not prove that a bloodline is standard, custom, obtainable or retired.

Exclude Borrowed Awakening, custom/player-owned bloodlines, and bloodlines with no bloodline jutsu, as instructed. Also flag test/dummy records and obsolete variants for sorting. Never infer custom ownership from a name, H rank or `hidden` alone. Do not treat a hidden kit as a missing kit. Keep distinct IDs distinct until the user confirms they are aliases or variants.

`roster.json` initially has an empty `approved_remaining_ids` list. Obtain the user's classification, record include/exclude/hold decisions and reasons by stable bloodline ID, and freeze the approved roster. **Do not begin the all-bloodline design batch while that gate remains open.** You can complete the source review and evidence-gap list first. If the user has already sorted it in a later committed revision, use that revision without asking again.

Resolve missing records through existing captures and repository evidence first. If those cannot establish the complete population, request the specific read-only capture needed from dauntless. Do not use live account/session credentials, run the game, or issue live-game writes. Do not silently use a failed query as proof that a kit is empty.

## Phase 1: kit and selector audit

For every approved entry, identify native/equippable jutsu, optional item-gated jutsu, hidden/retired records, and recursively injected actions separately. Record effect rows, supported tags, original element scopes, targets, power plus level scaling, action cost, cooldown and duration. Retain both rows if the same supported tag appears twice.

Audit the proposed bloodline potency classification separately from combat elements. Verify whether it uniquely selects the intended kit; check collisions with other bloodlines, normal jutsu, aliases and injected children. Do not assume every bloodline already has an exclusive usable element. Do not use an analysis-only `bloodlineId` or `jutsuId` filter as though the production potency resolver supports it.

Pin the source used for mechanical claims. Supplied current-source review pin: `studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050`. A fresh source does not prove live deployment. If refreshed records differ from the supplied snapshot, show the change and update calculations without silently changing the approved Taiyo Kami example.

## Phase 2: propose each tree

Use at most 10 meaningful named skills, 4 BP total, 1 BP per once-only purchase, Foundations / Hidden Arts / Advanced Arts, forks only, and a graph in which two Advanced Arts cost more than 4 BP including prerequisites. Taiyo Kami supplies one successful topology, not a mandatory stencil. Aim for 2–3 distinct complete build choices where the kit supports them, with optional fourth-purchase choices. Do not pad a small kit to ten nodes or reskin one generic tree across the roster.

Work backwards from finished four-purchase kits. Declare a primary emphasis, secondary emphasis and tertiary support. Show exact final effect-row values for 2–3 representative legal builds, then justify the node split. Use static increases to existing supported tags; audit the number of affected jutsu and repeated rows before setting numbers. Advanced Arts are the strongest commitment rewards, Hidden Arts are meaningful intermediates, Foundations are broadly useful support within that bloodline's kit.

## Phase 3: cross-roster review

Enumerate all affordable prerequisite-closed allocations for each proposed tree, not just advertised builds. Check reachability, impossible double-Advanced purchases, unused nodes, hidden dominant combinations, duplicate-tag amplification and coverage. Compare marginal benefit across bloodlines using the same assumptions; distinguish inherited rank/kit strength from the added strength of Bloodright. Mechanical legality and non-dominance do not prove combat balance.

Report broad basic-element leakage, main-tree stacking, sustain/reflect amplification, percent caps, delivery/uptime constraints, item restrictions and injection behavior. Keep unproven interactions explicit. Do not claim an ideal/meta build or equal win rates without suitable combat evidence.

## Required deliverables

Place design outputs under `docs/design/bloodright/`:

1. Final approved roster and exclusion ledger, with every census record accounted for and newly discovered records added.
2. A source/kit dossier per approved bloodline.
3. One structured tree JSON plus readable Markdown and a deterministic SVG per proposed tree. SVGs show costs, tiers, full effect names/values, scope, target roles and unambiguous prerequisite arrows.
4. Two or three complete build examples per tree, with all 4 purchases and before/after effect-row tables. Explain genuine narrow-kit exceptions.
5. A cross-bloodline balance matrix and validation results, including all legal allocations and the strongest found combinations.
6. An engine-gap register and open user decisions, separate from design deliverables.

Progress in reviewable batches: first 3–5 contrasting approved kits, then the remaining roster with checkpoints. Continue draft planning within the authorized scope; do not repeatedly ask permission to do the next approved bloodline. Reserve final acceptance for the user.

Return exact branch/base/head SHAs, changed paths, sources, actual validation commands/results, completed versus blocked bloodlines, deviations and what has not begun. If you add reusable validators/tooling, identify that Lane A work and its independent-review surface. Do not modify canonical contracts/doctrine as a side effect. No live manifest is being delivered, so do not imply a manifest-validation result that was never run.

## Exit criteria

Every approved remaining bloodline has either a complete evidence-backed proposal or an explicit source/engine blocker; every excluded entry has a reason; all graphs satisfy the four-purchase rule; every affected effect row is auditable; no production implementation, release or live write has begun.
