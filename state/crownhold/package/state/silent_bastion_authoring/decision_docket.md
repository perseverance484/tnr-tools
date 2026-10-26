# Silent Bastion — director decision docket (one list)

As of 2026-10-16 the director has ruled on every design and balance decision this package raised (RUL-2026-10-16-004 to -013, table F; review F1 found that Extermination Order's AP, range and powers and the two weapons were not yet ruled, and RUL-2026-10-16-013 closed that). What remains is listed below. Section A is still the director's to decide. B–D are not design decisions: they are fresh reads, live checks and tooling that must happen before a manifest. Evidence paths are relative to the repository root. "Gate A/C/I…" means the authoring harness `harness/silent_bastion_authoring/` (results in its `results/`).

## A. Still open for the director

1. **Cache names.** "Bastion Arsenal Cache" and "Bastion Research Cache" are still `[provisional]`. RUL-2026-10-16-001 made them category names, not final names.
2. **Rarity.** Cache rarity is CANDIDATE LEGENDARY for both caches; Beacon rarity is CANDIDATE LEGENDARY. Item type CONSUMABLE is a candidate for all three.
3. **Cache description wording.** The factual candidate copy is in `design/entry_and_rewards.json`.
4. **Art.** 20 avatars, 6 scenes and 5 icons (`art_shotlist.md`). No binaries exist. A visible quest scene needs a scene background and scene characters.

## B. Required before a manifest (operator / fresh capture; not design decisions)

5. **Fresh reads of the referenced records.** All current values come from committed captures (2026-08 to 2026-10) or the upstream seed. None is a live readback.
   - Tempest Cleave `Ul83iTziN__Z0i_UOzZTK` (Master of Arms): confirm it is live and equippable on an AI.
   - Solar Bow `ALqXVSL58QMfJ4DgoJ5Il` (HAND_1) and Crossbow `LbccOnzfsADLgTBPSHjKK` (HAND_2) (Arakane): the **selection is approved** (RUL-2026-10-16-013), but the IDs and values are historic seed rows. Capture current IDs, item actions, AP, range, cooldown, slots, durability and AI loadout before manifest construction. A material mismatch goes to the director; never substitute weapons.
   - B09 Veilstep: RUL-2026-10-16-007 uses whatever the live record is; re-run gate A6 if it differs from 1r / CD 5.
   - The 19 cache ingredient IDs and the 8 recipes (2026-10-13 census capture).
6. **Username collisions** for the 16 regulars and 4 commanders (law 66).
7. **Calibration anchor fight** (balance doctrine law 13) before the stat ladder (RUL-2026-10-16-011) is final in game.
8. **Two-phase build (law 17).** The Last Directive and Extermination Order must be created first. Arakane then equips them by literal ID; the validator errors for this are expected until then.
9a. **F5: full AI loadout and combat integration** (independent review). Build a small offline fixture: create/edit through the editor with the Arakane loadout and at least one regular; attach `aiProfileId`; start one real quest battle. Verify the real gear rows (new AI items are inserted `equipped: "CHEST"`, while gate A's synthetic fixture uses ITEM_1 / HAND_1 / HAND_2), their usable battle actions and the attached rules. The release stays **BLOCKED** until this and calibration pass.
9. **Ghost Ship Beacon drop** (10% per clear, RUL-2026-10-16-010) goes into the Ghost Ship content when the Beacon ships. This package does not edit Ghost Ship.

## C. Tooling (Lane A, not changed here)

10. **VAL1.** `validate.py` lint L18 forbids `clear` on items. At `0651b039` the engine accepts it, and gate A6 shows Countermand's Clear working.
11. **VAL2.** `validate.py`'s tag schemas (`skills/building-tnr-content/data/46_DATA_tag_schemas.json`, extracted 2026-07-10) predate `rewardMode` / `weightedCache` on `noncombatconsumereward`. Gate C shows both caches pass the engine's own schemas and open natively.
12. `harness/silent_bastion_authoring/tools/check_validate.py` passes only on the exact documented error set:
    - 2 errors for the two-phase build;
    - 4 for the puzzle exception (RUL-2026-10-16-012);
    - 1 for VAL1;
    - 4 for VAL2.
    - The 9 warnings are the regulars' engagement-gated self-buffs, which are intentional.

## D. Integration

13. **Rulings ID collision.** `RUL-2026-10-14-001` is the Bastion Medical100 ruling on this branch and an unrelated art ruling on main. Reconcile the IDs deliberately at integration.
14. **Source drift.** All gates ran at upstream `0651b039`. Re-run `harness/silent_bastion_authoring/run.sh` at the build pin.

## E. LOCKED — do not reopen

- `alt99_f4gate`: 99 objectives. Four interior divisions, deserted exterior, no Gatewarden.
- 50% recovery; Medical sets 100%; player-side Combat buffs; Security Alert on a wrong puzzle answer.
- Arakane defeat hard-fails the attempt.
- Beacon charged at `startQuest`, once per attempt, never refunded.
- Exactly one of two caches at quest level after completion.
- Commander kit memberships and signature effects.
- Everything in F.

## F. Resolved 2026-10-16 (rulings in `docs/RULINGS.md`)

| Item | Decision | Ruling | Where it lands |
| --- | --- | --- | --- |
| AR1: Extermination Order on an expired Final Stand | Cooldown **4** (residual risk accepted; no engine change) | RUL-2026-10-16-004 | `design/commanders.json`; gate A6 probe |
| F3: recovery-loop battle income | **O2**: `scaleGains: 0` on the 8 recovery battles | RUL-2026-10-16-005 | `design/entry_and_rewards.json`; gates C and I |
| Grand Marshal kit and priorities | **Ratified** as translated | RUL-2026-10-16-006 | `design/commanders.json`; roster §4 |
| SRC1: Veilstep record vs design | Use the captured record (**Stealth 1r, cooldown 5**); shared jutsu not edited | RUL-2026-10-16-007 | Arakane profile; gate A6 |
| D5: Division IV Combat Protocol | Pick delegated; **Debuff Prevent 100 / 3r** (option A) | RUL-2026-10-16-008 | `design/protocols.json`, D5 text in `design/script.json` |
| RC1: unclaimed cache blocks the next completion | **Accepted** with the "claim before you set out" entry copy | RUL-2026-10-16-009 | quest description in `design/script.json` |
| Cache contents | 4 + 4 shortlist, **Strong Pyramid** (whole EPIC recipe / 40% LEGENDARY), one roll, **EPIC 50 / LEGENDARY 50** | RUL-2026-10-16-010 | `design/entry_and_rewards.json` → `compiled/cache_items.candidate.json`; gates C1b, C2 |
| Tradability | Caches **untradeable**; Beacon **tradeable** | RUL-2026-10-16-010 | `design/entry_and_rewards.json` |
| Beacon source | **10% per Ghost Ship clear** | RUL-2026-10-16-010 | Ghost Ship content (later) |
| `maxAttempts` / `maxCompletes` | **100 / 100** | RUL-2026-10-16-010 | `design/entry_and_rewards.json` |
| Stat ladder | Accepted as launch values (calibration may tune) | RUL-2026-10-16-011 | `economy_and_f3.md` §1, `design/` |
| Security Alert; Protocols I–III | IDT 10 / 2r; Stun Prevent 100 / 2r, IDG 25 / 3r, Seal Prevent 100 / 2r | RUL-2026-10-16-011 | `design/protocols.json` |
| Arakane values | The Last Directive 40 AP / CD 99 / IDG 30; Countermand as compiled; name **Extermination Order** | RUL-2026-10-16-011 | `design/commanders.json` |
| Replicant Zero heals | **Bulwark first** (as authored) | RUL-2026-10-16-011 | `design/commanders.json` |
| Written content | 16 regulars, 4 puzzles, 99 texts and the Division IV foreshadowing accepted | RUL-2026-10-16-011 | `design/regulars.json`, `design/script.json` |
| Puzzle validator exception | Granted for `d2`–`d5.n.puzzle` | RUL-2026-10-16-012 | `check_validate.py` |
| F4/F5 API text exposure | Accepted | RUL-2026-10-16-012 | this docket |
| Extermination Order stats | 60 AP, range 5, single target, 80 damage, Elemental Seal 100/2r, Cleanse Prevent 100/2r; cooldown 4; active Final Stand only | RUL-2026-10-16-013 | `design/commanders.json` |
| Arakane equipment | Countermand, Solar Bow (HAND_1), Crossbow (HAND_2) **approved**; fresh captures required | RUL-2026-10-16-013 | `design/commanders.json` (`itemsStatus`) |
