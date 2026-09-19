# Godstorm / Forge defects repair — implementation handoff

**Status: IMPLEMENTATION REQUIRED / EVIDENCE FROZEN FOR HANDOFF**

This handoff turns the failed Godstorm operator push into a bounded Lane A Forge repair task. The live game is production. The user remains the only live-game operator. Fable / Claude Code owns the Forge implementation. ChatGPT should independently review the exact frozen Fable SHA before the user runs the repair manifest.

| Field | Value |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Current main | `8c47d52cbabd8bf712f8bb0f76da0f4ff9383dc3` |
| Main head meaning | committed Forge result `harvests/inbox/tnr_results_1789829183863.json` |
| Planning / evidence branch | `chatgpt/godstorm-two-pyramid-plan` |
| Planning branch pre-handoff head | `dfae60d524cb5b9c13021d5052da1ef9beb8a75b` |
| Upstream game source inspected | `studie-tech/TheNinjaRPG@a670c9aaa741157dc66eacc949600ff2db0b48cd` |
| Forge UI version observed | `forge 0.4.1` |
| Failed final manifest | `push/52_godstorm_two_pyramid_final_update_v4.json` |
| Authoritative run evidence | `harvests/inbox/tnr_results_1789829183863.json` |
| Targeted repair manifest | `push/53_godstorm_failed_items_repair.json` on this branch only; **do not stage/run until Forge fixes are reviewed** |
| Suggested Fable branch | `fable/godstorm-forge-defects-repair` from fresh current main |
| Live requests/writes by ChatGPT | **none** |
| Operator live writes already made | yes: manifest 52 partially applied; exact persisted state is captured below |
| Credentials | none used or requested by ChatGPT |

## 1. Executive result

The Godstorm run did not fail atomically. It partially applied.

The committed Forge bundle reports:

- job state: **INCOMPLETE**
- outcome: **failed**
- 28 manifest items total
- **9 FAILED**
- **18 CONFIRMED / verify**
- **1 VERIFIED**
- four requested post-run full captures all succeeded and persisted

The live-state conclusion from those captures is:

1. **Marrow Vaults final quest update landed and VERIFIED.**
2. **All 18 AI-profile Law 40 corrections landed.** Forge left them CONFIRMED because its verifier reported a `rules` drift, but the exported `sent` and `live` structures are semantically identical for every one of the 18 entries.
3. **The three new Stormcourt background assets did not get created.**
4. **The five new Marrow avatar updates did not land.**
5. **Stormcourt quest update did not land** because the failed background creates left its `@scene:` references unresolved.
6. The post-run Stormcourt capture proves the live quest is still the old Tower-era 61-objective version.

Do **not** replay the full 28-item manifest. The nine unapplied writes have already been isolated in `push/53_godstorm_failed_items_repair.json`.

---

## 2. Incident chronology

### 2.1 Manifest 49 — AI Law 40 preflight failure

The first final manifest used direct jutsu range as `distance_lower_than`. Forge correctly rejected it before mutation because Engine Law 40 uses A* path length including both endpoints:

- range 3 -> gate 4
- range 4 -> gate 5
- range 5 -> gate 6
- SELF / ALL actions -> no distance gate

That defect was corrected before the later live write.

### 2.2 Manifest 50 — corrected AI rules, blocked in asset-name dedup

Manifest:
`push/50_godstorm_two_pyramid_final_update_v2.json`

Observed Forge pause:

```
Paused: NETWORK
dedupNames: gameAsset.getAllNames failed: BAD_REQUEST
{
  "expected": "object",
  "code": "invalid_type",
  "path": [],
  "message": "Invalid input: expected object, received undefined"
}
```

No manifest mutation was sent in that attempt.

### 2.3 Manifest 51 — dedup disabled, but journal hash collision

Manifest 51 changed `dedupNames:true` to `false` to bypass the failing dedup pass.

Forge refused to open it:

```
plan: journal: an open job for this manifest already exists
(50-mu8hlyma); resume it instead
```

