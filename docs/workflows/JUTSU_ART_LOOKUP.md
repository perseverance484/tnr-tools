# Workflow — Jutsu art lookup

Use when an art session needs the **current live image** of an existing jutsu: name → captured
record → image URL. Tool: `scripts/jutsu_art.py`. Derived output: `answers/jutsu_art.json`
(generated; never hand-edit).

## Sources

The corpus is pinned in `SOURCES` inside the script:

- **#68–#74** — seven completed Forge capture-only batches of exact `jutsu.get` full-record reads
  (604 records, tranches of the #67 target list, in order).
- **#67** manifest — the 604-id target list the batches must reproduce ordinal for ordinal.
- **#66** partial bundle — used only for its completed `jutsu.getAllNames` row count (coverage).
- `answers/names_jutsu.json` + `answers/hot.json` — today's known jutsu id count, printed by
  `build`/`verify` as a **diagnostic only**. It is never written to the output and never changes
  coverage status.

Eligibility follows the #66 inclusion policy: live `hidden` exactly false, live `jutsuType` in
NORMAL/SPECIAL/FORBIDDEN/LOYALTY/CLAN/EVENT, live `bloodlineId` empty. Current corpus:
**604 captured / 441 eligible / 440 unique image URLs** (one URL is shared by two records).

## Provenance

`build`, `verify` and `record` re-derive from the bundles and **fail closed** (exit 2) on any
bundle state/outcome, capture count, persist status, snapshot key, input/record id, or manifest
hash mismatch (the hash is Forge's FNV-1a identity, recomputed from the committed manifest), and
when derived counts differ from the pinned expectations. `verify` also fails (exit 1) when
`answers/jutsu_art.json` is not byte-identical to a fresh derivation.

**Known caveat — preserved, not resolved:** live `jutsu.getAllNames` returned 1,493 rows (#66)
against 1,491 repository ids known at census time. Two live rows were never classified; the
census is exhaustive only over the known candidate set. The status is pinned `UNRESOLVED` in
`SOURCES` together with both counts, and every `build`/`verify` and every lookup miss prints the
warning. Catalog growth cannot clear it: two unrelated new ids would make today's count 1,493
without classifying anything. Only a reviewed change that adopts follow-up capture evidence
identifying and classifying the missing rows may resolve it; pinning a different status or a
`resolution` without that evidence check fails closed.

## Commands

```
python3 scripts/jutsu_art.py verify                 # always first in a session
python3 scripts/jutsu_art.py lookup "Name" [--json]
python3 scripts/jutsu_art.py image-url "Name"       # bare URL; excluded records need --any
python3 scripts/jutsu_art.py search fang [--all]
python3 scripts/jutsu_art.py record "Name"          # full captured record + bundle provenance
python3 scripts/jutsu_art.py materialize "Name" ... --out DIR [--dry-run]
python3 scripts/jutsu_art.py build                  # only after a deliberate SOURCES change
```

`--id` on lookup/record/image-url/materialize takes an exact record id instead of a name.

## Lookup policy

Normalized exact match only: NFKC, curly quotes folded to ASCII, whitespace collapsed and
trimmed, casefolded. A miss exits 1 and lists suggestions **that are never selected**; the
operator re-runs with the exact name. A normalized name that maps to more than one id refuses to
resolve and asks for `--id`.

## Network boundary

Zero TNR requests in every command. `materialize` is the only networked command: HTTPS to the
allowlisted asset CDNs only (redirects re-checked), game hosts refused outright. It is
all-or-nothing:

1. every name resolves and is eligible, and any existing `materialized.json` is verified against
   the files it names (missing file, hash mismatch, or unreadable index → refused), before the
   first request;
2. every image is fetched **and fully decoded with Pillow, every frame** (signature must agree
   with the decoded format; header-only or truncated bytes are rejected; animated GIF/WebP are
   kept as served);
3. only then are files staged as temps in the output directory and swapped in with
   `os.replace`, index last. A fetch or decode failure leaves the previous files and index
   byte-for-byte unchanged; an unindexed file at a target path is never overwritten.

Files are `<id>.<ext>`; the index records url, bytes, sha256, dimensions and frame count.
Requires Pillow (approved art dependency). Tests are socket-free:
`python3 -m unittest scripts/test_jutsu_art.py`.

## Not yet built

Phase 2 — a rotating active workspace of ~10 materialized icons for an art session — has not
begun. `materialize --out` is its building block; workspace rotation/eviction policy is open.
