"""Rebuild the curated tag snapshot _build/data.json (area, polarity, copy/mirror eligibility, live usage counts).

    python3 data.py TAGS_RAW_JSON USAGE_TABLE_MD [OUT_JSON]

TAGS_RAW_JSON is extract.py's --legacy-raw output. USAGE_TABLE_MD is a markdown table with rows
"| tag | jutsu count | pvp-legal count |" (the Nov 21 table lives in the project files, outside this repo).
OUT_JSON defaults to _build/data.json, the committed snapshot kb.py reads. Only rerun this to change the curated
fields or refresh usage counts; rerunning blanks the overlaps notes in OUT_JSON, which kb.py no longer reads.
"""
import json,os,re,sys
if len(sys.argv) < 3:
    sys.exit(__doc__)
RAW, USAGE = sys.argv[1], sys.argv[2]
OUT = sys.argv[3] if len(sys.argv) > 3 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")
raw=json.load(open(RAW))
bytype={v['type']:(k,v) for k,v in raw.items()}
# usage
use={}
for line in open(USAGE):
    m=re.match(r'\| (\w+) \| (\d+) \| (\d+) \|',line)
    if m: use[m.group(1)]=(int(m.group(2)),int(m.group(3)))

AREAS=[
 ("dmgnow","Damage now","#d1495b"),
 ("dmglater","Damage later","#e07a1f"),
 ("scaling","Damage scaling","#c9a227"),
 ("soak","Soak","#2a9d8f"),
 ("sendback","Send back","#8a5cc2"),
 ("heal","Healing","#3a9d4a"),
 ("remove","Remove","#5a6b7d"),
 ("take","Take","#b5487f"),
 ("protect","Protection","#2f6fbf"),
 ("deny","Deny actions","#a33b3b"),
 ("speed","Speed up","#1f9bb5"),
 ("position","Position","#7a7a2a"),
 ("fighters","Extra fighters","#6d4c9e"),
 ("pools","Pools and money","#8c6d3f"),
 ("escape","Escape","#4f7f6f"),
 ("aggro","AI aggro","#9b6b9e"),
 ("sage","Sage","#c2703d"),
 ("noncombat","Non-combat","#8d8d8d"),
]
A={}
def put(area,*tags):
    for t in tags: A[t]=area
put("dmgnow","damage","pierce","elementaldamage","onehitkill","weakness")
put("dmglater","wound","afterburn","poison","drain","diffuse","curse")
put("scaling","increasedamagegiven","decreasedamagegiven","increasedamagetaken","decreasedamagetaken","increasepotency","decreasepotency","increasestat","decreasestat","increasemastery","decreasemastery")
put("soak","shield","barrier","absorb","siphon","consume","finalstand")
put("sendback","reflect","parry","recoil","mirror")
put("heal","heal","lifesteal","vamp","increaseheal","decreaseheal","healprevent")
put("remove","clear","cleanse")
put("take","copy")
put("protect","buffprevent","debuffprevent","clearprevent","cleanseprevent","stunprevent","sealprevent","summonprevent","onehitkillprevent","robprevent","immunity")
put("deny","stun","seal","elementalseal","stealth","disarm","timecompression","increasepoolcost","increasecooldown")
put("speed","timedilation","decreasepoolcost","decreasecooldown","injectjutsus","increaserange")
put("position","move","moveprevent","redirection")
put("fighters","summon","clone")
put("pools","increasemaxpools","decreasemaxpools","rob")
put("escape","flee","fleeprevent")
put("aggro","increaseaggro","decreaseaggro")
put("sage","activatesagemode")
for t in bytype:
    if t not in A: A[t]="noncombat"

