# Single source for the three new Skyglass treasure hunts. Text rewritten 2026-10-28 to docs/design/SKYGLASS_STORY_BIBLE.md.
# (Original header:) Single source for the three new Skyglass treasure hunts (draft content). Borrowed text is marked B (live Ghost Ship
# quest, push/98 capture, or the approved Skyglass graph patch); new text is marked N and is a draft for the director.
# Node: (id, task, scene, source, text, edges, extra)
#   edges: list of (choice label or "", target)
#   extra: dict, e.g. {"fight": [...], "debuff": "...", "step": "V"}

ARCHIVE = {
 "name": "The Quarantined Archive", "chart": "Chart of the Quarantined Archive", "ladder": "clean V · alarm III",
 "premise": "This chart shows a room no other plan of the wreck admits to: an archive someone aboard sealed shut, and filed behind three seals. A wrong answer at any seal rings the alarm, and the archive's guard comes for you before you can go on. Answer all three cleanly for the better haul.",
 "scenes": ["exterior_keel_walk", "lower_hull", "reconstruction_chamber", "quarantined_archive"],
 "portraits": ["Sealwright"],
 "new_ai": [],
 "nodes": [
  ("d_arrive", "dialog", "exterior_keel_walk", "B", "The seal channels along the keel still glow, carrying the Core's chakra up into the hull. One thin line runs the wrong way, against their flow, and it carries scraps of handwriting with it, toward a part of the ship no plan admits to. Someone aboard once cut something off from the rest of the ship, and hid it.", [("Follow the breach into the hull", "d_hull")], {}),
  ("d_hull", "dialog", "lower_hull", "N", "Below the tide line the hull is mending itself out of timber and rope that do not belong together. Something large is being mended with them. The Core has lost the shape of whoever it was, and it is filling the gaps with whatever it can reach.", [("Face what the hull is building", "b_horror")], {}),
  ("b_horror", "start_battle", "lower_hull", "N", "The Core Horror drags itself out of the half-mended frame.", [("", "d_conduit")], {"fight": ["Core Horror"]}),
  ("d_conduit", "dialog", "lower_hull", "B", "The Core Horror comes apart, and the frame around it is already sketching it back together. Beneath the ladder the wrong-way seal line runs on, toward a door with no handle.", [("Follow the severed seal channel", "d_chamber")], {}),
  ("d_chamber", "dialog", "reconstruction_chamber", "B", "Rows of empty recall frames stand in the dark. Each still holds an impression, not a body: a remembered greeting, a hand reaching for a cup of warm tea, an order repeated until its meaning wore away. Behind them, a small seal plate guards the way on.", [("Examine the seal plate", "d_seal1")], {}),
  ("d_seal1", "dialog", "reconstruction_chamber", "B", "First seal. Three seal paths cross the plate. One climbs to the deck seals, one bears the Captain's command mark, and a third turns back beneath the empty frames. Beside the third someone has scratched: 'What command will not mend must first be sealed away.'", [("Trace the return seal beneath the frames", "d_seal2"), ("Force the Captain's command seal", "d_alarm1"), ("Force the deck seals", "d_alarm1")], {}),
  ("d_alarm1", "dialog", "reconstruction_chamber", "N", "The plate flares red. Every empty frame in the room turns toward you, and a Skyglass Sentinel steps out of the nearest one.", [("Fight through the alarm", "b_alarm1")], {}),
  ("b_alarm1", "start_battle", "reconstruction_chamber", "N", "The archive's guard bars the way.", [("", "d_seal2_a")], {"fight": ["Skyglass Sentinel", "Seal Charge"], "debuff": "alarm debuff (type and strength set at calibration)"}),
  ("d_seal2", "dialog", "quarantined_archive", "N", "Second seal. The return path ends at a door with no handle. Pale script crosses it in the Oathkeeper's hand: 'What does every traveler keep while every journey spends it?'", [("Time", "d_seal3"), ("Breath", "d_alarm2"), ("Gold", "d_alarm2")], {"borrowed_riddle": "Oathkeeper's parley"}),
  ("d_seal2_a", "dialog", "quarantined_archive", "N", "Second seal. The alarm still sounds as you reach a door with no handle. Pale script crosses it in the Oathkeeper's hand: 'What does every traveler keep while every journey spends it?'", [("Time", "d_seal3_a"), ("Breath", "d_alarm2"), ("Gold", "d_alarm2")], {"borrowed_riddle": "Oathkeeper's parley"}),
  ("d_alarm2", "dialog", "quarantined_archive", "N", "The script burns out. The door opens, and the archive's guard is already inside.", [("Fight through the alarm", "b_alarm2")], {}),
  ("b_alarm2", "start_battle", "quarantined_archive", "N", "The archive's guard bars the way.", [("", "d_seal3_a")], {"fight": ["Skyglass Sentinel", "Seal Charge"], "debuff": "alarm debuff"}),
  ("d_seal3", "dialog", "quarantined_archive", "N", "Third seal. The index shelf holds three copies of one route: the first ink from the day the ship first sailed, a copy corrected once, and a sheet corrected so many times the paper has gone soft. The Wayfinder's note is pinned above them: 'The route is real. Read it against the newest chart.'", [("Take the most corrected sheet", "d_entry"), ("Take the original ink", "d_alarm3"), ("Take the copy corrected once", "d_alarm3")], {"borrowed_riddle": "Wayfinder's charts"}),
  ("d_seal3_a", "dialog", "quarantined_archive", "N", "Third seal. The index shelf holds three copies of one route: the first ink from the day the ship first sailed, a copy corrected once, and a sheet corrected so many times the paper has gone soft. The Wayfinder's note is pinned above them: 'The route is real. Read it against the newest chart.'", [("Take the most corrected sheet", "d_entry_a"), ("Take the original ink", "d_alarm3"), ("Take the copy corrected once", "d_alarm3")], {"borrowed_riddle": "Wayfinder's charts"}),
  ("d_alarm3", "dialog", "quarantined_archive", "N", "The shelf locks and the index burns white. The archive's guard comes to defend its records.", [("Fight through the alarm", "b_alarm3")], {}),
  ("b_alarm3", "start_battle", "quarantined_archive", "N", "The archive's guard bars the way.", [("", "d_entry_a")], {"fight": ["Skyglass Sentinel", "Seal Charge"], "debuff": "alarm debuff"}),
  ("d_entry", "dialog", "quarantined_archive", "B", "The last seal opens on a narrow room no plan of the ship admits to. Orders, reports and damaged crew impressions were carried down here and filed away, out of command's sight. Their keeper has not yet shown himself.", [("Read the suppressed incident reports", "d_records"), ("Go further in", "d_sealwright")], {}),
  ("d_entry_a", "dialog", "quarantined_archive", "N", "The alarm dies as you cross into the archive, too late to matter. Orders, reports and damaged crew impressions were filed away down here, out of command's sight. Their keeper already knows you are coming.", [("Go further in", "d_sealwright_a")], {}),
  ("d_records", "dialog", "quarantined_archive", "B", "The reports span decades, all in one seal-smith's hand. Each warns that the crew's impressions are fraying: names forgotten, faces filled in wrong, men coming back as less each time. Each asks leave to let them rest. Every answer is the same, sealed in cyan wax under a crown of jagged frost points around one tall central blade, sent down from a fortress called Crownhold: 'Refused. None is relieved.'", [("Confront the archive's custodian", "d_sealwright")], {}),
  ("d_sealwright", "dialog", "quarantined_archive", "B", "An old seal-smith gathers out of the engraved lines, steadier than the broken crew below. A black iron reliquary is chained to the wall behind him. 'I sealed away what I could not mend,' the Sealwright says. 'The crown would not let me stop the work. It will not let you take these records either.' He raises a sealing stance, and he does not look as though he wants to.", [("Challenge the Sealwright", "b_sealwright")], {}),
  ("d_sealwright_a", "dialog", "quarantined_archive", "N", "The Sealwright is waiting, already in his sealing stance. 'You came through my alarms,' he says. 'Then you have seen enough to know what this place is for.'", [("Challenge the Sealwright", "b_sealwright_a")], {}),
  ("b_sealwright", "start_battle", "quarantined_archive", "B", "Break the Sealwright's seals.", [("", "w_clean")], {"fight": ["Sealwright"]}),
  ("b_sealwright_a", "start_battle", "quarantined_archive", "B", "Break the Sealwright's seals.", [("", "w_alarm")], {"fight": ["Sealwright"]}),
  ("w_clean", "win_quest", "quarantined_archive", "N", "Every seal held for you. You leave with the archive's stores, and with one name the Sealwright kept hidden for a lifetime: Crownhold.", [], {"step": "V"}),
  ("w_alarm", "win_quest", "quarantined_archive", "N", "The archive is yours, though the alarms cost you. You leave with what its keeper could not hold, and with one name: Crownhold.", [], {"step": "III"}),
 ],
}

