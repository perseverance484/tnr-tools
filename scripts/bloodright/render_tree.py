#!/usr/bin/env python3
"""Render a normalized Bloodright tree JSON to a deterministic SVG and Markdown.

Usage:
  python3 scripts/bloodright/render_tree.py docs/design/bloodright/trees/<slug>.json [--check]

The SVG follows the Taiyo Kami presentation contract: shared role legend with
matching text colors, no role labels or skill numbers on cards, costs, tiers,
full effect names/values, scope line, unambiguous prerequisite arrows, build
table and final-value table. Layout is computed from the graph, so forks of
any shape up to depth 4 render without manual placement.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bloodright_lib as L  # noqa: E402

W = 2400
MARGIN = 80
CONTENT_W = W - 2 * MARGIN
BG = "#0a101a"
CARD = "#131f2c"
CARD_ADV = "#1c2027"
GREY = "#b8c4cc"
WHITE = "#f2f2ed"
DIVIDER = "#394858"
BRANCH_COLORS = ["#e5bb69", "#9ac1ca", "#b8d98d", "#d9a6e0"]
FONT = "DejaVu Sans, sans-serif"
CHAR_W = 0.56  # approximate average glyph width as a fraction of font size


def t(x, y, s, size, fill, weight=400, anchor="start"):
    return (f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}" '
            f'text-anchor="{anchor}">{escape(str(s))}</text>')


def wrap(text: str, max_chars: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for w in words:
        cand = (cur + " " + w).strip()
        if len(cand) > max_chars and cur:
            lines.append(cur)
            cur = w
        else:
            cur = cand
    if cur:
        lines.append(cur)
    return lines or [""]


def fmt_val(v: float, calc: str) -> str:
    if calc == "percentage":
        return f"{v:g}%"
    return f"{v:g}"


def mod_text(m: dict) -> str:
    tag = m["tag"]
    flat = m["flat"]
    label = L.TAG_LABELS[tag]
    if tag == "damage":
        return f"+{flat} Damage power"
    if tag == "heal":
        return f"+{flat} Heal power"
    return f"+{flat}% {label}"


ADVERSE_ROLES = ("SELF DEBUFF", "ENEMY BUFF")
ADVERSE_COLOR = L.ROLE_COLORS["SELF DEBUFF"]


def finals_index(tree: dict) -> dict[tuple[str, int], dict]:
    """Map (jutsu, row) to the first example's finals row, which carries role/recipient/adverse per row."""
    ex = tree.get("examples") or []
    if not ex:
        return {}
    return {(fr["jutsu"], int(fr["row"])): fr for fr in ex[0].get("finals", [])}


def adverse_lines(node: dict, labels: dict[str, str] | None = None, fidx: dict | None = None) -> list[tuple[str, str]]:
    """One (text, colour) card line per adverse (jutsu, role) pair the node amplifies.

    Recipients come from the validator's coverage.adverse_rows ("Jutsu#row") and the finals
    row's role, never from the modifier's display_role, so a tag whose enemy row and self row
    share a card is never printed as if every occurrence targeted the opponent.
    """
    labels = labels or {}
    fidx = fidx or {}
    fallback = next((r for m in node.get("modifiers", []) for r in m.get("row_roles", []) if r in ADVERSE_ROLES), "SELF DEBUFF")
    out: list[tuple[str, str]] = []
    seen: set[tuple[str, str]] = set()
    for key in node.get("coverage", {}).get("adverse_rows", []):
        jutsu, _, row = str(key).rpartition("#")
        fr = fidx.get((jutsu, int(row))) if row.isdigit() else None
        role = (fr or {}).get("role") or fallback
        lab = labels.get(jutsu) or short_jutsu(jutsu)
        if (lab, role) in seen:
            continue
        seen.add((lab, role))
        out.append((f"{lab}: {role.lower()} (adverse)", L.ROLE_COLORS.get(role, ADVERSE_COLOR)))
    return out


def scope_phrase(cls: dict, bl: dict) -> str:
    """'Scorch-classified Taiyo Kami jutsu', or the bloodline-keyed wording when the label is the bloodline name."""
    label = str(cls.get("potency_classification") or "").strip()
    name = str(bl.get("name") or "").strip()
    if label.lower() == name.lower():
        return f"{name} jutsu (bloodline-keyed classification, proposed extension)"
    return f"{label}-classified {name} jutsu"


