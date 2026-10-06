# TNR Tools

Repository-backed content production, evidence and operator tooling for TNR.

Start with the task:

```sh
python3 scripts/tnr.py missions check --rank A
python3 scripts/tnr.py context missions.check --rank A
python3 scripts/tnr.py workstream init one_perfect_crop --task <task-id>
python3 scripts/tnr.py session          # optional read-only global summary
python3 scripts/tnr.py verify           # repository consistency gates
```

Mission checks use captured observations, show dates and coverage, and make no
live-game requests. A missing or stale generated view is derived in memory.
Without a checkout, resolve a GitHub ref to a commit and fetch
`answers/missions_A.md`; use `answers/missions_A.json` for detailed provenance
when needed, at that same commit.

| Location | Owner / purpose |
|---|---|
| `CHATGPT.md`, `CLAUDE.md` | Short agent entry points |
| `docs/00_INDEX.md` | Task routing and evidence precedence |
| `docs/DOCTRINE.md`, `docs/ENGINE_LAWS.md` | Shared rules and numbered laws |
| `skills/` | Canonical content/art tools and references; generated task packs |
| `state/workstreams/` | Per-project task coordination and durable evidence |
| `state/digest.json` | Global navigation; status/context are alternative generated views |
| `harvests/` | Original captures and historical seed catalogs |
| `answers/` | Generated query views, observed names and provenance |
| `push/` | Operator manifests; spent manifests move to `archive/` |
| `forge/` | Operator runtime, tests and build tools |
| `guide-studio/` | Guide application and its own gates |
| `art/`, `pack/` | Art sources and distribution packs |
| `dist/`, root bundles/configs | Generated compatibility/distribution artifacts |
| `.github/workflows/` | Installed automation; historical staged copies are retired |
| `archive/`, `docs/handoffs/`, `docs/reviews/` | Dated evidence, outside routine startup |

Shared rules are edited at their owner and projected with repository tools.
See `docs/RELEASE_DISTRIBUTION.md` before changing public root paths or release
pins. See `docs/DEVELOPMENT_WORKFLOW.md` before repository implementation or
integration. All live-game operations remain user-controlled.

Python tooling uses the standard library; the existing art lookup tests require
Pillow. Forge and Guide Studio retain their own Node dependencies. No new hosted
service, database or agent framework is required.
