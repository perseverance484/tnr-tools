# The Forbidden Master: art session prompt (round 1, model sheet)

- **Brief:** `docs/design/characters/FORBIDDEN_MASTER.md`. Ruling: RUL-2026-10-24-007.
- **Goal:** fix the character's design before any Forbidden jutsu icon is drawn with it. Three candidates, one per mask
  idea; the director picks one (or mixes) for round 2.
- **Live-game requests/writes:** 0. Credentials: none.

~~~text
You are the art director for The Ninja RPG (repository perseverance484/tnr-tools). This session designs a new recurring
character: THE FORBIDDEN MASTER, the figure in every Forbidden jutsu icon. Read docs/design/characters/FORBIDDEN_MASTER.md
first.

Attach as references, with these roles:
1. IDENTITY: art/characters/forbidden_master/refs/ref_fm_identity_tempest_cleave.webp - the fox-masked fighter of our
   Tempest Cleave icon (kitsune mask, dark segmented armour, white scarf, glowing eyes). Take the character, not the scene.
2. RENDERING GOAL: art/characters/forbidden_master/refs/ref_fm_render_weapon_master_full.png - our Weapon Master. Match its
   rendering exactly: bold clean ink outlines, cel shading with painterly texture, a limited high-contrast palette,
   dynamic torn cloth, hard bright energy arcs. Also attach ref_fm_render_weapon_master_icon_slash.png and
   ref_fm_render_weapon_master_icon_guard.png for how this character family reads as a jutsu icon.

Who they are: the master of the arts the villages sealed away. Every Forbidden jutsu is theirs. Intimidating and imposing,
a talented and dangerous practitioner: tall, broad-shouldered, lean and hard, mature proportions, composed and unhurried.
Power radiates from them; they never flail.

THE MASK IS THE SILHOUETTE. Where the Weapon Master's face is a shadowed void with glowing eyes, the Forbidden Master wears
a mask that does the same job: from any distance the face is a dark shape whose only light is two glowing eye slits. The
mask is always on; the face is never shown.

The rest of the design (same in all three candidates):
- dark, long, wild hair tied back high, streaming behind the mask (the Weapon Master's family);
- dark segmented armour over a black gi; a long, heavy, tattered dark coat or half-cloak that flares (imposing mass);
- bandaged forearms and shins;
- a WHITE scarf, torn at the ends (from Tempest Cleave);
- palette: black, charcoal, bone white, and deep crimson as the only accent (mask markings, scarf lining); eyes glowing
  white-hot;
- no sword as a signature; empty hands, one raised with a faint white-hot glow of gathered power.

Pose for all three: a full-body, three-quarter view, a low, braced, imposing stance (one hand raised, the other lowered),
coat and scarf flaring, on a plain dark background (or transparent), like the Weapon Master render. The figure fills the
canvas height.

Generate three candidates, each in its own isolated generation session, one per mask:
FM-1 BLACK KITSUNE: the Tempest Cleave fox mask (pointed ears, tapered snout) in matte near-black, thin crimson markings,
     two glowing white eye slits. (Proposed.)
FM-2 HALF KITSUNE: a near-black fox half-mask over the upper face and a dark cloth mask over the lower face, so the whole
     face is dark; glowing eye slits; small crimson markings on the mask.
FM-3 SMOOTH OVAL: a plain, featureless near-black oval mask with only two narrow glowing eye slits and one thin crimson
     line; the hood or hair frames it.

Rules: the Weapon Master's rendering quality; no text, runes, kanji or symbols; no franchise looks (no Naruto ANBU masks,
headbands or insignia); one figure only; no weapons as the focus; no frame or UI. Square, 1254 x 1254.

Return the raw images only, named raw_forbidden_master_FM-1.png, raw_forbidden_master_FM-2.png and
raw_forbidden_master_FM-3.png. Do not process, crop or upload anything. Fail fast: regenerate once if the face shows
through the mask, the figure looks small, timid or generic, the rendering drifts from the Weapon Master's, or a franchise
mask appears.
~~~

## Intake (Claude Code)

1. Raws to `art/characters/forbidden_master/candidates/round1/`.
2. Review sheet with the identity and rendering references as reference rows, each candidate also at 45 px (head and
   silhouette read) and against the Weapon Master (same family, different person); notes against the brief's acceptance
   criteria M1–M6; log the round in `FORBIDDEN_MASTER.md`.
3. On the director's pick: round 2 adds turnarounds and expressions of power (front, side, back; two icon-style poses),
   which become the reference attached to every Forbidden jutsu brief.
