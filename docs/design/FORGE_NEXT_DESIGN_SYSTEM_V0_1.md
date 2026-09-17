# Forge Next — Design System v0.1

**Status:** DESIGN-SUPPORT PROPOSAL — FOUNDATION LAYER ONLY  
**Date:** 2026-09-12  
**Branch:** `chatgpt/forge-next-planning`  
**Depends on:** `docs/design/FORGE_NEXT_VISUAL_DIRECTION.md`  
**Scope:** visual foundations, component language, semantic state presentation, motion, responsive constraints  
**Out of scope:** final information architecture, screen map, backend architecture, auth model, manifest contracts, Builder retirement, procedure capability decisions

## 1. Intent

This file turns the approved Forge Next visual north star into a reusable design-system foundation that can be applied to whatever screen architecture Fable's planning pass ultimately recommends.

It deliberately avoids deciding navigation, feature grouping, content taxonomy, backend behavior or workflow architecture. Those remain planning/implementation questions for Fable and user review.

The design objective is a **professional TNR operations console**: dark, atmospheric, first-party-feeling, highly legible under production pressure, and a little flashy through controlled depth, light, motion and branded visual character.

## 2. Core principles

1. **Operational clarity before spectacle.** Flash reinforces state; it never obscures it.
2. **TNR character without game-screen cosplay.** Forge should feel born from the same world, but purpose-built for staff/content operations.
3. **Mobile is a first-class layout, not a collapsed desktop.** Touch targets, density and disclosure are designed for phones from the start.
4. **Semantic state always wins over decorative color.** Lane accents never redefine success, danger, warning, ambiguity or publishing.
5. **Human language first, raw technical detail second.** IDs, procedures and payloads remain available but should not dominate ordinary workflows.
6. **Uncertainty is visible.** Ambiguous writes, unread results, authentication failure and permission denial must never inherit success styling.
7. **Consistency creates speed.** Repeated operations should reuse the same visual grammar across content classes.

## 3. Foundation palette

These are proposed design tokens, not implementation requirements. Exact values may be tuned during accessibility/contrast review.

### Neutral surfaces

| Token | Proposed value | Role |
| --- | --- | --- |
| `forge.bg.canvas` | `#070B12` | deepest page/background field |
| `forge.bg.shell` | `#0B111B` | navigation/application shell |
| `forge.bg.panel` | `#111A28` | default cards/panels |
| `forge.bg.panelElevated` | `#172235` | selected/raised cards, popovers |
| `forge.bg.panelSoft` | `#1D2A3D` | hover/secondary fills |
| `forge.border.subtle` | `#29384D` | standard dividers/borders |
| `forge.border.strong` | `#40526C` | focused or high-attention border |

### Text

| Token | Proposed value | Role |
| --- | --- | --- |
| `forge.text.primary` | `#F5F1E7` | main operational text |
| `forge.text.secondary` | `#B7C0CE` | supporting copy |
| `forge.text.muted` | `#7F8B9C` | metadata/de-emphasis |
| `forge.text.inverse` | `#111016` | text on light/parchment surfaces |
| `forge.text.parchment` | `#F8F1DC` | warm branded highlight |

### Signature accents

| Token | Proposed value | Role |
| --- | --- | --- |
| `forge.accent.crimson` | `#B7331F` | signature TNR action/brand accent |
| `forge.accent.crimsonBright` | `#E0472C` | active focus/energy edge |
| `forge.accent.gold` | `#D7A33D` | premium/review/admin emphasis |
| `forge.accent.goldSoft` | `#F0C66A` | highlighted text/icon accents |
| `forge.accent.chakra` | `#6BB8FF` | system/active/read-oriented accent |
| `forge.accent.chakraDeep` | `#2269B7` | active blue surfaces |
| `forge.accent.violet` | `#9366FF` | non-semantic lane/decorative accent |
| `forge.accent.teal` | `#35B7AA` | non-semantic lane/decorative accent |

### Semantic colors

