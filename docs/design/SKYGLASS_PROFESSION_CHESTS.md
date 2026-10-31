# Skyglass profession chests: redesign

**Status:** FINAL tables (RUL-2026-10-29-036, -037; tier names RUL-2026-10-29-058; quantities rounded to the nearest 5, RUL-2026-10-31-074 item 2). Chest kind is settled: one combined kind, 8 chests. Built from the push/323 item capture
(material rarity, hunted/gathered flags, cost) and the push/325 recipe capture (CraftingRequirement rows). Generator:
`push/skyglass_profession_chests.gen.py`; output `state/skyglass_design/chests.json`.

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
3. **Recipe lots, then round numbers.** Recipes take materials in fixed lots: Common ×2, Rare ×3, Epic ×5, Legendary ×10.
   The generator sizes every quantity in whole lots, then rounds it to the nearest 5 (RUL-2026-10-31-074 item 2:
   readable stacks win over exact lots). The Epic and Legendary chests already sat on multiples of 5; the Common and
   Rare chests changed (Common Hunter's 26→25, 12→10, 78→80, 12→10; Rare Hunter's 27→25, 12→10, 81→80, 12→10;
   Common Gatherer's 34→35, 16→15; Rare Gatherer's 27→25, 12→10, 81→80, 12→10).
4. **Tiers inside each chest** (named Common, Rare, Epic and Legendary since RUL-2026-10-29-058; formerly Staples,
   Recipe kit, Bulk and Windfall/Heirloom):
   - **Common 56%** (55% on Legendary chests): one material at a time, weighted by recipe demand. A material used in more current recipes appears
     more often; a material no recipe uses is excluded.
   - **Rare 26%** (25% on Legendary chests), the recipe kit: a bundle of the same-profession materials that one real recipe needs at that rarity, e.g.
     Damage Crystal I's hunted half: Owlcat's Fur + Moonlight Antlers + Badger Shell + Glimmer Dust.
   - **Epic 12%**, bulk: a big stack of one of the three most-demanded materials.
   - **Legendary 6%** (Common to Epic chests), the windfall: one lot of the next rarity up.
   - **Legendary 8%** (Legendary chests, in place of the windfall), the heirloom: a doubled three-material legendary kit, the jackpot.
   - **No Upgrade tier** (RUL-2026-10-29-036): a chest inside a chest is the Unmarked Cargo's job. Its 2% went back as
     Common +1 and Rare +1.
   - **Quantities** are capped at 100, the engine's limit (Common Gatherer's Epic tier ×100).
5. **Profession purity.** Hunter's Chests hold only hunted materials and Gatherer's Chests only gathered ones.
   - Rust Ferret Pelt moves out of the Common Gatherer's Chest; Copper Ore comes in.
   - Frostbite Leaf is out.
   - Imperial Gold and the Bloodthorn materials are not added.
   - Heart of Kaeruun is excluded (RUL-2026-10-29-035).
   - Seed of False Vitality leaves the Legendary Hunter's Chest and stays with its real source (RUL-2026-10-29-036).
6. **Descriptions** use the condensed ◆ format (loot tables §0, RUL-2026-10-31-074 item 1): every material named with its chance, the Common tier grouped by chance, the Rare tier as "(k kits, x% each)" where it has more than two kits, and the variable-roll line ("3–6 rolls."). Text of record: `SKYGLASS_TEXT.md` §4.5.

## Common-tier weighting (share of the Common tier)

- Hunter Legendary: Parchment Core 20%, Cracked Auditory Core 20%, Mask Core 20%, Shard of Willful Steel 20%, Thread Core 20%
- Hunter Epic: Moonpetal Weave 18%, Ofuda Moss 18%, Urami Drop 18%, Yamidangan 18%, Seika Seal Petal 14%, Tsukinari Bell 14%
- Hunter Rare: Ashrend Wing 21%, Brasel Spine 16%, Glimmerchitin 16%, Lurethorne 16%, Voltleaf Plume 16%, Frostscale 16%
- Hunter Common: Owlcat's Fur 20%, Glimmer Dust 20%, Moonlight Antlers 15%, Mosswolf Tuft 15%, Badger Shell 15%, Rust Ferret Pelt 15%
- Gatherer Legendary: Mithril Ore 13%, Phoenix Ash Bloom 13%, Heart of Kuraokami 13%, Lunaris Bloom 13%, Tempest Heart 13%, Voidshade Petal 13%, Fujin's Breath 13%, Orichalcum Ore 9%
- Gatherer Epic: Rainbow Cabochon 11%, Adamantine Ore 11%, Celestial Thristle 11%, Icewarden Root 11%, Shadeleaf 11%, Susanoo's Tear 11%, Tempest Thorn 11%, Ember Frond 11%, Diamond Ore 11%
- Gatherer Rare: Galecrest Sage 16%, Gold Ore 16%, Silver Ore 16%, Shiverthorn 11%, Solar Petal 11%, Starfire Petal 11%, Widow's Kiss 11%, Wraithbloom 11%
- Gatherer Common: Murkshade 21%, Sunroot 21%, Copper Ore 16%, Iron Ore 16%, Whistlegrass 11%, Moonveil Moss 5%, Muskshade 5%, Nightshade Thorn 5%

