# Spent and withdrawn manifests — 2026-10-12

Both are moved out of `push/` because the builder and Forge pickers list that directory (`push/README.md`).

## 87_skyglass_crystal_mirror_capture.json — RUN, SUCCESS

Read-only Skyglass Crystal mirror capture (RUL-2026-10-12-005).
**Result:** `harvests/inbox/tnr_results_1791766317760.json` (Forge 0.5.0, job `87-mv4jehc4`, `2026-10-12T00:51:57Z`), state DONE, outcome success. `item.get` x7, all ok and `persistOk`, zero mutations.
Crystal target types returned: Fortify Crystal III (LEGENDARY) targets **ARMOR**; Heal Crystal III `iJM0kb1i6iNXjADJlZGV_` (LEGENDARY) targets **WEAPON**; Damage Crystal II, Afterburn Crystal, Drain Crystal (EPIC) and Hemorrhage Cystal, Offense Crystal 1 (RARE) target WEAPON. All seven are non-hidden. Heal Crystal III is the only public LEGENDARY WEAPON crystal captured, so it is the mirror source for the Skyglass Crystal's undecided fields. Field adoption is Fable's next implementation step.

## 88_ghost_ship_deployed_damage_settings_capture.json — WITHDRAWN, NOT RUN

Forge 0.5.0 rejected it at selection: `persist "full" is only allowed for the audited content-record point reads gameAsset.get, jutsu.get, item.get, bloodline.get, quests.get, profile.getAi, ai.getAiProfile` (`forge/src/runner/manifest.mjs` `normalizeCapture`). The only other mode, `summary` (the default), stores just `ok`, a row count and any error code, never the returned body (`forge/src/runner/runner.mjs` `_captures`). So `misc.getDmgConfig` values cannot be captured through the Forge in any mode, and no other public procedure exposes the deployed engine version. No read was issued.
Options, recorded for dauntless: (a) the operator reads the live damage config or build version manually; (b) a separately reviewed Lane A change adds `misc.getDmgConfig` to the Forge's audited full-persistence allowlist; (c) keep the documented limitation that the offline harnesses use engine source defaults.

## 81–84 ai_pool_reequip_census_stage2_batch1–4.json — RUN, SUCCESS, CENSUS INCOMPLETE AND NOW STALE

Read-only stage 2 of the 82 shared-AI-pool jutsu re-equip census (stage 1 is push/80, archived under
`push-2026-10-09/`). `profile.getAi` with `persist: "full"` for 535 repository-known AI ids.

**Results:** Forge, 2026-10-12T02:21Z–02:25Z, all DONE/success, every read ok, 0 persist errors:
`harvests/inbox/tnr_results_1791771716198.json` (81, `b17e396c`, 134/134),
`tnr_results_1791771811766.json` (82, `78141288`, 134/134),
`tnr_results_1791771915726.json` (83, `cefd8c20`, 134/134),
`tnr_results_1791771966137.json` (84, `b6a8cd2f`, 133/133).

- 506 non-null bodies, all non-ELDER; 29 ids returned `data: null` (deleted AIs).
- **Completeness check failed:** 506 against 522 live (`profile.getAllAiNames` at push/80), so 16 live AIs were
  not known to the repository. Two were found in later bundles (Jellyfish `1WAgDucRwcwGZ_yQ9r0uN`, Jelly Chakra
  Beast `msKodzIJSH2J_BO-1FCIN`).
- 336 AIs hold at least one pool jutsu (148 of them carry only pool jutsu), and 71 of the 82 pool jutsu are
  equipped somewhere. B28 (Recoil Slam) has 7 holders: IronClawS2, Fire Grunt # 2/# 3/# 4, \*Ava-The Snow
  Terror\*, Ava-The Snow Terror, Ryouichi.
- This census was the before-image for push/109–121 (Bloodright classification). Those runs and push/90–126 then
  wrote to 58 AIs, 38 of them pool holders, so it is **stale for the AI pool pass**. Superseded by the fresh census
  push/157–161.
