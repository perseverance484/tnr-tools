#!/usr/bin/env python3
"""The director's fight 2 critique as planner guards (AP test 2026-11-16, DDXXD at home, lost in round 9).

His words, typed after the fight (state/player/dauntless/pvp_playbook.md, "AP test fight 2"):

  "Phantom stepping off the center of Subaku Palace and within range of the center tile allowed the enemy to move
   into the center and thus no longer be debuffed by decreased damage taken. Essentially phantom stepping like that
   increased their damage. Using buff prevent at the end of the fight with a pill and offensive stance while better
   damage and defense options are available?? Set yourself behind massively there. Not using limit Breaker to pump
   damage during burst round? Not using aetherion during burst round? Using all buffs while enemy had clear and you
   did not have clear prevention active? That was a mess. Didnt try to use Danse Macabre or Chakra Resistance to
   prevent getting nuked even though they have damage mitigation effects that can stack with DR"

And on round 8 itself, asked why it picked Lotus Dance's buff prevent, a pill and a stance (rule 6):

  "Buff prevent does prevent the enemies buffs. The reason why it was a bad choice is because the next round was the
   final round... It should have prioritized something it could benefit from, the Buff prevent was never going to
   pay off. 2. My buffs were not blocked. Pill and stance is significantly less value than any other choices on the
   board... 3. It should have seen the nuke coming. Opponent had a burst window and a nuke available. Could have
   tried to seal and phantom step if they had debuff prevent, chakra resistance and subaku palace also work if they
   did not. Even chakra shield would have been good"

  "pretty much any attack except lotus dance would have been acceptable. Forgotten Ember Blade, Forbidden Chakra
   Fury and Shrapnel Clone Barrage are all high value there for their ability to give me more leverage over the
   enemy's hp pool. Danse would have been nice as an instant damage cut to the enemy's damage, and could've been
   paired with chakra resistance to attempt to survive the next round or with a buff(chakra overflow perhaps) to
   keep me alive long enough to go for the kill"

  On the wound tick: "I dont think chakra resistance or any damage reduction works on wound ticks themselves but yeah
   maybe if it cut the incoming damage i wouldve taken a smaller overall hit and then less wound damage also as a
   result." (The game agrees: a wound is a share of the hit that made it, and its tick is not adjusted by damage
   taken; the planners model it that way, shotplan.apply / planner2 apply.)

One rule per point, each a penalty in HP units on a bundle with its reason. Two users:
- the replay review (review_fight, run by postmortem.py after each fight and by `critique.py <battle id>`): every
  turn I played, checked against the rules, the director's way of going over a fight;
- the planners (turn.penalties, planner2.Planner.extras), as score terms, only with TNR_CRITIQUE=1 until
  tune_real.py shows they help against real opponents. The sizes are hand-set and named here, not tuned, and they
  are not hard bans: a line that wins by more still wins.

Run the tests: python3 tests/test_critique.py
The review of one fight: python3 critique.py <battle id prefix>   (or --entries FILE)
"""
import os
import re

import cd_plan

# In the planners only on TNR_CRITIQUE=1 (director 2026-11-16: review replays rather than veto live decisions; the
# coordinator's brief: planner changes ship when tune_real.py, run with TNR_CRITIQUE=1 against =0, says they help).
LIVE = os.environ.get("TNR_CRITIQUE", "0") == "1"

# ---------------------------------------------------------------- sizes (HP units, as the planners' scores)
OFF_CENTRE = 900.0       # moving off the centre of my live Subaku Palace ("increased their damage")
BUFF_INTO_CLEAR = 250.0  # each self-buff in a bundle of two or more, into his ready Clear with no clear prevention
BURST_UNPUMPED = 300.0   # a burst round with neither Limit Breaker nor Aetherion while one is ready and fits
NUKE_NO_SEAL = 400.0     # a nuke on his clock and neither Danse Macabre nor Chakra Resistance in the bundle
LATE_FILLER = 300.0      # each pill / stance late in the fight when a better ready action fits its AP
LAST_WASTED = 400.0      # each setup or buff prevent in a likely last round, when an attack or a seal fits its AP

