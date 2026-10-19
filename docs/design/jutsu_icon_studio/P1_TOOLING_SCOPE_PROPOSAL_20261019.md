# Jutsu Icon P1 Tooling — Scope Proposal and Gap Analysis

**Status:** APPROVED 2026-10-19 — all §8 recommendations (Option B, D1–D10) adopted as RUL-2026-10-19-005; build contract `state/prompt_jutsu_icon_p1_tooling_20261019.md`. The analysis below is kept as written at proposal time.
**Author / lane:** Fable (Claude Code), Lane A scoping only. No code was written, ported or integrated.
**Authority:** `docs/workflows/ISOLATED_ART_GENERATION.md` (P0 A–F, RUL-2026-10-19-003) governs. This proposal cites it; it does not restate or extend it.

## 0. Pins (verified this session)

| Item | Ref |
| --- | --- |
| Current main | `ee45269169aeddb055c39426ff5812ede2e3d006` |
| P0 merge (PR #58) | `1308bfe6f218af78345ecaf8ca270f5b9f9f2cc3` — ancestor of main ✔ |
| Prototype (UNREVIEWED / NOT INTEGRATED) | `claude/bloodline-jutsu-icon-studio-3nmvc2@18f52dd308eb59f8027e1e9e6892427842f98578` |
| Prototype merge-base with main | `9a0970002a80531078ac5e4b0f72578d3f7855f5` (the brief's stated base). Main is 125 commits ahead; prototype 17 ahead |
| Fable code commit inside prototype | `6bc0af4e` (CLI, selftest, style_refs, 16 exemplar WebPs, docs); `18f52dd` is the skillpack bot rebuild |
| Retrospective | `chatgpt/aerathiel-jutsu-art-studio-20261019@2994305e5cd4894953a14b7c1d8727ddfc00fdd3` — **not on main** |
| Implementer brief | `state/prompt_jutsu_icon_studio_fast_tooling_20261017.md` @ `18f52dd` (also on `chatgpt/bloodline-jutsu-studio-zip-first-20261017@d04a87c0`) — **not on main** |

**Preserved, unchanged by this proposal:** Aerathiel gallery acceptance **PENDING** · canonical preflight **NOT RUN** · Git binary pinning **PENDING** · user upload/readback **NOT PERFORMED** · live requests/writes **0/0** · credentials **none**.

## 1. Summary

The prototype is a solid base for the **mechanical** half of P0/P1: safe ZIP intake, exact ID mapping, cached lossless export, real-`artpreflight` invocation with honest NOT_RUN, deterministic gallery, deterministic ZIPs. Its own 83 checks pass. It predates P0, so it has **no** support for the target lock (A/B), attempt/failure records (J), pre-approval distinctness review (C), or per-target anatomy exceptions (D), and it has **four source-fidelity defects** against P0 F that must be fixed before any integration (§3.1).

Speed: the deterministic steps already finish in **under 5 s for 12 icons** here. Further CLI tuning saves seconds, not minutes. The measurable leverage is (a) getting the canonical preflight runnable in the art container in one command and (b) recording attempts per accepted raw so the P0 target lock's effect can be measured. No tool can shorten image-generation latency or decide whether pixels depict the right technique.

**Recommendation:** Option B (§4), implemented on a fresh `fable/*` branch from current main by porting the Fable code commit only, after the director settles D1–D10 (§8).

## 2. What was checked (offline, socket-free)

Run in a detached scratch worktree of `18f52dd`, Python 3.13.16, Pillow 12.3.0:

| Check | Result |
| --- | --- |
| `jutsu_studio_selftest.py` | **83 passed, 0 failed** (6.4 s) |
| `style_refs.py --selftest` | all checks passed |
| `style_refs.py verify` | 18/18 approved captures proven; BBE 8 + BEE 8 exemplars proven against `INTAKE_20261017.json` |
| `artpreflight_selftest.py` (prototype and main, run from `data/`) | 98 passed, 0 failed each |
| `jutsu_studio.py --help` cold start | ~80 ms (Pillow import dominates) |
| Trial merge of main into prototype (not committed, aborted) | one conflict: `docs/RULINGS.md`. `skills/producing-tnr-art/` is unchanged on main since the merge-base, so the code ports cleanly |

**Not performed:** independent review of the prototype, any run against real Aerathiel/BBE/BEE raws, any browser/ChatGPT-container run, any live or CDN request.

### Benchmark (`jutsu_studio.py bench --sizes 5,8,12`, two runs; ms)

| N | intake | full finalize (export / preflight / showcase / pack) | 1-icon-changed rerun (export / …) |
| --- | --- | --- | --- |
| 5 | 18–34 | 1750–1858 (1366–1566 / 72–80 / 172–239 / 49–66) | 672–785 (370–501 / …) |
| 8 | 19–22 | 2891–2923 (~2446 / 70–82 / 300–314 / 74–82) | 832–988 (428–474 / …) |
| 12 | 38–48 | 3958–4261 (3397–3703 / 74–88 / 355–378 / 106–119) | 1077–1151 (470–563 / …) |

Per-icon breakdown on a 1254 px noisy synthetic raw (closer to Aerathiel's 1254 px PNGs): decode+RGB ~39 ms, LANCZOS→256 ~18 ms, lossless WebP `method=6` ~122 ms (`method=4` ~65 ms, same 53,456 B output on this sample). The prototype encodes **every** icon twice (determinism check) and, on cache hits, still decodes and resizes every raw.

Synthetic images understate real encode cost. These figures measure only deterministic local steps.

## 3. Gap analysis: prototype vs integrated P0

Severity: **BLOCKER** = must fix before integration; **HIGH/MED/LOW** = P1 scope candidates.

### 3.1 Source-fidelity defects (P0 F, §4)

| # | Gap | Evidence | Sev |
| --- | --- | --- | --- |
| G1 | **Family acceptance is not bound to a gallery SHA.** `family_acceptance.status: ACCEPTED` in `approved.json` is copied onto any newly built gallery, so a gallery built from changed bytes inherits acceptance. P0 F5: changed source bytes invalidate the prior gallery and require fresh signoff | `verify_approved` / `build_showcase` / `final_ledger` — no `accepted_gallery_sha256` comparison | BLOCKER |
| G2 | **Tile pixel-equality check is self-referential.** It compares each canvas crop with the same in-memory tile it just pasted. It does not re-decode the written PNG, and it does not check that the export file on disk still hashes to its recorded `output_sha256` | `build_showcase` reopens `exports/<name>` without a hash check | BLOCKER |
| G3 | **Pack re-reads raws and exports from disk without re-hashing.** SHA256SUMS is computed from whatever bytes are present at pack time, so a swap between export and pack is sealed in as "verified" | `finalize` pack stage `read_bytes()` | BLOCKER |
| G4 | **No audit mode for an externally supplied gallery.** Under P0 F4 a generated sheet (e.g. Aerathiel `b4161df5…`) must be classed INVALID. The tool can only build galleries, not verify one against a manifest | — | HIGH |
| G5 | **N ≥ 10 layout is not balanced.** Hard-coded and self-tested: 10 → 4+4+2, 13 → 4+4+4+1 (a lone tile). P0 F2 says "balanced". The unmerged showcase doc allows "final shorter row centered", so this needs a director call (D5) | `grid_rows`; selftest `run_layout_tests` | MED |
| G6 | **An "upload" ZIP is built even when canonical preflight is NOT_RUN.** The status is recorded, but the archive name implies readiness. P0 §4: never promote local QC to upload-ready | `finalize` builds `*_upload_*.zip` regardless | HIGH |
| G7 | No DRAFT/partial gallery mode. P0 F1 permits a labelled DRAFT; the tool refuses anything short of N/N (fail-closed, which is safe) | — | LOW |

### 3.2 Provenance gaps

| # | Gap | Sev |
| --- | --- | --- |
| G8 | **"Canonical" preflight is not pinned.** The run records the script and spec SHA-256 but does not compare them with the pinned main blobs. A locally edited `artpreflight.py` would still be reported as a canonical PASS | HIGH |
| G9 | Roster evidence level is not labelled. `roster_source` says *where* IDs came from (ZIP manifest or director roster) but not whether they are historical captures or current-live checks (P0 A, retrospective K) | MED |
| G10 | Gate vocabulary differs from the retrospective's state table (K): `OUTPUT_FILE_QC_PASS` vs `OUTPUT_LOCAL_QC`, `ARCHIVE_DELIVERED` vs `ZIP_DELIVERED`, `GIT_BYTES_PINNED` vs `GIT_BINARY_PIN`. It also lacks `ORIGINAL_SOURCE_VERIFIED` and `DIRECTION_APPROVED`, has no collection-level state and no transition rules | MED |
| G11 | Style library caveat: `icon_bee_sanguine_plague_v3.webp` has no raw approval or raw original in the repository (the prototype's own RUL-2026-10-17-021 says so). The 16 exemplar binaries (1,225,288 B) are on the unmerged branch only | Decision (D3) |
| G12 | **Unmerged authorities.** The CLI cites `BLOODLINE_JUTSU_ICON_STUDIO.md`, `JUTSU_ICON_SHOWCASE.md`, the START_PROMPT/templates and RUL-2026-10-17-020/021. None are on main. RUL-2026-10-19-003 refers to the ZIP-first workflow only as a separate verified ref | BLOCKER for integration (D4) |
| G13 | Lineage mixes owners. The prototype's 17 commits include ChatGPT-authored ZIP-first docs commits underneath the Fable code commit. Merging the branch as-is would integrate ChatGPT docs through a Fable PR | Process (D2) |
| G14 | Cross-environment replay. Gallery PNG bytes depend on Pillow, zlib and font versions (all recorded). A replay in the ChatGPT container should compare decoded pixels and manifest geometry, not PNG bytes | LOW |

### 3.3 P0 A–E support (record-keeping only; pixel judgement stays human)

| P0 | Prototype | Gap | Sev |
| --- | --- | --- | --- |
| A Target lock | `approved.json` carries ID, name, slug and raw SHA only | No lock record (exact bloodline/jutsu IDs + name, action, evidence level, dominant silhouette, camera/motion axis, secondary effect, sibling exclusions, reference roles). No static brief-completeness check | HIGH |
| B Composition first; restart after 2 failures | — | No per-target attempt log, so the "two wrong-subject/composition failures → clean restart" rule cannot be recorded or surfaced | MED |
| C Distinctness at 125/64/32 | 125/64/32 strip built only at finalize, from exports, after approval | No pre-approval **candidate-beside-family** sheet at 125/64/32. No reserved-silhouette/action ledger for the target family (only for exemplars) | HIGH |
| D Anatomy off by default | — | No per-target exception record (director, scope, evidence); approval rows cannot show that an exception existed | MED |
| E Chakra, not symbols | — | Human judgement. P1 should only add rejection reason codes | LOW |
| J Failure statistics | Timings only | No `attempt_count`, `wrong_target_count`, `silhouette_conflict_count`, `art_style_drift_count`, `anatomy_rejection_count`, `approved_raw_after_attempt_n`; `generator_wait_ms` recorded only where measured | MED |

**Hard limit (P0 A, refinements):** no tool may claim to verify that a candidate depicts the locked technique, that two icons are or are not confusable, or anything about hidden generator prompts. P1 tooling records studio judgements, shows the evidence side by side, and refuses inconsistent records. It does **not** auto-reject on colour similarity.

## 4. P1 scope options

| | Option A — Harden and integrate | **Option B — A + P0 record support (recommended)** | Option C — B + extended |
| --- | --- | --- | --- |
| G1–G3, G6, G8, G12/G13 fixes | ✔ | ✔ | ✔ |
| K state table with K names + transition refusals (G10), evidence-level label (G9) | partial (names only) | ✔ | ✔ |
| `audit-gallery` (G4) | — | ✔ | ✔ |
| Target-lock record + static completeness check (A) | — | ✔ | ✔ |
| Attempt / failure log (B, J) | — | ✔ | ✔ |
| `compare`: candidate beside family at 125/64/32 (C), non-generative and judgement-free | — | ✔ | ✔ |
| Per-target anatomy exception record (D); rejection reason codes (E) | — | ✔ | ✔ |
| `doctor`: verify the skill bundle and pinned preflight/spec blobs; report RUN-capable or NOT_RUN | — | ✔ | ✔ |
| Export speedups (§6) | — | ✔ | ✔ |
| Prefilled isolated-session brief rendered from the lock record | — | — | ✔ |
| DRAFT partial gallery (G7); pixel-replay verifier across environments (G14) | — | — | ✔ |
| Relative size / review cost | small, 1 review cycle | medium, 1–2 cycles | large, 2+ cycles |

**Out of scope for every option:** automatic technique/identity classification, colour-similarity rejection, any image-generator integration, uploads, Forge/builder changes, live or CDN reads, and changes to `artpreflight.py` or the art spec (those have their own owners and review).

**Integration path (all options):** create `fable/jutsu-icon-p1-<date>` from current main; port the Fable code commit `6bc0af4e` (code, selftest and `style_refs` changes; binaries per D3); leave ChatGPT-owned docs to their owner's PR (D4); apply P1 changes; hand off an exact SHA for independent ChatGPT review. The prototype branch stays frozen as evidence and is not merged.

## 5. Proposed adversarial tests

All tests are synthetic and socket-free (the existing socket-disabled harness). Each must fail closed with a named refusal, never a silent pass.

**Source fidelity / gallery**
1. Accepted gallery SHA X; one raw changes → rebuild reports `FAMILY_SHOWCASE_ACCEPTED: INVALIDATED (was X)`, not ACCEPTED (G1).
2. `ACCEPTED` without `accepted_gallery_sha256`, or with one that differs from the built gallery → refused.
3. Swap an export file between the export and showcase stages (hook via `--stop-after export` and a file rewrite) → refused on hash mismatch (G2).
4. Swap a raw or export between showcase and pack → refused; no archive written; prior archive byte-identical (G3).
5. Gallery PNG with one tile altered by a single pixel, one tile replaced by a sibling, one recoloured, or a regenerated lookalike (seeded noise) → `audit-gallery` returns INVALID with the tile position (G4).
6. Gallery with a wrong caption kB, a KiB caption, wrong order, duplicate tile or missing tile → INVALID.
7. Valid deterministic gallery re-audited after a PNG re-encode (same pixels, different bytes) → VALID by pixels, with byte-difference noted (G14).
8. Layouts for N = 1…16 match the director-chosen rule (D5); no row has more than 4 tiles; no lone final tile unless the rule allows it.
9. Canonical preflight NOT_RUN → no archive named `upload`; archive and ledger carry the D6 label (G6).

**Provenance**
10. `artpreflight.py` with one byte changed, or spec blob ≠ pinned blob → verdict `NON_CANONICAL`, never PASS (G8).
11. Preflight script missing → NOT_RUN (existing); preflight exits 0 with JSON omitting a file → FAIL (existing, keep).
12. Roster labelled `historical_capture` is never displayed or recorded as current-live (G9).
13. Gate transitions: `CANONICAL_PREFLIGHT=PASS` with `OUTPUT_LOCAL_QC≠PASS`; `ZIP_DELIVERED` before build; `USER_UPLOAD_READBACK` set by tooling at all → refused (G10).
14. Exemplar without raw-approval provenance (the sanguine_plague_v3 pattern) is flagged `PROVENANCE_PARTIAL` in selection output (G11).

**Target lock / attempts (record consistency, not pixel judgement)**
15. Lock missing camera/motion axis, dominant silhouette, sibling exclusions or reference roles → `LOCK_INCOMPLETE`; brief not emitted.
16. Lock jutsu ID/name disagrees with the intake roster → refused.
17. Lock edited after `DIRECTION_APPROVED` without a version bump → refused.
18. Attempt log with 2 consecutive `wrong_target`/`composition` rejections and a 3rd attempt in the same session ID → `RESTART_REQUIRED` surfaced; recording it requires a new session ID.
19. Raw approved while its latest attempt is recorded as rejected, or an approved raw SHA not present in the attempt log → refused.
20. Anatomy present (recorded by studio) with no target-specific exception → approval refused; an exception for target X does not cover target Y.
21. Retrospective fixtures as **records**: "Particle Cannon" attempt logged as `wrong_target: depicts Decaying Touch handprint`; a six-finger anatomy rejection; an ornamental-triangle `invented_symbol` rejection. Counters come out as Aerathiel-shaped (e.g. 6 attempts → approved at n=6), proving the log reproduces the retrospective's 15/5 accounting.
22. Reference-role check: more than two references, a sheet/contact image (multi-tile geometry heuristic, flagged for human confirmation), or a reference SHA matching a rejected attempt → refused.

**Compare sheet**
23. `compare` output tiles are pixel-equal to recorded resizes of the candidate and the approved family exports; candidate bytes unchanged; output labelled `REVIEW AID — NOT A GALLERY`.

**Regression:** existing 83 checks, `artpreflight_selftest.py` 98/0, `style_refs.py --selftest`, plus doctrine/pack guards (`doctrinemap.py`, `render_doctrine.py --check`, `build_packs.py --check`) for any skill or doc change.

## 6. Measurable startup and processing improvements

Baselines are from §2 (this container, synthetic) and the retrospective (Aerathiel, one conversation, not a service benchmark).

| Metric | Baseline | P1 target (Option B) | How measured |
| --- | --- | --- | --- |
| Full export N=12 | 3.4–3.7 s | ≤ 2.2 s: one determinism probe per run and encoder version, instead of double-encoding every icon | `bench`, median of 3 |
| 1-icon rerun export, N=12 | 470–563 ms | ≤ 200 ms: cache records the transformed-pixel SHA; cache hits verify the export SHA instead of re-decoding and resizing the raw | `bench` |
| Full finalize N=12 | 3.96–4.26 s | ≤ 3.0 s | `bench` |
| CLI cold start | ~80 ms | unchanged (not a bottleneck) | `-X importtime` |
| Canonical preflight in art container | NOT RUN (Aerathiel: source/spec absent) | `doctor` reports RUN-capable from the installed skill bundle in 1 command, or a precise NOT_RUN reason | `doctor` exit and record |
| Operator inputs to start a family | 1 prompt + 1 ZIP (prototype design; unverified in the ChatGPT container) | same, verified end-to-end once in a non-live dry run | manual dry run; record steps |
| Generations per accepted raw | 3.0 (15/5); first-pass acceptance 2/5 | **measured, not promised**: the attempt log reports it per family | attempt log |
| Wrong-target results shown to director | ≥ 2 (Particle Cannon) | measured; P0 fail-fast should drive it to 0 | attempt log |

Expected savings are **seconds** on deterministic steps. The reported 8–10-minute turns are generation/session time, which tooling can only measure.

## 7. Source-fidelity and provenance protections (Option B)

1. Every stage re-verifies input bytes against recorded SHA-256 immediately before use (raws, exports, gallery, archive members). Any mismatch is a refusal; nothing downstream is written.
2. Family acceptance binds to `accepted_gallery_sha256` + member export SHAs. Any change sets INVALIDATED (prior history kept); it is never inherited.
3. Gallery equality is checked independently: decode the written PNG, recompute each tile from the export bytes as recorded in the manifest, compare pixels.
4. `audit-gallery` classifies any supplied sheet VALID / INVALID / DRAFT against its manifest. Generated sheets cannot pass.
5. Canonical preflight requires the script and spec blobs to equal the pinned main blobs (recorded as git blob SHA + main SHA). Otherwise the verdict is `NON_CANONICAL` or `NOT_RUN`, never PASS.
6. K gate table with tooling-forbidden states: tooling never sets `RAW_VISUAL_APPROVED`, `DIRECTION_APPROVED`, `FAMILY_SHOWCASE_ACCEPTED`, `GIT_BINARY_PIN` or `USER_UPLOAD_READBACK` on its own. It only records director/operator evidence supplied in the ledger, and refuses inconsistent combinations.
7. Raw immutability: approved raw bytes are copied once into the closeout. They are never re-encoded, "enhanced" or substituted, and their SHA is checked again at pack time.
8. Evidence-level labels (`historical_capture` / `director_roster` / `current_live_unverified`) travel with roster rows into briefs and ledgers.
9. Write-once archives and versioned names are kept from the prototype. Earlier outputs are never overwritten.
10. Zero network: the socket-disabled test harness is kept, and the CLI has no URL fetch path. Exemplar `raw_url`s are emitted as text for humans only, with the existing rule "attach bytes, not URLs".

## 8. Director decisions requiring approval

| ID | Decision | Options | Recommendation |
| --- | --- | --- | --- |
| **D1** | P1 scope | A / B / C (§4) | **B** |
| **D2** | Integration path | (a) fresh `fable/*` branch from main, port Fable code commit only; (b) review/merge the prototype branch as-is | **(a)**. Keeps one writer per branch and avoids integrating ChatGPT docs through a Fable PR (G13) |
| **D3** | 16 BBE/BEE exemplar WebPs (1.23 MB) and RUL-2026-10-17-021 | (a) pin in the P1 PR, with sanguine_plague_v3 flagged PROVENANCE_PARTIAL; (b) pin all except v3; (c) defer binaries, keep `STYLE_REFERENCE_PIXELS_PENDING` | **(a)** if the director still stands by RUL-021; otherwise (b) |
| **D4** | Unmerged workflow authorities (ZIP-first studio doc, showcase doc, START_PROMPT/templates, RUL-2026-10-17-020) | (a) ChatGPT/director land them on main first, reconciled with P0; (b) P1 CLI cites only main authorities (`ISOLATED_ART_GENERATION.md`) and the docs follow later | **(a)**, as a separate ChatGPT-owned PR. P1 handoff waits for it, or uses (b) if it slips |
| **D5** | Gallery layout for N ≥ 10 | (a) keep "≤4 per row, final row shorter": 10 = 4+4+2, 13 = 4+4+4+1; (b) balanced, ≤4 per row, longer rows first: 10 = 4+3+3, 11 = 4+4+3, 13 = 4+3+3+3 | **(b)**. Avoids a lone tile, closer to P0 F "balanced". Art-direction call |
| **D6** | Archive when canonical preflight is NOT_RUN / NON_CANONICAL | (a) build no flat WebP ZIP; (b) build it as `*_webps_PREFLIGHT_NOT_RUN_*.zip` | **(b)**. Mobile convenience without a readiness claim |
| **D7** | Gate vocabulary | adopt retrospective K names verbatim, or keep prototype names | **adopt K** |
| **D8** | Attempt-log contents and recorder | fields per §3.3 J; studio records them; `generator_wait_ms` only when actually measured | approve as listed |
| **D9** | Canonical-preflight pin rule | script + spec blob must equal a named main SHA's blobs, else NON_CANONICAL | approve |
| **D10** | Real Aerathiel/BBE/BEE bytes as P1 fixtures | (a) synthetic fixtures only; (b) use the Aerathiel closeout ZIP (needs supply + Git pinning decision) | **(a)**. Aerathiel states stay PENDING / NOT RUN; P1 does not consume or pin them |

## 9. Not begun / boundaries

- No P1 implementation, port, branch or PR has been created. The prototype branch has not been modified.
- No independent review has been performed or claimed; selftest passes are the prototype's own evidence.
- Aerathiel: gallery acceptance PENDING; canonical preflight NOT RUN; Git binary pinning PENDING; upload/readback NOT PERFORMED. This proposal does not touch them.
- No ChatGPT-owned branch was modified. No art was generated, processed or changed.
- Live-game requests/writes **0/0**; CDN/game reads 0; credentials none.

**Next:** director decides D1–D10. On approval, Fable writes the committed P1 brief (or ChatGPT does, per the usual brief pattern), then implements on a `fable/*` branch and hands off an exact SHA for independent review.
