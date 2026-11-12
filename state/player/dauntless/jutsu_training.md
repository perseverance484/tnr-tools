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
| 2026-11-10 14:16 | Earth Armor 4-5, First Chakra Gate 4, Divine Pulse 4, Raijin's Judgement 3 | | | queued (queue was empty); 5,050 energy to intelligence (+547.7); asleep |
| 2026-11-11 03:21 | Ryūsa Kōka | 4-5 | 11,243 | started (queue was empty; 0.4/level checked) |
| 2026-11-11 03:21 | Raijin's Judgement | 4 | 3,143 | queued |
| 2026-11-11 03:21 | Divine Pulse | 5 | 6,647 | queued |
| 2026-11-11 03:21 | First Chakra Gate | 5 | 4,472 | queued (active Ryūsa Kōka 4; waiting Ryūsa Kōka 5, Raijin 4, Divine Pulse 5, FCG 5; ends ~05:58); 4,289 energy to willpower (+483.2, intelligence had passed willpower); asleep |
| 2026-11-11 07:31 | none | | 0 | queue empty, not refilled: character was in PvP battle vs 4qua (started 07:21, lost at 0 HP), now HOSPITALIZED in 177; startTraining refused ("You are in the hospital"). Did not check out; director notified |
| 2026-11-11 10:21 | bank.toPocket 10,000,000 | | | pocket was 1,941,486 |
| 2026-11-11 10:22 | Raijin's Judgement | 5-6 | 10,833 | started (queue was empty). Character was status TRAVEL in sector 1335 (not home), being moved live by another session without the run lock; follow-up startTraining refused ("You are traveling"), travel re-issued (finish 10:25). Stopped: no more queueing, no stat training, not put to sleep. Director notified |
| 2026-11-11 11:30 | Divine Pulse 6, Ryūsa Kōka 6, Earth Armor 6 | 1 each | 25,587 total | queued (active Raijin's Judgement 6, ends ~11:46; 3 waiting). Pocket 11.9M, no withdrawal. Character again moved live by another session without the run lock (AWAKE in 1490, then 99, then TRAVEL back to 1490 within 2 min; API rate-limited); First Chakra Gate 6 refused ("You are traveling"). Not home: no stat training, not put to sleep. Director notified |
| 2026-11-11 13:26 | none | | 0 | queue empty (no levels waiting), not refilled: First Chakra Gate 6 refused ("You are traveling"). Character AWAKE, moved live by another session while this run held the lock (sector 1490 at 13:25, 1335 a minute later). Pocket 7.98M, no withdrawal. Not home: no stat training, not put to sleep. Director notified |
| 2026-11-11 15:23 | none | | 0 | queue already full (4 waiting: Raijin 7, Earth Armor 7, FCG 7, Mental Fortress 9; ends ~19:47), queued outside this log. Pocket 7.50M, no withdrawal. Character AWAKE in sector 99 (not home): no stat training, not put to sleep |
| 2026-11-11 20:23 | Ryūsa Kōka | 7 | 13,901 | queued (active ends 21:47; waiting FCG 8, Earth Armor 8-9, Ryūsa Kōka 7; ends ~01:36). Pocket 4.13M, no withdrawal. 4,550 energy to willpower (+268.55, intelligence had passed willpower); asleep |
| 2026-11-11 22:23 | bank.toPocket 10,000,000 | | | pocket was 1,874,157, now 11,874,157 |
| 2026-11-11 22:23 | none | | 0 | queue already full (active ends 22:47; waiting Earth Armor 8-9, Ryūsa Kōka 7, Thunderbolt Fury 19; ends ~02:36). Thunderbolt Fury 19 (620,939 reserved) was queued outside this log. No training started, so the character stayed ASLEEP in 177; 1,301 energy left unspent rather than waking it |
| 2026-11-11 23:23 | Divine Pulse | 8 | 20,103 | queued (active Earth Armor 8 ends 23:47; waiting Earth Armor 9, Ryūsa Kōka 7, Thunderbolt Fury 19, Divine Pulse 8; ends ~03:33). Pocket 11.87M, no withdrawal. 4,550 energy to willpower (+269.08, intelligence had passed willpower); asleep |
| 2026-11-12 00:23 | Ryūsa Kōka | 8 | 20,103 | queued (active ends 00:47; waiting Ryūsa Kōka 7, Thunderbolt Fury 19, Divine Pulse 8, Ryūsa Kōka 8; ends ~04:30). Pocket 11.83M, no withdrawal. 4,550 energy to intelligence (+383.15); asleep |
| 2026-11-12 01:25 | Raijin's Judgement | 8 | 12,872 | queued (active Ryūsa Kōka 7 ends 01:36; waiting Thunderbolt Fury 19, Divine Pulse 8, Ryūsa Kōka 8, Raijin 8; ends ~05:30). Pocket 11.82M, no withdrawal. 4,550 energy to willpower (+383.15, intelligence had passed willpower); asleep |
| 2026-11-12 02:30 | First Chakra Gate | 9 | 18,310 | queued (active ends 02:36; waiting Divine Pulse 8, Ryūsa Kōka 8, Raijin 8, FCG 9; ends ~06:30). Pocket 11.82M, no withdrawal. 4,550 energy to intelligence (+269.08); asleep |
| 2026-11-12 03:22 | Divine Pulse | 9 | 29,072 | queued (active Divine Pulse 8 ends ~03:33; waiting Ryūsa Kōka 8, Raijin 8, FCG 9, Divine Pulse 9; ends ~07:30). Pocket 11.77M, no withdrawal. 4,550 energy to willpower (+269.08, intelligence had passed willpower); asleep |
| 2026-11-12 04:23 | Ryūsa Kōka | 9 | 29,072 | queued (active Ryūsa Kōka 8 ends ~04:30; waiting Raijin 8, FCG 9, Divine Pulse 9, Ryūsa Kōka 9; ends ~08:30). Pocket 11.77M, no withdrawal. 4,550 energy to intelligence (+269.08); asleep |
| 2026-11-12 05:23 | Raijin's Judgement | 9 | (cost not returned) | queued (active Raijin 8 ends ~05:30; waiting FCG 9, Divine Pulse 9, Ryūsa Kōka 9, Raijin 9; ends ~09:30). Pocket 11.74M, no withdrawal. 4,550 energy to willpower (+269.08, intelligence had passed willpower); asleep |
| 2026-11-12 06:25 | Limit Breaker | 10 | 42,043 | queued (active FCG 9 ends ~06:30; waiting Divine Pulse 9, Ryūsa Kōka 9, Raijin 9, Limit Breaker 10; ends ~10:30). Pocket 11.68M, no withdrawal. 4,550 energy to intelligence (+383.15); asleep |
| 2026-11-12 07:27 | Mental Fortress | 10 | 42,043 | queued (active Divine Pulse 9 ends ~07:30; waiting Ryūsa Kōka 9, Raijin 9, Limit Breaker 10, Mental Fortress 10; ends ~11:30). Pocket 11.64M, no withdrawal. 4,550 energy to willpower (+383.15, intelligence had passed willpower); asleep |
| 2026-11-12 08:23 | Divine Pulse | 10 | 42,043 | queued (active Ryūsa Kōka 9 ends ~08:30; waiting Raijin 9, Limit Breaker 10, Mental Fortress 10, Divine Pulse 10; ends ~12:30). Pocket 11.60M, no withdrawal. 4,550 energy to intelligence (+269.08); asleep |
| 2026-11-12 09:23 | Earth Armor | 10 | 26,045 | queued (active Limit Breaker 10 ends ~10:30; waiting Mental Fortress 10, Divine Pulse 10, Earth Armor 10; ends ~13:30). Pocket 11.57M, no withdrawal. 4,550 energy to willpower (+269.08, intelligence had passed willpower); asleep |
| 2026-11-12 10:23 | Raijin's Judgement | 10 | 26,045 | queued (active Limit Breaker 10 ends ~10:30; waiting Mental Fortress 10, Divine Pulse 10, Earth Armor 10, Raijin 10; ends ~14:30). Pocket 11.55M, no withdrawal. 4,550 energy to intelligence (+269.08); asleep |
| 2026-11-12 11:25 | none | | 0 | not refilled: 3 waiting (Divine Pulse 10, Earth Armor 10, Raijin 10; ends ~14:30). profile.getUser failed 5x over ~3 min ("The database could not complete this request"), so status/sector/battle/pocket could not be checked; startTraining would wake the character with no way to confirm it home or put it back to sleep. No ryo, energy or sleep change |
| 2026-11-12 12:24 | First Chakra Gate | 10 | 26,045 | queued |
| 2026-11-12 12:25 | Ryūsa Kōka | 10 | 42,043 | queued (active ends ~12:30; waiting Earth Armor 10, Raijin 10, FCG 10, Ryūsa Kōka 10; ends ~16:30). Pocket 11.48M, no withdrawal. 4,550 energy to willpower (+383.15, intelligence had passed willpower); asleep |
| 2026-11-12 13:24 | Limit Breaker | 11 | 60,800 | queued (active Earth Armor 10 ends ~13:30; waiting Raijin 10, FCG 10, Ryūsa Kōka 10, Limit Breaker 11; ends ~17:30). Pocket 11.42M, no withdrawal. 4,550 energy to intelligence (+383.15); asleep |
