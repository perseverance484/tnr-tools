# Skyglass item description audit (Lane B review, 2026-10-31)

**Type:** review only. No manifest, generator or design doc was edited. Zero live game requests, no credentials.
**Base:** `perseverance484/tnr-tools` main at `2490b51107c2aea5e3181fa1a1e18448497ea8ed`.
**Goal (director, 2026-10-31):** players can't see drop rates in game, so every container lists its drops and rates in
its description, in the house format. Every other Skyglass item says what it is for, with story and mechanics blended in
one voice (not a lore line followed by a separate rules dump).

## Summary

**49 items audited** (16 containers, 33 non-containers): **41 FIX, 8 OK**, plus two format-wide findings (C1, C2) that
touch all 16 containers.

**Data integrity is clean.** For all 16 containers, description, loot-table doc and manifest data agree exactly (tiers
sum to 100%, RUL-2026-10-29-058 names and colours, roll and `Always:` lines). Manifest text equals `SKYGLASS_TEXT.md`
(45 checked, 0 differences). The 8 profession chest tables in push/339 equal `state/skyglass_design/chests.json`.
`scripts/skyglass_check.py`: 0 errors, 0 warnings. The fixes are about what the text leaves out and how it reads.

**Important fixes**
1. **C1. Profession chests hide drops.** The "list three, then *and more*" rule (loot tables §0) hides options in all 8
   chests, and within a tier options are not equally likely (entries are duplicated to weight by recipe demand; the
   engine picks one entry uniformly, theninjarpg `libs/weightedCache.ts`). Full-listing text in §4. Needs a ruling
   amending loot tables §0 / RUL-2026-10-28-030, plus a Lane A change to `skyglass_check.py` `tier_items_text` and
   `push/skyglass_items.gen.py` `tier_line`.
2. **C2. Tier colours fail contrast.** Dark item card: blue, purple, red 2.6-2.8:1. Light themes: grey, gold 1.9-2.5:1.
   No single hex reaches 3:1 on both. Proposal (§2): colour a ◆ glyph, keep the label in the theme's text colour.
   Director decision; Lane A `TIER_LINE` change. The §0 phone check is not recorded anywhere.
3. **N1. Captain's Watch chart omits its kept press-on room** (RUL-2026-10-30-060 item 6, -062 item 2).
4. **N2. Boss-token template doubles "the"** ("unlock the The First Blade variant").
5. **N3. Coffer contents (live, no manifest):** Filament and Katana use the banned word "lattice"; the Filament says the
   seals keep the ship "aloft"; the Fragment never says five make The Skyglass Crown; live rarities contradict RUL-058
   (Filament RARE → Common, Serum LEGENDARY → Rare, Fragment LEGENDARY → Epic).
6. **N4. Blended style.** All 28 player-obtainable non-containers use story-then-rules (text doc §4). Replacements in
   §5-§9; adopting them changes the §4 header rule (record as a ruling).
7. **Smaller:** Core Rot has no sources and says "the tainted chart" (RUL-058 item 4: name the tier); Trophy Hold page
   says "the hunters' trophies"; Haul pages are 690-736 characters with a 282-character rules line.

**Where fixes land**
- **Live, edited by go-live 339 (not yet run): 20 records.** Fix `SKYGLASS_TEXT.md` and the renderer (C1), regenerate 339.
- **New and hidden, created by 329/346/348 (already run): 23 records.** Need a new item-edit pass.
- **Live, covered by no manifest: the 4 Coffer contents (and the Skyglass Crystal).** New edit; proposed carrier 339
  phase 1, text in a new `SKYGLASS_TEXT.md` §4.6.

**Inferred facts (director to confirm):** (i) pick options and drops for the unbuilt runs come from loot tables
§4a/§5; (ii) twelve Filaments craft a Skyglass Crystal (RULINGS ~2917); (iii) five Fragments make The Skyglass Crown
(`GHOST_SHIP_SKYGLASS_FULL_MANIFEST_ROADMAP.md` line 67); (iv) Little Horror numbers (RUL-068/-070), pets fight only in
quest battles, while loot tables §5b still lists dungeons; (v) variants unlock from the weapon's Variants list;
(vi) Core Rot sources leave out "breaking the seal" (not built); (vii) the Burning Heading afterburn wording is kept.

