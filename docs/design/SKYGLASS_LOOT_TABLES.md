# Skyglass event — loot tables

**Status:** Structure ruled by RUL-2026-10-25-002 and the balance pass RUL-2026-10-25-004, amended by RUL-2026-10-28-009 … -019 (later rulings supersede earlier ones). Weights and quantities below are proposals unless marked ruled; currency amounts are set by the director in game (RUL-2026-10-24-019). Consumable-cache weights and quantities wait on the push/323 item capture (RUL-2026-10-28-018).

**Rule: every item has one home.** A reward appears in more than one source only as the same container, never as loose contents. Skyglass items come only from the Skyglass Coffer, with one exception: Crownhold's pick offers one Fragment of the Skyglass Crown directly (RUL-2026-10-28-003, recorded as an exception by RUL-2026-10-28-010).

## 0. Every item explains itself (RUL-2026-10-28-020)

Each Skyglass item's description tells the player what the item is for, in plain words, after one line of story voice.
- **Charts and the Lantern:** which run it opens; that the chart is spent at entry; that a lost fight ends the run; that health and chakra carry between fights; the press-on choice; for rares, that steeping can twist them.
- **Core Rot:** what steeping is, where it happens, the cost (a rare chart plus 3 Rot), and the outcome on a win (tainted chart) and on a loss (the chart comes back, the Rot is spent).
- **Tainted charts:** the twists, and that the run pays pick 2.
- **Chests, every one:** what can drop and how common each tier is, with the real weights (e.g. "Common 69% · Rare 24% · Epic 5% · Legendary 2%"), the roll count, and any fixed reward (e.g. the Treasury's 150,000 ryo).
- **Echo Jars:** which pet; that a full collection blocks opening.
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
- Tiers with the same name are added together.
- A fixed roll count is not repeated, because the card already shows it.
- The rendering is checked on the director's phone through a hidden test item before release.

## 1. Who owns what

| Container / item | Owns | Found in |
|---|---|---|
| Skyglass Coffer | every Skyglass item | Captain's Watch pick (×1); Sealed Reliquary, The Fall and Crownhold picks (×2); chest of chests Epic; Crown's Hoard |
| Sealed Treasury | 150,000 ryo on every opening + 3/4/6 rolls of Imperial Gold, Rare Jewels, Unobtanium (RUL-2026-10-28-012) | Endgame Wreck clear 3%; every hunt ending at 1% per ladder step (ruled); Sealed Reliquary and The Fall picks; chest of chests Legendary; Crown's Hoard |
| Archive Chart Case | the hunt charts, the Lantern and the rare charts | Quarantined Archive pick; Sealed Reliquary pick (×2); chest of chests Epic |
| Medicine Inro | healing consumables (§3a) | Low Tide Run pick (with 10,000 ryo); Buried Cache pick; chest of chests Common |
| Officer's Pill Case (new) | self-buff consumables (§3a) | Night Watch pick (with 10,000 ryo); chest of chests Rare |
| Sage's Strongbox | enemy-alchemy consumables (§3a) | Quarantined Archive pick; chest of chests Rare |
| Elemental Tool Pouch | throwing consumables, Elemental Kunai on every opening (§3a) | Low Tide Run pick (with 10,000 ryo); Drowned Foundry pick; chest of chests Common |
| Quartermaster's Kit (new) | utility consumables (§3a) | Night Watch pick (with 10,000 ryo); chest of chests Common |
| Galley Stores | pet experience (§5b) | Easy Wreck clear 10%; Low Tide Run, Night Watch, Buried Cache and Foundry picks; The Fall pick (×3); chest of chests Rare |
| Echo Jar | the five Skyglass pets (§5b) | Archive and Watch picks; Sealed Reliquary and The Fall picks (×2); chest of chests Legendary; Crown's Hoard |
| Crown's Hoard | opens the Skyglass Coffer, Sealed Treasury and Echo Jar caches together (RUL-2026-10-28-013) | Crownhold pick |
| Core Rot | steeping reagent (§5) | Endgame Wreck clears, the common runs, the Core Horror's hunt runs, breaking the seal, a failed rare run (§5) |
| Charts / Lastlight Lantern | hunt access (§5) | Wreck clear drops, the chart ladder, the Archive Chart Case |
| Unmarked Cargo (chest of chests) | one roll of the caches above (§2) | Endgame Wreck clear 10% |

**Retired (RUL-2026-10-28-016):** the Armory Requisition is removed entirely: out of the chest of chests, its live record hidden in push/319. **Shelved:** its Special quest (icon kept in `art/skyglass_event_icons/` unused); Lion Token as a Wreck drop.

## 2. Wreck clear (each member)

**Endgame Wreck.** Currency package (director, in game). Independent drops:
- the chest of chests **10%** (RUL-2026-10-25-014; one roll, reweighted by RUL-2026-10-28-016/-018): Common 40 Medicine Inro, Elemental Tool Pouch or Quartermaster's Kit / Rare 35 Sage's Strongbox, Officer's Pill Case or Galley Stores / Epic 18 Skyglass Coffer or Archive Chart Case / Legendary 7 Sealed Treasury or Echo Jar; **Unmarked Cargo**, untradeable;
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

**Archive Chart Case** (weights ruled; Legendary tier per RUL-2026-10-28-013)

| Tier | Weight | Gives |
|---|---|---|
| Common | 60 | Chart of the Drowned Foundry ×1 |
| Rare | 25 | Chart of the Quarantined Archive ×1 |
| Epic | 12 | Chart of the Captain's Watch ×1 |
| Legendary | 3 | Lastlight Lantern ×1 |
| Legendary | 5 | a rare chart ×1 (Reliquary Seal or The Last Heading) |

**Crown's Hoard** (RUL-2026-10-28-013): one item that opens the Skyglass Coffer, the Sealed Treasury and the Echo Jar caches. Open: whether each is opened once or more (§6).

The Medicine Inro, Sage's Strongbox and Elemental Tool Pouch contents are in §3a; their earlier contents (RUL-2026-10-25-012, RUL-2026-10-28-003) are superseded by RUL-2026-10-28-018. The Elemental Tool Pouch remains the single pouch (the Katon pouch record, re-pointed; RUL-2026-10-28-003) and gives Elemental Kunai on every opening.

## 3a. Consumable caches: five themed caches (RUL-2026-10-28-018)

Finished, profession-crafted consumables are allowed: every ninja uses them. Weights and quantities are set after the push/323 item capture. Old elemental kunai stay out; the single Elemental Kunai replaces them.

| Cache | Theme | Common → Legendary |
|---|---|---|
| Medicine Inro | healing | Field Tonic, Energy Potion → Small Health Pill, Full Potion → Panacea → Pill Pack |
| Officer's Pill Case (new) | self-buffs | Chakra Pill, Stamina Pill → Chakra Pill II, Stamina Pill II → Solider Pill → Dr. Kim's Miracle Potion |
| Sage's Strongbox | enemy alchemy | Dr. Kim's Poison Potion, Dr. Kim Disaster Potion → Infernum, Bashōsen → Enemy Pill, Mona's Mermaid Song, Chakra Disrupting Needles → Forbidden Jutsu Scroll (1%) |
| Elemental Tool Pouch | throwing | Elemental Kunai (every opening) plus a roll of Paper Bombs → Senbon Needles, Saki → Venom Cask |
| Quartermaster's Kit (new; the Arsenal Keeper's stores) | utility | Smoke Pellet, Whetstone Oil → Smoke Bomb → Elite Smoke Bomb → Repair Kit |

