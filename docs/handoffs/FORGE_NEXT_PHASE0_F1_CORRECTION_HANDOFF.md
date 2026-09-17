# Forge Next Phase 0 — F1 residual correction handoff

**Status: CORRECTION APPLIED. FROZEN.** Narrow final review requested, scoped as the re-review
specified: the state-mutation correction, test/bundle fallout, exact branch head, and
installed-workflow evidence.

| | |
|---|---|
| Repository | `perseverance484/tnr-tools` |
| Implementation branch | `fable/forge-next-phase0` |
| Previous frozen head (reviewed) | `12a9d4db881b552c1aa93ae6fddd57f5d81772c9` |
| Re-review | `chatgpt/review-forge-next-phase0@a8c01ecce498820e41334f32e65c4cd250affeea` — CORRECTIONS_REQUIRED |
| Base / merge-base | `b42c2afd5ceb3cd2e1f1eaa6f1e082cfc419cbea` (unchanged; still a direct descendant) |
| New frozen head | stamped in §5 |
| Live game requests / writes | **none** |
| Credentials used | repository PAT for clone and push only. No game credential or session. |

Scope held to F1. No Phase 1, no Studio integration, no shell redesign, no Content Admin, no
Builder retirement, no release movement, no source-pin adoption, no live-game activity, and no
change to the F2 gates the re-review closed.

---

## 1. F1 — closed

The re-review was right, and the defect it named is the one my own handoff had described as already
fixed. I wrote that `app.state` was "a read-through getter" and that view-only writes had moved out
of the core. The first half was false at the frozen SHA — the getter returned the mutable object —
and `mount()` falsified the second half in the same file. The re-review quoting my own sentence back
against the code is fair.

All four corrections it asked for:

**1. `go()` accepts only a validated patch.** It was:

```js
go(screen, patch = {}) { Object.assign(this.state, patch, { screen }); this.changed(); }
```

`patch` was unconstrained, so `go("jobs", { pickerQuery: "x" })` minted a key on core machine state
through the public API. Neither guard could see it: `snapshot()` copies a fixed key set, and the
render test exercises only the calls that exist today. Now the screen is validated against
`SCREENS` and the patch against `GO_PATCH_KEYS` (`["jobId"]`), both exported and both requiring a
deliberate edit to widen. An unknown key throws and leaves state untouched.

**2. The view can no longer write machine state.** `App.state` returns a read-only `Proxy`;
`set`, `defineProperty` and `deleteProperty` throw. Reads and object identity are unchanged, so no
screen needed rewriting. Rendering still reads `app.state.*`; changing it requires a core action.

**3. `mount()` uses a core action.** `this.state.screen = "jobs"` → `this.core.go("jobs")`.

**4. Red tests**, in `core.contract.test.mjs`:
- `go()` refuses `{pickerQuery}`, `{persisted}`, `{renderPicker}` and `{jobId, extra}` — including
  the mixed case where a valid key carries an invalid one — and state is asserted unchanged after
  each refusal;
- `go()` refuses unknown screens (`"dashboard"`, `""`, `null`, `42`) and non-object patches;
- the view cannot write a known key, add a new key, delete a key or redefine a property, **including
  during mount**, while reads and the action path still work.

### What the fix caught immediately

The Proxy failed two tests on its first run — `screen_scenarios.mjs` was writing `app.state.jobId`
directly to set up three fixtures. That is my test harness, not production code, but it is the same
mutation the review objected to, and it had been invisible. Routed through `go("run", { jobId })`.
**The fixtures did not change**, which is the evidence the two forms were equivalent.

---

## 2. F2 — untouched

Closed by the re-review; nothing in this round modified `check_imports.mjs`,
`check_boundaries.mjs`, `imports.test.mjs` or the boundary tests in `gates.test.mjs`. Both gates
still report 0 violations over 37 modules and 62 cross-layer imports.

---

## 3. F3 — still the operator's step

Unchanged and unchangeable from here. `state/staged_workflows/forge.yml` holds the canonical gate
set; `.github/workflows/forge.yml` on this branch is still byte-identical to `main`. The PAT is
refused on `.github/workflows/`, and I agree it should not be widened.

**Required before integration:** install the staged file through the GitHub web UI, then run that
installed workflow green against this corrected tree. If the install lands as a commit on this
branch, the head moves and the new exact SHA goes back for the final narrow review.

All gates run under `npm test` today, so the protection exists in the suite; CI enforcement is what
is pending.

---

## 4. Measurements

| | Reviewed head `12a9d4d` | This head | Δ |
|---|---|---|---|
| `npm test` | 340 / 340 pass | **343 / 343 pass / 0 fail / 0 cancelled / 0 skipped** | +3 |
| screen fixtures | 12, byte-identical | 12, **byte-identical** | none |
| bundle raw | 415,667 B | **417,370 B** | +1,703 |
| bundle gzip | 78,848 B | **79,294 B** | +446 |
| import-direction | 0 violations, 37 modules | 0 violations, 37 modules | — |
| boundaries | 0 violations, pin `345d18ac` | 0 violations, pin `345d18ac` | — |

```
npm ci                                      rc=0
npm test                                    343 / 343 pass / 0 fail
npm run fixtures + git diff --exit-code     clean (envelope and screens)
npm run build + git diff --exit-code        clean
node tools/check_imports.mjs                37 modules, 62 cross-layer imports, 0 violations
node tools/check_boundaries.mjs             37 modules, pin 345d18ac, 0 violations
node tools/check_bundle_budget.mjs          raw 417370/430000 (97.1%)  gzip 79294/81000 (97.9%)
```

### One thing that needs a decision, not a fix

**The gzip budget is at 97.9%** — about 1,700 bytes of headroom. The next change of any size will
trip it. That is the ratchet working as designed, but it means the budget needs a deliberate raise
early in Phase 1 rather than an emergency one mid-change. I did not raise it here: doing so during a
narrow correction round would be exactly the silent widening this round exists to close.

---

## 5. Commit

| SHA | |
|---|---|
| `e8df70e0b146654b04f6cfcb5752561de03cc752` | `fix(core): close the go() patch seam and stop exposing mutable core state (F1)` |

New frozen head: this document's commit plus the single stamp commit after it, which changes only
the line below. **Review the branch tip of `fable/forge-next-phase0`.**

---

## 6. Unchanged from the previous handoffs

Game-source drift remains measured and unadopted; no pin moved. The 12 screen scenarios still do not
cover paused, orphan or rate-limited renders. Dev-only `uploadthing` advisories remain.

**No real-browser verification was performed or possible** — no Firefox mobile, no ViolentMonkey, no
device. Carrier hydration, real CSSOM install, real IndexedDB persistence and the rollback path
remain browser evidence, not Node evidence. The read-only state Proxy is new runtime behaviour in
the view layer and has only been exercised under jsdom; a Proxy trap that throws where the old code
silently assigned is worth one real-device pass before release.
