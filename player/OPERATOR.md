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

- The word is for this one update. It is of no use for a later one, which is listed under another name.
- A batch the last relay from before the update had is listed only once the new relay has asked. List again
  then, and say `stopped all` again: until you do, that batch's calls stay held and the player has less room.
- `stopped TOKEN` or `stopped BATCH` for one old batch lets that batch go and leaves the update's minute held.
- A live folder that is new has no ledger and so no hold. Before the first relay of a new folder, make sure
  nothing from before is running, as at the start of any session.
- An ordinary restart, with the ledger this version kept, has no hold either.