def short_jutsu(name: str) -> str:
    # Last meaningful word(s) for compact coverage lines, mirroring "Nova · Reverb · Inferno".
    name = name.replace(":", "").replace("–", "").replace("—", "")
    parts = [p for p in name.split() if p.lower() not in ("the", "of", "a", "style", "release", "summoning", "mantle", "no")]
    if not parts:
        return name
    if len(parts) >= 3:
        return " ".join(parts[-2:])
    return parts[-1] if len(parts[-1]) > 2 else " ".join(parts[-2:])


def jutsu_labels(tree: dict) -> dict[str, str]:
    """Map every jutsu named by the tree to the label the SVG prints for it.

    Short labels (the last meaningful word, as in "Nova · Reverb · Inferno") are used
    only when every short label in the kit is unique and none equals the tree's potency
    classification or display element. Otherwise the whole kit is printed with full
    jutsu names, so "Reapers Storm" and "Death's Storm" never both collapse to "Storm"
    in a Storm-classified tree and a jutsu label is never mistaken for the element.
    """
    names: set[str] = set()
    for ex in tree.get("examples", []):
        for fr in ex.get("finals", []):
            names.add(fr["jutsu"])
    for n in tree.get("nodes", []):
        names.update(n.get("coverage", {}).get("jutsu", []))
    cls = tree.get("classification", {}) or {}
    reserved = {str(cls.get(k) or "").strip().lower() for k in ("potency_classification", "display_element")} - {"", "none"}
    shorts = {nm: short_jutsu(nm) for nm in sorted(names)}
    counts: dict[str, int] = {}
    for s in shorts.values():
        counts[s.lower()] = counts.get(s.lower(), 0) + 1
    unambiguous = all(counts[s.lower()] == 1 and s.lower() not in reserved for s in shorts.values())
    return shorts if unambiguous else {nm: nm for nm in shorts}


def coverage_line(node: dict, labels: dict[str, str] | None = None) -> str:
    cov = node.get("coverage", {})
    j = cov.get("jutsu", [])
    if not j:
        return "No matching rows"
    labels = labels or {}
    shorts = []
    seen = set()
    for name in j:
        s = labels.get(name) or short_jutsu(name)
        if s in seen:
            s = name
        seen.add(s)
        shorts.append(s)
    extra = ""
    if cov.get("effect_rows", 0) > len(j):
        extra = f" ({cov['effect_rows']} effects)"
    return " · ".join(shorts) + extra


def layout(tree: dict):
    nodes = tree["nodes"]
    by_id = {n["id"]: n for n in nodes}
    children: dict[str, list[str]] = {n["id"]: [] for n in nodes}
    roots = []
    for n in nodes:
        if n["parents"]:
            children[n["parents"][0]].append(n["id"])
        else:
            roots.append(n["id"])
    for k in children:
        children[k].sort()
    roots.sort()

    def leaves(nid):
        ch = children[nid]
        if not ch:
            return 1
        return sum(leaves(c) for c in ch)

    total_leaves = sum(leaves(r) for r in roots)
    gap = 60
    col_w = (CONTENT_W - gap * (total_leaves - 1)) / total_leaves
    pos: dict[str, dict] = {}
    cursor = [0]

    def place(nid, depth, branch):
        ch = children[nid]
        if not ch:
            c0 = cursor[0]
            cursor[0] += 1
            x = MARGIN + c0 * (col_w + gap)
            w = col_w
            pos[nid] = {"x": x, "w": w, "depth": depth, "branch": branch, "cols": (c0, c0)}
            return (c0, c0)
        first = None
        last = None
        for c in ch:
            a, b = place(c, depth + 1, branch)
            first = a if first is None else first
            last = b
        x = MARGIN + first * (col_w + gap)
        w = (last - first + 1) * col_w + (last - first) * gap
        pos[nid] = {"x": x, "w": w, "depth": depth, "branch": branch, "cols": (first, last)}
        return (first, last)

    for i, r in enumerate(roots):
        place(r, 1, i % len(BRANCH_COLORS))
    return pos, children, roots, by_id