LATE_SHARE = 0.4         # my HP at or under this share of my max is "the end of the fight"
LATE_TURNS = 2           # ... and so is HP that his hardest turn takes in this many turns (fight 2, R8: 2,142 of
                         # 5,050 by the log, 42%, with his turns taking 1,469 and 1,933: "at the end of the fight")
NUKE_SHARE = 0.35        # his hit at or over this share of my HP now is a nuke
CLEAR_CD = 10            # rounds between two Clears (cd_plan.ACTIONS["clear"]; the basic action is the same for all)

BUFFS = {"overflow", "eclipse", "thunders", "parry", "pill", "jewel", "limitbreaker", "offstance"}
DAMAGE = {"rebirth", "shrapnel", "lotus", "fury", "ember", "danse", "stormblade", "nights", "aetherion", "resonance",
          "leech", "yuki", "kunai"}
MOVES = {"phantom", "replace", "step", "stepback"}
SETUP = {"overflow", "thunders", "parry", "eclipse", "ember", "subaku", "limitbreaker", "pill", "jewel", "phantom"}
PUMPS = ("limitbreaker", "aetherion")
SHOW = {"panacea": "Panacea", "resist": "Chakra Resistance", "danse": "Danse Macabre", "shield": "Chakra Shield",
        "smoke": "Elite Smoke Bomb", "jewel": "Colored Jewel", "aetherion": "Aetherion", "limitbreaker": "Limit Breaker",
        "stormblade": "Stormblade", "nights": "Night's Testament", "kims": "Dr. Kim's",
        "ember": "Forgotten Ember Blade", "fury": "Forbidden Chakra Fury", "shrapnel": "Shrapnel Clone Barrage",
        "rebirth": "Rebirth", "subaku": "Subaku Palace", "phantom": "Phantom Step", "lotus": "Lotus Dance",
        "sealnull": "Seal Null", "overflow": "Chakra Overflow"}
PUMP_NAMES = {"limitbreaker": "Limit Breaker", "aetherion": "Aetherion"}
SEALS = ("danse", "resist")          # Danse Macabre's bloodline seal, Chakra Resistance's -taken and -potency
LATE_FILLERS = ("pill", "offstance", "defstance")
# Rule 6, a likely last round: what pays only in a round I will not reach. Lotus Dance's damage is real, but "any
# attack except lotus dance would have been acceptable": its buff prevent is the reason to pick it over the others.
LAST_WASTED_SET = ("lotus", "sealnull", "thunders", "parry", "eclipse", "overflow", "jewel")
WITH_DANSE = ("overflow", "eclipse", "thunders", "parry", "jewel")   # "or with a buff (chakra overflow perhaps)"
LAST_BETTER = ("ember", "fury", "shrapnel", "danse", "resist", "rebirth", "stormblade", "nights", "aetherion",
               "subaku", "shield", "phantom")
BETTER_LATE = ("panacea", "resist", "danse", "shield", "smoke", "jewel", "aetherion", "limitbreaker", "stormblade",
               "nights", "kims")


def _cost(name):
    return cd_plan.ACTIONS.get(name, (0,))[0]


def _dist(a, b):
    """Hex distance, column-offset coordinates (turn.dist's)."""
    def cube(c, r):
        z = r - (c - (c & 1)) // 2
        return c, -c - z, z
    a, b = cube(*a), cube(*b)
    return max(abs(a[i] - b[i]) for i in range(3))


GRID = (13, 9)           # the battle board (turn.GRID_W, turn.GRID_H)


