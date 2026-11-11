# AI player overhaul, phase AP1: what the live session showed, and the fixes

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md`. Written 2026-11-12, in answer to the director's "AP1 live
session review" (the session of 2026-11-11).

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-ap1-live (new)
Base: fable/ai-player-ap1 @ 39f30ead2b23575fa9bac1ebe85c6d1873ce3808 (the correction handoff; frozen, not moved)
Head: the commit that adds this note (FROZEN; the exact SHA is in the handoff message)
Evidence: duet/ai-player-ap1-live @ 112aadbd (status, events, turns, tokens of the session); the two fights' logs
          and round archives on fable/pilot-planner-fixes @ e14317c5. Read only; neither branch was touched.
The session ran on 583fe353: before the independent review's corrections (39f30ead), not after.
```

## What the session showed, and where each thing stands

| # | In the session | Cause | State |
|---|---|---|---|
| 1 | Four "fight ends" in a fight that was still on; four potions sent into it | A battle read came back without the battle and was taken for a deleted battle (the pilot's rule, ported). The fight was closed, reopened from nothing, and the Full Potion went out each time | **Fixed here** |
| 2 | Every battle-log read dropped from round 6 on | The log's effect-text column leaves out a line that has no effect, so it was one short; the whole read was thrown away | **Fixed here** |
| 3 | "Late turn": round 6 at 31.6 s | The turn's first actions went out at once. It was still my turn after two plans; past T+15 s the planner was given no time, and the stand-in stance went at T+24.5 s and T+31.6 s. The log showed the last send as the turn's time | **Fixed here** |
| 4 | Defensive Stance sent four times though refused | No check of refusals on the stand-in path (review finding 3, fixed in 39f30ead). 39f30ead still resent it when the refusal was not the one text it knew | **Fixed here** for any text |
| 5 | Rematch round 1 unplayed | `end_session` stopped the relay with the character awake at 648 HP in an enemy sector; DDX attacked with nothing running | **Fixed here**: a session ends asleep at home |
| 6 | "0 missed turns" for a fight joined in round 2 | The brain only counted turns it saw | **Fixed here**: rounds already over with no action of mine are counted apart and named in the fight's end event |
| 7 | "Full Potion used" five times, one real | Events written when a call was planned | Fixed in 39f30ead (review finding 9) |
| 8 | 118,190 tokens at the relay's birth; about 940k per fight turn; a stall at 383k | See "Tokens" | **Not fixed.** One part is prepared here; the rest needs the director's decisions |

The rematch's saved log (`_aywoLPbYrckMVSGZFLwn_entries.json`) shows one line of mine in round 1, `wait`, and two
real actions of mine in each of rounds 2 and 3. So the game writes `wait` for a turn that timed out, round 1 is
the one unplayed round, and round 2 was played by AP1. A `wait` line is therefore no longer taken as proof of an
action (`battle.py` `_turn_over`, `_joined`).

What is still not known: what the empty battle reads actually held, why the log first went ragged in round 6, and
the game's exact refusal texts. The relay transcripts hold all three, and they are on Duet's machine, not in the
session's files. From now on the brain writes each of them down itself (findings `about: read`, `selects`,
`refusal`).

## The fixes

1. **A read without the battle never ends a fight** (`battle.py` `_without_the_battle`, `_plainer`, `_proof`,
   `_profile`). A fight ends when a read shows a fighter down, or when my profile has left the battle. After such a
   read the next one is plain and my profile is asked beside it, until it answers; the budget cannot leave that
   read out. On my turn the plan goes from the last good read meanwhile. The fight keeps its state.
2. **The log survives a short column** (`calls.py` `log_rows`, `entries(whole=)`; `battle.py` `_log`). Who did what
   in which round always lines up and is always kept. When the texts do not line up, the lines are kept without
   them and the fight's later log reads ask for each line's effects whole, which fills them in.
3. **A turn's later plans get planner time** (`battle.py` `_my_turn`): what is left of the turn, less 8 s, at
   least 3 s. `turns.jsonl` now has `fired_after` (the first plan), `last_fired_after` and `plans`; the 20 s rule
   is judged on the first plan.
4. **Any refusal is honoured** (`battle.py` `_refusal`). "Not valid anymore" bans the action for the fight, as in
   the pilot; any other reason bans it for the turn. Each new reason is written down once. A stand-in action the
   game took without effect is not sent again either.
5. **A session ends asleep at home** (`activities/session.py`, `brain.py` `_stop`, `pvp_hunt.py`). With
   `end_session` set the hunt stops, recovery still heals, the character goes home and sleeps, and only then is
   the relay told to stop. A fight on the way is fought.
6. **Rounds nobody played** (`battle.py` `_joined`): `turns_unseen` in `status.json`, `unseen_rounds` in the
   `fight_end` event. Kept apart from missed turns: the log alone cannot say why I did not act.

