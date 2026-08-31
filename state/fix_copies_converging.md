# Copies, Not Thefts - converging menus: analysis and fix

Built and validated: `push/33_copies_converging_fix.json`, **0 errors, no skipPreflight**.
This record has failed validation on every manifest that touched it since the icon swap;
this is what was wrong and what changed.

## The three failures

`validate.py` and the builder preflight both reject on a1, a2 and f1.

| node | menu | went to | verdict |
|---|---|---|---|
| a1 | "Who bought them?" / "Why is ANBU not handling this openly?" | both `a2` | converges - every option the same |
| a2 | "Understood." / "And if the door is watched?" | both `a3` | converges - every option the same |
| f1 | autumn index / year index / "whichever the Kage's office uses" | `f2`, `f3`, `f3` | two options share a target |

a1 and a2 are the worse pair. The player is offered a real question, asks it, and gets the
speech she was going to give anyway. f1 is subtler: it looks like a three-way skill check
on the season-versus-year detail planted in a2, but two of the three doors are the same door.

## What changed

Four new dialog nodes, each cloning its neighbour's full field set so scene character,
background and the other 35 keys stay consistent with the scene it sits in.

**a1b** - answers "Who bought them?"

> *She does not answer straight away.*
>
> "A private archive does not buy anything. It stores, and it sells access. Whoever paid is
> a line in their ledger, which is why I want the ledger and not the archivist."

**a1c** - answers "Why is ANBU not handling this openly?"

> *She lets the question sit longer than it deserves.*
>
> "Openly means a village that knows its letters were read. That is a different problem than
> the one I have tonight."
>
> "And four people sent openly are four people who can be counted."

**a2b** - answers "And if the door is watched?"

> "Then it is watched by men paid to watch a door, not by men paid to expect you."
>
> *She does not look up from the map.*
>
> "Come back out the way you find it. If that means the front, use the front."

**f4** - the third front-door answer, which was sharing f3's ejection

> *The clerk's pen stops.*
>
> "The Kage's office does not hold an account here."
>
> He says it politely, and he says it loudly enough for the two men by the stair. The writ
> does not come back to you, and neither does the conversation.

f4 exits to `l1` (the roof route) like f3 does, but it earns its own text: naming the Kage's
office to a neutral archive is a different mistake than asking for a year, and a worse one.
Asking for a year marks you an outsider. Naming your employer tells them who sent you.

`a2` keeps "Understood." going straight to `a3` - a menu passes the check as long as its
options are not all the same, so the neutral option does not need a node of its own.

## Verified before handover

- 25 objectives to 29, all ids unique.
- Every edge resolves to a real node, every `failObjectiveId` too.
- None of the three menus has a duplicate target.
- No em dashes in the new text; every new node carries scene characters.
- Base is the current live record, so the Fleetfoot and Nightfoot retirement stays in place.

## Not in this manifest

Three nodes have **empty descriptions**: `l4` and `c6` (both `reset_quest`) and `d5`
(`win_quest`). Old Ghost and The Tenth Name both give those nodes a line - "Report filed.
Entry open.", "The frontage, and the chain of runners." Copies gives the player a blank
screen at the two failure resets and at the win. Worth fixing, but it is a separate change
and not what was asked for.
