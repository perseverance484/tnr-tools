# Bloodline Jutsu Icon Art Studio — ZIP-first production workflow

**Status:** DIRECTOR-DIRECTED STANDARD, 2026-10-17; approved workflow consolidation and latency optimization, NOT a claim that a new batch CLI already exists.
**Lead:** ChatGPT Art Director, Image Production for processing; **Fable / Claude Code:** normal owner of executable tooling, tests, schema/Forge changes.
**Scope:** individual, technique-specific **jutsu.image** replacement illustrations. **NOT** the three fixed Foundation / Hidden Art / Advanced Art Bloodright tier emblems.
**Routing and authority:** docs/00_INDEX.md; docs/DOCTRINE.md; docs/workflows/ART_PRODUCTION.md and ISOLATED_ART_GENERATION.md; docs/workflows/JUTSU_ICON_SHOWCASE.md for family review; skills/producing-tnr-art/SKILL.md and its LIVE 25x_DATA_art_spec.json for image contract. This document specializes *intake, studio flow and time-cost control*; it does not override the shared art protocol, skill numeric spec or director decisions.
**Decision history:** RUL-2026-10-14-001 (designed jutsu backgrounds); RUL-2026-10-17-020 on this branch (ZIP-first studio and speed-oriented review batching).
**Proven precedents (historical pinned evidence, not guaranteed live-art availability):**
- BBE: chatgpt/bbe-final-export-closeout-20261017@e5aa3b13eb4896e93b3e85799b8f0ec2eaedeb9f — eight current director-approved raws/exports and strict BBE-only under-80,000-byte cap; documentation PR #41 was OPEN at intake, final binaries in conversation exports, official preflight not run.
- BEE: chatgpt/bee-jutsu-art-studio-20261014@1f6010be0967d1ed42645a1a7476b8a1ec2a75e2 — eight current approved raws/exports including replaced Sanguine skull and Unholy veins; 74 local validation checks reported; preflight not run.
- Vaporia: chatgpt/vaporia-jutsu-art-studio-20261015@730f5393d4428282402f5f66ef2aeea3d156e405 — five current approved raws/exports; 3+2 deterministic gallery built, but separate final family/gallery signoff unproven in that historical closeout. Its legacy “generic ICON alpha blocked” comment is superseded by integrated JUTSU_ICON tooling; official preflight still not run.
See docs/design/jutsu_icon_studio/THREE_FAMILY_RECONCILIATION_20261017.md for the complete evidence boundary.

## 1. Operator contract — start with ONE prompt + ONE art ZIP

The user opens a fresh **persistent bloodline Art Studio** conversation and supplies:
- the concise, copy-ready prompt in docs/design/jutsu_icon_studio/START_PROMPT.md;
- ONE bloodline original-art ZIP, optionally containing manifest.json, original game jutsu icon images and a bloodline identity image.

Do **not** require screenshots, individual jutsu attachments, a master Bloodright library, a fresh Forge capture, or a separate style-choice questionnaire when the ZIP already contains the needed evidence. The ZIP is the **source-intake package**, NOT a direct reference to a generator. When a targeted isolated generation begins, pass the chosen **one or two extracted individual image files** explicitly.

A ZIP may be well-structured or a legacy collection of loosely named originals. For structured files, recognize:
- bloodline ID/name/rank where present;
- exact jutsu IDs/names/types and their original art member paths;
- optional immutable source capture URL/SHA evidence;
- optional identity/reference art and any previous accepted raw or output images.

**No guessed identity mapping.** Jutsu count N comes from the exact director-provided roster plus an identifiable capture/pinned kit, **not from rank or ZIP filename**. Include SPECIAL-owned bloodline techniques when their ownership is source-supported. If member path/name order cannot reliably match a jutsu ID, mark those rows MAPPING_REQUIRED and request only the missing mapping; do not invent a match or quietly discard assets. A manifest's claim about current live state is not a live capture.

