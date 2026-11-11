# Live fight loop (dauntless)

Why: on 2026-11-11 the director had to take my turn in three straight fights (TearsOfAngel R1, Arashii R2,
AngelSaber R3), and AngelSaber's round 1 went unanswered because nothing was watching when he attacked. The
tools were fine; the loop around them was not. This is the loop.

## 1. Never idle while exposed
- Out in the world and awake (hunting, travelling, standing in a sector) = exposed. While exposed, **no reply ends
  without a background `sleep 15-20` wake-up**, and every wake-up starts with a status check
  (`profile.getUser` select `userData.status`, `userData.battleId`). `BATTLE` -> go to section 2 at once.
- Not playing and not watching -> go home and sleep (`home.toggleSleep` in sector 177), never stand in the open.

## 2. Each poll in a fight (one parallel tool call, then one shell call)
1. Read both at once:
   - `combat.getBattle` select `battle.version`, `battle.round`, `battle.activeUserId`, and
     `battle.usersState.*.` `userId` `username` `curHealth` `maxHealth` `longitude` `latitude` `actionPoints`.
   - `combat.getBattleEntries` with `limit: 8` (the **first** poll of a battle: `limit: 200`), select `*.id`,
     `*.battleRound`, `*.userId`, `*.actionId`, `*.appliedEffects.*.txt`.
2. Merge the two results into one JSON object and pipe it in:
   `echo '<json>' | python3 fight.py BATTLE_ID`, run from `tools/`.
   The cache in `fights/live/<battle>.json` keeps the full log by entry id, and it survives the battle ending.
3. **His turn:** the output line ends `default: ...`. That plan is pre-computed and stored. Sleep 10-15 s in the
   background, then poll again.
4. **My turn:** the output is `FIRE vN: ...` followed by one ready `performAction` input per line, versions filled
   in. Send them back to back, with no other thinking in between. Verify only by the next poll.

## 3. Time rules
- The planner has a 14 s budget. Past about 34 s into my turn, `fight.py` skips planning and prints the stored
  default.
- "Battle state changed" on the first action means the director took the turn (or the version moved). Re-poll
  once; never re-plan by hand.
- Sanity overrides of the planner come from logged director lessons only, decided during **his** turn, never
  on mine.

## 4. After the battle
- `fights/live/<battle>.turn.txt` is a turn file that `fit_gear.py` and the post-fight tools read. Log the fight
  from it (entries are deleted from the game when the battle ends).
