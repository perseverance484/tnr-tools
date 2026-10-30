# Skyglass event — loot tables

> **Tiers and terms (RUL-2026-10-29-058).**
> - **Item rarity** uses the game's four: Common, Rare, Epic, Legendary.
>   - Common charts: Tide, Roster.
>   - Rare charts: Buried Cache, Foundry, Archive, Watch.
>   - Epic charts: Reliquary Seal, Last Heading.
>   - Legendary charts: tainted, Lantern, Haul pages.
> - **Cache tiers** are named Common, Rare, Epic, Legendary, plus **Forbidden** above Legendary (red), each name used once.
>   - Forbidden is used by the Sage's Strongbox (Forbidden Jutsu Scrolls) and the Archive Chart Case (Lastlight Lantern).
> - **Player-facing text** names a chart by its tier ("a Rare chart", "an Epic chart"), never "hunt": hunting is a separate game mechanic.
> - Older wording in this doc ("hunt charts", "rare charts", "hunts") is internal shorthand: hunt charts are the Rare charts, and "rare charts" are the Epic charts.

**Status:** Structure ruled by RUL-2026-10-25-002 and the balance pass RUL-2026-10-25-004, amended by RUL-2026-10-28-009 … -019 (later rulings supersede earlier ones). Weights and quantities below are proposals unless marked ruled; currency amounts are set by the director in game (RUL-2026-10-24-019). Consumable-cache weights and quantities wait on the push/323 item capture (RUL-2026-10-28-018).

**Rule: every item has one home.** A reward appears in more than one source only as the same container, never as loose contents. Skyglass items come only from the Skyglass Coffer, with one exception: Crownhold's pick offers one Fragment of the Skyglass Crown directly (RUL-2026-10-28-003, recorded as an exception by RUL-2026-10-28-010).

## 0. Every item explains itself (RUL-2026-10-28-020)

