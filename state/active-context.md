# active-context.md - read this first, then the board

**State in one line:** plan session (3 of 3) closed: Session 2 research report committed
verbatim (docs/RESEARCH_REPORT_2026-08-30_stack_optimization.md), implementation plan
shipped at docs/PLAN_2026-08-30_stack_optimization.md (11 work orders, 4 waves, 5 new
plan rulings). ZERO execution, zero game touches, zero workflow pushes by scope. Wave 1
executes on in-thread approval.

**Verified at open (exact runs, from data/):** lawmap.py <root> -> 93 laws, 0 errors,
5 known warnings; validate.py push/6_verify_and_fix.json -> 0/0; --parity vs
harvests/inbox/tnr_results_1788053115846.json -> 16/16 (parity note line). Report and
plan grep clean for the PAT.

**Start ritual next session:** git pull --rebase; read state/status.json. If Wave 1 is
approved or underway: read docs/PLAN_2026-08-30_stack_optimization.md Wave 1 rows
(WO-01/WO-03/WO-02/WO-10a) before touching anything; re-run lawmap + parity before
trusting anything. Builder release discipline: v4.28 carries WO-01 only.

**Plan skeleton (full text in the plan doc):**
- Wave 1: WO-01 builder v4.28 read-back+SHA self-verify; WO-03 schema_diff gate +
  extractor invariants; WO-02 drift sentinel (authored+staged); WO-10a scrub
  fail-closed (authored+staged)
- Wave 2: WO-04 doctrine projections; WO-05 session_open/close + digest + token ledger
- Wave 3: WO-06 batch Build + free reads (v4.29); WO-07 validate --laws + 45g shards
- Wave 4: WO-08 answer shards+freshness; WO-09 task packs; WO-11 rawqc+art ledger;
  WO-10b relay (ruling); jsDelivr pin (ruling)
- Staged-workflow convention: workflow YAML is PAT-blocked; container authors to
  state/staged_workflows/, dauntless installs via ONE web-UI batch.

**Open items, by owner:**
- dauntless: rule on the 5 PLAN rulings (web-UI upload batch, read-tap exemption,
  jsDelivr, PAT relay, history squashing) - one-line recs in the plan; approve Wave 1
  in-thread to start execution. Carried: PAT Workflows-RW stays DENIED by plan
  doctrine (upload batch replaces it). Confirm 00_INDEX/10_LAWS deleted from project
  knowledge. Wedge source note relay to Terr. Art queue: clerk portrait prompt at
  state/prompt_report_clerk.txt. Borrowed Awakening W4 closes ~Sep 5: hide the 5
  cosmic jutsu.
- Terr: quest-edit crash fix; push/6 stays held until then.

**Laws that bite immediately:** validate.py/factory.py want cwd=data/; lawmap wants
the repo root arg. Extraction owns CONTRACTS; capture-first owns LIVE STATE (law 83).
A push echo is not a read-back (WO-01 exists to fix exactly this). Everything ships
hidden:true. Always git pull --rebase before push - workflows commit back.

**Failure modes to watch in yourself:** structural-diff before adopting any
regenerated file (WO-03 mechanizes this - until it lands, do it by hand). Exact-match
count==1 asserts on every patch. Never push anything under .github/workflows/ - stage
it. Soft line targets: land inside the band before polishing prose.
