"""The registry: every activity, model and data feed the player has (design 4.3).

A thing that is not registered here does not exist: the brain only runs what the registry lists, and the wiring
test (player/tests/test_wiring.py) fails when a module under player/activities/ is not registered, or when a
registered activity, model or feed is never exercised.

An activity is a class with the same five methods (design 4.3):
    available(world)          can it do anything now
    value(world)              expected gain per minute, in progress points (design 4.4)
    plan(world)               a Plan: the next calls, or None
    on_result(world, results) fold the answers it understands into the model
    done(world)               nothing left to do for now
"""
import collections
import importlib
import pkgutil

# priority classes, highest first (design 4.4): a higher class always preempts a lower one
CLASSES = ("battle", "safety", "deadlines", "upkeep", "goals", "scouting")
LANES = ("battle", "recovery", "world")

Plan = collections.namedtuple("Plan", "steps lane note hold tag")
"""steps: call and wait steps, in order. lane: the budget lane. note: a short status line. hold: seconds the brain
waits before it hands the batch to the relay (a brain-side sleep: it costs the relay nothing). tag: "fight_end"
on the batch that closes a fight (the brain puts recovery in front of it), "urgent" on a batch that must not wait
behind a rate-limit pause, else ""."""


def plan(steps, lane="world", note="", hold=0.0, tag=""):
    return Plan(list(steps), lane, note, float(hold), tag)


class Activity:
    name = ""
    priority = "goals"         # one of CLASSES
    goal = None                # the key of player/goals.json "weights" its value is multiplied by, if any
    reads = ()                 # endpoints whose results it folds into the model
    rides = False              # never chosen on its own: its calls ride another activity's quiet world batch
    combat = budget = gates = None     # bound by the brain

    def available(self, world):
        return False

    def value(self, world):
        return 0.0

    def plan(self, world):
        return None

    def on_result(self, world, results):
        return None

    def done(self, world):
        return not self.available(world)


class Registry:
    def __init__(self):
        self.activities = collections.OrderedDict()
        self.models = collections.OrderedDict()
        self.feeds = collections.OrderedDict()

    def activity(self, cls):
        """Class decorator: register one activity (one per file under player/activities/)."""
        inst = cls()
        if not inst.name or inst.priority not in CLASSES:
            raise ValueError(f"{cls.__name__}: an activity needs a name and a priority class")
        if inst.name in self.activities:
            raise ValueError(f"activity {inst.name} is registered twice")
        self.activities[inst.name] = inst
        return cls

    def model(self, name, what, module):
        """A model the decisions read (opponent models, the dossier, the planner): name -> where it lives."""
        self.models[name] = {"what": what, "module": module}

    def feed(self, name, what, module):
        """A data feed (a file or state some model reads, and who writes it)."""
        self.feeds[name] = {"what": what, "module": module}

    def by_priority(self):
        return sorted(self.activities.values(), key=lambda a: CLASSES.index(a.priority))


REGISTRY = Registry()


def load():
    """Import every module under player/activities/ (each registers itself) and the combat adapter (it registers
    the models and feeds). Returns the registry."""
    from . import activities
    for m in pkgutil.iter_modules(activities.__path__):
        importlib.import_module(f"{activities.__name__}.{m.name}")
    importlib.import_module("player.combat")
    return REGISTRY
