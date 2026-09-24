# One Perfect Crop — scene-character production record

**Task:** `art.scene_characters`  
**Status:** IN_PROGRESS — Road Bandit production candidate is mechanically clean and awaits user visual acceptance.  
**Repository baseline:** `main@2f5c54ba4ec04596783a972f4c084b89d8087cec`  
**Production branch:** `chatgpt/one-perfect-crop-scene-characters-20260923`  
**Live-game activity:** none; zero TNR API requests, zero Forge execution, zero live writes.

## Scope result

The launch-final scene-character set for this packet is:

- Ittetsu — already accepted design; intake bytes are owned by the separate `art.intake_accepted_assets` packet.
- Waystation Keeper — already accepted design; intake bytes are owned by the separate `art.intake_accepted_assets` packet.
- Road Bandit — new `SCENE_CHARACTER` produced in this packet.
- Market Clerk — reuse `DM Mission Clerk`, gameAsset `XsLLy8awDAtaE6hXVIi_0`; no new Market Clerk art is required.

No Harvest Boar scene character is required by the frozen prose graph. Combat avatars, icons and backgrounds are outside this packet.

## Market Clerk reuse evidence

Committed read-only capture `harvests/inbox/tnr_results_1789060167786.json` resolves:

- id: `XsLLy8awDAtaE6hXVIi_0`
- name: `DM Mission Clerk`
- type: `SCENE_CHARACTER`
- capture outcome: successful read-only gameAsset.get, with no mutation journal entries.

The frozen prose graph wires this reused asset into `opc_d1` through `opc_d5`.

## Road Bandit direction

Narrative role: a lone opportunistic highway shinobi on the old levee road, not a named elite or faction operative.

Direction used:

- NINJA register, full-body 2:3 scene-character framing;
- worn charcoal/brown layered wraps and robe pieces;
- restrained rust/copper accent;
- open, weathered adult male face matching the prose pronoun;
- guarded but non-dynamic stance;
- no faction mark, forehead protector, clan symbol, real-world logo, ornate plate, text, UI or scenery;
- no separate weapon prop.

Committed calibration references inspected individually:

- `art/style_refs/scene_characters/commander_okabe.png` — face/detail anchor only, not framing.
- `art/style_refs/scene_characters/winter_crow.webp` — current full-body ninja silhouette.
- `art/style_refs/scene_characters/pale_fang.webp` — current full-body ninja silhouette.
- `art/style_refs/scene_characters/old_ghost.webp` — unarmoured full-body register.
- supporting role reference: `art/style_refs/scene_characters/squad_survivor.webp`.
- scene context: `art/style_refs/scene_backgrounds/east_road_ambush_site.webp`.

Reference-pack index/provenance: `skills/producing-tnr-art/data/style_refs.json` and committed read-only capture `harvests/inbox/tnr_results_1789061570022.json`.

## Generation record

### Rejected raw generation

ChatGPT image generation id: `68a7ae56-c879-4b30-aa3d-52f191f311dd`.

The visual direction was acceptable, but generator-native transparency produced partial alpha across the entire visible subject. Raw SHA-256: `19bd89789395b9252bd49bfdf1a177e70808715851c6214ebd6aa5bad51e6fb9`. It was rejected mechanically and not processed as a shipping candidate.

### Current candidate raw

ChatGPT image generation id: `5346b182-3d27-4149-9bc0-62a502bdd209`.

Raw SHA-256: `c4d13b2ce4b265a195d36acfc828e39244535a23f2d70004008b789566153475`.

Raw mechanical QC, using the current `rawqc.py` thresholds read from the exact baseline:

- 1024×1536, exact 2:3 source framing;
- detected key: lime;
- key coverage: 0.695, inside the 0.30–0.92 acceptance band;
- 2px border-ring purity: 1.0000;
- verdict: ACCEPT.

## Processing / candidate output

Exact launch filename contract:

`one_perfect_crop_road_bandit_scene.webp`

Processing target: `SCENE_CHARACTER`, frame `full`, lime key, 2:3 transparent padding, lossless WebP.

The repository shell was unavailable in this session because the sandbox could not resolve github.com for a clone. The committed `chroma.py` algorithm and per-file `artpreflight.py` check path were therefore read from exact `main@2f5c54b` through the GitHub connector and reproduced locally without changing their target constants.

Processed candidate:

- dimensions: 985×1478;
- bytes: 122,460 (119.6KB);
- SHA-256: `d4ce032ab1ffe9332e3673aa7437b140f17ae216aee31ba51c7aa2dd5a731a14`;
- lossless WebP: yes;
- aspect: 0.66644, within the ratified full-body band;
- h/w: 1.50051, below the 5/3 clip bound;
- width: above the 341px minimum;
- partial-alpha share: 0.0%;
- residual lime/magenta key pixels: 0;
- dark-background composite SHA-256: `9bc25c4587ad0e73655c0000e012ee96252fe7a07d8a32a333c3e5f6ea397ed8`;
- visual dark-QC: clean silhouette/edges, no obvious spill or chewed anatomy;
- reproduced per-file preflight result: **0 errors, 0 warnings**.

Before an accepted production handoff, rerun the repository-native CLI directly when a checkout is available. Do not treat this record as live-game wiring or publishing authorization.

## Resume / acceptance gate

Await user visual acceptance of the processed Road Bandit candidate.

If accepted:

1. make the exact processed bytes durable in the repository;
2. update `state/art_produced.md` from CANDIDATE to APPROVED with user/date;
3. rerun native `artpreflight.py` when a checkout is available and record zero errors;
4. mark `art.scene_characters` COMPLETE with evidence and regenerate workstream projections.

If rejected, generate a fresh version/filename according to the art filename/cache contract rather than silently replacing approved bytes.