**ZIP safety and provenance:** verify the archive itself and each entry; bound count, total expanded bytes and per-member size, reject traversal/absolute paths, symlinks, duplicate/case-colliding names and ZIP-bomb expansion. Decode actual MIME instead of trusting suffixes (BBE/BEE have JPEG bytes in .png-named uploads). Compare SHA-256, file lengths and image dimensions against any provided manifest, and mark unsupported/unverified fields explicitly. Keep the exact original bytes. If ZIP intake fails, do not generate.

## 2. Fast bootstrap — mandatory authority, minimum round trips

The speed optimization is **fewer sequential tool calls, fewer repeated repository reads and fewer chat turns**, NOT skipping authority/provenance checks.

**Cold start, once per bloodline:**
1. Verify live main, the intended art branch and frozen SHA. In **one batched/parallel repository retrieval where possible**, read state/active-context.md, state/status.json, docs/00_INDEX.md, docs/RULINGS.md, CHATGPT.md, docs/DEVELOPMENT_WORKFLOW.md, docs/agents/README.md, the two Art Director/Image Production roles, docs/workflows/ART_PRODUCTION.md, ISOLATED_ART_GENERATION.md and this document. Read current art skill + SPEC's JUTSU_ICON block, relevant old collection/pinned kit only as necessary. A fetch/parse error stays visible; do not proceed by replacing it with memory.
2. In **one local ZIP scan**, collect safe entry names, counts, decoded formats, bytes, hashes, supplied ID/name mappings and any missing/ambiguous entries. Build ONE compact image index; inspect that index for orientation, then open **2–4 selected individual original icons** and identity art where supplied to actually establish the family palette/material. Do not give a contact sheet to the generator as subject reference. **This step is one command** (§8): `jutsu_studio.py intake <ZIP> --out <dir> [--roster <file>]` writes `intake_report.md` (the one table), `source_index.json`, `studio_ledger.json`, `approved_template.json`, the exact original bytes under `originals/` and a studio-only `orientation_index.png`, and lists the pinned style exemplars with their reserved silhouettes.
3. Return ONE compact studio intake message: verified name/ID/rank/N, source-evidence level, any exact mapping questions, a **single family visual-treatment card** and a proposed **N-row technique-first silhouette ledger**, with one distinct primary shape/gesture per jutsu, and the first isolated target.
4. Director settles the family direction and disputed silhouette allocations **once** before individual generation. Do not require N separate generic palette discussions.

**Warm turns:** reuse the already-read document hashes, extracted reference index and director-approved family card in the same studio. Re-fetch only for a relevant SHA change, a newly exposed source disagreement, a new issue or the next major production phase. Never claim a stale ref is “current”; check current main on substantial milestones. No repository commit per proposed image/candidate; make durable register updates at meaningful direction/approval/closeout checkpoints.

**Performance visibility:** separately record cold-bootstrap retrieval time, ZIP scan/inspection, human direction iteration, image-generation wait, export/QC and repository delivery time. The previously observed 8–10-minute Bloodright turns have **not been profiled**; it would be misleading to promise a particular generation duration. This design minimizes overhead and defers nonessential tasks, while image-generation service latency remains externally variable.

## 3. Locked visual quality — family style, individually unique technique

