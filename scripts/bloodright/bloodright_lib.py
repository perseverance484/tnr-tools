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
TREES_DIR = os.path.join(DESIGN_DIR, "trees")
# Generated projection of the approved Taiyo Kami reference values (the original handoff
# files under examples/ are historical evidence). It is not one of the approved 43.
REFERENCE_TREE = os.path.join(TREES_DIR, "taiyo_kami.json")
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

# Balance ceilings for the 4-BP model (RUL-2026-10-03-005), evaluated over every legal
# prerequisite-closed allocation. Hard ceilings can never be exceeded; any other supported
# tag above DEFAULT_CEILING needs a recorded reason and a director-review exception.
HARD_CEILINGS = {"damage": 5, "lifesteal": 5, "afterburn": 15}
DEFAULT_CEILING = 10
ROUTE_BANDS = (5, 10, 15)

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

# Selectors the classification model must never use (RUL-2026-10-03-005).
NOT_SELECTORS = (
    "bloodline id or bloodline ownership",
    "equipment / required bloodline item (castability gate only)",
    "injected-child provenance",
    "jutsu names (examples only)",
)


def short_kind(kind: str | None) -> str:
    return {"element": "element", "multi-element": "multi", "classification extension": "ext"}.get(kind or "", kind or "")


# Wording that encodes the superseded bloodline-scoped model or old display units
# (RUL-2026-10-03-005/006). Authored tree prose must not use it.
STALE_PHRASES = (
    "bloodline-scoped", "bloodline scoped", "bloodline-keyed", "census collision", "whole-kit classification",
    "damage power", "heal power", "planning guardrail", "tithe of the red eye",
)
PROSE_FIELDS = ("title", "flavor", "coverage_note", "rationale", "primary", "secondary", "tertiary",
                "narrow_kit_exception", "design_notes", "risks", "name", "archetype")


def stale_language(tree: dict) -> list[str]:
    """Return 'field: phrase' for every stale phrase found in authored prose."""
    hits: list[str] = []

    def scan(where: str, val: Any) -> None:
        if isinstance(val, str):
            low = val.lower()
            for ph in STALE_PHRASES:
                if ph in low:
                    hits.append(f"{where}: {ph!r}")
        elif isinstance(val, list):
            for i, v in enumerate(val):
                scan(f"{where}[{i}]", v)
        elif isinstance(val, dict):
            for k, v in val.items():
                if k in PROSE_FIELDS or k in ("emphasis",):
                    scan(f"{where}.{k}", v)

    for k in ("title", "emphasis", "narrow_kit_exception", "design_notes", "risks"):
        if k in tree:
            scan(k, tree[k])
    for n in tree.get("nodes", []):
        scan(f"node {n.get('id')}", {k: n.get(k) for k in ("name", "flavor", "coverage_note") if k in n})
    for e in tree.get("examples", []):
        scan(f"example {e.get('name')}", {k: e.get(k) for k in ("name", "archetype", "rationale") if k in e})
    for k, v in (tree.get("route_band_rationale") or {}).items():
        scan(f"route_band_rationale.{k}", v)
    for e in tree.get("director_exceptions") or []:
        scan("director_exceptions", e.get("reason"))
    return hits


def ceiling_for(tag: str) -> int:
    return HARD_CEILINGS.get(tag, DEFAULT_CEILING)


def unit(tag: str) -> str:
    """Display unit: flat Damage is raw EP; every other modifier is shown with %."""
    return "" if tag == "damage" else "%"


