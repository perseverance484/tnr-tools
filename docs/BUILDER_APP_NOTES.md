# Builder app (forge): implementation notes

Branch `builder-app`, built against `docs/PLAN_2026-09-03_builder_app.md` and the client
contract on branches `client-contract-audit` / `client-contract-verification` (verification
wins). Every engine fact is pinned to `studie-tech/TheNinjaRPG@345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9`.

Nothing here has been run against the game. Zero live requests were made while building it.
Every behaviour is verified against recorded or adapter-derived fixtures; see "Verification".

## Layout

```
forge/                       the app, one directory per layer (brief section 3 order)
  src/storage/               L1 journal (localStorage), capture cache (IndexedDB), retained keys
  src/transport/             L2 superjson + tRPC 11 envelope, session seam, outcome, procedures, upload
  src/budget/                L3 per-path sliding window at a margin, cache-first reader
  src/runner/                L4 manifest plan, refs, pre-send validation, recipes, the runner
  src/reconcile/             L5 snapshots, orphan diff, adoption policy
  src/ui/                    L6 five screens, takeover, DOM helpers (createElement + CSSOM only)
  src/github.mjs             L7 manifest picker's contents-API client (bearer to api.github.com only)
  src/main.mjs               composition root; the only file that touches window.*
  tools/derive_envelope.mjs  produces test/fixtures/envelope/ by running the real tRPC adapter
  test/                      node --test, no network; shim.mjs, fakegame.mjs
  build.mjs                  esbuild IIFE -> ../forge_bundle.js
forge_bundle.js              the built userscript body (repo root, beside builder_bundle.js)
forge_loader_user.js         the ViolentMonkey loader (distinct name, namespace, @match, version)
```

Run tests: `cd forge && npm test`. Build: `cd forge && npm run build`. Regenerate the wire
fixtures: `npm run fixtures`. Dependencies are pinned in `forge/package.json`: `superjson 2.2.6`
(bundled), and dev-only `@trpc/client`/`@trpc/server 11.18.0`, `zod 4.4.3`, `uploadthing 7.7.4`
(read for protocol, not bundled), `esbuild`, `fake-indexeddb`, `jsdom`. Bundle version is
`package.json` `version` (banner line 1 of `forge_bundle.js`, and `VERSION` in `main.mjs`).

## Host path: `/forge`, and why

Any unmatched URL on the game origin. Three facts at source decide it:

- `app/next.config.mjs:21` sets `experimental.globalNotFound: true`.
- `app/src/proxy.ts` matcher comment: "URLs with no matching route render through
  global-not-found.tsx without the Clerk-dependent root layout". The middleware body returns
  immediately for every pathname other than `/` (`if (pathname !== "/") return;`), so it
  neither calls `auth()` nor redirects for `/forge`.
- `app/src/app/global-not-found.tsx` is a bare `<html><body>` with one `Link` and
  `globals.css`: no `ClerkProvider`, no `TrpcClientProvider`, no fetch on mount.

So the host page makes no game requests, mounts no React tree the app would have to
co-exist with, and the Clerk session cookie is still first-party for `/api/trpc`. The
loader matches `*://www.theninja-rpg.com/forge*` and the bare host, runs at
`document-start`, calls `window.stop()`, empties the document, and mounts the app. The
site's router never mounts on this path, so there is nothing to re-mount over the app.

The old loader matches the whole origin at `document-idle` and would append its panel to
this document too; `takeover.mjs` removes its root nodes (`.k-fab`, `.k-pn`) on arrival so
both scripts can stay installed. Retired deliberately, not by accident.

**Open risk, INFERRED, not verified (adversarial L2):** Clerk's `__session` cookie is a
short-lived JWT that `clerk-js` refreshes from the page. `global-not-found.tsx` does not load
`ClerkProvider`, and the takeover stops the document anyway, so nothing on `/forge` refreshes
it. If the JWT expires mid-job, the next request answers `UNAUTHORIZED` and the job pauses
with reason `SESSION`; nothing is lost, because every send is journaled, but a long job may
pause repeatedly until the user opens a game tab. A same-origin hidden iframe of a cheap game
page would keep `clerk-js` refreshing; it was considered and not built, because it would be
a second document making game requests the budget cannot see. Decide after the first live run.

## Journal schema (v1)

One localStorage key per job: `tnr_forge_job_v1:<jobId>`. The job list is derived by
scanning keys with that prefix; there is no separate index that can disagree with the jobs.

