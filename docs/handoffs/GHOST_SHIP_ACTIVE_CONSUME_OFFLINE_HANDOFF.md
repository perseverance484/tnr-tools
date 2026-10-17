# Handoff — Ghost Ship / Skyglass active Consume revision

**Repository:** `perseverance484/tnr-tools`.
**Branch:** `fable/ghost-ship-active-consume-20261011` (new, single writer).
**Design/base SHA:** `46df27172556807ab5bf723b0aa8c1251445ba2e`.
**Historical r4:** `3f825562ea051306a3803f47428b742ae5100011` (unchanged).
**Review target:** exact bundle head in the delivery message; freeze that SHA.
**Publication:** BLOCKED. Command-line `git push -u origin fable/ghost-ship-active-consume-20261011` failed because no GitHub authentication is configured (`could not read Username`). No remote head was created or claimed verified. The connected commit-creation API cannot preserve existing author/date metadata, so it was not used to rewrite this history. Import the verified delivery bundle and push through configured native Git access, then verify the remote SHA before normal Lane A review/integration.
**Integration target:** main, verified at `50f980f08dfcc798723c26243b9399cc0a97911a`
at initialization; verify again before integration. Nothing is integrated by this handoff.

The previously unpublished design commit was delivered and verified as a git
bundle containing exactly the design branch head46df271 and requiring r4.
Bundle SHA256: `c58e18391c2065cd9c54ea4567ea72e7449762a9cd5a049b66c96873955b7443`.
This local implementation branch and its delivery bundle include that exact commit as its parent/ancestor;
no `chatgpt/*` or frozen r4 branch is written.

## Objective and scope

Implement the committed `state/prompt_ghost_ship_skyglass_consume_revalidation.md`:
Katana15 / Crystal10 on the new active-Consume engine, with full candidate schemas,
actual item actions, adversarial processor probes and read-only occupation guards.
Timing remains **unapproved source-default test carriers: rounds3/shieldRounds3**.

Added:
- `harness/ghost_ship_consume/`: versioned runner, builder, fixture helpers, tests,
  failure-enforcement probes and committed evidence/provenance.
- `state/ghost_ship_skyglass_active_consume_carriers.json`: field provenance,
  explicit test-only fields, capture hashes and old Katana diff.
- `docs/reviews/GHOST_SHIP_ACTIVE_CONSUME_SOURCE_DRIFT.md` and
  `docs/reviews/GHOST_SHIP_ACTIVE_CONSUME_OFFLINE_RESULTS.md`.

Current reward decisions and roadmap gain pointers to the scoped carrier evidence.
Frozen r4 harness, record, generator, results, graph and global September Forge
state are unchanged. No session-close projection was run.

## Verification

Exact paths/commands are in results §5 and the harness README.

- `harness/ghost_ship_consume/run.sh`, twice under explicit seccomp mode:
  M0 482/0; Bun34 pass/0 fail/195 expects/2 files; CONTRACT16/0,
  GUARDS17/0, ACTIVE75/0; all five negative probes enforced; exit0.
- Both runs' four gate JSON files and provenance are byte-identical.
- `python3 harness/ghost_ship_consume/tools/build_item_carriers.py --check`: current.
- Historical `build_katana_record.py --check`: current.
- All 1,780 pinned app files verified against git blobs before/after execution.
- Upstream Consume preflight:30 pass/0 fail/93 expects.
- `git diff --check`; historical protected paths and engine checkout unchanged.
- No doctrine/skill/generated-source adoption: corresponding regeneration gates
  are not applicable. These are test carriers, not a Forge manifest.

## Source, runtime and deliberate differences

Engine `studie-tech/TheNinjaRPG@585534d7eb21d6f0dd678d5c3eb92662f611d39b`;
old pincddd7d91 is its ancestor, range162 commits. Lock SHA256
`da6602f2550bea9f1baf8508fa82b03d320bfcee269257f36cf25b47f1906c08`.
Dependency manifests unchanged; existing approved frozen install reused.
Bun1.4.2 / Nodev24.19.0 / Python3.12.14, recorded in provenance.

`unshare -rn` is unavailable in this environment. The explicit alternative is
seccomp syscall denial, with socket EPERM preflight, closed inherited extra FDs,
clean placeholder environment and Bun dotenv/auto-install disabled. No namespace
claim. Default unshare mode fails closed when unavailable; neither that failure
nor malformed negative probes counts as successful enforcement.

## Findings and review targets

- Positive-duration Consume-only Crystal validates without a Damage/Pierce filler
  or upstream correction. Instant Consume still requires its companion.
- Both revised rates convert granting/later damage. No-damage recipient actions
  can grant a useful active Crystal buff for subsequent attacks.
- Same-action SELF dedupe remains; separate two-weapon casts overlap10+10→20.
  Active ratio aggregation caps at100%; shields cap individually at100,000 HP.
- Buff and earned-shield expiry are independent. Clear removes item Consume.
  Existing Buff Prevent does not suppress tested Consume; immunity window is unchanged.
- All approved Katana costs/cooldown/range and non-imbuable guards remain intact.

Attack hardest: real assembly/action versus synthetic processor-control boundaries;
exact duration interpretation; two-weapon reapplication versus same-action dedupe;
new engine drift and fixture limitations; seccomp fallback and failure enforcement.
GUARDS stubs profile refresh and traps the first DB write: no persistence,
CAS/concurrency, auction transaction or completed crafting/imbue proof.

## Open decisions / not begun

Director retains Consume buff/shield durations, Consume-on-Consume policy, Crystal
rarity/trade/crafting access, Katana presentation/art, all previously open AI/parity
and legacy packet hash decisions. No A1/A2 numerical carry-forward to the new pin
is claimed. Deployment/settings capture is absent; fresh operator quest capture
is still required before an edit.

No engine edit, tuning, art, manifest, quest change, publication, unhiding or main
integration. Live requests0 / writes0 / CDN0 / credentials none. No browser or
installed-client checks. Independent frozen-SHA review remains required.
