---
name: building-tnr-content
description: Builds and validates content for The Ninja RPG (TNR) - jutsu, AI enemies, items, quests and events - as builder manifests pushed through the hosted userscript. Use this skill whenever the user asks to create, edit, balance, audit or push TNR content, whenever a results bundle or capture is uploaded for verification, and whenever a manifest, engine law, pool code or entity id is mentioned, even if they do not name the skill or ask for a manifest explicitly.
---

# Building TNR content

## Doctrine (rendered)

<!-- doctrine:begin @17d6a71 target=skill-build - RENDERED from docs/DOCTRINE.md; edit there, then render_doctrine.py --write -->

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

## Picking a reference

Packs first. A jutsu, AI or quest build that ends in a push reads its pack — the curated
excerpt set with its pipeline sections already inlined. Depth on demand: slice one section by
byte range via `references/_toc/<name>.json` instead of reading a whole reference. The full
references are for deep dives and for editing (packs re-render from them).

| Working on | Read |
|---|---|
| Jutsu build/edit that pushes | `packs/jutsu-build.md` |
| AI enemy build/edit that pushes | `packs/ai-build.md` |
| Quest/event build/edit that pushes | `packs/quest-build.md` |
| Items, weapons, loot chests, crafting | `references/item.md` + pipeline sections via `_toc` |
| Tuning numbers, tiering, reward scale | `references/balance.md` |
| Processing a submitted staff design sheet into a whole event | `references/event.md` |
| Reusable enemy lines (Unsigned, Verge, Forsworn) | `references/lines.md` |
| Push mechanics outside a pack (capture, image upload, combined manifest) | `references/pipeline.md` or a `_toc` slice |

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

The numbered text of record is `docs/ENGINE_LAWS.md` in the repo, deliberately outside this
skill: the laws are cited by the tools and the state board and change as the source is
reconciled. Grep it by law number; never read it whole. `12b_LAWS_coverage.md` at this skill's
root says which laws `validate.py` already catches and which ones you have to actually know;
each reference and pack carries its relocated law text.

Two that bite most often, stated with their reasons because the reason generalises and the rule
does not:

- **Editing a jutsu that an AI has equipped severs the combat link.** The sequence is unequip,
  save, edit, re-equip. A severed link and an inert AI rule produce an identical log signature, so
  when an AI is not using a jutsu, check the equip link before you start debugging rule grammar.
- **Effects do not apply on the round they are cast** (`damage`, `heal` and `pierce` excepted). The
  engine tags every effect with `castThisRound` and every consumer ignores effects carrying it. So
  a buff cast in the same turn as an attack never amplifies that attack, and a rule ordering a
  stance before its attacks gains nothing over ordering it after.

## Lookups

Live-content lookups (name collision, id, what exists) fetch the repo answer layer:
`answers/INDEX.md` at the raw URL in the project instructions, then the entity answer file it
links. A capture beats any answer file. Working style, repo canon and the push loop are in the
mounted instructions; this file never restates them.
