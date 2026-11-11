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


def go(sec):
    """A trip: start it, try to finish it, and read where I am. A trip that has not landed is finished later."""
    return [call("travel.startGlobalMove", {"sector": sec}, ["success", "message", "data.travelFinishAt"]),
            call("travel.finishGlobalMove", {}, ["success", "message"]), user(), sector(sec)]


def finish_trip():
    return call("travel.finishGlobalMove", {}, ["success", "message"])


def wake():
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


def entries(bid, n):
    return call("combat.getBattleEntries", {"battleId": bid, "limit": n}, list(ENT))


def kit(user_id):
    """An opponent's public equipped jutsu, for his dossier."""
    return call("jutsu.getPublicUserJutsus", {"userId": user_id}, ["*.jutsuId", "*.level", "*.equipped"])


def act(bid, action_id, x, y, version):
    return call("combat.performAction", {"battleId": bid, "actionId": action_id, "longitude": x, "latitude": y,
                                         "version": version}, ["notification"])


# ---------------------------------------------------------------- recovery
def potion(user_item_id):
    return call("item.consume", {"userItemId": user_item_id}, ["success", "message"])


def ramen():
    return call("village.buyFood", {"ramen": "large"}, ["success", "message"], ryo=None)


def hospital():
    return call("hospital.npcHeal", {"villageId": C.HOME_VILLAGE}, ["success", "message"])


def ground_cols(read):
    """The ground columns of a getBattle read -> the ground list as dicts. None when the read had no ground columns
    (no ground on the field, or not asked); False when the columns do not line up (keep no ground from that read).
    The columns are popped from the read."""
    cols = {k: read.pop(f"battle.groundEffects.*.{k}", None) for k in GROUND_COLS + BARRIER_COLS}
    if all(v is None for v in cols.values()):
        return None
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
    """A column read -> rows. None when the columns are not all the same length (a key was missing somewhere)."""
    cols = [data.get(f"{prefix}{k}") or [] for k in keys]
    if len({len(c) for c in cols}) > 1:
        return None
    return [dict(zip(keys, x)) for x in zip(*cols)]
