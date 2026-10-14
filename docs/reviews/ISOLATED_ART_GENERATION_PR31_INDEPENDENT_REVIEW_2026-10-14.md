# PR #31 — Isolated art generation protocol: independent review

**Reviewer:** Fable (Claude Code)  
**Target:** `chatgpt/isolated-art-generation-protocol-20261014` at frozen head `accd14e935443de4fcec30492fb07c71a0f0765f`, base `83690aa7394e3253e1a3860b81bba0a0641577fe` (main had not moved).  
**Verdict:** PASS, docs only. Integrated into main as merge commit `f083ddecfd400431ae2160d814546dab30f54f15`.  
**Live-game requests/writes:** 0.

## What was checked

| Claim | Result |
|---|---|
| `jutsu.image` routes to the shared `ICON` target, `chroma_key: lime` | Confirmed in `25x_DATA_art_spec.json` at base. |
| `artpreflight.py` rejects an opaque RGB icon for missing alpha | Reproduced: a 256×256 opaque lossless WebP named `*_jutsu_*` drew `[alpha] mode RGB; a keyed asset must carry an alpha channel`, exit 1. |
| ICON recommends 256×256, square lossless WebP, min 160px | Confirmed. |
| `SOURCE_EVIDENCE.json` | Parses. The images are not in Git, so the recorded hashes and sizes could not be verified here; the file labels them `conversation_only_not_git_pinned`, which is accurate. |
| Doc gates at the head | `doctrinemap.py .` 0 errors/0 warnings; `render_doctrine.py --check` exit 0; `build_packs.py --check` exit 0; `lawmap.py .` 0 errors / 5 pre-existing warnings. |
| No real name, credentials or live-write authority | None found. |

## Findings

1. **Non-blocking.** RUL-2026-10-14-001 omits the ledger's **Rationale** field (`docs/RULINGS.md` entry format). Left as written; the ledger is not rewritten after the fact.
2. **Understated, corrected downstream.** The PR named only the `alpha` error. The pre-split validator also runs the residual-key check on opaque files, so any near-lime colour in a designed background draws a false `spill` error too (reproduced: 1,089 pixels on a test icon). The follow-up Lane A change below removes both for opaque jutsu icons.

## Follow-up (separate Lane A change)

The opaque-background conflict this PR recorded is reconciled on the Fable branch by a `JUTSU_ICON` spec target with `alpha: optional`, matching `artpreflight.py` handling, `--max-bytes` for the BBE cap, and selftest coverage. That change is under its own review and is not part of this PR.
