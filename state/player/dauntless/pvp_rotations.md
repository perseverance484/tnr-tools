# PvP rotations: the director's PvP loadout

Planned rotations and a priority rule set, in the style of PvE AI rules but without limits on complexity. They are
built on `state/player/combat_rules.md`, which holds the timing, damage, pierce and shared-cooldown rules. Numbers are
live (`jutsu.get` / `item.get`, 2026-11-10) at jutsu level 25 (`power + 25 x powerPerLevel`) and match what the
battle logs showed.

## 1. Kit card

**60 AP jutsu**

| Jutsu | CD | Instant effect | Tags (live next round) | Shared lock |
|---|---|---|---|---|
| Ethereal Rebirth | 8 | dmg 45, Highest | absorb 35% on me (3r); **-15% dmg given on me (2r)** | — |
| Shrapnel Clone Barrage | 7 | dmg 45, AoE circle | target takes 30% of non-pierce hits as afterburn (2r) | — |
| Eight Fist: Lotus Dance | 7 | dmg 45 | target buffprevent 100% (1r) | buffprevent 4 (locks Seal) |
| Forbidden Chakra Fury | 7 | dmg 45, Spd/Str, ground spiral | target recoils 40% of own non-pierce hits (2r) | — |
| Forgotten Ember Blade | 7 | dmg 40, Spd/Str | me +35% given (2r); target +35% taken (2r) | — |
| Danse Macabre | 8 | dmg 33 | target bloodline sealed (2r) | seal 3 |
| Stormblade Arc | 7 | **pierce 56, flat (~707)**, Lightning | me reflect 35% (2r) | pierce 3 (locks Night's Testament) |

**40 AP jutsu**

| Jutsu | CD | Instant effect | Tags (live next round) | Shared lock |
|---|---|---|---|---|
| Chakra Overflow | 7 | — | me +35% and +35% given (2r): x1.82 | — |
| Thunder's Judgement | 7 | — | me +30% given, reflect 35% (2r) | — |
| Parry | 7 | — | me +30% given, parry 20% (2r) | — |
| Eclipse Drain | 7 | — | me +30% given, lifesteal 35% (2r) | — |
| Subaku Palace | 7 | ground zone | me +30% given (2r); enemy on the zone -25% given (3r) | — |
| Seal of Nullification | 7 | — | target buffprevent 100% (1r); me debuffprevent 100% (2r) | buff/debuffprevent 4 (locks Lotus, Dr. Kim's) |
| Phantom Step | 6 | move up to 5 hexes | DR 20% on the landing hex (2r); me +30% given (2r) | — |
| Chakra Shield | 7 | **500 HP shield, immediate** | absorb 35% (2r) | — |

**Weapons (40 AP) and items (20 AP)**

| Action | AP | CD | Effect | Shared lock |
|---|---|---|---|---|
| Night's Testament | 40 | 6 | pierce 50, flat (~631); me immune to buffprevent (2r) | pierce 3 (locks Stormblade) |
| Aetherion | 40 | 6 | elemental dmg 30; target +20% taken (2r) | — |
| Ikazuchi Kunai | 20 | 4 | dmg 22 (5 carried) | — |
| Elite Smoke Bomb | 20 | 10 | EVERYONE -70% given (1r), me -25% taken (2r); one per fight | — |
| Panacea | 20 | 6 | me -25% taken (2r) | — |
| Colored Jewel | 20 | 6 | me +15% given, -10% taken (3r) | — |
| Chakra Pill | 20 | 4 | me +15% given, lifesteal 20% (2r) | — |
| Dr. Kim's Potion | 20 | 10 | clearprevent 100% (works now, through next round); debuffprevent (vs debuffs from next round) | debuff/clearprevent 4 (locks Seal) |

**Basics:** Offensive Stance +15% given / Defensive Stance -15% taken (20, next round only); Clear / Cleanse (60, CD 10);
Replacement (20, CD 2, range 5); Move (10); Basic Attack (20, range 1); Basic Heal (60, CD 5); Meditate (20).
**Never Flee.**

**Multipliers stack multiplicatively.** Fully set up: Overflow x1.82, Ember x1.35, one 30% buff x1.3, Pill or Jewel
x1.15 on me, and Ember x1.35 and Aetherion x1.2 on the target. Together that is about **x6 on non-pierce hits.** That
is the whole game: set up, then cash in. Pierce ignores all of it.

## 2. Timing reminders that shape every rotation
- My buffs and the target's debuffs from turn T are live on T+1 (and T+2 for 2-round tags), never on T.
- **The enemy always gets a turn between my setup and my payoff.** That is where they Clear or Cleanse. Clear-prevent
  (Dr. Kim's) is live immediately and lasts through the next round, so it covers that gap.
- Ethereal Rebirth puts -15% given on me for 2 rounds. Cast it while my debuff-prevent from Seal is live (the turn
  after Seal), and the self-debuff is blocked.

## 3. Rotations (T = my turn number)

### R1. "Locked burst": default opener when the enemy may still Clear
| T | Actions (AP) | Why |
|---|---|---|
| 1 | Chakra Overflow (40) + Thunder's Judgement (40) + **Dr. Kim's (20)** | x2.37 live on T2-T3, reflect 35% live T2-T3; Clear can't strip them during their turn |
| 2 | Forgotten Ember Blade (60) + Aetherion (40) | both hit at x2.37; set +35% given on me and +55% taken on him for T3-T4 |
| 3 | Ethereal Rebirth (60) + Chakra Pill (20) + Kunai (20) | **peak turn:** x2.37 x 1.35 on me x 1.35 x 1.2 on him, about x5.2. Absorb up for his reply |
| 4 | Shrapnel Clone Barrage (60) + Offensive Stance (20) + Panacea (20) | Ember/Aetherion still live; afterburn and stance set for T5; DR for his turn |
| 5 | Stormblade Arc (60) + Parry (40) | pierce finisher ignores any DR he stacked; Parry and reflect for T6 |
| 6 | Forbidden Chakra Fury (60) + Eclipse Drain (40) | afterburn from T4 is live, so Fury takes +30% |
| 7 | Seal (40, Dr. Kim's lock over) + Night's Testament (40, pierce lock over) + Kunai (20) | rotation resets: Overflow, Thunder and Ember are back on T8 |

Cooldowns check out: Overflow, Thunder and Ember return T8-T9; Dr. Kim's T11; Aetherion T8; Ethereal T11;
Kunai T7; Pill T7.

### R2. "Bait the Clear": quiet opener against a Clear-first player (Arashii, IndraUchiha)
| T | Actions | Why |
|---|---|---|
| 1 | Seal of Nullification (40) + Chakra Shield (40) + Defensive Stance (20) | blocks his T2 rebuff; my debuff-block T2-T3; 500 shield now; nothing big to Clear |
| 2 | **If he spent Clear:** switch to R1 from T1 (Dr. Kim's is locked until T5, so use Overflow + Thunder + Jewel). **If he didn't:** Ember (60) + Eclipse Drain (40) | his Clear is now on a 10-round cooldown |
| 3 | Ethereal Rebirth (60, its -15% blocked by Seal's ward) + Aetherion (40) | payoff on Ember/Eclipse |
| 4+ | continue R1 from T4 | — |

### R3. "Anti-finisher": against setup-then-finisher players (Arashii, Ziharkk, Korin)
Signal: in his last turn he put **+damage taken, afterburn or recoil on me**, or used time dilation or +tag power on
himself. His finisher comes next turn.

| Option | Actions | Use when |
|---|---|---|
| A | **Cleanse (60) + Elite Smoke Bomb (20) + Panacea (20)** | his stacks are on me now; Cleanse removes them before they go live, and smoke cuts his finisher 70% |
| B | Seal of Nullification (40) + Chakra Shield (40) + Defensive Stance (20) | cast *before* his setup turn: my debuff-block makes his stacks fail |
| C | Smoke (20) + Overflow (40) + Thunder's (40) | Cleanse is on cooldown: blunt his hit and set up my counter-burst |

After the smoke round, next turn is my payoff (his finisher fizzled; my setup is live).

### R4. "Pierce through": he has stacked DR, absorb or shield (e.g. Quintessential Flake -35% taken)
| T | Actions | Why |
|---|---|---|
| a | Stormblade Arc (60) + Chakra Overflow (40) | flat 707 now regardless of his DR; Overflow lands for next turn |
| b | Clear (60) if his DR is still live, + Aetherion (40) at x1.82 | strips the DR instantly, then hits |
| c | Ember (60) + Night's Testament (40, pierce lock over by c+?): check the lock (3 rounds) | — |

Pierce turns never get buffs, so always pair pierce with *setup*, not with other buffs for the same turn.

### R5. "Third-party finish": the target just won a fight and has low HP but fresh cooldowns
Buffs don't help on the first turn, so lead with instant damage and set up a lethal turn 2.

| T | Actions | Why |
|---|---|---|
| 1 | Phantom Step (40, close in) + Shrapnel (60), or Stormblade (60) + Aetherion (40) if already in range | 615 + afterburn, or ~707 flat + elemental |
| 2 | Stormblade (60) + Kunai (20, +30% afterburn) + Smoke (20) | won vs Arashii (1,393 HP + 600 heal) |

If target HP is at or below 700, Stormblade alone kills through any DR.

### R6. Gap-closer and spacing
- More than 4 hexes away: Phantom Step (40, range 5) plus a 60, or Replacement (20) when Phantom is on cooldown.
- Never spend bare 10-AP moves on a burst turn. Check cube distance first (odd-q grid).

## 4. Turn rule set (evaluate top-down every turn, like AI rules)
1. **Survive.** If his live setup threatens lethal next turn (my HP below about his last hit x his live multipliers)
   -> R3-A (Cleanse + Smoke + Panacea). If Cleanse is down: Smoke + Chakra Shield + Defensive Stance.
2. **Kill.** If his HP is at or below my instant damage this turn -> the highest instant bundle. Pierce is flat (707 /
   631, and they lock each other); non-pierce hits get my live multipliers and his DR.
3. **Strip.** If he has 2+ positive tags live (DR, absorb, reflect, damage buffs), Clear is up and he has no
   clear-prevent -> Clear (60) + a 40 setup (Overflow or Thunder). Never Clear into Dr. Kim's.
4. **Cash in.** If my damage buffs are live this turn (cast last turn), or his +taken debuffs are -> my two biggest
   non-pierce hits that fit the AP.
5. **Smoked.** If my -70% given is live -> setup only: Overflow + Dr. Kim's/Jewel + Panacea.
6. **Stunned (80 AP)** -> 60+20 or 40+40 or 40+20+20.
7. **Into DR without Clear** -> R4 (pierce + setup).
8. **Otherwise: set up.** R1 T1 (Overflow + Thunder + Dr. Kim's), or R2 T1 if he still holds Clear and acts like a
   Clear-first player.

Always: spend all usable AP; check own cooldowns, shared locks (pierce 3, prevent 4, stun 4, seal 3) and range 4;
check `do_not_attack.md`; never flee.

## 5. Gaps in this loadout (for the director)
- **No stun.** Every top player opens with one (Eternity Flux, Chakra Resonance, Stunning Jab are owned).
- **No owned cleanse besides basic Cleanse** (Cauterize is owned).
- **No wound/afterburn finisher** (Dragon King's Impact is owned).

Swapping Subaku Palace or Parry for a stun would add a round-1 AP denial. The director's call.
