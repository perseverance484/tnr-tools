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
- **Immediate (same action):**
  - instant damage and pierce (rounds 0), instant heals;
  - Clear and Cleanse;
  - shields (their HP absorbs at once);
  - stun AP loss (no timing gate; a stun lands on the enemy's turn the same round if they act after you);
  - seal roll, flee roll;
  - clearprevent and cleanseprevent (checked without an age test).
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
| Dr. Kim's Potion | 20 | 10 | 100% clear-prevent (works at once) + 100% debuff-prevent (vs debuffs from next round), 1 round |
| Night's Testament | 40 | 6 | pierce power 50 + 2 rounds of buff-prevent immunity |
| Ikazuchi Kunai | 20 | 4 | damage power 22 |

- Ground effects (Phantom Step's DR, Subaku Palace) only apply to whoever stands on that hex, each round.

## 8. How to play with these rules
1. **Setup turn, then payoff turn.** Apply buffs and debuffs on turn N; hit on turn N+1 while they are live (most
   last N+1 and N+2). Never expect a buff to count in the turn you cast it.
2. A good turn deals damage **and** sets up the next one: Ember Blade, whose +35% given/taken sets up next turn,
   plus Chakra Overflow. Next turn, burst into both.
3. Defend a round ahead. Your Defensive Stance or Panacea covers the enemy's *next* turn, not this one.
4. **Smoke means the next round is dead for both sides.** Throw it when their burst is coming, then spend that
   round on setup.
5. Pierce is flat. Don't buff for it. Use it into heavy DR or shields, and finish with it when DR is stacked.
6. Stun is immediate and can't be cleansed. Stunning first when you act first takes 20 AP off their turn this round.
7. Watch shared cooldowns: after Seal, no Dr. Kim's or Lotus for 4 rounds; after Stormblade, no Night's Testament
   for 3.
8. Afterburn and recoil never interact with pierce. Put afterburn on the target and follow with normal damage.

## 9. Corrections to my earlier notes
- "My pierce and kunai showed no reflect back while his reflect was up" (Arashii fight): wrong cause. His reflect
  was cast that round, so it wasn't active yet. Pierce *can* be reflected.
- "Smoke's area reached me at 3 tiles": wrong cause. The smoke always hits every fighter (method ALL), including
  the thrower.
- "Ethereal Rebirth + Chakra Overflow same turn" and "Clear + immediately burst with the buff": buffs didn't apply to
  that turn's damage.
