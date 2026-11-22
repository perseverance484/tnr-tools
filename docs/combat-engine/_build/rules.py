#!/usr/bin/env python3
"""Write docs/combat-engine/rules.json: the engine's numeric combat constants (caps, base pools, timing), each read
from the game source with its file and line, so tools load numbers instead of hardcoding them.

    python3 rules.py /path/to/TheNinjaRPG [out.json] [--revision FULL_SHA]

In a git checkout the constants are read from the HEAD commit's objects, the full SHA is recorded as
pinned_game_commit, and the script exits 1 if the two source files differ from HEAD. For an archive or any copy
without git metadata, pass --revision with the full 40-character commit it was taken from; without it the script
exits 1 rather than write an empty or ambiguous pin. read_constants() is shared with combat_map.py --check --game.
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


HEX40 = re.compile(r"^[0-9a-f]{40}$")


def _git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True, text=True)


def git_head(root):
    """Full HEAD SHA of root, or "" when root is not a git checkout."""
    r = _git(root, "rev-parse", "--verify", "HEAD^{commit}")
    return r.stdout.strip() if r.returncode == 0 else ""


def resolve_commit(root, rev):
    """Full SHA of rev in root's git history, or "" when it isn't there."""
    if not rev:
        return ""
    r = _git(root, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
    return r.stdout.strip() if r.returncode == 0 else ""


def changed_files(root, commit):
    """FILES whose working copy differs from commit (empty for a clean tree)."""
    out = []
    for rel in FILES:
        path = os.path.join(root, rel)
        want = _git(root, "show", f"{commit}:{rel}").stdout
        have = open(path).read() if os.path.exists(path) else None
        if have != want:
            out.append(rel)
    return out


def _lines(root, rel, commit):
    if commit:
        r = _git(root, "show", f"{commit}:{rel}")
        if r.returncode != 0:
            raise ValueError(f"{rel} not in commit {commit}: {r.stderr.strip()}")
        return r.stdout.splitlines(keepends=True)
    return open(os.path.join(root, rel)).readlines()


def read_constants(root, commit=None):
    """{group: {key: {value, what, source}}} for every name in NAMES. With commit, read from that git object, not
    the working tree, so local edits can't stand in for the pinned revision."""
    res = {"caps": {}, "base": {}, "timing": {}, "stacking": {}}
    found = set()
    for rel in FILES:
        for i, line in enumerate(_lines(root, rel, commit), 1):
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


def main(argv):
    ap = argparse.ArgumentParser(description="Write rules.json from the game source.")
    ap.add_argument("game_root")
    ap.add_argument("out", nargs="?", default=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                                                         "rules.json"))
    ap.add_argument("--revision", help="full 40-character game commit; required when game_root has no git metadata")
    a = ap.parse_args(argv)
    head = git_head(a.game_root)
    if head:
        commit = head
        if a.revision and resolve_commit(a.game_root, a.revision) != head:
            sys.exit(f"--revision {a.revision} is not the checkout's HEAD {head}")
        changed = changed_files(a.game_root, commit)
        if changed:
            sys.exit(f"{', '.join(changed)} differ from HEAD {head}; commit or discard the changes first")
    else:
        commit = (a.revision or "").strip().lower()
        if not HEX40.match(commit):
            sys.exit(f"{a.game_root} is not a git checkout; pass --revision with the full 40-character game commit "
                     f"it was taken from")
    try:
        res = read_constants(a.game_root, commit if head else None)
    except ValueError as e:
        sys.exit(str(e))
    res = {"pinned_game_commit": commit, **res}
    json.dump(res, open(a.out, "w"), indent=1)
    print(f"wrote {a.out}: {sum(len(v) for v in res.values() if isinstance(v, dict))} constants @ {commit}")


if __name__ == "__main__":
    main(sys.argv[1:])
