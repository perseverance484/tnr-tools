#!/usr/bin/env python3
"""Generate push/319: the Skyglass / Crownhold update, one manifest (director 2026-10-28: "one large update").

    python3 push/skyglass_update.gen.py

Assembles, by phase (law 18: an equipped jutsu or held item is taken off before it is edited and put back after):
  Phase 1  take Core Rupture off Seal Charge and Core Canister; take the Last Directive, Extermination Order and
           Countermand off the Crownhold boss while renaming it "The Crowned Captain" with the crew sprite
           (RUL-2026-10-28-003/-004); the 18 Crownhold usernames (was push/276, RUL-2026-10-26-003); the Katon Tool
           Pouch becomes the Elemental Tool Pouch.
  Phase 2  Core Rupture: a small, heavy blast (RUL-2026-10-28-001); the Last Directive's and Countermand's text name
           the Crowned Captain; the Armory Requisition and the Drowned Foundry pick 1 of 3.
  Phase 3  put Core Rupture back on both hazards and the exclusives back on the boss; create Crownhold (was push/273).
Still to join before it runs: the Wreck dungeon's AI copies and dungeon edit (harness pending), the easy dungeon, and the
Crownbreaker badge id. Sources: push/core_rupture.gen.py, push/elemental_pouch.gen.py, push/crownhold.gen.py.
Do not hand-edit the output.
"""
import importlib.util, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace(".", "_"), os.path.join(ROOT, "push", name))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


CR, EP, CH = load("core_rupture.gen.py"), load("elemental_pouch.gen.py"), load("crownhold.gen.py")
BOSS_ID = CH.IDS["@ai:D5.BOSS"]
EXCLUSIVE_JUTSU = {CH.IDS["@jutsu:last_directive"], CH.IDS["@jutsu:extermination_order"]}
COUNTERMAND = CH.IDS["@item:countermand"]


def phased(items, phase):
    return [{**it, "phase": phase} for it in items]


def boss_kit():
    p = next(p for p in CH.PROFILES if p["slot"] == "D5.BOSS")
    ai = CH.ai(p)["data"]
    return ai["jutsus"], [{"ids": it["ids"], "number": it.get("number", 0)} for it in ai["items"]]