Each Skyglass item's description tells the player what the item is for, in plain words, after one line of story voice.
- **Charts and the Lantern:** which run it opens; that the chart is spent at entry; that a lost fight ends the run; that health and chakra carry between fights; the press-on choice, on runs that have one (RUL-2026-10-30-060 item 6); for rares, that steeping can twist them.
- **Core Rot:** what steeping is, where it happens, the cost (a rare chart plus 3 Rot), and the outcome on a win (tainted chart) and on a loss (the chart comes back, the Rot is spent).
- **Tainted charts:** the twists, and that the run pays pick 2.
- **Chests, every one:** what can drop and how common each tier is, with the real weights (e.g. "Common 69% · Rare 24% · Epic 5% · Legendary 2%"), the roll count, and any fixed reward (e.g. the Treasury's 150,000 ryo).
- **The Little Horror's Jar:** the pet; that a full collection blocks opening.
- **Skin tokens:** which skins the token unlocks, that the player must own the base weapon, and that each skin unlocks once per player.
- **Galley Stores:** the pet exp goes to the active pet only, so the pet must be battle-ready and not on a task.
- **The Wreck's text:** it tells players the wreck drops charts, which lead to treasure hunts.

Descriptions are generated from the same tables the caches are built from, so the stated rates always match the live weights.

**Chest description format (RUL-2026-10-28-030).** Item descriptions render basic HTML (theninjarpg `utils/parse.ts` parseHtml). The item card already shows the cache's display name and roll odds (`layout/ItemWithEffects.tsx` ~1341), so the description adds the tiers and items:

```html
<i>One line of story.</i><br><br>
<b>Always:</b> 150,000 ryo<br>            (only when the item has a fixed reward)
<i>3–6 rolls.</i><br>                       (only when the roll count varies)
<b>Each roll:</b><br>
<span style="color:#9ca3af"><b>Common 69%</b></span> · Item ×n<br>
<span style="color:#3b82f6"><b>Rare 24%</b></span> · Item ×n<br>
<span style="color:#a855f7"><b>Epic 5%</b></span> · Item<br>
<span style="color:#f59e0b"><b>Legendary 2%</b></span> · Item
```

- A tier with several options joins them with " *or* ".
- A tier with more than 3 options lists the first three, then "and more".
- Each tier name appears at most once per cache, in order of weight. **Forbidden** (red, `#ef4444`) sits above Legendary (RUL-2026-10-29-058).
- A fixed roll count is not repeated, because the card already shows it.
- The rendering is checked on the director's phone through a hidden test item before release.

## 1. Who owns what

| Container / item | Owns | Found in |
|---|---|---|
| Skyglass Coffer | every Skyglass item | Captain's Watch pick (×1); Sealed Reliquary and The Fall picks (×2); Crownhold pick (×3); chest of chests Epic; Crown's Hoard |
| Sealed Treasury | 150,000 ryo on every opening + 3/4/6 rolls of Imperial Gold, Rare Jewels, Unobtanium (RUL-2026-10-28-012) | Endgame Wreck clear 3%; every hunt ending at 1% per ladder step (ruled); Sealed Reliquary and The Fall picks; chest of chests Legendary; Crown's Hoard |
| Archive Chart Case | the hunt charts, the Lantern and the rare charts | Quarantined Archive pick; Sealed Reliquary pick (×2); chest of chests Epic |
| Medicine Inro | healing and self-buff consumables, 2 rolls (§3a) | Low Tide Run, Night Watch, Buried Cache and Foundry picks; chest of chests Common |
| Sage's Strongbox | enemy-alchemy consumables (§3a) | Quarantined Archive pick; chest of chests Rare |
| Elemental Tool Pouch | throwing consumables and Elite Smoke Bombs, Elemental Kunai on every opening (§3a) | Drowned Foundry pick; chest of chests Common |
| Common charts as picks | Watch Roster, Tide Chart, Chart of the Drowned Foundry (§4a) | Low Tide Run, Night Watch and Buried Cache picks (RUL-2026-10-29-042) |
| Galley Stores | pet experience (§5b) | Easy Wreck clear 10%; Low Tide Run, Night Watch, Buried Cache and Foundry picks; The Fall pick (×3); chest of chests Rare |
| Skyglass Token | unlocks any one Skyglass skin (§5d) | Archive, Watch, Sealed Reliquary and The Fall picks; chest of chests Legendary; Crown's Hoard (RUL-2026-10-29-049) |
| Trophy tokens | each unlocks one boss skin (§5d) | the Wreck bosses (5%, once per player, RUL-2026-10-30-060); chart and hunt bosses (1% hunts, 2% rares, 4% tainted); Walked Every Deck (Crownbreaker) |
| The Little Horror's Jar | the event's one pet (§5b) | endgame Wreck clear, once per player, 5% (RUL-2026-10-29-054) |
| Crown's Hoard | opens the Skyglass Coffer and Sealed Treasury caches together, plus a Skyglass Token (RUL-2026-10-28-013, -049) | Crownhold pick |
| Core Rot | steeping reagent (§5) | Endgame Wreck clears, the common runs, the Core Horror's hunt runs, breaking the seal, a failed rare run (§5) |
| Charts / Lastlight Lantern | hunt access (§5) | Wreck clear drops, the chart ladder, the Archive Chart Case |
| Unmarked Cargo (chest of chests) | one roll of the caches above (§2) | Endgame Wreck clear 10% |

**Retired (RUL-2026-10-28-016):** the Armory Requisition is removed entirely: out of the chest of chests, its live record hidden in push/319. **Shelved:** its Special quest (icon kept in `art/skyglass_event_icons/` unused); Lion Token as a Wreck drop.

## 2. Wreck clear (each member)

**Endgame Wreck.** Currency package (director, in game). Independent drops:
- the chest of chests **10%** (RUL-2026-10-25-014; one roll, reweighted by RUL-2026-10-28-016/-018): Common 40 Medicine Inro or Elemental Tool Pouch / Rare 35 Sage's Strongbox or Galley Stores (RUL-2026-10-29-042) / Epic 18 Skyglass Coffer or Archive Chart Case / Legendary 7 Sealed Treasury or Skyglass Token (RUL-2026-10-29-049); **Unmarked Cargo**, untradeable;
- Chart of the Buried Cache **20%** (RUL-2026-10-25-012), Chart of the Drowned Foundry **12%**, Chart of the Quarantined Archive **6%**, Chart of the Captain's Watch **6%**, Lastlight Lantern **3%**, Sealed Treasury **3%** (ruled);
- Tide Chart **15%**, Watch Roster **10%** (RUL-2026-10-28-009);
- Core Rot **15%** for the Core Horror's floor (RUL-2026-10-28-009). Dungeon rewards carry no AI drops, so this is a clear drop, not a drop on the Core Horror record.

**Easy (level 40-60) Wreck.** Tide Chart **25%**, Watch Roster **15%**, Chart of the Buried Cache **5%** (the Buried Cache scales to the player, RUL-2026-10-28-010), Galley Stores **10%** (RUL-2026-10-28-013). The higher common-chart rates are deliberate: the easy Wreck should give a chart without many repeats (RUL-2026-10-28-019).

## 3. Caches (weighted, one roll each unless stated)

**Skyglass Coffer** — the only source of Skyglass items.

| Tier | Weight | Gives |
|---|---|---|
| Common | 69 | Skyglass Filament ×2 |
| Rare | 24 | Skyglass Serum ×3 |
| Epic | 5 | Fragment of the Skyglass Crown ×1 |
| Legendary | 2 | Skyglass Katana ×1 (ruled) |

The Skyglass Crystal is not in the Coffer: it comes only from crafting 12 Skyglass Filaments (live), about nine Coffers' worth (RUL-2026-10-25-004).

**Sealed Treasury** (premium; reworked by RUL-2026-10-28-012). Two effects on one item:
- a standard reward of **150,000 ryo** on every opening;
- a weighted cache with a random roll count: **3 rolls 60 / 4 rolls 30 / 6 rolls 10**.

| Tier | Weight | Gives |
|---|---|---|
| Common | 45 | Imperial Gold ×5 |
| Rare | 35 | Rare Jewels ×10 |
| Epic | 15 | Imperial Gold ×15 |
| Legendary | 5 | Unobtanium ×5 |

That averages about 13 Imperial Gold per opening, against about 1.2 before.

**Archive Chart Case** (reweighted towards sustain, RUL-2026-10-29-040; Legendary tier per RUL-2026-10-28-013)

| Tier | Weight | Gives |
|---|---|---|
| Common | 45 | Chart of the Drowned Foundry ×1 |
| Rare | 25 | Chart of the Quarantined Archive ×1 |
| Epic | 20 | Chart of the Captain's Watch ×1 |
| Legendary | 7 | an Epic chart ×1 (Reliquary Seal or The Last Heading) |
| Forbidden | 3 | Lastlight Lantern ×1 |

Haul pages, tainted charts and the common charts (Tide, Roster, Buried Cache) stay out of the case (RUL-2026-10-29-040).

**Crown's Hoard** (RUL-2026-10-28-013, RUL-2026-10-29-039, -049): one item with a Skyglass Coffer roll, a Sealed Treasury roll (its fixed ryo plus its rolls) and a Skyglass Token ×1.

The Medicine Inro, Sage's Strongbox and Elemental Tool Pouch contents are in §3a (RUL-2026-10-29-042). The Elemental Tool Pouch remains the single pouch (the Katon pouch record, re-pointed; RUL-2026-10-28-003) and gives Elemental Kunai on every opening.

## 3a. Consumable caches: three caches (RUL-2026-10-29-042; supersedes the five-cache split of RUL-2026-10-28-018)

The five-way split is undone:
- The **Officer's Pill Case** merges back into the Medicine Inro, because the Inro's healing half was one good pill and filler.
- The **Quartermaster's Kit** is dropped (worth ~0.04M); its Elite Smoke Bombs return to the Pouch.
- Neither new record was ever built.

Finished, profession-crafted consumables are allowed (RUL-2026-10-28-018). The single Elemental Kunai replaces the old elemental kunai.

The tables are the original pre-split tables with their original quantities (RUL-2026-10-28-033), less pure filler:
- the Inro is RUL-2026-10-25-012's two-roll table;
- the Strongbox keeps the RUL-2026-10-28-033 ×2 cap on its Legendary tier, which again includes the Solider Pill;
- the Pouch is RUL-2026-10-28-003's table without Smoke Pellet and Whetstone Oil.

Values are market prices where the director has shown sales (2026-10-29), otherwise the RUL-2026-10-28-033 basis:
- Elemental Kunai ~300k (sold auctions from 150k to 1.45M; median 300k);
- Small Health Pill ~450k;
- Chakra Pill II and Stamina Pill II ~125-150k.

| Cache | Common | Rare | Epic | Legendary | Value |
|---|---|---|---|---|---|
| Medicine Inro (2 rolls) | 70: Field Tonic / Chakra Pill / Stamina Pill ×10 | 22: Small Health Pill / Dr. Kim's Miracle Potion / Panacea ×10 | 7: Chakra Pill II / Stamina Pill II ×10 | 1: Pill Pack ×5 | ~1.4M |
| Sage's Strongbox (1 roll) | 65: Dr. Kim Disaster Potion / Chakra Disrupting Needles ×20 | — | 26: Infernum / Bashōsen / Dr. Kim's Poison Potion ×10 | 8: Solider Pill / Enemy Pill / Mona's Mermaid Song ×2; Forbidden 1: Forbidden Jutsu Scroll (Nexus / Rebirth) ×1 | ~4.2M |
| Elemental Tool Pouch (Elemental Kunai ×10 always, + 1 roll) | 70: Elemental Kunai ×10 / Venom Cask ×10 | 25: Elemental Kunai ×20 / Elite Smoke Bomb ×10 / Paper Bombs ×10 | 5: Elemental Kunai ×30 / Senbon Needles ×10 / Saki ×10 | — | ~5.5M |

- **The Pouch keeps Elemental Kunai ×10 on every opening** (RUL-2026-10-29-043). At ~5.5M it out-pays the Archive's Strongbox; the Foundry is the kunai run.
- Field Tonic has no price and no recipe in the capture, so it is valued at 0.
- **Dead Man's Draught is not used.** Skyglass Serum (Coffer) is its live successor.
- Placement: §1 and §4a.

## 4. Treasure hunts

Every hunt is an isolated Battle Pyramid. **Ending rewards** (always paid, every ending): the 1,000-5,000 exp ladder by final opponent and gating, the hunt's currency (director, in game) and the Sealed Treasury at **1% per ladder step** (I 1% · II 2% · III 3% · IV 4% · V 5% · VI 6%). No caches on endings. Chart drops on endings follow the chart ladder (§5). The **completion pick** is the hunt's identity; the final pick table is §4a.

Ladder per ending: Low Tide Run I; Night Watch II (III if pressed on); Foundry V (always fought to the Warden; the leave-early endings are removed, RUL-2026-10-25-004); Archive clean V / alarm III (left as is, RUL-2026-10-28-016); Watch no terms IV / one-two V / all VI; Sealed Reliquary, The Fall and the tainted runs VI; Crownhold VI. Exp I-VI = 1,000 / 2,000 / 3,000 / 4,000 / 5,000 / 5,000; Treasury chance = step number %.

The badge and the jutsu in Crownhold's pick grey out once held (the game blocks picking content a player already has), so a player needs at least two Crownhold clears to take both. Badge and jutsu are still to be designed.

The Sealwright's doubled health (push/252) applies to the Archive's final fight too, solo; accepted (RUL-2026-10-25-004).

## 4a. Completion picks: final (RUL-2026-10-28-016, ladder RUL-2026-10-28-034; supersedes every earlier pick table)

**Pick 1 on every run; tainted runs pick 2.** Difficulty scales through option quality and quantity, not pick count.

| Run | Options (pick 1) |
|---|---|
| Low Tide Run | Medicine Inro / Galley Stores / Watch Roster |
| Night Watch | Medicine Inro / Galley Stores / Tide Chart |
| Buried Cache | Medicine Inro / Galley Stores / Chart of the Drowned Foundry |
| Drowned Foundry | Elemental Tool Pouch / Medicine Inro / Galley Stores |
| Quarantined Archive | Archive Chart Case / Sage's Strongbox / Skyglass Token |
| Captain's Watch | Skyglass Coffer / Captain's Purse (1,000,000 ryo) / Skyglass Token |
| Sealed Reliquary | Skyglass Coffer ×2 / Sealed Treasury / Skyglass Token ×2 / Archive Chart Case ×2 |
| The Fall | Skyglass Coffer ×2 / Sealed Treasury / Skyglass Token ×2 / Galley Stores ×3 |
| Tainted runs | **pick 2** from their rare's options; Lantern 30% and Core Rot 40%. No guaranteed drops: the second pick is the appeal (RUL-2026-10-28-019) |
| Crownhold | Crown's Hoard / Skyglass Coffer ×3 / Crownbreaker badge / Crownhold jutsu / Crown Fragment (RUL-2026-10-28-017, RUL-2026-10-29-050) |

The rares double the Watch's Coffer, so each rung pays more than the one below it. Value ladder of each run's best item option (RUL-2026-10-28-033 basis): common runs ~1.4M (Inro, or the other common chart) < Buried Cache ~1.4M (Inro, or a Foundry chart) < Foundry ~5.5M (Pouch, kept by RUL-2026-10-29-043) < Archive ~4.2M (Strongbox) < Watch (Coffer) < rare runs (Treasury ~8M, Coffer ×2) < tainted (pick 2) < Crownhold (unique pieces). Ryo appears only as the Watch's Captain's Purse (RUL-2026-10-28-034). The common runs' chart options make them feed each other, and the Buried Cache feeds the Foundry (RUL-2026-10-29-042).

Cut and not to be rebuilt: every ryo card except the Watch's Captain's Purse (RUL-2026-10-28-034); the Archive's Records exp, the Watch's Inro ×3, The Fall's Captain's Purse, the commons' exp cards (RUL-2026-10-28-016); Crownhold's Honor and Crownhold's Echo Jar ×2 (RUL-2026-10-28-017); the tainted runs' guaranteed Sealed Treasury and Echo Jar (RUL-2026-10-28-019).

## 4b. Profession rewards: the Haul (RUL-2026-10-29-035, -037, -052, -053)

- **Shared hunts carry no profession drops.** Every player gets the same rewards from the same run.
- **The Haul** (`SKYGLASS_THE_HAUL.md`) is where the profession chests come from.
  - Six Legendary Haul pages: three hunter-themed, three gatherer-themed.
  - It is **open to every player**, with no rank gate (RUL-2026-10-29-052).
  - Its endings pay Hunter's or Gatherer's Chests as plain `reward_items`. The chests need no huntable/gatherable flags.
- **Page drops,** per page (RUL-2026-10-29-053):
  - endgame Wreck clear **2.4%**;
  - every Rare chart ending **1.5%**.
  - These rates are from RUL-2026-10-30-060 item 5, replacing 2% and 1.25%. They target about 1.5 Haul runs a dedicated weekend; the final pass measured 1.26 at the old rates.
  - Pages are tradeable.
- **The chests' rarity matches their contents** (RUL-2026-10-28-023 item 1, kept).
- **Chest content fixes** (RUL-2026-10-29-035):
  1. The Common Gatherer's Chest swaps Rust Ferret Pelt (a hunted material) for Copper Ore (gathered, used by Repair Kits).
  2. Frostbite Leaf, which no recipe uses, is removed.
  3. Contents are weighted by recipe demand from the push/325 capture.

  Not changed:
  - Imperial Gold is not added.
  - Heart of Kaeruun is excluded; it has its own pyramid source.

## 5. Charts: the map system (RUL-2026-10-28-009)

PoE-style maps: farming the Wreck drops charts, and each chart opens an isolated high-stakes run.

**Every chart run**
- The chart is an entry item, spent when the run starts.
- Losing any fight fails the run (`failObjectiveId`).
- Health and chakra carry between fights; there are no refills.
- Rewards bank at each fight. On a run with a press-on room, the player picks at the last landing: leave with what they hold, or press on into a final room whose reward is lost on a fall.
- **Press-on rooms** (RUL-2026-10-30-060 item 6, after RUL-2026-10-28-026 item 10): kept on the Night Watch, the Captain's Watch, The Fall and the Rotted Reliquary. Cut from the Low Tide Run, the Quarantined Archive, the Sealed Reliquary and the Burning Heading, which end at their last fight.

**Common charts** (`opponent_scaled_to_user`, so they serve L40 and L100 alike)
| Chart | Run | Shape |
|---|---|---|
| Tide Chart | The Low Tide Run | the tide opens a breach in the lower hull; 3 quick fights against scaled crew, with the Sentinel's Tide Line set piece |
| Watch Roster | The Night Watch | your name on the duty roster; hold the post through 3 waves back to back. The press-on room is the Second Watch. Ends with you relieving the Deck Warden |

**Rare charts** (drop only from hunts and the Archive Chart Case)
| Chart | Source | Run |
|---|---|---|
| Reliquary Seal | Archive | **The Sealed Reliquary**: the echoes the Core could not hold. Foundry Warden, Sealwright and Sentinel back to back, then a last echo: the First Blade (RUL-2026-10-28-013). (Named apart from the retired Skyglass Reliquary item, RUL-2026-10-24-024.) |
| The Last Heading | Watch | **The Fall**: the Wayfinder's final course. The Core replays the night the ship came down: burning decks, then the Core Horror as it breaks |

**Chart ladder** (each run can drop the next chart up)
| Source | Drops |
|---|---|
| Easy Wreck clear | Tide 25% · Roster 15% · Buried Cache 5% (§2) |
| Endgame Wreck clear | Tide 15% · Roster 10% · the rest of the §2 table |
| Low Tide / Night Watch ending | Buried Cache chart 10% |
| Buried Cache ending | Foundry chart 15% |
| Foundry ending | Archive chart 10% |
| Archive ending | Reliquary Seal 25% (RUL-2026-10-28-010; its press-on room and the +20% are cut, RUL-2026-10-30-060) |
| Watch ending | The Last Heading 25%, +20% from its press-on room |
| Crownhold ending | one of the two rare charts 50% |
| Sealed Reliquary / The Fall ending | Lastlight Lantern 15% |
| Archive Chart Case | Legendary: Lantern 3 / rare chart 7 (§3) |

**Tainted rares** (rares only). Harder upgrades of their counterpart; target clear rate about 55%, against about 80% for the base rare. Rewards: §4a (pick 2, Lantern 30%, Core Rot 40%, no guaranteed drops; RUL-2026-10-28-019). (Their doubled trophy rate is deferred with the trophies, RUL-2026-10-29-041.)
- **The Rotted Reliquary** (tainted Reliquary Seal)
  - The echoes fight in pairs: Foundry Warden + Sealwright, then Sentinel + the last echo.
  - Entry at 70% pools (`givePools`).
  - Elemental seal on the player for the first 2 rounds of every fight (`applyDebuffs`).
  - Press-on room: Replicant Zero (RUL-2026-10-28-013; this replaces the Core Horror room of RUL-2026-10-28-010). It is optional and paid extra.
- **The Burning Heading** (tainted Last Heading)
  - Runs backwards: it starts at the Core Horror as the ship breaks, entered at 70% pools, then fights out through the decks with no refill.
  - Afterburn on the player at the start of every fight.
  - The Captain fights beside the player (`allyAIs`) only after the Core Horror falls.
  - The Wayfinder duels at the gangway.

**Getting a tainted chart**
- **Steeping** (the signature gamble): **use the chart itself** (RUL-2026-10-29-055).
  - **Start.** Each rare chart's item effect (`noncombatquest`) starts its own steeping quest.
    - These are 2 `special` quests, one per rare chart. Special quests are started only by an item and never appear in any quest list.
    - Using the chart consumes one copy.
  - **Rot.** The quest needs Core Rot ×3. If the player lacks them, they take the refund: the chart comes back and nothing is spent.
  - **Opening dialog: "Steep" or "Take it back".** Taking it back refunds the chart (and any Rot already paid), which covers a mis-tap.
  - **Fight.** One fight against a Core Horror scaled to the player, about a 75% solo win rate. It uses its own Core Horror copy, with no Core Rot drop (RUL-2026-10-28-013).
  - **Win:** the tainted chart.
  - **Loss:** a "the rot spits it out" step (`failObjectiveId`) hands the chart back, and the 3 Core Rot are spent.
  - **Item text.** Each rare chart's description says both uses: run it from the Battle Arena, or **use it to steep it at the Core** (3 Core Rot; refund if you lack them; a loss returns the chart and spends the Rot).
  - **Accepted (RUL-2026-10-30-060 item 10):** steeping consumes nearly all Epic charts. The final pass measured about 2 steeps and about 0.07 Epic runs in a typical weekend (1.54 Epic runs without steeping). No change.
  - **To verify before building:** whether an item-started quest charges its entry items at the start (a shortfall would then roll the item use back by itself) or at the fight. The refund dialog covers both cases.
- **Breaking the seal:** an Archive dialogue choice adds an echo fight and guarantees Core Rot ×2.
- **Pressing on:** The Fall's press-on room drops its tainted chart 5%. The Sealed Reliquary's room is cut (RUL-2026-10-30-060 item 6).
- **Natural:** the Archive and Watch endings drop the tainted chart directly at 1%.

**Core Rot:** a stackable reagent with one job, steeping. Sources:
- Endgame Wreck clears: 15%, as a clear drop for the Core Horror's floor (§2). Dungeons have no AI drops.
- The common runs (Low Tide Run, Night Watch): 15% on the ending (RUL-2026-10-28-013).
- The Core Horror's hunt runs: 40% in The Fall, the Rotted Reliquary and the Burning Heading. In hunts the Core Horror carries Core Rot as an AI drop on its quest-battle record (RUL-2026-10-28-013).
- Breaking the seal: Core Rot ×2, guaranteed.
- A failed rare-chart run: 1 Core Rot as consolation (RUL-2026-10-28-019).

**Titles: deferred** (RUL-2026-10-29-041). The run titles are kept in git history for a later update; Walked Every Deck returns with the Crownbreaker trophy (§5c). Trophies return as skin tokens (§5d, RUL-2026-10-29-047).

**New art**
- 4 chart icons.
- 2 tainted chart recolours.
- 1 Core Rot icon.

## 5b. Pet: the Little Horror (RUL-2026-10-29-047; replaces the five-pet Echo Jar of RUL-2026-10-28-011)

Engine facts (theninjarpg source):
- **Reward-only species.** An inactive species is never offered in the sanctuary's daily picks, but an item can still grant it.
- **Pet grants need standard mode:** a `reward_pets` grant, one species per item.
- **Full collections block the jar.** A jar won't open while the collection is full, and it stays in the inventory.
- **Art is generated per owner** from the species' `artDirection` and `rankConcepts` (10 ranks).
- **Pets fight in quest PvE battles** (hunts, pyramid, dungeons). The tuning harness adds a pet.
- **Pet exp lands only for an eligible active pet**, otherwise it is lost. The Galley Stores description says so.
- **Signature jutsu** use `requiredPetSpeciesId`.

**The Little Horror's Jar** grants the event's one pet (kit: `SKYGLASS_PETS.md`).
- **Drop:** an endgame Wreck clear drop at **5%, once per player**, using the dungeon `onlyOnce` flag (RUL-2026-10-29-054). About 20 clears on average.
- **The Deck Gull, Bilge Rat, Lantern Moth and Ship's Cat are cut.**

**Galley Stores** (pet progression): 20,000 pet experience (RUL-2026-10-29-039).
- Found in: easy Wreck clear 10%; a pick option in the Low Tide Run, the Night Watch, the Buried Cache and the Foundry; The Fall's pick (×3); the chest of chests' Rare tier.

**New art:**
- 1 jar icon;
- the Galley Stores icon.

## 5c. Completion achievement: Walked Every Deck (RUL-2026-10-28-020, revived by RUL-2026-10-29-051)

**Walked Every Deck** is a one-time achievement quest. It completes when a player has cleared every chart run, using `complete_specific_quest` objectives:
- Low Tide Run, Night Watch, Buried Cache;
- Drowned Foundry, Quarantined Archive, Captain's Watch;
- Sealed Reliquary, The Fall, both tainted runs;
- Crownhold.

**Reward:** the untradeable **Crownbreaker** trophy token. It replaces the deferred title reward. Achievements complete once per player, so a duplicate is impossible.

## 5d. Skins: Skyglass Tokens and trophy tokens (RUL-2026-10-29-047 … -049)

Engine (theninjarpg upstream `3314d122`, after the 2af4b320 pin):
- **Variants are reskins.** An item variant is a cosmetic reskin of a base item: name, image and descriptions, with the same stats.
- **Token-gated unlock.** A `VARIANT_TOKEN` variant is unlocked by consuming a token item that carries `unlockitemvariant`. The player must own the base item. Each variant unlocks once per player.
- **Two locking fields:**
  - `requiredItemId` on a variant accepts only that token item;
  - `variantId` on a token unlocks only that variant.

**Skyglass Token** (farmable layer)
- **Unlocks:** any one Skyglass skin. Every Skyglass skin carries `requiredItemId` = Skyglass Token, so no other token opens them.
- **Tradeable.**
- **Pace:** about 2-3 a dedicated weekend. The final pass measured 3.0 for a typical player and 5.5 for one who always takes the token (RUL-2026-10-30-060). The event runs Friday to Sunday and repeats weekly, so half the catalogue takes a few weekends.
- **Found in** (×1, ×2 in the rare picks; no direct drop):
  - the Archive and Watch picks (×1), the Sealed Reliquary and The Fall picks (×2);
  - the chest of chests' Legendary tier;
  - the Crown's Hoard.
  - The tainted runs inherit their rare's options.
- **Catalogue:** 12 crafted weapons.
  - Legendary: Aetherion, Thornsilver, Night's Testament, Stormrender, Oathbinder, Ink of the Void, The Unwritten.
  - Epic: Gaea's Embrace, Warden's Bracers, Eclipsed Dawnblade, Zephyr's Whisper.
  - Rare: Yuki's Frostbite.
  - More skins can be added in later weekends without new tokens.

**Trophy tokens** (one skin each: `variantId` set, and the skin's `requiredItemId` is the token itself). Player-facing name: **variants**, never "trophies" (RUL-2026-10-29-053).

| Boss | Trophy skin | Base | Source | Tradeable |
|---|---|---|---|---|
| The Captain | Captain's Command Fan (a gunbai) | The Unwritten | endgame Wreck clear **5%**, once per player (`onlyOnce`; RUL-2026-10-30-060) | no |
| Core Horror | Rot-Bloom Reaper | Oathbinder | endgame Wreck clear **5%**, once per player (`onlyOnce`; RUL-2026-10-30-060) | no |
| Foundry Warden | Warden's Forge-Fists | Warden's Bracers | his runs: 1% hunts, 2% rares, 4% tainted | yes |
| Wayfinder | Wayfinder's Heading | Stormrender | his runs: 1% hunts, 2% rares, 4% tainted | yes |
| First Blade | The First Blade | Aetherion | 2% rares, 4% tainted | yes |
| Sealwright | Sealwright's Seal | Whispering Dawnblade (`mqCCZGSfXUNL02B4H6C9R`; not Eclipsed Dawnblade, RUL-2026-10-30-060) | his runs: 1% hunts, 2% rares, 4% tainted | yes |
| Crowned Captain | Crownbreaker | Thornsilver | the **Walked Every Deck** achievement (RUL-2026-10-29-051) | no |

**Art rule:** a skin keeps its base weapon's silhouette, with skyglass as inlay and accents. The Skyglass Katana stays the only all-crystal blade.

**New art:**
- 12 catalogue skin images;
- 7 boss variant images;
- the Skyglass Token icon;
- 7 boss variant token icons (one token base, seven motifs: RUL-2026-10-30-061).

## 6. To check before the manifests

Open:
- **Galley Stores amount:** the pet-experience lump (director).
- **Core Rot in the easy Wreck:** none (RUL-2026-10-28-020). Only the endgame Wreck drops it.
- **Profession material id lists** per hunt (§4b), from the push/323 capture.
- Reward packages are built in the game's catalog editor until Forge has a package recipe.

Done or obsolete:
- Skin token rates: confirmed by the final simulation pass (3.0 Skyglass Tokens a typical weekend). The Wreck variant tokens are set at 5%, once per player (RUL-2026-10-30-060).
- Forbidden Jutsu Scrolls at 3% of a Strongbox roll: obsolete; §3a places the scroll at 1% (RUL-2026-10-28-018).
- Armory Requisition (RUL-2026-10-25-014, RUL-2026-10-28-003): obsolete; retired (RUL-2026-10-28-016).
- `reward_pet_experience` exists in the pinned source (theninjarpg@2af4b320 `validators/rewards.ts`:54); Galley Stores can use it.
- Closed (RUL-2026-10-24-024): the Skyglass Reliquary, the Mystery Chest and the other old Ghost Ship chests are retired relics; their contents, including the Mystery Chest's Reliquary line, are left as they are.
