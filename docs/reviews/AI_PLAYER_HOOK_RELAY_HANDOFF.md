# AI player overhaul: the relay's hooks. Implementation handoff

Workflow: `docs/workflows/IMPLEMENTATION_HANDOFF.md`. Written 2026-11-13.

```text
Repository: perseverance484/tnr-tools
Branch: fable/ai-player-hook-relay
Base: 661f3f63f9bd51887c402ce00f76e8e9735cb2ea (fable/ai-player-ap2: AP2's first part, approved on
      chatgpt/review-ai-player-ap2-rereview2 @ 6bf7d297). Not rebased: this head is three commits on it.
Code: 6611ae77 (61193d61, and one commit that takes out a mark nothing needed)
Head: the commit that adds this note (FROZEN; the exact SHA is in the handoff message)
Intended integration: the AI player line, behind AP2's first part. Not `main`, and not before the director says.
Authority: RUL-2026-11-13-157 (run the probe and build the hook relay);
           RUL-2026-11-13-156 (the tokens to save are the ones the plan's limits count)
```

The diff to review is `git diff 661f3f63 HEAD`. Objective: the model in the relay carries neither a call nor
its result, so that what a fight reads costs the relay nothing, and nothing but the brain's own calls can
reach the game through it.

## What it is

A relay is a small model in a loop: it runs `brain next`, makes the calls that prints, and comes back. Each
batch is one model request, and a request carries the relay's whole conversation. So far the model wrote each
call out in full, select and all, and each result landed in its conversation: a full read of a fight is some
15,000 tokens, read again with every batch after it.

Claude Code runs hooks before and after every tool call. The relay's agent now declares four:

| Hook | When | What it does |
|---|---|---|
| `bash` | before a Bash command | lets `brain next` through, exactly as printed, with the relay's own id put behind it; refuses any other command |
| `pre` | before a call of the connector | puts the brain's real call in the place of the stand-in the model sent; refuses anything else |
| `post` | after a call that was answered | hands the result to the brain, and shows the model `ok` |
| `fail` | after a call that failed | hands the error to the brain as that call's result |

A relay whose `brain next` came through the first hook is printed a stand-in for each call:
`{"call":"player.relay","input":{"b":"<the batch's token>","n":1}}`. That is all the model writes, and `ok`
is all it reads. A relay whose `brain next` comes without the id has no hooks, and is printed its calls as
before. Nothing is switched off.

## The probe

Before building, as the director asked: Claude Code 2.1.323, in the session this was built in.
`docs/reviews/evidence/ai_player_hook_relay/PROBE.md` has every step, and `hook_inputs.json` what each hook
was given.

- **One live request**: a read of my own profile's status through the connector. The model sent a stand-in; a
  hook put the read in its place; the connector answered `{"userData.status":"AWAKE"}`; another hook replaced
  what the model was shown with a stub. No gameplay action and no write.
- **Five connector calls were refused by the hook and never made**: a stand-in for a call the batch had not
  got, a second copy of the one that was made, and three that the model had miscopied from a step described
  in words. The model writes `"text relay"` for `relay` when it is told "the text relay"; a batch's lines are
  JSON for that reason, as they always were.
- **Confirmed**: a hook can replace a tool's input and let it through, refuse it, and replace what the model
  sees of the result, for the connector's tool, inside a subagent; `PostToolUse` is given the result and the
  same `tool_use_id` as `PreToolUse`; the subagent's transcript keeps the stand-in and the stub, not the call
  and the result.
- **Not tried**: hooks declared in an agent file. This session did not load a new agent file, so the probe's
  hooks were in the project's settings file. Also not tried: a call that fails, a result too large for the
  conversation, several tool calls in one message, a hook that fails with `onFailure: block`, and anything on
  Duet's machine.

## What it buys

By the plan's count (RUL-156), on the live session's clean stretch: its first relay's 27 batches, the walk to
the fight and rounds 1 to 5. `docs/reviews/evidence/ai_player_hook_relay/estimate.py` makes the table.

