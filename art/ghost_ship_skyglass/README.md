# Ghost Ship / Skyglass art: 34 director-approved WebPs

These are the immutable bytes for push/90. Binding happens by commit SHA (`imagePack.ref`), never by branch name.

| Fact | Value |
| --- | --- |
| Source | Director-supplied `ghost_ship_skyglass_34_director_approved_webps_2026-10-11.zip`: 34 flat WebPs, visually approved |
| Evidence | `ghost_ship_skyglass_34_art_validation_handoff_2026-10-11.zip`: report, ledger, slot proposal and hashes in `_provenance/`. The two raw PNG sources are verified against `RAW_SOURCES_SHA256SUMS.txt` but not committed |
| Hashes | All 34 files match `_provenance/SHA256SUMS.txt` (`sha256sum -c`) |
| Canonical preflight | `skills/producing-tnr-art/scripts/artpreflight.py` (blob `b5fae818`) with spec `25x_DATA_art_spec.json` (blob `688b4ed6`) gives **0 errors, 2 warnings, 34 files**. The warnings are non-blocking oversize notes: the Serum icon is 768px and the quest icon 1202px, against a delivered 125px. Full output: `_provenance/artpreflight_canonical.json` |
| Release binding | 10 required slots in `state/ghost_ship_skyglass_release_art.json` (see `_provenance/ART_SLOT_INTAKE_PROPOSAL.json`) |
| Not bound | The other 24 files (renamed-AI avatars, existing-scene replacements, Serum/Crown/Fragment icons, quest icon) are committed for a deliberate optional-replacement decision. None of them is wired to a live record |

No live-game requests, uploads or publication happened at intake.