## Generated tables (EV is the expected material value per opening; old is the live chest)

Output of `python3 push/skyglass_profession_chests.gen.py` after the rounding (RUL-2026-10-31-074 item 2). All eight
sit within 10% of the live chest: Common Hunter's −7%, Rare Hunter's −7%, Rare Gatherer's −6%, Epic Hunter's −4%,
Legendary Hunter's +8% (before the rounding the first three were within 2%).
### Legendary Hunter's Chest — EV 11.5M (old 10.6M), scale 2.00
- Common 55%: Parchment Core ×20 | Cracked Auditory Core ×20 | Mask Core ×20 | Shard of Willful Steel ×20 | Thread Core ×20
- Rare 25%: Cracked Auditory Core ×10 + Mask Core ×10 | Mask Core ×10 + Parchment Core ×10 | Mask Core ×10 + Parchment Core ×10 + Shard of Willful Steel ×10 | Parchment Core ×10 + Shard of Willful Steel ×10 + Thread Core ×10 | Shard of Willful Steel ×10 + Thread Core ×10
- Epic 12%: Parchment Core ×60 | Cracked Auditory Core ×60 | Mask Core ×60
- Legendary 8%: Mask Core ×20 + Parchment Core ×20 + Shard of Willful Steel ×20 | Parchment Core ×20 + Shard of Willful Steel ×20 + Thread Core ×20

### Epic Hunter's Chest — EV 6.7M (old 7.0M), scale 5.00
- Common 56%: Moonpetal Weave ×25 | Ofuda Moss ×25 | Urami Drop ×25 | Yamidangan ×25 | Seika Seal Petal ×25 | Tsukinari Bell ×25
- Rare 26%: Moonpetal Weave ×10 + Yamidangan ×10 | Ofuda Moss ×10 + Yamidangan ×10 | Ofuda Moss ×10 + Tsukinari Bell ×10 | Ofuda Moss ×10 + Seika Seal Petal ×10 + Urami Drop ×10 | Seika Seal Petal ×10 + Urami Drop ×10
- Epic 12%: Moonpetal Weave ×75 | Ofuda Moss ×75 | Urami Drop ×75
- Legendary 6%: Parchment Core ×25 | Cracked Auditory Core ×25 | Mask Core ×25 | Shard of Willful Steel ×25

### Rare Hunter's Chest — EV 5.6M (old 6.0M), scale 9.00
- Common 56%: Ashrend Wing ×25 | Brasel Spine ×25 | Glimmerchitin ×25 | Lurethorne ×25 | Voltleaf Plume ×25 | Frostscale ×25
- Rare 26%: Ashrend Wing ×10 + Brasel Spine ×10 | Ashrend Wing ×10 + Frostscale ×10 + Glimmerchitin ×10 | Brasel Spine ×10 + Voltleaf Plume ×10 | Ashrend Wing ×10 + Glimmerchitin ×10 | Frostscale ×10 + Voltleaf Plume ×10 | Frostscale ×10 + Lurethorne ×10 + Voltleaf Plume ×10 | …
- Epic 12%: Ashrend Wing ×80 | Brasel Spine ×80 | Glimmerchitin ×80
- Legendary 6%: Moonpetal Weave ×10 | Ofuda Moss ×10 | Urami Drop ×10 | Yamidangan ×10

### Common Hunter's Chest — EV 3.9M (old 4.2M), scale 13.00
- Common 56%: Owlcat's Fur ×25 | Glimmer Dust ×25 | Moonlight Antlers ×25 | Mosswolf Tuft ×25 | Badger Shell ×25 | Rust Ferret Pelt ×25
- Rare 26%: Owlcat's Fur ×10 + Rust Ferret Pelt ×10 | Glimmer Dust ×10 + Moonlight Antlers ×10 | Badger Shell ×10 + Glimmer Dust ×10 + Moonlight Antlers ×10 + Owlcat's Fur ×10 | Badger Shell ×10 + Glimmer Dust ×10 + Rust Ferret Pelt ×10 | Mosswolf Tuft ×10 + Owlcat's Fur ×10
- Epic 12%: Owlcat's Fur ×80 | Glimmer Dust ×80 | Moonlight Antlers ×80
- Legendary 6%: Ashrend Wing ×10 | Brasel Spine ×10 | Glimmerchitin ×10 | Lurethorne ×10

