# Bandit war camp: avatar rework (six AI)

- **Director, 2026-10-25:** "Go ahead with the six bandit avatars. We'll do it as a suggestion"
- **Why:** these six are the only realistic painted scenes among the game's 544 AI avatars (full war-camp background,
  683 x 1024). Every other AI is a transparent pixel-art sprite. The client stretches AI avatars to a square
  (`Avatar.tsx`, `aspect-square` with no `object-fit`; art spec `AI_AVATAR`), so these show squashed, background and all.
- **Scope:** avatar art only. The kits, ranks and rules from push/223 are unchanged.
- **Roles:** the art director makes the raws; Claude Code keys, pads, exports and builds the suggestion. The director picks.
- **Session prompt:** `docs/handoffs/BANDIT_WAR_CAMP_AVATARS_SESSION_PROMPT.md`.
- **Live-game requests/writes:** 0.

## The six

Each keeps its current character, weapon, pose and colours; only the rendering and the background change.

| AI | Id | Lvl / rank | Character (from the current portrait) | Accent |
|---|---|---|---|---|
| Mara Vane | `fv33ZNwcZ_eXFWt-d-yrF` | 70 Jonin | woman, long dark wavy hair tied back, charcoal fitted gear with belts and pouches, red scarf, a kunai in one hand and a coil of wire in the other, low wide stance | red |
| Kellan Flint | `dVr5LmHVke0wYz52uWlZr` | 80 Jonin | young man, short dark hair, cream scarf, navy jacket with dark lamellar shoulder and arm guards, quiver on the back, a short bow in one hand and a kunai in the other, crouched | cream |
| Sable Crow | `FQ0ouWe29LXiUficxTACS` | 90 Jonin | woman, deep indigo hood, a cloak of black crow feathers, dark fitted armour, a short curved blade in each hand, lunging | indigo |
| Brigg Tusk | `t4tCdrXKXhQ15l3u4XH-c` | 100 Jonin | huge bearded man, topknot, heavy black armour, ochre sash and leg wraps, a studded iron club held two-handed, braced | ochre gold |
| Yara Reed | `mNvh7ddWnV412kGt9zVX8` | 110 Elite Jonin | woman, woven straw hat, a cloak of dried reeds and grass, moss-green clothes, a long-handled sickle, low stance | moss green |
| Goro Blackthorn | `fh8BgCYYChLhPNMFKRZ4I` | 120 Elite Jonin | scarred bearded man, topknot, fur collar, black armour, crimson sash, a long sword in one hand and a short blade in the other, wide stance | crimson |

Refs: `art/ai_avatars/bandit_war_camp/refs/ref_<slug>_current.webp` (the current portraits, character only) and
`style_{wayward_blade,thorn_ambusher,road_bandit}.webp` (live house-style AI sprites of the same register: the rendering
target).

## Target (art spec `AI_AVATAR`)

Square, 1:1 exact; delivered at 320 px, source about 640 x 640; lossless WebP under 460,800 bytes; full body, centred,
padded to square after keying (never cropped). House style: crisp pixel lineart, flat cel shading, limited palette, soft
even lighting, eye-level flat 3/4 view, near-black garments with one accent. No glow (they are weapon fighters).

## Shipping

One suggestion manifest, six AI edits of `avatar` only (an AI-editable key), each with its own short rationale. New
filenames `ai_<slug>_v1.webp`. Built after the director approves all six.
