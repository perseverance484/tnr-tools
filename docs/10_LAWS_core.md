> Moved from project knowledge 2026-08-30 (mounted migration), written from the in-context
> project document this session; /mnt/project exposed no file to cp. docs/ENGINE_LAWS.md
> remains the numbered text of record (93 ids; the '89-law' phrasing below predates the
> letter variants and laws 85-89).

# 10 - Cross-cutting engine laws

The full 89-law text lives verbatim, numbered, in repo `/docs/ENGINE_LAWS.md` (fetchable).
Workflow-scoped laws live beside the workflow that needs them, in the owning skill reference.
`validate.py`, `factory.py` and `artpreflight.py` enforce the validate class before anything
reaches the browser; `45c`/`45d`/`45e`/`45g` hold every number, bound and enum. This file keeps
only the laws that cut across every workflow and that no tool can catch. Law numbers cited here
resolve against ENGINE_LAWS.md.

## 1. Storage is not intent (the expensive one)

Live content tells you what the engine accepts, never what we decided to do. Two paid examples:
live quests converge choice menus, so the no-convergence rule was wrongly demoted (law 27 had
said otherwise the whole time; live was the older pattern); every live location node carries
`sector: 0`, so it went onto 85 new nodes, and it is a column default, meaningless across
`sectorType` values (law 89). The right question is never "does live do it" but "does live
doing it make it a decision, or just a fact". Copy a live field only after asking what it means.

## 2. Verification discipline

- A push echo is not a read-back (law 28). HTTP 200 never means success; per-entry
  `json.success` does, and `state: ok` with `live: NONE` means unverified.
- A filtered capture proves nothing. Capture before pushing into an unknown contract: every
  q.fill flow rule (85-88) was visible in a live record nobody had captured, and each cost a
  failed push instead.
- Live records rot silently. A jutsu can be reduced to a blank shell named
  `New Jutsu - <id>`; the id survives, so no reference breaks and no orphan scan notices
  (law 59). Quest `updatedAt` is not maintained, so it cannot indicate change (law 57). The
  in-game editor overwrites whatever it holds, including node images and the quest name, with
  no trace in any bundle: push before editor tweaks, or re-harvest after them (law 58).
- Ids are extracted from bundles by script, never transcribed from printed output (law 29).

## 3. Combat stacking and calibration (laws 9-13)

- Same-type percentage rows stack MULTIPLICATIVELY: total = product of (1 + p_i), within a
  record, across tag + item, everywhere. Thirty 100-rows is x2^30. Tier tuning is built as
  row products (law 9). DDT rows multiply the same way, as products of (1 - p_i): a 10% tag
  and a 10% item give ~19% mitigation, not 20 (law 10).
- Pierce bypasses damage modifiers. Never use pierce hits as a calibration reference; they sit
  at raw-base values amid amplified numbers and mislead the diagnosis (law 11).
- Stacking ramp effects compound exponentially over a fight. Gate or cap ramps by rounds
  (law 12).
- Calibration protocol: one anchor fight against a DECLARED dummy loadout; derive base swing;
  build tier row-products toward per-hit targets; verify one fight per tier. Player DDT is
  nonlinear: numbers tuned for tank-endgame hit normal players 2-3x harder. State the anchor
  in the design doc (law 13).
- `calc.py` does the bucket math; do not do it by hand.

## 4. Turns, rounds and effect timing (laws 61, 75, 76)

- A TURN is one combatant's window to spend its 100 action points; a ROUND is every
  combatant's turn taken together. Every `rounds` duration field counts rounds: a `rounds: 2`
  effect spans two of the bearer's turns, not two actions. Pool attacks cost 60 AP, stances
  40, consumables 20-40; one attack plus one stance fills a turn.
- Effects do NOT apply on the round they are cast; the engine tags `castThisRound` and every
  consumer ignores it. Exceptions, explicitly instant: `damage`, `heal`, `pierce`. So a buff
  cast the same turn as an attack never amplifies that attack; a stance ordered before its
  attacks gains nothing over ordering it after; a duration effect's usable uptime is its
  stated duration minus the cast round.

## 5. Names are global (law 66)

Usernames are unique across ALL UserData, players included: an AI create can be rejected by a
name no AI holds, returning 200 with `success: false` and leaving a blank shell. Short common
English words are already taken. Dedup runs against the answer layer, and a name that matters
gets a fresh `getAllNames` capture first (precedence: capture beats any snapshot).

## 6. Where the rest live

| Cluster | Laws | Location |
|---|---|---|
| Write validators, refs, builder envelopes, null/boolean shapes | 1-8, 16b, 17, 28-32, 36, 45, 46, 72-74 | `references/pipeline.md` |
| Jutsu: equip-sever order, inject guard, blank shells | 18, 20, 59, 60 | `references/jutsu.md` |
| Items: union, PvE, crafting | 19, 21, 22 | `references/item.md` |
| AI: stats model, caps, rules grammar, gates, economy | 14-16d, 39-41b, 62-66, 69-71 | `references/ai.md` |
| Quests: flow, rendering, placement, editor, q.fill | 7, 8, 23-27, 37, 38, 42-44, 47-58, 85-89 | `references/quest.md` |
| Tuning: formulas, drops, runtime constants | 4, 6, 9-13, 61, 67, 68, 75-78, 83 | `references/balance.md` |
| Art: chroma, delivery, preview lies, clipping | 33-35, 50, 79-82, 84 | art skill references |
| Enforcement matrix (what catches a forgotten law) | 12b | building skill root |

A law that must be read lives next to the workflow that needs it. If a number cited anywhere
does not resolve in the owning reference, fetch `/docs/ENGINE_LAWS.md` and read it there.
