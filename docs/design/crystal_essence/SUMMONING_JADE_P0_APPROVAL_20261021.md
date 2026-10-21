# Crystal Essence — Summoning: Jade P0 director approval and technical gate

**Decision date:** 2026-10-21. **Status:** TARGET P0 **DIRECTOR APPROVED** / OFFICIAL **LOCK-CHECK PASS** / READY FOR ONE FRESH ISOLATED GENERATION. This is **not** acceptance of a generated Jade image.

## Approved source identity and art direction

- Bloodline: **Crystal Essence** (rank A), ID `ssevlOGQ4JjPn2sHZtq0c`, BR-020.
- Jutsu: **Summoning: Jade** (rank A), ID `yuJn_D_zPlHV0xJW01JRA`, type `BLOODLINE`, client `jutsu.image`, asset target `JUTSU_ICON`.
- **Director decision:** “Approved, proceed” in response to the exact Summoning: Jade draft P0, **studio prior head `b60b04ff281237f6dacbbe3e1ff9cba2489da5ee`**. The director approved an **actor-free** summoning event and its two separate reference roles. This does not authorize human anatomy or approve any generated candidate.
- **Source evidence:** committed historical read-only `jutsu.get` capture index 0, `harvests/inbox/tnr_results_1792216502874.json`, 2026-10-17; action: a crystal cocoon opens and summons a fierce warrior. No live-game refresh or requests.
- **Primary working geometry/action:** **one upright jade-green faceted crystal chrysalis splitting OUTWARD and UPWARD** from its center seam, two heavy shell panels creating an open V-shaped deep dark gap, concentrated gold-white emergence light within. Frontal shallow 3/4, center→upper-left and upper-right movement. One subordinate cue: the thick shell plates peel/break apart; no particle storm.
- **Distinctness exclusions:** Kōsai's three lateral curved waves; Sphere's round protective shell and impact deflection; Cave's opposing ceiling/floor jagged jaws converging INWARD; Prism's long focused diagonal attack beam. No actor/face/hand/limb/body, runes, magical sigils, decorative V emblem, or floating gems. **Anatomy exception: NONE.**
- **Rendering:** director-approved LUMINOUS SILICATE — WARM-CORE REFRACTION, premium crisp TNR pixel-cluster shading; specifically favor deep translucent jade-green with teal/cyan facet edges, restrained amber-gold light, navy-black designed background.

**Sealed immutable target lock SHA-256:** `cda3c005261226a355ad745534200b3596669b6993922c8dd9e1181b781d0358` (hash of canonical target record excluding direction-approval block). **Final Git locks file blob:** `d89496208992bcb865bb9cd78f1e25f742207911`, path `docs/design/crystal_essence/JUTSU_TARGET_LOCKS.json`.

## Actual individual references (MAXIMUM TWO in the generator)

1. **IDENTITY ONLY:** original PNG `Crystal_Essence_Summoning_Jade_ORIGINAL_IDENTITY_ONLY.png`, **PNG RGB 235×235**, **64,058 bytes**, SHA-256 `04422340d90c43d9dc3c60a0c454c094185e28a5d3820a0be6944d877c252a8a`. Its legacy human actor is *not* authorized to be copied.
2. **STYLE/MATERIAL ONLY:** director-approved Kōsai raw `Crystal_Essence_Kosai_Shippu_APPROVED_RAW_v1.jpg`, **JPEG RGB 1536×1536**, **628,679 bytes**, SHA-256 `84a523fbc5fab3e3eb6f43ff3bf88682643477cf54154d1e0bc3b151353f8ee5`. Reference crystal facets, pixel shading and light treatment, not traveling crescent waves.

Both files were loaded/decoded and SHA-256-verified byte-for-byte in the local Studio runtime. No ZIP, contact sheet, rejected art or additional sibling raw enters the isolated generator.

## Executed offline technical gates

- Official user-supplied `producing-tnr-art (3).zip`, SHA-256 `73dd4228131dc8cbf112fc89466160eb604857c856419db5e664bc516a0727ed`, matches Git art-skill bundle blob `746a4460b59bb8b805bdd64837f738b3618d0b82`; bounded, safe ZIP extraction and CRC checks passed.
- `jutsu_studio.py doctor` **exit 0**, `RUN_CAPABLE_CANONICAL`: Pillow 12.3.0, libwebp 1.6.0, VP8L round-trip, deterministic encoding, canonical spec/script pins and synthetic preflight probe PASS. This probe is not preflight of a real game-ready export.
- **One** official `jutsu_studio.py intake` of the unmodified original `BR-020_Crystal_Essence.zip`, SHA-256 `0a6acc8fb678b1030f1ada358b7fd522cf531b0dfb2f49f2bf0a0a969f5329af`: **exit 0**, original ZIP CRC OK, **5/5 MANIFEST_VERIFIED**, `mapping_complete=true`; generated local source-index SHA-256 `469a07aa25b5299af3aa5aff953c73b4dc173fe6f23605fb6787476c0ab30a39`. The source-index records historical capture provenance, not a current-live census.
- Independently retrieved exact approved Git `JUTSU_TARGET_LOCKS.json` content; local git-blob SHA **matches `d89496208992bcb865bb9cd78f1e25f742207911`**.
- Actual `python .../jutsu_studio.py lock-check JUTSU_TARGET_LOCKS.json --source-index intake/source_index.json`: **exit 0**, **5/5 DIRECTION_APPROVED**, all target lock hashes confirmed, no incomplete/mismatched rows. Four sibling locks unchanged by the Jade approval.

**Known mapping note:** Original ZIP manifest says `jutsu_type`; the current CLI source-index `type` field can be null. Exact BLOODLINE type is independently corroborated from original manifest and committed read-only `jutsu.get` capture; it is not invented from null.

## Remaining distinct gates

`ORIGINAL_SOURCE_VERIFIED`: **5/5**; `DIRECTION_APPROVED`: **5/5**; `RAW_VISUAL_APPROVED`: **4/5** (Kōsai, Crystal Sphere, Crystal Cave, Prism; Jade NOT YET GENERATED); `OUTPUT_LOCAL_QC`: NOT_RUN on processed family exports; `CANONICAL_PREFLIGHT`: NOT_RUN on real exports; `FAMILY_SHOWCASE_ACCEPTED`: PENDING; `ZIP_DELIVERED`: NOT_PERFORMED; `GIT_BINARY_PIN`: NOT_PERFORMED for original/approved raw bytes; `USER_UPLOAD_READBACK`: NOT_PERFORMED.

**Next:** Open ONE **separate fresh isolated Summoning: Jade generation** conversation, attach these two actual individual files, generate ONE icon candidate, P0 visually check returned pixels at 125/64/32 against the four approved siblings, and request separate director raw acceptance. Persistent Studio must not generate/retouch/process while initializing/briefing.

**Live-game requests/writes:** 0/0. **Credentials:** none.
