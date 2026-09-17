# Forge Next Phase 0 — correction round handoff

**Status: CORRECTIONS APPLIED. FROZEN.** Narrow re-review requested, per the review's own scope.

| | |
|---|---|
| Repository | `perseverance484/tnr-tools` |
| Implementation branch | `fable/forge-next-phase0` |
| Previous frozen head (reviewed) | `8be4c5bb6a89832e705be1281f90b2395cfd11d4` |
| Review | `chatgpt/review-forge-next-phase0@6df00b836d1af3b7b06f3689ca00648e03af51bd` — CORRECTIONS_REQUIRED |
| Base / merge-base | `b42c2afd5ceb3cd2e1f1eaa6f1e082cfc419cbea` (unchanged; still a direct descendant) |
| New frozen head | stamped in §6 |
| Live game requests / writes | **none** |
| Credentials used | repository PAT for clone and push only. No game credential or session. |

The correction round stayed inside the review's stated scope: the core boundary, the static gates,
and the workflow-install evidence. No Phase 1, no Studio integration, no shell redesign, no Content
Admin, no Builder retirement, no release movement, no source-pin adoption, no live-game activity.

---

## 1. Both findings were reproduced before they were fixed

I did not take either finding on description. Each was demonstrated against a scratch copy of `src`
first, and in both cases the review was right.

**F1's contract citation.** I checked `state/prompt_forge_next_phase0.md@f7c77a6a` and the clause is
there at line 303: *"explicit core API/snapshot golden so the UI boundary cannot silently widen"*,
restated at line 452. **I never opened the contract file.** I worked from the brief pasted into the
session, which does not contain that clause, and I did not go to the governing document to check
what else it required. That is my error, not an ambiguity — the acceptance requirement was written
down and I did not read it.

**F2.1, side-effect imports.** Injected `import "../ui/dom.mjs";` into `runner/` and `core/` on a
scratch tree:

```
import-direction: 39 modules, 62 cross-layer imports scanned
0 violations          <- bypass confirmed
```

**F2.2, qualified fetch.** Injected `globalThis.fetch("/api/trpc/jutsu.get")` into `runner/` and
`window.fetch(...)` into `core/`:

```
boundaries: 41 modules scanned
0 violations          <- bypass confirmed
```

**F2.3, the `main.mjs` allowlist.** Checked whether composition issues a request: it does not.
`main.mjs:215` binds `win.fetch` and hands it over as `fetchImpl`; every other mention is a comment
or a parameter. The allowlist entry widened the gate for no behaviour and is removed.

---

## 2. F1 — core boundary frozen

Corrections, all five points the review asked for:

1. **Explicit dependency contract.** `REQUIRED_DEPS` / `OPTIONAL_DEPS` replace
   `Object.assign(this, d)`. Unknown keys are ignored — a shell can no longer hand the core a view
   helper and have it kept. A missing required dependency throws in the constructor.
2. **`repoCache` is required, with no fallback.** `this.repoCache ?? this.cache` is gone. A consumer
   that omits it fails immediately rather than silently reversing the Phase 0 storage isolation by
   putting repository text back into the game capture cache.
3. **`snapshot()`** returns a deep-copied, JSON-serializable picture of machine state over a pinned
   key set. Mutating a snapshot cannot reach the core.
4. **`clearSelection()`** is a core action; `ManifestsScreen`'s Clear button no longer assigns
   `app.state.selected` itself.
5. **View-only state moved to the view.** `pickerQuery`, the picker's `renderPicker` callback and
   `navigator.storage.persist()`'s result now live on App-owned `app.view`. `app.state` is a
   read-through getter to core machine state, not an alias the view writes into.

**The golden — `forge/test/core.contract.test.mjs`** — is the artifact the contract asked for and
the thing that would have caught this. It pins the public action names and the machine-state key
set; proves a snapshot is JSON-serializable, is a copy, and holds no function, DOM node or
dependency handle; proves every required dependency fails closed, naming `repoCache` specifically;
proves unknown dependencies are not absorbed; and renders all five screens across all 12 scenarios,
then asserts that **no key and no function landed on core machine state**.

That last assertion fails on the pre-correction tree. Every other Phase 0 test passed on it, which
is the review's point: the widening was invisible to behaviour tests.

**No rendered byte changed.** All 12 screen fixtures are byte-identical across this correction,
including the five screen edits.

---

## 3. F2 — gate bypasses closed

- `check_imports.mjs` now scans side-effect imports (`import "x"`) alongside `... from "x"` and
  dynamic `import("x")`.
- `check_boundaries.mjs` now matches qualified calls — `globalThis.fetch(`, `window.fetch(`,
  `self/top/parent.fetch(` and any `.fetch(` — as well as the bare form. `fetchImpl(` and
  `.fetch.bind(` are still deliberately not matched: the first is the injected seam, the second is
  composition handing that seam over, and flagging either would make the gate unusable.
