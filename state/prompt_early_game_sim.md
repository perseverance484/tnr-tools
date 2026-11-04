# Brief: early-game experience simulator, levels 1-70

- **Owner:** Fable (Claude Code). **Lane:** A (new tooling) on a `fable/early-game-sim` branch, exact-SHA handoff for ChatGPT review (`docs/DEVELOPMENT_WORKFLOW.md`). Content changes it leads to are Lane B and need director approval first.
- **Requested by:** the director, 2026-11-04: "A new priority for me is making the early game as engaging as we've made these end game fights ... makes an offline version of the game and Sims low level players experience accurately from level 1 to level 70. I want to make that gameplay loop enjoyable."
- **Boundary:** zero live game requests, no credentials, no session cookies (CLAUDE.md section 6). Read the game source at its pin; run it only inside the offline harness (socket-denied, as the Skyglass sim does).

## Goal

Build an offline model of a new player's journey from level 1 to 70 that is accurate enough to find where the early game is slow, confusing, too hard, too easy or unrewarding. Then propose changes that make the loop engaging, with the evidence to back each one. "Accurate" comes before "engaging": a recommendation built on a wrong player model is worse than none.

## What already exists (start here)

- **Combat engine sim:** `harness/skyglass_wreck_sim/` on `fable/mother-of-echoes-sim` (read its `README.md`). It runs the real combat code from a `git archive` of the game at a pinned SHA (currently `3314d122`) in a socket-denied child (`harness/ghost_ship_final/tools/offline_exec.py`). It already supports seeded runs, player models, AI rules, the 20-rule cap, movement and kiting, summons, ground effects, telegraph reads and per-source damage accounting. Reuse it; do not fork a second combat engine.
- **Player models:** `engine/moe_lib.ts` (`playerModel`, `realModel`, `AVG_GEAR`, `ELITE_GEAR`) and `engine/cclib.ts`. Only the endgame tier is calibrated, from two director battle logs (`loveispure` vs The Captain).
- **Game source:** `/home/claude/studie-tech/theninjarpg`, read with `git show <pin>:<path>`.
- **Repository authority:** `docs/00_INDEX.md`, `docs/ENGINE_LAWS.md`, `docs/RULINGS.md`; content skill `skills/building-tnr-content/`.

## Lesson from the Mother of Echoes (2026-11-04): calibrate players from evidence

The uber sim modelled endgame players at about 30,000 HP when real ones have about 5,050 base (6,250 with the Kitsune set). An early failure ("the player dies in round 2") was fixed by raising player HP instead of questioning the enemy side, and five tuning passes were built on it. For this project:
1. Derive every player number per level band (pools, stats, damage, gear, jutsu, sustain) from the game source's formulas and from director-supplied evidence (logs, screenshots, captures). Mark each one as source-derived, log-backed or assumed.
2. When a result looks wrong, question both sides. Never patch the player model to make a fight "work".
3. Present the assumed numbers to the director early. They know their players.

## Scope (first pass)

1. **Inventory the early game from source:** what a player can do at each level band (1-10, 10-20, ... 60-70): missions, quests, the arena, training, crafting, the village, item shops, jutsu learning, bloodlines, rank gates, and how experience, ryo, stats and pools grow (formulas with file:line).
2. **Live content the source does not hold:** the early AI enemies, quests, items and jutsu are database records. List what is needed and where it might come from (committed captures in the repo, `harvests/`, read-only capture manifests the director runs). Do not invent records.
3. **Progression model:** a simulated player (casual, engaged, optimal) choosing activities by level, with time per action, so the sim yields time-to-level, ryo and gear over time, power versus enemies by band, and fight win rates and lengths.
4. **Engagement read:**
   - dead zones (long stretches with nothing new);
   - difficulty spikes and walls;
   - fights decided before they start;
   - rewards that don't matter;
   - systems unlocked too late or never explained;
   - how quickly new jutsu and choices arrive.
5. **Recommendations:** each tied to a measured problem, with the content change it implies and its predicted effect, re-simulated.

## Decisions to settle with the director before building deep

- Which activities count as "the early game loop" and which are out of scope.
- What "engaging" means in measurable terms (for example a new unlock every N minutes, fights won 60-80% at level, no stretch over X minutes without a choice).
- Which player types matter most (new casual, returning, alt).
- What evidence he can supply for low-level players (logs, screenshots, a fresh character's numbers).

## Deliverables

- The sim on `fable/early-game-sim`, with a README and tests, frozen at an exact SHA for review.
- A report: the level 1-70 journey per player type, the problem list ranked by impact, and recommendations with before/after numbers.
- Clearly separated evidence tiers for every number.
