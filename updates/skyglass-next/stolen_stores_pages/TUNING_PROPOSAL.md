# Stolen Stores weekend (Nov 20): tuning proposal, ranked

Grounded in the Nov 13 weekend as logged to 03:06Z Nov 14 (watch shelved after that; Monday's final report may move
these): about 6 to 9 event players, all solo but one team of 3. Skyglass floors 1-3 cleared in 2-4 rounds; floor 4
taught by its omens; boss solo 0 of 7 (before and after tuning), team 1 of 1. Faded soloed by one L50 in ~6 min.
Watch Log pages 0 of 5 finished, trades 0 bought, new charts 0 run. Lobby invites 0 of 3; teams formed on their own
in sector 210. Players re-run straight after losses.

## Ship by Wednesday (top 3)

1. **Pages a player can finish in one weekend, led by the salvage loop.**
   What players do: Stolen Stores (81+) opens with "Win any of the Salvager's trades once", so the first order spends
   the salvage they already earn on a chart. Crew charts and haul rooms drop from 2 wins to 1.
   Why: 81+ charts come almost only from Skyglass clears, and solos aren't clearing the boss, so orders 3-5 need the
   trades to be reachable. Nobody has bought a trade yet; the page should be the tutorial for them.
   Cost: objective and text edits on Stolen Stores, already in this manifest. Fits Wednesday: yes.
   Manifest change: j3_low_decks becomes j3_trade (trades t_deck/t_hold/t_sealed/t_lantern, value 1, Tide Chart +
   3 salvage kept; a deck chart costs 4 salvage, so the low decks stay one trade away); j3_charts and j3_haul
   value 2 -> 1; description lines regenerated. The 30-80 page already has a trade order.

2. **A stamp for finishing the page.**
   What players do: finish all five on either band's page and get a "Stolen Stores" badge with the Skyglass Token.
   Why: a visible mark that the weekend was done, and the start of a collection (one badge per page). Costs nothing
   in balance.
   Cost: 1 badge record (Forge can create badges) and 1 painted icon; reward_badges on both pages' final reward.
   Fits Wednesday: yes; a stand-in icon works if the painting isn't ready.

3. **A set time to meet, named in the Discord post.**
   What players do: "Wreck night: Saturday 8 PM CT, sector 210" in Friday's thread; Monday's post names the first team
   clear and the first page finished.
   Why: lobby invites were ignored, but players grouped on their own in sector 210, and the only boss clear was a
   team. A time pulls 6 to 9 players into the same hour.
   Cost: two lines in the Friday thread, one Monday post. Nothing in the game. Fits Wednesday: yes.

## Not this weekend
4. **Floors with teeth** (second wave after the opening AoE on Skyglass 1-3): needs a dungeon edit, which Forge
   refuses; needs the connector working. Medium.
5. **Tougher Faded floor 4** (one L50 one-shot it): one data point; wait for Monday. Small AI edit.
6. **Weekly tide** (start-of-fight buffs on chart runs, doubled salvage): edits live chart runs midweek, which strands
   open attempts. Medium. Nov 27 at the earliest.
7. **Rare echo ambush** (2% on dailies, unique drop): new AI, avatar and badge, untested by Wednesday. Small to medium.
8. **Echo Duelists** (PvP-style chart run): medium; a later headline.
9. **Solo boss**: still 0 of 7. Decide team-only or more tuning after Monday's report.

## Icon prompt (only if 2 is picked; attach ref_chart_drowned_foundry.png for style)
Stolen Stores badge. Game badge icon in the same hand-painted style as the attached icons: a small round seal of
dark blue-black wax pressed over the lid of a dented tin ration box, the seal stamped with a simple ship's wheel, one
pale cyan skyglass fleck set in the wax. Thick dark ink outlines, cel shading with a few highlight steps, cool
blue-black and dull tin palette with one pale cyan accent. Single object, centered, small even margin, square
1024x1024, transparent background. No readable text, letters or numbers, no UI, no frame, no surface or shadow, no
glow halo, no second object.
