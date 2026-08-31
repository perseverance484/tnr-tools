"""push/37_pale_fang_b10_swap.json - swaps Veilstrike (B24) for Sovereign Ascendance (B10)
on Pale Fang.

REQUIRES the push/36 capture bundle. This script refuses to run without it: the live kit
and the live aiProfile rule chain have never been read, and the 2026-08-26 registry snapshot
cannot stand in for either.

Two coupled edits:
  1. the jutsu comes off Pale Fang's kit and B10 goes on in the same slot
  2. every aiProfile rule naming the Veilstrike id is repointed at B10

Doing only 1 leaves a rule pointing at a jutsu the AI does not own. Doing only 2 leaves the
AI holding a jutsu no rule fires.

Verification note (ai.md, equip-array ref law): an unresolvable id in the `jutsus` array is
STRIPPED SERVER-SIDE and the entry still reports ok. A green row therefore proves nothing
here - the read-back is the only evidence, and it must show B10 present AND Veilstrike gone.
"""
import json, os, glob

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POOL = json.load(open(os.path.join(R, "32b_DATA_pool.json")))["records"]
OLD, NEW = POOL["B24"], POOL["B10"]
assert OLD["name"] == "Veilstrike" and NEW["name"] == "Sovereign Ascendance"
assert NEW["target"] == "self" and NEW["ap"] == OLD["ap"] == 40      # round economy unchanged
assert not any("stealth" in e for e in NEW["effects"])               # the whole point

cap = None
for p in sorted(glob.glob(os.path.join(R, "harvests/inbox/*.json")), key=os.path.getmtime, reverse=True):
    b = json.load(open(p))
    procs = {c.get("proc") for c in b.get("captures", [])}
    if "profile.getAi" in procs:
        cap = b; src = p; break
assert cap, ("no bundle in harvests/inbox contains a profile.getAi capture - run push/36 first. "
             "Nothing here may be composed from the registry snapshot.")

ai = None
for c in cap["captures"]:
    if c.get("proc") != "profile.getAi": continue
    r = c["data"]
    if isinstance(r, dict) and "data" in r: r = r["data"]
    if isinstance(r, list): r = r[0]
    ai = r
assert ai and ai.get("username") == "Pale Fang" or ai.get("userId"), "unexpected getAi shape - inspect before building"
print("captured Pale Fang from", os.path.basename(src))
print("  kit field candidates:", [k for k in ai if "jutsu" in k.lower()])
print("  profile field candidates:", [k for k in ai if "profile" in k.lower() or "rule" in k.lower()])
print()
print("STOP: the getAi shape has not been seen before. Inspect the printed fields, then finish")
print("this generator against the real field names rather than guessing them.")
