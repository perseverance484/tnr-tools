# 31 - ARC: The Salt Crown (treatment + full storyboard)

[NON-CANON CANDIDATE. Standalone multi-ending CYOA arc: one hub quest, three branch quests, eight endings. All names dedup-checked against catalogs 40-43 (clean; "Founder" appears once in the asset catalog only, no item/AI collision). All numbers, levels, and rewards are placeholders unless marked RULED. Prefix: `salt_`. Everything builds `hidden: true`.]

## Logline

The world's greatest poisoner has been poisoned, and the free town she built must choose an heir before her body is cold. The player, an outsider with no stake, becomes the witness whose word crowns a successor, exposes a forgery, or unmakes the crown entirely.

## Theme

**Salt preserves what the villages threw away.** Every resident of Brinemark is someone's missing-nin, deserter, or disgrace. The arc asks what holds a town of discarded people together: fear (Roke), appetite (Vess), surrender (Ansa), or the truth (the hidden path).

## Architecture (engine shape)

- **Hub quest: The Salt Crown.** Shared investigation spine, one-shot final deduction, two fork-node variants (3-choice and 4-choice deathbed scenes), five terminals: three `new_quest`-then-`win_quest` branch exits and two hidden endings.
- **Branch quests** (granted via `newQuestIds` on dialog-gated `new_quest` nodes): The Ledger of Names (Roke), The Last Manifest (Vess), The Long Road In (Ansa). Each carries one sub-fork and two endings.
- **Ending count: 8.** Divergence is mechanically real: each path is a different quest record completed. No flags exist in the engine; "the world remembers" = which branch quest sits in the player's history.
- **Deduction design rule:** the two early deductions reset-teach (wrong reads bounce with the Saltmother's correction). The final deduction is **one-shot**: wrong reads route forward to the 3-choice fork and the hidden path is gone for that run. The quest teaches careful reading, then tests it for real. [DECISION: confirm the one-shot exception.]
- **Contract to verify by capture before build:** whether `newQuestIds` grants a `hidden: true` quest, and how granted quests surface to the player (quest log only vs browsable). Exclusivity of branches depends on grant-only entry; if granted quests must be public, all three branches become completable by anyone post-hub and prerequisite gating cannot restore exclusivity (all three would share the same prereq). This is the arc's one load-bearing unknown.

## World additions (paste block for 27_LORE section 4/5 on acceptance)

- **Brinemark** [NON-CANON CANDIDATE]: a free town on the salt flats of a dried inland sea between the Akasumi and Akikaze borders [PLACEHOLDER: placement]. Neither village claims it; claiming it means war with the other. Founded by the Saltmother. Population: the discarded.
- **The Saltmother** [NON-CANON CANDIDATE]: legendary missing-nin; her village's poisons-and-interrogation specialist in the last war; deserted after it; bounty never rescinded. Her framed bingo-book poster hangs in the Brinemark tavern; whoever rules the town "wears the Salt Crown," the price on her head. Verbal register: dry, precise, amused by her own death.
- **Roke** [NON-CANON CANDIDATE]: her adopted son, a former hunter-nin she caught and spared; head of the town watch. Keeps a bingo book of Brinemark's own residents. Tic: quotes entry numbers instead of names.
- **Vess** [NON-CANON CANDIDATE]: deserted village quartermaster who left with a set of ration and route seals; her forged papers feed the town down roads no village patrols. Tic: everything is priced, including apologies.
- **Ansa** [NON-CANON CANDIDATE]: retired ANBU captain who spent her career hunting the Saltmother and retired into the town she never caught. Tic: speaks in after-action report cadence.

## The truth (spoiler ledger, binding for all dialog)

The Saltmother is dying of chakra burn from her war work, not poison. The "poisoning" is her own forgery: she dosed herself with a compound only she can pace, staged the crime, and is running succession as her last mission. Three planted true facts implicate each claimant (Roke's confiscated crate, Vess's freight ledger, Ansa's requisition); the tell is the dose: the compound kills in hours, she has been dying nine days. Fair-play rule: the nine days are stated on screen (d03 aftermath and d11) before the final deduction.

---

# HUB QUEST: The Salt Crown

`questType` [PLACEHOLDER: story vs mission], level band [PLACEHOLDER], `hidden: true`. Dialog rules per 23 sec 6.2: max 3-4 sentences per node, no em dashes in dialog text, choices are stances in the player's voice.

## Node graph

```
d01 -> d02 -> d03 -> d04 -> d05 -> c01 -> d06 -> d07 -> f01 -> d08 -> c02 -> d09
        (r01 resets to d03)   (r02 resets to d06)  (f01 fail -> r03 -> d07)  (r04 resets to d09)
d09 -> d10 -> c03 -> d11 (ONE-SHOT FORK GATE)
d11 wrong reads -> dF3 (3 choices) | correct read -> dF4 (4 choices)
dF3/dF4 -> dR -> nqR -> wR   |   dV -> nqV -> wV   |   dA -> nqA -> wA
dF4 fourth choice -> d15 -> d16 -> w4 | w5
```

Single start: d01. All resets point at in-flow nodes. Every dialog carries a choices array. f01 carries `failObjectiveId`. nq/w chains sit directly behind gating dialogs (dR/dV/dA), so the instant tasks fire only after the consequence scene is read.

## Act 1: Arrival

**d01 (dialog) - The gate.** Scene: Brinemark gate, dusk.
> The gate guard reads your papers twice, then your face three times. Behind him, someone is boarding up the tavern windows in the middle of the day. He waves you through without a word, which is somehow worse.
- Choice: "Walk in like you belong here." -> d02

**d02 (dialog) - The news breaks.**
> The letter in your pack is addressed to the Saltmother herself. By sundown the whole town knows two things: their founder has been poisoned, and a stranger arrived carrying her mail the same day. Doors close as you pass.
- Choice: "Find whoever is in charge before they find you." -> d03

**d03 (dialog) - Audience.** Scene: sickroom. sceneCharacter: Saltmother portrait.
> She is smaller than her legend, and her eyes are not sick at all. "The greatest poisoner of the war, poisoned nine days and still breathing. Either my killer is impossible, or something worse is true." She studies you. "You are the only soul in Brinemark with nothing to gain from my death. That makes you the only witness I can afford."
- Choice: "I will find the truth. You have my word." -> d04
- Choice: "Witnesses charge by the day." -> d04
- Choice: "Find another stranger." -> **r01 (reset_quest)**:
> The gates sealed at dusk and they do not open for refusals. "There is no leaving," she says, almost kindly. "There is only pricing." (resets to d03)

**d04 (dialog) - Terms.**
> "Three claimants will wear my crown or burn it. Roke, my son, who files people like crimes. Vess, who feeds this town along roads that do not exist. Ansa, who hunted me for twenty years and retired into my shadow." She presses her seal into your palm. "Start with my son. He lies the least and hides the most."
- Choice: "Sons make tidy killers." -> d05
- Choice: "Take the seal and go." -> d05

## Act 2: The investigation (fixed order: Roke, Vess, Ansa)

**d05 (dialog) - Roke.** Scene: watch office, wall of ledgers.
> Roke does not look up from his desk. "Entry 114 arrives carrying her mail on the day she drops. If you were in my book, you would be a paragraph already." He slides a key across the desk. "The evidence room. Look. I confiscated worse than what felled her."
- Choice: "Take the key. Watch your back." -> c01

**c01 (collect_item) - The Confiscation Manifest.** Objective text: "Retrieve the Confiscation Manifest from the watch evidence room." `current_sector`, image required. -> d06

**d06 (dialog) - Deduction one (reset-teaching).**
> The manifest lists a war-era compound crate: seized last winter, signed by Roke, seal broken. The dates line up too well. But the crate count runs wrong in the other direction. Something was added to evidence, not taken.
- Choice: "Roke poisoned her. It is all here." -> **r02 (reset_quest)**:
> The Saltmother reads your accusation once. "My son signs what he seizes. A poisoner who signs his own poison is not a suspect, he is a gift. Look at what the manifest does not say." (resets to d06)
- Choice: "The crate was salted after the fact. Someone wants Roke found." -> d07

**d07 (dialog) - Vess.** Scene: dock warehouse, lantern light.
> You find Vess pricing grain by lantern light, flanked by dockhands with soldier posture. "The old woman's seal opens doors," she says, "but my crew opens people. They would like to know if her paper still means anything." The dockhands are already moving.
- Choice: "Show them exactly what it means." -> f01

**f01 (defeat_opponents) - Brinemark Dock Crew.** `current_sector`, image required, `failObjectiveId` -> **r03 (reset_quest)**:
> You wake in a salt bin with your boots gone and the seal untouched. Vess left a note: "Paper is not authority. Come back when you can enforce it." (resets to d07)
Win -> d08

**d08 (dialog) - Vess talks.**
> Vess calls them off with one finger, smiling like you passed an audit. "Good. Brinemark cannot be held by anyone soft." She tosses you a key. "My roads moved that compound, yes. Check my ledger. Then ask yourself who paid the freight."
- Choice: "Pull the ledger before she changes her mind." -> c02

**c02 (collect_item) - The Route Ledger.** Objective text: "Recover the Route Ledger from Vess's route office." `current_sector`, image required. -> d09

**d09 (dialog) - Deduction two (reset-teaching).**
> The ledger shows the crate moving on Vess's road, freight paid in advance, the sender's mark burned off every page. Vess profits from this town alive, not dead. But whoever paid knew her roads well enough to use them blind.
- Choice: "Vess moved the poison. She is guilty." -> **r04 (reset_quest)**:
> The Saltmother taps the burned marks. "Vess sells passage, not purpose. If she wanted me dead I would have died at a dinner years ago. Who pays in advance and burns their own name?" (resets to d09)
- Choice: "The sender knew the roads but hid from them. Someone with inside knowledge." -> d10

**d10 (dialog) - Ansa.** Scene: bare room.
> Ansa receives you in a room with nothing on the walls, which after Roke's office feels like a confession. "Subject: myself. Motive: confirmed. I spent twenty years learning her poisons in order to catch her. Opportunity: also confirmed." She sets a letter on the table. "I ordered that compound. Now ask me why."
- Choice: "Why order the poison that killed her?" -> c03

**c03 (collect_item) - The Requisition Letter.** Objective text: "Take Ansa's Requisition Letter as evidence." `current_sector`, image required. -> d11

**d11 (dialog) - The final deduction. ONE-SHOT. No reset.**
> Her letter is real: the compound was ordered for identification training half a year ago, logged and countersigned. Three claimants, three true facts, and none of them fits the one thing nobody says aloud. The compound in that crate kills in hours. The Saltmother has been dying for nine days.
- Choice: "It was Roke. The evidence room tells the story." -> dF3
- Choice: "It was Vess. Her roads, her freight." -> dF3
- Choice: "It was Ansa. Motive, means, and twenty years of patience." -> dF3
- Choice: "The dose is wrong. None of this is what it looks like." -> dF4

## Act 3: The fork

**dF3 (dialog) - Deathbed, three choices.** Scene: sickroom, all claimants present.
> The deathbed room holds three claimants and one silence. The Saltmother's eyes find yours. "My witness has walked every road in this town. Speak, and Brinemark will follow the name you say."
- Choice: "Roke should rule. Order keeps salt towns alive." -> dR
- Choice: "Vess should rule. A fed town forgives anything." -> dV
- Choice: "Ansa should rule. Brinemark needs a shield, not a crown." -> dA

**dF4 (dialog) - Deathbed, four choices.** Same scene; description varies by one line:
> The deathbed room holds three claimants and one silence. The Saltmother's eyes find yours. "Speak, and Brinemark will follow the name you say." The dose still itches at the back of your mind.
- The three choices above, plus:
- Choice: "Say nothing. Ask her why the dose is wrong." -> d15

**dR (dialog) - Consequence: Roke.**
> Roke does not thank you. He opens a fresh ledger and begins writing names, starting with the two people beside him. The Saltmother closes her eyes as if a sum has balanced. Whatever Brinemark becomes now, it will be filed correctly.
- Choice: "Long live the keeper of names." -> nqR

**nqR (new_quest)** grants The Ledger of Names -> **wR (win_quest)**:
> Word crosses the flats by morning: Brinemark has an heir with a book of everyone's sins. Your part is not finished. The watch expects you at dawn.

**dV (dialog) - Consequence: Vess.**
> Vess laughs once, short and real, and the dockhands relax for the first time in days. "Then we eat," she says. "All of us. Ask no questions about the menu." The Saltmother watches her the way one watches weather.
- Choice: "Long live the open road." -> nqV

**nqV (new_quest)** grants The Last Manifest -> **wV (win_quest)**:
> Brinemark chose its stomach over its conscience, and it will be fed. Vess wants you at the vault before the week turns.

**dA (dialog) - Consequence: Ansa.**
> Ansa stands like a report being filed. "Petition drafted. Route planned. Casualties expected." Roke and Vess leave without a word, which is its own declaration of war. The Saltmother smiles at the ceiling. "Twenty years, and she catches me at last."
- Choice: "Long live the shield." -> nqA

**nqA (new_quest)** grants The Long Road In -> **wA (win_quest)**:
> Brinemark will kneel to a village to survive the next war. The petition must cross the flats, and every road is watched. Ansa expects you at the gate.

## Hidden path

**d15 (dialog) - The reveal.**
> The room empties at her word until only you remain. "Nine days," she says. "You counted. Good." She sits up with no effort at all. "I am dying, witness, but slowly, and of my own war. A murdered legend holds a town together. A sick old woman scatters it. So I forged my murder and watched who moved."
- Choice: "You staged your own death to run succession." -> d16

**d16 (dialog) - The last choice.**
> "Every claimant showed me their teeth this week, and you saw all of it. So here is the final choice, and it is yours alone. Tell Brinemark the truth and let this town choose with clear eyes, or keep my forgery and let me finish the work." Her hand does not tremble at all.
- Choice: "The truth. Brinemark deserves clear eyes." -> w4
- Choice: "Keep the forgery. Finish your work." -> w5

**w4 (win_quest) - Ending: The Crown Unmade.**
> You tell the town at the salt market at noon. Some curse her, some laugh, and by evening the claimants stand before a crowd that knows everything. Brinemark will choose for itself now, loudly, and for years. The Saltmother watches from her window: unburdened, unforgiven, and alive.

**w5 (win_quest) - Ending: The Long Game.**
> You say nothing, and the forgery holds. The Saltmother has months to finish shaping her heirs, and now she has a witness who keeps secrets of their own. On your way out she presses the framed bounty poster into your hands. "A crown," she says, "for the only head in Brinemark that stayed cool."

[DECISION: hidden endings terminate in the hub as written, or each grants a short epilogue quest instead.]

---

# BRANCH QUEST R: The Ledger of Names

Granted by nqR. Prereq wiring [PLACEHOLDER pending the new_quest visibility capture]. Theme: order that costs everyone their past.

```
dR1 -> fR1 -> dR2 -> cR1 -> dR3 (SUB-FORK)
(fR1 fail -> rR1 -> dR1)
burn: dR3 -> dR4 -> bR1 -> wR-burn   (bR1 fail -> rR2 -> dR4)
keep: dR3 -> dR5 -> wR-keep
```

**dR1 (dialog) - Dawn muster.**
> Roke hands you a watch armband and does not ask if you slept. "Entries 61 through 80: the dock cells. We take them in order, alive where practical." Behind him the watch checks their blades like clerks checking sums.
- Choice: "In order, then. Move." -> fR1

**fR1 (defeat_opponents) - Dockside Smuggler Cell.** `current_sector`, image, fail -> **rR1**:
> Roke pulls you out before the water does. "Entry 114, status: revised downward. Again, and correctly this time." (resets to dR1)
Win -> dR2

**dR2 (dialog) - The sweep.**
> By noon the docks are quiet and the cells are full, and the town watches the watch with new eyes. A prisoner spits through the bars as you pass. "Ask him what number YOU are."
- Choice: "Numbers do not scare me." -> cR1
- Choice: "Find out for yourself." -> cR1

**cR1 (collect_item) - The Watch Ledger Page.** Objective text: "Slip into Roke's office and pull your own page from the watch ledger." `current_sector`, image. -> dR3

**dR3 (dialog) - SUB-FORK: your page.**
> Your page is thorough. Your arrival, your errand, the seal in your pocket, a column marked "uses" and a column marked "ends." Everyone in Brinemark has a page. The Saltmother has three.
- Choice: "Burn the book. No one should own a town's sins." -> dR4
- Choice: "Keep it. Someone must, and better you than only him." -> dR5

**dR4 (dialog) - Pre-battle.**
> The first pages catch as the door opens. Roke watches his life's work curl, and for once he does not quote a number. "Entry 114," he says, drawing steel. "Status: closed."
- Choice: "Finish what you lit." -> bR1

**bR1 (start_battle) - Roke.** fail -> **rR2**:
> You come to in the smoke with the book half burned and Roke standing over you, breathing hard, waiting. He wants you to try again. That is the worst part. (resets to dR4)
Win -> wR-burn

**wR-burn (win_quest) - Ending: Unfiled.**
> The book is ash and the watch is leaderless, and Brinemark wakes unfiled for the first time in years. It will be messier now, and freer, and nobody's past is a weapon anymore. In the tavern, someone has drawn a small crown on the Saltmother's poster.

**dR5 (dialog) - The pact.**
> "You understand now," Roke says, and hands you a pen instead of a blade. "The book does not punish. The book remembers, so that mercy becomes a choice instead of an accident." You write your first entry with a steady hand. It gets easier. That is the part that should worry you.
- Choice: "Entry one. Begin." -> wR-keep

**wR-keep (win_quest) - Ending: The Second Pen.**
> Brinemark is orderly, quiet, and afraid in a way it has decided to call safe. You keep the book now, beside Roke. Some nights you read your own page and add a line, just to stay honest.

---

# BRANCH QUEST V: The Last Manifest

Granted by nqV. Theme: a fed town with a rotten keel.

```
dV1 -> mV1 -> dV2 -> cV1 -> dV3 (SUB-FORK)
finish: dV3 -> dV4 -> dlV1 -> wV-fed
turn:   dV3 -> dV5 -> bV1 -> wV-honest   (bV1 fail -> rV1 -> dV5)
```

**dV1 (dialog) - The plan.**
> "The old woman's vault holds every deed, debt, and founding paper in Brinemark," Vess says, drawing the route in spilled salt. "Roke will freeze it by law, Ansa by petition. We take it tonight, or the town's paper belongs to whoever hates us most."
- Choice: "Walk me through the approach." -> mV1

**mV1 (move_to_location) - The counting house.** Objective text: "Reach the counting house above the founder's vault." Sector [PLACEHOLDER], image. -> dV2

**dV2 (dialog) - Under the counting house.**
> The vault door answers to the seal in your pocket like it remembers her hand. Inside, the shelves are exactly what Vess promised: the whole town in paper. The crew starts loading. You start reading.
- Choice: "Find the founder's seal. Fast." -> cV1

**cV1 (collect_item) - The Founder's Seal.** Objective text: "Take the Founder's Seal from the vault." `current_sector`, image. -> dV3

**dV3 (dialog) - SUB-FORK: the manifests.**
> The seal sat on a shelf of manifests in the Saltmother's own hand. This season's passenger lists are here too, written in Vess's: names, freight paid in advance, and a final column of destinations that do not exist. Fourteen people rode her roads into nowhere this year.
- Choice: "Finish the job. The town eats because of her." -> dV4
- Choice: "Turn the crew. This ends in the vault." -> dV5

**dV4 (dialog) - The quiet pocket.**
> You pocket the manifests where the crew cannot see and hand over the vault at dawn. "Smart," Vess says, not looking at your pocket, "and smarter still if those stay unread." The town will eat all winter. You know exactly what the grain costs now.
- Choice: "Deliver the seal. Say nothing." -> dlV1

**dlV1 (deliver_item) - The Founder's Seal to Vess.** Objective text: "Deliver the Founder's Seal to Vess at the docks." `current_sector`, image. -> wV-fed

**wV-fed (win_quest) - Ending: The Menu.**
> Brinemark under Vess is loud, fed, and busy, and nobody asks about the roads. You kept the manifests. Some nights that feels like a conscience. Other nights it feels like leverage.

**dV5 (dialog) - Fourteen names.**
> You read the fourteen names aloud in the vault, one by one, and the crew goes very still. Vess denies not a line of it. "Feed a town or judge it," she says from the stair, already leaving. "You cannot do both." Her captain draws for her.
- Choice: "Let her go. Not him." -> bV1

**bV1 (start_battle) - The Vaultbreaker Captain.** fail -> **rV1**:
> You wake among scattered paper with the fourteen names still in your fist. The captain waits by the vault door. He owes her that much, and you owe those names another try. (resets to dV5)
Win -> wV-honest

**wV-honest (win_quest) - Ending: Paper on the Door.**
> Vess vanished down her own roads before dawn, and her network scattered with her. Brinemark will be hungry by midwinter and it knows it, and the market square has never argued louder or more honestly. The fourteen names are nailed to the vault door, where paper belongs.

---

# BRANCH QUEST A: The Long Road In

Granted by nqA. Theme: safety through surrender. The arc's action chapter.

```
dA1 -> mA1 -> dA2 -> fA1 -> mA2 -> dA3 -> bA1 -> dA4 (SUB-FORK) -> wA-file | wA-burn
(fA1 fail -> rA1 -> dA2; bA1 fail -> rA2 -> dA3)
```

**dA1 (dialog) - The gate at dawn.**
> Ansa folds the petition into a bone tube and straps it under her arm like a splint. "Two sectors of open salt between here and the Akikaze border post. Roke's watch wants me arrested, Vess's roads want me lost. Standard escort doctrine: you are the blade, I am the package."
- Choice: "Move out. Stay low." -> mA1

**mA1 (move_to_location) - First leg.** Objective text: "Escort Ansa across the open flats." Sector [PLACEHOLDER], image. -> dA2

**dA2 (dialog) - Interceptors.**
> Dust on the eastern rise, moving wrong for traders. Ansa reads it in one glance. "Watch deserters. Roke's hardliners did not wait for orders. Contact in sixty."
- Choice: "Let them come to us." -> fA1

**fA1 (defeat_opponents) - Watch Deserters.** `current_sector`, image, fail -> **rA1**:
> Ansa drags you behind a salt ridge and stops the bleeding with field efficiency. "Casualty report: premature. We hold here and we go again." (resets to dA2)
Win -> mA2

**mA2 (move_to_location) - Second leg.** Objective text: "Push through to the Akikaze border post." Sector [PLACEHOLDER], image. -> dA3

**dA3 (dialog) - The last mile.**
> The border post sits low on the horizon, close enough to count its flags. Which is when the salt itself stands up: road agents in flat-country grey, and at their center a woman wearing one of Vess's route seals like a badge. "Toll road," she calls. "The package pays."
- Choice: "The package walks through." -> bA1

**bA1 (start_battle) - The Flatland Toll.** fail -> **rA2**:
> You come around to Ansa standing over you, blade out, the agents circling wider now. "After-action note: we are not done. On your feet." (resets to dA3)
Win -> dA4

**dA4 (dialog) - SUB-FORK: the steps.**
> The border post clerk waits behind a window with the receipt forms already stamped. Ansa sets the tube on the counter and does not let go. "Twenty years hunting the woman who built a free town," she says quietly. "Say the word, witness. I file it, or I burn it on these steps."
- Choice: "File it. Brinemark survives the next war." -> wA-file
- Choice: "Burn it. Brinemark stays Brinemark." -> wA-burn

**wA-file (win_quest) - Ending: The Number She Could Live With.**
> The petition enters the record, and Akikaze's flag will fly over the salt flats by spring. Brinemark is safe, taxed, patrolled, and no longer entirely itself. Ansa signs the receipt with a steady hand. "Casualties expected," she says. "This was the number I could live with."

**wA-burn (win_quest) - Ending: Alone and Marked.**
> The tube burns fast on the border post steps while the clerk watches through the glass, unmoved. "Then we stand alone," Ansa says, and for the first time she sounds relieved. Brinemark stays free, and marked, and the next war will find it. So will you.

---

# Asset plan (per 25 production order; counts are the ask, not the art)

**Backgrounds (7):** Brinemark gate at dusk; the Saltmother's sickroom; watch office (ledger wall); dock warehouse (lantern light); founder's vault; open salt flats; Akikaze border post.
**Scene characters (4):** the Saltmother, Roke, Vess, Ansa.
**Quest item icons (6):** sealed letter, Confiscation Manifest, Route Ledger, Requisition Letter, Watch Ledger Page, Founder's Seal.
**Enemy art:** per AI plan below. **Emblem (1):** the Salt Crown (the framed bounty poster motif).

# AI plan (design later per 21 Workflow A; names dedup-clean)

| AI | Role | Fights |
|---|---|---|
| Brinemark Dock Crew | trash cell | hub f01 |
| Dockside Smuggler | trash cell | R fR1 |
| Roke, Keeper of Names | boss | R bR1 |
| Vaultbreaker | trash | (optional adds, V) |
| Vaultbreaker Captain | boss | V bV1 |
| Watch Deserter | trash cell | A fA1 |
| Flatland Toll Agent | trash | A bA1 adds |
| The Toll Keeper | miniboss | A bA1 |

# Decision list (all reserved for Brandon)

1. Quest types and level band for hub + branches; tier levels.
2. All rewards, per-ending reward variance (do endings pay differently?), and whether resets carry partial credit (default zero).
3. Town placement: which sectors for Brinemark scenes and the two escort legs.
4. One-shot final deduction (d11 has no reset): approve or soften.
5. Hidden endings terminate in hub vs each granting an epilogue quest.
6. **Capture request:** one `new_quest` grant of a hidden quest on a test account, to confirm hidden-grant behavior and how granted quests surface. This decides the branch exclusivity model and must precede manifest work.
7. Enemy counts per fight, AI stats, boss mechanics.
8. Ratify or rename: Brinemark, the Saltmother, Roke, Vess, Ansa, and the four quest names.


## Addendum (Jul 10 2026): rulings + architecture status

**Rulings (decisions 1-6 of the decision list, RULED):**
1. All four quests `questType: "story"`, level band 100.
2. Rewards: 22,000 XP / 70,000 ryo / 480 prestige / 500 tokens / 500 clan points per quest. Hidden endings w4/w5 each carry ONE FULL EXTRA reward line as objective-level rewards on the terminal node (hidden-path total = hub + branch). Resets carry zero.
3. Brinemark = sector 234. Escort legs: mA1 -> sector 267, mA2 -> sector 268. All other location objectives `sectorType: specific, sector: 234` (town-anchored model).
4. d11 one-shot final deduction: APPROVED as designed, no reset.
5. Hidden endings terminate in the hub, no epilogue quests.
6. Exclusivity testing complete (see 23 addendum Jul 10). **Multi-record branch architecture is DEAD in the current engine.** Options: (a) fold branches into the hub as one ~60-node mega-quest with multiple terminals (recommended, works today; per-branch payouts move to terminal-node objective rewards), or (b) upstream engine change enabling grant-chaining. **ARCHITECTURE RULING PENDING.** Decisions 7 (enemy counts/stats/boss mechanics) and 8 (name ratification) remain open.

**Publish-time consequence of the sceneCharacters rule:** every Salt Crown quest needs scene characters set before `hidden: false` (the asset plan already includes the four portraits).
