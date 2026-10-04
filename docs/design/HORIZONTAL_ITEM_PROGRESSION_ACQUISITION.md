# Horizontal Item Progression — Acquisition and Development Proposal

**Status:** PROPOSAL / RESEARCH — NOT APPROVED FOR IMPLEMENTATION  
**Date:** 2026-10-04  
**Repository base:** `main@ca1980a1faa8c63ce020d9519962c1732ea201dd`  
**Lead:** ChatGPT — Content/System Designer  
**Supporting lenses:** economy, encounter design, engine feasibility  
**Live-game activity:** ZERO LIVE REQUESTS / ZERO LIVE WRITES  
**Implementation owner:** Fable / Claude Code after operator approval  
**Operator-owned:** final balance, drop rates, reward values, rarity decisions, publishing, live actions, final acceptance

## 1. Purpose

Design MMO-like horizontal equipment progression for TNR, beginning with acquisition.

The target experience is not an endless item-level ladder. A player should be able to keep equipment they care about, deliberately pursue alternatives, retune a build, and continue finding meaningful rewards after a functional loadout already exists.

This document separates:

- **Source-verified mechanics:** observed in the pinned TNR game source or generated contract.
- **Repository doctrine:** current TNR design/authority rules.
- **Assumptions:** useful hypotheses that require validation or operator choice.
- **Proposals:** recommended system design, not live-game fact.

## 2. Sources and authority

Repository authority follows `docs/00_INDEX.md`, `docs/DOCTRINE.md`, `docs/RULINGS.md`, and `docs/DEVELOPMENT_WORKFLOW.md`.

Reviewed repository sources include:

- `CLAUDE.md`
- `CHATGPT.md`
- `docs/00_INDEX.md`
- `docs/DOCTRINE.md`
- `docs/RULINGS.md`
- `state/active-context.md`
- `state/status.json`
- `docs/agents/README.md`
- `docs/agents/CONTENT_DESIGNER.md`
- `docs/workflows/CONTENT_WORKSTREAM.md`
- `skills/building-tnr-content/SKILL.md`
- `skills/building-tnr-content/references/item.md`
- `skills/building-tnr-content/references/balance.md`
- relevant quest / AI references
- generated contracts under `skills/building-tnr-content/data/`

Pinned source provenance used for engine claims:

- generated contract provenance: `studie-tech/TheNinjaRPG@bdec2883`
- source files inspected include:
  - `app/drizzle/schema.ts`
  - `app/src/validators/combat.ts`
  - `app/src/validators/objectives.ts`
  - `app/src/libs/quest.ts`
  - `app/src/libs/hunting.ts`
  - `app/src/libs/gathering.ts`
  - `app/src/libs/combat/actions.ts`
  - `app/src/libs/combat/util.ts`
  - `app/src/libs/combat/database.ts`
  - `app/src/server/api/routers/item.ts`
  - `app/src/server/api/routers/occupation.ts`
  - `app/src/server/api/routers/auction.ts`

The live upstream repository may have moved since this pin. This proposal uses the pinned source for TNR engine conclusions unless explicitly stated otherwise.

## 3. Executive recommendation

Adopt a **Targeted Arsenal Expedition** model.

The acquisition loop should combine:

1. **FFXIV-style dependable targeting:** a successful activity gives progress the player can direct toward a specific desired item, rather than requiring an indefinite random drop.
2. **Slay the Spire-style route decisions:** the player chooses safer or harder branches, ordinary or elite encounters, and optional extra risk for extra reward opportunities.
3. **PoE-style functional resources:** the long-term resource is useful because it changes an item, not merely because it is scarce.

For TNR, the launch shape should be small:

- authored repeatable expedition quest;
- two meaningful route forks;
- normal encounters, optional elite encounter, final guardian;
- target family selected at entry;
- exact permanent sidegrade selected at completion;
- direct AI drops supply random excitement and market value;
- one optional per-copy tradeoff imbuement slot for modular gear, never an additive “free power” socket;
- all endgame sidegrades remain within one active power budget and use the normal equipment-slot limits.

**Do not make a token treadmill the center of the content-only version.** The audited quest delivery path does not provide a safe generic “consume N identical stacked tokens and choose a reward” primitive, and CRAFTING recipes are occupation-gated.

A small engine extension should later expose a universal tuning service built on the existing per-`UserItem` imbuement tables and add a proper duplicate-salvage / deterministic exchange path.

## 4. What horizontal growth means

### 4.1 One item