POS=set("absorb consume siphon debuffprevent increaseaggro decreaseaggro decreasedamagetaken decreasepoolcost heal increasedamagegiven increaseheal increasepotency increasemaxpools increasestat increasemastery increaserange decreasecooldown lifesteal move onehitkillprevent reflect parry curse robprevent sealprevent shield stealth stunprevent summon timedilation immunity".split())
NEG=set("afterburn buffprevent clear damage elementaldamage decreasedamagegiven decreaseheal decreasepotency decreasestat decreasemastery decreasemaxpools disarm drain elementalseal flee fleeprevent healprevent increasedamagetaken increasepoolcost increasecooldown moveprevent onehitkill pierce poison recoil redirection rob seal stun summonprevent timecompression weakness wound".split())
COPYABLE=["increasedamagegiven","decreasedamagetaken","lifesteal","absorb","reflect","shield","increaseheal","increasestat"]
MIRROR_EX=set("damage pierce clear buffprevent cleanseprevent moveprevent healprevent stun timecompression".split())
MIRRORABLE=[t for t in sorted(NEG) if t not in MIRROR_EX]
POTENCY=["damage","increasedamagegiven","decreasedamagegiven","increasedamagetaken","decreasedamagetaken","afterburn","lifesteal","reflect","parry","curse","increaseheal","heal","vamp","absorb","consume","siphon","shield","pierce","drain","poison"]

BUFFP="increasestat increasemastery increasedamagegiven decreasedamagetaken increaseheal increaserange decreasecooldown increasepotency increasemaxpools reflect curse siphon timedilation increaseaggro decreaseaggro copy".split()
DEBUFFP="decreasestat decreasemastery decreasedamagegiven increasedamagetaken decreaseheal increasecooldown decreasepotency decreasemaxpools recoil drain poison timecompression mirror".split()
PREVENTS={
 "buffprevent":BUFFP,"debuffprevent":DEBUFFP,
 "healprevent":["heal","lifesteal","absorb","vamp","curse"],
 "clearprevent":["clear"],"cleanseprevent":["cleanse"],"stunprevent":["stun"],
 "sealprevent":["seal"],"summonprevent":["summon"],"onehitkillprevent":["onehitkill"],
 "robprevent":["rob"],"fleeprevent":["flee"],"moveprevent":["move","redirection"],
}
PREVENT_TYPES="buffprevent clearprevent cleanseprevent debuffprevent disarm fleeprevent healprevent moveprevent onehitkillprevent robprevent sealprevent stunprevent summonprevent".split()

STAGE={}
for t in "stealth buffprevent cleanseprevent clearprevent debuffprevent fleeprevent healprevent moveprevent onehitkillprevent robprevent sealprevent stunprevent summonprevent disarm weakness".split(): STAGE[t]="s2"
for t in "elementalseal injectjutsus activatesagemode cleanse clear increaseaggro decreaseaggro increasepotency decreasepotency decreasepoolcost decreasestat decreasemastery increasepoolcost increasestat increasemastery".split(): STAGE[t]="s3"
for t in "barrier shield finalstand diffuse clone redirection damage flee heal onehitkill rob seal stun summon".split(): STAGE[t]="s4"
for t in "decreasedamagegiven decreasedamagetaken increasedamagegiven increasedamagetaken".split(): STAGE[t]="s7"
STAGE["pierce"]="s8"
for t in "lifesteal drain poison afterburn absorb recoil reflect parry wound decreaseheal increaseheal".split(): STAGE[t]="s9"
for t in "copy mirror".split(): STAGE[t]="s1"
for t in "timecompression timedilation move".split(): STAGE[t]="s10"
for t in "vamp curse consume siphon immunity increasemaxpools decreasemaxpools increaserange increasecooldown decreasecooldown".split(): STAGE[t]="s10"
STAGE["elementaldamage"]="s0"
for t in bytype:
    if A[t]=="noncombat": STAGE[t]="nc"
STAGE["visual"]="s10"