This exposed a second Forge defect: manifest hashing excludes `dedupNames`.

Exact locally reproduced hashes using Forge's own `stableStringify` + FNV-1a contract:

```
manifest 50  dedupNames=true   hash=d5164ee3
manifest 51  dedupNames=false  hash=d5164ee3
manifest 52  dedupNames=false  hash=330fd853
```

Manifest 52 only got a different hash because an additional post-run capture was added.

### 2.4 Manifest 52 — partial live application

Manifest:
`push/52_godstorm_two_pyramid_final_update_v4.json`

Operator ran it. Forge auto-committed:

`harvests/inbox/tnr_results_1789829183863.json`

at main commit:

`8c47d52cbabd8bf712f8bb0f76da0f4ff9383dc3`.

Final item-state counts:

```
FAILED     9
CONFIRMED 18
VERIFIED   1
```

The exact failures and persisted state are below.

---

## 3. Exact item results from manifest 52

### Items 0-2 — all three Stormcourt asset creates FAILED before create

| idx | item | result |
| ---: | --- | --- |
| 0 | Godstorm Stormcourt Upper Court | FAILED |
| 1 | Godstorm Stormcourt Binding Dais Active | FAILED |
| 2 | Godstorm Stormcourt Binding Dais Released | FAILED |

Exact error on each:

```
snapshot failed: gameAsset.getAllNames BAD_REQUEST
```

No asset ID was minted. No `godstorm_sc_upper`, `godstorm_sc_dais_active`, or `godstorm_sc_dais_released` mapping exists in the result idmap.

This happened **even with `dedupNames:false`** because create reconciliation takes a separate pre-create name-list snapshot.

### Items 3-7 — all five Marrow avatar edits FAILED locally

| idx | avatar | selected file reported by Forge | bytes | ceiling |
| ---: | --- | --- | ---: | ---: |
| 3 | Starless Monk | `1000014259.png` | 1,709,179 | 524,288 |
| 4 | Hollow Lantern | `1000014258.png` | 1,616,414 | 524,288 |
| 5 | Umbral Reaver | `1000014257.png` | 1,464,991 | 524,288 |
| 6 | Nightveil Sentinel | `1000014260.png` | 1,339,617 | 524,288 |
| 7 | Warden of the First Dark | `1000014261.png` | 1,803,427 | 524,288 |

Exact error pattern:

```
<selected png> is <bytes> bytes; imageUploader ceiling is 524288
```

The manifest expected processed WebPs. The operator-selected PNG masters were not the expected upload artifacts.

The correct processed files are:

| expected file | exact bytes | SHA-256 |
| --- | ---: | --- |
| `ai_godstorm_marrow_umbral_reaver.webp` | 161,650 | `30693d5dc252f8ce61638a0b4c191523ef7df8461b8252ff309e21192154bfcc` |
| `ai_godstorm_marrow_hollow_lantern.webp` | 196,056 | `50d1786fb6f5c2a2350b04dd27ec1ff8b0e1d58237e98337c0a2065e226b6055` |
| `ai_godstorm_marrow_starless_monk.webp` | 207,410 | `877eef3b0cecc914d4e3300e21cb50c87030093c5730d4feb54b71a7e7cdc870` |
| `ai_godstorm_marrow_nightveil_sentinel.webp` | 115,618 | `d5c5a8c8a2be20700a7df16b9ac38e4b9cd6a7a2917efa5d7d815d19deebd9e2` |
| `ai_godstorm_marrow_warden_of_the_first_dark.webp` | 238,510 | `0d2bf09980ec6c99226d3528606cf07a112ccf0c843363f5d0761ae0ca997453` |

Post-run full capture of Warden of the First Dark still shows the default avatar URL, confirming its update did not land.

### Items 8-25 — all 18 AI-profile updates reached the live record

All 18 are:

```
state = CONFIRMED
phase = verify
error = null
diffs = [{ key: "rules", sent: ..., live: ... }]
```

