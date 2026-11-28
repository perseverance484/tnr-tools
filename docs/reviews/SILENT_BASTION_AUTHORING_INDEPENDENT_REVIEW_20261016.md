# Silent Bastion full authoring — independent frozen-SHA review

**CURRENT VERDICT (AMENDED 2026-10-16): REVISIONS REQUESTED for F2–F4; F1 is CLOSED by director ruling RUL-2026-10-16-013.** The offline content/evidence is substantially sound, but the generator fail-open, validator diagnostic robustness and small proofreading corrections still need work before final acceptance. F5 remains a distinct pre-manifest AI loadout/calibration gate. The Fable implementation branch and its tested artifacts remain frozen and unmodified; the existing historical review findings below are retained for audit traceability.

## Director follow-up — F1 CLOSED (RUL-2026-10-16-013)

The director **approved all presently compiled Extermination Order combat stats** at frozen implementation `16dbc5a2976a463be1f9506e007f10bd0814e85d`: **60 AP, range 5, 80 damage, Elemental Seal power 100 for 2 rounds, Cleanse Prevent power 100 for 2 rounds**, plus the **cooldown 4** and **Extermination Order** name previously approved. It remains an **active-Final-Stand-only** technique. The engine's `has_effect` stale-tag hazard and the previously accepted cooldown-4 residual risk remain explicitly known, not newly resolved by this ruling.

The director also approved the **Solar Bow in HAND_1 and Crossbow in HAND_2** as Arakane's two equipped supporting weapons, together with his previously approved Countermand. The only remaining source requirement for those two existing weapons is to obtain **fresh, authorized records/captures** and validate IDs/current values/slot behavior before a manifest. A capture discrepancy must be surfaced, not silently "corrected" by equipment substitution.

**F1 is no longer an open director decision or reason to reject these drafted values.** Fable should update the original `commanders.json`, Arakane design profile, decision docket and regenerated approval metadata **on its own authoring branch**, preserving source/capture requirements. We have **not** edited Fable's implementation. The remaining correction instructions are F2 (fail-open generator runner), F3 (validator diagnostic multiplicity/status), and F4 (single missing quotation mark and pool-reset timing wording). F5 (full AI assembled loadout/real battle, calibration, source reads) remains a pre-manifest gate, not an additional boss design decision.

## Scope and refs

| Field | Value |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Fable authoring branch (not modified) | `claude/silent-bastion-authoring-69za5u` |
| **Exact frozen target** | `16dbc5a2976a463be1f9506e007f10bd0814e85d` |
| Base and base merge-base | `25d2b2e159d9fb9b0769db5483571e0db87991f6` (target ahead by 4 commits) |
| Main at review | `99e86dc549b86f1f4a5846c0e509fa6bc15b3463` |
| Target/main merge-base | `057acddb986b50e486ccf550fac00b68fff51490` (diverged; no merge requested) |
| Frozen independent reward companion | `claude/recipe-cache-native-proof-69za5u@b133d73286df9e48ba1015b21dd694c69c9ea090` (unchanged; its independent review is a **separate** gate) |
| **Pinned native engine used by Fable** | `studie-tech/TheNinjaRPG@0651b039a466516a8fe24fc13b56f60dea11b7eb` |
| Later game source seen | `studie-tech/TheNinjaRPG@94f9d84c770004172ba423ada3d6710849acc451`, 13 commits ahead of test pin; related changes include `app/drizzle/constants.ts` and `app/src/validators/combat.ts` |
| Primary plan | `state/prompt_silent_bastion_complete_authoring.md` |
| Evidence | `docs/reviews/SILENT_BASTION_AUTHORING_OFFLINE_RESULTS.md`; `harness/silent_bastion_authoring/results/` |
| Review owner | ChatGPT, Engineering Auditor (support: Content Designer) |

Authority reconstructed from live main/project state, `docs/00_INDEX.md`, `docs/DOCTRINE.md`, `docs/ENGINE_LAWS.md`, `docs/RULINGS.md`, `CHATGPT.md`, `CLAUDE.md`, `docs/DEVELOPMENT_WORKFLOW.md`, `docs/agents/README.md`, `docs/workflows/FABLE_REVIEW.md`, relevant TNR content references, design lock and committed authoring outputs/harness; pinned game source for the tested contracts. Director rulings RUL-2026-10-16-004 through -012 are present at the frozen target, but **do not convert still-labelled CANDIDATE values into approved choices**.

## Findings, ordered by consequence

### F1 — HISTORICAL AT FROZEN AUDIT HEAD; DIRECTOR VALUES NOW APPROVED (CLOSED under RUL-2026-10-16-013)

