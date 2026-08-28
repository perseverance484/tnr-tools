> **STALE - archived 2026-08-28 (rollout Stage 1).** working copy is 32b_DATA_pool.json in skill data/; kit work via calc.py kit.
> Do not build from this file.

# 32_REGISTRY_shared_ai_pool.md - The shared AI jutsu pool

82 reusable combat records for AI kits. Reference by code. **Build from this before creating a one-off.**

## AP economy, read this first

A combat round is **100 action points**. Pool attacks cost **60**, stances cost **40**, consumable items cost **20 to 40**.
So one attack plus one stance is a full round, and two stances plus movement is an exhausted AI.
Only the self-target rows below cost 40, and only `S35 Second Wind` heals.
An AI built purely from attacks will run out of affordable actions and exhaust itself (law 61 to 63).

## Blocks

`S` generic strikes and stances · `A` area attacks · `B` boss tier · `E` elemental (EA air, EE earth, EF fire, EL lightning, EW water)

Skipped codes (`B25`, `S05`, `S09` to `S26`, `S37`) are reserved numbering, not missing records.


## A · area

| code | name | target | cd | AP | effects | id |
|---|---|---|---|---|---|---|
| `A1` | Cleaving Line | r4 | 4 | 60 | damage 50 | `brzGw6WgHsrFPkL9JWGir` |
| `A2` | Shattering Ring | r3 | 4 | 60 | damage 50 | `muGmYnLm8mWFrwoU4zsOE` |
| `A3` | Erupting Ground | r3 | 5 | 60 | damage 55 | `jBRyl7F4UjTyxG5nnzLqj` |

## B · boss tier

| code | name | target | cd | AP | effects | id |
|---|---|---|---|---|---|---|
| `B01` | Cataclysm Fist | r5 | 8 | 60 | damage 70 | `I66lzvVHf8v4thxR6tEJn` |
| `B02` | Annihilating Wave | r5 | 8 | 60 | damage 70 | `ZvPl6uyJfwF5EjmLHouQR` |
| `B03` | Sovereign Undertow | r5 | 6 | 60 | redirection 3 | `nOYLPmN3TXj6wEe_oE6HQ` |
| `B04` | Executioner Seal | r5 | 12 | 60 | onehitkill 100 | `tRwJPlTZK9YSUV_0AacID` |
| `B05` | Devouring Grasp | r5 | 6 | 60 | damage 60, drain 25/2r | `lft52q7DE_JjhR7PKXimB` |
| `B06` | Split Image | ground | 6 | 60 | clone 100/3r | `LQ26G2ANWkbTRL7Ry__F0` |
| `B07` | Stolen Form | r4 | 6 | 60 | copy 100/3r | `VuFuBtE7h5B1nnA2J1lFZ` |
| `B08` | Tempo Fracture | r4 | 8 | 60 | timecompression 100/2r | `ecRoSDPCDjO7zH-VBaFyY` |
| `B09` | Veilstep | self | 6 | 40 | stealth 100/2r | `IBjVpLutojh3m9PRnIce-` |
| `B10` | Sovereign Ascendance | self | 10 | 40 | increasedamagegiven 60/3r, increasedamagegiven 60/3r, decreasedamagetaken 60/3r | `yDznlfsnPaOSFtdjfCyTZ` |
| `B11` | Sovereign Malediction | r4 | 10 | 60 | seal 100/2r, increasedamagetaken 60/3r, afterburn 60/3r | `pJXJUSvq2kZU-tmgC12FL` |
| `B12` | Sovereign Ruin | r4 | 10 | 60 | decreasedamagegiven 60/3r, decreasedamagegiven 60/3r, decreaseheal 60/3r | `-M_BxzqB937XCdD1IMWW0` |
| `B13` | Hexweave | r4 | 8 | 60 | damage 40, increasedamagetaken 40/3r, decreaseheal 60/3r, decreasestat 15/3r | `_JRHgRL8pfUvt_-q1Xa3H` |
| `B14` | Cataclysm Detonation | r5 | 8 | 60 | damage 85 | `o-4SCAhJ4LHdCwcBDgJrV` |
| `B15` | Feast of Marrow | r5 | 8 | 60 | damage 50, drain 100/2r | `ubwtVj1o9q6VQ6VxOczxt` |
| `B16` | Sovereign Fetters | r5 | 10 | 60 | damage 60, stun 100/2r, seal 100/2r | `RPdeeWhFI5AIUUpJXwUlf` |
| `B17` | Worldbreaker Chorus | r5 | 10 | 60 | damage 70, stun 100/2r | `LisNuMJ2gncEByAxG6QPI` |
| `B18` | Apex Hunger | self | 6 | 40 | increasedamagegiven 60/99r, increasestat 25/99r | `w4F7-w5ubgKsqYPBPvRuV` |
| `B19` | Warrior's Poise | self | 5 | 40 | increasedamagegiven 30/3r, decreasedamagetaken 30/3r | `taxbZNdm1Q7YL5AxaRssW` |
| `B20` | Surging Overflow | self | 5 | 40 | increasedamagegiven 30/3r, increasestat 25/3r | `AicYoMMpZmHAykb_5hYtY` |
| `B21` | Hushed Hours | self | 5 | 40 | absorb 20/3r, increasedamagegiven 25/3r | `cZrZDI-A4fL324nX1CGss` |
| `B22` | Compression Barrier | self | 5 | 40 | absorb 20/3r, decreasedamagetaken 25/3r | `6UE5jC71Y6nRjobkJ-UTV` |
| `B23` | Bulwark Charge | self | 6 | 40 | increasedamagegiven 25/3r, shield 100/2r | `S_ix-gZcXi6RirSVpSLV0` |
| `B24` | Veilstrike | self | 8 | 40 | stealth 100/1r, increasedamagegiven 60/3r, decreasedamagetaken 50/3r, heal 25 | `yOgwN1WGkwNL9qMImc9aY` |
| `B26` | Braced Strike | r5 | 5 | 60 | damage 55, decreasedamagetaken 30/2r | `WvLCyGsPCKSDYl6-e_D9o` |
| `B27` | Scorching Rend | r5 | 6 | 60 | damage 55, wound 15/2r, afterburn 25/2r | `Uou0sCjZ1rwiMJZ-JWEI_` |
| `B28` | Recoil Slam | r5 | 5 | 60 | damage 75, recoil 15 | `ElSK-RCrLjddEUm76FZrs` |
| `B29` | Devouring Wave | r5 | 6 | 60 | damage 55, absorb 15/2r | `-45phqE2baTGC--lNSEx9` |
| `B30` | Suppressing Roar | r5 | 8 | 60 | damage 45, decreasedamagegiven 30/2r, stun 100/1r | `vWaGTnYOwiTiaMQW10y6A` |
| `B31` | Rallying Spiral | r3 | 8 | 40 | decreasedamagetaken 25/3r, increasedamagegiven 25/3r | `tq_kaS3nJ4Rv4hDRRJJ6p` |
| `B32` | Nullifying Wave | r5 | 8 | 60 | clear 100 | `JWZYiHKPNwYziWEFjw4Fn` |
| `B33` | Piercing Judgment | r5 | 7 | 60 | pierce 55, increasedamagetaken 25/2r | `OyswJoalfNpmz7FsA8Hd8` |
| `B34` | Mirror Edge | r5 | 5 | 60 | damage 50, reflect 30/2r | `AEeRf7i9215twJ_iEugZT` |
| `B35` | Reaping Strike | r5 | 5 | 60 | damage 50, heal 15 | `fuPRuLJ0vcBqSjrqdMi7o` |
| `B36` | Withering Weave | r4 | 5 | 60 | damage 30, increasedamagetaken 15/2r, decreaseheal 20/2r | `-kMekZ4rR64vjMF2Jc4pe` |
| `B37` | Fighter's Poise | self | 4 | 40 | increasedamagegiven 15/2r, decreasedamagetaken 15/2r | `P0GcazZ6yvULoH4kGuh4T` |
| `B38` | Minor Overflow | self | 4 | 40 | increasedamagegiven 15/2r, increasestat 12/2r | `oQo27NtvRS29CABHGXP94` |
| `B39` | Light Barrier | self | 5 | 40 | shield 100/2r | `05rH3kZNXbtFq9a9iRl-W` |

