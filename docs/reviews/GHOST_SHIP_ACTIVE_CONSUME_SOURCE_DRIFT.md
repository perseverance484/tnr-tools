# Ghost Ship / Skyglass — active Consume source drift

**Status:** source review for the RUL-2026-10-11-005 offline revalidation. This document does not report executed tests, deployed behavior, or Captain/Sealwright parity acceptance.

| Input | Exact reference |
| --- | --- |
| Accepted historical r4 evidence | `perseverance484/tnr-tools@3f825562ea051306a3803f47428b742ae5100011` |
| New design authority | `perseverance484/tnr-tools@46df27172556807ab5bf723b0aa8c1251445ba2e`; `state/prompt_ghost_ship_skyglass_consume_revalidation.md` |
| Historical engine | `studie-tech/TheNinjaRPG@cddd7d91c9e6bdebc978ddcb61e5b8a305bd0f93` |
| New execution candidate | `studie-tech/TheNinjaRPG@585534d7eb21d6f0dd678d5c3eb92662f611d39b` |

Source anchors below refer to the **new engine commit**, except where explicitly labelled historical. The new commit is an observed upstream revision, not a verified deployment pin. Endpoint files were read with `git show` and compared with `git diff`; neither engine checkout nor engine files were modified.

## 1. Review boundary and history

The endpoint comparison covers battle initialization, the action loop, AI selection, relevant effect processing, profile/capture compatibility, and the occupation guards exercised by the item harness. It is not a complete audit of every upstream change.

The source history was deepened before the range was finalized. `git merge-base old new` equals the exact historical pin `cddd7d91c9e6bdebc978ddcb61e5b8a305bd0f93`, and `git rev-list old..new --count` returns **162 commits**, matching the handoff. An earlier 136 count from the shallower clone was incomplete and is superseded. The endpoint file comparison is independent of the count. The execution provenance must separately record source/lockfile/runtime pins; no historical runtime result becomes current merely because a helper has the same name.

## 2. Initialization and action-loop contract

| Area | Endpoint change or preserved contract | Consequence for this harness |
| --- | --- | --- |
| Participant clones and rank caps | `routers/combat.ts:2219–2224,2470–2487`; `libs/profile.ts:198–211`. Each occurrence is cloned; rank caps still precede assembly. Scaling/distribution can run first when explicitly requested. | Preserve r4 deep-clone and `capUserStats` preprocessing. All Ghost Ship AI rows remain JONIN carriers; do not restore uncapped captured generals. The historical quest capture has no `scaleStats` field on its opponent entries. |
| Post-assembly preprocessing | `routers/combat.ts:2550–2581`: auto-combat, active max-pool adjustments, mastery refresh and first-participant aggressor flag. | Existing r4 ordering remains applicable to the declared QUEST carriers. No engine adapter or bypass is needed. |
| Team assignment | `routers/combat.ts:3131–3136,3175–3182`: optional ordered `leftSideUserCount` takes precedence over `leftSideUserIds`, supporting duplicate NPC templates on opposite sides. | Existing unique-ID item fixtures can keep explicit left-side IDs. A future duplicate-template/team fixture must pass the ordered boundary and distinguish combatant IDs; controller ID alone is insufficient. |
| Spawn | `routers/combat.ts:3346–3359`; `libs/combat/participants.ts:20–45`: finite distinct spawn cells, selected with `node:crypto.randomInt`. | `withSeed` controls `Math.random`, not this RNG. Existing explicit placements overwrite spawn positions before tested actions. Require every participant in a deterministic fixture to have a placement. Do not claim seeded random spawn or random-coordinate coverage. |
| Action loop | `routers/combat.ts:644–654,727–759`; `libs/combat/util.ts:2861–2949`. The align → action → align loop and sage transition calls are unchanged in function; `alignBattle` still owns duration decrement and round/AP progression. | Keep real `performBattleAction` / `performAIaction` plus alignment. Do not create a separate Consume timer model. The historical artificial idle-timeout branch is not a substitute for the full server polling/persistence path. |
| Client response | `routers/combat.ts:857`; `libs/combat/util.ts:1566–1782`: responses now use a stricter mask/catalog selection instead of the former dynamic mask. | In-process authoritative `CompleteBattle` fixtures bypass response masking. Their results do not validate browser rendering, catalog visibility, polling or persistence. |

