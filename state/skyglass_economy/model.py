#!/usr/bin/env python3
"""Skyglass event economy model: expected yields per activity and Monte Carlo time-to-goal per player type.

    python3 state/skyglass_economy/model.py                 # baseline + recommended, all CSVs in out/
    python3 state/skyglass_economy/model.py --quick         # fewer players (smoke test)
    python3 state/skyglass_economy/model.py --no-impacts    # skip the per-change isolated runs

Inputs: state/skyglass_economy/inputs.json (every rate with its source); scenario overrides:
state/skyglass_economy/recommended.json. Stdlib only, deterministic for a fixed seed. Zero live requests.

Model
- Time is continuous play hours; weekend = hours / hours_per_weekend of the player type. Inventory carries over between
  weekends (the event repeats every weekend). Nothing in the event is capped per day or per weekend.
- Each step the player takes the first available action of `policy.priority`: craft a shard from Salvage, assemble an
  Invitation (4 distinct shards, self-service), attempt the uber, run the best chart held (Lantern, tainted, steep or
  run an Epic chart, Haul page, Rare charts, Common charts), else farm the Wreck (party of three; drops per member).
- A run's ending drops and pick pay only on a clear; a failed run costs `fail_time_frac` of its minutes (the Wreck: its
  one-hour clock). Press-on rooms are free upside (a loss keeps the ending), so the player always presses on.
- With trade: duplicate shards swap 1:1 for a missing shard, and a share of loot value buys missing shards at a price
  (auto = the scenario's own fair price; see inputs.trade).
"""
import argparse
import copy
import csv
import json
import math
import os
import random
import statistics
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
SHARDS = ["shard_keel", "shard_crown", "shard_tide", "shard_ledger"]
CHART_ITEMS = ["chart_tide", "chart_roster", "chart_buried", "chart_foundry", "chart_archive", "chart_watch",
               "chart_reliquary", "chart_last_heading", "chart_rotted_reliquary", "chart_rotted_heading", "lantern",
               "haul_page"]
ENTRY_TO_ACT = {"chart_tide": "chart_tide", "chart_roster": "chart_roster", "chart_buried": "hunt_buried",
                "chart_foundry": "hunt_foundry", "chart_archive": "hunt_archive", "chart_watch": "hunt_watch",
                "chart_reliquary": "epic_reliquary", "chart_last_heading": "epic_fall",
                "chart_rotted_reliquary": "tainted_rotted", "chart_rotted_heading": "tainted_burning",
                "lantern": "crownhold", "haul_page": "haul", "invitation": "uber"}
FLOW_ITEMS = ["salvage", "core_rot", "skyglass_token", "invitation", "remnant", "galley_stores", "coffer", "treasury",
              "archive_chart_case", "unmarked_cargo"] + SHARDS + CHART_ITEMS


def V(x):
    return x["v"] if isinstance(x, dict) and "v" in x else x


def set_path(d, path, value):
    """Set a dotted path. A list element is addressed by `[item=<name>]` (drop lists) or by an integer."""
    parts = path.split(".")
    cur = d
    for i, p in enumerate(parts):
        last = i == len(parts) - 1
        if p.startswith("[item="):
            name = p[6:-1]
            hits = [x for x in cur if x.get("item") == name]
            if not hits:
                raise KeyError(f"{path}: no drop line for {name}")
            if last:
                raise KeyError(path)
            cur = hits[0]
            continue
        if isinstance(cur, list):
            p = int(p)
        if last:
            if isinstance(cur, dict) and isinstance(cur.get(p), dict) and "v" in cur[p] and not isinstance(value, dict):
                cur[p]["v"] = value
            else:
                cur[p] = value
        else:
            cur = cur[p]


def apply_changes(I, changes):
    I = copy.deepcopy(I)
    for ch in changes:
        for path, value in ch["set"].items():
            if path.endswith(".+append"):
                tgt = I
                for p in path[:-len(".+append")].split("."):
                    tgt = tgt[p]
                tgt.append(value)
            else:
                set_path(I, path, value)
    return I


