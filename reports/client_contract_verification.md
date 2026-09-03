# Client contract verification

Adversarial spot-verify of `reports/client_contract.json` (branch `client-contract-audit`,
commit `e86c4b4`) against source.

| | |
|---|---|
| Game SHA checked out | `345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9` |
| tnr-tools SHA | `7235ca6` (branch `main`) |
| Report verified | `e86c4b4`, `reports/client_contract.{json,md}` |
| Live requests made | **0.** No credential requested, used or synthesised. |
| Game clone | read-only, unmodified, no PR |
| Policy files | `CLAUDE.md`, `CONTRIBUTING.md`, `DEVELOPMENT.md`, `README.md`, `CODEOWNERS` left unread as instructed |

**This is a partial pass.** Coverage is stated honestly in section 3. It went deep on V1
and V2 because both are load-bearing for an architecture decision, and stopped there.

---

## 1. Verdict table

| Claim | Verdict | Reason |
|---|---|---|
| `md` top-5 #2 / `feasibility_gates.G5` "all 26 procedures the bundle calls are `protectedProcedure`" | **REFUTED** | At least 10 distinct procedures the bundle calls by literal string are `publicProcedure`, which carries the limiter |
| `divergence.ranked[D2-ratelimit-scope]` "inert" | **REFUTED** | The backoff runs against exactly the paths that are limited, and each trip debits money |
| `md` top-5 #2 population, "`ratelimitMiddleware` appears outside `trpc.ts` only at `misc.ts:108` and `towerDefense.ts:116`, `:157`" | **REFUTED** | 39 hits across 7 files |
| V1 sub-claim: no renamed or locally composed procedure builder | **CONFIRMED** | Only two builders exist, `trpc.ts:211` and `:230` |
| V1 sub-claim: no content mutation carries a local limiter | **CONFIRMED** | Verified procedure by procedure across all 7 content routers |
| `transport.batching` `PARTIAL`, route handler unread | **UNDERSTATED** | Handler found and read; it settles five things the report assigned to library default |
| `procedures.mcp_boundary` 14/12 split | **REFUTED** | At least two misclassifications, both understating MCP coverage |
| `transport.transformer` superjson at `trpc.ts:89` | **CONFIRMED** | `transformer: superjson` inside `initTRPC(...).create({...})` |
| `feasibility_gates.G2` CORS `NOT_IN_SOURCE` | **CONFIRMED** at handler level | The tRPC route handler sets no CORS headers |
| `write_semantics.mutation_return` | **UNVERIFIED** | Not checked this pass |
| `entities.unknown_key_rule` (V4) | **UNVERIFIED** | Not checked this pass |
| `fidelity.tag_power_max_is_wrong` (V3) | **UNVERIFIED** | Generator not read |
| `feasibility_gates.G7` (V5) | **UNVERIFIED** | Not adjudicated |

Counts: 4 `CONFIRMED`, 4 `REFUTED`, 1 `UNDERSTATED`, 4 not reached, out of roughly 88
claims in the JSON. **Coverage is approximately 9 of 88 claims, ~10 percent**, deliberately
concentrated on the two the dispatch named highest-consequence.

---

## 2. Findings in full

### F1. The rate limiter DOES gate the builder. (refutes the report's highest-consequence claim)

The report's summary states all 26 procedures the bundle calls are `protectedProcedure` and
concludes the limiter does not gate them. Source and the report's own JSON both say otherwise.

`publicProcedure` carries the limiter:

```
app/src/server/api/trpc.ts:211
export const publicProcedure = t.procedure
  .use(ratelimitMiddleware)
  .use(sentryMiddleware);
```

`protectedProcedure` (`trpc.ts:230`) does not. That half is correct.

But the read paths are `publicProcedure`. Verified at source:
`jutsu.ts:257 getAllNames`, `jutsu.ts:266 get`, `item.ts:163 getAllNames`,
`item.ts:197 get`, `quests.ts:134 getAllNames`.

And the bundle calls them. Literal string occurrences in `builder_bundle.js`:
`jutsu.get` 4, `jutsu.getAllNames` 2, `jutsu.getAll` 1, `item.get` 3, `item.getAllNames` 2,
`quests.get` 4, `quests.getAllNames` 2, `gameAsset.get` 4, `gameAsset.getAllNames` 2,
`bloodline.get` 2. Ten distinct rate-limited procedures, 26 call sites.

The report contradicts itself: `procedures.crud_surface` marks **16 of its 43 entries as
`publicProcedure`**, including every one listed above. The JSON was right and the summary
generalised past it.

Consequence, and this is why it matters rather than being a bookkeeping nit:

- The limiter is 60 requests per 60 seconds keyed `${path}-${userId}` (`trpc.ts:123`, `:148`).
- A trip increments `movedTooFastCount` and multiplies **both money and bank by 0.99**
  (`trpc.ts:164`), then throws `TOO_MANY_REQUESTS` with "Incident logged for review".
