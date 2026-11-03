#!/usr/bin/env python3
"""The Mother of Echoes (the Skyglass uber, RUL-2026-11-01-093..096, -097, -099..103): build manifests from the
offline-tested spec on fable/mother-of-echoes-sim.

    python3 push/mother_of_echoes.gen.py
        -> push/440_mother_of_echoes_jutsu.json        (HIDDEN creates: every new jutsu that names no AI)
    python3 push/mother_of_echoes.gen.py --step templates --bundles <440 bundle>
        -> push/461_mother_of_echoes_templates.json    (HIDDEN creates: the 5 summon-template AIs)
    python3 push/mother_of_echoes.gen.py --step summons --bundles <440> <461>
        -> push/462_mother_of_echoes_summons.json      (HIDDEN creates: the 6 summon jutsu, aiId literal)
    python3 push/mother_of_echoes.gen.py --step bosses --bundles <440> <461> <462>
        -> push/463_mother_of_echoes_bosses.json       (HIDDEN creates: the 4 boss AIs, inArena false)
    python3 push/mother_of_echoes.gen.py --step quest --bundles <440, 461-463> --economy <417>
        -> push/464_mother_of_echoes_quest.json        (the HIDDEN battle pyramid, one repeatable quest)
    python3 push/mother_of_echoes.gen.py --step publish --bundles <440, 461-464> --economy <417>
        -> push/465_mother_of_echoes_publish.json      (the quest re-sent whole with hidden false)

Every step after 440 needs literal ids from earlier results bundles (law 17, ID provenance law): AI equip arrays and
rule jutsuIds, summon aiIds and quest opponentAIs / entry items / rewards. `--bundles` takes any number of results
bundles; ids are read from their `entries` (create, state ok) and `idmap`, only for this generator's srcIds, and every
id a step needs must be present or the step refuses. `--economy` is push/417's results bundle (the four shards, the
Heartglass and The Remainder tokens).

Source of truth: harness/skyglass_wreck_sim/mother_of_echoes_spec.json at SPEC_REF (pinned below and in every
manifest's _note). The spec is read with `git show`, so fetch fable/mother-of-echoes-sim first. Records are taken as
the harness ran them (theninjarpg@3314d122 JutsuValidator / AiRule / insertAiSchema valid); this generator only
(1) drops harness-only keys, (2) maps art names to live asset ids or placeholders, (3) maps harness ids (moe-*) to
srcIds or literal ids, (4) refuses repeated display names (the game has unique name indexes on jutsu and AI usernames).

Do not hand-edit the outputs.
"""
import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC_REF = "dd7e33ab9abfc96ae1630177ea1bc386729b2c8f"  # fable/mother-of-echoes-sim commit holding the final spec (pass 4)
SPEC_PATH = "harness/skyglass_wreck_sim/mother_of_echoes_spec.json"
PFX = "sg440_"
ECON = "sg417_"
# 441 was taken by a concurrent session (push/441_dusk_dawn_variants.json); later steps use 461-465.
N = {"jutsu": 440, "templates": 461, "summons": 462, "bosses": 463, "quest": 464, "publish": 465}
SLUG = {"jutsu": "mother_of_echoes_jutsu", "templates": "mother_of_echoes_templates",
        "summons": "mother_of_echoes_summons", "bosses": "mother_of_echoes_bosses",
        "quest": "mother_of_echoes_quest", "publish": "mother_of_echoes_publish"}

PLACEHOLDER = "https://uploadthing.b-cdn.net/f/630cf6e7-c152-4dea-a3ff-821de76d7f5a_default.webp"  # engine default (45e)
CORE_CHAMBER = "81DATu13hATfbkPuLT54E"  # scene asset reconstruction_chamber (push/339), placeholder scene
BLANK = "1YXbXYW2wz3GETVMb6DT6"  # Blank Scene Character (push/383-385 publish rule)
STOLEN_FORM = "VuFuBtE7h5B1nnA2J1lFZ"  # live, reused as-is (34 holders; never edited)
HEAVY_ARMOR = "h-V9uiuxbL7lAWkO6nZWt"  # AI Heavy Armor (live item)
ENGINE_ACTIONS = {"basicAttack", "wait"}  # built-in action ids a rule may name (no record)

