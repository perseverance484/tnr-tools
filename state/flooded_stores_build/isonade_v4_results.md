# Isonade v4: two Black Waters, a rotation and player-style reactions (sim results, 2026-11-19)

Asked by the director (2026-11-19 15:16-15:19Z): keep the rotation and add two different Black Water set pieces;
numbers stronger ("25% increased damage taken won't result in 1400 more damage"); the boss Smokes, Clears and
Cleanses "like a player would when it reaches a threshold", with no tells; it acts second, so abuse player-2
advantage; "60ap to clear or cleanse then the remainder could go to a weapon".

Offline sim only. Zero live requests, nothing built, no fight run. Files: `isonade_v4_spec.json` (17 new jutsu,
20 rules, validated), `isonade_v4_results.json` (summaries and every fight), `harness/isonade_v4.ts`,
`harness/iso_cal.ts`. Engine pin 3314d122 with the live shared-cooldown table (Nov 18 capture) and live damage config.

## Revision 3 (2026-11-19 16:11Z): its own DR, so misses lose fights

Asked by the director: "So players still dont lose? The boss might need more DR". Isonade now layers its own damage
reduction like a PvP player, all of it buffs the player's Clear can strip:

- Barnacle Hide: shield plus 40% DR, 2 rounds.
- The Tide Draws Back: 40% DR, 2 rounds, alongside its damage layer and the brand.
- The Swell Builds: 30% DR, 1 round (covers the Breaker round).
- Shed: 40% DR, 2 rounds, after its cleanse.

The player's Clear now has two jobs (its DR or its burst) on one cooldown. Rules still 20; jutsu still 17.

Proposed targets (perfect / one miss / two misses / ignores): wins 95-100% / about 60% / about 45% / 0-10%.

| Read | Win % | Rounds (median) | HP left when won (median / p10) | Boss HP left when lost |
|---|---|---|---|---|
| 1 (answers every tell) | 100 | 12 | 45% / 14.5% | - |
| 0.85 (misses ~1) | 60 | 12 | 49.5% / 14.5% | 31% |
| 0.7 (misses ~2) | 45 | 12 | 49.5% / 1.6% | 30% |
| 0 (ignores everything) | 0 | - | - | 45% |

Damage taken per fight at read 1: Breaker 1,635, Anchor 776, Arm 725, Harpoon 444, wounds 293. A missed Breaker is
about 2,700-3,030.

## Revision 2 (2026-11-19, after the director's two corrections)

1. "It can see any tag using the conditional has_effect check." Re-read on today's game `main` (26391b51,
   `libs/combat/ai_v2.ts` `reachesEffectPower`): has_effect / target_has_effect sum the stored power of every effect
   of that type on the target and pass when the sum is at or above the threshold (0 to 100; 0 always passes). Decrease
   damage taken and decrease damage given are stored with negative power the moment they are cast (`tags.ts`
   `decreaseDamageTaken` / `decreaseDamageGiven` call `invertPower`, which rewrites `effect.power` in place; same on the
   pin and on main). Tested in the sim: the player's Defensive Stance reads -15 on the boss's turn and a Scour rule on
   target_has_effect decreasedamagetaken 20 never fires. So a DR or DDG stack can't be a trigger. Scour fires on what
   the condition can read: absorb 60+ (DR kits such as Folding Screen Guard carry absorb), shield 100+, damage given
   80+.
