# Supreme Commander Arakane — AI Profile Design

**Status:** Detailed source-routed AI candidate for director review; NOT an executable profile, test PASS, final numeric balance freeze, or authorization to change the game.  
**Director-approved:** Boss identity **Supreme Commander Arakane**, story/final-reveal premise, baseline 14-jutsu roster with Recoil Slam replaced by the elemental-seal nuke, **The Last Directive** (5r Final Stand + 5r IDG + 5r Clear Prevent) below 30% HP, **Countermand** command-seal item, anti-kiting Veilstep→Clear behavior, and innate 100%/99r Seal Prevent.  
**Owner:** This companion details Arakane's behavioral candidate; `state/silent_bastion_design.md` owns the ongoing Pyramid concept and accepted history.  
**Repo:** `perseverance484/tnr-tools@057acddb986b50e486ccf550fac00b68fff51490`. **Game engine pinned:** `studie-tech/TheNinjaRPG@67341a1fa1567b9b33827b802e48120e5d797a15`.  
**Authority:** `docs/00_INDEX.md`, `docs/DOCTRINE.md`, `skills/building-tnr-content/references/ai.md`, `skills/building-tnr-content/data/32b_DATA_pool.json`. No live requests/writes.

## Character / experience (accepted)

**Display name:** **Supreme Commander Arakane**; the title "Supreme Commander" must remain visible so defeating him appears to end the Bastion's chain of command. The Supreme Commander directed the Skyglass Project's military deployment. Replicant Zero established human chakra reconstruction, and The Grand Marshal (epithet **The Second**) made the operation militarily viable, with independent judgment trusted by Arakane. Arakane is composed, dignified, strategic, and bound by his duty, not a boastful madman.

**Reveal only after defeating him:** Another **newly issued** directive reaches the Ghost Ship under Supreme Command authority, proving that the reconstructed Supreme Commander himself was not the ultimate originator. The origin remains unidentified; do not spoil the twist during the fight or earlier Bastion dialogue.

**Distinction:** Grand Marshal systematically suppresses; Arakane **adapts** through suppression, theft, self-preparation, positional pressure, shield destruction, healing denial and an uncompromising five-round Final Stand.

## Locked move membership, item and parameters

**14 equipped jutsu (no extra roster substitutions):**
- B18 Apex Hunger (40AP self, IDG60/99r + stats25/99r); **once in the opening** to avoid stacking permanent boosts.
- B07 Stolen Form (60AP, range4/CD6, Copy); preferentially use on visibly enhanced targets.
- S34 Purging Stance (40AP, CD5, Cleanse); cast in response to eligible hostile effects.
- B09 Veilstep (40AP, CD6, Stealth 2r); use **early** against long-range kiting only, not the late Final Stand.
- EA04 Zephyr Lance (60AP, range5/CD6, Pierce); destroy shields rather than pretending Pierce scales with IDG.
- B13 Hexweave (60AP, range4/CD8, damage40+IDT40+reduced-healing60+stats reduction15); setup/punish healing.
- B17 Worldbreaker Chorus (60AP, range5/CD10, damage70+Stun2r); high-value follow-up.
- **Exclusive offensive nuke** (working name *Extermination Order*, not yet director-accepted): **80 EP Damage + Elemental Seal 2r + Cleanse Prevent 2r**. Cast **only with active Final Stand**.
- B27 Scorching Rend (60AP, range5/CD6, damage55+wound+afterburn); secondary aggressive pressure.
- B05 Devouring Grasp (60AP, range5/CD6, damage60+drain25/2r); resource punishment.
- B26 Braced Strike (60AP, range5/CD5, damage55+DDT30/2r); attack+defense.
- B20 Surging Overflow (40AP, CD5, IDG30/3r+stats25/3r); preparation while chasing, not constant combat-idling.
- S07 Rapid Fire (60AP, range5/CD2, damage40); reliable attack fallback.
- **Exclusive The Last Directive**: Final Stand **5r**, Increased Damage Given **5r**, Clear Prevent **5r**; **cast at self HP <30%**, with enough pools/AP to execute. **IDG power unspecified**; 40AP/CD99 are proposals, not accepted exact numbers.

