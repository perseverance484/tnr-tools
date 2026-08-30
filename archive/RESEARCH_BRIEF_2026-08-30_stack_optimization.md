# RESEARCH BRIEF 2026-08-30 - TNR content-stack optimization

## Instructions to the researcher (read first)

You are running a deep-research pass over the tooling stack described below. You have web
access only. The repo `github.com/perseverance484/tnr-tools` is public; every internal fact
you need is inline in this brief, and the SOURCE MAP at the end gives one absolute raw URL
per file worth pulling. Fetch 10-20 of them to verify claims and read code; each fetch is
token-priced, sizes are listed, and your fetcher follows only URLs it is given - it cannot
mint or guess paths, so work from the map. Solutions that violate the HARD GATES section
are non-answers, however clever. Per weakness, answer the numbered research questions
with concrete, citation-backed findings (tools, patterns, prior art, measured
trade-offs), not general advice. The ranked shortlist is a proposal, not a ruling -
challenge its order if evidence says otherwise. Output one report; a separate
implementation-planning session consumes it.

## The system in one page

The Ninja RPG (TNR) is a live, open-source browser MMORPG (Next.js / tRPC / Drizzle,
source at `github.com/studie-tech/TheNinjaRPG`). dauntless, a content-staff contributor,
builds game content - jutsu, AI enemies, items, quests, art - with Claude as the
build/validate partner. There is **no staging environment**: a bad push lands on players.

The write path: Claude composes JSON manifests in a sandboxed Linux container (Python
stdlib only, allowlisted network), validates, commits them to `push/`, pushes git.
dauntless, on a Samsung phone (Firefox mobile + ViolentMonkey, no desktop), opens the game
with a userscript builder panel that lists `push/` and taps Build. The builder replays the
game's own tRPC API to create/edit records, resolves cross-references, uploads images,
then auto-commits a results bundle to `harvests/inbox/` via the GitHub contents API. An
Action regenerates the `answers/` lookup layer from harvests; Claude verifies from the
bundle by script. Publishing (unhiding) is a separate manual act gated on a content admin.

The repo is canon and memory in one: `/skills/` holds two installable Claude skills
(building-tnr-content, producing-tnr-art) with scripts, references and generated data;
`/docs/` holds the law corpus; `/answers/` the name/id lookup layer; `/state/` the session
board and handoff; `/push/` staged manifests; `/harvests/` captures and results;
`/archive/` prior art. Three workflows commit back to the repo (answers regen, privacy
scrub gate, skillpack rebuild). Sessions are stateless: every conversation starts by
cloning the repo and reading the handoff.

Key generated files (from the game source via `schema_extract.py`, provenance-stamped):
`45c` constructors (every tagged shape), `45d` entity schemas, `45e` constants, `45f` tRPC
surface, `45g` the shared check config that both `validate.py` (container) and the builder
preflight (browser) read. The law corpus: `docs/ENGINE_LAWS.md` is the numbered text of
record (93 laws); `12b_LAWS_coverage.md` classifies each law as validator-enforced vs
knowledge-only; `scripts/lawmap.py` cross-audits text, matrix and code citations.

## Measured baseline (audit session 2026-08-30)

Token estimates use bytes/4; tier source-verified unless marked.

