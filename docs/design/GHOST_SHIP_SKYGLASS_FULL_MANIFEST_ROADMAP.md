# Ghost Ship / Skyglass Project — full-manifest release roadmap

**Status:** ROADMAP ACTIVE; **83-node / six-ending Stage 1 structure director-approved** under RUL-2026-10-10-003 (2026-10-10). Stage 2 mechanics, final prose, art and full manifest remain pending. No live execution or publication authorization.  
**Repository baseline:** `perseverance484/tnr-tools@0eb57de20877d266dde666229ae4c68e8fbcf4c0` (verified 2026-10-10).  
**Lead:** Content Designer (ChatGPT); implementation: Fable / Claude Code after freeze; independent review: ChatGPT; all live-game requests/writes and publication: director/operator only.  
**Outcome:** one complete reproducible Ghost Ship release, with the two existing profession quests, six endings each, Skyglass retheme + expanded exploration, shared AI-pool migration, accepted art, and new reward loops. A combined Forge manifest is technically feasible; execution staging and cutover must be chosen separately.

**2026-10-11 independent readiness checkpoint:** `docs/reviews/GHOST_SHIP_SKYGLASS_STAGE2_READINESS_2026-10-11.md`. Stage 2 remains pending. Source review confirms the Crystal validator blocker and Katana source feasibility, identifies the missing full Legendary Sword capture, and specifies B32 ALL-method and migrated-Captain/innate-effect test requirements. This is review evidence, not in-process combat validation or a new ruling. The existing Stage 2 brief remains the governing offline test contract.

## Source/evidence hierarchy