- Production **fails closed** if Redis is unreachable (`trpc.ts:141`).
- `getRL` in the bundle runs an **eight-try exponential backoff** (`builder_bundle.js:336`).
  Each retry that trips debits again. A fully exhausted sequence is ~7.7 percent of money
  and bank, and eight logged incidents.

`D2` calls this machinery "inert." It is the opposite of inert: it is pointed directly at
the only limited surface the client touches, with a compounding penalty and an incident log.

### F2. "protectedProcedure implies unlimited" is false as a general rule

The report's stated population for the limiter outside `trpc.ts` is `misc.ts:108` and
`towerDefense.ts:116`, `:157`. Actual population: **39 occurrences across 7 files** —
`misc.ts`, `towerDefense.ts`, `raids.ts`, `combat.ts`, `comments.ts`, `item.ts`, `travel.ts`.

`item.ts` matters because it is a content router. `item.splitStack` (`item.ts:1523`) is a
`protectedProcedure` with `.use(ratelimitMiddleware)` composed **at the call site**. That is
precisely the evasion pattern the dispatch predicted, and it means the base builder does not
determine limiting. It must be checked per procedure.

Mitigating, and verified independently: **no content mutation carries a local limiter.**
Checked `create` / `update` / `delete` / `clone` / `updateAi` / `updateAiProfile` across
`jutsu.ts`, `item.ts`, `ai.ts`, `asset.ts`, `quests.ts`, `profile.ts`, `bloodline.ts`. All
clean. So the operative rule is the inverse of the report's: **reads are limited, writes are not.**

### F3. V2 resolved: the route handler, and what it settles

`app/src/app/api/trpc/[trpc]/route.ts`, read in full. Five upgrades:

1. `fetchRequestHandler` with `endpoint: "/api/trpc"`, exported as **both `GET` and `POST`**.
   Batching is the tRPC 11 fetch-adapter default; nothing custom.
2. `export const maxDuration = 90` and `runtime = "nodejs"`. A **90 second ceiling per HTTP
   request**, which bounds how large a batch can safely get.
3. `withRequestScope` gives **one memo per HTTP request, shared by every procedure in the
   batch**. Batching is not merely fewer round trips; related procedures in one POST are
   cheaper server-side by design.
4. **No CORS headers, no request size limit** set in the handler. Confirms `G2` at this layer.
   Anything upstream is infra and outside this repo.
5. `onError` deliberately skips logging `UNAUTHORIZED` and `TOO_MANY_REQUESTS`. So a limiter
   trip is **silent in the operator's telemetry while still debiting the account** — a client
   cannot assume someone else will notice. It also treats `METHOD_NOT_SUPPORTED` on a mutation
   path as a crawler, confirming mutations must be POST.

### F4. mcp_boundary understates MCP coverage

Two entries in `not_reachable_over_mcp` are wrong at source:

- `item.get` — `item.ts:197` is `publicProcedure` with `.meta({ mcp: { enabled: true, ... } })`.
  The report's `crud_surface` also records `mcp_enabled: false` for it.
- `profile.create` — `profile.ts:1138` carries `mcp: { enabled: true, description: "Create a
  new AI character (content editors)" }`. Report records `mcp_enabled: false`.

So the 14/12 split is not reliable. Re-derived per procedure across the 7 content routers,
the authoring boundary is:

- **MCP-enabled writes:** `quests.create`, `quests.update`, `quests.clone`, `quests.delete`,
  `profile.create`, `profile.delete`, `profile.updateAi`
- **Not MCP-enabled:** all of `jutsu.*`, `item.*`, `asset.*`, `bloodline.*`, and
  `ai.updateAiProfile`

The report's headline conclusion — that the two halves of building an AI sit on opposite
sides of the boundary — survives and is if anything sharper: `profile.create` and
`profile.updateAi` are both reachable, `ai.updateAiProfile` is not.

Reported as mechanism only. Whether a non-browser client is sanctioned is not a source
question and stays reserved.

---

## 3. My own weak points

- **Coverage is ~10 percent of the claim set.** V3 (generator defect), V4 (`.strict()`
  population), V5 (G7 adjudication) and all of section 2's load-bearing positives except the
  transformer were not reached. Anyone reading this as a full pass is misreading it.
- The 39-hit limiter population is a raw `grep -rn` count across `src/`, including import
  lines. The 7-file breakdown is reliable; treat 39 as an upper bound on call sites.
- I checked `item.splitStack` as the one worked example of a call-site limiter on a content
  router. I did not enumerate the other six files' call sites.
- The mcp_boundary re-derivation used a block-boundary regex of the same family that produced
  the audit's own misclassification. I hand-verified `item.get` and `profile.create` at source
  afterwards; the rest of the re-derived list is machine-derived and unconfirmed.
- I wrote the original audit dispatch. That is a bias toward finding the audit's scope
  reasonable, and it is a reason to still run the fresh independent pass this file does not
  replace.

No architecture recommendation, and no conclusion about whether a non-browser client is
permitted. Both reserved.
