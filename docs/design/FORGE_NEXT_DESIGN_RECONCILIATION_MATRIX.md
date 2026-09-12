# Forge Next — Design Reconciliation Matrix

**Status:** PRE-TRANSCRIPT RECONCILIATION  
**Date:** 2026-09-12  
**Branch:** `chatgpt/forge-next-planning`  
**Lead lens:** UI/UX Reviewer  
**Supporting lens:** Art Director  
**Purpose:** identify what already agrees between durable Forge Next design sources and the latest style board, and isolate only the questions that require predecessor-chat chronology

## 1. Inputs compared

### Durable repository sources

- `docs/design/FORGE_NEXT_VISUAL_DIRECTION.md`
- `docs/design/FORGE_NEXT_DESIGN_SYSTEM_V0_1.md`
- `docs/design/FORGE_NEXT_COLOR_SEMANTICS.md`
- `state/prompt_forge_next_planning.md`
- `docs/design/FORGE_CURRENT_UI_UX_BASELINE_AUDIT.md`
- `docs/design/FORGE_NEXT_SAFETY_STATE_PRESENTATION_CONTRACT.md`

### Latest visual artifact

- user-supplied `Forge Design System v0.1` style board, inventoried in `docs/design/FORGE_NEXT_STYLE_BOARD_INVENTORY.md`

### Missing evidence

- predecessor ChatGPT conversation export, which is needed only where approval chronology or supersession cannot be established from repository evidence.

## 2. Status vocabulary

- **AGREES** — board and durable sources express the same direction.
- **BOARD ADDS DETAIL** — board makes a previously broad/illustrative idea more concrete without clearly contradicting it.
- **APPARENT CONFLICT** — board visibly disagrees with an existing durable proposal/ruling and chronology matters.
- **OPEN BY CONTRACT** — repository planning intentionally leaves the choice user-owned; board alone cannot settle it.
- **NEEDS VALIDATION** — visually proposed behavior still needs implementation/accessibility/source feasibility evidence rather than transcript evidence.

## 3. Reconciliation matrix

