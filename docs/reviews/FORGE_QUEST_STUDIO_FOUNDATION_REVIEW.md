# Independent review — Forge Quest Studio foundation

**Status:** INDEPENDENT ENGINEERING REVIEW — RETURNED TO IMPLEMENTATION OWNER
**Lead:** Engineering Auditor (Claude Code / Fable acting as independent reviewer)
**Date:** 2026-09-13
**Repository:** `perseverance484/tnr-tools`

| | |
|---|---|
| Review target | `chatgpt/forge-quest-studio-foundation` |
| **Frozen target SHA** | **`cda8ac76100b2fa4b5429bea27c3c8c80353e240`** |
| Branch head observed at review start | `cda8ac76100b2fa4b5429bea27c3c8c80353e240` (unmoved; frozen as declared) |
| **Live `main` observed at review start** | **`6848a7805d912378f7f8eb27f52c9625dd10ac54`** |
| Merge-base `main` ↔ target | `305a28f992e33194fbba279a3f32e698dfb2b67f` |
| Baseline the handoff inspected | `main@305a28f…` (main has since advanced; no conflict found in reviewed files) |
| Implementation owner | ChatGPT |
| Governing contract | `state/prompt_forge_quest_studio_foundation.md` |
| Frozen handoff | `docs/handoffs/FORGE_QUEST_STUDIO_FOUNDATION_HANDOFF.md` |
| Live-game requests/writes performed | **none** |
| Branch modified by this review | **none** — the ChatGPT branch was read through a detached worktree only |

---

## Verdict

**The seam is sound. No confirmed blocker exists in the trust boundary, in `main` safety, in the
compile/live separation, or in the repository-as-compiler-authority model.** The central claims of
the handoff reproduce.

Fifteen findings follow. Two must be corrected before this branch is merged to `main` (F1, F3);
the rest are correction-loop work that does not change the architecture. Nothing here justifies
discarding or replacing the seam.

Recommendation: **enter the correction/integration loop.**

---

## Findings, most severe first

### F1 — Undisclosed, out-of-scope weakening of the loader origin-allowlist test — **Confirmed defect / scope discipline — MEDIUM**

**File:** `forge/test/release_loader.test.mjs` (commit `529dba5` "test: allow released loader with no pending marker")

**Invariant:** a Lane A slice keeps its changes inside its declared scope, and an existing safety
assertion is not relaxed without disclosure (`CLAUDE.md` §13, §11.7; contract §2/§3).

**Evidence.** `forge/test/release_loader.test.mjs` is not in the contract's in-scope list (§2), not
in the handoff's "important implementation files" (§4), and is not mentioned in the handoff's known
debt/deviations (§8). The single commit touching it carries a message describing only the
`@x-release-pending` relaxation. It in fact makes three further edits, one of which removes a real
guard:

```
-  const matches = (LOADER.match(/^\/\/ @match\s+(\S+)$/gm) || []).map((line) => line.split(/\s+/)[2]);
-  assert.deepEqual(matches, ["*://www.theninja-rpg.com/*", "*://theninja-rpg.com/*"]);
-  assert.ok(!matches.some((m) => m.includes("/forge")), "a /forge-only match cannot reach the carrier");
+  const matches = LOADER.match(/^\/\/ @match\s+\S+$/gm) || [];
+  assert.ok(matches.includes("// @match        *://www.theninja-rpg.com/*"));
+  assert.ok(matches.includes("// @match        *://theninja-rpg.com/*"));
```

I ran `main@305a28f`'s version of this test file against the **frozen tree**:

```
$ git show 305a28f:forge/test/release_loader.test.mjs > forge/test/zz_base_release_loader.test.mjs
$ node --test test/zz_base_release_loader.test.mjs
ok 1 … ok 9 except:
not ok 2 - release loader: exactly one @x-release-pending marker, naming the package version
# tests 9  # pass 8  # fail 1
```

Only assertion **2** failed. Assertions **6** (`@match` deepEqual), **8** and **9** all pass
unchanged against the frozen tree — so three of the four edits were **not required by anything on
this branch**. `forge_loader_user.js` is byte-identical to the merge-base on this branch
(`git diff --stat 305a28f HEAD -- forge_loader_user.js` → empty).

I also confirmed the one genuine failure is **pre-existing on `main`**: at `305a28f`,
`node --test test/release_loader.test.mjs` is already 8 pass / 1 fail, because `release_pin.yml`
correctly strips the pending marker after a merge and the assertion hard-codes `=== 1`.

**Practical consequence.** `@match` is the origin allowlist of a userscript that injects
`forge_bundle.js` at `document-start` into a signed-in game session. The old assertion pinned the
*exact* set and explicitly forbade a path-scoped match; the replacement only asserts those two lines
are *present*, so an added `// @match *://*/*` (or any third origin) now ships green. The pending-marker
relaxation from `=== 1` to `<= 1` is defensible but silently also permits zero markers on a branch
that *has* bumped the package version, which is the case the `docs/00_INDEX.md` deploy note exists for.
Separately, the handoff's "Forge Node suite: 308 tests, 308 passed, 0 failed" is true but is partly
bought by relaxing an assertion inherited from `main`, and that is not disclosed.

**Smallest robust correction.**
1. Restore the exact-allowlist `@match` assertion and the "no `/forge`-only match" assertion verbatim.
2. Restore assertions 8 and 9 verbatim (they pass unchanged).
3. Keep only the pending-marker change, and make it express the real contract rather than `<= 1` —
   e.g. `markers.length === (LOADER_VERSION === PKG_VERSION ? 0 : 1)`.
4. Disclose the edit in the handoff as an inherited-`main` test defect fixed in passing, or split it
   to a separate one-commit branch so this slice stays in scope.

---

### F2 — The `S` Mission profile (`AWAITING_RULING`) is presented as a selectable "no combat" profile, and the draft is declared ready to compile — **Confirmed defect — MEDIUM**

**Files:** `forge/src/studio/ui.mjs:139-143` (`profileLabel`), `:126-137` (`missionDraftProblems`), `:330-334`, `:348-350`
**Data:** `skills/building-tnr-content/data/48_DATA_mission_profiles.json` → `ranks.S.shape.* == "AWAITING_RULING"`