These are reserved for operational meaning.

| Token | Proposed value | Meaning |
| --- | --- | --- |
| `forge.state.success` | `#45C779` | verified/succeeded/healthy |
| `forge.state.warning` | `#E6AD45` | caution/pause/needs attention |
| `forge.state.danger` | `#E05F5F` | destructive/refused/failed |
| `forge.state.info` | `#6BB8FF` | safe informational/read context |
| `forge.state.ambiguous` | `#B884FF` | SENT/uncertain/must reconcile |
| `forge.state.neutral` | `#8994A5` | planned/inactive/not yet run |

**Rule:** decorative content-lane colors may visually echo these hues but may not communicate operational state without a label/icon.

## 4. Operation modes

Every consequential workflow should support a persistent human-facing mode treatment. The mode is not the journal state; it summarizes production consequence.

| Mode | Visual family | Required cue |
| --- | --- | --- |
| `READ ONLY` | chakra blue | eye/search/capture icon + explicit label |
| `LIVE WRITE` | crimson | write/bolt/tool icon + explicit production wording |
| `PUBLISH` | gold | publish/visibility icon + explicit audience consequence |
| `RECOVERY` | amber/violet | repair/reconcile icon + explicit uncertainty wording |

A mode header should be capable of showing concise counts such as `12 records · 3 creates · 5 captures · 0 deletes` and a plain-language consequence sentence.

No mode should rely on color alone.

## 5. Typography

### Functional UI face

Use a highly legible system/UI sans for all operational content. The implementation should prefer a robust system stack unless Fable's architecture later establishes a safe bundled font path.

Recommended design reference stack:

`system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`

### Display/brand face

A stylized face may be used sparingly for:

- the `FORGE` mark;
- hero/empty-state headings;
- content-lane identity headings.

It must never be used for:

- form labels;
- warnings;
- diffs;
- IDs;
- logs;
- body copy;
- confirmation text.

### Type scale

Proposed mobile-first hierarchy:

| Role | Size | Weight | Notes |
| --- | --- | --- | --- |
| Brand display | 28–36px | 800/900 | rare |
| Page title | 24px | 750 | one per view |
| Section title | 18–20px | 700 | compact |
| Card title | 15–16px | 650/700 | primary card label |
| Body | 14–15px | 400/500 | default operational copy |
| Meta | 12–13px | 500 | secondary metadata |
| Micro/status | 11–12px | 650 | chips/badges only |

Desktop may increase page/hero typography but should not inflate dense operational text unnecessarily.

### Monospace

Use only for IDs, hashes, procedure names, source paths and raw payload/debug detail.

## 6. Spacing and density

Use a 4px base grid.

Core spacing steps: `4, 8, 12, 16, 20, 24, 32, 40`.

Guidelines:

- default card padding: 16px mobile, 18–20px desktop;
- dense rows may use 10–12px vertical padding but never sacrifice touch targets;
- section separation: 24px mobile, 28–32px desktop;
- minimum interactive target: 44x44px;
- primary mobile action: preferably 48px minimum height;
- avoid horizontal scrolling for ordinary forms/content lists;
- technical tables may become stacked key/value cards on narrow screens.

## 7. Shape language

Forge should avoid both extremes: neither completely square legacy utility UI nor generic heavily rounded SaaS cards.

Recommended geometry:

- panels/cards: 10–12px radius;
- compact controls: 6–8px radius;
- premium/hero lane cards: 10px radius with hard visual framing;
- status pills/chips: fully rounded only when semantically useful;
- high-consequence buttons may use squarer TNR-inspired geometry rather than soft pills.

Use confident 1px borders by default, 2px for selected/focus/high-consequence states.

## 8. Depth, shadows and glow

Depth should make hierarchy obvious, not decorate every edge.

### Standard elevation

- panel: subtle dark shadow and border separation;
- elevated panel/popover: stronger shadow plus slightly lighter surface;
- selected lane/action card: accent edge + controlled outer glow;
- primary TNR-style action: restrained 3–5px offset accent shadow inspired by current TNR ink controls.

