# Stage 4: Fight design (bosses)

A boss fight is designed as a performance first and a record second. This stage fills the
`boss` block: bible, acts, script, telegraphs, anti-camping, enrage.

## Template

```
Character bible:  <who they are, what they want, how their power looks and sounds>
Act <n>: <title>
  Script:      <round or phase> -> <what the boss does, and what the player should read>
  Telegraphs:  <omen> -> <payoff>, <rounds between>
Anti-camping:  <what happens to a player who will not move or will not approach>
Enrage:        <when the fight ends itself; AWAITING_RULING until the director sets it>
```

The shipped example of a bible is `docs/design/SAYO_BIBLE.md`; of a fight script,
`docs/design/MOTHER_OF_ECHOES_FIGHT_SCRIPT.md`. That fight's art language is its own
(RUL-2026-11-09-141 item 5): borrow from it, do not treat it as the rule for every boss.

## Exit checklist

Each line cites the rule it checks; read the owner, not this summary.

- [ ] Every dangerous move has an omen the round before, and the mark resolves on the following
      turn (RUL-2026-10-28-028 item 6).
- [ ] No set piece can be cast without its mark (the fallback rule, RUL-2026-10-29-046).
- [ ] Telegraph art will ride a carrier that survives the round (RUL-2026-11-02-101).
- [ ] Every phase change has a one-line battle cue.
- [ ] No lingering hazard is placed on the hex the target stands on without a warning first.
- [ ] The rule count fits the engine's cap (`AI_PROFILE_MAX_RULES` in the build skill's
      `data/45e_DATA_constants.json`), counted per phase list.
- [ ] Each round, a player can tell which hexes are dangerous next, where everyone is, and
      what state the boss is in.
- [ ] A player who camps and a player who ignores the mechanics both have an answer written
      down.

## Decision for the director

The fight script, read as a story: "is this the fight?" Clear-rate targets and the enrage
timing are separate cards at stage 5.
