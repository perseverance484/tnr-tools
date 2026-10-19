# Jutsu Icon P1 — Frozen-SHA Focused Correction Re-review (2026-10-19)

**Verdict: CORRECTIONS MOSTLY VERIFIED / ONE MEDIUM ISSUE REMAINS — HOLD INTEGRATION AT THIS SHA.** The original four blockers are closed at source level; F5 is closed; F6 is **partially** closed. One additional low-severity reporting discrepancy is recorded. No wider scope or P0/Option B regression found in the changed paths.

| Field | Verified pin |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Fable sole-writer branch | `ccr-f0d2b974-k6121h` |
| Base and merge-base | `661857510cf52e0997945f0121790aa98b794860` (not rebased) |
| Previous reviewed head | `0db856bb4b35a6d28eacb49467e068ffe3d99ae3` |
| New frozen head | `78c8c9801caa3b344e64ebaf5b5e4b29909ce38a` (branch ref identical at review) |
| Integration target | `main@24006047fcbe440f6d02208f406177bf1d49c7a7` (one unrelated harvest result since base) |
| Earlier review | `chatgpt/review-jutsu-icon-p1-20261019@b8fdafdc73aee4d781714a69f94ec4178a5ef3e6` |
| Governing approval | RUL-2026-10-19-005 / Option B D1–D10; P0 RUL-2026-10-19-003 |
| Source code changed since prior | `skills/producing-tnr-art/scripts/jutsu_studio.py`, `jutsu_studio_selftest.py`, rebuilt `dist/producing-tnr-art.zip` |

## Focused finding closure

| Earlier finding | Status | Evidence at new frozen head |
| --- | --- | --- |
| **F1 BLOCKER** Gallery acceptance survives changed source bytes | **CLOSED (static)** | `members_commitment` hashes the ordered `[jutsu_id, approved_raw_sha256, output_sha256]` list; `acceptance_for` requires member match *and* either matching gallery file SHA or matching decoded-pixel SHA, never comparing across hash domains. New fixtures cover metadata-only raw change, re-encoded gallery, changed export hash, missing commitment. |
| **F2 BLOCKER** Swapped lock/attempt records sealed after verification | **CLOSED (static)** | `verify_approved` captures the exact approved, lock and attempts bytes once; `check_locks` and `check_attempts` parse captured bytes; pack re-hashes all three files via `read_verified` and seals the captured bytes. Swap-after-showcase regressions cover each one; records have ledger SHA fields. |
| **F3 BLOCKER** Nonterminal approval and shared sessions | **CLOSED (static)** | Terminal attempt must be `approved` and match raw SHA; global `session_owner` prevents cross-jutsu `session_id` reuse; regression tests cover old acceptance then rejection, fresh reaffirmation, shared ID. See small reporting note below. |
| **F4 BLOCKER** Doctor false-green | **CLOSED (static)** | Any failed required/requested check except pin mismatch yields `NOT_READY` and nonzero exit; pin mismatch retains `RUN_CAPABLE_NON_CANONICAL`, never canonical green; regressions cover nonexistent `--git-ref` and nondeterministic encoder. |
| **F5 MEDIUM** Outdated layouts externally audit VALID | **CLOSED (static)** | `LAYOUT_NONCONFORMING` is now a problem and prevents VALID. Independent `pixel_fidelity`/layout statuses make a faithful archival 4+4+2 sheet invalid as final. N=10 fixture added. |
| **F6 MEDIUM** Bloodline identity drifts from intake | **PARTIALLY CLOSED** | If `--source-index` is supplied, both intake `bloodline.id` and `.name` must match the approved ledger, and missing approved ID is refused. But locks-only mode has an unclosed empty-ID/name case below. |

## R1 — MEDIUM / Remaining F6: locks-only path can finalize missing or wrong bloodline identity

**Location:** `skills/producing-tnr-art/scripts/jutsu_studio.py`, `verify_approved` locks block at approximately lines 1293–1303 (frozen head `78c8c980`). The check is conditional:

```python
if bl.get("id") not in (None, "") and lock_info["doc"].get("bloodline", {}).get("id") != bl.get("id"):
    errs.append(...)
```

