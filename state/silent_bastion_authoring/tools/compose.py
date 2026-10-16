#!/usr/bin/env python3
"""Deterministic offline composer for the Silent Bastion authoring package.

Inputs (all committed): the selected graph named by state/silent_bastion_approved_authoring_lock.json
(sha256-verified), design/{script,regulars,commanders,protocols,entry_and_rewards}.json and
sources/source_records.json. Outputs (compiled/): quest.candidate.json, ai_profiles.candidate.json,
encounter_ledger.json, story_script.md. Symbolic refs (@ai:<slot>, @item:<key>, @jutsu:<code>) stay
symbolic — this is NOT a live manifest and is never written under push/.

    python3 tools/compose.py          # write compiled/
    python3 tools/compose.py --check  # fail if compiled/ is stale or any structural rule breaks
"""
import hashlib, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, ".."))
REPO = os.path.abspath(os.path.join(ROOT, "../.."))
LOCK = "state/silent_bastion_approved_authoring_lock.json"
OUTD = os.path.join(ROOT, "compiled")
# Display order of puzzle answers per division (graph order is correct-first; never show that).
PUZZLE_ORDER = {2: ["wrong_a", "correct", "wrong_b"], 3: ["wrong_b", "wrong_a", "correct"],
                4: ["wrong_a", "correct", "wrong_b"], 5: ["correct", "wrong_b", "wrong_a"]}
# Display order maps to the script's option labels: correct→clean, wrong_*→alert.

def j(p):
    return json.load(open(os.path.join(REPO, p) if not os.path.isabs(p) else p))

def sha(p):
    return hashlib.sha256(open(os.path.join(REPO, p), "rb").read()).hexdigest()

def fail(msg):
    sys.exit(f"compose: {msg}")

def load():
    lock = j(LOCK)
    gp = lock["selectedGraph"]["path"]
    if sha(gp) != lock["selectedGraph"]["rawSha256"]:
        fail(f"{gp} sha256 does not match the coordination lock")
    g = j(gp)
    if len(g["nodes"]) != lock["selectedGraph"]["counts"]["objectives"]:
        fail("graph node count differs from lock")
    a = "state/silent_bastion_authoring/"
    return lock, gp, g, j(a + "design/script.json"), j(a + "design/regulars.json"), j(a + "design/commanders.json"), \
        j(a + "design/protocols.json"), j(a + "design/entry_and_rewards.json"), j(a + "sources/source_records.json")

def dsl_rule(r, sources):
    conds = []
    for c in r["if"]:
        op = c[0]
        if op == "hp<": conds.append({"type": "health_below", "value": c[1]})
        elif op == "round<": conds.append({"type": "round_lower_than", "value": c[1]})
        elif op == "round>": conds.append({"type": "round_greater_than", "value": c[1]})
        elif op == "round=": conds.append({"type": "specific_round", "value": c[1]})
        elif op == "dist<=": conds.append({"type": "distance_lower_than", "value": c[1], "target": "CLOSEST_OPPONENT"})
        elif op == "dist>=": conds.append({"type": "distance_higher_than", "value": c[1], "target": "CLOSEST_OPPONENT"})
        elif op == "self": conds.append({"type": "has_effect", "effectType": c[1], "threshold": c[2]})
        elif op == "target": conds.append({"type": "target_has_effect", "effectType": c[1], "threshold": c[2], "target": "CLOSEST_OPPONENT"})
        else: fail(f"unknown condition {op}")
    kind = r["do"][0]
    if kind == "jutsu":
        code = r["do"][1]
        jid = f"@jutsu:{code[2:].lower()}" if code.startswith("X:") else sources["jutsu"][code]["id"]
        act = {"type": "use_specific_jutsu", "jutsuId": jid, "target": r["do"][2]}
    elif kind == "item":
        key = r["do"][1]
        iid = f"@item:{key[2:].lower()}" if key.startswith("X:") else sources["seedItems"]["records"][key[5:]]["id"]
        act = {"type": "use_specific_item", "itemId": iid, "target": r["do"][2]}
    elif kind == "move": act = {"type": "move_towards_opponent", "target": "CLOSEST_OPPONENT"}
    elif kind == "end": act = {"type": "end_turn"}
    else: fail(f"unknown action {kind}")
    return {"conditions": conds, "action": act, "source": r["src"]}

