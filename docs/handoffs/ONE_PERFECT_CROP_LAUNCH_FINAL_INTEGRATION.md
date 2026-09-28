# One Perfect Crop launch-final — integration handoff

**Status:** READY FOR REPOSITORY INTEGRATION; LIVE EXECUTION REMAINS USER-OWNED  
**Prepared:** 2026-09-27  
**Repository:** `perseverance484/tnr-tools`

## Frozen references

- reviewed execution SHA: `b080825c46cdaf33c78f163821ddd3394fcfafd4`
- reviewed manifest: `push/54_one_perfect_crop_launch_final.json`
- reviewed manifest hash: `0b942400`
- imagePack ref: `6a4f439a77517b23935c17058c2ec644f280e91e`
- round-2 review: `docs/reviews/ONE_PERFECT_CROP_LAUNCH_FINAL_R2_REVIEW.md`
- integration source / post-review evidence head: `5ccecf0386ddb23e8ec2bd71af75e76b8f972e99`
- this handoff document is committed afterward for coordination only and is not required in the integration merge
- main observed while preparing handoff: `5bbc030b1c20a3939f1586c9403a7213e591a420`
- merge-base: `2f5c54ba4ec04596783a972f4c084b89d8087cec`

The implementation reviewed at `b080825c` is unchanged after review. Commits through the
post-review evidence head add only durable review/workstream records.

## Why integration is required

Forge's GitHub manifest picker is configured for repository branch `main` and directory
`push/`. The reviewed `push/54_one_perfect_crop_launch_final.json` exists on the ChatGPT
launch-finalization branch but not on `main`, so it will not appear in Forge until the
repository integration is complete.

## Integration method

Use a normal merge of the ChatGPT branch into current `main`; do **not** copy only the
manifest or cherry-pick the image files into unrelated history.

The immutable image pack names commit
`6a4f439a77517b23935c17058c2ec644f280e91e`. A normal merge preserves that commit as an
ancestor of the integrated result, which keeps the generator's ancestry guard and repository
image provenance intact.

At handoff preparation, `main` is one unrelated sentinel commit ahead of the merge-base and
the branch/main net diff is confined to One Perfect Crop assets/state/reviews/manifest plus the
OPC Forge regression in `forge/test/runner.test.mjs`. The sentinel commit changes
`docs/DRIFT.md` and `state/schema_sentinel.json`, so no overlap is expected.

## Operator/integrator procedure

From a clean clone:

```bash
git fetch origin --prune

# Re-verify the refs. Do not integrate a moving target.
git merge-base --is-ancestor 5ccecf0386ddb23e8ec2bd71af75e76b8f972e99 origin/chatgpt/opc-launch-finalization-20260924
MAIN_NOW="$(git rev-parse origin/main)"
echo "main=$MAIN_NOW"

git checkout -B opc-launch-final-integration origin/main
git merge --no-ff 5ccecf0386ddb23e8ec2bd71af75e76b8f972e99 -m "opc: integrate reviewed launch-final hidden package"
```

If `MAIN_NOW` is not `5bbc030b1c20a3939f1586c9403a7213e591a420`, inspect the
new `main` delta before continuing. Proceed only if it does not modify the OPC integration
surface or Forge planner/manifest behavior; otherwise stop and return for reconciliation.

Before pushing `main`, confirm the immutable pack ref is still an ancestor:

```bash
git merge-base --is-ancestor 6a4f439a77517b23935c17058c2ec644f280e91e HEAD
```

Then run the same offline gates used for the reviewed candidate:

```bash
python3 push/54_one_perfect_crop_launch_final.gen.py \
  --image-ref 6a4f439a77517b23935c17058c2ec644f280e91e --check

python3 skills/building-tnr-content/scripts/validate.py \
  push/54_one_perfect_crop_launch_final.json \
  --ctors skills/building-tnr-content/data/45c_DATA_constructors.json \
  --pool skills/building-tnr-content/data/32b_DATA_pool.json \
  --entities skills/building-tnr-content/data/45d_DATA_entity_schemas.json \
  --checks skills/building-tnr-content/data/45g_DATA_checks.json \
  --lints skills/building-tnr-content/data/45h_DATA_lints.json

node forge/tools/check_manifest.mjs push/54_one_perfect_crop_launch_final.json

npm ci --prefix forge
npm test --prefix forge

python3 skills/producing-tnr-art/scripts/artpreflight.py \
  art/one_perfect_crop/one_perfect_crop_road_bandit_avatar.webp \
  --type AI_AVATAR \
  --spec skills/producing-tnr-art/data/25x_DATA_art_spec.json \
  --manifest push/54_one_perfect_crop_launch_final.json

python3 skills/producing-tnr-art/scripts/artpreflight.py \
  art/one_perfect_crop/one_perfect_crop_ittetsu_scene.webp \
  art/one_perfect_crop/one_perfect_crop_waystation_keeper_scene.webp \
  --type SCENE_CHARACTER \
  --spec skills/producing-tnr-art/data/25x_DATA_art_spec.json \
  --manifest push/54_one_perfect_crop_launch_final.json

python3 scripts/content_workstream.py validate --all
python3 scripts/content_workstream.py render --all --check
python3 scripts/content_workstream.py --selftest
```

Expected reviewed results:

- generator exact;
- content validator: 0 errors / 0 warnings;
- Forge offline gate: 5 planned items / 0 pre-send problems / manifest hash `0b942400`;
- Forge suite: 523 / 523;
- Road Bandit artpreflight: 0 / 0;
- Ittetsu + Keeper artpreflight: 0 / 0;
- workstream validate/render/selftest: PASS.

If those remain green, push the merge commit to `main` through the repository's normal
integration path. Do not rewrite or force-push `main`.

## After integration

Verify these two facts from `main`:

```bash
git cat-file -e main:push/54_one_perfect_crop_launch_final.json
git merge-base --is-ancestor 6a4f439a77517b23935c17058c2ec644f280e91e main
```

Forge reads `push/` from `main`. After repository/CDN refresh, the picker should expose
`54_one_perfect_crop_launch_final.json`.

Repository integration is **not** authorization to execute live content. Once the manifest is
visible in Forge, the director may separately execute the reviewed manifest while hidden under
the round-2 review approval. Do not publish/unhide as part of that run.

If Forge refuses, pauses unexpectedly, reports an unresolved ref/image-pack mismatch, or returns
readback drift, stop and preserve the result bundle; do not retry or repair live state before
closeout review.
