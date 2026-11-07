# Forge over the game connection (MCP runner)

Runs a Forge manifest without a browser tab. The same Forge runner, journal, budget, reconciler
and results bundle are used; only the wire changes. Instead of the signed-in game tab, each game
call goes through the game's own MCP endpoint, called by a Claude session that has the game
connected as a connector.

Code: `forge/src/hosts/mcp/` (bridge, pacer, file hand-off), `forge/tools/mcp_run.mjs` (CLI),
tests in `forge/test/mcp.bridge.test.mjs`. The userscript bundle does not import any of it.

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

## A run (the Claude session holding the connection)

From the repository root, on an up-to-date `main` checkout:

```
node forge/tools/mcp_run.mjs plan push/412_x.json
```

Offline. Parses, plans and pre-send validates exactly as Forge does when a manifest is opened.

```
node forge/tools/mcp_run.mjs run push/412_x.json --state <state dir>
```

Run it in the background. For every game call it writes `<state dir>/exchange/request.json`:

```
{"id": "...", "tool": "callEndpoint", "arguments": {"endpointName": "...", "input": {...}},
 "kind": "query" | "mutation", "answerFile": "answer-<id>.txt", "errorFile": "answer-<id>.error.txt"}
```

The session makes exactly that `callEndpoint` call with exactly those arguments, then writes the
tool result's text verbatim to `<state dir>/exchange/<answerFile>`. If the tool call itself
failed, it writes the failure text to `<errorFile>` instead. Never edit, summarise or reformat an
answer: Forge verifies writes against it and stores captures from it.

When the job ends, the results bundle is written to `harvests/inbox/` in the working tree (the
CLI's "committed" line means written there). Commit it to `main` as usual. `resume <jobId>` picks
up a paused job, and `jobs` lists the journal. Both use the same `--state` directory. Keep it in
`/mnt/project-files/` so a later session can resume.

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

- **Answers travel through the session.** A large record (a full quest or AI) is copied from the
  tool result into the answer file. Keep answers verbatim. A capture whose text was damaged would
  carry the damage, while a damaged read-back shows up as a mismatch rather than a false pass.
- **Not yet run live.** The first live run should be a small read-only capture.
