# Dragon King's Scroll and Tiger's Scroll: icon rework

- **Director, 2026-10-25:** "Let's do scrolls. Start with the dragon scroll". Shape (director's pick): **hanging scroll
  pair**. Both stay hanging scrolls, unrolled; a painted creature replaces the writing (a fire dragon, later the white
  tiger), so the quest's two rewards read as a set.
- **Where they come from:** *Blood of the Tiger, The Dragon's Wrath* (`DOiYuFgUVCIKc7ecpLtnD`, visible event quest: 500 PvP
  kills). Each is a Legendary consumable that teaches a Forbidden S-rank jutsu and is destroyed on use.
- **Roles:** the art director makes the raws; Claude Code processes and builds the suggestion. The director picks.
- **Live-game requests/writes:** 0.

## The items

| Item | Id | Teaches | Live art | Problem |
|---|---|---|---|---|
| Dragon King's Scroll | `Apc3YBy_gWux5g9dpN1kB` | Dragon King's Impact (`FytS2iqFInf1go6WhOvUU`): a blade wreathed in a chakra dragon, plunging from the air; fire damage, afterburn, wound | parchment hanging scroll, dark wood rollers, a gold dragon wax seal, the characters 祝福 ("blessing") | the writing is unrelated to the jutsu and is the focus; flat, plain rendering |
| Tiger's Scroll | `U_vp884X6iwsgUVnGj6GR` | Fury of The White Tiger (`QXE9J0fnu1t-DAGTGbaCX`): seven inner gates, a tiger-shaped shockwave | white hanging scroll, a white tiger head in blue, red cord | flat, low-detail; done after the dragon, to match it |

**Text flag (director's call, not in this ticket unless asked):** Tiger's Scroll's description is a copy of the dragon's,
"Unseal the power of the forgotten Dragon King." It should name the White Tiger.

Refs in `art/item_icons/forbidden_pvp_scrolls/refs/`: `ref_dragon_kings_scroll_live.webp`, `ref_tigers_scroll_live.webp`,
`ref_dragon_kings_impact_jutsu.webp` (the jutsu icon: the dragon's look and colours), `style_dragons_scroll.webp`,
`style_demon_scroll.webp` (our approved scroll rendering).

## Design (the pair)

- **Shared frame:** a hanging scroll (kakejiku) shown upright and fully unrolled, slightly angled; dark lacquered wood
  rollers with gold end caps top and bottom; a silk brocade border; aged cream paper; a short hanging cord. No writing.
- **Dragon King's Scroll:** a crimson and gold fire dragon coils down the paper, maw open at the bottom, flame-tipped
  whiskers; a deep crimson brocade border; the dragon's eye the brightest point. Colours from the jutsu (crimson, ember
  orange, gold). Warmer and redder than the jade Dragon's Scroll, and a different silhouette from every rolled scroll.
- **Tiger's Scroll (round 2):** the same frame, a white tiger mid-leap in white and ice blue, a navy border.

## Target (art spec `ICON`)

Square 1:1, 256 x 256 lossless WebP under 460,800 bytes, transparent, small margin (the rarity frame sits behind it).

## Shipping

One suggestion per item, `image` only, each with its own rationale (the Tiger's description fix rides with its icon if
the director approves it).