| Relay | Born with | The plan's count | a batch | Requests over 100,000 tokens | Context at the end |
|---|---|---|---|---|---|
| as it ran, the session's relay | 118,190 | 4.84M | 179k | 27 of 27 | 398,138 |
| as it ran, a small relay kept for the stretch (what the code does in a fight) | 5,000 | 2.42M | 90k | 10 of 27 | 284,948 |
| as it ran, a small relay replaced past 60,000 (not done inside a fight) | 5,000 | 0.41M | 15k | none | - |
| with hooks, a small relay kept for the stretch | 5,000 | 0.14M | 5k | none | 29,600 |

- **About a third of the best the code could do without hooks**, and that best needs a relay to be replaced
  inside a fight, which it is not. Against what the code does today with a small relay, a seventeenth.
  Against the session, a thirty-fifth.
- **The conversation stays small whatever is read.** Five rounds end at 30,000 tokens, not 285,000. The step
  at 100,000 tokens, where Haiku 5.5 costs five-fold, is not reached in a fight, and a relay need not be
  replaced inside one.
- **What is left is mostly output**: about 100 tokens for a stand-in call, counted five-fold.
- **In my reply to the director I put this at 0.07M.** That was before the probe: I had 250 tokens of output
  a batch, and the probe's requests took about 100 a call. 0.14M is the figure.

It is an estimate. What a stand-in adds and takes is from single requests of the probe, not from a relay's
batch; the script's notes say which figures are measured. The token log now keeps what was read from the
cache and what was written to it apart, and says which batches a relay with hooks carried
(`live/tokens.jsonl`: `cached`, `written`, `hooks`): the first session gives the figure itself.

**Light reads on his turn** (`fable/ai-player-light-polls` @ 27add9fb, frozen, not reviewed) are not in this
line. A relay with hooks has no read in its conversation, so they would save it nothing and cost each turn a
round trip. I recommend holding that review until a relay with hooks has run on Duet's machine.

## What was built

`player/hook.py` (new, 324 lines); `player/relay.py` `lines`, `read_batch`, `put`, `log_tokens`, the number;
`player/brain/client.py` `next_batch`, `_greet`, `_collect`, `put`; `player/brain/__init__.py` `main`;
`player/config.py` `STAND_IN`; `.claude/agents/tnr-relay.md`; `player/RELAY.md` (one sentence).

### Which kind a relay is

- **The Bash hook says so.** It adds `--hooks <id>` to the `brain next` line: the subagent's id, or the
  session's when the relay is the session's main agent. `brain next` keeps the id the relay was named under
  (`live/client.json`, `hooks`).
- **From its first ask to its last.** A relay with hooks whose `brain next` comes without the id, or with
  another, is told to stop. So is a relay without hooks that comes with one.
- **Proved on its first calls.** The hook in front of the connector leaves a mark when it runs. A relay with
  hooks that hands in a batch with calls and no mark is told to stop before it is printed more: what it was
  printed went to the connector as it stood. A stand-in names no endpoint of the game, so nothing reached
  it. Once the mark has been seen the relay is not judged again: a batch the model left out is not a stop.

### What the hook lets through

A stand-in, to the letter: the connector's tool, `endpointName` the stand-in's, `input` exactly `b` and `n`.
Then, in this order, and refused at the first that fails:

1. `live/client.json` is this version's and names a relay with hooks and a batch.
2. The tool call is that relay's: the id is the one it was named under.
3. `b` is the batch that relay holds, and the brain has not taken its results yet.
4. The batch has a call `n`.
5. The run lock's cutoff, which the batch carries, has not come. A cutoff that cannot be read has.
6. Call `n - 1` has been made, and is answered. It is waited for, up to 30 s: Claude Code may start the calls
   of one message together.
7. Call `n` has not been made. Its file is made once, whole, by a link that fails when it exists.

Then the hook spends the wait the batch has in front of call `n`, looks at 1 to 5 again, and gives the real
call: endpoint, input and select, as the brain made them.

- **A refused call is not made.** Nothing reaches the connector, and the model is shown the reason.
- **A call refused before its turn is not used up.** One refused after its wait is: what refused it (the
  cutoff, a batch handed in, a relay replaced) refuses every call behind it as well.
- **A hook that fails refuses.** Whatever goes wrong inside it becomes a refusal, and the agent's two hooks
  that stand in front of a call have `onFailure: block`.
- **Each hook that ran is one line in `live/hook/log.jsonl`**, with the reason for a refusal.