def subaku_centres(ground, me_id, grid=GRID):
    """The centre of my Subaku Palace while its ground is live, as a set (empty when none is up). The ground list is
    the battle read's, which holds live ground only. Its footprint (AOE_SPIRAL_SHOOT) is every
    hex within 4 of the caster but the caster's own (targeting.ts:56-58; art/subaku_palace/TIMING.md), so the centre
    is the hole: a hex with no Palace ground whose neighbours on the board all have it. (Should a unit's hex also be
    left bare, that is a second hole: each is a centre, as far as the guard is concerned.)"""
    tiles = {(g["longitude"], g["latitude"]) for g in ground or []
             if g.get("type") == "decreasedamagegiven" and g.get("creatorId") == me_id
             and g.get("longitude") is not None and g.get("latitude") is not None}
    if not tiles:
        return set()
    board = [(x, y) for x in range(grid[0]) for y in range(grid[1])]
    return {h for h in board if h not in tiles and all(n in tiles for n in board if _dist(n, h) == 1)}


def his_last_clear(rows, en_id):
    """The round of his last Clear in this fight's log (rows: (round, userId, action, texts)), or None."""
    rounds = [r for r, u, a, _ in rows if u == en_id and a == "clear"]
    return max(rounds) if rounds else None


def observed_peak(rows, en_id, me_name):
    """His hardest turn on me in this fight: the most damage the log shows me taking in one of his turns."""
    per = {}
    for r, u, _, ts in rows:
        if u != en_id:
            continue
        for t in ts or []:
            for m in re.finditer(rf"{re.escape(me_name)} takes ([\d.]+) (?:damage|afterburn damage|wound damage)", t):
                per[r] = per.get(r, 0.0) + float(m.group(1))
    return max(per.values(), default=0.0)


def wound_ticks(rows, me_name):
    """{round: wound damage due on me at that round's start}, from the log's "<me> will take N wound damage for the
    next K rounds" (cast in round c: due in c+1 .. c+K)."""
    due = {}
    pat = re.compile(rf"{re.escape(me_name)} will take ([\d.]+) wound damage for the next (\d+) rounds")
    for r, _, _, ts in rows:
        for t in ts or []:
            for m in pat.finditer(t):
                for k in range(1, int(m.group(2)) + 1):
                    due[r + k] = due.get(r + k, 0.0) + float(m.group(1))
    return due


def context(*, R, en_acted, st, ap, my_hp, my_max, me_pos, ground, me_id, rows, en_id, clear_safe, nuke_hit,
            afk=False, tick=0.0):
    """What the guards read, once per turn.
    st: the planner's {"loadout", "used"} after bans; clear_safe: clear-immunity live on me for his next turn
    already (Dr. Kim's cast before); nuke_hit: the planner's estimate of his hardest next turn on me; tick: the wound
    and drain due on me from now to the start of the round after his next turn (no damage reduction cuts it)."""
    his_turn = R + 1 if en_acted else R            # his next turn: this round when I act first, else next round
    last = his_last_clear(rows, en_id)
    return {
        "en_acted": bool(en_acted),
        "ready": {n for n in st["loadout"] if n in cd_plan.ACTIONS and cd_plan.ready_round(st, n) <= R},
        "ap": ap, "my_hp": float(my_hp), "my_max": float(my_max or 5050),
        "on_subaku_centre": tuple(me_pos) in subaku_centres(ground, me_id),
        "his_clear_ready": not afk and (last is None or his_turn - last >= CLEAR_CD),
        "clear_safe": bool(clear_safe),
        "setup_live": any(r == R - 1 and n in SETUP for r, n in st["used"]),
        "nuke": float(nuke_hit or 0) > 0 and float(nuke_hit) >= NUKE_SHARE * max(float(my_hp), 1.0),
        "last_round": float(nuke_hit or 0) > 0 and float(my_hp) <= float(nuke_hit) + float(tick or 0),
        "tick": float(tick or 0), "nuke_hit": float(nuke_hit or 0),
        "late": float(my_hp) <= LATE_SHARE * float(my_max or 5050)
                or (float(nuke_hit or 0) > 0 and float(my_hp) <= LATE_TURNS * float(nuke_hit)),
    }


