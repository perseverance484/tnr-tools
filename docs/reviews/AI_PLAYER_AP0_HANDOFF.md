# AI player overhaul, phase AP0: handoff and findings

Contract: `state/prompt_ai_player_overhaul.md` section 3 (AP0). Design: `docs/design/AI_PLAYER_OVERHAUL.md`.
Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md`. Written 2026-11-11.

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-base
Base: 41ee6bff7b4ee9c4e849b749cd906e511a49e816 (fable/ai-player-overhaul-brief = main 04245259 + the design and brief)
Merged in: fable/pilot-planner-fixes @ 6cbaa03f1888c52c8f984accd7f3b5638b73ea9d
           fable/pvp-engine-harness  @ f6e8c860037229ee5f72556ec7f351df990a1702
Head: the commit that adds this note (FROZEN; the exact SHA is in the handoff message)
Integration target: main @ 0f7d3535e10a42dbe8776cef842eb2c5f9493c90 (5 run-lock commits ahead of the base;
                    it changed state/run_lock.json only; git merge-tree reports no conflict)
```

## Objective

One base branch for the AI player overhaul, a draft endpoint allowlist from the live router surface with its
never-list check, and every current tool file mapped to keep, port or retire.

## Changed

| Commit | What |
|---|---|
| `949bc632` | Merge of `fable/pilot-planner-fixes`. No conflict. |
| `f57f1538` | Merge of `fable/pvp-engine-harness`. One conflict, in `pilot.py` `world()`. Resolved as the brief says: Duet's battle loop whole, plus the harness branch's kit read before the attack and its kit-read retry. The merged `pilot.py` differs from Duet's by exactly those two hunks (8 lines). |
| `3759148e` | `tests/test_pilot.py`: the stale second copies of three tests are removed, and a test for the kit-read retry is added. |
| `0034f6b2` | `docs/design/AI_PLAYER_OVERHAUL.md` section 2: the file map (53 files). |
| `f5b97ef3` | `data/mcp_surface.json`, `data/player_allowlist.json`, `scripts/player_allowlist.py`, `scripts/test_player_allowlist.py`, `docs/design/AI_PLAYER_ALLOWLIST_REVIEW.md`. |
| this commit | This note. |

Not begun: everything in AP1 and later. There is no `player/` package, brain, relay, budget or gates module yet.
`data/player_allowlist.json` is data and a checker; nothing enforces it at run time until `player/gates.py` (AP1).
Neither source branch was touched.

## Verification

Run on the head, from the repository root unless a folder is given.

| Command | Result |
|---|---|
| `python3 tests/test_planner2.py` (in `state/player/dauntless/tools`) | exit 0; `parity: 4000/4000 lines match` |
| `python3 tests/test_pilot.py` (same folder) | exit 0; 8 `ok` lines |
| `python3 tests/test_integration.py` (same folder) | exit 0; 27 checks `ok`, none missing; `ok: every system is wired in` |
| `python3 tests/test_nearkill.py` (same folder) | exit 0; 3 `ok` lines |
| `python3 -m unittest scripts/test_player_allowlist.py` | `Ran 33 tests`, `OK` |
| `python3 scripts/player_allowlist.py check` | exit 0; `never-list check: clean (0 violation(s))`; 89 endpoints; surface 85 allowed, 4 ask first, 320 never, 532 not listed |
| `python3 scripts/player_allowlist.py report --check` | exit 0; the review is current |
| `python3 scripts/check_no_real_name.py`, and `--commits 41ee6bff..HEAD` | exit 0, both |
| `python3 scripts/check_large_files.py` | **exit 1**: `harvests/inbox/tnr_results_1794368544997.json` (7.9 MB). See debt 1. |

