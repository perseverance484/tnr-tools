# Wave workflow — agreed 2026-08-30, build+harden next session
One art wave, one thread, one pack, one press.

1. Session open; fix the wave scope (asset type + list).
2. Thread init: init prompt + style reference attached by dauntless; sprite
   references attached per-card for characters with existing designs.
3. Per asset, depth-2 pipelined: card -> gen -> rawqc/chroma/preflight ->
   dark-composite QC -> dauntless approve -> ledger. One gen per card, QC
   between.
4. Asset sheet composed from the processed set (house sheet style).
5. ONE push pack staged: zip at push/ (manifest.json + every image at zip
   root, imgSizes ledger). No picker, ever. Dauntless presses Repo -> Build
   once.
6. Inbound results bundle: harvest.py verify (per-entry json.success);
   live ids ledgered.
7. Close out (digest patch + session_close).

Wiring (@scene refs into quest registries) is its own later manifest, gated
on speak-map rulings. Art generation itself stays manual in the ChatGPT
thread.
