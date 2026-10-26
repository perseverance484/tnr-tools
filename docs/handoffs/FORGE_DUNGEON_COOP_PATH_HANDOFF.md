# Forge 0.9.1: dungeon procedures at their mount path (handoff)

- **Branch:** `fable/forge-dungeon-coop-path` (frozen for review). **Superseded by the correction handoff at the end of this file.**
- **Base:** `a10d8be4ca5eb24da6778dfcec3bc905ab077a98` (main) **Head (audit target):** `c45fbb9399b5728b3471cbc3b3901101b23f7f2e`
- **Game source pin:** studie-tech/theninjarpg@107d7a86894f806a4c9cec89effef5992118a0ed (read only, never run)
- **Live requests made by Claude:** 0. Credentials: none.

## Why

The director ran push/263 on Forge 0.9.0. The job paused before any write:
`dedupNames: dungeon.getAll failed: NOT_FOUND No procedure found on path "dungeon.getAll"`. At the pin, `root.ts` mounts
`coopRouter` at `coop` and `routers/coop.ts` mounts `dungeonRouter` at `dungeon`, so the real paths are
`coop.dungeon.getAll` and `coop.dungeon.save`. The 0.9.0 extractor read only `routers/dungeon.ts` and named the
procedures after the file; the fake game accepted the same wrong path, so no test could see it.

## What changed

- `forge/tools/derive_dungeon.mjs`: pins `app/src/server/api/root.ts` and `app/src/server/api/routers/coop.ts`; asserts
  exactly one `import { coopRouter }` + `coop: coopRouter,` in root, no `dungeonRouter` in root, exactly one
  `import { dungeonRouter }` + `dungeon: dungeonRouter,` in coop; procedures keyed `coop.dungeon.getAll/save`.
- `forge/src/dungeon/contract.json`: regenerated (two more source hashes, renamed procedure keys).
- `forge/src/{budget,dungeon,reconcile,runner}/*`: every path string and message uses `coop.dungeon.*`.
- `forge/test/fakegame.mjs`: routes `coop.dungeon.*`; a bare `dungeon.*` path answers NOT_FOUND like the server.
- `forge/test/dungeon.review.test.mjs`: new test for the mount chain plus three fail-closed mutations.
- Other tests: path strings only.
- `forge/src/main.mjs`: VERSION `forge 0.8.1` -> `forge 0.9.1` (0.9.0 shipped with a stale label: the panel showed 0.8.1).
- `forge/package.json` 0.9.1; `forge_loader_user.js` `@x-release-pending 0.9.1`; `forge_bundle.js` rebuilt.
- `docs/BUILDER_APP_NOTES.md`: mount-path note; procedure names updated.

## Gates (Node 24, `TNR_GAME_CHECKOUT` = a worktree at the pin)

| Command | Result |
|---|---|
| `cd forge && npm test` | ~~718/718 pass, exit 0~~ **Wrong (review correction 2):** against c45fbb93 it is 718 total, 717 pass, 1 fail (the bundle-budget test), exit 1. See the correction below. |
| `node tools/derive_dungeon.mjs <pin> --check` | "dungeon contract current", exit 0 |
| `npm run build` | exit 0; bundle has 6 `coop.dungeon.getAll`, 0 bare `"dungeon.getAll"` |
| `node tools/check_release_pin.mjs` | "release pin ok", exit 0 |
| `node tools/check_bundle_budget.mjs` | **exit 1: raw 435,145 / 435,000, gzip 105,126 / 105,000** |
| `check_manifest.mjs` + `validate.py --strict` on push/263 | 0 problems / exit 0 |

## Known debt / open decisions

- **Bundle budget (director):** main was already at 434,875 / 104,677. The two new source hashes in the bundled contract
  cost most of the +270 raw. Options: raise the budget to 436,000 / 105,500, or drop `_meta.sources` from the bundled
  contract (a build change, not done).
- Other Forge recipes were checked: every other contract path's first segment is mounted directly in `root.ts`
  (contentReview, skillTree and the 31 audited paths); only the dungeon router is nested.
- `fable/forge-suggest-create@92d8103` (0.8.2, unmerged) needs to rebase onto this and take the next version number.

## Not performed

No browser, live or session checks. The fix to the live path is shown by source and by the live error text, and has not
been observed working. Not begun: merge, release promotion, any re-run of push/263.

---

# Correction handoff (review of c45fbb93: APPROVE WITH FIXES)

**Superseded by correction 2 below.** After the later rebase, the SHAs here map to: `7253f9b9` -> `9df2ace9`,
`15ba0b9b` -> `4b965a97`; the reviewed tip `59ae551c` -> `e9fe2563`. Content is unchanged by the rebase.