B={} # behaviour
def b(t,text): B[t]=text
b("damage","Hits the target for a formula amount: a baseline (max HP at the attacker's level divided by the base-hits setting) scaled by power and by an attack-vs-defence advantage built from the square roots of offence and the chosen generals, clamped to a min and max. Weakness multiplies the raw number. It then runs the full damage pipeline. With rounds above 0 it repeats as residual damage on the target's turn each round, multiplied by residualModifier.")
b("pierce","Same formula as damage, but resolved after the damage pipeline, so no damage increase, no damage reduction and no Curse bonus touches it. It destroys every shield on the target instead of being soaked, and Parry, Recoil and Afterburn ignore it. Lifesteal, Absorb and Reflect still read it.")
b("elementaldamage","An authoring shortcut. On cast it becomes an ordinary damage tag with one element: the caster's saved preferred element, else their basic innate element, else Fire. It counts as elemental for Elemental Seal.")
b("onehitkill","Rolls power% to set the target's HP to 0 outright. It skips shields, damage reduction and Final Stand. Onehitkillprevent blocks it. The HP removed counts as damage dealt.")
b("weakness","Lands on a roll of power%. While active, damage or pierce from the listed jutsu, items, elements or general types has its raw damage multiplied by dmgModifier. Only the biggest matching weakness counts. No prevent stops it.")
b("wound","When cast, it records the damage its caster dealt to the target in that action. Each later round it deals power% of that recorded hit again; ticking on its own, that damage skips shields. It's mirror-eligible.")
b("afterburn","A debuff on the holder. Every direct hit they take once it's live adds power% of that hit as extra damage, capped at 60% of the hit. Pierce doesn't trigger it, and no prevent check runs on it.")
b("poison","When the poisoned player acts, they take power% of the chakra plus stamina that action cost as damage. Debuffprevent blocks it.")
b("drain","Each round it removes a flat amount, or power% of the max, from the chosen pools (HP, chakra, stamina). Debuffprevent blocks it. When mirrored, its power is divided by the mirror's rounds.")
b("diffuse","The holder defers power% (up to 99%) of each incoming non-lethal hit and repays it over the next delayRounds (default 3). Damage reduction applies first; shields and Absorb only see the immediate part. Repayment survives expiry, skips defences and respects Final Stand. It can't be cleansed, prevented or copied.")
b("curse","The holder stores half of power% of the damage they deal and take. While active it adds damageBonusPercent to their raw damage (not to pierce) and switches off their own Lifesteal, Absorb and Vamp. When it expires naturally, it heals the stored amount, with heal modifiers applied, up to max HP. Clear or any other removal throws the store away. Healprevent on the holder blocks the payout, and Seal blocks it for a bloodline Curse. Buffprevent stops it landing.")
b("increasedamagegiven","Percentage: multiplies the holder's outgoing damage in the in-battle increase step (each one multiplies separately, so two +25% give ×1.5625). Static: adds a flat amount after the percentage steps. It's live from the round after it's cast. Elements can limit it. Buffprevent blocks it.")
b("decreasedamagegiven","Percentage: a sequential damage-reduction multiplier on the holder's outgoing damage. Static: a flat subtraction after the percentage steps. Total reduction can't push a hit below 10% of its post-system-DR value. Debuffprevent blocks it.")
b("increasedamagetaken","Multiplies damage the holder takes, in the same in-battle increase step as increasedamagegiven, with no cap. It's live from the round after it's cast. Debuffprevent blocks it.")
b("decreasedamagetaken","Damage reduction on hits the holder takes. Static values apply before percentage ones; the 90% reduction cap applies. Buffprevent blocks it.")
b("increasepotency","Raises the power of the selected tag type (or all 20 potency-eligible types) on the holder's later jutsu casts, flat or by percentage, optionally limited to elements. It's live from the round after it lands; potency set on the ground affects anyone casting from that tile. Buffprevent blocks it.")
b("decreasepotency","Lowers the power of the selected tags on the holder's later jutsu casts. It works the same way as increasepotency, and debuffprevent blocks it.")
b("increasestat","Raises offence and/or defence (direction) and the chosen generals, flat or as a % of the base stat, from the round after cast. Those stats feed the damage formula's advantage term. Buffprevent blocks it.")
b("decreasestat","Lowers offence, defence or generals the same way as increasestat. Debuffprevent blocks it.")
b("increasemastery","Raises the holder's mastery values for the chosen jutsu types, from the round after cast. Buffprevent blocks it.")
b("decreasemastery","Lowers the chosen jutsu-type masteries. Debuffprevent blocks it.")
b("shield","Rolls power% to appear, then becomes a separate HP bar worth its health field. Incoming damage drains shields before HP, except pierce (which destroys them), reflect and wound (which skip them). It's positive, so Clear removes it and Copy can take it.")
b("barrier","A ground object on a tile with its own HP (its level is the power). A single-target hit that passes through it loses absorbPercentage of its damage to the barrier, and an AoE hits a barrier standing on its tile. It breaks at 0 HP. It also stops Redirection from landing on its tile. Clear can't touch it.")
b("absorb","Converts power% (or a flat amount) of each hit the holder takes into HP, chakra or stamina, split across the chosen pools, capped at 60% of the hit. It reads the immediate part after Diffuse and is live from the round after cast. Healprevent blocks it, Curse disables it, and heal modifiers scale it.")
b("siphon","While active, a percentage of damage the holder takes after their existing shields becomes new stacking temporary shields once the hit resolves. It excludes self-damage and recoil, shares conversion and shield-HP caps with Consume, and is unaffected by heal modifiers. Buffprevent blocks it, and Clear removes it.")
b("consume","While active, a percentage of all damage the caster deals becomes stacking temporary shields on themselves (shieldRounds long). It shares caps with Siphon, and no prevent check runs on it.")
b("finalstand","Rolls power% to activate. While active, damage can't take the holder below 1 HP (One Hit Kill still can). A bloodline version re-arms itself. Neither Clear nor Cleanse can remove it.")
b("reflect","Returns power% of each hit the holder takes to the attacker, capped at 60% of the hit. Buffprevent blocks it, and Copy can take it.")
b("parry","Before shields and Absorb, redirects power% of incoming direct damage (damage tags only, not pierce) back to the attacker. Several parries stack up to 100%, and returned damage can't be parried again. Buffprevent can't stop it, but Clear removes it.")
b("recoil","A debuff on the holder. Power% of the damage they deal comes back to them. Pierce damage is exempt. Debuffprevent blocks it.")
b("mirror","Rolls power% to clone up to 4 of the caster's own active negative effects onto the target for the mirror's rounds. The caster keeps their copies. Order of preference: damage-taken up or damage-given down first, then afterburn, then poison or pool-cost, then wound, then anything else. Raw damage, pierce, clear, stun, time compression and four prevents are excluded, and so is anything from bloodline, gear or other passives. The target's debuffprevent blocks it.")
b("heal","Restores HP, chakra or stamina each tick: power×10 if static, or power% of the max pool if percentage. Healprevent blocks it. The healer's increaseheal and decreaseheal scale it. Clear removes a heal-over-time.")
b("lifesteal","The holder heals power% of the damage they deal (matched by generals and elements). Lifesteal and Vamp share one cap: 60% of the hit, Vamp first. Healprevent blocks it, Curse disables it, and Copy can take it.")
b("vamp","Lives on the jutsu itself: the caster instantly heals power% of the damage that jutsu dealt. Healprevent on the caster blocks it, and Curse disables it.")
b("increaseheal","Scales every heal the holder produces: Heal, Lifesteal, Vamp, Absorb and the Curse payout. Buffprevent blocks it, and Copy can take it.")
b("decreaseheal","Shrinks every heal the holder produces, the same way increaseheal grows it. Debuffprevent blocks it.")
b("healprevent","A prevent-type status. Once it lands, it blocks Heal, Lifesteal, Absorb, Vamp and the Curse payout on the holder.")
b("clear","Rolls power% each tick until it lands. Then it removes every positive effect on the target, plus positive ground effects on their tile, except those from bloodline, sage mode, gear, skills or other pre-battle sources. Clear is itself negative, so Cleanse removes a pending Clear. Clearprevent blocks it.")
b("cleanse","Rolls power% each tick until it lands. Then it removes every negative effect on the target, with the same persistent-source exceptions as Clear. Cleanseprevent blocks it.")
b("copy","The caster's own buffprevent can block it. Otherwise it rolls power% to clone the target's best positive effects onto the caster for the copy's rounds; the target keeps theirs. It holds 4 at most at once, per caster. Order of preference: damage-given up or damage-taken down, then lifesteal, then absorb or reflect, then shield, then increaseheal, then increasestat. Passive and gear sources can't be copied.")
for p,tg in PREVENTS.items():
    if p not in B: b(p,f"A prevent-type status. It rolls power% once to land and then blocks {', '.join(tg)} with certainty, but only effects cast in a later round. Effects already on the holder stay. Immunity can cancel it.")
