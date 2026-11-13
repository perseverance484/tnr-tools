"""What the brain asks for in a fight against a player, on the code of the checkout this is run from.

    PYTHONPATH=. python3 docs/reviews/evidence/ai_player_light_polls/duel.py

On the base (661f3f63), from a throwaway worktree of it, with the head's files given by path:

    PYTHONPATH=. python3 <head>/docs/reviews/evidence/ai_player_light_polls/duel.py \\
        <head>/player/tests/test_light_polls.py

The fight is the stand-in of player/tests/test_light_polls.py (class Duel): my turn passes to him when the game
has taken my last action; his turn lasts a set time, in which he acts three times; the relay takes a set time
before a batch's first call. The base has neither ENTRIES_TURN nor PLAN_AT_LEAST, which the test file names:
they are set here, in this process only. The base's code reads neither, and no file of it is changed.
"""
import importlib.util
import json
import sys

from player import config as C

for name, value in (("ENTRIES_TURN", 20), ("PLAN_AT_LEAST", 3.0)):
    if not hasattr(C, name):
        setattr(C, name, value)

if len(sys.argv) > 1:
    spec = importlib.util.spec_from_file_location("player.tests.test_light_polls", sys.argv[1])
    tests = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tests)
else:
    from player.tests import test_light_polls as tests

from player.tests.support import FOE, Rig          # noqa: E402
from player.tests.test_review import turns          # noqa: E402

FIGHTS = (("his turn 20 s, the relay 3 s a batch", {}, 420),
          ("his turn 40 s, the relay 3 s a batch", {"his_turn": 40.0}, 600),
          ("his turn 30 s, the relay 10 s a batch", {"lag": 10.0, "his_turn": 30.0}, 600),
          ("his turn 6 s, the relay 10 s a batch", {"lag": 10.0, "his_turn": 6.0}, 600))

print("| Fight | Turns of mine | All acted | Full reads | a round | Light reads | Log reads | Batches | "
      "First action, mean | latest |\n|---|---|---|---|---|---|---|---|---|---|")
for name, kw, seconds in FIGHTS:
    rig = Rig()
    rig.combat.kits.add(FOE)
    game = tests.Duel(rig, **kw)
    batches = 0
    tick = rig.tick

    def counted(*a, _tick=tick, **k):
        global batches
        batches += 1
        return _tick(*a, **k)
    rig.tick = counted
    game.play(seconds)
    played = turns(rig)
    n = max(1, len(played))
    fired = [t["fired_after"] or 0 for t in played]
    print(f"| {name} | {len(played)} | {'yes' if {t['outcome'] for t in played} == {'acted'} else 'NO'} | "
          f"{game.asked.count('full')} | {game.asked.count('full') / n:.1f} | {game.asked.count('light')} | "
          f"{game.asked.count('log')} | {batches} | {sum(fired) / n:.1f} s | {max(fired):.1f} s |")
