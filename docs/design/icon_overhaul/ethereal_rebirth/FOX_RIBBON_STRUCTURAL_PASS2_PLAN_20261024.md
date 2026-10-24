# Ethereal Rebirth — Fox ribbon structural reconstruction, next pass

**Status:** PLANNED / exploratory; NO next-pass image generated or accepted. Director requested the planning phase after rejecting the cleaner-but-unchanged third attempt (2026-10-24). **Execution is gated on restoring the exact approved Fox source.**
**Target:** jutsu `K0t6Z-Q4lau1jFt8Tkpot` — Ethereal Rebirth, FORBIDDEN, non-elemental, `jutsu.image` / `JUTSU_ICON`.
**Plan branch base:** `main@a0ac366abbe7cfc1ac5373409a54ce649ac81276`.
**Previous frozen branch:** `chatgpt/ethereal-rebirth-fox-ribbon-refinement-20261024@94bbc2e2170bc9f93e4acfc24692569cf12f279c`; previous plan `docs/design/icon_overhaul/ethereal_rebirth/FOX_RIBBON_REFINEMENT_PASS1_20261024.md` exists **on that branch**, not on this main-based branch.
**Lead:** Art Director; supporting lens: Image Production. Director owns art direction and visual acceptance. No Fable code change is assigned.

## 1. Why Pass 1 and the follow-up failed

The earlier two generations changed the Fox, softened the native pixel clusters, exaggerated the scarf, and kept long ornamental spirals. The additional clean-context candidate was tidier but still reproduced the same full-character double helix, rather than visibly separating the **guard** from the **paired strike**. Its source was a re-rendered 1254 px image, not a strict preservation edit. A more elaborate prompt or another global redraw is not a corrective strategy.

**New method:** replace ribbon **topology** first, then render the light. Do not re-render the character. A pass with perfect colour/glow and the same repeated helix is a FAIL.

## 2. Source integrity and governing evidence

| Role | Exact evidence | Status at planning |
| --- | --- | --- |
| **SUBJECT — immutable Fox base** | `1000019289.png`, RGB PNG 1536×1536, SHA-256 `0690f51a1e66793212c1a19e56a8f07a0d8ead638ce177aff615a84ba746a602` | Required for execution; the exact file is not in this chat's mounted inputs or committed to the repo. This identity/hash comes from the prior committed Pass 1 record, **not** a fresh re-hash. |
| Current chat Fox attachment | `1000019305.jpg`, JPEG 1536×1536, SHA-256 `95bb966920c1ce175e93893cb64f3c839f02cb07619d2c33c9e7b985d27aec10` | Actual local hash verified. Visually useful, **not byte-identical** to the approved PNG; do not substitute as the exact source. |
| **MOTION — animation caster peak** | `1000019306.png`, RGBA 274×260, SHA-256 `a94264740c17c8e9e14cea3e92f53797f089a9754a0fe3b4cb1287e1dbf450c8` | Actual local hash verified; use as the second, **motion/material-only** reference. |
| Additional rejected candidate | `a_dynamic_high_contrast_pixel_art_illustration.png`, RGB 1254×1254, SHA-256 `da1592fa67a592899640dbd438e648cf17bea18674c603ae56e73b8439090962` | Third failure; **evaluation evidence only**, never a generator reference. |
| Technique meaning | `docs/design/icon_overhaul/ethereal_rebirth/TEXT_V3.md` | Approved: seal/core cracks; six bands in cast; **two ribbons twist together into a spiralling spear** for the hit; **two remain** in a protective absorb orbit. |
| Animation look | `docs/handoffs/ETHEREAL_REBIRTH_ANIMATION_V5_ART_REQUEST.md` and `art/jutsu_icons/ethereal_rebirth/animation/raws/ref_anim_v5_peak.png` | Broad, translucent glassy light-cloth with crisp pale edges and soft amber/deep-blue outer halos. Blue passes upper half, gold lower; previous v4 single-gold lash is **not** the current v3 attack. |
| Production policy | `docs/workflows/ISOLATED_ART_GENERATION.md`, `docs/workflows/ART_PRODUCTION.md`, `skills/producing-tnr-art/SKILL.md` + current `25x_DATA_art_spec.json` | One raw candidate per isolated conversation; visual approval distinct from lossless 256 px WebP export and `artpreflight.py --type JUTSU_ICON`. **No pixel-conversion/snap/quantisation** per RUL-2026-10-24-005. |

