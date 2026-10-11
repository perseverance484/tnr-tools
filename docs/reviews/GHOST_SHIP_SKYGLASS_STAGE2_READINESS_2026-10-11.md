# Ghost Ship / Skyglass — Stage 2 independent readiness review

**Verdict: Stage 2 NOT COMPLETE.** Approved design remains intact. The Crystal has a confirmed source-validator blocker; the Katana has a plausible source path but no exact item/runtime proof; Sealwright has no measured Captain-parity evidence; no full Legendary Sword baseline is captured. This review makes the remaining work concrete, not release-ready.

**Date:** 2026-10-11. **Lead:** Engineering Auditor; supporting Content Designer. Fable remains the implementation and new test-harness owner. All balance, reward policy, art, engine-change authorization, publication and final acceptance remain with dauntless.

## 1. Verified targets and authority

| Target | Verified SHA / status |
| --- | --- |
| `perseverance484/tnr-tools`, live `main` | `0eb57de20877d266dde666229ae4c68e8fbcf4c0` |
| Frozen design branch `chatgpt/ghost-ship-skyglass-manifest-roadmap` | `0dbd54c04f2025a1a652712a9ea6df94e35cf8f5` |
| Review branch, based on that frozen design | `chatgpt/ghost-ship-stage2-review-20261011` |
| Latest operative item ruling | `RUL-2026-10-10-007` |
| Historical AI/static-review game pin, called **A** below | `studie-tech/TheNinjaRPG@4774560eb6e8c9a5ef156d66b953dcb6aeeba4d6` |
| Operative item-ruling game pin, called **B** below | `studie-tech/TheNinjaRPG@cddd7d91c9e6bdebc978ddcb61e5b8a305bd0f93` |
| Upstream repository HEAD observed during review, called **C** | `1853b6abef2993615ea6a5c56632ec6a12e0ed8f` |

Live refs were read from GitHub using `git ls-remote`; both TNR refs match the handoff. Game-source files were read from exact commits. Upstream HEAD is **not evidence of the deployed game version**.

The governing brief remains `state/prompt_ghost_ship_skyglass_stage2_feasibility.md`, unchanged. This report adds evidence and review criteria; it does not replace that brief or authorize an engine patch. Read the bootstrap/router/doctrine, relevant engine laws, agent roles, Fable-review/handoff/workstream/decision workflows, all twelve handoff source documents, item/AI references, captures and generated pool. Current global session projections describe September Forge work and are stale as Ghost Ship status; the task-specific roadmap, operative reward decisions and rulings supply this workstream's state. There is no registered Ghost Ship `roadmap.json`; `content_workstream.py list` currently lists only One Perfect Crop. Use the explicit Stage 2 brief rather than invent an initializer task.

### Source drift must remain visible

Compared nine files: `app/src/validators/{ai,combat}.ts`, `app/src/libs/combat/{ai_v2,actions,tags,process}.ts`, and `app/src/server/api/routers/{combat,occupation,item}.ts`.

- A → B: only `ai.ts` and `ai_v2.ts` differ in that set, adding coordinate-action targets and their movement handling. Existing closest-opponent threshold semantics remain.
- B → C: `ai_v2.ts`, `actions.ts` and the combat router differ in that set. Changes include authored NPC ally team targeting, battle participant setup, spawning and scaling. The combat validator, tags, process, occupation and item router are unchanged in this scoped comparison.
- A separate B → C check of `libs/combat/util.ts` finds related NPC-ally victory and closest-enemy changes; the Consume calculations cited below are unchanged.
- Fable must declare one coherent execution pin and dependencies, retain historical provenance, and assess relevant drift. Do not mix A's fixture assumptions with C's battle setup silently. No generated contracts were regenerated or adopted here.

## 2. Freeze and ownership matrix

