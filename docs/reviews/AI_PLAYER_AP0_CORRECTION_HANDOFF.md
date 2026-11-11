# AI player overhaul, phase AP0: correction handoff

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md` section 5. Written 2026-11-11, in answer to the independent
review of `a95dfd1e` ("request changes": one validator defect, two handoff issues).

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-base
Reviewed: a95dfd1e5d8dbf2b6e506dba7bf0d4990d7339ce (the first AP0 handoff)
Head: the commit that adds this note (FROZEN; the exact SHA is in the correction message)
Commits since the reviewed SHA: 6d7380ec, 3a8a4c3f, f3b53a89, and this note
Integration target: main (it differs from the base in state/run_lock.json only)
```

## The three findings

| # | Finding | Verdict | What was done |
|---|---|---|---|
| 1 | [P2] Incomplete schema captures pass validation | Accepted | Fixed in `f3b53a89`. |
| 2 | `a95dfd1e` does not meet AP0's gate: a draft allowlist, and the large-file guard fails | Accepted | Both are closed on this branch, by `3a8a4c3f` and `6d7380ec`. |
| 3 | The handoff was superseded: the branch moved to `3a8a4c3f` with no correction handoff | Accepted | This note is that correction handoff. |

### 1. Incomplete captures passed the check

Reproduced on `3a8a4c3f` before the fix: with all 93 allowlisted schemas removed from `data/mcp_surface.json`,
`check` reported 0 errors; with capture faults written into `_meta`, 0 errors; and a failed `getEndpointSchema`
call followed by a reply cut short was counted as answered.

Fix (`scripts/player_allowlist.py`, `scripts/test_player_allowlist.py`, `data/mcp_surface.json`):
- `check`: on a live capture every allowlisted endpoint must have a valid input schema, and every fault the
  capture's builder recorded is a violation.
- `build_surface`: replies are parsed as they are collected, and only a reply that parsed is an answer. The newest
  good reply to a call is kept whatever came before or after it. A call that failed, or came back cut short or
  unreadable, stays unanswered unless some reply to it parsed. `answered_calls` counts parsed replies.
- The capture was rebuilt with the fixed builder from the same transcripts: its routers and schemas are unchanged,
  and only the fault lists in `_meta` are renamed and added to (`failed_calls_never_answered`,
  `replies_that_did_not_parse`, `schemas_for_endpoints_not_listed`, `schemas_that_say_nothing`).
- Seven tests (`CaptureCompleteness`). The reviewer's two cases are among them: removing every schema from the
  committed capture now fails all 93 entries, and a failed call followed by a cut reply stays unanswered.

One thing the stricter rule turned up, for the reviewer to judge: the game answers `{"$schema": ...}` and nothing
else for `travel.startGlobalMove`. That is the server's real answer (it publishes no input shape for that
procedure), so the capture keeps it, lists it under `schemas_that_say_nothing`, and `check` prints a note. It is
not treated as a fault. The pilot sends `{"sector": N}` to it live.

### 2. The gate was not met at `a95dfd1e`

Correct on both counts. I handed off with the allowlist still a draft for the director, and with the guard failure
written down as inherited debt instead of fixed. Inherited is not green.

- **Allowlist:** the director approved it the same day (RUL-2026-11-11-149, item 1). `data/player_allowlist.json`
  says so since `3a8a4c3f`.
- **Large-file guard:** the director allowed the capture to be trimmed (same ruling, item 7). `6d7380ec` removed
  the three hidden pulls from `harvests/inbox/tnr_results_1794368544997.json`: 7.87 MB to 4.56 MB. The untrimmed
  file is in history at `b7e34dd1`. `python3 scripts/check_large_files.py` exits 0.

### 3. The frozen SHA moved

Correct. After the director answered the handoff I pushed `6d7380ec` and `3a8a4c3f` to this branch while
`a95dfd1e` was under review, and named no new SHA in a correction handoff. That broke the freeze (CLAUDE.md
section 11, step 10). The reviewed commit is intact and is an ancestor of this head; no history was rewritten. The
head this note names does not move until the review returns.

