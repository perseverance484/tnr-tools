# Supreme Commander Arakane — 20-Rule AI Profile

**Status:** Source-verified *candidate* for director review; no executable AI build or balance acceptance. Replaces the previous invalid **32-rule proposal** at this same path. The superseded rules are retained in Git history, not treated as deployable content.
**Repository:** `perseverance484/tnr-tools@057acddb986b50e486ccf550fac00b68fff51490`; design branch `chatgpt/silent-bastion-design-20261013`.
**Game source:** `studie-tech/TheNinjaRPG@67341a1fa1567b9b33827b802e48120e5d797a15`.
**Owner documents:** `state/silent_bastion_design.md`; `docs/00_INDEX.md`, `docs/DOCTRINE.md`, `skills/building-tnr-content/references/ai.md`, `skills/building-tnr-content/data/32b_DATA_pool.json`.

## Critical correction: hard maximum is 20, not 25

**Source-verified:** `app/drizzle/constants.ts:1723` defines `AI_PROFILE_MAX_RULES = 20`. `app/src/server/api/routers/ai.ts:79–81` returns an error when `input.rules.length > 20`. The `AiRule` validator's unconstrained `z.array` does not override this server cap. **No engine patch is proposed.**

**Exact authored profile:** 20 rules, `includeDefaultRules:false`. The final `end_turn` is mandatory so Arakane never suicides via the native AI give-up behavior when Stealth/cooldowns/ranges exhaust available actions. Do not append the engine's default catchalls: they can select the ultimate outside Final Stand and/or push over the rule limit.

## Director-approved identity and effects (unchanged)

**Display:** Supreme Commander Arakane, dignified and tactically adaptive. Preserve the final twist: freshly generated directives continue arriving after the Supreme Commander falls, and their source is unidentified.

**Approved innate:** 100% `sealprevent`, 99 rounds.

**Fourteen equipped jutsu:**
- B18 Apex Hunger (40AP self; IDG60%/99r + Stats25%/99r; use once early).
- B07 Stolen Form (60AP, range4/CD6; Copy enemy enhancements).
- S34 Purging Stance (40AP/CD5; Cleanse).
- B09 Veilstep (40AP/CD6; Stealth2r). **Superseded by RUL-2026-10-16-007:** use the captured record as-is (Stealth 1 round, cooldown 5); the stealth branch is natively validated with it.
- EA04 Zephyr Lance (60AP, range5/CD6; flat Pierce against shields).
- B13 Hexweave (60AP, range4/CD8; Damage40, IDT40%, reduced healing, reduced stats).
- B17 Worldbreaker Chorus (60AP, range5/CD10; Damage70 + Stun2r).
- **Exclusive Extermination Order** (working name only; **Damage80 + Elemental Seal2r + Cleanse Prevent2r**; only during active Final Stand). **Cooldown 4 approved** (RUL-2026-10-16-004, AR1 mitigation). **Name approved** (RUL-2026-10-16-011).
- B27 Scorching Rend (60AP, range5/CD6; damage + wound + afterburn).
- B05 Devouring Grasp (60AP, range5/CD6; damage + drain).
- B26 Braced Strike (60AP, range5/CD5; damage + defensive buff).
- B20 Surging Overflow (40AP/CD5; offensive buff + stat buff).
- S07 Rapid Fire (60AP, range5/CD2; fallback).
- **Exclusive The Last Directive:** Final Stand5r + IDG5r + Clear Prevent5r, activate once at HP<30%. **IDG 30, 40 AP, cooldown 99 approved** (RUL-2026-10-16-011).

**Approved item identity:** Countermand, an equipped AI-only reusable military command seal. **Approved** (RUL-2026-10-16-011) native item parameters: `itemType:'OTHER'`, `slot:'ITEM'`, `target:'OTHER_USER'`, 100% Clear, 40AP, range5, CD6, `destroyOnUse:false`, positive quantity, `equipped:'ITEM_1'`. No player-facing drop or reward. Confirm compatibility with the current item schema before implementation.

## Equipped items — dedicated Stealth continuity

**Goal:** Veilstep leaves Arakane with no jutsu or basic attack; once close enough, he must have reusable **item** attacks. `app/src/libs/combat/actions.ts` permits equipped weapon/item actions during Stealth and filters out all jutsu and basic attacks. `app/src/libs/combat/ai_v2.ts` supports `use_specific_item` with native distance gates and reevaluates the priority chain after actions.

