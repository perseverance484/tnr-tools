# Forge protected-auth independent review

**Repository:** `perseverance484/tnr-tools`  
**Implementation branch:** `fable/forge-protected-auth`  
**Intended base:** `2855825ca215b48c1b04522c2a40948dd8cefe02`  
**Reviewed frozen head:** `13cc091aa6239ea1774605bf7b7f4c7720805b0e`  
**Review branch:** `chatgpt/review-forge-protected-auth`  
**Verdict:** REJECT / correction required before integration

## Scope and evidence

Reviewed the exact one-commit delta from base to head, the frozen task brief `state/prompt_forge_protected_auth.md`, current collaboration/workflow authorities, the changed Forge source/tests/bundle/loader, the behaviour-proven failed protected captures, and the task-pinned TNR auth/provider source. No live-game request or write was made. The review environment could not clone/run the repository over the network, so Fable's reported test/build commands were inspected rather than independently re-executed.

## FPA-1 — Confirmed defect / integration blocker: carrier boot assumes `document.body` exists at `document-start`

### Invariant
The `/forge` entry must reliably hand off to an authenticated application-route carrier in the actual Android + Violentmonkey workflow.

### Evidence
- `forge_loader_user.js` deliberately keeps `@run-at document-start` and now matches the entire game origin.
- `forge/src/main.mjs::bootHost()` immediately executes `const host = mountHost(doc, win)` on an armed non-entry page.
- `forge/src/ui/takeover.mjs::mountHost()` immediately reads `doc.body` and calls `doc.body.appendChild(host)` with no body-readiness wait.
- `bootHost()` calls `mountHost()` before its local `try`, while the bundle's top-level boot wrapper swallows rejected boot promises so a failure does not break the game.
- The new carrier tests use a jsdom helper that always constructs `<body>` before calling `boot()`. `release_loader.test.mjs` separately asserts `document-start`; no test covers an armed carrier before `document.body` exists.

At `document-start`, a normal page is not guaranteed to have a body yet. The entry page does not expose this because `entryTakeover()` creates its own body, but the carrier relies on the real app document.

### Consequence
A valid `/forge` handoff can redirect to the carrier and then silently fail to mount Forge before the authenticated runtime is ever checked. The operator would see the underlying game instead of Forge, with the per-tab arm marker still present. This directly defeats the repair's production workflow.

### Smallest robust correction
Keep the early `/forge` interception, but make the armed carrier boot wait for a real `document.body` before `mountHost()`. Keep unarmed pages completely inert. Put carrier mounting inside the guarded failure path. Add a socket-free regression test that starts an armed host with no body, inserts the body later, and proves Forge mounts exactly once without touching the page before body readiness.

## FPA-2 — Confirmed defect / integration blocker: a server-proven `UNAUTHORIZED` does not invalidate the auth-health state

### Invariant
Once the server proves the current session is unauthenticated, Forge must fail closed and its standing auth state must not continue to claim protected work is available.

### Evidence
- `AuthState` can be `READY` after its initial probe.
- In `Runner._failFromOutcome()`, a protected mutation returning a SESSION/`UNAUTHORIZED` is correctly converted from SENT to FAILED and the job pauses, but `this.auth` is not changed from READY.
- In `Runner._captures()` and protected read-back handling, a SESSION/`UNAUTHORIZED` likewise pauses without invalidating `AuthState`.
- `App.authBanner()` renders READY as `TNR session active. Protected reads and writes are available.`
- `RunScreen` always offers `Resume` for a SESSION-paused job; it does not require a successful re-check first.
- On resume, the runner's preflight consults the still-READY `AuthState`, so it can issue another protected request against the already-refused session. For a multi-item write job, the first refused item is terminal FAILED and a later resume can advance to the next protected item and receive another predictable refusal.
- Existing tests prove the pause classification but do not assert that a server SESSION response transitions the shared auth state away from READY or blocks resume until re-establishment.

