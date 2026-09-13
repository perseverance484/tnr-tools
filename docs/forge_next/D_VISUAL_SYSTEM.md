# D2. Visual system: the approved direction elaborated

**Status:** planning; elaboration of the director-approved visual north star (`docs/design/FORGE_NEXT_VISUAL_DIRECTION.md` at `chatgpt/forge-next-planning@0bb5a54b`) into a token proposal, a component inventory and binding state/motion rules, as the amendment's section 13 asks. Produced by the design panel (three independent elaborations, two independent judges who recomputed 34 contrast pairs, one synthesis), then read against the consolidated design lane at `chatgpt/forge-quest-studio-foundation@824c4d58` (colour semantics, design system v0.1, style-board inventory, reconciliation matrix, icon/motion semantics, safety-state presentation contract). Machine-readable source: `evidence/visual-synthesis.json`. Rows marked PENDING stay open under K-21, K-22 and K-23 until the predecessor transcript is reconciled; everything marked SETTLED follows from the approved character plus a non-negotiable and needs no further ruling.

**Abbreviations and cite conventions.** Unprefixed `forge/src/*` and `docs/forge_next/*` cites resolve in this repository (`forge/` is byte-identical to `main@305a28f`). The design contracts are cited as ABBR:line and resolve at `chatgpt/forge-quest-studio-foundation@824c4d58` (their headers may still say `chatgpt/forge-next-planning`): SSC = docs/design/FORGE_NEXT_SAFETY_STATE_PRESENTATION_CONTRACT.md at chatgpt/forge-quest-studio-foundation@824c4d58; CPY = docs/design/FORGE_NEXT_UI_COPY_AND_STATE_LANGUAGE.md at chatgpt/forge-quest-studio-foundation@824c4d58; ICN = docs/design/FORGE_NEXT_ICON_MOTION_SEMANTICS.md at chatgpt/forge-quest-studio-foundation@824c4d58; WCM = docs/design/FORGE_NEXT_WORKFLOW_COMPONENT_MAP.md at chatgpt/forge-quest-studio-foundation@824c4d58; MOB = docs/design/FORGE_NEXT_MOBILE_ACCESSIBILITY_AUDIT.md at chatgpt/forge-quest-studio-foundation@824c4d58; WFA = docs/design/FORGE_NEXT_WIREFRAME_ANATOMY.md at chatgpt/forge-quest-studio-foundation@824c4d58; IRM = docs/design/FORGE_NEXT_INTERACTION_RISK_MATRIX.md at chatgpt/forge-quest-studio-foundation@824c4d58; SCR = docs/design/FORGE_NEXT_SCREEN_CONTENT_REQUIREMENTS.md at chatgpt/forge-quest-studio-foundation@824c4d58; COL = docs/design/FORGE_NEXT_COLOR_SEMANTICS.md at chatgpt/forge-quest-studio-foundation@824c4d58; SBI = docs/design/FORGE_NEXT_STYLE_BOARD_INVENTORY.md at chatgpt/forge-quest-studio-foundation@824c4d58; RCM = docs/design/FORGE_NEXT_DESIGN_RECONCILIATION_MATRIX.md at chatgpt/forge-quest-studio-foundation@824c4d58; DS = docs/design/FORGE_NEXT_DESIGN_SYSTEM_V0_1.md at chatgpt/forge-quest-studio-foundation@824c4d58; IDX = docs/design/FORGE_NEXT_UI_DESIGN_INPUT_INDEX.md at chatgpt/forge-quest-studio-foundation@824c4d58. The prefix `824c4d58:` marks files that exist only on that branch (`forge/src/studio/*`). Meaning is owned by the cited contract; this file records construction and facts and does not restate the contract text (CLAUDE.md section 7). Evidence tiers follow docs/00_INDEX.md: Source-verified (file:line read in this pass), Behaviour-proven, Observed, Inferred, Assumed.

**Concept:** Forge (approved direction, synthesized): 'Ink & Ember', corrected

The director-approved dark TNR operations console made buildable: navy-charcoal ground, ivory ink, crimson only on the control that writes to the game, gold only where content becomes player-visible, cool blue for the resting system, orchid for the one ambiguous state, orange caution, ivory for the one decision that must be made, lane tints that cannot reach a pill, and motion spent only on transitions and the single running cell.

## D2.1 Relationship to the ruling and the one organising rule

The direction ruled at chatgpt/forge-next-planning@0bb5a54b is not re-ranked. This file starts from visual-c, applies every graft both judges drew from A and B, corrects the two token pairs a judge showed failing (count chips on the crimson band 2.61:1; opacity-.45 disabled text 4.01:1), withdraws the two motion rules that contradicted the non-negotiables (whole-root fade; press-and-hold), adds the missing 'authenticated but unauthorized' state, and marks every row where the approved character, design system v0.1, the colour-semantics amendment and the latest style board disagree as pending director/transcript confirmation with the values side by side.

HUE says which authority family you are in (blue read/system, crimson write, gold publish/admin, orange caution/recovery, orchid unconfirmed, green verdict, coral failure, ivory decide-now). CONSTRUCTION says the exact state (fill vs outline vs hatch vs inverted; dotted/dashed/solid; 1 px/2 px; square vs rounded). MOTION is spent only on transitions and the one cell that is actually running. A stylesheet contract test turns the rule into a build gate.

## D2.2 Design tokens

**scope rule.** All custom properties are declared on .f-host and .f-app (forge/src/ui/styles.mjs:19-20 pattern; never :root, styles.mjs:3-9); color-scheme: dark stays on those two elements; lane tokens are declared only inside .f-lane. One stylesheet installed through dom.mjs installCss (adoptedStyleSheets with the insertRule fallback; splitRules keeps @media/@keyframes whole, dom.mjs:44-52). No url(), no @font-face, no fetched asset; a static test greps the sheet for both.

**How this file stands to the Tier A colour semantics.** `FORGE_NEXT_COLOR_SEMANTICS.md` binds the separation of meaning, not the hues: its own closing line says the reference values "are references, not implementation locks. The separation of meaning is the binding design rule" (COL:64-66). This file therefore does not claim to supersede it, and nothing here asserts which document came later. What it claims is narrower: the mapping below satisfies COL's collision rules as constructed (publish is not in the error-red family, live write is not in the yellow-amber warning family, mode and outcome stay distinguishable, and no state is carried by colour alone). Where a hue family differs from COL's reference value, that difference is the substance of K-22 and is shown side by side in the rows below rather than argued away.

**status legend.** SETTLED = follows from the approved character plus a non-negotiable, no director input needed. PENDING = recommended default shown beside the v0.1 / colour-semantics-amendment / style-board value; the director or transcript reconciliation confirms (K-21/K-22/K-23). Every ratio below was recomputed in scratchpad/design/synth/contrast_synth.py (WCAG 2.x relative luminance, sRGB 0.04045 linearisation, (L1+0.05)/(L2+0.05)); text pairs are held to 4.5:1 even for 12 px/700 pill words, non-text boundaries to 3:1.


#### surfaces

