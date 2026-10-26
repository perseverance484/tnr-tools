# Handoff: retire two stale validation rules (Lane A)

```text
Repository: perseverance484/tnr-tools
Branch: fable/validate-stale-rules
Base: main @ 6d4de246da3fb72b331b357b05040f44de42082b
Code head: 79e8fad82c5c780a7ff8c77436bc17dbbb9639f7 (the one implementation commit)
Head: the tip of this branch at handoff = the commit that adds this file, whose only parent is the
      code head and whose only change is this file. FROZEN until review returns.
Integration target: main @ 6d4de246da3fb72b331b357b05040f44de42082b (re-verify at integration)
Brief: state/prompt_validate_stale_rules.md (RUL-2026-10-25-009; context RUL-2026-10-25-008)
```

The branch was cut from main @ 11585c0 and rebased once, before freeze, onto 6d4de246. The three
commits main gained in between are Lane B content only (push/263, push/264, one results file); none
touches a file this branch changes. Every gate below was re-run after the rebase.

## Objective

Make `validate.py --strict` and Forge agree with the pinned game schemas on two rules, so push/261 and
push/262 pass without one-off exceptions:

1. **L06 / law 4:** `statTypes` is required only where the tag's schema has it (`damage`, `pierce`);
   `generalTypes` is still required on all three formula tags (`damage`, `pierce`, `wound`).
2. **Law 14 / L05:** `preferredStat` is no longer required or enumerated on an AI create.

## Source evidence (read, never run)

Pin `studie-tech/TheNinjaRPG@85cecaebf4ada2e265a18a1405f63c9637443275`, which is the pin of
`forge/src/runner/nested.json` and `fields.json` (`_meta.pin` / `_provenance.pin`) and the source drop of
`45c_DATA_constructors.json` / `45d` (`git:studie-tech/TheNinjaRPG@85cecaeb`).

| Claim | File:line at 85cecaeb |
|---|---|
| `IncludeGeneralsAndElements` = `generalTypes`, `elements` | `app/src/validators/combat.ts:151-154` |
| `IncludeStats` = `statTypes` + `...IncludeGeneralsAndElements` | `combat.ts:156-169` |
| `DamageTag` spreads `IncludeStats` | `combat.ts:544-546` |
| `PierceTag` spreads `IncludeStats` | `combat.ts:584-586` |
| `WoundTag` spreads only `IncludeGeneralsAndElements`; `calculation` is `percentage` only | `combat.ts:760-768` |
| `preferredStat` column dropped | `app/drizzle/migrations/0056_unified_combat_stats_masteries.sql:254` (`ALTER TABLE \`UserData\` DROP COLUMN \`preferredStat\``) |

The generated contracts say the same: `nested.json` effects `damage`/`pierce` key set 5 contains
`statTypes` and `generalTypes`, `wound` key set 2 contains `generalTypes` and no `statTypes`; 45c
`unions.AllTags` agrees field for field.

**Upstream main re-checked:** `studie-tech/TheNinjaRPG@e27cbebe3458daeca3cc651a41d331c22bb198ac`
(2026-10-25). The five schema blocks above are textually identical (line numbers shift: 152, 157, 546,
586, 771), and `app/drizzle/schema.ts` there has no `preferredStat`. Fetched with a blob-less git fetch;
nothing was executed.

## Changed