### Legendary Gatherer's Chest — EV 10.5M (old 10.0M), scale 2.00
- Common 55%: Mithril Ore ×20 | Phoenix Ash Bloom ×20 | Heart of Kuraokami ×20 | Lunaris Bloom ×20 | Tempest Heart ×20 | Voidshade Petal ×20 | …
- Rare 25%: Fujin's Breath ×10 + Heart of Kuraokami ×10 | Fujin's Breath ×10 + Mithril Ore ×10 | Heart of Kuraokami ×10 + Mithril Ore ×10 | Mithril Ore ×10 + Voidshade Petal ×10 | Mithril Ore ×10 + Orichalcum Ore ×10 | Orichalcum Ore ×10 + Tempest Heart ×10 + Voidshade Petal ×10 | …
- Epic 12%: Mithril Ore ×60 | Phoenix Ash Bloom ×60 | Heart of Kuraokami ×60
- Legendary 8%: Orichalcum Ore ×20 + Tempest Heart ×20 + Voidshade Petal ×20 | Lunaris Bloom ×20 + Phoenix Ash Bloom ×20 + Voidshade Petal ×20 | Fujin's Breath ×20 + Lunaris Bloom ×20 + Phoenix Ash Bloom ×20 | Fujin's Breath ×20 + Lunaris Bloom ×20 + Orichalcum Ore ×20

### Epic Gatherer's Chest — EV 5.4M (old 5.5M), scale 5.00
- Common 56%: Rainbow Cabochon ×25 | Adamantine Ore ×25 | Celestial Thristle ×25 | Icewarden Root ×25 | Shadeleaf ×25 | Susanoo's Tear ×25 | …
- Rare 26%: Celestial Thristle ×10 + Shadeleaf ×10 | Adamantine Ore ×10 + Icewarden Root ×10 + Rainbow Cabochon ×10 | Celestial Thristle ×10 + Susanoo's Tear ×10 | Diamond Ore ×10 + Susanoo's Tear ×10 | Adamantine Ore ×10 + Ember Frond ×10 + Icewarden Root ×10 + Shadeleaf ×10 | Adamantine Ore ×10 + Diamond Ore ×10 + Shadeleaf ×10 | …
- Epic 12%: Rainbow Cabochon ×75 | Adamantine Ore ×75 | Celestial Thristle ×75
- Legendary 6%: Mithril Ore ×25 | Phoenix Ash Bloom ×25 | Heart of Kuraokami ×25 | Lunaris Bloom ×25

### Rare Gatherer's Chest — EV 4.5M (old 4.8M), scale 9.00
- Common 56%: Galecrest Sage ×25 | Gold Ore ×25 | Silver Ore ×25 | Shiverthorn ×25 | Solar Petal ×25 | Starfire Petal ×25 | …
- Rare 26%: Gold Ore ×10 + Shiverthorn ×10 + Starfire Petal ×10 + Wraithbloom ×10 | Galecrest Sage ×10 + Solar Petal ×10 | Gold Ore ×10 + Silver Ore ×10 + Starfire Petal ×10 | Solar Petal ×10 + Wraithbloom ×10 | Gold Ore ×10 + Silver Ore ×10 | Shiverthorn ×10 + Solar Petal ×10 + Wraithbloom ×10 | …
- Epic 12%: Galecrest Sage ×80 | Gold Ore ×80 | Silver Ore ×80
- Legendary 6%: Rainbow Cabochon ×10 | Adamantine Ore ×10 | Celestial Thristle ×10 | Icewarden Root ×10

### Common Gatherer's Chest — EV 3.2M (old 3.2M), scale 17.00
- Common 56%: Murkshade ×35 | Sunroot ×35 | Copper Ore ×35 | Iron Ore ×35 | Whistlegrass ×35 | Moonveil Moss ×35 | …
- Rare 26%: Murkshade ×15 + Whistlegrass ×15 | Iron Ore ×15 + Murkshade ×15
- Epic 12%: Murkshade ×100 | Sunroot ×100 | Copper Ore ×100
- Legendary 6%: Galecrest Sage ×15 | Gold Ore ×15 | Silver Ore ×15 | Shiverthorn ×15

## Settled
- Tier weights and the 3/4/6 roll distribution: approved (RUL-2026-10-29-036).
- No Upgrade tier; Seed of False Vitality out (RUL-2026-10-29-036).
- One combined chest kind, not separate kit and stockpile chests (RUL-2026-10-29-037).
- Cross-rarity recipe kits: not used. Each kit stays inside its chest's rarity.
