# PvP rotations: the director's PvP loadout (v2, 2026-11-10: deck model, seat-aware combos)

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
| Eight Fist: Lotus Dance | 7 | dmg 45 | target buffprevent 100% (1r) | buffprevent 4 (locks Seal, Dr. Kim's) |
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
| Dr. Kim's Potion | 20 | 10 | clearprevent + debuffprevent 100%, live the round **after** it is drunk (1r) | debuff/clearprevent 4 (locks Seal, Lotus) |

**Basics:** Offensive Stance +15% given / Defensive Stance -15% taken (20, next round only); Clear / Cleanse (60, CD 10);
Replacement (20, CD 2, range 5); Move (10); Basic Attack (20, range 1); Basic Heal (60, CD 5); Meditate (20).
**Never Flee.**

**Multipliers stack multiplicatively.** Fully set up: Overflow x1.82, Ember x1.35, one 30% buff x1.3, Pill or Jewel
x1.15 on me, and Ember x1.35 and Aetherion x1.2 on the target. Together that is about **x6 on non-pierce hits.** That
is the whole game: set up, then cash in. Pierce ignores all of it.

## 2. What the cooldowns really mean (read this first)

Every equipped PvP jutsu has a **7-round cooldown** except Phantom Step (6), Ethereal Rebirth (8) and Danse Macabre
(8). PvP fights last 3-8 rounds, so **each jutsu is effectively one shot per fight.** The loadout is a deck of
15 cards, not a rotation:

- **7 hits (60 AP):** Ethereal 45, Shrapnel 45, Lotus 45, Fury 45, Ember 40, Danse 33, Stormblade pierce 56.
- **8 utilities (40 AP):** Overflow, Thunder's, Parry, Eclipse, Phantom, Subaku, Seal, Chakra Shield.
- A full turn is one hit + one utility (60 + 40), so 7 turns use the whole deck. Plan the *order*, not a loop.

**Once per fight (cooldown 10):** Clear, Cleanse, Elite Smoke Bomb, Dr. Kim's. The same is true for the enemy.
**Twice per fight:** Kunai and Chakra Pill (cooldown 4). Aetherion, Night's Testament, Panacea, Jewel: cooldown 6.

**Shared locks that cut the deck further:**
- **Prevent family (4 rounds):** Seal of Nullification, Lotus Dance, Dr. Kim's. Using one locks the other two
  for 4 rounds. In practice you get **one of the three** per fight window. Pick deliberately (section 6).
- **Pierce family (3 rounds):** Stormblade and Night's Testament can't go back to back.
- "Action not valid anymore" = own cooldown. "No longer possible" = range (target moved) or AP (stun).

## 3. Damage estimator

Calibrated from logs: **one point of jutsu power is worth about 15 damage unbuffed** against a level-100 target
with ordinary defence (Fury 45 hit 4,042 at about x5.6, so ~16; Ember 40 hit 598 at x1.0, so ~15). Heavy DR lowers this to about
11-12 (Ethereal 533 into IndraUchiha).

Multipliers stack multiplicatively; each one is x(1 + p):

| Source | On | x | Lives |
|---|---|---|---|
| Chakra Overflow | me | 1.82 (two +35%) | 2 rounds after cast |
| Ember Blade (given) | me | 1.35 | 2 rounds |
| Ember Blade (taken) | him | 1.35 | 2 rounds |
| Thunder's / Parry / Eclipse / Phantom / Subaku | me | 1.30 each | 2 rounds |
| Shrapnel afterburn | him | 1.30 (non-pierce hits) | 2 rounds |
| Aetherion | him | 1.20 | 2 rounds |
| Chakra Pill / Colored Jewel | me | 1.15 | 2 / 3 rounds |
| Offensive Stance | me | 1.15 | next round only |
| Ethereal Rebirth self-debuff | me | **0.85** | 2 rounds |

Quick table (one power-45 hit, ordinary defence):

| Live stack | x | Power-45 hit |
|---|---|---|
| nothing | 1.0 | ~680 |
| one 30% buff | 1.3 | ~880 |
| Overflow | 1.82 | ~1,230 |
| Overflow + one 30% | 2.37 | ~1,600 |
| Overflow + 30% + Pill | 2.72 | ~1,840 |
| Overflow + 30% + Ember (both sides) | 4.32 | ~2,920 |
| Overflow + 30% + Pill + Ember + Eclipse | **6.46** | **~4,360** |
| same + Aetherion instead of Eclipse | 5.96 | ~4,020 |

Pierce is always flat: Stormblade ~707, Night's Testament ~631. Kunai (22) and Aetherion (30) take the multipliers.

## 4. Seat timing in one table (from combat_rules.md 7b)

| | As **P1** (I act first) | As **P2** (I act second) |
|---|---|---|
| My buff cast round N | dormant during his N reply (he can Clear it); live my N+1 | live my N+1, his reply in N already happened |
| My defence cast round N | covers his **N+1** turn, not his immediate reply | covers his **very next** turn |
| Instant defence that covers his immediate reply | Chakra Shield 500, Phantom DR hex, Subaku zone on him, Fury recoil ground on him, Danse seal | same, but rarely needed |
| Dr. Kim's drunk round N | protects round N+1: his N+1 reply can't Clear what I cast in N and N+1 | protects his N+1 turn: the buffs I drink it with survive to my N+1 cash-out |
| Smoke thrown round N | -70% for everyone in N+1: must be thrown the round **he sets up**, before seeing it | throw it after seeing his round-N setup: it hits his N+1 cash-out (and my N+1 turn) |
| Clear | his round-N buffs are live during my N+1 turn; Clear then, before his N+1 cash | Clear in my round-N turn right after he buffs, before they ever go live |
| Seal | blocks his buffs cast in N+1 (his N reply can still rebuff) | Clear + Seal leaves him buffless for 2 rounds |

**Short version:** P1 predicts and must hide value from his reply; P2 reacts and gets clean answers.

## 5. Track the enemy's once-per-fight buttons

Keep a 4-box tracker each fight, from `combat.getBattleEntries`:

| His button | When it's gone | What it unlocks for me |
|---|---|---|
| Clear | for the rest of the fight | **K1 Triple Stack** (my buffs can't be stripped) |
| Cleanse | for the rest of the fight | stack debuffs on him freely (Ember taken, Aetherion, Shrapnel afterburn) |
| Dr. Kim's | rest of fight; Seal and Lotus also locked 4 rounds for him | my Clear and debuffs land; he can't Seal me |
| Smoke | rest of fight | my cash-out turns can't be blunted |

Mine are the same four. **Never let him bait my Clear onto a cheap setup**: Clear only when he has 2+ live
damage tags or a DR/absorb wall, and never into his live Dr. Kim's.

## 6. Pick one prevent per window: Seal vs Lotus vs Dr. Kim's

| Pick | Does | Best when |
|---|---|---|
| **Seal of Nullification** (40) | his buffs blocked next round; my debuff-block for 2 rounds (also blocks my own Ethereal -15%) | he's a buffer or a debuff-finisher; P2 after a Clear |
| **Lotus Dance** (60, dmg 45) | damage + his buffs blocked next round | you want damage this turn and only need one round of buff denial |
| **Dr. Kim's** (20, item) | my buffs can't be Cleared and I can't be debuffed next round | he still holds Clear and I'm about to stack |

## 7. Combo library (T = my turn; every combo fits the AP and cooldowns)

### K1. Triple Stack (the kill combo): when he can't Clear (spent, or smoked/stunned)
| T | Actions | Live on this turn | Damage |
|---|---|---|---|
| 1 | Overflow (40) + Thunder's (40) + Chakra Pill (20) | — | 0 |
| 2 | Ember Blade (60) + Eclipse Drain (40) | x2.72 | Ember ~1,630 |
| 3 | **Forbidden Chakra Fury (60) + Aetherion (40)** | **x6.46** | ~4,360 + ~2,910 = **~7,270** |
| 4 | Ethereal Rebirth (60) + Phantom/Parry (40) | Ember, Eclipse, Aetherion (~x2.9) | ~2,000 |
About 8,900 damage by T3 from full HP if nothing is stripped: lethal through moderate DR. Swap Eclipse for Phantom
Step on T2 when you also need to close distance.

### K2. Kim's Window, P1 version ("kims, then buff, then cash out")
| T | Actions | Why |
|---|---|---|
| 1 | Shrapnel (60) + **Dr. Kim's** (20) + Kunai (20) | nothing he can Clear on his R1 reply; afterburn on him R2-R3; Kim's live R2 |
| 2 | Overflow (40) + Thunder's (40) + Chakra Pill (20) | his R2 reply **can't Clear** these |
| 3 | Ember Blade (60) + Aetherion (40) | x2.72 x afterburn 1.3 = **x3.5** on both hits (~2,100 + ~1,570) |
| 4 | Fury (60) + Eclipse (40) | x5.96 if he didn't Clear on his R3 reply (~4,000); x1.6 if he did (~1,090) |
If he Clears on his R3 reply, his Clear is gone: move to K1 for the rest of the fight.

### K3. Kim's Window, P2 version ("protect the cash-out when you buff")
| T | Actions | Why |
|---|---|---|
| 1 | Overflow (40) + Thunder's (40) + **Dr. Kim's** (20) | Kim's live R2: his R2 turn can't Clear them |
| 2 | Ember Blade (60) + Aetherion (40) | x2.37 now (~1,420 + ~1,070); sets x1.35 / x1.35 / x1.2 for R3 |
| 3 | Fury (60) + Eclipse (40) | x5.2 if he didn't Clear on his R3 turn (~3,500) |

### L1. Clear-Seal Lock (P2, against a buff opener). Won vs Thronaris
| T | Actions | Why |
|---|---|---|
| 1 | **Clear** (60) + **Seal** (40) | strips his R1 buffs before they go live; blocks his R2 rebuffs; my debuff-block R2-R3 |
| 2 | Ember Blade (60) + Overflow (40) | he is buffless through his R2 turn; my stack goes live R3 |
| 3 | Ethereal (60, its -15% blocked by my ward) + Aetherion (40) | x1.82 x 1.35 x 1.35 = x3.3 (2,234 + 1,245 in the Thronaris log) |
| 4 | Fury (60) + Kunai (20) + Pill (20) | Ember/Aetherion still live |
As **P1** this lock only works from round 2 (Clear his live R1 buffs before his R2 cash-out; Seal blocks his R3
buffs, not his R2 rebuff). Prefer K2 as P1.

### Director coaching (2026-11-09, 22:57)
"If you want to cut damage the best combo is seal subaku especially if going first. If you want to reflect and
mitigate the best is forbidden Chakra Fury and chakra shield, although that can be pierced very effectively. Smoke
bomb is also often countered by pierce. Seal of Nullification debuff prevent can be used to prevent ethereal rebirth
and smoke bombs self debuffs. Subaku Palace applies to enemies."
- **Cut damage: Seal + Subaku (80 AP), best as P1.** Subaku's ground zone on his hex is instant (-25% his damage,
  3 rounds); Seal blocks his buffs next round and wards me 2 rounds. Fill with Def. Stance / Panacea.
- **Reflect and mitigate: Fury on his hex + Chakra Shield.** Pierce beats it (pierce destroys shields and ignores
  recoil), so don't use it into a player holding Stormblade/Night's Testament-style pierce.
- **Smoke is countered by pierce** (pierce ignores the -70%). Don't rely on Smoke against a pierce holder.
- **Seal's debuff-block also blocks my own self-debuffs:** Ethereal's -15% and Smoke's -70% on me. Seal, then next
  turn Smoke + Ethereal: he is smoked, I'm not.
- Subaku Palace's zone applies to enemies (not me).

### D1. Instant Wall (P1's answer to "his burst lands on his reply")
| Actions | Effect on his immediate reply |
|---|---|
| **Fury on his hex** (60) + **Subaku Palace on his hex** (40) | he recoils 40% of every non-pierce hit he lands and deals -25% while he stands there; Fury still hits 45 |
| Chakra Shield (40) + Phantom Step onto a fresh hex (40) + Defensive Stance (20) | 500 HP shield + 20% DR hex now; Def. Stance covers the round after |

Use when his last turn was a setup (2+ damage tags live on him, or +taken stacked on me) and you are P1.
Fury's ground recoil landing on the enemy at once is confirmed in the Old Ghost log. Subaku's split (which side gets
+30% and which gets -25%) is still unverified: check the next log before relying on it.

### D2. Mirror Box (punish a burst that's coming)
| T | Actions | Effect |
|---|---|---|
| a | Stormblade (60, pierce ~707) + Thunder's (40) | reflect 35% + 35% = **60% (cap)** live next round |
| a+1 | Fury on his hex (60) + Parry (40) | adds instant 40% recoil on him: his hits now cost him ~100% of their damage |
P2 casts it after seeing his setup (it covers his next turn). P1 casts it one round earlier than his expected cash-out
(the reflect turns on for his N+1 turn). Weak into heavy lifesteal: Clear his lifesteal first or skip.

### D3. Smoke Pivot (turn his cash-out into my setup round)
| Seat | When | Actions |
|---|---|---|
| P2 | right after his setup turn | Smoke (20) + Overflow (40) + Thunder's (40) |
| P1 | the round you expect him to set up (usually R1 vs buff-first players, or the turn after he Clears) | Smoke (20) + Overflow (40) + Panacea (20) + Def. Stance (20) |
The smoked round is dead for both sides: spend it on 40-AP setup and items only (never a 60 hit). The round after is
my cash-out with his burst wasted.

### P. Pierce rules
- Pierce never benefits from buffs, so **fire it when multipliers are low**: round 1, the turn after his Clear,
  into a DR/shield wall, or as the hit right after Ethereal (my -15% doesn't touch pierce).
- Kill check: HP at or below ~707 -> Stormblade; ~631 -> Night's Testament (not within 3 rounds of each other).
  Add Kunai (~330 x multipliers) for ~1,000 total.

### Ethereal placement
Ethereal puts -15% on my damage for 2 rounds. Make it the **last** non-pierce hit of a burst window, or cast it while
Seal's debuff-block is live, or follow it with pierce. Its 35% absorb (3 rounds) makes it the best hit to land right
before his cash-out turn.

### Danse Macabre
Instant bloodline seal: open with it (or cast it the turn before his cash-out) against bloodline-reliant players.
Cheapest hit (33), so it's the filler 60 when the turn is about the 40.

## 8. Full scripts

### S1. P1 against an unknown opponent (default)
| R | Me (P1) | Watch for |
|---|---|---|
| 1 | Shrapnel + Dr. Kim's + Kunai (K2 T1). Far away: Phantom Step + Shrapnel and drop the items | his R1: buff (-> R2 as planned), Clear (wasted: go K1), stun (R2 is 80 AP) |
| 2 | Overflow + Thunder's + Pill (protected) | his R2: buffs -> plan Clear on R3 if he has 2+ live; Smoke -> R3 is setup only |
| 3 | Ember + Aetherion at ~x3.5 | if his live stack threatens lethal: D1 instead |
| 4 | Fury + Eclipse (~x6) | his Clear used? -> K1 rest of fight |
| 5 | Ethereal + Parry (last big hit, absorb before his reply) | — |
| 6 | Stormblade (pierce, ignores my -15%) + Seal (prevent lock over by R5) | kill check |
| 7 | Lotus + Subaku / Danse + Chakra Shield | anything left |

### S2. P2 against a buff opener
| R | Me (P2) | Watch for |
|---|---|---|
| 1 | Clear + Seal (L1) | — |
| 2 | Ember + Overflow | his R2 attack is unbuffed; Seal blocks his rebuffs |
| 3 | Ethereal + Aetherion (~x3.3) | — |
| 4 | Fury + Thunder's (Ember gone; Thunder's sets R5) | he rebuffs R3 (live R4): if 2+ tags and Clear is down, D2 Mirror Box or Smoke |
| 5 | Stormblade + Eclipse | kill check |

### S3. P2 against a quiet opener or a Clear-holder
| R | Me (P2) | Watch for |
|---|---|---|
| 1 | Overflow + Thunder's + Dr. Kim's (K3) | — |
| 2 | Ember + Aetherion (~x2.4) | — |
| 3 | Fury + Eclipse (x5.2 if not Cleared) | if he Cleared on R3: K1 from R4 (Pill, Parry, Phantom still unused) |
| 4 | Ethereal + Parry | — |
| 5 | Stormblade + Seal | — |

## 9. Turn rule set (top-down; seat-aware)
1. **Survive.** His live stack x his last big hit >= my HP? P2: Cleanse + Smoke + Panacea, or D2. P1: D1 (instant
   only), and Smoke this round if his setup is likely.
2. **Kill.** His HP <= my instant damage this turn (pierce flat; others x live stack) -> fire it.
3. **His Clear is spent and I have 3+ unused buffs** -> K1.
4. **Strip.** 2+ of his damage/DR tags will be live for his next cash-out, my Clear is up, no Dr. Kim's on him -> Clear
   + a 40 setup. (P2: right after he casts. P1: on my next turn, before his.)
5. **Cash in.** My buffs or his +taken are live now -> biggest non-pierce hit + Aetherion/Kunai.
6. **Smoked** -> 40s and items only. **Stunned** (80 AP) -> 60 + 20 or 40 + 40.
7. **DR wall and no Clear** -> pierce + a setup 40.
8. **Otherwise set up by seat:** P1 -> K2. P2 -> L1 if he buffed, else K3.

Always: one prevent (Seal/Lotus/Kim's) per 4 rounds; one pierce per 3 rounds; spend all AP; check range 4 against his
*current* hex; heal the moment the fight ends; never flee.

## 10. Gaps in this loadout (for the director)
- **No stun.** Every top player opens with one (Eternity Flux, Chakra Resonance, Stunning Jab are owned).
- **No owned cleanse besides basic Cleanse** (Cauterize is owned).
- **No wound/afterburn finisher** (Dragon King's Impact is owned).

Swapping Subaku Palace or Parry for a stun would add a round-1 AP denial. The director's call.
