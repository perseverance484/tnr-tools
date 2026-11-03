# Forge 0.4 carrier-disappears review

**Status:** confirmed blocker; implementation correction required  
**Date:** 2026-09-13  
**Repository baseline inspected:** `main@b526dee5b2bf070fe3aaebab82bc0e146b98025d`  
**Released Forge bundle:** merge `ce603def204f585d23837121b86cfdd9fd4c308c`, implementation head `e2bab901cdcab15018a80eadefefe64ae565d0e5`  
**Lead:** UI/UX Reviewer · supporting lens: Engineering Auditor  
**Live-game writes:** none. User browser observation is behaviour evidence; repository/source inspection only in this review.

## Operator symptom

On Firefox Android + ViolentMonkey, opening `/forge` shows the Forge handoff/splash, navigates to `/`, Forge appears for only a fraction of a second, then disappears while the game continues its normal landing flow to `/profile`.

The symptom began with the 0.4.0 authenticated-carrier architecture and persists with the exact released 0.4.0 loader/bundle.

## Confirmed defect

The 0.4.0 implementation assumes a Forge host appended to `document.body` is "outside" the game's React root and therefore survives hydration/client navigation. That assumption is false for the pinned Next App Router source.

At both protected-auth source pins (`bdec2883` and `345d18ac`), `app/src/app/layout.tsx` defines the React root layout as `<html>...<body>...</body></html>`. The body itself and its children are therefore part of the hydrated React document tree. Forge's `mountHost()` appends `.f-host` directly to `document.body` at document-start as soon as a body exists, before the application hydration it is trying to preserve has necessarily completed.

The released comments explicitly claim the overlay is "appended to document.body outside that root" and will survive `HomeLanding`'s `router.push('/profile')`. The source does not support that claim.

This exactly matches the observed failure shape: Forge can render briefly after `whenBodyReady()`, then disappear when the real application hydrates/reconciles the body while the landing page proceeds to `/profile`.

## Test-model gap

`forge/test/auth.test.mjs` models the game as:

```html
<body><div id="__next">the game</div></body>
```

and asserts Forge is a sibling of `#__next` under `body`.

That is not the pinned game's App Router root. The real root layout owns `<html>` and `<body>` directly. The test therefore proves survival beside a synthetic legacy-style inner root, not survival through the actual Next document hydration boundary.

The existing FPA-1 tests correctly cover "body does not exist yet" but not "body exists and is subsequently hydrated/reconciled by the framework that owns it." Passing those tests does not cover the user's failure.

## Why this is not a login requirement

The 0.4.0 architecture does not intentionally log the operator in again. `/forge` is an unmatched providerless route. It hands the tab to `/` so the already-authenticated game's Clerk/Next provider tree can run and maintain the existing session. At the pinned source, `HomeLanding` then routes a resolved signed-in user with `userData` + `userId` to `/profile`.

Reaching `/profile` is therefore consistent with the existing session being recognized; the unwanted behavior is Forge losing its host during that normal app startup/navigation sequence.

## Required correction properties

A correction should not merely add another delay without proving the boundary. It should:

1. stop treating `document.body` as outside the Next/React root;
2. establish a mount strategy that survives the pinned App Router hydration and `/` -> `/profile` client transition in Firefox Android + ViolentMonkey;
3. preserve the existing rule that an unarmed game page is inert;
4. preserve the existing Clerk/session safety boundary (no cookie/token extraction or copied auth material);
5. preserve journaling/reconciliation/write safety; this is a host lifecycle fix, not a reason to weaken mutation safety;
6. add a regression whose DOM/lifecycle model reflects the pinned root-layout shape rather than a synthetic `#__next` child;
7. perform a real operator smoke on Firefox Android before release, because this failure is specifically at the userscript/framework/browser integration seam local jsdom did not cover.

Potential implementation directions to evaluate include mounting only after the provider/runtime has demonstrably hydrated, and/or an explicitly lifecycle-resilient host strategy. Do not assume that simply re-appending before hydration is stable.

## Classification

**Confirmed defect / release blocker for Forge usability.** No evidence here indicates a live write or data-integrity failure; the consequence is that Forge 0.4.0 is unusable on the operator's real mobile path.
