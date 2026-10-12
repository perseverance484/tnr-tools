#!/usr/bin/env python3
"""
Build the combined Ghost Ship / Skyglass release manifest (push/90).

This generator never contacts the game. It derives every write from committed design state and
committed operator captures, then checks the result against both offline gates (the skill's
validate.py --strict and Forge's own tools/check_manifest.mjs).

Usage from repository root:

    python3 push/90_ghost_ship_skyglass_release.gen.py --draft [--check]
    python3 push/90_ghost_ship_skyglass_release.gen.py --final \
        --image-ref <40-hex art commit> [--check]

--draft  builds against the push/89 fresh quest capture, keeps labelled placeholders for the director
         text in state/ghost_ship_skyglass_release_presentation.json, and leaves art slots from
         state/ghost_ship_skyglass_release_art.json unbound. The draft is a review artifact; Forge
         refuses it (unbound art) by design.
--final  refuses unless every presentation value and every required art slot is supplied, the
         quest base is not the stale October 1 capture (default: push/89), and
         --image-ref is an immutable ancestor commit containing the art.

Inputs (all committed):
  AIs, kits, rules     harvests/inbox/tnr_results_1791727613862.json (push/86, post-0056 rows)
                       state/ghost_ship_hybrid_kit_proposal.json (RUL-2026-10-11-003)
                       RUL-2026-10-12-001 (Crowned support), -002 (Sealwright), -003 (remap), -004 (IDG)
  Legacy jutsu text    state/ghost_ship_legacy_jutsu_conversion.json (RUL-2026-10-11-002, final by -008)
  Items                state/ghost_ship_skyglass_final_item_records.json (Katana, Crystal)
                       donor rows: Endless Night Chest (Reliquary chassis), Fragment (Filament chassis)
  Quests               state/ghost_ship_retheme_patch.json + state/ghost_ship_skyglass_graph_patch.json
  Text / art           state/ghost_ship_skyglass_release_presentation.json, ..._release_art.json

Execution order (Forge sorts by `phase`, then manifest order; refs add a partial order):
  1 asset creates (new scenes)      2 item creates (Filament, Crystal, Katana, Reliquary)
  3 asset renames, item edits       4 AI unequip of the eleven retained legacy jutsu (law 18/60)
  5 legacy jutsu text edits         6 AI final edits + Sealwright create
  7 Sealwright post-0056 stat edit  8 quest edits
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import subprocess
import sys
from collections import Counter, deque
from typing import Any

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "push", "90_ghost_ship_skyglass_release.json")
# Not under push/: builder pickers list every .json there.
REPORT = os.path.join(ROOT, "state", "ghost_ship_skyglass_release_manifest_report.json")

P86 = "harvests/inbox/tnr_results_1791727613862.json"
OCT1_QUESTS = "harvests/inbox/tnr_results_1790826101573.json"
# push/89 fresh operator capture (Forge 0.5.0, 2026-10-12T01:30Z, persist full): the quest edit base.
FRESH_QUESTS = "harvests/inbox/tnr_results_1791768613624.json"
OCT1_ITEMS = "harvests/inbox/tnr_results_1790826836406.json"
CHEST_DONOR_CAPTURE = "harvests/inbox/tnr_results_1789402842027.json"
KIT = "state/ghost_ship_hybrid_kit_proposal.json"
LEGACY = "state/ghost_ship_legacy_jutsu_conversion.json"
CONTRACT = "state/ghost_ship_skyglass_sealwright_rule_contract.json"
RECORDS = "state/ghost_ship_skyglass_final_item_records.json"
RETHEME = "state/ghost_ship_retheme_patch.json"
GRAPH = "state/ghost_ship_skyglass_graph_patch.json"
PRESENTATION = "state/ghost_ship_skyglass_release_presentation.json"
ART = "state/ghost_ship_skyglass_release_art.json"
FORGE_FIELDS = "forge/src/runner/fields.json"
ROOT_POOL = "32b_DATA_pool.json"  # the pool Forge imports (forge/src/runner/pool.mjs)

QUEST_IDS = ["6Ri-W5TtUrEMWpyYlnf_F", "HckXVOf-qk6ESU9t5rxLh"]
CAPTAIN = "QY69h271Nx9uHrBeR6jwW"
CROWNED = "fDU9jCPZtH7YHbdQPO9RF"
DIADEM = "LnRVMzyVmVwgaKvTH52Zy"
SERUM = "XhilCv1Hq4eNt-Wddok-m"
FRAGMENT = "ayiRmSjWs05lMPyL3G-1d"
CROWN = "yTS9TSpr_QLnh_3zmEpGg"
RARE_JEWELS = "05hx4hI0I4L2vAME8CcZu"
ORNATE_CHEST = "ONMLl57L7o0MivjhySHMA"
CHEST_DONOR = "HLycjzUcVwKZenBWpd0V-"  # Endless Night Chest, LEGENDARY CONSUMABLE chest
S35 = "STu1VHNcfgeC3x-UiQDgt"
B07 = "VuFuBtE7h5B1nnA2J1lFZ"
REFLECT = "T3glZGcSd-jS8G-NB43GR"

SRC = {
    "filament": "skyglass_filament",
    "crystal": "skyglass_crystal",
    "katana": "skyglass_katana",
    "reliquary": "skyglass_reliquary",
    "sealwright": "sealwright",
}
REF = {k: ("@ai:" if k == "sealwright" else "@item:") + v for k, v in SRC.items()}

# Graph-patch scene symbols that need a new asset. srcId doubles as the art slot key.
NEW_SCENES = {
    "exterior_keel": ("gs_scene_exterior_keel", "SCENE_BACKGROUND"),
    "reconstruction": ("gs_scene_reconstruction", "SCENE_BACKGROUND"),
    "quarantined_archive": ("gs_scene_quarantined_archive", "SCENE_BACKGROUND"),
    "command_gallery": ("gs_scene_command_gallery", "SCENE_BACKGROUND"),
    "sealwright_portrait": ("gs_char_sealwright", "SCENE_CHARACTER"),
}
ASSET_FOLDER = "GhostShip"

# Boss innate IDG (RUL-2026-10-12-004): one 99-round increasedamagegiven per boss.
BOSS_IDG = {CAPTAIN: 375, CROWNED: 450, "sealwright": 375}

# New-schema item columns Forge 0.5.0 (pinned 345d18ac) does not know. Its pre-send validator
# refuses unknown keys, so they are omitted; the generator asserts each is at its server default.
ITEM_SERVER_DEFAULTS = {
    "auctionMaxPrice": None, "auctionMinPrice": None, "coordinateTargeting": None,
    "purchaseLimit": None, "purchaseLimitPeriod": "NONE", "requiredBloodlineMastery": None,
    "requiredBukijutsuMastery": None, "requiredGenjutsuMastery": None,
    "requiredNinjutsuMastery": None, "requiredSageMastery": None, "requiredSkillId": None,
    "requiredTaijutsuMastery": None,
}
ITEM_DROP = {"id", "createdAt", "updatedAt", "expireFromStoreAt"}

# Sealwright = the regular Captain's profile (RUL-2026-10-12-008 item 5). Keys Forge knows at its
# pin go on the create; the post-0056 columns it refuses before a create go on a follow-up edit,
# where the live row makes them known keys.
SEALWRIGHT_CREATE_KEYS = [
    "level", "rank", "statsMultiplier", "poolsMultiplier", "regeneration", "gender",
    "preferredGeneral1", "preferredGeneral2", "primaryElement", "secondaryElement",
    "strength", "intelligence", "willpower", "speed", "isSummon", "avatarFacing",
]
SEALWRIGHT_POST0056_KEYS = [
    "offence", "defence", "ninjutsuMastery", "genjutsuMastery", "taijutsuMastery",
    "bukijutsuMastery", "bloodlineMastery", "sageMastery",
]

COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
PENDING_TEXT = "Pending director text."


class BuildError(SystemExit):
    pass


def fail(msg: str) -> None:
    raise BuildError("BUILD REFUSED: " + msg)


def load(rel: str) -> Any:
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return json.load(fh)


def sha256_file(rel: str) -> str:
    with open(os.path.join(ROOT, rel), "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def stable(v: Any) -> str:
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def ptr(doc: Any, pointer: str) -> Any:
    cur = doc
    for raw in pointer.strip("/").split("/"):
        t = raw.replace("~1", "/").replace("~0", "~")
        cur = cur[int(t)] if isinstance(cur, list) else cur[t]
    return cur


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", ROOT, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)


# --------------------------------------------------------------------------------------------
# captures


def captures(rel: str, proc: str) -> list[dict]:
    doc = load(rel)
    return [c["data"] for c in doc.get("captures", []) if c.get("proc") == proc and isinstance(c.get("data"), dict)]


def p86_ais() -> dict[str, dict]:
    return {d["userId"]: d for d in captures(P86, "profile.getAi")}


def p86_profiles() -> dict[str, dict]:
    return {d["id"]: d for d in captures(P86, "ai.getAiProfile")}


def item_row(rel: str, item_id: str) -> dict:
    for d in captures(rel, "item.get"):
        if d.get("id") == item_id:
            return copy.deepcopy(d)
    fail(f"item {item_id} not captured in {rel}")
    return {}


# --------------------------------------------------------------------------------------------
# presentation and art


def presentation(final: bool) -> tuple[dict, list[str]]:
    doc = load(PRESENTATION)
    pending = []
    out = {}
    for key, slots in doc["items"].items():
        out[key] = {}
        for field in ("description", "battleDescription"):
            v = slots.get(field)
            if v is None:
                pending.append(f"{key}.{field}")
                v = PENDING_TEXT
            elif not isinstance(v, str) or not v.strip():
                fail(f"{PRESENTATION}: {key}.{field} must be a non-empty string or null")
            out[key][field] = v
        fx = slots.get("effectPresentation")
        if fx is not None:
            allowed = {"appearAnimation", "staticAnimation", "disappearAnimation", "appearSfx", "disappearSfx", "staticAssetPath"}
            if not isinstance(fx, dict) or set(fx) - allowed:
                fail(f"{PRESENTATION}: {key}.effectPresentation has keys outside {sorted(allowed)}")
        out[key]["effectPresentation"] = fx
    if final and pending:
        fail("director presentation text missing: " + ", ".join(pending))
    return out, pending


class Art:
    """Art slots -> @img names. Final mode binds each to an immutable blob at --image-ref."""

    def __init__(self, final: bool, image_ref: str | None):
        doc = load(ART)
        self.final = final
        self.ref = image_ref
        self.required = doc["required"]
        self.optional = {k: v for k, v in doc.get("optional", {}).items() if not k.startswith("_")}
        self.pending: list[str] = []
        self.files: dict[str, dict] = {}
        self.sizes: dict[str, int] = {}
        if final:
            missing = [k for k, v in self.required.items() if not v]
            if missing:
                fail("required art slots unbound: " + ", ".join(missing))
            if not image_ref or not COMMIT_RE.fullmatch(image_ref):
                fail("--final needs --image-ref <40-hex commit>")
            if git("cat-file", "-e", f"{image_ref}^{{commit}}").returncode:
                fail(f"--image-ref {image_ref} is not a local commit")
            if git("merge-base", "--is-ancestor", image_ref, "HEAD").returncode:
                fail(f"--image-ref {image_ref} is not an ancestor of HEAD")

    def _bind(self, slot: str, path: str) -> str:
        name = os.path.basename(path)
        if not re.fullmatch(r"[A-Za-z0-9_.\-]+\.webp", name):
            fail(f"art {slot}: {path} must be a plain .webp filename")
        if self.ref:
            proc = git("show", f"{self.ref}:{path}")
            if proc.returncode:
                fail(f"art {slot}: {path} not readable at {self.ref}")
            blob = proc.stdout
            if len(blob) > 512 * 1024:
                fail(f"art {slot}: {path} exceeds the 512KB presign cap (law 35)")
            prev = self.files.get(name)
            entry = {"path": path, "sha256": hashlib.sha256(blob).hexdigest(), "bytes": len(blob)}
            if prev and prev != entry:
                fail(f"art: two slots bind {name} to different blobs")
            self.files[name] = entry
            self.sizes[name] = len(blob)
        return "@img:" + name

    def image(self, slot: str) -> str:
        """A required slot: bound ref, or a labelled pending ref in draft mode."""
        path = self.required.get(slot)
        if path:
            return self._bind(slot, path)
        self.pending.append(slot)
        return "@img:PENDING_" + re.sub(r"[^A-Za-z0-9_.\-]", "_", slot) + ".webp"

    def replacement(self, slot: str) -> str | None:
        path = self.optional.get(slot)
        return self._bind(slot, path) if path else None


# --------------------------------------------------------------------------------------------
# items


def forge_item_fields() -> set[str]:
    f = load(FORGE_FIELDS)["entities"]["item"]
    return set(f if isinstance(f, list) else f.get("fields", f))


def to_item_data(record: dict, fields: set[str], label: str) -> dict:
    data = {}
    for k, v in record.items():
        if k in ITEM_DROP:
            continue
        if k in ITEM_SERVER_DEFAULTS:
            if v != ITEM_SERVER_DEFAULTS[k]:
                fail(f"{label}: {k}={v!r} is not the server default, and Forge 0.5.0 cannot send it")
            continue
        if k not in fields:
            fail(f"{label}: field {k} unknown to Forge's pinned item field set")
        data[k] = copy.deepcopy(v)
    return data


def apply_effect_presentation(effects: list[dict], fx: dict | None) -> None:
    if fx:
        for e in effects:
            e.update(fx)


def build_items(pres: dict, art: Art, report: dict) -> tuple[list[dict], list[dict]]:
    fields = forge_item_fields()
    packet = load(RECORDS)
    creates, edits = [], []

    # Filament: Fragment-of-the-Crown chassis (the only captured MATERIAL row), RUL-008 overrides.
    frag = item_row(OCT1_ITEMS, FRAGMENT)
    filament = dict(frag)
    filament.update({
        "name": "Skyglass Filament", "itemType": "MATERIAL", "rarity": "RARE", "canBeTraded": True,
        "hidden": True, "inShop": False, "canBeCrafted": False, "effects": [],
        "description": pres["skyglass_filament"]["description"],
        "battleDescription": pres["skyglass_filament"]["battleDescription"],
        "image": art.image("item:skyglass_filament"),
    })
    # Katana / Crystal: the reviewed derived records (harness/ghost_ship_final, r2).
    katana = copy.deepcopy(packet["katana"]["record"])
    crystal = copy.deepcopy(packet["crystal"]["record"])
    for rec, key in ((katana, "skyglass_katana"), (crystal, "skyglass_crystal")):
        rec["description"] = pres[key]["description"]
        rec["battleDescription"] = pres[key]["battleDescription"]
        rec["image"] = art.image("item:" + key)
        apply_effect_presentation(rec["effects"], pres[key]["effectPresentation"])
    if crystal["craftingRequirements"] != [{"ids": [REF["filament"]], "number": 12}] or crystal["canBeCrafted"] is not True:
        fail("Crystal record does not carry the RUL-2026-10-12-005 recipe")
    # Reliquary: Endless Night Chest chassis; loot table from the reward decisions.
    chest = item_row(CHEST_DONOR_CAPTURE, CHEST_DONOR)
    reliquary = dict(chest)
    eff = copy.deepcopy(chest["effects"][0])
    if eff.get("type") != "noncombatconsumereward" or len(chest["effects"]) != 1:
        fail("chest donor is not a single-effect noncombatconsumereward chest")
    eff["description"] = "Skyglass Reliquary loot table"
    eff["reward_items"] = [
        {"ids": [REF["filament"]], "number": 100, "quantity": 1},
        {"ids": [RARE_JEWELS], "number": 100, "quantity": 3},
        {"ids": [REF["filament"]], "number": 25, "quantity": 1},
        {"ids": [SERUM], "number": 30, "quantity": 1},
        {"ids": [ORNATE_CHEST], "number": 15, "quantity": 1},
        {"ids": [REF["crystal"]], "number": 3, "quantity": 1},
    ]
    reliquary.update({
        "name": "Skyglass Reliquary", "rarity": "LEGENDARY", "canBeTraded": False, "hidden": True,
        "inShop": False, "cost": 1, "effects": [eff],
        "description": pres["skyglass_reliquary"]["description"],
        "battleDescription": pres["skyglass_reliquary"]["battleDescription"],
        "image": art.image("item:skyglass_reliquary"),
    })
    for k, v in (("itemType", "CONSUMABLE"), ("slot", "ITEM"), ("destroyOnUse", True), ("preventBattleUsage", True),
                 ("actionCostPerc", 60), ("stackSize", 999), ("canStack", True), ("requiredLevel", 1)):
        if reliquary.get(k) != v:
            fail(f"Reliquary chassis {k}={reliquary.get(k)!r}, expected {v!r}")

    order = [("filament", filament, "Skyglass Filament"), ("crystal", crystal, "Skyglass Crystal"),
             ("katana", katana, "Skyglass Katana"), ("reliquary", reliquary, "Skyglass Reliquary")]
    for key, rec, name in order:
        creates.append({"entity": "item", "slot": "create", "phase": 2, "name": name, "srcId": SRC[key],
                        "data": to_item_data(rec, fields, name)})

    report["itemChassis"] = {
        "Skyglass Filament": {"donor": f"{OCT1_ITEMS} item {FRAGMENT} (Fragment of the White Crown)",
                              "ruled": ["itemType MATERIAL", "rarity RARE", "canBeTraded true"],
                              "mirroredUndecided": {k: frag[k] for k in ("stackSize", "cost", "isEventItem", "target", "slot", "preventBattleUsage", "actionCostPerc")}},
        "Skyglass Reliquary": {"donor": f"{CHEST_DONOR_CAPTURE} item {CHEST_DONOR} (Endless Night Chest)",
                               "ruled": ["rarity LEGENDARY", "canBeTraded false", "loot table per reward decisions"],
                               "mirroredUndecided": {k: chest[k] for k in ("stackSize", "isEventItem", "actionCostPerc", "target", "battleUsageType")}},
        "Skyglass Katana": {"source": RECORDS + " katana.record (sha256 " + sha256_file(RECORDS) + ")"},
        "Skyglass Crystal": {"source": RECORDS + " crystal.record (Heal Crystal III mirror, 12-Filament recipe)"},
    }

    # Edits: Skyglass Serum (director text), Fragment and Crown (accepted patch text).
    patch = load(RETHEME)["itemChanges"]
    serum = {"name": "Skyglass Serum", "description": pres["skyglass_serum"]["description"],
             "battleDescription": pres["skyglass_serum"]["battleDescription"]}
    frag_edit = {k: patch[FRAGMENT][k] for k in ("name", "description", "battleDescription")}
    crown_edit = {k: patch[CROWN][k] for k in ("name", "description", "battleDescription")}
    for target, data, name in ((SERUM, serum, "Skyglass Serum (rename + text)"),
                               (FRAGMENT, frag_edit, "Fragment of the Skyglass Crown (rename + text)"),
                               (CROWN, crown_edit, "The Skyglass Crown (rename + text)")):
        img = art.replacement("item:" + target)
        if img:
            data["image"] = img
        edits.append({"entity": "item", "slot": "edit", "phase": 3, "name": name, "targetId": target, "data": data})
    return creates, edits


# --------------------------------------------------------------------------------------------
# AIs


def member_id(kit: dict, member: str) -> str:
    if member.startswith("legacy:"):
        return member[len("legacy:"):]
    return kit["sharedReferences"][member]["id"]


def pool_gates() -> dict[str, int]:
    recs = load(ROOT_POOL)["records"]
    rows = recs.values() if isinstance(recs, dict) else recs
    return {r["id"]: r["gate"] for r in rows if r.get("gate") is not None}


def normalize_gates(rules: list[dict], gates: dict[str, int]) -> list[str]:
    """Law 40 as Forge enforces it: every distance_lower_than on a pool-jutsu rule equals range+1."""
    changes = []
    for i, rule in enumerate(rules):
        g = gates.get(rule["action"].get("jutsuId") or "")
        if g is None:
            continue
        for c in rule["conditions"]:
            if c.get("type") == "distance_lower_than" and c.get("value") != g:
                changes.append(f"rule {i}: distance_lower_than {c['value']} -> {g} (law 40)")
                c["value"] = g
    return changes


def remap_rules(rules: list[dict], mapping: dict[str, str]) -> tuple[list[dict], list[str]]:
    """RUL-2026-10-12-003, identical to the harness's F.remappedRules."""
    out = copy.deepcopy(rules)
    changes = []
    for i, rule in enumerate(out):
        a = rule["action"]
        jid = a.get("jutsuId")
        if jid and mapping.get(jid) and mapping[jid] != jid:
            changes.append(f"rule {i}: jutsuId {jid} -> {mapping[jid]}")
            a["jutsuId"] = mapping[jid]
        if isinstance(a.get("comboIds"), list):
            before = list(a["comboIds"])
            mapped = [mapping.get(x, x) for x in a["comboIds"]]
            a["comboIds"] = [x for k, x in enumerate(mapped) if k == 0 or x != mapped[k - 1]]
            if before != a["comboIds"]:
                changes.append(f"rule {i}: combo {','.join(before)} -> {','.join(a['comboIds'])}")
    return out, changes


