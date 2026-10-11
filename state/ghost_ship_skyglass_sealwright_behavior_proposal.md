# Sealwright — combat behavior proposal

**Status:** REQUESTED DESIGN COMPLETE; DIRECTOR ACCEPTANCE AND NEW-PIN OFFLINE TESTS PENDING. This is a behavior proposal, not a manifest, new balance ruling or parity claim.

**Owner:** `state/ghost_ship_skyglass_sealwright_combat_draft.md` retains the accepted encounter identity. This companion supplies the proposed next behavior for Fable. The original `state/ghost_ship_skyglass_sealwright_rule_contract.json` and Stage 2 harness remain unchanged historical test inputs.

**Design base:** `perseverance484/tnr-tools@fcd79e5a3401dc8d95abbdaa05d0d4664c04a6e2`. Remote checks on 2026-10-11: main `50f980f08dfcc798723c26243b9399cc0a97911a`, frozen r4 branch `3f825562ea051306a3803f47428b742ae5100011`; the active-Consume implementation branch was absent remotely. Engine source checked: `studie-tech/TheNinjaRPG@585534d7eb21d6f0dd678d5c3eb92662f611d39b`, not a verified deployment.

## Player experience

A methodical containment fighter who strips enhancements, reinforces his ward and advances while applying pressure. He uses a ranged technique when one is available, then uses spare action points to approach and strike. Direct pressure, protected buffs and timing around his defensive/Clear cooldowns remain meaningful responses.

Keep the accepted seven techniques unchanged. Keep Level100/JONIN, stats3x, pools2.5x and regeneration60 as the starting profile; no new innate buff, armor, weapon, summons, phase or independent loot. Full preferred-stat/general/element fields remain a separate record-freeze gate; the existing Captain-derived numeric test carrier is not silently accepted as the final profile. The Reliquary remains a quest-end reward.

## Exact proposed priority

Rules restart from the top after each action. This is a priority list, not a guaranteed round-by-round combo. Use `includeDefaultRules:false` and explicit actions only.

| Priority | Action | Native condition/target | Intended behavior |
| --- | --- | --- | --- |
| 1 | **B32 Nullifying Wave** | `target_has_effect`, `increasedamagegiven`, threshold71, CLOSEST_OPPONENT; `distance_lower_than:6` on that same target | Emergency purge only. Preserve the director's exact native threshold and gate. Unavailable action falls through. |
| 2 | **S31 Unraveling Strike** | CLOSEST_OPPONENT; `distance_lower_than:4` | Routine high-priority damage plus Clear, including against an unbuffed opponent. |
| 3 | **B22 Compression Barrier** | SELF; no condition | Restore the ward whenever the action is available. Its existing cooldown limits repetition. |
| 4 | **B16 Sovereign Fetters** | CLOSEST_OPPONENT; `distance_lower_than:6` | Apply damage and the existing AP reduction/bloodline seal. |
| 5 | **B14 Cataclysm Detonation** | CLOSEST_OPPONENT; `distance_lower_than:6` | Main heavy damage attack. |
| 6 | **B33 Piercing Judgment** | CLOSEST_OPPONENT; `distance_lower_than:6` | Piercing pressure and vulnerability for subsequent damage. |
| 7 | **S27 Weakening Strike** | CLOSEST_OPPONENT; `distance_lower_than:6` | Damage and offensive suppression when higher priorities are unavailable. |
| 8 | **Basic Attack** | CLOSEST_OPPONENT; `distance_lower_than:2`; `use_combo_action` with the singleton `comboIds:["basicAttack"]` | One native basic strike when adjacent and available. No broad random/highest-power/default selector. |
| 9 | **Move toward opponent** | CLOSEST_OPPONENT; `distance_higher_than:3`; `move_towards_opponent` | Spend spare AP approaching adjacency after available attacks. Reevaluate from priority1 after each step. |
| 10 | **End turn** | unconditional `end_turn` | Safely finish when no preceding action is executable. |

Distances above are native path lengths including endpoints, not displayed hex distances. The original proactive movement rule before B16 is removed. Keep all original jutsu IDs, mechanics and relative jutsu ordering; the only behavior changes are late movement, restricted basic filler and explicit termination. Do not add a second range-closing rule before the named attacks.

**AP examples (source-based, not new combat results):** native Basic Attack is20AP, range1, JONIN cooldown1; movement is10AP per adjacent step. A60AP technique plus two steps plus one basic can fit100AP from hex distance3 on an unobstructed path when all actions are available. At adjacency, a60AP technique plus basic uses80AP; the remaining20 can legitimately be unused. A40AP ward plus a60AP technique consumes the full turn. Do not promise two basics or a fabricated40AP filler. The movement goal is adjacency, not stopping at S31's range3, which would leave basic attacks mostly unused.

