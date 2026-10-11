# Ghost Ship / Skyglass Project — full-manifest release roadmap

**Latest Crowned Captain decision (RUL-2026-10-11-007):** activate healing at40% health, Copy against high IDG and regular Reflect. See `state/ghost_ship_skyglass_crowned_support_behavior.md`. Exact Copy threshold, native strict-below40 boundary, ordering and measured difficulty remain open; the prior dormant-support activation question is resolved in favor of activation. Historical support tests do not validate the new conditions.

**Current decision checkpoint (2026-10-11, RUL-2026-10-11-006):** both active Consume buffs and generated shields are **2/2 rounds**. Katana15/Crystal10 rates stay fixed. Crystal is **LEGENDARY, tradable, not craftable**; the12-Filament recipe is removed. Other Reliquary rewards remain. Consume overlap is expressly deferred and does not block this pass. Final item revalidation: `state/prompt_ghost_ship_skyglass_final_item_revalidation.md`. The new Sealwright attack-first/late-movement/basic-strike design is `state/ghost_ship_skyglass_sealwright_behavior_proposal.md`, pending director acceptance and tests. Historical records/evidence remain unchanged.

**Latest combat decision (2026-10-11, RUL-2026-10-11-001/002):** The eleven-record roster in `state/ghost_ship_legacy_retention_review.md` is approved, including Explosion and six Crowned Captain legacy signatures. Names, descriptions and battle text are converted in `state/ghost_ship_legacy_jutsu_conversion.json` with a readable `.md` companion; final presentation acceptance remains open. All mechanics and original IDs are preserved. Wholesale shared-pool replacement, blanket legacy retirement and the automatic Explosion clone are superseded. Hybrid kit membership and the five-move regular-Captain comparator are accepted under RUL-2026-10-11-003; exact rules and parity require tests before combat freeze; Sealwright's seven moves, quests, rewards/items and art locks are unchanged.

**Status:** ROADMAP ACTIVE; **83-node / six-ending Stage 1 structure director-approved** under RUL-2026-10-10-003. Stage 2 r4 offline evidence covers its pinned engine and former item contracts; the revised active Consume items require revalidation. Final combat acceptance, prose, art and full manifest remain pending. No live execution or publication authorization.
**Repository baseline:** `perseverance484/tnr-tools@0eb57de20877d266dde666229ae4c68e8fbcf4c0` (verified 2026-10-10).  
**Lead:** Content Designer (ChatGPT); implementation: Fable / Claude Code after freeze; independent review: ChatGPT; all live-game requests/writes and publication: director/operator only.  
**Outcome:** one complete reproducible Ghost Ship release, with the two existing profession quests, six endings each, Skyglass retheme + expanded exploration, selective legacy retention and shared-pool replacements, accepted art, and new reward loops. A combined Forge manifest is technically feasible; execution staging and cutover must be chosen separately.

**Historical Consume revision checkpoint (RUL-2026-10-11-005):** Katana15/Crystal10 introduced active Consume. R4 evidence at engine `cddd7d91c9e6bdebc978ddcb61e5b8a305bd0f93` remains historical. Upstream `585534d7eb21d6f0dd678d5c3eb92662f611d39b` allows positive-duration Consume without a Damage/Pierce companion; deployment remains unverified. RUL006 now settles timing/economy and supplies the final-item brief. Night's Testament baseline remains accepted under RUL004.

**Active Consume candidate execution:** `docs/reviews/GHOST_SHIP_ACTIVE_CONSUME_OFFLINE_RESULTS.md` records passing Katana15/Crystal10 schema, runtime and eligibility tests using **historical3/3 carriers**. Exact source drift and provenance are included. Final2/2/economy revalidation, independent review, presentation and director combat acceptance remain open; no manifest freeze follows from that PASS.

**Hybrid kit baseline accepted:** `state/ghost_ship_hybrid_kit_proposal.md` / `.json` are accepted under RUL-2026-10-11-003, including Sentinel reuse and disclosed shared-substitution tradeoffs. They preserve all original retained/shared memberships. The regular Captain keeps its captured five moves. Crowned support activation is directed by RUL007; exact behavior details, final ordering and measured parity remain open.