B["buffprevent"]="A prevent-type status. It rolls power% once to land, then blocks with certainty every buff cast on the holder in a later round: stat, mastery, damage given up, damage taken down, heal up, range, cooldown down, potency up, max pools up, reflect, curse, siphon, time dilation, aggro, and the holder's own Copy. Buffs already on the holder stay. Parry, shield, absorb and lifesteal ignore it."
B["debuffprevent"]="A prevent-type status. It rolls power% once to land, then blocks with certainty debuffs cast on the holder in a later round: stat down, mastery down, damage given down, damage taken up, heal down, cooldown up, potency down, max pools down, recoil, drain, poison, time compression, and Mirror. Damage, wound, afterburn, stun and pool cost go through."
b("disarm","A prevent-type status. While active it hides the holder's weapon items and every jutsu that needs a weapon.")
b("immunity","While active, it cancels any new prevent-type status of one chosen kind (the blocks field) as it lands on the holder. It's positive, so Clear removes it.")
b("stun","Stunprevent can block it. Otherwise it rolls power% to land. While active, the holder has apReduction less AP to spend. Only the strongest stun counts, and that includes stun ground effects on their tile.")
b("seal","Sealprevent can block it. Otherwise it rolls power% to land. From the following round it switches off all of the holder's bloodline effects, including bloodline damage modifiers, bloodline potency and bloodline-gated payouts.")
b("elementalseal","Rolls power% to land. While active, the holder's 60-AP elemental jutsu are hidden: jutsu classed elemental, carrying elementaldamage, or carrying any non-None element. No prevent stops it.")
b("stealth","Rolls power% to land. While active, other players' INHERIT-target effects can't land on the holder. The holder can't use any jutsu or the basic attack, heal, clear, cleanse, stances or flee; they keep move, replacement and items. It's positive, so Clear removes it.")
b("timecompression","Makes the holder's actions cost 10 more AP (all jutsu, or only listed elements). Only one can be active at a time. Debuffprevent blocks it.")
b("increasepoolcost","Raises the chakra or stamina cost of the holder's actions. No prevent check runs on it. It feeds Poison, which reads the pool spent.")
b("increasecooldown","Lengthens the cooldown of the listed basic actions. Debuffprevent blocks it.")
b("timedilation","Makes the holder's actions cost 10 less AP. Only one can be active at a time. Buffprevent blocks it.")
b("decreasepoolcost","Lowers the chakra or stamina cost of the holder's actions.")
b("decreasecooldown","Shortens the cooldown of the listed basic actions. Buffprevent blocks it.")
b("injectjutsus","Temporarily adds the listed jutsu to the holder's action list while active. Neither Clear nor Cleanse can remove it.")
b("increaserange","Adds range to the listed basic actions. Buffprevent blocks it.")
b("move","Moves the caster to the chosen tile, which registers them with any ground effects there. Moveprevent blocks it.")
b("moveprevent","A prevent-type status. It hides basic move, the replacement technique and every jutsu with a move tag, and it blocks Redirection.")
b("redirection","Pulls the target toward the caster or pushes them away, by power hexes. It stops at the first open tile, before players or barriers. Moveprevent blocks it.")
b("summon","Spawns the chosen AI on the target tile with aiHp HP and stats scaled to power% of the summoner's total. It acts in the summoner's initiative slot, can be player-piloted, and leaves when its rounds end. Summonprevent hides summon jutsu.")
b("clone","Spawns an AI copy of the caster with stats × power%. The clone can't summon or clone, has no sage mode, and disappears when its rounds end.")
b("increasemaxpools","Raises maximum and current HP, chakra or stamina. Buffprevent blocks it.")
b("decreasemaxpools","Lowers maximum and current pools. Debuffprevent blocks it.")
b("rob","Only works in 1v1 player combat. Robprevent can block it. Otherwise it rolls power% to steal robPercentage% of the target's pocket ryo. If the thief flees, they drop the stolen ryo; if the victim flees, they get it back.")
b("flee","Rolls power% each tick to leave the battle. It's not allowed in dungeons. Fleeprevent blocks it.")
b("fleeprevent","A prevent-type status that blocks Flee.")
b("increaseaggro","AI targeting. ENMITY mode adds to current enmity once; GENERATION mode raises the enmity each hit generates. Buffprevent blocks it.")
b("decreaseaggro","The reverse of increaseaggro. It's classed positive, so Clear removes it, and buffprevent blocks it.")
b("activatesagemode","Enters the holder's equipped sage mode. Its buffs and exhaustion are persistent sources that Clear and Cleanse can't strip.")
b("visual","Cosmetic battlefield effect; no rules.")
NC={"increaseregeneration":"Raises out-of-combat regeneration.","decreasecookingtime":"Activity passive: shortens each meal cooking job.","decreasecraftingtime":"Activity passive: shortens crafting jobs.","decreasefarmingtime":"Activity passive: shortens crop growth.","decreasegatheringtime":"Activity passive: shortens gathering collection.","increasegatheringyield":"Activity passive: extra units per gathering drop.","increasehuntingyield":"Activity passive: extra units per hunting drop.","increasejutsuslots":"Item use: permanently adds jutsu slots.","marriageslotincrease":"Item use: adds marriage slots.","noncombatincreasereskins":"Item use: adds reskin slots.","noncombatconsumereward":"Item use: grants rewards.","noncombatgainskill":"Item use: unlocks a skill tree entry.","noncombatquest":"Item use: starts a quest.","repair":"Item use: repairs durability.","removebloodline":"Item use: removes bloodline.","rollbloodline":"Item use: random bloodline.","rollsagemode":"Item use: random sage mode.","unlockitemvariant":"Item use: unlocks an item variant.","unknown":"Placeholder for an unrecognised tag."}
for t,v in NC.items(): b(t,v)