## E · elemental

| code | name | target | cd | AP | effects | id |
|---|---|---|---|---|---|---|
| `EA01` | Gale Bolt | r5 | 3 | 60 | damage 45 | `SJwW0b5tO4PuBhNrLJIR2` |
| `EA02` | Tempest Breaker | r3 | 5 | 60 | damage 60, redirection 3 | `d00wewEL2x6V3Th5gS0dh` |
| `EA03` | Windlash Focus | self | 4 | 40 | increasedamagegiven 20/2r | `_9k7kSYUgMtB-AEFgRly5` |
| `EA04` | Zephyr Lance | r5 | 6 | 60 | pierce 60 | `A5HrHSzx4J3WM4Fln8Lbf` |
| `EE01` | Shale Bolt | r5 | 3 | 60 | damage 45 | `qymEx2jhCwmSZPJOnPuRD` |
| `EE02` | Bedrock Breaker | r3 | 5 | 60 | damage 60, moveprevent 100/2r, stun 100/1r | `0qhjpBMtG9HSWoOWztAB1` |
| `EE03` | Stoneward | self | 4 | 40 | decreasedamagetaken 20/2r | `V3WrfQ3pB-eCq2hojsxWe` |
| `EF01` | Cinder Bolt | r5 | 3 | 60 | damage 45 | `Sic286tbCpCjwaic0EX5q` |
| `EF02` | Pyre Breaker | r3 | 5 | 60 | damage 60, wound 15/2r | `EJOCWmrrUnECI2MikM8ho` |
| `EF03` | Emberwake | r5 | 4 | 60 | damage 40, afterburn 20/2r | `bLBu130QaqCaDlSIcEmUD` |
| `EL01` | Arc Bolt | r5 | 3 | 60 | damage 45 | `Fkfa_oRbCPPOnBPPHlikF` |
| `EL02` | Storm Breaker Volt | r3 | 5 | 60 | damage 60, reflect 20/2r | `hxNWprk1AYwH0OVX0rxaR` |
| `EL03` | Static Jolt | r5 | 4 | 60 | damage 40, stun 100/1r | `3hMzYwiV8VOEx2XOm1CJe` |
| `EL04` | Ion Lance | r5 | 6 | 60 | pierce 60 | `xGVqWSX93hXZgfmlKZODp` |
| `EW01` | Tide Bolt | r5 | 3 | 60 | damage 45 | `UnQKfwq_JoRVu10aTX6Uv` |
| `EW02` | Deluge Breaker | r3 | 5 | 60 | damage 60, shield 100/2r | `UAgYZvo_7DUtmBsBAaAar` |
| `EW03` | Springguard | self | 4 | 40 | absorb 20/2r | `mOA1hXNf4CcuwOhnnN7ZK` |

