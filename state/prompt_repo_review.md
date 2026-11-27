# Repository review and cleanup: implementation brief

**Status:** DRAFT for the director's approval and an independent ChatGPT review. When approved, this file
is the build contract (CLAUDE.md §11). It changes no law, doctrine or ruling by itself; each decision
below that changes an operative rule gets its own ruling entry and owner update when it is made.

**Base:** `perseverance484/tnr-tools` main at `f0b5f0f89` (2026-11-27). **Live requests made by the
review:** none. **Branch:** this session can push only to `ccr-6a1d8ed7-02ktab`, which stands in for the
usual `fable/*` branch.

**Evidence:** `docs/reviews/REPO_REVIEW_2026-11-27/findings.json` holds all 93 findings (ids `BR-`, `LA-`,
`LB-`, `DA-`, `ASSET-`, `SA-`, `RL-`) plus the critic's verdicts, conflicts and gaps. Per-item tables are
in `evidence/` (branch classification, stranded rulings, unlanded live results, asset move list, state
and push inventories, a current-state draft). This brief cites ids and does not restate the findings.

---

## 1. Goal

Three outcomes, in this order:

1. **main is the full record again.** Everything that ran live, every ruling and every review verdict is
   on main, and nothing new can stay off it.
2. **The repo is lean and orients itself.** Orientation, the run queue and the rules in force are
   generated from sources, so they cannot go stale. Noise (lock heartbeats, telemetry, dead branches,
   bulky working art) moves out of main's way.
3. **Design sessions are creative-first.** The director touches a session three times: pick a concept,
   answer one decision card, say go. Everything else is a tool, a hook or a skill step.

## 2. What the review found (headline)

- **main does not describe the live game.** Since about 11-16, live jobs have run from unmerged
  `claude/project-thread-*` branches. The results bundles and manifests of jobs 640-698 and the 11-07
  quest deletes are off main (BR-01, LB-01). Forge source from an unmerged branch with red CI ran
  jobs 640/641 (LA-05). About 66 ruling entries exist only on branches, 12 of them under ids that main
  gave to other rulings (BR-03, LB-13). 112 review verdicts exist only on review branches (BR-04).
  Push numbers collide across branches (BR-02).
- **Orientation is hand-made and stale.** The digest/active-context is wrong in at least 10 places,
  for example it calls Mother of Echoes hidden when it went live on 11-14. About 45% of the 21
  non-done run_queue rows are wrong (LB-03, LB-05).
- **CI is red for an old reason.** Forge CI has failed on main since the 11-09 history rewrite
  because its tests pin pre-rewrite SHAs. PR #123 fixes it and has waited since 11-14 (LA-01, LA-02).
  Locally, about 900 tests pass, and none of them run in CI (LA-08).
- **Noise.** 57% of main's commits since 11-08 are run-lock writes, and about 300 more are jutsu-engine
  logs. Each one triggers three unfiltered CI workflows (LA-03, RL-*). 455 branches; the 11-08 prune
  was never run (BR-05).
- **Weight.** About 911 MB of the 1.23 GB checkout is working art (raws, previews, superseded
  versions) that nothing in code or manifests cites. The large-file guard only blocks files over
  5 MB, and 456 MB sits in 2-5 MB files that passed it (ASSET-01..05).