def cond(kind: str, **kw: Any) -> dict:
    desc = {
        "health_below": "Health below given percentage",
        "distance_lower_than": "Distance lower than or equal given value",
        "distance_higher_than": "Distance higher than or equal given value",
        "target_has_effect": "Target is affected by a specific effect",
    }[kind]
    return {"type": kind, "description": desc, **kw}


def use(jutsu_id: str, target: str) -> dict:
    return {"type": "use_specific_jutsu", "description": "Select specific jutsu", "jutsuId": jutsu_id, "target": target}


def crowned_support_rules() -> list[dict]:
    """RUL-2026-10-12-001, the tested order (harness/ghost_ship_final/engine/crowned_support.test.ts)."""
    return [
        {"conditions": [cond("health_below", value=40)], "action": use(S35, "SELF")},
        {"conditions": [cond("target_has_effect", effectType="increasedamagegiven", target="CLOSEST_OPPONENT", threshold=71),
                        cond("distance_lower_than", value=5, target="CLOSEST_OPPONENT")],
         "action": use(B07, "CLOSEST_OPPONENT")},
        {"conditions": [], "action": use(REFLECT, "SELF")},
    ]


def sealwright_rules() -> tuple[list[dict], list[str]]:
    """RUL-2026-10-12-002: the accepted proposal's ten-step priority, built on the contract's rules."""
    plan = load(CONTRACT)["aiProfile"]["priorityOrderedRulePlan"]
    keep = [r for r in plan if r.get("jutsuCode")]
    codes = [r["jutsuCode"] for r in keep]
    if codes != ["B32", "S31", "B22", "B16", "B14", "B33", "S27"]:
        fail(f"Sealwright contract order changed: {codes}")
    rules = [{"conditions": copy.deepcopy(r["conditions"]), "action": copy.deepcopy(r["action"])} for r in keep]
    rules += [
        {"conditions": [cond("distance_lower_than", value=2, target="CLOSEST_OPPONENT")],
         "action": {"type": "use_combo_action", "description": "Cycly through a specific combo of jutsu & items",
                    "comboIds": ["basicAttack"], "target": "CLOSEST_OPPONENT"}},
        {"conditions": [cond("distance_higher_than", value=3, target="CLOSEST_OPPONENT")],
         "action": {"type": "move_towards_opponent", "description": "Move towards opponent", "target": "CLOSEST_OPPONENT"}},
        {"conditions": [], "action": {"type": "end_turn", "description": "End turn"}},
    ]
    jutsus = [j["liveJutsuId"] for j in load(CONTRACT)["jutsus"]]
    return rules, jutsus


