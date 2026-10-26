# Bandit war camp avatars: art session prompt (round 1)

- **Brief:** `docs/design/characters/BANDIT_WAR_CAMP_AVATARS.md`.
- **Goal:** six house-style AI sprites that replace the six painted war-camp portraits, one per fighter, each in its own
  isolated session. The director picks.
- **Live-game requests/writes:** 0. Credentials: none.

~~~text
You are the art director for The Ninja RPG (repository perseverance484/tnr-tools). This session redraws ONE AI avatar as a
TNR house-style pixel sprite. Run each of the six fighters below in its own fresh, isolated generation session, so styles
and characters do not bleed together.

Attach two kinds of reference, with these roles:
1. STYLE (match the rendering exactly): art/ai_avatars/bandit_war_camp/refs/style_wayward_blade.webp,
   style_thorn_ambusher.webp and style_road_bandit.webp - live TNR AI sprites. Crisp pixel lineart, flat cel shading,
   limited palette, near-black garments with one accent colour, soft even lighting, full body, no background.
2. SUBJECT (keep the character, NOT the scene or the rendering): that fighter's
   art/ai_avatars/bandit_war_camp/refs/ref_<slug>_current.webp. Keep the face, hair, build, outfit, weapon, colours and
   stance. Drop the camp, the palisade, the banners, the ground and the realistic painting.

Prompt for every fighter (fill SUBJECT from the list):
single ninja character, full body, dynamic combat stance, crisp pixel lineart, flat cel shading, limited palette, soft
even lighting, camera at eye level, flat 3/4 view, no low angle and no foreshortening, both arms held within the
subject's own silhouette and touching nothing, centered, on a true solid flat lime-green chroma key background (#00FF00)
covering the entire canvas, not transparent, not checkerboard, no shadow cast onto the green.
SUBJECT: <from the list>
Negative: no text, no UI, no watermark, no chibi, no blur, no soft pastel, no muddy dither, no background scenery, no
ground, no aura, no halo, no glow, no lime spill on the character, no multiple characters, no checkerboard background,
no white or grey background, no gradient green, no asset sheet, no grid, no labels, no franchise insignia, no headband
plate, no clan symbol.

The six (one session each):
BWC-1 mara_vane: a woman bandit, long dark wavy hair tied back, charcoal fitted gear with leather belts and pouches, a
      red scarf (her one accent), a kunai in one hand and a coil of wire in the other, low wide stance.
BWC-2 kellan_flint: a young man bandit, short dark hair, a cream scarf (his one accent), navy jacket with dark lamellar
      shoulder and arm guards, quiver of arrows on his back, a short bow in one hand and a kunai in the other, crouched.
BWC-3 sable_crow: a woman bandit, a deep indigo hood (her one accent), a cloak of black crow feathers, dark fitted
      armour, a short curved blade in each hand, lunging.
BWC-4 brigg_tusk: a huge, heavily built bearded man, topknot, heavy black armour, ochre sash and ochre leg wraps (his one
      accent), a long studded iron club held two-handed across his body, braced.
BWC-5 yara_reed: a woman bandit, a woven straw hat, a cloak of dried reeds and grass, moss-green clothes (her one accent),
      a long-handled sickle held in both hands, low stance.
BWC-6 goro_blackthorn: the camp's leader, a scarred bearded man, topknot, a dark fur collar, black armour, a crimson
      sash (his one accent), a long sword in one hand and a short blade in the other, wide commanding stance.

Rules: one figure, the whole body inside the frame with a clear margin (weapons included), nothing touching the edges;
grounded adult proportions; the weapon reads at a glance; square, 1024 x 1024.

Return the raw images only, named raw_bwc_<slug>.png (for example raw_bwc_mara_vane.png). Do not process, crop, key or
upload anything. Fail fast: regenerate once if the background is not flat lime, the figure is cropped or touches an edge,
the rendering drifts from the style references (painterly or realistic), the character loses their weapon or accent, or
any insignia appears.
~~~

## Intake (Claude Code)

1. Raw QC each image (spec section "Raw QC").
2. Key the lime, clean edges, pad to an exact square with the figure centred, export lossless WebP at 640 x 640 to
   `art/ai_avatars/bandit_war_camp/exports/ai_<slug>_v1.webp`, under 460,800 bytes.
3. Review sheet: current portrait beside the new sprite, each also at battle-portrait size on a dark composite.
4. After the director approves all six, build the suggestion manifest (six `avatar` edits, one rationale each).
