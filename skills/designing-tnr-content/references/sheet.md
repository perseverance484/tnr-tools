# The design sheet

The sheet is the only contract between design and build. Its schema is
`data/design_sheet.schema.json`; this page explains it and never restates a rule the build
skill owns. Paths such as `references/ai.md` below are the build skill's
(`building-tnr-content`) unless they start with `docs/`.

## Contents

- 1. Envelope
- 2. Slot words
- 3. What a sheet may not carry
- 4. Library references
- 5. Blocks by kind
- 6. Payout and tuning values
- 7. Text and art
- 8. Decisions
- 9. The two older sheets

## 1. Envelope

Every sheet has `sheet_version`, `kind`, `id` (a lowercase slug), `title` and `brief`. `brief` is
stage 1 on the sheet: purpose, audience, where the content lives, and its size (`single`,
`small` or `event`), with `agreed` set true once the director has agreed it. `concept` is stage
2: hook, fantasy, references, the options offered and the one chosen. `voice` carries the
register line and the words this piece of content must never use.

## 2. Slot words

| Word | Means | Who fills it |
|---|---|---|
| `AWAITING_RULING` | a balance, reward, tuning or taste value | the director (`D-reserved-dauntless`) |
| `AUTHOR` | creative text not written yet | whoever is writing, then the director's read |
| `dauntless` | the event sheet's older spelling of `AWAITING_RULING` | accepted inside `event` only |

A slot is named by its path in the sheet (`boss.enrage`, `payout.entries[0].value`). `check`
lists every one. They are the same word `mission.py` and `data/48_DATA_mission_profiles.json`
already use, so a slot means the same thing in both skills.

A numeric field (an enemy's level, a wave's enemy count, a wave delay, the rounds between an
omen and its payoff) holds a whole number or a slot word and nothing else. "Soon" or "a few"
is refused: write the number, or leave the slot for whoever decides it.

Never replace a slot with a placeholder number to make a tool run. `compile` refuses while one
is open, and that refusal is the point.

## 3. What a sheet may not carry

A sheet states choices. The build tools derive the engine fields from them, and a sheet that
could set those fields would. `check` refuses these keys anywhere on a sheet and names the
owner of each:

- the mission profile fields, fixed fields and null-by-design fields: read from
  `data/48_DATA_mission_profiles.json` (`_field_routing`);
- an AI's stat numbers and role multipliers: read from `scripts/enemy.py` (`STAT_FIELDS`,
  `ROLE_DEFAULTS`);
- an AI's rank and pools, which engine laws 14 to 16 explain and `enemy.py` derives.

What you write instead: an enemy's **level** and **role**, its **kit** as pool codes
(`D-pool-codes`), and its behaviour as **library references**. Parameters of a library entry
are not sheet fields; each entry bounds its own.

One exception, for compatibility: an event sheet in the older form (section 9) is not held to
this rule, because that form was written with gate fields on it. New work puts gates in the
quest structure's parameters instead.

## 4. Library references

Behaviour, structure and loadouts are named, not spelled out:

```json
"rules": [ { "use": "rule_pattern/telegraph_payoff/v1", "params": { "signature": "Core Rupture" } } ]
```

An id is `family/name/vN`. `check` resolves it against `data/libraries/<family>.json`. If the
family's library has not shipped, the reference is reported as pending; if the library exists
and the id does not, it is an error. Never write a rule object in a sheet: the vocabulary is
fixed by engine law 39 and built only from `data/45c_DATA_constructors.json`.

## 5. Blocks by kind

| Kind | Block | Holds |
|---|---|---|
| `ai` | `enemy` | one enemy: name, role, level, combat role, tactical read, rules, phases, loadout |
| `ai_line` | `line` | a named line of two or more enemies (rungs) and its build order; `references/lines.md` has the shipped lines |
| `boss` | `boss` | the boss enemy, its allies, the character bible, acts with a fight script and a telegraph list, anti-camping, enrage |
| `quest` | `quest` | a quest structure by library id, its parameters, summary, gating in words, enemies, setups; or a `mission` block (section 9) |
| `quest_chain` | `chain` | two or more quests with their order, and shared enemies |
| `dungeon` | `dungeon` | floors, waves by enemy key and count, delays, the boss floor, enemies |
| `event` | `event` | an event sheet (section 9); the structure framework is `docs/design/EVENT_STRUCTURE.md` |

An enemy's `loadout.kit` is a list of pool codes from `data/32b_DATA_pool.json`. A
`signature` is a new jutsu the pool lacks: give its name and intent; its effects are built in
the build skill from live exemplars (engine law 3), not described here as numbers.

## 6. Payout and tuning values

Every value under `payout` and `tuning` takes one of three forms:

```json
"AWAITING_RULING"
{ "value": 5000, "source": "docs/rulings/2026-10.md RUL-2026-10-24-018" }
{ "reward_package": "<the package's name in the game's reward catalog>" }
```

- A number must carry its source: the owner's path, or a ruling id. A bare number is refused.
- A reward package is the preferred form for currency (RUL-2026-11-09-141 item 1): the game's
  own catalog holds the amounts and the director sets them there (RUL-2026-10-24-019). Until
  the catalog has been captured into the repository, a package name is taken as written and
  cannot be verified by `check`.
- Mission rewards are not written on a sheet at all: `mission.py` fills them from the profile.

`data/48_DATA_mission_profiles.json` marks some of its own values as proposed or inferred
rather than ruled. When you cite it as a source, say which standing the value has.

## 7. Text and art

`text.entries` holds every player-facing string with what it is for, the entity and field it
lands in, and whether players see it. `entity` is required: it is how `check` finds the
field's length bound in the build skill's `data/45d_DATA_entity_schemas.json`. The schema's
`_meta.text_entities` maps the sheet's entity names to that file's (an `asset` is its
`gameAsset`); an entity with no generated contract, such as `ai`, is reported as unchecked. `references/writing.md` is the guide and lists what
`check` lints. `art.slots` names each asset the design needs and which skill makes it:
`producing-tnr-art` for anything still, `animating-tnr-combat` for anything that moves.

## 8. Decisions

`decisions` is the list of questions for the director: an id, the topic, the options, what each
changes, what it blocks, and `status` (`open` or `ruled`, with the ruling id once it exists).
`explain` prints each open one as a card. The design doc it writes ends with a table of
every value on the sheet, so a choice cannot be on the sheet and absent from what the director
reads; `explain` refuses a sheet whose structure is invalid rather than render it wrongly. A ruled decision is recorded in the rulings ledger
(`docs/RULINGS.md` says how), not only on the sheet.

## 9. The two older sheets

Both keep working unchanged.

- **Mission sheet.** The creative half that `scripts/mission.py` reads (rank, name, the two
  descriptions, objectives, roster). Put it under `mission`, or pass the bare file: `check`
  wraps it as kind `quest`. Its top level is held to section 3; its objective nodes are the
  build skill's to validate.
- **Event sheet.** An instance of `data/26x_EVENT_sheet_schema.json`, the machine twin of the
  staff canvas `EVENT_SHEET.md`; `references/event.md` is its build contract. Put it under
  `event`, or pass the bare file: `check` wraps it as kind `event` and reports each
  `dauntless` as an open ruling slot.