def html(text):
    """Quest node text renders as HTML (validate.py): paragraphs and line breaks become <br>."""
    return text.replace("\n", "<br>")

def compose():
    lock, gp, g, script, regs, cmds, prot, entry, sources = load()
    units = {u["slot"]: u for u in regs["units"] + cmds["units"]}
    sym = {n["id"]: n for n in g["nodes"]}
    obj_text = script["objectives"]
    if set(obj_text) != set(sym):
        fail(f"script ids differ from graph: {sorted(set(obj_text) ^ set(sym))}")
    eff = {"SECURITY_ALERT_TBD": prot["securityAlert"]["effect"]}
    for d in (2, 3, 4, 5):
        eff[f"COMBAT_PROTOCOL_D{d}_TBD"] = prot["combat"][f"D{d}"]["effect"]
    objectives = []
    for n in g["nodes"]:
        t = obj_text[n["id"]]
        k = n["kind"]
        if k == "dialog":
            if n.get("next"):
                opts = [{"text": "Continue", "nextObjectiveId": n["next"]}]
            elif n["id"].endswith(".puzzle"):
                d = int(n["id"][1])
                by = {c["label"]: c["to"] for c in n["choices"]}
                opts = [{"text": t["options"][lab], "nextObjectiveId": by[lab]} for lab in PUZZLE_ORDER[d]]
            else:
                opts = [{"text": t["options"][c["to"]], "nextObjectiveId": c["to"]} for c in n["choices"]]
            if not t["text"].strip() or any(not o["text"].strip() for o in opts):
                fail(f"{n['id']}: empty dialog text")
            objectives.append({"id": n["id"], "task": "dialog", "description": html(f"<b>{t['title']}</b>\n\n{t['text']}"), "nextObjectiveId": opts})
        elif k == "battle":
            o = {"id": n["id"], "task": "start_battle", "description": t["text"],
                 "opponentAIs": [{"ids": [f"@ai:{n['encounterSlot']}"], "number": 1}],
                 "nextObjectiveId": n["onWin"], "failObjectiveId": n["onLoss"]}
            if "startPoolsPercent" in n: o["givePools"] = n["startPoolsPercent"]
            if n["id"] in entry["battleIncome"]["scaleGains"]["appliesTo"]:
                o["scaleGains"] = entry["battleIncome"]["scaleGains"]["recoveryBattles"]
            if n.get("startEffect"):
                e = eff[n["startEffect"]]
                o["applyBuffs" if e["kind"] == "buff" else "applyDebuffs"] = [dict(e["tag"])]
            if not t["text"].strip():
                fail(f"{n['id']}: empty battle text")
            objectives.append(o)
        elif k == "reset":
            objectives.append({"id": n["id"], "task": "reset_quest", "resetObjectiveId": n.get("resetTarget") or n.get("resetTo")})
        elif k == "win":
            objectives.append({"id": n["id"], "task": "win_quest", "description": t["text"]})
        elif k == "fail":
            objectives.append({"id": n["id"], "task": "fail_quest", "description": t["text"]})
    q = entry["quest"]
    quest = {
        "status": "OFFLINE PACKAGE — not a manifest; symbolic refs; values and wording accepted (RUL-2026-10-16-004..012) except art, cache/Beacon rarity and cache names; never push/",
        "provenance": {"graph": gp, "graphSha256": lock["selectedGraph"]["rawSha256"], "lock": LOCK, "lockSha256": sha(LOCK),
                       "ruling": lock["selectedGraph"]["directorSelectionRuling"]},
        "record": {
            "name": script["quest"]["name"], "description": html(script["quest"]["description"]),
            "successDescription": script["quest"]["successDescription"], "questType": q["questType"],
            "hidden": q["hidden"], "consecutiveObjectives": q["consecutiveObjectives"],
            "maxAttempts": q["maxAttempts"]["value"], "maxCompletes": q["maxCompletes"]["value"],
            "tierLevel": None, "startsAt": None, "endsAt": None,
            "content": {
                "isolated": q["isolated"], "entryItems": q["entryItems"], "rewardMode": q["rewardMode"],
                "rewardPickCount": q["rewardPickCount"], "reward": entry["caches"]["questReward"],
                "objectives": objectives, "sceneBackground": q["sceneBackground"]["value"], "sceneCharacters": [],
            },
        },
    }
    ledger, profiles = [], []
    for slot in sorted(units):
        u = units[slot]
        battles = [n["id"] for n in g["nodes"] if n["kind"] == "battle" and n["encounterSlot"] == slot]
        ledger.append({"slot": slot, "ref": f"@ai:{slot}", "key": u["key"], "name": u["name"],
                       "role": "Commander" if slot.endswith("BOSS") else u.get("role"),
                       "battleObjectives": battles,
                       "kit": [{"code": c, "id": (f"@jutsu:{c[2:].lower()}" if c.startswith("X:") else sources["jutsu"][c]["id"]),
                                "name": (cmds["exclusives"][c]["record"]["name"] if c.startswith("X:") else sources["jutsu"][c]["name"]),
                                "provenance": ("CANDIDATE exclusive" if c.startswith("X:") else sources["jutsu"][c]["provenance"]["capture"])} for c in u["kit"]],
                       "items": u["items"]})
        profiles.append({"slot": slot, "ref": f"@ai:{slot}", "key": u["key"], "name": u["name"],
                         "status": u.get("aiStatus") or u.get("status"), "kitStatus": u.get("kitStatus", "NEW CANDIDATE"),
                         "record": {**u["candidate"], "jutsus": [x["id"] for x in ledger[-1]["kit"]],
                                    "items": [{"ids": [f"@item:{k[2:].lower()}" if k.startswith("X:") else sources["seedItems"]["records"][k[5:]]["id"]], "number": 0} for k in u["items"]],
                                    "effects": [{k: v for k, v in e.items() if k != "status"} for e in u["innate"]]},
                         "aiProfile": {"includeDefaultRules": False, "rules": [dsl_rule(r, sources) for r in u["rules"]]}})
    for p in profiles:
        if len(p["aiProfile"]["rules"]) > 20:
            fail(f"{p['key']}: {len(p['aiProfile']['rules'])} rules > 20")
        last = p["aiProfile"]["rules"][-1]
        if last["conditions"] or last["action"]["type"] != "end_turn":
            fail(f"{p['key']}: last rule must be unconditional end_turn")
    # Readable story script keyed to every objective id.
    md = [f"# {script['quest']['name']} — story script", "",
          "Generated by `state/silent_bastion_authoring/tools/compose.py` from `design/script.json`; keyed to all 99 objective ids of `alt99_f4gate`. Reset objectives are silent by design. Accepted as launch copy (RUL-2026-10-16-011).", "",
          "## Quest", "", f"**Description.** {script['quest']['description']}", "", f"**Success.** {script['quest']['successDescription']}", ""]
    cur = None
    for o in objectives:
        t = obj_text[o["id"]]
        div = t.get("division")
        if div and div != cur:
            md += [f"## {div}", ""]; cur = div
        if o["task"] == "dialog":
            md += [f"### `{o['id']}` — {t['title']}", "", t["text"], ""]
            if len(o["nextObjectiveId"]) > 1:
                md += [f"- *{x['text']}* → `{x['nextObjectiveId']}`" for x in o["nextObjectiveId"]] + [""]
            if t.get("logic"):
                md += [f"> Puzzle logic: {t['logic']}", ""]
        elif o["task"] == "start_battle":
            extra = []
            if "givePools" in o: extra.append(f"pools set to {o['givePools']}%")
            for f in ("applyBuffs", "applyDebuffs"):
                for e in o.get(f, []): extra.append(f"player {e['type']} {e.get('power', '')}/{e.get('rounds', '')}r")
            md += [f"- `{o['id']}` vs `{o['opponentAIs'][0]['ids'][0]}` — {o['description']}" + (f" *({'; '.join(extra)})*" if extra else "")]
        elif o["task"] == "reset_quest":
            md += [f"- `{o['id']}` → reset to `{o['resetObjectiveId']}` (silent)"]
        else:
            md += [f"- `{o['id']}` ({o['task']}) — {o['description']}"]
    md.append("")
    caches = cache_items(entry)
    manifest = validation_manifest(quest, profiles, cmds, entry, caches)
    return {"quest.candidate.json": json.dumps(quest, indent=1, ensure_ascii=False) + "\n",
            "validation_manifest.candidate.json": json.dumps(manifest, indent=1, ensure_ascii=False) + "\n",
            "ai_profiles.candidate.json": json.dumps({"status": "OFFLINE PACKAGE — rules compile from design/*.json; launch values accepted (RUL-2026-10-16-011), calibration may tune", "profiles": profiles}, indent=1, ensure_ascii=False) + "\n",
            "encounter_ledger.json": json.dumps({"status": "20 encounter identities (16 regulars + 4 commanders), source-mapped", "slots": ledger}, indent=1, ensure_ascii=False) + "\n",
            "cache_items.candidate.json": json.dumps({"status": entry["caches"]["status"], "caches": caches}, indent=1, ensure_ascii=False) + "\n",
            "story_script.md": "\n".join(md)}

