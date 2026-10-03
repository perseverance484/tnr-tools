#!/usr/bin/env python3
"""Shared library for Bloodright planning tooling.

Planning-only analysis over the committed kit snapshot
(docs/design/bloodright/evidence/kit_snapshot.json) and roster
(docs/design/bloodright/roster.json). Nothing here contacts the game.

Mechanical facts encoded here were read at
studie-tech/TheNinjaRPG@16498fd776fad9c91e4b84efed4380fe3a487050:
- app/src/libs/combat/potency.ts (resolvePotencyTags): static modifier adds
  flat power before percentage scaling; percentage-valued tags are capped at
  100; powerPerLevel is baked in at jutsu level then zeroed.
- app/src/validators/combat.ts (PotencyTagTypes): the ten supported tags.
- app/src/validators/combat.ts (isPositive/isNegativeUserEffect) as projected
  in skills/building-tnr-content/data/46_DATA_tag_schemas.json _effectPolarity.
"""
from __future__ import annotations

import itertools
import json
import os
import re
from dataclasses import dataclass, field, asdict
from typing import Any

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DESIGN_DIR = os.path.join(REPO_ROOT, "docs", "design", "bloodright")
SNAPSHOT_PATH = os.path.join(DESIGN_DIR, "evidence", "kit_snapshot.json")
ROSTER_PATH = os.path.join(DESIGN_DIR, "roster.json")

GAME_SOURCE_PIN = "16498fd776fad9c91e4b84efed4380fe3a487050"
DEFAULT_JUTSU_LEVEL = 25
BP_CAP = 4
NODE_COST = 1
MAX_NODES = 10

SUPPORTED_TAGS: tuple[str, ...] = (
    "damage",
    "increasedamagegiven",
    "decreasedamagegiven",
    "increasedamagetaken",
    "decreasedamagetaken",
    "afterburn",
    "lifesteal",
    "reflect",
    "increaseheal",
    "heal",
)

TAG_LABELS = {
    "damage": "Damage",
    "increasedamagegiven": "Increase Damage Given",
    "decreasedamagegiven": "Decrease Damage Given",
    "increasedamagetaken": "Increase Damage Taken",
    "decreasedamagetaken": "Decrease Damage Taken",
    "afterburn": "Afterburn",
    "lifesteal": "Lifesteal",
    "reflect": "Reflect",
    "increaseheal": "Increase Heal",
    "heal": "Heal",
}

TAG_ABBR = {
    "damage": "DMG",
    "increasedamagegiven": "IDG",
    "decreasedamagegiven": "DDG",
    "increasedamagetaken": "IDT",
    "decreasedamagetaken": "DDT",
    "afterburn": "AB",
    "lifesteal": "LS",
    "reflect": "REF",
    "increaseheal": "IH",
    "heal": "HEAL",
}

# Engine polarity (isPositiveUserEffect / isNegativeUserEffect projection).
POSITIVE_TAGS = {
    "absorb", "clearprevent", "debuffprevent", "decreasedamagetaken",
    "decreasepoolcost", "heal", "increasedamagegiven", "increaseheal",
    "increasemaxpools", "increasestat", "increaserange", "decreasecooldown",
    "lifesteal", "move", "moveprevent", "onehitkillprevent", "reflect",
    "robprevent", "sealprevent", "shield", "stealth", "stunprevent", "summon",
    "timedilation", "injectjutsus", "immunity", "barrier", "consume", "vamp",
}
NEGATIVE_TAGS = {
    "afterburn", "buffprevent", "cleanseprevent", "clear", "damage",
    "decreasedamagegiven", "decreaseheal", "decreasestat", "decreasemaxpools",
    "drain", "elementalseal", "flee", "fleeprevent", "healprevent",
    "increasedamagetaken", "increasepoolcost", "increasecooldown", "moveprevent",
    "onehitkill", "pierce", "poison", "recoil", "redirection", "rob", "seal",
    "summonprevent", "timecompression", "weakness", "wound", "stun", "mirror",
    "copy",
}

