"""The combat engine, as the brain sees it: the one adapter to the combat tools under state/player/<account>/tools.

Until AP4 folds them into the player package, the planner, the offline engine, the opponent models and the
post-fight review stay where they are and keep their own files (fights/live/<battle>.json, <battle>_bases.json,
the turn file, fights/<battle>_entries.json). This module is the only place in player/ that knows about them, and
it registers each one as a model or a data feed so the wiring test can see it.

Nothing here talks to the game.
"""
import json
import os
import re
import subprocess
import sys
import time

from . import calls as K
from . import config as C
from .registry import REGISTRY

REGISTRY.model("planner", "the turn planner (planner2.py; turn.py while AP4 has not consolidated them)", "planner2.py")
REGISTRY.model("dossier", "the opponent's kit, weapons and imbues, read before the first action", "opponent_kit.py")
REGISTRY.model("opponents", "opponent models from every logged fight, rebuilt after each one", "opponents.py")
REGISTRY.model("postmortem", "the per-fight review that feeds the solution library", "postmortem.py")
REGISTRY.feed("fight_bases", "both kits' base damage for this matchup, from the offline engine", "fight_bases.py")
REGISTRY.feed("live_state", "the exact live effect list of every round, kept per battle", "fights/live_states")
REGISTRY.feed("fight_log", "the battle log, saved when the fight ends (the game deletes it)", "fights/*_entries.json")
REGISTRY.feed("harvest", "other players' battle logs, read between fights", "harvest.py")

PERM_KEYS = ("type", "targetId", "creatorId", "power", "powerPerLevel", "level", "calculation", "direction", "elements",
             "statTypes", "generalTypes", "fromType", "timedBuffExpiresAt", "rounds", "createdRound")
LIVE_KEYS = ("type", "targetId", "creatorId", "actionId", "power", "powerPerLevel", "level", "calculation", "direction",
             "elements", "fromType", "rounds", "createdRound", "castThisRound", "isNew", "poolsAffected",
             "timedBuffExpiresAt", "statTypes", "generalTypes")
GROUND_KEYS = ("type", "creatorId", "longitude", "latitude", "curHealth", "maxHealth", "absorbPercentage", "power",
               "rounds", "createdRound")


def live_effects(effects):
    """The live effect list, compact: what planner2.from_live needs (a wound keeps its recorded hit)."""
    out = []
    for e in effects or []:
        if not isinstance(e, dict):
            continue
        x = {k: e.get(k) for k in LIVE_KEYS if e.get(k) is not None}
        od = (e.get("timeTracker") or {}).get("originalDamage")
        if od:
            x["timeTracker"] = {"originalDamage": od}
        out.append(x)
    return out


def perm_effects(effects):
    """The permanent effects (no round count) from a whole effect list, compact."""
    return [{k: e.get(k) for k in PERM_KEYS if e.get(k) is not None}
            for e in effects or [] if isinstance(e, dict) and e.get("rounds") is None]


def ground_effects(raw):
    """The ground list, compact: barriers (tile, HP, absorb) and tile effects for the planner."""
    return [{k: g.get(k) for k in GROUND_KEYS if g.get(k) is not None} for g in raw or []
            if isinstance(g, dict) and g.get("type") not in ("visual", "move")]


def _tools():
    if C.TOOLS not in sys.path:
        sys.path.insert(0, C.TOOLS)


