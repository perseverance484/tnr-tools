# Skills & automation audit notes (main@f0b5f0f, 2026-11-27, read-only)

INST = /root/.claude/skills/synced/c6b61462-c5db-4e38-a151-1724b489b258_7c24f8b2-5657-4eb6-9a0f-c3ba094f5ecf

## 1. Three-way skill drift (installed vs repo skills/ vs dist/*.zip)

dist/*.zip == repo skills/ exactly (unzipped and diff -rq: only __pycache__ differs). Last dist rebuild c8843583f 2026-11-16.
Installed (manifest.json updatedAt): building 2026-11-22T05:58, designing 2026-11-22T05:58, art 2026-11-22T19:57.

Neither side is a superset — both moved:

building-tnr-content
- Installed doctrine block stamped @17d6a71 = docs/DOCTRINE.md blob from bcd3b30ff (2026-08-30). Repo stamp @b614200 = current blob (776278878, 2026-11-09). Installed doctrine projection is ~3 months stale (missing D-user-pushes RUL-132, D-no-franchise RUL-141).
- Installed-only text: pointer to docs/combat-engine/tags/<tag>.yaml for tag behaviour (SKILL.md line ~80).
- Repo-only files: data/45h_DATA_lints.json; scripts/bloodright_bridge.py, build_event_sheet_docx.js, catalog_checks.py, dungeon_bridge.py, pet_checks.py, variant_checks.py.
- 25+ files differ (45c..45g contracts, packs/*, references ai/event/pipeline, validate.py, selfcheck.py, factory.py, harvest.py, session_open/close.py, schema_extract/diff ...). Installed contracts are older (installed lacks 45h lints the repo validate uses).
designing-tnr-content
- Installed = SKILL.md ONLY (no scripts/design.py, no references/templates, no data/schema) yet the SKILL.md tells the agent to run scripts/design.py "in the tnr-tools repo".
- Installed-only content (newer direction, 2026-11-22): stage 3F Freeze + freeze card, hard-limit checklist in brief, fight design delegated to designing-tnr-pve-encounters, combat-engine map as owner of tag behaviour, exclusions.yaml check.
- Repo-only: doctrine block, templates table, data/, references/, scripts/design.py (new/check/explain/compile stub).
producing-tnr-art
- Installed-only: "Consumable icons: the Shisui standard" section (~70 lines, director rulings 2026-11-22), upload via UploadThing host + connector (shipping-tnr-content image jobs) with browser Forge as fallback.
  grep -r Shisui over skills/ docs/ state/: no hits. art/consumables_upgrade/refs/shisui/ does not exist on main.
- Repo-only: data/frames, data/rank_icons (archive-only, excluded from zip by pack_skills.py anyway).
- Third version: origin/fable/art-skill-duelyst (12 commits ahead, 2026-11-19, Duelyst library-first, fx_recipe.py, RUL-2026-11-16-165) — unmerged; installed has 0 Duelyst mentions; duelyst branch has 0 Shisui mentions.

## 2. Installed-only TNR skills: where they point (existence checked on main)
| skill | referenced paths | status on main |
|---|---|---|
| designing-tnr-pve-encounters | docs/combat-engine/*, docs/design/COMBAT_ANIMATION_ENGINE.md, docs/design/SKYGLASS_DUNGEON_AND_TREASURE_HUNTS.md, docs/workflows/OPERATING_MODEL.md, state/player/combat_rules.md | all present |
| shipping-tnr-content | forge/tools/mcp_run.mjs, run_lock.mjs, check_manifest.mjs, docs/workflows/FORGE_MCP_RUNNER.md, OPERATING_MODEL.md, state/run_queue.json, harvests/inbox, push/NNN | all present |
| simulating-tnr-combat | harness/combat_sim/{run.sh, tools/pull_live.py, tools/merge_results.py, scenarios/isonade_replay.json, genin_hideout.json} | MISSING on main; exists only on origin/claude/project-thread-f2r8sb (3 commits, PR #128 open since 2026-11-19, merge-tree: 0 conflicts) |
| tnr-jutsu-engine | forge/tools/run_lock.mjs, data/player_allowlist.json, state/player/dauntless/jutsu_training.md | present |
| tnr-pvp-combat | state/player/<account>/tools/{combat_map,hunt_plan,policy,postfight,shotplan,turn,enemy_model,ids,replay}.py, rules_config.json, state/player/dauntless/*.md, state/prompt_playing_tnr.md, docs/combat-engine | present (dauntless) |
| tnr-replay-analysis | state/player/dauntless/tools/{postmortem,engine_check,fight_bases,tune_real,ids}.py, /mnt/project-files/tnr/<opp>_review/REVIEW.md | repo paths present; /mnt/project-files is a claude.ai project mount, not repo |
beo-event-package: not TNR (hotel BEO whiteboards). Keep out of the TNR repo.

## 3. Packaging / CI evidence
- .github/workflows/skillpack.yml triggers on push to ANY branch touching skills/** and auto-commits dist/*.zip + 3 root JSON copies.
- "skillpack: rebuild" commits: 122 across all refs vs 96 on main => ~26 noise commits on feature branches.
- git merge-tree origin/main origin/fable/skill-overhaul-p2 -> only CONFLICT is dist/building-tnr-content.zip (generated).
- pack_skills.py iterates every dir in skills/ -> adding skills is automatic; 2 MiB cap per zip.
- README.md: "/dist/ installable skill zips, rebuilt by the skillpack workflow". No documented upload step to claude.ai; installed versions show hand edits on claude.ai side.
- No .claude/settings.json, no hooks, no .claude/skills in repo (.claude/agents/tnr-relay.md only).

## 4. Skill overhaul (state/prompt_skill_overhaul.md)
P0 merged (docs/handoffs/skill_overhaul/INVENTORY.md), P1 merged (776278878 .. 13d2c2b29, 2026-11-09).
P2 origin/fable/skill-overhaul-p2: 3 commits (fa4624aa5 laws 90/91 groundwork; 7de246ee9 libraries + compile ai/ai_line; 0ad5f7617 skillpack auto). 22 files, +1671. Stalled since 2026-11-10; no P2 handoff/review doc found in docs/reviews or docs/handoffs.
On main, design.py compile is a stub that always refuses (cmd_compile returns 3).
P3-P6 not begun (no branches). Brief predates the installed-side "freeze" + pve-encounters split (2026-11-22) and the Duelyst art redesign.
Gates run: doctrinemap.py exit 0; render_doctrine.py --check exit 0; build_packs.py --check exit 0; design.py --selftest exit 0; rulings_index.py --check exit 0.

## 5. Commit mining (origin/main since 2026-11-08; 2309 commits)
run-lock: release by player 353, heartbeat by player 246, claim by player (jutsu engine) 179, claim (refill) 113, release by claude 88, ...  (~1316 total)
player: jutsu engine 178; jutsu training refill 117  -> 306 commits all touching state/player/dauntless/jutsu_training.md
results: 16 (harvests/inbox); sentinel 15 (docs/DRIFT.md + state/schema_sentinel.json, auto); skillpack 11; harvest 9.
state/run_queue.json hand-edited in 67 commits (no tool writes it: grep run_queue.json in *.py/*.mjs = 0 writers).
docs/rulings/ touched by 35 commits; docs/reviews+docs/handoffs by 79.
state/active-context.md/status.json/digest.json last refreshed 2026-11-09 (commit msg: "stale since 2026-10-17") -> manual refresh roughly every 3 weeks, stale in between.
Rulings sequence numbers reused across dates (127,136,137,138,139,148,149 appear twice); 165 used on unmerged duelyst branch, skipped on main. Full ids unique by date, index check passes.
run_lock.mjs already supports RUN_LOCK_BRANCH env (default main). Browser Forge core.mjs reads/writes state/run_lock.json via contents API (needs a ref param to move). RUL-2026-11-07-133 fixes the lock on main -> moving needs a ruling amendment.

## 6. Automation candidates (ranked by estimated director minutes/week; estimates, not measured)
1. One decision card per design (design.py `decisions`): ~60-120 min/wk (fewer round trips of single questions)
2. Go card generator (`gocard.py push/NNN` from manifest + validate/check_manifest/ledger exits + run_queue row): ~30-60
3. Run closeout chain (mcp_run -> harvest.py verify -> run_queue row -> commit bundle -> one-line outcome): ~30-45
4. Skill sync drift check + single source (repo -> zip -> claude.ai): ~30 (and removes stale-doctrine risk)
5. Scheduled state refresh (digest/active-context from run_queue, open PRs, last rulings): ~20-30
6. Handoff generator (base/head, changed files, gate commands+exits): agent time mostly; ~10 director
7. Rulings `new` allocator + duplicate check: ~5-10
8. Run lock + player commits off main (RUN_LOCK_BRANCH): director review/noise; 57% of main commits
9. skillpack: check on branches, build+commit only on main: removes dist merge conflicts

## 7. Creative-first design session flow
Director: idea (one paragraph)  ->  [designing-tnr-content] brief+hard-limit checklist auto-filled from design.py new --from-idea; concept options
 -> design sheet (design.py new/check; libraries P2) -> freeze card (installed 3F)
 -> fight shape [designing-tnr-pve-encounters] -> sim [simulating-tnr-combat, harness/combat_sim] measured rates
 -> compile [design.py compile -> building-tnr-content factory/mission/enemy -> validate --strict, check_manifest]
 -> art slots [producing-tnr-art]
 -> ONE decision card (design.py decisions: all AWAITING_RULING slots + open decisions + sim gaps vs targets + reward/rarity/publish questions, DIRECTOR_DECISIONS.md §6 format, numbered for one-line answers)
 -> director answers in one message -> rulings auto-drafted (rulings_index.py new) -> sheet filled -> recompile
 -> go card [shipping-tnr-content gocard.py] -> "go" -> mcp_run + closeout chain.
Hooks: Claude Code Stop/SessionEnd hook runs session_close.py + run_queue lint; PreToolUse on mcp__Tnr__callEndpoint write procs requires a held run-lock token (settings in repo .claude/settings.json).
