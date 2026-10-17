# Fable Implementation Brief — Fast ZIP-first Jutsu Icon Studio Tooling

**Status:** FABLE IMPLEMENTATION QUEUED; director requested faster jutsu Art Studio startup and processing. This is a tooling **brief**, not implemented code. Art-workflow owner: docs/workflows/BLOODLINE_JUTSU_ICON_STUDIO.md. Batch-showcase owner: docs/workflows/JUTSU_ICON_SHOWCASE.md.
**Repository verified base:** main@9a0970002a80531078ac5e4b0f72578d3f7855f5 (2026-10-17; refresh before implementation). **Review:** independent ChatGPT at frozen exact Fable SHA.
**Lane A owner:** Fable/Claude Code on dedicated implementation branch only; preserve one-writer rules.
**No game source/network or credential access authorized.** Browser/game uploads remain operator-only.

## Problem / quality goals

The director reports Bloodright image turns can take **8–10 minutes**, but no timing trace currently distinguishes tool-call overhead, image generation service wait, ZIP processing and repository writes. **Do not claim the tool reduces model generation latency.** Reduce operator work to **one prompt + one existing original-jutsu-art ZIP**, one batched read/intake, compact first report, prebuilt per-jutsu isolated briefs, and **one family-level processing/preflight/showcase pass** after director raw approvals.

Maintain the current strong invariants:
- existing JUTSU_ICON image target (jutsu.image), optional alpha with designed opaque background;
- one dominant technique-specific shape per jutsu; no automatic generative sheets;
- family N from exact IDs/verified roster, not rank; extra/missing/misidentified art fails explicitly;
- BBE under 80,000 bytes is collection-specific, not global;
- no raw art changes after director acceptance; no invented source-game facts or live updates;
- separate RAW_VISUAL, FAMILY_APPROVED, EXPORT_QC, CANONICAL_PREFLIGHT, BINARIES_PINNED, LIVE_READBACK statuses.

## Minimal implementation (one CLI, no UI/Forge features)

Implement reusable **offline** utility at an appropriate repository skill/script path (Fable chooses placement) with these functions or equivalent subcommands:

1. **intake:** safe ZIP enumeration and bounded extraction; recognize existing BR-style art-pack manifest.json (`bloodline`, `jutsu[]` with `jutsu_id`, `name`, `file`, `sha256`, optional `identity`) and loose packs; decode true MIME with Pillow, collect SHA/bytes/dimensions and exact jutsu-ID mapping evidence. Emit small normalized `source_index.json` and friendly `intake_report.md` (one table). For unresolved ID mapping emit `MAPPING_REQUIRED` and exact names/paths, not a fabricated complete scan.
2. **verify-approved:** read a per-family approved raw ledger provided by Art Studio, assert exact current approved source hashes/IDs, no superseded sources, stable versioned names. Do not parse chat approval as automatic acceptance.
3. **batch-export:** one local call processes accepted raws to 256x256 square opaque RGB lossless VP8L WebPs with logged Pillow interpolation/encoder params; permit opt-in per-image median-cut palette reduction if director explicitly approved the visual loss, but never auto-quantize or apply BBE's cap to every family. Always retain immutable input bytes, verify decoded export equality to **approved transformed** pixels, source integrity, file signature/format and byte budget.
4. **preflight:** invoke the **real repo artpreflight.py** over all current output WebPs once, with `--type JUTSU_ICON`, and if/only-if the family has a stricter approved cap `--max-bytes <N>`. Record exact command, spec script/hash, stdout/stderr, exit code, individual failures; `NOT_RUN` if script unavailable. Do not substitute a reimplementation and claim canonical green.
5. **showcase+pack:** deterministic adaptive grid by exact N, matching docs/workflows/JUTSU_ICON_SHOWCASE.md, source-faithful pixels, real bytes/1000 caption labels, dark neutral background, 125/64/32 QC and phone preview. Output one complete studio ZIP with manifest/raws/WebPs/gallery/QC and optional small flat `N_webps.zip` for mobile upload. Zip CRC, member hashes and replay-deterministic membership. No upload capability.
6. **incremental rerun:** key caches by `(approved_raw_sha, processor_options, current_art_spec_sha)`; when only one director-approved raw changes, invalidate that export plus derived gallery/ZIP, not all accepted files. Refuse a filename reused for changed bytes; atomically write accepted bundles and preserve prior exports.