FOUNDRY = {
 "name": "The Drowned Foundry", "chart": "Chart of the Drowned Foundry", "ladder": "V (always fought to the Warden)",
 "premise": "Under the wreck's keel are the works where the Core grows the skyglass that mends the hull. The sea came in when the ship came down, and the works never stopped. The water rises the deeper you go, and the haul is at the bottom: there is no way out but through the crucible. Lose a fight and the flood throws you out, chart and all.",
 "scenes": ["exterior_keel_walk", "lower_hull", "hold"],
 "portraits": [],
 "new_ai": ["Foundry Warden (boss; avatar needed)"],
 "nodes": [
  ("d_arrive", "dialog", "exterior_keel_walk", "N", "Outside, the ship is a wreck on the sand. Inside, the Core still holds every deck the way it was. Beneath them, seal channels feed a hatch rimmed with cooled skyglass. Seawater pours past it into the dark. Somewhere below, something is still being poured.", [("Climb down into the keel works", "d_intake")], {}),
  ("d_intake", "dialog", "lower_hull", "N", "The intake is half flooded. A Deck Warden stands knee-deep in it, counting canisters that bob against the walls. Above his cloth mask his eyes are young; his gear is generations out of date. He loses count, and starts again. 'No one is relieved,' he says, as if reading it from a list.", [("Break the intake guard", "b_intake")], {}),
  ("b_intake", "start_battle", "lower_hull", "N", "The Deck Warden and a Core Canister hold the intake.", [("", "d_racks")], {"fight": ["Deck Warden", "Core Canister"]}),
  ("d_racks", "dialog", "hold", "N", "Cooling racks line the first hall, stacked with fresh skyglass no one has come to collect in years. The water is at your ankles and still rising, and the hatch above has sealed behind you. A stair goes down into the pour halls.", [("Go deeper into the pour halls", "d_hall")], {}),
  ("d_hall", "dialog", "lower_hull", "N", "In the pour hall the Arsenal Keeper is checking a ledger he has checked every day for decades, beside seal charges bound to every mould. Rice that rotted a generation ago is still listed as fresh stores, and every page carries the same request for shore leave, crossed out: crew not relieved. He looks up. 'You are not in the ledger.'", [("Stop the Arsenal Keeper", "b_hall")], {}),
  ("b_hall", "start_battle", "lower_hull", "N", "The Arsenal Keeper sets off his charges.", [("", "d_gate")], {"fight": ["Arsenal Keeper", "Seal Charge", "Seal Charge"]}),
  ("d_gate", "dialog", "lower_hull", "N", "The water is at your knees. The pour hall's best work sits cooling on the moulds, and below it the crucible glows through the floor grates. Whatever keeps the works running is down there.", [("Descend to the crucible", "d_crucible")], {}),
  ("d_crucible", "dialog", "hold", "N", "The crucible chamber is the only dry room in the works, kept dry by heat. The Foundry Warden stands in it, half fused with the pouring frame, a master smelter whose impression never set down his ladle. 'The last pour is not finished,' he says. 'It is never finished.'", [("Face the Foundry Warden", "b_warden")], {}),
  ("b_warden", "start_battle", "hold", "N", "The Foundry Warden tips the crucible.", [("", "d_pour")], {"fight": ["Foundry Warden", "Core Canister"]}),
  ("d_pour", "dialog", "hold", "N", "The Warden cools into a shell of skyglass. The last pour sits unclaimed in its mould, and the works fall silent for the first time since the ship was built.", [("Take the last pour and leave", "w_deep")], {}),
  ("w_deep", "win_quest", "hold", "N", "You carry the last pour out of the keel works. Behind you, the wreck is already starting to mend what you broke.", [], {"step": "V"}),
 ],
}

