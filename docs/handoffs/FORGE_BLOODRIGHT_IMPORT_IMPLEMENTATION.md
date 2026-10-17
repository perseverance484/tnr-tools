# Forge Bloodright import — implementation handoff

Repository: `perseverance484/tnr-tools`.
Branch: `chatgpt/forge-bloodright-import`.
Base / integration target: `main`, `5963810895aae4e2deaa61b72424c203752f50c1`.
Frozen implementation commit: `c807ecf9cc35b4d62ad33793259081d747c1c8e5`.
This handoff is a subsequent documentation-only commit; executable code is unchanged.
The final branch head is recorded in the review PR and delivery message.

## Result

Forge 0.6.0 compiles approved five-point structural Bloodright designs into staged website
records with authenticated discovery, explicit ID bindings, a field-level preview and
journaled writes. Existing Hungry Pulse is edited, its image is preserved, and subsequent
imports reuse IDs. The 12-node BEE fixture has 106 legal allocations and one reachable
Advanced Art. One import verifies 13 records; a second sends zero mutations.

Main changes:

- `forge/src/bloodright/`: deterministic compiler, scoped source projection and validation.
- Transport/reader/recipes: seven audited procedures, paginated inventory of BOTH skill paths,
  complete folder lookup, two-phase Bloodright creation and one-phase folder creation.
- Core/UI: package selection, create/update/reuse preview, blockers, frozen compiled text in
  separate repository-text storage, reload/resume, exported compiled manifest.
- Runner/journal/reconciliation: guarded read-only reuse, scoped persistent ID map, parent
  verification, preimage/binding checks, same-bloodline lease, explicit orphan adoption and
  role denial distinct from session expiration. Full skill point captures are allowlisted.
- Repository Python factory/validator bridge uses Forge's scoped validator. Harvest format
  stays compatible. Source extraction, tests, documentation, bundle and pending-release marker
  are included. The released loader's version and immutable bundle pin remain unchanged.

Approved brief: `state/prompt_forge_bloodright_import.md`.
Audit: `docs/reviews/BLOODRIGHT_IMPORT_SOURCE_AUDIT.md`.
Operator instructions: `forge/bloodright/README.md`.
Pilot package: `forge/bloodright/bee.pilot.json` (outside `push/` while decisions are missing).

## Verification

All executed locally without sockets in the behavior tests:

| Command / check | Result |
| --- | --- |
| `npm ci` in `forge/` | Passed, Node 24.19.0 |
| `npm test` in `forge/` | **546 passed**, 0 failed/skipped; 23 new Bloodright tests |
| `npm audit --omit=dev --audit-level=high` | 0 vulnerabilities |
| `node tools/check_imports.mjs` | 42 modules, 78 cross-layer edges, 0 violations |
| `node tools/check_boundaries.mjs` | 42 source + 13 presentation modules, 0 violations |
| `npm run fixtures` + diff | Envelope and 14 screen fixtures unchanged |
| `npm run build`, repeated byte comparison | Reproducible bundle |
| `node tools/check_bundle_budget.mjs` | 371,184 raw / 83,849 gzip bytes; ceilings 386,000 / 88,000 |
| `checkReleasePin()` | Clean; 0.6.0 pending, released 0.5.1 pin preserved |
| `node forge/tools/derive_bloodright.mjs /workspace/TheNinjaRPG --check` | Exact regenerated scoped contract match; clean pinned source |
| `factory.py --selftest` from skill data directory | 20/20 passed |
| Actual Python `validate.py --strict` and `harvest.py verify` in Bloodright tests | Compiled manifest accepted; 13 records verified |
| `doctrinemap.py` | 0 errors, 0 warnings |
| `render_doctrine.py --check` | All projections current |
| `build_packs.py --check` | All packs/TOCs current |
| `lawmap.py` | 0 errors; 5 existing coverage warnings |
| `git diff --check` | Clean |

Bundle SHA-256: `a6e498fa666586777456e3ac03198a5e3e0c33f97212704cf22f70de805b1093`.

The scoped game pin is `1ccdaf078a58101872675e459c8e755b495d4c83`. Generation reads
validators/router/constants and verifies their working files against that commit. The new
projection contains source hashes, fields, spread-expanded element enum, potency targets and
procedure metadata. Bounds and the narrower potency-only import policy are audited code.
The legacy global contract remains at `345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9`; neither
legacy fields nor nested contracts were refreshed. The source audit documents adoption
scope and the differences that make legacy potency validation inappropriate here.

## Review targets and remaining decisions

- Hungry Pulse's 20 Silver / 99 rounds are screenshot evidence for that node only. Eleven
  other costs/durations are deliberately null and block the live pilot. No prices were invented.
- Hidden-node visibility is proven through a known hidden skill read, not a profile/role dump.
  Content-writing permission is ultimately enforced by the server; role denials are distinguished.
- Lost creates ALWAYS require ownership confirmation, even with one candidate. This is more
  conservative than legacy reconciliation because there is no server idempotency key.
- No compare-and-swap or cross-browser transaction exists. Remote edits can race after the last
  preimage read. Readback is mandatory; same-browser leases are not a distributed lock.
- Corrupt/evicted frozen text blocks resume. Exports contain the exact compiled manifest, but
  restoration is currently manual; no new restore UI was added.
- This release supports the current structural `bonuses` schema and audited potency effects.
  Older four-point `modifiers` trees require separate design conversion. SVG placement itself
  is not a website import field. New nodes retain server placeholder art unless supplied.
- Python bridge requires Node 24 and the repository checkout; standalone skill packs fail
  explicitly. The bundle budget increase pays for the scoped importer and is visible for review.
- Attack the reuse transition guard, mixed-pin isolation, paginated hidden inventory, stale
  binding handling before resume synchronization, and ambiguous-create ownership in review.

No independent review has been claimed or completed. No merge or release has begun.
No game writes, player refunds, deletions, publication, art generation, or engine changes were
performed. Implementation/tests made no live game requests and used no live session material.
Earlier source analysis made the public read-only GET observations recorded in the audit.
A real browser/Clerk staff session and the deployed website contract have not been pilot-tested.
