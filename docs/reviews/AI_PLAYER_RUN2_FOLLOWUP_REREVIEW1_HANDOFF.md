# AI player, after AP run 2: correction handoff, after the review of e051d062

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md` section 5. Written 2026-11-17, in answer to the review of
`e051d062` ("changes requested": F1 to F4, P2 each; the Ring check's weakness, P3).

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-run2-followup
Reviewed: e051d0622d9861032b583276b8b95cd96d1d6287
Review: docs/reviews/AI_PLAYER_RUN2_FOLLOWUP_REVIEW_20261117.md on
        chatgpt/review-ai-player-run2-followup-20261117 @ c05e5a86 (evidence; not merged)
Code: e4708482 (F1), 5121a4b4 (F2, F3), 1f0d2bd6 (F4), d5eb035e (the Ring check)
Head: the commit that adds this note (FROZEN; the exact SHA is in the correction message)
```

The diff to review is `git diff e051d062 HEAD`. Nothing wider is in it: no planner weight, no data, no default.
The token count and the planner's three settings are as reviewed.

## Disposition

All five are **confirmed and corrected**. Each of the review's runs is a test now, and each fails on e051d062.

| | What the review found | Now |
|---|---|---|
| F1 | With the heal line at full health, a heal that changed nothing set recovery aside for ten minutes and the hunt attacked the next target, at 5,049 of 5,050 | With health missing the hunt plans no attack, and the attack is refused at the call. The ten minutes stay |
| F2 | A fight against an AI came back from the post-mortem with no turn in it and `"engine": true` | A review with no turn says so and why; `engine` is null |
| F3 | The no-engine review ended in `FileNotFoundError` in a fresh checkout: `fights/live` is not tracked | The folder is made; what the review writes on its way can be sent to a test's own folder, and is |
| F4 | `keep(bid, paths)` let any file under the fights folder through, whatever the fight | A path is one of the fight's five own files, by name, or a kit of a player its log names |
| Ring | With no FIRE line the check on the fired move held for nothing | The planner must have ended well and fired a line before its landings are looked at |

## F1: no fight is started with health missing

The review's run, through the brain: a failed potion at 5,049 of 5,050, then a target in the scan. Recovery still
waits ten minutes before the next heal. What changed is what the hunt may do meanwhile.

- `player/activities/pvp_hunt.py`: with a target in the scan and health missing, it scans on and says whom it
  is not attacking and why. It still moves round the circuit.
- `player/gates.py`, `_whole`: `combat.attackUser` is refused with health missing (`health_missing`), the second
  lock, as `session_ending` is for an ending session.
- A fight that is running is played, and one he starts is fought: those are not `combat.attackUser`.

So the rule holds for every fight the brain starts. It cannot hold for one he starts.

**What this costs.** Where no heal takes (no potion, and none to buy), the hunt starts no fight until one does.
That is the rule as the director gave it; it shows in the status file as the hunt's reason.

Tests (`player/tests/test_loss_fixes.py`, `NoFightIsStartedMissingHealth`): the review's run, then a second look
still hurt, then whole again and the attack; the gate, hurt and whole; a running fight at 900 HP. The older test
that had the hunt go on after an unchanged heal (`test_activities.py`) now also says it starts no fight.

## F2: a post-mortem with no turn in it

`engine_check.positions` rebuilds a fight of two players and gives nothing for any other. So against an AI no
turn reached `swings`, and `engine` stayed at what it was set to before the loop. When no turn was rebuilt the
report now carries a note (the opponent is an AI; or no turn of mine could be rebuilt), `engine` is null, and
the report prints the note and no "turning point". The replay review reads any log and is still made.

I took the narrower of the review's two corrections. Rebuilding positions against an AI is not attempted: the
rules of the turn-by-turn review (his model, his kit, his reply) are a player's.

Test: the committed Arsenal Keeper fight through the whole post-mortem.

## F3: a fresh checkout

- `engine_check.exact_inputs` makes `fights/live` before it writes there.
- `fight_bases.LIVE`, planner2's two reads of it and `opp_profile`'s index take the folder from `TNR_PILOT_LIVE`
  when it is set, as `pilot.py` already does. Unset, nothing changes.
- The test sets it to its own temporary folder, checks the intermediate file is there, and checks that the
  checkout's `fights/live` is as it was (there or not).

Run in a fresh worktree of this branch with no `fights/live`, no engine pointer and no catalog: exit 0, five
checks. The only new files in the checkout afterwards are `harness/pvp_turn/kit/catalog.json` and
`bloodlines.json`, which the harness builds from the tracked harvests on first use.

## F4: `keep` and the files of a fight

`_rel(path, bid)` took any path under `state/player/<account>/fights/`. It now takes a path only if it is one
of `<bid>_entries.json`, `<bid>_meta.json`, `live_states/<bid>.json`, `live_states/<bid>.full.jsonl.gz`,
`live_states/<bid>.plans.jsonl.gz`, or the kit of a player that fight's log names. The check is before any fetch,
and one bad path in a list refuses the list.

Test: another fight's log and live state, a stray file, the same fight's post-mortem, this fight's log under
another fight's name, a good list with one bad path. Each refused, nothing pushed; the bare repository still
holds only the first commit's three files.

## The Ring check

`check("R5: planner2 ran to its end and fired a line", ...)` comes first: exit 0, a FIRE line, every action in it
with a name and an id. The landing check then also asks for the fired line. With `fire` set to nothing after the
planner's run the test stops at the new check; before, it passed.

I did not make the fixture require a move in the fired line: with and without his kit the line fired differs,
and the rule is where a move lands, not that there is one.

## Verification

On the head before this note (`d5eb035e`), with the note in the tree:

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 684 tests`, `OK` (e051d062: 681) |
| `python3 -m unittest docs/reviews/evidence/ai_player_hook_relay/test_preflight.py` | `Ran 44 tests`, `OK` |
| `python3 docs/reviews/evidence/ai_player_hook_relay/fake_connector.py --selftest` | exit 0 |
| `tools/tests/test_{critique,integration,loss_fixes,nearkill,pilot,planner2,review_tools}.py`, engine present | exit 0 each; planner2 parity 4000/4000; test_critique 76 checks |
| `test_{critique,loss_fixes,review_tools}.py` with `TNR_ENGINE_APP` pointed at nothing | exit 0 each |
| `test_review_tools.py` in a fresh worktree: no `fights/live`, no engine, no catalog | exit 0, five checks |
| the nine `scripts/test_*.py` | `OK` each |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files, and `--commits origin/main..HEAD`), `git diff --check origin/main HEAD` | exit 0 each; 337 rulings |
| `player_allowlist.py check`, `report --check`, `player_size.py` | exit 0 each |
| `doctrinemap.py`, `render_doctrine.py --check`, `build_packs.py --check`, `lawmap.py` | exit 0 each |

Each new test on e051d062's code: F1's two fail (the attack is planned; the gate allows it); F2's and F3's are
of code that is not there; F4's fails at the first stray path, which is pushed; the Ring test with the fired
line taken out passed there and stops here.

## What is not shown

- **Nothing live**, as before.
- **A fight he starts** while I am hurt: fought, as it must be.
- **Positions against an AI**: not rebuilt.
- **`fable/ai-player-ap4`** (handed off at 2f89e85d, under review) stands on e051d062 and does not have these
  corrections. They are brought into it when its review returns; it is not moved meanwhile.

## Live-game statement

Zero live requests. The engine ran offline at the harness's pin with socket calls denied. `keep`'s tests push
to a bare repository in a temporary folder.

## Not begun

As the first note has it.
