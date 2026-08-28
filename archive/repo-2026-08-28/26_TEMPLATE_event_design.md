> **STALE - archived 2026-08-28 (rollout Stage 2).** Superseded by the skill references and generated data under /skills/, and by /docs/ENGINE_LAWS.md. Do not build from this file.

# 26 - TEMPLATE: Event Design Sheet

A fill-in sheet for staff. Copy everything below the line, fill in what you know, and submit it. An AI assistant reads the completed sheet against the source stack (00-45) and builds the whole event: enemies, jutsu kits, behavior, quest, dialog, and art, delivered as candidate content for the Content Admin's approval before anything goes live.

**How to fill it in (staff):**
- Fill what you know. Leave a field blank or write `AI` to let the assistant decide within the game's design doctrine.
- Write `NONE` to explicitly exclude something (that is different from leaving it blank).
- Anything under a **[BALANCE PROPOSAL]** header is a suggestion only. Reward values, drop rates, stat tuning, and difficulty gates are finalized by the Content Admin.
- Plain language is fine everywhere. You never need field names, JSON, or API knowledge.
- Do not use em dashes in dialog lines or choice text; use commas, colons, or hyphens.
- Do not reference Naruto or any franchise names, symbols, or characters. Original content only.

---

## 1. Basics

- **Event name:**
- **One-line fantasy** (what the player gets to do or feel):
- **Content prefix** (a unique word stamped on every enemy and jutsu name to avoid collisions, e.g. "Drowned"):
- **Event type** (pick one):
  - [ ] Battle gauntlet (a chain of fights climbing to a boss, battlepyramid style)
  - [ ] Story mission (dialog, choices, investigation, scripted battles across the map)
  - [ ] Repeatable event (a short reward-driven loop players run many times)
  - [ ] Raid boss (one big shared boss fight)
  - [ ] AI decides from the fantasy
- **When does it run?** Always available / specific window (give start and end dates) / AI decides:
- **Testing:** the event is built hidden and only published after approval. Write here only if you need something different:

## 2. Who can play it

- **Level range** (min and max, or blank for AI proposal) **[BALANCE PROPOSAL]**:
- **Rank requirement** (e.g. Chunin and up, or blank):
- **Village restriction** (a specific village, or blank for everyone):
- **Prerequisite** (must a quest be completed first? name it, or blank):
- **How many attempts / completions per player** (e.g. one-time, once per day, unlimited) **[BALANCE PROPOSAL]**:

## 3. Story

- **Premise** (2 to 4 sentences: what is happening and why the player is involved):
- **Setting** (locations or backdrops the event moves through, in order if it matters):
- **Key characters** (villains, NPCs, the boss; a name and one line each):
- **Opening hook** (the first thing the player is told):
- **Victory outcome** (what changed because the player won):
- **Failure flavor** (what a loss looks like; is retrying part of the story?):
- **Tone** (e.g. grim, mysterious, heroic, comedic):

## 4. Enemies

- **How many regular enemies:**    **Elites:**    **Bosses:**
- **Difficulty feel** (pushover / fair fight / hard / brutal; the actual numbers are balance) **[BALANCE PROPOSAL]**:

