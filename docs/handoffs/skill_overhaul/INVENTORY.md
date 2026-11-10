# Skill overhaul P0: inventory

**Status:** P0 deliverable of `state/prompt_skill_overhaul.md` (§8), for independent review. Review-only
document: it changes no skill, tool, law, doctrine or ruling.
**Base:** `perseverance484/tnr-tools` main at `fca8625b6c55e3889b270bd2fde76d63b2f9a4d1`. The work began on
`a4f05507f093fc635e00b095953512b95429b4c5`; main advanced during P0 (see B-01), the branch was rebased once
before handoff, and every claim that touched a changed file was rechecked on the new base.
**Live requests:** none. No credentials. No game code was executed.

**What this file is.** A map of where each rule the overhaul needs lives today, which rules have no
owner, which reward tables exist and which are missing, and which director decisions were found.
It is an index, not an authority: it names owners and does not restate their numbers or text
(CLAUDE.md §7). Where a number appears below it is an identifier (a law number, a ruling id, a
constant name, a commit), not a rule.

**How to read the ids.** `G-nn` a rule with no owner. `C-nn` owners that disagree or lag. `R-nn` a
ratified reward or pacing table. `RG-nn` a reward-table gap. `D-nn` an open director decision.
`B-nn` a place where the brief and the repository disagree. `T-nn` a tooling finding.

## 0. Coverage: what was read, and how closely

| Source | How it was read |
|---|---|
| `CLAUDE.md`, `docs/00_INDEX.md`, `docs/DOCTRINE.md`, `docs/workflows/OPERATING_MODEL.md`, `docs/workflows/IMPLEMENTATION_HANDOFF.md`, `state/prompt_skill_overhaul.md` | in full |
| `docs/ENGINE_LAWS.md` | in full |
| Both `SKILL.md` files; `references/ai.md`, `balance.md`, `lines.md`, `event.md` | in full |
| `references/quest.md` | sections 1 to 8, the addenda and the appendix in full; the relocated-law tail not re-read (it mirrors `ENGINE_LAWS.md`) |
| `references/jutsu.md`, `item.md`, `pipeline.md`; `producing-tnr-art/references/*` | headings plus targeted sections (item §4, jutsu §2, pipeline §2.8 to §2.10); not read end to end |
| `packs/*.md` | not read; they are rendered from the references (`build_packs.py --check` passes) |
| The rulings ledger: index `docs/RULINGS.md`, entries in `docs/rulings/2026-09.md`, `2026-10.md`, `2026-11.md` (308 entries) | full heading index; status and canonical destination of every entry from 2026-10-23 on; the ruling text of 36 entries read (listed in §6.1), the longest of them in part, and their evidence quotes mostly skipped |
| `docs/design/EVENT_STRUCTURE.md`, `docs/handoffs/skill_overhaul/TNR_ANIMATION_HANDOFF.md` | in full |
| Other `docs/design/*` named in the brief §3 | headings, status lines and targeted sections only |
| `data/48`, `26x`, `32b`, `45e` | structure and the fields cited below |
| `harness/skyglass_wreck_sim` on `fable/mother-of-echoes-sim` | README, `run.sh`, file listing and sizes; no report read in full |
| Scripts | docstrings and the constants cited below; every `--selftest` run (§7) |

Anything this file says about a source in the last five rows is limited to what those reads can
support. Phases that build on such a source must read it properly first (brief §0 item 3).

---

## 1. Rule owners today

Owner classes follow `docs/00_INDEX.md`: doctrine (`docs/DOCTRINE.md`), engine law
(`docs/ENGINE_LAWS.md`), generated contract (`data/45*`, `46*`, `25x`), skill reference, design
doc, ruling, generator or tool. "Copies" are other places that carry the same rule today.

### 1.1 Cross-surface doctrine

| Rule | Owner | Copies / projections | Checked by |
|---|---|---|---|
| No staging; hidden on create; validate before handover; push echo is not a read-back; capture first; compose from generated files; build order; ids by script; adopt gate; repo is tool canon; rebase first | `docs/DOCTRINE.md` (`D-*` ids) | rendered into the mounted instructions, both `SKILL.md` files and `references/pipeline.md`; referenced from `docs/00_INDEX.md` | `doctrinemap.py`, `render_doctrine.py --check` |
| Balance, rewards, rarity, art direction, publishing and acceptance are the director's | `D-reserved-dauntless` | `CLAUDE.md` §10; `references/balance.md` §7; `references/event.md` | none mechanical |
| Pool codes over raw ids | `D-pool-codes` | `SKILL.md` (rendered) | `enemy.py` resolves codes |
| No franchise reference; no real first name | `D-no-franchise`, `D-no-real-name` | `producing-tnr-art/SKILL.md` raw QC; `references/ai.md` §6.3 | none mechanical |
| Em dash ban in player-facing dialog | `D-emdash-dialog` | `references/quest.md` §6.2; `references/event.md` | `validate.py` L11 |
| Items default Legendary; weapon riders stay light | `D-legendary-default`, `D-riders-light` | `references/balance.md` §6 | none mechanical |
| Who may write to the live game, and how | `CLAUDE.md` §6 (RUL-2026-11-06-132) | `docs/workflows/OPERATING_MODEL.md`, `docs/workflows/FORGE_MCP_RUNNER.md` | run lock (`forge/src/runner/runlock.mjs`) |
| Go cards, connector first, small jobs, live checks, delete inventory | `docs/workflows/OPERATING_MODEL.md` (RUL-2026-11-07-135) | none found | none mechanical |
| Lane A branch, handoff and review | `CLAUDE.md` §4, §11, §12; `docs/DEVELOPMENT_WORKFLOW.md`; `docs/workflows/IMPLEMENTATION_HANDOFF.md` | none | none mechanical |

### 1.2 AI enemies