### Glow

Allowed for:

- active content lane;
- active run/progress state;
- current system focus;
- selected Quick Action.

Avoid glow around:

- long text blocks;
- forms;
- error messages;
- confirmation dialogs;
- ambiguous/recovery content where strong crisp borders communicate better.

## 9. Buttons and actions

### Primary action

Use for the single most important action in a region. Strong fill, high contrast, clear verb.

Examples: `Run captures`, `Start live write`, `Save changes`, `Approve & publish`.

### Secondary action

Dark/elevated surface, explicit border, no competing glow.

### Quiet action

Text/icon treatment for low-risk secondary actions such as `View details`, `Copy ID`, `Open raw`.

### Destructive action

Semantic danger color plus explicit verb. Never make destructive actions visually identical to a normal primary button.

### Production-action rule

`LIVE WRITE` and `PUBLISH` actions should include consequence-oriented wording rather than generic `Continue`/`Submit` labels.

## 10. Core component vocabulary

These components are architecture-neutral and safe to design before Fable settles the final IA.

### `ForgePanel`

Base layered surface with title, optional description, optional action slot and semantic variant.

### `ForgeActionCard`

High-visibility task entry with icon, action title, one-line explanation and optional count/status.

### `ForgeLaneCard`

Visual content-family entry. Supports decorative artwork/gradient, lane accent, title, examples/subtitle and active state. Accent must not imply success/failure.

### `ForgeStatusChip`

Compact labeled state with icon/shape + color. Examples: `Verified`, `Paused`, `Unverified`, `Needs review`, `Published`.

### `ForgeOperationHeader`

Persistent contextual block for `READ ONLY`, `LIVE WRITE`, `PUBLISH`, `RECOVERY`. Shows consequence summary and counts.

### `ForgeHealthRow`

Compact system/session/repository readiness row with state icon, human label and optional detail/action.

### `ForgeActivityRow`

Human-readable recent action with subject, action, time, status and optional drill-in.

### `ForgeCallout`

Info/warning/danger/recovery blocks. Must support concise title + actionable explanation + next safe step.

### `ForgeProgress`

Determinate/indeterminate operation progress with current phase text. Animation may be energetic but restrained.

### `ForgeField`

Consistent label/help/error/control wrapper for text, select, textarea, switch, upload and structured editors.

### `ForgeDiffRow`

Human-facing before/after presentation with changed-value emphasis and optional raw expansion.

### `ForgeConfirmation`

Confirmation treatment that states: action, production consequence, counts, uncertainty and safe cancel path.

### `ForgeEmptyState`

Can use atmospheric art/brand personality because no critical data competes with it.

## 11. State language

State visuals should distinguish lifecycle concepts clearly.

### Recommended presentation groups

- **Planned / queued:** neutral gray; no success cues.
- **In progress:** chakra blue + motion/progress indicator.
- **Sent / ambiguous:** violet + explicit `Needs reconciliation`; never a green progress check.
- **Confirmed but unverified:** blue/amber hybrid; wording must explain that the write landed but read-back is still owed.
- **Verified:** green + check.
- **Paused / incomplete:** amber + pause/attention icon.
- **Failed/refused:** red + failure icon.
- **Skipped:** neutral muted + skip icon.
- **Published:** gold + visibility/publish icon; publication is a lifecycle state, not synonymous with technical success.

## 12. Forms and editing surfaces

Editing surfaces should prioritize scanability and clear change state.

Guidelines:

- label above control on mobile;
- helper/error text directly below control;
- edited/dirty state should be visible without using danger red;
- field groups use section headings and concise descriptions;
- raw JSON/payload editor is advanced-only and visually separated from normal form editing;
- previews should be visually distinct from editable controls;
- destructive/publish controls should not sit immediately adjacent to ordinary Save actions without separation.

## 13. Content-lane visual system

