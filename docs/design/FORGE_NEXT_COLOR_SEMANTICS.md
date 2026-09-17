# Forge Next — Color Semantics Amendment

**Status:** USER-DIRECTED CORRECTION TO DESIGN SYSTEM v0.1  
**Date:** 2026-09-12  
**Branch:** `chatgpt/forge-next-planning`  
**Applies to:** `docs/design/FORGE_NEXT_DESIGN_SYSTEM_V0_1.md` and all subsequent visual boards  
**Scope:** color semantics only; no IA/architecture/workflow changes

## 1. Ruling

Operation-mode colors and semantic outcome colors must be visually distinct enough that the user cannot reasonably confuse an operation context with a system state.

The first style board reused near-identical red for `PUBLISH` and `ERROR`, and near-identical amber/orange for `LIVE WRITE` and `WARNING`. The project director flagged this as potentially confusing. That concern is accepted and this amendment supersedes those color pairings.

## 2. Revised operation-mode families

Operation modes describe **what kind of action is being performed**. They are not success/warning/error states.

| Mode | Revised visual family | Meaning |
| --- | --- | --- |
| `READ ONLY` | cool cyan / chakra blue | inspection, capture, no mutation |
| `LIVE WRITE` | hot copper / saturated orange | mutation-capable production action |
| `PUBLISH` | magenta / royal violet | audience-visible lifecycle action |
| `RECOVERY` | indigo / deep violet | reconcile, repair, ambiguous-state handling |

These mode colors must always appear with an explicit text label and icon. They may tint headers, borders, or focused controls, but must not replace semantic status messaging.

## 3. Reserved semantic outcome colors

Semantic colors describe **what happened or what attention is needed** and remain reserved:

| Semantic state | Reserved family |
| --- | --- |
| `SUCCESS / VERIFIED / HEALTHY` | green |
| `WARNING / CAUTION / PAUSED / NEEDS ATTENTION` | yellow-amber |
| `ERROR / FAILED / REFUSED / DESTRUCTIVE` | red |
| `INFO` | blue |
| `AMBIGUOUS / SENT / MUST RECONCILE` | violet only when visually distinct from the `PUBLISH` mode treatment; prefer muted lavender plus explicit wording |
| `NEUTRAL / PLANNED` | gray / steel |

## 4. Collision rules

1. `PUBLISH` must never use the same red family as `ERROR` or destructive actions.
2. `LIVE WRITE` must never use the same yellow-amber family as `WARNING`.
3. An operation header and a semantic alert may appear together. Their palettes must remain distinguishable at a glance.
4. Color is never the sole cue: mode label, icon, semantic wording, and shape/border treatment remain required.
5. Decorative content-lane colors remain independent and may not override either operation or semantic color meaning.
6. When a mode itself enters an error state, keep the mode identity in a small contextual marker while the failure message uses the reserved semantic error red. Example: a magenta `PUBLISH` context can contain a red `Publish failed` callout without making the entire page red.

## 5. Recommended reference values

Exact values remain subject to contrast/accessibility tuning, but the intended separation is:

- `mode.readOnly`: `#38BDF8` — cyan
- `mode.liveWrite`: `#F97316` — copper/orange
- `mode.publish`: `#D946EF` — magenta
- `mode.recovery`: `#7C3AED` — indigo/violet
- `state.success`: `#22C55E`
- `state.warning`: `#FACC15`
- `state.error`: `#EF4444`
- `state.info`: `#3B82F6`
- `state.neutral`: `#94A3B8`

The values are references, not implementation locks. The separation of meaning is the binding design rule.

## 6. Visual-board correction

All future Forge style boards and UI mockups should demonstrate the corrected mapping explicitly. The prior board remains an exploratory artifact and should not be used as the semantic-color implementation reference.
