# tnr-tools repo package - 2026-08-26

## Repo root: the three files the builder fetches at load

The builder pulls these from the repo root at startup. If any one is missing, the panel reads
`partial` instead of `cfg generated`.

- `45c_DATA_constructors.json` - tagged shapes, used by `ctorBad`
- `32b_DATA_pool.json` - shared AI pool, used by `resolvePool`
- `45g_DATA_checks.json` - **NEW, required by v4.23.** Without it the null guard silently reverts to
  stripping every null, which is the safe direction but not the fixed one. Commit this BEFORE the
  bundle, or the deploy looks successful and does nothing.

## Repo root: the bundle

- `builder_bundle.js` - **v4.23**. Loader `?v` unchanged; refresh via ViolentMonkey.
  Panel must read `Content builder v4.23 · cfg generated`.

Deploy order: commit `45g` -> commit the bundle -> verify the GitHub BLOB view shows v4.23 (raw CDN
caches about 5 minutes) -> VM refresh -> check the panel string.

## Repo root: generated reference (not fetched, kept as deploy truth)

- `45d_DATA_entity_schemas.json`, `45e_DATA_constants.json`, `45f_DATA_procedures.json`

All five `45*` files are stamped with the same provenance: generator `schema_extract.py v2.0`, source
drop `TheNinjaRPG-main__3_.zip`, extracted 2026-08-26. Regenerate the whole set from one drop or they
disagree with each other; `stack.py` errors when the stamps diverge.

## `tools/`

The Python toolchain, identical to what ships inside the `building-tnr-content` skill. The skill copy
is what runs; this copy is for editing and diffing. They drifted inside a single session once, which
is why `selfcheck.py` exists - run it and it will tell you if the bundle is stale.

## `archive/guides/`

Migrated into the `building-tnr-content` and `producing-tnr-art` skills, removed from project
knowledge. Also here: `45_DATA_field_schemas.json` (hand-authored, superseded by the generated `45d`,
and wrong in six places when audited) and `50_DATA_combat_facts.md` (its numbers are generated into
`45e`; its formula prose is pending a ruling on reopening `46b`).

## `archive/lore_and_arcs/`

Cut from project knowledge by ruling. Consulted rarely and never during a mechanical build. **Live
exposure:** the Ashen Concord holds 208 unpushed entries and the Salt Crown is unbuilt - writing new
dialog or story beats in either arc needs the file re-uploaded that session.

## Not in this package

- `builder_loader_user.js` - lives in ViolentMonkey and the repo; unchanged by this session.
- The full catalogs (jutsu, item, AI, asset, quest) - unchanged; the columnar `4x_INDEX` twins in
  project knowledge are the working set.