TIER_NAME = {"EPIC": "Epic", "LEGENDARY": "Legendary"}

def cache_items(entry):
    """The two completion caches as item records (RUL-2026-10-16-010): one roll, tier weights and
    quantities from design/entry_and_rewards.json, recipe entries from the approved candidate pools.
    Ingredient ids are the census capture's; a fresh read is still required before a manifest."""
    c = entry["caches"]; wc = c["weightedCache"]
    pools = j(wc["poolsSource"])
    if sum(wc["tierWeights"].values()) != 10000 or sum(r["probability"] for r in wc["rolls"]) != 10000:
        fail("cache roll/tier weights must total 10000")
    out = []
    for fam in ("arsenal", "research"):
        spec, pool = c[fam], pools["pools"][fam]
        tiers = {t: [] for t in wc["tierWeights"]}
        for r in pool["chosen"]:
            if r["status"] != "PROPOSED_PILOT": continue
            items = [{"itemId": i["id"], "quantity": i["quantityPyramid"]} for i in r["ingredients"]]
            if any(x["quantity"] < 1 for x in items): fail(f"{r['output']['name']}: zero quantity")
            tiers[r["output"]["rarity"]].append({"recipe": r["output"]["name"], "recipeId": r["output"]["id"], "items": items})
        if any(not v for v in tiers.values()): fail(f"{fam}: empty tier")
        effect = {"type": "noncombatconsumereward", "rewardMode": "weightedCache",
                  "weightedCache": {"version": 1, "displayName": spec["name"], "rolls": wc["rolls"],
                                    "tiers": [{"name": TIER_NAME[t], "probability": w, "entries": [{"items": e["items"]} for e in tiers[t]]}
                                              for t, w in wc["tierWeights"].items()]}}
        out.append({"ref": spec["ref"], "srcId": spec["ref"].split(":")[1],
                    "entries": {TIER_NAME[t]: [e["recipe"] for e in v] for t, v in tiers.items()},
                    "record": {"name": spec["name"], "description": spec.get("description", ""), "itemType": spec["itemType"],
                               "rarity": spec["rarity"]["value"], "canBeTraded": spec["tradeable"], "destroyOnUse": spec["destroyOnUse"],
                               "preventBattleUsage": spec["preventBattleUsage"], "target": "SELF", "canStack": True, "stackSize": 10, "hidden": True,
                               "effects": [effect]}})
    return out

