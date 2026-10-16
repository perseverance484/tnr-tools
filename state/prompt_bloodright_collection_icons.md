# Bloodright collection and icons

User request, 2026-10-16: "I want to be able to push a manifest to import all my bloodright trees with their icons."

Implementation branch: `chatgpt/bloodright-collection-icons-20261016`, based on
PR #30 at `484d554b65954c18d04b62b00b31ad2b9057bfec`. PRs #29 and #30 remain frozen.
This is Lane A tooling plus a content-readiness inventory. No live requests.

Implement one `bloodrightCollection` package containing multiple existing structural
tree configurations, plus a shared immutable `imagePack` and `imgSizes`. Support
Foundation/Hidden Art/Advanced Art icon defaults and explicit per-node image overrides.
Prepare and validate every tree and every icon before Start; reject duplicate bloodlines,
cross-tree name collisions, missing icons and unsupported designs. Preserve single-tree
packages and their current image-preservation behavior.

Execute separate scoped, frozen Bloodright jobs sequentially after one Start. Stop on
pause, failure, drift, lost visibility or explicit Pause; never start later trees after
an incomplete tree. Each job keeps existing leases, provenance, preimages, recovery,
ID maps and export. After reload, resume the current job normally, then reopen the
collection to prepare remaining work; completed trees should reuse without mutations.
Never recompile an active job or automatically resume writes on page load.

Tests must use the real Core selection/Start path, mock transport only, and cover icons,
cross-tree refusal, interrupted execution, reload/resume and repeat-import no-op behavior.
Run Forge tests/build/import boundaries/budget/fixtures and source-contract check.

Content evidence found: BEE has the updated five-BP structural JSON at `59638108`.
The 44-tree Fable roster at `7c1dfdd5` uses legacy four-BP modifiers and must not be
silently migrated. The icon tracker at `c85c1ea8` describes 29 A/S/H sets, six approved
BEE/BBE images, but contains no image binaries or upload URLs. Ask for the newer
collection location; do not manufacture artwork, URLs, prices or tree mechanics.
The 20 Silver/99 rounds ruling remains BEE-only. No release, main merge or live pilot
is implied by implementing this capability. Record measured bundle growth explicitly.
