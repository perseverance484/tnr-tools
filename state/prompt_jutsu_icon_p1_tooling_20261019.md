# Fable Implementation Brief — Jutsu Icon P1 Tooling (Option B)

**Status:** APPROVED 2026-10-19 (RUL-2026-10-19-005, decisions D1–D10). Lane A, Fable implementation; independent ChatGPT review at an exact frozen SHA.
**Scope source:** `docs/design/jutsu_icon_studio/P1_TOOLING_SCOPE_PROPOSAL_20261019.md` (gap IDs G1–G14, tests 1–23, targets §6). The proposal is the analysis; this brief is the build contract.
**Governing protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md` (P0 A–F, RUL-2026-10-19-003). This brief adds no art rule.
**Base:** main@`f620db3d` (refresh before handoff). **Branch:** the session-assigned implementation branch (one writer).
**Boundaries:** zero network, zero live requests/writes, no credentials, no uploads. Aerathiel gallery PENDING / preflight NOT RUN / Git pinning PENDING / upload-readback NOT PERFORMED are untouched.

## 1. Port (D2, D3, D4)

From `claude/bloodline-jutsu-icon-studio-3nmvc2@6bc0af4e` port only: `skills/producing-tnr-art/scripts/{jutsu_studio.py,jutsu_studio_selftest.py,style_refs.py}`, `data/style_refs.json`, the `SKILL.md` rows, and `art/style_refs/jutsu_icons/**` (16 WebPs + intake records). Do not port ChatGPT-owned workflow documents or RUL-2026-10-17-020. CLI text cites only main authorities until those documents land.

## 2. Required changes

| Gap | Change |
| --- | --- |
| G1 | `family_acceptance` ACCEPTED requires `gallery_sha256`. At build the gate is ACCEPTED only if the built gallery's file SHA **or** decoded-pixel SHA matches; otherwise `INVALIDATED` with the prior SHA recorded. Never inherited. |
| G2 | Showcase re-hashes every export against its recorded `output_sha256` before use. After writing, the gallery PNG is decoded from its written bytes and audited (same code path as `audit-gallery`); any mismatch refuses. |
| G3 | Pack re-hashes every raw and export against the recorded SHAs before sealing. A mismatch refuses; no archive is written. |
| G4 | `audit-gallery GALLERY.png --manifest M --exports DIR` → VALID / INVALID, naming tile positions, caption and geometry faults. |
| G5 / D5 | `grid_rows`: N ≤ 9 unchanged; N ≥ 10 → `ceil(N/4)` rows, balanced, longer rows first. |
| G6 / D6 | Flat WebP ZIP is named `<fam>_jutsu_icons_webps_PREFLIGHT_<VERDICT>_<N>webp_<label>.zip`. The word `upload` is never used. |
| G8 / D9 | `data/preflight_pins.json` records the git blob SHA-1 of `scripts/artpreflight.py` and `data/25x_DATA_art_spec.json` and the main commit they were verified at. A run whose script or spec blob differs is `NON_CANONICAL` (output still recorded). A selftest asserts the pins equal the shipped files. |
| G9 | Roster rows carry `evidence_level` ∈ {`historical_capture`, `director_roster`, `current_live_unverified`}. A ZIP manifest defaults to `historical_capture`; a director roster is `director_roster`. Tooling never asserts current-live. |
| G10 / D7 | Gates use the K names: `ORIGINAL_SOURCE_VERIFIED, DIRECTION_APPROVED, RAW_VISUAL_APPROVED, OUTPUT_LOCAL_QC, CANONICAL_PREFLIGHT, FAMILY_SHOWCASE_ACCEPTED, ZIP_DELIVERED, GIT_BINARY_PIN, USER_UPLOAD_READBACK`, per icon and per collection. `check_gates()` refuses inconsistent combinations. Tooling never sets `GIT_BINARY_PIN` or `USER_UPLOAD_READBACK` beyond `NOT_PERFORMED`. |
| G11 | `style_refs.py` marks a JUTSU_ICON exemplar with `closeout_match: false` as `PROVENANCE_PARTIAL` in `list`/`select` and in intake output. |
| A | `lock-check LOCKS.json [--source-index]`, schema `tnr.jutsu-studio.locks/1`. Per target: `jutsu_id, name, version, evidence_level, action, dominant_silhouette, camera, motion_axis, secondary_effect, sibling_exclusions[{jutsu_id, silhouette}]` (covering every other target), optional `wrong_subject_exclusions[]`, `references[≤2 {sha256, role ∈ identity-only/style-only/material-only/subject, kind = individual}]`, `anatomy_exception` (null or `{scope, director_evidence}`), `direction_approval {status PENDING/APPROVED, evidence, lock_sha256}`. `lock_sha256` = SHA-256 of the canonical target without `direction_approval`; a mismatch under APPROVED is refused (bump version, re-approve). Incomplete → `LOCK_INCOMPLETE`. |
| B / J / D8 | `attempts ATTEMPTS.json [--locks]`, schema `tnr.jutsu-studio.attempts/1`. Per attempt: `jutsu_id, attempt` (1..n contiguous per jutsu), `session_id, outcome` (rejected/viable/approved), `reasons[]` (required when rejected; codes `wrong_target, composition, silhouette_conflict, art_style_drift, anatomy, invented_symbol, quality, other`), `candidate_sha256` (required when approved), `anatomy_present`, `references[≤2 sha]`, `shown_to_director`, `generator_wait_ms` (only if measured). Two consecutive wrong_target/composition rejections in one session make a further attempt in that session a refusal (`RESTART_REQUIRED`). A reference equal to a rejected candidate is refused. Approved + anatomy requires a lock `anatomy_exception` for that target. Stats are reported per jutsu and per family. |
| A/B/D | `verify-approved` / `finalize` accept `--locks` and `--attempts`. With them, each approved raw must equal the last approved attempt's candidate SHA, and its lock must be DIRECTION_APPROVED and intact. |
| C | `compare CANDIDATE FAMILY_FILE... --out DIR [--label]`: non-generative 125/64/32 sheet of the candidate beside family files, labelled `REVIEW AID - NOT A GALLERY`, with a manifest of SHAs and positions, tile pixel-equality, unchanged candidate bytes, and write-once output. |
| doctor | Checks Pillow WebP lossless/VP8L, an encoder determinism probe, the spec's JUTSU_ICON target, script presence, pins (canonical or not), and a real `artpreflight --type JUTSU_ICON` run on a synthetic probe export. Reports `RUN_CAPABLE_CANONICAL` / `RUN_CAPABLE_NON_CANONICAL` / `NOT_RUN: <reason>`; exit 0 only for canonical. Optional `--git-ref` compares the blobs with a git ref when git is present. |
| §6 speed | One encoder-determinism probe per run (not per icon). The cache stores the transformed-pixel SHA, so a cache hit verifies raw SHA + export SHA + decoded export pixels without decoding or resizing the raw. Targets on `bench`: full export N=12 ≤ 2.2 s, 1-changed export ≤ 200 ms, full finalize N=12 ≤ 3.0 s. Report measured numbers; do not tune encoder parameters (output bytes stay as before). |

## 3. Tests and gates

Implement proposal §5 tests 1–23 as socket-free selftest checks, except where a check is a human judgement (record it as a deviation). Keep the existing checks green (update the two layout checks to D5 and the archive-name check to D6). Run: `jutsu_studio_selftest.py`, `style_refs.py --selftest` and `verify`, `artpreflight_selftest.py`, `jutsu_studio.py doctor`, `bench --sizes 5,8,12`, `doctrinemap.py`, `render_doctrine.py --check`, `build_packs.py --check`.

## 4. Handoff

Follow `docs/workflows/IMPLEMENTATION_HANDOFF.md`: base/head SHA, changed files, commands with exact results, measured bench, deviations, and what was not done (no real-art run, no ChatGPT-container run, no review). Freeze the SHA. The integration PR waits for D4's documents or proceeds citing main authorities only.