- **Skills have three drifting copies.** Six TNR skills exist only on claude.ai. The repo and the
  installed copies have each moved on without the other. simulating-tnr-combat points at a harness
  that exists only on PR #128. Skill overhaul P2 has sat unreviewed since 11-10, and `design.py
  compile` is still a stub (SA-01..04).
- **The authority prose has drifted; the mechanism is healthy.** Doctrine, packs and rulings gates
  pass. CHATGPT.md and DEVELOPMENT_WORKFLOW still say the live-game boundary predates RUL-132, and
  00_INDEX has wrong paths, a retired PAT step and no routes for AI player/PvP (DA-01..03).
- **Privacy gaps found by the critic.** The repo is public. Harvest bundles and PvP logs carry other
  players' usernames, and `scrub.yml` is weaker than `no-real-name.yml` (critic gaps 1-2).

## 3. Work packages, in order

Each package is one or more small Lane A branches, each handed off at an exact SHA for ChatGPT review.
Lane B record harvests (W1) are content commits under the existing ritual. Order follows the critic's
sequencing, so that nothing is deleted before its contents are safe and nothing is moved before its
readers are updated.

**W0. Today (director only).** The Watch Log Fourth Page, job 520, is scheduled for tonight's release
(Fri 11-27, 6 PM CT = 00:00Z) and is still unpublished. Its precondition has been met since 11-14
(LB-04). This needs a go card and the director's go, or a recorded skip. It is a live write and is
outside this brief.

**W1. Restore main as the record.** No deletes in this package.
1. Harvest the live-run records from the 12 branches in `evidence/live_unlanded.tsv`: bundles, result
   notes and manifests that ran, with colliding numbers renamed. Rebuild run_queue rows 640-698 and fix
   the stale and duplicate rows (BR-01, LB-03). Pre-run the answers, large-file, no-real-name and
   scrub gates locally first (critic conflict on BR-01).
2. Merge PR #123 after resolving its conflicts, so Forge CI goes green (LA-01). Then cut the Forge
   tests loose from pinned history and Lane B content (LA-02).
3. Land the record of jobs 640/641. Put the `zeroInstantResidual` livePatch through review (LA-05).
4. Harvest the 112 review verdicts into `docs/reviews/` (BR-04).
5. Produce the stranded-rulings reconciliation list, pre-sorted, for the director to confirm (BR-03,
   decision D3). Re-id the collisions (LB-13).
6. Harvest `state/moe_upload/uploaded.json` from `duet/moe-uploadthing`, which push generators name as
   their URL source (critic conflict on LB-15).

**W2. Guards so W1 cannot recur.**
- Reserve push numbers and ruling ids on main. Add a CI check for duplicates (BR-02, LB-02).
- `rulings_index --check` refuses duplicate ids, statuses outside the enum and ambiguous supersession
  (DA-04).
- `mcp_run` refuses live writes from Forge source that is not on origin/main, unless an override
  names the director's go (LA-05).
- A run-lock release refuses when the job has no results bundle on main (BR-01).
- Move bot workflows off other writers' branches (LA-04). Delete the dead `relay.yml` (LA-10). Run
  the passing test suites in CI (LA-08). Fix the `validate.py --parity` TypeError (LA-06).

**W3. Branch prune and lifecycle.** Only after W1.
- Push archive tags for every abandoned chain tip first. Then delete, with a scripted proof that each
  deleted head is an ancestor of `main` or of a pushed tag (critic verdicts on BR-10/BR-11).
- Never delete `builder-app` (CLAUDE.md §4) or `ops/*`.
- Then adopt the lifecycle rule (BR-12, decision D4): records and reviews land on main, numbers are
  reserved on main, `delete_branch_on_merge` is on, and a TTL report runs.

**W4. Skills single-source.**
- Bring all 9 TNR skills into `skills/`, merging the installed-only text first: the Shisui standard,
  the freeze stage and the pve-encounters split (SA-01, SA-02).
- Land PR #128 (harness/combat_sim) (SA-03). Review and land P2 (SA-04). Adopt or drop the Duelyst
  art redesign (BR-09).
- Add a drift check, and stop the art skill from sending raws into the repo (SA-05, ASSET-08).
- `beo-event-package` is not TNR and stays out.

**W5. Ops branches for the lock and telemetry.** Only after W4, because the lock writers run from
installed skills (critic conflict on RL-04).
- Move the lock to `ops/run-lock`, and telemetry plus the hourly jutsu log to `ops/player-log`
  (RL-01, RL-02, RL-05, RL-06).
- Browser Forge gets a lock-branch setting and a release (RL-03).
- Fail-closed cutover: tombstone main's lock, never delete it. A migrate-only path with its own tests
  (RL-04).
- Path-filter the workflows (RL-07). Update the "lock is on main" text in its owners (RL-08). Protect
  `ops/*` from pruning and rewrite tooling (RL-11).
- Requires a ruling that amends RUL-2026-11-07-133 (decision D5) and a scheduled idle window.

**W6. Orientation that cannot go stale.**
- Generate active-context/digest from run_queue, branches, CI and rulings, on a schedule and at session
  close (LB-05, SA-09).
- Add a `run_queue` tool and lint, so the queue stops being hand-edited (LB-03, SA-08).
- Make one start-here map: fix the 00_INDEX routes and paths, refresh the README, give full gate
  paths in CLAUDE.md §8 (DA-02, critic gap 3).
- Make CHATGPT.md and DEVELOPMENT_WORKFLOW cite CLAUDE.md §6 instead of restating it, and add a lane
  table covering Fable, ChatGPT, Duet, Astra and the pilot (DA-01, DA-03).
- Generate a "rules in force" view from the ledger (DA-05).
- Triage the sentinel drift and the law-reconciliation backlog: law 18 items, the 5 lawmap warnings
  (LA-07, DA-06, DA-11).

**W7. Archive passes.** Every move is gated on a reference graph that maps manifests to generators,
exceptions, scripts, run_queue and the Forge loader (critic gap 7). That graph would have caught the
Skyglass generators that read push/342-420 and `state/skyglass_thread_boards_v2/v3`.
- Ghost Ship goes as one unit (harness, state and push together) or not at all (critic conflict).
- Then: state/ spent entries (LB-09), push/ manifests that ran (LB-10), Ghost Ship harness (LA-11),
  `10_LAWS_core.md` folded into a citing index (DA-07), spent root docs (DA-08), and the
  reviews/handoffs retention policy (DA-09).

**W8. Asset offload.**
- Build the manifest and fetch/check tool first (ASSET-06). Import the existing per-folder SHA256SUMS
  and update the allowlist in the same commit (critic gaps).
- Fix the classifier so delivered avatars and SUMS entries stay (critic verdict on ASSET-04). Keep the
  Skyglass raws while the event runs, or add a fetch step (critic verdict on ASSET-03).
- Move M1-M5, about 911 MB (ASSET-02..05). Keep the 18.5 MB of raws that approved.json validates
  (ASSET-07). Tighten the guard (ASSET-01). Use partial clones for agent sessions (ASSET-10).

**W9. Creative-first automation** (SA-06..SA-12, LA-15).
- One decision card per design (`design.py decisions`).
- Generated go cards.
- A chained post-run closeout: bundle, verify, run_queue row, one-line outcome.
- Generators for rulings entries and implementation handoffs.
- One general before/after read-back verifier.
- Repo hooks: a SessionStart drift check, a Stop closeout and a PreToolUse run-lock guard on connector
  writes. Hooks are added only with the director's approval (decision D9).

Session shape: idea → `design.py new` offers 2-3 concepts (**touch 1**) → design check and freeze →
encounter shape → sim → `design.py compile` → validate and check_manifest → art → **one decision card**
(touch 2) → generated go card (**touch 3**) → run → automatic closeout.

## 4. Decision card

The director's answers go into rulings where they change an operative rule.

| # | Decision | Recommended | Ids |
|---|---|---|---|
| D1 | Watch Log Fourth Page (520) tonight: publish or skip | director's call (needs a go card) | LB-04 |
| D2 | Were jobs 640/641 (11-18) authorized? Should the livePatch be reviewed and merged? | land the record either way; review the code | LA-05 |
| D3 | 66 branch-only rulings: in force, superseded or never adopted (pre-sorted list to confirm) | Fable pre-sorts, director confirms | BR-03 |
| D4 | Branch lifecycle rule: records land on main, numbers reserved, auto-delete on merge, TTL | approve | BR-12 |
| D5 | Lock on `ops/run-lock`, telemetry on `ops/player-log`; amend RUL-133; idle window | approve | RL-01, RL-04, RL-10, SA-11 |
| D6 | What stays on main: `pvp_playbook.md`, `do_not_attack.md` (curated) | approve the split | RL-10 |
| D7 | Offload storage: GitHub Releases (public, like the repo) or private R2 (needs a token) | Releases, unless working art should be private | ASSET-09 |
| D8 | Public repo and other players' names in bundles and PvP logs: accept, redact going forward, or make the repo private | redact going forward, at minimum | critic gap 1 |
| D9 | Approve repo-level Claude Code hooks and the three-touch session shape | approve | SA-12 |
| D10 | claude.ai skills uploaded only from repo zips (no direct edits); adopt the Shisui and freeze text verbatim | approve | SA-01, SA-05 |
| D11 | Adopt the Duelyst art redesign (at most one visual tag per jutsu); keep or drop the separate animation skill (P5) | director's call | BR-09, SA-04 |
| D12 | Workstream calls: AP4 next or parked; guide-studio resume or archive; Forge Next status; One Perfect Crop publish, hold or retire; MoE/Skyglass sim harness archive as tags; PR #126 and early-game spine; Duet MoE branch reconcile path | per finding | BR-06..08, BR-13, LA-14, DA-12, LB-08 |
| D13 | Retire the old pilot under `state/player/dauntless/tools/` in favour of `player/` | approve if retired | LA-13 |
| D14 | Forge bundle budget: size pass before the next feature, or keep raising it | size pass | LA-09 |
| D15 | Skill zips committed to `dist/` or published as release assets only | release assets | ASSET-12 |
| D16 | Reviews/handoffs retention: archive closed chains to `docs/archive/<workstream>/` | approve | DA-09 |
| D17 | Retire the PAT step in the mounted instructions | approve | DA-03 |

## 5. Execution guardrails

- Zero live requests in every package except where the director gives a go for a specific job
  (CLAUDE.md §6).
- No deletes before the contents are on main or in a pushed tag, with a scripted proof. Branch and
  file deletes list exactly what goes and are approved in the handoff.
- Every archive or offload move passes the reference graph and the existing gates. Generated
  projections are regenerated, never hand-edited (CLAUDE.md §7).
- Each package's gates are reported with exact commands and exit codes (CLAUDE.md §8).
- The history rewrite question stays closed: none is proposed (ASSET-10).

## 6. Not begun

No cleanup, harvest, prune, move or skill change has been made. This review added only this brief and
`docs/reviews/REPO_REVIEW_2026-11-27/`.
