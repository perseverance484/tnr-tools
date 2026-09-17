# Forge Next Phase 1 — correction pass handoff (frozen)

**Status:** FROZEN FOR INDEPENDENT RE-REVIEW
**Date:** 2026-09-17
**Implementation owner:** Fable / Claude Code
**Independent reviewer:** ChatGPT
**Governing contract:** `state/prompt_forge_next_phase1.md` (unchanged)
**Answers:** `docs/reviews/FORGE_NEXT_PHASE1_INDEPENDENT_REVIEW.md` — findings FN1–FN5
**Live-game policy observed:** ZERO LIVE REQUESTS / ZERO LIVE WRITES

## 1. Refs

| field | value |
|---|---|
| repository | `perseverance484/tnr-tools` |
| branches | `fable/forge-next-phase1` and `claude/forge-next-phase1-uwhcn1`, same commit |
| previous frozen target (reviewed) | `8f15416d510eeb53aa82f7b8b09b7ce00accfa83` |
| **new frozen head (correction target)** | `7bd8592f1d579f33d71c0713cfee4529cd691526` |
| base / merge-base | `77f02c30f7714eb8506ace8802904cb351a70d34` (unchanged) |

One commit: `7bd8592` `fix(forge): correct the five Phase 1 independent review findings`.
The correction diff against the reviewed target touches 14 files; `forge_bundle.js` is a rebuild.

## 2. Verdict on the review

**All five findings are accepted. All five reproduced at `8f15416` before any change was made.**
FN1 and FN2 are regressions this implementation introduced; FN3–FN5 are gaps against the brief.
Nothing was disputed, deferred or reinterpreted.

The reviewer's scope statements were checked and match: no finding claimed a currently admitted
non-content body escapes, and none did. The `__proto__` probe demonstrated bypassed field
validation, not global prototype pollution, and is fixed as the former.

## 3. What each correction does

### FN1 — a Phase 0 journal's full captures went silently bodyless

Root cause: `materialize()` and `captureOk()` keyed on `capture.tier`, which a record written by
`runner.mjs` at the base SHA does not carry. The reviewer is right that fresh-manifest alias
parsing is a different code path and does not restore completed records.

Correction: `captureTier()` in `forge/src/storage/captures.mjs` is now the single place that
decision is made, and `materialize`, `captureOk`, `jobOutcome`, `runHeadline` and both screens ask
it. Per the reviewer's constraint, the legacy mapping is narrow — only `persist: "full"`, the exact
shape the base runner wrote; every other tier-less record stays a summary capture. Two conservative
checks were added on top: a legacy record naming a path that is not an approved repo-safe one is
refused rather than interpreted, and a snapshot with no tier of its own is repo-safe only if its
path still is, otherwise it falls to the narrowest tier. Export re-reads the old snapshot and issues
no game read; recorded failures stay failures.

### FN2 — a journal projection could redirect an immutable declaration

Correction: the declaration retained beside the body is authority. The journal may only agree; any
difference is a non-success naming both lists, and nothing is exported. The retained declaration is
re-validated through `validateProjection` at the leak boundary, as a verdict rather than a throw, so
a withdrawn field or a hand-edited store fails the export instead of being applied or escaping into
the export fallback. A journal declaration can no longer widen or replace the retained one.

### FN3 — a declared path could stop on a structure and ship the subtree

Correction: a projection terminal must be a scalar or a list of scalars. A structured terminal is an
explicit projection failure naming the path. Descending *through* an array is supported, which is
how a per-element field is declared: `content.objectives.id` projects the named leaf out of each
element and nothing else, so a field added to the record later cannot ride along. No wildcard or
subtree escape hatch was added.

As the reviewer required, the Phase 1 test that codified the old behaviour is replaced rather than
relaxed, and the fixture scenario now declares a leaf path.

### FN4 — captures did not retain the contract that admitted them

Correction: `REGISTRY_REVISION` is a derived content identity over the pin, tiers, projectable
allowlists, input contracts and paging bounds, so a registry edit cannot leave it stale.
`capturePolicy(path)` stamps `{pin, registry, tier, source}` onto the journal entry and onto the
snapshot at capture time, and the export carries it. Per the reviewer's constraint, export never
fabricates provenance for an older record: a Phase 0 capture materializes with no `policy` key
rather than being relabelled with today's registry.

### FN5 — a later-page 429 lost the walk's per-page evidence

Correction: `budget.observe()` throws with the decoded element already in hand, so that element now
rides on the error; `query()` attaches every page walked plus the one that tripped; the runner
journals the abandoned attempt to an append-only `<phase>Attempts` list *before* the pause
propagates. The completed list is deliberately untouched — it is the resume cursor, so a resumed
attempt is a new record beside the abandoned one rather than an overwrite of it. Attempts reach the
exported bundle and the run screen. The rate-limit stop, the pause reason and the non-success
semantics are unchanged.

## 4. Regression coverage added

`forge/test/research.review.test.mjs`, 13 tests named after the findings:

| finding | tests |
|---|---|
| FN1 | base-era capture restores its exact body with one snapshot read; a recorded persistence failure stays failed for capture-only and mixed write jobs; missing and oversized legacy snapshots are explicit non-success with no re-read; the legacy mapping adopts nothing it does not recognise, including a legacy record on a non-repo-safe path |
| FN2 | seven journal redirections (extra field, replacement, empty, null, `__proto__`, `*`, trailing space) all withheld; retained declaration re-validated as a verdict; a snapshot with no declaration exports nothing |
| FN3 | object, nested-object and object-array terminals all fail with `missing` naming them and no partial object; leaf paths through an array succeed; a scalar list is a field; a later-added element field cannot ride along; descending through a scalar fails |
| FN4 | pin and revision on journal entry, snapshot and export; no fabrication for a pre-stamp record; the revision is a content identity |
| FN5 | 429 on page 2 keeps both pages with exact inputs and per-page verdicts, reaches the bundle, leaves the resume cursor untouched, and the job still pauses and is still `open`; a resumed attempt does not overwrite the abandoned one |

The base-era record shapes are transcribed into the test rather than produced, because the code that
wrote them no longer exists and a record in an operator's browser is all that is left of it.

## 5. Verification — exact commands and results

From `forge/`, Node v22.22.2, after `npm ci`:

| command | result |
|---|---|
| `npm test` | **394 tests, 394 pass, 0 fail** (381 at the reviewed target; +13) |
| `npm audit --omit=dev --audit-level=high` | found 0 vulnerabilities |
| `node tools/check_imports.mjs` | 38 modules, 70 cross-layer imports, **0 violations** |
| `node tools/check_boundaries.mjs` | 38 modules, pin `345d18ac…`, **0 violations** |
| `npm run fixtures` + `git diff --exit-code -- test/fixtures` | clean |
| `npm run build` + `git diff --exit-code -- ../forge_bundle.js` | clean |
| `node tools/derive_registry.mjs` + `git diff --exit-code -- RESEARCH_REGISTRY.md` | clean |
| `node tools/check_bundle_budget.mjs` | raw 452,000 / 460,000 (98.3%), gzip 88,963 / 90,000 (98.8%) |
| release pin check | clean |

**No further budget change.** The corrections fit inside the ratchet raised at `f6a244b`
(raw 446,372 → 452,000, +5,628; gzip 87,450 → 88,963, +1,513). Gzip headroom is now 1,037 bytes;
flagged in section 7.

All 12 Phase 0 screen fixtures remain byte-identical. One Phase 1 fixture moved,
`manifests_selected_research.txt`, because its scenario now declares a leaf path.

**Canonical Forge CI: run `35263303607`, job `verify` (`105344127640`) — conclusion `success`**, on
head `f34e5f8` (this handoff's own commit; the correction head `7bd8592` differs from it only by
these two Markdown files). <https://github.com/perseverance484/tnr-tools/actions/runs/35263303607>
All twelve steps ran and passed, none skipped.

## 6. Source and provenance

Unchanged and re-confirmed: registry pin `345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9`, not moved;
upstream head `1fd355ab92cec78148130e02c8d38834836c3181`; no generated contract regenerated or
adopted; no registry row added, removed or retiered by this pass. The reviewer's independent source
reading of `combat.ts:382`, `combat.ts:530` and `trpc.ts:230` agrees with the handoff's, including
the `secondsBack` correction (a truthy switch for a fixed three-hour cutoff, not an arbitrary
duration) — that field is accepted as an optional number and is not interpreted by Forge, so no code
change follows from it. `BattleTypes` moving from pinned line 539 to upstream line 608 with identical
content is noted and needs no action.

Regenerated artefacts: `forge_bundle.js`, screen fixtures, `forge/RESEARCH_REGISTRY.md` (which now
also prints `REGISTRY_REVISION`, so a stamped capture can be tied back to the table).

## 7. Known debt and what to attack

1. **Gzip headroom is 1,037 bytes (98.8%).** Inside the ratchet, so no raise was taken, but the next
   change of any size will need one.
2. **`<phase>Attempts` is new journal state** at journal version 1. It is additive and optional;
   `validateJobShape` ignores unknown keys and an older build reading it simply does not render the
   attempts. No migration was added.
3. **Abandoned attempts appear in the exported bundle** alongside completed captures, marked
   `abandoned: true` with a non-success verdict. `jobOutcome` reads the journal's completed lists, so
   a resumed job that later succeeds can export a success bundle that also carries the earlier
   failed attempt. That is intended as honest evidence; confirm it reads that way to a reviewer.
4. **Legacy interpretation is by shape, not by a version stamp.** `captureTier` infers a Phase 0
   record from `persist: "full"` with no tier. It is narrow and guarded, but it is still inference
   over old data; worth attacking for a record shape it would misread.
5. **Items 1, 5–9 of the previous handoff's debt list stand unchanged**, including the two open
   user-owned decisions in section 12 there, which this pass did not touch.

## 8. Live-game statement

- Live requests: **none.** Live writes: **none.** Credentials or session material: **none.**
- Browser checks not performed: unchanged from the previous handoff — no real browser, IndexedDB,
  Clerk session, userscript run or transport. The new abandoned-attempt row on the run screen is
  covered only by the serialized fixture and unit tests, not visually.
- The reviewer's probes were read, not executed in this session; every finding was independently
  reproduced against the frozen tree before being corrected.

## 9. What explicitly has not begun

Unchanged: Phase 2 visual shell, Phase 3 manifest UX, Quest Studio integration, Content Admin,
Publish, Project Workspace, Builder retirement, and any game-source pin adoption.

## 10. Freeze

`7bd8592f1d579f33d71c0713cfee4529cd691526` is frozen for independent re-review. Do not integrate
until re-review returns. Phase 2 will not begin automatically.
