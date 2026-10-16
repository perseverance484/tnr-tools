#!/usr/bin/env python3
"""Author-side generator for design/regulars.json (16 NEW regular encounters).

Kept as code so rule gates come from the pool's own ranges (range+1, law 40) instead of hand
arithmetic. Kits are shared-pool picks only (references/ai.md: per-event jutsu minting retired);
commanders' signature B-codes are avoided. Accepted with the stat ladder by RUL-2026-10-16-011.
    python3 tools/gen_regulars.py [--check]
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, ".."))
REPO = os.path.abspath(os.path.join(ROOT, "../.."))
POOL = json.load(open(os.path.join(REPO, "skills/building-tnr-content/data/32b_DATA_pool.json")))["records"]
OUT = os.path.join(ROOT, "design", "regulars.json")

# Candidate multipliers per division (escalating attrition); REG4 is the optional elite.
TIER = {2: (1.5, 1.0), 3: (1.75, 1.25), 4: (2.0, 1.5), 5: (2.25, 1.75)}
ELITE = 0.25
RATIOS = {
 "Bukijutsu": {"bukijutsuOffence": 6, "taijutsuOffence": 2, "ninjutsuOffence": 1, "genjutsuOffence": 1, "bukijutsuDefence": 3, "taijutsuDefence": 3, "ninjutsuDefence": 2, "genjutsuDefence": 2, "strength": 3, "speed": 4, "intelligence": 1, "willpower": 2},
 "Taijutsu": {"taijutsuOffence": 6, "bukijutsuOffence": 2, "ninjutsuOffence": 1, "genjutsuOffence": 1, "taijutsuDefence": 3, "bukijutsuDefence": 3, "ninjutsuDefence": 2, "genjutsuDefence": 2, "strength": 4, "speed": 3, "intelligence": 1, "willpower": 2},
 "Ninjutsu": {"ninjutsuOffence": 6, "genjutsuOffence": 2, "taijutsuOffence": 1, "bukijutsuOffence": 1, "ninjutsuDefence": 3, "genjutsuDefence": 3, "taijutsuDefence": 2, "bukijutsuDefence": 2, "strength": 1, "speed": 2, "intelligence": 4, "willpower": 3},
 "Genjutsu": {"genjutsuOffence": 6, "ninjutsuOffence": 2, "taijutsuOffence": 1, "bukijutsuOffence": 1, "genjutsuDefence": 3, "ninjutsuDefence": 3, "taijutsuDefence": 2, "bukijutsuDefence": 2, "strength": 1, "speed": 2, "intelligence": 3, "willpower": 4},
}
GEN = {"Bukijutsu": ["Strength", "Speed"], "Taijutsu": ["Strength", "Speed"], "Ninjutsu": ["Intelligence", "Willpower"], "Genjutsu": ["Intelligence", "Willpower"]}

def gate(code):
    t = POOL[code]["target"]
    return None if t in ("self", "ground") else POOL[code]["range"] + 1

def attack(code):
    return {"if": [["dist<=", gate(code)]], "do": ["jutsu", code, "CLOSEST_OPPONENT"], "src": f"{POOL[code]['name']} (range {POOL[code]['range']}, gate +1)"}

def selfcast(code, cond=None, why=""):
    return {"if": cond or [], "do": ["jutsu", code, "SELF"], "src": f"{POOL[code]['name']} {why}".strip()}

U = []
def unit(slot, key, name, title, element, stat, kit, rules, role, tactical, look):
    d = int(slot[1]); reg4 = slot.endswith("REG4")
    s, p = TIER[d]
    U.append({"key": key, "slot": slot, "name": name, "title": title, "division": d,
      "role": "Elite PvE Enemy" if reg4 else "Standard PvE Enemy", "kit": kit,
      "items": [], "innate": [],
      "candidate": {"level": 100, "rank": "JONIN", "statsMultiplier": round(s + (ELITE if reg4 else 0), 2), "poolsMultiplier": round(p + (ELITE if reg4 else 0), 2),
                    "regeneration": 40, "element": element, "preferredStat": stat, "generals": GEN[stat], "ratio": RATIOS[stat]},
      "rules": rules + [{"if": [["dist>=", 3]], "do": ["move"], "src": "close distance (gated so end_turn stays reachable)"}, {"if": [], "do": ["end"], "src": "safe end-turn (includeDefaultRules:false)"}],
      "combatRole": role, "tacticalRead": tactical, "look": look, "status": "ACCEPTED — RUL-2026-10-16-011 (identity, kit, rules, stat tier); username live-collision check pending"})

# ---------- Division I — Experimental Armory (D2): weapon trials, the first sign the base is not empty
unit("D2.REG1", "proving_proctor", "Bastion Proving Proctor", "the Silent Examiner", "None", "Bukijutsu",
 ["S04", "S06", "A1", "B38", "S40"],
 [selfcast("B38", [["dist<=", 6]], "before engaging"), attack("S04"), attack("A1"), attack("S06"), attack("S40")],
 "Opening skirmisher. Marks the target with Opening Strike, then trades evenly; teaches that the Armory still runs drills.",
 "A fair first test: steady damage, no control. Heal through the 15% vulnerability window and keep pressure on.",
 "Reconstructed armory proctor in faded Skyglass grey drill uniform, chakra-glow seams, clipboard of stamped weapon trials, dual practice blades")
unit("D2.REG2", "ordnance_quartermaster", "Ordnance Quartermaster", "Keeper of the Live Rounds", "Fire", "Ninjutsu",
 ["EF03", "S30", "EF01", "S27", "EW03"],
 [selfcast("EW03", [["dist<=", 6]], "brace before trading"), attack("EF03"), attack("S30"), attack("S27"), attack("EF01")],
 "Attrition caster: stacks Afterburn and trims outgoing damage.",
 "Afterburn adds up across the run; Cleanse or burst the Quartermaster before the burns stack.",
 "Quartermaster in scorched apron over Skyglass officer coat, ammunition satchels of glowing sealed tags, soot-darkened gloves")
unit("D2.REG3", "prototype_lancer", "Prototype Lancer Unit", "Serial Zero-Three", "Lightning", "Bukijutsu",
 ["EL04", "EL01", "S08", "B39", "S43"],
 [selfcast("B39", [["hp<", 50]], "shield once hurt"), {"if": [["target", "shield", 1], ["dist<=", gate("EL04")]], "do": ["jutsu", "EL04", "CLOSEST_OPPONENT"], "src": "Ion Lance pierces player shields"},
  attack("S08"), attack("EL01"), attack("S43"), attack("EL04")],
 "Anti-defence test unit: pierces shields and slips in a light stun chance.",
 "Shields buy little here. Drop it before its own Light Barrier comes up under half health.",
 "Half-built lightning-lance automaton fused with a reconstructed test pilot, exposed capacitor coils, armory serial plate 03")
unit("D2.REG4", "calibration_duelist", "Calibration Duelist", "Master's Last Apprentice", "Wind", "Taijutsu",
 ["EA02", "A2", "S33", "B19", "S35"],
 [selfcast("S35", [["hp<", 40]], "emergency"), selfcast("B19", [["dist<=", 4]], "when engaged"), attack("EA02"), attack("S33"), attack("A2")],
 "Optional elite (Protocol access): a close-quarters duelist who calibrates Master of Arms' technique.",
 "Beating the Duelist unlocks Medical or Combat Protocol. Bring burst for its Warrior's Poise window.",
 "Duelist in calibration harness with chakra-measuring rings on both arms, wind-swept practice sword, apprentice insignia of the Armory")
# ---------- Division II — Skyglass Research (D3): reconstruction revealed
unit("D3.REG1", "archive_keeper", "Skyglass Archive Keeper", "Custodian of Impressions", "Water", "Genjutsu",
 ["S28", "S32", "EW01", "S36", "S41"],
 [selfcast("S36", [["round<", 2]], "opening ward"), attack("S32"), attack("S28"), attack("EW01"), attack("S41")],
 "Debuff archivist: Cleanse Prevent and stat reduction, warded against counter-debuffs.",
 "Its Lingering Strike stops you cleansing for two rounds; time your Cleanse after it lands, not before.",
 "Archivist impression rendered in pale blue chakra light, holding a Skyglass core ledger, translucent where the reconstruction is incomplete")
unit("D3.REG2", "containment_warden", "Impression Containment Warden", "Seal of the Vat Halls", "Water", "Ninjutsu",
 ["EW02", "B36", "EW03", "S29", "EW01"],
 [selfcast("EW03", [["dist<=", 6]], "brace"), attack("EW02"), attack("B36"), attack("S29"), attack("EW01")],
 "Shielded jailer: shields itself on its breaker strike and poisons over time.",
 "Pierce or Clear its shields; Withering Weave cuts your healing, so do not rely on it mid-fight.",
 "Warden in sealed containment suit with water-filled observation visor, chain of reconstruction vat keys, Skyglass research crest")
unit("D3.REG3", "unstable_echo", "Unstable Echo Subject", "Failed Iteration Nine", "Shadow", "Genjutsu",
 ["S29", "B36", "S33", "B21", "S35"],
 [selfcast("S35", [["hp<", 40]], "self-repair"), selfcast("B21", [["round<", 3]], "early absorb shell"), attack("B36"), attack("S29"), attack("S33")],
 "A flawed reconstruction: absorbs early damage and repairs itself when broken.",
 "Hit hard after its Hushed Hours shell expires; heal-prevent shuts down its self-repair.",
 "Flickering failed reconstruction, body glitching between two silhouettes, shadow chakra leaking from seams, research tag 'IX'")
unit("D3.REG4", "failed_prototype", "Failed Reconstruction Prototype", "The One They Kept", "Earth", "Taijutsu",
 ["A3", "S29", "B36", "B24", "S44"],
 [selfcast("B24", [["hp<", 35]], "escape stealth on a health trigger (law 62)"), attack("A3"), attack("B36"), attack("S29"), attack("S44")],
 "Optional elite: a heavy hitter that vanishes once to recover and come back stronger.",
 "When it drops below about a third it slips into stealth and heals; save a finisher for when it reappears.",
 "Hulking earth-bound prototype, crystal growths over a half-formed body, reconstruction rig still bolted to its back")
# ---------- Division III — High Command (D4): officers still giving orders
unit("D4.REG1", "signal_adjutant", "Command Signal Adjutant", "Voice of the Relay", "Wind", "Ninjutsu",
 ["S27", "S08", "EA01", "EA03", "S42"],
 [selfcast("EA03", [["dist<=", 6]], "focus"), attack("S27"), attack("S08"), attack("EA01"), attack("S42")],
 "Relay officer: weakens outgoing damage and fires fast wind bolts.",
 "Low durability for a Division III foe; close quickly and burst.",
 "Signal officer with relay headset and wind-banner semaphore flags, Skyglass High Command rank stripes")
unit("D4.REG2", "staff_tactician", "High Command Staff Tactician", "Planner of the Second", "None", "Genjutsu",
 ["S32", "S28", "S27", "S36", "EA01"],
 [selfcast("S36", [["round<", 2]], "ward"), attack("S32"), attack("S28"), attack("S27"), attack("EA01")],
 "Staff planner: layers Cleanse Prevent, stat and damage reductions under a debuff ward.",
 "Its ward blocks your debuffs early; spend those turns on damage instead.",
 "Staff tactician with campaign maps pinned to a field desk, quill of chakra ink, aide's cord of the Grand Marshal")
unit("D4.REG3", "honor_guard_commandant", "Honor Guard Commandant", "Shield of the Second", "Earth", "Taijutsu",
 ["EE02", "EE01", "B19", "EE03", "S44"],
 [selfcast("B19", [["dist<=", 4]], "when engaged"), selfcast("EE03", [["hp<", 60]], "stonewall"), attack("EE02"), attack("S44"), attack("EE01")],
 "Bulwark officer: pins the target in place with Bedrock Breaker and hits hard.",
 "Bedrock Breaker roots and briefly stuns; do not stand in melee if you rely on repositioning.",
 "Heavy honor-guard commandant in ceremonial stone-plated armour, tower shield bearing the High Command seal")
unit("D4.REG4", "aide_de_camp", "Strategist's Aide-de-Camp", "Last Courier of the Second", "Lightning", "Ninjutsu",
 ["S33", "EL02", "EL04", "B21", "S43"],
 [selfcast("B21", [["round<", 3]], "early absorb"), {"if": [["target", "shield", 1], ["dist<=", gate("EL04")]], "do": ["jutsu", "EL04", "CLOSEST_OPPONENT"], "src": "Ion Lance vs shields"},
  attack("S33"), attack("EL02"), attack("S43")],
 "Optional elite: reflective lightning courier carrying the Grand Marshal's orders.",
 "Storm Breaker Volt reflects damage for two rounds; switch to sustain while it is up.",
 "Courier officer with sealed dispatch tubes crackling with lightning, reflective lacquered armour, aide's sash")
# ---------- Division IV — Command Sanctum (D5): the inner guard
unit("D5.REG1", "sanctum_vanguard", "Sanctum Vanguard", "First Line of the Sanctum", "Fire", "Taijutsu",
 ["EF02", "B01", "EF01", "B19", "S35"],
 [selfcast("S35", [["hp<", 40]], "steady"), selfcast("B19", [["dist<=", 4]], "when engaged"), attack("B01"), attack("EF02"), attack("EF01")],
 "Heavy vanguard: Cataclysm Fist bursts and wounding blows.",
 "The hardest opening fight of the run; arrive with pools ready or expect to use the recovery checkpoint.",
 "Vanguard in obsidian-and-ember Sanctum armour, gauntlets glowing with fire chakra, banner of the Supreme Command")
unit("D5.REG2", "directive_herald", "Directive Herald", "Mouth of the Orders", "Lightning", "Genjutsu",
 ["S32", "S28", "EL03", "B38", "S44"],
 [selfcast("B38", [["dist<=", 6]], "before engaging"), attack("S32"), attack("EL03"), attack("S28"), attack("S44")],
 "Herald who reads out each new directive: stuns and locks Cleanse.",
 "Static Jolt stuns for a round; Stun Prevent pays off here.",
 "Herald in long ceremonial robes reading from a glowing directive scroll that rewrites itself, lightning-lit eyes")
unit("D5.REG3", "last_watch_executor", "Last Watch Executor", "Enforcer of Final Orders", "Wind", "Bukijutsu",
 ["B02", "EA02", "S33", "B21", "S43"],
 [selfcast("B21", [["round<", 3]], "early absorb"), attack("B02"), attack("EA02"), attack("S33"), attack("S43")],
 "Executor with a heavy wave strike and redirection to pull fleeing targets back.",
 "Its Annihilating Wave is a big swing on an 8-round cooldown; defend that turn, punish the next.",
 "Executor in tattered Sanctum night-watch cloak, twin wind glaives, mask stamped with an unreadable new order")
unit("D5.REG4", "order_bearer", "Order-Bearer of the Sanctum", "Keeper of the Unsigned Seal", "Water", "Ninjutsu",
 ["EL04", "B01", "EW02", "B19", "S35"],
 [selfcast("S35", [["hp<", 40]], "steady"), selfcast("B19", [["dist<=", 4]], "when engaged"),
  {"if": [["target", "shield", 1], ["dist<=", gate("EL04")]], "do": ["jutsu", "EL04", "CLOSEST_OPPONENT"], "src": "Ion Lance vs shields"},
  attack("B01"), attack("EW02")],
 "Optional elite guarding Arakane's door; carries a sealed order that bears no signature.",
 "Pierces shields and shields itself; earn your Medical or Combat Protocol before the Supreme Commander.",
 "Order-bearer in deep-water Sanctum regalia carrying a sealed scroll case with a blank, unsigned command seal")

doc = {"schema": "tnr.silent_bastion_authoring.units.v1",
       "status": "ACCEPTED REGULARS — RUL-2026-10-16-011: 16 identities, kits (shared pool), rules and the stat ladder accepted as launch values (calibration may tune later); recovery fights reuse each division's REG1 at 50% pools",
       "generator": "state/silent_bastion_authoring/tools/gen_regulars.py",
       "tiers": {str(k): {"statsMultiplier": v[0], "poolsMultiplier": v[1]} for k, v in TIER.items()}, "eliteBonus": ELITE,
       "units": U}
text = json.dumps(doc, indent=1, ensure_ascii=False) + "\n"
if "--check" in sys.argv:
    ok = os.path.exists(OUT) and open(OUT).read() == text
    print("regulars.json:", "current" if ok else "STALE"); sys.exit(0 if ok else 1)
open(OUT, "w").write(text); print(f"wrote design/regulars.json: {len(U)} regulars")