**Approved extra active item:** **Countermand**, an AI-only military command-seal item, **not a 15th jutsu**. Initial proposed mechanics: Clear100, **40AP**, range5, cooldown6, single enemy target; must be equipped, usable, non-consumed in a quest battle. In engine source, availableUserActions permits item actions during Stealth and `use_specific_item` selects them. Actual item fields/slot and successful stealth use must be validated from the generated contract + in-process tests. No reward/drop or external usability is implied by the approval.

**Boss innate:** `sealprevent` 100%, 99 rounds. **Profile:** `includeDefaultRules:false`; order the rules explicitly; keep an `end_turn` fallback so missed ranges/cooldowns never cause AI self-forfeit.

**Targets:** `CLOSEST_OPPONENT` consistently for offensive rules and target-conditioned checks; `SELF` for self-buffs, cleansing and Veilstep. Check multi-target/summon behavior; an original human opponent cannot be guaranteed as the target by `CLOSEST_OPPONENT` alone. For pool-jutsu attacks with range5 use native `distance_lower_than:6`; range4 uses `distance_lower_than:5`. The AI distance is path-length based, so Fable must verify actual target reach.

## Native ordered-rule candidate (proposed, not yet accepted as profile)

Use the engine's exact `AiRule.conditions` AND semantics. Each line represents one actual rule, including separate rules when a different status condition triggers the same action. "FS" means `has_effect(effectType:'finalstand',threshold:1)`, never threshold 0. "Stealth" means `has_effect(effectType:'stealth',threshold:1)`. "Target X" means `target_has_effect(effectType:X,threshold:Y,target:'CLOSEST_OPPONENT')`. Every offensive action and distance condition uses `CLOSEST_OPPONENT`; self actions target `SELF`. The AI engine tries later rules when a prior action is unavailable/unaffordable/out of range. Rules are reevaluated after each successful action in a turn.

