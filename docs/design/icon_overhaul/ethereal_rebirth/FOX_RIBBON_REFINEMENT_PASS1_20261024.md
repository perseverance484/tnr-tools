# Ethereal Rebirth — Fox ribbon-geometry refinement (2026-10-24)

**Status:** Director approved the two-pass *approach*; Pass 1 is **NOT ACCEPTED**. Two exploratory generations were rejected. No raw candidate is approved for polish, processing, upload, or live use.

**Repository baseline:** `main@d3acf39d328a58735f3ad3eb645bfa01e201a926`; separate ChatGPT-owned documentation branch.
**Jutsu target:** Ethereal Rebirth, `K0t6Z-Q4lau1jFt8Tkpot`, FORBIDDEN / non-elemental. Approved semantic owner: `docs/design/icon_overhaul/ethereal_rebirth/TEXT_V3.md`. The cast has a cracking chest core and six orbiting bands, the hit sends **two gold/blue ribbons as one corkscrew spear**, and the absorb loop retains two protective orbiting bands. The old single-gold-whip/v2 text is superseded; do not silently reuse the paused `ETHEREAL_REBIRTH_ROUND4_SESSION_PROMPT.md`.

## Director-approved art strategy

1. **Lock the existing Fox subject and native premium pixel-art finish.** Preserve the chosen Fox mask construction, covered neck and black gloves, body/pose, armour, restrained crimson scarf, navy-black background, gold/blue palette, chest starburst and cracks. No new hair, skin, exposed fingertips, mouth smile, helmet side projections, runes or magical wrist seals. Treat character identity and composition as fixed; redesign **ribbon geometry only** in Pass 1.
2. **Defensive orbits:** one broad translucent pale-gold and one icy-blue band curve compactly behind shoulders and around waist. Only short translucent portions cross in front; keep mask and white-hot chest core clear. Shorten the ornamental loops by roughly 35–45%; widen each principal band roughly 40–60%, but assess by the actual 45px read rather than numerical width alone.
3. **Offensive release:** an identifiable *second gold-and-blue pair* leaves that system and twists into a short, forceful corkscrew spear exiting toward the upper-right. This represents the approved v3 attack, not a single unpaired gold ribbon or an unrelated projectile.
4. **Particle restraint:** 3–5 tiny, thin four-point stars only; plenty of dark negative space. No spray, water, fire, lightning bolts, particle blizzard, or decorative spell circles. Gold remains pale cream to white; blue remains saturated icy blue with crisp near-white edges. The chest burst stays the single brightest focal point.
5. **Pass 2 only after Pass 1 passes:** restore/refine the original crisp premium TNR pixel clusters without pixel conversion. Check 125px, 64px, 45px, 32px and 112px badge-occluded layouts. Mask/core/defensive orbit/departing spear must survive.

## Actual source references (user-supplied; binaries NOT committed)

- **Primary composition/palette base:** `1000019289.png`; true RGB PNG 1536×1536, SHA-256 `0690f51a1e66793212c1a19e56a8f07a0d8ead638ce177aff615a84ba746a602`. User explicitly preferred this version's composition, palette and rendering.
- **Corrections context only:** `1000019290.png`; true RGB PNG 1536×1536, SHA-256 `2bfe1fc670d71de7280b252901fa3fd58b0a533dba13057301cbf526cf28ab4c`. It had useful restraint/corrections, but is NOT the main rendering reference.
- **Actual animation:** `1000019282.gif`, SHA-256 `78b8a5529abe337b8b5e142f9d8f147741c6eb15a61e386d7b11fcf2d9276444`. A *single*, source-cropped caster peak frame (GIF frame 50, x=0..274, y=28..288) is `er_animation_caster_peak_reference.png`, 274×260, SHA-256 `a94264740c17c8e9e14cea3e92f53797f089a9754a0fe3b4cb1287e1dbf450c8`. This file exists in the producing chat container only; provide the actual unchanged pixels in the next isolated generation session.
- **Reference gate:** attach only the primary icon + the single animation peak, each separately. A filename or URL alone does not establish conditioning. Do not attach the rejected attempts or a comparison collage.

## Pass 1 attempt log and independent visual verdict

| Attempt | Generated source (chat-container only) | SHA-256 | Verdict |
|---|---|---|---|
| A | `dramatic_high_detail_digital_anime_pixel_painting.png` | `fa15d0212cd169b088e9224033739fbafc2ce653d45d4d416fce412d2c0d8982` | **REJECT**: figure/costume and scarf drift; softened painterly finish; lengthened ornamental ribbons; weak 45px improvement |
| B | `a_dramatic_high_quality_anime_pixel_art_style_fan.png` | `6e644031fcba9a2d1970b0680e706f4e3a21862a7e5ca1137ffd432be00f63cc` | **REJECT**: clearer paired upper-right twist but still redraws Fox/long red scarf and loses the original locked composition and pixel finish |

Both are 1254×1254 RGB PNGs. Comparison at actual 125/45/32px: `ethereal_rebirth_pass1_qc.png`, SHA-256 `fe4b215779773f3cbbab8e68992916235ca9489bde7e52a6016c28efb0b6f653`, generated in chat and not committed. They are *attempt evidence*, not accepted raws, exports, or proof of canonical preflight.

**Fail-fast:** Per `docs/workflows/ISOLATED_ART_GENERATION.md`, after two composition/style failures close this generation context. Start a fresh isolated one with the two actual individual references above and a brief that changes only compact orbit widths/paths, paired exit geometry and particles; no extra styling instructions or failed renders.

**Authority note:** Older `RUL-2026-10-24-007` and `FORBIDDEN_MASTER.md` still describe a single Forbidden Master, whereas the director's later chat direction uses individual animal-mask characters, including Fox. Do not silently change the old ruling or assume canonical character identity was reconciled. For this exploratory icon use the current director-directed Fox artwork; record any durable canon reconciliation separately.

**Operations:** Repository documentation only. Live-game requests 0; live writes 0; credentials none; no icon export, preflight or upload conducted by this review.
