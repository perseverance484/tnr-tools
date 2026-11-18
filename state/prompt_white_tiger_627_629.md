# Fury of The White Tiger animations: jobs 627 → 628 → 629 (Duet)

Director, 2026-11-17: "Prep the white tiger one for a ticket." This is the run's contract; CLAUDE.md and the
Forge/engine laws still govern. Pattern: Rengoku Rō push/624 → 625 → 626.

**Strip height rule (2026-11-17).** Every strip is <= 4096 px tall. The 300 px Rengoku strips on UploadThing drew as
black boxes on phones (off-Bunny hosts load native; phones cap textures at 4096 px). Never upload a taller strip.

**What it does.** Two new animation assets for Fury of The White Tiger (`QXE9J0fnu1t-DAGTGbaCX`), adapted from
OpenDuelyst (CC0): the **gates** (teal chakra lotus under the caster; `fx_f2_eightgates_teallotus`; 29 × 70 ms,
140 px) and the **tiger** (spectral tiger lunges through the target after a short travel lead-in;
`fx_f2_saberspineseal`; 40 × 80 ms, 102 px). Then a suggestion ticket that puts them on the jutsu and clears the
three v15d custom clips (claw strike, sparks loop, aura burst). No mechanics, text or icon change.

## Steps

1. Pull `perseverance484/tnr-tools` (main). Claim the run lock:
   `node forge/tools/run_lock.mjs claim --holder duet --job "630 + 627-629 Rengoku fix, White Tiger animations" --ttl 45 --wait`.
2. **627, UploadThing route (connector):** upload the four strips in `state/recut_upload/upload_list.json` to the
   director's UploadThing with the same one-off workflow as the Rengoku upload (on your own task branch; results to
   `state/recut_upload/uploaded.json`, copied to main). Then **630 first**: `python3 push/630_rengoku_recut.gen.py`,
   run `push/630_rengoku_recut.json` (2 direct asset edits), read both back (image = new URL, frames 23/35, speed 70,
   hidden false). Then `python3 push/627_white_tiger_animations_ut.gen.py` and run
   `push/627_white_tiger_animations_ut.json` (2 asset creates, hidden). (Forge route instead: run
   `push/627_white_tiger_animations.json`.) Commit the results bundles to `harvests/inbox/`.
   Confirm both creates in the bundle `idmap` (`white_tiger_anim_gates`,
   `white_tiger_anim_tiger`).
3. **628:** `python3 push/628_white_tiger_animations_unhide.gen.py <627 bundle>`, then run
   `push/628_white_tiger_animations_unhide.json` (2 direct edits, `hidden: false`). Read both assets back
   (`gameAsset.get`): `hidden: false`, frames 29 / 40, speed 70 / 80.
4. **629 (Forge, suggest mode):** capture a fresh `jutsu.get` of Fury of The White Tiger into a bundle, then
   `python3 push/629_white_tiger_suggestion.gen.py <627 bundle> <capture bundle>`. The generator refuses if the
   record changed since the read. Run `push/629_white_tiger_suggestion.json` in **suggest mode** (never
   skipPreflight). One suggestion, category ANIMATION, title "New gates and tiger animations". Commit its bundle;
   record the proposal id.
5. Release the lock. Update `state/run_queue.json` rows 630 and 627-629 (done, bundle paths, proposal id) in the same commit.

## Stop and report instead of improvising if

- any create/edit fails or the bundle idmap lacks an id;
- the 629 generator's live-record assertion fails (someone changed the jutsu);
- Forge flags a preflight problem on any job.

## Not in scope

No direct edit of the jutsu (the review desk applies it). No AI re-equip. No other records. Rengoku: only job 630's two asset edits.
