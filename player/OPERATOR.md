# Operating the player: what the operator does about relays

For whoever runs a play session and starts the relay (Duet). The relay's own instructions are `player/RELAY.md`;
this page is about the one thing the brain cannot know by itself, and takes on the operator's word.

## Calls that are held

The game allows 30 calls a minute for the whole account. The brain counts every call it prints to a relay.

When a relay is replaced while it still has a batch, the brain cannot tell whether that relay will go on and
make those calls. So it **holds** them: they take their places in every minute, for as long as it takes, until
one of two things happens.

- The replaced relay comes back (it runs its last `brain next` and is told to stop). Nothing to do.
- You say that relay has been stopped.

The same happens to a batch that nothing on record says who has: after the client's file was lost, or left by
an older version. And after the player's code is updated a whole minute's calls are held, whatever the old
ledger says: see the last section.

## What it looks like

- `live/status.json`, `budget.held`: one line per held batch, with the relay's token (or nothing, when it is not
  on record), the batch's id, how many calls, and since when.
- `live/events.jsonl`: a finding when a batch goes loose; a stall when it has been held for 15 minutes; a stall
  each time a call is not sent because held calls leave no room.
- The player itself: fewer reads of a fight first, then calls that are not sent at all. With the minute full of
  held calls nothing goes out, and the relay is made to wait six seconds between asks.

## What to do

```text
python3 -m player.brain stopped              list what is held; changes nothing
python3 -m player.brain stopped TOKEN        that relay has been stopped (the token is in status.json)
python3 -m player.brain stopped BATCH        the same, by the batch's id: for one with no relay to its name
python3 -m player.brain stopped all          every relay but the one that is running has been stopped
```

**Say it only when it is true.** "Stopped" means that relay cannot make another call: you ended its agent and
saw it end, or the session it ran in is gone. A relay that has gone quiet is not stopped. If you say it of a
relay that is still running, its calls go uncounted and the account can pass 30 a minute.

- When you replace a relay: end the old one first if you can, start the new one, then `stopped TOKEN`.
- At the start of a session, when no relay from before can be running: `stopped all`.
- `all` covers exactly what is held at the moment you say it. A relay that is replaced later is not covered:
  say it again then.
- What is held is read from what the brain last saved. If a batch you expect is not listed yet, let the relay
  ask once more and list again.

## What it does

The held calls are counted from the moment you spoke, and leave the minute sixty seconds after that. So room
comes back a minute later, not at once. The brain hears of your word with the relay's next `brain next`, and
writes a `setting_changed` event when it has applied it.

A held batch holds more than its calls, until the brain has read behind it:

- **What it may have cost.** The ryo of its purchases stays reserved against the day's allowance until a
  profile read that was asked for after the batch was over. Until then the player buys less, never more.
- **What it may have equipped.** If it selected a loadout or swapped a weapon in, the hunt, restock and repair
  wait until my items have been read after it was over. While such a batch is held, the player reads my items
  every half minute and does not hunt. Ending that relay and saying `stopped` is what gets the hunt going.

## The pocket

The pocket holds at most 200,000 ryo on the road (RUL-2026-11-12-153). With more in it the player starts no
trip by choice: training does not set off for the village, a session's end does not set off for home, the hunt
stays in its sector. The bank's deposit is what brings it down. **This holds with the bank activity switched
off as well.** Then nothing brings the pocket down, the player stays where it is, and a session's end waits
with a note that says so. Bank by hand, or switch the bank back on.

## The run lock

One runner at a time may write to the game on this account (`docs/workflows/FORGE_MCP_RUNNER.md`). The lock is
`state/run_lock.json` on `main`. **The brain holds it for a play session; you do not claim it for the brain.**

- A play session runs on the account's own live folder (`state/player/<account>/live`), from a checkout that can
  push to `main` (the lock tool, `forge/tools/run_lock.mjs`, makes one commit a write) and has `node`.
- The brain claims the lock as `player`, job `play session`, before its first call. Until it has the lock it
  sends nothing, and the relay is told to ask again. `live/status.json`, `run_lock`, says `held` and until
  when, or `not held` and why; a stall is written when another runner has it.
