# Fable handoff — Skyglass active Consume revision

**Director ruling:** RUL-2026-10-11-005. Katana Consume **15%**; Crystal Consume **10%**. Use the changed active-buff behavior. These replace 40%/20% and the old instant-only interpretation. The canonical owner is `state/ghost_ship_skyglass_reward_decisions.md`; the machine-readable design delta is `state/ghost_ship_skyglass_consume_revision.json`.

**Scope:** Fable-owned offline item revalidation and subsequent derived-record update. Preserve the approved quest graph, AI/jutsu membership, rewards, art and all non-Consume item fields. No live requests/writes, CDN requests, credentials, engine edits, publication or full manifest. ChatGPT has updated design authority only, leaving Fable's branch and accepted r4 harness untouched.

## Source and historical evidence

- Accepted r4: `perseverance484/tnr-tools@3f825562ea051306a3803f47428b742ae5100011`, engine `cddd7d91c9e6bdebc978ddcb61e5b8a305bd0f93`. All original results remain evidence for that pin and the former values, not this revision.
- New source reviewed: `studie-tech/TheNinjaRPG@585534d7eb21d6f0dd678d5c3eb92662f611d39b`, observed upstream main. This is not a verified deployment pin. Active Consume starts with `83fd27941449bdffd08922666cc4787dcb9717da`; include its subsequent Consume fixes already present in the reviewed head.
- `validators/combat.ts:618–629`: active Consume `rounds` defaults to 3; generated `shieldRounds` separately defaults to 3.
- `SuperRefineEffects:1429–1438`: Consume needs Damage/Pierce in the same array only when `rounds === 0`. Positive-duration standalone Consume is source-admissible. Reassess the old Crystal blocker; do not implement the historical validator-exemption proposal automatically.
- Runtime source distinctions to test: weapon activation is action-based (`routers/combat.ts:3657–3709`); same-action SELF-tag dedupe (`actions.ts:1103–1108`) differs from separately active Consume ratios aggregating up to 100% (`tags.ts:2047–2058`). Generated shields are capped individually, not as one aggregate stack (`process.ts:1141–1154`). These are source findings, not executed evidence for the revised items.

## Locked and open fields

Katana keeps exactly Pierce50 (Crystal), SELF Buff Prevent immunity2r and Consume15; LEGENDARY WEAPON/SWORD, non-imbuable, accepted Night's Testament AP40/CD6/range4/costs40/40/0 and all other RUL004 baseline/economy fields. Crystal keeps one Consume10 effect, CRYSTAL/WEAPON-only, with no filler damage. Acquisition, quantities and probabilities do not change.

The director has not selected the Consume buff duration for either item or newly accepted generated-shield duration. Record both separately. Do not silently carry over `rounds:0` or turn an omitted field's new default into director approval. Source defaults 3/3 may be clearly labelled **test carriers** while timing remains open. Final full records await accepted timing; research and carrier tests can proceed.

The old `state/ghost_ship_skyglass_katana_record.json`, its generator and frozen harness still use 40%/rounds0 and Crystal20. Preserve their historical reproducibility; produce the next version deliberately with source/ruling provenance and an explicit before/after diff. The current delta is not a full item record or manifest.

## Required offline evidence

1. Pin the source/runtime/lockfile and assess drift from the old execution pin. Validate exact revised effects and complete candidate items, with presentation placeholders clearly labelled. Demonstrate positive-duration Consume-only Crystal acceptance and the instant-mode companion restriction. Keep weapon-only and non-imbuable recipient guards.
2. Exercise granting Consume, granting-hit timing and later hits from other actions while active, including subsequent rounds. Measure buff expiry separately from each generated shield's lifetime and accumulation. Do not claim permanent on-equip Consume without evidence or approval.
3. Test shielded targets, Pierce, multiple hits/targets, delayed damage and self/reflected-damage eligibility against actual engine behavior. Test refresh/reapplication, overlap with existing Consume, shield caps and expiry. Old one-action SELF dedupe findings do not by themselves settle new passive stacking.
4. Test Clear/removal and Buff Prevent interactions, including the Katana's unchanged immunity. Verify accepted cooldown/AP/costs/targeting and that no Crystal can be imbued onto the Katana. Retain existing B3 guard boundaries and distinguish pre-write eligibility from persistence/concurrency.
5. Preserve the r4 evidence failure enforcement and infrastructure-aware self-tests. Return reproducible results, current derived-record/builder status, remaining timing/economy/presentation decisions, and an exact frozen SHA for independent review.

The approved AI kits and graph are not reopened. Their old-pin measurements remain historical evidence; assess relevant engine drift before claiming they carry to the new pin. No balance acceptance is implied by passing tests. If a remaining engine defect is found, report it separately; an upstream fix requires its own authorization.
