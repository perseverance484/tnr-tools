# DOCTRINE - the single source for cross-surface rules

Every rule that appears on more than one surface (mounted project instructions,
SKILL.md preambles, docs/00_INDEX.md) is defined here EXACTLY ONCE and rendered
outward by `scripts/render_doctrine.py`. Edit here; never edit a rendered block.
`doctrinemap.py` audits that every id is defined once and every reference
resolves; `render_doctrine.py --check` fails CI when a projection drifts.

Format per assertion: `### D-id`, a `targets:` line (which projections carry
it: mounted, skill-build, skill-art), an optional `short:` line (compact form
for the mounted paste; body used when absent), blank line, then the canonical
body. `[[D-id]]` elsewhere in docs is a reference, audited but not rendered.

### D-no-staging
targets: skill-build skill-art

TNR is a live browser game with no staging environment: a bad push lands on
players. Every rule in the mounted project instructions and in this block
exists because a push failed, or because a record went live wrong and someone
had to repair it by hand on a phone.

### D-doctrine-pointer
targets: skill-build skill-art

**Doctrine rides the mounted project instructions.** docs/DOCTRINE.md is the
single source; this block carries only what the mounted paste does not. If
this skill is ever run without the mounted instructions, read
docs/DOCTRINE.md before building anything.

### D-push-echo
targets: mounted
short: A push echo is not a read-back: verify per-entry json.success; state: ok with live: NONE is unverified. A filtered capture proves nothing.

**A push echo is not a read-back, and a filtered capture proves nothing.**
The server returns HTTP 200 on requests it did not honour. It strips fields it
does not recognise without complaint. It silently drops unresolvable
references. A manifest that "went through" tells you nothing about what is now
in the database - only a fresh read does. `state: ok` with `live: NONE` means
unverified; builder v4.28 reads back every write and `harvest.py verify` is
the gate that reads the verdicts.

### D-capture-first
targets: mounted
short: Extraction owns CONTRACTS (schemas, enums, constants, tRPC surface - from the game source). Capture-first owns LIVE STATE (law 83; record contents, runtime overrides). Never guess what either can answer.

**Capture first.** Read the live record and the schemas before composing
anything. Extraction owns CONTRACTS (what fields ARE); capture owns LIVE STATE
(what records HOLD) - law 83. Guessing a field shape is the single largest
source of failure in this project's history, and it is avoidable at zero cost.
If a contract is genuinely unconfirmed, ask for a capture rather than
inferring it.

### D-compose-generated
targets: mounted
short: Compose against generated files (45c/45d/45e/45g), never memory. factory.py constructs payloads.

**Compose against generated files, never memory.** `45c` holds every tagged
shape, `45d` every field and bound per entity, `45e` every engine constant,
`45f` the tRPC surface. They are generated from the game source and stamped
with provenance. When one disagrees with a reference file, the generated file
is right and the reference is stale. `factory.py` constructs payloads from
them; hand-authoring is the fallback.

### D-validate-always
targets: mounted
short: validate.py on every manifest before handover, zero errors, run from the skill data/ directory, and say what ran.

**Validate before handing anything over.** `python3 scripts/validate.py
manifest.json` must report zero errors, run from the skill `data/` directory,
and you say what you ran. Handing over an unvalidated manifest wastes a push
cycle on a phone, which is the user's scarcest resource. The validator now
carries the builder's L-lint layer, so a manifest that would be blocked at the
panel cannot validate clean.

### D-user-pushes
targets: mounted
short: dauntless taps Build in the builder panel - the ONLY act that touches the game. Claude pushes git, never the game.

**The user pushes.** Claude never pushes the game. The Build tap in the panel
is the only act that touches the game, by design; do not optimize the human
out of writes. Claude pushes git; results auto-commit to `harvests/inbox/`.

### D-verify-by-script
targets: mounted
short: Ids come from bundles or edit URLs by script, never transcribed or invented.

**Verify from the bundle, by script.** Extract ids programmatically; never
transcribe them from printed output. A truncated printout once put invented
ids into live reward tables. Absence claims must print the population scanned.

### D-build-order
targets: mounted
short: Build order: jutsu -> assets -> items -> ai -> aiProfile -> quest.

**Build order: `jutsu -> assets -> items -> ai -> aiProfile -> quest`.**
Each stage produces ids the next stage references. Building out of order means
composing references to records that do not exist yet, and unresolved
references are stripped silently rather than erroring - the AI stands there
with no jutsu equipped and nothing in the bundle says so.