def mod_text(tag: str, flat: int, abbr: bool = False) -> str:
    """'+2 Damage', '+3% Lifesteal' (or '+3% LS' with abbr)."""
    if tag == "damage":
        return f"+{flat} Damage"
    return f"+{flat}% {TAG_ABBR[tag] if abbr else TAG_LABELS[tag]}"


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
    enemy_hazard: bool = False

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
                # Friendly fire at the pin (process.ts 154-183): an absent friendlyFire is ALL.
                # OTHER_USER/OPPONENT area methods apply INHERIT rows directly to each living
                # non-caster user on the affected tiles (actions.ts 1029-1060; util.ts isValidMove
                # excludes the caster), so a harmful row with friendlyFire None/ALL also lands on
                # allies in the area, never on the caster. GROUND/EMPTY_GROUND INHERIT rows become
                # ground effects re-applied each round to whoever stands on the tiles, caster and
                # enemies included (process.ts 321-340); SELF-target rows on ground actions are
                # realized on the caster at cast time (actions.ts 980-1004).
                ground = j.get("target") in ("GROUND", "EMPTY_GROUND")
                area = str(j.get("method") or "").startswith("AOE_") or ground
                inherit = e.get("target", "INHERIT") in (None, "INHERIT")
                hazard = bool(area and inherit and tag in NEGATIVE_TAGS
                              and e.get("friendlyFire") in (None, "ALL") and eff == "enemy")
                enemy_hazard = bool(ground and inherit and tag in POSITIVE_TAGS
                                    and e.get("friendlyFire") in (None, "ALL"))
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
                    ally_hazard=hazard, enemy_hazard=enemy_hazard,
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


def jutsu_elements(jutsu: dict) -> list[str]:
    """A jutsu's own elements: the union of its effect-row elements, ['None'] when empty.

    Mirrors checkJutsuElements (app/src/libs/train.ts 189-198 at the pin), the source's only
    jutsu-level element derivation.
    """
    els: list[str] = []
    for e in jutsu.get("effects", []):
        for x in (e.get("elements") or []):
            if x not in els:
                els.append(x)
    return sorted(els) or ["None"]


def classification_audit(kit: dict, rows: list[Row], snapshot: dict, roster: dict) -> dict:
    """Element-wide potency classification (RUL-2026-10-03-005).

    The qualifying element is the kit's signature element (the non-None element on its
    damage/pierce rows). Potency then reaches every jutsu of that element that carries a
    matching supported tag, wherever it comes from; bloodline id, equipment, injected-child
    provenance and jutsu names are never selectors. Shared elements are expected.
    """
    b = kit["bloodline"]
    bname = b["name"].strip()
    sig = signature_elements(rows)
    sup = [r for r in rows if r.supported]
    users = census_element_users(snapshot, roster)
    if len(sig) == 1:
        qualifying = list(sig)
        label = sig[0]
        kind = "element"
        status = "element"
        note = (f"Single signature element {sig[0]} on the kit's damage/pierce rows. Potency reaches "
                f"matching supported tags on every {sig[0]} jutsu: this kit, other bloodlines' "
                f"{sig[0]} jutsu and any NORMAL/SPECIAL/EVENT/FORBIDDEN or injected {sig[0]} jutsu. "
                "Sharing the element with other bloodlines is expected, not a collision.")
    elif len(sig) > 1:
        qualifying = list(sig)
        label = " + ".join(sig)
        kind = "multi-element"
        status = "multi-element: director review"
        note = ("Several signature elements (" + ", ".join(sig) + ") on damage/pierce rows. The "
                "proposal lists every signature element as qualifying, which reaches every jutsu of "
                "any of them; choosing one element, all of them, or a classification extension is a "
                "director decision.")
    else:
        qualifying = []
        label = bname
        kind = "classification extension"
        status = "requires classification extension"
        note = ("No non-None element on any damage/pierce row, so no existing element identifies "
                "this kit. Requires a classification extension: a new jutsu classification "
                f"(placeholder name '{bname}') assigned to jutsu records. It is not a bloodline-id "
                "selector; which jutsu carry it is a director/engine decision. Targeting 'None' "
                "would reach every non-elemental row in the game.")

    members = []
    for vis, key in (("public", "public_jutsu"), ("hidden", "hidden_jutsu")):
        for j in kit.get(key, []):
            jel = jutsu_elements(j)
            derived = bool(qualifying) and any(x in jel for x in qualifying)
            members.append({
                "jutsu": j["name"], "jutsu_elements": jel,
                "membership": "derived" if derived else "authored",
                "supported_rows": sum(1 for e in j.get("effects", []) if e.get("type") in SUPPORTED_TAGS),
            })

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
            "note": ("Current resolver matches each effect row's own elements (absent list -> "
                     "['None']); it has no jutsu-level classification. Rows on a qualifying jutsu "
                     "that do not carry the element are unreachable today: ENGINE GAP, not a "
                     "design question."),
        }

    shared = []
    for el in qualifying:
        for u in users.get(el, []):
            if u["bloodline_id"] != b["id"]:
                shared.append({"element": el, **u})
    return {
        "signature_elements": sig,
        "qualifying_elements": qualifying,
        "display_element": sig[0] if len(sig) == 1 else None,
        "proposed_label": label,
        "label_kind": kind,
        "classification_status": status,
        "note": note,
        "not_selectors": list(NOT_SELECTORS),
        "kit_membership": members,
        "kit_jutsu_by_authored_classification": sorted(m["jutsu"] for m in members if m["membership"] == "authored"),
        "current_resolver_reach": [reach(x) for x in (qualifying or ["None"])],
        "shared_element_bloodlines": shared,
        "shared_element_note": (
            "Other captured bloodlines with jutsu of the qualifying element. Sharing is expected. "
            "Their bloodline jutsu are castable only by their own bloodline's owners "
            "(checkJutsuBloodline, app/src/libs/train.ts 185-188), so they do not widen what one "
            "owner can amplify; NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu of the element can."),
        "census_bloodlines_with_None_rows": len(users.get("None", [])),
        "off_kit_coverage": (
            "UNVERIFIED: the repository holds no non-bloodline jutsu catalog with effect rows "
            "(harvests/seed/40_INDEX_jutsu.json is an id/name index; inbox bundles carry AI jutsu "
            "only). NORMAL/SPECIAL/EVENT/FORBIDDEN jutsu of the qualifying element are in scope "
            "by rule; how many exist needs a read-only public jutsu listing capture."),
        "injected_children": injected_children(kit, snapshot),
        "item_gated_jutsu": sorted({r.jutsu_name for r in rows if r.item_gate}),
        "mode_restricted_jutsu": sorted({f"{r.jutsu_name} ({r.usage})" for r in rows if r.usage not in (None, "BOTH")}),
        "hidden_jutsu": sorted({r.jutsu_name for r in rows if r.visibility == "hidden"}),
        "non_bloodline_type_jutsu_in_kit": sorted({f"{r.jutsu_name} ({r.jutsu_type})" for r in rows if r.jutsu_type != "BLOODLINE"}),
        "engine_status": engine_status_for(kind),
    }