def slot_src(slot):
    return "bastion_" + slot.lower().replace(".", "_")

def validation_manifest(quest, profiles, cmds, entry, caches):
    """Builder-dialect manifest for skills/building-tnr-content/scripts/validate.py ONLY.
    Not a push manifest: it lives in compiled/ and carries no capture."""
    def ref(v):
        if isinstance(v, str) and v.startswith("@ai:"):
            return "@ai:" + slot_src(v[4:])
        if isinstance(v, str) and v.startswith("@asset:"):
            return ""
        return v
    def deep(x):
        if isinstance(x, dict): return {k: deep(v) for k, v in x.items()}
        if isinstance(x, list): return [deep(v) for v in x]
        return ref(x)
    items = []
    for key, ex in cmds["exclusives"].items():
        r = {k: v for k, v in ex["record"].items() if k not in ("dropChancePerc",)}
        r["effects"] = [{k: v for k, v in e.items() if k != "candidate"} for e in r["effects"]]
        entity = "item" if r.get("itemType") else "jutsu"
        items.append({"entity": entity, "slot": "create", "srcId": key[2:].lower(), "name": r["name"], "data": {**r, "hidden": True}})
    b = entry["beacon"]
    items.append({"entity": "item", "slot": "create", "srcId": "skyglass_signal_beacon", "name": b["name"],
                  "data": {"name": b["name"], "description": b["description"], "itemType": b["itemType"]["value"], "rarity": b["rarity"]["value"],
                           "effects": [], "destroyOnUse": True, "preventBattleUsage": True, "canBeTraded": b["tradeable"]["value"], "hidden": True, "cost": 1, "canStack": True, "stackSize": 10}})
    for ch in caches:
        items.append({"entity": "item", "slot": "create", "srcId": ch["srcId"], "name": ch["record"]["name"], "data": {**ch["record"], "cost": 1}})
    for p in profiles:
        rec = dict(p["record"]); ratio = rec.pop("ratio")
        gens = rec.pop("generals")
        data = {"username": p["name"], "level": rec["level"], "rank": rec["rank"], "regeneration": rec["regeneration"],
                "statsMultiplier": rec["statsMultiplier"], "poolsMultiplier": rec["poolsMultiplier"], "isSummon": False, "hidden": True,
                "primaryElement": rec["element"], "secondaryElement": "", "preferredStat": rec["preferredStat"],
                "preferredGeneral1": gens[0], "preferredGeneral2": gens[1],
                **{k: v * 100 for k, v in ratio.items()},
                "jutsus": rec["jutsus"], "items": rec["items"], "effects": rec["effects"],
                "rules": [{"conditions": r["conditions"], "action": r["action"]} for r in p["aiProfile"]["rules"]],
                "includeDefaultRules": False}
        items.append({"entity": "ai", "slot": "create", "srcId": slot_src(p["slot"]), "name": p["name"], "data": deep(data)})
    rec = deep(quest["record"])
    items.append({"entity": "quest", "slot": "create", "srcId": "bastion_quest", "name": rec["name"], "data": rec})
    return {"_note": "VALIDATION-ONLY builder-dialect view of the offline candidate for validate.py; NOT a push manifest, never under push/, no capture",
            "items": items}

def main():
    out = compose()
    if "--check" in sys.argv:
        bad = [f for f, t in out.items() if not os.path.exists(os.path.join(OUTD, f)) or open(os.path.join(OUTD, f)).read() != t]
        print("compiled/:", "current" if not bad else f"STALE {bad}")
        return 1 if bad else 0
    os.makedirs(OUTD, exist_ok=True)
    for f, t in out.items():
        open(os.path.join(OUTD, f), "w").write(t)
    q = json.loads(out["quest.candidate.json"])["record"]["content"]["objectives"]
    print(f"wrote compiled/: {len(q)} objectives, {len(json.loads(out['ai_profiles.candidate.json'])['profiles'])} AI profiles")
    return 0

if __name__ == "__main__":
    sys.exit(main())
