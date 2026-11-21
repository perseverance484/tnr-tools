# Sector 335 resource caches: live run (2026-11-21)

All five caches created as CONSUMABLE weighted caches with UploadThing icons, verified, then unhidden.

| Cache | Live id | Silo chance |
|---|---|---|
| Frontline War Cache | DHVuX_BxUEDqcOaHZLRUc | 100 |
| Bloodcore Cache | Fr4NDgv7talLrBh_uRAbR | 20 |
| War Chest | mqrTLPZ4mM2wdLZ2b5vgp | 6 |
| Conqueror's Stockpile | c4LmQmD_U_M1aJTYRFHXx | 4 |
| Warlord's Hoard | vxpn02wvCP0nqJDCkHQ7d | 2 |

Silo "war-torn" saved at ~01:43Z with 8 entries (kept: S-Rank Dungeons Level 100 at 5, Quartermaster's Reserve at 2, Genin Supply Package at 50). Read back with resourceSilos.getEditor: all 8 kinds, ids and chances match.

Notes:
- Job 1 (A) failed on a malformed answer file before any create; job 2 (A2) edited the blank shell left by the create into Frontline and created the other four. Its capture step paused on unresolved @item refs; every write was already verified by item.get.
- Job B (unhide) finished DONE, 5 VERIFIED: harvests/inbox/tnr_results_1795225332418.json.
- Run lock released (main 06d7c4c3).

## Tradeable (2026-11-21 ~14:39Z)
On the director's request, canBeTraded set true on all five caches (each update diff: canBeTraded only). Read back: all five canBeTraded true, still unhidden, icons unchanged. Silo not touched.
