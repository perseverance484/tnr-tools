# Forge Presentation Studio P0/P1 — integration and release checkpoint

Verified on 2026-09-20 using repository objects only. **P0/P1 are integrated; Forge 0.5.1 is pinned for release.** Live-game requests/writes: **0/0**. No installed Android session or CDN delivery was tested.

| Checkpoint | Exact commit |
| --- | --- |
| Previous main / reviewed base | `eefefd1afd67111a90c332951a8dd9f83cb99cbd` |
| Approved implementation, present verbatim in main | `5ac0e947196f88c695d0cdee7aabe75a2f0278b2` |
| Independent approval report | `939168b6045e2469ec2c9934429b2c61b4ef1a9a` |
| Stage Forge 0.5.1 / immutable bundle target | `13b313d8eaf0687907178ceedc406a7154e0a473` |
| Verified main / automatic loader-pin commit | `42cbcb8a06a168e594e303c812a61b3d1a1cbeb3` |

The ancestry is linear: `eefefd1 → 05e7156 → 8830443 → ac792ef → 5ac0e94 → 13b313d → 42cbcb8`. The approved SHA is an ancestor of main; no cherry-pick substitution or rewritten implementation was used.

The two release commits change only `forge/package.json`, `forge/src/main.mjs`, `forge_bundle.js`, and the Forge/legacy builder loaders. The presentation tree at the approved SHA and at main is identical (`44a4e8eb8c62455cde029ed3e8b07dd0f5adcf45`). Replacing the approved bundle's two `0.5.0` strings with `0.5.1` produces the released bundle byte for byte. Main's bundle equals the blob at the new immutable pin. The legacy builder's newly pinned bundle is unchanged from its previous pin.

Forge's package, runtime version, and loader report **0.5.1**. The loader has no pending marker and requires `forge_bundle.js` at `13b313d8eaf0687907178ceedc406a7154e0a473`. The release-pin check passes. The budget check remains **339,669 / 354,000 raw; 74,926 / 78,000 gzip**.

The [approval review](https://github.com/perseverance484/tnr-tools/blob/939168b6045e2469ec2c9934429b2c61b4ef1a9a/docs/reviews/REVIEW_2026-09-20_forge_presentation_studio_p1_r1_r3.md) records R1–R3 closed, 522 passing tests, 17 focused assertions, reproducible build/fixtures, and the prior F1–F7 closures. Those tests were run at the approved implementation SHA; this release checkpoint checks the narrow version/pin delta and does not claim a fresh full test run. No additional implementation review is required for these verified version substitutions.

Main's session snapshot at `42cbcb8` still described 0.5.0 and an unstarted size pass. This closeout branch corrects only the digest, its two generated projections, and this checkpoint document. It is based on `42cbcb8`; it contains no implementation changes. The older review branches remain historical evidence and need not be merged to adopt these session updates.

## Next work and carried limits

- P0 size pass and P1 dossier/spec/lint are complete and integrated. The repository-side presentation modules remain outside the runtime bundle; this release does not add a Presentation Studio UI.
- The governing plan remains `chatgpt/forge-presentation-studio-plan@99f1aa8a6fe7cc7361aa613cdcad258bafb9c83e`, `docs/plans/FORGE_PRESENTATION_STUDIO_UPGRADE_PLAN.md`.
- The design contract and Godstorm reference remain a proposal at `chatgpt/forge-presentation-studio-design@4532ef917a1dfb40d00c554fd7f065e13216afc7`. Director acceptance and the concrete P2 brief remain the next design checkpoint.
- Carry source-archive resolution, approved derivatives, MIME/dimensions, exact source pixels, and complete-art readiness into the renderer work. The default golden dossier is not a complete deterministic render: 5 of 23 registry entries have verified bytes; strict exact-byte lint refuses the other 18. Use the existing source archive at `1bca57eeb0c1836a49334dc2f49196a5a3db24c7`; do not generatively redraw named entities.
- Godstorm's push/53 verification remains historical evidence from Forge 0.5.0. This release makes no content or publishing change; the selected captures remain hidden. Android preview/export/share behavior and installed-loader uptake remain unverified here.
- The existing session parity adapter failure on `checks:null` remains outside this work. No green global parity result is claimed.
