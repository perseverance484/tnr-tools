# tnr-tools

Deploy truth for the TNR content pipeline.

ROOT (load-bearing, referenced at runtime):
- builder_bundle.js  - the content builder (v4.20). Loaded by the ViolentMonkey loader via @require.
- builder_loader_user.js - install this in ViolentMonkey; bump ?v on bundle updates.
- 45c_DATA_constructors.json + 32b_DATA_pool.json - generated config fetched by the bundle at load.
  The panel title must read "cfg generated"; "fallback" means these two are missing from root.
- capture_example.json - manifest capture-block reference.

archive/ - retired reference data (full catalogs, superseded schemas, analysis dumps). Nothing reads
these at runtime; they exist so history is not lost.

Deploy: commit to root, verify the BLOB view shows the new version (raw CDN caches ~5 min), bump the
loader ?v, reload the game page.