| Rule | Owner | Copies | Checked by |
|---|---|---|---|
| Required create fields; level is the stat budget; stats are ratio weights; pools are overwritten | laws 14, 15, 71 | `references/ai.md` §1.2 and its relocated-law tail; `enemy.py`, `calc.py` docstrings | `enemy.py`; `validate.py` |
| Rank is the combat-time cap | law 16; table `USER_CAPS` in `45e` | `references/ai.md` §1.2; hard-coded in `enemy.py` (`RANK_LVL_CAP`) and `calc.py` (`USER_CAPS`) | `enemy.py` refuses a rank below the level's floor |
| Rule object shape and vocabulary | laws 16d, 39, 64; `45c` (`ZodAllAiConditions`, `ZodAllAiActions`) | `references/ai.md` Part 2 §2 to §6 | `factory.py`, `validate.py` |
| Rule count cap | `45e` `AI_PROFILE_MAX_RULES` (generated at 3314d122), applied in `45d` | prose in `references/pipeline.md` (AI equip addendum); RUL-2026-10-31-066 item 1, -077 | `validate.py` (a literal in the script, not read from `45e`); the unmerged harness has `engine/rulecap.ts` (see G-01) |
| Distance gate | law 40 | `references/ai.md` §7; gate values precomputed in `32b` (`gate`) | lint L22; `enemy.py` |
| Final rule and reachability | laws 41, 41b, 63 | `references/ai.md` (2026-08-01 addendum, R52) | lint L24 |
| Equip link is severed by an edit | laws 18, 60 | `SKILL.md`; `references/ai.md` | knowledge only (`12b_LAWS_coverage.md`); see C-03 |
| Unresolved equip refs are stripped | law 17 | `references/ai.md` §1.2 | builder ref substitution |
| Effect timing (`castThisRound`), turn versus round | laws 61, 75, 76 | `SKILL.md`; `references/balance.md` tail | knowledge only |
| Stealth blocks attacking; items in rules; unique usernames; item list sync | laws 62, 65, 66, 69, 70 | `references/ai.md` tail | partial |
| Condition quirks: zero threshold, dead `BARRIER_BETWEEN`, action selection, STUDENT strip, stun does not stack, weakness semantics | `references/ai.md` addenda (R41, R50 to R54, H10) | none | lints L31, L35, L36 |
| Basic attack as a rule target | `references/ai.md` ("confirmed rule vocabulary"), RUL-2026-10-31-071 | `validate.py`, Forge kit lint | `validate.py` |
| Role defaults (pools, stats multiplier, kit size, armour, passive tags) | `references/ai.md` §1.8 | `enemy.py` `ROLE_DEFAULTS` | `enemy.py`; see C-05 |
| Stat-ratio shapes per role | `calc.py` `ROLES` (a tool is the only owner) | none | see G-03 |
| Shared jutsu pool: codes, ids, range, gate, AP, cooldown | `data/32b_DATA_pool.json` | repo-root copy for the builder (synced by skillpack) | `enemy.py`, `calc.py kit` |
| Kits come from the pool; signature budget per boss | `references/ai.md` §1.2; `references/event.md` addendum item 4 | none | none mechanical |
| AI restrictions (no lifesteal or vamp, no movement jutsu, HP conditionals limited) | `references/ai.md` §1.5, §4.1 | none | none mechanical |
| Enemy spec template, poster layout, QA checklist | `references/ai.md` §1 to §8 | none | none |
| AI-only jutsu are exempt from the cooldown floor | lint L16 in `forge/src/runner/lints.mjs` and `validate.py` (RUL-2026-11-02-106) | none | L16 |
| Enemy lines (Unsigned, Verge): rungs, kits, behaviour, build order | `references/lines.md` | none | none; see RG-10 |

### 1.3 Jutsu

| Rule | Owner | Copies | Checked by |
|---|---|---|---|
| Field shapes, bounds, strict per-tag unions, formula effects | laws 1 to 6; `45c`, `45d`, `46`, `46b` | `references/jutsu.md` §2 | `factory.py`, `validate.py` |
| Effects composed from live exemplars | law 3; `data/40x_EXEMPLARS_effects.json` | `references/ai.md` §7.4 | `factory.py` |
| AP is one of two values; damage is a tag; tag limit | `references/balance.md` §1 | `references/ai.md` §1.6, §4 | lints (not individually verified in P0) |
| Player damage tiers | `references/balance.md` §2 | none | none mechanical |
| Stacking is multiplicative; pierce bypasses modifiers; ramps compound; calibration protocol | laws 9 to 13 | `references/balance.md` §6 and tail | `calc.py` |
| Runtime-only tags; companion requirements | laws 77, 78 | `references/balance.md` tail | `validate.py` |
| Damage constants are defaults, live values differ | law 83 | `references/balance.md` tail | knowledge only |
| Level cap and `powerPerLevel` house rule | `references/balance.md` (H17) | none | none |
| Battle line placeholders | `references/jutsu.md` §2 (`battleDescription`) | none | `validate.py` (non-empty) |

### 1.4 Quests and events

| Rule | Owner | Copies | Checked by |
|---|---|---|---|
| Objective graph, single start, acyclic, loops only through `reset_quest`, terminals | laws 85 to 88; `references/quest.md` §1, §3.4b | `references/event.md` | `validate.py` flow checks |
| Task classes; a dialog is the only gate; `start_battle` shield doctrine | `references/quest.md` §3.1, §3.4b, appendix §2 | none | `validate.py` (partly) |
| `consecutiveObjectives` required, at data level | laws 23, 24, 37 | `references/quest.md` §3.4b; `48` `_field_routing.fixed` | `mission.py` fixes it; `validate.py` |
| Availability filter, start guards, where each quest type lists | `references/quest.md` (source-extraction addendum) | none | none |
| Reset semantics; lose-retry pattern | `references/quest.md` §3.5, §3.6, appendix §6; law 26 | `references/event.md` | `validate.py` (law 88) |
| Ambush `attackers` versus `opponentAIs` | law 44; `references/quest.md` appendix §7 | none | `validate.py` (headcount sum) |
| Gate field caps; plain dates; quest edits reproduce the record | laws 7, 8; `references/quest.md` §3.4c, §3.4d | `references/event.md` | `validate.py` |
| Single prerequisite makes a tree; reveal pacing; profession quests | laws 38, 42, 43; `references/quest.md` ("Unlock graph") | `references/balance.md` (reward class item 4) | partial |
| Placement, sectors, map pins, collect timer | laws 52 to 56, 89; `data/34b_DATA_pins.json` | `references/quest.md` | `validate.py` |
| Client display (silent reset and win text, one scene character, HTML dialog) | laws 47 to 51; `references/quest.md` §6.2b | `references/balance.md` ("Client display laws") | partial |
| Dialog writing rules; choices fork to distinct targets | `references/quest.md` §6.2, §6.2b | `references/event.md` step 5 | L11; the distinct-target lint is described as wanted, not confirmed built |
| CYOA wings doctrine | law 27; `references/quest.md` §3.4b-2 | `references/event.md` addendum item 3 | none |
| Battlepyramid shape | `references/quest.md` §3.7 | `references/event.md` | `validate.py` (partly) |
| Mission profile per rank (gates, shape, reward) | `data/48_DATA_mission_profiles.json` | `references/balance.md` ("Observed template"); see R-01 | `mission.py` |
| Mission design sheet: a sheet cannot reach a profile field | `mission.py` | `SKILL.md` | `mission.py` |
| Staff event sheet and its build contract | `EVENT_SHEET.md`; `references/event.md`; `data/26x_EVENT_sheet_schema.json` | none | none found for `26x` instances |
| Event structure framework (principles, sheet, ladder, checklist, anti-patterns) | `docs/design/EVENT_STRUCTURE.md` (RUL-2026-11-05-116) | reference map `docs/design/SKYGLASS_EVENT_MAP.md` | none; see C-06 |
| Event journal pattern | `docs/design/EVENT_JOURNAL.md` (RUL-2026-11-05-120 to -122, RUL-2026-11-08-139) | none | none |
| Pets, badges and titles, item variants, dungeon `onlyOnce` (write shapes) | `references/pipeline.md` §2.8 to §2.10 | none | `pet_checks.py`, `variant_checks.py` |
| Dungeon limits (party, run time, tiers, floors, waves, mobs, drops) | `45e` `DUNGEON_*` | none in any reference; see G-06 | none |
| Skyglass design-to-manifest consistency | `scripts/skyglass_check.py`; `state/skyglass_design/design_data.json`; `docs/workflows/SKYGLASS_CHECK.md` (RUL-2026-10-28-028 item 3) | none | itself |

