#!/usr/bin/env python3
"""Offline QA checks over saved TNR content records.

Reads a folder (or several) of saved read responses and runs mechanical checks:
broken references, visible-depends-on-hidden, placeholder and duplicate text,
self-contradicting effects, write-bound violations, quest flow and placement,
reward and cost outliers, AI loadout/rule problems and image load results.

It never talks to the game. Fetching is a separate step; this tool only reads files.

Accepted inputs (any mix, found recursively under each path):
  * one-call envelopes: {"proc": "jutsu.getAll", "input": {...}, "at": ISO, "data": <decoded>}
  * builder results bundles / harvest captures: {"captures": [{"proc", "input", "at", "data"}]}
    (the same shape skills/building-tnr-content/scripts/harvest.py reads)
  * an image check map, given with --images: {"<url>": {"status": 200, ...}}

Procedures understood: <entity>.getAll (paged {data:[...]}), <entity>.get, <entity>.getAllNames,
profile.getAllAiNames, profile.getAi, ai.getAiProfile, for entity in jutsu, item, quests,
gameAsset, bloodline. The newest capture of a record wins.

Usage
  python3 scripts/qa_live.py check DIR [DIR ...] [--captures harvests/inbox] [--images img.json]
                             [--contracts .] [--json out.json] [--md out.md]
  python3 scripts/qa_live.py --selftest

Severity (fixed vocabulary, used by the report):
  S1 Breaks play | S2 Balance outliers | S3 Content defects | S4 Low-quality content | S5 Polish
Certainty: "verified" means the record shows the defect directly; "needs check" means the
mechanical signal is real but its in-game consequence has not been proven.

Balance and reward findings are SIGNALS for a human ruling (CLAUDE.md section 10), never a
decision. Outliers use the modified z-score of Iglewicz and Hoaglin over the stated peer group:
M = 0.6745 * (x - median) / MAD, flagged when |M| > 3.5 and the group has at least 8 members;
when MAD is 0 the mean absolute deviation stands in (M = (x - median) / (1.253314 * meanAD)).
"""
from __future__ import annotations

import argparse
import json
import math
import os
import re
import statistics
import sys
import tempfile
import unicodedata
from collections import Counter, defaultdict

SEVERITY = {
    "S1": "Breaks play",
    "S2": "Balance outliers",
    "S3": "Content defects",
    "S4": "Low-quality content",
    "S5": "Polish",
}
ENTITY_OF_PROC = {"jutsu": "jutsu", "item": "item", "quests": "quest", "gameAsset": "asset", "bloodline": "bloodline"}

# ------------------------------------------------------------------ loading


class DB:
    def __init__(self):
        self.rec = {e: {} for e in ("jutsu", "item", "quest", "asset", "bloodline", "ai", "aiprofile")}
        self.at = {}  # (entity, id) -> capture timestamp
        self.names = {}  # entity -> {id: row}
        self.names_at = {}
        self.sources = Counter()
        self.images = {}
        self.contracts = {}
        self.legacy_fx = Counter()
        self.pruned = {}

    def put(self, ent, rid, row, at):
        if not rid:
            return
        key = (ent, rid)
        if key in self.at and (self.at[key] or "") > (at or ""):
            return
        self.rec[ent][rid] = row
        self.at[key] = at


def _captures(doc):
    if isinstance(doc, dict) and "proc" in doc and "data" in doc and "captures" not in doc:
        yield doc
    elif isinstance(doc, dict) and isinstance(doc.get("captures"), list):
        for c in doc["captures"]:
            if isinstance(c, dict) and "proc" in c:
                if c.get("data") is None and isinstance(c.get("rows"), list):
                    c = dict(c, data=c["rows"])
                yield c


def ingest(db, doc, label=""):
    for c in _captures(doc):
        proc, data, at = c.get("proc"), c.get("data"), c.get("at")
        if data is None or c.get("ok") is False:
            continue
        db.sources[proc] += 1
        root, _, op = proc.partition(".")
        if proc == "profile.getAi" and isinstance(data, dict):
            db.put("ai", data.get("userId"), slim_ai(data), at)
        elif proc == "ai.getAiProfile" and isinstance(data, dict):
            db.put("aiprofile", data.get("id"), data, at)
        elif proc == "profile.getAllAiNames" and isinstance(data, list):
            if (at or "") >= (db.names_at.get("ai") or ""):
                db.names["ai"] = {r.get("userId"): r for r in data}
                db.names_at["ai"] = at
        elif root in ENTITY_OF_PROC:
            ent = ENTITY_OF_PROC[root]
            if op == "getAll" and isinstance(data, dict) and isinstance(data.get("data"), list):
                for r in data["data"]:
                    db.put(ent, r.get("id"), r, at)
            elif op == "get" and isinstance(data, dict):
                db.put(ent, data.get("id"), data, at)
            elif op == "getAllNames" and isinstance(data, list):
                if (at or "") >= (db.names_at.get(ent) or ""):
                    db.names[ent] = {r.get("id"): r for r in data}
                    db.names_at[ent] = at


AI_KEEP = ("userId", "username", "level", "rank", "aiProfileId", "isSummon", "inArena", "isAi", "avatar",
           "statsMultiplier", "poolsMultiplier", "maxHealth", "maxChakra", "maxStamina", "strength", "speed",
           "intelligence", "willpower", "ninjutsuOffence", "ninjutsuDefence", "genjutsuOffence", "genjutsuDefence",
           "taijutsuOffence", "taijutsuDefence", "bukijutsuOffence", "bukijutsuDefence", "regeneration",
           "preferredStat", "preferredGeneral1", "preferredGeneral2", "bloodlineId")


def slim_ai(a):
    """Keep only content fields; player-account fields (ip, bank, ...) never leave this function."""
    out = {k: a.get(k) for k in AI_KEEP if k in a}
    out["jutsus"] = [{"jutsuId": j.get("jutsuId"), "equipped": j.get("equipped"), "level": j.get("level"),
                      "createdAt": j.get("createdAt"), "updatedAt": j.get("updatedAt"),
                      "range": (j.get("jutsu") or {}).get("range"), "name": (j.get("jutsu") or {}).get("name")}
                     for j in a.get("jutsus") or []]
    out["items"] = [{"itemId": i.get("itemId"), "equipped": i.get("equipped"), "quantity": i.get("quantity"),
                     "dropChancePerc": i.get("dropChancePerc")} for i in a.get("items") or []]
    return out


def load_paths(db, paths):
    for p in paths:
        files = [p] if os.path.isfile(p) else [os.path.join(dp, f) for dp, _, fs in os.walk(p) for f in fs]
        for f in sorted(files):
            if not f.endswith(".json"):
                continue
            try:
                with open(f, encoding="utf-8") as fh:
                    ingest(db, json.load(fh), f)
            except (OSError, ValueError):
                continue


def prune_to_live(db):
    """Drop captured records whose id is absent from a newer live name list (deleted since capture)."""
    pruned = {}
    for ent in ("jutsu", "item", "quest", "asset", "bloodline", "ai"):
        live = db.names.get(ent)
        if live is None:
            continue
        gone = [k for k in db.rec[ent] if k not in live and (db.at.get((ent, k)) or "") < (db.names_at.get(ent) or "~")]
        for k in gone:
            del db.rec[ent][k]
        pruned[ent] = len(gone)
    db.pruned = pruned
    return pruned


def load_contracts(db, root):
    def rd(*names):
        for n in names:
            for base in (root, os.path.join(root, "skills/building-tnr-content/data")):
                fp = os.path.join(base, n)
                if os.path.exists(fp):
                    with open(fp, encoding="utf-8") as fh:
                        return json.load(fh)
        return {}
    db.contracts = {"45g": rd("45g_DATA_checks.json"), "45c": rd("45c_DATA_constructors.json"),
                    "45d": rd("45d_DATA_entity_schemas.json"), "45e": rd("45e_DATA_constants.json")}


# ------------------------------------------------------------------ helpers

URL_RE = re.compile(r"^https?://", re.I)
PLACEHOLDER_RE = re.compile(r"\b(placeholder|todo|tbd|fixme|lorem ipsum|new (jutsu|item|quest|bloodline) description|description here|"
                            r"insert (text|description)|xxx+)\b", re.I)
INTERNAL_RE = re.compile(r"(pending sign-?off|balance values pending|shared pool record|do not publish|"
                         r"\bwip\b|not final|temp(orary)? (text|name|description))", re.I)
TESTNAME_RE = re.compile(r"\b(probe|readback|smoke ?test|test(ing)?( ?\d+)?|copy of|untitled)\b", re.I)
MISSPELL = {
    "teh": "the", "recieve": "receive", "recieves": "receives", "seperate": "separate", "definately": "definitely",
    "occured": "occurred", "untill": "until", "wich": "which", "thier": "their", "becuase": "because",
    "beacuse": "because", "acheive": "achieve", "agressive": "aggressive", "apparant": "apparent",
    "begining": "beginning", "beleive": "believe", "calender": "calendar", "commited": "committed",
    "concious": "conscious", "embarass": "embarrass", "enviroment": "environment", "existance": "existence",
    "foriegn": "foreign", "goverment": "government", "independant": "independent", "occassion": "occasion",
    "persue": "pursue", "posession": "possession", "prefered": "preferred", "realy": "really",
    "relevent": "relevant", "succesful": "successful", "succesfully": "successfully", "suprise": "surprise",
    "tommorow": "tomorrow", "truely": "truly", "wierd": "weird", "withold": "withhold", "dammage": "damage",
    "damge": "damage", "abilty": "ability", "oppenent": "opponent", "opponant": "opponent", "enemey": "enemy",
    "stregth": "strength", "strenght": "strength", "lenght": "length", "chakara": "chakra", "techinque": "technique",
    "tecnique": "technique", "attak": "attack", "attacs": "attacks", "powerfull": "powerful", "speacial": "special",
    "defence's": "defence", "it's own": "its own", "loose control": "lose control", "alot": "a lot",
    "ofthe": "of the", "inthe": "in the", "tothe": "to the", "andthe": "and the", "recieved": "received",
    "neccessary": "necessary", "necesary": "necessary", "accross": "across", "arguement": "argument",
    "wont": "won't", "dont": "don't", "doesnt": "doesn't", "cant": "can't", "isnt": "isn't", "youre": "you're",
    "shinobis": "shinobi", "sheild": "shield", "feild": "field", "peice": "piece", "freind": "friend",
}
AN_EXCEPT = {"herb", "heir", "honest", "honor", "honour", "hour", "hourly", "x", "s", "f", "l", "m", "n", "r"}
A_EXCEPT = {"one", "once", "united", "unique", "universal", "unit", "unicorn", "union", "uniform", "usual",
            "use", "used", "user", "euro", "european", "ewe", "utility", "ufo", "unified", "urn"}
POWER_TYPES = {"damage", "pierce", "heal", "absorb", "shield", "reflect", "lifesteal", "vamp", "drain", "poison",
               "recoil", "afterburn", "wound", "barrier", "elementaldamage", "stun", "consume"}
