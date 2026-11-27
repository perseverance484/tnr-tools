# Run lock and player telemetry off main: audit notes (read-only, main@f0b5f0f)

## Commit mix on origin/main since 2026-11-08 (2309 commits)
- run-lock touches of state/run_lock.json: 1316 (git log -- state/run_lock.json)
  - by player: release 353, heartbeat 246, claim(jutsu engine) 179, claim(jutsu training refill) 113, play/war-hunt/pvp ~20
  - by claude: release 88, heartbeat 33, claims ~40; duet ~30; browser ~30; misc threads ~25
- "player: jutsu engine" 178 + "player: jutsu training refill" 117 -> each touches ONLY state/player/dauntless/jutsu_training.md
- "dauntless ..." 81 -> sessions/2026-11-10.md, tools/policy_weights.json, pvp_playbook.md, tools/train_log.jsonl, tools/*.py (code)
- "fight log <bid>" (player/keep.py) -> state/player/dauntless/fights/*
- Last 8 days: 70-106 commits/day, of which ~50-67 run-lock and ~13-23 player: ~85-90% bookkeeping.
- Disk cost is small (deltas): jutsu_training.md 314 blobs 25.6 MB raw / 0.1 MB packed; run_lock.json 1390 blobs 0.1 MB packed; state/player 996 blobs 1.4 MB packed. The cost is history noise, push contention and CI runs, not size.

## Writers (all use one-commit-per-write against a fetched base)
| writer | file | mechanism | branch knob |
|---|---|---|---|
| forge/tools/run_lock.mjs (CLI; used by Claude, player/runlock.py, mcp_run.mjs, jutsu-engine skill, pvp skill, shipping skill) | state/run_lock.json | private index, commit-tree, plain ff push, 4 retries | RUN_LOCK_BRANCH (default main), RUN_LOCK_REMOTE, RUN_LOCK_REPO already exist |
| Forge browser (core.mjs lockStore -> github.mjs readExact/writeExact) | state/run_lock.json | contents API GET + PUT with blob sha; 409/422 = conflict | none: uses GH.branch = "main" (github.mjs:7); _url(path, ref) already takes ref |
| player/keep.py (spawned by player/combat.py:360) | state/player/<acct>/fights/** | same private-index ff push as run_lock.mjs | KEEP_BRANCH (default main) |
| tnr-jutsu-engine skill (claude.ai-synced, not in repo) | jutsu_training.md | agent commits "player: jutsu engine", pushes main | prose in SKILL.md line 52 |
| tnr-pvp-combat skill (synced) | sessions/<date>.md, pvp_playbook.md, target_cooldowns.md, fights/*_review.md, policy_weights.json/train_log.jsonl via postfight.py | agent commits | prose |

## Readers
- No raw.githubusercontent reader of run_lock.json or state/player found (grep over *.js/*.mjs/*.py/*.yml). raw readers: forge_loader_user.js (bundle by SHA), pin_release.py (bundle by SHA), build_answers.py (harvests), style_refs.py (art). None affected.
- run_lock.json readers: run_lock.mjs status/fetchLock (mcp_run.mjs imports fetchLock), Forge browser readExact, humans/agents per docs (FORGE_MCP_RUNNER.md:34-42, OPERATING_MODEL.md:18, player/OPERATOR.md:75-94, shipping-tnr-content SKILL.md:64-66, tnr-pvp-combat SKILL.md:15, tnr-jutsu-engine SKILL.md:16, several state/prompt_*.md).
- Telemetry readers: tnr-replay-analysis (fights/ in a checkout), tnr-pvp-combat (do_not_attack, target_cooldowns, hunt_roster, playbook, rotations, jutsu_training), state/player/dauntless/tools/* via relative ../fights paths; player/config.py fights_dir() (TNR_PLAYER_FIGHTS) -- note keeps_fights() treats that env as "rehearsal", so pointing it at an ops worktree would silently disable keep.py.
- release_pin.yml: triggered only by builder_bundle.js/forge_bundle.js on main; does not read the lock. builder: no run_lock reference found outside forge_bundle.js.
- scripts/session_open.py is referenced by docs/00_INDEX.md:70 but does not exist in scripts/ (outside this area; flagged for the orientation auditor).

## CI fan-out
- scrub.yml (on: [push]), large-files.yml and no-real-name.yml (on: [push, pull_request]) have no branch/path filter: every lock push runs 3 jobs; no-real-name does fetch-depth 0 + blob:none every time. ~1316 lock pushes x 3 = ~3.9k runs since 11-08 (estimated from commit count; Actions history not queried). A new branch still triggers these unless filtered.

## Proposed split
Move to ops/run-lock (lock only): state/run_lock.json
Move to ops/player-log (append-only telemetry):
- state/player/<acct>/fights/** (keep.py)
- state/player/<acct>/sessions/*.md
- jutsu_training.md "## Queue log" section plus "Owned already at 25" / "Donor jutsu" running lists -> e.g. jutsu_log.md on ops
- tools/train_log.jsonl
- target_cooldowns.md (24h ephemeral state)
Stay on main (curated / code / director-owned):
- player/** code and tests; state/player/<acct>/tools/*.py and tests
- PILOT.md, pvp_playbook.md, pvp_rotations.md, combat_rules.md, do_not_attack.md (safety list), hunt_roster.md, ryo_plan.md, medical_answers.md
- jutsu_training.md rules/limits/targets sections (director-edited)
- tools/policy_weights.json (read by policy.py at runtime; only 24 commits; revisit later)
- state/run_queue.json (job coordination; updated with job commits)
- harvests/inbox results bundles (answers.yml depends on push to main)

## Cutover sketch (lock)
1. PR (fable/*): RUN_LOCK_BRANCH default -> ops/run-lock; github.mjs GH.lockBranch + readExact/writeExact use it; refuse if branch missing (fail closed); tests; docs; bundle rebuild + budget check.
2. Claim main lock as holder "migration" (--ttl 240) -> proves free and blocks old clients.
3. Create ops/run-lock as orphan with a single state/run_lock.json = release body (releasedAt=now, quiet period honoured).
4. Merge PR; release_pin pins new bundle; director reloads userscript.
5. CAS-replace main's lock with a tombstone held by "moved" (expiresAt 2099, job "run lock moved to ops/run-lock, RUL-..."), using the migration token. Old CLIs/bundles see "held by moved" and refuse (fail closed). Never delete main's file: absent = free to old code.
Rollback: revert PR (or RUN_LOCK_BRANCH=main), release tombstone with its token (visible in the file), ops branch left for history.
