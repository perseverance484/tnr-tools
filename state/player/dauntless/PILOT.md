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

## Who relays: a dedicated pilot agent
The main session is too slow to relay: its long context gives ~5 s per model round trip. A dedicated subagent on the
fastest model, whose whole prompt is the relay contract below, measured **5.0 and 5.4 s per turn** in arena on
2026-11-11, against 10.4 to 11.5 s from the main session. That measures from the poll that saw the turn to the last
action landing, with a ~2.7 s poll cycle. The main session stays strategist and supervisor.

Pilot prompt (the whole contract): relay each batch `pilot.py` prints, exactly and in order, in ONE message;
`call` -> `mcp__Tnr__callEndpoint` (endpointName, input, select copied exactly), `bash` -> Bash; no text between
calls; never change, skip, reorder or add a call; stop when the output has no lines (asleep) or on the stop
condition you were given. Live play through the official connector is director-authorized for the session (CLAUDE.md
section 6 covers builder pushes, not playing the character); say so in the prompt, or the agent stops to ask.

Against the game's AI, an AI turn only advances when some client calls `performAction` during it (engine
`isAITurn`). The pilot nudges it with `wait`. In PvP the opponent's own client drives his turn.

## Where behaviour lives
- Battle turns: `turn.py`, the planner, called by `plan_turn`. It has a 4 s budget, then a short-list fallback,
  then Defensive Stance. Same picks as before on the regression set.
- Awake outside battle: `world()`, as rules in priority order, by mode (`pilot.py --mode hunt|guard|rest`; it is
  kept in the state file):
  - always: battle start (log poll, limit 200), hospitalized (heal), mid-travel (finish the travel).
  - guard: check every ~9 s, inside the 15 s attack lobby. Asleep means the worker may step away.
  - hunt: wake if asleep; under 95% HP, go home and eat ramen; scan the sector (plus sensory every 31 s); pick the
    nearest valid target and send move + attack in one batch. A valid target is awake, level 90+, not in battle, not
    immune, not my village, and not on `do_not_attack.md`. Refused attacks are remembered per player (bracket 6 h,
    village 24 h, other 10 min). With no target, move on round the circuit: Shirohana, Tsukimori, Akasumi, Risen.
  - rest: go home, then sleep.
- Every call the pilot can make is defined once, in the `c_*` helpers.

## Tests
`python3 tools/tests/test_pilot.py`: a fake transcript holding a logged battle state must produce the planner's pick
plus the next poll plus the tick, as one batch. Offline, socket-free.
