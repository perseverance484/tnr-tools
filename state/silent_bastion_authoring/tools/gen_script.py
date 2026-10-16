#!/usr/bin/env python3
"""Author-side source for design/script.json — player-facing text for all 99 objectives.

Prose lives here (readable triple-quoted strings); the composer consumes design/script.json.
All strings accepted as launch copy by RUL-2026-10-16-011.
Reset objectives are silent by design. Each division's puzzle is solvable from clues placed in
that division's first three dialogs (marked CLUE in comments).
    python3 tools/gen_script.py [--check]
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, ".."))
OUT = os.path.join(ROOT, "design", "script.json")

QUEST = {
    "name": "Ghost Ship: The Last Directive",
    "description": (
        "The Skyglass Signal Beacon hums toward a mountain the maps call empty. The Silent Bastion, the old "
        "headquarters of the Skyglass Project, has not answered a call in a generation. Its gates stand open. "
        "Nothing guards them.\n\n"
        "Starting this expedition consumes one Skyglass Signal Beacon. Failure or abandonment will not refund it. "
        "Retrying a division costs no additional Beacon.\n\n"
        "If you still have a reward to choose from a previous expedition, claim it before you set out: an "
        "expedition cannot be completed while an earlier reward choice is waiting."
    ),
    "successDescription": (
        "The Supreme Commander has fallen, and the Bastion's orders did not fall with him. Choose your reward: "
        "a Bastion Arsenal Cache or a Bastion Research Cache."
    ),
}

DIVISIONS = {
 2: {
  "label": "Division I — Experimental Armory",
  "f1": ("Gate of the Silent Bastion", """The road ends at a gate cut into the mountain. No sentry calls out, no banner hangs, and snow has drifted unbroken across the parade ground. Whatever lived here left long ago.

Inside, the Experimental Armory is lit.

Rows of weapon racks hum behind glass. A brass placard by the first rack reads: "NEVER CUT THE SEAL WHILE THE CHARGE STILL HUMS." Somewhere ahead a whistle shrills, and a figure in a faded Skyglass drill uniform steps out of the light: a proctor, clipboard raised, as though you were late for a trial that began decades ago.

"Candidate. Trial number?" Its outline flickers at the seams."""),
  "f2": ("The Quartermaster's Ledger", """The proctor dissolves into drifting light, and the drill whistle falls silent. Nothing about that was a ghost. It answered like a man reading from a memory.

Past the trial range, an ordnance store stands open. A ledger lies on the counter in a careful hand: "Coolant first, always, or the charge flashes." Behind it, the Quartermaster looks up from a tray of sealed tags already glowing with heat.

"Live rounds are not for candidates," it says, and lifts the tray."""),
  "f3": ("Serial Zero-Three", """The armory narrows into a test gallery. A lance-armed construct stands bolted into a firing rig, a man's silhouette fused into its frame, the serial plate on its chest stamped 03. Beneath the number, someone scratched a reminder for the night crew: "Seal comes last."

Its capacitors whine awake. The rig releases."""),
  "terminal": ("Armory Command Terminal", """Beyond the gallery, a Military Command Terminal glows in the wall, and beyond that the armory's heart: a sealed door marked MASTER OF ARMS.