No breaking signature change was found for the harness's imported `processUsersForBattle`, `capUserStats`, `applyPoolAdjustmentsToBase`, `refreshMasteries`, `alignBattle`, `performAIaction`, or `performBattleAction` entry points. This is a source-compatibility observation, not an executed compatibility claim.

## 3. Consume and related damage drift

| Change | Source anchor | Required interpretation/test boundary |
| --- | --- | --- |
| Active Consume schema and distinct timers | `validators/combat.ts:618–629`: `rounds` defaults to 3, `shieldRounds` independently defaults to 3. | Katana 15% and Crystal 10% are approved; these duration defaults are only labelled test carriers until separately accepted. |
| Standalone active Consume | `validators/combat.ts:1429–1438`: the Damage/Pierce companion check applies to Consume only at `rounds === 0`. | Re-test the complete positive-duration Crystal and an explicit instant-mode negative control. The old blanket Crystal validator blocker and historical exemption proposal do not carry forward. |
| Activation versus equipment | `routers/combat.ts:3657–3709`: imbuement effects compose into a permitted weapon, but only ARMOR/ACCESSORY/KEYSTONE realize their effects on assembly. | Weapon/imbued-weapon Consume must be granted through a weapon action. A permanent on-equip weapon buff is not established by the source. |
| Active registration and granting-hit ordering | `libs/combat/process.ts:414–419,487–515`; `libs/combat/util.ts:1105–1152`: active Consume registers after activation/prevention and before damage accumulation; a newly authored zero-duration instance has a separate allowance. | Test granting action, later actions and expiry separately. Do not treat an expired formerly active instance as a new instant instance. |
| Overlap | `libs/combat/tags.ts:2047–2058`: active ratios accumulate by creator up to 100%, and use the greatest generated-shield duration. `libs/combat/actions.ts:1103–1108` retains same-action SELF stack-key deduplication. | Same-action dedupe and separate active-buff overlap are different cases. The old Consume-on-Consume observation does not settle the active version. |
| Damage sources and grant ordering | `libs/combat/process.ts:509–526,784–815,990–1014,1141–1154`: accumulation precedes shield mitigation; direct/residual/wound/afterburn/drain/poison and reflected-return handling exist, while self/recoil are excluded in the relevant accumulation branches. Generated shields are granted after consequences and individually capped at `SHIELD_MAX_HEALTH`. | Execute shielded/Pierce/multi-target/delayed/reflect/self/recoil probes. Establish actual grant amounts and total accumulated shield lifetime from runtime state. Do not infer one aggregate shield-stack cap from the per-grant cap. |
| New Diffuse processing | `libs/combat/process.ts:517–526,678–698`; `libs/combat/diffuse.ts`: immediate versus deferred damage now has separate handling, including repayment and conversion callbacks. | A fixture without Diffuse does not exercise it. Do not assert universal damage-timing equivalence with r4. Diffuse is not added to either approved item. |
| Persistent-source protection | `libs/combat/tags.ts:1218–1230` adds `elementalMastery` to the sources Clear/Cleanse must not strip. | Include that exact source spelling in new harness effect accounting. Active item Consume is a removable positive effect when its source is not protected. |

The damage-default constants and the 0056 AI migration file do not change between these endpoints. Their stability does not eliminate the effect-pipeline changes above. Delayed drain attribution also changes from a target-only key to a creator/target key (`tags.ts:2087–2124`); wound matching now requires the same creator (`tags.ts:1866–1871`). Multi-attacker attribution deserves new evidence whenever tested.

## 4. AI, captured rows and old A1/A2 measurements