## Source/evidence hierarchy

- `docs/00_INDEX.md`, `docs/DOCTRINE.md`, `docs/ENGINE_LAWS.md`, `docs/RULINGS.md`, `CHATGPT.md`, `docs/DEVELOPMENT_WORKFLOW.md`.
- `state/ghost_ship_skyglass_reward_decisions.md` — operative item/reward specification and current hidden-state report. `state/ghost_ship_skyglass_final_item_contract.json` records RUL006's final timing/economy design; the previous `ghost_ship_skyglass_consume_revision.json` remains historical RUL005 input. Neither is a full item record.
- `state/ghost_ship_skyglass_expansion_design.md` — **Stage 1 STRUCTURE APPROVED** for the 83-node six-ending quest (RUL-2026-10-10-003); new dialogue and choice prose remain draft.
- `state/ghost_ship_skyglass_graph_patch.json` — machine-readable **STRUCTURE APPROVED / PROSE DRAFT** patch containing 26 new nodes, 12 original forward-edge rewires, four new scene symbols and one Sealwright AI symbol. Not a Forge manifest.
- `state/ghost_ship_skyglass_sealwright_rule_contract.json` — preserved historical7-jutsu rule plan tested by r3/r4. New proposed movement/basic behavior: `state/ghost_ship_skyglass_sealwright_behavior_proposal.md`; no live writes or implementation freeze.
- `docs/reviews/GHOST_SHIP_SEALWRIGHT_RULE_STATIC_CHECK.md` — 112/112 narrow source-key/priority static checks, 12 selection scenarios; deliberately NOT full game combat or true Captain-parity proof.
- `state/prompt_ghost_ship_skyglass_stage2_feasibility.md` — historical r4 offline brief. Its item packages are superseded for new work by `state/prompt_ghost_ship_skyglass_consume_revalidation.md`; approved combat scope is unchanged. Neither authorizes game writes.
- `state/ghost_ship_skyglass_sealwright_combat_draft.md` — **Director-accepted seven-jutsu kit and intentional double-Clear identity** (RUL-2026-10-10-006); S31 Unraveling Strike routinely strips removable buffs, B32 Nullifying Wave remains conditional on IDG above 70. Effective parity and final AI priority/positioning still require offline validation.
- `state/ghost_ship_retheme_design.md` — Skyglass lore, reveal cadence, named entities, rewards (original preserve-57 scope is now superseded for the expansion only).
- `state/ghost_ship_retheme_patch.json` — approved base 57-node text/identity/reward patch. Invariant to preserve all edges and count MUST be explicitly superseded by a versioned expansion; do not silently alter this base or treat it as the full release.
- `state/ghost_ship_legacy_retention_review.md` — approved eleven-record retention roster and pool-comparison rationale.
- `state/ghost_ship_legacy_jutsu_conversion.json` / `.md` — authored three-field text conversion on the eleven existing IDs; all other captured fields preserved; presentation acceptance pending.
- `state/ghost_ship_hybrid_kit_proposal.json` / `.md` — accepted eleven-enemy hybrid membership and exact source references under RUL-2026-10-11-003; final behavior and measured balance require tests/acceptance.
- `state/ghost_ship_shared_pool_migration.json` — superseded all-shared kit/clone proposal, retained as historical evidence with an explicit policy override. Final hybrid kits remain open.
- `harvests/inbox/tnr_results_1790826101573.json` — two full live quest records + out-of-scope Drowned Fleet.
- `harvests/inbox/tnr_results_1790826836406.json` — 11 directly wired AI records, 10 scene assets, item captures.
- `harvests/inbox/tnr_results_1790828718767.json` — 11 AI profiles + Crown record.
- `harvests/inbox/tnr_results_1791727479372.json` — push/85 full Night's Testament capture, the accepted RUL-2026-10-11-004 Katana baseline. The frozen `state/ghost_ship_skyglass_katana_record.json` retains former Consume40/rounds0 for historical r4 reproducibility; use the new Consume design delta for its next version.
- `skills/building-tnr-content/` quest/AI/item/balance/pipeline references and current generated contracts; `forge/src/runner/{refs,manifest,runner}.mjs` and Forge tests; `skills/producing-tnr-art/` spec, processing and QC.
- Approved art source: conversation-mounted `ghost_ship_skyglass_art_handoff.zip` (35/35 manifest SHA-256 checks pass, 9 already processed). It is **not yet a committed repository source**; intake is mandatory before a workstream task may be called READY. Director-selected raw Crystal/Katana art are also currently conversation assets, not preflight-clean WebPs.