```text
Repository: perseverance484/tnr-tools
Branch: fable/forge-dungeon-coop-path
Base: main @ 7ba661b83ba4a6ef417c7cb9942ea1547ba55dc5 (rebased; was a10d8be4)
Code head: 15ba0b9b9158b89baabb6a75b5f7bcb782dd9ced
Head: the tip of this branch = the commit that updates this file; its only parent is the code
      head and it changes only this file. FROZEN until re-review returns.
Integration target: main @ 7ba661b8 (re-verify at integration)
Game pin: studie-tech/theninjarpg@107d7a86894f806a4c9cec89effef5992118a0ed (read only, never run)
```

Commits on the branch: `7253f9b9` is c45fbb93 rebased onto main. Main gained only docs, content and
results commits since a10d8be4. Then `15ba0b9b` is the corrections, and the tip commit updates this
handoff. `git diff --quiet c45fbb93 HEAD -- forge/src forge_bundle.js forge_loader_user.js
docs/BUILDER_APP_NOTES.md` exits 0. The branch was rebased twice during the correction, first onto
e61ab0dd and then onto 7ba661b8, so that main's RUL-2026-10-25-010 and this branch's RUL-2026-10-26-001
sit in date order instead of conflicting at the end of RULINGS.md. The 15ba0b9b commit message still
names e61ab0dd from the first rebase. All gates below were re-run on the final tree.

## Findings

| # | Finding | Outcome | Files |
|---|---|---|---|
| 1 | Mount guards counted lines, so additional aliases and spreads passed | **Fixed** | `forge/tools/derive_dungeon.mjs`, `forge/test/dungeon.review.test.mjs` |
| 2 | Handoff claimed 718/718; the frozen head failed the budget test | **Corrected** (row above struck; results below) | this file |
| 3 | Bundle over budget by 145 raw / 126 gzip | **Director ruled:** raise to 436,000 / 105,500 (RUL-2026-10-26-001); trimming `_meta.sources` offered and declined | `forge/tools/check_bundle_budget.mjs`, `docs/RULINGS.md` |

**1, mount extraction.** `routerMounts(src, name, dir, where)` reads the whole
`export const NAME = createTRPCRouter({ ... });` object, for `appRouter` in root.ts and `coopRouter` in
coop.ts. It accepts only `  key: importedIdentifier,` lines and resolves each identifier through a
single-line named import to a repository path. It fails closed on:
- a spread, or a computed, quoted or shorthand key;
- an inline router, or a trailing comment;
- a duplicate key, or one router bound under two keys;
- a binding with no named import, or an aliased import;
- a second `createTRPCRouter(` call, or `mergeRouters`.

`mountChain()` then requires:
- exactly one root mount of `routers/coop`, bound as `coopRouter`;
- no `dungeonRouter` reference or `routers/dungeon` import in root.ts;
- exactly one coop.ts mount of `routers/dungeon`, bound as `dungeonRouter`;
- exactly one `export const dungeonRouter = createTRPCRouter({` in dungeon.ts.

The prefix is derived as `<root key>.<coop key>`, and the contract's `_meta.scope` string uses it.
At the pin the contract is byte-identical (`--check` current), so no runtime source or bundle byte
changed. A renamed link no longer matches a hard-coded text line: it changes the derived path, which
`derive_dungeon.mjs --check` then reports as a contract difference. The test asserts the derived path
for both renames.

New negative cases, 23 in total:
- additional root and coop aliases (`party: coopRouter`, `dungeons: dungeonRouter`);
- identical duplicate lines in both files, and a duplicate key bound to another router;
- spreads in both files;
- computed members in both files, a quoted key, shorthand, and a trailing comment;
- an inline router, a second router in coop.ts, and `mergeRouters`;
- an unimported binding, an aliased import, and a renamed binding;
- coop mount removed, and dungeon router imported from another file;
- dungeon also mounted or imported at the root;
- dungeon.ts exporting a different router.

With c45fbb93's extractor swapped back in, both new tests fail ("Missing expected exception:
additional root alias"). With the corrected one, all 32 tests in that file pass.

## Verification (Node v24.22.1; full history; `TNR_GAME_CHECKOUT` = a complete depth-1 checkout of 107d7a86, `git status --porcelain` empty)

Each command run separately; exit codes read directly with `$?`, nothing piped through a gate.

