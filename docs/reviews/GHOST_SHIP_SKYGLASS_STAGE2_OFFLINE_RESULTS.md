# Ghost Ship / Skyglass Stage 2 — offline test results (Fable Lane A)

**Status: OFFLINE TEST PACKAGE COMPLETE (r3 correction pass). RELEASE STILL BLOCKED.** M0, A1, A2, B1, B2, B3, C1, C2 and C3 were executed against actual pinned engine code and PASS on their stated scope. C3 passed after the Night's Testament baseline was accepted (RUL-2026-10-11-004, revision 2026-10-11 r2); Katana presentation fields remain pending. Crystal production validity is BLOCKED by the validator (B1 is an expected-rejection PASS). Sealwright parity is measured, not accepted.

**Revision r3 (2026-10-11) supersedes every r1/r2 combat figure in §3 and §4.** ChatGPT's independent review of r2 (`2c64c9e5…`, findings F1–F6) found that the harness skipped `initiateBattle`'s battle-start stat caps, that a failed evidence check did not fail execution, and that several A2 metrics and the A1 cadence denominator were wrong. All are corrected and A1/A2 regenerated. The correction ledger is in the handoff's r3 section. M0, B1, B2, C1 and C3 evidence is byte-identical to r2. B3 and C2 recorded data is unchanged; only their checks were replaced or added.

**Date:** 2026-10-11. **Implementer:** Fable (Claude Code). **Independent reviewer:** ChatGPT, at the frozen SHA. **Decisions:** dauntless.
**Governing briefs:** `state/prompt_ghost_ship_skyglass_stage2_feasibility.md` (test contract) and `state/prompt_ghost_ship_skyglass_stage2_start.md` (execution packet), at input commit `61373538035d41f7e773ec082b739740cdf0860e` (RUL-2026-10-11-003).
**Harness and evidence:** `harness/ghost_ship_stage2/` (README, runner, tests, `results/*.json`). **Engine proposal:** `docs/design/GHOST_SHIP_CRYSTAL_ENGINE_CORRECTION_PROPOSAL.md`.

## 1. Gate summary

