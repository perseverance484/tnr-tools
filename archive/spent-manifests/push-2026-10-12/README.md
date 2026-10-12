# Spent and withdrawn manifests — 2026-10-12

Both are moved out of `push/` because the builder and Forge pickers list that directory (`push/README.md`).

## 87_skyglass_crystal_mirror_capture.json — RUN, SUCCESS

Read-only Skyglass Crystal mirror capture (RUL-2026-10-12-005).
**Result:** `harvests/inbox/tnr_results_1791766317760.json` (Forge 0.5.0, job `87-mv4jehc4`, `2026-10-12T00:51:57Z`), state DONE, outcome success. `item.get` x7, all ok and `persistOk`, zero mutations.
Crystal target types returned: Fortify Crystal III (LEGENDARY) targets **ARMOR**; Heal Crystal III `iJM0kb1i6iNXjADJlZGV_` (LEGENDARY) targets **WEAPON**; Damage Crystal II, Afterburn Crystal, Drain Crystal (EPIC) and Hemorrhage Cystal, Offense Crystal 1 (RARE) target WEAPON. All seven are non-hidden. Heal Crystal III is the only public LEGENDARY WEAPON crystal captured, so it is the mirror source for the Skyglass Crystal's undecided fields. Field adoption is Fable's next implementation step.

## 88_ghost_ship_deployed_damage_settings_capture.json — WITHDRAWN, NOT RUN

Forge 0.5.0 rejected it at selection: `persist "full" is only allowed for the audited content-record point reads gameAsset.get, jutsu.get, item.get, bloodline.get, quests.get, profile.getAi, ai.getAiProfile` (`forge/src/runner/manifest.mjs` `normalizeCapture`). The only other mode, `summary` (the default), stores just `ok`, a row count and any error code, never the returned body (`forge/src/runner/runner.mjs` `_captures`). So `misc.getDmgConfig` values cannot be captured through the Forge in any mode, and no other public procedure exposes the deployed engine version. No read was issued.
Options, recorded for dauntless: (a) the operator reads the live damage config or build version manually; (b) a separately reviewed Lane A change adds `misc.getDmgConfig` to the Forge's audited full-persistence allowlist; (c) keep the documented limitation that the offline harnesses use engine source defaults.
