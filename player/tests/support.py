"""Shared pieces for the player tests. Socket-free: a temporary live folder, a clock the test moves, a combat
adapter that starts no background job, and battle states from logged fights (state/player/dauntless/tools/tests)."""
import json
import os
import tempfile

from player import calls as K, config as C
from player.brain import Brain
from player.combat import Combat
from player.gates import Gates
from player.world import RATE_LIMITED, Result

FIXTURES = os.path.join(C.TOOLS, "tests")
FOE = "user_2q6t0HJD3ACwbIV3o0bX7pfdn5m"          # AngelSaber in angelsaber_r3.txt
LINE = [{"actionId": "stormblade_id", "longitude": 6, "latitude": 4, "name": "stormblade"},
        {"actionId": "kunai_id", "longitude": 6, "latitude": 4, "name": "kunai"}]
DNA = """# Do not attack
| Player | Village | Why | Added |
|---|---|---|---|
| Friend | Risen | Director: ally | 2026-11-09 |
| Shisui | user_shisui | Director | 2026-11-10 |

## Do not snipe (no third-party jumps after their fights)
| Player | Village | Why | Added |
|---|---|---|---|
| AngelSaber | Shirohana | Director | 2026-11-09 |

## Temporary holds
- 2026-11-10 16:22-16:52 UTC: Luka and 4qua. Director: leave them be.
"""


def fixture(name="angelsaber_r3.txt"):
    """(battle read, log entries) of a logged state: my turn, round 3."""
    with open(os.path.join(FIXTURES, name), encoding="utf8") as f:
        battle, ents = [json.loads(line) for line in f.read().splitlines() if line.strip()]
    n = len(ents["*.battleRound"])
    ents["*.id"] = [f"e{n - i}" for i in range(n)]
    return battle, ents


# What the offline catalog says of the items the upkeep activities handle (harness/pvp_turn/kit/catalog.json,
# read 2026-11-12), and of two that are made up for the tests: an armour, and a thing sold for reputation.
CATALOG = {
    "6DnJn4x6LWWXtBu7UZybb": {"name": "Dr. Kim's Miracle Potion", "inShop": True, "cost": 150000, "repsCost": 0,
                              "seichiSilverCost": 0, "stackSize": 100, "maxDurability": 100},
    "TtYPd-LcXKeK3sMuhq1TP": {"name": "Elite Smoke Bomb", "inShop": True, "cost": 50000, "repsCost": 0,
                              "seichiSilverCost": 0, "stackSize": 100, "maxDurability": 100},
    "rsc2uO5QuffXzejfhwF_F": {"name": "Panacea", "inShop": True, "cost": 55000, "repsCost": 0,
                              "seichiSilverCost": 0, "stackSize": 100, "maxDurability": 100},
    "tZTvqYWiAc_OrY64nDvIo": {"name": "Chakra Pill", "inShop": True, "cost": 1000, "repsCost": 0,
                              "seichiSilverCost": 0, "stackSize": 100, "maxDurability": 100},
    "yVNeLzxHSFkNpTPnlm7yQ": {"name": "Bloodthorn Kunai", "inShop": False, "cost": 1, "stackSize": 100,
                              "maxDurability": 100},
    "1ovHq7jsGdut2fSNKs5q_": {"name": "Repair Kit", "inShop": False, "cost": 1, "stackSize": 9999,
                              "maxDurability": 100},
    "GMF1JZ0MChUHc7AtnKABw": {"name": "Ikazuchi Kunai", "inShop": False, "cost": 1, "stackSize": 100,
                              "maxDurability": 100},
    "armour_id": {"name": "Kaeruun Armor", "inShop": False, "cost": 1, "stackSize": 1, "maxDurability": 400},
    "premium_id": {"name": "Reputation Charm", "inShop": True, "cost": 10, "repsCost": 5, "stackSize": 10},
}


