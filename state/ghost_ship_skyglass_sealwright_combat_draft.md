# Skyglass Project — Sealwright Encounter / Stage 2 Combat Draft

**Status:** CAPTAIN-TIER COMBAT DRAFT / DIRECTOR-LOCKED SEVENTH RESERVE. Director requires boss-pool techniques and parity with the regular Captain, and has now explicitly directed **B32 Nullifying Wave** as a seventh jutsu, reserved solely for opponent IDG above 70. The other six rotation moves, precise AI rules and parity testing remain proposed, **not fully frozen**. No manifest, no live game actions.  
**Baseline:** `perseverance484/tnr-tools@0eb57de20877d266dde666229ae4c68e8fbcf4c0`.  
**Approved structural route:** `state/ghost_ship_skyglass_expansion_design.md` and `state/ghost_ship_skyglass_graph_patch.json` (RUL-2026-10-10-003).  
**Approved reward scope:** `state/ghost_ship_skyglass_reward_decisions.md` (Skyglass Reliquary route reward, separate Katana and Crown loop).  
**Combat pool authority:** `state/ghost_ship_shared_pool_migration.json` plus generated `skills/building-tnr-content/data/32b_DATA_pool.json` (82 shared jutsu codes).  
**Evidence:** `harvests/inbox/tnr_results_1790826836406.json` captures the regular Captain as **Level 100 / JONIN; stats multiplier 3.0; pools multiplier 2.5; regeneration 60**, plus his inventory. The approved regular-Captain shared kit in `state/ghost_ship_shared_pool_migration.json` is **B19, B14, B17, B05, S31, B33**.

## Identity and design objective

The **Sealwright** was a highly trained shinobi engineer entrusted with isolating a damaged impression-lattice branch of the Ghost Ship. His preserved higher-fidelity impression discovered deteriorating reconstructions and quarantined their records, but the Captain's preservation command overrode his attempts to stop the system. Skyglass still reconstructs him as the archive's custodian. The character is **not undead, a modern technician, or a generic spellcaster**.

**Encounter identity:** **Captain-tier containment boss**, not a mid-tier elite. He uses boss-pool offense and disruptive seals while retaining a distinctive defensive identity: wards, power suppression, shield-breaking and the occasional command-grade lockdown. He should be **on par with the regular Captain in practical combat difficulty**, not the more powerful Crowned Captain. He is not a second final-phase enemy or a repeated stun-lock machine. Defeating him unlocks the Reliquary as a **quest-completion reward**, not an extra AI drop.

**Combat slot:** The new `b_sealwright` battle in the Quarantined Archive. One Sealwright, battle entered directly from `d_sealwright`; on loss `r_sealwright` returns to `d_sealwright`. The fight is the second combat on the successful secret route after Core Horror. The existing `w_secret` gives exactly one Skyglass Reliquary on completion and terminates the quest.

## Proposed player-facing tactical character

**Seal, withstand, detonate.** The Sealwright reinforces himself with a compression ward, applies suppression, and dismantles the player's defensive setup. A powerful sealing restraint creates a dangerous opening for a boss-grade detonation, but their cooldowns leave counterplay windows. He has **credible boss-level damage** and a rare high-control sequence rather than cheap continuous stuns or death mechanics.

This should feel like fighting the person who built the ship's seal safety systems, not like fighting the Captain again.

## Seven-jutsu loadout — six rotation candidates plus approved reserve

Two boss-pool moves, **B14** and **B16**, are the proposed high-impact signatures. The four remaining rotation candidates define his containment specialty. **B32 Nullifying Wave is separately director-approved as an equipped seventh jutsu, for a conditional IDG counter only; it must not join ordinary unconditional casting rules or generic random action selection.**

| Priority | Code | Shared jutsu | Role | Captured pool effects | AP / Cooldown |
| --- | --- | --- | --- | --- | --- |
| 1 | **B22** | Compression Barrier | Protective opener | 20% Absorb for 3 rounds; 25% Decrease Damage Taken for 3 rounds | 40 AP / 5r |
| 2 | **B16** | Sovereign Fetters | **Boss-grade control** | 60 Damage; 100% Stun for 2 rounds; 100% Seal for 2 rounds | 60 AP / 10r |
| 3 | **B14** | Cataclysm Detonation | **Boss-grade heavy attack** | 85 Damage | 60 AP / 8r |
| 4 | **B33** | Piercing Judgment | Defensive counter | 55 Pierce; 25% Increase Damage Taken for 2 rounds | 60 AP / 7r |
| 5 | **S27** | Weakening Strike | Pressure suppression | 40 Damage; 20% Decrease Damage Given for 2 rounds | 60 AP / 4r |
| 6 | **S31** | Unraveling Strike | Remove enemy buffs / fallback attack | 40 Damage; 100% Clear | 60 AP / 5r |
| **7 (reserve)** | **B32** | **Nullifying Wave** | **Director-locked emergency counter when enemy IDG >70** | **100% Clear of removable positive effects**, not an IDG-only purge | **60 AP / 8r** |