# Live Skyglass danger-language art (push/431, RUL-2026-11-02-101): field -> asset id. Marks ride the
# increaseregeneration carrier; pool art sits on the lasting effect (no disappear animation).
APPEAR, VANISH = "bJy2IjRKmAVYEoXUYmXv5", "k8J4ic-KEz9ewEq1gAszr"
TG = {
    "tg_heavy": {"staticAssetPath": "dGCN9ZaoyXwDK9E3ZuWgU", "staticAnimation": "dL1vh_PNbZQ9m6nYwGnFa",
                 "appearAnimation": APPEAR, "disappearAnimation": VANISH},
    "tg_control": {"staticAssetPath": "M2oqurvH5jYkuCeDafnFK", "staticAnimation": "ZZ2YrtIAxfnlHAzOHXSgl",
                   "appearAnimation": APPEAR, "disappearAnimation": VANISH},
    "tg_safe": {"staticAssetPath": "-hIV18piGe0EcC0u6eN8d", "staticAnimation": "v9nA0cPU5NXxBXoONhdLH",
                "appearAnimation": APPEAR, "disappearAnimation": VANISH},
    "tg_linger": {"staticAssetPath": "PoG_KDERWlvyj7MsKSDW2", "staticAnimation": "qlGYJizxxxdd794Jea6lB",
                  "appearAnimation": APPEAR, "disappearAnimation": ""},
}
# tg_etch has no live art yet: the Etching marks borrow the violet control tile so they stay readable (RUL-101 item 3).
TG_STANDIN = {"tg_etch": "tg_control"}
ART_FIELDS = ("staticAssetPath", "staticAnimation", "appearAnimation", "disappearAnimation")
LIVE_ID = re.compile(r"^[A-Za-z0-9_-]{10,21}$")
DROP_KEYS = {"id", "createdAt", "updatedAt"}


# Rewards (RUL-2026-11-01-095 item 2 as amended by RUL-2026-11-02-100, -104 (no Salvage) and -105 (no first-clear
# mechanics, no title; every clear rolls both tradeable tokens)): pick ids by name from verified bundles.
CROWNS_HOARD = "WrnHlt3h6ZDjFaJk3i41O"   # harvests/inbox/tnr_results_1793491854510.json (unhide, verified)
SKYGLASS_COFFER = "THo7rfzP-S82_43aN8fs3"  # harvests/inbox/tnr_results_1793491854510.json
SKYGLASS_TOKEN = "nzCW7A-_AuYMzBs2wClnM"   # harvests/inbox/tnr_results_1793424666625.json
PICK = [(CROWNS_HOARD, 2), (SKYGLASS_COFFER, 5), (SKYGLASS_TOKEN, 2)]
TOKEN_PCT = {"heartglass": 25, "remainder": 25}  # PLACEHOLDER rates (RUL-2026-11-02-105), reversible
# PLACEHOLDER (RUL-105: the director sets exp and ryo; Crownhold's win pays reward_exp 5000 and no ryo).
REWARD_EXP = 7500
REWARD_MONEY = 0

Q_NAME = "The Mother of Echoes"


def die(msg):
    sys.exit(f"mother_of_echoes.gen.py: {msg}")


# ---------------------------------------------------------------------------------------------------------------
# Spec
# ---------------------------------------------------------------------------------------------------------------
def load_spec():
    if not re.fullmatch(r"[0-9a-f]{40}", SPEC_REF):
        die("SPEC_REF is not pinned to a fable/mother-of-echoes-sim commit")
    try:
        raw = subprocess.check_output(["git", "-C", ROOT, "show", f"{SPEC_REF}:{SPEC_PATH}"], stderr=subprocess.PIPE)
    except subprocess.CalledProcessError:
        die(f"cannot read {SPEC_PATH} at {SPEC_REF}; run: git fetch origin fable/mother-of-echoes-sim")
    spec = json.loads(raw)
    if not str(spec.get("validation", "")).startswith("valid"):
        die(f"the spec at {SPEC_REF} does not validate: {spec.get('validation')}")
    return spec


def sid(hid):
    """Harness id -> srcId (moe-glass-lancet -> sg440_glass_lancet; moe-ai-sayo -> sg440_ai_sayo)."""
    if not hid.startswith("moe-"):
        die(f"not a harness id: {hid}")
    return PFX + hid[4:].replace("-", "_")


def unique_names(rows, key):
    """The game keeps jutsu names and AI usernames unique (theninjarpg@3314d122 drizzle/schema.ts Jutsu_name_key,
    UserData_username_key). Names come from the spec only (RUL-2026-11-02-105: proper names, no numbered
    placeholders), so a repeated name refuses the build instead of being suffixed."""
    out, seen = {}, {}
    for r in rows:
        name = key(r)
        if name in seen:
            die(f"name {name!r} is used by both {seen[name]} and {r['id']}; name them in the spec (FINAL_TEXT)")
        seen[name] = r["id"]
        out[r["id"]] = name
    return out


