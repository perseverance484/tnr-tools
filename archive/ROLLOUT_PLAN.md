> **STALE - archived 2026-08-30. Plan executed and closed.** Stage 0 ruled raw serving
> 2026-08-28; Stages 1-3 (project slim, repo restructure + answer layer, tools canon +
> skillpack) landed 2026-08-28; Stage 4 (mounted session ritual) landed 2026-08-29 and
> acceptance-passed 2026-08-30 (zero-touch round trip, Law 29 carve-out closed).
> Stage 5 (command relay) remains DEFERRED by its own terms - revive from here if ever.
> Do not build from this file.

# ROLLOUT_PLAN.md - Three-axis restructure (tokens / throughput / accuracy)

Staged 2026-08-28 from the architecture research report. Owner of every go/no-go: dauntless.
Each stage lists tasks by owner, an exit benchmark, and a rollback. A stage does not start
until the prior stage's benchmark passes, except where marked parallel-safe.

## Stage 0 - Serving surface decision [DONE 2026-08-28]

Tested in-session:
- `github.com/*/blob/*` - fetchable, ~30-40% HTML chrome overhead. Fallback and chaining index only.
- `github.com/*/raw/*` redirect - BLOCKED (github.com robots disallows `/*/raw/`).
- `raw.githubusercontent.com/*` - **FETCHABLE. Clean text/plain, zero chrome.** Verified against
  a third-party repo; host serves no robots.txt, default-allow.

**Ruling this produces: raw.githubusercontent.com is the primary serving surface.** GitHub Pages
is deferred - it only buys custom robots/headers, and costs a deploy step and ~10 min TTL.
Answers are fetchable the moment they are committed, plus ~5 min raw CDN cache.

Standing constraint that shapes everything below: the fetcher cannot mint URLs. It follows only
URLs already present in the conversation, project instructions, or a previously fetched page.
Therefore `answers/INDEX.md` must list **absolute** raw.githubusercontent.com URLs (relative
links do not resolve), and the INDEX's own raw URL goes into the project instructions so it is
fetchable from turn one of any session.

## Stage 1 - Slim the always-loaded project layer [parallel-safe with Stage 2]

Objective: 12 files / ~101KB -> 3 files / ~30KB. Both byte size AND file count matter: RAG
chunking has been observed to trigger on file count (~13) independent of bytes. Target single
digits with margin.

File map:

| Current | Disposition |
|---|---|
| 00_INDEX.md | KEEP, rewritten: router + task table + non-negotiables, folds in 01_PRECEDENCE |
| 01_PRECEDENCE.md | MERGE into 00_INDEX (small, load-bearing) |
| 11_TECH_source_map.md | MOVE to building skill `references/pipeline.md` (tier rules belong beside capture workflow) |
| 12_TECH_engine_laws.md (41KB) | SPLIT. Cross-cutting knowledge laws stay (~12KB): storage-vs-intent, stacking/calibration 9-13, turn/round/castThisRound 61/75/76, capture-first, name uniqueness 66, editor overwrite 58, blank shell 59. Workflow-scoped laws move beside their workflow: quest rendering 47-53 + placement 54-58 -> quest.md; art 33-35/79-84 -> art skill; AI economy 62-65 -> ai.md; drops 67-69 -> balance.md; write shapes 72-74 -> pipeline.md. Validate-class laws compress to one-line citations (the tool enforces; prose is redundant) |
| 12b_LAWS_coverage.md | MOVE to building skill (audit doc, needed when patching validators, not every session) |
| 32_REGISTRY_shared_ai_pool.md | ARCHIVE to repo. 32b JSON is the working copy (skill data); kit work goes through `calc.py kit` |
| 34_REGISTRY_map_pins.md | ARCHIVE to repo. 34b JSON is the working copy |
| 35 / 36 / 37 (Ashen, shipped) | ARCHIVE to repo `/archive/` |
| 38 / 39 (operative lines) | MOVE to building skill `references/lines.md` (one file, used during mission builds, slow-moving) |

