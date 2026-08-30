# active-context.md - read this first, then the board

**State in one line:** audit session (1 of 3) closed: full-stack sweep measured, research
brief shipped at docs/RESEARCH_BRIEF_2026-08-30_stack_optimization.md (505 lines, W1-W12,
ranked shortlist, SOURCE MAP). ZERO game touches, zero tool patches by scope. Session 2
(fetch-only deep research) opener emitted in the closing transcript; Session 3 builds the
implementation plan from brief + research report.

**Verified at close (exact runs, from data/):** lawmap.py -> 93 laws, 0 errors, 5 known
warnings; validate.py push/6_verify_and_fix.json -> 0/0; --parity vs
harvests/inbox/tnr_results_1788053115846.json -> 16/16. Two SOURCE MAP raw URLs curl 200
unauthenticated. Brief greps clean for the PAT.

**Start ritual next session:** git pull --rebase; read state/status.json. If this is
Session 3: also fetch the brief and the Session 2 research report before proposing
anything. Re-run lawmap + the parity line before trusting anything. Normal work sessions:
unchanged ritual.

**Open items, by owner:**
- dauntless: run Session 2 with the emitted opener (paste as-is). PAT Workflows RW still
  blocks regen_schemas.yml (also brief W3). Phase 3 rulings unchanged in rulings_open.
  Confirm 00_INDEX/10_LAWS were deleted from project knowledge (mounted copy is live, so
  the ruling looks half-done). Wedge source note relay to Terr still pending. Art queue:
  clerk portrait prompt at state/prompt_report_clerk.txt. Borrowed Awakening W4 closes
  ~Sep 5: hide the 5 cosmic jutsu.
- Terr: quest-edit crash fix; push/6 stays held until then.

**Laws that bite immediately:** validate.py/factory.py want cwd=data/. Extraction owns
CONTRACTS; capture-first owns LIVE STATE (law 83). A push echo is not a read-back.
Everything ships hidden:true. Always git pull --rebase before push - workflows commit back.

**Failure modes to watch in yourself:** structural-diff before adopting any regenerated
file. Exact-match count==1 asserts on every patch. In-session web_fetch cannot mint URLs -
curl via the container allowlist is the public-resolvability check. Soft line targets:
land inside the band before polishing prose.