class Build:
    def __init__(self, spec):
        self.spec = spec
        self.jutsu = {j["id"]: j for j in spec["jutsu"]}
        self.ais = {a["id"]: a for a in spec["ais"]}
        self.jname = unique_names(spec["jutsu"], lambda j: j["record"]["name"])
        self.aname = unique_names(spec["ais"], lambda a: a["username"])
        self.notes = []
        summon = {jid for jid, j in self.jutsu.items() if any(e.get("aiId") for e in j["record"]["effects"])}
        self.summon_jutsu = [jid for jid in self.jutsu if jid in summon]
        self.plain_jutsu = [jid for jid in self.jutsu if jid not in summon]
        self.templates = [a["id"] for a in spec["ais"] if a["summonTemplate"]]
        self.bosses = [a["id"] for a in spec["ais"] if not a["summonTemplate"]]

    # ---- jutsu -----------------------------------------------------------------------------------------------
    def art(self, label, eff):
        e = dict(eff)
        for f in ART_FIELDS:
            v = e.get(f) or ""
            if v in TG_STANDIN:
                e[f] = TG[TG_STANDIN[v]][f]
                self.notes.append(f"{label}: effects[{e['type']}] art {v} (no live art yet; the {TG_STANDIN[v]} tile stands in)")
            elif v in TG:
                e[f] = TG[v][f]
            elif v.startswith("moe_"):
                e[f] = ""
                self.notes.append(f"{label}: effects[{e['type']}] art {v} (art pending; left empty)")
            elif v and not LIVE_ID.match(v):
                die(f"{label}: unknown art name {v!r} in {f}")
        return e

    def jutsu_data(self, jid, ids=None):
        rec = self.jutsu[jid]["record"]
        name = self.jname[jid]
        d = {k: v for k, v in rec.items() if k not in DROP_KEYS and v is not None}
        d["name"] = name
        d["hidden"] = True
        d["image"] = PLACEHOLDER
        self.notes.append(f"jutsu {sid(jid)}: {name} (engine default image)")
        d["effects"] = [self.art(name, e) for e in rec["effects"]]
        for e in d["effects"]:
            if e.get("aiId"):
                if ids is None:
                    die(f"{jid} names an AI; it is built by --step summons")
                e["aiId"] = ids[sid(e["aiId"])]
        return d

    def jutsu_entry(self, jid, ids=None):
        return {"entity": "jutsu", "slot": "create", "srcId": sid(jid), "phase": 1, "name": self.jname[jid],
                "data": self.jutsu_data(jid, ids)}

    # ---- AI --------------------------------------------------------------------------------------------------
    def lit(self, hid, ids):
        if hid == STOLEN_FORM or hid in ENGINE_ACTIONS:
            return hid
        k = sid(hid)
        if k not in ids:
            die(f"no created id for {hid} ({k}) in the bundles given")
        return ids[k]

    def ai_entry(self, aid, ids):
        a = self.ais[aid]
        d = json.loads(json.dumps(a["create"]))
        d["username"] = self.aname[aid]
        d["avatar"] = PLACEHOLDER
        d["inArena"] = False
        d["hidden"] = True
        d["jutsus"] = [self.lit(j, ids) for j in d["jutsus"]]
        for r in d["rules"]:
            act = r["action"]
            if act.get("jutsuId"):
                act["jutsuId"] = self.lit(act["jutsuId"], ids)
            if act.get("comboIds"):
                act["comboIds"] = [self.lit(j, ids) for j in act["comboIds"]]
        left = sorted(set(re.findall(r'"(moe-[a-z0-9-]+)"', json.dumps(d))))
        if left:
            die(f"{aid}: unresolved harness ids {left}")
        for it in d["items"]:
            if it["ids"] != [HEAVY_ARMOR]:
                die(f"{aid}: unexpected item {it}")
        self.notes.append(f"ai {sid(aid)}: {d['username']} (engine default image as avatar)")
        return {"entity": "ai", "slot": "create", "srcId": sid(aid), "phase": 1, "name": d["username"], "data": d}


# ---------------------------------------------------------------------------------------------------------------
# Bundles
# ---------------------------------------------------------------------------------------------------------------
def created(paths, prefix):
    got = {}
    for p in paths or []:
        b = json.load(open(p))
        for e in b.get("entries") or []:
            s = e.get("srcId") or ""
            if e.get("slot") == "create" and e.get("state") == "ok" and e.get("id") and s.startswith(prefix):
                got[s] = e["id"]
        for k, v in (b.get("idmap") or {}).items():
            if k.startswith(prefix):
                got.setdefault(k, v)
    return got


