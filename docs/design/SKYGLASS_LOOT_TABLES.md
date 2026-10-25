# Skyglass event — loot tables

**Status:** PROPOSAL. Structure ruled by RUL-2026-10-24-011; every line, tier weight, quantity and package content below is a proposal for the director. Generated from one data source with the review page; edit both together.

## 1. Wreck clear (each member)

15,000 exp · 1,000 tokens · 1,000 prestige · one chest.

## 2. Skyglass Salvage Chest (name open) — hybrid, not tradable

**Standard part** (independent lines):

| Line | Chance |
|---|---|
| 50,000 ryo | 100% |
| Skyglass Serum ×2 | 100% |
| Chart of the Drowned Foundry | 12% |
| Chart of the Quarantine Vault | 6% |
| Skyglass Signal Beacon (Silent Bastion) | 6% |
| Chart of the Skyglass Expedition | 3% |
| Lion Token | 1% |

**Weighted part:** 2 rolls; each roll picks a tier, then one entry uniformly.

| Tier | Weight | Entries (per-roll chance each) |
|---|---|---|
| Supplies | 60% | Small Health Pill ×5 (12%); Field Tonic ×10 (12%); Smoke Pellet ×10 (12%); Venom Cask ×10 (12%); Elite Smoke Bomb ×5 (12%) |
| Valuables | 30% | Rare Jewels ×5 (5%); Imperial Gold ×5 (5%); Unobtanium ×5 (5%); Senbon Needles ×5 (5%); Chakra Pill II ×10 (5%); Stamina Pill II ×10 (5%) |
| Reward cache | 9% | Medicine Inro (3%); Shinobi Tool Pouch (3%); Sage's Strongbox (3%) |
| Prize | 1% | Ornate Chest (0.3%); Pill Pack ×2 (0.3%); Skyglass Filament ×2 (0.3%) |

## 3. Reward caches (weighted, finished items)

**Medicine Inro** — Pills and potions; 2 roll(s).

| Tier | Weight | Entries |
|---|---|---|
| Common | 55% | Field Tonic ×10; Chakra Pill ×10; Stamina Pill ×5 |
| Rare | 30% | Small Health Pill ×5; Dr. Kim's Miracle Potion; Panacea |
| Epic | 12% | Chakra Pill II ×10; Stamina Pill II ×10 |
| Legendary | 3% | Pill Pack ×2 |

**Shinobi Tool Pouch** — Kunai and tools; one element per roll; 2 roll(s).

| Tier | Weight | Entries |
|---|---|---|
| Common | 60% | Katon Kunai ×10; Wave Kunai ×10; Ikazuchi Kunai ×10; Stonefall Kunai ×10; Zephyrfang Kunai ×10; Elite Smoke Bomb ×5; Chakra Disrupting Needles |
| Rare | 30% | Smoke Pellet ×10; Whetstone Oil ×10; Venom Cask ×10; Paper Bombs ×5 |
| Epic | 10% | Senbon Needles ×5; Saki; Bashōsen; Infernum |

**Sage's Strongbox** — High-tier consumables; 1 roll(s).

| Tier | Weight | Entries |
|---|---|---|
| Epic | 60% | Chakra Pill II ×10; Stamina Pill II ×10; Dr. Kim's Poison Potion ×5 |
| Legendary | 37% | Pill Pack ×2; Solider Pill; Enemy Pill; Mona's Mermaid Song |
| Forbidden | 3% | Forbidden Jutsu Scroll: Nexus; Forbidden Jutsu Scroll: Rebirth |

## 4. Treasure hunts

Completion: pick 1 of 4 reward-package cards — **Medic's Haul** (Medicine Inro ×2); **Shinobi's Haul** (Shinobi Tool Pouch ×2); **Sage's Haul** (Sage's Strongbox ×1); plus the hunt's own card.

### The Drowned Foundry

Entry: Chart of the Drowned Foundry (consumed at start). Own card: **Filament Haul** (Skyglass Filament ×3, Skyglass Serum ×5).

| Ending | Pays automatically |
|---|---|
| Leave after the first fight | 50,000 ryo, 5,000 exp, Skyglass Filament ×1 |
| Leave after the second fight | 100,000 ryo, 10,000 exp, Skyglass Filament ×2 |
| Defeat the Foundry Warden | 200,000 ryo, 20,000 exp, Skyglass Filament ×5, Skyglass Serum ×3 |

### The Quarantine Vault

Entry: Chart of the Quarantine Vault (consumed at start). Own card: **Archive Haul** (Skyglass Reliquary ×1).

| Ending | Pays automatically |
|---|---|
| Clean run (no alarms) | 150,000 ryo, 15,000 exp, Skyglass Reliquary (100%) |
| Alarm tripped | 150,000 ryo, 15,000 exp, Skyglass Reliquary (50%) |

### The Silent Bastion

Entry: Skyglass Signal Beacon (consumed at start). Own card: **Armory Haul** (Senbon Needles ×10, Elite Smoke Bomb ×10, Venom Cask ×20, Dr. Kim's Poison Potion ×5).

| Ending | Pays automatically |
|---|---|
| Defeat Supreme Commander Arakane | 300,000 ryo, 30,000 exp |

### The Skyglass Expedition

Entry: Chart of the Skyglass Expedition (consumed at start). Own card: **Skyglass Haul** (Skyglass Filament ×5, Skyglass Serum ×5).

| Ending | Pays automatically |
|---|---|
| w_A hidden shore cache | 75,000 ryo, Rare Jewels ×5 (55%), Ornate Chest (15%) |
| w_B1 accessible hold | 75,000 ryo, Imperial Gold ×5 (40%), Ornate Chest (15%) |
| w_B2 restricted vault | 100,000 ryo, Ornate Chest (25%), Unobtanium ×5 (25%) |
| w_C direct Captain | 150,000 ryo, Ornate Chest (35%), Skyglass Serum ×5 (50%) |
| w_Co oathbound Crowned Captain | 150,000 ryo, Ornate Chest (25%), Skyglass Serum ×5 (20%), Skyglass Katana (3%), Fragment of the Skyglass Crown (20%) |
| w_secret Quarantined Archive | 100,000 ryo, Skyglass Reliquary (100%) |

## 5. To check before the manifests

- Shop items sit in a cache's Common tier; Dr. Kim's Miracle Potion is the one exception, in Rare. Pill Pack, Small Health Pill, Stamina Pill II, Paper Bombs, Saki, Senbon Needles, Smoke Pellet, Venom Cask, Whetstone Oil, Solider Pill and Mona's Mermaid Song have no capture with a shop flag yet; confirm each before the manifest.
- Forbidden Jutsu Scrolls at 3% of one Strongbox roll: keep, lower or remove.
- Reward packages are built in the game's catalog editor until Forge has a package recipe.
- Skyglass Reliquary stays LEGENDARY, not tradable; Vault and the Expedition secret ending both pay it.
- The Mystery Chest's 10% Reliquary line was added outside any push.
