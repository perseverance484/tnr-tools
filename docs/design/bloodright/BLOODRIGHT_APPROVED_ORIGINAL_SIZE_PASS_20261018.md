# Bloodright — Approved Original Artwork, Game-Size Consolidation

**Status:** DIRECTOR-APPROVED NO-REGENERATION EXPORT POLICY; **27/87 exact final-size source-art WebPs independently verified and packaged from bytes currently recoverable in this conversation**; 57 earlier approved individual binaries not accessible; BR-036 Blackwire three individual exports are REVIEW-ONLY. **Not a 87/87 export closeout.** Field-specific `skillTree.image` preflight unresolved.

**Date:** 2026-10-18 · **Lead:** Image Production · **Lens:** Art Director · **Repository:** `perseverance484/tnr-tools`.
**Art branch:** `chatgpt/bloodright-approved-original-sizepass-20261018`; exact base `chatgpt/bloodright-wave06-art-studio-20261018@b9150dd7c05701fe443c8b41472a2cfc9744057a`. The user did **not** approve earlier pixelation batch; prior exploratory branch `chatgpt/bloodright-pixelart-wave01-20261018@da68f34d6d400cd11a9244ebbff66079be53b3fc` remains a rejected/abandoned production alternative, not an approved art source. This branch does not overwrite that evidence.

## Settled director workflow decision

User: **“Honestly they look pretty good if they just get processed down to size. Why dont we just do that for all of them, no regeneration or edits needed. They're pretty much pixel art once processed.”** The operator then explicitly directed **“Proceed.”**

- **Do NOT** restyle, recolor, regenerate, paint, modify effects, add sparkle, change silhouettes, remaster/pixelate, or replace artistically accepted content while processing.
- Approved 256×256 opaque RGB VP8L lossless source WebPs already satisfy the target-size/format QC. **Retain the original bytes exactly** rather than recompressing merely to claim work.
- For recoverable director-approved *raw* high-res art lacking a local game-sized WebP, resize once with Pillow **LANCZOS** and export lossless RGB VP8L using the approved art processing recipe; the output must be verified against any prior accepted file SHA.
- Keep each original filename and byte hash and deliver separate icon files (one bloodline shared icon for each of the three Foundation, Hidden Art, Advanced Art tiers), not a generated showcase.
- Preserve formal technical boundaries: the generic keyed `ICON` spec still wants RGBA, while the director-approved Bloodright skill tier icons have deliberately opaque black RGB backgrounds. The separate `JUTSU_ICON` optional-alpha exception does not prove `skillTree.image` field readiness; Fable must resolve the actual target field and preflight. Neither files nor repository access authorize live game requests/writes.
- Accepting the art visually does not settle older 12 strict-master-geometry failures. Retain those accepted file bytes, and obtain a new user decision before any visual pixel changes to enforce geometry.

## Exact recoverable 27 approved outputs

The operator's conversation currently mounts the four original Wave06 bloodline source ZIPs, their derived approved/proposed family packs, and the `Bloodright_Wave06_Production_Starter_20261018.zip` that preserves all **15 director-approved Wave05 VP8L WebPs** plus the **three director-approved Ethereal Monarch 1254px geometry-master raw PNGs**. The other earlier approved per-wave icon binaries are *not* contained in that starter, are not attached to this conversation, are not in the accessible Library Bloodright Reference folder, and were explicitly recorded as **not Git-pinned binaries**. Textual SHA ledgers alone are not a substitute for source pixel bytes.

| Cohort / verified source | Families | Icons | Handling |
|---|---|---:|---|
| Wave05 starter accepted comparators | BR-078 Tenohira Musei, BR-005 Arashima **Stormcloud V02**, BR-065 Shinrai Ou, BR-034 Hyouga Yui, BR-077 Teno Yuki | **15** | Each original approved 256×256 VP8L WebP copied **byte-for-byte**, checked against `WAVE05_APPROVED_MANIFEST.json` exact SHA and bytes. Arashima existing master-mask discrepancy remains RED; do not substitute rejected V01. |
| Wave06 approved three-icon production members | BR-033 Houkyuken **Ferroflux V02**, BR-002 Aerathiel **Aether Dissolution V02**, BR-040 Kyuko-sei **Dustwake Strict V05** | **9** | Approved WebPs read exactly from the documented conversation archives, reused without resizing/re-encoding. Archived proposal-wrapper names for BR033/BR040 do **not** make the exact, later director-accepted individual PNG/WebP pixels provisional; subsequent user acceptance is recorded in the owning QC records. |
| Three accepted Ethereal Monarch tier-geometry/appearance masters | BR-023 Ethereal Monarch | **3** | Approved exact RGB 1254px PNGs `bb3a…`, `97ac…`, `0e975…` converted via Pillow 1254→256 LANCZOS + VP8L lossless `exact=True`, **bitwise reproducing their historical accepted WebP SHA256s** `cf84d626...`, `c5032859...`, `99be189f...`. |
| **Total** | **9 families** | **27** | All originally approved pixels preserved or earlier approved encoded hashes exactly recovered. |

**Independent offline processing QC:** **459/459 explicit test assertions PASS, zero FAIL**. Included 5 archive SHA-256 matches, exact Wave05 ledger hash/membership, WebP decode/mode/256²/VP8L checks, opaque near-black corners, <460,800-byte working reference cap, no filename duplicates, all raw/processed Ethereal exact SHA and pixel decode equivalence, approved wave06 raw/candidate file SHA, all zip-member byte-equality/CRC checks, provisional Blackwire crop source preservation. The deterministic ZIP builder was run **twice**; each delivery SHA remained identical.