A horizontally progressing item should have four properties.

**A. It is useful when acquired.**  
A new endgame item is not a low-rarity base that must climb a rarity ladder before becoming relevant.

**B. Its identity is bounded.**  
It has a clear job: pressure, defense, sustain, control, counterplay, mobility, resource efficiency, or another narrow purpose. It does not accumulate every role.

**C. Development changes allocation, not ceiling.**  
If the item is tunable, a modifier must move power from one function to another or add a benefit paired with a real cost. Adding a modifier cannot simply increase the total legal budget.

**D. It remains recognizable.**  
The player should be able to keep the same owned item and change how it is tuned where the engine permits. Cosmetic variants can deepen attachment without adding combat power.

### 4.2 A collection

A horizontally growing collection becomes stronger mainly through **option value**:

- more match-up answers;
- more playstyle alternatives;
- more slot-specific combinations;
- different offense / defense / support emphases;
- cosmetic variants and prestige goals;
- resources that let the player retune existing gear.

The collection may grow indefinitely, but the combat loadout does not. TNR’s equipment slots, `maxEquips`, keystone slot, and any approved imbuement cap remain the hard boundary on simultaneous benefits.

### 4.3 After a functional build exists

Progress remains rewarding because the player can pursue:

- a sidegrade for a different opponent or encounter;
- a safer or more aggressive version of a slot;
- a support/control option instead of personal damage;
- a technique crystal that retunes an owned modular item;
- tradable chase drops;
- cosmetics / item variants;
- completion or mastery goals that do not raise raw combat ceiling.

New content should add a new **question** or **answer**, not a higher item level.

## 5. Relationship to skill tree, keystones, and Bloodright

### Normal skill tree

Treat the skill tree as the persistent general foundation of a build. Equipment should be the swappable layer that changes encounter-specific emphasis.

A player who spends skill points on offense should not automatically receive the best offensive equipment outcome as another unconditional multiplier. Equipment should often ask that player whether they want to reinforce offense at a defensive/support cost or cover a weakness.

### Keystones

Keystones are the strongest existing TNR precedent for horizontal equipment identity: a keystone can gate a bloodline/jutsu style and change what a build is doing rather than merely add a higher-tier stat package.

### Bloodright

Bloodright is a **proposal**, not evidence of current engine support.

Carry over its design principle: benefits need clear scope, mutually exclusive choices, and a total cap so the player cannot eventually own and apply every bonus simultaneously.

If Bloodright ships, gear + skill tree + Bloodright need a combined balance review. In particular:

- avoid repeated global damage-given multipliers across all three systems;
- avoid raw-damage additions that move jutsu between damage tiers;
- prefer scoped or conditional gear effects;
- keep weapon riders light per doctrine;
- ensure equipment tuning spends a closed budget.

A cross-system automated “legal loadout budget” validator is not currently established by this audit.

## 6. Existing rarity and base-item doctrine

### Legendary default

Repository doctrine says new endgame gear defaults to Legendary because the active player population has outgrown lower tiers.

That doctrine **fits** horizontal progression if rarity stops functioning as the progression ladder. New alternatives can all be Legendary and still be sidegrades.

The recommendation therefore does not require a new rarity hierarchy.

### Existing common → rare → epic → legendary material conversion

The existing Ashen-style base-item/material pattern is useful infrastructure, but its literal tier ascent conflicts with the target model.

Do not make that chain the horizontal system’s core progression.

Possible reuse:

- stable recipes and material requirements;
- converting one item identity into another;
- same-rarity specialization recipes;
- crafter economy.

If reused, prefer Legendary → Legendary specialization or recipe-driven sidegrades rather than “same item, bigger rarity, bigger numbers.”

Because player crafting is CRAFTING-occupation-gated, recipe conversion should remain an optional profession/economy path rather than the only route to core equipment.

## 7. Source-verified mechanics audit

