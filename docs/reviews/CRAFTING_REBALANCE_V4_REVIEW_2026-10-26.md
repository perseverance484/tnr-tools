# Crafting rebalance v4: review against Ghost Ship drops

- **Input:** `Crafting-balanced-revised-v4.xlsx` (director upload, 2026-10-26; not committed). Its own note: built from a
  live TNR MCP read on 2026-10-26; "Live game recipes were not updated."
- **Ask (director):** "Analyze this and tell me your findings. Particularly how this affects the most recent update to
  ghost ship drops like the kunai pouches"
- **Evidence limits:** Forge can only keep full records from single-record reads, so live recipes (`craftingRequirements`)
  cannot be captured today; the sheet's own "current" columns are the recipe evidence. The newest committed reads of
  the Ghost Ship reward caches are from 2026-10-13. push/250 reads the records this review depends on.

## What the sheet does

76 visible craftable outputs (meals and some requested entries removed). Raw inputs drawn from a supplied
gathering/hunting list; rarity-matched materials (Common 2-4 recipe uses each, Rare 4-6, Epic 5-6, Legendary 6); at most
7 inputs (consumables 4, kunai exempt) and 10 per input; village parity of 101 local units per village.

## Findings

1. **The five elemental kunai are not outputs.** Ikazuchi, Katon, Stonefall, Wave and Zephyrfang Kunai have no recipe in
   the sheet (Ikazuchi and Katon read `canBeCrafted: true` in the 2026-10-25 census). Only **Elemental Kunai** (RARE, six
   village commons x2) and **Bloodthorn Kunai** are. Yet Bashosen still needs Zephyrfang Kunai x1 and Infernum needs
   Katon Kunai x1. If those kunai stop being craftable, drops (War Caches, the Shinobi Tool Pouch) become their only
   source.
2. **Elemental Kunai is the one cross-village craft.** It takes one Common material from each of the six villages, so
   every crafter must trade. Each village material falls to 2 recipe uses (Whistlegrass 14 -> 2, Moonveil Moss 8 -> 2,
   Sunroot 5 -> 2).
3. **The Shinobi Tool Pouch (as last read, 2026-10-13) is a kunai-smith kit**: Iron Ore x20 guaranteed plus 50% lines of
   exactly the six Elemental Kunai village materials and five Rare materials (Ashrend Wing, Frostscale, Voltleaf Plume,
   Brasel Spine, Lurethorne). Under the sheet those still have uses (Rares 5-6 each; Iron Ore 1 -> 3), so a material
   pouch keeps its value, but RUL-2026-10-23-005 already moves the caches to **finished items** (the pouch's signature
   = an elemental kunai stack). With finished kunai in the pouch, finding 1 makes the pouch a main kunai source, so its
   rates matter more.
4. **Bloodthorn Kunai gets much cheaper**: Bloodcore Ore and Bloodflower (Legendary) are dropped; it becomes four Common
   hunting materials x2. Its Bloodthorn Cache drop is worth less.
5. **Skyglass items are out of scope, and the sheet contradicts itself on them.** Skyglass Filament and Fragment of the
   Skyglass Crown are "Excluded" (0 proposed uses), and Skyglass Crystal and The Skyglass Crown have no recipe rows, but
   the Live Use Audit sheet lists them as proposed outputs (Heart of Kuraokami, Tempest Heart, Whispered Ember). If the
   Crown and Crystal recipes were removed rather than left alone, the Expedition's 20% Crown fragment and the Drowned
   Foundry's Filament reward lose their purpose.
6. **The Live Use Audit sheet is stale:** 23 of its rows disagree with the Recipes sheet (e.g. Axel's Frost and Dagger's
   Steel are listed with uses but appear in no recipe; Potato Sunflower, Countess's Silk Ribbon and Gilded Clasp likewise).
   It references eight outputs the Recipes sheet does not have. Recipes and Material Coverage agree with each other.
7. **Event materials lose all uses:** Axel's Frost, Dagger's Steel, Decaying Wood, Bloodcore Ore and Bloodflower are
   excluded (0 uses).

## Decisions for the director

- Are the five elemental kunai meant to stop being craftable (drop-only), or were they left out by mistake?
- Should the Skyglass Crown and Crystal recipes stay as they are (still needing Fragments and Filament)?
- Shinobi Tool Pouch: finished kunai (RUL-2026-10-23-005) at what stack and rate, given finding 1.
