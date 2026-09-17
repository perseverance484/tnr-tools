# Forge Next Phase 1 — second correction pass handoff (frozen)

**Status:** FROZEN FOR NARROW INDEPENDENT RE-REVIEW
**Date:** 2026-09-17
**Implementation owner:** Fable / Claude Code
**Independent reviewer:** ChatGPT
**Governing contract:** `state/prompt_forge_next_phase1.md` (unchanged)
**Answers:** `docs/reviews/FORGE_NEXT_PHASE1_CORRECTION_REREVIEW.md` — FN3-R1, FN4-R1, FN4-R2
**Live-game policy observed:** ZERO LIVE REQUESTS / ZERO LIVE WRITES

## 1. Refs

| field | value |
|---|---|
| repository | `perseverance484/tnr-tools` |
| branches | `fable/forge-next-phase1` and `claude/forge-next-phase1-uwhcn1`, same commit |
| first implementation target (reviewed) | `8f15416d510eeb53aa82f7b8b09b7ce00accfa83` |
| first correction target (re-reviewed) | `7bd8592f1d579f33d71c0713cfee4529cd691526` |
| **new frozen head (correction target)** | `9133145c1e626eb1611ac6a23302b58885c33fe6` |
| base / merge-base | `77f02c30f7714eb8506ace8802904cb351a70d34` (unchanged) |

Two commits, in this order:

| SHA | commit |
|---|---|
| `c12d693` | `build(forge): raise the bundle ratchet before the re-review corrections` — the ceiling change alone |
| `9133145` | `fix(forge): correct the three re-review findings FN3-R1, FN4-R1 and FN4-R2` |

Both are green independently. `c12d693` was measured against the then-current bundle
(raw 452,000 / 466,000, gzip 88,963 / 92,000) with the suite at 394/394.

## 2. Verdict on the re-review

**All three remaining findings are accepted.** All three reproduced at `7bd8592` before any change
was made. FN3-R1 is a regression the first correction introduced; FN4-R1 and FN4-R2 are incomplete
work in that same correction. Nothing was disputed or deferred.

The closures are noted and nothing in FN1, FN2 or FN5 was touched; their regressions still pass.

Two reviewer observations that needed no code change are accepted as stated:

- **FN2 null/absent journal copy.** The reviewer is right that a null or non-array journal
  projection falls back to the intact retained declaration and returns `{id:"q1"}` rather than
  `persistOk:false`, and that this is safe retained-authority behaviour rather than a redirection.
  The previous handoff's phrase "all seven redirections withheld" was loose; "withheld" meant the
  undeclared field never exported, not that every case returned a failure. Corrected here rather
  than in code.
- **FN5 abandoned-attempt outcome.** A later successful job correctly reporting `success` while
  retaining separately marked abandoned attempts is confirmed as the intended reading.

## 3. What each correction does

### FN3-R1 — an overlapping declaration silently dropped the deeper request

Root cause: `projectInto` groups declared paths by first segment; the terminal branch returned
without consulting the deeper group, so a scalar or scalar-list leaf took an early `continue` and
the descendant request disappeared. The reviewer's side-by-side is right that the previous frozen
projector rejected these, so this is a regression of the FN3 correction, not an inherited gap.

Both halves of the offered smallest correction are taken, because they guard different callers:

- `validateProjection` refuses a declaration that is a strict prefix of another. A value cannot be
  both a leaf and a structure, and resolving the pair either way discards something the manifest
  asked for, so it is refused rather than resolved. This fires at manifest parse **and** at the
  leak-boundary revalidation, since `materialize` re-validates the retained declaration.
- `projectInto` additionally records every unsatisfied deeper path in `missing` instead of dropping
  it, so `projectBody` called directly — past the declaration gate — is honest too.

A shared prefix that is not itself declared (`content.a` beside `content.b`) stays legal: those are
siblings, not an overlap.

### FN4-R1 — the revision omitted the facts that decide admission

The reviewer's sensitivity probes are correct and the previous claim did not hold. `policyFacts()`
now emits the complete admission contract as plain data — full input specifications including types
and enum members, projectable allowlists, per-row paging descriptors, and the global tier lattice,
default tier and page ceiling — and `revisionOf()` takes the identity over it.

Both are exported deliberately, so the property that matters can be tested directly rather than
asserted about the digest's shape. The revision moves from `35d2269b` to **`0657385d`**.

### FN4-R2 — summary captures and abandoned attempts were unstamped

`_persist` ran only when a tier was present, so an ordinary `persist: "summary"` research capture
carried no provenance, and `_journalAttempt` stamped none either. The stamp is now taken in
`_captures` **before** the entry splits into a summary, a persisted or an abandoned record, and
`_journalAttempt` stamps its own. Capture-time identity is unchanged in kind; old records are still
shown as carrying none rather than being backfilled from current policy.

## 4. Regression coverage added

Seven tests added to `forge/test/research.review.test.mjs` (13 → 20):