- `docs/00_INDEX.md`, `docs/DOCTRINE.md`, `docs/ENGINE_LAWS.md`, `docs/RULINGS.md`, `CHATGPT.md`, `docs/DEVELOPMENT_WORKFLOW.md`.
- `state/ghost_ship_skyglass_reward_decisions.md` — operative 2026-10-10 director-approved Katana/Crystal numerical design and current hidden-state report; unresolved engine mappings kept explicit.
- `state/ghost_ship_skyglass_expansion_design.md` — **Stage 1 STRUCTURE APPROVED** for the 83-node six-ending quest (RUL-2026-10-10-003); new dialogue and choice prose remain draft.
- `state/ghost_ship_skyglass_graph_patch.json` — machine-readable **STRUCTURE APPROVED / PROSE DRAFT** patch containing 26 new nodes, 12 original forward-edge rewires, four new scene symbols and one Sealwright AI symbol. Not a Forge manifest.
- `state/ghost_ship_skyglass_sealwright_rule_contract.json` — source-backed **candidate** 7-jutsu exact AI rule plan with director-locked dual Clear and parity test matrix; no Forge live writes or implementation freeze.
- `docs/reviews/GHOST_SHIP_SEALWRIGHT_RULE_STATIC_CHECK.md` — 112/112 narrow source-key/priority static checks, 12 selection scenarios; deliberately NOT full game combat or true Captain-parity proof.
- `state/prompt_ghost_ship_skyglass_stage2_feasibility.md` — offline-only, Fable-owned research/test brief covering Sealwright parity, weapon-only Consume Crystal feasibility and Katana Legendary baseline. Not a game-write authorization.
- `state/ghost_ship_skyglass_sealwright_combat_draft.md` — **Director-accepted seven-jutsu kit and intentional double-Clear identity** (RUL-2026-10-10-006); S31 Unraveling Strike routinely strips removable buffs, B32 Nullifying Wave remains conditional on IDG above 70. Effective parity and final AI priority/positioning still require offline validation.
- `state/ghost_ship_retheme_design.md` — Skyglass lore, reveal cadence, named entities, rewards (original preserve-57 scope is now superseded for the expansion only).
- `state/ghost_ship_retheme_patch.json` — approved base 57-node text/identity/reward patch. Invariant to preserve all edges and count MUST be explicitly superseded by a versioned expansion; do not silently alter this base or treat it as the full release.
- `state/ghost_ship_shared_pool_migration.json` — approved shared AI kits and Core Rupture concept; no revival of 29 bespoke legacy jutsu.
- `harvests/inbox/tnr_results_1790826101573.json` — two full live quest records + out-of-scope Drowned Fleet.
- `harvests/inbox/tnr_results_1790826836406.json` — 11 directly wired AI records, 10 scene assets, item captures.
- `harvests/inbox/tnr_results_1790828718767.json` — 11 AI profiles + Crown record.
- `answers/names_item.json` / `harvests/seed/41_INDEX_item.json` — Night's Testament item id `osJq3k77YPGoFWgof12FQ` (catalog ID only, **not** a captured full stat record).
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
- Preserve 11 captured existing AI IDs and approved shared-pool combat roles; add **Sealwright** as the one new secret-route Captain-tier boss after combat design freeze. New shared `Core Rupture` for Seal Charge/Core Canister as approved if not already present. Unequip but do not delete retiring 37 legacy-only jutsu.
- Two quest records keep their IDs and profession-specific reward fields/coordinates except expressly approved changes. The approved graph is exactly **83 objectives per quest** (57 preserved + 26 additions, with 12 original forward-edge rewires). Six endings, with the secret archive route terminating exclusively at its own ending.
- Model B: exterior keel traversal, reconstruction chamber, quarantined archive/Sealwright secret branch, command observation gallery, deeper Wayfinder/Arsenal Keeper/First Blade interactions, visible failure-feedback dialogs, stronger Captain escalation.
- `Skyglass Serum` is the director-approved restorative rename; stale `Stillwater Tonic` prose in original patch is superseded.
- Existing Crown: `Fragment of the Skyglass Crown` = **20% Crowned Captain AI loot only**; remove the 10% `w_Co` quest roll; five fragments craft `The Skyglass Crown`; no direct Crown drop; no change to confirmed Crown mechanics; clear erroneous Captain equipment drops and the Diadem attachment.
- New **Legendary `Skyglass Katana`**: **3% independent Crowned Captain AI drop**; `itemType:WEAPON`, `weaponType:SWORD`, `canBeImbued:false`. Exactly three on-use effects: **50 EP Pierce** (`pierce(power:50)`), **2-round self Buff Prevent immunity** (`immunity(blocks:buffprevent,target:SELF,rounds:2)`), **40% Consume** (`consume(power:40,target:SELF)`, current generated shield duration defaults to 3 rounds). NO generic 30 EP Damage, NO separate 300 HP Shield, NO imbue slot. Earlier Night's Testament, shield-potency and 30-Damage/fixed-Shield designs are superseded. Remaining fields need a captured Legendary Sword baseline and director review.
- New `Skyglass Reliquary`: **one guaranteed chest for successful secret-route ending** (both professions). Director-approved proposed loot structure: guaranteed 1 Skyglass Filament + 3 Rare Jewels; independent chances 25% bonus Filament, 30% Skyglass Serum, 15% Ornate Chest, 3% Skyglass Crystal. No fragments or Katana in Reliquary.
- **`Skyglass Crystal`**: Ghost Ship-exclusive `CRYSTAL` imbuement, **weapon-only** (`crystalTargetTypes:WEAPON`) with **20% Consume as its only effect**. The independent 3% Reliquary direct drop and 12-Filament recipe are unchanged. This crystal cannot be used on Skyglass Katana (`canBeImbued:false`). Crystal rarity/trade and the Consume-only crystal validator/runtime blocker remain open. Do not add unapproved `damage`/`pierce` to make validation pass.
- No new cosmetic gear/Latticebound Guards, no generic new pirate jutsu, no automatic new loot family, no changes to independent quests.

## Entry/mutation inventory (planning estimate, not frozen)

