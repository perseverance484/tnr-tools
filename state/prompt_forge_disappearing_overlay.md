# Forge disappearing-overlay repair — Fable implementation brief

**Status:** implementation brief for Lane A tooling work  
**Repository:** `perseverance484/tnr-tools`  
**Verified baseline:** `main` = `c5f8faaf2ddafe687b0dfb764ad5974e05823f86`  
**Implementation owner:** Fable / Claude Code  
**Independent reviewer:** ChatGPT  
**Live-game actor:** dauntless only  
**Current production game source inspected for this defect:** `studie-tech/TheNinjaRPG@98d0eca5c2e922f3b41e56120f096c072645c1f0`

## Objective

Repair Forge 0.4.0 so opening `/forge` reliably hands off to an authenticated TNR application route and leaves the Forge overlay mounted and usable instead of briefly showing Forge and then leaving the operator on the normal game page.

Do not broaden this task into combat-capture support, Aerathiel tooling, general Forge redesign, or unrelated refactoring.

## Operator-observed production failure

On current production, while signed in:

1. Open `https://theninja-rpg.com/forge`.
2. Forge splash appears briefly.
3. Forge redirects to the game as designed by 0.4.0.
4. The Forge overlay disappears; only the normal game remains.
5. Repeating `/forge` continues to produce the same splash -> game behavior indefinitely.
6. The same behavior occurs on the bare domain, so this is not explained by `www` -> bare-domain canonicalization alone.

No mutation is involved in this observation.

The repeated loop is important evidence. In current source `bootHost()` resets the Forge arm hop counter only after `mountHost()` and `App.mount()` complete. If the host never mounted, repeated entry attempts should eventually hit `MAX_HOPS`. Because the operator can repeat the splash/handoff indefinitely, treat “Forge mounts and is subsequently lost” as the leading hypothesis. Do not claim the precise removal mechanism until reproduced.

## Current implementation facts

Forge 0.4.0 intentionally separates entry from host:

- `/forge` is only the entry splash.
- It writes a per-tab `sessionStorage` arm marker.
- It navigates to `/`.
- On an armed normal application page, `bootHost()` waits only for `document.body`, appends `.f-host` to `document.body`, mounts `App`, and then resets the hop counter to zero.
- `.f-host` is fixed, full-screen, opaque, and extremely high z-index. If that node remained attached, the normal game would not simply be visible in its place.
- TNR's current root layout owns `<html>` / `<body>` and hydrates the normal Clerk/tRPC application provider tree.
- Current tests model the carrier as a static jsdom body with a pre-existing fake game root. They verify body-readiness and coexistence, but they do not simulate a framework hydration/reconciliation step after Forge inserts the host.

This makes a hydration/lifecycle race the strongest present hypothesis, but it remains a hypothesis until Fable reproduces the host detachment.

## Required investigation

Reproduce the failure locally without a live game request if possible.

Instrument the lifecycle in tests/harnesses sufficiently to answer:

- Does `.f-host` get detached after `mountHost()` succeeds?
- Is the detachment caused by a hydration-style body reconciliation/replacement, a client navigation, a Forge code path, or another DOM owner?
- Does `document.body` itself change identity, or only its children?
- Does the existing `/` -> `/profile` client navigation contribute, or does the overlay disappear before/independent of that navigation?
- Is `App.close()` or `release()` ever reached without an operator Close action?

Do not solve this with an arbitrary sleep unless evidence proves a time delay is the contract. Prefer a source-backed lifecycle/readiness condition.

## Required behavior

The repaired Forge must satisfy all of the following:

- The operator still enters through `/forge`.
- An unarmed normal game page remains completely inert.
- Forge must not destroy or replace TNR's React/Next/Clerk/tRPC provider tree.
- Forge must mount only when the carrier DOM is safe for an external overlay to persist.
- The overlay must survive initial application hydration and the normal signed-in landing-page client navigation to `/profile`.
- Exactly one Forge overlay may exist.
- If the Forge host is unexpectedly detached without the operator pressing Close, the condition must not fail silently. Recover safely after the carrier is stable or surface an explicit Forge startup/host-loss diagnostic.
- Do not enter a DOM tug-of-war with React. Any remount strategy must be bounded and lifecycle-aware.
- Do not reset the `/forge` hop counter merely because an instantaneous mount succeeded if that host has not yet reached the implementation's chosen stable-mounted condition. An overlay that vanishes immediately must not make `/forge` loop forever as though startup succeeded.
- Close must still remove Forge, disconnect any new lifecycle observers, restore scrolling, and disarm the tab.
- Preserve current authentication semantics: normal Clerk runtime stays alive; no cookie/token extraction; protected work remains gated by AuthState.
- Preserve current capture, journal, reconciliation, budget, upload, GitHub sync, and release-pin behavior.

