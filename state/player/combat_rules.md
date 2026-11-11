# TNR combat rules, read from the engine

Source: TheNinja-RPG engine snapshot `cb755375` (pinned 2026-11-05):
- `app/src/libs/combat/process.ts`, `tags.ts`, `util.ts`, `actions.ts`;
- `app/drizzle/constants.ts`.

Shared cooldowns come from the live `misc.getSharedCooldowns` (2026-11-10). Live item and jutsu numbers come from
`item.get` and `jutsu.get`. Re-check after balance patches.

## 1. Rounds and turns
- Turn order is fixed at battle start (initiative). Each round, every fighter takes one turn in that order. AP refills to
  100 when the round changes.
- A turn ends when the 60-second timer runs out, or when the actor has no affordable action left. Leftover AP is lost.

## 2. When effects take effect (the rule I kept breaking)
- **A tag with a duration cast in round N is active from round N+1.** Durations only count down at round changes
  after round N. "2 rounds" means rounds N+1 and N+2 (`calcEffectRoundInfo`, `alignBattle`; the tag handlers check
  `!effect.isNew && !effect.castThisRound`).
- **Applies to:**
  - increase/decrease damage given and taken;
  - absorb, reflect, parry, lifesteal, recoil, afterburn;
  - wound ticks, multi-round heals, residual damage.
