# Pilot (dauntless)

Director rulings, 2026-11-11:
- While the character is awake, the worker is always piloting. It steps away only while the character rests.
- A turn takes 8 s or less.
- PvP uses scripted tool calls. Auto-combat is only for fights against the game's AI (under half human strength).
- Attacks open with a 15 s lobby, so a check every ~10 s cannot miss one.

## The loop
Run `tools/pilot.py`. It prints a status line and then the next batch, one JSON object per line. Relay that batch
exactly, in order, in ONE message: each `call` goes to `mcp__Tnr__callEndpoint`, each `bash` to Bash. The last line
is always the next `pilot.py` tick. `{"wait": N}` means a background `sleep N`, then relay the rest on wake. No
lines means the character is asleep and the worker may step away. Write nothing else during the loop.

`pilot.py` reads that batch's game results straight from the session transcript (`fresh_results`) and keeps one state
file (`fights/live/pilot.json`, gitignored). Battle logs are cached by entry id and saved to
`fights/<battle>_entries.json` when the battle ends, because the game deletes them.

## Where behaviour lives
- Battle turns: `turn.py`, the planner, called by `plan_turn`. It has a 4 s budget, then a short-list fallback,
  then Defensive Stance. Same picks as before on the regression set.
- Awake outside battle: `world()`, as rules in priority order. Today: battle start, asleep, hospitalized, guard.
  Hunting rules go here.
- Every call the pilot can make is defined once, in the `c_*` helpers.

## Tests
`python3 tools/tests/test_pilot.py`: a fake transcript holding a logged battle state must produce the planner's pick
plus the next poll plus the tick, as one batch. Offline, socket-free.