**Invariant:** repository-backed facts stay repository-owned, and an unresolved director decision is
never rendered as a settled fact (task focus 11; `FORGE_NEXT_QUEST_STUDIO.md` §15.7;
`CLAUDE.md` §10).

**Reproduction.** Driving the real `48_DATA_mission_profiles.json` (not the test stub) through the
shipped `QuestStudioWorkspace` under jsdom:

```
--- profile options rendered from the real repository profile file ---
  value="D"          disabled=false text=D · 4 nodes · no combat
  value="D_story"    disabled=false text=D_story · 6 nodes · no combat
  value="D_combat"   disabled=true  text=D_combat · 4 nodes · 1 battle · Encounter editor required
  value="C"          disabled=true  text=C · 4 nodes · 1 battle · Encounter editor required
  value="B"          disabled=true  text=B · 23 nodes · 3 battles · Encounter editor required
  value="A"          disabled=true  text=A · 46 nodes · 6 battles · Encounter editor required
  value="S"          disabled=false text=S · ? nodes · no combat

missionDraftProblems for S-rank draft -> []
Compile button disabled? -> false | label: Compile in repository
Readiness banner -> qs-callout ok | "Ready for repository compile…"
Profile fact callouts -> ["NaN objectivesOwned by the selected Mission profile.",
                          "NaN battle nodesCombat profiles unlock after the Encounter editor lands."]
```

**Cause.** Every guard coerces the sentinel string and fails open:

- `Number(profile?.shape?.battle_nodes || 0) > 0` → `Number("AWAITING_RULING")` is `NaN`, `NaN > 0` is `false` → option not disabled.
- `if (profile?.shape?.battle_nodes > 0)` → `"AWAITING_RULING" > 0` is `false` → no blocking problem raised.
- `Number.isInteger(Number("AWAITING_RULING"))` is `false` → the objective-count check is skipped entirely.
- `battles ? … : " · no combat"` → `NaN` is falsy → the label positively asserts "no combat".
- The two "Repository policy" callouts interpolate `Number(...)` directly and print the literal string `NaN`.

**Why the existing test does not catch it.** `forge/test/quest.studio.ui.test.mjs` stubs profiles as
`{ D: {objective_count:4, battle_nodes:0}, D_combat: {objective_count:4, battle_nodes:1} }` — clean
integers only. The "combat profiles are not silently downgraded" coverage is real but is tested
against a fixture that does not represent the repository file it claims to read.

**Backstop that does hold.** The canonical compiler is correct. I compiled a hand-built S-rank Quest
Source at the frozen SHA:

```
status: blocked   requestId: quest-advs01
blockers: [{"code":"decision_required",
  "message":"profile incomplete for rank S; these are rulings, not defaults:\n  S.quest.requiredLevel\n  S.shape.objective_count\n  S.shape.battle_nodes\n …"}]
```

So nothing wrong is generated. The defect is confined to the pre-compile surface — but that surface
is exactly where the slice claims "repository-owned facts and compilers".

**Practical consequence.** An operator can select S, be told the profile has no combat, be told the
draft is "Ready for repository compile", see `NaN` printed as a repository fact, compile, and only
then learn the entire rank is unratified. It is the "Forge invented a repository fact" failure mode
the architecture exists to prevent.

**Smallest robust correction.** Add one sentinel-aware reader used by all four sites, e.g.

```js
const RULING = "AWAITING_RULING";
function shapeNumber(profile, key) {
  const raw = profile?.shape?.[key];
  return typeof raw === "number" && Number.isFinite(raw) ? raw : null;  // null === unresolved
}
```

Then: an unresolved `battle_nodes` disables the option and adds a blocking problem
("rank S is awaiting a director ruling"); an unresolved value renders as "awaiting ruling", never as
`NaN`, `?` or "no combat". Add a regression test that loads the **real**
`48_DATA_mission_profiles.json` rather than a synthetic stub.

---

### F3 — The in-product PAT instruction is now wrong; Compile will 403 for any operator who follows it — **Contract/source mismatch — MEDIUM**

**Files:** `forge/src/ui/screens.mjs:305`; `forge/src/github.mjs:131-148` (`dispatch`); `forge/src/studio/repository.mjs:105-118`

**Invariant:** the operator-facing setup instruction matches the permissions the code actually needs.

**Evidence.** The Settings field still reads:

```js
const pat = h("input", { type: "password", placeholder: "fine-grained PAT (contents: write on tnr-tools only)", … });
```

`QuestStudioRepository.dispatch()` calls `POST /repos/{owner}/{repo}/actions/workflows/quest_studio.yml/dispatches`,
which requires the fine-grained **Actions: write** repository permission. `ensureBranch` and `put`
need only Contents: write, so the failure is ordered badly:

1. `ensureBranch` → 201, `studio/quest/<id>` created;
2. `put` → 201, Quest Source committed;
3. `dispatch` → **403**, `buildState = { error: "dispatch quest_studio.yml: HTTP 403 …" }`.

The operator is left with a real branch and a real committed source revision and no build, and the
UI never names the missing scope. "Refresh build status" cannot recover it (it only re-reads the
result path); re-pressing Compile writes another commit and 403s again.

**Practical consequence.** First-run failure is guaranteed for an operator who created their PAT as
the product told them to, with a diagnostic that does not point at the cause. This also silently
widens the browser-held credential from Contents-only to Contents + Actions (see F9).

**Smallest robust correction.** Update the placeholder and any setup note to
`fine-grained PAT (contents: write + actions: write on tnr-tools only)`, and map a 403 from
`dispatch` to a specific message naming Actions: write. Record the scope change in the handoff.
(A structurally better option is in F9.)

---

### F4 — A whole class of source errors produces a build result Forge cannot read, and wedges the draft — **Confirmed defect — MEDIUM**

**Files:** `skills/building-tnr-content/scripts/quest_compile.py:383-407` (fallback envelope),
`:242` (`registry_entry` called outside the `try`); `forge/src/studio/repository.mjs:45`

**Invariant:** `failed` is a readable result envelope, not an unreadable one (contract §5; handoff §5).

**Reproduction** (frozen SHA, unknown subtype — a value `validateQuestSource` on the Forge side does
*not* reject, because it only checks that `subtype` is a non-empty string):

