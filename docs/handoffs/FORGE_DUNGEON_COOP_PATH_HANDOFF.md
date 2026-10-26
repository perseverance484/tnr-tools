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