E=[]
def e(s,t,k,note=""): E.append({"s":s,"t":t,"k":k,"n":note})
for p,tg in PREVENTS.items():
    for t in tg: e(p,t,"prevents")
e("summonprevent","clone","prevents","no: clone ignores it") if False else None
for p in PREVENT_TYPES: e("immunity",p,"counters","cancels a new one of the chosen kind")
for t in sorted(POS): e("clear",t,"removes")
for t in sorted(NEG): e("cleanse",t,"removes")
for t in COPYABLE: e("copy",t,"transfers","clones to caster")
for t in MIRRORABLE: e("mirror",t,"transfers","clones caster's own onto target")
for t in POTENCY:
    e("increasepotency",t,"boosts","raises its power on later casts")
    e("decreasepotency",t,"weakens","lowers its power on later casts")
# damage pipeline
e("increasedamagegiven","damage","boosts","× in-battle increase step")
e("increasedamagetaken","damage","boosts","× in-battle increase step")
e("decreasedamagegiven","damage","weakens","sequential DR")
e("decreasedamagetaken","damage","weakens","sequential DR")
e("weakness","damage","boosts","raw × dmgModifier")
e("weakness","pierce","boosts","raw × dmgModifier")
e("increasestat","damage","boosts","advantage term")
e("decreasestat","damage","weakens","advantage term")
e("curse","damage","boosts","raw × damage bonus")
e("barrier","damage","counters","absorbs part of hits passing through")
for t in ["increasedamagegiven","increasedamagetaken","decreasedamagegiven","decreasedamagetaken","curse"]:
    e("pierce",t,"bypasses","pierce skips the damage pipeline")
