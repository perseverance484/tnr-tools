> **Superseded by** `state/skyglass_hunts/hunts.py` (hunt text, rewritten to the story bible), `SKYGLASS_STORY_BIBLE.md`, `SKYGLASS_LOOT_TABLES.md` and `SKYGLASS_BOSS_FIGHTS.md`, under RUL-2026-10-28-001 … -019. Kept for history; where it disagrees with those files, they win.

# Skyglass treasure hunts — content draft

**Status:** DRAFT for the director (RUL-2026-10-24-020/-021). Borrowed text (B) comes from the live Ghost Ship quest (push/98 capture) or the approved Skyglass graph patch; new text (N) is a first draft. Final prose, debuff strengths and the Foundry Warden are the director's. Generated with the review page from one source.

## The Quarantined Archive

**Chart:** Chart of the Quarantined Archive · **Ladder:** clean V · alarm III · **Scenes:** exterior_keel_walk, lower_hull, reconstruction_chamber, quarantined_archive · **Portraits:** Sealwright · **New AI:** none

A chart marks a chamber missing from every ship plan. Someone aboard the Ghost Ship once tried to quarantine what the Core was getting wrong, and filed it behind three seals. A wrong answer at any seal trips the alarm: you fight the archive's guard, then continue. Answer all three cleanly for the better haul.

| Node | Type | Scene | Src | Text | Next |
|---|---|---|---|---|---|
| `d_arrive` | dialog | exterior_keel_walk | B | The upward seal channels hold the ship aloft. A thinner line runs against their flow, carrying fragments of handwriting and fractured memories toward a sealed section inside the hull. Someone once tried to isolate a failure from the main network. | Follow the breach into the hull → d_hull |
| `d_hull` | dialog | lower_hull | N | Below the waterline the hull is rebuilding itself from timber and cable that do not belong together. Something large is being rebuilt with them, and it is not finished. | Face what the hull is building → b_horror |
| `b_horror` | start_battle | lower_hull | N | The Core Horror pulls itself out of the frame. **vs Core Horror** | → d_conduit |
| `d_conduit` | dialog | lower_hull | B | With the Core Horror defeated, the surrounding frame begins sketching its ruined body again. Beneath the ladder, a severed impression conduit pulses toward a sealed maintenance chamber. | Follow the severed impression conduit → d_chamber |
| `d_chamber` | dialog | reconstruction_chamber | B | Rows of framed seal patterns stand without occupants. Each carries a human impression, not a living body: a remembered greeting, the shape of a hand reaching for warm tea, a command repeated until its meaning has faded. A small maintenance plate is locked behind the frames. | Examine the maintenance plate → d_seal1 |
| `d_seal1` | dialog | reconstruction_chamber | B | First seal. Three seal paths remain on the plate. One rises to the lift network, one bears the Captain's command mark, and a third turns back beneath the inactive frames. Beside the return path someone scratched: 'What command cannot repair must first be quarantined.' | Trace the return seal beneath the frames → d_seal2; Force the Captain's command seal → d_alarm1; Override the lift lattice → d_alarm1 |
| `d_alarm1` | dialog | reconstruction_chamber | N | The plate flares red. Every frame in the chamber turns toward you, and a Skyglass Sentinel steps out of the nearest one. | Fight through the alarm → b_alarm1 |
| `b_alarm1` | start_battle | reconstruction_chamber | N | The alarm guard bars the way. **vs Skyglass Sentinel + Seal Charge** (alarm debuff (type and strength set at calibration)) | → d_seal2_a |
| `d_seal2` | dialog | quarantined_archive | N | Second seal. The return path ends at a door with no handle. Pale script crosses it in the Oathkeeper's hand: 'What does every traveler keep while every journey spends it?' | Time → d_seal3; Breath → d_alarm2; Gold → d_alarm2 |
| `d_seal2_a` | dialog | quarantined_archive | N | Second seal. The alarm still sounds as you reach a door with no handle. Pale script crosses it in the Oathkeeper's hand: 'What does every traveler keep while every journey spends it?' | Time → d_seal3_a; Breath → d_alarm2; Gold → d_alarm2 |
| `d_alarm2` | dialog | quarantined_archive | N | The script burns out. The door opens, and the alarm guard is already inside. | Fight through the alarm → b_alarm2 |
| `b_alarm2` | start_battle | quarantined_archive | N | The alarm guard bars the way. **vs Skyglass Sentinel + Seal Charge** (alarm debuff) | → d_seal3_a |
| `d_seal3` | dialog | quarantined_archive | N | Third seal. The index shelf holds three copies of one route: the first ink from the day the ship vanished, a copy corrected once, and a sheet corrected so many times the paper has gone soft. The Wayfinder's note is pinned above them: 'The route is real. Read it against the newest chart.' | Take the most corrected sheet → d_entry; Take the original ink → d_alarm3; Take the copy corrected once → d_alarm3 |
| `d_seal3_a` | dialog | quarantined_archive | N | Third seal. The index shelf holds three copies of one route: the first ink from the day the ship vanished, a copy corrected once, and a sheet corrected so many times the paper has gone soft. The Wayfinder's note is pinned above them: 'The route is real. Read it against the newest chart.' | Take the most corrected sheet → d_entry_a; Take the original ink → d_alarm3; Take the copy corrected once → d_alarm3 |
| `d_alarm3` | dialog | quarantined_archive | N | The shelf locks and the index burns white. The alarm guard comes for the archive itself. | Fight through the alarm → b_alarm3 |
| `b_alarm3` | start_battle | quarantined_archive | N | The alarm guard bars the way. **vs Skyglass Sentinel + Seal Charge** (alarm debuff) | → d_entry_a |
| `d_entry` | dialog | quarantined_archive | B | The last seal opens a narrow chamber not marked on any ship plan. Command records and damaged crew impressions were moved here and filed as containment faults. Their custodian has not yet appeared. | Read the suppressed incident reports → d_records; Go further in → d_sealwright |
| `d_entry_a` | dialog | quarantined_archive | N | The alarm dies as you cross into the archive, too late to matter. Command records and damaged crew impressions were filed here as containment faults. Their custodian already knows you are coming. | Go further in → d_sealwright_a |
| `d_records` | dialog | quarantined_archive | B | The reports span decades. Each warns that reconstructed patterns are deteriorating while preservation remains mandatory. The same seal-engineer's signature appears on every revision, although no living engineer could have filed them all. The final correction is stamped 'Access refused by command priority.' | Confront the archive's custodian → d_sealwright |
| `d_sealwright` | dialog | quarantined_archive | B | A senior shinobi engineer gathers from the engraved lines, his form steadier than the damaged crew below. 'I sealed the worst of it away,' the Sealwright says. 'Command would not permit me to stop the work. It will not permit you to take these records.' He raises a sealing stance. | Challenge the Sealwright → b_sealwright |
| `d_sealwright_a` | dialog | quarantined_archive | N | The Sealwright is waiting, already in his sealing stance. 'You came through my alarms,' he says. 'Then you know what this place is for.' | Challenge the Sealwright → b_sealwright_a |
| `b_sealwright` | start_battle | quarantined_archive | B | Break the Sealwright's containment defense. **vs Sealwright** | → w_clean |
| `b_sealwright_a` | start_battle | quarantined_archive | B | Break the Sealwright's containment defense. **vs Sealwright** | → w_alarm |
| `w_clean` | win_quest | quarantined_archive | N | Every seal held for you. You leave the archive with its records intact and its stores open, and the Sealwright's work unbroken. **Step V** |  |
| `w_alarm` | win_quest | quarantined_archive | N | The archive is yours, though the alarms cost you. You leave with what the custodian could not keep. **Step III** |  |

