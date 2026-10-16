# Recipe-aligned cache — native offline proof (Silent Bastion one-of-two reward)

Brief: `docs/handoffs/RECIPE_ALIGNED_CACHE_NATIVE_OFFLINE_PROOF_BRIEF_20261016.md`.
Results: `docs/reviews/RECIPE_ALIGNED_CACHE_NATIVE_OFFLINE_RESULTS.md`.

**Synthetic fixture, not a manifest.** The two caches, six ingredients, bundles and weights in
`engine/lib/cachefix.ts` are scratch values that prove the mechanics only.

```bash
harness/recipe_cache_native_proof/run.sh          # preflight + gates S, F + C99 regression on alt99_f4gate
harness/recipe_cache_native_proof/run.sh flow     # one gate (static|flow)
```

Requirements and isolation match `harness/silent_bastion_condensed99/` (git, bun 1.4.x, python3, `unshare`,
Docker). The engine is pinned to `studie-tech/TheNinjaRPG@0651b039a466516a8fe24fc13b56f60dea11b7eb`. The
suite reuses `harness/silent_bastion_phase1/engine/lib/{graph,driver,report}.ts` and
`harness/silent_bastion_condensed99/engine/lib/run99.ts`, with `TNR_GRAPH` set to the approved `alt99_f4gate`.

| File | Gate | What runs |
| --- | --- | --- |
| `engine/rc_static.test.ts` | **S** | `QuestValidator`, `verifyRewardChoiceForSave`, `buildRewardChoiceCards`, the weighted-cache schema (valid config and 8 invalid configs), 20,000 seeded `resolveWeightedCache` draws per cache |
| `engine/rc_flow.test.ts` | **F** | F1 editor save and item validation · F2 completion → one offer → Arsenal claim, with replays rejected · F3 parallel claims · F4 opening, receipt replay, concurrency, rollback, invalid config, in-run refusal · F5 failure, abandonment and recovery isolation · F6 unclaimed offer plus re-run (RC1) · F7 negative control with caches on `w.complete` |
| C99 regression | S/D/R/E | the frozen `harness/silent_bastion_condensed99` gates on `alt99_f4gate` at this pin |
