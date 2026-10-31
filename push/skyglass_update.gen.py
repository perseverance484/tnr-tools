#!/usr/bin/env python3
"""Generate the Skyglass / Crownhold update (push/319, 328, 329), all HIDDEN, placeholder art (RUL-2026-10-30-059).

    python3 push/skyglass_update.gen.py

push/319 was one manifest run by phase. Law 18 (a held jutsu is taken off before it is edited and put back after) puts
AI edits on both sides of the jutsu edits, which validate.py's build-order lint refuses inside one manifest, and the
Core Rupture blast carries the approved law-6 exception (RUL-2026-10-28-002). It is now three ordered manifests:

  319  kit off (AI edits only): Core Rupture off Seal Charge and Core Canister; the Crownhold boss renamed The Crowned
       Captain with the crew sprite and his Last Directive, Extermination Order and Countermand off; the 18 Crownhold
       usernames (RUL-2026-10-26-003).
  328  Core Rupture: a small, heavy blast (RUL-2026-10-28-001). The law-6 pierce exception (RUL-2026-10-28-002) is held
       by state/validate_exceptions/328_skyglass_core_rupture.json.
  329  hidden records only (RUL-2026-10-30-063 item 1): the Last Directive and Countermand texts; the 22 new Skyglass
       items (charts, Haul pages, Core Rot, Galley Stores, Skyglass Token, the seven boss variant tokens), all hidden;
       the 19 variants (no hidden state); kits back on (closes 319); Crownhold created hidden.
  340  the Crownbreaker badge, created by the builder (--badge; RUL-2026-10-31-064 item 3). Runs FIRST, before 319:
       its id goes into state/crownhold/ids.json as badge:crownbreaker, then 329 is regenerated so Crownhold's pick
       carries it.
  338  the seven boss tokens bound to their variants, from 329's results (--binds). (Was 330 until 2026-10-31; renumbered
       because another workstream holds push/330, 332 and 337.)
  339  GO-LIVE (RUL-2026-10-30-063 item 1; was 331), from 329's results (--golive): every edit that changes what live players can
       obtain or see. The 20 edits to existing items (the four Rare charts' text and tier, the Lantern, the Coffer, Sealed
       Treasury, Archive Chart Case, Medicine Inro, Sage's Strongbox, Elemental Tool Pouch, Unmarked Cargo, the 8
       profession chests) and the Buried Cache, Drowned Foundry, Quarantined Archive and Captain's Watch re-sent with the
       section 4a picks, the chart-ladder, Haul-page and boss-token drops, the stakes headers and closing lines (text doc
       2.8, 2.8a, 6.1, 6.2, 8) and the Watch's dawn-watch press-on room (+20% Last Heading only, RUL-2026-10-31-064
       item 2). Runs LAST, after every other manifest of the
       event (push/README.md lists the preconditions). The new items it names are 329 creates, so it carries their
       literal ids from 329's results bundle (L01; check_manifest plans with no retained idmap).

Sources: push/core_rupture.gen.py, push/crownhold.gen.py, push/skyglass_hunts.gen.py (state/skyglass_hunts/hunts.py),
push/skyglass_items.gen.py, docs/design/SKYGLASS_TEXT.md, docs/design/SKYGLASS_LOOT_TABLES.md. Do not hand-edit the output.

Not in these (built later, from these manifests' results): the chart runs, steeping, the Haul, Walked Every
Deck, the Wreck dungeon drops and floors, the set-piece library and the AI copies; see push/README.md.
"""
import copy
import hashlib
import importlib.util
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load(name):
    spec = importlib.util.spec_from_file_location(name.replace(".", "_"), os.path.join(ROOT, "push", name))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


CR, CH, G, IT = load("core_rupture.gen.py"), load("crownhold.gen.py"), load("skyglass_hunts.gen.py"), load("skyglass_items.gen.py")
T = IT.T
BOSS_ID = CH.IDS["@ai:D5.BOSS"]
EXCLUSIVE_JUTSU = {CH.IDS["@jutsu:last_directive"], CH.IDS["@jutsu:extermination_order"]}
COUNTERMAND = CH.IDS["@item:countermand"]
REQUISITION_ITEM, REQUISITION_QUEST = "Fz1MU04kLIIM0EMXgouo6", "3BYr-HMkOepywS77vJvJh"  # retired (RUL-2026-10-28-016)
QUEST_ID = {"foundry": "UGHSuhi83C3wRtH3FD4Eu", "archive": "-bZ_ZoI6yrUJ_LKT9R5zm", "watch": "liljq0yVXWTSna4X6dZE1",
            "cache": "CgwAVCyZLgNQtEnqgLxxv"}  # push/265, 266, 270 (design_data.json picks)