- **Consequences:**
  - A buff or debuff never changes the damage of the action that applied it, or of anything else either side does
    in the same round. Chakra Overflow then Ember Blade in one turn: Overflow adds nothing to Ember. Ember's own
    +35% given and +35% taken only boost the following rounds.
  - Defensive buffs (Defensive Stance, Panacea, Chakra Shield's absorb, Smoke's DR, Phantom Step's ground DR)
    protect from next round. If you act first in a round, they do not cover the enemy's turn later that round.
- **Instant (works from the action that casts it):**
  - instant damage and pierce (rounds 0) and instant heals;
  - Clear, Cleanse, shields (their HP absorbs at once), moves and teleports, flee;
  - **bloodline seal** (`isActiveSeal` only needs `!isNew`; director confirmed);
  - **ground effects**: Phantom Step's DR hex, Subaku Palace's zone, Fury's recoil ground. Each round they become
    user tags on whoever stands on the hex, backdated one round so they work at once.
  - **Potency** (`increasepotency`, "+N power points on subsequent jutsu", recently added) boosts every later
    *jutsu* tag in the same turn, pierce included. It does not touch items.
- **Next round (the round after the cast):**
  - all damage given/taken buffs and debuffs, absorb, reflect, parry, lifesteal, recoil, afterburn, wound ticks;
  - **every prevent** (clearprevent, cleanseprevent, buffprevent, debuffprevent, stunprevent, healprevent): Dr.
    Kim's and Seal of Nullification's blocks;
  - **stun**: AP loss is read through `getActiveTargetEffects`, which skips tags cast this round.
- **Age-gated prevents:** buffprevent, debuffprevent, healprevent and stunprevent only block tags created in a later
  round than the prevent. Their power is a % chance.

## 3. Damage
- **Base:** (HP at attacker level / 10) x (jutsu power / 40) x advantage.
  - Advantage compares sqrt(offence) + 2 x sum of sqrt(matching generals) against the defender's.
  - It is curve 1.6 and amplitude 0.75, clamped 0.01 to 10.
- **Boosts:** every active increase (given on the attacker, taken on the defender) multiplies separately:
  x(1 + p) each, so they stack multiplicatively.
- **Reduction:** a system 50% DR, then gear DR, then each in-battle DR multiplies x(1 - p) in turn. Damage never
  drops below 10% of the boosted damage after system DR (90% cap).
- **Late stages:** after that come flat increases/reductions, keystone, then bloodline modifiers. Bloodline
  modifiers are off while your bloodline is sealed (Danse Macabre).
- **Element-scoped modifiers** ("[Fire, Lightning, None...]") only touch damage of a listed element. Damage with
  no element counts as "None".
- **Pierce skips the whole modifier pipeline:**
  - no boosts and no DR; it is fixed damage;
  - it destroys shields instead of being absorbed;
  - it never triggers afterburn or recoil;
  - it can be reflected and lifestolen.
- **Shields** absorb normal damage immediately. Pierce, reflect and wound bypass them.

## 4. Damage-derived tags (active from the round after cast)
- **Afterburn** (on the target): the target takes p% of each non-pierce hit again. It stacks across sources, capped
  at 60% of the hit.
- **Recoil** (on the target): the target's own non-pierce outgoing damage hurts them by p%. Pierce avoids it.
- **Reflect** (buff): returns p% of incoming damage, pierce included, to the attacker, capped at 60% of the hit.
- **Lifesteal** (buff): heals p% of your outgoing damage. Vamp and lifesteal share a 60% cap.
- **Absorb** (buff): turns p% of incoming damage into HP. **Parry** returns part of incoming damage.
- **Wound:** remembers the damage of the hit that applied it, then deals p% of that on each of the target's
  later turns.

## 5. Clear, Cleanse, prevents
- Clear and Cleanse remove everything positive or negative on the target right now, including ground effects on
  their tile. Tags applied later in the same round survive.
- Stun is not "negative": **Cleanse cannot remove it, and debuff-prevent does not block it.**
- Basic Clear and Cleanse: 60 AP, range 4, cooldown 10.
- Immunity tags block a named prevent type from being applied.

## 6. Shared cooldowns (live)
Using any action with tag T locks every other action carrying T for N rounds:

| Rounds | Tags |
|---|---|
| 4 | stun, buffprevent, debuffprevent |
| 3 | pierce, clear, cleanse, clearprevent, cleanseprevent, seal, moveprevent, increasepotency, drain, poison, vamp, consume, siphon, barrier, summon, increasepoolcost |

Each tag locks only actions carrying that exact tag type: Clear (tag `clear`) and Cleanse (tag `cleanse`) do NOT
lock each other (both usable in the same fight two rounds apart; Aurora_Dusk 2026-11-10 R2 Cleanse, R4 Clear).
The lock only fires when the used action has its own cooldown > 0 (engine `applyActionCooldowns`, pin 107d7a868).

In this account's kit:
- Stormblade Arc and Night's Testament lock each other (pierce, 3).
- Seal of Nullification, Dr. Kim's Potion and Lotus Dance lock each other (buff/debuff-prevent, 4).
- Danse Macabre locks other seals (3).

## 7. Exact basics and items
| Action | AP | Cooldown | Effect |
|---|---|---|---|
| Move | 10 | 0 | 1 hex |
| Replacement | 20 | 2 | teleport up to 5 hexes |
| Basic Attack | 20 | short | power 10, range 1 |
| Offensive Stance | 20 | 1 | +15% damage given, next round only |
| Defensive Stance | 20 | 1 | -15% damage taken, next round only |
| Meditate | 20 | 4 | +300 CP/SP |
| Basic Heal | 60 | 5 | flat heal (Arashii: +600) |
| Clear / Cleanse | 60 | 10 | see section 5 |
| Flee | 100 | 0 | 20% chance. **Banned by the director.** |
| Elite Smoke Bomb | 20 | 10 | method ALL. -70% damage given for 1 round to **everyone, you included**; you get -25% damage taken for 2 rounds. Active next round. **One per fight.** |
| Dr. Kim's Potion | 20 | 10 | 100% clear-prevent + 100% debuff-prevent, live the round after use, for 1 round |
| Night's Testament | 40 | 6 | pierce power 50 + 2 rounds of buff-prevent immunity |
| Ikazuchi Kunai | 20 | 4 | damage power 22 |

- Ground effects (Phantom Step's DR, Subaku Palace) only apply to whoever stands on that hex, each round.

## 7b. Player 1 vs player 2: turn order makes every tag asymmetric
Turn order is fixed for the whole battle. **P1** acts first in every round; **P2** acts second. Every tag with a
duration cast in round N switches on at the round change into N+1. That includes buffs, debuffs, prevents, stun,
absorb, reflect, lifesteal, afterburn and recoil. These resolve at once: shields, Clear, Cleanse, instant damage,
pierce and heals, bloodline seal, ground effects and potency.

### The timeline
```
round N:    P1 turn  ->  P2 turn      | round change: tags cast in N switch on
round N+1:  P1 turn  ->  P2 turn      | round change: 1-round tags from N switch off
round N+2:  P1 turn  ->  P2 turn      | round change: 2-round tags from N switch off
```
- **P1's tags from round N** sit dormant through P2's round-N turn, the reply that comes right after them. They are
  live for P1 N+1, P2 N+1, P1 N+2, P2 N+2.
- **P2's tags from round N** are live from the very next turn: P1 N+1, P2 N+1, P1 N+2, P2 N+2.
- Both seats get the same number of live turns from a 2-round tag. **The difference is the gap:** P1 always gives the
  enemy one free reply (P2's round-N turn) before anything P1 cast that round works. P2's tags answer the enemy's
  very next move.

**P1 must predict. P2 can react.**

### Tag by tag (this kit)
| Tag / action | If I am P1 (cast in round N) | If I am P2 (cast in round N) |
|---|---|---|
| Self damage buff (Overflow, Ember-self, Thunder, Parry, Eclipse, Phantom, Pill, Jewel, Off. Stance) | live on my N+1 (and N+2) turns. **The enemy's N turn can Clear it before it is ever live** | live on my N+1 (and N+2). The enemy's N+1 turn comes first and can Clear it unless Dr. Kim's from N is live |
| Debuff on enemy (Ember +taken, Aetherion +taken, Shrapnel afterburn, Fury recoil) | dormant during his N turn (he can Cleanse it); live on my N+1 payoff | live on his N+1 turn (he can Cleanse it then), then on my N+1 payoff |
| My DR (Def. Stance, Panacea, Jewel, Smoke DR, Phantom ground) | does **not** cover his round-N turn; covers his N+1 (and N+2) | covers his very next turn (N+1), and N+2 |
| Chakra Shield (500 HP) | **instant**: covers his round-N turn | instant too |
| Ground effects (Phantom Step DR hex, Subaku Palace zone, Fury recoil ground) | **instant** for whoever stands on the hex: Phantom's DR covers his round-N turn if I stay on it; Subaku cuts his damage at once if he stands in the zone | instant |
| Bloodline seal (Danse Macabre) | **instant**: his bloodline tags are off on his round-N turn | instant |
| Potency (+tag power) | instant for my later jutsu this turn (pierce included) | instant |
| Stun on enemy | dormant during his N turn; costs him AP on N+1 and N+2 | costs him AP on his very next turn (N+1) and N+2 |
| Seal of Nullification: buff-prevent on him (1r) | live N+1 only: blocks buffs he casts on his N+1 turn. **His N-turn rebuff right after my Seal still lands** | live N+1: blocks his very next turn's buffs |
| Seal: debuff-prevent on me (2r, age-gated) | blocks debuffs he casts in N+1 and N+2; his round-N debuffs (same round as my Seal) still land | blocks his N+1 and N+2 debuffs, his next two turns |
| Dr. Kim's (clear + debuff prevent, 1r) | live N+1: protects what I cast in N+1 during his N+1 turn. Doesn't protect round-N buffs during his N turn | live N+1: protects what I cast in N (and N+1) during his N+1 turn, the turn before my cash-out |
| Elite Smoke Bomb (-70% given for everyone, 1r) | live N+1: smokes his N+1 turn **and my N+1 turn**. His N turn right after the throw is **not** smoked. Throw a round ahead of his burst | live N+1: smokes his very next turn (and my N+1). Thrown the turn I see his setup, it blunts his cash-out |
| Clear / Cleanse (instant) | strips what's live or dormant on him now. He can rebuff on his N turn, and that rebuff goes live N+1 for his N+1 turn | strips his fresh round-N buffs before they ever go live. His rebuff in N+1 isn't live until N+2. With Seal (P2) the rebuff is blocked outright |
| Reflect, absorb, lifesteal on me | dormant during his N turn | live on his very next turn |

### Standard lines by seat
**P1 ("Kim's, then buff, then cash out"; director):**
- R1: Dr. Kim's (20) + positioning or damage that doesn't need protecting (Phantom Step 40, Aetherion 40, or Shrapnel 60).
  Kim's goes live R2.
- R2: the big buffs (Overflow 40 + Thunder or Eclipse 40, or Ember 60 + Overflow 40). His R2 turn can't Clear or debuff
  them, because Kim's is live.
- R3: cash out. Everything from R2 is live; R1's 2-round buffs too if cast with Phantom.
- **P1 free ramp:** if he's AFK or not a Clear-holder, ramp R1 *and* R2 (2-round buffs stack across both) and cash out
  R3 at about x5-6 (vs Luminous: Fury 4,042).
- P1 defence must be cast a round early, except the instant ones: Chakra Shield's 500 HP, standing on Phantom Step's
  DR hex, and Danse Macabre's bloodline seal all cover his immediate reply.
- P1 stun or Seal opener: they bite on his R2 turn, not R1. Use them in R1 only to deny his R2.

**P2 ("protect the cash-out as you set it up"; director):**
- R1 (after seeing his R1):
  - If he buffed: Clear + Seal (vs Thronaris). His buffs die before going live, his R2 rebuff is blocked, and my
    debuff-block covers his R2-R3.
  - If he didn't: Dr. Kim's + Overflow + Thunder or Eclipse. All live for his R2 turn, which can't Clear them.
- R2: cash out (Ember + Aetherion, or Ethereal + items) with R1's buffs live.
- R3: second cash-out with R2's Ember and Aetherion debuffs live.
- P2 defence is reactive: when his log shows setup, Smoke, Panacea or Def. Stance in my turn cover his very next
  (burst) turn.

### Reading the enemy by seat
- **I am P2:** what he cast this round is dormant until the round change. I see it in the log before my turn, and I can
  Clear it before it ever goes live, or prepare a counter (Smoke, DR) that is live for his next turn.
- **I am P1:** what he cast in his last turn (the previous round) is already live at the start of my turn. Clear strips
  it before his turn uses it, but he gets to rebuff right after me.

## 8. How to play with these rules
1. **Setup turn, then payoff turn.** Apply buffs and debuffs on turn N; hit on turn N+1 while they are live (most
   last N+1 and N+2). Never expect a buff to count in the turn you cast it.
2. A good turn deals damage **and** sets up the next one: Ember Blade, whose +35% given/taken sets up next turn,
   plus Chakra Overflow. Next turn, burst into both.
3. Defend a round ahead. Your Defensive Stance or Panacea covers the enemy's *next* turn, not this one.
4. **Smoke means the next round is dead for both sides.** Throw it when their burst is coming, then spend that
   round on setup.
5. Know your seat (section 7b) before planning anything: P1 predicts, P2 reacts.
6. Pierce is flat. Don't buff for it (potency is the one exception: it raises pierce power). Use it into heavy DR or
   shields.
7. Stun can't be cleansed; it bites from the round after it is cast.
8. Watch shared cooldowns: after Seal, no Dr. Kim's or Lotus for 4 rounds; after Stormblade, no Night's Testament
   for 3.
9. Afterburn and recoil never interact with pierce. Put afterburn on the target and follow with normal damage.

## 9. Corrections to my earlier notes
- "My pierce and kunai showed no reflect back while his reflect was up" (Arashii fight): wrong cause. His reflect
  was cast that round, so it wasn't active yet. Pierce *can* be reflected.
- "Smoke's area reached me at 3 tiles": wrong cause. The smoke always hits every fighter (method ALL), including
  the thrower.
- "Ethereal Rebirth + Chakra Overflow same turn" and "Clear + immediately burst with the buff": buffs didn't apply to
  that turn's damage.

## Summons (Korin's Jade, 2026-11-11)
- A summon acts in its owner's turn on its own cooldowns: Jade pierced my shield in R5 two rounds after Korin's own
  Night's Testament, so the owner's 3-round pierce lock does not cover summons.
- No death message exists in the log; a live summon is listed in battle usersState. Our Fury (AoE) one-shot Jade
  for 2646, so an AoE turn removes the summon threat.
