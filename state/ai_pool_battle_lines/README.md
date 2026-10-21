# AI pool battle lines (82 shared-AI-pool jutsu)

Working folder for the battle-description pass on the 82 jutsu in `32b_DATA_pool.json`.
**Nothing here is in `push/`, on purpose.** The jutsu edit severs every AI's combat link to an
edited jutsu (laws 18, 60), so it must run only between a validated unequip and re-equip, and
those don't exist yet.

## Files

| File | What it is |
|---|---|
| `recovered/ai_jutsu_battle_descriptions_82_backlash_palm_forge.json` | Reconstructed manifest as supplied by the director, byte-exact (sha256 `373764377a0e4f9dd898d991d3f255811fc8448280ea14039db6aa5b853ff8c8`). The original bytes were lost; only the B28 line is the previously approved text. Kept for comparison. |
| `recovered/AI_JUTSU_82_REEQUIP_GATEPLAN.md` | Reconstructed gate plan, byte-exact (sha256 `541a974e9e7217b404267945afdb3f75a692138ede6558338c221374367380bd`). |
| `battle_lines.json` | **Source of truth** for the draft: one line per code, plus `rename` and `target` where they change. |
| `build.py` | Builds the two files below from `battle_lines.json`, the pool file and a capture bundle. `--check` fails if they are stale. |
| `ai_pool_battle_lines_draft.json` | Generated draft manifest: 82 jutsu `convert` entries. Do not hand-edit. |
| `REVIEW.md` | Generated prose review sheet: mechanics, new line, recovered line. |

Rebuild: `python3 state/ai_pool_battle_lines/build.py harvests/inbox/<bundle>.json`

## What the draft changes

- `battleDescription` on all 82: 2-3 sentences, Edo-era ninja voice, chakra-driven, describing only
  effects the live record carries. Lint (in `build.py`): `%user` always, `%target` exactly when the
  jutsu targets another fighter, no exclamation marks, dashes or curly quotes.
- `name` on 17 jutsu, including B28 Recoil Slam → Backlash Palm (director-approved). The other 16
  are proposals. Each was checked against the jutsu name catalog (`Jutsu_name_key` is unique).
- `target` on B31 Rallying Spiral: OTHER_USER → ALLY (director, 2026-10-21). Its buffs used to land
  on the enemy.
- `injectableInBattle` re-sent at its captured live value (law 20).

## Status

- Built from `harvests/inbox/tnr_results_1792551342555.json` (push/157, 2026-10-21). It runs as
  `push/170_ai_pool_battle_lines_edit.json`, between the unequip (162-169) and the re-equip (171-177).
  See `push/README.md`.
- **Changed live since the first draft** (edited in the game, not by the repository): B04 Executioner Seal
  (2026-10-11, instant kill -> lowers the target's jutsu power for 5 rounds), S02 Quick Strike and S07
  Rapid Fire (2026-10-15, new effects; S07 now targets OPPONENT). Their lines were rewritten to match,
  and B04 gets a proposed rename, Choking Seal.
- Director prose review of the lines and the 16 proposed renames is pending.
- **Open balance question:** B28's recoil effect has `rounds: 0`. The engine skips recoil on the round
  it is cast (`tags.ts` `recoil`, `!effect.isNew && !effect.castThisRound`), so it may never fire,
  and the approved line describes an effect that may not happen.
- After an operator-verified live run, update the pool registry names (and B31's target) through
  `32_REGISTRY_shared_ai_pool.md` -> `32b_DATA_pool.json`. Do not edit 32b by hand.

Validation of the draft: `validate.py --strict` 0 errors, 0 warnings;
`forge/tools/check_manifest.mjs` exit 0 (82 planned updates). The recovered manifest on its own:
0 errors, 82 law-20 warnings (strict fails).
