# Forge protected-auth repair — Fable implementation brief

**Status:** approved implementation contract for Lane A tooling work.  
**Repository:** `perseverance484/tnr-tools`  
**Baseline when frozen:** `main` = `9b8a6f6c74577f5f4329ad6468fc69e98e2a6c76`  
**Implementation owner:** Fable / Claude Code  
**Independent reviewer:** ChatGPT  
**Live-game actor:** dauntless only  
**Pinned game-source evidence:** `studie-tech/TheNinjaRPG@bdec2883`

## Objective

Repair Forge so protected TNR tRPC reads and writes run from a valid authenticated Clerk session in the real Android + Violentmonkey operator workflow, without extracting, copying, persisting, logging, or manually handling Clerk cookies/session tokens.

The defect is production-blocking for Forge use: public captures work, but protected `profile.getAi` full captures return `UNAUTHORIZED` even when the operator expects to be using Forge while signed into TNR.

## Behaviour-proven evidence

Two separate Forge 0.3.0 runs of the same read-only manifest failed identically and sent zero mutations:

- `harvests/inbox/tnr_results_1789066888093.json`
- `harvests/inbox/tnr_results_1789067111434.json`

Each run attempted five `profile.getAi` reads with the correct `{ userId }` shape. All five returned `UNAUTHORIZED`; no body existed to persist; job outcome was failed; zero mutations were sent.

The second run followed an attempted `www.theninja-rpg.com` navigation. Production canonicalized back to `theninja-rpg.com`, so a simple hostname switch is not a fix.

Earlier Forge 0.3.0 full captures using public `gameAsset.get` succeeded, so the capture/full-persistence machinery and general same-origin tRPC transport are not globally broken.

## Source-verified constraints

At pinned game source `bdec2883`:

1. `app/src/server/api/trpc.ts`
   - `createAppTRPCContext` obtains `userId` from Clerk `auth()`.
   - `protectedProcedure` rejects when `ctx.userId` is absent.
2. `app/src/app/_trpc/Provider.tsx`
   - the normal browser tRPC client uses same-origin `/api/trpc` with no custom Authorization header.
3. `app/src/app/layout.tsx`
   - valid application routes render under `ClerkProvider` and `TrpcClientProvider`.
4. Forge 0.3.0 currently boots on `/forge`, whose loader explicitly describes it as a same-origin 404 with **no game providers**, and takes over at `document-start`.
5. `forge/src/transport/session.mjs`
   - the intended session model is cookie-based, same-origin only; no Authorization header is allowed.

The exact browser/session reason the providerless 404 loses usable Clerk authentication is not yet behaviour-proven. Do not claim a specific Violentmonkey sandbox bug or cookie-TTL mechanism unless implementation evidence proves it. The repair must solve the observed contract failure regardless.

## Required behaviour

### A. Preserve the operator entry point

The operator must still be able to navigate to:

`https://theninja-rpg.com/forge`

It is acceptable for that entry point to redirect/transition internally to a source-verified valid application route carrying a Forge marker, if that is the safest way to keep Clerk hydrated. The operator should not have to remember a replacement URL.

### B. Forge must run with the normal authenticated app session

Choose the smallest robust architecture that lets the normal TNR Clerk runtime establish/refresh the signed-in session before Forge sends protected tRPC calls.

Preferred design direction, unless source/testing reveals a better one:

- `/forge` remains a lightweight entry/redirect;
- Forge activates on a valid TNR application route under the normal root provider tree;
- do **not** destroy/unmount the Clerk provider required to maintain auth;
- hide or visually cover the carrier page rather than replacing the provider tree if necessary;
- mount Forge after the auth/runtime readiness condition is satisfied;
- keep game requests same-origin.

Fable may choose the specific carrier route after inspecting pinned/current source. Prefer a low-side-effect, stable route over a gameplay-heavy page. Record the chosen route and why.

### C. No credential extraction or bearer-token workaround

Forbidden:

- reading/copying `__session` or other Clerk cookies into JS state;
- calling `document.cookie` to obtain auth material;
- extracting a Clerk session JWT/token and adding `Authorization` headers;
- storing auth material in localStorage, IndexedDB, Forge journals, captures, logs, GitHub results, or manifests;
- adding a new user-entered credential field;
- weakening `CookieSession`'s game-request header allowlist to permit arbitrary auth headers.

Forge should benefit from the browser/app's established authenticated context, not become a credential manager.

### D. Explicit auth-health UX

Forge must distinguish authentication failure from ordinary read/capture failure.

At minimum:

- when Forge knows the app session is signed out/not ready, protected work must be blocked before any protected mutation is sent;
- UI must say that TNR authentication is unavailable and tell the operator to sign in/refresh the authenticated host context;
- a server `UNAUTHORIZED` from a protected procedure must surface as an auth/session problem, not merely `read failed` / `0 bodies persisted`;
- public read-only manifests may still run when signed out if the existing contract allows them;
- no auth failure may be presented as a successful capture/job.

Do not persist the response body of any auth-health check. Do not add a sensitive user-profile capture merely to test auth.

### E. Protected-write safety

This repair must cover mutations too, not only `profile.getAi`.

- If auth is known unavailable, do not send a protected mutation.
- If a protected mutation is sent and receives a clean server `UNAUTHORIZED` refusal, treat it as a failed/refused item, not an ambiguous write.
- Existing SENT/reconciliation semantics for network/transport ambiguity must remain unchanged.
- Do not add automatic mutation retry.

### F. Preserve Forge contracts

Do not regress:

- immutable full-capture snapshots and `persist: "full"` fail-closed boundary;
- zero-mutation capture-only jobs;
- write-ahead journal / SENT semantics;
- reconciliation;
- budget/rate-limit handling;
- image upload path;
- GitHub sync;
- release-pin workflow and immutable loader `@require`;
- mobile layout/touch usability.

## Tests required

All implementation tests are socket-free / no live-game requests.

Add targeted tests that prove at least:

1. `/forge` entry reaches the authenticated-host Forge mode without requiring a manually different URL.
2. Forge does not boot its protected-operation mode before auth/runtime readiness.
3. signed-out/not-ready state blocks protected mutations before transport send.
4. public capture-only work remains possible without auth where procedure guards allow it.
5. `UNAUTHORIZED` on a protected query is classified/presented as auth failure.
6. `UNAUTHORIZED` on a protected mutation is a clean refusal and never enters ambiguous SENT/retry behaviour.
7. no cookie/token/auth value is copied into persistent storage or result exports.
8. the selected carrier-page strategy leaves the provider/auth runtime alive while Forge is mounted.
9. existing full-capture tests remain green.
10. loader release tests cover any changed `@match`, activation-marker, redirect, or run-at behaviour.

Use mocks/fakes for Clerk/runtime readiness. Do not require Clerk packages unless the chosen implementation actually needs them; avoid adding a dependency solely for tests if a small fake interface proves the seam.

## Required gates

From `forge/` run and report exact results for:

- `npm test`
- `npm run build`
- `npm run fixtures` if transport/envelope fixtures are affected
- a fresh build-equivalence check showing checked-in `forge_bundle.js` matches the source build

Run any additional static/grep safety checks needed to prove no credential extraction/storage path was introduced.

If loader metadata changes, ensure release-loader tests and release-pin expectations remain correct. Stage the next package/version in the existing release model; do not bypass `.github/workflows/release_pin.yml`.

## Browser/live verification boundary

Implementation and ChatGPT review are zero-live-request.

Fable must state which behaviour is only locally simulated. After independent review and integration, dauntless performs the live smoke test.

The first live smoke after release should be **read-only**:

- reload Forge through the normal `/forge` entry;
- run `push/04_one_perfect_crop_bandit_ai_probe.json`;
- expected: 5/5 `profile.getAi` reads succeed and 5/5 full bodies persist; zero mutations.

Only after that read-only smoke succeeds should One Perfect Crop continue toward protected content writes.

## Scope boundary

In scope:

- Forge boot/host/session/auth-readiness mechanics;
- transport/error classification only where needed for auth semantics;
- operator auth-state UI;
- tests/build/release metadata required by the repair.

Out of scope:

- One Perfect Crop content/AI/art implementation itself;
- changing TNR game source;
- introducing OAuth/MCP as a replacement transport;
- storing/exposing credentials;
- general Forge redesign;
- unrelated refactors;
- law/doctrine rewrites.

## Handoff

Implement on a Fable-owned Lane A branch, e.g. `fable/forge-protected-auth`.

Return the standard exact-SHA handoff from `docs/workflows/IMPLEMENTATION_HANDOFF.md`, including:

- exact base and frozen head;
- changed files;
- architecture chosen for authenticated host context and why;
- exact tests/builds/gates;
- evidence that no credential material is read or persisted;
- release version/pin status;
- known deviations/debt;
- browser/live behaviours not tested;
- explicit statement that no live request/write/credential material was used.

Freeze the handoff SHA until ChatGPT's independent review returns.