def need(ids, keys, what):
    miss = sorted(k for k in keys if k not in ids)
    if miss:
        die(f"{what}: the bundles given lack {miss}")


# ---------------------------------------------------------------------------------------------------------------
# Quest (444) and publish (445)
# ---------------------------------------------------------------------------------------------------------------
Q_DESC = ("The four shards are her invitation. Carry one of each (Keel, Crown, Tide and Ledger) to the Mother Glass "
          "under Crownhold; all four are spent when the fight begins.\n\n"
          "Three battles, one after another. Health, chakra and stamina carry from each battle to the next, with no "
          "refills. Lose any battle and the attempt ends; the shards are not returned.\n\n"
          "Watch the floor. Every mark she draws is a warning, and every warning comes due.\n\n"
          "If you still have a reward to choose from an earlier attempt, claim it before you start.")
Q_SUCCESS = "The Mother Glass cracks from the root to the crown. Choose your reward."
LOSS = {"failDescription": "The glass goes quiet around you. The shards are spent.",
        "drawDescription": "The glass goes quiet around you. The shards are spent.",
        "fleeDescription": "You back out of the hall. The shards stay in the glass."}
F_LOST = "The glass keeps what it was given. Find four more shards and come back."


def quest_data(b, ids, econ):
    q = b.spec["quest"]
    obj = {o["n"]: o for o in q["objectives"]}
    sc = {"sceneBackground": CORE_CHAMBER, "sceneCharacters": []}

    def battle(oid, n, nxt):
        o = obj[n]
        return {"id": oid, "task": "start_battle", "description": o["title"], **sc,
                "opponentAIs": [{"ids": [ids[sid(a)]], "number": 1, "quantity": 1} for a in o["opponents"]],
                "completionOutcome": "Win", "scaleGains": 1, "keepOriginalPools": False,
                "opponent_scaled_to_user": False, "nextObjectiveId": nxt, "failObjectiveId": "f_lost", **LOSS}

    def dialog(oid, n, nxt, label):
        return {"id": oid, "task": "dialog", "description": obj[n]["text"], **sc,
                "nextObjectiveId": [{"text": label, "nextObjectiveId": nxt}]}

    win = {"id": "w_clear", "task": "win_quest", "description": obj[6]["text"], **sc, "reward_exp": REWARD_EXP}
    if REWARD_MONEY:
        win["reward_money"] = REWARD_MONEY
    win["reward_items"] = [{"ids": [econ[ECON + k]], "number": pct, "quantity": 1} for k, pct in TOKEN_PCT.items()]
    objs = [dialog("d_open", 0, "b_act1", "Step into the hall"),
            battle("b_act1", 1, "d_act2"), dialog("d_act2", 2, "b_act2", "Hold your ground"),
            battle("b_act2", 3, "d_act3"), dialog("d_act3", 4, "b_act3", "Do not hold still"),
            battle("b_act3", 5, "w_clear"), win,
            {"id": "f_lost", "task": "fail_quest", "description": F_LOST, **sc}]
    entry = [{"ids": [econ[ECON + k]], "number": 1} for k in ("keel", "crown", "tide", "ledger")]
    return {"name": Q_NAME, "description": Q_DESC, "successDescription": Q_SUCCESS,
            "image": PLACEHOLDER, "questType": "battlepyramid", "questRank": "S", "hidden": True,
            "retryDelay": "none", "attemptDelay": "none", "consecutiveObjectives": True, "requiredLevel": 1,
            "maxLevel": 100, "maxAttempts": 100, "maxCompletes": 100,
            "prerequisiteQuestId": None, "tierLevel": None, "requiredVillage": None, "requiredBloodlineId": None,
            "startsAt": None, "endsAt": None,
            "content": {"objectives": objs, "sceneBackground": CORE_CHAMBER, "sceneCharacters": [BLANK],
                        "entryItems": entry, "isolated": True, "rewardMode": "choose", "rewardPickCount": 1,
                        "reward": {"reward_items": [{"ids": [i], "number": 100, "quantity": n} for i, n in PICK]}}}


