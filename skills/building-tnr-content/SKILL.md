---
name: building-tnr-content
description: Builds and validates content for The Ninja RPG (TNR) - jutsu, AI enemies, items, quests and events - as builder manifests pushed through the hosted userscript. Use this skill whenever the user asks to create, edit, balance, audit or push TNR content, whenever a results bundle or capture is uploaded for verification, and whenever a manifest, engine law, pool code or entity id is mentioned, even if they do not name the skill or ask for a manifest explicitly.
---

# Building TNR content

## Doctrine (rendered)

<!-- doctrine:begin @6246ee3 target=skill-build - RENDERED from docs/DOCTRINE.md; edit there, then render_doctrine.py --write -->

TNR is a live browser game with no staging environment: a bad push lands on
players. Every rule below exists because a push failed, or because a record
went live wrong and someone had to repair it by hand on a phone.

**A push echo is not a read-back, and a filtered capture proves nothing.**
The server returns HTTP 200 on requests it did not honour. It strips fields it
does not recognise without complaint. It silently drops unresolvable
references. A manifest that "went through" tells you nothing about what is now
in the database - only a fresh read does. `state: ok` with `live: NONE` means
unverified; builder v4.28 reads back every write and `harvest.py verify` is
the gate that reads the verdicts.

**Capture first.** Read the live record and the schemas before composing
anything. Extraction owns CONTRACTS (what fields ARE); capture owns LIVE STATE
(what records HOLD) - law 83. Guessing a field shape is the single largest
source of failure in this project's history, and it is avoidable at zero cost.
If a contract is genuinely unconfirmed, ask for a capture rather than
inferring it.

**Compose against generated files, never memory.** `45c` holds every tagged
shape, `45d` every field and bound per entity, `45e` every engine constant,
`45f` the tRPC surface. They are generated from the game source and stamped
with provenance. When one disagrees with a reference file, the generated file
is right and the reference is stale. `factory.py` constructs payloads from
them; hand-authoring is the fallback.

**Validate before handing anything over.** `python3 scripts/validate.py
manifest.json` must report zero errors, run from the skill `data/` directory,
and you say what you ran. Handing over an unvalidated manifest wastes a push
cycle on a phone, which is the user's scarcest resource. The validator now
carries the builder's L-lint layer, so a manifest that would be blocked at the
panel cannot validate clean.

**The user pushes.** Claude never pushes the game. The Build tap in the panel
is the only act that touches the game, by design; do not optimize the human
out of writes. Claude pushes git; results auto-commit to `harvests/inbox/`.

**Verify from the bundle, by script.** Extract ids programmatically; never
transcribe them from printed output. A truncated printout once put invented
ids into live reward tables. Absence claims must print the population scanned.

**Build order: `jutsu -> assets -> items -> ai -> aiProfile -> quest`.**
Each stage produces ids the next stage references. Building out of order means
composing references to records that do not exist yet, and unresolved
references are stripped silently rather than erroring - the AI stands there
with no jutsu equipped and nothing in the bundle says so.

**Everything ships `hidden: true`.** Publishing is a separate, deliberate act
and it belongs to the user, never to you; it waits on the content admin's
go-ahead, then dauntless publishes. This applies to every entity on every
create.

**Balance, rewards, rarity, art direction, publishing and final acceptance are
the user's to finalise.** Propose numbers, carry them as explicit
placeholders, and list every placeholder in the delivery summary. Do not
quietly settle a drop rate because a build needs one. Custom user-owned
bloodlines are never edited without a go-ahead.

**Items default to Legendary rarity** unless told otherwise. Most of the
playerbase has outgrown Epic and below.

**Weapon riders stay light.** Damage stacks multiplicatively, so separate
small sources beat one large source; a weapon should carry at most one modest
damage bucket and let the player supply the stacking. Weapons cost only 40 AP
and deal guaranteed damage, so they are already strong.

**No em dashes in player-facing dialog text** - a node's `description` and its
choice text. Commas, colons and hyphens instead. Everywhere else they are
fine. `validate.py` checks this (L11).

**Pool codes over raw ids** when referring to shared AI records, so a renamed
record does not silently repoint.

**Never reference the Naruto franchise.** TNR is open source; extract facts
from the source, never copy proprietary text. This binds art prompts as hard
as it binds prose.

**The real first name never appears in any artifact of any kind** - no
deliverable, Discord post, doc, code comment, or manifest note. The username
is dauntless; write "per dauntless" or second person, no authority titles.

**Never adopt regenerated data without the mechanical gate.**
`schema_extract.py <src> --ctors` first, then `schema_diff.py --invariants`
on the fresh 45c and `schema_diff.py diff OLD NEW` per file; adopt only on
exit 0. The gate fail-closes on enum-member, variant and field removals and
type changes; the SECTOR_TYPES collision is the corruption class it exists
to stop.

**The repo is canon for tools.** A tool, skill or doc change lands in the repo
`/skills/` tree first; the packaging workflow rebuilds `/dist/`; the container
skill copy is never patched in place.

**Always `git pull --rebase` before every push.** The answers, skillpack and
sentinel workflows commit back `[auto]`; pushing without a rebase loses races
against them.

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
