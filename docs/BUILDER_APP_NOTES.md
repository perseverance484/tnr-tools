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
(read for protocol, not bundled), `esbuild`, `fake-indexeddb`, `jsdom`.

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

## Journal schema (v1)

One localStorage key per job: `tnr_forge_job_v1:<jobId>`. The job list is derived by
scanning keys with that prefix; there is no separate index that can disagree with the jobs.

```
job  = { v: 1, jobId, manifestPath, manifestNumber, manifestHash, startedAt, updatedAt,
         state: RUNNING | PAUSED | DONE | ABORTED,
         pause: null | { reason, path, until, idx, detail },
         capturesBefore?, capturesAfter?, items[] }
item = { idx, entity, op: create | update, name, srcId, targetId, payloadHash,
         state: PLANNED | SENT | CONFIRMED | VERIFIED | FAILED | ORPHANED | SKIPPED,
         phase: create | update | rules-toggle | rules | verify,
         entityId, snapshotKey, aiProfileId?, sentAt, confirmedAt, verifiedAt,
         error, diffs?, verify?: match | drift | unread, candidates?, reconciled?, adopted? }
```

Legal transitions are a table in `journal.mjs`; `SENT -> PLANNED` is absent from it, which
makes "never retry a SENT create" structural rather than a runner discipline. `CONFIRMED ->
SENT` exists only for the later phases of one item (update after create, rules after
update). `withSent(jobId, idx, patch, thunk)` flushes SENT synchronously and only then runs
the thunk; if the flush throws, the thunk never runs. Migrations are a chain keyed on `v`.
`exportText()` returns the whole journal as JSON text (Settings > Export).

Other keys: `tnr_forge_sendlog_v1` (budget send log), `tnr_forge_snap_v1:<jobId>:<entity>`
(pre-create id snapshots, removed when the job is DONE). Retained unchanged from the old
builder: `tnr_bk_idmap_v1` (srcId -> id, image name -> url) and `tnr_bk_gh_v1` ({on, pat}).
Capture cache: IndexedDB `tnr_forge` / `captures`, keyed `path:id`, entity index.

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
  always an array indexed by batch position.
- An undefined input serialises as `{"json":null,"meta":{"values":["undefined"],"v":1}}`.
- Status rule: a single-element batch carries its own status; any mixed batch is **207**. A
  429 can sit at one index of a 207 while another index succeeded. Outcome is read per index
  and the status is never consulted for a verdict (spec section 8).
- Error elements carry `data.code`, `data.httpStatus`, `data.path`, `data.zodError` (issues
  array or null). `readCreate` refuses a `success:true` whose message is not nanoid-shaped.
- A GET on a mutation path is 405 `METHOD_NOT_SUPPORTED` before any resolver runs.

`CookieSession` sends `credentials: "same-origin"` and structurally refuses an
`Authorization` header. The GitHub bearer lives in `github.mjs` and is sent to
`api.github.com` only. The native shell or a bearer session is a new `Session`
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

## Pre-send validation and the 45g power bound

Unknown keys are refused locally against the 45d field lists for jutsu, item, bloodline,
quest and gameAsset. The AI record has no 45d entity (`insertAiSchema` is the whole
`userData` table), so AI keys are checked against the live record fetched before the write
plus the schema's extension keys (`jutsus`, `items`, `primaryElement`, `secondaryElement`,
`rules`, `includeDefaultRules`).

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
balance, and are shown in the UI as settings: the budget margin (0.5) and the batch size
(20 per request, under the route handler's `maxDuration = 90`).

## Verification

`cd forge && npm test`. No test opens a socket.

| layer | tests | what is proven |
|---|---:|---|
| storage | 24 | write-ahead ordering, the four mandated evictions, SENT->PLANNED impossible, IDB invalidation |
| transport | 39 | every recorded request reproduced byte for byte; every recorded response decoded to what the real client decoded |
| budget | 16 | write-ahead send log, window survives eviction, 31st send waits, a 429 in a 207 halts after caching the good index |
| runner + reconcile | 33 | two-phase creates, six entities, kit re-send, refs, unknown-key refusal, power uncapped, crash before send / after send / after response / mid two-phase against server-side row counts, gameAsset two-orphan ambiguity, TOO_MANY_REQUESTS pause, NetworkError leaves SENT |
| ui | 8 | no HTML string sink in src, takeover, five screens render, resume banner, run screen, settings persist, picker -> start -> DONE, render errors surface |

Adversarial passes: independent skeptic panels were run against L1, L2 and L3-5 (see the
commit history for what changed as a result).

## Not finished

- **Pause during a run.** The Run screen's "Pause after this item" only toasts. Pausing
  happens on 429, session loss, or network ambiguity; a user-initiated pause between items
  is not wired.
- **Captures with `select` / `scope`.** The old bundle's capture entries carried a `select`
  field list; the runner records row counts and stores full decoded data in the capture
  cache but does not trim to `select`.
- **Pool-code resolution and the lint set** (`resolvePool`, L09-L22) from builder v4.32 are
  not ported. Manifests that still carry pool codes will fail pre-send validation only if
  the code lands in an unknown key; a pool code in a legal field would be sent as a literal.
  Port before running any AI-kit manifest through forge.
- **`dedupNames` (live name collision check)** is parsed but not enforced.
- **The loader `@require` points at the branch**, not a commit. `release_pin.yml` is
  paths-filtered to `builder_bundle.js`; extending it to `forge_bundle.js` is a workflow
  edit (web UI install) and is not done here.
- **Not exercised in a browser.** jsdom covers rendering and wiring; Firefox Android,
  ViolentMonkey's `@run-at document-start` timing on a 404 response, `window.stop()`
  behaviour, and `navigator.storage.persist()` prompts are unverified until dauntless
  installs it.
