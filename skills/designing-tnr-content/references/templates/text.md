# Stage 6: Text

Every player-facing string, in `text.entries`. Guide: `references/writing.md`.

## Template (one entry)

```json
{ "for": "<record or node the text belongs to>", "entity": "jutsu|item|quest|ai|asset",
  "field": "name|description|battleDescription|successDescription|dialog|choice|log_line|item_description",
  "text": "<the text, or AUTHOR>", "player_facing": true }
```

## Exit checklist

- [ ] `design.py check` shows no text errors, and its notes were read.
- [ ] Every jutsu has a description and a battle line; every boss phase has a cue.
- [ ] Each description says what the effects do and nothing they do not.
- [ ] Names were checked against `answers/` for collisions.
- [ ] The event's banned words are in `voice.banned_words`.
- [ ] No `AUTHOR` remains.

## Decision for the director

The text itself, in one read. Names first if any are new: a rejected name changes everything
that quotes it.