for t in ["shield"]: e("pierce",t,"bypasses","destroys all shields")
for t in ["parry","recoil","afterburn"]: e("pierce",t,"bypasses","not triggered by pierce")
e("onehitkill","finalstand","bypasses","sets HP to 0 directly")
e("onehitkill","shield","bypasses","sets HP to 0 directly")
e("wound","shield","bypasses","wound damage skips shields")
# defenders vs damage
for t,n in [("shield","soaks before HP"),("absorb","converts part to pools"),("diffuse","defers part"),("finalstand","floors HP at 1"),("parry","sends part back first"),("reflect","sends part back"),("siphon","turns part into shields")]:
    e(t,"damage","counters",n)
# damage feeds
for t,n in [("wound","records the hit"),("lifesteal","heals from damage dealt"),("vamp","heals from this jutsu's damage"),("consume","shields from damage dealt"),("afterburn","adds % of hits taken"),("recoil","returns % to dealer"),("curse","stores half %")]:
    e("damage",t,"feeds",n)
e("increasepoolcost","poison","boosts","bigger pool spend, bigger poison")
e("decreasepoolcost","poison","weakens","smaller pool spend")
for t in ["lifesteal","absorb","vamp"]: e("curse",t,"disables","off while Curse is on the holder")
for t in ["heal","lifesteal","vamp","absorb","curse"]:
    e("increaseheal",t,"boosts","scales the holder's healing")
    e("decreaseheal",t,"weakens","scales the holder's healing")