| # | Conditions (all required) | Action / target | Why |
|---:|---|---|---|
| 01 | `health_below:30` | **The Last Directive** / SELF | Highest priority; one activation via long CD; native boundary strictly <30. |
| 02 | FS + `distance_lower_than:6` | **Extermination Order** / opponent | Signature ultimate first whenever castable; 80EP + elemental seal/cleanse prevention. |
| 03 | FS + `distance_lower_than:6` | **B17 Worldbreaker Chorus** / opponent | 70EP + Stun if ultimate unavailable. |
| 04 | FS + `distance_lower_than:5` | **B13 Hexweave** / opponent | Reapply IDT and heal suppression when the nukes are cooling down. |
| 05 | FS + `distance_lower_than:6` | **B27 Scorching Rend** / opponent | Force pressure through Wound/Afterburn. |
| 06 | FS + `distance_lower_than:6` | **B05 Devouring Grasp** / opponent | Damage and drain while protection remains. |
| 07 | FS + `distance_lower_than:6` | **B26 Braced Strike** / opponent | Keeps attacking with a defensive rider. |
| 08 | FS + `distance_lower_than:6` | **S07 Rapid Fire** / opponent | Prevents an idle offensive phase. |
| 09 | `round_lower_than:3` | **B18 Apex Hunger** / SELF | Opens prepared, with one cast max on its CD. |
| 10 | `round_lower_than:5` + `distance_higher_than:7` | **B09 Veilstep** / SELF | One early anti-kite stealth window; never deliberately re-enter stealth near the final phase. |
| 11 | Stealth + `distance_lower_than:6` | **Countermand** / opponent | **Guaranteed attempt at next-turn Clear** while stealthed, even if limited native buff detection misses the player's setup. |
| 12 | `has_effect(afterburn,threshold:1)` | **S34 Purging Stance** / SELF | Cleanse a relevant ongoing hostile effect. |
| 13 | `has_effect(poison,threshold:1)` | **S34 Purging Stance** / SELF | Secondary cleanse check. |
| 14 | `has_effect(increasedamagetaken,threshold:1)` | **S34 Purging Stance** / SELF | Respond to exposure debuffs; avoid using Purging on nothing. |
| 15 | Target `shield>=1` + `distance_lower_than:6` | **EA04 Zephyr Lance** / opponent | Pierce breaks shields rather than being treated as an IDG-scaling nuke. |
| 16 | Target `increasedamagegiven>=71` + `distance_lower_than:5` | **B07 Stolen Form** / opponent | Copy first; cooldown/fallthrough handle conflicts. |
| 17 | Target `increasedamagegiven>=71` + `distance_lower_than:6` | **Countermand** / opponent | Follow Copy with Clear if 40AP remains, or counter alone. |
| 18 | Target `reflect>=1` + `distance_lower_than:6` | **Countermand** / opponent | Additional buff response. |
| 19 | Target `absorb>=1` + `distance_lower_than:6` | **Countermand** / opponent | Additional buff response. |
| 20 | Target `increasestat>=1` + `distance_lower_than:6` | **Countermand** / opponent | Additional buff response. |
| 21 | Target `increaseheal>=1` + `distance_lower_than:5` | **B13 Hexweave** / opponent | Heal-dependent builds face suppression. |
| 22 | Target `increasedamagetaken>=1` + `distance_lower_than:6` | **B17 Worldbreaker Chorus** / opponent | Exploit already established exposure. |
| 23 | `distance_lower_than:5` | **B13 Hexweave** / opponent | Ordinary setup. |
| 24 | `distance_lower_than:6` | **B17 Worldbreaker Chorus** / opponent | Strong control/damage when setup unavailable. |
| 25 | `distance_lower_than:6` | **B27 Scorching Rend** / opponent | Wound and afterburn. |
| 26 | `distance_lower_than:6` | **B05 Devouring Grasp** / opponent | Drain and damage. |
| 27 | `distance_lower_than:6` | **B26 Braced Strike** / opponent | Consistent offensive/defensive fallback. |
| 28 | `distance_lower_than:6` | **S07 Rapid Fire** / opponent | Offensive filler before chasing. |
| 29 | `round_greater_than:2` + `distance_higher_than:7` | **B20 Surging Overflow** / SELF | Buff while genuinely out of attacking range; movement comes next. |
| 30 | `distance_higher_than:3` | `move_towards_opponent` / opponent | Pursue kiters and close toward melee; works during Stealth. |
| 31 | `distance_lower_than:2` | `use_highest_power_action(effect:'damage')` / opponent | Spend remaining AP on feasible basic/attacking actions. |
| 32 | No conditions | `end_turn` | Always safe; never surrender due to exhausted rule matches. |

**Preliminary sequence:** opening long range = Apex Hunger (40AP) → Veilstep (40AP) → move with remaining AP; while stealthed on the following turn = approach until within 5-range then **Countermand (40AP)**, which can work while hidden; ordinary close combat = Hexweave setup → Worldbreaker/other damage, Copy (60AP) → Countermand (40AP) against eligible buffs. Under Final Stand = The Last Directive → Extermination Order and other aggressive attacks; no deliberate control staggering.

## Mechanical limitations that must not be hidden

