#!/usr/bin/env python3
"""Write tags/<tag>.yaml and tags.json from the curated data plus the game source.

Usage:
  python3 kb.py GAME_REPO_ROOT DATA_JSON OUT_DIR [--extract RESOLVED_JSON]

GAME_REPO_ROOT  TheNinjaRPG checkout (the directory holding app/), pinned commit.
DATA_JSON       data.py's output (curated behavior, stage, polarity, links, usage).
OUT_DIR         gets tags/<tag>.yaml and tags.json. Point it at a scratch directory and diff
                before copying over docs/combat-engine/.
--extract       extract.py's output; without it kb.py runs extract.py in-process.

Curated text (behavior, stage, live_from, applies, links) is copied from DATA_JSON unchanged.
Fields and calculation come from extract.py's resolved schemas. Source lines are read from the
game files: EFFECT_SORT_RANK only from inside its Map literal (spreads followed to their
definition), and the applyEffects dispatch pass from process.ts.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import extract as X
import curation as CUR  # noqa: E402

SRC = "app/src"
BASE_GROUPS = ("BaseAttributes", "PowerAttributes")

HANDLER = {"damage": "damageUser", "pierce": "damageUser", "elementaldamage": None, "onehitkill": "onehitkill",
           "weakness": "weakness", "wound": "wound", "afterburn": "afterburn", "poison": "poison", "drain": "drain",
           "diffuse": None, "curse": "curse", "increasedamagegiven": "increaseDamageGiven",
           "decreasedamagegiven": "decreaseDamageGiven", "increasedamagetaken": "increaseDamageTaken",
           "decreasedamagetaken": "decreaseDamageTaken", "increasepotency": "potency", "decreasepotency": "potency",
           "increasestat": "increaseStats", "decreasestat": "decreaseStats", "increasemastery": "increaseMastery",
           "decreasemastery": "decreaseMastery", "shield": "shield", "barrier": "damageBarrier", "absorb": "absorb",
           "siphon": "registerShieldConversion", "consume": "registerShieldConversion", "finalstand": "finalStand",
           "reflect": "reflect", "parry": "parry", "recoil": "recoil", "mirror": "mirror", "heal": "heal",
           "lifesteal": "lifesteal", "vamp": "vamp", "increaseheal": "increaseHealGiven",
           "decreaseheal": "decreaseHealGiven", "clear": "clear", "cleanse": "cleanse", "copy": "copy",
           "immunity": "immunity", "stun": "stun", "seal": "seal", "elementalseal": "elementalseal",
           "stealth": "stealth", "timecompression": "temporalShift", "timedilation": "temporalShift",
           "increasepoolcost": "increasepoolcost", "decreasepoolcost": "decreasepoolcost",
           "increasecooldown": "increaseCooldown", "decreasecooldown": "decreaseCooldown",
           "injectjutsus": "injectjutsus", "increaserange": "increaseRange", "move": "move",
           "redirection": "redirection", "summon": "summon", "clone": "clone", "increasemaxpools": "increaseMaxPools",
           "decreasemaxpools": "decreaseMaxPools", "rob": "rob", "flee": "flee", "increaseaggro": "adjustAggro",
           "decreaseaggro": "adjustAggro"}
for _p in ("buffprevent debuffprevent clearprevent cleanseprevent stunprevent sealprevent summonprevent "
           "onehitkillprevent robprevent fleeprevent healprevent moveprevent disarm").split():
    HANDLER[_p] = "applyPreventTag"

# Extra citations: "file function [note]". The function is looked up in that file and its line added;
# a name that is not defined there is reported and left without a line.
EXTRA_SRC = {
    "elementaldamage": ["libs/combat/elementalDamage.ts resolveElementalDamage"],
    "diffuse": ["libs/combat/damagePipeline.ts applyDiffuseToConsequences"],
    "curse": ["libs/combat/tags.ts settleCurse", "libs/combat/curse.ts getCurseDamageMultiplier (curse bonus)"],
    "increasedamagegiven": ["libs/combat/damagePipeline.ts computeDamagePacket"],
    "decreasedamagegiven": ["libs/combat/damagePipeline.ts computeDamagePacket"],
    "increasedamagetaken": ["libs/combat/damagePipeline.ts computeDamagePacket"],
    "decreasedamagetaken": ["libs/combat/damagePipeline.ts computeDamagePacket"],
    "increasepotency": ["libs/combat/potency.ts resolvePotencyTags"],
    "decreasepotency": ["libs/combat/potency.ts resolvePotencyTags"],
    "shield": ["libs/combat/process.ts mitigateConsequence"],
    "finalstand": ["libs/combat/tags.ts applyFinalStandDamage"],
    "pierce": ["libs/combat/process.ts mitigateConsequence (destroys shields)"],
    "stun": ["libs/combat/turn.ts calcApReduction"],
    "stealth": ["libs/combat/actions.ts availableUserActions", "libs/combat/actions.ts (stealthed target skipped)"],
    "disarm": ["libs/combat/actions.ts availableUserActions"],
    "moveprevent": ["libs/combat/actions.ts availableUserActions"],
    "summonprevent": ["libs/combat/actions.ts availableUserActions"],
    "elementalseal": ["libs/combat/actions.ts availableUserActions"],
    "injectjutsus": ["libs/combat/actions.ts availableUserActions"],
    "seal": ["libs/combat/util.ts isEffectEnabled / sealCheck"],
    "weakness": ["libs/combat/tags.ts calcDmgModifier"],
    "barrier": ["libs/combat/actions.ts (barrier path absorb)"],
    "damage": ["libs/combat/tags.ts damageCalc", "libs/combat/damagePipeline.ts computeDamagePacket"],
}

EX_AREA = {"dmgnow": "Damage now", "dmglater": "Damage later", "scaling": "Damage scaling", "soak": "Soak damage",
           "sendback": "Send it back", "heal": "Healing", "remove": "Remove effects", "take": "Take effects",
           "protect": "Protection", "deny": "Deny actions", "speed": "Speed up actions", "position": "Position",
           "fighters": "Extra fighters", "pools": "Pools and money", "escape": "Escape",
           "aggro": "Enemy AI focus (PvE)", "sage": "Sage mode", "noncombat": "Outside battle or cosmetic"}
STAGE_TXT = {"nc": "outside combat"}   # combat tags take their stage from curation.STAGE (S0-S16)
LIVE = {}
for _t in ("increasedamagegiven decreasedamagegiven increasedamagetaken decreasedamagetaken increasestat "
           "decreasestat increasemastery decreasemastery increasepotency decreasepotency absorb reflect parry recoil "
           "afterburn lifesteal increaseheal decreaseheal").split():
    LIVE[_t] = "next round (waits while isNew/castThisRound)"
for _t in "damage pierce heal".split():
    LIVE[_t] = "on cast if rounds 0 (instant); residual ticks on later rounds"
TICK = set(("damage pierce heal drain wound poison clear cleanse flee rob stun seal increasepoolcost decreasepoolcost "
            "onehitkill increaseaggro decreaseaggro").split())

# Tags rewritten into another type before effects resolve (elementalDamage.ts resolveElementalDamage).
RUNTIME_AS = {"elementaldamage": "damage"}

POLARITY_NOTE = "positive = Clear removes; negative = Cleanse removes; neutral = neither"
FIELDS_NOTE = ("zod expressions resolved from the schema (helpers, spreads, extend); fields inherited unchanged "
               "from BaseAttributes/PowerAttributes are in engine.md section 6")


class BuildError(Exception):
    pass


def yq(s):
    s = str(s)
    if s == "":
        return '""'
    if re.search(r"[:#\[\]{}&*!|>'\"%@`,]|^\s|\s$|^-", s) or s.lower() in ("yes", "no", "true", "false", "null",
                                                                             "on", "off"):
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s


def line_of(lines, pat, start=0):
    for i, l in enumerate(lines[start:], start):
        if re.search(pat, l):
            return i + 1
    return None


def only_line(lines, pat, what):
    hits = [i + 1 for i, l in enumerate(lines) if re.search(pat, l)]
    if len(hits) != 1:
        raise BuildError(f"{what}: expected one line matching {pat!r}, found {hits}")
    return hits[0]


class Game:
    def __init__(self, root):
        self.root = root
        self.res = X.Resolver(root)
        self._lines = {}

    def lines(self, rel):
        if rel not in self._lines:
            self._lines[rel] = open(os.path.join(self.root, SRC, rel), encoding="utf-8").read().split("\n")
        return self._lines[rel]

    def mod(self, rel):
        return self.res.module(os.path.join(SRC, rel))

    def const_array(self, mod, name):
        m2, k = self.res.lookup(mod, name)
        if not m2:
            raise BuildError(f"{name} not found from {mod.rel}")
        vals = self.res.string_array(m2, X.collapse(m2.text(k)))
        if vals is None:
            raise BuildError(f"{name} is not a string array")
        return vals

    def definition_line(self, rel, name):
        pat = (r"^(?:export\s+)?(?:const|let|function|async function)\s+" + re.escape(name) + r"\b")
        return line_of(self.lines(rel), pat)

    # ---- EFFECT_SORT_RANK ----------------------------------------------------------
    def sort_ranks(self):
        """{tag: {rank, line, via}} read from the EFFECT_SORT_RANK Map literal only."""
        mod = self.mod("libs/combat/util.ts")
        if "EFFECT_SORT_RANK" not in mod.decls:
            raise BuildError("EFFECT_SORT_RANK not found in util.ts")
        a, b, _ = mod.decls["EFFECT_SORT_RANK"]
        s = mod.src
        arr = s.index("[", a)
        if arr >= b:
            raise BuildError("EFFECT_SORT_RANK has no array literal")
        ranks = {}
        idx = 0
        for p, q in X.split_top(s, arr + 1, X.match_close(s, arr)):
            ent = s[p:q]
            line = mod.line(p)
            if ent.startswith("..."):
                name = re.match(r"\.\.\.\(?\s*([A-Za-z_$][\w$]*)", ent).group(1)
                m2, k = self.res.lookup(mod, name)
                if not m2:
                    raise BuildError(f"EFFECT_SORT_RANK spread {name} not resolved")
                da, db, _ = m2.decls[k]
                s2 = m2.src
                arr2 = s2.index("[", da)
                for p2, q2 in X.split_top(s2, arr2 + 1, X.match_close(s2, arr2)):
                    tag = X.string_value(s2[p2:q2])
                    if tag is None:
                        raise BuildError(f"{name}: non-literal entry")
                    ranks[tag] = {"rank": idx, "line": line,
                                  "via": (name, os.path.relpath(m2.rel, SRC), m2.line(p2))}
                    idx += 1
                continue
            tag = X.string_value(ent)
            if tag is None:
                raise BuildError(f"EFFECT_SORT_RANK: non-literal entry {ent!r}")
            ranks[tag] = {"rank": idx, "line": line, "via": None}  # Map: a later duplicate wins
            idx += 1
        fallback = only_line(self.lines("libs/combat/util.ts"),
                             r"EFFECT_SORT_RANK\.get\(a\.type\) \?\? Number\.POSITIVE_INFINITY",
                             "unranked fallback")
        return ranks, fallback

    # ---- applyEffects dispatch passes ---------------------------------------------
    def dispatch(self):
        """{tag: [(pass name, line)]} for the applyEffects passes in process.ts."""
        rel = "libs/combat/process.ts"
        L = self.lines(rel)
        txt = "\n".join(L)
        start = only_line(L, r"^export const applyEffects = \(", "applyEffects")

        def at(pat, what):
            hits = [i + 1 for i, l in enumerate(L) if i + 1 > start and re.search(pat, l)]
            if not hits:
                raise BuildError(f"process.ts {what}: anchor {pat!r} not found after applyEffects")
            return hits[0]

        # The filters these passes use; if any of them changes, stop rather than cite a stale pass.
        need = [
            r'usersEffects\.filter\(\(e\) => e\.type === "mirror" \|\| e\.type === "copy"\)\.forEach\(resolve\)',
            r'\.filter\(\(e\) => !damageModifierTypes\.includes\(e\.type\)\)',
            r'\.filter\(\(e\) => !POST_DAMAGE_MODIFIER_TYPES\.includes\(e\.type\)\)',
            r'\.filter\(\(e\) => e\.type !== "pierce"\)',
            r'\.filter\(\(e\) => e\.type !== "increaseheal" && e\.type !== "decreaseheal"\)',
            r'POST_DAMAGE_MODIFIER_TYPES\.includes\(e\.type\) &&\s*e\.type !== "consume" &&\s*e\.type !== "siphon"',
        ]
        for pat in need:
            if not re.search(pat, txt):
                raise BuildError(f"process.ts pass filter changed: {pat!r}")
        mod = self.mod(rel)
        dmg_mod = self.const_array(mod, "damageModifierTypes")
        post_dmg = self.const_array(mod, "POST_DAMAGE_MODIFIER_TYPES")

        P = {
            "copymirror": ("applyEffects copy and mirror pass, after ground effects and before the main pass",
                           at(r'e\.type === "mirror" \|\| e\.type === "copy"\)\.forEach\(resolve\)', "copy/mirror")),
            "main": ("applyEffects main pass (nonDamageModifierEffects, sorted by sortEffects)",
                     at(r"nonDamageModifierEffects\.sort\(sortEffects\)\.forEach\(resolve\)", "main")),
            "convert": ("applyEffects Consume/Siphon registration, after the main pass and before damage",
                        at(r'\(e\.type === "consume" \|\| e\.type === "siphon"\) &&', "conversion")),
            "pipeline": ("applyEffects damage modifier pipeline",
                         at(r"applyDamageModifierPipelineToConsequences\(\{", "pipeline")),
            "pierce": ("applyEffects pierce pass, after the damage pipeline",
                       at(r"pierceEffects\.sort\(sortEffects\)\.forEach\(resolve\)", "pierce")),
            "parry": ("applyEffects Parry split, before the other post-damage readers",
                      at(r'\.filter\(\(e\) => e\.type === "parry"\)', "parry")),
            "post": ("applyEffects post-damage pass, after pierce",
                     at(r"postDamageModifierEffects\.sort\(sortEffects\)\.forEach\(\(effect\) => \{", "post")),
            "absorb_late": ("applyEffects deferred Absorb when Parry returned damage or the target has Diffuse",
                            at(r'^\s+e\.type === "absorb" &&$', "deferred absorb")),
            "repay": ("applyEffects Diffuse debt repayment, before the damage pipeline",
                      at(r"^\s+repayDiffuseDamage\($", "diffuse repay")),
            "defer": ("applyEffects Diffuse deferral, after the post-damage readers",
                      at(r"^\s+applyDiffuseToConsequences\(\{$", "diffuse defer")),
            "healadj": ("applyEffects heal adjustment pass, after the post-damage readers",
                        at(r"healAdjustmentEffects\.sort\(sortEffects\)\.forEach\(resolve\)", "heal adjust")),
        }

        def passes(tag):
            if tag in ("mirror", "copy"):
                out = ["copymirror"]
            elif tag in dmg_mod:
                out = ["pipeline"]
            elif tag in ("consume", "siphon"):
                out = ["convert"]
            elif tag == "pierce":
                out = ["pierce"]
            elif tag == "parry":
                out = ["parry"]
            elif tag in post_dmg:
                out = ["post"] + (["absorb_late"] if tag == "absorb" else [])
            elif tag in ("increaseheal", "decreaseheal"):
                out = ["healadj"]
            else:
                out = ["main"] + (["repay", "defer"] if tag == "diffuse" else [])
            return [P[k] for k in out]

        return passes


def build(game_root, data, resolved, out_dir, interactions=None):
    g = Game(game_root)
    tg = g.lines("libs/combat/tags.ts")
    pr = g.lines("libs/combat/process.ts")
    ranks, unranked_line = g.sort_ranks()
    passes = g.dispatch()
    rtags = resolved["tags"]
    commit = resolved.get("game_repo_head") or "unknown"
    warnings = []
    if interactions is not None:
        edges = [{"s": e["from"], "t": e["to"], "k": e["kind"]} for e in interactions["edges"]]
    else:
        edges = data["edges"]

    def extra(spec):
        m = re.match(r"(libs/[\w/]+\.ts) ([A-Za-z_$][\w$]*)(.*)$", spec)
        if not m:
            return spec
        rel, name, rest = m.groups()
        ln = g.definition_line(rel, name)
        if ln is None:
            warnings.append(f"EXTRA_SRC {spec!r}: {name} is not defined in {rel}")
            return spec
        note = re.fullmatch(r"\s*\((.*)\)\s*", rest)
        if note:
            return f"{rel} {name} (line {ln}; {note.group(1)})"
        return f"{rel} {name} (line {ln}){rest}"

    os.makedirs(os.path.join(out_dir, "tags"), exist_ok=True)
    bundle = {}
    for n in data["nodes"]:
        t = n["id"]
        if t not in rtags:
            raise BuildError(f"{t}: not in the resolved schemas")
        r = rtags[t]
        if r["schema"] != n["schema"]:
            warnings.append(f"{t}: data.json schema {n['schema']} != source {r['schema']}")
        L, D = [], {}

        def put(key, value, text=None, comment=None):
            D[key] = value
            line = f"{key}: {text if text is not None else yq(value)}"
            L.append(line + (f"   # {comment}" if comment else ""))

        put("tag", t)
        put("schema", f"validators/combat.ts {r['schema']} (line {r['line']})")
        put("exclusion_area", EX_AREA[n["area"]])
        put("in_game_text", n["desc"])
        put("behavior", CUR.BEHAVIOR.get(t, n["beh"]))
        put("polarity", n["pol"], text=n["pol"], comment=POLARITY_NOTE)
        if n["pb"]:
            put("prevented_by", list(n["pb"]), text=f"[{', '.join(n['pb'])}]")
            put("prevent_check", CUR.PREVENT_CHECK.get(t, CUR.PREVENT_CHECK_DEFAULT))
        else:
            put("prevented_by", [], text="[]", comment="no prevent check in its handler")
        for key, src in (("copy_can_take", "copy"), ("mirror_can_pass", "mirror"),
                         ("potency_eligible", "potency"), ("immunity_can_cancel", "prevtype")):
            put(key, bool(n[src]), text=str(bool(n[src])).lower())
        stage = CUR.STAGE.get(t) or STAGE_TXT.get(n["stage"])
        if not stage:
            raise BuildError(f"{t}: no stage in curation.STAGE")
        put("stage", stage)
        live = CUR.LIVE.get(t, LIVE.get(t))
        if live:
            put("live_from", live)
        if t in TICK or t in CUR.APPLIES:
            ap = CUR.APPLIES.get(t, "on landing, then once a round when the holder acts")
            put("applies", ap, text=yq(ap))
        calc = r["calculation"]
        if not calc:
            raise BuildError(f"{t}: calculation not resolved")
        put("calculation", list(calc), text=f"[{', '.join(calc)}]",
            comment=f"default {r['calculation_default']}" if r.get("calculation_default") else None)
        if r.get("helper") == "simpleTag":
            put("fields_note", "simpleTag (BaseAttributes + PowerAttributes only)")
        own = {k: f for k, f in r["fields"].items()
               if k not in ("type", "description") and f["from"] not in BASE_GROUPS}
        if own:
            D["own_fields"] = {}
            L.append(f"own_fields:   # {FIELDS_NOTE}")
            for k, f in own.items():
                D["own_fields"][k] = f["expr"]
                note = None
                if f["from"] != r["schema"]:
                    via = [v for v in f["via"] if v != f["from"]]
                    note = f"from {f['from']}" + (f" via {' > '.join(via)}" if via else "")
                L.append(f"  {k}: {yq(f['expr'])}" + (f"   # {note}" if note else ""))
        D["live_usage_2026_11_21"] = {"jutsu": n["use"], "pvp_legal": n["pvp"]}
        L.append(f"live_usage_2026_11_21: {{jutsu: {n['use']}, pvp_legal: {n['pvp']}}}")

        srcs = []
        h = HANDLER.get(t)
        if h:
            ln = line_of(tg, r"^export const " + h + r"\s*=") or line_of(tg, r"^const " + h + r"\s*=")
            if ln is None:
                warnings.append(f"{t}: handler {h} not found in tags.ts")
            srcs.append(f"libs/combat/tags.ts {h} (line {ln})")
        dl = line_of(pr, r'effect\.type === "' + t + r'"')
        if dl:
            srcs.append(f"libs/combat/process.ts first reference (line {dl})")
        combat = n["area"] != "noncombat"
        # elementaldamage never reaches applyEffects: resolveElementalDamage turns it into damage at cast.
        rt = RUNTIME_AS.get(t, t)
        as_note = f", as {rt}" if rt != t else ""
        if combat:
            for name, ln in passes(rt):
                srcs.append(f"libs/combat/process.ts {name}{as_note} (line {ln})")
        rk = ranks.get(rt)
        if rk and rk["via"]:
            name, rel, ln2 = rk["via"]
            srcs.append(f"libs/combat/util.ts EFFECT_SORT_RANK rank {rk['rank']} (line {rk['line']}, "
                        f"...{name} entry at {rel} line {ln2})")
        elif rk:
            srcs.append(f"libs/combat/util.ts EFFECT_SORT_RANK rank {rk['rank']}{as_note} (line {rk['line']})")
        elif combat:
            srcs.append(f"libs/combat/util.ts EFFECT_SORT_RANK: no explicit rank, sorts last "
                        f"(line {unranked_line})")
        srcs += [extra(s_) for s_ in EXTRA_SRC.get(t, [])]
        if srcs:
            D["source"] = srcs
            L.append(f"source:   # game repo studie-tech/TheNinjaRPG @ {commit}, paths under app/src")
            for s_ in srcs:
                L.append(f"  - {yq(s_)}")

        outs = [e for e in edges if e["s"] == t]
        ins = [e for e in edges if e["t"] == t]
        if outs or ins:
            D["interactions"] = {}
            L.append("interactions:   # full list with notes in ../interactions.json")
            for label, group, other in (("outgoing", outs, "t"), ("incoming", ins, "s")):
                if not group:
                    continue
                D["interactions"][label] = {}
                L.append(f"  {label}:")
                for kk in sorted(set(e["k"] for e in group)):
                    names = [e[other] for e in group if e["k"] == kk]
                    D["interactions"][label][kk] = names
                    L.append(f"    {kk}: [{', '.join(names)}]")
        with open(os.path.join(out_dir, "tags", f"{t}.yaml"), "w") as fh:
            fh.write("\n".join(L) + "\n")
        bundle[t] = D
    with open(os.path.join(out_dir, "tags.json"), "w") as fh:
        json.dump({"pinned_game_commit": commit, "tags": dict(sorted(bundle.items()))}, fh, indent=1,
                  ensure_ascii=False)
        fh.write("\n")
    return bundle, warnings


def main():
    ap = argparse.ArgumentParser(description=__doc__.strip().split("\n\n")[0])
    ap.add_argument("game_root")
    ap.add_argument("data_json")
    ap.add_argument("out_dir")
    ap.add_argument("--extract", help="extract.py output; omitted: run the extractor in-process")
    ap.add_argument("--interactions", help="interactions.json to read links from (default: data.json edges)")
    a = ap.parse_args()
    data = json.load(open(a.data_json))
    if a.extract:
        resolved = json.load(open(a.extract))
    else:
        resolved = X.extract(a.game_root)
    if resolved.get("unresolved"):
        print("extract.py left expressions unresolved:", *resolved["unresolved"], sep="\n  ", file=sys.stderr)
        return 1
    try:
        inter = json.load(open(a.interactions)) if a.interactions else None
        bundle, warnings = build(a.game_root, data, resolved, a.out_dir, inter)
    except BuildError as e:
        print(f"kb.py: {e}", file=sys.stderr)
        return 1
    for w in warnings:
        print("WARNING:", w, file=sys.stderr)
    print(f"{len(bundle)} tag files -> {os.path.join(a.out_dir, 'tags')}; tags.json written")
    return 0


if __name__ == "__main__":
    sys.exit(main())
