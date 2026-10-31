#!/usr/bin/env python3
"""Skyglass final art push, part 1 (push/372): image-only edits on existing records.

    python3 push/skyglass_final_art.gen.py       # writes push/372_skyglass_final_art.json

One direct edit per row, only the image field (item/jutsu `image`, AI `avatar`), so nothing else changes and hidden
records stay hidden. Exports are pinned by the newest commit that touched them (commit them first). Records named here
all exist live (ids from the art register and the results bundles). Not here (separate builds): scene backgrounds
SC01-SC06 and the salvager PT01 (quest edits), FX AN01-AN09 (gameAsset creates + library jutsu edits), the Chart of the
Buried Cache icon (held back by the art audit until its seal is checked). Do not hand-edit the output.
"""
import hashlib, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NUM = 372
OUT = os.path.join(ROOT, "push", f"{NUM}_skyglass_final_art.json")
I, A, J = "art/skyglass_event_icons/exports/", "art/crownhold/avatars/exports/", "art/skyglass_jutsu_icons/exports/"
FW = "art/skyglass_event_icons/avatars/avatar_skyglass_foundry_warden.webp"
ROWS = [  # (entity, id, name, field, export)
    ("item", "nzCW7A-_AuYMzBs2wClnM", "Skyglass Token", "image", I + "icon-skyglass-token.webp"),
    ("item", "vltFmOTgOyqssIpNXvT37", "Captain's Gunbai (token)", "image", I + "icon-variant-token-captains-gunbai.webp"),
    ("item", "-7dQs2qwokuNSAS2c3X8Q", "Rotbloom (token)", "image", I + "icon-variant-token-rotbloom.webp"),
    ("item", "d96tj122ex6BnzhMDwy0s", "Forgefists (token)", "image", I + "icon-variant-token-forgefists.webp"),
    ("item", "giSqzJqE6YdsrnOoy1KLV", "Wayfinder (token)", "image", I + "icon-variant-token-wayfinder.webp"),
    ("item", "5rpvgpKckgmN-vXjzJpb8", "The First Blade (token)", "image", I + "icon-variant-token-the-first-blade.webp"),
    ("item", "3ZR700BAWr_Pd3Eqnu1c9", "Sealscript (token)", "image", I + "icon-variant-token-sealscript.webp"),
    ("item", "pqKpEqo-x6BHTjxTRUEfD", "Crownbreaker (token)", "image", I + "icon-variant-token-crownbreaker.webp"),
    ("item", "oSFTrX15PqtFtjwRXk041", "The Little Horror's Jar", "image", I + "icon-little-horrors-jar.webp"),
    ("item", "D-QTnbjgTyIVc593zzdSB", "Galley Stores", "image", I + "icon-galley-stores.webp"),
    ("item", "WrnHlt3h6ZDjFaJk3i41O", "Crown's Hoard", "image", I + "icon-crowns-hoard.webp"),
    ("item", "W3lOjQhhIPUYPkIZmiNum", "Countermand", "image", I + "icon-countermand.webp"),
    ("item", "pZxD40F8sn1oE5XuaqILx", "Keeper's Reserve", "image", I + "icon-legendary-hunters-chest.webp"),
    ("item", "dpMIYFFcfa6PKkcGsoTUs", "Quartermaster's Reserve", "image", I + "icon-legendary-gatherers-chest.webp"),
    ("jutsu", "0F-68bxOXW_LkJnXV0lwT", "Lastlight", "image", J + "icon-jutsu-lastlight.webp"),
    ("jutsu", "GYy5K24tGkYIeGEJef3TW", "Little Maw", "image", J + "icon-jutsu-little-maw.webp"),
    ("jutsu", "GHFMU_DDKvBBp5BEuTeah", "The Last Directive", "image", J + "icon-jutsu-the-last-directive.webp"),
    ("jutsu", "EqZsaqser8c2-KpVCaXk_", "Extermination Order", "image", J + "icon-jutsu-extermination-order.webp"),
    ("ai", "1syezT0axWVQVgeOGN-LH", "Crown Tagwright", "avatar", A + "avatar_crownhold_tagwright.webp"),
    ("ai", "e5ye0RlN0fManSKdD_k-o", "Crown Lancer", "avatar", A + "avatar_crownhold_lancer.webp"),
    ("ai", "1orTQQ0Q9XhBvwlSZuzj5", "Honor Guard", "avatar", A + "avatar_crownhold_honor-guard.webp"),
    ("ai", "-U_-iIwhGodkqdvc4GPa6", "Crown Runner", "avatar", A + "avatar_crownhold_runner.webp"),
    ("ai", "pshn-LkaC5vIgI6EOv68I", "Crown Vanguard", "avatar", A + "avatar_crownhold_vanguard.webp"),
    ("ai", "Q6QjSoH6d1SabfQOLb12-", "Crown Herald", "avatar", A + "avatar_crownhold_herald.webp"),
    ("ai", "qQn9h2FY3GUUqgaFIRAuf", "Last Watch", "avatar", A + "avatar_crownhold_last-watch.webp"),
    ("ai", "09gLgh9sCtshISC0dvpka", "Crown Sealbearer", "avatar", A + "avatar_crownhold_sealbearer.webp"),
    ("ai", "-GKFYAZUg1eF-3VnZhDjx", "Crown Armsmaster", "avatar", "art/crownhold/avatar_crownhold_master_of_arms.webp"),
    ("ai", "vjEFUJ9mb1zNTuQf4lfXv", "Replicant Zero", "avatar", "art/crownhold/avatar_crownhold_replicant_zero.webp"),
    ("ai", "ZsfRoyJ55Zsay5bHNLMPv", "The Second", "avatar", "art/crownhold/avatar_crownhold_the_grand_marshal.webp"),
    ("ai", "81lnIP-q97gItQYWl5vWD", "Foundry Warden", "avatar", FW),
    ("ai", "hBbq6ZO4JJE11ZIjGwN4k", "Veteran Foundry Warden", "avatar", FW),
    ("ai", "ySwv3MDO5a-fzUF99M3pi", "Rot-Touched Foundry Warden", "avatar", FW),
]


