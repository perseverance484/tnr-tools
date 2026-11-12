"""Everything is wired in (director, 2026-11-11: "Every time we add a new system I discover you weren't using it
because it wasnt tied in").

Three checks, none of which takes the registry's word for itself:

1. A played-through session on the production combat adapter (player/combat.py, not a stub). The tool scripts
   it starts are stand-ins in a temporary folder that write down what they were given and answer in the real
   tools' format; the tools it imports are the real ones, pointed at temporary folders. Each model and feed must
   leave its trace in what came out: the planner's line is the line that was sent, the saved kit stops the kit
   read, the background jobs ran and could read the files written for them.
2. The same session with one production method unplugged at a time: the check for that model or feed must fail.
3. An inventory from outside the registry: every pilot tool the player's code runs or imports has an owner in
   the registry and nothing else is claimed; every tool the design's file map keeps for AP1 is owned; the feeds
   that the file map found running by hand or not at all are listed as deferred, with a phase and an owner.

A new activity, model or feed must be added to the session below, or this fails.
"""
import ast
import glob
import gzip
import importlib.util
import json
import os
import pkgutil
import re
import sys
import tempfile
import time
import unittest
from unittest import mock

import player.activities
from player import config as C
from player.combat import Combat
from player.tests.support import FOE, Rig, battle_read, fixture, log_read, my_items, res, scan, user

PREY = (FOE, "AngelSaberTwin", 13, 14, "AWAKE", 100, "y", None, None)
KIMS, SMOKE, PANACEA, PILL, KUNAI, KIT = ("6DnJn4x6LWWXtBu7UZybb", "TtYPd-LcXKeK3sMuhq1TP", "rsc2uO5QuffXzejfhwF_F",
                                         "tZTvqYWiAc_OrY64nDvIo", "yVNeLzxHSFkNpTPnlm7yQ", "1ovHq7jsGdut2fSNKs5q_")
OTHERS = (SMOKE, PILL, KIT)                 # in stock, and not what the upkeep part is about
SCRIPTS = ("turn.py", "planner2.py", "fight_bases.py", "opponents.py", "postmortem.py")
JOBS = ("fight_bases.py", "opponents.py", "postmortem.py")          # started in the background: the session waits
STANDIN = r'''"""A stand-in for a pilot tool script (player/tests/test_wiring.py): it writes down what it was given."""
import json, os, sys, time
name, fights = os.path.basename(__file__), os.environ["WIRING_FIGHTS"]
row = {"tool": name, "argv": sys.argv[1:]}
if name in ("turn.py", "planner2.py"):
    with open(sys.argv[1], encoding="utf8") as f:
        battle, log = [json.loads(line) for line in f.read().splitlines()]
    row.update(live="battle.liveEffects" in battle, log_lines=len(log["*.battleRound"]))
    print("FIRE: " + json.dumps([{"actionId": "standin_strike", "longitude": 6, "latitude": 4, "name": "Stand-in"}]))
elif name == "fight_bases.py":
    with open(os.path.join(fights, "live", sys.argv[1] + ".json"), encoding="utf8") as f:
        row["cache"] = sorted(json.load(f))
elif name == "opponents.py":
    row["logs"] = sorted(f for f in os.listdir(fights) if f.endswith("_entries.json"))
elif name == "postmortem.py":
    print("stand-in post-mortem of", sys.argv[1])
with open(os.path.join(os.environ["WIRING_RAN"], f"{name}-{time.time_ns()}.json"), "w", encoding="utf8") as f:
    json.dump(row, f)
'''