Maintain a compact, machine-readable single `studio_ledger.json` recording jutsu ID, display name, reference/member SHA, director silhouette/art approval state (provided explicitly), actual source/export hashes and unresolved gates. Avoid a separate registry requiring manual transcription of all fields into every prompt.

## Startup and processing benchmarks

Add socket-free timings to the CLI (`intake_ms`, `hash_decode_ms`, `export_ms`, `preflight_ms`, `showcase_ms`, `pack_ms`). Compare baseline simulated **5-, 8-, and 12-icon** packs and one changed-icon incremental rerun with the optimized path. Report expected savings only for the measured deterministic steps, not an unmeasured 8–10-minute ChatGPT/imagegen service cycle. User-facing cold startup should require **one archive** and **one batch command** where dependencies are available.

## Adversarial tests / completion gates

- ZIP-slip, absolute paths, symlinks, decompression bombs, too many members, duplicate/case-colliding names, corrupt CRC, JSON schema mismatch, altered hashes, undecodable JPEG disguised as PNG (detect correctly, not reject solely for extension), oversized images and missing mapped IDs.
- N=5 (3+2), N=8 (4+4), N=12 (4+4+4), dynamically sized galleries; reject silent omission, duplicate ID, missing source, stale accepted icon, inaccurate file-size caption.
- ID joins across exact historic/pinned jutsu and source manifest; include bloodline-owned SPECIAL records where source verified. Avoid assumptions of live freshness.
- BBE family cap **80000 exclusive**: 79999 allowed/80000 fails; BEE/Vaporia use spec working ceiling instead; verify current shared client item/bloodline alpha requirement unchanged.
- Test controlled quantization as explicit, director-approved step; verify VP8L losslessness **relative to transformed pixels**, original raw immutability, versioned filenames, content-replay deterministic output.
- Mock canonical preflight subprocess and unavailable script path; genuine validator run must be evidenced by exit code; no forged pass or bypass.
- Simulate partial processing/interruptions, cache tamper, stale gallery, changed approved image, ZIP rewrite collision and prove fail-closed atomic output, no mutation of previous successful archive.
- Run existing artpreflight/skill selftests, any new test suite, repo doctrine/pack guards applicable to changed files. No live TNR requests/writes/CDN reads during tests.

## Authoritative precedent pins (evidence only; binaries remain conversation deliveries)

- BBE closeout: `e5aa3b13eb4896e93b3e85799b8f0ec2eaedeb9f`; eight approved and processed, BBE-specific median-cut under-80k. PR #41 documentation only, open at review.
- BEE closeout: `1f6010be0967d1ed42645a1a7476b8a1ec2a75e2`; 8/8 local WebPs with no forced under-80k; final skull/vein replacements.
- Vaporia closeout: `730f5393d4428282402f5f66ef2aeea3d156e405`; five raw/exports, 3+2, family acceptance historically pending, legacy alpha comment superseded.
- JUTSU_ICON current spec at main, source of numeric requirements; previous generic ICON alpha records must not be mistaken for current JUTSU_ICON rejection.

## Handoff format

Return Branch/Base/Merge-base/Frozen Head, exact file/CLI paths and syntax, normalized input/output contracts, synthetic benchmark command+times, tests, artifact SHA/ZIP proof, error reporting, **game requests/writes 0/0**, credentials none, independent review request. Do not merge on implementation success alone. Do not modify active ChatGPT-owned workflow/art branches in this implementation pass.
