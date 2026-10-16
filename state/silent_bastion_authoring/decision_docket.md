# Silent Bastion — director decision docket (one list)

Everything below needs the director. Items marked **LOCKED** are already ruled and are listed only so nothing gets re-opened by accident. Evidence paths are relative to the repository root. "Gate A/C/R…" means the authoring harness `harness/silent_bastion_authoring/` (results in its `results/`) or the reward proof on its own branch.

## A. Native-test results still open

All five native-test blockers from the first run were ruled on 2026-10-16; see **F. Resolved**. Only the validator results below remain in this section.

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
8. **The Grand Marshal.** Kit and priorities **RATIFIED** (RUL-2026-10-16-006), including the stacked suppression; see F. Combat Protocol for Division III is candidate **Seal Prevent 100 / 2r on the player**. The roster's "redundant" label is wrong (release plan §4.3).
9. **Arakane (membership accepted).** These values are candidates:
   - The Last Directive: 40 AP, cooldown 99, IDG **30** / 5r.
   - Extermination Order: **name not approved**; 60 AP, range 5, Elemental Seal 100 / 2r, Cleanse Prevent 100 / 2r. Cooldown 4 is **approved** (RUL-2026-10-16-004).
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
- Commander kit memberships (Grand Marshal's kit ratified, RUL-2026-10-16-006) and The Last Directive's effects.

## F. Resolved 2026-10-16 (rulings in `docs/RULINGS.md`)

| Item | Decision | Ruling | Where it lands |
| --- | --- | --- | --- |
| AR1: Extermination Order on an expired Final Stand | Cooldown **4** (residual risk accepted; no engine change) | RUL-2026-10-16-004 | `design/commanders.json`; gate A6 probe |
| F3: recovery-loop battle income | **O2**: `scaleGains: 0` on the 8 recovery battles | RUL-2026-10-16-005 | `design/entry_and_rewards.json`; gates C and I |
| Grand Marshal kit and priorities | **Ratified** as translated | RUL-2026-10-16-006 | `design/commanders.json`; roster §4 |
| SRC1: Veilstep record vs design | Use the captured record (**Stealth 1r, cooldown 5**); shared jutsu not edited | RUL-2026-10-16-007 | Arakane profile; gate A6 |
| D5: Division IV Combat Protocol | Pick delegated; **Debuff Prevent 100 / 3r** (option A) | RUL-2026-10-16-008 | `design/protocols.json`, D5 text in `design/script.json` |
| RC1: unclaimed cache blocks the next completion | **Accepted** with the "claim before you set out" entry copy | RUL-2026-10-16-009 | quest description in `design/script.json` |