| Surface | Bytes | ~Tokens | Notes |
|---|---|---|---|
| Mounted project instructions | ~5.6 KB | ~1.4 K | loaded every conversation turn 0 |
| userMemories block | ~9.5 KB | ~2.4 K | loaded every conversation; overlaps instructions heavily |
| SKILL.md x2 (content + art) | 19.2 KB | ~4.8 K | read at session start per mandate |
| Session ritual tool output | ~7 KB | ~1.8 K | observed this session: clone+state+verify, 4 calls |
| **Turn-one floor, working session** | **~41 KB** | **~10 K** | before any task file is opened |
| docs/00_INDEX.md + 10_LAWS_core.md | 12.8 KB | ~3.2 K | repo copies of doctrine (mounted text duplicates much of it) |
| docs/ENGINE_LAWS.md | 43.2 KB | ~10.8 K | read whole when law work happens |
| 12b_LAWS_coverage.md | 15.0 KB | ~3.7 K | |
| references/ total (10 files) | 273.6 KB | ~68 K | heaviest: ai.md 67.7 KB, quest.md 61.7 KB, pipeline.md 49.0 KB |
| Per-task read set: quest build | ~121.9 KB | ~30 K | SKILL + quest.md + pipeline.md |
| Per-task read set: AI build | ~127.8 KB | ~32 K | SKILL + ai.md + pipeline.md |
| Generated data (13 + 2 files) | 911 KB | n/a | script-read, never enters context - by design |
| builder_bundle.js | 96.2 KB | n/a | v4.27 live; loader 489 B |
| state/active-context.md + status.json | 7.7 KB | ~1.9 K | overlapping content, both hand-maintained |
| Repo clone | 4.0 MB work + 2.3 MB .git | n/a | 114 commits, 8 `[auto]` from workflows |
| harvests/ | seed 444 KB (5 catalogs) + inbox 52 KB (1 bundle) | n/a | answers/ generated 2026-08-30 01:25Z |

Push-loop interaction cost (observed from docs + panel design, per manifest): open game
tab, open panel, tap Repo list, select `push/N`, tap Build, wait, results auto-commit.
~5 taps steady-state. Bundle update adds: ViolentMonkey refresh (2-3 taps) plus a GitHub
blob-view check because raw CDN caches ~5 min and a fresh `?v` can still serve stale bytes.
Verification adds zero taps (inbox auto-commit) but a full read-back capture is a separate
manual panel action.

Law enforcement coverage (behaviour-proven this session): lawmap 93 laws, 70 code
citations, 0 errors, 5 warnings (laws 16d/37/69 claimed-enforced but no enforcing site
found; laws 18/61 cited in code but classed knowledge). validate.py on the staged manifest:
0 errors. Builder/validator parity vs the live acceptance bundle's own checks inventory:
16/16. 45g carries 18 check entries.

## Weaknesses

Format per item: statement / evidence (tier) / impact axis / current mitigation /
constraints on any solution / research questions (RQ).

### W1. Doctrine lives in four places and drifts

**Statement.** Working doctrine (workflow, precedence, reserved decisions, style) exists in
four independently edited homes: mounted project instructions, Claude's userMemories, the
two SKILL.md files, and repo `docs/` (00_INDEX, 10_LAWS_core). Content overlaps heavily
(hidden:true, build order, reserved-for-dauntless, working style each appear in 3+ places)
and versions drift.

**Evidence.** Bytes measured above (source-verified). Drift instances (observed): `references/pipeline.md` documents
"the current builder (v4.12)" while v4.27 is live; status.json still carries the
"paste instructions then delete project-knowledge copies" ruling while the mounted copy
is already live; commit `d3c4ba8` existed to reconcile one such fork.

**Impact.** Accuracy (a stale copy wins an argument it should lose) and token economy
(~6 K tokens of the turn-one floor is duplicate doctrine).

**Mitigation today.** 00_INDEX carries a precedence table; generated files beat prose by
rule; lawmap audits law text specifically. Nothing audits doctrine-vs-doctrine agreement.

**Constraints.** Mounted instructions and userMemories cannot fetch at load time - they are
static text pasted by dauntless; any "single source" still needs a paste step for those two
surfaces. Repo is public.

**RQ1.** What patterns exist for single-sourcing LLM operating instructions with generated
projections (one canonical doc -> rendered instruction paste, rendered SKILL preamble),
and what is the minimal stdlib tooling to diff the projections against canon in CI?
**RQ2.** Is there prior art on checksum/version pinning inside mounted-instruction text
("this paste is projection of docs/00_INDEX.md@<sha>") so a session can detect staleness
turn one at near-zero token cost?
**RQ3.** Can lawmap.py's cite-audit model extend to doctrine claims (grep-able assertion
ids in prose) without turning prose into a schema?

