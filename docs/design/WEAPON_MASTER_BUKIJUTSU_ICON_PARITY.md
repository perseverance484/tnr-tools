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

**Status:** repaired after audit; director acceptance pending. Phase 3 remains blocked until this repaired lock is accepted.

The first Phase 2 attempt used generation to synthesize a model sheet and then cropped a sword from that generated sheet. Audit rejected that approach because it reintroduced the character and weapon variance Phase 2 was intended to eliminate. Those generated candidates are **superseded and non-canonical**.

### Phase 2A - canonical character identity lock

The repaired identity lock is deterministic. It is assembled only from the original user-supplied Weapon Master reference; no regenerated character pixels are used.

Primary identity source:
- source: `1000017776.png`, user-supplied Weapon Master sheet
- exact authoritative front/3/4 panel: `weapon_master_identity_primary_exact.png`
- dimensions: 543x998
- SHA-256: `796022cc5dae207f0aaea1ed13a0290725dcef179b21a138aea0495e5a6d4afd`

Inspection board:
- runtime filename: `weapon_master_identity_lock_v4.png`
- dimensions: 1760x1160
- SHA-256: `f89c8df4b5138ab5b93302b2e0f43a8ad493fb6ea8f2c13073c011913f1dee9e`
- contents: exact crops of the same authoritative figure for head/hair/eyes, scarf/upper torso, forearm/glove, waist/sash, lower wraps/footwear, plus deterministic 256px and 125px readability proxies

Authority:
- the original front/3/4 figure locks proportions, hair mass, void face and eye geometry, scarf construction, robe, wraps, gloves, waist sash, trousers and footwear;
- other supplied views remain supporting reference only;
- later jutsu work may change pose but must not independently redesign these traits;
- the earlier generated model sheet remains a style study only and owns no character geometry.

### Phase 2B - canonical reusable katana lock

The repaired katana is deterministic and uses no image-generation step.

Hilt/tsuba provenance:
- exact source pixels come from the original user-supplied Weapon Master katana detail in `1000017776.png`;
- the detail was normalized to a horizontal orientation and isolated with a fixed geometric mask;
- the dark diamond wrap, gold/brass circular tsuba and gold/brass pommel therefore derive from the original character reference rather than the rejected generated sheet.

Blade provenance:
- geometry derives from the approved Parry composition `dynamic_anime_style_action_illustration_on_a_dark_2.png`;
- the Parry blade was normalized to horizontal orientation and converted to a reproducible locked curve;
- later jutsu effects must be layered over this blade and may not change its physical silhouette.

Reusable raster:
- runtime filename: `weapon_master_katana_lock_v2.png`
- dimensions: 1200x240 RGBA
- alpha range: 0..255
- SHA-256: `b196812e526f82bbb7e23fc6e37c1c35c8fbe615dbf325b71597776fa121599c`

Inspection preview:
- runtime filename: `weapon_master_katana_lock_v2_preview.png`
- dimensions: 1300x340
- SHA-256: `ca3eca02ebbb221b6a1f740d355b85f80d470247ca618ad70c144c857d437558`

Reproducible geometry record:
- runtime filename: `weapon_master_katana_lock_v2_geometry.json`
- SHA-256: `ec7d31289ae468ae29050c603ecf0dd05fb8591bcd4e2d9f8527322d12dadcc1`
- canvas: 1200x240
- blade root x: 300
- blade tip: (1168, 57)
- upper cubic: (300,91) -> (555,103) -> (865,126) -> (1168,57)
- lower cubic: (300,146) -> (560,161) -> (900,180) -> (1168,57)

Reuse rule:
- this exact katana raster is the recurring Weapon Master sword layer;
- allowed transforms are rotation, translation and uniform scale;
- pose occlusion may cover it with hands/body;
- do not regenerate, redraw or alter handle/tsuba/blade geometry per jutsu without a new director ruling.

### Phase 2 repair gate

