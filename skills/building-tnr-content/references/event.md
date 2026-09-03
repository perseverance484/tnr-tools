# Event design sheet and its processing contract

> Migrated from `26_TEMPLATE_event_design.md` (Phase 3, 2026-08-26).
> Pointers refreshed and staff guidance expanded 2026-09-02.

A fill-in sheet for staff. Copy everything between the two rules, fill in what you know, and
submit it. An assistant reads the completed sheet against the repo canon (`docs/` laws,
`skills/*/references/`) and builds the whole event: enemies, jutsu kits, behaviour, quest,
dialog and art, delivered as candidate content for the Content Admin's approval before
anything goes live.

**How to fill it in (staff):**
- Fill what you know. Leave a field blank or write `AI` to let the assistant decide within doctrine.
- Write `NONE` to explicitly exclude something. That is different from leaving it blank.
- Anything marked **[BALANCE PROPOSAL]** is a suggestion only. Reward values, drop rates, stat
  tuning and difficulty gates are finalized by the Content Admin.
- Plain language is fine everywhere. You never need field names, JSON or API knowledge.
- Attach anything you have: reference images, a rough draft, a blueprint, a sketch of the map.
  A half-finished idea processes fine. Note what you attached in section 1.
- Do not use em dashes in dialog lines or choice text. Use commas, colons or hyphens.
- Do not reference Naruto or any franchise names, symbols or characters. Original content only.
- House vocabulary: "bounty contract", never "Bingo Book".

**What happens after you submit:**
1. The assistant reads the sheet and comes back with questions on anything ambiguous.
2. It builds enemies, kits, rules, dialog and art, and assembles one combined manifest.
3. `validate.py` must return zero errors before anything is handed over.
4. dauntless taps the builder. That is the only act that touches the live game.
5. Everything lands `hidden: true`. The Content Admin approves, then it is published.

---

## 1. Basics

- **Event name:**
- **One-line fantasy** (what the player gets to do or feel):
- **Content prefix** (a unique word stamped on every enemy and jutsu name to avoid collisions,
  e.g. "Drowned"):
- **Attachments** (reference images, draft, blueprint, moodboard; list what you are sending):
- **Event type** (pick one):
  - [ ] Battle gauntlet (a chain of fights climbing to a boss, battlepyramid style)
  - [ ] Story mission (dialog, choices, scripted battles across the map)
  - [ ] Repeatable event (a short reward-driven loop players run many times)
  - [ ] Raid boss (one big shared boss fight)
  - [ ] AI decides from the fantasy
- **When does it run?** Always available / specific window (give start and end dates) / AI decides:
- **Testing:** the event is built hidden and only published after approval. Write here only if
  you need something different:

## 2. Who can play it

- **Level range** (min and max, or blank for a proposal) **[BALANCE PROPOSAL]**:
- **Rank requirement** (e.g. Chunin and up, or blank):
- **Village restriction** (a specific village, or blank for everyone):
- **Prerequisite** (must a quest be completed first? name it, or blank):
- **How many attempts / completions per player** (e.g. one-time, once per day, unlimited)
  **[BALANCE PROPOSAL]**:

> Engine ceiling: max level, max attempts and max completes are each capped at 100. Ask for more
> and the whole record is rejected. Attempt and completion caps are only enforced for event,
> story, battlepyramid, starter and raid types; mission, errand and crime repeatables ignore them.

## 3. Story

- **Premise** (2 to 4 sentences: what is happening and why the player is involved):
- **Setting** (locations or backdrops the event moves through, in order if it matters):
- **Key characters** (villains, NPCs, the boss; a name and one line each):
- **Opening hook** (the first thing the player is told):
- **Victory outcome** (what changed because the player won):
- **Failure flavor** (what a loss looks like; is retrying part of the story?):
- **Tone** (e.g. grim, mysterious, heroic, comedic):

