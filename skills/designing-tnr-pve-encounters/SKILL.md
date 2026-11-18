---
name: designing-tnr-pve-encounters
description: Designs PvE fights for The Ninja RPG (TNR) - dungeon floors and waves, bosses, mini-bosses, hunt and quest fights, dailies - so they are readable, fair and fun for every build, solo or in a party, within what the AI priority-list engine can actually do. Use this skill whenever the user asks for a new enemy, boss, wave, floor, dungeon, hunt fight or PvE encounter, asks why players lose to or dislike a fight, wants a fight tuned, harder or easier, or mentions telegraphs, marks, eruptions, safe tiles, stun, seal, one-hit KO, enrage, phases or win rates, even if they don't say "encounter design". It decides the fight's shape and budgets; designing-tnr-content turns it into a design sheet and building-tnr-content into records.
---

# Designing TNR PvE encounters

A fight is good when the player can see what is coming, has something to do about it on their next turn, and
loses only because of choices they can name. Hard is welcome; arbitrary is not. This skill decides the fight's
shape, its budgets and its AI loop, then hands off. It never writes a manifest and never touches the live game.

Director's standing rules, which every encounter follows:
- Fun first. Make the readable version before the hard one.
- Losing ends a run. A wipe in a dungeon sends the party back to the tier's first floor, so a fight's cost is
  every floor before it.
- Fleeing is not intuitive gameplay. Never design a fight whose answer is to flee.
- Boss attacks are telegraphed, every time, with consistent damage.

Full research and evidence: the Claude Doc "TNR PvE Encounter Design Research" (2026-11-18). Engine facts below
were true at that date; re-read the live shared-cooldown table and the current game pin before tuning.

## 1. What the engine is (design around this, never against it)

- **The AI is a priority list, not a script.** Up to 20 rules, read top to bottom on every action; the first
  rule whose conditions pass and whose action can run fires. A rule that can't run (cooldown, AP, range) is
  skipped silently. There is no memory, counter, "last action" or NOT. State lives only in effects the AI puts
  on itself (markers).
- **Conditions:** round below/above/exact, distance below/above (A* path length, gate = range + 1, range cap 5),
  own HP below %, has effect, target has effect, no summon out.
- **Targets:** self, closest or random opponent, closest or random ally, barrier and empty-ground placements.
  No lowest-HP, healer or marked-player targeting.
- **Turns:** 100 AP per combatant per turn. Duration tags (buffs, debuffs, prevents, stun, DR) switch on the
  round after cast. Damage, heals, pierce, shields, Clear, Cleanse and ground effects are instant. A mark cast on
  the boss's turn pays off on its next turn, so the player gets exactly one turn to answer.
- **Shared cooldowns are per combatant** and live, staff-editable data (`misc.getSharedCooldowns`). Nov 2026:
  stun, buffprevent, debuffprevent 4 rounds; pierce, clear, cleanse, seal, moveprevent, drain, poison, vamp,
  summon, barrier and others 3 (drain read 4 live in the Isonade tests, so trust the live table over this list).
  Three enemies can still chain one player.
- **A stunned boss can't pay for a 100 AP set piece** and idles. Bosses that run set pieces must be stun-immune.
- **Readability limits:** the AI's whole turn shows as one snapshot; decrease tags on characters are invisible;
  no floating numbers; HP bars only on hover; the killing blow isn't animated. The battle log
  (`battleDescription`) is the only voice channel.