**Changes from v1:** Added **B16 Sovereign Fetters** and **B14 Cataclysm Detonation**; removed low-tier **S32 Lingering Strike** and **S41 Steady Strike**. **Director's subsequent addition:** the seventh, reserved **B32 Nullifying Wave**. The defensive B22 and control/damage support of B33, S27 and S31 remain. Exact in-game names/effects are drawn from `skills/building-tnr-content/data/32b_DATA_pool.json`; use the captured IDs rather than inventing or renaming moves.

**Proposed AI priority:** `includeDefaultRules:false`; place the **conditional B32 emergency-response rule at the very top**, before B22 or any boss-grade attacks. If it does not qualify or is unavailable, fall through to the six-move rotation: B22 when usable, B16 when close enough and off cooldown, B14, B33, S27, S31, then the normal move-toward-target fallback. Derive actual conditions and range gates from pool codes: B16/B14/B33/S27 are range 5 (gate 6), S31 is range 3 (gate 4), B22 is SELF. Prefer selectively using S31 when the opponent has a relevant buff, if an audited `target_has_effect` condition can do this without harming fallback behavior.

### B32 reserve-only trigger — director approved

The AI uses the *real* `target_has_effect` condition on the exact effect type `increasedamagegiven` (IDG); the current source in `studie-tech/TheNinjaRPG@4774560eb6e8c9a5ef156d66b953dcb6aeeba4d6`, `app/src/libs/combat/ai_v2.ts`, sums the target's matching effect **powers**, then tests `totalTargetPower >= threshold`. This is the SUM of IDG effect powers, not net damage after other damage modifiers.

**Strictly greater than 70:** the current validator accepts an integer `threshold` from 0 to 100. Use **`threshold: 71`** so totals **70** and below do not trigger. The native condition will also wait until **71** for fractional totals, so **70.5 is an expressiveness edge case**, not an additional desired threshold. Fable must document and test that limitation if fractional IDG stacks are possible.

**Highest-priority AI rule, before every other action:**

```json
{
  "conditions": [
    {
      "type": "target_has_effect",
      "effectType": "increasedamagegiven",
      "target": "CLOSEST_OPPONENT",
      "threshold": 71,
      "description": "Target's total Increased Damage Given is 71 or higher"
    },
    {
      "type": "distance_lower_than",
      "target": "CLOSEST_OPPONENT",
      "value": 6,
      "description": "Distance lower than or equal to 6"
    }
  ],
  "action": {
    "type": "use_specific_jutsu",
    "target": "CLOSEST_OPPONENT",
    "jutsuId": "JWZYiHKPNwYziWEFjw4Fn",
    "description": "Select specific jutsu"
  }
}
```

The jutsu ID above is the **captured shared-pool B32 ID**, not a new create symbol. B32 has **range 5**, therefore the precise AI A*-path gate is **`distance_lower_than:6`**. Using the *same target* in the IDG condition, range condition and action prevents selecting a different opponent on execution. B32 costs **60 AP** and has an **8-round cooldown**. If the enemy is not above threshold, is outside range, or the jutsu is not available (cooldown/AP/resources), the engine continues to ordinary rules: it is a **reserve**, not a filler. Do not write a second unconditional B32 rule; do not include it in the normal combo/random cast selection.

**Effect scope:** B32 is `clear 100`, not a special IDG-only removal. On success, its Clear mechanic removes **removable positive buffs broadly**, including IDG; it may be stopped by `clearprevent` and excludes source-protected effects. Using it solely as an answer to excess IDG preserves the requested *trigger*, not selective dispelling.

**Important overlap with the six-move draft:** **S31 Unraveling Strike already carries `clear 100`** and is proposed for the normal rotation. It can remove IDG long before the B32 emergency threshold is reached. This does not invalidate the approved seventh-jutsu trigger, but it could make the reserve rarely fire. **Do not remove S31 without director approval**; resolve this overlap when finalizing the other six jutsu and AI rule priorities.

**Multi-target limitation:** `target_has_effect` checks the selected **CLOSEST_OPPONENT**, not the most-buffed enemy. When summons or multiple enemies exist, test that this still enforces the intended anti-IDG response; do not silently invent a non-existent `highest_IDG` selector.