**Historical finding below records the frozen audit snapshot BEFORE the director approved these exact stats and weapon selections. Current disposition: CLOSED by RUL-2026-10-16-013.**

**Invariant:** All unapproved boss mechanics that affect battle balance must remain visible as operator-owned decisions. The authoring report asserts every design/balance choice raised was ruled; the final docket section A lists only cache names, cache/Beacon rarity, cache descriptions, and art.

**Source conflict:** `docs/RULINGS.md` **RUL-2026-10-16-011** expressly states: **"Extermination Order's AP, range and effect powers remain candidates."** The authored `state/silent_bastion_authoring/design/commanders.json` nevertheless selects **60 AP / range 5 / Elemental Seal 100 / Cleanse Prevent 100**, removes the `candidate` notes when compiling jutsu tags, and the final `decision_docket.md` fails to list these three outstanding approval areas. `RUL-2026-10-16-004` accepts the ultimate **cooldown 4 only** (and residual stale-effect risk), not all other fields.

A second unratified equipment selection: the prescribed **Solar Bow + Crossbow** Arakane Stealth fallback appears in the compiled boss items. `state/silent_bastion_arakane_ai_profile.md` and the accepted coordination lock distinguish these **specific two weapons as proposals**, not finally selected equipment; `RUL-2026-10-16-011` approves **Countermand's** item fields, not those two weapon choices. The docket relegates Solar Bow/Crossbow exclusively to "fresh reads (not design decisions)." A fresh record check does not itself approve equipping those weapons.

**Consequence:** A builder could ship unapproved AP/range/proc and weapon choices, believing the docket's "every decision ruled" statement. This is user-authority drift even though these fields validate mechanically.

**Minimum correction:** Update `decision_docket.md`, authoring report, and affected generated candidate/provenance status so **ultimate AP60, range5, Elemental Seal100, Cleanse Prevent100, and selection of Solar Bow/Crossbow are explicitly CANDIDATE / DIRECTOR APPROVAL REQUIRED**. Preserve approved name, damage80, final-phase restriction and cooldown4. Either obtain explicit director decisions before production or keep these fields as explicitly unresolved candidates; do not silently ratify them. Revisit other `candidate` flags before declaring all final decisions closed. No new boss-kit brainstorming requested.

### F2 — GENERATOR PRECHECK CAN RETURN GREEN AFTER AN EARLIER GENERATOR FAILS (P1 runner correction)

**Exact site:** `harness/silent_bastion_authoring/run.sh`, section 2, `set +e`; five `python3 ... --check` commands in one `{ ... }` group followed by `|| GEN_STATUS=1`; only the **last** command's exit status controls the group. A separate grep catches the literal word `STALE`, but does **not** catch other errors such as `compose: script ids differ from graph`, JSON errors, missing captures, or Python exceptions from earlier commands.

**Independent reproduction of its Bash control flow**, without the game or any repo mutation:

```bash
set +e
GEN_STATUS=0
{ false; true; } >/dev/null 2>&1 || GEN_STATUS=1
printf '%s\n' "$GEN_STATUS"     # observed 0 despite an earlier failure
```

**Consequence:** With pre-existing compiled outputs, a failed source-extraction or composer integrity check can be hidden by the successful final `derive_alternatives.py --check`. Subsequent validators can then test **stale compiled artifacts** while the run reports `generators=0`. This is a real provenance/fail-closed defect, not a hypothetical syntax complaint.

**Minimum correction:** Run each check with an explicit `|| GEN_STATUS=1`, or execute the group in a `set -e` subshell and preserve its exit status, with a targeted negative test that makes the *first, middle and last* generator fail independently. Then re-run the full authoring harness and freeze a new SHA. **This does not invalidate the currently committed success evidence**, whose generator log explicitly shows all five commands as current; it invalidates the guarantee that the runner *would catch future drift*.

### F3 — VALIDATOR EXCEPTION CHECK DOES NOT COMPARE MULTIPLICITY OR PROCESS STATUS (P2 hardening; release remains blocked)

**Exact site:** `harness/silent_bastion_authoring/tools/check_validate.py`:

```python
got, want = set(errors), set(EXPECTED)
return 1 if unexpected or vanished else 0
```

This set equality checks distinct normalized error strings only. **Duplicate occurrences are discarded**, the parsed "11 errors, 9 warnings" summary is not compared to the expected cardinality, and `validate.py`'s exit status is not tested. If one previously approved error appears multiple times, the gate can still return green. The normalizer also truncates any changed `. Valid:` field diagnostics, making the check less specific. This is manageable but not the exact "11/11" diagnostic-set lock the report suggests.