However, replaying the exported `sent` and `live` values through a key-sorted semantic comparison found them equal for **18/18** items.

The live payloads show the intended corrected rules:

- opponent-target specific jutsu at exact `range + 1`
- opponent-target combos at exact shared `range + 1`
- SELF jutsu with no distance condition
- bounded adjacent highest-damage fallback at path-distance 2

Examples present in the committed result:

```
Umbral Reaver
Quick Strike range 3 -> gate 4
combo range 5 -> gate 6
SELF Warrior's Poise -> no distance gate
highest damage fallback -> <=2
```

```
Starless Monk / Nightveil Sentinel / Warden First Dark /
Gloaming Judge / Herald
Opening Strike range 4 -> gate 5
combo range 5 -> gate 6
SELF stance -> no distance gate
fallback -> <=2
```

Do not replay these 18 writes in the content repair manifest.

### Item 26 — Marrow Vaults VERIFIED

```
idx 26
Marrow Vaults final update
state VERIFIED
entityId 2yvE9PUQqlD8lbYNfgX-b
```

Full post-run `quests.get` confirms:

- name: `Marrow Vaults`
- 53 objectives
- 25 battles
- 26 dialogs
- no `d*_choice` / `d*_cash` nodes
- connected-setting copy is live
- approved background remap is live
- quest-level `sceneCharacters = ["1YXbXYW2wz3GETVMb6DT6"]`
- dialog scene character fallback is live
- final reward item list is empty
- numeric final reward remains 125,000 ryo / 25 tokens / 10 prestige
- `retryDelay:"none"`, `maxAttempts:100`, `maxCompletes:100` remain as captured

Do not replay Marrow in the repair manifest.

### Item 27 — Stormcourt FAILED before update

Exact failure class:

```
unresolved refs:
@scene:godstorm_sc_upper ...
@scene:godstorm_sc_dais_active ...
@scene:godstorm_sc_dais_released ...
```

The dependency references could not resolve because items 0-2 never created their assets.

Full post-run Stormcourt capture proves **no final quest update landed**:

- old name: `The Tower of Endless Night: The Stormcourt`
- 61 objectives
- 25 battles
- 34 dialogs
- all eight cash-out / choice nodes still present
- old Tower / Dawnless Crown prose still present
- old final item rewards still present
- no new background wiring
- old keeper reroutes still live

---

## 4. Post-run captures — all four succeeded

Manifest 52 requested four full captures. All four read successfully and persisted exact bodies.

| capture | result |
| --- | --- |
| `profile.getAi` — Warden of the First Dark | OK / full body persisted |
| `gameAsset.get` — Blank Scene Character | OK / full body persisted |
| `quests.get` — Marrow Vaults | OK / full body persisted |
| `quests.get` — Stormcourt | OK / full body persisted |

Blank scene-character evidence:

```
id: 1YXbXYW2wz3GETVMb6DT6
name: Blank Scene Character
type: SCENE_CHARACTER
hidden: true
folder: ghostship
```

This is the current approved fallback for both pyramids. Keeper-specific portrait production remains optional later art enhancement, not a repair prerequisite.

---

## 5. Confirmed Forge defect A — list-query input contract is wrong

### Current Forge code

`forge/src/budget/reader.mjs`:

```js
/** A list procedure (getAll / getAllNames / getAllAiNames): cached under id "". */
async list(path, { fresh = false } = {}) {
  ...
  const [r] = await this.client.batch([{ path, input: undefined }]);
  ...
}
```

The comment itself assumes the name-list procedures take no input.

### Current upstream server contract

Current upstream main verified:

`studie-tech/TheNinjaRPG@a670c9aaa741157dc66eacc949600ff2db0b48cd`

`app/src/server/api/routers/asset.ts`:

```ts
getAllNames: publicProcedure
  .input(
    z.object({
      type: z.enum(GameAssetTypes).optional(),
      folderPrefix: z.boolean().optional(),
    }),
  )
```