### W2. Session lifecycle is expensive and hand-carried

**Statement.** Every session pays clone + ritual + doctrine reads (~10 K tokens) before
work; close-out is hand-written prose (active-context.md) plus hand-edited JSON
(status.json) with overlapping content; handoff fidelity depends on the closing session's
discipline under a shrinking context budget.

**Evidence.** Turn-one floor measured (source-verified). The `0dca30d` incident: a
close-out `cp` from an unmounted path no-oped and only a manual read-back caught it
(observed). active-context.md and status.json restate each other's state line, blocked
list and open rulings (source-verified).

**Impact.** Token economy, throughput, and reliability of continuity.

**Mitigation today.** The ritual is short prose; verification re-runs make trust cheap;
closeout.py exists for bundle assembly. The archived ROLLOUT_PLAN's Stage 4 already
proposed `session_open.py`; it landed as prose ritual, not script.

**Constraints.** Container is ephemeral; state must round-trip through git; the board must
stay human-readable on a phone (dauntless reads status.json raw on GitHub mobile).

**RQ1.** For agent session persistence, what handoff schemas measurably survive
compaction best - single generated digest vs split board/narrative - and what field set is
the proven minimum (state line, verified-at-close runs, open items by owner, failure
modes)?
**RQ2.** What would a `session_open.py` / `session_close.py` pair look like that emits and
verifies one canonical digest (writing status.json and active-context.md as projections),
asserts write success by read-back, and costs <500 output tokens per end?
**RQ3.** Are shallow/sparse clones worth it at 6.3 MB repo scale, or is clone cost
already noise against the doctrine-read cost?

### W3. Schema regen is blocked and staleness is invisible

**Statement.** The 45x files are stamped at upstream `bdec2883` (2026-08-30). Their regen
automation (`regen_schemas.yml`) was rejected at push - the fine-grained PAT lacks
Workflows RW - so it exists nowhere, and nothing signals upstream drift; staleness is
found only when a push fails or a manual audit runs.

**Evidence.** status.json `blocked` quotes the rejection; provenance stamps in
45c/45e/45f; the 2026-08-30 source audit found accumulated true drift and adopted it
manually (all source-verified).

**Impact.** Accuracy - composing against a stale contract is this project's named largest
failure source.

**Mitigation today.** Manual: clone upstream, `--ctors` first, structural diff before
adopting. Proven when run; runs only when someone thinks to.

**Constraints.** GH Actions is the natural home (node allowed, network open there); the
container's allowlist does include github.com so in-session regen is possible but costs
session time; game pushes stay manual regardless - this is contract freshness only.

**RQ1.** Cheapest reliable upstream-drift sentinel: scheduled Action that clones upstream,
runs the extractor, and opens an issue/commits a `DRIFT.md` on hash change - what are the
rate/cost bounds and failure modes of that pattern on a solo free-tier repo?
**RQ2.** Risk assessment of adding Workflows RW to a fine-grained single-repo PAT vs the
one-time web-UI upload of the workflow file (after which contents RW suffices for edits) -
is there any reason the web-UI route was not simply taken?
**RQ3.** Should the sentinel diff at the *extracted artifact* level (45x output hash) rather
than upstream file level, so churn that does not change contracts stays silent?

### W4. Extractor adoption has no mechanical gate