class Combat:
    """spawn=False keeps the background jobs (fight bases, model rebuild, post-mortem) from starting: the tests."""

    def __init__(self, fights=None, spawn=True):
        self.fights = fights or C.fights_dir()
        self.live = os.path.join(self.fights, "live")
        self.spawn = spawn
        self.spawned = []                         # what would have been started, for the tests

    # ------------------------------------------------------------ the one switch still read from the pilot's folder
    def _switch(self, name):
        try:
            with open(os.path.join(self.live, name), encoding="utf8") as f:
                return f.read().strip()
        except OSError:
            return ""

    def planner_choice(self):
        """fights/live/planner_choice: "planner2" or "turn" (the pilot's default). The pilot's own switch file, kept
        so the brain and the pilot fight with the same planner; it goes when AP4 leaves one planner."""
        return self._switch("planner_choice") or "turn"

    def pilot_handover(self):
        """What the brain takes over from the pilot the first time it starts on this account: the Full Potion's
        current user-item id (the pilot's restock keeps it; AP2's restock will), and who not to attack again yet."""
        try:
            with open(os.path.join(self.live, "pilot.json"), encoding="utf8") as f:
                st = json.load(f)
        except (OSError, ValueError):
            return {}
        return {k: st[k] for k in ("full_potion_uid", "lost_to", "skip") if st.get(k)}

    # ------------------------------------------------------------ the dossier
    def kit_path(self, user_id):
        return os.path.join(C.ROOT, "harness", "pvp_turn", "kit", "opponents", f"{user_id}.json")

    def kit_known(self, user_id):
        return os.path.exists(self.kit_path(user_id))

    def save_kit(self, user_id, data):
        """Save his equipped kit from a jutsu.getPublicUserJutsus answer. A bad read never stops the player."""
        try:
            _tools()
            import opponent_kit
            opponent_kit.save_kit(user_id, data or {})
            return True
        except Exception:  # noqa: BLE001
            return False

    def learn_weapons(self, foe, live):
        """His weapons and their imbues, learned from what they just applied. True when his kit changed."""
        try:
            _tools()
            import opponent_kit
            return bool(opponent_kit.learn_weapons(foe, live))
        except Exception:  # noqa: BLE001
            return False

    def absorb(self, results):
        """Save every kit read that came back, whoever asked for it (the hunt before an attack, the fight after)."""
        for r in results:
            if r.endpoint == "jutsu.getPublicUserJutsus" and not r.error and r.input.get("userId"):
                self.save_kit(r.input["userId"], r.data)

    # ------------------------------------------------------------ files the combat tools read
    def _save(self, path, obj):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = f"{path}.{os.getpid()}"
        with open(tmp, "w", encoding="utf8") as f:
            json.dump(obj, f)
        os.replace(tmp, path)

    def write_cache(self, bid, state, battle=None):
        """fights/live/<battle>.json: the battle state in the shape fight_bases.py and the planners read."""
        self._save(os.path.join(self.live, f"{bid}.json"), dict(state, battle=battle) if battle is not None else state)

    def _popen(self, argv, stdout=None):
        self.spawned.append(argv)
        if not self.spawn:
            return
        try:
            subprocess.Popen(argv, stdout=stdout or subprocess.DEVNULL, stderr=subprocess.STDOUT if stdout else
                             subprocess.DEVNULL, start_new_session=True)
        except OSError:
            pass

    def start_fight_bases(self, bid):
        self._popen([sys.executable, os.path.join(C.TOOLS, "fight_bases.py"), bid])

    # ------------------------------------------------------------ the planner
    def plan_turn(self, bid, battle, entries, enemy, exact=False, ban=(), seconds=None):
        """(plan, how). plan: [{actionId, longitude, latitude, name}, ...] or None. seconds: what is left before the
        best line so far must be fired; each planner run is cut to it, and none is started with no time left."""
        path = os.path.join(self.live, f"{bid}.turn.txt")
        os.makedirs(self.live, exist_ok=True)
        rows = entries[::-1]                                   # the planners read newest-first, like the connector
        with open(path, "w", encoding="utf8") as f:
            f.write(json.dumps(battle) + "\n" +
                    json.dumps({k: [r[i] for r in rows] for i, k in enumerate(K.ENT) if k != "*.id"}) + "\n")
        t0 = time.time()
        bans = ("--ban", ",".join(ban)) if ban else ()
        if self.planner_choice() == "planner2":
            tries = [("planner2.py", bans, 6.0), ("turn.py", ("--no-engine", "--keep", "6", "--cash", "3") + bans, 6.0)]
        else:
            tries = ([("turn.py", ("--fast",) + bans, 9.0)] if exact else []) + \
                [("turn.py", ("--no-engine",) + bans, 6.0), ("planner2.py", bans, 6.0)]
        tries.append(("planner2.py", (), 10.0))                # last resort: no bans, long budget
        errs = []
        for script, extra, budget in tries:
            left = None if seconds is None else seconds - (time.time() - t0)
            if left is not None and left < 0.5:
                errs.append("out of time")
                break
            try:
                proc = subprocess.run([sys.executable, os.path.join(C.TOOLS, script), path, "--battle", bid, "--top",
                                       "1", "--enemy", enemy, *extra], capture_output=True, text=True,
                                      timeout=budget if left is None else min(budget, left))
                out = proc.stdout
            except subprocess.TimeoutExpired:
                errs.append(f"{script} cut off")
                continue
            m = re.search(r"^FIRE: (.*)$", out, re.M)
            if m:
                return json.loads(m.group(1)), f"{time.time() - t0:.1f}s {script.split('.')[0]}" + \
                    (" engine" if "--fast" in extra else "")
            errs.append(f"{script}: " + ((proc.stderr.strip().splitlines() or out.strip().splitlines()
                                          or ["no output"])[-1])[:120])
        return None, "planner failed: " + " | ".join(errs)

    # ------------------------------------------------------------ the end of a fight
    def log_says_lost(self, state):
        """My last seen HP minus the damage the log shows on me after it (heals added back) is gone."""
        try:
            _tools()
            import exam
            b = state.get("battle") or {}
            users = b.get("battle.usersState.*.userId") or []
            hp = b["battle.usersState.*.curHealth"][users.index(C.ME)]
            rows = [(e[1], e[2], e[3], e[4]) for e in (state.get("entries") or [])[state.get("n_at_battle", 10 ** 9):]]
            track = exam.hp_track(rows + [(0, None, None, [])], [C.ME_NAME])
            return hp - (C.MAX_HP - track[-1][C.ME_NAME]) <= 0
        except Exception:  # noqa: BLE001
            return False

    def turning_point(self, state):
        """The round that decided the fight, from the log's own HP count: the round with the widest gap between what
        I lost and what he lost. None when the log cannot say."""
        try:
            _tools()
            import exam
            enemy = state.get("enemy")
            rows = [(e[1], e[2], e[3], e[4]) for e in state.get("entries") or []]
            track = exam.hp_track(rows + [(0, None, None, [])], [C.ME_NAME, enemy])
            per = {}
            for row, before, after in zip(rows, track, track[1:]):
                d = per.setdefault(row[0], [0.0, 0.0])
                d[0] += before[C.ME_NAME] - after[C.ME_NAME]
                d[1] += before[enemy] - after[enemy]
            rnd, (mine, his) = max(per.items(), key=lambda kv: abs(kv[1][0] - kv[1][1]))
            if abs(mine - his) < 1:
                return None
            return f"round {rnd}: I lost {mine:.0f} HP, {enemy} lost {his:.0f}"
        except Exception:  # noqa: BLE001
            return None

    def close_fight(self, bid, state, covered, director_mode):
        """Keep the fight for the tools that learn from it (the game deletes the log): the log, who played which
        round, the exact live state of every round; then rebuild the opponent models and review the fight."""
        rows = (state.get("entries") or [])[::-1]
        if rows:
            self._save(os.path.join(self.fights, f"{bid}_entries.json"),
                       {k: [r[i] for r in rows] for i, k in enumerate(K.ENT)})
            self._save(os.path.join(self.fights, f"{bid}_meta.json"),
                       {"director_mode": director_mode, "pilot_rounds": covered})
        if state.get("live_hist"):
            self._save(os.path.join(self.fights, "live_states", f"{bid}.json"), state["live_hist"])
        self._popen([sys.executable, os.path.join(C.TOOLS, "opponents.py"), "build"])
        out = None
        if self.spawn:
            os.makedirs(os.path.join(self.fights, "postmortems"), exist_ok=True)
            out = open(os.path.join(self.fights, "postmortems", f"{bid}.txt"), "w")  # noqa: SIM115 (the child owns it)
        self._popen(["nice", "-n", "15", sys.executable, os.path.join(C.TOOLS, "postmortem.py"), bid[:8]], stdout=out)

    # ------------------------------------------------------------ the harvest feed
    def harvest(self):
        """The harvest module, pointed at this account's fights folder."""
        _tools()
        import harvest
        harvest.OBS = os.path.join(self.fights, "observed")
        harvest.STATE = os.path.join(harvest.OBS, "harvest.json")
        return harvest

    def harvest_seed_ids(self):
        """User ids from the logged fights, to seed the harvest list."""
        try:
            _tools()
            import opponents
            return [u for _, _, rows, _ in opponents.load_logs() for _, u, _, _ in rows]
        except Exception:  # noqa: BLE001
            return []
