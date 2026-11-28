# Isonade animation audit and art brief (2026-11-20)

Read live with `jutsu.get` and `gameAsset.get` on the 18 Isonade jutsu during the QA pass.
Style for new art: Skyglass (hand-painted, thick ink, cel shading, blue-black, pale cyan, rot green;
refs in /mnt/project-files/tnr/art/prompt_refs/). Strips stay under 4096 px tall (the director's rule).

## Current state

| Move | Battle text | Animation now |
|---|---|---|
| Barnacle Hide | Barnacles grind shut over %user's hide. | appear Blank Animation; static `absorb_large_violet` (generic) |
| Tide Draws Back (Breaker warning) | The water pulls away from the shore and gathers around %user. | none |
| Breaker | The wave breaks over %target. | Isonade - Black Water (hit); Open Eye loop on weakness |
| Harpoon Line | %user spits a rusted harpoon through %target. | `toon_explosion_small_yellow` (generic, off-style) |
| Brine Brand (Undertow warning) | Brine burns into %target. | none |
| The Undertow | The undertow drags %target under. | Black Water (hit) |
| Scour | The undertow tears through %target's guard. | none |
| Swell Builds (Bore warning 1) | The sea rears up behind %user. | none |
| Swell Rises (Bore warning 2) | The wave stands over the hold. | none |
| Tidal Bore | The Tidal Bore breaks over %target. | Black Water (hit), shared |
| Omen: Black Water | The water goes still and black. Only the floating crates stay pale. | `water3` tiles, Skyglass Mark Heavy glint / Safe emblem; seal appear Blank |
| Black Water Floods | Black water crashes down. %user surfaces to feed. | Black Water (hit); Open Eye loop |
| Silt Cloud | %user thrashes and braces. Silt clouds the hold. | none |
| Omen: The Deep | %user sinks out of sight. The whole hold goes black. | appear Blank; static `absorb_large_violet` (same as Barnacle Hide) |
| The Deep Crashes | Black water rises to the ceiling and crashes down on %target. | Black Water (hit) |
| Surfaces | %user surfaces through its broken shell, gasping. | Open Eye loop |
| It Rises (every round) | Black water churns around %user. | `water3` appear; Body Water loop |
| Grasping Arm Rises | The deck bursts upward. A wet black arm rises out of it. | Arm Burst (appear) |

## Warning gaps

- Omen: The Deep looks identical to Barnacle Hide, and its line gives no hint that breaking the shield is the answer.
- Swell Rises has no board marker; only the log says the Bore is loaded.
- It Rises prints every round and buries the real warnings.

## Art brief, in priority order

1. Swell Builds: cast on Isonade. The sea rearing up behind it.
2. Swell Rises: loop on Isonade while the marker is up. A tall wave held over it.
3. Tidal Bore: hit on the target. The biggest crash, clearly bigger than the shared Black Water hit.
4. Tide Draws Back: cast on Isonade. Water pulling off the deck and gathering around it.
5. Omen: The Deep: cast plus loop on Isonade. It sinking with dark rings; must not read as Barnacle Hide.
6. Barnacle Hide: loop on Isonade. Barnacles grinding shut, replacing the violet bubble.
7. Brine Brand: loop on the target for the brand's length. A salt-white burn mark.
8. Harpoon Line: hit on the target. A rusted harpoon strike.
9. Scour: hit on the target. Undertow tearing the guard off.
10. Silt Cloud: loop on Isonade. Murky silt around it.

Keep: Black Water (hit), Open Eye loop, Body Water loop, Arm Burst, Black Water omen tiles.