## Verified captured starting point

Two existing quests, as recorded in the older October 1 captures:
- Gather `6Ri-W5TtUrEMWpyYlnf_F`: `questType:gathering`, S-rank Gathering.
- Hunt `HckXVOf-qk6ESU9t5rxLh`: `questType:hunting`, A-rank Hunting.
- Each: 57 nodes (24 dialog, 12 start_battle, 14 reset, 2 collect_item, 5 win), `hidden:false` **in that historical capture**, `consecutiveObjectives:true`, `retryDelay:none`, `maxAttempts:1`, `maxCompletes:1`, top-level sceneBackground empty, 6 existing unique backgrounds and 3 named portraits. Gather/Hunt have reward and location differences. The caps are not reliably enforced for these profession quest types under the documented engine behavior.
- **Current visibility:** director reports both quests are now **hidden**. Historical `hidden:false` in October 1 capture must not be treated as current; fresh user-run `quests.get` before any update must confirm `hidden:true`. No agent live read was performed.
- Entrances: gangplank / hull infiltration / Oathkeeper parley. Main branches: chart/cache / hold accessible / hold vault / normal Captain. Oathbound direct Crowned Captain shortcut is intentionally short for repeated fragment farming; **do not add mandatory detours**.
- Five existing ends `w_A, w_B1, w_B2, w_C, w_Co`. The expansion adds one mutually exclusive *secret* Reliquary ending per quest rather than an extra reward collected before continuing to Captain.
- Drowned Fleet is out of scope; preserve its records and check for any AI reuse before edits.

## Locked content goals / release scope

- Original fiction: airborne forbidden shinobi warship supported by a Skyglass Core/seal lattice; reconstructed chakra impressions, not undead; crew memory tragedy; original nine-beat reveal; Crowned Captain alone carries deepest terminated-mission failure truth.
- Preserve 11 captured existing AI IDs; retain the approved eleven legacy jutsu with unchanged mechanics and replace genuinely redundant roles from the shared pool. Add **Sealwright** as the one new secret-route Captain-tier boss after combat design freeze. Rename the original Explosion to `Core Rupture` for Seal Charge/Core Canister; do not clone it. The remaining 26 captured legacy-only records are retirement candidates for Ghost Ship kits, not deletion targets.
- Two quest records keep their IDs and profession-specific reward fields/coordinates except expressly approved changes. The approved graph is exactly **83 objectives per quest** (57 preserved + 26 additions, with 12 original forward-edge rewires). Six endings, with the secret archive route terminating exclusively at its own ending.
- Model B: exterior keel traversal, reconstruction chamber, quarantined archive/Sealwright secret branch, command observation gallery, deeper Wayfinder/Arsenal Keeper/First Blade interactions, visible failure-feedback dialogs, stronger Captain escalation.
- `Skyglass Serum` is the director-approved restorative rename; stale `Stillwater Tonic` prose in original patch is superseded.
- Existing Crown: `Fragment of the Skyglass Crown` = **20% Crowned Captain AI loot only**; remove the 10% `w_Co` quest roll; five fragments craft `The Skyglass Crown`; no direct Crown drop; no change to confirmed Crown mechanics; clear erroneous Captain equipment drops and the Diadem attachment.
- New **Legendary `Skyglass Katana`**: **3% independent Crowned Captain AI drop**; WEAPON/SWORD, `canBeImbued:false`. Exactly Pierce50 (Crystal), SELF Buff Prevent immunity2r, and active Consume15 (`rounds:2,shieldRounds:2`). Weapon actions grant the buff; qualifying damage generates shields. No extra Damage, flat Shield or Shield Potency tag. Other Night's Testament baseline/economy fields remain RUL004-approved.
- New `Skyglass Reliquary`: **one guaranteed chest for successful secret-route ending** (both professions). Director-approved proposed loot structure: guaranteed 1 Skyglass Filament + 3 Rare Jewels; independent chances 25% bonus Filament, 30% Skyglass Serum, 15% Ornate Chest, 3% Skyglass Crystal. No fragments or Katana in Reliquary.
- **`Skyglass Crystal`**: LEGENDARY, tradable, not craftable; WEAPON-only CRYSTAL with exactly active Consume10 (`rounds:2,shieldRounds:2`). Independent3% Reliquary direct drop; no12-Filament recipe. Cannot imbue Skyglass Katana. Positive-duration Consume passed3/3 carrier tests; final2/2/economy validation remains. Do not add Damage/Pierce filler. Filament drops remain unchanged with replacement use/trading unresolved.
- No new cosmetic gear/Latticebound Guards, no generic new pirate jutsu, no automatic new loot family, no changes to independent quests.