# ---------------------------------------------------------------------------------------------------------------
# Expected values (analytic)
# ---------------------------------------------------------------------------------------------------------------
def table_ev(I, name):
    t = I["tables"][name]
    out = defaultdict(float)
    if "fixed" in t:
        for k, q in t["fixed"].items():
            out[k] += q
        return out
    tot = sum(w for w, _ in t["tiers"])
    for w, entries in t["tiers"]:
        for e in entries:
            for k, q in e.items():
                out[k] += q * (w / tot) / len(entries)
    return out


def expand(I, items, depth=0):
    """Open containers that are opened on receipt (Unmarked Cargo, Archive Chart Case, Crown's Hoard)."""
    out = defaultdict(float)
    for k, q in items.items():
        if k in I["tables"] and I["tables"][k].get("open_on_receipt") and depth < 4:
            for k2, q2 in expand(I, table_ev(I, k), depth + 1).items():
                out[k2] += q * q2
        else:
            out[k] += q
    return out


def drops_ev(drops):
    out = defaultdict(float)
    for d in drops:
        out[d["item"]] += V(d["p"]) * d.get("qty", 1) * d.get("lines", 1)
    return out


def pick_options(I, act):
    pk = act.get("picks")
    if not pk:
        return None, 0
    opts = I["activities"][pk["same_as"]]["picks"]["options"] if "same_as" in pk else pk["options"]
    return opts, pk["count"]


def choose_picks(I, key, opts, n, taken_once):
    pref = I["policy"]["picks"].get(key) or I["policy"]["picks"].get(I["activities"][key]["picks"].get("same_as", ""), [])
    by = {o["label"]: o for o in opts}
    order = [by[l] for l in pref if l in by] + [o for o in opts if o["label"] not in pref]
    chosen = []
    for o in order:
        if o.get("once") and (key, o["label"]) in taken_once:
            continue
        chosen.append(o)
        if len(chosen) == n:
            break
    return chosen


def activity_ev(I, key, ptype=None, haul_route=None):
    """Expected items per run and expected minutes per run (steady state: once-only picks/drops counted as drops)."""
    G = I["global"]
    a = I["activities"][key]
    oh = V(G["overhead_min_per_run"])
    ff = V(G["fail_time_frac"])
    items = defaultdict(float)
    if a["kind"] == "haul":
        route_mode = haul_route or "value"
        pages = a["pages"]
        mins = 0.0
        for page, pg in pages.items():
            r = pick_route(pg, route_mode)
            mins += (r["minutes"] + oh) / len(pages)
            for c in r["chests"]:
                items[f"{pg['profession']}_{c}"] += r["clear"] / len(pages)
                if c == "L" and V(a["reserve_shard_mode"]) == "per_reserve_chest":
                    items["shard_ledger"] += r["clear"] * V(a["reserve_shard"]["p"]) / len(pages)
            if V(a["reserve_shard_mode"]) == "per_clear":
                items["shard_ledger"] += r["clear"] * V(a["reserve_shard"]["p"]) / len(pages)
        items["haul_page"] -= 1
        return items, mins
    if a["kind"] == "steep":
        w = V(a["win"])
        items["core_rot"] -= V(a["rot_cost"])
        items["chart_epic (consumed on a win)"] -= w
        items["chart_tainted"] += w
        return items, V(a["minutes"]) + oh
    if a["kind"] == "uber":
        c = V(I["player_types"][ptype]["uber_clear"])
        for k, q in drops_ev(a["on_clear"]).items():
            items[k] += c * q
        opts, n = pick_options(I, a)
        for o in choose_picks(I, key, opts, n, set()):
            for k, q in expand(I, o["items"]).items():
                items[k] += c * q
        items["invitation"] -= 1
        m = V(a["minutes"]) * (c + (1 - c) * V(a["fail_time_frac"])) + oh
        return items, m
    c = V(a["clear"])
    base = drops_ev(a.get("drops", []))
    press = a.get("press_on")
    pw = V(press["win"]) if (press and V(I["policy"]["press_on"])) else 0.0
    if press and pw:
        alt = drops_ev(press["win_drops"])
        for k in set(base) | set(alt):
            items[k] += c * ((1 - pw) * base.get(k, 0) + pw * alt.get(k, 0))
    else:
        for k, q in base.items():
            items[k] += c * q
    items = expand(I, items)
    opts, n = pick_options(I, a)
    if opts:
        for o in choose_picks(I, key, opts, n, set()):
            for k, q in expand(I, o["items"]).items():
                items[k] += c * q
    if a.get("ryo"):
        items["ryo"] += c * V(a["ryo"])
    if a.get("exp"):
        items["exp"] += c * V(a["exp"])
    if a.get("entry"):
        items[a["entry"]] -= 1
    if a["kind"] == "farm":
        fm = V(a.get("fail_minutes", {"v": V(a["minutes"])}))
        m = c * V(a["minutes"]) + (1 - c) * fm + (V(G["wreck_party_overhead_min"]) if a.get("party_overhead") else oh)
    else:
        m = V(a["minutes"]) * (c + (1 - c) * ff) + oh
        if press and pw:
            m += c * V(press["extra_minutes"])
    return items, m


