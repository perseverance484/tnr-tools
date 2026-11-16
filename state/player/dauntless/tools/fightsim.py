#!/usr/bin/env python3
"""Full-fight simulator (director 2026-11-11: "simming replays and scenarios to understand damage windows, turn order,
cadence and battle flow/rhythm as well as counters").

Plays whole battles on planner2's numeric engine: rounds, turn order (I act first or second every round), cooldowns
and shared locks for both sides, stuns, ground, copy. My side is planner2 (the live decision code); his side is a bot
built from a real kit (saved opponents) or a style kit, choosing from his ready lines by his own score, sampled
(softmax) so repeated fights explore his choices. Offline only, no game calls; run under `nice`.

Usage:
  fightsim.py matrix [--n 4] [--opps all|name,...]   win rate / HP / length for each opponent x turn order
  fightsim.py fight OPP [--second] [--seed 1] [-v]   one fight, turn by turn
"""
import argparse
import copy
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cd_plan  # noqa: E402
import clock  # noqa: E402
import engine_bridge as EB  # noqa: E402
import opp_profile  # noqa: E402
import planner2 as P2  # noqa: E402
import shotplan  # noqa: E402
import turn  # noqa: E402
import value_model  # noqa: E402

ME_ID, EN_ID = turn.ME, "sim_enemy"
MAX_ROUNDS = 14
LOADOUT = "pvp1"


# ------------------------------------------------------------------ opponents
def style_kits():
    """Style opponents from catalog jutsu, picked by what they do (each also has the basics: Clear, Cleanse...)."""
    recs = EB._records()

    def pick(pred, n):
        out = []
        for j, v in recs.items():
            r = v.get("record", {})
            if r.get("hidden") or not r.get("effects") or r.get("itemType") or r.get("battleUsageType") == "PVE":
                continue
            if pred({e.get("type") for e in r["effects"]}, r) and r.get("actionCostPerc") in (40, 60):
                out.append(j)
        out.sort()
        return out[:n]
    dmg = lambda t, r: "damage" in t and r.get("actionCostPerc") == 60 and len(t) <= 3
    return {
        "style:burst": pick(lambda t, r: "increasedamagegiven" in t and "damage" not in t, 3) + pick(dmg, 5),
        "style:debuffer": pick(lambda t, r: "increasedamagetaken" in t and "damage" not in t, 3) + pick(dmg, 4)
                          + pick(lambda t, r: "increasedamagegiven" in t and "damage" not in t, 1),
        "style:copier": [j for j, v in recs.items() if v.get("record", {}).get("name") == "Shadow Dance"][:1]
                        + pick(lambda t, r: "decreasedamagegiven" in t, 2) + pick(dmg, 5),
        "style:tank": pick(lambda t, r: ("absorb" in t or "lifesteal" in t) and "damage" not in t, 3) + pick(dmg, 4)
                      + pick(lambda t, r: "decreasedamagetaken" in t and "damage" not in t, 2),
        "style:pierce": pick(lambda t, r: "pierce" in t, 3) + pick(dmg, 4)
                        + pick(lambda t, r: "increasedamagegiven" in t and "damage" not in t, 1),
    }


def opponents(styles=True, logs=True, saved=True):
    """name -> (acts, profile[, habit]). Log-modelled players (opponents.py: kit + habits from every logged fight),
    saved real kits, then styles."""
    out = {}
    if logs:
        import opponents as OM
        for uid, m in OM.load().items():
            if len(m.get("bundles", [])) < 3:
                continue
            name = "log:" + (m["names"][0] if m.get("names") else uid)
            prof = opp_profile.profile(uid, [(0, uid, a, None) for a in m["ids"]])
            out[name] = (OM.acts_for(m), prof, OM.habit_fn(m))
    if not saved:
        return out
    d = os.path.join(EB.HARNESS, "kit", "opponents")
    for f in sorted(os.listdir(d)):
        k = json.load(open(os.path.join(d, f)))
        if not k.get("jutsu"):
            continue
        uid = f[:-5]
        out[k.get("name") or uid] = (clock.acts_from_ids(k["jutsu"], k.get("jutsuLevels")), opp_profile.profile(uid))
    for name, ids in (style_kits().items() if styles else ()):
        out[name] = (clock.acts_from_ids(ids), {"source": "style", "elements": ["None"], "given": (0.40, ["None"]),
                                                "dr": (0.0, [])})
    return out