| Gate | Status | What actually executed | Evidence |
| --- | --- | --- | --- |
| **M0** | **PASS** | 482 deterministic checks: 4 capture/registry SHA-256 pins; 65 memberships resolve to exact full records; 11 retained protected-field hashes (all repeated copies identical); 11 AI and 11 profile hashes and linkage; innate arrays (duplicates kept); baseline numeric profiles; Captain/Crowned/Sentinel/First Blade boundary checks; Sealwright's 7 records; embedded-vs-pool field drift equals the packet's declared lists (absent ≠ null) | `results/m0.json` |
| **A1** | **PASS** | All 11 AIs assembled with `initiateBattle`'s battle-start preprocessing (rank caps, then the engine's `processUsersForBattle`). Battle-start stats asserted equal to min(stored, JONIN cap). Captured / kit-only / candidate-rule variants. 20-round cadence against a passive dummy at hex 3 and 7 over the full 20-round interval. 9 fights per variant. Hazard trigger tests. Crowned dormant-support check. 207 evidence assertions, 0 failed | `results/a1.json` |
| **A2** | **PASS** (measurements, parity not accepted) | Sealwright selector matrix: IDG 69/70/70.5/71/90, gate distance, B32 unavailable ×4 (incl. exact Clear-GCD release), summons and second opponents, blocked path, new/expired/protected IDG, Clear Prevent, S31 routine. Battle-start caps on Captain and carrier. B16 AP-reduction timeline. 120 full fights: Captain vs 3 Sealwright rule variants × 6 player fixtures × 5 seeds, with reconciled damage attribution, AP-based lockout and state-diff Clear accounting. 39 assertions, 0 failed | `results/a2.json` |
| **B1** | **PASS** (expected rejection). Production Crystal **BLOCKED** | The real item `effects` schema and the full `ItemValidator` reject `[consume 20%]` with exactly `ConsumeTag must be used together with a damage or pierce effect on the same action` | `results/b1.json` |
| **B2** | **PASS** (post-composition runtime only) | Real assembly composes weapon + imbuement. Weapon action produces a 20% pre-shield-basis shield, 3 rounds. Shielded target, multi-target aggregation, no-damage recipient, Consume-on-Consume all tested | `results/b2.json` |
| **B3** | **PASS** | Real `occupation.imbueItem` and `craftItem` procedures, read-only stub client (writes trapped): WEAPON-only, non-imbuable recipients, duplicates, slot limit, equipped item, occupation. Every cell of the imbue and craft rank × rarity matrices is asserted against a source-derived expectation. Battle-side suppression of old imbuements. 14 assertions. Scope: tested pre-write eligibility guards only; persistence and concurrency guards (snapshot claim, atomic consume) were not run | `results/b3.json` |
| **C1** | **PASS** | The accepted Pierce 50 (Crystal) + SELF immunity(buffprevent, 2r) + Consume 40% parses. `maxImbueNumber` 0 is rejected and 1 accepted. The full `ItemValidator` accepts the accepted record (presentation placeholders) | `results/c1.json` |
| **C2** | **PASS** | Real weapon action using the accepted record: 40% shield, pre-shield basis, aggregation, absorption and exact expiry, item-level scaling, exact immunity window and post-window application against a captured Buff Prevent jutsu, cooldown 6 / full shared-GCD lock and release / AP 40. 18 assertions | `results/c2.json` |
| **C3** | **PASS** (mechanics and economy; presentation pending) | `state/ghost_ship_skyglass_katana_record.json` is derived from the push/85 Night's Testament row. Every non-override field equals the capture. The overrides are exactly the ruling-cited set. The full `ItemValidator` passes, and 9 contract invariants hold (LEGENDARY SWORD, not imbuable, exactly three effects, Pierce 50 Crystal, SELF immunity 2r, Consume 40 SELF, drop-only, tradable, created hidden). 12 assertions | `results/c3.json` |

Commands and outcomes (§7) are exact. The engine suite reported `73 pass, 0 fail, 174 expect() calls, Ran 73 tests across 4 files`, exit 0. Every evidence file passed `tools/check_evidence.py`, and the negative gate-enforcement self-test failed at every layer as required. Two independent full runs produced byte-identical evidence for every gate.

## 2. Source, dependency and fixture provenance

