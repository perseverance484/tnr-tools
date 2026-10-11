# Ghost Ship Skyglass Project — Stage 2 source-backed feasibility and parity brief

**2026-10-11 accepted combat baseline — RUL-2026-10-11-003:** The eleven retained legacy jutsu and all eleven hybrid enemy kits are accepted for offline tests. Read `state/ghost_ship_hybrid_kit_proposal.md` / `.json`; historical filenames/JSON keys remain stable but membership is approved. The regular-Captain comparator is its five captured moves: Unbroken Command, Remembered Form, Keelbind, B14 and B17. Preserve all retained mechanics and original IDs. Exact rule behavior and measured parity remain pending. Sealwright's seven jutsu and item packages B/C remain unchanged; no engine modification or full manifest is authorized.

**Accepted substitutions:** Crowned Captain keeps ten moves and replaces Sharpened Focus with EA03; Sentinel gains Rigging Snare/Hollow Timber; First Blade uses EL04 Ion Lance; all other substitutions/consolidations are those accepted from `89fa921c839a9830fd66bb64aa267c470e8dd678`. Source pointers, full-record hashes and innate-effect preservation are in the kit packet. Kit order is not rule priority. Do not silently activate Crowned Captain's equipped but unselected heal/copy/reflect support. Execution entry point: `state/prompt_ghost_ship_skyglass_stage2_start.md`.

**Status:** READY FOR FABLE OFFLINE RESEARCH / TEST WORK ON SEPARATE OWNED BRANCH — **NOT** production-content authorization.  
**Issued:** 2026-10-10  
**Repository:** `perseverance484/tnr-tools`; baseline main `0eb57de20877d266dde666229ae4c68e8fbcf4c0` (recheck head).  
**Authoritative design:** Use the complete handoff commit identified by the delivery envelope, inheriting frozen design `0dbd54c04f2025a1a652712a9ea6df94e35cf8f5` plus later rulings through `RUL-2026-10-11-003`. The approved kit proposal is anchored at `89fa921c839a9830fd66bb64aa267c470e8dd678`. Do not use the older remote design head alone or write to ChatGPT's branch.
**Roles:** Fable = technical implementation/architecture owner for offline tests and tools; ChatGPT = independent frozen-SHA reviewer; director = all combat/balance/rewards/engine-change/live-game/publishing decisions.  
**Live-game requests/writes:** ZERO. No operator credentials. No actual site interactions, asset-CDN fetches, game updates or publishes.

## Inputs to read before work

- `docs/00_INDEX.md`, `docs/DOCTRINE.md`, `docs/ENGINE_LAWS.md`, `docs/RULINGS.md`, `CHATGPT.md`, `docs/DEVELOPMENT_WORKFLOW.md`, `docs/agents/README.md`, `docs/agents/ENGINEERING_AUDITOR.md`, `docs/workflows/CONTENT_WORKSTREAM.md`.
- `state/ghost_ship_skyglass_expansion_design.md` and `state/ghost_ship_skyglass_graph_patch.json`: **approved 83-node structure**, not a request to edit quests.
- `state/ghost_ship_skyglass_sealwright_combat_draft.md`, `state/ghost_ship_skyglass_sealwright_rule_contract.json`, and `docs/reviews/GHOST_SHIP_SEALWRIGHT_RULE_STATIC_CHECK.md`.
- `state/ghost_ship_hybrid_kit_proposal.json` / `.md`, `state/ghost_ship_legacy_jutsu_conversion.json`, and `docs/reviews/GHOST_SHIP_SKYGLASS_STAGE2_READINESS_2026-10-11.md`. The older all-shared migration is historical, not a final kit map.
- `state/ghost_ship_skyglass_reward_decisions.md`, `state/ghost_ship_shared_pool_migration.json`, `skills/building-tnr-content/data/32b_DATA_pool.json`, `harvests/inbox/tnr_results_1790826836406.json`, `harvests/inbox/tnr_results_1790828718767.json`.
- Current/pinned `studie-tech/TheNinjaRPG` source, especially `app/src/libs/combat/ai_v2.ts`, `app/src/validators/ai.ts`, `app/src/validators/combat.ts`, `app/src/libs/combat/actions.ts`, `app/src/libs/combat/tags.ts`, `app/src/libs/combat/process.ts`, `app/src/server/api/routers/combat.ts`, `app/src/server/api/routers/occupation.ts`.