| Feature | Classification | Evidence / consequence |
|---|---|---|
| Authored dialog branches | **Supported now** | Dialog objectives record an explicit selected next objective. Suitable for target selection and route forks. |
| Normal → elite → boss authored route | **Supported now** | Consecutive quest graphs plus `start_battle`, `failObjectiveId`, and explicit branches support a fixed expedition flow. |
| Fully procedural randomized expedition map | **Requires engine work** | No generic Slay-the-Spire-like procedural route generator was verified. |
| Guaranteed quest item reward | **Supported now** | `reward_items` chance field can be 100%. |
| Random quest item reward | **Supported now** | Quest reward entries independently roll their configured percentage. |
| Objective-level rewards before quest completion | **Supported now** | Finished objectives with `status.done && !status.collected` pay once for the current tracker. |
| Safe high-value checkpoint reward across reset/replay | **Content-risk / requires discipline** | Resetting/restarting a repeatable quest creates a fresh opportunity to earn early objective rewards again. Do not front-load valuable guaranteed progression unless it is intentionally farmable. |
| Direct AI combat drops | **Supported now** | On victory, defeated non-summon AI item rows roll their own `dropChancePerc`; currently AI are the source of droppable combat items. |
| Player-selected permanent reward | **Possible through content configuration** | Branch a dialog to distinct reward objectives. A generic reusable “choose 1 of N” reward UI was not verified. |
| Hunting item acquisition | **Supported now, occupation-gated** | Hunter pools use `canBeHunted`, optional valid IDs, profession rank and rarity-based drop chance. |
| Gathering item acquisition | **Supported now, occupation-gated** | Gathering mirrors hunting with `canBeGathered` and profession-rank chance. |
| Player crafting | **Supported now, occupation-gated** | `craftItem` consumes configured material requirements; CRAFTING occupation and rank restrictions apply. |
| Per-copy item modifiers | **Supported now** | `UserItemImbuement.userItemId` attaches an imbuement to one owned item instance. |
| Add a crystal effect to an owned item | **Supported now, occupation-gated** | `imbueItem` consumes a CRYSTAL and attaches it to a specific `UserItem`; target type and imbue limits are validated. |
| Replace a crystal effect | **Supported now, occupation-gated** | Player can remove an imbuement and add another. On a still-imbueable item the removed crystal is not refunded, creating a real sink. |
| Multiple identical crystal copies on one item | **Not supported** | UserItem + imbuement item ID has a uniqueness constraint. |
| Mechanical named item variants | **Not supported by current variant system** | `ItemVariant` changes name/image/descriptions/cost; it has no combat effect payload. Treat as cosmetic. |
| Owned-item levels | **Supported now** | `UserItem` has `level` and `experience`; combat actions use owned item level for players. |
| Item effects scaling by owned-item level | **Supported now when authored** | Item combat action level is the `UserItem.level`; `powerPerLevel` can therefore produce vertical growth. Horizontal gear should normally author `powerPerLevel: 0`. |
| Item evolution | **Supported now** | Owned item can evolve to a child definition at max item level and resets level/XP. |
| Broad PvE path for item XP | **Not verified at pin** | Audited item XP award path is for equipped gear in eligible PvP. Do not make evolution the universal PvE development loop without extension. |
| Keystone slot / keystone-gated style | **Supported now** | KEYSTONE is native; bloodline/jutsu content can require a bloodline item/keystone. |
| Tradability | **Supported at item-definition level** | `Item.canBeTraded` gates auction/direct-sale listing. Finished imbued gear can be listed if the item is tradable and not currently being imbued. |
| Per-copy bind-on-pickup / bind-on-modify | **Unverified / likely engine work** | No per-`UserItem` binding field was found in the audited schema. |
| Generic duplicate salvage | **Requires engine work** | No universal player action converting arbitrary owned gear into a deterministic resource was verified. |
| Chest / cache reward | **Supported now** | Consumables with `noncombatconsumereward` can grant random/guaranteed reward bundles on consume. This is not a choose-one UI. |
| “Turn in N identical stackable tokens” quest exchange | **Not safe as a generic primitive at pin** | `deliver_item` verifies item IDs and removes the matching user-item row; it is not a verified quantity-decrement exchange. `delete_on_complete` exists in schema but was not found driving symmetric runtime behavior. |

## 8. Inspiration research

### 8.1 Final Fantasy XIV — transfer the acquisition structure, not the item-level ladder

Useful official examples:

- Duty Roulettes feed common tomestone currencies from many activity types.
- Savage raids award a guaranteed per-floor token (“Mythos” in the cited tier) that can be exchanged for chosen gear in addition to direct encounter rewards.
- Normal raid tiers use slot-specific exchange items from treasure/reward structures.
- Resistance weapon quests create long-term attachment to one weapon and intentionally allow required items to be obtained both inside and outside the main field zone.

Primary sources:

- FFXIV Patch 6.05: https://na.finalfantasyxiv.com/lodestone/topics/detail/a03d26b7aca93ae712a2f0f298076f0dc763f7ad
- FFXIV Patch 5.01: https://na.finalfantasyxiv.com/lodestone/topics/detail/4ddd33c83933ec4ad3dccb0e6538bbb9e85e63e7
- FFXIV Patch 5.35: https://na.finalfantasyxiv.com/lodestone/topics/detail/f1e5bfcb2a0bf477bcc8c81845c440f300e12f75
- FFXIV Patch 5.0: https://na.finalfantasyxiv.com/lodestone/topics/detail/330f2b280067d69d85b17831c66712a499e97484

Transferable principle:

> Random/direct rewards create excitement; deterministic progress protects the player from indefinite bad luck; multiple activities can feed the same goal.

Do **not** import:

- an item-level treadmill;
- seasonal invalidation of old gear;
- a large rotating currency catalog;
- mandatory weekly/daily obligation as the main retention tool.

TNR adaptation:

- route/boss drops are the exciting layer;
- successful expedition completion gives the player a targetable permanent choice;
- later engine work can add a compact deterministic exchange resource;
- hunting/gathering/crafting may provide alternate supply but not exclusive mandatory access.

### 8.2 Path of Exile 1 — currency with verbs

PoE 1 Essences are explicit crafting objects: they upgrade/reforge while guaranteeing a property. Eldritch currency adds/replaces implicits, rerolls a chosen modifier side, adds a prefix/suffix, removes a prefix/suffix, or trades one modifier tier against another.

Primary sources:

- PoE 2.4 Essence patch notes: https://www.pathofexile.com/forum/view-thread/1716228/filter-account-type/staff
- Rebalanced Essences: https://www.pathofexile.com/forum/view-thread/3080281/filter-account-type/staff
- PoE 3.17 Eldritch currency: https://www.pathofexile.com/forum/view-thread/3229187

Transferable principle:

> A resource remains desirable because consuming it performs a useful item operation.

TNR adaptation:

- keep the catalog tiny;
- a Technique Crystal should describe exactly what it does to the owned item;
- changing the item consumes the old/new resource, keeping demand alive;
- avoid making players inspect huge quantities of randomized trash.

### 8.3 Path of Exile 2 — targeted crafting, separately verified

PoE 2 must not be conflated with PoE 1.

In PoE 2 0.3.0, Essences were reworked into four tiers. Lower tiers add a specific guaranteed modifier while upgrading an item; Perfect/corrupted Essences remove a random modifier and add a new guaranteed modifier. Early Access 0.1.0c also increased the value of disenchanting fully modded rare items and reduced repeat campaign-boss currency after the first kill.

Primary sources:

- PoE 2 Content Update 0.3.0: https://www.pathofexile.com/forum/view-thread/3826682/filter-account-type/staff
- PoE 2 0.1.0c: https://de.pathofexile.com/forum/view-thread/3611708/filter-account-type/staff

Transferable principles:

- deterministic targeting can coexist with destructive replacement;
- unwanted drops can feed a crafting resource;
- repeat-boss farming can require explicit reward tuning.

TNR adaptation:

- replacement should consume the previous tuning crystal;
- a future salvage action can convert duplicates into one compact resource;
- direct boss drops should be an optional accelerator/chase, not the only path to a functional build.

### 8.4 Slay the Spire — route tension and reward choice

Mega Crit’s official description emphasizes a changing layout, risky versus safe paths, different enemies, cards, relics and bosses. Community-maintained mechanical references document the familiar node grammar: normal fights, elites, unknown/events, merchant, treasure, rest sites and bosses, with elites offering stronger rewards and rest sites presenting heal-versus-upgrade choices.

Sources:

- Official Steam page (Mega Crit): https://store.steampowered.com/app/646570/Slay_the_Spire/
- Mechanical map reference: https://slaythespire.wiki.gg/wiki/Treasure_Rooms

Transferable principle:

> The route itself is a build decision: more danger buys more reward opportunity, while safer routes preserve the chance to finish.

TNR adaptation:

- represent routes through short dialog choices and authored battle nodes;
- use normal vs elite fights and optional cache/shortcut decisions;
- keep the map understandable in a phone-sized quest flow;
- make the permanent reward depend on TNR acquisition goals, not on temporary run-only deck construction.

Do **not** import:

- resetting permanent equipment between runs;
- a huge procedural map requirement for the first version;
- temporary relic/card power as a substitute for MMO collection progression.

## 9. Three acquisition models

### Model A — Drop Hunt + mercy layer