| Slot | Candidate | Historic seeded stats | Purpose |
| --- | --- | --- | --- |
| ITEM_1 | **Countermand** (approved identity; new item) | Proposed 40AP/range5/CD6; Clear100, reusable | Strip opponent buffs while concealed, can pair with Copy60 in normal combat. |
| HAND_1 | **Solar Bow** (existing item) | **40AP, range5, CD3, not consumed** | Long-range weapon response while concealed or after a 60AP jutsu. |
| HAND_2 | **Crossbow** (existing item) | **40AP, range3, CD0, not consumed** | **Repeatable close-range weapon action** after Arakane has approached; no need to wait for a jutsu or cooldown. |

**Provenance limitation:** Solar Bow and Crossbow stats above are from the pinned game's **historical `app/data/item.sql` seed**, not a fresh live readback. The seed holds Solar Bow id `ALqXVSL58QMfJ4DgoJ5Il` and Crossbow id `LbccOnzfsADLgTBPSHjKK`. Verify the *current* full item records, weapon equip limits, AI equipment quantities, cooldown and availability from a fresh approved capture before constructing the manifest. The game has HAND_1 and HAND_2 slots and permits multiple hand weapons absent a specific restriction, but this combination still requires an actual loadout test.

**Chakra Pill II:** Exists in the historic item-name index (`nThwqBAKNrl1_4UTL-D_m`, CONSUMABLE). Its **current effects, cost, cooldown and `destroyOnUse` are not verified** here. Do **not** treat it as guaranteed CP recovery, or use finite consumables as the only Stealth fallback. It may be added later as optional AI utility if a rule slot is intentionally reassigned and fresh capture proves it helps. The two repeatable weapons above are the current safety proposal.

## Ordered 20-rule candidate

Targets: `CLOSEST_OPPONENT` for enemies, `SELF` for all self-actions. Every enemy-targeting single-target rule uses the **exact path-distance gate** (`range+1`), from the shared pool/source rule: range5 → `distance_lower_than:6`, range4 → `distance_lower_than:5`, range3 → `distance_lower_than:4`. Special move distances remain intentional. Opponent buff checks use `target_has_effect` with the same target selector as the action.

| # | Native conditions | Action (target) | Intent |
| ---: | --- | --- | --- |
| 01 | `health_below:30` | **The Last Directive** (SELF) | Top priority; native strictly <30%. CD protects once-only activation. |
| 02 | `has_effect(finalstand,threshold:1)` AND `distance_lower_than:6` | **Extermination Order** (CLOSEST_OPPONENT) | Ultimate only in active Final Stand (requires expiry validation). |
| 03 | `round_lower_than:2` | **B18 Apex Hunger** (SELF) | Opening preparation only; prevents permanent stacking loop. |
| 04 | `round_lower_than:5` AND `distance_higher_than:7` | **B09 Veilstep** (SELF) | Early anti-kiter concealment when target is beyond attack reach. |
| 05 | `has_effect(stealth,threshold:1)` AND `distance_lower_than:6` | **Countermand item** (CLOSEST_OPPONENT) | Priority Clear while Stealthed, even if player uses non-IDG buffs. |
| 06 | `has_effect(afterburn,threshold:1)` | **S34 Purging Stance** (SELF) | Clear damaging debuff if present and no Stealth lock. |
| 07 | `target_has_effect(shield,threshold:1)` AND `distance_lower_than:6` | **EA04 Zephyr Lance** (CLOSEST_OPPONENT) | Destroy an active target shield. |
| 08 | `target_has_effect(increasedamagegiven,threshold:71)` AND `distance_lower_than:5` | **B07 Stolen Form** (CLOSEST_OPPONENT) | Copy strong buffs before stripping. |
| 09 | `target_has_effect(increasedamagegiven,threshold:71)` AND `distance_lower_than:6` | **Countermand item** (CLOSEST_OPPONENT) | Clear target after Copy, if AP and CD permit. |
| 10 | `distance_lower_than:5` | **B13 Hexweave** (CLOSEST_OPPONENT) | Setup vulnerability/heal suppression. |
| 11 | `distance_lower_than:6` | **B17 Worldbreaker Chorus** (CLOSEST_OPPONENT) | Damage + Stun; prioritize over less powerful attacks. |
| 12 | `distance_lower_than:6` | **B27 Scorching Rend** (CLOSEST_OPPONENT) | Wound/Afterburn pressure. |
| 13 | `distance_lower_than:6` | **B05 Devouring Grasp** (CLOSEST_OPPONENT) | Damage + drain. |
| 14 | `distance_lower_than:6` | **B26 Braced Strike** (CLOSEST_OPPONENT) | Damage + defense. |
| 15 | `distance_lower_than:6` | **S07 Rapid Fire** (CLOSEST_OPPONENT) | Attacking fallback, including Final Stand cooldown gaps. |
| 16 | `distance_higher_than:7` | **B20 Surging Overflow** (SELF) | Refresh offensive preparations only while truly at range. |
| 17 | `distance_lower_than:6` | **Solar Bow item** (CLOSEST_OPPONENT) | 40AP ranged weapon to spend AP during Stealth or after 60AP jutsu. |
| 18 | `distance_lower_than:4` | **Crossbow item** (CLOSEST_OPPONENT) | 40AP **zero-CD** repeatable fallback after closing distance. |
| 19 | `distance_higher_than:3` | `move_towards_opponent` (CLOSEST_OPPONENT) | Pursue while hidden or at range; reevaluate items when near. |
| 20 | *(none)* | `end_turn` | Guaranteed safe fallback; no AI forfeit when no legal action remains. |

