# AI rules may fire the engine's basic attack: Forge kit lint and validate.py exception at TheNinjaRPG@3314d122 — 2026-10-31

**Lane:** A (Forge pre-send lint + container validator). **Approval:** director 2026-10-31, "Do an exception for basic attack for now"; bundle budget raise authorised in advance by RUL-2026-10-31-066 item 2 ("the exact figure is set by that change's measured size, as RUL-2026-10-28-014 did").
**Repository:** `perseverance484/tnr-tools`. **Branch:** `fable/forge-basic-attack-rule`, cut from `main@2490b51107c2aea5e3181fa1a1e18448497ea8ed` (Forge 0.12.2 released: loader `@version 0.12.2`, `@require` pinned to `b3344635`). The frozen head is reported with the push; this file is the handoff for it. Integration target: `main`.
**Game source:** `studie-tech/TheNinjaRPG@3314d122c93e036618483d18229a793ad7ad21fd` (the current contract pin), read only through `git show 3314d122:<path>`, never executed.
**Live requests / writes:** 0 / 0. **Credentials:** none. `state/` and `docs/RULINGS.md` untouched.

## Objective

Since the Skyglass fallback fix (RUL-2026-10-30-060), every enemy's last rule names the engine's basic attack (`use_specific_jutsu`, `jutsuId: "basicAttack"`). Forge's `kitProblems` and `validate.py check_pool_kit` refused such a rule ("fires "basicAttack" but that jutsu is NOT in the AI's jutsus array") and Forge refused the whole manifest. This blocked 35 push/344 copies (push/README.md 344, `_blocked_forge_kit_lint`). This change accepts that one rule shape and keeps every other check as it was.

## Source audit (3314d122)

| Fact | Where |
|---|---|
| `use_specific_jutsu` resolves `rule.action.jutsuId` with `availActions.find((a) => a.id === rule.action.jutsuId)`: the AI's **available actions**, not its `jutsus` array | `app/src/libs/combat/ai_v2.ts` ~494-500 |
| `availActions` = `availableUserActions(nextBattle, user.userId, true, true)`, filtered by pool cost, castability and AP | `ai_v2.ts` ~139-161 |
| `availableUserActions` always includes `basicActions.basicAttack` when `basicMoves && !isStealth` (students included) | `app/src/libs/combat/actions.ts` ~146 |
| The basic attack's id is exactly `"basicAttack"` (range 1, 10 stamina, 20% AP, `DamageTag` power 10) | `actions.ts` ~512-540, `getDefaultBasicActions` |
| The server's rule schema takes any string `jutsuId`; `ai.updateAiProfile` checks only the rule cap and move/summon effects of the listed jutsu/items | `app/src/validators/ai.ts` ~195; `app/src/server/api/routers/ai.ts` ~70-105 |

**Other engine basic actions.** The same lookup also resolves `move`, `meditate`, `basicHeal`, `clear`, `cleanse`, `offensiveStance`, `defensiveStance`, `replacementTechnique` and `flee` (`actions.ts` ~543-737, gated at ~146-162), and `wait` (~166). The source proves they would resolve, but the director's exception is the basic attack only, so they are **not** exempted. They are still refused as unequipped. Widening the exception is a director decision (see open decisions).

## What changed

