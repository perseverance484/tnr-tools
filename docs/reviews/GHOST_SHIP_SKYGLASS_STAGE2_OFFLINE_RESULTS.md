# Ghost Ship / Skyglass Stage 2 — offline test results (Fable Lane A)

**Status: OFFLINE TEST PACKAGE COMPLETE. RELEASE STILL BLOCKED.** M0, A1, A2, B1, B2, B3, C1 and C2 were executed against actual pinned engine code and PASS on their stated scope. C3 is BLOCKED (no Legendary Sword baseline). Crystal production validity is BLOCKED by the validator (B1 is an expected-rejection PASS). Sealwright parity is measured, not accepted.

**Date:** 2026-10-11. **Implementer:** Fable (Claude Code). **Independent reviewer:** ChatGPT, at the frozen SHA. **Decisions:** dauntless.
**Governing briefs:** `state/prompt_ghost_ship_skyglass_stage2_feasibility.md` (test contract) and `state/prompt_ghost_ship_skyglass_stage2_start.md` (execution packet), at input commit `61373538035d41f7e773ec082b739740cdf0860e` (RUL-2026-10-11-003).
**Harness and evidence:** `harness/ghost_ship_stage2/` (README, runner, tests, `results/*.json`). **Engine proposal:** `docs/design/GHOST_SHIP_CRYSTAL_ENGINE_CORRECTION_PROPOSAL.md`.

## 1. Gate summary

| Gate | Status | What actually executed | Evidence |
| --- | --- | --- | --- |
| **M0** | **PASS** | 482 deterministic checks: 4 capture/registry SHA-256 pins; 65 memberships resolve to exact full records; 11 retained protected-field hashes (all repeated copies identical); 11 AI and 11 profile hashes and linkage; innate arrays (duplicates kept); baseline numeric profiles; Captain/Crowned/Sentinel/First Blade boundary checks; Sealwright's 7 records; embedded-vs-pool field drift equals the packet's declared lists (absent ≠ null) | `results/m0.json` |
| **A1** | **PASS** | All 11 AIs assembled by the engine's `processUsersForBattle`. Captured / kit-only / candidate-rule variants. 20-round cadence against a passive dummy at hex 3 and 7. 9 fights per variant. Hazard trigger tests. Crowned dormant-support check. 160 evidence assertions, 0 failed | `results/a1.json` |
| **A2** | **PASS** (measurements, parity not accepted) | Sealwright selector matrix: IDG 69/70/70.5/71/90, gate distance, B32 unavailable ×4, summons and second opponents, blocked path, new/expired/protected IDG, Clear Prevent, S31 routine. B16 control timeline. 120 full fights: Captain vs 3 Sealwright rule variants × 6 player fixtures × 5 seeds. 25 assertions, 0 failed | `results/a2.json` |
| **B1** | **PASS** (expected rejection). Production Crystal **BLOCKED** | The real item `effects` schema and the full `ItemValidator` reject `[consume 20%]` with exactly `ConsumeTag must be used together with a damage or pierce effect on the same action` | `results/b1.json` |
| **B2** | **PASS** (post-composition runtime only) | Real assembly composes weapon + imbuement. Weapon action produces a 20% pre-shield-basis shield, 3 rounds. Shielded target, multi-target aggregation, no-damage recipient, Consume-on-Consume all tested | `results/b2.json` |
| **B3** | **PASS** | Real `occupation.imbueItem` and `craftItem` procedures, read-only stub client (writes trapped): WEAPON-only, non-imbuable recipients, duplicates, slot limit, equipped item, occupation, full rank × rarity matrix. Battle-side suppression of old imbuements | `results/b3.json` |
| **C1** | **PASS** (effect array only) | Exact Pierce 50 + SELF immunity(buffprevent, 2r) + Consume 40% parses. `maxImbueNumber` 0 is rejected and 1 accepted. The carrier full record validates, but this is not a final-record PASS | `results/c1.json` |
| **C2** | **PASS** | Real weapon action on sourced carriers: 40% shield, pre-shield basis, aggregation, absorption and expiry, item-level scaling, immunity window against a captured Buff Prevent jutsu, cooldown/GCD/AP | `results/c2.json` |
| **C3** | **BLOCKED** | Scanned committed harvests: 3 distinct full WEAPON records, 0 LEGENDARY/SWORD. Final AP/costs/range/CD/GCD/requirements/economy cannot be validated | `results/c3.json` |

