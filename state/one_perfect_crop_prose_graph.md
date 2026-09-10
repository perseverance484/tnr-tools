# One Perfect Crop — frozen prose and logical graph

**Status:** wording/route frozen for implementation. Balance/admin fields and Road Bandit reuse decision are outside this file.  
**Formatting contract:** narration/action in `<i>...</i>`; spoken lines in normal text inside quotes; beat spacing is literal ` <br> <br> `; action choices are unquoted.

Logical IDs below are stable handoff labels. Fable may use these exact IDs as engine objective IDs if valid under the current generated contract; otherwise preserve the mapping exactly.

## O0 — Roadside Wreck

**Logical id:** `opc_o0`

**description**

`<i>A cabbage cart sits crooked beside the country road, one wheel split clean through and half its belongings scattered into the grass. A farmer is already gathering tools and checking the lashings around an improbably healthy mound of cabbages.</i> <br> <br> "If you're a shinobi, I could use another pair of hands. I'm Ittetsu. This harvest is expected at market before the day is out." <br> <br> "The cart was fine this morning. Then a passing wagon threw one stone into exactly the wrong pin, and here we are." <br> <br> <i>Before lifting the last tool back onto the cart, Ittetsu tucks a small folded seed packet securely into his tool roll.</i>`

**choices**
- `Help him get the shipment to market.` -> `opc_g1`

---

## G1 — The Cart

**Logical id:** `opc_g1`

**description**

`"I can repair the wheel properly. Give me enough time and it will carry the crop safely the rest of the way." <br> <br> <i>A proper repair would restore the cart's speed and keep the cabbages protected from the rough road. The sound timber could instead be stripped down into a crude drag-sled that leaves immediately, but the ride would be slower and much harder on the load.</i>`

**choices**
- `Strip it down. We keep moving.` -> `opc_g1_pass`
- `Repair it properly. It will travel better.` -> `opc_f1_1`

## G1 PASS — Sacrifice the Cart

**Logical id:** `opc_g1_pass`

**description**

`<i>Ittetsu dismantles the damaged wheel without hesitation, repurposing the sound timber and ironwork into runners and braces. The result is ugly, slow, and surprisingly sturdy.</i> <br> <br> "Good. I can build another cart after market day. I cannot grow another harvest by sunset."`

**choices**
- `Keep moving.` -> `opc_g2`

---

## F1.1 — A Good Repair

**Logical id:** `opc_f1_1`

**description**

`<i>Ittetsu works quickly and well. Before long the wheel sits straight, the axle turns cleanly, and the repaired cart rolls down the road without a single complaint.</i> <br> <br> "There. Nothing wrong with knowing how to fix what belongs to you."`

**choices**
- `Continue.` -> `opc_f1_2`

## F1.2 — Too Late

**Logical id:** `opc_f1_2`

**description**

`<i>The repaired cart reaches the river crossing intact. The Waystation Keeper is already chaining the loading gate shut while brown water climbs the pilings below.</i> <br> <br> "You just missed the final loaded crossing. River rose faster than expected. Nothing with cargo goes over until it settles." <br> <br> "A good cart. Shame it cannot swim."`

**choices**
- `There is no way to reach market in time.` -> `opc_f1_fail`

**terminal:** `opc_f1_fail` = `fail_quest`

---

## G2 — The Crossing

**Logical id:** `opc_g2`

**description**

`"Last loaded crossing of the day. Water is climbing, so I'm taking half the usual weight and twice the usual trouble." <br> <br> <i>The fee for the cabbage shipment will empty Ittetsu's purse and cost most of the provisions strapped to the sled. A free levee road follows the river toward market, longer but still apparently passable.</i>`

**choices**
- `Pay for the crossing.` -> `opc_g2_pass`
- `Take the old levee road.` -> `opc_f2_1`

## G2 PASS — Pay the Cost

**Logical id:** `opc_g2_pass`

**description**

