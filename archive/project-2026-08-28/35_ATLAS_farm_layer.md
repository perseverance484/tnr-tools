> **STALE - archived 2026-08-28 (rollout Stage 1).** shipped Ashen campaign; archive only.
> Do not build from this file.

# 38b_ATLAS_hubs.md: the farm layer, as wired [2026-07-27, verified against the master]

## The reveal schedule (story progress opens everything)
Ash Road (once) -> the hub -> **Muster** opens: The Outer Districts, the Long Patrol, the four one-time explorations (Wards, Rounds, Roost Climb, Cinder Rows) and the profession grinds. Each **clan chapter** opens its Furnace kiln and the next chapter (Ryokin also opens the First Fitting; each kiln cleared opens its Crucible). **The Compact** opens: The Clan Grounds, the Reckoning, the Quartermaster's Requisition (rare gloves). **The Veiled Table** opens: The Deep Works, the Table's Requisition (epic stance greaves), and the weekly Settlement; the Settlement opens the weekly Glassfire.

## The three story hubs (daily, one run each)
**The Outer Districts** (Muster). Three Ember fights (Unchartered Straggler pair, Waste Reaver pair, Warden of the Long Road), then the Quartermaster's slot pick. Pays: Kiln Salvage EV 2.25, an Ashen base of your chosen slot at 75%, Nemori and Shirakotsu component rolls. Rare: Founder's Stride at 1.2%.
**The Clan Grounds** (the Compact). Five clan tests in one round: the Rite Keeper, the Ledger Shinobi, the Silk Watcher, the Quench-Master, the Glasshouse Watcher. Pays: two rolls of every clan's components at 40% per leg.
**The Deep Works** (the Veiled Table). The Vigil watches (furnace pair, then a crucible boss), then the Undervaults gamble: the safe row (steady Ryokin and Ash) or the deep row (Ryokin at 50%, Kilnheart at 30%, the Debtkeeper's Greaves at 1.2%).

## The rest of the farm layer
Ten kilns (Furnace per chapter, Crucible behind each) and two patrols pay components and Ash, currencies zero: materials are the pay. **The profession lane is exclusive.** Kilnhide and Cinderbloom come only from rank-gated records: nobody outside the job farms them, and everyone else trades for them. Each profession gets two ways to work: the **standing mission** (Ashen Hunt, Ashen Gather: unlimited, run it as often as you like, 2 materials plus profession experience per run) and the **daily adventure** (the Long Climb, the Deep Rows: once a day, the richer run, 4 materials plus Concord Ash, profession experience, and on the hunter's side the Ashrend Talons at 1.2%). Both materials are tradeable and both feed core crafts (Cinderbloom in every Kilnwrought piece and the Mantle; Kilnhide in the Cleaver, the Talons, and the First Brick), so professionals are the camp's suppliers and the market is the fighter's route in. All rates [P]. The two weeklies pay the Kilnheart bulk (9/week between them) and carry the endgame chases: the Mantle and the Glasskissed at 12% each on the Glassfire.

## The chase map (every chase drops AND crafts)
The First Brick: the Pit Crucible daily 1.2%, pity forge. The Mantle and Glasskissed Gauntlets: the Glassfire weekly 12%, pity forges (the Glasskissed pity is the Kilnheart sink). Talons: the hunter's daily Long Climb at 1.2%, or crafted from 6 Kilnhide (tradeable, so non-hunters buy in). Stride: the Stair exploration and the Outer Districts daily. Debtkeeper's Greaves: the Undervaults exploration and the Deep Works' deep row daily.

## Why this shape holds
Rates are throttled to the two-to-three-week pacing promise (30f). Every chase has a deterministic path. Nothing is carryable, showable, or losable: story progress is the only key. The one push-time class of risk that remains is reward semantics on non-win nodes (comps paid on fight nodes), already on the first-push verification list.

## Push-time verification added by this pass
The two daily adventures are questType hunting and gathering carrying defeat_opponents nodes; the primitive proven inside those types is win_encounter_at_location (the standing missions use it). Confirm on first push that defeat_opponents runs inside a hunting or gathering quest; if it does not, the fights convert to win_encounter_at_location with the same rosters.