```
$ python3 skills/building-tnr-content/scripts/quest_compile.py adv/unknown_subtype.quest.json \
    --result adv/unknown.build.json --artifact-dir adv/build1 \
    --artifact-prefix studio/builds/quest-adv001 --source-revision 000… --compiler-revision 111…
{"status": "failed", "requestId": null, …}
```

```json
{ "status": "failed", "requestId": null, "subtype": null,
  "errors": [{ "code": "source_invalid", "message": "unknown Quest Studio subtype 'guide'" }] }
```

Feeding that exact file to the shipped Forge validator:

```
A) failed-envelope readable by Forge? NO -> Quest Studio result belongs to null, expected "quest-adv001"
```

`validateBuildResult` hard-requires `result.requestId === id` (correctly — it is the identity check
that stops a wrong build being shown as current). But `quest_compile.main()` deliberately drops
`requestId` on *any* source-validation error, including recoverable authoring errors. The same path
is taken for a bad `schemaVersion`, a non-object `content`, a non-object `meta`/`project`, and an
unknown subtype.

**Practical consequence.** `buildResult()` rethrows (it only swallows 404), so `compileMission`
renders `Repository request failed: Quest Studio result belongs to null…` instead of
`unknown Quest Studio subtype 'guide'`. Worse, the unreadable result is now committed at
`studio/results/<id>.build.json`, so every later `refreshBuild()` on that draft throws the same
identity error forever. The only escape is "New Mission" (a fresh `requestId`); the authored draft
is effectively stranded.

**Smallest robust correction.** The compiler already has the identity: pass
`--request-id "$REQUEST_ID"` from the workflow (it is the *validated* input, so it cannot be
poisoned by source content) and use it for `requestId` in the fallback envelope. Alternatively,
recover `raw.get("requestId")` when it matches `REQUEST_ID_RE`. Either way, add a Forge-side test
that a `status:"failed"` envelope round-trips through `validateBuildResult`.

**Related (fold into the same fix):** `validate_source` never checks that the source's declared
`requestId` equals the request id the worker validated from the branch/path. The identity binding
currently lives only in the workflow. Passing `--request-id` and asserting equality in
`validate_source` closes both halves at once.

---

### F5 — Mission profile *shape* is enforced only in the browser; the canonical compiler returns `valid` for a combat rank with no combat — **Contract/source mismatch — MEDIUM**

**Files:** `skills/building-tnr-content/scripts/quest_compile.py:152-200` (`compile_mission`);
`skills/building-tnr-content/scripts/mission.py:156-180` (`check_headcount`), `:284-311` (`build`)

**Invariant:** "Browser-side checks are advisory/editing aids. Canonical compile/validation runs in
repository tooling" and "Mission policy remains owned by `48_DATA_mission_profiles.json` +
`mission.py`" (contract §4).

**Reproduction** (frozen SHA; a Quest Source in exactly the shape `missionSourceFromDraft` emits —
dialog beats plus `win_quest`, no `start_battle` — at ranks whose profile declares battle nodes):

```
=== rank C (profile: objective_count 4, battle_nodes 1) ===
 status: valid   blockers: []   errors: []
 generated: {"entities":{"counts":{"quest":1},"creates":1},"enemies":[]}

=== rank B (profile: objective_count 23, battle_nodes 3) ===
 status: valid   blockers: []   errors: []
 generated: {"entities":{"counts":{"quest":1},"creates":1},"enemies":[]}
```

A rank-B Mission with 4 objectives instead of 23 and 0 battles instead of 3 passes canonical
compilation and `validate.py` as `valid`, and the generated manifest is a legal, pushable
`quest` create (`hidden: true` is correctly preserved — verified).

**Refutation attempted.** `mission.py` does enforce the `max_enemies_per_battle` **ceiling** and the
`AWAITING_RULING` refusal, so this is not an absent-guard bug in `mission.py` — it is a deliberate
pre-existing choice ("the profile stops being the value and becomes the CEILING",
`mission.py:156-166`). `mission.py` and `48_DATA_mission_profiles.json` are byte-identical to the
merge-base on this branch, so **this slice introduces no regression in `mission.py`**.

