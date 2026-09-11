# Forge protected-auth: source-pin reconciliation (FPA-3)

Answers independent review finding **FPA-3** on `chatgpt/review-forge-protected-auth`, which
rejected the first handoff for asserting task-pin compliance while deriving the auth table from a
different commit.

| | commit | role |
| --- | --- | --- |
| task pin | `bdec2883748f029a0ecb93505adfdcbae6851fe9` | pinned by `state/prompt_forge_protected_auth.md` |
| Forge's global pin | `345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9` | the commit the whole 0.2/0.3 Forge stack was audited against |

`345d18ac` is 89 commits after `bdec2883`, exactly as the review states.

**Neither pin was moved.** Forge's global pin stays `345d18ac`; the task's claims are now proven
against `bdec2883` as well. `docs/00_INDEX.md` gives the task-specific pin control over source
claims for a task that pins one, so the task pin is the authority below and the global pin is
shown alongside it.

## How this was produced

The game source was cloned read-only and both commits fetched; **no live game request was made,
nothing was executed from that checkout, and no credential was used.** The comparison is
reproducible with a committed tool rather than by prose:

```
node forge/tools/auth_pin_diff.mjs <checkout> <checkout> \
  --sha-a bdec2883748f029a0ecb93505adfdcbae6851fe9 \
  --sha-b 345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9
```

It re-derives the `publicProcedure` / `protectedProcedure` declaration of every procedure in the
seven content routers at each commit and compares both against
`forge/src/transport/procedures.mjs`. Exit 0 means no Forge path and no whole-surface
classification moved.

## 1. The auth table: identical at both pins

```
bdec2883: 164 procedures declared    345d18ac: 167 procedures declared

0 disagreement(s) across 43 Forge paths
0 procedure(s) changed auth class across the whole content surface
```

All 43 paths Forge can address carry the same class at both commits, and the class Forge records.
No procedure anywhere in the seven content routers was reclassified between the pins. The only
difference across the whole surface is three procedures **added** after `bdec2883`, all
`protectedProcedure`, none of them called by Forge:

- `profile.getSidebarTimers`
- `profile.updateTavernColor`
- `quests.getAchievementCatalogue`

An added procedure Forge does not call cannot change what Forge sends, so this is not a gap in the
gate. The review's spot check that `profile.getAi` agrees at both pins now holds for the full
table, which is what it asked for.

## 2. Every other fact this task rests on, checked at the task pin

Verified by reading `bdec2883` directly, not inferred:

| fact | evidence at `bdec2883` | vs `345d18ac` |
| --- | --- | --- |
| context takes `userId` from Clerk `auth()` | `app/src/server/api/trpc.ts:55-56` `const session = await auth(); const userId = session.userId;` | file byte-identical |
| `protectedProcedure` = `enforceUserIsAuthed`, throws `UNAUTHORIZED` | `trpc.ts:215`, `:222`, `:230` | file byte-identical |
| `publicProcedure` carries `ratelimitMiddleware`, `slidingWindow(60, "60 s")` | `trpc.ts:123`, `:211-212` | file byte-identical |
| browser tRPC client is same-origin `/api/trpc`, no Authorization header | `app/src/app/_trpc/Provider.tsx:92-94` | file byte-identical |
| valid routes render under `ClerkProvider` + `TrpcClientProvider` | `app/src/app/layout.tsx:73`, `:83` | provider lines identical; the file's one changed line is elsewhere |
| middleware returns early for every path but `/` | `app/src/proxy.ts:70` | file byte-identical |
| `experimental.globalNotFound` | `app/next.config.mjs:21` | present at both |
| `/forge` renders a providerless bare `<html><body>` | `app/src/app/global-not-found.tsx` (31 lines, no provider import) | file byte-identical |
| Forge's seven routers keep their names and mounts | `app/src/server/api/root.ts` | mount lines identical |

## 3. The carrier route, now source-verified rather than inferred

The first handoff justified `/` from repository-held evidence alone. Read at `bdec2883`:

- `app/src/app/page.tsx` is a real route rendering `HomeLanding`, so `/` is served by the root
  layout with `ClerkProvider` and `TrpcClientProvider` mounted — byte-identical at both pins;
- **the server does not redirect.** `app/src/proxy.ts` contains no `redirect` call at all; its `/`
  branch only ever *rewrites*, and the A/B rewrite is inside `if (!userId)` (`proxy.ts:101`), so
  for a signed-in operator the middleware callback falls through and `/` is served as `/`.
- **the client landing component does navigate after hydration.** Corrects a sentence in the first
  version of this document, which said the carrier "does no redirect and no extra work" on the
  strength of `proxy.ts` alone. `app/src/layout/HomeLanding.tsx:27-45` runs a `useEffect` that
  calls `router.push` once `useUserData()` resolves: `/profile` for a signed-in operator with
  character data, `/register` without it, `/500` on a user-data error
  (independent review round 2, FPA-3).

That client navigation does not disturb the repair, and the distinction is the point:

- it is a **client-side** `router.push`, not a document load. The document, the React root,
  `ClerkProvider` and `TrpcClientProvider` all stay mounted, which is the only property the
  carrier has to have;
- Forge's overlay is appended to `document.body` **outside** the Next root, so a route change
  inside that root does not touch it. Forge mounts as soon as the body exists, which is before
  hydration has resolved user data, and stays mounted across the push;
- activation is the per-tab marker, not the URL, so ending up on `/profile` (or `/register`) is
  not a miss. This is exactly the redirect case the route-agnostic marker was built for, and it is
  now a known behaviour rather than a hypothetical one.

The residual caveat is unchanged and belongs to the live smoke, not to source: `/profile` is a
busier page than `/`, so the carrier's own tRPC traffic — which Forge's budget cannot see — is
whatever that page reads, not whatever the landing page reads.

## 4. What is NOT claimed

- **Field lists are out of this task's scope and are not reconciled here.**
  `app/src/validators/combat.ts` and `objectives.ts` both changed between the pins, and
  `forge/src/runner/fields.json` / `nested.json` are derived from `345d18ac`. This task changed no
  validator, no field list and no pre-send validation, so nothing here depends on it — but it is a
  real open question for whichever pass next touches the derived contracts, and it is recorded
  rather than left implicit. `forge/tools/pin_relevance.mjs` is the tool for that question.
- Nothing was executed from the game checkout, and no browser or live-session behaviour was
  verified by reading source.
