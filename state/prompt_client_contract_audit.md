# CLIENT CONTRACT AUDIT - Claude Code dispatch brief

Drafted 2026-09-03 for dauntless. Paste this whole file as the opening prompt to a
Claude Code agent working in `perseverance484/tnr-tools`.

Purpose: derive, from the game's source, the complete client-side contract for
writing TNR content, so the next builder is designed to spec instead of by
guess-and-check. The audit is ARCHITECTURE-NEUTRAL. It does not assume the next
client is a userscript, and it does not assume it is a native app. It produces the
evidence that decides which.

---

## 0. Non-negotiables

Read these first. Violating any one of them invalidates the report.

1. **This is a source audit. Make zero live requests.** Never contact
   theninja-rpg.com. Never run the game. Never use, request, or synthesise a
   credential, session token, cookie, or API key. No writes to any game system.
2. **Read-only on the game source.** Clone `studie-tech/TheNinjaRPG` shallow, pin
   the SHA, record it, never modify it, never open a PR against it.
3. **Fix nothing.** Do not edit `builder_bundle.js`, `docs/`, `ENGINE_LAWS.md`,
   `skills/`, or any manifest. This dispatch reports; a later batch acts.
4. **Branch, never merge.** Work on a new branch off `main`. Commit only the two
   deliverables in section 5. Do not merge, do not open a PR against `main`.
5. **Every claim is anchored or it is not a claim.** Each finding carries
   `file`, `line`, and a `match` string (line anchors are byte-fragile; the match
   string is the durable locator). No claim from general Next.js, tRPC, Clerk, or
   Zod knowledge. If the source does not say it, the verdict is `NOT_IN_SOURCE`.
6. **Absence claims state the population scanned.** "No rate limiting exists" is
   worthless without "scanned 41 files under src/server/api, grep terms X, Y, Z".
7. **Never copy game prose.** TNR is open source for facts, not for text. Extract
   schemas, enums, constants, and control flow. Do not reproduce dialog, item
   descriptions, or flavour text into the report. Never reference the Naruto
   franchise in any output.
8. **No balance work.** Drop rates, reward values, stat tuning, and difficulty
   gates are reserved for dauntless and are out of scope entirely.

Verdict vocabulary, used on every finding:

- `ENGINE` - explicitly present in source at the pinned SHA
- `PARTIAL` - partly supported; the gap is stated
- `INFERRED` - a reasonable read of the code that the code does not state outright
- `NOT_IN_SOURCE` - searched for, not found; population scanned recorded
- `CONTRADICTED` - source contradicts a belief currently held in tnr-tools

---

## 1. Context you need

`tnr-tools` is the toolchain repo for a content contributor on TNR staff. The
current client is `builder_bundle.js` at repo root: 892 lines, a ViolentMonkey
userscript panel injected into the game in Firefox on Android. It posts to
`/api/trpc/` with `fetch`, uses `credentials` and an `Authorization` header, has
Clerk in the auth path, assembles procedure paths at runtime, sends batched
requests, and hand-rolls date and field coercion on the way in and out
(`data.createdAt`, `data.regenAt`, `data.sceneCharacters` and similar).

That bundle was built by observation, not from spec. Known consequences include
at least one silent failure class where a client-side reference shipped as a
literal, was dropped server-side, and still reported a green row.

`45c_DATA_constructors.json` and `45g_DATA_checks.json` at repo root are
generated payload constructors and checks that the toolchain composes against.
Their fidelity to source is one of the questions below.

Read `docs/00_INDEX.md` for routing and precedence before forming opinions about
what tnr-tools currently believes. Do not restate laws in the report; cite source.

---

## 2. Scope

Six surfaces. Cover all six.

### 2.1 Auth and identity
How Clerk is wired: middleware, provider config, where the session is read on the
server, how a token reaches a request, header versus cookie, token lifetime and
refresh, and what happens on expiry. The role and permission model: what
distinguishes content staff from admin, where each mutation checks role, and what
the failure shape is on a role miss.

### 2.2 Transport
tRPC major version and its wire format at that version. Endpoint path shape.
Batching envelope, exact request and response JSON. **Whether a transformer
(superjson or otherwise) is configured** - this is high value, because a
transformer changes how `Date`, `undefined`, `Map`, and `BigInt` cross the wire,
and the current bundle coerces dates by hand. HTTP method per procedure type.
The error envelope, including how Zod validation failures are shaped.

### 2.3 Procedure inventory
Every procedure a content client needs, for jutsu, item, ai, aiProfile, quest,
and asset upload: create, edit, fetch, delete, list, and any publish or visibility
toggle. For each: full path, query or mutation, resolved input shape, output
shape, auth gate, and observable side effects. Flag any procedure that the
current bundle calls but source does not expose, and any the bundle should be
calling and is not.

### 2.4 Entity field contracts
Per entity, per field: name, Zod type, required or optional, schema default, DB
default, enum members in full, and every `superRefine` or cross-field constraint
with its exact condition. Then the behaviour that matters most for silent
failures: **for each field, does an invalid or unknown value error, coerce, or get
silently stripped, and where.** Name the file and function that does the
stripping. Generalise the known failure class described in section 1 into a rule.