class StubCombat(Combat):
    """No planner subprocess and no background job: plan_turn answers from `line`, and every use is counted."""

    def __init__(self, fights):
        super().__init__(fights, spawn=False)
        self.line, self.how, self.kits, self.saved, self.used = list(LINE), "0.1s stub", set(), [], {}
        self.lost_by_log = False
        self.plan_args = []

    def _count(self, name):
        self.used[name] = self.used.get(name, 0) + 1

    def kit_known(self, user_id):
        return user_id in self.kits

    def save_kit(self, user_id, data):
        self._count("dossier")
        self.saved.append(user_id)
        self.kits.add(user_id)
        return True

    def learn_weapons(self, foe, live):
        self._count("dossier")
        return False

    def plan_turn(self, bid, battle, entries, enemy, exact=False, ban=(), seconds=None):
        self._count("planner")
        self.plan_args.append({"ban": list(ban), "seconds": seconds, "live": "battle.liveEffects" in battle})
        if seconds is not None and seconds < 0.5:
            return None, "planner failed: out of time"
        line = [a for a in (self.line or []) if a["actionId"] not in ban]
        return (line or None), self.how if line else "planner failed: stub"

    def log_says_lost(self, state):
        return self.lost_by_log

    def turning_point(self, state):
        return "round 2: I lost 900 HP, he lost 100"

    def harvest_seed_ids(self):
        return ["user_seed1"]

    def item_record(self, item_id):
        self._count("catalog")
        return dict(CATALOG.get(item_id) or {})

    def write_equipped(self, slots):
        self._count("equipped")
        super().write_equipped(slots)

    def write_cache(self, bid, state, battle=None):
        self._count("cache")
        super().write_cache(bid, state, battle)

    def start_fight_bases(self, bid):
        self._count("fight_bases")
        super().start_fight_bases(bid)

    def archive_state(self, bid, record):
        self._count("live_state")
        super().archive_state(bid, record)

    def close_fight(self, bid, state, covered, director_mode):
        self._count("fight_log")
        super().close_fight(bid, state, covered, director_mode)


UPKEEP = ("restock", "repair", "training", "equipment", "bank")


def my_items(*rows):
    """A read of my items: rows of (user item id, item id, quantity, slot or None, stored at home, durability)."""
    cols = list(zip(*rows)) if rows else [()] * 6
    return res("item.getUserItems", {f"*.{k}": list(c) for k, c in zip(K.ITEM_COLS, cols)})


class Rig:
    """A brain in a temporary folder with a clock the test moves."""

    def __init__(self, mode="hunt", combat=None, upkeep=False):
        """upkeep: leave the AP2 upkeep activities switched on. The tests written before them ask for a hunt, a
        fight or a relay and nothing else, so for those they are off, the way the director switches one off."""
        self.dir = tempfile.mkdtemp(prefix="player-test-")
        self.t = 1_800_000_000.0
        self.dna = os.path.join(self.dir, "do_not_attack.md")
        with open(self.dna, "w", encoding="utf8") as f:
            f.write(DNA)
        self.combat, self.upkeep = combat or StubCombat(os.path.join(self.dir, "fights")), upkeep
        self.brain = self.new_brain()
        self.world["control"]["mode"] = mode

    def new_brain(self):
        """A brain started fresh on the same folder: what a restart does."""
        self.brain = Brain(self.dir, clock=lambda: self.t, combat=self.combat, gates=Gates(dna_path=self.dna))
        if not self.upkeep:                         # off, unless the world model on disk already says otherwise
            for name in UPKEEP:
                self.brain.world["control"]["activities"].setdefault(name, False)
        return self.brain

    @property
    def world(self):
        return self.brain.world

    def tick(self, *results, dt=1.0):
        """Move the clock, hand the results in, return the batch."""
        self.t += dt
        return self.brain.handle([r._replace(at=self.t) if r.at is None else r for r in results])

    def calls(self, out):
        return [s["call"] for s in out["steps"] if "call" in s]

    def events(self, kind=None):
        try:
            with open(os.path.join(self.dir, "events.jsonl"), encoding="utf8") as f:
                rows = [json.loads(line) for line in f]
        except OSError:
            return []
        return [r for r in rows if kind is None or r["kind"] == kind]

    def status(self):
        with open(os.path.join(self.dir, "status.json"), encoding="utf8") as f:
            return json.load(f)


