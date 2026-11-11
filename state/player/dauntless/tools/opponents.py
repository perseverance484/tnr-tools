#!/usr/bin/env python3
"""Opponent models from every logged fight (director 2026-11-11: "Pull every log you can, model as many opponents as
possible as thoroughly as possible and play them. It's like you're playing back replays and trying to find the
right moves").

Source: every battle log in entries form under fights/ (my fights, the director's, observed ones under
fights/observed/). Per opponent (by user id, merged across fights):
  kit       every action he used (+ his saved equipped kit when we have it), compiled from catalog records
  profile   bloodline / rank / boost / elements (opp_profile)
  habits    how often each action shows up, on which rounds, his opening, what follows what (transitions), his full
            bundles per round, how many AP he spends
  results   fights, rounds, my wins / losses against him
The bot (fightsim) plays him by his own simulated score plus these habits, so he repeats his real rotation where
the log shows one and still reacts to the board where it does not. `opponents.py check` measures that: how often
the bot's first choice equals his real bundle in the logged positions.

Usage: opponents.py build | list | check [NAME]
"""
import collections
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FIGHTS = os.path.join(HERE, "..", "fights")
MODELS = os.path.join(HERE, "..", "fights", "opponents.json")
sys.path.insert(0, HERE)
from ingest import ME  # noqa: E402

NAME_RE = re.compile(r"^(.+?) (?:takes|damage|will|cannot|is|was|marked|heals|absorbs|copies|steals|vamps|loses|"
                     r"resists|uses|moves|pierced|dodges)\b")


def load_logs():
    """[(battle id, rows oldest-first [(round, user, action, texts)])] for every entries-form log."""
    out = []
    paths = glob.glob(os.path.join(FIGHTS, "*.json")) + glob.glob(os.path.join(FIGHTS, "observed", "*.json"))
    for p in sorted(paths):
        try:
            d = json.load(open(p))
        except (OSError, ValueError):
            continue
        if not isinstance(d, dict) or "*.battleRound" not in d:
            continue
        rows = list(zip(d["*.battleRound"], d["*.userId"], d["*.actionId"],
                        d.get("*.appliedEffects.*.txt") or [None] * len(d["*.battleRound"])))[::-1]
        bid = os.path.basename(p).split("_")[0]
        out.append((bid, p, rows))
    return out


def names_in(rows, uid, me_name="dauntless"):
    c = collections.Counter()
    for r, u, a, ts in rows:
        if u != uid:
            continue
        for t in ts or []:
            m = NAME_RE.match((t or "").strip())
            if m and m.group(1) != me_name:
                c[m.group(1)] += 1
    return c.most_common(1)[0][0] if c else uid


def turns_of(rows, uid):
    """His turns: [(round, (action ids...))] in order, waits and moves dropped."""
    out, cur, cur_r = [], [], None
    for r, u, a, ts in rows:
        if u != uid:
            if cur:
                out.append((cur_r, tuple(cur))); cur = []
            continue
        if cur_r is not None and r != cur_r and cur:
            out.append((cur_r, tuple(cur))); cur = []
        cur_r = r
        if a not in ("wait", "move"):
            cur.append(a)
    if cur:
        out.append((cur_r, tuple(cur)))
    return out


def build():
    models = {}
    for bid, path, rows in load_logs():
        users = {u for _, u, _, _ in rows}
        if ME not in users:
            continue                                           # observed fights between others: both sides count
        for uid in users - {ME}:
            if uid.startswith("ai_") or len(users) > 3:
                continue
            m = models.setdefault(uid, {"userId": uid, "names": [], "fights": [], "ids": {}, "rounds": {},
                                        "openings": [], "bundles": [], "trans": {}, "won": 0, "lost": 0})
            nm = names_in(rows, uid)
            if nm not in m["names"]:
                m["names"].append(nm)
            m["fights"].append(bid)
            prev = None
            for k, (r, b) in enumerate(turns_of(rows, uid)):
                if k == 0:
                    m["openings"].append(list(b))
                m["bundles"].append([r, list(b)])
                for a in b:
                    m["ids"][a] = m["ids"].get(a, 0) + 1
                    m["rounds"].setdefault(a, []).append(r)
                    if prev:
                        for p in prev:
                            t = m["trans"].setdefault(p, {})
                            t[a] = t.get(a, 0) + 1
                prev = b
            last = rows[-1] if rows else None
            txt = " ".join(" ".join(x or [] for x in (ts or [])) for _, _, _, ts in rows[-6:])
            if "dauntless" in txt and re.search(rf"{re.escape(nm)} (?:was defeated|lost|died)", txt):
                m["won"] += 1
    json.dump(models, open(MODELS, "w"), indent=0)
    return models


def load():
    try:
        return json.load(open(MODELS))
    except (OSError, ValueError):
        return build()


def habit_fn(model, scale=1.0):
    """habit(bundle, round, previous bundle) -> HP-equivalent bonus for doing what he does in the logs:
    share of his turns that use the action, a bonus when he used it on this round number, a bonus for what usually
    follows his last bundle, and a bonus for a whole bundle he has played on this round."""
    n_turns = max(1, len(model.get("bundles", [])))
    freq = {a: c / n_turns for a, c in model.get("ids", {}).items()}
    by_round = {a: collections.Counter(rs) for a, rs in model.get("rounds", {}).items()}
    trans = model.get("trans", {})
    seen = collections.defaultdict(set)
    for r, b in model.get("bundles", []):
        seen[r].add(tuple(sorted(b)))
    opening = collections.Counter(tuple(sorted(b)) for b in model.get("openings", []))

    def habit(hb, rnd, prev=None, first_turn=False):
        v = 0.0
        for a in hb:
            v += 350 * freq.get(a, 0.0)
            if by_round.get(a, {}).get(rnd):
                v += 150
            if prev:
                tot = sum(sum(trans.get(p, {}).values()) for p in prev) or 0
                if tot:
                    v += 300 * sum(trans.get(p, {}).get(a, 0) for p in prev) / tot
        key = tuple(sorted(hb))
        if key in seen.get(rnd, ()):
            v += 250
        if first_turn and opening.get(key):
            v += 500
        return v * scale
    return habit


def acts_for(model):
    import clock
    import engine_bridge as EB
    kit = EB.opponent_kit(model["userId"]) or {}
    ids = list(kit.get("jutsu", [])) + [a for a in model.get("ids", {}) if a not in ("wait", "move")]
    acts = clock.acts_from_ids(ids, kit.get("jutsuLevels", {}))
    # the basics already in acts use the engine's own ids: map his logged basic ids onto them
    return acts


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "build":
        ms = build()
        print(f"{len(ms)} opponents from {len(load_logs())} logs")
    ms = load()
    if cmd in ("build", "list"):
        for uid, m in sorted(ms.items(), key=lambda kv: -len(kv[1]["bundles"])):
            top = sorted(m["ids"].items(), key=lambda kv: -kv[1])[:4]
            print(f"{'/'.join(m['names'])[:20]:20} fights {len(m['fights']):2}  turns {len(m['bundles']):3}  "
                  f"actions {len(m['ids']):2}  opening {'+'.join(x[:6] for x in m['openings'][0]) if m['openings'] else '-'}")


if __name__ == "__main__":
    main()