| token | value | role | status | contrast (recomputed) | v0.1 / style board / other |
|---|---|---|---|---|---|
| `--bg` | `#0b121a` | page ground; the only surface a mode band sits on | SETTLED (sampled from the approved mockup ground #0b131b, judged AA-safe by both judges) |  | v0.1 forge.bg.canvas: #070B12; style board Deep Black: #05080F |
| `--paper` | `#121b26` | card / panel surface | SETTLED |  | v0.1 forge.bg.panel: #111A28; style board Slate 900: #0F172A |
| `--raised` | `#1a2532` | elevated surface: rail active row, sticky action bar, disabled-control fill, pressed rows | SETTLED |  | v0.1 forge.bg.panelElevated: #172235; style board Slate 800: #1E293B |
| `--float` | `#212f3f` | dialogs, confirmation sheets, toasts, popovers (elevation 3) | SETTLED |  | v0.1 forge.bg.panelSoft: #1D2A3D |
| `--line` | `#2a3644` | decorative divider only (1.41:1 on paper, exempt from 1.4.11); never a control boundary | SETTLED | vs paper: 1.41 |  |
| `--edge` | `#5d6d82` | control boundary: inputs, neutral buttons, progress track, SKIPPED/HIDDEN pill border, disabled-control border | SETTLED | vs paper: 3.28; vs bg: 3.56 |  |
| `--edge2` | `#738399` | control boundary on --raised / --float surfaces | SETTLED | vs raised: 4.01; vs paper: 4.49 |  |


#### text

| token | value | role | status | contrast (recomputed) | v0.1 / style board / other |
|---|---|---|---|---|---|
| `--ink` | `#f3efe6` | body text (warm ivory per amendment section 3, replaces the mockup's #ffffff) | SETTLED | on bg: 16.4; on paper: 15.12; on raised: 13.51; on float: 11.86 | v0.1 forge.text.primary: #F5F1E7; style board Ivory: #F4EBD9 |
| `--ink2` | `#fffaf0` | headings, wordmark, text and border on crimson | SETTLED | on raised: 14.9 |  |
| `--mute` | `#a9b3c2` | secondary text, captions, inactive nav labels, disabled-control text (at 100 % opacity) | SETTLED | on bg: 8.89; on paper: 8.19; on raised (disabled): 7.32 | v0.1 forge.text.secondary: #B7C0CE; style board Slate 400: #94A3B8 |
| `--dim` | `#8a97ab` | tertiary text (hashes, timestamps); the floor for any text | SETTLED | on bg: 6.36; on paper: 5.86 | v0.1 forge.text.muted: #7F8B9C (4.24:1 on #111A28 - below AA for 13 px, not adopted) |
| `--focus` | `#fffaf0` | 2 px solid focus ring, outline-offset 3 px (mandatory: the ring directly on gold is 1.78:1) | SETTLED | vs bg: 18.09; vs paper: 16.67; vs pub with no offset: 1.78 |  |


#### signature accents

| token | value | role | status | contrast (recomputed) | v0.1 / style board / other |
|---|---|---|---|---|---|
| `--acc` | `#7ab8ff` | cool chakra blue: system/active accent, nav current marker, links, focus of navigation, default primary button fill (with --acc-ink text), CONFIRMED / RUNNING / DRAFT pills | SETTLED at character level; exact hex PENDING (K-22) | on bg: 9.08; on paper: 8.37; on raised: 7.48 | v0.1 forge.accent.chakra: #6BB8FF; style board Ninja Ink: #0EA5E9 (4.6:1 on #0b121a as text: AA only, no margin) |
| `--acc-ink` | `#0b121a` | text on an --acc fill |  | on acc: 9.08 |  |
| `--acc-fill` | `#14304f` | info banner fill and READ ONLY band fill |  | acc on it: 6.47; ink on it: 11.69 |  |
| `--mut` | `#c0242f` | burnt crimson, the ONLY solid crimson fill in the app: LIVE WRITE band and the Start/Resume-live ink button. Never text, never a pill, never a nav fill. Mitigation: the 2.92:1 fill-vs-paper pair is not relied on: every crimson control carries a 2 px --mut-ink border on all four sides (the game's own ink construction, globals.css:265-271 at pin 345d18ac) giving 5.71:1 inner / 16.67:1 outer, and every crimson band carries 2 px --mut-edge rules top and bottom | SETTLED at character level (amendment section 3 'burnt crimson action family'); exact hex PENDING (K-22) | mut-ink on it: 5.71; fill vs bg (non-text): 3.17; fill vs paper (non-text): 2.92 | v0.1 forge.accent.crimson: #B7331F (ivory on it 5.33:1); style board Crimson: #B91C1C (ivory on it 6.0:1); colour-semantics amendment mode.liveWrite: #F97316 copper/orange (rejected here: collides with caution family, which the same amendment's rule 2 forbids for LIVE WRITE); mockup quick-action crimson: #cd1c24 (3.39:1 as text: never text) |
| `--mut-ink` | `#fffaf0` | text and 2 px border on crimson |  |  |  |
| `--mut-edge` | `#ff5f5a` | 2 px rules on the LIVE WRITE band; 3 px top-bar underline on every screen while a mutation job is RUNNING; rail active marker |  | vs bg: 6.31; vs paper (top bar): 5.81; vs raised: 5.19 |  |
| `--mut-glow` | `rgba(255,95,90,0.35)` | 8-24 px outer glow ONLY while a crimson button is focused/pressed; never resting, never ambient |  |  |  |
| `--pub` | `#e6b84f` | gold, the ONLY solid gold fill: PUBLISH band, Publish ink button, seal-card border. Text on it is --pub-ink. | SETTLED at character level (amendment: gold = premium/admin/review cue); exact hex PENDING (K-22); whether PUBLISH is gold vs magenta/orange is the K-21/K-22 mode-colour row | pub-ink on it: 10.0; fill vs paper (non-text): 9.36; fill vs bg: 10.16 | v0.1 forge.accent.gold: #D7A33D; style board Gold: #F59E0B; colour-semantics amendment mode.publish: #D946EF magenta; style board Publish mode: #F97316 orange |
| `--pub-ink` | `#1b1200` | text on gold |  |  |  |
| `--pub-text` | `#f0c65e` | gold as text/outline: PUBLISHED pill, pending-review count badge (OUTLINE, not solid), admin cues, REVIEW band if Review becomes a mode |  | on bg: 11.6; on paper: 10.69; on raised: 9.56 |  |
| `--read` | `#7ab8ff` | READ ONLY mode = the system's resting accent on purpose (reading is the safe default); distinguished from navigation by construction (outlined chip, ◎ glyph, the words READ ONLY), never by a second hue | PENDING (K-22): colour-semantics amendment proposes cyan #38BDF8, style board indigo #6366F1; recommended default keeps one cool blue so 'a screen with only blue on it cannot write' |  |  |
| `--read-fill` | `#14304f` | READ ONLY band fill |  |  |  |


#### semantic states

| token | value | role | status | contrast (recomputed) | v0.1 / style board / other |
|---|---|---|---|---|---|
| `--ok` | `#5ad48f` | success verdicts only: VERIFIED, DONE with outcome success, session READY lamp, 'body persisted'. NEVER a button fill. | SETTLED | on bg: 10.08; on paper: 9.29; on ok-fill: 7.68 | v0.1 forge.state.success: #45C779; style board Success: #16A34A (3.9:1 on #0b121a: fails AA as text, not adopted); colour-semantics state.success: #22C55E |
| `--ok-fill` | `#10301f` | VERIFIED pill fill and success banner fill |  | ink on it: 12.5 |  |
| `--warn` | `#f08a3c` | caution text/outline: PAUSED, INCOMPLETE pills; authorization-denied action state (per action, not a session lamp; E.3); advisories; budget at >= 80 %; RECOVERY band word and rules | PENDING director confirmation (D-VC-7 / judges U2, UD-2): recommended default is the more-orange #f08a3c so caution and publish gold stop sharing a hue; visual-c's #f5a25a shown beside it. Both pass AA everywhere; the shift buys a hue gap (orange vs yellow) at the cost of 1.5 points of margin. | on bg: 7.53; on paper: 6.94; on raised: 6.21; on warn-fill: 6.16; on rec-hatch stripe #3f2610: 5.62 | visual-c --warn: #f5a25a (8.42:1 paper, 5.98:1 on its #4a2f12 stripe; 1.11:1 from gold); v0.1 forge.state.warning: #E6AD45 (1.02:1 from --pub: not separable); style board Warning: #F59E0B (identical to the board's Gold: the collision the colour-semantics amendment was written to stop); colour-semantics state.warning: #FACC15 |
| `--warn-fill` | `#33210f` | warn banner fill, RECOVERY band base, authorization-denied line fill (per action; E.3) |  | ink on it: 13.4 |  |
| `--rec` | `#f08a3c` | RECOVERY mode shares the caution hue and is distinguished by construction: hatched band, ↻ glyph, the word RECOVERY, 2 px --warn rules | PENDING (K-21/K-22): colour-semantics amendment proposes indigo/violet #7C3AED, style board teal; recommended default keeps caution-hatch because RECOVERY is computed from PAUSED/SENT/ORPHANED states and violet is already the SENT colour |  |  |
| `--rec-fill` | `#33210f` | RECOVERY band base stripe |  |  |  |
| `--rec-hatch` | `#3f2610` | 45-degree 6 px stripes over --rec-fill (repeating-linear-gradient); darkened from visual-c's #4a2f12 so the shifted --warn keeps >= 5:1 on the lighter stripe |  | warn on it: 5.62; ink counts on it: 12.23 |  |
| `--bad` | `#ff8a80` | failure verdicts: FAILED, ABORTED pills; SIGNED OUT lamp; TRIPPED; 'not persisted'. Text/outline only; the opposite construction of the dark crimson fill (2.60:1 apart in luminance, never in the same construction). | SETTLED | on bg: 8.25; on paper: 7.6; on bad-fill: 7.07 | v0.1 forge.state.danger: #E05F5F; style board Error: #EF4444 (4.1:1 on #0b121a: fails AA as text); colour-semantics state.error: #EF4444 |
| `--bad-fill` | `#3a1518` | failure banner fill; SIGNED OUT lamp fill |  | ink on it: 14.07 |  |
| `--sent` | `#e79cff` | SENT / unconfirmed only. Text + 2 px dashed border + hatch; never a solid fill; nothing else in the app is this orchid (the Characters lane violet #8b5cf6 is 2.14:1 away and confined to .f-lane). | SETTLED (colour-semantics amendment section 3: 'violet only when visually distinct from PUBLISH'; publish is gold here, so the collision is absent) | on bg: 9.5; on paper: 8.75; on sent-fill: 7.73; on sent-hatch stripe: 6.38 | today styles.mjs:11 --sent: #b08cff; v0.1 forge.state.ambiguous: #B884FF |
| `--sent-fill` | `#2c1f3d` | SENT pill / banner base |  | ink on it: 13.35 |  |
| `--sent-hatch` | `#3d2a55` | stripes over --sent-fill |  | ink on it: 11.02 |  |
| `--hidden-text` | `#c9d2de` | HIDDEN content pill text |  | on hidden-fill: 8.72 |  |
| `--hidden-fill` | `#253041` | HIDDEN content pill slate fill (present but not player-visible; the default Forge creates into). Its boundary is the 1 px --edge border (3.28:1), not the fill (1.30:1 vs paper). |  |  |  |
| `--orph-fill` | `#f3efe6` | ORPHANED pill fill: the one inverted-polarity pill (ivory fill, --bg text), the heaviest pill in the system; ivory is the amendment's 'selective high-attention surface' and is not used as a fill anywhere else | SETTLED (graft from B via polish judge G3; ivory is in the approved palette) | bg text on it: 16.4; fill vs paper (non-text): 15.12; vs gold (informational): 1.61 |  |
| `--daylight-mute` | `#c5ccd8` | .f-daylight variant override of --mute |  | on paper: 10.74 |  |
| `--daylight-dim` | `#a3afc1` | .f-daylight variant override of --dim |  | on paper: 7.81 |  |


#### board-only semantic tiers (not mapped)

| board tier | value | Forge state it would map to | status |
|---|---|---|---|
| Critical | `#7F1D1D`, board wording 'System / Safety Critical' (SBI:81) | none. The most severe states Forge holds (FAILED, SIGNED OUT, TRIPPED, 'not persisted') are already in the --bad family above, and no journal, auth, budget or outcome value is more severe than those. RCM:53 records Critical as 'an added tier to evaluate'. | PENDING (K-22 sub-point, open); recommendation: drop, no token is reserved for it here |
| Ambiguous / SENT | absent from the board's semantic list (SBI:77-82 has Success, Info, Warning, Error, Critical, Muted); COL:38 reserves violet 'only when visually distinct from the PUBLISH mode treatment; prefer muted lavender plus explicit wording' | `--sent` above (orchid text, dashed border, hatch; never a solid fill) | SETTLED at character level; exact hex PENDING (K-22) |

#### lane accents scoped to .f-lane

- **policy**: Decoration only: a lane card's gradient wash (20 % -> 0 %), its 1 px edge, its inline-SVG glyph at 12 % alpha and its interaction glow. Declared inside .f-lane so no lane selector can reach a .f-pill, .f-band, .f-banner or button; the stylesheet contract test enforces it. Lane names are illustrative until K-24.
- **--lane-combat**:
  - **hex**: #e5484d
  - **contrast_vs_bg**: 4.81
  - **contrast_vs_paper**: 4.43
- **--lane-items**:
  - **hex**: #3b82f6
  - **contrast_vs_bg**: 5.12
  - **contrast_vs_paper**: 4.72
- **--lane-quests**:
  - **hex**: #d5a360
  - **contrast_vs_bg**: 8.28
- **--lane-locations**:
  - **hex**: #2fbfc9
  - **contrast_vs_bg**: 8.44
- **--lane-characters**:
  - **hex**: #8b5cf6
  - **contrast_vs_bg**: 4.45
  - **contrast_vs_paper**: 4.1
  - **note**: deliberately not --sent (2.14:1 apart, different construction)
- **--lane-systems**:
  - **hex**: #7c8797
  - **contrast_vs_bg**: 5.17
  - **contrast_vs_paper**: 4.77


#### operation modes

- **taxonomy_status**: READ ONLY / LIVE WRITE / PUBLISH / RECOVERY as named in the approved amendment section 8. Whether REVIEW is a fifth mode is PENDING (K-21, style board shows Read/Write/Review/Publish/Recovery). A reserved treatment is specified so adding it later does not change the other four.
- **READ ONLY**:
  - **fill**: #14304f
  - **rules**: 2 px #7ab8ff top and bottom
  - **word**: #7ab8ff
  - **counts**: #f3efe6 in chips outlined 1 px #7ab8ff, no fill
  - **glyph**: ◎ U+25CE
  - **contrast**:
    - **word**: 6.47
    - **counts**: 11.69
    - **chip outline**: 6.47
  - **side_by_side**:
    - **v0.1**: chakra blue
    - **colour-semantics amendment**: #38BDF8 cyan
    - **style board**: #6366F1 indigo
  - **status**: recommended default; PENDING K-22
- **LIVE WRITE**:
  - **fill**: #c0242f
  - **rules**: 2 px #ff5f5a top and bottom
  - **word**: #fffaf0
  - **counts**: #fffaf0 in chips outlined 1 px #fffaf0, no fill (replaces visual-c's --raised chips, which were 2.61:1 against the band)
  - **glyph**: ↯ U+21AF (energy bolt; Arrows block, no emoji presentation)
  - **contrast**:
    - **word**: 5.71
    - **chip outline**: 5.71
    - **rules vs bg**: 6.31
  - **side_by_side**:
    - **v0.1**: crimson
    - **colour-semantics amendment**: #F97316 copper/orange
    - **style board**: #06B6D4 cyan
  - **status**: recommended default follows the approved north star (crimson = action); PENDING K-22
- **PUBLISH**:
  - **fill**: #e6b84f
  - **rules**: 2 px #1b1200 top and bottom
  - **word**: #1b1200
  - **counts**: #1b1200 in chips outlined 1 px #1b1200, no fill
  - **glyph**: ◆ U+25C6
  - **contrast**:
    - **word**: 10.0
    - **chip outline**: 10.0
  - **side_by_side**:
    - **v0.1**: gold
    - **colour-semantics amendment**: #D946EF magenta
    - **style board**: #F97316 orange
  - **status**: recommended default follows the approved north star (gold = admin/review/publish); PENDING K-22
- **RECOVERY**:
  - **fill**: repeating-linear-gradient(45deg,#33210f 0 6px,#3f2610 6px 12px)
  - **rules**: 2 px #f08a3c top and bottom
  - **word**: #f08a3c
  - **counts**: #f3efe6 in chips outlined 1 px #f08a3c, no fill
  - **glyph**: ↻ U+21BB (reconcile arrow; not the emoji U+1F504)
  - **contrast**:
    - **word worst stripe**: 5.62
    - **counts worst stripe**: 12.23
    - **chip outline**: 5.62
  - **side_by_side**:
    - **v0.1**: amber/violet
    - **colour-semantics amendment**: #7C3AED indigo/violet
    - **style board**: teal
  - **status**: recommended default; PENDING K-21/K-22
- **REVIEW (reserved, only if ruled a mode)**:
  - **fill**: transparent
  - **rules**: 2 px #f0c65e top and bottom
  - **word**: #f0c65e
  - **glyph**: ◈ U+25C8
  - **note**: gold OUTLINE so PUBLISH keeps the only solid gold; if Review is ruled a workflow category rather than a mode, the Content Admin queue simply carries no band
  - **status**: PENDING K-21


#### Studio shell colours at 824c4d58 (implementation fact; to absorb)

- **fact**: the Quest Studio shell ships its own stylesheet with hard-coded design-system v0.1 neutrals (ground #070b12, ink #f5f1e7, panel #111a28, muted #b7c0ce and #7f8b9c; 824c4d58:forge/src/studio/ui.mjs:13-60), its own semantic callouts (#45c779 / #e6ad45 / #e05f5f; 824c4d58:forge/src/studio/ui.mjs:46-48) and a compile button filled #f97316 (824c4d58:forge/src/studio/ui.mjs:39). It is a second fixed overlay (`.qs-shell`, z-index 2147483002; 824c4d58:forge/src/studio/ui.mjs:14) above `.f-app`, mounted after app.mount and outside compose() (824c4d58:forge/src/main.mjs:151), and it routes destructive draft actions through app.confirm, which is window.confirm today (824c4d58:forge/src/studio/ui.mjs:302,314; app.mjs:172-175). Source-verified.
- **collision**: #f97316 equals the style board's Publish orange (SBI:113) and the colour-semantics reference for live write (`#F97316`, COL:55). A compile control that never touches the game would share a hue with two different mode mappings. COL:11 (operation context and outcome must stay distinct) and the collision rules COL:43-48 make this a defect to remove whichever K-22 mapping the director confirms. Source-verified.
- **plan**: absorb the Studio shell into this token set: one overlay, one stylesheet, ConfirmationSurface instead of window.confirm; the compile control takes a construction from this file (a neutral or read-primary control, since a repository build is not a game write). No colour is assigned to it here: PENDING K-22, and the ownership of `forge/src/studio/*` after integration is the CF-22 question in D2.10. Proposal.

#### state pills

- **construction**: Every pill = [glyph in a fixed 16 px aria-hidden box][WORD] at 12 px / 700 / uppercase / 0.04 em, min-height 24 px, padding 2 px 8 px, radius 3 px (hard edge is reserved for the three production ink buttons, judges G9), 1 px border in the state colour, text in the state colour, on --paper. Glyphs are Unicode text nodes from blocks with no emoji presentation (Geometric Shapes, Arrows, Mathematical Operators, ✓ U+2713, ✕ U+2715, ‖ U+2016, ✎ U+270E); the fixed box means tofu cannot shift the word. Pills never animate, never change size on state change, and are swapped, never faded. On phone the word is single (SENT / ORPHANED / INCOMPLETE / CONFIRMED) and the qualifier moves to a 13 px caption under the row; on desktop the qualifier stays in the pill (judges G15).
- **PLANNED**:
  - **text**: #a9b3c2
  - **border**: 1px dotted #8a97ab
  - **fill**: transparent
  - **glyph**: ○ U+25CB
  - **word**: PLANNED
  - **contrast**: 8.19
- **SENT**:
  - **text**: #e79cff
  - **border**: 2px dashed #e79cff
  - **fill**: repeating-linear-gradient(45deg,#2c1f3d 0 6px,#3d2a55 6px 12px)
  - **glyph**: ? U+003F
  - **word**: SENT · UNCONFIRMED (desktop) / SENT + caption 'request left this device; no answer; reconciled, never re-sent' (phone)
  - **contrast_fill**: 7.73
  - **contrast_stripe**: 6.38
  - **note**: the only dashed pill, the only hatched non-recovery pill, the only question glyph
- **CONFIRMED**:
  - **text**: #7ab8ff
  - **border**: 1px solid #7ab8ff
  - **fill**: transparent
  - **glyph**: ◐ U+25D0
  - **word**: CONFIRMED · NOT READ BACK (desktop) / CONFIRMED + caption 'write landed; read-back still owed' (phone)
  - **contrast**: 8.37
  - **note**: qualifier added (judge G6) so a landed-but-unverified write in the calm blue never reads as finished
- **VERIFIED**:
  - **text**: #5ad48f
  - **border**: 1px solid #5ad48f
  - **fill**: #10301f
  - **glyph**: ✓ U+2713
  - **word**: VERIFIED
  - **contrast**: 7.68
  - **note**: the only green pill; the only lifecycle pill with a solid tinted fill
- **FAILED**:
  - **text**: #ff8a80
  - **border**: 2px solid #ff8a80
  - **fill**: transparent
  - **glyph**: ✕ U+2715
  - **word**: FAILED
  - **contrast**: 7.6
- **ORPHANED**:
  - **text**: #0b121a
  - **border**: none
  - **fill**: #f3efe6
  - **glyph**: ! U+0021
  - **word**: ORPHANED · DECIDE (desktop) / ORPHANED + caption 'a write may have landed; adopt or skip below' (phone)
  - **contrast**: 16.4
  - **note**: the one inverted-polarity pill: the state that demands a human decision is the heaviest thing on the screen; distinct from gold PUBLISH on the blue-yellow axis that deuteranopia preserves (ivory neutral vs gold yellow)
- **SKIPPED**:
  - **text**: #a9b3c2
  - **border**: 1px solid #5d6d82
  - **fill**: transparent
  - **glyph**: ⇥ U+21E5
  - **word**: SKIPPED
  - **contrast**: 8.19
  - **note**: neutral terminal, never counted toward verified
- **PAUSED**:
  - **text**: #f08a3c
  - **border**: 1px solid #f08a3c
  - **fill**: transparent
  - **glyph**: ‖ U+2016
  - **word**: PAUSED
  - **contrast**: 6.94
  - **note**: job-level; the pause REASON is always a mono chip beside it: SESSION ✕ --bad · 429 △ --warn + countdown · NETWORK ✗ --warn · UNDECODABLE_RESPONSE ✗ --warn · AMBIGUOUS ? --sent · USER ‖ --mute · ORPHANED ! --warn. The runner raises seven reasons and all seven get a chip. NETWORK and UNDECODABLE_RESPONSE each occur in two situations whose next safe action differs: before anything was sent, where Try again is permitted, and inside a send, where the item is left SENT and only reconciliation may follow. The chip therefore carries the reason and the halt card carries the situation, never the reverse
- **INCOMPLETE**:
  - **text**: #f08a3c
  - **border**: 1px solid #f08a3c
  - **fill**: transparent
  - **glyph**: ◔ U+25D4
  - **word**: INCOMPLETE · UNVERIFIED (desktop) / INCOMPLETE + caption 'finished, but N writes are not proven; resume re-reads, never re-sends' (phone)
  - **contrast**: 6.94
- **RUNNING**:
  - **text**: #7ab8ff
  - **border**: 1px solid #7ab8ff
  - **fill**: transparent
  - **glyph**: ▸ U+25B8 (not ▶ U+25B6, which has emoji presentation)
  - **word**: RUNNING
  - **contrast**: 8.37
  - **note**: static; the ember sheen lives on the progress track beside it, never on the pill
- **DONE**:
  - **text**: #f3efe6
  - **border**: 1px solid #5d6d82
  - **fill**: transparent
  - **glyph**: ■ U+25A0
  - **word**: DONE
  - **contrast**: 15.12
  - **note**: neutral state pill; the OUTCOME lamp beside it (VERIFIED ALL --ok filled / UNVERIFIED --warn outline / FAILED --bad outline, from jobOutcome) carries the verdict (judge G9; `A_ARCHITECTURE_MAP.md`; app.mjs:384 exports both). DONE is never green on its own; today styles.mjs:44 paints it green.
- **ABORTED**:
  - **text**: #ff8a80
  - **border**: 1px solid #ff8a80
  - **fill**: transparent
  - **glyph**: ⊠ U+22A0
  - **word**: ABORTED
  - **contrast**: 7.6
- **content_HIDDEN**:
  - **text**: #c9d2de
  - **border**: 1px solid #5d6d82
  - **fill**: #253041
  - **glyph**: ◌ U+25CC
  - **word**: HIDDEN
  - **contrast**: 8.72
- **content_DRAFT**:
  - **text**: #7ab8ff
  - **border**: 1px dashed #7ab8ff
  - **fill**: transparent
  - **glyph**: ✎ U+270E (no emoji presentation; ✏ U+270F has one)
  - **word**: DRAFT
  - **contrast**: 8.37
- **content_PUBLISHED**:
  - **text**: #f0c65e
  - **border**: 1px solid #f0c65e
  - **fill**: transparent
  - **glyph**: ◆ U+25C6
  - **word**: PUBLISHED
  - **contrast**: 10.69
  - **note**: gold outline (state) vs solid gold (action); a publish in flight shows SENT · UNCONFIRMED until read-back, and the pill flips only on VERIFIED, never on HTTP success
- **session_lamp**:
  - **READY**:
    - **text**: #5ad48f
    - **glyph**: ✓
    - **word**: SESSION READY
    - **contrast**: 9.29
  - **PROBING**:
    - **text**: #7ab8ff
    - **glyph**: …
    - **word**: CHECKING SESSION
    - **contrast**: 8.37
  - **UNCONFIRMED**:
    - **text**: #f08a3c
    - **glyph**: ?
    - **word**: SESSION UNCONFIRMED
    - **contrast**: 6.94
  - **SIGNED_OUT**:
    - **text**: #ff8a80
    - **fill**: #3a1518
    - **glyph**: ✕
    - **word**: SIGNED OUT
    - **contrast**: 7.07
    - **note**: the only filled --bad chip in the app; server-proven refusal invalidates the earlier READY lamp (auth.mjs:199)
  - **NOT_AUTHORIZED (conditional)**:
    - **text**: #f08a3c
    - **border**: 1px solid #f08a3c
    - **glyph**: ⊘ U+2298
    - **word**: NOT AUTHORIZED
    - **contrast**: 6.94
    - **status**: CONDITIONAL, and the section E audit has now been done (`E_CONTENT_ADMIN_FEASIBILITY.md` E.3). Its finding: a role denial is per procedure, not per session, so a fifth session-lamp state has no source in the transport and is not adopted here; a per-action denial label is supported for the thirteen role-only paths E.3 lists, but only by matching the server's prose, because the response carries no code field (the same prose-coupling failure mode as `H_RISK_REGISTER.md` R-21), and for the four conflated paths it would be wrong some of the time. The construction that needs no invented signal is the pre-emptive one: read the role once per session, render the actions the role cannot perform as disabled with the reason, and re-check on send. `auth.mjs:54` keeps its four states (UNKNOWN, PROBING, READY, SIGNED_OUT) and `classifyError` (`outcome.mjs:58-73`) gains no FORBIDDEN class unless the director rules otherwise (K-34).
    - **note**: if K-34 admits the string-matched label, it is rendered on the action, never on the session lamp, as a hollow --warn chip plus a --warn-fill line naming the action the role lacks; never 'sign in again' (SSC:512). READ FAILED is never on the lamp: it is shown on the item row in --bad.
- **reuses_removed_today**: the STATE table above (its RUNNING row included; today's producer is the run screen, screens.mjs:224) replaces three colour reuses in the current UI: DONE painted --ok regardless of outcome (styles.mjs:44); the picker's 'ran' tag rendered with the VERIFIED pill class (screens.mjs:86); image 'picked' / 'missing' rendered with the VERIFIED / FAILED pill classes (screens.mjs:146). Each is an outcome colour carrying a non-outcome meaning (SSC:410-415; for DONE, SSC:223-227). 'ran', 'picked' and 'missing' become neutral tags; DONE gets the outcome lamp (D2.6 S2). Source-verified.


#### typography

- **ui_family**: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif (no @font-face, no fetch; resolves to Roboto or Samsung One on the operator's device)
- **mono_family**: ui-monospace, "Roboto Mono", "SF Mono", Menlo, Consolas, monospace (ids, procedure paths, hashes, snapshot keys, raw payloads only; amendment section 11)
- **display**: none bundled; brand identity is weight 900, tracking and the crimson hard offset (see brand). An embedded vector wordmark is option B (D-VC-4).
- **scale_status**: PENDING director/transcript confirmation (K-23). Recommended default is B's phone scale (judges G13/G1): it changes no colour and is the cheapest daylight-legibility gain on a Samsung panel.
- **recommended_phone_390**:
  - **body**: 16px/24px 400
  - **secondary**: 13px/18px 400 (floor for secondary and mono)
  - **pill_word**: 12px/1 700 uppercase 0.04em (the only 12 px text besides h3)
  - **h3**: 13px/18px 700 uppercase 0.06em --mute
  - **h2**: 18px/24px 700
  - **h1_screen_title**: 22px/28px 800
  - **control**: 16px/1 600; ink buttons 15px/1 800 uppercase 0.04em
  - **mode_word**: 14px/1 900 uppercase 0.08em
  - **count_numerals**: 17px/1 800 tabular-nums
- **recommended_desktop_1280**:
  - **body**: 15px/22px 400
  - **secondary**: 13px/18px
  - **pill_word**: 12px
  - **h3**: 13px
  - **h2**: 19px/24px 700
  - **h1**: 24px/30px 800
  - **hero_welcome**: 28px/34px 800 (Command Center only)
  - **mode_word**: 14px/1 900 uppercase 0.10em
  - **count_numerals**: 20px/1 800 tabular-nums
- **side_by_side**:
  - **visual-c**: 15px/22px body phone and desktop, 13px small, 12px caption
  - **design system v0.1 section 5**: body 14-15px 400/500, meta 12-13px 500, micro/status 11-12px 650, card title 15-16px, section 18-20px, page title 24px 750, brand display 28-36px
  - **style board section 6**: H1 40px, H2 28px, H3 20px, H4 16px, body 15px/150 %, small 13px/150 %, caption 12px/150 %
  - **today styles.mjs:19**: 15px/1.45
- **rules**: no weight below 400; tabular-nums on every count, budget and countdown (they update on the 1.5 s tick, app.mjs:268); px on .f-app, never rem (the carrier page's root font size is the game's, globals.css:223); nothing state-bearing under 12 px; the 11-12 px micro tier of v0.1 and the style board's 40 px H1 are not adopted (micro fails the daylight floor; 40 px belongs to a marketing masthead, not a 390 px overlay)


#### geometry and depth

- **radius**: cards 8 px; neutral buttons and inputs 6 px; lane cards 10 px; quick-action tiles 8 px (hard edge removed, judge G9); pills 3 px; dialogs/sheets 10 px; progress track 2 px; mode bands are full-bleed strips (no radius); the three production ink buttons (Start live write, Publish, Reconcile & resume) and the exceptional Re-send button are 0 px with a 5 px 5 px 0 offset shadow. Geometry is therefore a redundant risk channel: square = touches production or an unconfirmed send.
- **elevation**: paper 0 1px 0 rgba(0,0,0,.4); raised 0 4px 14px rgba(0,0,0,.45); float 0 12px 32px rgba(0,0,0,.55) + 1 px --edge2. backdrop-filter is decorative only and degrades to solid --raised.
- **ink_button**: radius 0; 2 px border on all four sides in the control's ink colour (--mut-ink on crimson, --pub-ink on gold, --warn on the amber-outlined Reconcile); 5 px 5 px 0 offset shadow in a darker step of the family (#5a0d13 crimson, #1b1200 gold, #33210f amber); press = translate 2 px 2 px + shadow 3 px over 90 ms (globals.css:281-289 at pin 345d18ac); focus = 2 px --focus outline at 3 px offset outside the shadow. 48 px tall on phone, 44 px desktop.
- **touch**: 44 px minimum everywhere; 48 px risk buttons; 56 px list rows and bottom-nav items; pills are not tap targets (rows are). Two controls sit under the floor today and are raised: the five nav tabs at 40 px (styles.mjs:27) and Close at 32 px (styles.mjs:25); the generic 44 px rule (styles.mjs:31) loses to both by specificity (MOB:123 floor). Source-verified.
- **spacing**: 4 / 8 / 12 / 16 / 24 / 32; card padding 12 px 14 px phone, 16 px 18 px desktop; page gutter 16 px phone, 24 px tablet, 32 px desktop


#### contrast table all pairs

- **kind**: text; **pair**: ink on bg; **fg**: #f3efe6; **bg**: #0b121a; **ratio**: 16.4; **passes**: True
- **kind**: text; **pair**: ink on paper; **fg**: #f3efe6; **bg**: #121b26; **ratio**: 15.12; **passes**: True
- **kind**: text; **pair**: ink on raised; **fg**: #f3efe6; **bg**: #1a2532; **ratio**: 13.51; **passes**: True
- **kind**: text; **pair**: ink on float; **fg**: #f3efe6; **bg**: #212f3f; **ratio**: 11.86; **passes**: True
- **kind**: text; **pair**: ink2 on raised; **fg**: #fffaf0; **bg**: #1a2532; **ratio**: 14.9; **passes**: True
- **kind**: text; **pair**: mute on bg; **fg**: #a9b3c2; **bg**: #0b121a; **ratio**: 8.89; **passes**: True
- **kind**: text; **pair**: mute on paper; **fg**: #a9b3c2; **bg**: #121b26; **ratio**: 8.19; **passes**: True
- **kind**: text; **pair**: mute on raised; **fg**: #a9b3c2; **bg**: #1a2532; **ratio**: 7.32; **passes**: True
- **kind**: text; **pair**: dim on bg; **fg**: #8a97ab; **bg**: #0b121a; **ratio**: 6.36; **passes**: True
- **kind**: text; **pair**: dim on paper; **fg**: #8a97ab; **bg**: #121b26; **ratio**: 5.86; **passes**: True
- **kind**: text; **pair**: acc on bg; **fg**: #7ab8ff; **bg**: #0b121a; **ratio**: 9.08; **passes**: True
- **kind**: text; **pair**: acc on paper; **fg**: #7ab8ff; **bg**: #121b26; **ratio**: 8.37; **passes**: True
- **kind**: text; **pair**: acc on raised; **fg**: #7ab8ff; **bg**: #1a2532; **ratio**: 7.48; **passes**: True
- **kind**: text; **pair**: acc on accfill (READ ONLY band word); **fg**: #7ab8ff; **bg**: #14304f; **ratio**: 6.47; **passes**: True
- **kind**: text; **pair**: ink on accfill (READ ONLY counts); **fg**: #f3efe6; **bg**: #14304f; **ratio**: 11.69; **passes**: True
- **kind**: text; **pair**: acc-ink on acc (blue primary button); **fg**: #0b121a; **bg**: #7ab8ff; **ratio**: 9.08; **passes**: True
- **kind**: text; **pair**: mut-ink on mut (LIVE WRITE band/button); **fg**: #fffaf0; **bg**: #c0242f; **ratio**: 5.71; **passes**: True
- **kind**: text; **pair**: pub-ink on pub (PUBLISH band/button); **fg**: #1b1200; **bg**: #e6b84f; **ratio**: 10.0; **passes**: True
- **kind**: text; **pair**: pub-text on bg; **fg**: #f0c65e; **bg**: #0b121a; **ratio**: 11.6; **passes**: True
- **kind**: text; **pair**: pub-text on paper (PUBLISHED pill, pending badge); **fg**: #f0c65e; **bg**: #121b26; **ratio**: 10.69; **passes**: True
- **kind**: text; **pair**: pub-text on raised; **fg**: #f0c65e; **bg**: #1a2532; **ratio**: 9.56; **passes**: True
- **kind**: text; **pair**: warn #f08a3c on bg; **fg**: #f08a3c; **bg**: #0b121a; **ratio**: 7.53; **passes**: True
- **kind**: text; **pair**: warn on paper (PAUSED/INCOMPLETE pill, authorization-denied action state); **fg**: #f08a3c; **bg**: #121b26; **ratio**: 6.94; **passes**: True
- **kind**: text; **pair**: warn on raised; **fg**: #f08a3c; **bg**: #1a2532; **ratio**: 6.21; **passes**: True
- **kind**: text; **pair**: warn on warnfill (warn banner lead); **fg**: #f08a3c; **bg**: #33210f; **ratio**: 6.16; **passes**: True
- **kind**: text; **pair**: warn on rec-hatch #4a2f12 (C stripe); **fg**: #f08a3c; **bg**: #4a2f12; **ratio**: 4.93; **passes**: True
- **kind**: text; **pair**: warn on rec-hatch #452a10; **fg**: #f08a3c; **bg**: #452a10; **ratio**: 5.28; **passes**: True
- **kind**: text; **pair**: warn on rec-hatch #3f2610 (proposed stripe); **fg**: #f08a3c; **bg**: #3f2610; **ratio**: 5.62; **passes**: True
- **kind**: text; **pair**: ink on warnfill; **fg**: #f3efe6; **bg**: #33210f; **ratio**: 13.4; **passes**: True
- **kind**: text; **pair**: ink on rec-hatch #3f2610 (RECOVERY counts, worst stripe); **fg**: #f3efe6; **bg**: #3f2610; **ratio**: 12.23; **passes**: True
- **kind**: text; **pair**: warnC #f5a25a on paper (C original, side by side); **fg**: #f5a25a; **bg**: #121b26; **ratio**: 8.42; **passes**: True
- **kind**: text; **pair**: warnC on rec-hatch #4a2f12; **fg**: #f5a25a; **bg**: #4a2f12; **ratio**: 5.98; **passes**: True
- **kind**: text; **pair**: sent on bg; **fg**: #e79cff; **bg**: #0b121a; **ratio**: 9.5; **passes**: True
- **kind**: text; **pair**: sent on paper; **fg**: #e79cff; **bg**: #121b26; **ratio**: 8.75; **passes**: True
- **kind**: text; **pair**: sent on sentfill; **fg**: #e79cff; **bg**: #2c1f3d; **ratio**: 7.73; **passes**: True
- **kind**: text; **pair**: sent on senthatch (worst stripe); **fg**: #e79cff; **bg**: #3d2a55; **ratio**: 6.38; **passes**: True
- **kind**: text; **pair**: ink on sentfill; **fg**: #f3efe6; **bg**: #2c1f3d; **ratio**: 13.35; **passes**: True
- **kind**: text; **pair**: ink on senthatch; **fg**: #f3efe6; **bg**: #3d2a55; **ratio**: 11.02; **passes**: True
- **kind**: text; **pair**: ok on bg; **fg**: #5ad48f; **bg**: #0b121a; **ratio**: 10.08; **passes**: True
- **kind**: text; **pair**: ok on paper (session READY lamp); **fg**: #5ad48f; **bg**: #121b26; **ratio**: 9.29; **passes**: True
- **kind**: text; **pair**: ok on okfill (VERIFIED pill); **fg**: #5ad48f; **bg**: #10301f; **ratio**: 7.68; **passes**: True
- **kind**: text; **pair**: ink on okfill; **fg**: #f3efe6; **bg**: #10301f; **ratio**: 12.5; **passes**: True
- **kind**: text; **pair**: bad on bg; **fg**: #ff8a80; **bg**: #0b121a; **ratio**: 8.25; **passes**: True
- **kind**: text; **pair**: bad on paper (FAILED pill, SIGNED OUT lamp); **fg**: #ff8a80; **bg**: #121b26; **ratio**: 7.6; **passes**: True
- **kind**: text; **pair**: bad on badfill; **fg**: #ff8a80; **bg**: #3a1518; **ratio**: 7.07; **passes**: True
- **kind**: text; **pair**: ink on badfill; **fg**: #f3efe6; **bg**: #3a1518; **ratio**: 14.07; **passes**: True
- **kind**: text; **pair**: hidden text on hidden fill; **fg**: #c9d2de; **bg**: #253041; **ratio**: 8.72; **passes**: True
- **kind**: text; **pair**: ORPHANED inverted: bg text on ink fill; **fg**: #0b121a; **bg**: #f3efe6; **ratio**: 16.4; **passes**: True
- **kind**: text; **pair**: ORPHANED alt: bg text on warn fill; **fg**: #0b121a; **bg**: #f08a3c; **ratio**: 7.53; **passes**: True
- **kind**: text; **pair**: disabled: mute on raised (100% opacity); **fg**: #a9b3c2; **bg**: #1a2532; **ratio**: 7.32; **passes**: True
- **kind**: text; **pair**: ink on 88% scrim over white; **fg**: #f3efe6; **bg**: #282e35; **ratio**: 11.94; **passes**: True
- **kind**: text; **pair**: mute on 88% scrim; **fg**: #a9b3c2; **bg**: #282e35; **ratio**: 6.47; **passes**: True
- **kind**: text; **pair**: Daylight hc-mute on paper; **fg**: #c5ccd8; **bg**: #121b26; **ratio**: 10.74; **passes**: True
- **kind**: text; **pair**: Daylight hc-dim on paper; **fg**: #a3afc1; **bg**: #121b26; **ratio**: 7.81; **passes**: True
- **kind**: nontext; **pair**: mut fill vs bg; **fg**: #c0242f; **bg**: #0b121a; **ratio**: 3.17; **passes**: True
- **kind**: nontext; **pair**: mut fill vs paper (mitigated: 2px ivory border all sides); **fg**: #c0242f; **bg**: #121b26; **ratio**: 2.92; **passes**: False
- **kind**: nontext; **pair**: mut-ink 2px border vs mut (button boundary inner); **fg**: #fffaf0; **bg**: #c0242f; **ratio**: 5.71; **passes**: True
- **kind**: nontext; **pair**: mut-ink 2px border vs paper (button boundary outer); **fg**: #fffaf0; **bg**: #121b26; **ratio**: 16.67; **passes**: True
- **kind**: nontext; **pair**: mut-edge rule vs bg; **fg**: #ff5f5a; **bg**: #0b121a; **ratio**: 6.31; **passes**: True
- **kind**: nontext; **pair**: mut-edge rule vs paper (top-bar underline); **fg**: #ff5f5a; **bg**: #121b26; **ratio**: 5.81; **passes**: True
- **kind**: nontext; **pair**: mut-edge rule vs raised; **fg**: #ff5f5a; **bg**: #1a2532; **ratio**: 5.19; **passes**: True
- **kind**: nontext; **pair**: count chip: raised fill vs mut band (C, FAILS -> replaced); **fg**: #1a2532; **bg**: #c0242f; **ratio**: 2.61; **passes**: False
- **kind**: nontext; **pair**: count chip: bg fill vs mut band (candidate); **fg**: #0b121a; **bg**: #c0242f; **ratio**: 3.17; **passes**: True
- **kind**: nontext; **pair**: count chip: mut-shadow #5a0d13 vs mut band (candidate); **fg**: #5a0d13; **bg**: #c0242f; **ratio**: 2.35; **passes**: False
- **kind**: nontext; **pair**: count chip: ivory 1px outline vs mut band (ADOPTED); **fg**: #fffaf0; **bg**: #c0242f; **ratio**: 5.71; **passes**: True
- **kind**: nontext; **pair**: count chip: raised vs rec-hatch #3f2610 (C, FAILS -> replaced); **fg**: #1a2532; **bg**: #3f2610; **ratio**: 1.1; **passes**: False
- **kind**: nontext; **pair**: count chip: warn outline vs rec-hatch #3f2610 (ADOPTED); **fg**: #f08a3c; **bg**: #3f2610; **ratio**: 5.62; **passes**: True
- **kind**: nontext; **pair**: count chip: acc outline vs accfill (ADOPTED); **fg**: #7ab8ff; **bg**: #14304f; **ratio**: 6.47; **passes**: True
- **kind**: nontext; **pair**: count chip: pub-ink outline vs pub (ADOPTED); **fg**: #1b1200; **bg**: #e6b84f; **ratio**: 10.0; **passes**: True
- **kind**: nontext; **pair**: pub fill vs paper (seal border, underline); **fg**: #e6b84f; **bg**: #121b26; **ratio**: 9.36; **passes**: True
- **kind**: nontext; **pair**: pub fill vs bg; **fg**: #e6b84f; **bg**: #0b121a; **ratio**: 10.16; **passes**: True
- **kind**: nontext; **pair**: edge vs paper (control boundary); **fg**: #5d6d82; **bg**: #121b26; **ratio**: 3.28; **passes**: True
- **kind**: nontext; **pair**: edge vs bg; **fg**: #5d6d82; **bg**: #0b121a; **ratio**: 3.56; **passes**: True
- **kind**: nontext; **pair**: edge2 vs raised; **fg**: #738399; **bg**: #1a2532; **ratio**: 4.01; **passes**: True
- **kind**: nontext; **pair**: edge2 vs paper; **fg**: #738399; **bg**: #121b26; **ratio**: 4.49; **passes**: True
- **kind**: nontext; **pair**: line vs paper (decorative only, exempt); **fg**: #2a3644; **bg**: #121b26; **ratio**: 1.41; **passes**: False
- **kind**: nontext; **pair**: focus ring vs bg; **fg**: #fffaf0; **bg**: #0b121a; **ratio**: 18.09; **passes**: True
- **kind**: nontext; **pair**: focus ring vs paper; **fg**: #fffaf0; **bg**: #121b26; **ratio**: 16.67; **passes**: True
- **kind**: nontext; **pair**: focus ring vs pub with no offset (why offset 3px is mandatory); **fg**: #fffaf0; **bg**: #e6b84f; **ratio**: 1.78; **passes**: False
- **kind**: nontext; **pair**: PLANNED dotted border dim vs paper; **fg**: #8a97ab; **bg**: #121b26; **ratio**: 5.86; **passes**: True
- **kind**: nontext; **pair**: SKIPPED border edge vs paper; **fg**: #5d6d82; **bg**: #121b26; **ratio**: 3.28; **passes**: True
- **kind**: nontext; **pair**: sent dot vs paper (nav dot); **fg**: #e79cff; **bg**: #121b26; **ratio**: 8.75; **passes**: True
- **kind**: nontext; **pair**: sent dot vs raised; **fg**: #e79cff; **bg**: #1a2532; **ratio**: 7.82; **passes**: True
- **kind**: nontext; **pair**: warn dot vs paper; **fg**: #f08a3c; **bg**: #121b26; **ratio**: 6.94; **passes**: True
- **kind**: nontext; **pair**: warn dot vs raised; **fg**: #f08a3c; **bg**: #1a2532; **ratio**: 6.21; **passes**: True
- **kind**: nontext; **pair**: warn 2px rule vs paper (RECOVERY underline); **fg**: #f08a3c; **bg**: #121b26; **ratio**: 6.94; **passes**: True
- **kind**: nontext; **pair**: ok cell vs bg track; **fg**: #5ad48f; **bg**: #0b121a; **ratio**: 10.08; **passes**: True
- **kind**: nontext; **pair**: acc cell vs bg track; **fg**: #7ab8ff; **bg**: #0b121a; **ratio**: 9.08; **passes**: True
- **kind**: nontext; **pair**: sent cell vs bg track; **fg**: #e79cff; **bg**: #0b121a; **ratio**: 9.5; **passes**: True
- **kind**: nontext; **pair**: bad cell vs bg track; **fg**: #ff8a80; **bg**: #0b121a; **ratio**: 8.25; **passes**: True
- **kind**: nontext; **pair**: warn cell vs bg track; **fg**: #f08a3c; **bg**: #0b121a; **ratio**: 7.53; **passes**: True
- **kind**: nontext; **pair**: edge (SKIPPED cell) vs bg track; **fg**: #5d6d82; **bg**: #0b121a; **ratio**: 3.56; **passes**: True
- **kind**: nontext; **pair**: lane combat vs bg; **fg**: #e5484d; **bg**: #0b121a; **ratio**: 4.81; **passes**: True
- **kind**: nontext; **pair**: lane items vs bg; **fg**: #3b82f6; **bg**: #0b121a; **ratio**: 5.12; **passes**: True
- **kind**: nontext; **pair**: lane quests vs bg; **fg**: #d5a360; **bg**: #0b121a; **ratio**: 8.28; **passes**: True
- **kind**: nontext; **pair**: lane locations vs bg; **fg**: #2fbfc9; **bg**: #0b121a; **ratio**: 8.44; **passes**: True
- **kind**: nontext; **pair**: lane characters vs bg; **fg**: #8b5cf6; **bg**: #0b121a; **ratio**: 4.45; **passes**: True
- **kind**: nontext; **pair**: lane systems vs bg; **fg**: #7c8797; **bg**: #0b121a; **ratio**: 5.17; **passes**: True
- **kind**: nontext; **pair**: lane combat vs paper; **fg**: #e5484d; **bg**: #121b26; **ratio**: 4.43; **passes**: True
- **kind**: nontext; **pair**: lane items vs paper; **fg**: #3b82f6; **bg**: #121b26; **ratio**: 4.72; **passes**: True
- **kind**: nontext; **pair**: lane characters vs paper; **fg**: #8b5cf6; **bg**: #121b26; **ratio**: 4.1; **passes**: True
- **kind**: nontext; **pair**: lane systems vs paper; **fg**: #7c8797; **bg**: #121b26; **ratio**: 4.77; **passes**: True
- **kind**: nontext; **pair**: hidden fill vs paper (slate pill boundary; pill also has edge border); **fg**: #253041; **bg**: #121b26; **ratio**: 1.3; **passes**: False
- **kind**: nontext; **pair**: ORPHANED inverted ivory pill vs paper; **fg**: #f3efe6; **bg**: #121b26; **ratio**: 15.12; **passes**: True
- **kind**: info; **pair**: warn #f08a3c vs pub #e6b84f (luminance separation); **fg**: #f08a3c; **bg**: #e6b84f; **ratio**: 1.35; **passes**: 
- **kind**: info; **pair**: warnC #f5a25a vs pub (C original); **fg**: #f5a25a; **bg**: #e6b84f; **ratio**: 1.11; **passes**: 
- **kind**: info; **pair**: ivory ORPHANED fill vs pub gold; **fg**: #f3efe6; **bg**: #e6b84f; **ratio**: 1.61; **passes**: 
- **kind**: info; **pair**: sent vs lane violet; **fg**: #e79cff; **bg**: #8b5cf6; **ratio**: 2.14; **passes**: 
- **kind**: info; **pair**: bad vs mut; **fg**: #ff8a80; **bg**: #c0242f; **ratio**: 2.6; **passes**: 
- **kind**: info; **pair**: warn #f08a3c vs bad #ff8a80; **fg**: #f08a3c; **bg**: #ff8a80; **ratio**: 1.09; **passes**: 
- **kind**: info; **pair**: warn vs pub-text #f0c65e (PAUSED vs PUBLISHED text); **fg**: #f08a3c; **bg**: #f0c65e; **ratio**: 1.54; **passes**: 
- **kind**: info; **pair**: today disabled ink@.45 over paper; **fg**: #777a7c; **bg**: #121b26; **ratio**: 4.01; **passes**: 
- **kind**: info; **pair**: mockup crimson #cd1c24 as text on bg; **fg**: #cd1c24; **bg**: #0b121a; **ratio**: 3.39; **passes**: 

## D2.3 Component inventory

| WCM equivalent | component | renders | screens | states | notes |
|---|---|---|---|---|---|
| AppShell (WCM:32-34) | **AppShell (top bar phone / rail + content desktop)** | wordmark; session lamp (READY / CHECKING / UNCONFIRMED / SIGNED OUT; no fifth authorization state: denial is per action, not per session, E.3); Close raised to 44 px (today 32 px, styles.mjs:25; the button is created at app.mjs:66); Back on sub-screens; a 3 px underline in --mut-edge while any mutation job is RUNNING, in --pub while a publish is in flight, in the RECOVERY hatch while any job holds SENT or ORPHANED (judges G7/G5); the underline is present on EVERY screen, never animates | all | idle; write-in-flight; publish-in-flight; recovery-pending; auth non-ready (the full explanatory banner of app.mjs:143-150 renders under the bar on the screen that needs it, with Re-check) | 56 px sticky --paper on phone with a 1 px crimson brand rule; 232 px rail on desktop |
| AppShell navigation (WCM:34; WCM:605 keeps nav loosely specified) | **NavRail (desktop >= 1024)** | destinations as 44 px rows with glyph + label; active row on --raised with a 3 px --mut-edge left marker (crimson as a <= 4 px accent only; the mockup's crimson-tinted active fill is departure 12); static badges: orphan count, --sent dot when any SENT item exists (journal.resumable()), --warn dot for PAUSED, gold-OUTLINE pending-review count on Content Admin; 'Active work' block with the job's mini mode chip; session lamp + version + pin SHA in the footer | all desktop | active / inactive / badged / disabled (mute on raised, reason as title text) | destination set is the IA panel's (K-20); the visual system does not depend on it |
| AppShell navigation (WCM:34) | **BottomNav (phone < 768)** | <= 5 items, 56 px + safe-area-inset-bottom, 24 px glyph over 12 px/600 label always visible; current = --acc text + 3 px --acc top rail + glyph, never colour alone; same static dots/badges as the rail (Jobs/Recovery: --sent dot, --warn dot, orphan count; Admin: gold-outline count) | all phone screens including the run screen (judge U7: recommended NOT hidden during a run; if the director takes the 56 px back, the top-bar underline is the mandatory compensation) | current / inactive / badged | no icon-only tabs |
| AppShell navigation (WCM:34) | **MoreSurface (phone)** | a dialog sheet on --float with a visible Close, listing secondary destinations (Captures library, Settings, Diagnostics, Export journal) as 56 px rows with glyph + label; Escape and Close dismiss; backdrop at full opacity from the first frame | phone | open / closed; rows may be badged | 120 ms enter only; content final on first paint |
| OperationHeader (WCM:44-46) + OperationCounts chips (WCM:64-66) | **ModeBand (operation-mode header)** | 44 px full-width strip, sticky under the top bar (phone) or at the top of the content column (desktop): [glyph + MODE in 14px/900] left, count chips right (outlined in the band's text colour, no fill: 'creates 3 · updates 2 · uploads 1 · reads 6 · publishes 0'; phone shows the two most consequential and a ▾ that expands to a second 32 px line). Same height in every mode so content never jumps. Renders BEFORE any item list. Counts come from the parsed plan (preflight) or the journal (run), labelled with the amendment section 8 vocabulary; deletes shown only if a future authorized workflow adds them | manifest preflight; run; publish flow; any job in PAUSED/INCOMPLETE or holding SENT/ORPHANED (RECOVERY, computed per `A_ARCHITECTURE_MAP.md`); Command Center active-work card carries a 28 px mini chip. Settings and the Captures library show NO band: the band's presence itself means 'this screen can touch or has touched production' | READ ONLY / LIVE WRITE / PUBLISH / RECOVERY (+ REVIEW reserved); each with a readiness blocker line when auth is not READY ('blocked: session unconfirmed') | never animates; <header aria-live=polite> |
| SystemHealth (WCM:40-42) inside CommandCenter (WCM:36-38) | **CommandCenter.ReadinessCard** | three lamps, each glyph + word + specific state: SESSION (✓ signed in / ? unconfirmed / ✕ refused; ⊘ not authorized only under the D2.2 session_lamp condition), REPO (✓ reachable · listed 4 m ago / ✕ listing failed / – not configured), BUDGET (✓ 12 % used / △ 80 % / ✕ TRIPPED until hh:mm); headline computed per state ('Reads and writes available' / 'Public reads only: session unconfirmed'); green banner only when every lamp is ✓. Fed from state Forge already holds (auth probe result, pickerAt/pickerError, Budget.status()), never a fresh poll (R-03, R-16) | Command Center | all-ready / degraded / blocked / unknown ('not checked' in --mute, never green) | mockup departure 5 |
| ActivityRow (WCM:108-110) / ActionCard resume entry (WCM:48-50) | **CommandCenter.ActiveWorkCard** | the running/paused/resumable job with its mini mode chip, state pill + outcome lamp, one primary action in the job's own construction (Reconcile & resume amber ink / Resume blue / Re-read unverified amber outline / Open neutral); an orphan card pinned above it when any ORPHANED item exists | Command Center; Jobs | none (empty state with atmosphere) / running / paused (reason chip) / SENT pending / orphaned / incomplete | replaces today's generic .f-banner.warn open-job banner (screens.mjs:18-26) |
| ActionCard (WCM:48-50) | **CommandCenter.QuickActionTile** | 88 px raised tile, 8 px radius, --edge boundary, blue accent glyph + title + 13 px --mute subtitle; NO crimson, green, violet or gold fill (departures 1, 2, 9); glow ring only on :focus-visible/:active | Command Center (2x2 phone, 4-up desktop) | enabled / disabled (mute text on raised, reason caption) / capability-missing (rendered as disabled with 'needs X' caption, never hidden) | the number and order of tiles is the IA panel's |
| ContentLaneCard (WCM:52-54) | **LaneCard** | 10 px radius, 1 px lane-tint edge, gradient wash 20 % -> 0 %, inline-SVG lane glyph (createElementNS, <= 400 bytes, aria-hidden) at 12 % alpha, title 16px/700 ivory, subtitle 13 px --mute, chevron; 358 x 96 px strip on phone, tile on desktop; text always on a solid 88 % --bg scrim (11.94:1 worst case); glow 0 0 24px tint@35 % on focus/press only | Command Center; lane landing | idle / focused-pressed (glow) / with a slate HIDDEN count pill (global token, never lane-tinted) | carries no lifecycle state; the two card families cannot be confused: lane cards have colour and glow and no state, status cards have state and no glow |
| SystemHealth (WCM:40-42) | **StatusTile / HealthRow** | glyph + word + detail + optional action (Re-check); used for session, repo, budget, storage-persisted, images-present, sync | Command Center; Settings/Diagnostics; run screen Technical group | ok / caution / failed / unknown / checking; TRIPPED renders the budget track as --bad hatch with ✕ and 'TRIPPED until hh:mm' and is auto-expanded out of the Technical group | 'All systems nominal' never appears as a green banner alone |
| StateChip (SSC:430-433) as used by ItemProgress and ActivityRow | **StatePill** | see design_tokens.state_pills; job states, item states, content states, session lamp share one anatomy (glyph box + word + border style + fill construction) | everywhere a state is shown | PLANNED SENT CONFIRMED VERIFIED FAILED ORPHANED SKIPPED PAUSED INCOMPLETE RUNNING DONE ABORTED; HIDDEN DRAFT PUBLISHED; outcome lamps VERIFIED ALL / UNVERIFIED / FAILED | class names .f-pill.<STATE> kept so forge/test/ui.test.mjs:116 still selects them; pill() (screens.mjs:8) reads a STATE table; the VERIFIED/FAILED pill classes are no longer borrowed for 'ran' / 'picked' / 'missing' (screens.mjs:86,146) - those become neutral tags |
| SafetyCallout (WCM:92-94) | **Banner / Callout** | full-width, 2 px hard border in its construction, glyph + bold lead sentence (15/16 px) + secondary sentence (13 px) + next safe action; constructions: info (--acc-fill, --acc lead), ok (--ok-fill), warn (--warn-fill), bad (--bad-fill), SENT (hatched --sent-fill, dashed --sent border, '? 1 WRITE UNCONFIRMED · nothing is retried; Reconcile reads the server first'), NOT AUTHORIZED (conditional per D2.2 session_lamp; --warn-fill, ⊘, names the action the role lacks), full-capture advisory (▣ FULL in --warn + the repository-persistence sentence of screens.mjs:123-125) | preflight; run; jobs; admin queue; settings | static; role=alert when it appears; never auto-dismisses | toasts are a secondary echo: ok/info auto-dismiss 4 s, warn/bad persist until tapped and stack (judges G5/G7); a toast is never the sole carrier of PAUSED/ORPHANED/SENT |
| no WCM component; button hierarchy owned by IRM:251-271 | **ActionButton (per authority lane)** | neutral: --raised fill, 1 px --edge, --ink, 6 px radius. read-primary: --acc fill, --acc-ink text, 6 px ('Run 5 reads · zero mutations'). write-primary (ink): radius 0, --mut fill, 2 px --mut-ink border all sides, --mut-ink text, 5px 5px 0 #5a0d13 shadow, glow on focus/press only ('Start job → writes 5 records'). publish-primary (ink): radius 0, --pub fill, 2 px --pub-ink border, --pub-ink text, 5px 5px 0 #1b1200 shadow ('Publish 1 record → player-visible'). reconcile (ink outline): radius 0, transparent, 2 px --warn border, --warn text, ↻ glyph ('Reconcile & resume · reads first, never re-sends'). re-read: --warn outline, 6 px ('Re-read unverified items'). re-send (exceptional): radius 0, transparent, 2 px --bad border, --bad text, positioned last, label 'Re-send update (I have checked the record)'. destructive-local: --bad outline 6 px (cache clear, snapshot delete, forget PAT), each with its own sentence (contract section 9). disabled: --mute on --raised at 100 % opacity, --edge border, reason as a caption below (never opacity .45, styles.mjs:32) | preflight, run, jobs, orphan card, admin detail, publish seal, settings | enabled / pressed / focused / disabled-with-reason; a disabled-to-enabled change never animates | green is never a button; no control on a SENT item is labelled Retry or Send again |
| JobProgress (WCM:80-82) | **SegmentedProgress** | 12 px track, 1 px --edge, one cell per item (<= 40; 41-120 bucketed by worst state; > 120 plain fraction), cell fills = state colours with the same constructions (VERIFIED solid ok, CONFIRMED solid acc, SENT orchid hatch, FAILED solid bad with 1 px gaps, SKIPPED --edge, ORPHANED ivory, PLANNED transparent); the in-flight cell carries the ember sheen; beneath it one 13 px tabular line '7 verified · 1 SENT unconfirmed · 1 failed · 3 planned · 12 total' with glyph + colour per count; role=progressbar with an aria-label carrying the sentence | run; active-work card (mini) | running (sheen) / paused / done; the sheen element exists only while app.state.running === jobId and a jsdom test asserts its removal on PAUSED/DONE/INCOMPLETE | patched in place with stable keys; the 1.5 s replace() tick (app.mjs:268, dom.mjs:27) must not rebuild it (judges G3/G6) |
| ItemProgress (WCM:84-86) | **ItemRow** | >= 56 px: [idx][name 16 px][pill] then 13 px [entity · phase · id mono]; caption line for SENT/ORPHANED/CONFIRMED/INCOMPLETE on phone; error 13 px --bad wrapped; drift as <details> 'drift on N keys' in --warn; left rule 3 px: dashed --sent for SENT, solid ivory for ORPHANED, solid --bad for FAILED (line style differs, not only hue); tap opens detail | run; admin detail; preflight plan list | all item states | manifest order is kept; the count line above is the summary |
| SystemHealth rate-budget domain (WCM:42; WFA:414) | **BudgetMeter** | [path mono 13 px][8 px track --edge, fill --acc][used/allowance tabular][resets mm:ss]; >= 80 % fill --warn + △; TRIPPED = --bad hatch, ✕, 'TRIPPED until hh:mm', hoisted out of the Technical group and into the pause card | run (Technical group on phone, inspector column on desktop); Command Center budget lamp (worst line) | unspent / healthy / near limit / tripped | numbers step instantly, never count up |
| DiffView (WCM:116-118; WCM:627-629) | **DiffView** | human-facing before/after rows: [field label][live value][→][sent/proposed value], changed values emphasised with --warn text and a 3 px --warn left rule (never --bad: drift is caution, failure is failure); unchanged rows in --mute; raw JSON behind a 'Raw' <details> in mono 13 px; on phone each row stacks label / before / after | preflight (live-state diff where safe); run (drift on N keys); admin detail (what changed in human terms, brief section 8) | no change / changed / drift after read-back / unreadable (live value 'unread' in --warn with ◔) | a diff never implies the write landed; the row's pill does |
| Preview (WCM:623-625) | **PreviewFrame** | a --raised panel, 1 px --edge2 border, 'PREVIEW' 13 px/700 --mute eyebrow, the class's client-side render path inside (E_CONTENT_ADMIN_FEASIBILITY per class), a 'Preview reflects the LIVE hidden record read at hh:mm' freshness line, and the record's content pill (HIDDEN / PUBLISHED); no lane wash, no glow, no atmosphere behind it | admin detail / preview | available / no renderer for this class (neutral empty state, never an error) / stale (freshness line in --warn) | visually distinct from editable controls (v0.1 section 12); publish controls never sit inside the frame |
| SafetyCallout (WCM:92-94) + RecoveryDecision (WCM:96-98); construction detail in D2.3.2 | **RecoveryCard (halt card + orphan card)** | halt card: full width, 2 px hard border in the reason's construction, RECOVERY mini band, 18 px headline naming the pause reason from the journal vocabulary (SESSION in --bad with the ✕ SIGNED OUT chip repeated and Resume disabled with resumeBlockedReason as caption, app.mjs:159-163; 429 in --warn with the tripped meter hoisted in and a tabular countdown; AMBIGUOUS/ORPHANED with the SENT banner), what may already have been sent, what permits resume, and ONE primary in the recovery construction. Orphan card: 2 px solid --warn hard border, hatched 8 px corner tab 'DECIDE', the inverted ORPHANED pill, what is known, candidate rows (mono id + name) each with an 'Adopt <id>' --warn-outlined ink button (never preselected), paste-an-id input for creates, 'Skip (leave as is) · nothing is deleted' neutral button, and the Re-send button last in --bad outline; technical detail under <details> | run; jobs; Command Center (pinned above active work) | paused-session / paused-429 / paused-network / paused-user / SENT pending / orphaned with candidates / orphaned without candidates / incomplete | never a green or blue primary on this card; recovery is a screen, not a toast (brief section 15) |
| ConsequenceConfirmation (WCM:76-78) | **ConfirmationSurface** | for LIVE WRITE, PUBLISH and RE-SEND only: a sheet on --float (phone: docked bottom; desktop: centred 480 px) whose content is final on first paint, backdrop at full opacity, page frozen (sheen paused). It restates the mode band's counts, the record names with their CURRENT pill (HIDDEN), the session lamp READY, the exact flip in words ('hidden: true → false on 7c3…'), dependency warnings (referenced records still hidden, ▲ in --warn), and offers exactly one action button in the mode's ink construction plus a neutral Cancel at the far end; Confirm is disabled for ~600 ms after the sheet appears (an arming delay of the ACTION, not of state); dismiss only by Cancel/Escape, never backdrop tap; never press-and-hold. Publish adds the 'seal' framing: 2 px --pub border with an inner 1 px --pub rule at 4 px inset. Local-destructive actions (cache clear, snapshot delete, forget PAT) keep window.confirm (app.mjs:172-175). | preflight start; resume-with-re-send; publish; admin publish/unpublish | arming (Confirm disabled) / armed / blocked (session not READY: the button is disabled with the reason, the sheet still shows the facts) | the confirmation LEVEL (typed record count, plain armed tap) remains the director's (K-12 / U1); replacing window.confirm is an interaction change the director accepts (U8/UD-5) |
| CapturePersistence (WCM:100-102) | **CaptureRow (full-capture visibility)** | ▣ FULL in --warn before the path for persist:'full', ▢ SUMMARY in --mute otherwise; after the run two separate verdicts: 'read ok' ✓ --ok / 'read failed' ✕ --bad, and 'body persisted' ✓ / 'not persisted' ✕ with persistError in mono; captureLabel wording kept (screens.mjs:104-112) | preflight; run; captures library | planned / read ok + persisted / read ok + NOT persisted / read failed | a successful read never stands in for a persisted body (contract section 7) |
| AppShell brand (WCM:34) | **Brand / Wordmark** | option A (recommended): 'FORGE' system-ui 900 uppercase 0.14em --ink2 with a 2px 2px 0 (phone) / 3px 3px 0 (desktop) #c0242f text-shadow and a 4 px skewed crimson slash <span>; 'TNR' 11px/800 0.20em --mute above it on desktop; tagline 'CREATE · VALIDATE · DEPLOY' 11px/700 --mute static. Option B: embedded createElementNS path (~1.5 KB). Crimson in the brand is never a fill taller than 4 px, so the brand cannot be mistaken for a LIVE WRITE band | top bar; rail header; Command Center hero strip (96 px phone / 160 px desktop, CSS atmosphere only) | static | D-VC-4 / U4 |

### D2.3.1 WCM components with no row above

The rows above cover 15 of the 25 WCM responsibilities under this file's names (mapping column). The remaining ten are added here so that no WCM responsibility is unowned; the 'forge data source today' column names the state Forge already holds, so that no row implies a capability the source lacks (WCM:607-629; `H_RISK_REGISTER.md`, R-16). Responsibility text is the owner's; only the construction is this file's.

| WCM component | responsibility owner | forge data source today | states to render | construction here / status |
|---|---|---|---|---|
| **EvidencePanel** | WCM:88-90 | item.diffs, manifest hash, journal record, capture snapshotKey and bytes (runner.mjs:611-621), procedure paths, Budget.status() per path (bucket.mjs:204-216) | collapsed / expanded / copy or export available | phone: a full-screen sheet or a secondary route; desktop: a side panel (WFA:482). Sections in the WFA:471-480 order: IDs, path and hash, procedure, raw payload, journal state, phase and timestamps, before and after capture, asserted keys, verification diffs, bundle metadata, provenance (SCR:472-480 lists the same set). Progressive disclosure, never miniaturisation (MOB:153-157): consequence copy never below 14 px and IDs wrap in their own mono region; today IDs are inline 12 px mono (styles.mjs:41). Exact sizes PENDING K-23. |
| **ResultSummary** | WCM:104-106 | jobOutcome(job) (journal.mjs:76-88); bundle.postflight counts match / diff / unverified / failed / skipped / unresolved (app.mjs:385-392); the last Github.put result or GithubError (app.mjs:402-403) | Verified / Finished with failures / Finished unverified / open / capture-only complete / capture-only failed or partial / sync succeeded, failed, not configured | one line per SSC:462-470 question, each with its own lamp; a SYNC lamp (✓ committed @sha / ✕ sync failed / – not configured) is its own claim beside the game verdict (WCM:468). Today sync is a toast plus showExport (app.mjs:402-405); the lamp is fed from a journaled sync state once one exists (`H_RISK_REGISTER.md`, R-07; F/J) and until then from the last put result held in app state, never a fresh poll. |
| **WorkPackagePicker** | WCM:56-58 | Github.list of push/ plus manifestSummary (github.mjs:33,80; app.mjs:186-192); app.state.picker, pickerError, pickerAt (screens.mjs:89) | loaded / loading / refresh failed with the prior list retained / empty or no match / selected | 56 px rows: human title, type and status lead; repo path and number in 13 px mono second (WCM:58); a listing failure is a --bad banner above a still-usable prior list, and its 'Try again' is allowed (D2.3.6). |
| **MaintenanceAction** | WCM:124-126; SSC:379-386 | CaptureCache delete / clear / deleteSnapshot / clearSnapshots (captures.mjs); journal.remove, which refuses SENT (journal.mjs:277-283); writeGh | six distinct classes: invalidate one cache entry / clear read cache / delete snapshot / delete all snapshots / delete finished jobs / forget credential | each is its own destructive-local button (--bad outline, 6 px; ActionButton row) with its own sentence; never one generic Danger control (SSC:386). Classes R1 to R3 per IRM:178-179,184-185. window.confirm stays for these (app.mjs:172-175) until ConsequenceConfirmation covers them. |
| **PreflightSummary** | WCM:60-62 | runner plan, manifest problems and warnings, blocked paths, missing images (screens.mjs:118-134,151) | read-only / full capture / live write / blocked | sits directly under the ModeBand and above the item list; human summary first, technical detail under <details>. |
| **OperationCounts** | WCM:64-66 | plan item ops (create / update), manifest captures before and after, persist:'full' count, image slots | counts present / counts unavailable (omit, never fabricate) | rendered as the ModeBand chips (construction under D2.2 operation modes); 'publishes' and 'deletes' appear only when a source supports them (WCM:66). |
| **ValidationSummary** | WCM:68-70 | manifest.problems and manifest.warnings, app.blockedPaths, missingImgs (screens.mjs:126-134,151) | no issues / blockers ('Cannot run') / advisories only ('Check recommended') / both / auth blocker / missing image blocker | blockers in the bad Banner construction with ✕ and the primary disabled with the reason; advisories in the warn construction with △, never identical to blockers (CPY:415-425); each issue links to its item row. |
| **DependencyInput** | WCM:72-74 | image refs in the plan; upload ceilings (upload.mjs); picker state | missing (blocks) / picked / over ceiling | slot name and the reason it is required lead; 'picked' / 'missing' are neutral tags, replacing today's VERIFIED / FAILED pill reuse (screens.mjs:146); a ceiling error is --bad text on the row. |
| **PublishControl** | WCM:120-122; WCM:615-617 | none today: no publish or unhide recipe exists (`A_ARCHITECTURE_MAP.md`) | HOLD | the publish-primary ink construction (ActionButton row) is reserved; the control is never rendered enabled from visual readiness alone; a placeholder until the section E feasibility audit and K-03 to K-12. |
| **AdminReviewCard** | WCM:112-114; WCM:619-621 | none today: no approval field or backing store (K-09) | HOLD | placeholder card only; no invented approval state. |

### D2.3.2 RecoveryDecision construction (orphan card)

Meaning and grammar are SSC:165-175 and SSC:354-375; phone ergonomics are MOB:205-231; anatomy is WFA:328-353. Construction:

- above the fold, in this order: what is uncertain, whether a request may have left, what reconciliation found, that an ordinary retry is unsafe, the recommended next safe action (MOB:207-213).
- one candidate per 56 px row: name first (16 px ivory), then the id in 13 px mono, copyable (MOB:219-221; WFA:334-339). Today the id renders above the name (screens.mjs:57); the order is reversed.
- no candidate is preselected (SSC:175, SSC:360; WFA:341; MOB:223). Adopt is a --warn-outlined ink button on the row; its confirmation names the record and the continuation (SSC:359; CPY:196-197).
- Adopt, Skip and Re-send live in three separate regions with at least 16 px between regions, never packed in one row (MOB:227; MOB:116; SSC:174). The paste-an-id path is visually secondary to server candidates (WFA:345).
- Re-send: the exceptional construction (radius 0, 2 px --bad border, --bad text), last on the card, label naming the phase and the target entity, its own confirmation (SSC:366-369; MOB:231; WFA:349). Today it is a plain default button in its own row (screens.mjs:66).
- Skip: neutral button; label and confirmation repeat that nothing is deleted and a live row may remain (SSC:373; MOB:229; WFA:353; today's text at screens.mjs:68); never success or approved styling (SSC:374).

### D2.3.3 Phone chrome stack (BottomNav, sticky action bar, toasts)

Today the toast is fixed at bottom:12px (styles.mjs:55) over 80 px of main bottom padding (styles.mjs:29); there is no bottom nav and no sticky action bar. Rule for the new shell, bottom-up: BottomNav (56 px plus env(safe-area-inset-bottom)) under a sticky action bar (64 px, one dominant primary; MOB:115) under the risk-toast region, which never overlaps either; main bottom padding equals the height of the chrome present so the last row scrolls clear. A toast never intersects the bounding box of a Banner, halt card or orphan card (MOB:113; MOB:377; SSC:481); if it would, it docks under the ModeBand instead. Warn and bad toasts are an echo only, never the sole carrier of SENT, auth refusal, INCOMPLETE, orphan or persistence failure (WFA:496-505). The sticky bar hides while an input has focus if it would cover the field or the consequence text (MOB:117; MOB:378). Layout test: computed bounding boxes at 390 px for every toast and callout pair. D2.10 keeps the nav during a run, so chrome totals about 164 px on 390 x 844.

### D2.3.4 BUDGET TRIPPED rule (ReadinessCard, ActiveWorkCard, run screen)

While Budget.status().tripped is set (bucket.mjs:216), Resume, Reconcile & resume and Re-read are disabled with the reason as a caption: 'Paused · rate limit' and 'Try again after m:ss' where the countdown is trustworthy (CPY:402-404), naming the limited path (IRM:312). This mirrors runner.mjs:187-189, which re-pauses a resumed job with TOO_MANY_REQUESTS immediately. The countdown updates as text only; the disabled Resume never pulses or animates (IRM:317); the tripped BudgetMeter is hoisted into the pause card so the limit is visible before the next action (SSC:331). Source-verified for the runner fact; binding per the cited contracts.

### D2.3.5 SystemHealth rows render only when wired

A health domain renders only when its data source exists in state Forge already holds: SESSION from AuthState.describe() (auth.mjs:219); BUDGET from Budget.status() (bucket.mjs:204-216); REPO from readGh(storage) (app.mjs:400) and the last listing result (pickerAt, pickerError); STORAGE from app.state.persisted (app.mjs:408-410) and journal.broken (journal.mjs:221-228); RELEASE from the version and pin the shell already shows. Never 'Operational' by default (WFA:411-419). The board's Online / Operational / Degraded / Outage / Offline / Maintenance / Rate Limited / Unknown family (SBI:244-251) is illustrative (RCM:103): only Rate Limited and Unknown map to state Forge holds; none may imply a live poll (`H_RISK_REGISTER.md`, R-16). Contract test: a domain row exists only when its source is wired.

### D2.3.6 'Try again' only for retry-safe classes

A control labelled Try again is permitted only where nothing was sent and the failure is retry-safe: a transport failure before a send (the runner pauses with reason NETWORK, runner.mjs:226,286,369; client.mjs:3 notes a thrown transport error is NETWORK and is treated as AMBIGUOUS once a send left), a GitHub listing or repository request (the Studio's 'Repository request failed', 824c4d58:forge/src/studio/ui.mjs:384, is GitHub-only; 'Refresh build status' re-reads without resubmitting, 824c4d58:forge/src/studio/ui.mjs:385), or a local cache open. classifyError (outcome.mjs:58-73) marks RATE_LIMITED and CONTRACT never-retry and marks nothing retry-safe on its own, so the allow-list is by situation, not by class name. Never on an item in SENT, CONFIRMED or ORPHANED (SSC:130; SSC:510; CPY:576-578). D2.4 'no control anywhere labelled Retry' on a SENT item stands; the board's generic 'Something Went Wrong' plus Try Again (RCM:105-106) is restricted to this list.

### D2.3.7 UI strings come from the CPY label dictionary

Every state word, banner lead and button label is one constant per ITEM_STATES, JOB_STATES, pause.reason, verify and AUTH value, taken from CPY; a test checks the dictionary against the journal constants and lints the reserved words (CPY:560-583: Verified, Published, Live, Safe, Retry, Complete). Renames this forces on today's strings: 'TNR session active' (app.mjs:137) becomes 'TNR session ready' (CPY:363); 'Finished UNVERIFIED' (screens.mjs:203) becomes 'Finished unverified' (CPY:274). Kept as they are: 'Reconcile & resume' (CPY:138,246; screens.mjs:225), 'Re-read unverified items' (CPY:247; screens.mjs:225), 'Pause after this item' (IRM:190; screens.mjs:226), 'Skip (leave as is)' with 'Nothing is deleted; the server row (if any) stays.' (screens.mjs:68; wording rule SSC:373, IRM:195). The pill words in D2.2 are the compact form; the CPY primary labels are the row and banner form.

## D2.4 State and motion rules (construction; meaning and wording are owned elsewhere)

What is binding here is construction: geometry, border, fill, glyph, motion and the rule that no state is carried by colour alone. Meaning is owned by the safety-state contract, wording by the copy contract, and glyphs by the icon contract, each cited per rule below. Strings quoted in this section are examples of the pattern, not final copy: any label that names a mode or the publish act is settled by K-12, K-20 and K-21, and the label dictionary is where the final words will live.


Meaning is owned by SSC sections 3 to 11 (SSC:107-415, states and cue stack), CPY sections 5 to 11 (CPY:110-411, labels) and ICN sections 3 to 4 (ICN:46-177, glyph metaphors); this section specifies construction only and restates none of their rules. Where a line below names a state, the definition is the contract's; where it names a rule, the rule is cited, not copied (CLAUDE.md section 7).

### principle

Motion never carries state. Anything that animates is either a spatial transition between two already-rendered states or the single running indicator. State text, pills, bands, banners, lamps and counts appear at their final value on the same frame as the DOM update (amendment section 9-10; brief section 6 and 11).

### animates

| what | how | duration | note |
|---|---|---|---|
| press feedback | neutral buttons scale(.98); ink buttons translate 2px 2px with the shadow 5 -> 3 px | 90 ms ease-out |  |
| hover/focus colour and box-shadow (lane glow, --mut-glow on a focused/pressed crimson button) |  | 150 ms ease | appears on :focus-visible and :active, never hover-only |
| screen swap | the new screen is in the DOM at its final state at t=0; only the LIST BODY fades opacity 0 -> 1; the mode band, verdict banner, session lamp, halt and orphan cards are excluded and are at opacity 1 from the first frame; the old screen is removed synchronously; nothing ever fades OUT | <= 120 ms ease-out (judges G4/G14; visual-c's 180 ms whole-root fade is withdrawn) |  |
| details expand (Technical group, drift list, raw JSON) | grid-template-rows 0fr -> 1fr / opacity; content is in the DOM and focusable from t=0; the summary word changes instantly | 200 ms ease-out |  |
| progress fill width | transition on width, forward only, on a track patched in place with stable keys; the numeric fraction updates instantly | 300 ms linear |  |
| ember sheen | 1.6 s linear infinite translateX of a 40 %-wide gradient across the RUNNING progress cell only; element exists only while app.state.running === jobId; removed synchronously on PAUSED/DONE/INCOMPLETE/ABORTED; paused while document.hidden or any confirmation sheet is open |  | the only looping motion in the app |
| toast enter | translateY 8 px -> 0 + opacity; content final on first paint; toasts never animate out | 120 ms |  |
| confirmation sheet enter | backdrop and sheet appear at full opacity; optional 120 ms translateY on the sheet only; its text and record list are static |  |  |
| verified settle | one-time 150 ms scale 0.96 -> 1 on the VERIFIED outcome LAMP's container when the outcome becomes success (the pill itself is swapped, not animated); no confetti, no glow, no repeat |  | ICON_MOTION_SEMANTICS section 11 allows a short one-time settle |

### never animates

- state pills (any state, any transition): swapped, never faded, pulsed, colour-transitioned or resized
- verdict banners and outcome lamps (Verified / Finished UNVERIFIED / Finished with failures / Read-only capture complete\|incomplete)
- the operation-mode band: its colour, label, height or counts
- the session lamp and the auth banner; the authorization-denied line on an action
- halt cards, orphan cards and their buttons; the SENT banner; the DECIDE tab
- pause-reason chip, 429 countdown, budget numbers, count lines (text replacement only; no count-up)
- the top-bar underline and the nav dots/badges
- a risk button's disabled -> enabled change ('a button that fades in arrives late')
- anything fading OUT: a risk state is removed the instant the state changes
- confirmation sheet text, record lists and the backdrop's opacity after the first frame
- data tables and list rows (no highlight sweeps, no shimmer); the manifest picker skeleton is static after two cycles
- background/hero atmosphere (static gradients; no drift, particles, aurora, breathing glow)

### reduced motion

@media (prefers-reduced-motion: reduce) scoped under .f-app: every transition-duration and animation-duration -> 0.01 ms; the ember sheen is replaced by a static 2 px --acc rule at the running cell's leading edge and the word RUNNING already carries the state; progress width still updates without transition; details open instantly; the 600 ms confirm arming delay is kept (it delays an action, not state). Because Firefox Android forwarding the OS setting through a userscript overlay is unverified, Settings also has a 'Reduce motion' toggle that sets .f-app.rm with identical rules (stored in localStorage behind try/catch).

### prefers contrast

@media (prefers-contrast: more) scoped under .f-app: --line -> --mute, row rules 3 px -> 6 px, 1 px --ink border on every pill, --edge -> --edge2 (judges G11). The .f-daylight Settings variant applies the same plus --mute #c5ccd8 / --dim #a3afc1 for outdoor use; prefers-color-scheme is deliberately ignored (the overlay must not flip to light because the OS did).

### no colour only states

Every state = colour + glyph + word + construction (fill / outline / hatch / inverted; dotted / dashed / solid; 1 px / 2 px) + a row rule whose LINE STYLE differs. Every mode = glyph + word + fill-vs-hatch + rules. Every production control = geometry (square vs rounded) + offset shadow + a verb-and-count label. Pairs that collapse in hue (warn/pub, ok/acc, sent/lane-violet, bad/mut) stay distinct by construction and word; the weakest pair in visual-c (PAUSED vs PUBLISHED, both 1 px outlines at 1.27:1) is opened by the caution-hue shift (1.54:1 luminance, orange vs yellow) AND by giving PUBLISHED the ◆ glyph vs ‖.

### icon shape label redundancy

- **glyph_policy**: Unicode text nodes in a fixed 16 px aria-hidden box, only from codepoints with no emoji presentation (Geometric Shapes U+25A0-25FF, Arrows, Mathematical Operators, ✓ U+2713, ✕ U+2715, ‖ U+2016, ✎ U+270E, ⊘ U+2298, ⊠ U+22A0). Rejected: ⚑ U+2691, ⚠ U+26A0, ⚙ U+2699, ⛩ U+26E9, ⚔ U+2694, ▶ U+25B6, ✔ U+2714, ✏ U+270F, ☺ (all emoji-capable on Android; a colour-emoji flag on the ORPHANED pill would break the 'no lane tint on a pill' rule). Lane glyphs are decorative inline SVG (createElementNS, <= 400 bytes each, aria-hidden) so they may be expressive without touching the state vocabulary. If the user's smoke shows tofu for any state glyph, A's createElementNS SVG path set is the fallback; the word and construction stand alone meanwhile.
- **layer_separation**: operation context (band glyphs ◎ ↯ ◆ ↻) vs outcome/state (pill glyphs ○ ? ◐ ✓ ✕ ! ⇥ ‖ ◔ ▸ ■ ⊠) vs content identity (lane SVGs) never share a glyph (ICON_MOTION_SEMANTICS section 2); the only glyph used twice is ◆ for PUBLISH (solid) and PUBLISHED (outline), which is the intended action/state pairing
- **aria**: pills are spans whose text IS the state word (no aria-label needed for the word; the phone caption carries the qualifier); the mode band is <header aria-live=polite>; verdict banner role=alert on appearance; halt/orphan cards role=alert; the count line aria-live=polite; progress role=progressbar; buttons say what they do ('Start job → writes 5 records', 'Reconcile & resume · reads first, never re-sends', 'Publish 1 record → player-visible')

### risk states more obvious than today

Construction per state; the required cue stack is SSC:388-402 and the colour rules are SSC:404-415.

- **today**: one blue .f-primary for 'Run captures' and 'Start job' (styles.mjs:33, screens.mjs:151-156) differing only in window.confirm prose (app.mjs:172-175); SENT and CONFIRMED are hue-only outline pills (styles.mjs:43); ORPHANED/PAUSED/INCOMPLETE share --warn (styles.mjs:45); DONE is painted green regardless of outcome (styles.mjs:44); open jobs are a generic warn banner whose Resume is the same blue primary (screens.mjs:18-26); disabled = opacity .45 (styles.mjs:32, 4.01:1); bad toasts vanish after 9 s (app.mjs:100); publish does not exist (`A_ARCHITECTURE_MAP.md`); no 'authenticated but unauthorized' state exists
- **live_mutation**: 44 px pinned crimson band with ivory-outlined counts + the only crimson-filled control (square, 2 px ivory border, offset shadow, verb-and-count label) + a 3 px crimson underline on the top bar of EVERY screen while the job runs + a confirmation sheet restating counts and the READY lamp. Read-only gets a blue band, a rounded blue button and the words 'zero mutations'.
- **publish**: gold band, seal card with double rule, the only gold-filled control, 'PUBLISH SENT · UNCONFIRMED' until read-back, the gold underline while in flight, and an admin list row rendered in the gold-outline construction (never a plain chevron row).
- **ambiguous_SENT**: the only dashed + hatched + question-glyph pill, a caption that says 'never re-sent', a dashed row rule, a hatched SENT banner under the RECOVERY band, the only primary on the screen an amber-outlined square 'Reconcile & resume', a --sent dot on the shell's Jobs destination from every screen, and no control anywhere labelled Retry.
- **paused_orphaned**: RECOVERY hatch band + reason chip with distinct glyphs per reason + halt card with the reason as the headline + the inverted ivory ORPHANED pill + orphan card with DECIDE tab + orphan count badge on the shell; SESSION pauses keep Resume disabled with the reason (app.mjs:159-163).
- **auth**: four lamp states with distinct glyph + word (READY ✓, CHECKING …, UNCONFIRMED ?, SIGNED OUT ✕ filled; auth.mjs:54) with authorization denial rendered on the action rather than the session (pre-emptive disabled state from the role pre-check; the string-matched label only if K-34 admits it, E.3); READ FAILED lives on the item, never on the lamp.

### stylesheet contract test

A socket-free test parses the CSS text and asserts: (1) every selector is scoped under .f-host/.f-app/.f-boot; (2) animation/transition appear only on the allow-listed selectors; (3) --mut, --pub, --ok, --orph-fill appear as background only on allow-listed selectors (band, ink buttons, seal, VERIFIED pill, ORPHANED pill); (4) no lane token is referenced outside .f-lane; (5) the sheet contains no url( and no @font-face; (6) the contrast table is recomputed from the TOKENS string with the same formula as contrast_synth.py and fails under 4.5:1 for text pairs and 3:1 for boundary pairs, including the two pairs visual-c missed (count chips vs band; disabled text). This is the same build-gate mechanism forge/build.mjs already uses for innerHTML.

## D2.5 Departures from the approved mockup (each with the smallest correction)

- **1. Quick action 'New Content' is a crimson card** Evidence: amendment section 9 (read-only must look materially safer than live-write); mockup (300..580,245..318) sampled #cd1c24 Smallest correction: authoring/manifest tiles use the neutral raised tile with a blue glyph; crimson fill appears only on the control that actually sends a write Decision: D-VC-1 / judges U6, UD-4 (illustrative per amendment section 12; keep crimson only if 'New Content' truly opens a live-write flow)
- **2. Quick action 'Validate Content' is a green card** Evidence: amendment section 3 (green reserved for success) Smallest correction: neutral tile; validation's verdict is green/coral TEXT after it runs; green is never a button Decision: D-VC-2 / U6 (illustrative)
- **3. Illustrated hero (moon, pagoda) and full-bleed painted lane art** Evidence: self-contained bundle non-negotiable; the reference JPEG is 249 KB vs 59.5 KB for the whole UI layer (`A_ARCHITECTURE_MAP.md`); H_RISK_REGISTER R-06; text over raster cannot be contrast-guaranteed Smallest correction: CSS-drawn atmosphere (layered radial gradients: crimson ember 8 % bottom-left, cool blue 6 % top-right) + <= 3 KB inline SVG silhouette at 10 % alpha in the hero; lane cards get gradient wash + one <= 400-byte SVG glyph; any text over art sits on a solid 88 % --bg scrim (11.94:1). An opt-in repo-committed data-URI 'Rich art' pack, off by default on phone, is a later separately budgeted decision Decision: D-VC-3 / U3, UD-3: the CHARACTER (dark atmospheric console) survives; the PAINTED look does not in v1 - the director must confirm this reading or fund the art pack
- **4. Content Admin 'Publish / Unpublish' is a plain list row identical to 'Preview Content'** Evidence: amendment section 7 (publish must not become an accidental tap) and section 9 Smallest correction: row rendered in the gold-outline construction with ◆ and the pending count, leading to the seal card + PUBLISH band + armed confirmation sheet; never one-tap from the list Decision: K-12 / D-VC-6: the confirmation LEVEL is the director's; press-and-hold is withdrawn (U1/UD-1)
- **5. System Status rows: green 6 px dot + green adjective; one 'Ready for Content Work / All systems are go' green banner** Evidence: amendment section 9 (auth unavailable, denied and transport failure stay separate); safety contract section 6; R-16 (status must not imply a live poll) Smallest correction: three lamps with glyph + word + specific state; computed headline; green banner only when every lamp is ✓; fed from state Forge already holds Decision: none (non-negotiable)
- **6. Recent Activity rows use free green/blue/grey dots** Evidence: colour-only; dots do not map to lifecycle states Smallest correction: rows show the real job/record pill (VERIFIED / INCOMPLETE / HIDDEN / PUBLISHED …) Decision: none
- **7. Brushed display lettering for 'TNR FORGE'** Evidence: no web font or raster may be fetched; a raster wordmark cannot scale Smallest correction: system-font wordmark with crimson hard offset (A) or embedded createElementNS vector path (B) Decision: D-VC-4 / U4: recommend A
- **8. Pure white text and 999 px pills** Evidence: amendment section 3 prefers ivory; white glares on AMOLED; dashed borders render poorly on a full radius Smallest correction: --ink #f3efe6 / --ink2 #fffaf0; pills at 3 px radius (not 0: hard edge is reserved for production controls, judges G9) Decision: none (illustrative)
- **9. Violet on both 'Create Manifest' and the Characters lane; blue on both 'Capture from Live' and the Items lane** Evidence: a lane tint on a button makes the tint look like a semantic Smallest correction: lane tints confined to .f-lane; actions coloured by consequence only (neutral / blue / crimson / gold) Decision: none
- **10. ~12 px muted sub-labels on saturated card fills** Evidence: perceived ~#c9a9ae on #3f1b24 (~5:1) at 12 px is marginal in daylight Smallest correction: sub-labels 13 px --mute on --paper/--raised tiles (8.19:1); no small text on saturated fills Decision: none
- **11. No operation-mode header is drawn in the mockup** Evidence: amendment section 8 requires it Smallest correction: the 44 px mode band above every actionable flow Decision: none; taxonomy of a fifth REVIEW mode is K-21
- **12. Sidebar active item = crimson-tinted fill with a red edge (sampled #dd1124 at (8..14,208..250))** Evidence: a crimson-tinted nav fill weakens 'crimson block = LIVE WRITE' Smallest correction: active rail row = --raised fill with a 3 px --mut-edge left marker (crimson as a <= 4 px accent only) Decision: none
- **13. Hard-edged quick-action tiles (visual-c's own elaboration, not the mockup)** Evidence: judges G9: hard edge signals nothing if applied to tiles, chips and pills alike Smallest correction: square + offset shadow only on the three production ink buttons and the exceptional Re-send; tiles 8 px, pills 3 px Decision: none
- **14. Solid gold pending-review badge (visual-c) beside the rule 'gold fill only for PUBLISH'** Evidence: legibility judge flaw (6): internal inconsistency Smallest correction: the badge is a gold OUTLINE with a --pub-text numeral (10.69:1 on paper) Decision: none
- **15. Style board Success / Warning button variants** Evidence: green is a verdict, never a button; amber buttons would collide with the Reconcile construction (DESIGN_RECONCILIATION_MATRIX row 'Success/Warning action buttons': OPEN BY CONTRACT) Smallest correction: not adopted; the only coloured buttons are read-blue, write-crimson, publish-gold, reconcile-amber-outline, re-send/destructive coral-outline Decision: K-23 (pending transcript); recommendation is to drop them
- **16. Style board generic 'Something Went Wrong → Try Again' error state** Evidence: safety contract section 16: no generic Retry on an ambiguous write; `A_ARCHITECTURE_MAP.md` (SENT → PLANNED is structurally impossible) Smallest correction: 'Try again' exists only for retry-safe classes (a GitHub listing, a cache open); mutation failures render the halt/orphan card Decision: none (non-negotiable)
- **17. Style board five-tile mode SELECTOR** Evidence: reconciliation matrix: mode must be derived from the plan/journal/action, never chosen; choosing a colour must not look like acquiring authority Smallest correction: the band is display-only; there is no mode selector Decision: K-33 (open sub-decision of K-21: mode selectable by the user vs derived from the work package and capability); the recommendation here is derived, and the band stays display-only unless the director rules otherwise

## D2.6 Implementation sequence for the visual shell

- S1 (visual only, class names preserved): tokens on .f-host/.f-app, typography, pill() -> STATE table with glyph box, ModeBand, session lamp with four states (a fifth only under the D2.2 session_lamp condition), banners by construction, the four button lanes, disabled-without-opacity, prefers-reduced-motion + prefers-contrast + Daylight blocks, the contrast/allow-list contract test. Runs on the existing five screens; forge/test/ui.test.mjs selectors keep working.
- S2 (interaction): SegmentedProgress patched in place, halt/orphan cards, top-bar underline, sticky action bar, persistent risk toasts, the confirmation sheet for LIVE WRITE and RE-SEND (window.confirm kept for local-destructive actions), outcome lamp beside DONE.
- S3 (shell): rail / bottom nav / More surface, Command Center cards fed only from state Forge already holds, lane cards with CSS atmosphere, wordmark option A, Settings toggles (Reduce motion, Daylight).
- S4 (admin, after K-03/K-05/K-12): content pills, DiffView, PreviewFrame, the gold-outline admin rows, the publish seal + PUBLISH band + armed sheet, authorization handling as the pre-emptive per-action disabled state E.3 supports, with the string-matched label only if K-34 admits it.
- S5 (Studio absorption, after seam integration and the CF-22 ownership ruling): the Quest Studio shell moves onto this token set and ConfirmationSurface (D2.2 'Studio shell colours'); until then it keeps its own stylesheet and is not restyled from this branch (one writer per branch, CLAUDE.md section 4).
- Each slice leaves Forge usable, is reviewable on its own SHA, and none touches runner/storage/transport (amendment section 13.6).

## D2.7 Cost and unverified items

~16-20 KB unminified CSS (~5 KB gzip) in one sheet: ~75 tokens, ~160 rules, 3 media queries (768, 1024/1280, reduced-motion) + prefers-contrast, 1 keyframes (sheen), 4 hatch gradients, ~12 elevation/glow declarations; ~3 KB of createElementNS atmosphere/lane glyphs; ~350 lines of JS for pill/band/lamp/progress/sheet/shell. Total UI delta ~+18 KB on a 398 KB bundle (`A_ARCHITECTURE_MAP.md`), under 5 %; no dependency; no asset.

Firefox Android glyph coverage for the chosen Unicode blocks, adoptedStyleSheets support, and whether the OS reduced-motion/contrast preferences reach a userscript overlay are Inferred, not verified; every fallback (insertRule path in dom.mjs, manual toggles, word + construction carrying state without the glyph) is designed so nothing state-bearing depends on them. No browser, live or session check was performed.

## D2.8 Ideas grafted from the superseded explorations

- G-A1 geometry as a redundant risk channel: square + offset shadow only on Start-live-write, Publish, Reconcile & resume and the exceptional Re-send; pills 3 px; tiles 8 px (from A via legibility judge G9)
- G-A2 state lamp / outcome lamp split: DONE is a neutral pill, jobOutcome renders beside it as VERIFIED ALL / UNVERIFIED / FAILED (from A via polish judge G9)
- G-A3 2 px ivory border on all four sides of the crimson ink button, the game's own ink construction (from A via polish judge G4)
- G-A4 'CONFIRMED · not read back' qualifier (from A via legibility judge G6)
- G-A5 authorization denial (per action, not a session state, E.3; K-34 decides the string-matched label): disabled action with the reason, and a --warn-fill line naming the action; READ FAILED on the item only (from A/B via G1/G13)
- G-A6 motion discipline: new screen in the DOM at t=0, only the list body fades, <= 120 ms, mode band / verdict / lamp / halt cards excluded; nothing fades out; a risk button's enabled change never animates (from A via G4/G14)
- G-A7 persistent warn/bad toasts that stack; ok/info at 4 s; a toast is never the sole carrier of state (from A/B via G5/G7)
- G-B1 3 px top-bar underline on every screen while a mutation job is RUNNING; gold while a publish is in flight; recovery hatch while SENT/ORPHANED exists (from B via G7/G5)
- G-B2 static shell dots and badges: --sent dot for any SENT item, --warn dot for PAUSED, orphan count, gold-OUTLINE pending-review count (from B via G8)
- G-B3 ORPHANED as the one inverted-polarity pill, ivory fill, dark text, '!' glyph (from B via polish judge G3)
- G-B4 16 px/1.5 phone body, 13 px floor, 12 px only for 700-weight uppercase pill words and h3 (from B via G13/G1; pending K-23)
- G-B5 fixed 16 px aria-hidden glyph box; emoji-presentation codepoints replaced (from B via G12/G2)
- G-B6 two-step armed confirmation sheet, Confirm disabled ~600 ms, far from the trigger, Cancel/Escape only, never press-and-hold (from B via G10; level stays K-12)
- G-B7 @media (prefers-contrast: more) block (from B via G11)
- G-B8 disabled controls at 100 % opacity: --mute on --raised, --edge border, reason caption (from A/B via G2/G12)
- G-B9 qualifier moves to a 13 px caption on phone, stays in the pill on desktop (from B via polish judge G15)
- G-C1 (own correction, judge-identified fails) count chips on every mode band are OUTLINED in the band's text colour with no fill: 5.71 / 5.62 / 6.47 / 10.00 replace the 2.61 (crimson) and 1.10 (recovery) raised-chip boundaries
- G-C2 (own correction) progress track, sheen and mode band patched in place with stable keys so the 1.5 s replace() tick cannot restart transitions; the sheen element is bound to app.state.running and jsdom-tested for removal (from A/B via G3/G6)
- G-C3 (own correction) caution hue shifted to #f08a3c and the RECOVERY stripe darkened to #3f2610 (D-VC-7 / U2 / UD-2; pending director)
- G-C4 (own correction) the pending-review badge is a gold outline, not a solid, so 'solid gold = PUBLISH' has no exception (legibility judge flaw 6)

## D2.9 Superseded explorations (reference only)

**visual-a 'Instrument Panel' (superseded, reference only).** A dense, dark-first TNR console over layered navy with warm ivory ink where every lifecycle state is a labelled lamp (glyph + text + hollow/filled) and the three things that can touch production each own one hue AND one construction nothing else may use: a crimson ink button for LIVE WRITE, a parchment ink button (the game's own .tnr-ink-btn-primary re-tokenised) for PUBLISH, and a dashed-violet square for Reconcile. It shipped a full opt-in light theme (87 pairs per theme, all AA), ~18 createElementNS SVG glyphs, a custom confirm sheet and a segmented item track with phase dots. The legibility judge scored it highest (34) because it was built for that lens; both judges read it as austere against the 'atmospheric, premium' character the director approved (gold demoted to hollow admin cues, blue active-nav marker, no lane atmosphere) and the most expensive to build (two themes, SVG set, sheet).

Superseded by the director's ruling at chatgpt/forge-next-planning@0bb5a54b, not by a panel vote. Grafted into the synthesis: geometry as a redundant risk channel (square only for production controls); the state-lamp / outcome-lamp split so DONE is never green on its own; the four-sided 2 px ink border on the crimson button (fixes the 2.92:1 fill-vs-paper edge); the 'CONFIRMED · not read back' qualifier; the NOT AUTHORIZED session state; 'nothing fades out' and 'a risk button's enabled change never animates'; persistent warn/bad toasts; the fixed-width glyph box and SVG-path fallback; disabled controls at full opacity. Not grafted: the parchment publish surface (the amendment names gold as the admin/publish accent), the light theme (doubles the audit surface; the Daylight dark variant covers outdoor use), the 14 px desktop body, the strikethrough SKIPPED label.

**visual-b 'Workbench' (superseded, reference only).** A calm, card-based operations bench on the approved deep-navy ground where the only saturated colour on a screen is the authority lane you stand in (cool blue to read, crimson #d92a48 to write, gold to publish), every risk state is a word + glyph + fill style, motion is spent only on transitions and progress, and an opt-in Daylight light scheme keeps the same lane semantics for phone use outdoors (205 pairs checked, 0 failures, one mitigated gap: gold on white 2.11:1). It had the most rigorous legibility engineering: 16 px/1.5 body with a 13 px floor, a fixed 16 px glyph box, ORPHANED as the only inverted-polarity pill, a 3 px crimson top-bar underline on every screen while a write runs, static recovery dots on the bottom nav, persistent risk toasts, a prefers-contrast block and honest costing of in-place progress patching and the confirm-sheet interaction change. Judges read its muted teal/steel/sand/moss lanes, 999 px pills and 10-12 px radii as a deliberate step away from the approved ink-edged, atmospheric character, and its white-on-crimson band (4.80:1) as the thinnest margin in the panel.

Superseded by the same ruling. Grafted into the synthesis: the top-bar underline while a mutation job is RUNNING (extended to gold for publish and the recovery hatch for SENT/ORPHANED); static shell dots and badges so an orphan or SENT item is visible from every screen; the inverted ivory ORPHANED pill; the 16 px/1.5 phone body and 13 px floor (recommended default, pending K-23); the fixed glyph box; the two-step armed confirmation (Confirm disabled ~600 ms, far from the trigger, never press-and-hold); the prefers-contrast block; ok/info toasts at 4 s and warn/bad persisting; disabled = --mute on a raised fill at 100 % opacity; the qualifier-as-caption on phone. Not grafted: the light Daylight scheme (same reason as A), the 1.4 s picker shimmer loop (capped at two cycles), the violet Reconcile fill (Reconcile is amber-outlined here so violet stays SENT-only), the two stacked sticky bottom bars (120-128 px of a phone viewport).

## D2.10 Decisions this section surfaces

Each is registered in `K_USER_DECISIONS.md`: the visual ones are K-01, K-14, K-21, K-22, K-23, K-31, K-32, K-33, K-34, K-56, K-57 and K-58; the process ones are noted in the roadmap. Nothing here is settled by this file.

- **Token acceptance: adopt the synthesized token set (visual-c corrected by the judges' grafts) as the phase-2 design-freeze baseline, with the rows marked PENDING held open for transcript reconciliation (K-22 exact mode colours/hex; K-21 whether REVIEW is a mode; K-23 typography scale)** Options: accept the recommended defaults now and let transcript reconciliation only overturn PENDING rows; hold every hex until the transcript is reconciled; accept the character and defer all hex to implementation (not recommended: the contrast gate needs concrete values) Consequence: option 1 lets phase 0-1 proceed shell-independent and gives the stylesheet contract test concrete values; option 2 blocks the wireframe style tile; option 3 pushes AA verification to the implementer Recommendation: option 1 Can defer: True. Blocks: Phase 2 design freeze (K-01/K-22)
- **Caution-hue shift: --warn/--rec from visual-c's #f5a25a to #f08a3c (more orange) so caution and publish gold no longer share a hue; RECOVERY stripe darkened to #3f2610 to keep >= 5:1 on the band word** Options: adopt #f08a3c now (recommended; 6.94:1 paper, 6.16:1 warn-fill, 5.62:1 on the stripe, 1.54:1 from PUBLISHED text vs 1.27:1 before); keep #f5a25a and rely on construction + word alone; shift gold instead (rejected: gold is the approved admin/publish family and is sampled from the mockup badge) Consequence: the shift touches the approved accent family, so it is the director's even though every pair passes AA either way; PAUSED vs PUBLISHED remains the weakest colour-blind pair and is also opened by glyph (‖ vs ◆) and word Recommendation: adopt #f08a3c Can defer: True. Blocks: nothing before phase 2
- **Brand treatment: wordmark option A (system-font 'FORGE' 900 with crimson hard offset and slash, zero bytes) vs option B (embedded createElementNS vector path, ~1.5 KB, needs an art check that it carries no proprietary identity)** Options: A; B; A now, B later behind the same slot Consequence: A is buildable in the first shell slice and cannot fetch anything; B keeps the mockup's brushed silhouette at the cost of a designer pass and a director check Recommendation: A now; B as a later art decision Can defer: True. Blocks: nothing
- **Background art: CSS-drawn atmosphere + <= 3 KB inline SVG in v1 instead of the mockup's painted hero and lane illustrations; optional opt-in repo-committed data-URI 'Rich art' pack (off by default on phone) later** Options: CSS atmosphere only in v1 (recommended); CSS atmosphere now + fund an art pack behind a Settings toggle with a byte budget (R-06); embed the mockup art as data URIs (rejected: 249 KB parsed on every game page) Consequence: this is the one VISIBLE departure from the approved image; the character (dark, atmospheric, layered) survives, the painted look does not; the director must confirm the character survives without raster or fund the pack Recommendation: option 1, with option 2 recorded as a later decision Can defer: False. Blocks: Phase 2 Command Center (the hero region's height and content)
- **Publish confirmation construction: two-step armed sheet (restates record names, current HIDDEN pill, session READY; Confirm disabled ~600 ms, far from the trigger; Cancel/Escape only) replacing visual-c's press-and-hold option; the confirmation LEVEL (plain armed tap vs typed record count) stays K-12** Options: armed sheet, plain second tap; armed sheet + typed record count; armed sheet + typed record name Consequence: press-and-hold is withdrawn as an accessibility risk (timing-dependent, switch access, wet thumb in sun); the level trades taps for evidence and is the director's per brief section 14 Recommendation: armed sheet with a plain second tap for single-record publish; typed count once package publish exists (K-07) Can defer: False. Blocks: Phase 5 publish flow (K-12)
- **Replace window.confirm (app.mjs:172-175) with the custom confirmation sheet for LIVE WRITE, PUBLISH and RE-SEND only; window.confirm stays for local-destructive actions** Options: as recommended; custom sheet for everything; keep window.confirm everywhere (rejected: it cannot show lamps, counts or record lists) Consequence: an interaction change, not a restyle: app.confirm becomes async and touches every call site in screens.mjs and the stubs in forge/test/ui.test.mjs:149,178,216; needs its own jsdom tests Recommendation: as recommended Can defer: False. Blocks: Phase 2 (write flow) and Phase 5 (publish)
- **Phone bottom nav during a run: keep it visible (recommended) vs hide it to recover 56 px (visual-c)** Options: keep the nav; the top-bar underline and nav dots stay visible during a run; hide during a run; the top-bar underline (G7) is the mandatory compensation Consequence: keeping it preserves the Admin pending badge and orphan/SENT indicators during a run at the cost of 56 px of a 390x844 viewport (chrome then totals ~164 px: top bar 56 + band 44 + action bar 64, nav 56 below) Recommendation: keep the nav Can defer: True. Blocks: Phase 2 shell
- **Operation-mode taxonomy and colours where the approved north star, design system v0.1, the colour-semantics amendment and the latest style board disagree (K-21/K-22)** Options: recommended default: READ ONLY cool blue / LIVE WRITE crimson / PUBLISH gold / RECOVERY caution-hatch, REVIEW reserved as gold outline if ruled a mode; colour-semantics amendment reference: read cyan / write copper-orange / publish magenta / recovery indigo; style board: read indigo / write cyan / review violet / publish orange / recovery teal Consequence: the recommended default is the only mapping consistent with the LATER approved north star (crimson = action, gold = admin/publish, blue = system) AND with the amendment's binding separation rule (LIVE WRITE never amber, PUBLISH never error-red, colour never sole cue); options 2 and 3 would recolour the approved mockup's action family Recommendation: option 1, marked pending until the transcript is reconciled Can defer: True. Blocks: Phase 2 design freeze
- **Typography scale (K-23): recommended 16 px/1.5 phone body with a 13 px floor (B) vs visual-c's 15 px / v0.1's 14-15 px with 11-12 px micro vs the style board's 40/28/20/16/15/13/12** Options: 16 px phone / 15 px desktop, 13 px floor (recommended); 15 px everywhere (visual-c); style board scale Consequence: ~7 % less density on phone for a measurable daylight gain; the 11-12 px micro tier and 40 px H1 are not adopted regardless Recommendation: option 1 Can defer: True. Blocks: Phase 2
- **Light theme: none in v1; a 'Daylight' high-contrast DARK variant (5 token overrides) instead** Options: Daylight dark variant only (recommended); full opt-in light theme (A and B both built one; doubles the contrast audit; risks a light overlay flashing over the game's dark layout on close) Consequence: legibility outdoors is served by the variant (--mute 10.74:1); a light theme is a separate later decision Recommendation: option 1 Can defer: True. Blocks: nothing
- **Evidence hygiene before the design freeze: regenerate scratchpad/design/contrast_c.json from the JSON's own tokens (it still carries --mut #b3202b), correct visual-c's 'ink on RECOVERY hatch >= 13:1' to the recomputed value, and add the count-chip and disabled-text pairs to the contract test** Options: do it in the phase-2 implementation brief; do it now on the planning branch Consequence: a stale evidence file beside a correct proposal is the kind of drift docs/00_INDEX.md's adoption gate exists to stop Recommendation: now (this file's contrast_synth.json is the regenerated table for the synthesized set) Can defer: True. Blocks: nothing
- **Authorization-denial lamp (K-34, proposed; CF-04 to director): whether Forge Next distinguishes a role denial from other HTTP 200 refusals** Options: authorize a pinned-source audit of the admin procedures' refusal shapes (section E) and, if a stable signal exists, add a classifyError class and an AUTH extension as a Lane A deliverable below the UI seam, then render the D2.2 lamp; or drop the lamp and keep four states Consequence: today auth.mjs:54 has four states and outcome.mjs:58-73 no authorization class; a lamp without a signal would invent capability (IDX:145) and SSC:293 asks for the distinction only where the procedure surfaces it Recommendation: audit first; render nothing until it returns Can defer: True. Blocks: Phase 4 admin surface (K-03, K-05)
- **Board 'Critical' semantic tier (K-22 sub-point)** Options: drop it (no Forge state is more severe than the --bad family); map it to TRIPPED or SIGNED OUT (rejected here: both already have a construction and a second red tier weakens 'coral text = failure') Consequence: SBI:81 and RCM:53 leave it 'to evaluate'; the board also carries no ambiguous tier, which --sent supplies Recommendation: drop; PENDING until K-22 is ruled Can defer: True. Blocks: nothing
- **Mode selectable vs derived (K-33, sub-decision of K-21)** Options: derived from the plan, journal and action (recommended; departure 17); selectable by the operator (the board's five-tile selector, SBI:257-282 per the reconciliation matrix RCM:66 'OPEN BY CONTRACT') Consequence: a selector would let a colour look like acquired authority (WCM:611-613) Recommendation: derived; the band is display-only Can defer: True. Blocks: Phase 2 shell
- **Studio shell absorption ownership (CF-22, to director)** Options: after the seam integrates, Fable owns forge/src/studio/* for the design-system absorption (single writer thereafter); or ChatGPT continues the Studio slice and applies the token set from this file Consequence: the shell is a second overlay with a hard-coded palette and a #f97316 compile control (D2.2 'Studio shell colours'); absorbing it is UI work on files the ChatGPT branch owns today, so the one-writer rule (CLAUDE.md section 4) decides who edits, not this file Recommendation: none offered here; the director assigns the writer Can defer: True. Blocks: D2.6 S5

## D2.11 Evidence and how to reproduce it

Every contrast ratio in this file comes from one computation, committed as `evidence/contrast.py`, so a reviewer can reproduce any number rather than trust it: `printf '#f3efe6 #0b121a ink on bg\n' | python3 docs/forge_next/evidence/contrast.py`. The synthesised token set, component inventory and departures are committed as `evidence/visual-synthesis.json`. Paths below that begin `scratchpad/` are session working files from the design panel; they are named for provenance and are not committed, so any claim that rests on one is marked as such rather than presented as repository evidence.


- state/prompt_forge_next_planning.md@origin/chatgpt/forge-next-planning (git show; absent on this branch's disk) §1:26-39 (modern, responsive, polished, a little flashy), §6:211-232 (mobile-first, no hover, obvious read vs mutate/publish distinction, recovery), §11:353-372 ('a little flashy' = polish; risk states more obvious than today), §14:456-470 (visual style, publishing UX and confirmation level are user-owned), §15:474-485 (friendly surface, explicit machine state; recovery is a screen)
- scratchpad/amendment/FORGE_NEXT_VISUAL_DIRECTION.md:38-46 (foundation palette), :48-62 (ink language used selectively; no heavy ornament around safety-critical actions), :64-91 (rail / bottom nav / More), :93-113 (Command Center blocks), :115-130 (lanes illustrative), :132-146 (Content Admin; publish must not become an accidental tap), :148-171 (mode header + counts), :173-188 (state rules incl. 'do not use color alone'), :190-208 (motion allowed/avoid), :210-216 (typography), :218-254 (binding vs illustrative vs must-not-infer), :256-265 (deliverables 13.3-13.5)
- scratchpad/amendment/forge_next_concept_mockup.png viewed: crimson 'New Content' and green 'Validate' quick actions, violet 'Create Manifest', painted hero and lane art, green status dots and 'Ready for Content Work' banner, gold pending badge '3', crimson-tinted active nav row, 'Publish / Unpublish' as a plain chevron row
- forge/src/ui/styles.mjs:11 (today's tokens), :19-20 (scoping on .f-host/.f-app), :26-28 (horizontal five-button nav; active = acc fill), :31-34 (44 px buttons; one .f-primary; .f-danger outline), :32 (disabled opacity .45 -> 4.01:1, fails AA), :42-45 (999 px hue-only pills; SENT vs CONFIRMED hue only; ORPHANED/PAUSED/INCOMPLETE share --warn; DONE green), :48-51 (banners; 6 px acc bar)
- forge/src/ui/screens.mjs:8 (pill = word only), :18-26 (open job = generic warn banner; Reconcile & resume is the same blue primary), :45-69 (OrphanCard; Re-send is a default button), :86,146 (VERIFIED/FAILED pill classes borrowed for 'ran'/'picked'/'missing'), :104-125 (captureLabel; read-only info banner; full-capture warn banner), :151-156 (Start job vs Run captures: identical button), :170-171 (run header + bar), :208-219 (pause banners), :229-232 (budget as text), :264,288,297,322 (local-destructive confirms)
- forge/src/ui/app.mjs:15 (five screens), :65-71 (shell slots), :84 (aria-current), :93-100 (toasts auto-remove; bad after 9 s), :132-151 (auth banner: three states named in prose; no 'authorized' distinction), :159-163 (resumeBlockedReason), :172-175 (window.confirm), :268 (1.5 s replace() tick), :293-295 (toast reports outcome), :384 (bundle exports state AND outcome), :408-410 (storage persist)
- `A_ARCHITECTURE_MAP.md` (job/item states, transitions, outcome separate from state), :141 (SENT -> PLANNED impossible), :150-152 (writes behind confirm; no publish action today; full-persist allowlist), :171-177 (bundle 397,984 B; ui 59,501 B)
- `K_USER_DECISIONS.md` (K.0 rulings), :19-46 (K-01, K-02, K-12, K-20..K-24, K-30), :50-56 (K-01 ruled; A and B kept as graft sources only)
- `H_RISK_REGISTER.md` (R-06 mobile performance bans embedded art), :25 (R-16 mockup-implied capabilities; status blocks never poll)
- docs/agents/UI_UX_REVIEWER.md:27-39 (Android/mobile; destructive/ambiguous never looks like success; recovery actions never imply a repeat is safe; no hover-only; no HTML-string sink)
- docs/00_INDEX.md:3-4 (Samsung Android, Firefox, ViolentMonkey; no staging), :100-101 (hidden:true by default; publishing is a separate step), :115 (self-contained loader/bundle release path)
- IDX:14-26 (Tier A: visual direction and colour-semantics separation rule), :46-48 (v0.1 is a proposal, not a lock), :125-141 (mode taxonomy, palette, typography deliberately unsettled), :143-147 (conflict handling: later ruling wins; never invent capability to satisfy a mockup)
- COL:11-13 (ruling: operation context vs semantic outcome must be distinct), COL:19-26 (mode families; label + icon required), COL:32-39 (reserved semantic families; violet for SENT only if distinct from PUBLISH), COL:43-48 (collision rules 1-6), COL:52-64 (reference values are not locks). The file is 68 lines at 824c4d58; earlier line numbers in this list referred to a longer draft and are withdrawn
- DS:32-78 (v0.1 token values shown side by side), :82-95 (modes), :125-139 (type scale), :161-173 (shape language), :175-201 (glow allowed/avoid), :203-225 (button hierarchy; production-action wording), :227-281 (component vocabulary), :283-297 (state groups), :355-382 (motion timing), :418-434 (unresolved)
- SBI:39-66 (board palette), :69-84 (board semantic colours), :86-119 (five-mode taxonomy incl. Review; chronology flag), :123-139 (board type scale), :219-238 (Success/Warning buttons question), :270-282 (mode selector risk), :360-370 (generic Try Again constraint), :434-445 (transcript questions)
- RCM:62-63 (Review mode and mode colour mapping: APPARENT CONFLICT), :66 (mode selector OPEN BY CONTRACT), :83 (typography BOARD ADDS DETAIL), :90 (Success/Warning buttons OPEN BY CONTRACT), :96-100 (SENT/CONFIRMED/INCOMPLETE/orphan/auth NEEDS VALIDATION), :136-149 (frozen until export), :164-178 (transcript questions)
- ICN:18-44 (three layers never share a language), :46-103 (mode metaphors; avoid checkmark for write, refresh alone for recovery), :105-176 (state metaphors; ambiguity needs its own glyph), :189-211 (shape semantics), :240-296 (motion roles; stop promptly; SENT never a spinner), :324-333 (reduced-motion contract), :335-346 (no theatrical motion for danger), :370-376 (critical states never auto-dismiss)
- SSC:22-105 (six axes), :107-185 (certainty hierarchy PLANNED..SKIPPED), :187-233 (job states; INCOMPLETE never green; DONE alone is not success), :264-295 (auth incl. authorization/role denial), :297-322 (capture persistence two questions), :336-386 (recovery action grammar), :388-402 (five-cue stack + sixth for ambiguity), :404-415 (colour rules), :417-470 (component requirements), :505-517 (anti-patterns)
- scratchpad/design/visual-c.json (start point: tokens, pills, modes, motion, departures 1-12, D-VC-1..7), visual-a.json (grafts: geometry channel, state/outcome split, four-sided ink border, CONFIRMED qualifier, NOT AUTHORIZED, motion discipline, persistent toasts), visual-b.json (grafts: top-bar underline, nav dots, inverted ORPHANED, 16 px scale, glyph box, armed confirm, prefers-contrast, no-opacity disabled)
- scratchpad/design/judge-visual-legibility-and-risk.json (contrast recheck incl. the two missed fails 2.61 and 4.01; grafts G1-G13; U1-U9), judge-visual-polish-and-coherence.json (grafts G1-G15; UD-1..6; non_negotiable_conflicts), judge_contrast_recheck.json (independent recomputation of A/B/C pairs)
- scratchpad/tnr-src-345d18ac/app/src/styles/globals.css:243-300 (.tnr-ink-btn: radius 0, 2 px border, 5px 5px 0 offset shadow, hover translate 2 px + shadow 3 px, 150 ms transitions, focus outline 2 px at 4 px offset) - the construction borrowed selectively for the production ink buttons
- scratchpad/design/synth/contrast_synth.py + contrast_synth.json (113 pairs recomputed for this synthesis; every text pair >= 4.5:1, every relied-upon boundary >= 3:1; the three FAILs printed are the two pairs deliberately shown as replaced (raised chips vs crimson band 2.61, raised chips vs recovery stripe 1.10), the crimson fill vs paper 2.92 that is mitigated by the four-sided border, and the decorative --line and slate HIDDEN fill that are exempt because their boundary is the --edge border)