def pick_route(pg, mode):
    rs = pg["routes"]
    if mode == "reserve":
        return max(rs, key=lambda r: (r["clear"] * r["chests"].count("L"), r["evM"]))
    return max(rs, key=lambda r: r["evM"])


def item_value(I, k):
    vals = I["values_ryo"]
    if k == "ryo":
        return 1.0
    return V(vals[k]) if k in vals and not k.startswith("_") else 0.0


# ---------------------------------------------------------------------------------------------------------------
# Monte Carlo player
# ---------------------------------------------------------------------------------------------------------------
class Player:
    def __init__(self, I, ptype, trade, rng, shard_price=None, track_flows=False):
        self.I, self.ptype, self.trade, self.rng = I, ptype, trade, rng
        self.A = I["activities"]
        self.P = I["policy"]
        self.pt = I["player_types"][ptype]
        self.H = V(self.pt["hours_per_weekend"])
        self.inv = defaultdict(float)
        self.t = 0.0  # play hours
        self.once_got = set()
        self.taken_once = set()
        self.goals = {}
        self.tokens_received = 0
        self.uber_clears = 0
        self.keys_made = 0
        self.ryo_budget = 0.0
        self.shard_price = shard_price
        self.track = track_flows
        self.flow = defaultdict(float)
        self.value_ryo = 0.0
        self.shards_made = 0
        self.oh = V(I["global"]["overhead_min_per_run"])
        self.ff = V(I["global"]["fail_time_frac"])
        self.boss = V(I["goals"]["boss_variants"])
        self.skins = V(I["goals"]["skin_tokens"])
        self.remainder_cost = V(I["proposed"]["remnant_recipes"]["remainder"])
        self.shard_cost = V(I["proposed"]["salvage_exchanges"]["shard_any"])
        self.shard_order = V(self.P["salvage_shard_order"])
        self.haul_mode = V(self.pt["haul_route"])
        self.steep_on = V(self.P["steep"])
        self.press_on = V(self.P["press_on"])
        self.break_seal = V(self.P["break_seal"])
        self.pyr_share = V(self.P["solo_pyramid_share"])
        self.farm = V(self.P["farm_activity"])
        self.uber_clear = V(self.pt["uber_clear"])
        self.cprob = {k: V(a["clear"]) for k, a in self.A.items() if "clear" in a}
        self.route = {p: pick_route(pg, self.haul_mode) for p, pg in self.A["haul"]["pages"].items()}
        self.pages = list(self.A["haul"]["pages"].keys())

    # --- inventory -------------------------------------------------------------------------------------------
    def give(self, k, q, src):
        if q == 0:
            return
        T = self.I["tables"]
        if k in T and T[k].get("open_on_receipt"):
            if self.track:
                self.flow[(k, "in", src)] += q
                self.flow[(k, "out", "opened")] += q
            for _ in range(int(round(q))):
                self.open_table(k, src)
            return
        self.inv[k] += q
        if self.track:
            self.flow[(k, "in", src)] += q
        v = item_value(self.I, k)
        if v:
            self.value_ryo += v * q
            if self.trade:
                self.ryo_budget += v * q * V(self.I["trade"]["ryo_budget_fraction"])
        if k == "skyglass_token":
            self.tokens_received += q
        if k in SHARDS:
            self.shards_made += q

    def take(self, k, q, sink):
        self.inv[k] -= q
        if self.track:
            self.flow[(k, "out", sink)] += q

    def open_table(self, name, src):
        t = self.I["tables"][name]
        via = f"{src} > {name}"
        if "fixed" in t:
            for k, q in t["fixed"].items():
                self.give(k, q, via)
            return
        r = self.rng.random() * sum(w for w, _ in t["tiers"])
        for w, entries in t["tiers"]:
            if r < w:
                e = entries[int(self.rng.random() * len(entries))]
                for k, q in e.items():
                    self.give(k, q, via)
                return
            r -= w

    def roll(self, drops, src):
        rnd = self.rng.random
        for d in drops:
            p = V(d["p"])
            for _ in range(d.get("lines", 1)):
                if p >= 1 or rnd() < p:
                    if d.get("once"):
                        if d["item"] in self.once_got:
                            continue
                        self.once_got.add(d["item"])
                    self.give(d["item"], d.get("qty", 1), src)

    def do_picks(self, key):
        a = self.A[key]
        opts, n = pick_options(self.I, a)
        if not opts:
            return
        for o in choose_picks(self.I, key, opts, n, self.taken_once):
            if o.get("once"):
                self.taken_once.add((key, o["label"]))
            for k, q in o["items"].items():
                self.give(k, q, f"{key} pick")

    # --- actions ---------------------------------------------------------------------------------------------
    def run(self, key):
        a = self.A[key]
        rnd = self.rng.random
        if a.get("entry"):
            self.take(a["entry"], 1, key)
        kind = a["kind"]
        if kind == "farm":
            c = self.cprob[key]
            ok = rnd() < c
            m = (V(a["minutes"]) if ok else V(a["fail_minutes"])) + V(self.I["global"]["wreck_party_overhead_min"])
            if ok:
                self.roll(a["drops"], key)
                self.give("ryo", V(a["ryo"]), key)
            return m
        if kind == "haul":
            page = self.pages[int(rnd() * len(self.pages))]
            r = self.route[page]
            prof = self.A["haul"]["pages"][page]["profession"]
            m = r["minutes"] + self.oh
            if rnd() < r["clear"]:
                rs = self.A["haul"]["reserve_shard"]
                mode = V(self.A["haul"]["reserve_shard_mode"])
                for ch in r["chests"]:
                    self.give(f"{prof}_{ch}", 1, "haul")
                    if ch == "L" and mode == "per_reserve_chest" and rnd() < V(rs["p"]):
                        self.give("shard_ledger", 1, "haul reserve chest")
                if mode == "per_clear" and rnd() < V(rs["p"]):
                    self.give("shard_ledger", 1, "haul clear")
            self.goals.setdefault("first_haul", self.t + m / 60)
            return m
        if kind == "uber":
            m = V(a["minutes"])
            if rnd() < self.uber_clear:
                self.uber_clears += 1
                self.roll(a["on_clear"], "uber")
                self.do_picks("uber")
                if "heartglass" not in self.goals:
                    self.goals["heartglass"] = self.t + m / 60
                self.craft_remnants(m)
                return m + self.oh
            return m * V(a["fail_time_frac"]) + self.oh
        # chart runs
        c = self.cprob[key]
        extra_m = 0.0
        if key == "hunt_archive" and self.break_seal:
            bs = a["break_seal"]
            c *= V(bs["clear_mult"])
            extra_m = V(bs["extra_minutes"])
        m = V(a["minutes"]) + self.oh + extra_m
        if key == "crownhold":
            self.goals.setdefault("first_crownhold", self.t + m / 60)
        self.goals.setdefault("first_chart_run", self.t + m / 60)
        if rnd() < c:
            press = a.get("press_on")
            drops = a["drops"]
            if press and self.press_on:
                m += V(press["extra_minutes"])
                if rnd() < V(press["win"]):
                    drops = press["win_drops"]
            self.roll(drops, key)
            if key == "hunt_archive" and self.break_seal:
                self.give("core_rot", V(a["break_seal"]["core_rot"]), "archive break the seal")
            self.do_picks(key)
            if a.get("ryo"):
                self.give("ryo", V(a["ryo"]), key)
        else:
            m = V(a["minutes"]) * self.ff + self.oh + extra_m
        return m

    def steep(self, chart):
        a = self.A["steep"]
        cost = V(a["rot_cost"])
        self.take("core_rot", cost, "steeping")
        if self.rng.random() < V(a["win"]):
            self.take(chart, 1, "steeping (won)")
            self.give(a["map"][chart], 1, "steeping")
        return V(a["minutes"]) + self.oh

    def craft_remnants(self, m):
        R = self.I["proposed"]["remnant_recipes"]
        if "remainder" not in self.goals and self.inv["remnant"] >= self.remainder_cost:
            self.take("remnant", self.remainder_cost, "The Remainder")
            self.goals["remainder"] = self.t + m / 60
        elif V(R["heartglass_second_enabled"]) and self.inv["remnant"] >= V(R["heartglass_second"]):
            self.take("remnant", V(R["heartglass_second"]), "second Heartglass")
            self.inv["heartglass_second"] += 1

    def missing_shards(self):
        return [s for s in SHARDS if self.inv[s] < 1]

    def try_trade(self):
        if not self.trade:
            return False
        miss = self.missing_shards()
        if not miss:
            return False
        dup = [s for s in SHARDS if self.inv[s] >= 2]
        ratio = V(self.I["trade"]["shard_swap_ratio"])
        if dup and self.inv[dup[0]] - 1 >= ratio:
            self.take(dup[0], ratio, "sold (trade)")
            self.give(miss[0], 1, "bought with a shard (trade)")
            return True
        if self.shard_price and self.ryo_budget >= self.shard_price:
            self.ryo_budget -= self.shard_price
            self.give(miss[0], 1, "bought with ryo (trade)")
            if self.track:
                self.flow[("ryo_spent_on_shards", "out", "trade")] += self.shard_price
            return True
        return False

    def step(self):
        """One action. Returns minutes spent (0 for instant crafting)."""
        inv = self.inv
        if self.try_trade():
            return 0.0
        for act in self.P["priority"]:
            if act == "salvage_shard":
                miss = self.missing_shards()
                if miss and V(self.P["salvage_use"]) == "shards" and inv["salvage"] >= self.shard_cost:
                    s = next((x for x in self.shard_order if x in miss), miss[0])
                    self.take("salvage", self.shard_cost, f"exchange -> {s}")
                    self.give(s, 1, "salvage exchange")
                    return 0.0
            elif act == "assemble":
                if all(inv[s] >= 1 for s in SHARDS):
                    for s in SHARDS:
                        self.take(s, 1, "Invitation assembly")
                    self.give("invitation", 1, "assembly")
                    self.keys_made += 1
                    self.goals.setdefault("first_invitation", self.t)
                    return 0.0
            elif act == "uber":
                if inv["invitation"] >= 1:
                    return self.run("uber")
            elif act == "steep":
                if self.steep_on and inv["core_rot"] >= V(self.A["steep"]["rot_cost"]):
                    for ch in ("chart_reliquary", "chart_last_heading"):
                        if inv[ch] >= 1:
                            return self.steep(ch)
            elif act == "farm":
                if self.pyr_share > 0 and self.rng.random() < self.pyr_share:
                    return self.run("pyramid_full")
                return self.run(self.farm)
            else:
                ent = self.A[act].get("entry")
                if ent and inv[ent] >= 1:
                    return self.run(act)
        return self.run(self.farm)

    def check_goals(self):
        g = self.goals
        if "all_skins" not in g and self.tokens_received >= self.skins:
            g["all_skins"] = self.t
        if "all_boss_variants" not in g and all(self.inv[b] >= 1 for b in self.boss):
            g["all_boss_variants"] = self.t
        if "all_variants" not in g and all(k in g for k in ("all_skins", "all_boss_variants", "heartglass", "remainder")):
            g["all_variants"] = self.t


