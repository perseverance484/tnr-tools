#!/usr/bin/env python3
"""Write docs/combat-engine/rules.json: the engine's numeric combat constants (caps, base pools, timing), each read
from the game source with its file and line, so tools load numbers instead of hardcoding them.

    python3 rules.py /path/to/TheNinjaRPG [out.json] [--revision SHORT_SHA]

The game root must be a git checkout (its HEAD is recorded as pinned_game_commit). For an archive or any copy
without git metadata, pass --revision with the commit it was taken from; with neither, the script exits 1 rather
than write an empty commit. read_constants() is shared with combat_map.py --check --game.
"""
import argparse
import json
import os
import re
import subprocess
import sys

NAMES = {
    # libs/combat/constants.ts
    "DAMAGE_LEECH_CAP_RATIO": ("caps", "lifesteal_vamp", "Lifesteal plus vamp, shared: floor(cap x pre-shield immediate hit), vamp paid first"),
    "REFLECT_CAP_RATIO": ("caps", "reflect", "Reflect, as a fraction of the pre-Diffuse hit, not rounded, applied after the shield soak"),
    "ABSORB_CAP_RATIO": ("caps", "absorb", "Absorb HP share only, as a fraction of the immediate (post-Diffuse, pre-shield) hit; CP/SP shares uncapped"),
    "AFTERBURN_CAP_RATIO": ("caps", "afterburn", "Stacked afterburn per hit, floor(cap x hit), applied when the readers run"),
    "COMBAT_SECONDS": ("timing", "turn_seconds", "Seconds per turn"),
    # drizzle/constants.ts
    "BATTLE_TAG_STACKING": ("stacking", "same_tag_stacks", "Same tag from the same caster on the same target stacks"),
    "SHIELD_MAX_HEALTH": ("caps", "shield_hp", "Shield tag health ceiling, and the most new Consume/Siphon shield HP per fighter per action"),
    "DMG_REDUCTION_CAP": ("caps", "damage_reduction", "Reductions after the 50% system DR stop at this share: a hit never falls below 10% of its post-system-DR value"),
    "OUT_OF_COMBAT_BASE_DAMAGE_INCREASE": ("base", "damage_increase_points", "Percentage points in the pre-battle increase pool"),
    "OUT_OF_COMBAT_BASE_DAMAGE_REDUCTION": ("base", "damage_reduction_points", "Percentage points in the pre-battle DR pool"),
    "PARRY_MAX_PERCENTAGE": ("caps", "parry_pct", "Parry, summed, in percent"),
    "DIFFUSE_MAX_PERCENTAGE": ("caps", "diffuse_pct", "Diffuse, in percent"),
    "DIFFUSE_DEFAULT_DELAY_ROUNDS": ("timing", "diffuse_delay_rounds", "Default Diffuse delayRounds: debt repaid over the holder's next N acting rounds"),
    "TEMPORAL_AP_DELTA": ("timing", "temporal_ap_delta", "AP added or removed by timedilation / timecompression"),
    "COPY_MAX_TAGS": ("caps", "copy_held", "Copied tags held per caster"),
    "MIRROR_MAX_TAGS": ("caps", "mirror_held", "Mirrored tags held per caster"),
}
FILES = ["app/src/libs/combat/constants.ts", "app/drizzle/constants.ts"]


def value(raw):
    raw = raw.strip()
    if raw in ("true", "false"):
        return raw == "true"
    return float(raw) if "." in raw else int(raw)


def read_constants(root):
    """{group: {key: {value, what, source}}} for every name in NAMES, read from the game source at root."""
    res = {"caps": {}, "base": {}, "timing": {}, "stacking": {}}
    found = set()
    for rel in FILES:
        for i, line in enumerate(open(os.path.join(root, rel)), 1):
            m = re.match(r"export const (\w+) = ([\w.]+);", line)
            if m and m.group(1) in NAMES:
                grp, key, what = NAMES[m.group(1)]
                res[grp][key] = {"value": value(m.group(2)), "what": what,
                                 "source": f"{rel.replace('app/src/', '').replace('app/', '')}:{i} {m.group(1)}"}
                found.add(m.group(1))
    missing = set(NAMES) - found
    if missing:
        raise ValueError(f"not found in source: {sorted(missing)}")
    return res


def git_head(root):
    """Short HEAD of root, or "" when root is not a git checkout."""
    r = subprocess.run(["git", "-C", root, "rev-parse", "--short", "HEAD"], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def main(argv):
    ap = argparse.ArgumentParser(description="Write rules.json from the game source.")
    ap.add_argument("game_root")
    ap.add_argument("out", nargs="?", default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                         "rules.json"))
    ap.add_argument("--revision", help="game commit to record when game_root has no git metadata")
    a = ap.parse_args(argv)
    head = git_head(a.game_root)
    if head and a.revision and not head.startswith(a.revision[:len(head)]) and not a.revision.startswith(head):
        sys.exit(f"--revision {a.revision} does not match the checkout's HEAD {head}")
    commit = head or (a.revision or "").strip()
    if not commit:
        sys.exit(f"{a.game_root} is not a git checkout; pass --revision with the game commit it was taken from")
    try:
        res = read_constants(a.game_root)
    except ValueError as e:
        sys.exit(str(e))
    res = {"pinned_game_commit": commit, **res}
    json.dump(res, open(a.out, "w"), indent=1)
    print(f"wrote {a.out}: {sum(len(v) for v in res.values() if isinstance(v, dict))} constants @ {commit}")


if __name__ == "__main__":
    main(sys.argv[1:])
