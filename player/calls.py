"""Every call the player can ask for, in one place, each with the smallest select the brain uses (design 4.7).

A step is a dict: {"call": endpoint, "input": {...}, "select": [...]} for the connector, or {"wait": seconds}
for a pause. A step may carry "meta" (what the gates need to judge it: who is attacked, what it costs); meta never
leaves the brain. Ported from the pilot's c_* helpers; the selects are the ones the pilot runs live.

Lists are read as columns. The connector drops a missing key from its column instead of padding it, so a column
select is used only on keys every element carries, and readers check the lengths (ground_cols).
"""
from . import config as C


def call(endpoint, inp, select, **meta):
    step = {"call": endpoint, "input": inp, "select": list(select)}
    if meta:
        step["meta"] = meta
    return step


def wait(seconds):
    return {"wait": round(float(seconds), 1)}


def is_call(step):
    return "call" in step


USER_SEL = ["userData.status", "userData.battleId", "userData.curHealth", "userData.maxHealth", "userData.sector",
            "userData.longitude", "userData.latitude", "userData.curChakra", "userData.maxChakra",
            "userData.curStamina", "userData.maxStamina", "userData.money", "userData.bank", "userData.curEnergy",
            "userData.intelligence", "userData.willpower", "userData.dailyErrands"]


def user():
    return call("profile.getUser", {}, USER_SEL)


SECTOR_COLS = ("userId", "username", "longitude", "latitude", "status", "level", "villageId", "immunityUntil",
               "battleId")


def sector(sec):
    return call("travel.getSectorData", {"sector": sec}, [f"users.*.{k}" for k in SECTOR_COLS])


def move(cur, dest, sec):
    return call("travel.moveInSector", {"curLongitude": cur[0], "curLatitude": cur[1], "longitude": dest[0],
                                        "latitude": dest[1], "destLongitude": dest[0], "destLatitude": dest[1],
                                        "sector": sec, "villageId": C.HOME_VILLAGE, **C.ME_CARD}, ["success", "message"])


def attack(target, sec):
    """target: {userId, username, longitude, latitude}. The gates read meta.target against do_not_attack.md."""
    return call("combat.attackUser", {"userId": target["userId"], "longitude": target["longitude"],
                                      "latitude": target["latitude"], "sector": sec, "asset": "ground"},
                ["success", "message", "battleId"],
                target={"userId": target["userId"], "username": target.get("username")},
                third_party=bool(target.get("third_party")))


def sensory(sec):
    return call("stealth.useSensory", {"sector": sec}, ["success", "message"])


def trip(sec):
    """A trip: start it, try to finish it, and read where I am. A trip that has not landed is finished later."""
    return [call("travel.startGlobalMove", {"sector": sec}, ["success", "message", "data.travelFinishAt"]),
            call("travel.finishGlobalMove", {}, ["success", "message"]), user()]


def go(sec):
    """A trip, and a look at who is there."""
    return trip(sec) + [sector(sec)]


def finish_trip():
    return call("travel.finishGlobalMove", {}, ["success", "message"])


def wake():
    """The one switch between asleep and awake: it wakes a sleeper and puts a waker to bed."""
    return call("home.toggleSleep", {}, ["success", "message"])


# ---------------------------------------------------------------- battle
GROUND_COLS = ("type", "creatorId", "longitude", "latitude", "power", "rounds", "createdRound")
BARRIER_COLS = ("curHealth", "maxHealth", "absorbPercentage")
STATE_COLS = ("userId", "username", "curHealth", "maxHealth", "longitude", "latitude", "actionPoints", "isAi")
ENT = ("*.id", "*.battleRound", "*.userId", "*.actionId", "*.appliedEffects.*.txt")


def battle(bid, effects=False, ground=False):
    """effects: also the whole live effect list (both fighters' temporary and permanent effects). It is read whole:
    its elements do not all carry the same keys, so it cannot be read as columns. ground: the ground list, as the
    columns every ground effect carries plus the three only barriers carry."""
    return call("combat.getBattle", {"battleId": bid},
                ["battle.version", "battle.round", "battle.activeUserId"] +
                [f"battle.usersState.*.{k}" for k in STATE_COLS] +
                (["battle.usersEffects"] if effects else []) +
                ([f"battle.groundEffects.*.{k}" for k in GROUND_COLS + BARRIER_COLS] if ground else []))


