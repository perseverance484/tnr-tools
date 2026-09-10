# Builder app (forge): implementation notes

Built against `docs/PLAN_2026-09-03_builder_app.md` and the client contract on branches
`client-contract-audit` / `client-contract-verification` (verification wins). Every engine fact is
pinned to `studie-tech/TheNinjaRPG@345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9`, and that pin was
re-checked against the current upstream in this pass (see "Source pin: still relevant, and how that
was checked").

Branches: built on `builder-app`; the production-readiness pass
(`state/prompt_builder_app_readiness.md`) continues on
`claude/builder-app-production-readiness-kelsib`, which is `builder-app` with `main` merged in.

Nothing here has been run against the game. Zero live requests were made while building it, and
none while hardening it. Every behaviour is verified against recorded or adapter-derived fixtures
and a local checkout of the pinned source; see "Verification".

## 0.2.1 capture-only repair

The first real Firefox Android smoke exposed one integration seam: `parseManifest()` accepted capture-only manifests, but `Journal.open()` still rejected an empty item list. Forge 0.2.1 permits an empty journal only when `Runner.plan()` has parsed at least one capture, treats the job as successful only when every capture read succeeds, and labels the flow as read-only/zero-mutation in the UI. The smoke manifest is `push/00_forge_readonly_smoke.json`.

## 0.4.0 protected-auth repair

`state/prompt_forge_protected_auth.md`. Protected tRPC reads and writes now run from the browser's
own authenticated Clerk session, because Forge runs inside the running application rather than on
a providerless 404. See "Where Forge runs" and "Auth health" below. No credential is read, copied,
stored or transmitted by any of it.

## 0.3.0 full capture persistence

Built from `state/prompt_forge_full_capture.md`. Before this, `Runner._captures()` journalled only
`{phase, proc, input, ok, rows, error}`, so a bundle could prove a record was read and could not
show what the record said. An asset/content compatibility review therefore had a fresh existence
check plus an older catalog, which is not the same thing as a fresh record.

A capture entry may now carry `"persist": "full"`:

```json
{ "proc": "gameAsset.get", "input": { "id": "..." }, "persist": "full" }
```

Omitted or `"summary"` is the historical behaviour, unchanged, and a manifest written before this
contract keeps the manifest hash it already had, so an open job still resumes. Anything else is a
`ManifestError` before a job is opened.

- **Fail-closed allowlist.** `persist: "full"` is accepted only for the audited content-record
  POINT READS in `FULL_PERSIST_PATHS` (`storage/captures.mjs`): `gameAsset.get`, `jutsu.get`,
  `item.get`, `bloodline.get`, `quests.get`, `profile.getAi`, `ai.getAiProfile`. List procedures,
  mutations, unknown paths (including the un-audited `asset.get` spelling) and a full request with
  no record id are all refused at parse time. The kinds are read from the generated
  `transport/procedures.mjs`; the allowlist names paths and never restates their kind. Widening it
  is a separate reviewed change: the bundle these bodies land in is committed to this repository.
- **One read.** Full mode adds no request; it only decides how durably the body that read already
  returned is kept. Export materializes from IndexedDB and never re-reads.
- **An immutable snapshot per capture occurrence.** `tnr_forge` is now at DB v2 and has a second
  store, `capture_snapshots`, keyed `jobId::phase::ordinal`. `Runner._persistFull()` writes the
  body that read returned there, once, and `App._materialize()` exports from that key.

  The first implementation instead journalled the ordinary read cache key, `path:id`, and was
  rejected in independent review (FFC-1). `path + id` is the identity of a mutable cache slot, not
  of a capture event: the next read of that record replaces the slot and a write to that entity
  deletes it, both correctly. A manifest may legally read a record in `capture.before`, write it,
  and read it again in `capture.after` - so the before entry would have exported the AFTER body
  with `persistOk: true`, which is worse than exporting no body at all. Snapshots are written from
  the response in hand, are never reachable from `invalidateEntity`/`invalidateRecord`/`clear`,
  and are deleted only explicitly: per key, per job (with the job's journal record), or from the
  Captures screen, which lists them apart from the read cache and warns before deleting evidence.
- **The journal stays compact.** localStorage keeps `persist`, the snapshot key, the byte count and
  the persistence verdict, never a body. The `journal` embedded in a results bundle therefore does
  not duplicate the `data` beside it.
- **Fail-closed reporting.** A full capture makes two claims - the read succeeded, and the body is
  in the bundle - and they are reported separately. `App.resolveCaptures()` re-checks every
  requested body against IndexedDB at export and writes `persistOk` / `persistError` back onto the
  job; export may downgrade a success but never overwrites a reason the capture pass already
  recorded, and never upgrades a failure. A snapshot that is gone (an evicted store) or a body over
  `MAX_FULL_CAPTURE_BYTES` (512 KiB; the largest real content record in `harvests/` is a ~71 KB
  quest, and an oversized body is never stored at all) is an explicit failure: `jobOutcome()` turns
  a capture-only job `failed` and a writing job `unverified`, the run screen says "Read-only
  capture incomplete" with the reason, and `harvest.py verify` exits 1. Nothing truncates a body
  and calls it full.
- **Visible before it runs.** The selected-manifest card reads `5 full captures`, not `5 captures`,
  says where the bodies go, and the confirm prompt repeats it. It remains true, and still says,
  that a capture-only job sends zero mutations.

`push/02_one_perfect_crop_asset_probe.json` is the first consumer: five `gameAsset.get` point reads
at `persist: "full"`, `items: []`. It has NOT been run.

The FFC-1 section of `forge/test/capture.full.test.mjs` is where the storage identity is held:
before/write/after on one record exports both bodies; two full reads of one `path + id` keep their
own; a before-only capture survives the job's own write to that entity; the bodies reach neither
localStorage nor the embedded journal; and a snapshot exports intact from persisted state alone
after the tab that made it is gone. Each of those fails against a `path + id`-keyed
implementation.

## The readiness pass, and what it changed

Forge passed its own tests before this pass and was still not safe to make the normal content path.
The eight blockers in the readiness brief, and where each is now:

| blocker | state |
|---|---|
| F4: an undecodable per-index mutation error became a definite failure | closed - `isTrpcErrorBody()` now gates a per-index error too |
| a job with unread/drift verification could finish green | closed - `INCOMPLETE`, and `jobOutcome()` decides what is shown |
| `readBack:false` minted a false `VERIFIED` | closed - refused before a job exists on any manifest that writes |
| pool codes (TNR-01) and the safety lints were not ported | closed - resolved at parse time, with the lint set |
| `dedupNames` was parsed and ignored | closed - enforced through the budgeted reader before the first create |
| unknown NESTED keys were sent and silently stripped | closed - refused from a key surface derived from the pin |
| the source pin's relevance was unproven | proven - nothing forge relies on changed; the pin stays |
| the release floated on a branch | closed in-repo; one workflow install is a dauntless action |

## Layout

```
forge/                       the app, one directory per layer (brief section 3 order)
  src/storage/               L1 journal (localStorage), capture cache (IndexedDB), retained keys
  src/transport/             L2 superjson + tRPC 11 envelope, session seam, outcome, procedures, upload
  src/budget/                L3 per-path sliding window at a margin, cache-first reader
  src/runner/                L4 manifest plan, refs, pre-send validation, recipes, the runner
  src/runner/fields.json     field set per entity, derived from the PINNED validators (see below)
  src/main.mjs compose()     the ONE dependency graph; every test harness calls it
  src/reconcile/             L5 snapshots, orphan diff, adoption policy
  src/ui/                    L6 five screens, takeover, DOM helpers (createElement + CSSOM only)
  src/github.mjs             L7 manifest picker's contents-API client (bearer to api.github.com only)
  src/main.mjs               composition root; the only file that touches window.*
  tools/derive_envelope.mjs  produces test/fixtures/envelope/ by running the real tRPC adapter
  src/runner/pool.mjs        pool-code resolution, the stuck-code guard, kit integrity (laws 18, 40)
  src/runner/lints.mjs       the ported safety lints (L03-L18), errors and advisories
  src/runner/nested.json     nested key surface per discriminator, derived from the SAME pin
  tools/derive_fields.mjs    produces src/runner/fields.json from a checkout of the pinned game source
  tools/derive_nested.mjs    produces src/runner/nested.json from the same checkout
  tools/pin_relevance.mjs    is a newer game-source commit relevant to forge? (reads two checkouts)
  tools/check_release_pin.mjs the loader must resolve an immutable commit, or say it does not
  test/                      node --test, no network; shim.mjs, fakegame.mjs, compose.mjs
  build.mjs                  esbuild IIFE -> ../forge_bundle.js
forge_bundle.js              the built userscript body (repo root, beside builder_bundle.js)
forge_loader_user.js         the ViolentMonkey loader (distinct name, namespace, @match, version)
```

Run tests: `cd forge && npm test`. Build: `cd forge && npm run build`. Regenerate the wire
fixtures: `npm run fixtures`. Dependencies are pinned in `forge/package.json`: `superjson 2.2.6`
(bundled), and dev-only `@trpc/client`/`@trpc/server 11.18.0`, `zod 4.4.3`, `uploadthing 7.7.4`
(read for protocol, not bundled), `esbuild`, `fake-indexeddb`, `jsdom`. Bundle version is
`package.json` `version` (banner line 1 of `forge_bundle.js`, and `VERSION` in `main.mjs`).

## Where Forge runs: `/forge` entry, application-route carrier (0.4.0)

**0.3.0 ran on `/forge` itself and could not hold a session.** Any unmatched URL on the game
origin renders through `global-not-found.tsx`: `app/next.config.mjs:21` sets
`experimental.globalNotFound: true`, `app/src/proxy.ts` returns immediately for every pathname
other than `/`, and `global-not-found.tsx` is a bare `<html><body>` with one `Link`. That is why
it was chosen - no provider tree to fight, no game requests on mount - and it is exactly why
protected work failed there. `app/src/app/layout.tsx` mounts `ClerkProvider` and
`TrpcClientProvider` for VALID application routes only, so on `/forge` the page's own Clerk
runtime never starts, nothing refreshes the session, and `createAppTRPCContext`'s `auth()` finds
no `userId`. The "Open risk, INFERRED" note this section used to carry was right, and it landed:
two Forge 0.3.0 runs of the same read-only manifest each attempted five `profile.getAi` reads and
got `UNAUTHORIZED` five times (`harvests/inbox/tnr_results_1789066888093.json`,
`tnr_results_1789067111434.json`). Public `gameAsset.get` captures had worked, which is the
signature of an auth problem rather than a transport one.

**0.4.0 splits entry from host.**

| | path | what it is | what Forge does |
| --- | --- | --- | --- |
| entry | `/forge` | the providerless 404, unchanged | `window.stop()`, empty it, arm the tab, `location.replace` to the carrier |
| carrier | `/` | a real application route under the root layout | mount ONE fixed full-screen overlay; leave the React tree, `ClerkProvider` and `TrpcClientProvider` mounted underneath |

The operator still opens `https://theninja-rpg.com/forge` and has no second URL to remember
(brief section A). The provider tree staying alive is the whole repair: Forge no longer replaces
a document, it covers one.

**Why `/` is the carrier.** It is the one route repository-held source evidence names positively:
`proxy.ts`'s callback special-cases it (`if (pathname !== "/") return;`), so it is a matched route
rather than a global-not-found render, and the tRPC context carries two A/B variants that steer
landing-page layout (`reports/client_contract.json`, `feasibility_gates.G4`), which is a landing
page rendering under the root layout. It is also the lightest such route this audit can name.
**No route name is compiled into the activation logic.** Arming is a per-tab `sessionStorage`
marker (`tnr_forge_armed_v1`, a boolean and a hop count), so if the app redirects `/` elsewhere
for a signed-in operator, Forge activates on wherever it lands; `CARRIER_PATH` is a hint, and
being wrong about it costs a navigation, not the repair. Two hops without reaching a host disarms
the tab and says so rather than bouncing.

**The loader therefore matches the whole game origin**, as the old builder's loader already does,
at `document-start`. On any game page in a tab that has not been armed through `/forge`, `boot()`
returns before touching the document, issuing a request or installing a style, and the whole call
is wrapped so a Forge bug cannot break the game.

**Body readiness (independent review FPA-1).** `document-start` means an armed carrier can be
reached before the parser has produced `<body>`. `mountHost()` reads `doc.body`, so calling it
then throws, the top-level wrapper swallows the rejection, and the operator is left looking at the
game with the tab armed and Forge never mounted — a valid `/forge` handoff that silently does
nothing. `whenBodyReady()` therefore precedes the mount: it races a `MutationObserver` on
`documentElement`, `DOMContentLoaded`/`readystatechange`, and (only when no observer can be
constructed) an interval, each re-checking `doc.body` rather than trusting the signal. It writes
nothing while waiting and has no timeout, because a document that never gets a body is one Forge
must not touch. `alreadyMounted()` keeps it to one overlay per document, and `mountHost()` now
runs inside `bootHost()`'s guard, so a failure to mount at all leaves the carrier untouched
instead of half-decorated. The stylesheet is scoped to `.f-host` / `.f-app`
(the `html, body` reset lives in `CSS_DOC`, installed on the entry splash only), because an
adopted sheet outlives the overlay and a bare `body`/`*`/`button` rule would restyle the carrier
and keep restyling it after Forge is closed. Closing Forge disarms the tab, removes the overlay,
restores the carrier's scroll and disconnects the old-builder observer.

## Auth health: two signals, no credential material

`src/transport/auth.mjs` holds one of four states (`unknown`, `probing`, `ready`, `signed_out`)
and establishes it from:

1. **the page's own auth runtime**, free: `window.Clerk`'s `loaded` flag and the PRESENCE of a
   `session`/`user`. Booleans only - never a token, never a cookie, never a claim;
2. **one server probe**, `profile.getAi` with a nanoid-shaped sentinel id that cannot exist. Only
   the error CODE is read; the decoded element is never cached, journaled or exported. It is a
   protected procedure with no limiter, so the probe costs no budget a real read might need.

Anything other than `ready` blocks protected work, so a probe that cannot complete fails closed.
`isProtected(path)` comes from `PROCEDURES[path].auth`, transcribed per procedure from the
client-contract audit's `crud_surface[].auth` (each row carrying its own file/line/match at the
pinned SHA) rather than derived from `limited`: the two are exact complements across all 43 rows
today, but `limited` is a statement about the rate limiter, and deriving one from the other would
let a future limiter change move the auth gate silently.

**A server refusal invalidates the state (independent review FPA-2).** A probe is a snapshot and a
session can die a minute later. Whenever a protected procedure comes back `UNAUTHORIZED` — a
capture read, a read-back, a `dedupNames` list, or a mutation — `Runner._authRefused()` calls
`AuthState.refuse()` before pausing, so the banner stops claiming a live session, the gate blocks
every further protected path, and `Resume` is withheld until `probe()` succeeds again. Without it
the standing banner said "TNR session active" while the run screen said authentication was
unavailable, and resuming sent the next protected request at a session the server had already
refused.

**The gate runs before `withSent`, never inside it.** A blocked mutation is one that was never
journaled as sent, so it cannot enter reconciliation and cannot be ambiguous. A protected mutation
that IS sent and comes back `UNAUTHORIZED` is transitioned `SENT -> FAILED` with `authRefused`
and then the job pauses: the server decoded and refused it, so the resolver never ran and the
write does not exist. `resume()` gates before reconciliation too, because reconciling against a
dead session would orphan perfectly good writes. Public procedures are never gated: a capture-only
manifest over `gameAsset.get` still runs signed out.

Forbidden by the brief and asserted by `test/auth.test.mjs`: no `document.cookie`, no `__session`,
no `getToken`, no `Authorization` on a game request, and nothing auth-derived in localStorage,
IndexedDB, the journal, a capture or an exported bundle. `CookieSession`'s header allowlist is
unchanged (`accept`, `content-type`, `x-uploadthing-version`).

**Source pins.** `state/prompt_forge_protected_auth.md` pins `bdec2883`; Forge's global pin is
`345d18ac`, 89 commits later. Neither was moved. Every auth classification and every carrier/entry
fact this repair rests on was proven identical at both commits —
`docs/handoffs/FORGE_PROTECTED_AUTH_PIN_RECONCILIATION.md`, reproducible with
`forge/tools/auth_pin_diff.mjs`. Reading `bdec2883` also upgraded the carrier justification from
inference to source: `app/src/app/page.tsx` renders `/` under the root layout, and `proxy.ts`
contains no `redirect` at all, so a signed-in operator is never sent away from it.

**Known debt.** The carrier page runs the game's own tRPC traffic, which Forge's budget cannot
see. The content paths Forge spends are not the ones a landing page reads, and the limiter is
keyed `${path}-${userId}`, so the two should not collide - but it is a real change from the
providerless host, and it is a reason to prefer a quiet carrier route.

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

Pause reasons: `TOO_MANY_REQUESTS` (path + `until`), `SESSION` (since 0.4.0 also carrying
`authState` and `authRefused`, and raised by the auth gate BEFORE a send as well as by a server
refusal), `NETWORK` (a read failed on
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

`_read()` repairs a record whose persisted history contradicts its state label before anything
sees it: an item marked PLANNED that carries `sentAt`, `createSentAt`, `confirmedAt` or
`verifiedAt` is restored to SENT, which is the only state that routes through reconciliation.
Shape validation alone cannot catch that, and replaying such an item would mint a second live row,
because every create at the pin generates a fresh nanoid. The repair never advances an item
towards a terminal state and never invents an `entityId`; it records why on `item.repaired`.

Guards added by the adversarial pass: `annotate()` and `transition()` patches may not set
`state`, `idx` or any timestamp; `remove()` refuses a job holding a SENT item unless forced;
`setJobState(DONE)` refuses while an item is SENT; `open()` refuses empty item lists unless the runner explicitly opens a parsed capture-only job, and refuses a
second resumable job for the same `manifestHash`; error strings are capped at 512 chars;
`migrate()` refuses a newer or non-integer version; one corrupt record no longer blocks
`listJobs()`, `resumable()` or the export (it is collected in `journal.broken` and exported
raw). `knownEntityIds(entity)` lists every id any job recorded, which reconciliation uses.
`exportText()` returns the whole journal as JSON text (Settings > Export).

Other keys: `tnr_forge_sendlog_v1` (budget send log), `tnr_forge_snap_v1:<jobId>:<entity>`
(pre-create id snapshots, removed when the job is DONE), `tnr_forge_lease_v1:<jobId>` (the
driving tab's id and heartbeat: one tab drives a job at a time; another tab refuses to run or
resume it while the heartbeat is under 30 s old, and a paused or finished job releases it).
The tab id lives in sessionStorage, so a reload or a restored tab keeps its own lease; after
a whole-browser crash the job waits up to 30 s before another tab may take it. Retained unchanged from the old
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

The local mirror computes the server's own estimate. `@upstash/ratelimit 2.0.8` (the game's
pin; fetched from npm to read, not bundled) `slidingWindowLimitScript`: buckets are
`floor(now / 60s)`, and a request is rejected when
`floor((1 - (now % 60s) / 60s) * count(previous bucket)) + count(current bucket) >= 60`.
A strict 60 s window is NOT this: it lets a client that sent 30 early in one bucket send 30
more early in the next, which the server weights to about 59 from this client alone
(adversarial L3). `acquire()` therefore holds a request until BOTH the strict window and the
weighted estimate fit under the allowance, and `status()` shows both.

The allowance is `floor(60 * 0.5) = 30` per limited path per minute, because:

1. The window is per (path, user) and shared with every other tab the user has open; the
   game's own pages call the same `getAllNames`/`get` reads on mount. The client cannot see
   that traffic. Half the window is left for it.
2. The estimate depends on the client and the server agreeing on the bucket boundary. NTP
   keeps that within a second; a skewed clock is the residual risk, which the strict check
   and the margin absorb.
3. The cost asymmetry: a trip is a permanent 1% of money and bank plus a logged incident;
   under-spending costs seconds.

The send log is written to localStorage BEFORE `acquire()` resolves, so a restart inside the
window cannot overspend. `acquire()` waits (never fails). A server 429 at ANY batch index
persists a trip marker until the end of the NEXT server bucket (the current bucket counts
at full weight until it ends and decays over the following one), and every limited send
refuses until then; the job is PAUSED with the path and a countdown. There is no retry path
in the codebase. The margin is a constructor argument (`Budget({ margin })`) and shown on
Settings.

Batch elements on a limited path count one each against the window, and at the limiter edge
each element over the limit is a separate 1% penalty. So on limited paths a request carries
at most 10 elements and never more than the window has room for right now; with no room it
waits for a full chunk. Unlimited paths batch up to 20. `reader.list()` only accepts the
name-list procedures; `getAll` takes a required `{limit, cursor}` and is not used.

Limited paths (16, all `publicProcedure` reads): `jutsu|item|quests|gameAsset|bloodline .get
/ .getAll / .getAllNames`, `profile.getAllAiNames`. Not limited: `profile.getAi`,
`ai.getAiProfile`, every mutation. Table: `src/transport/procedures.mjs`, generated from the
audit's `crud_surface` with the verification's F4 corrections applied.

## One composition, shared by the app and every test

`compose()` in `main.mjs` builds the whole dependency graph, and `boot()` is a thin wrapper that
supplies `window`'s primitives. Every test harness calls the same function through
`test/compose.mjs`, substituting only the environment primitives and the transport client.

This is a rule with a reason. The harnesses used to build their own graphs, and one of them passed
the journal into the `Reconciler` when the shipped composition did not. The `Reconciler` needs the
journal to subtract ids other jobs already own, so the test named for cross-job adoption exercised
a safer graph than the app shipped, and a whole adversarial pass reported that hole as covered. The
independent review found it. Two things now prevent a recurrence: the wiring lives in exactly one
place, and `Reconciler` throws when constructed without a journal rather than quietly degrading.

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
- Only the adapter's own shape `{error:{json:{message, code, data:{code}}}}` counts as a
  request-level error, jsonrpc `code` included: every recorded adapter error carries a numeric
  one. A gateway's JSON body (`{"error":{"code":"FUNCTION_INVOCATION_TIMEOUT"}}` at 504) is a
  `TransportError` with `received: true`, so a mutation behind it stays ambiguous and is
  reconciled, never marked failed.
- A batch element that cannot be decoded at all is fatal **for a mutation** and salvageable for a
  query. A query batch keeps its well-formed siblings, because a missing read costs a re-read. A
  mutation throws, because the request reached a server that may have run the resolver: turning
  that into a per-index verdict would mark an already-SENT write terminally failed. `readMutation`
  refuses such an element a second time, so a future regression is ambiguity, not a false verdict.

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

## Pre-send validation, the field lists, and the 45g power bound

**45d is stale against the pin, so the app does not use it.** `tools/derive_fields.mjs`
reads the top-level keys of each entity validator from a checkout of the pinned commit
(`JutsuValidatorRawSchema`, `ItemValidatorRawSchema`, `BloodlineValidator`,
`QuestValidatorRawSchema`, `gameAssetValidator`) into `src/runner/fields.json`, which the
bundle carries; nothing is fetched at boot. The diff against
`45d_DATA_entity_schemas.json` (generated 2026-08-26 from an older drop):

| entity | pinned | 45d | difference |
|---|---:|---:|---|
| item | 71 | 59 | twelve `farm*` keys (`combat.ts:1498-1508`), of which `farmYieldItemId` is required-nullable |
| quest | 29 | 28 | `requiredFarmingLevel` (`objectives.ts:675`) |
| jutsu, bloodline, gameAsset | 42, 11, 10 | same | none |

The item gap is not cosmetic: an update payload picked by the 45d set omits
`farmYieldItemId`, which `ItemValidator` requires, so every item update would have been
refused by zod, and the `.prefault(0)` farm counters would have been reset had it passed.
The generator in `skills/` (`schema_extract.py`) needs re-running on the pinned drop; that
is a `skills/` change this branch does not make. Re-run `derive_fields.mjs` whenever the pin
moves.

Unknown keys are refused locally against those lists, **including for an AI create**. The AI
record has no content validator, so the extractor derives the effective key set of
`insertAiSchema` (`drizzle/schema.ts:2577`) as well: the 168 `userData` columns, minus the 13
`.omit()` entries, plus the 22 `.extend()` keys, giving 157. Checking AI keys only against a
fetched live row (the earlier behaviour) meant a typo could not be caught until after
`profile.create` had already minted the placeholder, so a local, knowable mistake cost a live row.
The pinned set needs no live row, so the check now runs before the create like every other entity.
The live row's keys and the extension set are still unioned in for an edit, and the omitted and
server-owned columns are refused in both directions.

**An AI item entry's `number` is `dropChancePerc`, never quantity** (law 69;
`profile.ts:1528-1530` builds `{id, chance: o.number}` and `:1577` writes
`dropChancePerc: chance`). The live kit is re-sent with each item's live `dropChancePerc`,
quantity is untouched, a bare id carries chance 0, and read-back compares chances per id.
The first draft sent quantity as the chance; the L3-5 panel caught it.

