#!/usr/bin/env python3
"""Build the AI pool battle-line manifest and its review sheet.

Inputs (all committed):
  battle_lines.json                    the draft text, renames and the one target change
  32b_DATA_pool.json                   the 82 pool codes and jutsu ids
  <capture bundle>                     a Forge results bundle holding jutsu.get persist:full for all 82
  recovered/ai_jutsu_..._forge.json    the reconstructed manifest, shown for comparison

Outputs:
  ai_pool_battle_lines_draft.json      82 jutsu `convert` entries (battleDescription, injectableInBattle
                                       at its captured live value per law 20, name on renames,
                                       target on B31, the full live effects list on B28 with the
                                       recoil rounds changed)
  REVIEW.md                            the prose review sheet

Usage (from the repository root):
  python3 state/ai_pool_battle_lines/build.py harvests/inbox/<bundle>.json [--check]

--check exits 1 if either output differs from what is committed. Never sends anything.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
_NESTED = json.load(open(os.path.join(ROOT, "forge/src/runner/nested.json")))
ALLOWED = {t: set(_NESTED["sets"][i]) for t, i in _NESTED["effects"].items()}
RECOVERED = os.path.join(HERE, "recovered", "ai_jutsu_battle_descriptions_82_backlash_palm_forge.json")

WORDS = {
    "damage": "damage", "pierce": "piercing damage", "drain": "drains chakra/stamina",
    "redirection": "pull/push", "onehitkill": "instant kill", "clone": "clone",
    "copy": "copies buffs", "timecompression": "actions cost more AP", "stealth": "stealth",
    "increasedamagegiven": "more damage dealt", "decreasedamagetaken": "less damage taken",
    "seal": "seals bloodline", "increasedamagetaken": "takes more damage", "afterburn": "afterburn",
    "decreasedamagegiven": "less damage dealt", "decreaseheal": "less healing",
    "decreasestat": "lowers stats", "increasestat": "raises stats",
    "absorb": "absorbs damage as health", "shield": "shield", "stun": "stun", "wound": "wound",
    "recoil": "recoil", "reflect": "reflects damage", "clear": "strips buffs", "heal": "heal",
    "poison": "poison", "moveprevent": "roots", "cleanseprevent": "blocks cleanse",
    "cleanse": "cleanses debuffs", "debuffprevent": "blocks debuffs",
}
AREA = {"ALL": "all in range", "AOE_LINE_SHOOT": "line", "AOE_CIRCLE_SHOOT": "ring",
        "AOE_CIRCLE_SPAWN": "area", "AOE_SPIRAL_SHOOT": "spiral"}
WHO = {"SELF": "self", "OTHER_USER": "other fighter", "OPPONENT": "enemy", "EMPTY_GROUND": "ground", "ALLY": "ally"}


def lint(code, line, target):
    """The house rules for these lines. Returns a list of problems."""
    out = []
    sentences = [s for s in re.split(r"(?<=[.?])\s+", line.strip()) if s]
    if not 2 <= len(sentences) <= 3:
        out.append(f"{code}: {len(sentences)} sentences (want 2-3)")
    if "%user" not in line:
        out.append(f"{code}: no %user")
    if target in ("OTHER_USER", "OPPONENT", "ALLY") and "%target" not in line:
        out.append(f"{code}: targets {target} but has no %target")
    if target in ("SELF", "EMPTY_GROUND") and "%target" in line:
        out.append(f"{code}: %target on a {target} jutsu")
    if re.search(r"%(?!user\b|target\b)", line):
        out.append(f"{code}: unknown placeholder")
    if re.search("[!—–‘’“”]", line):
        out.append(f"{code}: exclamation mark, dash or curly quote")
    if not line.endswith("."):
        out.append(f"{code}: no closing period")
    return out


def rec_rounds(rec, etype):
    return next(e.get("rounds") for e in rec["effects"] if e.get("type") == etype)


def build(bundle_path):
    src = json.load(open(os.path.join(HERE, "battle_lines.json")))["lines"]
    pool = json.load(open(os.path.join(ROOT, "32b_DATA_pool.json")))["records"]
    bundle = json.load(open(bundle_path))
    live = {c["input"]["id"]: c["data"] for c in bundle["captures"]
            if c.get("proc") == "jutsu.get" and isinstance(c.get("data"), dict)}
    recovered = {i["targetId"]: i["data"]["battleDescription"]
                 for i in json.load(open(RECOVERED))["items"]}

    problems = []
    if set(src) != set(pool):
        problems.append(f"battle_lines.json codes differ from 32b: {sorted(set(src) ^ set(pool))}")
    missing = [c for c in pool if pool[c]["id"] not in live]
    if missing:
        problems.append(f"capture bundle lacks jutsu.get bodies for {missing}")
    if problems:
        return None, None, problems

    items, review_rows, renames, changes, dropped = [], [], [], [], []
    for code in sorted(pool):
        jid = pool[code]["id"]
        rec, entry = live[jid], src[code]
        target = entry.get("target", rec["target"])
        problems += lint(code, entry["line"], target)
        data = {"battleDescription": entry["line"], "injectableInBattle": rec["injectableInBattle"]}
        if entry.get("rename"):
            data["name"] = entry["rename"]
            renames.append((code, rec["name"], entry["rename"]))
        if "target" in entry:
            data["target"] = entry["target"]
        if "effect_rounds" in entry:
            # Re-send the live effects as the server stores them: keys its validators no longer define
            # (pinned in forge/src/runner/nested.json) are dropped, as a save would drop them anyway.
            effects = []
            for e in rec["effects"]:
                keep = ALLOWED.get(e.get("type"))
                effects.append({k: v for k, v in e.items() if keep is None or k in keep})
                dropped += [f"{code} {e.get('type')}.{k}" for k in e if keep is not None and k not in keep]
            for etype, rounds in entry["effect_rounds"].items():
                hits = [e for e in effects if e.get("type") == etype]
                if len(hits) != 1:
                    problems.append(f"{code}: effect_rounds names {etype}, which appears {len(hits)} times in the live record")
                    continue
                hits[0]["rounds"] = rounds
                changes.append((code, rec["name"], etype, rec_rounds(rec, etype), rounds))
            data["effects"] = effects
        items.append({"name": entry.get("rename") or rec["name"], "entity": "jutsu", "slot": "convert",
                      "targetId": jid, "data": data})
        effects = []
        for e in rec.get("effects") or []:
            w = WORDS.get(e["type"], e["type"])
            if w not in effects:
                effects.append(w)
        area = AREA.get(rec["method"])
        who = WHO.get(target, target)
        if "target" in entry:
            who += f" (was {WHO.get(rec['target'], rec['target'])})"
        title = rec["name"] + (f" → **{entry['rename']}**" if entry.get("rename") else "")
        review_rows.append((code, title, f"{who}{', ' + area if area else ''}: {', '.join(effects)}",
                            entry["line"], recovered.get(jid, "")))

    manifest = {
        "_note": ("DRAFT for director prose review, NOT FOR LIVE USE. Generated by "
                  "state/ai_pool_battle_lines/build.py from battle_lines.json; do not hand-edit. 82 shared-AI-pool "
                  "jutsu: battleDescription rewritten, %d renames, B31 retargeted to ALLY, B28 recoil 2 rounds, injectableInBattle "
                  "re-sent at its captured live value (law 20) from %s. Laws 18 and 60: run ONLY between the "
                  "validated unequip and re-equip manifests." % (len(renames), os.path.relpath(bundle_path, ROOT))),
        "items": items,
    }
    lines = ["# AI pool battle lines: draft for prose review", "",
             "Generated by `build.py` from `battle_lines.json`; edit the source, then rebuild.", "",
             "82 shared-AI-pool jutsu. Each line is 2-3 sentences in an Edo-era ninja voice and describes only "
             "effects the live record carries. `%user` and `%target` are filled in by the game.", "",
             f"Capture: `{os.path.relpath(bundle_path, ROOT)}`.", "",
             f"## Proposed renames ({len(renames)})", "", "| Code | Current | Proposed |", "|---|---|---|"]
    lines += [f"| {c} | {old} | **{new}** |" for c, old, new in renames]
    lines += ["", "## Mechanical changes", "",
              "- B31 Rallying Spiral: `target` OTHER_USER → ALLY. Its buffs (less damage taken, more damage dealt) "
              "used to land on the enemy (RUL-2026-10-21-004)."]
    lines += [f"- {c} {name}: `{etype}` rounds {old} → {new}; the rest of the effects list is re-sent unchanged "
              "(RUL-2026-10-21-005)." for c, name, etype, old, new in changes]
    if dropped:
        lines += [f"- Obsolete effect keys left out of the re-sent list (the server drops them on any save): "
                  + ", ".join(f"`{d}`" for d in dropped) + "."]
    lines += ["", "## All 82 lines", ""]
    for code, title, mech, new, old in review_rows:
        lines += [f"### {code} · {title}", f"*{mech}*", "", f"- **New:** {new}", f"- Recovered: {old}", ""]
    return (json.dumps(manifest, indent=1, ensure_ascii=False) + "\n",
            "\n".join(lines).rstrip("\n") + "\n", problems)


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__)
        return 2
    manifest, review, problems = build(args[0])
    for p in problems:
        print("ERROR ", p)
    if manifest is None or problems:
        return 1
    targets = {"ai_pool_battle_lines_draft.json": manifest, "REVIEW.md": review}
    if "--check" in argv:
        stale = [n for n, body in targets.items()
                 if not os.path.exists(os.path.join(HERE, n)) or open(os.path.join(HERE, n)).read() != body]
        print("stale: " + ", ".join(stale) if stale else "current")
        return 1 if stale else 0
    for n, body in targets.items():
        open(os.path.join(HERE, n), "w").write(body)
    print("wrote", ", ".join(targets), "| 82 entries, 0 problems")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
