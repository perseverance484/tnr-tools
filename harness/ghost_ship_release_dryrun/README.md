# Ghost Ship / Skyglass release: headless Forge dry run

`dryrun.mjs` runs push/90 and then push/93 through the shipped ForgeCore and `compose()` wiring, the
same construction Forge's own tests use. It runs against Forge's in-memory FakeGame. No socket opens,
nothing is uploaded, and no game is contacted.

```bash
(cd forge && npm ci --ignore-scripts)    # lockfile-pinned test dependencies (director-approved 2026-10-12)
node harness/ghost_ship_release_dryrun/dryrun.mjs --out <dir>
```

| Substituted | With |
| --- | --- |
| Game | FakeGame, seeded from push/86 (11 AIs, profiles and embedded jutsu), push/89 (both quests) and the October 1 item rows (Serum, Fragment) |
| Synthetic seed (no capture exists) | The Skyglass Crown item shell; the 9 existing scene-asset shells; the post-0056 columns added to FakeGame's AI create placeholder |
| Repository | `git show <imagePack.ref>:<path>`, so the real committed art bytes |
| Uploader | Records name, size and sha256 for each file and returns a fake CDN URL |

FakeGame has no server logic: no zod, no `scaleEditedAi` and no `updateUserContent`. The run proves
Forge's side:
- parse, plan, phase order and ref resolution;
- pre-send validation against live rows, merges, the kit re-send and the rules step;
- image-pack fetch and verification, upload binding, read-back, captures and the results bundle.

## Result (`results/dryrun_report.json`)

27/27 checks pass. Two runs give byte-identical reports. The exported bundle differs only in Forge's
clock-derived job id.

**Defect found and fixed.** The first run failed the Sealwright follow-up edit. Forge's runner
resolves `@refs` in `data` but reads `targetId` literally (`forge/src/runner/runner.mjs:520`), so
`targetId: "@ai:sealwright"` sent `profile.getAi("@ai:sealwright")`. Sealwright would have kept
placeholder offence and defence live. validate.py's lint L01 had flagged it; it was wrongly dismissed.

The edit now lives in **push/93**. `push/93_ghost_ship_sealwright_stats.gen.py` generates it from
push/90's own results bundle, using the literal created id, and refuses any bundle that is not a
DONE/success push/90 at the committed Forge manifest hash. The dry run executes that exact chain.
