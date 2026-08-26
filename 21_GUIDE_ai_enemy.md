# 21 - GUIDE: AI Enemy Creation

Owner doc for AI (PvE) enemy record shape, generation conventions, the verified profile and jutsu tRPC contracts, the effect-object schema, the enemy-infographic layout, and the batch-script payload. For shared plumbing (the builder, capture tool, rate limit, the contract envelope) see `10_TECH_pipeline.md`. For cross-cutting balance philosophy see `30_DOCTRINE_balance.md`; where those conflict with this file on AI-enemy specifics, this file wins. Stat and pool values are balance decisions reserved by Brandon, never invented. Enemy outputs carry no patch or version framing.

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
