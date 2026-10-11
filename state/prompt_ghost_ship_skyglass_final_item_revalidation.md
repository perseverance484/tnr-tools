# Fable brief — final Skyglass 2/2 Consume items

**Authority:** RUL-2026-10-11-006 and `state/ghost_ship_skyglass_reward_decisions.md`; machine-readable design: `state/ghost_ship_skyglass_final_item_contract.json`. This brief supersedes the unresolved timing/economy instructions in `state/prompt_ghost_ship_skyglass_consume_revalidation.md`. That historical brief and its tests remain evidence for their original scope.

**Approved:** Katana15 and Crystal10 both use `rounds:2`, `shieldRounds:2`. Crystal is LEGENDARY, `canBeTraded:true`, `canBeCrafted:false`; remove the 12-Filament recipe from new construction. Keep independent 3% drops and the complete Reliquary table. Filament trading/replacement use is not decided. Consume overlap is explicitly deferred and does not block this pass; no overlap fix or additional policy is requested.

**Inputs:** frozen r4 `3f825562ea051306a3803f47428b742ae5100011`; passing 3/3 active-Consume package `fcd79e5a3401dc8d95abbdaa05d0d4664c04a6e2` (local/bundle delivery, not on main at this brief's creation); engine `585534d7eb21d6f0dd678d5c3eb92662f611d39b` (upstream, deployment unverified). Verify refs before work. Use a new Fable-owned branch; do not edit frozen review targets.

## Bounded implementation

1. Version the derived item records/builder/tests deliberately. Preserve the old r4 and 3/3 packages at their frozen SHAs; do not relabel historical PASS as final 2/2 evidence. Retain exact provenance and source-file integrity checks.
2. Derive Katana from the accepted Night's Testament capture and RUL004/005/006 overrides. Derive a complete Crystal candidate with the approved rarity/trade/craft flags, exactly one Consume tag and WEAPON-only target. Ensure no craft requirements or recipe remain operative; verify source-required inert crafting fields without inventing reward values. Keep unapproved presentation fields explicit.
3. Validate exact effects and full records with pinned engine validators. Recheck activation, granting and later hits, final eligible hit and first ineligible hit, independent per-shield expiry and surviving shields after buff expiry, removal by Clear, and Katana immunity. Verify exact `rounds:2`/`shieldRounds:2` progression using engine round advancement. Preserve rate, cost, cooldown, targeting and non-imbuable invariants.
4. Recheck Legendary Crystal native imbuement eligibility, WEAPON-only recipients and Katana exclusion. Prove `canBeCrafted:false` rejects crafting even for an otherwise eligible rank with materials. Verify the trade flag as record/schema evidence; do not claim an end-to-end committed trade. Keep the existing pre-write-only guard boundary explicit.
5. Retain earlier overlap observations/regressions as technical evidence where affected; no new overlap decision is required. Repeat broader tests only where final timing/economy changes invalidate assumptions.
6. Preserve fail-closed evidence enforcement (`requireClean`, evidence checker, negative self-tests). Run the final package twice and compare deterministic evidence. Hand off exact base/head, source/runtime/lock hashes, results, remaining field gaps and independent-review status. Push and verify if available; otherwise deliver a verified exact-history bundle and label it local-only.

No upstream engine change, live-game request/write, CDN request, credentials, art, publication, quest edit or full manifest. No global Forge state rewrite or session-close operation. Sealwright behavior is separately proposed in `state/ghost_ship_skyglass_sealwright_behavior_proposal.md`; it is not accepted tuning.
