# Skyglass Project — Sealwright Encounter / Stage 2 Combat Draft

**2026-10-11 comparator update:** `RUL-2026-10-11-001/002` approves eleven retained Ghost Ship legacy jutsu instead of wholesale shared-pool migration. See `state/ghost_ship_legacy_retention_review.md` and the text-only conversion in `state/ghost_ship_legacy_jutsu_conversion.json`. The regular Captain retains Death's Door, Death's Grasp and Battle Trance, rethemed as Unbroken Command, Keelbind and Remembered Form. Its five-move membership is accepted under RUL-2026-10-11-003; final rules and parity remain unvalidated. Its all-shared kit references are historical. Sealwright's own seven-jutsu identity and double-Clear design remain approved and unchanged.

**Accepted comparator:** RUL-2026-10-11-003 accepts all five captured regular-Captain moves: Unbroken Command, Remembered Form, Keelbind, B14 and B17. No new filler is authorized. Fable's rule/cadence/combat tests remain pending; equal multipliers do not prove parity.

**Status:** DIRECTOR-ACCEPTED DOUBLE-CLEAR PLAYSTYLE / SEVEN EQUIPPED POOL JUTSU; proposed source-backed rule ordering and combat parity tests remain open. The director expressly wants the Sealwright to strip positive buffs continually with regular S31 Unraveling Strike, plus B32 Nullifying Wave as an above-70 IDG reserve. Treat their overlapping Clear effects as intentional, **never a deduplication defect**. No implementation manifest, no live-game actions.  
**Baseline:** `perseverance484/tnr-tools@0eb57de20877d266dde666229ae4c68e8fbcf4c0`.  
**Approved structural route:** `state/ghost_ship_skyglass_expansion_design.md` and `state/ghost_ship_skyglass_graph_patch.json` (RUL-2026-10-10-003).  
**Approved reward scope:** `state/ghost_ship_skyglass_reward_decisions.md` (Skyglass Reliquary route reward, separate Katana and Crown loop).  
**Combat pool authority:** accepted `state/ghost_ship_hybrid_kit_proposal.json` for the Captain comparator, plus generated `skills/building-tnr-content/data/32b_DATA_pool.json` (82 shared jutsu codes). Detailed source-backed rule proposal and gate checks: `state/ghost_ship_skyglass_sealwright_rule_contract.json` (not a Forge manifest).
**Evidence:** `harvests/inbox/tnr_results_1790826836406.json` captures the regular Captain as **Level 100 / JONIN; stats multiplier 3.0; pools multiplier 2.5; regeneration 60**, plus his inventory. RUL-2026-10-11-003 accepts the five-move kit in `state/ghost_ship_hybrid_kit_proposal.json`: **Unbroken Command, Remembered Form, Keelbind, B14 and B17**.

## Identity and design objective

The **Sealwright** was a highly trained shinobi engineer entrusted with isolating a damaged impression-lattice branch of the Ghost Ship. His preserved higher-fidelity impression discovered deteriorating reconstructions and quarantined their records, but the Captain's preservation command overrode his attempts to stop the system. Skyglass still reconstructs him as the archive's custodian. The character is **not undead, a modern technician, or a generic spellcaster**.

**Encounter identity:** **Captain-tier containment boss**, not a mid-tier elite. He uses boss-pool offense and disruptive seals while retaining a distinctive defensive identity: wards, power suppression, shield-breaking and the occasional command-grade lockdown. He should be **on par with the regular Captain in practical combat difficulty**, not the more powerful Crowned Captain. He is not a second final-phase enemy or a repeated stun-lock machine. Defeating him unlocks the Reliquary as a **quest-completion reward**, not an extra AI drop.

**Combat slot:** The new `b_sealwright` battle in the Quarantined Archive. One Sealwright, battle entered directly from `d_sealwright`; on loss `r_sealwright` returns to `d_sealwright`. The fight is the second combat on the successful secret route after Core Horror. The existing `w_secret` gives exactly one Skyglass Reliquary on completion and terminates the quest.

## Director-approved combat personality — relentless buff removal

**Strip, seal, withstand, detonate.** The Sealwright constantly attempts to deny the player's buffs through Unraveling Strike; Nullifying Wave is a second Clear held for excessive IDG accumulation. **The overlap is a deliberate combat identity**, not redundant code. He reinforces himself with a compression ward, applies suppression, and threatens with boss-grade restraint and detonation. The player cannot count on keeping stacked positive effects indefinitely; counterplay lies in timing buffs, exploiting cooldowns/clear prevention and handling his lower-damage turns.

This should feel like fighting the person who built the ship's seal safety systems, not like fighting the Captain again.

## Director-accepted seven-jutsu roster — two deliberate Clears

Two shared boss-pool moves, **B14** and **B16**, provide high-impact offense. Four other rotation actions include **S31's ordinary, repeated full Clear**. **B32 is the seventh equipped jutsu, for IDG above 70 ONLY**; it must not be offered as routine filler or generic random action. The full seven-technique loadout is accepted in design through the director's explicit additive seventh-jutsu request and subsequent confirmation of deliberate dual-Clear overlap. The exact AI rule ordering, gear and effective parity remain subject to offline proof and final review.

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

