# QA revisit list - 2026-10-20

Records found in the live QA pass (`docs/reviews/QA_LIVE_2026-10-20.md`) that were skipped while
making text tickets, and why. All are visible unless noted. Rule from dauntless: battle lines on
items that cannot be used in combat are placeholders and are not fixed.

## Needs context before a description can be written

Quest props and rewards whose story is not in the data. Tell us what each one is for.

| Item | Type | Current description | What we know |
|---|---|---|---|
| Dungeon Key | OTHER, common | "New item description" | Not used by any live quest |
| Celestial Teapot | OTHER, rare | "New item description" | Not used by any live quest |
| Potion Sample | OTHER, epic | "New item description" | Not used by any live quest |
| Torn Stonefang Banner | OTHER, common | "Other" | Not used by any live quest |
| Ember-Stained Edict | OTHER, common | an embedded YouTube video, no text | Collected in a hidden Path of Crimson quest (Part II: The Ember Trail). Its battle line is empty, so like the Medallion it needs a battle line in the same edit |
| Akane's Grandmother | OTHER, common | empty | Not used by any live quest |
| Cat | OTHER, rare | "The Cat!" | Not used by any live quest |
| Plague Mask | MATERIAL, common | "New item description" | Not used by any live quest |
| Potato Sunflower | MATERIAL, rare | empty | Not used by any live quest |
| Bloodline Scroll | CONSUMABLE, legendary | "New item description" | Grants from a list of 14 bloodlines; how the pick works is unconfirmed |
| Inari Fox Figurine Whispers | CONSUMABLE, legendary | "New item description" | Grants the Hyouga Yui bloodline; how players get it is unconfirmed |

## Waiting on something else

| Record | Waiting on |
|---|---|
| Bloodthorn Cache description | Ticket 132 (loot fix) to be decided. A suggestion carries the whole record, so a second one could undo 132 if approved after it. |
| Medallion of the Serpent King description | Its battle line is empty, and items cannot be saved with an empty battle line, so a description-only edit would fail. Needs any non-empty battle line in the same edit. |
| Magma Slayer and Eruption Strike scaling (withdrawn 134) | The damage formula's handling of missing `generalTypes` read in the game source, or a fight capture. Archived under `archive/spent-manifests/push-2026-10-20/`. |

## Optional follow-ups

| Record | Issue |
|---|---|
| Apple, Blueberry, Corn, Eggplant, Mushroom, Pear, Plum, Potatoes, Pumpkin, Raspberry, Tomato | Usable in combat, but the battle line says "%user throws an onion at %target". Each could name its own item. |
| Nin Gen Alliance | Its damage can also hit allies (`friendlyFire: ALL`); the new description (ticket 136) does not say so. |
| Widow's bite | Pool costs are the fractional 0.05 placeholder; real costs are a balance call. |

## Deliberately not ticketed

Staff or test records, not player content: Dummy Armor 1-4, Static Hands, Static Chest, "Dont Die.
You're Too Pretty", Genin PVE Damage and Support, Ninja Force 1's, the silver payout bags and silver
rewards, Staff Booster, Tournament Prize Item, "You know what it is", "Item for Fixing account",
Compensation Scroll, SY SY, AI Blade 40AP, Aika's Love, The Deterrant, WaddleWaddle, and the
test-named jutsu and items. Retiring or hiding them is a separate decision.
