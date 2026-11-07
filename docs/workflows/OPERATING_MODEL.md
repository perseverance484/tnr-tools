# Operating model: who does what, and how a job reaches the game

Status: active from 2026-11-07 (RUL-2026-11-06-132, RUL-2026-11-07-133, RUL-2026-11-07-135).
The director decides and says go; agents build, run and check. This page is the routine. The
rules it relies on live where they are cited.

## Roles

| Who | Does |
|---|---|
| Director | Decisions, approvals, a "go" per job (or per chain). The Forge button only for image jobs nobody else can run. |
| Claude (this repo's builder) | Art, manifests, sims, gates, Forge code. Runs its own jobs over the game connection; reads live data directly. |
| Duet | Always-on: scans, reminders, morning status, live run-throughs and screenshots in its browser, announcements, image jobs through browser Forge. |
| ChatGPT | Independent review of Lane A code (`docs/DEVELOPMENT_WORKFLOW.md`), including Duet's. |

## 1. One runner at a time

Claim the run lock before any job or bulk read, release after (`docs/workflows/FORGE_MCP_RUNNER.md`,
"The run lock"). What is waiting, and on what, is `state/run_queue.json`; whoever builds, runs or
unblocks a job updates its row in the same commit.

## 2. The go card

A job reaches the director as a go card, not as a manifest to open:

```
GO? push/NNN <title>
What changes:  <one line per record kind, counts>   (e.g. 12 jutsu edited, 3 AI re-equipped)
Visible to players:  <yes/no, and what>
Gates:  validate --strict <exit>, check_manifest <exit>, ledger <ok/class>
Runner:  connector | browser (images)        Chain: <follow-ups this go also covers>
Needs you:  <decisions, or "nothing">
```

"go" runs it; "go NNN→MMM" approves a chain whose follow-ups are generated from the first job's
results bundle (e.g. create hidden, then unhide). After the run the runner commits the results
bundle, updates `state/run_queue.json`, and replies with the outcome in one line.

## 3. Image jobs

The game connection has no upload endpoint (the game uploads images through UploadThing, not
tRPC), so a manifest with new images runs in browser Forge. Duet's signed-in browser can run it
under the same lock and gates, so the director does not have to; failing that, the director's
Forge button. Everything else (edits, unhides, quests, AI, go-live) runs over the connector.

## 4. Live reads instead of capture jobs

A record needed to build an edit is read directly over the connector (jutsu, quest and AI edits
replace whole records, so read them back first). A capture manifest is only for a read the director
wants as a committed artifact. Bulk reads take the lock: they spend the same 30 calls a minute.

## 5. Job size

Masters existed to save button presses. Over the connector, keep jobs small and single-purpose:
they resume cleanly and their results bundles read easily. Combine only for a browser image run.

## 6. After any art change: look at it live

The connector checks mechanics (battle data: damage, effects, kills, cooldowns). Duet's browser
checks the picture (screenshots or GIFs of the cast, at real size, cold cache once). Both are what
"test on practice quest 469" now means, and both run before a go-live.

## 7. Deleting live content

`gameAsset.delete` (and the other deletes) check nothing: a record still used elsewhere breaks
silently. A delete job therefore ships with an inventory proving every target is unused (every live
record that can reference it, read under the lock), the director's go on that list, and the action
log as the only record of what was removed. Never delete what another staff member made unless the
director names it.
