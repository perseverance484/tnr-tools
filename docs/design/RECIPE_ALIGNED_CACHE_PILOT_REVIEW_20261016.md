# Recipe-Aligned Cache Pilot — Source-Mapped Shortlist and Value Scenarios

**Status: PROPOSAL, NOT APPROVED LOOT TABLES.** Approved *direction*: two new cache categories (Arsenal/Research), one chosen by the player after successfully completing Silent Bastion, native Weighted Cache outcome bundles. Director ruling `RUL-2026-10-16-001`. The graph selection `alt99_f4gate` was subsequently approved under `RUL-2026-10-16-002` on `chatgpt/silent-bastion-alt99-approval-20261016`. None of the eight specific output recipes, numeric scenarios, probabilities or rarity/economy values below is yet approved.

**Exact data source:** `docs/design/RECIPE_ALIGNED_CACHE_CANDIDATE_POOLS_20261016.json`, extracted deterministically from `claude/crafting-recipe-census-pln5za@eb625ca192fa440b76b204d48d13dbd89576ff7f:reports/crafting_recipe_census/craftable_recipes.json`. Original operator-run capture SHA-256 `81c76fef97e94c83d5c97bc7ce647edaea14a483577feac5b3928d5f0bc3d629`, finished 2026-10-13T03:27:14.940000Z; its source pin is `studie-tech/TheNinjaRPG@641040531176f91a3076fe5f32592ba18197a8c0`. The Oct-13 census is a **historical snapshot**, not current live validation. Checked source feature at `studie-tech/TheNinjaRPG@0651b039a466516a8fe24fc13b56f60dea11b7eb`. Main baseline for this design `99e86dc549b86f1f4a5846c0e509fa6bc15b3463`. No game/API requests or writes.

## Evidence and key finding: no eligible general armor recipe yet

The census contains 141 craftable item records, of which 86 were player-craftable at the source pin. Within the original visible/player-craftable recipe snapshot there are 25 weapons, 14 armor and 17 crystals (before additional safe-source curation). **None of those 14 armors is safe for an open recipe-material bundle using the first-pass rules**: 11 Kaeruun armors require the crafted/event `Unobtanium` and a special `Heart of Kaeruun` source; `Monarch's Crown` is flagged `isEventItem:true`; `The Skyglass Crown` is Ghost Ship exclusive; `Sash of the Crimson Court` has special materials with no verified ordinary direct hunt/gather origin. We cannot claim an armor pool merely because the equipment category was approved.

**Therefore the initial Arsenal shortlist below is weapons-only as an openly labelled proposal.** The *category* remains equipment-capable: future armor inclusion needs a separate eligibility/rank-gating or recipe-source decision, not an accidental material leak. This is a real design constraint for director acceptance, not a reason to violate event exclusivity.

The provisional filter excludes hidden/event output, hidden/event input, nested crafted ingredients, unknown-source inputs, blocked targets and non-integer recipe fractions. These filters are deliberately more conservative than the engine's bare `canBeCrafted` validation. The `Skyglass Crystal` and `Skyglass Crown` are excluded for their approved exclusive economy; the Oct-13 Crystal recipe also disagrees with the later 12-Filament director record and must **not** override it.

## Proposed shortlist: Bastion Arsenal Cache

| Output recipe | Output tier / rank | Full recipe (units) | 20% control | Strong-Pyramid scenario | Distinct reagents |
|---|---|---:|---:|---:|---:|
| Eclipsed Dawnblade | EPIC / MASTER | 50 | 10 | 50 | 4 |
| Gaea's Embrace | EPIC / MASTER | 50 | 10 | 50 | 4 |
| Aetherion | LEGENDARY / FORGEMASTER | 50 | 10 | 20 | 5 |
| Stormrender | LEGENDARY / FORGEMASTER | 50 | 10 | 20 | 5 |

- Two ordinary EPIC equipment recipes and two LEGENDARY weapons; all have directly sourced tradable hunting/gathering ingredients in the census. This mix is a **candidate**, not a locked output roster.
- Alternate eligible weapons (not yet in pilot) are Sunfire Edge, Thunderstrike Fang, Yasei's Bolt, Zephyr's Whisper and Thornsilver; their full source IDs, reagent splits and eligibility flags are in the machine candidate file.
- Excluded from this safe-supply test: Night's Testament, Oathbinder, The Unwritten and Whispering Dawnblade because they need event/crafted Unobtanium. This is not a recommendation to remove or alter those recipes.

## Proposed shortlist: Bastion Research Cache

| Output recipe | Output tier / rank | Full recipe (units) | 20% control | Strong-Pyramid scenario | Distinct reagents |
|---|---|---:|---:|---:|---:|
| Absorb Gem II | EPIC / MASTER | 20 | 4 | 20 | 2 |
| Damage Crystal II | EPIC / MASTER | 40 | 8 | 40 | 3 |
| Fortify Crystal II | EPIC / MASTER | 40 | 8 | 40 | 3 |
| Heal Crystal III | LEGENDARY / FORGEMASTER | 40 | 8 | 16 | 2 |

- Three distinct EPIC crystal recipes and one LEGENDARY Heal Crystal III recipe. All ingredients come from the captured direct hunting/gathering material sources.
- Reserves: Afterburn Crystal, Drain Crystal and Lotus Seal Crystal. Fortify Crystal III is **not** simply a fraction of raw materials: it requires one crafted Fortify Crystal II as an intermediate, making a 20% or 40% recipe packet misleading unless the nested-recipe policy is explicitly redesigned.
- The protected Skyglass Crystal is excluded; it should remain on the established Ghost Ship-exclusive acquisition path.

