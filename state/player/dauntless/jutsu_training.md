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

## Jutsu of interest (equipped PvP loadout below level 25)
| Jutsu | Id | Level | Why |
|---|---|---|---|
| Ethereal Rebirth | K0t6Z-Q4lau1jFt8Tkpot | 7 -> 12 queued | main cash-out hit (2,234 buffed at lv7) |
| Eclipse Drain | ou7VyChQ-SFCm8T8yGS7I | 7 | ramp buff + lifesteal |
| Thunder's Judgement | qNeccb2eF20oL0Ws-VhKS | 7 | ramp buff + reflect |
| Shrapnel Clone Barrage | GiKpip6NxsC8QWlZi6l_R | 1 | opener hit + afterburn |
| Parry | 73Sn-ihCNNRwxZ_G_2lTZ | 1 | buff + parry |
Owned, top-player picks, not equipped: Dragon King's Impact, Chakra Invigoration, Eternity Flux, Chakra Resonance (all 25).

## Queue log
| Started (UTC) | Jutsu | Levels | Ryo | Done |
|---|---|---|---|---|
| 2026-11-10 04:11 | Ethereal Rebirth | 8-12 | 479,594 | ~09:11 |

## Next
When slots open: Shrapnel and Parry 1 -> 6 (cheap), then Eclipse and Thunder's 7 -> 12, then Ethereal 13+.
