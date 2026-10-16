# Silent Bastion — director decision docket (one list)

Everything below needs the director. Items marked **LOCKED** are already ruled and are listed only so nothing gets re-opened by accident. Evidence paths are relative to the repository root. "Gate A/C/R…" means the authoring harness `harness/silent_bastion_authoring/` (results in its `results/`) or the reward proof on its own branch.

## A. Blockers found by native tests (need a choice)

1. **AR1 — Extermination Order can fire after Final Stand has expired.**
   - **Cause.** At the pinned engine, `routers/combat.ts` runs `alignBattle`, which lowers effect rounds to 0 without pruning them, and then runs `performAIaction`. `has_effect` sums raw effect power and never checks `isEffectActive`. The authored rule 2 (`has_effect finalstand ≥1`) therefore passes at the first decision after Final Stand reaches 0 rounds.
   - **Evidence.** Reproduced at the first-drafted cooldown 2 (gate A6, `AR.finalPhaseDecisions`).
   - **Probe.** Cooldowns 2, 3, 5 and 6 can each hit the expired decision. **Cooldown 4** kept every probed cast inside an active Final Stand at start distances 4, 7 and 9, with 2 casts per window. Cooldown 7 gives 1 cast.
   - **Options:**
     - (a) **Accept candidate cooldown 4.** This is the current compiled value. The residual risk is sequences the probe did not cover.
     - (b) Cooldown 7 or more: one ultimate per Final Stand.
     - (c) Request an engine change so `has_effect` ignores expired effects. That is Lane A and not proposed here.
     - (d) Accept the occasional post-expiry cast.
2. **D5 Combat Protocol.** The advertised Clear Prevent is still not in `questBuffTypes` at `0651b039`. The compiled candidate carries a **labelled stand-in**, Debuff Prevent 100 / 3r. Options in `design/protocols.json`:
   - A — Debuff Prevent 100 / 3r
   - B — Immunity, blocking Cleanse Prevent, 3r
   - C — Decreased Damage Taken 20 / 3r
3. **RC1 — re-run with an unclaimed cache choice.** The new expedition cannot be completed and must be abandoned, losing its Beacon. This comes from the reward proof (F6). The candidate copy already warns "claim before you set out". Options: accept the warning copy, or take it to an engine ruling.
4. **F3 — repeat battle income through recovery loops** (`economy_and_f3.md` §3). Options O1–O4. **O2** (`scaleGains: 0` on the 8 recovery battles) closes the cheapest loop without touching first-pass income. The compiled candidate leaves `scaleGains` unset.
5. **SRC1 — Veilstep record vs the design.** The captured B09 record has Stealth **1 round** with cooldown 5. The roster and Arakane profile assume Stealth 2 rounds with cooldown 6. Arakane's stealth branch (rules 4, 5, 17, 18) works natively with the 1-round record (gate A6), but the "two stealth rounds" premise is wrong. Confirm whether the live record is 1 round, or whether the pool registry (stealth 2r) is current. Do not edit the shared jutsu.

6a. **validate.py results** (`harness/silent_bastion_authoring/tools/check_validate.py`). These run on the validation-only manifest that `tools/compose.py` produces; it is **not** a push manifest. Seven errors remain, each documented:
   - **(i) Two-phase build requirement (law 17).** Arakane cannot equip the two exclusive jutsu by symbolic ref. They must be created first and then referenced by literal ID.
   - **(ii) Locked-topology conflict.** The four puzzles send both wrong answers to the same Security Alert approach. That is the approved `alt99_f4gate` shape, and the validator's "options share a target" hygiene rule rejects it. A future push will need an explicit validator exception ruling, as with RUL-2026-10-12-014.
   - **(iii) VAL1, stale lint.** L18 says `clear` is excluded from item effects. Gate A6 shows Countermand's item Clear strips player buffs at `0651b039`, so the lint should be source-reverified. That is Lane A tooling and is not changed here.
   - Of the 11 warnings, 2 are the unresolved cache refs (BLOCKED by design) and 9 are engagement-trigger gates on regulars' self-buffs (intentional: buff only when the enemy is near).

## B. Commander implementation decisions (design already authored; values open)

6. **Master of Arms (kit accepted).** The rules are translated 1:1 from roster §2.
   - **Tempest Cleave** resolves to `Ul83iTziN__Z0i_UOzZTK`: an existing EVENT jutsu, 60 AP, range 4, cooldown 7, `AOE_CIRCLE_SPAWN`, 45 EP + IDT 35/2r + Afterburn 30/2r, all `friendlyFire: ALL`. The ID comes from the committed operator capture of 2026-10-06, not from a fresh live read.
   - Native self-hit test (TC1): **no self-hit at path distance 2–5**, so no extra distance floor was added.
   - Confirm the ID is still live and still equippable on an AI.
7. **Replicant Zero (kit accepted).**
   - Split Image fires once, on round 2 (`specific_round 2`). One clone appears and takes its own turns.
   - The roster's priority order (Bulwark below 65% ahead of Second Wind below 40%) is kept. When both are ready below 40%, Bulwark wins.
   - Confirm that order, or allow moving Second Wind first.
