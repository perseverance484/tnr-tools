# FCF animation: lessons from v1-v21 and the research (2026-11-22)

Process
1. Design the whole move first (storyboard), then cut it into engine clips. Never start from what one tile can hold.
2. Block out timing in grey shapes at true game size and the engine's frame rate before any art. Approve timing first.
3. Then a value/hierarchy pass, then art, then polish. Judge at real size, never only on a 2x preview.
4. Art: ask the image tool for a sprite KIT (separate pieces on black), never finished scenes; animate the pieces in
   code as particles. Finished paintings only work as stills; sliding/fading them looks cheap.
5. No silhouettes or art built around the fighter: the fighter sprite cannot be located or matched (White Tiger).

Timing (anticipation -> climax -> dissipation)
6. One climax frame carries the hit: everything important lands together (within ~100 ms). Spreading strikes over
   300 ms reads as a firecracker, not a discharge.
7. Anticipation: a wind-up, plus a one-frame inward pull right before the hit.
8. Snappy, eased motion (ease-out), not linear fades. Dissipation short and low contrast.
9. Real lightning: faint branched leader -> one saturating channel (the impact frame) -> dark gap -> restrikes down
   the SAME channel, unbranched. Lightning reads as one big streak, not a web.

Hierarchy and value (League of Legends VFX style guide)
10. Primary: highest value, strong silhouette, full opacity. Secondary: lower value, smaller, softer. Tertiary: few,
    small, dim. If everything is bright, nothing leads the eye.
11. The highest values only at the climax flash and the leading edge/strike end of moving things.
12. Contrast defines the area of effect (dim the area under the climax). Avoid pure 100 % white or 0 % black.
13. Lower saturation on secondary pieces; one palette across every sprite.

Shape and coverage
14. Fewer, bigger bolts; cover every on-screen direction (check sectors as the player sees them, not on the squashed
    board); fire in an order that walks round the circle so every moment has bolts in different directions.
15. No glowing balls on bolt tips (reads as "sperm"); end on a small crisp glint or nothing.
16. Centre round sprites on their alpha centroid: decorations make crops lopsided and rings misalign.

Engine realities (TNR)
17. Normal alpha only (no additive light), no screen shake, effects cannot light fighters, sprite frame rates, strips
    <= 4096 px tall, tile clips cannot point at the caster. Win on shape and timing.
18. Sound is part of "premium": use the effect appear/disappear sounds.
