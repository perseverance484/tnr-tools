# Jutsu art lookup — independent review

Review date: 2026-10-05 America/Chicago (2026-10-06 UTC).

**Verdict: CHANGES REQUESTED — three P2 correctness findings.** The frozen corpus, exact-name lookup, manifest identity checks, and declared CDN restrictions passed the checks described below. The findings concern future coverage reporting and optional image materialization, not an incorrect current 604/441/440 corpus or a discovered live-game request path.

| Item | Verified value |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Implementation branch | `ccr-9fb18f2c-0wrhlu` |
| Frozen review target | `e73cd2e91c76c764be3895fa19f99fdbb13b3720` |
| Base, merge-base, and remote main observed during review | `b6f719dc5241f2b4fefc553670a61ea0c4a16d6e` |
| Delta | One commit; the five files listed in the handoff |
| Review branch | `chatgpt/review-jutsu-art-20261005`, based on the frozen target |
| Review boundary | No implementation edits; zero live-game requests/writes; zero image-CDN requests |

## JA-R1 — P2: catalog count equality silently clears unresolved census coverage

**Location:** `scripts/jutsu_art.py:285–302,354–384` (`load_corpus` known-name count and `derive` coverage status).

The historical census discrepancy is represented only as `live != known`, where `live` comes from the pinned #66 capture and `known` comes from automatically regenerated answer files. Adding two previously unknown IDs to the catalog/hot data makes the latter count 1,493. Without changing any census capture or classifying either ID, `build` then emits `coverage.status = "MATCHED"`, removes the unresolved warning, and produces output that passes `verify`.

**Reproduction against the frozen code, with sockets blocked:**

1. Copy the pinned sources and generated output into a temporary directory.
2. Append `["review-new-id-1", "Review New Jutsu 1", null]` and `["review-new-id-2", "Review New Jutsu 2", null]` to `answers/hot.json` → `entities.jutsu.rows`.
3. `verify` initially returns 1 for stale output, as expected. Run `build`, then `verify`, then `lookup "Review New Jutsu 1"`.
4. Observed: build 0; verify 0; lookup 1; `MATCHED`; warnings `[]`; corpus still 604 captured / 441 eligible / 440 URLs; neither new ID is in the corpus. Build, verify, and the lookup miss all omit the unresolved warning.

**Broken invariant and consequence:** `docs/workflows/JUTSU_ART_LOOKUP.md:29–32` and the handoff retain unresolved coverage until a delta follow-up capture resolves it. Equal cardinalities from different snapshots do not establish that the previously unknown records were classified. The handoff's recommended rebuild after answer regeneration can therefore erase the caveat it promises to preserve.

**Smallest robust correction:** retain the pinned census's unresolved status independently of the current known-name count. A current count can be additional diagnostic information. Clear the historical caveat only when explicitly adopted follow-up evidence establishes the necessary IDs and classifications; simply reaching 1,493 must not do so.

**Regression gate:** append unrelated IDs until counts match, rebuild, verify, and miss a lookup. The unresolved warning must remain in all three paths unless reviewed follow-up evidence has been adopted.

## JA-R2 — P2: a later download failure leaves files and their index inconsistent

**Location:** `scripts/jutsu_art.py:518–536` (`materialize`).

Images are written to their final paths inside the download loop, but `materialized.json` is updated only after every requested download succeeds. A failure on the second request leaves the first file on disk without its new index entry. When replacing an existing file, the old index can remain and advertise a SHA-256 that no longer matches that file.

**Reproduction against the frozen code, with an injected fetcher and real decodable PNG fixtures:**

- Select two eligible IDs and use a fresh temporary output directory. Return a valid PNG for the first request and raise `urllib.error.URLError` for the second. The first final PNG exists, but `materialized.json` does not.
- Repeat after successfully indexing the first ID with a red PNG. On the failing two-image call, return a valid blue PNG for that first ID before failing the second request. The on-disk file is replaced; the index still contains the red image's hash.

The observed old indexed hash was `be21aef17f0baf04b1bf148f8a23bda4e879b346a64637fdd711bea012e646a8`; the actual replacement hash was `548c752266def8c110bdce0cb60c3095427d099a2d8b33100e11fc484cc1a4c3`.

**Broken invariant and consequence:** the documented materialization output is an image set with its URL/byte/hash index (`docs/workflows/JUTSU_ART_LOOKUP.md:55–59`). A routine later-request failure can leave untracked images or stale provenance for files already replaced. The command raises an exception, but does not restore consistency or identify the completed subset through its index.

**Smallest robust correction:** give failure an explicit consistent outcome. Either commit each successfully validated image with an updated index before proceeding, or stage the requested batch and preserve the existing directory/index if fetching or validation fails. Use temporary files and atomic replacement where applicable; validate an existing index before overwriting assets.

**Regression gate:** second-fetch failure in both a fresh directory and a directory containing a prior materialization. After failure, every published file/index pair must agree, or the previous output must remain intact. This does not require implementing Phase 2 rotation.

## JA-R3 — P2: an image signature alone is accepted as a usable image

**Location:** `scripts/jutsu_art.py:484–493,523–531` (`sniff` and its caller).

`sniff` recognizes only a short prefix and `materialize` treats that as sufficient validation. Header-only or truncated responses are saved and indexed with `action = "fetched"`, despite being undecodable as images.