| Topic | Durable repository position | Latest board | Status | Action before export |
| --- | --- | --- | --- | --- |
| Product character | professional TNR operations app; dark, atmospheric, premium, clear under production pressure | strongly matches that character | **AGREES** | proceed using this as stable direction |
| TNR visual identity | TNR-inspired ink/hard-edge language, restrained atmospheric imagery | branded masthead, ninja-world landscape, strong borders, glow accents | **AGREES** | preserve direction; exact art remains illustrative |
| Generic SaaS avoidance | avoid generic soft admin styling | squared/moderately rounded controls, stronger outlines and branded imagery | **AGREES** | safe to preserve |
| Deep dark surfaces | deep navy/charcoal/near-black foundation | deep black/slate surface scale | **AGREES** | safe to preserve |
| Crimson brand accent | signature TNR action/brand family | Crimson `#B91C1C` prominently used | **AGREES** on role | exact value remains provisional |
| Gold brand accent | warm gold/amber branded/review emphasis | Gold `#F59E0B` | **AGREES** on role | exact value remains provisional |
| Cool blue accent | chakra/system/active accent | Ninja Ink `#0EA5E9` | **AGREES** on role | exact value remains provisional |
| Ivory/parchment | selective warm light text/highlight | Ivory `#F4EBD9` | **AGREES** | safe as direction, not locked hex |
| Neutral token values | v0.1 proposes canvas/shell/panel-specific values | board presents a conventional slate ramp | **BOARD ADDS DETAIL** / possible token revision | wait for transcript before replacing tokens |
| Semantic colors separate from decorative accents | explicit durable rule | dedicated Semantic Colors panel | **AGREES** | treat separation as stable |
| Semantic success family | green reserved for verified/healthy | green Success | **AGREES** | exact hex can wait |
| Semantic warning family | yellow/amber reserved for caution/paused/attention | amber Warning | **AGREES** | exact hex can wait |
| Semantic failure family | red reserved for failed/refused/destructive | red Error + dark-red Critical | **AGREES** | Critical is an added tier to evaluate |
| Semantic info family | blue informational | blue Info | **AGREES** | safe concept |
| Semantic muted/neutral | gray/steel | Muted slate | **AGREES** | safe concept |
| Exact semantic hex values | amendment supplies reference values, explicitly non-locking | board uses different reference values | **BOARD ADDS DETAIL**, not a binding conflict | do not update exact tokens until chronology/contrast review |
| Operation colors distinct from semantic outcome colors | binding correction | dedicated Operation Mode Colors panel | **AGREES** | separation is stable |
| `Read Only` mode | durable sources require/readily explore it | board includes Read Only/Read | **AGREES** | name likely stable; final wording still reviewable |
| `Live Write` mode | durable sources require live-write consequence context | board uses Write / LIVE WRITE | **AGREES** semantically | exact short label can wait |
| `Publish` mode | durable sources require explicit publishing context | board includes Publish | **AGREES** | stable concept |
| `Recovery` mode | durable sources require explicit recovery/repair context | board includes Recovery | **AGREES** | stable concept |
| `Review` as first-class operation mode | earlier durable mode set did not define Review as a mode; review exists elsewhere as workflow/admin concept | board adds Review / Staging / Approval | **APPARENT CONFLICT / ADDITION** | transcript must establish whether this was approved |
| Operation-mode color mapping | amendment: Read cyan, Write orange, Publish magenta, Recovery indigo | board: Read indigo, Write cyan, Review violet, Publish orange, Recovery teal | **APPARENT CONFLICT** | freeze exact mapping until transcript |
| Operation context uses label + icon + wording, not color alone | durable rule | board shows label/icon/color + consequence text | **AGREES** | safe to preserve |
| Persistent operation header | required exploration/durable design-system component | board shows prominent `LIVE WRITE` indicator | **AGREES** | continue designing behavior, not final visuals |
| Mode selector | not required; mode presentation is required | board shows five selectable tiles | **OPEN BY CONTRACT** | evaluate whether mode is selectable vs derived from workflow/capability |
| Desktop persistent shell | preferred left rail | board shows left rail | **AGREES** | safe structural direction, destinations unresolved |
| Mobile distinct navigation | preferred bottom nav / More rather than shrunken rail | board shows `Home / Create / Capture / Admin / More` | **AGREES** on pattern, **BOARD ADDS DETAIL** on destinations | pattern safe; labels await transcript/Fable IA |
| Desktop nav destinations | final destination set intentionally unresolved | board lists ten concrete destinations | **OPEN BY CONTRACT** | do not canonize list yet |
| Dashboard / Command Center | approved home/command-center direction | board includes Dashboard and content-lane/dashboard-like components | **AGREES** | safe to continue component anatomy |
| Content Admin first-class presence | approved | board has Content Admin desktop nav + Admin mobile nav | **AGREES** | placement exactness still open |
| Content lanes as human-facing entry points | approved principle | board devotes major visual section to lane cards | **AGREES** | safe to preserve principle |
| Combat lane | illustrative prior taxonomy | board shows Combat | **AGREES** as illustration | final taxonomy open |
| Items lane | illustrative prior taxonomy | board shows Items | **AGREES** as illustration | final taxonomy open |
| Quests & Events lane | illustrative prior taxonomy | board shows Quests & Events | **AGREES** as illustration | final taxonomy open |
| Locations lane | illustrative prior taxonomy | board shows Locations | **AGREES** as illustration | final taxonomy open |
| Characters lane | illustrative prior taxonomy | board shows Characters | **AGREES** as illustration | final taxonomy open |
| Systems lane | illustrative prior taxonomy | board shows Systems | **AGREES** as illustration | final taxonomy open |
| Lane decorative colors cannot redefine status | explicit durable rule | lane colors intentionally span red/blue/gold/teal/violet/steel | **AGREES**, but collision risk remains | preserve rule; validate real screens |
| Atmospheric imagery placement | preferred in hero/lane/empty areas, not safety-critical dense views | board concentrates imagery in masthead/lane cards/mobile nav demo | **AGREES** | safe direction |
| Form-heavy views stay readable | durable rule | forms use plain dark outlined controls without background art | **AGREES** | safe direction |
| Typography: stylized display only | display face sparingly; functional UI sans for operations | board uses stylized Forge H1 with clean operational copy | **AGREES** | safe principle |
| Exact typography scale | v0.1 proposes mobile-first scale with 24px page title, 28–36px rare brand display | board shows H1 40px, H2 28px, H3 20px, H4 16px, body 15px | **BOARD ADDS DETAIL / possible revision** | transcript can settle approval; later responsive test still required |
| Monospace limited to technical detail | durable rule | board does not visibly elevate monospace to general UI | **AGREES** | preserve |
| Panel radius / moderate geometry | v0.1 recommends 10–12px panels, 6–8px compact controls | board visually uses moderate rounded geometry | **AGREES** | exact radius can remain token-level tuning |
| Confident borders | approved TNR-inspired hard-edge language | board strongly outlines panels/controls | **AGREES** | preserve |
| Controlled glow | glow only for focus/activity/selected areas; avoid dense danger/recovery prose | board uses glow on active buttons/modes/cards | **AGREES** directionally | validate noise/contrast on real screens |
| Primary/secondary/destructive actions | durable component vocabulary | board shows Primary/Secondary/Danger | **AGREES** | safe concept |
| Ghost/quiet action | durable design system calls for quiet action | board shows Ghost Button | **AGREES** | naming can be reconciled later |
| Success/Warning action buttons | not required by durable system; semantic colors are outcome meanings | board includes Success Button / Warning Button | **OPEN BY CONTRACT** | assess whether these variants confuse state vs action semantics |
| Confirmation component | durable `ForgeConfirmation` requirement | board shows Confirm Deployment modal | **AGREES** | actual publish/deploy wording/authority remains open |
| Confirmation states production consequence | durable production-action rule | board says action will publish items live | **AGREES** | preserve behavior |
| Browser-native confirm as long-term UX | current baseline uses `window.confirm`; Forge Next calls for polished component | board demonstrates custom modal | **AGREES with redesign opportunity** | safe to specify custom confirmation behavior later |
| Notifications/callouts | durable `ForgeCallout` + semantic state guidance | board shows success/info/warning/error/review notifications | **AGREES** | exact review notification color depends on mode taxonomy |
| Progress feedback | durable `ForgeProgress` / controlled motion | board shows per-operation progress rows | **AGREES** | machine mapping still must follow safety contract |
| `SENT` ambiguity treatment | durable safety rule: distinct, never retry-safe | board does not explicitly demonstrate `SENT` | **NEEDS VALIDATION** | future wireframes must include ambiguous state, not infer from style board |
| `CONFIRMED` vs `VERIFIED` | durable safety distinction | not explicitly demonstrated | **NEEDS VALIDATION** | must appear in workflow wireframes |
| `INCOMPLETE` unverified writes | durable safety distinction | not explicitly demonstrated | **NEEDS VALIDATION** | must appear in workflow wireframes |
| Orphan/recovery decision UI | required first-class recovery | board shows Recovery mode but not orphan decision anatomy | **NEEDS VALIDATION** | design recovery card/wireframe separately |
| Auth states | global readiness required | board shows generic system status, not auth-specific states | **NEEDS VALIDATION** | future shell must explicitly handle auth ready/probing/refused/unauthorized |
| Rate limit state | current product + planning require clarity | board shows Rate Limited system chip and `Rate limit approaching` notification | **AGREES** | behavior thresholds remain technical planning concern |
| Full-capture persistence state | durable/current safety distinction | no explicit full-capture example | **NEEDS VALIDATION** | include in capture/preflight wireframes |
| System health indicator family | durable Command Center asks for system readiness | board shows Online/Operational/Degraded/etc. family | **BOARD ADDS DETAIL** | determine which statuses map to real data vs illustrative labels |
| Empty state | design system allows atmospheric/personality treatment | board shows `No Content Yet` + Create Content | **AGREES** | safe pattern |
| Generic error state | design system requires actionable errors | board shows `Something Went Wrong` + Try Again / View Logs | **AGREES** only for retry-safe failures | safety contract governs ambiguous writes |
| Generic `Try Again` | current safety rules prohibit blind retry for ambiguous writes | board uses Try Again in generic error example | **NEEDS VALIDATION** | restrict to explicitly retry-safe error classes |
| Icon family | clean, consistent, purposeful icons | board shows consistent outline icon set | **AGREES** | exact library/assets remain implementation choice |
| Motion | controlled motion approved | static board cannot prove motion behavior | **NEEDS VALIDATION** | leave to later prototype/accessibility pass |
| Reduced motion | required where practical | not shown | **NEEDS VALIDATION** | implementation acceptance criterion |
| Accessibility | WCAG AA target, color not sole cue, 44px touch targets | board claims accessible and mostly uses icon+label+color | **NEEDS VALIDATION** | real contrast/touch/focus testing still required |
| Desktop multi-column use | approved direction | style board itself uses dense multi-column showcase, not an app wireframe | **BOARD ADDS VISUAL EVIDENCE** only | final workflow layouts await IA |
| Technical details progressively disclosed | durable principle | style board does not show raw/detail disclosure | **NEEDS VALIDATION** | must appear in actual screen wireframes |
| Content Admin simplicity vs operations | approved conceptual distinction | board only shows navigation presence, not admin workflow | **NEEDS VALIDATION** | Fable source/feasibility work still needed |
| Publishing authority/permissions | explicit user/game authority boundary | board visually offers Publish | **NEEDS VALIDATION** | visual control must be permission-aware; board does not grant capability |

