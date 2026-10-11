# Fable start — Ghost Ship / Skyglass Stage 2 offline validation

**Item-package supersession — RUL-2026-10-11-005:** The item inputs below describe historical r4 work. The next item task is `state/prompt_ghost_ship_skyglass_consume_revalidation.md`: Katana15 / Crystal10 with active Consume. Approved combat scope is unchanged; historical item rates and instant timing are not current construction authority.

**Task:** Execute the accepted Ghost Ship technical test work, produce reproducible evidence and return a frozen exact-SHA handoff for ChatGPT's independent review. Do not begin another kit-selection round.

**Owner:** Fable / Claude Code implements the offline harness/tests on a separate owned branch. ChatGPT reviews. dauntless retains balance, art, item economics, engine-change, final content and live-game authority.

**Status:** READY FOR OFFLINE TEST WORK. Full release validation remains partly blocked by the Sword baseline and Crystal engine support. No live-game requests/writes, credentials, asset-CDN calls, engine modifications, art changes, publication or full write manifest.

## Recover the exact design input

- Repository: `perseverance484/tnr-tools`.
- Main verified 2026-10-11: `0eb57de20877d266dde666229ae4c68e8fbcf4c0`; verify again before work.
- Original remote design head: `0dbd54c04f2025a1a652712a9ea6df94e35cf8f5` on `chatgpt/ghost-ship-skyglass-manifest-roadmap`. This alone omits the later approvals.
- Accepted hybrid-kit proposal: `89fa921c839a9830fd66bb64aa267c470e8dd678`.
- Current input branch: `chatgpt/ghost-ship-stage2-review-20261011`; use the exact complete handoff SHA in the delivery envelope, which includes this file and `RUL-2026-10-11-003`. If delivered as a Git bundle, follow its START_HERE instructions and verify the SHA. Do not assume this branch was published remotely.
- Suggested new implementation branch: `fable/ghost-ship-skyglass-stage2-offline`. If already owned/active, choose another Fable-owned branch; do not alter someone else's worktree.
- Do not write to either ChatGPT branch. Base the test branch on the complete handoff commit, or explicitly reconcile its design inputs onto a newer baseline without dropping approvals.

Initialize from `CLAUDE.md`, `CHATGPT.md`, `docs/00_INDEX.md`, doctrine, relevant engine laws, agent/workflow instructions and current task sources. The global September Forge status projection is not the Ghost Ship workstream's current state.

**Exact governing test brief:** `state/prompt_ghost_ship_skyglass_stage2_feasibility.md`. This start packet clarifies accepted inputs, execution sequence and evidence boundaries; it does not replace the approved numerical contracts in that brief.

Required additional inputs:

- `state/ghost_ship_hybrid_kit_proposal.json` / `.md`: **accepted** memberships and mappings under their stable historical filenames. Display order is not rule order.
- `state/ghost_ship_legacy_jutsu_conversion.json`: eleven unchanged mechanical records, source pointers and protected-field hashes; only presentation edits are authored.
- `state/ghost_ship_skyglass_sealwright_rule_contract.json` and combat draft: approved seven-move identity with candidate rules, not a validated rule freeze.
- `state/ghost_ship_skyglass_reward_decisions.md`: latest Katana/Crystal and reward authority.
- `docs/reviews/GHOST_SHIP_SKYGLASS_STAGE2_READINESS_2026-10-11.md`: source findings, amended five-move comparator and unresolved evidence gates.
- Full AI, profile and shared-pool captures: `harvests/inbox/tnr_results_1790826836406.json`, `tnr_results_1790828718767.json`, `tnr_results_1791583362574.json` respectively, all under `harvests/inbox/`.
- Approved quest structure and graph, retheme and ruling ledger. The old all-shared migration is historical evidence with an override, not an alternative accepted kit.

## Accepted input boundary

