# Repo upload - 2026-08-26 (merged)

Flat upload to the repo ROOT. Files with these names already exist and will overwrite; the rest
are new. Nothing here needs a folder path.

## CRITICAL - overwrite, and do this one first

- `45c_DATA_constructors.json` - **the copy currently in the repo is WRONG.** It resolved the
  `enum_ref` for objective `sectorType` by bare name and picked up `SECTOR_TYPES` from
  `drizzle/constants.ts` (VILLAGE, OUTLAW, SAFEZONE, HIDEOUT, TOWN) instead of the one in
  `validators/objectives.ts` (specific, random, from_list, user_village, current_sector,
  enemy_village). The builder fetches this file at page load, so preflight is currently rejecting
  every legal quest objective and would accept illegal ones. Two documented laws (24 and 55)
  contradicted it and nothing caught it. Source-verified: exactly one such name collision exists
  in the whole codebase, so this fix is complete.

## Overwrite

- `schema_extract.py` - carries the enum-scoping fix above
- `chroma.py` - reads the art spec

## New

- `45d_DATA_entity_schemas.json`, `45e_DATA_constants.json` - reference copies, not fetched by
  the builder. NOTE law 83: the `DMG_*` values in 45e are compiled-in DEFAULTS; the engine reads
  live values from the `gameSetting` table.
- `artpreflight.py`, `artpreflight_selftest.py`, `shotlist.py` - the art determinism tools
- `SKILL.md`, `prompts.md` - producing-tnr-art skill, style block rewritten to cite the spec
- `balance.md`, `pipeline.md` - building-tnr-content references

## Already current, not included

`builder_bundle.js` (v4.23), `45g_DATA_checks.json`, `32b_DATA_pool.json` - uploaded earlier
today and unchanged. The archive folders and the rest of `tools/` are unchanged too.

## Skills

`SKILL.md` and `prompts.md` are the producing-tnr-art skill; `balance.md` and `pipeline.md` are
building-tnr-content references. Repackaging and reinstalling the skills is a separate step from
this repo upload - the repo copy is for editing and diffing, the installed skill is what runs.