| Type | Target logical records | Candidate count | Critical rule |
| --- | --- | ---: | --- |
| Shared AI jutsu | Core Rupture create if still absent | 1 | shared pool only; don't rename/delete legacy Explosion! |
| Existing scenes | 6 existing SCENE_BACKGROUND + 3 named SCENE_CHARACTER updates | 9 | reuse captured IDs; blank character unchanged |
| New scenes | 4 backgrounds + Sealwright scene portrait | 5 | create hidden; preserve lower-left overlay space |
| Existing items | Skyglass Serum, Crown Fragment, Crown edits | 3 | existing live IDs/mechanics preserved |
| New items | Reliquary, Filament, Crystal, Katana | 4 | full captured/template contracts; correct creation order |
| AI | 11 existing profile/kit/loot edits + 1 Sealwright create | 12 | capture full before images, rules embedded in AI entries |
| Quests | 2 full-record edits, existing quest IDs | 2 | preserve eligibility and all unaffected fields |
| **Total** | | **~36** | subject to contracts, status, new art, and final route spec |

Forge `forge/src/runner/refs.mjs` at base already supports `@item:`, `@ai:`, `@scene:`, `@jutsu:`, `@img:` with stable topological create ordering. A single combined full manifest can therefore reference a newly created Crystal/Filament inside the Reliquary table and a newly created Reliquary inside the quest. Fable must check release/current Forge behavior rather than assume old pipeline prose lists every ref.

## Stage 1 structural approval checkpoint (2026-10-10)

Stage 1 structure was **APPROVED by the director**, preserving the machine design proposal for prose refinement: `state/ghost_ship_skyglass_expansion_design.md` plus `state/ghost_ship_skyglass_graph_patch.json`. Both Gather and Hunt have been checked offline against the October 1 captured full objective graphs: **57 preserved nodes + 26 proposed additions = 83 nodes each**, **12 existing edge rewires**, **one root**, **all nodes reachable**, **six reachable endings**, **zero success/fail cycles**, **all 13 battle nodes dialog-gated**, and **no invented new map location tasks**. The secret route requires the hull/Core Horror and ends exclusively at `w_secret`; the direct Oathkeeper → Crowned Captain route still has two battles. The permanent original node IDs, AI opponent blocks, timed location mechanics, and original Gather/Hunt rewards are unchanged except where a later approved reward correction expressly applies.

**Director-approved structure (RUL-2026-10-10-003):** 83-node scope and optional dialog branches; wrong archive seal choice closes the secret route only for the current quest run; Sealwright as quarantine custodian and exclusive secret-route elite; single Reliquary sixth ending; short two-battle oathbound Crown route. **Still open:** final wording of new dialogue/choice text, exact Sealwright shared-pool AI combat profile and tuning, item-engine gates, art intake, and fresh hidden-state capture. These block the full manifest, not the accepted route structure.

## Stage 2 Sealwright kit accepted; exact combat implementation checks pending

**Director-approved two-Clear identity:** **S31 Unraveling Strike** regularly strips all removable positive buffs as a high-priority damaging attack; **B32 Nullifying Wave** is the seventh jutsu held for enemy IDG above 70. The overlap is INTENTIONAL (RUL-2026-10-10-006). B32 uses source-backed integer threshold 71; 100% Clear removes all removable positive effects, not IDG selectively. Its conditional rule must remain first and fall through when unavailable. **No jutsu may be deleted to remove the overlap.** Source-backed nine-rule positioning/behavior proposal: `state/ghost_ship_skyglass_sealwright_rule_contract.json` (not executable).