CHART_BURIED_CACHE = "nbLC37UzBamthKXvZsgQB"  # push/270 result (design_data.json items.chart_buried_cache cites this file)
R = IT.ref
assert R("Chart of the Buried Cache") == CHART_BURIED_CACHE
# The Coffer's contents (push/260; design_data.json items cite this file for their names).
COFFER_CONTENTS = {"Skyglass Filament": "CTZ1mwhHrICLtiCaZATY6", "Skyglass Serum": "XhilCv1Hq4eNt-Wddok-m",
                   "Skyglass Katana": "ZSUdrzzgorepP4CQrBfEk"}
assert all(R(n) == i for n, i in COFFER_CONTENTS.items())
PAGES = ["Ledger Page: The Trophy Hold", "Ledger Page: The Bone Store", "Ledger Page: The Snare Room",
         "Stores Manifest: The Overgrown Stores", "Stores Manifest: The Ore Vault", "Stores Manifest: The Bloom Cellar"]
PAGE_RARE_ENDING = 1.5  # per page, every Rare-chart ending (loot tables 4b; RUL-2026-10-30-060 item 5)
HUNT_VARIANT = 1        # boss variant token, his hunt runs (loot tables 5d)


def boss_kit():
    p = next(p for p in CH.PROFILES if p["slot"] == "D5.BOSS")
    ai = CH.ai(p)["data"]
    return ai["jutsus"], [{"ids": it["ids"], "number": it.get("number", 0)} for it in ai["items"]]


# ---------------------------------------------------------------------------------------------------------------
# Hunts (existing records, re-sent whole)
# ---------------------------------------------------------------------------------------------------------------
def drop(name, chance):
    return {"ids": [R(name)], "number": chance, "quantity": 1}


def add_drops(objs, ids, drops):
    for o in objs:
        if o["id"] in ids:
            assert o["task"] == "win_quest", o["id"]
            o["reward_items"] = list(o.get("reward_items") or []) + [dict(d) for d in drops]


def by_id(objs, i):
    return next(o for o in objs if o["id"] == i)


def prepend(o, line):
    o["description"] = line + "<br><br>" + o["description"]


def stakes(run, premise):
    L = T.lines()
    i = next(i for i, l in enumerate(L) if l.startswith(f"- **`quest:{run}.description`** (prepend):"))
    lines = []
    for l in L[i + 1:]:
        if not l.startswith("  `"):
            break
        lines.append(l.strip()[1:-1])
    return "\n".join(lines) + "\n\n" + premise


CLOSE = {row[0] + " @ " + row[1]: row[2] for row in T.table("### 6.2 Closing lines")}
_INTRO = [(row[0], row[2]) for row in T.table("### 6.1 Intro screens")]


def intro(target):
    hits = [p for t, p in _INTRO if target in t]
    assert len(hits) == 1, target
    return hits[0]


def close(boss, where):
    cell = CLOSE[boss + " @ " + where]
    if cell.startswith("`"):
        cell = cell[1:cell.index("`", 1)]
    return cell


PAGE_DROPS = [drop(p, PAGE_RARE_ENDING) for p in PAGES]


def foundry():
    objs = G.foundry()
    o = by_id(objs, "d_pour")
    old = "The Warden cools into a shell of skyglass."
    assert o["description"].startswith(old)
    o["description"] = close("Foundry Warden (Foundry)", "`d_pour`, prepend") + o["description"][len(old):]
    prepend(by_id(objs, "d_gate"), close("Arsenal Keeper (Foundry)", "`d_gate`, prepend"))
    prepend(by_id(objs, "d_racks"), close("Deck Warden (Foundry)", "`d_racks`, prepend"))
    add_drops(objs, {"w_deep"}, [drop("Chart of the Quarantined Archive", 10)] + PAGE_DROPS + [drop("Warden's Forge-Fists", HUNT_VARIANT)])
    reward = G.items_reward((R("Elemental Tool Pouch"), 1), (R("Medicine Inro"), 1), (R("Galley Stores"), 1))
    q = G.quest("hunt_foundry", "The Drowned Foundry", stakes("The Drowned Foundry", G.H.FOUNDRY["premise"]),
                "You carried the last pour out of the keel works.", R("Chart of the Drowned Foundry"),
                "@img:icon-chart-drowned-foundry.webp", objs, reward, "A", QUEST_ID["foundry"])
    return q