INSTANT_TYPES = {"damage", "pierce", "heal", "visual", "move", "flee", "cleanse", "clear", "summon", "onehitkill",
                 "injectjutsus", "noncombatconsumereward", "copy", "mirror", "repair", "rollbloodline",
                 "removebloodline", "rollsagemode", "noncombatgainskill", "noncombatquest", "unlockitemvariant",
                 "marriageslotincrease", "noncombatincreasereskins", "finalstand"}
HARM_TYPES = {"damage", "pierce", "poison", "stun", "wound", "drain", "decreasestat", "decreasedamagegiven",
              "increasedamagetaken", "healprevent", "moveprevent", "seal", "elementalseal", "disarm", "onehitkill"}
HARD_HARM = {"damage", "pierce", "poison", "stun", "wound", "drain", "onehitkill"}
BUFF_TYPES = {"heal", "shield", "absorb", "increasedamagegiven", "decreasedamagetaken", "increasestat",
              "increaseregeneration", "lifesteal", "reflect", "barrier", "cleanse", "debuffprevent", "stunprevent",
              "onehitkillprevent", "immunity"}
ANIM_FIELDS = ("appearAnimation", "staticAnimation", "disappearAnimation")
SFX_FIELDS = ("appearSfx", "disappearSfx")


def norm_name(s):
    s = unicodedata.normalize("NFKC", s or "")
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"[\s\-_]+", " ", s).strip().casefold()
    return re.sub(r"[^\w ]", "", s)


def strip_html(s):
    return re.sub(r"<[^>]+>", " ", s or "")


def mod_z(values):
    """Modified z-score per value (Iglewicz-Hoaglin). Returns list aligned with values (None if undefined)."""
    if len(values) < 8:
        return [None] * len(values)
    med = statistics.median(values)
    mad = statistics.median([abs(v - med) for v in values])
    if mad:
        return [0.6745 * (v - med) / mad for v in values]
    mean_ad = sum(abs(v - med) for v in values) / len(values)
    if not mean_ad:
        return [None] * len(values)
    return [(v - med) / (1.253314 * mean_ad) for v in values]


def is_hidden(rec):
    return bool(rec.get("hidden"))


class Findings:
    def __init__(self):
        self.items = []
        self._seen = set()

    def add(self, code, sev, ent, rec_id, name, msg, evidence, fix, certainty="verified", hidden=None, group=None):
        key = (code, rec_id, msg)
        if key in self._seen:
            return
        self._seen.add(key)
        self.items.append({"code": code, "severity": sev, "entity": ent, "id": rec_id, "name": name,
                           "hidden": hidden, "message": msg, "evidence": evidence, "fix": fix,
                           "certainty": certainty, "group": group})


def outliers(F, code, ent, rows, metric_name, fix, sev="S2", min_group=8, group_label=""):
    """rows: list of (rec, value). Flags |M| > 3.5."""
    vals = [v for _, v in rows]
    if len(vals) < min_group:
        return
    med = statistics.median(vals)
    for (rec, v), m in zip(rows, mod_z(vals)):
        if m is not None and abs(m) > 3.5:
            F.add(code, sev, ent, rec.get("id") or rec.get("userId"), rec.get("name") or rec.get("username"),
                  f"{metric_name} {v:g} vs peer median {med:g} ({group_label}, n={len(vals)}, M={m:+.1f})",
                  {"metric": metric_name, "value": v, "median": med, "n": len(vals), "M": round(m, 2),
                   "group": group_label}, fix, "needs check", is_hidden(rec), group=group_label)


def image_status(db, url):
    if not url:
        return "empty"
    r = db.images.get(url)
    if r is None:
        return "unchecked"
    if r.get("skipped"):
        return "unchecked"
    st = r.get("status")
    if st in (200, 206):
        ct = (r.get("ctype") or "").lower()
        if ct and not (ct.startswith("image/") or ct.startswith("video/") or ct.startswith("audio/")
                       or "octet-stream" in ct):
            return f"not-an-image ({ct})"
        return "ok"
    return f"fail ({st if st is not None else r.get('err', 'error')})"


# ------------------------------------------------------------------ text checks


def text_checks(F, ent, rec, fields, check_name=True):
    rid, name, hid = rec.get("id"), rec.get("name"), is_hidden(rec)
    nm = rec.get("name") or ""
    if check_name and (nm != nm.strip() or "  " in nm):
        F.add("TXT-NAME-SPACE", "S5", ent, rid, name, "name has leading/trailing or doubled whitespace",
              {"name": repr(nm)}, "Trim and collapse whitespace in the name.", hidden=hid)
    m = TESTNAME_RE.search(nm) if check_name else None
    if m:
        F.add("TXT-TEST-NAME", "S4", ent, rid, name, f"name looks like a test/probe record ('{m.group(0)}')",
              {"name": nm}, "Retire the test record, or rename it if it is real content.", "needs check", hidden=hid)
    for f in fields:
        val = rec.get(f)
        if f in ("description", "battleDescription") and (val is None or not strip_html(val).strip()):
            note = " (DB NOT NULL: the next editor save 500s, item.md gotcha 2)" if (ent == "item" and
                                                                                   f == "battleDescription") else ""
            F.add("TXT-EMPTY", "S3", ent, rid, name, f"{f} is empty" + note, {"field": f}, f"Write a real {f}.",
                  hidden=hid)
            continue
        if not isinstance(val, str):
            continue
        txt = strip_html(val)
        bare = txt.strip()
        if f == "description" and check_name and not hid and (0 < len(bare) < 12 or bare.lower() == nm.strip().lower()):
            F.add("TXT-SHORT", "S4", ent, rid, name, f"description is a stub: '{bare}'", {"field": f},
                  "Write a real description.", hidden=hid)
        m = PLACEHOLDER_RE.search(txt)
        if m:
            F.add("TXT-PLACEHOLDER", "S4", ent, rid, name, f"{f} contains placeholder text '{m.group(0)}'",
                  {"field": f, "excerpt": txt.strip()[:160]}, f"Replace the placeholder {f}.", hidden=hid)
        m = INTERNAL_RE.search(txt)
        if m:
            F.add("TXT-INTERNAL-NOTE", "S4", ent, rid, name, f"{f} carries an internal build note '{m.group(0)}'",
                  {"field": f, "excerpt": txt.strip()[:160]}, f"Replace the build note in {f} with player text.",
                  hidden=hid)
        for w in re.findall(r"[A-Za-z']+", txt):
            lw = w.lower()
            if lw in MISSPELL and lw not in ("wont", "cant", "dont", "doesnt", "isnt", "youre"):
                F.add("TXT-TYPO", "S5", ent, rid, name, f"{f}: '{w}' -> '{MISSPELL[lw]}'",
                      {"field": f, "word": w, "excerpt": _ctx(txt, w)}, "Fix the spelling.", hidden=hid)
        for m in re.finditer(r"\b(an)\s+([b-df-hj-np-tv-z][a-z]+)", txt, re.I):
            if m.group(2).lower() not in AN_EXCEPT and not m.group(2).isupper():
                F.add("TXT-ARTICLE", "S5", ent, rid, name, f"{f}: '{m.group(0)}' should use 'a'",
                      {"field": f, "excerpt": _ctx(txt, m.group(0))}, "Fix the article.", hidden=hid)
        for m in re.finditer(r"\b(a)\s+([aeio][a-z]+)", txt):
            if m.group(2).lower() not in A_EXCEPT:
                F.add("TXT-ARTICLE", "S5", ent, rid, name, f"{f}: '{m.group(0)}' should use 'an'",
                      {"field": f, "excerpt": _ctx(txt, m.group(0))}, "Fix the article.", hidden=hid)
        for m in re.finditer(r"\b([A-Za-z]{2,})\s+\1\b", txt, re.I):
            if m.group(1).lower() not in ("ha", "no", "hey", "so", "very", "bye", "go", "la", "na", "ho", "had"):
                F.add("TXT-REPEAT", "S5", ent, rid, name, f"{f}: repeated word '{m.group(0)}'",
                      {"field": f, "excerpt": _ctx(txt, m.group(0))}, "Remove the repeated word.", hidden=hid)


def _ctx(txt, w):
    i = txt.find(w)
    return txt[max(0, i - 50): i + len(w) + 50].strip() if i >= 0 else ""


def dup_names(F, ent, recs, key="name"):
    groups = defaultdict(list)
    for r in recs:
        groups[norm_name(r.get(key))].append(r)
    for k, rs in groups.items():
        if len(rs) > 1 and k:
            exact = len({r.get(key) for r in rs}) == 1
            vis = [r for r in rs if not is_hidden(r)]
            sev = "S3" if len(vis) > 1 else "S5"
            F.add("NAME-DUP" if exact else "NAME-NEAR-DUP", sev, ent, rs[0].get("id") or rs[0].get("userId"),
                  rs[0].get(key),
                  ("identical" if exact else "near-identical") + f" names on {len(rs)} records ({len(vis)} visible)",
                  {"records": [{"id": r.get("id") or r.get("userId"), "name": r.get(key), "hidden": r.get("hidden")}
                               for r in rs]},
                  "Rename or retire the duplicate so players and staff can tell them apart.",
                  hidden=not vis)


def bounds_checks(F, db, ent, schema_ent, rec):
    fields = ((db.contracts.get("45d") or {}).get("entities", {}).get(schema_ent) or {}).get("fields", {})
    for f, spec in fields.items():
        v = rec.get(f)
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            continue
        lo, hi = spec.get("min"), spec.get("max")
        if isinstance(lo, (int, float)) and v < lo or isinstance(hi, (int, float)) and v > hi:
            F.add("BOUNDS", "S3", ent, rec.get("id"), rec.get("name"),
                  f"{f}={v:g} is outside the write validator bounds [{lo}, {hi}]",
                  {"field": f, "value": v, "min": lo, "max": hi, "raw": spec.get("raw")},
                  "Bring the value inside bounds; until then any editor save of this record will be rejected.",
                  hidden=is_hidden(rec))


# ------------------------------------------------------------------ effect checks


