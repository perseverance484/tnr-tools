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