class Ledger:
    """Every call the budget schedules, kept for the whole test (the budget itself forgets after a minute):
    rows of (time it runs, lane, endpoint)."""

    def __init__(self, rig):
        self.rows = [(c[0], c[1], "") for c in rig.world["budget"]["calls"]]
        budget, real = rig.brain.budget, rig.brain.budget.pace

        def pace(steps, lane, start=None):
            out, waited = real(steps, lane, start)
            calls = [s["call"] for s in out if "call" in s]
            new = rig.world["budget"]["calls"][-len(calls):] if calls else []
            self.rows += [(e[0], e[1], c) for e, c in zip(new, calls)]
            return out, waited
        budget.pace = pace

    def worst(self, lane=None, window=60.0):
        """The most calls in any rolling minute (of one lane, or of all)."""
        times = sorted(r[0] for r in self.rows if lane is None or r[1] == lane)
        return max((sum(1 for u in times if t - window < u <= t) for t in times), default=0)


def res(endpoint, data=None, inp=None, error=None):
    return Result(endpoint, inp or {}, data, error, None)


def limited(endpoint, inp=None):
    return Result(endpoint, inp or {}, None, RATE_LIMITED, None)


def user(status="AWAKE", hp=5050, sector=1538, pos=(10, 10), bid=None, **more):
    d = {"userData.status": status, "userData.battleId": bid, "userData.curHealth": hp, "userData.maxHealth": 5050,
         "userData.sector": sector, "userData.longitude": pos[0], "userData.latitude": pos[1],
         "userData.curChakra": 100, "userData.maxChakra": 100, "userData.curStamina": 100,
         "userData.maxStamina": 100, "userData.money": 150_000, "userData.bank": 50_000_000,
         "userData.curEnergy": 0}
    d.update({f"userData.{k}": v for k, v in more.items()})
    return res("profile.getUser", d)


ROW = ("userId", "username", "longitude", "latitude", "status", "level", "villageId", "immunityUntil", "battleId")


def scan(rows, sector=1538):
    """rows: tuples in ROW order."""
    return res("travel.getSectorData", {f"users.*.{k}": [r[i] for r in rows] for i, k in enumerate(ROW)},
               {"sector": sector})


def battle_read(bid, battle):
    return res("combat.getBattle", dict(battle), {"battleId": bid})


def log_read(bid, ents):
    return res("combat.getBattleEntries", dict(ents), {"battleId": bid, "limit": 8})


def gone(rig, bid="B1", status="AWAKE", **tick):
    """The fight ends the way a deleted battle looks: its reads come back without it, and then my profile shows
    that I have left it. Returns the closing batch."""
    out = rig.tick(battle_read(bid, {}), **tick)
    assert "profile.getUser" in rig.calls(out), out          # an empty read alone ends nothing: my profile is asked
    out = rig.tick(battle_read(bid, {}), user(status), **tick)
    assert "BATTLE OVER" in out["note"], out
    return out


def start_fight(rig, bid="B1", battle=None, ents=None, effects=()):
    """Bring the rig to the first tick of a fight on the logged state; returns (battle, entries, the batch)."""
    fb, fe = fixture()
    battle, ents = battle or fb, ents or fe
    out = rig.tick(user("BATTLE", bid=bid))
    assert rig.calls(out)[:2] == ["combat.getBattle", "combat.getBattleEntries"], out
    read = dict(battle)
    read["battle.usersEffects"] = list(effects)
    out = rig.tick(battle_read(bid, read), log_read(bid, ents))
    return battle, ents, out