GOALS = ["first_chart_run", "first_crownhold", "first_haul", "first_invitation", "heartglass", "remainder",
         "all_skins", "all_boss_variants", "all_variants"]


def simulate(I, ptype, trade, n, cap_hours, seed, shard_price=None):
    rng = random.Random(seed)
    res = {g: [] for g in GOALS}
    keys_per_h, clears_per_h, tok_per_h, boss_per_h = [], [], [], []
    for _ in range(n):
        p = Player(I, ptype, trade, rng, shard_price)
        while p.t < cap_hours and len(p.goals) < len(GOALS):
            p.t += p.step() / 60.0
            p.check_goals()
        for g in GOALS:
            res[g].append(p.goals.get(g))
        keys_per_h.append(p.keys_made / max(p.t, 1e-9))
        clears_per_h.append(p.uber_clears / max(p.t, 1e-9))
        tok_per_h.append(p.tokens_received / max(p.t, 1e-9))
    return res, {"keys_per_hour": statistics.mean(keys_per_h), "uber_clears_per_hour": statistics.mean(clears_per_h),
                 "tokens_per_hour": statistics.mean(tok_per_h)}


def flows(I, ptype, trade, n, weekends, seed, shard_price=None):
    rng = random.Random(seed)
    agg = defaultdict(float)
    hours = 0.0
    value = 0.0
    shards = 0.0
    keys = 0.0
    H = V(I["player_types"][ptype]["hours_per_weekend"])
    for _ in range(n):
        p = Player(I, ptype, trade, rng, shard_price, track_flows=True)
        cap = weekends * H
        while p.t < cap:
            p.t += p.step() / 60.0
        for k, q in p.flow.items():
            agg[k] += q
        hours += p.t
        value += p.value_ryo
        shards += p.shards_made
        keys += p.keys_made
    per_weekend = {k: q / hours * H for k, q in agg.items()}
    return per_weekend, {"value_per_hour": value / hours, "shards_per_hour": shards / hours, "keys_per_hour": keys / hours}