| Path | Change |
|---|---|
| `skills/building-tnr-content/scripts/validate.py` | `FORMULA_KEYS` + `load_formula_keys(ctors)` read each formula tag's statTypes/generalTypes from 45c `unions.AllTags` (a tag 45c does not define keeps both, the old rule); `formula_missing()` drives both law 4 (`check_laws`) and L06 (`lint_entries`). `LFORM` removed. `AI_CREATE_REQUIRED` drops `preferredStat`; `check_ai_create` no longer enum-checks it; unused `STAT_TYPES` removed. |
| `skills/building-tnr-content/scripts/selfcheck.py` | New `check_stale_rules`: 9 fixtures run `validate.py --strict` (wound generalTypes-only clean, with and without `calculation`; wound without generalTypes warns naming only generalTypes; damage/pierce without statTypes still warn and law-4 error; pierce without generalTypes warns; AI create without preferredStat clean; missing rank / preferredGeneral2 still error), plus a guard that 45c still matches the pinned Wound/Damage key sets. `_AI_REQ` fixture drops `preferredStat`. |
| `forge/src/runner/lints.mjs` | L06 reads the per-tag key set from `nested.json` (`l06(t)`); a tag the table does not define keeps both keys. Stale `preferredStat` comment corrected (the key is refused, not accepted, since the re-pin). |
| `forge/test/l06_per_tag.test.mjs` | New, 6 tests: pinned key sets, wound clean, wound without generalTypes, damage/pierce per key (absent and empty), Forge's key check still refuses `statTypes` on a wound, push/261 carries no L06. |
| `forge/package.json`, `forge/src/main.mjs` | 0.9.0 -> 0.9.1 (`VERSION` was still `forge 0.8.1`; synced, same byte length). |
| `forge_bundle.js` | Rebuilt by `npm run build`. Only change besides the banner: `nested_default` moves up to the lints module (esbuild dedupe) and the L06 lines. |
| `forge_loader_user.js` | `@x-release-pending 0.9.1` added; `@version` / `@require` keep the last release (0.9.0 @ 4a3b7fb) for `release_pin.yml` to promote. |
| `docs/ENGINE_LAWS.md` | Laws 4 and 14 `[CORRECTED 2026-10-26, source-verified]` with source citations and the superseded text kept inline (law-reconciliation pattern of law 16c). |
| `references/ai.md`, `references/pipeline.md` | Hand-kept verbatim copies of laws 14 and 4 replaced with the new text; ai.md §8 checklist no longer lists `preferredStat`. |
| `references/jutsu.md` §2.1b | Restatement of law 4 made per tag, citing law 4. |
| `12b_LAWS_coverage.md` | Rows 4 and 14 marked corrected 2026-10-26. |
| `packs/*.md`, `references/_toc/*.json` | Re-rendered by `build_packs.py --write` (never hand-edited). |
| `dist/building-tnr-content.zip` | Rebuilt by `.github/scripts/pack_skills.py`; deterministic across two runs; packaged changed files byte-identical to sources. |

## Not done / out of scope

- No other lint, law, content manifest, or exception ledger was edited. `fable/forge-suggest-create` and
  the dungeon branch were not touched.
- `builder_bundle.js` (the legacy builder, line 645) still lists `preferredStat` in its own L05. The brief
  scopes validate.py and Forge only; left as debt.
- `45h_DATA_lints.json` has no L05/L06 entries, so there was nothing to change there.

## Verification (Node v24.22.1, full history: `git rev-parse --is-shallow-repository` = false)

Run on the rebased code head 79e8fad8. Exit codes captured directly with `$?` / `${PIPESTATUS[0]}`, not
masked by a pipe.