**Tests required before frozen AI implementation:** separate cases for IDG sums **69 / 70 / 70.5 / 71 / 90**, B32 cooldown, insufficient AP, out-of-range opponents, multiple targets/summons, and the intended fallback rotation. Also verify that Clear actually removes the stacked `increasedamagegiven` instances under the game's active-effect timing (not just that the rule selects the jutsu).

**Risk and parity gates:** B32's triggered full positive-effect clear gives the Sealwright a specific anti-IDG answer without routine spam; B16 is a substantial control move with **both a 2-round Stun and a 2-round Seal**. Together with B22's defenses, it could be more frustrating than the Captain even at identical multipliers. Its **10-round cooldown** and B14's **8-round cooldown** provide relief, but these are not substitutes for real behavior testing. Fable should compare time-to-defeat, action lockouts, damage peaks, pool drain, survival and recovery windows against the regular Captain using the same representative player fixtures. Preserve the 40 AP + 60 AP action economy and avoid unconditional repeated pointless B22 casts. Do not duplicate B16 effects, add extra boss phases, or give the Sealwright new bespoke jutsu. If combat tests find the Sealwright markedly harder, propose a **rule/priority change** for director approval before adjusting the locked Captain-parity target.

## Captain-tier difficulty target — director direction, effective parity pending tests

| Record | Captured Level / Rank | Stats × | Pools × | Purpose |
| --- | --- | ---: | ---: | --- |
| Oathkeeper | 100 / JONIN | 2.0 | 2.5 | technical duelist |
| Wayfinder | 100 / JONIN | 2.0 | 3.0 | ranged control |
| Sentinel | 100 / JONIN | 3.0 | 3.5 | heavy defense/controller |
| First Blade | 100 / JONIN | 3.0 | 3.5 | optional elite |
| **Regular Captain (captured)** | **100 / JONIN** | **3.0** | **2.5** | approved reference: B19/B14/B17/B05/S31/B33 |
| **Sealwright (revised target)** | **100 / JONIN** | **3.0** | **2.5** | Captain-tier containment / boss moves B14 and B16 |

**Design target:** Mirror the regular Captain's **Level 100, JONIN, 3.0× stats, 2.5× pools, regeneration 60** as the source-backed starting point. This follows the director's request for Captain parity, not proof that the final fight will actually be equally hard. First Blade and Sentinel are higher at 3.5× pools; Crowned Captain is separate and stronger at 3.6× pools. **Gear contribution remains open:** the captured Captain has AI Heavy Armor and Cursed Dagger equipped. Determine their mechanical impact and whether Sealwright needs equivalent non-dropping defensive equipment before declaring parity. Do not copy Captain inventory or accidentally add drop chances. Preferred stat/generals/elements, armor and final AI-rule encoding require a later audited contract.

## Completion and player guidance

- One **Captain-tier boss encounter**, no unseen reinforcements, no second combat phase and no random extra boss.
- Loss → retry via existing reset pattern. Do not award the Reliquary on boss damage or before `w_secret`.
- On victory, return to `d_reliquary_claim`; the archive's reconstruction persists, but the player may remove one Reliquary and depart.
- Do not grant Crown fragments, Skyglass Katana, or the Crystal directly from the Sealwright AI.
- Player can learn: shields/defenses protect the custodian; breaking through them and using controlled pressure is more effective than relying exclusively on long-lived buffs.
- The Secret route is a **two-combat route** (Core Horror then Sealwright) with fixed seal puzzle; no forced battle added to the Crowned Captain farm.

## Director decisions needed for combat freeze

**Already directed by director:** The Sealwright must be **on par with the regular Captain** and **must use meaningful moves from the shared boss pool**. The proposal reflects this with the same captured base multipliers and two substantial boss-grade jutsu. The fight remains the second successful secret-route encounter, and its reward source/route structure are already locked.

**Director-locked seventh jutsu:** B32 Nullifying Wave, with first-priority **target_has_effect increasedamagegiven threshold 71**, paired with the precise range-5 gate 6; no casting outside that condition. **Remaining six rotation moves pending acceptance:** approve or revise **B14 + B16** as the two boss-signature moves, with **B22, B33, S27 and S31** supporting containment. In particular, consider whether B16's 2-round Stun+Seal is acceptable against a shielded controller; if too oppressive, request a different existing boss-pool move instead of unilaterally downgrading the entire enemy.

**Technical gates:** Compare the real Captain and Sealwright under identical offline combat fixtures, including whether Captain gear materially changes parity; validate AI action-point/cooldown logic and full rule schema. Confirm no independent Sealwright loot or automatic farming power beyond the approved Reliquary at `w_secret`.

When the six rotation moves, the mandatory B32 reserve rule, and any necessary adjustments are accepted, Fable can author a frozen exact AI/profile contract using the captured shared-pool IDs, then build the manifest in normal dependency order. No game live requests, writes or publication.
