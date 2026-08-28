---
name: building-tnr-content
description: Builds and validates content for The Ninja RPG (TNR) - jutsu, AI enemies, items, quests and events - as builder manifests pushed through the hosted userscript. Use this skill whenever the user asks to create, edit, balance, audit or push TNR content, whenever a results bundle or capture is uploaded for verification, and whenever a manifest, engine law, pool code or entity id is mentioned, even if they do not name the skill or ask for a manifest explicitly.
---

# Building TNR content

TNR is a live browser game. Content is pushed by replaying the game's own tRPC API with generated
JSON through a hosted userscript. There is no staging environment: a bad push lands on players.

That single fact shapes everything below. Every rule here exists because a push failed, or because
a record went live wrong and someone had to repair it by hand on a phone.

## The one thing to internalise

**A push echo is not a read-back, and a filtered capture proves nothing.**

The server returns HTTP 200 on requests it did not honour. It strips fields it does not recognise
without complaint. It silently drops unresolvable references. So a manifest that "went through"
tells you nothing about what is now in the database — only a fresh read does. When you need to know
the state of a record, capture it; when you have pushed, capture again and compare.

## Workflow

Content moves in one direction. Skipping a step is how records get created that cannot then be
edited.

1. **Capture first.** Read the live record and the schemas before composing anything. Guessing a
   field shape is the single largest source of failure in this project's history, and it is
   avoidable at zero cost. If a contract is genuinely unconfirmed, ask the user to capture it
   rather than inferring it.
2. **Compose against generated files, never memory.** `45c_DATA_constructors.json` holds every
   tagged shape (effect tags, quest objectives, AI conditions and actions). `45d_DATA_entity_schemas.json`
   holds every field, bound, default and nullability per entity. `45e_DATA_constants.json` holds
   every engine constant with its value and doc comment. `45f_DATA_procedures.json` holds the tRPC
   surface. These are generated from the game source and stamped with provenance. When one of them
   disagrees with a reference file below, the generated file is right and the reference is stale.
3. **Validate before handing anything over.** `python3 scripts/validate.py manifest.json` must
   report zero errors, and you say what you ran. Handing over an unvalidated manifest wastes a
   push cycle on a phone, which is the user's scarcest resource.
4. **The user pushes.** You never push. They run the manifest and upload the results bundle.
5. **Verify from the bundle, by script.** Extract ids programmatically; never transcribe them from
   printed output. A truncated printout once put invented ids into live reward tables.

## Build order

`jutsu -> assets -> items -> ai -> aiProfile -> quest`

Each stage produces ids the next stage references. Building out of order means composing references
to records that do not exist yet, and unresolved references are stripped silently rather than
erroring — the AI stands there with no jutsu equipped and nothing in the bundle says so.

## Non-negotiables

These are not style preferences. Each one has cost someone a repair session.

- **Everything ships `hidden: true`.** Publishing is a separate, deliberate act and it belongs to
  the user, never to you. This applies to every entity on every create.
- **Balance, rewards, rarity and publishing are the user's to finalise.** Propose numbers, carry
  them as explicit placeholders, and list every placeholder in the delivery summary. Do not quietly
  settle a drop rate because a build needs one.
- **Items default to Legendary rarity** unless told otherwise. Most of the playerbase has outgrown
  Epic and below.
- **Weapon riders stay light.** Damage stacks multiplicatively, so separate small sources beat one
  large source; a weapon should carry at most one modest damage bucket and let the player supply
  the stacking. Weapons cost only 40 AP and deal guaranteed damage, so they are already strong.
- **No em dashes in player-facing dialog text** — a node's `description` and its choice text.
  Commas, colons and hyphens instead. Everywhere else they are fine. `validate.py` checks this.
- **Pool codes over raw ids** when referring to shared AI records, so a renamed record does not
  silently repoint.
- **Never reference the Naruto franchise.** TNR is open source; extract facts from the source,
  never copy proprietary text.

## Picking a reference

Read the one that owns the task. They are large; reading all of them wastes the context that the
actual build needs.

| Working on | Read |
|---|---|
| Jutsu: fields, converts, mass-edit sweeps | `references/jutsu.md` |
| AI enemies, stat blocks, behaviour rules, range gating | `references/ai.md` |
| Items, weapons, loot chests, crafting | `references/item.md` |
| Quests, events, objective graphs, dialog | `references/quest.md` |
| Anything that pushes: manifest format, envelopes, capture, image upload | `references/pipeline.md` |
| Tuning numbers, tiering, reward scale | `references/balance.md` |
| Processing a submitted staff design sheet into a whole event | `references/event.md` |
| Reusable enemy lines (Unsigned, Verge, Forsworn) | `references/lines.md` |

`references/pipeline.md` is shared plumbing — read it alongside the entity reference for any build
that ends in a push, not instead of it.

## Bundled scripts

Run these; do not read them unless you are changing them. They execute without entering context,
which is the point.

