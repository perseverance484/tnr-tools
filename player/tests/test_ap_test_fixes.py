"""Fixes from the AP model's test run (2026-11-16, /mnt/project-files/tnr/ap_test_2026-11-16/OPERATOR_REPORT.md).

F1: a battle id that starts with a dash (-CH613DKHOF7stgVwrDNR) was read by the planners' argument parser as an
option, so no plan came back. Ids and names now go in as --flag=value, and a positional id after "--".
F2: the relay was rotated at 60k tokens of context, so batches cost 7,698 tokens against the proof's 4,200-4,400.
It is now rotated by size (ROTATE_AFTER_TOKENS) or by count (ROTATE_AFTER_BATCHES), still never in a fight, and a
rotation nobody picks up is a stall that gives the run lock back.
F5: end_session=true refuses any new fight at the call (gate session_ending); a fight that is running is played.
F3: `brain stopped` on a live folder that does not exist yet.
F7/F8: the fight logs were never kept. They were written in the play session's checkout and lost with it; and the
second fight's id holds "_" (6_UqBB_MXSIqobeRrfmdd), so the post-mortem read it as battle "6" and found no log.
Each closed fight is now pushed to main (player/keep.py), and its closing batch reads the log once more with each
line's description, of which the tile ("on <b>F4</b>") is kept as the log's "*.tile" column: the replay review
reads positions from it.
Socket-free: no game call, no connector call; the planners run on a logged state.
"""
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

from player import calls as K, config as C, keep, relay
from player.activities.pvp_hunt import PvpHunt
from player.brain import client
from player.combat import Combat, planner_argv
from player.tests.support import FIXTURES, Rig, battle_read, fixture, gone, log_read, res, start_fight, user
from player.tests.test_runlock import on_the_accounts_folder

DASH = "-CH613DKHOF7stgVwrDNR"                    # the id of the AP test's first fight (ASV)


class DashIds(unittest.TestCase):
    def run_tool(self, argv):
        return subprocess.run(argv, capture_output=True, text=True, timeout=600, cwd=C.TOOLS)

    def test_the_old_form_fails_on_a_dash_id(self):
        """What happened in the test run: argparse takes the id for an option."""
        out = self.run_tool([sys.executable, os.path.join(C.TOOLS, "turn.py"), os.path.join(FIXTURES, "anbu_r3.txt"),
                             "--battle", DASH, "--top", "1", "--enemy", "ANBU Member", "--no-engine"])
        self.assertNotEqual(out.returncode, 0)
        self.assertIn("expected one argument", out.stderr)

    def test_both_planners_plan_a_dash_id(self):
        for script, extra in (("turn.py", ("--no-engine",)), ("planner2.py", ())):
            argv = planner_argv(os.path.join(C.TOOLS, script), os.path.join(FIXTURES, "anbu_r3.txt"), DASH,
                                "ANBU Member", extra)
            self.assertIn(f"--battle={DASH}", argv)
            out = self.run_tool(argv)
            self.assertEqual(out.returncode, 0, (script, out.stderr[-500:]))
            self.assertRegex(out.stdout, r"(?m)^FIRE: \[", script)

    def test_the_post_mortem_takes_a_dash_id_after_a_double_dash(self):
        bad = self.run_tool([sys.executable, os.path.join(C.TOOLS, "postmortem.py"), DASH[:8]])
        good = self.run_tool([sys.executable, os.path.join(C.TOOLS, "postmortem.py"), "--", DASH[:8]])
        self.assertNotEqual(bad.returncode, 0)
        self.assertNotIn("unrecognized arguments", good.stderr)
        self.assertNotIn("expected one argument", good.stderr)

    def test_plan_turn_hands_the_id_with_an_equals_sign(self):
        combat = Combat(tempfile.mkdtemp(), spawn=False)
        battle, ents = fixture("anbu_r3.txt")
        seen = []

        def fake_run(argv, **kw):
            seen.append(argv)
            return subprocess.CompletedProcess(argv, 0, 'FIRE: [{"actionId": "a", "longitude": 1, "latitude": 1}]\n', "")

        rows = [[ents[k][i] for k in K.ENT] for i in range(len(ents["*.battleRound"]))]
        with mock.patch("player.combat.subprocess.run", side_effect=fake_run):
            plan, how = combat.plan_turn(DASH, battle, rows, "ANBU Member")
        self.assertEqual(plan[0]["actionId"], "a", how)
        self.assertIn(f"--battle={DASH}", seen[0])
        self.assertIn("--enemy=ANBU Member", seen[0])
        self.assertNotIn(DASH, seen[0])                    # never on its own, where it reads as an option

    def test_no_tool_call_in_the_player_puts_an_id_on_its_own(self):
        """Every place an id goes on a command line: the planners and the post-mortem (fight_bases.py reads its
        argv[1] raw, so a dash is safe there)."""
        here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        for path in (os.path.join(here, "combat.py"), os.path.join(C.TOOLS, "pilot.py"),
                     os.path.join(C.TOOLS, "replay.py")):
            with open(path, encoding="utf8") as f:
                src = f.read()
            self.assertNotRegex(src, r'"--battle",\s*(bid|a\.battle)\b', path)
            self.assertNotRegex(src, r'"postmortem\.py"\),\s*bid', path)