**Loop:** repeat named enemies; rare direct equipment/crystal drops; deterministic fallback after enough clears.

**Strengths**
- immediate MMO loot excitement;
- direct AI drops already exist;
- easy to communicate.

**Weaknesses**
- repeated identical fights become the activity;
- duplicates and unlucky streaks dominate without a robust mercy/salvage system;
- a generic deterministic exchange layer is not currently cleanly supported by content alone.

**Verdict:** good supporting layer, poor core.

### Model B — Workshop-first progression

**Loop:** activities drop functional materials; player crafts the exact item or conversion desired.

**Strengths**
- highly targetable;
- resources stay useful when recipes consume them;
- naturally supports economy/professions.

**Weaknesses**
- current crafting and imbuing are CRAFTING-occupation-gated;
- turns the whole system into inventory/recipe administration;
- risks making non-crafters second-class participants;
- can become a currency catalog instead of gameplay.

**Verdict:** useful optional economy layer, not universal core.

### Model C — Targeted Arsenal Expedition (recommended)

**Loop:** choose what you are pursuing, choose a route, fight normal/elite encounters, beat a final guardian, then select an exact permanent sidegrade. Direct AI drops and functional crystals provide the random layer.

**Strengths**
- intentional target pursuit;
- route choice is gameplay rather than menu administration;
- success always advances the collection;
- direct drops still create excitement;
- casual safe route can reach the same functional ceiling;
- veteran harder route can improve efficiency/chase opportunities;
- achievable with authored quest content now.

**Weaknesses**
- content-authored branches are not procedurally fresh forever;
- exact reward-choice graph creates authoring overhead;
- current universal item tuning/salvage is incomplete.

**Verdict:** best fit.

## 10. Recommended acquisition loop

### 10.1 Entry

One short story/unlock quest introduces the system.

After unlock, the player may start the expedition without a mandatory daily cadence.

At entry, choose a **pursuit family** such as:

- **Pressure** — offensive / tempo sidegrades;
- **Guard** — defensive / sustain sidegrades;
- **Control** — support / utility / counter sidegrades.

These are taxonomy placeholders, not final item families.

The pursuit choice routes the completion reward list. It does not permanently lock the player out of the other families.

### 10.2 Route

Keep the first version to two route decisions.

Example:

1. **Outer Stores — normal encounter**
   - baseline difficulty;
   - small direct-drop opportunity.

2. **Fork A**
   - **Scout the sealed hall:** another normal encounter; lower risk.
   - **Breach the warded forge:** elite encounter; harder; better optional chase table.

3. **Fork B**
   - **Secure the cache:** take an extra encounter for another drop opportunity.
   - **Take the service tunnel:** skip the extra encounter and preserve completion odds.

4. **Final Guardian**
   - required boss/guardian battle.
   - boss has a compact direct-drop chase table.

5. **Recovery Vault**
   - successful player selects an exact item from the pursuit family, or—once their collection is functional—a useful tuning resource instead.

This translates Slay the Spire’s risk/reward grammar without pretending TNR has a procedural map.

### 10.3 What each layer gives

**Normal encounters**
- ordinary gameplay rewards;
- low chance at system-compatible material/crystal/chase item;
- no mandatory rare piece.

**Elite route**
- higher challenge;
- better chance at chase resource / tradable optional drop;
- not an exclusive higher-power gear tier.

**Final guardian**
- meaningful direct-drop excitement;
- no required build piece should exist only here at low RNG.

**Completion**
- dependable exact target choice;
- this is the protection against bad luck.

### 10.4 After the first item

The player returns because they can:

- collect another sidegrade in the same slot;
- target another family;
- take the elite route for better chase efficiency;
- earn a tuning crystal for an owned modular item;
- acquire a tradable chase item;
- pursue cosmetic variants/collection goals.

The system does not need to invent a stronger tier to make the next expedition relevant.

## 11. Random excitement versus dependable progress

The rule should be:

> RNG can accelerate or surprise; RNG does not gate the player’s first functional build or a specifically targeted core sidegrade.

Content-only implementation:

- completion reward: 100% branch-selected sidegrade;
- AI direct drop: low-probability optional item/crystal;
- unwanted random gear: tradable when appropriate;
- exact repeated item duplicates are mostly opt-in because completion choice is player-directed.

**Provisional pacing assumption for evaluation only:** one successful expedition can award one exact sidegrade. This deliberately makes expected and worst-case targeted acquisition equal after a successful clear. If that proves too fast, lengthen or gate the activity before lowering the item to a rare RNG drop.