- **Dungeons:** parties of 3 (solo may bring 2 pets, which don't count as party members); 1-4 tiers of 5 floors;
  up to 5 sequential waves of 10 AIs per floor; party healed after each floor; a wipe on a mini-boss floor
  retries that floor, a wipe anywhere else returns to the tier's first floor; enemies don't scale to the party;
  one-hour run; 3 idle rounds end it. A lapsed 60-second turn is played by the server AI.
- **Players' answers:** move (10 AP a hex), Replacement (20 AP, 5 hexes, not while rooted), shields, heals,
  Clear and Cleanse (60 AP, range 4, 10-round cooldown). Cleanse can't remove stun.

## 2. The twelve rules

1. **Hurt, don't delete.** No move kills from full HP. A telegraphed big hit takes 30-50% of its target's HP.
   No one-hit KO and no random KO roll in a dungeon or daily. If a fight must have a lethal move (a set-piece
   finale the director has asked to be brutal), it is warned twice and can't combine with any movement effect.
2. **Every telegraph has an instant answer:** step out, Replacement, a shield, a heal, or killing the source.
   A DR buff is a bonus, never the only answer, because it switches on a round late.
3. **Dodge out, not dodge in.** A hazard covers a third of the reachable board or less. Shapes are boss-centred
   or fixed to the board and never chase. No pull, push or root onto a pending mark.
4. **Budget control for the whole wave.** At most one hard control (stun or seal) per wave, 1 round of stun,
   never stun and seal on one player in the same turn, low or no damage on the control move. Seal comes from a
   source the player can kill or step away from. Solo budgets are half the party's.
5. **Never switch off the player's tools.** Boss buffs are clearable. No clearprevent on a boss that stacks
   DR. No heal-block in dungeons. Reflect or recoil only on a visible stance with a log line, never below 20% HP.
6. **Every build gets a window.** After each big hit, a 1-round weakness window (weakness on SELF) for all
   damage generals. Damage-type weaknesses may add a bonus for one build, never a gate. Stun builds get adds or
   summons worth controlling.
7. **A loop, not a timeline.** "If marked, pay off; if paid off, open; otherwise mark." Design reads as a
   timeline, but the AI is a stateless priority list, so aim for one beat per round and let markers carry the
   state. Never depend on round numbers or HP thresholds firing in order.
8. **Readable before hard.** One new idea per floor, introduced alone, then combined with at most one other.
   One tile language (heavy, control, linger, safe), one log line per big move, the same mark always means the
   same payoff.
9. **Short fights, kind finales.** Trash waves 2-4 rounds; bosses about 12-15. In a one-tier dungeon the final
   boss is the most readable fight. In a multi-tier dungeon the hardest check goes on a mini-boss floor.
10. **Solo is its own fight.** If solo entry is possible, every wave must be beatable by one player at the band's
    floor level with its usual gear. Pets add nothing to the budget.
11. **Pressure a habit, never ban a build.** Punish buff-stacking, standing still or turtling with a visible
    tell; every build still has a way to win.
12. **Tune with counts, not cruelty.** Raise difficulty with enemy count (one at a time), HP and capped damage.
    Never by adding lockdown, removing warning, or turning a hit into a KO.

## 3. Archetypes (pick one or two per boss, mix across floors)

| Archetype | Loop | Answer | Status |
| --- | --- | --- | --- |
| Windup Brute | If marked: capped heavy hit on closest opponent, then 1-round weakness window on self. Else: mark + basic attack. | Shield, heal, sturdier ally steps in; everyone hits the window. | Proven |
| Sweeper | If marked: fixed shape around itself, alternating sides each cycle. Else: mark the next shape. Rooted. | Step out; alternation is learnable. | Proven (Mender) |
| Warden and Ward | Boss keeps a summoned Ward that buffs it. If no summon: 2-round weakness window, skip big move; re-summon after the summon lock. | Any damage kills the Ward; stun builds lock it. | Probe |
| Source Hunt | A support add heals, shields or carries the wave's one seal. | Kill the source first. Solo: low HP, in reach. | Proven (teams) |
| Pack | 2-3 enemies, one verb each, no hard control, basic attack last. | Ordinary play, 2-4 rounds. | Proven |
| Visible Clock | Signature move adds a stacking, visible, clearable +damage buff. | Kill fast or Clear once. | Proven (Glass Lancet) |
| Habit Breaker | If target carries a big buff: mark, then a strip next turn. If adjacent: mark a knockback ring. | Play around the tell. | Probe |
| Phase Boss | Up to 3 phases by health_below + phase marker; each phase is one loop above; change prints a line and opens a window. | Read the new loop; first cycle is light. | Proven pieces |

"Probe" archetypes must pass the combat sim before they go into a design sheet as settled.

## 4. Workflow

1. **Frame the fight.** Write down: band and level range, solo or party or both, where it sits (trash wave,
   mid-floor, mini-boss, final boss, daily, hunt), the one new idea it teaches, and the target (for a boss: an
   average player wins most attempts and ends near 30-50% HP; for trash: no wipes).
2. **Pick archetypes** from §3. A floor gets one idea; a boss one or two loops; a finale reuses ideas the dungeon
   already taught.
3. **Fill the budget sheet** (below). Any line over budget is redesigned, not argued.
4. **Write the AI loop** in plain words, top rule first, then map each line to a rule:
   - top: payoff of a pending mark (`has_effect <marker>`);
   - next: open the window after a payoff;
   - next: start a new mark;
   - then: ordinary actions with correct distance gates and a move fallback;
   - last: the named basic attack. No `use_highest_power_*`, `use_random_jutsu` or `use_combo_action` damage rules.
   Markers use tags outside the shared-cooldown list (the Skyglass library uses increasecooldown with no actions,
   or increaserange). Aim for 12 rules or fewer.
5. **Walk three players through it on paper:** a melee taijutsu player with no stun-prevent, a ranged ninjutsu
   or genjutsu caster, and a support or tank build. For each: what does a telegraph cost them, what is their
   instant answer, where is their window? If any of them has no answer or no window, redesign.
6. **Check the solo case** if solo entry is possible: one player, every control move aimed at them.
7. **Hand off.** designing-tnr-content writes the design sheet and takes it to the director's "freeze it";
   nothing is built before that. Then tune with the combat sim, which loads the live shared-cooldown table,
   solo and in a party, at the current game pin. building-tnr-content compiles records after the numbers sit
   inside target. Where dauntless can't play the band (it is level 100, so genin and 30-80 content can't be
   hand tested), the sim is the only check: say so in the hand-off. Live writes go through
   shipping-tnr-content, with the director's go for that job.

