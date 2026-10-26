import json, sys
sys.path.insert(0, "/home/claude/tnr-tools/skills/building-tnr-content/scripts")
from factory import Factory
f = Factory()
a = json.load(open("/home/claude/tnr-tools/state/headless_rider/rider_getAi_push262.json"))
AID = a["userId"]
J = {j["jutsu"]["name"]: j["jutsuId"] for j in a["jutsus"]}
R = {j["jutsu"]["name"]: j["jutsu"]["range"] for j in a["jutsus"]}
kit = [j["jutsuId"] for j in a["jutsus"]]
wail = [x["jutsu"] for x in a["jutsus"] if x["jutsu"]["name"] == "Wail of Despair"][0]
NEW = sys.argv[1] if len(sys.argv) > 1 else None  # live id of Hellfire Harvest once created
NULLS = ["requiredPetSpeciesId","reskinParentJutsuId","bloodlineReskinId","parentJutsuId","coordinateTargeting","methodSize",
 "requiredNinjutsuMastery","requiredGenjutsuMastery","requiredTaijutsuMastery","requiredBukijutsuMastery","requiredBloodlineMastery",
 "requiredSageMastery","requiredStrength","requiredSpeed","requiredIntelligence","requiredWillpower","requiredSkillId","requiredBloodlineItemId"]
dmg = f.tag("damage", power=70, statTypes=["None"], generalTypes=["Highest"], elements=["Fire"])
jdata = {k: wail.get(k) for k in NULLS}
jdata.update({
    "name": "Hellfire Harvest", "jutsuType": "AI", "jutsuRank": "D", "requiredRank": "STUDENT", "requiredLevel": 1,
    "description": "The rider drags his burning scythe in a wide circle and the whole field catches. Every strike made inside the flames burns the striker, and wounds in the fire will not close.",
    "battleDescription": "%user drags a burning scythe across the field, setting every enemy ablaze with Hellfire Harvest",
    "target": "OPPONENT", "method": "ALL", "range": 5, "cooldown": 6, "actionCostPerc": 60,
    "chakraCost": 50, "staminaCost": 50, "healthCost": 0, "extraBaseCost": 0,
    "chakraCostReducePerLvl": 0, "staminaCostReducePerLvl": 0, "healthCostReducePerLvl": 0,
    "jutsuWeapon": "NONE", "statClassification": "None", "elementClassification": "None",
    "battleUsageType": "BOTH", "bloodlineId": "", "villageId": "", "image": wail["image"],
    "hidden": True, "injectableInBattle": False,
    "effects": [dmg, f.tag("recoil", power=40, rounds=3), f.tag("decreaseheal", power=60, rounds=3)],
})
jentry = f.entry("jutsu", "create", name="Hellfire Harvest", srcId="hellfire_harvest", data=jdata)
T = "CLOSEST_OPPONENT"
gate = lambda n: f.condition("distance_lower_than", value=R[n] + 1, target=T)
use = lambda n, t=T: f.action("use_specific_jutsu", jutsuId=J[n], target=t)
rules = [
    f.rule(action=use("Candle Lit Aura", "SELF")),
    f.rule(action=f.action("use_specific_jutsu", jutsuId=NEW, target=T)),
    f.rule(gate("Aura of Despair"), action=use("Aura of Despair")),
    f.rule(gate("Horseman's Charge"), action=use("Horseman's Charge")),
    f.rule(f.condition("target_has_effect", effectType="increasedamagegiven", threshold=0, target=T),
           gate("Essence Eater"), action=use("Essence Eater")),
    f.rule(gate("Unholy Pumpkin Patch"), action=use("Unholy Pumpkin Patch")),
    f.rule(gate("Scything Rend"), action=use("Scything Rend")),
    f.rule(gate("Essence Eater"), action=use("Essence Eater")),
    f.rule(gate("Wail of Despair"), action=use("Wail of Despair")),
    f.rule(action=f.action("move_towards_opponent", target=T)),
]
if NEW is None:
    m = {"_note": "Creates Hellfire Harvest, the Headless Rider's new signature jutsu (director spec 2026-10-26), hidden: method ALL on every "
                  "opponent, damage 70 (Fire, the rider's element), recoil 40% for 3 rounds, heal cut (decreaseheal) 60% for 3 rounds, "
                  "60 AP. PLACEHOLDERS: cooldown 6, heal-cut duration 3 (matches recoil), icon reuses Wail of Despair's image until art "
                  "exists. Create only: equipping it on the rider (eaMN5CfciNlxfezSKemJ6) and the rules follow as a separate edit with "
                  "this jutsu's live id, because an @jutsu ref in an AI jutsus array is refused by validate (law 17).",
         **f.manifest([jentry])}
    json.dump(m, open("/home/claude/tnr-tools/push/279_hellfire_harvest.json", "w"), indent=1)
    raise SystemExit
items = [
    {"entity": "ai", "slot": "edit", "targetId": AID, "name": "Headless Rider: equip Hellfire Harvest",
     "data": {"jutsus": kit + [NEW], "items": []}},
    {"entity": "aiProfile", "slot": "edit", "targetId": AID, "name": "Headless Rider: rules with Hellfire Harvest",
     "data": {"includeDefaultRules": False, "rules": rules}}]
m = {"_note": "Headless Rider (eaMN5CfciNlxfezSKemJ6): new signature jutsu Hellfire Harvest, director spec 2026-10-26: "
              "method ALL on every opponent, damage 70 (Fire, the rider's element), recoil 40% for 3 rounds, heal cut "
              "(decreaseheal) 60% for 3 rounds; 60 AP. PLACEHOLDERS: cooldown 6, heal-cut duration 3 (matches recoil), "
              "icon reuses Wail of Despair's image until art exists. Created hidden, then equipped by re-sending the "
              "kit (7 as read by push/262, items [] unchanged) plus the new id; updateAi inserts it equipped. Rules are "
              "the push/263 set with Hellfire Harvest as rule 2, ungated because ALL-method jutsu take no distance gate "
              "(law 40). Hellfire Harvest id from the push/279 results.",
     **f.manifest(items)}
json.dump(m, open("/home/claude/tnr-tools/push/280_headless_rider_equip_hellfire.json", "w"), indent=1)