### 1.5 Payouts and economy (structure; tables are in §5)

| Rule | Owner | Copies |
|---|---|---|
| Reward class and farm layer (uncapped pays materials only, the ladder, no door items, reveal discipline, profession materials, choice rewards, aim do not multiply) | `references/balance.md` ("Reward class and farm-layer doctrine") | `references/quest.md` ("Unlock graph") |
| Drop semantics: hunting drops ignore the chance field; guaranteed drops; AI item rows | laws 67, 68, 69 | `references/balance.md` tail |
| Loot chest mechanic | `references/item.md` §4 | none |
| Crafting recipe shape and the no-common-factor doctrine | law 22 | `references/item.md` |
| Reward timing and boosts by quest type | `references/quest.md` §3.4b item 7 | none |
| Component-chase economy default | `references/event.md` addendum item 2 | none |
| Skyglass: one home per item; ladder; picks; caches; charts; pets; tokens | `docs/design/SKYGLASS_LOOT_TABLES.md` and the rulings its sections cite | generators under `push/skyglass_*.gen.py`; `design_data.json` |
| Currency amounts on Skyglass content are set by the director in the in-game editor | RUL-2026-10-24-019 | status line of `SKYGLASS_LOOT_TABLES.md` |
| Rewards only for winning; ryo and exp on completion | RUL-2026-10-24-016, RUL-2026-10-28-022 | `SKYGLASS_LOOT_TABLES.md` |

### 1.6 Boss fight design

| Rule | Owner | Copies |
|---|---|---|
| Set-piece recipe (mark, marker, gated blast), fixed patterns, fallback rule | `docs/design/SKYGLASS_BOSS_FIGHTS.md` ("The tools we have", §5a, §6); RUL-2026-10-28-015, -024, RUL-2026-10-29-046, RUL-2026-10-30-060 | `library_spec.json` on the unmerged harness branches |
| Every fight follows the same rules (mark resolves next turn, phase cue, one burst tile) | RUL-2026-10-28-028 item 6 | `SKYGLASS_BOSS_FIGHTS.md` §10 |
| Telegraph art rides a non-visual ground carrier | RUL-2026-11-02-101 | `docs/design/SKYGLASS_BOSS_ANIMATIONS.md`; see C-04 |
| Damage model under shared cooldowns; faint floors | RUL-2026-11-06-128 | `docs/design/MOTHER_OF_ECHOES_ACT3.md` |
| Omens are marks; payoffs and lingering ground are paintings; the fight is a stage; colour by owner | RUL-2026-11-05-124 (scoped to the Mother of Echoes; see D-07) | `docs/design/MOTHER_OF_ECHOES_ART.md`; `docs/design/SAYO_BIBLE.md` §5 |
| Fight script is the design target beside the clear rates | RUL-2026-11-05-119 item 5 | `docs/design/MOTHER_OF_ECHOES_FIGHT_SCRIPT.md` |
| Character bible as the source of moves | `docs/design/SAYO_BIBLE.md` (the one example) | none |
| Per-fight targets (Wreck, Watch, Reliquary, Crownhold, the Haul, the Mother of Echoes) | RUL-2026-10-26-006, -007, RUL-2026-10-30-060, RUL-2026-11-02-097, RUL-2026-11-06-128 | the design docs each ruling names; harness reports on unmerged branches |
| Encounters are designed and tuned in the offline harness before any live edit | RUL-2026-10-26-006 item 1 | none |

### 1.7 Text

| Rule | Owner | Copies |
|---|---|---|
| Jutsu description and battle line house style; targeted edits; American English | `docs/design/jutsu_overhaul/WRITING_STYLE.md` (RUL-2026-10-21-021, -022) | none |
| Text and icon show the same moment | RUL-2026-10-24-004 | `docs/design/icon_overhaul/TEXT_AND_ICON_ROUND1.md` |
| Skyglass voice, banned words, item description format, chest description format, stakes lines, tier naming | `docs/design/SKYGLASS_TEXT.md`; `docs/design/SKYGLASS_STORY_BIBLE.md` (Voice); `SKYGLASS_LOOT_TABLES.md` §0; RUL-2026-10-28-028, -030, RUL-2026-10-29-057, -058, RUL-2026-10-31-074 | `skyglass_check.py` (`voice`, `chest-text`) |
| Battle text for shared and library jutsu follows the jutsu house style | RUL-2026-10-28-028 item 5 | none |
| Boss jutsu descriptions carry hint text players can read in battle | RUL-2026-11-05-123 item 3 | `docs/design/MOTHER_OF_ECHOES_JUTSU_TEXT.md`; see C-08 |
| Difficulty stars on charts and pyramids | RUL-2026-10-31-074 item 3; RUL-2026-11-05-119 item 6; RUL-2026-11-05-123 item 2 | `SKYGLASS_LOOT_TABLES.md` §0 |
| Length bounds | `45d` | none |

### 1.8 Still art

| Rule | Owner | Copies |
|---|---|---|
| Every art number (aspect, width, format, byte ceiling, key) | `producing-tnr-art/data/25x_DATA_art_spec.json` | laws 79 to 82, 84 cite it |
| Client rendering per field; editor preview | laws 50, 51, 80, 81 | `producing-tnr-art/SKILL.md` |
| Keying, glow, spill, fresh filenames | laws 32 to 35 | `producing-tnr-art/SKILL.md`; `chroma.py` |
| Battle assets must end unhidden | law 16c (RUL-2026-10-24-006) | `references/pipeline.md`; `processing.md`; `12b_LAWS_coverage.md` |
| Jutsu icon target, style library, isolated sessions | `25x` `JUTSU_ICON`; `docs/workflows/ISOLATED_ART_GENERATION.md`; RUL-2026-10-14-001, RUL-2026-10-17-021 | `producing-tnr-art/SKILL.md` |
| Asset folder and name convention | RUL-2026-11-05-127 as amended by RUL-2026-11-06-130 | `docs/design/MOTHER_OF_ECHOES_ART.md`; folder builders in `push/mother_of_echoes.gen.py` and `art/subaku_palace/` |

### 1.9 Combat animation

Every engine fact in this table is owned today by a handoff, a design doc or a ruling. None is an
engine law and none is in a skill (see G-08 to G-10).

| Rule | Where it is recorded today |
|---|---|
| Clip size ratio, 50 px rendition, strip format, folder pattern | `TNR_ANIMATION_HANDOFF.md` §1.1; `docs/design/COMBAT_ANIMATION_ENGINE.md` (older); `docs/design/SUBAKU_PALACE_ANIMATION.md` |
| Layering, start time, no delay, per-record start and load skew, lifetime | `TNR_ANIMATION_HANDOFF.md` §1.2 |
| Visual tags: targeting, parity, drop at the next round's first action, cost | `TNR_ANIMATION_HANDOFF.md` §1.3; RUL-2026-11-02-101 (the drop rule, with file and line at 3314d122) |
| AoE spiral coverage and unreachable rim hexes | `TNR_ANIMATION_HANDOFF.md` §1.4 |
| Shared cooldowns, lethal hits, damage floor, ground binding | `TNR_ANIMATION_HANDOFF.md` §1.5; RUL-2026-11-06-128 item 1; `MOTHER_OF_ECHOES_ACT3.md` §7 (ground binding) |
| Director's art rules (quality bar, omens, payoffs, lingering ground, stage, colour, restraint, clutter budget) | RUL-2026-11-05-124, -126; RUL-2026-11-06-128, -129; `TNR_ANIMATION_HANDOFF.md` §2 (items 7 and 8 have no ruling: G-11) |
| Techniques (slice mosaic, lattice paintings, caster-relative pieces, floor arrival, craft) | `TNR_ANIMATION_HANDOFF.md` §3; builders under `art/mother_of_echoes_fx/`, `art/subaku_palace/` |
| True-scale preview harness | `docs/handoffs/skill_overhaul/qa_preview.py.txt` (scratch paths; not runnable as committed) |
| Pipeline (design to live check) | `TNR_ANIMATION_HANDOFF.md` §4 |