RUL-2026-10-11-003 accepts **all eleven kits: 65 memberships, eleven retained legacy IDs and eighteen shared IDs**. This includes Sentinel's Rigging Snare/Hollow Timber reuse, First Blade's EL04, all disclosed substitutions/consolidations and their element/power/cadence tradeoffs. Preserve complete AI numeric profiles and innate effects, including duplicate entries. No compensating stat buffs or retained-jutsu tuning are authorized.

The **regular Captain** is the parity comparator and keeps five moves: Unbroken Command, Remembered Form, Keelbind, B14 and B17. Preserve its innate Highest-offense/general Stat30%/99r and captured preferences. Its unequipped armor/dagger do not become active equipment. The old B19/B14/B17/B05/S31/B33 comparator is superseded.

Crowned Captain keeps eleven moves with Sharpened Focus replaced by EA03. Equipped Second Wind, Stolen Form and Rebounding Form are not explicitly selected in its captured rules. Preserve that distinction: separately report any proposed active support rotation and do not treat membership approval as behavior approval.

Sealwright retains **B22/B16/B14/B33/S27/S31/B32**. S31 is routine high-priority damaging Clear. B32 is conditional-only, IDG threshold71 and CLOSEST_OPPONENT distance gate6; the jutsu itself is **ALL method**. The gate controls triggering, not the set of possible Clear recipients. Deliberate double Clear is approved. Final ordering/proactive closing and measured parity remain open.

Katana is exactly LEGENDARY WEAPON/SWORD, `canBeImbued:false`, Pierce50 EP + SELF Buff Prevent immunity2r + Consume40%. Crystal is WEAPON-only CRYSTAL with Consume20% as its only effect. Do not add filler Damage/Pierce or redesign either item to bypass a validator.

## Execution and evidence sequence

Use one coherent initial engine execution pin: `studie-tech/TheNinjaRPG@cddd7d91c9e6bdebc978ddcb61e5b8a305bd0f93`. Record runtime/dependency versions and provenance. Assess relevant differences from historical AI pin `4774560eb6e8c9a5ef156d66b953dcb6aeeba4d6` and the readiness review's observed later source; do not mix them silently or call upstream HEAD the deployed version.

Keep harness/tests in the Fable-owned TNR branch, using immutable source imports or an isolated source checkout. In-process test execution is authorized; starting the game server, connecting to a live database/API or modifying upstream engine code is not. Fixtures must run without live credentials or game-network access. Record any unavailable dependency/environment as BLOCKED rather than substituting a hand-written model for actual-engine proof.

| Gate | Work | Evidence / limitation |
| --- | --- | --- |
| M0 | Verify source-file hashes, all 65 memberships, selected full records, retained protected-field hashes, AI/profile pointers, innate arrays and missing/null distinctions. | Committed deterministic fixture checks. Do not normalize older records to look schema-current. |
| A1 | Actual AI/action tests for all eleven accepted kits: availability, cooldown gaps, attack/stance cadence, resources, targeting, idle/fallback behavior and hazards. | Compare captured profiles with candidate rebuilt rules; keep kit changes separate from rule changes. No AI-exhaustion failures or silent stat compensation. |
| A2 | Actual Sealwright AI selection and full combat comparison against the accepted regular Captain. | Include the brief's threshold/targeting/Clear/control/positioning matrix and representative player fixtures; report measurements, not parity from equal multipliers. |
| B1 | Parse Consume20-only through the actual item effects schema and reproduce rejection. | Exact validator issues and passing negative test. Production Crystal validity stays BLOCKED. |
| B2 | Exercise actual weapon-plus-imbuement effect composition and Consume20 runtime, including shields/multiple targets/stacking/no-damage recipient. | A manually merged fixture proves post-merge runtime only; distinguish it from inventory/composition integration. No validator bypass becomes production approval. |
| B3 | Test WEAPON restriction, non-imbuable recipients, duplicate crystal rejection and suppression of old imbuements; verify Crafting/rank constraints. | Separate runtime guards from unselected rarity/trading policy. |
| C1 | Parse the exact Pierce50 + self immunity2r + Consume40 array through the real item effects validator. Check minimum-one `maxImbueNumber` separately. | Effect-array PASS is not full-item PASS; imbuing is disabled by `canBeImbued:false`. |
| C2 | Actual Pierce-to-Consume shield generation, pre-shield basis, aggregation, expiry, player item-level scaling and immunity timing. | Use sourced fixture carriers; prove existing Buff Prevent is not cleared and new applications are blocked only during immunity. |
| C3 | Validate the complete final Katana record and exact AP/pools/range/target/CD/GCD/requirements/economy. | BLOCKED until a qualifying full Legendary Sword capture and director baseline acceptance. Do not invent final fields. |