def live_guards(bundle, c):
    """guards() for the planners: nothing unless TNR_CRITIQUE=1."""
    return guards(bundle, c) if LIVE else (0.0, [])


def guards(bundle, c):
    """(penalty <= 0, [reasons]) for one bundle of mine against the critique."""
    if not c:
        return 0.0, []
    b = list(bundle)
    p, why = 0.0, []
    ready = c["ready"] - set(b)
    spare = c["ap"] - sum(_cost(x) for x in b)

    # 1. Subaku Palace: its centre is mine while it is up. Off it, he walks on and its -damage given is off him.
    moved = [x for x in b if x in MOVES]
    if c["on_subaku_centre"] and moved:
        p -= OFF_CENTRE
        why.append(f"{'+'.join(moved)} off the centre of my Subaku Palace, which he can take (-{OFF_CENTRE:.0f})")

    # 2. Buffs into his Clear: two or more with his Clear ready and no clear prevention over his turn. Dr. Kim's
    #    cast now covers his turn only when he moves after the round turns (he acted first this round).
    buffs = [x for x in b if x in BUFFS]
    safe = c["clear_safe"] or ("kims" in b and c["en_acted"])
    if len(buffs) >= 2 and c["his_clear_ready"] and not safe:
        cost = BUFF_INTO_CLEAR * len(buffs)
        p -= cost
        why.append(f"{len(buffs)} buffs ({'+'.join(buffs)}) into his ready Clear with no clear prevention (-{cost:.0f})")

    # 3. The burst round: the turn after a setup (a damage buff of mine cast last round, live now) that throws a
    #    big hit (a 60 AP damage jutsu, or two damage jutsu). Limit Breaker (+10 potency now, +30% given) or
    #    Aetherion (+20% taken) pumps it. With 100 AP and a 60 AP hit only one of the two fits, so the guard asks
    #    for one of them when one is ready and fits in place of what is not damage.
    dmg = [x for x in b if x in DAMAGE]
    if c.get("setup_live", True) and (any(_cost(x) >= 60 for x in dmg) or len(dmg) >= 2):
        room = spare + sum(_cost(x) for x in b if x not in DAMAGE and x not in MOVES and x != "cleanse")
        pumps = [x for x in PUMPS if x in ready and _cost(x) <= room]
        if pumps and not any(x in b for x in PUMPS):
            p -= BURST_UNPUMPED
            why.append(f"burst ({'+'.join(dmg)}) without {' or '.join(PUMP_NAMES[x] for x in pumps)}"
                       f" (-{BURST_UNPUMPED:.0f})")

    # 4. A nuke on his clock: Danse Macabre or Chakra Resistance, which stack with DR.
    if c["nuke"] and not any(x in b for x in SEALS) and any(x in ready for x in SEALS):
        cost = NUKE_NO_SEAL * (0.5 if any(x in b for x in ("smoke", "shield")) else 1.0)
        p -= cost
        why.append(f"his nuke is ready and neither Danse Macabre nor Chakra Resistance is used (-{cost:.0f})")

    # 5. The end of the fight: no pill and stance padding while a better ready action fits their AP.
    if c.get("late", c["my_hp"] <= LATE_SHARE * c["my_max"]):
        pads = [x for x in b if x in LATE_FILLERS]
        if pads:
            room = spare + sum(_cost(x) for x in pads)
            better = [x for x in BETTER_LATE if x in ready and _cost(x) <= room]
            if better:
                cost = LATE_FILLER * len(pads)
                p -= cost
                why.append(f"late {'+'.join(pads)} while {SHOW.get(better[0], better[0])} is ready (-{cost:.0f})")

    # 6. A likely last round (his next turn and my wound tick take what I have): setup and buff prevent pay only in a
    #    round I will not reach. One buff beside Danse Macabre is the exception ("paired ... with a buff to keep me
    #    alive long enough to go for the kill"). What fits instead: an attack that moves his HP pool, or a seal.
    if c.get("last_round"):
        wasted = [x for x in b if x in LAST_WASTED_SET]
        if "danse" in b:
            spare_buff = next((x for x in wasted if x in WITH_DANSE), None)
            wasted = [x for x in wasted if x != spare_buff]
        if wasted:
            room = spare + sum(_cost(x) for x in wasted)
            better = [x for x in LAST_BETTER if x in ready and _cost(x) <= room]
            if better:
                cost = LAST_WASTED * len(wasted)
                p -= cost
                names = ", ".join(SHOW.get(x, x) for x in better[:3])
                why.append(f"{'+'.join(wasted)} into a likely last round (his next turn {c.get('nuke_hit', 0):.0f}"
                           f" and my wound tick {c.get('tick', 0):.0f} against {c['my_hp']:.0f} HP): it pays only"
                           f" in a round I will not reach, while {names} fit (-{cost:.0f})")
    return p, why


