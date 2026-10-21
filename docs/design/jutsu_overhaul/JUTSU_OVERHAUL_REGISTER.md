# Player jutsu overhaul — register

**Status:** OPEN (2026-10-21). One jutsu at a time, at dauntless's direction: new description and
battle line that match the name and the live effects, plus a new icon. Everything below marked
PROPOSAL is a draft for the director; final prose and art direction are dauntless's
(CLAUDE.md section 10).
**Text rules:** `skills/building-tnr-content/references/jutsu_text.md` (on review branch
`claude/tnr-content-tickets-tcbi34` until accepted).
**Icon protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md` (one jutsu per generation session),
spec `skills/producing-tnr-art/data/25x_DATA_art_spec.json` target `JUTSU_ICON`, the approved
jutsu-icon standard (RUL-2026-10-17-021, RUL-2026-10-20-004; exemplars listed in
`docs/design/starter_jutsu_icons/JUTSU_ICON_REGISTER.md`).
**Source basis:** the 2026-10-06 census (push/68-74) until the push/178-181 census lands; each
ticket is confirmed against that fresh record before it is built.
**Delivery:** text and icon go to the content review desk as Forge suggest-mode tickets (QA tickets
from 12, manifests from push/182). Text can go first; the icon follows as its own ticket once the
art is approved and preflighted, so a rejection of one does not cost the other.
**Live-game requests/writes:** 0.

## 1. Water's Domain

| Field | Live (2026-10-21 census, push/178) |
|---|---|
| Id | `-8W4JOqG3Cb-oPQtF9rMs` |
| Type / rank / gate | NORMAL, C rank, Chunin |
| Reach | `SINGLE`, `OPPONENT`, range 4 |
| Cost | 60 AP, cooldown 6 |
| Effect 1 | `damage` power 20, Water, instant |
| Effect 2 | `increaseheal` 25%, **target SELF**, 2 rounds: the caster's own healing (heals, lifesteal, vamp, absorb) is stronger, from the round after the cast (`tags.ts` `adjustHealGiven`) |
| AI-equipped | no (2026-10-21 census, push/158-161) |
| Classification | element Water, stat None (set 2026-10-18) |
| Last edited | 2026-10-18 (classification and target type only; effects unchanged since 2026-10-06) |

**Old text.** Description: "Encase your foe under a torrent of water." Battle line: "%user engulfs
%target in a powerful surge of water, dealing damage while sapping their strength."
**What is wrong:** the battle line claims it saps the target's strength, which no effect does; neither
text mentions the healing boost; the name's "domain" plays no part in either.

### Text (APPROVED, dauntless 2026-10-21)

- **Description** (D2 with the director's edits): "Within the user's domain, water answers to them
  alone. It rises to crush their foe, then flows back to its master, deepening their healing for a
  short time."
- **Battle line** (B2): "%user spreads their domain across the field, hurling its tide at %target
  before the waters pool back around %user to strengthen their healing."

Not chosen: D1, D3 and B1 (in git history at eeccaa4).

### Icon (I1 APPROVED, dauntless 2026-10-21; RUL-2026-10-21-007)

- **Why:** part of the overhaul; the new icon should show the domain and both halves of the jutsu
  (crushing tide, restorative calm). The current icon was not viewed for this request (no live
  reads); it is not passed to the generator either way.
- **Theme palette:** Water, deep blue and white foam, with one soft aqua-teal healing glow as the
  secondary cue.
- **Reserved silhouette (I1, approved):** a **vast whirlpool basin** seen from a low 3/4
  angle, its outer rim a churning wall of white foam, its calm eye glowing a soft restorative aqua.
- Not chosen: I2 (ring of water walls around a glowing pool) and I3 (torrent onto one point with a
  rising droplet).
- **Must not copy** (reserved by other families): Vaporia's coiling water dragon, crushing water
  column, water sphere and breaking wave; no shield or plates (Searing Might), no chains, no smoke.
- **Exemplar (style/material only):** Vaporia Surfing Strike,
  `art/jutsu_icons/vaporia/vaporia_surfing_strike_jutsu_icon_v1.webp`.
- **Delivery filename:** `icon-jutsu-waters-domain.webp` (corrections `_b`, `_c`).

Copy-ready isolated-session brief (filled for I1):

~~~text
Repository: perseverance484/tnr-tools
Workstream: Player jutsu overhaul (docs/design/jutsu_overhaul/JUTSU_OVERHAUL_REGISTER.md)
Target: Water's Domain
Jutsu target lock: jutsu ID -8W4JOqG3Cb-oPQtF9rMs, display name Water's Domain; no bloodline
Lead: Image Production; supporting lens Art Director
Session: ISOLATED GENERATION, one asset only
State: exploratory until director approves the raw
Live-game requests/writes: 0. Credentials: none.

Goal/action: the caster claims the water around them as their domain; a crushing tide strikes one
foe and the calm waters strengthen the caster's healing
Dominant silhouette: a vast whirlpool basin, outer rim a churning wall of white foam, calm eye at
the centre glowing a soft restorative aqua
Camera/perspective and motion axis: low 3/4 view looking into the basin, clockwise spiral
Secondary effect: soft aqua-teal glow rising from the calm eye
Rendering lock: approved JUTSU_ICON standard; deep blue and white foam, aqua-teal accent; full-bleed
dark designed background; opaque is fine; reads as one shape at 32 px
References attached: Vaporia Surfing Strike (style/material only: water and foam rendering,
contrast, rim light; not its composition or its breaking-wave silhouette)
Composition: one centred focal shape, clear negative space, nothing touching the edges
Distinctiveness exclusions: no coiling dragon, no vertical water column, no sphere or orb, no single
breaking wave, no shield, no chains, no smoke
Other negatives: no ninja, no face, no body, no hands or limbs, no text, no UI, no frame, no circular
seal or floating runes, no franchise imagery

Generate exactly ONE square icon candidate for review.
Do not generate other techniques or a collage.
Do not process or upload the image.
Return the original asset after director visual approval.
~~~

### Status

| Part | Status |
|---|---|
| Text | APPROVED 2026-10-21; sent as push/182 (QA ticket 12), awaiting the run |
| Icon | RAW APPROVED 2026-10-21 ("Honestly this one is approved, it matches the art style enough"); export `art/jutsu_icons/overhaul/exports/icon-jutsu-waters-domain.webp`, preflight 0/0; ticket push/183 waits for push/182 to resolve |