| Surface | Ready to preserve as approved design | Still required before implementation freeze | Owner |
| --- | --- | --- | --- |
| Quest structure | Model B; 83 objectives each; 26 additions/12 rewires; six endings; wrong-answer lockout; two-battle Crown loop | Final prose, accepted art and fresh complete before-state | ChatGPT/content + dauntless; Fable builds |
| Sealwright identity | Seven moves, intentional S31/B32 overlap, Captain-tier target and starting profile | Actual AI/combat execution, final rule ordering/movement, measured parity and acceptance | Fable tests → independent review → dauntless |
| Katana identity | LEGENDARY WEAPON/SWORD; non-imbuable; Pierce 50 EP + SELF Buff Prevent immunity 2 rounds + Consume 40%; 3% independent Crowned drop | Full Sword baseline capture/acceptance, item parse, combat/expiry/GCD tests | Operator capture; Fable tests; dauntless accepts |
| Crystal identity | WEAPON-targeted CRYSTAL; exactly Consume 20%; 3% Reliquary roll; 12 Filaments per Crystal | Validator support proposal and authorization, actual imbued-weapon runtime, rarity/trading/crafting policy | Fable evidence/proposal; dauntless decision |
| Other reward quantities | Crown fragment 20%; five-to-Crown; no direct Crown; guaranteed Reliquary; existing approved chest table | Remaining item economic fields and recipe/rank accessibility; independent-roll implementation checks | Fable mechanics; dauntless policy |
| Production | Preserve reported hidden state; no independent Sealwright loot | Fresh operator captures, full manifest audit, execution/readback and separate publishing authority | Operator only |

“Approved design” is not a parsed payload or mechanical PASS. No settled percentages, effects, routes or art are reopened by this review.

## 3. Confirmed item findings

### S2-01 — Consume-only Crystal cannot pass the current item validator

**Classification:** confirmed contract/source blocker, not a reason to redesign the item.

At B, `app/src/validators/combat.ts:1339–1347` requires Damage or Pierce in the same array as Consume. The item schema applies that refinement directly to `effects` at line 1600, before the outer item refinements at 1637–1639. A weapon's damage merged later in battle cannot satisfy the Crystal's own validation.

The same validator machinery protects other effect-bearing entities. The smallest proposal to investigate is context-aware support limited to a weapon-targeted Crystal; it must preserve ordinary weapon/jutsu/bloodline and other-target companion checks, including Vamp/Wound. A schema exception alone is insufficient: battle setup must actually combine the effects and the weapon action must generate the intended shield. No fake Damage/Pierce tag, wrapper jutsu, engine modification or validator relaxation was made.

Additional cases for Fable: a recipient WEAPON with no Damage/Pierce; other Consume sources on an eligible weapon; duplicate-crystal rejection; no effect on forbidden recipient types. At B, Consume ratios add up to 100% (`tags.ts:2012–2020`), while occupation rejects the same crystal twice (`occupation.ts:660–663`). Katana exclusion does not settle stacking on every other weapon.

### S2-02 — Katana effect shapes are source-admissible; full item/runtime proof pending

At B, the Pierce/Immunity/Consume tag definitions admit the intended shapes (`validators/combat.ts:513–524,585–605,834–842`), and Pierce satisfies the same-array companion requirement. `maxImbueNumber` has a minimum of one (1561): `canBeImbued:false`, not zero slots, disables imbuing.

The source path is concrete:

- Pierce emits an ordinary damage consequence (`tags.ts:1489–1540`); processing places Pierce before Consume's post-damage pass (`process.ts:576–609`).
- Consume reads new cast-round positive outgoing damage (`tags.ts:2012–2020,3411–3426`). Its basis is **pre-shield damage**, not just health removed (`util.ts:1448–1456,1507–1510`).
- Multi-target contributions aggregate into one shield, floored to integer HP (`process.ts:1032–1044`); shield caps and subsequent absorption/expiry still need exact-item fixtures. The engine default shield duration is three rounds, not a newly approved separate Shield effect.
- Immunity is checked on a newly incoming prevent effect (`tags.ts:194–207`), does not clear an existing Buff Prevent, and is not subject to a blanket next-round-only assumption. Test cast-round and two-round expiry boundaries.
- Occupation rejects a non-imbuable recipient (`occupation.ts:634–645`); battle assembly also suppresses legacy crystal effects when `canBeImbued:false` (`routers/combat.ts:3599–3607`). Test both guards.
- Pierce and Consume participate in the shared cooldown machinery (`app/drizzle/constants.ts:242–262`, `actions.ts:1361–1401`). The shared interval is three rounds; actual behavior depends on the unselected weapon baseline. Players use item level whereas AI item scaling uses character level (`actions.ts:714–743`). Exact costs, levels and zero `powerPerLevel` must be explicit fixture inputs.

