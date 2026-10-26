# Crownhold art

- `avatar_crownhold_arakane.webp`: Supreme Commander Arakane, AI avatar (RUL-2026-10-25-011), keyed from
  `raw/raw_avatar_crownhold_arakane.png` with `chroma.py --target AI_AVATAR --key magenta` (rawqc ACCEPT, ring purity
  0.9998; 1239 px, lossless webp, 283 KB). Source: the director's isolated session, 2026-10-25, from
  `docs/handoffs/CROWNHOLD_CROWN_ART_REQUEST.md` #1. It locks the Command Crown: gold spiked circlet, floating Skyglass
  blades with a seal ring at the centre, control threads. Masked and robed rather than the brief's bare-faced armoured
  warlord; the director's call. Review: `review/qc_arakane.png`, `review/sheet_arakane_vs_captain.png`.
- `icon-badge-crownbreaker.webp`: Crownbreaker badge icon (art batch #5, RUL-2026-10-25-011), keyed from
  `raw/raw_icon_badge_crownbreaker.png` with `chroma.py --target ICON --key magenta` (rawqc ACCEPT, ring purity 0.9998),
  1208 -> 256 px lossless webp (90390 bytes); artpreflight --type ICON 0/0. Director-approved 2026-10-25. Departs from the
  bible prompt by the director's acceptance: a round gold medallion frame with a dark backdrop (prompt said no frame) and
  a smoother rendering than the pixel set. The director uploads this when creating the badge by hand; no SWAPS row.
- `avatar_crownhold_master_of_arms.webp`, `avatar_crownhold_replicant_zero.webp`, `avatar_crownhold_the_grand_marshal.webp`,
  `avatar_crownhold_proving_proctor.webp`: art batch #8-#11, keyed from `raw/` with `chroma.py --target AI_AVATAR --key
  magenta` (rawqc ACCEPT each), native size lossless webp, then the control thread erased with
  `state/skyglass_art/dethread.py` (director 2026-10-26: the thread cut off at the frame edge reads as an antenna on the
  moving combat sprite). artpreflight --type AI_AVATAR 0/0.
- Art batch #14-#20 (Calibration Duelist, Skyglass Archive Keeper, Impression Containment Warden, Unstable Echo Subject,
  Failed Reconstruction Prototype, Command Signal Adjutant, High Command Staff Tactician): `avatar_crownhold_<name>.webp`,
  keyed from `raw/` with `chroma.py --target AI_AVATAR --key magenta` (rawqc ACCEPT each), native size lossless webp, no
  thread to erase; artpreflight --type AI_AVATAR 0/0.
- `avatar_crownhold_master_of_arms.webp` replaced 2026-10-26 by the RUL-2026-10-26-001 version (Seal Charge pixel-style reference; iron half-helm, orange face guard, axe and cleaver). Director-approved.