def git(*a):
    return subprocess.check_output(["git", "-C", ROOT, *a], text=True).strip()


def main():
    paths = sorted({r[4] for r in ROWS})
    ref = git("log", "-1", "--format=%H", "HEAD", "--", *paths)
    files = {}
    for p in paths:
        disk = open(os.path.join(ROOT, p), "rb").read()
        if subprocess.check_output(["git", "-C", ROOT, "show", f"{ref}:{p}"]) != disk:
            sys.exit(f"{p}: working copy differs from {ref}; commit it first")
        files[os.path.basename(p)] = {"path": p, "sha256": hashlib.sha256(disk).hexdigest(), "bytes": len(disk)}
    order = {"jutsu": 0, "item": 1, "ai": 2}  # build order (validator: jutsu before later phases)
    items = []
    for e, t, n, f, p in sorted(ROWS, key=lambda r: order[r[0]]):
        data = {f: "@img:" + os.path.basename(p)}
        if e == "jutsu":
            data["injectableInBattle"] = False  # law 20: sent explicitly; all four were created non-injectable
        items.append({"entity": e, "slot": "edit", "name": f"{n}: final art", "targetId": t, "data": data})
    m = {"_note": (f"push/{NUM}: Skyglass final art, part 1: {len(items)} image-only edits (item icons, boss tokens, "
                   "Haul Reserves, jutsu icons, AI avatars) on existing records; nothing else changes, hidden stays "
                   "hidden. Generated by push/skyglass_final_art.gen.py; do not hand-edit."),
         "dedupNames": True, "imgSizes": {k: v["bytes"] for k, v in files.items()},
         "imagePack": {"ref": ref, "files": files}, "items": items}
    json.dump(m, open(OUT, "w"), indent=1, ensure_ascii=False)
    open(OUT, "a").write("\n")
    print(f"push/{NUM}_skyglass_final_art.json: {len(items)} items, {len(files)} images")


if __name__ == "__main__":
    main()