## Work package A — Sealwright AI behavior and regular-Captain parity

**Director-locked:** Seven shared-pool jutsu: B22 Compression Barrier, B16 Sovereign Fetters, B14 Cataclysm Detonation, B33 Piercing Judgment, S27 Weakening Strike, **S31 Unraveling Strike** (routine high-priority 40 Damage + 100% Clear) and **B32 Nullifying Wave** (seventh jutsu, conditional-only 100% Clear when targeted opponent **IDG >70**). Overlapping Clears are **intentional and desired**. Do not deduplicate S31/B32, nor convert B32 to unconditional filler. B32 current-schema rule uses `target_has_effect(increasedamagegiven, CLOSEST_OPPONENT, threshold:71)` AND `distance_lower_than(CLOSEST_OPPONENT, value:6)`; `use_specific_jutsu` ID `JWZYiHKPNwYziWEFjw4Fn`. Use only existing shared IDs, no new custom jutsu.

**Parity target:** regular Captain Level 100/JONIN, 3× stats, 2.5× pools, regeneration 60. This is a **starting candidate**, not a measured equality. October 1 capture shows Captain inventory AI Heavy Armor and Cursed Dagger **both equipped:NONE**, so engine passive armor and item action filters don't apply them to ordinary fights. Refresh via operator-provided capture if current state may differ, no agent live query.

**Required offline proofs:** validate complete AiProfile field grammar, jutsu ID refs, gates/ranges, 40+60 AP cadence, and no exhaustion; execute actual in-process AI selection/combat tests (not only the small static priority model) for IDG 69/70/70.5/71/90; B32 unavailable, in/out of range, multi-opponent/summon targeting; S31 firing routinely when ready; Clear/clearprevent interactions; mixed control from B16 2r stun+seal. Compare a representative player-fixture matrix against the regular Captain: turns to victory/loss, control lockout rounds, damage spikes, shield uptime, buff uptime/clear frequency, pool pressure and counterplay. Show source/pin/test command/results. Do not silently weaken a director-chosen move; present tuning conflicts for the director.

**Candidate movement:** Design contract includes a proactive closing rule for S31's shorter range 3. That exact positioning order is not yet approved; test alternatives with/without it and quantify effects before freezing the rule array. Preserve the director's core mechanic either way.

## Work package B — Crystal weapon-only 20% Consume feasibility

**Director-locked revised specification (RUL-2026-10-10-007):** Skyglass Crystal is a weapon-targeted `CRYSTAL` imbuement with **20% Consume as its only effect**, not 30%. Use `crystalTargetTypes:"WEAPON"`. Engine's Consume default generated shield duration is currently 3 rounds (not separately director-specified). No separately authored damage/pierce or placeholder tag is approved. The Reliquary's 3% direct Crystal chance and 12-Filament crafting progression are unchanged. A WEAPON item with `canBeImbued:false`—including Skyglass Katana—is not a valid recipient; test this explicitly.

**Known source blocker:** `app/src/validators/combat.ts` item effects are validated with `SuperRefineEffects`, which rejects a Consume tag unless Damage/Pierce is present on the **same item effects array**. A Consume-only Crystal currently cannot pass that check. On the other hand, `app/src/server/api/routers/combat.ts` composes `ui.item.effects + imbuement.item.effects` for a weapon's action, and `app/src/libs/combat/tags.ts` computes Consume only when an effect is both `isNew` and `castThisRound` on positive outgoing damage. This suggests a potential **narrow CRYSTAL/WEAPON validator-specific correction**, but validity of the combined action and 20% shield generation remains **UNPROVEN**. A validator exception alone cannot establish correct runtime behavior. Research whether schema plumbing can safely allow weapon-only Consume-only crystals without relaxing general Consume+Damage law for jutsus/items/bloodlines, and whether resulting weapon attacks actually generate the intended self-shield across normal damage, shielded damage, and multi-target cases. If upstream game-code changes are necessary, write a minimal test-backed separate-Lane-A proposal; DO NOT modify game source or weaken validator without explicit authorization.