Six upstream tests in `app/tests/libs/combat/consume.test.ts` cover synthetic Damage with 25%/50% Consume, shields, multiple hits/targets and later absorption. They are useful existing patterns, **not** exact Katana or Crystal integration evidence. They were inspected, not executed; Bun and the app dependency installation were absent. No new test harness was implemented.

### S2-03 — Crystal rarity/trading changes accessibility

At B, both crafting (`occupation.ts:172–173`) and imbuing (`613–614`) require the player's **current** occupation to be CRAFTING. Gathering/Hunting recipients cannot do either while retaining their profession. The occupation switch cooldown is three days (`app/drizzle/constants.ts:40`, `occupation.ts:89–103`).

| Crystal rarity | Minimum rank for crafting and imbuing | XP threshold | Craft/imbue minutes at that rank |
| --- | --- | ---: | ---: |
| RARE | Apprentice | 100,000 | 65 |
| EPIC | Master | 300,000 | 70 |
| LEGENDARY | Forgemaster | 600,000 | 160 |

Source: `app/drizzle/constants.ts:1623–1665`, selected by `occupation.ts:223–243,666–673`. Higher ranks shorten some times. Novices have no imbuement slots. The imbuing error string's Epic/Legendary rank labels are stale; the table governs eligibility. Rarity is still a dauntless decision despite the general item default.

Trading the raw Crystal or Filaments does not waive the eventual user's imbuing occupation requirement. Policy must explicitly consider occupation switching and any intended trade of already-imbued eligible weapons; do not promise a service route without checking those recipient/transfer rules.

## 4. Sealwright findings and parity fixture contract

### S2-04 — B32 trigger target differs from its possible effect recipients

The October 9 full `jutsu.get` capture records B32 as **ALL method**, OTHER_USER target, range 5 (`harvests/inbox/tnr_results_1791583362574.json:3554–3630`). The compact pool omits method.

At A, `app/src/libs/hexgrid.ts:146–147` expands ALL to the grid; `libs/combat/util.ts:2992–2997` and `actions.ts:1044–1077` evaluate eligible targets, subject to friendly-fire/stealth rules. Thus closest-opponent IDG and gate 6 determine **whether to cast**; they do not make Clear single-target. Gate 6 is a director-approved trigger restriction, not a necessary native ALL attack-range limit. Preserve it; do not remove it mechanically under generic law 40.

Required cases beyond a one-opponent model:

- IDG 69/70/**70.5**/71/90: integer threshold 71 uses `>=`; 70.5 does not trigger. This is the approved native rule's boundary, not exact real-number `>70` equivalence.
- Near low-IDG summon versus farther high-IDG player; a distant second opponent after the closest target triggers; blocked paths that lengthen the gate distance.
- Newly cast/inactive or protected IDG: the condition sums matching raw powers without the same filtering used for effective/removable buffs.
- Unavailable B32 must fall through; S31 must remain a regular high-priority attack. Clear prevention and protected source behavior must be shown, not inferred from “100% Clear.”

Source at A: `validators/ai.ts:100–105`, `ai_v2.ts:123–127,334–352,484–490,530–535`, `tags.ts:1162–1234`. No automatic threshold, targeting or jutsu changes are proposed.

### S2-05 — Captain fixture must include the intended migration and innate effect

The parity comparator is the **regular Captain**, not Crowned Captain. Keep these two versions distinct:

| Comparator | Record/kit/rules |
| --- | --- |
| October 1 captured legacy Captain | `QY69h271Nx9uHrBeR6jwW`, then named Pirate King; Death's Door, B17, Battle Trance, B14, Death's Grasp; combo profile and `includeDefaultRules:true` |
| Approved intended migrated Captain | Same AI ID; B19/B14/B17/B05/S31/B33; rebuilt order and `includeDefaultRules:false` |