### Consequence
The run-specific error says authentication is unavailable while the standing banner simultaneously says the session is active. The operator can repeatedly send doomed protected requests after a server-proven auth failure. Writes remain cleanly refused rather than ambiguous, so this is not a corruption bug, but it violates the brief's explicit auth-health/fail-closed UX and weakens the safety gate.

### Smallest robust correction
Give `AuthState` a public method for recording a server-proven session refusal (for example `refuse(detail)`), transition to `SIGNED_OUT` when a protected query or mutation returns SESSION, and let the existing gate block all further protected work until `probe()` succeeds. Add regression tests for both protected read and mutation refusal: auth becomes SIGNED_OUT, the banner is no longer green, and pressing/resuming without a successful re-check sends zero additional protected requests.

## FPA-3 — Contract/source mismatch: implementation provenance silently substitutes a different TNR source pin

### Invariant
The task-specific pinned source controls source claims for this review unless a disagreement is surfaced and reconciled.

### Evidence
- `state/prompt_forge_protected_auth.md` pins `studie-tech/TheNinjaRPG@bdec2883`.
- The target's `forge/src/transport/procedures.mjs`, `forge/build.mjs`, generated bundle banner, Settings/About text, and builder notes instead identify `345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9` as Forge's source pin.
- `345d18...` is 89 commits after `bdec2883`; during that interval relevant `profile.ts`, `quests.ts`, and `item.ts` files changed.
- Spot checks show the key `profile.getAi` protected classification still agrees at both pins, but the full 43-row auth table was not proven against the task pin in this review.

### Consequence
This may be provenance-only rather than a functional defect, but the auth gate's completeness is security/safety relevant. The handoff should not claim task-pin compliance while deriving the table from another source without an explicit compatibility proof.

### Required resolution
Do not blindly downgrade Forge's established global pin. On the correction handoff, explicitly reconcile the two pins: either prove that every Forge-used CRUD auth classification and carrier/auth fact needed by this task is unchanged between `bdec2883` and `345d18...`, or align the task implementation/evidence to the task pin. Surface any real semantic difference rather than choosing one silently.

## Verified sound in the reviewed target

- Exact base/head relationship is clean: the target is one commit ahead of the intended base, with the same merge base.
- The high-level architecture follows the brief's preferred model: `/forge` is only the entry, an armed valid app route is the host, and the underlying provider tree is left mounted.
- The implementation does not introduce a custom game Authorization header or cookie copy path; `CookieSession` remains same-origin and rejects arbitrary auth/cookie headers.
- The auth probe uses a protected point read directly through the client and does not persist its body in the capture cache/journal/export path.
- Public capture-only work remains ungated by auth.
- A sent mutation receiving a decoded SESSION refusal is treated as a definite FAILED refusal, not ambiguous SENT, and no automatic mutation retry was added.
- Existing full-capture persistence, journal/reconciliation concepts, immutable loader pin staging, and generated 0.4.0 bundle remain present in the target.

## Unverified / not accepted as proof

- Fable reports `npm test` 278/278, deterministic bundle rebuild, fixture no-diff, release-pin green, doctrine/packs green, and lawmap 0 errors/5 warnings. I inspected the relevant source/tests but did not independently execute the repository because this review runtime has no network checkout of the repo.
- No browser/live-session verification was performed by ChatGPT. The first real verification must remain the read-only five-AI capture smoke after blockers are corrected, independently re-reviewed, integrated, and released.

## Correction/re-review boundary

FPA-1 and FPA-2 are blockers. FPA-3 must be explicitly reconciled in the next handoff. Fable should apply the corrections on its own implementation branch and return a new exact frozen SHA with the required gates rerun.

A **narrow re-review is acceptable** if the correction changes only carrier body-readiness/boot guarding, auth-state invalidation + associated UI/gate tests, and source-pin compatibility evidence. If the carrier architecture, session mechanism, procedure table semantics, or journal/reconciliation behaviour changes more broadly, repeat the relevant full auth review.