**Statement.** Regenerated 45x files are adopted after a *human* structural diff. The gate
that caught the SECTOR_TYPES corruption (a global/local enum name collision in the
extractor that silently swapped a union's members) was discipline, not tooling.

**Evidence.** SOURCE_AUDIT "Extractor regression found and closed" (source-verified);
active-context lists it under failure-modes-to-watch (observed).

**Impact.** Accuracy, with the worst case being silent - a wrong enum ships into validate.py
and the builder, and both then *enforce* the corruption.

**Mitigation today.** `--ctors` first rule; stamped provenance; the manual diff.

**Constraints.** stdlib only in-container; the diff must be readable on a phone if it lands
in a workflow log.

**RQ1.** What does a minimal structural-diff gate look like for JSON contract files -
key-set + enum-member + union-arity deltas, fail-closed on removals - and is there prior
art (OpenAPI diff tools, buf breaking-change detection) whose rules map onto this shape?
**RQ2.** Which extractor invariants are worth property-testing (every discriminator
literal unique per union, every $ref resolvable, enum members sorted-stable) so the
extractor fails loudly instead of emitting plausible wrongness?

### W5. 23 of 93 laws are enforced only by prose

**Statement.** The law matrix classes a substantial minority of laws as `knowledge` -
correct behaviour depends on the model having read and retained them. The stacking and
calibration cluster (laws 9-13) is the largest such block. Five matrix rows are currently
untrustworthy (16d/37/69 claim enforcement nobody can find; 18/61 are enforced but
classed knowledge).

**Evidence.** lawmap this session: 93 laws, 70 citations, 5 warnings (behaviour-proven).
12b's Phase 3 section itself names 9-13 as "most worth turning into a simulator assertion"
(source-verified); knowledge-row count from the 12b matrix, split pending open reclasses.

**Impact.** Accuracy and reliability; knowledge laws are exactly the ones that fail under
context pressure late in a session.

**Mitigation today.** Laws relocated into the owning reference so they are read in task
context; lawmap makes the gap auditable; `calc.py` and `sim_damage.py` exist but assert
nothing law-shaped.

**Constraints.** Any new check must land in *both* validate.py and 45g (builder parity) or
the browser starts accepting what the container rejects; phone-side preflight has to stay
fast.

**RQ1.** For laws 9-13 specifically (multiplicative bucket stacking, same-type product
formula, pierce bypassing the floor, cast-round suppression): what is the smallest
simulator-assertion harness that turns each into a red/green check against `45e` constants,
and can it run as a validate.py mode rather than a new tool?
**RQ2.** What is the marginal cost curve of widening 45g - at what point does the browser
preflight's size/latency budget on Android Firefox bite, and is lazy-loading checks per
entity type in the userscript a known-good pattern?
**RQ3.** Is there prior art on "enforcement provenance" tables (rule id -> enforcing site,
CI-verified) in lint ecosystems worth copying wholesale for the 12b matrix?

### W6. Writes are verified by courtesy, not by construction

**Statement.** The server returns 200 on requests it did not honour, strips unknown
fields, and silently drops unresolvable references; `live: NONE` on a state:ok row means
*unverified*. The only proof is a fresh capture - a separate manual phone action - so the
default loop ships pushes whose landed state is unknown until someone spends taps.

**Evidence.** Skill doctrine states the classes (source-verified, SKILL.md); the board
holds a push in exactly this state pending an editor-crash fix (observed); staged
`push/6_verify_and_fix.json` exists precisely to make the read-back one tap.

**Impact.** Reliability - the failure is silent by design of the upstream API.

**Mitigation today.** Capture-first law; harvest.py; per-entry `json.success` + checks
inventory in bundles; verify-manifests as a pattern.

**Constraints.** tRPC replay is the only write path; read-backs are also tRPC calls, so the
builder *can* issue them; taps are the scarce resource; upstream is open source, so a PR
adding verbose write responses is theoretically on the table but outside this stack's
control and timeline.

**RQ1.** Cost/benefit of the builder auto-appending a read-back (`<entity>.get`) after
every write entry and diffing landed-vs-sent inside the results bundle - what does that do
to bundle size, run time on mobile, and rate-limit exposure on the game API?
**RQ2.** Which diff granularity catches the known silent classes (stripped field, dropped
reference, blanked field on partial edit) with the fewest false alarms - full-record
canonicalized diff, or a per-manifest "fields I asserted" checklist?
**RQ3.** Is there a pattern for *standing* verification - a tiny scheduled capture of
recently-touched ids whose results auto-commit like harvests - that stays inside the
manual-push doctrine because reads are not writes?

### W7. The builder distribution chain trusts a 5-minute-stale CDN

**Statement.** The userscript loads via `@require` from raw.githubusercontent.com (~5-min
cache); a version bump can serve old bytes, and the safeguard is a human ritual (blob-view
check, panel-title confirm). The doc describing this chain is itself stale (v4.12 vs
v4.27 live).

**Evidence.** pipeline.md lines on caching and blob-view verification (source-verified);
panel-title-as-load-check doctrine (source-verified); version drift observed.

**Impact.** Reliability (running a manifest against a stale bundle) and throughput (the
ritual costs taps every deploy).

**Mitigation today.** ViolentMonkey refresh button; panel shows version + cfg-generated
stamp; loader kept 489 B so it almost never changes.

**Constraints.** Android Firefox + ViolentMonkey only; no build step on the phone; the
allowlist note is container-side - the *browser* can reach api.github.com already (the
sync uses it).

**RQ1.** Can the bundle self-verify at load - fetch its own blob SHA via api.github.com
(unauthenticated, 60 req/h suffices) and warn in the panel title on mismatch - and what
are the failure modes of that pattern offline or rate-limited?
**RQ2.** Do jsDelivr-style CDNs with purge APIs or commit-pinned URLs
(`cdn.jsdelivr.net/gh/user/repo@<sha>/file`) work under ViolentMonkey `@require` on
Firefox Android, and would commit-pinned loading (loader rewritten per release by a
workflow) eliminate the staleness class outright?
**RQ3.** What keeps the doc honest - can skillpack.yml stamp the live builder version into
pipeline.md (generated header) so version drift in prose becomes impossible?

### W8. The push loop is ~5 taps that only dauntless can spend

**Statement.** Every manifest costs a fixed phone interaction serialized through one
person - a deliberate gate on *writes*, but the same tap-price is paid for free probes,
captures and re-runs, and there is no batching beyond "one file per Build".

**Evidence.** Loop steps counted from panel design + pipeline doctrine (observed); the
board phrases a pending verification as "when Terr clears **or as free probe**" - probes
compete for the same taps (source-verified).

**Impact.** Throughput; also latency of verification (W6) since reads ride the same loop.

**Mitigation today.** Manifests are numbered and queued in `push/`; results auto-commit
removes the old upload step entirely (proven zero-touch loop).

**Constraints.** Manual game pushes are doctrine, not debt - solutions must preserve a
human tap per *write* batch. Reads are not writes.

**RQ1.** Multi-manifest Build (select several `push/` files, one confirmation, sequential
run with a combined bundle): what ordering, failure-isolation and resume semantics do
comparable batch-replay tools use, and what is the minimal UI for it in a userscript panel?
**RQ2.** Given W6-RQ3, can pure-read capture manifests be exempted from the one-tap rule
via a separate always-allowed panel action without eroding the write gate?

### W9. The lookup layer is fresh only by accident of the last harvest

**Statement.** `answers/` regenerates on harvest push and is stamped, but consumers see
row-level facts with no per-row freshness, and nothing schedules harvests - so the layer's
accuracy decays at the rate other staff edit the game, invisibly. Inbox retention is
likewise unpoliced (1 bundle now; nothing says what happens at 50).

**Evidence.** answers/INDEX.md header carries the stamp and the "fresher takes a capture"
rule (source-verified); answers.yml triggers only on harvest paths (source-verified); seed
corpus is a point-in-time 444 KB from 2026-08 (observed).

**Impact.** Accuracy (name-collision and id lookups against stale rows) and data retention
(inbox growth vs the deliberate bundle-diet doctrine).

**Mitigation today.** Capture-beats-answers precedence; dedup-against-answers is doctrine;
the 5-min CDN note is printed at the top of INDEX.

**Constraints.** Harvests cost taps (W8); planned Stage 4.5 sharding (per-pool + hot
shard) is prior art to build on; fetch-only consumers mean shard size prices into tokens.

**RQ1.** Freshness surfacing: what per-shard metadata (source stamp, age-at-generation,
row count delta) lets a consumer decide "capture or trust" in one fetch, and where does it
live so INDEX stays one small file?
**RQ2.** Retention policy for harvests/inbox that preserves audit history without repo
bloat - is generation-based squashing (keep latest N, roll older into seed) sound when
answers/ is a pure function of harvests?
**RQ3.** For the shard layout, what naming scheme keeps single-entity lookups to exactly
two fetches (INDEX -> shard) for a fetcher that cannot glob?

### W10. Credential surface: one PAT in pasted prose, one token in a panel

**Statement.** A fine-grained PAT (contents RW, single repo) travels as plaintext in the
mounted instructions every session; the panel's sync token is hand-entered (ViolentMonkey
storage; verified absent from the bundle). Rotation for either is undefined. The repo is
public, so a slipped string is world-readable, and the scrub workflow gates on exactly one
secret and *warns* rather than fails when unset.