```
job  = { v: 1, jobId, manifestPath, manifestNumber, manifestHash, startedAt, updatedAt,
         state: RUNNING | PAUSED | DONE | ABORTED,
         pause: null | { reason, path, until, idx, detail, httpStatus },
         capturesBefore?, capturesBeforePartial?, capturesAfter?, capturesAfterPartial?, items[] }
item = { idx, entity, op: create | update, name, srcId, targetId, payloadHash,
         state: PLANNED | SENT | CONFIRMED | VERIFIED | FAILED | ORPHANED | SKIPPED,
         phase: create | update | rules-toggle | rules | verify,
         entityId, snapshotKey, aiProfileId?, sentAt, createSentAt, confirmedAt, verifiedAt,
         error, diffs?, verify?: match | drift | unread, candidates?, reconciled?, adopted? }
```

Pause reasons: `TOO_MANY_REQUESTS` (path + `until`), `SESSION`, `NETWORK` (a read failed on
the wire, or a send failed before any response), `UNDECODABLE_RESPONSE` (a send got a body
that is not the audited envelope), `AMBIGUOUS` (a bug inside a send), `USER`, `ORPHANED`
(an item is waiting for adopt or skip; nothing after it is sent until then).

Legal transitions are a table in `journal.mjs`; `SENT -> PLANNED` is absent from it, which
makes "never retry a SENT create" structural rather than a runner discipline. `CONFIRMED ->
SENT` exists only for the later phases of one item and requires an `entityId` and a phase
other than `create`. `SENT` is refused unless the job is `RUNNING`. `withSent(jobId, idx,
patch, thunk)` flushes SENT synchronously, yields one macrotask (so the storage checkpoint is
queued before the fetch is issued), and only then runs the thunk; if the flush throws, the
thunk never runs. `sentAt` is the latest send; `createSentAt` is set once and never
overwritten. The phase recorded on `CONFIRMED` is the NEXT step, so an item whose update has
succeeded is at `verify` and a later run can only read it back, never re-send it.

Guards added by the adversarial pass: `annotate()` and `transition()` patches may not set
`state`, `idx` or any timestamp; `remove()` refuses a job holding a SENT item unless forced;
`setJobState(DONE)` refuses while an item is SENT; `open()` refuses empty item lists and a
second resumable job for the same `manifestHash`; error strings are capped at 512 chars;
`migrate()` refuses a newer or non-integer version; one corrupt record no longer blocks
`listJobs()`, `resumable()` or the export (it is collected in `journal.broken` and exported
raw). `knownEntityIds(entity)` lists every id any job recorded, which reconciliation uses.
`exportText()` returns the whole journal as JSON text (Settings > Export).

Other keys: `tnr_forge_sendlog_v1` (budget send log), `tnr_forge_snap_v1:<jobId>:<entity>`
(pre-create id snapshots, removed when the job is DONE). Retained unchanged from the old
builder: `tnr_bk_idmap_v1` (srcId -> id, image name -> url) and `tnr_bk_gh_v1` ({on, pat}).
A corrupt retained key is parked under `<key>.corrupt` before the fallback is written.
Capture cache: IndexedDB `tnr_forge` / `captures`, keyed `path:id` (ids normalised to
strings), entity index; the connection is memoised, reopened on `close`/`InvalidStateError`.

## Budget margin: 0.5, and why

Server: `Ratelimit.slidingWindow(60, "60 s")` keyed `${path}-${userId}` on `publicProcedure`
only (`trpc.ts:123`, `:148`, `:211`); a trip increments `movedTooFastCount`, multiplies money
and bank by 0.99, and throws `TOO_MANY_REQUESTS` (`:166-179`). Production fails closed. The
route handler deliberately does not log the trip. Mutations are `protectedProcedure` and
unlimited; no content mutation composes a limiter at its call site (verification F2).

The local allowance is `floor(60 * 0.5) = 30` per limited path per minute, because:

1. The window is per (path, user) and shared with every other tab the user has open; the
   game's own pages call the same `getAllNames`/`get` reads on mount. The client cannot see
   that traffic. Half the window is left for it.
2. Upstash's sliding window is an approximation (weighted previous window); a strict local
   count can disagree with it by a few requests near the boundary.
3. The cost asymmetry: a trip is a permanent 1% of money and bank plus a logged incident;
   under-spending costs seconds.

The send log is written to localStorage BEFORE `acquire()` resolves, so a restart inside the
window cannot overspend. `acquire()` waits (never fails). A server 429 at ANY batch index
persists a trip marker for the full 60 s and every limited send refuses until it passes; the
job is PAUSED with the path and a countdown. There is no retry path in the codebase. The
margin is a constructor argument (`Budget({ margin })`) and shown on Settings.

