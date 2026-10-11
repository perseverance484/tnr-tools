# Ghost Ship / Skyglass Project — full-manifest release roadmap

**Status:** PROPOSED ROADMAP / director review required; no implementation freeze, live execution, or publication authorization.  
**Repository baseline:** `perseverance484/tnr-tools@0eb57de20877d266dde666229ae4c68e8fbcf4c0` (verified 2026-10-10).  
**Lead:** Content Designer (ChatGPT); implementation: Fable / Claude Code after freeze; independent review: ChatGPT; all live-game requests/writes and publication: director/operator only.  
**Outcome:** one complete reproducible Ghost Ship release, with the two existing profession quests, six endings each, Skyglass retheme + expanded exploration, shared AI-pool migration, accepted art, and new reward loops. A combined Forge manifest is technically feasible; execution staging and cutover must be chosen separately.

## Source/evidence hierarchy

- `docs/00_INDEX.md`, `docs/DOCTRINE.md`, `docs/ENGINE_LAWS.md`, `docs/RULINGS.md`, `CHATGPT.md`, `docs/DEVELOPMENT_WORKFLOW.md`.
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

Two existing public quests:
- Gather `6Ri-W5TtUrEMWpyYlnf_F`: `questType:gathering`, S-rank Gathering.
- Hunt `HckXVOf-qk6ESU9t5rxLh`: `questType:hunting`, A-rank Hunting.
- Each: 57 nodes (24 dialog, 12 start_battle, 14 reset, 2 collect_item, 5 win), `hidden:false`, `consecutiveObjectives:true`, `retryDelay:none`, `maxAttempts:1`, `maxCompletes:1`, top-level sceneBackground empty, 6 existing unique backgrounds and 3 named portraits. Gather/Hunt have reward and location differences. The caps are not reliably enforced for these profession quest types under the documented engine behavior.
- Entrances: gangplank / hull infiltration / Oathkeeper parley. Main branches: chart/cache / hold accessible / hold vault / normal Captain. Oathbound direct Crowned Captain shortcut is intentionally short for repeated fragment farming; **do not add mandatory detours**.
- Five existing ends `w_A, w_B1, w_B2, w_C, w_Co`. The expansion adds one mutually exclusive *secret* Reliquary ending per quest rather than an extra reward collected before continuing to Captain.
- Drowned Fleet is out of scope; preserve its records and check for any AI reuse before edits.

## Locked content goals / release scope

- Original fiction: airborne forbidden shinobi warship supported by a Skyglass Core/seal lattice; reconstructed chakra impressions, not undead; crew memory tragedy; original nine-beat reveal; Crowned Captain alone carries deepest terminated-mission failure truth.
- Preserve 11 captured existing AI IDs and approved shared-pool combat roles; add **Sealwright** as the one new secret-route elite after combat design freeze. New shared `Core Rupture` for Seal Charge/Core Canister as approved if not already present. Unequip but do not delete retiring 37 legacy-only jutsu.
- Two quest records keep their IDs and profession-specific reward fields/coordinates except expressly approved changes. Expand current graph (rough design estimate ~75–85 nodes per quest; count is not locked). Six endings, with any secret-route choice cutting off other endings.
- Model B: exterior keel traversal, reconstruction chamber, quarantined archive/Sealwright secret branch, command observation gallery, deeper Wayfinder/Arsenal Keeper/First Blade interactions, visible failure-feedback dialogs, stronger Captain escalation.
- `Skyglass Serum` is the director-approved restorative rename; stale `Stillwater Tonic` prose in original patch is superseded.
- Existing Crown: `Fragment of the Skyglass Crown` = **20% Crowned Captain AI loot only**; remove the 10% `w_Co` quest roll; five fragments craft `The Skyglass Crown`; no direct Crown drop; no change to confirmed Crown mechanics; clear erroneous Captain equipment drops and the Diadem attachment.
- New `Skyglass Katana`: **3% independent Crowned Captain AI drop**, exact full stat template of Night's Testament **except** remove imbue capability and add shield potency `+X` (value/engine representation pending). Retheme/clone; never edit Night's Testament.
- New `Skyglass Reliquary`: **one guaranteed chest for successful secret-route ending** (both professions). Director-approved proposed loot structure: guaranteed 1 Skyglass Filament + 3 Rare Jewels; independent chances 25% bonus Filament, 30% Skyglass Serum, 15% Ornate Chest, 3% Skyglass Crystal. No fragments or Katana in Reliquary.
- `Skyglass Crystal`: Ghost Ship-exclusive equipment imbue, currently envisioned as weapon-targeted Consume `+X%`, 3-round generated shield; 12 exclusive Skyglass Filaments craft 1 Crystal. Crystal and Filament originate only via the Ghost Ship loop. Exact Consume legality, scaling, target, rarity and trade policy require contract tests/explicit director lock. Do not silently create a nonfunctional passive imbue.
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