**The 45g power bound is gated out, not fixed.** Brief section 5 offered two options; this is
the second. `validate.mjs` does not load `45g_DATA_checks.json` at all, and the header comment
there points at the brief. Reason: `PowerAttributes.power` is `z.coerce.number().min(0)` with
no maximum (`combat.ts:111`) and is spread after `BaseAttributes` in all 61 tags that use it;
`45g.tag_power_max` asserts 100 because `schema_extract.py` does not handle spread
precedence. A test asserts that `power: 400` on a damage tag is accepted by the runner.
Fixing the generator is a separate change to `skills/`, which this branch does not touch.

Merge for update picks the pinned field set from live ∪ asserted, so relation objects
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
- `resolvePool` (pool codes -> ids and distance gates) and the lint set: these ARE ported now, at
  parse time rather than mid-build; see "Pool codes, kit integrity and the ported lints".

## Placeholders carried (balance, reserved for dauntless)

None are hard-coded in `forge/`. The app carries no drop rates, reward values, stat numbers
or difficulty gates; those live in manifests. Two values that are policy rather than
balance, and are shown in the UI as settings: the budget margin (0.5), the batch sizes
(20 per request on unlimited paths, 10 on limited ones, under the route handler's
`maxDuration = 90`), and the job lease TTL (30 s).

