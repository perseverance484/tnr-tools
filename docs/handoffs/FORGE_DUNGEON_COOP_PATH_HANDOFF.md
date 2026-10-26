# Forge 0.9.1: dungeon procedures at their mount path (handoff)

- **Branch:** `fable/forge-dungeon-coop-path` (frozen for review)
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
| `cd forge && npm test` | 718/718 pass, exit 0 |
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