def idg_entry(template: dict, power: int) -> dict:
    e = copy.deepcopy(template)
    e["power"] = power
    return e


def build_ais(art: Art, report: dict, gate_policy: str) -> tuple[list[dict], list[dict], list[dict], set[str]]:
    kit = load(KIT)
    legacy = load(LEGACY)
    legacy_ids = {c["targetId"] for c in legacy["conversions"]}
    renames = load(RETHEME)["aiRenames"]
    loot = load(RETHEME)["lootCorrections"]
    live = p86_ais()
    profiles = p86_profiles()
    idg_template = next(e for e in live[CROWNED]["effects"] if e["type"] == "increasedamagegiven")
    unequip, final, sealwright = [], [], []
    ledger: dict[str, Any] = {}
    gates = pool_gates()

    for ent in kit["entities"]:
        uid = ent["aiId"]
        row = live[uid]
        prof = profiles[row["aiProfileId"]]
        name = renames[uid]
        if name != ent["name"]:
            fail(f"{uid}: retheme name {name!r} != kit name {ent['name']!r}")
        live_kit = [j["jutsuId"] for j in row["jutsus"]]
        new_kit = [member_id(kit, m) for m in ent["proposedKit"]]
        if len(set(new_kit)) != len(new_kit):
            fail(f"{name}: duplicate kit member")

        # Phase 4: unequip every retained legacy jutsu this AI holds live (law 18 / law 60).
        held = [j for j in live_kit if j in legacy_ids]
        if held:
            unequip.append({"entity": "ai", "slot": "edit", "phase": 4, "targetId": uid,
                            "name": f"{name}: unequip retained legacy jutsu before text edit (law 60)",
                            "data": {"jutsus": [j for j in live_kit if j not in legacy_ids]}})

        data: dict[str, Any] = {"username": name, "jutsus": new_kit}
        entry: dict[str, Any] = {"liveName": row["username"], "name": name, "kit": new_kit, "unequipped": held}

        # Rules: remap (RUL-003); Crowned gets the support prefix (RUL-001); Captain is untouched.
        mapping = {m["fromId"]: member_id(kit, m["to"]) for m in ent["mapping"]}
        rules, changes = remap_rules(prof["rules"], mapping)
        if uid == CROWNED:
            rules = crowned_support_rules() + rules
            changes = ["prefix S35 / B07 / Reflect support rules (RUL-2026-10-12-001)"] + changes
        if uid == CAPTAIN and changes:
            fail("regular Captain's rules changed under remap; RUL-003 says none")
        gate_changes = normalize_gates(rules, gates) if gate_policy == "law40" else []
        changes = changes + gate_changes
        entry["gateChanges"] = gate_changes
        probe = copy.deepcopy(rules)
        entry["gatesBelowRangePlusOne"] = normalize_gates(probe, gates)
        if changes:
            data["rules"] = rules
            data["includeDefaultRules"] = prof["includeDefaultRules"]
        entry["ruleChanges"] = changes
        missing = sorted({r["action"]["jutsuId"] for r in rules if r["action"].get("jutsuId")} - set(new_kit))
        entry["rulesReferencingUnequipped"] = missing

        # Loot (retheme lootCorrections; Katana 3% on Crowned, RUL004/005 reward decisions).
        if uid in loot or uid == CROWNED:
            items = [{"ids": [i["itemId"]], "number": i["dropChancePerc"]} for i in row["items"]]
            if any(DIADEM in t["ids"] for t in items):
                fail("Diadem still attached to an AI; legacyCleanup not satisfied live")
            for t in items:
                iid = t["ids"][0]
                if iid in loot.get(uid, {}):
                    t["number"] = loot[uid][iid]
            if uid == CROWNED:
                items.append({"ids": [REF["katana"]], "number": 3})
            data["items"] = items
            entry["items"] = items

        # Boss innate IDG (RUL-2026-10-12-004).
        if uid in BOSS_IDG:
            eff = copy.deepcopy(row["effects"])
            if uid == CROWNED:
                idg = [e for e in eff if e["type"] == "increasedamagegiven"]
                if len(idg) != 1 or idg[0]["power"] != 60 or idg[0]["rounds"] != 99:
                    fail("Crowned captured innate is not the single 60%/99r IDG RUL-004 replaces")
                eff = [idg_entry(idg_template, BOSS_IDG[uid]) if e is idg[0] else e for e in eff]
            else:
                if any(e["type"] == "increasedamagegiven" for e in eff):
                    fail("regular Captain already carries an innate IDG")
                eff.append(idg_entry(idg_template, BOSS_IDG[uid]))
            data["effects"] = eff
            entry["effects"] = [(e["type"], e["power"], e["rounds"]) for e in eff]

        img = art.replacement("ai:" + uid)
        if img:
            data["avatar"] = img
        final.append({"entity": "ai", "slot": "edit", "phase": 6, "targetId": uid,
                      "name": f"{name}: rename, kit, rules, loot, innate", "data": data})
        ledger[uid] = entry

    # Sealwright create (RUL-002 / RUL-004 / RUL-008): the regular Captain's profile.
    cap = live[CAPTAIN]
    rules, jutsus = sealwright_rules()
    data = {"username": "Sealwright", "hidden": True}
    for k in SEALWRIGHT_CREATE_KEYS:
        data[k] = cap[k]
    # Forge lint L05 requires preferredStat on an AI create. The column predates migration 0056
    # and the live row no longer has it (the server strips it); the Captain's last value is used.
    oct1_cap = next(d for d in captures(OCT1_ITEMS, "profile.getAi") if d["userId"] == CAPTAIN)
    data["preferredStat"] = oct1_cap["preferredStat"]
    data.update({"avatar": art.image("ai:sealwright"), "jutsus": jutsus, "items": [],
                 "effects": [idg_entry(idg_template, BOSS_IDG["sealwright"])],
                 "rules": rules, "includeDefaultRules": False})
    sealwright.append({"entity": "ai", "slot": "create", "phase": 6, "name": "Sealwright", "srcId": SRC["sealwright"], "data": data})
    sealwright.append({"entity": "ai", "slot": "edit", "phase": 7, "targetId": REF["sealwright"],
                       "name": "Sealwright: post-0056 combat stats and masteries equal the regular Captain",
                       "data": {k: cap[k] for k in SEALWRIGHT_POST0056_KEYS}})
    ledger["sealwright"] = {"profileFrom": CAPTAIN, "createKeys": SEALWRIGHT_CREATE_KEYS,
                            "followUpKeys": SEALWRIGHT_POST0056_KEYS, "kit": jutsus, "rules": len(rules)}
    report["ais"] = ledger
    return unequip, final, sealwright, legacy_ids