## Verification

`cd forge && npm test`. No test opens a socket, and a test asserts that: no test file may import a
network module or call a global fetch, and `src/` may name only `api.github.com` and
`cdn.jsdelivr.net`. 199 tests, all through the shipped `compose()`.

| layer | tests | what is proven |
|---|---:|---|
| storage | 24 | write-ahead ordering, the four mandated evictions, SENT->PLANNED impossible, IDB invalidation |
| transport | 39 | every recorded request reproduced byte for byte; every recorded response decoded to what the real client decoded |
| budget | 16 | write-ahead send log, window survives eviction, 31st send waits, a 429 in a 207 halts after caching the good index |
| runner + reconcile | 30 | two-phase creates, six entities, kit re-send, refs, unknown-key refusal, power uncapped, crash before send / after send / after response / mid two-phase against server-side row counts, gameAsset two-orphan ambiguity, TOO_MANY_REQUESTS pause, NetworkError leaves SENT, plus pre-send validation over every manifest under `push/` |
| ui | 12 | no HTML string sink in src, takeover, five screens render, resume banner, run screen, settings persist, picker -> start -> DONE, render errors surface, an unverified job never renders or exports as success, the release pin cannot float, the socket-free grep |
| harvest | 3 | a bundle carrying match/drift/unread/failure, run through the repository's real `harvest.py` |
| adversarial | 75 | one regression test per finding that survived the panels and the two independent reviews, plus the readiness invariants: R1-R5 (terminal semantics), K1-K6 (pool codes and lints), D1-D4 (dedupNames), N1-N5 (nested keys), F4c-F4d |

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
- **Late results (the panels' verify stages were cut short by a session limit, so these
  were verified by reading the pinned source directly):** the 45d field lists are stale
  (above); the AI kit re-send wrote quantity into `dropChancePerc` (above); a landed AI
  update reconciled after a crash skipped its rules step; a lost profile write whose only
  change was `includeDefaultRules` passed as landed; a 429 or wire failure during
  reconciliation escaped `resume()` raw; the strict-window budget could drive the server's
  weighted estimate to 59 from this client alone, and the trip countdown was one bucket
  short; a gateway's JSON error body would have been read as a per-index verdict; two tabs
  could drive one job. All fixed and pinned. Not acted on: the nested unknown-key check
  (only top-level keys are checked; misspelled keys inside `effects[]`, quest objectives and
  rule conditions pass), the rules read-back comparing serialised JSON (server prefaults may
  show as drift, which is visible and harmless), and verify `unread` staying non-terminal.

