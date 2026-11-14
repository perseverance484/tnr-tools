#!/usr/bin/env python3
"""Direct-connector edits for the Nov 13 release that Forge cannot save. Each prints the exact input for one call,
built from a fresh read saved to a file. No guessing: the read decides every other field.

    python3 push/connector_edits_nov13.py npc-pool <placement_read.json>   -> overworldAi.upsertPlacement input
        Her placement goagM4WhKWtnVb8oP5euM: drop the 4 RETIRED trade rows (Nov 13 retirement), keep isActive as read.
    python3 push/connector_edits_nov13.py husk <getAi_read.json> [name]     -> profile.updateAi input
        Yk1LNNncF2dt7jY_TVSXc "Wreck Test Husk" -> "Netted Husk" (players see it in every trade fight). Name only.
"""
import json, sys
RETIRED = {"TdYCx3GME2s6L33GjnWHx", "7pk21EmBrmL_EyHuPK2Xp", "jUQYz9zyMdJIRdLbucYjm", "MSQJTdZEQK1JWjFiVtQVI"}
PLACEMENT_KEYS = ["aiTemplateUserId", "interactionType", "sectorType", "locationType", "sector", "longitude", "latitude",
                  "sectorList", "quests", "isActive", "wanderRadius", "spawnCount", "groupMin", "groupMax", "habitats",
                  "wildOnly", "mapScale"]
SCHEMA = "/root/.claude/projects/-home-user/ac11ca9e-b18e-5e7b-be33-25a614300a95/tool-results/mcp-Tnr-getEndpointSchema-1794600048621.txt"


def load(p):
    r = json.load(open(p))
    return r.get("data", r) if isinstance(r, dict) and "data" in r and "id" not in r else r


def npc_pool(p):
    r = load(p)
    r = r if "aiTemplateUserId" in r else next(x for x in (r if isinstance(r, list) else r.get("placements", []))
                                               if x.get("id") == "goagM4WhKWtnVb8oP5euM")
    assert r["id"] == "goagM4WhKWtnVb8oP5euM", r.get("id")
    pool = r.get("quests") or r.get("questPool") or []
    pool = [{"questId": q["questId"], "chance": q["chance"]} for q in pool]
    kept = [q for q in pool if q["questId"] not in RETIRED]
    data = {k: r[k] for k in PLACEMENT_KEYS if k in r}
    data["quests"] = kept
    missing = [k for k in PLACEMENT_KEYS if k not in data]
    assert not missing, missing
    print(f"# removed {len(pool) - len(kept)} retired rows, kept {len(kept)}; isActive {data['isActive']}", file=sys.stderr)
    print(json.dumps({"id": r["id"], "data": data}, ensure_ascii=False))


def husk(p, name):
    r = load(p)
    assert r["userId"] == "Yk1LNNncF2dt7jY_TVSXc" and r["username"] == "Wreck Test Husk", (r.get("userId"), r.get("username"))
    t = open(SCHEMA).read()
    allowed = list(json.loads(t[t.find("{"):])["inputSchema"]["properties"]["data"]["properties"])
    data = {k: r[k] for k in allowed if k in r}
    data["username"] = name
    print(json.dumps({"id": r["userId"], "data": data}, ensure_ascii=False))


if __name__ == "__main__":
    if sys.argv[1] == "npc-pool":
        npc_pool(sys.argv[2])
    elif sys.argv[1] == "husk":
        husk(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "Netted Husk")
    else:
        sys.exit(__doc__)