class Rotation(unittest.TestCase):
    def test_the_relay_is_rotated_after_so_many_batches_and_never_in_a_fight(self):
        rig = Rig()
        rig.tick(user())
        rig.brain.handle([], {"in": 1, "out": 1, "context": 6_000})
        for seq in range(C.ROTATE_AFTER_BATCHES - 2):                         # the handle above was one
            relay.log_tokens(rig.world, seq, {"in": 1, "out": 1, "context": 6_100}, "")
        self.assertFalse(relay.should_rotate(rig.world))
        rig.world["battle"] = {"bid": "B1", "entries": [], "battle": {}}
        relay.log_tokens(rig.world, 99, {"in": 1, "out": 1, "context": 6_100}, "")
        self.assertFalse(relay.should_rotate(rig.world))                      # in a fight: never
        rig.world["battle"] = None
        out = rig.tick(user())
        self.assertTrue(out["stop"].startswith("rotate"))
        self.assertEqual(rig.world["relay"]["batches"], 0)                    # the new relay counts from 0

    def test_the_size_limit_is_near_the_proof(self):
        """PROOF.md: 4,200-4,400 tokens a batch with a small context; 12k is where it is cut now."""
        self.assertLessEqual(C.ROTATE_AFTER_TOKENS, 15_000)
        self.assertLessEqual(C.ROTATE_AFTER_BATCHES, 30)

    def test_a_rotation_nobody_picks_up_is_a_stall_and_the_lock_goes_back(self):
        rig = Rig()
        tool = on_the_accounts_folder(rig)
        rig.tick(user(sector=1538))
        with mock.patch.object(relay, "should_rotate", return_value=True):
            self.assertTrue(rig.tick(user(sector=1538))["stop"].startswith("rotate"))
        self.assertEqual([a[0] for a in tool.asked], ["claim"])
        rig.t += C.ROTATE_GRACE - 5
        self.assertFalse(rig.brain.watchdog())                                # not late yet
        rig.t += 10
        self.assertTrue(rig.brain.watchdog())
        self.assertEqual(tool.asked[-1], ("release", "token-1"))
        stall = [e["text"] for e in rig.events("stall") if "rotated" in e["text"]]
        self.assertEqual(len(stall), 1)
        self.assertIn("AWAKE at sector 1538", stall[0])
        self.assertIn("STALLED: rotation not picked up", rig.status()["note"] if "note" in rig.status()
                      else json.dumps(rig.status()))
        rig.t += 60
        self.assertFalse(rig.brain.watchdog())                                # said once
        rig.tick(user())                                                      # a relay asks again: it claims again
        self.assertEqual([a[0] for a in tool.asked], ["claim", "release", "claim"])
        self.assertNotIn("rotated_at", rig.world["relay"])

    def test_a_relay_that_comes_in_time_is_no_stall(self):
        rig = Rig()
        tool = on_the_accounts_folder(rig)
        rig.tick(user())
        with mock.patch.object(relay, "should_rotate", return_value=True):
            rig.tick(user())
        rig.tick(user(), dt=30.0)
        rig.t += C.ROTATE_GRACE * 2
        rig.brain.watchdog()
        self.assertEqual([a[0] for a in tool.asked], ["claim"])
        self.assertEqual([e for e in rig.events("stall") if "rotated" in e["text"]], [])


class EndingSession(unittest.TestCase):
    def test_no_new_fight_is_started_once_the_session_is_ending(self):
        rig = Rig()
        rig.tick(user())
        target = {"userId": "u1", "username": "Somebody", "longitude": 3, "latitude": 3}
        rig.world["control"]["end_session"] = True
        v = rig.brain.gates.check(K.attack(target, 1538), rig.world, "pvp_hunt")
        self.assertEqual((v.kind, v.rule), ("refuse", "session_ending"))
        self.assertFalse(PvpHunt().available(rig.world))                    # and the hunt plans none
        rig.world["control"]["end_session"] = False
        self.assertTrue(PvpHunt().available(rig.world))

    def test_a_fight_that_is_running_is_still_played(self):
        rig = Rig()
        rig.world["control"]["end_session"] = True
        battle, ents = fixture()
        battle["battle.usersEffects"] = []
        rig.tick(user("BATTLE", bid="B1"))
        out = rig.tick(battle_read("B1", battle), log_read("B1", ents))
        self.assertIn("combat.performAction", rig.calls(out))
        for s in out["steps"]:
            if s.get("call") == "combat.performAction":
                self.assertTrue(rig.brain.gates.check(s, rig.world, "battle").ok)


