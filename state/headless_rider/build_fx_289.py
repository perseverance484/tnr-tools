"""push/289: Hellfire Harvest + Aura of Despair visuals (assets from push/288), approved Aura text, re-equip the kit."""
import copy, json
R = "/home/claude/tnr-tools"
res = json.load(open(f"{R}/harvests/inbox/tnr_results_1793062957158.json"))
A = {e["srcId"]: e["id"] for e in res["entries"] if e["entity"] == "asset"}
rider = json.load(open(f"{R}/state/headless_rider/rider_getAi_push262.json"))
kit = [j["jutsuId"] for j in rider["jutsus"]]                     # the seven, Aura included
aura = next(j["jutsu"] for j in rider["jutsus"] if j["jutsuId"] == "N8V10pCnF7sEdrRs-mIdG")
hh = json.load(open(f"{R}/archive/spent-manifests/push-2026-10-25/287_hellfire_harvest_damage_25.json"))["items"][0]["data"]
FIRE_SFX = "9-b8hbTXA019dgn8yyr3j"
BLANK = {"staticAssetPath": "", "staticAnimation": "", "appearAnimation": "", "disappearAnimation": "",
         "appearSfx": "", "disappearSfx": ""}

hhd = copy.deepcopy(hh)
dmg, rec, heal = hhd["effects"]
assert (dmg["type"], rec["type"], heal["type"]) == ("damage", "recoil", "decreaseheal")
dmg.update(BLANK, appearAnimation=A["hrh_hh_appear"], appearSfx=FIRE_SFX)   # the slash wave, once per tile
rec.update(BLANK, staticAssetPath=A["hrh_domain"])                           # the pumpkin domain, 3 rounds
heal.update(BLANK)                                                           # no second copy of anything

eff = copy.deepcopy(aura["effects"])
assert eff[0]["type"] == "increasepoolcost"
for e in eff[1:]:                     # legacy key, absent from the current schema for these tags (the server strips it)
    assert e["type"] in ("decreasedamagetaken", "increasedamagetaken")
    e.pop("statTypes", None)
eff[0].update(appearAnimation=A["hrh_ad_appear"], staticAnimation=A["hrh_ad_loop"],
              disappearAnimation=A["hrh_ad_disappear"], staticAssetPath=A["hrh_mist"], appearSfx="")
items = [
    {"entity": "jutsu", "slot": "convert", "targetId": "XVJb8MfFvIKe4GOgBaqXO", "name": "Hellfire Harvest: FX",
     "data": hhd},
    {"entity": "jutsu", "slot": "convert", "targetId": "N8V10pCnF7sEdrRs-mIdG", "name": "Aura of Despair: FX + text",
     "data": {"description": "The Rider raises his lantern and its dead light spills across the ground. Those it "
                             "touches feel their strength drain away, and every blow lands harder.",
              "battleDescription": "%user raises a guttering lantern and dead light spills across the ground around %target.",
              "effects": eff, "injectableInBattle": False}},
    {"entity": "ai", "slot": "edit", "targetId": rider["userId"],
     "name": "Headless Rider: re-equip Hellfire Harvest + Aura of Despair",
     "data": {"jutsus": kit + ["XVJb8MfFvIKe4GOgBaqXO"], "items": []}},
]
m = {"_note": "STEP 2 of 2 (after 288). Hellfire Harvest: damage effect gets the new appear animation (the low hellfire "
              "slash) + FireSFX; recoil effect carries the pumpkin domain as its 3-round ground still; heal cut has no "
              "visuals (Shadow field and Black Thorn Rose removed). Aura of Despair: the increasepoolcost effect gets the "
              "new appear / loop / disappear animations and the despair mist still, Clear SFX removed; approved "
              "description and battle line (RUL-2026-10-26-009). Numbers, targeting and the other effects unchanged (their legacy statTypes key is dropped: not in the current schema for decrease/increasedamagetaken, so the server strips it anyway). "
              "Then re-equips the full kit: push/262's seven (Aura included) + Hellfire Harvest, items []. Rules untouched. "
              "Asset ids from the push/288 results.",
     "items": items}
json.dump(m, open(f"{R}/push/289_headless_rider_fx_jutsu.json", "w"), indent=1)
print(json.dumps(A, indent=1))