## Entry/mutation inventory (planning estimate, not frozen)

| Type | Target logical records | Candidate count | Critical rule |
| --- | --- | ---: | --- |
| Existing retained AI jutsu | Eleven approved presentation-only conversions, including Explosion to Core Rupture | 11 | same IDs and mechanics; fresh capture/dependency checks before edits; no clone |
| Existing scenes | 6 existing SCENE_BACKGROUND + 3 named SCENE_CHARACTER updates | 9 | reuse captured IDs; blank character unchanged |
| New scenes | 4 backgrounds + Sealwright scene portrait | 5 | create hidden; preserve lower-left overlay space |
| Existing items | Skyglass Serum, Crown Fragment, Crown edits | 3 | existing live IDs/mechanics preserved |
| New items | Reliquary, Filament, Crystal, Katana | 4 | full captured/template contracts; correct creation order |
| AI | 11 existing profile/kit/loot edits + 1 Sealwright create | 12 | capture full before images, rules embedded in AI entries |
| Quests | 2 full-record edits, existing quest IDs | 2 | preserve eligibility and all unaffected fields |
| **Total** | | **~46** | subject to contracts, status, new art, and final route spec |

Forge `forge/src/runner/refs.mjs` at base already supports `@item:`, `@ai:`, `@scene:`, `@jutsu:`, `@img:` with stable topological create ordering. A single combined full manifest can therefore reference a newly created Crystal/Filament inside the Reliquary table and a newly created Reliquary inside the quest. Fable must check release/current Forge behavior rather than assume old pipeline prose lists every ref.

## Stage 1 structural approval checkpoint (2026-10-10)

Stage 1 structure was **APPROVED by the director**, preserving the machine design proposal for prose refinement: `state/ghost_ship_skyglass_expansion_design.md` plus `state/ghost_ship_skyglass_graph_patch.json`. Both Gather and Hunt have been checked offline against the October 1 captured full objective graphs: **57 preserved nodes + 26 proposed additions = 83 nodes each**, **12 existing edge rewires**, **one root**, **all nodes reachable**, **six reachable endings**, **zero success/fail cycles**, **all 13 battle nodes dialog-gated**, and **no invented new map location tasks**. The secret route requires the hull/Core Horror and ends exclusively at `w_secret`; the direct Oathkeeper → Crowned Captain route still has two battles. The permanent original node IDs, AI opponent blocks, timed location mechanics, and original Gather/Hunt rewards are unchanged except where a later approved reward correction expressly applies.

