# Writing guide

How TNR content reads: names, descriptions, battle lines, log lines and quest text. This page
routes to the owners of each rule and says what `design.py check` lints. It restates none of
them. Final prose is always the director's call.

## Contents

- 1. Register
- 2. Who owns which rule
- 3. Names
- 4. Jutsu descriptions and battle lines
- 5. Boss text and log lines
- 6. Quest and dialog text
- 7. Item and chest descriptions
- 8. What `check` lints
- 9. Open questions

## 1. Register

TNR is a ninja world told plainly: concrete images, present tense, things a person does.
Analogues and flavour from the Naruto franchise are allowed to an extent, within copyright law
(`D-no-franchise`; RUL-2026-11-09-141 item 2). Art is held to a stricter house rule: no
forehead protectors, village headbands or clan insignia (RUL-2026-11-09-142). When it is
unclear whether a name or image is flavour or a copy, ask the director.

Each event has its own voice on top of this. Write it down once, in the event's story bible,
with the words it never uses, and put those words in the sheet's `voice.banned_words` so the
lint holds them. The worked examples of a voice section are
`docs/design/SKYGLASS_STORY_BIBLE.md` ("Voice") and `docs/design/SAYO_BIBLE.md`.

## 2. Who owns which rule

| Rule | Owner |
|---|---|
| Jutsu description and battle-line house style | `docs/design/jutsu_overhaul/WRITING_STYLE.md` (RUL-2026-10-21-021) |
| Edits to existing text are targeted; American English; area wording; chance wording | same file, "Review lessons" (RUL-2026-10-21-022) |
| Premium tier: event and forbidden jutsu | same file, "Premium tier" |
| Text and icon show the same moment | RUL-2026-10-24-004 |
| Battle-line placeholders | build skill `references/jutsu.md` section 2 |
| No em dashes in dialog | `D-emdash-dialog`; build skill `references/quest.md` 6.2 |
| Dialog is HTML; choices fork; no mechanics in player text | build skill `references/quest.md` 6.2b |
| Silent reset and win nodes need a dialog before them | engine law 47 |
| Battle text for shared and library jutsu: action first | RUL-2026-10-28-028 item 5 |
| Every phase change gets a one-line battle cue | RUL-2026-10-28-028 item 6 |
| Boss jutsu descriptions carry hint text players can read | RUL-2026-11-05-123 item 3 |
| Item descriptions explain the item; chest description format | `docs/design/SKYGLASS_LOOT_TABLES.md` section 0 (RUL-2026-10-28-020, -030, RUL-2026-10-31-074) |
| Tier and rarity naming | RUL-2026-10-29-058 |
| Length bounds | build skill `data/45d_DATA_entity_schemas.json` |
| Names are unique; usernames are unique across players too | engine laws 30, 66 |
| The director's real first name never appears | `D-no-real-name` |

## 3. Names

- A name says the job or the image in a word or two. The shipped lines show two grammars,
  compound job names and blunt trade nouns, and why they differ: build skill
  `references/lines.md`.
- Check a name against `answers/` in the repository before settling on it; distinctive beats
  generic, because collisions are silent (engine law 30).
- A themed set that collides takes a shared prefix. Variant and tier names follow the rulings
  in section 2.
- A name that echoes a franchise technique is flagged to the director, not quietly kept or
  quietly changed.

## 4. Jutsu descriptions and battle lines

Follow the house style file. The points people miss most: the description says everything the
player will notice and nothing the effects do not do; durations are in words; the battle line
is one vivid image of the cast, in present tense; existing premium text is corrected, never
shortened; event and forbidden jutsu get the premium treatment.

## 5. Boss text and log lines

- The battle log is the boss's voice. Every jutsu's battle line prints there, so a line can
  carry a clue: what the mark means, what is about to land, what the player should do.
- A phase change always has a cue line.
- Per RUL-2026-11-05-123, players can read boss jutsu descriptions in battle, so the hint
  voice stays in the descriptions. `docs/design/MOTHER_OF_ECHOES_JUTSU_TEXT.md` ("Voice and
  the hint rule") is the worked example.
- Keep boss lines short; the fight is read on a phone between turns.

## 6. Quest and dialog text

Follow the build skill's `references/quest.md` 6.2 and 6.2b. In short: one to three sentences
a node; a stage direction, then a voice; choices are lines a person would say and lead
somewhere different; wrong choices teach; the fiction states the danger, never the mechanics;
enemies and items are named in objective text.

For an event, every run's description opens by stating the stakes plainly (RUL-2026-10-28-028
item 8), and the tier is told through the fiction rather than a number
(`docs/design/EVENT_STRUCTURE.md`, P6).

## 7. Item and chest descriptions

One line of story, then what the item is for in plain words. Chests state every drop and its
chance in the format the loot-tables owner gives; that text is generated from the same table
as the chest, never typed twice.

## 8. What `check` lints

`design.py check` runs these on `text.entries`. Each cites its owner in the message.

| Lint | Result |
|---|---|
| Em dash in a `dialog` or `choice` entry | error |
| Em dash in other player-facing text | note (shipped events keep them out of all player text) |
| A battle line or log line with a placeholder the engine does not know | error |
| Text longer or shorter than the field's schema bound, looked up by the entry's `entity` | error |
| Text for an entity with no generated length contract (an AI's name, for one) | note: not checked |
| A word from the sheet's `voice.banned_words` in player-facing text | error |
| Empty text | error |
| `AUTHOR` left in place | listed as an open slot |

The lints run only once the sheet's structure is valid; until then `check` reports the
structure errors and says the text was not checked.

It cannot judge voice, accuracy against the effects, or whether a line is good. Those are read
by a person, and the director reads last.

## 9. Open questions

- Whether new bosses should keep readable hint text in their descriptions or use staff-only
  descriptions was raised in the overhaul inventory (D-08). Until the director says otherwise,
  the ruling in section 5 stands.
- There is no single guide yet for log lines outside boss fights or for achievement and badge
  text. Follow the nearest shipped example and bring the text to the director.
