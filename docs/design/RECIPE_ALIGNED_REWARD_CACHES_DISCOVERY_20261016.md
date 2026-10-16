# Recipe-Aligned Reward Caches — Design Discovery, 2026-10-16

**Status:** DRAFT / USER DIRECTION, NOT FINAL REWARD APPROVAL. **Lead:** ChatGPT Content Designer; Engineering Auditor lens. **Normal implementation owner:** Fable / Claude Code. **Director owns:** drop chances, quantities, rarity, economy, categories, player-facing rewards, art, acceptance and all live-game actions. No manifest, item creation, live request or publication is authorized by this document.

**Baseline and exact references (reverify before implementation):**
- TNR Tools `main@99e86dc549b86f1f4a5846c0e509fa6bc15b3463`; current global `state/active-context.md` / `state/status.json` still project a historical September Forge session, not the current reward task.
- TNR source `studie-tech/TheNinjaRPG@0651b039a466516a8fe24fc13b56f60dea11b7eb` (2026-10-16 schema sentinel); source paths below.
- Crafting census `claude/crafting-recipe-census-pln5za@eb625ca192fa440b76b204d48d13dbd89576ff7f`: `reports/crafting_recipe_census/craftable_recipes.json` — COMPLETE as of operator capture 2026-10-13, source `641040531176f91a3076fe5f32592ba18197a8c0`; historical snapshot, not perpetual live truth.
- Silent Bastion design `chatgpt/silent-bastion-node-budget-20261015@2af1ffd808f692d241b80c1d2c87e6e6d967016b`, `state/silent_bastion_design.md`, `state/silent_bastion_condensed99_candidate.json`, and `state/silent_bastion_release_plan.md` (four interior divisions, 16–20 victorious-run fights, one terminal reward, no exterior garrison).
- Silent Bastion native proof `claude/silent-bastion-budget-validation-69za5u@74eeb328f05d4258056b0a1c531619ffcf852ce3`, `docs/reviews/SILENT_BASTION_CONDENSED99_NATIVE_RESULTS.md`: selected 99-node candidate FAIL (C1 recovery-on-loss); `alt99_f4gate`, `alt99_alertgate` and `alt95_bossgates` PASS the pinned native gates, all still unselected. Beacon entry-consumption timing B1 needs director reconciliation against current source. No reward implementation should assume the Bastion quest is ready to release.

## Objective and scope

The director requests a full **design overhaul** of reward boxes away from scattering unrelated hunting/gathering material types. The newer Medicine Inro, Shinobi Tool Pouch and Sage's Strongbox show the improved principle of ingredients chosen from meaningful recipes, but still use the old independent-line reward method. The newly implemented **native Weighted Cache item effect** enables a better result: **a single opening awards a coherent bundle for a specific craft goal**, rather than independently rolling dozens of unrelated reagents. Use Silent Bastion as a first limited pilot if approved. **Do not replace or edit existing Gatherer's/Hunter's chests, the newer three crafting caches, Ghost Ship quest rewards or locked Skyglass Reliquary/fragment/Katana/Crystal economy as part of this design pass.**

The director's concern is *player utility and inventory clutter*, not simply total payout. A high nominal material yield can be a bad prize if most of its material types have no purpose for the recipient. Evaluate **recipe progress / completed crafts / trade liquidity per cache** in addition to raw unit counts.

## Source-confirmed Weighted Cache contract (not the older standard chest format)