def engine_status_for(kind: str) -> str:
    if kind == "classification extension":
        return "proposal_requires_jutsu_classification_resolver_and_classification_extension"
    return "proposal_requires_jutsu_classification_resolver"


def scope_label(cls: dict) -> str:
    """'Shadow', 'Shadow and Storm', or 'Dai Kenja-classified'."""
    q = list(cls.get("qualifying_elements") or [])
    if q:
        return q[0] if len(q) == 1 else ", ".join(q[:-1]) + " and " + q[-1]
    return f'{cls.get("potency_classification")}-classified'


def scope_sentence(cls: dict) -> str:
    s = f"Bonuses apply to matching supported tags on all {scope_label(cls)} jutsu."
    if cls.get("label_kind") == "classification extension":
        s = s[:-1] + " (requires classification extension)."
    return s


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


def max_over_legal(by_id: dict[str, Node]) -> dict[str, int]:
    """Per-tag maximum over every legal prerequisite-closed allocation of any size."""
    mx = {t: 0 for t in SUPPORTED_TAGS}
    for lst in enumerate_legal(by_id).values():
        for ids in lst:
            for t, v in bonuses_for(set(ids), by_id).items():
                mx[t] = max(mx[t], v)
    return {t: v for t, v in mx.items() if v}


def route_totals(by_id: dict[str, Node]) -> list[dict]:
    """One route per Advanced Art: its primary tag is the Advanced Art's first modifier tag,
    summed over the Advanced Art's prerequisite path."""
    out = []
    for n in sorted(by_id.values(), key=lambda z: z.id):
        if n.category != "Advanced Art" or not n.modifiers:
            continue
        tag = n.modifiers[0]["tag"]
        path = sorted(closure(n.id, by_id), key=lambda i: depth(i, by_id))
        steps = [sum(int(m["flat"]) for m in by_id[i].modifiers if m["tag"] == tag) for i in path]
        out.append({"advanced_art": n.id, "name": n.name, "primary_tag": tag, "path": path,
                    "steps": steps, "total": sum(steps)})
    return out


