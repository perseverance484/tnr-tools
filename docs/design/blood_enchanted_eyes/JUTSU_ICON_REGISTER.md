# Blood-Enchanted Eyes — Jutsu Icon Visual Identity Register

**Status:** NEW ART STUDIO INITIALIZED; **0/8 jutsu-icon artworks approved in this workstream**, no image-generation work started here.  
**Art director:** dauntless. **Art Studio role:** direction, per-icon silhouette briefs, approval tracking, processing/QC.  
**Operating contract:** docs/workflows/ISOLATED_ART_GENERATION.md and docs/workflows/ART_PRODUCTION.md; actual specs belong to skills/producing-tnr-art/.  
**Bloodline identity:** Blood-Enchanted Eyes (BEE; bloodline ID `ovZIWu28ANn-Cij5TjT8S`). Do not confuse with **Blue Blade Eyes (BBE)**.  
**Roster evidence:** historical captured-mechanics projection, not current live state: `fable/bloodright-planning-20261003@7c1dfdd5e3ee163b90c22694dbb2de94ede08866`, `docs/design/bloodright/kits/blood_enchanted_eyes.json` (public snapshot 2026-10-01). Need exact current images/descriptions/captured records or user attachments before final icon interpretations.

## Director's new visual direction (2026-10-14)

**Theme: BLACK + SCARLET / CRIMSON; SHADOW-BASED BLOODLINE WITH BLOOD MOTIFS.**

This is a new visual family, *not a recolor of BBE ice assets*. Initial identity:
- **Shared atmosphere:** black, near-black and charcoal/shadow depth with deep burgundy midtones; luminous scarlet/crimson blood chakra as the signature foreground energy; selective bright arterial-red highlights for shape recognition.
- **Materials / effect vocabulary:** blood-infused shadow, dark smoke or ribboning shadow chakra, concentrated blood chakra, ruby/translucent red fluid or hardened droplets, dark crimson splashes/veins/threads where the individual technique warrants them; rich high-quality TNR pixel-art treatment rather than gore, anatomy or horror portraits.
- **Rendering:** one large readable focal shape with controlled crimson highlights and sharply separated black negative space; restrained fine particles/mist and carefully chosen highlights. Dark does **not** mean an unreadable black silhouette against black.
- **Ninja/bloodline identity:** the icon depicts the **actual jutsu action**, not a generic blood droplet/eye/circle pasted onto every image. Bind/corrupt, drain/absorb, defend, restore, pierce, spiral or suppress according to actual evidenced skill.
- **Variation:** each jutsu gets its own uniquely identifiable dominant **silhouette + composition + chakra behavior**; avoid eight different red circular sigils, repeating an eye on every icon, or silhouettes indistinguishable at thumbnail size.
- **Background:** user-approved TNR jutsu rule: **full-bleed painted background fills all four edges**, **no jutsu rarity plate**, **no required transparency**; distinguish opaque visual requirement from unresolved shared ICON alpha check.
- **Avoid:** BBE's icy blue/snowflake/crystal family palette and sword shapes; unrelated characters/actors, franchise insignia, text, border, equipment UI, excessive gore, stock fantasy-red-fire look or non-technique ornaments.

This visual treatment is **director-provided palette/theme direction**, not approval of any individual silhouette, source reference or generated image. Do not start generation in the Art Studio.

## Eight historical BEE jutsu records — visual design NOT YET ASSIGNED

| Jutsu | Historical ID (not a live-refresh assertion) | Observed captured mechanical cues (for context, NOT a final visual interpretation) | Visual / generation status |
| --- | --- | --- | --- |
| Ring of Spilled Blood | `OeFCfJ--gEL_FioGfQvTY` | Spiral AOE; damage; opponent attack suppression | **PENDING SOURCE IMAGE + SILHOUETTE BRIEF** |
| Crimson Tithe | `zor6cX3qn2eTObW0fveBk` | Single-target damage, stun and time disruption | **PENDING SOURCE IMAGE + SILHOUETTE BRIEF** |
| Sanguine Plague | `XIcRftgH-UOJCdl91wbRD` | Vulnerability, afterburn and protective debuff prevention | **PENDING SOURCE IMAGE + SILHOUETTE BRIEF** |
| Reaper's Embrace | `7RtWUduLzfIPOlWdo-NIu` | AOE shadow damage, movement, vampiric recovery, protection | **PENDING SOURCE IMAGE + SILHOUETTE BRIEF** |
| Unholy Enhancement | `Nn75Lmvaep6oBQYH2BvVT` | Increases own damage, decreases opponent damage | **PENDING SOURCE IMAGE + SILHOUETTE BRIEF** |
| Crimson Impact | `fKEHVLvvj6q_b4l_X_k4k` | AOE impact, lifesteal, shield, vulnerability | **PENDING SOURCE IMAGE + SILHOUETTE BRIEF** |
| Hemocure | `9VRW6hqSoQuz5PA203jFE` | Absorption and defensive/offensive modulation | **PENDING SOURCE IMAGE + SILHOUETTE BRIEF** |
| Thousand Strike | `znPva-HIAz4EkyuKm2oh0` | Pierce attack and increased vulnerability | **PENDING SOURCE IMAGE + SILHOUETTE BRIEF** |