| Command | Result |
|---|---|
| `cd forge && npm ci` | ok |
| `npm test` | exit 0; tests 723, pass 718, fail 0, cancelled 0, skipped 5 (baseline on main: 717 / 712 / 0 / 5; +6 new) |
| `node --test test/l06_per_tag.test.mjs test/post0056.test.mjs test/adversarial.test.mjs` | 91/91 pass |
| `npm run build && git diff --quiet -- ../forge_bundle.js` | build exit 0, diff exit 0 (committed bundle reproduces) |
| `node tools/check_bundle_budget.mjs` | exit 0; raw 434,970 / 435,000, gzip 104,667 / 105,000 (main: 434,875 / 104,978) |
| `node tools/check_release_pin.mjs` | exit 0, "release pin ok" |
| `npm run fixtures` + `git diff --exit-code -- test/fixtures/envelope test/fixtures/screens` | exit 0 / exit 0 |
| `node tools/check_imports.mjs`, `node tools/check_boundaries.mjs` | 0 violations each |
| `npm audit --omit=dev --audit-level=high` | exit 0 |
| `cd skills/building-tnr-content/data && python3 ../scripts/selfcheck.py` | exit 0, 0 errors; "stale rules: 9 law 4/L06 and law 14 fixtures agree with the pinned schemas" |
| same selfcheck with main's `validate.py` swapped in | exit 1, 10 errors: the new fixtures fail on the old rules |
| `python3 ../scripts/validate.py --strict ../../../push/261_lastlight_jutsu_create.json` | exit 0, 0 errors, 0 warnings |
| `python3 ../scripts/validate.py --strict ../../../push/262_foundry_warden_create.json` | exit 0, 0 errors, 0 warnings |
| `validate.py --strict` on all 119 `push/*.json`, main vs branch | Only removals: 261 (L06 wound), 262 and the historical push/90 Sealwright line (law 14 preferredStat). No diagnostic added anywhere. (122/123 also differed, an artefact of running main's copy from a scratch directory where its Bloodright bridge path does not resolve.) |
| `python3 skills/building-tnr-content/scripts/doctrinemap.py .` | exit 0; 21 assertions, 0 errors, 0 warnings |
| `python3 skills/building-tnr-content/scripts/render_doctrine.py --check` | exit 0, all projections current |
| `python3 skills/building-tnr-content/scripts/build_packs.py --check` | exit 0, all packs and TOCs current |
| `python3 skills/building-tnr-content/scripts/lawmap.py .` | exit 0; 93 laws, 93 rows, 79 citations, 0 errors, 5 pre-existing warnings (16d, 18, 37, 61, 69). Main: 77 citations; +2 are the new law 4 / law 14 citations in selfcheck.py. |
| `python3 skills/building-tnr-content/scripts/catalog_sync.py --selftest` | OK |
| `python3 .github/scripts/pack_skills.py` twice + `sha256sum -c` | exit 0, both zips identical across runs; tree clean afterwards |

## Exceptions voided (ledgers not edited)

| Command | Result |
|---|---|
| `python3 scripts/validate_exception.py state/validate_exceptions/261_lastlight_jutsu.json` | exit 1, `VOID: diagnostics differ from the approved set` (found `[]`) |
| `python3 scripts/validate_exception.py state/validate_exceptions/262_foundry_warden.json` | exit 1, `VOID: diagnostics differ from the approved set` (found `[]`) |

Both ledgers are void by their own terms (RUL-2026-10-25-008 / -009): the manifests now pass
`validate.py --strict` with 0 diagnostics, so no exception is needed. Retiring or archiving the
ledgers is a separate Lane B step after integration. The push/90 release ledger
(`state/ghost_ship_skyglass_release_validate_exception.json`) pins validate.py by hash and was already
void before this branch; it is historical and untouched.

## Known debt / deviations / attack points

1. **Law 4 changed as well as L06.** The brief scopes "any L06 wording that names `wound` + `statTypes`".
   L06 is the lint form of law 4, whose text named `wound` among the tags needing both keys, and
   validate.py's law-4 check (`check_laws`) fired on a wound with no `calculation` key because it
   defaulted `calculation` to `formula` (wound's only value is `percentage`). I treated law 4 as in
   scope and made its check per tag too. The `calculation` default itself was left alone; with the
   per-tag keys a generalTypes-only wound passes either way. Reviewer: confirm this reading.
2. **Forge `VERSION` sync.** `src/main.mjs` said `forge 0.8.1` at package 0.9.0 (missed in the 0.9.0
   release). Bumped to `forge 0.9.1` with the package. Same byte length.
3. **Budget headroom is 30 raw bytes / 333 gzip bytes.** The next Forge change will need a budget
   decision (director-owned).
4. **validate.py and Forge differ on one value check, unchanged here:** validate.py treats a non-empty
   non-list value (e.g. the string `"Highest"`) as present; Forge requires an array. Pre-existing.
5. **Legacy `builder_bundle.js` L05** still demands `preferredStat` (out of scope).
6. **Message text changed.** L06 now names only the missing keys (`L06 wound missing generalTypes (...)`);
   law 4 names the tag's own keys. Anything grepping the old full string would need updating; the repo
   has none besides the two voided ledgers.

## Open user decisions

None for this change. Integration, and retiring the two voided ledgers, are the director's call.

## Live-game statement

- Live-game requests: **0**. Game writes: **0**. Credentials or session material: **none**.
- Game source was fetched from GitHub (`studie-tech/TheNinjaRPG`, blob-less fetch of two commits) and read
  only; nothing in it was executed.
- Not performed: any browser, userscript, ViolentMonkey or live-session check of Forge 0.9.1. The bundle
  is verified by the test suite and the reproducible build only.

## Copy-ready ChatGPT review prompt

```text
You are the independent reviewer for perseverance484/tnr-tools (Lane A, docs/DEVELOPMENT_WORKFLOW.md,
docs/workflows/FABLE_REVIEW.md). Do not modify branch fable/validate-stale-rules.

Review target: the tip of fable/validate-stale-rules. Its parent is the code commit
79e8fad82c5c780a7ff8c77436bc17dbbb9639f7; the tip only adds docs/handoffs/VALIDATE_STALE_RULES_HANDOFF.md.
Base: main @ 6d4de246da3fb72b331b357b05040f44de42082b.
Contract: state/prompt_validate_stale_rules.md (RUL-2026-10-25-009, context RUL-2026-10-25-008).
Handoff: docs/handoffs/VALIDATE_STALE_RULES_HANDOFF.md.

Check, against the pinned game source studie-tech/TheNinjaRPG@85cecaebf4ada2e265a18a1405f63c9637443275
(read only, do not run it; zero live-game requests):
1. validate.py (formula_missing / load_formula_keys, check_laws law 4, lint_entries L06, check_ai_create)
   and forge/src/runner/lints.mjs L06 agree per tag with combat.ts DamageTag/PierceTag/WoundTag
   (lines cited in the handoff), and with each other. Look for a tag, key or empty-value case where
   they disagree, and for any manifest the new rules wrongly let through.
2. Law 14 no longer requires or enum-checks preferredStat, and rank/regeneration/preferredGeneral1/2
   are still enforced on both surfaces.
3. Law-reconciliation (RUL-2026-09-08-004, CLAUDE.md section 7): docs/ENGINE_LAWS.md laws 4 and 14 are
   the owner edits; references/ai.md, pipeline.md, jutsu.md and 12b are hand-kept copies; packs and
   _toc were re-rendered with build_packs.py, not hand-edited. Is anything restated that should cite?
4. Handoff deviation 1: law 4 (not only L06) was treated as in scope. Is that the right reading?
5. Tests: selfcheck.py check_stale_rules and forge/test/l06_per_tag.test.mjs actually fail on the old
   rules (the handoff claims 10 selfcheck errors with main's validate.py).
6. Forge release staging: version 0.9.1, rebuilt bundle reproducible, budget (30 raw bytes headroom),
   @x-release-pending 0.9.1 with @version/@require left at the 0.9.0 release.
7. Re-run if you can: forge `npm ci && npm test` (Node 24, full history), `npm run build && git diff
   --quiet -- ../forge_bundle.js`, tools/check_bundle_budget.mjs, tools/check_release_pin.mjs;
   selfcheck.py and validate.py --strict on push/261 and push/262 from skills/building-tnr-content/data;
   doctrinemap.py, render_doctrine.py --check, build_packs.py --check, lawmap.py.

Return: PASS / PASS WITH NOTES / FAIL, findings ranked by severity with file:line, and for each finding
whether it blocks integration.
```
