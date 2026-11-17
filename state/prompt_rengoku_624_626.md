# Rengoku Rō animations: jobs 624 → 625 → 626 (Duet)

Director, 2026-11-16: chose the "tight" variant and said "submit it for review". This is the run's contract; CLAUDE.md
and the Forge/engine laws still govern. Pattern: Celestial Dew push/238 → 239 → 240.

**What it does.** Two new animation assets for Rengoku Rō (`fKQxOwBqZs8PXvpdGlbPg`), adapted from OpenDuelyst's
`fx_f4_obliterate` (CC0): the **strike** (ring of ghost-flame, implosion, dome detonation, smoke; 23 × 70 ms) and the
**smoulder** (afterburn loop; 35 × 70 ms), both 300 px. Then a suggestion ticket that puts them on the jutsu. No
mechanics, text or icon change.

## Steps

1. Pull `perseverance484/tnr-tools` (main). Claim the run lock:
   `node forge/tools/run_lock.mjs claim --holder duet --job "624-626 Rengoku Ro animations" --ttl 45 --wait`.
2. **624 (browser, Forge):** run `push/624_rengoku_animations.json` (2 asset creates, hidden). Commit the results
   bundle to `harvests/inbox/`. Confirm both creates in the bundle `idmap` (`rengoku_anim_strike`,
   `rengoku_anim_smoulder`).
3. **625:** `python3 push/625_rengoku_animations_unhide.gen.py <624 bundle>`, then run
   `push/625_rengoku_animations_unhide.json` (2 direct edits, `hidden: false`). Read both assets back
   (`gameAsset.get`): `hidden: false`, frames 23 / 35, speed 70.
4. **626 (Forge, suggest mode):** capture a fresh `jutsu.get` of Rengoku Rō into a bundle, then
   `python3 push/626_rengoku_suggestion.gen.py <624 bundle> <capture bundle>`. The generator refuses if the record
   changed since the read. Run `push/626_rengoku_suggestion.json` in **suggest mode** (never skipPreflight). One
   suggestion, category ANIMATION, title "New strike and smoulder animations". Commit its bundle; record the
   proposal id.
5. Release the lock. Update `state/run_queue.json` rows 624-626 (done, bundle paths, proposal id) in the same commit.

## Stop and report instead of improvising if

- any create/edit fails or the bundle idmap lacks an id;
- the 626 generator's live-record assertion fails (someone changed the jutsu);
- Forge flags a preflight problem on any job.

## Not in scope

No direct edit of the jutsu (the review desk applies it). No AI re-equip. No other records.
