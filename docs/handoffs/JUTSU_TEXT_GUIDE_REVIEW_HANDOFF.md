# Implementation handoff: jutsu text guide (Lane A, for independent review)

- **Repository:** `perseverance484/tnr-tools`
- **Branch:** `claude/tnr-content-tickets-tcbi34` (sole writer: Fable / Claude Code)
- **Base SHA:** `33300a0ab656f55b337192625e84f6ead55ba73a` (main at freeze)
- **Head SHA (audit target):** `c0e9d1b5250c2bed38d63c580c87c9ebca237169`
- **Integration target:** `main`, after review (director, 2026-10-21: "Writing guide goes for review then main")
- **Reviewer:** ChatGPT, independent; do not modify the branch. A skillpack workflow may add an automatic
  `dist/` rebuild commit on top of the head; it is not part of the audit target.

## Scope

**Objective:** a skill reference for writing player jutsu descriptions and battle lines that match the
jutsu's live effects, grounded in the game source.

| File | Change |
|---|---|
| `skills/building-tnr-content/references/jutsu_text.md` | new (about 115 lines): what the player sees, reading the record, description rules, battle-line rules, tag wording table, suggest-mode checklist |
| `skills/building-tnr-content/references/jutsu.md` | `battleDescription` row no longer lists `%jutsu` as a placeholder; both text rows point at the new reference |
| `skills/building-tnr-content/SKILL.md` | one routing row for the new reference |
| `skills/building-tnr-content/packs/jutsu-build.md`, `references/_toc/jutsu.json` | re-rendered by `build_packs.py --write` (not hand-edited) |

Commits: `3d35e9b` (guide), `ad25d2c` (drop the "one foe" reach rule after the director's note; use the
approved Water's Domain text as the example), `c0e9d1b` (checklist line: one open suggestion per record).

**Not done:** no change to `validate.py` or any lint (for example, flagging `%jutsu` or gendered
placeholders automatically); the guide's file is not added to the `_toc` list or to any pack; no doctrine
or law text changed.

## Verification (run on the head, from the repo root unless noted)

| Command | Result |
|---|---|
| `python3 scripts/build_packs.py --check` (cwd `skills/building-tnr-content`) | all packs and TOCs current (exit 0) |
| `python3 skills/building-tnr-content/scripts/doctrinemap.py .` | 21 assertions, 18 referenced, 16 surfaces; 0 errors, 0 warnings |
| `python3 skills/building-tnr-content/scripts/render_doctrine.py --check` | all projections current (exit 0) |
| `python3 skills/building-tnr-content/scripts/lawmap.py .` | 93 laws, 93 matrix rows; 0 errors, 5 warnings (pre-existing: 16d, 18, 37, 61, 69) |

## Source and provenance

Engine claims were read in `studie-tech/TheNinjaRPG@a744c04` (anonymous shallow clone, 2026-10-21), newer
than the repository's contract pin `85cecae`. The claims to check hardest, with locations:

1. `%jutsu` is never replaced in battle lines (`app/src/libs/combat/actions.ts` around 1268-1336: only
   `%user*`, `%location`, `%target*` are replaced). 13 visible jutsu used it at the 2026-10-06 census;
   8 test/boss jutsu still do at 2026-10-21.
2. `%target` is filled only from units an `INHERIT` effect reached (`actions.ts` ~1095, ~1121), so it
   prints the caster's name on `SELF` jutsu and the literal text on ground jutsu that hit nobody.
3. The gendered placeholders are wrong as shipped (`actions.ts` ~1272-1330: `%user_posessive` gives
   "hers", `%target_subject` gives "himself", non-Male genders get the female form).
4. The battle line is shown as `<name>: <line>` (`actions.ts` ~1271).
5. The jutsu card already lists each effect with its values (`layout/ItemWithEffects.tsx` ~1332-1378).
6. Tag wording table: from each tag's `description` in `app/src/validators/combat.ts`; stun is a chance
   (power %) with an AP loss (`libs/combat/tags.ts` `stun`); buffs and debuffs start the round after the
   cast (handlers skip `isNew` / `castThisRound`).

## Risk, debt, open points

- The style rules (one or two sentences, no numbers, no "you", reach only when it matters) are the
  director's prose preferences as shown in RUL-2026-10-21-007 to -010, written down as rules. Attack any
  rule the approved texts do not support.
- Item 6's "buffs start next round" is generalised from the handlers read (`adjustHealGiven`, `afterburn`,
  `wound`, damage modifiers); not every handler was read.
- `a744c04` is newer than the contract pin; if the reviewer pins a different source SHA, line numbers move.

## Live-game statement

No live game request, no game write, no credential or session material. No browser check was made.
