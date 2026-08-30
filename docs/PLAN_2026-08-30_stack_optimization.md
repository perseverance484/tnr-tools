# PLAN 2026-08-30 - TNR content-stack optimization (Session 3 of 3)

Consumes: archive/RESEARCH_BRIEF_2026-08-30_stack_optimization.md (W1-W12, HARD GATES)
and archive/RESEARCH_REPORT_2026-08-30_stack_optimization.md (answers + re-ranked
shortlist). This plan follows the report's re-ranked order; every deviation is stated
inline. No execution happened this pass. Guards at plan time: lawmap 93 laws / 0
errors / 5 known warnings; validate.py push/6 0/0; --parity 16/16 vs
harvests/inbox/tnr_results_1788053115846.json.

## Ground rules the whole plan obeys

- **HARD GATES are absolute.** Phone = Android Firefox + ViolentMonkey, createElement/
  CSSOM only. Container = Python stdlib only. Actions may use node. No staging. Writes
  stay manual and human-initiated; reads are not writes. Public repo, no secrets in
  artifacts. ~5-min raw-CDN staleness is designed around. Nothing below violates these;
  two report items that brushed gates (jsDelivr third-party CDN, read-only tap
  exemption) are re-scoped as rulings, not steps.
- **Staged-workflow convention (new, forced by the PAT).** The tnr-container PAT has
  contents-RW only; any push touching `.github/workflows/` is rejected (proven at
  regen_schemas.yml). Therefore every workflow create/edit in this plan is AUTHORED by
  the container at `state/staged_workflows/<name>.yml` and INSTALLED by dauntless in
  one browser session (web UI commit rides the browser session, not the PAT). One
  upload batch covers all staged files. Never add Workflows-RW to the container PAT
  (report W3-RQ2/W10).
- **Builder releases are batched.** Each release costs dauntless a ViolentMonkey
  refresh + panel-title check, so panel-side work rides exactly two releases: v4.28
  (Wave 1) and v4.29 (Wave 3).
- **Everything ships hidden; balance numbers stay placeholders;** any smoketest write
  is a minimal hidden entity behind one manual Build tap.

## Work orders

### WO-01 - W6 read-back verification in the builder (shortlist #1)
**Scope.** After every write entry, the builder issues the matching `<entity>.get`
read-back and records a verdict against the fields the manifest asserted. Upgrades
`live: NONE` from "unverified" to a landed-state snapshot. Rider (stated deviation):
W7-RQ1 blob-SHA self-verify ships in the same release - both are panel code and one
refresh instead of two.
**Files/tools.** `builder_bundle.js` + `builder_loader_user.js` (v4.28);
`skills/building-tnr-content/scripts/harvest.py` (parse readback blocks);
`skills/building-tnr-content/scripts/pushpack.py` (carry asserted-field lists);
new manifest `push/7_readback_smoke.json` (one hidden minimal entity, create+edit).
**Build steps.** (1) Builder computes per-entry `asserted_fields` from the manifest
payload at Build time. (2) After the write pass completes, batch the read-backs
(sequential GETs after all writes, not interleaved - mobile cost). (3) Attach
`{readback, verdict:{asserted, missing, blanked, unresolved_refs}}` per entry to the
results bundle. (4) Panel init fetches its own blob SHA via contents API, compares to
the built-in SHA; mismatch = warning in the panel title; offline/rate-limited = fail
OPEN with "unverified" note, never block; cache result per session (60/h unauth IP
budget shared with sync). (5) harvest.py normalizes verdicts; a verdict with missing/
blanked/unresolved entries prints as FAIL lines.
**Verification.** Container: harvest.py selftest extended with a fixture bundle
carrying one clean and one mismatched verdict (red/green). Live acceptance: one Build
tap on push/7; bundle auto-commits to inbox; harvest.py shows per-entry verdicts;
panel title shows `v4.28 · cfg generated` + SHA state.
**Acceptance.** Verdict blocks present for 100% of write entries; seeded mismatch
fixture FAILS; clean smoketest passes; blanked-field class (law: partial quest edits
blank fields) demonstrably caught by the checklist.
**Effort.** Med. **Deps.** None. Read-backs are reads - no ruling needed.