Batch elements on a limited path count one each against the window, and at the limiter edge
each element over the limit is a separate 1% penalty. So on limited paths a request carries
at most 10 elements and never more than the window has room for right now; with no room it
waits for a full chunk. Unlimited paths batch up to 20. `reader.list()` only accepts the
name-list procedures; `getAll` takes a required `{limit, cursor}` and is not used.

Limited paths (16, all `publicProcedure` reads): `jutsu|item|quests|gameAsset|bloodline .get
/ .getAll / .getAllNames`, `profile.getAllAiNames`. Not limited: `profile.getAi`,
`ai.getAiProfile`, every mutation. Table: `src/transport/procedures.mjs`, generated from the
audit's `crud_surface` with the verification's F4 corrections applied.

## Transport, derived from the adapter

`tools/derive_envelope.mjs` runs the real `@trpc/client` `httpBatchLink` (superjson) against
the real `@trpc/server` `fetchRequestHandler` with a recording fetch that never leaves the
process, and writes eleven exchanges to `test/fixtures/envelope/`. `envelope.mjs` is
asserted against them byte for byte. Observed and relied on:

- `?batch=1` always; queries GET with url-encoded `input`, mutations POST JSON; response is
  an array indexed by batch position, except that a request-level adapter error (bad
  envelope, unsupported media type, oversized body) is a bare `{error:{json}}` object; it is
  decoded once and replicated across the indices with `requestLevel: true`.
- An undefined input serialises as `{"json":null,"meta":{"values":["undefined"],"v":1}}`.
- Status rule: a single-element batch carries its own status; any mixed batch is **207**. A
  429 can sit at one index of a 207 while another index succeeded. Outcome is read per index
  and the status is never consulted for a verdict (spec section 8).
- Error elements carry `data.code`, `data.httpStatus`, `data.path`, `data.zodError` (issues
  array or null). `readCreate` refuses a `success:true` whose message is not nanoid-shaped.
  One malformed element becomes `{code: "MALFORMED_ELEMENT"}` at its index; its siblings
  are kept.
- A GET on a mutation path is 405 `METHOD_NOT_SUPPORTED` before any resolver runs.
- `NOT_FOUND` is split by message: the adapter's "No procedure found on path" is a client
  bug; the route handler's "Please complete registration." is a session problem; anything
  else is a real not-found. `INTERNAL_SERVER_ERROR` "Output validation failed" is a server
  contract break, never retried.
- Batch elements execute concurrently server-side; `batch()` is for latency only and the
  runner never batches dependent mutations (it sends one mutation per request).

Failure shapes the runner keys off: `NetworkError` carries `phase: connect | body`,
`causeName`, `httpStatus` and `received`, so "the request never left" and "a status came
back but the body did not" are distinguishable; on a mid-batch failure the decoded results
of earlier chunks ride on the error. A response that is not the audited envelope is a
`TransportError` enriched with `paths`, `kind`, `httpStatus`, `redirected`, `url`,
`contentType` and `looksLikeLogin`. A refusal inside the session (nothing left the device)
is `SessionRefused`, reported as `TransportError{sent:false}`, never as ambiguous.

`CookieSession` sends `credentials: "same-origin"`, only issues same-origin `/api/trpc/` and
`/api/uploadthing` requests, and builds the outgoing headers from an allowlist
(`content-type`, `x-uploadthing-version`, `accept`), so no `Authorization` header can leave
by construction. `fetchImpl` is wrapped receiver-free (`window.fetch` as a method of
another object throws "Illegal invocation"). The GitHub bearer lives in `github.mjs` and is
sent to `api.github.com` only. The native shell or a bearer session is a new `Session`
implementation plus configuration (brief section 6).

## Two-phase creates: six, not four

Spec section 5 lists four. At source there are six, all the same shape: no payload
(`item.create` takes `{type}`), placeholder row, id in `message`:

| procedure | placeholder | id in name |
|---|---|---|
| `jutsu.create` (jutsu.ts:391) | `New Jutsu - ${id}` | yes |
| `item.create` (item.ts:235) | `New Item - ${id}` | yes |
| `bloodline.create` (bloodline.ts:144) | `New Bloodline - ${id}` | yes |
| `gameAsset.create` (asset.ts:194) | `Placeholder` | **no** |
| `quests.create` (quests.ts:866) | `New Quest - ${id}` | yes |
| `profile.create` (profile.ts:1138) | username `New AI - ${id}` | yes |