## Roadmap / stage gates

| Stage | Owner | Deliverable | Acceptance gate |
| --- | --- | --- | --- |
| **0. Source and live-state reconciliation** | ChatGPT/Fable; director runs captures if required | Exact-SHA source map, latest read-only quest/AI/item captures, Night's Testament full `item.get`, existing art digest and route/loot deltas | No invented IDs or stale full-record edit baselines; zero changes to game |
| **1. Expansion content freeze** | ChatGPT + director | Versioned `state/ghost_ship_skyglass_expansion_design.md` and machine objective graph patch for Gather/Hunt; node IDs, types, every choice/fail/reset, all six endpoints, dialogue, new coordinates/scene assignments | Director approves route choices, Sealwright characterization and combat difficulty; oathbound two-battle shortcut preserved; one-end-per-run |
| **2. Technical feasibility / reward freeze** | Fable source/contracts + ChatGPT independent audit; director rules | Captured Night's Testament stat template; exact Katana clone delta and shield-potency mechanic; tested Consume crystal carrier/activation; item rarities/trade/recipe/rates; new Sealwright kit/profile | No X in released records; no unproven shield potency or inert Consume; if engine changes needed, split Lane A and review before content manifest |
| **3. Art intake + completion** | ChatGPT Art Director/Image Production + director QC | Commit/cache exact 9 processed approved assets and selected new raw sources with provenance, finish remaining art and deliver preflight-valid WebPs + SHA/filename ledger | ~25 remaining deliverables from prior plan including Katana; selected Crystal and Katana designs stay locked; content-specific scene wiring checks, all under art spec ceilings |
| **4. Full compile and dry-run** | Fable | Versioned combined Forge manifest + generator if appropriate, `imagePack` pinned to immutable repo art commit, full after-captures, reproducible package and operation census | All refs resolved, full-field/schema and graph validation 0 errors, no duplicate create, all assets/IDs known, order and runner tests pass |
| **5. Independent frozen-SHA audit** | ChatGPT | Report against exact Fable handoff SHA plus test evidence | Audit graph reachability, 6 endings, profession parity, loot math, Cobra/Captain regression, shared pool migration, source diffs, image digests, no public exposure/secret writes; blockers closed |
| **6. Operator-controlled production preparation** | director/operator only | Approved maintenance/publish plan; latest before-state and explicit rollback/recovery checklist | The existing quests are `hidden:false`: choose safe cutover (e.g. operator-controlled temporary hide/maintenance and active-quest implications). Never update public quests or shared AI accidentally while expecting hidden tests |
| **7. User-run execution + read-back** | director/operator only; Fable/ChatGPT read evidence afterward | Complete Forge result, idmap, full record after-captures, mismatch/diff report; defer public publish until separate approval | New content created hidden; no unresolved partial writes; public quests not unhidden by agents; exact AI drop rates/recipes/scene refs/art bytes verified |
| **8. Publication + post-launch** | director/operator only | Explicit publish decision, operational closeout, return to current-state capture, archive spent manifests | No publication without separate user authorization, rollback available, old quest continuity and farm route verified |

### Sequence and likely parallelism

