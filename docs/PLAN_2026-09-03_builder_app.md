# Builder app design spec

Working name `forge` (placeholder; rename freely). Replaces the injected ViolentMonkey
panel with a full-page same-origin application.

Drafted 2026-09-03. Every engine fact below is anchored to
`studie-tech/TheNinjaRPG@345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9` and was verified either
in `reports/client_contract.json` (branch `client-contract-audit`) or in
`reports/client_contract_verification.md` (branch `client-contract-verification`). Where the
two disagree, the verification wins and is marked.

## 1. What changes and what does not

Stays: ViolentMonkey on Firefox Android, same-origin cookie session, `/api/trpc`, results
auto-committed to `harvests/inbox/`, dauntless initiating every game write.

Changes: a full-viewport GUI instead of a panel; durable job state across tab eviction; a
cache-first read layer under the rate limiter; correct superjson transport; pre-send
validation; ids read from the response envelope instead of scraped.

Explicit non-goal: eliminating tab eviction. A userscript cannot. The goal is that eviction
costs nothing but the seconds already elapsed. A native shell later removes it for real, and
this codebase is meant to wrap unchanged.

## 2. Host page and takeover

The app needs a same-origin document and nothing else from the page it lands on.

- Match `www.theninja-rpg.com` and the bare host, on a path chosen for being cheap and
  inert. A path with no server-side data dependency is preferred over any live game page.
- At `document-start`, take over the document: build the UI with `createElement` and CSSOM
  only, never `innerHTML` (repo law). Do not attempt to co-exist with the site's own React
  tree; replace it.
- Record the chosen path and the reason in the implementation notes. If the site's router
  re-mounts over the app, that is a defect to solve, not to work around with timers.

## 3. Storage model

Two stores, chosen for different reasons.

**`localStorage` — the journal.** Writes are synchronous, so a record committed before a
fetch is on disk before the request leaves. IndexedDB is asynchronous and can lose the write
in exactly the eviction window that matters. This is the reason for the split; do not
"upgrade" the journal to IndexedDB.

**IndexedDB — the capture cache.** Captures exceed the localStorage quota. DB `tnr_forge`,
store `captures`.

Existing keys `tnr_bk_idmap_v1` and the GitHub PAT key are retained as-is.

## 4. The journal

A run is a job; a job is an ordered list of items.

```
job   = { jobId, manifestPath, manifestNumber, startedAt, state, items[] }
item  = { idx, entity, op, payloadHash, state, entityId, snapshotKey,
          sentAt, confirmedAt, verifiedAt, error }
```

Item states: `PLANNED` → `SENT` → `CONFIRMED` → `VERIFIED`, plus `FAILED`, `ORPHANED`,
`SKIPPED`.

**Write-ahead rule.** An item transitions to `SENT` and the journal is flushed *before* the
fetch is issued, never after the response. Without this, a crash mid-flight is
indistinguishable from a request that never left, and creates are not idempotent.

**Resume rule.** On boot, any job with non-terminal items is resumable. Items in `SENT` are
ambiguous and are **never retried**. They are reconciled (section 5).

## 5. Create semantics and orphan reconciliation

Verified at source. `create` accepts no meaningful payload, inserts a placeholder row, and
returns the new id inside `baseServerResponse.message`:

| Procedure | Placeholder name | Id in name |
|---|---|---|
| `jutsu.create` | `New Jutsu - ${id}` | yes |
| `item.create` | `New Item - ${id}` | yes |
| `bloodline.create` | `New Bloodline - ${id}` | yes |
| `asset.create` | `Placeholder` | **no** |

`item.create` alone takes an input, `{ type: ItemTypes }`.

So every create is two-phase: `create` yields an id for a live but wrong row, and the record
is not correct until the follow-up `update` lands. A crash between them leaves a real
placeholder in the game.

**Reconciliation, uniform across all four types.** Before the first create of a given entity
type in a job, snapshot the current set of placeholder ids for that type via `getAllNames`
and store it in the journal under `snapshotKey`. On resume, re-fetch and diff. Ids present
now and absent from the snapshot were created by the crashed run.

For jutsu, item and bloodline the id embedded in the name is an independent cross-check on
the diff. For `gameAsset` the diff is the *only* signal, because every orphan is named
`Placeholder`. That asymmetry is why the snapshot is mandatory rather than a nicety.

**Adoption policy.** Adopt automatically only when the match is unambiguous: exactly one new
id, exactly one item in `SENT` for that entity type. Adopted items become `CONFIRMED` and the
job continues at the `update` step. Anything ambiguous is listed in an orphans panel with
adopt / ignore actions surfaced to dauntless. **Nothing is ever deleted automatically.**

## 6. Read layer and the rate limiter

Corrects the audit. Reads, not writes, are the limited surface.

- `publicProcedure` is `t.procedure.use(ratelimitMiddleware)` (`trpc.ts:211`). The read paths
  the builder uses — `get`, `getAll`, `getAllNames` on jutsu, item, quests, gameAsset,
  bloodline — are all `publicProcedure`.