WATCH = {
 "name": "The Captain's Watch", "chart": "Chart of the Captain's Watch", "ladder": "no terms IV · one or two V · all three VI",
 "premise": "The Captain still keeps the night watch on his broken command deck, and he never refuses a challenger. But the Oathkeeper sets terms: before each fight you may accept a handicap. Every term you take and survive raises the haul. Lose any fight and the watch is over.",
 "scenes": ["cache_site", "chart_room", "deck_b", "helm", "command_observation_gallery"],
 "portraits": ["Oathkeeper", "The Captain"],
 "new_ai": [],
 "terms": [
  ("Term 1, Chart Room (Wayfinder)", "Fight without foreign seal-work", "elementalseal on the player"),
  ("Term 2, Deck (First Blade)", "Meet the First Blade unarmed", "disarm on the player"),
  ("Term 3, Helm (The Captain)", "No healing before the Captain", "healprevent on the player"),
 ],
 "graph_note": "The count of accepted terms is carried by which nodes the player is on: each fight has a node per count so far, with an 'accept' and a 'refuse' battle each (2 + 4 + 6 battle nodes). Counts 1 and 2 end at the same step.",
 "nodes": [
  ("d_landing", "dialog", "cache_site", "N", "The chart's route ends at a cove below the wreck, where the ship's boat is drawn up on the sand, waiting. The Oathkeeper stands beside it, in an officer's coat faded by no weather. 'The Captain keeps the night watch,' he says. 'He will meet you. I set the terms. We have time for terms. We have always had time.'", [("Board the boat", "d_term1")], {}),
  ("d_term1", "dialog", "chart_room", "N", "In the chart room the Wayfinder looks up from decades of corrections to a coastline that keeps moving. 'Still no home port,' he says. The Oathkeeper speaks from the doorway: 'Fight him without your elements, and the Captain will hear of it.'", [("Accept the term", "b1_t"), ("Refuse and fight", "b1")], {"portrait": "Oathkeeper"}),
  ("b1", "start_battle", "chart_room", "N", "The Wayfinder redraws the room around you.", [("", "d_term2_0")], {"fight": ["Wayfinder"]}),
  ("b1_t", "start_battle", "chart_room", "N", "The Wayfinder redraws the room around you. Your seals will not answer.", [("", "d_term2_1")], {"fight": ["Wayfinder"], "debuff": "elementalseal"}),
  ("d_term2_0 / d_term2_1", "dialog", "deck_b", "B/N", "On deck the First Blade waits in the uniform of a dead era, twin cleavers forming from the gale. 'Finally. Something new.' The Oathkeeper: 'Meet him with empty hands.' (One node per count so far.)", [("Accept the term", "b2_t (count +1)"), ("Refuse and fight", "b2 (count unchanged)")], {"portrait": "Oathkeeper"}),
  ("b2 ×2 / b2_t ×2", "start_battle", "deck_b", "B", "The First Blade steps forward.", [("", "d_term3_{count}")], {"fight": ["First Blade"], "debuff": "disarm on the accepted variants"}),
  ("d_term3_0 / _1 / _2", "dialog", "helm", "B/N", "At the helm stands the Captain, almost solid in the light of the Core. Behind the dais the helm's great skyglass ring burns, its heart empty, waiting for something that never comes. 'They built this ship to cross any wall and outlast any siege,' he says. 'No one asked what outlasting everything would cost.' The Oathkeeper: 'No healing at his helm.'", [("Accept the term", "b3_t"), ("Refuse and fight", "b3")], {"portrait": "The Captain"}),
  ("b3 ×3 / b3_t ×3", "start_battle", "helm", "B", "The Captain steps down from the command dais.", [("", "d_gallery_{IV|V|VI}")], {"fight": ["The Captain"], "debuff": "healprevent on the accepted variants"}),
  ("d_gallery_IV / _V / _VI", "dialog", "command_observation_gallery", "B/N", "The Captain lowers his weapon. 'The ship died once. The crown disagreed.' From the gallery you can see the whole wreck mending itself in the dark. He glances back at the empty ring and touches his bare head above the white mask, as if something should sit there. 'I keep his watch,' he says, to no one. 'I wear his mask. He never trusted me with the rest.' The Oathkeeper counts your terms aloud.", [("Claim the watch's stores", "w_IV / w_V / w_VI")], {}),
  ("w_IV", "win_quest", "command_observation_gallery", "N", "You beat the Captain on your own terms.", [], {"step": "IV"}),
  ("w_V", "win_quest", "command_observation_gallery", "N", "You took the Oathkeeper's terms and still beat the Captain.", [], {"step": "V"}),
  ("w_VI", "win_quest", "command_observation_gallery", "N", "Every term, every fight. The Oathkeeper bows: 'The Captain will remember this watch. Few of us remember anything.'", [], {"step": "VI"}),
 ],
}

HUNTS = [ARCHIVE, FOUNDRY, WATCH]