The current lane names remain illustrative until Fable's taxonomy work is complete. The design system supports any final grouping.

Each lane may define:

- one accent hue;
- one atmospheric/illustrative image style;
- one icon;
- one short descriptor.

Proposed reference palette:

- Combat — crimson;
- Items — chakra blue;
- Quests & Events — gold/amber;
- Locations — teal;
- Characters — violet;
- Systems — steel/neutral.

These are decorative identities only. A red Combat card does not mean danger; a green/teal lane does not mean success.

## 14. Imagery and atmosphere

Use illustration primarily in:

- Command Center hero/brand region;
- content-lane cards;
- empty states;
- onboarding/first-use surfaces.

Do not use atmospheric imagery behind:

- diffs;
- manifests/results details;
- recovery decisions;
- warnings;
- form-heavy editing;
- publish confirmation.

Visual style should be TNR-adjacent: moonlit villages/fortresses, paper/ink motifs, elemental/chakra energy, weapon/tool silhouettes, scrolls and mission-board themes, without prohibited franchise references or copied IP.

## 15. Motion system

Motion should improve orientation and feedback.

### Timing

- micro-interaction: 100–140ms;
- control/card transition: 140–180ms;
- panel expand/collapse: 180–240ms;
- page/major section transition: 180–260ms maximum.

### Motion patterns

- slight press/offset on TNR-style buttons;
- subtle glow ramp on active lane/action card;
- progress pulse/travel during long operations;
- smooth height/opacity expansion for advanced details;
- short success settle animation on verified completion.

### Avoid

- perpetual background particle movement in operational views;
- bouncing critical buttons;
- animated red danger states;
- cinematic page transitions;
- motion that delays interaction.

Respect `prefers-reduced-motion` by removing non-essential transitions/animation.

## 16. Mobile rules

These are design constraints independent of final navigation architecture.

- minimum 44px touch targets;
- no hover-only affordances;
- one clear primary action per decision region;
- critical consequence summary should appear before long detail;
- sticky bottom action areas are acceptable when they do not cover warnings/status;
- multi-column dashboards collapse into prioritized stacked sections;
- technical metadata progressively collapses behind `Details` rather than shrinking type;
- tables become stacked rows/cards when required;
- confirmation actions must remain thumb-accessible without accidental adjacency;
- operation mode and active/recovery state should remain visible during long workflows.

## 17. Desktop/tablet rules

- use available horizontal space for meaningful parallel context, not merely wider cards;
- permit two- or three-column dashboard composition when information groups are independent;
- preserve readable line length for prose/details;
- keep core operation context visible while secondary technical detail can occupy side panels;
- do not require hover for primary actions or state explanation.

## 18. Accessibility baseline

- target WCAG AA contrast for operational text/controls;
- never use color as the sole state cue;
- visible focus treatment on all interactive controls;
- form error messages must be textually associated with the field;
- status icons should supplement, not replace, words;
- motion-reduction support;
- avoid tiny all-caps copy for essential information;
- decorative imagery must not reduce text contrast.

## 19. What remains intentionally unresolved

This v0.1 does **not** decide:

- final nav destinations;
- exact content-lane taxonomy;
- Command Center block ordering;
- whether Content Admin is a top-level route or role-specific shell variant;
- which actions/capabilities actually exist;
- data sources for counts/activity/health;
- final design token implementation technology;
- final icon library;
- final display font;
- exact desktop breakpoints;
- component framework or rendering strategy.

Those questions must be reconciled with Fable's evidence-backed planning output before a production UI brief is written.

## 20. Next design-support pass

After user review of these foundations, the next safe parallel design pass is a **component/style board** showing:

1. palette and typography;
2. button variants;
3. operation-mode headers;
4. status chips and callouts;
5. lane cards;
6. form controls and edit/dirty states;
7. progress/recovery states;
8. representative mobile treatments.

That board should remain component-focused rather than proposing a competing screen architecture while Fable's planning pass is active.