Reconciliation covers all six. `profile.getAllAiNames` keys on `userId`/`username`, not
`id`/`name`, and `profile.getAi` takes `{userId}`; the recipes carry those per entity.

Everything that can fail locally fails BEFORE the placeholder is created: ref resolvability,
`@img` file presence, unknown keys. A read that fails on the wire between create and update
pauses the job with the item still `CONFIRMED`; it is never marked FAILED with a live
placeholder behind it.

## Reconciliation rules that the adversarial pass tightened

- A candidate row is never one that any item of any job in the journal already holds
  (`knownEntityIds`), so cross-job adoption cannot overwrite another job's row.
- An update is "already landed" only when every asserted key compares equal after refs are
  resolved the way the runner resolves them; an unresolvable ref or zero comparable keys is
  an orphan ("cannot compare"), never a confirm.
- The AI kit (`jutsus`, `items`) is compared by id against the live relation rows, so a lost
  `updateAi` cannot pass as landed.
- A reconciled rules-toggle continues at `rules`; a reconciled update continues at `verify`.
  Neither re-enters the update phase.
- `adopt()` requires an ORPHANED item, refuses an id another item holds, and keeps a
  non-create phase (the UI says which step adopting will send).
- A job with an ORPHANED item pauses at that item; the items after it are not started.

## Pre-send validation and the 45g power bound

Unknown keys are refused locally against the 45d field lists for jutsu, item, bloodline,
quest and gameAsset. The AI record has no 45d entity (`insertAiSchema` is the whole
`userData` table), so AI keys are checked against the live record fetched before the write
plus the schema's extension keys (`jutsus`, `items`, `primaryElement`, `secondaryElement`,
`rules`, `includeDefaultRules`); before the create only the structural checks run.

**The 45g power bound is gated out, not fixed.** Brief section 5 offered two options; this is
the second. `validate.mjs` does not load `45g_DATA_checks.json` at all, and the header comment
there points at the brief. Reason: `PowerAttributes.power` is `z.coerce.number().min(0)` with
no maximum (`combat.ts:111`) and is spread after `BaseAttributes` in all 61 tags that use it;
`45g.tag_power_max` asserts 100 because `schema_extract.py` does not handle spread
precedence. A test asserts that `power: 400` on a damage tag is accepted by the runner.
Fixing the generator is a separate change to `skills/`, which this branch does not touch.

Merge for update picks the validator's field set from live ∪ asserted, so relation objects
(`bloodline` on a jutsu row, `jutsus`/`items` rows on an AI) and server-owned columns never
reach the validator. For AI, the live kit is always re-sent reshaped (`jutsuId[]`,
`[{ids:[itemId], number}]`) because `updateAi` syncs by set difference against
`input.data.jutsus ?? []` (profile.ts:1529-1541): omitting the arrays deletes the kit (law 70).

## Things the old bundle did that this one does not

- Hand-built superjson `meta.values` / `referentialEqualities` (the `AIDATE`/`QRE` tables):
  the real library does it.
- Regex over raw response text for the new id: `message` on the decoded envelope.
- Eight-try exponential backoff on 429: a halt.
- Hoisting `content.reward.*` to top-level `reward_*` on quest updates: `QuestValidator` has
  no top-level reward fields (45d quest field list), so those keys were silently stripped.
  Not carried.
- `gameAsset.get` retried with a raw string input (audit D5): removed; the input is `{id}`.
- Computing the upload URL as `https://<id>.ufs.sh/f/<key>` by hand: `ufsUrl` is read from
  the PUT response, as the uploadthing client does.
- `resolvePool` (pool codes -> ids and distance gates) and the L09-L22 lint set: **not
  ported** (see "Not finished").

## Placeholders carried (balance, reserved for dauntless)

None are hard-coded in `forge/`. The app carries no drop rates, reward values, stat numbers
or difficulty gates; those live in manifests. Two values that are policy rather than
balance, and are shown in the UI as settings: the budget margin (0.5) and the batch sizes
(20 per request on unlimited paths, 10 on limited ones, under the route handler's
`maxDuration = 90`).

## Verification

`cd forge && npm test`. No test opens a socket. 151 tests.

