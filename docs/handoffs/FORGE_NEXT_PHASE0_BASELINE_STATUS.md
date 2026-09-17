# Forge Next Phase 0 — baseline, drift, and status

**Status: PHASE 0 NOT COMPLETE. This branch is NOT frozen and must not be treated as a
Phase 0 handoff.** What is finished is the mandatory pre-implementation baseline, the
game-source drift measurement, and one isolated baseline defect fix. The ForgeCore
extraction has not begun.

**Repository:** `perseverance484/tnr-tools`
**Implementation branch:** `fable/forge-next-phase0`
**Fresh-main base SHA:** `b42c2afd5ceb3cd2e1f1eaa6f1e082cfc419cbea`
**Merge-base with main:** `b42c2afd5ceb3cd2e1f1eaa6f1e082cfc419cbea` (branch is a direct descendant)
**Contract:** `chatgpt/forge-next-unified-contract@efbdc2a4a2f35b12b425ba88a4d415f66f79f2c0`
**Live requests: none. Live writes: none. Game-source modifications: none.**

---

## 1. Main reverification

The contract said main was last verified at `b42c2afd5ceb3cd2e1f1eaa6f1e082cfc419cbea` and told me
not to assume it was still current. Reverified at task start:

```
origin/main = b42c2afd5ceb3cd2e1f1eaa6f1e082cfc419cbea
2026-09-16 17:50:43 -0500  results: tnr_results_1789599042548.json (forge)
git rev-list --count b42c2afd..origin/main = 0
```

Unchanged. The branch was cut from that commit.

---

## 2. Baseline was RED on fresh main

This is the finding that changes the shape of the task. Before any refactor:

```
node v22.22.2   npm 10.9.7
npm ci    rc=0
npm test  310 tests / 309 pass / 1 FAIL / 0 cancelled / 0 skipped
```

**Failing test:** `forge/test/release_loader.test.mjs:47` —
*"release loader: exactly one @x-release-pending marker, naming the package version"*
`AssertionError: expected 1, actual 0`.

### Isolated diagnosis

The defect is in the test, not the loader, and the two rules in the repo contradict each other:

- `forge/test/release_loader.test.mjs:47` asserted **exactly one** `@x-release-pending` marker
  must always be present.
- `forge/tools/check_release_pin.mjs:68-69` treats a **surviving** marker as a blocker once
  `@version` equals `forge/package.json` — *"@x-release-pending … remains even though @version
  already equals …"*.

The marker is lifecycle state, not a constant. While a release is staged, the loader carries one
marker naming the next package version and keeps the last released `@version`. When
`.github/scripts/pin_release.py` promotes (line 32), it **strips the marker** and syncs `@version`.
Current main is in the promoted state: `@version 0.4.1`, `package.json 0.4.1`, zero markers —
which `checkReleasePin()` correctly reports as clean (the neighbouring test 192 passes).

So the suite went red the moment 0.4.1 was promoted. The test file's own header comment records
that it was written while a real marker existed and has been fragile for this reason before.

### Fix — isolated, in its own commit, not hidden in the refactor

**Commit `3b586b358ae7d2b4ee2f53bb5cfea32b58597a74`** — `forge/test/release_loader.test.mjs` only.

The test now asserts **at most one** marker (its own failure message says the risk being guarded
is a *second* marker shadowing the real one), and then asserts whichever lifecycle state the loader
is in is internally consistent:

- one marker → it names `PKG_VERSION` and `@version` still points at the last released version;
- zero markers → `@version` equals `PKG_VERSION`;
- either way → `checkReleasePin()` returns `[]`.

No production code touched. No other test weakened.

```
npm test  310 tests / 310 pass / 0 fail / 0 cancelled / 0 skipped
```

---

## 3. Baseline measurements (post-fix, on `3b586b3`)

| Measurement | Value |
|---|---|
| Node | v22.22.2 |
| npm | 10.9.7 |
| `npm ci` | rc=0 |
| `npm test` | **310 / 310 pass / 0 fail / 0 cancelled / 0 skipped** |
| `npm run fixtures` | rc=0 |
| `git diff --exit-code -- forge/test/fixtures/envelope` | **clean** |
| `npm run build` | rc=0 |
| `git status --porcelain forge_bundle.js` | **clean — no drift** |
| `forge_bundle.js` raw | **404,594 bytes** |
| deterministic gzip (`gzip -9 -n`) | **75,801 bytes** |
| `npm audit --omit=dev --audit-level=high` | **found 0 vulnerabilities** |
| `npm audit` full headline | **3 high severity vulnerabilities** — all dev-only, `node_modules/uploadthing` |
| `doctrinemap.py` | exit 0 |
| `render_doctrine.py --check` | exit 0 |
| `build_packs.py --check` | exit 0 |
| `lawmap.py .` | 93 laws / 93 matrix rows / 77 citations across 35 files — 0 errors, 5 warnings (pre-existing) |

These are the numbers any later extraction must reproduce.

---

## 4. Import-direction starting leak count: **zero**

Measured across `forge/src/{runner,storage,transport,budget,reconcile}` for imports reaching
`ui/` or `hosts/`:

```
prohibited imports on fresh main = 0
```