def entries(bid, n, whole=False):
    """The battle log's last n lines. The effect texts come as one list per line, but a line with no effect is
    left out of that column; whole asks for each line's effects as they are, which always lines up."""
    return call("combat.getBattleEntries", {"battleId": bid, "limit": n},
                list(ENT[:4]) + ["*.appliedEffects"] if whole else list(ENT))


def _number(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _line(row):
    """A log line of the kinds every saved line has: an id that is text or a number, a round that is a number,
    a fighter and an action that are text."""
    return ((isinstance(row["*.id"], str) or _number(row["*.id"])) and _number(row["*.battleRound"])
            and isinstance(row["*.userId"], str) and isinstance(row["*.actionId"], str))


def _line_texts(line):
    """One line's effects, as the game sends them whole -> its texts."""
    if not isinstance(line, list):
        return []
    return [e["txt"] for e in line if isinstance(e, dict) and isinstance(e.get("txt"), str) and e["txt"]]


def log_rows(data):
    """A log read -> rows [id, round, user, action, texts], newest first. texts is None on every row when the read
    cannot say which line each text belongs to.

    None when the four plain columns do not line up, or when any line is not a whole one (_line). A row is
    checked before it is a row, so nothing that fails here is ever kept in a fight's state (review of c0006266,
    finding 1: an action that was an object was kept, and every tick after it failed)."""
    base = columns(data, "", ENT[:4])
    if base is None or not all(_line(row) for row in base):
        return None
    whole, texts = data.get("*.appliedEffects"), data.get(ENT[4])
    if isinstance(whole, list) and len(whole) == len(base):
        texts = [_line_texts(line) for line in whole]
    elif (not isinstance(texts, list) or len(texts) != len(base)
          or not all(isinstance(t, list) and all(isinstance(x, str) for x in t) for t in texts)):
        texts = [None] * len(base)
    return [[row[k] for k in ENT[:4]] + [t] for row, t in zip(base, texts)]


def kit(user_id):
    """An opponent's public equipped jutsu, for his dossier."""
    return call("jutsu.getPublicUserJutsus", {"userId": user_id}, ["*.jutsuId", "*.level", "*.equipped"])


def act(bid, action_id, x, y, version):
    return call("combat.performAction", {"battleId": bid, "actionId": action_id, "longitude": x, "latitude": y,
                                         "version": version}, ["notification"])


# ---------------------------------------------------------------- recovery
def potion(user_item_id):
    return call("item.consume", {"userItemId": user_item_id}, ["success", "message"])


def ramen(ryo=None):
    """ryo: what a large ramen has cost before (measured), or None when it has never been bought: the spend gate
    then counts the whole pocket."""
    return call("village.buyFood", {"ramen": "large"}, ["success", "message"], ryo=ryo)


def hospital():
    return call("hospital.npcHeal", {"villageId": C.HOME_VILLAGE}, ["success", "message"])


def ground_cols(read):
    """The ground columns of a getBattle read -> the ground list as dicts. None when the read had no ground columns
    (no ground on the field, or not asked); False when the columns do not line up (keep no ground from that read).
    The columns are popped from the read."""
    cols = {k: read.pop(f"battle.groundEffects.*.{k}", None) for k in GROUND_COLS + BARRIER_COLS}
    if all(v is None for v in cols.values()):
        return None
    if not all(v is None or isinstance(v, list) for v in cols.values()):
        return False
    base = [cols[k] or [] for k in GROUND_COLS]
    n = len(base[0])
    if any(len(c) != n for c in base):
        return False
    rows = [dict(zip(GROUND_COLS, x)) for x in zip(*base)]
    bars = [r for r in rows if r["type"] == "barrier"]
    bcols = [cols[k] or [] for k in BARRIER_COLS]
    if any(len(c) != len(bars) for c in bcols):
        return False
    for r, x in zip(bars, zip(*bcols)):
        r.update(dict(zip(BARRIER_COLS, x)))
    return rows


def columns(data, prefix, keys):
    """A column read -> rows. None when the columns are not all the same length (a key was missing somewhere), or
    when one of them is not a list at all."""
    cols = [data.get(f"{prefix}{k}") for k in keys]
    if not all(c is None or isinstance(c, list) for c in cols) or len({len(c or []) for c in cols}) > 1:
        return None
    return [dict(zip(keys, x)) for x in zip(*(c or [] for c in cols))]
