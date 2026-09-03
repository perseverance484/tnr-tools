<!-- RENDERED pack 'ai-build' from ai.md@dffeb23 + pipeline.md@f49e49f via build_packs.py - edit the sources, never this file -->
# Pack: ai-build

Minimal set for an AI enemy create/edit that ends in a push. SKILL doctrine block first, this pack second; factory.py/enemy.py construct, 45c/45d/46b own shapes and vocab. Depth on demand via references/_toc/ai.json slices: infographic workflows, blank template, effect vocabulary 4.2-4.6, targets list, ai_v2 addendum. Pipeline relocated laws enforced by validate --parity + harvest verify.

<!-- pack-trace: ai.md @dffeb23 '1. AI Enemy Spec, full field schema' -->
## 1. AI Enemy Spec, full field schema

The Spec mirrors the infographic blocks so Workflow B is a 1:1 pull. Fields are grouped Identity → Profile → Passives → Role → Pattern → Kit → Tactical Read.

**No patch/version framing in enemy outputs.** Don't put "Patch N", patch numbers, or version tags in the enemy MD, identity, or poster. Patch context belongs in commit notes/changelogs, not the enemy itself.

---

<!-- pack-trace: ai.md @dffeb23 '1.1 Identity / Header' -->
### 1.1 Identity / Header
| Field | Tag | Allowed / format | Notes |
|---|---|---|---|
| `enemy_name` | [req] | string | Big display name (e.g., `War Commander`, `Galewraith`). |
| `title` | [opt] | string | Epithet (e.g., `the Tempest Coil`). |
| `event_theme` | [req] | string | Left half of subtitle line (e.g., `WARPATH`, `MOZZARELLA`). The collection/event tag. |
| `role` | [req] | `Standard PvE Enemy` \| `Elite PvE Enemy` \| `Boss PvE Enemy` | Drives default pools/scaling/passives (see 1.8). |
| `tagline` | [req] | 1-2 sentences, italic | Flavor + role hint. |

---

<!-- pack-trace: ai.md @dffeb23 '1.2 Profile / Stat block' -->
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

---

<!-- pack-trace: ai.md @dffeb23 '1.3 Passive AI Tags (0-N; bosses/elites)' -->
### 1.3 Passive AI Tags (0-N; bosses/elites)
Time-limited "steroids", **start strong, then fall off** as their duration expires. Each:
| Field | Tag | Format |
|---|---|---|
| `tag_name` | [req] | e.g., `Increased Damage Given (Bukijutsu)`, `Increased Damage Given (None Element)` |
| `magnitude` | [req] | e.g., `35% Damage Given` |
| `duration_rounds` | [req] | int (examples: `5`, `3`) |

Standard enemies normally have **none** (`ai_tags_summary: None`).

---

<!-- pack-trace: ai.md @dffeb23 '1.4 Combat Role' -->
### 1.4 Combat Role
| Field | Tag | Format |
|---|---|---|
| `combat_role` | [req] | 1 short paragraph, designer-facing, what the enemy *does* in a fight. |

---

<!-- pack-trace: ai.md @dffeb23 '1.5 AI Pattern (behavior)' -->
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

---

<!-- pack-trace: ai.md @dffeb23 '1.6 Jutsu Kit (AI jutsu sub-schema)' -->
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

---

<!-- pack-trace: ai.md @dffeb23 '1.6.1 Damage tuning' -->
### 1.6.1 Damage tuning
Superseded: kits come from 32_REGISTRY (EP doctrine); per-hit tuning is multiplicative row products against a declared anchor (30_DOCTRINE protocol, 12_TECH laws 9/13).

---

<!-- pack-trace: ai.md @dffeb23 '1.8 Role defaults (quick reference)' -->
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

---

<!-- pack-trace: ai.md @dffeb23 '1.9 Reserved / `NOT RECORDED` registry' -->
### 1.9 Reserved / `NOT RECORDED` registry
Never invent these, leave `NR` for you/the engine:
`exact base stat numbers if not provided` · `exact armor DR%` · `loot table / drop rates` · `encounter gating (required rank/level to fight)` · `spawn context` · `art/icon image files` · `element-wheel counter relationship` · `ViolentMonkey record IDs / form selectors / endpoint`.