Therefore the valid no-filter call is `{}`, not `undefined`.

### Two independent Forge paths are broken by the same assumption

1. `Runner._dedupNames()` calls:

```js
this.reader.list(rc.names, { fresh: true })
```

2. `Reconciler.beforeCreate()` separately calls:

```js
const list = await this.reader.list(rc.names, { fresh: true })
```

That second path is why disabling `dedupNames` did not unblock asset creation.

### Required shape of the fix

Do **not** special-case the Godstorm manifest.

Repair the query-input contract centrally. At minimum `gameAsset.getAllNames` must send `{}`. Better: audit every procedure currently permitted through `CachedReader.list()` against current upstream and use an explicit per-procedure input adapter rather than another regex assumption.

The existing `readInput(path,id)` precedent is the right architectural pattern: explicit path -> input shape, fail closed for unsupported list procedures.

### Required regression coverage

Must cover both paths:

1. dedupNames asset create succeeds against a fake server/router that rejects undefined and accepts `{}`;
2. `Reconciler.beforeCreate` snapshot succeeds under the same contract;
3. crash/reconcile semantics for asset creates remain intact;
4. a truly failing list read still pauses/fails safely and does not create;
5. no other name-list procedure regresses.

Reviewer should reject a patch that only modifies `_dedupNames`; it would leave `beforeCreate` broken.

---

## 6. Confirmed Forge defect B — manifest hash omits execution-affecting top-level fields

`forge/src/runner/manifest.mjs` currently hashes:

```js
hash: fnv1a32(stableStringify({
  items: raw,
  capture: rawCapture
}))
```

It does **not** hash `dedupNames`.

Observed result:

```
manifest 50  dedupNames=true   -> d5164ee3
manifest 51  dedupNames=false  -> d5164ee3
manifest 52  dedupNames=false  -> 330fd853
```

Manifest 51 was blocked by job 50 because Forge considered them the same manifest.

This is more than an inconvenience: the journal hash is also the compatibility guard used when attaching/resuming an existing job. Execution policy that can alter whether a job performs safety reads should not be invisible to that guard.

### Reviewer must widen the audit beyond `dedupNames`

Do not stop at adding one boolean.

Audit every top-level manifest key that can alter execution, validation, upload, persistence, or verification. In particular examine:

- `dedupNames`
- `imgSizes`
- `readBack`
- `skipPreflight`
- capture persistence inputs already covered by `capture`
- any future execution-policy switches

`_note` need not be execution-significant merely because it changes prose.

The implementation must preserve compatibility intentionally. If expanding the hash means old open jobs cannot attach under a new bundle, document/migrate that consequence rather than pretending it does not exist.

### Required tests

- toggling `dedupNames` changes hash;
- changing `imgSizes` changes hash if the ledger is deemed execution contract;
- purely changing `_note` does not change hash, if that remains the intended policy;
- same executable manifest remains stable/deterministic;
- attach rejects genuinely changed execution contracts;
- old-version migration behavior is explicit.

---

## 7. Confirmed observable defect C — AI profile verification false drift

The 18 AI-profile writes all reached live state. Yet every item remained:

`CONFIRMED / phase verify`

with a `rules` diff.

The committed result serializes each diff as:

```json
{
  "key": "rules",
  "sent": [...],
  "live": [...]
}
```

and a key-sorted recursive comparison over those exported values returns equality for all 18.

Current comparator:

`forge/src/runner/validate.mjs` -> `diffAsserted()` / `eqLoose()`.

The exact root cause is **not yet proven**. Do not paper over it by exempting `aiProfile.rules` from verification.

### Required reproduction method

Build a regression fixture from the actual committed result, not a synthetic one that merely looks similar:

`harvests/inbox/tnr_results_1789829183863.json`

For at least one affected profile:

1. materialize the manifest's asserted `rules`;
2. materialize the read-back `live.rules`;
3. reproduce why `diffAsserted("aiProfile", asserted, live)` returns a diff in the running code;
4. instrument raw types / own keys / array contents before JSON serialization if the exported values compare equal;
5. prove the correction still catches a real nested rules drift.

### Required tests

- exact Godstorm sent/live pair compares equal;
- mutate one gate value -> drift detected;
- mutate target -> drift detected;
- remove a rule -> drift detected;
- reorder rules -> drift detected unless ordering is explicitly non-semantic;
- extra server-owned / server-normalized nested material is treated according to explicit contract, not blanket ignored.

Reviewer should attack any fix that simply compares `JSON.stringify` or suppresses `rules` verification globally without proving the semantic model.

---

## 8. Confirmed operator-safety / UX debt D — image picker accepts the wrong physical file

The manifest asked for names such as:

`ai_godstorm_marrow_starless_monk.webp`

The UI rendered that expected logical filename as “picked”, but the run later reported the selected physical file as:

`1000014259.png`

at 1.7 MB.

Current picker code in `forge/src/ui/screens.mjs`:

```js
const inp = h("input", {
  type: "file",
  accept: "image/*",
  ...
  onChange: (e) => {
    const f = e.target.files[0];
    if (f) {
      app.runner.files.set(name, f);
      app.refresh();
    }
  }
});
```

The map key is the expected manifest name; the selected `File.name` can be anything. The UI then shows “picked” with no immediate contract check.

The uploader eventually catches the 524,288-byte ceiling, so this incident did not corrupt data. But the safety feedback is late and misleading.

### Recommended repair

At selection time, validate the physical file against the manifest image contract:

- expected logical filename / extension;
- exact `imgSizes[name]` when present;
- uploader hard ceiling;
- ideally a lightweight image-type check consistent with existing uploader policy.

The UI should show the actual selected file name and byte size when it differs from expected, and should not enable Start while any image selection violates the ledger.

Do not silently rename arbitrary selected bytes to satisfy the manifest key.

### Tests

- wrong filename selected -> blocked;
- wrong byte size -> blocked;
- over ceiling -> blocked before job open;
- exact processed WebP -> accepted;
- selecting a replacement updates the status correctly;
- eight-image Godstorm manifest cannot start with one wrong master PNG hidden behind a “picked” pill.

This item is not the reason background creation failed, but it is why all five avatar writes failed.

---

## 9. Repair manifest 53

Prepared on the ChatGPT planning branch only:

`push/53_godstorm_failed_items_repair.json`

Purpose: replay **only the nine writes that did not land**.

Contents:

```
3 asset creates
5 AI avatar edits
1 Stormcourt quest edit
= 9 writes
```

Explicitly omitted:

- 18 AI-profile edits — already landed;
- Marrow Vaults — already VERIFIED.

The repair manifest restores `dedupNames:true` because the Forge implementation is supposed to repair the actual list contract, not rely on a bypass.

Do not stage manifest 53 to `main` or run it until the Forge implementation is frozen, independently reviewed, and accepted.

The Stormcourt item still intentionally uses same-job refs:

- `@scene:godstorm_sc_upper`
- `@scene:godstorm_sc_dais_active`
- `@scene:godstorm_sc_dais_released`

A correct Forge run must create those three assets, remember their IDs, resolve the quest references, update Stormcourt, and read it back.

---

## 10. Exact image contract for repair run

### Backgrounds

| file | bytes | SHA-256 |
| --- | ---: | --- |
| `bg_godstorm_stormcourt_upper_court.webp` | 379,928 | `c0587d9fdeb8c4c75ecc6f5eaf0c08a0b783461299793c774f66f7aaab4f12b9` |
| `bg_godstorm_stormcourt_binding_dais_active.webp` | 283,000 | `41ca12f9d21604151f754ded0df2211bed5b671dcc2dd7c954e53c5f17f36d70` |
| `bg_godstorm_stormcourt_binding_dais_released.webp` | 256,826 | `97fc11d4ad1c24beeaffaf2e7f8a589715806dce6d17290d0fa253694fd3ef18` |