### Independent review of `a1f9144`

A separate reviewer audited the frozen branch against the pinned source and reported four
high-severity defects. All four reproduced, each was fixed, and each is pinned by a regression test
that fails against the frozen tree:

- **A hand-edited persisted record could replay a create.** Shape validation accepted an item
  labelled PLANNED that still carried `createSentAt`, and the runner re-sent the create, minting a
  second live row. Fixed by the history repair described above.
- **The shipped composition built the `Reconciler` without the journal**, so a resumed job could
  adopt and then overwrite a row another job had created, and `adopt()` refused an id only when
  another item in the *same* job held it. Fixed by the single composition, by making the journal
  mandatory, and by making `adopt()` consult every job through `journal.findHolder()`.
- **An unknown AI key was not knowable before the create**, so a typo cost a live placeholder.
  Fixed by deriving `insertAiSchema` in the extractor, as described above.
- **A malformed mutation response element became a definite failure**, discarding the ambiguity
  the journal exists to preserve. Fixed at the transport boundary, as described above.

### Independent review of `4062268`

The second review re-checked those four. F1, F2 and F3 were confirmed closed. **F4 was NOT closed**
and was reopened as a HIGH blocker: the correction only covered an element with no `error` at all.
`decodeElement()` still accepted *any* truthy `el.error`, so `[{"error":{}}]` decoded to a normal
`UNKNOWN` verdict and an already-SENT mutation was marked FAILED. Closed here: a per-index error is
now held to the same `isTrpcErrorBody()` adapter shape as a request-level one, so an element that is
not the audited shape throws, a mutation batch behind it raises a `TransportError`, the item stays
`SENT` and the job pauses at `UNDECODABLE_RESPONSE`. Query sibling salvage is unchanged. Pinned by
`F4c` (five malformed shapes, query salvage, end-to-end through the runner; fails against `4062268`)
and `F4d` (every recorded adapter error still decodes to the same code).

