# Forge Next Phase 1 — implementation handoff (frozen)

**Status:** FROZEN FOR INDEPENDENT REVIEW
**Date:** 2026-09-17
**Implementation owner:** Fable / Claude Code
**Independent reviewer:** ChatGPT
**Governing contract:** `state/prompt_forge_next_phase1.md` (READY / FROZEN)
**Live-game policy observed:** ZERO LIVE REQUESTS / ZERO LIVE WRITES

## 1. Repository and refs

| field | value |
|---|---|
| repository | `perseverance484/tnr-tools` |
| implementation branch | `fable/forge-next-phase1` (identical commit also on `claude/forge-next-phase1-uwhcn1`, the session's assigned branch) |
| base / merge-base | `77f02c30f7714eb8506ace8802904cb351a70d34` |
| **implementation head (code audit target)** | `8f15416d510eeb53aa82f7b8b09b7ce00accfa83` |
| branch head | the docs commit that adds this file, and any later commit that only records the CI result. Nothing above `8f15416` changes code, tests, fixtures or the bundle. |
| intended integration target | current `main` |

`main` was reverified as `77f02c30f7714eb8506ace8802904cb351a70d34` at implementation start, which is
the commit the brief was frozen at. The branch is a fast-forward from it; there is no merge commit
and no rebase.

**`main` has since advanced to `015583ba581388ed53770cb3a2ce7ad899cad6e3`** (`eb848fc` archive the
pre-Forge global digest, `015583b` close the Phase 0 session). Those two commits touch
`state/active-context.md`, `state/digest.json`, `state/status.json` and one new `archive/` file:
Lane B session bookkeeping with **zero overlap** with this branch, which touches only `forge/`,
`forge_bundle.js` and `docs/handoffs/`. The branch was deliberately NOT rebased or merged — no
synchronization is required, and the frozen SHA stays stable for the audit. Integration is a clean
merge; the merge-base above is still the honest one.

Two commits, in this order:

| SHA | commit |
|---|---|
| `f6a244b` | `build(forge): raise the bundle budget ratchet for Phase 1` — the ceiling change alone, per brief section 10 |
| `8f15416` | `feat(forge): Phase 1 research capture tiers and audited research-read registry` |

Both are green independently; `f6a244b` was verified in a detached worktree (343/343, bundle
reproducible, raw 417,370 / 460,000).

## 2. Objective

Make Forge a bounded research/evidence tool: captures carry an explicit persistence tier, research
reads are admitted only from an audited demand-driven registry, and filtered/paged reads bind cache
identity and provenance to the exact canonical input sent.

## 3. Changed surfaces

**New**

- `forge/src/research/registry.mjs` — the research-read registry and tier policy. A new top-level
  layer rather than an addition to `transport/procedures.mjs`, because brief section 5.2 requires
  product/privacy admission to be a different authority from source-derived transport facts.
  Registered as an execution layer in `tools/check_imports.mjs`; deliberately NOT added to
  `NETWORK_ALLOWED`, so a policy module can never issue a request.
- `forge/tools/derive_registry.mjs` + `forge/RESEARCH_REGISTRY.md` — a generated descriptor of the
  registry, held equal to the module by a test so the readable table cannot drift from the code.
- `forge/test/research.registry.test.mjs`, `research.tiers.test.mjs`, `research.paging.test.mjs`.
- `forge/test/fixtures/screens/manifests_selected_research.txt`, `run_finished_research.txt`.

**Changed**

- `forge/src/transport/procedures.mjs` — two additive audited rows (below). 43 → 45.
- `forge/src/budget/reader.mjs` — `query()` and `_page()`; `readInput` now delegates to the
  registry's canonical input, so one representation feeds identity, transport and provenance.
- `forge/src/storage/captures.mjs` — query-keyed cache rows, tier/projection/page on snapshots,
  `MAX_LOCAL_CAPTURE_BYTES`, `FULL_PERSIST_PATHS` derived from the registry rather than restated.
- `forge/src/runner/manifest.mjs` — tier/projection/page capture grammar and its validation.
- `forge/src/runner/runner.mjs` — read-mode dispatch, per-page evidence, `_persistFull` → `_persist`.
- `forge/src/core/results.mjs` — tier-aware, leak-proof materialization.
- `forge/src/core/facts.mjs`, `forge/src/ui/screens.mjs` — tier-aware labels, pre-read tier banners,
  per-page walk evidence. No visual redesign.
- `forge/src/storage/journal.mjs` — **two-line generalization only** of `captureOk`/`jobOutcome`
  from `persist === "full"` to "any tier", plus "an incomplete walk is never green". Journal
  redesign is out of scope and none was done; this is flagged because section 8 does not list
  `journal.mjs` and the change was required for honest verdicts (objective 5).
- `forge/tools/check_imports.mjs`, `check_boundaries.mjs`, `check_bundle_budget.mjs`.
- `forge/test/auth.test.mjs`, `transport.client.test.mjs` — table-shape ratchets 43 → 45,
  `PROTECTED_PATHS` 27 → 29, with the new rows asserted explicitly rather than only counted.
- `forge/test/capture.full.test.mjs` — four message-shape expectations updated. Every guarantee is
  unchanged; the refusals are now earlier and more specific. Worth attacking (section 8 below).
- `forge/test/fakegame.mjs`, `screen_scenarios.mjs`, `gates.test.mjs`.
- `forge_bundle.js` — rebuilt from source.

## 4. Research registry additions and source evidence

Audited against a read-only checkout of `studie-tech/TheNinjaRPG` at the declared pin
`345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9`. **The pin was not moved.**

| path | facts | evidence |
|---|---|---|
| `combat.getBattleEntries` | `query`, `protected`, limiter **no**, mcp yes | `app/src/server/api/routers/combat.ts:382`. Input `battleId` required; `refreshKey? checkBattle? limit? offset? userFilter?("all"\|"user"\|"opponents") showBasicActions?`. Offset paged: `limit ?? 30` (`:397`), `offset ?? 0` (`:417`), ordered `battleRound desc, battleVersion desc` (`:420`). |
| `combat.getBattleHistory` | `query`, `protected`, limiter **no**, mcp yes | `app/src/server/api/routers/combat.ts:530`. Input `userId? secondsBack? combatTypes?(BattleTypes[])`. **No pagination at source**; filtered, ordered `createdAt desc`, joined `with: {attacker, defender}` on `{username, userId, avatar}` (`:553-556`). |

Limiter status is a measurement, not an inference: `.use(ratelimitMiddleware)` occurs in `combat.ts`
at `:565`, `:898`, `:960`, `:1410` and `:1506` only, none of which is either procedure.
`protectedProcedure = enforceUserIsAuthed + sentryMiddleware` (`trpc.ts:230`).
`BattleTypes` is `app/drizzle/constants.ts:539-557`; all seven values `push/05` uses are members.

Demand is the two committed research manifests and nothing else: `push/05` calls
`combat.getBattleHistory`, `push/06` calls `combat.getBattleEntries` 43 times. No other
non-content path was admitted.

The registry also transcribes the reads Phase 0 already allowed — the seven repo-safe content point
reads (exactly the old `FULL_PERSIST_PATHS`, now derived from the registry) and the six name lists
at `local-only`. That is a transcription plus a tier, not a widening.

## 5. Tier policy as implemented

- Order narrow → wide: `local-only` < `projected` < `repo-safe`. A row's tier is its **default and
  its ceiling**; a manifest may ask for that tier or a narrower one. Widening needs a registry edit.
- `persist` accepts `summary` (default, no body kept), `full` (accepted alias for `repo-safe`, so
  every committed manifest parses and **hashes** unchanged), `repo-safe`, `local-only`, `projected`.
- The tier is written onto the snapshot. Export takes the **narrower** of snapshot and journal, so a
  stale or edited journal entry cannot widen an export. There is a test that forges exactly that.
- `local-only`: exact body retained in IndexedDB, absent from bundle, embedded journal, export
  payload, GitHub commit and localStorage. Asserted by substring-searching all of those for a
  distinctive token, not by checking for a missing key.
- `projected`: raw body stays local; export carries a freshly derived projection of the declared
  paths. An absent declared path is a projection failure with the field names; the full body is
  never substituted. Wildcards, indexes, empty segments and `__proto__`/`constructor`/`prototype`
  are refused at parse.
- Projection admission is direction-aware: on a `repo-safe` row a projection can only **narrow** an
  already-admitted body, so any well-formed path is accepted; on a narrower row it would **widen**
  what leaves the machine, so it is admitted only from the row's explicit `project` allowlist —
  which is `null` on every non-content row today.
- Ceilings: `repo-safe` keeps 512 KiB; `local-only`/`projected` get 8 MiB, because nothing local is
  committed and the risk being bounded is a runaway IndexedDB write, not a repository commit. Over
  either ceiling is an explicit failure; nothing truncates.

## 6. Pagination and cache identity

- `canonicalInput(path, input)` validates against the row's audited contract (unknown key, missing
  required, wrong type, value outside an enum are all refused **before transport**) and emits keys
  in the registry's declaration order. Absent optionals stay absent — no invented defaults, so the
  stored provenance equals what the server was sent.
