# Art request: Arakane's Command Crown (Arakane avatar, Crownbreaker badge)

- **Director, 2026-10-25:** "Crownbreaker. And now Arakane needs a cool Crown, and the badge is that Crown breaking. So he
  needs a better Crown than the captain. Its how they control the other afterimages" (RUL-2026-10-25-011).
- **2026-10-26:** the gold design below is **RETIRED**. The director moved Arakane's gold avatar to the redo queue
  (RUL-2026-10-26-002); the control threads were dropped (RUL-2026-10-26-001: they read as antennae on the moving combat
  sprite). The art director's v0.4 handoff locks a new crown.
- **Live-game requests/writes:** 0.

## Current design (art bible v0.4, PROPOSED)

- **Crown lock and Arakane's design:** `docs/design/ghost_ship_art_bible/roster.json` (entry 20, `crown`), explained in
  `ART_BIBLE.md` section 6.7. Blackened-iron closed ring, seven seal notches, one cyan seal stone, seven floating
  skyglass blades; no gold, no threads, no halo.
- **Prompts:** generated, never written here. Arakane is **brief A** in `docs/handoffs/SKYGLASS_CROWNHOLD_ART_BATCH.md`
  (delivers `avatar_crownhold_arakane_v2.webp`; the old avatar is kept). The Crownbreaker badge is **#5** there, with #46,
  #47 and #48.
- **Order:** brief A first. #5 and #46-#48 are BLOCKED until A is approved and committed; rerunning
  `state/skyglass_art/build_art_batch.py` then attaches the approved avatar to them as SUBJECT.

## Retired (history only; do not use)

The 2026-10-25 lock asked for a closed circlet of **blackened gold** engraved with seal-script, a halo of seven floating
skyglass blades, a large prism core with a pale circled-cross seal burning white, and **thin glowing control threads**
running from each blade out of frame. Its two prompts attached the Crowned Captain as style and the Captain's crown as a
"lesser crown". The resulting avatar (`art/crownhold/avatar_crownhold_arakane.webp`) is live and hidden, and is now
off-model. Its prompts are in this file's git history (`git log -p -- docs/handoffs/CROWNHOLD_CROWN_ART_REQUEST.md`).

## Intake (Claude Code)

Key magenta with `chroma.py` (see the open chroma-key contract issue in `ART_BIBLE.md` section 13); avatar to the
AI_AVATAR target, badge to the ICON target (`25x_DATA_art_spec.json`); review sheet against the anchor crew and the
Crowned Captain's crown.
