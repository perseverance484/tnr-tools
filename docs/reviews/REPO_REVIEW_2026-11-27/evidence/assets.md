# Assets & repo size audit (main@f0b5f0f, 2026-11-27, read-only)

Method: `git ls-files` + stat of every tracked file (7,956 files, 1,234 MB checkout);
role classifier by path segment/extension (scratchpad/classify.py); reference scan of every
tracked text file for image filenames (scratchpad/refs.txt); `git rev-list --objects --all |
git cat-file --batch-check` for history blobs (scratchpad/blobs.txt). Clone is shallow
(since 2026-08-01), so history numbers are a lower bound. GitHub API reports repo size
1,400,949 KB and visibility **public**.

## 1. Totals
- Checkout tracked: 1,234 MB. `.git` pack 1.39 GiB. Reachable blobs (disk): 1,369 MB, of which
  998 MB are in HEAD and 372 MB history-only (docs/design 172, dist/*.zip 46 across 189 versions,
  art/jutsu_icons 41, art/consumables_upgrade 25, state/moe_upload 23).
- Blobs reachable only from non-main branches: 85 MB (art/consumables_upgrade 25, state/moe_upload 23).
- By extension: .png 618 MB (1,013), .gif 288 MB (70), .json 190 MB (1,776), .webp 78 MB (3,187),
  .mp4 19.5 MB (13), .zip 9.7 MB (13).
- Files >5 MB: 17 (all allowlisted). >2 MB: 113 files / 456 MB. >1 MB: 384 / 851 MB. >512 KB: 548.

## 2. By role (all tracked)
| role | MB | files |
|---|---|---|
| raw-source (raw/raws/refs/src/candidates) | 469.2 | 407 |
| preview (gif/mp4/board/showcase/review/discord) | 368.8 | 235 |
| harvest results bundles | 142.3 | 556 |
| unclassified images | 72.4 | 1,287 |
| intermediate (vNN/seq/keys/sprites/kit) | 60.1 | 513 |
| code/text | 46.7 | 2,301 |
| final exports (exports/final) | 36.8 | 1,848 |
| push/ | 26.6 | 464 |
| archive/ | 11.4 | 345 |

## 3. Per-directory size table by role (MB)
| dir | total MB | final-export | raw-source | preview | intermediate | unclassified-img | code/text |
|---|---|---|---|---|---|---|---|
| docs/design | 293.7 | 0.0 | 0.8 | 240.3 | 0.0 | 39.7 | 12.8 |
| art/jutsu_icons | 289.3 | 14.0 | 129.4 | 83.3 | 58.7 | 3.2 | 0.6 |
| harvests | 142.3 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| art/skyglass_event_icons | 70.8 | 2.8 | 67.7 | 0.0 | 0.0 | 0.2 | 0.0 |
| art/crownhold | 57.6 | 2.1 | 51.6 | 1.3 | 0.0 | 2.6 | 0.0 |
| art/halloween_headless_rider | 54.9 | 0.9 | 17.1 | 34.2 | 0.0 | 2.6 | 0.1 |
| art/mother_of_echoes | 43.5 | 3.9 | 39.6 | 0.0 | 0.0 | 0.0 | 0.0 |
| art/skyglass_boss_fx | 38.6 | 0.2 | 38.3 | 0.0 | 0.0 | 0.0 | 0.1 |
| art/item_icons | 30.9 | 1.1 | 29.8 | 0.0 | 0.0 | 0.0 | 0.0 |
| push | 26.6 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| art/skyglass_variant_skins | 23.3 | 0.7 | 22.5 | 0.0 | 0.0 | 0.0 | 0.0 |
| skills/producing-tnr-art | 19.0 | 0.0 | 14.4 | 0.5 | 1.4 | 2.2 | 0.6 |
| art/dusk_dawn_variants | 12.0 | 0.1 | 11.9 | 0.0 | 0.0 | 0.0 | 0.0 |
| archive | 11.4 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| art/village_bloodline_scrolls | 11.0 | 0.4 | 10.6 | 0.0 | 0.0 | 0.0 | 0.0 |
| state | 10.6 | 0.0 | 0.0 | 0.0 | 0.0 | 1.5 | 9.2 |
| art/skyglass_jutsu_icons | 9.2 | 0.4 | 8.7 | 0.0 | 0.0 | 0.0 | 0.0 |
| art/ghost_ship_skyglass | 9.0 | 0.0 | 2.1 | 0.0 | 0.0 | 6.9 | 0.1 |
| art/two_tails_armor | 8.1 | 0.2 | 7.3 | 0.6 | 0.0 | 0.0 | 0.0 |
| art/skyglass_thread | 8.0 | 0.0 | 0.0 | 7.6 | 0.0 | 0.0 | 0.4 |
| docs/reviews | 6.4 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 6.4 |
| art/mother_of_echoes_fx | 6.3 | 4.9 | 0.0 | 0.0 | 0.0 | 0.5 | 0.9 |
| art/characters | 5.6 | 0.0 | 5.6 | 0.0 | 0.0 | 0.0 | 0.0 |
| art/bloodright | 5.1 | 0.0 | 0.0 | 0.0 | 0.0 | 5.1 | 0.0 |
| art/subaku_palace | 4.5 | 0.0 | 4.3 | 0.0 | 0.0 | 0.0 | 0.2 |
| art/gobblefather | 3.6 | 0.0 | 0.0 | 0.0 | 0.0 | 3.6 | 0.0 |
| art/style_refs | 3.3 | 0.0 | 3.3 | 0.0 | 0.0 | 0.0 | 0.0 |
| art/hullbound_mender_fx | 3.0 | 2.9 | 0.0 | 0.0 | 0.0 | 0.0 | 0.1 |
| guide-studio | 2.9 | 0.0 | 0.0 | 0.3 | 0.0 | 0.7 | 1.8 |
| forge | 2.1 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 2.1 |
| art/skyglass_scene_chars | 1.9 | 0.1 | 1.8 | 0.0 | 0.0 | 0.0 | 0.0 |
| skills/building-tnr-content | 1.9 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.9 |
| harness | 1.8 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.8 |
| art/godstorm | 1.8 | 0.0 | 0.0 | 0.0 | 0.0 | 1.8 | 0.0 |
| art/skyglass_journal | 1.7 | 0.1 | 1.6 | 0.0 | 0.0 | 0.0 | 0.0 |
| docs/handoffs | 1.5 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.5 |
| art/dragon_king_impact | 1.4 | 1.4 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| player | 1.1 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.1 |
| art/ai_avatars | 0.9 | 0.0 | 0.9 | 0.0 | 0.0 | 0.0 | 0.0 |
| art/duelyst_fx | 0.9 | 0.0 | 0.0 | 0.8 | 0.0 | 0.0 | 0.1 |

## 4. Move plan by directory (MB). Full per-file list: assets_movelist.tsv (category, bytes, path)
Categories: M1 docs/design previews+review stills; M2 art raw/unkeyed sources & rejected candidates;
M3 art preview GIF/MP4/boards (excluding exports/final); M4 superseded version dirs (vNN/seq/keys/sprites/kit);
M5 producing-tnr-art `_raw.png` (already excluded from skill ZIPs by pack_skills.py ARCHIVE_ONLY_DIRS);
K1 keep: raws pinned by approved.json (bakuhatsu/raws, ethereal_rebirth/candidates);
K3 keep: exports/final; K4 keep: other images (review per dir); K5 keep: art/style_refs.

| category | MB | files |
|---|---|---|
| M1 docs/design previews | 280.9 | 226 |
| M2 art raws/candidates | 432.2 | 353 |
| M3 art previews | 124.6 | 69 |
| M4 superseded versions | 58.7 | 509 |
| M5 skill archive-only raws | 14.4 | 7 |
| **move total** | **910.8** | 1,164 |
| K1 pinned raws | 18.5 | 12 |
| K3 final exports | 39.9 | 1,887 |
| K4 other images | 31.4 | 520 |
| K5 style_refs | 3.3 | 34 |

References to moved files (from refs.txt): referenced by per-folder build/preview scripts
(mostly as their own OUTPUT names) M1 36.6 / M2 52.7 / M3 81.9 / M4 24.5 MB; doc-only links
M1 196 / M2 202 / M3 26 MB; unreferenced M1 48 / M2 177 / M3 17 / M4 34 MB.
No push/*.json manifest, forge/*.mjs, or state/run_queue.json references any M-category path
(push/README.md is the only push/ file citing docs/design previews). Push manifests reference
1,641 local asset paths (~69 MB), 1,243 under /exports/; run_queue references none.
Exception to verify before moving: art/jutsu_icons/bakuhatsu/approved.json is validated by
skills/producing-tnr-art/scripts/jutsu_studio.py:1237-1243 which requires raw_file present and
sha-matching -> keep K1 or teach the validator to fetch.

| dir | M1 | M2 | M3 | M4 | M5 | K1 | K3 | K4 | K5 | move MB | keep MB |
|---|---|---|---|---|---|---|---|---|---|---|---|
| art/jutsu_icons/forbidden_chakra_fury |  | 18.2 | 82.2 | 58.7 |  |  | 2.9 |  |  | 159.1 | 2.9 |
| docs/design/celestial_dew_animation | 137.8 |  |  |  |  |  |  |  |  | 137.8 | 0.0 |
| art/skyglass_event_icons/raw |  | 67.7 |  |  |  |  |  |  |  | 67.7 | 0.0 |
| docs/design/ethereal_rebirth_animation | 62.3 |  |  |  |  |  |  |  |  | 62.3 | 0.0 |
| art/mother_of_echoes/raw |  | 39.6 |  |  |  |  |  |  |  | 39.6 | 0.0 |
| docs/design/icon_overhaul | 38.6 |  |  |  |  |  |  |  |  | 38.6 | 0.0 |
| art/skyglass_boss_fx/raw |  | 38.3 |  |  |  |  |  |  |  | 38.3 | 0.0 |
| art/halloween_headless_rider/fx |  |  | 32.9 |  |  |  | 0.9 |  |  | 32.9 | 0.9 |
| art/jutsu_icons/chakra_overflow |  | 25.2 |  |  |  |  | 0.7 |  |  | 25.2 | 0.7 |
| art/item_icons/event_scrolls |  | 24.4 |  |  |  |  | 1.0 |  |  | 24.4 | 1.0 |
| art/crownhold/raw |  | 23.3 |  |  |  |  |  |  |  | 23.3 | 0.0 |
| art/skyglass_variant_skins/raw |  | 22.5 |  |  |  |  |  |  |  | 22.5 | 0.0 |
| art/jutsu_icons/scroll_jutsu |  | 20.2 |  |  |  |  | 1.0 | 0.1 |  | 20.2 | 1.1 |
| art/jutsu_icons/tenryuseigan |  | 18.7 |  |  |  |  | 0.7 |  |  | 18.7 | 0.7 |
| docs/design/skyglass_boss_fx | 18.1 |  |  |  |  |  |  |  |  | 18.1 | 0.0 |
| art/crownhold/scenes |  | 14.7 |  |  |  |  | 1.0 |  |  | 14.7 | 1.0 |
| skills/producing-tnr-art/data |  |  |  |  | 14.4 |  |  | 4.0 |  | 14.4 | 4.0 |
| art/crownhold/avatars |  | 13.5 |  |  |  |  | 1.1 |  |  | 13.5 | 1.1 |
| art/dusk_dawn_variants/raw |  | 11.9 |  |  |  |  |  |  |  | 11.9 | 0.0 |
| art/village_bloodline_scrolls/raws |  | 10.6 |  |  |  |  |  |  |  | 10.6 | 0.0 |
| art/jutsu_icons/starter |  | 9.9 |  |  |  |  | 0.5 |  |  | 9.9 | 0.5 |
| art/jutsu_icons/celestial_dew |  | 9.7 |  |  |  |  | 3.8 |  |  | 9.7 | 3.8 |
| docs/design/chakra_overflow | 9.6 |  |  |  |  |  |  |  |  | 9.6 | 0.0 |
| art/skyglass_jutsu_icons/raw |  | 8.7 |  |  |  |  |  |  |  | 8.7 | 0.0 |
| docs/design/subaku_palace | 8.4 |  |  |  |  |  |  |  |  | 8.4 | 0.0 |
| art/halloween_headless_rider/domain |  | 8.4 |  |  |  |  |  |  |  | 8.4 | 0.0 |
| art/two_tails_armor/raws |  | 7.2 |  |  |  |  |  |  |  | 7.2 | 0.0 |
| art/jutsu_icons/ethereal_rebirth |  | 7.1 |  |  |  | 14.0 | 2.8 | 1.7 |  | 7.1 | 18.5 |
| art/characters/forbidden_master |  | 5.6 |  |  |  |  |  |  |  | 5.6 | 0.0 |
| art/skyglass_thread/preview.png |  |  | 5.5 |  |  |  |  |  |  | 5.5 | 0.0 |
| art/halloween_headless_rider/hellfire_harvest |  | 5.2 |  |  |  |  |  |  |  | 5.2 | 0.0 |
| art/subaku_palace/refs |  | 4.2 |  |  |  |  |  |  |  | 4.2 | 0.0 |
| art/halloween_headless_rider/aura_of_despair |  | 3.6 |  |  |  |  |  |  |  | 3.6 | 0.0 |
| docs/design/mother_of_echoes_fx | 2.8 |  |  |  |  |  |  |  |  | 2.8 | 0.0 |
| art/item_icons/chunin_exam_scrolls |  | 2.2 |  |  |  |  | 0.1 |  |  | 2.2 | 0.1 |
| docs/design/scroll_icons | 2.2 |  |  |  |  |  |  |  |  | 2.2 | 0.0 |
| art/ghost_ship_skyglass/structure |  | 2.1 |  |  |  |  |  | 0.3 |  | 2.1 | 0.3 |
| art/skyglass_scene_chars/raw |  | 1.8 |  |  |  |  |  |  |  | 1.8 | 0.0 |
| art/skyglass_journal/raw |  | 1.6 |  |  |  |  |  |  |  | 1.6 | 0.0 |
| art/jutsu_icons/overhaul |  | 1.6 |  |  |  |  | 0.1 |  |  | 1.6 | 0.1 |

## 5. Manifest format (proposal)
`assets/offloaded.jsonl` (one line per file, sorted by path, generated + checked by a script):
{"path":"art/crownhold/scenes/raw/X.png","sha256":"<64hex>","bytes":2345678,"category":"M2",
 "store":"gh-release:assets-2026-11","pack":"art-raws-crownhold.tar","added":"2026-11-27"}
- Moved paths go into .gitignore (by directory glob: `art/**/raw/`, `art/**/raws/`, `docs/design/**/*.gif`, ...)
  so a fetched file never shows as untracked and cannot be re-committed.
- `scripts/assets.py fetch <glob>|--for <dir>` downloads the pack(s), verifies sha256 per file, restores paths.
  `scripts/assets.py offload <glob>` hashes, packs, uploads, appends manifest lines, git rm --cached.
  `scripts/assets.py check` (CI): manifest sorted/unique, no manifest path tracked, every pack listed exists (HEAD request optional/offline skip).
- Pack per (category, top dir) as uncompressed tar (PNG/GIF/WebP don't compress); ~60 packs instead of 1,164 objects.

## 6. Storage comparison
| | GitHub Releases | Cloudflare R2 | UploadThing |
|---|---|---|---|
| auth in this env | gh CLI preconfigured, REST works (GraphQL 403) | MCP is deprecated and only manages buckets (no object put); needs API token via request_credential + rclone/wrangler | director's account; needs token |
| cost | free; 2 GiB per asset | 10 GB free, then ~$0.015/GB-mo, zero egress | free tier 2 GB; it is the live game image CDN host (ufs.sh) |
| privacy | same as repo = PUBLIC | private bucket possible | public URLs |
| fit | immutable versioned packs; one tag per offload batch | per-file fetch, browsable, private | mixing working raws with production CDN is a risk |
Recommendation: GitHub Releases for the first offload (no new credentials, same ACL and provenance as the repo,
packs are immutable). Switch to R2 only if the director wants working material private (decide).

## 7. Guard thresholds (proposal for scripts/check_large_files.py)
- Default new-file limit 1 MiB (was 5 MiB). 548 files currently exceed 512 KB, 384 exceed 1 MiB -> grandfather via --write once after the offload.
- Images under art/ (png/webp/jpg/gif): 512 KiB = spec upload.hard_cap_bytes (25x_DATA_art_spec.json); only 3 tracked exports exceed it.
- Path deny: new tracked files matching the offload globs (raw/, raws/, candidates/, previews/, docs/design/**/*.gif|mp4) fail regardless of size.
- .gif/.mp4/.zip anywhere: 512 KiB.
- Aggregate: PR/push adding > 20 MiB of new blobs fails (git diff --numstat base...head plus cat-file sizes).
- Allowlist stays a director decision; add an expiry/owner column.
