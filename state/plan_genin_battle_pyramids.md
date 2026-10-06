# Genin Battle Pyramids — Design Plan

**Status:** PROPOSAL — user approval required before manifest/build work  
**Design owner:** ChatGPT, Content Designer lead  
**Implementation owner after approval:** Fable / Claude Code  
**Frozen evidence baseline:** `main@b6f719dc5241f2b4fefc553670a61ea0c4a16d6e`  
**Fresh live quest census:** `harvests/inbox/tnr_results_1791233210169.json` (DONE / success)  
**Live requests/writes in this design pass:** 0 / 0

## Goal

Add three low-level `battlepyramid` challenges aimed at Genin progression:

- Level 15 — introductory combat fundamentals.
- Level 20 — first mixed-role encounter.
- Level 25 — simple ninja-on-ninja target-priority challenge.

These are deliberately ordinary TNR threats. They should feel like increasingly serious field hazards, not miniature raids, lore bosses, or mechanic checks.

## Current-state anchors

- Genin has `LVL_CAP: 30`; Student is capped at level 10.
- `battlepyramid` must place a non-battle node between every `start_battle`; otherwise later fights can pre-activate and skip.
- Recommended entry behavior is per-floor retry: each battle fails into a `reset_quest` that returns to that battle's preceding dialog.
- Current live level-10 Genin pyramid, **Kuroganekai: The Order of Black Steel GENIN**, has five scaled fights and reaches 2–3 enemies per battle. This proposal intentionally starts below that pressure curve instead of copying it.
- Ratified mission encounter doctrine allows one enemy in D combat and up to two in C. This is mission doctrine rather than battlepyramid doctrine, but it is a useful low-level pressure reference.
- New AI kits should use the shared AI pool; do not mint one-off jutsu for these pyramids.

## Shared design rules

1. **Fixed encounters, not user scaling.** Set `opponent_scaled_to_user: false`. The point of the 15 / 20 / 25 gates is to create readable milestones.
2. **Genin window.** Proposed `maxLevel: 30` on all three. This targets the Genin level band and prevents them from becoming generic high-level farms.
3. **Quest rank.** Level 15 uses D; levels 20 and 25 use C. Genin can start D/C; Student cannot reach the level gates.
4. **No hard-counter mechanics.** No seal, hard stun chains, movement lock, absorb, reflect, redirection, summon checks, one-hit kills, cleanse prevention, or similar mechanics.
5. **Simple AI.** Standard enemies: GENIN rank, `statsMultiplier: 1`, `poolsMultiplier: 1`, no passive AI tags, no special boss signatures. Prefer no armor on wildlife/basic regulars; at most AI Light on human leaders/guards.
6. **Shared-pool kits only.** Favor basic strikes, ranged shots, elemental bolts, and mild 10–15% offensive/defensive utility. No bespoke jutsu.
7. **Teach one idea at a time.** Level 15 = direct 1v1 fundamentals. Level 20 = melee vs ranged plus one 1v2. Level 25 = role recognition and two-enemy target priority.
8. **Per-floor recovery loop.** Failure/flee returns to the dialog immediately before the failed fight, not to the beginning of the entire pyramid.
9. **Rewards only on terminal victory.** No per-floor payouts. Exact reward values and repeat cadence are reserved for user approval.
10. **Ship hidden.** `hidden: true` until the user explicitly publishes.

---

## Pyramid 1 — Brushland Gauntlet

**Gate:** Level 15–30  
**Quest rank:** D  
**Purpose:** First true Genin battle gauntlet. Teach movement, AP use, cooldown pacing, and the difference between quick and heavy melee pressure without requiring matchup knowledge.

**Fantasy:** A commonly traveled woodland route has become dangerous after aggressive animals begin holding the trail. The assignment is simple: clear the path before travelers are hurt.

### Encounter ladder

| Floor | Encounter | Proposed AI level | Read |
|---|---|---:|---|
| 1 | Brush Boar | 12 | Slow, direct bruiser; basic damage only. |
| 2 | Ridge Wolf | 13 | Faster skirmisher; longer reach / more frequent light attacks. |
| 3 | Black Bear | 15 | Solo capstone; heavier attacks and slightly more durable, but no gimmick. |

**Enemy ceiling:** 1 at a time.  
**AI roster:** 3 records.  
**Mechanical vocabulary:** basic strike family only; optional mild self-buff on the capstone, no control.  
**Boss treatment:** Black Bear is a stronger standard enemy, not a raid-style boss. No passive steroid and no inflated pool multiplier.

**Why it exists:** A level-15 Genin should be able to understand every loss immediately: positioning, overspending AP, or taking too many direct hits. Nothing here should demand a specific build.

---

## Pyramid 2 — The Broken Tollhouse

**Gate:** Level 20–30  
**Quest rank:** C  
**Purpose:** Introduce human opponents, range differences, and the first simple multi-target decision.

**Fantasy:** A petty road gang has occupied an abandoned tollhouse and begun extorting travelers. They are criminals with practical weapons, not elite ninja or supernatural threats.

### Encounter ladder

| Floor | Encounter | Proposed AI level | Read |
|---|---|---:|---|
| 1 | Tollroad Cutter | 17 | Straight melee attacker. |
| 2 | Tollroad Slinger | 18 | Ranged attacker; teaches closing distance. |
| 3 | Tollroad Cutter + Tollroad Slinger | 17 + 18 | First 1v2; choose which pressure source to remove first. |
| 4 | Tollhouse Captain | 20 | Solo leader using simple attacks plus one light defensive/offensive stance. |

