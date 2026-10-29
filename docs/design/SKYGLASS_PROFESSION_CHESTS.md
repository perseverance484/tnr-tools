# Skyglass profession chests: redesign proposal

**Status:** PROPOSAL for director review (2026-10-29). Nothing here is ruled yet. Built from the push/323 item capture
(material rarity, hunted/gathered flags, cost) and the push/325 recipe capture (CraftingRequirement rows). Generator:
`push/skyglass_profession_chests.gen.py` (proposal draft).

## Why change them

Each live chest rolls one flat list. Every material of the chest's rarity drops as a 100%/50%/50% ×10 stack, with no
weighting, no shape, and no link to what crafters need. The weighted-cache engine (theninjarpg `libs/weightedCache.ts`)
can do much more:
- a roll-count distribution (up to 20 rolls);
- up to 20 tiers per chest;
- up to 50 entries per tier, each a bundle of up to 10 items (×1-100);
- several caches on one item.

## Design (every chest)

1. **Value parity.** Each chest's expected value stays within about 10% of the live chest, so professionals' rewards
   stay the same (RUL-2026-10-29-035). Value is material cost (RUL-2026-10-28-033).
2. **Variable haul.** 3 rolls 60% / 4 rolls 30% / 6 rolls 10%. Most openings are normal; one in ten is a big haul.
3. **Recipe lots.** Recipes take materials in fixed lots: Common ×2, Rare ×3, Epic ×5, Legendary ×10. Every quantity is
   a whole number of lots, so a drop always completes crafts with nothing left over.
4. **Tiers inside each chest:**
   - **Staples 55%:** one material at a time, weighted by recipe demand. A material used in more current recipes appears
     more often; a material no recipe uses is excluded.
   - **Recipe kit 25%:** a bundle of the same-profession materials that one real recipe needs at that rarity, e.g.
     Damage Crystal I's hunted half: Owlcat's Fur + Moonlight Antlers + Badger Shell + Glimmer Dust.
   - **Bulk 12%:** a big stack of one of the three most-demanded materials.
   - **Windfall 6%** (Common to Epic): one lot of the next rarity up.
   - **Upgrade 2%** (Common to Epic): the next chest up (Common → Rare → Epic → Legendary), a chest inside the chest.
   - **Heirloom 8%** (Legendary only, replacing Windfall and Upgrade): a doubled three-material legendary kit, the
     jackpot.
5. **Profession purity.** Hunter's Chests hold only hunted materials and Gatherer's Chests only gathered ones.
   - Rust Ferret Pelt moves out of the Common Gatherer's Chest; Copper Ore comes in.
   - Frostbite Leaf is out.
   - Imperial Gold and the Bloodthorn materials are not added.
   - Heart of Kaeruun is excluded (RUL-2026-10-29-035).
6. **Descriptions** use the RUL-2026-10-28-030 format and the variable-roll line ("3-6 rolls").

## Staples weighting (share of the Staples tier)

- Hunter Legendary: Parchment Core 20%, Cracked Auditory Core 20%, Mask Core 20%, Shard of Willful Steel 20%, Thread Core 20%
- Hunter Epic: Moonpetal Weave 18%, Ofuda Moss 18%, Urami Drop 18%, Yamidangan 18%, Seika Seal Petal 14%, Tsukinari Bell 14%
- Hunter Rare: Ashrend Wing 21%, Brasel Spine 16%, Glimmerchitin 16%, Lurethorne 16%, Voltleaf Plume 16%, Frostscale 16%
- Hunter Common: Owlcat's Fur 20%, Glimmer Dust 20%, Moonlight Antlers 15%, Mosswolf Tuft 15%, Badger Shell 15%, Rust Ferret Pelt 15%
- Gatherer Legendary: Mithril Ore 13%, Phoenix Ash Bloom 13%, Heart of Kuraokami 13%, Lunaris Bloom 13%, Tempest Heart 13%, Voidshade Petal 13%, Fujin's Breath 13%, Orichalcum Ore 9%
- Gatherer Epic: Rainbow Cabochon 11%, Adamantine Ore 11%, Celestial Thristle 11%, Icewarden Root 11%, Shadeleaf 11%, Susanoo's Tear 11%, Tempest Thorn 11%, Ember Frond 11%, Diamond Ore 11%
- Gatherer Rare: Galecrest Sage 16%, Gold Ore 16%, Silver Ore 16%, Shiverthorn 11%, Solar Petal 11%, Starfire Petal 11%, Widow's Kiss 11%, Wraithbloom 11%
- Gatherer Common: Murkshade 21%, Sunroot 21%, Copper Ore 16%, Iron Ore 16%, Whistlegrass 11%, Moonveil Moss 5%, Muskshade 5%, Nightshade Thorn 5%

