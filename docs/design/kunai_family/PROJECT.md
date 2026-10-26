# Kunai family: icon upgrade plan (Ikazuchi Kunai first)

- **Director, 2026-10-25:** "Let's do ikazuchi kunai. Research naruto kunai and actual kunai and develop a plan to upgrade
  this image to our premium pixel art and higher quality"
- **Roles:** the art director makes the raws; Claude Code processes and builds the suggestion. Art direction is the
  director's.
- **Live-game requests/writes:** 0.

## 1. The family

| Item | Id | Element | Where players get it | Live art |
|---|---|---|---|---|
| **Ikazuchi Kunai** | `GMF1JZ0MChUHc7AtnKABw` | Lightning (damage 22) | Storm War Cache; craftable | twin-flanged kunai, ring at the guard (no pommel ring), lightning scribble over everything, **opaque black square background** |
| Katon Kunai | `sXaqXBYXGHvK75D7Bpo1h` | Fire (damage 22) | Ember War Cache; craftable | same twin-flanged base as Ikazuchi, ember edges; old `utfs.io` host |
| Stonefall Kunai | `4ILs8HFIRQG56ygG-uGrW` | earth (presumed) | not captured yet (census parts 3-4) | not seen |
| Wave Kunai | `tFH-9RLeCUcVByQbqd2ic` | water (presumed) | not captured yet | not seen |
| Zephyrfang Kunai | `RIK6tVrKHPEJHz8B_y9dK` | wind (presumed) | not captured yet | not seen |
| Bloodthorn Kunai | `yVNeLzxHSFkNpTPnlm7yQ` | wound | Bloodthorn Cache | **the quality bar**: ring pommel, cord grip, crimson vein-etched blade, gem at the guard, tassel; transparent |
| Kunai | `u9mXSgVW_QjkRzCejGXZ1` | Metal | shop; 2 AI | the classic plain kunai (ring pommel, wrapped grip, flat blade); low detail |

The five elemental kunai are one set (one per war cache), so they share one base design and differ by element. Ikazuchi
is first and sets that base. Refs: `art/item_icons/kunai/refs/ref_*_live.webp`.

## 2. Research

**The real kunai** ([Wikipedia: Kunai](https://en.wikipedia.org/wiki/Kunai)): a farming and masonry tool, thought to
come from the masonry trowel; a leaf-shaped blade of soft wrought iron 20-30 cm long, often sharp only at the tip; a
**ring at the pommel** for a cord, so the handle could be wrapped as a grip, lashed to a pole as a spear, or used as an
anchor or piton. Variants: short, long, narrow, saw-toothed and wide-bladed. Mostly a tool, used as a weapon for
stabbing rather than throwing.

**The anime kunai** (popular image; [Narutopedia](https://naruto.fandom.com/wiki/File:Using_kunai_launcher.png)): a small
dark dagger, a symmetric leaf or arrowhead blade with a centre ridge, a **cord-wrapped handle** and a **ring pommel**.
The famous variant is the **three-pronged kunai with a seal on the handle** (Minato's Flying Thunder God kunai), which is
also a lightning ("thunder god") association. That one is a recognisable franchise prop: **we avoid it** (house rule: no
franchise looks), and we never put a seal or writing on the grip.

**What this gives us:** the silhouette everyone reads as "kunai" is **leaf blade + wrapped grip + ring pommel**. The live
Ikazuchi and Katon break it (twin flanges, the ring moved to the guard), so at 45 px they read as a generic fantasy
dagger. Bloodthorn keeps it and is the best of the set.

## 3. What is wrong with the live Ikazuchi

1. **Opaque black square**: hides the rarity frame and reads as a pasted tile (the art spec wants transparent).
2. **Lightning everywhere**: noisy strokes over and around the whole object; at 45 px the shape dissolves into static.
3. **Wrong silhouette**: twin flanges and a mid-guard ring instead of a ring pommel; not a recognisable kunai.
4. **No single focal point**: several equally bright glows.

## 4. The upgrade

**Family base (all five elemental kunai):**
- the classic silhouette: a broad **leaf-shaped blade with a raised centre ridge**, a short collar, a **tightly
  cord-wrapped grip**, a **round ring pommel**, a short loop of cord through the ring;
- diagonal at 45 degrees, **tip lower left, ring upper right** (same as Bloodthorn);
- dark forged steel; the element shows as a **pattern forged into the blade** (as Bloodthorn's crimson veins) plus a
  restrained effect hugging the edges only; one brightest point; transparent background, small margin.

**Ikazuchi (lightning):**
- blue-black storm steel; **branching lightning veins etched into the blade**, glowing pale electric blue, brightest at
  the tip;
- thin crackles of electricity hugging the **edges only**, never filling the frame;
- deep indigo cord grip, steel ring pommel, a small pale-yellow cord tassel (the thunder accent);
- brightest point: the spark at the tip;
- nothing else: no clouds, no background, no three prongs, no seal or writing.

**Rendering:** our premium pixel art, matching Bloodthorn Kunai and the approved scroll icons: bold clean dark outlines,
cel shading with painterly texture, crisp material detail (steel, cord), limited palette.

## 5. Checks before it ships

- At 45 px on the COMMON frame it reads as "kunai" first and "lightning" second.
- Transparent; artpreflight `--type ICON` clean; 256 x 256 lossless WebP.
- Beside Bloodthorn it looks like the same family; beside the four other elemental kunai (later) it sets their shared base.

## 6. Order

1. Ikazuchi Kunai (this round): `docs/handoffs/IKAZUCHI_KUNAI_SESSION_PROMPT.md`.
2. After census parts 3-4 capture Stonefall, Wave and Zephyrfang: read their elements and art, then Katon, Stonefall,
   Wave and Zephyrfang on the approved Ikazuchi base, attached as the PAIR reference.
3. Optional: the plain shop Kunai on the same base, in bare steel.

Each ships as a suggestion, `image` only, with its own rationale.
