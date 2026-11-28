# Isonade v4: a rotation fight (proposal, 2026-11-19)

Asked by the director (2026-11-19 14:40Z): "Cycle sounds fine but finishing at 82% is not a very engaging fight.
Perhaps we should cut some of the set pieces and try to make an engaging boss rotation as well. Analyze our PvP
knowledge and replays to propose a boss that uses a rotation that endgame PvPers will need to play smartly around."

Design only. Nothing built, run or changed. Research notes: the PvP skills, tonight's Ashutosh review
(/mnt/project-files/tnr/ashutosh_review/), the Nov 13 and Nov 15 battle logs, `isonade_v3_results.md`,
`isonade_parity_review.md`, the PvE encounter skill. Numbers below are estimates, not simulated.

## Why v3 was easy

dauntless dealt about 3,500 a round; Isonade dealt about 918 in 12 rounds, all from pool ticks. No Slam or Black
Water touched him. Every threat was "stand on the right tiles", which a reading player answers for free. The boss
never buffs, walls or Clears, so a setup-and-cash-out player runs unopposed. Ashutosh, by contrast, bursts 1,900 to
3,950 in one round after one or two visible setup turns, and the fights were won or lost on reading those turns.

## What goes

Slam rows and their pools, Black Water and its safe crates (a safe-spot mechanic), Undertow's pull, the triple-damage
feed window, every HP-threshold interrupt. The Grasping Arm stays as the one add (stun builds get a target; it is
already built and tested).

## The rotation: four beats, one per round, then repeat

Each beat is one 60-AP jutsu that also casts the marker for the next beat. Markers use debuff-polarity tags so a
player's Clear on the boss removes buffs but never breaks the chain. Extras (Scour, the Arm) cost 30, so two beats
never fit in one round and a beat never slips.

1. **Barnacle Hide** (wall). Instant shield on self (about 2,500) and 30% absorb next round. Log: "Barnacles close
   over its hide." Right play: pop the shield with cheap hits or pierce, set up buffs, don't spend the big hit here.
2. **The Tide Draws Back** (tell). Two damage-given buffs on self and a Brine Brand on the player (+25% damage taken),
   both live next round. Log: "The water pulls away from the shore." Right play: Clear the boss's buffs, Cleanse the
   Brand, shield, heal, Chakra Resistance. Each answer cuts the Break.
3. **Breaker** (burst). Big normal hit and a wound on the player, then self weakness for one round (the window).
   About 2,000 (40% of a 5,050 player) unanswered, about 600 with one good answer. Under the 50% cap; no KO.
4. **Harpoon Line** (kill shot). Fixed pierce of about 550 (11% of max HP), ignores DR and Smoke. Lands in the window
   round, so the right play is to cash out while staying above it, and to Cleanse the Breaker wound first if a tick
   would cross that line.

**Scour** (extra, once every 10 rounds): if the player is carrying a big damage buff stack (target_has_effect,
damage-given total 60+), Isonade Clears it. Log: "The undertow tears your stance away." Right play: bait it with a
cheap buff, or stack the round after it fires. Probe archetype in the PvE skill: needs a sim run before freeze.

**Bite** (once, below 50%): the next Tide Draws Back adds a third buff. That Breaker is the one worth your one Clear.

About 12 rules of the 20. Damage tags in the 40-80 power band scaled through the stats multiplier, so Chakra
Resistance's flat cut is worth 15-25% as in PvP (at v3's 360-640 power it is worth 2-3%).

## Who it's tuned for

A strong endgame player playing well: dauntless's PvE kit at level 100, no consumables, the anchor at about 3,500
damage a round on open rounds. Estimate over 12 to 15 rounds (3 to 4 cycles): three answered Breakers about 1,800,
three Harpoons about 1,650, Arm chip about 600, less about 1,000 healed: about 3,000 net, ending near 40%. One
misread Breaker costs about 1,400 more (ends near 12%); two lose the fight. Boss HP to be re-solved in the sim against
that anchor (v3 was 42,420; the Shell rounds slow the player, so expect higher).

## Not settled, and what fits before Friday 6 PM CT

- Seat: whether the player acts before Isonade in the Flooded Stores fight. If the player acts first, only instant
  answers meet the one-round tell (Clear, Cleanse, shield, heal, Chakra Resistance); Smoke and DR are a round late.
  Check before building; if needed, the tell becomes two beats.
- Whether target_has_effect sees a buff the player cast this round (Scour's harshness).
- The shared-cooldown table read live for every new tag (clear, pierce 3 rounds) before tuning.
- Fits by Friday if approved today: about 6 new jutsu and a new rule list (hidden), a sim on the current harness
  (pin 3314d122 plus the live lock table) for HP and damage, then one hidden test on dauntless. Re-pinning the sim to
  the game's current main does not fit before Friday.
- 30 to 80 players: Isonade stays fixed at level 100 and is the optional fourth fight; the Shallows page doesn't need
  it.
