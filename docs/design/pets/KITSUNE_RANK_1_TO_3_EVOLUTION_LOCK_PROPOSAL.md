# Kitsune — Rank 1 → 2 → 3 Evolution Lock (HISTORICAL / SUPERSEDED)

> **SUPERSEDED / VISUAL DEMONSTRATION REJECTED (director, 2026-10-20).** This earlier plan starts with already-mature multi-tail figures and prescribes changes too subtle to read as evolutions. Its Rank 1→3 art lineage and no-new-tails/mild-change restrictions are **not approved for further production**. Historical image candidates remain style-quality references only. See [KITSUNE_JUVENILE_GROWTH_METAMORPHOSIS_RESTART_20261020.md](KITSUNE_JUVENILE_GROWTH_METAMORPHOSIS_RESTART_20261020.md) for the current restart proposal: juvenile base, Rank 1–4 growth, Rank 5–9 visibly transformative stages, Rank 10 capstone proposed.

**Status:** PROPOSED art direction; director approval required before promotion to a generation lock.  
**Date:** 2026-10-20  
**Source:** `studie-tech/TheNinjaRPG@19e2010f9cd3f9be26fff96cca0bf6dece322f11`. Species `pet-species-65` (Kitsune), LEGENDARY. Actual game ranks: **1 Companion → 2 Scout → 3 Tracker**.  
**Scope:** Four existing individual Rank 1 images, four proposed Rank 2 images, then four Rank 3 images derived **only from their respective accepted Rank 2 predecessor**. No changes to game, no production uploads.

## Principle: anatomy before effects

The four director-accepted Rank 1 variants already have flowing multi-tail fans, luxurious neck fur and substantial fantasy detailing. **Do not add extra tails, crowns, armour or dramatic energy to make an early rank-up.** Make **one visibly readable physical improvement per rank**, saving the spectacular changes for later ranks. A different palette or extra glow is NOT evolution.

| Stage | Reserved physical change | How to recognize it at 160px | Explicitly reserved for higher ranks |
| --- | --- | --- | --- |
| **Rank 1: Companion** — existing, LOCKED | Lean adult fox spirit. Pointed ears, recognizable face, four native legs, individual connected bushy tail fan. Current fur pattern and decoration are accepted; no redraw. | Distinct fox head + full tail fan + light, flowing stance. | Additional tails, heavy protective mantle, large claws, crown. |
| **Rank 2: Scout** — PROPOSED | **Stronger shoulder/chest silhouette.** Deepen the upper chest modestly, tighten shoulder musculature and give both forelegs a visibly braced, confident stance. Sharpen *existing* cheek fur slightly without adding a new hanging mantle. | Chest becomes more substantial and the front stance looks secure, while still sleek and agile. | No new tails, enlarged paws/claws, armour, wing-like fur, tall crown. |
| **Rank 3: Tracker** — PROPOSED | **Hunting legs / ready-to-pounce silhouette.** Keep R2's strengthened chest; develop forepaws and hind haunches a further modest step and lower the body into a forward-ready tracking stance, eyes alert. Natural fox claws may become clearer, **not** giant blades. | Noticeably sturdier paws and a lower spring-loaded posture than R2. | No extra tails, protective layered shoulder shields, oversized talons, crown, giant chakra flare. |

**Progression scale:** subtle-to-moderate, not a three-stage metamorphosis. A viewer who ignores colours, markings, and aura should still distinguish R1, R2 and R3 by front-body shape and stance. Subject scale, age, number of tails, face, and relative camera must not jump. The actual in-game generic `RANK_APPEARANCES[1]` and `[2]` already emphasize a braced Scout and heavy-pawed Tracker; these concepts specialize that intent to Kitsune.

## The locked inputs

**Species base (identity for Rank 1 only):** `five_tailed_golden_kitsune_sprite.png` · SHA-256 `c2eb7d4b3b98d7758c9eb12518a86fbb6b78d604153be1165db23216bd1c92a7`

| Variant | Player's permanent trait selections | Rank 1 image — source of Rank 2 ONLY | SHA-256 |
| --- | --- | --- | --- |
| **A — Ember** | Ember (0) · Pale tips (10) · Wind (0) | `ember_tailed_kitsune_spirit_sprite.png` | `6afe4a8863b16f31d914fb14188a3194bfcd91467a6f611c6588dd80240bf24d` |
| **B — Moonlit** | Moonlit (1) · Crescent marking (1) · Moon (5) | `moonlit_five_tailed_fox_spirit.png` | `b1cc706446ebd249594e3e6a861f95ffd2e21d72a6d625bbd00d7d32615ba5b4` |
| **C — Jade** | Jade (10) · Mismatched eyes (5) · Lightning (4) | `jade_lightning_five_tailed_kitsune.png` | `5b203778f448c5b73aaf8e84f1c9d16acd29e3091867ed6e311e643bbf1e5d50` |
| **D — Obsidian** | Obsidian (9) · Dappled accents (9) · Spirit (7) | `celestial_five_tailed_kitsune_sprite.png` | `66a87f5213d139d401c60752d7cc66e7bb42334f1ab39c2db9faa7b637e29815` |

