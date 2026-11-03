# Workflow — Premium Item Icon Overhaul (collection and batch lane)

**Status:** staged pilot workflow; no blanket item-replacement approval. **Lead:** Art Director; **support:** Image Production.
**Routes from:** `docs/workflows/ART_PRODUCTION.md`; also apply `docs/workflows/ISOLATED_ART_GENERATION.md` for one-image sessions, `skills/producing-tnr-art/SKILL.md` for production, and `docs/design/premium_seichi_item_icons/V10_STYLE.md` for quality direction.

This is an **ICON item.image** workflow. The numeric/format/chroma/alpha/client contract remains exclusively in `skills/producing-tnr-art/data/25x_DATA_art_spec.json`; the script below is offline staging, **not** a new art format or new live API. A replacement collection groups related items and proceeds one approved subject at a time. Final selection, redesign exceptions, image approval, family acceptance, and all live-game actions belong to the director.

## Phase 1 — Intake and capture (required before art)

1. **Choose a coherent family/wave** with item IDs, not a random cross-rarity assortment. The initial **proposal** is `docs/design/item_icon_overhaul/W01_ELEMENTAL_KUNAI.json`; `ITEM_ICON_REGISTER.md` is the durable human register.
2. **Inspect existing repository evidence**: `harvests/seed/41_INDEX_item.json` and `answers/names_item.json` can route names/IDs, but are historical name indexes without `item.image`. `skills/producing-tnr-art/data/art_index_2026-08-26.json` enumerates gameAsset scene/static art, **not** items; never use it as an item-icon census. The historical kunai files at `art/item_icons/kunai/refs/` supply some original pixel references, not proof of current live images.
3. **Capture exact item full records** (`item.get` per ID) using the existing operator-authorized capture-only Forge/harvest route. Any future live request must be separately initiated by the director, outside this task. No live request is made by the tooling below. Check complete `id`, `name`, `itemType`, `rarity`, `slot`, `image`, visibility and capture timestamp. A `getAllNames` or trimmed seed row is insufficient to prove the icon. Preserve the full result bundle and `snapshotKey`.
4. Verify capture scope and success before use:
   ```bash
   python3 skills/building-tnr-content/scripts/harvest.py index harvests/inbox/<capture-bundle>.json
   python3 skills/building-tnr-content/scripts/harvest.py get harvests/inbox/<capture-bundle>.json --proc item.get
   ```
   The `get` command shows one result if multiple calls occur; retain and inspect the full capture bundle for ID-by-ID evidence.
5. **Offline roster** (run from repo root):
   ```bash
   python3 skills/producing-tnr-art/scripts/item_icon_batch.py roster \
     --wave docs/design/item_icon_overhaul/W01_ELEMENTAL_KUNAI.json \
     --capture harvests/inbox/<capture-bundle>.json \
     --out work/item_icon_overhaul/W01 --require-complete
   ```
   Repeat `--capture` for multiple source bundles. Outputs `roster.json` and `roster.csv`, recording source hash, snapshot/capture time, exact image URL and missing/conflict states. `--require-complete` exits nonzero when a candidate lacks exact confirmed `item.get` evidence. A miss means **not captured**, never **absent live**. Different images/names for the same ID are a **CONFLICT**, not silently reconciled.
6. **Materialize source image bytes only through the established, separately authorized artifact process.** Save each source image locally, hash it, and record exact URL + file/SHA mapping. The roster helper never fetches images and never calls the game or CDN. Keep raw source bytes in the wave archive when permitted. Create an image-map JSON `{"<item-id>": {"path":"<local-image-file>","sha256":"<actual-sha256>"}}` with explicit IDs and run:
   ```bash
   python3 skills/producing-tnr-art/scripts/item_icon_batch.py sheet \
     --roster work/item_icon_overhaul/W01/roster.json \
     --image-map work/item_icon_overhaul/W01/source_images.json \
     --out work/item_icon_overhaul/W01/source_contact_sheet.png
   ```
   Contact sheet is **deterministic, Pillow-only**, visually labeled at 256/125/64/32. `source_contact_sheet.json` records inputs, image hashes, resampling and `DRAFT_INCOMPLETE` until every file is present. This sheet is **studio review evidence**, not an image-generation input or a production export. Keep all image files unchanged.

## Phase 2 — Benchmark, identity lock and pilot

1. Study the *individual* current icon, then the *individual* Tatsumaki V10 benchmark (quality/style only), then the family references. Explicitly label every reference's role. A contact sheet is for collection QC only; **never attach a sheet as an image-generation reference**.
2. Write each item identity lock: exact item/ID, captured current URL/hash, core silhouette/anatomy, orientation, material/element, heritage motif, reserved family relationship, disallowed features and allowed changes. The prior elemental-kunai redesign concept is a **proposal**; it does not overrule identity preservation without director acceptance.
3. Choose one pilot (proposed: Ikazuchi). Make a single authored pixel-art candidate at a time. Code-assisted/layered production is valid; do not auto-pixelate a smooth painting. Use the V10 large/medium/small clusters, hue-shifted materials, sculptural energy and material/effect bounce.
4. Judge its native clusters plus 125/64/32 views and material transparency. Present for **explicit director pilot approval**. Do not extrapolate approval to the rest of the set. Archive original layered/native source and accepted raw, with SHA-256 and provenance before batch production.

## Phase 3 — Batch execution, sequential gates

1. Lock the family base from the approved pilot, while preserving each sibling's distinguishing blade, effect, material and identity.
2. Prepare one isolated subject brief and 1–2 *individual* references per target; never ask a generator to produce an entire sheet. Make/QC **one asset at a time** (the approved batch is a planning unit, not permission to skip individual gates).
3. Record each original/raw, approval, versions and optional non-destructive layer breakdown. Prefer deliberate pixel-cluster editing. If a subject's silhouette contradicts the pilot template, return to the director rather than silently standardizing it.
4. Use spec-driven `ICON` processing. Item icons require **transparent square lossless WebP**; do not borrow the opaque `JUTSU_ICON` exception. Corrected files receive new versioned names. Archive exports separately from proofs and from the source captures.

## Phase 4 — QC, family register and handoff

- For **each item**: source and native hash; director raw acceptance; pixel cluster/material/effect QC; transparency on dark and checker surfaces; 256/125/64/32 thumbnail readability; exact output bytes, pixel dimensions and filename; `artpreflight.py --type ICON` PASS (use repo spec); preserve artpreflight output.
- For **family set**: same presentation scale/crop/lighting logic, distinct silhouettes/elements, coherent quality, no repeated wind ribbons or artificial noise. Compose final comparison sheets **from exact approved export bytes** deterministically. Mark any missing member **DRAFT**, never family-approved. If an export changes, invalidate/rebuild the related sheet.
- Update `ITEM_ICON_REGISTER.md` with source IDs/URLs/snapshots, `wave`, benchmark reference roles, acceptance stages, hashes, export/QC and `@img`/wiring state. An icon can be art-approved but not export-QC-passing, and export-ready without being live.
- Prepare a **separate Fable/content wiring suggestion** only after accepted family/export evidence. Exact `@img` filename is a binding contract. No batch uploads, game writes, live verification or publishing are authorized by this workflow; only the director can execute the production action. Subsequent live read-back, if director-authorized, is recorded separately.

**Exit for intake:** named family, exact IDs, source status honestly marked, reproducible roster/sheet path, pilot proposal. **Exit for production:** all icons individually approved and preflighted, full final family gallery accepted, exact filenames/hashes, operator handoff. Those exits are deliberately different.