def pct(xs, q):
    xs = sorted(xs)
    i = q * (len(xs) - 1)
    lo, hi = math.floor(i), math.ceil(i)
    return xs[lo] + (xs[hi] - xs[lo]) * (i - lo)


def summarize(vals, H, cap_hours):
    got = [v for v in vals if v is not None]
    n = len(vals)
    out = {"reached_pct": 100.0 * len(got) / n}
    for q, name in ((0.5, "p50"), (0.9, "p90")):
        need = math.ceil(q * n)
        if len(got) >= need:
            h = pct([v if v is not None else float("inf") for v in vals], q)
            out[name + "_hours"] = h
            out[name + "_weekends"] = h / H
        else:
            out[name + "_hours"] = None
            out[name + "_weekends"] = None
    out["mean_hours_if_reached"] = statistics.mean(got) if got else None
    return out


def analytic_estimates(I, ptype, stats, H):
    """Rough steady-state extrapolations for goals beyond the cap (hours)."""
    c = V(I["player_types"][ptype]["uber_clear"])
    k = stats["keys_per_hour"]
    rate = k * c
    est = {}
    if rate > 0:
        est["heartglass"] = math.log(2) / rate
        est["remainder"] = V(I["proposed"]["remnant_recipes"]["remainder"]) / rate
    if k > 0:
        est["first_invitation"] = 1.0 / k
    return {g: (h, h / H) for g, h in est.items()}


