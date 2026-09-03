# Client contract audit

Source audit of the client-side contract for writing TNR content. Architecture-neutral:
this supplies evidence, and makes no recommendation.

| | |
|---|---|
| Game source | `studie-tech/TheNinjaRPG` |
| **Game SHA scanned** | **`345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9`** |
| Game SHA date | 2026-08-31 (`Stabilize hospital patient ordering`) |
| tnr-tools SHA | `6a1b3ca11168c49cd01aaf3aa023d4a2b6976e31` (branch `main`) |
| Report branch | `client-contract-audit` |
| Live requests made | **0.** No credential requested, used or synthesised. |

Versions read from `app/package.json`: next 16.3.2, @trpc/server 11.18.0, zod ^4.4.3,
drizzle-orm 0.45.2, @clerk/nextjs ^7.8.0, uploadthing 7.7.4, superjson 2.2.6,
@upstash/ratelimit ^2.0.8.

Findings: 65 `ENGINE`, 8 `PARTIAL`, 3 `INFERRED`, 9 `NOT_IN_SOURCE`, 3 `CONTRADICTED`.
Machine-actionable detail is in `reports/client_contract.json` (schema `client-contract/v1`).
Locate every finding by its `match` string; line numbers are valid only at these SHAs.

## Two corrections to the dispatch brief

- `builder_bundle.js` is **885** lines at `6a1b3ca`, not 892.
- The bundle's `Authorization: Bearer` header goes to `api.github.com` only. Game requests
  carry `credentials: 'same-origin'` and no `Authorization` header. Those are two separate
  auth paths, not one.

## Top five findings

**1. A transformer IS configured: superjson.** `app/src/server/api/trpc.ts:89`,
`transformer: superjson`, matched client-side at `_trpc/Provider.tsx:94`. `Date`, `undefined`,
`Map`, `Set` and `BigInt` cross the wire superjson-encoded. The current bundle hand-builds that
envelope (`meta.values`, `referentialEqualities`) rather than delegating, which is the sole
reason it needs per-field date tables at all. This was the brief's flagged high-value question
and the answer is unambiguous.

**2. The tRPC rate limiter does not cover the procedures a builder calls.** `publicProcedure`
uses `ratelimitMiddleware`; `protectedProcedure` (`trpc.ts:213`) does not. All 26 procedures the
bundle calls are `protectedProcedure`. The limiter that does exist is 60 requests per 60 seconds
keyed on `${path}-${userId}` (`trpc.ts:123`, `:148`), and a trip debits **1 percent of money
and bank** (`trpc.ts:164`). Population for the negative half: all 58 router files scanned;
`ratelimitMiddleware` appears outside `trpc.ts` only at `misc.ts:108` and `towerDefense.ts:116`,
`:157`.

**3. `45g.tag_power_max` is wrong at the generator, not just stale.** It asserts a maximum of 100
for `damage`, `heal`, `absorb`, `increasedamagegiven` and the rest. In source those are uncapped:
`PowerAttributes.power` is `z.coerce.number().min(0)` with no max (`validators/combat.ts:111`) and
is spread **after** `BaseAttributes` in all 61 tags that use it, overriding the capped declaration
at `:98`. `schema_extract.py` is not handling spread precedence, so re-pointing it at a newer SHA
will not fix this. It propagates into `validate.py:769-770`, which rejects payloads the server
would accept.

**4. The silent-failure class generalises to one rule.** Across all of `app/src/validators/*.ts`
and `app/drizzle/schema.ts`, `.strict()` appears exactly **once**, on an unrelated travel
validator; `passthrough()` and `strip()` appear nowhere. Every content validator is non-strict, so
an unknown or misspelled key is dropped at `.input()` parse time with no error and the mutation
reports success. There is no single file doing the stripping, which is exactly why it is invisible.
Client-side refusal before the send is the only place that error can ever surface.

**5. A create returns the new id inside `baseServerResponse.message`.** `asset.ts:206`,
`return { success: true, message: id }`. `create` accepts no payload: it inserts a fixed
placeholder row and returns its id (`asset.ts:199` `name: "Placeholder"`; `jutsu.create` inserts
`New Jutsu - ${id}`). So the "blank shell" tnr-tools treats as corruption is simply what create
always produces, visible whenever the follow-up update does not land. A role miss returns HTTP 200
with `success:false` (`asset.ts:208`), so authorization failure and success share a transport shape.