| layer | tests | what is proven |
|---|---:|---|
| storage | 24 | write-ahead ordering, the four mandated evictions, SENT->PLANNED impossible, IDB invalidation |
| transport | 39 | every recorded request reproduced byte for byte; every recorded response decoded to what the real client decoded |
| budget | 16 | write-ahead send log, window survives eviction, 31st send waits, a 429 in a 207 halts after caching the good index |
| runner + reconcile | 28 | two-phase creates, six entities, kit re-send, refs, unknown-key refusal, power uncapped, crash before send / after send / after response / mid two-phase against server-side row counts, gameAsset two-orphan ambiguity, TOO_MANY_REQUESTS pause, NetworkError leaves SENT |
| ui | 8 | no HTML string sink in src, takeover, five screens render, resume banner, run screen, settings persist, picker -> start -> DONE, render errors surface |
| adversarial | 36 | one regression test per finding that survived the panels (below) |

### Adversarial passes

Three independent skeptic panels ran against the code (attackers, then refuters per
finding, scratch tests under a gitignored directory; only what reproduced was kept):

- **L1 storage (11 attacks, 5 verified):** `annotate()` could set `state` (SENT -> PLANNED in
  one call); `CONFIRMED -> SENT` had no phase or id guard; `migrate()` passed a newer version
  through and `_write()` downgraded it; one corrupt key blocked every list and the export;
  `remove()` deleted a job holding a SENT item; `open()` accepted a second job for the same
  manifest; phase-2 SENT overwrote the create's timestamp; hash blind spots (`undefined`,
  `Date`); IndexedDB open had no in-flight guard and cached a dead connection. All fixed and
  pinned. Refuted and left alone: requiring evidence on `SENT -> FAILED` (the runner never
  takes that edge on an indeterminate failure), an `ORPHANED -> PLANNED` re-plan edge (an
  orphan that never landed is skipped and re-planned as a new job, auditable), per-item keys
  and a revision stamp (single writer per tab; not worth the schema change).
- **L2 transport (6 attacks, 6 verdicts):** `fetchImpl` called as a method (Illegal
  invocation in a browser); no origin pin on the session; request-level adapter errors are a
  bare object; a mid-batch failure discarded earlier chunks' results; connect and body
  failures were indistinguishable; an HTML login page came back as a bare "not JSON"; a
  session refusal was reported as a network failure; `NOT_FOUND` collapsed three meanings;
  one malformed element discarded its siblings; a single oversize GET was sent anyway;
  `maxBatch` was unvalidated. All fixed and pinned. Refuted: `readCreate` rejecting
  `ai.createAiProfile` (that procedure is never read through `readCreate`; the toggle is
  read as a plain mutation).
- **L3-5 budget/runner/reconcile (16 attacks):** the ones that mattered were all
  "re-send after a pause": a 429 on an item's own read-back, `readBack:false`, verify drift
  and a reconciled rules-toggle each left the item at a phase from which a later run
  re-sent the update. Fixed at the root by recording the NEXT step on `CONFIRMED`, and pinned
  four ways. Also fixed: pre-send validation ran after the create; a transient read failure
  between create and update marked the item FAILED; cross-job adoption; ref-blind update
  comparison; the AI kit never read back; the crash between CONFIRMED and the idmap write
  stranding a dependent `@ref`; `adopt()` with no state or uniqueness guard; a capture-pass
  failure escaping `run()` as a crash; a job with an ORPHANED item marked DONE.

## Not finished

- **Pause during a run** is wired (`Runner.requestPause()`, honoured between items; the Run
  screen button calls it) but only jsdom has exercised the button.
- **Captures with `select` / `scope`.** The old bundle's capture entries carried a `select`
  field list; the runner records row counts and stores full decoded data in the capture
  cache but does not trim to `select`.
- **Pool-code resolution and the lint set** (`resolvePool`, L09-L22) from builder v4.32 are
  not ported. Manifests that still carry pool codes will fail pre-send validation only if
  the code lands in an unknown key; a pool code in a legal field would be sent as a literal.
  Port before running any AI-kit manifest through forge.
- **`dedupNames` (live name collision check)** is parsed but not enforced.
- **Verify `unread`** (the read-back itself failed) leaves the item CONFIRMED at `verify`;
  each later run re-reads it (one limited token) and the job can finish DONE with it in
  that state. It is visible on the Run screen, not terminal.
- **Clerk session refresh on `/forge`** (see "Host path"): inferred risk, mitigated by the
  SESSION pause, not solved.
- **The loader `@require` points at the branch**, not a commit. `release_pin.yml` is
  paths-filtered to `builder_bundle.js`; extending it to `forge_bundle.js` is a workflow
  edit (web UI install) and is not done here.
- **Not exercised in a browser.** jsdom covers rendering and wiring; Firefox Android,
  ViolentMonkey's `@run-at document-start` timing on a 404 response, `window.stop()`
  behaviour, and `navigator.storage.persist()` prompts are unverified until dauntless
  installs it.
