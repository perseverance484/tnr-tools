# The Haul: profession-themed push-your-luck charts

**Update (RUL-2026-10-29-052):** the Haul is open to **every player**. There is no S-rank gate. Hunter and gatherer pages are themes, not requirements, and the rest of this doc applies as written.

**Status:** APPROVED direction (RUL-2026-10-29-037). Numbers are harness targets until the simulator rounds return.

These two charts are Skyglass's callback to the original S-rank Ghost Ship hunting and gathering quests. Professionals
are rewarded the same, but through a push-your-luck run instead of a flat payout. Both follow every chart rule: the chart is
spent at entry, any lost fight fails the run, health and chakra carry between fights, and the ending pays only what was
won.

## Lore

**The stores.** For decades the war-ship crossed the sky with nowhere to land, so it fed and repaired itself. The ship's
hunters took what the high air and the coastlines offered, and its gatherers cut what grew in the hull. Everything went
into the stores, logged by the Arsenal Keeper, sealed, and **never drawn**, because nobody was ever relieved and nothing
was ever spent. Now the ship lies broken on the shore and the Core is still mending it. The stores are intact, and the
echoes still guard them.

**The ledger.** The Arsenal Keeper's ledger names every locker: what is in it, who sealed it, and the date it was due to be
opened "on relief". Every due date has been crossed out and rewritten, for decades. The crate tags in the run are lines
from that ledger.

### Hunters: "The Trophy Hold"

- **Chart item:** *Ledger Page: The Trophy Hold* (Legendary rarity, tradeable).
  - *Description:* "A page torn from the Arsenal Keeper's ledger. Hides, horn and the hunters' trophies, sealed below the
    gun deck. 'Draw on relief.' Relief is crossed out."
  - Then the rules: S-rank hunting required, chart spent at entry, a lost fight ends the run, health carries over, and you
    may leave after any crate.
- **The place:** a long hold under the gun deck, racks of sealed lockers, trophies mounted on the bulkheads. Cold.
- **The guards:**
  - the ship's old hunting party, crew echoes who still walk the racks;
  - the **Trophy Warden**, a stat copy of the Oathkeeper, who guards the sealed lockers;
  - at high alertness, the **Arsenal Keeper** himself comes down to see who is drawing from his stores.
- **Hazards (the debuffs):** the hunters' old snares and baited lines.
  - wound: torn on a snare;
  - poison: an old bait vial bursts;
  - moveprevent: a line around the ankle;
  - decreasemaxpools: a trophy's cold eyes.
- **Voice of the tags:** short and practical. "Pelts, cured. Sealed by the third hunter. Draw on relief."

### Gatherers: "The Overgrown Stores"

- **Chart item:** *Stores Manifest: The Overgrown Stores* (Legendary rarity, tradeable).
  - *Description:* "The quartermaster's manifest for the lower stores. Ore, root and bloom, cut from the hull and sealed.
    Skyglass has grown through every line since."
  - Then the rules, as above, with S-rank gathering required.
- **The place:** store-rooms the Core has grown through. Skyglass in pale columns, crates set into the crystal like
  stones in a ring.
- **The guards:**
  - **Seal Charges and Core Canisters** set into the growth;
  - the **Stores Ward**, a stat copy of the Crown Archivist, keeping the sealed racks;
  - at high alertness, the **Sealwright's** seal-work flares and his echo seals the room.
- **Hazards (the debuffs):** skyglass dust and growth.
  - elementalseal: dust in the seal channels;
  - increasepoolcost: the growth drinks chakra;
  - decreasemaxpools: crystal in the lungs;
  - afterburn: a cut channel flares.
- **Voice of the tags:** the quartermaster's dry inventory. "Ore, refined, twelve crates. Sealed. Growth noted."

## The run

**Steps:** up to 5. At every step the player sees two or three tags and chooses one, or chooses to **leave**.

| Choice | Adds to the haul | Fight | Hazard |
|---|---|---|---|
| **Crate** (loose, logged) | one chest at the step's base tier | crew guards, scaled to the step | none |
| **Locker** (sealed) | one chest a tier higher | the step's elite guard plus crew | one hazard on the player for the first 2 rounds of this fight |
| **Cut through** (no fight) | one chest a tier lower, minimum Common | none now | the **next** fight opens with a lingering hazard |

The cut-through hazard is poison or decreasemaxpools for hunters, afterburn or increasepoolcost for gatherers.

**Base tier by step:** 1 Common, 2 Common, 3 Rare, 4 Epic, 5 Epic. A locker at step 5 is Legendary.

**Alertness.** Each locker opened raises the hold's alertness by 1, and it never falls during the run.

| Alertness | Effect on every later fight |
|---|---|
| 0 | as built |
| 1-2 | one more crew guard; +1 starting hazard |
| 3+ | the Arsenal Keeper (hunters) or the Sealwright's echo (gatherers) joins the elite fights; +2 starting hazards |

**Leaving.** A "Take what you have and go" choice sits beside every tag. It routes to the win ending for the exact haul.
Finishing step 5 also ends the run.

**Payout.** The haul pays at the ending as plain `reward_items` at 100%: the chests actually taken, from the 8
profession chests (`SKYGLASS_PROFESSION_CHESTS.md`). Nothing pays per fight.

