# One Perfect Crop hidden-core run/readback closeout

**Status:** COMPLETE for the hidden-core production/readback task.  
**Run evidence:** `harvests/inbox/tnr_results_1789599042548.json`  
**Manifest:** `push/47_one_perfect_crop_core_manifest.json`  
**Forge:** 0.4.1  
**Live actor:** dauntless only.

## Created records

- Road Bandit AI: `dKEz_VsgZjrfbtxt4ldo8`
- Harvest Boar AI: `2-gJmijAA8lGns_thDRjz`
- One Perfect Crop quest: `CZIZoHDAOWjxDtVaQwr6V`

The quest read back `VERIFIED / match`.

Both AI records were created and reached Forge `CONFIRMED` at phase `verify`. Forge exported the overall job as `INCOMPLETE / unverified` because its AI verifier reported two classes of drift that are not content defects.

## AI stat drift is expected server normalization

The manifest asserted twelve equal stat weights of 100 at level 100 with `statsMultiplier: 1`.

Pinned game source `studie-tech/TheNinjaRPG@bdec2883` shows that `profile.updateAi` calls `scaleUserStats(newAi)` before writing the row. `scaleUserStats` converts the supplied ratios into level-derived stored values. For twelve equal weights at level 100, the stored value is 278260 for each stat, exactly what Forge read back.

Therefore the `sent 100 / live 278260` diffs preserve the intended equal-stat ratio and are not a failed write.

## AI rule drift is object-key-order noise

The live AiProfile rules preserve the same:

- rule count and order;
- `distance_lower_than` condition;
- gate value 6;
- `RANDOM_OPPONENT` targets;
- exact jutsu IDs and priority order;
- `includeDefaultRules: true`.

Forge's special AI-profile verification compares rule arrays with `JSON.stringify`. The server returned the same objects with keys reordered (for example `action` before `conditions`), so the string comparison reports drift even though the structures are equivalent.

The general asserted-value comparator already compares object keys structurally; the profile-specific rules check bypasses that comparator.

## Closeout

The hidden core records exist and are suitable for hidden testing. Do **not** rerun manifest #47 as a new create job.

This closeout does not make the quest launch-final or publish-ready. Art, scene wiring, Cabbage Seed, rewards/economics, repeatability, eligibility, queued G1/G4 prose edits, final hidden readback, and the separate publish decision remain under `launch.finalization`.

No agent performed a live-game write during this analysis.
