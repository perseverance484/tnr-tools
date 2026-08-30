# active-context.md - read this first, then the board

**State in one line:** Wave 1 build side COMPLETE and pushed (WO-01 builder v4.28
read-back hardening @0e62821, WO-03 schema_diff gate @46f72a2, WO-02 sentinel staged
@c0df06d, WO-10a scrub staged @54e4ff6). Rulings 1+2 approved; 3/4/5 explained,
pending. Live acceptance + workflow installs sit with dauntless; Wave 2 (WO-04/WO-05)
starts on go.

**Verified at close (exact runs, from data/):** factory --selftest 20/20; validate.py
push/6 and push/7 both 0/0; --parity 16/16; lawmap <root> 93/0e/5w; node --check
builder_bundle.js OK; harvest.py verify fixtures green(0)/red(1); schema_diff
SECTOR-class red(1)/additive green(0)/live self-diff 0/invariants 0e over 128
variants; sentinel_hash green/red/stamp-invariant; scrub_check empty-red(1)/
seeded-red(1)/repo-clean-vs-real-PAT(0 hits, 145 files); shipped 45c/45d/45e vs
upstream HEAD = ZERO drift.

**Start ritual next session:** git pull --rebase; SET REPO-LOCAL GIT IDENTITY
IMMEDIATELY (git config user.name perseverance484 / user.email
288385517+perseverance484@users.noreply.github.com) - inline -c broke mid-rebase
this session. Read state/status.json. If a new inbox bundle exists: harvest.py
verify it FIRST (WO-01 acceptance). Re-run lawmap + parity before trusting anything.

**dauntless checklist (all Wave 1 closure items):**
1. ViolentMonkey refresh -> panel title must read "Content builder v4.28 · cfg
   generated" (a ⚠HEAD suffix means the loaded copy is stale vs repo).
2. DONE - WO-01 acceptance PASSED (bundle 1788061342415, verify green).
   container then runs harvest.py verify on it.
3. Web-UI install batch (browser, NOT the PAT): state/staged_workflows/
   regen_schemas.yml -> .github/workflows/ (new) and scrub.yml -> REPLACE
   .github/workflows/scrub.yml. SAME SESSION: set repo secret SCRUB_STRINGS
   (one pattern per line: both PATs at minimum) - gate is fail-closed, unset
   secret = every push fails by design.
4. First-run regen-schemas-sentinel via workflow_dispatch (expect: no drift).
5. Rulings 3 (jsDelivr pilot), 4 (PAT relay), 5 (history squash) whenever ready.
Carried: confirm 00_INDEX/10_LAWS deleted from project knowledge; wedge note to
Terr; clerk portrait prompt at state/prompt_report_clerk.txt; Borrowed Awakening
W4 ~Sep 5 (hide 5 cosmic jutsu).
- Terr: quest-edit crash fix; push/6 held until then.

**Wave 2 next (on go):** WO-04 doctrine single-sourcing (DOCTRINE.yml +
render_doctrine.py --check + doctrinemap.py + staged skillpack patch), then WO-05
session_open/close + digest + token ledger. Plan text: docs/PLAN_2026-08-30.

**Laws that bite immediately:** validate.py/factory.py want cwd=data/; lawmap wants
repo root arg. Regen adoption goes THROUGH schema_diff now (00_INDEX row). A push
echo is not a read-back; harvest.py verify is the read-back's reader. Everything
ships hidden:true. Always git pull --rebase before push - workflows commit back.

**Failure modes to watch in yourself:** container shell is /bin/sh - no process
substitution; use temp files. Inline git -c identity fails inside rebase
finalization - set repo-local config first. Never pipe a gate's output through
tail and read $? - the pipe masks the exit code (caught twice this session).
Exact-match count==1 asserts on every patch. Never push under .github/workflows/ -
stage to state/staged_workflows/.