def effect_checks(F, db, ent, rec, effects, owner_target=None, entity_kind="jutsu", reach=None):
    g = db.contracts.get("45g") or {}
    tag_max = (g.get("tag_power_max") or {}).get("fields", {})
    runtime_only = set((g.get("runtime_only_tags") or {}).get("values", []))
    companion = (g.get("companion_required") or {}).get("values", {})
    ent_only = (g.get("entity_only_tags") or {}).get("values", {})
    formula = set((g.get("formula_tags") or {}).get("values", ["damage", "pierce", "wound"]))
    rid, name, hid = rec.get("id"), rec.get("name"), is_hidden(rec)
    types = [e.get("type") for e in effects if isinstance(e, dict)]
    assets = db.rec["asset"]
    for i, e in enumerate(effects or []):
        if not isinstance(e, dict):
            continue
        t = e.get("type")
        where = f"effects[{i}] {t}"
        if t in formula and e.get("calculation") == "formula":
            missing = [k for k in ("statTypes", "generalTypes") if not e.get(k)]
            if missing:
                live = reach if reach is not None else not hid
                F.add("FX-FORMULA-TYPES", "S1" if live else "S5", ent, rid, name,
                      f"{where}: formula effect without {', '.join(missing)}",
                      {"effect": i, "missing": missing, "reachable": live}, "Set statTypes and generalTypes "
                      "(default ['Highest']); law 4 says an empty list detonates the damage formula.",
                      "needs check", hidden=hid)
        p = e.get("power")
        if t in tag_max and isinstance(p, (int, float)) and p > tag_max[t]:
            F.add("FX-POWER-CAP", "S3", ent, rid, name, f"{where}: power {p:g} above the tag cap {tag_max[t]}",
                  {"effect": i, "power": p, "cap": tag_max[t]}, "Lower to the cap or split into rows (law 6).",
                  hidden=hid)
        if t in POWER_TYPES and isinstance(p, (int, float)) and p == 0 and not e.get("powerPerLevel"):
            F.add("FX-ZERO-POWER", "S3", ent, rid, name, f"{where}: power 0 with no per-level growth",
                  {"effect": i}, "Give the effect a power or remove it.", hidden=hid)
        r = e.get("rounds")
        if t not in INSTANT_TYPES and r == 0 and t not in ("stun", "seal", "elementalseal"):
            F.add("FX-ZERO-ROUNDS", "S3", ent, rid, name, f"{where}: duration effect with rounds 0",
                  {"effect": i}, "Set rounds >= 1; effects do not apply on the cast round (law 75), so a 0-round "
                  "effect may never apply.", "needs check", hidden=hid)
        if t in runtime_only:
            F.add("FX-RUNTIME-ONLY", "S3", ent, rid, name, f"{where}: runtime-only tag on an authored record",
                  {"effect": i}, "Remove the tag (law 77).", hidden=hid)
        if t in companion and not (set(companion[t]) & set(types)):
            F.add("FX-COMPANION", "S3", ent, rid, name, f"{where}: needs a {'/'.join(companion[t])} effect on the "
                  "same action", {"effect": i}, "Add the companion effect or drop the tag (law 78).", hidden=hid)
        if t in ent_only and ent_only[t] != entity_kind:
            F.add("FX-ENTITY-ONLY", "S3", ent, rid, name, f"{where}: tag is {ent_only[t]}-only",
                  {"effect": i}, "Move the tag to an item (law 78).", hidden=hid)
        tgt = e.get("target") or "INHERIT"
        if owner_target == "SELF" and tgt == "INHERIT" and t in HARD_HARM:
            F.add("FX-SELF-HARM", "S1", ent, rid, name, f"{where}: harmful effect inherits a SELF target",
                  {"effect": i, "owner_target": owner_target}, "Retarget the record or the effect; as stored the "
                  "user hits themself.", "needs check", hidden=hid)
        if owner_target == "OPPONENT" and tgt == "INHERIT" and t in BUFF_TYPES:
            F.add("FX-BUFF-ENEMY", "S1", ent, rid, name, f"{where}: beneficial effect inherits an OPPONENT target",
                  {"effect": i, "owner_target": owner_target}, "Set the effect target to SELF if the buff is "
                  "meant for the caster.", "needs check", hidden=hid)
        for f in ANIM_FIELDS + SFX_FIELDS:
            v = e.get(f)
            if not v or not isinstance(v, str):
                continue
            if URL_RE.match(v):
                st = image_status(db, v)
                if st.startswith("fail"):
                    F.add("FX-COSMETIC-URL", "S5", ent, rid, name, f"{where}.{f} URL does not load ({st})",
                          {"effect": i, "url": v}, "Repoint to a working asset.", hidden=hid)
                continue
            a = assets.get(v)
            if a is None and re.fullmatch(r"[a-z_]+", v):
                db.legacy_fx[v] += 1  # built-in keyword animation (hit, smoke, ...); not an asset id
                continue
            if a is None:
                if assets:
                    F.add("FX-COSMETIC-MISSING", "S3", ent, rid, name, f"{where}.{f} points at missing asset {v}",
                          {"effect": i, "field": f, "assetId": v}, "Repoint to an existing ANIMATION/SFX asset.",
                          hidden=hid)
                continue
            want = "SFX" if f in SFX_FIELDS else "ANIMATION"
            if a.get("type") != want and not (want == "ANIMATION" and a.get("type") == "STATIC"):
                F.add("FX-COSMETIC-TYPE", "S3", ent, rid, name,
                      f"{where}.{f} points at a {a.get('type')} asset ('{a.get('name')}'), expected {want}",
                      {"effect": i, "field": f, "assetId": v}, f"Repoint to a {want} asset.", hidden=hid)


# ------------------------------------------------------------------ entity checks


def check_jutsu(F, db):
    J, B, I = db.rec["jutsu"], db.rec["bloodline"], db.rec["item"]
    equipped = {x.get("jutsuId") for a in db.rec["ai"].values() for x in a.get("jutsus") or [] if x.get("equipped")}
    for j in J.values():
        rid, name, hid = j.get("id"), j.get("name"), is_hidden(j)
        player = j.get("jutsuType") != "AI"
        if (name or "").startswith("New Jutsu"):
            F.add("JUTSU-SHELL", "S1" if ((player and not hid) or rid in equipped) else "S3", "jutsu", rid, name,
                  "blank shell record (law 59)" + (" equipped on a captured AI" if rid in equipped else ""),
                  {"name": name, "actionCostPerc": j.get("actionCostPerc")}, "Refill from the last harvest or retire.",
                  hidden=hid)
        text_checks(F, "jutsu", j, ("description", "battleDescription"))
        bounds_checks(F, db, "jutsu", "jutsu", j)
        bl = j.get("bloodlineId")
        if bl and bl not in B and B:
            F.add("REF-JUTSU-BLOODLINE", "S3" if (player and not hid) else "S5", "jutsu", rid, name,
                  f"bloodlineId {bl} does not exist (orphaned bloodline jutsu)", {"bloodlineId": bl,
                  "jutsuType": j.get("jutsuType")}, "Repoint to the live bloodline, or retire the jutsu.",
                  "needs check", hidden=hid)
        if j.get("jutsuType") == "BLOODLINE" and not bl:
            F.add("JUTSU-BLOODLINE-UNLINKED", "S3", "jutsu", rid, name, "jutsuType BLOODLINE with no bloodlineId",
                  {}, "Link the jutsu to its bloodline or change its type.", "needs check", hidden=hid)
        if bl and bl in B and not hid and is_hidden(B[bl]):
            F.add("VIS-JUTSU-HIDDEN-BLOODLINE", "S4", "jutsu", rid, name,
                  f"visible jutsu belongs to hidden bloodline '{B[bl].get('name')}'", {"bloodlineId": bl},
                  "Publish the bloodline or hide the jutsu.", "needs check", hidden=hid)
        for f, pool in (("requiredBloodlineItemId", I), ("parentJutsuId", J), ("reskinParentJutsuId", J)):
            v = j.get(f)
            if v and pool and v not in pool:
                F.add("REF-JUTSU-" + f.upper(), "S1", "jutsu", rid, name, f"{f} {v} does not exist", {f: v},
                      f"Repoint or clear {f}.", hidden=hid)
        reach = (rid in equipped) if not player else not hid
        effect_checks(F, db, "jutsu", j, j.get("effects") or [], j.get("target"), "jutsu", reach)
        if player and not hid:
            if j.get("actionCostPerc") not in (40, 60):
                F.add("JUTSU-AP-DOCTRINE", "S2", "jutsu", rid, name,
                      f"actionCostPerc {j.get('actionCostPerc')} (doctrine allows 40 or 60)",
                      {"actionCostPerc": j.get("actionCostPerc")}, "Ruling needed: keep as a deliberate exception "
                      "or move to 40/60 (balance.md 1).", "needs check", hidden=hid)
            costs = [j.get(k) for k in ("chakraCost", "staminaCost", "healthCost")]
            if any(isinstance(c, (int, float)) and 0 < c < 1 for c in costs):
                F.add("JUTSU-PLACEHOLDER-COST", "S3", "jutsu", rid, name, f"fractional placeholder pool cost {costs}",
                      {"costs": costs}, "Set real pool costs (jutsu.md 6); the value is a balance call.", hidden=hid)
            if not any((e.get("appearSfx") and e.get("appearAnimation")) for e in j.get("effects") or []
                       if isinstance(e, dict)):
                F.add("JUTSU-NO-CAST-FX", "S5", "jutsu", rid, name, "no effect carries both appearSfx and "
                      "appearAnimation (lint L30)", {}, "Add a cast animation and sound to one effect.", hidden=hid)
            if not (j.get("effects") or []):
                F.add("JUTSU-NO-EFFECTS", "S1", "jutsu", rid, name, "visible jutsu with no effects", {},
                      "Give it effects or hide it.", hidden=hid)
        _image_check(F, db, "jutsu", j, "image", visible=not hid)
    # outliers: visible player jutsu, peer group = (jutsuType, jutsuRank)
    groups = defaultdict(list)
    for j in J.values():
        if j.get("jutsuType") != "AI" and not is_hidden(j):
            groups[(j.get("jutsuType"), j.get("jutsuRank"))].append(j)
    for (jt, rk), rs in groups.items():
        lab = f"visible {jt} jutsu, rank {rk}"
        outliers(F, "OUT-JUTSU-COOLDOWN", "jutsu", [(r, r.get("cooldown") or 0) for r in rs], "cooldown",
                 "Ruling needed on cooldown.", group_label=lab)
        outliers(F, "OUT-JUTSU-COST", "jutsu",
                 [(r, (r.get("chakraCost") or 0) + (r.get("staminaCost") or 0) + (r.get("healthCost") or 0))
                  for r in rs], "total pool cost", "Ruling needed on pool cost.", group_label=lab)
        dmg = [(r, max([e.get("power") or 0 for e in r.get("effects") or []
                        if isinstance(e, dict) and e.get("type") == "damage"] or [0])) for r in rs]
        outliers(F, "OUT-JUTSU-DAMAGE", "jutsu", [x for x in dmg if x[1] > 0], "max damage power",
                 "Ruling needed on damage power.", group_label=lab)
    dup_names(F, "jutsu", list(J.values()))


def _image_check(F, db, ent, rec, field, visible, label=None):
    url = rec.get(field)
    st = image_status(db, url)
    rid, name = rec.get("id") or rec.get("userId"), rec.get("name") or rec.get("username")
    if st == "empty":
        F.add("IMG-EMPTY", "S3" if visible else "S5", ent, rid, name, f"{field} is empty", {"field": field},
              "Upload art.", hidden=not visible)
    elif st.startswith("fail") or st.startswith("not-an-image"):
        F.add("IMG-BROKEN", "S3" if visible else "S5", ent, rid, name, f"{field} does not load: {st}",
              {"field": field, "url": url, "check": db.images.get(url)}, "Re-upload the art and repoint the field.",
              hidden=not visible)


