# Weapon Master Bukijutsu icon parity lock

**Status:** Phase 1 frozen direction for the Chakra Edge / Parry reconstruction pass.
**Owner:** ChatGPT art-production branch; user retains final art-direction and acceptance authority.
**Base:** `main@2b6cefd8ce2f1ab4d16bb8a0db8f9e38921cdf0a`
**Live-game actions:** none. This record authorizes no upload, publish, or live-game write.

## Purpose

Bring Chakra Edge and Parry to near-identical Weapon Master and katana continuity while restoring the current TNR icon rendering language. This phase freezes the authorities and visual intent before any reconstruction work.

## Frozen authorities

### 1. Weapon Master identity authority

The user-supplied Weapon Master character sheet is the identity source of truth.

Session-local source fingerprint:
- filename: `1000017776.png`
- dimensions: 1536x1024
- SHA-256: `b0a5fad0b72bc55f8a9b919026a41357f8bfbf35f478926764440a23dba1e778`

Locked identity traits:
- shadow-black/void face;
- narrow white eyes;
- black high ponytail with red tie;
- front bang mass and overall hair silhouette derived from the sheet;
- torn red neck scarf;
- black layered shinobi clothing;
- black gloves;
- off-white forearm wraps;
- off-white waist sash with red hanging cloth accent;
- off-white lower-leg wraps;
- dark footwear;
- grounded adult proportions.

Pose may change by jutsu. Character construction may not silently redesign between icons.

### 2. Katana authority

The defender's katana in the current Parry composition is the weapon-design authority.

Session-local Parry composition source:
- generated source: `dynamic_anime_style_action_illustration_on_a_dark_2.png`
- dimensions: 1254x1254
- SHA-256: `87b93e35ee4500ff2b07ab05f36dc848855adf547662996a8aeaf9535bfecc4e`

Locked weapon traits:
- one recurring katana model for Weapon Master Bukijutsu;
- polished curved steel blade;
- fixed blade width/taper/curvature once reconstructed;
- gold/brass circular tsuba;
- dark diamond-wrapped handle;
- gold/brass pommel fitting;
- jutsu effects layer over the blade and must not redesign its physical silhouette.

The opposing blade in Parry is not part of the canonical Weapon Master weapon.

### 3. Rendering/style authority

Repository authority remains `skills/producing-tnr-art/data/25x_DATA_art_spec.json`, especially the ratified house style:
- crisp pixel lineart;
- flat cel shading;
- limited palette;
- soft/even base lighting;
- restrained painterly depth rather than smooth AI-painterly rendering;
- no bloom-heavy or airbrushed treatment.

Visual calibration sources supplied in this session:

**Earlier Chakra Edge**
- filename: `1000017791.png`
- dimensions: 1536x1536
- SHA-256: `e31f9279b7a1fbe92a340114700605bdd48d9ed5b0908ba285c777c88737d38b`

**Chakra Resistance**
- filename: `1000017760.webp`
- dimensions: 1536x1536
- SHA-256: `336d124f0af2cce85f639040a88a33f8c6b8252d3eff234690ce8091c212ded1`

These calibrate pixel discipline and small-icon readability. They do not override the repository art spec.

## Frozen jutsu directions

### Chakra Edge

Current composition source:
- generated source: `a_dramatic_high_contrast_action_fantasy_illustrat_1.png`
- dimensions: 1254x1254
- SHA-256: `82fbc0a9a70accd388208f884f0e67f1106a8325c1a1ed91395b06a9a275f274`

Keep:
- offensive two-handed katana action;
- strong wide stance;
- Weapon Master as dominant subject;
- concentrated cyan chakra reinforcement along the cutting edge;
- controlled cyan slash trail supporting the attack;
- dark uncluttered background;
- immediate small-icon read as an offensive chakra-reinforced sword technique.

Do not carry forward:
- smooth high-resolution anime rendering as the final surface;
- excessive cyan field/aura;
- chakra glow that changes the blade geometry;
- elemental wind vocabulary.

The composition is frozen as the target, but anatomy/costume geometry may be corrected to match the canonical Weapon Master.

### Parry

