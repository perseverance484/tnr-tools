> **STALE - archived 2026-08-28 (rollout Stage 1).** merged into project 00_INDEX.md.
> Do not build from this file.

# 01 - Precedence

When two sources disagree, this decides. Every row cost something real.

| Disagreement | Winner | Why |
|---|---|---|
| Live game content vs our doctrine | **Doctrine** | Live shows what the engine accepts, not what we chose |
| Catalog vs a fresh capture | **Capture** | Catalogs are snapshots and drift silently |
| Engine law vs a session finding | **The finding, if it cites evidence**; otherwise the law | A failed push is evidence; a hunch is not |
| Tool in a skill vs tool in the bundle | **Bundle** | Patches are strictly newer; a reinstall reverts them |
| `12b_LAWS_coverage.md` vs the validator's actual code | **The code** | The matrix documents a tool that has since been replaced |
| Generated file vs prose restating it | **Generated file** | Laws cite, never restate |
| Anything vs a file nobody read | **Read the file** | Four quest-flow rules were all visible in a live record nobody captured |

## Surface conflicts, do not resolve them silently

If two sources disagree and this table does not obviously settle it, say so and ask. A blended
answer from two incompatible sources looks confident and is wrong.

## The expensive one

**Live content is storage, not intent.**

Storage tells you what exists. Intent tells you what we meant. Reading one as the other is the
single most repeated mistake in this project:

- Live quests converge their choice menus, so the no-convergence rule got demoted. It should not
  have been: law 27 has said so in writing the whole time. Live content was the older pattern.
- Every live location node carries `sector: 0`, so it got written onto 85 new nodes. It is a
  column default across three different `sectorType` values, including ones where 0 cannot
  describe the real sector.

Both times the question asked was "what does live do?" The right question was "does live doing it
make it a decision, or just a fact?"

## Evidence tiers

Use these words precisely when recording a finding. They decide whether it can overturn a law.

| Tier | Means | Can overturn a law |
|---|---|---|
| **Source-verified** | read in the TNR source, file and line cited | yes |
| **Behaviour-proven** | a push or capture demonstrated it, bundle cited | yes |
| **Observed** | seen in live data, not yet explained | no, propose it |
| **Inferred** | reasoned from other laws | no |
| **Assumed** | nobody checked | no, and say so out loud |

An unresolved assumption worth carrying: we write `longitude` as x and `latitude` as y. Nothing
in any capture distinguishes them. Tier: **assumed**.