**Evidence.** Bundle greps 0 hits for the PAT pattern; scrub.yml behaviour read
(source-verified). PAT-in-instructions is the current mount's design (observed).

**Impact.** Reliability/security. Blast radius today is bounded (one repo, contents-only)
but the exposure channel repeats every session.

**Mitigation today.** Fine-grained scoping; scrub gate; doctrine that the PAT never
appears in artifacts (this brief complies).

**Constraints.** The container receives secrets *only* via pasted instruction text - there
is no secret store on that path; the phone side has ViolentMonkey storage; Actions has
proper secrets.

**RQ1.** Given the paste-only channel, what actually reduces risk: shorter-lived PATs on a
rotation ritual, a second write-only PAT for the panel distinct from the container's, or
moving all container git writes behind a workflow_dispatch relay (container pushes to a
branch, Action with repo-scoped GITHUB_TOKEN merges)?
**RQ2.** Should scrub.yml fail-closed when SCRUB_STRING is unset and take a list (both
tokens, any future ones), and what is the standard pattern for multi-secret scrub gates?

### W11. Heavyweight references price accuracy against tokens

**Statement.** Correct builds require the owning reference (ai.md 67.7 KB, quest.md
61.7 KB) plus pipeline.md (49 KB); relocating law text *into* these files - the accuracy
fix for W5 - inflated per-task cost to ~30 K tokens before composing begins, and with no
section-level retrieval a task needing one paragraph pays for the whole file.

