# Skill overhaul: implementation brief

Status: APPROVED by the director 2026-11-09 (decisions in §11, RUL-2026-11-09-137). This file is the build
contract (CLAUDE.md §11). The roadmap it implies can be loaded as a content workstream
(`python3 scripts/content_workstream.py`), but this brief still governs.

Lane: A (skills, tools, tests, docs). The implementing agent works on `fable/*` branches, hands
each phase over at an exact SHA for independent review (`docs/workflows/IMPLEMENTATION_HANDOFF.md`),
and changes nothing in the live game.

---

## 0. Read this first (implementing agent)

1. `CLAUDE.md`, `docs/00_INDEX.md` (precedence, evidence tiers), `docs/DOCTRINE.md`,
   `docs/workflows/OPERATING_MODEL.md`, `docs/RULINGS.md` (index; full entries in `docs/rulings/`).
2. The two current skills in full: `skills/building-tnr-content/` and `skills/producing-tnr-art/`,
   including their scripts' `--selftest` output.
3. The sources listed in §3 for the phase you are on. Mine them; do not paraphrase from memory.

Three rules shape everything below:

- **Cite, don't copy.** A rule has one canonical owner: `docs/DOCTRINE.md`, `docs/ENGINE_LAWS.md`, a
  generated contract, a reference file, or a ruling. Skills point to it, or render it through the
  existing doctrine and pack tools. Never restate a law, number or ruling in a second place
  (CLAUDE.md §7). Where a skill needs a rule that has no owner yet, create the owner first.
- **Construct, don't author.** Every new design capability ends in a tool that emits valid records
  through `factory.py`, `mission.py` and `enemy.py`, never in prose an agent has to transcribe into
  JSON. A shape the tool cannot build wrong needs no review.
- **The director decides taste, balance and rewards** (CLAUDE.md §10). Tools propose defaults from
  ratified tables; anything unratified is a named `AWAITING_RULING` slot, never a guess.

---

## 1. Goal

Make the designing of TNR content as fast and as reliable as its building already is.

Today the skills turn a *decided* design into correct records very well. Everything before that
lives in the heads of whoever did the last event, in design docs and rulings, or in branch-only
tools:

- deciding an enemy's role, rules and jutsu loadout;
- choosing a quest structure, its setup and its payouts;
- designing a boss fight and tuning it;
- writing its text;
- directing and building its animations.

The overhaul turns that practice into skills, templates, libraries and tools.

**Success, measured** (§9 has the eval set):