The reviewer also flagged that the request-level predicate was looser than its own comment; it now
requires the numeric jsonrpc `code`. Two of their observations were correct but not defects: the
per-element salvage is right for queries and is kept, and `MALFORMED_ELEMENT` remains a valid query
outcome. Deriving the AI keys exposed a parser bug in the extractor, which double-counted the first
key of every object body; the field sets were unaffected (object keys deduplicate) but the reported
counts were wrong, and both are fixed.

## Terminal and verification semantics

A job has a STATE (has execution finished) and an OUTCOME (is it good news). They were the same
thing, and the same thing was green.

- `RUNNING | PAUSED | DONE | INCOMPLETE | ABORTED`. `INCOMPLETE` is execution finished with at
  least one item not terminal - a read-back that could not be read (`verify: "unread"`) or that
  came back different (`verify: "drift"`) leaves its item `CONFIRMED` at phase `verify`.
  `setJobState()` REFUSES `DONE` while any item is unresolved, so the honest state is structural.
- An `INCOMPLETE` job is resumable, and resuming it can only re-read: the phase recorded on
  `CONFIRMED` is `verify`, so no mutation can be sent again. Two tests prove exactly that (R2, R3).
- `jobOutcome(job)` is what the UI, the summary and the exported bundle report: `success` only when
  every item read back equal; `failed` if anything FAILED; `unverified` for drift, unread, a skipped
  orphan or an unresolved item; `open` while running or paused. The Run screen banner and the toast
  are keyed off it, and an incomplete or failed run still auto-exports its bundle - as evidence,
  never as a success.