| Command | Result |
|---|---|
| `npm ci` | exit 0 |
| `TNR_GAME_CHECKOUT=<pin checkout> npm test` | **exit 0; 719 total, 719 pass, 0 fail, 0 skipped** |
| `npm test` (no checkout, for reference) | exit 0; 719 total, 712 pass, 0 fail, 7 skipped (the pin-checkout tests) |
| `node tools/derive_dungeon.mjs <pin checkout> --check` | exit 0, "dungeon contract current" |
| `npm run build` | exit 0 |
| `git diff --quiet -- ../forge_bundle.js` | exit 0 |
| `node tools/check_release_pin.mjs` | exit 0, "release pin ok" |
| `node tools/check_bundle_budget.mjs` | exit 0; raw 435,145 / 436,000, gzip 105,126 / 105,500 |
| `npm run fixtures` + `git diff --exit-code -- test/fixtures/envelope test/fixtures/screens` | exit 0 / exit 0 |
| `node tools/check_imports.mjs`, `node tools/check_boundaries.mjs` | 0 violations each, exit 0 |
| `npm audit --omit=dev --audit-level=high` | exit 0 |
| bare `"dungeon.getAll"` / `"dungeon.save"` strings in `forge_bundle.js` | 0 |

## Scope and risk

- The architecture is unchanged. The corrections touch the extractor tool, one test file, the budget
  constant and one ruling. `forge/src`, `forge_bundle.js` and the loader are byte-identical to c45fbb93.
  A narrow re-review (mount extraction and its tests, the budget correction, artifact fidelity) should
  be safe; that's the reviewer's call.
- Headroom after the raise is 855 raw / 374 gzip.
- **Version collision to resolve at integration:** `fable/validate-stale-rules@271d1103` (frozen,
  separate review) also stages Forge 0.9.1 on main @ 6d4de246. It adds about 95 raw bytes, which fits
  under the new ceiling. Whichever branch integrates second must rebase and take 0.9.2.
  `fable/forge-suggest-create@92d8103` (0.8.2) also still needs to rebase and take the next number.
- Not performed: browser, live or session checks. The live path is shown by source and by the
  2026-10-25 live error text only. Not begun: merge, release promotion, any re-run of push/263.
- Live-game requests: 0. Game writes: 0. Credentials or session material: none. Game source fetched
  from GitHub and read only; nothing in it was executed.

## Copy-ready re-review prompt

~~~text
You are the independent reviewer for a Lane A correction in perseverance484/tnr-tools. Review only; do not
patch the Fable branch. Follow docs/workflows/FABLE_REVIEW.md.

TARGET
- Branch: fable/forge-dungeon-coop-path, tip = the commit that updates
  docs/handoffs/FORGE_DUNGEON_COOP_PATH_HANDOFF.md; its parent is the code head
  15ba0b9b9158b89baabb6a75b5f7bcb782dd9ced. Verify both SHAs first; if the branch moved, stop and report.
- Previous review target: c45fbb9399b5728b3471cbc3b3901101b23f7f2e (APPROVE WITH FIXES).
- Base: main @ 7ba661b83ba4a6ef417c7cb9942ea1547ba55dc5 (the branch was rebased; 7253f9b9 is c45fbb93
  rebased, with forge/, the bundle and the loader unchanged).
- Handoff: the "Correction handoff" section of docs/handoffs/FORGE_DUNGEON_COOP_PATH_HANDOFF.md.
- Game pin: studie-tech/theninjarpg@107d7a86894f806a4c9cec89effef5992118a0ed (read only, never run).
SAFETY: zero live-game requests, no credentials or session material.

CHECK
1. forge/tools/derive_dungeon.mjs routerMounts/mountOf/mountChain: is any binding form still accepted
   that could add, rename or override the coop or dungeon mount (multi-line imports, default imports,
   re-exports, later mutation of appRouter, anything else)? Is the derived path exactly
   <root key>.<coop key> from the validated objects?
2. forge/test/dungeon.review.test.mjs: the derived-path test and the 23 negative cases. Do they fail
   against c45fbb93's extractor and pass now?
3. Budget: BUDGET is 436,000 / 105,500 with RUL-2026-10-26-001 recorded in docs/RULINGS.md; measured
   435,145 / 105,126.
4. Artifact fidelity: forge/src, forge_bundle.js and forge_loader_user.js are byte-identical to c45fbb93;
   the contract is current at the pin.
Reproduce, separately, recording every exit code (no masking pipes), with a complete checkout at the pin:
  cd forge
  TNR_GAME_CHECKOUT=/path/to/pinned-checkout npm test
  node tools/derive_dungeon.mjs /path/to/pinned-checkout --check
  npm run build
  git diff --quiet -- ../forge_bundle.js
  node tools/check_release_pin.mjs
  node tools/check_bundle_budget.mjs