Also in this stage: rewrite the project custom-instructions block. It currently cites retired
files (10_TECH, guides 20-26, 45_DATA_field_schemas.json, builder v4.12). New text: identity,
environment, working style, the layer contract, and the INDEX raw URL.

Tasks:
- [Claude] Draft the 3 replacement files + new project instructions text. Hand over as files.
- [dauntless] Replace project knowledge, paste new instructions.

Exit benchmark: no RAG indicator; a test question answered from a project file returns whole-file
content, not chunks. Rollback: old 12 files archived in repo `/archive/project-2026-08-28/`,
restorable by re-upload.

## Stage 2 - Repo restructure + answer layer

Objective: the repo becomes runtime host + tool canon + archive + fetchable answer layer.

**Task 1, before anything else lands: the privacy sweep.** The real first name is present in the
current public repo (confirmed in 22_GUIDE_item.md). dauntless runs a local grep on the clone,
scrubs every hit to the handle, force-commits. Nothing else commits until this passes.

Target layout:

```
/                      builder runtime (userscript, 45c/45g/32b at root - panel fetches root; unchanged)
/answers/              generated: names_{jutsu,item,ai,asset,quest}.json, ids_all.json, INDEX.md
/skills/building-tnr-content/   canonical skill tree (SKILL.md, scripts/, references/, data/)
/skills/producing-tnr-art/
/harvests/             full dumps, committed by dauntless after a harvester run
/dist/                 packaged skill zips (small; committed for one-tap mobile download)
/archive/              retired docs, each with a STALE banner line at top
/docs/                 this plan, runbooks
/.github/workflows/    answers.yml, scrub.yml, skillpack.yml
```

Workflows (Claude drafts all three, dauntless commits):
1. **answers.yml** - on push to `harvests/**` + manual dispatch: run the extractor (ported from
   `refresh_catalogs.py`), write `/answers/*.json` (name, id, hidden flag per entity) and rebuild
   `INDEX.md` with absolute raw URLs, commit back with `GITHUB_TOKEN`. Loop-safe by design:
   GITHUB_TOKEN pushes do not retrigger workflows.
2. **scrub.yml** - on every push: grep the whole tree for the name string held in Actions secret
   `SCRUB_STRING` (the string itself never appears in the repo); non-zero exit fails the build.
   Proven by seeding a fake hit once and watching it fail.
3. **skillpack.yml** - on push to `skills/**`: zip each skill dir into `/dist/`.

Tasks:
- [dauntless] Privacy sweep; create Actions secret `SCRUB_STRING` (Settings > Secrets, mobile web
  works); install the GitHub Mobile app for manual workflow dispatch (mobile-web dispatch is flaky).
- [Claude] Draft the three workflow files, the extractor port, the layout migration script, the
  STALE banner for each archived doc.
- [dauntless] Commit layout + workflows; push one harvest to prove answers.yml.

Exit benchmark: commit a harvest -> `/answers/names_ai.json` fetchable in-session via raw URL
within ~6 min, clean content; scrub gate fails on a seeded string. Rollback: workflows are
additive; deleting `.github/workflows/` restores the repo to dumb storage.

## Stage 3 - Tools canon + skill rebuild + bundle diet [depends on Stage 2]

Objective: kill the skill-reinstall-reverts-patches failure class and shrink the bundle to
truly volatile state.

Flow becomes one-directional: **repo -> skill zip -> installed skill -> container**. Patches are
committed to `/skills/` first, always; `skillpack.yml` rebuilds `/dist/`; dauntless downloads
and re-uploads the skill. The container copy and the bundle never hold authoritative tools again.

Splits:
- Slow-moving generated JSON (45c/45d/45e/45f/45g, 25x art spec, 26x, 32b, 34b, 40x, 46, 46b, 48)
  -> skill `data/`, so scripts find them on disk after a session-start copy. Repacked only on a
  source drop.
