# 00 - TNR content generation: router (mounted 2026-08-30)

TNR is an open-source Next.js / tRPC / Drizzle web game at theninja-rpg.com. dauntless is a
contributor on content staff, working from Samsung Android in Firefox with ViolentMonkey.
Claude turns concepts into validated builder manifests and commits them to push/; dauntless
replays them against the live game through the hosted builder userscript. There is no staging
environment. Never copy proprietary text, never reference the Naruto franchise.

**This file routes and arbitrates. It does not teach.** docs/DOCTRINE.md is the single
source for cross-surface rules (rendered outward; [[D-...]] anchors below reference it).
docs/10_LAWS_core.md holds the
cross-cutting laws; docs/ENGINE_LAWS.md is the numbered text of record. Everything else lives
where the work happens and loads only when it does.

## The layers

| Layer | Holds | Changes |
|---|---|---|
| Project instructions | short task bootstrap and non-negotiables | dauntless pastes |
| This repo | everything else: tool canon `/skills/`, laws `/docs/`, `/answers/`, `/harvests/`, staged `/push/`, `/state/`, `/archive/` | every commit; Claude pushes |
| Builder userscript | the push path; panel fetches `45c`/`45g`/`32b` from repo root; ⇩ Repo lists `push/` | ViolentMonkey refresh |
| Game source | `studie-tech/TheNinjaRPG`, public, clonable; contracts are extracted, never guessed | upstream commits |

Task state is the selected `state/workstreams/<slug>/roadmap.json`. The global
`state/digest.json` is a navigation summary; `active-context.md` and `status.json`
are alternative generated views. Historical closeouts are evidence dated at close.

Storage is what IS. Intent is what we MEAN. Live content, captures, catalogs and answer files
are storage; doctrine, state and rulings are intent. Reading one as the other is the most
repeated mistake in this project; the precedence table exists to stop it.

## Precedence

When two sources disagree, this decides. Every row cost something real.

| Disagreement | Winner | Why |
|---|---|---|
| Live game content vs our doctrine | **Doctrine** | Live shows what the engine accepts, not what we chose |
| Catalog or answer file vs a fresh capture | **Capture** | Snapshots drift silently |
| Extracted source contract vs a capture | **Contract for what fields ARE; capture for what records HOLD** | Extraction owns contracts, capture owns live state (law 83) |
| Engine law vs a session finding | **The finding, if it cites evidence**; otherwise the law | A failed push is evidence; a hunch is not |
| Tool in a skill install vs tool in the repo `/skills/` tree | **Repo** | The repo is canon; skills are packaged from it |
| Coverage matrix vs the validator's actual code | **The code** | `lawmap.py` makes this a command, not a discipline |
| Generated file vs prose restating it | **Generated file** | Laws cite, never restate |
| Stamped generated file vs a fresh re-extraction | **Neither, until structurally diffed** | The SECTOR_TYPES collision would have shipped silent corruption |
| Anything vs a file nobody read | **Read the file** | Four quest-flow rules sat visible in a live record nobody captured |

If two sources disagree and the table does not obviously settle it, say so and ask. A blended
answer from two incompatible sources looks confident and is wrong.

### Evidence tiers

Use these words precisely when recording a finding; they decide whether it can overturn a law.

| Tier | Means | Can overturn a law |
|---|---|---|
| **Source-verified** | read in the TNR source, file and line cited | yes |
| **Behaviour-proven** | a push or capture demonstrated it, bundle cited | yes |
| **Observed** | seen in live data, not yet explained | no, propose it |
| **Inferred** | reasoned from other laws | no |
| **Assumed** | nobody checked | no, and say so out loud |

Carried assumption: we write `longitude` as x and `latitude` as y; nothing in any capture
distinguishes them. Tier: assumed.

## Task start

Verify the requested ref to an exact commit once, then use the task route below.
With a checkout, commands derive from local evidence; without one, fetch the
relevant generated view at that commit. Do not mix files fetched from moving refs.

An explicit task starts immediately. A read-only lookup does not require a global
board read, branch, ledger write, code-review lane, or wait for another task choice.
`python3 scripts/tnr.py session` is an optional read-only global summary;
`--guards` is for repository maintenance. The two state projections are alternative
views of the digest, not two sources to hydrate. Workstream roadmaps own task state.
Use native environment Git authentication; ChatGPT uses the repository connector.
Never paste a PAT into project instructions or clone URLs.

