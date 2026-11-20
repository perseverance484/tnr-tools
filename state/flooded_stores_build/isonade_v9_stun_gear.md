# Isonade v9: stun guard on worn gear (HIDDEN, job 669)

The director (2026-11-20, relayed): seals stay as they are, armour pause included ("Leave it as is"), and "Stun
immunity should be granted". Then: "Stun immunity that cant be sealed would require an equipped item." Hull stays at
70% ("Keep 70% as is if players are still dealing 1500-3k hits thats acceptable").

## Source (engine pin 3314d122)

- AI record effects are realised as fromType "bloodline" (combat.ts 4117-4136). A resolved seal on the target
  switches off bloodline effects (isEffectEnabled, util.ts 1320-1336), so Black Water's own seal, or a player's,
  opened a stun window.
- Equipped ARMOR, ACCESSORY and KEYSTONE effects are realised as fromType "armor", "accessory" and "keystone", for
  AI too (combat.ts 4243-4275; AI gear keeps character-level scaling). A seal only affects "bloodline".
- Clear and Cleanse skip those source types (persistentEffectSourceTypes, tags.ts 1235), so no player can strip it.
- The AI edit inserts new item rows equipped "CHEST" (queries/profile.ts 1849-1861); "number" is the drop chance (0).
- Armour loses durability only on a lost war-torn battle, so the guard does not wear off.
- The Forge AI merge keeps live items on later AI edits (recipes.mjs mergeAi). An AI edit sent by hand without
  `items` would delete it (profile.ts: newItemIds = input.data.items ?? []).

## Sim (isonade_v9.ts, 12 seeds, perfect read, player stuns every 4 rounds; isonade_v9_sim/summary.txt)

| Variant | Stuns tried / landed per fight |
|---|---|
| live v8 (record guard), stun only | 5.1 / 0.4 (lands only while Isonade is sealed) |
| live v8, seal + stun | 3.7 / 3.7 (every stun lands; the player wins 100%) |
| no guard, stun only | 5 / 5 (stand-in check) |
| gear guard only, stun / seal + stun / seal + stun + Clear | 0 landed in all three |
| gear guard + record guard, seal + stun | 0 |

With no stuns, the gear guard changes nothing (75% win, 16 rounds, 39.3% HP, same as v8).

## Build (job 669-mwo9wsjw, DONE 2/2, bundle harvests/inbox/tnr_results_1795136537887.json)

- Item `ZBfu0h3K6U1g45Q4gTOG7` "Isonade's Old Hull": hidden ARMOR, CHEST, stunprevent 100 (99 rounds), not tradeable,
  not in shop, no bloodline. Stays hidden: it is boss gear, never a player item.
- Isonade: item equipped CHEST, durability 100, drop chance 0. 18/18 jutsu still equipped; rules untouched. The
  record's own stunprevent stays as a second guard.
- Read-back: `state/stolen_stores_captures/isonade_v8_live_2026-11-20/post669_getAi_isonade.json`.

Not tested live: dauntless has no stun or seal source in its kit, and is below full HP with no Full Potions.