For optional chase rewards, do not place critical power behind a low rate. A nominal 20% boss chase drop averages one per five clears, but still leaves a meaningful minority of players empty after many clears. That is acceptable for a cosmetic/market bonus, not a required build piece.

## 12. Functional currency and item development

### 12.1 What exists now

CRYSTAL is already the closest TNR analogue to PoE functional currency.

A crystal:

- is an item;
- can be restricted to target item types;
- is consumed when imbuing begins;
- creates a per-`UserItem` imbuement record;
- contributes its item effects to the owned item in combat;
- can be removed;
- normally is **not refunded** when removed from an item that remains imbue-enabled.

This is a real item-edit resource, not an admin edit.

### 12.2 Current limitation

Applying/removing imbuements is tied to the CRAFTING occupation.

Therefore:

- do not make an imbuement mandatory for a player’s first functional expedition item;
- do not assume every player can self-tune;
- allow crafters/market activity to be valuable, but not required for baseline parity.

### 12.3 Horizontal imbuement rule

For equipment in this system, recommend:

- `maxImbueNumber = 1` by default;
- the base item is complete without a crystal;
- an approved Technique Crystal is **budget-neutral**: upside + compensating downside;
- no crystal is a pure additive global damage/defense package;
- replacing a crystal consumes resources, sustaining demand.

Example structure:

- Aggressor Etching: shift a small amount from relevant defense to relevant offense.
- Sentinel Etching: shift the same budget from offense to defense.
- Flow Etching: gain a scoped utility benefit while accepting a separate explicit cost.

Exact tags, percentages, and legal combinations require balance validation and are operator-owned.

This uses the existing engine’s additive imbuement mechanism to produce a net sidegrade by encoding the tradeoff inside the crystal itself.

### 12.4 Why players spend instead of hoard

Functional resources are used when:

- their effect is explicit;
- acquisition is predictable enough that spending one does not feel irreversible;
- retuning solves an actual build/encounter problem;
- the previous crystal is consumed when the player changes direction.

A tiny catalog is preferable. Avoid PoE’s dozens of currencies and tier chains.

### 12.5 Recommended engine extension

Expose a universal **Tuning Service** that reuses the existing `UserItemImbuement` model but is not locked to the player having the CRAFTING occupation.

Possible implementations for Fable to evaluate later:

- NPC/service endpoint that applies an eligible Technique Crystal;
- item flag permitting public/self tuning independent of occupation;
- a specific system action for one tradeoff slot.

Crafting occupation can retain faster/cheaper/special recipe advantages if desired, but the horizontal system should not require profession switching.

Second extension:

- universal duplicate **salvage** action;
- converts eligible unwanted gear into one compact progression resource;
- account/non-inventory currency preferred if inventory clutter is a concern;
- use that resource for deterministic targeted crystal/item exchange.

Neither extension is treated as current support.

## 13. Item levels and evolution

This needs explicit protection against accidental verticality.

Pinned source now uses the owned `UserItem.level` when converting player items into combat actions. Any authored `powerPerLevel` therefore makes equipment vertically stronger as it levels.

The audited item-XP path credits equipped items in eligible PvP.

Recommendation for the acquisition system:

- author core horizontal gear with `powerPerLevel = 0`;
- avoid per-level cost reduction on these items unless deliberately approved;
- do not make max-level evolution a required PvE acquisition path.

A future “item mastery” layer could be useful **only** if:

- PvE/expedition play can advance it;
- evolution branches are same-budget sidegrades;
- evolution does not simply turn an item into a stronger tier.

That is a later workstream.

## 14. Duplicates, unwanted drops, and unsuccessful attempts

### Duplicates

Current-engine priority order:

1. reduce unwanted duplicates through targetable completion rewards;
2. keep optional random equipment tradable where economy goals permit;
3. keep random drop pools small;
4. avoid untradable random duplicates until salvage exists.

A per-copy binding rule was not verified. Tradability is definition-level.

### Unsuccessful attempt

High-value guaranteed progression should sit at completion.

Why: objective rewards are claimable when the objective completes, and a repeat/reset allows early sections to be run again. A large guaranteed reward on an early node is therefore farmable by repeatedly resetting.

On a failed run, the player may still retain legitimate direct drops already won from AI encounters. Those drops should be tuned as farmable content.

If guaranteed partial failure progress becomes important, implement a run-level claim ledger/account currency rather than front-loading a quest objective reward.

