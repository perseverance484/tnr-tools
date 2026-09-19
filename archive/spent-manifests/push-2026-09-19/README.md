# Spent manifests — 2026-09-19

## 53_godstorm_failed_items_repair.json — RUN AND VERIFIED

The targeted Godstorm repair, replaying the 9 writes that did not land in
`harvests/inbox/tnr_results_1789829183863.json`. Archived here because it has been run:
`push/README.md` requires it, and the builder and Forge pickers list `push/`, so leaving a spent
write-manifest there is one tap away from creating three duplicate `SCENE_BACKGROUND` records.

**Result:** `harvests/inbox/tnr_results_1789842714086.json`, Forge 0.5.0, `2026-09-19T18:31:54Z`.
`state: DONE`, `outcome: success`, 9/9 `VERIFIED` with verdict `match`, 0 drift, 0 unverified,
0 failed, 0 skipped. `harvest.py verify` reports `9 ok, 0 fail, 0 unverified, 0 skipped -> verified`
(exit 0). Six requested full captures all persisted.

It was the first production use of a repo-backed image pack. Its `imagePack` binds all eight
processed WebPs to `art/godstorm/` at commit `10fb25704dff1bab8105cd83631e0d524193ef0d` by
SHA-256, and the binding was checked end to end after the run: every one of the eight URLs the
live records now serve was fetched and hashed, and all eight digests equal the pack's exactly.

That is the whole chain verified by content rather than by trust:

    repository blob -> verified fetch -> upload -> live record -> served bytes

The two drift guards in `forge/test/` resolve this manifest through
`make_image_pack.mjs findManifest()`, so they still check this archived pack against the committed
art. If any of the eight files under `art/godstorm/` is ever re-processed, they fail until the pack
is regenerated — which for an archived manifest means the art no longer matches what was actually
shipped live, and that is worth knowing.
