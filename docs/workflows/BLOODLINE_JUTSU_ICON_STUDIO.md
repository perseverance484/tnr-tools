# Bloodline Jutsu Icon Art Studio — ZIP-first production workflow

**Status:** ACTIVE specialised workflow. Director-directed 2026-10-17 (RUL-2026-10-17-020); brought to `main` under RUL-2026-10-19-005 D4. P1 Option B executable tooling was integrated independently in PR #66 (2026-10-19).
**Lead:** Art Director; support: Image Production. Fable / Claude Code owns executable tooling, tests and skill changes.
**Scope:** individual technique-specific `jutsu.image` redesigns, **not** the three fixed Bloodright Foundation / Hidden Art / Advanced Art tier emblems.
**Authority:** `docs/00_INDEX.md` arbitrates; `docs/workflows/ART_PRODUCTION.md` routes; **`docs/workflows/ISOLATED_ART_GENERATION.md` is the operative P0 A–F generation and deterministic-gallery protocol (RUL-2026-10-19-003)**. This document only specialises ZIP intake, studio coordination and time-cost control. `docs/workflows/JUTSU_ICON_SHOWCASE.md` describes the presentation mechanics under P0 §4a. The current `skills/producing-tnr-art/SKILL.md` and `data/25x_DATA_art_spec.json` own executable/numerical art requirements.
**Rulings:** RUL-2026-10-14-001 (designed backgrounds), RUL-2026-10-17-020 (ZIP-first), RUL-2026-10-17-021 (BBE/BEE exemplars), RUL-2026-10-19-003 (P0), RUL-2026-10-19-005 (P1 Option B, D1–D10).

**Historical precedents, not current-live proof:** BBE `chatgpt/bbe-final-export-closeout-20261017@e5aa3b13eb4896e93b3e85799b8f0ec2eaedeb9f` (8 raws/exports, BBE-specific under-80,000-byte cap); BEE `chatgpt/bee-jutsu-art-studio-20261014@1f6010be0967d1ed42645a1a7476b8a1ec2a75e2` (8 visually approved raws/exports; skull and vein revisions); Vaporia `chatgpt/vaporia-jutsu-art-studio-20261015@730f5393d4428282402f5f66ef2aeea3d156e405` (5/5 raw approvals, deterministic 3+2 sheet, exact sheet signoff not established). Read `docs/design/jutsu_icon_studio/THREE_FAMILY_RECONCILIATION_20261017.md` for their evidence boundaries. Original raw archives and completed production acceptance are **not** implied by the now-pinned style WebPs.

## 1. Operator contract — one prompt + one original-art ZIP

The user opens a persistent bloodline **Art Studio** conversation with the compact `docs/design/jutsu_icon_studio/START_PROMPT.md` and **one original bloodline jutsu-art ZIP**. If the ZIP already carries source imagery, IDs and names, do not ask for individual screenshots or another art pack. The ZIP is a **source-intake package**, never a generator reference: isolated generation receives at most two actual, individually attached images with explicitly labelled roles.

Recognise a structured `manifest.json` or loosely named legacy originals. Capture source-provided bloodline ID/name/rank, exact jutsu ID/name/type, image member path, optional raw file/version, and any capture provenance. **N is the verified/director-supplied roster, not an assumption from rank or ZIP file count.** Include source-supported bloodline-owned SPECIAL techniques. Any ambiguous member/ID match is `MAPPING_REQUIRED`; request only the missing mapping, never guess. A historical manifest is not a current-live check.

Use the repo CLI's bounded ZIP intake, actual decoder (including JPEG-bytes-in-`.png` cases), SHA-256, CRC, size and safety checks. Refuse path traversal, symlinks, name collisions, ZIP bombs or missing/mismatched source entries; preserve the original bytes. If intake fails, do not generate.

## 2. Fast bootstrap — verify once, batch what is safe

Efficiency means **fewer repository requests and repeated turns**, not skipped evidence or less careful images.

1. Verify live `main`, studio branch/exact SHA if present; read `state/active-context.md`, `state/status.json`, `docs/00_INDEX.md`, `docs/RULINGS.md`, `CHATGPT.md`, `docs/DEVELOPMENT_WORKFLOW.md`, `docs/agents/README.md`, Art Director and Image Production roles, `docs/workflows/ART_PRODUCTION.md`, the operative `ISOLATED_ART_GENERATION.md`, this workflow, the art skill/spec, and the target's register/pinned kit where necessary. Batch independent reads. A fetch failure stays explicit.
2. Use the current `jutsu_studio.py doctor` before relying on canonical preflight in this runtime; it tests a *synthetic* file and does not certify any particular family's exports. Run **one** local `jutsu_studio.py intake PACK.zip --out WORK/intake [--roster roster.json|.csv]`. It emits `source_index.json`, `intake_report.md`, `studio_ledger.json`, `approved_template.json` and, when imagery permits, `orientation_index.png`.
3. Inspect that studio-only orientation index, plus 2–4 **individual** extracted originals and identity art to establish actually observed family material/color. **Never attach the index/contact sheet to a generator.** Return a compact verified ID/name/ZIP-member inventory, evidence-level/mapping gaps, **one** family visual-treatment card, and an N-row technique-first **silhouette/action reservation ledger** with the next target.
4. Director settles the family card and disputed silhouette allocations once, before per-jutsu generation. No extra style-choice questionnaire when evidence and approved direction already settle it.