The director rejected the initial mid-tier Sealwright proposal and requested **meaningful boss-pool jutsu and practical parity with the regular Captain**. The October 1 full AI capture gives the regular Captain **Level 100/JONIN; 3.0× stats; 2.5× pools; 60 regeneration**. The revised candidate is at `state/ghost_ship_skyglass_sealwright_combat_draft.md` and uses that same starting profile, with **B14 Cataclysm Detonation** and **B16 Sovereign Fetters** as two genuine high-impact boss-pool signatures alongside **B22, B33, S27 and S31** for defense, piercing and suppression. The seven-technique roster is now the director-accepted design target, although precise AI rule priority and relative fight difficulty remain unvalidated; Fable must compare it against the Captain's migrated kit **B19/B14/B17/B05/S31/B33** and confirm Captain item eligibility before claiming parity. The older October 1 captured Captain's AI Heavy Armor and Cursed Dagger were both `equipped:NONE`; current game source does not activate their passive or weapon effects when unequipped, so do not invent extra Sealwright gear for parity. In particular, B16's combined 2-round Stun/Seal could make the fight too oppressive if AI priorities are careless. No custom jutsu, extra battle phases, or boss loot are implied. Do not translate this draft into an AI/quest manifest.

The Stage 2 technical remainder includes a source-verified Legendary Sword cooldown/cost/AP/range baseline, the new Katana's exact `pierce:50 EP + immunity(self buffprevent/2r) + consume:40%` offline test and `canBeImbued:false` guard, Crystal weapon-only **Consume 20%** record/runtime feasibility, Crystal rarity/trading, and a fresh operator-run hidden-state capture.

**Research handoff prepared:** `state/prompt_ghost_ship_skyglass_stage2_feasibility.md` now covers offline-only Fable-owned tests: (A) Sealwright AI/Captain parity; (B) weapon-only Crystal **Consume 20%** as its only effect; (C) Legendary Sword **50 EP Pierce + self Buff Prevent immunity/2 rounds + Consume 40%** (non-imbuable) with source-backed remaining baseline. No live-game requests/writes. The earlier Sealwright static validation passed 112 scoped assertions/12 scenarios, not the full combat engine.

## Roadmap / stage gates

| Stage | Owner | Deliverable | Acceptance gate |
| --- | --- | --- | --- |
| **0. Source and live-state reconciliation** | ChatGPT/Fable; director runs captures if required | Exact-SHA source map, latest read-only quest/AI/item captures with **hidden:true** readback and exact Legendary weapon stat baseline, existing art digest and route/loot deltas | No invented IDs or stale full-record edit baselines; zero changes to game |
| **1. Expansion structural freeze (APPROVED)** | ChatGPT + director | `state/ghost_ship_skyglass_expansion_design.md` + `state/ghost_ship_skyglass_graph_patch.json`; 83-node graph with six endings and 12 rewires | **Structure approved RUL-2026-10-10-003; final dialogue wording and Sealwright combat are separately pending.** |
| **2. Technical feasibility / reward freeze** | Fable source/contracts + ChatGPT independent audit; director rules | Sealwright/Captain parity tests; captured Legendary Sword baseline; non-imbuable Katana `pierce:50 EP` + `immunity blocks buffprevent SELF/2r` + `consume:40%` in-process tests; weapon-only Crystal `consume:20%` one-effect validity/runtime; item rarity/trade/recipes | No unresolved X, invented baseline, inert Consume or stealth bonus effects. Engine changes require separate director authorization/review |
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
3. **Legendary Sword baseline:** Night's Testament exact-copy plan is superseded. Katana is `WEAPON/SWORD`, `canBeImbued:false`, with exactly **Pierce 50 EP, self Buff Prevent immunity 2 rounds and Consume 40%**. Capture existing Legendary Sword comparator(s) for the exact remaining cooldown, AP, costs, range, target, method, slot and durability fields; obtain director acceptance. Night's Testament (`osJq3k77YPGoFWgof12FQ`) is an optional comparator, not mandated.
4. **Katana three-effect runtime verification:** Confirm `pierce(power:50)` produces the *only* authored damage effect and `consume(power:40)` converts the outgoing Pierce consequence into a temporary self shield (current default `shieldRounds:3`), rather than an authored fixed 300 HP shield. Include `immunity(blocks:buffprevent,rounds:2,target:SELF)` and `canBeImbued:false`. Verify 3-tag legality, source-validated field ordering, on-action timing, shielding, fresh-Buff-Prevent blocking, and inability to apply any crystal. No live combat experiments.
5. **Consume-only Crystal:** Director locks **20% Consume on a WEAPON-only CRYSTAL** with exactly one effect. `SuperRefineEffects` currently demands `damage` or `pierce` on that same item's effects array, so a Consume-only Crystal cannot validate even if its imbued weapon action later deals damage. Investigate offline; any targeted engine-source correction requires separate director authorization and independent review. Do not insert an extra 0/1-damage or pierce effect.
6. **Rarity/trade/occupation:** Current imbuing requires Crafting occupation and rank. Proposed Epic Crystal requires Master; users earning it on Gather/Hunt cannot imbue without occupation change or trading. Director must lock rarities, trading, and actual distribution.
7. **Farm economics:** Fragment 20%, Katana 3%, Reliquary guaranteed + Filament conversion and Crystal 3% require an intentional exception/explicit reconciliation against general anti-uncapped-rare reward guidance. Track expected drops per run and re-run variance.
8. **Shared AI dependencies:** Audit current usages of all 11 existing Ghost Ship AIs outside these two quest records and consider effects of new kits; Drowned Fleet untouched. All AI inventory dropChancePerc and equipped jutsu/rule orders verified independently.
9. **Art is not yet release-ready:** The nine processed ZIP assets are exact and hash-verified but not repo-pinned. Current selected Katana `1000018208.png` and Crystal `1000018205.png` are opaque RGB raw; process without altering accepted visual, QC dark background vs rarity frame, and pin immutable delivered bytes.
10. **Engine graph:** All dialogs need true choice targets; `start_battle` must be dialog-gated; no cycles except reset mechanism; visible feedback before reset; single start; all six ends reachable; every profession coordinate valid. `consecutiveObjectives:true` and complete quest update payloads are mandatory.

