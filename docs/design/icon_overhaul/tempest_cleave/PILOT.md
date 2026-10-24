# Tempest Cleave: the pilot icon

- **Director, 2026-10-24:** "I think we need to start with exactly one icon and just work it to death. Make it the best
  most fitting premium pixel art icon we can, and go from there." Pilot chosen: **Tempest Cleave**.
- **Why this one:** our version scored 0/10 ("total fail, do not reuse at all"), yet the director gave a clear target: an
  older version players liked. As an abstract wind emblem, it tests the hardest problem in the overhaul: a round, radial
  subject that must still read at 45 px without becoming a blob or a shuriken.
- **Governing direction:** abstract emblems for now (RUL-2026-10-24-002); visual design rules in
  `docs/handoffs/ICON_OVERHAUL_ART_DIRECTION.md` section 2; analysis in `../VISUAL_DESIGN_DEEP_DIVE.md`.
- **Roles:** the art director makes the raws; Claude Code does everything after (RUL-2026-10-23-008 amendment 1). Every
  decision on the art is the director's.
- **Session prompt:** `docs/handoffs/TEMPEST_CLEAVE_PILOT_SESSION_PROMPT.md`.
- **Updated 2026-10-24 (round 1 v2):** under RUL-2026-10-24-003 and -004 the icon upgrades the **original** (the
  fox-masked fighter) and shows the **battle line's moment**: the fighter turning once at the eye of the whirlwind (the
  older version supplies the whirlwind). Premium text draft: `../TEXT_AND_ICON_ROUND1.md` section 1. Where sections 2–3
  below say "no figure" or forbid teal, the v2 prompt overrides them: the figure is in, and the palette is the original's
  (its lightning is cyan).
- **Live-game requests/writes:** 0.

## 1. The jutsu

| | |
|---|---|
| Id | `Ul83iTziN__Z0i_UOzZTK` |
| Live data | EVENT, A rank, Jonin; 60 AP; cooldown 7; area ring around the user (`AOE_CIRCLE_SPAWN`, range 4); damage 45, afterburn 30 for 2 rounds, target takes +35% damage for 2 rounds |
| Description | "A spinning storm of razor wind that carves through everything around the user, friend and foe alike. Its cuts keep singing long after it fades." |
| Battle text | "%user plants their feet and turns once, and the air itself becomes a blade. A storm of razor wind erupts outward in a howling ring, carving through everything within its reach, for the tempest knows no allegiance. Those caught in it are left with wounds that will not close, each cut still singing with the wind long after the gale has passed." |

The icon has to say **a storm of razor wind, spinning, dangerous to everyone near it**.

## 2. What we have

| Version | What it is | Verdict |
|---|---|---|
| **Older version** (director's screenshot; `art/jutsu_icons/tempest_cleave/refs/ref_tc_older_version_crop.png`) | a blue-white whirlwind spiralling into an off-centre eye; dark ink-like streaks on its outer arms; thin forked lightning; small traditional cloud curls along the lower right; slate-blue ground | **the target to beat**: "an older version we could use as inspiration" |
| **Live now** (the original; `ref_tc_live_original.webp`) | a fox-masked fighter casting blue lightning in a storm, burning village behind | a busy scene; not the direction |
| **Ours** (reverted) | a radial ring of steel blades with orange edges | "looks more like a shuriken skill... not intimidating enough... wrong shape and art direction"; **never attach or imitate** |

What the older version gets right: it reads as **wind** (soft, flowing arms, not rigid blades), as a **storm** (lightning,
ink-dark streaks), and as **Japanese** (cloud curls), and its spiral is **asymmetric**: one long arm sweeps out and the
eye sits off centre. What it lacks: premium pixel rendering, value contrast at 45 px (its pale arms sit on a mid-slate
ground), and menace.

At real size (`gate_sheet.py` on the references): the older version's spiral survives the 45 px silhouette test, and its
slate-blue ground makes it the one light icon in a bar of black-ground icons, which is a standout worth testing. Round 1
keeps that ground in TC-1 and tries a dark storm ground in the other five.

## 3. Acceptance criteria (the bar)

| # | Criterion | How it is checked |
|---|---|---|
| A1 | **Reads as a whirlwind of razor wind at 45 px**: a viewer says "tornado", "whirlwind" or "wind storm", never "shuriken", "saw" or "portal" | 45 px name test (deep dive G1) |
| A2 | **One silhouette:** an asymmetric spiral with a clear eye and one dominant sweeping arm | blurred greyscale at 45 px (G2) |
| A3 | **Intimidating:** storm-dark ground, sharp white cutting edges, lightning; the feeling of being caught in it | director |
| A4 | **Not a shuriken:** no rigid radial blades, no points arranged in rotational symmetry, no metal | director, fail-fast |
| A5 | **Distinct** from Ring of Spilled Blood (a red spiral) and from the reworked Aerathiel wind icons: blue-white and storm-grey, never teal or red | bar test beside the kept icons (G4) |
| A6 | **Faithful to the older version's spirit:** flowing arms, ink streaks, forked lightning, cloud curls | director |
| A7 | **Premium TNR pixel art:** real pixels on one grid (pixelsnap), 16–24 colours, hard edges, rim light from the top-left, one glow source (the eye), no gradients or blur | pixel-integrity gate (G6), director |
| A8 | **Safe area:** the eye and the dominant arm in the upper and central 60–70%; bottom corners low-detail | 112 px tile with badge (G5) |

## 4. Process ("work it to death")

1. **Round 1, explore:** six candidates, one per isolated generation session (section 2 of the session prompt).
2. **Claude Code intake per round:** each raw → `pixelsnap.py` → gate sheet: the 45 px name and silhouette tests, a mobile
   bar beside the kept icons, the 112 px tile with badge, 32 px, and the older version and live icon side by side.
3. **Director picks** one or two directions and says what to change.
4. **Round 2 onwards, refine:** only the chosen direction, one change at a time (composition, then values and palette,
   then detail), each round compared with the last at 45 px. Repeat until the director calls it.
5. **Lock:** final export, `artpreflight --type JUTSU_ICON`, side-by-side sheet for the staff thread.
6. **Then:** what worked becomes the template for the other 34 (RUL-2026-10-23-008; this pilot runs first).

## 5. Log

| Round | Date | What happened |
|---|---|---|
| 0 | 2026-10-24 | Pilot opened; round-1 prompt written. |
| 0 | 2026-10-24 | `gate_sheet.py` built and run on the references (older version, live icon, ours as a test). |
| 0 | 2026-10-24 | Round 1 rewritten as v2 (masked fighter at the eye of the whirlwind, tied to the drafted battle line); v1 not run. |
| 1 | 2026-10-24 | Texts approved by the director; round-1 (v2) art session started by the director. Waiting for raws. |