- `readBack:false` is REFUSED by `parseManifest` on any manifest carrying items. It used to mark
  every item `VERIFIED{skipped}`, so a manifest could opt out of verification and be reported as
  verified. No manifest under `push/` has ever set it and no skill instructs it, so nothing depended
  on it. A capture-only manifest is unaffected.

## Pool codes, kit integrity and the ported lints

`src/runner/pool.mjs`, wired into `parseManifest`, which is before any create, upload or update.

- Codes in `jutsus[]` and `rules[].action.jutsu` resolve from the repository's generated
  `32b_DATA_pool.json`, bundled at build time (the old builder fetched it from a moving branch on
  every run). A code-referenced rule also gets law 40's gate arithmetic (range+1) filled in.
- A code that does NOT resolve is a manifest problem: no job is opened and nothing is sent. This is
  the TNR-01 mechanism - `profile.updateAi` syncs the kit by set difference, so a literal code is
  dropped server-side and the AI is left with an empty kit behind a green row.
- The code pattern is `[A-Z]{1,2}\d{1,2}`, wider than the builder's `\d{2}`, which never matched
  A1-A3 and so never resolved OR flagged them.
- Kit integrity from `validate.py check_pool_kit`: a rule firing a jutsu the AI does not carry is
  inert (law 18) and a gate that is not range+1 (law 40) are errors; a gate on a self/ground jutsu
  and an all-60-AP kit stay advisory.
