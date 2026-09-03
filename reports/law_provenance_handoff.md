# Handoff: law provenance audit, and what it changes for tooling

For the agent that maintains this repo. Read this before touching `validate.py`,
`45c`/`45g`, or any balance or quest tooling that cites an engine law.

## What happened

Every law id in `docs/ENGINE_LAWS.md` (93 of them: 1-89 plus 16b, 16c, 16d, 41b) was
given one provenance verdict, verified against a single pinned commit of the game source:

```
studie-tech/TheNinjaRPG @ 345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9
2026-08-31  "Stabilize hospital patient ordering"
```

| Verdict | Count |
|---|---:|
| `ENGINE` (provable, file + line + symbol) | 36 |
| `PARTIAL` (some clauses provable) | 19 |
| `CONTRADICTED` (source says otherwise) | 1 |
| `NOT_IN_SOURCE` (not settleable from the codebase) | 26 |
| `DOCTRINE` (our convention, no engine fact) | 11 |

Data lives on branch `law-provenance`, commits `b9b3172` (first pass) and `fe2eecb`
(re-check):

- `reports/law_provenance.json` - machine readable, keyed by law number. Start here.
  Each entry carries `verdict`, `file`, `line`, `symbol`, `evidence`, and a `note`
  that says which clauses were and were not provable.
- `reports/law_provenance.md` - the same data plus a contradictions section, cross-law
  conflicts, a low-confidence list, and a record of what the re-check changed.

## Act on this first: four places `validate.py` disagrees with the engine

These are the audit's operational consequences. Two gates reject content the engine
accepts; two let through content the engine rejects. All four were confirmed by reading
both sides at the pinned commit. None has been fixed. **No tooling file was modified by
this audit.**

### 1. Over-strict: the power cap rejects legal content

`validate.py:769-770` errors on any effect with `power > 100`, citing law 6.

The engine caps `power` at 100 for only 9 tags. The other 61 spread `PowerAttributes`
(`app/src/validators/combat.ts:111`, `z.coerce.number().min(0)` with no maximum) *after*
`BaseAttributes`, so the uncapped definition wins. The uncapped set includes `damage`,
`pierce`, `heal`, `shield`, `stun`, `absorb` and the whole increase/decrease family.

Effect: any manifest using `power > 100` on a combat tag is blocked locally even though
the server would take it. This is a live false-rejection gate on balance work.

### 2. Over-strict: the acyclic check is not conditional

`validate.py:831` calls `check_acyclic` for every quest entry carrying `content`.

The engine runs the cycle check only for consecutive quests. `verifyQuestContentForSave`
(`app/src/libs/quest.ts:2036`) reaches the full flow validator through
`if (consecutiveObjectives) return verifyQuestObjectiveFlow(objectives)` at `:2053`; a
non-consecutive quest gets only the dialog-branch scan.

Effect: a non-consecutive quest with a back edge is rejected locally and would pass the
server. Note this does not license authoring cycles; law 87's advice is still good
practice. It means the gate's scope is wrong.

### 3. Under-strict: dialog option checks miss two engine rules

`validate.py:666-683` only rejects a dialog with zero options.

The engine's `verifyDialogBranches` (`app/src/libs/quest.ts:1840`) enforces three rules:
at least one option, **every option must carry a non-empty `nextObjectiveId` string**, and
**that id must resolve to an existing objective**. The second and third have no local
equivalent.

Effect: a manifest with a dangling or empty option passes local validation and is refused
at push. This is a rejected-push class we can close.

### 4. Under-strict: a string `nextObjectiveId` on a dialog

`validate.py:676` counts a bare non-empty string as one option:
`opts = len(nxt) if isinstance(nxt, list) else (1 if isinstance(nxt, str) and nxt else 0)`.

The engine requires an array: `if (!Array.isArray(nextRef) || nextRef.length === 0)` at
`quest.ts:1846`. A dialog whose `nextObjectiveId` is a plain string is rejected server-side
with the "must have at least one option" message.