class Session:
    """One played-through session that touches everything: start, wake, a trip, a scan, a heal, an attack, a
    fight with the exact state, its end, the result."""

    def __init__(self, harvest=True, jobs=JOBS):
        self.rig = rig = Rig(mode="guard")
        self.scripts, self.ran = tempfile.mkdtemp(prefix="wiring-tools-"), tempfile.mkdtemp(prefix="wiring-ran-")
        for name in SCRIPTS:
            with open(os.path.join(self.scripts, name), "w", encoding="utf8") as f:
                f.write(STANDIN)
        rig.combat = Combat(os.path.join(rig.dir, "fights"), spawn=True, scripts=self.scripts)   # the production one
        rig.new_brain()
        rig.world["control"]["mode"] = "guard"
        self.chosen, self.calls, self.sent, self.bought = [], [], [], []
        with self.temporary_folders():
            self.play(harvest)
            self.kit = rig.combat.kit_path(FOE)
            self.kit_saved = os.path.exists(self.kit)
            deadline = time.time() + 10.0                                   # the background jobs finish on their own
            while time.time() < deadline and not set(jobs) <= set(self.marks()):
                time.sleep(0.02)

    def temporary_folders(self):
        """The real tools write under harness/ and read WIRING_* from the environment: both are pointed away from
        the repository for the length of the session."""
        if C.TOOLS not in sys.path:
            sys.path.insert(0, C.TOOLS)
        import engine_bridge
        harness = tempfile.mkdtemp(prefix="wiring-harness-")
        os.makedirs(os.path.join(harness, "kit", "opponents"))
        os.symlink(os.path.join(engine_bridge.HARNESS, "kit", "records.json"), os.path.join(harness, "kit", "records.json"))
        # the catalog is built from the records on first use, into the repository's own folder: here the tracked
        # records stand in for it, so nothing is built and nothing is written outside the temporary folders
        os.symlink(os.path.join(engine_bridge.HARNESS, "kit", "records.json"), os.path.join(harness, "kit", "catalog.json"))
        env = {"WIRING_RAN": self.ran, "WIRING_FIGHTS": self.rig.combat.fights}
        return _both(mock.patch.object(engine_bridge, "HARNESS", harness),
                     mock.patch.object(engine_bridge, "_CATALOG", None), mock.patch.dict(os.environ, env))

    def tick(self, *results, **kw):
        out = self.rig.tick(*results, **kw)
        self.chosen.append(out["activity"])
        self.calls += self.rig.calls(out)
        self.sent += [s["input"]["actionId"] for s in out["steps"] if s.get("call") == "combat.performAction"]
        self.bought += [(s["input"]["itemId"], s["input"]["stack"], s["meta"]["ryo"]) for s in out["steps"]
                        if s.get("call") == "item.buy"]
        return out

    def play(self, harvest):
        rig, tick = self.rig, self.tick
        tick()                                                             # watch: the first read
        rig.world["control"]["mode"] = "hunt"
        rig.world["control"]["activities"]["harvest"] = harvest            # (the upkeep has its turn after the fight)
        tick(user("ASLEEP"))                                               # session: wake
        tick(user("TRAVEL"))                                               # travel: land the trip
        out = tick(user(hp=3000))                                          # recovery: Full Potion
        tick(res("item.consume", {"success": True}, out["steps"][0]["input"]), user())   # pvp_hunt: scan, harvest riding
        tick(user(), res("profile.getStrongestUsers", {"*.userId": ["user_top"], "*.username": ["Top"]}), dt=10)
        tick(user(), scan([PREY]))                                         # pvp_hunt: his kit, then the attack
        tick(res("jutsu.getPublicUserJutsus", {"*.jutsuId": ["j1"], "*.level": [25], "*.equipped": [True]},
                 {"userId": FOE}), user("BATTLE", bid="W1"))               # battle: the opening read
        battle, ents = fixture()
        live = dict(battle, **{"battle.usersEffects": [{"type": "increasedamagegiven", "targetId": C.ME}]})
        tick(battle_read("W1", live), log_read("W1", ents))                # battle: my turn, planned on the live state
        tick(battle_read("W1", {}))                                        # the battle is gone: my profile is asked
        tick(battle_read("W1", {}), user())                                # I have left it: the fight closes
        tick(user())                                                       # the result is settled
        self.upkeep()

    def upkeep(self):
        """After the fight, with every upkeep activity on: a worn item repaired, a short one bought at the price
        the real catalog gives, the PvP 1 loadouts, the training queue, the pocket banked."""
        rig, tick = self.rig, self.tick
        rig.world["control"]["activities"] = {"harvest": False}
        rich = dict(money=30_000_000, bank=900_000_000)
        rows = {"kims": ("u1", KIMS, 6, "ITEM_1", False, 100), "panacea": ("u3", PANACEA, 2, "ITEM_3", False, 100),
                "kunai": ("u5", KUNAI, 30, "THROWN", False, 10)}           # the kunai: 10 of 100, close to broken
        short = [r for r in rows.values()] + [(f"s{n}", i, 30, "NONE", False, 100) for n, i in enumerate(OTHERS)]
        mended = [r if r[1] != KUNAI else r[:5] + (100,) for r in short]
        full = [r if r[1] != PANACEA else r[:2] + (6,) + r[3:] for r in mended]
        def yes(out, *endpoints):
            """The game's yes to each of these calls of a batch."""
            return [res(s["call"], {"success": True}, s["input"]) for s in out["steps"] if s.get("call") in endpoints]
        tick(user(**rich))                                                 # restock: reads my items
        out = tick(my_items(*short), user(**rich))                         # repair: the worn kunai
        out = tick(*yes(out, "item.useRepairAll"), my_items(*mended), user(**rich))    # restock: buys the Panacea
        out = tick(*yes(out, "item.buy"), my_items(*full), user(**rich))   # equipment: the PvP 1 loadouts
        tick(*yes(out, "jutsu.selectJutsuLoadout", "item.selectItemLoadout"), user(**rich))   # training: the queue
        out = tick(res("jutsu.getTrainingQueue", {"capacity": 4, "waiting.*.jutsuId": [], "waiting.*.level": []}),
                   res("jutsu.getUserJutsus", {"*.jutsuId": ["j1"], "*.level": [3], "*.finishTraining": [None]}),
                   user(**rich))                                           # training: the free places are filled
        out = tick(*yes(out, "jutsu.startTraining"), user(**rich))         # bank: the pocket is over its mark
        tick(*yes(out, "bank.toBank"), user(money=10_000_000, bank=920_000_000))

    def marks(self):
        """What the stand-in scripts wrote down, by tool."""
        rows = {}
        for path in sorted(glob.glob(os.path.join(self.ran, "*.json"))):
            try:
                with open(path, encoding="utf8") as f:
                    row = json.load(f)
            except ValueError:
                continue                                                   # still being written
            rows.setdefault(row["tool"], []).append(row)
        return rows

    def evidence(self):
        """{model or feed: did it leave its trace in what the session produced}."""
        rig, fights, ran = self.rig, self.rig.combat.fights, self.marks()
        planned = [r for name in ("turn.py", "planner2.py") for r in ran.get(name, [])]
        end = (rig.events("fight_end") or [{}])[0]
        post = os.path.join(fights, "postmortems", "W1.txt")
        first_state = {}
        try:
            with gzip.open(os.path.join(fights, "live_states", "W1.full.jsonl.gz"), "rt") as f:
                first_state = json.loads(f.readline())
        except OSError:
            pass
        return {
            # the planner got the fight's file with the live state in it, and its line is the line that was sent
            "planner": bool(planned) and planned[-1]["live"] and "W1" in planned[-1]["argv"]
            and set(self.sent) == {"standin_strike"},
            # the kit read before the attack was saved by the real tool, so the fight did not read it again
            "dossier": self.kit_saved and self.calls.count("jutsu.getPublicUserJutsus") == 1,
            # the model rebuild ran after the fight, with the fight's log already on disk for it
            "opponents": any(r["argv"] == ["build"] and "W1_entries.json" in r["logs"] for r in ran.get("opponents.py", [])),
            "postmortem": os.path.exists(post) and "stand-in post-mortem of W1" in open(post, encoding="utf8").read(),
            # the log's own HP count named the result and the round that decided it
            "fight_result": end.get("result") == "won" and str(end.get("turning_point")).startswith("round "),
            # the bases job ran for this fight and could read the state written for it
            "fight_bases": any(r["argv"] == ["W1"] and "entries" in r["cache"] for r in ran.get("fight_bases.py", [])),
            "live_state": first_state.get("seat") in (1, 2) and bool(first_state.get("effects"))
            and os.path.exists(os.path.join(fights, "live_states", "W1.json")),
            "fight_log": os.path.exists(os.path.join(fights, "W1_entries.json")),
            "harvest": "players" in rig.world.own("harvest").get("stats", "")
            and "combat.getBattleHistory" in self.calls,
            # the purchase was sized and priced from the real catalog's record: 4 Panacea at 55,000 ryo
            "catalog": self.bought == [(PANACEA, 4, 220_000.0)] and "item.useRepairAll" in self.calls,
            # what is equipped was written where the planners look for the thrown weapon
            "equipped": self._equipped().get("THROWN") == KUNAI,
        }

    def _equipped(self):
        try:
            with open(os.path.join(self.rig.combat.live, "equipped.json"), encoding="utf8") as f:
                return json.load(f)
        except (OSError, ValueError):
            return {}


