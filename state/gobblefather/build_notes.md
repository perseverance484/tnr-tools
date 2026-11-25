# The Gobblefather (Thanksgiving 2026) - build notes

Source: `state/gobblefather/event_sheet.txt` (staff sheet, verbatim). Planner's calls: RUL-2026-11-25-168.
Generator: `push/622_gobblefather_core.gen.py` (one script, two manifests). Art: `state/gobblefather/art_shotlist.md`.

| Job | Manifest | Contents | Gates |
|---|---|---|---|
| 622 | `push/622_gobblefather_jutsu.json` | 12 AI jutsu, hidden | validate.py 0/0, check_manifest 0 |
| 623 | `push/623_gobblefather_ai_quest.json` (built from 622's bundle) | 7 AI + quest, hidden | dry: check_manifest 0; validate.py 7 x law-14 preferredStat, ledgered (RUL-2026-10-25-009) |
| image job | (after art) | scenes on the quest, AI avatars, badge + reward_badges | - |

Two steps because AI `jutsus` arrays need literal ids (law 17).

## Quest

`questType: event`, rank S, requiredLevel 75, runs 2026-11-26 to 2026-12-03, unlimited tries (maxAttempts -1), one
completion. 30 nodes; every fight sits behind a dialog.

Goah (o1) -> Trade Road / Hachiro (o2-o3) -> Tollgate (o4-o5) -> **Drumstick Brothers** (b6)
-> Golden Silo guards (b8: Enforcer x2, Corn Collector x2) -> **Don Giblet** + Accountant x2 (b10)
-> Feathered Estate (o11-o12) -> **The Gobblefather** + Enforcer x2 (b13) -> defeat scene (o14)
-> Goah (o15) -> narration (o16) -> win.

Losing b6/b8/b10 resets to the dialog before that fight. Losing b13 = fail_quest (Objective X line); with unlimited
tries the player simply starts again.

## Kits (3 signatures per boss, the rest shared pool)

| Boss | Signatures | Shared pool |
|---|---|---|
| Tony | Concrete Clobber, Feather Barrage, Family Business | S42 |
| Vinny | Wing Guard, Back-Alley Counter, Double Drumstick Beatdown | S41 |
| Don Giblet | Compound Interest, Collection Day, Feather Tax | S34 (Emergency Audit), S28 (Golden Avalanche) |
| Gobblefather | Flying Drumsticks, The Final Feast, Omertà | B23 (Family Protection), A3 (Gravy), S27 (Offer) |

Phases: under 70% HP Flying Drumsticks ("NOW IT'S PERSONAL!") and the area attack; under 35% Omertà ("THE FAMILY IS
POWER!") and The Final Feast. Debt Marks = increased damage taken, cleansable; Collection Day fires only on a marked
target. Not built (engine limits): Family Vengeance, interrupting The Final Feast, a mid-fight summon.

## Still open

- Rewards (item 21): sheet values are placeholders (18,000 exp, 15,000 ryo, 600 prestige, 500 tokens, 600 clan
  points) pending the teammate's answer.
- Balance placeholders: enemy level 75 scaled to the player; multipliers; jutsu numbers. Final Feast to be toned down
  on launch day if too strong.
- Ring and cane: proposals with the director.
- Art: 19 shots in `art_shotlist.md`.

## Repo debt found (Lane A, not fixed here)

- `enemy.py` and `validate.py` still use the old AI stat fields (8 offence/defence + preferredStat). The generator
  converts them.
- `enemy.py` targets self-stance rules at RANDOM_OPPONENT. The generator rebuilds those rules.
- Pinned 45d says quest maxAttempts min 0; upstream and the live schema take -1 (unlimited). The generator sets -1
  after construction. The pinned contracts need a re-extract (the sentinel has flagged drift since 2026-11-22).