# ---------------------------------------------------------------------------------------------------------------
# Output
# ---------------------------------------------------------------------------------------------------------------
def write(step, note, items, notes=None):
    m = {"_note": f"{note} Spec: fable/mother-of-echoes-sim@{SPEC_REF}:{SPEC_PATH}. "
                  "Generated by push/mother_of_echoes.gen.py; do not hand-edit.",
         "dedupNames": True}
    if notes:
        m["_placeholders"] = sorted(set(notes))
    m["items"] = items
    path = os.path.join(ROOT, f"push/{N[step]}_{SLUG[step]}.json")
    with open(path, "w") as f:
        json.dump(m, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"push/{N[step]}_{SLUG[step]}.json: {len(items)} items")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--step", choices=["jutsu", "templates", "summons", "bosses", "quest", "publish"], default="jutsu")
    ap.add_argument("--bundles", nargs="*", default=[], help="results bundles of 440-444 (any order)")
    ap.add_argument("--economy", help="push/417 results bundle (the shards, Heartglass and The Remainder tokens)")
    a = ap.parse_args()
    b = Build(load_spec())
    ids = created(a.bundles, PFX)

    if a.step == "jutsu":
        items = [b.jutsu_entry(j) for j in b.plain_jutsu]
        write("jutsu", (
            f"push/440 (RUL-2026-11-02-103 part 2), all HIDDEN: the {len(items)} new Mother of Echoes jutsu that name no "
            f"AI (the {len(b.summon_jutsu)} summon jutsu come in push/442 with literal aiIds; Stolen Form "
            f"{STOLEN_FORM} is reused live, not created). No earlier ids needed. Telegraph marks ride the "
            "increaseregeneration carrier with the live Skyglass tiles (push/431); pool art on the lasting effect."),
            items, b.notes)
    elif a.step == "templates":
        need(ids, [sid(j) for j in b.plain_jutsu], "templates")
        items = [b.ai_entry(t, ids) for t in b.templates]
        write("templates", f"push/441 (from push/440's bundle; literal ids, law 17): the {len(items)} summon-template "
              "AIs, plain AI rows (the engine marks the summoned unit). No hidden column on AI records (law 16b); "
              "inArena false, referenced only by push/442's summon jutsu.", items, b.notes)
    elif a.step == "summons":
        need(ids, [sid(t) for t in b.templates], "summons")
        items = [b.jutsu_entry(j, ids) for j in b.summon_jutsu]
        write("summons", f"push/442 (from push/441's bundle; literal aiIds, law 17), all HIDDEN: the {len(items)} "
              "summon jutsu.", items, b.notes)
    elif a.step == "bosses":
        need(ids, [sid(j) for j in b.plain_jutsu + b.summon_jutsu], "bosses")
        items = [b.ai_entry(t, ids) for t in b.bosses]
        write("bosses", f"push/443 (from push/440 and 442's bundles; literal ids, law 17): the {len(items)} boss AIs "
              f"with AI Heavy Armor ({HEAVY_ARMOR}), inArena false. Fresh creates, equipped once (law 18: any later "
              "edit to an equipped moe jutsu is unequip, edit, re-equip).", items, b.notes)
    elif a.step in ("quest", "publish"):
        econ = created([a.economy] if a.economy else [], ECON)
        need(econ, [ECON + k for k in ("keel", "crown", "tide", "ledger", *TOKEN_PCT)], "--economy (push/417)")
        need(ids, [sid(t) for t in b.bosses], a.step)
        d = quest_data(b, ids, econ)
        notes = [f"quest {PFX}quest: image and every node's scene {CORE_CHAMBER}",
                 f"quest {PFX}quest: reward_exp {REWARD_EXP}, reward_money {REWARD_MONEY} (director to set, RUL-2026-11-02-105)"]
        notes += [f"quest {PFX}quest: {k} token {pct}% per clear (reversible placeholder rate, RUL-2026-11-02-105)"
                  for k, pct in TOKEN_PCT.items()]
        if a.step == "quest":
            write("quest", "push/444 (literal ids from push/417 and 440-443, law 17): the HIDDEN battle pyramid, one "
                  "repeatable quest (RUL-2026-11-02-105: no first-clear mechanics, no title). Every clear rolls the "
                  "Heartglass and The Remainder tokens (both tradeable) and a pick of one reward.",
                  [{"entity": "quest", "slot": "create", "srcId": PFX + "quest", "phase": 1, "name": Q_NAME, "data": d}],
                  notes)
        else:
            need(ids, [PFX + "quest"], "publish")
            d["hidden"] = False
            write("publish", "push/445 (literal ids): the quest re-sent whole with hidden false (quest edits are "
                  "full-record). The jutsu stay hidden (AIs use hidden jutsu; law 18). Run after push/419.",
                  [{"entity": "quest", "slot": "edit", "targetId": ids[PFX + "quest"], "name": f"{Q_NAME}: publish",
                    "data": d}], notes)


if __name__ == "__main__":
    main()