def archive():
    objs = G.archive()
    for b in ("b_sealwright", "b_sealwright_a"):
        assert by_id(objs, b)["description"] == "Break the Sealwright's seals."
        by_id(objs, b)["description"] = intro("obj:The Quarantined Archive/b_sealwright.description")
    for w in ("w_clean", "w_alarm"):
        prepend(by_id(objs, w), close("Sealwright (Archive)", "`w_clean`, `w_alarm`, prepend"))
    add_drops(objs, {"w_clean", "w_alarm"}, [drop("Reliquary Seal", 25), drop("Rotted Reliquary Seal", 1)] + PAGE_DROPS
              + [drop("Sealwright's Seal", HUNT_VARIANT)])
    reward = G.items_reward((R("Archive Chart Case"), 1), (R("Sage's Strongbox"), 1), (R("Skyglass Token"), 1))
    return G.quest("hunt_archive", "The Quarantined Archive", stakes("The Quarantined Archive", G.H.ARCHIVE["premise"]),
                   "The archive's last seal is broken and its records are yours.", R("Chart of the Quarantined Archive"),
                   "@img:icon-chart-quarantined-archive.webp", objs, reward, "A", QUEST_ID["archive"])


# A won press-on room pays the step's own ladder ending plus the Last Heading at 45% instead of 25% (loot tables 4a:
# "+20% from its press-on room"; RUL-2026-10-31-064 item 2). It pays no extra ladder step.


def watch():
    objs = G.watch()
    captain = intro("obj:The Captain's Watch/b3*.description")
    for o in objs:
        if o["task"] == "start_battle" and o["id"].startswith("b3"):
            base = "The Captain steps down from the command dais."
            assert o["description"].startswith(base), o["id"]
            o["description"] = captain + o["description"][len(base):]
        if o["id"].startswith("d_term2_"):
            prepend(o, close("Wayfinder (Watch)", "`d_term2_*`, prepend"))
        if o["id"].startswith("d_term3_"):
            prepend(o, close("First Blade (Watch)", "`d_term3_*`, prepend"))
    gallery_add = T.block("obj:The Captain's Watch/d_gallery_*.description")
    gch = T.choices("obj:The Captain's Watch/d_gallery_*.description")
    press = T.block("obj:The Captain's Watch/b_press_*.description")
    press_win = T.block("obj:The Captain's Watch/w_press_*.description")
    fail_press = "You fall back, and keep only what you held."  # text doc section 2, shared press-on failDescription
    new = []
    for step in ("IV", "V", "VI"):
        g = by_id(objs, "d_gallery_" + step)
        assert g["nextObjectiveId"][0]["text"] == gch[0]
        g["description"] += gallery_add
        g["nextObjectiveId"].append({"text": gch[1], "nextObjectiveId": "b_press_" + step})
        b = G.battle("b_press_" + step, "command_observation_gallery", press, ["Deck Warden", "Wayfinder"],
                     "w_press_" + step)[0]
        b["failObjectiveId"] = "w_" + step
        b["failDescription"] = fail_press
        new.append(b)
        w = G.win("w_press_" + step, "command_observation_gallery", press_win, step)
        new.append(w)
    objs = objs[:-1] + new + objs[-1:]  # keep the fail ending last
    ends = {"w_IV", "w_V", "w_VI"}
    add_drops(objs, ends, [drop("The Last Heading", 25), drop("The Rotted Heading", 1)] + PAGE_DROPS
              + [drop("Wayfinder's Heading", HUNT_VARIANT)])
    add_drops(objs, {"w_press_IV", "w_press_V", "w_press_VI"},
              [drop("The Last Heading", 45), drop("The Rotted Heading", 1)] + PAGE_DROPS + [drop("Wayfinder's Heading", HUNT_VARIANT)])
    reward = G.items_reward((R("Skyglass Coffer"), 1), (R("Skyglass Token"), 1), reward_money=1000000)
    return G.quest("hunt_watch", "The Captain's Watch", stakes("The Captain's Watch", G.H.WATCH["premise"]),
                   "You kept the Captain's watch and claimed its stores.", R("Chart of the Captain's Watch"),
                   "@img:icon-chart-captains-watch.webp", objs, reward, "A", QUEST_ID["watch"])