# ------------------------------------------------------------------ one fight
class Fight:
    def __init__(self, acts, prof, me_first, seed=0, temp=200.0, policy=None, habit=None):
        self.rng = random.Random(seed)
        self.acts, self.prof, self.me_first, self.temp = acts, prof, me_first, temp
        self.cal = value_model.load_cal()
        value_model.calibrate_kit(self.cal)
        cd_plan.ACTIONS.setdefault("basicheal", (60, 5, None, "heal 600 instant"))
        shotplan.MINE.setdefault("basicheal", (0, [("me", "heal", 600, 0, True)]))
        self.my_kit = P2.make_my_kit(prof)
        self.mine_prof = opp_profile.own_profile()
        self.gmul = opp_profile.given_mult(prof)
        self.scale = self.gmul / max(1.0, opp_profile.given_mult(self.mine_prof))
        gk = value_model.generic_kit(self.cal)
        self.base_turn = gk["turn"][0] * self.gmul
        self.his_kit = {k: P2.compile_spec(v, False) for k, v in gk.items()}
        for aid, (nm, cost, cd, locks, spec) in acts.items():
            # his raw kit sits on my calibration (my bloodline boost inside); rescale to his
            self.his_kit[aid] = P2.compile_spec((spec[0] * self.scale,) + tuple(spec[1:]), False)
        self.me = P2.Side(5050.0).passives(**self.mine_prof.get("passives", {}))
        self.en = P2.Side(5050.0).passives(**prof.get("passives", {}))
        self.rows = []          # (round, user, action id, None): both sides' history, oldest first
        self.used = []          # [round, my short name] for cd_plan
        self.R = 1
        self.log = []
        self.policy = policy or self.planner_move
        self.habit, self.his_prev, self.his_turns = habit, None, 0
        self.on_my_turn = None
        self.use_book = False
        self.loadout = list(cd_plan.LOADOUTS[LOADOUT]) + ["basicheal"]

    # ---- my side: planner2's own decision
    def ctx(self):
        his_used = {a for r, u, a, _ in self.rows if u == EN_ID}
        pierce_ids = {a for a, v in self.acts.items() if v[4][2:3] == ("pierce",)}
        last_p = max([r for r, u, a, _ in self.rows if u == EN_ID and a in pierce_ids] or [-9])
        copier = any(t[1] == "copy" for v in self.acts.values() for t in v[4][1])
        return {"pierce_ready": bool(pierce_ids) and self.R - last_p >= 3, "pierce_shown": bool(pierce_ids),
                "copier": copier,
                "clear_held": "clear" not in his_used, "smoke_spent": True, "afk": False, "summon": False,
                "pierce_window": self.me.given(0) < 0.6 or bool(self.en.g(P2.SHD, 0))
                or 1 - 35 / 50 * self.en.g(P2.DR, 0) >= 0.55 or self.en.hp <= 720}

    def planner(self, ap):
        en_acted = not self.me_first
        ctx = self.ctx()
        clockd, _ = P2.make_clock(self.acts, self.rows, EN_ID, self.R, en_acted, self.me, self.en, ctx, self.cal,
                                  self.his_kit, self.base_turn, self.scale)
        st = {"loadout": self.loadout, "used": self.used}
        P = P2.Planner(self.me.copy(), self.en.copy(), self.R, ctx, self.cal, self.my_kit, self.his_kit, st,
                       en_acted, (5050, 5050), self.base_turn, clockd)
        if self.use_book:
            import solutions
            P.book_key = solutions.situation_key(P, ctx, st, self.R, self.his_prev, self.acts)
            P.book_path = solutions.LIB
        return P, st

    def planner_move(self, ap):
        P, st = self.planner(ap)
        bundles = P2.legal_bundles(st, self.R, ap, 1, self.loadout, P.me0, P.en0)
        if not bundles:
            return ()
        res = P2.rank(P, bundles, ap, P2.load_weights())
        if P2.LOOKAHEAD:
            res = P2.lookahead_rerank(P, {"st": st, "R": self.R}, res, P2.LA_BUDGET)
        return res[0][1]

    def snapshot(self):
        f = copy.copy(self)
        f.me, f.en = self.me.copy(), self.en.copy()
        f.rows, f.used, f.log = list(self.rows), [list(x) for x in self.used], list(self.log)
        f.rng = random.Random(self.rng.random())
        f.on_my_turn = None
        return f

    def resume_from_my_turn(self):
        """Continue a snapshot taken at the start of my turn: my turn, the rest of this round, then the fight."""
        self.my_turn()
        if self.me.hp <= 0 or self.en.hp <= 0:
            return self.result()
        if self.me_first:
            self.his_turn()
            if self.me.hp <= 0 or self.en.hp <= 0:
                return self.result()
        self.me.shift(); self.en.shift()
        self.R += 1
        return self.run()

    def my_turn(self):
        if self.on_my_turn:
            self.on_my_turn(self)
        ap = 100 - (20 if self.me.g(P2.STUN, 0) else 0)
        b = tuple(self.policy(ap))
        if "cleanse" in b:
            self.me.wipe(P2.NEGK)
        if any(x in ("phantom", "replace", "step") for x in b):
            self.me.wipe((P2.GGRD,))
        d, t = P2.run_turn(self.me, self.en, [self.my_kit[x] for x in b if x in self.my_kit], 0, 5050, 5050)
        for x in b:
            if x not in ("step", "stepback"):
                self.used.append([self.R, x])
            self.rows.append((self.R, ME_ID, turn.ACTION_ID.get(x, x), None))
        self.log.append((self.R, "me", b, d, t, self.me.hp, self.en.hp))

    # ---- his side: his ready lines scored from his side, sampled
    def his_turn(self):
        ap = 100 - (20 if self.en.g(P2.STUN, 0) else 0)
        ready = clock.ready_at(self.acts, EN_ID, self.rows, self.R)
        lines = clock.bundles(self.acts, ready, ap)
        if not lines:
            return
        ctx = self.ctx()
        P = P2.Planner(self.me, self.en, self.R, ctx, self.cal, {}, self.his_kit, {"loadout": [], "used": []},
                       False, (5050, 5050), self.base_turn, {})
        P.hr = 0
        sc = [(P.his_score(hb, self.me, self.en)
               + (self.habit(hb, self.R, self.his_prev, self.his_turns == 0) if self.habit else 0.0), hb) for hb in lines]
        opts = clock.soft(sc, k=5, temp=self.temp)
        x, acc = self.rng.random(), 0.0
        hb = opts[-1][1]
        for w, b in opts:
            acc += w
            if x <= acc:
                hb = b
                break
        self.his_prev, self.his_turns = hb, self.his_turns + 1
        if "cleanse" in hb:
            self.en.wipe(P2.NEGK)
        d, t = P2.run_turn(self.en, self.me, [self.his_kit[a] for a in hb], 0, 5050, 5050)
        for a in hb:
            self.rows.append((self.R, EN_ID, a, None))
        self.log.append((self.R, "him", tuple(self.acts[a][0] for a in hb), d, t, self.me.hp, self.en.hp))

    def run(self):
        while self.R <= MAX_ROUNDS:
            for side in ((self.my_turn, self.his_turn) if self.me_first else (self.his_turn, self.my_turn)):
                side()
                if self.me.hp <= 0 or self.en.hp <= 0:
                    return self.result()
            self.me.shift(); self.en.shift()
            self.R += 1
        return self.result()

    def result(self):
        win = self.en.hp <= 0 < self.me.hp or (self.me.hp > 0 and self.en.hp > 0 and self.me.hp > self.en.hp)
        return {"win": win, "ko": self.en.hp <= 0 or self.me.hp <= 0, "rounds": self.R,
                "me": max(0, self.me.hp), "him": max(0, self.en.hp)}


