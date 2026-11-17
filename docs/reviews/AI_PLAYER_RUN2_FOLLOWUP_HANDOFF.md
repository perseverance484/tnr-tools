# AI player, after AP run 2: what the review's open list comes to. Handoff for review

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md`. Written 2026-11-17.

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-run2-followup
Base: main @ 0b52988dec3a018cabae7b3aa36363b82407ca01
Head: the commit that adds this note (FROZEN; the exact SHA is in the handoff message)
Authority: RUL-2026-11-17-165 (the director: "Begin next phases", with a review of AP runs 1 and 2)
Engine: studie-tech/theninjarpg @ df864509f8b33f4c9cf8332fd416ab511d2f0478, the harness's pin
        (harness/pvp_turn/README.md, "Engine version"), offline
```

The review lists seven open items. This is what each came to, what was changed for it, and what was measured.
Nothing here was played: every figure is from committed logs, run 2's own files, or the game's combat code run
offline at the harness's pin.

## What the open list came to

| | The review's item | What it is | Changed here |
|---|---|---|---|
| 1 | Token cost, about 27.5k a batch against the proof's 4.2 to 4.4k | **A counting error.** Counted once, run 2 cost 4,930 a batch | `player/tokens.py`, `brain tokens` |
| 2 | Review the two losses; fix the `postmortem.py` crash on losses | The crash was the missing engine, not the losses. Both are reviewed, in the engine | `postmortem.py`; the two reviews |
| 3 | The critique terms are off; `tune_real` never run | Run, twelve fights under both: no gain shown. They stay off | nothing |
| 4 | `turn.py` ranks danse+aetherion over danse+resist on round 8; no death check | Reproduced. planner2 on the same position has a fault of its own | a setting in planner2, default as before |
| 5 | `critique.py` stops on AI-opponent logs | Fixed | `critique.py`, `postmortem.py` |
| 6 | Not modelled: keeping the enemy on our floor | Not begun | nothing |
| 7 | Worst-case reply check: offered, not decided | The director's to decide; see "Open" | nothing |

Two more that the work turned up: the kits run 2 saved of its opponents never reached `main`, and the heal line
did not meet the director's rule.

## 1. Tokens

`ops/ap_model_session/scripts/token_report.py` (on the run's branch, not on `main`) computes
`0.1 x cached + 1.25 x written + in + 5 x out`. Its own header says it assumes `in` is fresh input and asks for
one line to be checked by hand. `in` is the batch's whole input: `player/relay.py`, `_usage`, adds what was
read from the cache and what was written to it into it. So the conversation is in the sum twice. The proof's
own reader subtracts them (`proof_read.py`, line 149), which is what PROOF.md defines.

Run 2's 390 rows (`ops/ap_model_session/run2/tokens.jsonl` on the run's branch), counted once:

| | As the run reported | Counted once |
|---|---|---|
| A batch | 27,514 | **4,930** |
| A batch in a fight (222) | 34,913 | 5,475 |
| A batch out of one (168) | | 4,210 |

