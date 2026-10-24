# Fable implementation brief — `elementaldamage` weapon census and full-record capture

**Date:** 2026-10-20  
**Status:** DIRECTOR-REQUESTED IMPLEMENTATION HANDOFF; no capture jobs built or run in this workstream yet  
**Implementation owner:** Fable / Claude Code (Forge/capture tooling, then routine capture-manifest generation)  
**Independent reviewer:** ChatGPT (Engineering Auditor; Content Designer lens)  
**Operator:** Director alone performs any live-game reads and subsequent item proposals/edits.

## 1. Exact evidence and authority

| Surface | Verified reference |
| --- | --- |
| Repository/base | `perseverance484/tnr-tools` `main@383ac0f45bc47004a4a8915f4c724c79b35798f3` |
| Upstream source | `studie-tech/TheNinjaRPG@6524d0fbd7c0b80ecfd28ca63e9c4becdfb210eb` (public source, **not confirmed deployed production SHA**) |
| Operator capture | `harvests/inbox/tnr_results_1792478135730.json` (Forge 0.8.0; three `ok:true`, `persistOk:true` point-read bodies) |
| Existing case report | `docs/reviews/ELEMENTALDAMAGE_GODSTORM_CAPTURE_FINDINGS_20261020.md` at PR #72 `dcccb8a7b7bade48993ceb98a2a9db2fd1450cef` (**open**, not part of baseline) |
| Specific repair | `push/131_stormrender_highest_scaling_suggestion.json` and `docs/reviews/STORMRENDER_HIGHEST_SCALING_MANIFEST_GATE_20261020.md` at PR #73 `590c0d8968d21aa53713276ef2faacf2fb42b84c` (**draft/blocked**, not part of baseline) |
| Prior capture workflow | `push/130_elementaldamage_godstorm_three_record_capture.json` and PR #71 (merged) |
| Governing procedures | `docs/00_INDEX.md`, `docs/DOCTRINE.md`, `docs/ENGINE_LAWS.md`, `docs/RULINGS.md`, `CLAUDE.md`, `docs/DEVELOPMENT_WORKFLOW.md` |
| Routed item and capture guidance | `skills/building-tnr-content/references/item.md` and `references/pipeline.md`; `docs/workflows/IMPLEMENTATION_HANDOFF.md` and `FABLE_REVIEW.md` |

The director asks for a **complete capture of other affected weapons** to support subsequent repairs. The director approved **Stormrender's** specific Highest-equivalent scaling correction, but has **not pre-approved blanket repairs or unreviewed balance changes for other items**.

## 2. Outcome — exhaustive, operator-run, read-only

Implement a repeatable workflow that, when the director triggers it in Forge, determines **all current `WEAPON` item records containing any `elementaldamage` effect**, regardless of visibility, rarity, shop status, equip slot, creation date or name. Produce immutable source-faithful full item records and a reproducible, reviewable affected-candidate ledger. **Zero content mutations and zero player/private/profile/account data** in this capture.

**Required completeness:** all current `itemType:"WEAPON"` records, **`hidden:false` AND `hidden:true`**, all pages to `nextCursor:null`. Inspect each returned record's `effects` array; do not assume that old seed catalog entries or `getAllNames` carry effect contents or the current full population. Cross-check the complete inventory against filtered spot-checks when useful.

The census covers **all `elementaldamage` WEAPON effects**, not only ones that appear broken, so correctly configured weapons act as controls. Produce a separate shortlist of the **formula-scaling-risk candidates** rather than implying every dynamic-element weapon needs a change.

The earlier `Stormrender` ID `cLXXf8RJv5l9B_gGsYN2a` is an expected positive control. List it in the complete census, but mark **ALREADY STAGED / PR #73** in the proposed repair inventory to prevent duplicate submissions.

## 3. Source-supported discovery (not yet Forge-capturable as a complete export)

**Game's actual list contract:** `app/src/server/api/routers/item.ts:1098-1133` exposes public `item.getAll`, input `{itemType:"WEAPON",hidden:<boolean>,limit,cursor}`, returning `{data:[item records],nextCursor}`; max limit **500** (`app/src/validators/item.ts:55-92`). Source sorts by `cost`, `repsCost`, then `id`, and uses **offset/cursor pages**. Explicitly pass `hidden`; otherwise `itemDatabaseFilter` defaults to **hidden:false**, silently omitting hidden content (`item.ts:4395-4458`).

Run both visibility partitions, using conservative pages (e.g. `limit:100`) and following the server's `nextCursor`, not a guessed item count:

```json
{"itemType":"WEAPON","hidden":false,"limit":100,"cursor":0}
{"itemType":"WEAPON","hidden":true,"limit":100,"cursor":0}
```

`item.getAll` also supports `effect:["elementaldamage"]`, but its `JSON_SEARCH` checks **any matching JSON string anywhere in the effects body**, not necessarily `effects[*].type`. Filtering alone is insufficient proof of exact tag identity; perform an exact parsed-tag check. An **unfiltered WEAPON crawl** is preferable as the exhaustive denominator; an effect-filtered crawl can be a cross-check.