`<i>Ittetsu counts out every coin, then adds his packed provisions when the Waystation Keeper points out the remaining weight allowance. By the time the shipment crosses, he has little left besides his tools and the clothes on his back.</i> <br> <br> "Expensive crossing." <br> <br> "You could have taken the levee." <br> <br> "I could also have eaten my money. Neither gets the harvest to market."`

**choices**
- `Continue toward market.` -> `opc_g3`

---

## F2.1 — The Cheap Route

**Logical id:** `opc_f2_1`

**description**

`<i>For a while, the old levee road seems like the smarter choice. It is quiet, dry, and empty enough that the loaded cart makes better time than expected.</i> <br> <br> "We are still moving. I'll call that good news while it lasts."`

**choices**
- `Keep going.` -> `opc_f2_2`

## F2.2 — Road Bandit Ambush

**Logical id:** `opc_f2_2`

**description**

`<i>A lone shinobi steps from the trees ahead and plants himself in the middle of the levee. His attention settles immediately on the loaded shipment.</i> <br> <br> "Toll road is for travelers with money. This road is for travelers with something worth taking." <br> <br> "I already dislike this road."`

**choices**
- `Drive him off.` -> `opc_f2_battle`

## F2 battle

**Logical id:** `opc_f2_battle`

- task: `start_battle`
- opponent: exactly 1 Road Bandit
- success -> `opc_f2_3`
- fail -> `opc_f2_battle_fail`
- `opc_f2_battle_fail` = terminal `fail_quest`
- no authored retry path

## F2.3 — False Victory

**Logical id:** `opc_f2_3`

**description**

`<i>The Road Bandit retreats, leaving the road open. Ittetsu checks every rope, every bundle, and finally the cabbages themselves.</i> <br> <br> "Nothing missing. Keep moving."`

**choices**
- `Continue down the levee.` -> `opc_f2_4`

## F2.4 — The Levee

**Logical id:** `opc_f2_4`

**description**

`<i>The road stays peaceful long enough for the fight to feel like the only danger it had to offer. Then somewhere upstream, wood cracks with a sound like a tree splitting.</i> <br> <br> "That was not a tree."`

**choices**
- `Look upstream.` -> `opc_f2_5`

## F2.5 — Delayed Failure

**Logical id:** `opc_f2_5`

**description**

`<i>An irrigation gate gives way upstream, sending a sudden wall of water across the low levee. Ittetsu gets clear, but the loaded cart is swept sideways into the flooded channels before either of you can secure it.</i> <br> <br> "I can repair a cart. I can earn more coin. I cannot sell a harvest that is halfway to the coast."`

**choices**
- `The shipment is lost.` -> `opc_f2_fail`

**terminal:** `opc_f2_fail` = `fail_quest`

---

## G3 — The Accident

**Logical id:** `opc_g3`

**description**

`<i>Beyond the crossing, the route climbs between terraced fields. A section of old retaining wall suddenly gives way, knocking Ittetsu beneath a broken fence rail as the loaded sled shifts sideways on the sloping road.</i> <br> <br> "Well. That's unfortunate." <br> <br> <i>The rail is pressing harder against Ittetsu, while the sled gives another slow scrape toward the edge of the drainage cut.</i>`

**choices**
- `Brace the load.` -> `opc_g3_pass`
- `Pull Ittetsu free.` -> `opc_f3_1`

## G3 PASS — Brace the Load

**Logical id:** `opc_g3_pass`

**description**

`<i>You catch the sled before it reaches the edge and drive its brace into the road. With the shipment secure, it takes only moments to lift the rail and drag Ittetsu free.</i> <br> <br> "Good choice. I was not going anywhere. The harvest was." <br> <br> <i>He tests his leg, finds it usable, and immediately reaches for the hauling rope.</i>`

**choices**
- `Keep moving.` -> `opc_g4`

---

## F3.1 — Heroic Rescue

**Logical id:** `opc_f3_1`

**description**

