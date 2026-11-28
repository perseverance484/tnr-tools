# Jutsu Icon P1 — Final Focused Re-review (2026-10-19)

**Verdict: PASS — INTEGRATION RECOMMENDED for frozen head `f4a0d1d18ebdf7728d397761c828a925d5dc5fec`.** The remaining R1 identity gate and R2 attempt-summary defect have been corrected in the exact reviewed tree. Earlier F1–F5 fixes remain unchanged. No new blocker was found in the narrowed correction surface.

## Review identity

| Field | Exact value |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Fable branch (sole writer) | `ccr-f0d2b974-k6121h` |
| Base and merge-base | `661857510cf52e0997945f0121790aa98b794860` |
| Prior reviewed head | `78c8c9801caa3b344e64ebaf5b5e4b29909ce38a` |
| Final frozen review head | `f4a0d1d18ebdf7728d397761c828a925d5dc5fec` |
| Integration target checked | `main@24006047fcbe440f6d02208f406177bf1d49c7a7` (one unrelated harvest commit ahead of base) |
| Correction commits | `bd7d63710d5fe4f4401b4bb7265a682643cc6196` + bot skillpack `f4a0d1d1` |
| Prior review | `chatgpt/review-jutsu-icon-p1-20261019@5fea5e3f2aa4f962ce5f578bfa26330d9f6f28d1` |
| Approval | RUL-2026-10-19-005 / Option B, D1–D10; P0 RUL-2026-10-19-003 |

The live GitHub comparison confirmed the implementation branch **equals** the frozen SHA. Since the previously reviewed head, exactly three files differ: `skills/producing-tnr-art/scripts/jutsu_studio.py`, `jutsu_studio_selftest.py` and the bot-built `dist/producing-tnr-art.zip`. Source changes consist solely of the locks-only bloodline check, terminal-attempt summary, and CLI message. The previous F1–F5 implementation paths were not modified.

## Narrow corrections

**R1 / outstanding F6 — CLOSED (static verification).** At `skills/producing-tnr-art/scripts/jutsu_studio.py`, `verify_approved` compares *both* approved `bloodline.id` and `bloodline.name` with available nonempty lock identity, **regardless of whether `--source-index` is supplied**. Missing or blank approved values fail when the corresponding lock field is available; wrong IDs fail exact equality and wrong names fail the intake-equivalent `name_key` comparison. The previous skip-if-approved-ID-is-blank condition is gone. New tests cover matching identity, blank ID, missing ID, different ID and different name **with `--locks` alone**.

**R2 / attempt-summary truthfulness — CLOSED (static verification).** `approved_raw_after_attempt_n` now refers only to a terminal-approved candidate; `last_approved_attempt_n` holds an earlier historical approval independently. After an approval followed by a rejection, `approved_candidate_sha256=None`, `approved_raw_after_attempt_n=None`, and the CLI explicitly reports the terminal rejection and the historical last-approval number. Added regression checks assert both the data record and CLI output. The existing terminal-approval and global per-session one-jutsu checks remain intact.

**F1–F5 — REMAIN CLOSED.** No source edits touched the member-bound gallery acceptance, evidence sealing, terminal approval/session ownership, doctor false-green, or nonconforming gallery-layout rejection implementations. Their prior review/fixtures remain valid for this focused re-check.

## Independent verification performed

- **GitHub refs/merge-base:** branch exactly matches `f4a0d1d1`, base-to-head eight commits, main divergence one unrelated harvest-results commit, and previous-to-current diff exactly three intended files.
- **Static source/test cross-check:** 19/19 targeted assertions PASS, including R1/R2 implementation, presence and content of new regressions, preservation of representative F1–F5 guards, and pinned artpreflight/spec blob identities.
- **Independent binary verification:** fetched and decoded the *actual* committed `dist/producing-tnr-art.zip` — **170,359 bytes**, SHA-256 **`73dd4228131dc8cbf112fc89466160eb604857c856419db5e664bc516a0727ed`**, identical to Fable's claimed file hash and length. Parsed its ZIP central directory; all **16/16 included members** agree with the frozen-head source files on **uncompressed byte count and ZIP CRC32** (including both Jutsu Studio scripts, style_refs, preflight, spec, pins and SKILL). This independently supports source/package parity but is **not** a fresh run of `pack_skills.py`.
- **Canonical pin verification:** `artpreflight.py` Git blob `71ed409853c8b3da6f5b66c5c3db5ab2c9274bb4` and `25x_DATA_art_spec.json` blob `8536cd9b81da4c8f88a095af89026437a25a2c15` agree with `data/preflight_pins.json`.

**Implementer-reported only — NOT independently rerun:** Python 3.13.16 / Pillow 12.3.0 / libwebp 1.6.0: `jutsu_studio_selftest.py` 191 passed / 0 failed; `artpreflight_selftest.py` 98 / 0; `style_refs.py --selftest` and `verify` pass; `doctor --git-ref origin/main` RUN_CAPABLE_CANONICAL; doctine/render/packs/catalog guards pass; `pack_skills.py` rebuilt byte-identically; R1/R2 mutations trigger tests; prior synthetic speed benchmarks meet targets. The GitHub connector supports exact source/byte readback, but an authenticated executable local checkout was not available in this reviewer environment. Neither the full test suite nor real-art runs were independently executed.

## Integration recommendation and boundaries

**Recommend a normal reviewed Lane A integration of this exact Fable head** after re-verifying moving `main` and required GitHub checks. Do not rebase or move the frozen head without an updated handoff; do not merge this ChatGPT-owned review branch into the Fable implementation branch.

**D4 is separate:** ChatGPT-owned ZIP-first studio/showcase workflow documents and RUL-2026-10-17-020 have their own PR path. They remain outstanding; the tool may integrate independently because its current CLI cites only the already integrated `ISOLATED_ART_GENERATION.md` authority. Retrospective Option C, undecleared-collage heuristic, image-generator integration and game uploads remain outside this pass. The pinned provenance limitation on BEE Sanguine Plague remains labeled `PROVENANCE_PARTIAL`; no automatic pixel judgment is claimed.

**Aerathiel production gates unchanged:** source-faithful gallery acceptance **PENDING**, canonical artpreflight **NOT RUN**, Git binary pinning **PENDING**, user upload/readback **NOT PERFORMED**. **Live-game requests/writes: 0/0; credentials: none.** Reviewer changed only the ChatGPT-owned review branch; no Fable-branch changes or merge performed.