`player/tests/test_live.py` (20 tests): one class per defect, and a replay of the shape of the session's first
fight: eleven rounds, a relay that takes 7 to 13 s a batch, empty reads, a short log column from round 6. On
39f30ead, 15 of the 20 fail; the other five are controls.

## Tokens

Measured from the session's `tokens.jsonl` (69 batches):

- **Nothing is resent by the brain.** The brain is code and uses no tokens. Every batch is one model request by
  the relay, and a request carries the relay's whole conversation. So a batch costs the relay's context size.
- **The relay was born with 118,190 tokens.** That is not the relay prompt (294 words). It is what a
  general-purpose agent starts with in Duet's environment: the Claude Code system prompt, every tool and connector
  definition, and CLAUDE.md. A general-purpose Haiku agent in this cloud session starts at 65k; a headless Haiku
  with its own system prompt and only Bash starts at 3,146 (both measured here).
- **Each poll of the fight added about 14k** (median; up to 19k): the whole effect list, the ground columns and
  the log, every few seconds on his turn too. They stay in the conversation, so the cost grows with the square of
  the fight's length. Relay 1 went from 118k to 383k in 27 batches. Haiku 5.5's window is 1M, so that was not a
  full window: a 383k prompt is simply slow, and requests over 100k tokens cost more per token.

The same 69 batches, recomputed:

| Case | Session total | Per fight turn |
|---|---|---|
| A. As it ran (118k at birth, a full read on every poll) | 15.9M | 1,001k |
| B. Born at 5k | 7.1M | 478k |
| C. B, and light polls on his turn | 3.6M | 235k |
| D. C, and a fresh relay every round | 1.1M | 61k |

So a small birth context alone halves the cost; the rest comes from what accumulates. Case D needs relays that
are restarted by a script, because a restart by Duet costs Duet's own tokens.

Prepared here for case B: `.claude/agents/tnr-relay.md`, the relay prompt as an agent of its own with two tools
(Bash and the connector's `callEndpoint`) and no CLAUDE.md. **Untested**: a first agent file needs a session
restart to be seen, and the connector tool's name on Duet's machine may differ from `mcp__Tnr__callEndpoint`. The
first `context` in `tokens.jsonl` shows what it achieves.

## Decisions for the director

1. **Light polls on his turn (case C).** His turn would be watched with a five-field read; the full state would be
   read once, when my turn starts. This undoes "every poll is a full read", a rule the pilot got after a turn was
   lost to a refused second read. AP1 has what the pilot lacked then: at T+12 s it plans from the last good read.
   The cost is one extra round trip at the start of each of my turns. The approved design (section 4.7) already
   says the effect list is read whole only on my turn.
2. **Short-lived relays (case D).** A loop script that starts a headless Haiku relay, lets it run a few batches and
   starts the next. It needs the TNR connector in headless mode on Duet's machine, which I cannot test here (this
   container's headless mode has no connectors).
3. **His turn's opening state in the archive.** It is read right after my actions, only for the archive. It costs
   about one full read of context per round. Keep it, or archive my turn's opening state only.
4. Still open from the correction handoff: the wording of "never paced"; End Turn as the last resort.

## Verification on the head's parent (the code commit)

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 224 tests`, `OK`, three runs in a row |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 46 tests`, `OK` |
| `python3 scripts/player_allowlist.py check`, and `report --check` | exit 0, both |
| The four pilot tests | exit 0 each |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` | exit 0 each |
| `test_live.py` on 39f30ead (a throwaway worktree) | 15 of 20 fail or error |

## Size

Player code 3,140 lines in 19 files (39f30ead: 3,030); tests 3,280 lines. `battle.py` is 545 lines (AP6 budget
400) and `_my_turn` branches 18 ways (budget 12). Ten functions are over 12. `battle.py` should be split before
AP2; I did not split it inside a fix. Config constants unchanged (47). Nothing ships switched off.

## Known limits

1. Everything here is proven on tests and a simulated replay, not on the game. The empty reads, the short column
   and the refusals are modelled from the session's symptoms, not from their text.
2. Sleeping at home uses the same call as waking (`home.toggleSleep`), as the pilot does. Not sent live by the
   brain yet.
3. The archive rows of rounds whose my-turn full read failed are still missing (the session lost rounds 8 to 10).
4. The token work is not done: at 39f30ead and here the relay still reads the full state on every poll.

## Live-game statement

Zero live requests: no connector call, no gameplay, no credential. Two headless Haiku runs were made in this
container to measure starting context ("Reply with the single word ok"); they had no connector and called nothing.

Not begun: AP2. No live run is proposed until the director has ruled on the token decisions and the fixes here
and in 39f30ead are verified.