A batch is made of: 2,190 read from the cache (the conversation's mean size was 19,123), 853 written, 1,885
output. The proof said 4,200 to 4,400 a batch for a main agent and 3,500 to 3,630 for a subagent born at 4,090;
run 2's relays were born at 6,162. So run 2 is about 15% over the proof's main-agent figure, not six times.

What is left to gain, from the same rows:

- **Fights on one relay.** Twelve relays carried 16 to 71 batches; a relay is not replaced in a fight, and one
  grew to 50,805. Had every relay been replaced at 20 batches, fights included: about 4,080 a batch (17% less).
  At 10: about 3,840. That needs replacing a relay inside a fight, which is not built.
- **One message a batch.** 67 batches of 390 took more than one request: 6,771 each against 4,548.
- **Output** is 38% of a batch: about 110 tokens for `brain next` and 100 for each call.

**Not measured, and likely the larger number:** the session that starts each relay. Its tokens are in no file of
the run. Every replacement is a turn of that session on its own model with its own conversation.

I cannot check run 1's figure (7,698 a batch): its rows are not in the repository.

## 2. The two losses, in the engine

`postmortem.py` fires each turn's alternatives in the engine. Run 2 ran where there is no engine app; the bridge
gives no answer there and the review ended in `IndexError` on the first turn. It now reviews what it can and says
what was not measured. The engine can be had in a cloud container in about three minutes (below), so both
losses are reviewed in full: `state/player/dauntless/fights/postmortems/`.

| | Shisui (fight 6, lost in round 13) | Selaphiel (fight 8, lost in round 11) |
|---|---|---|
| Turns of mine reviewed | 12 | 10 |
| Where it turned, against what he actually did | R9: Clear + Aetherion instead of Clear + Phantom Step, +524 HP | R9: Rebirth + Colored Jewel + Replacement instead of Rebirth + basic attack + Defensive Stance, +1,007; R8, +817 |
| Regret, all turns added | 1,502 | 3,119 |
| Turns where the planner gave his actual turn under 10% | 11 of 12 | 8 of 10 |
| Turns where the planner's damage was over 5% off the log | 6 | 2 |
| The replay review's findings | 6 | 4 |

Both were reviewed with the opponent's kit present (section 5) and the planner as it is on this head.

What they show:

- **No single turn lost either fight.** The largest regret is 524 and 1,007 HP. Added up they come to about what
  he had left at the end (1,400 and 2,060), but that sum has the hindsight of every reply and takes each turn
  alone: it is a ceiling, not what was on the table.
- **The planner did not see either of them coming.** It was the first fight against each, so there was no model
  of him to read: his actual turn was given under 10% on 19 of 22 turns.
- **The planner's damage figures run high** against these two: Shisui R2 331 against 236 logged, R5 628 against
  448, R12 790 against 562 (31 to 41% over); Selaphiel R3 293 against 220. The engine was within 6% of the log
  on each. That is AP4's fifth step (accuracy), not a weight.
- **Today's planner would not have done better, by this measure.** Asked for its pick on each turn, it chooses
  what was played on 5 of 22. Over the 17 turns where both could be fired, its picks end 815 HP behind what was
  played against Shisui and 809 behind against Selaphiel. The measure is one exchange deep: it gives a buff no
  credit for the rounds after. It does not say the planner is wrong to set up; it cannot see it.

The replay review's findings on both (ten in all): four bursts without Aetherion, two Phantom Steps onto his
ground, two basic attacks with the kunai ready, one pair of buffs into his ready Clear, one late stance. The
kunai, ground and stance ones are what pull request 125 changed.

## 3. The critique terms: `tune_real`, off against on

Twelve logged fights reviewed under both settings, each of my turns fired in the engine and answered by what he
actually played next. Mean of my HP less his after the exchange:

| | Turns measured | The planner's pick | What was played | The pick is the best of the set |
|---|---|---|---|---|
| `TNR_CRITIQUE=0` | 51 | +574 | +639 | 19 of 51 |
| `TNR_CRITIQUE=1` | 47 | +593 | +665 | 13 of 47 |

The terms changed the pick on 21 of 66 turns. Over the 47 turns measured under both, the pick averages +576
with them off and +593 with them on: 17 HP apart, on swings that differ by hundreds from one turn to the next,
and the pick is the best of its set less often with them on. That does not show they help. By the rule already
written in `critique.py` (they ship when `tune_real` says they help) **they stay off.**

Either way the pick is 70 to 90 HP a turn behind what was played. It is the same one-exchange measure as in
section 2, with the same blind spot, and it is the first time it has been taken. (These runs were made while
the planner's desperate-position order was the "off" setting of section 4; both rows are on the same code.)

## 4. Round 8 against DDXXD

Rebuilt from the fight's log (`tools/tests/ddxxd_r8.txt`; the playbook's re-run was on the live read):

- `turn.py`, the fallback, puts Danse Macabre + Aetherion first at +4609 and Danse + Chakra Resistance nowhere
  in its eight. As the review says. **Not changed:** the brief's AP4 step 1 leaves one planner, and `turn.py` is
  reached only when planner2 fails or runs out of time.
- **planner2 has a fault here of its own.** Every line loses, so `rank()` puts the lines that live best first
  (Thunder's Judgement + Basic Heal, 67% dead, 788 off him). Then the lookahead sorts its candidates again and
  Basic Heal + Chakra Resistance is fired: 99% dead, 16 damage. The lookahead is on in every live fight.

I first made the lookahead leave such an order alone. The simulator said no: over 94 simulated fights the lookahead as it was won 90, and
  with nothing reordered 88. Then four fights a cell against the nine opponents where it could matter, 72
  fights under each setting: `all` 60 wins, `alive` 58, `off` 57. The lookahead puts a hopeless line first on
  round 8, and it also finds ways out of positions the one-turn score calls lost.
So it is a setting, `TNR_DESPERATE_LA` (`all`, `alive`, `off`), and **the default is `all`: no fight is played
differently.** Which is right is for the simulator and `tune_real` to say.

## 5. Also found

- **Run 2's opponent kits never reached `main`.** The tools save what an opponent has equipped before the
  fight; `player/keep.py` pushed the fight's own files and not that. Six kits are on the run's branch only.
  `keep` now pushes the kit of each player a fight's log names, and refuses any other. The six are brought over.
- **A check that held only while a kit was missing.** `tests/test_critique.py` asked that every Phantom Step
  and Replacement in planner2's top twelve on Mamba's round 5 land off his ground. With his kit present a
  Replacement onto it, for a basic attack, is fifth, priced with the ground's -20%. The check now asks where the
  planner goes: the first such line and the move that is fired. Any saved kit can move a planner fixture.
- **The heal line.** The director's rule in the review: never start a fight missing HP. The Full Potion was
  used under 95%. `config.HEAL_BELOW` is 1.0 (RUL-2026-11-17-165).
- **The engine in a cloud container.** The game's repository is public. A clone, `git archive <pin> app`,
  `bun install --frozen-lockfile --ignore-scripts` (639 packages), the path into `harness/pvp_turn/.engine_app`:
  about three minutes. The harness runs it with socket calls denied. `tune_real`, the post-mortems and
  `engine_check` then run there.

## Changed

| Commit | What |
|---|---|
| `d9b4627c` | `critique.opponent_of`; `postmortem.swings`; a fight against an AI is read, a loss is reviewed with no engine |
| `f8e12fe5` | `player/tokens.py`; `python3 -m player.brain tokens`; `plan_last_hour` in the status file |
| `ec993c47`, `cd96487f` | planner2: `P.desperate`, `TNR_DESPERATE_LA`; `tests/ddxxd_r8.txt` |
| `5188994a` | `config.HEAL_BELOW` 1.0 |
| `63bd74a2` | RUL-2026-11-17-165 |
| `fc4830c8` | `keep.py` pushes the opponents' kits; run 2's six kits |
| `ee92b961` | `tests/test_critique.py`: the Ring check |
| this one | the two post-mortems, this note |

`ec993c47` is corrected by `cd96487f`; together they change no default. The protocol number stays 10: nothing a
relay is printed or runs is changed.

## Verification

On the head before this note (`ee92b961`), with the note and the two reviews in the tree:

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 681 tests`, `OK` (`main`: 675) |
| `python3 -m unittest docs/reviews/evidence/ai_player_hook_relay/test_preflight.py` | `Ran 44 tests`, `OK` |
| `python3 docs/reviews/evidence/ai_player_hook_relay/fake_connector.py --selftest` | exit 0 |
| `tools/tests/test_{critique,integration,loss_fixes,nearkill,pilot,planner2,review_tools}.py`, engine present | exit 0 each; planner2 parity 4000/4000 |
| `test_{critique,loss_fixes,review_tools}.py` with `TNR_ENGINE_APP` pointed at nothing | exit 0 each |
| the nine `scripts/test_*.py` | `OK` each |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files, and `--commits origin/main..HEAD`), `git diff --check origin/main HEAD` | exit 0 each; 337 rulings |
| `player_allowlist.py check`, `report --check`, `player_size.py` | exit 0 each |
| `doctrinemap.py`, `render_doctrine.py --check`, `build_packs.py --check`, `lawmap.py` | exit 0 each |

Each new test was run on the code before its change and fails there: the review tools' four, the planner's
setting, the heal line's two, the kit's one.

Measured, not gated (figures above): both post-mortems; `tune_real --fights 12` under both settings; the
simulator, 94 fights before and after the first planner change and 72 under each of the three settings.

## What is not shown

- **Nothing live.** No relay, no connector call, no run lock. `brain tokens` was run on a copy of run 2's file.
- **The operator session's tokens**, as above.
- **The reviews against an AI** use rules written for a player ("his ready Clear"). They run now; whether each
  rule fits an AI was not looked at.
- **A heal that changed nothing** is still not tried again for ten minutes, and the hunt goes on meanwhile. So
  "never" holds while the potion works.
- **The simulator is kind** (run 2's own analysis says so: it wins Shisui every time, and we lost).

## Live-game statement

Zero live requests. The engine ran offline at the harness's pin with socket calls denied. The game's public
repository was cloned to read and to export that pin; nothing was sent to it.

## Open, for the director

In the handoff message.

## Not begun

The move atlas and the rest of AP4. AP3. Keeping the enemy on our ground. Replacing a relay inside a fight.