Warm turns reuse the pinned source/asset index and family decision; re-fetch relevant current refs at major milestones or when a source conflict appears. Save durable register checkpoints at direction/approval/closeout, rather than committing every rejected candidate. Record bootstrap, ZIP, generation-wait (only if measured), export/QC, gallery and delivery timings separately. The previously reported 8–10-minute chat turns were **not** profiled as generator latency; CLI speedups measure only deterministic local work.

## 3. Visual direction, references and target lock

**The operative art gates are in `ISOLATED_ART_GENERATION.md` §§2–3.** Apply its immutable bloodline/jutsu identity and action, camera/motion axis, singular dominant silhouette, sibling exclusions (**geometry and action, not color alone**), 125/64/32 visual check, default **no anatomy**, target-specific director-approved exceptions, working chakra geometry and returned-*pixel* fail-fast decision. P1 tooling records/checks the stated evidence; it does not classify visual correctness or inspect hidden image-generator prompts.

The old icon represents legacy **identity**, not mandatory composition. The family shares visual rendering/material, but each jutsu must have its own readable action and major silhouette. Historical examples: BBE crystal/ice facets and distinct sword, X-restraint and flake shapes; BEE crimson-black negative-space silhouettes including skull and veins; Vaporia turquoise hydrothermal water/incandescent rupture. These calibrate craft rather than impose a palette on future families.

**Pinned style exemplars (now on `main`):** PR #66 and RUL-2026-10-17-021 pin **16 BBE/BEE JUTSU_ICON WebPs** in `art/style_refs/jutsu_icons/`, indexed by `skills/producing-tnr-art/data/style_refs.json`. `style_refs.py select --target JUTSU_ICON [--family BBE|BEE]` selects candidates for **STYLE/MATERIAL ONLY** alongside one source identity icon; never copy exemplar silhouette/action into the new family. `icon_bee_sanguine_plague_v3.webp` is explicitly `PROVENANCE_PARTIAL` (the closeout-approved raw/version was not proven). **Vaporia finals are not Git-pinned.** The image model must receive actual individual image bytes, not merely a Git path/URL/hash. If bytes cannot be attached, say so.

## 4. Isolated generation loop — P0 first

The persistent Studio plans the family. For **each** target it maintains `tnr.jutsu-studio.locks/1` records with exact bloodline and jutsu IDs/name, source evidence level, action, dominant silhouette, camera, motion axis, one secondary effect, every sibling reserved silhouette/action, reference roles, anatomy exception (when separately approved), and a director `direction_approval` bound to `lock_sha256`. `lock-check` catches incomplete/contradictory data; it does not prove a generated image is the right technique.

Start a **new isolated conversation for that one jutsu** with a focused brief and only the individual target identity image plus at most one approved style/material exemplar. Generate one candidate; visually inspect the actual pixels against P0 and use `compare` at 125/64/32 before director review as needed. On two wrong-target/composition failures in one conversation, restart clean as P0 requires—not with rejected images as new positive conditioning.

Record outcomes in `tnr.jutsu-studio.attempts/1` with ordered attempts, `session_id`, candidate SHA (required for approval), reasons, role-labeled references, actual measured wait if present, and explicit director decision. `attempts --locks` refuses reused cross-jutsu sessions, rejected conditioning, anatomically unauthorized approval, and a third candidate after the two-failure restart trigger. Finalization requires **terminal approved attempts** equal to each exact accepted raw when an attempts record is supplied. Transfer accepted original source bytes back to Studio; the isolated thread does not process exports, make a family collage or contact the game.

## 5. Batch processing, canonical checks and deterministic gallery