- `forge/src/runner/pool.mjs` `kitProblems`: a rule is exempt from the "not in the jutsus array" error only when `action.type === "use_specific_jutsu"` and `action.jutsuId === "basicAttack"` exactly (module-private constant `ENGINE_BASIC_ATTACK_ID`, with source citations). Nothing else changed. The law 40 gate check still runs only for pool records (`POOL_BY_ID`); `basicAttack` is not a pool record, so it gets no gate arithmetic, as before.
- `skills/building-tnr-content/scripts/validate.py` `check_pool_kit`: the same exception (`ENGINE_BASIC_ATTACK_ID`).
- `forge/package.json`, `forge/src/main.mjs`: 0.12.2 → **0.12.3**. `forge_bundle.js` rebuilt. `forge_loader_user.js` gains only `// @x-release-pending 0.12.3`; it keeps the released `@version 0.12.2` and the `@require` pin `b3344635`.
- `forge/tools/check_bundle_budget.mjs`: budget **466,000 / 112,000 → 470,000 / 113,000** (raw / gzip), with a history line.
- Docs: `docs/BUILDER_APP_NOTES.md` gets a 0.12.3 section, and its 0.3-era kit-integrity bullet now notes the exemption. `skills/building-tnr-content/references/ai.md` gets an author note in the rule-vocabulary section. `packs/ai-build.md` and `references/_toc/ai.json` were re-rendered by `build_packs.py --write` (hash stamps only). No law text stated the old rule: laws 18, 39, 40 and 41 are unchanged, and no doctrine projection was touched.
- Tests (socket-free):
  - `forge/test/adversarial.test.mjs` **K3b**: a basic-attack rule (no gate and gate 2) beside an equipped pool rule parses. An unequipped pool jutsu beside it is still refused. `basicattack`, `basicHeal`, `move`, and `basicAttack` under `use_highest_power_jutsu` are still refused. A pool gate at range is still refused (law 40).
  - New `scripts/test_pool_kit.py` (4 tests): the same cases against `check_pool_kit` with the committed `32b_DATA_pool.json`.
  - Mutation check: with the two source edits reverted, K3b fails, as do 2 of the 4 Python tests (the other two assert behaviour that should not change).

## Bundle budget (for the director's ruling record, RUL-2026-10-31-066 item 2)

| | raw | gzip |
|---|---|---|
| Base `2490b511` (0.12.2) | 465,508 | 111,989 |
| Head (0.12.3) | **465,670** | **112,059** |
| Delta | +162 | +70 |
| Old budget | 466,000 | 112,000 (head was 59 over) |
| **New budget** | **470,000** | **113,000** |
| Headroom at head | 4,330 (99.1%) | 941 (99.2%) |

The margin follows the RUL-2026-10-29-054 step (about +4,200 raw / +1,000 gzip over measured).

## Gates (exact; exit codes not masked)

| Gate | Result |
|---|---|
| `npm test` (forge/) | exit 1: 787 tests, 771 pass, **1 fail (pre-existing)**, 15 skipped (checkout-gated). The failure is `runner.test.mjs` "compatibility: staged manifests parse, plan and pass Forge pre-send validation": `push/337_voth_scale_to_player.json` `@ai:pz_boss is unknown` (Lane B, debt as in the 0.12.2 handoff). Base: `forge/src` and `forge/test` are unchanged between `a65bd23b` (the 0.12.2 handoff, 786 tests, the same single failure) and this base, so the +1 is K3b. The base suite was not re-run in this session. |
| `node --test --test-name-pattern=K3 test/adversarial.test.mjs` | exit 0, 2/2 |
| `npm run build` ×3 (twice in the shared checkout, once in a clean worktree) | exit 0, byte-identical, sha256 `b77bd07a0260334275a5d02d2b12ac63cd26540dcd0e4240f2f10a298b29d791` (matches the committed bundle) |
| `npm run fixtures` | exit 0. In the review worktree, 5 envelope fixtures differed only in the absolute `node_modules` path inside recorded stack traces: the worktree's `node_modules` is a symlink to another directory, so `derive_envelope` did not normalise it. This is an environment artifact and was reverted, not committed. The fixture producers do not read `pool.mjs`. |
| `node tools/check_bundle_budget.mjs` | exit 0: raw 465,670 / 470,000, gzip 112,059 / 113,000 (before the raise: exit 1, gzip 59 over) |
| `node tools/check_boundaries.mjs` | exit 0: 0 violations (49 + 13 modules; pin 3314d122) |
| `node tools/check_imports.mjs` | exit 0: 0 violations |
| `node tools/check_release_pin.mjs` | exit 0: release pin ok |
| `check_manifest.mjs`, `validate.py`, `validate.py --strict` (cwd skill `data/`) on all 137 `push/*.json`, base tree vs head tree | full output and every exit code **identical** (after normalising the root path). 7 pre-existing `check_manifest` refusals (122, 123, 337, 47, 56, 61, 62); 6 `validate.py` / 20 `--strict` non-zero, same on both. No committed manifest uses `basicAttack`. |
| Same two tools on `push/skyglass_copies.gen.py --blocked` output (`344_skyglass_copies_3.json`, generated at base into scratch, **not committed**) | base: check_manifest exit 1, 41 basicAttack + 146 gate problems; validate.py exit 1, 225 errors / 7 warnings. Head: check_manifest exit 1, **0** basicAttack + 146 gate problems; validate.py exit 1, **184** errors / 7 warnings. Everything except the 41 removed lines and the totals is identical. |
| `python3 -m unittest scripts/test_pool_kit.py scripts/test_pet_species.py scripts/test_schema_diff.py scripts/test_catalog_checks.py scripts/test_variant_checks.py scripts/test_skyglass_check.py` | exit 0, 91 OK |
| `selfcheck.py --generated .` (cwd `data/`) | exit 0, 0 errors |
| `doctrinemap.py .` | exit 0: 21 assertions, 0 errors, 0 warnings |
| `render_doctrine.py --check` | exit 0: all projections current |
| `build_packs.py --check` (after `--write`) | exit 0: all packs and TOCs current |
| `lawmap.py .` | exit 0: 93 laws, 80 citations / 42 files, 0 errors, 5 pre-existing warnings (16d, 18, 37, 61, 69). Identical on `main`. |

