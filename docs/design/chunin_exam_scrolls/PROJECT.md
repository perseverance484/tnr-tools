# Chunin Exam scrolls: Earth and Heaven icon rework

- **Director, 2026-10-25:** "Yeah lets do earth and heaven scrolls, since they appear in the live quests. We'll do earth
  scroll first."
- **Direction (director, 2026-10-25):** colour + seal. Keep each scroll's colours, drop the painted 地 / 天 character,
  close the scroll with a wax seal and cord ("do not open"), and press a relief into the seal: mountain ridges for
  Earth, a cloud swirl for Heaven.
- **Why these two:** both are live quest props in The Chunin Exams (`iB3mdNvAZfBWVhsMEVBBl`, visible): two objectives give
  them (Heaven first, then Earth) and a third collects both. Usage check: every captured visible quest (394 of 393
  listed), all 544 AI and the 100 captured items.
- **What dates the old art:** a thick yellow outline glow around the whole sprite, sparkles, and the big painted
  characters, a near copy of the anime's exam scrolls (house rules: no text, no franchise looks).
- **Roles:** the art director makes the raws; Claude Code processes and builds the suggestion. The director picks.
- **Live-game requests/writes:** 0.

## The items

| Item | Id | Live | Colours kept |
|---|---|---|---|
| Earth Scroll | `npOljgp_QZUUd6g9wPBk0` | OTHER, COMMON, "Earth Scroll for the Chunin Exams" | deep forest green brocade, gold fittings, cream paper |
| Heaven Scroll | `5W8HJUSPt15Lu14EFvHqi` | OTHER, COMMON, "Heaven Scroll for the Chunin Exams" | deep navy brocade, gold fittings, cream paper |

Refs in `art/item_icons/chunin_exam_scrolls/refs/`: `ref_{earth,heaven}_scroll_live.webp` (the live art: shape, colours,
gold knob caps) and `style_dragons_scroll.webp`, `style_scroll_of_bastion.webp` (our approved scroll rendering).

## Design

- **A pair, one silhouette:** a closed hand scroll at 45 degrees with the live art's **gold** knob finials (not the steel
  caps of the jutsu-scroll family), so the exam pair reads as its own set.
- **Sealed:** a cord band around the middle closed with a round wax seal, the brightest point. The seal carries a
  pictorial relief, no writing: mountain ridges (Earth), a cloud swirl (Heaven).
- **Colour carries the pair:** Earth deep forest green with an umber-red seal; Heaven deep navy with a crimson seal. The
  forest green sits darker and cooler than the jade Dragon's Scroll so they don't overlap.
- **No outline glow, no sparkles**, transparent background with a small margin so the rarity frame reads.

## Target (art spec `ICON`)

Square 1:1, 256 x 256 lossless WebP under 460,800 bytes, transparent, small margin (the rarity frame sits behind it).

## Known follow-up (not suggestion-mode)

The quest's "deliver the scrolls" objective (`bDndw`) stores the old Earth Scroll image URL as its own icon. Changing
the item does not update it, and suggest mode refuses quests, so that objective keeps the old art until a direct quest
edit (the director's call).

## Shipping

Earth first: one suggestion manifest, one item edit (`image`), with a short rationale. Heaven follows as its own round.