def card_height(node: dict, w: float, labels: dict[str, str] | None = None, fidx: dict | None = None) -> int:
    mods = node.get("modifiers", [])
    max_chars = int((w - 50) / (26 * CHAR_W))
    cov_lines = wrap(coverage_line(node, labels), max_chars)
    h = 153 + 45 * max(0, len(mods) - 1) + 42 + 33 * (len(cov_lines) + len(adverse_lines(node, labels, fidx))) + 95
    return max(330, int((h + 9) // 10 * 10))


def render_svg(tree: dict) -> str:
    bl = tree["bloodline"]
    cls = tree["classification"]
    audit = tree["audit"]
    nodes = tree["nodes"]
    pos, children, roots, by_id = layout(tree)
    labels = jutsu_labels(tree)
    fidx = finals_index(tree)
    has_adverse = any(n.get("coverage", {}).get("adverse_rows") for n in nodes)
    depth_max = max(p["depth"] for p in pos.values())
    # layer heights
    layer_h = {}
    for d in range(1, depth_max + 1):
        hs = [card_height(by_id[nid], p["w"], labels, fidx) for nid, p in pos.items() if p["depth"] == d]
        layer_h[d] = max(hs) if hs else 330
    y0 = 450
    layer_y = {}
    y = y0
    for d in range(1, depth_max + 1):
        layer_y[d] = y
        y += layer_h[d] + 180
    tree_bottom = y - 180
    out = []
    # edges
    edges = []
    for nid, p in pos.items():
        n = by_id[nid]
        for c in children[nid]:
            cp = pos[c]
            px = p["x"] + p["w"] / 2
            py = layer_y[p["depth"]] + layer_h[p["depth"]]
            cx = cp["x"] + cp["w"] / 2
            cy = layer_y[cp["depth"]]
            color = BRANCH_COLORS[p["branch"]]
            marker = f"arrow-{p['branch']}"
            if abs(px - cx) < 1:
                d = f"M{px:g} {py:g} V{cy - 7:g}"
            else:
                d = f"M{px:g} {py:g} V{py + 78:g} H{cx:g} V{cy - 7:g}"
            edges.append(f'<path id="edge-{nid}-{c}" data-from="{nid}" data-to="{c}" d="{d}" fill="none" stroke="{color}" '
                         f'stroke-width="5" stroke-linejoin="round" marker-end="url(#{marker})"/>')
    cards = []
    for nid in sorted(pos, key=lambda k: (pos[k]["depth"], pos[k]["x"])):
        n = by_id[nid]
        p = pos[nid]
        x, w = p["x"], p["w"]
        yy = layer_y[p["depth"]]
        h = layer_h[p["depth"]]
        color = BRANCH_COLORS[p["branch"]]
        adv = n["category"] == "Advanced Art"
        fill = CARD_ADV if adv else CARD
        stroke_w = 4 if adv else 2
        stroke = "#e5bb69" if adv else color
        g = [f'<g id="node-{nid}" data-cost="{n["cost"]}" data-prerequisites="{",".join(n["parents"])}" data-potency-classification="{escape(str(n["potency_classification"]))}">']
        g.append(f'<rect x="{x:g}" y="{yy}" width="{w:g}" height="{h}" rx="14" fill="{fill}" stroke="{stroke}" stroke-width="{stroke_w}"/>')
        g.append(t(x + 25, yy + 43, n["category"].upper(), 26, color if not adv else "#e5bb69", 700))
        g.append(t(x + w - 25, yy + 43, f'{n["cost"]} BP', 28, WHITE, 700, "end"))
        name_size = 42 if n["category"] == "Foundation" and w > 700 else 35
        g.append(t(x + 25, yy + 99, n["name"], name_size, WHITE, 700))
        my = yy + 153
        for m in n.get("modifiers", []):
            role = m.get("display_role", "SELF BUFF")
            g.append(t(x + 25, my, mod_text(m), 31, L.ROLE_COLORS.get(role, GREY), 700))
            my += 45
        my += 2
        max_chars = int((w - 50) / (26 * CHAR_W))
        for line in wrap(coverage_line(n, labels), max_chars):
            g.append(t(x + 25, my + 28, line, 26, GREY))
            my += 33
        for line, colour in adverse_lines(n, labels, fidx):
            g.append(t(x + 25, my + 28, line, 26, colour, 700))
            my += 33
        if n["parents"]:
            g.append(f'<path d="M{x + 24:g} {yy + h - 77} L{x + w - 24:g} {yy + h - 77}" fill="none" stroke="{DIVIDER}" stroke-width="2"/>')
            g.append(t(x + 25, yy + h - 44, f'Requires {by_id[n["parents"][0]]["name"]}', 26, color))
            rem = L.BP_CAP - n["minimum_path_bp"]
            tail = f'{n["minimum_path_bp"]} BP path' + (f' · {rem} purchase{"s" if rem != 1 else ""} remain' if adv else "")
            g.append(t(x + 25, yy + h - 15, tail, 24, GREY))
        else:
            g.append(t(x + 25, yy + h - 37, "ENTRY · No prerequisite", 28, GREY))
        g.append("</g>")
        cards.append("\n".join(g))

    # header
    hdr = []
    hdr.append(f'<rect x="0" y="0" width="{W}" height="__H__" rx="0" fill="{BG}"/>')
    hdr.append(t(MARGIN, 95, f'BLOODRIGHT / {bl["name"].upper()}', 34, "#e5bb69", 700))
    title = tree.get("title", "")
    sub = title.split("—", 1)[1].strip() if "—" in title else title
    hdr.append(t(MARGIN, 175, sub or bl["name"], 72, WHITE, 700))
    hdr.append(t(MARGIN, 226, f'{tree.get("revision", "")} · Foundations support. Hidden Arts focus. Advanced Arts define.', 31, GREY))
    hdr.append(t(W - MARGIN, 105, f'{len(nodes)} SKILLS  /  {L.BP_CAP} PURCHASES', 36, "#e5bb69", 700, "end"))
    hdr.append(t(W - MARGIN, 156, "1 BP each · Acquire points with silver", 29, GREY, 400, "end"))
    hdr.append(t(W - MARGIN, 205, "Only your current bloodline unlocks", 28, GREY, 400, "end"))
    hdr.append(f'<rect x="{MARGIN}" y="282" width="{CONTENT_W}" height="112" rx="14" fill="{CARD}" stroke="{DIVIDER}" stroke-width="2"/>')
    kind = cls.get("label_kind", "")
    if kind == "element":
        band = f'{str(cls["potency_classification"]).upper()} POTENCY CLASSIFICATION'
    else:
        band = f'{str(cls["potency_classification"]).upper()} CLASSIFICATION · BLOODLINE-KEYED (PROPOSED EXTENSION)'
    hdr.append(t(MARGIN + 40, 328, band, 30, "#e5bb69", 700))
    hdr.append(t(MARGIN + 40, 370, f'Every {bl["name"]} jutsu: existing supported tags qualify; combat scope stays unchanged.', 29, GREY))
    if has_adverse:
        hdr.append(t(MARGIN, 426, "SELF BUFF · YOURSELF OR ALLIES", 25, L.ROLE_COLORS["SELF BUFF"], 700))
        hdr.append(t(MARGIN + 600, 426, "ENEMY DEBUFF · OPPONENT", 25, L.ROLE_COLORS["ENEMY DEBUFF"], 700))
        hdr.append(t(MARGIN + 1160, 426, "DAMAGE · OPPONENT", 25, L.ROLE_COLORS["DAMAGE"], 700))
        hdr.append(t(W - MARGIN, 426, "ADVERSE · ALSO WORKS AGAINST YOU", 25, ADVERSE_COLOR, 700, "end"))
    else:
        hdr.append(t(MARGIN, 426, "SELF BUFF · YOURSELF OR ALLIES", 25, L.ROLE_COLORS["SELF BUFF"], 700))
        hdr.append(t(MARGIN + 760, 426, "ENEMY DEBUFF · OPPONENT", 25, L.ROLE_COLORS["ENEMY DEBUFF"], 700))
        hdr.append(t(MARGIN + 1580, 426, "DAMAGE · OPPONENT", 25, L.ROLE_COLORS["DAMAGE"], 700))

    # path labels + rules
    body = []
    y = tree_bottom + 58
    examples = tree.get("examples", [])
    for nid, p in pos.items():
        n = by_id[nid]
        if n["category"] != "Advanced Art":
            continue
        label = None
        for ex in examples:
            if nid in ex.get("ids", []):
                label = (ex.get("archetype") or ex.get("name") or "").upper()
                break
        if label:
            body.append(t(p["x"] + p["w"] / 2, y, label, 28, "#e5bb69", 700, "middle"))
    y += 46
    if depth_max >= 4:
        body.append(t(W / 2, y, "Routes finish in three or four purchases. Spend any remainder on support or a sibling Hidden Art.", 30, WHITE, 400, "middle"))
    else:
        body.append(t(W / 2, y, "Finish a path in 3 purchases. Spend your fourth on support or a sibling Hidden Art.", 30, WHITE, 400, "middle"))
    y += 53
    adv_n = audit["advanced_art_count"]
    if adv_n >= 2:
        body.append(t(W / 2, y, f'Any two Advanced Arts require at least {audit["minimum_two_advanced_cost"]} points. Your limit is {L.BP_CAP}.', 34, "#e5bb69", 700, "middle"))
    elif adv_n == 1:
        body.append(t(W / 2, y, f'One Advanced Art exists; its route costs {max(n["minimum_path_bp"] for n in nodes if n["category"] == "Advanced Art")} of your {L.BP_CAP} points.', 34, "#e5bb69", 700, "middle"))
    else:
        body.append(t(W / 2, y, "This tree has no Advanced Art (narrow kit).", 34, "#e5bb69", 700, "middle"))
    y += 48
    body.append(t(W / 2, y, "Each skill purchased once · Only your current bloodline unlocks · No converging paths", 27, GREY, 400, "middle"))
    y += 99
    body.append(t(MARGIN, y, f'{["ZERO","ONE","TWO","THREE","FOUR"][min(len(examples),4)]} COMPLETE BUILD{"S" if len(examples)!=1 else ""}', 36, "#e5bb69", 700))
    y += 46
    body.append(t(MARGIN, y, "Examples are choices, not locked presets. Advanced Arts are optional.", 29, GREY))
    y += 24
    for i, ex in enumerate(examples):
        body.append(f'<rect x="{MARGIN}" y="{y}" width="{CONTENT_W}" height="59" rx="0" fill="{CARD if i % 2 == 0 else BG}"/>')
        body.append(t(MARGIN + 24, y + 35, ex.get("name", ""), 29, WHITE, 700))
        ids = ex["ids"]
        advs = [by_id[i]["name"] for i in ids if by_id[i]["category"] == "Advanced Art"]
        rest = [by_id[i]["name"] for i in ids if by_id[i]["category"] != "Advanced Art" and
                not any(i in L.closure(a, {k: L.Node(k, v["name"], v["category"], 1, v["parents"], v.get("modifiers", [])) for k, v in by_id.items()}) for a in ids if by_id[a]["category"] == "Advanced Art")]
        desc = (f'{advs[0]} path' if advs else "No Advanced Art") + (" + " + " + ".join(rest) if rest else "")
        body.append(t(MARGIN + 400, y + 35, desc, 29, "#e5bb69"))
        bon = ex.get("bonuses", {})
        top = sorted(bon.items(), key=lambda kv: -kv[1])[:3]
        bs = " / ".join((f'+{v} Damage' if k == "damage" else f'+{v} Heal' if k == "heal" else f'+{v}% {L.TAG_ABBR[k]}') for k, v in top)
        body.append(t(MARGIN + 1450, y + 35, bs, 28, GREY))
        y += 61
    y += 55
    tags_used = [tg for tg in L.SUPPORTED_TAGS if tg not in ("damage", "heal") and any(ex.get("bonuses", {}).get(tg) for ex in examples)]
    if not tags_used:
        tags_used = [tg for tg in L.SUPPORTED_TAGS if tg not in ("damage", "heal") and any(m["tag"] == tg for n in nodes for m in n.get("modifiers", []))]
    body.append(t(MARGIN, y, " · ".join(f'{L.TAG_ABBR[tg]}: {L.TAG_LABELS[tg]}' for tg in tags_used) or "Damage and Heal additions are raw power", 24, GREY))
    y += 48
    body.append(t(MARGIN, y, f'FINAL {bl["name"].upper()} TAG VALUES', 35, "#e5bb69", 700))
    y += 43
    body.append(t(MARGIN, y, f'Jutsu level {tree.get("evaluation_level", L.DEFAULT_JUTSU_LEVEL)} · main-tree bonuses and bloodline passives excluded', 27, GREY))
    y += 27
    # finals table: collapse identical rows (same jutsu, tag, base, calc) across examples
    finals_cols = examples
    rows_tbl = []
    if finals_cols:
        base_rows = finals_cols[0]["finals"]
        groups = {}
        order = []
        for i, fr in enumerate(base_rows):
            if not fr["supported"]:
                continue
            key = (fr["jutsu"], fr["tag"], fr["base"], fr["calculation"], bool(fr.get("adverse")))
            if key not in groups:
                groups[key] = []
                order.append(key)
            groups[key].append(i)
        for key in order:
            idxs = groups[key]
            jutsu, tag, base, calc, adverse = key
            lab = f'{labels.get(jutsu, jutsu)} · {L.TAG_LABELS[tag]}' + (f' (each of {len(idxs)} effects)' if len(idxs) > 1 else "")
            colour = None
            if adverse:
                fr0 = base_rows[idxs[0]]
                lab += f' · {fr0.get("recipient", "self")} (adverse)'
                colour = L.ROLE_COLORS.get(fr0.get("role", ""), ADVERSE_COLOR)
            vals = [fmt_val(base, calc)] + [fmt_val(ex["finals"][idxs[0]]["final"], calc) for ex in finals_cols]
            rows_tbl.append((lab, vals, colour))
    ncols = 1 + len(finals_cols)
    col_x0 = MARGIN + 1040
    step = (CONTENT_W - 1040) / max(1, ncols) if ncols > 1 else 250
    body.append(f'<rect x="{MARGIN}" y="{y}" width="{CONTENT_W}" height="60" rx="0" fill="#263240"/>')
    body.append(t(MARGIN + 14, y + 36, "EXISTING EFFECT", 24, WHITE, 700))
    heads = ["BASE"] + [(ex.get("archetype") or ex.get("name") or "").upper()[:16] for ex in finals_cols]
    head_size = 24 if ncols <= 3 else 21
    for i, hname in enumerate(heads):
        body.append(t(col_x0 + 34 + i * step, y + 36, hname, head_size, WHITE, 700))
    y += 65
    for i, (lab, vals, colour) in enumerate(rows_tbl):
        if i % 2 == 0:
            body.append(f'<rect x="{MARGIN}" y="{y}" width="{CONTENT_W}" height="48" rx="0" fill="{CARD}"/>')
        body.append(t(MARGIN + 14, y + 34, lab, 26, colour or GREY))
        for j, v in enumerate(vals):
            body.append(t(col_x0 + 40 + j * step, y + 34, v, 29, colour or "#e5bb69"))
        y += 49
    y += 42
    body.append(t(MARGIN, y, "Static bonuses: a 35% tag with +5% becomes 40%. A 40 EP jutsu with +5 Damage becomes 45EP.", 25, GREY))
    y += 41
    tree_tags = {m["tag"] for n in nodes for m in n.get("modifiers", [])}
    if "afterburn" in tree_tags:
        body.append(t(MARGIN, y, "Afterburn is an enemy debuff: while it lasts, damage the target takes adds Afterburn damage at the debuff percentage (60% cap per hit).", 24, GREY))
        y += 36
    if "heal" in tree_tags:
        body.append(t(MARGIN, y, "Heal additions are raw power: each +1 Heal power is +10 HP per tick of a static heal.", 24, GREY))
        y += 36
    if "lifesteal" in tree_tags or "reflect" in tree_tags:
        body.append(t(MARGIN, y, "Lifesteal shares a 60%-of-hit leech budget with vamp; Reflect returns at most 60% of a hit.", 24, GREY))
        y += 36
    body.append(t(MARGIN, y, "Proposed whole-kit potency classification. Current effect-element matching alone does not provide this inheritance.", 24, GREY))
    y += 36
    body.append(t(MARGIN, y, f'{audit["full_budget_allocations"]} legal four-skill allocations · {adv_n} Advanced Art{"s" if adv_n != 1 else ""} available · Combat tuning remains experimental', 24, "#e5bb69"))
    H = y + 40

    desc_forks = []
    for r in roots:
        chs = children[r]
        parts = []
        for c in chs:
            chain = [by_id[c]["name"]]
            cur = c
            while children[cur]:
                cur = children[cur][0]
                chain.append(by_id[cur]["name"])
            parts.append(" then ".join(chain))
        desc_forks.append(f'{by_id[r]["name"]} forks into ' + ", or ".join(parts) + "." if parts else f'{by_id[r]["name"]} stands alone.')
    desc = (f'{len(nodes)} skills, {L.BP_CAP} purchases, one Advanced Art maximum. ' + " ".join(desc_forks) +
            f' No paths converge. Bonuses affect existing supported tags on {scope_phrase(cls, bl)}.')
    meta = json.dumps(tree, ensure_ascii=True, separators=(",", ":"))
    defs = "".join(
        f'<marker id="arrow-{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10Z" fill="{c}"/></marker>'
        for i, c in enumerate(BRANCH_COLORS))
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',
           f'<title id="title">{escape(tree.get("title", bl["name"]))}. {escape(str(tree.get("revision", "")))}.</title>',
           f'<desc id="desc">{escape(desc)}</desc>',
           f'<metadata id="design-data">{escape(meta)}</metadata>',
           f'<defs>{defs}</defs>',
           f'<g font-family="{FONT}">']
    svg.extend(h.replace("__H__", str(H)) for h in hdr)
    svg.extend(edges)
    svg.extend(cards)
    svg.extend(body)
    svg.append("</g></svg>")
    return "\n".join(svg) + "\n"


def render_md(tree: dict, validation: dict | None) -> str:
    bl = tree["bloodline"]
    cls = tree["classification"]
    audit = tree["audit"]
    nodes = tree["nodes"]
    by_id = {n["id"]: n for n in nodes}
    out = [f'# {tree.get("title", bl["name"])}\n']
    out.append(f'**Bloodline:** {bl["name"]} ({bl.get("review_id")}, rank {bl.get("rank")}, `{bl["id"]}`) · **Revision:** {tree.get("revision")} · '
               f'**Classification:** {cls["potency_classification"]} ({cls.get("label_kind")}) · **Engine status:** {cls.get("engine_status")}\n')
    em = tree.get("emphasis") or {}
    if em:
        out.append(f'**Emphasis:** primary {em.get("primary")} · secondary {em.get("secondary")} · tertiary {em.get("tertiary")}.')
        if em.get("rationale"):
            out.append(f'\n{em["rationale"]}\n')
    if tree.get("narrow_kit_exception"):
        out.append(f'> **Narrow-kit exception:** {tree["narrow_kit_exception"]}\n')
    out.append(f'All nodes cost 1 BP; the budget is {L.BP_CAP} BP acquired with silver; each skill is bought once; forks only. '
               f'Bonuses are static additions to existing supported tags of {scope_phrase(cls, bl)} under the proposed classification behavior; no row\'s combat scope changes. Baselines at jutsu level {tree.get("evaluation_level")}.\n')
    out.append("## Skills\n")
    out.append("| ID | Skill | Tier | Requires | Exact bonus and recipient | Coverage (jutsu / rows) |\n|---|---|---|---|---|---|")
    for n in nodes:
        req = by_id[n["parents"][0]]["name"] if n["parents"] else "None"
        bonus = "; ".join(f'{mod_text(m)} ({m.get("display_role", "").lower()})' for m in n["modifiers"])
        cov = n.get("coverage", {})
        cv = f'{", ".join(cov.get("jutsu", []))} / {cov.get("effect_rows", 0)}'
        if cov.get("adverse_rows"):
            cv += f' · **adverse:** {", ".join(cov["adverse_rows"])}'
        out.append(f'| {n["id"]} | {n["name"]} | {n["category"]} | {req} | {bonus} | {cv} |')
    edges = [f'{n["parents"][0]}→{n["id"]}' for n in nodes if n["parents"]]
    out.append(f'\nConnections: {", ".join(edges)}. Advanced Arts: {audit["advanced_art_count"]}; any two cost at least {audit["minimum_two_advanced_cost"]} BP including prerequisites (cap {L.BP_CAP}); maximum affordable Advanced Arts: {audit["maximum_advanced_arts"]}.\n')
    for n in nodes:
        if n.get("flavor") or n.get("coverage_note"):
            out.append(f'- **{n["name"]}** — {n.get("flavor", "")} {n.get("coverage_note", "")}'.rstrip())
    out.append("\n## Complete four-purchase examples\n")
    tags_present = [t for t in L.SUPPORTED_TAGS if any(e.get("bonuses", {}).get(t) for e in tree.get("examples", []))]
    out.append("| Build | Purchases | " + " | ".join(L.TAG_ABBR[t] for t in tags_present) + " |")
    out.append("|---|---|" + "|".join("---:" for _ in tags_present) + "|")
    for ex in tree.get("examples", []):
        names = ", ".join(by_id[i]["name"] for i in ex["ids"])
        vals = " | ".join((f'+{ex["bonuses"].get(t, 0)}' + ("" if t in ("damage", "heal") else "%")) if ex["bonuses"].get(t) else "—" for t in tags_present)
        out.append(f'| {ex.get("name")} ({ex.get("archetype")}) | {names} | {vals} |')
    out.append("\nAbbreviations: " + " · ".join(f'{L.TAG_ABBR[t]} = {L.TAG_LABELS[t]}' for t in tags_present) + ". Values are per-matching-row static additions, not final combat percentages.\n")
    for ex in tree.get("examples", []):
        if ex.get("rationale"):
            out.append(f'- **{ex.get("name")}:** {ex["rationale"]}')
    out.append("\n## Before/after effect rows\n")
    exs = tree.get("examples", [])
    out.append("| Jutsu | Row | Tag | Recipient | Base | " + " | ".join(str(e.get("archetype") or e.get("name")) for e in exs) + " |")
    out.append("|---|---:|---|---|---:|" + "|".join("---:" for _ in exs) + "|")
    if exs:
        for i, fr in enumerate(exs[0]["finals"]):
            vals = " | ".join(fmt_val(e["finals"][i]["final"], fr["calculation"]) + ("" if e["finals"][i]["gain"] == 0 else f' (+{e["finals"][i]["gain"]})') for e in exs)
            note = "" if fr["supported"] else " (unsupported)"
            adv = " **adverse**" if fr.get("adverse") else ""
            out.append(f'| {fr["jutsu"]} | {fr["row"]} | {fr["label"]}{note}{adv} | {fr["recipient"]} | {fmt_val(fr["base"], fr["calculation"])} | {vals} |')
    out.append("\n## Allocation audit\n")
    la = audit["legal_allocations_by_size"]
    out.append(f'- Legal prerequisite-closed allocations by size: ' + ", ".join(f'{k}: {v}' for k, v in la.items()))
    out.append(f'- Full-budget allocations: {audit["full_budget_allocations"]}; numerically non-dominated (per-tag totals): {audit["non_dominated_full_allocations"]}; all nodes appear in a non-dominated build: {audit["all_nodes_in_non_dominated_builds"]}')
    out.append(f'- Maximum individually achievable additions: ' + ", ".join(f'{L.TAG_LABELS[k]} +{v}{"" if k in ("damage","heal") else "%"}' for k, v in audit["maximum_tag_bonuses"].items()) + " (not jointly attainable)")
    out.append(f'- Supported rows in kit: {audit["supported_rows_in_kit"]} (' + ", ".join(f'{L.TAG_ABBR[k]} {v}' for k, v in audit["supported_rows_by_tag"].items()) + ")")
    if audit.get("supported_tags_in_kit_not_targeted"):
        out.append(f'- Supported tags present but not targeted: {", ".join(audit["supported_tags_in_kit_not_targeted"])}')
    if validation:
        a = validation["audit"]
        s = a.get("strongest_full_build_by_row_weight")
        if s:
            out.append(f'- Strongest full build by row-weighted total: {", ".join(by_id[i]["name"] for i in s["ids"])} (raw +{s["raw_flat_total"]}, row-weighted {s["row_weighted_total"]})')
        wk = a.get("lowest_value_node_by_row_weight")
        if wk:
            out.append(f'- Lowest row-weighted node: {wk["name"]} ({wk["row_weighted_total"]})')
        if validation.get("warnings"):
            out.append("\nValidator warnings:\n")
            for w in validation["warnings"]:
                out.append(f'- {w}')
    out.append("\n### All legal full-budget allocations\n")
    out.append("| # | Nodes | Bonuses |\n|---:|---|---|")
    for i, b in enumerate(tree.get("legal_full_budget_builds", []), 1):
        bon = ", ".join(f'{L.TAG_ABBR[k]} +{v}' for k, v in b["bonuses"].items() if v)
        out.append(f'| {i} | {", ".join(by_id[x]["name"] for x in b["ids"])} | {bon} |')
    if tree.get("design_notes"):
        out.append("\n## Design notes\n")
        for d in tree["design_notes"]:
            out.append(f'- {d}')
    if tree.get("risks"):
        out.append("\n## Risks and unproven interactions\n")
        for r in tree["risks"]:
            out.append(f'- {r}')
    out.append("\n## Limits\n")
    for lim in audit.get("limits", []):
        out.append(f'- {lim}')
    out.append("")
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    rc = 0
    for p in args.paths:
        if p.endswith(".validation.json"):
            continue
        tree = L.load_json(p)
        if "audit" not in tree:
            print(f"{p}: not normalized (run validate_tree.py --write first)")
            rc = 1
            continue
        base = p[:-5]
        vpath = base + ".validation.json"
        validation = L.load_json(vpath) if os.path.exists(vpath) else None
        svg = render_svg(tree)
        md = render_md(tree, validation)
        if args.check:
            for q, txt in ((base + ".svg", svg), (base + ".md", md)):
                cur = open(q, encoding="utf-8").read() if os.path.exists(q) else None
                if cur != txt:
                    print(f"STALE {q}")
                    rc = 2
        else:
            L.write_text(base + ".svg", svg)
            L.write_text(base + ".md", md)
            print(f"rendered {base}.svg / .md")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