## Generated tables (EV is the expected material value per opening; old is the live chest)

### Legendary Hunter's Chest — EV 11.5M (old 10.6M), scale 2.00
- Staples 55%: Parchment Core ×20 | Cracked Auditory Core ×20 | Mask Core ×20 | Shard of Willful Steel ×20 | Thread Core ×20
- Recipe kit 25%: Cracked Auditory Core ×10 + Mask Core ×10 | Mask Core ×10 + Parchment Core ×10 | Mask Core ×10 + Parchment Core ×10 + Shard of Willful Steel ×10 | Parchment Core ×10 + Shard of Willful Steel ×10 + Thread Core ×10 | Shard of Willful Steel ×10 + Thread Core ×10
- Bulk 12%: Parchment Core ×60 | Cracked Auditory Core ×60 | Mask Core ×60
- Heirloom 8%: Mask Core ×20 + Parchment Core ×20 + Shard of Willful Steel ×20 | Parchment Core ×20 + Shard of Willful Steel ×20 + Thread Core ×20

### Epic Hunter's Chest — EV 7.4M (old 7.0M), scale 5.00
- Staples 55%: Moonpetal Weave ×25 | Ofuda Moss ×25 | Urami Drop ×25 | Yamidangan ×25 | Seika Seal Petal ×25 | Tsukinari Bell ×25
- Recipe kit 25%: Moonpetal Weave ×10 + Yamidangan ×10 | Ofuda Moss ×10 + Yamidangan ×10 | Ofuda Moss ×10 + Tsukinari Bell ×10 | Ofuda Moss ×10 + Seika Seal Petal ×10 + Urami Drop ×10 | Seika Seal Petal ×10 + Urami Drop ×10
- Bulk 12%: Moonpetal Weave ×75 | Ofuda Moss ×75 | Urami Drop ×75
- Windfall 6%: Parchment Core ×25 | Cracked Auditory Core ×25 | Mask Core ×25 | Shard of Willful Steel ×25
- Upgrade 2%: Legendary chest ×1

### Rare Hunter's Chest — EV 6.0M (old 6.0M), scale 8.00
- Staples 55%: Ashrend Wing ×24 | Brasel Spine ×24 | Glimmerchitin ×24 | Lurethorne ×24 | Voltleaf Plume ×24 | Frostscale ×24
- Recipe kit 25%: Ashrend Wing ×12 + Brasel Spine ×12 | Ashrend Wing ×12 + Frostscale ×12 + Glimmerchitin ×12 | Brasel Spine ×12 + Voltleaf Plume ×12 | Ashrend Wing ×12 + Glimmerchitin ×12 | Frostscale ×12 + Voltleaf Plume ×12 | Frostscale ×12 + Lurethorne ×12 + Voltleaf Plume ×12 | …
- Bulk 12%: Ashrend Wing ×72 | Brasel Spine ×72 | Glimmerchitin ×72
- Windfall 6%: Moonpetal Weave ×12 | Ofuda Moss ×12 | Urami Drop ×12 | Yamidangan ×12
- Upgrade 2%: Epic chest ×1

### Common Hunter's Chest — EV 4.3M (old 4.2M), scale 12.00
- Staples 55%: Owlcat's Fur ×24 | Glimmer Dust ×24 | Moonlight Antlers ×24 | Mosswolf Tuft ×24 | Badger Shell ×24 | Rust Ferret Pelt ×24
- Recipe kit 25%: Owlcat's Fur ×12 + Rust Ferret Pelt ×12 | Glimmer Dust ×12 + Moonlight Antlers ×12 | Badger Shell ×12 + Glimmer Dust ×12 + Moonlight Antlers ×12 + Owlcat's Fur ×12 | Badger Shell ×12 + Glimmer Dust ×12 + Rust Ferret Pelt ×12 | Mosswolf Tuft ×12 + Owlcat's Fur ×12
- Bulk 12%: Owlcat's Fur ×72 | Glimmer Dust ×72 | Moonlight Antlers ×72
- Windfall 6%: Ashrend Wing ×12 | Brasel Spine ×12 | Glimmerchitin ×12 | Lurethorne ×12
- Upgrade 2%: Rare chest ×1