### Farming exploits

Watch for:

- reset after early reward node;
- fastest-route spam if optional harder branches have no compensating reward;
- farming a weak early AI with an overly valuable direct drop;
- using tradable deterministic crystals to arbitrage a scarce market;
- duplicate-item accumulation if salvage is absent;
- multi-system stacking of global damage/defense modifiers.

## 15. Economy structure

Keep the economy legible.

Recommended first system has at most:

- equipment sidegrades;
- one family of Technique Crystals;
- normal existing currencies/materials where already useful.

Do not create separate tokens for every encounter, slot, difficulty and season.

### Supply

- expedition normal/boss drops;
- guaranteed completion choice;
- optional hunting/gathering supply for selected resources;
- optional crafting recipes.

### Sinks

- crystal consumed on imbuement;
- crystal not refunded on ordinary removal;
- optional crafting recipes consume materials;
- future salvage/exchange can add a closed recycle loop.

### Trading

Tradeability is a design decision with major consequences.

Current engine supports definition-level `canBeTraded`, not audited per-copy bind behavior.

If gear/crystals are tradable:

- duplicates retain market value;
- profession specialization is healthier;
- deterministic crafting/tuning can amplify economic power and needs rate control.

If untradable:

- acquisition is easier to balance per player;
- duplicate dead-ends become worse until salvage exists.

Recommendation for the current-engine phase: prefer tradability for random chase drops; decide core reward tradability only after economy review.

## 16. Worked activity — The Broken Arsenal

**Narrative wrapper is provisional. Mechanics come first.**

### Premise

A sealed wartime testing complex contains equipment prototypes built by rival shinobi schools. The prototypes were not a linear series of “better” weapons; each school solved a different battlefield problem. The archive’s seals force an entrant to commit to a recovery wing before reaching the central vault.

This naturally explains sidegrades.

### Player flow

**Entry — Archivist’s Briefing**

Player reads a short explanation:

- “Choose what you are recovering today.”
- Pressure / Guard / Control.

This only targets the current run’s reward family.

**Node 1 — Outer Stores**

Normal AI encounter.

Player learns the enemy pattern and gets an ordinary drop chance.

**Choice 1 — Hall or Forge**

- **Sealed Hall:** normal encounter. Lower risk.
- **Warded Forge:** elite encounter. Higher chase-resource/drop chance.

The elite does not gate a higher item tier.

**Choice 2 — Cache or Tunnel**

- **Secure the cache:** extra fight, extra drop opportunity.
- **Service tunnel:** skip it and move toward the boss.

This gives a meaningful risk-versus-completion decision even without a procedural map.

**Final — Archive Warden**

Required boss encounter.

On loss/flee:
- route ends/fails;
- already-earned legitimate AI drops remain;
- no guaranteed completion item.

On win:
- move to the Recovery Vault.

**Recovery Vault**

Player selects one exact permanent sidegrade from the chosen family.

A player who already has the wanted gear may instead select an approved tuning resource or choose another item.

**Return**

Start again immediately or later. Choose another family or a harder route. Permanent equipment never resets between runs.

### Current-engine implementation shape

- authored consecutive quest graph;
- explicit dialog branches;
- normal/elite `start_battle` nodes;
- `failObjectiveId` to failure/exit path;
- AI item rows for chase drops;
- final branch-specific `reward_items` at 100%.

No live-game execution is authorized by this design note.

## 17. Worked item — Hushguard Bracer

**Illustrative only. Name/effects/numbers are provisional.**

### Acquisition

Player completes a Guard-targeted Broken Arsenal run and chooses **Hushguard Bracer** as the guaranteed final reward.

Proposed structural properties:

- endgame rarity follows Legendary-default doctrine;
- HAND equipment;
- static, complete baseline role;
- combat effects use `powerPerLevel: 0`;
- `maxImbueNumber: 1`;
- no large raw-damage rider;
- any crystal must be an approved tradeoff modifier.

### Customization decision 1 — Aggressor Etching

The player wants to turn the balanced bracer into a pressure tool.

**Provisional test concept, not approved balance:**

- gain a small scoped offensive-stat increase;
- lose an equal/appropriate amount of the corresponding defensive stat.

What changes:

- faster offensive pressure;
- less resilience;
- the item becomes attractive to a build that already has defensive coverage elsewhere.

What it does **not** do:

- add a free global damage multiplier on top of the original item;
- unlock a second simultaneous tuning benefit.