- It renews the claim every 15 minutes. If the lock is taken from it, it stops sending at once. If a renewal
  cannot be pushed, it plays on until a minute before the lease ends, then stops.
- That last minute is kept clear of calls by when they are made, not by when they are planned. The brain puts
  no call in a batch that is due in it. `brain next` prints nothing of a batch whose last call, after the
  waits inside the batch, would fall in it: not when the relay was slow to wake, not when the batch waited
  through a crash, not when it is given again after one. The relay is sent straight back and the brain decides
  afresh.
- **The relay's part** is what it always is: the calls of a batch at once and in order, with the waits the
  batch carries. The last minute of the lease is its time to finish a batch it got just before. A relay that
  sits on a printed batch for longer than that is making calls outside the lock: end it, and say `stopped`.
- It gives the lock back when the session has ended and the character is asleep, and when you pause the player
  outside a fight. A brain that dies holds the lock until its lease runs out, an hour at most:
  `node forge/tools/run_lock.mjs status` shows it.
- If you hold the lock yourself as `player` (a job run by hand), release it before the session: the brain's
  claim is refused while anyone holds the lock, whatever the label.
- With `TNR_PLAYER_LIVE` pointing anywhere else the brain is a rehearsal: it claims nothing, and
  `status.json` says so. **Never give a rehearsal a relay that can reach the game.**

## Hooks

The relay's agent (`.claude/agents/tnr-relay.md`) declares four hooks (`player/hook.py`; what they keep of a
batch is in `player/hooked.py`). With them the model in the relay is printed a stand-in for each call, a hook
puts the real call in, and another takes the result out and hands it to the brain. The model's conversation
then holds no call and no result, which is most of what a relay costs (RUL-2026-11-13-156,
RUL-2026-11-13-157).

- **Before the first session on a machine.** Claude Code 2.1.295 or later. Start the relay from the
  repository's root, in a folder whose trust dialog you have accepted: until then Claude Code runs the agent
  and skips its hooks. If the connector's tool has another name there than `mcp__Tnr__callEndpoint`, put that
  name on the agent's `tools:` line.
- **Then check it, before a live session** (RUL-2026-11-14-160). From the repository's root on that machine, in
  a terminal of your own and not from inside a Claude session, at a head whose review has passed the check
  itself:
  `python3 docs/reviews/evidence/ai_player_hook_relay/preflight.py`. It starts the relay against a stand-in for
  the connector, once as a session's main agent and once as a subagent, for three reads of my own profile each.
  It says for each whether the agent file's hooks ran for every call, and ends with 0 when they did. Do not
  start a live session while it says no. It is built to make no request of the game: its sessions are given
  the stand-in as their only MCP server, and a gate in front of every call lets nothing through but those
  reads. If it ever says that a call was answered and not by the stand-in, tell the director: that would have
  been a read of my profile from the game, where none is allowed.
- **Which kind a relay is.** `live/client.json`, `hooks`: the relay's id, or nothing. `live/tokens.jsonl`,
  `hooks`: true for a batch such a relay carried; `cached` and `written` there are what the plan counts by.
  `live/hook/log.jsonl`: every hook that ran, and why a call was refused or a result was not handed in.
- **A relay without hooks plays as before**, and costs what it did. That is what you get when the hooks do
  not run at all: the brain is not told otherwise, and prints the calls themselves. Do not rely on it: on
  Claude Code 2.1.325 such a relay stopped itself in 7 sessions of 17 against the stand-in
  (`docs/reviews/evidence/ai_player_hook_relay/PROOF.md`, "A relay without hooks").
- **`STOP the relay's hooks are not running`.** The relay's `brain next` came through its hook, so it was
  printed stand-ins; but no hook ran in front of its connector calls, or its `brain next` came back without
  the hook, or with the id and no hook in front of it (run by hand). Nothing it was printed reached the game:
  a stand-in names no endpoint. The usual cause is the tool's name (above). End that relay, say `stopped` for
  the batch it had, and start one when the cause is found.