`<i>You pull Ittetsu free before the fallen stones can shift again. The rescue works perfectly.</i> <br> <br> "The load."`

**choices**
- `Turn back to the sled.` -> `opc_f3_2`

## F3.2 — Too Late

**Logical id:** `opc_f3_2`

**description**

`<i>The sled is already in the drainage cut. You recover what you can, but too much of the harvest is crushed, soaked, or scattered to fulfill the delivery.</i> <br> <br> "You saved me." <br> <br> "I wish the cabbages could say the same."`

**choices**
- `The shipment can no longer be delivered.` -> `opc_f3_fail`

**terminal:** `opc_f3_fail` = `fail_quest`

---

## G4 — The Perfect Cabbage

**Logical id:** `opc_g4`

**description**

`<i>The market road is finally visible ahead when one side restraint snaps loose. A single flawless cabbage tumbles free and rolls toward an irrigation ditch below.</i> <br> <br> <i>Behind you, the main load shifts with a long wooden creak. Nothing has fallen yet, but one of the remaining ropes has started slipping through its knot.</i> <br> <br> "Oh, that is a beautiful one."`

**choices**
- `Hold the load.` -> `opc_g4_pass`
- `Go after it.` -> `opc_f4_1`

## G4 PASS — Hold the Shipment

**Logical id:** `opc_g4_pass`

**description**

`<i>You seize the slipping rope and pull the main load back into place. The runaway cabbage crosses the road below and disappears into the irrigation ditch.</i> <br> <br> "Leave it." <br> <br> "One head is not a harvest."`

**choices**
- `Continue to market.` -> `opc_c1`

---

## F4.1 — The Perfect Catch

**Logical id:** `opc_f4_1`

**description**

`<i>You sprint downhill and catch the runaway cabbage just before it reaches the water. It is completely unharmed.</i> <br> <br> <i>When you turn around, the main load is gone.</i> <br> <br> "Excellent catch." <br> <br> "Now where is the rest?"`

**choices**
- `One perfect cabbage is not the shipment.` -> `opc_f4_fail`

**terminal:** `opc_f4_fail` = `fail_quest`

---

## C1 — Final Approach

**Logical id:** `opc_c1`

**description**

`<i>The shipment is secure again, and the market gate is close enough to hear carts and vendors beyond it. For the first time since meeting Ittetsu, the road ahead looks almost uneventful.</i> <br> <br> "Do not say anything."`

**choices**
- `Keep moving.` -> `opc_c1_1`

## C1.1 — The Boar

**Logical id:** `opc_c1_1`

**description**

`<i>The brush beside the road explodes outward. A large wild boar barrels through the fence, catches the scent of fresh produce, and immediately turns toward the loaded shipment.</i> <br> <br> "Of course." <br> <br> <i>The boar lowers its head and charges.</i> <br> <br> "That one wants the load. Drive it off."`

**choices**
- `Protect the shipment.` -> `opc_c1_battle`

## C1 battle

**Logical id:** `opc_c1_battle`

- task: `start_battle`
- opponent: exactly 1 Harvest Boar
- success -> `opc_c1_win`
- fail -> `opc_c1_fail`
- `opc_c1_fail` = terminal `fail_quest`
- no authored retry path

## C1 WIN

**Logical id:** `opc_c1_win`

**description**

`<i>The Harvest Boar finally turns and crashes back through the brush. Ittetsu checks the load, tightens one rope, and points toward the market gate.</i> <br> <br> "Good. Keep moving before the sky learns what we're carrying."`

**choices**
- `Enter the market.` -> `opc_d1`

---

## D1 — Market Arrival

**Logical id:** `opc_d1`

**description**

`<i>The battered shipment rolls into market looking as though it has survived a small war. A Market Clerk watches Ittetsu approach, looks at the cabbages, then looks back at Ittetsu.</i> <br> <br> "Ittetsu." <br> <br> "Count them."`

**choices**
- `Wait for the count.` -> `opc_d2`