**Not done:** no live read-back, no phone render; contrast computed from theninjarpg@2af4b320 CSS tokens
(`styles/globals.css`, `layout/ItemWithEffects.tsx`), not measured on a device.

## 1. Where each record lives

| Record | Status | Fix carrier |
|---|---|---|
| 4 Rare charts (Buried Cache, Drowned Foundry, Quarantined Archive, Captain's Watch) | live; edited by 339 | text doc §4.1 → regenerate 339 |
| Lastlight Lantern | live; edited by 339 | §4.1 → regenerate 339 |
| Coffer, Sealed Treasury, Archive Chart Case, Medicine Inro, Sage's Strongbox, Elemental Tool Pouch, Unmarked Cargo | live; edited by 339 | §4.4 → regenerate 339 |
| 8 profession chests | live; edited by 339 | §4.5 + `tier_line` → regenerate 339 |
| Tide Chart, Watch Roster, Reliquary Seal, The Last Heading, Rotted Reliquary Seal, The Rotted Heading | new, hidden (329) | §4.1 → new item edit |
| 6 Haul pages | new, hidden (329) | §3.2 → new item edit |
| Core Rot, Galley Stores | new, hidden (329) | §4.2 → new item edit |
| Skyglass Token, 7 boss tokens | new, hidden (329, 338) | §4.3 → new item edit |
| The Little Horror's Jar | new, hidden (346) | §4.2 → new item edit |
| Crown's Hoard | new, hidden (348) | new edit only if C2 adopted |
| Countermand | hidden boss item | none |
| Skyglass Filament, Serum, Fragment, Katana (and Crystal) | live; no manifest | new edit (339 phase 1; new §4.6) |

## 2. Format-wide findings

### C1: "and more" hides drops; within-tier rates are unequal

| Chest | Hidden by "and more" | Unequal within a tier |
|---|---|---|
| Common Hunter's | Common 3/6, Rare 2/5 kits, Legendary 1/4 | Common 11/11/8.4×4% |
| Rare Hunter's | Common 3/6, Rare 7/10, Legendary 1/4 | Common 12/8.8×5% |
| Epic Hunter's | Common 3/6, Rare 2/5, Legendary 1/4 | Common 10×4/7.6×2% |
| Legendary Hunter's | Common 2/5, Rare 2/5 | equal |
| Common Gatherer's | Common 5/8, Legendary 1/4 | Common 12/12/8.8/8.8/5.9/2.9×3% |
| Rare Gatherer's | Common 5/8, Rare 8/11, Legendary 1/4 | Common 8.8×3/5.9×5% |
| Epic Gatherer's | Common 6/9, Rare 6/9, Legendary 1/4 | equal |
| Legendary Gatherer's | Common 5/8, Rare 9/12, Legendary 1/4 | Common 7.2×7/4.8% |

**Proposed rule** (replaces loot tables §0's "more than 3 options" bullet): list every option; a tier of unequal single
stacks reads `one stack ×n:` then each item with its per-roll rate; equal options add `(x% each)`; a recipe-kit tier with
more than 2 kits reads `a recipe kit of a–b materials ×n each (k kits, x% each), drawn from: <materials>`; rates per roll,
one decimal under 10%, whole percent from 10%. Carriers: loot tables §0, text doc §4.5, `skyglass_items.gen.py`
`tier_line`, `skyglass_check.py` (Lane A).

### C2: tier colour contrast

| Colour | dark popover | dark card | light popover | light card | reading cream |
|---|---|---|---|---|---|
| grey #9ca3af | 4.02 | 5.84 | **2.25** | **2.45** | **2.29** |
| blue #3b82f6 | **2.78** | 4.03 | 3.26 | 3.54 | 3.32 |
| purple #a855f7 | **2.58** | 3.75 | 3.51 | 3.81 | 3.58 |
| gold #f59e0b | 4.75 | 6.90 | **1.90** | **2.07** | **1.94** |
| red #ef4444 | **2.71** | 3.94 | 3.34 | 3.63 | 3.40 |

Recommended: `<span style="color:#a855f7">◆</span> <b>Epic 5%</b> · Fragment of the Skyglass Crown`. Carriers:
RUL-2026-10-28-030 template, text doc §4.4/§4.5, `tier_line`, `skyglass_check.py` `TIER_LINE` (Lane A).

## 3. Containers

| Item | Status | Notes |
|---|---|---|
| Skyglass Coffer | OK (C2) | 69/24/5/2; contents' card rarities contradict the tier labels (N3) |
| Sealed Treasury | OK (C2) | `Always:` 150,000 ryo; 3/4/6 rolls at 60/30/10; 45/35/15/5 |
| Archive Chart Case | OK (C2) | 45/25/20/7 (3.5 each)/Forbidden 3 |
| Medicine Inro | OK (C2) | 2 rolls; 70/22/7/1 |
| Sage's Strongbox | OK (C2) | 65/26/8/1 |
| Elemental Tool Pouch | OK (C2) | `Always:` Elemental Kunai ×10; 70/25/5 |
| Unmarked Cargo | OK (C2) | 40/35/18/7 |
| Crown's Hoard | OK (C2) | two caches under their own headings |
| 8 profession chests | **FIX** (C1, C2) | §4 |

Doc-only: `SKYGLASS_PROFESSION_CHESTS.md` still uses the pre-RUL-058 tier names and the superseded "professionals'
rewards stay the same" goal.

## 4. Proposed profession chest text (C1; current colours)

**Common Hunter's Chest**
```html
<i>A hunter's sea-chest from the ship's stores: the everyday take, cured and logged.</i><br><br><i>3–6 rolls.</i><br><b>Each roll:</b><br><span style="color:#9ca3af"><b>Common 56%</b></span> · one stack ×26: Owlcat's Fur 11%, Glimmer Dust 11%, Moonlight Antlers 8.4%, Mosswolf Tuft 8.4%, Badger Shell 8.4%, Rust Ferret Pelt 8.4%<br><span style="color:#3b82f6"><b>Rare 26%</b></span> · a recipe kit of 2–4 materials ×12 each (5 kits, 5.2% each), drawn from: Badger Shell, Glimmer Dust, Moonlight Antlers, Mosswolf Tuft, Owlcat's Fur, Rust Ferret Pelt<br><span style="color:#a855f7"><b>Epic 12%</b></span> · Owlcat's Fur ×78 <i>or</i> Glimmer Dust ×78 <i>or</i> Moonlight Antlers ×78 (4% each)<br><span style="color:#f59e0b"><b>Legendary 6%</b></span> · Ashrend Wing ×12 <i>or</i> Brasel Spine ×12 <i>or</i> Glimmerchitin ×12 <i>or</i> Lurethorne ×12 (1.5% each)
```

**Rare Hunter's Chest**
```html
<i>A hunter's chest of the rarer game the ship took along the coastlines.</i><br><br><i>3–6 rolls.</i><br><b>Each roll:</b><br><span style="color:#9ca3af"><b>Common 56%</b></span> · one stack ×27: Ashrend Wing 12%, Brasel Spine 8.8%, Glimmerchitin 8.8%, Lurethorne 8.8%, Voltleaf Plume 8.8%, Frostscale 8.8%<br><span style="color:#3b82f6"><b>Rare 26%</b></span> · a recipe kit of 2–4 materials ×12 each (10 kits, 2.6% each), drawn from: Ashrend Wing, Brasel Spine, Frostscale, Glimmerchitin, Lurethorne, Voltleaf Plume<br><span style="color:#a855f7"><b>Epic 12%</b></span> · Ashrend Wing ×81 <i>or</i> Brasel Spine ×81 <i>or</i> Glimmerchitin ×81 (4% each)<br><span style="color:#f59e0b"><b>Legendary 6%</b></span> · Moonpetal Weave ×12 <i>or</i> Ofuda Moss ×12 <i>or</i> Urami Drop ×12 <i>or</i> Yamidangan ×12 (1.5% each)
```

**Epic Hunter's Chest**
```html
<i>A hunter's chest of strange catches from the high air, sealed under the Warden's mark.</i><br><br><i>3–6 rolls.</i><br><b>Each roll:</b><br><span style="color:#9ca3af"><b>Common 56%</b></span> · one stack ×25: Moonpetal Weave 10%, Ofuda Moss 10%, Urami Drop 10%, Yamidangan 10%, Seika Seal Petal 7.6%, Tsukinari Bell 7.6%<br><span style="color:#3b82f6"><b>Rare 26%</b></span> · a recipe kit of 2–3 materials ×10 each (5 kits, 5.2% each), drawn from: Moonpetal Weave, Ofuda Moss, Seika Seal Petal, Tsukinari Bell, Urami Drop, Yamidangan<br><span style="color:#a855f7"><b>Epic 12%</b></span> · Moonpetal Weave ×75 <i>or</i> Ofuda Moss ×75 <i>or</i> Urami Drop ×75 (4% each)<br><span style="color:#f59e0b"><b>Legendary 6%</b></span> · Parchment Core ×25 <i>or</i> Cracked Auditory Core ×25 <i>or</i> Mask Core ×25 <i>or</i> Shard of Willful Steel ×25 (1.5% each)
```

**Legendary Hunter's Chest**
```html
<i>The hunt-master's own chest: the best of decades, sealed and never drawn.</i><br><br><i>3–6 rolls.</i><br><b>Each roll:</b><br><span style="color:#9ca3af"><b>Common 55%</b></span> · one stack ×20 (11% each): Parchment Core, Cracked Auditory Core, Mask Core, Shard of Willful Steel, Thread Core<br><span style="color:#3b82f6"><b>Rare 25%</b></span> · a recipe kit of 2–3 materials ×10 each (5 kits, 5% each), drawn from: Cracked Auditory Core, Mask Core, Parchment Core, Shard of Willful Steel, Thread Core<br><span style="color:#a855f7"><b>Epic 12%</b></span> · Parchment Core ×60 <i>or</i> Cracked Auditory Core ×60 <i>or</i> Mask Core ×60 (4% each)<br><span style="color:#f59e0b"><b>Legendary 8%</b></span> · Mask Core ×20 + Parchment Core ×20 + Shard of Willful Steel ×20 <i>or</i> Parchment Core ×20 + Shard of Willful Steel ×20 + Thread Core ×20 (4% each)
```

**Common Gatherer's Chest**
```html
<i>The quartermaster's crate of everyday ore and root, cut from the hull and logged.</i><br><br><i>3–6 rolls.</i><br><b>Each roll:</b><br><span style="color:#9ca3af"><b>Common 56%</b></span> · one stack ×34: Murkshade 12%, Sunroot 12%, Copper Ore 8.8%, Iron Ore 8.8%, Whistlegrass 5.9%, Moonveil Moss 2.9%, Muskshade 2.9%, Nightshade Thorn 2.9%<br><span style="color:#3b82f6"><b>Rare 26%</b></span> · Murkshade ×16 + Whistlegrass ×16 <i>or</i> Iron Ore ×16 + Murkshade ×16 (13% each)<br><span style="color:#a855f7"><b>Epic 12%</b></span> · Murkshade ×100 <i>or</i> Sunroot ×100 <i>or</i> Copper Ore ×100 (4% each)<br><span style="color:#f59e0b"><b>Legendary 6%</b></span> · Galecrest Sage ×16 <i>or</i> Gold Ore ×16 <i>or</i> Silver Ore ×16 <i>or</i> Shiverthorn ×16 (1.5% each)
```

**Rare Gatherer's Chest**
```html
<i>A gatherer's crate of the rarer ore and bloom, sealed against the damp.</i><br><br><i>3–6 rolls.</i><br><b>Each roll:</b><br><span style="color:#9ca3af"><b>Common 56%</b></span> · one stack ×27: Galecrest Sage 8.8%, Gold Ore 8.8%, Silver Ore 8.8%, Shiverthorn 5.9%, Solar Petal 5.9%, Starfire Petal 5.9%, Widow's Kiss 5.9%, Wraithbloom 5.9%<br><span style="color:#3b82f6"><b>Rare 26%</b></span> · a recipe kit of 2–4 materials ×12 each (11 kits, 2.4% each), drawn from: Galecrest Sage, Gold Ore, Shiverthorn, Silver Ore, Solar Petal, Starfire Petal, Widow's Kiss, Wraithbloom<br><span style="color:#a855f7"><b>Epic 12%</b></span> · Galecrest Sage ×81 <i>or</i> Gold Ore ×81 <i>or</i> Silver Ore ×81 (4% each)<br><span style="color:#f59e0b"><b>Legendary 6%</b></span> · Rainbow Cabochon ×12 <i>or</i> Adamantine Ore ×12 <i>or</i> Celestial Thristle ×12 <i>or</i> Icewarden Root ×12 (1.5% each)
```

**Epic Gatherer's Chest**
```html
<i>A gatherer's crate of crystal-grown ore and blooms the skyglass got into.</i><br><br><i>3–6 rolls.</i><br><b>Each roll:</b><br><span style="color:#9ca3af"><b>Common 56%</b></span> · one stack ×25 (6.2% each): Rainbow Cabochon, Adamantine Ore, Celestial Thristle, Icewarden Root, Shadeleaf, Susanoo's Tear, Tempest Thorn, Ember Frond, Diamond Ore<br><span style="color:#3b82f6"><b>Rare 26%</b></span> · a recipe kit of 2–4 materials ×10 each (9 kits, 2.9% each), drawn from: Adamantine Ore, Celestial Thristle, Diamond Ore, Ember Frond, Icewarden Root, Rainbow Cabochon, Shadeleaf, Susanoo's Tear<br><span style="color:#a855f7"><b>Epic 12%</b></span> · Rainbow Cabochon ×75 <i>or</i> Adamantine Ore ×75 <i>or</i> Celestial Thristle ×75 (4% each)<br><span style="color:#f59e0b"><b>Legendary 6%</b></span> · Mithril Ore ×25 <i>or</i> Phoenix Ash Bloom ×25 <i>or</i> Heart of Kuraokami ×25 <i>or</i> Lunaris Bloom ×25 (1.5% each)
```

**Legendary Gatherer's Chest**
```html
<i>The quartermaster's reserve, sealed by his own hand and marked never to be drawn.</i><br><br><i>3–6 rolls.</i><br><b>Each roll:</b><br><span style="color:#9ca3af"><b>Common 55%</b></span> · one stack ×20: Mithril Ore 7.2%, Phoenix Ash Bloom 7.2%, Heart of Kuraokami 7.2%, Lunaris Bloom 7.2%, Tempest Heart 7.2%, Voidshade Petal 7.2%, Fujin's Breath 7.2%, Orichalcum Ore 4.8%<br><span style="color:#3b82f6"><b>Rare 25%</b></span> · a recipe kit of 2–3 materials ×10 each (12 kits, 2.1% each), drawn from: Fujin's Breath, Heart of Kuraokami, Lunaris Bloom, Mithril Ore, Orichalcum Ore, Phoenix Ash Bloom, Tempest Heart, Voidshade Petal<br><span style="color:#a855f7"><b>Epic 12%</b></span> · Mithril Ore ×60 <i>or</i> Phoenix Ash Bloom ×60 <i>or</i> Heart of Kuraokami ×60 (4% each)<br><span style="color:#f59e0b"><b>Legendary 8%</b></span> · Orichalcum Ore ×20 + Tempest Heart ×20 + Voidshade Petal ×20 <i>or</i> Lunaris Bloom ×20 + Phoenix Ash Bloom ×20 + Voidshade Petal ×20 <i>or</i> Fujin's Breath ×20 + Lunaris Bloom ×20 + Phoenix Ash Bloom ×20 <i>or</i> Fujin's Breath ×20 + Lunaris Bloom ×20 + Orichalcum Ore ×20 (2% each)
```

## 5. Charts and the Lantern (blended style; all FIX)

Pick options from loot tables §4a (inferred i).

**Tide Chart**
```html
The Wayfinder's tide table, marked where the low tide opens the wreck's lower hull. Take it to the <b>Battle Arena</b> and slip in for <b>The Low Tide Run</b>: three fights against the crew, scaled to you, and the chart is spent the moment you go in.<br><br>Health and chakra carry from fight to fight with no refills, and one lost fight ends the run. Come out the far side to choose a <b>Medicine Inro</b>, <b>Galley Stores</b> or a <b>Watch Roster</b>, with a chance at the Chart of the Buried Cache and Core Rot.
```

**Watch Roster**
```html
The Deck Warden's duty roster, with a new name at the bottom in fresh ink: yours. Take it to the <b>Battle Arena</b> to stand <b>The Night Watch</b>, three watches back to back against crew scaled to you; the roster is spent when the first watch starts.<br><br>Health and chakra carry from watch to watch, and one lost fight ends it. After the last watch, end your watch with what you hold, or stand the <b>Second Watch</b> for more and keep only what you held if you fall. Clear it to choose a <b>Medicine Inro</b>, <b>Galley Stores</b> or a <b>Tide Chart</b>.
```

**Chart of the Buried Cache**
```html
A salt-stained chart of a field cache the crew buried on the shore before the ship vanished. Take it to the <b>Battle Arena</b> to dig up <b>The Buried Cache</b>, guarded by crew scaled to you; the chart is spent when you set out.<br><br>Health and chakra carry from fight to fight, and one lost fight ends the run. Reach the cache to choose a <b>Medicine Inro</b>, <b>Galley Stores</b> or a <b>Chart of the Drowned Foundry</b>, with a small chance at a Haul page.
```

**Chart of the Drowned Foundry**
```html
A waterlogged chart of the wreck's keel, where the drowned foundry still pours. Take it to the <b>Battle Arena</b> to go down into <b>The Drowned Foundry</b>; the chart is spent at the first step, and there is no way out but through the crucible and the Foundry Warden.<br><br>Health and chakra carry from fight to fight, and one lost fight ends the run. Win to choose an <b>Elemental Tool Pouch</b>, <b>Medicine Inro</b> or <b>Galley Stores</b>, with a chance at the Archive's chart and a Haul page.
```

**Chart of the Quarantined Archive**
```html
A chart that shows a sealed chamber missing from every other plan of the wreck. Take it to the <b>Battle Arena</b> to break into <b>The Quarantined Archive</b>; the chart is spent at the door. Three seals bar the way, and a wrong answer brings the archive's guard and a smaller haul.<br><br>Health and chakra carry from fight to fight, and one lost fight ends the run. Clear it to choose an <b>Archive Chart Case</b>, <b>Sage's Strongbox</b> or <b>Skyglass Token</b>, with a chance at the <b>Reliquary Seal</b>, an Epic chart.
```

**Chart of the Captain's Watch** (adds the press-on room, N1)
```html
The Captain's own chart of the command decks. Take it to the <b>Battle Arena</b> to stand <b>The Captain's Watch</b>; the chart is spent when the watch begins. Before each fight the Oathkeeper offers a term, and every term you take and survive makes the fight harder and the haul bigger.<br><br>Health and chakra carry, and one lost fight ends the run. At the end, claim the watch's stores, or stand the <b>dawn watch</b> for a better shot at <b>The Last Heading</b> and keep only what you held if you fall. Clear it to choose a <b>Skyglass Coffer</b>, <b>1,000,000 ryo</b> or a <b>Skyglass Token</b>.
```

**Reliquary Seal**
```html
The seal of the iron reliquary chained behind the Sealwright, where the echoes the Core could not hold were locked away. It opens two ways.<br><br><b>Run it</b> at the <b>Battle Arena</b>: <b>The Sealed Reliquary</b>, four echoes back to back, each leaving its mark on the floor when it falls. The seal is spent when you enter; health and chakra carry, and a loss ends the run but leaves you 1 Core Rot. Clear it to choose two Skyglass Coffers, a Sealed Treasury, two Skyglass Tokens or two Archive Chart Cases.<br><br><b>Steep it</b> by using it from your inventory: pour in 3 Core Rot and fight what the rot builds. Win and it becomes the <b>Rotted Reliquary Seal</b>, a Legendary chart. Lose and the seal comes back, but the Rot is spent. Short of Rot? Take it back and nothing is spent.
```

**The Last Heading**
```html
The Wayfinder's final course: the night the ship came down, as the Core still replays it. It opens two ways.<br><br><b>Run it</b> at the <b>Battle Arena</b>: <b>The Fall</b>, the burning decks and then the Core as it breaks. The heading is spent when you board; health and chakra carry, and a loss ends the run but leaves you 1 Core Rot. After the break, get off with what you hold or climb to the helm, and keep only what you held if you fall there. Clear it to choose two Skyglass Coffers, a Sealed Treasury, two Skyglass Tokens or three Galley Stores.<br><br><b>Steep it</b> by using it from your inventory: pour in 3 Core Rot and fight what the rot builds. Win and it becomes <b>The Rotted Heading</b>, a Legendary chart. Lose and the heading comes back, but the Rot is spent. Short of Rot? Take it back and nothing is spent.
```

**Rotted Reliquary Seal**
```html
The Reliquary Seal after a long soak in the Core's rot, steeped to open the reliquary the rot remembers. Take it to the <b>Battle Arena</b> to run <b>The Rotted Reliquary</b>; the seal is spent when you enter. You go in already worn, at 70% health and chakra, the echoes come out in pairs, and the rot clogs your elemental jutsu for the first 2 rounds of every fight.<br><br>Nothing refills, and one lost fight ends the run. After the last pair, leave with what you hold or open the door the rot added, and keep only what you held if you fall. Win and you <b>pick 2</b> rewards, not 1.
```

**The Rotted Heading**
```html
The Last Heading, steeped in rot until it runs the night of the fall backwards. Take it to the <b>Battle Arena</b> to run <b>The Burning Heading</b>; the heading is spent when you start. You wake in the break at 70% health and chakra, and fire catches you at the start of every fight, so the damage you take burns again.<br><br>Fight your way out through the decks with no refills; one lost fight ends the run. You will not fight all of it alone. Win and you <b>pick 2</b> rewards, not 1.
```

**Lastlight Lantern**
```html
Crownhold's final signal, caught in a skyglass lantern. It still burns with the last order the crew obey, and its light points home. Take it to the <b>Battle Arena</b> to follow the light to <b>Crownhold</b>, the mountain fortress at the end of the story; the Lantern is spent when the expedition sets out.<br><br>Health carries from fight to fight, and one lost fight ends the expedition, so claim any reward choice still waiting from an earlier run first. At the throne, choose the <b>Crown's Hoard</b>, three Skyglass Coffers, a Fragment of the Skyglass Crown, or Crownhold's own badge and jutsu.
```

## 6. Haul pages (blended style and length; Trophy Hold also "trophies")

Template (per page: `<story>`, `<page>`, `<chests>`). Facts from `SKYGLASS_THE_HAUL.md` "The run".
```html
<story>. Take it to the <b>Battle Arena</b> to raid <b><page></b>; the page is spent when you go in.<br><br>Up to 5 steps deep, you choose each time: a <b>crate</b> for a chest and a crew fight; a sealed <b>locker</b> for a better chest and a shot at a bonus one, against harder guards and a hazard; or <b>cut through</b> where the way allows, with no fight now but a hazard waiting in the next. Every locker puts the stores on alert. Health and chakra never refill. Leave whenever you like with your haul of <b><chests> Chests</b>, Common up to Legendary; lose a fight and you leave with nothing.
```

| Page | `<story>` |
|---|---|
| Ledger Page: The Trophy Hold | A page torn from the Arsenal Keeper's ledger: hides, horn and the hunters' prizes, sealed below the gun deck, every due date crossed out and written again |
| Ledger Page: The Bone Store | A page from the Keeper's ledger for the bone store: horn, tusk and antler, the best of it sealed nearest the door |
| Ledger Page: The Snare Room | The trapper's page of the ledger, stained with old bait, listing every snare he ever set and none marked as taken down |
| Stores Manifest: The Overgrown Stores | The quartermaster's manifest for the lower stores, ore, root and bloom cut from the hull and sealed, with skyglass grown through every line since |
| Stores Manifest: The Ore Vault | The manifest for the ore vault, weighed twice and signed three times, for the best guarded metal below decks |
| Stores Manifest: The Bloom Cellar | The manifest for the drying cellar, its ink faded to the colour of old petals and its last line a warning about the dust |

About 620-650 characters (from 690-736). Carrier: text doc §3.2 and `skyglass_items.gen.py` `haul_pages()`, as a new item edit.

## 7. Core Rot, Galley Stores, the Little Horror's Jar

**Core Rot** (inferred vi)
```html
What the Core leaves behind when it rebuilds an impression badly: wet timber, rotten rope and skyglass gone cloudy. It turns up after endgame Wreck clears, the Low Tide Run and the Night Watch, in The Fall and the rotted runs, and as consolation when an Epic run goes wrong.<br><br>Its one use is <b>steeping</b>. Use an Epic chart (the Reliquary Seal or The Last Heading) from your inventory, pour in <b>3 Core Rot</b> and fight what the rot builds. Win and the chart comes out a Legendary chart: the Rotted Reliquary Seal or The Rotted Heading. Lose and you get the chart back, but the Rot is gone. Short of 3? Take the chart back at the start and nothing is spent.
```

**Galley Stores**
```html
The galley still stocks a larder for a crew that does not eat, and a companion that does grows strong on it. Use it to feed <b>20,000 pet experience</b> to your active pet. The pet must be battle-ready and not away on a task; if no pet can eat, the stores spoil and the experience is lost.
```

**The Little Horror's Jar** (inferred iv)
```html
One of the Skyglass Project's first recalls was the ship's mascot, sealed in a jar. The Core tried to remember it, and this is what came back. Open the jar to bind the <b>Little Horror</b> to you as a Legendary pet. It answers to you, not the crown, and fights beside you in quest battles such as chart runs and the Haul: while it is out, enemies deal 10% less damage, and it bites 20% harder.<br><br>The jar will not open while your pet collection is full; it waits in your inventory until you make room.
```

## 8. Tokens

**Skyglass Token** (inferred v)
```html
A token pressed from clouded skyglass and stamped with the four-point star. Spend it from one of your crafted weapons' variants to unlock its <b>Skyglass variant</b>: a new look and name, the same stats. You must own the weapon, each variant unlocks once per player, and the token is used up.<br><br>Skyglass variants exist for Aetherion, Thornsilver, Night's Testament, Stormrender, Oathbinder, Ink of the Void, The Unwritten, Gaea's Embrace, Warden's Bracers, Eclipsed Dawnblade, Zephyr's Whisper and Yuki's Frostbite.
```

**Boss variant token template** (fixes N2; story lines in text doc §4.3 unchanged)
```html
<story line> Spend it on <b><Base></b> to unlock its variant <b><Variant></b>: a new look and name, the same stats. You must own <Base>; the variant unlocks once per player, and the token is used up.
```
The Crownbreaker token stays hidden until Walked Every Deck (RUL-2026-10-31-069).

## 9. Countermand and the Coffer contents

| Item | Status | Finding | Proposed |
|---|---|---|---|
| Countermand | OK | hidden boss item | none |
| Skyglass Filament (live RARE) | **FIX** | "lattice"; "aloft" stale; RUL-058 says Common | `A hair-thin strand of skyglass pulled from the wreck's hull, still holding the shape of the seals that kept the ship in the sky. Twelve can be worked into a <b>Skyglass Crystal</b>.` (inferred ii) + rarity COMMON |
| Skyglass Serum (live LEGENDARY) | **FIX** | RUL-058 says Rare | rarity RARE only |
| Fragment of the Skyglass Crown (live LEGENDARY) | **FIX** | no use stated; RUL-058 says Epic | `A shard of the Skyglass Crown, threaded with dormant command seals. Gather five and they can be joined into <b>The Skyglass Crown</b>.` (inferred iii) + rarity EPIC |
| Skyglass Katana (live LEGENDARY) | **FIX** | "lattice"; capital "Crystal" | `A crystal-edged sword borne by the Captain's most faithful reconstruction. Its command seals resist interference, turning a measure of the wielder's damage into a brief protective shield.` |
| (Skyglass Crystal) | **FIX** | "lattice" twice | `A shard of skyglass worked to carry the ship's protective seals into another weapon. When its seals wake, part of the wielder's damage returns as a brief shield.` |

Carrier: a new edit (proposed 339 phase 1, text in a new `SKYGLASS_TEXT.md` §4.6). Retiering the three Coffer contents
is a rarity decision for the director (RUL-058's table states it; no manifest applies it).