# --------------------------------------------------------------------------------------------
# legacy jutsu


def build_jutsu_edits(report: dict) -> list[dict]:
    legacy = load(LEGACY)
    live_rows: dict[str, dict] = {}
    for row in p86_ais().values():
        for uj in row["jutsus"]:
            live_rows.setdefault(uj["jutsuId"], uj["jutsu"])
    out = []
    drift = {}
    for c in legacy["conversions"]:
        jid = c["targetId"]
        row = live_rows.get(jid)
        if row is None:
            fail(f"legacy jutsu {jid} not equipped by any push/86 Ghost Ship AI")
        before = {k: row[k] for k in ("name", "description", "battleDescription")}
        if before != c["before"]:
            drift[jid] = {"packet": c["before"], "push86": before}
        # law 20: injectableInBattle defaults to false when absent; carry the live value explicitly.
        data = {**c["after"], "injectableInBattle": row["injectableInBattle"]}
        out.append({"entity": "jutsu", "slot": "edit", "phase": 5, "targetId": jid,
                    "name": f"{c['after']['name']} (was {before['name']})", "data": data})
    if drift:
        fail("legacy jutsu presentation drifted since the conversion packet: " + stable(drift))
    report["legacyJutsu"] = {"count": len(out), "beforeTextMatchesPush86": True}
    return out


