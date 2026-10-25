# Skyglass event — loot tables

**Status:** Structure ruled by RUL-2026-10-25-002 (supersedes the ladder caches and the shared pick of RUL-2026-10-24-014/-017). Weights and quantities below are proposals unless marked ruled; currency amounts are set by the director in game (RUL-2026-10-24-019).

**Rule: every item has one home.** A reward appears in more than one source only as the same container, never as loose contents. Skyglass items come only from the Skyglass Coffer.

## 1. Who owns what

| Container | Owns | Found in |
|---|---|---|
| Skyglass Coffer | every Skyglass item | Captain's Watch pick (×1), Silent Bastion pick (×2) |
| Crew Footlocker | valuables: Rare Jewels, Imperial Gold, Unobtanium | 3% on the Wreck clear and on every hunt ending (ruled) |
| Archive Chart Case | the four hunt maps | Quarantined Archive pick |
| Sage's Strongbox | battle reagents, elite pills, forbidden scrolls | Quarantined Archive pick |
| Medicine Inro | all pills and potions, Pill Pack included | Captain's Watch pick |
| Tool Pouches ×5 | element kunai, smoke, oil, venom, bombs, senbon, saki | Drowned Foundry pick |
| Charts / Beacon | hunt access | Wreck clear drops, Archive Chart Case |

## 2. Wreck clear (each member)

Currency package (director, in game). Independent drops: Chart of the Drowned Foundry **12%**, Chart of the Quarantined Archive **6%**, Chart of the Captain's Watch **6%**, Skyglass Signal Beacon **3%**, Crew Footlocker **3%** (ruled).

## 3. Caches (weighted, one roll each)

**Skyglass Coffer** — the only source of Skyglass items.

| Tier | Weight | Gives |
|---|---|---|
| Common | 70 | Skyglass Filament ×2 |
| Rare | 24 | Skyglass Serum ×3 |
| Epic | 5 | Fragment of the Skyglass Crown ×1 |
| Legendary | 1 | Skyglass Katana ×1 or Skyglass Crystal ×1 |

**Crew Footlocker** (new; premium, the Ornate Chest's old role)

| Tier | Weight | Gives |
|---|---|---|
| Common | 70 | Rare Jewels (quantity open) |
| Rare | 24 | Imperial Gold (quantity open) |
| Epic | 6 | Unobtanium (quantity open) |

**Archive Chart Case** (new; weights ruled)

| Tier | Weight | Gives |
|---|---|---|
| Common | 60 | Chart of the Drowned Foundry ×1 |
| Rare | 25 | Chart of the Quarantined Archive ×1 |
| Epic | 12 | Chart of the Captain's Watch ×1 |
| Legendary | 3 | Skyglass Signal Beacon ×1 |

**Medicine Inro** — Common 70 (Field Tonic ×10 / Chakra Pill ×10 / Stamina Pill ×10); Rare 22 (Small Health Pill ×10 / Dr. Kim's Miracle Potion ×10 / Panacea ×10); Epic 7 (Chakra Pill II ×10 / Stamina Pill II ×10); Legendary 1 (Pill Pack ×5).

**Sage's Strongbox** — Common 65 (Dr. Kim Disaster Potion ×20 / Chakra Disrupting Needles ×20); Epic 26 (Infernum ×10 / Bashōsen ×10 / Dr. Kim's Poison Potion ×10); Legendary 8 (Solider Pill ×5 / Enemy Pill ×5 / Mona's Mermaid Song ×5; Pill Pack removed, the Inro owns it); Forbidden 1 (Forbidden Jutsu Scroll: Nexus ×1 / Rebirth ×1).

**Tool Pouches** (Katon, Wave, Ikazuchi, Stonefall, Zephyrfang) — that element's kunai ×10 every opening, plus one roll: Common 70 (kunai ×10 / Smoke Pellet ×10 / Whetstone Oil ×10 / Venom Cask ×10; Chakra Disrupting Needles removed, the Strongbox owns them); Rare 25 (kunai ×20 / Elite Smoke Bomb ×10 / Paper Bombs ×10); Epic 5 (kunai ×30 / Senbon Needles ×10 / Saki ×10).

## 4. Treasure hunts

Every hunt is an isolated Battle Pyramid. **Ending rewards** (always paid, every ending): the 1,000-5,000 exp ladder by final opponent and gating, the hunt's currency (director, in game) and Crew Footlocker **3%**. No caches on endings. **Completion pick** (choose 1) is the hunt's identity:

| Hunt | Pick 1 of |
|---|---|
| Drowned Foundry | Katon / Wave / Ikazuchi / Stonefall / Zephyrfang Tool Pouch |
| Quarantined Archive | Archive Chart Case · Sage's Strongbox · The Records (exp lump) |
| Captain's Watch | Skyglass Coffer · Captain's Purse (ryo lump) · Medicine Inro (quantity open) |
| Silent Bastion | Skyglass Coffer ×2 · Bastion's Honor (village tokens lump) · **Bastion badge** · **Bastion jutsu** |

The badge and the jutsu grey out once held (the game blocks picking content a player already has), so a player needs at least two Bastion clears to take both; later clears pick the Coffers or Bastion's Honor. Badge and jutsu are still to be designed.

Exp ladder per ending (unchanged): Foundry leave-1 I / leave-2 III / Warden V; Archive clean V / alarm III; Watch no terms IV / one-two V / all VI; Bastion VI. I-VI = 1,000 / 2,000 / 3,000 / 4,000 / 5,000 / 5,000 exp.

**Shelved:** Armory Requisition and its Special quest (icon kept in `art/skyglass_event_icons/` unused); Lion Token as a Wreck drop.

## 6. To check before the manifests

- Shop items sit in a cache's Common tier; Dr. Kim's Miracle Potion is the one exception, in Rare. Pill Pack, Small Health Pill, Stamina Pill II, Paper Bombs, Saki, Senbon Needles, Smoke Pellet, Venom Cask, Whetstone Oil, Solider Pill and Mona's Mermaid Song have no capture with a shop flag yet; confirm each before the manifest.
- Forbidden Jutsu Scrolls at 3% of one Strongbox roll: keep, lower or remove.
- Reward packages are built in the game's catalog editor until Forge has a package recipe.
- Closed (RUL-2026-10-24-024): the Skyglass Reliquary, the Mystery Chest and the other old Ghost Ship chests are retired relics; their contents, including the Mystery Chest's Reliquary line, are left as they are.