- `main.mjs` removed from the network allowlist.

**Red tests for both forms.** `imports.test.mjs` injects a side-effect import into `runner/` and
`core/`; `gates.test.mjs` injects `globalThis.fetch`, `window.fetch` and bare `fetch` into
`runner/`, `core/` and `storage/`. Both assert the gate exits nonzero naming each file. A fourth
test asserts the `fetchImpl` seam and `.fetch.bind()` handover are **not** flagged, so the widened
detector did not become a false-positive generator.

The real tree remains clean: 37 modules, 62 cross-layer imports, 0 violations either way.

### One self-inflicted error, recorded rather than buried

I committed `2c9a558b4f6c5280f32f86e57bc4cd3dac4fc0d4` with a **red suite**. The new red-test
fixture strings contained a literal `fetch(`, and a long-standing guard in `ui.test.mjs` greps every
test file for exactly that. The guard was right; my commit was wrong. Fixed in
`8e68eb061db7635b4c5bf165eaad0a0fc9ccbac4` by assembling the token so the guard stays strict and
unmodified, rather than carving an exemption into it. Both commits are on the branch; the red one
is not squashed away.

---

## 4. F3 — canonical workflow still staged, not installed

Unchanged and unchangeable from here. The PAT is refused on `.github/workflows/`:

```
refusing to allow a Personal Access Token to create or update workflow
.github/workflows/forge.yml without `workflow` scope
```

The reviewed gate set remains at **`state/staged_workflows/forge.yml`**;
`.github/workflows/forge.yml` on this branch is still byte-identical to `main` and still runs the
older sequence. I agree with the review that this is not a reason to widen the credential.

**Action required from dauntless:** install the staged file through the GitHub web UI, the path
`release_pin.yml`, `scrub.yml`, `skillpack.yml`, `relay.yml` and `regen_schemas.yml` already use.
If that install lands as a commit on this branch, the branch SHA moves and the new exact SHA should
go back for the narrow re-review. Until it runs, Phase 0 is not integration-ready.

All four new gates run under `npm test`, so the protection exists in the suite today; it is the CI
enforcement that is pending.

---

## 5. Measurements

| | Reviewed head `8be4c5b` | Corrected head | Δ |
|---|---|---|---|
| `npm test` | 332 / 332 pass | **340 / 340 pass / 0 fail / 0 cancelled / 0 skipped** | +8 |
| bundle raw | 413,323 B | **415,667 B** | +2,344 |
| bundle gzip | 77,998 B | **78,848 B** | +850 |
| import-direction | 0 violations, 37 modules | 0 violations, 37 modules | — |
| boundaries | 0 violations | 0 violations | — |
| screen fixtures | 12, byte-identical | 12, **byte-identical** | none |

```
npm ci                                      rc=0
npm test                                    340 / 340 pass / 0 fail
npm run fixtures + git diff --exit-code     clean (envelope and screens)
npm run build + git diff --exit-code        clean
node tools/check_imports.mjs                37 modules, 62 cross-layer imports, 0 violations
node tools/check_boundaries.mjs             37 modules, pin 345d18ac, 0 violations
node tools/check_bundle_budget.mjs          raw 415667/430000 (96.7%)  gzip 78848/81000 (97.3%)
```

The budget is now at 96.7% / 97.3%. It is still a ratchet and it is getting tight; a reviewed raise
belongs to Phase 1, which was always the intent.

---

## 6. Commits in this round

| SHA | |
|---|---|
| `2c9a558b4f6c5280f32f86e57bc4cd3dac4fc0d4` | `fix(gates): close the import and network gate bypasses (F2)` — **committed red, see §3** |
| `8e68eb061db7635b4c5bf165eaad0a0fc9ccbac4` | `fix(test): assemble the fetch token in gate fixtures` — makes the suite green again |
| `f4d69ef3d46ffb0b6ba3c163950d727d391b0224` | `fix(core): freeze the ForgeCore dependency/state boundary (F1)` |

New frozen head: this document's commit, plus the single stamp commit that follows it and changes
only the line below. **Review the branch tip of `fable/forge-next-phase0`.**

---

## 7. Unchanged from the original handoff

Game-source drift remains measured and unadopted; no pin moved. The 12 screen scenarios still do
not cover paused, orphan or rate-limited renders. Dev-only `uploadthing` advisories remain. And
**no real-browser verification was performed or possible** — no Firefox mobile, no ViolentMonkey,
no device. Carrier hydration, real CSSOM install, real IndexedDB persistence and the rollback path
remain browser evidence, not Node evidence, and that check is the operator's before any release.
