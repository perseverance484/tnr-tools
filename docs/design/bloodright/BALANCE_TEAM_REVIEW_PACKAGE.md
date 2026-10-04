# Bloodright balance-team review package

**Status:** FOUNDATION / fill after Fable roster-wide rebalance  
**Date:** 2026-10-04  
**Source authority:** repository Bloodright tree JSON + generated evidence at a frozen exact SHA  
**Generated deliverables:** workbook and visual review pack are review surfaces, not canonical sources

## 1. Deliverables

The completed package contains:

1. `BLOODRIGHT_DESIGN.md`
2. `Bloodright_Balance_Workbook.xlsx`
3. Bloodright tree review pack (PDF or HTML, one bloodline per page)
4. package source-lock note with repository, branch and exact SHA

## 2. Workbook sheets

### 00 — How to Review
One-screen instructions:
- what BU means;
- what BU does not mean;
- color legend;
- review order;
- source SHA;
- package generation date;
- canonical-source warning.

### 01 — Tag Weights
Editable calibration surface.

Columns:

- Tag
- Display name
- Unit
- Suggested starting BU / unit
- Team BU / unit
- Normal ceiling
- Hard ceiling where applicable
- Leverage class
- Engine / design note
- Ratified? (Yes/No)
- Reviewer note

The **Team BU / unit** column is the only weight column used by workbook formulas.

Initial suggested weights are calibration hypotheses, not canon.

### 02 — All Skills
One row per skill node.

Columns:

- Bloodline
- Rank
- Classification
- Foundation
- Tier
- Skill ID
- Skill name
- Cost BP
- Parent IDs
- Tag 1
- Value 1
- BU 1
- Tag 2
- Value 2
- BU 2
- Tag 3
- Value 3
- BU 3
- Node BU
- Eligible jutsu
- Eligible rows
- Status
- Reviewer proposed tag/value fields
- Review note

### 03 — All Routes
One row per Advanced Art / three-node specialization.

Columns:

- Bloodline
- Foundation
- Advanced Art
- Route identity
- Foundation node
- Hidden node
- Advanced node
- 3-BP BU
- Primary tag
- Primary total
- Eligible jutsu
- Eligible rows
- Damage threshold flag
- Downstream leverage
- Strongest fourth purchase
- 4-BP BU
- 4-BP modifier package
- Sibling BU delta
- Review flag
- Reviewer note

### 04 — Bloodline Review
Meeting-facing sheet.

At finalization this sheet should support one selected bloodline and show:

- bloodline metadata;
- two Foundation sentences;
- simplified 2 / 4 / 4 tree;
- modifier values;
- node BU;
- three-BP route totals;
- strongest fourth-BP build;
- coverage / threshold warnings;
- canonical vs proposed values;
- reviewer comments.

If a fully dynamic selector is inconvenient, generate one review block per bloodline instead. Accuracy and readability are more important than spreadsheet cleverness.

### 05 — Fourth BP
Every Advanced path crossed with every legal fourth purchase.

Columns:

- Bloodline
- Advanced Art
- 3-BP node IDs
- Fourth purchase
- Legal?
- 3-BP BU
- Fourth-node BU
- 4-BP BU
- Complete modifiers
- Coverage note
- Dominance warning
- Reviewer note

### 06 — Damage Thresholds
One row per affected Damage jutsu / allocation.

Columns:

- Bloodline
- Route / allocation
- Jutsu
- Base Damage
- Added Damage
- Final Damage
- Base tier
- Final tier
- Tier delta
- >50 flag
- Eligible row count
- Notes

Conditional formatting:
- final > 50 = red;
- 45 -> 50 = amber/red;
- any tier crossing = amber;
- no tier change = neutral.

### 07 — Tag Coverage
Normalized kit evidence.

Columns:

- Bloodline
- Tag
- Distinct jutsu
- Effect rows
- Base values
- Delivery
- Duration
- Recipient
- Classification-wide note
- Downstream leverage
- Item gated?
- Mode restricted?
- Evidence status

