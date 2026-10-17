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

## 76_the_wayward_challenge.json — RUN, CREATED BOTH RECORDS, AI DRIFT UNDER INVESTIGATION

Creates a new Wayward Blade AI, then the hidden event quest that fights it. Archived because it
has been run: leaving a spent create manifest in `push/` is one tap from duplicate records.

**Result:** `harvests/inbox/tnr_results_1791510874027.json` (Forge, `2026-10-09T01:54Z`),
`state: INCOMPLETE`, `outcome: unverified`, postflight 1 match / 1 diff / 1 unresolved.

- Quest `wayward_challenge_quest` -> `EymfSL5MDPfrCpaT4O4Y5`: **VERIFIED**, verdict `match`.
- AI `ai_wayward_blade` -> `uO4sBfcUGUZ7SYUTEaq4Q`: CONFIRMED, verdict `drift`. Rules pushed to
  its own AiProfile `ut9tduz-TcEUjFf6qje3z` (`assertedRules: true`).
  - The eight per-type stats (`ninjutsuOffence` ... `bukijutsuDefence`) and `preferredStat` are
    absent from the live read: upstream `studie-tech/TheNinjaRPG@c6c3d33` (see `docs/DRIFT.md`)
    removed them and added single `offence`/`defence`. The repo's pinned 45c/45d predate that, so
    `validate.py` and the factory passed a shape the live game no longer has.
  - Generals came back at 1,460,842.5 each (level 100, statsMultiplier 3).
  - Passive effects landed (IDG 40 / DDT 15, rounds 99) but the server dropped `statTypes`
    (the upstream rework also changed that enum) and added `direction`/`description`.
  - `offence`/`defence` were not sent and are unknown; read back by push/78.