### What the brain gets

- **Each result as `brain put` hands one in.** The hook finds its call by the tool call's id and writes
  `live/inbox/put-<token>-<n>.json`, the file a relay with no readable transcript has always handed in.
  `brain next` takes those for a relay with hooks, whether it finds the transcript or not.
- **In any shape Claude Code gives a result**: a list of text blocks (what the probe saw), a string, an object
  with `content`; and the notice that stands in for a result too large for the conversation, whose file is
  read from under the session's own folder and nowhere else.
- **A failed call is that call's error.** A rate limit is read as one. The model sees the error text, which a
  hook cannot replace.
- **The transcript is read for the tokens only.** It has stand-ins and `ok`: none of it is a result, and none
  of it is a call the batch did not ask for.
- **The results' times are the hook's**, on the brain's own machine.

### The waits

A relay with hooks is printed no wait. The 1.2 s between two actions of a turn, and any wait the budget put in
front of a call, are spent by the hook in front of that call. That is one tool call less for each wait.

### The number is 8

`live/client.json` now says which kind a relay is and keeps the batch's steps and cutoff for the hook, and a
relay with hooks has its calls let through under rules of its own. A file of 7 says none of that. One test
holds `661f3f63` to it with its own package.

### The token log

`relay._usage` kept one sum for fresh input, cache writes and cache reads. The plan does not count them alike
(RUL-156). A batch's row in `live/tokens.jsonl` now has `cached` and `written` beside `in`, and `hooks`. I
listed this as not begun in the handoff of the light reads. It is in because this change is judged by it; it
is ten lines and can come out.

## What did not change

The brain: what it decides, its gates, the budget and the call ledger, receipts, the run lock. What
`brain next` keeps of who holds which batch. A relay without hooks, in every respect, but for the number.

The ledger still holds the batch of a replaced relay until it comes back or the operator says `stopped`. With
hooks that relay's calls are refused from the moment the new one is named, so the hold is longer than it need
be. Making the ledger know that is a change to the most reviewed part of the player, and is not in this one.

## Readings of mine

The director's to change. None is settled by a ruling.

1. **The hook answers "allow".** The next call of the batch the running relay holds goes without a prompt, and
   so does `brain next`. Everything else the relay sends is refused. The relay needed the connector's tool
   allowed before; what is allowed now is narrower.
2. **A batch is cut where the model leaves a call out.** The calls behind it are refused. The brain is used to
   a batch that came back short; it is not used to one made out of order.
3. **The waits are spent in the hook.**
4. **The light reads are held**, not merged and not dropped.
5. **The token log's two new figures** are in this change.
6. **`effort` is not set** on the relay's agent. Haiku 5.5 thinks before it answers, and thinking is output;
   `effort: low` in the agent file may halve what is left. It is one line and wants trying on its own.

## Tests

`player/tests/test_hook_relay.py` (new, 44 tests). The hooks are run the way Claude Code runs them: each is
given the hook's input as the probe recorded it, and gives its answer. `brain next` is the real one, with a
brain made afresh for every request.

- the one command: what is let through, what is refused, an id that cannot be passed on safely;
- what such a relay is printed, and that a relay without hooks is printed what it was;
- what the hook lets through: each rule above, with the game counting what reached it;
- what the brain gets: each shape of result, a failure, a result that is too large, a tool call no hook let
  through;
- a relay whose hooks do not run;
- **the same session played twice** against one stand-in for the game, by a relay without hooks and by one
  with: the game sees the same calls at the same moments, batch for batch, and the brain's world model ends
  the same;
- the agent file: its four commands, each run by a shell as Claude Code runs it;
- the head before, held to its number.

The base has no `player/hook.py`, which the file imports, so none of it can run there.

`test_relay.py`: the agent file's front matter now has the hooks; a batch's token use has the two new figures.

## Verification on the head's parent (the code commit)

