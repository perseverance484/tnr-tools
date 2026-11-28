# Forge protected-auth independent review — round 2

**Repository:** `perseverance484/tnr-tools`  
**Implementation branch:** `fable/forge-protected-auth`  
**Intended base:** `2855825ca215b48c1b04522c2a40948dd8cefe02`  
**Previous rejected head:** `13cc091aa6239ea1774605bf7b7f4c7720805b0e`  
**Reviewed frozen head:** `3b6c566eef5459fe16f104d5ee21accbc4e0f6c8`  
**Review branch:** `chatgpt/review-forge-protected-auth-r2`  
**Verdict:** REJECT / one correction loop remains before integration

## Scope

This is the narrow re-review authorized by the first report: FPA-1 carrier body-readiness, FPA-2 auth invalidation/resume behavior, and FPA-3 source-pin reconciliation. Current `main` remains the intended base. No live-game request or write was made. The review runtime inspected the exact source/tests/evidence but did not independently execute Fable's npm/build commands.

## FPA-1 — CLOSED

The document-start carrier hazard is corrected.

- `bootHost()` now awaits `whenBodyReady()` before touching the carrier document.
- `whenBodyReady()` re-checks `doc.body`, writes nothing while waiting, and resolves from parser-observable signals.
- `mountHost()` moved inside the guarded host-start path.
- `alreadyMounted()` prevents duplicate overlays.
- The new bodyless-jsdom tests cover an armed host before `<body>` exists, delayed body insertion, exactly-one mount, an unarmed bodyless page, and the original direct-mount hazard.

No surviving FPA-1 blocker was found.

## FPA-2 — NOT CLOSED / integration blocker: protected SESSION handling is still incomplete in AI-rules and reconciliation paths

### Invariant
Once any protected TNR procedure returns a server-proven SESSION/`UNAUTHORIZED`, the shared auth state must be invalidated before further protected work, and recoverable work must remain resumable rather than being misclassified as an ordinary content failure/orphan.

### What round 2 fixed

`AuthState.refuse()` and `Runner._authRefused()` correctly invalidate the shared state for several paths: capture reads, ordinary fill reads, ordinary verify reads, `ai.getAiProfile` verification, dedup-name reads, and decoded mutation refusals. `App.resumeBlockedReason()` then disables Resume until a successful re-check.

### Surviving path A — `_rules()` `profile.getAi` reads

`forge/src/runner/runner.mjs::_rules()` performs two protected `profile.getAi` reads:

1. the initial AI read before deciding whether a profile toggle is needed;
2. the post-toggle AI read used to obtain `aiProfileId`.

Both are preceded by `_requireAuth()`, but neither classifies a returned SESSION response through `_authRefused()`:

```js
let live = await this.reader.get(rc.get, userId, { fresh: true });
if (!live.ok || !live.data) throw new Error(`profile.getAi failed for ${userId}`);
...
live = await this.reader.get(rc.get, userId, { fresh: true });
apid = live.ok && live.data ? live.data.aiProfileId : null;
if (!apid) throw new Error("no aiProfileId after toggle");
```

If the session expires after the earlier gate/probe, the first path becomes an ordinary item failure and leaves `AuthState` READY. If expiration happens after a successful `ai.toggleAiProfile`, the second path is worse: the toggle mutation has landed, the item is `CONFIRMED` at the rules phase, then the unauthenticated read is converted by `_runItem()` into terminal `FAILED`. Resume will skip that item, leaving a partially configured AI/profile rather than pausing it for re-auth and continuation.

This path is directly relevant to One Perfect Crop because its enemy AI implementation uses the AI-rules/profile machinery.

### Surviving path B — reconciliation reads after the resume gate

`Runner.resume()` correctly gates before reconciliation, but a session can expire between that gate and `Reconciler.resolveSent()`. The reconciler performs protected AI reads in `_resolveUpdate`, `_resolveToggle`, and `_resolveRules`, and treats `!ok` generically as orphan/unavailable rather than returning a SESSION condition to the runner.