## Preferred design direction

Fable should choose the smallest robust solution after reproducing the lifecycle.

A likely shape is to split “body exists” from “carrier is ready for a persistent external overlay.” Wait for a source-backed stable application/runtime condition, then append Forge. Existing `pageAuthRuntime()` / Clerk readiness may be useful evidence, but do not equate authentication with DOM stability without testing it.

A bounded host-loss observer is acceptable as defense-in-depth, provided it does not repeatedly fight application reconciliation. If the host is lost during initial hydration, Forge may wait for the stable condition and mount once. If it is repeatedly removed after stabilization, stop and show a diagnostic rather than looping.

## Tests required

Add regression coverage that proves:

1. `/forge` still arms and hands off without requiring another URL.
2. An unarmed normal page remains untouched.
3. An armed carrier reached at `document-start` still waits safely when no body exists.
4. A hydration-style reconciliation/removal after the initial body appears does not permanently erase Forge; after the chosen stable point there is exactly one persistent `.f-host`.
5. The test must actually detach/replace the first attempted host or otherwise model the production failure, so it would fail against current 0.4.0.
6. The normal application/provider root remains intact throughout.
7. A simulated `/` -> `/profile` client-side navigation does not remove Forge.
8. An unexpectedly detached host does not silently reset startup to “success”; the hop/startup lifecycle behaves deterministically.
9. Close cleans up the overlay, observers/listeners, scroll lock, and arm state.
10. Existing auth tests still prove protected work cannot run before auth readiness, public reads remain allowed where appropriate, and no credential material is read or persisted.
11. Existing Forge test suite remains green.
12. Loader/release tests remain green if loader metadata or activation behavior changes.

Tests must be socket-free and make zero live-game requests.

## Source/provenance requirement

Inspect the current production source at:

`studie-tech/TheNinjaRPG@98d0eca5c2e922f3b41e56120f096c072645c1f0`

At minimum re-check the current equivalents of:

- `app/src/app/layout.tsx`
- `app/src/app/page.tsx`
- `app/src/layout/HomeLanding.tsx`

Also compare any carrier/hydration assumption used by the fix against Forge's existing pinned-source evidence (`345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9`). Do not silently move Forge's global source pin as part of this bug fix unless the implementation genuinely requires a separate pin migration and calls it out for review.

## Release

Treat this as a patch release of Forge unless repository release machinery dictates otherwise.

Do not bypass the existing two-stage release-pin workflow. The checked-in loader must continue to point to an immutable `forge_bundle.js` commit after promotion.

Because the defect is browser/live-integration specific, local tests are necessary but not sufficient. After review/integration/release, dauntless performs the live smoke.

## Live smoke after release

First smoke is read-only:

1. Sign in normally.
2. Open `/forge`.
3. Confirm Forge remains visible through the carrier handoff and the automatic landing-page navigation.
4. Leave it open long enough to establish that it does not vanish immediately.
5. Confirm the Forge auth banner reaches the expected authenticated state.
6. Run the existing read-only Forge smoke/probe manifest if still current and appropriate.
7. Confirm zero mutations.

Do not proceed to a protected write merely because the overlay stays visible. The read-only smoke remains the gate.

## Explicitly out of scope

- `combat.getBattleHistory` / `combat.getBattleEntries` support.
- Aerathiel guide/content work.
- Builder retirement.
- New authentication mechanisms.
- Credential/token/cookie handling.
- TNR game-source changes.
- General Forge UI redesign.
- Unrelated Forge refactors.
- Doctrine/law changes.

## Required verification and handoff

Run the normal Forge gates from `forge/`, including at minimum:

- `npm test`
- `npm run build`
- `npm run fixtures` if fixtures or transport contracts are affected
- fresh build-equivalence check proving checked-in `forge_bundle.js` matches the source build
- release-loader/release-pin checks if loader metadata changes
- static credential-safety checks already required by the protected-auth repair

Return the standard frozen-SHA handoff from `docs/workflows/IMPLEMENTATION_HANDOFF.md` with:

- repository and implementation branch
- exact base SHA
- exact frozen head SHA
- integration target
- changed files
- reproduction/root cause found
- behavior implemented
- exact test commands/results
- build/bundle equivalence
- source/provenance inspected
- release/version/pin status
- known debt/deviations
- browser/live behavior not locally verified
- explicit statement of live requests, live writes, and credential/session material used

Freeze the handed-off SHA until ChatGPT's independent review returns.