| finding | tests |
|---|---|
| FN3-R1 | six overlapping declarations refused at parse — scalar, scalar list, inside an object array, both declaration orders, structured terminal plus a leaf, and a multi-segment descendant — plus a control that an undeclared shared prefix stays legal; the projector records the unsatisfied path rather than dropping it; an overlapping retained declaration cannot reach a green capture or export |
| FN4-R1 | 13 probes — input field type, enum member withdrawn, enum member added, input key removed, required key made optional, global page ceiling, row maximum limit, row default limit, tier ordering, default tier, row tier, projectable allowlist, source pin — each must move the revision **and** land on a distinct value; equivalent policy data is stable |
| FN4-R2 | a summary capture carries the policy through journal and export while remaining bodyless; an abandoned attempt carries it through journal and export; all four research shapes in one job (summary, persisted, failed read, paged query) are stamped, with the legacy no-stamp control still holding |

The FN4-R1 probes are the reviewer's three plus ten more, and they assert distinctness rather than
mere inequality, so a derivation that collapsed two different contracts onto one identity would fail.

## 5. Verification — exact commands and results

From `forge/`, Node v22.22.2, after `npm ci`:

| command | result |
|---|---|
| `npm test` | **401 tests, 401 pass, 0 fail** (394 at the re-reviewed target; +7) |
| `npm audit --omit=dev --audit-level=high` | found 0 vulnerabilities |
| `node tools/check_imports.mjs` | 38 modules, 70 cross-layer imports, **0 violations** |
| `node tools/check_boundaries.mjs` | 38 modules, pin `345d18ac…`, **0 violations** |
| `npm run fixtures` + `git diff --exit-code -- test/fixtures` | clean — all 14 screen fixtures and the envelope fixtures byte-identical |
| `npm run build` + `git diff --exit-code -- ../forge_bundle.js` | clean |
| `node tools/derive_registry.mjs` + `git diff --exit-code -- RESEARCH_REGISTRY.md` | clean |
| `node tools/check_bundle_budget.mjs` | raw 453,086 / 466,000 (97.2%), gzip 89,296 / 92,000 (97.1%) |
| release pin check | clean |

**Budget raised, in its own commit `c12d693`.** At the previous ceilings the corrections measured
98.5% raw and **99.2% gzip — 704 bytes of headroom**. That passes, but it is a tripwire rather than
a ratchet: the next one-line comment would fail CI on a gate whose job is catching structural
regressions, and a control that cries wolf gets raised in a hurry by whoever is unblocking a build.
Measured delta over the previous pass: +6,714 raw / +1,846 gzip. The new ceilings restore the
tightness every prior pass ran at — 97.2% and 97.1%, against Phase 0's 97.1% / 97.9%.

**Canonical Forge CI: run `35267833732`, job `verify` (`105359335508`) — conclusion `success`**, on
head `dccd627` (this handoff's own commit; the correction head `9133145` differs from it only by
two Markdown files). <https://github.com/perseverance484/tnr-tools/actions/runs/35267833732>
All twelve gate steps ran and passed, none skipped.

## 6. Source and provenance

Unchanged: registry pin `345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9`, not moved; upstream head
`1fd355ab92cec78148130e02c8d38834836c3181`; no generated contract regenerated or adopted; **no
registry row added, removed or retiered**. The reviewer's statement that this correction does not
change admitted rows or the source-derived transport table holds for this pass too.

`REGISTRY_REVISION` changes `35d2269b` → `0657385d` because its *derivation* now covers the whole
contract. No admitted behaviour changed with it; the rows are identical. `RESEARCH_REGISTRY.md` is
regenerated to print the new value.

## 7. Known debt and what to attack

1. **The revision is a 32-bit FNV-1a digest.** It is an identity for change detection, not a
   cryptographic commitment; two different contracts could in principle collide. The 13 probes each
   land on a distinct value, but that is evidence, not a proof. If collision resistance is wanted,
   the derivation is one line.
2. **Overlap refusal is a policy choice, not the only one.** A reviewer could reasonably prefer
   "the deeper path wins and the leaf is dropped", or supporting both by emitting the leaf beside a
   nested object. Refusing keeps the manifest author's intent explicit, and it is the conservative
   reading of the brief's "absent or invalid declared paths yield non-success evidence".
3. **`policyFacts()` and `revisionOf()` are now public surface** on the registry module, exported so
   the identity's sensitivity is testable. They are pure and read-only.
4. **Items 1–5 of the previous correction handoff's debt list stand**, except that the gzip-headroom
   item is superseded by the raise above. The two open user-owned decisions in section 12 of the
   first implementation handoff are still open and untouched.

## 8. Live-game statement

- Live requests: **none.** Live writes: **none.** Credentials or session material: **none.**
- Browser checks not performed: unchanged — no real browser, IndexedDB, Clerk session, userscript
  run, clipboard or transport.
- The reviewer's harnesses were read, not executed in this session; each finding was independently
  reproduced against the frozen tree before being corrected.

## 9. What explicitly has not begun

Unchanged: Phase 2 visual shell, Phase 3 manifest UX, Quest Studio integration, Content Admin,
Publish, Project Workspace, Builder retirement, and any game-source pin adoption.

## 10. Freeze

`9133145c1e626eb1611ac6a23302b58885c33fe6` is frozen for narrow re-review of FN3-R1, FN4-R1 and
FN4-R2. Do not integrate until re-review returns. Phase 2 will not begin automatically.
