<!-- PROJECTION of state/digest.json - edit the digest, run session_close.py; never edit this file -->
# active-context.md - read this first, then the board

**State in one line:** Wave 3 CLOSED with live acceptance PASSED: batch '2,3' ran push/7+8 sequentially (two v4.29 bundles 5s apart), push/7 resume A:40/0 flags (pfEq ''<->null self-proven live - prior run flagged 2), push/8 free-reads captured both name lists, and the Reads-refusal red test on the write manifest confirmed REFUSED by dauntless. Picker papercut queued: accept filename leading digits, not just menu positions.

**Verified at close (exact runs):**
- lawmap -> 93 laws, 93 matrix rows, 74 citations across 36 files; 0 errors, 5 warnings
- parity tnr_results_1788065642059.json -> 0 errors, 0 warnings

**Start ritual next session:** git pull --rebase; set repo-local git identity
(user.name perseverance484 / user.email
288385517+perseverance484@users.noreply.github.com); then
`python3 skills/building-tnr-content/scripts/session_open.py` - it prints this
state, runs the guard trio (lawmap, validate on the in-progress file, parity
vs the newest inbox bundle), and seeds the token ledger. If a new inbox bundle
exists: `harvest.py verify` it FIRST. No clone means no state: say so.

**In progress:** wave: Wave 4 next on go: WO-08 answer shards+freshness, WO-09 task packs+TOC, WO-11 rawqc+art ledger, WO-10b relay + jsDelivr pin staged (second web-UI batch)

**Open items, by owner:**
- dauntless: re-paste mounted instructions from state/mounted_instructions.txt (insert PAT at the slot) whenever convenient - old paste keeps working, stamp detects staleness; Wave 4 web-UI batch later: skillpack.yml v2 + relay.yml + release-pin (staged as authored); carried: wedge note to Terr; clerk portrait prompt; Borrowed Awakening ~Sep 5 hide 5 cosmic jutsu; smoke jutsu 0QixZN9jD_bqAKTimDafB disposable
- terr: quest-edit crash fix; push/6 held until then

**Rulings open:** - Phase 3 T1 scope + whether warnings ship validator-first (12b Phase 3 section)
- laws 18/61 reclass knowledge->validate(partial); laws 16d/37/69 annotate-or-reclass
- stack.py: retire or re-point (audits retired project-knowledge layout)
- Wedge source note ready for Terr: AllObjectives discriminators clean at HEAD; suspect duplicate zod across chunks - relay?
- Paste mounted project instructions (delivered 2026-08-30), then DELETE 00_INDEX.md + 10_LAWS_core.md from project knowledge - repo docs/ copies are now canon
- lint table now lives in TWO places (builder JS + validate.py port, drift hazard): single-source as shared data both read - fold into WO-04 doctrine work or a builder release?

**Next:** Wave 4 on go.

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
