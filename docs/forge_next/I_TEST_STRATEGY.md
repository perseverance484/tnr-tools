# I. Test and verification strategy

## I.0 Status and scope

**Status:** planning only. No test was written, no implementation was performed, no browser was opened, no live game request was made, and no credential or session material was read, requested or created in this pass. Every gate below is a proposal for a later implementation brief under `CLAUDE.md` §11, and every user-owned decision it touches stays open in section K.

**Scope.** This section answers brief §13-I: the unit, fixture, adversarial and UI-contract layers a much larger Forge needs, the static gates that keep the safety core and the bundle honest, the per-phase acceptance gates that section G names, and the exact browser and live smoke that will eventually require the operator's own device and the operator's own tap. It records today's suite as the measured baseline, maps each risk gate in `H_RISK_REGISTER.md` to a test family, maps each of the thirteen UI-level semantic guarantees in AUD §17 to a kept-green test, and states plainly which things no socket-free harness can prove. Planning and implementation tests stay socket-free (`CLAUDE.md` §8; the premise is already enforced by a grep at `forge/test/ui.test.mjs:331-350`). It settles nothing: it neither picks the confirmation level, nor the palette, nor the publishing UX, nor the retirement date.

**Method and inputs.** The design panel produced no proposal or synthesis file for test strategy at this SHA; its directory carries the IA, architecture, capture, queue and visual families only (Observed, by listing). Therefore: **panel synthesis unavailable at this SHA; recommendation derived by the planning owner.** The inputs that did exist and were read are `evidence/forge-tests-ci.json` (334 rows: 275 test rows, 21 gap rows, 16 harness rows, 15 totals rows, 7 CI rows), the Tier C reading `consolidated_read/ux-contracts.json` (166 requirement rows each carrying a `testable_as`, 72 scenario rows, 27 grouped checklist rows, 35 machine-state rows), `consolidated_read/baseline-and-handoff.json` (BF-09, BF-51, BF-54, CC-M3, CF-10), `consolidated_read/foundation-impl.json` (G2, M2, M6, RI6, RI8), the package sections `A_ARCHITECTURE_MAP.md`, `D_VISUAL_SYSTEM.md`, `D_IA_AND_JOURNEYS.md`, `F_ARCHITECTURE_RECOMMENDATION.md`, `G_ROADMAP.md`, `H_RISK_REGISTER.md`, `J_MIGRATION_AND_RETIREMENT.md` and `K_USER_DECISIONS.md`, and the Forge source, test and workflow files cited inline. Two alternatives to the recommended architecture are kept in I.2 with the reason each lost.

**Abbreviations, defined once.** Each is `docs/design/<file>` at `chatgpt/forge-quest-studio-foundation@824c4d58`, cited as `ABBR:line` or `ABBR §n`; the rule always belongs to the owner and is cited, never copied (`CLAUDE.md` §7). SSC = FORGE_NEXT_SAFETY_STATE_PRESENTATION_CONTRACT.md. MOB = FORGE_NEXT_MOBILE_ACCESSIBILITY_AUDIT.md. WCM = FORGE_NEXT_WORKFLOW_COMPONENT_MAP.md. WFA = FORGE_NEXT_WIREFRAME_ANATOMY.md. SCR = FORGE_NEXT_SCREEN_CONTENT_REQUIREMENTS.md. IRM = FORGE_NEXT_INTERACTION_RISK_MATRIX.md. CPY = FORGE_NEXT_UI_COPY_AND_STATE_LANGUAGE.md. ICN = FORGE_NEXT_ICON_MOTION_SEMANTICS.md. SCN = FORGE_NEXT_UX_SCENARIO_MATRIX.md. ACC = FORGE_NEXT_DESIGN_ACCEPTANCE_CHECKLIST.md. COL = FORGE_NEXT_COLOR_SEMANTICS.md. AUD = FORGE_CURRENT_UI_UX_BASELINE_AUDIT.md. QS = FORGE_NEXT_QUEST_STUDIO.md. RB = FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md. IDX = FORGE_NEXT_UI_DESIGN_INPUT_INDEX.md. FBRF = `state/prompt_forge_quest_studio_foundation.md` at the same SHA. Files that exist only on that branch carry the prefix `824c4d58:`. Unprefixed `forge/**`, `.github/**` and `docs/forge_next/**` paths are `main@305a28f`, which this planning branch is byte-identical to for `forge/`, `.github/`, `forge_bundle.js` and `forge_loader_user.js`.

**Evidence tiers** are `docs/00_INDEX.md`'s and are never upgraded. Code and workflow claims are Source-verified. The suite counts and timings are Behaviour-proven from one local run. The Actions run history is Observed. Anything about a real browser, a real phone or the live game is Assumed or Inferred and is routed to I.8 rather than asserted.

## I.1 Today's baseline

`cd forge && npm test` on this checkout is **293 tests, 292 pass, 1 fail, exit 1, 10.2 s wall, Node v22.22.2** (Behaviour-proven, `evidence/forge-tests-ci.json` totals row for `ALL`). CI pins Node 24 (`.github/workflows/forge.yml:39`), so the local run and the CI run are not the same runtime and `forge/package.json` declares no `engines` range.