> **House standard, read this before writing the premise.** Missions read as short stories or
> anime episodes, not investigations. Somebody wants something out loud in the first minute, the
> player goes there, one person is in the way for a reason the player understands, one fight, one
> truth delivered in a LINE rather than a deduction, and the player goes home slightly worse off.
> Target 12 to 14 nodes. If the player has to hold three facts at once to follow it, the premise
> is too complicated and the assistant will say so rather than build it.
>
> **Motive audit.** Every actor needs a stated reason for their method AND a stated reason for not
> doing the obvious cheaper thing. If the villain could have just bought the thing, say why they
> did not.
>
> **Rank is set by who the player fights**, not by raw difficulty: C is untrained opposition,
> B is trained ninja, A is village or state level stakes.

## 4. Enemies

- **How many regular enemies:**    **Elites:**    **Bosses:**
- **Difficulty feel** (pushover / fair fight / hard / brutal; the actual numbers are balance)
  **[BALANCE PROPOSAL]**:
- **Reuse** (any existing enemy this should reuse or reskin? name it, or blank):

For each enemy (add rows as needed; any blank column is the assistant's call):

| Name (with prefix) | Element | Role (bruiser / caster / assassin / tank / support) | One-line identity | Signature move idea |
|---|---|---|---|---|
|  |  |  |  |  |
|  |  |  |  |  |
|  |  |  |  |  |

- **Boss mechanics wishes** (e.g. enrages below 30% health, opens with a shield, summons help,
  punishes players who stay close):

## 5. Jutsu and abilities

- **Enemy kits:** [ ] assistant designs each kit from role and element (default)
  [ ] I have specific ideas (list below)
- **Specific jutsu ideas** (name, what it does, which enemy uses it):
- **Player-facing reward jutsu?** (should winning teach the player a new jutsu? describe it,
  or NONE) **[BALANCE PROPOSAL]**:

> Kits are drawn from the shared AI jutsu pool by default so enemies reuse proven records instead
> of minting new ones. Signature moves are the exception, budget 3 or fewer per boss.

## 6. Battle structure

- **Number of fights start to finish:**
- **Any multi-enemy fights?** (which fights, which enemies together):
- **Order** (which enemies come first, who guards the boss):
- **On a loss:** retry that fight / restart the whole run / hard fail / AI decides:
- **Anything between fights?** (dialog beats, choices, item pickups, travel):

> A retry always sends the player back to the step BEFORE the fight, never straight into the
> fight again. That is an engine rule, not a preference.

## 7. Rewards [BALANCE PROPOSAL]

All values here are proposals; the Content Admin sets the final numbers.

- **Completion reward feel** (small / standard / finale-sized, or reference an existing mission's
  tier):
- **Currency / exp / tokens proposal** (or blank for a proposal from existing tiers):
- **Item drops** (a loot chest? specific items? new items to create?):
- **Anything unique** (a badge, a title, a one-off item):

## 8. Art direction

- **Palette and motifs** (colors, imagery, materials; e.g. "drowned ships, sickly green light,
  rusted anchors"):
- **Reference images** (attach them; say what each one is for, e.g. "this is the boss silhouette,
  this is the palette"):
- **Backgrounds needed** (one per stage or location; list them, or derive from section 3):
- **Boss dialog portrait?** (yes / no / AI decides):
- **Icon vibe** (what should the quest icon evoke?):
- Leave anything blank to use the standard art pipeline defaults.

> Reference images do the most work when they carry palette and material. They constrain
> composition much less reliably, so describe the composition in words as well.

## 9. Constraints and notes

- **Off-limits** (themes, imagery or mechanics to avoid):
- **Deadline or target date:**
- **Anything else the builder should know:**

## 10. Sign-off

- **Submitted by:**    **Date:**
- **Approved to build by Content Admin:** [ ] yes  [ ] pending

---

*Staff can stop here. Everything below is the assistant's build contract.*

## AI processing contract (for the assistant reading a submitted sheet)

Read `docs/00_INDEX.md` first for precedence and routing, then process the sheet in this order.
Everything produced is **candidate** content: built hidden, delivered for review, published only
on the Content Admin's acceptance.

1. **Interpret the sheet.** Blank or `AI` = your call within `references/balance.md`; `NONE` =
   excluded. Every **[BALANCE PROPOSAL]** value is a proposal: carry it into the build as a
   placeholder, list each one explicitly in the delivery summary for the Content Admin's decision,
   and never invent exact drop percentages the sheet did not give.
2. **Map the event type** to a quest pattern in `references/quest.md`: gauntlet -> battlepyramid
   (3.7, a dialog before every battle, per-stage resets); story mission -> generic quest with
   `defeat_opponents` chains (3.2, different sectors, `sectorType: "random"`, `failObjectiveId`
   everywhere); repeatable event -> `questType: event` loop (6.1); raid boss -> `questType: raid`
   rules (2.1). Section 6 of the sheet drives the objective graph; validate the flow rules
   (quest 1.2) before manifest time, and honour law 88 on resets.
3. **Design each enemy** with `references/ai.md` Workflow A: the spec, the stat block from role
   defaults (1.8) and the difficulty feel (numbers are balance placeholders), the kit from the
   attack-weight curve (1.6.1). Prefix every enemy and jutsu name with the sheet's content prefix
   and dedup against `answers/names_ai.json` and `answers/names_jutsu.json` plus the panel's live
   dedup.
4. **Design kits and any reward jutsu** with `references/jutsu.md` (payload shape 2.1) and the
   shared pool in `data/32b_DATA_pool.json`: reuse pool records across enemies, signature budget
   3 or fewer per boss. AI-kit jutsu are hidden, `jutsuType: "AI"`.
5. **Write behaviour rules** with `references/ai.md`: range gating on every attack rule, move
   fallback, ordered specific-to-general, `includeDefaultRules: true`. A rule that fires a
   SELF-target jutsu must itself target SELF and carries no distance gate (law 40). Boss mechanics
   wishes from section 4 become condition rules.
6. **Write dialog** to `references/quest.md` 6.2 and 6.2b: 1 to 3 sentences per node, no em dashes
   in node description or choice text, multi-choice menus fork to distinct targets, wrong choices
   teach, enemies and items named in objective text.
7. **Plan and produce art** with the `producing-tnr-art` skill: its production order, prompt
   scaffolds and chroma pipeline; palette from sheet section 8; franchise-safe always.
8. **Assemble one combined manifest** per `references/pipeline.md` 1.5, entity payload shapes in
   2.2 through 2.6 (AI record 2.4, scene asset creation contract 2.6): jutsu creates, AI entries
   with `rules`, asset entries, the quest with `@jutsu` / `@ai` / `@img` / `@scene` refs,
   `hidden: true` throughout. Build order is fixed: jutsu, assets, items, ai, aiProfile, quest.
   The builder preflights the manifest; fix anything it names before delivery.
9. **Deliver:** the enemy specs, the quest flow summary, the asset pack, the manifest, and a
   decision list of every balance placeholder awaiting the Content Admin. `validate.py` at zero
   errors before handover, and say that it ran.

## Addendum: post-Masquerade contract requirements (2026-07-18)

Every event design sheet and its processing now also specifies:
1. **Calibration anchor:** the declared dummy loadout the damage bands are tuned against (e.g.
   "PvE endgame armor"), with per-tier per-hit targets. Tuning is built as multiplicative row
   products from a sniffer anchor fight (`references/balance.md` protocol).
2. **Component-chase economy (default reward architecture):** one component per ending at
   difficulty-priced rates; a shared binder material across recipes; social/CYOA endings drop
   their OWN materials at knowledge-gated 70/35-style rates (knowledge doubles the take, never
   skips the fight); reward slots reserved on every win node for a filler layer even if undefined
   at build time.
3. **Committed-choice structure (the wings pattern, default for branch events):** entrances
   partition the endings; no shared everything-menu hub; gossip nodes single-continuation;
   exclusive intel picks. See `references/quest.md` 3.4b-2.
4. **Shared-pool kits:** all AI kits from `data/32b_DATA_pool.json`; signature budget 3 or fewer
   per boss at EP 70 or below.
5. **Launch block:** `consecutiveObjectives` true, plain-date window, maxAttempts/maxCompletes,
   the unhide list.
