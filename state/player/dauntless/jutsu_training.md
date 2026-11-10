# Jutsu training queue (dauntless)

Director (2026-11-09): "Maintain an active jutsu training queue. Identify jutsu of interest and train them."
"I can transfer jutsu levels for free infinitely as staff, yes this is allowed. But I also have substantial ryo so
I'd like to continue expanding my jutsu levels." So keep ryo training running at all times; level transfers are
allowed too.

## Rules
- `jutsu.startTraining {jutsuId, levels 1-5}`; `jutsu.getTrainingQueue` (5 waiting slots behind the active level).
  Each level takes 1 hour. Starting training wakes the character: go back to sleep after (`home.toggleSleep`).
- Cost per level rises about 1.48x per level (Ethereal: lv9 55,831, lv10 82,642, lv11 122,329, lv12 181,075 ryo).
  Training levels 8-12 cost 479,594 in total. A 24-25 level costs tens of millions, so the cheap low levels
  give the most power per ryo.
- `jutsu.transferLevel {fromJutsuId, toJutsuId, transferLevels}`: source must be level 10+, target max 25, cancel
  queued training on either first. Moves levels; doesn't add them.
- Power at level L = power + (L-1) x powerPerLevel. In-battle numbers scale with this.

## PvP loadout: nothing to train
Director (2026-11-09): "ethereal rebirth doesnt scale, no need to train it. It can level through PvP use alone."
Every equipped PvP jutsu is either level 25 or has powerPerLevel 0 (Ethereal Rebirth, Eclipse Drain, Thunder's
Judgement, Shrapnel Clone Barrage, Parry: descriptions say "DON'T TRAIN. ALREADY CAPPED"). They level by use.
**Before training anything, check `jutsu.get` effects powerPerLevel > 0.**

## Director (2026-11-09, 22:17-22:19 local)
"Anything that looks useful, I have 1billion ryo banked. You will perform ryo producing activities to offset your
expenditures. Blank check granted." "The new potency skills and 40ap stance skills are interesting. Chakra Edge,
Choha, etc." "Limit Breaker, Mental Fortress..."
- Withdraw from the bank with `bank.toPocket` in batches; keep about 10M in pocket, the rest banked (`bank.toBank`).
- Log what is spent; offset it later with ryo-producing play (missions, hunter contracts, PvP).

## Limits (source: routers/jutsu.ts, libs/train.ts)
- Training cap is level 20 for Jonin (`JUTSU_LEVEL_CAP`; Elite Jonin 30). Levels 21-25 come from use or transfer.
- "Jutsu not for you": element/bloodline lock. My elements: Lightning (primary), Earth (secondary); mastery Fire,
  Water. Chōha (Water) and Fire Style: Beast (other bloodline) are refused.
  Enjin (Fire) refused 2026-11-10 10:22 UTC ("Jutsu not for you"): skip it.
- Queue: 4 waiting levels behind the active one in practice. Starting training wakes the character; sleep after.
- Time per level = (1 + (level-1) x k) minutes, k = D7 C8 B9 A10 S11, capped at 1 hour. Low levels take minutes,
  so the greedy rule is: always queue the target whose next level is quickest.
- `jutsu.stopTraining` drops the active level and the whole waiting queue (refund the queue first if needed).

## Training targets (priority order; skip any that says "not for you" and note it)
1. 40-AP potency/stance self-buffs (+20 dmg given scaling 0.4/level, potency fixed):
   Limit Breaker `P7dDcC102RhwBTTgA4HU_` (no element, C), Mental Fortress `UiBR2V2AKkmh64JiYlL3w` (no element, C),
   Divine Pulse `7rYARNUr1kXiJb3VLXqUb` (no element, 2 potency tags, C), Raijin's Judgement `GsDJufr8bn-55VSGPe0hA`
   (Lightning potency, B), Earth Armor `CWdsrv5uM2R3hEyG6fvaX` (Earth, B), Enjin `PwTpi68-ZNKk5CnsR9Q8_` (Fire, B),
   First Chakra Gate `rCmgi5gtJb-wnPfuwruI2` (+20 given/-20 taken, B), Ryūsa Kōka `sEDO_J07YRbTqHnxuPUA5` (lv3).