## The Drowned Foundry

**Chart:** Chart of the Drowned Foundry · **Ladder:** V (always fought to the Warden) · **Scenes:** exterior_keel_walk, lower_hull, hold · **Portraits:** none · **New AI:** Foundry Warden (boss; avatar needed)

Under the warship's keel are the works where the Core grows and pours the Skyglass that repairs the hull. The seawater got in when the ship fell, and the works kept running. The water rises the deeper you go, and the haul is at the bottom: there is no way out but through the crucible. A lost fight costs time, not the haul.

| Node | Type | Scene | Src | Text | Next |
|---|---|---|---|---|---|
| `d_arrive` | dialog | exterior_keel_walk | N | Beneath the keel, seal channels feed a hatch rimmed with cooled crystal. Seawater pours past it into the dark. Somewhere below, something is still being poured. | Climb down into the keel works → d_intake |
| `d_intake` | dialog | lower_hull | N | The intake is half flooded. A Deck Warden stands knee-deep in it, counting canisters that bob against the walls. 'No one is relieved,' he says, as if reading it from a list. | Break the intake guard → b_intake |
| `b_intake` | start_battle | lower_hull | N | The Deck Warden and a Core Canister hold the intake. **vs Deck Warden + Core Canister** | → d_racks |
| `d_racks` | dialog | hold | N | Cooling racks line the first hall, stacked with fresh Skyglass that no one has collected. The water reaches your ankles and is still rising, and the hatch above has sealed behind you. A stair goes down into the pour halls. | Go deeper into the pour halls → d_hall |
| `d_hall` | dialog | lower_hull | N | In the pour hall the Arsenal Keeper is checking the same ledger he has checked for decades, beside seal charges wired into every mould. He looks up. 'Unlisted personnel.' | Stop the Arsenal Keeper → b_hall |
| `b_hall` | start_battle | lower_hull | N | The Arsenal Keeper sets off his charges. **vs Arsenal Keeper + Seal Charge + Seal Charge** | → d_gate |
| `d_gate` | dialog | lower_hull | N | The water is at your knees. The pour hall's best work sits on the moulds, and below it the crucible glows through the floor grates. Whatever runs the works is down there. | Descend to the crucible → d_crucible |
| `d_crucible` | dialog | hold | N | The crucible chamber is the only dry room in the works, kept dry by heat. The Foundry Warden stands in it, half fused with the pouring gear, a master smelter whose impression never set down his ladle. 'The last pour is not finished,' he says. | Face the Foundry Warden → b_warden |
| `b_warden` | start_battle | hold | N | The Foundry Warden tips the crucible. **vs Foundry Warden + Core Canister** | → d_pour |
| `d_pour` | dialog | hold | N | The Warden cools into a shell of crystal. The last pour sits unclaimed in its mould, and the works fall silent for the first time since the ship fell. | Take the last pour and leave → w_deep |
| `w_deep` | win_quest | hold | N | You carry the last pour out of the keel works. Above you the warship sails on, already starting to rebuild what you broke. **Step V** |  |