**Evidence limitation:** the captured Bloodright kit is a mechanical projection of earlier captures, not current live text or current artwork. Before locking an image concept, inspect the original visual references and preferably the jutsu's actual descriptive text. These cues provide **possibilities, not an artistic rulebook or permission to change mechanics**. Do not invent jutsu effects based on names.

## Scope separation: jutsu icons versus Bloodright art

The **already approved BEE Foundation, Hidden Art and Advanced Art tier emblems** belong to a different Bloodright three-symbol workstream (context/evidence in `chatgpt/bloodright-icon-production-tracker-20261008@c85c1ea834e24315b5688f73a65c35479b8963e6`, `docs/design/bloodright/ICON_PRODUCTION_TRACKER.md`). They are **not** among these eight jutsu icons and are **not authorized for redesign** here. Their reported black-backed identity may help palette calibration **only when exact approved reference images are supplied**; never copy their tier-symbol geometry into jutsu compositions by default.

The Bloodright tree title **Crimson Covenant** is established in RUL-2026-10-03-006 and is not a new name for this eight-jutsu production workstream.

## Approval / source register conventions

Every final icon needs: `jutsu name/ID`, approved primary silhouette, approved **individual** style reference(s), raw filename, actual decoded format/dimensions, raw SHA-256 and original bytes availability, director visual approval, processed output filename/size/SHA-256, 125/64/32px confusion review, current artpreflight verdict, and user-controlled upload/read-back status.

- **UNSTARTED** = no approved concept or generated image.
- **REFERENCE READY** = exact real image reference(s) inspected; style brief can be prepared.
- **GENERATED** = single raw draft exists, not yet approved.
- **RAW VISUAL APPROVED** = director approved one exact candidate; no implied upload readiness.
- **PROCESSING QC PASSED** = actual transformed file checked against format, size and target bounds.
- **PREFLIGHT CLEAR** = current canonical validator genuinely passed, not assumed.
- **LIVE VERIFIED** = user-supplied production upload/read-back evidence only.

Original sources and output SHA records live in `SOURCE_EVIDENCE.json`; empty until real files are examined. **Do not invent hashes or repo/asset locations.**

## Technical decisions pending

- **File cap:** the extra **strict <80,000-byte** rule is explicitly a **BBE** workstream ruling. For BEE, the live canonical ICON spec governs until the director expressly adopts the same stricter cap here; the studio may *propose* it for quality/performance.
- **Format:** current source-derived ICON defaults target square 256x256 lossless WebP; check the current live repository and target rules at processing time rather than trusting this snapshot.
- **Opaque alpha mismatch:** the shared current ICON `chroma_key=lime` requires RGBA under `artpreflight.py` even for the director-approved full-bleed RGB jutsu background. Do not manufacture transparency, quietly override it, or call the tool green; request separate reviewed Fable implementation or report an explicit unresolved block.
- **Assets:** exact BEE jutsu image source pixels have **not been provided in this workspace**, and previous bloodline-emblem binaries are not Git-pinned by this branch.

## First studio actions

1. Bootstrap from the current repository and this register, then inspect 2–4 exact existing BEE jutsu icons or approved BEE source art supplied by the director.
2. Establish a **small visual identity card** (black/charcoal/shadow vs scarlet/crimson, brightness/contrast/material). Show it for director feedback before locking jutsu prompts.
3. Assign **eight distinct silhouettes** rooted in the actual jutsu effects and descriptions. Review for confusion as a collection.
4. Select first jutsu with director; write its **isolated-generation prompt** and specify only 1–2 individual references (style-only or subject-only).
5. **Do not generate in this studio.** Open a new generation conversation per icon; return the approved original to studio for processing/QC.
6. Preserve every approval separately from processing, validation and publishing. No live-game requests/writes without explicit operator authorization.

**Current visual approval:** 0/8 in this workstream. **Live-game requests/writes:** 0. **Credentials:** none.
