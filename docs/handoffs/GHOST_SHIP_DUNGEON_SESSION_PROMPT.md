# Session prompt: Ghost Ship becomes a dungeon

Paste-ready opener for a new Claude Code session (director request, 2026-10-23).

~~~text
Repository: perseverance484/tnr-tools. Read CLAUDE.md first and follow it: verify the branch and SHA you work from,
read state/active-context.md, state/status.json, docs/00_INDEX.md, the relevant entries in docs/RULINGS.md, and
docs/DEVELOPMENT_WORKFLOW.md for any tooling work.

OBJECTIVE
Turn the Ghost Ship content into a DUNGEON. Today it is a quest line (two quest variants, the Skyglass Expedition
retheme) whose chests drop wide-range profession loot, which forced the quests to be limited to specific
professions. The update restructures every chest's drops so ALL players benefit, crafters included, which makes the
profession limits irrelevant. Use the player-choice reward option and the new reward caches/packages to make this a
genuinely good update.

THIS SESSION, IN ORDER (stop for the director at each decision point)
1. Research and report. Do not build or write anything to the game yet.
2. A design proposal for the director: dungeon structure, encounters, and the new drop/reward plan.
3. A tooling assessment: what the repository can and cannot build today (see TOOLING GAP below).
Only after the director approves the design and the tooling plan do you produce manifests.

WHAT TO READ (ghost ship history and current live state)
- Rulings: RUL-2026-10-10-001/-002/-003/-007, RUL-2026-10-11-001/-002/-004, RUL-2026-10-12-003/-012/-015,
  RUL-2026-10-13-001..003 (crafting caches), RUL-2026-10-20-002 (Ghost Ship chest icons). Read them in full.
- Design: docs/design/GHOST_SHIP_SKYGLASS_FULL_MANIFEST_ROADMAP.md, docs/design/GHOST_SHIP_CRYSTAL_ENGINE_CORRECTION_PROPOSAL.md,
  docs/design/crafting_caches/ (caches_draft.json: Medicine Inro, Shinobi Tool Pouch, Sage's Strongbox).
- Harnesses: harness/ghost_ship_* (legacy baseline, stage2, consume, release dry-run, final) and their READMEs.
- Push history: push/README.md and archive/spent-manifests/ entries naming Ghost Ship, Skyglass, Keel Walk, the
  Guardian/Sentinel, the crafting caches (push/90-97, 132, 139, 140) and their results bundles in harvests/inbox.
- Live state: the newest committed captures of both Ghost Ship quests, their AIs (ten Ghost Ship AIs at JONIN caps),
  chests/caches and their loot tables. If the captures are stale, write a read-only Forge capture for the director to
  run; do not assume.

THE NEW SYSTEMS (pinned game source: studie-tech/theninjarpg at 107d7a8; verify before relying on it)
- Dungeons are their own entity, not a quest type: app/src/validators/dungeon.ts, app/src/server/api/routers/dungeon.ts,
  constants in app/drizzle/constants.ts (DUNGEON_PARTY_SIZE 3, DUNGEON_RUN_SECONDS 3600, up to 4 tiers of exactly 5
  floors, floor kinds floor/mini-boss/boss, up to 5 waves of up to 10 AIs per floor, up to 100 drops). Rewards: money,
  experience, tokens, prestige, and drops of type item, jutsu, cache or package, each with a chance and quantity;
  every party member rolls each drop. Placement by sector/longitude/latitude, a combat background biome, an optional
  structure asset, hidden by default.
- Reward packages (the "reward caches"): app/src/validators/rewardPackages.ts. Reusable named reward payloads
  (catalog packages, snapshotted when attached) usable on quests, objectives and dungeon drops.
- Player choice: quests can set rewardMode "choose" (app/src/validators/objectives.ts around line 783;
  app/src/validators/rewards.ts REWARD_CHOICE_AMOUNT_FIELDS / REWARD_CHOICE_CONTENT_FIELDS / RewardChoiceCardSchema):
  each eligible reward becomes a card the player picks. Find out exactly where choice is available (quests and
  objectives? dungeons? caches?) and design around what the source supports, not what would be convenient.

DESIGN GOALS (the director's)
- Every chest/drop is worth something to every player: combat players and every crafting profession alike. No drop
  table that only one profession can use; where profession materials remain, offer them through choice or through
  caches that let each player take what fits them.
- Use the choose option and reward packages so players pick what they need, instead of random profession-specific
  loot.
- Keep what was good about Ghost Ship: the Skyglass theme, the retained legacy jutsu, the Skyglass Katana drop and
  the AI roster, unless the director says otherwise. Map the existing encounters onto dungeon tiers, floors and boss
  floors.
- The dungeon replaces the profession-limited quests: propose what happens to the two existing quests (retire,
  hide, or keep as a story lead-in), and say what each option means for players. Retiring or hiding content is the
  director's call.

USER-OWNED DECISIONS (CLAUDE.md section 10): balance, reward values and drop chances, rarity, what gets retired or
hidden, art direction and final prose. Propose with options and consequences; do not settle them.

TOOLING GAP (check, then report as Lane A work if confirmed)
Forge and the generated contracts do not appear to know the dungeon entity yet (forge/src/runner/recipes.mjs has no
dungeon recipe; skills/building-tnr-content/data/45d_DATA_entity_schemas.json lists jutsu, item, bloodline, quest,
gameAsset, aiRule; reward packages may be missing too). Confirm this. If true, building the dungeon needs either the
director to build it in the in-game editor from your spec, or a Lane A change (contract extraction for dungeon and
reward packages, a Forge recipe, tests) on a fable/* branch with ChatGPT review per docs/DEVELOPMENT_WORKFLOW.md.
Lay out both options with their cost; the director chooses.

RULES
- You send no live game requests and use no credentials. The director runs every manifest. Captures are read-only
  manifests for the director to run.
- Suggest mode refuses quests, creates that other records reference, and Bloodright trees; plan delivery accordingly.
- Never edit a jutsu an AI has equipped through suggest mode without flagging it (laws 18, 60).
- Every manifest must pass validate.py --strict (run from skills/building-tnr-content/data) and
  node forge/tools/check_manifest.mjs (run from forge/). Commit tickets to main with a push/README.md entry.
- Prefer small batches grouped by kind of fix.

FIRST DELIVERABLE
A short report: (1) what Ghost Ship is today (quests, nodes, AIs, chests and their drop tables, profession limits),
(2) what the dungeon system can do and where choice and packages fit, (3) a proposed dungeon outline with a drop and
reward plan where every chest serves every player, with the decisions the director must make listed as options,
(4) the tooling gap and the two ways to build it.
~~~
