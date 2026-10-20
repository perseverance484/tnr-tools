# TNR Master Asset Processing Station — scope transition and opening contract

**Status:** Director-directed 2026-10-20 session handoff; **not** a change to game doctrine or production-tooling code.  
**Repository:** `perseverance484/tnr-tools`. **Verified main at handoff:** `10053b7215aa53d1fc3fc7b466cb3958ef361cea`.  
**Lead:** Image Production; **support:** Engineering Auditor. **Live-game requests/writes:** 0/0. **Credentials:** none.

## Director-directed change

Retire the A/S/H **master collection** station as an active 25-family accumulation/delivery pipeline. Replace it with ONE persistent, reusable **Master Asset Processing Station** for **all TNR production-art types**. The operator supplies one approved image or one ZIP of approved images; the station inspects, mechanically processes, validates and returns game-ready exported image bytes, exact binding information and, when sufficient source-backed target information exists, a **validated upload manifest + flat ZIP push pack**. Per-intake delivery replaces cumulative campaign checkpoints. This station does **not** generate or creatively alter artwork and does **not** touch the game.

The historical 29-family ledger is archived provenance, **not** the universal station's queue. Four previously processed/submitted bloodlines (Blood-Enchanted Eyes, Blue Blade Eyes, Vaporia, Aerathiel) are outside the retired A/S/H pipeline and are not reprocessed merely because this desk exists.

## Authority and boundaries

Read current `main` and `state/active-context.md`, `state/status.json`, `docs/00_INDEX.md`, `docs/RULINGS.md`, `CHATGPT.md`, `docs/DEVELOPMENT_WORKFLOW.md`, the applicable `docs/agents/` roles, `docs/workflows/ART_PRODUCTION.md`, `skills/producing-tnr-art/SKILL.md`, `skills/producing-tnr-art/references/processing.md`, and `skills/producing-tnr-art/data/25x_DATA_art_spec.json`. For jutsu, also read `ISOLATED_ART_GENERATION.md`, `BLOODLINE_JUTSU_ICON_STUDIO.md`, `JUTSU_ICON_SHOWCASE.md`, and current family records. For any actual builder manifest, read `skills/building-tnr-content/references/pipeline.md` and the **current generated contracts and validator**. `docs/00_INDEX.md` still arbitrates evidence.

Fable remains the normal implementer of tooling/code and content manifests unless explicitly assigned otherwise. This station can prepare **asset-only mapping manifests**, and may prepare a **visual-only upload manifest** when the operator provides exact target bindings and the current source/capture/contract evidence permits it. Never invent ids, change gameplay fields, substitute a fake empty `items` manifest or call an unchecked metadata inventory an executable builder manifest. Use Forge `mode: suggest`, `category: VISUAL` and specific per-item rationales for appropriate existing-record icon proposals; check current authoritative suggest-mode contract. No credentials, no TNR API requests, no submissions, no publishing, no claims of current-live state based only on historical records.

## Per-intake contract

1. **One upload/ZIP at a time.** Identify intended TNR client field and spec target, exact entity/record/jutsu ID if provided, director-approved original and version, existing `@img`/manifest if any, workstream cap and any permitted quality tradeoff. Never infer an unknown identity. Refuse malformed ZIP paths, symlinks, duplicates/collisions, bombs, bad CRC and unverified/superseded member bytes.
2. **Preserve the source bytes and provenance.** Record true MIME/decoder, dimensions, SHA-256, version and evidence level. Existing compliant WebP exports remain byte-for-byte unchanged. No generative changes, repaints, silent recolors, automatic quantization or irreversible crops.
3. **Process only as needed** with the real repo skill tools and current per-type spec. In particular: opaque designed `jutsu.image` background permitted (`JUTSU_ICON`); item/bloodline `ICON` retains alpha; scene backgrounds, keyed scene characters, avatars, pins and animations have different contracts. Never apply lime chroma to a designed opaque jutsu background. Do not silently reuse jutsu-specific limits on unrelated assets.
4. **Verify output and run the real canonical preflight** for each target; record actual command, exit code, output and canonical pins when relevant. `doctor` tests environment capability only. `NOT_RUN` and `NON_CANONICAL` are never `PASS`. Inspect dark composites and appropriate true-size thumbnails. For full jutsu families, retain distinct family/gallery director acceptance and audit exact exported pixels.
5. **Manifest join:** preserve exact production filenames; corrected bytes require a new versioned filename. Produce source/output hashes, dimensions, size, type, target binding and `@img:<filename>` mapping. If producing a runnable builder/Forge `manifest.json`, include exact `imgSizes`, validated target IDs/contracts, `@img` references and per-item rationales; run `validate.py` with zero errors. The actual builder push ZIP is FLAT: `manifest.json` and its image files at ZIP root. If binding, validation, approval or preflight is missing, produce an explicitly **NON-RUNNABLE HOLD/asset-mapping** package, never a deceptively named ready-to-upload manifest.
6. **Delivery per job:** hand back (a) a flat, checked upload pack **only when all relevant gates passed**, (b) a separate provenance/recovery ZIP preserving original submission, receipts, QC, source/output hashes and validation logs, and (c) brief current gate status. Maintain a job ledger, not a 29-bloodline running master. Never upload, publish, operate Forge, or modify game records.

## Carryover: Bakuhatsu (optional first job)

A previously accepted **raw Art Studio** handoff exists at `chatgpt/bakuhatsu-jutsu-art-studio-20261019@fca659fec26af61ae4fe99b5ad2752440177cc42`; archive `bakuhatsu_Art_Studio_Closeout_5of5_20261020.zip` SHA-256 `c66853c6009e4de3d5bd901b26ab10e4c1f155d88ed079b5aa63e442b6e574cc`. The retired station produced local staged recovery `TNR_ASH_BAKUHATSU_FULL_CLOSEOUT_INTAKE_HOLD_v3.zip`, SHA-256 `88410e71933a7ad77075ce4cac06da5beb206760231c37e1ceab9585dfd99e83`, containing the full original closeout and five previously prepared lossless VP8L WebPs **unchanged**. Five approved original raws and ID bindings were checked. Its actual `CANONICAL_PREFLIGHT=NOT_RUN` and `FAMILY_SHOWCASE_ACCEPTED=PENDING`, so it is **not** an upload-ready pack. Do not reprocess unless necessary or accidentally promote past HOLD. No image-byte Git pin or game upload/readback was performed by this station.

Portable starter and carryover files are hand-delivered to the operator in the old conversation; their binary bytes are not added to the repository by this documentation branch.

## New-thread first response

Verify live `main`, inspect attached starter/binary bytes and official installed art runtime, run `jutsu_studio.py doctor` when available. Say which canonical tools are actually runnable. Confirm the universal, per-job scope and the Bakuhatsu optional HOLD. Ask for the first approved image or ZIP and target-binding evidence. Do not fabricate `PASS`, invent a manifest or start image generation.
