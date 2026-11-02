#!/usr/bin/env python3
"""Skyglass mark fix: telegraph and pool art that stays on screen until the danger resolves (RUL-2026-11-02-101).

    python3 push/skyglass_mark_fix.gen.py   -> push/430_skyglass_mark_fix_unequip.json  (AI edits: the edited jutsu off)
                                            -> push/431_skyglass_mark_fix.json          (jutsu edits: effects only)
                                            -> push/432_skyglass_mark_fix_reequip.json  (AI edits: exact kits back on)

Cause (theninjarpg@3314d122; offline probe, zero live requests): at the end of every combat.performAction request the
server keeps only the visual ground effects created in the round the request started in or later
(routers/combat.ts:857-859, originalRound :652), whatever their `rounds`. A round is a full cycle of every combatant
(libs/combat/actions.ts:1707-1708). So a `visual` cast in round R disappears after the first request that starts in
round R+1, which is usually a player's first action of the next round, while the blast that follows (its own
coordinates, gated on the caster's marker) still lands. Non-visual ground effects live by `rounds`
(libs/combat/util.ts:3035-3060, process.ts:284-312) and are drawn at their hex by the client
(rendering/scenes/combatEffects.ts sync). Copies of ground effects onto a standing user are never persisted
(process.ts:406-412, :1667), so the art stays on the ground and does not follow a player.

431 changes, per jutsu (effects only; injectableInBattle false sent explicitly, law 20):
  * Marks (every live Skyglass telegraph with tile art on a rounds-1 `visual`: the 12 Omen marks of push/342): each
    art-bearing visual becomes a carrier, `increaseregeneration` power 1 rounds 1 friendlyFire FRIENDLY, carrying the
    visual's staticAssetPath, staticAnimation, appearAnimation and disappearAnimation, target INHERIT (the Three Lights
    safe-star visual keeps its target COORDINATES and coordinateTargeting, or it would land on the struck hexes).
    increaseregeneration has no combat consumer at the pin (routers/combat.ts:4102 skips it; libs/cooking.ts,
    timedBuffs.ts, titles.ts only), and no Skyglass rule tests it with has_effect. FRIENDLY: players never get the
    passing copy and are no longer logged as its targets (actions.ts:1092-1110). The self marker is unchanged.
  * Pools (art on a `visual` while a lasting ground effect outlives it): Eruption: Ebb Scatter and Flood Scatter
    (damage 30 for 2 rounds, push/342) and Spreading Fire I-III (drain 5% for 10 rounds; art from push/376): the visual's
    staticAssetPath, staticAnimation and appearAnimation move onto the lasting effect, no disappearAnimation, and the
    visual is dropped. Who is hit does not change: the lasting effect keeps its friendlyFire ENEMIES; checkFriendlyFire
    (process.ts:165-186) reads only creatorId and friendlyFire; a visual never applied to anyone (process.ts:399).
Side effect: a non-visual ground effect with rounds writes "<caster> marked the ground with <type> for the next N rounds"
to the battle log when cast (process.ts:391-396): every Omen mark now adds "... with increaseregeneration for the next
1 rounds". The pools already wrote theirs (damage, drain).

Law 18/60 and the hidden save: every edited jutsu is hidden (push/342 creates; push/390 unhid none of them), and a save
with hidden true runs updateUserJutsuForUpdate (routers/jutsu.ts:1117-1118), which unequips every holder. Hence 430
(off) -> 431 (edit) -> 432 (back on), the push/375-377 and 398-400 pattern. An AI edit inserts only ids that change, so
430 must take them off first.

Holders: every AI whose newest RUN kit holds an edited jutsu. For each AI the generator walks the committed results
bundles (harvests/inbox, archive) in time order, maps every ok AI entry to its committed manifest item (name + id or
srcId), and takes the jutsus of the newest send that carried jutsus and the items of the newest send that carried items.
Rules are not sent (fetch-merge keeps the live rules exactly). A committed manifest that has not run is ignored; if
push/414 (Core Horror kit swap) has run by the time this is regenerated, its kits are picked up automatically.
Do not hand-edit the outputs.
"""
import copy
import glob
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NUM = {"unequip": 430, "edit": 431, "reequip": 432}
LIB = "push/342_skyglass_library.json"
LIB_BUNDLE = "harvests/inbox/tnr_results_1793426982231.json"  # push/342 run, 41/41 ok
FX = "push/376_skyglass_fx.json"
FX_BUNDLE = "harvests/inbox/tnr_results_1793489791328.json"  # push/376 run (@scene refs -> literal asset ids)
MARK_PREFIX = "Omen: "
POOLS = ("Eruption: Ebb Scatter", "Eruption: Flood Scatter", "Spreading Fire I", "Spreading Fire II", "Spreading Fire III")
ART = ("staticAssetPath", "staticAnimation")
CARRIER = {"type": "increaseregeneration", "power": 1, "powerPerLevel": 0, "rounds": 1, "friendlyFire": "FRIENDLY",
           "calculation": "percentage", "description": "Increase out-of-combat regeneration"}