TIERS = ("Foundation", "Hidden Art", "Advanced Art")
BASIC_ELEMENTS = {"Fire", "Water", "Wind", "Earth", "Lightning"}

ROLE_COLORS = {
    "SELF BUFF": "#7cdbc7",
    "ALLY BUFF": "#7cdbc7",
    "ENEMY DEBUFF": "#f09aaf",
    "DAMAGE": "#e5bb69",
    "SELF DEBUFF": "#ff8a65",
    "ENEMY BUFF": "#ff8a65",
}

JOKE_WORDS = {"kaboom", "boom", "lol", "yolo", "pew", "bonk", "zap", "oops", "lmao", "meme"}


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def dump_json(path: str, data: Any) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False, sort_keys=False)
        fh.write("\n")


def write_text(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def load_snapshot() -> dict:
    return load_json(SNAPSHOT_PATH)


def load_roster() -> dict:
    return load_json(ROSTER_PATH)


def slugify(name: str) -> str:
    s = name.strip().lower()
    s = s.replace("'", "").replace("’", "").replace("–", "-")
    s = re.sub(r"[^a-z0-9]+", "_", s)
    return s.strip("_")


def census_index(snapshot: dict, roster: dict) -> dict[str, dict]:
    """bloodline_id -> {kit, record}"""
    recs = {r["bloodline_id"]: r for r in roster["records"]}
    out = {}
    for kit in snapshot["kits"]:
        bid = kit["bloodline"]["id"]
        out[bid] = {"kit": kit, "record": recs.get(bid)}
    return out


# ---------------------------------------------------------------------------
# Row classification
# ---------------------------------------------------------------------------

def scaled_power(effect: dict, level: int) -> float:
    power = float(effect.get("power", 0) or 0)
    ppl = float(effect.get("powerPerLevel", 0) or 0)
    return power + ppl * level


def effective_elements(effect: dict) -> list[str]:
    """Resolver fallback: an absent/empty element list matches ['None']."""
    els = effect.get("elements")
    if isinstance(els, list) and len(els) > 0:
        return list(els)
    return ["None"]


def recipient_for(jutsu: dict, effect: dict) -> tuple[str, str]:
    """Return (raw_recipient, effective_recipient).

    raw: self | enemy | ally | area_allies | area_enemies | area_all
    effective collapses area_all by polarity (negative -> enemy, positive -> self).
    """
    tag = effect.get("type")
    etarget = effect.get("target") or "INHERIT"
    jtarget = jutsu.get("target")
    ff = effect.get("friendlyFire")
    if etarget == "SELF":
        raw = "self"
    elif etarget in ("OTHER_USER", "OPPONENT"):
        raw = "enemy"
    elif etarget == "ALLY":
        raw = "ally"
    else:  # INHERIT
        if jtarget == "SELF":
            raw = "self"
        elif jtarget in ("OTHER_USER", "OPPONENT"):
            raw = "enemy"
        elif jtarget == "ALLY":
            raw = "ally"
        elif jtarget in ("GROUND", "EMPTY_GROUND", "CHARACTER"):
            if ff == "FRIENDLY":
                raw = "area_allies"
            elif ff == "ENEMIES":
                raw = "area_enemies"
            else:
                raw = "area_all"
        else:
            raw = "area_all"
    if raw == "area_all":
        eff = "enemy" if tag in NEGATIVE_TAGS else "self"
    elif raw == "area_enemies":
        eff = "enemy"
    elif raw == "area_allies":
        eff = "self" if tag in POSITIVE_TAGS else "enemy"
    else:
        eff = raw
    return raw, eff


def role_for(tag: str, eff_recipient: str) -> tuple[str, bool]:
    """Return (display_role, adverse)."""
    if tag == "damage":
        return "DAMAGE", False
    positive = tag in POSITIVE_TAGS
    if eff_recipient in ("self",):
        return ("SELF BUFF", False) if positive else ("SELF DEBUFF", True)
    if eff_recipient == "ally":
        return ("ALLY BUFF", False) if positive else ("ENEMY DEBUFF", True)
    # enemy
    return ("ENEMY BUFF", True) if positive else ("ENEMY DEBUFF", False)


@dataclass
class Row:
    jutsu_id: str
    jutsu_name: str
    jutsu_rank: str
    jutsu_type: str
    bloodline_id_on_jutsu: str
    row: int
    tag: str
    label: str
    calculation: str
    base: float
    power: float
    power_per_level: float
    rounds: Any
    elements: list[str]
    elements_effective: list[str]
    target: str
    jutsu_target: str
    friendly_fire: Any
    recipient_raw: str
    recipient: str
    role: str
    adverse: bool
    stat_types: Any
    general_types: Any
    direction: Any
    supported: bool
    visibility: str  # public | hidden
    item_gate: Any
    usage: Any
    injectable: Any
    jutsu_hidden: Any
    ap_cost: Any
    cooldown: Any
    method: Any
    range: Any
    ally_hazard: bool = False

    def as_dict(self) -> dict:
        return asdict(self)


def kit_rows(kit: dict, level: int = DEFAULT_JUTSU_LEVEL, include_unsupported: bool = True) -> list[Row]:
    rows: list[Row] = []
    for vis, key in (("public", "public_jutsu"), ("hidden", "hidden_jutsu")):
        for j in kit.get(key, []):
            for i, e in enumerate(j.get("effects", [])):
                tag = e.get("type")
                sup = tag in SUPPORTED_TAGS
                if not sup and not include_unsupported:
                    continue
                raw, eff = recipient_for(j, e)
                role, adverse = role_for(tag, eff)
                # Friendly fire: checkFriendlyFire (process.ts 154-183 at the pin) treats an absent
                # friendlyFire as ALL, so a harmful row delivered by an area method or a ground
                # target with friendlyFire None/ALL also lands on allies (and the caster) in the area.
                area = str(j.get("method") or "").startswith("AOE_") or j.get("target") in ("GROUND", "EMPTY_GROUND")
                hazard = bool(area and e.get("target", "INHERIT") in (None, "INHERIT") and tag in NEGATIVE_TAGS
                              and e.get("friendlyFire") in (None, "ALL") and eff == "enemy")
                rows.append(Row(
                    jutsu_id=j["id"], jutsu_name=j["name"], jutsu_rank=j.get("jutsuRank"),
                    jutsu_type=j.get("jutsuType"), bloodline_id_on_jutsu=j.get("bloodlineId"),
                    row=i, tag=tag, label=TAG_LABELS.get(tag, tag), calculation=e.get("calculation"),
                    base=round(scaled_power(e, level), 4), power=e.get("power"),
                    power_per_level=e.get("powerPerLevel"), rounds=e.get("rounds"),
                    elements=list(e.get("elements") or []), elements_effective=effective_elements(e),
                    target=e.get("target") or "INHERIT", jutsu_target=j.get("target"),
                    friendly_fire=e.get("friendlyFire"), recipient_raw=raw, recipient=eff,
                    role=role, adverse=adverse, stat_types=e.get("statTypes"),
                    general_types=e.get("generalTypes"), direction=e.get("direction"),
                    supported=sup, visibility=vis, item_gate=j.get("requiredBloodlineItemId"),
                    usage=j.get("battleUsageType"), injectable=j.get("injectableInBattle"),
                    jutsu_hidden=j.get("hidden"), ap_cost=j.get("actionCostPerc"),
                    cooldown=j.get("cooldown"), method=j.get("method"), range=j.get("range"),
                    ally_hazard=hazard,
                ))
    return rows


def injected_children(kit: dict, snapshot: dict) -> list[dict]:
    """Jutsu reachable through injectjutsus rows on this kit, resolved from the
    snapshot's injected dependency tables (public first, then extended)."""
    deps_pub = snapshot.get("injected_dependencies_public", {})
    deps_ext = snapshot.get("injected_dependencies_extended", {})
    out = []
    seen = set()
    for key in ("public_jutsu", "hidden_jutsu"):
        for j in kit.get(key, []):
            for e in j.get("effects", []):
                if e.get("type") != "injectjutsus":
                    continue
                for jid in e.get("jutsuIds", []):
                    dep = deps_pub.get(jid) or deps_ext.get(jid)
                    rec = dep.get("data", dep) if dep else None
                    out.append({
                        "parent_jutsu": j["name"],
                        "parent_jutsu_id": j["id"],
                        "inject_rounds": e.get("rounds"),
                        "inject_power": e.get("power"),
                        "child_id": jid,
                        "child_name": rec.get("name") if rec else None,
                        "child_bloodline_id": rec.get("bloodlineId") if rec else None,
                        "child_type": rec.get("jutsuType") if rec else None,
                        "child_resolved": rec is not None,
                        "child_effects": [
                            {"type": ce.get("type"), "power": ce.get("power"),
                             "powerPerLevel": ce.get("powerPerLevel"),
                             "elements": ce.get("elements"), "target": ce.get("target"),
                             "supported": ce.get("type") in SUPPORTED_TAGS}
                            for ce in (rec.get("effects", []) if rec else [])
                        ],
                        "duplicate": jid in seen,
                    })
                    seen.add(jid)
    return out


# ---------------------------------------------------------------------------
# Classification audit
# ---------------------------------------------------------------------------

def signature_elements(rows: list[Row]) -> list[str]:
    els: set[str] = set()
    for r in rows:
        if r.tag in ("damage", "pierce"):
            for x in r.elements:
                if x != "None":
                    els.add(x)
    return sorted(els)


def census_element_users(snapshot: dict, roster: dict) -> dict[str, list[dict]]:
    """element -> list of {bloodline_id, name, disposition, rows}"""
    recs = {r["bloodline_id"]: r for r in roster["records"]}
    users: dict[str, dict[str, dict]] = {}
    for kit in snapshot["kits"]:
        b = kit["bloodline"]
        rec = recs.get(b["id"], {})
        disp = rec.get("owner_decision", "UNLISTED")
        for key in ("public_jutsu", "hidden_jutsu"):
            for j in kit.get(key, []):
                for e in j.get("effects", []):
                    for x in (e.get("elements") or []):
                        d = users.setdefault(x, {})
                        ent = d.setdefault(b["id"], {"bloodline_id": b["id"], "name": b["name"],
                                                     "disposition": disp, "rows": 0, "damage_rows": 0})
                        ent["rows"] += 1
                        if e.get("type") in ("damage", "pierce"):
                            ent["damage_rows"] += 1
    return {k: sorted(v.values(), key=lambda z: z["name"]) for k, v in users.items()}


def classification_audit(kit: dict, rows: list[Row], snapshot: dict, roster: dict) -> dict:
    b = kit["bloodline"]
    bname = b["name"].strip()
    sig = signature_elements(rows)
    sup = [r for r in rows if r.supported]
    users = census_element_users(snapshot, roster)
    if len(sig) == 1 and sig[0] in BASIC_ELEMENTS:
        label = bname
        kind = "bloodline-keyed extension"
        note = (f"Single signature element {sig[0]} is a basic element carried on rows of many "
                "bloodlines and ordinary jutsu; using it as the classification label would leak "
                "broadly. A bloodline-keyed classification label is required; the element is kept "
                "as the display element only.")
    elif len(sig) == 1:
        label = sig[0]
        kind = "element"
        note = ("Single signature element on the kit's damage/pierce rows; usable as the "
                "classification label under the proposed whole-kit classification, provided the "
                "classification is bloodline-scoped (see census collisions) rather than a bare "
                "element match.")
    elif len(sig) == 0:
        label = bname
        kind = "bloodline-keyed extension"
        note = ("No non-None element on any damage/pierce row. No existing element can "
                "isolate this kit; a bloodline-keyed classification label (extension of the "
                "proposed resolver change) is required. Targeting 'None' would reach every "
                "non-elemental row in the game.")
    else:
        label = bname
        kind = "bloodline-keyed extension"
        note = ("Multiple signature elements (" + ", ".join(sig) + ") on damage/pierce rows; "
                "no single element isolates the kit. A bloodline-keyed classification label is "
                "required unless the user accepts one element as the classification key and "
                "documents the uncovered rows.")

    def reach(lbl: str) -> dict:
        direct = [r for r in sup if lbl in r.elements_effective]
        none_fallback = [r for r in sup if r.elements_effective == ["None"]]
        other = [r for r in sup if lbl not in r.elements_effective and r.elements_effective != ["None"]]
        return {
            "label": lbl,
            "rows_matching_label_directly": len(direct),
            "rows_falling_back_to_None": len(none_fallback),
            "rows_with_other_elements_only": len(other),
            "supported_rows_total": len(sup),
            "exclusive_under_current_resolver": False,
            "note": ("Current resolver matches each effect row's own elements (absent list -> "
                     "['None']). Rows without the label are unreachable with affectedElements=[label]; "
                     "reaching them needs affectedElements including 'None', which also reaches every "
                     "non-elemental row on any jutsu the player can cast."),
        }

    collisions = []
    for el in (sig if sig else []):
        for u in users.get(el, []):
            if u["bloodline_id"] != b["id"]:
                collisions.append({"element": el, **u})
    none_users = len(users.get("None", []))
    exclusive = (len(sig) == 1 and not collisions and sig[0] not in BASIC_ELEMENTS)
    return {
        "signature_elements": sig,
        "display_element": sig[0] if len(sig) == 1 else None,
        "proposed_label": label,
        "label_kind": kind,
        "element_exclusive_within_census": exclusive,
        "note": note,
        "current_resolver_reach": [reach(x) for x in (sig or ["None"])],
        "census_collisions_on_signature_elements": collisions,
        "census_bloodlines_with_None_rows": none_users,
        "normal_jutsu_collision": (
            "UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows "
            "(harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI "
            "jutsu only). Whether NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu carry this element needs a "
            "read-only public jutsu listing capture requested from dauntless."),
        "injected_children": injected_children(kit, snapshot),
        "item_gated_jutsu": sorted({r.jutsu_name for r in rows if r.item_gate}),
        "mode_restricted_jutsu": sorted({f"{r.jutsu_name} ({r.usage})" for r in rows if r.usage not in (None, "BOTH")}),
        "hidden_jutsu": sorted({r.jutsu_name for r in rows if r.visibility == "hidden"}),
        "non_bloodline_type_jutsu_in_kit": sorted({f"{r.jutsu_name} ({r.jutsu_type})" for r in rows if r.jutsu_type != "BLOODLINE"}),
        "engine_status": "proposal_requires_resolver_adjustment",
    }


# ---------------------------------------------------------------------------
# Tree graph validation and enumeration
# ---------------------------------------------------------------------------

@dataclass
class Node:
    id: str
    name: str
    category: str
    cost: int
    parents: list[str]
    modifiers: list[dict]
    raw: dict = field(default_factory=dict)


def parse_nodes(tree: dict) -> list[Node]:
    nodes = []
    for n in tree.get("nodes", []):
        nodes.append(Node(
            id=str(n["id"]), name=n["name"], category=n["category"], cost=int(n.get("cost", 1)),
            parents=[str(p) for p in (n.get("parents") or [])],
            modifiers=list(n.get("modifiers") or []), raw=n,
        ))
    return nodes


def closure(node_id: str, by_id: dict[str, Node]) -> set[str]:
    out: set[str] = set()
    stack = [node_id]
    while stack:
        cur = stack.pop()
        if cur in out:
            continue
        out.add(cur)
        for p in by_id[cur].parents:
            stack.append(p)
    return out


def depth(node_id: str, by_id: dict[str, Node]) -> int:
    return len(closure(node_id, by_id))


def is_closed(subset: set[str], by_id: dict[str, Node]) -> bool:
    for nid in subset:
        for p in by_id[nid].parents:
            if p not in subset:
                return False
    return True


def bonuses_for(subset: set[str], by_id: dict[str, Node]) -> dict[str, int]:
    tot = {t: 0 for t in SUPPORTED_TAGS}
    for nid in subset:
        for m in by_id[nid].modifiers:
            tot[m["tag"]] = tot.get(m["tag"], 0) + int(m["flat"])
    return tot


def enumerate_legal(by_id: dict[str, Node], cap: int = BP_CAP) -> dict[int, list[list[str]]]:
    ids = sorted(by_id)
    out: dict[int, list[list[str]]] = {k: [] for k in range(cap + 1)}
    for k in range(cap + 1):
        for combo in itertools.combinations(ids, k):
            s = set(combo)
            if sum(by_id[i].cost for i in combo) <= cap and is_closed(s, by_id):
                out[k].append(list(combo))
    return out


def dominates(a: dict[str, int], b: dict[str, int]) -> bool:
    ge = all(a.get(t, 0) >= b.get(t, 0) for t in SUPPORTED_TAGS)
    gt = any(a.get(t, 0) > b.get(t, 0) for t in SUPPORTED_TAGS)
    return ge and gt


def validate_structure(tree: dict) -> list[str]:
    """Return a list of structural errors (empty = valid)."""
    errors: list[str] = []
    nodes = parse_nodes(tree)
    by_id = {n.id: n for n in nodes}
    if len(nodes) == 0:
        return ["tree has no nodes"]
    if len(nodes) > MAX_NODES:
        errors.append(f"{len(nodes)} nodes exceeds the {MAX_NODES}-node ceiling")
    if len(by_id) != len(nodes):
        errors.append("duplicate node ids")
    names = [n.name.strip() for n in nodes]
    if len(set(n.lower() for n in names)) != len(names):
        errors.append("duplicate node names within tree")
    for n in nodes:
        if n.cost != NODE_COST:
            errors.append(f"node {n.id} cost {n.cost} != {NODE_COST}")
        if n.category not in TIERS:
            errors.append(f"node {n.id} category {n.category!r} not in {TIERS}")
        if len(n.parents) > 1:
            errors.append(f"node {n.id} has {len(n.parents)} parents; forks only (max 1)")
        for p in n.parents:
            if p not in by_id:
                errors.append(f"node {n.id} parent {p} missing")
            elif p == n.id:
                errors.append(f"node {n.id} is its own parent")
        if n.category == "Foundation" and n.parents:
            errors.append(f"Foundation {n.id} must not have a prerequisite")
        if n.category != "Foundation" and not n.parents:
            errors.append(f"{n.category} {n.id} must have exactly one prerequisite")
        if not n.modifiers:
            errors.append(f"node {n.id} has no modifiers")
        for m in n.modifiers:
            if m.get("tag") not in SUPPORTED_TAGS:
                errors.append(f"node {n.id} modifier tag {m.get('tag')!r} is not a supported potency tag")
            try:
                flat = int(m.get("flat"))
                if flat <= 0 or flat > 15:
                    errors.append(f"node {n.id} modifier {m.get('tag')} flat {flat} outside 1..15")
                if m.get("flat") != flat:
                    errors.append(f"node {n.id} modifier {m.get('tag')} flat must be an integer")
            except Exception:
                errors.append(f"node {n.id} modifier {m.get('tag')} flat is not an integer")
        if re.search(r"\d", n.name):
            errors.append(f"node {n.id} name {n.name!r} contains a digit; card titles carry no skill numbers")
        if any(w in n.name.lower().split() for w in JOKE_WORDS):
            errors.append(f"node {n.id} name {n.name!r} contains a joke word")
        if len(n.name) > 34:
            errors.append(f"node {n.id} name {n.name!r} longer than 34 characters")
    if errors:
        return errors
    # cycle check via closure sizes
    for n in nodes:
        seen: set[str] = set()
        cur = n
        while cur.parents:
            p = cur.parents[0]
            if p in seen or p == n.id:
                errors.append(f"cycle through node {n.id}")
                break
            seen.add(p)
            cur = by_id[p]
    if errors:
        return errors
    # tier ordering
    for n in nodes:
        if n.parents:
            par = by_id[n.parents[0]]
            if n.category == "Hidden Art" and par.category not in ("Foundation", "Hidden Art"):
                errors.append(f"Hidden Art {n.id} requires {par.id} ({par.category}); must follow a Foundation or Hidden Art")
            if n.category == "Advanced Art" and par.category != "Hidden Art":
                errors.append(f"Advanced Art {n.id} requires {par.id} ({par.category}); must follow a Hidden Art")
            if par.category == "Advanced Art":
                errors.append(f"node {n.id} requires Advanced Art {par.id}; Advanced Arts are route leaves")
    # reachability within budget
    for n in nodes:
        if depth(n.id, by_id) > BP_CAP:
            errors.append(f"node {n.id} needs {depth(n.id, by_id)} BP to reach; cap is {BP_CAP}")
    # Advanced Art affordability proof
    adv = [n for n in nodes if n.category == "Advanced Art"]
    for a in adv:
        if depth(a.id, by_id) < 3:
            errors.append(f"Advanced Art {a.id} reachable in {depth(a.id, by_id)} BP; must cost at least 3 including prerequisites")
    for a, b in itertools.combinations(adv, 2):
        cost = len(closure(a.id, by_id) | closure(b.id, by_id))
        if cost <= BP_CAP:
            errors.append(f"Advanced Arts {a.id} and {b.id} are jointly affordable for {cost} BP (cap {BP_CAP})")
    return errors


def audit_tree(tree: dict, rows: list[Row]) -> dict:
    """Full audit: assumes validate_structure returned no errors."""
    nodes = parse_nodes(tree)
    by_id = {n.id: n for n in nodes}
    sup_rows = [r for r in rows if r.supported]
    legal = enumerate_legal(by_id)
    full = legal[BP_CAP]
    full_bonus = [(ids, bonuses_for(set(ids), by_id)) for ids in full]
    non_dom = []
    for ids, bon in full_bonus:
        if not any(dominates(ob, bon) for oids, ob in full_bonus if oids != ids):
            non_dom.append(ids)
    nodes_in_non_dom = set(itertools.chain.from_iterable(non_dom))
    unused = sorted(set(by_id) - nodes_in_non_dom)
    adv = [n for n in nodes if n.category == "Advanced Art"]
    pair_costs = [len(closure(a.id, by_id) | closure(b.id, by_id)) for a, b in itertools.combinations(adv, 2)]
    max_adv = 0
    for k, lst in legal.items():
        for ids in lst:
            max_adv = max(max_adv, sum(1 for i in ids if by_id[i].category == "Advanced Art"))
    max_tag = {t: 0 for t in SUPPORTED_TAGS}
    for ids, bon in full_bonus:
        for t in SUPPORTED_TAGS:
            max_tag[t] = max(max_tag[t], bon.get(t, 0))
    rows_by_tag: dict[str, list[Row]] = {}
    for r in sup_rows:
        rows_by_tag.setdefault(r.tag, []).append(r)

    def node_value(n: Node) -> dict:
        raw = sum(int(m["flat"]) for m in n.modifiers)
        weighted = sum(int(m["flat"]) * len(rows_by_tag.get(m["tag"], [])) for m in n.modifiers)
        adverse = []
        for m in n.modifiers:
            for r in rows_by_tag.get(m["tag"], []):
                if r.adverse:
                    adverse.append({"jutsu": r.jutsu_name, "row": r.row, "tag": r.tag, "role": r.role})
        covered_jutsu = sorted({r.jutsu_name for m in n.modifiers for r in rows_by_tag.get(m["tag"], [])})
        covered_rows = sum(len(rows_by_tag.get(m["tag"], [])) for m in n.modifiers)
        return {"id": n.id, "name": n.name, "category": n.category, "depth": depth(n.id, by_id),
                "raw_flat_total": raw, "row_weighted_total": weighted,
                "covered_jutsu": covered_jutsu, "covered_rows": covered_rows,
                "adverse_rows_amplified": adverse,
                "tags_without_rows": [m["tag"] for m in n.modifiers if not rows_by_tag.get(m["tag"])]}

    node_values = [node_value(n) for n in nodes]
    builds = []
    for ids, bon in full_bonus:
        raw = sum(bon.values())
        weighted = sum(bon[t] * len(rows_by_tag.get(t, [])) for t in SUPPORTED_TAGS)
        builds.append({"ids": list(ids), "bonuses": {t: bon[t] for t in SUPPORTED_TAGS if bon[t]},
                       "raw_flat_total": raw, "row_weighted_total": weighted,
                       "advanced_arts": [i for i in ids if by_id[i].category == "Advanced Art"],
                       "non_dominated": ids in non_dom})
    strongest = max(builds, key=lambda b: (b["row_weighted_total"], b["raw_flat_total"])) if builds else None
    weakest_node = min(node_values, key=lambda v: v["row_weighted_total"]) if node_values else None
    return {
        "available_skills": len(nodes),
        "foundation_count": sum(1 for n in nodes if n.category == "Foundation"),
        "hidden_art_count": sum(1 for n in nodes if n.category == "Hidden Art"),
        "advanced_art_count": len(adv),
        "bloodright_point_cap": BP_CAP,
        "cost_per_skill": NODE_COST,
        "maximum_advanced_arts": max_adv,
        "minimum_two_advanced_cost": min(pair_costs) if pair_costs else None,
        "maximum_parents_per_node": max((len(n.parents) for n in nodes), default=0),
        "maximum_depth": max(depth(n.id, by_id) for n in nodes),
        "legal_allocations_by_size": {str(k): len(v) for k, v in legal.items()},
        "full_budget_allocations": len(full),
        "non_dominated_full_allocations": len(non_dom),
        "all_nodes_in_non_dominated_builds": len(unused) == 0,
        "nodes_absent_from_non_dominated_builds": unused,
        "maximum_tag_bonuses": {t: v for t, v in max_tag.items() if v},
        "supported_rows_in_kit": len(sup_rows),
        "supported_rows_by_tag": {t: len(v) for t, v in sorted(rows_by_tag.items())},
        "tags_targeted_by_tree": sorted({m["tag"] for n in nodes for m in n.modifiers}),
        "supported_tags_in_kit_not_targeted": sorted(set(rows_by_tag) - {m["tag"] for n in nodes for m in n.modifiers}),
        "node_values": node_values,
        "strongest_full_build_by_row_weight": strongest,
        "lowest_value_node_by_row_weight": weakest_node,
        "full_builds": builds,
        "legal_allocations": {str(k): v for k, v in legal.items()},
    }


def finals_for(ids: list[str], tree: dict, rows: list[Row]) -> list[dict]:
    nodes = parse_nodes(tree)
    by_id = {n.id: n for n in nodes}
    bon = bonuses_for(set(ids), by_id)
    out = []
    for r in rows:
        gain = bon.get(r.tag, 0) if r.supported else 0
        final = r.base + gain
        if r.calculation == "percentage":
            final = min(100.0, final)
        out.append({
            "jutsu": r.jutsu_name, "row": r.row, "tag": r.tag, "label": r.label,
            "combat_elements": r.elements_effective, "recipient": r.recipient, "role": r.role,
            "adverse": r.adverse, "base": round(r.base, 2), "gain": gain, "final": round(final, 2),
            "calculation": r.calculation, "supported": r.supported,
            "capped_at_100": bool(r.calculation == "percentage" and r.base + gain > 100),
        })
    return out
