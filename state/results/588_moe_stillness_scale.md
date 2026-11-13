# 588 MoE: first per-effect animation scale (Stillness at 2.5)

Why: upstream 8bd670153 (2026-11-09) added `animationScale` (1x-3x, default 1) to every combat tag.
Clips render at `tile.height * EFFECT_ANIMATION_HEX_RATIO (1) * animationScale`
(`libs/rendering/scenes/combatEffects.ts`). The Mother of Echoes clips were drawn for 2.5 hex heights
(docs/design/MOTHER_OF_ECHOES_ART.md), which is what held her go-live (RUL-2026-11-06-131 item 4,
"until the clip-size update"). Director go 2026-11-13 ~03:39 UTC ("You have my go, proceed") on: the
Forge/validator fix, a one-jutsu live test, and the scale choice.

Change: Stillness (A8c_3evIw6fOfnmKIkTgb), effect 0 (the increaseregeneration telegraph: appear
2BrQiTU3Igc3oC0WNv7XT, static loop dFcS4mKAdJNc0yda-pzsa, ground art i2D_-pxpRJHsrneGwMox3, on 36
hexes around the caster) animationScale 1 -> 2.5. Nothing else. Still hidden.

How: hand-sent over the connector under the run lock (claude, 04:24-04:27 UTC), law 18/60 order:
1. profile.updateAi The Silence (IhNR-W1FElTsrWw1KfuQ9) without Stillness. First try refused by zod
   before any write (insertAiSchema requires userId, gender, regeneration, level, the six stats, six
   masteries, statsMultiplier, poolsMultiplier, isSummon, effects); resent with those from a fresh
   read. updateAi merges input over the live row (`{...ai, ...input.data}`, profile.ts), so the
   minimal payload is safe as long as jutsus and items are both sent (both sync by set difference).
2. jutsu.update with the full live record, effect 0 + animationScale 2.5. Server diff:
   "Added: effects.0.animationScale 2.5, effects.1.animationScale 1".
3. profile.updateAi The Silence with Stillness back.

Read back 04:27 UTC:
- Stillness: updatedAt 2026-11-13T04:25:52.640Z, hidden true, effects animationScale [2.5, 1], art ids,
  power, friendlyFire, cooldown 3, method COORDINATES, all 36 coordinates, both texts unchanged.
- The Silence: 8/8 jutsus equipped (same ids as before), AI Heavy Armor on CHEST drop 0, 5,050/5,050 HP,
  stats 1,622,255.8, statsMultiplier 5.83, poolsMultiplier 1, effects increasedamagegiven 30 +
  sealprevent 100. Only The Silence equips Stillness (the 6 other MoE AIs and An Absence read 2026-11-13).

Next: look at it in practice quest 469 (Act 1, the Silence casts Stillness). The 36 marks either tile
hex to hex (art drawn for 2.5: apply 2.5 across the kit) or pile up (drawn for 1: set back to 1).
Then the bulk pass over the 58 MoE jutsu (1,274 animated tags) with law 18 on her AIs.

Tooling: Forge and validate.py refused the key until fable/animation-scale-key (b3937081), awaiting
review. Until it lands, a manifest that carries animationScale cannot run through Forge/mcp_run, and any
Forge edit whose data.effects comes from a capture taken before this write resets the scale to 1.