At the pinned upstream game source:
- `app/src/validators/combat.ts`, `NonCombatConsumeRewardTag`, accepts `rewardMode: "weightedCache"` plus a `weightedCache` object inside a consumable item's `noncombatconsumereward` effect; this is not a new quest-reward field.
- `app/src/validators/weightedCache.ts` requires `version:1`, `displayName`, a weighted `rolls` count distribution and weighted `tiers`. Each tier has `entries`; each entry's `items` are pairs of `itemId` and `quantity`. Each nonzero tier's entries are nonempty. Probabilities are integer basis points and must **sum to 10,000 independently for roll counts and tiers**.
- `app/src/libs/weightedCache.ts`, `resolveWeightedCache`: draw how many rolls to perform; **each roll** chooses a tier by its weight and **one uniformly chosen entry within that tier**, granting *all* items in that entry. Recipe identities do **not** receive independent per-entry weights within a tier. Same-recipe-entry duplicates would distort odds; curate deliberate weighting via tiers where justified, not accidental duplication.
- Limits: up to 20 roll-count rows, 20 tiers, 50 entries per tier, 10 distinct item entries per bundle, 100 of an item per bundle row, at most 2,000 items per opening worst-case. Active caches must prevent battle use; consumable items require `destroyOnUse:true`. Weighted caches cannot grant reputation, bloodlines or bloodline-linked items.
- `app/src/server/api/routers/item.ts`, `item.consume` performs existence/restriction checks before item debit and has a `requestId`-backed consumption/receipt path. The config's reward receipts disclose granted *item names/chances*, not a guaranteed player-facing label identifying which specific recipe the bundle was designed to fund.
- `app/src/validators/rewards.ts` separately defines quest-level `rewardMode:"choose"`. **Do not conflate** choosing a quest prize with the item's Weighted Cache rolls. Whether the Battle Pyramid completion UI and operator manifest can safely offer a player pick among cache item types requires offline tests at the actual current engine pin.

The reference `skills/building-tnr-content/references/item.md` primarily documents the **legacy independent `reward_items` line chest**. Its chassis/safety guidelines remain relevant, but its old loot mechanic must not be mistaken for the current native weighted-cache schema. Refresh generated contract/Forge support by source extraction and structural diff before authoring.

## Design proposal v0: outcome = one coherent recipe

A cache is categorized by a real crafting goal, not by gathering-profession tier alone. One selected entry contains **only the ingredients belonging to one verified, presently usable output recipe**. If the intended payout is a *complete* craft, include every required ingredient in the current ratio. If the intended payout is *partial progress*, preserve legible ratios as far as item granularity allows; openly record unavoidable residual amounts. Nested recipes (an output requiring an intermediate crafted item) need explicit recursive expansion policy; never silently substitute ingredients. Distinct output recipes that have identical ingredients can share a bundle: do not imply two materially different rewards.