- **Engine execution pin:** `studie-tech/TheNinjaRPG@cddd7d91c9e6bdebc978ddcb61e5b8a305bd0f93` (pin B). It is exported with `git archive` into a disposable directory, and the upstream working tree is unchanged. `bun.lock` sha256 `da6602f2…1906c08`; runtime bun 1.4.2, node v22.22.0, python 3.13. Dependencies were installed with `bun install --frozen-lockfile --ignore-scripts` (approved by the user for this session). Tests ran in `unshare -rn` with upstream CI placeholder environment values and no database.
- **Drift assessment.** A=`4774560e` (historical AI pin) → B: only `validators/ai.ts`/`ai_v2.ts` change, adding COORDINATE action targets. No Ghost Ship or Sealwright rule uses them. B → C=`1853b6ab` (the readiness review's observed HEAD): `supportsNpcAllies()` makes **QUEST**/OVERWORLD battles choose enemies and allies by battlefield side instead of village/controller (`ai_v2.ts`, `actions.ts getTargetUser`, `participants.ts`). That change also affects `combat.ts` setup/spawn. Every fixture here has opponents that differ in both village and side, so the measured outcomes do not depend on that change. **Re-run the harness at the deployed pin once it is known.** Upstream HEAD moved again during this session (`0b730e9f`). That is not evidence of deployment.
- **Captures (committed, hashed by M0):** AI `harvests/inbox/tnr_results_1790826836406.json`, profiles `…1790828718767.json`, pool `…1791583362574.json`, registry `skills/building-tnr-content/data/32b_DATA_pool.json`. Katana: accepted record derived from Night's Testament `…1791727479372.json#/captures/0/data` (push/85). Carriers: Flaming Sword `…1788235198666.json#/captures/8/data/items/0/item` (Crystal and imbuable-recipient non-effect fields, EPIC SWORD), Seal of Nullification `…1789188714166.json#/captures/13/data` (Buff Prevent), Rose Sanctuary `…1791247737840.json#/captures/52/data` (Clear Prevent), plus Light Barrier, Cataclysm Fist, Ion Lance and Heavy Cut from the pool capture.
- **Schema conversion (important).** The October 1 AI rows predate upstream migration `0056_unified_combat_stats_masteries.sql` (commit `46f62cd9`, 2026-10-08). Pins A, B and C all fight with `offence`/`defence`/`*Mastery`, which those rows lack. Unconverted, the bosses deal near-zero damage. The harness applies the migration's **AI branch verbatim** (`offence`=max of 4 offences, `defence`=max of 4 defences, mastery=max(off,def), bloodline/sage mastery 10). This is a source-defined conversion, not tuning. The operator post-migration recapture push/86 (2026-10-11) confirmed it: live offence, defence and masteries equal the conversion exactly for all eleven AIs.
- **Battle-start preprocessing (r3, F1).** `initiateBattle` caps every fighter with `capUserStats` before `processUsersForBattle`; r1/r2 skipped this. The harness now deep-clones each input, caps it at its own rank (QUEST is not ranked; the captured Ghost Ship quest objectives `opponentAIs` carry no `scaleStats`, so `scaleTarget` is false), and applies the post-assembly steps (`applyPoolAdjustmentsToBase`, `refreshMasteries`, aggressor flag). All eleven AIs are JONIN. All exceed the JONIN generals cap of 400,000 (stored generals 556,520–1,329,367 after 0056), so every AI fights with 400,000 in strength, intelligence, willpower and speed. Only Core Canister also exceeds the offence/defence cap (1,329,367 → 1,300,000). Captured records are unchanged. Still not reproduced: random start tiles and random initial ground barriers.
- **Not read:** live `gameSetting` damage overrides (`dmgConfig` uses source defaults), live player populations, deployed version.

## 3. A1 — eleven accepted kits

**Preserved (asserted after real assembly, all 11):** the assembled membership equals the accepted kit. Numeric profile is identical between captured and accepted assembly: level, rank, multipliers, regeneration, pools, offence/defence, generals, preferred generals, elements. Innate effects are realised identically, including duplicates, and remain protected from Clear (`fromType` bloodline). Item rows keep their `equipped`/`dropChancePerc`. Every kit jutsu is an available action in round 1. No stat compensation exists anywhere.

**Behaviour (candidate = captured rules with jutsu IDs remapped through the accepted mapping):** there were no AI-exhaustion give-ups and no cooldown violations in any variant, at either distance, in any fight. Every cadence run covered the full 20-round interval with the dummy alive. Damage per round against the cadence dummy (hex 3; captured → kit-only → candidate; r3: capped stats, divided by the 20 completed rounds):

| AI | captured | kit-only | candidate | Note |
| --- | ---: | ---: | ---: | --- |
| Deck Warden | 6897 | 4712 | 4255 | Smaller shared attacks replace the ghost combos |
| Core Horror | 17185 | 17945 | 12532 | |
| Oathkeeper | 12256 | 7505 | 6682 | |
| Wayfinder | 16699 | 8105 | 8580 | |
| Arsenal Keeper | 8436 | 5378 | 5290 | |
| Sentinel | 10189 | 9346 | 8447 | |
| First Blade | 14085 | 8003 | 7413 | |
| The Captain | 1078 | 1078 | 1078 | Kit and rules unchanged |
| Crowned Captain | 2405 | 2020 | 2269 | Kit-only loses the Sharpened Focus rule; the remap uses EA03 |

The kit-only column shows rules falling through to default/backup rules when they reference removed IDs. It is not a proposed configuration. With the candidate remap, every AI uses its accepted kit. The accepted substitutions are weaker attacks, as the packet disclosed ("role substitutes, not equal-strength copies"). Per RUL-2026-10-11-003 nothing was compensated.

**Observation for the director (no change made):** the seven non-hazard minions carry preserved **duplicate innate IDG** entries. They hold +200% to +350% for 99 rounds, plus shorter entries, for totals of +350% to +420%; for example Wayfinder is 100+100+100+50, all 99 rounds. Under source-default damage settings and battle-start caps, they out-damage the regular Captain per round against the cadence dummy by 3.9–11.6× (candidate rules) and 6.4–15.9× (captured). Against the three player fixtures they won all 9 fights per variant, in a mean of 1.0–3.0 rounds. This comes from the captured data and the 0056 conversion, not from the kit change.

**Hazards (Seal Charge, Core Canister):** the original ID `nCQETf-HNnbRec1OSY2-R` is kept. They wait in rounds 1–2 / 1–6 with no exhaustion (end_turn fallback → `wait`). In round 3 / 7 they cast Core Rupture, spending 100 AP, self-destructing (one-hit-kill SELF), and dealing Pierce 120 (×2 dmgModifier) plus Stun −60 AP to the opponent (4,676 / 3,927 damage to the dummy). **Core Rupture is ALL-method:** at hex distance 8 it fired on the same round and reached the opponent, because the nominal range 5 does not limit ALL. This is identical in all three variants.

**Crowned Captain dormant support:** across 10 fights each, the captured and candidate rules selected Second Wind, Stolen Form and Rebounding Form **zero times**, so the equipped support stays dormant. A labelled **unapproved** proposal rotation was also run (Second Wind <50% HP; Stolen Form when the closest opponent has IDG ≥30 within 5; Rebounding Form within 3). It used Rebounding Form (Oct 1 name Counter Stance) 10× and Stolen Form 5×. The boss still won 10/10, with mean length 3.5 → 4.0 rounds and mean boss HP left 94.3% → 87.2%. This is evidence for the activation decision only.

## 4. A2 — Sealwright selection and Captain comparison

**Selector matrix (contract rules, single decisions on assembled battles):**

| Case | Result |
| --- | --- |
| IDG 69 / 70 / 70.5 / 71 / 90 at hex 3 | S31 / S31 / S31 / **B32** / **B32**. Integer threshold 71 uses `>=`, so 70.5 does not trigger |
| IDG 90 at hex 4 / 5 / 6 | B32 / B32 / B22. Gate 6 is path length = hex distance + 1 |
| B32 on cooldown; only 40 AP left | S31; B22 |
| B32 "no pools" | Still B32. AI pool cost for B32 is 0/0/0, so pools never gate it |
| **After S31, a fresh IDG 90 each round** | **B32 is unavailable for 2 rounds and returns in round +3**: S31 and B32 share the `clear` GCD (`SHARED_COOLDOWN_ROUNDS` = 3) |
| Closest summon with low IDG, farther player with IDG 90 | S31 on the summon. The player's buff stays |
| Closest summon with IDG 90, player with IDG 60 behind it | B32 clears **both** (ALL method) |
| Closest player IDG 90, second player far outside the gate | B32 clears **both** |
| Barrier wall making hex 5 a path >6 | No B32 |
| IDG with `rounds:0` (expired, still in the array) | **B32 still cast**: the condition sums raw power without an active check |
| Protected (bloodline-source) IDG 90 | B32 cast; IDG **not removed** |
| Clear Prevent (Rose Sanctuary effect) + IDG 90 | B32 cast; nothing removed |
| Newly cast IDG (isNew/castThisRound) | B32 cast and the IDG removed |
| No buffs or IDG 50 at hex 3; no buffs at hex 4 | S31; S31; B22 |

**Deliberate double Clear (approved intent) is limited by the engine.** Neither Clear can follow the other within 3 rounds. A same-round S31 + B32 is impossible, both for this reason and because a 60 + 60 AP pair does not fit in 100 AP. The approved overlap still happens across GCD windows.

**B16 Sovereign Fetters control:** Stun 100/2r reduces AP by **20 per round** for rounds +1 and +2 (0 in the cast round), asserted as the exact engine AP-reduction timeline [0, 20, 20, 0]. It does not lock the player out. Seal 100/2r seals the **bloodline**. This is weaker control than "2r stun+seal" suggests; it is the captured shared record unchanged.

**40+60 AP capacity:** no exhaustion in any of 120 fights. The contract profile has `includeDefaultRules:false` and no 40-AP filler after B22's cooldown, so Sealwright often uses only 60 AP and then `wait`s (9–30 waits per fight; active AP 50–67 per round). The Captain fills spare AP with basic attacks from the default rules (active AP 48–75 per round).

**Metric definitions (r3, F3/F4).** The r2 values in this section are superseded:

- **Boss damage** is every player HP loss across whole steps, including delayed ticks that resolve during the player's turn or at round transitions. Step deltas plus the residual reconcile exactly to final − initial HP in every fight (asserted). Player kits carry no health cost and no self-damage (asserted), so all player HP loss is boss-side. r2 counted only HP lost inside the boss's own actions and missed the Captain's delayed 505-HP ticks.
- **Stunned rounds** is stun presence at round start. Under the engine's `calcApReduction` that never removed more than 20 AP, and **full lockout** (a reduction removing all 100 AP) occurred in **0** rounds of all 120 fights. r2's "lockout rounds" counted stun presence.
- **Clears** are split into removing (at least one positive, removable effect on the player side disappeared during the action) and empty. r2 counted success text, which appears even when nothing was removed.
- **Sampling** is one round-start sample per distinct round. r2 could add a duplicate terminal sample.
- **Cadence** damage (§3) is divided by the completed 20-round interval, not by the round index 21.

**Full comparison (mean per fight; each cell is 5 identical seeds; start hex distance 6; B=boss wins, P=player wins; r3):**

| Player fixture | Boss | B/P | Rounds | Boss dmg (direct + delayed) | Spike/action (%maxHP) | Stunned rounds (−20 AP) | Full lockout | Recovery windows | Player IDG uptime | Boss defence uptime | Clears removing / empty (B32) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| JONIN cap, buffer | Captain | 5/0 | 10 | 5050 (4040 + 1010) | 30% | 2 | 0 | 1 | 0.90 | 0.00 | 0 |
| | Sealwright (all 3 variants) | 5/0 | 14 | 5050 (5050 + 0) | 16% | 3 | 0 | 4 | 0.29 | 0.64 | 3 / 1 (2) |
| JONIN cap, striker | Captain | 5/0 | 10 | 5050 (4040 + 1010) | 19% | 2 | 0 | 0 | 0 | 0.00 | 0 |
| | Sealwright (all 3) | 5/0 | 13 | 5050 (5050 + 0) | 16% | 3 | 0 | 3 | 0 | 0.61 | 0 / 3 (0) |
| JONIN half, moderate | Captain | 5/0 | 5 | 5050 (4482 + 568) | 28% | 2 | 0 | 0 | 0.60 | 0.00 | 0 |
| | Sealwright contract | 5/0 | 7 | 5050 (5050 + 0) | 24% | 2 | 0 | 1 | 0.43 | 0.57 | 2 / 0 (0) |
| | Sealwright no/late closing | 5/0 | 9 | 5050 (5050 + 0) | 24% | 2 | 0 | 2 | 0.33 | 0.67 | 2 / 0 (0) |
| Durable (pools ×2.5), buffer | Captain | **0/5** | 11 | 5394 (4384 + 1010) | 13% | 2 | 0 | 1 | 0.91 | 0.00 | 0 |
| | Sealwright (all 3) | **5/0** | 39 | 12625 (12625 + 0) | 6% | 8 | 0 | 13 | 0.28 | 0.61 | 10 / 1 (4) |
| Durable, striker | Captain | **5/0** | 22 | 12625 (9832 + 2793) | 8% | 5 | 0 | 0 | 0 | 0.00 | 0 |
| | Sealwright (all 3) | **0/5** | 31 | 11063 (11063 + 0) | 6% | 6 | 0 | 9 | 0 | 0.58 | 0 / 6 (0) |
| Durable, moderate | Captain | 5/0 | 20 | 12625 (10605 + 2020) | 14% | 4 | 0 | 3 | 0.80 | 0.00 | 0 |
| | Sealwright contract | 5/0 | 34 | 12625 (12625 + 0) | 6% | 7 | 0 | 10 | 0.47 | 0.62 | 7 / 0 (0) |
| | Sealwright no/late closing | 5/0 | 34 | 12625 (12625 + 0) | 6% | 8 | 0 | 9 | 0.47 | 0.62 | 7 / 0 (0) |

Boss pools never dropped below 100% (AI costs are 0). Against the Captain, player chakra fell to 80–92% and stamina to 79–91%. Against Sealwright, chakra stayed at 100% and stamina at 97–99%. The Captain casts no Clears.

**Reading, for the director (no tuning applied; these corrected measurements replace r2's):** with equal multipliers, Sealwright is **not** a like-for-like copy of the Captain. Compared with the Captain, Sealwright:

- spikes lower (6–24% vs 8–30% of max HP per action);
- has no delayed damage, while 568–2,793 of the Captain's damage per fight arrives as delayed 505-HP ticks;
- runs fights 1.3–3.5× longer;
- leaves far more recovery windows;
- holds a B22 defence uptime of about 0.6 that the Captain lacks;
- cuts buffer IDG uptime from about 0.9 to about 0.3, which turns the durable-buffer matchup from 0/5 to 5/0;
- **loses the durable-striker matchup 0/5 (31 rounds) that the Captain wins 5/0 (22 rounds)**. This reverses r2, which had Sealwright winning it in 23 rounds;
- casts only empty Clears against a damage-only player (3 or 6 per fight, all S31; B32 is never cast there). The Clear component removes nothing against this damage-only fixture; S31 still deals damage. Routine S31 and conditional B32 are preserved as designed.

Stun never fully locked the player out, for either boss. The three closing-rule variants were identical in 4 of 6 fixtures. In the other two they differed by 2 rounds (half-cap moderate: 7 vs 9) and by about one stunned round and one recovery window (durable moderate). The proactive closing rule has little measurable effect here. Parity, tuning and rule acceptance remain the director's to judge on these corrected numbers.

## 5. B and C — items

**Crystal (B1–B3):**

- B1: the expected rejection is reproduced exactly. The controls pass: Damage or Pierce in the same array makes it valid, and Vamp-only and Wound-only arrays are also rejected.
- B2 (hypothetical record, imbuable Flaming Sword carrier): the composition order is `[damage, afterburn, consume]`. 472.1 damage gives a **94-HP shield** (floor 20%) for 3 rounds. A 500-HP target shield absorbed the whole hit (HP loss 0), yet the Consume shield was still 94, which proves the pre-shield basis. ALL-method carrier: 2 × 472.1 aggregates to one 188 shield.
- **B2 finding:** Consume 40 on the weapon + Crystal 20 gives **40%** (188 of 472.1), and two Crystal records give **20%** (94). `insertAction` keeps only the first SELF Consume per stack key, so stacking does not happen within one action.
- B2: a recipient without cast-round Damage/Pierce gets no shield, silently.
- B3: an eligible imbuable WEAPON passes every tested pre-write eligibility guard (the run stops at the first trapped write). Persistence and concurrency guards (the CAS snapshot claim, atomic crystal consume, in-progress imbue queue against live rows) were not run, so this is not evidence of a committed imbue. Rejections: the accepted Katana in its published state and the captured Flaming Sword (`canBeImbued:false`). While the Katana is still `hidden:true` it is invisible to `imbueItem`, because `fetchUserItems` excludes hidden items ("Target item not found"); an ARMOR recipient ("only WEAPON items"); a duplicate crystal ID; the slot limit; an equipped recipient; a non-CRYSTAL item; no, GATHERING or HUNTING occupation (imbue and craft).
- B3 rank × rarity (all 24 imbue and craft cells asserted, r3): imbuing needs Novice = 0 slots, RARE ≥ Apprentice, EPIC ≥ Master, LEGENDARY = Forgemaster. Crafting needs RARE ≥ Apprentice, EPIC ≥ Master, LEGENDARY = Forgemaster. With the 12-Filament requirement carrier, eligible ranks stop at the material check. The slot limit is asserted exactly: an Apprentice cannot add a second crystal to a `maxImbueNumber` 1 weapon ("…for this item (1)"). **Engine text observation:** the imbue rarity rejection names the wrong rank. An Apprentice imbuing EPIC is told "at least Apprentice rank", and a Master imbuing LEGENDARY is told "at least Master rank"; the actual gate is `CRAFTING_TIMES_MINS[rank][rarity] === 0`. This is recorded verbatim and not changed. Assembly drops legacy imbuements on `canBeImbued:false` items.
- Rarity, trading and accessibility remain policy decisions.

**Katana (C1–C3), accepted record (RUL-2026-10-11-004, Night's Testament baseline, Crystal Pierce):**

- The three-effect array parses (`shieldRounds` 3; consume `rounds` normalised to 0). `maxImbueNumber` 0 is rejected, so `canBeImbued:false` is the switch.
- **Pierce 1475.4** produces a **590-HP self shield for 3 rounds**. The result is identical against a 500-HP target shield, which was consumed while the HP loss stayed unchanged. With an ALL-method control override, two targets aggregate to 1180. The Crystal element and Night's Testament's stat/general classes give the same damage as the earlier carrier.
- The shield absorbed a later 70-power hit (590 → 222.7, wielder HP loss 0). Asserted exactly: present in the cast round and the next three (rounds 3, 3, 2, 1), gone from round +4.
- Approved powerPerLevel 0: identical damage at item level 1 and 50. A 0.5 control scales with the player's item level (1490 → 2213).
- **Immunity:** a pre-existing Buff Prevent is not removed. A new Buff Prevent (Seal of Nullification at power 100) is **blocked in the cast round and the next two rounds and lands again in round +3**. Asserted as the exact pattern [true, true, true, false]: blocked attempts leave no Buff Prevent, and the round +3 attempt applies an active power-100 Buff Prevent.
- With the accepted cooldown 6 and AP 40, a swing in round 1 makes the Katana unavailable through round 6; it returns in round 7. Ion Lance (pierce GCD tag) is locked rounds 1–3 and released from round 4 (`SHARED_COOLDOWN_ROUNDS` 3). Heavy Cut (no shared tag) stays available in every round. The full per-round availability of all three is asserted. 60 AP remains after a swing.

## 6. Ledger — separate from approved memberships

| Kind | Item | Status |
| --- | --- | --- |
| Rule proposal | Candidate remap of each captured profile through the accepted mapping (`results/a1.json` `ruleChangeLedger`; none for the Captain, 1 for Crowned, 4–5 for the others). Removes kit-only fall-through | Proposed; not approved |
| Rule proposal | Sealwright: contract order as written; the closing rule's effect is small (§4) | Order and closing need director acceptance |
| Rule proposal (option) | Sealwright filler for idle 40 AP: either `includeDefaultRules:true` (adds basic-attack fill like the Captain) or an explicit basic-attack rule. **Not tested as a variant**; it would raise damage | Director to decide whether to test |
| Behaviour proposal | Crowned support rotation (§3). Evidence only | Not approved |
| Tuning | None applied. Possible discussion items: minion innate-IDG duplicates (§3); Sealwright vs Captain profile (§4); B16 is only −20 AP | Director |
| Engine | Crystal validator correction and the Consume-on-Consume decision: `docs/design/GHOST_SHIP_CRYSTAL_ENGINE_CORRECTION_PROPOSAL.md` | Proposal only; not implemented |

## 7. Exact commands and results

r3 (2026-10-11), engine pin `cddd7d91`, `bun.lock` sha256 `da6602f2…1906c08`, bun 1.4.2, node v22.22.0, `unshare -rn`:

```text
TNR_OUT=<scratch>/r3a harness/ghost_ship_stage2/run.sh          (first run)
  → M0 PASS: 482 checks, 0 failed
  → bun test v1.4.2: 73 pass, 0 fail, 174 expect() calls, Ran 73 tests across 4 files (exit 0)
  → evidence m0/a1/a2/b1/b2/b3/c1/c2/c3: clean (tools/check_evidence.py)
  → evidence assertions: a1 207/0 failed, a2 39/0, b1 4/0, b2 7/0, b3 14/0, c1 4/0, c2 18/0, c3 12/0
  → negative self-test: synthetic failed:1 evidence exit 1; missing gate file exit 1;
    bun test with a failed Evidence.check exit 1; evidence written by that run exit 1
  → run.sh: bun=0 evidence=0 negativeSelftest=0 -> exit 0
harness/ghost_ship_stage2/run.sh                                 (second run → results/)
  → exit 0, same counts; cmp: m0/a1/a2/b1/b2/b3/c1/c2/c3.json byte-identical to the first run
python3 harness/ghost_ship_stage2/tools/build_katana_record.py --check
  → current
```

M0, B1, B2, C1 and C3 evidence is byte-identical to r2. B3 and C2 recorded data is identical to r2; only their checks changed, with recorded-only or partial checks replaced by exact assertions and new ones added. A1 and A2 data reflect r3. r1/r2 commands (68 pass, 141 expect() calls) are superseded.

No skill, doctrine, law or generated-contract file changed in r3, so the doctrine, law and pack gates do not apply. **Correction to earlier text:** r1 changed no `state/` file and not `docs/RULINGS.md`, but r2 did. It appended RUL-2026-10-11-004 to `docs/RULINGS.md`, updated the Katana section of `state/ghost_ship_skyglass_reward_decisions.md`, and added `state/ghost_ship_skyglass_katana_record.json`. r3 corrects only that file's stale "Build acceptance gates still open" list (§9).

## 8. Not done, and not authorised

- **Live-game requests 0, writes 0, asset-CDN requests 0.** No credentials, cookies or live session material. No game server, live DB or API.
- No upstream engine change, including in the scratch export. No art, manifest, publication, quest edit or Forge work.
- No browser or installed-client check. No deployed-version confirmation.
- Not tested: multi-player parties against these bosses; Sealwright with a basic-attack filler; tuning variants; live damage settings.

## 9. Open decisions (dauntless) and narrow operator requests

1. **Sealwright:** accept or adjust the rule order and closing rule; decide whether to test or adopt a 40-AP filler; accept the measured profile against the Captain or request tuning. Judge this on the r3 measurements (§4), not r2's: Sealwright now loses the durable-striker matchup the Captain wins, and its Clears are empty against damage-only players. Seven jutsu and overlapping Clears stay locked; note the shared Clear GCD.
2. **Crowned Captain:** keep the support dormant (current behaviour) or approve a rotation.
3. **Candidate rule remap** for the other nine AIs, or a different rebuild.
4. **Minion innate IDG duplicates:** preserve as captured (current instruction) or review separately.
5. **Crystal:** authorise or decline the Lane A correction, and decide the Consume-on-Consume behaviour. Set rarity, trading and crafting accessibility (see the §5 table).
6. **Katana:** baseline settled (RUL-2026-10-11-004). Still pending: description, battle description, image, effect animation/SFX.
7. **Operator captures:** (a) and (b) are done (push/85 and push/86; see `docs/reviews/GHOST_SHIP_SKYGLASS_CAPTURES_85_86_2026-10-11.md`). Live AI stats equal the harness conversion exactly. Still open: (c) The deployed engine version or settings snapshot (`gameSetting` damage values), if obtainable, so the harness can be re-run at that pin.

Minor documentation inconsistency, not altered: the feasibility brief's 2026-10-11 header says the Crowned Captain "keeps ten moves". RUL-2026-10-11-003, the start packet and the kit packet say eleven, and M0 verifies eleven.