Commands and outcomes (§7) are exact. The engine suite reported `68 pass, 0 fail, 136 expect() calls, Ran 68 tests across 4 files`, exit 0. Two independent full runs produced byte-identical evidence for every gate.

## 2. Source, dependency and fixture provenance

- **Engine execution pin:** `studie-tech/TheNinjaRPG@cddd7d91c9e6bdebc978ddcb61e5b8a305bd0f93` (pin B). It is exported with `git archive` into a disposable directory, and the upstream working tree is unchanged. `bun.lock` sha256 `da6602f2…1906c08`; runtime bun 1.4.2, node v22.22.0, python 3.13. Dependencies were installed with `bun install --frozen-lockfile --ignore-scripts` (approved by the user for this session). Tests ran in `unshare -rn` with upstream CI placeholder environment values and no database.
- **Drift assessment.** A=`4774560e` (historical AI pin) → B: only `validators/ai.ts`/`ai_v2.ts` change, adding COORDINATE action targets. No Ghost Ship or Sealwright rule uses them. B → C=`1853b6ab` (the readiness review's observed HEAD): `supportsNpcAllies()` makes **QUEST**/OVERWORLD battles choose enemies and allies by battlefield side instead of village/controller (`ai_v2.ts`, `actions.ts getTargetUser`, `participants.ts`). That change also affects `combat.ts` setup/spawn. Every fixture here has opponents that differ in both village and side, so the measured outcomes do not depend on that change. **Re-run the harness at the deployed pin once it is known.** Upstream HEAD moved again during this session (`0b730e9f`). That is not evidence of deployment.
- **Captures (committed, hashed by M0):** AI `harvests/inbox/tnr_results_1790826836406.json`, profiles `…1790828718767.json`, pool `…1791583362574.json`, registry `skills/building-tnr-content/data/32b_DATA_pool.json`. Carriers: Flaming Sword `…1788235198666.json#/captures/8/data/items/0/item` (weapon non-effect fields, EPIC SWORD), Seal of Nullification `…1789188714166.json#/captures/13/data` (Buff Prevent), Rose Sanctuary `…1791247737840.json#/captures/52/data` (Clear Prevent), plus Light Barrier, Cataclysm Fist, Ion Lance and Heavy Cut from the pool capture.
- **Schema conversion (important).** The October 1 AI rows predate upstream migration `0056_unified_combat_stats_masteries.sql` (commit `46f62cd9`, 2026-10-08). Pins A, B and C all fight with `offence`/`defence`/`*Mastery`, which those rows lack. Unconverted, the bosses deal near-zero damage. The harness applies the migration's **AI branch verbatim** (`offence`=max of 4 offences, `defence`=max of 4 defences, mastery=max(off,def), bloodline/sage mastery 10). This is a source-defined conversion, not tuning. A fresh post-migration operator capture must confirm the live rows.
- **Not read:** live `gameSetting` damage overrides (`dmgConfig` uses source defaults), live player populations, deployed version.

## 3. A1 — eleven accepted kits

**Preserved (asserted after real assembly, all 11):** the assembled membership equals the accepted kit. Numeric profile is identical between captured and accepted assembly: level, rank, multipliers, regeneration, pools, offence/defence, generals, preferred generals, elements. Innate effects are realised identically, including duplicates, and remain protected from Clear (`fromType` bloodline). Item rows keep their `equipped`/`dropChancePerc`. Every kit jutsu is an available action in round 1. No stat compensation exists anywhere.

**Behaviour (candidate = captured rules with jutsu IDs remapped through the accepted mapping):** there were no AI-exhaustion give-ups and no cooldown violations in any variant, at either distance, in any fight. Damage per round against the cadence dummy (hex 3; captured → kit-only → candidate):

| AI | captured | kit-only | candidate | Note |
| --- | ---: | ---: | ---: | --- |
| Deck Warden | 6789 | 5090 | 4574 | Smaller shared attacks replace the ghost combos |
| Core Horror | 16937 | 17807 | 12470 | |
| Oathkeeper | 12073 | 7703 | 6769 | |
| Wayfinder | 16460 | 8414 | 8693 | |
| Arsenal Keeper | 8316 | 5435 | 5300 | |
| Sentinel | 10406 | 9715 | 8747 | |
| First Blade | 14559 | 9205 | 8296 | |
| The Captain | 1550 | 1550 | 1550 | Kit and rules unchanged |
| Crowned Captain | 3042 | 2599 | 2869 | Kit-only loses the Sharpened Focus rule; the remap uses EA03 |

The kit-only column shows rules falling through to default/backup rules when they reference removed IDs. It is not a proposed configuration. With the candidate remap, every AI uses its accepted kit. The accepted substitutions are weaker attacks, as the packet disclosed ("role substitutes, not equal-strength copies"). Per RUL-2026-10-11-003 nothing was compensated.

**Observation for the director (no change made):** the seven non-hazard minions carry preserved **duplicate innate IDG** entries. They hold +200% to +350% for 99 rounds, plus shorter entries, for totals of +350% to +420%; for example Wayfinder is 100+100+100+50, all 99 rounds. Under source-default damage settings, they out-damage the regular Captain about 3–11× per round against the cadence dummy. Against the three player fixtures they won all 9 fights per variant, in a mean of 1.0–2.3 rounds. This comes from the captured data and the 0056 conversion, not from the kit change.

**Hazards (Seal Charge, Core Canister):** the original ID `nCQETf-HNnbRec1OSY2-R` is kept. They wait in rounds 1–2 / 1–6 with no exhaustion (end_turn fallback → `wait`). In round 3 / 7 they cast Core Rupture, spending 100 AP, self-destructing (one-hit-kill SELF), and dealing Pierce 120 (×2 dmgModifier) plus Stun −60 AP to the opponent. **Core Rupture is ALL-method:** at hex distance 8 it fired on the same round and reached the opponent, because the nominal range 5 does not limit ALL. This is identical in all three variants.

**Crowned Captain dormant support:** across 10 fights each, the captured and candidate rules selected Second Wind, Stolen Form and Rebounding Form **zero times**, so the equipped support stays dormant. A labelled **unapproved** proposal rotation was also run (Second Wind <50% HP; Stolen Form when the closest opponent has IDG ≥30 within 5; Rebounding Form within 3). It used Rebounding Form 10× and Stolen Form 5×. The boss still won 10/10, with mean length 3 → 4 rounds and mean boss HP left 96.1% → 90.8%. This is evidence for the activation decision only.

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

**B16 Sovereign Fetters control:** Stun 100/2r reduces AP by **20 per round** for rounds +1 and +2 (0 in the cast round). It does not lock the player out. Seal 100/2r seals the **bloodline**. This is weaker control than "2r stun+seal" suggests; it is the captured shared record unchanged.

**40+60 AP capacity:** no exhaustion in any of 120 fights. The contract profile has `includeDefaultRules:false` and no 40-AP filler after B22's cooldown, so Sealwright often uses only 60 AP and then `wait`s (17–21 waits per long fight; active AP 52–70 per round). The Captain fills spare AP with basic attacks from the default rules.

**Full comparison (mean per fight; each cell is 5 identical seeds; start hex distance 6; B=boss wins, P=player wins):**

| Player fixture | Boss | B/P | Rounds | Boss dmg | Spike/action (%maxHP) | Lockout rounds | Recovery windows | Player IDG uptime | Boss defence uptime | Clears (B32) |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| JONIN cap, buffer | Captain | 5/0 | 10 | 4040 | 22% | 2 | 1 | 0.91 | 0.00 | 0 |
| | Sealwright (all 3 variants) | 5/0 | 11 | 5050 | 22% | 2 | 3 | 0.25 | 0.58 | 3 (1) |
| JONIN cap, striker | Captain | 5/0 | 5 | 4040 | 27% | 2 | 0 | 0 | 0.00 | 0 |
| | Sealwright (all 3) | 5/0 | 9 | 5050 | 22% | 2 | 2 | 0 | 0.70 | 2 (0) |
| JONIN half, moderate | Captain | 5/0 | 3 | 5050 | 46% | 3 | 0 | 0.75 | 0.00 | 0 |
| | Sealwright contract | 5/0 | 5 | 5050 | 36% | 3 | 1 | 0.33 | 0.50 | 1 (0) |
| | Sealwright no/late closing | 5/0 | 4 | 5050 | 36% | 2 | 0 | 0.20 | 0.80 | 1 (0) |
| Durable (pools ×2.5), buffer | Captain | **0/5** | 14 | 9106 | 18% | 4 | 1 | 0.93 | 0.00 | 0 |
| | Sealwright (all 3) | **5/0** | 27 | 12625 | 9% | 6 | 9 | 0.32 | 0.61 | 8 (3) |
| Durable, striker | Captain | 5/0 | 18 | 10605 | 11% | 4 | 0 | 0 | 0.00 | 0 |
| | Sealwright (all 3) | 5/0 | 23 | 12625 | 9% | 6 | 6 | 0 | 0.62 | 5 (0) |
| Durable, moderate | Captain | 5/0 | 13 | 11272 | 20% | 5 | 1 | 0.86 | 0.00 | 0 |
| | Sealwright contract | 5/0 | 24 | 12625 | 9% | 6 | 7 | 0.40 | 0.64 | 5 (0) |
| | Sealwright no/late closing | 5/0 | 23 | 12625 | 9% | 7 | 6 | 0.42 | 0.62 | 5 (0) |

Boss pools never dropped below 100% (AI costs are 0). Player stamina and chakra fell to 78–100% against the Captain (100% only in the 3-round half-cap fight) and stayed at 98–100% against Sealwright. Every Clear cast removed something (`clearsThatRemoved` = `clearCasts`).

**Reading, for the director (no tuning applied):** with equal multipliers, Sealwright is **not** a like-for-like copy of the Captain. Compared with the Captain, Sealwright:

- spikes lower (9–36% vs 11–46% of max HP per action);
- runs fights 1.1–1.9× longer;
- leaves far more recovery windows;
- holds a B22 defence uptime of about 0.6 that the Captain lacks;
- cuts buffer IDG uptime from about 0.9 to about 0.3, which turns the durable-buffer matchup from 0/5 to 5/0.

The three closing-rule variants were identical in 4 of 6 fixtures and differed by about one round in the other two. The proactive closing rule has little measurable effect here.

## 5. B and C — items

**Crystal (B1–B3):**

- B1: the expected rejection is reproduced exactly. The controls pass: Damage or Pierce in the same array makes it valid, and Vamp-only and Wound-only arrays are also rejected.
- B2 (hypothetical record, imbuable Flaming Sword carrier): the composition order is `[damage, afterburn, consume]`. 472.1 damage gives a **94-HP shield** (floor 20%) for 3 rounds. A 500-HP target shield absorbed the whole hit (HP loss 0), yet the Consume shield was still 94, which proves the pre-shield basis. ALL-method carrier: 2 × 472.1 aggregates to one 188 shield.
- **B2 finding:** Consume 40 on the weapon + Crystal 20 gives **40%** (188 of 472.1), and two Crystal records give **20%** (94). `insertAction` keeps only the first SELF Consume per stack key, so stacking does not happen within one action.
- B2: a recipient without cast-round Damage/Pierce gets no shield, silently.
- B3: an eligible imbuable WEAPON passes every guard (the run stops at the first trapped write). Rejections: the Katana carrier and the captured Flaming Sword (`canBeImbued:false`); an ARMOR recipient ("only WEAPON items"); a duplicate crystal ID; the slot limit; an equipped recipient; a non-CRYSTAL item; no, GATHERING or HUNTING occupation (imbue and craft).
- B3 rank × rarity: imbuing needs Novice = 0 slots, RARE ≥ Apprentice, EPIC ≥ Master, LEGENDARY = Forgemaster. Crafting needs RARE ≥ Apprentice, EPIC ≥ Master, LEGENDARY = Forgemaster. With the 12-Filament requirement carrier, eligible ranks stop at the material check. Assembly drops legacy imbuements on `canBeImbued:false` items.
- Rarity, trading and accessibility remain policy decisions.

**Katana (C1–C2), Flaming Sword carrier fields:**

- The three-effect array parses (`shieldRounds` 3; consume `rounds` normalised to 0). `maxImbueNumber` 0 is rejected, so `canBeImbued:false` is the switch.
- **Pierce 1475.4** produces a **590-HP self shield for 3 rounds**. The result is identical against a 500-HP target shield, which was consumed while the HP loss stayed unchanged. With an ALL-method carrier, two targets aggregate to 1180.
- The shield absorbed a later 70-power hit (590 → 222.7, wielder HP loss 0). It counted down through rounds 2–4 and was gone in round 5.
- Approved powerPerLevel 0: identical damage at item level 1 and 50. A 0.5 control scales with the player's item level (1490 → 2213).
- **Immunity:** a pre-existing Buff Prevent is not removed. A new Buff Prevent (Seal of Nullification at power 100) is **blocked in the cast round and the next two rounds and lands again in round +3**.
- With the carrier's cooldown 4 and AP 40, the Katana is unavailable rounds 1–4 and returns in round 5. Ion Lance (pierce GCD tag) is locked rounds 1–3. Heavy Cut (no shared tag) stays available. 60 AP remains after a swing.
- These are carrier values; the final cadence is a C3 question.

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

```text
python3 harness/ghost_ship_stage2/m0_verify.py --out …/m0.json
  → "M0 PASS: 482 checks, 0 failed" (exit 0)
TNR_ENGINE_WORK=<scratch> harness/ghost_ship_stage2/run.sh
  → M0 PASS: 482 checks, 0 failed
  → bun test v1.4.2: 68 pass, 0 fail, 136 expect() calls, Ran 68 tests across 4 files (exit 0)
  → evidence assertions: a1 160/0 failed, a2 25/0, b1 4/0, b2 7/0, b3 9/0, c1 4/0, c2 15/0, c3 1/0
TNR_ENGINE_WORK=<scratch> TNR_OUT=<scratch>/rerun harness/ghost_ship_stage2/run.sh   (second run)
  → exit 0; cmp: m0/a1/a2/b1/b2/b3/c1/c2/c3.json byte-identical to results/
Preflight (pin B, same isolation): bun test tests/libs/combat/consume.test.ts ai_v2_rules.test.ts shared_cooldown.test.ts
  → 63 pass, 0 fail
```

No skill, doctrine, law or generated-contract file changed, so the doctrine, law and pack gates do not apply and were not run. `state/` projections and `docs/RULINGS.md` are unchanged.

## 8. Not done, and not authorised

- **Live-game requests 0, writes 0, asset-CDN requests 0.** No credentials, cookies or live session material. No game server, live DB or API.
- No upstream engine change, including in the scratch export. No art, manifest, publication, quest edit or Forge work.
- No browser or installed-client check. No deployed-version confirmation.
- Not tested: multi-player parties against these bosses; Sealwright with a basic-attack filler; tuning variants; live damage settings.

## 9. Open decisions (dauntless) and narrow operator requests

1. **Sealwright:** accept or adjust the rule order and closing rule; decide whether to test or adopt a 40-AP filler; accept the measured profile against the Captain or request tuning. Seven jutsu and overlapping Clears stay locked; note the shared Clear GCD.
2. **Crowned Captain:** keep the support dormant (current behaviour) or approve a rotation.
3. **Candidate rule remap** for the other nine AIs, or a different rebuild.
4. **Minion innate IDG duplicates:** preserve as captured (current instruction) or review separately.
5. **Crystal:** authorise or decline the Lane A correction, and decide the Consume-on-Consume behaviour. Set rarity, trading and crafting accessibility (see the §5 table).
6. **Katana:** accept the baseline after the capture below.
7. **Operator captures (read-only, operator-run, not agent requests):** (a) `item.get` full record of a LEGENDARY WEAPON/SWORD; Night's Testament `osJq3k77YPGoFWgof12FQ` is the first suggestion, and its SWORD typing is unverified. (b) Fresh post-0056 `profile.getAi` for the eleven Ghost Ship AIs and the regular Captain, to replace the migration conversion. (c) The deployed engine version or settings snapshot (`gameSetting` damage values), if obtainable, so the harness can be re-run at that pin.

Minor documentation inconsistency, not altered: the feasibility brief's 2026-10-11 header says the Crowned Captain "keeps ten moves". RUL-2026-10-11-003, the start packet and the kit packet say eleven, and M0 verifies eleven.