Evidence: `state/ghost_ship_shared_pool_migration.json:445–495`; `harvests/inbox/tnr_results_1790828718767.json:1076–1156`. Use the intended migrated Captain as the primary release-parity comparator; label the captured legacy case separately if included for regression context. This follows the roadmap's Stage 2 comparator direction and does not choose a different balance target.

The October 1 full AI also contains **innate 30% Highest offense/general increasestat for 99 rounds** (`harvests/inbox/tnr_results_1790826836406.json:8096–8119`). At A, battle assembly initializes it active with protected bloodline provenance (`routers/combat.ts:3479–3494`). Do not drop it from the Captain fixture or silently copy it to Sealwright. AI Heavy Armor and Cursed Dagger are both `equipped:NONE`, so their ordinary combat effects are excluded; that does **not** exclude innate AI effects. Preserve preferred Bukijutsu/Speed/Strength, null elements and the captured numeric profile explicitly.

Final rule/movement acceptance must follow actual `performAIaction` and combat execution: 40+60 AP cadence, no exhaustion/death, S31 positioning alternatives, B16 control-lock duration, turns to win/loss, damage spikes, shield/buff uptime, Clear frequency, pool pressure and counterplay over a declared player-fixture matrix. Equal starting multipliers are not measured parity.

The current rule-contract blob matches the old static report: `be9cfe4f243755016e385aae8bc438dfb96854a6`. Its reported 112 assertions/12 scenarios are a small source-derived model; no committed reproducer or Sealwright combat harness was located. **That pass count was not rerun or promoted to engine evidence.** Generic upstream `ai_v2_rules.test.ts` and `ai_v2_unreachable_target.test.ts` were inspected only.

## 5. Legendary Sword baseline recommendation

**Recommend the next record to inspect, not unverified numbers.** Recursive inspection parsed all **299 repository JSON files**, found **four full WEAPON dictionaries / three distinct IDs**, and **zero full LEGENDARY/SWORD records**. No committed numeric baseline qualifies.

| Full captured record | Why it cannot be used |
| --- | --- |
| Flaming Sword; `tnr_results_1788235198666.json#/captures/8/data/items/0/item` | SWORD, but EPIC; September 1 |
| Barrage of 1000 Demons; `tnr_results_1789271613950.json#/captures/16/data/items/0/item` | LEGENDARY, but weaponType NONE; September 13 |
| Cursed Dagger; `tnr_results_1790826836406.json#/captures/{9,10}/data/items/{1,3}/item` respectively | COMMON/DAGGER; October 1 |

Night's Testament `osJq3k77YPGoFWgof12FQ` is the first suggested comparator to capture. `harvests/seed/41_INDEX_item.json#/rows/422` confirms only index data including WEAPON/LEGENDARY/HAND, with `last_verified:null`. It does not establish SWORD or costs/range. Battle action-ID occurrences are not item records. Alternate index candidates, only if necessary, are Chakra Sword `oOdkdJixCLy2bW0Gxo5e0` and Masamune `An9G-YkaAonclWsmcpx4E`; their Sword typing also requires capture.

Minimal **operator-run read-only capture specification**, not an executable manifest and not an agent request:

```json
{"proc":"item.get","input":{"id":"osJq3k77YPGoFWgof12FQ"},"persist":"full"}
```

Keep the complete returned row and export metadata (`at`, `ok`, `persistOk`, `snapshotKey`), no field selection. Require a non-null matching ID and LEGENDARY/WEAPON/SWORD before recommending a baseline. Compare AP, cooldown, all pool/health costs and reducers, target/method/range, slot/durability, level/stat requirements, battle scope, trade/economy and all server-required fields. `item.get` is defined at B `routers/item.ts:217–230`; crafting relations require the separately exposed query at 262–273 if needed. Existing `push/58_ghost_ship_retheme_dependency_capture.json` demonstrates the established full-capture workflow; this review creates no new operator manifest.

Fresh full `quests.get` captures for both profession IDs remain mandatory before edits. The October 1 `hidden:false` values are historical; preserve the current director-reported hidden state and verify it through the operator's fresh capture. No hide/unhide operation is implied.