INJECTABLE = False  # law 20; push/342 created them all false


def jload(p):
    return json.load(open(os.path.join(ROOT, p)))


def manifests():
    out = []
    for p in sorted(glob.glob(os.path.join(ROOT, "push/*.json"))) + sorted(glob.glob(os.path.join(ROOT, "archive/**/*.json"), recursive=True)):
        if "tnr_results_" in p or "_skyglass_mark_fix" in os.path.basename(p):  # skip bundles and this generator's outputs
            continue
        try:
            d = json.load(open(p))
        except (ValueError, UnicodeDecodeError):
            continue
        if isinstance(d, dict) and isinstance(d.get("items"), list):
            out.append((os.path.relpath(p, ROOT), d))
    return out


def bundles():
    out = []
    for p in glob.glob(os.path.join(ROOT, "harvests/inbox/tnr_results_*.json")) + glob.glob(os.path.join(ROOT, "archive/**/tnr_results_*.json"), recursive=True):
        try:
            b = json.load(open(p))
        except (ValueError, UnicodeDecodeError):
            continue
        if isinstance(b, dict) and isinstance(b.get("entries"), list) and b.get("at"):
            out.append((b["at"], os.path.relpath(p, ROOT), b))
    out.sort(key=lambda x: x[0])
    return out


def targets():
    """Edited jutsu: live id -> (name, current effects). push/342 as committed (= live; 343 changed text only), with
    push/376's later effects for Spreading Fire I-III (@scene refs resolved from its bundle)."""
    lib = jload(LIB)["items"]
    b = jload(LIB_BUNDLE)
    assert sum(e["state"] == "ok" for e in b["entries"]) == len(lib) == 41
    ids = b["idmap"]
    cur = {}
    for it in lib:
        n = it["name"]
        if n.startswith(MARK_PREFIX) or n in POOLS:
            assert it["data"]["hidden"] is True and it["data"]["injectableInBattle"] is INJECTABLE, n
            cur[ids[it["srcId"]]] = (n, copy.deepcopy(it["data"]["effects"]))
    fxb = jload(FX_BUNDLE)
    assert fxb["outcome"] == "success" and all(e["state"] == "ok" for e in fxb["entries"])
    scene = {k: v for k, v in fxb["idmap"].items() if k.startswith("sg376_")}
    for it in jload(FX)["items"]:
        if it["entity"] == "jutsu" and it["targetId"] in cur:
            effs = copy.deepcopy(it["data"]["effects"])
            for e in effs:
                for k, v in list(e.items()):
                    if isinstance(v, str) and v.startswith("@scene:"):
                        e[k] = scene[v[len("@scene:"):]]
            cur[it["targetId"]] = (cur[it["targetId"]][0], effs)
    # nothing else has sent effects for these ids
    for path, d in manifests():
        if path in (LIB, FX):
            continue
        for it in d["items"]:
            if it.get("entity") == "jutsu" and it.get("targetId") in cur:
                assert "effects" not in it["data"], (path, it["targetId"])
    assert len(cur) == 17, len(cur)
    return cur


def is_art_visual(e):
    return e["type"] == "visual" and any(e.get(k) for k in ART)


