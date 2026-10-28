#!/usr/bin/env python3
"""Resolve the Skyglass Wreck baseline from committed evidence only (no network).

Inputs (all committed in tnr-tools):
  - archive/spent-manifests/push-2026-10-25/263_skyglass_wreck_dungeon.json  (dungeon definition)
  - harvests/inbox/tnr_results_1792900120886.json   (push/249 roster capture: profile.getAi + ai.getAiProfile)
  - archive/spent-manifests/push-2026-10-25/250_skyglass_sentinel_rules.json + results tnr_results_1792900236721.json
      (verdict "drift": the server stored the rules with use_highest_power_action.effect="damage"
       added; the LIVE readback from the results bundle is used, not the sent payload)
  - archive/spent-manifests/push-2026-10-25/251_skyglass_crew_rules.json + results tnr_results_1792904268435.json (all "match")
  - archive/spent-manifests/push-2026-10-25/252_skyglass_boss_health.json + results tnr_results_1792904277241.json (all "match")
  - player jutsu records: newest captured copy across harvests/ and answers/ (path recorded per record)

The 252 poolsMultiplier edits are NOT applied here: they are recorded as pending AI edits
and replayed in the engine through `scaleEditedAi` (the server's own save path).

Output: data/baseline.json (deterministic; --check verifies it is current).
"""
import glob
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HARNESS = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(HARNESS))
OUT = os.path.join(HARNESS, "data", "baseline.json")

DUNGEON = "archive/spent-manifests/push-2026-10-25/263_skyglass_wreck_dungeon.json"
ROSTER = "harvests/inbox/tnr_results_1792900120886.json"
P250 = "archive/spent-manifests/push-2026-10-25/250_skyglass_sentinel_rules.json"
R250 = "harvests/inbox/tnr_results_1792900236721.json"
P251 = "archive/spent-manifests/push-2026-10-25/251_skyglass_crew_rules.json"
R251 = "harvests/inbox/tnr_results_1792904268435.json"
P252 = "archive/spent-manifests/push-2026-10-25/252_skyglass_boss_health.json"
R252 = "harvests/inbox/tnr_results_1792904277241.json"

# Player kit: real, non-hidden, non-elemental NORMAL jutsu usable in PvE (battleUsageType BOTH/PVE;
# QUEST battles filter out PVP-only jutsu) seen in captures. Eight = within the JONIN equip limit (9).
# Endgame kit (director 2026-10-28: level-capped PvE jutsu). Strongest common, non-hidden,
# PvE-usable (battleUsageType PVE/BOTH) damage jutsu in the captures for a Fire/Wind player:
# all formula damage scaling 0.4 per level, used at the Jonin level cap 25.
ENDGAME_JUTSU = {
    "nS-iidYFYqWE9Z-UkC84y": "Scorching Sun Strike (CHUNIN, PVE, Fire; damage 40 + wound 30, cd 7)",
    "mYCbcdDwDzJBul52HiwhC": "Burning Coil (CHUNIN, PVE, Fire; damage 40 + IDT 30, cd 7)",
    "V_VY284CMTuqYqOOX5sa7": "Phoenix Flame Strike (CHUNIN, PVE, Fire; damage 35 + IDG 30, cd 7)",
    "fCWC_ICdWT1bJDkDVq22e": "Wind Style: Sky Dragon (CHUNIN, PVE, Wind; damage 40 + wound 30, cd 7)",
    "PQdSt0IDdYFoR44tC3Hvo": "Typhon Burst (CHUNIN, PVE, Wind; AOE damage 35 + IDG 30, cd 7)",
    "uf5dAzEg_Blu4MBePzx_m": "Tempestual Fury (CHUNIN, PVE, Wind; AOE damage 35 + afterburn 30, cd 7)",
    "rBcwIiHjKOF07Yoq4wVqU": "Gale Force Blast (CHUNIN, BOTH, Wind; pierce 56 + IDT 30, cd 7)",
}

