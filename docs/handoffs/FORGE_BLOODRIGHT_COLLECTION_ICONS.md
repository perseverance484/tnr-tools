# Forge Bloodright collection and icons — implementation handoff

Date: 2026-10-16. Author: ChatGPT/Codex. Status: ready for independent code review;
**not a released loader or a ready all-roster production manifest**.

Repository: `perseverance484/tnr-tools`.
Branch: `chatgpt/bloodright-collection-icons-20261016`.
Exact base: `484d554b65954c18d04b62b00b31ad2b9057bfec` (PR #30).
Integration: stacked on `chatgpt/bee-pilot-values`; #29, then #30, then this change.
The exact frozen head is recorded in the PR handoff. Main observed at
`99e86dc549b86f1f4a5846c0e509fa6bc15b3463`; integration with it was not performed.
Brief: `state/prompt_bloodright_collection_icons.md`.

## Behavior

One `bloodrightCollection` package prepares every tree and verifies all pack-backed
icons before Start. Start runs independently scoped jobs sequentially, stopping on any
unverified/failed/paused child or explicit Pause. Whole-collection unresolved-job guards
run before the first child, then each child runs the original guards. Frozen preview
text and icon packs persist per job; exports retain collection identity/index/count.
Reload resumes only the selected frozen job. Reopening the collection prepares remaining
work afresh; completed children reuse without writes. No automatic restart on load.

Single-tree packages now forward `imagePack` and `imgSizes`. Per-category icon defaults
allow three images to serve the whole tree; explicit per-node images override them.
Existing images are preserved only when no replacement is specified. Uploads and preview
reuse use digest-backed upload history rather than filename-only URLs. HTTPS icon URLs
are also accepted; their remote bytes are not verified by the image pack machinery.

Core/API scope: no new public actions or top-level state keys, no changes to the runner's
single-bloodline provenance/lease model, recovery transitions, endpoint contracts or game.
`make_image_pack.mjs` now discovers category/node references in both package envelopes.
The collection template is deliberately blocked without its missing immutable icon pack.

## Verification

Node 24.19.0, full Git history, socket-free simulated game transport:

- `cd forge && npm test`: **575/575** pass (11 new collection tests, 1 pack-authoring test).
- Collection tests exercise actual Core selection/Start, two trees/26 records/six icons,
  per-node overrides, changed bytes behind the same name, idempotent rerun, corrupt bytes,
  post-preview replacement, missing icons, bad designs/settings, duplicate bloodlines/names,
  new unresolved jobs after preview, drift, lost updates, reload/resume, concurrent actions,
  Pause during persistence and Pause at a tree boundary. Starter refuses with zero writes.
- Two compiled icon manifests pass `validate.py --strict` from the skill data directory;
  both exported bundles pass `harvest.py verify` with 13 match / 0 failures each. These
  are simulated runs, not game evidence. The UI test renders collection/start/run labels.
- `npm run build` twice: byte-identical checked-in bundle SHA-256
  `2d3355c2fcb79a7a7f40e9959c0d369c83597fe223e356a40c14c8cccadeaa2a`.
- `node tools/check_bundle_budget.mjs`: **389,034 raw / 87,864 gzip**. Proposed ceilings
  **400,000 / 91,000**. Cost over PR #30: +7,735 raw / +1,744 gzip. This exceeds the
  prior candidate's raw 386,000 ceiling; the increase is explicit and **not approved**.
- `npm run fixtures`: no fixture changes.
- `node tools/check_imports.mjs`: 44 modules, 88 cross-layer imports, zero violations.
- `node tools/check_boundaries.mjs`: 44 source + 13 presentation modules, zero violations.
- `node tools/derive_bloodright.mjs /workspace/TheNinjaRPG --check`: byte-identical.
- `npm audit --omit=dev --audit-level=high`: zero vulnerabilities.
- `checkReleasePin()`: `[]`; loader remains 0.5.1, 0.6.0 pending.
- `skills/building-tnr-content/scripts/{doctrinemap.py,render_doctrine.py --check,build_packs.py --check}`:
  pass; `lawmap.py .`: zero errors, five existing warnings.
- `git diff --check`: clean.

## Source and remaining content

Game contract remains `studie-tech/TheNinjaRPG@1ccdaf078a58101872675e459c8e755b495d4c83`.
Legacy generated contracts remain at `345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9`.
The deployed website was not compared with either pin.

The dated source inventory is `forge/bloodright/collection.readiness.json`:
44 old four-BP designs at Fable `7c1dfdd5`; one newer five-BP structural BEE design at
`59638108`; icon tracker `c85c1ea8` describes 29 A/S/H sets, with six approved BEE/BBE
outputs whose binaries remain conversation deliverables. No image files or upload URLs
were found in that tracker. Actual icons and the latest intended trees are still needed.
The three BEE filenames/byte sizes in the blocked template come from its pinned QC report;
no art SHA is represented as a verified blob binding without the actual file.

No four-BP to five-BP conversion, new artwork, new tags, global price/duration ruling,
description acceptance, folder visibility change, push staging, main integration or
release was performed. The 20 Silver/99 rounds approval remains BEE-only.

## Review focus and limitations

Attack collection stop boundaries, stale selection/re-entry during awaits, icon provenance
through export/reload, and complete-preview refusal when the last tree is invalid. The
collection is sequential, not transactional: completed writes are never rolled back.
Inventory is double-scanned per tree under the existing read budget, so a large roster
can take substantial time. UI rendering is tested in jsdom; installed Android behavior,
download behavior for multiple exports, Clerk/staff sessions and real uploads are untested.
Cross-browser edits, storage eviction, source/deployment drift and the inherited release
conditions still apply. Budget approval includes the earlier importer budget increase.

Live-game requests: **0**. Game writes/uploads: **0**. Game credentials used: **none**.
No messages or PR comments sent to other people. PRs #29/#30 were read, not modified.