The execution→UI direction is already clean. The mechanical gate still has to be written and put in
CI — the requirement is not satisfied merely because the count is currently zero — and it becomes
load-bearing once `core/` exists, where the new prohibited edge is core→ui/hosts.

---

## 5. Game-source drift — measured only, nothing adopted

**Upstream head inspected:** `studie-tech/TheNinjaRPG@1fd355ab92cec78148130e02c8d38834836c3181`
(2026-09-16 17:58:16 +0200). This is **identical** to the head observed when the contract was
authored — `git rev-list --count 1fd355ab..origin/main = 0`. No new upstream movement since the
contract was written.

### Two different pins exist in this repo

| Artifact | Pin | Behind head |
|---|---|---|
| `forge/src/runner/fields.json` `_provenance.pin` | `345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9` (2026-08-31) | **154 commits** |
| `45c_DATA_constructors.json` `source_drop` | `bdec2883` (2026-08-29) | **243 commits** |

`bdec2883` is an ancestor of `345d18ac`. Worth naming because a reader can easily assume one pin
governs both surfaces; it does not.

### Forge-relevant drift, `345d18ac` → head

848 files changed upstream overall; **114** match Forge-relevant surfaces
(router/tRPC/procedure/auth/session/schema/validators). Of the routers Forge actually calls:

| Router | Change since the Forge contract pin |
|---|---|
| `item.ts` | **+120 / −63** — by far the largest |
| `asset.ts` | +20 / −10 |
| `bloodline.ts` | +11 / −14 |
| `village.ts` | +13 / −12 |
| `ai.ts` | +6 / −5 |
| `jutsu.ts` | +5 / −4 |
| `app/drizzle/schema.ts` + `app/src/validators/` | **+558 / −9** across 9 files |

### Procedure existence check — all present

All **43** procedures in `forge/src/transport/procedures.mjs` were checked against the routers at
upstream head. **Zero missing.** The drift is in field shapes and validators, not in the procedure
surface Forge addresses.

### Conclusion: no adoption is necessary to make the baseline truthful

`fields.json` correctly describes its own pin and that pin has not moved. The baseline is
internally consistent. Per the contract, **no pin was moved, no contract regenerated, no auth
semantics or procedure shapes changed, and no game source touched.** The shape drift above is real
standing debt and belongs to a separately scoped Lane A adoption task — the `item.ts` and
validator deltas in particular should not be absorbed silently.

---

## 6. Gap assessment for the work not yet done

Measured, so the remaining effort is estimated from the tree rather than guessed:

- **`forge/src` is 5,173 lines** across 24 modules; `ui/app.mjs` is 411 lines, `runner/runner.mjs`
  691, `storage/journal.mjs` 423. The extraction surface is smaller than the phase description
  implies, which is good news for feasibility.
- **Screen fixtures do not exist.** `forge/test/fixtures/` contains only `envelope`. The five
  released screens (`jobs`, `manifests`, `run`, `captures`, `settings`, enumerated at
  `ui/app.mjs:15`) have no deterministic serialization. The contract requires these to be
  established **before** the domain logic moves — they are the only thing that can prove
  byte-identity afterwards. This is the correct next step.
- **DOM hardening is absent.** `forge/src/ui/dom.mjs` carries only a comment — *"createElement and
  CSSOM only; no innerHTML anywhere (repo law)"* — with no mechanical rejection of `innerHTML`,
  `outerHTML`, `srcdoc` or `insertAdjacentHTML` for computed property assignment. The contract's
  conditional ("if equivalent protection is not already present") resolves to: it is not present,
  so it is in scope.

---

## 7. What has explicitly NOT begun

ForgeCore extraction (`forge/src/core/*`); host isolation (`forge/src/hosts/userscript/`); the
composition root rework in `main.mjs`; the mechanical import-direction gate; the runner
progress/event emitter; the five screen fixtures; DOM hardening; the separate repository/manifest
IndexedDB; CI consolidation.

Also not begun, and out of scope by instruction: Quest Studio integration, Phase 1, the visual
shell redesign, Content Admin, Builder retirement, release movement. No ChatGPT branch was
modified. No Studio code was cherry-picked or merged.

---

## 8. Recommendation

Two things need a decision before the extraction proceeds.

**The baseline defect should be reviewed on its own.** `3b586b3` is a one-file test change that
makes `main` green again, and it is independent of everything Phase 0 does. It is worth landing and
reviewing separately rather than arriving inside a large architecture diff — which is what the
contract's own instruction to isolate it was protecting against. Note that `main` is currently red
by this measure, so anything that gates on a green suite is gating on a stale assumption.

**The remaining extraction should run where it can iterate.** What is left is a refactor of the
orchestration layer under a byte-identity guarantee across five screens, plus a storage migration
with a rollback constraint. The measurements above say the surface is tractable, but the work needs
repeated build-test-compare cycles against fixtures that do not exist yet. Doing it in a session
that cannot iterate to convergence risks producing a branch that passes the gates it was given
while quietly changing behaviour the fixtures were never written to catch — a false success signal
on exactly the axis this phase is meant to protect. The honest sequence is: land the baseline fix,
establish the five screen fixtures and confirm them stable, and only then move domain logic.

I have not frozen this branch and make no completeness claim about Phase 0.