### Portable outputs

| Conversation delivery | SHA-256 | Contents |
|---|---|---|
| `Bloodright_27_Approved_Original_WebPs_256px_20261018.zip` | **`a941e28898ecff609d35f2361f1c251933c2d9eeb094d1e73190cb8c7f81f6c0`** | **Flat 27 separate, original named, approved 256×256 lossless VP8L files**. No remaster, no reimagined sheet, no duplicate, no Itojinsei V01. |
| `Bloodright_27_Approved_Original_SizePass_Archive_with_QC_20261018.zip` | **`280ac6a5e950adfe90eea0f08123f88ccb2b2141198ca9a1a64e6a0e4712ae8d`** | 27 identical originals, 3 exact approved Ethereal 1254px PNG masters, all 87 slot statuses with exact 27 WebP hashes and full source parent SHA, QC gallery, readme. |
| `BR-036_Itojinsei_Blackwire_3_Separated_REVIEW_ONLY_20261018.zip` | **`42d94702cc75d4b33f351f2f3a43d8eac0b5296b5d7275841320f26360d73f17`** | One unmodified accepted Blackwire 1254px triple-source composite + **three strictly crop/pad/resize-derived individual 256px VP8L files** and review composite + crop coordinates. The director accepted the **single original sheet**, NOT these individual exports. Exact approved geometry-master preservation **has NOT been verified** for Blackwire; do not include these in approved 27 pack or wire to the game without separate acceptance. |

## Missing exact original approved bytes — 57/87

There are **19 previously visually approved families** whose individual approved full-resolution PNG / 256px WebP source bytes are **absent** from the current conversation artifacts and repository. They are represented by SHA/document metadata only. Their original Wave01/02/03/04 art cannot be faithfully regenerated from text, prior collage, archived screenshots, unrelated references or their original jutsu art.

**Needed from director's original approved archives** (batch-friendly):
1. First/pilot family approved exports for BR-011 **Blood-Enchanted Eyes**, BR-015 **Blue Blade Eyes**, BR-075 **Taiyo Kami**, BR-029 **Godstorm Eclipse**. BR-023 Ethereal Monarch is **already recovered** and need not be re-uploaded.
2. `Bloodright_Wave02_Approved_15_WebPs_256px_RoleSwap_v02.zip` expected SHA-256 **`6a04203df4d35a2c86db550014c809dfcdd1d01cf296a4578485e5a81b2b5f4a`** (BR-067, BR-018, BR-027, BR-051, BR-059; **15 icons**).
3. `Bloodright_Wave03_Approved_15_WebPs_256px_20261017.zip` expected SHA-256 **`d31ffd49acdfac9702210b9cac321f91569697649be90962155297435f82d1fd`** (BR-083, BR-064, BR-020, BR-074, BR-090; **15 icons**).
4. `Bloodright_Wave04_Approved_15_WebPs_256px_20261017.zip` expected SHA-256 **`7270fa9bd79f4171724031207fd3b3d84eb0057322875a9e8c1824f4aa093d51`** (BR-066, BR-008, BR-053, BR-063, BR-032; **15 icons**).

The expected SHA values and status are from `BLOODRIGHT_WAVE02_ART_QC_20261017.json`, `BLOODRIGHT_WAVE03_APPROVED_QC_20261017.json`, `BLOODRIGHT_WAVE04_APPROVED_QC_20261017.json`, Ethereal/BBE/BEE QC, and exact starter metadata on the art lineage. **Wave02 BR-067 Shiroi Youso's tier mapping is ALREADY director-resolved**: `BLOODRIGHT_WAVE02_BR067_ROLE_SWAP_20261017.json` owns the accepted Hidden/Advanced role swap with artwork bytes unchanged. Use only the corrected Wave02 `RoleSwap_v02` archive named above. The earlier Wave02 art-QC file retains its historical pre-correction open status; it does not supersede the later director ruling.

With these 57 exact WebPs recovered and verified, the approved standalone icon bytes would total **84/87**. The final three **Itojinsei Blackwire** per-tier assets still need the distinct composite→individual geometry/export acceptance resolution. The director has visually accepted all **87 tier designs** across 29 families, but presently only 84 individually approved artworks exist in the records (27 now verified accessible, 57 existing elsewhere), plus the three one-sheet Itojinsei designs.

## Branch/workflow/readiness boundaries

- This branch is **an art processing/provenance record**, not a modified Fable implementation branch and not permission to merge; the inherited art lineage has a **RUL-2026-10-17-004 ID collision** with `main`'s separate placeholder-element import ruling, requiring reconciliation before merging.
- Formal **`skillTree.image` field-specific alpha/codec/upload preflight remains blocked/unverified** even though these 27 are size/format/SHA verified and the 3 Ethereal outputs reproduce exact historical accepted hashes. This is an Fable tooling/source-review gate, not an art-direction waiver.
- **Game reads 0; game writes 0; uploads 0; credentials none**. User remains sole live-game operator.
- New visual style-generation batch `chatgpt/bloodright-pixelart-wave01-20261018` is not accepted as replacement and must not feed this package.
- **Next:** Director supplies the missing earlier accepted WebP ZIPs (4 early-family exports + 3 multi-family waves). ChatGPT validates actual source hash/CRC and appends **bytes unchanged** until 84/87 individual assets are consolidated; retain Ito Blackwire separately pending geometry/standalone approval. Then Fable resolves actual field-specific image preflight/Forge binding; only the user performs any live import.
