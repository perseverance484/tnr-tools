# Bakuhatsu jutsu icons: approved raws (2026-10-19)

The director approved these five raws one by one on 2026-10-19, under the art direction **CONCUSSIVE FRACTURE**:
fire and explosion art with no figures. They **replace** the live Bakuhatsu icons, which are the old
figure-silhouette set and are no longer an approved reference (RUL-2026-10-20-004, as amended).

Source: `bakuhatsu_Art_Studio_Closeout_5of5_20261020.zip` (sha256
`c66853c6009e4de3d5bd901b26ab10e4c1f155d88ed079b5aa63e442b6e574cc`, every `SHA256SUMS` line verified at intake). The bytes are copied exactly.

| Jutsu | Id | Raw | Format | sha256 | Shows |
|---|---|---|---|---|---|
| Inferno Cataclysm | `FTTl_wnTlbvOfOyiGCc-b` | `raws/raw_bakuhatsu_inferno_cataclysm_v1.jpg` | JPEG 1536x1536 | `6bdaaf03a35532b0cfa3bc64150187540a2b4bbcaf87b283d0f6d09e0828e214` | a fire pillar erupting from a fissure, tilted stone slabs |
| Kinetic Nova | `y8y01n9jz16bz5EBzl4wr` | `raws/raw_bakuhatsu_kinetic_nova_v1.jpg` | JPEG 1536x1536 | `7bfdcfaeb20a026f5f98a5381ac564f8a6d441ab8b024f1c7d39a84237bc5050` | an airborne cluster of many small explosions |
| Blast Shield | `Awyd1k1-tw4uzn-PLbcdP` | `raws/raw_bakuhatsu_blast_shield_v1.jpg` | JPEG 1536x1536 | `f2167a947f77c56f39a6d24b8af0660406cf7654872fdf88407333f0539be308` | a circular fire barrier deflecting debris |
| Charge 4 Explosion | `rOqCTqNBSW_A-QYesFBw9` | `raws/raw_bakuhatsu_charge_4_explosion_v1.jpg` | JPEG 1536x1536 | `619bc4f7a86adfdbdf98a124a2f816911e199389ae26240cb04a56c8bb1bdd8a` | linked micro-detonations tracing a "C4" on cracked ground |
| Howitzer Crash | `hW4IV1Hp59BqVFx0u-gTd` | `raws/raw_bakuhatsu_howitzer_crash_v3.png` | PNG 1254x1254 | `e410b382b9e268efdad878f80d9f97ce21b70a289350674c3c18c7ec9a39727c` | a V-shaped bow shock converging on one point |

## Status

- Raw approvals: 5/5. Direction locks: 5/5 `DIRECTION_APPROVED`.
- **Exports (2026-10-20):** `exports/icon_bakuhatsu_*.webp`, 256x256 lossless WebP, made by
  `jutsu_studio.py finalize` from the raws without retouching. `artpreflight.py --type JUTSU_ICON`:
  0 errors, 0 warnings. QC and preflight output in `exports/qc/`; the 125/64/32 px sheet and the 3+2
  showcase are in `exports/`.
- Family acceptance (director approval of the export showcase) is still `PENDING` in `approved.json`.
- Sent to the content review desk as push/142 (suggest mode). The live game shows the old icons until
  a reviewer approves.

| Export | Bytes | sha256 |
|---|---|---|
| `exports/icon_bakuhatsu_blast_shield_v1.webp` | 114406 | `69111187faee0a28f997bb202a635116808e1e604a74ac32873eab8ae51f0e13` |
| `exports/icon_bakuhatsu_charge_4_explosion_v1.webp` | 132104 | `61738332b128c02cbd94fe4539914ae5c72c5771f6774b0ee19c3bc022f01748` |
| `exports/icon_bakuhatsu_howitzer_crash_v3.webp` | 100670 | `661fa177909871dc05a677a66a298a07e4978acc56f8b8f72463e78b82129417` |
| `exports/icon_bakuhatsu_inferno_cataclysm_v1.webp` | 130016 | `e1556eafe266ea53e4c9f1f0c223f73954bd3cbc3049527f20da4aa16e19ee6e` |
| `exports/icon_bakuhatsu_kinetic_nova_v1.webp` | 119208 | `bd2dbe42b0ea603998a1867362c54838e88b9a3d3f00e56f31856b860fcc052b` |

## Files

- `approved.json`, `locks.json`, `source_index.json`, `studio_ledger.json`, `jutsu_id_map.csv`: the
  studio ledgers, unchanged. Raw paths are relative to this folder.
- `evidence/`: approval and provenance, the intake report, and the studio's doctor and check output.
- `VERSION_HISTORY_AND_REJECTIONS.md`: rejected and superseded candidates. They are not inputs.
- Left out of the repository: the old live icons and their source ZIP (superseded, and they must not be
  used as references) and the draft 3+2 raw preview (not an approved gallery).

## Checks (run from this folder)

```shell
python3 ../../../skills/producing-tnr-art/scripts/jutsu_studio.py lock-check locks.json --source-index source_index.json
python3 ../../../skills/producing-tnr-art/scripts/jutsu_studio.py verify-approved approved.json --source-index source_index.json --locks locks.json
```

Both pass on 2026-10-20: verify-approved reports `N=5, family acceptance PENDING`.
