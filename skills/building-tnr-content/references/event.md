# Processing a submitted event design sheet

> Migrated from `26_TEMPLATE_event_design.md` (Phase 3, 2026-08-26).
> Split 2026-09-02: the staff-facing canvas is `EVENT_SHEET.md` at repo root and carries no
> engine detail by design. This file is the build contract and is not handed to staff.

Staff copy `EVENT_SHEET.md`, fill it in and submit it. It is deliberately thin: plain language,
no field names, no doc pointers, no engine rules. Everything the sheet does not say is settled
here instead of being pushed onto the submitter.

## Reading the sheet

- Blank or `AI` = the assistant's call within `references/balance.md`. `NONE` = deliberately
  excluded. They are different and the sheet says so.
- Every **[BALANCE]** field is a proposal. Carry it as a placeholder, list every one explicitly
  in the delivery summary for the Content Admin, and never invent drop percentages the sheet did
  not give.
- The sheet's "Shape" tick maps to a quest pattern, section 2 below.
- Attachments arrive alongside the sheet. Reference images inform palette and material; treat
  their composition as non-binding unless the sheet describes it in words.
- Contradictions between an attached draft and the filled sheet get raised, not silently
  reconciled.
- Everything produced is candidate content: built hidden, delivered for review, published only
  on the Content Admin's acceptance.

## Build order

1. **Map the shape** to a pattern in `references/quest.md`: chain of fights -> battlepyramid
   (3.7, a dialog before every battle, per-stage resets); story -> generic quest with
   `defeat_opponents` chains (3.2, different sectors, `sectorType: "random"`, `failObjectiveId`
   everywhere); short reward loop -> `questType: event` (6.1); one big boss -> `questType: raid`
   (2.1). Sheet section 6 drives the objective graph; validate the flow rules (quest 1.2) before
   manifest time.
2. **Design each enemy** with `references/ai.md` Workflow A: stat block from role defaults (1.8)
   and the sheet's difficulty feel (numbers stay placeholders), kit from the attack-weight curve
   (1.6.1). Prefix every enemy and ability name with the sheet's naming word and dedup against
   `answers/names_ai.json` and `answers/names_jutsu.json` plus the panel's live dedup.
3. **Design kits and any reward jutsu** with `references/jutsu.md` (payload shape 2.1) and the
   shared pool in `data/32b_DATA_pool.json`: reuse pool records across enemies, signature budget
   3 or fewer per boss. AI-kit jutsu are hidden, `jutsuType: "AI"`.
4. **Write behaviour rules** with `references/ai.md`: range gating on every attack rule, move
   fallback, ordered specific-to-general, `includeDefaultRules: true`. A rule firing a SELF-target
   jutsu must itself target SELF and carries no distance gate (law 40). Sheet section 4's boss
   behaviour wishes become condition rules.
5. **Write dialog** to `references/quest.md` 6.2 and 6.2b: 1 to 3 sentences per node, no em dashes
   in node description or choice text, multi-choice menus fork to distinct targets, wrong choices
   teach, enemies and items named in objective text. House standard is the episode shape stated
   on the sheet: one want, one antagonist, one fight, one truth in a line, a cost at the end,
   12 to 14 nodes.
6. **Plan and produce art** with the `producing-tnr-art` skill: its production order, prompt
   scaffolds and chroma pipeline; palette from sheet section 8; franchise-safe always.
7. **Assemble one combined manifest** per `references/pipeline.md` 1.5, entity payload shapes in
   2.2 through 2.6 (AI record 2.4, scene asset creation contract 2.6): jutsu creates, AI entries
   with `rules`, asset entries, the quest with `@jutsu` / `@ai` / `@img` / `@scene` refs,
   `hidden: true` throughout. Build order is fixed: jutsu, assets, items, ai, aiProfile, quest.
   The builder preflights the manifest; fix anything it names before delivery.
8. **Deliver:** enemy specs, quest flow summary, asset pack, manifest, and a decision list of
   every balance placeholder awaiting the Content Admin. `validate.py` at zero errors before
   handover, and say that it ran.

## Constraints the sheet does not mention

The submitter is not asked to know these. Apply them and, where one blocks what the sheet asked
for, say so in the delivery summary rather than silently altering the design.

- `maxLevel`, `maxAttempts` and `maxCompletes` are each capped at 100; a larger value 400s the
  whole write. Attempt and completion caps are enforced only for `event`, `story`,
  `battlepyramid`, `starter` and `raid`; `mission`, `errand` and `crime` ignore them.
- A retry loop goes through `reset_quest` and must land on the node BEFORE the fight, never on a
  battle node (law 88). "Retry that fight" on the sheet means exactly this.
- Rank follows who the player fights: C untrained opposition, B trained ninja, A village or state
  level stakes. If the sheet's difficulty feel and its antagonist disagree, raise it.
- Every actor needs a stated reason for their method and a stated reason for not doing the obvious
  cheaper thing. A sheet that fails this gets a question, not an invented motive.
- House vocabulary: "bounty contract", never "Bingo Book".

## Addendum: post-Masquerade contract requirements (2026-07-18)

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