No baseline capture is needed to begin M0/A1/A2/B1/B2/B3/C1/C2. Use named upstream helper defaults or captured records as **test carriers**, with exact values and provenance; they are not a recommendation for Katana's unselected fields. General cooldown experiments may run, but final Katana cadence remains a C3 question.

A1 must preserve Explosion's original ID,100AP self-destruct and delayed triggers >2 / >6 for the two hazards. Prove waiting and safe fallback behavior. Keep retained and shared records exactly as sourced; smaller generic attacks do not justify silent AI-stat changes.

A2 must include IDG69/70/70.5/71/90, B32 unavailable, distance boundaries, closest summons versus farther buffed players, ALL recipients, new/inactive/protected buffs, Clear Prevent and protected source effects. Demonstrate routine S31 and conditional-only B32, B16 control duration,40+60AP capacity and optional closing-rule alternatives. Use the same player inputs/seeds for both bosses. Report wins/losses, duration, spikes, action lockout, recovery windows, pool pressure, buff/shield uptime and Clear frequency. No numeric parity tolerance has been approved; provide evidence for director acceptance.

If Crystal support requires an upstream change, deliver a minimal **separate Lane A proposal**, with failing reproducer and required regression coverage. Do not implement it. Preserve companion validation for ordinary weapons/jutsu/bloodlines and other recipient types, including Vamp/Wound checks.

## Capture and decision boundary

No agent live capture is authorized. The first suggested Sword record for a future operator-supplied full capture is Night's Testament `osJq3k77YPGoFWgof12FQ`; its catalog entry does not prove SWORD or any numeric baseline. If unsuitable, alternatives remain those named in the readiness review. Do not pause independent test gates while waiting for this record.

Remaining director decisions: final tested AI priorities/parity and any tuning changes; Crowned support activation; exact Sword baseline; Crystal rarity/trading/crafting accessibility and related item economic fields; any separately proposed engine correction; final prose/art and eventual release. Approved item effects, quantities, graph and reward loops are not reopened.

## Required return

- Repository/branch/base/head, exact frozen SHA and integration target; verify the remote return head when publishing the Fable handoff under the normal workflow.
- Committed test/harness sources and fixture provenance, exact engine/dependency pins, commands, results and relevant logs/traces sufficient for independent reproduction.
- PASS/BLOCKED per **M0/A1/A2/B1/B2/B3/C1/C2/C3**, with overall package status. A passing expected-rejection test does not make Crystal production-compatible; passing C1/C2 does not unblock C3.
- Separate captured-baseline versus rebuilt-rule outcomes and an explicit ledger of proposed behavior/tuning changes. Include original-versus-candidate Crowned support behavior.
- Report what the harness actually executed. A static selector model or cited upstream test count is not full combat evidence.
- Remaining director-owned decisions and any narrow operator capture request; no fake values or silent fallbacks.
- Explicit counters: live-game requests0, writes0, credentials none, with upstream engine working tree unchanged. No art, full manifest or publication work.

Return the frozen handoff to dauntless for ChatGPT's independent review. This packet has not dispatched a message or started a Fable implementation session.
