# tnr-tools

Tooling, canon and data layer for TNR content production. Maintained by dauntless.

| Path | Function |
|---|---|
| root `*.js` + `45c` / `45g` / `32b` | builder userscript runtime; the panel fetches these three JSON at load |
| `/skills/` | canonical source of both Claude skills (tools, references, data). Patches land here first |
| `/dist/` | installable skill zips, rebuilt by the `skillpack` workflow on any `/skills/` push |
| `/answers/` | generated lookup layer (name/id/hidden per entity + `INDEX.md`), rebuilt by the `answers` workflow on any `/harvests/` push |
| `/harvests/` | committed harvester dumps and catalog seeds; the answers input |
| `/docs/` | `ENGINE_LAWS.md` (canonical numbered law text) |
| `/archive/` | retired documents, STALE-bannered. Do not build from them |

Workflows: `answers` and `skillpack` commit back with `GITHUB_TOKEN` (loop-safe); `scrub`
gates every push on the `SCRUB_STRING` secret and fails the build on a privacy hit.
Generated 2026-08-28.