For AI SENT states this can turn a server-proven authentication problem into `ORPHANED`, recreating the exact class of operator confusion the auth repair is intended to eliminate. A write that may be perfectly recoverable after signing back in can instead become an adopt/skip decision.

### Test gap

The five new FPA-2 tests cover capture refusal, mutation refusal, subsequent-run blocking, multi-item blocking, and banner/Resume behavior. They do not exercise:

- `profile.getAi` returning UNAUTHORIZED inside `_rules()` before toggle;
- `profile.getAi` returning UNAUTHORIZED after a successful toggle;
- a SESSION response during AI reconciliation after `resume()` has already passed its auth gate.

The correction commit message claims that "every decoded SESSION classification" is centralized through `_authRefused()`, but these protected reads are counterexamples.

### Smallest robust correction

Keep the current architecture. Do not redesign auth.

- In `_rules()`, classify both `profile.getAi` read failures. SESSION must call `_authRefused()` and pause without terminalizing the item. For the post-toggle read, preserve `CONFIRMED`/rules state so a successful re-check can resume and finish the rules write.
- Make reconciliation surface SESSION distinctly to `Runner.resume()` rather than converting it to an orphan. The runner should invalidate auth and pause, preserving the SENT state for later reconciliation after re-auth.
- Add focused socket-free regressions for the three paths above and prove no additional protected request is sent until `probe()` returns READY.

Because the correction is localized, another narrow re-review is appropriate.

## FPA-3 — FUNCTIONALLY CLOSED for the auth gate; one documentation sentence needs correction

The new `auth_pin_diff.mjs` is a reasonable reproducible mechanism for comparing `publicProcedure`/`protectedProcedure` declarations across the seven Forge content routers, and the handoff records 0 disagreements across all 43 Forge-addressable paths plus 0 auth-class changes across the whole compared surface. The task pin remains `bdec2883` and Forge's broader established pin remains `345d18ac`; the disagreement is now surfaced rather than silently blended.

One narrative claim in `docs/handoffs/FORGE_PROTECTED_AUTH_PIN_RECONCILIATION.md` is too strong: it says the signed-in `/` carrier "does no redirect and no extra work" because `proxy.ts` does not redirect. At task pin `bdec2883`, `HomeLanding.tsx` performs a client-side `router.push("/profile")` once signed-in user data is available. This does not presently invalidate the carrier architecture because the activation is per-tab and the provider tree/document remain alive, but the source note should say the server/proxy does not redirect while the client landing component may navigate after hydration.

Treat this as a documentation/source-evidence correction, not an integration blocker by itself.

## Verified sound in round 2

- Exact target remains frozen at `3b6c566eef5459fe16f104d5ee21accbc4e0f6c8`; `main` remains `2855825ca215b48c1b04522c2a40948dd8cefe02`.
- Round 2 is one commit on top of the rejected SHA and stays inside the authorized correction surface.
- FPA-1 body readiness is robustly addressed and covered by targeted tests.
- `AuthState.refuse()` plus the UI Resume gate are good primitives and correctly solve the paths actually wired through them.
- No credential extraction/copy mechanism was introduced; the same-origin `CookieSession` boundary remains intact.
- FPA-3 now has explicit dual-pin provenance and a committed comparison tool rather than an unsupported assertion.
- Public capture-only behavior remains outside the protected-auth gate.

## Unverified gates

Fable reports 290/290 tests green, byte-identical rebuild, fixtures no-diff, release-pin green, auth-pin diff exit 0, doctrine/packs/doctrinemap green, and lawmap 0 errors / 5 baseline warnings. These were not independently executed in this review environment.

## Next step

Fable should make one small correction commit on its own branch covering only the surviving FPA-2 read/reconciliation paths and the inaccurate carrier sentence, rerun the existing gates plus the new targeted regressions, freeze a new SHA, and return it for narrow round-3 review. Do not integrate or release `3b6c566...`, and do not rerun the live Bandit probe yet.