class _both:
    """Several context managers as one."""

    def __init__(self, *managers):
        self.managers = managers

    def __enter__(self):
        for m in self.managers:
            m.__enter__()

    def __exit__(self, *exc):
        for m in reversed(self.managers):
            m.__exit__(*exc)


class Wiring(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.run_ = Session()
        cls.rig, cls.chosen, cls.calls = cls.run_.rig, cls.run_.chosen, cls.run_.calls
        cls.reg = cls.rig.brain.reg

    def test_every_module_under_activities_registers_one_activity(self):
        modules = {m.name for m in pkgutil.iter_modules(player.activities.__path__)}
        self.assertEqual(modules, set(self.reg.activities))
        for name, act in self.reg.activities.items():
            self.assertEqual(type(act).__module__, f"player.activities.{name}")

    def test_every_activity_is_chosen_in_a_session(self):
        riders = {n for n, a in self.reg.activities.items() if a.rides}
        for name in self.reg.activities:
            if name in riders:
                continue
            self.assertIn(name, self.chosen, f"{name} is registered but the brain never chose it")
        self.assertEqual(riders, {"harvest"})
        self.assertIn("profile.getStrongestUsers", self.calls)         # the rider's read went out
        self.assertIn("combat.getBattleHistory", self.calls)           # and its answer set up the next one

    def test_every_model_and_feed_leaves_a_trace_on_the_production_adapter(self):
        self.assertIs(type(self.rig.combat), Combat)                   # not a stub of it
        evidence = self.run_.evidence()
        self.assertEqual(set(evidence), set(self.reg.models) | set(self.reg.feeds),
                         "a model or feed is registered with no check here (or checked and not registered)")
        self.assertEqual([k for k, ok in evidence.items() if not ok], [])

    def test_the_session_played_out(self):
        self.assertEqual(self.rig.events("fight_start")[0]["battle"], "W1")
        self.assertEqual(self.rig.events("fight_end")[0]["result"], "won")
        self.assertEqual(self.calls.count("item.consume"), 2)          # the heal before, and the one at the fight's end
        self.assertEqual(self.rig.world["records"]["turns_missed"], 0)

    def test_every_call_the_code_can_send_is_on_the_approved_list(self):
        spec = importlib.util.spec_from_file_location("pa", os.path.join(C.ROOT, "scripts", "player_allowlist.py"))
        pa = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(pa)
        self.assertIn(os.path.join(C.ROOT, "player"), pa.CODE_DIRS)
        errs, _ = pa.check(pa._load(pa.ALLOWLIST), pa._load(pa.SURFACE), [os.path.join(C.ROOT, "player")])
        self.assertEqual(errs, [])
        listed = pa._load(pa.ALLOWLIST)["endpoints"]
        for ep in set(self.calls):
            self.assertIn(ep, listed)


class Unplugged(unittest.TestCase):
    """The review's test of the test: with a production method disconnected, the wiring check must fail for it."""

    def broken(self, method, stand_in, jobs=JOBS):
        with mock.patch.object(Combat, method, stand_in):
            return {k for k, ok in Session(jobs=jobs).evidence().items() if not ok}

    def test_a_planner_that_is_not_called_through_fails(self):
        self.assertEqual(self.broken("plan_turn", lambda self, *a, **k: (None, "unwired")), {"planner"})

    def test_a_kit_that_is_not_saved_fails(self):
        self.assertEqual(self.broken("save_kit", lambda self, *a, **k: False), {"dossier"})

    def test_background_jobs_that_are_not_started_fail(self):
        self.assertEqual(self.broken("_popen", lambda self, *a, **k: None, jobs=()),
                         {"opponents", "postmortem", "fight_bases"})

    def test_a_fight_that_is_not_kept_fails(self):
        self.assertEqual(self.broken("close_fight", lambda self, *a, **k: None, jobs=JOBS[:1]),
                         {"opponents", "postmortem", "fight_log", "live_state"})
        self.assertEqual(self.broken("archive_state", lambda self, *a, **k: None), {"live_state"})

    def test_a_result_that_is_not_read_from_the_log_fails(self):
        self.assertEqual(self.broken("turning_point", lambda self, state: None), {"fight_result"})
        self.assertEqual(self.broken("log_says_lost", lambda self, state: True), {"fight_result"})

    def test_a_harvest_that_does_not_ride_fails(self):
        self.assertEqual({k for k, ok in Session(harvest=False).evidence().items() if not ok}, {"harvest"})

    def test_a_catalog_that_is_not_read_fails(self):
        self.assertEqual(self.broken("item_record", lambda self, item_id: {}), {"catalog"})

    def test_what_is_equipped_and_not_written_down_fails(self):
        self.assertEqual(self.broken("write_equipped", lambda self, slots: None), {"equipped"})


class Inventory(unittest.TestCase):
    """Who owns which pilot tool, held against the code and the design's file map, not against the registry."""

    @classmethod
    def setUpClass(cls):
        from player import registry
        cls.reg = registry.load()
        cls.tools = {f for f in os.listdir(C.TOOLS) if f.endswith(".py")}
        wired = list(cls.reg.models.values()) + list(cls.reg.feeds.values())
        cls.owned = {t for e in wired for t in e["tools"]}
        cls.read = {t for e in wired for t in e["reads"]}
        cls.deferred = {t for e in cls.reg.deferred.values() for t in e["tools"]}
        with open(os.path.join(C.ROOT, "docs", "design", "AI_PLAYER_OVERHAUL.md"), encoding="utf8") as f:
            cls.file_map = f.read().split("### File map", 1)[1].split("\n## 3.", 1)[0]

    def used_by_the_code(self):
        """The pilot tools the player's own code runs (a script name) or imports, read from its syntax tree.
        The registry's own declarations are left out: a claim is not a use."""
        used = set()
        for path in glob.glob(os.path.join(C.ROOT, "player", "**", "*.py"), recursive=True):
            if f"{os.sep}tests{os.sep}" in path:
                continue
            with open(path, encoding="utf8") as f:
                tree = ast.parse(f.read())
            claims = {id(n) for call in ast.walk(tree) if isinstance(call, ast.Call)
                      and isinstance(call.func, ast.Attribute) and getattr(call.func.value, "id", "") == "REGISTRY"
                      for n in ast.walk(call)}
            for node in ast.walk(tree):
                if id(node) in claims:
                    continue
                if isinstance(node, ast.Constant) and isinstance(node.value, str) and node.value in self.tools:
                    used.add(node.value)
                elif isinstance(node, ast.Import):
                    used |= {a.name + ".py" for a in node.names if a.name + ".py" in self.tools}
                elif isinstance(node, ast.ImportFrom) and not node.level and f"{node.module}.py" in self.tools:
                    used.add(f"{node.module}.py")
        return used

    def test_every_tool_the_code_runs_or_imports_has_an_owner_and_nothing_else_is_claimed(self):
        self.assertEqual(self.used_by_the_code(), self.owned)

    def test_a_tool_a_model_reads_through_another_is_really_imported_by_a_wired_tool(self):
        for lib in self.read:
            module = lib[:-3]
            importers = [t for t in self.owned
                         if re.search(rf"^\s*(import|from) {module}\b", open(os.path.join(C.TOOLS, t)).read(), re.M)]
            self.assertTrue(importers, f"{lib} is listed as read, but no wired tool imports it")

    def test_every_tool_the_file_map_keeps_for_ap1_is_owned(self):
        keeps = set()
        for row in re.findall(r"^\| `.*$", self.file_map, re.M):
            cells = [c.strip() for c in row.strip("|").split("|")]
            if cells[2].startswith("keep") and "AP1" in cells[4]:
                keeps |= set(re.findall(r"`([a-z_0-9]+\.py)`", cells[0]))
        self.assertGreaterEqual(len(keeps), 6)                          # the map still reads as a table
        self.assertEqual(keeps - self.owned - self.read, set())

    def test_the_feeds_the_file_map_found_unwired_are_listed_as_deferred(self):
        line = re.search(r"Three feeds run by hand or not at all \(([^)]*)\)", self.file_map).group(1)
        named = set(re.findall(r"`([a-z_0-9]+\.py)", line))
        self.assertEqual(named, {"meal_factor.py", "validate.py", "engine_fit.py"})
        self.assertEqual(named, self.deferred)
        self.assertEqual(self.deferred & self.used_by_the_code(), set())     # deferred means the code does not run it
        for name, entry in self.reg.deferred.items():
            self.assertRegex(entry["phase"], r"^AP\d$", name)
            self.assertTrue(entry["owner"].strip() and entry["what"].strip(), name)
            self.assertTrue(set(entry["tools"]) <= self.tools, name)


if __name__ == "__main__":
    unittest.main()