### Avatars

See §3. Files are all under 460,800 bytes and under the 524,288-byte uploader ceiling.

The operator convenience ZIP prepared in chat contains only the five processed avatar WebPs. The repository manifest ledger remains the authority for names and byte counts.

---

## 11. Commands / probes executed and observed results

ChatGPT did not have a normal mutable clone for this investigation. Repository and upstream inspection used exact GitHub REST/content reads through the authorized connector; local computation was used only for archive/image/hash analysis. No game endpoint was called by ChatGPT.

### Ref checks

```
GET /repos/perseverance484/tnr-tools/branches/main
-> 8c47d52cbabd8bf712f8bb0f76da0f4ff9383dc3
-> "results: tnr_results_1789829183863.json (forge)"
```

```
GET /repos/perseverance484/tnr-tools/commits?sha=chatgpt%2Fgodstorm-two-pyramid-plan&per_page=1
-> dfae60d524cb5b9c13021d5052da1ef9beb8a75b
-> "manifest: isolate failed Godstorm writes for repair"
```

```
GET /repos/studie-tech/TheNinjaRPG/branches/main
-> a670c9aaa741157dc66eacc949600ff2db0b48cd
```

### Result read

```
GET repository file:
harvests/inbox/tnr_results_1789829183863.json@main
-> 440,163 bytes
-> journal state INCOMPLETE
-> outcome failed
-> 9 FAILED / 18 CONFIRMED / 1 VERIFIED
-> 4/4 full after-captures OK + persisted
```

### Forge code reads

```
forge/src/budget/reader.mjs@main
-> list() sends { path, input: undefined }
```

```
forge/src/reconcile/reconciler.mjs@main
-> beforeCreate() always calls reader.list(rc.names, {fresh:true})
-> asset creates therefore still hit gameAsset.getAllNames even when dedupNames=false
```

```
forge/src/runner/manifest.mjs@main
-> hash = fnv1a32(stableStringify({items: raw, capture: rawCapture}))
-> dedupNames / imgSizes / other top-level execution fields omitted
```

```
forge/src/runner/validate.mjs@main
-> diffAsserted()
-> eqLoose()
-> no intentional blanket exemption for aiProfile.rules
```

```
forge/src/ui/screens.mjs@main
-> image picker stores arbitrary selected File under expected manifest-name key
-> no immediate filename or imgSizes check at selection
```

### Current upstream route read

```
studie-tech/TheNinjaRPG
app/src/server/api/routers/asset.ts@a670c9aaa741157dc66eacc949600ff2db0b48cd

gameAsset.getAllNames input:
z.object({
  type: z.enum(GameAssetTypes).optional(),
  folderPrefix: z.boolean().optional(),
})
```

Result: `undefined` is invalid; `{}` is the empty-filter input.

### Manifest hash reproduction

Using the exact Forge stable stringify / FNV-1a contract over normalized raw capture shape:

```
50: dedupNames=true   d5164ee3
51: dedupNames=false  d5164ee3
52: dedupNames=false  330fd853
```

The only reason 52 differs is its extra capture entry.

### Semantic replay of exported profile diffs

For every item 8-25, recursively sort object keys and compare the exported `diffs[].sent` and `diffs[].live`:

```
18 / 18 equal
```

This proves the observable false-drift symptom. It does **not** prove the internal cause.

### Correct avatar extraction

Processed avatar bundle contents checked:

```
ai_godstorm_marrow_hollow_lantern.webp       196056
ai_godstorm_marrow_nightveil_sentinel.webp  115618
ai_godstorm_marrow_starless_monk.webp        207410
ai_godstorm_marrow_umbral_reaver.webp        161650
ai_godstorm_marrow_warden_of_the_first_dark.webp 238510
```

All are below the uploader ceiling.

---

## 12. Reproduction / implementation command sequence for Fable