REPORT: per finding severity (blocker / should-fix / note), file:line, reproduction, suggested fix; what
you checked and found clean. Verdict: approve, approve with fixes, or reject.
~~~

---

# Correction 2 handoff (re-review of 59ae551c: APPROVE WITH FIXES)

**Superseded by correction 3 below.** Its tip 3f8e9fcb is unchanged history on this branch (no rebase this round).

```text
Repository: perseverance484/tnr-tools
Branch: fable/forge-dungeon-coop-path
Base: main @ a6bba6176e60a35c38ab84b0f21555db94470106 (rebased; was 7ba661b8)
Code head: 9ff2322e1b9ec883ecc784f60d922f289eadb1dc
Head: the tip of this branch = the commit that updates this file; its only parent is the code
      head and it changes only this file. FROZEN until re-review returns.
Integration target: main @ a6bba617 (re-verify at integration)
Game pin: studie-tech/theninjarpg@107d7a86894f806a4c9cec89effef5992118a0ed (read only, never run)
```

The branch was rebased onto a6bba617 because main had appended RUL-2026-10-25-011 to -014, which
conflicted with this branch's RUL-2026-10-26-001 at the end of `docs/RULINGS.md`. The resolution keeps
every ruling, in date order. Main's commits since 7ba661b8 touch no Forge file. Commits after the
rebase:
- `9df2ace9`: the original fix (was c45fbb93);
- `4b965a97`: correction 1;
- `e9fe2563`: the correction 1 handoff (was the reviewed tip 59ae551c);
- `9ff2322e`: correction 2;
- the tip: this section.

The diff from 59ae551c to the code head is limited to `forge/tools/derive_dungeon.mjs`,
`forge/test/dungeon.review.test.mjs` and `docs/RULINGS.md` (rebase merge only).

## Findings

| # | Finding | Outcome |
|---|---|---|
| 1 | Import validation kept source and local name but dropped the imported symbol (alias over a re-export; a named import inside a block comment plus an active default import) | **Fixed** |
| 2 | Statements after the router literal (`delete`, `Object.assign`) were ignored | **Fixed** |

Both fixes come from one narrow grammar in `forge/tools/derive_dungeon.mjs` `routerMounts()`.

`stripComments()` removes line and block comments and keeps string literals, so comments never count
as imports or mounts. A comment opener inside a regex literal could be misread, but the text left
before it can never form an accepted statement, so a misread fails closed.

After that, root.ts and coop.ts may contain only:
- `import { A, B, type C } from "path";`: plain named imports. Aliases (`x as y`), default, namespace,
  `import type` and mixed default+named imports are refused.
- exactly one `export const NAME = createTRPCRouter({ key: importedRouter, ... });`, where each member is
  `key: identifier` and the identifier is a plain named import;
- for root.ts only, the pin's two read-only exports (`CDN_CACHED_QUERY_PATHS` and
  `export type AppRouter = typeof appRouter;`), matched token for token.

Any other statement is refused ("unsupported statement ..."). That covers `delete`, `Object.assign`,
assignments to `_def`, export lists, default exports, statements before or after the literal, and a
read-only export with altered code.

Symbol identity is checked link by link:
- root.ts imports the plain name `coopRouter` from `routers/coop`. Under the same grammar, coop.ts's
  only export is `export const coopRouter`.
- coop.ts imports the plain name `dungeonRouter` from `routers/dungeon`. dungeon.ts is checked on its
  raw text, so a comment can only make the check fail: `dungeonRouter` must appear exactly once, as
  `export const dungeonRouter = createTRPCRouter({`, and the file may have no export list, re-export
  or default export.

The contract is byte-identical at the pin. No runtime source, bundle or loader byte changed.

## Regression evidence

The reviewer's four reproductions, applied to scratch copies of the pinned sources:

| Reproduction | 15ba0b9b extractor | Corrected extractor |
|---|---|---|
| `import { alternateRouter as coopRouter }` + coop.ts `export { questPartyRouter as alternateRouter };` | accepted, emits coop.dungeon.* | refused: `unsupported import "alternateRouter as coopRouter"` |
| named import inside a multi-line block comment + active `import coopRouter from "./routers/coop";` + coop.ts default export | accepted, emits coop.dungeon.* | refused: `unsupported statement "import coopRouter from ..."` |
| `delete appRouter._def.procedures["coop.dungeon.save"];` appended | accepted | refused: `unsupported statement "delete appRouter..."` |
| `Object.assign(appRouter._def.procedures, { "coop.dungeon.save": itemRouter._def.procedures.create });` appended | accepted | refused: `unsupported statement "Object.assign..."` |

