# Chakra Overflow: icon project

- **Director, 2026-10-23:** "probably the cornerstone jutsu of the game... the most seen jutsu in the game by far... the
  most important icon in the game. The essential damage steroid. The symbolic chakra power up. Needs to be the best, most
  iconic, high quality icon we do... It deserves a project of its own." Split out of jutsu upgrade batch 1
  (`docs/handoffs/JUTSU_BATCH1_ICONS_ART_REQUEST.md`, which continues with the other nine).
- **Owner of every decision below:** the director (art direction, CLAUDE.md section 10). This file proposes; it decides nothing.
- **Live-game requests/writes:** 0. Data below comes from the public reads of 2026-10-23
  (`harvests/inbox/tnr_results_1792732003454.json`).

## 1. What it is and why it matters

| | |
|---|---|
| Id | `e2eC-x4UXc5m6QexNbx8w` |
| Live | NORMAL, A rank, Jonin; self; 40 AP; cooldown 7; damage given +25% twice (stacked), 2 rounds; `injectableInBattle: true` |
| Use | **107,720 battle uses**, the most of any jutsu: 6.6% of all jutsu use in the game, 1.6 times the next (Sonic Slash, 67,993) and 3 times anything not a starter. 298 players have it equipped. |
| Role | the universal damage steroid: the buff nearly every build opens with, seen every day by almost every player, in their own bar and in their opponents' battle logs |

So the icon has to do three jobs at once: be recognized instantly in a crowded battle bar, read as **"power up"** before
anything else, and look like the flagship of the collection.

## 2. Where players see it (from the game source at 107d7a8)

| Place | Size | Source |
|---|---|---|
| Battle action grid, default | 112 px and up, with the name label under it | `combat/page.tsx:103` |
| Battle action grid, small-actions mode | about **45 px on mobile** (7 columns), about 70 px on desktop (9 columns) | `combat/page.tsx:102` |
| Jutsu lists and loadouts | tile with a **28 px level badge on the bottom-left corner** and a count badge bottom-right | `CombatActions.tsx:330-339` |
| Every tile | rounded corners (0.75 rem) and a 2 px border clip the corners | `ContentImage.tsx:103,128` |

Design consequences: **the bottom corners are covered** in lists, the four corners are rounded off everywhere, and on
mobile the whole icon is about 45 px. The emblem must live in the central area and read as one shape at 45 px and 32 px.

## 3. Acceptance criteria (the bar for "nothing less will suffice")

1. **Reads as a power-up at 32 px** without its label: a viewer who has never seen it says "buff" or "power up".
2. **One silhouette**, recognizable in grayscale and blurred (the preview's silhouette test).
3. **Unique in the bar:** no confusion with any approved icon (starter 6, scroll-jutsu 10, BEE, bloodline families) at
   45 px. It must not be a spiral (the set already has three), a crescent, a dragon, or a ring of fire.
4. **Clear of the corners:** nothing important in the bottom-left or bottom-right quarter-circle.
5. **Brightest-tier luminance and contrast** in the set: it should catch the eye first in a bar of approved icons.
6. **House rendering:** the approved JUTSU_ICON standard (detailed pixel art, crisp edges, strong rim light, luminous core,
   high contrast, full-bleed dark atmosphere); no actor, hands, faces, text, kanji, frames or franchise insignia.
7. **Timeless and simple:** an emblem that could serve as the game's symbol for chakra power.

## 4. Decision 1: color (director)

| Option | Reads as | For | Against |
|---|---|---|---|
| **A. Chakra blue to white-hot core** | pure chakra | matches "chakra" literally; blue is rare among the warm power icons | blue reads calm or defensive to many players |
| **B. Gold to white-hot core** (the current icon's warmth) | power, energy, a steroid | continuity with the icon players know; gold reads as "power up" in most games | gold sits near the fire icons (Searing Might, Blazing Fang) |
| **C. Blue body bursting into gold** | chakra pushed past its limit | tells the story in the color itself: calm blue erupting into hot gold where it overflows | the hardest to keep readable at 32 px |

Recommendation: **C**, if the art session can hold it at 32 px; otherwise **B** for continuity.

## 5. Decision 2: concept direction (director picks one or two for round 1)

Each is one bold emblem, the metaphor of the jutsu, no actor.

| # | Direction | The emblem | Why it could be the one | Risk |
|---|---|---|---|---|
| D1 | **The breaking vessel** | a brimming orb of chakra cracking open, light bursting through its fissures and spilling over the rim | "overflow" literally: more power than the vessel can hold | can read as "shatter" (a debuff) if the cracks dominate |
| D2 | **The flare** | a compact white-hot core with a crown of flame-tongues erupting upward, like a sun flare rising | the universal power-up shape: upward, explosive, bright | close to a fireball if the palette is warm |
| D3 | **The surge** | a bold upward chevron or arrowhead made of rushing chakra, sparks streaming off its edges | the clearest "buff" signal at 32 px; no confusion with attacks | can look like a UI arrow rather than a jutsu |
| D4 | **The opened gate** | a seal or tenketsu node at the center bursting open, chakra pouring out of it in all directions | "beyond the natural limit": the body's chakra point thrown open | must avoid Eight Gates / franchise symbols and mandalas |
| D5 | **The overflowing pillar** | a column of chakra shooting up from a pool that floods over its own rim | combines the pool (overflow) with the rise (power) | the Ethereal Rebirth pillar already exists (green); must differ clearly |

Recommendation: **D1 and D2** in round 1. D1 says "overflow" and D2 says "power up"; the best icon may combine them
(an orb whose overflow erupts upward as a flare).

## 6. Process

1. **Round 1 (concepts):** for each chosen direction, 3 to 4 generations, one per isolated session
   (`docs/workflows/ISOLATED_ART_GENERATION.md`), in the chosen color. Raws to `art/jutsu_icons/chakra_overflow/candidates/`.
2. **Review in context:** every candidate goes through `art/jutsu_icons/chakra_overflow/preview_in_context.py`
   (mobile bar, desktop bar, 112 px tile with level badge, 32 px, silhouette test) on one sheet, against the current icon.
3. **Shortlist:** the director picks one or two; round 2 refines the composition and color only.
4. **Final checks:** the section 3 criteria one by one, `artpreflight --type JUTSU_ICON`, export 256x256 lossless WebP to
   `exports/icon_jutsu_chakra_overflow_v1.webp`.
5. **Ticket:** its own suggest-mode ticket (icon plus the approved text), or ride batch 1, as the director prefers.

## 7. Text

The batch-1 draft (`docs/design/jutsu_overhaul/BATCH1_TEXT_DRAFTS.md`, section 1) stands as the starting point; it gets
the same scrutiny and is finalized with the icon so both tell the same image.

## 8. Reference

- Current icon (predecessor record; never attach to a generation): `art/jutsu_icons/batch1/originals_live/original_chakra_overflow.webp`.
- Approved style: `art/style_refs/jutsu_icons/bee/`, `art/jutsu_icons/scroll_jutsu/exports/`, `art/jutsu_icons/starter/exports/`.