These are the commands the implementation owner should run in a real clone. Record actual outputs in the implementation handoff; do not substitute the expected values below for real execution.

```bash
git fetch origin --prune
git switch main
git pull --ff-only
git rev-parse HEAD
# expected starting point at handoff time:
# 8c47d52cbabd8bf712f8bb0f76da0f4ff9383dc3

git switch -c fable/godstorm-forge-defects-repair
```

Reconstruct state and read the governing files before implementation:

```bash
sed -n '1,240p' state/active-context.md
cat state/status.json
sed -n '1,260p' docs/00_INDEX.md
sed -n '1,320p' docs/RULINGS.md
sed -n '1,280p' CLAUDE.md
sed -n '1,320p' docs/DEVELOPMENT_WORKFLOW.md
sed -n '1,260p' docs/agents/README.md
sed -n '1,340p' docs/handoffs/GODSTORM_FORGE_DEFECTS_REPAIR_HANDOFF.md
```

Baseline Forge:

```bash
cd forge
npm ci
npm test
npm run fixtures
git diff --exit-code -- test/fixtures/envelope test/fixtures/screens
npm run build
git diff --exit-code -- ../forge_bundle.js
node tools/check_imports.mjs
node tools/check_boundaries.mjs
node tools/check_bundle_budget.mjs
cd ..
```

Inspect the exact incident evidence:

```bash
python - <<'PY'
import json
p='harvests/inbox/tnr_results_1789829183863.json'
r=json.load(open(p))
from collections import Counter
print(r['state'], r['outcome'])
print(Counter(i['state'] for i in r['journal']['items']))
for i in r['journal']['items']:
    print(i['idx'], i['state'], i['name'], i.get('error',''))
PY
```

Expected headline:

```
INCOMPLETE failed
Counter({'CONFIRMED': 18, 'FAILED': 9, 'VERIFIED': 1})
```

After implementation, add focused tests for all repaired contracts, then run the complete baseline sequence again.

Do **not** make a real game request to test this branch. Use FakeGame / transport fixtures / exact committed result fixtures. Browser-only UI behavior can be checked locally without contacting the live game.

Freeze the exact branch head and hand it to ChatGPT for independent review.

---

## 13. Debt list

### Must fix before repair manifest 53

1. **List-input contract drift:** `gameAsset.getAllNames` object input vs Forge `undefined`.
2. **Pre-create snapshot path:** prove asset create works through `Reconciler.beforeCreate`, not just dedup.
3. **Manifest hash completeness:** execution-affecting policy must not collide as 50/51 did.
4. **AI-profile false verify drift:** root cause + regression; do not replay the 18 live-correct profiles.
5. **Image picker contract check:** at minimum prevent the exact wrong-master-PNG failure before job start if included in this repair scope.

### High-value Forge debt exposed by this incident

6. Audit **all** `CachedReader.list()` procedures against current upstream route input schemas. One stale regex assumption caused two independent failures.
7. Audit manifest hash coverage of `imgSizes`, `readBack`, `skipPreflight`, and any execution flags.
8. Clarify job-result semantics when server readback is actually equal but verifier reports drift. A user should not have to inspect raw JSON to know whether a production write landed.
9. Image picker should display both logical expected filename and actual selected physical filename/bytes.
10. Add a fixture representing a partial multi-entity production run: creates fail, edits succeed, dependent quest ref resolution fails, post-run captures still complete.

### Existing repo / release debt, not a blocker to the narrow code fix

11. Forge source contracts are visibly behind upstream; main already carries upstream-drift sentinel history. This incident is a concrete consequence. Do not silently adopt the entire upstream contract set inside this narrow repair, but record the need for deliberate contract regeneration/adoption.
12. Keeper-specific Godstorm `SCENE_CHARACTER` portraits are not produced. The existing Blank Scene Character is the accepted current fallback.
13. Final reward/balance/playtest signoff remains user/content-admin work after the technical repair.
14. Manifest 52 is now a spent partial-run artifact and result 1789829183863 is its authoritative evidence. Let normal scrub/archive policy handle it; do not delete evidence ad hoc.
15. The operator's local incomplete job may remain in the browser journal. No implementation should require deleting it to make the new repair manifest work.