- QUEST and OVERWORLD allegiance now follows battlefield direction: `participants.ts:8–16`, `ai_v2.ts:109–122,579–634`, `actions.ts:1305–1333`. The historical one-player/one-boss fixtures differ in both village and direction, so no selector difference is expected solely from this change. That is an inference, not a new fight result. Multi-participant/summon tests must state teams explicitly.
- AI target choices add `HIGHEST_ENMITY_OPPONENT` and `LOWEST_ENMITY_OPPONENT` (`validators/ai.ts:9–10`, `ai_v2.ts:266–272`). Participants initialize `enmity:0` (`routers/combat.ts:3212`); damage credits enmity through the new aggro helpers. Approved Ghost Ship/Sealwright rules do not select these targets. No AI kit or rule remap is authorized here.
- Actions now resolve per-effect coordinate patterns through `getActionAffectedTiles` (`actions.ts:952–963,993–1009`; `util.ts:3308–3351`). Captured SINGLE/ALL actions without coordinate overrides use their inherited patterns. Random coordinate sampling uses secure randomness outside `withSeed` and is outside the existing carrier claim.
- Migration `0056_unified_combat_stats_masteries.sql` is byte-unchanged. Keep its source-defined conversion for pre-0056 AI captures and the r4 rank-cap step. The later schema adds elemental/PvP fields, required-skill IDs and coordinate-targeting data; it does not justify rewriting retained legacy mechanics or protected hashes.
- New player equipment/jutsu eligibility depends on `requiredSkillId` (`routers/combat.ts:3383–3392,3563–3568`; `libs/skillRequirements.ts:9–20`). Existing `queryShell.userSkills:[]` satisfies the new required array read; absent/null required-skill IDs mean no skill gate. Do not claim compatibility with a newly skill-gated live record from an older capture lacking that field.
- Active trained elemental mastery can add a protected elemental IDG passive (`routers/combat.ts:3418–3436`). Older carriers omit `activeTrainedElement` and `elementalMastery`; the source helper treats that as no active element (`libs/elementalMastery.ts:31–43`). State this absence as a carrier boundary, not a representation of current players.
- All accepted r4 A1/A2 measurements remain tied to `cddd7d91…`, the old fixtures and source-default damage settings. The new item tests do not re-accept Sealwright parity, support activation, minion tuning or AI rule order. New-pin combat measurements require a separately labelled rerun before numerical carry-forward.

## 5. Occupation and profile boundaries

`occupation.imbueItem` keeps occupation, item kind, weapon-target, non-imbuable, duplicate/slot and equipped-item checks. It adds rejection of a crystal reserved for auction/trade and a required-skill check (`routers/occupation.ts:620–653`). The new harness should exercise those added pre-write cases or explicitly exclude them from its evidence claim.

The snapshot claim still precedes persistence (`occupation.ts:690–703`). The target-auction guard and crystal consumption are later writes; crystal consumption now also requires `isInAuction:false` (`occupation.ts:705–731`). A read-only stub stopped at the first write verifies pre-write eligibility only. It does not verify those later CAS/atomic-consumption/concurrency guarantees or a committed imbuement. Craft material consumption likewise adds an auction-state condition (`occupation.ts:400–409`).

Profile refresh now fetches a PvP population-average setting (`routers/profile.ts:3852–3858`); regeneration and crafting/imbuing experience can receive PvP boosts (`libs/profile.ts:432–442`; `occupation.ts:345–352,749–756`). Existing fixture settings `[]` and absent PvP fields yield no boost in `libs/pvpExperience.ts:15–47`. A DB stub invoking full profile refresh may require an extra **read-only** query response; do not suppress the query by changing engine source. Elemental-training queue settlement and persistence have also changed and are not covered by an item eligibility stub.

Migrations 0063–0071 add skill requirements, coordinate fields, elemental progression, auction offers, report/parental-control tables, PvP fields and village missions. None is run by this offline harness. New schema fields absent from old captures remain an explicit fixture limitation. No live settings, deployed migration state or current player data were read.

## 6. Minimal new-harness adaptation

The historical `harness/ghost_ship_stage2/` remains frozen. In its deliberately separate successor, `harness/ghost_ship_consume/engine/lib/sim.ts`, this source pass makes only:

1. Add `consume` to the positive-effect accounting set, so removal/expiry observations can include the new active buff.
2. Add `elementalMastery` to the protected-source accounting set, matching the new engine.
3. Correct the determinism comment: `Math.random` seeding does not control the new secure initial-spawn or random-coordinate RNG; fixed-placement fixtures avoid depending on them.

Keep the real capped/cloned assembly, pool/mastery preprocessing, action-loop ordering and evidence-failure enforcement. Preserve missing-versus-null capture distinctions and source/ruling provenance in revised item carriers. Additional changes belong to the new item fixtures/tests or their safe dependency stubs, not the old evidence or engine code.

Before release, the director still owns both Consume durations, both generated-shield durations, Crystal economy/access policy, presentation and art. This source pass grants no approval for defaults, engine corrections, live writes, publication or manifest construction.