def check_items(F, db):
    J, I, B, Q = db.rec["jutsu"], db.rec["item"], db.rec["bloodline"], db.rec["quest"]
    for it in I.values():
        rid, name, hid = it.get("id"), it.get("name"), is_hidden(it)
        text_checks(F, "item", it, ("description", "battleDescription"))
        bounds_checks(F, db, "item", "item", it)
        _image_check(F, db, "item", it, "image", visible=not hid)
        effs = it.get("effects") or []
        effect_checks(F, db, "item", it, effs, it.get("target"), "item")
        if not any((it.get(k) or 0) > 0 for k in ("cost", "repsCost", "seichiSilverCost")):
            F.add("ITEM-NO-COST", "S3", "item", rid, name, "cost, repsCost and seichiSilverCost are all 0",
                  {}, "Set one price above 0; SuperRefineItem rejects the record on its next save.", hidden=hid)
        if it.get("itemType") == "CONSUMABLE" and not it.get("destroyOnUse"):
            F.add("ITEM-CONSUMABLE-KEEP", "S3", "item", rid, name, "CONSUMABLE with destroyOnUse false",
                  {}, "Set destroyOnUse true (write validator) or change the item type.", hidden=hid)
        if it.get("inShop") and hid:
            F.add("ITEM-SHOP-HIDDEN", "S4", "item", rid, name, "inShop but hidden", {}, "Decide: publish or "
                  "take it out of the shop.", "needs check", hidden=hid)
        for f in ("parentItemId", "farmYieldItemId", "farmExtractSeedItemId"):
            v = it.get(f)
            if v and v not in I:
                F.add("REF-ITEM-" + f.upper(), "S1", "item", rid, name, f"{f} {v} does not exist", {f: v},
                      f"Repoint or clear {f}.", hidden=hid)
        if it.get("bloodlineId") and B and it["bloodlineId"] not in B:
            F.add("REF-ITEM-BLOODLINE", "S1", "item", rid, name, f"bloodlineId {it['bloodlineId']} does not exist",
                  {}, "Repoint or clear bloodlineId.", hidden=hid)
        for i, e in enumerate(effs):
            if not isinstance(e, dict):
                continue
            if e.get("type") == "injectjutsus":
                for jid in e.get("jutsuIds") or []:
                    jj = J.get(jid)
                    if jj is None:
                        F.add("REF-ITEM-INJECT", "S1", "item", rid, name, f"injectjutsus points at missing jutsu {jid}",
                              {"effect": i, "jutsuId": jid}, "Repoint the inject to an existing jutsu.", hidden=hid)
                    elif is_hidden(jj) or not jj.get("injectableInBattle"):
                        F.add("ITEM-INJECT-UNUSABLE", "S1", "item", rid, name,
                              f"injected jutsu '{jj.get('name')}' is "
                              + ("hidden" if is_hidden(jj) else "not injectableInBattle"),
                              {"effect": i, "jutsuId": jid, "hidden": jj.get("hidden"),
                               "injectableInBattle": jj.get("injectableInBattle")},
                              "Injected jutsu must be unhidden and injectableInBattle (item.md 9.2).",
                              "needs check" if not is_hidden(jj) else "verified", hidden=hid)
            if e.get("type") == "noncombatconsumereward":
                reward_refs(F, db, "item", it, e, f"effects[{i}]")
        if it.get("itemType") == "WEAPON" and not hid:
            buckets = [e for e in effs if isinstance(e, dict) and e.get("type") in ("increasedamagegiven",
                                                                                     "increasedamagetaken")]
            if len(buckets) > 1:
                F.add("ITEM-WEAPON-RIDERS", "S2", "item", rid, name, f"weapon carries {len(buckets)} damage buckets "
                      "(doctrine: at most one modest bucket)", {"powers": [b.get("power") for b in buckets]},
                      "Ruling needed (D-riders-light).", "needs check", hidden=hid)
    groups = defaultdict(list)
    for it in I.values():
        if not is_hidden(it):
            groups[(it.get("itemType"), it.get("rarity"))].append(it)
    for (t, r), rs in groups.items():
        lab = f"visible {t} items, {r}"
        outliers(F, "OUT-ITEM-COST", "item", [(x, x.get("cost") or 0) for x in rs if (x.get("cost") or 0) > 0],
                 "ryo cost", "Ruling needed on price.", group_label=lab)
        dm = [(x, max([e.get("power") or 0 for e in x.get("effects") or [] if isinstance(e, dict)
                       and e.get("type") in ("damage", "pierce")] or [0])) for x in rs]
        outliers(F, "OUT-ITEM-DAMAGE", "item", [d for d in dm if d[1] > 0], "max damage power",
                 "Ruling needed on damage.", group_label=lab)
    dup_names(F, "item", list(I.values()))


REWARD_ID_FIELDS = (("reward_items", "item"), ("reward_jutsus", "jutsu"), ("reward_bloodlines", "bloodline"),
                    ("reward_hunter_items_ids", "item"), ("reward_gathering_items_ids", "item"))


def _ids(v):
    out = []
    for x in v or []:
        if isinstance(x, str):
            out.append(x)
        elif isinstance(x, dict):
            out.extend([i for i in x.get("ids") or [] if isinstance(i, str)])
            if isinstance(x.get("id"), str):
                out.append(x["id"])
    return out


def reward_refs(F, db, ent, rec, block, where):
    rid, name, hid = rec.get("id"), rec.get("name"), is_hidden(rec)
    for f, target in REWARD_ID_FIELDS:
        pool = db.rec[target]
        if not pool:
            continue
        for x in _ids(block.get(f)):
            t = pool.get(x)
            if t is None:
                F.add("REF-REWARD", "S3" if hid else "S1", ent, rid, name, f"{where}.{f} grants missing {target} {x}",
                      {"where": where, "field": f, "id": x}, f"Repoint the reward to an existing {target}.",
                      hidden=hid)
            elif not hid and is_hidden(t) and target != "item":
                F.add("VIS-REWARD-HIDDEN", "S3", ent, rid, name,
                      f"{where}.{f} grants hidden {target} '{t.get('name')}'", {"where": where, "id": x},
                      f"Publish the {target} or change the reward.", "needs check", hidden=hid)
            elif not hid and is_hidden(t):
                F.add("VIS-REWARD-HIDDEN-ITEM", "S4", ent, rid, name,
                      f"{where}.{f} grants hidden item '{t.get('name')}'", {"where": where, "id": x},
                      "Confirm the hidden item is meant to be granted (players can still hold hidden items).",
                      "needs check", hidden=hid)


def _next_ids(o):
    n = o.get("nextObjectiveId")
    if isinstance(n, list):
        return [c.get("nextObjectiveId") for c in n if isinstance(c, dict)]
    return [n] if n else []


LOCATION_TASKS = {"move_to_location", "collect_item", "deliver_item", "defeat_opponents", "win_encounter_at_location"}
BATTLE_TASKS = {"start_battle", "defeat_opponents"}
TERMINALS = {"win_quest", "fail_quest", "reset_quest"}
DAILY_GOVERNED = {"mission", "errand", "crime", "medical", "daily", "pvp", "anbu", "war", "village_mission"}
REWARD_SUM_KEYS = ("reward_money", "reward_exp", "reward_tokens", "reward_prestige", "reward_clanpoints",
                   "reward_reputation", "reward_seichi_silver", "reward_skillpoints")