`forge/test/dungeon.review.test.mjs` gains the test "review C2: imports keep symbol identity, comments
are ignored, and post-construction statements are refused". It has one positive case: mounts with
line and block comments around and inside both router literals still derive coop.dungeon.*. It has
18 negative cases:
- the four reproductions above, two of them also split so each file is tested alone;
- a commented-out mount;
- namespace, type-only and mixed default+named imports;
- assigning a procedure, and a mutation before the router;
- an altered read-only export, and a read-only export added to coop.ts;
- a mutation in coop.ts;
- dungeon.ts no longer defining the name, an export list in dungeon.ts, and a post-definition
  `delete dungeonRouter...` in dungeon.ts.

The earlier C1 cases were adjusted for comment stripping:
- a trailing comment is now a positive case;
- the alias case now expects "unsupported import" (it previously only left the local name unbound,
  as the reviewer noted);
- two spread messages were updated.

## Verification (Node v24.22.1; full history; `TNR_GAME_CHECKOUT` = complete checkout of 107d7a86, `git status --porcelain` empty)

Each command run separately; exit codes read directly with `$?`, nothing piped through a gate.

| Command | Result |
|---|---|
| `TNR_GAME_CHECKOUT=<pin checkout> npm test` | **exit 0; 720 total, 720 pass, 0 fail, 0 skipped** |
| `npm test` (no checkout, for reference) | exit 0; 720 total, 712 pass, 0 fail, 8 skipped (the pin-checkout tests) |
| `node tools/derive_dungeon.mjs <pin checkout> --check` | exit 0, "dungeon contract current" |
| `npm run build` | exit 0 |
| `git diff --quiet -- ../forge_bundle.js` | exit 0 |
| `node tools/check_release_pin.mjs` | exit 0, "release pin ok" |
| `node tools/check_bundle_budget.mjs` | exit 0; raw 435,145 / 436,000, gzip 105,126 / 105,500 |
| `npm run fixtures` + `git diff --exit-code -- test/fixtures/envelope test/fixtures/screens` | exit 0 / exit 0 |
| `node tools/check_imports.mjs`, `node tools/check_boundaries.mjs` | 0 violations each |
| `npm audit --omit=dev --audit-level=high` | exit 0 |
| `git diff --quiet c45fbb93 HEAD -- forge/src forge_bundle.js forge_loader_user.js docs/BUILDER_APP_NOTES.md` | exit 0 (runtime byte-identical to the first review target) |

## Scope, residual boundary and risk

- The scope is the extractor binding and statement grammar, its tests and this handoff. Runtime
  source and architecture are unchanged.
- **Residual boundary:** the grammar covers the three pinned mount files only. A module outside them
  that imports `appRouter` and mutates it at load time is not read. The exact-pin and dirty-source
  CLI checks, and the source hashes in `_meta.sources`, still bind the artifact to the pin.
  Procedures inside `dungeonRouter` are read by the existing `procedureFacts()`, which this change
  does not touch.
- The version collision noted in correction 1 still stands: `fable/validate-stale-rules@271d1103` also
  stages 0.9.1, and whichever branch integrates second takes 0.9.2.
- Not performed: browser, live or session checks.
- Live-game requests: 0. Game writes: 0. Credentials or session material: none. The game source was
  read only, and nothing in it was executed.

## Copy-ready re-review prompt

~~~text
You are the independent reviewer for a Lane A correction in perseverance484/tnr-tools. Review only; do not
patch the Fable branch. Follow docs/workflows/FABLE_REVIEW.md.

TARGET
- Branch: fable/forge-dungeon-coop-path, tip = the commit that adds the "Correction 2 handoff" section to
  docs/handoffs/FORGE_DUNGEON_COOP_PATH_HANDOFF.md; its parent is the code head 9ff2322e1b9ec883ecc784f60d922f289eadb1dc (verify
  with git log). If the branch moved, stop and report.
- Previous review target: 59ae551ca88c88a5ecd5407bd684aee778e65354 (APPROVE WITH FIXES); after the rebase
  its content is e9fe2563.
- Base: main @ a6bba6176e60a35c38ab84b0f21555db94470106.
- Game pin: studie-tech/theninjarpg@107d7a86894f806a4c9cec89effef5992118a0ed (read only, never run).
SAFETY: zero live-game requests, no credentials or session material.