2. "You can do multiple IDG/IDT buffs on the same jutsu or layer them across a combination of jutsu to create a burst
   window." Confirmed: each tag gets its own effect, and in-battle percentage modifiers multiply one after another
   (`damagePipeline.ts` `applyPercentageIncreases`, same pipeline in the pin's `process.ts`). The 100 cap is per tag,
   not per stack. The burst is now two beats of layers: The Tide Draws Back (+50% damage given on itself for 2 rounds,
   Brine Brand +30% damage taken on the player for 2 rounds) then The Swell Builds (another +50% and +30%, 1 round),
   then Breaker (400 power) with all four live: x3.8. Bite is gone (it was the same idea, once).

Other changes: Shed moved below the burst beats (its cleanse wiped the boss's own chain markers and ate the Breaker),
so it now takes the Hide slot; the Deep's shield is 1,500 (2,500 and 2,000 held against an unplanned turn). 20 rules,
17 new jutsu, spec validated.

Counterplay to the burst: Clear its two damage layers, Cleanse the two brands, Defensive Stance, a smoke bomb on it.
Scour then Drowned Anchor punishes a player who turtles behind absorb or shields during the build-up.

## Revision 2 sim results (20 seeds each)

| Read | Win % | Rounds (median) | HP left when won (median / p10) |
|---|---|---|---|
| 1 (answers every tell) | 100 | 12 | 45% / 45% |
| 0.85 (misses ~1) | 95 | 12 | 46% / 24.6% |
| 0.7 (misses ~2) | 90 | 12 | 44.7% / 22.5% |
| 0 (ignores everything) | 40 | 9 | 4.5% / 2.3% |

Breaker: about 3,030 ignored (48% of 6,250), about 1,140 with the layers Cleared and a Stance. Damage taken per fight
at read 1: Breaker 1,144, Anchor 776, Arm 553, Harpoon 444, wounds 257. The Deep shows in about 60% of read-1 fights:
a strong player often kills Isonade from 40% before its slot comes round.

Revision 1 (below) is kept for the record.

## Revision 1: The fight

Boss 20,200 HP, level 100. The Grasping Arm stays as the one add.

**Rotation (one beat a round, each beat lays the marker for the next):** Barnacle Hide (1,500 shield) -> The Tide
Draws Back (+100% damage given on self, Brine Brand +50% damage taken on the player, both live next round) ->
Breaker (450 power hit + wound) -> Harpoon Line (fixed pierce) -> repeat.

**Black Water I, at 75% HP:** the room floods; only the crates are safe next round. About 1,800-1,900 if ignored.

**Black Water II, The Deep, at 40% HP:** Isonade sinks behind a 2,500 shield (70 AP, so nothing else rides along).
Break it in your next turn or the crash hits the whole room for about 2,590. The crash also washes Isonade clean.
HP gates, not cycle slots, so a fast player can't skip either one.

**Reactions (no tells; checked against what the AI can see after the player acts, since it acts second):**
- Scour (Clear, 60 AP): fires when the player carries absorb 60+, shield 100+ or a damage-given buff 80+. Then
  Drowned Anchor, its own weapon (30 AP, 150 power), fills the rest of the round.
- Shed (Cleanse, 60 AP): fires on a wound 5+ or damage-taken 40+ on itself, then re-lays the Tide marker, so a
  Cleanse never resets the rotation.
- Silt Cloud (Smoke, 30 AP): when the player stacks damage given 60+, halves the player's next-round damage and
  gives itself 25% less damage taken for 2 rounds.

20 of 20 rules.

## Engine findings that shaped it

- Isonade always acts second, and `target_has_effect` sees an effect the player cast that same round. Player-2
  advantage is real: it Clears a buff before the buff ever lands.
- The AI cannot see DR or damage-dealt-down stacks. Those tags store negative power, and the condition needs power
  at or above a positive threshold, so a rule on them never fires. It reacts to damage buffs, absorb and shields.
- One buff tag caps at 100 power (validators/combat.ts), so +100% is the ceiling for a single Tide buff. Two tags of
  the same type in one jutsu merge. Hence Tide +100% and Brand +50%, not stacked smaller buffs.
- Brand math: a Breaker the player ignores hits about 2,700 (43% of 6,250). Cleared, with a stance, about 1,140.

## Sim results (20 seeds each)

Player: stand-in calibrated to dauntless's live 12-round v3 kill (6,250 HP, PvE kit, pet), no consumables or smoke
bombs. "Read" = how often it answers a tell correctly.

| Read | Win % | Rounds (median) | HP left when won (median / p10) |
|---|---|---|---|
| 1 (answers every tell) | 90 | 11.5 | 50.4% / 48% |
| 0.85 (misses ~1) | 80 | 11 | 48.8% / 12.5% |
| 0.7 (misses ~2) | 65 | 11 | 48% / 15.5% |
| 0 (ignores everything) | 100 | 12 | 7.2% |

Damage taken per fight at read 1: Breaker 1,426, Anchor 648, Arm 547, Harpoon 394, wounds 253. The Deep was broken
in 100% of read-1 fights. Both Black Waters appear in every fight.

The two read-1 losses are a second Breaker landing while Clear is still on its 10-round cooldown: only a Cleanse
is left, and after Bite it hits about 2,830. A real player has smoke bombs and items for that round; the sim player
doesn't.

Read 0 still winning at 7% is the price of a hard but fair fight for an 81+ PvP player: ignoring every tell brings
you to the floor; one more miss on top of that loses.

## Limits

- Engine pin 3314d122, not today's game `main` (see `isonade_parity_review.md`, conflict 6).
- The stand-in player has no consumables, smoke bombs or burst planning; seeds are fairly deterministic.
- Read 1 sits near 50%, above the "near 40%" target; one more nudge (more boss HP or chip) would close it. Left for
  the live test to settle, since the live player is stronger than the sim's.

## Fits by Friday 6 PM CT if approved

A hidden build of the 17 new jutsu and the 20-rule list over the connector, then one hidden test on dauntless.
Re-pinning the sim to the game's current `main` does not fit.

## Live hidden test (2026-11-19 16:33-16:46Z, after jobs 651/652)

One run of The Flooded Stores on dauntless (PvE kit, pet Little Horror). Crew fights 1-3 won at full HP (5, 3 and 5
rounds). Pools carry over between the four fights: the run is an isolated pyramid, so food and shops are refused
mid-run (dauntless entered Isonade at full HP, 3,734 chakra and 3,718 stamina of 5,050).

**Isonade: lost in round 11, Isonade at 78% (15,751 of 20,200).** Sim target for a perfect read: 100% wins, median
12 rounds. Log: /mnt/project-files/tnr/battle-logs/2026-11-19_isonade_v4_test_UxWYi_H4aAf1qk_crwkoB.json.

Damage taken: Breaker 3,524 (one hit), Drowned Anchor 2,821 (two hits), Arm Lash 1,030, Harpoon Line 505, wounds 446.
Damage dealt: 4,449 to Isonade's HP and 1,999 into its Barnacle Hide shields, in 11 rounds.

What happened, round by round:
- r1 Overflow (+35% x2 damage given), walk in. Isonade: Scour, then Drowned Anchor on everyone: 587 on dauntless,
  13,635 on the pet (one hit; the pet was 5+ tiles away).
- r2 Ember Blade 1,234, Ignition. Isonade: Shed (cleanses the Ember brand, 40% DR) and Silt Cloud (-50% given, 25% DR).
- r3 Clear on Isonade (strips Shed, Silt and its rotation markers), Severed Pulse. Isonade: Barnacle Hide, Arm rises.
  The rotation carried on after the Clear.
- r4 Storm Fist 945 and a basic attack, all into the shield. Isonade: Tide Draws Back.
- r5 Thunderbolt and basics on the Arm. Isonade: Swell Builds.
- r6 Cleanse (both brands off) and Defensive Stance; Clear still on cooldown from r3. Isonade: Breaker 3,524, wound
  211 per action for 2 rounds.
- r7 Rebirth 2,874, Invigoration. Isonade: Harpoon Line 505.
- r8 Basic Heal. Isonade: Barnacle Hide. r9 killed the Arm; Isonade raised it again the same turn, then Tide.
- r10 Storm Fist into the shield, Ignition. Isonade: Swell. Neither Black Water fired (75% gate never reached).
- r11 Clear and Cleanse both still on cooldown; Stance and Chakra Shield. Isonade: Scour (on the shield) then Drowned
  Anchor 2,233 with both damage layers live. Defeated.

Live vs sim:
- Breaker with both brands cleansed and a Stance hit 3,524, above the sim's 2,700-3,030 for a Breaker that is
  ignored outright. The sim's 1,140 needs Clear on the damage layers too, and Clear is one cooldown for two jobs.
- Isonade's DR layers (Hide 40, Tide 40, Swell 30, Shed 40, Silt 25) cut dauntless's hits to about a fifth of what
  the same moves did to the crew (Storm Fist 5,593 on the Quartermaster, 945 on Isonade).
- Scour preempts Breaker when both qualify (r11). Drowned Anchor hits every enemy on the board and one-shots a pet.
- Play errors on the tester's side: Clear spent on Shed/Silt in r3 left it down for both Breakers; Overflow in r1 and
  Chakra Shield in r11 fed Scour.

## Revision 4: DR retune (2026-11-19 17:06Z, the director)

Asked by the director after the live test: "Yes, lower its damage reduction to one generic 25-30%/2 rounds, and one
stronger one it uses in anticipation of a big hit at 40%/1 round".

- Barnacle Hide keeps its 1,500 shield; its DR is the one generic layer, 25% for 2 rounds (picked from his range: the
  sim's perfect-read win rate is 83% at 25 and 67% at 30, and dauntless took more live than the sim's player does).
- DR removed from The Tide Draws Back, The Swell Builds and Shed.
- Silt Cloud is the brace: 40% DR for 1 round, cast when the player's damage-given buffs reach 60. Its -50% damage
  given on the player is dropped. Its rule moves from slot 17 (below Barnacle Hide, so it almost never fired) to slot 7,
  above the Drowned Anchor follow-up. Still 20 rules. Cooldown stays 10 (4 changed nothing in the sim).
- Hits unchanged (Breaker 400, Drowned Anchor 150, Harpoon 20, Arm Lash 45): the director gave no numbers for them.

Sim (12 seeds per read, same player model as revision 3; files in `v4_retune/`):

| Read | Rev 3 win % | Hide 30 win % | Hide 25 win % | Rounds (25) |
|---|---|---|---|---|
| 1 (answers every tell) | 100 | 67 | 83 | 11 |
| 0.85 | 60 | 75 | 75 | 11 |
| 0.7 | 45 | 75 | 75 | 11 |
| 0 (ignores everything) | 0 | 17 | 33 | 9 |

Losses now come late, with Isonade under 2% at a perfect read and 12-16% at weaker reads: the player runs dry on HP.

Against today's live log:
- Breaker in the live state (both damage layers on, brands cleansed, Stance) is 2,177 in the sim and 3,524 live:
  dauntless takes about 1.6x what the sim's player takes. The sim's numbers above are optimistic for dauntless.
- Re-scoring dauntless's live hits on Isonade under the new DR adds roughly 700-800 damage over the 11 rounds: the old
  layers rarely stacked on a hit. The live loss was damage taken (Breaker 3,524, two Anchors 2,821) and three rounds
  spent on the Grasping Arm, not DR. Cutting the hits is the bigger lever; that's the director's call.

## Revision 4 live hidden test (2026-11-19 17:17-17:25Z, push 653, Hide 25%)

One hidden run on dauntless, PvE kit, full HP before every fight. Battle uHjSwGVSB409OFHehyWxA.
Log: /mnt/project-files/tnr/battle-logs/2026-11-19_isonade_v4r4_test_uHjSwGVSB409OFHehyWxA.json.

- Crew fights: won in 4, 3 and 5 rounds. Entered Isonade at full HP.
- Isonade: **WON in round 12**, dauntless at 4,030 / 5,050 (80%). Lowest point 2,682 (53%) at the start of r8.
- Sim at read 1 for this build: 83% wins, median 11 rounds. The live run sits inside that.

Round by round:
- r1 Thunderbolt. Isonade: Barnacle Hide (25% / 2 rounds, 1,500 shield), Arm rises, Arm Lash kills the pet.
- r2 Storm Fist into the shield, Ignition. Isonade: Silt Cloud brace (40% / 1 round), Tide Draws Back.
- r3 Ember Blade, Severed Pulse (shield gone). Isonade: Scour, then Drowned Anchor 1,145.
- r4 Clear on Isonade (Tide's +50% off), Defensive Stance. Isonade: Swell Builds.
- r5 Cleanse (both brands off), Invigoration. Isonade: Breaker 1,997 (660 absorbed back).
- r6 Rebirth 2,707, Stormguard. Isonade: Harpoon Line 505.
- r7 Dragon's Tomb, Eclipse Drain. Isonade: Shed (on the tomb's wound), Drowned Anchor 285.
- r8 Thunderbolt, Stance. Isonade: Omen Black Water.
- r9 walked to the crate at (6,1), Storm Fist 2,092. Black Water missed; Isonade surfaced (weak).
- r10 Ember Blade 2,555, Severed Pulse. Isonade: Omen The Deep (1,500 shell).
- r11 Thunderclap broke the shell, Stance. Isonade surfaced (weak).
- r12 Stun Jab 6,301, kill.

Damage taken: Breaker 1,997, Drowned Anchor 1,430 (two hits), Harpoon 505, wounds about 450, Arm Lash 0
(it only ever hit the pet and its own side). Lifesteal and absorb gave back about 2,100.

What changed from the 16:46Z loss: the boss's own DR no longer stacks, so the player's damage lands; Breaker hit
1,997 instead of 3,524 because the Clear went on Tide in r4 instead of on Shed/Silt; the Arm cost no rounds.

Findings for the director:
- Silt Cloud fired in r2 with only Thunderbolt's displayed 38% damage given on the player, and Scour fired in r3 at
  a displayed 38% + 35%. Both thresholds (60 and 80) read the stored power, which looks higher than the % the
  battle log shows. A player cannot judge "stay under 60" from the log. Worth knowing before tuning those rules.
- Silt did not fire again (cooldown), so the brace showed once.
- Hits were not cut; that stays his call.
