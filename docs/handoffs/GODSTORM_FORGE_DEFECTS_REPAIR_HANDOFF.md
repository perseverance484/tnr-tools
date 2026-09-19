# Godstorm Forge defects — repair handoff

**Status: IMPLEMENTED. Awaiting freeze SHA stamp; see the branch head.** Independent ChatGPT review
requested on the exact head SHA recorded below. Lane A (code/tooling), `docs/DEVELOPMENT_WORKFLOW.md`.

| | |
|---|---|
| Repository | `perseverance484/tnr-tools` |
| Implementation branch | `claude/forge-godstorm-defects-repair-rxxwky` (assigned by the task) |
| Base / merge-base | `8c47d52cbabd8bf712f8bb0f76da0f4ff9383dc3` (`main` at start, re-verified at close) |
| Integration target | `main` |
| Live game requests / writes | **none** |
| Credentials used | repository auth for fetch/push only. No game credential, no session material. |
| Evidence bundle under repair | `harvests/inbox/tnr_results_1789829183863.json` (committed at base) |
| Repair manifest (NOT in this branch) | `chatgpt/godstorm-two-pyramid-plan@dfae60d524cb5b9c13021d5052da1ef9beb8a75b` → `push/53_godstorm_failed_items_repair.json` |

## 1. Objective

Fix the two Forge defects named in the task before manifest 53 is staged and run: the
`gameAsset.getAllNames` input-contract break that failed the asset create path, and the AI-profile
read-back comparison that reported 18 landed writes as drift. Nothing else.

## 2. The two defects, as found

### D1 — `gameAsset.getAllNames` was called with no input

`CachedReader.list()` sent `input: undefined` for every name list. At source the asset list alone
carries an `.input()`:

```
gameAsset.getAllNames  .input(z.object({ type: z.enum(GameAssetTypes).optional(),
                                         folderPrefix: z.boolean().optional() }))
```

(`skills/building-tnr-content/data/45f_DATA_procedures.json`, `routers/asset.getAllNames`, extracted
by `schema_extract.py` from `git:studie-tech/TheNinjaRPG@bdec2883`.) **Both members are optional; the
object is not** — the schema carries no `.optional()`, so an absent input fails zod before the
resolver runs and the adapter answers `BAD_REQUEST`. `jutsu`, `item`, `bloodline`, `quests` and
`profile.getAllAiNames` declare no `.input()` at all, so `undefined` is correct for those and this
fix does not touch them.

Both list callers died on it in the live run:

- `Reconciler.beforeCreate()` — the pre-create snapshot. Journal items 0–2:
  `snapshot failed: gameAsset.getAllNames BAD_REQUEST`, three Stormcourt `SCENE_BACKGROUND` creates
  never sent;
- `Runner._dedupNames()` — the same read, one call earlier, for any manifest with `dedupNames`
  (manifest 53 sets it).

Item 27, the Stormcourt quest update, then failed on `unresolved refs: @scene:godstorm_sc_upper …`,
which is the same defect one step downstream: **1 input bug, 4 of the 9 failures.** (The remaining 5,
the Marrow avatar edits, failed on the 524288-byte `imageUploader` ceiling — an art-side input
problem, out of scope here, and already addressed by manifest 53's processed `.webp` files: all 8 of
its `imgSizes` entries are ≤ 380 KB, checked offline.)

### D2 — the AI-profile read-back compared rules as TEXT

`Runner._verify()` compared `JSON.stringify(sent)` against `JSON.stringify(live)`. The server
re-emits a validated document in **schema** key order, so a condition sent as
`{type, value, target, description}` reads back as `{type, description, value, target}`. Every one of
the 18 corrections was reported as drift and left `CONFIRMED` instead of `VERIFIED`. Replaying the
committed bundle: all 18 recorded `sent`/`live` pairs differ as text and parse to **identical**
objects. `Reconciler._resolveRules()` carried the same comparison, where the consequence is worse: a
resumed job would have called a landed rules write `ORPHANED`.

## 3. Changed files and behaviour