## 4. What is already safe to treat as stable direction

Without waiting for the transcript, subsequent design work may rely on these principles:

- Forge Next is a dark, atmospheric, professional TNR operations product.
- Brand personality belongs in shell/hero/lane/empty-state surfaces, not behind dense safety-critical information.
- Desktop should use a persistent application shell rather than the current five-button horizontal strip.
- Mobile should have an intentionally different navigation treatment rather than a compressed desktop sidebar.
- A Command Center/home is preferred over dropping directly into raw manifests/jobs.
- Content lanes should make common work human-recognizable.
- Content Admin is a first-class product area but remains conceptually distinct from content execution.
- Operation consequence and semantic outcome are separate visual systems.
- Safe read, live mutation, publishing and recovery must be legible before the operator studies technical detail.
- Color is never the sole state cue.
- Verified success is distinct from confirmed/unverified/ambiguous execution.
- Recovery must be first-class and operator-controlled.
- Functional text stays highly legible; display typography is sparing.
- Moderate hard-edged/outlined geometry and controlled glow fit the target character.
- Mobile touch/readability/accessibility constraints remain first-class.

## 5. What should remain frozen until the export is reconciled

Do not promote the following board details to canonical implementation decisions yet:

1. exact operation-mode taxonomy, specifically whether `Review` is a first-class mode;
2. exact operation-mode color mapping;
3. exact desktop destination list;
4. exact mobile destination list;
5. exact neutral/semantic/brand hex values where they differ from repository proposals;
6. exact typography sizes where the board tightens or changes the v0.1 proposal;
7. exact content-lane taxonomy;
8. semantic `Success`/`Warning` button variants as production component types;
9. whether the board's deployment-confirmation wording reflects an approved publish flow;
10. any assumption that a visible Publish/Admin control implies current source-level permission/capability.

## 6. Work that can continue before the export

The matrix shows that the missing transcript no longer blocks most foundational work.

Safe next work includes:

- mobile ergonomics/accessibility audit;
- workflow-to-component mapping;
- architecture-neutral component anatomy for Command Center, preflight, execution, capture, recovery and admin review;
- Fable's Builder parity/current architecture/source-permission research;
- design of ambiguous/unverified/recovery wireframe states using the safety-state contract;
- analysis of what system-health indicators can truthfully derive from current Forge data.

## 7. Export reconciliation target

When the predecessor transcript arrives, search it first for the rows marked **APPARENT CONFLICT**, then for **OPEN BY CONTRACT** items where the user may have already ruled.

The primary transcript questions are now reduced to:

- operation-mode taxonomy;
- mode palette;
- navigation destinations;
- exact token/typography acceptance;
- lane taxonomy acceptance;
- button/modal specifics;
- any late Content Admin/publish decisions.

Everything else should be treated as already reconciled unless the transcript contains an explicit later user ruling.

## 8. Completion statement

Step 4 of the interim Forge UI workflow is complete.

The latest board and durable repository sources are now reconciled far enough that the pending chat export is a **small chronology-resolution task**, not a prerequisite for continuing the broader Forge Next design and planning effort.