# Kitsune armour set (push/204 capture, 12/12 reads ok): one piece per armour slot.
GEAR_CAPTURE = "harvests/inbox/tnr_results_1792629744565.json"
KITSUNE_SET = {
    "X0-snQ-GNGpqn4w5Ir2M0": "HEAD",   # Kitsune Mask
    "WgjbuICAqrLq1y6wmNHTd": "CHEST",  # Kitsune Armor
    "kNshju2IjLN8h0FvpNKgg": "HAND",   # Kitsune Gauntlets
    "tOSetjSOXPFOlfKH8ogkR": "WAIST",  # Kitsune Belt
    "CIT8c_SvjTP59tmNz1ghy": "LEGS",   # Kitsune Pants (Pants-F AmtbbB3Jm2dDB3t3r6kSW is an identical alternate)
    "hDvjJp4aQlMW_jeYA8U_L": "FEET",   # Kitsune Tabi-Shoes
}

PLAYER_JUTSU = {
    "e2eC-x4UXc5m6QexNbx8w": "Chakra Overflow (JONIN A, BOTH; SELF IDG 25+25, 2 rounds, cd 7)",
    "cUPCLvCCEO9MCSRtFsulW": "Aqua Barrier (CHUNIN B, PVE; SELF DDT 30 + IDG 30, 2 rounds, cd 7)",
    "4eDM_5VVZkasBjaW2fEmI": "Void Pulse Barrage (JONIN A, BOTH; AOE pierce 46 + IDT 20, cd 7)",
    "GiKpip6NxsC8QWlZi6l_R": "Shrapnel Clone Barrage (JONIN A, BOTH; AOE damage 45 + wound 30, cd 7)",
    "VT7oxj_fObWuQa3Rq_BbI": "Stunning Jab (CHUNIN B, PVE; damage 35 + stun 90, cd 5)",
    "zCmYLVL4JYzfhjPXHi9rH": "Eight Fist Style: Lotus Dance (JONIN A, BOTH; damage 35 + buffprevent, cd 7)",
    "kbrQuf3nYNHoKEvusATTO": "Phantom Requiem (JONIN S, BOTH; damage 30 + drain 250, cd 7)",
    "fAKcf34Vlt_-utDdDdjxH": "Rejuvenating Chakra (CHUNIN C, BOTH; SELF heal 40, cd 10)",
    # Chunin-rank kit for the level 40-60 version (all requiredLevel 1, CHUNIN rank, PvE-usable).
    "C1SdH7N13naMHG3bKE07k": "Harden Fist (CHUNIN B, BOTH; SELF IDG 20 + DDT 20, cd 6)",
    "uhEr3x6ucxHJbcjnTs7ps": "Shattering Strike (CHUNIN C, BOTH; damage 30 + DDT 15, cd 7)",
    "5JCcW9EdcDy7a5-0SiH_W": "Chakra Palm (CHUNIN C, BOTH; damage 28 + shield, cd 7)",
    "kvuECU_A6qeZYsWwU_Zvq": "Resounding Crescendo (CHUNIN C, BOTH; damage 28 + DDT 15, cd 7)",
    "Oi5pYxNaHa-5o737i5gAu": "Iron Fist (CHUNIN A, PVE; damage 20 + lifesteal 20, cd 6)",
    **ENDGAME_JUTSU,
}


BASIC_ACTIONS = {"basicAttack", "basicHeal", "basicMeditate", "meditate", "move", "wait", "flee", "cleanse", "clear"}


def rel(p):
    return os.path.join(REPO, p)


def load(p):
    with open(rel(p), "rb") as f:
        raw = f.read()
    return json.loads(raw), hashlib.sha256(raw).hexdigest()


def entries_verdicts(bundle):
    return [(e.get("name"), e.get("verdict"), e.get("id")) for e in bundle.get("entries", [])]