- **Dead Man's Draught is not used.** Skyglass Serum (Coffer) is its live successor.
- Placement: §1 and §4a.

## 4. Treasure hunts

Every hunt is an isolated Battle Pyramid. **Ending rewards** (always paid, every ending): the 1,000-5,000 exp ladder by final opponent and gating, the hunt's currency (director, in game) and the Sealed Treasury at **1% per ladder step** (I 1% · II 2% · III 3% · IV 4% · V 5% · VI 6%). No caches on endings. Chart drops on endings follow the chart ladder (§5). The **completion pick** is the hunt's identity; the final pick table is §4a.

Ladder per ending: Low Tide Run I; Night Watch II (III if pressed on); Foundry V (always fought to the Warden; the leave-early endings are removed, RUL-2026-10-25-004); Archive clean V / alarm III (left as is, RUL-2026-10-28-016); Watch no terms IV / one-two V / all VI; Sealed Reliquary, The Fall and the tainted runs VI; Crownhold VI. Exp I-VI = 1,000 / 2,000 / 3,000 / 4,000 / 5,000 / 5,000; Treasury chance = step number %.

The badge and the jutsu in Crownhold's pick grey out once held (the game blocks picking content a player already has), so a player needs at least two Crownhold clears to take both. Badge and jutsu are still to be designed.