**Absolute source gate:** locate/reattach the actual `1000019289.png`, decode it, verify its SHA-256 and dimensions. If unavailable, **stop** with SOURCE_LOCK_BLOCKED: it is not honest to call a JPEG-based redraw a source-faithful edit. Do not import earlier failed candidates, the correction-context image, or a comparison sheet into generation.

## 3. Desired still-frame choreography: guard + release, not a helix

A single static moment condenses the animation's six cast bands into **two readable guard remnants and a separate gold/blue attack pair**. It need not literally draw all six simultaneously. The single primary action is **soul-light expelled from the cracked chest seal and discharged as a paired corkscrew spear**. The protective orbit remains legible but is secondary.

**Visual hierarchy (strict):** (1) intact Fox mask/pose and **one** white-hot chest seal; (2) the paired directional strike; (3) compact guard; (4) restrained stars. No competing magical halo or second bright explosion.

### Topology sketch — approximate normalized source-canvas coordinates

These are **layout guides**, not permission to reposition the original subject; final paths are shaped against the exact 1536 px base and original Fox silhouette.

| Layer | Shape, depth and anchoring | Required reading |
| --- | --- | --- |
| **G-BLUE**, defensive upper arc | A **single broad icy-blue, tilted crescent** behind upper torso/shoulders. Rough occupied corridor x=0.18–0.84, y=0.23–0.59. Reveal a **short**, semi-transparent segment near the outer lower torso only; stay behind the mask and arms. | Light defending the caster, not a closed full-frame spiral. |
| **G-GOLD**, defensive lower arc | One broad pale-gold loop **around waist/hips** (rough y=0.55–0.77), with most of its far side behind Fox and one controlled translucent near-side crossing **below** the chest core. No wrap below thighs, no second lap. | A short orbit that can remain after the attack. |
| **S-GOLD + S-BLUE**, paired release | A **new, linked pair** visibly separates from the caster-side light near Fox's right upper torso, outside the chest-protection mask (approx start x=0.66–0.74, y=0.41–0.47). Travel on **one diagonal axis** toward the **upper-right** (guide tip x≈1.04, y≈0.14). The two broad bands switch near/far order **once**, converge into a pointed corkscrew/spear and **exit the same region of the frame together**. | One accelerating paired hit, not a lone gold whip, two unrelated arcs or an endless orbit. This is the release direction inside the icon; the separate hit animation later drives down onto the target. |
| **STARS** | Just **3–5 tiny thin four-point stars**, placed near the core and release path, not evenly scattered. | Small punctuation, never the spectacle. |

Geometry constraints: make the principal guard bands approximately **6–8% of tile width** at broadest visible face and the spear's individual bands about **5–7%**; turn some short stretches edge-on to show twisting. Keep the old ornamental path length cut by **about 35–45%** as an initial visual target, but judge success at 45 px, not by exact pixel ratios. A small, local segmented speed trail on the **rear** of the spear is allowed; no long light tail covering the full canvas. Restrict all other ribbon tips to the inside of the canvas. Leave obvious dark negative space **below the belt and between the arms and energy**.

**Conservation law:** exactly two protective arcs + one paired spear are the dominant energy shapes; any residual old helix is a reject. Do not add circular spell seals, magical wrist bands, ornamental rings, fire, water, lightning bolts or runes.

## 4. Immutable Fox protection map