# --------------------------------------------------------------------------------------------
# assets


def build_assets(art: Art) -> tuple[list[dict], list[dict]]:
    creates, edits = [], []
    graph = load(GRAPH)
    legends = {**graph["sceneSymbolLegend"], **graph["characterSymbolLegend"]}
    for sym, (src, kind) in NEW_SCENES.items():
        name = legends[sym]["newAsset"]
        creates.append({"entity": "asset", "slot": "create", "phase": 1, "name": name, "srcId": src,
                        "data": {"name": name, "type": kind, "image": art.image("scene:" + src), "folder": ASSET_FOLDER,
                                 "frames": 1, "speed": 1, "hidden": True, "onInitialBattleField": False, "licenseDetails": "TNR"}})
    for aid, name in load(RETHEME)["sceneAssetRenames"].items():
        data: dict[str, Any] = {"name": name}
        img = art.replacement("asset:" + aid)
        if img:
            data["image"] = img
        edits.append({"entity": "asset", "slot": "edit", "phase": 3, "targetId": aid, "name": f"{name} (rename)", "data": data})
    return creates, edits


# --------------------------------------------------------------------------------------------
# quests


def edge_list(o: dict) -> list[str]:
    out = []
    n = o.get("nextObjectiveId")
    if isinstance(n, str) and n:
        out.append(n)
    elif isinstance(n, list):
        out += [c["nextObjectiveId"] for c in n if isinstance(c, dict) and c.get("nextObjectiveId")]
    for k in ("failObjectiveId", "resetObjectiveId"):
        if isinstance(o.get(k), str) and o[k]:
            out.append(o[k])
    return out