| File | Change |
|---|---|
| `forge/src/budget/reader.mjs` | New `LIST_INPUT_FOR` table + exported `listInput(path)`: `{}` for `gameAsset.getAllNames`, `undefined` for the five inputless lists. `list()` now takes an optional `input` and sends `listInput(path)` by default. A caller-supplied **filter** is sent, but is never served from nor written into the single id-`""` cache slot (one slot per path cannot hold two different answers, and `invalidateRecord` finds list captures by that empty id) — a filtered list is always fresh and costs one token. |
| `forge/src/runner/validate.mjs` | New exported `deepEqualPayload(a, b)`: key order is not meaning, a key carrying `undefined` is a key that is not there, and **nothing else** is normalised — array order, `null`, types and both-direction key presence stay strict. Deliberately separate from `eqLoose()`, which is one-sided against a live DB row and applies the ai numeric tolerance (law 71); a rules payload is a closed document sent whole and read back whole. |
| `forge/src/runner/runner.mjs` | Rules read-back uses `deepEqualPayload`. `_captures()` passes a list capture's input through to `list()` and journals **the input the read was actually called with**. |
| `forge/src/reconcile/reconciler.mjs` | `_resolveRules()` uses `deepEqualPayload`. |
| `forge/test/fakegame.mjs` | Holds the source contract now: `gameAsset.getAllNames` refuses a non-object input with `BAD_REQUEST` and honours `type`/`folderPrefix`; `ai.updateAiProfile` stores rules re-keyed (`rekey`) the way zod re-emits them. |
| `forge/test/godstorm.repair.test.mjs` | New. 13 tests (see §4). |
| `forge_bundle.js` | Rebuilt from source by `forge/build.mjs`. |
| `forge/package.json`, `forge/package-lock.json`, `forge/src/main.mjs`, `forge_loader_user.js` | Version staged 0.4.1 → 0.4.2: `@version`/`@require` keep the last released pin and the loader carries `@x-release-pending 0.4.2`, which is the development-branch state `check_release_pin.mjs` requires. |

### Adjacent fix, called out deliberately

