# Isonade v7 probe: rules that a player's own effects can set off (OFFLINE, nothing live)

The director (2026-11-19 23:47Z) settled Scour and Silt Cloud at **cooldown 5**. He also asked that a player's
move-prevent on Isonade must not throw off the whole fight. He likes "break the shield and it stops X". He then asked
whether cooldowns and rule order alone could do it. This page answers both from the engine and the sim.

## How the rules read effects

`has_effect` (engine `ai_v2.ts`) adds up the power of **every** effect of that type on Isonade, whoever cast it.
So every chain marker that is also a player debuff can be set off by a player. A player's root is enough to fire
the Undertow.

**Power reset.** These tags are reset to power 100 when they land (`tags.ts`), so a higher power on Isonade's own
marker can't tell it apart from a player's: buffprevent, debuffprevent, fleeprevent, healprevent, moveprevent,
onehitkillprevent, robprevent, cleanseprevent, clearprevent, sealprevent, stunprevent, summonprevent and disarm.

**Tags that keep their power:** seal and elementalseal.

**Shared cooldowns.** Seal (and moveprevent) carry a 3-round shared cooldown on the caster. Elementalseal does not.

## Live rules (profile 3xrmVKb3oAZDQ7YzpGh-S, read 2026-11-19 23:5xZ)

"Player can trip" counts jutsu in the last player catalog capture (1,186 jutsu, harvest 1794368544997). Items and
bloodlines are not counted.

| # | Rule: condition | AP | Casts | Player can trip? |
|---|---|---|---|---|
| 0 | always | 10 | It Rises (visual) | no |
| 1 | disarm and shield on Isonade | 60 | The Deep Crashes: 800 to the player, cleanses itself | needs a player disarm (0 found) while Barnacle's shield is up |
| 2 | disarm | 60 | Surfaces: weakness on itself | player disarm (0 found) |
| 3 | seal | 60 | Black Water Floods: 900 to all hexes but crates | **yes: 18 jutsu seal.** Floods with no omen |
| 4 | increasepoolcost and robprevent | 60 | Tidal Bore 900 | needs robprevent (0 found) |
| 5 | increasepoolcost | 60 | Swell Rises (sets robprevent) | **yes: 16 jutsu.** Bore early with a one-turn warning, or spent before 55% |
| 6 | health below 35% | 70 | Omen: The Deep | no |
| 7 | player increasedamagegiven ≥ 100 | 60 | Scour | by design (the player's own buffs) |
| 8 | player increasedamagegiven ≥ 90 | 30 | Silt Cloud | by design |
| 9 | moveprevent | 60 | Undertow 450 + wound | **yes: 16 jutsu (Dragon's Tomb)** |
| 10 | healprevent | 60 | Brine Brand (cooldown 99) | yes: 4 jutsu. Brand early, then the real chain has none |
| 11 | elementalseal | 60 | Harpoon Line | 1 jutsu (power 80); Harpoon is also a fallback |
| 12 | increasecooldown | 60 | Breaker 600 + wound | 1 jutsu: a Breaker with no Tide warning |
| 13 | fleeprevent | 60 | Tide Draws Back (cooldown 99) | 1 jutsu |
| 14 | health below 75% | 60 | Omen: Black Water | no |
| 15 | health below 55% | 60 | Swell Builds | no |
| 16 | always | 60 | Barnacle Hide (sets fleeprevent) | no |
| 17 | always | 60 | Harpoon Line | no |
| 18 | no summon | 30 | Grasping Arm | no |
| 19 | always | | end turn | |

The chain runs once a fight: Barnacle → fleeprevent → Tide → increasecooldown → Breaker → elementalseal → Harpoon →
healprevent → Brine → moveprevent → Undertow. Tide and Brine have cooldown 99, so the only intended Undertow is the
one after Brine. Every later Undertow in a fight comes from a player root.

**The Deep's crash** (rule 1) is an 800-power hit on the player wherever they stand, and it cleanses Isonade's own
debuffs. It fires the turn after the omen only if the 4,000 shield still stands. Break the shield and the disarm
alone is left, so Isonade Surfaces exposed instead. That is the live "break it and it stops X".

## Sim (harness `isonade_v7.ts` = v5 + a root/seal stand-in; v6 cd-5 params; 12 seeds; reads every tell)

**Root stand-in:** moveprevent 100 for 1 round, 30 AP, cooldown 4, no damage, cast whenever ready. Because it deals
no damage and costs AP, every root variant wins less whatever the fix. The column that matters is stray Undertows.

| Variant | Root player? | Win | HP left (wins) | Undertows/fight (intended + stray) | Stray hit | Intended Undertow lost |
|---|---|---|---|---|---|---|
| Live v6 | no | 66.7% | 39% | 1 + 0 | | 0/12 |
| Live v6 | yes | 16.7% | 4% | 1 + **2.6** | 896 | 0/12 |
| **B** cooldown 99, rule moved just above Barnacle | no | 75% | 39% | 0.8 + 0 | | **2/12** (lapsed) |
| **B** | yes | 50% | 40% | 0.3 + **0.7** | 896 | **8/12** (an early root used it up) |
| A, moveprevent power 1000 | no | | | 0 + 0 | | **12/12** (the engine resets it to 100) |
| **A2** Brine marks itself elementalseal 1000; Undertow needs ≥1000; Harpoon needs ≥100 | no | 66.7% | 27% | 1 + 0 | | 0/12 |
| **A2** | yes | 16.7% | 19% | 1 + **0** | | 0/12 |
| **C** Undertow needs the Brand on the player (≥200) | no | 66.7% | 58% | 0 + 0 | | Cleanse skips it every time |
| **C** | yes | 33.3% | 43% | 0 + 0 | | |
| Live v6, seal player | seal | 66.7% | 60% | | Floods: **2.3 stray/fight, ~1,792 each** | |
| Seal key 1000 (BW omen seal 1000, Floods needs ≥1000) | seal | 100% | 56% | | Floods: 0 stray | |

What this shows:

- **Cooldowns and order alone can't do it.** The Undertow is ready from round 1, so an early root fires it, and with
  cooldown 99 that early, unbranded Undertow uses it up. A longer cooldown also made the intended Undertow lapse
  in 2 of 12 clean fights. That is the same cooldown-and-marker timing slip that broke earlier retests.
- **A2 is clean.** No root ever fires it, and the intended Undertow never lapses. One slip: Brine's elementalseal
  lingers a round, so the Harpoon rule fires once in the slot right after the Undertow, where Barnacle used to.
  That costs the player about 365 more HP a fight.
- **C is the "break it and it stops X" version.** Cleanse removes the Brand, and with it the Undertow. It is also
  root-proof, but the Cleanse window becomes "skip it" instead of "halve it", so the fight gets easier (58% HP left).
- **Player seals are the bigger hole.** They set off Black Water Floods with no omen. The same power key on the seal
  fixes it in the sim.
- **Not yet keyed:** Swell Rises, Brine, Breaker and Tide can also be set off by player debuffs. Their markers are
  reset-to-100 types, so they need elementalseal or seal tiers too. Not designed yet.
