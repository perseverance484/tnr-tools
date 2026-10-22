# Bug report: battle text placeholders and basic-action grammar

- **For:** the TheNinjaRPG developers (studie-tech/theninjarpg)
- **From:** the content team (dauntless), prepared by Claude Code, 2026-10-22
- **Source checked:** `origin/main` at `107d7a8` (2026-10-22). Line numbers are from that commit.
- **Impact:** players see the battle log on every action. These bugs put wrong pronouns, raw placeholder
  tokens and bad grammar into it, including on the basic actions every player uses.
- **How this was found:** reading the source only. Nothing was run against the live game.

## Summary

| # | Bug | Where | Seen by players |
|---|---|---|---|
| 1 | `%target_subject` prints a reflexive pronoun ("himself"/"herself") | `libs/combat/actions.ts:1301-1307` | any jutsu text using it |
| 2 | `%user_posessive` / `%target_posessive` print "hers"/"theirs" instead of "her"/"their" | `actions.ts:1282-1284`, `1317-1323` | any text using them on a non-male user/target or several targets |
| 3 | Every gender that is not exactly `"Male"` gets female pronouns, including `"Other"` | `actions.ts:1274-1288`, `1301-1331`; genders in `validators/register.ts:44` | players who registered as Other, and barriers |
| 4 | Barriers are pushed as target name `"barrier"` with gender `"it"`, which then reads as "her" | `actions.ts:1154-1155`, `1173-1174` | any attack that also hits a barrier |
| 5 | Target genders are de-duplicated, so two targets of the same gender read as one ("him" for two men) | `actions.ts:1223` | AoE jutsu using `%target_*` |
| 6 | `%jutsu` is never substituted, but it is in the default battle description of every new jutsu | default at `server/api/routers/jutsu.ts:662`; no `replaceAll("%jutsu", …)` anywhere | jutsu created and never edited |
| 7 | With no recipient, `%target` and `%target_*` stay as literal text | `actions.ts:1299`, `1333` (replacement only runs when there are targets) | ground/AoE jutsu that hit nobody, misses |
| 8 | Basic actions use "%user perform", not "performs" | `actions.ts:497` (basic attack), `actions.ts:584` (basic heal) | every battle |
| 9 | Basic cleanse reads "cleanses all negative effects from self" | `actions.ts:683` | every cleanse |

## Details

### 1. `%target_subject` is reflexive

```ts
// actions.ts:1301
"%target_subject",
targetGenders.length === 1 && targetGenders[0]
  ? targetGenders[0] === "Male" ? "himself" : "herself"
  : "they",
```

The subject form should be "he"/"she" (the `%user_subject` branch above it does this correctly). Example:
"%target_subject staggers back" prints "himself staggers back".

### 2. Possessive placeholders use the pronoun form

`%user_posessive` returns `"his" : "hers"` (1282-1284) and `%target_posessive` returns `"his" : "hers"` / `"theirs"`
(1317-1323). Possessive determiners are "her" and "their": "%user raises %user_posessive blade" prints
"Aiko raises hers blade".

### 3. Only "Male" gets male pronouns; "Other" gets female ones

Every branch is `gender === "Male" ? <male> : <female>`. Registration allows `["Male", "Female", "Other"]`
(`validators/register.ts:44`), so players who chose Other are written as "she/her". Suggested fix: a single
helper mapping Male → he/him/his/himself, Female → she/her/her/herself, anything else (Other, barriers, AIs
without a gender) → they/them/their/themselves.

### 4. Barriers appear as a target named "barrier" with gender "it"

When an attack damages a barrier, `targetUsernames.push("barrier")` and `targetGenders.push("it")` run (1154-1155,
1173-1174). `"it"` is not `"Male"`, so it reads as "her", and "barrier" is joined into `%target`
("Aiko strikes Kenji, barrier"). Consider leaving barriers out of the text lists, or naming them properly.

### 5. De-duplicated genders make several targets singular

`targetGenders = [...new Set(targetGenders)]` (1223) runs before the `targetGenders.length === 1` checks. Two
male targets become `["Male"]`, so the text reads "him" instead of "them". The singular/plural decision should use
the number of recipients (for example `targetUsernames.length`, before or after de-duplication of names), not
the number of distinct genders.

### 6. `%jutsu` is never replaced

New jutsu are created with `battleDescription: "%user uses %jutsu on %target"` (`routers/jutsu.ts:662`), but no
code substitutes `%jutsu`. The line prints "Fireball: Aiko uses %jutsu on Kenji". Either add
`replaceAll("%jutsu", action.name)` next to the `%user` replacement, or change the default text.

### 7. Unreplaced `%target` when nobody is hit

The `%target_*` replacements run only `if (targetGenders.length > 0)` (1299) and `%target` only
`if (targetUsernames.length > 0)` (1333). A ground or area jutsu that hits nobody prints the raw token:
"Aiko unleashes a storm on %target". Suggested fallback: replace with a neutral word such as "the area" or
"nobody", or strip the token.

### 8 and 9. Basic action grammar

- `actions.ts:497`: `"%user perform a basic physical strike against %target"` → "performs".
- `actions.ts:584`: `"%user perform basic healing of %target"` → "%user performs basic healing on %target".
- `actions.ts:683`: `"%user cleanses all negative effects from self"` → "from themselves" (or use
  `%user_reflexive` once bug 3 is fixed).

## Also noted (lower priority)

- Empty battle descriptions fall back to `` `%user uses ${action.name}` `` and are then prefixed with the action
  name (1269-1271), giving "Fireball: Aiko uses Fireball".
- The placeholder is spelled `posessive` (one "s"). Content authors have to match the typo; consider accepting
  `possessive` as an alias.
- There are no tests covering this text pipeline. A small unit test over the replacement block would catch
  every item above.

## Content-side follow-up (ours)

The content team will avoid `%jutsu`, `%target_subject`, the possessive and gendered tokens in new text until
these are fixed (house style already does), and will correct the tooling reference that lists `%jutsu` as
working (`skills/building-tnr-content/references/jutsu.md`).