# ================================================================ the replay review (director 2026-11-16)
# "I might be better to analyze replays as I just did to spot errors rather than trying to veto live decisions. In
# other words go over and analyze data then update the planner to account for new knowledge."
# review_fight() goes over a finished fight the way he went over fight 2: each turn I played, against the same five
# rules, with what the log shows (and the round's archived live state, when the brain kept one: positions, ground,
# HP). It looks back, so the nuke rule reads his ACTUAL next turn; the planner's guard has to forecast it. What it
# finds is for the director and for planner changes, which ship only when tune_real.py says they help.

BASIC = {"clear": "clear", "cleanse": "cleanse", "replacementTechnique": "replace", "defensiveStance": "defstance",
         "offensiveStance": "offstance", "move": "step", "basicHeal": "basicheal", "basicAttack": "basic"}
PALACE_ROUNDS = 3        # Subaku Palace's ground lasts 3 rounds, the round it is cast in counting (catalog)
TAKES = r"{me} takes ([\d.]+) (?:damage|afterburn damage|wound damage|reflect damage|recoil damage)"


def _name(a):
    import ingest
    return ingest.IDS.get(a) or BASIC.get(a)


def _turn_damage(rows, who, r, me_name):
    """What one side's turn in round r took off me, by the log."""
    pat = re.compile(TAKES.format(me=re.escape(me_name)))
    return sum(float(m.group(1)) for rr, u, _, ts in rows if rr == r and u == who
               for t in ts or [] for m in pat.finditer(t))


def _cols(d, prefix):
    """Columns ({prefix.*.field: [..]}) as a list of rows."""
    keys = [k for k in d if k.startswith(prefix + ".*.")]
    n = max((len(d[k]) for k in keys), default=0)
    return [{k[len(prefix) + 3:]: d[k][i] for k in keys if i < len(d[k])} for i in range(n)]


def archived_states(bid, fights=None):
    """{round: the archived live state at the start of my turn} from fights/live_states/<bid>.full.jsonl.gz (the
    brain keeps one per side per round, player/activities/battle.py _archive), or {} without one."""
    import gzip
    import json
    path = os.path.join(fights or os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fights"),
                        "live_states", f"{bid}.full.jsonl.gz")
    out = {}
    try:
        with gzip.open(path, "rt", encoding="utf8") as f:
            for line in f:
                rec = json.loads(line)
                if rec.get("turn") == "me":
                    out[int(rec["round"])] = rec
    except (OSError, ValueError):
        pass
    return out


def _from_state(rec, me_id):
    """(my position, my HP, my max HP, ground rows) from an archived state, any of them None when missing."""
    fighters = _cols(rec.get("fighters") or {}, "battle.usersState")
    me = next((f for f in fighters if f.get("userId") == me_id), {})
    ground = rec.get("ground")
    if isinstance(ground, dict):
        ground = _cols(ground, "battle.groundEffects") or _cols(ground, "groundEffects")
    pos = (me["longitude"], me["latitude"]) if me.get("longitude") is not None else None
    return pos, me.get("curHealth"), me.get("maxHealth"), ground if isinstance(ground, list) else None