---

## 2. Gaps: rules with no owner

Each is something a library entry, a tool or a skill page in the brief needs to cite, and cannot
today. Per the brief ("where a skill needs a rule that has no owner yet, create the owner first"),
the phase that needs it creates the owner. P0 creates none.

| Id | Missing rule | Evidence | Needed by | Suggested owner (not created) |
|---|---|---|---|---|
| G-01 | The AI rule cap has no law number. The constant is generated and `validate.py` enforces it, but with its own literal, and no engine law exists for a library entry to cite "by number" (brief §5.3). | brief §3 names `docs/ENGINE_LAWS.md` as the owner; no match there. | P2 (rule patterns state their count) | a new engine law citing `AI_PROFILE_MAX_RULES`, through reconciliation; `validate.py` and `design.py check` read the constant |
| G-02 | Shared cooldowns: which effect types share a lock, the lock length, per-caster scope, AI not exempt. Introduced upstream after the contract pin (C-01). | recorded only in `TNR_ANIMATION_HANDOFF.md` §1.5, RUL-2026-11-06-128, `SKYGLASS_BOSS_FIGHTS.md` §6 | P2 (loadout pacing, lock map), P4 | regenerated `45e` under the adopt gate, plus an engine law |
| G-03 | AI archetypes beyond three role names. `standard`, `elite`, `boss` are ratified; `calc.py` has stat shapes named skirmisher, support and others with no ratification record; the brief wants bruiser, skirmisher, caster, support, summoner, controller, boss by rank band. | `references/ai.md` §1.8; `enemy.py` ("a shape is a balance opinion"); `calc.py` `ROLES` | P2 (library 1) | library data file, each shape a director slot (D-05) |
| G-04 | Rule patterns as named, reusable groups. The behaviours exist only inside shipped records, generators and the unmerged `library_spec.json`. | `SKYGLASS_BOSS_FIGHTS.md` §5a, §6; `push/*.gen.py` | P2 (library 2) | library data plus one reference page |
| G-05 | AI attack weights by level and rank. `references/balance.md` §2 and `references/event.md` step 2 point to `references/ai.md` §1.6.1, which says "Superseded". | the three files named | P2 (library 3: damage tier per slot) | see RG-08 |
| G-06 | Dungeons, special and item-started quests, entry items, completion picks (`rewardMode`, pick count), weighted caches, treasure and chart hunts, hauls, steeping. No skill reference describes them; they live in Skyglass design docs, generators and Forge. | `references/quest.md` has no dungeon or pick section; `45e` has the `DUNGEON_*` constants only | P3 (library 5: most of the catalogued structures beyond battles, chains and branches) | a quest-structures reference page citing source at a pin |
| G-07 | Setups (scenes and characters, ally AIs, starting effects, objective debuffs, ground hazards, timed windows) as a catalogue. Fragments are spread over `references/quest.md`, `34b`, and Skyglass docs. | as stated | P3 (library 6) | library data plus one reference page |
| G-08 | Animation engine facts (§1.9 rows 1 to 4) have no law. The brief requires promotion through reconciliation. | `TNR_ANIMATION_HANDOFF.md` §1 | P5 | new engine laws; needs authorization (D-09) |
| G-09 | Ground effects bind to whoever stands on the hex when any action resolves; `onehitkill` semantics (target, chance, no damage packet). | `TNR_ANIMATION_HANDOFF.md` §1.5; `MOTHER_OF_ECHOES_ACT3.md` §7 | P2 fast checks, P4 | new engine laws |
| G-10 | Law 18 does not mention items, although RUL-2026-10-26-008 rules that it extends to them ("pending reconciliation"). | `docs/ENGINE_LAWS.md` law 18 | P2, P6 | law 18, through reconciliation |
| G-11 | Clutter budget and "restraint" (entrances stay inside the caster's clip). Recorded as director's rules in the handoff, with no ruling id. | `TNR_ANIMATION_HANDOFF.md` §2 items 7, 8; `MOTHER_OF_ECHOES_ART.md` (stacking pass) | P4 (library 4), P5 | a ruling, then the boss-grammar page (D-07) |
| G-12 | A general writing guide. Voice rules exist per project (jutsu overhaul, Skyglass, Sayo) and no file owns names, log lines and quest text across content. | §1.7 | P1 (§5.6) | the new writing-guide reference page, citing the three sources |
| G-13 | `references/jutsu_text.md` is cited by `WRITING_STYLE.md` as the owner of placeholder and effect text rules, "under review". It is not on main. | file absent in `skills/building-tnr-content/references/` | P1 | resolve with the reviewer: land it or drop the pointer |
| G-14 | Player profiles and gear tiers for tuning. The brief says gear tiers "come from the balance tables"; `references/balance.md` has none. Profiles exist only as code on the unmerged harness. | `references/balance.md`; harness `engine/` | P4 | data file on promotion; values are director slots (D-02) |
| G-15 | Live verification recipes (readback, in-battle effect read, player-report investigation). No page exists. | brief §7.3 | P6 | the new reference page |
| G-16 | The telegraph and omen grammar as one rule set. It is split across RUL-2026-10-28-024, -028 item 6, RUL-2026-11-02-101 and RUL-2026-11-05-124. | those rulings | P4 (library 4) | the boss-grammar page, citing the four |

## 3. Owner conflicts and stale owners

| Id | Conflict | Detail | Proposed handling |
|---|---|---|---|
| C-01 | More than one engine pin is in use. | Generated contracts: 3314d122 (2026-10-29). Harness `run.sh` default: c86f43f4. Animation handoff and final Mother of Echoes tuning: cb755375. Shared cooldowns arrived in b54541f1; the clip-ratio change in 338126cb. | Each phase states its pin. P2 and P4 need a pin that includes shared cooldowns, which means a contract regeneration under the adopt gate (`D-adopt-gate`). Reviewer and director to confirm before P2 (D-10). |
| C-02 | `includeDefaultRules` has three answers. | `references/ai.md` §7 gotchas: keep it true. Same file, "confirmed rule vocabulary": this project runs it false. `references/event.md` step 4: true. `SKYGLASS_BOSS_FIGHTS.md` §6: off, with backup rules restated. | One owner sentence in `references/ai.md`, the others cite it. Lane A edit in the phase that touches it (P2), not P0. |
| C-03 | "40 AP self-buff jutsu are unreliable as actions" (`references/ai.md` §7) against law 41b, which describes the Verge line opening every kit with a stance, and against the set-piece recipe's 40 AP mark. | as stated | Evidence check in P2 before the opener pattern is written. |
| C-04 | `SKYGLASS_BOSS_FIGHTS.md` §6 still says a mark is a `visual` ground jutsu. RUL-2026-11-02-101 moved marks off `visual`, and says its own destination doc has an out-of-date renderer description. | as stated | The boss-grammar page cites the ruling; the design doc fix is Skyglass work (RUL-2026-11-05-119 item 6 schedules doc fixes). |
| C-05 | Elite role defaults: `references/ai.md` §1.8 gives ranges; `enemy.py` uses the top of each range and calls the table ratified. | as stated | D-05. |
| C-06 | `EVENT_STRUCTURE.md` §8 lists Q1 to Q7 as open. RUL-2026-11-05-119 item 6 answered all but the progress surface. | as stated | Owner update when P3 touches it; only Q3 remains open (D-03). |
| C-07 | The mission reward ladder has four homes. | `data/48` (the ratified owner), `references/quest.md` §6.3 (a table), `calc.py` `REWARDS` (labelled "derived from the shipped set"), `references/balance.md` ("Observed template", D row). They agree today. | P3 `payout.py` reads `48` only; the copies become citations. |
| C-08 | Boss jutsu descriptions. The brief §5.6 calls them staff-only; the handoff §1.3 says the same; RUL-2026-11-05-123 item 3 says players can read them in battle and the hint text stays. | as stated | The ruling is the newer, cited source. Writing guide to follow it unless the director says otherwise (D-08). |
| C-09 | Franchise references. The brief allows "Naruto analogues" at the concept stage (§5.1) and sets the register as "Naruto-flavoured" (§5.6). `D-no-franchise` and `docs/00_INDEX.md` say never reference the franchise. | as stated | Doctrine outranks the brief (CLAUDE.md §2). P1 cannot write either line until the director rules on scope (D-06). |
| C-10 | Colour grammar. `SKYGLASS_BOSS_ANIMATIONS.md` and the art audit use bile green for lingering ground; RUL-2026-10-28-028 item 4 gives the tainted tier a rot-green seal; RUL-2026-11-05-124 item 4 bans sickly green "anywhere in the fight"; the handoff reads that as "ever". | as stated | D-07. |
| C-11 | Legacy file names in the references (`32_REGISTRY_shared_ai_pool.md`, `45_DATA_field_schemas.json`, `10_TECH_pipeline.md`, `30_DOCTRINE_balance.md`, `21_GUIDE`, `24_GUIDE`, `QUEST_ENGINE_ANALYSIS.md`, `44_DATA_id_registry.md`). | several no longer exist at those names | New skill pages cite current paths only. Cleaning the old references is outside this brief (§10). |
| C-12 | `data/48` rank D notes say the level band is null and that D combat is "blocked only on enemy_level_band", while the band is filled. | `48` `_variant_note` fields | Note for P3; no rule depends on the notes. |
| C-13 | Ruling ids repeat and the numbering has holes. | RUL-2026-10-25-002, RUL-2026-10-26-001 and RUL-2026-10-26-002 each head two different entries; the running suffixes -136 and -137 are each used on two dates (2026-11-07 and 2026-11-08; 2026-11-07 and 2026-11-09); there is, for example, no RUL-2026-10-22-005 or RUL-2026-11-03-113. The ledger's own rule is that entries are never renumbered. | Cite rulings by full id plus title where ambiguous. |
| C-14 | Who pushes the game. `D-user-pushes` and the `docs/00_INDEX.md` non-negotiables say the director's tap is the only act that touches the game and Claude never pushes it. RUL-2026-11-06-132 lets Claude write through the connector after gates and a go; its canonical destination is `CLAUDE.md` §6 only. | the doctrine text and the index were not amended | The brief §7.1 tells P6 to cite the operating model. The rendered doctrine block in `SKILL.md` would still contradict it. A doctrine edit is outside this brief and needs the director's word (D-11). |

---

## 4. What exists to build each library from

Short pointers for the phases; none of this was mined in depth in P0.

| Library (brief §5.3) | Shipped material found | Machine-readable today |
|---|---|---|
| 1 AI archetypes | `references/ai.md` §1.8; `references/lines.md`; `calc.py` `ROLES`; Skyglass tiers (RUL-2026-10-31-067, -077) | `enemy.py` `ROLE_DEFAULTS` only |
| 2 Rule patterns | set-piece library (`SKYGLASS_BOSS_FIGHTS.md` §5a, §6, §9); minor marks; fallback rule; `push/crownhold.gen.py`, `push/mother_of_echoes.gen.py`, `push/skyglass_*.gen.py` (41 generators) | `library_spec.json` and per-fight specs on the unmerged harness |
| 3 Loadout recipes | `data/32b`; line kits in `references/lines.md`; `calc.py kit` | `32b` |
| 4 Boss fight grammar | `MOTHER_OF_ECHOES_*` (five docs), `SAYO_BIBLE.md`, `SKYGLASS_BOSS_FIGHTS.md`, rulings in §1.6 | none |
| 5 Quest structures | `references/quest.md` §3, §6.1, §7; `data/48`; `EVENT_JOURNAL.md`; `SKYGLASS_DUNGEON_AND_TREASURE_HUNTS.md`, `SKYGLASS_THE_HAUL.md`, `SKYGLASS_HUNTS_CONTENT.md` | `48` (missions only); `26x` (event sheet) |
| 6 Setups | `data/34b`; quest scene fields; Skyglass hazards and rare-run twists | `34b` |
| 7 Payout model | §5 below | `48` rewards; `45e` drop table; `design_data.json` (Skyglass) |

Worked-example sources named in the brief were all found on main, with two exceptions:
`harness/skyglass_wreck_sim/` (branch only) and a Mother of Echoes design doc of record
(`docs/design/SKYGLASS_SEEDVAULT.md`, named by RUL-2026-11-01-093, does not exist; the five
`MOTHER_OF_ECHOES_*` docs stand in for it).

---

## 5. Reward tables

### 5.1 Ratified tables found

| Id | Table | Owner | Ratified by | Scope |
|---|---|---|---|---|
| R-01 | Individual mission reward ladder, ranks D to S (exp, ryo, prestige, tokens, clan points) | `data/48_DATA_mission_profiles.json` (`ranks.*.reward`, `_reward_ratified`) | director, 2026-08-26 | `questType: mission` only |
| R-02 | Mission gates and shape per rank (level window, attempts, objective count, battle nodes, enemies per battle, level band) | `data/48` (`_ratified_2026-08-27`) | director, 2026-08-27 | ranks D to A; S is open (RG-07) |
| R-03 | Hunting drop chance by hunting rank and item rarity | `45e` `HUNTING_ITEM_DROP_CHANCES` (law 67) | engine constant | hunting quests |
| R-04 | Dungeon reward and drop limits | `45e` `DUNGEON_MAX_*` | engine constants | dungeons (limits, not payouts) |
| R-05 | Verge line stat anchors | `references/lines.md` ("Rulings (2026-08-26)") | director, 2026-08-26 | three built rungs |
| R-06 | Skyglass ending ladder and its exp steps | RUL-2026-10-24-017, -018; `SKYGLASS_LOOT_TABLES.md` §4 | director | Skyglass |
| R-07 | Skyglass completion picks | RUL-2026-10-28-016, -034; `SKYGLASS_LOOT_TABLES.md` §4a | director | Skyglass |
| R-08 | Skyglass caches, consumable caches, profession chests, Haul chests | `SKYGLASS_LOOT_TABLES.md` §3, §3a, §4b; `SKYGLASS_PROFESSION_CHESTS.md`; `SKYGLASS_THE_HAUL.md`; rulings cited there | director, in part: the status line says weights and quantities are proposals unless marked ruled | Skyglass |
| R-09 | Skyglass shard, salvage and token rates | RUL-2026-11-02-099 item 5, -104, -107; `push/skyglass_uber_economy.gen.py` (`RATES`) | director | Skyglass |
| R-10 | Mother of Echoes clear rewards and pick | RUL-2026-11-03-110, RUL-2026-11-04-114; `push/mother_of_echoes.gen.py` | director | one fight |
| R-11 | Event journal Week 1 rewards | RUL-2026-11-05-121 item 3; `EVENT_JOURNAL.md` §4 | director | one page |
| R-12 | Event pacing by player type, and finale pacing | RUL-2026-11-01-096 item 4; made the default for future events, with per-event overrides, by RUL-2026-11-05-119 item 6 | director | all events |

Doctrine that shapes payouts without numbers (reward class, farm layer, choice rewards,
component chase) is in §1.5.

### 5.2 Gaps

The brief's payout model is "reward class × rank band × effort to money, XP, items, caches, drop
rates and event currency", read only from ratified tables. Against that:

| Id | Gap | What exists instead | Tool behaviour until ruled |
|---|---|---|---|
| RG-01 | No ratified currency table for any quest type except `mission`: story, event, battlepyramid, dungeon, raid, daily, hunting, gathering, special, achievement. | `references/quest.md` §6.3 lists story-act "reference points" from existing acts, not marked ratified; RUL-2026-10-24-018 caps exp for Skyglass endings only. | `AWAITING_RULING` per quest type and rank |
| RG-02 | The game's own reward-package catalog (content type × rank) is not in the repository. RUL-2026-10-24-019 makes it the director's source for amounts, set in the in-game editor, and tells manifests to leave currency fields alone unless he supplies values. A `rewardPackages` router is present in `45f`; no capture of its data was found. | none | currency left unset; slot named per record |
| RG-03 | No effort axis. Nothing maps expected minutes, fights or difficulty to a payout outside Skyglass's per-run decisions. | R-12 pacing targets; per-fight clear targets in rulings | slot |
| RG-04 | Event currency rates are Skyglass-only, and their modelled owner is not on main: `state/skyglass_economy/recommended.json` (named by RUL-2026-11-02-099) exists only on `fable/skyglass-economy-model`. | generators carry the shipped rates | slot per currency; Skyglass rates cited as an exemplar only |
| RG-05 | No default cache tier weights or roll counts. | Skyglass caches, proposals unless marked ruled (R-08) | slot per cache |
| RG-06 | No default drop rates for AI item drops, chart or key drops, or once-only dungeon drops. | Skyglass rates per ruling | slot per drop |
| RG-07 | S-rank mission profile: six fields deferred by the director on 2026-08-27 (`_awaiting`). | `mission.py` refuses S by design | unchanged: refuses |
| RG-08 | AI attack weights by level and rank (G-05). `references/balance.md` §2 gives a baseline and approximations and defers to a table that no longer exists. | per-record effects in `32b` | slot; loadout recipes use pool records as they are |
| RG-09 | Outcome variants (reduced, standard, bonus success) appear in `references/quest.md` §6.3 with no ratification record. | as stated | slot |
| RG-10 | Unsigned line: stat anchors are band medians with three "Decisions for you" still open (median or above, elements, drops). | `references/lines.md` | slot; Verge is the ratified exemplar |
| RG-11 | Reward tables for the new structures in the catalogue (treasure and chart hunts, hauls, dungeon clear, journal pages, tutorial) exist only as Skyglass instances. | R-06 to R-11 | slot per structure; exemplar cited |
| RG-12 | Clear-rate and timing targets per content kind. | per-fight rulings (§1.6); proposed standard bands in `EVENT_STRUCTURE.md` §8 Q1 are not ruled as bands | simulator reports without a verdict (brief §11.2) |
| RG-13 | Per-hit damage bands by enemy tier. | one reference precedent in `references/balance.md` §6 (calibration protocol), tied to a named event and armour | slot; calibration protocol cited |

Mining the current tables into `data/` "with a citation per row" (brief §5.3 item 7) is P3 work
and was not started.

---

## 6. Director decisions

### 6.1 Settled decisions that bind the overhaul

Ruling text read for this inventory (36; see §0 for depth): RUL-2026-10-21-021, -022; RUL-2026-10-24-016, -017, -018,
-019; RUL-2026-10-26-006, -007, -008; RUL-2026-10-28-015, -024, -028, -030, -034; RUL-2026-10-29-057,
-058; RUL-2026-10-30-060; RUL-2026-10-31-066, -071, -077; RUL-2026-11-01-096; RUL-2026-11-02-097,
-099, -101, -106; RUL-2026-11-03-110; RUL-2026-11-05-119, -121, -123, -124, -126, -127;
RUL-2026-11-06-128, -129, -130; RUL-2026-11-09-137 (skill overhaul).

| Area | Decision | Ruling |
|---|---|---|
| Overhaul | Brief approved; simulator may run the engine offline; targets and reward gaps come back for review; one phase per reviewed handoff; install each skill when its review passes | RUL-2026-11-09-137 (skill overhaul) |
| Delivery | Connector writes; run lock; operating model | RUL-2026-11-06-132, RUL-2026-11-07-133, -135 |
| Rewards | Amounts set by the director in game; ryo and exp on completion only; rewards only for winning; one home per item | RUL-2026-10-24-016, -019; RUL-2026-10-28-022; RUL-2026-10-25-002 (Skyglass reward restructure) |
| Economy | Three player types per weekend; finale pacing; trade is the pity; no crafter intermediaries on finale inputs; one playable route per key outcome; a gamble may starve content only with approval | RUL-2026-11-01-096; RUL-2026-11-02-104; RUL-2026-11-05-119 item 6 |
| Events | Event structure framework; weekly journal; one badge per event; difficulty stars stay on pyramids | RUL-2026-11-05-116, -119 to -122 |
| Encounters | Design-led tuning in the harness; rule cap trims; one record per measured tuning; set-piece lock; minor marks; same fight rules everywhere; fallback rule | RUL-2026-10-26-006; RUL-2026-10-31-066, -077; RUL-2026-10-28-015, -024, -028; RUL-2026-10-29-046 |
| Boss design | Telegraphs on a non-visual carrier; damage model under shared cooldowns; fight script is a design target; stun immunity for the finale boss | RUL-2026-11-02-101; RUL-2026-11-06-128; RUL-2026-11-05-119 |
| Tooling exceptions | Basic-attack rule target; AI-only cooldown floor exemption; per-manifest validate ledgers | RUL-2026-10-31-071; RUL-2026-11-02-106; `state/validate_exceptions/` |
| Text | Jutsu house style; targeted edits; tier and naming system; chest and item description formats; hint text stays readable | RUL-2026-10-21-021, -022; RUL-2026-10-29-058; RUL-2026-10-28-030; RUL-2026-10-31-074; RUL-2026-11-05-123 |
| Art | Art direction for the finale; asset folders and names; faint floors; light-only arrival; jutsu icon standard | RUL-2026-11-05-124, -126, -127; RUL-2026-11-06-128, -129, -130; RUL-2026-10-14-001 |
| Engine | Battle assets must not be hidden; law 18 extends to items | RUL-2026-10-24-006; RUL-2026-10-26-008 |

### 6.2 Open decisions found

Presented as cards in the shape of `docs/workflows/OPERATING_MODEL.md` §2, adapted: these are
decisions, not push jobs, so "Gates" and "Runner" do not apply and are omitted.

```
GO? D-01 Reward tables for the payout model
What changes:   nothing until ruled; payout.py leaves a named slot per quest type and rank
Visible to players:  no
Needs you:  choose how currency amounts enter designs (RG-01, RG-02):
            (a) keep RUL-2026-10-24-019 as is: tools never write currency, cards say "set in game"
            (b) capture the in-game reward-package catalog once and let tools propose from it
            (c) ratify a ladder per content kind, as was done for missions (R-01)
Blocks:  P3 (payout model)
```

```
GO? D-02 Clear-rate and timing targets per content kind
What changes:   nothing until ruled; the simulator reports rates with no pass or fail
Visible to players:  no
Needs you:  a table per content kind (finale boss, event boss, dungeon floor, weekly page) and
            which player profiles and gear tiers define it (RG-12, G-14). P4 brings the Mother of
            Echoes numbers and a proposal, as the brief §11.2 says.
Blocks:  P4 verdicts only
```

```
GO? D-03 Where "what have I done" lives for an event
What changes:   the event sheet's legibility table (EVENT_STRUCTURE.md §2 item 9)
Visible to players:  yes, on future events
Needs you:  the one framework question RUL-2026-11-05-119 left open. The journal is the proposed
            answer in EVENT_STRUCTURE.md §8 Q3; it is not ruled.
Blocks:  nothing; P3 carries it as a slot
```

```
GO? D-04 S-rank mission profile
What changes:   six fields in data/48 (RG-07)
Visible to players:  no
Needs you:  values, or confirm S stays deferred (deferred 2026-08-27)
Blocks:  nothing; eval set has no S mission
```

```
GO? D-05 AI archetypes and their numbers
What changes:   library 1: seven roles by rank band (G-03, C-05), attack weights (RG-08),
                the Unsigned line's three open questions (RG-10)
Visible to players:  no
Needs you:  P2 will bring one proposal table mined from shipped enemies. Until then every
            archetype value outside ai.md §1.8 is a slot.
Blocks:  P2 defaults only; structure can be built
```

```
GO? D-06 Franchise references in design work
What changes:   two lines of the new design skill (concept stage; writing register)
Visible to players:  no
Needs you:  the brief allows Naruto analogues as design references and a Naruto-flavoured
            register; D-no-franchise says never reference the franchise (C-09). Options:
            (a) doctrine stands everywhere: the skill says "ninja-world register", no analogues
            (b) amend the doctrine: analogues allowed in internal design notes only, never in
                any artifact that ships or any art prompt
Blocks:  P1 wording of §5.1 stage 2 and §5.6
```

```
GO? D-07 Boss fight grammar as standing rules
What changes:   library 4 and the animation skill cite one ruling instead of a handoff
Visible to players:  no
Needs you:  (1) is RUL-2026-11-05-124 standing for every boss, or the Mother of Echoes only?
            (2) "no sickly green": everywhere, or that fight only? Skyglass uses rot-green for
                the tainted tier and bile green for lingering ground (C-10)
            (3) the fixed danger colours (heavy, control, safe, etching) as a rule
            (4) the clutter budget and "restraint", which have no ruling (G-11)
Blocks:  P4 and P5 wording
```

```
GO? D-08 Boss jutsu descriptions: staff-only or player hint text
What changes:   one line of the writing guide
Visible to players:  yes, on future bosses
Needs you:  the brief says staff-only; RUL-2026-11-05-123 item 3 says players read them in
            battle and the hint voice stays (C-08). The ruling is followed unless you say otherwise.
Blocks:  nothing
```

```
GO? D-09 Authorization to add engine laws during the overhaul
What changes:   docs/ENGINE_LAWS.md gains laws for G-01, G-02, G-08, G-09, and law 18 gains
                items (G-10), each with file and line at a stated pin, through the
                reconciliation sequence of RUL-2026-09-08-004
Visible to players:  no
Needs you:  yes or no. CLAUDE.md §7 requires the owner change to be authorized; the brief
            requires the promotion (§6) but RUL-2026-11-09-137 does not mention law text.
Blocks:  P2 (G-01, G-02), P5 (G-08)
```

```
GO? D-10 Engine pin for the overhaul, and a contract regeneration
What changes:   45c/45d/45e/45f regenerated at a pin that includes shared cooldowns, adopted
                only through the mechanical gate (D-adopt-gate); the simulator pins the same SHA
Visible to players:  no
Needs you:  approve a regeneration as a separate Lane A task before P2, or direct P2 to read
            shared cooldowns from source at a stated pin without regenerating (C-01)
Blocks:  P2 lock map; P4
```

```
GO? D-11 Doctrine wording for connector writes
What changes:   D-user-pushes in docs/DOCTRINE.md and the matching non-negotiable in
                docs/00_INDEX.md, re-rendered into the mounted instructions and both SKILL.md files
Visible to players:  no
Needs you:  RUL-2026-11-06-132 changed who presses the switch but only CLAUDE.md §6 was
            amended (C-14). Approve bringing the doctrine line into step, as its own small
            Lane A change, or leave doctrine as is and have the build skill cite the ruling.
Blocks:  P6 wording
```

Other open items found, outside this brief's scope and listed so they are not lost:

- `state/active-context.md` (refreshed 2026-11-08): the director's go on Watch Log pages 3 and 4
  rewards and the page names; the Forge bundle budget; how the Mother of Echoes upload branch
  lands; whether to rewrite git history for large files; legacy law provenance (laws 19, 23, 37).
- `docs/design/SKYGLASS_TEXT.md` §9: tier colours outside the four rarities (item 8); variant
  battle lines (item 9).
- RUL-2026-11-02-099 item 7: First Blade and Wayfinder variant rates; the model re-run on the
  shorter Wreck. RUL-2026-11-05-119 item 4 and `MOTHER_OF_ECHOES_ACT3.md` §7: the three who
  refused, and An Absence, post-launch. RUL-2026-11-06-128 item 2: a reading-based alternative
  to the Act III clock, post-launch.
- RUL-2026-10-31-084: a validator fix for the `move_towards_opponent` false positive is "a later
  Lane A task". RUL-2026-10-31-091: harness specs on `fable/skyglass-rule-cap` not yet updated.

---

## 7. Tooling baseline (before any change)

T-01 to T-04, T-15 and T-16 were run on the rebased branch head. T-05 to T-14 were run on a4f0550;
`skills/` is byte-identical at fca8625, so they were not repeated. Exit codes unmasked.

| Id | Command | Result |
|---|---|---|
| T-01 | `python3 skills/building-tnr-content/scripts/doctrinemap.py .` | exit 0: 21 assertions, 18 referenced, 16 surfaces, 0 errors, 0 warnings |
| T-02 | `python3 skills/building-tnr-content/scripts/render_doctrine.py --check` | exit 0: all projections current |
| T-03 | `python3 skills/building-tnr-content/scripts/build_packs.py --check` | exit 0: all packs and TOCs current |
| T-04 | `python3 skills/building-tnr-content/scripts/lawmap.py .` | exit 0: 93 laws, 93 matrix rows, 0 errors, 5 warnings (laws 16d, 18, 37, 61, 69; the same five recorded in `state/active-context.md`) |
| T-05 | `factory.py --selftest` (cwd `data/`) | exit 0: 20/20 |
| T-06 | `enemy.py --selftest` | exit 0: 18 passed |
| T-07 | `profile_derive.py --selftest` | exit 0: 20 passed |
| T-08 | `catalog_sync.py --selftest` | exit 0 |
| T-09 | `selfcheck.py` | exit 0: 0 errors (it has no `--selftest` flag) |
| T-10 | `mission.py --selftest` (cwd `data/`) | **exit 1**: cannot find `25x_DATA_art_spec.json`; its search path is cwd, the scripts directory and `/mnt/project`, and it ignores `TNR_ART_SPEC` |
| T-11 | `mission.py --selftest` with every data file and the art spec copied into one scratch directory | **exit 1**: its own fixture puts 2 enemies in a rank D fight and the ratified profile caps D at 1 (`check_headcount`) |
| T-12 | `artpreflight_selftest.py` | exit 0: 98 passed |
| T-13 | `jutsu_studio_selftest.py` | exit 0: 191 passed |
| T-14 | `shotlist.py --selftest`, `rawqc.py --selftest`, `style_refs.py --selftest` | exit 0 each |
| T-15 | `python3 scripts/rulings_index.py --check` | exit 0: 308 rulings, index current |
| T-16 | `python3 scripts/check_large_files.py` | exit 0: 17 files over the limit, all on the allowlist |

Findings:

- **T-10 and T-11 mean `mission.py --selftest` is red on main.** T-10 is the defect already noted
  in `state/active-context.md`. T-11 is not noted anywhere: the selftest fixture and the
  ratified profile disagree, so the test fails even when it can find its data. The brief says
  "the existing selftests ... must stay green"; this one is not green to begin with. It needs a
  small fix on its own reviewed branch before P3 extends `mission.py`. Not fixed in P0.
- `validate.py`, `calc.py`, `harvest.py`, `schema_diff.py`, `lawmap.py`, `storyboard.py`,
  `sim_damage.py`, `sim_turns.py`, `pet_checks.py`, `variant_checks.py` and others have no
  `--selftest`; `selfcheck.py` covers part of `validate.py`.
- `render_doctrine.py` hard-codes two skills (`SKILLS`) and `build_packs.py` hard-codes one
  (`SKILL`). P1 must extend both (brief §2: "must learn about new skills rather than be bypassed").
- `doctrinemap.py` scans `docs/*.md` only, so this file (under `docs/handoffs/`) is outside its
  scan and adds no doctrine reference.
- Forge tests were not run in P0 (no Forge change).

## 8. Where the brief and the repository disagree

| Id | Brief says | Repository |
|---|---|---|
| B-01 | the brief was approved on main at a4f0550 | main moved to fca8625 while P0 ran: the ledger was split into `docs/rulings/` month files with a generated index (now matching the brief §0), `state/` was refreshed from its 2026-10-17 projection, a 5 MB new-file limit was added to CI, and Forge was rebuilt. `skills/`, `docs/design/`, `docs/workflows/`, the laws, the doctrine, the index and the brief are byte-identical between the two SHAs. |
| B-02 | `docs/ENGINE_LAWS.md` owns the rule cap and shared cooldowns (§3) | neither is a law (G-01, G-02) |
| B-03 | gear tiers "come from the balance tables" (§5.4) | no gear tier table (G-14) |
| B-04 | player profiles are perfect, real, everyone else (§5.4) | Act III results use perfect, real, average, ignore, camp; `engine/moe.ts` cells are elite and average with play or ignore |
| B-05 | merge the harness code, "not the big result files" (§5.4) | results are about 51 MB of the 58 MB directory; the remaining 6.7 MB includes specs of up to 1.9 MB each (`haul_spec.json`, `mother_of_echoes_spec.json`, `charts_spec.json`, `data/baseline.json`). Whether specs count as code needs a call from the reviewer before P4. Every file is under the new 5 MB CI limit (`scripts/check_large_files.py`); adding to its allowlist is a director decision. |
| B-06 | "pinned engine SHA" (§2), singular | several pins in use (C-01) |
| B-07 | the simulator runs from "the pinned game source" | it needs a local clone of the public game repository at a path outside this repo, Bun, and a one-time dependency install from the npm registry; none is in the repository. This environment has Bun and `unshare` but no game clone. P4 setup item. |
| B-08 | reward tables are mined from `balance.md` and the reward rulings (§5.3 item 7) | the only generic ratified table is in `data/48` (R-01); `balance.md` holds doctrine, not tables; the rulings are Skyglass-specific and one of them (RUL-2026-10-24-019) moves currency out of manifests |
| B-09 | staff-only descriptions on boss jutsu (§5.6) | C-08 |
| B-10 | Naruto analogues and register (§5.1, §5.6) | C-09 |

## 9. What each phase can rely on, and what it must settle first

| Phase | Ready to start on | Must be settled first |
|---|---|---|
| P1 | workflow, templates, schema family (`mission.py` sheet, `26x`, `design_data.json`), packaging hooks | D-06 for two lines; G-13; extend `render_doctrine.py` and `build_packs.py` |
| P2 | `enemy.py`, `32b`, `45c`, laws 14 to 18, 39 to 41b, 61 to 66, line exemplars | D-09 and D-10 (rule cap and shared cooldown owners); C-02; C-03; D-05 for defaults |
| P3 | `mission.py`, `48`, `references/quest.md`, `EVENT_STRUCTURE.md`, `EVENT_JOURNAL.md`, `skyglass_check.py` | T-11 fix; D-01; G-06 owner page |
| P4 | rulings and design docs in §1.6; harness on its branch | D-02; D-07; B-05; B-07; D-10 |
| P5 | handoff, builders, `artpreflight.py` | D-09 (G-08); D-07; the live clip ratio: `state/active-context.md` says the upstream revert of `EFFECT_ANIMATION_HEX_RATIO` is still pending, so the ratio stays a parameter read from the pin |
| P6 | `OPERATING_MODEL.md`, `FORGE_MCP_RUNNER.md`, `forge/tools/mcp_run.mjs` | G-15 design; D-11 (C-14); the afterburn report the brief's recipe is worked from is still open in `state/active-context.md` and needs one live read to close |
