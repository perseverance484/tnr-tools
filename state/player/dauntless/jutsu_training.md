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
  For the AI player this is replaced by RUL-2026-11-12-153: at most 200,000 in pocket while running around;
  up to 10,000,000 may be drawn for training.
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

## Donor jutsu (train first, cap level 10)
Donors are kept at level 10 so the daily transfer can take 5 levels from them. When a donor is below 10, its next
level comes before every target below (it is cheap and short), and it is never trained past 10.
- Stone of the Withering `CTYkpwuoqS9mJkOB3Lm8U` (Earth, C, extraBaseCost 1500, not equipped): 5 after the
  2026-11-17 transfer; 6 trained, 7-10 queued 2026-11-17 19:23 (back to 10 ~23:19).

## Daily level transfer (director, 2026-11-16)
"Once per day I want you to use the free jutsu transfer to hard cap a jutsu at 25. Pick a jutsu and transfer 5 levels
from a donor jutsu. Ideal donor jutsu would be level 10, then you would train it from 5 to 10 again. This is because
10 is the lowest level a jutsu can be to transfer its levels to another jutsu and thus you can train it from a low
level and save ryo then transfer it onto another jutsu." One `jutsu.transferLevel` call in any 24 hours
(RUL-2026-11-11-149 item 3; `data/player_allowlist.json` gate `one_transfer_a_day`): check `jutsu.getRecentTransfers`
first and skip the day if the last transfer is under 24 hours old.
- Target: a jutsu at exactly level 20 with powerPerLevel > 0, not the active level and not in the waiting queue,
  taken in this order: Mental Fortress, Divine Pulse, Raijin's Judgement, Earth Armor, First Chakra Gate, Ryūsa Kōka,
  Soul Laceration Mirage, Thunderbolt Fury, Ethereal Nexus, then any other list-3 jutsu that reaches 20.
- Donor: one of the donor jutsu above at level 10 (or more), not equipped, nothing queued for it. If no donor is at 10,
  skip the day and say so. Never use an equipped jutsu or a target-list jutsu as a donor.
- Move exactly 5 levels (20 -> 25), read `jutsu.getRecentTransfers` back, then queue the donor's level 6 if a queue
  slot is free (the hourly refill trains the rest).
- If the game would charge reputation points or anything else (the message should say "0 reputation points"), stop
  and report instead.

## Training targets (priority order; skip any that says "not for you" and note it)
1. 40-AP potency/stance self-buffs (+20 dmg given scaling 0.4/level, potency fixed):
   Limit Breaker `P7dDcC102RhwBTTgA4HU_` (no element, C), Mental Fortress `UiBR2V2AKkmh64JiYlL3w` (no element, C),
   Divine Pulse `7rYARNUr1kXiJb3VLXqUb` (no element, 2 potency tags, C), Raijin's Judgement `GsDJufr8bn-55VSGPe0hA`
   (Lightning potency, B), Earth Armor `CWdsrv5uM2R3hEyG6fvaX` (Earth, B), Enjin `PwTpi68-ZNKk5CnsR9Q8_` (Fire, B),
   First Chakra Gate `rCmgi5gtJb-wnPfuwruI2` (+20 given/-20 taken, B), Ryūsa Kōka `sEDO_J07YRbTqHnxuPUA5` (lv3).
2. Scaling damage/setup jutsu near the cap: Soul Laceration Mirage `GlgS3FVoQ6F8k3RAo_Uht` (19),
   Thunderbolt Fury `INuy-ITnPsH22eUoGQgwW` (18), Phantom Requiem `kbrQuf3nYNHoKEvusATTO` (18),
   Cyclone Palm Strike `pqCqPemRNk3ht-SFrjq5G` (18), Ethereal Nexus `iktsCP-RjIhlYlsTg-JTN` (10).
Owned already at 25: Chakra Edge, Gust Armor (Wind potency), Limit Breaker (transfer 2026-11-16), Mental Fortress (transfer 2026-11-17).
3. Director (2026-11-16): "I want all Jonin level elemental and none jutsu trained next." Jonin-rank
   (requiredRank JONIN), non-bloodline, element None or one of mine (Lightning, Earth), at least one effect
   powerPerLevel > 0, not yet at 20 (found with `jutsu.getAll {rank:[JONIN], excludedJutsuTypes:[AI,PETS,BLOODLINE]}`).
   Same greedy rule: lowest next level first. Skip and note any "not for you" or other refusal.
   - Owned: Crescent Reaper Fang `cjRErpuffG4GiwIU8OsCw` (0, A), Inferno Leech `0nIgI7oNn-PSesn8T8kGl` (2, A),
     Kinjutsu: Black Thorn Rose `qB550OM_X-Mh0w_KlNNji` (7, S), Hellfire Apparition `LXBw6TW0yRxGOfUhaTMkT` (13, S).
   - Normal, not owned yet: Void Pulse Barrage `4eDM_5VVZkasBjaW2fEmI`, Summoning: Unholy Harvest
     `_rfLi3-QHtVefymRDhDQk`, Shard Pulse Eruption `qVL7NnmNN949g-VH9lyAN`, Chakra Overflow `e2eC-x4UXc5m6QexNbx8w`,
     Sealing Technique: Lotus Barrier `04HFzvH0IvRZBEc3mGM_r`, Summoning: Hell Hound `kP_KMs7H9wQJwRHeaTGCZ`
     (needs level 70), Summoning Poison Salamander `JcZb5OE6sMoDxvOKhuKWv` (all A).
   - Event/special/forbidden, not owned (may be refused if they come from quests or events): Dark World
     `p4N7lt4QgQjLytzkXJTz9` (Lightning, S), Black Crow `c-yTyBUJil8MzlAIHApUG` (Earth, D), Lastlight
     `0F-68bxOXW_LkJnXV0lwT`, Forbidden Art: Heaven's Rupture Oath `lOZQks4GCxjXsNQxop-zo` (S, level 80),
     Crippling Blade `z17S47TiSnNBgQMVkxsnH` (S), Dark Pact `NJMGDcIzIkL9pF5qElwre`, Summoning: Momo
     `_mTOi6z16b3PNyCSaKcs9` (S).
   - Left out: Primordial Blight (0.04/level only), Phantom Requiem 19 (already in list 2), village totems
     (other villages), test entries (Sage Mode Test 3, Storm Style ... 2), and Fire/Water/Wind/Yin-Yang jutsu.
     No scaling, so not trained: Cosmic Explosion/Rift/Gravity, Corrupting Miasma, Black Coffin, Earthen Bastion,
     Celestial Dew, Flash Pulse, Echoing Rift, Kuzenbo x3, Herald of the
     Apocalypse, Spirit Wall.