Current composition source:
- generated source: `dynamic_anime_style_action_illustration_on_a_dark_2.png`
- dimensions: 1254x1254
- SHA-256: `87b93e35ee4500ff2b07ab05f36dc848855adf547662996a8aeaf9535bfecc4e`

Keep:
- grounded defensive brace;
- two-handed katana guard/intercept;
- cropped incoming opponent blade;
- bright metallic contact gleam;
- compact steel-on-steel sparks;
- dark uncluttered background;
- immediate small-icon read as timing, interception, and defense.

Do not carry forward:
- large cyan aura/vortex effects;
- elemental read;
- large explosive effects;
- smooth high-resolution anime rendering as the final surface.

The composition is frozen as the target, but anatomy/costume geometry may be corrected to match the canonical Weapon Master.

## Pair relationship

The finished pair must read as two frames from the same Weapon Master asset family:
- same character construction;
- same costume construction and palette;
- same katana model;
- same pixel/cel rendering vocabulary;
- different pose and jutsu-specific effects only.

Skill differentiation:
- **Chakra Edge:** offensive motion + cyan chakra edge reinforcement.
- **Parry:** defensive intercept + metal gleam/sparks, with no surrounding blue energy field.

## Phase 1 acceptance gate

Phase 1 is complete when:
1. identity, weapon, style, and skill authorities are frozen;
2. no further pose/concept exploration is required for these two icons;
3. later work treats the current smooth images as composition references, not final rendering references;
4. reconstruction cannot silently change locked identity or weapon traits.

Next phase: build the reusable Weapon Master production master and canonical katana before reconstructing either finished icon.


## Phase 2 - reusable Weapon Master production master

**Status:** production candidate complete; director acceptance pending.

Phase 2 deliberately does not reconstruct Chakra Edge or Parry yet. It creates the shared actor/weapon reference layer that later icon work must inherit.

### Canonical character-production board candidate

Generated reference board:
- runtime filename: `a_clean_pixel_art_character_asset_sheet_and_color.png`
- dimensions: 1536x1024
- mode: RGBA
- SHA-256: `3adecc472fcd393b66bb9d14b1769118234e7d4f6fe5779cdb780c2b12278d13`
- bytes: 2,390,506

Use:
- establishes the pixel/cel reinterpretation of the locked Weapon Master identity;
- carries front, 3/4 front, side, 3/4 back, back, head, eye, glove, sash, footwear and silhouette references;
- is a production/reference board only, not player-facing game art;
- any incidental board text or layout has no authority over the character design.

Locked interpretation from this board:
- void-black face and narrow white eyes;
- high black ponytail with red tie and the same dominant bang/ponytail mass across views;
- torn red scarf;
- black layered upper garment and loose black trousers;
- off-white forearm and lower-leg wraps;
- black gloves and dark footwear;
- off-white waist sash with red cloth accent;
- restrained limited-palette pixel/cel treatment readable at icon scale.

The original user-supplied sheet remains the higher authority if this derived board disagrees with it.

### Canonical katana reusable layer

A clean right-facing katana was isolated from the Phase 2 board into a transparent reusable layer:
- runtime filename: `weapon_master_canonical_katana.png`
- dimensions: 808x83
- mode: RGBA with transparent exterior
- SHA-256: `698be45ca0dd13700a995cb2677f346bc685ee402be99cc865f079f610576c98`
- bytes: 85,192

Locked weapon grammar:
- polished curved steel;
- gold/brass circular tsuba;
- dark handle with repeated light diamond wrap;
- gold/brass pommel fitting;
- no chakra, sparks, glow, hands or opposing weapon baked into the reusable layer.

This exact raster is the reuse target for later icon compositing. Transformations may rotate, translate and uniformly scale it, but later jutsu work must not redraw or redesign the sword unless the director rejects this Phase 2 candidate.

### Phase 2 gate

Before Phase 3 starts:
1. director accepts or corrects the Phase 2 character board;
2. director accepts or corrects the canonical katana;
3. any correction is made here before the jutsu compositions are reconstructed.

If accepted, Phase 3 begins from these shared assets rather than generating a new Weapon Master or a new sword.