For each enemy (add rows as needed; any blank column is the AI's call):

| Name (with prefix) | Element | Role (bruiser / caster / assassin / tank / support) | One-line identity | Signature move idea |
|---|---|---|---|---|
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

- **Boss mechanics wishes** (e.g. enrages below 30% health, opens with a shield, summons help, punishes players who stay close):

## 5. Jutsu and abilities

- **Enemy kits:** [ ] AI designs each kit from the enemy's role and element (default)  [ ] I have specific ideas (list below)
- **Specific jutsu ideas** (name, what it does, which enemy uses it):
- **Player-facing reward jutsu?** (should winning teach the player a new jutsu? describe it, or NONE) **[BALANCE PROPOSAL]**:

## 6. Battle structure

- **Number of fights start to finish:**
- **Any multi-enemy fights?** (which fights, which enemies together):
- **Order** (which enemies come first, who guards the boss):
- **On a loss:** retry that fight / restart the whole run / hard fail / AI decides:
- **Anything between fights?** (dialog beats, choices, item pickups, travel):

## 7. Rewards [BALANCE PROPOSAL]

All values here are proposals; the Content Admin sets the final numbers.

- **Completion reward feel** (small / standard / finale-sized, or reference an existing mission's tier):
- **Currency / exp / tokens proposal** (or blank for an AI proposal from existing tiers):
- **Item drops** (a loot chest? specific items? new items to create?):
- **Anything unique** (a badge, a title, a one-off item):

## 8. Art direction

- **Palette and motifs** (colors, imagery, materials; e.g. "drowned ships, sickly green light, rusted anchors"):
- **Backgrounds needed** (one per stage or location; list them, or AI derives from section 3):
- **Boss dialog portrait?** (yes / no / AI decides):
- **Icon vibe** (what should the quest icon evoke?):
- Leave anything blank to use the standard art pipeline defaults.

## 9. Constraints and notes

- **Off-limits** (themes, imagery, or mechanics to avoid):
- **Deadline or target date:**
- **Anything else the builder should know:**

## 10. Sign-off

- **Submitted by:**    **Date:**
- **Approved to build by Content Admin:** [ ] yes  [ ] pending

---

## AI processing contract (for the assistant reading a submitted sheet)

Read `00_INDEX.md` first, then process the sheet in this order. Everything produced is **candidate** content: built hidden, delivered for review, published only on the Content Admin's acceptance.

1. **Interpret the sheet.** Blank or `AI` = your call within `30_DOCTRINE_balance.md`; `NONE` = excluded. Every **[BALANCE PROPOSAL]** value is a proposal: carry it into the build as a placeholder, list each one explicitly in the delivery summary for the Content Admin's decision, and never invent exact drop percentages the sheet did not give.
2. **Map the event type** to a quest pattern in `23_GUIDE_quest.md`: gauntlet -> battlepyramid (3.7, a dialog before every battle, per-stage resets); story mission -> generic quest with `defeat_opponents` chains (3.2, different sectors, `sectorType: "random"`, `failObjectiveId` everywhere); repeatable event -> `questType: event` loop (6.1); raid boss -> `questType: raid` rules (2.1). Section 6 of the sheet drives the objective graph; validate the flow rules (23 section 1.2) before manifest time.
3. **Design each enemy** with `21_GUIDE_ai_enemy.md` Workflow A: the spec, the stat block from role defaults (1.8) and the difficulty feel (numbers are balance placeholders), the kit from the attack-weight curve (1.6.1) and doctrine 2. Prefix every enemy and jutsu name with the sheet's content prefix and dedup against `40`/`42` catalogs.
4. **Design kits and any reward jutsu** with `20_GUIDE_jutsu.md` and doctrine 1/4 (40 AP setup, 60 AP damage, tag budget). AI-kit jutsu are hidden, `jutsuType: "AI"`.
5. **Write behavior rules** with `24_GUIDE_ai_behavior.md`: range gating on every attack rule, move fallback, ordered specific-to-general, `includeDefaultRules: true`. Boss mechanics wishes from section 4 become condition rules (health thresholds, round gates, summon checks).
6. **Write dialog** to `23_GUIDE_quest.md` 6.2: 1 to 3 sentences per node, no em dashes in dialog text, wrong choices teach, enemies and items named in objective text.
7. **Plan and produce art** with `25_GUIDE_assets.md`: production order in its section 5, prompt scaffolds in section 2, palette from sheet section 8, franchise-safe always.
8. **Assemble one combined manifest** per `10_TECH_pipeline.md` 1.5: jutsu creates, AI entries with `rules`, asset entries, the quest with `@jutsu` / `@ai` / `@img` / `@scene` refs, `hidden: true` throughout. The v4.12 builder preflights it; fix anything it names before delivery.
9. **Deliver:** the enemy specs, the quest flow summary, the asset pack, the manifest, and a decision list of every balance placeholder awaiting the Content Admin.

## Addendum: post-Masquerade contract requirements (2026-07-18)

Every event design sheet and its AI processing now also specifies:
1. **Calibration anchor:** the declared dummy loadout the damage bands are tuned against (e.g. "PvE endgame armor"), with per-tier per-hit targets. Tuning is built as multiplicative row products from a sniffer anchor fight (30_DOCTRINE protocol).
2. **Component-chase economy (default reward architecture):** one component per ending at difficulty-priced rates; a shared binder material across recipes; social/CYOA endings drop their OWN materials at knowledge-gated 70/35-style rates (knowledge doubles the take, never skips the fight); reward slots reserved on every win node for a filler layer even if undefined at build time.
3. **Committed-choice structure (the wings pattern, default for branch events):** entrances partition the endings; no shared everything-menu hub; gossip nodes single-continuation; exclusive intel picks. See 23 3.4b-2.
4. **Shared-pool kits:** all AI kits from 32_REGISTRY_shared_ai_pool.md; signature budget <= 3 per boss at EP <= 70.
5. **Launch block:** consecutiveObjectives true, plain-date window, maxAttempts/maxCompletes, the unhide list.