## Everything that changed since `a95dfd1e`

| Commit | Files | What |
|---|---|---|
| `6d7380ec` | `harness/pvp_turn/tools/build_catalog.py`, `fetch_catalog.py`, `harness/pvp_turn/README.md`, `state/player/dauntless/tools/add_record.py`, `harvests/inbox/tnr_results_1794368544997.json`, `scripts/test_player_catalog.py` (new) | RUL-2026-11-11-149 item 4: hidden jutsu, items and bloodlines never reach the player's catalogue (902 and 1 left out on this tree); the fetch tool asks for none; `add_record.py` refuses one; the capture is trimmed. 6 tests. |
| `3a8a4c3f` | `docs/rulings/2026-11.md`, `docs/RULINGS.md`, `data/player_allowlist.json`, `data/mcp_surface.json`, `docs/design/AI_PLAYER_ALLOWLIST_REVIEW.md`, `scripts/test_player_allowlist.py`, `state/prompt_ai_player_overhaul.md`, `docs/design/AI_PLAYER_OVERHAUL.md`, `docs/reviews/AI_PLAYER_AP0_HANDOFF.md` | The ruling recorded. The list is APPROVED and has 4 more endpoints (`misc.getCaptcha`, `misc.refreshCaptcha`, `misc.verifyCaptcha`, `jutsu.transferLevel`); the ask-first rules `captcha` and `staff_free_path` and the gate `no_captcha_answer` are gone; the gate `one_transfer_a_day` is new. 4 more schemas in the capture. |
| `f3b53a89` | `scripts/player_allowlist.py`, `scripts/test_player_allowlist.py`, `data/mcp_surface.json` (`_meta` only) | Finding 1. |
| the head | this note | |

## Did a wider assumption change?

Yes, so this is more than a narrow re-check of finding 1. The scope is the reviewer's to set; what changed is:

- **The catalogue the combat tools read is smaller:** 1,859 records instead of 2,985. Five hidden records that
  logged opponents used or had equipped are now catalogue gaps (Stone Coffin, Mirror Edge, Numbing Senbon,
  Springguard, Twin Kunai). The four player tests pass on it. The engine replay tools (`engine_check`,
  `tune_real`) were not run, because there is no offline engine on this machine, so the effect on them is not
  measured.
- **The approved list allows two things the reviewed draft refused,** by the director's ruling: answering a
  training captcha, and one `jutsu.transferLevel` a day (free for this account as staff).
- **The capture's `_meta` keys were renamed.** Nothing else in the repository reads them.

## Verification on the head

| Command | Result |
|---|---|
| `python3 tests/test_planner2.py`, `test_pilot.py`, `test_integration.py`, `test_nearkill.py` (in `state/player/dauntless/tools`) | exit 0 each; `parity: 4000/4000 lines match` |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 46 tests`, `OK` (40 and 6) |
| `python3 scripts/player_allowlist.py check` | exit 0; `never-list check: clean (0 violation(s))`; 93 endpoints; one note (`travel.startGlobalMove`) |
| `python3 scripts/player_allowlist.py report --check` | exit 0 |
| `python3 scripts/rulings_index.py --check` | exit 0 |
| `python3 scripts/check_large_files.py` | exit 0 |
| `python3 scripts/check_no_real_name.py`, and `--commits 41ee6bff..HEAD` | exit 0, both |

## Live-game statement

Since `a95dfd1e`: four `getEndpointSchema` reads at 20:22 UTC for the four endpoints the ruling added, made with
the run lock free. No `callEndpoint`, no write, no gameplay action, no credential. The whole of AP0 is 173
router-surface reads.

## Still open

- AP0 finding 4: may live play use what the harvest learned from other players' fights about a named opponent.
  The ruling did not cover it.
- Duet's live pilot builds its own catalogue from its own branch and still has the hidden records until it takes
  `6d7380ec`.
- `fable/ai-player-ap1` (AP1) is built on `3a8a4c3f` and takes this head by merge. It is a separate handoff.
