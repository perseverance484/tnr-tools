# Libraries: the building blocks a sheet names

A design sheet never spells out a rule, a stat or a multiplier. It names a **block** from a
library and gives the block its parameters. `design.py check` proves the block exists and its
parameters are in bounds; `design.py compile` turns it into records through the build skill's
own tools.

This page is the map. The entries themselves are data, in `data/libraries/<family>.json`, and
`python3 scripts/library.py list` and `show <id>` print them. Read the entry, not this page,
for what a block takes.

## 1. What a block is

An entry has the same parts in every family:

| Part | What it says |
| --- | --- |
| `summary` | one line: what the block does |
| `params` | each parameter, its type and bounds. A value may be a slot word |
| `builder` | the function in `scripts/library.py` that does the work |
| `laws` | the engine laws the block rests on, by number. The law text lives in `docs/ENGINE_LAWS.md` only |
| `exemplars` | where shipped content or the build skill already does this |
| `failure_modes` | how the block goes wrong, so a reader does not have to find out live |
| `standing` | `engine`, `shipped` or `proposed` (below) |

A block holds **no balance number**. A number is either a parameter, which the sheet supplies
and may leave as `AWAITING_RULING`, or it is read at compile time from its owner (a pool
record's gate, `enemy.py`'s role table, the rule cap in `data/45e_DATA_constants.json`).

### Standing

- `engine`: the block only arranges what its cited laws require.
- `shipped`: the block repeats a shape shipped content already uses.
- `proposed`: the block rests on a value the director has not ratified. `check` and `compile`
  say so every time it is used. A proposed block is usable for drafting; it is not a ruling.

## 2. Families shipped in this build

| Family | A sheet names it at | Builds |
| --- | --- | --- |
| `rule_pattern` | `enemy.rules[].use`, `enemy.phases[].rules[].use` | AI rules |
| `loadout` | `enemy.loadout.recipe` | nothing; it checks the kit |
| `archetype` | `enemy.role` | the role `enemy.py` derives the record from |

The other families the sheet schema allows for (quest structures, setups, payouts, boss
grammar) have not shipped. A reference to one is reported as pending and `compile` refuses.

### Rule patterns

Rules are tried top to bottom and the first that can act wins (law 39), so **the order on the
sheet is the priority**. Compile keeps it.

| Block | Use it for |
| --- | --- |
| `rule_pattern/opener/v1` | a self-target stance used before any attack |
| `rule_pattern/use_jutsu/v1` | one pool jutsu, usually with a `when` |
| `rule_pattern/rotation/v1` | several pool jutsu in priority order |
| `rule_pattern/basic_attack/v1` | the engine's basic attack on an adjacent opponent |
| `rule_pattern/fallback/v1` | the unconditional last rule |

A pattern never takes a distance: the gate comes from the pool record (law 40). A pattern
never takes a jutsu id: it takes a pool code (`D-pool-codes`).

### `when`: conditions on a block or a phase

Any rule block except the fallback, and any phase, may carry `when`:

```json
{ "use": "rule_pattern/use_jutsu/v1", "params": { "jutsu": "S35" }, "when": { "health_below": "AWAITING_RULING" } }
```

| Key | Value |
| --- | --- |
| `health_below`, `round_greater_than`, `round_lower_than`, `specific_round`, `distance_at_least` | a whole number of at least 1, or a slot word |
| `self_has_effect`, `target_has_effect` | an effect type |
| `no_summon` | `true` |

The keys map to the engine's condition vocabulary (laws 39 and 64). A threshold in `when` is a
tuning value: leave it as `AWAITING_RULING` unless a ruling or a recorded design gives it.

### Phases

A phase is a group of rule blocks under one `when`. Compile puts phases above the enemy's
standing rules, last phase first, so the most specific situation is tried first. A phase's
`trigger` is prose for the reader; only its `when` compiles.

## 3. What compile does with an enemy

For kinds `ai` and `ai_line`, one manifest entry per enemy:

1. `enemy.py build_ai` derives the record from the level, the archetype's role, the kit and
   the generals. The sheet cannot set any of those derived fields (`references/sheet.md`
   section 3).
2. The sheet's blocks replace the default rule list. Every rule is made by `factory.py`.
3. If the list has no unconditional last rule, the fallback block is added and reported (law 41).
4. The list is checked against the rule cap (law 90) and the factory's own rule-set check.
5. The manifest is written with every record hidden (`D-hidden-true`), and
   `validate.py --strict` runs on it. Its output and exit code are passed through untouched.

`compile` exits 0 only when validation passes. Otherwise the manifest is on disk and is not
pushable (`D-validate-always`).

## 4. Adding a block

1. Add the entry to its family file, with every part in section 1 filled. Cite laws by number.
   Give at least one exemplar. Put no balance number in it.
2. If the behaviour is new, add one builder to `scripts/library.py` that makes its rules
   through the factory, and register it in `RULE_BUILDERS` (or `KIT_CHECKS`).
3. Add a selftest line for what it builds and for what it refuses.
4. Run `python3 scripts/library.py --selftest` and `python3 scripts/design.py --selftest`.

A changed behaviour is a new version (`/v2`), never an edit to a shipped one: sheets name the
version they were designed against.

## 5. Limits of this build

Known and deliberate. Each is a later entry or phase, not a workaround to invent now.

- **Stat shape.** Every compiled enemy has the uniform stat block. A recorded stat anchor
  (for example the ratified ones in the build skill's `references/lines.md`) cannot be written
  on a sheet yet. Shaped archetypes wait for decision D-05.
- **Roles.** The three archetypes map to `enemy.py`'s role table, which has no ratification
  record. They are `proposed`.
- **Shared cooldowns.** Two jutsu that share a cooldown group lock each other out (law 91).
  The group table is live data; no capture of it is in the repository, so no block checks it.
- **Ground-target jutsu, summons, telegraphs, enrage, anti-camping.** These belong to the boss
  fight grammar and the setup library. A rule pattern refuses a ground-target jutsu.
- **Ally-facing support.** A pool jutsu is gated on distance to an opponent even when its
  effect is meant for allies.
- **`validate.py --strict` and `preferredStat`.** The validator still requires a field the
  game dropped (RUL-2026-10-25-009; fix brief `state/prompt_validate_stale_rules.md`). Until
  that separate fix merges, every compiled AI reports that one diagnostic and `compile`
  exits 1. It is reported, never waived.

## 6. Worked examples

`references/examples/` holds three shipped enemies written as sheets: `verge_prowler.json`
(`ai`), `verge_line.json` (`ai_line`) and `unsigned_nightfoot.json` (`ai`). Kits, levels and
behaviour are as the build skill's `references/lines.md` records them. Values that page does
not record (role, generals, one health threshold) are left as open slots, so each example
checks clean and `compile` refuses it, naming the slots. That is the intended state of a sheet
waiting on the director.
