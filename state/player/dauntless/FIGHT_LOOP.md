# Live fight loop (dauntless)

Director rulings, 2026-11-11: a turn takes 8 s or less. PvP is played through scripted tool calls with me in the
loop. Auto-combat is only for fights against the game's AI (hunting), never PvP. It plays at under half human
strength.

Measured in arena, 2026-11-11: game calls take ~0.4 s each; the planner took 2.3 to 2.6 s. **My own latency between
messages was ~5 s per gap**, the largest cost. So a turn is built to have exactly one gap.

## 1. Never idle while exposed
- Awake in the world = exposed. No reply ends without a background `sleep 15-20` wake-up, and each wake-up starts
  with a status check (`profile.getUser`: `userData.status`, `userData.battleId`). `BATTLE` -> section 2 at once.
- Not playing -> go home and sleep (`home.toggleSleep`, sector 177).

## 2. The turn: two messages, no text in either
**Message A, the poll (one batch, three calls, in this order):**
1. `combat.getBattle {battleId}`, select `battle.version`, `battle.round`, `battle.activeUserId`, and
   `battle.usersState.*.` `userId` `username` `curHealth` `maxHealth` `longitude` `latitude` `actionPoints`.
2. `combat.getBattleEntries {battleId, limit: 8}` (the first poll of a battle: `limit: 200`), select `*.id`,
   `*.battleRound`, `*.userId`, `*.actionId`, `*.appliedEffects.*.txt`.
3. Bash `cd state/player/dauntless/tools && python3 fight.py`, with no arguments.

Calls in one batch run in order, and the script reads 1 and 2 from the session transcript (verified: it sees results
from earlier in the same batch). It merges the log into `fights/live/<battle>.json` by entry id.

- **His turn:** it prints a status line and returns at once. A detached worker pre-plans my next turn with the full
  planner and the engine, and stores it as the default. **Poll again immediately**: no sleep, no text. The speed of
  this loop is the detection lag.
- **My turn:** it plans inside the budget (or uses the stored default) and prints `FIRE vN: ...` plus one
  `performAction` input per line, versions filled in.

**Message B, the actions (one batch):** every printed `performAction`, in order, in one message. Verified in arena:
they land in order. Then go back to Message A.

## 3. Rules
- Write nothing during a fight: every token I write is turn time. Report after the fight.
- "Battle state changed" or "no longer possible" on an action -> the next poll re-plans. Never re-plan by hand.
- An unusable 10 AP left over (after a -10 stun) -> `wait` ends the turn.
- Planner lessons from the director go into the tools between fights, never into on-the-clock reasoning.

## 4. After the battle
- `fights/live/<battle>.turn.txt` is a turn file for `fit_gear.py` and the post-fight tools. Log from it, because
  the game deletes the entries when a battle ends.