4. Director (2026-11-17): add the Chunin-rank jutsu, owned and not owned. Chunin rank (requiredRank CHUNIN),
   type NORMAL, non-bloodline, not another village's, elementClassification None/Lightning/Earth, at least one
   effect powerPerLevel > 0, below 20. Same greedy rule as list 3 (all targets in lists 3 and 4 compete: lowest next
   level first). Skip and note any "not for you" or other refusal. Not included: Genin jutsu and the special/event
   leftovers (director declined for now); Cyclone Palm Strike (still pending) and the donor.
   - Owned (28): Crimson Surge `2JqtZoGk8FuMbym6Ng5zc` (15, C, None), Rock Fortress Strike `p0-15kTrb_uMirGLE5p5R`
     (15, C, Earth), Crimson Vein `GGms9iTcZq_gICEuZYF2Q` (15, C, None), Stormguard Aura `J2KOpNHk5LJthnzb27H1h` (13,
     B, None), Martial Movement `V34OBxnSDj6PfxT4Y3fhx` (12, C, None), Decapitating Slash `mXC6PujAXANZwri71jOTZ` (11,
     C, None), Stunning Jab `VT7oxj_fObWuQa3Rq_BbI` (8, B, None), Lightning Drift `57xgGwYtfhQXFQePC4_V4` (7, B,
     Lightning), Storm Fist `j2H5lwEkOq4HwxgMR9a4j` (7, B, Lightning), Veil of Shadows `l6iUf3mc7LZQQEDDif1zW` (6, C,
     None), Void Rend `_QfGq0SseWD11jHO23pr1` (5, C, None), Stone Dance Slash `UMGgKY9iM29Xtcfqb1qyO` (3, C, Earth),
     Rejuvenating Chakra `fAKcf34Vlt_-utDdDdjxH` (3, C, None), Earthquake Fist `eX60fhnB15ChiqatViMjS` (2, C, Earth),
     Netherblight `l5kgBGL2CZjzLMW5wFHdP` (1, C, None), Rock Cleaver `bP9QCHwyqyP8nBNDlN9mC` (1, C, Earth), Rending
     Slash `B6AWSCTjuD_BCcqUU1qZi` (1, C, None), Stormguard Retaliation `ZDXT84wQHPqA3Lri8u8ue` (1, C, Lightning),
     Static Flicker `UwWqo_4Igdue7-unPXwne` (1, C, Lightning), Terra Shift `CLlN7iJPGCGRIDbJTo4P5` (1, B, Earth), Fist
     of 10 ,000 Volts `JKgaTbuFTeNZjYOXrb49M` (1, B, Lightning), Guard `lNvXZycno0P0LKOMuo6Zr` (1, B, None), Storm's
     Lullaby `Ac1nbz3RUrPCCWmiOl7Jr` (1, B, None), Primate Assimilate `AFxOB8St3rqdY3xqkBJo4` (1, B, None), Chakra
     Enfeeblement `FlQ0Mk8CB7afkYqxFempz` (1, C, None), Boulder Barrage `fEMP_dLlFKLg-BbQ7S0Hm` (1, C, Earth), Quaking
     Earth Strike `VOS_VDwAUUlpYxYlNSLnt` (1, B, Earth), Inner Flame `kUcL8K94TW3iCkRcoik_7` (1, B, None).
   - Not owned yet (67): Earthquake Slam `W3DYPc2NbNjFP8KJlrWAG` (B, Earth), Eight Fist Style: Earthen Grasp
     `0LpgkGVTHrg3mJXFTQPNK` (B, Earth), Ganpaken `YyvGod-dr31VQJQYJKxwC` (B, Earth), Stone Stomp
     `oi7gQl0TuwV8oPcLXGhi6` (B, Earth), Tectonic Stomp `CXbUs7Ew7JVkh72rRWNrD` (B, Earth), Earth Release: Earthquake
     `1fkXurgdTdV5QkLZiG0LH` (C, Earth), Earth Release: Seven Heavenly Pillars `0f-qDg-CcolKVZ25lVY7k` (C, Earth,
     needs level 50), Gaia's Wrath `2Ye-jrvIAdn2Ckk6lqhiP` (C, Earth), Graveyard of Stone `Ad0K8Kgo0WqDgDt5E4lkx` (C,
     Earth), Mountain Crusher `yNyBxYW9BupuWp1R_ssWp` (C, Earth), Quaking Fist `XVHy-OORSuDuZi0U8jXu3` (C, Earth),
     Quicksand Trap `fv98USDeNTb8DFPgBkfDS` (C, Earth), Stone Breaker `VUDhCjKW-RseBAAl7Ag-b` (C, Earth), Stone Hammer
     Kick `ixKFXfF3g16_kIj5AksTs` (C, Earth), Stone Warden `rhXnjfAdFMqYavvjX1Qp_` (C, Earth), Stonebreaker Strike
     `ntGBMLX_UAwPgGw0vytDU` (C, Earth), Divine Thunder Slap `Je0gvHDVCm__vy2rT8YBB` (B, Lightning), Eclipse Cyclone
     `UgCKhDiEvNuXsrwf85tMM` (B, Lightning), Lightning Blitz Strike `HNMweb8uPrZFIJXlMhdkm` (B, Lightning), Lightning
     Release: Raijin's Bow `cEu_gGsh8kJk0JIBI64ga` (B, Lightning), Lightning Release: Spark Blade
     `LwCDZpiRgXoApfDUnBNPa` (B, Lightning), Lightning Release: Stormcaller Whip `BEaaogbbqkL_WeEk95bPH` (B,
     Lightning), Lightning Release: Thunder Edge `aj1gDBeNKzxWKEPOPiKKp` (B, Lightning), Lightning Surge
     `OqGevgRisdJXE2EpHl5XK` (B, Lightning), Raijin Puncture `ixCVqH2jC1nbB2Mul5uSb` (B, Lightning), Retribution
     `ZnXkvxDfvw6SNtpVj7yhe` (B, Lightning), Thunderbolt Fusillade `WfluLTdmhSRBkOCbLK54Q` (B, Lightning), Arashi
     Ikari `eJISnE5IrvC09FuoeuQ5X` (C, Lightning), Arcbound Vortex `Yp9zmQuJBdL8BmCbQAjTp` (C, Lightning, needs level
     50), Bolt of Terror `7_Mxzow6OAyK8UF9-HXgn` (C, Lightning), Electric Prison `Y57kLbqcGN7PYeWBAg0d6` (C,
     Lightning), Rai Yari `lTgAFUgVj1Erzh6LbzI0w` (C, Lightning), Rensa Kaminari `TI1JQAG1ltx_uLHE9-UUs` (C,
     Lightning), Storm Kick `exOKjKQiIi0r2xFxGWC6n` (C, Lightning), Thunder Fist `WWc1ny_fRgPXEy2N5ZgXU` (C,
     Lightning), Thunder Shockwave `ipNt-D4NAs-4r_7rUf873` (C, Lightning), Thunderbolt Spear `41ZvXLK7xw_Y2ePKdsCSB`
     (C, Lightning), Thunderstorm Delusion `80fuWZZhMMG7PtHFe09Qx` (C, Lightning), Thunderstrike Blade
     `DIveDAYAb_4uNUaaSXnRJ` (C, Lightning), Thunderstrike Punch `6l-E6XDZfGr2h6q_1eQ-K` (C, Lightning), Volt Crash
     `fXpFymFNqyTPNiivQKGnv` (C, Lightning), Volt Jab Barrage `tAV232faDLgzFoYcnkWc3` (C, Lightning), Volt Reaper
     `ZZ3BNMarAAO-G2vI2zvHV` (C, Lightning), Iron Fist `Oi5pYxNaHa-5o737i5gAu` (A, None), Aqua Barrier
     `cUPCLvCCEO9MCSRtFsulW` (B, None), Cleansing Aura `MTH9bqTMRo8yJaD7J5Vx4` (B, None), Heaven's Blessing
     `gkZYgOkTp8sQ_6qLR0uIy` (B, None), Wind Dance `wL3GSeUVnts8GxCZCb4jB` (B, None), Bonecrusher Kick
     `PB70sBEpFd3AWm81h3w7R` (C, None), Chakra Palm `5JCcW9EdcDy7a5-0SiH_W` (C, None), Chakra Siphon
     `bETFmYm_J6RJRZTedogld` (C, None), Dreamshell `jkWkH36d6apM11qyt-Zn4` (C, None), Echoing Void
     `jy77jG_yHWnag4xQURz5s` (C, None), Force Wave `f_1_leJBO29rTRqPTkOs5` (C, None), Illusionary Celestial Mirage
     `UEZY8uf5EbpN7_8vIKiKH` (C, None), Lunar Descent `sks41OM0PDvM2RH_ECjQh` (C, None), Mind Flay
     `BkM8yq3J-P9SkCsCoKrtG` (C, None), Phantom Scythe `OkPqXUMvbXZPGH3UA-I6M` (C, None), Resounding Crescendo
     `kvuECU_A6qeZYsWwU_Zvq` (C, None), Rib Breaker `cNVnsrANAhtym1JmW1ZJl` (C, None), Senbon Sakura
     `eGKKXArrxlpzk9iZaWyOo` (C, None), Shattering Strike `uhEr3x6ucxHJbcjnTs7ps` (C, None), Spectral Chain
     `NavJ494P96fquk81SQxVF` (C, None), Summoning: Lord Pengu `eyp7n2EBpiRXavV6KG8Wa` (C, None), Swift Combination
     `ngoQnm-PqVMslvj3hcybD` (C, None), Toxic Pool `HBof21qe_fP_mUE5UNKtR` (C, None), Weary Fists
     `8TNJHxH0dswm6Tl52m_vn` (C, None).

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
| 2026-11-12 14:23 | Mental Fortress | 11 | 60,800 | queued (active Raijin 10 ends ~14:30; waiting FCG 10, Ryūsa Kōka 10, Limit Breaker 11, Mental Fortress 11; ends ~18:30). Pocket 11.36M, no withdrawal. 4,550 energy to willpower (+269.08, intelligence had passed willpower); asleep |
| 2026-11-12 15:22 | Divine Pulse | 11 | 60,800 | queued (active First Chakra Gate 10 ends ~15:30; waiting Ryūsa Kōka 10, Limit Breaker 11, Mental Fortress 11, Divine Pulse 11; ends ~19:30). Pocket 11.30M, no withdrawal. 4,550 energy to intelligence (+269.08); asleep |
| 2026-11-12 18:23 | bank.toPocket 10,000,000 | | | pocket was 150,000 (down from 11.30M at 15:22; spent or moved outside this log), now 10,150,000 |
| 2026-11-12 18:23 | none | | 0 | queue already full (active First Chakra Gate/Ryūsa Kōka slot ends 18:30; waiting Divine Pulse 11, Mental Fortress 12, Raijin 11, Earth Armor 11; ends ~22:30), Mental Fortress 12 queued outside this log. No training started, so the character stayed ASLEEP in 177; 1,720 energy left unspent rather than waking it |
| 2026-11-12 19:23 | First Chakra Gate | 11 | 37,048 | queued (active Divine Pulse 11 ends ~19:30; waiting Mental Fortress 12, Raijin 11, Earth Armor 11, FCG 11; ends ~23:30). Pocket 10.15M, no withdrawal. 139 energy to intelligence (+11.91); asleep in 177 |
| 2026-11-12 20:24 | Ryūsa Kōka | 11 | 60,800 | queued (active Mental Fortress 12 ends ~20:30; waiting Raijin 11, Earth Armor 11, FCG 11, Ryūsa Kōka 11; ends ~00:30). Pocket 10.05M, no withdrawal. 4,550 energy to intelligence (+273.87); asleep in 177 |
| 2026-11-12 21:23 | Limit Breaker | 12 | 87,924 | queued (active Raijin 11 ends ~21:30; waiting Earth Armor 11, FCG 11, Ryūsa Kōka 11, Limit Breaker 12; ends ~01:30). Pocket 9.96M, no withdrawal. 4,550 energy to intelligence (+273.87); asleep in 177 |
| 2026-11-12 22:23 | Divine Pulse | 12 | 87,924 | queued (active Earth Armor 11 ends ~22:30; waiting FCG 11, Ryūsa Kōka 11, Limit Breaker 12, Divine Pulse 12; ends ~02:30). Pocket 9.88M, no withdrawal. 4,550 energy to willpower (+273.87, intelligence had passed willpower); asleep in 177 |
| 2026-11-12 23:22 | Raijin's Judgement | 12 | 52,698 | queued (active First Chakra Gate 11 ends ~23:30; waiting Ryūsa Kōka 11, Limit Breaker 12, Divine Pulse 12, Raijin 12; ends ~03:30). Pocket ~9.82M, no withdrawal. 4,550 energy to intelligence (+273.87); asleep in 177 |
| 2026-11-13 00:35 | Earth Armor | 12 | 52,698 | queued |
| 2026-11-13 00:35 | First Chakra Gate | 12 | 52,698 | queued (active Limit Breaker 12 ends ~01:30; waiting Divine Pulse 12, Raijin 12, Earth Armor 12, FCG 12; ends ~05:30). Pocket 9.72M, no withdrawal. 4,550 energy to willpower (+389.96, intelligence had passed willpower); asleep in 177. Run waited ~13 min for an expired "play session" lock (character was asleep, not in battle) |
| 2026-11-13 02:25 | Ryūsa Kōka | 12 | 87,924 | queued (active Divine Pulse 12 ends ~02:30; waiting Raijin 12, Earth Armor 12, FCG 12, Ryūsa Kōka 12; ends ~06:30). Pocket 9.63M, no withdrawal. Waking the character drew an immediate PvP attack (Luminous, battle X-MJ9pJGWSkOn-teg8y4r, 02:25:55); the refill job doesn't fight or flee, so no stat training and no sleep; character left AWAKE IN BATTLE; director notified |
| 2026-11-13 04:23 | Limit Breaker | 13 | 127,148 | queued |
| 2026-11-13 04:23 | Mental Fortress | 13 | 127,148 | queued (active ends ~04:30; waiting FCG 12, Ryūsa Kōka 12, Limit Breaker 13, Mental Fortress 13; ends ~08:30). Pocket 9.36M, no withdrawal. Waking the character drew an immediate PvP attack again (AngelSaber, COMBAT battle u3su-FSTOvyM3W9vFTs7a, 04:23:29, both at 5,050 HP); the refill job doesn't fight or flee, so no stat training and no sleep; character left AWAKE IN BATTLE in 177; director notified |
| 2026-11-13 09:22 | bank.toPocket 10,000,000 | | | pocket was 150,531, now 10,150,531 |
| 2026-11-13 09:23 | Ethereal Nexus | 12 | 181,075 | started (queue was empty; powerPerLevel 0.4 checked) |
| 2026-11-13 09:23 | Divine Pulse | 13 | 127,148 | queued |
| 2026-11-13 09:23 | Earth Armor | 13 | 74,961 | queued |
| 2026-11-13 09:23 | Raijin's Judgement | 13 | 74,961 | queued |
| 2026-11-13 09:23 | First Chakra Gate | 13 | 74,961 | queued (active Ethereal Nexus 12 ends ~10:23; waiting Divine Pulse 13, Earth Armor 13, Raijin 13, FCG 13; ends ~14:23). Pocket 9.62M. 4,550 energy to intelligence (+549.86); asleep in 177 |
| 2026-11-13 11:23 | Ryūsa Kōka | 13 | 127,148 | queued |
| 2026-11-13 11:24 | Ethereal Nexus | 13 | 268,032 | queued (active Earth Armor 13 ends ~12:23; waiting Raijin 13, FCG 13, Ryūsa Kōka 13, Ethereal Nexus 13; ends ~16:23). Pocket 9.29M, no withdrawal. 2,369 energy to willpower (+286.29, intelligence had passed willpower); asleep in 177 |
| 2026-11-13 12:22 | none | | 0 | queue already full (active ends ~12:23; waiting Raijin 13, FCG 13, Ryūsa Kōka 13, Ethereal Nexus 13; ends ~16:23). Pocket 9.29M, no withdrawal. No training started, so the character stayed ASLEEP in 177; 5,050 energy left unspent rather than waking it |
| 2026-11-13 14:26 | none | | 0 | not refilled: TNR connector failed to connect this run (CONNECT_TIMEOUT), so no live calls were made. Last known queue (12:22 log) ends ~16:23. No ryo, energy or sleep change |
| 2026-11-13 15:24 | Limit Breaker | 14 | 183,874 | queued |
| 2026-11-13 15:24 | Mental Fortress | 14 | 183,874 | queued |
| 2026-11-13 15:24 | Divine Pulse | 14 | 183,874 | queued |
| 2026-11-13 15:24 | Raijin's Judgement | 14 | 106,628 | queued (queue was empty; active Ethereal Nexus 13 ends ~16:23; waiting Limit Breaker 14, Mental Fortress 14, Divine Pulse 14, Raijin 14; ends ~20:23). Pocket 8.63M, no withdrawal. 4,550 energy to willpower (+549.86, intelligence had passed willpower); asleep in 177 |
| 2026-11-13 16:22 | none | | 0 | queue already full (active Ethereal Nexus 13 ends ~16:23; waiting Limit Breaker 14, Mental Fortress 14, Divine Pulse 14, Raijin 14; ends ~20:23). Pocket 8.63M, no withdrawal. No training started, so the character stayed ASLEEP in 177; 5,050 energy left unspent rather than waking it |
| 2026-11-13 17:22 | Earth Armor | 14 | 106,628 | queued (queue had 3 waiting; now Mental Fortress 14, Divine Pulse 14, Raijin 14, Earth Armor 14; ends ~21:23). First Chakra Gate 14 refused, queue full. Pocket 8.53M, no withdrawal. 4,550 energy to willpower (+549.86, intelligence had passed willpower); asleep in 177 |
| 2026-11-13 18:23 | bank.toPocket 10,000,000 | | | pocket was 150,000 (down from 8.53M at 17:22; spent or moved outside this log), now 10,150,000 |
| 2026-11-13 18:24 | First Chakra Gate | 14 | 106,628 | queued (queue had 3 waiting; now Divine Pulse 14, Raijin 14, Earth Armor 14, FCG 14; ends ~22:23). Ryūsa Kōka 14 refused, queue full. Pocket 10.04M. 4,550 energy to willpower (+782.95, intelligence had passed willpower); asleep in 177 |
| 2026-11-13 19:23 | none | | 0 | not refilled: run lock held by an active content session ("598 Deck Warden Seven Planks back on", heartbeat 19:20, ~58 min left), so no live calls were made. Last known queue (18:24 log) ends ~22:23. No ryo, energy or sleep change |
| 2026-11-13 20:25 | bank.toPocket 10,000,000 | | | pocket was 150,616 (down again from 10.04M at 18:24; spent or moved outside this log), now 10,150,616 |
| 2026-11-13 20:26 | Ryūsa Kōka | 14 | 183,874 | queued |
| 2026-11-13 20:26 | Ethereal Nexus | 14 | 396,747 | queued |
| 2026-11-13 20:26 | Limit Breaker | 15 | 265,905 | queued (queue had 1 waiting; active Earth Armor 14 ends ~21:23; waiting FCG 14, Ryūsa Kōka 14, Ethereal Nexus 14, Limit Breaker 15; ends ~01:23). Pocket 9.30M. 4,550 energy to willpower (+549.86, intelligence had passed willpower); asleep in 177 |
| 2026-11-13 21:22 | none | | 0 | not refilled: run lock held by an active content session ("moe-fixes-1-3+hand-rerun", claimed 21:21, ~59 min left), so no live calls were made. Last known queue (20:26 log) ends ~01:23. No ryo, energy or sleep change |
| 2026-11-13 22:22 | none | | 0 | not refilled: run lock held by an active content session ("push/607_moe_etching_swap.json", ~20 min left), so no live calls were made. Last known queue (20:26 log) ends ~01:23. No ryo, energy or sleep change |
| 2026-11-13 23:22 | none | | 0 | not refilled: run lock held by release-thread ("Skyglass Nov 13 hidden prep + flips", claimed 22:34, ~72 min left), so no live calls were made. Last known queue (20:26 log) ends ~01:23. No ryo, energy or sleep change |
| 2026-11-14 00:24 | bank.toPocket 10,000,000 | | | pocket was 150,965, now 10,150,965 |
| 2026-11-14 00:24 | Raijin's Judgement | 15 | 151,673 | queued |
| 2026-11-14 00:24 | Earth Armor | 15 | 151,673 | queued |
| 2026-11-14 00:24 | First Chakra Gate | 15 | 151,673 | queued |
| 2026-11-14 00:25 | Mental Fortress | 15 | 265,905 | queued (active Limit Breaker 15 ends ~01:23; waiting Raijin 15, Earth Armor 15, FCG 15, Mental Fortress 15; ends ~05:23). Pocket 9.43M. Character was already AWAKE in sector 222 (not home, not in battle) when the run started, right after release-thread's "sweep + dauntless sleep" lock released: no stat training, not put to sleep; 5,050 energy unspent. Director notified |
| 2026-11-14 01:23 | bank.toPocket 10,000,000 | | | pocket was 152,212 (down from 9.43M at 00:25; spent or moved outside this log), now 10,152,212 |
| 2026-11-14 01:23 | none | | 0 | queue already full (active Limit Breaker 15 ending; waiting Raijin 15, Earth Armor 15, FCG 15, Mental Fortress 15; ends ~05:23). Character AWAKE in sector 210 (not home, not in battle): no stat training, not put to sleep; 5,050 energy unspent |
| 2026-11-14 02:22 | Divine Pulse | 15 | 265,905 | queued (queue had 3 waiting; now Earth Armor 15, FCG 15, Mental Fortress 15, Divine Pulse 15; ends ~07:23). Pocket 9.89M, no withdrawal. 4,550 energy to intelligence (+549.86); asleep in 177 |
| 2026-11-15 03:22 | none | | 0 | not refilled: TNR connector needed sign-in this run (server reported it requires authentication), so no live calls were made and the run lock was not claimed. Last known queue (2026-11-14 02:22 log) ended ~07:23 that day. No ryo, energy or sleep change |
| 2026-11-15 06:22 | none | | 0 | not refilled: TNR connector needed sign-in again this run (server reported it requires authentication), so no live calls were made and the run lock was not claimed. Second run in a row; queue state unknown (last known queue, 2026-11-14 02:22 log, ended ~07:23 that day). No ryo, energy or sleep change |
| 2026-11-15 07:23 | bank.toPocket 10,000,000 | | | pocket was 120,407, now 10,120,407 |
| 2026-11-15 07:23 | Ryūsa Kōka | 16 | 384,532 | started (queue was empty; last level had finished 2026-11-14 16:23). Levels 16 on Divine Pulse/Earth Armor/LB/FCG/MF and 15 on Ryūsa Kōka/Ethereal Nexus were reached outside this log |
| 2026-11-15 07:23 | Ethereal Nexus | 16 | 869,298 | queued |
| 2026-11-15 07:23 | Limit Breaker | 17 | 556,082 | queued |
| 2026-11-15 07:23 | Mental Fortress | 17 | 556,082 | queued |
| 2026-11-15 07:23 | Divine Pulse | 17 | 556,082 | queued (active Ryūsa Kōka 16 ends ~08:23; waiting Ethereal Nexus 16, Limit Breaker 17, Mental Fortress 17, Divine Pulse 17; ends ~12:23). Pocket 7.20M. 4,550 energy to intelligence (+817.78); asleep in 177 |
| 2026-11-15 08:24 | none | | 0 | queue already full (active Ethereal Nexus 16 ends ~09:23; waiting Limit Breaker 17, Mental Fortress 17, Divine Pulse 17; ends ~12:23); Earth Armor 17 refused ("queue is full"). Pocket 7.20M, no withdrawal. No training started, so the character stayed ASLEEP in 177; 5,050 energy left unspent rather than waking it |
| 2026-11-15 09:23 | Earth Armor | 17 | 306,887 | queued (queue had 3 waiting; active Ethereal Nexus 16 ending ~09:23; waiting Limit Breaker 17, Mental Fortress 17, Divine Pulse 17, Earth Armor 17; ends ~13:23). Pocket 6.89M, no withdrawal. 4,550 energy to intelligence (+574.32); asleep in 177 |
| 2026-11-15 10:23 | First Chakra Gate | 17 | 306,887 | queued (active Mental Fortress 17 ends ~11:23; waiting Divine Pulse 17, Earth Armor 17, First Chakra Gate 17; ends ~14:23); Ryūsa Kōka 17 refused ("queue is full"). Pocket 6.58M, no withdrawal. 4,550 energy to intelligence (+574.32); asleep in 177 |
| 2026-11-15 11:23 | Ryūsa Kōka | 17 | 556,082 | queued (active Divine Pulse 17 ending ~12:23; waiting Earth Armor 17, FCG 17, Ryūsa Kōka 17; ends ~15:23); Ethereal Nexus 17 refused ("queue is full"). Pocket 6.03M, no withdrawal. 4,550 energy to intelligence (+574.32); asleep in 177 |
| 2026-11-15 12:22 | Ethereal Nexus | 17 | 1,286,755 | queued (Divine Pulse 17 finished; queue now Earth Armor 17, FCG 17, Ryūsa Kōka 17, Ethereal Nexus 17; ends ~16:23). Pocket 4.74M, no withdrawal. 4,550 energy to willpower (+817.78, intelligence had passed willpower); asleep in 177 |
| 2026-11-15 16:22 | none | | 0 | not refilled: run lock held by player ("dauntless automated protector sweep (pilot thread)", ~35 min left), so no live calls were made. Last known queue (12:22 log) ends ~16:23. No ryo, energy or sleep change |
| 2026-11-15 17:22 | none | | 0 | not refilled: run lock held by player ("dauntless automated protector sweep (pilot thread)", ~35 min left), so no live calls were made. Last known queue (12:22 log) ended ~16:23. No ryo, energy or sleep change |
| 2026-11-15 18:23 | none | | 0 | not refilled: run lock held by player ("dauntless automated protector sweep (pilot thread)", ~35 min left), so no live calls were made. Last known queue (12:22 log) ended ~16:23. No ryo, energy or sleep change |
| 2026-11-15 19:22 | none | | 0 | not refilled: run lock held by player ("dauntless automated protector sweep (pilot thread)", claimed 12:51, heartbeat 19:12, ~35 min left), so no live calls were made. Last known queue (12:22 log) ended ~16:23. No ryo, energy or sleep change |
| 2026-11-15 20:22 | none | | 0 | not refilled: run lock held by player ("dauntless automated protector sweep (pilot thread)", claimed 12:51, ~36 min left), so no live calls were made. Last known queue (12:22 log) ended ~16:23. No ryo, energy or sleep change |
| 2026-11-15 21:22 | none | | 0 | not refilled: run lock held by player ("dauntless automated protector sweep (pilot thread)", claimed 12:51, ~36 min left), so no live calls were made. Last known queue (12:22 log) ended ~16:23. No ryo, energy or sleep change |
| 2026-11-15 22:23 | bank.toPocket 10,000,000 | | | pocket was 129,232, now 10,129,232 |
| 2026-11-15 22:24 | Limit Breaker | 19 | 1,162,924 | queued (queue had Mental Fortress 18 and Ethereal Nexus 18 only, both added outside this log; Limit Breaker 18 finished 22:23) |
| 2026-11-15 22:24 | Earth Armor | 19 | 620,939 | queued (active Mental Fortress 18 ends ~23:23; waiting Ethereal Nexus 18, Limit Breaker 19, Earth Armor 19; ends ~02:23); First Chakra Gate 19 refused ("queue is full"). Pocket 8.35M. 4,550 energy to willpower (+574.32, intelligence had passed willpower); asleep in 177 |
| 2026-11-15 23:24 | First Chakra Gate | 19 | 620,939 | queued (active Ethereal Nexus 18 ends ~00:23; waiting Limit Breaker 19, Earth Armor 19, FCG 19; ends ~03:23). Mental Fortress 18 finished 23:23. Pocket 7.72M, no withdrawal. 4,550 energy to willpower (+574.32, intelligence had passed willpower); asleep in 177 |
| 2026-11-16 00:22 | none | | 0 | not refilled: run lock held by player ("dauntless scout for human PvP targets (ping the director)", claimed 2026-11-15 23:50, ~13 min left), so no live calls were made. Last known queue (2026-11-15 23:24 log) ends ~03:23. No ryo, energy or sleep change |
| 2026-11-16 01:23 | bank.toPocket 10,000,000 | | | pocket was 146,697, now 10,146,697 |
| 2026-11-16 01:24 | Mental Fortress | 19 | 1,162,924 | queued |
| 2026-11-16 01:24 | Divine Pulse | 19 | 1,162,924 | queued (Limit Breaker 19 finished 01:23; active Earth Armor 19 ends ~02:23; waiting FCG 19, Mental Fortress 19, Divine Pulse 19; ends ~05:23). Pocket 7.82M. Character was already AWAKE in sector 1490 (not home, not in battle) when the run started, after the scout session's lock: no stat training, not put to sleep; 5,050 energy unspent. Director notified |
| 2026-11-16 02:23 | bank.toPocket 10,000,000 | | | pocket was 150,710, now 10,150,710 |
| 2026-11-16 02:24 | Raijin's Judgement | 19 | 620,939 | queued (Earth Armor 19 finished ~02:23; active FCG 19 ends ~03:23; waiting Mental Fortress 19, Divine Pulse 19, Raijin's Judgement 19; ends ~06:23); Ryūsa Kōka 19 refused ("queue is full"). Pocket 9.53M. 4,550 energy to willpower (+504.13, intelligence had passed willpower); asleep in 177 |
| 2026-11-16 03:23 | bank.toPocket 10,000,000 | | | pocket was 139,032, now 10,139,032 |
| 2026-11-16 03:24 | Ryūsa Kōka | 19 | 1,162,924 | queued (FCG 19 finished ~03:23; active Mental Fortress 19 ends ~04:23) |
| 2026-11-16 03:25 | Ethereal Nexus | 19 | 2,819,355 | queued (waiting Divine Pulse 19, Raijin's Judgement 19, Ryūsa Kōka 19, Ethereal Nexus 19; ends ~08:23). Pocket ~6.16M. 4,550 energy to willpower (+505.19, intelligence had passed willpower); asleep in 177 |
| 2026-11-16 04:24 | Earth Armor | 20 | 883,251 | queued (Mental Fortress 19 finished 04:23; active Divine Pulse 19 ends ~05:23; waiting Raijin's Judgement 19, Ryūsa Kōka 19, Ethereal Nexus 19, Earth Armor 20; ends ~09:23). Phantom Requiem 19 (S, ~7M) and Cyclone Palm Strike 19 (pending director) passed over as in earlier runs. Pocket 5.27M, no withdrawal. 4,550 energy to willpower (+505.19, intelligence had passed willpower); asleep in 177 |
| 2026-11-16 05:22 | none | | 0 | not refilled: run lock held by player ("PvP hunt (pilot)", ~13 min left), so no live calls were made. Last known queue (04:24 log) ends ~09:23. No ryo, energy or sleep change |
| 2026-11-16 06:23 | bank.toPocket 10,000,000 | | | pocket was 54,450, now 10,054,450 |
| 2026-11-16 06:24 | Raijin's Judgement | 20 | 883,251 | queued (Raijin's Judgement 19 finished 06:23; active Ryūsa Kōka 19 ends ~07:23; waiting Ethereal Nexus 19, Earth Armor 20, Raijin's Judgement 20; ends ~10:23); First Chakra Gate 20 refused ("queue is full"). Pocket 9.17M. 4,550 energy to willpower (+359.67, intelligence had passed willpower); asleep in 177 |
| 2026-11-16 07:24 | First Chakra Gate | 20 | 883,251 | queued |
| 2026-11-16 07:24 | Limit Breaker | 20 | 1,681,734 | queued (Ryūsa Kōka 19 finished 07:23; active Ethereal Nexus 19 ends ~08:23; waiting Earth Armor 20, Raijin's Judgement 20, FCG 20, Limit Breaker 20; ends ~12:23). Pocket 6.61M, no withdrawal. 4,550 energy to willpower (+359.67, intelligence had passed willpower); asleep in 177 |
| 2026-11-16 08:24 | none | | 0 | queue already full (Ethereal Nexus 19 finished 08:23; active Earth Armor 20 ends ~09:23; waiting Raijin's Judgement 20, FCG 20, Limit Breaker 20; ends ~12:23); Mental Fortress 20 refused ("queue is full"). Pocket 6.61M, no withdrawal. 4,550 energy to willpower (+252.60, intelligence had passed willpower); asleep in 177 |
| 2026-11-16 09:23 | Mental Fortress | 20 | 1,681,734 | queued (Earth Armor 20 finished 09:23; active Raijin's Judgement 20 ends ~10:23; waiting FCG 20, Limit Breaker 20, Mental Fortress 20; ends ~13:23); Divine Pulse 20 refused ("queue is full"). Pocket ~4.92M, no withdrawal. 4,550 energy to willpower (+252.60, intelligence had passed willpower); asleep in 177 |
| 2026-11-16 10:24 | Divine Pulse | 20 | 1,681,734 | queued (active First Chakra Gate 20 ends ~11:23; waiting Limit Breaker 20, Mental Fortress 20, Divine Pulse 20; ends ~14:23); Ryūsa Kōka 20 refused ("queue is full"). Pocket 3.24M, no withdrawal. 4,550 energy to willpower (+252.60, intelligence had passed willpower); asleep in 177 |
| 2026-11-16 11:24 | Ryūsa Kōka | 20 | 1,681,734 | queued (First Chakra Gate 20 finished ~11:23; active Limit Breaker 20 ends ~12:23; waiting Mental Fortress 20, Divine Pulse 20, Ryūsa Kōka 20; ends ~15:23) |
| 2026-11-16 11:25 | bank.toPocket 10,000,000 | | | pocket was 1,561,012, now 11,561,012. 4,550 energy to willpower (+252.60, intelligence had passed willpower); asleep in 177 |
| 2026-11-16 12:24 | Thunderbolt Fury | 20 | 883,251 | queued (Limit Breaker 20 finished ~12:23; active Mental Fortress 20 ends ~13:23; waiting Divine Pulse 20, Ryūsa Kōka 20, Thunderbolt Fury 20; ends ~16:23); Soul Laceration Mirage 20 refused ("queue is full"). Phantom Requiem 19 (S) and Cyclone Palm Strike 19 (pending director) passed over as in earlier runs. Pocket 10.68M, no withdrawal. 4,550 energy to willpower (+359.67, intelligence had passed willpower); asleep in 177 |
| 2026-11-16 13:24 | Soul Laceration Mirage | 20 | 1,892,774 | queued |
| 2026-11-16 13:24 | Ethereal Nexus | 20 | 4,173,274 | queued (Mental Fortress 20 finished ~13:23; active Divine Pulse 20 ends ~14:23; waiting Ryūsa Kōka 20, Thunderbolt Fury 20, Soul Laceration Mirage 20, Ethereal Nexus 20; ends ~18:23). All trainable targets now at or queued to 20 except Phantom Requiem 19 (S) and Cyclone Palm Strike 19 (pending director). Pocket 4.61M, no withdrawal. 4,550 energy to willpower (+359.67, intelligence had passed willpower); asleep in 177 |
| 2026-11-16 14:24 | none | | 0 | target list exhausted: Divine Pulse 20 finished ~14:23; active Ryūsa Kōka 20 ends ~15:23; waiting Thunderbolt Fury 20, Soul Laceration Mirage 20, Ethereal Nexus 20; queue runs dry ~18:23. Every target is at or queued to the level-20 cap except Phantom Requiem 19 (S) and Cyclone Palm Strike 19 (pending director), passed over as in earlier runs; director asked for new targets. Pocket 4.61M, no withdrawal. 4,550 energy to willpower (+252.60, intelligence had passed willpower); asleep in 177 |
| 2026-11-16 14:28 | Crescent Reaper Fang | 1 (learned at 0) | 1,615 | queued (new list 3: director asked for all Jonin None/Lightning/Earth jutsu next; active Ryūsa Kōka 20 ends ~15:23; waiting Thunderbolt Fury 20, Soul Laceration Mirage 20, Ethereal Nexus 20, Crescent Reaper Fang 1; ends ~18:25). Asleep in 177 |
| 2026-11-16 14:46 | transfer: Stone of the Withering -> Limit Breaker | 5 (Limit Breaker 20 -> 25, Stone 10 -> 5) | 0 | "Level transferred for 0 reputation points"; read back in getRecentTransfers. First daily transfer; Stone of the Withering is now the donor (train 6-10). Queue unchanged (full); asleep in 177 |
| 2026-11-16 16:24 | bank.toPocket 10,000,000 | | | pocket was 59,600, now 10,059,600. Stone of the Withering 6-7 refused: "You are in the hospital. Check out before taking this action." (character HOSPITALIZED in 177, not in battle; no hospital checkout paid, outside this job). Queue: active Soul Laceration Mirage 20 ends ~17:23; waiting Ethereal Nexus 20, Crescent Reaper Fang 1; runs dry ~18:25. No energy spent, no sleep toggle (hospitalized) |
| 2026-11-16 17:24 | none | | 0 | not refilled: character was AWAKE in 177 (no longer hospitalized) when the run started, then entered PvP battle yt-dCJL1VkF1VzMMuwu_C at ~17:23:44 (5,050 HP); Stone of the Withering 6-8 refused ("You are in battle"). The refill job doesn't fight or flee, so no stat training and no sleep; character left IN BATTLE in 177. Queue: active Ethereal Nexus 20 ends ~18:23; waiting Crescent Reaper Fang 1; runs dry ~18:25. Pocket 10.04M, no withdrawal. Director notified |
| 2026-11-16 18:25 | Stone of the Withering (donor) | 6-10 | 114,732 | started (queue was empty; Ethereal Nexus 20 and Crescent Reaper Fang 1 finished; active Stone 6 ends ~19:07; waiting Stone 7-10; ends ~22:53). Donor back to 10 then. Pocket 9.90M, no withdrawal. 4,550 energy to willpower (+359.67, intelligence had passed willpower); asleep in 177 |
| 2026-11-16 20:23 | bank.toPocket 10,000,000 | | | pocket was 100,000, now 10,100,000 |
| 2026-11-16 20:24 | Void Pulse Barrage | 1 (learned at 0) | 1,615 | queued (list 3, first not-owned entry; active Stone of the Withering 8 ends ~20:53; waiting Stone 9, Stone 10, Phantom Requiem 19 (4,469,942 ryo, queued outside this job), Void Pulse Barrage 1; ends ~23:54). Note: Chakra Overflow already owned at 25, nothing to train. Intelligence and willpower both answer "Already capped" (400,000), so 5,050 energy left unspent; asleep in 177. Pocket ~10.1M |
| 2026-11-16 21:23 | Summoning: Unholy Harvest | 1 (learned at 0) | 2,375 | queued (list 3, next not-owned entry; active Stone of the Withering 9 ends ~21:53; waiting Stone 10, Phantom Requiem 19, Void Pulse Barrage 1, Unholy Harvest 1; ends ~23:55). Pocket ~10.1M, no withdrawal. Intelligence and willpower both at the 400,000 cap, so 5,050 energy left unspent; asleep in 177 |
| 2026-11-16 22:23 | Shard Pulse Eruption | 1 (learned at 0) | 1,615 | queued (list 3, next not-owned entry; active Stone of the Withering 10 ends ~22:53; waiting Phantom Requiem 19, Void Pulse Barrage 1, Unholy Harvest 1, Shard Pulse Eruption 1; ends ~23:56). Pocket ~10.09M, no withdrawal. Intelligence and willpower both at the 400,000 cap, so 5,050 energy left unspent; asleep in 177 |
| 2026-11-16 23:23 | Sealing Technique: Lotus Barrier | 1 (learned at 0) | (cost not returned) | queued (list 3, next not-owned entry; active Phantom Requiem 19 ends ~23:53; waiting Void Pulse Barrage 1, Unholy Harvest 1, Shard Pulse Eruption 1, Lotus Barrier 1; ends ~23:57). Pocket ~10.09M, no withdrawal. Intelligence and willpower both at the 400,000 cap, so 5,050 energy left unspent; asleep in 177 |
| 2026-11-17 00:23 | Crescent Reaper Fang | 2 | 2,341 | started (queue was empty; all earlier levels finished, Stone of the Withering at donor cap 10) |
| 2026-11-17 00:23 | Void Pulse Barrage, Summoning: Unholy Harvest, Shard Pulse Eruption, Sealing Technique: Lotus Barrier | 2 each | 11,263 total | queued (active Crescent Reaper Fang 2 ends ~00:34; 4 waiting, ends ~01:18); Inferno Leech 3 refused ("queue is full"). Pocket 10.08M, no withdrawal. Intelligence and willpower both at the 400,000 cap, so 5,050 energy left unspent; asleep in 177 |
| 2026-11-17 01:24 | Summoning Poison Salamander | 1 (learned at 0) | 1,615 | started (queue was empty; list 3, next not-owned entry; finished ~01:25) |
| 2026-11-17 01:24 | Inferno Leech, Crescent Reaper Fang, Void Pulse Barrage, Summoning: Unholy Harvest | 3 each | 15,383 total | queued (4 waiting, ends ~02:49). Stone of the Withering already at donor cap 10. Pocket 10.06M, no withdrawal. Intelligence and willpower both at the 400,000 cap, so 5,050 energy left unspent. Note: the character was found ASLEEP after the queue calls, so the first sleep toggle woke it; toggled again and read back ASLEEP in 177 |
| 2026-11-17 05:23 | bank.toPocket 10,000,000 | | | pocket was 127,638, now 10,127,638 |
| 2026-11-17 05:24 | Earthquake Slam | 1 (learned at 0) | 1,092 | started (queue was empty; list 4, first not-owned entries at level 0 are quickest) |
| 2026-11-17 05:24 | Eight Fist Style: Earthen Grasp, Ganpaken, Stone Stomp, Tectonic Stomp | 1 each (learned at 0) | 4,368 total | queued (4 waiting, ends ~05:29); Earth Release: Earthquake 1 refused ("queue is full"). Stone of the Withering already at donor cap 10. Pocket 10.12M. Intelligence and willpower both at the 400,000 cap, so 5,050 energy left unspent; asleep in 177 (read back) |
| 2026-11-17 06:24 | Earth Release: Earthquake | 1 (learned at 0) | 1,045 | started (queue was empty; list 4, next not-owned entries at level 0 are quickest) |
| 2026-11-17 06:24 | Earth Release: Seven Heavenly Pillars, Gaia's Wrath, Graveyard of Stone, Mountain Crusher | 1 each (learned at 0) | 5,130 total | queued (4 waiting, ends ~06:29); Quaking Fist 1 refused ("queue is full"). Stone of the Withering already at donor cap 10. Pocket 10.12M, no withdrawal. Intelligence and willpower both at the 400,000 cap, so 5,050 energy left unspent; asleep in 177 (read back) |
| 2026-11-17 07:24 | Quaking Fist | 1 (learned at 0) | 1,520 | started (queue was empty; list 4, next not-owned entries at level 0 are quickest) |
| 2026-11-17 07:24 | Quicksand Trap, Stone Breaker, Stone Hammer Kick, Stone Warden | 1 each (learned at 0) | 6,080 total | queued (4 waiting, ends ~07:29). Stone of the Withering already at donor cap 10. Pocket 10.11M, no withdrawal. Intelligence and willpower both at the 400,000 cap, so 5,050 energy left unspent; asleep in 177 (read back) |
| 2026-11-17 08:23 | Stonebreaker Strike | 1 (learned at 0) | 1,520 | started (queue was empty; list 4, next not-owned entries at level 0 are quickest) |
| 2026-11-17 08:23 | Divine Thunder Slap, Eclipse Cyclone, Lightning Blitz Strike, Lightning Release: Raijin's Bow | 1 each (learned at 0) | 4,843 total | queued (4 waiting, ends ~08:28). Stone of the Withering already at donor cap 10. Pocket 10.10M, no withdrawal. Intelligence and willpower both at the 400,000 cap, so 5,050 energy left unspent; asleep in 177 (read back) |
| 2026-11-17 09:23 | Lightning Release: Spark Blade | 1 (learned at 0) | 1,092 | started (queue was empty; list 4, next not-owned entries at level 0 are quickest) |
| 2026-11-17 09:24 | Lightning Release: Stormcaller Whip, Lightning Release: Thunder Edge, Lightning Surge, Raijin Puncture | 1 each (learned at 0) | 4,368 total | queued (4 waiting, ends ~09:28). Stone of the Withering already at donor cap 10. Pocket 10.10M, no withdrawal. Intelligence and willpower both at the 400,000 cap, so 5,050 energy left unspent; asleep in 177 (read back) |
| 2026-11-17 10:23 | Retribution | 1 (learned at 0) | 1,092 | started (queue was empty; list 4, next not-owned entries at level 0 are quickest) |
| 2026-11-17 10:24 | Thunderbolt Fusillade, Arashi Ikari, Arcbound Vortex, Bolt of Terror | 1 each (learned at 0) | 5,652 total | queued (4 waiting, ends ~10:29). Stone of the Withering already at donor cap 10. Pocket 10.09M, no withdrawal. Intelligence and willpower both at the 400,000 cap, so 5,050 energy left unspent; asleep in 177 (read back) |
| 2026-11-17 11:23 | Electric Prison | 1 (learned at 0) | 1,520 | started (queue was empty; list 4, next not-owned entries at level 0 are quickest) |
| 2026-11-17 11:24 | Rai Yari, Rensa Kaminari, Storm Kick, Thunder Fist | 1 each (learned at 0) | 6,080 total | queued (4 waiting, ends ~11:28). Stone of the Withering already at donor cap 10. Pocket 10.08M, no withdrawal. Intelligence and willpower both at the 400,000 cap, so 5,050 energy left unspent; asleep in 177 (read back) |
| 2026-11-17 12:23 | Thunder Shockwave | 1 (learned at 0) | 1,520 | started (queue was empty; list 4, next not-owned entries at level 0 are quickest) |
| 2026-11-17 12:23 | Thunderbolt Spear, Thunderstorm Delusion, Thunderstrike Blade, Thunderstrike Punch | 1 each (learned at 0) | 6,080 total | queued (4 waiting, ends ~12:28). Stone of the Withering already at donor cap 10. Pocket 10.07M, no withdrawal. Intelligence and willpower both at the 400,000 cap, so 5,050 energy left unspent; asleep in 177 (read back) |
| 2026-11-17 13:24 | Volt Crash | 1 (learned at 0) | 1,520 | started (queue was empty; list 4, next not-owned entries at level 0 are quickest) |
| 2026-11-17 13:24 | Volt Jab Barrage, Volt Reaper, Iron Fist, Aqua Barrier | 1 each (learned at 0) | 5,747 total | queued (4 waiting, ends ~13:28). Stone of the Withering already at donor cap 10. Pocket 10.07M, no withdrawal. Intelligence and willpower both at the 400,000 cap, so 5,050 energy left unspent; asleep in 177 (read back) |
| 2026-11-17 14:23 | Cleansing Aura | 1 (learned at 0) | 1,567 | started (queue was empty; list 4, next not-owned entries at level 0 are quickest) |
| 2026-11-17 14:23 | Heaven's Blessing, Wind Dance, Bonecrusher Kick, Chakra Palm | 1 each (learned at 0) | 5,224 total | queued (4 waiting, ends ~14:27). Stone of the Withering already at donor cap 10. Pocket 10.06M, no withdrawal. Intelligence and willpower both at the 400,000 cap, so 5,050 energy left unspent; asleep in 177 (read back) |
| 2026-11-17 15:22 | Chakra Siphon | 1 (learned at 0) | 1,520 | started (queue was empty; list 4, next not-owned entries at level 0 are quickest) |
| 2026-11-17 15:23 | Dreamshell, Echoing Void, Force Wave, Illusionary Celestial Mirage | 1 each (learned at 0) | 7,030 total | queued (4 waiting, ends ~15:27). Stone of the Withering already at donor cap 10. Pocket 10.05M, no withdrawal. Intelligence and willpower both at the 400,000 cap, so 5,050 energy left unspent; asleep in 177 (read back) |
| 2026-11-17 16:23 | Lunar Descent | 1 (learned at 0) | 1,520 | started (queue was empty; list 4, next not-owned entries at level 0 are quickest) |
| 2026-11-17 16:24 | Mind Flay, Phantom Scythe, Resounding Crescendo, Rib Breaker | 1 each (learned at 0) | 6,745 total | queued (4 waiting, ends ~16:28). Stone of the Withering already at donor cap 10. Pocket 10.04M, no withdrawal. Intelligence and willpower both at the 400,000 cap, so 5,050 energy left unspent; asleep in 177 (read back) |
| 2026-11-17 17:24 | Senbon Sakura | 1 (learned at 0) | 570 | started (queue was empty; list 4, next not-owned entries at level 0 are quickest) |
| 2026-11-17 17:24 | Shattering Strike, Spectral Chain, Summoning: Lord Pengu, Swift Combination | 1 each (learned at 0) | 4,655 total | queued (4 waiting, ends ~17:29). Stone of the Withering already at donor cap 10. Pocket 10.04M, no withdrawal. Intelligence and willpower both at the 400,000 cap, so 5,050 energy left unspent; asleep in 177 (read back) |
| 2026-11-17 18:23 | Toxic Pool | 1 (learned at 0) | 1,520 | started (queue was empty; last not-owned list-4 entries) |
| 2026-11-17 18:24 | Weary Fists 1 (learned at 0); Netherblight, Rock Cleaver, Rending Slash 2 each | | 8,111 total | queued (4 waiting, ends ~18:52). All list-4 not-owned entries are now learned; next refills take owned level-1 targets to 2. Stone of the Withering already at donor cap 10. Pocket 10.03M, no withdrawal. Intelligence and willpower both at the 400,000 cap, so 5,050 energy left unspent; asleep in 177 (read back) |
| 2026-11-17 18:39 | Transfer Stone of the Withering -> Mental Fortress | 5 (MF 20-25; donor 10-5) | 0 | done, 0 reputation points, read back in getRecentTransfers; Stone of the Withering 6 queued (1 was waiting); asleep in 177 |
| 2026-11-17 19:23 | Stone of the Withering (donor) | 7-10 | 105,119 | queued (active Stone of the Withering 6 ends ~19:33; 4 waiting, ends ~23:19); donor back to cap 10 for the next daily transfer. Pocket 9.91M, no withdrawal. Intelligence and willpower both at the 400,000 cap, so 5,050 energy left unspent; asleep in 177 (read back) |
| 2026-11-17 20:24 | Stormguard Retaliation, Static Flicker | 2 each (from 1) | 4,394 total | queued behind Stone of the Withering 9-10 (4 waiting, ends ~23:37). Next refills keep taking owned level-1 targets to 2. Pocket 9.91M, no withdrawal. Intelligence and willpower both at the 400,000 cap, so 5,050 energy left unspent; asleep in 177 (read back) |
| 2026-11-17 21:25 | Chakra Enfeeblement | 2 (from 1) | 784 | queued behind Stone of the Withering 10, Stormguard Retaliation 2, Static Flicker 2 (4 waiting, ends ~23:46). Pocket 9.91M, no withdrawal. Intelligence and willpower both at the 400,000 cap, so 5,050 energy left unspent; asleep in 177 (read back) |
| 2026-11-17 22:24 | Boulder Barrage | 2 (from 1) | 784 | queued behind Stone of the Withering 10 (active, donor back to cap), Stormguard Retaliation 2, Static Flicker 2, Chakra Enfeeblement 2 (4 waiting, ends ~23:55). Pocket 9.91M, no withdrawal. Intelligence and willpower both at the 400,000 cap, so 5,050 energy left unspent; asleep in 177 (read back) |
