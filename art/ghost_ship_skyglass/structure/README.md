# Skyglass Wreck world-map structure

| Fact | Value |
| --- | --- |
| Use | Map structure (`mapAsset`, category "structure") for the Skyglass Wreck dungeon entrance |
| Chosen | Concept 1, Beached wreck (RUL-2026-10-24-022). Hovering and Rising were generated and not chosen |
| Prompt | `docs/handoffs/SKYGLASS_WRECK_STRUCTURE_ART_SESSION_PROMPTS.md`, concept 1; subject ref `../quest_icon_ghost_ship_skyglass.webp` |
| Raw | `raw_skyglass_wreck_structure_beached.png`, 1254 x 1254, magenta key |
| Export | `structure_skyglass_wreck_beached_v1.png`, 512 x 476 RGBA PNG: keyed with `skills/producing-tnr-art/scripts/chroma.py --key magenta`, trimmed with a 3% margin, Lanczos to 512 px longest side |
| Hashes | `SHA256SUMS.txt` |
| Not done | No upload, no live record, no renderScale/entrance scale chosen. `25x_DATA_art_spec.json` has no map-structure target yet, so `artpreflight.py` does not cover this file |
