# Godstorm processed art — the files push/53 binds

These are the eight **processed** `.webp` deliverables the Godstorm repair uploads, supplied by
dauntless as an approved set. They are the assets manifest 49
(`push/49_godstorm_two_pyramid_final_update.json`, staged at `bad3a2d9`) ledgered, and
`push/53_godstorm_failed_items_repair.json` replays the subset of 49's writes that did not land, so
it binds the same eight files with the same byte counts.

They are committed here so a manifest can bind them by **content**: `push/53`'s `imagePack` names
each one by repository path, the commit that holds it, and its SHA-256, and Forge refuses to upload
any of them unless the digest it computes matches (`forge/src/runner/imgpack.mjs`).

Do **not** substitute the unprocessed originals. `chatgpt/godstorm-source-art-pack` and
`chatgpt/godstorm-art-recovery` hold lime-key master PNGs and a different set of backgrounds;
push/53's `_note` explicitly forbids them, and the byte ledger would refuse them anyway. The
1.7 MB master that rode into a live run behind a 207 KB filename is exactly what this binding exists
to prevent (`harvests/inbox/tnr_results_1789829183863.json`, items 3-7).

Verified on receipt: all eight filenames and byte counts match push/53's `imgSizes`; the SHA-256 of
each matches the digest list shipped alongside them; all are valid WebP containers under the
524,288-byte `imageUploader` presign ceiling.

| file | bytes | dimensions |
|---|---|---|
| `bg_godstorm_stormcourt_upper_court.webp` | 379,928 | 1536x1024 |
| `bg_godstorm_stormcourt_binding_dais_active.webp` | 283,000 | 1536x1024 |
| `bg_godstorm_stormcourt_binding_dais_released.webp` | 256,826 | 1536x1024 |
| `ai_godstorm_marrow_warden_of_the_first_dark.webp` | 238,510 | 1490x1490 |
| `ai_godstorm_marrow_starless_monk.webp` | 207,410 | 1477x1477 |
| `ai_godstorm_marrow_hollow_lantern.webp` | 196,056 | 1476x1476 |
| `ai_godstorm_marrow_umbral_reaver.webp` | 161,650 | 1492x1492 |
| `ai_godstorm_marrow_nightveil_sentinel.webp` | 115,618 | 1429x1429 |

Regenerate the pack after any change here (the digests move with the bytes):

```sh
node forge/tools/make_image_pack.mjs push/53_godstorm_failed_items_repair.json \
     --root art/godstorm --ref HEAD --write
```