### WO-02 - W3 upstream-drift sentinel, authored + staged (shortlist #2a)
**Scope.** Scheduled Action that clones the public game source, runs the extractor,
hashes the 45x artifacts, and commits `DRIFT.md` + updates `state/schema_sentinel.json`
on change. Diff at the extracted-artifact level, not upstream files (report W3-RQ3):
refactors stay silent, contract changes ring.
**Files/tools.** New `state/staged_workflows/regen_schemas.yml` (cron `17 6 * * *` +
`workflow_dispatch`; off-hour minute and manual trigger per documented cron-delay
mitigations; auto-commit via the same idiom answers.yml uses). New
`skills/building-tnr-content/scripts/sentinel_hash.py` (stdlib: canonical-serialize +
sha256 the extractor outputs) so the Action body stays a thin caller.
**Build steps.** Author both files; local dry-run in the container: clone
`studie-tech/TheNinjaRPG` (allowlisted), run `schema_extract.py --ctors`, run
sentinel_hash.py, write the baseline `state/schema_sentinel.json`.
**Verification.** Local dry-run produces a stable hash across two runs (determinism);
structural-diff of dry-run 45c vs shipped 45c is empty at current HEAD (or
differences are listed, never adopted - adoption is WO-03's gate). Post-install:
dauntless triggers `workflow_dispatch`; first run commits the baseline; freshness is
hours-not-minutes and that is acceptable because game pushes stay manual.
**Acceptance.** Dry-run hash stable; staged YAML lints (`python3 -c` yaml via
stdlib?? no - visual + Action first-run is the lint); after install, one dispatch run
commits back cleanly.
**Effort.** Low. **Deps.** RULING: one-time web-UI workflow upload (batch).

### WO-03 - W4 mechanical adoption gate (shortlist #2b)
**Scope.** No regenerated 45x file is adopted without passing a fail-closed
structural diff plus extractor invariants. Kills the SECTOR_TYPES silent-corruption
class (same arity, swapped enum member).
**Files/tools.** New `skills/building-tnr-content/scripts/schema_diff.py` (stdlib
json + set algebra). Extractor invariant selftest added to `schema_extract.py
--selftest`. Fixtures under `skills/building-tnr-content/data/fixtures/` (synthetic
pairs; no game text). `docs/00_INDEX.md` routing row: regen adoption = extract ->
--selftest -> schema_diff old new -> adopt only on exit 0.
**Build steps.** schema_diff rules (json-schema-diff-validator shape): BREAKING =
enum member removed (compare member SETS BY VALUE, never counts), union arity
shrink, required-key removal, type change -> exit 1; additive = listed, exit 0;
output = phone-readable ADDITIONS/REMOVALS. Invariants: every discriminator literal
unique within its union; every cross-reference resolves; enums emitted sorted-stable.
**Verification.** Red/green fixture suite: SECTOR_TYPES-class pair (swapped member,
same arity) MUST exit 1; additive pair MUST exit 0; ref-broken and dup-discriminator
fixtures fail --selftest. Run against live: schema_diff current-45c current-45c = 0.
**Acceptance.** All fixtures behave; adoption flow documented; selfcheck.py green.
**Effort.** Med. **Deps.** None (composes with WO-02: sentinel says "changed", gate
says "what and whether adoptable").

### WO-04 - W1+W7-doc single-sourcing with generated projections (shortlist #3)
**Scope.** Doctrine gets one source and rendered projections; drift becomes a CI
failure instead of a reading-comprehension task. Includes W7-RQ3: pipeline.md can no
longer lie about the builder version.
**Files/tools.** New `docs/DOCTRINE.yml` (assertions with stable ids `[[D-...]]`,
canonical text; 00_INDEX.md stays the router and gains the id anchors). New
`skills/building-tnr-content/scripts/render_doctrine.py` (emits (a)
`state/mounted_instructions.txt` paste block with first-line
`<!-- projection of docs/DOCTRINE.yml@<sha7> rendered <ISO8601> -->`, (b) SKILL.md
preamble blocks between markers; `--check` mode re-renders to temp and
difflib.unified_diff's against committed projections, exit 1 on delta). New
`skills/building-tnr-content/scripts/doctrinemap.py` (lawmap sibling: every id
defined exactly once, every cross-ref resolves). Staged patch
`state/staged_workflows/skillpack.yml` adding two steps: `render_doctrine.py --check`
and a pipeline.md generated header stamping the live builder version read from
builder_bundle.js.
**Build steps.** Extract the ~6K duplicated doctrine into DOCTRINE.yml; render;
replace duplicated blocks in SKILL.md preambles with rendered blocks; commit
projections; wire --check.
**Verification.** `render_doctrine.py --check` = zero delta on clean tree; a
deliberate one-word drift fixture exits 1; doctrinemap 0 errors; lawmap still
93/0e/5w (law stack untouched).
**Acceptance.** Mounted-paste block regenerated with sha7 header (dauntless
re-pastes at leisure - detect-not-autoheal is the honest ceiling); duplicate doctrine
token floor removed from always-loaded surfaces.
**Effort.** Med. **Deps.** Staged skillpack patch rides the upload batch; the
render/check tooling works container-side immediately regardless.

### WO-05 - W2 session_open/close pair + digest (shortlist #4)
**Scope.** One generated digest is the session state; status.json and
active-context.md become projections of it; close-out is read-back-asserted (kills
the 0dca30d silent no-op class). Includes W11-RQ3's token ledger as a digest field.
Clone optimization is explicitly SKIPPED (report: noise at 6.3 MB).
**Files/tools.** New `skills/building-tnr-content/scripts/session_close.py` and
`session_open.py`. New `state/digest.json` (schema: state_line, touched,
decisions+rationale, in_progress, constraints, next, open_by_owner, rulings_open,
token_ledger[files x bytes read]). status.json keeps its board shape but is written
by the projector; active-context.md likewise.
**Build steps.** close: assemble digest -> project both files -> re-read all three
-> byte-assert -> print the one-line state. open: read digest, print state line +
rulings_open, run the verify trio (lawmap, validate on the file under work, --parity
vs newest inbox bundle), print verdicts, propose next.
**Verification.** Round-trip selftest: close into a temp tree, open from it,
byte-equality + state-line match; a seeded projection mismatch makes close exit 1.
**Acceptance.** Next real session opens via session_open.py with <500 emitted
tokens for the ritual; handoff fields match the ESAA minimum set; ledger populates.
**Effort.** Med. **Deps.** Soft on WO-04 (ritual text becomes doctrine-rendered);
runs fine before it with one manual doctrine sync.

### WO-06 - W8 batch Build + free-read capture action (shortlist #5, RAISED 8->5 by report)
**Scope.** One confirmation tap runs an ordered batch of push/ manifests with
per-entry isolation and resume; a separate read-only capture action stops probes
competing for write taps. Report's re-rank reason honored: this is the delivery
vehicle that makes WO-01's verification affordable in taps.
**Files/tools.** `builder_bundle.js` (v4.29): multi-select checklist over the
existing Repo-list of push/, topological order via the existing cross-ref resolver,
sequential run, continue-on-entry-failure with per-entry capture, resume that skips
already-succeeded entries within the session, ONE confirm tap per write batch.
Free-read action: separate button whose dispatcher allowlists `*.get/getAll/
getAllNames/list` endpoints ONLY (structurally incapable of mutation); code lands in
v4.29 but the button surfaces only after the tap-exemption ruling.
**Build steps.** UI (createElement/CSSOM only) -> sequencing -> capture -> resume ->
read-action allowlist.
**Verification.** Batch smoketest: two minimal hidden manifests, one with an induced
failing entry - the other completes, the bundle shows isolation, a re-tap resumes
and skips successes. Read action: attempted non-get endpoint name in a capture
manifest is refused client-side (fixture).
**Acceptance.** One tap = whole batch; combined bundle parses in harvest.py;
write-gate doctrine intact (reads exempted only after ruling).
**Effort.** Med. **Deps.** RULING: read-only tap exemption (button). v4.29 release
shared with WO-07's panel half.

### WO-07 - W5 simulator assertions for laws 9-13 + provenance (shortlist #6)
**Scope.** The five combat-math laws become executable red/green assertions; 45g
stops being an always-loaded monolith in the panel; the 12b enforcement-provenance
column becomes machine-checked.
**Files/tools.** `validate.py --laws` mode (reads 45e constants as fixture; asserts:
law 9 cross-bucket product within epsilon; law 10 same-type (1+p_i) product not sum;
law 11 pierce lands below the normal floor; laws 12/13 suppressed rounds contribute
zero - each asserts the VALUE, not that calc ran). 45g split into per-entity shards
(panel lazy-loads the shard for the build type - rides v4.29; validate.py reads all
shards, script side unaffected). `lawmap.py --strict-provenance` flag: matrix row
classed validate with no resolvable citation = ERROR (default OFF pending the
Phase-3 ruling already open; the 5 known warnings 16d/37/69/18/61 stay warnings
until ruled).
**Verification.** --laws exits 0 against shipped 45e; a mutated-constant fixture
exits 1 per law (five red cases); parity stays 16/16; panel-open latency on the
Samsung device measured before/after sharding (empirical, no published cliff).
**Acceptance.** Five laws move from prose-only to asserted; lawmap counts unchanged
except intended; sharded panel loads only its entity's checks.
**Effort.** Med. **Deps.** Panel half rides WO-06's v4.29. Strict-provenance flip is
ruling-gated (existing Phase-3 rulings_open row).

### WO-08 - W9 shard + freshness metadata (shortlist #7)
**Scope.** answers/ becomes deterministic two-fetch sharded with per-shard freshness
headers, so a fetch-only consumer can decide capture-or-trust in the same fetch.
**Files/tools.** `.github/scripts/build_answers.py` (container-editable - NOT a
workflow file): emit `answers/<pool>/<shard-key>.json` per the Stage-4.5 layout plus
a hot shard for recently harvested records; each shard header carries
`{generated, source_bundle, age_at_generation, row_delta}`; `answers/INDEX.md` stays
one screen: shard -> stamp table + the deterministic key rule (pool name; printed,
never globbed). New `docs/COMPACTION_RUNBOOK.md`: keep latest-N bundles verbatim,
fold older into the seed, squash superseded inbox commits - MANUAL, scheduled,
force-push acknowledged, seed is the durable audit floor. Runbook only; execution is
ruling-gated.
**Verification.** Local regen: headers present on every shard, INDEX table matches
the shard set, row_delta arithmetic checks against the prior generation; two-fetch
demo via container curl (raw INDEX -> raw shard, both 200, second URL computed from
the first, no directory listing needed).
**Acceptance.** Any single-entity lookup = exactly two fetches; freshness readable
without a third; old flat names_*.json kept as aliases for one generation then
removed.
**Effort.** Low-Med. **Deps.** RULING: history squashing (runbook execution only;
sharding itself is unblocked).

### WO-09 - W11 task packs + section-addressable references (shortlist #8, LOWERED 5->8 by report)
**Scope.** Per-build-type generated packs collapse the ~30K per-task reference read
to the excerpts that matter; anchors+TOC cover ad-hoc slices. Pure token economy -
correctly sequenced after the reliability cluster (report's stated re-rank).
**Files/tools.** Anchors (depth 2-3, stable `<a id>`-style or heading-slug) added to
ai.md (68K), quest.md (64K), pipeline.md (48K). New
`skills/building-tnr-content/scripts/build_packs.py` (stdlib; runnable locally AND
callable by the staged skillpack step): emits `skills/building-tnr-content/packs/
<build-type>.md` = owning reference's relevant sections + that type's relocated laws
+ applicable pipeline steps, per the 00_INDEX routing table; emits per-file TOC
sidecars `references/_toc/<file>.json` (anchor -> byte range) for fetch-then-slice.
Staged skillpack.yml step: rebuild packs on canon change (rides the upload batch;
until installed, the container ritual runs build_packs.py by hand).
**Verification.** Deterministic: two consecutive builds byte-equal; every pack
section traces to a source anchor (script asserts); TOC byte ranges slice-verified.
Empirical acceptance: WO-05's token ledger shows the per-task read drop on the next
real build session - the report's "measured instead of vibed" instrument.
**Acceptance.** A jutsu build session reads pack + data files only; ledger delta
recorded.
**Effort.** Med. **Deps.** WO-05 (ledger instrument); staged workflow batch for
auto-rebuild.

### WO-10 - W10 credential hardening (shortlist #9)
**Scope.** (a) Scrub gate goes fail-closed multi-pattern NOW (channel repeats every
session; currently WARNS and passes on unset secret - verified in scrub.yml). (b)
The long-lived PAT comes off the write hot path via a workflow_dispatch relay -
ruling-gated. (c) Panel/container token separation - ruling note.
**Files/tools.** (a) `state/staged_workflows/scrub.yml` patch: unset/empty
SCRUB_STRINGS = exit 1 (fail-closed); newline-separated multi-pattern loop; hit =
exit 1 with file list. Plus `skills/building-tnr-content/scripts/scrub_check.py`
(stdlib) so the container can run the same gate pre-push with a local pattern file
that never commits. (b) `state/staged_workflows/relay.yml` (workflow_dispatch,
input=branch; job merges branch->main under the expiring GITHUB_TOKEN) + a flow note
in docs: container pushes to a work branch, dispatch performs the privileged commit.
(c) rulings entry only.
**Build steps + verification.** (a) authored + locally proven: empty pattern list
exits 1; a seeded fake token in a temp tree exits 1; clean tree exits 0. (b)
authored + staged; dry-run only possible post-install.
**Acceptance.** (a) installed in the upload batch and the first push after it runs
the fail-closed gate green. (b/c) move on ruling.
**Effort.** Low (a) / Med (b). **Deps.** Upload batch (a, b install); RULING:
PAT/relay strategy (b activation, c).
**Stated deviation.** (a)'s AUTHORING is pulled into Wave 1: it shares the one
web-UI upload vehicle with WO-02 and costs minutes; the report itself says "ship the
fail-closed scrub gate now."

### WO-11 - W12 art QC mechanization + hit-rate ledger (shortlist #10)
**Scope.** Three zero-human-look raw-QC checks + an evidence ledger that turns
scaffold editing and the reference-escalation question into measured calls.
**Files/tools.** New `skills/producing-tnr-art/scripts/rawqc.py` (stdlib only:
struct for PNG chunk walk, zlib for IDAT inflate): (1) IHDR aspect sanity vs the
asset-type spec table (counters the lying square preview), (2) chroma coverage % of
key pixels vs band, (3) border-ring halo scan for non-key non-subject fringe pixels.
Wired as a pre-step ahead of chroma.py in the pipeline reference. New append-only
`skills/producing-tnr-art/data/art_ledger.jsonl`: one row per generation
`{scaffold_id, ts, verdict, reason_code}` (halo | wrong-aspect | low-coverage |
unprocessable | art-direction). shotlist.py reads accept-rate per scaffold and FLAGS
reference-escalation candidates - the escalation rule itself stays an open art
ruling; this builds the evidence, not the policy.
**Verification.** Fixture PNGs (clean / haloed / wrong-aspect / low-coverage)
red/green; chroma.py selftest still 38/38; ledger append + shotlist read round-trip.
**Acceptance.** Next art session runs rawqc before any human QC look; ledger
populates from real generations.
**Effort.** Low. **Deps.** None - most decoupled; slots anywhere, kept at tail per
ranking.

### Contingent (ruling-gated, not a numbered wave step)
**jsDelivr commit-pin (W7-RQ2).** If ruled yes: staged release workflow rewrites
`builder_loader_user.js` `@require` to
`cdn.jsdelivr.net/gh/perseverance484/tnr-tools@<sha>/builder_bundle.js` per release
(immutable, permanently cached - kills the staleness class); raw.githubusercontent
stays the fallback path; ViolentMonkey refresh still needed per release (documented
sticky @require cache), but fetched bytes are guaranteed correct. Only tnr-tools
code rides the CDN, never game source.

## Waves

Wave 1 is the smallest set that lands the report's #1 and #2 reliability wins; the
only ranking deviations are the two stated riders (scrub authoring shares Wave 1's
upload vehicle; blob-SHA self-verify shares v4.28) and the release-batching of
WO-07's panel half into v4.29.

| Wave | WO | Item | Effort | What proves it |
|---|---|---|---|---|
| 1 | WO-01 | W6 read-back + SHA self-verify (builder v4.28) | Med | harvest fixture red/green; push/7 smoketest bundle carries verdicts; panel title v4.28 |
| 1 | WO-03 | W4 schema_diff gate + extractor invariants | Med | SECTOR_TYPES-class fixture exits 1; additive fixture exits 0; self-diff = 0 |
| 1 | WO-02 | W3 drift sentinel (authored + staged) | Low | local dry-run hash stable x2; post-install dispatch commits baseline |
| 1 | WO-10a | scrub fail-closed (authored + staged) | Low | empty-list exit 1; seeded-token exit 1; clean exit 0 |
| 2 | WO-04 | W1+W7-doc doctrine projections | Med | --check zero-delta; drift fixture exit 1; doctrinemap 0e; lawmap still 93/0e/5w |
| 2 | WO-05 | W2 session_open/close + digest + ledger | Med | round-trip byte-assert selftest; next session opens <500 tokens |
| 3 | WO-06 | W8 batch Build + free reads (v4.29) | Med | induced-failure batch isolates + resumes; one tap per batch |
| 3 | WO-07 | W5 --laws + 45g shards + provenance flag | Med | 5 red mutation fixtures + green on shipped 45e; parity 16/16; panel latency measured |
| 4 | WO-08 | W9 shards + freshness headers | Low-Med | two-fetch curl demo; headers + INDEX table verified |
| 4 | WO-09 | W11 task packs + anchors/TOC | Med | deterministic rebuild; token-ledger delta on a real session |
| 4 | WO-11 | W12 rawqc + art ledger | Low | fixture PNGs red/green; chroma selftest 38/38 |
| 4 | WO-10b | PAT relay (on ruling) | Med | post-install dispatch dry-run merges a branch |
| 4 | cont. | jsDelivr pin (on ruling) | Low | pinned URL serves exact commit bytes; panel loads |

Cross-wave dependency spine: WO-02/WO-10a INSTALL (and WO-04/WO-09 auto-rebuild
steps) all ride ONE web-UI upload batch - dauntless can do it any time after Wave 1
authoring; nothing else blocks on it. WO-05 before WO-09 (ledger is the acceptance
instrument). v4.28 before v4.29.

## rulings_open (proposed additions - propose, never finalize)

1. **One-time web-UI workflow upload** - install state/staged_workflows/* via
   browser in one session; never grant Workflows-RW to the container PAT.
   Recommendation: approve; near-zero effort, unblocks the top failure source.
2. **Read-only tap exemption** - surface the v4.29 free-read capture button
   (allowlisted *.get/list only). Recommendation: approve; reads are not writes,
   write gate untouched, unblocks free probes + standing verification.
3. **jsDelivr dependency** - commit-pinned loader via third-party CDN.
   Recommendation: approve as pilot with raw fallback; kills the staleness class.
4. **PAT/relay strategy** - workflow_dispatch relay (expiring GITHUB_TOKEN does
   privileged writes) + separate panel PAT. Recommendation: adopt relay, mint a
   second PAT; skip rotation rituals (they slip).
5. **History squashing** - COMPACTION_RUNBOOK execution (force-push, keep-latest-N,
   seed floor). Recommendation: approve as manual scheduled compaction only.

Pre-existing open rulings (Phase-3 T1 scope / warn-vs-error, laws 16d-37-69 and
18-61 reclass, stack.py retire-or-repoint, wedge source note relay, project-knowledge
deletion confirm) are untouched by this plan except where noted (WO-07 builds the
strict-provenance mechanism but ships it OFF).

## What this plan does NOT do

No game writes, no workflow pushes, no builder release, no doctrine rewrites this
pass. Execution starts with Wave 1 on approval in-thread.
