# Job 630: re-cut strips for Rengoku Rō and Fury of The White Tiger (Duet)

Director, 2026-11-17: the review desk preview drew Rengoku Rō's animations as black boxes; "update your prompt
appropriately to fix". This is the run's contract; CLAUDE.md and the Forge/engine laws still govern.

**Cause.** Strips on the director's own UploadThing (`bbenpyo9uu.ufs.sh`) are not Bunny hosts, so the game loads them
at native size. A battle clip is one texture, and combat effects have no MAX_TEXTURE_SIZE guard; phones cap textures
at about 4096 px, so taller strips draw black. Live and affected: Rengoku strike 300 × 6900, smoulder 300 × 10500;
White Tiger gates 234 × 6786, tiger 252 × 10080 (627 ran before the re-cut landed).

**Rule from now on.** Every battle strip is ≤ 4096 px tall (frame px × frames). Never upload a taller strip.

**Fix.** Four strips re-cut by `art/duelyst_fx/recut_4096.py` (same frames and timing, fresh filenames), listed in
`state/recut_upload/upload_list.json`. Job 630 repoints the four live assets at them by direct edit. Asset ids do
not change, so both pending suggestions (Rengoku `96rmM8V6Qj2Ksq6s40e31` and the 629 White Tiger one) stay valid.

| asset | id | new strip | frames × ms |
|---|---|---|---|
| Rengoku Ro - Purgatory Prison | `nAUh6EdgIUrPwLeyaeTPB` | anim_rengoku_strike_tight_178_c.webp (4094 px) | 23 × 70 |
| Rengoku Ro - Smoulder | `cMax_mQ9G8TGmWBB-DcVR` | anim_rengoku_smoulder_tight_116_c.webp (4060 px) | 35 × 70 |
| Fury of The White Tiger - Gates | `92C_BYjulGUsL1y1X49Ee` | anim_white_tiger_gates_140.webp (4060 px) | 29 × 70 |
| Fury of The White Tiger - Tiger | `A7JDFeATf0DL-Sdv_6ssF` | anim_white_tiger_tiger_102.webp (4080 px) | 40 × 80 |

## Steps

1. Pull `perseverance484/tnr-tools` (main). Push your 627-629 results to main first if they are not there yet.
   Claim the run lock: `node forge/tools/run_lock.mjs claim --holder duet --job "630 strip re-cut" --ttl 30 --wait`.
2. Upload the four files in `state/recut_upload/upload_list.json` to the director's UploadThing with the same
   one-off workflow you used for Rengoku (your own task branch; sha-check each file). Commit the results to main as
   `state/recut_upload/uploaded.json` (same shape as `state/rengoku_upload/uploaded.json`, keyed by srcId).
3. `python3 push/630_strip_recut.gen.py` (refuses on a sha mismatch or a strip over 4096 px), then
   `validate.py push/630_strip_recut.json` (0/0). Run it over the connector: 4 direct `gameAsset` edits.
4. Read all four back with `gameAsset.get`: image = the new URL, frames and speed as in the table, hidden false.
5. Commit the results bundle to `harvests/inbox/`, release the lock, and set `state/run_queue.json` row 630 done
   (bundle path, read-back) in the same commit.

## Stop and report instead of improvising if

- an upload fails or a sha does not match;
- any edit fails or a read-back differs from the table.

## Not in scope

No jutsu edits, no suggestion changes, no AI re-equip, no other assets. Do not delete the old uploads.
