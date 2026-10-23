# Replacement Technique: icon rework session prompt (round 1)

- **Director, 2026-10-23:** "Lets start with rep tech, where we try to faithfully upgrade the old icon to the newer
  version." Review note (`docs/design/icon_overhaul/ICON_SCORES.md` #12, 3/10 for ours): "while it was a good image on its
  own players missed the old one. They felt the old image more properly captured the skill. Perhaps we can try working
  the two together."
- **Batch:** first rework of the icon overhaul (RUL-2026-10-23-008); ships with the rest of the batch, not alone.
- **How to use:** paste section 1 into a new art-director session. That session runs each brief in section 2 in its own
  isolated generation session (`docs/workflows/ISOLATED_ART_GENERATION.md`), one candidate per session, and returns the
  raws. Claude Code previews them in context (section 3) for the director.
- **Live-game requests/writes:** 0. Credentials: none.

## 0. What to keep and what to fix

| From | Keep | Why |
|---|---|---|
| **Old icon** (live now; `art/jutsu_icons/replacement_technique/refs/ref_rt_old_original.png`) | the ninja in black with the pink-red sash, caught mid-leap away; the white-blue chakra rings whirling around them; the **log left behind** as the decoy; the bright, sunlit forest clearing | players say it "more properly captured the skill": you see the swap happen. Its daylight greens also make it stand out in a bar of dark icons |
| **Our icon** (reverted; `refs/ref_rt_new_reverted.png`) | the **white smoke puff** where the user vanished, and the **blue chakra swap trail** showing the jump from the log to the new spot | the battle text: "vanishes in a puff of smoke, leaving behind a decoy... reappears elsewhere" |
| **Lessons from the review** | premium TNR pixel art; two big readable shapes (ninja and log) at 45 px; a calm background that never takes over (the Blue Blade Eyes lesson); nothing important in the bottom corners (badges) | the most common complaints across the 51 icons |

**People:** the thread leaned towards no people in reworked icons (RUL-2026-10-23-008), but the director asked for a
**faithful** upgrade of the old icon, which shows the ninja. Briefs RT-1 to RT-3 keep the ninja; RT-4 is the no-person
fallback. The director chooses.

## 1. Session prompt (paste into the art-director session)

~~~text
You are the art director for The Ninja RPG (repository perseverance484/tnr-tools). This session reworks ONE jutsu
icon: Replacement Technique. Read docs/handoffs/REPLACEMENT_TECHNIQUE_REWORK_SESSION_PROMPT.md first.

The goal is a FAITHFUL UPGRADE of the old icon: the same scene players loved, rendered to the premium TNR pixel-art
standard. It is not a new concept.

What the jutsu does (game data): D rank, 20 AP, moves the user to an empty tile next to them. Battle text: "%user forms
a quick seal and vanishes in a puff of smoke, leaving behind a decoy. In the same instant, they reappear elsewhere on the
battlefield." The decoy is the classic log.

The old icon (attach as the SUBJECT reference): a ninja in black with a pink-red sash, mid-leap and spinning away inside
whirling white-blue chakra rings, while a cut log lies where they stood, in a sunlit forest clearing. Players missed it
because it shows the swap happening. Keep that scene, that pose energy, that log, and that daylight.

What to add from our later icon (attach only where a brief says so): a white smoke puff bursting around the log where the
user vanished, and a blue chakra trail linking the log to the ninja, so the swap reads instantly.

Premium standard: detailed pixel art with crisp edges, clean readable forms, strong rim light on the ninja and the log,
confident value contrast. Two dominant shapes, the ninja and the log, readable at 45 px on a phone. The forest is
simplified and softly lit so it never competes with them. Nothing important in the bottom-left or bottom-right corner
(jutsu lists cover them with 28 px badges); nothing touching the edges.

Exclusions: no text, kanji or runes; no village headband symbol or other franchise insignia; no frame or UI; no
night scene, no dark void background; no extra characters; no weapons drawn except as in the old icon.