The Sealwright's doubled health (push/252) applies to the Archive's final fight too, solo; accepted (RUL-2026-10-25-004).

## 4a. Completion picks: final (RUL-2026-10-28-016; supersedes every earlier pick table)

**Pick 1 on every run; tainted runs pick 2.** Difficulty scales through option quality and quantity, not pick count.

| Run | Options (pick 1) |
|---|---|
| Low Tide Run | Pouch + 10,000 ryo (one package card) / Inro + 10,000 ryo (one package card) / Galley Stores |
| Night Watch | Officer's Pill Case + 10,000 ryo / Quartermaster's Kit + 10,000 ryo / Galley Stores (RUL-2026-10-28-018) |
| Buried Cache | 25,000 ryo / Medicine Inro / Galley Stores |
| Drowned Foundry | Elemental Tool Pouch / 50,000 ryo / Galley Stores |
| Quarantined Archive | Archive Chart Case / Sage's Strongbox / Echo Jar |
| Captain's Watch | Skyglass Coffer / Captain's Purse / Echo Jar |
| Sealed Reliquary | Skyglass Coffer ×2 / Sealed Treasury / Echo Jar ×2 / Archive Chart Case ×2 |
| The Fall | Skyglass Coffer ×2 / Sealed Treasury / Echo Jar ×2 / Galley Stores ×3 |
| Tainted runs | **pick 2** from their rare's options; Lantern 30% and Core Rot 40%. No guaranteed drops: the second pick is the appeal (RUL-2026-10-28-019) |
| Crownhold | Crown's Hoard / Skyglass Coffer ×2 / Crownhold badge / Crownhold jutsu / Crown Fragment (RUL-2026-10-28-017) |

The rares double the Watch's Coffer and Jar, so each rung pays more than the one below it.

Cut and not to be rebuilt: the Archive's Records exp, the Watch's Inro ×3, The Fall's Captain's Purse, the commons' exp cards (RUL-2026-10-28-016); Crownhold's Honor and Crownhold's Echo Jar ×2 (RUL-2026-10-28-017); the tainted runs' guaranteed Sealed Treasury and Echo Jar (RUL-2026-10-28-019).

## 4b. Profession chests (RUL-2026-10-28-023; supersedes the per-item rolls of RUL-2026-10-28-019)

- **Which chests:** the eight live profession chests. The Hunter's Chests are flagged `canBeHunted` and the Gatherer's Chests `canBeGathered`.
- **Rarity:** the Rare, Epic and Legendary chests have their rarity set to match their contents; the Common ones stay Common. The engine rolls each chest at the player's rank chance for its rarity, so D rank never rolls Epic or Legendary.

  | Rank | Common | Rare | Epic | Legendary |
  |---|---|---|---|---|
  | D | 15% | 10% | 0% | 0% |
  | C | 20% | 15% | 5% | 1% |
  | B | 25% | 20% | 10% | 2% |
  | A | 30% | 25% | 15% | 5% |
  | S | 40% | 30% | 20% | 10% |

- **When they roll:** every battle win in a hunt carries `reward_hunter_items` and `reward_gathering_items`, limited to the area's chest tier. Only that occupation receives them (`routers/quests.ts` ~2218), and each success is one chest.
- **Tiers and yield:**

  | Area | Chest tier | Chests per run at D / C / B / A / S |
  |---|---|---|---|
  | Buried Cache and the common runs | Common | 0.4 / 0.6 / 0.8 / 0.9 / 1.2 |
  | Drowned Foundry | Rare | 0.4 / 0.6 / 0.8 / 1.0 / 1.2 |
  | Quarantined Archive and Captain's Watch | Epic | 0 / 0.2 / 0.4 / 0.6 / 0.8 |
  | The rare runs and Crownhold | Epic + Legendary | 0 / 0.3 / 0.6 / 1.0 / 1.5 |

  A chest averages about 120 materials. The old Ghost Ship profession quests paid about 1-1.5 chests per clear, so A and S rank land at about 50-100% of that.
