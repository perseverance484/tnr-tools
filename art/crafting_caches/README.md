# Crafting caches art: 3 director-approved icons

These are the immutable bytes for push/97 (crafting caches release step A, RUL-2026-10-13-001..004). Binding happens by commit SHA (`imagePack.ref`), never by branch name.

| Fact | Value |
| --- | --- |
| Source | Director-supplied WebPs, 2026-10-13, generated from `docs/handoffs/CRAFTING_CACHES_IMAGE_GEN_HANDOFF.md` (branch `claude/crafting-recipe-census-pln5za`) |
| Files | `icon-medicine-inro.webp`, `icon-shinobi-tool-pouch.webp`, `icon-sages-strongbox.webp`: each 256×256, lossless WebP, RGBA with a transparent background, 42–57 KB |
| Hashes | `_provenance/SHA256SUMS.txt` (`sha256sum -c`) |
| Canonical preflight | `skills/producing-tnr-art/scripts/artpreflight.py` (blob `b5fae81`) with spec `25x_DATA_art_spec.json` (blob `688b4ed`), `--type ICON`: **0 errors, 0 warnings, 3 files**. Full output: `_provenance/artpreflight.json` |
| Edge QC | Composited on a dark background: no key-colour fringe. The Inro's green pixels are its jade accent: none sit on a soft edge and none is pure #00FF00 |
| Release binding | push/97 binds all three by path, sha256 and bytes |

No live-game requests, uploads or publication happened at intake.