### Legendary Gatherer's Chest — EV 10.5M (old 10.0M), scale 2.00
- Staples 55%: Mithril Ore ×20 | Phoenix Ash Bloom ×20 | Heart of Kuraokami ×20 | Lunaris Bloom ×20 | Tempest Heart ×20 | Voidshade Petal ×20 | …
- Recipe kit 25%: Fujin's Breath ×10 + Heart of Kuraokami ×10 | Fujin's Breath ×10 + Mithril Ore ×10 | Heart of Kuraokami ×10 + Mithril Ore ×10 | Mithril Ore ×10 + Voidshade Petal ×10 | Mithril Ore ×10 + Orichalcum Ore ×10 | Orichalcum Ore ×10 + Tempest Heart ×10 + Voidshade Petal ×10 | …
- Bulk 12%: Mithril Ore ×60 | Phoenix Ash Bloom ×60 | Heart of Kuraokami ×60
- Heirloom 8%: Orichalcum Ore ×20 + Tempest Heart ×20 + Voidshade Petal ×20 | Lunaris Bloom ×20 + Phoenix Ash Bloom ×20 + Voidshade Petal ×20 | Fujin's Breath ×20 + Lunaris Bloom ×20 + Phoenix Ash Bloom ×20 | Fujin's Breath ×20 + Lunaris Bloom ×20 + Orichalcum Ore ×20

### Epic Gatherer's Chest — EV 5.2M (old 5.5M), scale 4.00
- Staples 55%: Rainbow Cabochon ×20 | Adamantine Ore ×20 | Celestial Thristle ×20 | Icewarden Root ×20 | Shadeleaf ×20 | Susanoo's Tear ×20 | …
- Recipe kit 25%: Celestial Thristle ×10 + Shadeleaf ×10 | Adamantine Ore ×10 + Icewarden Root ×10 + Rainbow Cabochon ×10 | Celestial Thristle ×10 + Susanoo's Tear ×10 | Diamond Ore ×10 + Susanoo's Tear ×10 | Adamantine Ore ×10 + Ember Frond ×10 + Icewarden Root ×10 + Shadeleaf ×10 | Adamantine Ore ×10 + Diamond Ore ×10 + Shadeleaf ×10 | …
- Bulk 12%: Rainbow Cabochon ×60 | Adamantine Ore ×60 | Celestial Thristle ×60
- Windfall 6%: Mithril Ore ×20 | Phoenix Ash Bloom ×20 | Heart of Kuraokami ×20 | Lunaris Bloom ×20
- Upgrade 2%: Legendary chest ×1

### Rare Gatherer's Chest — EV 4.8M (old 4.8M), scale 8.00
- Staples 55%: Galecrest Sage ×24 | Gold Ore ×24 | Silver Ore ×24 | Shiverthorn ×24 | Solar Petal ×24 | Starfire Petal ×24 | …
- Recipe kit 25%: Gold Ore ×12 + Shiverthorn ×12 + Starfire Petal ×12 + Wraithbloom ×12 | Galecrest Sage ×12 + Solar Petal ×12 | Gold Ore ×12 + Silver Ore ×12 + Starfire Petal ×12 | Solar Petal ×12 + Wraithbloom ×12 | Gold Ore ×12 + Silver Ore ×12 | Shiverthorn ×12 + Solar Petal ×12 + Wraithbloom ×12 | …
- Bulk 12%: Galecrest Sage ×72 | Gold Ore ×72 | Silver Ore ×72
- Windfall 6%: Rainbow Cabochon ×12 | Adamantine Ore ×12 | Celestial Thristle ×12 | Icewarden Root ×12
- Upgrade 2%: Epic chest ×1

### Common Gatherer's Chest — EV 3.2M (old 3.2M), scale 15.00
- Staples 55%: Murkshade ×30 | Sunroot ×30 | Copper Ore ×30 | Iron Ore ×30 | Whistlegrass ×30 | Moonveil Moss ×30 | …
- Recipe kit 25%: Murkshade ×16 + Whistlegrass ×16 | Iron Ore ×16 + Murkshade ×16
- Bulk 12%: Murkshade ×90 | Sunroot ×90 | Copper Ore ×90
- Windfall 6%: Galecrest Sage ×16 | Gold Ore ×16 | Silver Ore ×16 | Shiverthorn ×16
- Upgrade 2%: Rare chest ×1


## Open questions for the director

- Tier weights (55/25/12/6/2) and the roll distribution (3/4/6).
- Whether Upgrade (a chest inside a chest) should exist. It makes the jackpot feel like treasure.
- Whether recipe kits may also draw from cross-rarity recipes (e.g. Kaeruun armour = Epic ×5 + Legendary ×10).
- Seed of False Vitality sits in the Legendary Hunter's Chest today but has no hunted flag. Keep it, or move it to its
  real source?