---

---

<!-- pack-trace: ai.md @dffeb23 '4.1 AI restrictions (read first)' -->
### 4.1 AI restrictions (read first)
- **AI enemies must NOT use `Lifesteal` (LS) or `Vamp` (VMP).** For AI sustain, use `Heal` or `Absorb` instead (e.g., War Commander's `40% Absorb`).
- **No `Movement` (MV) self-reposition jutsu on AI** (the generic "move to close" basic action is fine; `Movement Prevent` *on the target* is allowed).
- **`Trigger` is experimental**, not live canon; never use it.

---

<!-- pack-trace: ai.md @dffeb23 '8. Master QA checklist (before delivering any AI enemy)' -->
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

---

<!-- pack-trace: ai.md @dffeb23 'Addendum: effect and edit rules (live-verified)' -->
## Addendum: effect and edit rules (live-verified)

- **Direction is per-tag literal**: `"defence"` is accepted ONLY by absorb, barrier, increasepoolcost, decreasepoolcost; every other tag (including decreasedamagetaken) requires `"offence"`. Mixed setups split accordingly.
- **Barrier is a battlefield structure, not a self-buff**: target EMPTY_GROUND, requires a non-empty `staticAssetPath`, `calculation: "static"`, and real `curHealth`/`maxHealth`/`absorbPercentage`. For a worn "armor" concept use absorb + decreasedamagetaken.
- **AI edit rule**: see 10 addendum; `jutsus` (strings) + `items` (ids-with-number) explicit on every edit.

---

---

<!-- pack-trace: ai.md @dffeb23 'Rules live on the AI entry (added 2026-07-27)' -->
## Rules live on the AI entry (added 2026-07-27)

Behavior rule sets are a field on the AI record, not a separate entity: the builder pushes the AI, toggles the profile, and updates it. An audit that counts `aiProfile` entries in a manifest and finds zero has found nothing. Author rules per the vocabulary and range laws in `24_GUIDE_ai_behavior.md` (laws 39 to 41), and remember that `data.name` must be set on the create itself (law 36).

---

<!-- pack-trace: ai.md @dffeb23 '1. Contract (verified)' -->
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

---

<!-- pack-trace: ai.md @dffeb23 'Pipeline to set behavior on a fresh enemy' -->
### Pipeline to set behavior on a fresh enemy
1. `profile.create` -> AI userId.
2. `profile.updateAi(userId, stats + jutsus:[ids])` -> stats and equipped jutsu.
3. `profile.getAi(userId)` -> read `aiProfileId`. On a fresh AI this is **null**.
4. If `aiProfileId` is null: `ai.toggleAiProfile({aiId: userId})` -> creates the AI its own profile, then `profile.getAi(userId)` again to read the now-populated `aiProfileId`.
5. `ai.updateAiProfile(aiProfileId, rules, includeDefaultRules:true)` -> behavior.

The universal builder (v4.7+) does steps 3 to 5 automatically when an AI manifest entry carries `rules`, including the toggle-only-if-null guard. The older AI maker userscript does steps 1 and 2 only.

---

---

<!-- pack-trace: ai.md @dffeb23 '2. Rule object' -->
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

---

<!-- pack-trace: ai.md @dffeb23 '3. Conditions (9 total)' -->
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

---

<!-- pack-trace: ai.md @dffeb23 '4. Actions (10 total)' -->
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

---

<!-- pack-trace: ai.md @dffeb23 '7. Gotchas' -->
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

---

<!-- pack-trace: ai.md @dffeb23 'The confirmed rule vocabulary and the range law (added 2026-07-27)' -->
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

---

<!-- pack-trace: ai.md @dffeb23 'Relocated engine laws (2026-08-28)' -->
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

---

<!-- pack-trace: pipeline.md @f49e49f '1.4 Image upload (the builder resolves `@img` refs)' -->
### 1.4 Image upload (the builder resolves `@img` refs)

A manifest field value `@img:<filename>` is uploaded by the builder and replaced with the stored URL, so image assets never have to be uploaded by hand. Upload flow (uploadthing, captured):

1. Presign: POST `/api/uploadthing?actionType=upload&slug=imageUploader`, credentials same-origin, body `{files:[{name,size,type,lastModified}]}` -> `[{url:<signed ingest URL>, key}]`.
2. HEAD then PUT the file (FormData field `file`) to the signed url.
3. Stored URL = `https://<app-id>.ufs.sh/f/<key>` (app id `ui0arpl8sm`). No finalize or poll; the URL is live immediately. The builder caches it in the idmap under the filename and reuses it on re-run.

**Picker gotcha (Android).** The Gallery / Photos picker hands the file input MediaStore-numbered names (e.g. `1000007643.jpg`) and re-encodes PNGs to JPG, which destroys sprite transparency. Load images through the **Files / Documents** picker, which preserves the real filename and the raw bytes. The builder's file input carries no `accept` filter specifically to steer Firefox to the document picker. As a safety net the manifest may carry an `imgSizes` map (`{filename: bytes}`); the builder then matches a file by byte size even when the picker renamed it, but this only works on the raw original (document picker), not a re-encoded copy.

---

<!-- pack-trace: pipeline.md @f49e49f '2.1 Request envelope and conventions' -->
### 2.1 Request envelope and conventions

- TNR uses tRPC batch links. **Every POST body is a batch envelope:** `{"0": { "json": <payload>, "meta": <meta> }}`.
- **Create endpoints take a null-body envelope** (`{"json": null, "meta": {"values": ["undefined"], "v": 1}}`) and **return the new id in the response `message` field** (exception: `item.create`, see 2.3).
- **Update endpoints** take `{"json": {"id": <id>, "data": <data>}, "meta": <meta>}`. The `meta` typically flags `createdAt`/`updatedAt` as Dates.
- **GET list endpoints** (`*.getAll`) are `?batch=1&input=<urlencoded {"0":{"json":{cursor,limit}}}>` and page via `nextCursor`.
- HTTP 200 does not mean success. Read `json.success` and `json.message`.

---

<!-- pack-trace: pipeline.md @f49e49f '2.4 AI enemy (profile)' -->
### 2.4 AI enemy (profile)

| Op | Method | Shape |
|---|---|---|
| `profile.create` | POST | null body -> new AI id in `message`. |
| `profile.updateAi` | POST | `{json:{id,data}}` with **NO meta wrapper and NO date fields** (differs from jutsu/item). |

Edit URL for the in-console editor: `/manual/ai/edit/[id]`. Armor is set in the editor, not in the payload. See `21_GUIDE_ai_enemy.md` for the data schema. AI behavior rules live on a separate AiProfile row with its own contract (`ai.toggleAiProfile`, `ai.getAiProfile`, `ai.updateAiProfile`); a fresh AI is `aiProfileId: null` and needs the toggle before rules attach. See `24_GUIDE_ai_behavior.md`.

---

<!-- pack-trace: pipeline.md @f49e49f '3. Rate limit' -->
## 3. Rate limit

The limiter is a **rolling cumulative request-count budget**, not per-burst. It drains across repeated sessions and refills over time. Use fewer, larger requests with exponential backoff (the builder does this), and let it refill rather than hammering.

---

<!-- pack-trace: pipeline.md @f49e49f '4. id-fetch and capture-first discipline' -->
## 4. id-fetch and capture-first discipline

- Pull live ids from edit URLs (`/manual/ai/edit/[id]`, `/manual/asset/edit/[id]`, the item editor) or from catalog dumps.
- For names to ids, dump the relevant catalog and resolve from the JSON.
- After a builder run, the status rows show `-> <id>` and the idmap holds `srcId -> createdId`; copy those into dependent content (e.g. chest ids into a quest branch reward).
- To verify a new or changed contract, run it once in the editor, capture the call, and confirm `json.success` before building a generator. A 500 with a clear column message (e.g. the `battleDescription` case) still teaches the exact field rule.

---

<!-- pack-trace: pipeline.md @f49e49f '5. Universal gotcha checklist' -->
## 5. Universal gotcha checklist

Run before any push:

1. No em dashes in quest player-facing dialog text (a dialog node's `description`, a choice's `text`). Em dashes are fine elsewhere, in payloads, prose, and code.
2. All ids (AI, item, asset, jutsu) are real, pulled from edit URLs or catalog dumps, never invented.
3. Read `json.success` / `json.message`; HTTP 200 alone does not mean the save applied.
4. `item` pushes: `battleDescription` is non-empty; `item.create` body is `{type}`, not null.
5. `profile.updateAi` carries no meta and no dates; `jutsu.update` and `item.update` do carry date meta.
6. Quest pushes: the flatten rule and 7 referentialEqualities are present (builder handles), and the objective graph passes flow validation (see `23_GUIDE_quest.md`).
7. Rate limit is cumulative and cross-session; batch with backoff and let it refill.
8. Userscripts match both `www` and non-`www`, use `createElement`/CSSOM not `innerHTML`, and are hosted via `@require` if large.
9. `create` payloads carry the COMPLETE field set for the type (guides 20/23), including easy-to-miss required numbers (jutsu `*ReducePerLvl`, quest `consecutiveObjectives`/`maxAttempts`/`maxCompletes`); `convert`/`edit` payloads carry only the change and reproduce whole arrays.
10. Names are unique: dedup a new jutsu / AI / item / quest name against the catalog or a `getAllNames` capture before creating. A duplicate returns 200 with `success:false` and leaves a blank `New ...` shell.
11. Images load through the Files / Documents picker, not Gallery, so filenames and PNG transparency survive (1.4).
12. After a build, spot-check the live records. v4.12 reads `json.success` per entry so a rejected save shows red; on older bundles a 200 with `success:false` showed "ok" and left blank shells.

---

<!-- pack-trace: pipeline.md @f49e49f 'Addendum: push-path rules learned in the field (Tower / Howling builds)' -->
## Addendum: push-path rules learned in the field (Tower / Howling builds)

- **AI edits never rely on fetch-merge for `jutsus` or `items`.** The builder passes live rows through raw (jutsu objects, UserItem rows with `dropChancePerc`), which the server rejects. Every AI edit sends `jutsus` as string id refs AND `items` as ids-with-number explicitly, even when only touching other fields. Bundle fix (row normalization in the edit merge) queued for the next builder rev.
- **Quest EDITS do not fetch-merge top-level fields.** A partial quest edit reaches the server with `name`/`description`/`questType`/`tierLevel` undefined and 400s. Reproduce the FULL quest record from a live capture with changes applied. (Whole-array rule, promoted to whole-record for quests.)
- **Items: `battleDescription` is DB NOT NULL.** Empty string is nulled by the write path and 500s at the DB. Always non-empty.
- **AI edits require an explicit `targetId`.** The idmap does not resolve srcIds for `ai` edit entries ("ai needs targetId or slot create"); jutsu converts/edits accept srcId via idmap but carry `targetId` anyway when known. Pull the AI id from the idmap dump or edit URL.
- **The jutsu edit/convert merge-base load trips the API rate limiter** (v4.12): even single-entry, targetId-carrying edit manifests stall on "limited 10s" retries. Workarounds until the builder rev (per-id `jutsu.get` merge base + lazy catalog load): make small scalar/effect changes by hand in the admin UI while the jutsu is unequipped, then push a lean re-equip ai edit; keep any builder-path edit manifests to the minimum entries and let the limiter cool between runs.
- **`stun` AP loss is the `apReduction` field, not `power`.** Power is only the stun CHANCE (RNG roll); an omitted `apReduction` silently takes the server default (-10 AP observed live). Always set `apReduction` explicitly on stun effects. Same power-as-chance pattern applies to the whole prevent/control family (shield creation, flee, seal, prevents).
- **Combat internals are documented in 50_DATA_combat_facts.md** (damage formula and constants, 450k/200k battle-init caps incl. AIs, LVL_CAP 100 clamp, the 10% minimum-damage floor and its boost scaling, pierce pipeline bypass, modifier staging order, ai threshold semantics). Read it before any combat balance work; it is calibrated against live fight captures.
