# Bloodright imports in Forge 0.6.0

Forge prepares a five-point structural Bloodright design as a reviewed, hidden website
import using the existing `skillTree` API and game-page session. The SVG remains a design
artifact: importing creates skill records and prerequisites, not an SVG on the game page.

## BEE pilot

`bee.pilot.json` names the approved 12-node BEE design at tools commit
`5963810895aae4e2deaa61b72424c203752f50c1`. It explicitly binds:

- Bloodline: `ovZIWu28ANn-Cij5TjT8S` (from the design).
- Folder: `kvxMu9ntHbNcD6FFHKGo3` (existing, remains visible).
- Hungry Pulse (`p2_t1`): `HWq7986PPhl5emkAM3L4a` (existing image preserved).

Hungry Pulse has 20 Silver / 99 rounds from the supplied screenshots. The other eleven
nodes have `null` prices and durations. Fill each with approved values. Zero Silver is valid;
omitted/null Silver is not. Rounds must be 1–100. The compiler creates plain mechanical
descriptions; optional `description` and `image` per node override them. It does not invent
balance values or generate art.

After review and the normal release process, stage the completed package under a numbered
`push/*.json` filename. Forge's manifest picker recognizes its `bloodright` envelope.
Opening it prepares the preview with queries only; preparation never rewrites source files.

1. Sign in to TNR with content-writing and hidden-skill access, then open Forge.
2. Select the package. Forge proves visibility of the known hidden Hungry Pulse ID,
   then reads every page of both SKILL and BLOODRIGHT twice and requires the complete
   results to agree. Accessible folders are also read.
3. Review create/update/reuse, target IDs and field-level before/after changes. BEE reports
   **106 legal allocations** and **one reachable Advanced Art** with five BP. Missing
   decisions disable Start.
4. Start the reviewed job. Changed preimages pause as `STALE_PREVIEW`; changed bindings
   pause as `STALE_BINDINGS`. Missing target visibility pauses immediately as `VISIBILITY`,
   retaining the current item for resume instead of creating further placeholders.
5. Save the exported results. Verify all 13 records (folder plus 12 skills), then prepare
   the package again. It should show only reuse and send **zero mutations**.

The released loader stays pinned to 0.5.1 while 0.6.0 is pending review/release; this branch
does not redirect the loader or repository reads. No pilot game write was performed.

## Package contract

```json
{
  "_note": "Bloodright import",
  "bloodright": {
    "version": 1,
    "source": {"path": "docs/design/bloodright/examples/blood_enchanted_eyes_structural.json", "ref": "5963810895aae4e2deaa61b72424c203752f50c1"},
    "hiddenProbeId": "HWq7986PPhl5emkAM3L4a",
    "bindings": {"folderId": "kvxMu9ntHbNcD6FFHKGo3", "nodes": {"p2_t1": "HWq7986PPhl5emkAM3L4a"}},
    "nodes": {"p2_t1": {"seichiSilverCost": 20, "rounds": 99}}
  }
}
```

The abbreviated example requires settings for the other nodes before it can run. For a new
folder, omit `bindings.folderId` and supply `folder` with a unique name and optional image,
description and order. New folders are hidden. Duplicate names require explicit ID bindings;
existing folders are reused unchanged.

Structural designs must use `nodes[].bonuses`, one point per skill, five BP and ALL
prerequisites. Only audited potency tags with explicit qualifying elements are supported.
Leading/trailing whitespace in skill names, legacy `modifiers` files and other combat effects
are refused. Bindings cannot identify SKILL
rows, another bloodline, or already visible skills. Global name conflicts block preparation.

## Persistence and recovery

IDs use `br:<bloodlineId>:<localNodeId>` keys in Forge's existing ID map, exported in every
result bundle. The reserved local key `folder` identifies the folder. Explicit bindings that
conflict with saved IDs block preparation. Back up results before clearing browser storage.

An unresolved job for the same bloodline blocks preparation, Start, and execution of a second
job, even if settings or the manifest hash change. The guard checks SENT, ORPHANED and
CONFIRMED items in the persistent journal, including older jobs identified by scoped IDs.
Resume that job or explicitly resolve its pending writes before preparing another import.

If a CONFIRMED item remains drifted or unreadable and you choose to stop recovery, open
the paused/incomplete job and use **Mark failed (leave as is)** beside that item. Confirm
the prompt. This records an operator failure, preserves its target ID, saved binding and
drift evidence, and sends no game request. It does not accept the write as verified or let
dependent skills in that job run. Reconcile all SENT items first; the action is unavailable
while a job is running and refuses another tab's active lease. Resume remains the preferred
option for temporary visibility loss.

Once all unresolved items have been resolved, prepare a fresh preview against current
records. A target that was deleted still needs its binding repaired explicitly; marking it
failed does not erase the remembered ID or authorize an automatic replacement. Export the
old job to retain the resolution and verification evidence.

The compiled manifest, preimages, source pin and bindings are frozen into job identity.
The exact text is stored in the separate repository-text IndexedDB database before opening
the job; exports additionally include `compiledManifest`. Reload resumes this text, never a
recompiled design. Missing/evicted text blocks resume until the exact saved text is restored
to the job's recorded `bloodright.manifest` cache key. There is no automatic restore UI in
this release. Do not start a duplicate job to bypass an unresolved create.

Skills use create-then-update; folders use one-phase creation. Parents must verify before
children run. Interrupted updates are read and compared, never blindly resent. Lost create
responses become ORPHANED even with one matching candidate: the API has no idempotency key,
so another editor could own that candidate. Inspect it, then adopt or skip through Forge's
existing recovery controls. Folder adoption goes straight to verification. Skill adoption
may fill only the matching hidden Bloodright placeholder, or verify an already exact record.

Role denials use `PERMISSION` and leave session state intact; expiration uses the existing
`SESSION` flow. No full player-profile reads are used to discover roles. Server purchase and
dependent guards remain authoritative. The importer never refunds, deletes or publishes.
Same-browser leases serialize imports of a bloodline. The server has no compare-and-swap or
cross-browser lock: remote edits can race between the last read and update. Readback detects
drift; coordinate live editing during the pilot. Offset pagination is not a transaction either:
two matching scans detect the reviewed deletion/omission case and other observed changes, but
cannot prove an atomic snapshot under continuous or adversarial concurrent edits. Each scan
uses the normal request budget; no partial or inconsistent result is returned/cached.

## Contract and repository tools

```sh
node forge/tools/derive_bloodright.mjs /path/to/TheNinjaRPG --check
```

The checkout must be at `1ccdaf078a58101872675e459c8e755b495d4c83` with unchanged source
files. The generator extracts fields, potency targets, spread-expanded elements, procedure
metadata and source hashes. `src/bloodright/validate.mjs` applies audited bounds and the
narrower import policy. Legacy `fields.json` and `nested.json` retain their `345d18ac` pin.

Python `Factory.entry` and `validate.py` delegate the two new entities to
`forge/tools/validate_bloodright.mjs` over JSON stdin. Node 24 and a full checkout are required;
a standalone skill pack fails explicitly instead of falling back to stale schemas.
Bloodright write manifests must carry the compiler provenance, dedupNames:true, and an explicit
binding plus frozen preimage for every edit. Hand-written skill/folder manifests without those
checks are refused. Python `Factory.manifest` accepts `bloodright_import=` for assembling an
already prepared envelope; entry construction alone does not authorize a runnable manifest.
Read-only skill captures remain available without compiler provenance.
`harvest.py` consumes the existing Forge results dialect without a new ingestion format.
