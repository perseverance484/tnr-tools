"""Mother of Echoes puzzle report (director design intent, 2026-11-05).

  python3 tools/moe_puzzle.py results/*.json

Per cell: clears; damage taken split into READABLE mechanics (telegraphed eruptions, follow-the-player marks, pools,
debuffs, the Feeler's Grasp, Breathless Pull) vs untelegraphed FILLER (Glass Lancet, summon hits, The Quiet) vs the
enrage; deaths by the same split; Glass Lancet per landed hit as % of the player's max HP, by act; solvability (player
turns that started with no free hex within reach 5 clear of every live mark; and clear of marks + pools); misread
Recasts. "own turn" damage (pool / mark drains that land on the player's own action) is counted as readable.
"""
import collections, json, statistics, sys

ERUPT = ("Refraction", "Facet", "Lucid", "Nothing Moves", "Stillness", "Recast", "Shatterfall", "Every Name", "Glassfall")
FILLER_SUMMON = ("Your Likeness", "Gate Porter", "Cadet Tomo", "Tomo")


def cat(src: str) -> str:
    if src.startswith("own turn"): return "readable"
    who, _, move = src.partition(": ")
    if "Glass Remembers" in move: return "enrage"
    if any(w in who for w in FILLER_SUMMON): return "filler"
    if "Feeler" in who: return "readable"
    if any(move.startswith(e) for e in ERUPT) or "Breathless" in move or "Hush" in move: return "readable"
    return "filler"  # Glass Lancet, The Quiet, anything untelegraphed


def pct(a, b): return round(100 * a / b) if b else 0


for f in sys.argv[1:]:
    d = json.load(open(f))
    for cn, c in d["cells"].items():
        label = cn + ("" if d.get("kill", "sayo") == "sayo" else " (silence first)")
        runs = c["runs"]
        dmg = collections.defaultdict(lambda: collections.Counter())
        deaths = collections.Counter()
        lanc = collections.defaultdict(list)
        solv = collections.Counter()
        rmis = 0
        for r in runs:
            for a in r["acts"]:
                for k, v in (a.get("dmgBySource") or {}).items(): dmg[a["act"]][cat(k)] += v
                if a.get("deathCause"): deaths[f"A{a['act']} {cat(a['deathCause'])}"] += 1
                lanc[a["act"]] += (a.get("lancet") or {}).get("pctOfMax", [])
                s = a.get("solv") or {}
                solv["turns"] += s.get("turns", 0); solv["noSafe"] += s.get("noSafe", 0); solv["noSafePools"] += s.get("noSafeInclPools", 0)
                rmis += a.get("recastMisreads", 0) or 0
        share = {}
        for act in sorted(dmg):
            t = sum(dmg[act].values())
            share[act] = f"read {pct(dmg[act]['readable'], t)}% / filler {pct(dmg[act]['filler'], t)}% / enrage {pct(dmg[act]['enrage'], t)}%"
        lt = {act: (round(statistics.mean(v), 1), round(statistics.median(v), 1), max(v), len(v)) for act, v in sorted(lanc.items()) if v}
        print(f"{label} [{f.split('/')[-1]}]: clears {sum(r['cleared'] for r in runs)}/{len(runs)}")
        print(f"   damage share by act: {share}")
        print(f"   deaths: {dict(deaths)}")
        print(f"   Lancet per landed hit, % of max HP (mean, median, max, n): {lt}")
        print(f"   solvability: {solv['noSafe']} of {solv['turns']} player turns with no safe reachable hex (marks); {solv['noSafePools']} counting pools; misread Recasts {rmis}")