**Enemy ceiling:** 2 at a time.  
**AI roster:** 3 records.  
**Mechanical vocabulary:** basic melee/ranged damage, one mild mark/debuff or light barrier at most. Avoid reliable stun.  
**Leader treatment:** GENIN rank, standard multipliers; AI Light armor is acceptable if testing shows the solo finale is too fragile.

**Why it exists:** This is the transition from “fight what is in front of you” to “read the opponent.” It teaches that a ranged enemy and a melee enemy create different positioning pressure without adding exotic mechanics.

---

## Pyramid 3 — Wayward Training Ground

**Gate:** Level 25–30  
**Quest rank:** C  
**Purpose:** Cap the entry Genin ladder with basic ninja-vs-ninja combat: mild buffs/defenses, a simple elemental attacker, and two-enemy role combinations.

**Fantasy:** A disused training ground has been taken over by a small group of rogue shinobi using it to drill and prey on nearby traffic. They are competent enough to be dangerous to a Genin, but still low-grade field threats.

### Encounter ladder

| Floor | Encounter | Proposed AI level | Read |
|---|---|---:|---|
| 1 | Wayward Striker | 21 | Mobile close-range attacker. |
| 2 | Wayward Adept | 22 | Simple ranged elemental attacker using a basic shared-pool bolt. |
| 3 | Wayward Striker + Wayward Guard | 21 + 22 | Pressure + defense; introduces target priority. |
| 4 | Wayward Adept + Wayward Guard | 22 + 23 | Ranged pressure behind a sturdier frontliner. |
| 5 | Dojo Renegade | 25 | Solo capstone combining ordinary strikes with one mild stance or light shield. |

**Enemy ceiling:** 2 at a time.  
**AI roster:** 4 records.  
**Mechanical vocabulary:** damage, basic movement/range, one light shield, one mild damage-given/taken modifier, one elemental bolt. No hard CC or counter-check effects.  
**Leader treatment:** GENIN rank, `statsMultiplier: 1`, `poolsMultiplier: 1`; AI Light armor only if needed after testing. The challenge should come from a broader ordinary kit, not inflated numbers.

**Why it exists:** By level 25 the player should be asked to identify a threat role and choose a target, but should still be able to win with any reasonable Genin build.

---

## Difficulty curve

| Feature | Lv15 | Lv20 | Lv25 |
|---|---:|---:|---:|
| Battles | 3 | 4 | 5 |
| Max enemies at once | 1 | 2 | 2 |
| Highest enemy level | 15 | 20 | 25 |
| Human/ninja tactics | None | Basic | Basic ninja |
| Utility pressure | None / minimal | Mild | Mild |
| Hard CC / gimmick checks | None | None | None |
| User scaling | No | No | No |
| Failure | Retry current floor | Retry current floor | Retry current floor |

The progression comes from **depth + composition + role complexity**, not from enemies exceeding the player's intended level.

## Shared-pool direction

Exact kits should be selected during implementation from `32b_DATA_pool.json`, but the allowed beginner vocabulary should stay narrow:

- Basic melee: `S01 Heavy Strike`, `S02 Quick Strike`, `S03 Lunging Strike`.
- Basic ranged: `S06 Twin Shot`, `S07 Rapid Fire`.
- Mild vulnerability/pressure: `S04 Opening Strike` or equivalent 10–15% effect.
- Mild stance: `B37 Fighter's Poise` or `B38 Minor Overflow`.
- Light defense: `B39 Light Barrier`.
- Basic elemental identity at level 25: one of the 45-power elemental bolt entries (`EA01/EE01/EF01/EL01/EW01`).

Do not use the stronger shared-pool boss/control entries merely to make the fights feel distinct.

## Reward / repeat proposal — unresolved

User-owned decision. Recommended shape only:

- Terminal reward only.
- No exclusive jutsu, gear, bloodline, or progression-critical drop.
- Reward value should increase 15 < 20 < 25 and be calibrated as repeatable Genin PvE rather than a one-time windfall.
- **Proposed cadence:** daily repeat, but this is not approved.
- Exact ryo / EXP / prestige / tokens / maxCompletes remain unset until user decision.

## Art / production scope

Minimum new art if no suitable reusable assets are approved:

- Lv15: 3 AI avatars + 1 woodland route scene background.
- Lv20: 3 AI avatars + 1 abandoned tollhouse/road scene.
- Lv25: 4 AI avatars + 1 weathered training-ground scene.

Production can be reduced by sharing visual bases within each family (for example one road-gang clothing language with silhouette/weapon changes), but distinct AI records should remain readable in combat.

## Implementation handoff after approval

Fable should:

1. Point-read any existing candidate AI/assets before deciding to reuse them.
2. Prefer fresh AI records if the live candidate's level/kit is not an exact fit; do not mutate unrelated live enemies for convenience.
3. Use shared-pool codes, not raw jutsu ids, in the design/build source.
4. Build every battle as `dialog -> start_battle -> dialog`; never place consecutive `start_battle` nodes.
5. Route every failed/fled regular floor to a reset that returns to that floor's preceding dialog.
6. Keep all three quests `hidden: true`.
7. Validate the manifest, then require full live read-back after hidden execution before publication is considered.

## User decisions requested

1. Approve/rename the three themes and titles.
2. Approve the 3 / 4 / 5 battle progression and max headcount 1 / 2 / 2.
3. Approve fixed enemy levels (rather than user scaling).
4. Approve `maxLevel: 30`.
5. Decide whether the three pyramids are independent (recommended) or prerequisite-chained.
6. Decide reward amounts and repeat cadence.