LIMIT_BREAKER_FROM = "2026-11-16"  # Limit Breaker reached level 25 that day (jutsu_training.md) and joined PvP 1


def had_limit_breaker(rows, me_id, path=None):
    """Whether Limit Breaker counts as in my set for a logged fight: the log shows it, or the log was saved on or
    after LIMIT_BREAKER_FROM (older fights were fought without it, so its absence there is no error)."""
    import datetime as dt
    if any(u == me_id and _name(a) == "limitbreaker" for _, u, a, _ in rows):
        return True
    try:
        day = dt.datetime.fromtimestamp(os.path.getmtime(path), dt.timezone.utc).strftime("%Y-%m-%d")
    except (TypeError, OSError):
        return False
    return day >= LIMIT_BREAKER_FROM


def review_fight(rows, me_id, en_id, me_name="dauntless", my_max=5050, states=None, loadout="pvp1",
                 limit_breaker=True, tiles=None):
    """The errors in one fight, turn by turn: [{round, played, text}]. rows: the log, oldest first, as
    (round, userId, actionId, texts); states: archived_states() for the fight, if any; limit_breaker: whether it
    was in my set (had_limit_breaker); tiles: each row's tile ("F4", the "*.tile" column), oldest first, when the
    log kept them. With tiles, positions come from the log: mine at the start of each turn, the Palace's centre
    where I stood when I cast it, and where each move went."""
    states = states or {}
    track = track_positions(rows, tiles, me_id, en_id) if tiles and any(tiles) else None
    palaces = []                                   # (cast round, centre) of each of my Palaces, by the log's tiles
    if track:
        for i, (rr, u, a, _) in enumerate(rows):
            if u == me_id and _name(a) == "subaku" and track[i][0] is not None:
                palaces.append((rr, track[i][0]))
    kit = [n for n in cd_plan.LOADOUTS[loadout] if limit_breaker or n != "limitbreaker"]
    found = []
    rounds = sorted({r for r, u, _, _ in rows if u == me_id})
    hp = float(my_max)
    for r in rounds:
        mine = [(i, _name(a)) for i, (rr, u, a, _) in enumerate(rows) if rr == r and u == me_id]
        played = [n for _, n in mine if n]
        first = mine[0][0] if mine else 0
        en_acted = any(u == en_id for rr, u, _, _ in rows[:first] if rr == r)
        before = [row for row in rows[:first]]
        used = [[rr, _name(a)] for rr, u, a, _ in before if u == me_id and _name(a) not in (None, "step")]
        # my HP at the start of my turn: the archived state's, else my max less every hit the log shows before it
        pat = re.compile(TAKES.format(me=re.escape(me_name)))
        log_hp = my_max - sum(float(m.group(1)) for _, _, _, ts in before for t in ts or [] for m in pat.finditer(t))
        pos, s_hp, s_max, ground = _from_state(states[r], me_id) if r in states else (None, None, None, None)
        if track and pos is None:
            pos = track[first][0]
        if track and ground is None:
            live = [(c, ctr) for c, ctr in palaces if c < r <= c + PALACE_ROUNDS - 1]
            ground = [g for c, ctr in live for g in palace_ground(ctr, me_id, c)]
        hp = float(s_hp) if s_hp is not None else log_hp
        his_turn = r + 1 if en_acted else r
        nxt = _turn_damage(rows, en_id, his_turn, me_name)
        ticks = wound_ticks(before + [rows[i] for i, _ in mine], me_name)
        tick = sum(ticks.get(k, 0.0) for k in range(r + 1, his_turn + 2))
        kims = any("cannot be cleared" in t and me_name in t for rr, u, _, ts in before if rr == his_turn - 1
                   for t in ts or [])
        c = context(R=r, en_acted=en_acted, st={"loadout": kit, "used": used}, ap=100,
                    my_hp=hp, my_max=float(s_max or my_max), me_pos=pos or (-1, -1), ground=ground or [], me_id=me_id,
                    rows=before, en_id=en_id, clear_safe=kims, nuke_hit=nxt,
                    afk=all(_name(a) is None and a == "wait" for rr, u, a, _ in rows if u == en_id), tick=tick)
        _, why = guards(played, c)
        for w in why:
            w = re.sub(r" \(-\d+\)$", "", w).replace("his nuke is ready", f"his next turn took {nxt:.0f}")
            if track and "centre of my Subaku Palace" in w:
                w = _centre_story(w, rows, track, mine, pos, palaces, r, en_id)
            found.append({"round": r, "played": played, "text": w})
        # no positions: a move while my Palace is up is flagged, the centre left to a look at the replay
        if pos is None and not track and any(x in MOVES for x in played):
            cast = [rr for rr, u, a, _ in before + [rows[i] for i, _ in mine]
                    if u == me_id and _name(a) == "subaku" and rr <= r]
            if cast and r <= max(cast) + PALACE_ROUNDS - 1:
                found.append({"round": r, "played": played,
                              "text": f"{'+'.join(x for x in played if x in MOVES)} while my Subaku Palace was up "
                                      f"(cast R{max(cast)}): if I stood on its centre, that let him take it "
                                      f"(no positions kept for this round: check the replay)"})
    return found