8. **The Grand Marshal (12-move kit is a CANDIDATE).**
   - Roster ratification is still pending.
   - Stacked suppression: Ruin applies two DDG 60 / 3r effects, which stack multiplicatively under law 9, and Malediction adds IDT 60 + Seal. The DDG stack the player carried after 8 rounds is recorded in gate A5 (`GM.playerDDGStackAfter8`).
   - Decide whether the double DDG stays.
   - Combat Protocol for Division III is candidate **Seal Prevent 100 / 2r on the player**. The roster's "redundant" label is wrong (release plan §4.3).
9. **Arakane (membership accepted).** These values are candidates:
   - The Last Directive: 40 AP, cooldown 99, IDG **30** / 5r.
   - Extermination Order: **name not approved**; 60 AP, range 5, cooldown 4 (see AR1), Elemental Seal 100 / 2r, Cleanse Prevent 100 / 2r.
   - Countermand: OTHER item, 40 AP, range 5, cooldown 6, Clear 100, PVE, reusable, drop chance 0.
   - Solar Bow (`ALqXVSL58QMfJ4DgoJ5Il`, 40 AP, range 5, cooldown 3) and Crossbow (`LbccOnzfsADLgTBPSHjKK`, 40 AP, range 3, cooldown 0). Both are **historic upstream seed rows**; a fresh read is needed.
   - Natively the full 20-rule order holds, including stealth → Countermand → weapons → move → end, and Copy → Countermand at 60 + 40 AP.
   - **One source-forced note:** Worldbreaker Chorus is ALL-method. The authored ≤6 gate is kept (it is safe and only narrows use).
10. **All four commanders:**
    - Innate Seal Prevent 100 / 99r is **LOCKED**. Gate A1 shows it passes the AI write schema as a passive effect.
    - Each rule set ends `move` (gated at distance ≥3), then an unconditional `end_turn`. This follows the pattern of Arakane's rule 19 and keeps the end rule reachable for the validator. The engine also appends its own `end_turn`, and gate A found no exhaustion give-ups.

## C. New content needing acceptance

11. **16 regular enemies** (`design/regulars.json`). Names, identities, shared-pool kits (no commander signature jutsu reused), rules and the stat ladder in `economy_and_f3.md` §1 are all CANDIDATE. Usernames must be unique game-wide (law 66); live collisions are unchecked.
12. **Four puzzles** (`design/script.json`, rendered in `compiled/story_script.md`):
    - Each puzzle is logically solvable from three clues planted in the same division's first three dialogs; gate C verifies the clue text.
    - Answers are displayed in a different order per division, so the correct answer is not always first.
    - **Division IV foreshadows:** the "unsigned directive" option and the Order-Bearer's blank seal hint at the unknown issuer without exposing it. Confirm this stays within "no premature exposition".
13. **Story script, all 99 objective texts.** Key beats:
    - The exterior is deserted.
    - The personnel are revealed as reconstructions in Division I (hint) and Division II (explicit, via Replicant Zero), and are never undead.
    - The Grand Marshal is shown as "the Second".
    - Arakane's dignity is kept.
    - The final order arrives after his defeat, from an unshown issuer.
14. **Beacon item** (new): rarity, tradability, source and drop rate. The disclosure copy follows RUL-2026-10-16-003 and the timing is **LOCKED**.
15. **Security Alert magnitude:** candidate IDT 10% / 2r on the player.
16. **Combat Protocol magnitudes, Divisions I–III:** Stun Prevent 100 / 2r · IDG 25 / 3r · Seal Prevent 100 / 2r.
17. **Cache identities and contents.** Names, art, rarity, tradability, recipe shortlist, quantity model and weights. The mechanics are proven; the values are **BLOCKED**.
18. **`maxAttempts` / `maxCompletes`:** candidate 100 / 100 (the validator maximum).
19. **Art shotlist** (`art_shotlist.md`): 20 avatars, 6 scenes and 5 icons. No binaries produced.

## D. Integration (not blocking offline authoring)

20. **Rulings ID collision.** `RUL-2026-10-14-001` is the Bastion Medical100 ruling on this branch and an unrelated art ruling on main. Both decisions survive; reconcile the IDs deliberately at integration.
21. **Source drift.** All authoring and native gates ran at upstream `0651b039`, the current main when the run started. The C99 topology gates were re-run there in the reward proof and pass.
22. **Spoilers (F4/F5).** Quest text, including the aftermath, is readable through the public API even while hidden. The narrative order holds only in the intended UI.

## E. LOCKED — do not reopen

- `alt99_f4gate`: 99 objectives.
- Four interior divisions, deserted exterior, no Gatewarden.
- 50% recovery; Medical sets 100%; player-side Combat buffs; Security Alert on a wrong puzzle answer.
- Arakane defeat hard-fails the attempt.
- Beacon charged at `startQuest`, once per attempt, never refunded.
- Exactly one of two caches at quest level after completion.
- Commander kit memberships (Grand Marshal's kit is a candidate) and The Last Directive's effects.
