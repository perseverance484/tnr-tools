# Spent manifests, 2026-11 (repo review W1)

Manifests that already ran live and were harvested from unmerged branches on 2026-11-28, but that the
staged-manifest gate on main (`forge/test/runner.test.mjs`, "compatibility: staged manifests ...") refuses,
because they need tooling that exists only on their source branch or carry keys today's contracts flag.
Their results bundles are in `harvests/inbox/` and their rows in `state/run_queue.json` point here.

| File | Run-queue id | Why it is here |
|---|---|---|
| `631_weapon_effect_targets.json` + `weapon_effect_targets.gen.py` | 631-wt | effects carry `animationOffsetY`, flagged as an unknown key |
| `639_salvager_pool_upsert.json` | 639-pool | a direct connector call, not a Forge items manifest |
| `640_residual_modifier_fix.json`, `641_residual_modifier_fix_bloodline.json` + `640_residual_modifier_fix.gen.py` | 640-rm, 641-rm | use the `zeroInstantResidual` livePatch held for Lane A review (`docs/reviews/REPO_REVIEW_2026-11-27/livepatch_zeroInstantResidual.diff`) |

Note for the W7 archive pass: `push/short_rations.gen.py` still writes `push/639_salvager_pool_upsert.json`
when re-run.