| Script | Use |
|---|---|
| `scripts/factory.py` | **Construct payloads; do not author them.** `Factory().tag(...)`, `.condition(...)`, `.action(...)`, `.rule(...)`, `.objective(...)`, `.entry(...)`, `.manifest(...)`. Fills schema defaults, rejects unknown fields, enforces build order, hidden-on-create, targetId, nullability and the effect laws at construction. A shape that cannot be built wrong needs no review. Run `--selftest` to see what it catches. |
| `scripts/validate.py manifest.json` | Full preflight: shapes against `45c`, nullability against `45d`, rules from `45g`, quest flow graph, em dashes, id lengths. Zero errors before handover, always. `--parity <builder-checks.json>` proves the builder and this tool implement the same checks. |
| `scripts/calc.py` | Damage and stacking maths. Multiplicative buckets are easy to get wrong by hand. |
| `scripts/harvest.py` | Turn a results bundle or capture into catalog rows. |
| `scripts/stack.py <dir>` | Audit the source stack itself: dangling references, law numbering, id rot. |
| `scripts/schema_extract.py <repo>` | Regenerate `45c`/`45d`/`45e`/`45f` from a source drop. Run `--ctors` FIRST on any new drop, before trusting anything else. |
| `scripts/mission.py sheet.json` | **Build a mission from its profile; do not decide it again.** Reads `48_DATA_mission_profiles.json` and a design sheet carrying only the creative half, and emits the quest, its enemies, its wired battle nodes and its art shots as one manifest. A sheet cannot reach a profile field. Refuses while any `AWAITING_RULING` slot remains for that rank, naming all of them at once. Pass `--spec 25x_DATA_art_spec.json` for the art half. |
| `scripts/enemy.py` | AI records from ratified role defaults. Rank is derived from level, never set: `USER_CAPS` clamps GENIN at 60k, so a level-45 enemy written GENIN passes every check and is gutted at combat time. Kits resolve from pool codes to literal ids. Refuses on unresolved level. |
| `scripts/profile_derive.py capture.json` | Turn a mission capture into a ratification table. Proposes, never writes. A field with no majority proposes NOTHING rather than averaging a bimodal population. |

`mission.py` needs `shotlist.py` from the **producing-tnr-art** skill for the art half. Both script
directories are put on the path automatically; if that skill is not installed, the manifest still
builds and the art half reports itself absent rather than failing silently.

`validate.py` and `factory.py` read `45c`, `45d` and `45g` from the working directory. Copy them in
before running, or pass `--ctors`, `--entities` and `--checks`.

**Prefer `factory.py` over hand-writing JSON.** Validation tells you a payload was wrong after you
wrote it; construction means you could not have written it wrong. Hand-authoring is for shapes the
factory does not cover yet, and those should be added to it rather than repeated.

`45g_DATA_checks.json` is the one config both this toolchain and the builder preflight read. If you
add a check to one side, add it to the other and re-run the parity test, or the browser will start
accepting things the container rejects.

## Engine laws

The laws live in `12_TECH_engine_laws.md` in project knowledge, deliberately outside this skill:
they are cited by the tools and by the state board, they change as the source is reconciled, and
they should be loadable without a build in flight. `12b_LAWS_coverage.md` says which laws
`validate.py` already catches and which ones you have to actually know.

Two that bite most often, stated with their reasons because the reason generalises and the rule
does not:

- **Editing a jutsu that an AI has equipped severs the combat link.** The sequence is unequip,
  save, edit, re-equip. A severed link and an inert AI rule produce an identical log signature, so
  when an AI is not using a jutsu, check the equip link before you start debugging rule grammar.
- **Effects do not apply on the round they are cast** (`damage`, `heal` and `pierce` excepted). The
  engine tags every effect with `castThisRound` and every consumer ignores effects carrying it. So
  a buff cast in the same turn as an attack never amplifies that attack, and a rule ordering a
  stance before its attacks gains nothing over ordering it after.

## Working style

The user is terse and action-first. Lead with the answer. At most one question per response — make
a reasonable assumption and state it rather than stalling. Propose and validate before presenting,
then action rulings into files immediately. For minor edits hand back only the changed files.


## Repo canon and lookups (2026-08-28)

The repo `perseverance484/tnr-tools` is the single source of truth for every tool, reference
and data file in this skill, under `/skills/building-tnr-content/`. Patches land there first;
the packaging workflow rebuilds the installable zip in `/dist/`. Never patch the installed
copy or ship tool patches in the session bundle.

Live-content lookups (name collision, id, what exists) fetch the repo answer layer:
`answers/INDEX.md` at the raw URL in the project instructions, then the entity answer file it
links. A capture beats any answer file. The enforcement matrix for the engine laws sits at
this skill's root as `12b_LAWS_coverage.md`; each reference carries its relocated law text in
a "Relocated engine laws" section, and the full numbered text is `/docs/ENGINE_LAWS.md` in
the repo.