### Customization decision 2 — switch to Sentinel Etching

Later, the player prepares for a dangerous boss or a defensive/support setup.

They remove Aggressor Etching. On an ordinary imbue-enabled item, the removed crystal is not refunded. They consume a Sentinel Etching to apply the new tune.

**Provisional test concept:**

- gain a small scoped defensive-stat increase;
- lose a matching/appropriate offensive amount.

What changes:

- the same owned bracer now fills a different role;
- the player paid a real resource to change direction;
- the active ceiling did not increase because only one tradeoff slot exists.

Why another build chooses differently:

- glass-cannon/tempo build: Aggressor;
- defensive/support build: Sentinel;
- balanced build: leave the bracer untuned.

This is the desired PoE-like “currency performs an item operation” behavior without importing randomized six-affix loot.

### Access caveat

Under the pinned engine, the player performing the imbuement must use the CRAFTING occupation. Therefore the item can exist now, but universal self-tuning requires the Tuning Service extension described above.

## 18. Casual, veteran, offense, defense and support treatment

### Casual player

- safe route;
- same guaranteed functional ceiling;
- no obligation to fight the elite;
- no daily streak pressure.

### Veteran

- harder route improves efficiency/chase opportunities;
- can optimize crystal tuning and market participation;
- does not receive an exclusive numerically stronger gear tier simply for choosing the elite path.

### Offense build

Receives sidegrades that trade safety/utility for pressure rather than stacking free global damage.

### Defense/support build

Receives equally intentional items: mitigation, sustain, control, team utility, resource efficiency, counterplay.

### Existing functional build

Still has reasons to play because a new item can solve a different encounter or enable another loadout, while the old item remains valid.

## 19. Why this is preferable to a vertical ladder

A vertical ladder asks:

> “Is this number higher?”

The proposed system asks:

> “Which problem do I want this slot to solve?”

That is the core retention mechanism:

- attachment survives new content;
- collection breadth matters;
- player knowledge matters;
- trading and crafting remain useful;
- old gear is not automatically invalidated.

## 20. Recommended rollout

### Phase 0 — design validation

- define power budget by slot;
- define 2–4 sidegrade identities for one test slot;
- define a tiny crystal vocabulary;
- test stacking against skill tree and proposed Bloodright;
- decide tradeability.

### Phase 1 — content-only pilot

- one Broken Arsenal-style expedition;
- one or two equipment slots;
- fixed Legendary sidegrades;
- static `powerPerLevel: 0`;
- targeted completion rewards;
- small direct-drop chase table;
- optional tradeoff crystal only if occupation/economy friction is acceptable.

### Phase 2 — engine-quality extension

- universal Tuning Service using existing per-item imbuement storage;
- duplicate salvage;
- compact deterministic exchange resource;
- anti-repeat-claim/run ledger as needed.

### Phase 3 — breadth

- more encounter families;
- more sidegrades;
- hunting/gathering/crafting alternative supply;
- cosmetics/variants;
- optional same-budget item mastery/evolution only after PvE advancement exists.

## 21. Open operator decisions

Only the decisions that materially change the direction are listed here.

1. **Core tuning access:**  
   Should the first release keep tuning as an optional crafter/economy service, or should Fable implement a universal Tuning Service before the system is considered complete?  
   **Recommendation:** universal service before broad rollout; content-only pilot can precede it.

2. **Tradability:**  
   Should expedition gear and Technique Crystals be tradable?  
   **Recommendation:** random chase drops tradable; core guaranteed gear requires economy review. Current engine has definition-level tradability, not audited per-copy binding.

3. **Hard-route philosophy:**  
   Should elite routes improve efficiency/chase opportunity only, or contain exclusive mechanical sidegrades?  
   **Recommendation:** efficiency/chase/cosmetic distinction, not a higher power tier.

4. **Item mastery:**  
   Should existing item levels/evolution become part of this system?  
   **Recommendation:** not in the acquisition pilot. Revisit only with PvE item-XP support and same-budget evolution rules.

Exact balance numbers, rarity exceptions, rates, encounter counts and final reward values remain operator-owned.

## 22. Immediate next design step after approval

Take one real TNR equipment slot and build a **horizontal option matrix**:

- current live reference items;
- one baseline budget;
- three proposed sidegrade identities;
- one-tradeoff-slot crystal set;
- skill-tree / Bloodright stacking audit;
- acquisition mapping into the Broken Arsenal pilot.

Do not implement or publish until the operator approves the direction.
