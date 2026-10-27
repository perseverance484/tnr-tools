# Session prompt: Headless Rider animation layers (Hellfire Harvest + Aura of Despair)

Paste the block below to the art director. It covers every raw layer still needed for both animations.

~~~text
Repository: perseverance484/tnr-tools — verify main at the latest head.
Role: Art Director, then Image Production. Live-game requests/writes: 0. Credentials: none.

READ FIRST
1. docs/handoffs/HELLFIRE_HARVEST_ANIMATION_ART_REQUEST.md
2. docs/handoffs/AURA_OF_DESPAIR_ANIMATION_ART_REQUEST.md — the director-locked version is in PR #115
   (branch chatgpt/aura-of-despair-art-lock-20261026, RUL-2026-10-26-009). If #115 is not merged yet, read it
   from that branch; section 3a is the binding visual lock.
3. docs/workflows/ISOLATED_ART_GENERATION.md
4. skills/producing-tnr-art/data/25x_DATA_art_spec.json, targets STATIC and ANIMATION.

STATUS
- Hellfire T1 SCORCH is DONE (director-approved raw, committed at
  art/halloween_headless_rider/hellfire_harvest/raws/T1_scorch_raw.png, 1254x1254, native alpha).
  Do not regenerate it. It is now the Hellfire family's STYLE reference.
- Still needed: 10 raw layers, below.

WORK ORDER (one fresh isolated session per layer, one candidate at a time, show me and wait)
Hellfire Harvest — fast, bright, orange-gold fire; the Rider's scythe:
  1. B1 SCYTHE BLADE  — the Rider's scythe blade alone, side view, pointing right, curved edge wreathed in flame.
  2. C1 SLASH ARC     — a blazing crescent slash trail, thick in the middle, tapering to points, orange core, red edge.
  3. F1 FLAME BURST   — an upward burst of flame from a flat base, front view, orange core, red edges, black smoke curl on top.
  4. G1 GRIN          — a carved jack-o-lantern grin and two triangle eyes made of light only; no pumpkin body.
  5. E1 EMBERS        — 12-16 separate glowing embers and ash flecks, 30-120 px, spaced apart.
  References per session: the Rider avatar (art/halloween_headless_rider/headless_rider_avatar.webp) STYLE ONLY,
  plus T1_scorch_raw.png STYLE/PALETTE ONLY. Never as composition.

Aura of Despair — slow, low, cold ground mist; the Rider's dead lantern light; restrained dull red (#7a1a1f), never
orange; follow section 3a of the locked request exactly:
  6. M1 MIST POOL     — the static tile: a mottled dark mist pool from above, faint underlight, feathered translucent
                        edges; no cracks, no scorch, no bright centre.
  7. L1 LANTERN FLARE — a short, restrained round flare from broken crimson edge-light and sparse rays; no lantern
                        prop, no solid disc.
  8. R1 MIST RING     — a ragged near-circular roll of black-red ground mist, slightly from above, open centre; never a
                        slash, magic circle or wall of fire.
  9. W1 WISPS         — 6-8 separate bone-grey smoke wisps; exactly two carry faint hollow, mournful faces (not
                        jack-o-lantern features).
 10. D1 GUTTER        — subdued red underlight touching the undersides of mist, broken and translucent; not a flat red
                        spot.
  References per session: the Rider avatar STYLE ONLY. Do NOT attach T1 or any Hellfire layer to an Aura session.

RULES FOR EVERY LAYER
- 1254 x 1254 (M1 may be 1024 x 1024), one element per canvas, nothing else on it.
- Native transparency; real alpha, no grey or tinted backing, no dark fringe, no checkerboard. Lime key only if
  transparency is unavailable (Hellfire only: no green in its palette; Aura: ask me first).
- Crisp pixel rendering matching the Rider avatar; dark one-pixel outlines; flat cel steps; no airbrush or bloom.
- Glow is edge light only, never a painted disc, panel or halo.
- No text, runes, symbols or franchise insignia; faces only in G1 (the grin) and W1 (two wisps).
- Hellfire and Aura must never look like the same move: no flame, ember, crack, scythe or orange in any Aura layer.
- Two wrong-subject results in one session: close it and start clean; do not lengthen the prompt.

RETURN
- Each director-approved original, unprocessed, named by layer (B1_..., C1_..., M1_..., etc.), with its approval note.
- I (Fable) do raw QC, process T1/M1 to STATIC tiles, build the strips by script (112 px square frames), preview them
  on a hex board over the River background, and build the manifests. Do not process or upload anything.
~~~
