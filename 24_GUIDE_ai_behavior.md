# 24 - GUIDE: AI Behavior (AiProfile rule sets)

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
