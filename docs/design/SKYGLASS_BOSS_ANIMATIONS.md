# Skyglass boss animations: marked set pieces

Director, 2026-10-28: "Need high quality animations to pull this off. Players need to clearly understand the danger but
it needs to look good too. Boss animations especially." Mechanics: `SKYGLASS_WRECK_ENCOUNTERS.md` (showcase bosses,
icon language). Style: Edo-era Japanese fantasy ninja pixel art (`ghost_ship_art_bible/`, RUL-2026-10-26-002).

## How the game draws them (theninjarpg `libs/threejs/combat.ts` ~610-680, `util.ts` showAnimation)

- **One sprite per hex.** Every effect on a hex gets its own sprite at a fixed scale (`EFFECT_ANIMATION_SIZE = 50`), centred on the hex.
  - `staticAnimation` loops while the effect lasts.
  - `appearAnimation` plays once when the effect lands.
  - `staticAssetPath` is a still image stretched to the hex.
  - A pattern of 19 hexes is 19 copies of the same tile animation, so **a telegraph is a tile that reads as a field when repeated**.
- **Asset format:** ANIMATION asset, a vertical strip of square frames, with `frames` and `speed` fields.
  - Created hidden, then unhidden by literal id; battles load only unhidden assets (law 16b/16c).
  - New filename for every revision (law 32).
  - Strip under 460,800 bytes.
- **The four kinds of animation:**
  - **Telegraph:** the ground effect's `staticAnimation`, looping for the round it stands.
  - **Detonation:** the damage effect's `appearAnimation`, played once on each hit hex.
  - **Boss aura:** a buff's `staticAnimation` on the boss.
  - **Cast flourish:** the `appearAnimation` on the boss's self effect.

## Readability rules (the danger must read first, beauty second)

1. **Shape carries the meaning; colour confirms it.** Each threat type has its own silhouette, so players with colour-blindness can still read it.
2. **Telegraphs sit on the ground; detonations rise.** Telegraphs are flat, low-contrast at the edge and bright in the core; they never hide a character. Detonations are tall, fast and loud.
3. **Telegraphs pulse with one shared cadence** (about 0.8 s), so a field of marked hexes breathes together. Tiles must join seamlessly into a field with no visible hex seams.
4. **The safe hex must be the most inviting thing on the board** during an arena-wide mark: bright, calm, upward-pointing.
5. **One palette family per threat, shared across every boss**, so the language is learned once:
   - heavy damage: ember red into white-hot;
   - control/lock: violet into ink. Violet means control or lock, not stun: the violet set pieces apply the set-piece lock (RUL-2026-10-28-015: elemental seal, +10 AP on every jutsu, +2 cooldown on Move and Replacement Technique) or a root;
   - lingering: bile green;
   - safe: Skyglass cyan.
6. **Clear test:** at the delivered size, on a real battle background, with three characters standing in the field, someone who has never seen the fight can say "get out" or "get here" within a second.

## Asset list

### Shared language (every boss)
| Id | Kind | Look | Loop / length |
|---|---|---|---|
| tg_heavy | telegraph | cracked ember ring on scorched stone; the cracks glow and pulse inward | loop ~0.8 s |
| tg_control | telegraph (control/lock) | violet ink chain links coiled flat on the ground, slowly tightening | loop ~0.8 s |
| tg_linger | telegraph | bile-green seep bubbling up through floorboards or stone | loop ~1.2 s |
| tg_safe | telegraph | Skyglass emblem (four-point star in a diamond) rising light, calm | loop ~1.6 s |
| dt_heavy | detonation | the ring bursts: ember column, debris, white flash frame | one-shot ~0.6 s |
| dt_control | detonation | chains snap up and lock, ink splash | one-shot ~0.6 s |
| dt_linger | detonation | seep erupts into a pool (then tg_linger stays as the pool) | one-shot ~0.5 s |

### Core Horror (stage boss)
| Id | Kind | Look |
|---|---|---|
| ch_collapse | detonation | the deck caves in around him: splintered planks and dark water |
| ch_rupture | detonation | skyglass-tainted rot bursts up through the floor |
| ch_maw | detonation | a vast maw of black water and teeth rises across the arena; per-hex tiles form it |
| ch_bile_spit | cast/hit | glob arc and splash, for his plain attack |
| ch_enrage | aura | rot glow and drip on him under 50% |

### The Crowned Captain (showcase boss)
| Id | Kind | Look |
|---|---|---|
| cc_crownfall | detonation | a frost-pointed skyglass shard falls point-first and shatters; the mark under it is a thin blade shadow (tg_heavy variant) |
| cc_command_absolute | detonation | the crown's sigil stamps down and chains lock every unsafe hex (tg_control / dt_control at boss scale) |
| cc_shardstorm | detonation | a hail of small skyglass shards; rotating patterns |
| cc_recall | summon flourish | an echo pulled out of chakra haze, eyes lighting first |
| cc_crown_aura | aura | his crown's frost points and the crystal on his armour glinting in slow pulses (phase 1-2; must sit on the existing avatar, no redraw) |
| cc_last_directive | aura | the crown and every armour crystal blaze white-cyan (phase 3) |
| cc_phase_shift | cast flourish | crown flare and shockwave at 60% and 30% |

### The Captain (Wreck boss)
| Id | Kind | Look |
|---|---|---|
| cp_bell_toll | detonation | a temple-bell shockwave ring (Great Bell Toll) |
| cp_command | aura | a command banner snapping in a wind behind him (Unbroken Command) |

## Production

- **Telegraph and detonation tiles:** built in code as pixel art (Pillow), so cadence, seams and palette are exact and repeatable. The builder is pinned in the repo, as with Ethereal Rebirth (`art/jutsu_icons/ethereal_rebirth/animation/build_strip.py`).
- **Boss signatures and auras:** art-director key layers drawn in fresh sessions (reference zip per prompt, as for the art batch), then animated in code. This is the Ethereal Rebirth v5 route.
- **Approval previews:** every animation is shown as a GIF on a real battle frame at the delivered size, with characters standing in the field, before upload. Previews use the battle-recording tooling in `docs/design/ethereal_rebirth_animation/`.
- **Order:**
  1. The shared language first; every boss depends on it.
  2. Then the Crowned Captain.
  3. Then the Core Horror.
  4. Then the Captain.