- **What the hook refuses** is not made: a call that is not a line of the batch the relay holds, a second
  copy of one, a call whose line before it was left out or refused, a call after the run lock's cutoff, a
  call of a batch the relay has come to hand in, a call of a relay that was replaced. So a replaced relay
  with hooks makes no call from the moment the new one is named. The ledger still holds its batch until it
  comes back or you say `stopped`: the word is as cheap as before, and now it is true sooner.
- **`brain next` may take two minutes to start.** Its hook first waits for every call of the batch that went
  to the connector and has not come back, 120 seconds at most, and 2 seconds for a line the relay left out.
- **A call that is still out after that.** The brain is told that call has no answer, and reads again. Its
  batch is not over: the brain holds the batch's calls against every minute and keeps what they may cost
  reserved, as for a relay that did not hand its batch in, and the event says so in those words though the
  relay is running. When the call's result comes, the batch is over as of then, by itself. If it never comes,
  `brain stopped` lists the batch under its token: say it stopped once you know that call is not on its way
  any more. The same holds for a replaced relay that came back while a call of its was out.
- **`live/hook/late/`** holds results that could not go to the inbox: for a batch that was closed by then,
  for one whose relay had been replaced, or because the inbox could not be written. One that is there when
  its batch is handed in goes with it. The others the brain does not take, as it takes no late result from a
  relay without hooks; what they are good for is the word that their batch is over. They are there for you to
  read, and go an hour after their batch is over. A result the hook could not write down anywhere is left in
  the relay's conversation; `brain next` looks for it in the relay's transcript each time it comes.
  `live/hook/log.jsonl` says "could not be written down" when that happened, which means the disk.
- **A relay with hooks runs one command**, `brain next`. Its hook refuses every other, `brain stopped` and
  `brain set` among them: those are yours.

## After the player's code is updated

The call ledger a version before this one kept cannot be trusted to say everything that is out. That version
may have let calls go that its relays can still make; an older one did so after fifteen minutes. So when this
version takes such a ledger over it sends **no call at all** until you have said that every relay from before
the update is stopped, and none for a minute after you said it.

Do these in this order.

1. **End the brain that was running.** `pkill -f "player.brain run"`, then `pgrep -f "player.brain run"` must
   print nothing. While a brain from before the update runs, it keeps the ledger by its own rules, and this
   version's relay gets no answer at all.
2. **End every relay from before the update, and see each one end.** A relay from before that asks again is
   told to stop: the player uses nothing an earlier version left for a relay, not its name, not a batch that
   was waiting, not word that was waiting for the brain.
3. **Say so.** `python3 -m player.brain stopped` lists what is held. After an update the list has a line
   `the relays from before the update (update-…)`: that is the minute held for what the old ledger may not
   say, 30 calls. `python3 -m player.brain stopped all` lets it go, with every other batch that is listed.
   If you had said `stopped` just before the update, say it again.
4. **Start a new relay.** Its first calls come a minute after your word, not before.

Steps 3 and 4 can change places: a relay started first gets no call, only the line to ask again, until a
minute after you have spoken.

**Say it only when it is true**, here more than anywhere. Nothing in the ledger stands behind this hold: if a
relay from before the update is still running when you say it, its calls are counted by nobody.

- The word is for this one update. It is of no use for a later one, which is listed under another name, also
  when the file that is taken over then is the same as before, byte for byte.
- If the list says `the relays from before the update (a brain is saving the takeover: say it again in a
  moment)`, nothing was taken down for it: a brain is in the middle of writing what it took over, or could not
  write it yet. Say `stopped all` again a moment later; the line then has the hold's own `update-…` name.
- A batch the last relay from before the update had is listed only once the new relay has asked. List again
  then, and say `stopped all` again: until you do, that batch's calls stay held and the player has less room.
- `stopped TOKEN` or `stopped BATCH` for one old batch lets that batch go and leaves the update's minute held.
- A live folder that is new has no ledger and so no hold. Before the first relay of a new folder, make sure
  nothing from before is running, as at the start of any session.
- An ordinary restart, with the ledger this version kept, has no hold either.