**IMPORTANT BLOCKER #1:** Generic Forge `CachedReader.list` at `forge/src/budget/reader.mjs` refuses `item.getAll` (`list()` is restricted to `*.getAllNames` and special skill-tree inventory). A generic `capture.before` entry for `item.getAll` will therefore **not** perform the expected pagination.

**IMPORTANT BLOCKER #2:** Forge `persist:"full"` currently allows **only audited content-record POINT READS**; `item.getAll` and `item.getAllNames` are intentionally excluded by `forge/src/storage/captures.mjs` and `forge/src/runner/manifest.mjs`. Existing summary-list captures do not export the raw list body/IDs. **Do not broaden global `FULL_PERSIST_PATHS` to arbitrary lists** just to implement this task, and do not pass off a summary-list bundle as an item census.

**Recommended narrow design:** Add an explicitly audited read-only Forge item-census flow (or an equivalently complete and reviewed operator workflow) that uses the existing `item.getAll` query/limiter for **ID discovery**, performs a stable complete scan of both hidden partitions, then uses allowed `item.get {id}` point reads with `persist:"full"` for every discovered `elementaldamage` WEAPON. The `skillTree.getAll` complete inventory implementation in `forge/src/budget/reader.mjs` is a precedent for validating pages, deduplicating IDs and double-scanning an offset-paginated source for stability. **Keep the current full-persistence security boundary unchanged.**

Architecture choice belongs to Fable provided these invariants hold. If existing tooling admits a simpler workflow without code changes, demonstrate exhaustive provenance and full exported record bodies; do not default to the known-stale 766-row seed as if it is exhaustive.

## 4. Two-stage evidence / operator flow

**Stage A — inventory discovery:** operator explicitly starts a read-only Forge census. It enumerates every WEAPON record in both visibility partitions, tracks `id`, `itemType`, `hidden`, `updatedAt`, `effects` type list, pagination provenance and a stable deterministic inventory digest. Reject or flag failed pages, malformed `{data,nextCursor}`, repeated IDs, unexpected type, missing partitions, non-monotonic cursor, or mid-scan changes. Ideally perform two full source reads and compare stable ordered ID+relevant-field snapshots; do not label an unstable single pass complete. The read-only inventory must be operator-exportable or feed directly into Stage B without requiring the director to manually copy IDs.

**Stage B — full point reads:** every WEAPON whose parsed `effects` contains `type:"elementaldamage"` receives one `item.get` full-body capture with `persist:"full"` under the existing allowlist. Fetch **all** dynamic-element weapons, not only candidate failures. Prefer automatic generation/execution inside a reviewed Forge census job; multiple generated `items:[]` point-capture manifests are acceptable if the operator can execute/export them safely. Preserve exact `effects`, `id`, `updatedAt` and all original item fields. Check captured current `updatedAt` against Stage A; a drifted row is **STALE/RECAPTURE REQUIRED**.

Capture acceptance is **per point**: `ok:true`, `rows:1`, `persist:"full"`, `persistOk:true`, non-null full `data`, `data.id === requested id`, `data.itemType === "WEAPON"`, and an intact `effects` array. Missing captures/persistence are hard failures, never silently dropped. Snapshot records are immutable (existing `capture_snapshots` contract); exports must not re-query on demand or replace earlier results from mutable caches. Obey the **512-KiB per-record** limit and size/split results bundles conservatively if needed.

**No Stage A or B actor may submit `item.update`, content-review proposals, create, equip, edit, or other mutation.** No agent uses live credentials or sends live-game requests; Fable implements and tests offline, director executes in Forge.

## 5. Machine-readable affected-candidate ledger

From the COMPLETE point-read population emit a deterministic item-ID-keyed ledger (JSON, plus readable summary), with for each WEAPON:

- exact item `id`, name, rarity, `hidden`, `updatedAt`, effect position(s), full original effect values or evidence pointer/hash, originating capture bundle/path/SHA and capture timestamp;
- actual `elementaldamage` calculation type, power, `statTypes`, `generalTypes`, `allowBloodlineDamageIncrease`, element-selection implications, and other rider effects **for context**;
- `formula / missing statTypes`, `formula / missing generalTypes`, `formula / both missing`, `formula / both present`, `non-formula / scaling not applicable`, `malformed or ambiguous`, and `already-staged Stormrender` classifications;
- explicit **observed evidence vs proposed repair** distinction. A missing field is a **candidate**, not proof of unintended content design. No auto-approval of repairs.

**Critical engine nuance:** `statTypes:[]` and absent are stat-scaling-negative; a **nonempty** `statTypes:["None"]` is stat-scaling-positive. New game `app/src/validators/combat.ts:156-169` normalizes raw legacy `["Highest"]` to `["None"]` on save; source `damageCalc` checks whether the stat array is nonempty to enable Offence/Defence (`tags.ts:1438-1447`). For generals, `generalTypes:["Highest"]` dynamically contributes the player's highest generals. Do not misdiagnose `["None"]` as missing or blindly overwrite intentionally restricted selectors.