- **AI enemies.** A new agent, given a one-paragraph request ("a level-60 Jonin bruiser that punishes
  campers, 3 phases"), produces a reviewed design and a manifest that passes `validate.py --strict`
  in one session, using library patterns. No hand-written JSON, and no rule grammar re-derived from
  source.
- **Quests.** It produces any of the catalogued quest structures with a payout taken from the
  ratified reward tables.
- **Boss fights.** It produces a fight that goes through the full pipeline: bible, script,
  telegraphs, simulated clear rates against targets, text, art direction, build.
- **Combat animations.** It produces one that meets the director's art rules at true scale, using
  the shipped harness rather than re-learning the engine's clip, layering and timing facts.
- **The director's load.** The director spends time only on taste and reward decisions, presented
  as go cards with options.

---

## 2. Ground rules

- **No live game requests during implementation.** Use captures, fixtures, `answers/` and the
  pinned game source. Eval runs build manifests; they do not run them.
- **Game engine execution.** The encounter simulator (§5.4) runs the game's combat engine offline,
  in a socket-denied child. CLAUDE.md §6 says to read the source but not run it unless a task
  authorizes execution. **The director authorized that use as standing design-time tooling**
  (RUL-2026-11-09-137): offline, socket-denied, pinned engine SHA, no network, no credentials, never
  the live game.
- **Gates.** Every phase passes:
  - doctrine: `doctrinemap.py`, `render_doctrine.py --check`, `build_packs.py --check`, `lawmap.py`;
  - its own selftests: socket-free, with exit codes never masked.

  The existing selftests and Forge tests must stay green.
- **Packaging.** Skills ship from `skills/` through the existing `skillpack.yml` workflow into
  `dist/*.zip`. New skills follow the same layout:
  - `SKILL.md` front matter (name and a description that triggers correctly);
  - `references/` with `_toc`;
  - `packs/` where builds read curated excerpts;
  - `scripts/` with selftests;
  - `data/`.

  `build_packs.py` and `render_doctrine.py` must learn about new skills rather than be bypassed.
- **Scope discipline.** No refactor of `factory.py`, `validate.py` or Forge beyond what a phase
  needs, and no new authority documents where an existing one can own the rule.

---

## 3. What exists to mine

### Content design and building

| Area | Sources |
|---|---|
| AI records, rule grammar, range gating | `skills/building-tnr-content/references/ai.md` (spec template, rule object, vocabulary); `packs/ai-build.md`; `scripts/enemy.py` (role defaults, rank from level); `data/32b_DATA_pool.json` (pool codes); `data/40x_EXEMPLARS_effects.json`; `data/46_DATA_tag_schemas.json`, `46b_DATA_tag_runtime.json`; `docs/ENGINE_LAWS.md` (rule cap, law 18 equip link, law 40 gates, shared cooldowns). |
| Jutsu | `references/jutsu.md`, `packs/jutsu-build.md`, `references/balance.md` §2-4 (damage tiers, generation doctrine); `scripts/calc.py`. |
| Quests and events | `references/quest.md` (objective graph, types, availability gating, ambush attackers, QA checklist); `packs/quest-build.md`; `scripts/mission.py` + `data/48_DATA_mission_profiles.json`; `references/event.md` + `data/26x_EVENT_sheet_schema.json` + `EVENT_SHEET.md`; `docs/design/EVENT_STRUCTURE.md`, `EVENT_JOURNAL.md`. |
| Payouts and economy | `references/balance.md` (reward class, farm layer, keystones, items); `references/item.md`; the reward and loot rulings (search the RULINGS index for "reward", "cache", "loot", "chest", "drop"); `docs/design/SKYGLASS_LOOT_TABLES.md`, `SKYGLASS_PROFESSION_CHESTS.md`, `SKYGLASS_THE_HAUL.md`. |
| Enemy lines | `references/lines.md` (Unsigned, Verge, Forsworn: level ladders, build order). |

### Shipped designs to turn into worked examples

- **Mother of Echoes:** `docs/design/MOTHER_OF_ECHOES_EXPERIENCE.md`, `_FIGHT_SCRIPT.md`, `_ACT3.md`,
  `_JUTSU_TEXT.md`, `_ART.md`; `docs/design/SAYO_BIBLE.md` (character bible);
  `push/mother_of_echoes.gen.py`; `push/mother_of_echoes_log_lines.json`.
- **Skyglass:** `docs/design/SKYGLASS_STORY_BIBLE.md`, `SKYGLASS_BOSS_FIGHTS.md`,
  `SKYGLASS_WRECK_ENCOUNTERS.md`, `SKYGLASS_DUNGEON_AND_TREASURE_HUNTS.md`,
  `SKYGLASS_HUNTS_CONTENT.md`, `SKYGLASS_EVENT_MAP.md`, `SKYGLASS_TEXT.md`; `push/crownhold.gen.py`
  and the `push/skyglass_*.gen.py` generators; `state/skyglass_design/design_data.json` and
  `scripts/skyglass_check.py` (a design-to-manifest consistency checker worth generalising).
- **Ghost Ship:** `docs/design/ghost_ship_art_bible/`, `GHOST_SHIP_SKYGLASS_FULL_MANIFEST_ROADMAP.md`.

### Encounter simulation

- `harness/skyglass_wreck_sim/` on branch `fable/mother-of-echoes-sim` (head `fd353115`), never
  merged: an offline, engine-driven fight simulator.
  - **Runners:** dungeon, hunts, charts, haul, Crownhold, kite.
  - **Built in:** a rule-cap gate, law-40 gates, player profiles, results tables.
  - **Reports:** `REPORT*.md`.
  - **Its later use:** Mother of Echoes clear-rate tuning ("perfect / real / everyone else"
    profiles). The 2026-11-06 summary of that tuning is in `docs/design/MOTHER_OF_ECHOES_ACT3.md` §7.
- `harness/ghost_ship_final/tools/offline_exec.py` (on main): the socket-denied child runner.

### Combat animation (none of this is in a skill yet)

- `docs/handoffs/skill_overhaul/TNR_ANIMATION_HANDOFF.md` (committed with this brief) covers:
  - the engine facts: clip size and rendition, layering, load skew, visual tags, AoE, shared
    cooldowns, one-hit kills, ground binding;
  - the director's art rules, the techniques and the pipeline.
- `docs/handoffs/skill_overhaul/qa_preview.py.txt` (committed with this brief): the true-scale preview
  harness as it ran. Its paths point at a scratch checkout (`wt_custom`). Port it into a tool; do not
  run it as is.
- `docs/design/COMBAT_ANIMATION_ENGINE.md` (older; the handoff's §1 wins where they differ),
  `MOTHER_OF_ECHOES_ART.md`, `SKYGLASS_BOSS_ANIMATIONS.md`, `SUBAKU_PALACE_ANIMATION.md`.
- Builders: `art/mother_of_echoes_fx/build_fx*.py`, `art/subaku_palace/` (`classic.py`,
  `build_domain.py`, `floor.py`, `TIMING.md`), `art/skyglass_boss_fx/`.
- Art direction rulings: RUL-2026-11-05-124, -126, -127; RUL-2026-11-06-128, -129, -130.

### Delivery (current)

- `docs/workflows/OPERATING_MODEL.md` (go cards, connector-first, image jobs in the browser).
- `docs/workflows/FORGE_MCP_RUNNER.md` (the connector runner and the run lock).
- RUL-2026-11-06-132, RUL-2026-11-07-133, RUL-2026-11-07-135.

---

## 4. Target architecture

Four skills with clear handoffs. The design skill is the planning center: it owns the *what* and
the *why*, and emits a design sheet the build skill compiles.

```
designing-tnr-content  (NEW, the planning center)
   | design sheet (JSON, schema-checked) + design doc
   v
building-tnr-content   (UPDATED)   -> manifests -> connector / Forge -> live
   ^                                   |
   | @img / asset ids                  v
producing-tnr-art      (UPDATED)   live verification recipes
animating-tnr-combat   (NEW)       -> animation assets + visual-tag wiring for the build
```

Two boundaries matter:

- **Design and build.** The design sheet is the only contract. A sheet carries creative and
  structural choices and named slots. It never carries engine fields the factory derives
  (`mission.py`'s rule today: "a sheet cannot reach a profile field"; extend it, don't loosen it).
- **Animation and build.** Animation tools emit asset files plus a wiring spec: visual-tag
  coordinates per hex, plus `staticAssetPath` and `appearAnimation` per effect. The build skill
  turns that into records through the factory.

---

## 5. designing-tnr-content (new): the main deliverable

### 5.1 The workflow (SKILL.md body)

Each stage below has three parts:

- a template (in `references/templates/`);
- an exit checklist;
- a director decision point, presented as a go card (`OPERATING_MODEL.md` §2).

Stages can be skipped by size: a single AI needs stages 3, 6 and 7; a boss event needs all of them.

| # | Stage | Artifact | Exit |
|---|---|---|---|
| 1 | Brief | One paragraph: purpose, audience (rank or level band), where it lives, size. | Director agrees the brief. |
| 2 | Concept | Hook, fantasy, references (Naruto analogues allowed), 2-3 options. | Director picks one. |
| 3 | Design sheet | The machine-readable sheet (§5.2) plus a short design doc: roles, rules, loadouts, structure, payouts, text slots, art slots. | Sheet validates, with no unresolved slots except named `AWAITING_RULING` items. |
| 4 | Fight design (bosses) | Character bible, fight script (per round or phase), telegraph map (omen → payoff), clutter budget, anti-camping, enrage. | Telegraph and clutter checklist passes. |
| 5 | Tuning | Simulator runs against targets per player profile (§5.4); payout check against reward tables. | Within targets, or the gaps are listed for the director. |
| 6 | Text | Names, descriptions, battle descriptions, log lines, quest text, following the writing guide (§5.6). | Text lint clean. |
| 7 | Build handoff | `design.py compile` → manifest; `validate.py --strict`; go card. | Gates clean; director's go. |
| 8 | Art (as needed) | Art slots handed to `producing-tnr-art` or `animating-tnr-combat`. | Their gates. |
| 9 | Live verification | Post-run reads and a battle check (§7.3). | Matches the design; findings logged. |

### 5.2 The design sheet

`data/design_sheet.schema.json`, plus `scripts/design.py`:

```
design.py new <kind> [--from <exemplar>]   scaffold a sheet (kinds: ai, ai_line, boss, quest, quest_chain, dungeon, event)
design.py check <sheet>                    schema, library references, slot report, balance and payout bounds
design.py compile <sheet> -o push/NNN_x.json  through factory.py / mission.py / enemy.py; refuses while slots are open
design.py explain <sheet>                  the human-readable design doc, generated from the sheet (never hand-kept twice)
```

The sheet references library entries by id, for example `"rules": ["telegraph_payoff/v1", ...]`,
with parameters, instead of spelling out rule objects. It extends the existing mission design sheet
and `26x_EVENT_sheet_schema.json` rather than replacing them. Reconcile the three into one schema
family, keeping backward compatibility with existing sheets.

### 5.3 Libraries (`data/` plus a reference page each)

Each library entry carries:

- a stable id and version;
- its parameters with bounds;
- the records or fragments it expands to (built through the factory);
- the engine laws it depends on (cited by number);
- the shipped content that proves it (exemplar ids);
- its known failure modes.

Entries are mined from shipped content first, and invented second.

1. **AI archetypes.** Role (bruiser, skirmisher, caster, support, summoner, controller, boss) ×
   rank band. Each gives a stat profile (from `enemy.py` role defaults), jutsu slot budget, pool
   preferences and default rule set.
2. **Rule patterns.** The behaviours, as parameterised `AiProfile` rule groups:
   - an opener;
   - telegraph → payoff (omen round, then eruption);
   - phase change on an HP threshold;
   - enrage by round;
   - summons and add waves;
   - anti-camping (the Absence, hush pools);
   - healer and shielder support;
   - kite and close-range gating;
   - the shared-cooldown-aware rotation;
   - a one-hit-kill finisher with a chance;
   - fleeing and despawning.

   Each pattern states its rule count against the server's 20-rule cap, and its law-40 gate needs.
3. **Jutsu loadout recipes.** Per role and rank: slot counts, cooldown pacing under shared cooldowns
   (b54541f1), damage tier per slot (`balance.md`), pool codes over raw ids, and which slots
   telegraph.
4. **Boss fight grammar.**
   - The omen and payoff language.
   - The clutter budget (three things readable every round).
   - The fixed danger colours.
   - Act structure.
   - Enrage and one-hit-kill policy.
   - "The fight is a stage" (terrain that changes as the fight goes).

   Cited from the art direction rulings and `MOTHER_OF_ECHOES_*`.
5. **Quest structures.** Each structure states its objective graph shape, availability gating,
   reset semantics and QA checklist (from `quest.md`). The catalogue:
   - a single battle;
   - a chain;
   - a branch or choice;
   - a gated daily or weekly;
   - event journal pages;
   - treasure and chart hunts;
   - hauls;
   - dungeon floors and waves;
   - ambush attackers;
   - ally AIs;
   - collection and turn-in;
   - a tutorial or intro.
6. **Setups.** Scenes and characters, dialogue beats, ally AIs, starting effects and objective
   debuffs (traps), ground hazards, timed windows.
7. **Payout model.** `scripts/payout.py`: reward class × rank band × effort to money, XP, items,
   caches, drop rates and event currency, read only from ratified tables in `balance.md` and the
   reward rulings. Where no ratified number exists, the slot stays open. Mine the current tables
   into `data/` with a citation per row; ask the director only for the gaps.

### 5.4 Tuning: the encounter simulator

- **Promote the simulator.** Take `harness/skyglass_wreck_sim` from `fable/mother-of-echoes-sim` to
  main as a general encounter simulator, after the director authorizes engine execution (§11
  decision 1). This includes:
  - merging the harness code (not the big result files);
  - keeping it socket-free;
  - pinning the engine SHA per run.
- **Generalise its input** to take a compiled design sheet.
- **Ship player profiles as data:**
  - perfect: plays every telegraph right;
  - real: an average reader who makes typical mistakes;
  - everyone else.

  Gear tiers come from the balance tables.
- **Targets per content kind are director rulings** (e.g. a finale's clear rate for perfect and real
  players). The simulator reports against them; it never decides them.
- **Fast design-time checks**, with no simulation: `calc.py` damage maths, the rule-cap count, gate
  checks, the shared-cooldown lock map, and ground binding on the target's hex.

### 5.5 Generalise the consistency checker

`skyglass_check.py` proves a set of manifests matches a design data file. Factor out a general
`design_check.py` that checks any compiled event against its sheet, keeping Skyglass's checks as
its first configuration.

### 5.6 Writing guide (reference page)

Names, descriptions, battle descriptions and log lines:

- **Register:** Naruto-flavoured ninja world, the director's voice.
- Staff-only descriptions on boss jutsu.
- Log lines that carry gameplay clues.
- No em dashes (validator).
- Length bounds from the schemas.

Cite the owning rulings (search the index for "battle description", "log line", "text"), and add
a text lint to `design.py check`.

### 5.7 Worked examples (`references/examples/`)

Six to eight short case files. Each one gives:

- what was asked;
- the sheet that would produce it (validated by `design.py check`);
- what shipped;
- what was learned.

Candidates:

- a Mother of Echoes act;
- the Crownhold Captain;
- a Skyglass Wreck floor;
- a chart run;
- the Haul;
- a Watch Log page;
- an Unsigned line enemy;
- a Ghost Ship encounter.

---

## 6. animating-tnr-combat (new)

- **SKILL.md and references.** From `TNR_ANIMATION_HANDOFF.md`:
  - **Engine facts:** cite `docs/ENGINE_LAWS.md` and game source lines; promote any fact that has no
    law owner into a law through the reconciliation process.
  - **Art rules:** cite the rulings.
  - **Techniques:** slice mosaic, lattice-periodic paintings, caster-relative pieces, floor-arrival
    options, craft rules.
  - **Pipeline:** design → build → true-scale preview → preflight → independent review → naming
    and folders → hidden create → edit with law 18 → unhide → live check.
- **Tools** (`scripts/`, each with a selftest):
  - `preview.py`: the ported `qa_preview` harness. Repo-relative paths, an LPC stand-in, light and
    dark boards, skew 0 and 2, both parities, the clip ratio as a parameter, the 50 px rendition
    with linear filtering.
  - `slice.py`: one painting → per-hex strips, polygon-clipped with a 1 px bleed, deduplicated by
    content hash, plus a wiring spec.
  - `tagwire.py`: the wiring spec → visual-tag effects, built through `factory.py`.
  - The existing `artpreflight.py` (shared with producing-tnr-art).
- **Live-engine drift check.** A `clip_ratio` read from the pinned source, with a loud warning when
  upstream changes it (338126cb, clip size 1, is the cautionary case).
- **Exemplars:** the Refraction line (the quality bar), a Subaku light-only bloom, a faint floor,
  an omen mark.

---

## 7. Updates to the existing skills

### 7.1 building-tnr-content

- Replace "builder manifests pushed through the hosted userscript" with the current delivery:
  - Forge (browser) for image jobs;
  - the connector runner (`mcp_run.mjs`) for everything else;
  - the run lock, go cards and live reads.

  Cite `OPERATING_MODEL.md` and `FORGE_MCP_RUNNER.md`; do not restate them.
- Add the design-sheet entry point: "if the request is a design, start in designing-tnr-content".
- Fix the description so it triggers on connector-era phrasing.

### 7.2 producing-tnr-art

- Add the director's standing art direction (cited rulings), with a pointer to
  animating-tnr-combat for anything that moves.
- Keep the still-art pipeline as is.

### 7.3 Live verification (in building-tnr-content)

A reference page plus `scripts/battle_read.mjs`:

- post-run readback of records;
- reading an in-progress battle's effects (who created an effect, and from what: item, skill,
  quest, pet, AI);
- the player-report investigation recipe, worked from the 2026-11-07 Wreck afterburn report:
  log → hypothesis → live read → owner.

Live reads go through the connector under the run lock; the script itself is fixture-tested.

---

## 8. Phases

Each phase is one or more `fable/*` branches, each handed over at an exact SHA for review.

| Phase | Delivers | Depends on |
|---|---|---|
| P0 | Inventory: mine §3 into `docs/handoffs/skill_overhaul/INVENTORY.md`, with every rule's current owner, every gap without an owner, and the list of director decisions found. No skill changes. | — |
| P1 | designing-tnr-content skeleton: SKILL.md workflow, templates, design sheet schema + `design.py new/check/explain`, writing guide, packaging wired into `build_packs` / `render_doctrine`. | P0 |
| P2 | Libraries 1-3 (AI archetypes, rule patterns, loadouts) + `design.py compile` for `ai` / `ai_line`; three worked examples. | P1 |
| P3 | Libraries 5-7 (quest structures, setups, payout model) + compile for `quest` / `quest_chain` / `dungeon` / `event`; `design_check.py`; three worked examples. | P1 |
| P4 | Boss fight grammar (library 4) + the simulator promoted and generalised (needs decision 1) + `boss` compile; Mother of Echoes worked example. | P2, P3 |
| P5 | animating-tnr-combat: references, `preview.py`, `slice.py`, `tagwire.py`, exemplars. | P1 |
| P6 | building-tnr-content and producing-tnr-art updates, the live verification page and `battle_read.mjs`. | P1 |
| P7 | Evals (§9), fixes, final packaging, and a director walkthrough. | all |

P2, P3, P5 and P6 can run in parallel once P1 lands.

After P7: the skill research program (`state/prompt_skill_research_program.md`, RUL-2026-11-09-138) continues the skills with research-backed toolkits, starting with combat VFX.

---

## 9. Acceptance: the eval set

`skills/designing-tnr-content/evals/` holds ten or so requests, each paired with what a passing
result must show. Run each with a fresh agent and only the skills. Record per eval:

- the time taken;
- the validate and gates result;
- the open slots;
- the director's quality score (1-5).

Examples:

1. "A level-60 Jonin bruiser that punishes campers, 3 phases": rule patterns from the library, rule
   count ≤ 20, gates met, `validate --strict` clean.
2. "A 4-enemy Chunin line ladder, 30→75": the line structure from `lines.md`, rank from level, pool
   codes.
3. "A weekly event journal page with five tasks and a cache payout": the journal structure, the
   payout from the tables or named open slots, publish gating.
4. "A 3-floor dungeon with a boss floor and two add waves": waves, delays, the rule cap, simulated
   clear time against the dungeon limit (after decision 1).
5. "A treasure hunt with chart drops": the hunt structure, the drop-rate table, the shard-style
   cross-links.
6. "A boss with two acts, an omen/payoff signature move and an anti-camping summon": the full
   pipeline to compile, plus clutter and telegraph checklists.
7. "An animation for a line attack across 5 hexes": slice + wire + preview at the right clip ratio,
   preflight 0.
8. "Investigate: enemies take X from round 1" (fixture battle): the recipe reaches the effect's
   creator.

**Done means:**

- every eval compiles or reports only named director slots;
- every gate is green;
- the director's average score is at least 4;
- the time spent on the AI and quest evals at least halves against a baseline run on today's skills.

---

## 10. Non-goals

- No balance or reward numbers invented to fill tables (slots instead).
- No change to how the live game is written (Forge, connector and lock stay as they are).
- No rewrite of `factory.py`, `validate.py` or the doctrine system, beyond extension points.
- No merging of the simulator's large result files.
- No history rewrite or repo restructuring (separate cleanup track).

---

## 11. Director decisions (taken 2026-11-09, RUL-2026-11-09-137)

1. **Engine execution: AUTHORIZED.** The encounter simulator may run the game's combat engine offline
   as standing design-time tooling: socket-denied, pinned engine SHA, no network, no credentials,
   never the live game.
2. **Clear-rate and timing targets: to be reviewed in detail with the director.** P4 brings the
   Mother of Echoes numbers and a proposed table per content kind (finale boss, event boss, dungeon
   floor, weekly page) as a go card. Until then the simulator reports measured rates without a
   pass/fail verdict.
3. **Reward-table gaps: reviewed with the director when P0 finds them.** Each gap is listed in
   `INVENTORY.md` and stays an open slot in the tools until ruled.
4. **Names and split: as proposed.** Two new skills, `designing-tnr-content` and
   `animating-tnr-combat`. Animation stays out of `producing-tnr-art`, which is still art.
5. **Implementer: a separate Claude agent (Fable 5.2, medium effort), started by the director.** One
   phase per handoff; ChatGPT reviews each frozen SHA.
6. **Installation: as soon as each skill is complete.** When a phase completes a skill, or an update
   to one, and its review passes, the implementer builds its `dist/*.zip` through the existing
   `skillpack.yml` path and tells the director it is ready to install. Do not wait for P7.

## 12. Handoff per phase

Per `docs/workflows/IMPLEMENTATION_HANDOFF.md`:

- base and head SHAs;
- changed files;
- gates run, with exact commands and results;
- selftests and evals run;
- open director slots;
- what was not begun.

Freeze the SHA until review returns. Update `state/run_queue.json` only if a phase creates live
work (it should not).
