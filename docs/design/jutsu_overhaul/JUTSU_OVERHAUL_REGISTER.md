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

## 2. Blazing Death Star

| Field | Live (2026-10-21 census, push/180) |
|---|---|
| Id | `y0fmp1QvVcQnBoVZVLFfL` |
| Type / rank / gate | NORMAL, C rank, Chunin |
| Reach | `SINGLE`, `OPPONENT`, range 4; weapon NONE |
| Cost | 60 AP, cooldown 7 |
| Effect 1 | `damage` power 30, Fire, instant |
| Effect 2 | `afterburn` 20%, on the target, 2 rounds: from the round after the cast, the target takes an extra 20% of every non-pierce hit it receives as burn damage, from anyone (`tags.ts` `afterburn`; capped at 60% of a hit when stacked) |
| AI-equipped | no (2026-10-21 census, push/158-161) |
| Last edited | 2026-10-18 (classification sweep) |

**Old text.** Description: "Add fire nature chakra to your Shurikens". Battle line: "%user throws a
barrage of shuriken at %target as they are  flying towards target they weave together handsigns as fire
nature chakra envelops the shuriken increasing their speed and their destructive power "
**What is wrong:** it claims the fire makes the shuriken faster, which no effect does; neither text
mentions the afterburn, the jutsu's real second effect; the battle line is one run-on sentence with a
doubled space, no full stop and a trailing space; the description addresses "you" and has no full stop.

### Text (APPROVED, dauntless 2026-10-21; RUL-2026-10-21-008)

- **Description** (D1): "Shuriken wreathed in fire nature chakra blaze across the field like falling stars. They strike the target and leave them smouldering, so the blows that follow burn deeper."
- **Battle line** (B1): "%user hurls a fan of shuriken that ignite mid-flight, slamming into %target as blazing stars and leaving them smouldering."

Not chosen: D2, D3, B2 (in git history).

### Icon (I2 APPROVED, dauntless 2026-10-21; RUL-2026-10-21-008)

- **Theme palette:** Fire, ember orange and molten gold on charcoal.
- **Reserved silhouette (I2, approved):** three flaming four-pointed shuriken in a falling-star arc, each
  trailing a tail of fire.
- Not chosen: I1 (one flaming shuriken with a comet tail) and I3 (shuriken in charred ground with ember
  cracks).
- **Must not copy:** Poisonous Senbon's needle volley, Bakuhatsu's explosions and burst clusters,
  Searing Might's shield, Vaporia Scorch Break's fire fissure.
- **Exemplar (style/material only):** Vaporia Scorch Break,
  `art/jutsu_icons/vaporia/vaporia_scorch_break_jutsu_icon_v1.webp` (ember rendering on a dark ground).
- **Rendering lock:** the reusable block in `docs/reviews/WATERS_DOMAIN_PIXEL_STYLE_ANALYSIS_2026-10-21.md`
  section 7 (high-resolution pixel art; neither painterly nor chunky).
- **Delivery filename:** `icon-jutsu-blazing-death-star.webp`.

### Status

| Part | Status |
|---|---|
| Text | APPROVED 2026-10-21; sent as push/184 (QA ticket 13), awaiting the run |
| Icon | DIRECTION APPROVED 2026-10-21 (I2); prompt `docs/handoffs/BLAZING_DEATH_STAR_ICON_DIRECTOR_PROMPT.md`; raw needs director approval |

## 3. Divine Thunder Slap

Icons are paused for now (director, 2026-10-21: text and icon suggestions cannot both be open on one
record); this entry is text only.

| Field | Live (2026-10-21 census) |
|---|---|
| Id | `Je0gvHDVCm__vy2rT8YBB` |
| Type / rank / gate | NORMAL, B rank, Chunin |
| Reach | `SINGLE`, `OPPONENT`, range 4; weapon NONE |
| Cost | 60 AP, cooldown 6 |
| Effect 1 | `damage` power 20, Lightning, instant, scaled on Taijutsu (Speed, Strength) |
| Effect 2 | `increasedamagegiven` 20%, **target SELF**, 2 rounds: the user's own attacks hit harder, from the round after the cast |
| AI-equipped | no (2026-10-21 census, push/158-161) |
| Last edited | 2026-10-18 (classification sweep) |

**Old text.** Description: "Give your opponent a shocking hit." Battle line: "%user claps his hands
together as they begin to crackle with lightning. Suddenly, %target reels in pain as a bright and subtle
hit caresses their cheek."
**What is wrong:** neither text mentions the jutsu's second effect (the user's damage boost); the battle
line uses "his" for every caster, and "subtle" and "caresses" undercut a thunder slap; the description
addresses the reader ("your opponent").

### Text (PROPOSAL, pick one of each or edit)

Description:
- **D1** "The user claps their hands until they crackle with lightning, then delivers a thunderous
  open-palm slap. The charge lingers in their hands, making their next attacks hit harder."
- **D2** "A slap carried on a clap of thunder. Lightning bursts from the user's palm on impact, and the
  leftover current keeps surging through them, strengthening their attacks for a short time."
- **D3** "Divine lightning gathers in the user's palm and lands with a ringing slap. The storm stays with
  them afterwards, adding weight to every attack they make for a short while."

Battle line:
- **B1** "%user claps their hands until they crackle with lightning, then slaps %target with a
  thunderous crack, keeping the leftover charge sparking in their own palms."
- **B2** "Lightning gathers between %user's palms and breaks across %target in one ringing slap, leaving
  %user crackling with power."

### Status

| Part | Status |
|---|---|
| Text | DRAFT, awaiting director pick |
| Icon | PAUSED |

