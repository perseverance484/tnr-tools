# Ryo generation (dauntless)

Director (2026-11-09 23:26): "Let's look into developing some ryo generation habits. We can use our hunting profession
to produce materials to sell on the Auction House. Can also purchase items there. We could add profession work to the
circuit." (23:27) "Also can spend all our exp on willpower/intelligence."

## Unspent experience
- `profile.useUnusedExperiencePoints {offence..Lightning}` assigns `earnedExperience` to stats. Put it into
  intelligence until it matches willpower, then split. 2026-11-10 05:27: 7,054 -> intelligence.

## Daily caps (director 2026-11-10): 20 missions, 50 errands, 9 medical. Counters: profile.getUser dailyMissions/dailyErrands/dailyMedicalMissions (count on start).

## Errands (fixed 2026-11-10)
Director: "Lets figure out why errands arent finishing that seems like a problem."
**Cause:** the errand's quest content lists a sector (e.g. 271) but the per-user tracker re-targets every
move_to_location goal to the sector the errand was started in (home, 177). Read the real targets from
`profile.getUser` -> `userData.questData[<questId>].goals[*].{sector, longitude, latitude}`, not from `quests.getAll`.
**Flow (all inside the home sector, no travel):** `quests.startRandom {type:"errand", rank:"D", userLevel:100,
userSector:177, userVillageId}` (A/S ranks: "Setting not found") -> for each goal in order: `travel.moveInSector
{cur..., longitude, latitude, destLongitude, destLatitude, sector:177, ...}` (moves straight there) ->
`quests.checkLocationQuest` ("You arrived at destination") -> after the last goal `quests.checkRewards {questId}`.
"Hyorin's Broken Gate": (5,5) then (10,7). **Pays 23,200 ryo + 2 tokens, ~7 calls, chainable back to back.**

## Hunting profession (occupation HUNTER, huntingExperience 3.75M)
Flow (routers/hunting.ts): `hunting.getBoard` -> `hunting.accept {habitatId, contractId, version:null}` -> travel to
the contract sector -> `hunting.getSession` -> `hunting.sessionAction {id, version, action:"prepare"}` -> wait 10 s ->
`hunting.start {id}` (AI battle, PvE loadouts) -> repeat prepare/start up to the allowance (10 hunts per contract) ->
`sessionAction finish` (releases the session; allowance kept). Each win drops 10 materials; 1-hour cooldown per contract.

| Rank | Contracts (sector) |
|---|---|
| S (Very Hard) | Dojigiri (330), Somen Shoko (340), Kinmokuzai (336), Byakuho (337), Akaibako (340), Unkei no Kami (336) |
| A (Hard) | Kajioka (336), Uramaru (336), Shigekai (336) |
| B (Medium) | Tsukihana (334), Enrai No Oni (334), Kugatsunagi (334) |
| C / D | many, sectors 331-342 |

- **Check gear durability before PvE/PvP** (`item.getUserItems` durability). On 2026-11-10 six equipped pieces
  (Kitsune Mask/Armor/Pants/Belt/Tabi, Meteor Hammer) were at 0: both Dojigiri losses happened on broken gear.
  Ryo repair needs the Crafting occupation; use `item.useRepairAll` (Repair Kits; 9 used for 13 items). Buy kits.
- **Kajioka (A) is farmable:** 3 rounds every time with repaired gear: R1 Chakra Invigoration (move in) + Stunning Jab
  (~2,680), R2 Ember Blade + Chakra Overflow, R3 Forbidden Chakra Fury (~9,500) = win. ~90 s per hunt, 10 Seika Seal
  Petals each. 5 of 10 hunts done 2026-11-10 (contract still has 5).
- PvE loadout gained Severed Pulse (heal-cut 50%, +30% taken on [None] damage only, 40 AP) on director advice
  ("you need a healcut like black thorn rose, seimyaku or severed pulse").
- 2026-11-10: **lost to Dojigiri (S)** in round 10: 15,150 HP, heals ~1,500/round, damage reduction, HP/chakra drain,
  reflect. Got him to ~3,000. S-rank needs a stronger sustain plan or kit before retrying.