Phase 2 is ready for director acceptance when:
1. the deterministic identity lock is accepted as the Weapon Master geometry authority;
2. the deterministic katana lock is accepted as the recurring weapon authority;
3. the rejected generated Phase 2 board and sword remain non-canonical;
4. Phase 3 starts only after acceptance and derives both Chakra Edge and Parry from these same locks.

No live-game request, upload, publish or write is authorized by this phase.


## Director correction — Phase 2B rejected

**Date:** 2026-10-06  
**Status:** ACTIVE correction to Phase 2B.

The director rejected `weapon_master_katana_lock_v2.png` as the canonical Weapon Master katana. Although its provenance and reconstruction were deterministic, the result does not read convincingly as a katana and is visually below the quality of the earlier generated Icon Production Master sheet.

Consequences:
- `weapon_master_katana_lock_v2.png`, its preview, and its geometry JSON are **REJECTED / NON-CANONICAL**;
- deterministic provenance does not outrank visual correctness for an art-direction decision;
- do not use the rejected v2 sword in Chakra Edge, Parry, or later Bukijutsu;
- Phase 2A identity lock remains unaffected;
- Phase 2B is reopened and Phase 3 remains blocked.

### Revised Phase 2B direction

Use the earlier generated Icon Production Master sheet as the **weapon visual-quality and silhouette reference**, while keeping the original Weapon Master sheet and approved Parry composition as continuity checks.

The new katana lock must:
- read immediately as a traditional katana rather than a generic curved fantasy sword;
- preserve the stronger blade-to-hilt proportions, curvature, kissaki, circular brass/gold tsuba, wrapped tsuka and pommel treatment visible in the preferred master-sheet weapon;
- be isolated as one clean reusable weapon asset;
- avoid independently regenerating a different sword for each jutsu;
- prioritize visual quality and recognizability first, then freeze the accepted raster for deterministic reuse.

The generated master sheet is promoted only as a **weapon design reference**. Its independently synthesized character turnarounds remain non-canonical for Weapon Master identity.

Phase 2B is complete only after the director accepts the replacement katana.


## Phase 2B v3 — preferred master-sheet katana isolation

**Date:** 2026-10-06  
**Status:** CANDIDATE / director acceptance pending.

The replacement Phase 2B weapon lock now uses the director-preferred Icon Production Master sheet sword **without redrawing it**.

Source:
- runtime source: `a_clean_pixel_art_character_asset_sheet_and_color.png`
- role: preferred master-sheet weapon visual reference
- source crop: x=30..860, y=690..780

Isolation method:
- smooth dark panel background estimated from background-only rows/columns;
- RGB distance threshold used to locate the sword;
- largest connected component selected;
- external silhouette filled so the dark tsuka/steel pixels remain included;
- RGB artwork pixels are copied directly from the preferred master sheet;
- only the alpha mask is reconstructed;
- no image generation and no sword redraw are used in v3.

Replacement reusable raster:
- filename: `weapon_master_katana_lock_v3.png`
- dimensions: 812x79 RGBA
- SHA-256: `149cd35b0126b2717c3deacda04b0cec261e3a4039493024338a2bfed8e3a979`

Inspection preview:
- filename: `weapon_master_katana_lock_v3_preview.png`
- SHA-256: `034a36db10c50b415779f44cbfa2a0b950a4eabb1a320e2163fa1c18966e05eb`

Provenance record:
- filename: `weapon_master_katana_lock_v3_provenance.json`
- SHA-256: `887fb3037bc5fe01b744250727afce93d088dd645030f9c8940273b5ba63cd94`

Visual lock carried by this candidate:
- traditional katana read;
- compact wrapped tsuka with repeated light diamond pattern;
- brass/gold pommel and circular tsuba;
- slim polished blade with restrained curvature;
- clearly formed kissaki;
- no chakra, sparks, glow, hands or opposing weapon baked into the reusable layer.

The rejected v2 sword remains non-canonical. If the director accepts v3, this exact raster becomes the recurring Weapon Master katana layer for Chakra Edge, Parry and later Bukijutsu, with only uniform scale, rotation, translation and pose occlusion permitted.

Phase 3 remains blocked until director acceptance of Phase 2B v3.