**Notes on ordering:** When stealthed, almost all jutsu rules fail action availability; rule 05 attempts Countermand, rule 17 uses Solar Bow, rule 18 uses the zero-CD Crossbow when in range, then rule 19 moves closer, and rule 20 ends safely. At close range, Crossbow can spend 40AP repeatedly if the engine allows repeat item use that round; this is a required test, not assumed as measured fact. In normal combat, 60AP jutsu plus 40AP weapon/Countermand supports full-turn spending. There is no `use_highest_power_jutsu`/generic damage fallback, which could accidentally select Extermination Order before Final Stand.

**True 20-rule count:** exactly 20 rows; `includeDefaultRules:false`. The old 32-rule table must NOT be built; it exceeds the live server maximum by 12.

## Source caveats and tests before acceptance

- **Native condition blind spots:** `has_effect` and `target_has_effect` sum raw matching effect power without explicit active/source filtering. If an expired Final Stand tag remains visible before pruning, rule02 could erroneously fire the ultimate. Test phase boundary precisely; if this cannot be reliably gated under the native AI selector, **flag the blocker and propose a safe alternative instead of weakening the user's only-while-active requirement**. IDG≥71 may be passive/non-copyable; count wasted Copy/Clear casts.
- **Weapon action safety:** Confirm the specific weapon records are nonconsuming, equipped and positive-quantity, have correct battle-usage flags, viable durability, target methods, cooldowns, and current AP/ranges. Verify two HAND slots are populated and are not unequipped by loader. Damage weapons should not share a blocking cooldown for pure damage; `damage` is absent from `SHARED_COOLDOWN_TAGS` (`app/drizzle/constants.ts`).
- **Stealth path:** Against far-range kiter, test round0–4, movement until range5 for Countermand/Solar Bow, then range3 for Crossbow. Exercise both Stealth rounds, weapon attacks, AP left at 40/20/10, crowded tiles and chase failure. End-turn must never self-forfeit. Verify item use and the 3-durability-per-weapon-use rule in quest battles.
- **Final phase:** Test HP ratios 30.1/30.0/29.9/1, CP/SP shortages, exact Final Stand five-round activation/expiry, Clear Prevent strength, ultimate cast cadence under ongoing Final Stand, and clean disable on expiry. The desired signature 40AP / 99-CD and ultimate 60AP / range5 / CD are **proposed**, not director-approved numeric decisions.
- **Opponent fixtures:** Healers, shields, buff-heavy, high-IDG bloodlines with uncopyable effects, durable melee, ranged kiting, stun/seal strategies. Compare difficulty to Crowned Captain and the other Bastion commanders; do not invent acceptance thresholds.
- **Safety:** Design only. Do not create a game manifest, change source, request credentials, call live game, or publish without a separate director-approved workflow.

**Next decision:** Approve the two-weapon Stealth fallback and the condensed 20-rule profile direction. Then Fable can construct and offline-test an exact schema-correct candidate using current records; all balance and player-facing content stay with the director.
