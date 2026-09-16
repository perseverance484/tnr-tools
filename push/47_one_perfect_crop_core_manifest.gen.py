#!/usr/bin/env python3
"""
push/47_one_perfect_crop_core_manifest.gen.py

Builds push/47_one_perfect_crop_core_manifest.json: the HIDDEN CORE MANIFEST for
One Perfect Crop.

Contract: state/prompt_one_perfect_crop.md, governed by the 2026-09-16 override
state/one_perfect_crop_core_manifest_override.md (ruling RUL-2026-09-16-001).

Five creates, nothing else:
    ai         Road Bandit
    ai         Harvest Boar
    aiProfile  Road Bandit behaviour
    aiProfile  Harvest Boar behaviour
    quest      One Perfect Crop

DELIBERATELY ABSENT, because the override defers them to launch finalization:
  - no asset entries, no @img refs, no fabricated scene/image ids
  - no Cabbage Seed item and no Cabbage Seed reward grant
  - no jutsu entries (the kits are existing shared-pool ids)
  - no Ryo/XP/token reward values, no repeatability, no eligibility gate
  - no publish/unhide operation; every create is hidden:true

Nothing here is transcribed from prose by hand:
  - node text and choice routing are PARSED out of the frozen
    state/one_perfect_crop_prose_graph.md at generation time;
  - jutsu ids and their distance gates are resolved from pool codes through
    32b_DATA_pool.json;
  - the AI records are built by skills/building-tnr-content/scripts/enemy.py
    from its ratified role defaults, then given only the values the combat spec
    fixes explicitly;
  - rule objects, objective nodes and the quest entry are built by
    skills/building-tnr-content/scripts/factory.py from 45c/45d/45g.

Run from the repository root:
    python3 push/47_one_perfect_crop_core_manifest.gen.py
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "skills", "building-tnr-content")
sys.path.insert(0, os.path.join(SKILL, "scripts"))

from factory import Factory                      # noqa: E402
from enemy import build_ai, load_pool            # noqa: E402

PROSE = os.path.join(ROOT, "state", "one_perfect_crop_prose_graph.md")
SPEC = os.path.join(ROOT, "state", "one_perfect_crop_combat_spec.md")
OUT = os.path.join(ROOT, "push", "47_one_perfect_crop_core_manifest.json")

CTORS = os.path.join(ROOT, "45c_DATA_constructors.json")
ENTS = os.path.join(SKILL, "data", "45d_DATA_entity_schemas.json")
CHECKS = os.path.join(ROOT, "45g_DATA_checks.json")
POOL = os.path.join(ROOT, "32b_DATA_pool.json")

QUEST_NAME = "One Perfect Crop"
QUEST_SRC = "opc_quest"

# state/one_perfect_crop_combat_spec.md, "Shared combat facts" and the two
# per-enemy sections. Kits are POOL CODES; enemy.py resolves them to the literal
# shared ids and this generator asserts the ids against the spec text below.
ENEMIES = [
    {
        "name": "Road Bandit",
        "srcId": "opc_ai_road_bandit",
        "kit": ["S27", "S41", "S40"],
        "preferredStat": "Bukijutsu",
        "battle_node": "opc_f2_battle",
    },
    {
        "name": "Harvest Boar",
        "srcId": "opc_ai_harvest_boar",
        "kit": ["S27", "S42", "S41"],
        "preferredStat": "Taijutsu",
        "battle_node": "opc_c1_battle",
    },
]

AI_RANK = "JONIN"
AI_LEVEL = 100
AI_ELEMENT = "None"
AI_GENERAL_1 = "Strength"
AI_GENERAL_2 = "Speed"

# The battle nodes the frozen graph defines, keyed by node id: the AI srcId that
# fights there. One enemy per battle (spec: "exactly one enemy").
BATTLE_OPPONENT = {e["battle_node"]: e["srcId"] for e in ENEMIES}


# --------------------------------------------------------------- frozen prose

def parse_prose(path):
    """Read state/one_perfect_crop_prose_graph.md into node records.

    The file is the frozen wording/route contract, so it is parsed rather than
    retyped: a typo here would be a silent content change nobody diffs.
    """
    text = open(path, encoding="utf-8").read()
    # Stop before the scene-family wiring appendix: that section is the deferred
    # art task and names assets this core manifest deliberately does not create.
    text = text.split("# Scene-family wiring")[0]

    nodes, order = {}, []

    def add(nid, **kw):
        if nid not in nodes:
            nodes[nid] = {"id": nid}
            order.append(nid)
        nodes[nid].update(kw)

    for block in re.split(r"^## ", text, flags=re.M)[1:]:
        m = re.search(r"\*\*Logical id:\*\*\s*`([a-z0-9_]+)`", block)
        if not m:
            continue
        nid = m.group(1)

        task = re.search(r"^- task: `([a-z_]+)`", block, flags=re.M)
        add(nid, task=task.group(1) if task else "dialog")

        d = re.search(r"\*\*description\*\*\s*\n+`(.+?)`\s*\n", block, flags=re.S)
        if d:
            add(nid, description=d.group(1))

        comp = re.search(r"^- completion text: `(.+?)`\s*$", block, flags=re.M)
        if comp:
            add(nid, successDescription=comp.group(1))

        ch = re.findall(r"^- `(.+?)` -> `([a-z0-9_]+)`\s*$", block, flags=re.M)
        if ch:
            add(nid, choices=[{"text": t, "nextObjectiveId": n} for t, n in ch])

        succ = re.search(r"^- success -> `([a-z0-9_]+)`", block, flags=re.M)
        if succ:
            add(nid, nextObjectiveId=succ.group(1))
        fail = re.search(r"^- fail -> `([a-z0-9_]+)`", block, flags=re.M)
        if fail:
            add(nid, failObjectiveId=fail.group(1))

        # Terminal declarations, in both spellings the frozen file uses.
        for tid, ttask in re.findall(
                r"\*\*terminal:\*\* `([a-z0-9_]+)` = `([a-z_]+)`", block):
            add(tid, task=ttask)
        for tid, ttask in re.findall(
                r"^- `([a-z0-9_]+)` = terminal `([a-z_]+)`\s*$", block, flags=re.M):
            add(tid, task=ttask)

    return [nodes[i] for i in order]


# ----------------------------------------------------------------- objectives

def build_objectives(f, parsed):
    """One generated-constructor node per frozen node. No reward block is
    authored on any node: the generated objective contract (45c AllObjectives)
    carries no reward fields, and the override forbids choosing reward values.
    Scene fields keep their constructor defaults because the scene-wiring / art
    tasks are deferred and must not be half-authored from fabricated ids.
    """
    objs = []
    for n in parsed:
        task, nid = n["task"], n["id"]
        if task == "dialog":
            node = f.objective(
                "dialog",
                id=nid,
                description=n["description"],
                nextObjectiveId=[dict(c) for c in n["choices"]],
                # No ambush rolls anywhere in this event: `attackers` stays
                # empty, so the scale flag is inert and set explicitly because
                # the schema carries no default for it.
                attackers=[],
                attackers_scaled_to_user=False,
            )
        elif task == "start_battle":
            node = f.objective(
                "start_battle",
                id=nid,
                opponentAIs=[{"ids": ["@ai:" + BATTLE_OPPONENT[nid]],
                              "number": 1, "quantity": 1}],
                # Frozen quest-level battle setting: scale the single enemy to
                # the player (combat spec, "Shared combat facts").
                opponent_scaled_to_user=True,
                keepOriginalPools=False,
                completionOutcome="Win",
                nextObjectiveId=n["nextObjectiveId"],
                failObjectiveId=n["failObjectiveId"],
            )
        elif task in ("win_quest", "fail_quest"):
            kw = {"id": nid, "task": task}
            if n.get("successDescription"):
                kw["successDescription"] = n["successDescription"]
            node = f.objective("InstantWinLoseObjective", **kw)
        else:
            raise SystemExit(f"{nid}: unexpected task {task!r} in the frozen graph")
        objs.append(node)
    return objs


# --------------------------------------------------------------- AI + profile

def build_enemy_entries(f, pool, spec_text):
    ai_entries, profile_entries = [], []
    for e in ENEMIES:
        entry = build_ai(
            {"name": e["name"], "srcId": e["srcId"], "role": "standard",
             "kit": e["kit"], "element": AI_ELEMENT, "rank": AI_RANK,
             "stat_archetype": "uniform"},
            AI_LEVEL, f, pool,
        )
        entry.pop("_derived", None)
        data = entry["data"]

        # Behaviour lives on the AiProfile entry, which is its own record
        # (ai.updateAiProfile). Keeping one copy means the two cannot drift.
        rules = data.pop("rules")
        data.pop("includeDefaultRules")

        # The five fields law 14 / builder lint L05 require, at the values the
        # combat spec fixes. Everything else is enemy.py's ratified default.
        data["preferredStat"] = e["preferredStat"]
        data["preferredGeneral1"] = AI_GENERAL_1
        data["preferredGeneral2"] = AI_GENERAL_2

        # Exactly the three authored rules, in the frozen order, gate-checked
        # against the pool: no movement, highest-power or anti-exhaust rule is
        # authored, because includeDefaultRules appends the engine's own tail.
        rules = [f.rule(f.condition("distance_lower_than", value=pool[c]["gate"]),
                        action=f.action("use_specific_jutsu", jutsuId=pool[c]["id"]))
                 for c in e["kit"]]

        ai_entries.append(entry)
        profile_entries.append({
            "name": e["name"] + " AiProfile",
            "entity": "aiProfile",
            "slot": "create",
            "srcId": e["srcId"] + "_profile",
            # The builder resolves this to the AI created above (phase ai runs
            # before phase aiProfile), then getAi -> toggleAiProfile -> update.
            "targetId": "@ai:" + e["srcId"],
            "data": {
                # name/hidden are inert on this push path (the builder sends
                # only rules + includeDefaultRules) and are carried so the
                # entry satisfies the create laws 16b and 36 like any other.
                "name": e["name"] + " AiProfile",
                "hidden": True,
                "rules": rules,
                "includeDefaultRules": True,
            },
        })

        # Contract assertions against the spec text itself, not against memory.
        for code in e["kit"]:
            assert pool[code]["id"] in spec_text, f"{code} id absent from the combat spec"
        assert data["jutsus"] == [pool[c]["id"] for c in e["kit"]]
        assert [r["action"]["jutsuId"] for r in rules] == data["jutsus"]
        assert data["rank"] == AI_RANK and data["level"] == AI_LEVEL
        assert data["statsMultiplier"] == 1 and data["poolsMultiplier"] == 1
        assert data["regeneration"] == 60 and data["hidden"] is True
        assert "effects" not in data and "avatar" not in data
    return ai_entries, profile_entries


# ------------------------------------------------------------------ assembly

def main():
    f = Factory(ctors=CTORS, entities=ENTS, checks=CHECKS)
    pool = load_pool(POOL)
    spec_text = open(SPEC, encoding="utf-8").read()

    parsed = parse_prose(PROSE)
    objectives = build_objectives(f, parsed)
    ai_entries, profile_entries = build_enemy_entries(f, pool, spec_text)

    quest = f.entry(
        "quest", "create", name=QUEST_NAME, srcId=QUEST_SRC,
        data={
            "name": QUEST_NAME,
            "questType": "event",
            # Law 23/37: required with no schema default, and it lives at data
            # level, never inside content.
            "consecutiveObjectives": True,
            "hidden": True,
            # The only completion prose the frozen graph carries. Deliberately
            # not paraphrased into a second listing blurb: quest `description`
            # stays null (a schema-nullable create-path placeholder) until the
            # launch-final pass supplies player-facing listing copy.
            "successDescription": next(o["successDescription"] for o in objectives
                                       if o["task"] == "win_quest"),
            "description": None,
            # No launch window is chosen here; both are schema-required and
            # nullable, and null is the create-path "unset".
            "startsAt": None,
            "endsAt": None,
            "tierLevel": None,
            "content": {
                "objectives": objectives,
                # Zero authored rewards. The override defers Ryo/XP/tokens and
                # the Cabbage Seed grant to launch finalization.
                "reward": {},
                # Scene wiring is the deferred art task: no background or
                # character id is authored, so the create path keeps its own
                # defaults rather than half-wiring a scene family whose
                # characters this manifest may not create.
                "sceneBackground": "",
                "sceneCharacters": [],
            },
        },
    )

    man = f.manifest(ai_entries + profile_entries + [quest])
    # Live name dedup before any create (laws 30/66): a collision returns
    # success:false and leaves a blank shell.
    out = {"dedupNames": True, "items": man["items"]}

    verify(out, objectives, parsed)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(f"{OUT}: {len(out['items'])} entries, {len(objectives)} objectives")


# ------------------------------------------------------------ self-assertions

def verify(man, objectives, parsed):
    """The handoff checklist from state/prompt_one_perfect_crop.md, executed."""
    items = man["items"]
    kinds = [(i["entity"], i["slot"]) for i in items]
    assert kinds == [("ai", "create")] * 2 + [("aiProfile", "create")] * 2 \
        + [("quest", "create")], kinds
    assert all(i["data"].get("hidden") is True for i in items), "a create is not hidden"

    blob = json.dumps(man)
    for forbidden in ("@img:", "@scene:", "skipPreflight", "reward_items",
                      "Cabbage Seed", "sectorType", "locationType"):
        assert forbidden not in blob, f"{forbidden!r} must not appear in this manifest"
    assert not re.search(r'"entity":\s*"(asset|item|jutsu)"', blob)

    # Every @ref resolves inside the manifest.
    srcs = {i["srcId"] for i in items}
    assert set(re.findall(r"@ai:([a-z0-9_]+)", blob)) <= srcs

    ids = [o["id"] for o in objectives]
    assert len(ids) == len(set(ids)), "duplicate objective id"
    assert ids == [n["id"] for n in parsed], "objective order left the frozen order"

    edges, wins, fails, battles = [], [], [], []
    for o in objectives:
        n = o.get("nextObjectiveId")
        edges += [c["nextObjectiveId"] for c in n] if isinstance(n, list) else (
            [n] if isinstance(n, str) else [])
        if o.get("failObjectiveId"):
            edges.append(o["failObjectiveId"])
        if o["task"] == "win_quest":
            wins.append(o["id"])
        if o["task"] == "fail_quest":
            fails.append(o["id"])
        if o["task"] == "start_battle":
            battles.append(o)
        assert "resetObjectiveId" not in o, "no retry route is authored"
    assert not set(edges) - set(ids), f"dangling edges {set(edges) - set(ids)}"
    starts = [i for i in ids if i not in edges]
    assert starts == ["opc_o0"], f"expected exactly one start objective, got {starts}"
    assert len(wins) == 1, wins
    assert len(fails) == 6, fails          # F1-F4 wings plus one per battle loss

    # Both fights: dialog-gated, one enemy, and a loss hard-routes to fail_quest.
    by_id = {o["id"]: o for o in objectives}
    for b in battles:
        gates = [o for o in objectives
                 if isinstance(o.get("nextObjectiveId"), list)
                 and any(c["nextObjectiveId"] == b["id"] for c in o["nextObjectiveId"])]
        assert gates and all(g["task"] == "dialog" for g in gates), b["id"]
        assert len(b["opponentAIs"]) == 1 and b["opponentAIs"][0]["number"] == 1
        assert b["opponent_scaled_to_user"] is True
        assert by_id[b["failObjectiveId"]]["task"] == "fail_quest", b["id"]
    assert len(battles) == 2

    # Delivery acceptance lands before the final cabbage catastrophe.
    assert ids.index("opc_d2") < ids.index("opc_d4") < ids.index("opc_win")
    assert "Shipment accepted" in by_id["opc_d2"]["description"]
    assert "MY CABBAGES!" in by_id["opc_d4"]["description"]

    # Every dialog forward link is a choice array (law H02 / lint L29).
    for o in objectives:
        if o["task"] == "dialog":
            assert isinstance(o["nextObjectiveId"], list) and o["nextObjectiveId"]
        for d in ("—", "–"):
            assert d not in json.dumps(o), f"{o['id']}: em/en dash in node text"

    q = items[-1]["data"]
    assert q["consecutiveObjectives"] is True and "consecutiveObjectives" not in q["content"]
    assert q["questType"] == "event"
    for deferred in ("requiredLevel", "maxAttempts", "maxCompletes", "retryDelay",
                     "questRank", "image", "requiredVillage"):
        assert deferred not in q, f"{deferred} is deferred and must stay a create default"


if __name__ == "__main__":
    main()