**Source-backed rule-order proposal:** `includeDefaultRules:false`; **B32 emergency IDG rule FIRST**, **S31 ordinary damage+Clear SECOND** at its range-3 gate (cast whenever usable, not only when a named buff type is detected), followed by B22 self-ward and the B16/B14/B33/S27 boss-pressure rotation. A candidate movement preference can close into S31's shorter range before ranged attacks; its exact placement must be validated for Captain-tier parity. Use in-game IDs and exact range+1 gates from the pool. This design is materialized as a nine-rule candidate in `state/ghost_ship_skyglass_sealwright_rule_contract.json`; rule ordering has **not** been engine-simulated or frozen.

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

The jutsu ID above is the **captured shared-pool B32 ID**, not a create symbol. Its full record has **ALL method** and range5. The approved `distance_lower_than:6` remains a **trigger restriction on CLOSEST_OPPONENT**, not a native ALL-recipient range boundary. Matching the condition/action target keeps the trigger coherent; the actual Clear may affect other eligible opponents through ALL targeting. B32 costs60AP with an8-round cooldown. If its threshold/gate is unmet or the action is unavailable, fall through to ordinary rules. Keep it out of unconditional/combo/random filler. Test closest-summon versus farther-player and other multi-opponent cases.

**Effect scope:** B32 is `clear 100`, not a special IDG-only removal. On success, its Clear mechanic removes **removable positive buffs broadly**, including IDG; it may be stopped by `clearprevent` and excludes source-protected effects. Using it solely as an answer to excess IDG preserves the requested *trigger*, not selective dispelling.

**Director-approved overlapping dispels:** **S31 Unraveling Strike (`damage 40` + `clear 100`) must be used routinely whenever ready and in range**, even without a narrow named-buff condition. It may remove IDG before B32's 71-power trigger and leave B32 unused in many fights. **This is exactly the desired behavior.** B32 remains an emergency second Clear when the enemy manages to stack >70 IDG despite routine S31 casts. Neither jutsu is removed, combined, or narrowed to IDG-only. Ordinary Clear also removes other removable positive buffs; the defender may use Clear Prevent to resist it.

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
| **Regular Captain (captured)** | **100 / JONIN** | **3.0** | **2.5** | accepted reference: Unbroken Command / Remembered Form / Keelbind / B14 / B17 |
| **Sealwright (revised target)** | **100 / JONIN** | **3.0** | **2.5** | Captain-tier containment / boss moves B14 and B16 |

**Design target:** Mirror the regular Captain's **Level 100, JONIN, 3.0× stats, 2.5× pools, regeneration 60** as the source-backed starting point. This follows the director's request for Captain parity, **not proof of equal outcomes**. First Blade and Sentinel are higher at 3.5× pools; Crowned Captain is separate and stronger at 3.6× pools. **Gear correction, source audited:** October 1 `profile.getAi` capture DOES show AI Heavy Armor and Cursed Dagger owned by the regular Captain, but BOTH have `equipped:"NONE"` (not equipped). In pinned game source `app/src/server/api/routers/combat.ts` passive armor effects require `ui.equipped !== "NONE"`, and `app/src/libs/combat/actions.ts` excludes unequipped item actions. Thus these captured pieces **do not contribute to his ordinary combat baseline unless current live equipment or encounter overrides changed**. Sealwright needs no copied gear by default; fresh capture confirms. Preferred stat/generals/elements and effective runtime difficulty remain subject to separate review.

## Completion and player guidance

- One **Captain-tier boss encounter**, no unseen reinforcements, no second combat phase and no random extra boss.
- Loss → retry via existing reset pattern. Do not award the Reliquary on boss damage or before `w_secret`.
- On victory, return to `d_reliquary_claim`; the archive's reconstruction persists, but the player may remove one Reliquary and depart.
- Do not grant Crown fragments, Skyglass Katana, or the Crystal directly from the Sealwright AI.
- Player can learn: shields/defenses protect the custodian; breaking through them and using controlled pressure is more effective than relying exclusively on long-lived buffs.
- The Secret route is a **two-combat route** (Core Horror then Sealwright) with fixed seal puzzle; no forced battle added to the Crowned Captain farm.

## Director decisions needed for combat freeze

**Already directed by director:** The Sealwright must be **on par with the regular Captain** and **must use meaningful moves from the shared boss pool**. The proposal reflects this with the same captured base multipliers and two substantial boss-grade jutsu. The fight remains the second successful secret-route encounter, and its reward source/route structure are already locked.

**Director-confirmed playstyle:** B32 Nullifying Wave stays as the seventh reserve with first-priority **target_has_effect increasedamagegiven threshold 71** and gate 6, and **S31 stays in frequent normal use as a second full buff Clear**. The seven-jutsu roster is accepted as the current design target: **B22, B16, B14, B33, S27, S31 + B32**. B16's two-round Stun+Seal combination remains a combat-parity validation risk, not permission to silently replace a chosen move. Exact priority/positioning logic and numeric effective parity remain open for engine tests.

**Technical gates:** Compare the regular Captain and Sealwright under identical offline combat fixtures, including absence of passive Captain gear when equipped NONE; validate AI action-point/cooldown/close-range movement, repeated S31 Clear behavior, triggered B32, B16 2-round control, and full rule schema. Confirm no independent Sealwright loot or automatic farming power beyond the approved Reliquary at `w_secret`. Do not interpret unequipped Captain inventory as passive or active equipment.

The seven-technique design and deliberate overlapping Clears are now settled. **Next authorized work:** offline validate the proposed rule order and effective Captain parity, record any director-facing corrections, then let Fable translate the approved exact AI/profile into Forge while separately resolving the remaining item-engine, art and hidden-state gates. No game live requests, writes or publication.