## Task routing

| Task | Use |
|---|---|
| Any manifest, before handoff | `validate.py m.json` MANDATORY, zero errors, run from skill `data/`, say it ran |
| Building any payload | `factory.py` CONSTRUCTS it (cwd = skill `data/`); hand-authoring is the fallback |
| Field shapes, bounds, enums, constants, tRPC surface | `45c` / `45d` / `45e` / `45f` in skill `data/` |
| Name/id lookup | `answers/INDEX.md`; full-record overrides have timestamps in `answers/records.json`. These are observed snapshots, not proof of current live state |
| Law coverage vs code | `skills/building-tnr-content/scripts/lawmap.py <repo-root>` |
| A source drop or regen | `schema_extract.py <src> --ctors` FIRST, then the MECHANICAL gate: `schema_diff.py --invariants NEW_45c --constants 45e` and `schema_diff.py diff OLD NEW` per file; adopt only on exit 0 (fail-closed on enum-member/variant/field removal and type changes) |
| AI enemies, kits, stats, behaviour rules | skill `references/ai.md`; `enemy.py`, `calc.py ai\|kit` |
| Quests, events, dialog, flow | skill `references/quest.md`; `mission.py`, `storyboard.py` |
| Items, weapons, chests | skill `references/item.md` |
| Jutsu, converts, sweeps | skill `references/jutsu.md` |
| Tuning, rewards, tiers, drop math | skill `references/balance.md`; `calc.py` |
| Operative and raider lines (Unsigned, Verge, Forsworn) | skill `references/lines.md` |
| Anything that pushes | skill `references/pipeline.md`, alongside the entity reference |
| Art, any asset | skill `producing-tnr-art`; `chroma.py`, `artpreflight.py`, `shotlist.py` |
| Existing jutsu art: name → captured record → image URL | `scripts/jutsu_art.py verify`, then `lookup`/`image-url`; `docs/workflows/JUTSU_ART_LOOKUP.md` |
| Any capture or results bundle | `harvest.py` (v4.26+ inbox bundles normalize directly) |
| Full law text by number | `docs/ENGINE_LAWS.md`; cross-cutting clusters `docs/10_LAWS_core.md` |
| Inspect existing missions | `python3 scripts/tnr.py context missions.check --rank A`; then `missions check --rank A`. This checks observations, not construction profiles |
| Build a mission, any rank | `48_DATA_mission_profiles.json` + `mission.py sheet.json` |
| A multi-session content project (event/quest/mission arc) | `docs/workflows/CONTENT_WORKSTREAM.md`; `scripts/content_workstream.py`. Coordination state only - it never competes with this file's precedence table |
| `Initialize session from repo. Workstream: X. Task: Y.` | `content_workstream.py init <slug> --task <id>`, then read exactly what the packet routes |
| Ending work | update the owning workstream and evidence. Change the global digest only for cross-workstream navigation; `session_close.py --guards` projects it |

## Non-negotiables

- Everything ships `hidden: true`, every entity, no exceptions. Publishing is a separate step:
  it waits on the content admin's go-ahead, then dauntless publishes. [[D-hidden-true]]
- Claude pushes git. ALL game pushes are dauntless's - the ▶ tap is the only act that touches
  the game. [[D-user-pushes]]
- Nothing is handed over unvalidated, and say what ran. [[D-validate-always]]
- A push echo is not a read-back. `state: ok` with `live: NONE` means unverified. A filtered
  capture proves nothing. [[D-push-echo]]
- Never adopt regenerated data without a structural diff against the stamped file. [[D-adopt-gate]]
- Balance, rewards, rarity, art direction and final acceptance are dauntless's to settle.
  Propose, show one at a time, wait. [[D-reserved-dauntless]]
- The real first name never appears in any artifact of any kind. The username is dauntless. [[D-no-real-name]]

## Repository writes and releases

Use `docs/DEVELOPMENT_WORKFLOW.md` when writing code/infrastructure or integrating.
Release and distribution details: `docs/RELEASE_DISTRIBUTION.md`. Runtime root paths
are compatibility interfaces; never move them as an incidental cleanup.
