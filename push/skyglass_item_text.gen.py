#!/usr/bin/env python3
"""Skyglass item description pass for the HIDDEN records already created (push/360; RUL-2026-10-31-074).

    python3 push/skyglass_item_text.gen.py        # writes push/360_skyglass_item_text.json

Description-only edits, so `hidden` and every other field stay as they are (a Forge edit is merged over the live
record). Live records reachable by players today get their new text from go-live push/339 instead
(push/skyglass_update.gen.py --golive); nothing here is live-visible except the one variant below.

- 22 push/329 creates: the six new charts, the six Haul pages, Core Rot, Galley Stores, the Skyglass Token and the seven
  boss variant tokens (tokens: the section 4.3 template with each token's story line and base weapon).
- The Little Horror's Jar (push/346) and Crown's Hoard (push/348; its text rendered from the Coffer and Treasury tables
  by push/skyglass_hoard.gen.py, which checks it against the text doc).
- The Crownbreaker variant (push/329, on Thornsilver): description blanked until Walked Every Deck exists
  (RUL-2026-10-31-072 item 6, RUL-2026-10-31-069). Variants have no hidden state, so this one shows today.

Every description is read verbatim from docs/design/SKYGLASS_TEXT.md (via push/skyglass_text.py) and every id is the
VERIFIED create of that exact name in its run's results bundle (literal ids, L01); a renamed or missing record stops
the build. Do not hand-edit the output; change the text doc and re-run.
"""
import importlib.util
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NUM = 360
OUT = os.path.join(ROOT, "push", f"{NUM}_skyglass_item_text.json")
BUNDLES = {  # push number -> results bundle (push/README.md run logs)
    329: "harvests/inbox/tnr_results_1793424666625.json",
    346: "harvests/inbox/tnr_results_1793463543589.json",
    348: "harvests/inbox/tnr_results_1793459592295.json",
}


def _load(name):
    spec = importlib.util.spec_from_file_location(name.replace(".", "_"), os.path.join(ROOT, "push", name))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


H = _load("skyglass_hoard.gen.py")
IT, T = H.IT, H.T

CHARTS = ["Tide Chart", "Watch Roster", "Reliquary Seal", "The Last Heading", "Rotted Reliquary Seal", "The Rotted Heading"]
OTHERS = ["Core Rot", "Galley Stores", "Skyglass Token"]


def created(num, entity="item"):
    """name -> id of every VERIFIED create of `entity` in push/<num>'s results bundle."""
    out = {}
    for e in json.load(open(os.path.join(ROOT, BUNDLES[num])))["entries"]:
        if e["entity"] == entity and e["slot"] == "create" and e.get("forgeState") == "VERIFIED":
            assert e["name"] not in out, e["name"]
            out[e["name"]] = e["id"]
    return out


def token_text():
    """Boss token descriptions: the section 4.3 template filled per token (story line, variant, base)."""
    L = T.lines()
    i = next(i for i, l in enumerate(L) if l.startswith("**Boss variant tokens.**"))
    j = next(j for j in range(i, len(L)) if L[j].startswith("```")) + 1
    tmpl = L[j]
    return {name: tmpl.replace("<story line>", story).replace("<Variant>", name).replace("<Base>", base)
            for name, base, story in IT.VT}


def main():
    c329, c346, c348 = created(329), created(346), created(348)
    v329 = created(329, "itemVariant")
    rows = []  # (id, name, description)
    for name in CHARTS + IT.PAGES + OTHERS:
        rows.append((c329[name], name, T.block(f"item:{name}.description")))
    tokens = token_text()
    assert len(tokens) == 7
    for name, desc in tokens.items():
        rows.append((c329[name], name, desc))
    rows.append((c346["The Little Horror's Jar"], "The Little Horror's Jar", T.block("item:The Little Horror's Jar.description")))
    rows.append((c348["Crown's Hoard"], "Crown's Hoard", H.hoard_description()))
    assert len(rows) == 24 and len({r[0] for r in rows}) == 24
    items = [{"entity": "item", "slot": "edit", "name": f"{name}: text (RUL-2026-10-31-074)", "targetId": tid,
              "data": {"description": desc}} for tid, name, desc in rows]

    # The Crownbreaker variant (F09): blank. itemId is the envelope key Forge needs for a variant edit.
    design = json.load(open(os.path.join(ROOT, "state/skyglass_design/design_data.json")))["variants"]["var_vt_crownbreaker"]
    vid = v329["Crownbreaker"]
    assert design["id"] == vid and design["base_item"] == IT.base_id("Thornsilver"), design
    items.append({"entity": "itemVariant", "slot": "edit", "name": "Crownbreaker (variant): description blanked (RUL-2026-10-31-072 item 6)",
                  "targetId": vid, "data": {"itemId": design["base_item"], "description": ""}})

    m = {
        "_note": (f"push/{NUM} Skyglass item description pass (RUL-2026-10-31-074) for the HIDDEN records already created by "
                  "push/329, 346 and 348: 24 description-only item edits (Tide Chart, Watch Roster, Reliquary Seal, The Last "
                  "Heading, Rotted Reliquary Seal, The Rotted Heading, the six Haul pages, Core Rot, Galley Stores, the "
                  "Skyglass Token, the seven boss variant tokens, The Little Horror's Jar, Crown's Hoard) and one itemVariant "
                  "edit blanking the Crownbreaker variant's description until Walked Every Deck exists (RUL-2026-10-31-072 item "
                  "6). hidden is not touched (Forge merges an edit over the live record). Text read verbatim from "
                  "docs/design/SKYGLASS_TEXT.md; ids literal from the 329/346/348 results bundles. Live records get their text "
                  "from go-live push/339. Generated by push/skyglass_item_text.gen.py; do not hand-edit."),
        "items": items,
    }
    with open(OUT, "w") as f:
        json.dump(m, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"push/{NUM}_skyglass_item_text.json: {len(items)} items")


if __name__ == "__main__":
    main()