- `protectedProcedure` (`trpc.ts:230`) carries no limiter, and no content mutation adds one
  at its call site (verified across all seven content routers). **But `item.splitStack`
  proves a limiter can be composed per procedure, so limiting is a per-procedure fact and is
  never inferred from the base builder.**
- Limit: 60 per 60s sliding, keyed `${path}-${userId}`. A trip increments `movedTooFastCount`,
  multiplies **money and bank by 0.99**, and throws `TOO_MANY_REQUESTS`. Production fails
  closed. The route handler deliberately does not log it, so it debits silently.

Requirements:

1. **Cache first.** Captures keyed `path:id`, invalidated on any write to that entity.
2. **Token bucket per procedure path**, at a deliberate safety margin below 60/60s, because
   the window is shared with any other tab the user has open on the game.
3. **Never retry a 429.** Replace the current eight-try exponential backoff outright: on
   `TOO_MANY_REQUESTS`, stop the job, mark it `PAUSED`, show the offending path and a
   countdown. Each retry debits again; the existing backoff can cost ~7.7% of money and bank.
4. **Batch for latency, not for budget.** Middleware runs per procedure, so a batch of forty
   `jutsu.get` costs forty tokens. Batching still pays: `withRequestScope` shares one memo
   across every procedure in an HTTP request. Respect `maxDuration = 90` per request.

## 7. Transport

- **superjson both directions.** Configured at `trpc.ts:89` and matched client-side. Use the
  real library rather than hand-building `meta.values` and `referentialEqualities`. This
  deletes the `AIDATE` / `QRE` date tables and the null-strip bug behind law 72.
- Derive the batch envelope from the tRPC 11 fetch adapter, **not** from the existing bundle.
- Mutations must be POST; a GET on a mutation path is rejected as `METHOD_NOT_SUPPORTED`
  before any resolver runs.
- Game requests carry `credentials: 'same-origin'` and no `Authorization` header. The bearer
  header is for `api.github.com` only. Two separate auth paths; do not merge them.

## 8. Outcome reading

- The verdict is `baseServerResponse.success` on the decoded body. **Never infer outcome from
  HTTP status**: a role miss returns HTTP 200 with `success:false`.
- On create, `message` carries the id. Read it from the decoded envelope; do not regex the raw
  response text as the current bundle does at `builder_bundle.js:509`.
- Verify by reading back through the entity's `get` and diffing **only the keys the manifest
  asserted**. The `get` shape matches neither `create` nor `update`, so a whole-record diff is
  noise.

## 9. Pre-send validation

Every content validator is non-strict; `.strict()` appears once in the codebase, on an
unrelated travel validator. An unknown or misspelled key is dropped at `.input()` parse time
with no error and the mutation reports success. **Client-side refusal before the send is the
only place that error can ever surface.**

Dependency, and it is real: `45g.tag_power_max` is wrong at the generator. `PowerAttributes.power`
is `z.coerce.number().min(0)` with no maximum and is spread *after* `BaseAttributes` in all 61
tags using it; `schema_extract.py` does not handle spread precedence, so `45g` asserts a cap of
100 that source does not impose, and `validate.py:769-770` rejects payloads the server accepts.
Validating against `45g` as it stands would bake that defect into the new client. **Fix the
generator before wiring validation, or gate the power bound until it is fixed.**

## 10. Manifest picker

Fetch the `push/` listing through the GitHub contents API with the stored PAT. For each entry
show filename, the manifest's own number, its title, item count, and whether the journal has
seen it run. Search box; tap to select. No positional index, and nothing the user has to type.

## 11. Screens

1. **Jobs** — resume banner if a job is open, recent runs, orphans needing a decision.
2. **Manifests** — the picker above; selecting one shows its parsed items before any send.
3. **Run** — per-item state, live budget per path, pause and resume, and the current phase of
   any two-phase create.
4. **Captures** — cache contents, age, manual invalidate.
5. **Settings** — PAT, sync toggle, cache size, journal export.

## 12. Invariants

- Everything ships `hidden: true`. Publishing is dauntless's, after admin go-ahead.
- No automated game writes. The app acts only when dauntless starts a job.
- No deletions, ever, without an explicit per-item confirmation.
- Balance values stay placeholders and are listed in the delivery summary.
- DOM via `createElement` and CSSOM only.
- Validate every manifest at zero errors before it can be run.

## 13. Later: the native shell

Not in scope now. The shell adds exactly two things: builds that continue while the user is
in another app, and no eviction. It gets them by holding the Clerk session in an offscreen
WebView, lifting the cookie into native networking via Android `CookieManager`, and rendering
this same app on top. If TNR's developers enable `mcp.enabled` on the remaining content
writes, the WebView drops out and a bearer token replaces it. Keep the transport behind one
interface so that swap is configuration, not surgery.