# ---------------------------------------------------------------------------------------------------------------
# Scenarios and outputs
# ---------------------------------------------------------------------------------------------------------------
def fmt(x, nd=2):
    if x is None:
        return ""
    if isinstance(x, float):
        return f"{x:.{nd}f}"
    return str(x)


def fair_price(I, seed, n, weekends):
    """Fair shard price: the dedicated policy's ryo-equivalent value per hour x its hours per shard produced."""
    fl, st = flows(I, "dedicated", False, n, weekends, seed)
    if st["shards_per_hour"] <= 0:
        return None, st
    return st["value_per_hour"] / st["shards_per_hour"], st


def run_scenario(I, name, n, cap, seed, flow_n, flow_w):
    price_cfg = V(I["trade"]["shard_price_ryo"])
    if price_cfg == "auto":
        price, pst = fair_price(I, seed + 7, flow_n, flow_w)
    else:
        price, pst = float(price_cfg), None
    rows, fl_rows, est_rows = [], [], {}
    for ptype in I["player_types"]:
        H = V(I["player_types"][ptype]["hours_per_weekend"])
        for trade in (False, True):
            res, st = simulate(I, ptype, trade, n, cap, seed, price)
            est = analytic_estimates(I, ptype, st, H)
            for g in GOALS:
                s = summarize(res[g], H, cap)
                e = est.get(g)
                rows.append({"scenario": name, "player_type": ptype, "hours_per_weekend": H,
                             "trade": "with trade" if trade else "no trade", "goal": g,
                             "reached_within_cap_pct": fmt(s["reached_pct"], 1),
                             "p50_hours": fmt(s["p50_hours"], 1), "p50_weekends": fmt(s["p50_weekends"]),
                             "p90_hours": fmt(s["p90_hours"], 1), "p90_weekends": fmt(s["p90_weekends"]),
                             "cap_hours": cap,
                             "steady_state_estimate_weekends": fmt(e[1]) if e else "",
                             "shard_price_ryo": fmt(price, 0) if trade else ""})
            est_rows[(ptype, trade)] = st
        fl, fst = flows(I, ptype, False, flow_n, flow_w, seed + 1)
        for (item, d, where), q in sorted(fl.items()):
            fl_rows.append({"scenario": name, "player_type": ptype, "item": item, "direction": "source" if d == "in" else "sink",
                            "where": where, "per_weekend": fmt(q, 3)})
        fl_rows.append({"scenario": name, "player_type": ptype, "item": "ryo_equivalent_value", "direction": "source",
                        "where": "all (valued items + ryo)", "per_weekend": fmt(fst["value_per_hour"] * H, 0)})
    return rows, fl_rows, price, pst