# ---- positions from the log (director 2026-11-16: "every jutsu used states where it was used, the tile letter and
#      number: d4, etc"). Each log line's description ends "on <b>F4</b>": the tile the action was aimed at. The board
#      names its tiles letter = column (A is longitude 0), number = row + 1 (latitude 0 is row 1): hexgrid.ts
#      nameArenaTile, `${String.fromCharCode(65 + tile.col)}${tile.row + 1}`. The brain keeps that tile per line as
#      the "*.tile" column of fights/<bid>_entries.json (player/calls.py described, tile_of).
TILE_RE = re.compile(r"<b>\s*([A-Za-z])\s*(\d{1,2})\s*</b>")
SELF_AIMED = {"heavenbows", "smoke"}  # mine, aimed at my own tile, that are in no planner table's self list


def tile_of(description):
    """A log line's description -> its tile ("F4"), or None. The last tile named is the one the line was aimed at."""
    found = TILE_RE.findall(description or "")
    return f"{found[-1][0].upper()}{int(found[-1][1])}" if found else None


def tile_xy(tile):
    """"F4" -> (5, 3), the (longitude, latitude) the battle state uses; None for anything else."""
    m = re.fullmatch(r"\s*([A-Za-z])(\d{1,2})\s*", tile or "")
    if not m:
        return None
    x, y = ord(m.group(1).upper()) - 65, int(m.group(2)) - 1
    return (x, y) if 0 <= x < GRID[0] and 0 <= y < GRID[1] else None


def tile_name(xy):
    return f"{chr(65 + xy[0])}{xy[1] + 1}" if xy else "?"


def _aims_at_him(name):
    """Whether one of my actions is aimed at him (its tile is his) rather than at me (its tile is mine)."""
    import turn
    if name in MOVES or name in SELF_AIMED or name in turn.SELF_T:
        return False
    return name in DAMAGE or name in {"subaku", "clear", "resist", "danse", "shrapnel"} or name not in BUFFS


def track_positions(rows, tiles, me_id, en_id):
    """Where each of us stood, by the log's tiles: [(mine, his)] before each row, and one more after the last.
    rows oldest first; tiles the same length (None where a line has none). Mine are read from my own lines (a move
    or a self-aimed action is my tile, an attack is his); his from his (a line aimed at my tile is aimed at me,
    any other is his own tile: a buff, a move, a heal). Unknown is None."""
    me = him = None
    out = [(me, him)]
    for (r, u, a, _), t in zip(rows, tiles):
        xy = tile_xy(t)
        if xy is not None and u == me_id:
            name = _name(a) or a
            if name in MOVES or not _aims_at_him(name):
                me = xy
            elif xy != me:
                him = xy
        elif xy is not None and u == en_id:
            if xy != me:
                him = xy
        out.append((me, him))
    return out


