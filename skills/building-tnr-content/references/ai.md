# AI enemies and behaviour

> Migrated from `21_GUIDE_ai_enemy.md` + `24_GUIDE_ai_behavior.md` (Phase 3, 2026-08-26). Part 1 is the enemy spec and stat block; Part 2 is the AiProfile rule vocabulary and range gating.

## Contents

- [Part 1 - Enemy design and stat blocks](#part-1---enemy-design-and-stat-blocks)
  - [0. What this file is for](#0-what-this-file-is-for)
  - [1. AI Enemy Spec, full field schema](#1-ai-enemy-spec-full-field-schema)
  - [2. Blank fill-in template (copy-paste)](#2-blank-fill-in-template-copy-paste)
- [<enemy_name>, <element> <role>](#enemyname-element-role)
  - [Identity](#identity)
  - [Profile](#profile)
  - [Passive AI Tags (omit if None)](#passive-ai-tags-omit-if-none)
  - [Combat Role](#combat-role)
  - [AI Pattern](#ai-pattern)
  - [Jutsu Kit](#jutsu-kit)
  - [Tactical Read](#tactical-read)
  - [Reserved (NOT RECORDED)](#reserved-not-recorded)
  - [3. Machine record](#3-machine-record)
  - [4. Effect & tag vocabulary, full canonical list](#4-effect--tag-vocabulary-full-canonical-list)
  - [5. WORKFLOW A, Author the Spec from a request](#5-workflow-a-author-the-spec-from-a-request)
  - [6. WORKFLOW B, Infographic from the Spec](#6-workflow-b-infographic-from-the-spec)
  - [7. WORKFLOW C, ViolentMonkey batch payload from the Spec](#7-workflow-c-violentmonkey-batch-payload-from-the-spec)
  - [8. Master QA checklist (before delivering any AI enemy)](#8-master-qa-checklist-before-delivering-any-ai-enemy)
  - [Addendum: effect and edit rules (live-verified)](#addendum-effect-and-edit-rules-live-verified)
  - [Rules live on the AI entry (added 2026-07-27)](#rules-live-on-the-ai-entry-added-2026-07-27)
  - [Addendum: harvest Stage 1 facts (2026-08-01)](#addendum-harvest-stage-1-facts-2026-08-01)
- [Part 2 - Behaviour, rules and range gating](#part-2---behaviour-rules-and-range-gating)
  - [1. Contract (verified)](#1-contract-verified)
  - [2. Rule object](#2-rule-object)
  - [3. Conditions (9 total)](#3-conditions-9-total)
  - [4. Actions (10 total)](#4-actions-10-total)
  - [5. Targets (9 total)](#5-targets-9-total)
  - [6. Effect enum (71, used by has_effect / target_has_effect / use_highest_power_*)](#6-effect-enum-71-used-by-haseffect--targethaseffect--usehighestpower)
  - [7. Gotchas](#7-gotchas)
  - [8. Residual unknowns](#8-residual-unknowns)
  - [Addendum (Jul 10 2026, source extraction): vocabulary VERIFIED](#addendum-jul-10-2026-source-extraction-vocabulary-verified)
  - [The confirmed rule vocabulary and the range law (added 2026-07-27)](#the-confirmed-rule-vocabulary-and-the-range-law-added-2026-07-27)
  - [Addendum: ai_v2 source verification + harvest facts (2026-08-01)](#addendum-aiv2-source-verification--harvest-facts-2026-08-01)


---

# Part 1 - Enemy design and stat blocks


Owner doc for AI (PvE) enemy record shape, generation conventions, the verified profile and jutsu tRPC contracts, the effect-object schema, the enemy-infographic layout, and the batch-script payload. For shared plumbing (the builder, capture tool, rate limit, the contract envelope) see `10_TECH_pipeline.md`. For cross-cutting balance philosophy see `30_DOCTRINE_balance.md`; where those conflict with this file on AI-enemy specifics, this file wins. Stat and pool values are balance decisions reserved by dauntless, never invented. Enemy outputs carry no patch or version framing.

---

## 0. What this file is for

One AI enemy = one **Spec** (the MD record below). From a finished Spec you can produce two downstream artifacts without re-deciding anything:

```
                 ┌─────────────────────────────┐
   request  ──▶  │  AI ENEMY SPEC  (MD + JSON)  │  ◀── single source of truth
                 └──────────────┬──────────────┘
                                │
              ┌─────────────────┴─────────────────┐
              ▼                                     ▼
   WORKFLOW B: INFOGRAPHIC                WORKFLOW C: VIOLENTMONKEY BATCH
   (poster like the examples)            (commands that auto-create AI + jutsu)
```

- **Workflow A** fills the Spec from a request.
- **Workflow B** renders the infographic by pulling Spec fields into a fixed layout.
- **Workflow C** emits batch commands for the ViolentMonkey userscript by mapping Spec fields to script actions.

Every field below is tagged **[req]** required, **[opt]** optional, or **[NR-ok]** may be `NOT RECORDED`. Reserved/engine values are never invented.

---

## 1. AI Enemy Spec, full field schema

The Spec mirrors the infographic blocks so Workflow B is a 1:1 pull. Fields are grouped Identity → Profile → Passives → Role → Pattern → Kit → Tactical Read.

**No patch/version framing in enemy outputs.** Don't put "Patch N", patch numbers, or version tags in the enemy MD, identity, or poster. Patch context belongs in commit notes/changelogs, not the enemy itself.

### 1.1 Identity / Header
| Field | Tag | Allowed / format | Notes |
|---|---|---|---|
| `enemy_name` | [req] | string | Big display name (e.g., `War Commander`, `Galewraith`). |
| `title` | [opt] | string | Epithet (e.g., `the Tempest Coil`). |
| `event_theme` | [req] | string | Left half of subtitle line (e.g., `WARPATH`, `MOZZARELLA`). The collection/event tag. |
| `role` | [req] | `Standard PvE Enemy` \| `Elite PvE Enemy` \| `Boss PvE Enemy` | Drives default pools/scaling/passives (see 1.8). |
| `tagline` | [req] | 1-2 sentences, italic | Flavor + role hint. |

### 1.2 Profile / Stat block
| Field | Tag | Allowed / default | Notes |
|---|---|---|---|
| `rank` | [req] | Student / Genin / Chunin / Jonin / … | Examples: `Jonin`. |
| `level` | [req for boss/elite, NR-ok for standard] | int | Boss example `100`. Standard often omits → set per content or `NR`. |
| `hp` / `cp` / `sp` | [req] | int | **Base** pools before multiplier. Defaults: Standard `4050` each; Boss `10100` each. |
| `pool_multiplier` | [req] | number, default `1` | Multiplies all three pools. Boss example `2`. |
| `stat_multiplier` | [req] | number, default `1` | Multiplies effective stats. Boss example `3`. Standard `1`. |
| `regeneration` | [req] | int, default `60` | Per-round regen. |
| `preferred_stat` | [req] | Ninjutsu / Bukijutsu / Genjutsu / Taijutsu | Casting/scaling stat. |
| `preferred_generals` | [req] | two of: Strength, Speed, Intelligence, Willpower | a.k.a. "Stat Focus". |
| `element` | [req] | 21 canon: Fire / Water / Wind / Earth / Lightning / Ice / Crystal / Dust / Shadow / Wood / Scorch / Storm / Magnet / Yin-Yang / Lava / Explosion / Light / Boil / Metal / Sand / None | Use `None`, never `Normal`. Source-confirmed enum, `45_DATA_field_schemas.json`. |
| `equipped_armor` | [req] | None / AI Light / AI Medium / AI Heavy | Mitigation tier. Boss `AI Heavy`; Galewraith `AI Light`. Exact DR% is `NR`. |
| `ai_tags_summary` | [req] | `None` \| short string (e.g., `2 Passive Steroids`) | Detailed list in 1.3. |
| `stat_cap_note` | [const] | `Effective stats are capped at 450,000` | Constant; display in profile. |

**HARD WARNING [REWRITTEN 2026-08-26, source-verified against `app/src/libs/profile.ts`]: the DB default is rank STUDENT with every stat 10.** An AI created without the required block above is a level-100 paper doll: near-zero defense (players hit for 15k+), tag-only offense.

**Stats are RATIOS, not numbers.** `scaleUserStats` runs on every `profile.updateAi` and keys off **level**, never rank. It computes `exp = calcLevelRequirements(level) - 500`, sums the twelve stat fields you sent, and rewrites each as `10 + (stat / sum) * exp`, then multiplies by `statsMultiplier`. So the twelve numbers in a payload are weights describing the SHAPE of the enemy; the total is fixed by level and cannot be argued with. Writing 62,000 into `taijutsuOffence` on a level 45 record produces 92,326, because level 45 has a budget of 517,000 to spend. A second edit re-runs the same normalisation, so **there is no two-phase trick to pin exact stats.**

**Pools are overwritten, so do not send them.** `maxHealth`/`curHealth`/`maxChakra`/`curChakra`/`maxStamina`/`curStamina` are all replaced with `(100 + 50*(level-1)) * poolsMultiplier`. To hit a target HP, set the multiplier: `poolsMultiplier = target / (100 + 50*(level-1))`. Range 1 to 50.

**Rank is the combat-time cap, not the budget.** `USER_CAPS` clamps stats during battle: STUDENT 20,000, GENIN 60,000, CHUNIN and above 450,000. An AI written at GENIN with level-60 stats passes validation and is silently gutted in the fight. Use CHUNIN or higher for anything above level 30.

Practical method: pick the level for the tier, write the twelve stats as a ratio expressing the role (glass cannon, wall, skirmisher), set `poolsMultiplier` for the HP anchor, and accept the offence numbers that fall out. Verify against a live `getAi` after the push, never against the payload you sent.

**Equip-array ref law:** unresolvable `@jutsu:`/`@item:` refs in AI `jutsus`/`items` arrays are silently STRIPPED server-side; the entry reports ok and the AI stands naked. Manifests must be fully ref-substituted with literal ids, or run in the same builder session as their creates.

**Damage tuning:** AI-side tags stack as multiplicative row products (12_TECH laws 9 and 13); build tier targets as products, and use one shared team item (the Court Regalia pattern: a hidden AI-only armor piece worn roster-wide) as the global damage/mitigation re-anchor lever.

**Kits:** all new AI kits come from 32_REGISTRY_shared_ai_pool.md (pool picks + rules order + tags + at most a few boss signatures). Per-event jutsu minting is retired.

Server write caps (insertAiSchema, source-confirmed): `level` 1 to 200, `statsMultiplier` and `poolsMultiplier` 1 to 50, `regeneration` 1 to 100, every offence/defence stat and general minimum 10. `profile.updateAi` coerces empty strings to null server-side. The full write schema is machine-readable in `45_DATA_field_schemas.json`.

### 1.3 Passive AI Tags (0-N; bosses/elites)
Time-limited "steroids", **start strong, then fall off** as their duration expires. Each:
| Field | Tag | Format |
|---|---|---|
| `tag_name` | [req] | e.g., `Increased Damage Given (Bukijutsu)`, `Increased Damage Given (None Element)` |
| `magnitude` | [req] | e.g., `35% Damage Given` |
| `duration_rounds` | [req] | int (examples: `5`, `3`) |

Standard enemies normally have **none** (`ai_tags_summary: None`).

### 1.4 Combat Role
| Field | Tag | Format |
|---|---|---|
| `combat_role` | [req] | 1 short paragraph, designer-facing, what the enemy *does* in a fight. |

### 1.5 AI Pattern (behavior)
`ai_pattern` [req] = an **ordered, numbered list** (5-7 steps). This is the established infographic format: a priority list with light range conditionals + a fallback. Drives both the infographic "AI Pattern" panel and the script's pattern field.

**This is the display and design-intent format only.** The actual scriptable AI behavior is a verified `rules[]` array on a separate AiProfile row, pushed via `ai.updateAiProfile`. Author the `ai_pattern` here for the infographic and the intent, then translate it into `rules[]` per `24_GUIDE_ai_behavior.md` when building. A new AI does not use its `ai_pattern` automatically; behavior must be pushed as its own step (see 7.1 and guide 24).

**Allowed step shapes:**
- `Open / Round 1: use <self-buff/setup>`
- `If far away: use <global-range or ranged opener>`
- `Move toward opponent to close gap` *(generic move action, allowed)*
- `When in range / At range 5: use <primary single-target>`
- `Follow with <secondary / finisher>`
- `Refresh <buff> when needed`
- `Fallback: use highest power action`

**Conventions:**
- The list is order + the jutsu's own cooldown. Cooldowns pace recurrence; long cooldowns = rare big hits, short = filler.
- **No movement *jutsu*** (no `MV`-tag self-reposition jutsu in the kit). The generic "move toward opponent" basic action is fine.
- Keep conditionals light: range checks + one "refresh" + the fallback. **Limit HP-threshold conditionals (e.g., `<50% HP`) to at most one or two jutsu** total.
- **Conditionals never override a jutsu's cooldown.** A trigger changes *when/whether* a ready jutsu is chosen, not whether it can fire off cooldown.
- **Valid triggers include target state**, not just HP, e.g. "use the pierce jutsu when the target has a **shield**" (shield/DR denial), or "use *freely* below 50% HP" (drop the usual gating and fire it whenever it's off cooldown). Pierce attacks make natural shield/DR-denial tools and read as *sustained* pressure, not one-shot finishers, when their cooldown is short.

### 1.6 Jutsu Kit (AI jutsu sub-schema)
`jutsu_kit` [req] = ordered list. Each jutsu:
| Field | Tag | Allowed / format | Notes |
|---|---|---|---|
| `name` | [req] | string | |
| `ap` | [req] | `40%` \| `60%` | **Only 40 or 60.** |
| `function_label` | [req] | `Self Buff` \| `Self Defense` \| `In-Range Setup` \| `Single Target • Range N` \| `All Targeting • Global Range` | Display descriptor under the name. |
| `target` | [req] | self \| enemy \| all | |
| `range` | [req] | `0` (self) \| int (single; examples use `5`) \| `global` | |
| `method` | [req] | single \| all \| aoe_circle_spawn \| … | Engine targeting method. |
| `cooldown` | [req] | int rounds | Paces recurrence. |
| `chakra_cost` / `stamina_cost` | [req] | int | AI default low (~`5`) so the AI never resource-starves; tunable. |
| `damage` | [60% only; `-` on 40%] | int | Set by **attack weight × level/rank**, see the AI damage tiers in 1.6.1. (Distinct from AP: AP is the action cost; weight is the damage magnitude.) |
| `pierce` | [opt] | bool | Piercing damage ignores Damage Reduction. |
| `element` | [req if damage] | enemy's element by default | Shown in the damage strip. |
| `tags` | [req] | canon tag codes (see 4) | Damage counts as a tag; max 3, 2 preferred. |
| `effects` | [req] | 1-3 strings, canon vocab | **Do not restate the damage number here**, it lives in `damage` / the damage strip. |
| `conditional` | [opt] | string | Only for the ≤1-2 allowed HP/state conditionals. |
| `icon_asset` | [NR-ok] | asset ref | Image file; usually `NR` until art exists. |

**AP convention (holds across all examples):** `40% AP` = setup/utility, **no damage**; `60% AP` = a damage action. Keep it. AP (the action cost, 40/60) and **attack weight** (the damage magnitude, below) are independent, a 60% AP jutsu can be a light, normal, or heavy hit.

### 1.6.1 Damage tuning
Superseded: kits come from 32_REGISTRY (EP doctrine); per-hit tuning is multiplicative row products against a declared anchor (30_DOCTRINE protocol, 12_TECH laws 9/13).

### 1.7 Tactical Read, counters & footer
| Field | Tag | Format |
|---|---|---|
| `tactical_read` | [req] | 1 short paragraph, **player-facing**, how to beat it (cleanse, survive stun, pressure before steroids fade, element counter). |
| `counters` | [poster] | 3-5 short bullets for the poster's COUNTERS box (e.g. "Cleanse / Debuff Removal", "Burst Damage", "Damage Reduction before the spike", "Punish cooldown windows"). |
| `footer_tags` | [poster] | 2-4 spaced caps for the footer strip, usually the signature mechanics (e.g. `WIND / PIERCE / AFTERBURN`). |

### 1.8 Role defaults (quick reference)
| | Standard | Elite | Boss |
|---|---|---|---|
| Base HP/CP/SP | 4050 | 4050-10100 | 10100 |
| `pool_multiplier` | 1 | 1-2 | 2 |
| `stat_multiplier` | 1 | 1-2 | 3 |
| Passive AI tags | None | 0-1 | 1-2 |
| Armor | None / Light | Light / Medium | Heavy |
| Level shown | optional | optional | yes |
| Kit size | 5 | 5-6 | 6 |

### 1.9 Reserved / `NOT RECORDED` registry
Never invent these, leave `NR` for you/the engine:
`exact base stat numbers if not provided` · `exact armor DR%` · `loot table / drop rates` · `encounter gating (required rank/level to fight)` · `spawn context` · `art/icon image files` · `element-wheel counter relationship` · `ViolentMonkey record IDs / form selectors / endpoint`.

---

## 2. Blank fill-in template (copy-paste)

```
# <enemy_name>, <element> <role>

## Identity
Name:            <enemy_name>
Title:           <title | -->
Event/Theme:     <event_theme>
Role:            <Standard | Elite | Boss> PvE Enemy
Tagline:         <1-2 sentences>

## Profile
Rank:            <rank>
Level:           <int | NR>
HP / CP / SP:    <hp> / <cp> / <sp>      (base, pre-multiplier)
Pool Multiplier: <x1 | x2 | …>
Stat Multiplier: <x1 | x3 | …>
Regeneration:    60
Preferred Stat:  <Ninjutsu | Bukijutsu | Genjutsu | Taijutsu>
Generals:        <General A> / <General B>
Element:         <None | Wind | …>
Armor:           <None | AI Light | AI Medium | AI Heavy>
AI Tags:         <None | "N Passive Steroids">
Stat Cap:        Effective stats are capped at 450,000

## Passive AI Tags (omit if None)
- <tag_name>, <magnitude>, <duration_rounds> rounds
- <tag_name>, <magnitude>, <duration_rounds> rounds

## Combat Role
<one short paragraph>

## AI Pattern
1. <Open: use ...>
2. <If far away: use ...>
3. <Move toward opponent>            (optional)
4. <When in range: use ...>
5. <Follow with ...>
6. <Refresh ... when needed>
7. Fallback: use highest power action

## Jutsu Kit
### <jutsu name>, <AP%> • <function_label>
- Damage:   <int | -->  <element, if damage>   <pierce?>
- Cooldown: <int>   |  CK/SP: <int>/<int>
- Tags:     <...>
- Effects:  <bullet 1>; <bullet 2>; <bullet 3>
- Conditional: <only if used>
[repeat per jutsu]

## Tactical Read
<one short player-facing paragraph>

## Reserved (NOT RECORDED)
Base stats: <NR> | Armor DR: <NR> | Loot: <NR> | Gating: <NR> | Art: <NR> | Element counter: <NR>
```

---

## 3. Machine record
Retired: the puller/emitter intermediate format is superseded by the builder's combined manifest (10_TECH 1.5). Author specs (Workflow A), then emit builder manifest entries directly.

## 4. Effect & tag vocabulary, full canonical list

Compiled from the source stack (tag/mechanics registries, schema value-aliases, the alias registry, and effect text across the jutsu DB). Every jutsu effect must resolve to a tag here. **Damage is a tag** and only appears on 60% AP jutsu. **Max 3 tags per jutsu, 2 preferred.** Use the canonical name; the code is the compressed alias.

### 4.1 AI restrictions (read first)
- **AI enemies must NOT use `Lifesteal` (LS) or `Vamp` (VMP).** For AI sustain, use `Heal` or `Absorb` instead (e.g., War Commander's `40% Absorb`).
- **No `Movement` (MV) self-reposition jutsu on AI** (the generic "move to close" basic action is fine; `Movement Prevent` *on the target* is allowed).
- **`Trigger` is experimental**, not live canon; never use it.

### 4.2 Offense / damage
| Canonical | Code | Effect | AI note |
|---|---|---|---|
| Damage | `DMG` | Direct damage (60 AP only; counts as a tag) | core |
| Pierce | `PRC` | Piercing damage; ignores Damage Reduction (own higher scaling, §1.6.1) | yes |
| Increased Damage Given | `IDG` | `+X% Damage Given` (stat- or element-scoped); *stacks* | yes |
| Increased Damage Taken | `IDT` | `+X% Increased Damage Taken` on target; *stacks* | yes |
| Decreased Damage Given | `DDG` | `-X% Damage Given` on target | yes |
| Wound | `WND` | DoT based on damage dealt (new content ≤30%; one per kit) | yes |
| Afterburn (Taken) | `Afterburn` | DoT, % of incoming damage applied over time; *stacks* | yes |
| Recoil | `RCL` | Self-damage on use | rare |
| Reflect | `Reflect` | Reflect % of damage back to attacker | situational |
| Drain / Pool Drain | `Drain` | Static drain of target Chakra/Stamina/Health pools (e.g., `200 pool drain`) | yes |

### 4.3 Defense / sustain
| Canonical | Code | Effect | AI note |
|---|---|---|---|
| Damage Reduction / Decreased Damage Taken | `DR` / `DDT` | `-X% Damage Taken` (self), **same tag** (also surfaced as "Mitigation"). Scopes by `statTypes` (offense schools) OR `elements` (all six incl `"None"`); the two are separate buckets that stack (see 7.4). Pierce ignores mitigation. | yes |
| Heal | `HEAL` | Flat/percentage healing | **use this for AI sustain** |
| Absorb | `ABS` | Convert incoming damage → health/chakra/stamina | **use this for AI sustain** |
| Shield | `SHD` | Temporary HP / shield pool (Temporary HP scores as Shield). Effect carries a `health` field (the pool size), `calculation:"static"` (see 7.4). **Pierce destroys shields instantly.** | yes |
| Lifesteal | `LS` | Heal from damage **dealt** | **FORBIDDEN for AI** |
| Vamp | `VMP` | Source-defined vampiric healing | **FORBIDDEN for AI** |

### 4.4 Control / disruption
| Canonical | Code | Effect | Rule |
|---|---|---|---|
| Stun | `STN` | Target loses AP next turn | −40 AP next turn |
| Movement Prevent | `Movement Prevent` | Prevents target movement for N rounds | target-only (ok for AI) |
| Movement | `MV` | Self-move on battlefield | **not for AI** |
| Poison | `PSN` | DoT | 3-round global cooldown |
| Increased Action Cost | `Increased Cost` | Raises target Chakra/Stamina action costs (**not AP**) | 3-round global cooldown |
| Heal Cut / Reduce Heal | `Heal Cut` | Reduces healing by % (distinct from Prevent Healing) |, |
| Prevent Healing | `Prevent Healing` | Fully prevents healing effects from activating | canon |
| Cleanse | `CLN` | Instantly removes queued negative effects | instant |
| Clear | `CLR` | Removes positive effects from target | instant |
| Prevent Cleansing | `Prevent Cleansing` | Stops the target from cleansing |, |
| Stun Prevent | `Stun Prevent` | Target cannot be stunned ("Prevents being stunned") |, |
| Buff Prevent | `Buff Prevent` | Prevents target from gaining buffs |, |
| Debuff Prevent | `Debuff Prevent` | Prevents target from receiving debuffs |, |
| Bloodline Seal | `Bloodline Seal` | Seals the target's base bloodline effect |, |
| Pull / Push | `Pull` / `Push` | Move target N tiles toward/away (`Direction: pull`/`push`) | situational |

### 4.5 Buff / utility / meta
| Canonical | Code | Effect | Note |
|---|---|---|---|
| Combat-stat buff | (rides on `IDG`/buff jutsu) | `+X% Combat Stats (Gen A, Gen B)` | the "+X% combat stats" line in self-buffs |
| Increased Healing Given | `Increased Healing Given` | Raises how much the target can heal | rare |
| Copy Positive Effects | `Copy Positive Effects` | Copies the target's buffs onto the user | situational |
| Barrier / Temporary HP | `SHD` | Temporary HP bar / barrier, **scores as Shield** | yes |
| Battlefield visual | (cosmetic) | Visual-only effect; no mechanical value | flavor |
| AoE | `AOE` | Area targeting | a targeting **method**, not a standalone effect |
| Trigger | `Trigger` | Experimental pending-effect system | **experimental, do not use** |

### 4.6 Special rules
- **Damage** requires 60 AP for new design and counts toward the 3-tag limit.
- **Poison** and **Increased Action Cost** each carry a **3-round global cooldown**; Increased Action Cost affects chakra/stamina, never AP.
- **Stun** = −40 AP on the target's next turn.
- Don't conflate **Vamp / Absorb / Lifesteal**, they are mechanically distinct.
- **Stacking:** `IDG`, `IDT`, `Afterburn`, and `WND` stack across re-applications, keep per-cast magnitudes modest if re-applied on a short cycle.

> Provenance: this set is reconstructed from the active source stack. If your full effect-type dump (from the prior failed call) lists engine effects beyond these, e.g., Flee / Flee Prevent, Stun Prevent, Summon, Steal/Rob, element Weakness, paste it and I'll fold the extras in and map them to the §7.4 effect-object schema.

---

## 5. WORKFLOW A, Author the Spec from a request

1. **Read the stack first** (`00_INDEX.md`, `10_TECH_pipeline.md`, `30_DOCTRINE_balance.md`, and this guide) for canon effect vocab and constraints.
2. **Pick `role`** → apply 1.8 defaults (pools, multipliers, passives, armor, level, kit size).
3. **Fill Identity** (name, title, event_theme, tagline) and **Combat Role** + **Tactical Read** (player-facing).
4. **Fill Profile** (rank, level, base pools, multipliers, regen 60, preferred stat, generals, element, armor, stat cap 450k, AI-tags summary).
5. **Define Passive AI Tags** if elite/boss (name, magnitude, duration; remember they fall off).
6. **Build the Jutsu Kit:** AP 40/60 convention (40 = setup no damage, 60 = damage); canon effect vocab (§4); **set each damage number by attack weight (light/normal/heavy) on the level/rank curve in 1.6.1**; assign cooldowns (short = filler, long = the big hit); low CK/SP; ≤3 tags each; one Wound jutsu max; **no MV-tag movement jutsu; no Lifesteal/Vamp, use Heal or Absorb for AI sustain**.
7. **Write the AI Pattern:** numbered priority, open buff/setup → ranged if far → (move to close) → in-range primary → follow/finisher → refresh buff → fallback highest power. Keep conditionals light; ≤1-2 HP-threshold conditionals.
8. **Mark reserved fields `NR`** (1.9).
9. **Emit both forms:** the human field dump (§2 filled) and the consolidated JSON (§3).
10. **QA** against §8.

---

## 6. WORKFLOW B, Infographic from the Spec

The poster is a fixed layout; every text element is a direct pull from the Spec. Build the design in the background, skip brainstorming, output the final layout + the character-art prompt + all text.

### 6.1 Layout contract (clean "ENEMY SHOWCASE" boss-guide format)
A premium player-facing boss guide, **not** a database sheet. Art dominates; few panels; big text; short copy.
```
TOP HEADER (dominates top):  kicker "ENEMY SHOWCASE" · <enemy_name> (huge) · "<event_theme/title>"
                             · subtitle row "<role> • <element> Elemental" · <tagline>
ENEMY ART:                   huge central/left-dominant illustration, the strongest anchor,
                             larger & more dramatic than any panel ← character art
PROFILE panel:               compact, 7 rows max ← profile subset (see 6.2)
COMBAT ROLE panel:           short ← combat_role
AI PATTERN panel:            numbered list + fallback line ← ai_pattern
JUTSU KIT panel:             a clean stacked ROW-LIST (not dense cards) ← jutsu_kit
                             (each row: circular icon · name · "<AP> • <function> • Range N" · 2 effect bullets · AP badge)
TACTICAL READ panel:         short ← tactical_read
COUNTERS box:                short bullets ← counters
FOOTER BANNER:               centered, accent glow ← footer_tags
```
Make the pierce/finisher jutsu row visually stand out as the danger spike.

### 6.2 Section → field map
| Poster element | Spec field |
|---|---|
| Kicker / title / sub-title / subtitle row / tagline | const `ENEMY SHOWCASE` / `enemy_name` / `event_theme` / `role`+`element` / `tagline` |
| Profile rows (**only**: Role, Level, Rank, Element, Armor, Pools, Preferred Stat) | `role`, `profile.level`, `profile.rank`, `profile.element`, `profile.armor`, `profile.pool_multiplier`, `profile.preferred_stat` |
| Combat Role | `combat_role` |
| AI Pattern steps (+ fallback) | `ai_pattern[]` |
| Jutsu rows (name, "AP • function • Range", 2 bullets, AP badge) | `jutsu_kit[].name`, `.ap`+`.function_label`+`.range`, `.effects` (max 2), `.ap` |
| Jutsu damage (shown once in the row) | `jutsu_kit[].damage` + `.element` |
| Tactical Read | `tactical_read` |
| Counters bullets | `counters[]` |
| Footer | `footer_tags` |

**Excluded from the poster** (kept in the MD/Spec, never drawn): stat multiplier, regeneration, generals, stat cap, status/candidate, **patch/version framing**, HP/CP/SP rows, and any backend/schema/payload/engine language.

### 6.3 Style rules (TNR established)
- **Premium boss-guide poster, not a database sheet.** Readable at a glance: huge art, strong title hierarchy, big text, short copy, **few panels**. Bias every choice toward clarity over completeness.
- **Illustrated dark-fantasy poster** look (rough-brush/serif title, ornate panels with filigree corners, smoky battlefield backdrop, one full illustrated character). Showcase lane, *not* the in-game pixel-sprite lane.
- **Art is the anchor**, larger and more dramatic than the panels; central or left-dominant.
- **Jutsu kit = a clean stacked row-list** (War Commander style), **not five dense cards**, and **no per-jutsu "visual cue" text**.
- **Damage shown once** per jutsu row (with the element icon); never duplicate the damage number in the effect bullets. Max 2 effect bullets per jutsu row.
- **Profile is compact**, only the 7 rows in 6.2. No backend/dev/schema/payload language anywhere on the poster.
- Use `Element: None` (never "Normal"). Use the approved 19-element sprite sheet for element icons; Magnet uses the locked horseshoe icon.
- **No Naruto-specific gear or marks** (forehead protectors, copied village symbols, Akatsuki cloaks, Sharingan eyes, Naruto uniforms). Preserve the TNR feel without protected marks.
- **No effect-icon legend strip**, no tiny unreadable microtext, no text baked into the character illustration.
- Editing existing art = targeted edits only; preserve approved character identity, don't full-remake unless asked.

### 6.4 Character-art prompt template (for the external image model)
```
A <theme/role> <character archetype> for a dark-fantasy ninja RPG, full body, dramatic battlefield
backdrop (smoke, embers, war banners), cinematic rim lighting, high detail, painterly-illustrative
(not pixel art, not photoreal). Color mood: <event_theme palette, e.g., crimson/black/gold>.
Wardrobe: original ninja-fantasy gear, NO forehead protector, NO village symbols, NO Akatsuki cloak,
NO Sharingan eyes, NO Naruto uniform. Pose conveys <role verb: command / pin / control / strike>.
Vertical poster orientation, character left-weighted to leave panel space on the right.
```

### 6.4b Full poster master prompt (the default Workflow B output)
Compile the Spec into this template every time. Every `<…>` is a direct Spec pull; the `counters` / `footer_tags` fields (1.7) exist to fill it. Pick the palette from 6.4c by element. Goal: a **premium boss-guide poster, not a database sheet**.

```
A single vertical dark-fantasy video-game "ENEMY SHOWCASE" boss-guide poster, 2:3 portrait, high
resolution. A premium player-facing boss guide, NOT a database/stat sheet. Cinematic painterly
illustration + ornate game-UI overlay. Readable at a glance: big art, big text, short copy, few panels.
Render ALL text exactly. No real-world logos, no Naruto forehead protectors, no village symbols.

STYLE: ornate brushed-<frame-metal> / dark-metal art-deco outer frame, filigree corners, thin <accent>
glow. <ELEMENT> palette: <palette line from 6.4c>. Painterly cinematic, NOT pixel art, NOT photoreal,
NOT flat anime cel. Huge rough-brush/serif title font; clean readable sans for body; no tiny database text.

ENEMY ART (the dominant visual anchor, larger and more dramatic than any panel; central or left-weighted):
<enemy_name>, <character_archetype + element-creature description: form, face, eyes, motion>, razor/
elemental arcs spiraling around it, debris and faint embers caught in the vortex, dark storm-wracked
battlefield horizon below.

TOP HEADER (dominates the top): kicker "ENEMY SHOWCASE"; huge title "<ENEMY_NAME>"; sub-title
"<TITLE / event_theme>"; small subtitle row "<role> • <element> Elemental"; short tagline "<tagline>".

PROFILE panel (compact icon bullets, ONLY these rows): Role / Level / Rank / Element / Armor / Pools /
Preferred Stat = <values>. Do NOT show stat multiplier, regeneration, generals, stat cap, status, HP/CP/SP,
or any backend/engine note.

COMBAT ROLE panel (short): "<combat_role>".

AI PATTERN panel (numbered, circular markers, clean spacing): <ai_pattern[] as short lines>, ending
"Fallback: highest-power action."

JUTSU KIT panel (a clean stacked ROW-LIST like a War Captain / War Commander sheet, NOT dense cards, and
NO per-jutsu visual-cue text): one row per jutsu, each with a small circular <element> icon, the name, a
"<AP> • <function> • Range <N>" line, two concise effect bullets, and an AP badge on the right:
<for each jutsu: NAME · ap · function · range · two effect bullets (show damage once, do not restate it)>
Make the pierce/finisher row visually stand out as the danger spike.

TACTICAL READ panel (short): "<tactical_read>".

COUNTERS box (short bullets): <counters[]>.

FOOTER BANNER (centered, <accent> glow + silver trim + element-sigil ornament): <footer_tags>.
```
Keep copy short and the panel count low, when in doubt, cut text and enlarge the art.

### 6.4c Element → palette table (swap by `profile.element`)
| Element | Palette line | Frame metal / accent |
|---|---|---|
| Wind | deep slate-black & teal, cyan/aqua glow, silver-white highlights, cool storm light | silver / cyan |
| Fire | crimson, gold, charred black, ember-orange glow, hot rim light | gold / orange |
| Water | deep blue, aqua, foam-white, cool caustic glow | steel-blue / aqua |
| Earth | umber, sandstone, mossy green, dim warm light | bronze / amber |
| Lightning | indigo-black, electric violet, white-blue arcs, high contrast | chrome / violet |
| Ice | pale cyan, white, glacial blue, frosted glow | platinum / ice-blue |
| Lava | molten orange-red, obsidian black, glowing magma cracks | dark iron / magma |
| Shadow / Dark | near-black, deep purple, cold grey mist, low key | gunmetal / violet |
| Light / Divine | ivory, gold, soft white bloom, radiant backlight | gold / white |
| None (non-elemental) | neutral steel-grey, muted gold, black, restrained light | steel / gold |


1. Lock the Spec (all text final).
2. Generate character art (6.4) → draft → post-process/compress if delivered as a transparent asset.
3. Assemble the poster (HTML poster template or layout tool) pulling §6.2 fields; apply §6.3 style.
4. Export PNG. (If using `wkhtmltoimage`: avoid CSS grid / clip-path / gradient-text / Google Fonts, they don't render there; use an HTML artifact in a modern browser for those, or fall back to supported CSS.)
5. QA against §6.6, open the exported file (not just the source).

### 6.6 Infographic QA
Title legible · all profile rows present · passives shown only if they exist · AI Pattern numbered & readable · every jutsu has name + descriptor + AP badge · damage shown once with element icon · no Naruto marks · no legend strip · no baked-in text on the art · reads clearly at final size.

---

## 7. WORKFLOW C, ViolentMonkey batch payload from the Spec

**Three userscripts** cover the build. Pick by what already exists; all write to the **live DB**.

| Script | Page | Input | Does |
|---|---|---|---|
| `TNR batch enemy v1.0` | `/manual/ai` | `{ ai, jutsus }` | creates each jutsu, creates the AI, equips. Aborts *before* the AI if a jutsu fails. |
| `TNR batch jutsu v1.0` | `/manual/jutsu` | `{ jutsus: [...] }` (or bare array) | creates jutsu **only**; continues past failures; lists every id. |
| `TNR AI maker v1.1` | `/manual/ai` | **flat** AI object | creates an AI **only** (or fills an existing one), and **equips existing jutsu** by id, no jutsu creation. |

- The two jutsu-creating scripts share the **same jutsu shape**: per jutsu POST a blank `jutsu.create`, grab the id, then `jutsu.update` with your fields merged over `DEFAULTS`.
- **Use the AI maker when the jutsu already exist** (e.g. a prior run created them, or you made them with the batch-jutsu script). It avoids duplicate jutsu. See 7.6.

### 7.1-7.3 Legacy batch script
Retired: the standalone batch-enemy script is superseded by the builder (10_TECH). AI entries ride the combined manifest with slot create/edit, explicit targetId, and full 1.2-table payloads.

### 7.4 Effect objects
Composed exclusively from 40x_EXEMPLARS_effects.json (proven update-strict shapes) with 46_DATA_tag_schemas.json as the field authority - see 12_TECH laws 2-4. This guide no longer duplicates the schema.


### 7.5 Safety
Writes are live and irreversible by the script. If a staging/test account exists, build there first. Keep the failure behavior (7.1) in mind: a mid-run abort leaves orphan jutsu to clean up. Never emit an unconfirmed field/enum as if verified.

### 7.6 (retired with 7.1-7.3)

## 8. Master QA checklist (before delivering any AI enemy)
- [ ] Identity complete (name, event_theme, role, tagline).
- [ ] Profile complete; `regeneration=60`; stat cap noted; multipliers set per role.
- [ ] Passive AI tags present iff elite/boss; each has magnitude + duration.
- [ ] Combat Role (designer) and Tactical Read (player) both written.
- [ ] AI Pattern numbered; conditionals light; ≤1-2 HP-threshold conditionals; no MV-tag movement jutsu.
- [ ] Jutsu kit: AP 40/60; damage only on 60 AP; damage numbers set by attack weight × level/rank (1.6.1); ≤3 tags each; one Wound max; cooldowns assigned; low CK/SP.
- [ ] Effect vocab uses canon tag names (§4); **no Lifesteal/Vamp on AI** (use Heal/Absorb); no `Trigger`; damage not duplicated in effect bullets.
- [ ] Reserved fields marked `NR` (base stats, armor DR, loot, gating, art, element counter).
- [ ] Both outputs emitted: human field dump + consolidated JSON.
- [ ] Infographic (if requested): layout contract followed, style rules met, damage shown once, no Naruto marks, no legend strip.
- [ ] Batch payload (if requested): `{ ai, jutsus }` (or flat AI for the AI maker) with script keys (`username`, `poolsMultiplier`, `statsMultiplier`, `actionCostPerc`, `jutsuType:"AI"`, UPPERCASE enums); **every jutsu has `description` + `battleDescription`**; **AI block has `gender`, `regeneration`, `preferredStat`, generals, `primaryElement`/`secondaryElement`, and all 12 stat numbers**; effect objects use the verified lean shape (§7.4); live-DB safety noted.
- [ ] Reusing existing jutsu → use the **AI maker** (`jutsus: [ids]`), not the batch enemy script (which re-creates jutsu).

---

## Addendum: effect and edit rules (live-verified)

- **Direction is per-tag literal**: `"defence"` is accepted ONLY by absorb, barrier, increasepoolcost, decreasepoolcost; every other tag (including decreasedamagetaken) requires `"offence"`. Mixed setups split accordingly.
- **Barrier is a battlefield structure, not a self-buff**: target EMPTY_GROUND, requires a non-empty `staticAssetPath`, `calculation: "static"`, and real `curHealth`/`maxHealth`/`absorbPercentage`. For a worn "armor" concept use absorb + decreasedamagetaken.
- **AI edit rule**: see 10 addendum; `jutsus` (strings) + `items` (ids-with-number) explicit on every edit.

---

## Rules live on the AI entry (added 2026-07-27)

Behavior rule sets are a field on the AI record, not a separate entity: the builder pushes the AI, toggles the profile, and updates it. An audit that counts `aiProfile` entries in a manifest and finds zero has found nothing. Author rules per the vocabulary and range laws in `24_GUIDE_ai_behavior.md` (laws 39 to 41), and remember that `data.name` must be set on the create itself (law 36).

## Addendum: harvest Stage 1 facts (2026-08-01)

- **H10. AI weakness to a specific item** is a passive entry in the AI's own `effects` array: `type: "weakness"`, `calculation: "static"`, `power: 100`, `items: ["<itemId>"]`. Runtime (R20): weakness matches by ANY of jutsu id / item id / element / statType / generalType overlap; the multiplier is the `dmgModifier` FIELD (power is only the application roll); only the single highest-power matching weakness applies - weaknesses NEVER stack; applies to pierce too.
- **H11. `profile.updateAi` payload facts:** all 12 stat numbers are required; stat cap 450,000; `gender` accepts `"Unknown"`; **armor is editor-only, NOT a payload field** (do not attempt to write armor DR via the API).
- **Stun no-stack (R41):** the engine takes the MAX `apReduction` across all live stuns on a target (ground stuns included) - two stuns on one target is one wasted record. One stun source per target lane; lint L31 warns.

---

# Part 2 - Behaviour, rules and range gating


How a PvE AI decides which jutsu/item/action to use each turn. This is the verified `ai.getAiProfile` / `ai.updateAiProfile` contract plus the full condition / action / target / effect vocabulary. Extends `21_GUIDE_ai_enemy.md` (which owns the AI record itself) and `10_TECH_pipeline.md` (shared envelope). All endpoint and id facts below were confirmed by 200-OK saves; the full enums were harvested live from the editor, and every condition and action field shape has now been round-tripped through a real save. The rule schema has also been verified against the TNR source validators; the machine-readable version is `45c_DATA_constructors.json` (generated; supersedes the prose below for shape questions).

> **[2026-08-26] DO NOT HAND-AUTHOR A RULE OBJECT.** Build every condition and action from
> `45c_DATA_constructors.json` (`ZodAllAiConditions`, `ZodAllAiActions`), which is generated straight from
> `app/src/validators/ai.ts` and carries every field, its `prefault` default, and its resolved enum.
> The correct shape was already documented in section 2 below AND in file 45, and a rule set was still
> authored from memory as a flat `{action, condition, conditionValue, target}` triple and rejected live with
> `path: ["rules", 0, "conditions"], expected: "array"`. Prose describing a shape does not prevent this.
> A constructor does.

This supersedes the old `ai_pattern` note in `21_GUIDE` 1.5: the pattern is real and scriptable, but it is this `rules[]` array, not a single field.

---

## 1. Contract (verified)

The AiProfile is a separate row from the AI user record, joined by id.

| Op | Method | Shape |
|---|---|---|
| `profile.getAi` | GET | input `{userId}` -> full AI record; the link field is **`aiProfileId`**. |
| `ai.toggleAiProfile` | POST | body `{"0":{json:{aiId: <userId>}}}`, no meta. Gives the AI its **own** AiProfile row and returns "AiProfile updated". Call this only when `aiProfileId` is null. |
| `ai.getAiProfile` | GET | input `{id: <aiProfileId>}` -> `{id, userId, rules[], includeDefaultRules}`. |
| `ai.updateAiProfile` | POST | body `{"0":{json:{id, rules, includeDefaultRules}}}`, **no meta wrapper, no dates** (like `profile.updateAi`). Response `{success, message:"AiProfile updated"}`. |

- The `id` passed to getAiProfile/updateAiProfile is the **aiProfileId**, not the AI userId. Resolve it with `profile.getAi(userId).aiProfileId`.
- **A freshly created AI has `aiProfileId: null`** and falls back to the shared **Default** profile, which is admin-locked: pushing rules to the Default id returns `success:false` with `Default profile only modifiable by content admin`. Call `ai.toggleAiProfile({aiId})` first to create the AI its own profile, then re-read `aiProfileId` (now populated), then update. **Toggle only when `aiProfileId` is null;** toggling an AI that already has its own profile flips it back off, which is why the builder guards the call.
- HTTP 200 is not success: read `json.success`.
- Editor: `/manual/ai/edit/[id]`, the "AI Profile" panel, with a **Default / Custom** toggle. Custom = your `rules[]`. `includeDefaultRules: true` appends the engine's default catch-all rules after yours (recommended, so the AI never stalls when no custom rule matches). The default rules cannot be edited or reordered.

### Pipeline to set behavior on a fresh enemy
1. `profile.create` -> AI userId.
2. `profile.updateAi(userId, stats + jutsus:[ids])` -> stats and equipped jutsu.
3. `profile.getAi(userId)` -> read `aiProfileId`. On a fresh AI this is **null**.
4. If `aiProfileId` is null: `ai.toggleAiProfile({aiId: userId})` -> creates the AI its own profile, then `profile.getAi(userId)` again to read the now-populated `aiProfileId`.
5. `ai.updateAiProfile(aiProfileId, rules, includeDefaultRules:true)` -> behavior.

The universal builder (v4.7+) does steps 3 to 5 automatically when an AI manifest entry carries `rules`, including the toggle-only-if-null guard. The older AI maker userscript does steps 1 and 2 only.

---

## 2. Rule object

```
{
  "conditions": [ { type, ...fields, description } ],   // AND-ed; empty [] = always true
  "action":      { type, target, ...fields, description },
  "priority":    <int>                                  // optional
}
```

- Rules are evaluated **top to bottom**; the first rule whose conditions all pass fires its action that turn. Order is everything.
- `conditions` within a rule are AND-ed. An empty array always passes (use as a fallback at the bottom).
- `priority` is optional (omitted on most captured rules).
- `description` is the human blurb the editor attaches to each condition/action; include it to mirror the editor, it is not load-bearing.
- A condition never overrides a jutsu cooldown. It changes whether a ready action is chosen, not whether an on-cooldown one can fire.

---

## 3. Conditions (9 total)

| type | fields | meaning | shape |
|---|---|---|---|
| `round_lower_than` | `value` | current round < value | CONFIRMED |
| `round_greater_than` | `value` | current round > value | CONFIRMED |
| `specific_round` | `value` | exactly on round N | CONFIRMED |
| `distance_lower_than` | `value`, `target` | distance to target <= value | CONFIRMED |
| `distance_higher_than` | `value`, `target` | distance to target >= value | CONFIRMED |
| `health_below` | `value` (percent, self) | self HP below value% | CONFIRMED |
| `has_effect` | `effectType`, `threshold` | self has effectType at/above threshold | CONFIRMED |
| `target_has_effect` | `effectType`, `target`, `threshold` | target has effectType at/above threshold | CONFIRMED |
| `does_not_have_summon` | (none) | no summon currently out | CONFIRMED |

Note the key names: effect-based CONDITIONS use `effectType`; effect-based ACTIONS use `effect`. `has_effect` / `target_has_effect` are NOT boolean, they carry a `threshold` (a value, so you can gate on effect magnitude, not just presence). The validator bounds `threshold` to an integer 0 to 100 (default 0); the comparison semantics (magnitude vs rounds vs stacks) are still not pinned.

Server prefault defaults when a field is omitted (source-confirmed): `health_below` 10, `specific_round` 10, `round_greater_than` 5, `round_lower_than` 3, `distance_higher_than` 3, `distance_lower_than` 2. Distance conditions default `target` to `RANDOM_OPPONENT`; `target_has_effect` defaults to `CLOSEST_OPPONENT`. Every `value` must be a positive integer (strings are coerced).

Confirmed condition object example (from a real save):
```
{ "type":"distance_lower_than", "value":4, "target":"RANDOM_OPPONENT",
  "description":"Distance lower than or equal given value" }
{ "type":"health_below", "value":"30", "description":"Health below given percentage" }
{ "type":"has_effect", "effectType":"absorb", "threshold":"20", "description":"AI is affected by a specific effect" }
{ "type":"target_has_effect", "effectType":"reflect", "target":"CLOSEST_OPPONENT", "threshold":"30", "description":"Target is affected by a specific effect" }
{ "type":"does_not_have_summon", "description":"Does not have a summon active" }
```

---

## 4. Actions (10 total)

Every action carries a `target` except `end_turn`. Some carry an extra selector.

| type | extra fields | meaning | shape |
|---|---|---|---|
| `move_towards_opponent` | - | close distance toward target | CONFIRMED |
| `end_turn` | - (no `target`) | stop, spend no more AP | CONFIRMED |
| `use_specific_jutsu` | `jutsuId` | fire one named jutsu | CONFIRMED |
| `use_specific_item` | `itemId` | use one named item | CONFIRMED |
| `use_random_jutsu` | - | any available jutsu | CONFIRMED |
| `use_random_item` | - | any available item | CONFIRMED |
| `use_highest_power_action` | `effect` | highest-power action (jutsu OR item) of that effect | CONFIRMED |
| `use_highest_power_jutsu` | `effect` | highest-power jutsu of that effect | CONFIRMED |
| `use_highest_power_item` | `effect` | highest-power item of that effect | CONFIRMED |
| `use_combo_action` | `comboIds` (array) | cycle a fixed list of jutsu/items in order | CONFIRMED |

Confirmed action object examples (from real saves):
```
{ "type":"use_specific_jutsu", "target":"SELF", "jutsuId":"<id>", "description":"Select specific jutsu" }
{ "type":"use_combo_action", "target":"RANDOM_OPPONENT",
  "comboIds":["<id>","<id>","<id>"], "description":"Cycly through a specific combo of jutsu & items" }
{ "type":"use_highest_power_action", "target":"RANDOM_OPPONENT", "effect":"damage",
  "description":"Use action with given effect with highest power" }
{ "type":"use_highest_power_jutsu", "target":"RANDOM_OPPONENT", "effect":"damage", "description":"Use jutsu with given effect with highest power" }
{ "type":"use_highest_power_item", "target":"RANDOM_OPPONENT", "effect":"absorb", "description":"Use item with given effect with highest power" }
{ "type":"use_random_jutsu", "target":"RANDOM_OPPONENT", "description":"Use random jutsu" }
{ "type":"use_specific_item", "target":"RANDOM_OPPONENT", "itemId":"<id>", "description":"Select specific item" }
{ "type":"end_turn", "description":"End turn" }
```

---

## 5. Targets (9 total)

`SELF`, `CLOSEST_OPPONENT`, `RANDOM_OPPONENT`, `CLOSEST_ALLY`, `RANDOM_ALLY`, `BARRIER_BETWEEN`, `BARRIER_BLOCKING_CLOSEST_OPPONENT`, `EMPTY_GROUND_CLOSEST_TO_OPPONENT`, `EMPTY_GROUND_CLOSEST_TO_SELF`.

- UPPER_SNAKE_CASE (conditions and actions are lowercase snake).
- `*_ALLY` matters in multi-enemy fights (our pyramid waves), e.g. an enemy healing or buffing a teammate.
- `EMPTY_GROUND_*` are placement targets for movement or ground-spawn AoE.
- `BARRIER_*` are for barrier interactions.
- The action target must respect the chosen jutsu/item's own target setting. A self-only jutsu will not fire on an opponent target; pair it with a self-targeted rule.

---

## 6. Effect enum (71, used by has_effect / target_has_effect / use_highest_power_*)

Identical to the jutsu effect-type enum in `21_GUIDE` 7.4 (minus the internal `unknown`). Verified exact against the TNR source tag union:

`absorb, afterburn, barrier, buffprevent, cleanseprevent, cleanse, clearprevent, clear, clone, copy, damage, debuffprevent, decreasecooldown, decreasedamagegiven, decreasedamagetaken, decreaseheal, decreasepoolcost, decreasemaxpools, decreasestat, drain, elementalseal, finalstand, fleeprevent, flee, healprevent, heal, increasecooldown, increasedamagegiven, increasedamagetaken, increaseheal, marriageslotincrease, noncombatincreasereskins, injectjutsus, increasepoolcost, increasemaxpools, increaserange, increasestat, immunity, lifesteal, mirror, moveprevent, move, noncombatconsumereward, noncombatgainskill, repair, onehitkillprevent, onehitkill, pierce, poison, recoil, redirection, reflect, removebloodline, robprevent, rob, rollbloodline, sealprevent, seal, shield, stealth, stunprevent, stun, summonprevent, summon, timecompression, timedilation, unlockitemvariant, vamp, visual, weakness, wound`

So `use_highest_power_action` with `effect:"damage"` means "best damage action available," with `effect:"heal"` means "best heal," and so on.

---

## 7. Gotchas

- **Range gating (CRITICAL).** An AI must be in range to use any target-requiring action; the tile it stands on counts as 1, max range is 5. Calling a jutsu while the target is out of range triggers a targeting bug that leaves the human stuck in combat indefinitely, so every attack / debuff / absorb rule MUST carry a `distance_lower_than` gate that guarantees whatever fires is in range, plus a `move_towards_opponent` fallback. For `use_specific_jutsu` the EXACT gate is **that jutsu's range + 1** (source law R49, 2026-08-01: rule distance is A* path length including both endpoints, so an adjacent enemy reads 2). `distance_lower_than: range` is safe but forfeits the outermost range band; `distance_lower_than: 1` on a melee jutsu can NEVER fire. A range-5 jutsu takes `distance_lower_than 6`. For `use_highest_power_action` / `_jutsu` / `_item` the engine may pick ANY equipped action of that effect, so the gate must be the MINIMUM range across all equipped jutsu of that effect; an r4 absorb jutsu that also deals damage drags the damage pool's min range down to 4. When ranges are mixed, prefer `use_specific_jutsu` with the exact range so there is no ambiguity. SELF buffs and heals have no range requirement and need no distance gate; they can fire round 1 or while the target is still closing.
- `use_highest_power_action` / `_jutsu` / `_item` is never required. Because rules fire top to bottom, lead with specific high-priority rules instead: e.g. enrage = `health_below` + `distance_lower_than <range>` then `use_specific_jutsu` the strongest jutsu, or a `use_combo_action` of specific jutsu. Reserve highest-power only where its min-range constraint is acceptable.
- `use_combo_action` has a single `target` field, so every jutsu in a combo must share a target type: an all-self-buff combo (`SELF`) or an all-enemy combo for damage/debuffs (`RANDOM_OPPONENT` etc.). Never mix self-buffs and attacks in one combo. For the same range-gating reason, all jutsu in a combo must also share a range so one `distance_lower_than` gate keeps every member in range.
- Rules run in order; put specific/situational rules above general ones, and a no-condition fallback last.
- Keep `includeDefaultRules: true` so the AI has a catch-all and never stalls.
- In a combo, order is the use order; if a combo jutsu is on cooldown and AP remains, the AI falls back to a weapon or basic attack to spend it.
- 40 AP self-buff jutsu are unreliable as actions (they may not resolve and can strand the AI); favor 60 AP actions, per `21_GUIDE` and the in-game guidance.
- Cooldowns are never bypassed by a condition.
- A condition's `value` for distance is A* PATH LENGTH: the AI's own tile counts, so an adjacent target reads 2, and occupied tiles (cost 100) force detours that inflate the reading in crowded fields. Both comparators are inclusive (>= / <=). For `health_below` it is a percent of effective max HP.
- `value` may serialize as a **string** (the editor emitted `"30"` for health_below) and the API accepts it; sending a number also saves.

---

## 8. Residual unknowns

All 9 condition and 10 action shapes are now CONFIRMED. Remaining small unknowns, not blocking:
- `threshold` semantics on `has_effect` / `target_has_effect`: whether it compares the effect's magnitude, remaining rounds, or stack count. Captured as a string (e.g. `"20"`); the source bounds it to int 0-100.
- (Resolved) The `decreasedamagetaken` jutsu effect accepts `target:"SELF"` on an enemy-targeted attack (direction stays `offence`), so a self buff can ride an attack. `absorb` (direction `defence`) and `decreasedamagetaken` (direction `offence`) are the two confirmed self-targetable effects on attacks.


## Addendum (Jul 10 2026, source extraction): vocabulary VERIFIED

`app/src/validators/ai.ts` confirms the full rule vocabulary exactly as documented and as embedded in builder preflight: 9 conditions (health_below, specific_round, round_greater_than, round_lower_than, distance_higher_than, distance_lower_than, does_not_have_summon, has_effect, target_has_effect), 10 actions (move_towards_opponent, end_turn, use_specific_jutsu, use_random_jutsu, use_highest_power_jutsu, use_specific_item, use_random_item, use_highest_power_item, use_highest_power_action, use_combo_action), 9 targets (SELF, CLOSEST_OPPONENT, RANDOM_OPPONENT, CLOSEST_ALLY, RANDOM_ALLY, BARRIER_BETWEEN, BARRIER_BLOCKING_CLOSEST_OPPONENT, EMPTY_GROUND_CLOSEST_TO_OPPONENT, EMPTY_GROUND_CLOSEST_TO_SELF). `has_effect`/`target_has_effect` accept any of the 72 tag literals (46). `includeDefaultRules` appends engine default rules after custom rules (ai_v2.ts); real users always get defaults. Engine internals (evaluation order details, backup rules) live in `app/src/libs/combat/ai_v2.ts` per the source map.

---

## The confirmed rule vocabulary and the range law (added 2026-07-27)

Rules ride on the AI entry itself; the builder toggles the profile and pushes them. There is no separate profile entity to author, so an AI manifest with no `aiProfile` records is not missing anything.

**Only the `ai.ts` vocabulary exists** (law 39). Conditions carry their own `target`; actions carry the target inside the action; every target literal is UPPER_SNAKE. The invented forms (`distance`, `use_jutsu`, `move`, a rule-level `target` object) are rejected or stored inert, and an inert rule set silently drops the enemy onto engine defaults.

```json
{"conditions": [{"type": "distance_lower_than", "value": 3, "target": "CLOSEST_OPPONENT",
                 "description": "Distance lower than or equal given value"}],
 "action": {"type": "use_specific_jutsu", "jutsuId": "<live id>", "target": "CLOSEST_OPPONENT",
            "description": "Select specific jutsu"},
 "priority": 3}
```

**Gate equals range + 1, and only for SINGLE** (law 40, amended 2026-08-01 per source R49: distance = A* path length, adjacent = 2; range+1 is exact and can never fire out of range since hex distance <= path length - 1). Derive the value as registry range + 1 from the table in `32_REGISTRY_shared_ai_pool.md`. A gate above range + 1 can fire out of range and leave a human stuck in combat; a gate at or below range never misfires but wastes reach. ALL-method and SELF-target actions carry no distance condition at all.

**This project runs `includeDefaultRules: false`**, so every rule set ends with an unconditional `move_towards_opponent` (law 41). Anything below that line is dead and should be deleted rather than left as documentation.

**Prefer literal live jutsu ids over `@jutsu:` symbols** in any manifest that is not creating the jutsu in the same run, since symbols resolve only through the builder idmap.

## Addendum: ai_v2 source verification + harvest facts (2026-08-01)

**Self-cast REINSTATED (H03 falsified).** `use_specific_jutsu` with `target: SELF` fires normally (ai_v2 getTarget returns the actor, distance 0). The Raiveth round-4 failure was law 18: the jutsu had been edited while equipped, severing the AI-jutsu combat link. A severed link and an inert rule produce the SAME log signature (rule matches, action does not execute, engine falls through, no error). **Diagnostic order: check the equip link FIRST, rule grammar second.** Line 143's all-self-buff combo stands as valid.

**Rule-list mechanics (R52):** rules evaluate top-down; first VALID action wins; invalid actions fall through silently. Backup rules (when `includeDefaultRules` or a player-account AI) APPEND AFTER custom rules. An auto `end_turn` is appended only while an effect-bearing action still exists. If NO rule yields a valid action, the engine sets the AI's curHealth to 0 ("exhausted and has to give up") - literal suicide. Every profile MUST terminate in an always-fireable rule (lint L24).

**Condition quirks (R50):** `has_effect` / `target_has_effect` with `threshold: 0` (or omitted, prefault 0) return TRUE unconditionally - a no-op. Use `threshold >= 1` to test presence; threshold compares the SUM of matching effect powers. Lint L35.

**Dead target (R51):** `BARRIER_BETWEEN` has no resolver case in ai_v2 - it always yields undefined and the rule silently never fires. Only `BARRIER_BLOCKING_CLOSEST_OPPONENT` works. Lint L36.

**Action selection (R54):** `use_highest_power_action/_jutsu/_item` filters by `rule.action.effect` (tag literal, prefault "damage"); a missing or mistyped effect matches nothing. Combos suffix-match action history against a PREFIX of comboIds; any break restarts at comboIds[0]; all steps share the one rule target and the one condition set.

**STUDENT strip (R53):** rank STUDENT loses basicHeal, meditate, clear, cleanse, both stances, replacementTechnique, and flee - a defaulted-rank AI is action-crippled on top of stat-floored (law 14's second bite).

**H07.** A ground-spawn AoE circle placed adjacent to the caster covers the caster's own tile and applies its effect to him (Raiveth ate his own 20 AP stun). Fix: `friendlyFire: "ENEMIES"` on the effect PLUS a `distance_higher_than` floor so the radius cannot reach back.

**H08.** Strict round windows are built as `round_greater_than` + `round_lower_than` bounding a combo action, never as paired `specific_round` rules. Comparators inclusive (live dgt 6/7 precedent).

**H09 (OPEN watch item).** Combo pointer independence across two rules sharing an identical `comboIds` list is unverified; if shared, a later window opens mid-combo. Check on the next Raiveth log.

**H06 (OPEN, Stage 2 capture).** Ground-spawn zones do not deliver `onehitkillprevent`; whether this generalizes to the whole prevent family is unknown.


## Relocated engine laws (2026-08-28)

Verbatim law text moved out of project knowledge. Stage 3 splices these into the
owning skill reference. Numbers stay canonical against /docs/ENGINE_LAWS.md.

14. **`rank`, `regeneration`, `preferredStat`, `preferredGeneral1/2` are REQUIRED on every AI create.** DB default is `STUDENT` with every stat 10; a rank-less create produces a level-100 paper doll.

15. **[CORRECTED 2026-08-26, source-verified] LEVEL is the stat budget, not rank.** `scaleUserStats` (`app/src/libs/profile.ts`) runs on every `profile.updateAi` and reads `user.level` only; `rank` never enters it. The supplied stat numbers act as **RATIO WEIGHTS**, not absolutes: each stat becomes `10 + (stat / sum_of_all_12) * exp`, where `exp = calcLevelRequirements(level) - 500`. Pools are overwritten outright with `calcHP(level) * poolsMultiplier`, i.e. `(100 + 50*(level-1)) * poolsMultiplier` (HP, SP and CP share the per-level constant of 50). Consequences: absolute stat values are UNREACHABLE, a second edit re-normalises so **two-phase pinning is impossible**, and sending `maxHealth` is noise. The only levers are level, the ratio between stats, `statsMultiplier` and `poolsMultiplier`. PRECISION (2026-08-26): `statsMultiplier` multiplies the WHOLE result including the flat +10 floor (`calcStat(x) * statMod`), and the per-stat value is floored to two decimals before the multiplier. Verified line by line against `scaleUserStats` in this drop. The prior reading ("writing rank triggers regeneration") came from a JONIN write that changed rank and level together and never separated them.

16. **[RECONCILED 2026-08-26] Rank governs COMBAT-TIME stat caps via `USER_CAPS`.** Read the table from `45e_DATA_constants.json`; it carries `GENS_CAP`, `STATS_CAP` and `LVL_CAP` per rank and the numbers are no longer restated here. THIRD COLUMN, previously unrecorded: `USER_CAPS` also carries `LVL_CAP` (STUDENT and GENIN are level-capped well below 100), applied at `routers/profile.ts`. `capUserStats` clamps each of the 12 stats individually, so a lopsided AI loses only the stats that breach, not the whole block. `getUserCaps` is applied in `libs/combat/util.ts`, not at write time, so an under-ranked AI writes fine and is silently clamped in battle. A level 45+ AI left on GENIN loses everything above that rank's `STATS_CAP`, which is the single most common way an AI is built strong and fights weak. `statsMultiplier` is a dead lever at endgame for the same reason: `MAX_STATS_CAP` is reached without it.

16d. **[NEW 2026-08-26] AI behaviour rules are `{conditions: Condition[], action: Action}`, tagged objects on both sides** (`app/src/validators/ai.ts`). NOT a flat `{action, condition, conditionValue, target}` triple. Every condition and action carries `type`, a `description` with a `prefault` string, and its own fields. Never hand-author one: build from `45c_DATA_constructors.json`.

39. **The AI rule vocabulary is fixed by `app/src/validators/ai.ts` and nothing else is real.** Conditions carry their own `target` (`distance_lower_than`, `distance_higher_than`, `round_lower_than`, `round_greater_than`, `specific_round`, `health_below`, `has_effect`, `target_has_effect`, `does_not_have_summon`). Actions carry the target INSIDE the action (`use_specific_jutsu`, `use_specific_item`, `use_random_jutsu`, `use_random_item`, `use_highest_power_action|jutsu|item`, `use_combo_action`, `move_towards_opponent`, `end_turn`). Target literals are UPPER_SNAKE. There is no condition type `distance`, no action `use_jutsu` or `move`, and no rule-level `target` object; rules written that way are rejected or stored inert, dropping the AI onto engine defaults with no error anyone sees. 166 of 385 rules in one campaign were in the invented dialect.

40. **The exact distance gate is the jutsu's range + 1, and ALL-method or SELF-target jutsu take NO gate at all.** (AMENDED 2026-08-01 per source R49: rule distance is A* path length including both endpoints, so an adjacent enemy reads 2 and hex distance <= path length - 1; range+1 therefore never fires out of range.) A gate above range+1 can fire out of range and leave a human player stuck in combat; a gate at or below range is safe but forfeits the outermost band; a gate of 1 on a melee jutsu can NEVER fire. A gate on an ALL-method jutsu makes a global attack walk into melee first. Derive every gate as registry range + 1 from the table in `32_REGISTRY_shared_ai_pool.md`. Lint L22 enforces.

41. **With `includeDefaultRules: false` the final rule must be unconditional** (`move_towards_opponent`, `end_turn`, or `use_random_jutsu`). Forty-two dead rules were found below fallbacks in one roster.

41b. **[QUALIFIED 2026-08-26] Unreachability applies only below ALWAYS-EXECUTABLE actions.** The engine falls through a rule whose action cannot execute, so an unconditional `use_specific_jutsu` on cooldown, or unaffordable at the current AP, does NOT block the rules beneath it - the same fall-through law 63 describes from the exhaustion side. An unconditional specific-jutsu rule is therefore a legitimate priority-ordering device, not a bug: the Verge line opens each kit with an unconditional self-buff stance (cooldown 4-5, duration 2-3) and reaches its attack rules on every round the stance is down. Only `move_towards_opponent`, `end_turn` and `use_random_jutsu` genuinely terminate a chain. Read this law with the cooldowns in hand; a rule audit that flags unconditional rules without checking cooldown will report false failures.

62. **Stealth blocks attacking.** An AI that opens with a stealth jutsu cannot attack that round, and if its remaining rules are all attacks it burns the round on movement and exhausts. Stealth belongs on a `health_below` escape rule, not an opener.

63. **`use_highest_power_action` at the end of a rule chain exhausts the AI when nothing is affordable.** Every kit needs at least one action it can always pay for.

64. **Rule condition grammar** (source-verified): `distance_lower_than`, `distance_higher_than`, `round_greater_than`, `round_lower_than`, `specific_round`, `health_below`, `does_not_have_summon` take `value`. `has_effect` and `target_has_effect` take `effectType` and `threshold` instead, NOT `value`.

65. **AI rules can use items:** `use_specific_item` (by itemId) and `use_random_item`. Consumables at 20 AP are the cheapest filler available to an AI.

66. **Usernames are unique across ALL UserData, players included.** An AI name can be rejected by a name no AI holds. Short common English words are already taken.

69. **For AI items, `{ids, number}` means number = dropChancePerc.** This is the OPPOSITE of reward arrays, where number is a drop-chance percentage and quantity is the count. Easy to invert.

70. **`updateAi` syncs items by set difference.** Any item id currently owned but absent from the payload is DELETED. Always send the creature's complete item list.

71. **`updateAi` runs `scaleUserStats` on every write.** Stat ratios are preserved exactly, but absolute totals are recomputed from level and multipliers, so every AI edit nudges the block slightly. Unavoidable on any path that writes AI fields.
