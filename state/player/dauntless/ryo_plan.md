# Ryo generation (dauntless)

Director (2026-11-09 23:26): "Let's look into developing some ryo generation habits. We can use our hunting profession
to produce materials to sell on the Auction House. Can also purchase items there. We could add profession work to the
circuit." (23:27) "Also can spend all our exp on willpower/intelligence."

## Unspent experience
- `profile.useUnusedExperiencePoints {offence..Lightning}` assigns `earnedExperience` to stats. Put it into
  intelligence until it matches willpower, then split. 2026-11-10 05:27: 7,054 -> intelligence.

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

- 2026-11-10: **lost to Dojigiri (S)** in round 10: 15,150 HP, heals ~1,500/round, damage reduction, HP/chakra drain,
  reflect. Got him to ~3,000. S-rank needs a stronger sustain plan or kit before retrying.

## Auction House prices (sold / asking, 2026-11-10)
- S-rank hunt materials (Thread Core, Mask Core, Parchment Core, Seed of False Vitality, Shard of Willful Steel,
  Cracked Auditory Core): sold ~1.5M-3.5M per stack of 10; asking 2.0-2.5M per 10.
- Kunai to buy later: Ikazuchi listed 20M/50 (buyout 25M); Elemental 35M/100.
- Many "2 ryo" sales are DIRECT gifts between friends: ignore them for pricing.