## D2 — Delivery Accepted

**Logical id:** `opc_d2`

**description**

`<i>The Market Clerk inspects the surviving load, checks the delivery slate, and marks the shipment received.</i> <br> <br> "Shipment accepted. Your delivery is complete." <br> <br> "Complete?" <br> <br> "Complete."`

**choices**
- `Let that sink in.` -> `opc_d3`

## D3 — One Quiet Moment

**Logical id:** `opc_d3`

**description**

`<i>Ittetsu stares at the accepted shipment for several seconds. His shoulders finally drop.</i> <br> <br> "There." <br> <br> "Done."`

**choices**
- `...` -> `opc_d4`

## D4 — The Catastrophe

**Logical id:** `opc_d4`

**description**

`<i>A sudden gust catches a market awning and tears one support loose. The falling pole startles a pack animal, which kicks an empty handcart downhill into the newly accepted cabbage stack.</i> <br> <br> <i>The stack collapses. Cabbages scatter across the market, bounce down the sloping street, and pour almost ceremonially into the drainage canal.</i> <br> <br> "MY CABBAGES!"`

**choices**
- `Survey the damage.` -> `opc_d5`

## D5 — One Survivor

**Logical id:** `opc_d5`

**description**

`<i>When the noise finally stops, Ittetsu finds his battered tool roll beneath an overturned basket. The folded seed packet inside has been torn open, but one seed remains caught in the paper crease.</i> <br> <br> "It was received before all this. The mark on the slate stands." <br> <br> "Yes." <br> <br> <i>Ittetsu looks from the surviving seed to the canal, then places it in your hand.</i> <br> <br> "Keep it. Apparently it likes you better."`

**choices**
- `Take the seed.` -> `opc_win`

## PASS — One Perfect Crop

**Logical id:** `opc_win`

- task: `win_quest`
- completion text: `<i>Ittetsu and the shipment reached their destination. What happened after that is, thankfully, the market's problem.</i>`
- guaranteed reward item: `Cabbage Seed x1`
- all other reward numbers remain content-admin owned until explicitly supplied.

---

# Scene-family wiring

Every dialog has an explicit scene background and scene-character list.

- `opc_o0`, `opc_g1`, `opc_g1_pass`, `opc_f1_1`, `opc_g3`, `opc_g3_pass`, `opc_f3_1`, `opc_f3_2`, `opc_g4`, `opc_g4_pass`, `opc_f4_1`, `opc_c1`, `opc_c1_1`, `opc_c1_win`:
  - background: `Forsworn Scene BG - Pass Road Dusk` (`nmrMHmz9xWojzyIV2mAR8`)
  - character: created Ittetsu scene asset from `@img:one_perfect_crop_ittetsu_scene.webp`

- `opc_f1_2`, `opc_g2`, `opc_g2_pass`:
  - background: `Forsworn Scene BG - Waystation Door` (`kmDsQUEHSub9GIX5ulO6i`)
  - characters: created Ittetsu + created Waystation Keeper from `@img:one_perfect_crop_waystation_keeper_scene.webp`

- `opc_f2_1`, `opc_f2_2`, `opc_f2_3`, `opc_f2_4`, `opc_f2_5`:
  - background: `Forsworn Scene BG - East Road Ambush Site` (`E4VJ-IeIQMwbmGGfKc-sn`)
  - Ittetsu on all five
  - Road Bandit scene character additionally on `opc_f2_2` only, from `@img:one_perfect_crop_road_bandit_scene.webp`

- `opc_d1`, `opc_d2`, `opc_d3`, `opc_d4`, `opc_d5`:
  - background: `BustlingTownMarket` (`cYu6VwVX55m6uq1oxlWc1`)
  - characters: created Ittetsu + `DM Mission Clerk` (`XsLLy8awDAtaE6hXVIi_0`)

Do not add a Harvest Boar scene character. The animal is narrated immediately before its `start_battle`.