e("consume","siphon","shares","shared conversion and shield caps")
e("siphon","shield","feeds","makes temporary shields")
e("consume","shield","feeds","makes temporary shields")
e("seal","finalstand","disables","bloodline-sourced copies only")
e("seal","curse","disables","blocks bloodline payout")
e("stealth","damage","counters","can't be targeted by others")
e("stealth","copy","counters","can't be targeted by others")
e("timecompression","timedilation","counters","AP +10 vs −10")
e("increasepoolcost","decreasepoolcost","counters","opposite pool cost")
e("increasecooldown","decreasecooldown","counters","opposite cooldown")
e("barrier","redirection","counters","blocks landing tile")
e("moveprevent","move","prevents") if False else None
e("redirection","barrier","feeds","") if False else None
e("diffuse","absorb","feeds","absorb reads immediate part")
e("elementalseal","elementaldamage","prevents","hides 60-AP elemental jutsu")
e("elementaldamage","damage","feeds","becomes a damage tag")
e("cleanse","clear","removes","Clear is negative") if False else None
e("summon","clone","shares","") if False else None
e("heal","drain","counters","") if False else None
e("rob","flee","feeds","fleeing drops/returns stolen ryo")

nodes=[]
for t,(k,v) in sorted(bytype.items()):
    u=use.get(t,(0,0))
    pol = "positive" if t in POS else "negative" if t in NEG else "neutral"
    pb=[p for p,tg in PREVENTS.items() if t in tg]
    if t=="copy": pb=["buffprevent (on the caster)"]
    fields=[f for f in v['fields'] if f not in ('calculation','power','powerPerLevel','target','direction','rounds')]
    grp=[s for s in v['spreads'] if s not in('BaseAttributes','PowerAttributes')]
    extra={"IncludeGeneralsAndElements":["generalTypes","elements"],"DamageModifierAttributes":["calculation","elements"],"HealModifierAttributes":["calculation"],"PotencyAttributes":["affectedTag","affectedElements","calculation","rounds (1–100)"],"PoolCostAttributes":["poolsAffected","calculation","rounds (2–20)"],"MaxPoolsAttributes":["poolsAffected","calculation"],"StatModifierAttributes":["generalTypes","elements","calculation","direction"],"AggroAttributes":["aggroMode","calculation","target"],"TimeShiftAttributes":["generalTypes","elements","calculation","rounds (1–20)"],"PoolAttributes":["poolsAffected"],"ActivityBonusAttributes":["power (percent)"],"PercentageCalculation":["calculation"],"rewardFields":["rewards"]}
    for g in grp: fields+=extra.get(g,[])
    if v['helper']=="basicActionTag": fields+=["actionsAffected"]
    if v['helper']=="masteryModifierTag": fields+=["masteryTypes"]
    if t in ("damage","pierce","elementaldamage"): fields=list(dict.fromkeys(fields+["generalTypes","elements"]))
    if t=="pierce" or t=="elementaldamage":
        k2,v2=bytype["damage"]; fields=list(dict.fromkeys(fields+[f for f in v2['fields'] if f in("residualModifier","dmgModifier")]))
    calc=re.search(r'calculation:\s*z\.(?:enum\(\[([^\]]*)\]\)|literal\("(\w+)"\))',v['block'])
    calcs=None
    if calc: calcs=(calc.group(1) or calc.group(2)).replace('"','').replace(' ','')
    elif "PercentageCalculation" in v['spreads'] or "DamageModifierAttributes" in v['spreads'] or "HealModifierAttributes" in v['spreads']: calcs="static,percentage"
    fields=list(dict.fromkeys(fields))
    nodes.append({"id":t,"area":A[t],"desc":v['desc'],"beh":B.get(t,""),"fields":fields,"calc":calcs,"stage":STAGE.get(t,"s10"),"pol":pol,
      "copy":t in COPYABLE,"mirror":t in MIRRORABLE,"potency":t in POTENCY,"pb":pb,"use":u[0],"pvp":u[1],"schema":k,"prevtype":t in PREVENT_TYPES})