## 5. Budget sheet (copy per encounter)

```
Encounter:             Band / levels:            Solo / party / both:
Position:              New idea taught:           Target result:
Biggest hit:           ___% of target HP (max 50; no KO)        Instant answer:
Hazard coverage:       ___ of reachable hexes (max 1/3)          Chases? no
Hard control:          ___ per wave (max 1; solo max 1 per 2 waves)   Stun rounds: ___ (max 1)
Stun + seal same turn: no        Seal source killable / avoidable: yes
Player tools blocked:  none (Clear works, heals work, no hidden reflect/recoil)
Window after big hit:  ___ rounds, generals covered: all
Rounds (median):       trash 2-4 / boss 12-15
Boss stun-immune (if it runs 100 AP set pieces): yes
Rules: ___ (aim <= 12)   Last rule: basic attack   Random/highest-power damage rules: none
Markers outside shared-cooldown list: yes   Live cooldown table read on: ____
Three-build walk-through done: melee / caster / support
```

## 6. Review rubric (use on existing fights too)

Score each yes/no; any "no" in the first five is a redesign, not a tune.

1. Can a player at full HP survive any single enemy action?
2. Does every lethal-tier move have a telegraph and an instant answer?
3. Can every build in the walk-through act on most of its turns (not stunned, not sealed, not forced to walk)?
4. Does the AI loop still work if any one action is skipped (cooldown, stun, missed gate)?
5. Can the player see why they died (mark on screen, log line, no hidden reflect)?
6. Does every build get a damage window?
7. Is the fight inside its round target?
8. Does it teach or reuse an idea, rather than add a third new one?

When reviewing a live fight, use win/loss data per build and per solo/party where it exists, and say which
answers are inferred.

## 7. Hard nos

- One-hit KO or KO chance on a warned attack in a dungeon, daily or hunt.
- "Whole board except safe tiles" patterns.
- Stun longer than 1 round; stun and seal together; chained control across a wave.
- Pull, push or root into a pending mark.
- Timeline fights driven by round numbers or HP thresholds firing in order.
- Unclearable boss DR, heal-block, hidden reflect or recoil.
- Lowering a high-band kit for a low band instead of designing the low band first.
- Any change or request to the game's own code. Work within the engine as it is.
- Any live write, live fight or record change from this skill. It designs; others build, and the director says go.
