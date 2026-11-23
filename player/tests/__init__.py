"""The player's tests.

The suite was written before the autopilot's switches (tnr-autopilot, 2026-11-23). A brain now starts in the dry
run, keeps out of fights against people and casts stealth when it hunts; the tests written before drive it as it
played then: run live, pvp_turns on, stealth already up. That is set here, for the test package only, on the world
model's template. The tests of the new defaults (test_autopilot.py) put the real defaults back for themselves.
"""
from player import world as _world

LIVE_DEFAULTS = {"run": _world.TEMPLATE["control"]["run"], "pvp_turns": _world.TEMPLATE["control"]["pvp_turns"]}
_world.TEMPLATE["control"].update(run="live", pvp_turns=True)
_world.TEMPLATE["map"]["stealth"] = {"on": True, "until": 1e12, "ready_at": 0}
