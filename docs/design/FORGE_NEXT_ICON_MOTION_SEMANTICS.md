# Forge Next — Icon and Motion Semantics

**Status:** DESIGN FOUNDATION — LIBRARY-AGNOSTIC / COLOR-AGNOSTIC  
**Date:** 2026-09-12  
**Branch:** `chatgpt/forge-next-planning`  
**Depends on:** visual direction, safety-state presentation contract, design system v0.1, interaction-risk matrix  
**Lead lens:** UI/UX Reviewer  
**Supporting lens:** Art Director  
**Scope:** icon metaphor, shape cues, and motion behavior used to reinforce operational meaning  
**Out of scope:** exact icon library, exact SVG paths, final operation-mode taxonomy, final palette, implementation framework

## 1. Purpose

Forge Next should not rely on color to communicate state. Icons, shape, wording, and motion must form a second channel.

This document establishes semantic roles for those channels without locking a particular icon set or visual library.

## 2. Three visual-semantic layers

Do not reuse one visual language for all three layers.

### Layer A — operation context

Answers: **what kind of work is this?**

Examples: read/inspect, write, review, publish, recovery.

Operation icons may appear in headers, mode selectors, and action cards. They are persistent context, not success/error indicators.

### Layer B — outcome/state

Answers: **what happened?**

Examples: verified, warning/paused, failure, info, ambiguous/unverified, neutral/planned.

Outcome icons belong in status chips, callouts, result summaries, and item rows.

### Layer C — object/content identity

Answers: **what kind of thing is this?**

Examples: combat, item, quest/event, location, character, system, asset, manifest/package.

Decorative lane/content icons must not be reused as state indicators.

## 3. Operation-context metaphors

These are metaphor families, not exact library requirements.

### Read / inspect

Preferred metaphors:

- eye;
- search/magnifier;
- capture frame;
- document inspection.

Avoid metaphors that imply download/export if the operation is only reading.

### Write / mutation

Preferred metaphors:

- pen/edit tool;
- forge/hammer/tool;
- bolt/energy only if paired with explicit text;
- document-with-edit mark.

Avoid checkmarks: a write action is not a success state.

### Review

If `Review` survives transcript/IA reconciliation as a distinct context, preferred metaphors include:

- magnifier over document;
- comparison/diff;
- person/document review;
- clipboard inspection.

Avoid using the same eye icon as plain read-only unless text/shape clearly separates the contexts.

### Publish

Preferred metaphors:

- visibility/eye with outward cue;
- upload/outward arrow only if publication is genuinely the semantic meaning;
- broadcast/visibility mark;
- open/public state symbol.

Avoid trash/destructive metaphors and ordinary success checkmarks.

### Recovery

Preferred metaphors:

- circular reconcile arrows;
- wrench/repair;
- broken-to-restored link;
- circular arrows around a record/document.

Avoid refresh/retry icon alone; recovery is not always repetition.

## 4. Outcome/state metaphors

### Verified / success

Preferred:

- check mark in a stable enclosing shape;
- completed verification seal/check circle.

Use only when evidence supports the positive state.

### Info

Preferred:

- `i` information symbol;
- neutral dot/indicator when space is tight.

### Warning / pause / needs attention

Preferred:

- exclamation triangle or clearly cautionary shape;
- pause symbol for literal paused state, optionally paired with warning cue when attention is required.

Do not use warning icon for all non-success states.

### Error / failed / refused

Preferred:

- `x` / cross;
- stop/octagonal or strong failure mark where appropriate.

Destructive action icons (trash) remain separate from failure icons.

### Ambiguous / needs reconciliation

This needs its own metaphor.

Preferred:

- reconcile/circular arrows with uncertainty mark;
- split/branch question;
- unresolved link/loop;
- question mark paired with reconcile shape.

Avoid:

- warning triangle alone;
- refresh icon alone;
- success check;
- error cross alone.

The user should be able to distinguish `needs attention` from `result uncertain` without relying on color.

### Planned / neutral

Preferred:

- hollow circle;
- queue/list position;
- clock only when time/queued meaning is actually relevant.

### Skipped

Preferred:

- skip-forward style mark;
- horizontal minus/dash in a neutral enclosure.

Avoid success check.

## 5. Job and item icon rules

A job row may need both operation context and outcome state.

Example composition:

- leading operation icon: what kind of work the package does;
- trailing/status icon: current evidence/outcome.

Do not attempt to encode both meanings into one overloaded icon.

## 6. Shape semantics

Shape can reinforce meaning independently of color.

### Stable completion

Closed, symmetric shapes work well for verified/finished states.

### Caution

Angular/triangular geometry can reinforce attention.

### Destructive

Squared/high-contrast bordered controls with destructive icon and explicit verb are preferable to decorative glow.

### Ambiguity/recovery

Circular/looping geometry can imply reconciliation/process, but must be paired with text so it does not read as ordinary refresh.

### Operation modes

Mode selectors may use consistent rectangular/tile geometry with mode-specific icon + label. Shape should remain common across modes so the meaning difference is carried by icon/label/accent rather than suggesting one mode is inherently successful or dangerous.

## 7. Icon consistency rules

- Use one stroke family/weight across operational icons.
- Use filled variants sparingly for selected/active state, not to change semantic meaning.
- Do not mix highly detailed fantasy illustrations with simple line-status icons in the same hierarchy.
- Icons must remain readable at the small sizes used in chips/rows.
- Every safety-relevant icon has an accessible text label or adjacent wording.
- Tooltips may supplement but cannot carry essential meaning alone.
- Do not depend on hover to explain an icon.