**Director-approved structure (RUL-2026-10-10-003):** 83-node scope and optional dialog branches; wrong archive seal choice closes the secret route only for the current quest run; Sealwright as quarantine custodian and exclusive secret-route elite; single Reliquary sixth ending; short two-battle oathbound Crown route. **Still open:** final wording of new dialogue/choice text, exact Sealwright shared-pool AI combat profile and tuning, item-engine gates, art intake, and fresh hidden-state capture. These block the full manifest, not the accepted route structure.

## Stage 2 Sealwright kit accepted; exact combat implementation checks pending

**Director-approved two-Clear identity:** **S31 Unraveling Strike** regularly strips all removable positive buffs as a high-priority damaging attack; **B32 Nullifying Wave** is the seventh jutsu held for enemy IDG above 70. The overlap is INTENTIONAL (RUL-2026-10-10-006). B32 uses source-backed integer threshold 71; 100% Clear removes all removable positive effects, not IDG selectively. Its conditional rule must remain first and fall through when unavailable. **No jutsu may be deleted to remove the overlap.** Source-backed nine-rule positioning/behavior proposal: `state/ghost_ship_skyglass_sealwright_rule_contract.json` (not executable).



The director rejected the initial mid-tier Sealwright proposal and requested **meaningful boss-pool jutsu and practical parity with the regular Captain**. The October 1 full AI capture gives the regular Captain **Level 100/JONIN; 3.0× stats; 2.5× pools; 60 regeneration**. The revised candidate is at `state/ghost_ship_skyglass_sealwright_combat_draft.md` and uses that same starting profile, with **B14 Cataclysm Detonation** and **B16 Sovereign Fetters** as two genuine high-impact boss-pool signatures alongside **B22, B33, S27 and S31** for defense, piercing and suppression. The seven-technique roster is now the director-accepted design target, although precise AI rule priority and relative fight difficulty remain unvalidated. Fable must use the accepted five-move Captain kit **Unbroken Command, Keelbind, Remembered Form, B14 and B17**, confirm Captain item eligibility, and validate its rules before claiming final parity. The earlier all-shared **B19/B14/B17/B05/S31/B33** comparator is historical. The older October 1 captured Captain's AI Heavy Armor and Cursed Dagger were both `equipped:NONE`; current game source does not activate their passive or weapon effects when unequipped, so do not invent extra Sealwright gear for parity. In particular, B16's combined 2-round Stun/Seal could make the fight too oppressive if AI priorities are careless. No new custom Sealwright jutsu, extra battle phases, or boss loot are implied. Do not translate this draft into an AI/quest manifest.

The Stage2 item remainder is final2/2 record/runtime validation and independent review. Rates, both timers, Katana baseline and Crystal rarity/trade/no-crafting are settled. Overlap policy is deferred. R4 and the3/3 package remain historical; Sealwright/AI acceptance and fresh operator-run hidden-state capture remain separate gates.

**Current item handoff:** `state/prompt_ghost_ship_skyglass_final_item_revalidation.md`. Fable tests the approved2/2 records and Legendary/tradable/non-craftable Crystal. Preserve r4 and the3/3 package at their exact frozen SHAs. No live requests/writes or upstream engine modification. Sealwright's new behavior proposal awaits acceptance for testing; prior A2 parity is not accepted.

## Roadmap / stage gates

