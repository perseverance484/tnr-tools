"""Account constants, limits and paths. One place; ported from the pilot (state/player/dauntless/tools/pilot.py).

Nothing here is a credential. The brain never holds one: it prints call descriptions and a relay carries them.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACCOUNT = "dauntless"
ACCOUNT_DIR = os.path.join(ROOT, "state", "player", ACCOUNT)
TOOLS = os.path.join(ACCOUNT_DIR, "tools")                 # the combat tools the brain still runs (player/combat.py)
ALLOWLIST = os.path.join(ROOT, "data", "player_allowlist.json")
GOALS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "goals.json")
DO_NOT_ATTACK = os.path.join(ACCOUNT_DIR, "do_not_attack.md")


def live_dir():
    """Runtime state (world model, outbox, inbox, logs). Gitignored. TNR_PLAYER_LIVE points tests at a temp folder."""
    return os.environ.get("TNR_PLAYER_LIVE") or os.path.join(ACCOUNT_DIR, "live")


def fights_dir():
    """Where the combat tools keep fight logs and their own live files (fights/live). TNR_PLAYER_FIGHTS for tests."""
    return os.environ.get("TNR_PLAYER_FIGHTS") or os.path.join(ACCOUNT_DIR, "fights")


# ---------------------------------------------------------------- the account (from pilot.py)
ME = "user_37qazcrgUPldBPI65bb25DQiCjz"
ME_NAME = "dauntless"
HOME_VILLAGE = "9FZf8b9E7tZJZTaChmhHB"
HOME_SECTOR = 177
CIRCUIT = [1538, 1490, 1335, 99]        # Shirohana, Tsukimori, Akasumi, Risen: where active enemies gather
ME_CARD = {"level": 100, "username": "dauntless",
           "avatar": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJ2ZSxgqnMXlcRpYmJ5do0zKw4Qx6PVEtBa9b8",
           "avatarLight": "https://ui0arpl8sm.ufs.sh/f/Hzww9EQvYURJEJNnVieLfKL5D7TAFe29bymSaPCIQ846MdzG"}
FULL_POTION = "IRfg2NFKKYe0ynroXI7qZ"   # user item: HP to full out of combat (ramen refills chakra and stamina only)
MAX_HP = 5050.0

# ---------------------------------------------------------------- play (from pilot.py; director rulings cited there)
HEAL_BELOW = 0.95        # fights start at full health
POOLS_BELOW = 0.5        # chakra / stamina floor before ramen
HEAL_RETRY = 600         # s a heal that changed nothing is not tried again
MIN_LEVEL = 90           # targets under this are not farmed
LOST_TO_HOURS = 6        # a player who just beat me is not attacked again for this long
SKIP_FOR = {"bracket": 6 * 3600, "village": 24 * 3600, "immune": 120, "move": 60, "other": 600}
SENSORY_EVERY = 31       # s; the game's cooldown is 30
HUNT_WAIT = 8.0          # s before a hunt scan: about 6 scans a minute
WATCH_WAIT = 7.0         # s between guard reads: inside the 15 s lobby before an attack lands
TRAVEL_RETRY = 3.0       # s between tries to finish a trip that has not landed

# ---------------------------------------------------------------- battle (design section 4.6)
POLL_GAP = 3.0           # s before the first poll of his turn
POLL_GAP_MAX = 6.0       # s: polls back off to this on his turn (fewer batches for the relay)
ACTION_GAP = 1.2         # s between the actions of one turn (director: not all at once)
TURN_LIMIT = 60.0        # s the game gives a turn
FIRE_BY = 20.0           # s from turn start by which the actions are out
LAST_GOOD_READ_AT = 12.0  # s from turn start after which a missing exact read is not waited for
BEST_LINE_AT = 15.0      # s from turn start at which the planner is cut off and the best line so far is fired
LATE_TURN = TURN_LIMIT - 20.0   # a turn that lands later than this is a finding
HANDOFF_WAIT = 40.0      # s of each of my turns left to the director in director mode
KIT_TRIES = 3            # tries to read an opponent's kit in a fight
ENTRIES_START = 200      # log lines read when a battle starts
ENTRIES_POLL = 8         # log lines read on each poll

# ---------------------------------------------------------------- calls a minute (design section 4.6; RUL-2026-11-11-149 item 6)
CALL_LIMIT = 30          # the connector's limit for the whole account, any client
WORLD_CAP = 20           # the world lane outside fights
RATE_BACKOFF = 6.0       # s to wait after "Too Many Requests" on the world lane
CALL_COST = 0.4          # s a relayed call is assumed to take, for pacing

# ---------------------------------------------------------------- the relay (design section 4.7)
ROTATE_AFTER_TOKENS = 60_000    # a relay is rotated once its context has grown this much past its first batch
ROTATE_HARD_CAP = 150_000       # or once its context is this large, whatever it started at
STALE_OUTBOX = 10.0             # s a batch may wait for a relay before the watchdog alerts
BRAIN_WAIT = 0.05               # s between looks at the outbox and inbox files

# ---------------------------------------------------------------- spend (design section 9 item 3)
RESERVE = 500_000        # ryo never spent (the pilot's value, from restock.py; not ruled on)
DAILY_CAP = 50_000_000   # ryo: a purchase over this, or one that takes the UTC day past it, is asked first
                         # (RUL-2026-11-11-152 item 3: "Over 50m ryo, ask")
TRANSFER_EVERY = 86_400  # s between two level transfers (RUL-2026-11-11-152 item 5: 24 h from the last one)


def goals():
    with open(GOALS, encoding="utf8") as f:
        return json.load(f)
