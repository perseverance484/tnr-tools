> **STALE - archived 2026-08-28 (rollout Stage 1).** superseded by project 00_INDEX.md (rewritten for the layer architecture).
> Do not build from this file.

# 00 - TNR Content Generation: router

TNR is an open-source Next.js / tRPC / Drizzle web game at theninja-rpg.com. dauntless is a
contributor on content staff, working from Samsung Android in Firefox with ViolentMonkey. Claude
turns concepts into validated builder manifests; the hosted builder replays them against the live
game. Never copy proprietary text, never reference the Naruto franchise.

**This file routes. It does not teach.** Everything it names owns its subject; nothing here
restates what that file says.

## The two layers

Storage is what IS. Intent is what we MEAN. They live apart on purpose, because reading one as
the other is a repeat failure.

| Layer | Holds | Where |
|---|---|---|
| **Prose Claude reads** | laws, coverage, doctrine, design registries, this router | project knowledge, 12 files |
| **Craft prose and base tools** | jutsu / ai / item / quest / pipeline / balance references | skills, on demand |
| **Everything scripts read** | generated contracts, catalogs, art spec, mission profiles, tools | the session bundle, `data/` and `tools/` |
| **Intent** | current work, decisions, blockers, lessons | the session bundle, `state/` |
| **Cold storage** | builder bundle, full catalogs, archived lore and retired docs | tnr-tools repo |

**Why the split is drawn here.** Project knowledge is retrieved, and once it is large enough
Claude stops seeing whole files and starts seeing chunks. It was believed that JSON was exempt
because scripts read it off `/mnt/project/`. **That was tested on 2026-08-28 and is false**: a
`project_knowledge_search` returned three chunks of `45c_DATA_constructors.json`. Every byte here
counts. So anything a script reads lives in the bundle, where it costs nothing, and project
knowledge keeps only prose that has to be in Claude's head.

Project knowledge changes only by deliberate promotion.

## Precedence

Read `01_PRECEDENCE.md`. The one rule that keeps getting broken, stated here too because it is
the expensive one:

**Live content is storage, not intent. It shows what the engine accepts, never what we chose.**

When two sources disagree, say so. Do not silently pick one.

## Session start

1. Unpack the uploaded bundle. Read `state/active-context.md`, then parse `state/status.json`.
2. Copy tools from the skills into the workdir, then overlay `tools/` from the bundle. A skill
   reinstall reverts every patch; `tools/PATCHES.md` lists what and why.
3. Copy the bundle's `data/` and `state/catalogs/` into the workdir. The generated contracts,
   the art spec and the mission profiles all live there now, NOT in project knowledge.
4. Run `selfcheck.py`, then `stack.py /mnt/project`.
5. Run `catalog_sync.py --check` and report anything past `stale_after` before starting work.
6. Report done / in progress / blocked / stale, and propose the next item.

No bundle means no catalogs. Say so rather than working from memory.

## Task routing

| Task | Read | Use |
|---|---|---|
| Any manifest, before handoff | - | `validate.py m.json` MANDATORY, zero errors, state what ran |
| Building any payload | - | `factory.py` CONSTRUCT it; hand-authoring is the fallback |
| Payload shape, tag or rule fields | - | `45c_DATA_constructors.json` |
| Field bounds, defaults, nullability | - | `45d_DATA_entity_schemas.json` |
| Any engine constant or its doc comment | - | `45e_DATA_constants.json` |
| Which tRPC procedure, what input | - | `45f_DATA_procedures.json` |
| What both validators check | - | `45g_DATA_checks.json`, one config two consumers |
| Is a law enforced or must I know it | `12b_LAWS_coverage.md` | it claims coverage the tool may not have; verify |
| AI enemy stats and pools | law 15, skill `references/ai.md` | `calc.py ai --level N --hp N --role X` |
| AI kit ids and gates | `references/ai.md` | `calc.py kit --codes ...` |
| Rewards | `references/balance.md` | `calc.py reward --rank X` |
| Any capture or results bundle | - | `harvest.py`, then `catalog_sync.py` to fold it in |
| Name collision or id lookup | - | bundle `state/catalogs/`; live truth via a capture block |
| A mission, any rank | `48_DATA_mission_profiles.json` | `mission.py sheet.json --spec 25x_DATA_art_spec.json` |
| Ratifying a profile slot | - | `profile_derive.py <capture>` |
| New jutsu / item / AI / quest / event | skill references | validate before handoff |
| Dialog | `references/quest.md` | HTML format, forks must diverge, no em dashes |
| Art | skill `producing-tnr-art` | exact filenames are the wiring contract |
| Balance philosophy | `references/balance.md` | propose; dauntless decides |
| Registries | 32 / 34 / 38 / 39 plus twins 32b / 34b | codes over ids in authoring |
| Builder edits | `references/pipeline.md` | upload the current bundle from the repo first |
| Repo drop lands | - | regenerate `45c` FIRST: `schema_extract.py <repo> --ctors` |
| Ending a session | `tools/CLOSEOUT.md` | `closeout.py`, which refuses a bad bundle |

## Non-negotiables

- Everything ships `hidden: true`, every entity, law 16b. Publishing is a separate step: it waits
  on the content admin's go-ahead, then dauntless publishes.
- Nothing is handed over unvalidated, and you say what ran.
- A push echo is not a read-back. `state: ok` with `live: NONE` means unverified.
- A filtered capture proves nothing.
- Balance, rewards, rarity, art direction and final acceptance are dauntless's to settle.
  Propose, show one at a time, wait.

## Retired from this stack

Archived in the repo: hand file 45, file 50, the migrated guides (10, 20-26, 30, 33), the lore and
arc files (27, 28, 28b, 29, 31, 31b), the `70_TOOL_*` scripts.

Moved to the session bundle 2026-08-28, so that project knowledge could leave chunked retrieval:
every `.json` (21 files, 1140KB), the three loose `.py` tools, and the intent files `90_STATE_board`,
`91_PLAN_stack_overhaul`, `94_ART_disposition`, `44` and `44b`. Archived to the repo:
`92_MAP_file50_retirement`, `README_APPLY`, `MANIFEST.sha256`.

The stack went from 43 files / 1360KB to 12 files / 100KB. `stack.py` treats `migrated`,
`archived` and `bundled` as legitimate states and errors only if a retired file reappears here.

## Deploy notes

Bundle: commit to repo root, verify the GitHub blob view shows the new version, raw CDN caches
about five minutes, refresh via ViolentMonkey rather than a `?v` bump, reload. The panel title
must show the version and `cfg generated`. **`partial` means one of `45c`, `32b` or `45g` is
missing from the repo root**, and a missing `45g` silently reverts the v4.23 null fix.