## Locked engine limitations and counterplay

- Both Clears remain. They share the native three-round Clear GCD, so they cannot alternate every round or cast together. S31 also deals damage when its Clear removes nothing.
- B32's condition sums raw matching effect power. Threshold71 is the approved integer approximation to strictly greater than70:70.5 does not trigger. Expired/protected IDG and Clear Prevent can produce an empty B32. Do not silently replace the predicate with an invented “removable active IDG” test.
- CLOSEST_OPPONENT may be a summon. B32's ALL method can clear other opponents outside the trigger's distance gate; the gate restricts selection, not every recipient.
- B16's measured old-pin Stun100/2r is minus20AP in each of the next two rounds, with bloodline seal. It is not two rounds of complete lockout. Recheck on the new pin.
- Ordinary Clear can remove eligible active Consume and generated shields. Include the approved2/2 items in the next interaction checks; do not weaken the accepted anti-buff identity to protect the new rewards.
- No new health-based enrage or stronger statistics are proposed. Fights should retain recovery opportunities when ward/control are unavailable.

## Evidence and Fable comparison

Corrected r3/r4 A2 reports **boss wins/losses**. Sealwright lost to the durable striker0/5 in31 rounds; Captain won5/0 in22. Against the durable buffer, Sealwright won5/0 in39 and Captain lost0/5 in11. Across carriers Sealwright had lower spikes and longer fights, but much stronger buff suppression. Five repeated deterministic seeds in a single-opponent fixture are not a player-population win-rate estimate. These results belong to old engine `cddd7d91...`; the new item tests did not rerun A1/A2 or prove parity.

After director acceptance for testing, Fable compares at the same pinned engine and identical capped/assembled fixtures:

1. Accepted five-move regular Captain, preserving captured innate effects and actual equipment eligibility.
2. Historical Sealwright rules, rerun at the new pin as the control.
3. Late movement without basic filler, to isolate movement effects.
4. The full proposed late-movement/basic candidate above.

Exercise all six existing player carriers; fixed near/medium/far starts; obstacles, blocked movement, adjacency, multiple opponents and summon interception. Verify the singleton basic selector,20AP cost/cooldown and no repeated basic; range gates; B32 boundary69/70/70.5/71/90 and unavailable fallthrough; shared Clear GCD; routine S31 even without buffs; B22 cadence; B16 actual AP timeline; no movement starvation or exhaustion. Include active2/2 Consume, shields, protected buffs and Clear Prevent.

Measure complete-step direct/delayed damage, spikes, fight duration/outcomes, AP use, recovery windows, ward/IDG uptime and removing versus empty Clears. Keep initial preprocessing and no-DB/no-network boundaries faithful to the real engine. Retain fail-closed evidence and two-run reproducibility. No engine edits.

**Acceptance remains director-owned:** judge practical Captain-tier difficulty across damage-oriented and buff-dependent builds. Do not silently adopt a numeric tolerance or tune solely to reverse the striker loss. If the candidate improves ordinary pressure but makes the buffer fight excessively punishing, report that tradeoff before adjusting locked jutsu or statistics. Independent review follows Fable's frozen test SHA; this proposal alone does not freeze combat or authorize manifest construction.

## Source anchors

- New engine `app/src/libs/combat/actions.ts:463–491,610–628`: basic strike and movement cost/range/cooldown.
- `app/src/libs/combat/ai_v2.ts:88` and `actions.ts:291–310`: AI requests cooldown-filtered actions; unavailable basics are removed before selection.
- `app/src/libs/combat/ai_v2.ts:306–376,402–413,464–476,502–518,719–758`: predicates, one-step movement, singleton combo selection, fallthrough and combo progression.
- `app/src/validators/ai.ts:226–234,323–356`: combo grammar and broad backup rules that this proposal intentionally does not enable.
- `docs/reviews/GHOST_SHIP_SKYGLASS_STAGE2_OFFLINE_RESULTS.md`, section4: corrected A2 measurements and limitations.
- `docs/reviews/GHOST_SHIP_ACTIVE_CONSUME_SOURCE_DRIFT.md`, sections2–4: new-pin initialization/target/effect drift and historical measurement boundary.

No live-game or CDN request, credentials, art change, engine edit or manifest was involved in this design.
