# Isonade v11 live test 2 (2026-11-20, battle PR9BqStMNtxR7fxqKpTbp)

Hidden quest "Isonade Test" (nzETMobtvoP_rZnTuIJLH), dauntless solo with pet, PvE kit plus
Dr. Kim's Miracle Potion and Danse Macabre at the director's request. Full log:
`/mnt/project-files/tnr/battle-logs/2026-11-20_isonade_v11_win_PR9BqStM.json`.

**Result: WIN in round 12, dauntless 2,136 / 5,050 HP left.** Pet died R2 (Arm Lash 2,020).

## Round by round

| R | dauntless | Isonade |
|---|---|---|
| 1 | Dragon's Tomb 370 | Barnacle Hide (1500 shield, 25% DR), Arm rises |
| 2 | Forgotten Ember Blade (all into shield) | Tide Draws Back (+100% dmg given) |
| 3 | Clear (wiped Tide), Chakra Ignition Strike | Breaker 2,349 on me (775 absorbed), weakness for R4 |
| 4 | Forbidden Chakra Fury 1,594 (+1,915 Arm), Chakra Shield | Harpoon 884 pierce |
| 5 | Severed Pulse, Stormguard Aura | Brine Brand |
| 6 | Cleanse | Undertow 342 after 800 shield (456 recoil back) |
| 7 | Dr. Kim's Miracle (clear/debuff prevent active R8), move | Omen: Black Water |
| 8 | Heaven Bows, Eclipse Drain, Chakra Pill | Black Water Floods (weakness R9) **and Silt Cloud** (-40% dmg taken R9). No Scour. |
| 9 | Move, Danse Macabre 3,026 (+3,436 Arm), Kunai 1,664 | Omen: The Deep (4,000 shield, 80% DR, 1 rd), new Arm |
| 10 | Captain's Decree 156 and Shrapnel 280, both into shield | The Deep Crashes 3,133 on me, self-cleanse |
| 11 | Dragon's Tomb 407, Chakra Ignition Strike | Hold Floods 379 pierce, Swell Builds |
| 12 | Elite Smoke Bomb, Ethereal Rebirth 2,566 (kill) | - |

## Findings

- Scour never fired. Isonade used Silt Cloud in R8 instead, so clear prevent had nothing to block:
  the clear-prevent-vs-Scour question is untested and no re-sim condition was met.
- Danse Macabre applied no seal: its effects were a ground decreasedamagegiven mark and damage.
- All three Black Water crates are 5 hexes from Isonade, out of range-4 jutsu, so the round after
  Black Water opens with a move.
- Clear used on R3 (Tide) was still on cooldown at The Deep crash in R10, so the crash landed.
- The Deep's 4,000 shield ate the whole R10 follow-up (Decree and Shrapnel).
- Full Potion was refused in battle twice (R6, R7); cause not found.