What the slice does change is who the sheet author is. Historically the sheet came from an agent
working from `references/quest.md`; now it comes from a generated browser draft whose only shape
gate is `missionDraftProblems`. Through the shipped UI the path is closed (combat ranks are
disabled, F2's S-rank hole aside). It is reachable today by committing a
`studio/requests/<id>.quest.json` directly to a Studio branch and dispatching, and it becomes
reachable through the UI the moment the Encounter editor lands.

**Practical consequence.** Exactly the failure `mission.py`'s own docstring names: "the record
pushes cleanly and is simply wrong, and nothing catches it." A combat-rank Mission ships as a
dialog walk. Recoverable (nothing is live until the operator taps ▶) but it is content corruption
with a green light on it.

**Smallest robust correction.** Do **not** change `mission.py`'s general ceiling policy. Add a
Quest-Studio-adapter conformance check in `compile_mission` only: after `mission.build`, count
`start_battle`/`defeat_opponents` objectives and total objectives in the produced record and compare
against the resolved profile's `battle_nodes` / `objective_count` when those are ratified numbers.
On disagreement return a structured `blocked` with a new code (e.g. `profile_shape_unmet`) naming
both numbers. This keeps the canonical authority in Python, leaves the browser check advisory as the
contract requires, and needs no change to mission policy.

*(The `blocked` vs `failed` classification for this new code is ChatGPT's call; both readings are
defensible and neither is a director decision.)*

---

### F6 — Worker boundary-gate and dispatch failures are invisible; the UI reports "Build still running" indefinitely — **Needs refinement — MEDIUM-LOW**

**Files:** `.github/workflows/quest_studio.yml` (validate step, `exit 2` / `exit 3`);
`forge/src/studio/ui.mjs:410-427` (`pollBuild`), `:387-400`; `forge/src/github.mjs:131-148`

**Invariant:** `FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md` §11 requires Forge to distinguish
`Building`, `Build result received`, `Repository unavailable / retry save`, `Build failed` and
`Build blocked by design decision`.

**Evidence.** When the boundary gate rejects a request (`exit 2` on an id/branch/path/symlink
mismatch, or `exit 3` when the request branch advanced between the Forge `put` and the worker's
`actions/checkout` of the branch **tip**), the workflow exits *before* the compile step, so **no
result file is ever written**. Forge's only signal is the absence of a result: `pollBuild` runs
`maxPolls × pollMs` = 30 × 2000 ms = 60 s and then renders

> **Build still running** — "No current result has landed yet. Refresh status without resubmitting the source."

which is false and never becomes true. `Github.dispatch` returns `{ ok: true }` on HTTP 204 and
discards the response, so Forge holds no run id and never reads run status.

`state.error` also conflates three of §11's states — transport failure, dispatch rejection, and an
unreadable result (F4) all render as "Repository request failed".

**Practical consequence.** The operator cannot distinguish "worker still running", "worker rejected
the request at the gate", and "workflow never started". The exit-3 race is real: any second write to
the branch between `put` and checkout produces it.

**Smallest robust correction.** Two independent halves; either alone is a large improvement:
1. Make the worker fail *loudly into the result path*: on a boundary rejection, write a
   `status:"failed"` envelope carrying the validated `request_id` to
   `studio/results/<id>.build.json` and push it before exiting non-zero. Then Forge already
   surfaces it.
2. Have `dispatch` capture the workflow run (poll `GET /actions/workflows/{file}/runs?branch=main`
   filtered by the dispatch time, or switch to `repository_dispatch` — see F9) so "Build still
   running" can be distinguished from "the run finished red".
Also pin the request checkout with `ref: ${{ inputs.source_sha }}` so the exit-3 race disappears
(the `rev-parse` equality check then becomes a cheap assertion rather than the primary gate).

---

### F7 — "Inspect generated manifest" renders behind the full-screen Studio overlay and appears to do nothing — **Confirmed defect — MEDIUM-LOW**

**Files:** `forge/src/studio/ui.mjs:472-482` (`inspectManifest`), `:14` (`.qs-shell` CSS),
`:192-195` (`open()` appends the shell to `app.root`); `forge/src/ui/app.mjs:177-183` (`showExport`)

**Invariant:** the one affordance for inspecting compiled output is actually reachable
(`FORGE_NEXT_QUEST_STUDIO.md` §15.8).

**Evidence.** `open()` does `this.app.root.appendChild(this.shell)` where
`.qs-shell { position:fixed; inset:0; z-index:2147483002; overflow:auto; background:#070b12; }` —
an opaque, viewport-filling, last-child overlay. `showExport` does `this.$main.prepend(card)`, and
`$main` (`main.f-main`, `app.mjs:69`) sits *inside* `app.root`, underneath the overlay.
`inspectManifest` never hides the shell and never re-parents the card. There is no shadow root in
the path (`mountHost` appends a plain `div` to `document.body`), so the CSS applies as written.

The existing test cannot catch this: `fakeApp.showExport` records to `root.dataset`, proving the
call happens, not that it is visible.

**Practical consequence.** Pressing "Inspect generated manifest" produces no visible change and no
error. The generated manifest — the only artefact the operator can review before any future
promotion step — is unreachable from the Studio. Separately, §15.8 asks that a valid output "can be
opened directly in existing Forge preflight"; `showExport` is a read-only textarea, not preflight,
so that criterion is unmet even once the overlay issue is fixed. (The handoff's debt #6 covers
promotion into the *runner*, which is a broader and correctly-withheld thing; preflight is not the
same ask.)

**Smallest robust correction.** Render the manifest inside the Studio shell (a `qs-card` with a
read-only `textarea` and a Copy button, reusing the existing pattern), or `this.close()` before
calling `showExport`. Then state explicitly in the handoff whether §15.8's "open in Forge preflight"
is deferred, and why.

---

### F8 — Generated-artifact confinement is bypassed by percent-encoded traversal and by `?` query injection — **Confirmed defect — LOW**

**Files:** `forge/src/studio/repository.mjs:51-63` (`generatedArtifactPath`);
`forge/src/github.mjs:39-41` (`_url` interpolates `path` unencoded)

**Invariant:** handoff §7.2 — "The adapter now rejects traversal (`.` / `..`), empty segments and
backslashes before reading generated artifacts."

**Reproduction** (frozen modules, `github.text` stubbed to record reads):

```
  rejected: studio/builds/quest-adv001/../../../push/46.json
  rejected: studio/builds/quest-adv001/./x.json
  rejected: studio/builds/quest-adv001//x.json
  ACCEPTED: studio/builds/quest-adv001/..%2f..%2fpush%2f46.json
  ACCEPTED: studio/builds/quest-adv001/%2e%2e/%2e%2e/push/46.json
  ACCEPTED: studio/builds/quest-adv001/a?ref=main&x=.json
```

`_url()` interpolates `path` verbatim, so the accepted third case builds:

```
https://api.github.com/repos/perseverance484/tnr-tools/contents/studio/builds/quest-adv001/a?ref=main&x=.json?ref=studio%2Fquest%2Fquest-adv001
```

— the result-supplied `ref=main` is now the first `ref` parameter, ahead of the adapter's intended
branch scoping. The percent-encoded forms survive the segment check (`%2e%2e` is not the string
`..`) and reach GitHub's API without client-side encoding.

**Refutation / scope.** This is genuinely low severity. `generated.manifestPath` originates from
`--artifact-prefix "studio/builds/$REQUEST_ID"`, which the workflow derives from the **validated**
`request_id`, so an honest build never produces one of these. Reaching it requires already having
write access to the Studio branch to tamper with the result file, and the payoff is reading a file
the PAT can already read. It is a defence-in-depth gap in a stated invariant, not an escalation.
Whether GitHub's contents API actually resolves `%2e%2e` to a traversal is **unverified** (settling
it would need a live GitHub request I did not make); the `?ref=` branch override needs no server
behaviour to be a real loss of the invariant.

**Smallest robust correction.** Two lines. In `generatedArtifactPath`, reject any tail containing
`%`, `?` or `#` (a repository build path never needs them). Independently, encode path segments in
`Github._url` / `Github.put`: `path.split("/").map(encodeURIComponent).join("/")`. Extend
`github.studio.test.mjs`'s traversal loop with the three accepted strings above.

---