def main():
    jutsus, items = boss_kit()
    assert EXCLUSIVE_JUTSU <= set(jutsus) and any(COUNTERMAND in it["ids"] for it in items)
    unequip, convert, reequip = CR.main()
    boss_off = {"entity": "ai", "slot": "edit", "targetId": BOSS_ID, "name": "Crownhold boss -> The Crowned Captain (kit off, law 18)",
                "data": {"username": CH.BOSS_NAME, "avatar": CH.SPRITE["D5.BOSS"],
                         "jutsus": [j for j in jutsus if j not in EXCLUSIVE_JUTSU],
                         "items": [it for it in items if COUNTERMAND not in it["ids"]]}}
    boss_on = {"entity": "ai", "slot": "edit", "targetId": BOSS_ID, "name": "The Crowned Captain: kit back on",
               "data": {"jutsus": jutsus, "items": items}}
    renames = [{"entity": "ai", "slot": "edit", "name": CH.USERNAME[p["name"]], "targetId": CH.IDS["@ai:" + p["slot"]],
                "data": {"username": CH.USERNAME[p["name"]]}} for p in CH.PROFILES if p["name"] in CH.USERNAME]
    ld = CH.COMMANDERS["exclusives"]["X:LAST_DIRECTIVE"]["record"]
    ld_text = {"entity": "jutsu", "slot": "convert", "targetId": CH.IDS["@jutsu:last_directive"],
               "name": "The Last Directive: the Crowned Captain",
               "data": {"description": ("The Crowned Captain's final order to himself. For five rounds he cannot fall, "
                                        "strikes harder, and nothing he carries can be stripped away."),
                        "injectableInBattle": False}}
    cm_text = {"entity": "item", "slot": "edit", "targetId": COUNTERMAND, "name": "Countermand: the Crowned Captain",
               "data": {"description": CH.countermand()["data"]["description"]}}
    pouch, armory, foundry = EP.pouch_edit(), EP.armory_edit(), EP.foundry_edit()
    # Story rewrite (docs/design/SKYGLASS_STORY_BIBLE.md, 2026-10-28): the other three hunts re-sent whole with the new
    # text; rewards, ladders, fights and debuffs as last written (push/268, push/270).
    G = EP.G
    archive = G.quest("hunt_archive", "The Quarantined Archive", G.H.ARCHIVE["premise"],
                      "The archive's last seal is broken and its records are yours.", G.ITEM["chart_archive"],
                      "@img:icon-chart-quarantined-archive.webp", G.archive(),
                      G.items_reward((G.ITEM["case"], 1), (G.ITEM["strongbox"], 1), reward_exp=15000), "A", "-bZ_ZoI6yrUJ_LKT9R5zm")
    watch = G.quest("hunt_watch", "The Captain's Watch", G.H.WATCH["premise"],
                    "You kept the Captain's watch and claimed its stores.", G.ITEM["chart_watch"],
                    "@img:icon-chart-captains-watch.webp", G.watch(),
                    G.items_reward((G.ITEM["coffer"], 1), (G.ITEM["inro"], 3), reward_money=100000), "A", "liljq0yVXWTSna4X6dZE1")
    cache = G.quest("hunt_buried_cache", "The Buried Cache", G.CACHE_PREMISE,
                    "You dug up the Skyglass crew's field cache.", "nbLC37UzBamthKXvZsgQB",
                    "@img:icon-chart-drowned-foundry.webp", G.cache(),
                    G.items_reward((G.ITEM["inro"], 1), reward_money=50000, reward_exp=5000), "B", "CgwAVCyZLgNQtEnqgLxxv")
    requisition = {"entity": "item", "slot": "edit", "targetId": "Fz1MU04kLIIM0EMXgouo6", "name": "Armory Requisition: text",
                   "data": {"description": ("A sealed requisition slip from the Skyglass armory. Present it to draw one "
                                            "issue: an Elemental Tool Pouch, a Medicine Inro, or a purse of ryo.")}}
    quest = CH.quest()
    badge = "badge:crownbreaker" in CH.IDS
    items = (phased(unequip + [boss_off] + renames + [pouch], 1)
             + phased([convert, ld_text, cm_text, requisition, armory, foundry, archive, watch, cache], 2)
             + phased(reequip + [boss_on, quest], 3))
    # image pack: the Foundry's chart icon (hunts pack) is the only @img; the Crownhold quest uses a live sprite
    files = {}
    used = json.dumps(items)
    for name, path in EP.G.IMAGES.items():
        if "@img:" + name in used:
            import hashlib
            b = open(os.path.join(ROOT, path), "rb").read()
            files[name] = {"path": path, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
    m = {"_note": (
            "push/319 Skyglass / Crownhold update, all HIDDEN (director 2026-10-28: one large update). Phase 1: Core Rupture "
            "off both hazards; the Crownhold boss renamed The Crowned Captain with the crew sprite, exclusives off; the 18 "
            "Crownhold usernames (RUL-2026-10-26-003); Katon Tool Pouch -> Elemental Tool Pouch. Phase 2: Core Rupture = AOE "
            "circle spawn, range 5, pierce 180 (self-destruct and 2r stun kept; RUL-2026-10-28-001, law-6 exception "
            "RUL-2026-10-28-002); the Last Directive and Countermand texts; Armory Requisition and Drowned Foundry pick 1 of: "
            "Elemental Tool Pouch / Medicine Inro / 50,000 ryo; the Archive, Watch and Buried Cache re-sent with the story-bible text "
            "(docs/design/SKYGLASS_STORY_BIBLE.md); the Armory Requisition's text. Phase 3: kits back on; Crownhold created (Crowned Captain "
            "story, RUL-2026-10-28-004; pick gains a Crown fragment). " + ("" if badge else "HOLD: no Crownbreaker badge id yet. ")
            + "Generated by push/skyglass_update.gen.py; do not hand-edit."),
         "dedupNames": True, "imgSizes": {k: v["bytes"] for k, v in files.items()},
         "imagePack": {"ref": EP.G.PACK_REF, "files": files}, "items": items}
    json.dump(m, open(os.path.join(ROOT, "push/319_skyglass_update.json"), "w"), indent=1)
    print(len(items), "items;", "badge in" if badge else "NO BADGE ID YET")


if __name__ == "__main__":
    main()
