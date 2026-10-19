# Bloodright imports in Forge 0.6.0

Forge prepares a five-point structural Bloodright design as a reviewed, hidden website
import using the existing `skillTree` API and game-page session. The SVG remains a design
artifact: importing creates skill records and prerequisites, not an SVG on the game page.

## BEE pilot

> Superseded for import by the naming-pass collections below (RUL-2026-10-17-003): BEE now
> uses the CSV names and bonuses. Do not run `bee.pilot.json` or `collection.template.json`
> alongside them; they target the older pilot design and would rename BEE nodes.

`bee.pilot.json` names the approved 12-node BEE design at tools commit
`5963810895aae4e2deaa61b72424c203752f50c1`. It explicitly binds:

- Bloodline: `ovZIWu28ANn-Cij5TjT8S` (from the design).
- Folder: `kvxMu9ntHbNcD6FFHKGo3` (existing, remains visible).
- Hungry Pulse (`p2_t1`): `HWq7986PPhl5emkAM3L4a` (existing image preserved).

All 12 BEE nodes use **20 Silver / 99 rounds**, approved by the user on 2026-10-08
(RUL-2026-10-08-002). This completes the pilot price/duration settings. Zero Silver is valid;
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

Integrated into main on 2026-10-17 on top of the released 0.5.2 loader (`b62704c0`) and its AI
validation changes. The loader carries `@x-release-pending 0.6.0`; the release-pin workflow
promotes it after the merge. No pilot game write was performed.

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

## Multiple trees and icons

The collection candidate adds a `bloodrightCollection` envelope to the same picker.
Start imports its trees in order, as separate scoped jobs. All trees must compile and
all referenced icon bytes must verify before the first job opens. A bad final tree or
icon therefore blocks the entire initial run. Each child still checks its scope, session,
bindings and preimages when it starts. This is sequential execution, **not a transaction**:
completed trees remain saved if a later tree stops.

```json
{
 "_note": "My Bloodright trees with icons",
 "bloodrightCollection": {
  "version": 1,
  "trees": ["REPLACE with complete bloodright configuration objects, one per bloodline"]
 },
 "imgSizes": {},
 "imagePack": {"ref": "REPLACE with the exact art commit", "files": {}}
}
```

This shape illustration is intentionally not executable. Each `trees` entry is the
same configuration object used under the single-tree `bloodright` key, with optional
category defaults:

```json
"icons": {
 "Foundation": "@img:bee_foundation_black_bg_256.webp",
 "Hidden Art": "@img:bee_hidden_art_black_bg_256.webp",
 "Advanced Art": "@img:bee_advanced_art_black_bg_256.webp"
}
```

`nodes.<id>.image` overrides the category icon. Icons may instead be exact HTTPS URLs
already supplied by the operator; URL-only icons are assigned without uploads (their
remote bytes are not hash-verified). Collections require an explicit icon for every
node. Single-tree packages without icons keep the old image-preservation behavior.
Category icons explicitly replace existing images, including Hungry Pulse's when selected
(approved, RUL-2026-10-17-002).
New folders may also use an image reference; bound existing folders remain unchanged.

For automatic image upload, put `imgSizes` and `imagePack` at the **package top level**,
outside `bloodright` or `bloodrightCollection`. Every collection `@img` must be bound
to an immutable pack; the collection never falls back to the device picker. One shared
file can serve many skills. Upload reuse uses the content digest, not just its filename.
Preview also uses the content upload ledger, so repeat imports show reuse rather than
claiming that an unchanged uploaded icon needs replacement. Back up results and browser
storage: losing the upload ledger can require uploading the same bytes again.

After committing the actual approved WebPs and recording their byte sizes, use the existing
authoring tool (now aware of category and node icons):

```sh
node forge/tools/make_image_pack.mjs my-trees.json --root art/bloodright --ref ART_COMMIT --write
```

Use repeatable `--map filename.webp=art/path/filename.webp` arguments for files in different
folders. It hashes **committed blobs**, rejects missing files and ledger mismatches, and
pins the resolved commit. It does not approve artwork or replace art preflight. Forge
validates the compiled per-tree manifests against the same scoped contract as the pilot.

Operation:

1. Select the collection; inspect all tree previews and the verified image ledger.
2. **Start all trees** writes one tree at a time. A pause, failed item, visibility loss,
   drift, or explicit Pause stops the collection before any later tree starts.
3. Export/retain each tree's results. Exports carry collection ID/index/count as well as
   the exact frozen compiled manifest and icon pack.
4. After interruption or page reload, resume the current job using Jobs. This resumes its
   exact saved manifest only; it does not automatically start the rest of the collection.
5. Reopen the collection for a fresh preview. Finished trees should show reuse; Start
   verifies them without mutations and proceeds to the remaining trees. Any unresolved
   child blocks the new collection. Missing frozen text still refuses resume safely.

Preparation currently performs the existing complete double inventory scan **per tree**;
the normal budget throttles reads. Large rosters can take substantial time to preview.
There is no collection-wide rollback or cross-browser lock. Avoid concurrent edits.
Duplicate bloodline entries and cross-tree skill/folder name collisions are refused;
different trees may explicitly reuse the same existing folder unchanged.

### Production inputs located on 2026-10-16

`collection.template.json` contains the real BEE settings and the three icon filenames/
byte counts from the recorded BEE QC report. It intentionally lacks an imagePack because
the repository has no corresponding image blobs. **It is blocked, not a staged manifest.**
Do not invent a commit or URL to fill it. `collection.readiness.json` records the exact
44-tree roster scanned and source pins:

- Fable `7c1dfdd5` contains 44 legacy four-BP trees using `modifiers` (6–10 nodes each).
  These are not silently converted into five-BP designs.
- The updated structural BEE tree is available at `59638108`; no other updated
  structural tree was found on the inspected Bloodright branches.
- Icon tracker `c85c1ea8` plans 29 A/S/H bloodlines / 87 icons and records six approved
  BEE/BBE images. It explicitly says those binaries remain conversation deliverables.
  No immutable image blobs or uploaded URLs are supplied there.

The complete package needs the latest intended trees, actual icons (or exact uploaded
URLs), and explicit node settings for those trees. The approved 20 Silver / 99 rounds
settings were BEE-only when written; RUL-2026-10-17-003 now applies them as placeholders to the naming-pass trees. Description acceptance, folder visibility,
release and live execution remain the earlier separate decisions. Nothing is newly
staged under `push/`, merged, released, uploaded or sent to the game by this change.

## Naming-pass collections (RUL-2026-10-17-003)

The naming pass (`docs/design/bloodright/naming_pass/review.csv`) covers 25 bloodlines. Their
five-point designs are generated, never hand-edited:

```sh
python3 scripts/bloodright_from_naming.py [--check]          # docs/design/bloodright/structural/
python3 scripts/bloodright_collection_package.py [--icons-ref SHA] [--check]
```

The first script reads the legacy tree metadata from `docs/design/bloodright/trees/*.json`,
byte-identical copies of `fable/bloodright-planning-20261003` checked against the blob ids in
`trees/SOURCE.json`.

The second script writes two collections. Bonuses are the scorer-v1 rebalance
(RUL-2026-10-18-006; Shiroi Youso keeps its CSV placeholder); 20 Silver and 99 rounds remain
placeholders.

- `naming_pass_collection_a.json`: 15 trees using only the original ten potency tags. This
  works with the current Forge contract.
- `naming_pass_collection_b.json`: 10 trees using pierce, absorb, poison, drain, consume
  or vamp. These need the contract re-pinned to TheNinjaRPG `94f9d84` and a
  live game running upstream `133e2c7` or later. Import A first, then B.

Cosmic Ascendant and Shiroi Youso use the element `None` as a placeholder until their
classification is resolved (RUL-2026-10-17-004); their bonuses then only reach jutsu without
an element. The package script pins `DESIGN_REF`; after
changing designs, commit them, update `DESIGN_REF` and rerun. Merge with a merge commit. New trees create a hidden
folder named after the bloodline. If a folder with that name already exists, preview refuses
and the folder must be bound by ID. BEE binds its existing folder and Hungry Pulse.

Icons go in `art/bloodright/<slug>/{foundation,hidden_art,advanced_art}.webp`, where `<slug>`
is the design's file name. Commit them, then rerun the package script with
`--icons-ref <that commit>` to bind every icon to an immutable image pack. Until then both
files are BLOCKED templates and must not be staged in `push/`.

Before staging, run `validate.py <package> --strict` from `skills/building-tnr-content/data`.
For a collection it runs Forge's own `prepareCollection` offline
(`forge/tools/validate_bloodright_package.mjs`). Designs come from this checkout at each
tree's pinned ref, and the image pack and byte ledger are parsed. Each icon blob is verified at
the pack ref: it must exist, match its SHA-256 and byte count, fit the 524,288-byte upload
ceiling, and sit on a pushed branch (a remote-tracking branch must contain the pack ref; commits
reachable only from tags or PR refs are refused offline even though GitHub would serve them). Only live facts (bindings exist and are hidden, no
global name or folder collision) are left to Forge's preview.
Skill icons render as 48 px and 64 px circles (`object-cover`), so keep the subject centred.
Check them with `artpreflight.py --type JUTSU_ICON --max-bytes 524288`; the opaque route
is allowed, and 524,288 bytes is Forge's upload ceiling.

## Persistence and recovery

Compiled Bloodright manifests record the game-contract pin. After a Forge update that
changes the pin, a job compiled by the previous bundle can no longer be resumed: it is
refused, not misapplied, and it still blocks new imports for its bloodline. Finish or close
every open Bloodright job before switching to a bundle with a new pin.

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

For a target you have independently confirmed was deleted, repair its binding without
editing browser storage:

1. Export the old job. Resolve all SENT/ORPHANED/CONFIRMED items for this bloodline first;
   a merely invisible target may still exist, so restore access before concluding deletion.
2. In the old job, find the FAILED or VERIFIED item and choose **Forget saved binding**.
   Confirm the exact name and ID. The action refuses unresolved same-bloodline jobs, running
   work, another tab's lease, or a saved ID that changed after the button was displayed.
3. If the package explicitly names that old ID in `bindings.nodes` or `bindings.folderId`,
   remove it to propose a new record, or replace it with the intended existing record's ID.
   A new folder also needs `folder` settings. If the deleted record was `hiddenProbeId`,
   supply another known existing hidden skill as the access probe.
4. Select the package again and review its fresh create/update preview. Forgetting sends
   no game request and does not itself create, delete, or rebind any server record.

Only the selected saved binding is removed. Its old ID and item evidence remain in the
journal/export. All existing jobs that reference that source key are marked as invalidated;
they cannot restore the old ID or continue their writes. The current selection is cleared,
and a fresh job can reuse the same manifest hash when the prior job was explicitly invalidated.
Other unresolved obligations still block new preparation. Export the old job again to retain
the forgotten-binding record. **Mark failed** alone continues to preserve every saved binding.

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

The checkout must be at `94f9d84c770004172ba423ada3d6710849acc451` with unchanged source
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