- **Technique first:** depict what the jutsu actually does, based on supplied exact record/mechanics; the old icon is *identity/history*, not necessarily the desired new composition. Actors/hands/weapons appear only when genuinely necessary to convey that jutsu and after director acceptance.
- **Thumbnail-first silhouette:** one unmistakable action/formation, one supporting effect, decisive focal hierarchy and dark/light separation readable at 125/64/32. No repeating generic chakra rings, mandatory symmetrical mandalas, random rubble/explosions, vague energy blobs, lookalike slashes or dense noise that makes techniques indistinct.
- **Shared rendering, NOT shared composition:** choose palette, chakra material, atmosphere, edge treatment and detail density from **actual observed reference pixels**. BBE uses icy translucent facets/precise silhouettes; BEE crimson-black broad supernatural shapes/negative space; Vaporia dimensional azure hydrothermal water and incandescent orange rupture. These are **examples of craft**, not palettes to copy into another bloodline.
- **Actual accepted art-style exemplars:** the new bloodline's legacy ZIP is the **subject/identity source**; the best new rendering reference is an individual, *director-approved revised jutsu icon*, labeled **STYLE/MATERIAL ONLY**. The **approved JUTSU_ICON style library is pinned** (RUL-2026-10-17-021): the 8 BBE and 8 BEE final exports, exact bytes under `art/style_refs/jutsu_icons/{bbe,bee}/`, indexed in `skills/producing-tnr-art/data/style_refs.json` with delivery provenance (`art/style_refs/jutsu_icons/INTAKE_20261017.json`). Select with `python3 skills/producing-tnr-art/scripts/style_refs.py select --target JUTSU_ICON [--family BBE|BEE] [--tag ...]`; `list --target JUTSU_ICON` shows every exemplar's **reserved silhouette** for the exclusion list. The operator does **not** upload a style ZIP per bloodline. Vaporia's finals are not yet pinned. **Do not claim model reference conditioning on bytes the generator never received:** a raw URL or path in a prompt is not an attached image, so fetch the exemplar file and attach it; if that is impossible in the session, say so and label the generation *style pixels not attached*.
- **Silhouette ownership ledger:** before generating, reserve the primary shape/axis of each jutsu and record conflicts. BEE's Ring spiral vs Unholy radial waves and Vaporia's dragon-like shapes are documented failure cases. If the director later changes one technique, revise its row and rerender only that jutsu, not the entire family.
- **Opaque designed backgrounds are approved for jutsu.image.** Rarity frame accommodation is not a visual requirement. Do not key out backgrounds or add artificial alpha. The JUTSU_ICON spec permits opaque RGB while item/bloodline ICON rules stay separate. No text, UI cards, labels, watermarks, franchise imagery or unrelated actors on a jutsu icon.

## 4. Focused image-generation loop (retain existing isolation protocol)

The Art Studio is **persistent coordination**, not a polluted multi-jutsu generator. It prepares a complete set of briefs before the first image, but image production follows docs/workflows/ISOLATED_ART_GENERATION.md:

1. For the next ONE jutsu, produce a compact approved brief: exact name/ID/effects where known, primary silhouette, motion, one supporting cue, family palette/material, reserved conflicting shapes, placement and exclusions. Select **at most two individual image references** by role: old jutsu icon (identity only), **actual approved current-family or pinned BBE/BEE/Vaporia exemplar bytes** (style/material only), or a true subject reference when needed. Prefer one legacy identity image + one approved-quality style example; neither may dictate a duplicate composition.
2. Open a **fresh isolated generation conversation for that one technique**. Attach the real selected image(s), not the ZIP, screenshots, metadata alone, or family sheet. One square icon candidate at a time. Revisions for the same subject remain in that thread; after two wrong-subject/composition failures, reset that isolated thread.
3. Director explicitly approves/rejects **the exact raw file**; preserve it and record its hash/actual decoder format. Back in the Studio, update its N-row register and only then move to another jutsu. The generation thread does **no** pack processing, repository guessing or game actions.

**Latency cut:** assemble the entire N-jutsu silhouette/exclusion register and per-icon isolated starter briefs **once** in the Studio. Do not reread all game/canon docs in every icon thread when a pinned, current per-icon brief covers them; each new thread still verifies its live main and applicable authority. Work with 1–2 targeted images, not all N imagery. No repeated scene setup after an icon is approved.

## 5. Fast, source-faithful processing/QC and package

**Do not process or fully preflight every rejected candidate.** Raw-format/rough thumbnail rejection happens immediately; costly codec processing happens after exact visual approval and preferably as **one local batch per completed family**.