def log_tiles(path):
    """A saved log's tiles, oldest first like opponents.load_logs' rows (the file keeps the connector's newest-first
    order); None when the log kept none (every log saved before 2026-11-16)."""
    import json
    try:
        d = json.load(open(path))
    except (OSError, ValueError, TypeError):
        return None
    t = d.get("*.tile") if isinstance(d, dict) else None
    return list(t)[::-1] if isinstance(t, list) and any(t) else None


def palace_ground(centre, me_id, cast):
    """My Subaku Palace's ground as the battle read shows it: every hex within 4 of its centre but the centre."""
    return [{"type": "decreasedamagegiven", "creatorId": me_id, "longitude": x, "latitude": y,
             "rounds": PALACE_ROUNDS, "createdRound": cast}
            for x in range(GRID[0]) for y in range(GRID[1]) if 0 < _dist((x, y), centre) <= 4]


def _centre_story(text, rows, track, mine, pos, palaces, r, en_id):
    """The centre finding told with the log's tiles: where I stepped to, and whether he then stood on the centre."""
    centre = pos
    cast = max((c for c, ctr in palaces if ctr == centre and c <= r), default=None)
    last = mine[-1][0]
    dest = next((track[i + 1][0] for i, n in mine if n in MOVES), None)
    took = [rr for i, (rr, u, _, _) in enumerate(rows) if i > last and u == en_id and track[i + 1][1] == centre
            and cast is not None and rr <= cast + PALACE_ROUNDS - 1]
    text = text.replace(", which he can take", "")
    text += f": {tile_name(centre)} to {tile_name(dest)}, {_dist(centre, dest)} from the centre" if dest else ""
    text += f" (cast R{cast})" if cast is not None else ""
    return text + (f", and he took the centre ({tile_name(centre)}) in R{took[0]}" if took else "")


def report_fight(found, title=""):
    print(f"replay review{': ' + title if title else ''}: {len(found)} error(s)")
    for f in found:
        print(f"  R{f['round']} {'+'.join(f['played'])}: {f['text']}")


def main():
    import argparse
    import json
    ap = argparse.ArgumentParser(description="the replay review of one logged fight")
    ap.add_argument("bid", nargs="?", help="battle id prefix (fights/<bid>_entries.json)")
    ap.add_argument("--entries", help="an entries JSON instead (columns as the connector returns them)")
    ap.add_argument("--me-id", default=None)
    a = ap.parse_args()
    from ingest import ME
    me_id = a.me_id or ME
    if a.entries:
        raw = json.load(open(a.entries))
        rows = list(zip(raw["*.battleRound"], raw["*.userId"], raw["*.actionId"], raw["*.appliedEffects.*.txt"]))
        tiles = raw.get("*.tile") or [None] * len(rows)
        if len(rows) > 1 and rows[0][0] > rows[-1][0]:
            rows, tiles = rows[::-1], tiles[::-1]
        bid, path = os.path.basename(a.entries).split("_entries")[0], a.entries
    else:
        import opponents as OM
        log = next(((b, rr, p) for b, p, rr, m in OM.load_logs() if b.startswith(a.bid or "")), None)
        if not log:
            raise SystemExit(f"no log for {a.bid}")
        bid, rows, path = log
        tiles = log_tiles(path)
    en_id = next(u for u in dict.fromkeys(u for _, u, _, _ in rows) if u != me_id and (u or "").startswith("user_"))
    report_fight(review_fight(rows, me_id, en_id, states=archived_states(bid),
                              limit_breaker=had_limit_breaker(rows, me_id, path), tiles=tiles), bid[:8])


if __name__ == "__main__":
    main()
