#!/usr/bin/env python3
"""Opponent profile from his equipped kit (director 2026-11-11: "see what bloodline jutsu they have equipped, then
match that to the rank, then give them the corresponding boost and elements. Real quick calls").

One read at battle start (the pilot sends jutsu.getPublicUserJutsus once per opponent; opponent_kit.save_kit stores
it). Everything else is offline: his bloodline jutsu -> bloodlineId (catalog) -> the bloodline record
(kit/bloodlines.json: rank and its passive effects), and the elements of his damage jutsu (catalog).
Usage: opp_profile.py USER_ID
"""
import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import engine_bridge as EB  # noqa: E402

_BL = None
_IDX = None


def _index():
    """jutsuId -> [bloodlineId, damage elements], a compact cache of the 8 MB catalog (rebuilt when the catalog
    changes) so a profile builds in milliseconds."""
    global _IDX
    if _IDX is None:
        cat = os.path.join(EB.HARNESS, "kit", "catalog.json")
        idx = os.path.join(HERE, "..", "fights", "live", "jutsu_index.json")
        try:
            if os.path.getmtime(idx) >= os.path.getmtime(cat):
                _IDX = json.load(open(idx))
                return _IDX
        except OSError:
            pass
        _IDX = {j: [v.get("record", {}).get("bloodlineId") or "", elements_of(v.get("record", {}))]
                for j, v in EB._records().items()}
        os.makedirs(os.path.dirname(idx), exist_ok=True)
        json.dump(_IDX, open(idx, "w"))
    return _IDX


def _bloodlines():
    global _BL
    if _BL is None:
        try:
            _BL = json.load(open(os.path.join(EB.HARNESS, "kit", "bloodlines.json")))
        except (OSError, ValueError):
            _BL = {}
    return _BL


def elements_of(rec):
    """Elements of a jutsu's damage (its damage/pierce effects), e.g. ['Fire'] or ['None']."""
    out = []
    for e in rec.get("effects", []):
        if e.get("type") in ("damage", "pierce") and e.get("elements"):
            out += e["elements"]
    return sorted(set(out))


def profile(user_id, rows=()):
    """{bloodline, rank, given: (pct, elements), dr: (pct, elements), elements: his damage elements, source} or {}."""
    kit = EB.opponent_kit(user_id) or {}
    idx = _index()
    ids = list(kit.get("jutsu", [])) + [a for r, u, a, _ in rows if u == user_id]
    votes = collections.Counter(idx[j][0] for j in ids if j in idx and idx[j][0])
    bl_id = kit.get("bloodlineId") or (votes.most_common(1)[0][0] if votes else None)
    out = {"source": "kit" if kit else ("log" if ids else "none")}
    els = collections.Counter()
    for j in ids:
        if j in idx:
            els.update(idx[j][1])
    out["elements"] = [e for e, _ in els.most_common()]
    bl = _bloodlines().get(bl_id) if bl_id else None
    if not bl:
        # no bloodline jutsu seen: the common endgame passive (+25% given on his elements and None) as the stand-in
        out.update(bloodline="unknown", rank="?", given=(0.25, out["elements"] + ["None"]), dr=(0.0, []))
        return out
    out.update(bloodline=bl["name"], rank=bl.get("rank"), given=(0.0, []), dr=(0.0, []))
    for e in bl.get("effects", []):
        if e.get("calculation") != "percentage":
            continue
        if e["type"] == "increasedamagegiven":
            out["given"] = (e["power"] / 100, e.get("elements") or [])
        elif e["type"] == "decreasedamagetaken":
            out["dr"] = (e["power"] / 100, e.get("elements") or [])
    return out


def given_mult(p):
    """His bloodline boost on his own hits: applies when his damage elements fall in the boosted set."""
    pct, els = p.get("given", (0.0, []))
    if not pct:
        return 1.0
    mine = p.get("elements") or ["None"]
    share = sum(1 for e in mine if e in els) / len(mine)
    return 1 + pct * share


def dr_vs(p, elements):
    """His bloodline damage reduction against a hit of these elements (1.0 = none)."""
    pct, els = p.get("dr", (0.0, []))
    return 1 - pct if pct and any(e in els for e in (elements or ["None"])) else 1.0


if __name__ == "__main__":
    print(json.dumps(profile(sys.argv[1]), indent=1))
