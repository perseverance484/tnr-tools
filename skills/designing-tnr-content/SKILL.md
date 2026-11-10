---
name: designing-tnr-content
description: Designs content for The Ninja RPG (TNR) before it is built - AI enemies and enemy lines, boss fights, quests and quest chains, dungeons and whole events - as a checked design sheet the build skill compiles. Use this skill whenever the user asks for a new enemy, boss, fight, quest, mission, dungeon, hunt, event or event page, asks what something should do, pay or say, wants options or a concept before anything is built, or hands over a one-paragraph idea, even if they do not say "design". If the design is already decided and they want records, use building-tnr-content; for still art use producing-tnr-art.
---

# Designing TNR content

This skill owns the *what* and the *why*. It ends in a **design sheet**: one JSON file, checked by
`scripts/design.py`, that the build skill turns into records. Nothing here writes a manifest by
hand, and nothing here decides a number that is the director's.

## Doctrine (rendered)

<!-- doctrine:begin @b614200 target=skill-design - RENDERED from docs/DOCTRINE.md; edit there, then render_doctrine.py --write -->

TNR is a live browser game with no staging environment: a bad push lands on
players. Every rule in the mounted project instructions and in this block
exists because a push failed, or because a record went live wrong and someone
had to repair it by hand on a phone.

**Doctrine rides the mounted project instructions.** docs/DOCTRINE.md is the
single source; this block carries only what the mounted paste does not. If
this skill is ever run without the mounted instructions, read
docs/DOCTRINE.md before building anything.

**Pool codes over raw ids** when referring to shared AI records, so a renamed
record does not silently repoint.

<!-- doctrine:end -->

## Three rules

- **Cite, don't copy.** Every engine rule, number and ruling has one owner: an engine law, a
  generated contract, a reference page of the build skill, or a ruling. This skill points at the
  owner. If you find yourself typing a number from memory, stop and read it from its owner.
- **Construct, don't author.** A design ends in a sheet that `design.py` checks and compiles
  through the build skill's `factory.py`, `mission.py` and `enemy.py`. You never write a rule
  object, a stat block or a reward block as JSON.
- **The director decides taste, balance and rewards.** Anything not ratified is a named open slot
  (`AWAITING_RULING`), listed for the director, never a guess. Unwritten text is `AUTHOR`.

## The workflow

Work the stages in order. Skip by size: one enemy needs stages 1, 3, 6 and 7; a boss event needs
all nine. Each stage has a template in `references/templates/` with its exit checklist and the
decision it brings to the director.

| # | Stage | You produce | Done when | Template |
|---|---|---|---|---|
| 1 | Brief | one paragraph: purpose, audience, where it lives, size | the director agrees it | `brief.md` |
| 2 | Concept | hook, fantasy, references, two or three options | the director picks one | `concept.md` |
| 3 | Design sheet | the sheet, plus its generated design doc | `design.py check` has no errors; only named slots remain | `design_sheet.md` |
| 4 | Fight design (bosses) | character bible, fight script, telegraph map, clutter and anti-camping checks | the checklist passes | `fight_design.md` |
| 5 | Tuning | measured results against targets; payout check | within targets, or the gaps are listed for the director | `tuning.md` |
| 6 | Text | names, descriptions, battle lines, log lines, quest text | text lint clean | `text.md` |
| 7 | Build handoff | the compiled manifest, validated, as a go card | gates clean and the director says go | `build_handoff.md` |
| 8 | Art (as needed) | art slots handed to the art or animation skill | their gates | `art.md` |
| 9 | Live verification | post-run reads and a battle check | it matches the design; findings logged | `live_verification.md` |

## The design sheet

```
python3 scripts/design.py new <kind> --id <slug> --title "<name>" -o sheet.json
python3 scripts/design.py check sheet.json
python3 scripts/design.py explain sheet.json -o design.md
python3 scripts/design.py compile sheet.json -o push/NNN_name.json
```

Kinds: `ai`, `ai_line`, `boss`, `quest`, `quest_chain`, `dungeon`, `event`.

- `new` scaffolds a sheet with every undecided value already marked as a slot.
- `check` validates the sheet and prints every open slot, every library reference and every
  error. Open slots do not fail it: they are the list you take to the director.
- `explain` writes the design doc from the sheet, ending with a table of every value on it. The
  doc is never edited by hand; change the sheet and regenerate.
- `compile` refuses while a slot, a decision or a library reference is open, and says which.

`references/sheet.md` explains every block of the sheet, the slot words, and how the older
mission and event sheets fit inside it.

**A sheet cannot reach an engine field.** Level, role, kit and rules go on the sheet; rank, stat
numbers, pools, multipliers, quest gates and reward blocks do not. `check` refuses them and
names the owner that derives each one.

## Bringing a decision to the director

One decision per card, with options and what each one costs. A decision that needs a ruling is
recorded in the sheet's `decisions` list and `explain` prints it as a card:

```
GO? <id> <the decision in one line>
What changes:  <what each answer changes in the design>
Needs you:  <option A> / <option B> / <option C>
Blocks:  <which stage waits on it, or "nothing">
```

The card for a finished job (stage 7) is the repository's own, in
`docs/workflows/OPERATING_MODEL.md` section 2; do not invent a second format for it.

## References

| When | Read |
|---|---|
| Filling in or reading a sheet | `references/sheet.md` |
| Writing any player-facing text | `references/writing.md` |
| Working a stage | its template in `references/templates/` |
| An engine rule, a bound, a pool code | the build skill: its packs first, then `references/`, then the generated `data/` files |
| How an event should be structured | `docs/design/EVENT_STRUCTURE.md` in the repository |

## What this build of the skill does not do yet

Said plainly so nobody plans around a tool that is not there:

- **Libraries** (archetypes, rule patterns, loadouts, quest structures, setups, payouts, boss
  grammar) are not shipped. A sheet may already name library entries; `check` reports them as
  pending and `compile` refuses.
- **`compile`** is not shipped for any kind.
- **The encounter simulator** and the worked examples are not shipped.

Until they are, a decided design is built with the build skill directly, as before.