Effect: same class as 3. Local pass, server refusal.

## Four laws the source contradicts

Full detail in the report's contradictions section. In every case the law's *instruction*
survives; the stated mechanism, reason or direction is what is wrong.

**Law 19 is a full `CONTRADICTED` and inverts.** There is no narrower item union. Jutsu and
item share one union, `effects: z.array(AllTags).superRefine(SuperRefineEffects)`
(`combat.ts:1327` jutsu, `:1491` item). The asymmetry lives in the per-entity refinements
and runs the other way: `SuperRefineJutsu` (`:1218-1220`) rejects `rollbloodline`,
`rollsagemode` and `removebloodline` outright, while `SuperRefineItem` (`:1122`) permits all
three. The item path is **wider** than the jutsu path. Any tag list derived from the law's
stated direction will wrongly exclude item-legal tags.

**Law 6** states `power` caps at 100 per row. It does not, for 61 of 70 tags. See divergence 1.

**Law 23** states the `consecutiveObjectives` DB default is false. `app/drizzle/schema.ts:3622`
is `.default(true).notNull()`. The instruction still holds for a different reason: the write
schema requires the field (`validators/objectives.ts:700`, `z.coerce.boolean()` with no
prefault). Law 37 rests on 23's premise and needs re-deriving.

**Law 75** says ground effects promoted to user effects get `createdRound: curRound - 1`
*when instant*. `process.ts:335` is `createdRound: isInstant ? curRound : curRound - 1`,
which is `curRound - 1` when **not** instant. The condition is inverted. Everything else in
law 75 verifies exactly.

## Constraints on anything you do with this

1. **Do not edit law text.** `docs/ENGINE_LAWS.md`, `docs/10_LAWS_core.md` and
   `skills/building-tnr-content/12b_LAWS_coverage.md` were untouched by this audit and
   should stay that way until a human decides how to record a correction. The report is
   evidence for that decision, not the decision.
2. **Provenance is a different axis from ENFORCEMENT.** The `validate` / `builder` /
   `generated` / `knowledge` / `superseded` classes in `12b_LAWS_coverage.md` are unrelated
   to these verdicts and were deliberately not touched or reported on. Do not merge the two.
3. **Every verdict is pinned to `345d18ac`.** It is a statement about that commit, not about
   prod and not about any later commit. The `regen-schemas-sentinel` workflow is the thing
   that will tell you the contract moved; when it fires, these verdicts need re-testing.
4. **`NOT_IN_SOURCE` does not mean false.** For laws that look engine-shaped it means this
   pass did not settle it, and the `note` field says so. Twenty-six laws carry it, and many
   are behaviour-proven from fight captures. Do not delete or demote a law on this basis.
5. **Do not add citations to the report from memory.** Every `file:line` in it was read at
   the pinned commit. A wrong citation is worse than none, because it launders a guess into
   evidence.

## Known-weak verdicts

The report's "Least confident" section lists seven, ranked. The two worth knowing before
you rely on anything:

- **Law 80** is the weakest. The asset form entry is `type: "avatar"` for every scene type
  (`hooks/asset.ts:66-69`, `:74-77`), which is the law's mechanism, but the trail was not
  followed through `ContentImageSelector` to the image element. The AvatarImage claim is
  uncited.
- **Laws 41b and 63** both describe AI rule fall-through from different sides and both came
  back `NOT_IN_SOURCE` for the same reason: the action selector in
  `app/src/libs/combat/ai_v2.ts` was not traced. This is the largest remaining gap, and the
  two should be verified together rather than separately.

## Suggested order

1. Divergences 3 and 4 first. They are small, they close a rejected-push class, and they
   make local validation stricter rather than looser, so nothing new gets through.
2. Divergence 1 next. It is unblocking rather than tightening, so it wants a human call on
   whether the 100 cap should stay as house policy even though the engine does not enforce it.
3. Divergence 2 after that, with the same question attached.
4. Laws 41b and 63 as a single verification pass against `ai_v2.ts`.