### 08 — Review Decisions
Human decision ledger for the balance session.

Columns:

- Bloodline
- Skill / Route
- Issue
- Current value
- Proposed value
- Rationale
- Reviewer
- Status
- Director decision
- Repo reconciliation status

Status values:
- Not reviewed
- Discuss
- Proposed
- Director approved
- Rejected
- Repo reconciled

### 09 — Calibration Cases
Director-reviewed examples used to reason about the BU table.

Start with:
- Taiyo Kami
- Ethereal Monarch
- Shakunetsu Sakura
- Blood-Enchanted Eyes
- Arashima

Show:
- route identity;
- exact modifiers;
- nominal BU under current weights;
- coverage;
- important leverage lesson;
- why the route was accepted/rejected during review.

## 3. Suggested BU starting hypotheses

These are placeholders for calibration, not rulings.

| Tag | Unit | Suggested starting BU / unit | Reason to challenge |
|---|---|---:|---|
| Damage | +1 flat | 3.0 | threshold-sensitive; often affects multiple attacks |
| Increase Damage Given | +1% | 1.0 | multiplicative damage modifier |
| Increase Damage Taken | +1% | 1.0 | multiplicative; can benefit later attacks |
| Decrease Damage Taken | +1% | 1.0 | multiplicative mitigation |
| Decrease Damage Given | +1% | 1.0 | multiplicative suppression |
| Lifesteal | +1% | 2.0 | downstream healing scales with damage |
| Afterburn | +1% | 1.5 | one application may affect many later hits |
| Reflect | +1% | 1.25 | downstream return damage with cap behavior |
| Heal | +1 displayed unit | 1.0 | actual value depends on underlying Heal row |
| Increase Heal | +1% | 1.0 | downstream heal amplification |

The team is expected to edit these weights.

The workbook should recalculate immediately.

## 4. Formula principles

Nominal node BU:

`SUM(modifier_value * team_weight_for_tag)`

Nominal route BU:

`Foundation node BU + Hidden node BU + Advanced node BU`

4-BP BU:

`route BU + selected legal fourth-node BU`

Do **not** automatically multiply BU by eligible-row count.

Coverage is shown next to the BU score as impact context.

## 5. Conditional review flags

### Red
- final Damage > 50;
- hard ceiling exceeded;
- illegal allocation;
- missing required source data.

### Amber
- any Damage tier crossing;
- 45 -> 50;
- large sibling BU delta;
- unusually broad coverage;
- unusually high downstream leverage;
- fourth BP produces a disproportionate jump;
- narrow tag receives extreme magnitude.

### Neutral / Green
No structural or high-priority mechanical warning.

Green does not mean “balanced”; it means “no automatic triage flag.”

## 6. Source lock

The completed package must display:

- repository;
- source branch;
- frozen source SHA;
- merge-base / main where useful;
- package-generation date;
- statement that no live-game requests/writes were performed.

If the source SHA changes, regenerate the package.

## 7. Finalization checklist after Fable handoff

When Fable returns the roster-wide rebalance:

1. Verify exact frozen Fable SHA.
2. Review Fable handoff and tests.
3. Re-read all trees changed since this foundation.
4. Pull final `balance_matrix.json`, fourth-BP audit, damage-threshold audit and kit dossiers.
5. Populate the workbook tables.
6. Replace workbook placeholder weights only if the balance team/director has ratified new values.
7. Populate calibration cases from current canonical/director-approved trees.
8. Generate one review page per bloodline from exact SVG/tree structure.
9. Scan workbook flags.
10. Produce a short “balance-team attention list.”
11. Freeze package against exact SHA.
12. Do not reconcile balance-team edits back to canonical tree JSON until the director approves them.

## 8. Items deliberately deferred until Fable completes

- final roster count;
- final changed-tree list;
- final route identities for batch-adjusted trees;
- exact fourth-BP combinations;
- exact damage-threshold table;
- exact coverage values;
- final workbook route/skill rows;
- balance-team attention queue;
- final visual review pack.

This keeps the foundation stable while Fable's active branch is still changing.