def check_quests(F, db, now_date):
    Q, A, AI, AIN, I, J, B = (db.rec["quest"], db.rec["asset"], db.rec["ai"], db.names.get("ai") or {},
                              db.rec["item"], db.rec["jutsu"], db.rec["bloodline"])
    for q in Q.values():
        rid, name, hid = q.get("id"), q.get("name"), is_hidden(q)
        vis = not hid
        content = q.get("content") or {}
        objs = [o for o in content.get("objectives") or [] if isinstance(o, dict)]
        ids = [o.get("id") for o in objs]
        byid = {o.get("id"): o for o in objs}
        text_checks(F, "quest", q, ("description", "successDescription"))
        bounds_checks(F, db, "quest", "quest", q)
        _image_check(F, db, "quest", q, "image", visible=vis)
        tset = {o.get("task") for o in objs}
        if not q.get("consecutiveObjectives") and len(objs) >= 2 and q.get("questType") not in ("achievement",) and \
                tset & {"win_quest", "dialog", "start_battle", "reset_quest"}:
            win = "win_quest" in tset
            F.add("QUEST-NOT-CONSECUTIVE", ("S1" if win else "S3") if vis else "S5", "quest", rid, name,
                  "consecutiveObjectives is false: every objective is live at once (law 23)"
                  + ("; the win_quest node is claimable immediately" if win else ""), {"tasks": sorted(tset)},
                  "Set consecutiveObjectives true on a full-record edit.", "verified" if win else "needs check",
                  hidden=hid)
        rl, ml = q.get("requiredLevel") or 0, q.get("maxLevel")
        if isinstance(ml, (int, float)) and ml < rl:
            F.add("QUEST-LEVEL-WINDOW", "S1" if vis else "S3", "quest", rid, name,
                  f"maxLevel {ml} below requiredLevel {rl}: nobody is eligible", {"requiredLevel": rl, "maxLevel": ml},
                  "Fix the level window.", hidden=hid)
        pre = q.get("prerequisiteQuestId")
        if pre:
            if pre not in Q:
                F.add("REF-QUEST-PREREQ", "S1" if vis else "S3", "quest", rid, name,
                      f"prerequisiteQuestId {pre} does not exist", {"prerequisiteQuestId": pre},
                      "Repoint or clear the prerequisite.", hidden=hid)
            elif vis and is_hidden(Q[pre]):
                F.add("VIS-QUEST-PREREQ-HIDDEN", "S1", "quest", rid, name,
                      f"prerequisite '{Q[pre].get('name')}' is hidden, so non-staff can never unlock this quest",
                      {"prerequisiteQuestId": pre}, "Publish the prerequisite or clear it.", hidden=hid)
        rb = q.get("requiredBloodlineId")
        if rb and B and rb not in B:
            F.add("REF-QUEST-BLOODLINE", "S1", "quest", rid, name, f"requiredBloodlineId {rb} does not exist", {},
                  "Repoint or clear.", hidden=hid)
        qt = q.get("questType")
        if qt == "daily" and not (3 <= len(objs) <= 7):
            F.add("QUEST-DAILY-COUNT", "S3", "quest", rid, name, f"daily quest with {len(objs)} objectives (3-7)",
                  {}, "Bring the objective count to 3-7.", hidden=hid)
        ends, starts = (q.get("endsAt") or "")[:10], (q.get("startsAt") or "")[:10]
        if ends and starts and starts > ends:
            F.add("QUEST-DATES", "S1" if vis else "S3", "quest", rid, name, f"startsAt {starts} after endsAt {ends}",
                  {}, "Fix the dates.", hidden=hid)
        if vis and ends and ends < now_date:
            F.add("QUEST-EXPIRED-VISIBLE", "S5", "quest", rid, name, f"visible but ended {ends}",
                  {"endsAt": ends}, "Hide or re-date the quest.", hidden=hid)
        if vis and qt == "event" and not ends:
            F.add("QUEST-EVENT-NO-END", "S4", "quest", rid, name, "visible event quest with no endsAt",
                  {}, "Confirm it is meant to run forever, else set endsAt.", "needs check", hidden=hid)
        reward_refs(F, db, "quest", q, content.get("reward") or {}, "content.reward")
        # scenes
        def scene(where, bg, chars, visible):
            if bg:
                if URL_RE.match(bg):
                    st = image_status(db, bg)
                    if st.startswith("fail"):
                        F.add("IMG-BROKEN", "S3" if visible else "S5", "quest", rid, name,
                              f"{where}.sceneBackground URL does not load ({st})", {"url": bg},
                              "Repoint to a working background.", hidden=hid)
                elif A and bg not in A:
                    by_name = [x.get("id") for x in A.values() if x.get("name") == bg]
                    F.add("REF-SCENE-BG", "S3" if visible else "S5", "quest", rid, name,
                          f"{where}.sceneBackground '{bg}' is not a gameAsset id"
                          + (f" (an asset has that NAME: {by_name[0]})" if by_name else ""),
                          {"where": where, "value": bg, "asset_with_that_name": by_name[:3]},
                          "Write the asset id, not its name or a fill-in token.", hidden=hid)
                elif A and A[bg].get("type") != "SCENE_BACKGROUND":
                    F.add("SCENE-BG-TYPE", "S3", "quest", rid, name,
                          f"{where}.sceneBackground is a {A[bg].get('type')} asset ('{A[bg].get('name')}')",
                          {"where": where, "id": bg}, "Use a SCENE_BACKGROUND asset (3:2).", "needs check", hidden=hid)
                elif A:
                    st = image_status(db, A[bg].get("image"))
                    if st.startswith("fail"):
                        F.add("IMG-BROKEN-SCENE", "S3" if visible else "S5", "quest", rid, name,
                              f"{where}.sceneBackground asset '{A[bg].get('name')}' image does not load",
                              {"where": where, "assetId": bg}, "Re-upload the asset art.", hidden=hid)
            for c in chars or []:
                if not isinstance(c, str) or not c:
                    continue
                if c in A:
                    if A[c].get("type") != "SCENE_CHARACTER":
                        F.add("SCENE-CHAR-TYPE", "S3", "quest", rid, name,
                              f"{where}.sceneCharacters uses a {A[c].get('type')} asset ('{A[c].get('name')}')",
                              {"where": where, "id": c}, "Use a SCENE_CHARACTER asset.", "needs check", hidden=hid)
                elif c in AIN or c in AI:
                    F.add("SCENE-CHAR-AI", "S3", "quest", rid, name,
                          f"{where}.sceneCharacters holds an AI userId; it renders nothing (law 49)",
                          {"where": where, "id": c}, "Make a SCENE_CHARACTER asset for the AI.", hidden=hid)
                elif A and not URL_RE.match(c):
                    F.add("REF-SCENE-CHAR", "S3", "quest", rid, name,
                          f"{where}.sceneCharacters {c} is not a gameAsset", {"where": where, "id": c},
                          "Repoint to a SCENE_CHARACTER asset.", hidden=hid)
            if chars and len([c for c in chars if c]) > 1:
                F.add("SCENE-CHAR-STACK", "S5", "quest", rid, name,
                      f"{where} has {len(chars)} scene characters; they stack in one spot (law 48)",
                      {"where": where}, "Keep one character per node.", hidden=hid)
        scene("content", content.get("sceneBackground"), content.get("sceneCharacters"), vis)
        if objs and not content.get("sceneBackground") and vis:
            F.add("QUEST-NO-TOP-SCENE", "S5", "quest", rid, name, "top-level sceneBackground empty (law 25)", {},
                  "Set a deliberate global scene.", hidden=hid)
        # graph
        incoming = Counter()
        for o in objs:
            for n in _next_ids(o) + ([o.get("failObjectiveId")] if o.get("failObjectiveId") else []):
                if n:
                    incoming[n] += 1
        for o in objs:
            oid, task = o.get("id"), o.get("task")
            where = f"objective {oid} ({task})"
            for f, targets in (("nextObjectiveId", _next_ids(o)), ("failObjectiveId", [o.get("failObjectiveId")]),
                               ("resetObjectiveId", [o.get("resetObjectiveId")])):
                for t in targets:
                    if t and t not in byid:
                        F.add("QUEST-FLOW-REF", "S3" if vis else "S5", "quest", rid, name,
                              f"{where}.{f} points at missing objective {t}; save-time flow validation rejects "
                              "unknown references, so the next editor save of this quest will fail",
                              {"objective": oid, "target": t}, "Repoint or clear the edge.", hidden=hid)
            if task == "dialog":
                nx = o.get("nextObjectiveId")
                if not isinstance(nx, list) or not nx:
                    F.add("QUEST-DIALOG-NO-CHOICE", "S1" if vis else "S3", "quest", rid, name,
                          f"{where} has no choices (law 85)", {"objective": oid}, "Add a continuation.", hidden=hid)
                elif any(isinstance(c, dict) and not c.get("nextObjectiveId") for c in nx):
                    F.add("QUEST-CHOICE-DEAD-END", "S1" if vis else "S3", "quest", rid, name,
                          f"{where} has a choice that leads nowhere", {"objective": oid,
                          "choices": [c.get("text") for c in nx if isinstance(c, dict) and not c.get("nextObjectiveId")]},
                          "Route every choice.", hidden=hid)
                for c in nx if isinstance(nx, list) else []:
                    if isinstance(c, dict) and isinstance(c.get("text"), str):
                        text_checks(F, "quest", {"id": rid, "name": name, "hidden": hid,
                                                 f"{oid}.choice": c["text"]}, (f"{oid}.choice",), check_name=False)
            text_checks(F, "quest", {"id": rid, "name": name, "hidden": hid, f"{oid}.description":
                                     o.get("description")}, (f"{oid}.description",), check_name=False)
            if task in BATTLE_TASKS:
                opp = o.get("opponentAIs") or []
                if not _ids(opp):
                    F.add("QUEST-BATTLE-NO-OPPONENT", "S1" if vis else "S3", "quest", rid, name,
                          f"{where} has no opponents", {"objective": oid}, "Add opponentAIs.", hidden=hid)
                head = sum((x.get("number") or 0) for x in opp if isinstance(x, dict))
                if head > 3:
                    F.add("QUEST-BATTLE-HEADCOUNT", "S3", "quest", rid, name,
                          f"{where} opponent headcount {head} (> 3; number is a COUNT, law 44)",
                          {"objective": oid, "opponentAIs": opp}, "Confirm the count.", "needs check", hidden=hid)
                if not o.get("failObjectiveId"):
                    sb = task == "start_battle"
                    F.add("QUEST-BATTLE-NO-FAIL", ("S1" if sb else "S3") if vis else "S5", "quest", rid, name,
                          f"{where} has no failObjectiveId; " + ("a loss strands the player on the retry button "
                          "(quest.md 3.1)" if sb else "a loss has no route (quest.md 3.2 re-arm risk)"),
                          {"objective": oid}, "Route the loss to a reset or fail node.",
                          "verified" if sb else "needs check", hidden=hid)
                if task == "start_battle" and incoming[oid]:
                    preds = [p for p in objs if oid in _next_ids(p)]
                    if preds and not any(p.get("task") == "dialog" for p in preds):
                        F.add("QUEST-BATTLE-UNGATED", "S1" if vis else "S3", "quest", rid, name,
                              f"{where} is not directly behind a dialog; it pre-activates with the previous node "
                              "and can auto-resolve without a fight (quest.md 3.1/3.7)",
                              {"objective": oid, "preds": [(p.get("id"), p.get("task")) for p in preds]},
                              "Put a dialog directly before the battle.", "needs check", hidden=hid)
                for x in _ids(opp) + _ids(o.get("allyAIs")):
                    if AIN and x not in AIN:
                        F.add("REF-QUEST-AI", "S1" if vis else "S3", "quest", rid, name,
                              f"{where} references missing AI {x}", {"objective": oid, "aiId": x},
                              "Repoint to an existing AI.", hidden=hid)
                    elif x in AI and not o.get("opponent_scaled_to_user") and vis:
                        lv = AI[x].get("level") or 0
                        if rl and (lv > (ml or 100) + 10 or lv + 50 < rl):
                            F.add("QUEST-AI-LEVEL", "S2", "quest", rid, name,
                                  f"{where} AI '{AI[x].get('username')}' level {lv} vs quest window {rl}-{ml}",
                                  {"objective": oid, "aiId": x, "aiLevel": lv}, "Ruling needed on difficulty.",
                                  "needs check", hidden=hid)
            if task == "reset_quest":
                t = o.get("resetObjectiveId")
                if t in byid and byid[t].get("task") in BATTLE_TASKS:
                    F.add("QUEST-RESET-ONTO-BATTLE", "S3", "quest", rid, name, f"{where} resets onto a battle (law 88)",
                          {"objective": oid, "target": t}, "Reset to the dialog before the fight.", "needs check",
                          hidden=hid)
            if task in LOCATION_TASKS:
                st, lt = o.get("sectorType"), o.get("locationType")
                x, y = o.get("longitude"), o.get("latitude")
                if lt == "specific" and st not in ("random", "from_list") and (x or 0) == 0 and (y or 0) == 0:
                    F.add("QUEST-LOC-ORIGIN", "S1" if (vis and task == "collect_item") else "S3", "quest", rid, name,
                          f"{where} placed at tile 0,0 (law 54)", {"objective": oid, "sectorType": st},
                          "Give the node real coordinates two or more tiles off the edge.", hidden=hid)
                elif lt == "specific" and isinstance(x, (int, float)) and isinstance(y, (int, float)) and (
                        not (0 <= x <= 25) or not (0 <= y <= 25)):
                    F.add("QUEST-LOC-OFFMAP", "S3" if vis else "S5", "quest", rid, name,
                          f"{where} coordinates {x},{y} are off the 26x26 sector", {"objective": oid},
                          "Move the node inside the sector.", hidden=hid)
                if not o.get("image"):
                    F.add("QUEST-LOC-NO-PIN", "S3" if vis else "S5", "quest", rid, name,
                          f"{where} has no image, so no map pin is drawn (law 52)", {"objective": oid},
                          "Set the node image.", hidden=hid)
                if task in ("collect_item", "deliver_item"):
                    for x in _ids(o.get("collectItemIds")) + _ids(o.get("deliverItemIds")):
                        if I and x not in I:
                            F.add("REF-QUEST-ITEM", "S1" if vis else "S3", "quest", rid, name,
                                  f"{where} references missing item {x}", {"objective": oid, "itemId": x},
                                  "Repoint to an existing item.", hidden=hid)
                if task == "win_encounter_at_location":
                    att = o.get("attackers") or []
                    if not _ids(att) or not any((a.get("number") or 0) > 0 for a in att if isinstance(a, dict)):
                        F.add("QUEST-ENCOUNTER-NEVER", "S1" if vis else "S3", "quest", rid, name,
                              f"{where} has no attacker with spawn chance > 0; it can never complete",
                              {"objective": oid}, "Add attackers with number > 0 (a percent).", hidden=hid)
            for x in _ids(o.get("attackers")):
                if AIN and x not in AIN:
                    F.add("REF-QUEST-AI", "S1" if vis else "S3", "quest", rid, name,
                          f"{where} attackers reference missing AI {x}", {"objective": oid, "aiId": x},
                          "Repoint to an existing AI.", hidden=hid)
            for f, pool, lab in (("newQuestIds", Q, "quest"), ("completeQuestIds", Q, "quest"),
                                 ("craftItemIds", I, "item"), ("buyItemIds", I, "item"), ("useItemIds", I, "item"),
                                 ("trainJutsuIds", J, "jutsu"), ("useJutsuIds", J, "jutsu")):
                for x in _ids(o.get(f)):
                    if pool and x not in pool:
                        F.add("REF-QUEST-" + lab.upper(), "S1" if vis else "S3", "quest", rid, name,
                              f"{where}.{f} references missing {lab} {x}", {"objective": oid, "id": x},
                              f"Repoint to an existing {lab}.", hidden=hid)
            reward_refs(F, db, "quest", q, o, f"objective {oid}")
            scene(f"objective {oid}", o.get("sceneBackground"), o.get("sceneCharacters"), vis)
        if objs:
            starts = [o.get("id") for o in objs if not incoming[o.get("id")]]
            if len(starts) != 1 and q.get("consecutiveObjectives"):
                F.add("QUEST-FLOW-STARTS", "S1" if vis else "S3", "quest", rid, name,
                      f"{len(starts)} starting objectives (exactly 1 required)", {"starts": starts[:10]},
                      "Leave exactly one unreferenced start node.", hidden=hid)
            if len(set(ids)) != len(ids):
                F.add("QUEST-FLOW-DUP-ID", "S1" if vis else "S3", "quest", rid, name, "duplicate objective ids",
                      {"dups": [k for k, v in Counter(ids).items() if v > 1]}, "Make ids unique.", hidden=hid)
            # reachability + cycles
            adj = {o.get("id"): [n for n in _next_ids(o) + [o.get("failObjectiveId")] if n in byid] for o in objs}
            seen, cyc = set(), False
            if starts:
                stack = [(starts[0], iter(adj.get(starts[0], [])))]
                onpath = {starts[0]}
                seen.add(starts[0])
                while stack:
                    node, it = stack[-1]
                    nxt = next(it, None)
                    if nxt is None:
                        stack.pop()
                        onpath.discard(node)
                        continue
                    if nxt in onpath:
                        cyc = True
                    elif nxt not in seen:
                        seen.add(nxt)
                        onpath.add(nxt)
                        stack.append((nxt, iter(adj.get(nxt, []))))
            unreach = [i for i in ids if i not in seen and len(starts) == 1 and q.get("consecutiveObjectives")]
            if cyc:
                F.add("QUEST-FLOW-CYCLE", "S1" if vis else "S3", "quest", rid, name, "objective graph has a cycle "
                      "(law 87)", {}, "Route loops through reset_quest.", hidden=hid)
            if unreach:
                F.add("QUEST-FLOW-UNREACHABLE", "S3", "quest", rid, name, f"{len(unreach)} objectives unreachable "
                      "from the start", {"objectives": unreach[:10]}, "Wire or remove them.", hidden=hid)
            tasks = Counter(o.get("task") for o in objs)
            dialog_terms = [o.get("id") for o in objs if o.get("task") == "dialog" and not _next_ids(o)]
            if not tasks.get("win_quest") and tasks.get("dialog"):
                F.add("QUEST-NO-WIN", "S3" if vis else "S5", "quest", rid, name,
                      "quest with dialog nodes has no win_quest node; the builder flow validator rejects this shape "
                      "(law 86) and engine completion without it is unverified", {"tasks": dict(tasks)},
                      "End the walked path on win_quest.", "needs check", hidden=hid)
            # rewards
            total = Counter()
            for blk in [content.get("reward") or {}] + objs:
                for k in REWARD_SUM_KEYS:
                    v = blk.get(k)
                    if isinstance(v, (int, float)) and not isinstance(v, bool):
                        total[k] += v
                total["items"] += len(_ids(blk.get("reward_items")))
                total["jutsus"] += len(_ids(blk.get("reward_jutsus")))
            q["_reward_total"] = dict(total)
            if vis and not any(total.values()) and qt in ("story", "mission", "event", "crime", "errand",
                                                           "battlepyramid", "tier", "exam", "daily"):
                F.add("QUEST-ZERO-REWARD", "S2", "quest", rid, name, f"visible {qt} quest pays nothing",
                      {"rewards": dict(total)}, "Ruling needed: intended (e.g. tutorial) or missing rewards.",
                      "needs check", hidden=hid)
            # mission-hall and daily types are throttled by the engine's daily counters (quest.md 3.4c)
            uncapped = (q.get("retryDelay") in (None, "none") and qt not in DAILY_GOVERNED and (
                qt not in ("event", "story", "battlepyramid", "starter", "raid") or (q.get("maxCompletes") or 0) > 1))
            if vis and uncapped and (total.get("reward_exp") or total.get("reward_money") or total.get("reward_tokens")):
                F.add("QUEST-UNCAPPED-PAYS", "S2", "quest", rid, name,
                      f"repeatable without delay (retryDelay none, maxCompletes {q.get('maxCompletes')}) and pays "
                      f"exp {total.get('reward_exp', 0):g} / ryo {total.get('reward_money', 0):g} / tokens "
                      f"{total.get('reward_tokens', 0):g}", {"rewards": dict(total), "questType": qt},
                      "Ruling needed (balance.md reward class 1: uncapped records pay materials only).",
                      "needs check", hidden=hid, group="uncapped")
    groups = defaultdict(list)
    for q in Q.values():
        if not is_hidden(q) and q.get("_reward_total"):
            groups[(q.get("questType"), q.get("questRank"))].append(q)
    for (t, r), rs in groups.items():
        for k in ("reward_money", "reward_exp", "reward_tokens", "reward_prestige"):
            rows = [(x, x["_reward_total"].get(k, 0)) for x in rs if x["_reward_total"].get(k, 0) > 0]
            outliers(F, "OUT-QUEST-" + k.upper(), "quest", rows, k, "Ruling needed on reward size.",
                     group_label=f"visible {t} quests, rank {r}")
    for q in Q.values():
        q.pop("_reward_total", None)
    dup_names(F, "quest", list(Q.values()))


