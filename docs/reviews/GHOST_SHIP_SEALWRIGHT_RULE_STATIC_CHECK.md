# Skyglass Sealwright — source-key and priority static check

**Status:** PASS for scoped static rule checks / **NOT** a full combat parity test or Forge manifest validation.  
**Date:** 2026-10-10  
**Repository:** `perseverance484/tnr-tools@0eb57de20877d266dde666229ae4c68e8fbcf4c0`  
**Design contract tested:** `state/ghost_ship_skyglass_sealwright_rule_contract.json` at blob SHA `be9cfe4f243755016e385aae8bc438dfb96854a6`  
**Game source:** `studie-tech/TheNinjaRPG@4774560eb6e8c9a5ef156d66b953dcb6aeeba4d6` (`app/src/libs/combat/ai_v2.ts`, `app/src/validators/ai.ts`).  
**Generated nested/keys:** `forge/src/runner/nested.json` on reviewed main.  
**Shared pool:** `skills/building-tnr-content/data/32b_DATA_pool.json`.  
**Live requests/writes:** 0 / 0.

## Method and result

Ran a pure JavaScript static check over the committed rule-contract JSON. Each supplied condition/action discriminant and field key was compared against the generated Forge nested-key allowlists. Every literal equipped jutsu ID, AP and cooldown was matched to its code in the shared pool. Condition values and priority behavior were exercised by a small source-derived selection model mimicking the verified `ai_v2.ts` branches (`target_has_effect` sums powers and uses `>=`, distance conditions use inclusive path length, unavailable jutsu actions fall through). The model does **not** execute TNR's full action simulator, effects, movement grid or turn loop.

**Result: 112/112 scoped assertions passed; 12/12 scenario expectations passed.**

| Scenario | First selected action |
| --- | --- |
| IDG 69, distance 3, all ready | S31 routine Clear |
| IDG 70, distance 3, all ready | S31 routine Clear |
| IDG 70.5, distance 3, all ready | S31 (integer-threshold limitation) |
| IDG 71, distance 3, all ready | B32 reserve |
| IDG 90, distance 6, all ready | B32 reserve |
| IDG 90, B32 on cooldown | S31 routine Clear |
| IDG 0, S31 on cooldown | B22 ward |
| Normal boss pressure after S31/B22 unavailable | B16 Fetters |
| Outside S31 range, B22 unavailable | Move toward enemy |
| Movement unavailable | Fall through to B16 ranged boss attack |
| Beyond all attack ranges | Move toward enemy |
| Adjacent, all actions unavailable | Reaches engine-appended end-turn path |

## Specific source findings

1. **Deliberate double Clear:** `S31` (Damage 40 + Clear 100, range 3, cooldown 5) is high-priority normal offense. `B32` (Clear 100, range 5, cooldown 8) has one conditional-only AI rule; it cannot activate at IDG 70 but does at integer total >=71. No duplicate unconditional B32 rule exists. This implements the director's requested continual buff denial, not two redundant normal dispels.
2. **Trigger limitation:** The live schema's `target_has_effect.threshold` is an integer 0–100, so a strict ">70" threshold is only exactly expressible for integer IDG sums. With a fractional sum of 70.5, threshold 71 does not fire. Do not silently relax to threshold 70 without director permission.
3. **Target limitation:** The specified reserve checks **CLOSEST_OPPONENT**. In multi-target fights (summons), a nearer target with little IDG can prevent emergency action against a more buffed but farther player. The director asked for targeted opponent IDG, not a new global-any-target selector.
4. **Source equipment correction:** October 1 regular Captain `profile.getAi` capture owns AI Heavy Armor and Cursed Dagger, but each inventory row has `equipped:"NONE"`. Current combat code activates passive equipment effects only when equipped and ignores unequipped item actions. These two items **are not evidence of active Captain buffs or attacks**; a fresh capture/replay still decides current state.
5. **Full Clear scope:** Both jutsus remove eligible positive buffs broadly, not only IDG; `clearprevent` can block them and some effect sources are protected.
6. **Movement preference is a proposal, not a settled user balance choice:** The nine-rule draft moves toward an enemy at path length >=5 to reach S31's shorter range. That improves buff-strip frequency but can change damage/defensive cadence; test before freeze.

## Remaining blocking validation

- Schema-aware AI Profile build/preflight using Forge's current runner and the exact source pin.
- Actual offline `performAIaction` test cases for threshold, cooldown/AP/pools, exact movement and repeated S31 dispels, Clear Prevent, 70.5 and multi-target cases.
- Representative offline fight comparison against current regular Captain (same player loadouts, no active Captain armor/weapon without proof of equipping), covering win rate, time-to-kill, B16 Stun+Seal lockout, damage spikes and debuff/clear uptime.
- Confirm the actual current regular Captain and quest visibility through a user-run read-only capture before creating any full-record update manifest.
- No game/source changes, live requests, Forge write manifest, publication or release authorization resulted from these static checks.

**Next:** Fable performs source-backed AI/profile validation and representative combat tests using the committed rule-contract candidate; ChatGPT independently audits the resulting frozen tests/handoff, surfacing any director-owned tuning rather than changing values autonomously.
