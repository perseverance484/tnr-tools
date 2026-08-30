<!-- PROJECTION of state/digest.json - edit the digest, run session_close.py; never edit this file -->
# active-context.md - read this first, then the board

**State in one line:** Wave 4 COMPLETE, all four waves of PLAN_2026-08-30 executed: WO-08 hot shard @55d1533 (seed-lag gap CLOSED - SMOKE + 22 delta rows visible in answers, regen idempotent), WO-11 rawqc @d5e8b8d (4/4 synthesized selftest, ledger + escalation-candidate stats), WO-09 packs @fb36aa2 (jutsu-build exemplar 15.6K vs ~68K, --check fail-closed, TOCs for 5 refs), WO-10b @6f764a3 (relay + release-pin staged, rewrite dry-run proven). No live acceptance needed this wave - all container/CI-side; the second web-UI batch (skillpack v2, relay, release_pin) installs at leisure.

**Verified at close (exact runs):**
- lawmap -> 93 laws, 93 matrix rows, 74 citations across 38 files; 0 errors, 5 warnings
- doctrine projections -> all projections current (exit 0)
- packs/TOCs -> all packs and TOCs current (exit 0)
- parity tnr_results_1788065642059.json -> 0 errors, 0 warnings

**Start ritual next session:** git pull --rebase; set repo-local git identity
(user.name perseverance484 / user.email
288385517+perseverance484@users.noreply.github.com); then
`python3 skills/building-tnr-content/scripts/session_open.py` - it prints this
state, runs the guard trio (lawmap, validate on the in-progress file, parity
vs the newest inbox bundle), and seeds the token ledger. If a new inbox bundle
exists: `harvest.py verify` it FIRST. No clone means no state: say so.

**In progress:** wave: Plan executed 11/11 WOs + contingent. Remaining plan-adjacent: pack curation (ai/quest/item/art), relay ritual switch post-install, jsDelivr pilot watch after first pinned release.

**Open items, by owner:**
- dauntless: second web-UI batch: skillpack v2 (replace) + relay.yml + release_pin.yml (new) - no secrets needed this time; mounted instructions re-paste from state/mounted_instructions.txt (PAT slot) at leisure; carried: wedge note to Terr; clerk portrait prompt; Borrowed Awakening ~Sep 5 hide 5 cosmic jutsu; smoke jutsu 0QixZN9jD_bqAKTimDafB disposable
- terr: quest-edit crash fix; push/6 held until then

**Rulings open:** - Phase 3 T1 scope + whether warnings ship validator-first (12b Phase 3 section)
- laws 18/61 reclass knowledge->validate(partial); laws 16d/37/69 annotate-or-reclass
- stack.py: retire or re-point (audits retired project-knowledge layout)
- Wedge source note ready for Terr: AllObjectives discriminators clean at HEAD; suspect duplicate zod across chunks - relay?
- Paste mounted project instructions (delivered 2026-08-30), then DELETE 00_INDEX.md + 10_LAWS_core.md from project knowledge - repo docs/ copies are now canon
- lint table now lives in TWO places (builder JS + validate.py port, drift hazard): single-source as shared data both read - fold into WO-04 doctrine work or a builder release?

**Next:** dauntless at leisure: second web-UI batch (state/staged_workflows/: skillpack.yml REPLACE, relay.yml new, release_pin.yml new); mounted re-paste. Then normal content work resumes - Forsworn board unchanged (Faceless Stray art, Old Ghost + Tenth Name prose, Terr wedge).

**Laws that bite immediately:** validate.py/factory.py want cwd=data/; lawmap
and doctrinemap want no args (paths resolve from the repo). Regen adoption
goes THROUGH schema_diff (00_INDEX row). A push echo is not a read-back;
harvest.py verify reads the verdicts. Everything ships hidden:true. Always
git pull --rebase before push - workflows commit back. Doctrine edits happen
in docs/DOCTRINE.md, then render_doctrine.py --write; rendered blocks are
never hand-edited.

**Failure modes to watch in yourself:** container shell is /bin/sh - no
process substitution; use temp files. Inline git -c identity fails inside
rebase finalization - set repo-local config first. Never pipe a gate's output
through tail and read $? - the pipe masks the exit code. Never search a
truncated blob and claim absence - print the population scanned. Exact-match
count==1 asserts on every patch. Never push under .github/workflows/ - stage
to state/staged_workflows/.