| File | Tests | Pass | Fail | ms | What it holds |
|---|---|---|---|---|---|
| `forge/test/adversarial.test.mjs` | 75 | 75 | 0 | 377 | crash-resume, ambiguity, lease, budget arithmetic, transport malformations |
| `forge/test/auth.test.mjs` | 45 | 45 | 0 | 9744 | auth table pinned to source, gate, FPA-1/2/2b, takeover, scoping, no-leak |
| `forge/test/transport.envelope.test.mjs` | 30 | 30 | 0 | 122 | 11 recorded tRPC exchanges, byte-equality of requests |
| `forge/test/capture.full.test.mjs` | 23 | 23 | 0 | 196 | allowlist, 512 KiB ceiling, honest persistence verdicts |
| `forge/test/runner.test.mjs` | 21 | 21 | 0 | 232 | plan, drive, adopt/skip, every `push/*.json` re-validated |
| `forge/test/storage.journal.test.mjs` | 19 | 19 | 0 | 108 | write-ahead order, transitions, quota, repair |
| `forge/test/budget.test.mjs` | 16 | 16 | 0 | 192 | sliding window, trip-until, sleep accounting |
| `forge/test/ui.test.mjs` | 16 | 16 | 0 | 8925 | the whole DOM surface, plus two repo laws |
| `forge/test/storage.captures.test.mjs` | 13 | 13 | 0 | 132 | IDB v1 to v2 upgrade, two-way allowlist invariant |
| `forge/test/reconcile.test.mjs` | 9 | 9 | 0 | 145 | candidate survey, adopt, no blind retry |
| `forge/test/transport.client.test.mjs` | 9 | 9 | 0 | 175 | batching, 207 splitting, superjson |
| `forge/test/release_loader.test.mjs` | 9 | 8 | **1** | 99 | loader text and pin shape |
| `forge/test/harvest.test.mjs` | 8 | 8 | 0 | 715 | agreement with the real `harvest.py` (7 shell out to `python3`) |

**Harness.** Four socket-free doubles plus two libraries: `MemoryStorage` and `fakeClock` (`forge/test/shim.mjs:8-52`), `FakeGame`/`FakeClient` (`forge/test/fakegame.mjs`), `composeForTest`, which calls the **shipped** `compose()` from `forge/src/main.mjs:35` and substitutes only storage, IndexedDB, clock, tabId, auth state, runtime, `fetchImpl`, client and sleep (`forge/test/compose.mjs:12-27`), `fake-indexeddb` 6.0.0 (`forge/package.json:19`), jsdom for about 31 DOM cases, and 11 recorded tRPC envelope fixtures derived in-process from real `@trpc` 11.18.0 with a recording fetch. That `composeForTest` wraps production wiring is the single most valuable property of the current harness: a core extracted behind `compose()` inherits all 293 cases on its first commit (F.4).

**CI.** `forge.yml` runs on push and pull request for `forge/**`, the two root bundles, `harvest.py`, `pin_release.py` and two workflow files (`:3-20`), then `npm ci`, `npm audit --omit=dev --audit-level=high`, `npm test`, fixture regeneration with `git diff --exit-code`, and bundle rebuild with `git diff --exit-code` (`:42-53`). Five runs are recorded on `main`, all green, the last at `ce603def` (Observed, Actions API listing for `forge.yml`, queried 2026-09-12).

**The R-11 gap, stated exactly.** `forge/test/release_loader.test.mjs:47-51` asserts exactly one `@x-release-pending` marker naming the package version; `.github/scripts/pin_release.py:32` removes that marker when it pins the release on `main`; so every checkout of `main` is red by one test. The bot commit that creates the red state is pushed by `commit_generated.py` with the checkout's `GITHUB_TOKEN` (`.github/workflows/release_pin.yml:20-28`), and GitHub does not trigger workflows from such pushes (Inferred), so no run exists at `d1dbecc` and CI never sees the red. The only existing relaxation lives on the Studio branch bundled with unrelated assertion changes (`824c4d58:forge/test/release_loader.test.mjs:47-51`, which also drops the `@match` ordering `deepEqual` and the negative "/forge-only match" assertion, per foundation-impl M6). Phase 0 lands a marker-only relaxation and its brief records the branch's own version for integration (**K-60**, an engineering entry under `K_USER_DECISIONS.md` §K.1); gate **G-09** cannot close before one of them lands.

**Runtime parity.** The local run used Node v22.22.2 and CI pins Node 24 (`.github/workflows/forge.yml:37-41`); `forge/package.json` declares no `engines` range and no test asserts one. A larger suite that leans on newer test-runner features should pin the range rather than discover the difference in CI.

**Coverage gaps by module.**

| Area | Gap | Cite |
|---|---|---|
| `transport/upload.mjs` (79 lines) | zero tests; the three-step presign/PUT/asset flow is unreachable through `composeForTest` because `fetchImpl` throws | `forge/src/transport/upload.mjs:32-71`; `forge/test/compose.mjs:22` |
| `github.mjs` (89 lines) | zero direct tests; every UI test replaces `d.github` with a stub, so base64 decode, `ref` handling, 404 and rate-limit handling and the PAT header are unproven | `forge/src/github.mjs:13-89`; `forge/test/ui.test.mjs:51` |
| UI contract | 16 UI cases assert `textContent` regexes and class selectors; no serialized-DOM snapshot, no element-order or attribute assertion, no idempotent-re-render assertion; four of five screens are only asserted to have at least one child | `forge/test/ui.test.mjs:86-94,107-120` |
| UI flows never driven | "Reconcile & resume", "Re-read unverified items", adopt/skip, Exit, pause, delete-snapshot warning, toast panel, picker error states, the clipboard fallback | `forge/test/ui.test.mjs:96-105,254-284`; `forge/src/ui/app.mjs:180` |
| `boot()` end to end | only tested with `{establish:false}`; the real boot to compose to establish to probe to mount chain never runs | `forge/test/auth.test.mjs:39,172-190,749-758` |
| Transport under the runner | the real `TrpcClient`/`CookieSession` path is driven by the Runner only in two adversarial cases with one malformed body | `forge/test/compose.mjs:22-23`; `forge/test/adversarial.test.mjs:1013-1059` |
| Accessibility | no tooling and no assertions; `aria-current` at `forge/src/ui/app.mjs:84` is the only ARIA attribute in the tree | `forge/src/ui/app.mjs:84` |
| Keyboard | no `keydown` handler anywhere in `forge/src`, no `KeyboardEvent` dispatched in any test | `evidence/forge-tests-ci.json` keyboard gap row |
| Responsive | `forge/src/ui/styles.mjs` has zero `@media` rules; jsdom performs no layout, so nothing about width is testable today | `forge/src/ui/styles.mjs:19-53` |
| Visual | no screenshot or pixel tooling; the only visual contract is the selector-scoping string test | `forge/test/auth.test.mjs:262-276` |
| Bundle and performance | `forge/build.mjs:38` prints the size; no ceiling, no gzip budget, no startup or render measurement | `forge/build.mjs:32-38` |
| Coverage | no `--experimental-test-coverage`, no mutation testing; per-module coverage is unknown | `forge/package.json:7-11` |
| Generated artifacts | CI regenerates and diffs only the envelope fixtures; `fields.json` and `nested.json` are never re-derived in CI | `.github/workflows/forge.yml:46-49` |
| Legacy manifests | the compatibility walk is non-recursive, so `archive/spent-manifests` is never re-validated | `forge/test/runner.test.mjs:322-327` |
| CI paths | `push/**` is not in the path filters although `forge/test/runner.test.mjs:320-328` validates every file in it | `.github/workflows/forge.yml:3-20` |
| `harvest.py` | 7 of 8 cases `t.skip()` silently when `python3` is absent, so a skipped suite is still green | `forge/test/harvest.test.mjs:25-37,92-94` |
| Error-message coupling | `classifyError` splits `NOT_FOUND` by message regex; one of the two strings is a tRPC adapter string pinned by no fixture | `forge/src/transport/outcome.mjs:58-70` |