**Reproduction from control flow:** take an otherwise valid approved ledger and lock file (the existing synthetic `family(...)` and `lock_doc(...)` fixtures suffice). Remove `approved.json.bloodline.id`, or set it to an empty string; use `verify_approved(..., locks=locks_path)` **without** `source_index`. The new source-index checks do not execute, and the lock comparison skips empty approved IDs. Despite the approved lock containing exact `bloodline.id`, the ledger is accepted with no bloodline ID. A wrong `approved.json.bloodline.name` also passes locks-only comparison because only ID is compared. This is distinct from the fixed `--source-index` reproduction.

**Requirement:** Original F6 correction recommendation expressly said require nonempty ID whenever the source **or lock** supplies one; P0 target lock preserves immutable bloodline identity. The accepted lock and exported approved ledger should not silently disagree about the family.

**Smallest fix:** with `--locks`, require approved `bloodline.id` to equal the nonempty lock ID, including rejection of blank/missing IDs. When the lock supplies `bloodline.name`, compare that too (using the same non-lossy/normalized name policy as intake). Add two socket-free tests: blank ID with locks but no source-index; inconsistent name with locks but no source-index. No new user decision is needed.

**Consequence:** Incorrect/missing family identity may reach the closeout/gallery metadata under a `DIRECTION_APPROVED` lock without an available exact-identity equality check. No live write is possible from this CLI, but provenance and operator trust are affected.

## R2 — LOW / Attempt summary can print “approved at N” after terminal rejection

**Location:** `check_attempts` and the `attempts` CLI output. After a jutsu's earlier approved attempt is followed by a terminal rejection, `approved_candidate_sha256` becomes `None` (correct) and `verify_approved` refuses finalize (correct), but `approved_raw_after_attempt_n` retains `approved_n` from the earlier attempt, and the CLI still prints `approved at <n>` without noting `terminal_outcome=rejected`.

**Smallest fix:** report `approved_raw_after_attempt_n` only for a currently terminal-approved raw, or label the last historical approval separately and always show terminal state. This is a truthful reporting refinement, not a blocker by itself.

## Verification and boundaries

1. **Repository/readback:** Current main remains `24006047fcbe440f6d02208f406177bf1d49c7a7`, frozen implementation branch equals `78c8c9801caa3b344e64ebaf5b5e4b29909ce38a`, and the change since the prior frozen head contains exactly the CLI, selftest and bot rebuilt skill ZIP.
2. **Independent static checks:** inspected the corrected source paths, their adversarial regression test bodies and all six earlier findings. Targeted source-level assertions verified the changed control-flow guards and the two residual conditions. This is not an independently executed Python selftest.
3. **Independent artifact-byte verification:** fetched the actual `dist/producing-tnr-art.zip` at the frozen SHA, decoded its 169,908 bytes and computed SHA-256 **`9feb16157a9ce0f52f277fe3127f25996da4c2aaa44dc0c5b0cee3e05623be04`**. Central directory contains 16 members, including the CLI, selftest, style_refs, spec pins and SKILL.md. This confirms the reported binary/hash and expected membership; **not** byte-for-byte source-to-bundle regeneration parity.
4. **Canonical pins unchanged:** `artpreflight.py` Git blob `71ed409853c8b3da6f5b66c5c3db5ab2c9274bb4`; art spec blob `8536cd9b81da4c8f88a095af89026437a25a2c15`. Both agree with `preflight_pins.json` and the pinned named main ref.
5. **Reported by Fable (not independently rerun here):** studio 184/0, preflight 98/0, style-reference verification, doctor canonical pass, doctrine/pack guards, deterministic package rebuild and N=12 synthetic benchmarks (2137ms full export; 159ms 1-icon export; 2908ms full finalize). Network to github.com is unavailable in the local execution environment; GitHub repository connector enabled the source/byte readback only. No real-art, Aerathiel, browser or game runs.
6. **D4/authority boundary:** ChatGPT-owned ZIP-first/showcase docs PR remains separate; CLI cites current merged main protocol. Do not co-merge those docs through this implementation branch.

**Integration gate:** Existing F1–F4 blockers and F5 are satisfied, but original F6 identity invariant remains unmet in the locks-only case. Request a **minimal** F6 patch and optionally R2 cleanup on Fable's own branch, new frozen SHA, focused review of that diff and tests; do not merge the reviewed `78c8c980` head. No architecture redesign needed.

**Aerathiel:** exact gallery acceptance PENDING; its canonical preflight NOT RUN; Git binary pinning PENDING; user upload/readback NOT PERFORMED. **Game requests/writes 0/0. Credentials none.** Review-only Git branch, no Fable-branch mutation.