These are **raw ChatGPT generations**, not measured production exports. All originals currently 1254×1254 RGBA; source names are not TNR upload filenames. Match *actual attached bytes*, not filenames alone. A named file does not prove a generator consumed it.

## One reusable prompt — both rank-ups

Replace only `[RANK]`, `[RANK_CONCEPT]`, `[PREVIOUS_RANK]` and the permanent trait fields; **attach exactly one image: that individual's latest accepted appearance**. No other pet image or the original species-base image enters the rank-up call.

```text
Draw exactly ONE new image of the SAME individual Kitsune fox spirit
shown in the attached Rank [PREVIOUS_RANK] image, evolving naturally
to Rank [RANK] of 10.

IDENTITY LOCK: Keep this exact fox's facial identity and muzzle, ears,
natural four-legged anatomy, existing number of separately attached
bushy tails, permanent [PALETTE] colour placement, individual
[MARKING] characteristic and contained [AURA] signature. The selected
palette is the source of colour, not the species-base sample. Retain
all previously developed anatomical structures. Do not invent new
tails, appendages, horns, wings, paws or ornaments. No other fox.

NEW EVOLUTION MILESTONE (apply once, physically, not as paint):
[RANK_CONCEPT]
It must be visible in the shape at thumbnail size, while remaining
only a MILD but NOTICEABLE advance over the attached image.
Do not age, enlarge the camera zoom, merely recolour, or add a large
effect to simulate power. Preserve the recognizable individual.
The body remains agile and fox-like, not a hulking final form.

RENDERING: premium TNR pixel art, carefully formed crisp pixel clusters,
clean dark silhouette, elegant intentional linework, richly resolved
natural fur, distinct cel-shaded depth, high quality material highlights
without painterly brush blur. Maintain the source's three-quarter
perspective, facing and comparable subject scale. One full animal,
completely inside a square canvas, with visible paws and tail tips.

FINAL SPRITE: transparent negative space including all gaps between
tails and legs; no environment, floor, shadow, border, labels, smoke,
oversized exterior halo or disconnected magical geometry. Preserve
the pet's EXISTING subtle aura identity without expanding it.
```

### Rank insertions — same words across A, B, C, D

**Rank 2 / Scout** (previous Rank 1):

> Gently deepen the upper chest and shoulders into a sturdier but still sleek fox profile. Both forelegs take a grounded, alert scouting stance, with slightly stronger natural forearm definition. Refine the existing cheek and shoulder fur tips, but do not add a new layered mantle. Preserve the exact existing tail fan and paws.

**Rank 3 / Tracker** (previous Rank 2):

> Keep the sturdier Rank 2 shoulders and recognizable cheek fur. Develop naturally broader fox forepaws and stronger hind haunches, with slightly clearer natural claws. Shift the stance into a lower forward-ready tracker about to spring, retaining the same camera. Existing tail fan and all R2 development stay intact; no extra tails, no large protective mantle.

## Sequence — *do not skip parentage*

1. Generate **A Rank 2** from A Rank 1 and compare at full + 160px to its parent. Reject if change too weak, too dramatic, wrong traits, new tails or malformed anatomy. Director approves or adjusts the **shared Scout prompt** before it is reused.
2. Repeat the **identical approved Rank 2 concept** for **B, C and D**, each with only its **own Rank 1** image and persistent trait slots. Do not borrow A's anatomy image.
3. Generate **A Rank 3 using only approved A Rank 2** (never A Rank 1). Director approves or adjusts **shared Tracker prompt**; then B, C, D each evolve from their own approved Rank 2.
4. Assemble **four columns A/B/C/D × three rows R1/R2/R3**, the species base held separately above/left for comparison. Use actual accepted images, not image-generation synthesis of a gallery. Report eight distinct parent→child links with source+output SHA-256.

**Review gates:** same species identity and tail count; variant colour/marking/aura continuity; only one expected rank milestone; no giant morphology jumps; clean transparent cutout; crisp pixel style; 160px silhouette progression. Failing one variant triggers revision of that variant, **not** a silent different prompt for its siblings. If a shared prompt fails repeatedly, revise it deliberately and recheck already generated siblings.

**Camera caution:** the currently accepted images face toward the viewer's right. For the demonstration, preserve the *source facing* during generation to prevent redraw/reflection drift; TNR's actual combat path normalizes facing separately. The game's current automated pet prompt instead instructs left-facing, so shipping the prototype prompt unchanged requires implementation review.

**Mode caution:** Native-transparent ChatGPT images are suitable for this demonstration; TNR's current Nano Banana/851-labs pipeline stages on uniform #f0f0f0 grey and removes that backdrop. Adapt the final background sentence to this staging rule if this wording is implemented in the live generator; do not confuse a gray source with an opaque final pet sprite.

**Current state:** Rank 1 images user-approved by prior conversation. Rank 2 and Rank 3 direction PROPOSED, image generation not yet accepted or validated. User owns visual lock; no production requests/writes.