When the family has N/N exact raw approvals:
1. Verify all exact current raw hashes/IDs and decode formats. Preserve them **unaltered** in a source archive. Do not reuse rejected, withdrawn or earlier gallery files.
2. Export N files **once**, with a consistent logged processor: approved square originals → Pillow LANCZOS to the current spec's recommended **256×256** → opaque RGB **lossless WebP VP8L**, without chroma key. Verify actual codec, decoded dimensions, working upload cap (currently **460,800 B**, 512KiB hard cap), per-file SHA and decoded source→export pixel equality. A specific family may impose a **stricter** cap; for BBE this was *under 80,000 B*. Never copy that restriction to BEE/Vaporia automatically.
3. **Quantization is an exception, not universal:** BBE used <=256-color adaptive MEDIANCUT and lossless WebP to stay under its 80,000-byte cap. BEE/Vaporia did not need this. If a strict cap forces a visually material quality change, show director the actual 125/64/32 comparison for explicit approval, then record the chosen transform. A VP8L container is lossless *relative to the processed pixels*, not necessarily faithful to an unquantized raw.
4. Run the **actual** canonical preflight **once on the finished output directory**, passing `--type JUTSU_ICON` explicitly and `--max-bytes N` only when approved. Write the command, exact spec SHA, stdout/stderr and exit code into the QC record. Don't label local equivalent checks or preflight code inspection as an actual PASS; if the script isn't available, report NOT_RUN, not BLOCKED by legacy generic ICON alpha.
5. Render all N exact saved WebPs at 125/64/32, inspect family confusion, then create **one deterministic adaptive N-icon family showcase**, with exact display names and **real export bytes/1000 decimal kB** captions. Use docs/workflows/JUTSU_ICON_SHOWCASE.md. The compositor may enlarge tiles for display but must not generate, retouch, recolor or replace original game icon pixels. Director explicitly signs off on **the family** after reviewing the final compiled sheet; 5/5 raw approvals alone are not that signoff.
6. Create a **single full closeout ZIP** (approved raw originals, exports, jutsu-ID manifest, QC/preflight, showcase, thumbnail preview and SHA256SUMS) and optionally a small, flat **N-WebP upload ZIP** for mobile use. Stable versioned filenames; verify ZIP CRC, members, cross-file hash equality and safe extraction. Never confuse the showcase file with a game `@img` asset.

**Batch utility status:** steps 1–6 are **one command**, `jutsu_studio.py finalize approved.json --out <dir> [--label vN] [--source-index <intake>/source_index.json]` (§8). It refuses unapproved, superseded or hash-mismatched raws and any silent omission against the intake roster; exports with the logged Pillow LANCZOS → lossless VP8L processor (it reproduced all 8 BEE closeout exports byte-for-byte); applies median-cut **only** where approved.json records the director's approval for that icon; runs the **real** `artpreflight.py --type JUTSU_ICON` (`--max-bytes` only with a recorded family-cap ruling) and records command/exit/stdout; builds the count-adaptive showcase from the saved WebPs with a per-tile pixel-equality assertion; and writes the closeout ZIP plus a flat upload ZIP. Fable owns the code (Lane A); flags beyond those in `--help` do not exist.

## 6. Evidence and gate ledger (never blend statuses)

Track these separately per jutsu or collection:
- ZIP_RECEIVED → SOURCE_DECODE/HASH_VERIFIED → JUTSU_ID_MAPPING_VERIFIED → DIRECTION_APPROVED → RAW_VISUAL_APPROVED → OUTPUT_FILE_QC_PASS → CANONICAL_PREFLIGHT_PASS/FAIL/NOT_RUN → FAMILY_SHOWCASE_ACCEPTED → ARCHIVE_DELIVERED → GIT_BYTES_PINNED (if performed) → USER_UPLOAD/READBACK (if independently proven).