## The Captain's Watch

**Chart:** Chart of the Captain's Watch · **Ladder:** no terms IV · one or two V · all three VI · **Scenes:** cache_site, chart_room, deck_b, helm, command_observation_gallery · **Portraits:** Oathkeeper, The Captain · **New AI:** none

The Captain's impression still keeps the night watch, and he never refuses a challenger. But the Oathkeeper sets terms: before each fight you may accept a handicap. Every term you take and survive raises the haul. A lost fight is retried with the same terms.

| Term | Handicap | Debuff |
|---|---|---|
| Term 1, Chart Room (Wayfinder) | Fight without foreign seal-work | elementalseal on the player |
| Term 2, Deck (First Blade) | Meet the First Blade unarmed | disarm on the player |
| Term 3, Helm (The Captain) | No healing before the Captain | healprevent on the player |

The count of accepted terms is carried by which nodes the player is on: each fight has a node per count so far, with an 'accept' and a 'refuse' battle each (2 + 4 + 6 battle nodes). Counts 1 and 2 end at the same step.

| Node | Type | Scene | Src | Text | Next |
|---|---|---|---|---|---|
| `d_landing` | dialog | cache_site | N | The chart's route ends at a cove where the Ghost Ship's boat is drawn up on the sand, waiting. The Oathkeeper stands beside it. 'The Captain keeps the night watch,' he says. 'He will meet you. I set the terms.' | Board the boat → d_term1 |
| `d_term1` | dialog | chart_room | N | In the chart room the Wayfinder looks up from decades of corrections. The Oathkeeper speaks from the doorway: 'Fight him without your foreign seal-work, and the Captain will hear of it.' | Accept the term → b1_t; Refuse and fight → b1 |
| `b1` | start_battle | chart_room | N | The Wayfinder redraws the room around you. **vs Wayfinder** | → d_term2_0 |
| `b1_t` | start_battle | chart_room | N | The Wayfinder redraws the room around you. Your seals will not answer. **vs Wayfinder** (elementalseal) | → d_term2_1 |
| `d_term2_0 / d_term2_1` | dialog | deck_b | B/N | On deck the First Blade waits in the uniform of a dead era, twin cleavers forming from the gale. 'Finally. Something new.' The Oathkeeper: 'Meet him with empty hands.' (One node per count so far.) | Accept the term → b2_t (count +1); Refuse and fight → b2 (count unchanged) |
| `b2 ×2 / b2_t ×2` | start_battle | deck_b | B | The First Blade steps forward. **vs First Blade** (disarm on the accepted variants) | → d_term3_{count} |
| `d_term3_0 / _1 / _2` | dialog | helm | B/N | At the command dais stands the Captain, almost solid beneath the core-link seals. 'They built this ship to cross any wall and outlast any siege,' he says. 'No one asked what outlasting everything would cost.' The Oathkeeper: 'No healing at his helm.' | Accept the term → b3_t; Refuse and fight → b3 |
| `b3 ×3 / b3_t ×3` | start_battle | helm | B | The Captain steps down from the command dais. **vs The Captain** (healprevent on the accepted variants) | → d_gallery_{IV/V/VI} |
| `d_gallery_IV / _V / _VI` | dialog | command_observation_gallery | B/N | The Captain lowers his weapon. 'The ship died once. Skyglass disagreed.' From the observation gallery the whole seal network is visible, already repairing the damage. The Oathkeeper counts your terms aloud. | Claim the watch's stores → w_IV / w_V / w_VI |
| `w_IV` | win_quest | command_observation_gallery | N | You beat the Captain on your own terms. **Step IV** |  |
| `w_V` | win_quest | command_observation_gallery | N | You took the Oathkeeper's terms and still beat the Captain. **Step V** |  |
| `w_VI` | win_quest | command_observation_gallery | N | Every term, every fight. The Oathkeeper bows: 'The Captain will remember this watch.' **Step VI** |  |