- Live-state lookups (the 4x catalog indexes) -> retired from the bundle entirely; the answer
  layer replaces them and is fresher than any bundle could be.
- Bundle keeps: `state/status.json`, `state/active-context.md`, session captures/results,
  anything newer than the last skill build. Expected size: under 200KB, from ~1.2MB.
- `tools/PATCHES.md` retires. `closeout.py` updated: refuses to bundle a `tools/` dir; emits a
  "skills changed - commit to /skills/ and repack" notice instead.

Tasks:
- [Claude] Produce the canonical skill trees = current skills + every bundle patch merged
  (enemy.py, mission.py, profile_derive.py, validate.py, stack.py, selfcheck.py B1 fix, plus the
  new tools). Update closeout.py. Hand over as one commit-ready folder.
- [dauntless] Commit `/skills/`, download `/dist/` zips, reinstall both skills.

Exit benchmark: fresh skill install passes `selfcheck.py` with all patches present (the B1 guard
wired, profile_derive reads `data`, enemy.py rank logic) - verified by a patch-marker check
script. Rollback: previous skill zips kept in `/dist/` history; one transition bundle keeps a
final `tools/` copy.

## Stage 4 - Session ritual rewire [depends on Stages 1-3]

Objective: session start collapses from ~8 round trips to 1-2.

- [Claude] Write `session_open.py`: copy skill tools + data to workdir, unpack bundle state, run
  selfcheck + catalog-freshness note, print the board. One call, one consolidated output.
- Lookups become lazy: fetch `answers/INDEX.md` only when a dedup or id lookup is actually
  needed, not ritually. First fetch in a session chains everything else.
- [Claude] Update 00_INDEX task table + skill SKILL.md to route lookups at the answer layer.
- [dauntless] Confirm the INDEX raw URL sits in project instructions.

Exit benchmark: a cold session reaches "board reported, next item proposed" in <=2 tool-visible
steps, and a name-collision check runs against answer-layer data fresher than 24h without any
catalog in the bundle.

## Stage 5 - Command relay: DEFERRED

On-push Actions + GitHub Mobile app dispatch cover every current trigger need. Revisit trigger:
a proven need for Claude-initiated, sub-minute rebuilds mid-session via a fixed GET URL. Then:
Cloudflare Worker (100k req/day free), secret path segment, idempotent jobs only, and a
fetchability test of workers.dev before building anything.

## Sequencing

```
Stage 0  DONE
Stage 1  ----------------->  (parallel-safe)
Stage 2  sweep -> layout -> workflows -> prove
Stage 3            (needs Stage 2 workflows)
Stage 4                      (needs 1+3)
Stage 5  deferred
```

## Risk register

| Risk | Mitigation |
|---|---|
| RAG triggers on file count, not bytes (single-source report) | Stage 1 targets 3 files; benchmark verifies whole-file injection before proceeding |
| raw CDN ~5 min cache serves a stale answer right after a commit | INDEX carries a `generated` timestamp; a lookup that matters within 5 min of a push waits or uses the blob-page fallback |
| Answer file grows past comfortable fetch size | Per-entity split already caps it; hidden/live split next if a file passes ~100KB |
| Fetched content is context-priced, paid twice if written to disk | Answers stay small and are consumed in-context; bulk data never routes through fetch - it rides harvest commits and browser-side filtering |
| Pages-class outage (n/a now) / GitHub incident stalls Actions | Answers are committed files - readable via blob fallback even if Actions is down; last-good answers remain fetchable |
| Skill upload friction discourages tool fixes | skillpack.yml makes the zip one tap; fixes land in repo regardless, so nothing is lost between reinstalls |
| Stale archived docs mislead a fetch | STALE banner line at top of every `/archive/` file; INDEX links current files only |

## Standing rules unchanged by this plan

Everything ships hidden; publishing waits on the content admin's go-ahead, then dauntless
publishes. Balance, rewards, rarity, art direction and final acceptance are dauntless's.
Nothing is handed over unvalidated. A push echo is not a read-back.
