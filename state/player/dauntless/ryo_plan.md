# Ryo generation (dauntless)

Director (2026-11-09 23:26): "Let's look into developing some ryo generation habits. We can use our hunting profession
to produce materials to sell on the Auction House. Can also purchase items there. We could add profession work to the
circuit." (23:27) "Also can spend all our exp on willpower/intelligence."

## Unspent experience
- `profile.useUnusedExperiencePoints {offence..Lightning}` assigns `earnedExperience` to stats. Put it into
  intelligence until it matches willpower, then split. 2026-11-10 05:27: 7,054 -> intelligence.

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