def matrix(opps, n, book=False):
    out = {}
    for name, spec in opps.items():
        acts, prof, habit = (tuple(spec) + (None,))[:3]
        for first in (True, False):
            res = []
            for sd in range(n):
                f = Fight(acts, prof, first, seed=sd, habit=habit)
                f.use_book = book
                res.append(f.run())
            w = sum(r["win"] for r in res) / n
            out[(name, first)] = res
            print(f"{name[:18]:18} {'P1' if first else 'P2'}  win {w:4.0%}  rounds {sum(r['rounds'] for r in res) / n:4.1f}"
                  f"  my HP {sum(r['me'] for r in res) / n:5.0f}  his HP {sum(r['him'] for r in res) / n:5.0f}", flush=True)
    tot = [r for v in out.values() for r in v]
    print(f"\nALL: win {sum(r['win'] for r in tot) / len(tot):.0%} over {len(tot)} fights")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["matrix", "fight"])
    ap.add_argument("opp", nargs="?")
    ap.add_argument("--n", type=int, default=4)
    ap.add_argument("--opps", default="all")
    ap.add_argument("--second", action="store_true")
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("-v", action="store_true")
    ap.add_argument("--book", action="store_true", help="planner2 with the solution library (solutions.json)")
    ap.add_argument("--set", default="all", choices=["all", "logs", "styles"])
    a = ap.parse_args()
    opps = opponents(styles=a.set != "logs", logs=a.set != "styles", saved=a.set == "all")
    if a.cmd == "matrix":
        if a.opps != "all":
            opps = {k: v for k, v in opps.items() if any(x.lower() in k.lower() for x in a.opps.split(","))}
        matrix(opps, a.n, a.book)
        return
    name = next(k for k in opps if a.opp.lower() in k.lower())
    spec = tuple(opps[name]) + (None,)
    f = Fight(spec[0], spec[1], me_first=not a.second, seed=a.seed, habit=spec[2])
    res = f.run()
    for r, who, b, d, t, mh, eh in f.log:
        print(f"R{r} {who:3} {'+'.join(b):60.60} dealt {d:5.0f} self {t:+5.0f} -> me {mh:5.0f} / him {eh:5.0f}")
    print(res)


if __name__ == "__main__":
    main()