CHECK (narrow: extractor binding/statement validation, regression tests, handoff evidence)
1. forge/tools/derive_dungeon.mjs stripComments/statement/ROOT_READ_ONLY/routerMounts/mountChain: can any
   import, export or statement form still rebind, add, remove or override the coop or dungeon mount, or a
   procedure under it, in root.ts, coop.ts or dungeon.ts, and still derive coop.dungeon.*?
2. Your four reproductions are refused; the "review C2" test's cases are valid (each edit applies to text
   present once at the pin) and fail for the stated reason.
3. Runtime fidelity: forge/src, forge_bundle.js and forge_loader_user.js byte-identical to c45fbb93;
   contract current at the pin; RULINGS.md rebase resolution keeps every ruling.
Reproduce, separately, recording every exit code (no masking pipes), with a complete checkout at the pin:
  cd forge
  TNR_GAME_CHECKOUT=/path/to/pinned-checkout npm test
  node tools/derive_dungeon.mjs /path/to/pinned-checkout --check
  npm run build
  git diff --quiet -- ../forge_bundle.js
  node tools/check_release_pin.mjs
  node tools/check_bundle_budget.mjs

REPORT: per finding severity (blocker / should-fix / note), file:line, reproduction, suggested fix; what
you checked and found clean. Verdict: approve, approve with fixes, or reject.
~~~

---

# Correction 3 handoff (re-review of 3f8e9fcb: APPROVE WITH FIXES)

```text
Repository: perseverance484/tnr-tools
Branch: fable/forge-dungeon-coop-path
Base: main @ a6bba6176e60a35c38ab84b0f21555db94470106 (unchanged; not rebased this round)
Code head: e28bb20d288e0df6fa348cf023f26ea7411828e1
Head: the tip of this branch = the commit that updates this file; its only parent is the code
      head and it changes only this file. FROZEN until re-review returns.
Previous target: 3f8e9fcbbee19e9db12ebbc5a6ad4e46e5e7e8e5 (its ancestor; history not rewritten)
Integration target: main @ 7fd8c6e825f13cd0e54e418aa620a676afca621c, checked at handoff:
      git merge-tree exits 0 and main touches no Forge file since a6bba617
Game pin: studie-tech/theninjarpg@107d7a86894f806a4c9cec89effef5992118a0ed (read only, never run)
```

`git diff --name-only 3f8e9fcb <code head>` lists only `forge/tools/derive_dungeon.mjs` and
`forge/test/dungeon.review.test.mjs`.

## Finding

| # | Finding | Outcome |
|---|---|---|
| 1 | dungeon.ts was checked textually: `}).save;` exported a procedure instead of the router, and `delete dungeonRouter._def.record["save"];` named the router through an escaped identifier the word count missed | **Fixed** |

`dungeonExport()` in `forge/tools/derive_dungeon.mjs` is called from `mountChain()`. dungeon.ts is
too large for the whole-file grammar, so it is held to the shape it has at the pin:
- **Complete initializer, last statement.** On comment-free code, the bracket opened by
  `createTRPCRouter(` is matched, skipping string literals. The closing must be `})`, then `;`, then
  only whitespace or comments to the end of the file. This refuses `}).save;`, a trailing call or
  cast, and any statement after the declaration. At the pin the literal does close the file
  (`...\n});\n`).
- **No escapes.** Any `\u` or `\x` in the raw text is refused, so no identifier can be spelled other
  than literally. The pin has none. The raw count of `dungeonRouter` (exactly one, its definition)
  is kept, so a named reference after the declaration fails as well.
- **No indirect reach.** These are refused on comment-free code: `eval`, `Function`, `globalThis`,
  `setTimeout` / `setInterval` / `setImmediate` / `queueMicrotask`, dynamic `import(`, a self-import,
  export lists, re-exports, default exports, and a second `createTRPCRouter(`. The pin uses none of
  them. A timer or microtask is the way code written before the declaration could run after it.

## Regression evidence

The reviewer's two reproductions, applied to scratch copies of the pinned sources:

| Reproduction | 9ff2322e extractor | Corrected extractor |
|---|---|---|
| final `});` -> `}).save;` | accepted, emits coop.dungeon.* | refused: `the dungeonRouter initializer must be exactly createTRPCRouter({ ... }); as the last statement, found ".save;"` |
| append `delete dungeonRouter._def.record["save"];` | accepted, emits coop.dungeon.* | refused: `\u/\x escapes are not read` |