Before the merge, the same four player tests passed on each source branch as fetched (`test_nearkill.py` exists on
Duet's branch only).

Two checks were made by hand and are not committed as tests:
- The new kit-retry test fails when `pilot.py` is put back to the old one-shot rule (`kit_asked`).
- Every literal input that `pilot.py`, `restock.py` and `harvest.py` build (30 call shapes) fits the live schema of
  its endpoint: every required key is sent, and no key is sent that the schema does not have.

## Source and provenance

- **Live surface:** `data/mcp_surface.json`, captured 2026-11-11 19:48:38 to 20:01:41 UTC through the TNR
  connector: 1 `listGameRouters`, 79 `listRouterEndpoints`, 89 `getEndpointSchema`. It is rebuilt with
  `python3 scripts/player_allowlist.py surface --transcript <session transcripts> --kinds-from
  skills/building-tnr-content/data/45f_DATA_procedures.json`. The transcripts live on the session's machine and are
  not in the repository, so the file is a capture, not something a reviewer can rebuild.
- **Query or mutation:** the server does not say. 476 types come from the stand-in description the server writes
  for a procedure that has none ("query x.y"), 455 from the source extract `45f` (studie-tech/TheNinjaRPG @
  3314d122, 2026-10-29, older than the live server), and 10 are unknown. All 89 listed endpoints have a type.
- **Prerequisites and cooldowns** on the list come from the pilot code, the account notes and the `tnr-pvp-combat`
  skill. They are not read from the game. The 33 `proposed` endpoints carry what the live description says and no
  more.
- **Generated:** `docs/design/AI_PLAYER_ALLOWLIST_REVIEW.md` is rendered from the two data files and is
  byte-reproducible (`report --check`).

## Live-game statement

- Live requests: 169, all through the official connector, all one of the three router-surface tools above.
  **No `callEndpoint` call was made**, by this session or by the two relay agents it used; the count is taken from
  the transcripts of all three.
- Game writes: none. Gameplay actions: none.
- Credentials or session material: none used or seen. The connector holds its own.
- Run lock: claimed as `claude` 19:48:30 UTC after Duet's pilot released it at 19:35:16, renewed once, released
  20:02:13 (RUL-2026-11-07-133: bulk reads take the lock). Those are 3 commits on `main` that touch
  `state/run_lock.json` only, written by `forge/tools/run_lock.mjs`.
- Not performed: any read of the character, a battle or a list through `callEndpoint`; any browser check.

## Findings

1. **The live surface is 79 routers and 941 endpoints**, not the 83 routers the design quotes.
2. **Stat training has a captcha.** `train.startTraining` and `train.updateEnergyTrainingQueue` take an optional
   `guess`, and `misc.getCaptcha`, `refreshCaptcha` and `verifyCaptcha` exist ("Answer the pending training
   captcha"). The list refuses the three captcha endpoints and forbids `guess` (gate `no_captcha_answer`). The
   pilot does not send `guess` today.
3. **`jutsu.transferLevel` is off the list.** `jutsu_training.md` says transfers are free for this account "as
   staff". The brief allows no staff powers in play.
4. **The harvest reads other players' fights.** `harvest.py` crawls `combat.getBattleHistory` and
   `combat.getBattleEntries` for other players, and `opponents.py` feeds what it learns into the live planner.
   RUL-2026-11-09-146 calls these staff reads, for study, and says live play does not use them on a named opponent
   unless the director says so. Both endpoints are on the list with the gate `study_only`, pending a ruling.
5. **The record catalogue holds hidden records.** `harness/pvp_turn/tools/fetch_catalog.py` reads the game's public
   unauthenticated API with `hidden: true`. It is not a connector call, so the allowlist does not cover it. The
   player brief (section 5.2) says the player does not use hidden records.
6. **`quests.getAll` and `quests.get` are off the list.** The medical-mission notes use them to read question text,
   and on a staff account they can return hidden quests. The missions playbook (AP3) needs another read.
7. **`profile.getPublicUsers` has an `ip` filter**, and two proposed reads take a `userId`. The entries say never
   the filter, and own id only.
8. **`turn.py` is not a dead fallback.** The repository default leads with it, and Duet's five planner fixes of
   2026-11-11 changed 384 lines there against 32 in planner2. AP4 is a port of rules, not a deletion.
9. **Three data feeds are run by hand or not at all:** `meal_factor.py` (nothing runs it; planner2 reads its file),
   `validate.py --write-scales`, `engine_fit.py --write`.
10. **Field selects over lists do not stay aligned** when an element lacks the field: the connector drops it from
    the column. This is recorded in `pilot.py` and enforced by `opponent_kit.save_kit`; it was seen live by the
    pilot on 2026-11-11 and not re-checked here, because AP0 made no game reads.
11. **`tests/test_pilot.py` hid a test.** Three tests were defined twice and the older copies ran, so the
    daily-errand assertions never ran. They run now and pass.

## Known debt and deviations

1. **The large-file guard fails on this branch.** `harvests/inbox/tnr_results_1794368544997.json` (the public
   catalogue capture of 2026-11-10, commit `b7e34dd1`) is 7.9 MB and came in with both source branches; `main` does
   not have it. Allowing it or trimming it is the director's call (`scripts/check_large_files.py`), so it was left.
2. The player tests write into the working tree: `tools/pilot_good.py` and `fights/observed/harvest.json`. Neither
   is committed. The AP1 tests write to a temporary folder only.
3. `pilot.py` looks up a result under `travel.startRandom`, which is not an endpoint. It is harmless and is listed
   under `not_calls`.
4. Deviation: the allowlist's schemas cover the 89 listed endpoints, not all 941. The full set is about 850 more
   calls, some 45 minutes with the pilot paused, for endpoints the player is refused anyway.
5. Deviation: `data/player_allowlist.json` sits at the repository root's `data/`, read literally from the brief.
   The player brief writes the same path relative to a skill. AP1 fixes where `player/` lives; the file moves with
   it if needed.
6. No workflow in `.github/workflows` runs `scripts/test_player_allowlist.py` or the player tests.

## Open decisions

For approval now (the AP0 gate):

- **The allowlist** (`docs/design/AI_PLAYER_ALLOWLIST_REVIEW.md`): approve, strike entries, or add. In particular
  the 33 `proposed` endpoints, and the two rules that came from the live surface rather than the brief (captcha;
  the staff-free level transfer).
- **Findings 4 and 5:** may live play use harvested fights of named opponents, and hidden catalogue records?

Due in AP1 (brief section 5):

1. **Goal weights** (item 1; seeds `player/goals.json`): the order of PvP wins, the daily caps (50 errands, 20
   missions, 9 medical), ryo income, hunting materials, and stat and jutsu training.
2. **Session windows and call share** (item 5): when the brain may run; its cap on world calls outside a fight
   (the pilot paces reads to 22 a minute today, the player brief's default is 12); and what it does while the
   director plays in the browser (the design pauses world activities).

Not due yet: equipment-swap scope and spend caps (AP2), PvE auto-combat scope and what counts as a rare item
(AP3), which further modes first (AP5).

## For the reviewer to attack

- The conflict resolution in `pilot.py` `world()` and the claim that nothing else of Duet's loop changed
  (`git diff 6cbaa03f <head> -- state/player/dauntless/tools/pilot.py`).
- The never and ask-first rules in `data/player_allowlist.json`: patterns that are too narrow. An unlisted
  endpoint is refused whatever the rules say, so a gap matters only when someone later adds an entry.
- The 33 `proposed` entries: each should be a call a normal player makes on their own account.
- `scripts/player_allowlist.py` `read_transcripts` and `build_surface`: that a failed or truncated result cannot
  enter the capture as an answer.
