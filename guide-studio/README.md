# TNR Guide Studio

Astra’s implementation of the handoff at `87fb673938d915c0732351d2efb208d05ef38c7c`: two complete editorial templates, local player authorship, final-artifact staff review, immutable signed packages, and an isolated native TNR draft importer. This is an independent-review candidate, not a deployed service.

## Run locally

Requires Node 24. From `guide-studio/`:

```sh
npm ci --ignore-scripts
npm run gate
npm run dev
```

Open `http://localhost:4173`. `/staff` is the local staff harness; `/local-importer.html` runs native game mocks. The harness accepts only localhost Host headers and uses memory storage and ephemeral signing keys. Restarting discards submissions. Do not expose it publicly. The production build deletes harness files.

Choose a bloodline, select and order a build, write inline HOW I USE IT notes, then write thematic chapters. The complete kit and special system render even with an empty loadout. Public authoring uses committed static data and same-origin art, with no game transport or credentials. Drafts autosave; download/recovery controls, cross-tab conflict detection, and private feedback receipts support recovery and revision.

Staff opens the exact content and asset bytes, begins review, and approves its package hash. D1 compare-and-swap freezes approval. The ZIP contains `submission.json`, `game-guide.json`, `content.html`, `assets-manifest.json`, `metadata.json`, `approval.json`, `README.txt`, and generated SVG/WebP assets.

The separate TNR-side importer verifies the configured public approval key, package hashes, and origin before enabling **Import draft guide**. One explicit click creates/updates the native guide and verifies every approved field through readback. It reports the guide ID and a receipt. `published` is always false; publication remains a separate staff action. All development mutations use mocks.

| Path | Responsibility |
|---|---|
| `templates/`, `catalog/`, `fixtures/`, `public/assets/` | Locked foundation, captured mechanics, official art and provenance |
| `src/` | Editorial UI, drafts, schema, semantics, renderer and package format |
| `server/` | Turnstile, Access, queue, immutable storage and approval signing |
| `importer/` | Native tRPC adapter, staff panel and recovery journal |
| `compatibility/` | Pinned game source, constants, generated runtime and hashes |
| `test/`, `scripts/` | Regression harnesses, read-only refresh and deterministic builds |

`npm run fixtures` writes self-contained previews and artifact files under `test-output/fixtures/`. `python3 scripts/card-gallery.py` renders static 360px card inspections (CairoSVG 2.9.1; Pillow 12.3.0). These are not browser screenshots.

See [implementation review](docs/IMPLEMENTATION_REVIEW.md), [catalog provenance](docs/CATALOG_PROVENANCE.md), and [deployment](docs/DEPLOYMENT.md).
