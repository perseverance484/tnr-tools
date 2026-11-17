# The Gobblefather (Thanksgiving 2026) - build notes

Source: `state/gobblefather/event_sheet.txt` (staff sheet, verbatim).
Generator: `push/622_gobblefather_core.gen.py` (one script, two manifests).

| Job | Manifest | Contents | Gates |
|---|---|---|---|
| 622 | `push/622_gobblefather_jutsu.json` | 15 AI jutsu, hidden | validate.py 0/0, check_manifest 0 |
| 623 | `push/623_gobblefather_ai_quest.json` (built from 622's bundle) | 7 AI + quest, hidden | dry: check_manifest 0; validate.py 7 x law-14 preferredStat, ledgered (RUL-2026-10-25-009) |

Two steps because AI `jutsus` arrays need literal ids (law 17).

## Quest shape

`questType: event`, rank S, requiredLevel 75, 30 nodes. Every fight sits behind a dialog.

Goah (o1) -> Trade Road / Hachiro (o2-o3) -> Tollgate (o4-o5) -> **Drumstick Brothers** (b6)
-> Golden Silo guards (b8: Enforcer x2, Corn Collector x2) -> **Don Giblet** + Accountant x2 (b10)
-> Feathered Estate (o11-o12) -> **The Gobblefather** + Enforcer x2 (b13) -> defeat scene (o14)
-> Goah (o15) -> narration (o16) -> win.

- Losing b6/b8/b10 resets to the dialog before that fight (lose-retry). Losing b13 = fail_quest with the sheet's Objective X line.
- The sheet's "Move to Location" steps are arrival dialogs with a scene, not map travel (no sectors, no co-firing risk).
- Choices that the sheet sent to the same node now each get their own reply beat first (house rule: no decorative menus). Don's and the Gobblefather's extra sheet lines fill those beats.
- Phase lines are in the jutsu combat-log text: Gravy Release says "NOW IT'S PERSONAL!", Omertà says "THE FAMILY IS POWER!", Feather Tax says "Your chakra has been repossessed."

## How the sheet's mechanics landed (no new code)

| Sheet mechanic | Built as | Gap |
|---|---|---|
| Family Business: Tony buffed while Vinny lives | Tony self buff, used every time it's ready | Engine can't check if an ally is alive |
| Family Vengeance when a brother dies | not built | Same limit |
| Wing Guard shields Tony or himself | Vinny self damage reduction, under 60% HP | Self only |
| Bleed (Feather Barrage, Flying Drumsticks) | afterburn | No bleed tag. Wound skipped: its statTypes rule disagrees between lint L06 and the source |
| Debt Marks stack, Collection Day consumes them | Compound Interest = small hit + 15% increased damage taken, 4 rounds, cooldown 2 (stacks). Collection Day (80) fires only while the target carries the mark | Marks aren't consumed. Cleansing still removes them, which is the counterplay the sheet wants |
| Emergency Audit | shared pool Purging Stance (cleanse), under 50% HP | Shows the pool name in the log |
| Feather Tax steals chakra into a shield | hit + chakra drain + 25% absorb on Don | |
| Gobblefather phases at 70% / 35% | health_below rules: Gravy + Flying Drumsticks under 70%; Omertà + Final Feast under 35% | Can't stay seated in phase 1 |
| Family Protection summons enforcers | the final fight starts with 2 Enforcers; skill = shared pool Bulwark Charge (shield + damage) | A summon jutsu needs the enforcer's id before it exists |
| Interrupt The Final Feast | not built | No channel/interrupt mechanic |
| Gravy Goon | not used | The sheet never puts it in a fight |

Signature budget: Tony 3, Vinny 3, Don 4, Gobblefather 5. **Don and the Gobblefather go over the doctrine's 3**. Your call: keep it, or move Golden Avalanche / Offer to shared pool jutsu.

## PLACEHOLDERS (your decision)

1. Enemy level 75 on all AI; every fight `opponent_scaled_to_user: true`.
2. Multipliers: supports 1/1; bosses pools 2 / stats 3; Gobblefather pools 3.
3. AI stat shape: masteries weighted to each boss's school, uniform otherwise.
4. Jutsu numbers (power / rounds / cooldown):
   - Concrete Clobber 65 + stun 1r, cd 4, range 2 | Feather Barrage ALL 40 + afterburn 20/2r, cd 5 | Family Business +30% dmg 3r, cd 5
   - Wing Guard -35% taken 2r, cd 5 | Back-Alley Counter reflect 30% 2r, cd 6 | Double Drumstick Beatdown 75 + stun 1r, cd 7, range 3
   - Golden Avalanche ALL 45 + speed -15% 2r, cd 5 | Feather Tax 35 + chakra drain 20/2r + absorb 25% 2r, cd 6 | Compound Interest 25 + taken +15% 4r, cd 2 | Collection Day 80, cd 6
   - Offer 30 + dmg given -20% 3r + pool cost +25% 3r, cd 5 | Gravy ALL 45 + moveprevent 1r, cd 5 | Flying Drumsticks 60 + afterburn 15/2r, cd 4 | Final Feast ALL 85, cd 8 | Omertà -30% taken + reflect 25%, 99r, cd 10
5. Quest rewards (from the sheet): 18,000 exp, 15,000 ryo, 600 prestige, 500 tokens, 600 clan points, on the quest so they show on the description screen.
6. Launch block not set: dates, maxAttempts / maxCompletes, unhide list.

## Not in this build (follow-up jobs)

- **Art:** 6 backgrounds, scene characters (Goah, Hachiro, Toma, the brothers, Don, Gobblefather), 7 AI avatars, 15 jutsu icons (currently the default image), quest icon. Goes through producing-tnr-art, then a Forge image run.
- **Rewards:** title "The Tax Evader", badge "Family Business", item Golden Feathered Ring, item Gobblefather's Cane. Need art and your stat/rarity call.
- **Hidden achievement "Not a Single Kernel"** (beat him without being hit by The Final Feast): achievements can't track hits taken. Not buildable as written.
- Farmer Toma is in the character list but in no objective. The sheet's flow never uses him.

## Repo debt found (Lane A, not fixed here)

- `enemy.py` and `validate.py` still use the old AI stat fields (8 offence/defence + preferredStat). The game and Forge use masteries + offence/defence. The generator converts them; the tools need a fix.
- `enemy.py` targets self-stance rules at RANDOM_OPPONENT. The generator rebuilds those rules.
