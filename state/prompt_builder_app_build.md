# BUILDER APP - Claude Code implementation brief

Drafted 2026-09-03 for dauntless. Paste this whole file as the opening prompt to a Claude Code
agent working in `perseverance484/tnr-tools`.

Build the full-page builder app specified in `docs/PLAN_2026-09-03_builder_app.md`. Read that
spec first; it is the contract. This brief covers method, constraints and deliverables only,
and does not restate the design.

---

## 0. Non-negotiables

1. **Make zero live requests to theninja-rpg.com.** Never contact the game, never run it,
   never use, request or synthesise a session cookie or credential. You are writing a client,
   not exercising one. Every behaviour is verified against recorded fixtures, never live.
2. **No game writes.** Nothing you produce may run against the game. dauntless is the only
   one who starts a job, on his own device.
3. **Branch, never merge.** Work on a branch off `main`, do not merge, do not open a PR
   against `main`.
4. **Do not edit** `builder_bundle.js`, `docs/ENGINE_LAWS.md`, `reports/`, or any manifest
   under `push/`. The existing bundle stays working and untouched until the new app replaces
   it deliberately.
5. **DOM via `createElement` and CSSOM only.** No `innerHTML`, anywhere. Repo law.
6. **Never copy game prose.** Extract schemas, enums and constants. Never reference the Naruto
   franchise in code, comments or UI copy.
7. **No balance work.** Drop rates, reward values, stat tuning and difficulty gates are
   reserved for dauntless. Carry placeholders and list every one in your summary.

## 1. Sources of truth, in precedence order

1. `docs/PLAN_2026-09-03_builder_app.md` — the design
2. `reports/client_contract_verification.md` (branch `client-contract-verification`) — where
   it disagrees with the audit, it wins
3. `reports/client_contract.json` (branch `client-contract-audit`) — the contract, especially
   `redesign_spec` R1 through R10
4. `docs/00_INDEX.md` for routing and precedence; repo `docs/` and `skills/` are canon

Fetch both report branches; do not merge them. Locate every claim by its `match` string, not
by line number.

**Do not re-derive the contract from `builder_bundle.js`.** The old bundle encodes a false
model of the server in at least six places. Read it only to understand what a feature was
trying to do, never to learn what the server expects.

## 2. Environment

Samsung Android, Firefox mobile, ViolentMonkey. No desktop, no devtools, no local server.
The userscript rides repo root and is refreshed through ViolentMonkey. Userscripts match
`www` and the bare host. Container shell is `/bin/sh`: no process substitution, use temp
files. Never pipe a gate through `tail` then read `$?`.

Assume the user cannot open a console to debug your code. Errors must surface in the UI with
enough context to act on, and the journal must be exportable as text.

## 3. Build order

Bottom-up, because each layer is testable against fixtures without the one above it.

1. **Storage** — journal in `localStorage` (synchronous, write-ahead), capture cache in
   IndexedDB. Journal schema, migrations, export.
2. **Transport** — superjson encode/decode, tRPC 11 fetch-adapter batch envelope derived from
   the adapter, `credentials: 'same-origin'`, POST for mutations, decoded
   `baseServerResponse` as the only outcome signal.
3. **Budget** — per-path token bucket, cache-first reads, hard stop on `TOO_MANY_REQUESTS`
   with no retry.
4. **Runner** — job execution, write-ahead state transitions, two-phase create, read-back
   diff on asserted keys only.
5. **Reconciliation** — pre-create snapshots, orphan diff, adoption policy, orphans panel.
6. **UI** — the five screens in the spec, full viewport, takeover at `document-start`.
7. **Manifest picker** — GitHub contents API listing, searchable, no positional index.

Land each layer working before starting the next. A half-finished runner on top of an
untested transport is worse than no runner.

## 4. Verification without a live game

`harvests/inbox/` holds real recorded response bundles. Use them.

- Build a fixture harness that replays recorded responses through the transport and asserts
  the decoded shape, including superjson round-trips of dates and nulls.
- **Crash-consistency tests are mandatory and are the point of this project.** Simulate
  eviction at every transition: before send, after send and before response, after response
  and before journal flush, mid-two-phase-create. Assert that resume never retries a `SENT`
  create and never double-creates.
- Test the `gameAsset` ambiguity explicitly: two placeholder creates crashed mid-run must
  produce an ambiguous result surfaced to the user, not a guess.
- Assert the budget never exceeds the configured margin, and that a 429 halts rather than
  retries.

Do not add tests that require network.

## 5. Known defect you must not inherit

`45g.tag_power_max` asserts a maximum of 100 on `damage`, `heal`, `absorb`,
`increasedamagegiven` and others. At source those are uncapped: `PowerAttributes.power` is
`z.coerce.number().min(0)` with no max and is spread *after* `BaseAttributes` in all 61 tags
that use it. `schema_extract.py` does not handle spread precedence.

So: either fix the generator's spread precedence handling first, or gate the power bound out
of pre-send validation with a comment pointing at this brief. **Do not wire validation
against `45g` as it stands** — you would bake a rule into the new client that rejects payloads
the server accepts. State in your summary which of the two you did.

## 6. Keep the seam for the native shell

A shell will later hold the session in an offscreen WebView, lift the cookie into native
networking via Android `CookieManager`, and render this app on top. Separately, if TNR's
developers enable `mcp.enabled` on the remaining content writes, a bearer token replaces the
cookie entirely.

Put all credential and request-issuing behaviour behind one interface with a single
cookie-based implementation today. Both later changes must be a new implementation of that
interface plus configuration, never a rewrite of the runner or the UI.

## 7. Deliverables

On one unmerged branch:

- The app source, structured so the layers in section 3 are separately readable
- A built userscript bundle at repo root, loadable by the existing loader, **versioned
  distinctly from `builder_bundle.js` so both can be installed side by side.** The old bundle
  must keep working until dauntless retires it.
- The fixture harness and tests, runnable with no network
- `docs/BUILDER_APP_NOTES.md`: the host path you chose and why, the journal schema, the
  budget margin and its reasoning, every placeholder you carried, and everything you did not
  finish

## 8. Working method

- Terse commits, one layer per commit where possible.
- When the spec and a report disagree, follow the precedence in section 1 and say so in the
  commit message.
- When something in the spec turns out to be wrong or unbuildable, stop and write it down in
  the notes rather than improvising around it. The spec was derived from a source audit and a
  partial verification; it is not infallible, and a surprise in it is a finding.
- Report the branch name, what runs, what does not, and what you checked before handing back.

Nothing here ships to the game on delivery. dauntless installs the bundle, runs it against a
manifest of his choosing, and verifies from the inbox bundle as always.
