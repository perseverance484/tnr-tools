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
   then reads every page of both SKILL and BLOODRIGHT and all accessible folders.
3. Review create/update/reuse, target IDs and field-level before/after changes. BEE reports
   **106 legal allocations** and **one reachable Advanced Art** with five BP. Missing
   decisions disable Start.
4. Start the reviewed job. Changed preimages pause as `STALE_PREVIEW`; changed bindings
   pause as `STALE_BINDINGS`.
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
Legacy `modifiers` files and other combat effects are refused. Bindings cannot identify SKILL
rows, another bloodline, or already visible skills. Global name conflicts block preparation.

## Persistence and recovery

IDs use `br:<bloodlineId>:<localNodeId>` keys in Forge's existing ID map, exported in every
result bundle. The reserved local key `folder` identifies the folder. Explicit bindings that
conflict with saved IDs block preparation. Back up results before clearing browser storage.

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
drift; coordinate live editing during the pilot.

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
`harvest.py` consumes the existing Forge results dialect without a new ingestion format.