Hard-lock the **approved source's** silhouette, mask proportions and ear attachment, red markings, covered neck, solid **full-finger black gloves**, hands/fingers, arms-wide pose, dark layered armour, controlled crimson scarf/sash, belt, palette, near-black background, native pixel clusters, crop, and **white-gold chest core with branching light cracks**.

A physically honest limitation: the original glow/ribbons cross some armour/background. Removing an existing foreground band necessarily exposes pixels the source never showed. Therefore:

- **Untouched area:** composite directly from the exact original PNG, pixel for pixel. Verify zero RGB difference outside an explicitly reviewed repair/edit mask.
- **Old-ribbon occlusion area:** remove old bands first and locally reconstruct *only the newly exposed* background/armour using adjacent original pixel-art shapes; preserve known lines/colour blocks. Record these constrained reconstruction zones; do not globally reimagine the figure.
- **Never paint over protected high-identity regions:** Fox mask and ears, neck/scarf seam, full gloves and fingers, visible forearms, chest centre/rays/cracks. Foreground new light is translucent and stays **below/outside** these areas.
- **If old ribbons cannot be removed without visibly changing the locked subject, stop** with LOCAL_REPAIR_BLOCKED rather than presenting a technically cleaner, newly generated Fox as a faithful edit.

Do not use the generator to "fix" pose, clothing, mask, scarf, anatomy, colour grade or character rendering. Do not blur/pixel-convert/quantise the native pixel-art finish.

## 5. Execution order for **one** new raw

1. **SOURCE LOCK.** Restore and verify the original exact PNG; attach it as **SUBJECT / preserve** and the verified caster-peak crop as **MOTION / geometry and material**. Fresh isolated generation context. No extra images.
2. **PROTECTION/MATTE.** Establish immutable mask/core/glove/pose regions, original energy-path removal areas and any limited underpainting zones. Preserve original pixels outside the union of approved edit zones.
3. **GEOMETRY PROOF FIRST (internal, non-generative).** Lay down simple flat blue/gold paths in the specified order. Inspect the flattened duplicate at 125 and **45 px** before adding glow. If it still reads as repeated rings or lacks a distinct paired projectile, correct geometry now; do not spend a generation on polishing it.
4. **RIBBON SURGERY.** Locally clean previous ribbons (including old leg-level passes), repair their occluded substrate only where necessary, and compose G-BLUE/G-GOLD behind Fox plus the S-GOLD/S-BLUE pair leaving the chest/shoulder. Depth order must make sense. Keep mask/core/gloves pristine.
5. **PIXEL-ART LIGHT TREATMENT.** Build wide translucent pale washes and subtle along-band streaks; crisp near-white long edges; restrained amber `#e27d1b` and blue `#286aec` outer glows. Gold pale cream `#fef383`→white; blue `#9aa4d2`→`#75dcff`. Use a **short stepped directional trail** only on the outward braid; keep the core the brightest point.
6. **REMOVE PARTICLES.** Recreate at most 3–5 deliberate four-point stars and clean other glitter. Keep the dark ground unbusy.
7. **ONE RAW CANDIDATE.** Output an original square PNG preserving the source's 1536×1536 frame, without a resize where the editing workflow permits. Supply exact hash, dimensions, true format and raw source provenance. **No export, no preflight, no upload in this pass.**

If image editing cannot do the matte/local surgery without changing Fox, **do not run a third global redraw**. Escalate to a deterministic layered compositing/local inpainting approach or report the source-preservation constraint; production tooling belongs to Fable unless separately assigned.

## 6. Acceptance and rejection gates