## Known debt, deviations, open decisions

1. **push/344 part 3 stays blocked.** All 35 copies still trip the law 40 gate check (146 gates written at range, not range+1). That gate is deliberately unchanged here. Unblocking them needs the content to move each gate to range+1, or a separate director decision.
2. **`push/skyglass_copies.gen.py` carries its own port of `kitProblems`** (`forge_kit_problems`), which still counts `basicAttack` as a problem. That is Lane B content tooling and was not touched. Its partition labels are now stale for basic-attack rules, but the partition itself does not change, because every held copy also has gate problems. Update it in the next Lane B pass.
3. **No ruling entry for the exception.** The director's 2026-10-31 "Do an exception for basic attack for now" is not in `docs/RULINGS.md`, and the new budget figures need recording against RUL-2026-10-31-066 item 2. Proposed text for the director's record: *"Forge 0.12.3 / validate.py accept `use_specific_jutsu` `jutsuId: "basicAttack"` without the jutsu in the AI's kit (engine basic attack; theninjarpg@3314d122 ai_v2.ts ~494, actions.ts ~513/~146); other engine basic actions are not exempted. Bundle budget 466,000/112,000 → 470,000/113,000, measured 465,670/112,059."*
4. **Open (director):** whether the exception should widen to the other source-proven engine actions (`move`, `meditate`, `basicHeal`, `clear`, `cleanse`, stances, `replacementTechnique`, `flee`, `wait`). It was not done here.
5. Unavailable-when-stealthed: a basic-attack rule does nothing while its AI is stealthed (`actions.ts` ~146) and falls through to the next rule, like any unaffordable action. This is engine behaviour and is not linted.

## Attack especially hard

- That `"basicAttack"` is the exact and only id the engine accepts for the basic attack, and that `use_specific_jutsu` is the only action type that resolves it by `jutsuId` (`use_combo_action` uses `comboIds`, a different key, and is not affected by this lint).
- That the exception cannot hide an unequipped real jutsu: it is an exact string match on an id that is not nanoid-shaped, and the action type is checked too.
- That no other check moved: the push-sweep identity, and the 344 part-3 delta being exactly the 41 basicAttack lines.

## Not done / not begun

No browser, live or session checks. No Forge release (`release_pin.yml` promotes 0.12.3 after merge). push/344 part 3 was not regenerated, edited or committed. No content manifest, `state/`, or `docs/RULINGS.md` edits.
