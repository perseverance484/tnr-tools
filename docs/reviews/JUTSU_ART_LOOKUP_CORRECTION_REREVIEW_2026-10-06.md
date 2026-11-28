# Jutsu art lookup — focused correction re-review

**Verdict: PASS for frozen `2cc3a0901361f43b6285c098b0b1ef42848942ed`. JA-R1, JA-R2, and JA-R3 are CLOSED. No merge-blocking findings remain within this correction scope.** One non-blocking clarification about the final publication boundary is recorded below.

| Review identity | Verified value |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Implementation branch, sole writer Claude Code | `ccr-9fb18f2c-0wrhlu` |
| Frozen correction target | `2cc3a0901361f43b6285c098b0b1ef42848942ed` |
| Previous target | `e73cd2e91c76c764be3895fa19f99fdbb13b3720` |
| Original base / merge-base with current main | `b6f719dc5241f2b4fefc553670a61ea0c4a16d6e` |
| Remote main observed | `0a554ef200b37f0d9f7c5c32446e057441617aa0` |
| Prior review | `b330b3eeeb8cf2dcda22b0d7eacdcd84c3dcb4d0`, `docs/reviews/JUTSU_ART_LOOKUP_REVIEW_2026-10-05.md` |
| This review branch | `chatgpt/review-jutsu-art-corrections-20261006`, based on the correction target |

The correction is exactly one commit and four changed files: `scripts/jutsu_art.py`, `scripts/test_jutsu_art.py`, `answers/jutsu_art.json`, and `docs/workflows/JUTSU_ART_LOOKUP.md`. The implementation remains within the agreed focused re-review boundary. No capture bundles, manifests, eligibility or lookup rules, CDN allowlist, or router row changed.

Main's change since the base is limited to `docs/DRIFT.md` and `state/schema_sentinel.json`. It has no file overlap with the feature or its pinned sources. Preserving the frozen target without rebasing was appropriate.

## Finding closure

### JA-R1 — CLOSED: current catalog size cannot clear the historical coverage gap

Reviewed `scripts/jutsu_art.py:52–71,221–239,366–404,423–432` and the corresponding generated output/documentation.

The live #66 row count is checked against its pin. The historical known count and unresolved status are independent of today's catalog/hot count. Today's count is printed only as a diagnostic and does not enter the generated JSON. A status flip or non-null resolution is refused until an evidence-verification path is implemented.

Independently repeated the original +2-hot-ID reproduction in a temporary source copy. `verify` succeeds before rebuilding, `build` and subsequent `verify` succeed, all keep the unresolved warning, and the lookup miss returns 1 with that warning. The generated output remains byte-identical to the frozen correction's output. The author regressions also pass for a status flip, a fabricated resolution, and a changed live-count pin.

### JA-R2 — CLOSED for the requested download/decode failure guarantee

Reviewed `scripts/jutsu_art.py:572–671`.

All names and eligibility checks precede fetching; the existing index is validated before fetching. Every requested image is fetched and decoded before image/index staging begins. The original second-fetch failure no longer publishes a partial batch or changes a prior file behind its index. Format replacement, unindexed-target protection, and duplicate-request handling are implemented.

Independent probes confirmed:

- A second-fetch failure publishes nothing in a fresh directory and preserves an existing directory byte-for-byte.
- A second-decode failure after a valid first replacement also preserves existing output byte-for-byte.
- Non-object/malformed-entry indices, unsafe filenames, and indexed missing files refuse before any fetch.
- An injected staging `fsync` failure preserves existing files and removes staged temporary files.
- Two normalized spellings of the same name result in one fetch and one result.

The author's red/blue regression, inconsistent-index, unindexed-file, and format-change cleanup tests also pass. The remaining final-publication limitation below does not reopen the original second-fetch/second-decode defect.

### JA-R3 — CLOSED: materialization validates decoded image content

Reviewed `scripts/jutsu_art.py:524–551`.

The signature is now a preliminary filter. Pillow opens the response, and every reported frame is sought and loaded. The decoded format must agree with the signature; permissive `LOAD_TRUNCATED_IMAGES` mode is refused. Image bytes are retained exactly rather than re-encoded.