def check_bloodlines(F, db):
    B, J = db.rec["bloodline"], db.rec["jutsu"]
    by_bl = defaultdict(list)
    for j in J.values():
        if j.get("bloodlineId"):
            by_bl[j["bloodlineId"]].append(j)
    for b in B.values():
        rid, name, hid = b.get("id"), b.get("name"), is_hidden(b)
        text_checks(F, "bloodline", b, ("description",))
        bounds_checks(F, db, "bloodline", "bloodline", b)
        _image_check(F, db, "bloodline", b, "image", visible=not hid)
        effect_checks(F, db, "bloodline", b, b.get("effects") or [], "SELF", "bloodline")
        js = by_bl.get(rid, [])
        if not hid and J and not [j for j in js if not is_hidden(j)]:
            F.add("VIS-BLOODLINE-NO-JUTSU", "S1", "bloodline", rid, name,
                  f"visible bloodline has {len(js)} jutsu and none are visible", {"jutsu": len(js)},
                  "Publish its jutsu or hide the bloodline.", "needs check", hidden=hid)
    dup_names(F, "bloodline", list(B.values()))


def check_assets(F, db):
    A = db.rec["asset"]
    for a in A.values():
        rid, name, hid = a.get("id"), a.get("name"), is_hidden(a)
        bounds_checks(F, db, "asset", "gameAsset", a)
        if a.get("type") in ("SFX", "MUSIC"):
            st = image_status(db, a.get("image") or a.get("url"))
        else:
            st = image_status(db, a.get("image"))
        if st == "empty":
            F.add("ASSET-NO-FILE", "S3", "asset", rid, name, "asset has no image/file", {}, "Upload the file.",
                  hidden=hid)
        elif st.startswith("fail"):
            F.add("IMG-BROKEN", "S3", "asset", rid, name, f"asset file does not load: {st}",
                  {"url": a.get("image")}, "Re-upload and repoint.", hidden=hid)
    groups = defaultdict(list)
    for a in A.values():
        groups[(a.get("type"), a.get("folder") or "", norm_name(a.get("name")))].append(a)
    for (t, folder, n), rs in groups.items():
        if len(rs) > 1 and n:
            F.add("ASSET-DUP-NAME", "S5", "asset", rs[0].get("id"), rs[0].get("name"),
                  f"{len(rs)} {t} assets named '{rs[0].get('name')}' in folder '{folder}'",
                  {"ids": [r.get("id") for r in rs]}, "Rename so pickers can tell them apart.")