## 6. Independent checks and limits

| Check | Actual result this review |
| --- | --- |
| In-memory graph audit against both captured quest graphs | Each: 57 preserved + 26 new = 83; 12 rewires; one root; all 83 reachable; six endings; no success/failure cycles excluding reset targets; all 13 battles dialog-gated; secret-only archive outcome; wrong-answer lockout cannot reach secret; direct Crowned route minimum two battles |
| Complete JSON baseline population scan | 299 parsed, zero parse failures; four full weapons; zero Legendary Swords |
| Exact source file inspection and scoped pin diffs | Completed at A/B, with C drift reported above |
| `session_open.py` | Exit 1: lawmap 0 errors/5 pre-existing warnings; doctrine and packs current; parity adapter fails on capture `checks:null` |
| `harvest.py verify harvests/inbox/tnr_results_1791583362574.json` | Exit 0; capture-only bundle, zero write entries, nothing to verify |
| `validate.py --parity ...1791583362574.json` from skill data directory | Exit 1, `TypeError: 'NoneType' object is not iterable` at line 201; pre-existing adapter issue, not a manifest-validation result |
| `content_workstream.py list` | One Perfect Crop only; no Ghost Ship task registry |
| `content_workstream.py validate --all` | Exit 1: unrelated Crop `launch.finalization` evidence references absent `push/54_one_perfect_crop_launch_final.json` |
| Exact ItemValidator / battle / Captain-parity execution | **Not performed; Fable deliverable still required** |
| Art intake, regeneration, preflight | Outside this Stage 2 packet; no locked art changed |

The unrelated global guard failures were recorded, not silently fixed or labeled green. `session_open.py`'s ledger-only changes to `state/digest.json` were restored so this review does not rewrite unrelated global operational history. No Forge manifest was assembled or validated, so there is no “manifest PASS” claim.

Two stale planning labels were found: the full roadmap still called the count an unlocked 75–85 estimate, and graph metadata says `SEALWRIGHT_UNSPECIFIED`. The report's branch corrects only the roadmap's count sentence and adds a review pointer. The graph file remains byte-for-byte unchanged; its stale combat label must not override the later seven-move ruling or imply full combat approval.

## 7. Remaining decisions and next handoff

Fable can begin the existing offline brief now on a separate owned branch. No additional authorization is needed for that already-authorized research/test work. Return a frozen exact SHA with the chosen source pin, fixture provenance, reproducible commands/results, and PASS/BLOCKED per package. Preserve all locked designs. This review has not sent a message to Fable or started another agent's implementation session.

Decisions requiring evidence before acceptance:

1. **Engine dependency:** whether to authorize a separately scoped, test-backed Crystal validator/runtime correction once Fable supplies the minimal proposal. If support cannot be delivered, the affected Crystal release path stays blocked; do not substitute another effect.
2. **Sword baseline:** accept exact remaining item values after a qualifying full capture and comparison.
3. **Crystal/Filament access policy:** rarity, tradability, crafting/imbuing rank and occupation-switch consequences; remaining item/recipe economic fields. The 12-Filament requirement and all approved chest/drop numbers are already settled.
4. **Sealwright final tuning:** accept measured Captain parity, exact rule order/movement and any disclosed behavior at fractional thresholds/multi-target boundaries. Seven jutsu and overlapping Clears remain locked.
5. **Final prose and art:** accept wording and outstanding assets, intake/preflight exact selected artwork. No redesign of accepted Katana/Crystal art.
6. **Later release:** technical/content freeze, fresh full before-state and shared-AI dependency audit, Fable's complete manifest, independent review, operator execution/readback, and separate publication acceptance.

The approved reward quantities are not a new question. Any remaining repeat-farming policy discussion must evaluate those approved loops, not silently change their rates.

**Safety record:** live-game requests **0**; live-game writes **0**; asset-CDN requests **0**; game credentials **none**. Repository reads/source retrieval only, plus this isolated review documentation. No engine changes, Fable-branch edits, art changes, publication or full write manifest.