Treat non-`formula` dynamic tags as captured **out of scope for this particular scaling defect**. Exclude ordinary `damage` tags from the automatic affected list, but compare them as contextual controls. Multiple dynamic damage tags per item must be assessed independently.

**Outputs:** exact-total row counts for both visibility partitions; dynamic-weapon IDs/captured count; candidates by classification; known-good controls; errors/staleness/missing IDs; zero-mutation proof; an auditable list for director's approval. Do not invent a candidate count ahead of the capture.

## 6. Safety, edge cases and validation

- **Live-source fidelity:** verify each returned `item.getAll` row is a `WEAPON`, and each `item.get` record is the same ID. Do not infer absence from seed `harvests/seed/41_INDEX_item.json` (766-row, historical, unknown newest record). A clean zero-match census is valid only with complete pages and stable source passes.
- **Pagination safety:** handle both hidden states, empty first page, exact-multiple-of-page-size terminating empty page, >1 page, duplicate/reordered/shifted rows, null cursor termination, and malformed cursors. Offset pagination can skip rows under live edits; stable rescans and/or explicit drift verdicts are necessary.
- **Budget & resume:** `item.getAll` and `item.get` are public rate-limited queries (`forge/src/transport/procedures.mjs`). Use `forge/src/budget/bucket.mjs`'s existing safety margin (**30 per path per minute**, 60 server ceiling), persistence and 429 pause/resume behavior; never bypass it with direct `fetch`, parallel unbudgeted requests, or a separate token. On reload/partial completion do not lose already-exportable immutable point-read evidence or mislabel an incomplete scan COMPLETE.
- **Privacy/boundaries:** queries only for public item content. No player profiles, ownership/inventory, user IDs, cookies or account fields in bundled evidence. Do not generalize full-persist to unfiltered list endpoints. Browser/preflight must clearly show **0 writes**, exact planned read scope and counts, incomplete/error states.
- **Reproducible build:** add offline mocks/fixtures for mixed WEAPON/OTHER, visible/hidden, >1 page, effect `elementaldamage` vs a coincidental description-string match, absent/empty/None/Highest selector cases, multiple effects and non-formula, changing `updatedAt`, partial `persistOk:false`, stale snapshots, 429, resume and bundle-size/large-output behavior.
- **Verification:** run focused Forge tests and full relevant tests; regenerate/re-diff checked-in Forge output if source changes. If staging Forge capture manifests, **run `python3 scripts/validate.py <manifest>` and `node forge/tools/check_manifest.mjs <manifest>` with zero errors** per repository authority. State exact commands/results, pinned source/fixtures and known unverified browser behavior.
- **Release discipline:** Forge source changes are Lane A, on a Fable-owned implementation branch and handed back at an exact frozen SHA for independent review. The operator's later census/manifest runs are Lane B, separate from the code review. No feature release to live Forge without the ordinary reviewed integration process.

## 7. Separate downstream repair gate — not authorized here

PR #73 already stages the specific Stormrender correction in `mode:"suggest"`. It remains BLOCKED: `forge/src/runner/nested.json` and skill `45c/45g` are stale and fail-closed on the `elementaldamage` tag. This does **not** prevent implementing/validating read-only census behavior but **does** block repair submissions that assert an `elementaldamage` effects array.

**Do not modify PR #73's `chatgpt/*` branch; do not bypass its blocker.** Fable should coordinate the governed source-contract refresh as a separately reviewable Lane A dependency before any item repair manifest proceeds. After the census and evidence verification, submit an ID-level candidate review for director approval. Only then prepare specific minimal repairs using full captured effects, item fetch-merge and independent readback / content-review workflow. The director has not granted blanket write or suggest approval for newly discovered weapons.

## 8. Completion criteria and Fable handback

Complete this workstream when there is:

1. a reviewed **operator-runnable, fully read-only and exhaustive** Forge discovery + point-capture path, with a manifest/operator guide and exact source/model coverage;
2. audited output/test fixtures proving **both hidden partitions, all pages, full captured bodies, no unauthorized writes, and fail-closed incomplete states**;
3. after the director executes the capture, a reproducible machine-readable **candidate ledger with counts and provenance** keyed by item ID, excluding no controls;
4. a clear **STOP/REVIEW** gate before mass suggestion or edit manifests, with PR #73's existing Stormrender status accounted for;
5. a frozen Fable handoff containing branch/base/head, changed files, tests/builds and generators, game-source pin, evidence, pending operator steps, and live requests/writes/credentials statement.

**Review focus for ChatGPT:** truth of completeness claims, filtered/unfiltered/hidden semantics, list → id provenance, immutable capture evidence, limiter accounting and crash-resume, private data exclusion, generated contract compatibility, and whether the UX ever labels partial evidence as complete.

**Current activity:** ChatGPT only read the GitHub repository and game *source* via GitHub, authored this handoff on its own branch, and made **0/0 live-game requests/writes**. No list census or production capture has yet been run for this workstream.