ids={n['id'] for n in nodes}
for x in E: assert x['s'] in ids and x['t'] in ids,(x)
# dedupe
seen=set();E2=[]
for x in E:
    key=(x['s'],x['t'],x['k'])
    if key in seen: continue
    seen.add(key);E2.append(x)
json.dump({"areas":[{"id":a,"name":n,"color":c} for a,n,c in AREAS],"nodes":nodes,"edges":E2},open(OUT,'w'))
print(len(nodes),len(E2))
from collections import Counter
print(Counter(x['k'] for x in E2))
print([n['id'] for n in nodes if not n['beh']])
print(Counter(n['area'] for n in nodes))

# --- overlaps (design judgement), added after the first build ---
OV=[("reflect","parry"),("lifesteal","vamp"),("consume","siphon"),("shield","barrier"),("clear","cleanse"),("copy","mirror"),("stun","timecompression"),("timecompression","increasepoolcost"),("buffprevent","clear"),("debuffprevent","cleanse"),("afterburn","increasedamagetaken"),("weakness","increasedamagetaken"),("recoil","reflect"),("wound","drain"),("drain","poison"),("curse","diffuse"),("increasedamagegiven","increasedamagetaken"),("decreasedamagegiven","decreasedamagetaken"),("stealth","elementalseal"),("summon","clone"),("heal","curse"),("finalstand","diffuse")]
# notes for each pair are in ../interactions.json (kind: overlaps)
_d=json.load(open(OUT))
if not any(e['k']=='overlaps' for e in _d['edges']):
    _d['edges']+=[{"s":a,"t":b,"k":"overlaps","n":""} for a,b in OV]
    json.dump(_d,open(OUT,'w'))