- Query cache key is `` `${path}?${canonicalJson}` ``: the **whole serialization**, not a digest. A
  32-bit hash of an unbounded input space can collide, and a collision would answer one filter's
  read with another's body under a green provenance.
- Query rows carry `id: null`, so a write to an entity invalidates them exactly as it does list
  captures.
- A walk stops at a short page, a failed page, or its declared bound — whichever is first. Bounds:
  the manifest's `pages`, the row's audited `maxLimit` (500 for `getBattleEntries`), and
  `MAX_PAGES = 20`. A walk that stopped on its bound with a full page is reported `complete: false`,
  is not persisted as a whole body, and makes the job non-green.
- A rate-limited page pauses the job through the existing budget path; the capture is not journaled
  as finished and the pass resumes at it.

## 7. Verification — exact commands and results

Run from `forge/`, Node v22.22.2, after `npm ci`:

| command | result |
|---|---|
| `npm audit --omit=dev --audit-level=high` | found 0 vulnerabilities |
| `node tools/check_imports.mjs` | 38 modules, 67 cross-layer imports, **0 violations** |
| `node tools/check_boundaries.mjs` | 38 modules, pin `345d18ac…`, **0 violations** |
| `npm test` | **381 tests, 381 pass, 0 fail** (Phase 0 baseline 343/343, verified on `main` before starting) |
| `npm run fixtures` then `git diff --exit-code -- test/fixtures/envelope` | clean |
| `npm run fixtures` then `git diff --exit-code -- test/fixtures/screens` | clean; all **12** Phase 0 fixtures byte-identical, 2 added |
| `npm run build` then `git diff --exit-code -- ../forge_bundle.js` | clean — bundle reproducible from source |
| `node tools/check_bundle_budget.mjs` | raw 446,372 / 460,000 (97.0%), gzip 87,450 / 90,000 (97.2%) |
| `node tools/derive_registry.mjs` | `RESEARCH_REGISTRY.md` reproducible; held by a test |
| `node -e "…checkReleasePin()…"` | release pin clean |

