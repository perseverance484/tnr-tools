# Forge over the game connection (MCP runner)

Runs a Forge manifest without a browser tab. The same Forge runner, journal, budget, reconciler
and results bundle are used; only the wire changes. Instead of the signed-in game tab, each game
call goes through the game's own MCP endpoint, called by a Claude session that has the game
connected as a connector.

Code: `forge/src/hosts/mcp/` (bridge, pacer, file hand-off, transcript answers, durable capture
store), `forge/tools/mcp_run.mjs` (CLI), tests in `forge/test/mcp.bridge.test.mjs` and
`forge/test/mcp.durable.test.mjs`. The userscript bundle does not import any of it.

## Why this works

The game publishes an MCP server at `https://www.theninja-rpg.com/api/mcp`
(TheNinjaRPG `app/src/app/api/mcp/[[...transport]]/route.ts`). Its `callEndpoint` tool reaches
every tRPC procedure through a server-side caller (`app/src/libs/mcp/handler.ts`,
`meta-tools.ts`, checked at 15a37ea on 2026-11-06), so every content write Forge uses is
reachable, signed in as the account that approved the connection. Authentication is an OAuth
grant held by the MCP client. No password, cookie or token is ever stored by this code or in the
repo. Server-side calls also skip the BotID check that guards browser mutations on `/api/trpc`.

## One-time setup (operator)

1. In Claude settings, add a custom connector with the URL `https://www.theninja-rpg.com/api/mcp`.
2. Approve it on the game's own sign-in page when asked. That grant is the only credential, and
   it can be revoked from Claude's connector settings or the game account at any time.

## The run lock: one writer at a time

Every runner on the account (the browser tab, a Claude session, Duet) spends the same two limits
without seeing the others: the game connection's 30 calls per minute per user, and the game's 60
per minute per procedure, whose mutation overruns fine the account 1% of money and bank
(TheNinjaRPG `app/src/server/api/trpc.ts` `enforceRateLimit`; `app/src/app/api/mcp/[[...transport]]/route.ts`).
So only one runner works at a time (RUL-2026-11-07-133). The lock is `state/run_lock.json` on
`main`; a claim is a commit pushed to `main`, so git's fast-forward check decides between two
claimers.

```
node forge/tools/run_lock.mjs status
node forge/tools/run_lock.mjs claim   --holder claude --job "push/502" [--ttl 60]
node forge/tools/run_lock.mjs release --holder claude
```

`run` and `resume` need `--holder NAME` and refuse, before any game call, unless NAME holds the
lock on `origin/main`. They extend it every 15 minutes and release it when the process exits
(`--keep-lock` keeps it, to chain the next job). A lock nobody extends expires after its TTL
(default 60 minutes). The browser never claims: Start and Resume read the lock at the tap and
refuse while anyone holds it (a missing file is free; a read failure warns and lets the operator
go on). Bulk live reads (scans, inventories) take the lock too: they spend the same 30 per minute.
What is waiting to run, and on what, is `state/run_queue.json`.

## A run (the Claude session holding the connection)

From the repository root, on an up-to-date `main` checkout:

```
node forge/tools/mcp_run.mjs plan push/412_x.json
```

Offline. Parses, plans and pre-send validates exactly as Forge does when a manifest is opened.

```
node forge/tools/mcp_run.mjs run push/412_x.json --holder claude --state <state dir> --transcript auto
```

Run it in the background. For every game call it writes `<state dir>/exchange/request.json`:

```
{"id": "...", "tool": "callEndpoint", "arguments": {"endpointName": "...", "input": {...}},
 "kind": "query" | "mutation", "answerFile": "answer-<id>.txt", "errorFile": "answer-<id>.error.txt"}
```

The session makes exactly that `callEndpoint` call with exactly those arguments, and nothing else:
no `select`, `search` or `maxLength`, which would filter the answer.

With `--transcript auto`, that is all the session does. The runner reads the session's own record
of the call (its Claude Code transcript, found from `CLAUDE_CODE_SESSION_ID`; or pass a path) and
writes the answer file itself, byte for byte (`transcript.mjs`). Only a call recorded after the
request was written can answer it, and each call answers one request. A result too large to show
in the conversation is saved by Claude Code to a file; the runner reads that file, after checking
it sits in the session's folder and has exactly the length the notice states. A result marked as
a tool error goes to the error file. The run log prints one `answered` line per call.

Without `--transcript` (or if a call is passed over, which the log says), the session writes the
tool result's text verbatim to `<state dir>/exchange/<answerFile>`, or the failure text to
`<errorFile>` when the tool call itself failed. Never edit, summarise or reformat an answer: Forge
verifies writes against it and stores captures from it.

When the job ends, the results bundle is written to `harvests/inbox/` in the working tree (the
CLI's "committed" line means written there), or to `--inbox <dir>`. Commit it to `main` as usual.
`resume <jobId>` picks up a paused or crashed job, and `jobs` lists the journal. Both use the same
`--state` directory. Keep it in `/mnt/project-files/` so a later session can resume.

The state directory holds everything a resume needs: `storage.json` (journal, send logs, id map,
pacer window) and `captures.idb` (the capture cache and the immutable full-capture snapshots,
`idbfile.mjs`). Each committed IndexedDB transaction is on disk before Forge continues, so a job
that dies mid-run and resumes in a new process still exports the exact bodies its full captures
read, rather than "snapshot is gone".

## What the host refuses

- **Image uploads.** Manifests with `@img` refs or an `imagePack` upload to `/api/uploadthing`,
  which is not on the MCP surface. Run those in the browser.
- **Bloodright collections in `plan`.** Opening one reads the live inventory, so use `run`.

## Limits and mapping

- The MCP endpoint allows 30 calls per rolling minute per user and per IP, across all paths. The
  pacer keeps the wire at 20 per minute by default (`--allowance`), on top of Forge's own
  per-path budget, which still mirrors the tRPC limiter and its fines on mutations.
- Errors arrive as the text `Error calling <endpoint>: <message>` with no code. The bridge recovers
  the code from the game's own wording (rate limit, unauthorized, registration, zod issues,
  "not found"). Anything else is a definite refusal (`MCP_ERROR`), never a success.
- A tool call that fails without an answer is ambiguous for a mutation, exactly as a dropped
  connection is in the browser. The item stays SENT and reconciliation settles it on resume.
- Results are plain JSON (no superjson), so dates arrive as ISO strings.

## Known risks

- **Answers come from the session record.** With `--transcript`, nothing is retyped. If Claude
  Code ever changes its transcript format, calls stop matching and the run simply waits; answer
  by hand as above. Answers written by hand must stay verbatim: a damaged capture carries the
  damage, while a damaged read-back shows up as a mismatch rather than a false pass.
- **Live so far: reads only.** `push/00_forge_readonly_smoke.json` ran live on 2026-11-07, twice
  (the second time answered entirely from the transcript, including a 320,135-character answer).
  No write has been sent over the connection yet.