def main(check=False):
    prov = {}
    dungeon, prov[DUNGEON] = load(DUNGEON)
    roster, prov[ROSTER] = load(ROSTER)
    m250, prov[P250] = load(P250)
    r250, prov[R250] = load(R250)
    m251, prov[P251] = load(P251)
    r251, prov[R251] = load(R251)
    m252, prov[P252] = load(P252)
    r252, prov[R252] = load(R252)

    tier = dungeon["items"][0]["data"]["tiers"]
    if len(tier) != 1:
        raise SystemExit("expected exactly one tier")
    floors = tier[0]
    ai_ids = sorted({a for f in floors for w in f["waves"] for a in w["aiIds"]})

    users, profiles = {}, {}
    for i, c in enumerate(roster["captures"]):
        if not c.get("ok"):
            raise SystemExit(f"capture {i} not ok")
        if c["proc"] == "profile.getAi":
            users[c["data"]["userId"]] = (c["data"], f"{ROSTER}#/captures/{i}/data")
        elif c["proc"] == "ai.getAiProfile":
            profiles[c["data"]["id"]] = (c["data"], f"{ROSTER}#/captures/{i}/data")
    missing = [a for a in ai_ids if a not in users]
    if missing:
        raise SystemExit(f"AIs not in roster capture: {missing}")

    # Jutsu catalog from the roster capture (includes unequipped rows; needed for push/251 kit edit).
    jutsu_catalog = {}
    for uid, (u, p) in users.items():
        for k, uj in enumerate(u["jutsus"]):
            jutsu_catalog.setdefault(uj["jutsuId"], (uj["jutsu"], f"{p}/jutsus/{k}/jutsu"))

    enemies = {}
    edits_log = []
    for aid in ai_ids:
        u, upath = users[aid]
        prof, ppath = profiles[u["aiProfileId"]]
        enemies[aid] = {
            "user": u,
            "userSource": upath,
            "profile": prof,
            "profileSource": ppath,
            "pendingAiEdit": None,
        }

    # push/250: Sentinel rules. Verdict drift -> use the live readback (server-normalised).
    v250 = entries_verdicts(r250)
    assert v250 == [("Skyglass Sentinel: rules use the whole kit", "drift", "3V_gdHYaclMB1gTyOPAbV")], v250
    diff = r250["entries"][0]["diffs"]
    live_rules = next(d["live"] for d in diff if d["key"] == "rules")
    sent = m250["items"][0]["data"]
    e = enemies["3V_gdHYaclMB1gTyOPAbV"]
    e["profile"] = {**e["profile"], "rules": live_rules, "includeDefaultRules": sent["includeDefaultRules"]}
    e["profileSource"] = f"{R250}#/entries/0/diffs[key=rules]/live (push/250, verdict drift: server added effect=damage)"
    edits_log.append("push/250 Sentinel rules: live readback applied (drift = server default effect:'damage' on use_highest_power_action)")

    # push/251: crew kit + rules. All verified 'match' -> sent payload is stored state.
    v251 = entries_verdicts(r251)
    assert all(v == "match" for _, v, _ in v251), v251
    for k, it in enumerate(m251["items"]):
        tid = it["targetId"]
        e = enemies[tid]
        if it["entity"] == "ai" and "jutsus" in it["data"]:
            wanted = it["data"]["jutsus"]
            have = {uj["jutsuId"]: uj for uj in e["user"]["jutsus"]}
            new_rows = []
            for jid in wanted:
                if jid in have:
                    new_rows.append(have[jid])
                else:
                    rec, src = jutsu_catalog[jid]
                    new_rows.append({
                        "id": f"push251-{tid[:6]}-{jid[:6]}", "userId": tid, "jutsuId": jid,
                        "level": 1, "experience": 0, "equipped": True, "finishTraining": None,
                        "reskinId": None, "jutsu": rec,
                    })
                    edits_log.append(f"push/251 {it['name']}: +{rec['name']} ({jid}) equipped, record from {src}")
            e["user"] = {**e["user"], "jutsus": new_rows}
        elif it["entity"] == "aiProfile":
            e["profile"] = {**e["profile"], "rules": it["data"]["rules"], "includeDefaultRules": it["data"]["includeDefaultRules"]}
            e["profileSource"] = f"{P251}#/items/{k}/data (verified match in {R251})"
            edits_log.append(f"push/251 {it['name']}")

    # push/252: pools multiplier edits, replayed in-engine through scaleEditedAi.
    v252 = entries_verdicts(r252)
    assert all(v == "match" for _, v, _ in v252), v252
    for k, it in enumerate(m252["items"]):
        enemies[it["targetId"]]["pendingAiEdit"] = {"data": it["data"], "source": f"{P252}#/items/{k}/data"}
        edits_log.append(f"push/252 {it['name']}: {it['data']} (replayed via scaleEditedAi)")

    # Rule references to unequipped/missing jutsu (informational).
    rule_warnings = []
    for aid, e in enemies.items():
        eq = {uj["jutsuId"] for uj in e["user"]["jutsus"] if uj.get("equipped")}
        for ri, r in enumerate(e["profile"]["rules"]):
            a = r["action"]
            ids = ([a["jutsuId"]] if a.get("jutsuId") else []) + list(a.get("comboIds") or [])
            bad = [x for x in ids if x not in eq and x not in BASIC_ACTIONS]
            if bad:
                rule_warnings.append(f"{e['user']['username']} rule {ri} ({a['type']}) references unequipped/missing jutsu {bad}")

    # Player jutsu: newest captured copy across harvests/ and answers/.
    found = {}
    files = sorted(glob.glob(rel("harvests/**/*.json"), recursive=True) + glob.glob(rel("answers/**/*.json"), recursive=True))

    def walk(x, f):
        if isinstance(x, dict):
            if x.get("id") in PLAYER_JUTSU and "jutsuType" in x and "effects" in x:
                cur = found.get(x["id"])
                if cur is None or (x.get("updatedAt") or "") > (cur[0].get("updatedAt") or ""):
                    found[x["id"]] = (x, os.path.relpath(f, REPO))
            for v in x.values():
                walk(v, f)
        elif isinstance(x, list):
            for v in x:
                walk(v, f)

    for f in files:
        try:
            with open(f) as fh:
                walk(json.load(fh), f)
        except Exception:
            continue
    nf = [j for j in PLAYER_JUTSU if j not in found]
    if nf:
        raise SystemExit(f"player jutsu not captured: {nf}")
    for j, (rec, src) in found.items():
        prov[src] = hashlib.sha256(open(rel(src), "rb").read()).hexdigest()

    # Kitsune armour records (full item.get reads).
    gdoc, prov[GEAR_CAPTURE] = load(GEAR_CAPTURE)
    gear = {}
    for i, c in enumerate(gdoc["captures"]):
        x = c.get("data")
        if isinstance(x, dict) and x.get("id") in KITSUNE_SET:
            if not c.get("ok"):
                raise SystemExit(f"gear capture {i} not ok")
            if x["slot"] != KITSUNE_SET[x["id"]] or x["itemType"] != "ARMOR":
                raise SystemExit(f"{x['name']}: slot {x['slot']} / {x['itemType']} unexpected")
            gear[x["id"]] = {"slot": x["slot"], "record": x, "source": f"{GEAR_CAPTURE}#/captures/{i}/data"}
    missing_gear = [k for k in KITSUNE_SET if k not in gear]
    if missing_gear:
        raise SystemExit(f"Kitsune pieces not captured: {missing_gear}")

    out = {
        "_note": "Generated by tools/build_baseline.py from committed captures. Do not hand-edit.",
        "provenance": dict(sorted(prov.items())),
        "edits": edits_log,
        "ruleWarnings": rule_warnings,
        "dungeon": {
            "name": dungeon["items"][0]["data"]["name"],
            "floors": [{"kind": f["kind"], "waves": [{"aiIds": w["aiIds"], "delayRounds": w["delayRounds"]} for w in f["waves"]]} for f in floors],
        },
        "enemies": enemies,
        "jutsuCatalog": {k: {"record": v[0], "source": v[1]} for k, v in sorted(jutsu_catalog.items())},
        "playerJutsu": {k: {"label": PLAYER_JUTSU[k], "record": found[k][0], "source": found[k][1]} for k in PLAYER_JUTSU},
        "playerGear": gear,
    }
    text = json.dumps(out, indent=1, sort_keys=True) + "\n"
    if check:
        cur = open(OUT).read() if os.path.exists(OUT) else ""
        if cur != text:
            print("baseline.json is stale; run tools/build_baseline.py", file=sys.stderr)
            return 1
        print("baseline.json current")
        return 0
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        f.write(text)
    print(f"wrote {os.path.relpath(OUT, REPO)}: {len(enemies)} enemies, {sum(len(f['waves']) for f in out['dungeon']['floors'])} waves")
    for w in rule_warnings:
        print("  rule warning:", w)
    return 0


if __name__ == "__main__":
    sys.exit(main("--check" in sys.argv))