**Occupation/rank:** check Crafting-only imbuement, crystal rarity Master/other thresholds, tradability and inability of Gather/Hunt players to imbue unless craft-occupation constraints allow; present director-owned options, don't decide.

## Work package C — Skyglass Katana non-imbuable Legendary Sword

**Director-locked revised contract (RUL-2026-10-10-007):** Skyglass Katana is LEGENDARY, `itemType:WEAPON`, `weaponType:SWORD`, `canBeImbued:false`. It has EXACTLY THREE authored effects on attack: **Pierce 50 EP** (one `pierce(power:50)`, NOT a separate `damage` tag), **self Buff Prevent Immunity for 2 rounds** (one `immunity(blocks:buffprevent,rounds:2,target:SELF)`), and **40% Consume** (one `consume(power:40,calculation:percentage,target:SELF)`, `shieldRounds` source default currently 3). This supersedes ALL earlier Katana variants: no ordinary Damage 30 EP, no fixed 300 HP Shield/2 rounds, no shield-potency rider, and no permission to imbue it.

**Drop unchanged:** Crowned Captain **3% independent AI Katana drop** alongside a **20% independent Crown Fragment drop**. No Katana in quest-completion or Reliquary chest rewards.

**Source-based feasibility:** `SuperRefineEffects` accepts Consume when the **same weapon item's effects array** also has Pierce. `tags.damageUser()` emits the normal `Consequence.damage` for a cast-round Pierce effect; `forEachOutgoingDamage()` inside Consume looks for the same actor's positive outgoing `damage` consequence and sets Consume ratio/rounds. This makes the Katana's Pierce+Consume design source-plausible but is NOT yet a passing in-process item validation/combat fixture.

**Tests:** verify actual parsed three-effect WEAPON/SWORD, `canBeImbued:false` and `maxImbueNumber` schema guard (minimum 1 means setting 0 to disable is invalid); Pierce 50 EP weapon action scaling/target/range; Consume 40% converts outgoing Pierce damage into an actual temporary self shield in the same cast, including shielded/pierced and multi-target cases; self immunity only prevents **new** Buff Prevent effects for two rounds; cooldown, GCD, AP/pools and interaction with any already-existing player imbuements; inability to apply the Skyglass Crystal or any crystal to this Katana. Do not copy attributes from a named weapon without reading its actual record.

**Remaining baseline fields:** Source-verify a comparable LEGENDARY **Sword** full item record for AP, cooldown, pool/health costs and per-level reducers, action target/range/method, equip slot, durability, requirements, trade/economy and all server-required fields. Night's Testament `osJq3k77YPGoFWgof12FQ` may be a comparator but exact-copy requirement is superseded. If no recent full copy is in committed captures, request a narrow **operator-run read-only `item.get` capture**, never a live agent query. Director accepts exact baseline values before release manifest freeze.

## Art, rewards, quest safety

No art generation, uploads or processing in this packet. No quest/AI/item edits; no manifest assembly or production test run. Preserve the approved 83-node graph and six endings; preserve the Crowned Captain's short two-battle route, 20% fragment + 3% Katana independent AI drops, and secret-route guaranteed Reliquary. Do not publish/unhide either profession quest. Existing quests are reported hidden by the director; old `hidden:false` capture is stale for visibility.

## Expected Fable deliverable and review gate

- One durable, exact-SHA **offline feasibility report** with source code/test evidence, PASS/BLOCKED per package and list of unresolved user-owned choices.
- Actual automated/in-process tests for AI rules where feasible and reproducer for item effect/crystal validator behavior; output commands and results, not only narrative.
- Explicit engine-change requirement **if and only if** confirmed by tests. Keep proposed patches segregated for prior authorization, never sneak changes into a content manifest.
- Pin implementation/review SHA and provide compact fielded handoff to ChatGPT for independent review. No source/tool/engine changes in the game, no live requests/writes or credentials.

**Next project gate:** director reviews any balance/rarity/engine-dependency decisions; then author the full frozen content implementation brief and move to Fable's normal Forge manifest build with accepted art and fresh operator captures.
