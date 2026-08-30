# 00 - TNR content generation: router (mounted 2026-08-30)

TNR is an open-source Next.js / tRPC / Drizzle web game at theninja-rpg.com. dauntless is a
contributor on content staff, working from Samsung Android in Firefox with ViolentMonkey.
Claude turns concepts into validated builder manifests and commits them to push/; dauntless
replays them against the live game through the hosted builder userscript. There is no staging
environment. Never copy proprietary text, never reference the Naruto franchise.

**This file routes and arbitrates. It does not teach.** docs/10_LAWS_core.md holds the
cross-cutting laws; docs/ENGINE_LAWS.md is the numbered text of record. Everything else lives
where the work happens and loads only when it does.

## The layers

| Layer | Holds | Changes |
|---|---|---|
| Project instructions | credentials, session ritual, non-negotiables | dauntless pastes |
| This repo | everything else: tool canon `/skills/`, laws `/docs/`, `/answers/`, `/harvests/`, staged `/push/`, `/state/`, `/archive/` | every commit; Claude pushes |
| Builder userscript | the push path; panel fetches `45c`/`45g`/`32b` from repo root; ⇩ Repo lists `push/` | ViolentMonkey refresh |
| Game source | `studie-tech/TheNinjaRPG`, public, clonable; contracts are extracted, never guessed | upstream commits |

Session state is `state/active-context.md` (the handoff, rewritten at every close) plus
`state/status.json` (the board). Session bundles are retired: the repo is the bundle.

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

## Session start

1. Clone with the PAT from the project instructions. `git pull --rebase` before every push
   thereafter - the answers/skillpack workflows commit back.
2. Read `state/active-context.md` and follow its start ritual. Parse `state/status.json`.
3. Report the one-line state and `rulings_open`, propose the next item, wait.

No clone means no state. Say so rather than working from memory.

## Task routing

| Task | Use |
|---|---|
| Any manifest, before handoff | `validate.py m.json` MANDATORY, zero errors, run from skill `data/`, say it ran |
| Building any payload | `factory.py` CONSTRUCTS it (cwd = skill `data/`); hand-authoring is the fallback |
| Field shapes, bounds, enums, constants, tRPC surface | `45c` / `45d` / `45e` / `45f` in skill `data/` |
| Name collision, id lookup, what exists live | `answers/` in the clone; fresher than the last harvest takes a capture |
| Law coverage vs code | `scripts/lawmap.py <repo-root>` |
| A source drop or regen | `schema_extract.py <src> --ctors` FIRST; structural diff before adopting anything |
| AI enemies, kits, stats, behaviour rules | skill `references/ai.md`; `enemy.py`, `calc.py ai\|kit` |
| Quests, events, dialog, flow | skill `references/quest.md`; `mission.py`, `storyboard.py` |
| Items, weapons, chests | skill `references/item.md` |
| Jutsu, converts, sweeps | skill `references/jutsu.md` |
| Tuning, rewards, tiers, drop math | skill `references/balance.md`; `calc.py` |
| Operative and raider lines (Unsigned, Verge, Forsworn) | skill `references/lines.md` |
| Anything that pushes | skill `references/pipeline.md`, alongside the entity reference |
| Art, any asset | skill `producing-tnr-art`; `chroma.py`, `artpreflight.py`, `shotlist.py` |
| Any capture or results bundle | `harvest.py` (v4.26+ inbox bundles normalize directly) |
| Full law text by number | `docs/ENGINE_LAWS.md`; cross-cutting clusters `docs/10_LAWS_core.md` |
| A mission, any rank | `48_DATA_mission_profiles.json` + `mission.py sheet.json` |
| Ending a session | rewrite `state/active-context.md` as the handoff, re-run guards, record output (CLOSEOUT.md mounted addendum) |

## Non-negotiables

- Everything ships `hidden: true`, every entity, no exceptions. Publishing is a separate step:
  it waits on the content admin's go-ahead, then dauntless publishes.
- Claude pushes git. ALL game pushes are dauntless's - the ▶ tap is the only act that touches
  the game.
- Nothing is handed over unvalidated, and say what ran.
- A push echo is not a read-back. `state: ok` with `live: NONE` means unverified. A filtered
  capture proves nothing.
- Never adopt regenerated data without a structural diff against the stamped file.
- Balance, rewards, rarity, art direction and final acceptance are dauntless's to settle.
  Propose, show one at a time, wait.
- The real first name never appears in any artifact of any kind. The username is dauntless.

## Deploy notes

Repo: commit, `git pull --rebase`, push; raw CDN caches ~5 min. Builder: refresh via
ViolentMonkey; the panel title must show the version and `cfg generated`; `partial` means
`45c`, `32b` or `45g` is missing from repo root (skillpack syncs root from skill `data/`).
Skills: change lands in repo `/skills/` first, the packaging workflow rebuilds `/dist/`,
download and reinstall; the container copy is never patched in place.