The terminal offers two ways through. A maintenance crawlway runs behind the live-fire racks, but its lock asks for the racks' disable sequence. Or you can request protocol access the proper way, and the duty officer, the Calibration Duelist, is already striding toward you to test your credentials with a blade."""),
  "terminal_options": {"maintenance": "Maintenance Passage: enter the disable sequence", "f4": "Protocol access: face the Calibration Duelist"},
  "puzzle": ("Live-Fire Rack Lockout", """The crawlway lock shows three switches (COOLANT, CHARGE, SEAL) and asks for the order that safely disarms the racks. A wrong order will not stop you getting through, but the armory will know you are there.

Which sequence do you enter?"""),
  "puzzle_options": {"correct": "Coolant, then Charge, then Seal", "wrong_a": "Charge, then Coolant, then Seal", "wrong_b": "Seal, then Coolant, then Charge"},
  "clues": ["NEVER CUT THE SEAL WHILE THE CHARGE STILL HUMS", "Coolant first", "Seal comes last"],
  "puzzle_logic": "f2: coolant must come first; f1: the seal may not be cut while the charge hums, so charge before seal; f3: seal comes last ⇒ Coolant → Charge → Seal.",
  "boss_clean": ("The Master of Arms", """The racks go quiet one by one, and the crawlway lets you out behind the sealed door before anyone has noticed you.

The Master of Arms turns from a forge wall hung with every weapon the Skyglass Project ever tested. "Clean work," he says. "Now show me whether you can fight as well as you can read." He chooses two blades without looking."""),
  "boss_alert": ("The Master of Arms: Alarm Raised", """The racks spit sparks and an alarm bell hammers through the armory. You reach the sealed door with the whole floor awake behind you.

The Master of Arms is already armed. "An intruder who trips the racks," he says, "fights tired and expected. Security Alert: all stations." The lights turn red."""),
  "protocol": ("Duty Officer Relieved", """The Calibration Duelist kneels, its practice blade broken, and the terminal accepts your credentials. Two field protocols unlock before the Master of Arms' door.

Medical Protocol will flood you with the armory's restorative mist: you enter the fight fully recovered. Combat Protocol will instead brace you against his Sovereign Fetters, so his stuns will not hold you."""),
  "protocol_options": {"medical": "Medical Protocol: enter fully restored", "combat": "Combat Protocol: steel yourself against stuns"},
  "lost_first": ("Recalled to the Proving Hall", """You wake on the cold floor of the proving hall with the proctor's whistle still ringing. Your pools have been set to half, the way the armory resets a failed candidate.

The proctor taps its clipboard. "Again." """),
  "lost_later": ("Recalled to the Proving Hall", """The armory throws you out the way it throws out every failed candidate: back to the proving hall, pools set to half, the doors you opened sealed behind you.

The proctor is waiting. Beat it again and the armory will let you resume from the Quartermaster's store."""),
  "recovered": ("Clearance Restored", """The proctor steps aside and stamps your trial card. The doors to the Quartermaster's store slide open again.

You keep what this fight left you. No more, no less."""),
  "battles": {
   "n.f1": "Defeat the Bastion Proving Proctor.",
   "n.f2": "Defeat the Ordnance Quartermaster.",
   "n.f3": "Defeat the Prototype Lancer Unit.",
   "n.f4": "Defeat the Calibration Duelist to claim protocol access.",
   "n.boss.clean": "Defeat the Master of Arms.",
   "n.boss.alert": "Defeat the Master of Arms under Security Alert.",
   "n.boss.medical": "Defeat the Master of Arms (Medical Protocol: fully restored).",
   "n.boss.combat": "Defeat the Master of Arms (Combat Protocol: stun-braced).",
   "recovery_first": "Retake the proving trial: defeat the Bastion Proving Proctor.",
   "recovery_later": "Retake the proving trial: defeat the Bastion Proving Proctor.",
  },
 },
 3: {
  "label": "Division II — Skyglass Research",
  "f1": ("The Archive of Impressions", """Beyond the armory's back stair, the air turns cold and blue. The Skyglass Research Division is a library of glass: shelves of crystal cores, each holding a faint, sleeping light.

An archivist made of that same pale light looks up from a ledger and frowns at you. "You are not on the register," it says, as if that were the stranger thing. "Understand what you are walking through. An impression repeats. An original hesitates."

It closes the ledger, and it does not hesitate."""),
  "f2": ("The Vat Halls", """The archivist folds back into the shelves. The register it carried lists names (Skyglass researchers, engineers, officers), each with a date and the word RECONSTRUCTED.

The vat halls beyond are lit by a single tall Skyglass lamp. A containment warden stands beneath it, visor full of water, chain of vat keys at its belt. You notice the lamp throws the warden's shadow across the floor, and the warden notices you noticing.

"Replicas never cast a shadow under the Skyglass lamp," it says. "You do. Hold still for intake." """),
  "f3": ("Iteration Nine", """In the last vat hall, something that was almost a person flickers between two outlines. Its tag reads IX. Its voice comes from both outlines at once.

"They kept trying," it says. "Every one of us carries his scar: the burn from Subject Zero's first failure. Every one of us but the copies. I am not a copy. I am not finished."

It lunges, and both of it come at you."""),
  "terminal": ("Research Command Terminal", """A command terminal stands at the door of the reconstruction theatre. The plaque beside the door reads REPLICANT ZERO, and beneath it, smaller: FIRST SUCCESSFUL SUBJECT.

The terminal offers the maintenance stair behind the specimen tanks, locked until you identify the one original among three subjects. Or request protocol access, and face the theatre's last guardian: the Failed Reconstruction Prototype, the one they kept."""),
  "terminal_options": {"maintenance": "Maintenance Passage: identify the original", "f4": "Protocol access: face the Failed Reconstruction Prototype"},
  "puzzle": ("Original or Replica", """Three subjects float in the specimen tanks under the Skyglass lamp. The lock asks which one is the original.

Subject A casts a shadow and bears the old burn scar.
Subject B casts no shadow and bears the old burn scar.
Subject C casts a shadow and bears no scar.

A wrong answer will still open the stair, but the theatre will be waiting for you."""),
  "puzzle_options": {"correct": "Subject A", "wrong_a": "Subject B", "wrong_b": "Subject C"},
  "clues": ["Replicas never cast a shadow under the Skyglass lamp", "Every one of us carries his scar", "An impression repeats. An original hesitates."],
  "puzzle_logic": "f2: replicas cast no shadow under the lamp ⇒ not B; f3: every original carries the scar, copies do not ⇒ not C ⇒ A.",
  "boss_clean": ("Replicant Zero", """The stair lets you into the theatre from behind the observation glass. On the operating floor, a man in a scientist's coat is rebuilding his own hand from light.

"Subject A," says Replicant Zero, without turning. "Correct. I was the first one they brought back, you know. My body died in that tank. I did not." He looks at you, interested. "Let us see what you are made of. I would like a copy." """),
  "boss_alert": ("Replicant Zero: Containment Breach", """The tanks drain with a roar and the theatre floods with blue warning light. Every reconstruction rig in the room is pointed at you.

"Wrong subject," says Replicant Zero, rebuilding his own hand from light. "Containment breach protocols are already running. I was the first one they brought back. My body died in that tank. I did not." He smiles. "Neither will you leave."""),
  "protocol": ("The Prototype Falls", """The Failed Reconstruction Prototype collapses into crystal dust, and the theatre's protocols unlock.

Medical Protocol will run you through the reconstruction rig: you enter the fight fully recovered. Combat Protocol will instead overcharge your chakra, increasing the damage you deal for the opening rounds."""),
  "protocol_options": {"medical": "Medical Protocol: enter fully restored", "combat": "Combat Protocol: overcharge your attacks"},
  "lost_first": ("Returned to the Archive", """You wake among the crystal shelves with your pools at half. The archivist is re-shelving a core. "Intake failed," it says. "Again." """),
  "lost_later": ("Returned to the Archive", """The research division returns you to the archive, pools at half, as though you were one more impression to be rebuilt. The halls you cleared have sealed again.

The archivist is waiting. Pass it, and the vat halls will reopen."""),
  "recovered": ("Register Amended", """The archivist writes your name into its register, crosses it out, and writes it again. The vat halls unseal.

You keep what this fight left you."""),
  "battles": {
   "n.f1": "Defeat the Skyglass Archive Keeper.",
   "n.f2": "Defeat the Impression Containment Warden.",
   "n.f3": "Defeat the Unstable Echo Subject.",
   "n.f4": "Defeat the Failed Reconstruction Prototype to claim protocol access.",
   "n.boss.clean": "Defeat Replicant Zero.",
   "n.boss.alert": "Defeat Replicant Zero under Security Alert.",
   "n.boss.medical": "Defeat Replicant Zero (Medical Protocol: fully restored).",
   "n.boss.combat": "Defeat Replicant Zero (Combat Protocol: overcharged).",
   "recovery_first": "Pass intake again: defeat the Skyglass Archive Keeper.",
   "recovery_later": "Pass intake again: defeat the Skyglass Archive Keeper.",
  },
 },
 4: {
  "label": "Division III — High Command",
  "f1": ("The Signal Room", """Above the research division, the Bastion becomes a headquarters. Maps of borders that no longer exist cover the walls of High Command. Relay lines still chatter.

A signal adjutant turns from the relay board, headset crackling. "Orders arrive by this room or they do not arrive," it says. "And only orders countersigned by the Second carry two seals. Remember that, intruder. You will not live to use it." """),
  "f2": ("The Planning Hall", """The planning hall is set for a war council no one will attend. At the head of the table, a staff tactician corrects a campaign map with a quill of chakra ink.

"Protocol matters," it says without looking up. "The Supreme Commander's seal is always placed to the left of the Second's. Always. An order that gets that wrong was written by someone who never stood in this room." It sets down the quill and stands."""),
  "f3": ("The Honor Guard", """The corridor to the Grand Marshal's office is lined with ceremonial armour. One suit is occupied. The Honor Guard Commandant raises a tower shield bearing the High Command seal.

"Since the Silence fell over this mountain, no true order has been issued from these halls," it says. "Any order dated after the Silence is a forgery, and so are those who carry them." """),
  "terminal": ("High Command Terminal", """Outside the office of The Grand Marshal (the Second, the only officer the Supreme Commander allowed to question him), a command terminal waits.

The service corridor to his office opens only for a properly authorised order. Or request protocol access through the front: the Strategist's Aide-de-Camp, last courier of the Second, stands at the door with sealed dispatches crackling at its belt."""),
  "terminal_options": {"maintenance": "Maintenance Passage: present an authorised order", "f4": "Protocol access: face the Strategist's Aide-de-Camp"},
  "puzzle": ("Countersigned Orders", """The terminal holds three orders. Only one will open the service corridor.

Order A: two seals; the Supreme Commander's seal on the right; dated before the Silence.
Order B: two seals; the Supreme Commander's seal on the left; dated before the Silence.
Order C: two seals; the Supreme Commander's seal on the left; dated after the Silence.

A forged order will still open the corridor, but it will be logged."""),
  "puzzle_options": {"correct": "Order B", "wrong_a": "Order A", "wrong_b": "Order C"},
  "clues": ["only orders countersigned by the Second carry two seals", "seal is always placed to the left of the Second's", "Any order dated after the Silence is a forgery"],
  "puzzle_logic": "f1: countersigned orders carry two seals (all three); f2: Commander's seal on the left ⇒ not A; f3: dated after the Silence is forged ⇒ not C ⇒ B.",
  "boss_clean": ("The Grand Marshal", """The service corridor delivers you into the Grand Marshal's office behind a folding map table. He does not reach for a weapon at once.

"Order B," says The Grand Marshal. "So you read before you fight. Good. I questioned his orders for thirty years, and I would question this one too, but I gave my word to hold this door." He straightens his coat. "So I will hold it." """),
  "boss_alert": ("The Grand Marshal: Order Logged", """A forged order is still an order, and High Command logs it. Every relay in the building announces your position as you step into the Grand Marshal's office.

"A forgery," says The Grand Marshal, and sounds almost disappointed. "I questioned his orders for thirty years. I never forged one." He signals, and the room's wards turn against you."""),
  "protocol": ("Dispatches Delivered", """The Aide-de-Camp falls, and its sealed dispatches burn away into the terminal, which unlocks two protocols.

Medical Protocol will open the officers' infirmary to you: you enter the fight fully recovered. Combat Protocol will instead ward your techniques, so the Grand Marshal's seals will not hold you."""),
  "protocol_options": {"medical": "Medical Protocol: enter fully restored", "combat": "Combat Protocol: ward against seals"},
  "lost_first": ("Back to the Signal Room", """You wake beside the relay board, pools at half. The adjutant does not look up. "Dismissed. Report again." """),
  "lost_later": ("Back to the Signal Room", """High Command dismisses you back to the signal room, pools at half. The planning hall's doors have closed again.

The adjutant is waiting at the relay board. Get past it, and the planning hall will reopen."""),
  "recovered": ("Report Accepted", """The adjutant initials your report and waves you through. The planning hall unseals.

You keep what this fight left you."""),
  "battles": {
   "n.f1": "Defeat the Command Signal Adjutant.",
   "n.f2": "Defeat the High Command Staff Tactician.",
   "n.f3": "Defeat the Honor Guard Commandant.",
   "n.f4": "Defeat the Strategist's Aide-de-Camp to claim protocol access.",
   "n.boss.clean": "Defeat The Grand Marshal.",
   "n.boss.alert": "Defeat The Grand Marshal under Security Alert.",
   "n.boss.medical": "Defeat The Grand Marshal (Medical Protocol: fully restored).",
   "n.boss.combat": "Defeat The Grand Marshal (Combat Protocol: seal-warded).",
   "recovery_first": "Report again: defeat the Command Signal Adjutant.",
   "recovery_later": "Report again: defeat the Command Signal Adjutant.",
  },
 },
 5: {
  "label": "Division IV — Command Sanctum",
  "f1": ("The Sanctum Gate", """The last stair climbs into the summit of the mountain. The Command Sanctum is dark obsidian and ember light, and its vanguard stands across the gate in full regalia.

"State your directive," says the Sanctum Vanguard. "No? Then hear the Sanctum's: when two orders disagree, the Sanctum obeys the one that protects the Command." Its gauntlets ignite."""),
  "f2": ("The Herald", """In the Sanctum's antechamber, a herald reads from a scroll that rewrites itself as it speaks. Lightning moves in its eyes.

"Directive..." it begins, and stops, frowning at the scroll. "A directive without a signature is not an order. It is a rumour." It rolls the scroll shut. "You are a rumour, intruder. I will correct you." """),
  "f3": ("The Last Watch", """The night-watch corridor ends at the Supreme Commander's outer ring. The Last Watch Executor stands in a tattered cloak, twin glaives crossed.

"The newest order countermands the old, if it is signed," it recites, as if from a manual worn thin with use. "I have kept watch for a long time, waiting for a new one. None has come." Its mask is stamped with an order no one can read."""),
  "terminal": ("Sanctum Terminal", """The outer ring of the Sanctum holds the Bastion's last Military Command Terminal. Past it is the door of Supreme Commander Arakane.

The maintenance channel around the ring will open for whoever can name the directive currently in force. Or request protocol access, and face the Order-Bearer of the Sanctum, who guards the door with a sealed scroll case and a blank, unsigned command seal."""),
  "terminal_options": {"maintenance": "Maintenance Passage: name the directive in force", "f4": "Protocol access: face the Order-Bearer of the Sanctum"},
  "puzzle": ("Contradictory Directives", """Three directives are posted on the terminal. Only one is in force.

Directive 1 (older, signed by the Supreme Commander): "Hold the Sanctum doors."
Directive 2 (newer, unsigned): "Open the doors to the intruder."
Directive 3 (newest, signed by the Supreme Commander): "Seal the outer ring. Let the intruder reach me."

A wrong answer still opens the channel, but the ring will be on alert."""),
  "puzzle_options": {"correct": "Directive 3", "wrong_a": "Directive 1", "wrong_b": "Directive 2"},
  "clues": ["the Sanctum obeys the one that protects the Command", "A directive without a signature is not an order", "The newest order countermands the old"],
  "puzzle_logic": "f2: an unsigned directive is not an order ⇒ not 2; f3: the newest signed order countermands the old ⇒ 3 over 1; f1 (protect the Command) is consistent with 3, which is the Commander's own order ⇒ 3.",
  "boss_clean": ("Supreme Commander Arakane", """The channel lets you out at the foot of the throne room, exactly where Directive 3 said it would.

Supreme Commander Arakane stands at a window that looks out over the whole mountain range. "You read the orders correctly," he says. "Then you understand what this place is. Every officer you passed believes he is still serving. I gave them that. I built this command so it would outlast us." He turns. "It has. Now it will outlast you." """),
  "boss_alert": ("Supreme Commander Arakane: The Ring Is Sealed", """The ring locks down behind you as you step into the throne room. Every ward in the Sanctum turns toward you.

Supreme Commander Arakane does not hurry. "You obeyed a rumour, or an order that had already been replaced," he says. "Command does not forgive that. I built this command to outlast us all." He turns from the window. "It will outlast you." """),
  "protocol": ("The Seal Is Broken", """The Order-Bearer falls, and its blank command seal shatters on the floor. The terminal unlocks the Sanctum's last two protocols.

Medical Protocol will restore you in the Sanctum's reliquary: you enter the final fight fully recovered. Combat Protocol is the Sanctum's last field directive: for the opening rounds, nothing the Supreme Commander does can weaken you."""),
  "protocol_options": {"medical": "Medical Protocol: enter fully restored", "combat": "Combat Protocol: ward yourself against debilitation"},
  "lost_first": ("Turned Back at the Gate", """You come to at the Sanctum gate, pools at half. The Vanguard has not moved. "State your directive," it says again."""),
  "lost_later": ("Turned Back at the Gate", """The Sanctum turns you back to its gate, pools at half, and closes the antechamber behind you.

The Vanguard is waiting. Break past it once more, and the antechamber will open."""),
  "recovered": ("The Gate Yields", """The Vanguard lowers its burning gauntlets. The antechamber doors grind open again.

You keep what this fight left you. Losing to the Supreme Commander himself would end the expedition."""),
  "battles": {
   "n.f1": "Defeat the Sanctum Vanguard.",
   "n.f2": "Defeat the Directive Herald.",
   "n.f3": "Defeat the Last Watch Executor.",
   "n.f4": "Defeat the Order-Bearer of the Sanctum to claim protocol access.",
   "n.boss.clean": "Defeat Supreme Commander Arakane. Defeat ends the expedition.",
   "n.boss.alert": "Defeat Supreme Commander Arakane under Security Alert. Defeat ends the expedition.",
   "n.boss.medical": "Defeat Supreme Commander Arakane (Medical Protocol: fully restored). Defeat ends the expedition.",
   "n.boss.combat": "Defeat Supreme Commander Arakane (Combat Protocol: debuff-warded). Defeat ends the expedition.",
   "recovery_first": "Break the gate again: defeat the Sanctum Vanguard.",
   "recovery_later": "Break the gate again: defeat the Sanctum Vanguard.",
  },
 },
}