**Evidence.** Sizes measured (source-verified); read-the-owner doctrine and the relocation
rationale in 12b ("a law that must be read should live next to the workflow")
(source-verified).

**Impact.** Token economy, and indirectly accuracy late in long sessions (context pressure
evicts exactly the prose W5 depends on).

**Mitigation today.** The table-of-owners stops whole-corpus reads; data files never enter
context; answers/ offloads lookups.

**Constraints.** References must stay single files for skill packaging and human editing;
any split must keep the "read the one that owns the task" rule simple.

**RQ1.** Measured techniques for section-addressable docs in agent stacks - stable anchor
ids + a generated per-file TOC-with-byte-offsets, so a session can `sed`-range or
web_fetch-then-slice instead of whole-file reads: what granularity pays off at these file
sizes?
**RQ2.** Would a generated "task packs" layer (build-type -> concatenated minimal excerpt
set, rebuilt by skillpack.yml) beat section retrieval on both tokens and reliability,
given packs can be regenerated whenever canon changes?
**RQ3.** What is the right budget instrument - a per-session token ledger emitted at close
(files read x sizes) so this cost stays measured instead of vibed?

### W12. Art loop depends on an external generator and a lying preview

**Statement.** Generation is external (ChatGPT) with known systematic failure shapes;
the game's asset editor previews everything through a square widget, so non-square art is
judged only via the local dark composite; acceptance hit-rate is untracked, so scaffold
quality cannot improve on evidence.