### D-hidden-true
targets: mounted
short: Everything ships hidden: true. Publishing waits on the content admin's go-ahead, then dauntless publishes.

**Everything ships `hidden: true`.** Publishing is a separate, deliberate act
and it belongs to the user, never to you; it waits on the content admin's
go-ahead, then dauntless publishes. This applies to every entity on every
create.

### D-reserved-dauntless
targets: mounted
short: Balance and rewards are proposals only - drop rates, reward values, enemy counts, stat tuning, difficulty gates, exact percentages: carry placeholders and list every one in the delivery summary. Publishing, art direction, final acceptance, and ALL game pushes are dauntless's.

**Balance, rewards, rarity, art direction, publishing and final acceptance are
the user's to finalise.** Propose numbers, carry them as explicit
placeholders, and list every placeholder in the delivery summary. Do not
quietly settle a drop rate because a build needs one. Custom user-owned
bloodlines are never edited without a go-ahead.

### D-legendary-default
targets: mounted
short: Items default Legendary.

**Items default to Legendary rarity** unless told otherwise. Most of the
playerbase has outgrown Epic and below.

### D-riders-light
targets: mounted
short: Weapon riders stay light (one modest damage bucket; multiplicative stacking belongs to the player).

**Weapon riders stay light.** Damage stacks multiplicatively, so separate
small sources beat one large source; a weapon should carry at most one modest
damage bucket and let the player supply the stacking. Weapons cost only 40 AP
and deal guaranteed damage, so they are already strong.

### D-emdash-dialog
targets: mounted
short: Em dashes are banned in player-facing dialog text only (node description and choice text); fine everywhere else.

**No em dashes in player-facing dialog text** - a node's `description` and its
choice text. Commas, colons and hyphens instead. Everywhere else they are
fine. `validate.py` checks this (L11).

### D-pool-codes
targets: skill-build

**Pool codes over raw ids** when referring to shared AI records, so a renamed
record does not silently repoint.

### D-no-franchise
targets: mounted
short: TNR is open source: extract facts from it, never copy proprietary text, never reference the Naruto franchise.

**Never reference the Naruto franchise.** TNR is open source; extract facts
from the source, never copy proprietary text. This binds art prompts as hard
as it binds prose.

### D-no-real-name
targets: mounted
short: The real first name never appears in any artifact; the username is dauntless.

**The real first name never appears in any artifact of any kind** - no
deliverable, Discord post, doc, code comment, or manifest note. The username
is dauntless; write "per dauntless" or second person, no authority titles.

### D-adopt-gate
targets: mounted
short: A source drop or regen: schema_extract.py --ctors FIRST, then schema_diff.py --invariants and diff OLD NEW per file; adopt only on exit 0.

**Never adopt regenerated data without the mechanical gate.**
`schema_extract.py <src> --ctors` first, then `schema_diff.py --invariants`
on the fresh 45c and `schema_diff.py diff OLD NEW` per file; adopt only on
exit 0. The gate fail-closes on enum-member, variant and field removals and
type changes; the SECTOR_TYPES collision is the corruption class it exists
to stop.

### D-tool-canon
targets: mounted
short: Tool/skill/doc changes commit to the repo (/skills/ first; skillpack rebuilds /dist/); the container skill copy is never patched in place.

**The repo is canon for tools.** A tool, skill or doc change lands in the repo
`/skills/` tree first; the packaging workflow rebuilds `/dist/`; the container
skill copy is never patched in place.

### D-rebase-first
targets: mounted
short: ALWAYS git pull --rebase before every push - the workflows commit back [auto].

**Always `git pull --rebase` before every push.** The answers, skillpack and
sentinel workflows commit back `[auto]`; pushing without a rebase loses races
against them.

### D-working-style
targets: mounted
short: Terse and action-first. Lead with the answer, minimal preamble, at most one question per response; make a reasonable assumption and state it rather than stalling. Prefer the simplest tool already built; correct scope fast on redirect. Plans are approved before execution. For minor edits hand back only changed files. Own errors, and say what was checked before every handoff.

Terse and action-first. Lead with the answer, minimal preamble, at most one
question per response; make a reasonable assumption and state it rather than
stalling. Prefer the simplest tool already built; correct scope fast on
redirect. Plans are approved before execution. For minor edits hand back only
changed files. Own errors, and say what was checked before every handoff.