def fix(name, effects):
    """Return (new effects, change log, kind)."""
    log, out = [], []
    if name.startswith(MARK_PREFIX):
        vis = [e for e in effects if is_art_visual(e)]
        assert vis and all(e["rounds"] == 1 for e in vis), name
        assert all(e["type"] == "visual" or e["target"] == "SELF" for e in effects if not is_art_visual(e)), name
        for e in effects:
            if not is_art_visual(e):
                out.append(copy.deepcopy(e))
                continue
            c = copy.deepcopy(e)
            c.update(CARRIER)
            if e["target"] != "COORDINATES":
                c["target"] = "INHERIT"
                c.pop("coordinateTargeting", None)
            log.append(f"{name}: visual (target {e['target']}, art {e.get('staticAssetPath')}/{e.get('staticAnimation')}) -> "
                       f"increaseregeneration carrier p1 r1 FRIENDLY target {c['target']}, same art and appear/disappear")
            out.append(c)
        return out, log, "mark"
    vis = [e for e in effects if e["type"] == "visual"]
    assert len(vis) == 1 and is_art_visual(vis[0]) and vis[0]["rounds"] > 1, name
    v = vis[0]
    last = [e for e in effects if e["type"] != "visual" and e.get("rounds") == v["rounds"]]
    assert len(last) == 1 and last[0]["friendlyFire"] == "ENEMIES" and last[0]["target"] == "INHERIT", name
    t = last[0]
    assert not any(t.get(k) for k in (*ART, "appearAnimation", "disappearAnimation")), name
    for e in effects:
        if e is v:
            continue
        c = copy.deepcopy(e)
        if e is t:
            for k in (*ART, "appearAnimation"):
                c[k] = v[k]
            c["disappearAnimation"] = ""
        out.append(c)
    log.append(f"{name}: visual r{v['rounds']} dropped; {t['type']} r{t['rounds']} (friendlyFire ENEMIES, unchanged) takes "
               f"staticAssetPath {v['staticAssetPath']}, staticAnimation {v['staticAnimation']}, appearAnimation "
               f"{v['appearAnimation']}; no disappearAnimation")
    return out, log, "pool"


def holders(edited):
    """Every AI whose newest run kit holds an edited jutsu, with that kit and the items of its newest items send."""
    items = {}
    for path, d in manifests():
        for it in d["items"]:
            if it.get("entity") == "ai":
                items.setdefault(it.get("name") or it["data"].get("username"), []).append((path, it))
    hist = {}
    for at, bpath, b in bundles():
        for e in b["entries"]:
            if e.get("entity") != "ai" or e.get("state") != "ok" or not e.get("id"):
                continue
            cands = [(p, it) for p, it in items.get(e.get("name"), [])
                     if it.get("targetId") == e["id"] or (it["slot"] == "create" and it.get("srcId") and it.get("srcId") == e.get("srcId"))]
            datas = {json.dumps(it["data"], sort_keys=True) for _, it in cands}
            pick = cands[0] if len(datas) == 1 else ("AMBIGUOUS", [p for p, _ in cands]) if cands else None
            hist.setdefault(e["id"], []).append((at, bpath, pick, e["name"]))
    out = []
    for aid, h in hist.items():
        if not any(c and c[0] != "AMBIGUOUS" and any(j in edited for j in c[1]["data"].get("jutsus") or []) for _, _, c, _ in h):
            continue
        bad = [(b, c[1]) for _, b, c, _ in h if c and c[0] == "AMBIGUOUS"]
        assert not bad, (aid, bad)  # a holder's history must map to exactly one manifest item per send
        kit = next(((at, b, c) for at, b, c, _ in reversed(h) if c and "jutsus" in c[1]["data"]), None)
        if not kit or not any(j in edited for j in kit[2][1]["data"]["jutsus"]):
            continue
        # every send after the kit send is mapped (an unmapped later send could have changed the kit)
        later = [x for x in h if x[0] > kit[0]]
        assert all(x[2] for x in later), (aid, [x[1] for x in later if not x[2]])
        it_send = next(((at, b, c) for at, b, c, _ in reversed(h) if c and "items" in c[1]["data"]), None)
        assert it_send, aid
        d = kit[2][1]["data"]
        name = d.get("username") or kit[2][1]["name"].split(":")[0]
        out.append({"id": aid, "name": name, "kit": list(d["jutsus"]), "kitFrom": f"{kit[2][0]} (run {os.path.basename(kit[1])})",
                    "items": copy.deepcopy(it_send[2][1]["data"]["items"]),
                    "itemsFrom": f"{it_send[2][0]} (run {os.path.basename(it_send[1])})",
                    "off": [j for j in d["jutsus"] if j in edited]})
    out.sort(key=lambda h: h["name"])
    assert len(set(h["id"] for h in out)) == len(out)
    return out