Bundle before/after: raw **417,370 → 446,372** (+29,002), gzip **79,294 → 87,450** (+8,156).
Budget-ratchet commit: **`f6a244b`**.

New tests: 38 (343 → 381), across registry admission and provenance, canonical input, tier
behaviour end to end, leak sweeps, paging and cache identity, plus two red tests for the new view
boundary gate and one for the metadata listings staying body-free.

**Canonical Forge CI: run `35255548523`, job `verify` (`105318155721`) — conclusion `success`**, on
head `31559fe` of `claude/forge-next-phase1-uwhcn1`.
<https://github.com/perseverance484/tnr-tools/actions/runs/35255548523>

All twelve steps ran and passed, none skipped: checkout, setup-node, `npm ci`, audit runtime
dependencies, import direction, static boundaries, `npm test`, verify generated fixtures, verify
checked bundle, bundle size budget, report release pin state.

## 8. Known debt, deviations, and what to attack

1. **`journal.mjs` touched** though section 8 does not list it. Two predicate lines, no redesign.
   Justified by objective 5, flagged rather than buried.
2. **Four expectation changes in `capture.full.test.mjs`.** Each refusal still happens at parse with
   nothing sent; the reasons moved earlier and got sharper. This is the change most worth attacking:
   confirm no guarantee was relaxed to make a test pass.
3. **`projected` has no production row that widens.** Every non-content row has `project: null`, so
   projection is reachable today only where it narrows a repo-safe body. This is deliberate
   fail-closed behaviour, and it means the widening path is exercised only by refusal tests.