## I.2 Test architecture for a larger UI

**Recommendation.** Keep one runner (`node --test`), one composition (`composeForTest`) and one law (socket-free), and grow **seven layers** on top of it. The UI-contract and scenario layers do the work a component library would otherwise do by type checking, which is the price F.5 names for hand-rendered components.

| # | Layer | Runs in | Proves | Fails when |
|---|---|---|---|---|
| 1 | Unit | `node --test` | one module's invariants: journal transitions, budget arithmetic, outcome classification, validator rules | a rule changes without its test |
| 2 | Contract and fixture | `node --test` plus `python3` | agreement with things Forge does not own: recorded tRPC envelopes, `harvest.py` verdicts, generated field and nested contracts, archived manifests, exported journals | a wire format, a consumer or a pinned contract drifts |
| 3 | UI-contract | `node --test` + jsdom | the rendered DOM for a screen and a state, as a committed serialized snapshot, plus labels, order, targets, ARIA and the copy dictionary | a redesign changes a safety-bearing construction |
| 4 | Scenario snapshots | `node --test` + jsdom | the 72 SCN situations rendered from fixtures, S-46 to S-55 and S-65 held | a state combination collapses two axes |
| 5 | Adversarial | `node --test` | crash, eviction, ambiguity, refusal, quota, lease and clock cases, kept unedited across the programme | the safety core is re-implemented rather than moved |
| 6 | Static gates | `node --test` and `build.mjs` | laws that must hold by construction: no HTML sink, no unexpected host, scoped stylesheet, bundle ceiling, import direction, registry drift | a law is broken anywhere in `forge/src` or in the built bundle |
| 7 | Browser and live smoke | the operator's own device | layout, glyph coverage, injection, persistence prompts, and the one live write that proves parity | the real world disagrees with the harness; user-owned, see I.8 |

**Four harness rules that come with the growth.** (1) Replace the real `setTimeout(10..40 ms)` waits in the UI tests with awaited app and runner promises; they exist at `forge/test/ui.test.mjs:151,180,218,222,229,247,268` and `forge/test/auth.test.mjs:207,236,256` and are the only timing flakiness in the suite. (2) Reuse one JSDOM per file: `auth.test.mjs` and `ui.test.mjs` are 18.7 s of the 10.2 s wall clock's parallel budget, and a UI-contract layer multiplies DOM cases by an order of magnitude. (3) Drive controls through `click()` rather than calling app methods, so that `FakeGame`'s call log becomes the UI's contract and an unexpected call is a failure. (4) Enumerate rather than hand-pick: the journal's `ITEM_STATES` and `TRANSITIONS` are exported and already pinned by the adversarial suite (`forge/src/storage/journal.mjs:39-47`), so screen invariants can be asserted over the product of item state, job state, pause reason, verify result and auth state instead of over five chosen cases.

**Alternatives kept.**

- **A real-browser layer (Playwright plus Firefox) as the primary UI gate.** Lost on three grounds. It cannot be part of `npm test` without a ruling, because the socket-free premise is enforced by a grep over the test directory (`forge/test/ui.test.mjs:331-350`) and the task rule is explicit (`CLAUDE.md` §8); the fake game would have to be served in-process by route interception to avoid a listening socket, and Playwright's own control channel is local IPC whose status under the socket rule is undecided; and it would add a large devDependency and a browser download to a repository whose only runtime dependency is `superjson` (`forge/package.json:12-14`). It is not dead: it is the honest answer for responsive and visual regression, and I.8 keeps that work as an operator smoke until a director rules on the socket question.
- **A review checklist instead of a UI-contract layer.** Lost because ACC's 27 grouped rows are written as acceptance criteria for a human reviewer (ACC:11-20), and the package already has thirty-one risks whose mitigations are stated as gates. A checklist that is not a test regresses silently between phases, which is precisely the failure R-27 names: a redesign quietly drops one of AUD §17's thirteen guarantees.

### I.2.1 What the doubles cannot simulate, and where each thing goes instead

Naming this is part of the strategy: a harness that is trusted beyond its fidelity is worse than no harness. Each row below is Source-verified from `evidence/forge-tests-ci.json`'s harness rows and the files they cite.