| Stage | Owner | Deliverable | Acceptance gate |
| --- | --- | --- | --- |
| **0. Source and live-state reconciliation** | ChatGPT/Fable; director runs captures if required | Exact-SHA source map, latest read-only quest/AI/item captures with **hidden:true** readback and exact Legendary weapon stat baseline, existing art digest and route/loot deltas | No invented IDs or stale full-record edit baselines; zero changes to game |
| **1. Expansion structural freeze (APPROVED)** | ChatGPT + director | `state/ghost_ship_skyglass_expansion_design.md` + `state/ghost_ship_skyglass_graph_patch.json`; 83-node graph with six endings and 12 rewires | **Structure approved RUL-2026-10-10-003; final dialogue wording and Sealwright combat are separately pending.** |
| **2. Technical feasibility / reward freeze** | Fable source/contracts + ChatGPT independent audit; director rules | Final Sealwright/Captain acceptance; accepted Sword baseline; Katana Pierce50 + immunity2r + active Consume15; weapon-only one-effect Crystal Consume10; separate buff/shield timing and updated runtime/guard tests; economy decisions | No unresolved timing, inert Consume or extra effects. Old-pin PASS is historical for changed mechanics. Engine changes require separate authorization/review |
| **3. Art intake + completion** | ChatGPT Art Director/Image Production + director QC | Commit/cache exact 9 processed approved assets and selected new raw sources with provenance, finish remaining art and deliver preflight-valid WebPs + SHA/filename ledger | ~25 remaining deliverables from prior plan including Katana; selected Crystal and Katana designs stay locked; content-specific scene wiring checks, all under art spec ceilings |
| **4. Full compile and dry-run** | Fable | Versioned combined Forge manifest + generator if appropriate, `imagePack` pinned to immutable repo art commit, full after-captures, reproducible package and operation census | All refs resolved, full-field/schema and graph validation 0 errors, no duplicate create, all assets/IDs known, order and runner tests pass |
| **5. Independent frozen-SHA audit** | ChatGPT | Report against exact Fable handoff SHA plus test evidence | Audit graph reachability, 6 endings, profession parity, loot math, Crowned/Captain regression, shared pool migration, source diffs, image digests, no public exposure/secret writes; blockers closed |
| **6. Operator-controlled production preparation** | director/operator only | Approved maintenance/publish plan; latest before-state and explicit rollback/recovery checklist | Director reports both quests currently hidden: obtain fresh pre-write read-back verifying `hidden:true`; preserve it on every edit. Do not issue an unnecessary hide/unhide transition. Audit shared AI reachability separately before mutations |
| **7. User-run execution + read-back** | director/operator only; Fable/ChatGPT read evidence afterward | Complete Forge result, idmap, full record after-captures, mismatch/diff report; defer public publish until separate approval | All new content created hidden and both quest edits retain `hidden:true`; no unresolved partial writes; exact AI drop rates/recipes/scene refs/art bytes verified |
| **8. Publication + post-launch** | director/operator only | Explicit publish decision, operational closeout, return to current-state capture, archive spent manifests | No publication without separate user authorization, rollback available, old quest continuity and farm route verified |

### Sequence and likely parallelism

- Stage 0 and preparatory art SHA intake can begin before full narrative freeze. Do **not** begin mass new art until target rooms and dialogues are frozen.
- Stage 1 (graph) and Stage 2 (mechanics) can run in separate contexts, then converge at a director content/reward freeze. Art generation uses the frozen visual list one asset at a time.
- Full compile depends on all new/updated entities and art (Stages 1–3). Frozen-SHA review follows compile; no further edits on Fable's frozen branch until review returns.
- Stage 6 is a separately approved **live production cutover**. A monolithic manifest is a compilation deliverable, not authority to execute it. If executing a monolith risks partial publication or rate-limit recovery, Fable may propose dependency-safe sub-manifests with a single release specification, but the user decides launch structure.

## Production safety and mechanical blockers

