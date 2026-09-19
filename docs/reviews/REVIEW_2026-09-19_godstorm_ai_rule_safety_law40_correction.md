# Correction — Godstorm AI Law 40 audit

Date: 2026-09-19  
Status: ACTIVE correction; supersedes the range conclusion in `REVIEW_2026-09-19_godstorm_ai_rule_safety.md`.

The prior audit incorrectly treated an AI rule's `distance_lower_than` value as direct hex distance. TNR Engine Law 40 states that the AI rule distance is A* path length including both endpoints, so a jutsu with combat range R must use an exact profile gate of **R+1**. SELF-target and ALL-method jutsu take no distance gate.

The Forge preflight correctly exposed this error on the first attempted final manifest before any mutation was sent.

## Corrected retained-AI rule policy

For all 18 retained Godstorm profiles:

- `use_specific_jutsu` with an opponent-targeted SINGLE jutsu: exact `distance_lower_than = jutsu.range + 1`.
- `use_combo_action`: all captured combo members here are opponent-targeted SINGLE jutsu with the same range; use that shared `range + 1` gate.
- SELF-target jutsu: remove distance gates.
- ALL-method jutsu: remove distance gates.
- Action target must continue to match the jutsu target class.
- Existing bounded adjacent `use_highest_power_action(effect=damage)` fallback remains guarded at path distance <=2.

Applied corrections across the retained roster:
- 10 specific offensive gates corrected.
- 18 combo gates corrected.
- 18 distance conditions removed from SELF jutsu rules.
- 18 profiles re-audited with zero remaining target/gate findings under this contract.

The existing blank scene character `1YXbXYW2wz3GETVMb6DT6` ("Blank Scene Character", SCENE_CHARACTER, hidden) is used as the quest-level fallback and on all 52 retained dialog nodes.

Corrected executable manifest:
`push/50_godstorm_two_pyramid_final_update_v2.json`.

The preflight-failing `push/49_godstorm_two_pyramid_final_update.json` was removed from `main` so it cannot be selected accidentally.

No live write was performed by ChatGPT.