## Feasibility gates

- **G1 Token portability** `ENGINE`. Yes, but only on the MCP route: it verifies a bearer token
  with `@clerk/backend` (`api/mcp/[[...transport]]/route.ts:2`) behind `withMcpAuth`, and is
  env-gated by `NEXT_PUBLIC_MCP_ENABLED` (`:16`). For `/api/trpc` there is no bearer path in source.
- **G2 CORS** `NOT_IN_SOURCE`. No `Access-Control-Allow-*` anywhere. Population: all `.ts`/`.tsx`
  under `app/src` plus `next.config.mjs`; two hits, both unrelated. A browser would block a
  credentialed cross-origin POST; a non-browser client is not subject to CORS at all.
- **G3 CSRF** `NOT_IN_SOURCE`. No CSRF token, double-submit, custom-header requirement, or Origin
  or Referer comparison on mutations. Same population; hits confined to two `samesite=lax` layout
  cookies.
- **G4 Page context** `PARTIAL`. No content procedure needs page state. Context is token, IP,
  user-agent and two A/B layout cookies (`trpc.ts:68`); the same `appRouter` is served over MCP
  with no page state at all.
- **G5 Rate limits** `ENGINE`. 60 per 60s sliding window per procedure path plus identity, on
  `publicProcedure` only, with a 1 percent money and bank penalty on trip and fail-closed in
  production. MCP is stricter and doubly limited: 30 per 60s by IP pre-auth and 30 per 60s per user
  post-auth. Nothing treats batching as abusive per se.
- **G6 Client visibility** `ENGINE`. A `uaMiddleware` returning HTTP 403 "Forbidden. Only access
  through browser" for any unparseable browser string is present in source and **commented out**
  (`proxy.ts:11-21`, call site disabled at `:101-102`). The live crawler regex only pins an A/B
  variant on `/`. `userAgent` is captured into every context and logged, never gated on. No bot
  detection, attestation or fingerprinting is wired in. **Reported as mechanism only; whether a
  non-browser client is sanctioned is not a source question and is out of this audit's remit.**
- **G7 WebView viability** `INFERRED`, and the weakest answer here. No CSP is set anywhere, and the
  tRPC path receives no redirect. Clerk's hosted flow and cookie behaviour are not expressed in this
  repo, so this cannot be settled from source.

## Three highest-severity divergences

**D1 superjson reimplementation** (high). Source configures the transformer; the bundle hand-builds
`meta.values` and `referentialEqualities` at `builder_bundle.js:536`. Every new date-bearing or
nullable field needs a hand-maintained entry, which is why law 72's null-strip bug and the
`AIDATE`/`QRE` tables exist.

**D2 rate-limit machinery on uncovered paths** (high). `postRL`/`getRL` run an eight-try
exponential backoff (`builder_bundle.js:336`) against a limiter that does not gate
`protectedProcedure`. Inert rather than harmful, but it encodes a false model of the server. Note
the correct reading: this says the tRPC middleware does not gate these paths, not that no limiting
exists anywhere. Edge infrastructure in front of Next is outside this repo.

**D3 id extraction by regex** (medium). `rid(c.text)` scrapes the id out of raw response text
(`builder_bundle.js:509`) where `baseServerResponse.message` carries it. Same failure mode as law
29, one layer down.

Also recorded: unknown keys asserted then silently dropped (D4), a `gameAsset.get` retry that can
never validate (D5), and eight delete/clone procedures the client implements none of (D6).

Where the client is correct and worth keeping: zero phantom procedures across all 26 it calls, the
`imageUploader` slug and its 512KB ceiling both match `core.ts:89` exactly, and its rule that
per-entry `success` decides the outcome is the only safe reading of this envelope.

## Not adopted on delivery

Nothing here changes tnr-tools. No law text, manifest, generated file or bundle was edited. The
`redesign_spec` in the JSON is ten dependency-ordered requirements stated as behaviour, usable by a
userscript rewrite or a native shell without favouring either.