---

## 14. What the reviewer should attack hardest

### Attack 1 — prove asset creates are safe across every path

The most important target is not “does getAllNames return 200 now?” It is whether create safety remains correct.

Try to break:

- normal dedup preflight;
- pre-create snapshot;
- crash after create request left but before response;
- multiple same-entity creates;
- resume/reconciliation;
- a list endpoint returning BAD_REQUEST / network failure / 429;
- stale cache vs `fresh:true`;
- empty-object input serialization in single and batched tRPC GETs.

A patch that bypasses snapshots, disables dedup globally, or catches BAD_REQUEST and continues is unacceptable.

### Attack 2 — hash identity must mean execution identity

Construct pairs of manifests identical in items/captures but different in:

- dedupNames;
- imgSizes;
- other execution switches.

Try to attach/resume a job with the wrong policy. The hash must refuse unsafe equivalence or there must be an explicit versioned compatibility layer.

This incident demonstrated the bug in production operator workflow, not merely in a unit test.

### Attack 3 — do not weaken AI verification to make the false drift disappear

The repair must explain the exact false positive.

Feed the verifier:

1. the exact exported equal Godstorm pair -> no drift;
2. one changed gate -> drift;
3. one changed target -> drift;
4. missing rule -> drift;
5. reordered rule -> whatever the documented semantic policy says, with a test.

Reject “ignore rules”, “stringify both sides”, or broad normalization that can hide a real target/range error.

### Attack 4 — picker must bind the operator to the manifest's bytes

The user saw “picked” beside an expected `.webp` name while Forge actually held a large `.png`.

Try malicious/accidental selections:

- different filename, same MIME;
- right filename, wrong byte count;
- wrong extension;
- > hard ceiling;
- processed image with exact ledger;
- replacing a bad selection with a good one;
- page reload / remount if file handles are not persistent.

The UI must make the physical bytes obvious before Start.

### Attack 5 — repair manifest idempotence and dependency resolution

After code review passes, validate `push/53_godstorm_failed_items_repair.json` locally:

- exactly nine writes;
- no AI-profile writes;
- no Marrow quest write;
- three background creates precede Stormcourt;
- Stormcourt depends on the three `@scene:` srcIds;
- five avatar edits reference exact WebP ledger entries;
- same-job ID mapping resolves every scene ref;
- post-run captures are sufficient to prove final state.

Try to prove a second run would duplicate background assets. Dedup + reconciliation must make the operator stop safely.

---

## 15. Acceptance gate for Fable implementation

Do not hand back “fixed” based only on unit tests around the edited function.

Required handoff evidence:

- exact branch and frozen SHA;
- exact merge-base / base main;
- changed-file list;
- baseline test count before and after;
- all Forge tests pass;
- generated screen/envelope fixtures clean;
- bundle rebuild clean;
- import/boundary/bundle-budget gates clean;
- focused tests for defects A-D;
- no live-game requests/writes;
- no source pin silently moved;
- no repair manifest run;
- known remaining debt listed explicitly.

Only after independent ChatGPT review accepts the frozen SHA should manifest 53 be staged to main for the user-operated live repair.

---

## 16. Current content-side stopping point

The live game is intentionally left in a mixed state until Forge is repaired:

**Live now**
- Marrow Vaults: final connected 25-battle version, verified.
- 18 retained AI profiles: corrected Law 40 rules landed.
- Blank Scene Character: existing reusable asset, verified by capture.

**Still old / absent**
- five Marrow avatars: still old/default because uploads failed;
- three new Stormcourt backgrounds: absent;
- Stormcourt quest: still old Tower/cash-out version.

That mixed state is not a reason to rush a manual write. The repair manifest is intentionally narrow and should be run only after the Forge path that failed is corrected and reviewed.