`forge/test/dungeon.review.test.mjs` gains the test "review C3: dungeon.ts must export the complete
router literal as its last statement, with no escaped or indirect reference". It has 16 negative cases:
- both reproductions, plus a braced `\u{52}` escape;
- a trailing `.lazy()` call, a trailing cast, a missing semicolon followed by a statement, a
  statement after the router, and a named mutation after the router;
- `eval` via `queueMicrotask`, `globalThis`, `setTimeout`, `Function`, dynamic `import(`, a
  self-import, an export list, and a second router construction.

It also has one positive case: comments after the literal still derive coop.dungeon.*.

## Verification (Node v24.22.1; full history; `TNR_GAME_CHECKOUT` = complete checkout of 107d7a86, `git status --porcelain` empty)

Each command run separately; exit codes read directly with `$?`, nothing piped through a gate.

| Command | Result |
|---|---|
| `TNR_GAME_CHECKOUT=<pin checkout> npm test` | **exit 0; 721 total, 721 pass, 0 fail, 0 skipped** |
| `npm test` (no checkout, for reference) | exit 0; 721 total, 712 pass, 0 fail, 9 skipped (the pin-checkout tests) |
| `node tools/derive_dungeon.mjs <pin checkout> --check` | exit 0, "dungeon contract current" |
| `npm run build` | exit 0 |
| `git diff --quiet -- ../forge_bundle.js` | exit 0 |
| `node tools/check_release_pin.mjs` | exit 0, "release pin ok" |
| `node tools/check_bundle_budget.mjs` | exit 0; raw 435,145 / 436,000, gzip 105,126 / 105,500 |
| `npm run fixtures` + `git diff --exit-code -- test/fixtures/envelope test/fixtures/screens` | exit 0 / exit 0 |
| `node tools/check_imports.mjs`, `node tools/check_boundaries.mjs` | 0 violations each |
| `npm audit --omit=dev --audit-level=high` | exit 0 |
| `git diff --quiet c45fbb93 HEAD -- forge/src forge_bundle.js forge_loader_user.js docs/BUILDER_APP_NOTES.md` | exit 0 (runtime byte-identical to the first review target) |

## Scope, residual boundary and risk

- The scope is dungeon.ts export and reference validation, its regression tests and this handoff.
  Runtime source and architecture are unchanged.
- **Residual boundary:** this is a shape check, not a JavaScript parser. The bracket matcher skips
  string and template literals whole, so a template whose `${...}` holds its own backtick, or a regex
  literal containing a quote or bracket, can mis-scan. ~~A mis-scan is unbalanced or leaves text after
  the close, so it fails closed.~~ **Withdrawn (re-review of 3feea971): false.** A regex literal with a
  quote can hide a trailing `.save` export and a following statement; see "Integration disposition"
  below. Code inside the router literal (procedure bodies, which run at
  request time) is not modelled. The procedure keys and kinds are still read by `procedureFacts()`.
  Mutations from modules outside the three mount files remain out of scope, as recorded in
  correction 2. The exact-pin and dirty-source CLI checks and `_meta.sources` hashes bind the
  artifact to the pin.
- Integration: the Forge 0.9.1 version collision with `fable/validate-stale-rules@271d1103` stands.
  Whichever branch integrates second takes 0.9.2.
- Not performed: browser, live or session checks.
- Live-game requests: 0. Game writes: 0. Credentials or session material: none. The game source was
  read only, and nothing in it was executed.

## Copy-ready re-review prompt

~~~text
You are the independent reviewer for a Lane A correction in perseverance484/tnr-tools. Review only; do not
patch the Fable branch. Follow docs/workflows/FABLE_REVIEW.md.

TARGET
- Branch: fable/forge-dungeon-coop-path, tip = the commit that adds the "Correction 3 handoff" section to
  docs/handoffs/FORGE_DUNGEON_COOP_PATH_HANDOFF.md; its parent is the code head
  e28bb20d288e0df6fa348cf023f26ea7411828e1. If the branch moved, stop and report.
- Previous review target: 3f8e9fcbbee19e9db12ebbc5a6ad4e46e5e7e8e5 (APPROVE WITH FIXES), an ancestor.
- Base: main @ a6bba6176e60a35c38ab84b0f21555db94470106.
- Game pin: studie-tech/theninjarpg@107d7a86894f806a4c9cec89effef5992118a0ed (read only, never run).
SAFETY: zero live-game requests, no credentials or session material.

CHECK (narrow: dungeon.ts export/reference validation, regression tests, handoff evidence)
1. forge/tools/derive_dungeon.mjs dungeonExport() and closing(): can dungeon.ts still export something
   other than the complete createTRPCRouter({ ... }) value, or reach/mutate the router after construction
   (by name, escape, or indirection), and still derive coop.dungeon.*?
