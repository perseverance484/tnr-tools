# Jutsu Icon P1 Tooling — Independent Frozen-SHA Review (2026-10-19)

**Verdict: CHANGES REQUIRED / DO NOT MERGE.** Four blocking issues and two contract refinements. This is an independent **static GitHub-tree audit**, not an independently executed Python test run.

| Field | Pin |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Implementation owner / branch | Fable, sole writer on `ccr-f0d2b974-k6121h` |
| Base and merge-base | `661857510cf52e0997945f0121790aa98b794860` |
| Frozen reviewed head | `0db856bb4b35a6d28eacb49467e068ffe3d99ae3` |
| Integration target at review | `main@24006047fcbe440f6d02208f406177bf1d49c7a7` (one unrelated harvest commit ahead) |
| Review branch | `chatgpt/review-jutsu-icon-p1-20261019` (not the implementation branch) |
| Approval | RUL-2026-10-19-005 Option B / D1–D10 |
| Build contract | `state/prompt_jutsu_icon_p1_tooling_20261019.md` |
| Governing P0 | `docs/workflows/ISOLATED_ART_GENERATION.md` / RUL-2026-10-19-003 |

Verified from the GitHub connector: the implementation branch still points at the frozen head; it is four commits ahead of its base and has not rebased. The main divergence is a single unrelated harvest file. The script/spec blobs at both the frozen head and pinned `main@f620db3d934fbb5a13effa5f90ed25bf16a33718` are `71ed409853c8b3da6f5b66c5c3db5ab2c9274bb4` and `8536cd9b81da4c8f88a095af89026437a25a2c15`, matching `preflight_pins.json`. Scope excludes game source, game requests, credentials and live operations.

## Findings — exact reviewed tree

### F1 — BLOCKER / Source acceptance can survive changed raw and export provenance

**Location:** `skills/producing-tnr-art/scripts/jutsu_studio.py:1572–1590` (`acceptance_for`), `:1663–1713` (`build_showcase`). The acceptance check receives only the newly rendered gallery's file SHA and decoded-pixel SHA. It never checks the **previously accepted member raw/export SHA set**, even though those SHA values are in the current showcase manifest.

**Reproduction path:** accept gallery G, then re-encode a previously approved PNG raw with different ancillary metadata but identical decoded pixels; approve the new raw, bump its export version, and rebuild. The raw SHA changes, but the lossless export pixels, gallery tile pixels, captions and potentially the entire gallery PNG remain identical. `acceptance_for` returns `ACCEPTED` for G rather than `INVALIDATED`. Re-encoding an export into different but pixel-equivalent bytes creates the same omission. A separate cross-environment problem is that a previously accepted **file** SHA cannot be compared to a new **pixel** SHA to prove pixel identity on PNG re-encoding; those are different hash domains.

**Contract:** P0 F5 invalidates a gallery after changed source bytes; approved P1 proposal §7.2 explicitly binds acceptance to gallery SHA **plus member export SHAs**. The one-raw-visually-changed selftest does not cover pixel-equivalent byte changes.

**Smallest correction:** record and compare immutable accepted family member raw/export SHAs (ordered ID/hash commitment) as well as the accepted gallery file/pixel identities; preserve the prior evidence and mark any changed member bytes `INVALIDATED`. Add metadata-only-raw and pixel-equivalent-export tests, plus a re-encoded gallery test.

### F2 — BLOCKER / Packed lock and attempt evidence is not reverified

**Location:** `jutsu_studio.py:1114–1284` verifies lock/attempt records; `:1818–1912` builds the archives. Packing uses `Path(locks).read_bytes()` and `Path(attempts).read_bytes()` directly, unlike raw/export/showcase members protected by `read_verified`.

**Reproduction path:** run a valid finalize with `--locks` and `--attempts` and use the existing test-only `on_stage("showcase")` hook to overwrite either JSON record with conflicting or malformed content. The subsequent pack path seals the changed JSON under `manifest/locks.json` or `manifest/attempts.json` while `studio_ledger.json` retains the earlier, checked approval and statistics. It can return successful archives with contradictory approval evidence.

**Contract:** source-fidelity rehash at every use (§7.1), truthful provenance, P0 exact approved lock/attempt binding.

**Smallest correction:** capture SHA and preferably immutable verified bytes for both inputs during verification, and pack only those bytes after an unchanged-on-disk check. Add two injection tests (lock swap, attempt swap) requiring refusal before archive publication.

### F3 — BLOCKER / Attempt records allow nonterminal approval and reuse of an isolated session by another jutsu

**Location:** `jutsu_studio.py:993–1103` groups attempts by jutsu; `:1070–1086` retains the last *approved* SHA irrespective of later outcomes; `:1267–1281` compares that SHA with the final raw. Each jutsu has an independent `session_id` streak map; no global session-to-target ownership exists.

**Reproduction A:** attempt 1 for J0 is `approved` with raw SHA A, then attempt 2 is `rejected` for quality in a valid session. `approved_candidate_sha256` remains A; `verify_approved` accepts raw A because it checks last *approved* attempt, not the **terminal** attempt. This contradicts proposed adversarial test 19 ("latest attempt is recorded as rejected" must refuse). The current selftest checks only *wrong SHA* on an approved attempt.