| Double | What it cannot model | Where the proof goes |
|---|---|---|
| `MemoryStorage` | the `storage` event to another tab; browser byte accounting; a torn write | SM-7, and a `BroadcastChannel` double once a channel exists |
| `fakeClock` | wall-clock drift against the server's bucket boundaries; timers firing during an await | budget fixtures with explicit skew cases; never a real timer |
| `FakeGame`/`FakeClient` | HTTP batching, 207 mixed status, `maxBatch` and URL splitting, superjson on the wire; latency and interleaving; the real 429 message and its 1 percent money penalty | layer 2: a runner-level suite through the real `TrpcClient` against the recorded fixtures, which does not exist today |
| jsdom | layout and paint, so no responsive or visual assertion is possible; `adoptedStyleSheets` support is only guarded with `\|\| []`; keyboard and focus are never dispatched | SM-3 and SM-5 for layout and glyphs; keyboard becomes a jsdom family via dispatched `KeyboardEvent` |
| `fake-indexeddb` | origin-level eviction, IDB quota errors, `versionchange` from a second tab | SM-7 |
| envelope fixtures | the game's real routers and middleware, Clerk context, Next.js and Vercel gateway bodies | layer 2 fixtures plus the registry drift gate; gateway bodies stay hand-written |
| nothing at all | ViolentMonkey injection and self-update, `@run-at document-start` ordering against the real 404, `window.stop()` efficacy, `navigator.storage.persist()`, clerk-js session lifecycle, Upstash weighted-window behaviour, multi-tab interleaving | I.8 in full; none of these may be claimed as covered |


## I.3 UI-contract layer

One bullet per family. Each names its owning contract and the **value today** that becomes the regression baseline, so that a later implementation can prove it moved rather than assert it. Construction is `D_VISUAL_SYSTEM.md` §D2.4's; meaning is the contract's; wording is CPY's.

- **Label dictionary.** Every string a screen renders for an item state, a job state, a `pause.reason`, a verification result or an auth state comes from one dictionary keyed by the machine value (CPY §5 item lifecycle CPY:110-214, §6 job state CPY:215-283, §7 verification CPY:284-318, §9 authentication CPY:355-383, §10 authorization CPY:384-397, §11 rate limit CPY:398-412). Today: `pill()` renders the raw enum word and the `SESSION` pause sentence is a literal inside the App (`forge/src/ui/app.mjs:159-162`). Test: no screen module contains a state word as a literal; every dictionary key has exactly one string; every enum value has a key.
- **No send path while `SENT`.** No control bound to a send path may be enabled while any item of the job is `SENT`, and no control anywhere may be labelled "Retry" (SSC §3 SSC:107-186; ACC lifecycle rows ACC:52-63). Today the refusal is real but below the UI: `forge/src/runner/runner.mjs:192-194` throws, and `SENT` to `PLANNED` is structurally absent from the transitions table (`forge/src/storage/journal.mjs:39-47`); the UI side is asserted only as banner text (`forge/test/ui.test.mjs:96`) and "Reconcile & resume" is never clicked. Test: enumerate every button in every screen for a job holding a `SENT` item and assert `disabled` or a non-send handler, plus a source-wide assertion that no rendered label matches `/retry/i`.
- **Toast-only prohibition.** `SENT` ambiguity, an authorization refusal, `INCOMPLETE` verification, an orphan decision, a publish failure and a persistence failure each need a durable in-workflow surface and may never live only in a toast (WFA §16 WFA:484-506; SCR §16 SCR:450-465). Today a bad toast is the only surface for several of these and it disappears after 9 s (`forge/src/ui/app.mjs:98-102`). Test: render each state and assert a non-toast node carries it, and that removing the toast layer entirely leaves the state visible.
- **Disabled primaries carry a reason.** Every disabled primary has an adjacent, programmatically associated reason (IRM §7 IRM:273-291). Today the run button is correctly disabled by blockers (`forge/src/ui/screens.mjs:151`) and the resume button by `resumeBlocked` (`:222-226`), but disablement is communicated by `opacity:.45` (`forge/src/ui/styles.mjs:32`). Test: for every disabled control, a reason node exists within the same card and is referenced by `aria-describedby`.
- **No colour-only state.** Every state is colour plus glyph plus word plus construction plus a row rule whose line style differs (`D_VISUAL_SYSTEM.md` §D2.4 "no colour only states"; SSC §11 SSC:404-416). Today three collisions are in the sheet: `VERIFIED` and `DONE` share `--ok` (`forge/src/ui/styles.mjs:44`), `ORPHANED`, `PAUSED` and `INCOMPLETE` share `--warn` (`:45`), and `SENT` and `CONFIRMED` differ only in hue (`:43`). Test: for each state pair, assert the serialized pill differs in at least two of glyph, word and construction class, not only in colour token.
- **Minimum target size per control class.** Computed `min-height` per class against the floors (MOB §5 MOB:119-136, §18 MOB:369-388; CC-M3). Today: buttons and inputs 44 px (`forge/src/ui/styles.mjs:31,35`), navigation buttons 40 px (`:27`), the exit button 32 px (`:25`). Those two failing values are the baseline; the phase-2 slice fixes them (G.2.2). Test: a table of control class to floor, asserted from the parsed sheet rather than from prose.
- **Programmatic label for every input.** Today there is exactly one `<label>` in the tree, on the auto-commit checkbox (`forge/src/ui/screens.mjs:312`); the search input (`:75`), the paste-an-id input (`:62`) and the PAT input (`:305`) are placeholder-only, and AUD §15's "labels heavily used" (AUD:425-429) overstates it (CF-10). Test: every `input`, `select` and `textarea` in every rendered screen has a `<label for>`, an `aria-label` or an `aria-labelledby` that resolves.
- **Stylesheet allowlist and contrast.** The six-clause contract in `D_VISUAL_SYSTEM.md` §D2.4 "stylesheet contract test": every selector scoped under `.f-host`/`.f-app`/`.f-boot`; animation and transition only on allow-listed selectors; `--mut`, `--pub`, `--ok` and `--orph-fill` as background only where allowed; no lane token outside `.f-lane`; no `url(` and no `@font-face`; and the contrast table recomputed from the token string. Today the scoping rule is a comment and a string test (`forge/src/ui/styles.mjs:1-9`; `forge/test/auth.test.mjs:262-276`) and nothing covers animation, assets or contrast. This is BF-09's requested gate and R-28's.
- **Scenario snapshots S-01 to S-70.** Render each SCN situation from fixtures and commit the serialized DOM, diffed in CI exactly as the envelope fixtures are (`.github/workflows/forge.yml:46-49` is the pattern). S-46 to S-55 (Content Admin) and S-65 (publish failure inside publish context) stay **HOLD** until their K entries land. The first wireframe review's required subset is SCN's own: S-01, S-02, S-08, S-09, S-13, S-18, S-22, S-27, S-28, S-34, S-39, S-51 and S-52 provisional, S-59 (SCN:470-484); the pass criterion is SCN:484-488. S-39 is the mandatory split: a live-verified job whose repository sync failed is never rendered as overall failure, which is also R-07's UI half.
- **DOM order.** Consequence before detail and before the primary, per MOB §6 (MOB:137-164) and WFA §3 (WFA:43-101) and §5 (WFA:130-186). Test: assert index order of the mode band, blockers, advisories, counts and the primary control inside the serialized snapshot, not just their presence.
- **Mobile layout assertions.** MOB §18's checklist at 360, 414, 768 and 1280 (MOB:369-388). jsdom performs no layout, so the honest split is: in jsdom assert the media-query structure parsed from the sheet, the class and DOM structure per breakpoint, and that no element carries a fixed width above the smallest breakpoint; real wrapping, sticky behaviour and safe-area insets are I.8's SM-3. Claiming responsive coverage from jsdom would be exactly the dishonesty SSC §1 forbids.
- **Reduced motion.** `prefers-reduced-motion` and the Settings toggle produce the same information (ICN §14 ICN:324-334; `D_VISUAL_SYSTEM.md` §D2.4 "reduced motion"). Test: the serialized DOM for a running job is equal with and without the reduced-motion class except for the ember element, and every state word is present in both.
- **Live regions.** The `aria-live` assignments MOB §13 requires for status transitions (MOB:275-291): the mode band polite, the verdict banner an alert on appearance, halt and orphan cards alerts, the count line polite, progress as a progressbar. Today no live region exists. Test: per transition, assert the announcing node and its politeness.
- **Contrast.** Recompute every text and boundary pair from the token string with the same formula the visual work used, failing under 4.5:1 for text and 3:1 for boundaries (MOB §11 MOB:251-263). Today's known failure is disabled text at 4.01:1 from `opacity:.45` (`forge/src/ui/styles.mjs:32`).
- **Action matrix.** One table-driven test over IRM §4's current action matrix (IRM:170-202): action to button class, confirmation requirement, pre-action text and post-action evidence. Today ten `app.confirm()` sites carry the consequence as native dialog prose (`forge/src/ui/app.mjs:172-175`), which is R-12.
- **Axis combinations.** Every combination ICN §19 lists as one that must stay distinguishable is rendered and asserted (ICN:386-400), which is R-24's gate: operation context, job state, outcome, auth, budget and content lifecycle are six separate axes (SSC §2 SSC:22-106) and one cue may never mean two of them. The four snapshot cases the risk register names are S-64 to S-67; S-65 stays HOLD.
- **Per-screen budget.** No screen issues a read on render or on an interval; every read is an explicit tap through `CachedReader`, and the budget is rendered from `Budget.status()` rather than re-derived (R-03; `forge/src/ui/screens.mjs:229-232`). Test: mount each screen against `FakeGame` and assert zero calls, then assert the call count after the explicit refresh.