A director closeout instruction can end a Studio **without** claiming an unaccepted final gallery, as Vaporia demonstrated. A final montage created after a director approved an earlier set also does not automatically inherit approval of its exact new pixels (BEE). A prompt, hash, external URL or a JPEG re-encoded showcase is **not** proof of byte-equivalent raw art.

No studio role uploads icons, updates jutsu records, or publishes to the production game. Fable builds technical tooling and content bindings under the repository's one-writer rules. User owns live actions and any explicit new art decisions.

## 7. Operational quick-reference / minimal new-session reply

The first startup response should be **ONE compact table** of verified jutsu names/IDs ↔ ZIP entry with mismatches marked, followed by ONE family treatment card, ONE proposed technique-silhouette ledger and the next single generation target. If everything necessary is supplied in the ZIP, do not request redundant images. If some critical source is missing, name exactly the missing field/member and continue with safe visual work only.

Before closing: give the user final ZIP download(s), one clear accepted/not-run gate summary and **one compact fenced handoff at the very end**. Never turn a jutsu Art Studio closeout into a Bloodright tier-emblem reskin, an unrequested Houkyuken initialization, or a live-game action.

**Tooling brief:** state/prompt_jutsu_icon_studio_fast_tooling_20261017.md, implemented by §8. Timings it reports cover the deterministic steps only, never image-generation latency.

## 8. Commands (skills/producing-tnr-art/scripts/)

The tools need Python 3 + Pillow and the `skills/producing-tnr-art/` layout (`scripts/` beside `data/`); the installed producing-tnr-art skill ZIP carries it. In a sandbox without the skill, fetch `scripts/jutsu_studio.py`, `scripts/style_refs.py`, `scripts/artpreflight.py`, `data/25x_DATA_art_spec.json` and `data/style_refs.json` into that same layout. No network, game access or credentials are used.

~~~text
# cold start - one ZIP, one command (exit 0 mapped | 3 MAPPING_REQUIRED/roster needed | 1 refused)
python3 jutsu_studio.py intake PACK.zip --out work/intake [--roster roster.csv] [--ref <git ref for exemplar URLs>]

# style exemplars to attach (STYLE/MATERIAL ONLY; one per generation by default)
python3 style_refs.py select --target JUTSU_ICON [--family BBE|BEE] [--ref <git ref>]

# after N/N director raw approvals are written into approved.json (from approved_template.json)
python3 jutsu_studio.py verify-approved work/approved.json --source-index work/intake/source_index.json
python3 jutsu_studio.py finalize work/approved.json --out work/final --label v1 --source-index work/intake/source_index.json
~~~

- **Roster:** a structured pack's `manifest.json` (`bloodline{id,name,rank}`, `jutsu[{jutsu_id,name,file,sha256?}]`, optional `identity{file,sha256?}`) is read directly. A loose pack needs `--roster` (JSON of the same shape, or CSV `jutsu_id,name[,file]`); files then map only by **exact normalized name** (an `icon_<family>_<slug>_vN` prefix/suffix is understood), and every other row is `MAPPING_REQUIRED`. A roster that disagrees with the manifest is a conflict, never merged.
- **approved.json** is written by the Studio, never inferred from chat: per jutsu `raw_file` + `raw_sha256`, `director_raw_approval {status: APPROVED, evidence}`, `version` (bump it when an approved raw is replaced and list the old hash in `superseded_raw_sha256`), optional `quantize {method: MEDIANCUT, colors, director_approved}`; per family optional `family_byte_cap_exclusive` + `family_byte_cap_ruling`, and `family_acceptance {status, evidence}`, which stays PENDING until the director accepts the compiled showcase.
- **Reruns** are incremental: unchanged approved raws reuse their cached exports; a changed raw under the same version, a tampered export, or an archive label reused for different contents is refused, and earlier exports/archives are never overwritten. Use a new `--label` for each delivered set.
- **Until this tooling is on `main`,** fetch it, and pass `--ref`, from the integration branch named in START_PROMPT.md.