1. **Stealth:** All jutsu and basic Clear are disabled while concealed; equipped items/weapons remain available. This is why **Countermand is an item**. Without the equipped item, the anticipated next-round buff-stripping trap does not work. At long range, item range still applies: move first, then Clear when reachable. Sources: `app/src/libs/combat/actions.ts` and `app/tests/libs/combat/seal_stealth.test.ts`.
2. **Native condition expressiveness:** `has_effect` and `target_has_effect` SUM matching raw power, **do not filter persistent/passive sources**, and **do not explicitly filter inactive/expired effects**. A target with bloodline-sourced IDG≥71 may trigger Stolen Form/Countermand despite having no transferable/removable enhancement. Purging may trigger on a stale effect until the next normal effect-processing prune. Target-side remaining HP, gear composition and intention to kite are **not directly selectable**. Don't sell this profile as a cognitive opponent with actual memory or learning. Test failed casts and ineffective Copy/Clear. If the false-positive rate is unacceptable, propose a source-compatible rule change or revised behavior for director approval rather than silently claim accurate detection.
3. **Final Stand check:** Native `has_effect:finalstand` requires **threshold≥1** (0 always passes), and the raw-sum limitation must be tested around the exact expiry action/turn. `FinalStand` protections should not persist after its 5 rounds. `health_below:30` is strictly less than 30; the director's threshold is conceptually 30%. A burst crossing 30→0 before the boss acts may bypass signature activation; calibrate enough practical survival without adding unapproved pre-trigger invulnerability.
4. **Priority interactions:** Native turns carry **100 AP** and will reassess rules after successful actions. Cooldowns, pool costs, movement and range must permit meaningful **40+60** turns. `Countermand`'s Clear participates in shared-Clear cooldowns (3-round global lock against other Clear-tag actions), while **Stolen Form's Copy** does not have the shared-Clear tag, so the Copy60→Countermand40 sequence is plausible but **not yet behavior-proven**.
5. **Weapon/items and loot:** Ensure Countermand's action has active item type (not MATERIAL/CRYSTAL/ARMOR etc.), `equipped` not NONE, positive quantity, `destroyOnUse:false`, cooldown and 40AP. Do not inadvertently grant Countermand to the player or introduce an independent drop. It must also be tested against equipment and action consumption rules.
6. **Behavioral survivability:** With custom `includeDefaultRules:false`, an unsafe profile can **forfeit** if no rule yields a valid action. The ordered move, melee fallback and unconditional `end_turn` explicitly prevent that. Verify out-of-range, obstacles, AP10/20/40, zero CP/SP, high-CD, invisibility and disabled items.
7. **Ultimate:** Damage80+Elemental Seal2r+Cleanse Prevent2r is the director-approved three-tag attack. Native Elemental Seal blocks eligible **60AP elemental jutsu**, not all elemental actions. Confirm actual effects, status duration, damage multiplication, CD and Final Stand gating in offline fixtures.
8. **Story boundary:** The name and characterization are approved. **Do not reveal the directive's unidentified origin until after Arakane's defeat.** Actual game/jutsu/item writes remain reserved for a later Fable-owned implementation contract and user-run live push.

## Acceptance gates before build

- Test 1: opening-distance 3 / 5 / 7 / 9, initiative both ways, Apex Hunger exactly once, Veilstep only during opening long range; no loop.
- Test 2: kiting with ordinary temporary IDG/Reflect/Absorb, inactive buffs and permanent bloodline buffs; measure valid Countermand from Stealth, range after chasing, and Copy60→Countermand40. Confirm players can counter and the boss isn't repeatedly wasting turns on nonremovable buffs.
- Test 3: Shield counter through EA04 and whether it destroys vs merely bypasses the shield.
- Test 4: Turn-by-turn below30 signature at 30.1 / 30.0 / 29.9 / 1 HP and sudden burst across threshold; exact 5-round Final Stand, Clear Prevent and IDG uptime, no second cast, Extermination only with **active** protection, fallback while its attack is cooling.
- Test 5: Heal-dependent, defensive, striker, buffer, kiter, control-build fixtures against Grand Marshal and Ghost Ship benchmarks; damage peaks, time-to-kill, offense cadence, Copy success, Clear effectiveness, AP usage, boss stalling. No new balance number becomes accepted without director decision.

**Next director review:** Approve/adjust the ordered behavior, especially deliberately unconditional Countermand when emerging from Veilstep; settle Countermand item fields and ultimate AP/range/CD/name only after behavioral testing and user balance review.
