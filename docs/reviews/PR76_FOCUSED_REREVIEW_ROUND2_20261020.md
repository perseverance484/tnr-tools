# PR #76 — focused independent re-review, round 2 (2026-10-20)

**Lead:** Engineering Auditor; **scope:** only round-1 findings F1/F2 and directly affected pins/contracts/tests; **verdict:** **PASS WITH NOTES — F1 and F2 closed. Recommend PR #76 for integration into main before the concurrent Forge census branch.** This is not an operator game-run approval.

| Field | Verified |
| --- | --- |
| Repo / PR | `perseverance484/tnr-tools` / #76 |
| Implementation branch | `claude/stormrender-highest-scaling-yj2nef` |
| Round-2 frozen code head | `503d98d059ff1eaaa2f7cabbcd17b3e63cbcdb2e` |
| PR tip | `e48d3fb0952092b421961bc3edfb369370d59e09` (one later `dist/building-tnr-content.zip` auto rebuild only; no source-code delta) |
| Current main | `e13bc9fa085b37bd84ab7736256da8d1ad2a4a99` |
| Original merge-base | `383ac0f45bc47004a4a8915f4c724c79b35798f3` |
| Main → reviewed head | 9 commits ahead / 0 behind |
| Pin | `studie-tech/TheNinjaRPG@85cecaebf4ada2e265a18a1405f63c9637443275` |
| Round-1 review | `docs/reviews/PR76_INDEPENDENT_INTEGRATION_REVIEW_20261020.md`, review SHA `62b81061d644054e798261e6ab82661caa147f09` |
| Safety | GitHub repository and pinned source reads only; live-game requests/writes 0/0; credentials none |

## F1 — CLOSED: preserve `publicLocations` and map-location objective fields

Previously `mergeForUpdate("quest")` dropped the newer `publicLocations` column, and the game update validator defaulted its omission to `false`. At the corrected SHA:

- `forge/src/runner/fields.json` is pinned to 85cecae: 38 quest fields, including `publicLocations`; the `mergeForUpdate` known-fields copy can preserve a fetched live `true` and an explicitly asserted `false` can override it.
- `forge/src/runner/nested.json`, also pinned to 85cecae, includes `structureAssetId`, `locationName`, `locationDescription`, `structureScale` on sampled objective variants (dialog, move_to_location, collect_item, deliver_item, defeat_opponents).
- `forge/tools/derive_nested.mjs:42-52,69-80` now searches other validator modules, including the owning `mapLocation.ts`, and refuses duplicate declarations.
- `forge/test/adversarial.test.mjs:1163-1186` asserts the preserved live setting, explicit false override, valid map-location keys and typo rejection.
- `skills/building-tnr-content/data/45d_DATA_entity_schemas.json` carries the field, and adopted `45c` objective shapes carry all four map-location keys. Root `45c` equals its canonical skill-data counterpart by Git blob SHA.

**Verdict:** Original confirmed drop path is closed at the reviewed source pin. No browser/live deployment was assumed.

## F2 — CLOSED: union-variant type / requiredness changes are guarded

- `skills/building-tnr-content/scripts/schema_diff.py` emits `vfield-type` and `vfield-required` atoms for union variants and pairs them with existing fields in shared `classify()`, handling type-to-type changes, type removal and optional→required tightening. The 45d entity field gate remains intact.
- `scripts/test_schema_diff.py` supplies nine synthetic negative/positive tests including the original `AllTags.damage.power` number→string mutation, omitted type, optional→required, new required fields, ledger evidence/hash mismatch, 45g check and 45f procedure removal. The source logic now marks the previously invisible type flip breaking.
- `scripts/schema_adoption_ledger.py` calls that same gate classifier, and the regenerated hash-bound `state/schema_adoption_ledger_85cecae.json` covers **698** breaking atoms across all five 45x files. Inspection of the committed ledger: 153 (45c) + 18 (45d) + 55 (45e) + 33 (45f) + 439 (45g); class counts sum to 698. The ledger source pins were checked.

**Verdict:** The round-1 F2 counterexample is now recognized and the intended reviewed-removal gate is retained.

## Gates / limitations

- The [Forge PR-head CI run 39461372839](https://github.com/perseverance484/tnr-tools/actions/runs/39461372839) completed **successfully** at frozen head `503d98d`; that is independently verified via GitHub Actions status.
- The author reports Forge 644/644 tests, Python `scripts/test_schema_diff.py` 9/9, all 5 diff/ledger/regen checks, `validate.py push/131` 0 errors/warnings, reproducing fixtures/bundle and budget/pin/size checks. **Reviewer did not independently execute npm, Python extractor/ledger, or a local game-source checkout** in the current GitHub-connector-only environment. The green Forge CI run covers its configured Forge gates, not every claimed Python gate.
- Reviewed the source-to-contract and fetch-merge paths; no new confirmed F1/F2 defect survives. This is a **focused** re-review, not a re-audit of the entire broad extractor redesign.

## Integration / production notes

1. PR #76 can be considered for `main` integration on this review; the tip auto-commit changes only `dist/building-tnr-content.zip` compared to the green source head. Verify live `main` and the tip again at actual merge time.
2. **Merge PR #76 before the independently developed 0.9.0 weapon census**. The census branch is still based on pre-0.8.1 `main` and has overlapping Forge/version/loader/budget/build files. That branch needs its own correction/rebase and review before any integration. Both branches independently claimed `RUL-2026-10-20-001` for different director decisions; preserve PR #76's contract-adoption ruling and give the census size ruling a different unique identifier on its correction branch. Do **not** silently blend them.
3. The deferred law 4/6 reconciliation, expected sentinel output drift, and legacy push/90/93/94 diagnostics remain tracked, not silently cured by the re-pin.
4. A `main` merge/release is **not** authorization to run push/131. Forge version uptake, fresh Stormrender full recapture, 0-error operator gates, suggestion submission, reviewer approval and fresh `item.get` verification remain separate user-owned steps.

**Next:** Independent PR #76 review complete. Main integration may proceed by its authorized integrator, subject to current-ref checks. Do not merge this review branch into main as feature code.
