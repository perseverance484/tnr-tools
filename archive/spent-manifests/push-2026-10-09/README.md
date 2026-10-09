# Spent manifests — 2026-10-09

## 80_ai_pool_reequip_census_stage1.json — RUN, SUCCESS (AI list not retained)

Read-only stage 1 of the 82 shared-AI-pool jutsu battle-description / re-equip census
(evidence: `docs/reviews/AI_JUTSU_82_REEQUIP_EVIDENCE.md` on `claude/ai-jutsu-reequip-validation-7ywxag@62ad0cf`).
Archived because it has been run: `push/README.md` requires it, and the builder and Forge pickers list `push/`.

**Result:** `harvests/inbox/tnr_results_1791583362574.json` (Forge 0.5.0, job `80-mv1idrdt`,
`2026-10-09T22:00:03Z`–`22:02:42Z`), manifest hash `1047e4b3`, state DONE, outcome success,
83/83 reads ok, zero mutations.

- `jutsu.get` x82, `persist: "full"`, 82/82 `persistOk`: every pool id in `32b_DATA_pool.json`
  resolved, with names matching 32b and `jutsuType: AI`; every one has a non-empty `battleDescription`.
  **This is the before-image and recovery source for the jutsu edit.**
  B28 is live as `Recoil Slam` (`ElSK-RCrLjddEUm76FZrs`), hidden, battleDescription
  `%user unleashes Recoil Slam on %target`.
- Live jutsu records carry `required{Ninjutsu,Genjutsu,Taijutsu,Bukijutsu,Bloodline,Sage}Mastery` and no
  `required*Offence/Defence`: the upstream stat rework is live on jutsu as well as AIs.
- `profile.getAllAiNames`: ok, **522 rows** (live AIs with rank != ELDER). Only the count is kept: Forge
  stores list procedures as counts (already noted for push/77 in `push-2026-10-08/README.md`). The AI
  list itself is therefore not in the bundle, and stage 2 (push/81–84) point-reads every known AI id instead,
  using 522 as the completeness check.
