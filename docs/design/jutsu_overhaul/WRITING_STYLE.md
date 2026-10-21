# Jutsu text: house style (from the director's choices)

**Status:** derived 2026-10-21 from the director's 13 overhaul decisions (RUL-2026-10-21-007 to -021) and
notes. Engine rules for placeholders and effects are in `skills/building-tnr-content/references/jutsu_text.md`
(under review); this file is the voice. Final prose stays the director's call.

## What the choices show

| Jutsu | Description picked | Battle line picked | What it tells us |
|---|---|---|---|
| Water's Domain | D2, director-edited ("their foe", split into two sentences) | B2 | name drives the image; no "one foe"; short sentences |
| Blazing Death Star | D1 | B1 | name drives the image ("falling stars") |
| Divine Thunder Slap | D1 | B2 (shorter) | action first, then the lingering effect |
| Fire Release: Great Fireball | D1 | B2 | plain "over the next few rounds" for a DoT |
| Earthshatter Strike → Bedrock Stance | rework N1, D1 | B2 | name must match the effect; a buff is not a "Strike" |
| Flame Barrage | D1 | B1 | cut false movement claims |
| Kinjutsu: Black Thorn Rose | D1 | B3, second round | forbidden or high-rank jutsu get a fuller, richer battle line |
| Static Flicker | D1 | B1 | movement + burst + lingering charge, in that order |
| Martial Movement | D2 | B1 | soft wording for small debuffs ("unsettle", "dulling") |
| Void Rend | D2 | B2 (more vivid) | the image ("a rift... splits open") over a list of effects |
| Purgatory | D1 | B2 (shorter) | one sentence, one image |
| Blazing Edge | D2 | B2 | the secondary effect may live in the description only |
| Liquid Palm | D1 | B2 | sustain told through the element ("the current... drink in the next blow") |

Director notes: "You seem to have a fixation on 'one foe' as a term."; "this is a forbidden jutsu it should
have a high quality battle line"; rationales should "describe the fix without telling a story".

## Description

- **Two sentences.** Sentence one shows the technique as something the user does, in a concrete image that
  echoes the jutsu's name. Sentence two gives the follow-on effect in plain words.
- **About 140 to 230 characters.**
- **Every effect the player will notice is there**, and nothing is claimed that the effects do not do
  (no movement that is not a `move`, no burn that is not a DoT, no enemy debuff that is really a self buff).
- **Duration in words:** "for a short time", "for a short while", "over the next few rounds"; "for
  several rounds" when it lasts 3 or more. No numbers.
- **Reach without stock phrases:** "the target", "their foe", "nearby enemies", "every enemy caught in
  the blast", "the user". Never "one foe" or "a single foe".
- Third person ("the user"), present tense, British spelling ("armour", "smouldering", "spiralling").
  No "you", no em dashes, no lore that hides what the jutsu does.

## Battle line

- **One sentence**, about 90 to 160 characters, present tense, starting with `%user` or with the image
  around them ("Flames burst from %user's fists...").
- **One vivid image of the cast.** The secondary effect may be hinted ("the heat building with every
  blow") or left to the description; the director usually picked the tighter, more vivid option.
- **Forbidden, S-rank and signature jutsu** get a fuller line: two sentences, richer imagery (Black Thorn
  Rose).
- `%target` only when the jutsu targets an enemy unit (`OPPONENT`, `OTHER_USER`). Never on `SELF`, `GROUND`
  or `EMPTY_GROUND` jutsu. No `%jutsu`, no gendered placeholders, no "his"/"her" for the caster.
- Ends with a full stop.

## Ticket rationale

One to three plain sentences: what was wrong and what changed (RUL-2026-10-21-012). Example: "Adds the
missing user damage boost (+20% for 2 rounds) to both texts. Battle line: 'his' replaced, 'subtle hit
caresses' wording removed."

## Out of scope for a text ticket

Names, effects, costs and balance. A name that contradicts the effects, or echoes a franchise technique,
is flagged to the director; an effect that lands on the wrong side is flagged as a mechanics finding.
