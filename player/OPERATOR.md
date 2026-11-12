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
an older version.

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

## What it does

The held calls are counted from the moment you spoke, and leave the minute sixty seconds after that. So room
comes back a minute later, not at once. The brain hears of your word with the relay's next `brain next`, and
writes a `setting_changed` event when it has applied it.