def scene_ref(sym: str, legends: dict) -> str:
    ent = legends[sym]
    if "existingId" in ent:
        return ent["existingId"]
    return "@scene:" + NEW_SCENES[sym][0]


def check_graph(objs: list[dict], label: str) -> dict:
    ids = [o["id"] for o in objs]
    if len(ids) != len(set(ids)):
        fail(f"{label}: duplicate objective id")
    by = {o["id"]: o for o in objs}
    for o in objs:
        for t in edge_list(o):
            if t not in by:
                fail(f"{label}: {o['id']} -> unknown {t}")
    root = objs[0]["id"]
    seen, q = {root}, deque([root])
    while q:
        for t in edge_list(by[q.popleft()]):
            if t not in seen:
                seen.add(t)
                q.append(t)
    if len(seen) != len(objs):
        fail(f"{label}: unreachable {sorted(set(ids) - seen)}")
    # forward graph (resets excluded) must be acyclic
    fwd = {o["id"]: [t for t in edge_list(o) if o.get("resetObjectiveId") != t] for o in objs}
    state: dict[str, int] = {}

    def dfs(n: str) -> None:
        state[n] = 1
        for t in fwd[n]:
            if state.get(t) == 1:
                fail(f"{label}: forward cycle through {n} -> {t}")
            if t not in state:
                dfs(t)
        state[n] = 2

    sys.setrecursionlimit(10000)
    dfs(root)
    preds: dict[str, list[str]] = {i: [] for i in ids}
    for o in objs:
        for t in edge_list(o):
            preds[t].append(o["id"])
    for o in objs:
        if o["task"] == "start_battle":
            bad = [p for p in preds[o["id"]] if by[p]["task"] not in ("dialog",) and by[p].get("resetObjectiveId") != o["id"]]
            if bad:
                fail(f"{label}: battle {o['id']} entered from non-dialog {bad}")
        if o["task"] == "dialog":
            if not isinstance(o["nextObjectiveId"], list) or not o["nextObjectiveId"]:
                fail(f"{label}: dialog {o['id']} needs explicit choices")
    endings = sorted(o["id"] for o in objs if o["task"] == "win_quest")
    return {"nodes": len(objs), "root": root, "endings": endings, "tasks": dict(Counter(o["task"] for o in objs))}