- Stage 0 and preparatory art SHA intake can begin before full narrative freeze. Do **not** begin mass new art until target rooms and dialogues are frozen.
- Stage 1 (graph) and Stage 2 (mechanics) can run in separate contexts, then converge at a director content/reward freeze. Art generation uses the frozen visual list one asset at a time.
- Full compile depends on all new/updated entities and art (Stages 1–3). Frozen-SHA review follows compile; no further edits on Fable's frozen branch until review returns.
- Stage 6 is a separately approved **live production cutover**. A monolithic manifest is a compilation deliverable, not authority to execute it. If executing a monolith risks partial publication or rate-limit recovery, Fable may propose dependency-safe sub-manifests with a single release specification, but the user decides launch structure.

## Production safety and mechanical blockers

1. **Public in-place quest edit:** Both current profession quests were captured with `hidden:false`. Rewriting the graph while public can expose unfinished routes and affect active trackers. Hiding an active public quest may prune players' active instances. Director must choose cutover timing and approve the production impact.
2. **Outdated retheme invariant:** `state/ghost_ship_retheme_patch.json` says preserve 57 objectives/edges. Model B explicitly supersedes that constraint while inheriting unchanged lore/IDs/combat foundations; version a new patch with explicit diffs.
3. **Night's Testament:** `osJq3k77YPGoFWgof12FQ` is catalog-resolved, but full mechanics are not in the specified Ghost Ship captures. Need full `item.get` and compare every field, copy not infer.
4. **Shield potency:** The pinned `45c_DATA_constructors.json` tag list includes `shield` but has no standalone `shieldpotency` effect. Resolve what the director means mechanically; do not swap to a generic shield or invent a tag.
5. **Consume on Crystal:** `SuperRefineEffects` requires `consume` alongside damage/pierce on the same action, while passive equipment imbue effects may never activate action-time Consume. Require focused in-process source tests, or separately authorized Lane A upstream change; no live experiment without director.
6. **Rarity/trade/occupation:** Current imbuing requires Crafting occupation and rank. Proposed Epic Crystal requires Master; users earning it on Gather/Hunt cannot imbue without occupation change or trading. Director must lock rarities, trading, and actual distribution.
7. **Farm economics:** Fragment 20%, Katana 3%, Reliquary guaranteed + Filament conversion and Crystal 3% require an intentional exception/explicit reconciliation against general anti-uncapped-rare reward guidance. Track expected drops per run and re-run variance.
8. **Shared AI dependencies:** Audit current usages of all 11 existing Ghost Ship AIs outside these two quest records and consider effects of new kits; Drowned Fleet untouched. All AI inventory dropChancePerc and equipped jutsu/rule orders verified independently.
9. **Art is not yet release-ready:** The nine processed ZIP assets are exact and hash-verified but not repo-pinned. Current selected Katana `1000018208.png` and Crystal `1000018205.png` are opaque RGB raw; process without altering accepted visual, QC dark background vs rarity frame, and pin immutable delivered bytes.
10. **Engine graph:** All dialogs need true choice targets; `start_battle` must be dialog-gated; no cycles except reset mechanism; visible feedback before reset; single start; all six ends reachable; every profession coordinate valid. `consecutiveObjectives:true` and complete quest update payloads are mandatory.

## Non-goals / prohibited actions during planning

No direct live-game requests or writes, no publication, no change to any active Fable branch, no automatic mass art generation, no immediate manifest, no Drowned Fleet changes, no retiring legacy jutsu deletion, no generic Skyglass lore alteration. Repository proposals remain unmerged until the director accepts design boundaries.

## Director-facing decision queue (do not fill in by convenience)

- Freeze the sixth route's exact choices, Sealwright encounter/AI tuning, and whether optional First Blade/Wayfinder/Arsenal Keeper portraits enter scope.
- Confirm mechanics and `X` values for Skyglass Katana shield potency and Skyglass Crystal Consume, with source-backed working implementations.
- Confirm Crystal rarity, tradeability, Filament tradeability, fixed Reliquary rewards, and unlimited-repeat chase policy.
- Approve public-quest maintenance/cutover plan and separate publish timing.

**Immediate next task:** prepare the expansion graph and exact reward/mechanical decision sheet (not the manifest), then seek director approval before downstream implementation.