def check_ai(F, db):
    AI, J, I, P, AIN = db.rec["ai"], db.rec["jutsu"], db.rec["item"], db.rec["aiprofile"], db.names.get("ai") or {}
    caps = {}
    raw = (((db.contracts.get("45e") or {}).get("constants") or {}).get("USER_CAPS") or {}).get("raw", "")
    for m in re.finditer(r'"?([A-Z ]+?)"?:\s*\{\s*GENS_CAP:\s*(\w+),\s*STATS_CAP:\s*(\w+),\s*LVL_CAP:\s*(\d+)', raw):
        caps[m.group(1).strip()] = int(m.group(4))
    max_stats = ((db.contracts.get("45e") or {}).get("constants") or {}).get("MAX_STATS_CAP", {}).get("value")
    stat_cap = {}
    for m in re.finditer(r'"?([A-Z ]+?)"?:\s*\{\s*GENS_CAP:\s*(\w+),\s*STATS_CAP:\s*(\w+),', raw):
        v = m.group(3)
        stat_cap[m.group(1).strip()] = int(v) if v.isdigit() else max_stats
    quest_ai = defaultdict(list)
    for q in db.rec["quest"].values():
        for o in (q.get("content") or {}).get("objectives") or []:
            if isinstance(o, dict):
                for x in _ids(o.get("opponentAIs")) + _ids(o.get("attackers")) + _ids(o.get("allyAIs")):
                    quest_ai[x].append(q)
    for uid, a in AI.items():
        name = a.get("username")
        live = AIN.get(uid)
        used = [q for q in quest_ai.get(uid, []) if not is_hidden(q)]
        visible = bool(used) or bool((live or a).get("inArena"))
        if AIN and live is None:
            F.add("AI-GONE", "S5", "ai", uid, name, "captured AI is no longer in profile.getAllAiNames", {},
                  "Ignore if deleted on purpose.", "needs check", hidden=not visible)
            continue
        lvl = (live or {}).get("level", a.get("level")) or 0
        rank = a.get("rank")
        if lvl > 100:
            F.add("AI-LEVEL-ABOVE-100", "S5", "ai", uid, name, f"level {lvl} is above the player cap of 100",
                  {"level": lvl}, "Confirm the over-cap level is intended.", "needs check", hidden=not visible)
        elif rank in caps and lvl > caps[rank] and not a.get("isSummon"):
            F.add("AI-RANK-LVLCAP", "S3", "ai", uid, name,
                  f"level {lvl} above the {rank} LVL_CAP {caps[rank]} (law 16); rank is below what the level implies",
                  {"level": lvl, "rank": rank}, "Raise the rank to match the level (enemy.py derives it).",
                  "needs check", hidden=not visible)
        statv = [a.get(k) for k in ("strength", "speed", "intelligence", "willpower", "ninjutsuOffence",
                                    "ninjutsuDefence", "genjutsuOffence", "genjutsuDefence", "taijutsuOffence",
                                    "taijutsuDefence", "bukijutsuOffence", "bukijutsuDefence")
                 if isinstance(a.get(k), (int, float))]
        if rank in stat_cap and stat_cap[rank] and statv and max(statv) > stat_cap[rank] and not a.get("isSummon"):
            F.add("AI-STATS-CLAMPED", "S2", "ai", uid, name,
                  f"highest stat {max(statv):,.0f} above the {rank} STATS_CAP {stat_cap[rank]:,}; clamped in combat",
                  {"rank": rank, "max_stat": max(statv)}, "Ruling needed: raise rank or accept the clamp.",
                  "needs check", hidden=not visible)
        eq = [j for j in a.get("jutsus") or [] if j.get("equipped")]
        if not eq and visible:
            F.add("AI-NO-JUTSU", "S1" if used else "S3", "ai", uid, name, "no equipped jutsu", {"used_by": [q.get("name") for q in used][:5]},
                  "Equip a kit.", "needs check", hidden=not visible)
        for j in a.get("jutsus") or []:
            live_j = J.get(j.get("jutsuId"))
            if J and live_j is None:
                F.add("REF-AI-JUTSU", "S1" if visible else "S3", "ai", uid, name,
                      f"equipped jutsu {j.get('jutsuId')} ('{j.get('name')}') no longer exists",
                      {"jutsuId": j.get("jutsuId")}, "Re-equip with an existing jutsu.", hidden=not visible)
            elif live_j and j.get("equipped") and (live_j.get("updatedAt") or "") > (j.get("updatedAt") or "~"):
                cap_at = db.at.get(("ai", uid)) or ""
                observed = cap_at > (live_j.get("updatedAt") or "")
                F.add("AI-STALE-EQUIP" if observed else "AI-STALE-EQUIP-UNCONFIRMED",
                      ("S1" if visible else "S3") if observed else "S3", "ai", uid, name,
                      f"jutsu '{live_j.get('name')}' edited {live_j.get('updatedAt', '')[:10]} after it was equipped "
                      f"{(j.get('updatedAt') or '')[:10]}; the combat link may be severed (laws 18/60)"
                      + ("" if observed else f"; AI capture {cap_at[:10]} predates the edit, so a later re-equip "
                         "would not show here"),
                      {"jutsuId": j.get("jutsuId"), "jutsu_updatedAt": live_j.get("updatedAt"),
                       "equip_updatedAt": j.get("updatedAt"), "ai_captured_at": cap_at},
                      "Unequip, save, then re-equip." + ("" if observed else " Take a fresh profile.getAi first."),
                      "needs check", hidden=not visible)
        for it in a.get("items") or []:
            if I and it.get("itemId") not in I:
                F.add("REF-AI-ITEM", "S3", "ai", uid, name, f"item {it.get('itemId')} no longer exists",
                      {"itemId": it.get("itemId")}, "Remove or replace the item.", hidden=not visible)
        _image_check(F, db, "ai", {"userId": uid, "username": name, "avatar": (live or a).get("avatar")}, "avatar",
                     visible=visible)
        prof = P.get(a.get("aiProfileId")) if a.get("aiProfileId") else None
        if prof:
            rules = prof.get("rules") or []
            eq_ids = {j.get("jutsuId") for j in eq}
            rng = {j.get("jutsuId"): (J.get(j.get("jutsuId")) or {}).get("range", j.get("range")) for j in eq}
            for i, r in enumerate(rules):
                act = r.get("action") or {}
                jid = act.get("jutsuId")
                if act.get("type") == "use_specific_jutsu" and jid and jid not in eq_ids:
                    F.add("AI-RULE-UNEQUIPPED", "S1" if visible else "S3", "ai", uid, name,
                          f"rule {i} uses jutsu {jid} that is not equipped; the rule is inert",
                          {"rule": i, "jutsuId": jid}, "Equip the jutsu or change the rule.", hidden=not visible)
                if act.get("type") == "use_specific_jutsu" and jid in rng and isinstance(rng[jid], int):
                    for c in r.get("conditions") or []:
                        if c.get("type") == "distance_lower_than" and isinstance(c.get("value"), (int, float)) \
                                and c["value"] > rng[jid] + 1 and rng[jid] > 0:
                            F.add("AI-RULE-GATE", "S3", "ai", uid, name,
                                  f"rule {i} gate {c['value']} above jutsu range {rng[jid]} + 1 (law 40)",
                                  {"rule": i, "gate": c["value"], "range": rng[jid]}, "Set the gate to range + 1.",
                                  "needs check", hidden=not visible)
            term = set(((db.contracts.get("45g") or {}).get("terminal_actions") or {}).get("values", []))
            if rules and prof.get("includeDefaultRules") is False:
                last = rules[-1]
                if (last.get("conditions") or []) or (last.get("action") or {}).get("type") not in term:
                    F.add("AI-RULE-NO-FALLBACK", "S3", "ai", uid, name,
                          "includeDefaultRules false and the last rule is not an unconditional terminal (law 41)",
                          {"last": last.get("action", {}).get("type")}, "End the chain with move/end_turn/random.",
                          "needs check", hidden=not visible)
    groups = defaultdict(list)
    for uid, a in AI.items():
        if uid in AIN and not a.get("isSummon"):
            lv = a.get("level") or 0
            groups[min(10, (lv - 1) // 10 if lv else 0)].append(dict(a, id=uid, name=a.get("username")))
    for band, rs in groups.items():
        lab = f"non-summon AI, level {band * 10 + 1}-{band * 10 + 10}"
        outliers(F, "OUT-AI-STATSMULT", "ai", [(r, r.get("statsMultiplier") or 0) for r in rs], "statsMultiplier",
                 "Ruling needed on AI strength.", group_label=lab)
        outliers(F, "OUT-AI-POOLSMULT", "ai", [(r, r.get("poolsMultiplier") or 0) for r in rs], "poolsMultiplier",
                 "Ruling needed on AI pools.", group_label=lab)
    dup_names(F, "ai", [dict(r, id=k, name=r.get("username")) for k, r in (AIN or {}).items()], key="username")


def inventory(db, repo_root):
    """Diff live names against answers/names_*.json and harvests/seed/4*_INDEX_*.json."""
    out = {}
    pairs = {"jutsu": ("names_jutsu.json", "40_INDEX_jutsu.json"), "item": ("names_item.json", "41_INDEX_item.json"),
             "ai": ("names_ai.json", "42_INDEX_ai.json"), "asset": ("names_asset.json", "43_INDEX_asset.json"),
             "quest": ("names_quest.json", "47_INDEX_quest.json")}
    for ent, (ans, seed) in pairs.items():
        live = db.names.get(ent)
        if live is None:
            continue
        live_names = {k: (v.get("name") if ent != "ai" else v.get("username")) for k, v in live.items()}
        row = {"live": len(live_names), "fetched_at": db.names_at.get(ent)}
        for label, path, getter in (
                ("answers", os.path.join(repo_root, "answers", ans), lambda d: {r[0]: r[1] for r in d.get("rows", [])}),
                ("seed", os.path.join(repo_root, "harvests", "seed", seed),
                 lambda d: {r[0]: r[1] for r in d.get("rows", [])})):
            if not os.path.exists(path):
                continue
            with open(path, encoding="utf-8") as fh:
                old = getter(json.load(fh))
            new = sorted(set(live_names) - set(old))
            gone = sorted(set(old) - set(live_names))
            renamed = sorted(k for k in set(old) & set(live_names) if (old[k] or "") != (live_names[k] or ""))
            row[label] = {"count": len(old), "new": len(new), "gone": len(gone), "renamed": len(renamed),
                          "gone_list": [(k, old[k]) for k in gone][:50],
                          "renamed_list": [(k, old[k], live_names[k]) for k in renamed][:50],
                          "new_sample": [(k, live_names[k]) for k in new][:15]}
        out[ent] = row
    if db.names.get("bloodline") is not None:
        out["bloodline"] = {"live": len(db.names["bloodline"]), "fetched_at": db.names_at.get("bloodline"),
                            "note": "no answers/seed index exists for bloodlines"}
    return out


def publish_candidates(db):
    """Hidden records that look finished. Information only: publishing is the user's decision."""
    out = []
    for j in db.rec["jutsu"].values():
        if is_hidden(j) and j.get("jutsuType") != "AI" and j.get("image") and j.get("effects") and \
                not PLACEHOLDER_RE.search(strip_html(j.get("description") or "")) and \
                (j.get("description") or "").strip() and not (j.get("name") or "").startswith("New Jutsu"):
            out.append(("jutsu", j["id"], j.get("name"), j.get("jutsuType")))
    for q in db.rec["quest"].values():
        objs = (q.get("content") or {}).get("objectives") or []
        if is_hidden(q) and objs and any(o.get("task") == "win_quest" for o in objs if isinstance(o, dict)) and \
                (q.get("description") or "").strip() and q.get("image"):
            out.append(("quest", q["id"], q.get("name"), q.get("questType")))
    for it in db.rec["item"].values():
        if is_hidden(it) and it.get("image") and (it.get("description") or "").strip() and \
                not PLACEHOLDER_RE.search(it.get("description") or ""):
            out.append(("item", it["id"], it.get("name"), it.get("itemType")))
    for b in db.rec["bloodline"].values():
        if is_hidden(b) and b.get("image") and (b.get("description") or "").strip():
            out.append(("bloodline", b["id"], b.get("name"), b.get("rank")))
    return out


def run_all(db, now_date, repo_root="."):
    F = Findings()
    check_jutsu(F, db)
    check_items(F, db)
    check_quests(F, db, now_date)
    check_bloodlines(F, db)
    check_assets(F, db)
    check_ai(F, db)
    return F


def summarize(F):
    by = Counter((f["severity"], f["code"]) for f in F.items)
    return [{"severity": s, "code": c, "count": n} for (s, c), n in sorted(by.items())]


# ------------------------------------------------------------------ selftest


def selftest():
    import datetime
    good_img = "https://x.ufs.sh/f/good"
    bad_img = "https://x.ufs.sh/f/bad"
    def jutsu(i, **kw):
        base = {"id": i, "name": f"Jutsu {i}", "description": "A real description.", "battleDescription": "%user acts",
                "jutsuType": "NORMAL", "jutsuRank": "C", "actionCostPerc": 60, "cooldown": 3, "chakraCost": 100,
                "staminaCost": 100, "healthCost": 0, "target": "OPPONENT", "hidden": False, "image": good_img,
                "bloodlineId": "", "updatedAt": "2026-10-01T00:00:00Z",
                "effects": [{"type": "damage", "power": 40, "rounds": 0, "calculation": "formula", "target": "INHERIT",
                             "statTypes": ["Highest"], "generalTypes": ["Highest"], "appearSfx": "s1",
                             "appearAnimation": "a1"}]}
        base.update(kw)
        return base
    J = [jutsu(f"j{i}") for i in range(10)]
    J.append(jutsu("jcd", cooldown=90))  # cooldown outlier
    J.append(jutsu("jfx", effects=[{"type": "damage", "power": 40, "calculation": "formula", "target": "INHERIT",
                                    "statTypes": ["Highest"], "generalTypes": [], "appearSfx": "s1",
                                    "appearAnimation": "missing-anim"}]))
    J.append(jutsu("jself", target="SELF", description="placeholder"))
    J.append(jutsu("jdup", name="Jutsu  j1 "))
    J.append(jutsu("jai", jutsuType="AI", hidden=True, range=2, updatedAt="2026-10-15T00:00:00Z"))
    items = [{"id": "i1", "name": "Real Item", "description": "An tusk.", "battleDescription": "x", "itemType": "WEAPON",
              "rarity": "LEGENDARY", "cost": 0, "repsCost": 0, "seichiSilverCost": 0, "hidden": False, "image": bad_img,
              "effects": [{"type": "injectjutsus", "power": 1, "jutsuIds": ["jai", "nope"]}]}]
    assets = [{"id": "a1", "name": "Anim", "type": "ANIMATION", "image": good_img},
              {"id": "s1", "name": "Sfx", "type": "SFX", "image": good_img},
              {"id": "bg", "name": "Bg", "type": "SCENE_BACKGROUND", "image": good_img}]
    def node(i, task, **kw):
        d = {"id": i, "task": task, "image": good_img, "description": "Text."}
        d.update(kw)
        return d
    quests = [
        {"id": "q1", "name": "Broken Quest", "description": "d", "image": good_img, "questType": "story",
         "questRank": "C", "hidden": False, "consecutiveObjectives": False, "requiredLevel": 50, "maxLevel": 40,
         "prerequisiteQuestId": "q2", "retryDelay": "none", "maxCompletes": 1,
         "content": {"sceneBackground": "bg", "sceneCharacters": [], "reward": {"reward_items": [{"ids": ["ghost"]}]},
                     "objectives": [
                         node("d1", "dialog", nextObjectiveId=[{"text": "Go", "nextObjectiveId": "b1"}]),
                         node("b1", "start_battle", opponentAIs=[{"ids": ["missing-ai"], "number": 1}],
                              nextObjectiveId="c1"),
                         node("c1", "collect_item", sectorType="user_village", locationType="specific",
                              longitude=0, latitude=0, collectItemIds=["i1"], nextObjectiveId="w1",
                              sceneBackground="nope-bg"),
                         node("w1", "win_quest"),
                         node("orphan", "dialog", nextObjectiveId=[{"text": "x"}])]}},
        {"id": "q3", "name": "Two Starts", "description": "d", "image": good_img, "questType": "event",
         "questRank": "D", "hidden": True, "consecutiveObjectives": True, "endsAt": "2026-12-01",
         "content": {"sceneBackground": "bg", "reward": {}, "objectives": [
             node("s1", "dialog", nextObjectiveId=[{"text": "a", "nextObjectiveId": "w"}]),
             node("s2", "dialog", nextObjectiveId=[{"text": "b", "nextObjectiveId": "w"}]), node("w", "win_quest")]}},
        {"id": "q2", "name": "Hidden Prereq", "description": "d", "image": good_img, "questType": "story",
         "questRank": "C", "hidden": True, "consecutiveObjectives": True,
         "content": {"objectives": [node("w", "win_quest")], "reward": {}}},
    ]
    ai_names = [{"userId": "ai1", "username": "Grunt", "level": 50, "inArena": True, "avatar": good_img}]
    ai_cap = {"userId": "ai1", "username": "Grunt", "level": 50, "rank": "GENIN", "aiProfileId": "p1",
              "jutsus": [{"jutsuId": "jai", "equipped": True, "updatedAt": "2026-10-01T00:00:00Z"}],
              "items": [{"itemId": "gone-item"}]}
    prof = {"id": "p1", "userId": "ai1", "includeDefaultRules": False,
            "rules": [{"action": {"type": "use_specific_jutsu", "jutsuId": "jai"},
                       "conditions": [{"type": "distance_lower_than", "value": 6}]},
                      {"action": {"type": "use_specific_jutsu", "jutsuId": "not-equipped"}, "conditions": []}]}
    caps_raw = ('{\n  STUDENT: { GENS_CAP: 20000, STATS_CAP: 20000, LVL_CAP: 10 },\n  GENIN: { GENS_CAP: 60000, '
                'STATS_CAP: 60000, LVL_CAP: 30 },\n}')
    with tempfile.TemporaryDirectory() as td:
        def w(name, proc, data):
            with open(os.path.join(td, name), "w") as fh:
                json.dump({"proc": proc, "input": {}, "at": "2026-10-20T00:00:00Z", "data": data}, fh)
        w("j.json", "jutsu.getAll", {"data": J, "nextCursor": None})
        w("i.json", "item.getAll", {"data": items, "nextCursor": None})
        w("a.json", "gameAsset.getAll", {"data": assets, "nextCursor": None})
        w("q.json", "quests.getAll", {"data": quests, "nextCursor": None})
        w("b.json", "bloodline.getAll", {"data": [], "nextCursor": None})
        w("n.json", "profile.getAllAiNames", ai_names)
        with open(os.path.join(td, "bundle.json"), "w") as fh:
            json.dump({"builder": "test", "captures": [
                {"proc": "profile.getAi", "at": "2026-10-10T00:00:00Z", "data": dict(ai_cap, lastIp="1.2.3.4")},
                {"proc": "ai.getAiProfile", "at": "2026-10-10T00:00:00Z", "data": prof}]}, fh)
        db = DB()
        load_paths(db, [td])
        prune_to_live(db)
        db.images = {good_img: {"status": 200, "ctype": "image/webp"}, bad_img: {"status": 404}}
        db.contracts = {"45g": {"formula_tags": {"values": ["damage", "pierce", "wound"]},
                                "terminal_actions": {"values": ["move_towards_opponent", "end_turn", "use_random_jutsu"]}},
                        "45e": {"constants": {"USER_CAPS": {"raw": caps_raw}, "MAX_STATS_CAP": {"value": 1300000}}}}
        F = run_all(db, datetime.date(2026, 10, 20).isoformat())
    got = {(f["code"], f["id"]) for f in F.items}
    expect = [
        ("FX-FORMULA-TYPES", "jfx"), ("FX-COSMETIC-MISSING", "jfx"), ("FX-SELF-HARM", "jself"),
        ("TXT-PLACEHOLDER", "jself"), ("TXT-NAME-SPACE", "jdup"), ("NAME-NEAR-DUP", "j1"),
        ("OUT-JUTSU-COOLDOWN", "jcd"), ("ITEM-NO-COST", "i1"), ("REF-ITEM-INJECT", "i1"),
        ("ITEM-INJECT-UNUSABLE", "i1"), ("IMG-BROKEN", "i1"), ("TXT-ARTICLE", "i1"),
        ("QUEST-NOT-CONSECUTIVE", "q1"), ("QUEST-LEVEL-WINDOW", "q1"), ("VIS-QUEST-PREREQ-HIDDEN", "q1"),
        ("REF-REWARD", "q1"), ("REF-QUEST-AI", "q1"), ("QUEST-BATTLE-NO-FAIL", "q1"), ("QUEST-LOC-ORIGIN", "q1"),
        ("REF-SCENE-BG", "q1"), ("QUEST-FLOW-STARTS", "q3"), ("QUEST-CHOICE-DEAD-END", "q1"),
        ("AI-RANK-LVLCAP", "ai1"), ("AI-STALE-EQUIP-UNCONFIRMED", "ai1"), ("REF-AI-ITEM", "ai1"), ("AI-RULE-UNEQUIPPED", "ai1"),
        ("AI-RULE-GATE", "ai1"), ("AI-RULE-NO-FALLBACK", "ai1"),
    ]
    missing = [e for e in expect if e not in got]
    clean = [f for f in F.items if f["id"] in {f"j{i}" for i in range(10)} - {"j1"}]
    leaked = "lastIp" in json.dumps(db.rec["ai"])
    ok = not missing and not clean and not leaked
    for e in expect:
        print(("PASS " if e in got else "FAIL ") + "%s on %s" % e)
    print(("PASS" if not clean else "FAIL") + f" no findings on clean controls ({len(clean)})")
    print(("PASS" if not leaked else "FAIL") + " player-account fields stripped from AI captures")
    print(f"{len(expect) + 2 - len(missing) - bool(clean) - leaked} passed, "
          f"{len(missing) + bool(clean) + leaked} failed")
    return 0 if ok else 1


# ------------------------------------------------------------------ main


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--selftest", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    c = sub.add_parser("check")
    c.add_argument("paths", nargs="+")
    c.add_argument("--captures", action="append", default=[], help="extra capture folders/bundles (e.g. harvests/inbox)")
    c.add_argument("--images", help="JSON map url -> {status, ctype}")
    c.add_argument("--contracts", default=".", help="repo root holding 45c/45g (and skill data/ 45d/45e)")
    c.add_argument("--now", help="YYYY-MM-DD used for expiry checks (default: today UTC)")
    c.add_argument("--json", help="write findings JSON here")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.cmd != "check":
        ap.print_help()
        return 2
    import datetime
    db = DB()
    load_paths(db, a.paths + a.captures)
    prune_to_live(db)
    load_contracts(db, a.contracts)
    if a.images:
        with open(a.images, encoding="utf-8") as fh:
            db.images = json.load(fh)
    now = a.now or datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    F = run_all(db, now, a.contracts)
    counts = {e: len(v) for e, v in db.rec.items()}
    print("records:", json.dumps(counts))
    print("names:", json.dumps({e: len(v) for e, v in db.names.items()}))
    for row in summarize(F):
        print(f"{row['severity']} {SEVERITY[row['severity']]:<20} {row['code']:<30} {row['count']}")
    print(f"total findings: {len(F.items)}")
    if a.json:
        out = {"records": counts, "names": {e: len(v) for e, v in db.names.items()}, "names_at": db.names_at,
               "sources": dict(db.sources), "inventory": inventory(db, a.contracts),
               "publish_candidates": publish_candidates(db), "summary": summarize(F), "findings": F.items}
        with open(a.json, "w", encoding="utf-8") as fh:
            json.dump(out, fh, indent=1, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    sys.exit(main())