`_captures()` previously stamped a list capture's journal entry with the filter the manifest wrote
while `list()` had sent `undefined` — an unfiltered answer recorded against a filtered question, in
the one artifact that is read as evidence ("a type-filtered `gameAsset.getAllNames` cannot see STATIC
records no matter how many exist"). It is in the function D1 forced me to touch and it is the same
class of bug, so it is fixed rather than left; it is flagged here because it is adjacent to the two
named defects rather than one of them. No manifest in flight (53 included) uses a list capture.

## 4. Verification — exact commands and results

All runs local, socket-free, against the fake game. Node v22.22.2.

```
cd forge && npm ci                     # clean install from the committed lockfile
cd forge && npm test                   # 356 tests, 356 pass, 0 fail  (343 at base, +13 new)
cd forge && npm run build              # wrote forge_bundle.js (409.9 KB)
node forge/tools/check_boundaries.mjs  # 37 modules, 0 violations; pin 345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9
node forge/tools/check_imports.mjs     # 37 modules, 63 cross-layer imports, 0 violations
node forge/tools/check_bundle_budget.mjs  # raw 419762/430000 (97.6%), gzip 79915/81000 (98.7%) — PASS
node forge/tools/check_release_pin.mjs # release pin ok
node forge/tools/check_manifest.mjs <manifest 53 from the chatgpt branch>
                                       # 9 planned items, hash f3d63184, 0 pre-send problems
```

`npm test` runs the static gates too (`test/gates.test.mjs` calls `checkBoundaries`, the bundle
budget and the release-pin gate), so the checked-in bundle is inside its budget as tested.

**The fixture reproduces both defects.** With `forge/src` reverted to its pre-fix state and the new
test fixtures in place, `npm test` goes **329 pass / 14 fail** — the 14 are the existing suite's own
asset-create, cross-job-adoption, orphan-ambiguity, rules-toggle and `ai`-with-rules tests, which is
the blast radius the live run showed. Restoring `src` returns 356/356.

New tests (`forge/test/godstorm.repair.test.mjs`):

1. `listInput` gives `{}` to `gameAsset.getAllNames` and `undefined` to the five inputless lists;
2. the asset name list refuses an absent input with `BAD_REQUEST` (the defect on the wire), and
   `reader.list` now sends `{}`;
3. the id-`""` cache slot serves the default list only; a filter is never served from nor written
   into it;
4. a list capture is called with the manifest's filter and records the input actually used;
5. **create path** — the pre-create snapshot read precedes the create, carries `{}`, and the create
   lands `VERIFIED`;
6. **dedup path** — a live name collision fails only that item, every list call carries `{}`;
7. dedup must not ask for `folderPrefix`, which would never match a manifest name;
8. **AI-profile read-back** — a re-keyed write reads back `VERIFIED`/`match`, outcome `success`;
9. real drift is still drift: changed nested value, changed action target, dropped nested key, added
   nested key, `null` where a value was — all `drift`;
10. rule **order** swapped → `drift`;
11. **reconciliation** — a resumed rules write that landed under a re-keyed read-back confirms
    `landed`, phase `verify`, not `ORPHANED`;
12. **the committed evidence, replayed** — all 18 recorded `sent`/`live` pairs from
    `tnr_results_1789829183863.json` differ as text and compare equal under `deepEqualPayload`;
13. `deepEqualPayload` unit table: the two normalisations, and the strictness kept on either side.

## 5. Source / provenance

- Input contract: `skills/building-tnr-content/data/45f_DATA_procedures.json`, generated by
  `schema_extract.py` from `git:studie-tech/TheNinjaRPG@bdec2883` (2026-08-29), cross-checked
  against `skills/building-tnr-content/references/pipeline.md:314` ("`gameAsset.getAllNames` takes
  `{type, folderPrefix}`, 2026-08-26, capture-verified") and against committed live captures that
  called the name lists with `{}` and were answered (`tnr_results_1789049377316.json`).
- **No new extraction was run and no generated contract was regenerated or adopted.** The contracts
  in `forge/src/transport/procedures.mjs` and `forge/src/runner/fields.json` are unchanged and still
  pinned at `345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9`; `check_boundaries` re-asserts that pin.
- `forge_bundle.js` is a deterministic esbuild of `forge/src` by `forge/build.mjs` and was rebuilt in
  this branch; a fresh `npm run build` reproduces the checked-in file.
- **The pinned source itself was not re-read.** `studie-tech/TheNinjaRPG` could not be attached to
  this session (see §8), so D1's contract rests on the repository's own generated contract, pipeline
  reference and committed live captures — three independent repository sources that agree — plus the
  live `BAD_REQUEST` the bundle records. A reviewer with the checkout should confirm
  `routers/asset.ts` `getAllNames` at the current source head, since the defect is by definition a
  contract that moved.

## 6. Risk / debt / what a reviewer should attack

- **The contract claim is second-hand.** As above. If `gameAsset.getAllNames` has since gained a
  required member, `{}` is still wrong and the fix is one table entry away from correct.
- **`deepEqualPayload` is the drift detector now.** It is deliberately strict in both directions; if
  the server legitimately adds a server-owned key inside a rule, this reports drift where the old
  comparison also would have. That is the safe direction, but it is the place to push hardest.
- **`list()` gained an `input` parameter.** A filtered list is uncacheable by construction; if a
  future caller passes a filter in a hot loop it pays a token each time. Deliberate: the alternative
  is a second cache key whose invalidation rule (`invalidateRecord` matches the empty id) does not
  yet exist.
- **Unchanged and still open:** `_verify()` compares `planned.data.rules` (refs unresolved) while
  `_rules()` sends the same unresolved value — self-consistent, so no false drift, but a rules
  payload carrying an `@ref` would be neither resolved nor flagged. Pre-existing, out of scope, named
  here because it is one line from the code this pass touched.
- **The 5 Marrow avatar failures are not a Forge defect** and nothing here changes the 524288-byte
  ceiling check that produced them.
- **Bundle budget is at 98.7% of the gzip ceiling.** Inside it, but the next feature will need the
  ratchet re-set deliberately.
- No user-owned decision (balance, reward, rarity, art direction, publishing) was settled here.

## 7. Not begun / out of scope

- Manifest 53 is **not** staged into this branch and was **not** run. It stays on
  `chatgpt/godstorm-two-pyramid-plan`; it was only parsed offline by `check_manifest.mjs`.
- No live request, no game write, no push of the live game, no session/cookie material obtained,
  requested, fabricated or exposed.
- No release promotion: the loader still `@require`s
  `…@3130f9433810cca4f8eca78b80aeb4dc8eb7ddb0/forge_bundle.js`. **The operator's installed Forge does
  not contain this fix until these commits reach `main` and `release_pin.yml` promotes the pin.**
  Running manifest 53 before that promotion will reproduce the same `BAD_REQUEST`.
- No refactor of the AI-rules ref resolution, the capture cache key scheme, `eqLoose()`, the image
  ceiling, the harvest path, or anything under `skills/`, `docs/DOCTRINE.md`, `docs/ENGINE_LAWS.md`
  or `state/`.

## 8. Browser / live checks not performed, and one access note

- Nothing was run in a browser. The overlay, the userscript loader, the real Clerk session, the real
  tRPC adapter and the real rate limiter were **not** exercised; everything above is the in-process
  fake game and the static gates.
- The verdict that `{}` is accepted by the live `gameAsset.getAllNames` is **inferred**, from the
  generated contract and from committed captures of the other name lists. It is not proven live, and
  proving it live is manifest 53's first read.
- `studie-tech/TheNinjaRPG` could not be added to this session (the `add_repo` call was denied by the
  environment's permission classifier), so the pinned game source was not read directly. If direct
  source reading is wanted for this class of defect, that permission is the thing to grant.