- **Not in the Wreck:** dungeon rewards don't support these flags.
- **Before the flags change:** the push/324 quest audit and the push/323 item capture must show no `reward_hunter_items` or `reward_gathering_items` reward with an empty id list.

## 5. Charts: the map system (RUL-2026-10-28-009)

PoE-style maps: farming the Wreck drops charts, and each chart opens an isolated high-stakes run.

**Every chart run**
- The chart is an entry item, spent when the run starts.
- Losing any fight fails the run (`failObjectiveId`).
- Health and chakra carry between fights; there are no refills.
- Rewards bank at each fight. At the last landing the player picks: leave with what they hold, or press on into a final room whose reward is lost on a fall.

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
| Archive ending | Reliquary Seal 25%, +20% from its press-on room (RUL-2026-10-28-010) |
| Watch ending | The Last Heading 25%, +20% from its press-on room |
| Crownhold ending | one of the two rare charts 50% |
| Sealed Reliquary / The Fall ending | Lastlight Lantern 15% |
| Archive Chart Case | Legendary: Lantern 3 / rare chart 5 (§3) |

**Tainted rares** (rares only). Harder upgrades of their counterpart; target clear rate about 55%, against about 80% for the base rare. Rewards: §4a (pick 2, Lantern 30%, Core Rot 40%, no guaranteed drops; RUL-2026-10-28-019), and twice the trophy rate (RUL-2026-10-28-010).
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
- **Steeping** (the signature gamble): a short quest at the Core.
  - Entry: a rare chart plus Core Rot ×3, both spent.
  - One fight against a Core Horror scaled to the player. This fight uses its own Core Horror copy, which carries no Core Rot drop (RUL-2026-10-28-013).
  - Win: the tainted chart. Lose: a "the rot spits it out" step (`failObjectiveId`) hands the chart back, and the 3 Core Rot are spent.
  - Two versions, one per rare chart. The scaled Core Horror is tuned in the harness to about a 75% solo win rate.
- **Breaking the seal:** an Archive dialogue choice adds an echo fight and guarantees Core Rot ×2.
- **Pressing on:** the rare runs' final room drops the tainted chart 5%.
- **Natural:** the Archive and Watch endings drop the tainted chart directly at 1%.

**Core Rot:** a stackable reagent with one job, steeping. Sources:
- Endgame Wreck clears: 15%, as a clear drop for the Core Horror's floor (§2). Dungeons have no AI drops.
- The common runs (Low Tide Run, Night Watch): 15% on the ending (RUL-2026-10-28-013).
- The Core Horror's hunt runs: 40% in The Fall, the Rotted Reliquary and the Burning Heading. In hunts the Core Horror carries Core Rot as an AI drop on its quest-battle record (RUL-2026-10-28-013).
- Breaking the seal: Core Rot ×2, guaranteed.
- A failed rare-chart run: 1 Core Rot as consolation (RUL-2026-10-28-019).

**Titles** (one each; one-time first-clear achievements, RUL-2026-10-28-013)
| Title | Run |
|---|---|
| Relief of the Watch | The Night Watch |
| Who Relieved the Captain | Captain's Watch |
| Keeper of Echoes | The Sealed Reliquary |
| Walked Out of the Fire | either tainted rare |
| Crownbreaker | Crownhold (matches the badge) |

Each title carries a small permanent mastery or regeneration bonus; the values are proposed for approval and not yet ruled (§6).

**Trophies** (rare boss drops, 1-2%; effect sketches, with numbers set when the kits are approved)
- **The Warden's Maul:** a bukijutsu weapon, a forge maul glowing at the head, with fire damage and a short burn. Drops from the Foundry Warden (Foundry, Sealed Reliquary, Rotted Reliquary).
- **Wayfinder's Compass:** an accessory with a flee bonus; its needle never settles ("Still no home port"). Drops from the Wayfinder (Watch, Burning Heading).

**New art**
- 2 trophy icons and 4 chart icons.
- 2 tainted chart recolours.
- 1 Core Rot icon.

## 5b. Pets: Galley Stores and the Echo Jar (RUL-2026-10-28-011)