### I.3.1 The thirteen AUD §17 guarantees, each mapped to a kept-green test

AUD:457-469 is the acceptance list; SSC owns the meanings; BF-54 mapped each to code. A phase cannot close with an unmapped guarantee (R-27; G.0 standing gates).

| # | Guarantee (AUD §17) | Code today | Test today | Test after |
|---|---|---|---|---|
| 1 | read-only distinguished from mutation-capable | `forge/src/ui/screens.mjs:120-122,153-156` | `forge/test/ui.test.mjs:135` | + mode-band snapshot per mode, S-07, S-08 |
| 2 | full-capture persistence disclosed apart from read success | `forge/src/ui/screens.mjs:123-125` | `forge/test/ui.test.mjs:162`; `capture.full.test.mjs` | + two-verdict snapshot on CR-5 |
| 3 | blocking preflight, auth and image failures disable execution | `forge/src/ui/screens.mjs:151` | `forge/test/auth.test.mjs:786` | + disabled-with-reason family |
| 4 | auth re-evaluated at consequential actions | `forge/src/ui/app.mjs:228-237` | `forge/test/auth.test.mjs:341,366` | + re-read at the tap on every mutation control |
| 5 | ambiguous `SENT` reconciled, never retry-safe | `forge/src/runner/runner.mjs:192-194`; `screens.mjs:222-226` | `forge/test/ui.test.mjs:96` | + no-send-path-while-SENT family, no `/retry/i` label |
| 6 | `CONFIRMED` is not `VERIFIED` | `forge/src/storage/journal.mjs:39-47`; `styles.mjs:43-44` | `forge/test/ui.test.mjs:254` | + pill construction pair test |
| 7 | incomplete verification stays visibly unverified | `forge/src/ui/screens.mjs:203-206` | `forge/test/ui.test.mjs:254` | + S-27, S-28 snapshots |
| 8 | recovery decisions explicit and operator-controlled | `forge/src/ui/screens.mjs:45-70` | `forge/test/runner.test.mjs:287` (API only) | + adopt and skip driven through `click()` |
| 9 | no automatic deletion | `forge/src/storage/journal.mjs:275-282` | journal suite | + maintenance-action family, bounded by K-16 |
| 10 | evidence deletion explains its consequence | `forge/src/ui/screens.mjs:286-297` | `forge/test/ui.test.mjs:206` (listing only) | + confirmation-copy assertion on both delete paths |
| 11 | rate-limit state inspectable | `forge/src/ui/screens.mjs:229-232` | `forge/test/ui.test.mjs:107`; budget suite | + budget rendering under TRIPPED |
| 12 | technical detail remains available | `forge/src/ui/screens.mjs:249-252` | `forge/test/ui.test.mjs:107` | + progressive-disclosure family, ACC:244-249 |
| 13 | no carrier contamination | `forge/src/ui/styles.mjs:1-9`; `takeover.mjs:177-181` | `forge/test/auth.test.mjs:262`; `ui.test.mjs:70` | + stylesheet allowlist and a release test asserting no node or style survives `release()` |