Examples **from the frozen Oct-13 census** (not approved payout quantities):
- Chakra Pill II: Galecrest Sage ×2 and Glimmer Dust ×2.
- Stamina Pill II: Galecrest Sage ×2 and Mosswolf Tuft ×2.
- Katon Kunai: Ashrend Wing ×2, Iron Ore ×2, Sunroot ×2.
- Enemy Pill: Cracked Auditory Core ×10 and Heart of Kuraokami ×10.
- Forbidden Jutsu Scroll: Nexus / Rebirth have identical three-ingredient requirements (Fujin's Breath ×10, Parchment Core ×10, Voidshade Petal ×10); distinguish target flavor from ingredient outcome.

Unlike the old Medicine Inro example (five materials showered together, about 80 expected units) or the broad Shinobi Tool Pouch (about 75 expected units), a native cache can select **one named recipe's coherent ingredient set** at a time. Native entry-level selection is random even if the *category* is chosen. This is an important distinction for player control.

### Candidate portfolio (NOT selected)

1. **Bastion Arsenal Cache:** outcome sets for selectively approved endgame equipment recipes (weapons/armor); themed to Experimental Armory. Avoid filling a single chest with unrelated equipment families and avoid legendary-complete-recipe grants until their supply impact is explicitly balanced.
2. **Bastion Research Cache:** outcome sets for approved crystals/imbuement recipes; themed to Skyglass Research. Respect native crafting-rank requirements, hidden/event-only inputs and existing Skyglass-exclusive item authority.
3. **Bastion Field Stores** (deferred candidate): targeted useful combat consumable recipes, with the existing Medicine Inro / Tool Pouch / Strongbox serving as *design references*, not automatically cloned or replaced.

**Recommended first pilot:** design and compare only **Arsenal + Research**. A tiny number of distinct cache types reduces *box clutter* and lets the director see whether recipe-aligned opening actually feels rewarding.

## Silent Bastion acquisition proposal (requires director approval and proof)

Attach the new cache **item ID(s)** to the **single successful terminal completion** of Ghost Ship: The Last Directive (the Bastion `w.complete`), not to per-division battle rewards or retry loops. This preserves the reward-once architecture and prevents farming a mid-floor payout by intentionally losing. The Bastion's four-division quest topology should not gain objectives solely to dispense a cache.

**Preferred player-facing experience:** on final completion choose **one** thematic cache family (e.g. Arsenal or Research), then open it for a recipe-focused outcome. This is *conditional* on validating quest `rewardMode:"choose"` for the Battle Pyramid and on the director accepting that completion-pick UX. **Fallback:** award one prechosen Bastion cache that internally weights outcome families, with honest disclosure that players cannot direct its exact recipe. Neither option is approved. Existing Beacon acquisition and Ghost Ship Skyglass rewards stay intact.

**Source-blocking status:** Fable's 2026-10-15 native proof says the original 99-node recovery bridge fails if a subsequent recovery battle is lost; three content-only fixes passed. The director still owns selection. Beacon charged at quest start (at tested source) rather than first fight; also a user decision. This cache proposal adds no authority to bypass either Bastion gate.

## Curation, economy, and verification gates

1. Build a **recipe graph** from the stamped census: target output → requirements, including nested dependencies; filter hidden/blocked/non-player-craftable outputs, nonexistent inputs, event/quest-locked materials and any profession-exclusive materials prohibited in open chests by reward doctrine. A full **fresh operator-run capture**, only if the director requests it, must reconcile drift before a live manifest.
2. Keep a human-reviewable table per outcome: output recipe and id, source capture pin, item ids/quantities, crafting rank, source occupations, ingredient tradability, drop restrictions, spillover into other recipes, and whether quantities are complete-craft or partial-progress units. Do not use the old seed catalog as proof of current existence.
3. Simulate opening yields at proposed roll-count/tier weights; report distribution of **useful craft-equivalents**, duplicates, rare-material supply per Beacon/quest clear, profession income displacement, tradable value and possible waste by player segment (crafter vs noncrafter; equipped build versus alternate goal). The source's 10-item/100-quantity/2,000-total limits and 10,000-basis-point sums are hard gates, not tuning guidelines.
4. Avoid duplicate material supply silently undermining original hunting/gathering reward economies while legacy chests remain. Do not turn special profession-only or secret-route resources into generic trade-unlocked boxes without an explicit user ruling. Preserve Ghost Ship's exclusive Skyglass chase; the census's Skyglass Crystal line should be reconciled with current reward decisions before considering it an outcome.
5. Validate through current contract extraction, recipe checker, deterministic probability / value simulation, item factory and `validate.py` (0 errors), then Fable offline source-driven tests, read-only operator capture if actually required, director-approved hidden create and post-push read-back. Publishing is a separate user action. No agent game writes.

## Open director decisions (no default authorization)

- **Unit value:** one complete recipe per winning roll vs a targeted fraction/progress pack; separately tier by recipe rarity and market value. The more valuable the recipe, the more important the material-supply impact.
- **Pilot set:** Arsenal and Research only, or a broader initial portfolio; which particular player-usable craft outputs belong in each.
- **Agency:** final-quest **pick a cache category** (requires proof) vs receive a predetermined/random cache. A random recipe within a category may still yield an unwanted craft; decide acceptable degree of targeting.
- **Economy:** target expected value per Beacon/clear, rates/weights/roll counts, chest and ingredient tradability, rarity and stack behavior; quest caps and Beacon cost; handling non-crafters.
- **Presentation:** cache names and icons, descriptions that explain eligible recipe outcomes, how to communicate the specific recipe won when native UI exposes only item names/chances; whether to add receipt/UX tooling later.
- **Scope:** how/when to migrate or supersede legacy Hunter's/Gatherer's chests, if ever; **not** part of the first Silent Bastion pilot.

**Next bounded design task:** inventory candidate endgame recipe outputs from `reports/crafting_recipe_census/craftable_recipes.json` into two draft candidate pools (Arsenal and Research), deduplicating ingredient sets, attaching acquisition/tradability/rank flags; create draft full-kit and partial-kit yield scenarios for the director to compare. **No manifest yet.**