The four original header-only payloads are independently rejected. The author suite passes with actual PNG, JPEG, three-frame GIF, and two-frame WebP fixtures, checks exact saved bytes and frame counts, and rejects the tested truncated payloads while preserving prior output. An additional independent probe confirms refusal when Pillow's truncated-image override is enabled.

In a fresh process with Pillow imports explicitly blocked, `lookup`, `search`, `record`, and `image-url` each complete successfully. Pillow is required only by actual materialization.

## Non-blocking clarification — publication is not a directory transaction

**JA-N1 — low severity / documentation refinement.** Locations: `scripts/jutsu_art.py:572–574,666–670`; `docs/workflows/JUTSU_ART_LOOKUP.md:64–77`; correction handoff's crash-window paragraph.

The multi-file `os.replace` sequence is not crash-atomic. This is disclosed in the handoff and is acceptable for the bounded correction, which protects the previous output from download/decode failures. Ordinary filesystem errors during replacement can interrupt the same sequence as a process crash.

The claim that the next index check always detects and refuses the interrupted state is too broad. With an indexed PNG already present, stage replacement JPEGs, then inject an `OSError` immediately before the index replacement. The old indexed PNG still matches its old hash, while the new JPEGs and staged index are unindexed. `_read_index` returns successfully because it validates named files, not every directory entry. By comparison, interrupting a same-format replacement after changing the indexed PNG causes the next index read to refuse its hash mismatch.

Both cases were reproduced offline. This is additional characterization of the already disclosed publication boundary, not a renewed fetch/decode failure. Narrow “all-or-nothing” wording to the verified pre-publication guarantees, and describe next-run checking as validation of indexed files rather than guaranteed detection of all partial publications. The existing unindexed-target guard can still require manual cleanup if a later request targets an orphan. Durable directory-level transactions, recovery, and concurrent-writer support remain outside this correction approval.

## Verification results

| Check | Result |
| --- | --- |
| Remote implementation head / correction ancestry | Exact frozen target; one commit above the previous target |
| Current main vs original base | Only the two reported sentinel files; no overlap |
| Author suite via `unittest.defaultTestLoader.discover('scripts', pattern='test_jutsu_art.py')` | 43 tests passed with `socket.socket` and `socket.create_connection` patched to raise |
| Independent scratch harness, `python3 /workspace/scratch/9dc0bafbe2e4/correction_probes.py` | 8 focused tests passed with sockets blocked; two publication-boundary probes recorded above |
| `python3 scripts/jutsu_art.py verify` | Exit 0; 604 captured / 441 eligible / 440 unique URLs; UNRESOLVED warning retained; exact rebuild match |
| Generated JSON comparison against the previous target | All 604 record objects, counts, and pinned source metadata unchanged; only `coverage` and `warnings` differ |
| Offline commands with all Pillow imports blocked | Lookup, search, record, image-url all exit 0 |
| `python3 skills/building-tnr-content/scripts/doctrinemap.py .` | Exit 0; 0 errors, 0 warnings |
| `python3 skills/building-tnr-content/scripts/render_doctrine.py --check` | Exit 0; all projections current |
| `python3 skills/building-tnr-content/scripts/build_packs.py --check` | Exit 0; all packs and TOCs current |
| Reviewer runtime | Pillow 12.3.0 |
| Frozen worktree before adding review evidence | Clean |

The scratch harness was not committed. Neither implementation code nor pinned sources were edited during this review.

## Scope and next permitted step

This approval covers the correction target, not a live CDN/browser/game run or Phase 2. Zero live-game requests/writes and zero image-CDN requests were made. Download/decode behavior was exercised with injected local fixtures; the prior review's unchanged URL/redirect boundary remains applicable.

The existing `validate.py --parity` failure on Forge `checks: null` is unchanged from the previous target/base. It was established in the initial review and was not rerun or included in the passing doc-gate claim here. Phase 2 workspace rotation and the producing-tnr-art skill routing update remain explicitly deferred.

The implementation may proceed through the normal integration process after final ref verification. At the main head verified here, only the unrelated sentinel delta separates it from the original base. Any subsequent implementation correction or integration conflict that alters reviewed behavior must be identified before approval is carried forward. JA-N1 can be addressed as a small documentation clarification; it does not require a new architecture or another round of the already closed JA-R1–R3 work.