## I.4 Execution-core protection

The core is `forge/src/runner/`, `forge/src/storage/`, `forge/src/transport/`, `forge/src/budget/` and `forge/src/reconcile/`. R-13 is the risk that a UI programme silently re-implements it. Five mechanical proofs, all socket-free, all from F.4.

1. **Per-phase diff gate.** Each phase reports every file it touched under those five directories. The expected report is empty for a shell phase; for the whole programme it is two reviewed additive entries: the structured progress emitter beside `forge/src/runner/runner.mjs:91`, and `MIGRATIONS[1]` in the empty table at `forge/src/storage/journal.mjs:407`. This is gate `G-<phase>.seam` (G.0).
2. **Suites below the seam stay unedited.** The acceptance evidence for the phase-0 extraction is that not one of the 75 adversarial, 45 auth, 19 journal or 16 budget cases is modified while all of them pass. An edited case is a finding, not a fix.
3. **Import direction ratchet.** Cross-seam imports from `ui/` and `hosts/` go from eleven to zero and then hold at zero.
4. **DOM fixtures across the move.** Deterministic serialized fixtures for all five screens are committed **before** the extraction and must come back byte-identical after it. That is what distinguishes "moved" from "rewritten".
5. **Advisory emitter.** A throwing event subscriber leaves journal bytes, write order and the transition sequence identical; and a static forbidden-string test, modelled on `forge/test/auth.test.mjs:749`, asserts no event payload can carry a record body, a PAT or cookie material.

**Fixture journals from real exports.** `Journal.exportText()` (`forge/src/storage/journal.mjs:398-401`) is the source of migration fixtures: real exported journals, redacted of nothing because nothing auth-derived is written to them (`forge/test/auth.test.mjs:749`), replayed through `migrate()`. Three properties must be asserted for `MIGRATIONS[1]`: a v1 record migrates additively with no field renamed or removed; a v2 record refuses to load on the previous bundle, which `migrate()` already enforces at `forge/src/storage/journal.mjs:413`, so the two-release rule is testable rather than a convention; and a failed migration parks the record and surfaces it through `journal.broken` (`:225`) rather than deleting it (R-09).

**Adversarial cases the larger surface must add**, in the same file and the same style as the existing 75:

- a `SENT` item on every screen that can reach a send path, with every control enumerated and asserted refused;
- an `ORPHANED` item adopted through the DOM and skipped through the DOM, asserting the journal transition each takes and that "skip" copy says the live row may remain (ACC:104-114);
- an `INCOMPLETE` job re-read through the DOM, asserting zero mutation calls in the `FakeGame` log;
- a session that dies between preflight render and the tap, asserting the run is refused at the gate rather than at the server (the API-level case exists at `forge/test/auth.test.mjs:366`);
- a budget trip during a multi-item job, asserting no early retry control appears (ACC recovery row);
- a repository sync failure on a verified job, asserting the live verdict and the sync verdict are separate nodes (S-39, R-07);
- a `checks: null` Forge bundle replayed through `harvest.py verify`, asserting UNVERIFIED and exit 1, which is R-19's parity case and a Builder-retirement gate (G-13).

## I.5 Studio seam gates, post-integration

**Precondition.** Nothing in this subsection begins before all three of G.0's Studio preconditions hold: `chatgpt/forge-quest-studio-foundation@824c4d58` independently reviewed and integrated into `main`, **K-26** ratified or reverted, **K-15** ruled. Fable writes no test against that branch while it is active (`CLAUDE.md` §4; RM-01). The gates named in the approved foundation brief (FBRF:108-120) are the starting list, and these are the additions the reading makes necessary.

- **One CI job, not two.** `824c4d58:.github/workflows/quest_studio_ci.yml` adds a second `npm ci` and `npm test` beside `forge.yml` and carries no `npm audit` step where `.github/workflows/forge.yml:44` has one. Fold the Python steps into the existing Forge and skillpack jobs; keep one gate set (R-22; RI6).
- **`quest_compile.py --selftest` and the compiler integration test run once**, in that single job, alongside `npm test`, the fixture diff and the bundle diff.
- **The no-live-game static check becomes a gate.** FBRF:110-118 requires "static verification that the worker has no live-game URL/use"; no CI step performs it today (G2). The mechanism already exists in the repository: `forge/test/ui.test.mjs:341-349` walks `forge/src` and asserts the only hosts named are `api.github.com` and `cdn.jsdelivr.net`. Extend the same walk over the worker, the compiler and the Studio files.
- **Bundle size budget.** The Studio adds 39,621 bytes, 10.0 percent, to the unminified bundle, measured in a scratch overlay by the foundation reading and not re-run here (Observed). Baseline is `A_ARCHITECTURE_MAP.md` §A.9's 397,984 raw and 74,969 gzip. The budget asserts raw and gzip against a per-phase declared delta (R-06; **K-14**).
- **Composition under test includes the Studio.** `installQuestStudio(deps.app)` is called from `bootHost` after mount rather than from `compose()` (`824c4d58:forge/src/main.mjs:151`), so the Studio sits outside the graph every harness covers, and its jsdom test builds a `fakeApp` (`824c4d58:forge/test/quest.studio.ui.test.mjs:22-41`). Moving Studio state into `compose()` puts it under `composeForTest` and lets the jsdom tests run against the real App (RI8; F.8).
- **Promotion contract test.** The bytes named by the envelope, and only those, are fetched under the request's build directory, parsed by `parseManifest`, planned by `planOrder`, validated by the same validator and gated by the same auth check at the tap, with provenance journaled (Studio branch, source revision, compiler revision, generated-manifest hash). There is no Start control in the Studio (QS:306-312; F.7). The contract itself is **K-39**; the test asserts whatever K-39 rules, and asserts today that no second path into the runner exists.
- **Generated-projection test.** A browser-side advisory rule that encodes a constraint the generated source does not carry fails the build (R-20). The concrete case: the draft check refuses a profile shape the canonical compiler does not enforce (`824c4d58:forge/src/studio/ui.mjs:122-138` against `skills/building-tnr-content/scripts/mission.py:156-174`). Whether the compiler should enforce it is **K-36** and belongs to a canonical-owner brief (F.17), not to a Forge slice.
- **Classification-by-code test.** A test fails when blocker classification depends on message text (R-21). It can only pass after `mission.py` emits structured codes, which is its own Lane A brief; until then the three literal markers stay covered by fixtures and the debt is recorded.
- **Durability and observability.** A per-request draft record survives a simulated tab eviction mid-compile with its sync state intact, using the RB §11 vocabulary (RB:271-280); and a build that will never land is named within one poll cycle instead of leaving silence (K-38).