| Command | Result |
|---|---|
| `python3 -W ignore::ResourceWarning -m unittest discover -s player/tests -t .` | `Ran 592 tests`, `OK`, three runs in a row, none skipped (`661f3f63`: 548) |
| Fifty-nine planted defects in the code of this change, in throwaway worktrees | below |
| `python3 -m player.tests.test_walk 200 300` | 200 walks, 5,481 calls, no problem: the figures of the base |
| `python3 -m unittest scripts/test_player_allowlist.py scripts/test_player_catalog.py` | `Ran 46 tests`, `OK` |
| `python3 scripts/player_allowlist.py check`, and `report --check` | exit 0, both |
| The four pilot tests (`state/player/dauntless/tools/tests/`) | exit 0 each |
| `rulings_index.py --check`, `check_large_files.py`, `check_no_real_name.py` (files and commits), `git diff --check` | exit 0 each |
| `estimate.py`, on the session's log from `duet/ai-player-ap1-live` @ 112aadbd | exit 0; the table above |
| Two fuzz scripts and three simulated fights of mine, not in the repository | the results of the base |

## Planted defects

Fifty-nine, one at a time, each in a throwaway worktree made from the code commit, never in the
repository's own tree. The whole player suite was run for each. Every one fails at least one test. The
worktrees were clean after the runs and are removed. The unchanged code passes: the three runs of the suite
above.

A first run, of sixty-one on the commit before, let two through. Both were in one thing: a call refused after
its wait was marked refused, so that the calls behind it would not wait for its answer. They never do: what
refuses a call after its wait refuses every call behind it before its turn is looked at. The mark changed
nothing, and is gone (the second commit).

| Planted defect | Tests that fail |
|---|---|
| command: any command is run | 1 fails |
| command: `brain next` may have more behind it | 1 fails |
| command: it may be run from anywhere | 1 fails |
| command: the relay's id is not put behind it | 3 fail, 35 errors |
| command: an id is passed on whatever is in it | 1 fails |
| command: a subagent is known by its session, not by itself | 7 fail |
| command: the id is not taken from the command line | 1 fails |
| command: the id stays among `brain next`'s arguments | 1 fails |
| batch: a relay with hooks is printed the calls themselves | 7 fail, 23 errors |
| batch: a relay without hooks is printed stand-ins | 30 fail, 2 errors |
| batch: a stand-in does not say which batch it is of | 19 fail, 10 errors |
| batch: the stand-ins are numbered from nought | 20 fail, 8 errors |
| batch: the waits are printed to a relay with hooks too | 2 fail, 1 error |
| batch: the steps are not kept for the hook | 21 fail, 10 errors |
| batch: the cutoff is not kept for the hook | 1 fails |
| batch: which kind a relay is, is not kept | 12 fail, 20 errors |
| hook: a call written out by hand is taken for a stand-in | 1 fails |
| hook: a stand-in with more beside it is taken | 1 fails |
| hook: a stand-in whose input has more in it is taken | 1 fails |
| hook: a number in any form is taken for the call's | 1 fails |
| hook: any tool is taken for the connector's | 1 fails |
| hook: another agent's call for this relay's batch goes | 2 fail |
| hook: a call of a batch the relay does not hold goes | 1 fails |
| hook: a call of a batch that was handed in goes | 1 fails |
| hook: a call the batch has not got is looked for | 1 fails |
| hook: the run lock's cutoff is not minded | 2 fail |
| hook: a call at the cutoff goes | 2 fail |
| hook: a cutoff that cannot be read is no cutoff | 1 fails |
| hook: another version's client file is used | 1 fails |
| hook: the calls of a batch are made in any order | 1 fails |
| hook: a call does not wait for the one before it to be answered | 1 fails |
| hook: a call can be made twice | 2 fail |
| hook: the wait in front of a call is not spent | 3 fail |
| hook: a wait is spent again in front of every call behind it | 2 fail |
| hook: after the wait nothing is looked at again | 1 fails |
| hook: the select is left out of the call | 1 fails, 4 errors |
| hook: a hook that fails lets the call go as it stands | 1 fails |
| hook: an input that cannot be read is let through | 1 error |
| hook: nothing is on record of the hook having run | 15 fail, 9 errors |
| hook: what is on record of older batches is kept for ever | 1 fails |
| hook: the log is swept away with the batch | 1 fails |
| hook: nothing is written down of what was refused | 2 fail |
| result: the model is shown the result itself | 16 fail |
| result: any tool call's result is taken for call 1 | 1 fails |
| result: one that came as a dict is not understood | 1 fails |
| result: a failed call's words are read as a result | 1 fails |
| result: a result that cannot be read loses the hook its answer | 1 error |
| result: the hook's results are looked for in the transcript | 1 fails |
| result: its stand-ins are counted as calls nobody asked for | 1 fails |
| result: the results' times are taken for the transcript's | 1 fails |
| result: `brain put` hands a result in for the wrong call | 1 error |
| stop: a relay whose hooks never ran is printed more | 1 fails |
| stop: a relay may come with hooks one time and without the next | 1 fails |
| stop: a relay is judged at every batch, however often its hooks have run | 1 error |
| stop: a relay that has had no call yet is stopped | 12 fail, 20 errors |
| stop: a relay without hooks is judged as one with | 44 fail, 20 errors |
| tokens: what was read from the cache is not kept apart | 2 fail |
| tokens: the log does not say which relay carried a batch | 1 error |
| protocol: the number is still the one before | 1 fails |