**Evidence.** producing-tnr-art SKILL.md unprocessable-failures list and preview-lie note
(source-verified); one wrong re-export already attributed to the preview (source-verified);
one-at-a-time rhythm is ratified doctrine (source-verified).

**Impact.** Throughput (regeneration cycles) and accuracy of what ships.

**Mitigation today.** Spec-driven chroma.py/artpreflight.py (38/38 selftest), raw-QC
reject checklist, reference-image escalation after 3 failed re-descriptions
(proposed, unruled).

**Constraints.** Generator choice, art direction and acceptance are dauntless's; QC code
is stdlib-only (chroma.py already lives within that).

**RQ1.** Which raw-QC checks are mechanizable pre-processing within stdlib-image limits
(flat-field chroma coverage %, edge-halo detection, aspect sanity) so rejects cost zero
human looks?
**RQ2.** What is the minimal hit-rate ledger (prompt-scaffold id -> accept/reject/reason)
that turns scaffold editing into an evidence-driven loop, and where does it live so
shotlist.py can read it?

## Ranked shortlist (proposal, not ruling)

1. **W6 read-back verification in the builder** - kills the largest silent-failure class.
2. **W3+W4 regen sentinel + mechanical adoption gate** - top failure source, zero automation.
3. **W1+W7-doc single-sourcing with generated projections** - drift observed; compounds all.
4. **W2 session_open/close pair** - direct ~10 K-token/session + handoff-fidelity win.
5. **W11 section-addressable references or task packs** - biggest per-task token lever.
6. **W5 simulator assertions for laws 9-13 + parity widening** - accuracy tail.
7. **W9 shard + freshness metadata** - cheap lookups for fetch-only consumers.
8. **W8 batch Build + free reads** - pure throughput, small UI change.
9. **W10 credential rotation/relay** - bounded today, cheap to harden.
10. **W12 art QC mechanization + hit-rate ledger** - valuable, most decoupled.

## Hard gates (solutions MUST respect)

- Phone side: Android Firefox + ViolentMonkey userscripts only. No desktop, ever. DOM via
  createElement/CSSOM, no innerHTML.
- Container side: Python stdlib only; network limited to an allowlist (github,
  raw.githubusercontent, pypi, npm, api.anthropic, ubuntu mirrors). Ephemeral filesystem.
- CI side: GitHub Actions may use node; free-tier budgets.
- No staging environment exists or will.
- Solo maintainer, on a phone; operating cost is measured in taps and small-screen
  readability.
- tRPC replay through the builder is the ONLY game write path; pushes stay manual and
  human-initiated **by design** - do not optimize the human out of writes.
- The repo is public: no secrets in any committed artifact; raw CDN ~5-min staleness is a
  fact to design around.
- Publishing (unhiding) waits on the content admin; balance/reward numbers are proposed,
  never settled, by tooling.

## SOURCE MAP

Raw first (immediate, ~5-min CDN cache); blob fallback pattern:
`https://github.com/perseverance484/tnr-tools/blob/main/<path>`. Sizes to budget fetches.