**Reproduction against the frozen code, with sockets blocked:** inject each response below into `materialize` for `Crescent Reaper Fang`:

| Bytes returned by the fetcher | Result |
| --- | --- |
| `b"\x89PNG\r\n\x1a\n"` (8 bytes) | Saved and indexed as PNG |
| `b"GIF89a"` (6 bytes) | Saved and indexed as GIF |
| `b"\xff\xd8\xff"` (3 bytes) | Saved and indexed as JPEG |
| `b"RIFF\x04\x00\x00\x00WEBP"` (12 bytes) | Saved and indexed as WebP |

All four returned `fetched`; all four were rejected by Pillow with `UnidentifiedImageError`. The existing materialization success fixture at `scripts/test_jutsu_art.py:23` is likewise just a fabricated WebP-shaped byte sequence, so those tests do not demonstrate acceptance of a usable image.

**Broken invariant and consequence:** the handoff says the response is checked to be an image, and the workflow promises image bytes for art work. A signature establishes a possible format, not usable content. An incomplete response can therefore produce a false-success asset. The current corpus URLs themselves were not contacted and are not alleged to be broken.

**Smallest robust correction:** retain signature detection if useful, then validate the image with a real decoder before any final file or index replacement. Pillow is already an approved art dependency under `CLAUDE.md` section 9. Reject truncated or invalid payloads, preserve existing output on rejection, and replace the success fixtures with minimal valid images.

**Regression gate:** actual valid PNG/JPEG/GIF/WebP fixtures succeed; header-only and truncated payloads fail without publishing or overwriting an indexed asset. Preserve support for animated assets when selecting the validation method.

## Checks that passed

| Check | Result |
| --- | --- |
| Remote implementation/main and merge-base | Exactly matched handoff head/base |
| Author suite, run via unittest discovery with `socket.socket` and `socket.create_connection` blocked | 34 tests passed |
| `python3 scripts/jutsu_art.py verify` | Exit 0; generated output matches fresh derivation |
| Independent direct aggregation of the seven bundle files | 604 captured; 441 eligible; 440 unique eligible URLs; 163 excluded; eligible ID set exactly matches output |
| Forge's own `parseManifest` for #67–#74 | All eight hashes match the script's pins and corresponding read counts |
| Historical #66 manifest at `1a1c4b9` | Hash `61579eea`; its 604 point-read IDs match #67 in order |
| Current #66 manifest | Hash `d231f7fb`, confirming the disclosed historical/current distinction |
| Eligible URL host inventory | All 441 URLs use the five declared hosts |
| Direct redirect-handler probes | Game apex, game subdomain, unapproved host, and HTTP refused; allowed HTTPS CDN redirect accepted |
| `python3 skills/building-tnr-content/scripts/doctrinemap.py .` | Exit 0; 0 errors, 0 warnings |
| `python3 skills/building-tnr-content/scripts/render_doctrine.py --check` | Exit 0; current |
| `python3 skills/building-tnr-content/scripts/build_packs.py --check` | Exit 0; current |
| Frozen worktree before adding this report | Clean; no tracked implementation/source changes |

The author suite also exercises normalization, exact-only resolution, ambiguity refusal, suggestions without automatic selection, excluded-record handling, full-record retrieval, source tamper rejection, deterministic generation, and all-name resolution before materialization requests. These passed. The independent probes above exercise failure cases absent from that suite.

## Existing initialization issue, separate from this commit

The repository session initializer was exercised in process with its digest-save function suppressed to keep the review read-only. Its lawmap check reports 0 errors / 5 warnings, and its doctrine/pack checks pass. Its latest-bundle parity check exits 1: `validate.py:201` attempts `set(None)` because the Forge bundle has `"checks": null`.

Direct reproduction: run `python3 ../scripts/validate.py --parity <repo>/harvests/inbox/tnr_results_1791248170855.json` from `skills/building-tnr-content/data/`.

The validator subtree and that input bundle are byte-identical between the stated base and review target (`git diff --exit-code BASE HEAD -- skills/building-tnr-content harvests/inbox/tnr_results_1791248170855.json` passed). This is a pre-existing initialization failure, not a regression caused by the jutsu-art commit, and not one of JA-R1–R3. The handoff's three named doc checks did pass; that is not equivalent to every repository initialization guard being green.

## Scope, limitations, and next step

No real CDN transfer, browser/game session, live image decoding, or game write was performed. Network behavior was inspected in code and exercised through injected responses/direct redirect-handler calls, with review tests socket-blocked. The scratch reproduction harness was not committed, per the review workflow.

Phase 2 workspace rotation and the art-skill routing update remain disclosed deferred work, not review defects. The current generated census correctly retains the unresolved gap; JA-R1 describes a reproducible subsequent-regeneration failure.

Claude should correct JA-R1–R3 on its implementation branch, add focused regressions, rerun the 34-test suite plus additions, corpus verification, and applicable doc gates, then return a new frozen SHA. A focused re-review is sufficient if changes stay within coverage-state handling, materialization validation/consistency, their tests, and corresponding documentation. Wider source or architecture changes require reviewing their affected assumptions. Do not merge this reviewed target as approved while these findings remain open.