## Size

Player code 6,027 lines in 31 files (`661f3f63`: 5,666 in 30); tests 10,993 lines (10,270). The new file,
`hook.py`, is 324 lines. `brain/client.py` is 400 lines (400) and `relay.py` 399 (367). Over the AP6 budget of
400, as before: `activities/battle.py` 685 and `budget.py` 416. Seventeen functions branch more than 12 ways:
the same seventeen, with the same counts. Config constants 52 (51). Nothing ships switched off.

## Source, generated files, and what else changed

- **No game source was read.** No capture was made. The allowlist is untouched: the hook gives the connector
  the calls the brain made, and the stand-in is not an endpoint.
- **`docs/design/AI_PLAYER_OVERHAUL.md`** section 4.7: what is counted (RUL-156, as on the light reads'
  branch), and the relay's hooks.
- **`docs/rulings/2026-11.md`, `docs/RULINGS.md`**: RUL-156, carried over unchanged, and RUL-157.
- **`player/OPERATOR.md`**: "Hooks".
- **`docs/reviews/evidence/ai_player_hook_relay/`**: the probe, what its hooks were given, its script, and
  the estimate.

## Known limits

1. **It has not run on Duet's machine, and hooks in an agent file have not run anywhere.** If they do not
   run there, the relay is one without hooks: it plays as before, at the cost it had, and
   `live/client.json` says so. If only the hook in front of the connector does not run, the relay is stopped
   after its first batch of calls.
2. **`fail` is written from the documentation.** No call failed in the probe.
3. **The model still copies lines.** A stand-in it gets wrong is refused, and the rest of that batch with it:
   the turn waits for the next batch. The probe's model copied JSON without a fault and words with one.
4. **A relay stopped for want of hooks leaves its batch held** until the operator says `stopped`, like any
   relay that ends without handing in. What the connector does with a stand-in that reaches it was not
   tried: it names no endpoint the game has.
5. **Order rests on a wait.** If Claude Code starts a message's calls together, each waits for the one
   before it, 30 s at most. A call whose answer never reaches the hook holds the rest up for that long, and
   then they are refused.
6. **A hook is a process**: about a tenth of a second in front of and behind each call.
7. **`live/hook/log.jsonl` is not trimmed.** One line a hook; some megabytes in a day.
8. **A result the hook cannot hand in is lost**, and the model is still not shown it. The brain treats the
   call as unanswered.
9. **The player needs a POSIX system**, as it did (`fcntl`); the hook adds a hard link.
10. The limits of AP1's and AP2's handoffs stand.

## Live-game statement

One live request, in the probe the director asked for: a read of my own profile's status through the
connector, on 2026-11-13. Nothing else: no gameplay, no write, no credential or session material. The tests
make none.

## Open

- For the director: a first run on Duet's machine (the operator's page, "Hooks", says what to look at); the
  six readings; whether the light reads' branch is dropped.
- From before, unchanged: AP1's live gate and which head it runs on; AP2's three readings; whether the line
  goes to `main`.

## Not begun

AP2's second part; the script that starts short-lived relays; a live run. Also not begun, and not proposed
without the director's word: a ledger that knows a replaced relay with hooks is stopped; `effort: low` on the
relay; one connector call that carries a whole batch, which needs the connector to offer it.