**Executable CLI (P1 Option B, PR #66):** `skills/producing-tnr-art/scripts/jutsu_studio.py`; `skills/producing-tnr-art/SKILL.md` contains its shipped command row; `state/prompt_jutsu_icon_p1_tooling_20261019.md` is the build contract. Consult `jutsu_studio.py <command> --help` for any additional flags. From repository root, substituting your own actual paths:

~~~sh
python3 skills/producing-tnr-art/scripts/jutsu_studio.py doctor
python3 skills/producing-tnr-art/scripts/jutsu_studio.py intake PACK.zip --out WORK/intake
# For loose/missing identity mapping add --roster roster.json (or roster.csv).
python3 skills/producing-tnr-art/scripts/jutsu_studio.py lock-check WORK/locks.json --source-index WORK/intake/source_index.json
python3 skills/producing-tnr-art/scripts/jutsu_studio.py attempts WORK/attempts.json --locks WORK/locks.json
python3 skills/producing-tnr-art/scripts/jutsu_studio.py compare CANDIDATE.png FAMILY1.webp --out WORK/compare --label c1
python3 skills/producing-tnr-art/scripts/jutsu_studio.py verify-approved WORK/approved.json --source-index WORK/intake/source_index.json --locks WORK/locks.json --attempts WORK/attempts.json
python3 skills/producing-tnr-art/scripts/jutsu_studio.py finalize WORK/approved.json --out WORK/final --label v1 --source-index WORK/intake/source_index.json --locks WORK/locks.json --attempts WORK/attempts.json
python3 skills/producing-tnr-art/scripts/jutsu_studio.py audit-gallery WORK/final/showcase/<family>_jutsu_showcase_v1.png --manifest WORK/final/showcase/showcase_manifest.json --exports WORK/final/exports
~~~

Only after **N/N exact director-approved raws**: `verify-approved` checks identities/hashes and binds optional lock/attempt records; `finalize` caches/export-verifies opaque square RGB lossless VP8L WebPs, runs actual `artpreflight.py --type JUTSU_ICON`, composites a source-faithful full family gallery (and phone/125-64-32 previews), audits its decoded pixels and sealed members, and packages a versioned closeout with SHA256SUMS. It **refuses incomplete family export**, rather than implementing the optional DRAFT partial-gallery mode (Option C not approved). Do not process every rejected candidate. Quantization is an individual explicit director-approved quality tradeoff, **never** automatic. BBE's strict **under-80,000-byte** cap is BBE-specific, not a default for BEE/Vaporia. Numerical output rules come from the current art spec.

**Canonical preflight D9:** `doctor` gives environment capability only. The family's `finalize` must invoke the real preflight over current exported files; `data/preflight_pins.json` binds its script/spec Git blobs. `NOT_RUN` and `NON_CANONICAL` are **not PASS**, even if local QC is green. A correct `doctor` result does not retroactively certify any prior family's raw/export ZIP.

**Gallery acceptance recording (see operative P0 §4a):** after director acceptance of the **exact** `showcase_manifest.json` gallery, copy `gallery.sha256`, optionally `gallery.pixels_sha256`, **and `members_sha256`** from that manifest into `approved.json.family_acceptance` with director evidence. Re-finalize under a **fresh label** so write-once archives do not collide. Prior acceptance becomes `INVALIDATED` after **any approved raw/export byte change**, even a pixel-identical re-encoding. `JUTSU_ICON_SHOWCASE.md` explains the deterministic QC/audit work mode, not an independent acceptance authority.

**D6 archive names:** full `<fam>_jutsu_icons_closeout_<label>.zip`; flat phone-friendly WebPs `<fam>_jutsu_icons_webps_PREFLIGHT_<PASS|FAIL|NOT_RUN|NON_CANONICAL>_<N>webp_<label>.zip` (the word `upload` is never used). A generated archive is not upload-ready when canonical preflight is not PASS. No game upload/publishing code exists in this CLI.

## 6. Evidence ledger (P1/K names)

Record these **separately per icon and per collection**: `ORIGINAL_SOURCE_VERIFIED`, `DIRECTION_APPROVED`, `RAW_VISUAL_APPROVED`, `OUTPUT_LOCAL_QC`, `CANONICAL_PREFLIGHT`, `FAMILY_SHOWCASE_ACCEPTED`, `ZIP_DELIVERED`, `GIT_BINARY_PIN`, `USER_UPLOAD_READBACK`. These are the *implemented P1 K names* under RUL-2026-10-19-005 D7; do not use obsolete `OUTPUT_FILE_QC_PASS`, `GIT_BYTES_PINNED` or an inferred linear status. `BUILT_NOT_DELIVERED` is not user delivery. The tool cannot mark Git binary pinning or user upload/readback as performed.

The director can close a studio while gallery acceptance is **PENDING**. Gallery acceptance is separate from raw approvals, local QC, canonical preflight, Git pinning and user-controlled upload/readback. Historical BEE/Vaporia closeouts demonstrate why these statuses cannot be blended.

## 7. First and final messages

The first response is **one compact exact name/ID/source-member inventory**, any explicit mapping gaps, one family treatment card, one N-row reserved technique/silhouette ledger and the first isolated target. Avoid redundant ZIP/screenshot requests when evidence already exists.

The closeout returns actual working ZIP links when produced, recorded preflight/acceptance status and **one fielded fenced handoff at the very end**. Never turn jutsu icons into fixed Bloodright emblems or perform live-game actions.

**Historical (not queued):** the original P1 sketch `state/prompt_jutsu_icon_studio_fast_tooling_20261017.md` remains at `chatgpt/bloodline-jutsu-studio-zip-first-20261017@d04a87c05999c7037af8667db2b2b79324a53d3c`. It is **SUPERSEDED by reviewed P1 Option B tooling, RUL-2026-10-19-005, `state/prompt_jutsu_icon_p1_tooling_20261019.md`, PR #66**. Do not treat its proposed future commands as an unstarted task.