def cache():
    objs = G.cache()
    sentinel = intro("obj:The Buried Cache` Sentinel battle")
    for b in ("b_guardian", "b_guardian_late"):
        assert by_id(objs, b)["description"] == "The Sentinel rises between you and the cache."
        by_id(objs, b)["description"] = sentinel
    fix = next(r for r in T.table("## 8. Corrections") if "The Buried Cache` win objectives" in r[0])
    old, new = "Tucked under the lid is a note in a careful hand: 'For when we are relieved.'", fix[2]
    for w in ("w_clean", "w_late"):
        o = by_id(objs, w)
        assert o["description"].endswith(old)
        o["description"] = o["description"][:-len(old)] + new
    add_drops(objs, {"w_clean", "w_late"}, [drop("Chart of the Drowned Foundry", 15)] + PAGE_DROPS)
    reward = G.items_reward((R("Medicine Inro"), 1), (R("Galley Stores"), 1), (R("Chart of the Drowned Foundry"), 1))
    return G.quest("hunt_buried_cache", "The Buried Cache", stakes("The Buried Cache", G.CACHE_PREMISE),
                   "You dug up the Skyglass crew's field cache.", R("Chart of the Buried Cache"),
                   "@img:icon-chart-drowned-foundry.webp", objs, reward, "B", QUEST_ID["cache"])


def crownhold():
    q = CH.quest()
    q["srcId"] = IT.PFX + "crownhold"
    d = q["data"]
    d["description"] = T.block("quest:Crownhold.description") + "\n\n" + d["description"]
    r = d["content"]["reward"]
    coffer = next(x for x in r["reward_items"] if x["ids"] == [CH.ITEM["coffer"]])
    coffer["quantity"] = 3  # RUL-2026-10-29-050 item 2
    # Crown's Hoard (no id) and the Crownbreaker badge (push/340, RUL-2026-10-31-064 item 3) join when their ids exist
    # (state/crownhold/ids.json badge:crownbreaker; CH.quest() adds reward_badges).
    for o in d["content"]["objectives"]:
        if o["task"] == "win_quest":  # loot tables 4a: Crownhold ending, two independent 25% lines (RUL-2026-10-31-064 item 5)
            o["reward_items"] = list(o.get("reward_items") or []) + [drop("Reliquary Seal", 25), drop("The Last Heading", 25)]
    return q


# ---------------------------------------------------------------------------------------------------------------
# Manifests
# ---------------------------------------------------------------------------------------------------------------
def phased(items, phase):
    return [{**it, "phase": phase} for it in items]


def pack(items):
    files = {}
    used = json.dumps(items)
    for name, path in {**G.IMAGES, **IT.IMAGES, **BADGE_IMAGES}.items():
        if "@img:" + name in used:
            b = open(os.path.join(ROOT, path), "rb").read()
            files[name] = {"path": path, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)}
    return files


def pack_ref(files):
    import subprocess
    paths = [f["path"] for f in files.values()]
    ref = subprocess.check_output(["git", "-C", ROOT, "log", "-1", "--format=%H", "HEAD", "--", *paths], text=True).strip()
    for f in files.values():
        b = subprocess.check_output(["git", "-C", ROOT, "show", f"{ref}:{f['path']}"])
        assert hashlib.sha256(b).hexdigest() == f["sha256"], f["path"]
    return ref


def write(num, slug, note, items, extra=None):
    m = {"_note": note + " Generated by push/skyglass_update.gen.py; do not hand-edit.", "dedupNames": True}
    files = pack(items)
    if files:
        m["imgSizes"] = {k: v["bytes"] for k, v in files.items()}
        m["imagePack"] = {"ref": pack_ref(files), "files": files}
    if extra:
        m.update(extra)
    m["items"] = items
    path = os.path.join(ROOT, f"push/{num}_{slug}.json")
    with open(path, "w") as f:
        json.dump(m, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"push/{num}_{slug}.json: {len(items)} items")