def yields_rows(I, name):
    rows = []
    acts = [k for k in I["activities"]]
    for key in acts:
        a = I["activities"][key]
        variants = [(None, None)]
        if a["kind"] == "uber":
            variants = [(pt, None) for pt in I["player_types"]]
        if a["kind"] == "haul":
            variants = [(None, "value"), (None, "reserve")]
        for pt, route in variants:
            items, mins = activity_ev(I, key, pt, route)
            label = a["label"] + (f" [{pt}, clear {V(I['player_types'][pt]['uber_clear']):.0%}]" if pt else "") + \
                (f" [{route} route]" if route else "")
            val = sum(item_value(I, k) * q for k, q in items.items() if q > 0)
            src = f"inputs.json activities.{key}"
            rows.append({"scenario": name, "activity": key, "label": label, "item": "_minutes_per_run (per_hour = runs per hour)",
                         "per_run": fmt(mins, 2), "per_hour": fmt(60.0 / mins, 3), "source": src})
            for k, q in sorted(items.items()):
                if abs(q) < 1e-9:
                    continue
                rows.append({"scenario": name, "activity": key, "label": label, "item": k, "per_run": fmt(q, 5),
                             "per_hour": fmt(q * 60.0 / mins, 5), "source": src})
            rows.append({"scenario": name, "activity": key, "label": label, "item": "_ryo_equivalent_value",
                         "per_run": fmt(val, 0), "per_hour": fmt(val * 60 / mins, 0), "source": "inputs.values_ryo (0 where no price)"})
    return rows


def common_loop(I):
    """Per hour, a player who always takes the other common chart card loops Tide <-> Roster forever."""
    out = defaultdict(float)
    mins = 0.0
    for key, card in (("chart_tide", "Watch Roster"), ("chart_roster", "Tide Chart")):
        a = I["activities"][key]
        c = V(a["clear"])
        base = drops_ev(a["drops"])
        press = a.get("press_on")
        if press:
            pw = V(press["win"])
            alt = drops_ev(press["win_drops"])
            base = {k: (1 - pw) * base.get(k, 0) + pw * alt.get(k, 0) for k in set(base) | set(alt)}
        for k, q in base.items():
            out[k] += c * q
        _, m = activity_ev(I, key)
        mins += m
    return {k: q * 60.0 / mins for k, q in out.items()}, mins / 2