### F9 — `Github.dispatch` is a general workflow-trigger primitive, not an allowlisted one — **Needs refinement / architecture recommendation — LOW-MEDIUM**

**File:** `forge/src/github.mjs:131-148`

**Invariant:** `RUL-2026-09-12-002` — "Repository/build operations must be approved typed operations
rather than arbitrary remote command execution"; `FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md` §12
— do not give the browser an arbitrary remote primitive.

**Evidence.** `dispatch()` accepts any workflow filename matching `^[A-Za-z0-9._-]+$`, any `ref`
passing `assertBranch`, and any `inputs` object. Only the call site
(`QuestStudioRepository.dispatch`, which hard-codes `QUEST_STUDIO.workflow`) narrows it. The
repository contains `relay.yml`, a `workflow_dispatch` workflow that merges a `relay/*` branch into
`main` with `contents: write`.

**Refutation / severity.** I checked: `main` is **not** branch-protected
(`list_branches` → `{"name":"main", …, "protected":false}`), so a PAT with `contents: write` can
already write `main` directly and can already trigger the push-triggered workflows. Adding
Actions: write therefore does **not** create a new worst case on this repository today; it widens the
reachable set (`workflow_dispatch`-only workflows such as `relay.yml`, `answers.yml`,
`regen_schemas.yml`) and it removes a would-be protection if `main` is ever protected later. It is a
scope observation, not an exploit.

Note also that `docs/design/FORGE_NEXT_QUEST_STUDIO.md` §16 lists "GitHub authentication/least-privilege
model" and "build-trigger choice (push vs dispatch)" as explicitly open engineering decisions, so the
final shape is not this slice's to settle.

**Smallest robust correction (current defect half).** One constant:

```js
const DISPATCHABLE = new Set(["quest_studio.yml"]);
…
if (!DISPATCHABLE.has(workflow)) throw new GithubError(`workflow ${JSON.stringify(workflow)} is not dispatchable from Forge`);
```

**Architecture recommendation (for the integration contract, not this slice).** Consider
`POST /repos/{owner}/{repo}/dispatches` (`repository_dispatch`) instead of
`workflow_dispatch`. It needs only **Contents: write** (removing F3's scope expansion entirely), and
it *always* runs the workflow file from the default branch — which turns the
`TRUSTED_REF == refs/heads/main` guard from an advisory check into a structural guarantee (see F10).

---

### F10 — Trust-boundary ordering, and the contract test pins substrings rather than order — **Needs refinement — LOW**

**Files:** `.github/workflows/quest_studio.yml` (step order);
`skills/building-tnr-content/scripts/quest_worker_contract_test.py`

**a) Ordering.** "Checkout authored request branch" runs **before** "Validate request boundary", so
an unvalidated `inputs.request_branch` is passed to `actions/checkout` as a ref. I tried to make this
matter and could not: `actions/checkout` does not execute repository content (hooks are not fetched;
a tracked `.gitattributes` cannot define a filter command without config), and the validation gate
does run before `python3 tools/…/quest_compile.py`, so even a request branch carrying an *unmodified*
copy of the workflow exits 2 before any compile. **Not exploitable at this SHA.** Still worth
reordering: validation costs nothing and defence-in-depth should not depend on an argument about
what `checkout` does.

**b) The guard that protects the guard.** `quest_worker_contract_test.py` is 21 `require`/`forbid`
substring checks. It verifies each token exists *somewhere in the file*; it verifies **no ordering**.
A refactor that moved "Validate request boundary" after "Compile Quest Source" would pass all 21
checks. Given that this test is the stated proof of the trust boundary, that is a real gap.

**c) Fragile run-body extraction.** The `${{ inputs.` forbid only inspects lines collected after a
literal `run: |` and terminated by a line starting with exactly `      - name:` / `      - uses:`. A
step written `run: >-`, or re-indented, silently contributes nothing, making that check vacuously
pass. It is currently correct only because every step happens to match the assumed layout.

**d) Residual structural limitation (expected behaviour, worth stating).** The
`TRUSTED_REF == refs/heads/main` check can only exist in the copy of the workflow that is running.
Dispatching `quest_studio.yml` on a request branch runs *that branch's* copy, so the guard is
bypassable by anyone who can push a modified workflow file — i.e. anyone with `contents: write`,
which is already full compromise on this repository. This is the standard GitHub Actions trust model
and is correctly implemented; the only way to make it structural is F9's `repository_dispatch`
recommendation. **Not a defect; documenting it so it is not mistaken for a stronger guarantee than it is.**

**Smallest robust correction.** Move the "Validate request boundary" step above the request checkout
(keeping the `rev-parse` assertion after it). Parse the workflow as YAML in the contract test and
assert step *order* and `permissions`, rather than substring presence.

---

### F11 — `h()` can still write to an HTML sink, contradicting the file's own stated repo law — **Needs refinement / hardening — LOW (not exploitable at this SHA)**

**File:** `forge/src/ui/dom.mjs:1`, `:15`

```js
// DOM helpers. createElement and CSSOM only; no innerHTML anywhere (repo law).
…
else if (k in el && typeof v !== "string") el[k] = v;
```

The generic property branch will assign to `innerHTML`, `outerHTML` or `srcdoc` if a key with that
name reaches it. The `typeof v !== "string"` condition does not close it: any object with a
`toString` is coerced by the sink.

**Refutation attempted — and it holds.** I searched every `h()` call site in `forge/src` for computed
or spread attribute keys. There are none; every attrs object uses literal keys, and no site builds
attrs from data. `grep -rn "innerHTML\|outerHTML\|srcdoc\|insertAdjacent" forge/src` returns only the
comment on line 1. **This is a latent hazard, not a live defect**, and I am reporting it as such
rather than as the exploitable finding the planning lens anticipated. The Studio's new
`value`-as-property branch (line 14) is a correct fix for the textarea bug and introduces nothing.

**Practical consequence.** None today. The risk is that Quest Studio is the first Forge surface that
renders repository-supplied strings at volume, and the natural next step (attrs derived from a
registry entry or a build result) turns the latent sink live.

**Smallest robust correction.** One denylist before the generic branch:

```js
const HTML_SINKS = new Set(["innerHTML", "outerHTML", "srcdoc", "insertAdjacentHTML"]);
…
else if (HTML_SINKS.has(k)) throw new Error(`h(): ${k} is not assignable (repo law: no innerHTML)`);
```

That makes the header comment enforceable instead of aspirational.

---

### F12 — No lifecycle or retention contract for Studio branches and build artefacts — **User decision required / planning item — LOW**

Every compile permanently creates `studio/quest/<requestId>` off `main` and leaves
`studio/requests/`, `studio/results/` and `studio/builds/` on it. Nothing deletes or ages them, and
`requestId` is `quest-<base36 ms>`, so the count grows monotonically with compile presses. The
repository already carries ~60 branches.

`FORGE_NEXT_QUEST_STUDIO.md` §16 lists "project-branch/source lifecycle and cleanup" as an open
engineering decision, so this is correctly *not* settled by this slice. Flagging it so it enters the
integration contract rather than being discovered as branch sprawl. Retention policy (and whether
build artefacts are ever promoted to `push/`) is dauntless's call.

*Positive side note:* `scrub.yml` triggers on every push, so authored Studio prose does pass the
privacy gate on each build commit. That is a good property and appears to be incidental — worth
making deliberate.

---

### F13 — Single global draft slot; multi-tab last-write-wins; `lastResult` written but never read — **Operator inconvenience — LOW**

`DRAFT_KEY = "tnr_forge_quest_studio_draft_v1"` holds exactly one draft. Two tabs with the Studio
open silently overwrite each other (`writeDraft` on every keystroke, no lease or version check),
which is the same cross-tab ownership class the repo's own review workflow calls out. `startNewMission`
does confirm before replacing, so single-tab loss is guarded.

`compileMission`/`pollBuild` persist `draft.lastResult`, but nothing ever reads it back —
`openMission` re-fetches from the repository instead. Dead state that will read as a cache to the
next maintainer. Either use it as the offline/"last known result" surface §11 of the architecture doc
asks for, or drop it.

---

### F14 — `docs/RULINGS.md` no longer ends with a newline — **Trivial**

The two new ruling entries end the file without a trailing newline (`\ No newline at end of file`).
The ledger is append-oriented; the next append will concatenate onto the last line. One byte.

---

### F15 — Dependency debt is real but not this feature's — **Expected behaviour / do not block**

`npm ci` in `forge/` reports 3 high-severity advisories, and all three are one chain:

```
uploadthing (devDependency, direct) → @uploadthing/shared → effect
  "Effect AsyncLocalStorage context lost/contaminated inside Effect fibers under concurrent load with RPC"
```