AFTERMATH = ("The Last Directive", """Supreme Commander Arakane falls to one knee, and then he is only light, settling over the floor of the throne room like ash.

For a moment the Bastion is silent in a new way. The relay lines stop. The lamps dim.

Then, in the signal room far below, the relay board wakes. A new order prints itself, line by line, onto the Supreme Commander's own paper. It is dated today. It bears no seal you have seen anywhere in the Bastion. It is addressed to the Ghost Ship.

The Bastion did not stop giving orders when its commander fell. Something else is still giving them.""")
WIN = "Expedition complete."
FAIL = "Supreme Commander Arakane has defeated you. The expedition is over."

def build():
    obj = {}
    for d, D in DIVISIONS.items():
        p = f"d{d}"
        for key, nid in (("f1", f"{p}.n.f1"), ("f2", f"{p}.n.f2"), ("f3", f"{p}.n.f3"), ("terminal", f"{p}.n.terminal"),
                         ("puzzle", f"{p}.n.puzzle"), ("boss_clean", f"{p}.n.boss.clean"), ("boss_alert", f"{p}.n.boss.alert"),
                         ("protocol", f"{p}.n.protocol"), ("lost_first", f"{p}.lost_first"), ("lost_later", f"{p}.lost_later"),
                         ("recovered", f"{p}.recovered")):
            title, text = D[key]
            obj[nid] = {"kind": "dialog", "title": title, "text": text.strip(), "division": D["label"]}
        obj[f"{p}.n.terminal"]["options"] = {f"{p}.n.puzzle": D["terminal_options"]["maintenance"], f"b{d}.n.f4": D["terminal_options"]["f4"]}
        obj[f"{p}.n.puzzle"]["options"] = {k: v for k, v in D["puzzle_options"].items()}
        obj[f"{p}.n.puzzle"]["logic"] = D["puzzle_logic"]
        obj[f"{p}.n.puzzle"]["clues"] = D["clues"]
        obj[f"{p}.n.protocol"]["options"] = {f"b{d}.n.boss.medical": D["protocol_options"]["medical"], f"b{d}.n.boss.combat": D["protocol_options"]["combat"]}
        for suffix, text in D["battles"].items():
            obj[f"b{d}.{suffix}"] = {"kind": "battle", "text": text, "division": D["label"]}
        for r in ("reset_first", "reset_later_win", "reset_later_loss"):
            obj[f"r{d}.{r}"] = {"kind": "reset", "text": "", "note": "silent by design"}
    obj["d.aftermath"] = {"kind": "dialog", "title": AFTERMATH[0], "text": AFTERMATH[1].strip(), "division": "Aftermath"}
    obj["w.complete"] = {"kind": "win", "text": WIN}
    obj["f.arakane"] = {"kind": "fail", "text": FAIL}
    return {"schema": "tnr.silent_bastion_authoring.script.v1",
            "status": "ACCEPTED COPY — RUL-2026-10-16-011 (all 99 objective texts, 4 puzzles, Division IV foreshadowing)",
            "generator": "state/silent_bastion_authoring/tools/gen_script.py",
            "quest": QUEST, "divisions": {str(d): D["label"] for d, D in DIVISIONS.items()}, "objectives": obj}

text = json.dumps(build(), indent=1, ensure_ascii=False) + "\n"
if "--check" in sys.argv:
    ok = os.path.exists(OUT) and open(OUT).read() == text
    print("script.json:", "current" if ok else "STALE"); sys.exit(0 if ok else 1)
open(OUT, "w").write(text); print(f"wrote design/script.json: {len(json.loads(text)['objectives'])} objectives")
