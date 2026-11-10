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

## Cost (libs/train.ts calcJutsuTrainCost)
base (D 50, C 100, B 150, A 200, S 250, + extraBaseCost) ^ (1 + level/20). Low levels are cheap; high levels are
very expensive (Cyclone Palm Strike level 19 quoted 1,949,575 ryo for one level; cancelled pending director).

## Queue log
| Started (UTC) | Jutsu | Levels | Ryo | Result |
|---|---|---|---|---|
| 2026-11-10 04:11 | Ethereal Rebirth | 8-12 | 479,594 | 9-12 cancelled and refunded (no scaling); level 8 left to finish ~05:11 |
| 2026-11-10 04:20 | Cyclone Palm Strike | 19 | 1,949,575 | cancelled and refunded; waiting for the director's picks |