`effect` is a **devDependency**, it is not bundled (`forge/src` never imports the npm package;
the six `uploadthing` matches in `forge_bundle.js` are Forge's own hand-written protocol code in
`forge/src/transport/upload.mjs`, derived from the game's pinned 7.7.4 wire format), and the advisory
describes a server-side Effect-runtime concurrency bug with no reachable path from Quest Studio.

This matches handoff debt #1 and should be tracked as a separate dependency audit. **It is not a
reason to hold this slice.**

---

## Verified claims that held

Each of these was reproduced against `cda8ac76…`, not accepted from the handoff.

| Claim | Evidence |
|---|---|
| `quest_worker_contract_test.py` passes | 6/6 PASS, rc 0 |
| `quest_compile.py --selftest` = 9 passed, 0 failed | reproduced exactly |
| Mission adapter integration test passes | 2/2 PASS, rc 0 |
| Forge Node suite = 308/308 | reproduced exactly (see F1 on how one assertion got there) |
| Fixture regeneration is clean | `npm run fixtures` → `git diff --exit-code -- test/fixtures/envelope` clean |
| Checked `forge_bundle.js` is reproducible from the canonical build | `npm run build` → sha256 **identical** before/after: `c9c80b663032a6f532ecc160fb871b9e8d67a157faf8af390e14476ae24dc789` (427.2 KB, matching the handoff) |
| `dist/building-tnr-content.zip` is reproducible | `pack_skills.py` re-run → sha256 identical (`e10f64f12a2a…`), `git status` clean |
| Skill coherence gates green | `doctrinemap.py` 0 err/0 warn · `render_doctrine.py --check` exit 0 · `build_packs.py --check` exit 0 · `catalog_sync.py --selftest` OK |
| `lawmap.py` not regressed | target: 93 laws / 93 rows / 77 citations / 0 errors / 5 warnings — identical to base `305a28f` |
| No normal Studio path writes `main` | `submit()` always passes `{branch}`; `put` default is untouched; worker pushes only `HEAD:$REQUEST_BRANCH` after asserting `== studio/quest/$REQUEST_ID`; legacy-default test reproduced |
| No other workflow is triggered onto `main` by a Studio push | `answers.yml` (`harvests/**`), `skillpack.yml` (`skills/**`), `release_pin.yml` (`branches:[main]`), `quest_studio_ci.yml` (path filter) — none match `studio/**`; only `scrub.yml` (read-only gate) fires |
| Untrusted inputs never reach shell syntax | every `run:` body reads inputs through `env:`; `concurrency.group` is the only direct interpolation and is not a shell context |
| Trusted compiler is separated from authored content | compiler checked out at `github.sha` under `tools/`, request under `request/`; only `python3 tools/…/quest_compile.py` executes |
| Untrusted request-branch code cannot execute | validation gate (incl. `TRUSTED_REF == refs/heads/main`) runs before the compile step; no `python3 request/`, `bash request/`, `sh request/`; no untrusted import path (`ensure_import_paths` adds only `CONTENT_SCRIPTS`/`ART_SCRIPTS` under the trusted root) |
| Generated output is confined to `studio/results/<id>.build.json` + `studio/builds/<id>/` | artefacts are produced into `$RUNNER_TEMP` and copied in with `cp -a "$TMP/build/."`, so a traversal-named artefact cannot land in the repo; `git add` is path-allowlisted |
| Symlinked Studio paths are refused | `-L` checks on `studio`, `studio/requests`, `studio/results`, `studio/builds` and on the source file itself; `rm -rf` precedes the result/build writes |
| Compile is structurally separated from the live game | `forge/src/studio/*` imports only `ui/dom.mjs`, `github.mjs`, `repository.mjs` — zero references to Session, Runner, transport or the game origin; `main.mjs` change is purely additive (a launcher button) |
| `liveGameTouched:false` is enforced on read | `validateBuildResult` rejects any other value — verified by test and by inspection |
| Stale results are not presented as current | `provenance.sourceRevision` is the worker-verified `source_sha`; Forge compares it to the `commitSha` returned by its own `put`; `pollBuild` refuses to accept a stale result at all |
| `AWAITING_RULING` returns a structured blocker, never a guessed value | S-rank compile → `status:"blocked"`, `code:"decision_required"`, all six unresolved fields named |
| `blocked` is not over-applied | `classify_mission_error`'s three markers all exist verbatim in `mission.py` (`:192`, `:131-132`); an ordinary error stays `failed` (selftest + inspection) |
| `hidden: true` survives the Studio path | generated manifest → `hidden: True`, `questType: mission`, `slot: create` |
| Browser JS does not own Mission policy | profiles, objective counts and battle counts are all read from `48_DATA_mission_profiles.json` at runtime; `missionSourceFromDraft` authors a design sheet, it does not decide policy (F2 is a coercion bug in *reading* that data, not a second copy of it) |
| Unsupported subtypes stay visibly unavailable | registry `maturity != "supported"` → card disabled, "Adapter pending"; compiler returns `blocked`/`subtype_not_executable` |
| Handoff debt #7 (`mission.py --selftest` stale) is accurate | reproduced: raises `MissionError: objective 'n2': 2 enemies in one fight, but rank D caps a battle at 1`; **identical at base `305a28f`** and `mission.py`/profiles are unchanged on this branch — pre-existing on `main`, correctly not papered over |
| The temporary write-enabled bundle-sync workflow is gone | `.github/workflows/` at the target contains no such file; `quest_studio_ci.yml` is `contents: read` |
| The branch is frozen | branch head still `cda8ac76…` at review end |

---

## Unverified — browser / live / session

Stated so they are not mistaken for verified safety. Zero live-game requests and zero live-game
writes were performed, per the task.

- Real browser smoke on Android/Firefox + ViolentMonkey: **not performed.** All UI findings (F2, F7)
  come from jsdom execution of the shipped modules plus CSS inspection; F7's overlay conclusion is
  inspection-based and has not been seen rendered.
- A real `workflow_dispatch` from the Forge UI with a real PAT: **not performed.** F3's 403 is derived
  from GitHub's documented fine-grained permission for the workflow-dispatch endpoint, not observed.
- Whether GitHub's contents API resolves `%2e%2e` in a path to a traversal: **not tested** (F8). The
  `?ref=` override half of F8 needs no server behaviour.
- Actual execution of `.github/workflows/quest_studio.yml`: **not performed.** The worker was reviewed
  statically and through `quest_worker_contract_test.py`; the handoff's cited run
  (`34723093835` / job `103632390318`) was not re-run.
- Any live-game request, read, write, capture or publication: **none, as required.**

---

## Tests and gates run (all against `cda8ac76…` in a detached read-only worktree)

```
python3 skills/building-tnr-content/scripts/quest_worker_contract_test.py      → 6 PASS, rc 0
python3 skills/building-tnr-content/scripts/quest_compile.py --selftest        → 9 passed, 0 failed
python3 skills/building-tnr-content/scripts/quest_compile_integration_test.py  → 2 PASS, rc 0
cd forge && npm ci                                                            → ok (3 high advisories, see F15)
cd forge && npm test                                                          → 308 tests, 308 pass, 0 fail
cd forge && npm run fixtures && git diff --exit-code -- test/fixtures/envelope → clean
cd forge && npm run build                                                     → 427.2 KB; sha256 identical to checked bundle
git diff --exit-code -- forge_bundle.js                                       → clean (bundle parity PASS)
python3 .github/scripts/pack_skills.py (×1 re-run)                             → dist zips byte-identical, git clean
python3 skills/building-tnr-content/scripts/doctrinemap.py                     → 21 assertions, 0 errors, 0 warnings
python3 skills/building-tnr-content/scripts/render_doctrine.py --check         → all projections current (exit 0)
python3 skills/building-tnr-content/scripts/build_packs.py --check             → all packs and TOCs current (exit 0)
python3 skills/building-tnr-content/scripts/catalog_sync.py --selftest         → OK
python3 skills/building-tnr-content/scripts/lawmap.py .                        → 93/93/77, 0 errors, 5 warnings (= base)
python3 skills/building-tnr-content/scripts/mission.py --selftest              → rc 1 (pre-existing on main; see F15/debt #7)
```

Adversarial scratch harnesses (scratch only, not committed, removed after use):

```
unknown-subtype Quest Source  → compiler emits requestId:null; Forge validateBuildResult rejects it   (F4)
S-rank Quest Source           → status blocked / decision_required, six fields named                  (verified claim)
C- and B-rank Quest Source with no combat nodes → status valid, enemies []                            (F5)
real 48_DATA_mission_profiles.json driven through QuestStudioWorkspace under jsdom                    (F2)
8 generatedArtifactPath traversal probes through the public adapter method                            (F8)
main@305a28f's release_loader.test.mjs run against the frozen tree → 8 pass / 1 fail                   (F1)
same test run against base 305a28f                            → 8 pass / 1 fail (pre-existing)        (F1)
```

---

## Architectural reconciliation (A–E)

Assessed against the completed Forge Next planning package as an architecture lens only. Where that
package left something as an open director decision, this implementation is **not** judged against it.

### A. Preserve unchanged

- **The repository worker's trust boundary.** Trusted-compiler checkout at `github.sha` under
  `tools/`, authored content under `request/`, all untrusted inputs through `env:`, exact-SHA
  pinning, symlink refusal, path-allowlisted `git add`, push only to the validated request branch.
  This is the correct shape and should survive into ForgeCore unchanged.
- **The `valid | blocked | failed` envelope with provenance and `liveGameTouched:false`.** The
  conservative `classify_mission_error` posture — only known human-decision refusals become
  `blocked`, everything else stays `failed` — is the right default and should not be loosened.
- **`quest_compile.py`'s adapter dispatch through a repository-owned registry.** Adding Event/Story/
  Raid is adapter work, exactly as intended.
- **`49_DATA_quest_studio_subtypes.json` as a repository-owned contract** with `maturity` +
  `compilerAdapter`, and the honest "visible but not executable" presentation of immature subtypes.
- **Branch-scoped `put` with legacy `main` defaults preserved.** The explicit opt-in is the right
  call and the legacy-compatibility test should be kept verbatim.
- **Artefact production into `$RUNNER_TEMP` followed by `cp -a` into a fixed directory.** This is a
  stronger confinement than any path-string check and should be kept as the primary mechanism.

### B. Move behind / into ForgeCore

- **`QuestStudioRepository` in its entirety.** Request identity, branch/path derivation, submit,
  dispatch, result read, staleness and artefact confinement are headless-core concerns with no DOM
  dependency. It already imports nothing from `ui/`; it is close to lift-and-shift.
- **`Github` transport, with the F9 dispatch allowlist folded in.** Core should own the single place
  a bearer token exists, and should own the workflow allowlist rather than relying on call sites.
- **`missionSourceFromDraft` and `missionDraftProblems`.** These are pure functions today (good).
  They belong in core as the Mission subtype adapter's browser half, with F2's sentinel-aware reader
  as their contract for reading profile data — and with their advisory status enforced structurally
  (F5's repository-side conformance check is the matching half).
- **Build-state machine.** `busy / waiting / error / result{valid,blocked,failed} / stale` is
  currently inline in the workspace class. Lift it to core as an explicit state machine and extend it
  to the eight states `FORGE_NEXT_REPO_BACKED_STUDIO_ARCHITECTURE.md` §11 names (F6).
- **Draft persistence.** `readDraft`/`writeDraft` should become a core draft store with a real key
  space and cross-tab ownership (F13), not a single `localStorage` slot.

### C. Temporary shell/UI scaffolding to replace

- **`STUDIO_CSS` and the `.qs-*` class family.** ~48 lines of hard-coded hex and a private full-screen
  overlay. Replaced wholesale by the unified design system's tokens and surfaces. F7 disappears for
  free once the Studio is a route in the shell rather than a `position:fixed` overlay appended to
  `app.root`.
- **`install()`'s launcher-button injection into `$top`.** Navigation belongs to the shell.
- **`renderFrame` / `renderHome` / `renderMission` / `renderBuildState`.** Full-subtree re-render on
  every keystroke-adjacent state change, with `this.field(...)` rebuilding inputs each pass. It works
  (the `value`-as-property fix is what makes it work), but it is scaffolding, not the target
  rendering model.
- **`showExport` as the manifest surface.** Replace with a real result/preflight surface (F7,
  `FORGE_NEXT_QUEST_STUDIO.md` §15.8).
- **The hand-rolled callout/eyebrow/status vocabulary.** Superseded by
  `FORGE_NEXT_UI_COPY_AND_STATE_LANGUAGE.md` and `FORGE_NEXT_SAFETY_STATE_PRESENTATION_CONTRACT.md`.

### D. Fundamental conflicts with the recommended architecture

**None.** I looked specifically for four and found none:

1. *Does the seam put canonical policy in the browser?* No. Profiles, contracts and compilation are
   read/executed from the repository. F2 and F5 are bugs in reading and in where a check lives, not
   architectural inversions — both fixes move enforcement toward the repository, not away.
2. *Does it couple compile to the live runner?* No. The Studio modules have zero references to
   Session/Runner/transport; the absence of a promotion path is deliberate and correct.
3. *Does it fork state ownership?* No. The only local state is a draft; every durable fact is a
   repository read with provenance.
4. *Does the UI shell foreclose the unified design?* No. It is an overlay bolted onto `$top`; nothing
   in core depends on it.

The two places where the seam and the target architecture *rub* are both open questions the design
docs already flag as unsettled (`FORGE_NEXT_QUEST_STUDIO.md` §16): build-trigger choice
(`workflow_dispatch` vs push vs `repository_dispatch`) and the browser credential model. F9 offers a
recommendation; neither is a conflict, and neither is mine to settle.

### E. Integrate first, then absorb incrementally?

**Yes — incremental absorption is viable, and no confirmed blocker prevents integration** once F1 and
F3 are corrected.

The seam's value is in the parts that are already in the right place (A) and the parts that move
without redesign (B). Absorption order I would recommend when the integration contract is written:

1. lift `repository.mjs` + `github.mjs` into ForgeCore behind the headless boundary (no behaviour change);
2. lift the build-state machine and extend it to the §11 state set (closes F6);
3. lift the Mission adapter's browser half with the sentinel-aware profile reader (closes F2);
4. add the repository-side profile-shape conformance check (closes F5) — independent of all UI work;
5. replace the UI shell last, when the design system lands (closes F7, retires C).

Steps 1–4 are all repository/core work that can proceed while the shell is still the current overlay.
That is the sequence I would expect to see in the unified integration contract.

---

## Is the target safe to enter the correction/integration loop?

**Yes.**

- **Required before merge to `main`:** F1 (restore the loader `@match` allowlist assertions; disclose
  the inherited-test fix) and F3 (correct the PAT scope instruction, or adopt F9's
  `repository_dispatch` recommendation and keep Contents-only).
- **Should be in the same correction round:** F2, F4, F5, F6, F7 — all small, all localised, none
  architectural.
- **May be scheduled:** F8, F9 (allowlist half), F10, F11, F13, F14.
- **Track separately, do not block:** F12 (lifecycle — needs a dauntless ruling), F15 (dependency debt).

No finding requires redesigning the seam, and none justifies discarding it. The approved
repository-backed Studio boundary is demonstrated working: a browser-authored Quest Source reaches a
trusted repository compiler, canonical Mission policy stays in `mission.py` and the profile file,
unresolved director rulings come back as structured blockers rather than guesses, the compiled
artefact is reproducible and confined, and nothing in the path can reach the live game.

Corrections are returned to **ChatGPT as implementation owner**. This review implements none of them
and did not modify `chatgpt/forge-quest-studio-foundation`.

After ChatGPT returns a corrected SHA, the re-review scope can be narrowed to F1–F7 plus a bundle/
gate re-run, provided the fixes do not touch the worker trust boundary or the transport layer. Once
the planning-package correction round is also complete, the next workflow step is the unified
integration contract described in E.