def ceiling_findings(tree: dict) -> tuple[list[str], list[str], dict]:
    """Ceiling and band checks (RUL-2026-10-03-005) over all legal allocations.

    Returns (errors, warnings, report). Damage > 5, Lifesteal > 5% and Afterburn > 15% are
    invalid. Any other tag above +10% is invalid unless tree.director_exceptions records
    {tag, max, reason, status}; a recorded exception is reported as a warning until the
    director approves it. Route primary totals off the 5/10/15 bands warn unless
    tree.route_band_rationale[<advanced art id>] gives a reason.
    """
    errors: list[str] = []
    warnings: list[str] = []
    by_id = {n.id: n for n in parse_nodes(tree)}
    mx = max_over_legal(by_id)
    exc = {}
    for e in tree.get("director_exceptions") or []:
        exc[e.get("tag")] = e
    for tag, e in exc.items():
        if tag in HARD_CEILINGS:
            errors.append(f"director_exceptions cannot lift the hard {TAG_LABELS.get(tag, tag)} ceiling {mod_text(tag, HARD_CEILINGS[tag])}")
        elif tag not in SUPPORTED_TAGS:
            errors.append(f"director_exceptions names unsupported tag {tag!r}")
        elif mx.get(tag, 0) <= DEFAULT_CEILING:
            warnings.append(f"director exception for {TAG_LABELS[tag]} is unused: legal maximum {mod_text(tag, mx.get(tag, 0))} is within +{DEFAULT_CEILING}%")
    for tag, v in mx.items():
        cap = ceiling_for(tag)
        if v <= cap:
            continue
        if tag in HARD_CEILINGS:
            errors.append(f"maximum {TAG_LABELS[tag]} {mod_text(tag, v)} in a legal allocation exceeds the hard ceiling {mod_text(tag, cap)}")
            continue
        e = exc.get(tag)
        if not e or not str(e.get("reason") or "").strip() or int(e.get("max") or 0) < v:
            errors.append(f"maximum {TAG_LABELS[tag]} {mod_text(tag, v)} in a legal allocation exceeds +{cap}% without a recorded director-review exception")
        else:
            warnings.append(f"maximum {TAG_LABELS[tag]} {mod_text(tag, v)} exceeds +{cap}% under a director-review exception "
                            f"({e.get('status') or 'pending director review'}): {e['reason']}")
    rationale = tree.get("route_band_rationale") or {}
    routes = route_totals(by_id)
    for r in routes:
        why = str(rationale.get(r["advanced_art"]) or "").strip()
        r["on_band"] = r["total"] in ROUTE_BANDS
        if why:
            r["band_rationale"] = why
        if not r["on_band"] and not why:
            warnings.append(f"route {r['name']} primary total {mod_text(r['primary_tag'], r['total'])} is off the 5/10/15 bands "
                            "without a route_band_rationale")
        if r["primary_tag"] == "damage" and r["steps"][-2:] != [2, 3] and not why:
            warnings.append(f"Damage route {r['name']} uses {'/'.join(str(x) for x in r['steps'])} rather than the default Hidden +2 / Advanced +3")
    for k in rationale:
        if k not in by_id or by_id[k].category != "Advanced Art":
            errors.append(f"route_band_rationale key {k!r} is not an Advanced Art id")
    report = {
        "maximum_over_all_legal_allocations": mx,
        "ceilings": {t: ceiling_for(t) for t in mx},
        "hard_ceilings": dict(HARD_CEILINGS),
        "default_ceiling": DEFAULT_CEILING,
        "route_bands": list(ROUTE_BANDS),
        "routes": routes,
        "director_exceptions": list(tree.get("director_exceptions") or []),
    }
    return errors, warnings, report


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
    max_tag = max_over_legal(by_id)
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
        "maximum_tag_bonuses": {t: max_tag[t] for t in SUPPORTED_TAGS if max_tag.get(t)},
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