2. Scaling damage/setup jutsu near the cap: Soul Laceration Mirage `GlgS3FVoQ6F8k3RAo_Uht` (19),
   Thunderbolt Fury `INuy-ITnPsH22eUoGQgwW` (18), Phantom Requiem `kbrQuf3nYNHoKEvusATTO` (18),
   Cyclone Palm Strike `pqCqPemRNk3ht-SFrjq5G` (18), Ethereal Nexus `iktsCP-RjIhlYlsTg-JTN` (10).
Owned already at 25: Chakra Edge, Gust Armor (Wind potency).

## Cost (libs/train.ts calcJutsuTrainCost)
base (D 50, C 100, B 150, A 200, S 250, + extraBaseCost) ^ (1 + level/20). Low levels are cheap; high levels are
very expensive (Cyclone Palm Strike level 19 quoted 1,949,575 ryo for one level; cancelled pending director).

## Queue log
| Started (UTC) | Jutsu | Levels | Ryo | Result |
|---|---|---|---|---|
| 2026-11-10 04:11 | Ethereal Rebirth | 8-12 | 479,594 | 9-12 cancelled and refunded (no scaling); level 8 left to finish ~05:11 |
| 2026-11-10 04:20 | Cyclone Palm Strike | 19 | 1,949,575 | cancelled and refunded |
| 2026-11-10 04:20 | bank.toPocket 30,000,000; bank.toBank 23,000,000 after | | | |
| 2026-11-10 04:21 | Soul Laceration 20, Thunderbolt Fury 19-20 | | 3,396,964 | cancelled and refunded (moved potency jutsu first) |
| 2026-11-10 04:21 | Ethereal Rebirth lv8 | | ~37,000 | stopped (no scaling) |
| 2026-11-10 04:21 | Limit Breaker 1-4 (learned), Mental Fortress 1 (learned) | | 13,011 | queue ends ~05:13 |
| 2026-11-10 08:23 | Mental Fortress | 3 | 3,178 | queued (4 waiting: Limit Breaker 7-9, Mental Fortress 3); Divine Pulse 2 refused, queue full; 1,228 energy to intelligence; asleep |
| 2026-11-10 09:23 | Divine Pulse | 2 | 2,197 | queued (4 waiting: Limit Breaker 8-9, Mental Fortress 3, Divine Pulse 2; ends ~11:49); 4,550 energy to intelligence; asleep |
| 2026-11-10 10:22 | Earth Armor | 1 (learned) | 1,092 | queued (active Limit Breaker 9; waiting Mental Fortress 3, Divine Pulse 2, Earth Armor 1; ends ~11:50); Enjin refused (not for you); First Chakra Gate 1 refused, queue full; 4,550 energy to intelligence; asleep |
| 2026-11-10 11:25 | First Chakra Gate | 1 (learned) | 1,092 | queued |
| 2026-11-10 11:25 | Raijin's Judgement | 2 | 1,553 | queued (active Mental Fortress 3; waiting Divine Pulse 2, Earth Armor 1, First Chakra Gate 1, Raijin's Judgement 2; ends ~12:01); 4,550 energy to intelligence; asleep |
| 2026-11-10 12:25 | Earth Armor | 2 | 1,553 | started (queue was empty) |
| 2026-11-10 12:25 | First Chakra Gate | 2-3 | 3,762 | queued |
| 2026-11-10 12:25 | Divine Pulse | 3 | 3,178 | queued |
| 2026-11-10 12:25 | Earth Armor | 3 | 2,209 | queued (active Earth Armor 2; waiting FCG 2, Divine Pulse 3, Earth Armor 3, FCG 3; ends ~13:40); 4,550 energy to intelligence; asleep |