## S · generic

| code | name | target | cd | AP | effects | id |
|---|---|---|---|---|---|---|
| `S01` | Heavy Strike | r3 | 5 | 60 | damage 60 | `pUrUJX8Jml7fUIBXKsPwv` |
| `S02` | Quick Strike | r3 | 3 | 60 | damage 45 | `FeYnH7BBw_usnc1K-TM-J` |
| `S03` | Lunging Strike | r4 | 4 | 60 | damage 45 | `_nUaGHlWhn3-U0xbxJHFw` |
| `S04` | Opening Strike | r4 | 3 | 60 | damage 40, increasedamagetaken 15/2r | `Cw51Wm_Uy0GiIkiEjlQtn` |
| `S06` | Twin Shot | r5 | 3 | 60 | damage 45 | `3v9c1SHlD2GLPF2HW1_Sc` |
| `S07` | Rapid Fire | r5 | 2 | 60 | damage 40 | `Nrxc8m9utE9qaD_gWpLgf` |
| `S08` | Numbing Shot | r5 | 4 | 60 | damage 40, stun 30/1r | `m-ur3A8TS8r5jGb84L9x7` |
| `S27` | Weakening Strike | r5 | 4 | 60 | damage 40, decreasedamagegiven 20/2r | `YiRdVytsdxFzZtqkEDs5Q` |
| `S28` | Enervating Strike | r5 | 4 | 60 | damage 40, decreasestat 15/2r | `mpHuTrJX7EonpuW_jBunt` |
| `S29` | Venom Strike | r5 | 5 | 60 | damage 40, poison 20/2r | `LiVOnYq6qHzjB0XkIIA2e` |
| `S30` | Searing Strike | r5 | 4 | 60 | damage 40, afterburn 20/2r | `OWAm8o12bkZUMAAHLoGLz` |
| `S31` | Unraveling Strike | r3 | 5 | 60 | damage 40, clear 100 | `1OhP0StX4VTsosWtCxhsG` |
| `S32` | Lingering Strike | r5 | 4 | 60 | damage 40, cleanseprevent 100/2r | `YD9GEwXU6LDuIC06TGzWG` |
| `S33` | Marking Volley | r5 | 5 | 60 | damage 50, increasedamagetaken 15/2r | `mQ7-q8q46ry5njNVBFpGp` |
| `S34` | Purging Stance | self | 5 | 40 | cleanse 100 | `HcAs8gBtvopPZkjP8HCC2` |
| `S35` | Second Wind | self | 6 | 40 | heal 15 | `STu1VHNcfgeC3x-UiQDgt` |
| `S36` | Warding Stance | self | 5 | 40 | debuffprevent 100/2r | `hh-FMFv67CAL10DA35K2T` |
| `S38` | Glancing Strike | r5 | 3 | 60 | damage 12 | `u7AMx4nbPsU_ev8mfi5yG` |
| `S39` | Bruising Blow | r5 | 4 | 60 | damage 25 | `Rufs-Y-FZIDooXO7g6k0F` |
| `S40` | Measured Strike | r5 | 3 | 60 | damage 20 | `kkGDat1XWUxhOQ1_T5025` |
| `S41` | Steady Strike | r5 | 3 | 60 | damage 30 | `fKvCGRgzGNskgFWocQCAg` |
| `S42` | Forceful Strike | r5 | 3 | 60 | damage 40 | `4TM6iS8P0qgNHsFpALFhg` |
| `S43` | Heavy Cut | r5 | 4 | 60 | damage 45 | `Vo8N1luCT0p48y7JzKe84` |
| `S44` | Sundering Blow | r5 | 4 | 60 | damage 50 | `b7ZOgdZmhZiUbCVrmQiwH` |

## Notes

- `B04 Executioner Seal` is a one-hit-kill on a 12 cooldown. Use deliberately.
- `B18 Apex Hunger` runs 99 rounds, effectively permanent once cast.
- `S38` to `S44` are a clean damage ladder (12, 25, 20, 30, 40, 45, 50) for scaling a creature's basic attack to its tier without touching effects.
- Editing a pool record that is equipped on an AI severs the combat link. Sequence is unequip, edit, re-equip (law 60).
- A pool record can be silently reduced to a blank shell named `New Jutsu - <id>`; the id survives so nothing flags it (law 59).