| Gate | PASS requirement | Immediate FAIL examples |
| --- | --- | --- |
| **0. Source** | Primary exact SHA matches; motion SHA matches; no rejected image used as style input. | Recompressed JPEG used while claiming strict original preservation. |
| **1. Identity lock** | Fox mask/ears, full black gloves, scarf, armour, hands, core/cracks, pose, palette/crop and native finish visibly match source; pixel-identity outside the reviewed edit mask. | Redesigned mask, fingerless look, extended scarf, pose/scale drift, painterly restyling. |
| **2. Defensive orbit** | Only two clear broad, compact guard arcs; near/far occlusion reads; face, hands, core stay open. | Tall body-spanning double helix, extra loops around legs or thick opaque foreground bar across torso. |
| **3. Offensive spear** | Separate gold **and** blue leaving **together** toward upper-right, one visible depth crossover, convergent pointed direction at 45 px. | Single gold whip, two independent waves, long circular ribbons, spear never exiting the image. |
| **4. Restraint** | 3–5 small four-point stars; quiet negative space and one focal chest light. | Particle storm, new explosion, decorative symbol, added hue family. |
| **5. Actual-size** | Inspect exact-source/candidate side-by-side at **125, 64, 45, 32 px** and **112 px with badge occlusion**. At 45 px: Fox, white-hot core, compact guard and paired directed release can all be found without zooming. | At 45 px light dominates the face/body, guard and attack merge, or spear becomes an illegible streak. |
| **6. Raw intake** | New raw identity/format/dimensions/hash recorded; director evaluates one candidate; no processed-export claim. | Candidate called approved or upload-ready before explicit director acceptance/QC. |

**Fail-fast discipline:** reject a drifted full redraw immediately. One candidate only in the next session. If two structurally wrong edits accumulate, close that context; do not feed its rejected output into further prompts.

## 7. Canon, approvals, and operations boundary

- The **approved `TEXT_V3.md`** governs the technique description and three animations; **do not** revert to `TEXT_V2.md` or the paused round-4 one-gold-whip brief.
- **Open doctrine/ruling conflict:** RUL-2026-10-24-007 and `docs/design/characters/FORBIDDEN_MASTER.md` still frame a *single* Forbidden Master, while later director instructions use individual animal-mask characters including Fox. This plan follows the **director's current exploratory Fox art** without silently rewriting the older ruling; durable canon reconciliation is a separate director decision.
- A director-approved candidate moves **later**, through the established art-intake, 256px lossless WebP, spec-driven `artpreflight.py --type JUTSU_ICON`, versioned filename, and user-owned publishing pathway. Fable remains the normal processing/manifests owner per RUL-2026-10-23-008 amendment.
- This is a **planning-only repository document**. No image generation, processing, art export, manifest/code change, test execution, live-game request/write or credentials.

## 8. Minimal next isolated-session brief (once source gate passes)

```text
Repository: perseverance484/tnr-tools
Target: Ethereal Rebirth / K0t6Z-Q4lau1jFt8Tkpot
Plan: docs/design/icon_overhaul/ethereal_rebirth/FOX_RIBBON_STRUCTURAL_PASS2_PLAN_20261024.md
Mode: ISOLATED SOURCE-PRESERVING RIBBON EDIT; one PNG candidate, no processing
Reference 1 SUBJECT: exact 1000019289.png (SHA-256 0690f51a...) — keep Fox pixel structure
Reference 2 MOTION: exact 1000019306.png (SHA-256 a9426474...) — short broad bands/paired velocity
Protected: Fox mask/attached ears, black full gloves, costume/short scarf, pose,
           palette, crop/background, native pixel clusters, chest seal/core/cracks.
Remove the tall ornamental gold/blue helix and excessive sparkles.
Draw two short broad defensive bands (blue high behind shoulders; gold at waist),
PLUS a distinct gold+blue pair spiralling ONCE together into a short upper-right spear.
Keep the core unobscured, dark negative space and only 3–5 tiny four-point stars.
First solve geometry at 45px. Prefer local ribbon surgery/compositing, not full-frame redraw.
Reject identity drift or renewed long loops. Return ONE raw, exact bytes/hash, no WebP or upload.
Live-game requests/writes: 0 / 0. Credentials: none.
```