```
https://raw.githubusercontent.com/perseverance484/tnr-tools/main/docs/00_INDEX.md                                    7 KB   router + precedence table (W1)
https://raw.githubusercontent.com/perseverance484/tnr-tools/main/docs/10_LAWS_core.md                                6 KB   cross-cutting laws (W1)
https://raw.githubusercontent.com/perseverance484/tnr-tools/main/docs/ENGINE_LAWS.md                                43 KB   numbered law text of record (W5)
https://raw.githubusercontent.com/perseverance484/tnr-tools/main/docs/SOURCE_AUDIT_2026-08-30.md                     4 KB   extractor regression + drift adoption + wedge (W3,W4)
https://raw.githubusercontent.com/perseverance484/tnr-tools/main/skills/building-tnr-content/SKILL.md               11 KB   workflow doctrine, silent-failure classes (W6)
https://raw.githubusercontent.com/perseverance484/tnr-tools/main/skills/building-tnr-content/12b_LAWS_coverage.md   15 KB   enforcement matrix + Phase 3 plan (W5)
https://raw.githubusercontent.com/perseverance484/tnr-tools/main/skills/building-tnr-content/references/pipeline.md 49 KB   push/verify plumbing, CDN ritual, v4.12 drift exemplar (W6,W7)
https://raw.githubusercontent.com/perseverance484/tnr-tools/main/skills/building-tnr-content/references/ai.md       68 KB   heaviest reference; fetch only to gauge W11 shape
https://raw.githubusercontent.com/perseverance484/tnr-tools/main/skills/building-tnr-content/scripts/validate.py            preflight + --parity implementation (W5,W6)
https://raw.githubusercontent.com/perseverance484/tnr-tools/main/skills/building-tnr-content/scripts/factory.py             construct-not-author layer (W5)
https://raw.githubusercontent.com/perseverance484/tnr-tools/main/skills/building-tnr-content/scripts/lawmap.py              law/code cross-audit (W1-RQ3, W5)
https://raw.githubusercontent.com/perseverance484/tnr-tools/main/skills/building-tnr-content/scripts/schema_extract.py      extractor under audit (W3,W4)
https://raw.githubusercontent.com/perseverance484/tnr-tools/main/skills/building-tnr-content/scripts/harvest.py             bundle -> catalog rows (W6,W9)
https://raw.githubusercontent.com/perseverance484/tnr-tools/main/skills/building-tnr-content/data/45g_DATA_checks.json 21 KB shared check config, parity surface (W5)
https://raw.githubusercontent.com/perseverance484/tnr-tools/main/skills/building-tnr-content/data/45d_DATA_entity_schemas.json 41 KB entity contracts (W4)
https://raw.githubusercontent.com/perseverance484/tnr-tools/main/skills/producing-tnr-art/SKILL.md                   8 KB   art doctrine, preview lie (W12)
https://raw.githubusercontent.com/perseverance484/tnr-tools/main/skills/producing-tnr-art/scripts/artpreflight.py           art acceptance checker (W12)
https://raw.githubusercontent.com/perseverance484/tnr-tools/main/skills/producing-tnr-art/data/25x_DATA_art_spec.json 44 KB per-target art authority (W12)
https://raw.githubusercontent.com/perseverance484/tnr-tools/main/builder_bundle.js                                  96 KB   the userscript panel v4.27 (W6,W7,W8)
https://raw.githubusercontent.com/perseverance484/tnr-tools/main/builder_loader_user.js                             0.5 KB  @require loader (W7)
https://raw.githubusercontent.com/perseverance484/tnr-tools/main/state/active-context.md                             3 KB   handoff narrative (W2)
https://raw.githubusercontent.com/perseverance484/tnr-tools/main/state/status.json                                   5 KB   board incl. blocked regen entry (W2,W3)
https://raw.githubusercontent.com/perseverance484/tnr-tools/main/answers/INDEX.md                                    2 KB   lookup layer + stamps (W9)
https://raw.githubusercontent.com/perseverance484/tnr-tools/main/.github/workflows/answers.yml                       1 KB   regen trigger scope (W9)
https://raw.githubusercontent.com/perseverance484/tnr-tools/main/.github/workflows/scrub.yml                         1 KB   privacy gate, warn-if-unset (W10)
https://raw.githubusercontent.com/perseverance484/tnr-tools/main/.github/workflows/skillpack.yml                     1 KB   pack rebuild loop (W1,W11)
https://raw.githubusercontent.com/perseverance484/tnr-tools/main/archive/ROLLOUT_PLAN.md                             8 KB   prior restructure art - do NOT re-derive stages (W2,W11)
https://raw.githubusercontent.com/perseverance484/tnr-tools/main/harvests/inbox/tnr_results_1788053115846.json      52 KB   live acceptance bundle w/ checks inventory (W6)
```

*Brief authored session 2026-08-30 (audit, session 1 of 3). Zero game touches. All numbers
measured in-session; tiers marked inline.*