4. **`push/05`'s `select` is not applied.** Its declared fields include `attacker`/`defender`
   player names. It parses and runs, and emits an advisory saying no projection is applied. See
   open decisions below.
5. **`gameAsset.getAllFolders`** appears once in `harvests/` but in no committed `push/` manifest,
   so it was not admitted. Demand-driven, recorded here rather than silently added.
6. **`.getAll` paged list dumps** (`quests.getAll`, `gameAsset.getAll`, …) remain unsupported.
   `CachedReader.list()` still refuses them. Builder-era harvest evidence exists, but no committed
   manifest demands them, and their `{limit, cursor}` shape was not audited in this pass.
7. **The 8 MiB local ceiling is a judgement call**, argued from the largest body the committed
   manifests ask for. It is not derived from a measured browser limit.
8. **`MAX_PAGES = 20` and `maxLimit = 500`** are Forge's bounds, not the server's — source imposes
   neither. Both are argued in the registry module.
9. **A new top-level `src/research/` layer** is not literally in the section 8 file list. Rationale
   in section 3; if the reviewer prefers it inside an existing layer, the move is mechanical.

## 9. Source and provenance

- Game source pin used for all registry audits: `345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9`.
  **Not moved.** `fields.json` and `nested.json` are untouched and still carry it;
  `check_boundaries.mjs` now holds the registry's declared pin equal to theirs.
- Current upstream head inspected: `studie-tech/TheNinjaRPG@1fd355ab92cec78148130e02c8d38834836c3181`
  — the head the brief recorded at freeze; it has not moved.
- **Drift check:** `combat.ts:382-402` and `:530-560` are byte-identical at the pin and at upstream,
  as is `BattleTypes`. No source-pin adoption task is required by this phase, and none was opened.
- Generated artefacts rebuilt: `forge_bundle.js`, `test/fixtures/envelope`, `test/fixtures/screens`,
  `forge/RESEARCH_REGISTRY.md`. No generated contract was regenerated or adopted.
- Fixtures/captures consumed: all 14 committed `push/*.json` manifests were parsed against the new
  grammar (all still parse); `push/05` and `push/06` supplied the demand evidence.

## 10. Live-game statement

- Live requests: **none.**
- Live writes: **none.**
- Live credentials or session material obtained, requested or used: **none.**
- Browser checks not performed: Forge was not loaded in a real browser; no ViolentMonkey/userscript
  run, no real IndexedDB (fake-indexeddb only), no real Clerk session, no real tRPC transport, no
  visual check of the two new banners or the retained-captures list outside the serialized fixtures.
- The game source was read from a read-only checkout at the pinned SHA. That is a GitHub source
  read, not a game request.

## 11. What explicitly has not begun

Phase 2 visual shell / design system, Phase 3 manifest UX, Quest Studio integration (Phase S
remains accepted at `chatgpt/forge-quest-studio-foundation@5ba636d8…` and was not merged, read or
modified), Content Admin, Publish, Project Workspace, Builder retirement, and any game-source pin
adoption.

## 12. Open user-owned decisions

1. **Whether `combat.getBattleHistory` may project player-identifying fields into the repository.**
   `push/05` asks for `attacker` and `defender` (usernames) and `attackedId`/`defenderId`. Its own
   note says the editorial pass must anonymize names as ANBU MEMBER. Admitting those fields for
   repository export is a publishing/privacy call, so the row ships at `local-only` with no
   `project` allowlist and the manifest's `select` is not applied. Options: (a) leave as is and
   anonymize downstream from the local body; (b) admit only the non-name fields
   (`battleId, battleType, createdAt`); (c) admit the id fields too; (d) admit the names.
   Implementing any of (b)–(d) is a one-row registry edit plus a test.
2. **Whether the name-list rows should be `repo-safe`.** They return only ids and names and are
   substantively harmless, but they were never repo-safe in Phase 0, so they were not widened.

## 13. Freeze

`8f15416d510eeb53aa82f7b8b09b7ce00accfa83` is frozen until independent review returns: no commit
after it touches `forge/`, `forge_bundle.js` or any other executable surface, so the branch head and
the implementation head are the same code. Phase 2 will not begin automatically.
