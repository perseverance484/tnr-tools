# Bloodright balance workbook data contract

**Status:** FOUNDATION / producer-neutral  
**Purpose:** define the normalized data needed to populate the balance workbook after Fable freezes the roster-wide rebalance.

The package may be populated by a future script or by a one-time extraction. The repository tree JSON remains canonical.

## Dataset A — tag weights

Required fields:

- tag_key
- display_name
- unit_label
- suggested_bu_per_unit
- team_bu_per_unit
- normal_ceiling
- hard_ceiling
- leverage_class
- note
- ratified

## Dataset B — skills

One record per tree node.

Required fields:

- bloodline_slug
- bloodline_name
- rank
- classification
- foundation_id
- foundation_name
- node_id
- node_name
- tier
- cost_bp
- parent_ids
- modifiers[]:
  - tag
  - value
  - display_role
- eligible_jutsu_count
- eligible_row_count
- status
- source_tree_path
- source_sha

Derived in workbook:

- modifier BU
- node BU

## Dataset C — routes

One record per Advanced Art.

Required fields:

- bloodline_slug
- foundation_id
- hidden_id
- advanced_id
- route_identity
- node_ids
- modifier_totals
- eligible_jutsu_count_by_tag
- eligible_row_count_by_tag
- strongest_fourth_purchase_id
- strongest_fourth_package
- review_flags
- source_sha

Derived in workbook:

- 3-BP BU
- 4-BP BU
- sibling BU delta

## Dataset D — fourth-BP allocations

One record per legal fourth purchase for each Advanced route.

Required fields:

- bloodline_slug
- advanced_id
- route_node_ids
- fourth_node_id
- full_node_ids
- modifier_totals
- legal
- dominance_flags
- source_sha

## Dataset E — damage thresholds

One record per affected Damage jutsu / relevant allocation.

Required fields:

- bloodline_slug
- route_or_allocation
- jutsu_id
- jutsu_name
- base_damage
- added_damage
- final_damage
- base_tier
- final_tier
- tier_delta
- over_50
- source_sha

## Dataset F — tag coverage

One record per bloodline/tag.

Required fields:

- bloodline_slug
- tag
- distinct_jutsu_count
- effect_row_count
- base_values
- delivery_summary
- duration_summary
- recipient_summary
- item_gated_count
- mode_restricted_count
- classification_scope_note
- downstream_leverage_note
- evidence_status
- source_sha

## Dataset G — calibration cases

One record per manually reviewed route.

Required fields:

- bloodline
- route
- status
- exact_modifiers
- coverage_summary
- important_leverage_lesson
- director_note
- ruling_id_if_any
- source_sha

## Package invariants

- Every workbook row must trace to a source SHA.
- Canonical and reviewer-proposed values must occupy separate fields.
- Proposed spreadsheet edits never silently replace canonical values.
- Damage tier fields are derived from the player-jutsu ladder: 38 / 40 / 45 / 50.
- No workbook formula may treat BU as proof of combat parity.
- No live request is required to populate the package.