def ai_edit(h, jutsus, label):
    return {"entity": "ai", "slot": "edit", "targetId": h["id"], "name": f"{h['name']}: {label}",
            "data": {"jutsus": jutsus, "items": h["items"]}}


def write(num, slug, m):
    path = os.path.join(ROOT, "push", f"{num}_{slug}.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(m, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(f"push/{num}_{slug}.json: {len(m['items'])} items")


def main():
    cur = targets()
    edits, changes, kinds = [], [], {}
    for jid, (name, effects) in sorted(cur.items(), key=lambda x: x[1][0]):
        new, log, kind = fix(name, effects)
        kinds[jid] = kind
        changes += log
        edits.append({"entity": "jutsu", "slot": "edit", "targetId": jid,
                      "name": f"{name}: {'telegraph art on a lasting carrier' if kind == 'mark' else 'pool art on the lasting effect'}",
                      "data": {"effects": new, "injectableInBattle": INJECTABLE}})
    hs = holders(set(cur))
    names = {jid: n for jid, (n, _) in cur.items()}
    table = [f"{h['name']} ({h['id']}): kit {h['kitFrom']}, items {h['itemsFrom']}; off/on: "
             f"{[names[j] for j in h['off']]}" for h in hs]
    held = {j for h in hs for j in h["off"]}
    unheld = sorted(names[j] for j in cur if j not in held)
    pre = "Generated by push/skyglass_mark_fix.gen.py; do not hand-edit."
    write(NUM["unequip"], "skyglass_mark_fix_unequip", {
        "_note": (f"push/{NUM['unequip']}, step 1 of 3 (RUL-2026-11-02-101; law 18/60, hidden-jutsu save): every Skyglass "
                  f"mark and pool jutsu push/{NUM['edit']} edits comes off every holder. Kit otherwise unchanged; items "
                  "re-sent (law 70); rules untouched. Run 430 -> 431 -> 432 back to back, Monday to Thursday. " + pre),
        "_holders": table, "_notHeld": unheld,
        "items": [ai_edit(h, [j for j in h["kit"] if j not in h["off"]], "Skyglass marks off (law 18/60)") for h in hs]})
    write(NUM["edit"], "skyglass_mark_fix", {
        "_note": (f"push/{NUM['edit']}, step 2 of 3 (after push/{NUM['unequip']}; RUL-2026-11-02-101): effects only "
                  "(injectableInBattle false, law 20). Omen marks: the tile-art visual becomes an increaseregeneration "
                  "carrier (power 1, rounds 1, FRIENDLY), which the server keeps until the round after the cast ends, "
                  "so the mark stays up until the eruption; self markers unchanged. Pools (Eruption: Ebb / Flood "
                  "Scatter, Spreading Fire I-III): the art moves onto the lasting damage / drain (ENEMIES, unchanged), "
                  "the visual is dropped. The jutsu stay hidden. " + pre),
        "_changes": changes, "items": edits})
    write(NUM["reequip"], "skyglass_mark_fix_reequip", {
        "_note": (f"push/{NUM['reequip']}, step 3 of 3 (after push/{NUM['edit']}): every holder from push/{NUM['unequip']} "
                  "gets its exact current kit back (the newest run send carrying jutsus) and its items (newest run send "
                  "carrying items); rules untouched. " + pre),
        "_holders": table, "items": [ai_edit(h, h["kit"], "Skyglass marks back on (law 18/60)") for h in hs]})
    print(f"{len(hs)} holders; edited jutsu not held by any AI: {unheld}")


if __name__ == "__main__":
    main()