class KeptLogs(unittest.TestCase):
    def test_a_description_names_its_tile(self):
        self.assertEqual(K.tile_of("Phantom Step: dauntless ... on <b>F4</b>"), "F4")
        self.assertEqual(K.tile_of("Defensive Stance: x on <b>h5</b>.  It is now dauntless's turn."), "H5")
        self.assertIsNone(K.tile_of("DDXXD stands and does nothing. "))
        self.assertEqual(K.log_tiles({"*.id": ["a", "b"], "*.description": ["x", "y on <b>J8</b>"]}),
                         {"a": None, "b": "J8"})
        self.assertIsNone(K.log_tiles({"*.id": ["a"], "*.description": []}))

    def test_the_closing_batch_reads_the_tiles_and_they_are_kept(self):
        rig = Rig()
        battle, ents, _ = start_fight(rig, "B1")
        out = gone(rig, "B1")
        reads = [s for s in out["steps"] if s.get("call") == "combat.getBattleEntries"]
        self.assertEqual(reads, [K.described("B1")])
        self.assertEqual(reads[0]["select"], ["*.id", "*.description"])     # the polls never carry descriptions
        path = os.path.join(rig.combat.fights, "B1_entries.json")
        with open(path, encoding="utf8") as f:
            ids = json.load(f)["*.id"]
        desc = [f"x on <b>{chr(65 + i % 13)}{1 + i % 9}</b>" for i in range(len(ids))]
        rig.tick(res("combat.getBattleEntries", {"*.id": ids, "*.description": desc},
                     {"battleId": "B1", "limit": K.LOG_KEEP}))
        with open(path, encoding="utf8") as f:
            saved = json.load(f)
        self.assertEqual(saved["*.tile"], [K.tile_of(d) for d in desc])
        self.assertEqual(rig.world["records"]["log_tiles_due"], [])

    def test_the_polls_in_a_fight_stay_small(self):
        self.assertNotIn("*.description", K.entries("B1", 8)["select"])
        self.assertNotIn("*.description", K.entries("B1", 8, whole=True)["select"])

    def test_a_fight_is_pushed_only_from_the_accounts_own_folder(self):
        combat = Combat(tempfile.mkdtemp(), spawn=False)
        combat.keep_fight("B1")
        self.assertEqual(combat.spawned, [])                                  # a test or rehearsal folder: never
        real = Combat(spawn=False)
        with mock.patch.dict(os.environ, {}, clear=False):
            for k in ("TNR_PLAYER_LIVE", "TNR_PLAYER_FIGHTS", "TNR_PLAYER_KEEP"):
                os.environ.pop(k, None)
            real.keep_fight("-CH613DKHOF7stgVwrDNR")
            self.assertEqual(real.spawned[-1][1:], ["-m", "player.keep", "-CH613DKHOF7stgVwrDNR"])
            os.environ["TNR_PLAYER_KEEP"] = "0"
            n = len(real.spawned)
            real.keep_fight("B2")
            self.assertEqual(len(real.spawned), n)

    def test_keep_commits_only_the_fight_files_to_main(self):
        tmp = tempfile.mkdtemp()
        git = lambda *a, cwd=None: subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True,  # noqa: E731
                                                 env=dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@x.invalid",
                                                          GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@x.invalid"))
        origin, work = os.path.join(tmp, "origin.git"), os.path.join(tmp, "work")
        git("init", "-q", "--bare", "-b", "main", origin)
        git("clone", "-q", origin, work)
        with open(os.path.join(work, "README"), "w") as f:
            f.write("x\n")
        git("add", "README", cwd=work)
        git("-c", "commit.gpgsign=false", "commit", "-q", "-m", "base", cwd=work)
        git("push", "-q", "origin", "HEAD:main", cwd=work)
        fights = os.path.join(work, "state", "player", C.ACCOUNT, "fights")
        bid = "6_UqBB_MXSIqobeRrfmdd"
        os.makedirs(os.path.join(fights, "live_states"))
        for name in (f"{bid}_entries.json", f"{bid}_meta.json", os.path.join("live_states", f"{bid}.json")):
            with open(os.path.join(fights, name), "w") as f:
                f.write("{}\n")
        env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@x.invalid", GIT_COMMITTER_NAME="t",
                   GIT_COMMITTER_EMAIL="t@x.invalid")
        with mock.patch.object(keep, "REPO", work), mock.patch.dict(os.environ, env):
            files = keep.fight_files(bid, fights)
            self.assertEqual(len(files), 3)
            first = keep.keep(bid, files)
            self.assertTrue(first.get("commit"), first)
            again = keep.keep(bid, files)
            self.assertIsNone(again["commit"])                                # nothing new: no commit
            stray = os.path.join(work, "README")
            self.assertIn("error", keep.keep(bid, [stray]))                    # only fight files
        listed = subprocess.run(["git", "--git-dir", origin, "show", "--name-only", "--format=", "main"],
                                capture_output=True, text=True, check=True).stdout.split()
        self.assertEqual(sorted(listed), sorted(f"state/player/{C.ACCOUNT}/fights/" + os.path.relpath(p, fights)
                                                for p in files))
        status = subprocess.run(["git", "status", "--porcelain"], cwd=work, capture_output=True, text=True).stdout
        self.assertIn("?? state/", status)                                    # the working tree was not touched

    def test_the_kits_of_the_players_in_a_fight_are_kept_with_it(self):
        """AP run 2 saved the kit of every player it met and pushed none: on main the reviews of its two losses
        had no kit to read him from."""
        tmp = tempfile.mkdtemp()
        env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@x.invalid", GIT_COMMITTER_NAME="t",
                   GIT_COMMITTER_EMAIL="t@x.invalid")
        git = lambda *a, cwd=None: subprocess.run(["git", *a], cwd=cwd, check=True, capture_output=True, env=env)  # noqa: E731
        origin, work = os.path.join(tmp, "origin.git"), os.path.join(tmp, "work")
        git("init", "-q", "--bare", "-b", "main", origin)
        git("clone", "-q", origin, work)
        git("-c", "commit.gpgsign=false", "commit", "-q", "--allow-empty", "-m", "base", cwd=work)
        git("push", "-q", "origin", "HEAD:main", cwd=work)
        fights, kits = os.path.join(work, "state", "player", C.ACCOUNT, "fights"), os.path.join(work, keep.KITS)
        os.makedirs(fights), os.makedirs(kits)
        bid, him, other = "9j3DIjLVbD_9b1RmJ69UM", "user_2SAAMvwqsbjyS2Qd8A2pB0Gzn4W", "user_38UxfHXcwBi8IyvtblWpaqkoX7y"
        with open(os.path.join(fights, f"{bid}_entries.json"), "w") as f:
            json.dump({"*.userId": [him, C.ME, "aTGxSsvezuwZbqj2rPHQN", None, him]}, f)   # an AI's id is no player's
        for name in (him, other, "aTGxSsvezuwZbqj2rPHQN", C.ME):
            with open(os.path.join(kits, name + ".json"), "w") as f:
                f.write("{}\n")
        with mock.patch.object(keep, "REPO", work), mock.patch.dict(os.environ, env):
            files = keep.fight_files(bid, fights)
            self.assertEqual([os.path.relpath(p, work) for p in files],
                             [f"state/player/{C.ACCOUNT}/fights/{bid}_entries.json", f"{keep.KITS}/{him}.json"])
            self.assertTrue(keep.keep(bid, files).get("commit"))
            for stray in (other, C.ME, "aTGxSsvezuwZbqj2rPHQN"):               # not this fight's opponent: refused
                self.assertIn("error", keep.keep(bid, [os.path.join(kits, stray + ".json")]), stray)
            self.assertIn("error", keep.keep("B-other", [os.path.join(kits, him + ".json")]))   # nor for another fight
        listed = subprocess.run(["git", "--git-dir", origin, "show", "--name-only", "--format=", "main"],
                                capture_output=True, text=True, check=True).stdout.split()
        self.assertEqual(sorted(listed), sorted([f"state/player/{C.ACCOUNT}/fights/{bid}_entries.json",
                                                 f"{keep.KITS}/{him}.json"]))


class StoppedWithNoFolder(unittest.TestCase):
    def test_brain_stopped_on_a_folder_that_is_not_there_yet(self):
        live = os.path.join(tempfile.mkdtemp(), "not-yet", "live")
        buf = io.StringIO()
        self.assertEqual(client.stopped(live, [], out=buf), 0)
        json.loads(buf.getvalue().strip().splitlines()[-1])


if __name__ == "__main__":
    unittest.main()
