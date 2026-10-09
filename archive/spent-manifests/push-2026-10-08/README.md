# Spent manifests — 2026-10-08

## 77_wayward_blade_live_capture.json — RUN, NEGATIVE RESULT

Read-only capture for the opponent of the hidden candidate event The Wayward Challenge
(branch `fable/wayward-challenge-candidate`). Archived because it has been run: `push/README.md`
requires it, and the builder and Forge pickers list `push/`.

**Result:** `harvests/inbox/tnr_results_1791505778681.json` (Forge, `2026-10-09T00:29Z`), 11 reads,
zero mutations.

- `profile.getAi {userId: aWwhu2wloj5nm9SgzeNxi}` (Wayward Blade): `ok: true`, `data: null`,
  4-byte body. This is the signature `state/one_perfect_crop_bandit_resolution.md` reads as
  "catalog id no longer resolves to a live AI record". **Wayward Blade no longer exists at this id.**
- `jutsu.get` x9, every Wayward-trio jutsu id listed in `44c_DATA_ids.json`: all `NOT_FOUND`.
  None of those jutsu ids resolve.
- `gameAsset.get Eu4B9CbWQRMkSEeXCQ1Y-`: ok. Shine training ground, `SCENE_BACKGROUND`, public.
  (The user has since ruled it out as the quest backdrop.)

**Consequence:** the 44c "AIs - Wayward daily trio (LIVE, candidate/hidden)" rows, and the
`answers/names_ai.json` seed rows for Wayward Blade/Ember/Gale, are stale for at least the Blade and
the nine jutsus. The Wayward Challenge's `opponentAIs` points at a dead id and must not be pushed
until the opponent is re-resolved or rebuilt.

**Not possible through Forge as of 0.5.1:** confirming whether a Wayward Blade exists under a new id
by name. Forge list captures (`profile.getAllAiNames`, `jutsu.getAllNames`) record only a row count
in the bundle, and `persist: "full"` is restricted to single-record reads
(`forge/src/runner/manifest.mjs`).