## Craft demand is a second gate, not just recipe correctness

The source census establishes **that a recipe can be crafted**, not whether its output is still desirable to today's endgame players. Two proposed EPIC Arsenal weapons (Eclipsed Dawnblade and Gaea's Embrace) and EPIC Research crystals might already have low demand among Silent Bastion's intended audience. If so, even exact full-recipe bundles would perpetuate the user's **unwanted inventory** problem. Before selecting outcomes, validate current item effects, progression relevance, trading value and genuine player demand against fresh non-live evidence and director judgment. The safe shortlist is a **mechanically sourced candidate pool**, not a claim of endgame utility. Favor fewer, distinctly useful options over trying to represent every craftable recipe.

## Two quantity scenarios for director comparison (not approval)

| Model | EPIC outcomes | LEGENDARY outcomes | Arsenal average units/open* | Research average units/open* | Consequence |
|---|---|---|---:|---:|---|
| **Controlled20** | 20% of source recipe, exact ratios | 20% of source recipe, exact ratios | 10.00 | 6.87 | Lowest material injection; may feel negligible after a 16–20-battle Pyramid. |
| **Strong Pyramid** | Ingredients for one whole EPIC recipe | 40% of a LEGENDARY recipe, exact ratios | 42.50 | 30.73 | Meaningful one-craft or high-end progress, but requires supply and market checks. |

*These expected unit counts use a **single outcome roll** per opening, not several independent material rolls, with entirely **illustrative** tier odds: Arsenal 75% EPIC /25% LEGENDARY; Research 85% EPIC /15% LEGENDARY. Within a tier, each listed recipe entry is *uniformly* selected (current native Weighted Cache behavior). The numbers do **not** value all material units equally or imply equal pricing, crafting utility or earning rate. Selected recipe and scenario amounts are never engine-tested payloads.

### The targeting problem still matters

The player selects **Arsenal or Research**, not a specific weapon or crystal. Under the illustrative one-roll weights:
- Arsenal: either EPIC recipe is 37.5% per opening and either LEGENDARY is 12.5%. Expected openings to see a particular Legendary packet once is 8; to collect three 40%-packets for one specific Legendary craft averages **24 openings**, assuming unchanged independent odds, no trades and no ingredient-sharing offsets.
- Research: each of the three EPIC recipes is 28.33%; Heal Crystal III is 15%. Three 40%-packets for Heal III average **20 openings**, similarly ignoring trades and shared materials.

**Interpretation:** native coherent bundles eliminate random independent-ingredient sprays, but randomness among unwanted target recipes can still build surplus. Keep the launch outcome list short (four per category here) and compare actual in-game usefulness by player archetype. Do not declare the clutter problem solved just because the tables are recipe-correct. We could later reconsider recipe-level targeting if real use shows persistent waste, but that is beyond the director-approved two-category launch.

## Production boundaries and remaining gates

The native source contract is `noncombatconsumereward` with `rewardMode:"weightedCache"`: `rolls` and `tiers` must each total **10,000 basis points**, and every selected `tier.entries[].items[]` contains all item ID/quantity pairs for exactly one recipe packet. An item card in quest-level `content.reward.reward_items` plus `content.rewardMode:"choose"`, `content.rewardPickCount:1` implements the requested category-selection *design*. Adding the cache IDs directly to the Pyramid `win_quest` objective would pay both unconditionally and is prohibited. Fable must prove the quest choice save/claim and cache consume paths offline with the actual pinned build engine; the previous condensed graph's PASS did not cover reward-choice behavior.

**Director decisions still required before a real manifest:** accept or alter the shortlist; decide if Arsenal being weapons-only for pilot is acceptable; select complete versus partial progression model and exact counts; approve the tier and recipe-entry distribution, cache rarity/trade/stacking and any profession-exclusivity exceptions; settle Beacon economy and current entry-at-start wording; approve art and release. These items should remain placeholders, not be guessed by a generator.

**Unresolved Bastion prerequisite:** Fable's original 99-node graph failed native reset behavior; the director now approved `alt99_f4gate` with Fable proof at `74eeb328f05d4258056b0a1c531619ffcf852ce3`. The new implementation must reconcile current upstream, the Beacon charging timing B1 and Arakane Combat Protocol stand-in; content may be drafted without silently treating these as settled. No live requests or writes.

**Recommended next bounded activity:** Fable performs an isolated **offline** `battlepyramid` reward-choice fixture and Weighted Cache bundle/receipt compatibility proof (without creating a live-clickable push manifest); ChatGPT and the director compare these candidate recipe profiles and choose the economic model before content freeze.


## Read-only source-data consistency check (2026-10-16)

Following document creation, each of the **8 proposed pilot** and **8 reserve** entries was compared again to the exact source census by item ID, name, type, rarity and ingredient ID/quantity. All 16 matched, and no two entries duplicate an identical full ingredient set. The two quantity scenarios preserve exact integer recipe ratios for every ingredient. Both illustrative tier distributions and both one-roll distributions sum to 10,000 basis points. The source's 14 visible player-craftable armor records were filtered independently; **0/14** passed the non-event, directly sourced, non-nested test. The frozen `alt99_f4gate` graph has 99 nodes, with all four recovery-win dialog bridges and four folded fourth-fight introductions present. Current upstream `main` still resolved to `0651b039a466516a8fe24fc13b56f60dea11b7eb` during this check.

**Scope of this check:** repository connector comparisons and arithmetic only. It did **not** execute `validate.py`, the game engine, a database, live browser, Forge, weighted-cache item update or item consume. These findings are **source-data QA**, not release validation, independent Fable review or proof of desirable balance. A future native builder/engine proof and user reward approval remain gates.