**Current evidence is NOT zero-error validation:** committed `validate_py.txt` records **11 errors, 9 warnings**. The 11 correspond to 2 exclusive two-phase refs, 4 director-excepted puzzle shared targets, 1 stale item Clear lint (VAL1) and 4 stale Weighted Cache fields (VAL2). The engine-native fixtures support the latter two as contract/source mismatches at the pin, and the puzzle routing was approved under RUL-012. The exact **11 distinct diagnostic types are documented**; nevertheless **no production manifest may be described as `validate.py` clean**.

**Minimum correction:** Compare `Counter(errors)` rather than `set(errors)`, assert count equals 11, assert the validator process returned its expected nonzero exit (and wasn't killed), and keep the explicit exception rationale. Follow the separate Lane A VAL1/VAL2 fix or sanctioned source-aware exception process before any live-selectable manifest. Do **not** weaken the repository validator globally or use `skipPreflight`.

### F4 — APPROVED QUEST COPY HAS AN UNTERMINATED QUOTATION AND MISSTATES RESET TIMING (P2 narrow editorial correction)

**Specific reproducible copy defect:** `state/silent_bastion_authoring/design/script.json`, `d3.n.boss.alert` ends:

```text
He smiles. "Neither will you leave.
```

The closing `"` is missing. Independent scan of the **99 objective texts** found this as the only text containing an odd number of ASCII quotation marks. This copy is generated from `tools/gen_script.py` and then included in the compiled quest. The director's general approval of the draft story (RUL-011) does not require preserving an evident punctuation mistake.

**Timing mismatch:** Multiple defeat dialogs, e.g. `d2.lost_first` ("Your pools have been set to half") and `d3.lost_first` ("You wake ... with your pools at half"), describe the player already at 50% **before starting** the recovery fight. The native C99 settlement explicitly leaves the player at **1 HP** between defeat and the next recovery battle; **`givePools:50` is applied only when the player starts that recovery fight**. Player-facing inventory/profile resources would therefore disagree with the text while on the defeat dialog. Equivalent phrasing appears in each division.

**Minimum correction:** Add the missing closing quote at the owning `gen_script.py` source. Change only the defeat lines to a truthful future-action description (e.g., "Your next trial begins with half your pools"), without changing the approved story, difficulty, graph, effects or player choices. Regenerate `script.json`, quest candidate, story script and test evidence. Treat substantive wording changes as director-owned; this is a targeted proofreading/accuracy fix.

### F5 — FULL AI LOADOUT/PROFILE ATTACHMENT AND COMBAT DIFFICULTY NOT END-TO-END PROVEN (release gate, not authoring failure)

**Verified evidence:** Gate A uses a **synthetic battle state** populated with the captured jutsus, Countermand and seed weapons, equipped appropriately, and a bespoke profile object. It checks real `performAIaction` and `alignBattle` behavior, including combos, Copy/Clear, shield response and Stealth, against a **passive player**. Gate C creates test user rows, inserts profile rows directly, then checks 20 `ai.updateAiProfile` saves and rejects a 21-rule control. D/R/E execute the compiled 99-node quest **with placeholder/default fixture AIs and imposed combat outcomes**, not the 20 authored AI opponents fighting actual archetypes.

**Not proven by that composition:** the complete native AI **creation/edit of item+jutsu membership**, correct item slot/quantity and weapon eligibility, attachment of `aiProfileId` to every newly created AI, and one actual quest battle started from those authored records exercising Arakane's Countermand and both weapons. At the pinned game source, `profile.updateAi` calls `updateUserContent`; `applyUserContentChanges` creates new AI items as `equipped:"CHEST"` (`app/src/server/api/routers/profile.ts:3107–3117`), whereas the synthetic combat fixture equips Countermand in `ITEM_1` and bows in `HAND_1/HAND_2`. `getAvailableActions` mainly tests `equipped !== "NONE"`, so this **is not proof of failure**, but exact live loadout behavior cannot be inferred solely from the synthetic fixture.

**Minimum follow-up before a live manifest:** make a separate small **offline editor/create→profile attach→combat-start** native fixture using the proposed Arakane loadout and at least one regular; verify real gear rows, their usable battle actions and the attached rules. Separately perform the user-required calibration fight and multi-archetype battle/damage tuning. If Fable's remaining work intentionally excludes these until fresh record capture/creation, preserve the explicit **release BLOCKED** status rather than claiming a real populated-AI encounter passed.

## Verified sound components (independently checked)

- **Graph:** The frozen `alt99_f4gate` graph is still the selected source, not the broken C1 candidate. Quest composer checks the graph's SHA-256 and exact node IDs. Native evidence plus independently inspected compiled quest show **99 objectives** (45 dialogs, 40 battle nodes, 12 resets, win and fail), four divisions, 16 regular identities + four commanders, 625 success paths and 16–20 fights, with confirmation dialog before recovery reset and direct terminal→optional REG4 gating.
- **Jutsu membership and priority:** Four commander memberships retain 10/11/12/14 equipped jutsu positions, 47 total (some reused across commanders); native rule counts 13/14/15/20, `includeDefaultRules:false`, all with unconditional final `end_turn`. Master/Replicant/Grand Marshal rules cite the preauthored roster; Arakane's ordered 20 cite his approved candidate profile. No intentional redesign seen. Signature and active-effect tests cover RUL-004's cooldown4 residual-risk compromise; do not overstate it as mathematically airtight Final Stand gating.
- **Protocols/Beacon/economy:** Quest protocol records give Medical **100%** at boss start; Combat buffs and Security Alert target the player; D5 Debuff Prevent100/3r per RUL-008. All eight recovery fights explicitly set `scaleGains:0`; no first-pass battle gets that override. Native evidence I checks recovery income 0 vs positive first-pass XP. Beacon charged once at `startQuest`, never refunded/charged on division retry.
- **Cache math independent recomputation:** Two cache records, one roll, 5,000/5,000 EPIC/LEGENDARY; each of eight selected recipes has exactly **one** matching tier entry with **every** required ingredient ID and integer quantity, EPIC = `quantityFull` and LEGENDARY = `quantityFull×2/5`. Arsenal: 50/50/20/20 unit bundles → weighted expected **35** units/open. Research: 20/40/40/16 → **24⅔** units/open. No hidden duplicate/missing ingredient set in the committed compiled cache. This is math/source-snapshot parity, **not** current live recipe validation or economic approval of demand.
- **Quest reward placement:** quest `content.rewardMode:"choose"`, pick1; exactly two distinct cache item cards under quest-level `content.reward.reward_items`, zero objective-level cache grants; no extra objective. Separate frozen reward-branch report supports native one-of-two claims and idempotent Weighted Cache consume, but that companion still needs its own independent frozen-SHA review.
- **Reproducibility evidence:** inspected committed `generators_check.log` (all five `current`), `validate_py.txt`, preflight `117/117`, Gate A `218/0`, C `44/0`, compiled runtime D `543/0`, R `7033/0`, E `592/0`, I `456/0`. Two Fable runs reportedly produced seven byte-identical evidence JSONs. These are valid **committed result reports**, not independently rerun native database tests.
- **Safety and scope:** no `push/` manifest, game-engine edit, live requests/writes, credentials, asset binaries, hidden publication or main merge. 16 regular enemy designs and all 99 objective texts exist. Exactly source-locked supplied recipe pool used. Main integration conflict for duplicated `RUL-2026-10-14-001` remains explicitly noted, not overwritten.

## Verification performed, limits and required next step

**Reviewer-executed:** exact ref and merge-base verification; complete primary report, generated design/script/economy, compiler, code, tests and evidence source inspection; independent JSON recipe-ID/quantity calculation and weighted expected-value arithmetic; comparison of commander native DSL vs existing roster; pinpointed punctuation and pool-dialog mismatch; Bash early-failure reproduction; pinned upstream source trace of AI creation/content edit and action availability; review of Fable test artifacts/provenance and user-ruling text. **Not reviewer-executed:** Fable's full Bun/MySQL native harness (container lacks local game clone and Docker/MySQL test setup), a completed player battle, fresh live captures, hidden readback, browser/Android UI. No live-game requests/writes or credentials; no engine modification.

**Required Fable follow-up on Fable-owned branch, new frozen head:** (1) correct the generator fail-open and strengthen the documented validator expected-error count check; (2) **apply RUL-2026-10-16-013 on Fable's branch**, marking the previously compiled Extermination Order stats and Solar Bow/Crossbow equipment selections **APPROVED**, while keeping fresh weapon captures as a blocking source-verification task; (3) fix the missing quote and make defeat-dialog recovery-timing copy truthful; (4) regenerate all deterministic artifacts, rerun all pinned gates, provide before/after evidence, and hand back a new exact SHA. Do not change the approved 99-node graph, 16 regulars, four commander kits, reward weights, Beacon timing or existing director rulings as a workaround. AI integration, fresh-source/live username/recipe reads, calibration, final art and the historical ruling-ID collision remain separately identified **pre-manifest/integration gates**.

**Amended verdict recap:** Offline package is **substantively correct and valuable**. **F1's director approval is closed**; the remaining immediate corrections are **F2 runner fail-open, F3 validator error matching and F4 copy accuracy**. Full AI loadout/native battle, captured record validation, calibration and production are distinct **F5 pre-manifest gates**, not evidence the offline authoring package was fully playtested. **Do not merge or publish yet.** Frozen Fable head stays `16dbc5a2` until Fable returns a new SHA.