def write_csv(path, rows, fields=None):
    fields = fields or list(rows[0].keys())
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", default=os.path.join(HERE, "inputs.json"))
    ap.add_argument("--changes", default=os.path.join(HERE, "recommended.json"))
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--no-impacts", action="store_true")
    a = ap.parse_args()
    I0 = json.load(open(a.inputs))
    S = I0["sim"]
    n, cap, seed = V(S["players"]), V(S["cap_hours"]), V(S["seed"])
    fn, fw = V(S["flow_players"]), V(S["flow_weekends"])
    if a.quick:
        n, fn = 60, 40
    os.makedirs(OUT, exist_ok=True)
    rec = json.load(open(a.changes)) if os.path.exists(a.changes) else {"changes": []}
    I1 = apply_changes(I0, rec["changes"])

    all_rows, all_flows, yrows, prices = [], [], [], {}
    for name, I in (("current", I0), ("recommended", I1)):
        print(f"[{name}] simulating ...", file=sys.stderr)
        rows, fl, price, pst = run_scenario(I, name, n, cap, seed, fn, fw)
        all_rows += rows
        all_flows += fl
        yrows += yields_rows(I, name)
        prices[name] = price
        loop, lm = common_loop(I)
        for k, q in sorted(loop.items()):
            yrows.append({"scenario": name, "activity": "common_loop", "label": "Tide <-> Roster loop (always take the other common chart card)",
                          "item": k, "per_run": "", "per_hour": fmt(q, 5), "source": "chart_tide/chart_roster picks (push/skyglass_charts.gen.py:149-150)"})
    write_csv(os.path.join(OUT, "time_to_goal.csv"), all_rows)
    write_csv(os.path.join(OUT, "flows.csv"), all_flows)
    write_csv(os.path.join(OUT, "activity_yields.csv"), yrows)

    # recommended_changes.csv: combined before/after on the key goals, plus each change's isolated effect
    key = {(r["scenario"], r["player_type"], r["trade"], r["goal"]): r for r in all_rows}
    out = []
    iso_n = max(40, n // 4)
    for ch in rec["changes"]:
        row = {"id": ch["id"], "change": ch["change"], "parameters": json.dumps(ch["set"], ensure_ascii=False),
               "before": ch.get("before", ""), "after": ch.get("after", ""), "rationale": ch.get("rationale", "")}
        if not a.no_impacts:
            Ii = apply_changes(I0, [ch])
            res, _ = simulate(Ii, "dedicated", False, iso_n, cap, seed)
            s = summarize(res["first_invitation"], V(I0["player_types"]["dedicated"]["hours_per_weekend"]), cap)
            row["isolated_dedicated_first_invitation_p50_hours"] = fmt(s["p50_hours"], 1)
        out.append(row)
    for ptype in I0["player_types"]:
        for g in ("first_invitation", "heartglass", "remainder", "all_variants"):
            for tr in ("no trade", "with trade"):
                b, r = key[("current", ptype, tr, g)], key[("recommended", ptype, tr, g)]
                out.append({"id": "RESULT", "change": f"{ptype} / {g} / {tr}", "parameters": "",
                            "before": f"p50 {b['p50_weekends'] or '>cap'} wk, p90 {b['p90_weekends'] or '>cap'} wk (est {b['steady_state_estimate_weekends']})",
                            "after": f"p50 {r['p50_weekends'] or '>cap'} wk, p90 {r['p90_weekends'] or '>cap'} wk (est {r['steady_state_estimate_weekends']})",
                            "rationale": "Monte Carlo, all recommended changes together"})
    fields = ["id", "change", "parameters", "before", "after", "rationale", "isolated_dedicated_first_invitation_p50_hours"]
    write_csv(os.path.join(OUT, "recommended_changes.csv"), out, fields)
    with open(os.path.join(OUT, "run_meta.json"), "w") as f:
        json.dump({"players_per_cell": n, "cap_hours": cap, "seed": seed, "flow_players": fn, "flow_weekends": fw,
                   "shard_price_ryo": prices}, f, indent=1)
        f.write("\n")
    print(json.dumps({"shard_price_ryo": prices}), file=sys.stderr)


if __name__ == "__main__":
    main()