**Reproduction B:** J0 attempt 1 and J1 attempt 1 both identify `session_id="shared"` and can independently be approved. `check_attempts` accepts the record, despite P0's one-jutsu-per-isolated-conversation rule.

**Smallest correction:** enforce that the terminal attempt for each finalized jutsu is `approved` and SHA-bound (or require a fresh explicit terminal reaffirmation if reverting). Enforce one jutsu identity per session ID globally. Cover both with fixtures.

### F4 — BLOCKER / `doctor` can exit green while its own checks fail

**Location:** `jutsu_studio.py:2013–2071`, `:2163–2174`. `doctor` accumulates failed checks but its terminal verdict uses only `reason` and `canonical["canonical"]`; it does not require all necessary/requested checks to be `ok`.

**Reproduction path:** in a canonical checkout run `doctor --git-ref does-not-exist`. The requested `git_ref_blobs` check fails, but `reason` is never set by that failure and the local pins still match. `doctor` returns `RUN_CAPABLE_CANONICAL` and CLI exits 0 despite a visible `FAIL` check. Similarly, a false `webp_lossless` or `encoder_determinism` check does not itself block a green verdict when the probe subprocess succeeds. This is a **doctor/readiness** false-green, not evidence that `run_preflight` misclassifies a modified script: its script/spec blob comparison itself correctly returns NON_CANONICAL on mismatch.

**Smallest correction:** make every essential or expressly requested failed doctor check block a green verdict/exit 0; distinguish absent optional `--git-ref` from a supplied ref whose comparison failed. Add missing-ref and mocked encoder-failure tests.

### F5 — MEDIUM / External gallery can audit VALID with a rejected N>=10 layout

**Location:** `jutsu_studio.py:1591–1662`. When `manifest.row_lengths` differs from the director-approved `grid_rows(N)`, `audit_gallery` adds only a `LAYOUT_RULE_OUTDATED` **note**, not a problem, so a faithfully rendered 10-icon 4+4+2 sheet with a matching manifest can return `VALID`.

**Contract:** RUL-2026-10-19-005 D5 requires 10=4+3+3; P0 F2 balanced count-adaptive grid. `build_showcase` generates correct rows; the gap is **external audit**.

**Smallest correction:** refuse nonconforming row lengths in final-validity mode, or emit an explicitly separate archival pixel-fidelity status that is never confused with a valid final gallery. Add 10-icon outdated-layout fixture.

### F6 — MEDIUM / Source-index roster check can miss a changed bloodline identity

**Location:** `jutsu_studio.py:1248–1279`. With `--source-index` but no `--locks`, `verify_approved` checks set equality of jutsu IDs and names but never compares the intake `bloodline.id` with `approved.json.bloodline.id`. The approved bloodline ID is not independently required to be nonempty. Lock-based protection applies only when the optional `--locks` is supplied and the approved ID is nonempty.

**Reproduction path:** with matching J0–Jn names and IDs, change only approved `bloodline.id` to an unrelated ID and run `verify-approved --source-index` without locks; it can pass. This defeats an available exact-identity cross-check.

**Smallest correction:** on any supplied intake index, compare all known authoritative bloodline identity fields to the approved ledger; require a nonempty ID when the source/lock has one. Add mismatched/missing-ID tests.

## What held / limits

- The exact reviewed branch/head/base relationship is confirmed. No Fable branch edits were made.
- `run_preflight` checks script/spec git blobs against the pinned data and does not report PASS when they differ and the checker returns cleanly.
- The export/readback path contains VP8L mode/size/decoded-pixel checks, versioned cache paths and raw/export SHA checks; gallery tiles are independently recomputed from verified export bytes. Written gallery hash is checked again on packing.
- New flat-archive names carry the preflight verdict and do not claim upload readiness.
- `style_refs.py` visibly flags `bee_sanguine_plague` as `PROVENANCE_PARTIAL`; the admitted missing undeclared-collage heuristic is known, not a newly discovered defect.
- The author reports 160/0 selftests, 98/0 artpreflight checks, style-ref verification, green doctrine/pack checks, doctor and benchmark targets. **These are not independently reproduced:** the GitHub connector supplies repository content but no executable checkout to this reviewer; container GitHub DNS was unavailable. Independent work here consisted of source-level control-flow tracing and targeted static assertions, not running those Python suites, image-byte comparisons, a bundle rebuild or real-art tests.
- The checked-in `dist/producing-tnr-art.zip` rebuild is author-reported reproducible but not independently rebuilt in this review. Synthetic-only P1 tests and no real Aerathiel/BBE/BEE raw processing respect D10.

## Correction / return gate

Fable is the sole implementation writer: correct F1–F4, and close F5/F6 or explicitly document any remaining mismatch for director disposition. Add adversarial selftests matching the above reproductions, rerun all existing required P1/skill/pack guards, and freeze a **new exact implementation SHA**. Return that for an independent focused re-review, including fresh bundle parity. Do not merge this frozen head.

**Aerathiel boundaries preserved:** deterministic gallery acceptance PENDING; canonical artpreflight NOT RUN; Git binary pinning PENDING; user upload/readback NOT PERFORMED. **Live game requests/writes:** 0/0. **Credentials:** none. **Repository writes:** this independent review branch only, not the implementation branch.