## I.6 Static gates

| Gate | Assertion | Exists today | Cite |
|---|---|---|---|
| no HTML sink in source | walk `forge/src`, fail on `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write` | yes | `forge/test/ui.test.mjs:29-34` |
| no HTML sink in the bundle | re-grep the built output and throw | yes | `forge/build.mjs:32-37` |
| `h()` deny-list | refuse a dangerous property assignment at runtime, closing the hole both greps are blind to | no | F.5 |
| socket-free | no test imports a network module or calls a global fetch | yes | `forge/test/ui.test.mjs:331-344` |
| host allowlist | `forge/src` names only `api.github.com` and `cdn.jsdelivr.net` | yes | `forge/test/ui.test.mjs:345-349` |
| no live-game URL in worker, compiler, Studio | same walk over the new surfaces | no | FBRF:110-118; G2 |
| stylesheet contract | six clauses, see I.3 | no | `D_VISUAL_SYSTEM.md` §D2.4 |
| bundle ceiling | raw and gzip against the declared per-phase delta | no | F.16 |
| core API surface golden | facade names, event types and snapshot keys are a reviewed list | no | F.4, F.16 |
| contract-data drift | `forge/src/runner/fields.json` and `nested.json` re-derive from the pin byte-identically | no | `.github/workflows/forge.yml:46-49` |
| procedure registry drift | every registry row's kind, auth class and limiter still matches the pinned source; `auth_pin_diff.mjs` and `pin_relevance.mjs` run in CI | partial: the auth table is pinned in-suite, the tools are not wired | `forge/test/auth.test.mjs:88,120` |
| import direction | nothing under `ui/` or `hosts/` imports below the seam | no | F.4 |
| event payload purity | no record body, PAT or cookie material in any event or snapshot | no, but the pattern exists | `forge/test/auth.test.mjs:749` |
| exactly one immutable `@require` | one pinned commit URL per bundle | yes | `.github/scripts/pin_release.py:24-29`; `forge/tools/check_release_pin.mjs:28-34` |
| CI path filters | add `push/**` and `state/staged_workflows/release_pin.yml` so a manifest change runs the suite that validates it | no | `.github/workflows/forge.yml:3-20`; `forge/test/runner.test.mjs:320-328` |
| coverage collection | `node --test --experimental-test-coverage` in CI so a much larger surface cannot silently drop coverage | no | `forge/package.json:7-11` |
| legacy manifest sweep | walk `archive/spent-manifests` recursively as well as `push/` | no | `forge/test/runner.test.mjs:322-327` |
| `harvest.py` presence | fail rather than skip when `python3` is absent in CI | no | `forge/test/harvest.test.mjs:25-37` |

## I.7 Per-phase gate map

`PH-<phase>.state` and `PH-<phase>.seam` are the per-phase gates defined in `G_ROADMAP.md` §G.0, named with a distinct prefix so they cannot be read as retirement gates; the retirement gates `G-01` to `G-13` are `B_PARITY_MATRIX.md` §B.4's and `J_MIGRATION_AND_RETIREMENT.md` §J.1's and are not reworded here. **Standing in every phase:** R-01 (no send path while `SENT`), R-27 (thirteen guarantees mapped), R-06 (bundle budget), R-05 (source-drift check), R-02 (a user-owned read-only browser smoke after each release).

| Phase | `PH-n.state` evidence | `PH-n.seam` expected diff | Risk gates asserted here | Test families added | Blocked by |
|---|---|---|---|---|---|
| **0** foundations | five screens render byte-identically from committed DOM fixtures; every rendered value traces to F.10's seam table | one reviewed additive entry: the emitter beside `runner.mjs:91` | R-11, R-13, R-19, R-22; R-05 and R-06 gain standing gates; R-02 gains the host-drift check | DOM fixtures, import-direction ratchet, headless-host lifecycle, core API golden, contract-data drift, bundle budget, no-live-URL static check, the thirteen-guarantee map | none from the director; K-13, K-14 and K-60 are engineering positions the brief fixes |
| **1** capture tiers | tier, verdict and budget values all come from producers, none from the view | empty | R-04, R-03, the persistence half of R-10 | registry rows from the pin, journalled-input equals sent-input, tier export refusal, `*.gen.py` byte-identical replay, null-body `harvest.py` fixture, per-screen budget | K-06, K-17 |
| **2** shell | no pill, lamp, band or label without a machine source; every element traces to a capability row | empty | R-12, R-16, R-24, R-25, R-28; R-15 release clause | stylesheet contract, release test, scenario snapshots S-64 to S-67 and the ICN §19 combinations, durable-surface test, target floors, labels, live regions, contrast, reduced motion | K-01 tokens, K-02, K-20 to K-24, K-31 to K-33, K-56 to K-58 |
| **3** manifest and recovery | `job.sync` and every recovery affordance render from journal state | one reviewed additive entry: `MIGRATIONS[1]` | R-07, R-09, the recovery half of R-01 | journal-v2 fixtures from real exports, sync-journaled-before-write, zip pack replay with byte ledgers, partial-quest-edit shapes, derived enum sets, ingress inventory, `github.mjs` contract tests against a fake | K-12, K-15, K-16, K-59 |
| **S** Studio | build state renders on the content-lifecycle axis, never as execution success | empty | R-17, R-18, R-20, R-29, R-30 | I.5 in full | the three G.0 preconditions; K-25 to K-27, K-36 to K-40, K-46, K-49, K-50 |
| **4** admin read | status is folded from events, never stored; lifecycle values come from a fresh read | empty | R-03 queue clause, R-14, R-26, R-31, the read half of R-08 | fold-the-events, staleness re-read before send, hidden-is-not-confidential copy test, conditional authorization label, per-class preview or neutral state | K-03 to K-05, K-08 to K-10, K-16, K-34, K-47, K-52, K-53 |
| **5** publish | the publish verdict comes only from a read-back | empty | R-08 publish clauses, R-12 level, R-31 copy | dependency pre-check, read-back-only publication, publish never styled as execution success, armed-confirmation naming the record | K-07, K-12, K-30, K-54, K-55 |
| **W** workspace | every rendered value is derived on read, none stored | empty | none new | projection test, provenance test, explicit no-write assertion | K-28, K-43, K-44 |
| **6** retirement | the gate table re-measured on the named release SHA | empty | R-10, R-15 | full gate re-measure, `npm test` at 100 percent with the exact count, `CLAUDE.md` §8 gates for touched skills and docs with exit codes | K-10, K-11 |