2. Your two reproductions are refused; the "review C3" cases apply to the pinned text and fail for the
   stated reason; the comments-after case derives.
3. Runtime fidelity: forge/src, forge_bundle.js, forge_loader_user.js byte-identical to c45fbb93; the
   contract is current at the pin.
Reproduce, separately, recording every exit code (no masking pipes), with a complete checkout at the pin:
  cd forge
  TNR_GAME_CHECKOUT=/path/to/pinned-checkout npm test
  node tools/derive_dungeon.mjs /path/to/pinned-checkout --check
  npm run build
  git diff --quiet -- ../forge_bundle.js
  node tools/check_release_pin.mjs
  node tools/check_bundle_budget.mjs

REPORT: per finding severity (blocker / should-fix / note), file:line, reproduction, suggested fix; what
you checked and found clean. Verdict: approve, approve with fixes, or reject.
~~~

---

# Integration disposition (re-review of 3feea971: APPROVE WITH FIXES)

The review approved `3feea9715cc6c703c2f6406daa0ddfa6bac2125b` (code head `e28bb20d`), with integration
conditional on two open extractor findings:
1. `dungeonExport()` accepts an empty-object substitution for the router argument, e.g.
   `createTRPCRouter({ ... } && {});`, and still derives coop.dungeon.*. Reproduced by Fable at the
   reviewed head: accepted.
2. Regex-literal mis-scanning can hide a trailing `.save` export and a following statement. The
   "fails closed" claim above was false and is withdrawn.

**Disposition:** the director accepted both residual risks and directed integration
(**RUL-2026-10-26-002**). Neither is a runtime defect, and the extractor runs only at a re-pin. The
open follow-up is to replace the text scanning of the three mount files with a syntax-aware (AST)
check, reviewed as its own change, before the next re-pin. Until then, a person reads the re-pin diff
of those files.

**No code change after review.** The integration candidate is the reviewed head plus:
- a merge of main at the integration boundary, which brings no Forge file;
- this docs-only commit (`docs/RULINGS.md`, this handoff).

**Version:** this branch integrates first and keeps Forge 0.9.1. `fable/validate-stale-rules@271d1103`,
which also stages 0.9.1, must rebase and take 0.9.2.

The merged SHA, released version, bundle pin and final gate results are recorded below.

## Integration record (2026-10-26)

| Item | Value |
|---|---|
| PR | #114, merged with a merge commit at expected head `a70e59c6ea7d6ef3d39b04e8be93f4907f4df97a`; PR CI `gate` and `verify` both succeeded on that head |
| Merged SHA | `b13425b348eafc7235dfd6dd7d819d17c9a26113` |
| Released version | Forge **0.9.1** |
| Loader promotion | `release_pin.yml` run 31 committed `860324a93ab68b392a49990b69332f4fe6e87af7`. `forge_loader_user.js` now has `@version 0.9.1`, no `@x-release-pending` line, and `@require https://raw.githubusercontent.com/perseverance484/tnr-tools/b13425b348eafc7235dfd6dd7d819d17c9a26113/forge_bundle.js` |
| Bundle fidelity | `git diff --quiet 3feea971 b13425b3 -- forge_bundle.js forge` exits 0: the shipped bundle and Forge tree are the reviewed ones. The bundle's sha256 begins `65980fc75caa23a8` |

Final gates on main @ `860324a9` (Node 24.22.1, complete clean checkout at the game pin, each run separately):

| Command | Result |
|---|---|
| `TNR_GAME_CHECKOUT=<pin> npm test` | exit 0; 721 total, 721 pass, 0 fail, 0 skipped |
| `node tools/derive_dungeon.mjs <pin> --check` | exit 0, contract current |
| `npm run build` | exit 0 |
| `git diff --quiet -- ../forge_bundle.js` | exit 0 |
| `node tools/check_release_pin.mjs` | exit 0, "release pin ok" |
| `node tools/check_bundle_budget.mjs` | exit 0; raw 435,145 / 436,000, gzip 105,126 / 105,500 |

**Still open:**
- The RUL-2026-10-26-002 follow-up: an AST-based check of the mount files before the next re-pin.
- `fable/validate-stale-rules@271d1103` must rebase onto main and take Forge 0.9.2 before its own integration.
- Live acceptance (user-operated, not authorized by this merge): installing 0.9.1, auth/BotID, the
  corrected `coop.dungeon.getAll` / `coop.dungeon.save` requests and read-back. No agent re-ran push/263.

Live-game requests: 0. Credentials or session material: none.