# Edits to existing records that live players can reach today (RUL-2026-10-30-063 item 1): they go in the go-live
# manifest, never in 329. Every item edit push/skyglass_items.gen.py builds must be named here, so a new one cannot slip
# into 329 unclassified.
GO_LIVE_ITEM_EDITS = {
    "Chart of the Buried Cache", "Chart of the Drowned Foundry", "Chart of the Quarantined Archive",
    "Chart of the Captain's Watch", "Lastlight Lantern", "Skyglass Coffer", "Sealed Treasury", "Archive Chart Case",
    "Medicine Inro", "Sage's Strongbox", "Elemental Tool Pouch", "Unmarked Cargo",
    *IT.PROF.values(),
}
# Manifest numbers. push/330, 332 and 337 belong to another workstream (Zombie Outbreak); the binds and go-live
# manifests were 330 and 331 until 2026-10-31 and are now 338 and 339; the badge is 340.
BINDS, GO_LIVE, BADGE = 338, 339, 340
BADGE_SRC = "sg340_crownbreaker_badge"
BADGE_IMAGES = {"icon-badge-crownbreaker-v2.webp": "art/crownhold/icon-badge-crownbreaker-v2.webp"}
# Director-approved description (RUL-2026-10-31-064 item 3, 2026-10-31: no "crown", simple and elegant).
BADGE_DESCRIPTION = "The throne is empty. The order still stands."


def split_items(items):
    """(hidden creates for 329, live item edits for the go-live manifest)."""
    creates = [e for e in items if e["slot"] == "create"]
    edits = [e for e in items if e["slot"] != "create"]
    assert all(e["data"].get("hidden") is True for e in creates)
    ids = {IT.LIVE.get(n) or IT.cid(n): n for n in GO_LIVE_ITEM_EDITS}
    assert {e["targetId"] for e in edits} == set(ids), "an item edit is not classified for 329 / go-live"
    return creates, edits


def resolve_329(o, idmap, missing):
    """Replace every @item/@variant ref to a 329 create with its literal id from 329's results (L01)."""
    if isinstance(o, list):
        return [resolve_329(x, idmap, missing) for x in o]
    if isinstance(o, dict):
        return {k: resolve_329(v, idmap, missing) for k, v in o.items()}
    if isinstance(o, str) and o.startswith("@") and ":" + IT.PFX in o and not o.startswith("@img:"):
        key = o.split(":", 1)[1]
        if not idmap.get(key):
            missing.add(key)
            return o
        return idmap[key]
    return o


def golive(bundle):
    b = json.load(open(bundle))
    idmap = b.get("idmap") or {}
    _, edits = split_items(IT.all_items()["items"])
    body = phased(edits, 1) + phased([cache(), foundry(), archive(), watch()], 2)
    missing = set()
    body = resolve_329(body, idmap, missing)
    if missing:
        raise SystemExit("329 creates missing from the results idmap: " + ", ".join(sorted(missing)))
    write(GO_LIVE, "skyglass_go_live", (
        f"push/{GO_LIVE}, GO-LIVE (RUL-2026-10-30-063 item 1): DO NOT RUN until every other manifest of the Skyglass / "
        "Crownhold event has run (push/README.md lists the preconditions). Built from push/329's results bundle "
        + os.path.basename(bundle) + " (literal ids, L01). Phase 1: the 20 edits to existing items live players can reach "
        "(the four Rare charts' text and tier, the Lantern, the Coffer, Sealed Treasury, Archive Chart Case, Medicine Inro, "
        "Sage's Strongbox, Elemental Tool Pouch, Unmarked Cargo, the 8 profession chests). Phase 2: the Buried Cache, "
        "Drowned Foundry, Quarantined Archive and Captain's Watch re-sent whole (section 4a picks, chart ladder, Haul pages "
        "1.5% each, boss variant tokens 1%, stakes headers and closing lines, the Watch's dawn-watch press-on room: the "
        "step's own ending plus the Last Heading at 45%, no extra ladder step, RUL-2026-10-31-064 item 2)."),
        body)


def badge():
    item = {"entity": "badge", "slot": "create", "srcId": BADGE_SRC, "name": "Crownbreaker",
            "data": {"name": "Crownbreaker", "image": "@img:icon-badge-crownbreaker-v2.webp",
                     "description": BADGE_DESCRIPTION, "hidden": True}}
    write(BADGE, "crownbreaker_badge", (
        f"push/{BADGE} (RUL-2026-10-31-064 item 3; supersedes RUL-2026-10-30-063 item 4's 'by hand'). Runs FIRST, before "
        "push/319. Creates the Crownbreaker badge (Crownhold's pick; image art/crownhold/icon-badge-crownbreaker-v2.webp). "
        "A badge has no hidden column: hidden:true is stripped before the send (law 16b), and nothing grants the badge "
        "until a published reward names it (Crownhold is created hidden by push/329). Description director-approved "
        "(2026-10-31). After it runs: put the new id into state/crownhold/ids.json as badge:crownbreaker, "
        "regenerate (python3 push/skyglass_update.gen.py) and re-run the gates, then run 319, 328, 329."), [item])