1. **Hidden-state discrepancy:** Both quests were `hidden:false` in the October 1 capture, but director explicitly reports that they are **currently hidden**. Treat the historical capture as stale for visibility, verify with an operator-run pre-write readback, and preserve `hidden:true`. This removes the previously assumed mandatory public-quest hide/cutover step, not the need for production safety or fresh full-record bases.
2. **Outdated retheme invariant:** `state/ghost_ship_retheme_patch.json` says preserve 57 objectives/edges. Model B explicitly supersedes that constraint while inheriting unchanged lore/IDs/combat foundations; version a new patch with explicit diffs.
3. **Legendary Sword baseline (settled):** Night's Testament accepted by RUL004, including AP40/CD6/range4 and costs40/40/0. Preserve its non-effect fields. Fable versions the final Consume15/2/2 record under RUL005/006 while preserving historical evidence.
4. **Katana final runtime verification:** Validate Pierce50, SELF Buff Prevent immunity2r and active Consume15 with approved2/2 timers. Confirm exact activation/expiry, later-hit conversion, Clear/Buff Prevent, accepted costs/cooldown and non-imbuable guards. No live combat experiments.
5. **Consume-only Crystal:** Director locks active **10% Consume on a WEAPON-only CRYSTAL**, exactly one effect. At reviewed source `585534d7`, the companion Damage/Pierce restriction applies only to instant Consume (`rounds:0`). Positive-duration standalone Consume is source-admissible; full-item and imbued-action runtime tests remain required. Reassess the old correction proposal instead of implementing it automatically. No extra damage tag or unauthorized engine change.
6. **Rarity/trade/occupation:** Crystal is now Legendary, tradable and not craftable. Verify native Legendary imbuement access without bypassing occupation/rank guards; trading allows transfer to an eligible crafter. No Crystal crafting route remains.
7. **Farm economics:** Fragment20%, Katana3%, guaranteed Reliquary and its fixed loot table remain approved. Remove the12-Filament conversion from new construction. Filament replacement use/trading remains unresolved; do not invent either. Track expected drops and variance from the approved table.
8. **Shared AI dependencies:** Audit current usages of all 11 existing Ghost Ship AIs outside these two quest records and consider effects of new kits; Drowned Fleet untouched. All AI inventory dropChancePerc and equipped jutsu/rule orders verified independently.
9. **Art is not yet release-ready:** The nine processed ZIP assets are exact and hash-verified but not repo-pinned. Current selected Katana `1000018208.png` and Crystal `1000018205.png` are opaque RGB raw; process without altering accepted visual, QC dark background vs rarity frame, and pin immutable delivered bytes.
10. **Engine graph:** All dialogs need true choice targets; `start_battle` must be dialog-gated; no cycles except reset mechanism; visible feedback before reset; single start; all six ends reachable; every profession coordinate valid. `consecutiveObjectives:true` and complete quest update payloads are mandatory.

## Non-goals / prohibited actions during planning

No direct live-game requests or writes, no publication, no change to any active Fable branch, no automatic mass art generation, no immediate manifest, no Drowned Fleet changes, no retiring legacy jutsu deletion, no generic Skyglass lore alteration. Repository proposals remain unmerged until the director accepts design boundaries.

## Director-facing decision queue (do not fill in by convenience)

- **Hybrid memberships accepted (RUL-2026-10-11-003):** Sentinel reuse, First Blade EL04 and all disclosed shared substitutions are accepted for testing. Crowned support activation is directed by RUL007; its precise trigger/boundary/order and measured balance remain open alongside other final AI behavior. Membership selection is not reopened.
- The quest graph and **seven Sealwright techniques** are approved as design intent, including S31's routine Clear plus B32's IDG-threshold Clear. Do not treat them as redundant. **Still open:** source-checked rule positioning, comparative Captain parity and any director-signed test adjustments.
- **Resolved (RUL006 and prior approvals):** Katana identity/baseline/economy, Pierce50 (Crystal), immunity2r and Consume15; weapon-only Crystal with one Consume10, Legendary/tradable/not craftable. Both Consume timers2/2. **Open:** final2/2/economy validation, independent review, presentation and release gates. Consume overlap is deferred and not blocking this pass.
- Filament tradeability/use remains open after removal of the Crystal recipe. The fixed Reliquary table remains approved.
- **Visibility:** director says both existing quests are currently hidden. Operator confirms with fresh captures; maintain hidden state during edits. Separate publishing decision remains open.

**Immediate next tasks:** Fable executes `state/prompt_ghost_ship_skyglass_final_item_revalidation.md` on a new owned branch. Director reviews the concrete Sealwright behavior proposal, then Fable compares it offline if accepted for testing. Return exact-source validation, reproducible evidence and frozen SHAs. No full manifest before technical/content/art/current-capture gates.
