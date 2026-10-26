# Art request: Ethereal Rebirth animation, ribbons in the icon's style (v5)

- **Director, 2026-10-24:** "Draw the ribbons as they appear in the icon. Exactly. Map it out to look just like the icon.
  If you need new assets say so."
- **Why new assets:** the v2 ribbon layers are narrow, opaque, saturated strokes with a wavy centre line; the icon's ribbons
  are broad, flat, translucent bands that twist. No warp can turn one into the other.
- **Reference (attach):** the approved icon `art/jutsu_icons/ethereal_rebirth/exports/icon_jutsu_ethereal_rebirth_v1.webp`
  (full-size raw: `candidates/round3/raw_ethereal_rebirth_final.png`) and three close-ups of its ribbons in
  `art/jutsu_icons/ethereal_rebirth/animation/raws/`: `ref_icon_ribbon_gold.png`, `ref_icon_ribbon_blue.png`,
  `ref_icon_ribbon_gold_whip.png`.
- **Kept:** the v1 starburst core (director's choice) and the v4 motion (centred on the portrait, start behind, orbit
  round in front, the gold ribbon lashes out; mask only on passes behind the avatar).
- **Live-game requests/writes:** 0.

## What the icon's ribbons look like

- **Broad, flat bands** like silk or light-cloth, about a fifth as wide as they are long, that **twist**: in places the band
  turns edge-on and narrows to a bright line, then opens again.
- **Translucent and glassy:** the inside is a pale, see-through wash with soft lighter streaks running along it; the
  background shows through.
- **Bright edges:** each long edge is a crisp near-white line; outside it, a soft glow (warm amber for gold, deep
  blue for blue).
- **Colours:** gold: pale cream `#fef383` to white, amber glow `#e27d1b`. Blue: icy `#9aa4d2` to `#75dcff`, white
  edges, deep-blue glow `#286aec` / `#2676e1`.
- **Ends:** long, tapering whip tips, the tip curling slightly.
- **Sparkles:** small, thin **four-point stars** (long vertical and horizontal points, no diamond body), white with a
  warm or cool tint.

## Deliverables (transparent PNG, nothing else on the canvas)

| Layer | What | Size |
|---|---|---|
| **R1 GOLD BAND** | one gold ribbon in the icon's style, painted **straight and flat, face-on, horizontal**: an even width along most of its length, one end a long tapering whip tip (right end), the other a soft fade (left end). No twist painted in (the script twists it). | 1600 × 300, band about 220 px wide |
| **R2 BLUE BAND** | the same in the icon's blue | 1600 × 300 |
| **S1 SPARKLES** | 8–10 separate thin four-point stars as in the icon, mixed sizes (40–120 px), white-gold and white-blue, spaced apart | 1254 × 1254 |

Rules: premium TNR pixel art matching the icon's finish; real transparency (the glow fades to clear, no grey or tinted
panel behind, no border); no text, figures or symbols; non-elemental (no fire, water or lightning).

## Intake (Claude Code)

The script bends each band along the v4 orbit, twists it (narrowing it to a bright edge where it turns, darkening the
back face), places the passes behind the avatar under the portrait mask, and lays out the peak frame to match the icon:
blue looping round the portrait's upper half, gold sweeping round the lower half and whipping out to the upper right,
sparkles around it. Then the usual preview over the director's avatar.