## I.8 Browser and live smoke, user-owned

**None of this was performed in this pass.** Each row is the operator's action on the operator's own device (`CLAUDE.md` §6: repository access is not live-game authorization, and Claude does not push the live game). Ids `SM-1` to `SM-9` are local to this section and renumber nothing. Read-only smoke comes first in every case; the one mutating row is `SM-2`, which is the live write that gate **G-08** cannot close without.

| Id | After | Steps | Expected observation | Proves | Does not prove |
|---|---|---|---|---|---|
| SM-1 | phase 0 release | install the pinned loader, open a matched game page signed in, open `/forge`, visit all five screens, press Close | Forge mounts once, the game page is intact after Close, the session lamp reads ready | injection, `@require` resolution, boot, mount and `release()` on a real Fenix build | anything about mutation |
| SM-2 | phase 0, `main` green | run one hidden jutsu create with an `@img` upload, one quest edit, one ai edit with rules, then commit the bundle to `harvests/inbox` | records created and edited, read-back verified, bundle committed | **G-08** live write proof; the uploader path that has zero tests; `harvest.py` agreement on a real bundle | Builder parity in general |
| SM-3 | phase 2 | open the shell at 360, 414, 768 and 1280 CSS px, one portrait and one landscape | no horizontal page scroll, targets meet the floors, the sticky bar never covers a warning, safe-area insets respected | MOB §18 and ACC:182-193, which jsdom cannot decide | contrast under daylight |
| SM-4 | phase 2 | toggle the OS reduced-motion and increased-contrast settings, then the in-app toggles | both paths produce the same information; the ember stops | whether OS preferences reach a userscript overlay, recorded as Inferred in `D_VISUAL_SYSTEM.md` §D2.7 | anything about other browsers |
| SM-5 | phase 2 | read every state pill and mode glyph on the device | no tofu; if any glyph is missing, the word and construction still carry the state | Firefox Android coverage of the chosen Unicode blocks (§D2.4 glyph policy) | desktop rendering |
| SM-6 | phase 2 | load a page with both loaders installed | the Builder panel does not reappear over the Forge surface, and the game keeps its own nodes | R-15, which is source-verified but unverified in a browser | long-term coexistence |
| SM-7 | phase 3 | start a read-only job, background the tab until the browser evicts it, return | the job is reconstructed with its real state and no request is re-sent | recovery after real eviction, which no harness models | eviction of the whole origin |
| SM-8 | phase 3 | observe the storage-persistence prompt | the permission outcome and the label it produces | `navigator.storage.persist()` behaviour, untested because `forge/src/ui/app.mjs:408-410` swallows it | quota behaviour under pressure |
| SM-9 | after the Studio seam merges to `main` | dispatch one compile with a throwaway request id from the operator's device | a build result document appears at the submitted revision with `liveGameTouched:false` | the seam end to end; the worker refuses any ref but `refs/heads/main`, so a branch cannot exercise it (G.2.S) | nothing about the live game, which it must not touch |

**Two rules that bind this table.** A smoke step is never scheduled as Fable work and never appears as a phase deliverable; it is an operator action a phase enables. And a smoke observation is Behaviour-proven only for the device and build it ran on; it never upgrades a source-verified claim and never substitutes for a socket-free test that could have been written instead.

## I.9 Open decisions routed to K

Every entry stays open; this section settles none of them and creates no new id.

- **K-14** minification decides what the bundle-size budget and the reproducibility diff compare, and whether a reviewer can still read the checked-in artefact.
- **K-13** pin refresh decides which SHA the contract-data and registry drift gates re-derive against.
- **K-60** is the release-loader baseline fix. It is an engineering entry: phase 0 authors the marker-only relaxation, and gate G-09 closes when it or the ChatGPT branch's equivalent is in `main`.
- **K-06** and **K-17** decide what the capture-tier and registry-row tests are allowed to assert.
- **K-12**, **K-16** and **K-58** decide the confirmation and deletion behaviour the action-matrix and maintenance-action families test.
- **K-20** to **K-24** decide the label and token values the scenario snapshots freeze; snapshots taken before those rulings would have to be retaken.
- **K-34** decides whether an authorization-denial label may be rendered at all, and therefore whether that test asserts a label or its absence.
- **K-05**, **K-53** and **K-55** decide which admin classes get preview tests and whether a publish control exists to test.
- **K-36** and **K-39** decide what the generated-projection and promotion-contract tests assert; both are owned outside Forge.
- **K-15** and **K-26** decide the credential scope the Studio tests must assume.

**One question the register does not yet carry.** If automated responsive or visual regression is ever wanted, whether a locally driven browser and its IPC control channel count as "socket-free" is a user-owned decision under `CLAUDE.md` §8 and §10. This section does not need that ruling, because it routes responsive and visual proof to the operator smoke in I.8 instead; it is surfaced in the handoff so that section K can adopt it if the director wants the automated layer.