def build_quests(base_rel: str, final: bool, report: dict) -> list[dict]:
    retheme = load(RETHEME)
    graph = load(GRAPH)
    legends = {**graph["sceneSymbolLegend"], **graph["characterSymbolLegend"]}
    base = {d["id"]: d for d in captures(base_rel, "quests.get")}
    out = []
    qrep = {}
    observed_hidden: dict[str, Any] = {}
    for qid in QUEST_IDS:
        if qid not in base:
            fail(f"quest {qid} not in {base_rel}")
        q = copy.deepcopy(base[qid])
        # The fresh capture read hidden:false on both quests (event window ended 2026-09-21). The
        # edit asserts hidden:true, so the run hides them; the observed state is reported.
        observed_hidden[qid] = {"hidden": q.get("hidden"), "startsAt": q.get("startsAt"), "endsAt": q.get("endsAt")}
        content = q["content"]
        objs = content["objectives"]
        by = {o["id"]: o for o in objs}
        if len(objs) != 57:
            fail(f"{qid}: base has {len(objs)} objectives, expected 57")
        text = retheme["objectiveText"]
        if set(text) != set(by):
            fail(f"{qid}: objectiveText covers {len(text)} ids, base has {len(by)}; mismatch {sorted(set(text) ^ set(by))}")
        for oid, t in text.items():
            o = by[oid]
            o["description"] = t["description"]
            if "choices" in t:
                if not isinstance(o["nextObjectiveId"], list) or len(o["nextObjectiveId"]) != len(t["choices"]):
                    fail(f"{qid}/{oid}: {len(t['choices'])} choice texts for {o['nextObjectiveId']!r}")
                for c, label in zip(o["nextObjectiveId"], t["choices"]):
                    c["text"] = label
        # Fragment leaves the w_Co completion roll (questRewardCorrection).
        corr = retheme["questRewardCorrection"]
        node = by[corr["node"]]
        before = len(node["reward_items"])
        node["reward_items"] = [r for r in node["reward_items"] if corr["removeItemId"] not in r["ids"]]
        if len(node["reward_items"]) != before - 1:
            fail(f"{qid}: expected exactly one Fragment roll on {corr['node']}")
        # Twelve forward-edge rewires.
        for rw in graph["rewires"]:
            by[rw["id"]]["nextObjectiveId"] = copy.deepcopy(rw["nextObjectiveId"])
        # Twenty-six new nodes, each cloned from a same-task base node (field sets are uniform per
        # task in the base; location fields are therefore inherited, no new coordinates).
        tmpl = {}
        for o in objs:
            tmpl.setdefault(o["task"], o)
        captain_battle = next(o for o in objs if o["task"] == "start_battle"
                              and any(CAPTAIN in a["ids"] for a in o.get("opponentAIs", [])))
        tmpl["start_battle"] = captain_battle
        new_nodes = []
        for spec in graph["newNodes"]:
            n = copy.deepcopy(tmpl[spec["task"]])
            n["id"] = spec["id"]
            n["description"] = spec["description"]
            n["sceneBackground"] = scene_ref(spec["scene"], legends)
            n["sceneCharacters"] = [scene_ref(s, legends) for s in spec["sceneCharacters"]]
            if spec["task"] in ("dialog", "start_battle"):
                n["nextObjectiveId"] = copy.deepcopy(spec["nextObjectiveId"])
            if spec["task"] == "start_battle":
                n["failObjectiveId"] = spec["failObjectiveId"]
                opp = []
                for o in spec["opponents"]:
                    if o["aiSymbol"] != "sealwright":
                        fail(f"unknown AI symbol {o['aiSymbol']}")
                    opp.append({"ids": [REF["sealwright"]], "number": o["number"], "quantity": o["quantity"]})
                n["opponentAIs"] = opp
            if spec["task"] == "reset_quest":
                n["resetObjectiveId"] = spec["resetObjectiveId"]
            if spec["task"] == "win_quest":
                r = spec["reward"]
                if r["itemSymbol"] != "skyglass_reliquary":
                    fail("w_secret reward is not the Reliquary")
                n["reward_items"] = [{"ids": [REF["reliquary"]], "number": r["chance"], "quantity": r["quantity"]}]
            new_nodes.append(n)
        content["objectives"] = objs + new_nodes
        stats = check_graph(content["objectives"], qid)
        if stats["nodes"] != 83 or stats["endings"] != sorted(graph["scope"]["expectedEndings"]):
            fail(f"{qid}: graph {stats}")
        qtext = retheme["quests"][qid]
        data = {"name": qtext["name"], "description": qtext["description"],
                "successDescription": qtext["successDescription"], "hidden": True, "content": content}
        out.append({"entity": "quest", "slot": "edit", "phase": 8, "targetId": qid,
                    "name": f"{qtext['name']}: Skyglass retheme + 83-node expansion", "data": data})
        qrep[qid] = stats
    report["quests"] = {"base": base_rel, "baseSha256": sha256_file(base_rel), "graphs": qrep,
                        "baseVisibility": observed_hidden, "editAsserts": {"hidden": True}}
    return out