- `src/runner/lints.mjs` ports L03, L04, L05, L07, L11, L12b, L13, L16, L17, L18 as errors and L06,
  L08, L10, L15 as advisories that do not block. Three deliberate differences are documented at the
  top of that file: `skipPreflight` cannot switch a safety lint off (every check fires only on data
  the entry carries, so a partial quest edit needs no bypass); L09 is left to the source-derived
  nested check; and L18's "clear/copy are excluded" half is NOT enforced, because `docs/RULINGS.md`
  records law 19 as contradicted at source - enforcing it would reject payloads the server accepts.
- L13 on an `ai` create was re-derived at the pin: `userData` has no `hidden` column, so it is not
  required there. A manifest that carries `hidden: true` anyway (the repo rule says every create
  does) is accepted, dropped by the pinned-field merge before the send, and excluded from the diff.

## dedupNames

Enforced before the first create of the job, through the cache-first reader under the budget. A
collision fails that item with no placeholder minted. Two differences from the builder's version:
only PLANNED creates are checked (an item this job already created owns its live name, and an edit
re-asserting its own name would always collide with itself), and a limited or failed name read
PAUSES the job rather than being skipped with a warning - the check is either performed or the job
stops.

## Nested unknown keys

`tools/derive_nested.mjs` reads the same pin as `derive_fields.mjs` and writes
`src/runner/nested.json`: the allowed key set per discriminator value for effect tags (76), quest
objectives (65), AI rule conditions (9) and actions (10), plus the rule envelope, the objective
reward block, quest `content`, dialog choices and the `{ids, number, quantity}` entries behind
`opponentAIs` and `attackers`. `Validator.nestedProblems()` refuses an unknown key, or an unknown
`type`/`task`, before any create or update.

Key sets only, never bounds: a bound the generator gets wrong is the `45g.tag_power_max` mistake,
and a test still asserts that `power: 400` is accepted. It fails closed - with no `nested.json`, or
for a discriminator the pin does not define, the structure is refused rather than sent unchecked -
except that an EMPTY nested structure carries nothing to check and is not a reason to refuse.

**Two real findings this surfaced in committed manifests.** Both are keys the live server drops
today, both re-verified absent from the validators at the pin AND at the current game `main`
(`62af1b34`), and both are
pinned by a test so they cannot later be mistaken for false positives:

1. five quest EDITS (`push/27`, `30`, `33`, `34`, `35`) re-assert whole live records including
   `raidEndsAt`, `raidCaptureDeadline` and `raidGracePeriodEnd`. Those are `drizzle/schema.ts`
   columns but not `QuestValidatorRawSchema` fields: read shapes are not write shapes, and those
   values never landed.
2. `push/46` gives every `start_battle` objective an `image`, which `InstantStartBattleObjective`
   does not define. The value has no effect.

Neither is a forge defect. Forge refuses those manifests pre-send until someone edits them; whether
to edit them is dauntless's call.

## Source pin: still relevant, and how that was checked

`tools/pin_relevance.mjs <checkout-of-pin> <checkout-of-newer>` re-derives `fields.json` and
`nested.json` from both checkouts and compares them, then diffs the 22 declared surfaces forge reads
for behaviour rather than field sets (the limiter, router registration, the six content routers, the
validator files, the drizzle schema behind `insertAiSchema`, the drizzle constants the validators
import, the upload route, the three files that make `/forge` a host, and the dependency pins). It
reads only; it never runs the game.

**Run against the actual current game `main`, not a repository sentinel snapshot.** The first pass
proved the pin against `e02f8159`, the upstream SHA recorded by this repository's sentinel; the
independent review of `c388ea6` was right that this is not the same claim as relevance to
production. Resolved fresh with `git ls-remote` at 2026-09-09T01:44Z:

- `studie-tech/TheNinjaRPG` default branch `main` head: **`62af1b3405b10183b31f838c9a5f131d790460f1`**
- forge pin, unchanged: `345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9`

Result, `node tools/pin_relevance.mjs <pin> <62af1b34>`:

- **both derived contracts are byte-identical.** `fields.json` and `nested.json` regenerated from a
  checkout of the current game head match the checked-in files exactly. That is the strong claim:
  what the bundle validates against at the pin is what production's validators say today.
- **three declared surfaces differ, all read, none relevant:**
  - `app/src/server/api/root.ts`: two new routers registered (`push`, `purchases`). No path forge
    calls moved.
  - `app/drizzle/schema.ts`: twelve new device/purchase/store tables and their relations, no
    removals. No `userData` column moved, which the identical 157-key `ai` field set proves
    independently.
  - `app/drizzle/constants.ts`: purely additive (push/store/native constants, one forum
    pagination constant), no removals. Forge derives key sets and never enums, so a constant cannot
    make it reject something the server accepts; it is a declared surface so that a reviewer sees
    such a change rather than having it sit outside the gate.
- everything else forge depends on is byte-identical between the pin and current `main`, including
  `trpc.ts` (the limiter), all six content routers, all four validator files, the upload route,
  `proxy.ts`, `next.config.mjs`, `global-not-found.tsx` and `app/package.json`.
- for the record, what changed between the sentinel `e02f8159` and current `main` is SEO, forum,
  comments and public-profile work plus that one forum constant: sixteen files, none of them a forge
  surface.

So the pin STAYS at `345d18ac` on evidence, not inertia. The gate exits 1 on any change, so the next
person has to read it rather than skip it. Nothing was adopted for being newer. If game `main`
advances again before integration, rerun the same command; the two checkouts are the only inputs.

## Release pin

The loader used to `@require` a BRANCH. jsDelivr caches a branch ref for about twelve hours and any
later push changes what that URL returns, so the installed bytes were not provably the reviewed
bytes - not acceptable for a mutation client.

- `state/staged_workflows/release_pin.yml` now covers `forge_bundle.js` as well as the builder's.
  Each loader is rewritten only when its own bundle changed in that push; the forge loader's
  `@version` is synced from `forge/package.json` (ViolentMonkey refetches on a version rise); and
  the pin deletes the `@x-unpinned-until-release` marker. The builder path is untouched.