## Hunting run log (2026-11-10)
Director (23:48): "Do all the hunting contracts. Just add hunting contracts as a valid activity."
| Contract (rank, sector) | Result | Material |
|---|---|---|
| Kajioka (A, 336) | 10/10 | 100 Seika Seal Petal |
| Uramaru (A, 336) | 10/10 | 100 Urami Drop |
| Shigekai (A, 336) | 10/10 | 100 Ofuda Moss |
| Tsukihana (B, 334) | 10/10 | 100 Moonpetal Weave |
| Enrai No Oni (B, 334) | 10/10 | 100 Yamidangan |
| Kugatsunagi (B, 334) | 10/10 | 100 Tsukinari Bell |
| Thornelure / Spintret / Luzzel (C, 337) | 10/10 each | Lurethorne / Glimmerchitin / Glimmer Dust |
| Rust Ferret / OwlCat / MossWolf (D, 337) | 10/10 each | Pelt / Owlcat's Fur / Mosswolf Tuft |
| Moonprowler / Badgertle (D, 331) | 10/10 each | Moonlight Antlers / Badger Shell |
| Cryverin / Brassel / Blazdrift (C, 342) | 10/10 each | Frostscale / Brasel Spine / Ashrend Wing |
| Byakuho (S, 337) | lost 0/1 | 60% absorb, 10%/turn self-heal, stacking 3-round wound; S-ranks need a new kit |
Scripts by target HP (all with PvE loadouts):
- 2,940 HP (OwlCat, MossWolf, Moonprowler, Badgertle): Stunning Jab one-shots. Jab range is 4: if he is within 4,
  Jab alone (1 call); else Chakra Invigoration toward him first. 2-3 calls per hunt.
- 5,250 HP (Rust Ferret): Invigoration + Jab (~4,560) then one basic attack.
- 5,740 HP (C-ranks): Invigoration + Jab (~3,250) then Ember Blade (kills). 3 actions.
- 10,650 HP (A/B): full 4-round script below.
- Hex pick: cube coords (x=col, z=row-(col-(col&1))/2, y=-x-z); choose a hex <=5 from me and adjacent (or <=4) to him.
- Empty response from performAction = race with the AI's turn: re-read or retry with version+1 (not a stun).
- Ramen restores SP/CP only; use a Full Potion when HP falls under ~3,000.
Script that wins A/B every time (10,650 HP targets): R1 Chakra Invigoration to a hex next to him (<=5 from me) +
Stunning Jab -> R2 Ember Blade + Chakra Overflow -> R3 Forbidden Chakra Fury + basic attack (+ a stance to end the
turn) -> R4 Ethereal Rebirth. If he stuns me R1 (80 AP), R2 = Overflow + basic + stance, R3 = Ember + basic, R4 Fury.
Speed: every `combat.performAction` response carries `battleUpdate {version, usersState}`: select
`battleUpdate.version` and positions from it instead of calling `getBattle`; the AI's turn runs automatically once
my AP is spent. After a win the session stays prepared: call `hunting.start` again directly. ~10 calls per hunt.
Upkeep in the field: `village.buyFood` works at the hunting sector's ramen stand; Full Potion between hunts
(restores HP and chakra). Buffed basic attacks with the repaired Meteor Hammer hit ~1,000-3,000.

## Listing rule (director 2026-11-09 23:44)
"Most items have a sell price recommendation in their description. You can gauge a stack based on that price and list
it for full price." If the description has no price, use the item's `cost` field. Buyout must be above the starting
price (start = buyout - 1).
- 2026-11-10 05:45: listed 50 Seika Seal Petals (cost 60,000) for 3,000,000 buyout, 72 h. 66 petals kept.
  Shard of Willful Steel cost is 110,000 (sells ~150-250k each), so cost is a floor, not a ceiling.

## Auction House prices (sold / asking, 2026-11-10)
- S-rank hunt materials (Thread Core, Mask Core, Parchment Core, Seed of False Vitality, Shard of Willful Steel,
  Cracked Auditory Core): sold ~1.5M-3.5M per stack of 10; asking 2.0-2.5M per 10.
- Kunai to buy later: Ikazuchi listed 20M/50 (buyout 25M); Elemental 35M/100.
- Many "2 ryo" sales are DIRECT gifts between friends: ignore them for pricing.
- 2026-11-10 07:23: listed at full cost, 72 h: 100 Lurethorne 5M, 100 Badger Shell 3.5M, 100 Rust Ferret Pelt 3.5M,
  100 Moonlight Antlers 3.5M, 100 Mosswolf Tuft 3.5M, 100 Brasel Spine 5M, 100 Owlcat's Fur 3.5M, 100 Frostscale 5M,
  100 Glimmerchitin 5M, 44 Yamidangan 2.64M, 80 Tsukinari Bell 4M (~44.1M total). `quantity` lists part of a big stack.