def binds(bundle):
    b = json.load(open(bundle))
    write(BINDS, "skyglass_token_binds", (
        f"push/{BINDS} (after 329, from its results bundle " + os.path.basename(bundle) + "). Each of the seven boss variant "
        "tokens is bound to its own variant (unlockitemvariant.variantId; pipeline 2.10 step 3). Until this runs, each "
        "token (all hidden) could unlock any token variant without a required item."), IT.bind_edits(b.get("idmap") or {}))


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--binds":
        return binds(sys.argv[2])
    if len(sys.argv) > 1 and sys.argv[1] == "--badge":
        return badge()
    if len(sys.argv) > 2 and sys.argv[1] == "--golive":
        return golive(sys.argv[2])
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

    write(319, "skyglass_update", (
        "push/319, step 1 of 3 (RUL-2026-10-30-059: hidden, placeholder art). Kit off (law 18), AI edits only: Core "
        "Rupture off Seal Charge and Core Canister (AI Heavy Armor kept); the Crownhold boss renamed The Crowned Captain "
        "with the crew sprite, his Last Directive, Extermination Order and Countermand off (RUL-2026-10-28-003/-004); the "
        f"18 Crownhold usernames (RUL-2026-10-26-003). push/{BADGE} (the Crownbreaker badge) runs before this. Then run "
        "push/328, then push/329."),
        unequip + [boss_off] + renames)

    write(328, "skyglass_core_rupture", (
        "push/328, step 2 of 3 (after 319). Core Rupture: AOE circle spawn, range 5, pierce 180; the self-destruct and the "
        "2-round stun kept (RUL-2026-10-28-001). The law-6 pierce cap is exceeded by ruling (RUL-2026-10-28-002); "
        "gate: python3 scripts/validate_exception.py state/validate_exceptions/328_skyglass_core_rupture.json."),
        [convert])

    ld = {"entity": "jutsu", "slot": "convert", "targetId": CH.IDS["@jutsu:last_directive"],
          "name": "The Last Directive: the Crowned Captain",
          "data": {"description": ("The Crowned Captain's final order to himself. For five rounds he cannot fall, "
                                   "strikes harder, and nothing he carries can be stripped away."),
                   "injectableInBattle": False}}
    cm = {"entity": "item", "slot": "edit", "targetId": COUNTERMAND, "name": "Countermand: the Crowned Captain",
          "data": {"description": CH.countermand()["data"]["description"]}}
    # The retired Armory Requisition (RUL-2026-10-28-016) is already hidden live (push/274 created it hidden); it is no
    # longer edited, and the Unmarked Cargo edit below drops it from the chest of chests.
    parts = IT.all_items()
    creates, _live_edits = split_items(parts["items"])  # the live edits go in the go-live manifest (--golive)
    body = (phased([ld], 1) + phased(creates + [cm], 1) + phased(parts["variants"], 2)
            + phased(reequip + [boss_on], 4) + phased([crownhold()], 5))
    ph = IT.placeholders(body)
    write(329, "skyglass_items_and_quests", (
        "push/329, step 3 of 3 (after 328). Hidden records only (RUL-2026-10-30-063 item 1): nothing here changes what "
        "live players can obtain or see, except the variants (no hidden state). Every new image is the engine default "
        "placeholder (RUL-2026-10-30-059; list in _placeholders). Phase 1: the Last Directive and Countermand texts (hidden "
        "Crownhold exclusives); 22 new HIDDEN items (6 charts, 6 Haul pages, Core Rot, Galley Stores, the Skyglass Token, "
        "7 boss variant tokens). Phase 2: the 19 variants (12 Skyglass, 7 boss); each shows on its base weapon as 'Need "
        f"<token>' from this run, the tokens staying hidden. The seven boss tokens are bound to their variants by push/{BINDS}, "
        "built from this manifest's results. Phase 4: kits back on (Core Rupture; the Crowned Captain's exclusives), "
        "closing push/319. Phase 5: Crownhold created HIDDEN (pick: Skyglass Coffer x3 / Lastlight / Crown Fragment; "
        "Crown's Hoard joins when its id exists; "
        + ("the Crownbreaker badge is in the pick" if "badge:crownbreaker" in CH.IDS
           else f"the Crownbreaker badge joins once push/{BADGE} has run and its id is recorded") + "). The live item edits and the four live chart "
        f"runs' re-sends are push/{GO_LIVE} (go-live), built from this manifest's results and run last."),
        body, {"_placeholders": ph})


if __name__ == "__main__":
    main()