- `forge_loader_user.js` carries `@version 0.2.0` and, while this branch is unreviewed, an explicit
  `@x-unpinned-until-release` marker naming the branch it floats on.
- `tools/check_release_pin.mjs`, asserted by the suite, fails on a floating `@require` without that
  marker, a marker that disagrees with the URL, a marker left behind after pinning, a `@version`
  that did not rise with the bundle, and a staged workflow that does not cover forge. A second test
  performs the workflow's own rewrite on a copy and proves the result is clean.

**One dauntless action is required:** install `state/staged_workflows/release_pin.yml` at
`.github/workflows/release_pin.yml` through the GitHub web UI. The PAT cannot push
`.github/workflows/`, and no credential workaround was attempted. Until then the check reports it as
`pending-install` rather than failing the suite.

## Harvest compatibility

Forge auto-commits a bundle to `harvests/inbox/`, and nothing had ever read one. Running the real
`harvest.py` over a generated bundle showed it would have been read as EMPTY: harvest counts an
entry by its state vocabulary (`ok`/`error`) and forge wrote the journal's, so every entry fell
through to SKIP and `verify` exited 0 with nothing verified - a bad run reported as fine, in the one
tool meant to catch that.

`exportJob` now emits the shape `harvests/inbox/` already holds: `state` in harvest's vocabulary,
`verdict` (`match|drift|unread`), and the v4.28 `asserted` checklist built from the keys the runner
asserted and the diffs it recorded, so a drift reads as a per-field FAIL. The journal's own state
rides along as `forgeState`, and the bundle carries `outcome` and honest postflight counters.

Two tightly-scoped changes OUTSIDE `forge/` (a widened Lane A review surface), both in
`harvest.py`'s `verify`, both checked against every bundle already in `harvests/inbox/` with not one
verdict changed:

1. an entry with `state=error` was a SKIP, so a bundle holding a failed push could exit 0 as
   "verified". An entry that never shipped is now an `ERROR` line that fails the gate.
2. **a forge bundle now fails closed** (independent review of `c388ea6`, finding 1). A job whose
   only unresolved item was a SKIPPED orphan exported a bundle that `verify` printed as SKIP and
   exited 0 on, while forge itself reported `outcome: unverified` and the asset row the skip walked
   away from was still live. For a bundle marked as forge (`cfg: "forge"`, or entries carrying
   `forgeState`), a `skipped` or `pending` entry is now UNVERIFIED rather than a skip, and the
   bundle's own `outcome` must be `success` before the gate exits 0 - forge's verdict is
   authoritative in the failing direction, and a forge bundle with no `outcome` fails closed.
   Legacy builder bundles keep their old semantics, where those states meant a row the builder never
   attempted; a regression pins that too.

`test/harvest.test.mjs` runs a job producing all four outcomes, exports the bundle and runs the real
`harvest.py` over it: `verify` prints OK / FAIL / UNVERIFIED / ERROR and exits 1, `index` still
reports the capture calls, `diff` says honestly that a forge bundle carries no `pushed`/`live`
payloads rather than inventing them, and a clean run exits 0. Three more do the same end to end for
the review's finding: an ambiguous create resolved through the real `Runner.skip()` (verify exits 1
and the server row is asserted still present), a job exported with its create still in flight, and a
legacy-shaped bundle proving the old semantics survive.

A forge capture-only bundle is still read by the early "nothing to verify" branch. Forge cannot
produce one today (`journal.open()` refuses an empty item list), so that path is unreachable from
forge; it is listed under "Not finished" rather than guarded speculatively.

## Not finished

- **Pause during a run** is wired (`Runner.requestPause()`, honoured between items; the Run
  screen button calls it) but only jsdom has exercised the button.
- **Captures with `select` / `scope`.** The old bundle's capture entries carried a `select` field
  list, and forge has no projection mode: a capture is a row count or, since 0.3.0, the whole
  record. Consequence for ingestion, measured rather than assumed: `harvest.py index` lists a forge
  bundle's capture calls and their inputs; `get`/`names`/`assets` answer from a capture only when it
  asked for `persist: "full"`, and answer nothing for a summary capture. A projected
  `persist: "fields"` mode would help for large records and is deliberately NOT built - it was
  ruled out of scope by the full-capture brief. Verification of written records does not depend on
  any of it (that runs off `entries[]`).
- **A capture-only manifest cannot be run.** `parseManifest` accepts one, but `journal.open()`
  refuses an empty item list, so a manifest with captures and no items cannot start a job.
  Pre-existing, unrelated to the readiness blockers, and not changed here.
- **Clock skew** shifts the budget's bucket boundary relative to the server's; the strict
  window and the margin absorb a second or two, not more.
- **Clerk session refresh on `/forge`** (see "Host path"): inferred risk, mitigated by the
  SESSION pause, not solved.
- **The release-pin workflow install** is a dauntless action (above). Until it lands, a push to
  `main` that changes `forge_bundle.js` does not pin the forge loader.
- **`selfcheck.py` fails on this branch and on `main` identically** (TNR-03: `45d` is absent from the
  repository root and `45c`/`45g` disagree on provenance). Pre-existing, untouched by this pass,
  and verified to be byte-identical output before and after it.
- **Not exercised in a browser.** jsdom covers rendering and wiring; Firefox Android,
  ViolentMonkey's `@run-at document-start` timing on a 404 response, `window.stop()`
  behaviour, `navigator.storage.persist()` prompts, real cookie/session continuity through a long
  job, and real rate-limit clock skew are all unverified until dauntless installs it. The code
  fails or pauses safely when those assumptions break; that is an argument, not a measurement.