### 2.5 Write semantics and read-back
What a mutation actually returns: the persisted record, an id, or a bare success
flag. Which procedure is the ground truth for reading a record back, and whether
its shape matches what create accepted. How ids are generated and where they
first become knowable to a client. The semantics of the hidden flag and the
publish path, including who may flip it.

### 2.6 Assets
The upload path end to end: procedure or route, storage backend, accepted mime
types, byte ceiling and where it is enforced, returned identifier shape, and what
a client must do to make an uploaded asset referenceable by a later create.

---

## 3. Generation fidelity and divergence

Two comparisons, both against the pinned game SHA.

**Fidelity.** Do `45c_DATA_constructors.json` and `45g_DATA_checks.json` match
source? Report drift field by field: fields present in source and missing from
the generated files, fields present in the generated files and absent from
source, wrong types, stale enum members, missing constraints. State whether the
generator that produced them can be re-pointed at source, or whether it is
observation-derived and needs replacing.

**Divergence.** Every place `builder_bundle.js` diverges from the contract. Rank
by severity, with the observed symptom where one is known. Hand-rolled coercion
that a configured transformer would make unnecessary belongs here. So does any
place the bundle trusts a response field that source does not guarantee.

---

## 4. Feasibility gates

This section decides the next client's architecture. Answer each from source, with
anchors. Do not recommend an architecture; supply the evidence.

- **G1 Token portability.** Can a valid session token be obtained and used from
  outside a browser page context, or does any server check bind it to page
  origin, referer, or a browser-only signal?
- **G2 CORS.** The exact CORS configuration on the tRPC route and anything in
  front of it. Would a credentialed cross-origin POST from a different origin be
  accepted or rejected?
- **G3 CSRF.** Any CSRF token, double-submit cookie, origin check, or custom
  header requirement on mutations.
- **G4 Page context.** Any procedure that depends on state a page establishes
  rather than on the token alone.
- **G5 Rate limits and abuse controls.** Per-user and per-endpoint limits,
  windows, and responses on trip. Include anything that would treat a batched
  client as abusive.
- **G6 Client visibility.** Anything in source that detects, fingerprints, or
  restricts non-browser clients: user-agent checks, bot detection, device
  signals, headless checks. Also note any ToS, contributing, or licence file in
  the repo that speaks to third-party clients. **Report this factually and draw
  no conclusion about permission.** Whether a native client is sanctioned is
  dauntless's call with the admin, not this audit's.
- **G7 WebView viability.** Purely from source and dependency config: is there
  anything in the Clerk flow, the auth redirects, or the CSP that is known to
  break inside an Android WebView? Say `INFERRED` where that is what it is.

---

## 5. Deliverables

Two files, committed to a new unmerged branch.

**`reports/client_contract.json`**, schema `client-contract/v1`, with top-level
keys in this order:

```
schema, generated, target, consumer_notes, auth, transport, procedures,
entities, write_semantics, assets, fidelity, divergence, feasibility_gates,
redesign_spec, out_of_scope, audit_method
```

- `target` records both SHAs (game and tnr-tools), the branch scanned, and the
  framework versions read out of the game's `package.json`: next, trpc, zod,
  drizzle, clerk, and the upload library if any.
- `consumer_notes` states that anchors are fragile and must be located by `match`
  string, and names anything a downstream agent must not assume.
- `procedures` and `entities` are the bulk. Machine-actionable, one object per
  procedure and per field. Prose only where a constraint needs it.
- `redesign_spec` is a ranked, dependency-ordered list of what a from-spec client
  must do, each item with `depends_on`. Describe required behaviour, not chosen
  technology. This list must be equally usable by a userscript rewrite and by a
  native shell.
- `audit_method` records grep terms, directories walked, file counts, and what
  was deliberately not read.

**`reports/client_contract.md`**, a short executive summary: the SHAs, the top
five findings, the answer to each of G1 through G7 in one line each, and the
three highest-severity divergences. Cap it at roughly 120 lines. No
recommendation on architecture.

---

## 6. Working method

1. Clone the game source shallow, pin and record the SHA before reading anything.
2. Walk the tRPC router tree and the schema definitions first. Build the
   procedure and entity inventory before forming any opinion about the bundle.
3. Only then read `builder_bundle.js` and the generated data files, and diff
   observed behaviour against derived contract.
4. Prefer breadth over depth on first pass. A complete inventory with some
   `PARTIAL` verdicts beats three perfect entities and four missing ones.
5. When source and a tnr-tools belief conflict, mark `CONTRADICTED`, cite both
   sides, and move on. Do not rewrite the tnr-tools side.
6. Commit the two deliverables, push the branch, and report the branch name and
   both SHAs.

Nothing in this dispatch is adopted on delivery. The report will be spot-verified
against source before any of it changes tnr-tools, exactly as the law provenance
report was.