**How the engine holds the state.** A quest has no counters, so the graph encodes the state as its position: step,
alertness, and whether a cut-through hazard is pending.
- Each choice node branches to battle nodes that carry their own `applyDebuffs` and opponents.
- Each "leave" routes to an ending that carries the haul.
- The quest is generated; it is too big to write by hand.
- Different paths can reach the same state with different hauls, so the generator keys each node by state plus a haul
  signature, and folds hauls into value bands to keep the node count down.

## Balance targets (harness)

- **Values:** chest values on the RUL-2026-10-28-033 basis.
  - Hunter's Chests: Common ~4.2M, Rare ~6.1M, Epic ~6.7M, Legendary ~11.5M.
  - Gatherer's Chests: Common ~3.2M, Rare ~4.9M, Epic ~5.4M, Legendary ~10.5M.
  - These are the final tables (`SKYGLASS_PROFESSION_CHESTS.md`, Upgrade tier removed).
  - The old S-rank Ghost Ship endings paid roughly 7-8M a run.
- **A sensible path** (about 3 steps, 1 locker) clears about 85% of the time and averages the old payout, about 7-8M.
- **A greedy path** (5 steps, 3+ lockers) clears 30-40% of the time. A clear pays about 2-2.5× the old payout, so its
  expected value is close to the sensible path's. Greed is variance, not free value.
- **A timid path** (leave after 1-2 crates) clears about 98% of the time and pays clearly less.
- **No dominant path:**
  - every path's expected value sits within about 20% of the sensible path;
  - cut-through is worth it sometimes, not always;
  - a locker at alertness 3+ is a real gamble.
- **Fight lengths:** crates 3-5 rounds, lockers 5-8, Keeper or Sealwright 8-10. A full greedy run takes about 12-15
  minutes.
- **Player model:** a solo S-rank professional at level 100, with the Kitsune set and a pet (RUL-2026-10-28-026 items
  7-8). Both dodging and no-dodging are tested.

## Build

- **New:**
  - the 2 chart items (Legendary, tradeable);
  - about 4 guard copies (Trophy Warden, Stores Ward, and alertness copies of the Keeper and the Sealwright's echo);
  - 2 generated quests, gated by S rank (`huntingRank` / `gatheringRank`) and entered with the chart;
  - no new jutsu.
- **Chart sources:** both drop for everyone and are tradeable. Rates are set with the simulator so S-rank professionals'
  total stays at the old quests' level. Starting candidates: endgame Wreck 3% each, hunt endings 2% each.
- **Lore and text:** tag lines from the ledger and manifest, one per locker or crate per step, written in the story
  bible's voice.

## Variety (RUL-2026-10-29-038)

A quest can't roll randomness mid-run: battles and branches are fixed. So the variety comes from where the engine does
roll: drops, chest openings and reward chances.

1. **Layout variants.** Three pages per profession, each a different part of the stores. The page is picked at random when
   the chart drops (uniform among the three).

   | Profession | Page | Character |
   |---|---|---|
   | Hunters | **The Trophy Hold** | the classic balance |
   | Hunters | **The Bone Store** | lockers early, a cheap but dangerous start |
   | Hunters | **The Snare Room** | heavy hazards, safe cut-throughs |
   | Gatherers | **The Overgrown Stores** | the classic balance |
   | Gatherers | **The Ore Vault** | dense guards, rich lockers |
   | Gatherers | **The Bloom Cellar** | heavy dust hazards, a steep tier curve |

   Variants differ in which steps offer lockers, the guard mix, the hazards and the tier curve, so the best route
   depends on the page.
2. **Steeping (RUL-2026-10-28-010 rules).** A Haul page plus 3 Core Rot steeps into a **Rot-Sealed Page** of that
   same page: a weighted-cache item whose opening rolls one of the 4 modifiers below. The layout is kept: steep the
   Bone Store, get a modified Bone Store. Each page has its own Rot-Sealed Page, because a steeping entry is a fixed
   item (director, 2026-10-29).

   | Modifier | Effect |
   |---|---|
   | **Rot-soaked** | every hazard doubled; every chest one tier higher |
   | **Flooded hold** | moveprevent in every fight; lockers carry no hazard |
   | **Alarmed** | start at alertness 2; a Legendary locker from step 4 |
   | **Picked clean** | easier fights, smaller haul: the gamble's bad roll |

   Weights 30 Rot-soaked / 25 Flooded hold / 25 Alarmed / 20 Picked clean (RUL-2026-10-29-044). A lost steeping fight returns the page, and the Rot is spent.
3. **Bonus chances.** Each locker pays its chest plus a chance at a bonus chest of the same tier (starting at about 20%),
   as a `reward_items` drop chance at the ending. The same route gives different hauls.
4. **Chest rolls.** The 8 profession chests already vary: 3-6 rolls across staples, kits, bulk and windfall.

**Cost:**
- **Items:**
  - 6 page charts (3 per profession);
  - 6 Rot-Sealed Page items (one per page; each opening rolls one of the 4 modifiers, as 4 cache entries);
  - the modified page charts that those openings grant, made on demand by the generator: up to 24.
- **Quests:**
  - 6 base quests;
  - up to 24 modified quests, generated from a modifier pass over the base graphs.

  The harness reports whether the full set is worth its size, or whether some modifiers should apply only to the
  classic layout.
- **No new jutsu.**