# --------------------------------------------------------------------------------------------
# captures


def capture_block() -> dict:
    live = p86_ais()
    reads = [{"proc": "quests.get", "input": {"id": q}, "persist": "full"} for q in QUEST_IDS]
    reads += [{"proc": "profile.getAi", "input": {"userId": u}, "persist": "full"} for u in live]
    reads += [{"proc": "ai.getAiProfile", "input": {"id": live[u]["aiProfileId"]}, "persist": "full"} for u in live]
    reads += [{"proc": "jutsu.get", "input": {"id": c["targetId"]}, "persist": "full"} for c in load(LEGACY)["conversions"]]
    reads += [{"proc": "item.get", "input": {"id": i}, "persist": "full"} for i in (SERUM, FRAGMENT, CROWN)]
    reads += [{"proc": "gameAsset.get", "input": {"id": a}, "persist": "full"} for a in load(RETHEME)["sceneAssetRenames"]]
    return {"before": copy.deepcopy(reads), "after": copy.deepcopy(reads)}


# --------------------------------------------------------------------------------------------


def build(final: bool, quest_base: str | None, image_ref: str | None, gate_policy: str) -> tuple[dict, dict]:
    report: dict[str, Any] = {"mode": "final" if final else "draft", "gatePolicy": gate_policy}
    if final:
        if quest_base == OCT1_QUESTS:
            fail("--final cannot use the stale October 1 quest capture")
        if gate_policy != "law40":
            fail("--final requires --gate-policy law40 (RUL-2026-10-12-009); Forge refuses the captured gates")
    base = quest_base or FRESH_QUESTS
    pres, pending_text = presentation(final)
    art = Art(final, image_ref)

    asset_creates, asset_edits = build_assets(art)
    item_creates, item_edits = build_items(pres, art, report)
    unequip, ai_final, sealwright, _ = build_ais(art, report, gate_policy)
    jutsu_edits = build_jutsu_edits(report)
    quests = build_quests(base, final, report)

    # Forge executes by `phase` (then refs), so array order is presentation only. Assets sit last
    # because validate.py renames "asset" to "gameAsset" before its build-order lookup, which ranks
    # it after every other entity; law 60 still puts the AI unequip before the jutsu edits.
    items = item_creates + item_edits + unequip + jutsu_edits + ai_final + sealwright + quests + asset_creates + asset_edits
    note = ("Ghost Ship / Skyglass combined release (RUL-2026-10-12-001..008). Generated by "
            "push/90_ghost_ship_skyglass_release.gen.py; do not hand-edit. Phases: 1 scene creates, 2 item creates, "
            "3 renames/item edits, 4 AI unequip of retained legacy jutsu, 5 legacy jutsu text, 6 AI final edits + "
            "Sealwright create, 7 Sealwright post-0056 stats, 8 quest edits. Everything new is created hidden; both "
            "quests stay hidden:true. Run by the operator only.")
    if not final:
        note = "DRAFT, NOT RUNNABLE: director text and art pending. " + note
    manifest: dict[str, Any] = {"_note": note, "dedupNames": True}
    if art.files:
        manifest["imgSizes"] = dict(sorted(art.sizes.items()))
        manifest["imagePack"] = {"ref": image_ref, "files": dict(sorted(art.files.items()))}
    manifest["items"] = items
    manifest["capture"] = capture_block()
    report["pending"] = {"presentationText": pending_text, "artSlots": art.pending}
    report["counts"] = dict(Counter(f"{i['entity']}.{i['slot']}" for i in items))
    report["inputs"] = {rel: sha256_file(rel) for rel in (P86, OCT1_ITEMS, CHEST_DONOR_CAPTURE, KIT, LEGACY, CONTRACT, RECORDS,
                                                          RETHEME, GRAPH, PRESENTATION, ART, base)}
    return manifest, report


def main() -> int:
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--draft", action="store_true")
    mode.add_argument("--final", action="store_true")
    ap.add_argument("--quest-base", help="committed quests.get results file (default: push/89 fresh capture)")
    ap.add_argument("--image-ref", help="40-hex commit holding the art (--final)")
    ap.add_argument("--gate-policy", choices=["captured", "law40"], default="law40",
                    help="law40 (RUL-2026-10-12-009, default): normalize remapped gates to range+1; captured: historical RUL-003 conditions, which Forge refuses")
    ap.add_argument("--check", action="store_true", help="do not write; fail unless the committed files are generator-exact")
    args = ap.parse_args()
    manifest, report = build(args.final, args.quest_base, args.image_ref, args.gate_policy)
    outputs = {OUT: json.dumps(manifest, indent=1, ensure_ascii=False) + "\n",
               REPORT: json.dumps(report, indent=1, ensure_ascii=False, sort_keys=True) + "\n"}
    if args.check:
        bad = 0
        for path, text in outputs.items():
            cur = open(path, encoding="utf-8").read() if os.path.exists(path) else None
            if cur != text:
                print(f"STALE: {os.path.relpath(path, ROOT)}", file=sys.stderr)
                bad = 1
        if not bad:
            print("OK: manifest and report are generator-exact")
        return bad
    for path, text in outputs.items():
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
    print(f"{os.path.relpath(OUT, ROOT)}: {len(manifest['items'])} items {report['counts']}; "
          f"pending text {len(report['pending']['presentationText'])}, art {len(report['pending']['artSlots'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