Run the four briefs in section 2 of that file, ONE per isolated generation session, one square candidate each. Do not
process, crop, upscale or upload anything. Return every raw named by its brief id, e.g. raw_replacement_technique_RT-1.png.
Fail fast: reject a raw whose ninja or log is unreadable at 45 px, whose background is busier than the subject, or that
has anatomy errors (extra limbs, broken hands), and regenerate that brief once.
~~~

## 2. Isolated generation briefs (one per session)

Shared header for every brief:

~~~text
Repository: perseverance484/tnr-tools
Workstream: icon overhaul, Replacement Technique rework (docs/handoffs/REPLACEMENT_TECHNIQUE_REWORK_SESSION_PROMPT.md)
Target: Replacement Technique
Jutsu target lock: jutsu ID clh4d6pok0002tb0hx1bxro6l, display name Replacement Technique; no bloodline
Lead: Image Production; supporting lens Art Director
Session: ISOLATED GENERATION, one asset only
State: exploratory until the director approves
Live-game requests/writes: 0. Credentials: none.
Goal/action: the user vanishes in a puff of smoke, leaving a log decoy, and reappears a step away
Rendering lock: premium TNR JUTSU_ICON pixel art; crisp edges, strong rim light, clean readable forms, high value
contrast; opaque, full-bleed; reads at 45 px
Setting lock: sunlit forest clearing in daylight, simplified and softly lit behind the subject; greens and warm light
Composition: two dominant shapes, the ninja and the log; nothing important in the bottom-left or bottom-right corners;
nothing touching the edges
Negatives: no text, kanji, runes; no headband symbol or franchise insignia; no frame or UI; no night or dark void; no
extra characters; no anatomy errors
Generate exactly ONE square icon candidate. No collage. Do not process or upload it.
~~~

| Brief | References to attach (at most two) | What to draw (add to the header) |
|---|---|---|
| **RT-1 Faithful** | `ref_rt_old_original.png` (SUBJECT: composition and characters) | The old icon's scene, same layout: the ninja in black with the pink-red sash mid-leap at upper centre, spinning inside two or three whirling white-blue chakra rings, the cut log lying lower left where they stood, sunlit trees framing the clearing. Upgrade only the rendering: sharper, cleaner, more luminous chakra rings, stronger rim light, a calmer background. |
| **RT-2 Faithful + smoke** | `ref_rt_old_original.png` (SUBJECT) and `ref_rt_new_reverted.png` (ELEMENTS ONLY: the smoke puff and blue trail, not its layout or dark background) | RT-1's scene, plus a bright white smoke puff bursting around the log (the moment of the swap) and a blue chakra trail arcing from the smoke to the ninja's chakra rings. The log, smoke and ninja form one readable diagonal from lower left to upper right. |
| **RT-3 Closer** | `ref_rt_old_original.png` (SUBJECT) | Tighter crop for small sizes: the ninja larger, filling the upper right, wrapped in chakra rings; the log big in the lower left foreground half-hidden in a smoke puff; the forest reduced to soft light and a few trunks. Same characters and colours as the old icon. |
| **RT-4 No person (fallback)** | `ref_rt_old_original.png` (SUBJECT: setting, log and rings) | The same clearing and log, with the ninja replaced by an afterimage: their leaping silhouette dissolving into the whirling white-blue chakra rings and wisps of smoke, so the shape reads as a person who has just vanished. No face or detail on the afterimage. |

## 3. Intake (Claude Code)

1. Save the raws to `art/jutsu_icons/replacement_technique/candidates/` as delivered.
2. Preview them as players see them, next to the old icon:
   `python3 art/jutsu_icons/chakra_overflow/preview_in_context.py docs/design/icon_overhaul/replacement_technique/round1_in_context.png art/jutsu_icons/replacement_technique/refs/ref_rt_old_original.png art/jutsu_icons/replacement_technique/candidates/*.png`
   and send the sheet to the director with notes against section 0.
3. The director picks one; refinements stay in that brief's isolated session. Export 256 px lossless WebP to
   `art/jutsu_icons/replacement_technique/exports/icon_jutsu_replacement_technique_v2.webp` after
   `artpreflight.py --type JUTSU_ICON` passes, then hold it for the batch manifest.