## 8. Decorative content-lane icon rules

Content-lane icons may be more expressive than operational status icons, but still need a coherent family.

Directionally appropriate metaphors from the latest board include:

- Combat — crossed weapons/combat silhouette;
- Items — flask/bag/object;
- Quests & Events — scroll/document/mission marker;
- Locations — map/pagoda/location mark;
- Characters — person/silhouette;
- Systems — cube/gears/tooling.

These remain illustrative until taxonomy is final.

A crimson Combat icon does not mean error. A teal Location icon does not mean success.

## 9. Motion roles

Motion in Forge has four legitimate roles:

1. indicate ongoing work;
2. acknowledge an interaction;
3. help spatial orientation during expansion/navigation;
4. settle a state transition after evidence changes.

Motion should not be used merely because a region is visually important.

## 10. Ongoing-work motion

### Allowed

- subtle progress travel/pulse;
- restrained rotating/looping indicator for reconciliation/probing;
- determinate progress movement when real progress exists;
- small active edge/glow response around the currently running item/mode.

### Required behavior

- pair indeterminate motion with phase text;
- stop motion promptly when the state stops;
- reduced-motion mode replaces traveling/pulsing animation with static state plus text.

### Avoid

- pulsing red error panels;
- bouncing primary buttons;
- continuous background particles behind forms/logs;
- fake determinate percentages when the backend cannot provide them.

## 11. State-transition motion

### Verification success

Allowed: short, one-time settle/appearance of verified check/state.

Not allowed: celebratory confetti, prolonged glow, repeated pulse.

### Failure

Prefer crisp immediate state change. Do not shake forms/dialogs as the only error cue.

### Pause

Stop active-running motion; transition to static pause/attention state.

### `SENT` ambiguity

If motion is used, prefer a restrained unresolved/reconcile loop, not a spinner that implies Forge is still automatically working when it actually requires operator action.

### Recovery resolved

A brief transition from ambiguity/recovery treatment to confirmed/verified is acceptable when the evidence genuinely changes.

## 12. Navigation and disclosure motion

### Page/section transitions

Use short fade/slide only when it reinforces spatial orientation. Do not delay interaction.

### Expand/collapse

Height/opacity transitions may help reveal technical detail but should remain short and interruptible.

### Bottom sheets/modals

A short entrance is acceptable. Focus behavior and immediate interactivity are more important than animation.

## 13. Duration guidance

Carry forward the design-system reference ranges unless accessibility/performance review requires adjustment:

- micro feedback: roughly 100–140ms;
- control/card transition: roughly 140–180ms;
- panel expand/collapse: roughly 180–240ms;
- major view transition: roughly 180–260ms maximum.

These are reference ranges, not implementation locks.

Avoid easing/durations that make controls feel sluggish under repeated operational use.

## 14. Reduced-motion contract

When `prefers-reduced-motion` is active:

- remove traveling glows and decorative pulses;
- eliminate nonessential page/card motion;
- keep determinate progress understandable through static bar/value/text updates;
- keep state icons/labels unchanged;
- do not remove evidence or status information;
- allow minimal opacity changes where needed for immediate feedback if they are not vestibular/disorienting.

## 15. Motion and production consequence

Do not use more animation merely because an action is more dangerous.

Danger/publication/recovery should gain **clarity and deliberate structure**, not theatrical motion.

In particular:

- publish confirmation should be calm and explicit;
- error should be crisp and readable;
- recovery should visually slow the decision down through layout/copy, not distracting animation;
- verified completion may feel satisfying but must remain professional.

## 16. Loading/progress semantics

### Spinner/indeterminate indicator

Means only: work is ongoing and completion fraction is unknown.

It must not mean:

- success pending;
- server accepted the write;
- verification is guaranteed.

### Determinate bar

Use only when numerator/denominator is meaningful.

For jobs, consider explicitly labeling what the fraction counts (items resolved, phases complete, reads complete) so `100%` cannot be mistaken for verification success.

### Skeletons

Acceptable for loading non-critical lists/cards. Avoid skeleton placeholders for safety-critical status where a neutral `Checking…` label is clearer.

## 17. Notification motion

Transient toasts may enter/leave subtly.

Durable critical states should not auto-dismiss and should not depend on animation for discovery.

No critical error/recovery message should disappear merely because an animation timer elapsed.

## 18. Accessibility and icon labeling

- Status icon must have adjacent visible text in primary safety contexts.
- `aria-label`/accessible name should describe the state/action, not the glyph (`Verified`, not `check icon`).
- Decorative lane artwork/icons may be hidden from assistive technology when the text label already names the lane.
- Icon-only compact controls need accessible names and sufficiently large targets.
- Do not encode multiple independent state axes into one inaccessible icon.

## 19. Scenario checks

The icon/motion system must support at least these combinations without confusion:

- live-write mode + semantic warning;
- publish mode + publish failure;
- recovery mode + verified final result;
- decorative crimson Combat lane + verified state;
- read-only mode + capture persistence failure;
- paused job + authentication failure;
- `SENT` ambiguity + operator attention required;
- repository sync failure after verified live write.

If two layers become indistinguishable in any of these combinations, the icon/shape/motion vocabulary needs revision.

## 20. Transcript-sensitive items

Keep open until transcript reconciliation/director ruling:

- exact operation-mode set;
- exact icons chosen for each mode;
- whether `Review` receives its own context icon;
- exact selected/fill/glow treatment from the latest board;
- final icon library.

The separation between operation, outcome, and content identity should remain regardless.