Engine facts (theninjarpg source):
- **Reward-only species.** An inactive species is never offered in the sanctuary's daily picks, but an item can still grant it (`item.ts`: "Authored rewards may grant species excluded from daily sanctuary offers").
- **Pet grants need standard mode.** A pet can only come from a standard `reward_pets` grant, one species per item; a weighted cache cannot grant a pet. So the Echo Jar rolls jar items, and each jar grants its pet.
- **Full collections block the jar.** A jar won't open while the collection is full, and stays in the inventory.
- **Art is generated per owner** from the species' `artDirection` and `rankConcepts` (10 ranks). No hand-drawn art per pet.
- **Pets fight in quest PvE battles**, which includes the hunts, the pyramid and dungeons (`combat/pets.ts`). The tuning harness must add a pet.
- **Pet exp lands only for an eligible active pet** (battle-enabled, art ready, not on a task); otherwise it is lost (`pets/experience.ts`). The Galley Stores description must say so.
- **Signature jutsu.** Pet jutsu are `jutsuType PETS`. A jutsu with `requiredPetSpeciesId` can be equipped only by that species.

**Galley Stores** (pet progression)
- A standard reward of pet experience (`reward_pet_experience`): a lump of roughly 5-7 meals' worth, with no feeding cooldown. The amount is set by the director (open, §6).
- No meal items, because meals are crafted.

**Echo Jar** (weighted, 1 roll; each jar is its own tradeable item granting one inactive species)
| Weight | Jar → pet | Rarity / role |
|---|---|---|
| 50 | Deck Gull | Common / Support |
| 30 | Bilge Rat | Uncommon / Assault |
| 13 | Lantern Moth | Rare / Healer |
| 5 | The Ship's Cat | Epic / Support |
| 2 | Little Horror | Legendary / Assault |

**Placement** (the Footlocker / Shore Leave proposals were not adopted)
- **Galley Stores:** easy Wreck clear 10%; a pick option in the Low Tide Run, the Night Watch, the Buried Cache and the Foundry; The Fall's pick (×3); the chest of chests' Rare tier.
- **Echo Jar:** a pick option in the Archive, the Watch and the rare runs (×2 in the rares); the chest of chests' Legendary tier; the Crown's Hoard. It is not guaranteed on the tainted runs (RUL-2026-10-28-019) and is not in Crownhold's pick (RUL-2026-10-28-017).

**New art:** 2 chest icons, plus 1 jar icon recoloured per pet.

**Kits:** `SKYGLASS_PETS.md`.

## 5c. Completion achievement (RUL-2026-10-28-020)

**Walked Every Deck** is a one-time achievement quest. It completes when a player has cleared every chart run: Low Tide Run, Night Watch, Buried Cache, Drowned Foundry, Quarantined Archive, Captain's Watch, Sealed Reliquary, The Fall, both tainted runs, and Crownhold. It uses `complete_specific_quest` objectives.
- **Reward:** the title **Walked Every Deck**. Its bonus is set with the other title values.
- **Purpose:** an endgame goal past Crownhold.

## 6. To check before the manifests

Open:
- **Crown's Hoard contents:** how many of each cache (Coffer, Treasury, Echo Jar) one Hoard opens.
- **Galley Stores amount:** the pet-experience lump (director).
- **Title values:** the small mastery/regeneration bonuses are proposed, not ruled.
- **Core Rot in the easy Wreck:** none (RUL-2026-10-28-020). Only the endgame Wreck drops it.
- **Consumable-cache weights and quantities** (§3a), set from the push/323 capture. That capture also settles the shop flags still unconfirmed for Pill Pack, Small Health Pill, Stamina Pill II, Paper Bombs, Saki, Senbon Needles, Smoke Pellet, Venom Cask, Whetstone Oil, Solider Pill and Mona's Mermaid Song.
- **Profession material id lists** per hunt (§4b), from the push/323 capture.
- Reward packages are built in the game's catalog editor until Forge has a package recipe.

Done or obsolete:
- Forbidden Jutsu Scrolls at 3% of a Strongbox roll: obsolete; §3a places the scroll at 1% (RUL-2026-10-28-018).
- Armory Requisition (RUL-2026-10-25-014, RUL-2026-10-28-003): obsolete; retired (RUL-2026-10-28-016).
- `reward_pet_experience` exists in the pinned source (theninjarpg@2af4b320 `validators/rewards.ts`:54); Galley Stores can use it.
- Closed (RUL-2026-10-24-024): the Skyglass Reliquary, the Mystery Chest and the other old Ghost Ship chests are retired relics; their contents, including the Mystery Chest's Reliquary line, are left as they are.