## Non-goals / prohibited actions during planning

No direct live-game requests or writes, no publication, no change to any active Fable branch, no automatic mass art generation, no immediate manifest, no Drowned Fleet changes, no retiring legacy jutsu deletion, no generic Skyglass lore alteration. Repository proposals remain unmerged until the director accepts design boundaries.

## Director-facing decision queue (do not fill in by convenience)

- The quest graph and **seven Sealwright techniques** are approved as design intent, including S31's routine Clear plus B32's IDG-threshold Clear. Do not treat them as redundant. **Still open:** source-checked rule positioning, comparative Captain parity and any director-signed test adjustments.
- **Resolved (RUL-2026-10-10-007):** Katana LEGENDARY WEAPON/SWORD, non-imbuable, **50 EP Pierce**, **self Buff Prevent immunity for 2 rounds**, **Consume 40%**. Crystal weapon-only **Consume 20%** as a single effect. Former Katana 30 EP Damage, 300 HP Shield and old Crystal Consume 30% are superseded. **Open:** Legendary Sword base values, source-backed in-process Katana proof, working one-tag Crystal validation/runtime path, Crystal rarity/trade and launch gates.
- Confirm Crystal rarity, tradeability, Filament tradeability, fixed Reliquary rewards, and unlimited-repeat chase policy.
- **Visibility:** director says both existing quests are currently hidden. Operator confirms with fresh captures; maintain hidden state during edits. Separate publishing decision remains open.

**Immediate next task:** Run Fable's revised offline-only Stage 2 test brief: Katana 50 EP Pierce + self Buff Prevent immunity/2 rounds + Consume 40% with no imbue slot; Crystal weapon-only single-tag Consume 20%; Sealwright Captain parity. Resolve source-verified Legendary Sword base fields and Crystal engine blocker, then independent exact-SHA review. No write manifest before director-owned balance, art and current-capture gates are satisfied.
