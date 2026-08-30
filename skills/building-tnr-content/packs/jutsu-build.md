<!-- RENDERED pack 'jutsu-build' from jutsu.md@f9fa8cc + pipeline.md@f1985e5 via build_packs.py - edit the sources, never this file -->
# Pack: jutsu-build

Minimal set for a jutsu create/edit that ends in a push. Read the SKILL doctrine block first, this pack second, data files as needed. Curation of ai/quest/item/art packs is follow-up work; this pack is the proven exemplar.

<!-- pack-trace: jutsu.md @f9fa8cc '1. Jutsu tRPC contract' -->
## 1. Jutsu tRPC contract

Envelope rules are in `10_TECH_pipeline.md`. Jutsu-specific:

| Op | Method | Shape |
|---|---|---|
| `jutsu.create` | POST | null-body envelope, returns new id in `message`. |
| `jutsu.update` | POST | `{json:{id,data}, meta:{values:{"data.createdAt":["Date"],"data.updatedAt":["Date"]}, v:1}}`. |
| `jutsu.getAll` | GET | requires a `limit` (number) in the input or it 400s; page via `nextCursor`. |

The builder pattern is create-then-fill: POST a blank `jutsu.create`, read the id from `message`, then `jutsu.update` with your fields.

**Create-fill merges as of builder v4.12.** After `jutsu.create`, the builder GETs the fresh record (`jutsu.get {id}`, source-confirmed) and merges your `data` over its defaults, the same fetch-merge `convert` uses. A partial `create` no longer NaN-fails on a missing required field. Complete payloads (2.1) remain best practice, since server defaults are placeholders (blank name, default image), not content. On v4.11 and older, `create` sent `data` as-is with no merge, and a missing required number coerced to `NaN` and failed with `expected number, received NaN`; that era is why the complete-payload discipline exists.

---

---

<!-- pack-trace: jutsu.md @f9fa8cc '2. Jutsu field schema (complete)' -->
## 2. Jutsu field schema (complete)

The complete set of fields written on `jutsu.update`, captured from a live AI jutsu record and now verified against the server's own write validator (JutsuValidator, extracted from the TNR source). The machine-readable schema with every type, range, default, and enum is `45_DATA_field_schemas.json`. Defaults shown are safe values for an AI-kit jutsu; player jutsu differ where noted (not hidden, real rank, real pool costs, a player `jutsuType`). Do not omit a required field on a `create`.

**Required strings and enums**

| Field | Values | Notes |
|---|---|---|
| `name` | string | Display name. **Must be UNIQUE across all live jutsu.** A duplicate name returns HTTP 200 with `success:false` and leaves a blank `New Jutsu - <id>` shell. See 2.2. |
| `description` | non-empty string | Menu blurb. Empty or missing 400s. |
| `battleDescription` | non-empty string | Combat-log line. Placeholders `%user`, `%target`, `%jutsu`. Empty or missing 400s. |
| `jutsuType` | `"AI"` for enemy kits; a player category otherwise | AI-kit jutsu use `"AI"`. |
| `jutsuRank` | full ladder `D` / `C` / `B` / `A` / `S` / `H` (there is no E rank) | Cosmetic for hidden AI jutsu; prefer `"D"`. |
| `jutsuWeapon` | `NONE`, or one of: `STAFF` `AXE` `FIST_WEAPON` `SHURIKEN` `SICKLE` `DAGGER` `SWORD` `POLEARM` `FLAIL` `CHAIN` `FAN` `BOW` `HAMMER` | This is the JUTSU weapon field; the same 14-value enum as the item `weaponType`. |
| `statClassification` | `Highest` / `Ninjutsu` / `Genjutsu` / `Taijutsu` / `Bukijutsu` | Scaling school. Prefer `"Highest"` for elementals. |
| `battleUsageType` | `PVE` / `PVP` / `BOTH` | Server default `BOTH` when omitted. |
| `target` | `SELF` / `OTHER_USER` / `OPPONENT` / `ALLY` / `CHARACTER` / `GROUND` / `EMPTY_GROUND` | |
| `method` | `SINGLE` / `ALL` / `AOE_CIRCLE_SPAWN` / `AOE_LINE_SHOOT` / `AOE_WALL_SHOOT` / `AOE_LARGE_WALL_SHOOT` / `AOE_CIRCLE_SHOOT` / `AOE_SPIRAL_SHOOT` | `ALL` is all-targets; the `AOE_*` methods are shaped ground patterns. |
| `requiredRank` | `"STUDENT"` for AI | Gating rank to learn or use. |

**Required numbers** (a missing one coerces to `NaN` and 400s)

| Field | Notes |
|---|---|
| `range` | int 0 to 5 (0 self). The validator caps range at 5. |
| `requiredLevel` | int 1 to 100, `1` for AI. |
| `actionCostPerc` | integer `40` or `60` only (doctrine). The validator accepts 10 to 100. |
| `cooldown` | int rounds, 0 to 300. |
| `chakraCost` / `staminaCost` / `healthCost` / `extraBaseCost` | real pool costs (pools 0 to 10000; extraBaseCost 0 to 65535). AI kit jutsu use `0`; the `0.05` value is a placeholder that leaked onto some player jutsu (sweep in 6). |
| `staminaCostReducePerLvl` / `chakraCostReducePerLvl` / `healthCostReducePerLvl` | **required, default `0`.** These three were the recurring NaN culprit; they are easy to forget and non-optional. |

**Required but emptyable (use `""`, not null)**

| Field | Notes |
|---|---|
| `bloodlineId` | `""` when none. The validator accepts string or null; the live record uses empty string. |
| `villageId` | `""` when none. The validator accepts string or null; live uses empty string. |
| `image` | uploaded asset url (or an `@img:<file>` ref the builder resolves). |
| `hidden` | bool. `true` for AI-kit jutsu, `false` for player jutsu. Optional server-side; always send it explicitly. |

**Nullable (default `null`)**

| Field | Notes |
|---|---|
| `requiredBloodlineItemId` | null when none. |
| `parentJutsuId` | null. |
| `injectableInBattle` | bool, default `false`. |
| `requiredStrength` / `requiredSpeed` / `requiredIntelligence` / `requiredWillpower` | stat gates, null when ungated. |
| `requiredNinjutsuOffence` / `requiredNinjutsuDefence` | null when ungated. |
| `requiredGenjutsuOffence` / `requiredGenjutsuDefence` | null when ungated. |
| `requiredTaijutsuOffence` / `requiredTaijutsuDefence` | null when ungated. |
| `requiredBukijutsuOffence` / `requiredBukijutsuDefence` | null when ungated. |

**Array**

| Field | Notes |
|---|---|
| `effects` | array of effect objects (section 3). Damage is itself an effect entry. |

**Builder-managed (do not hand-set)**

`id`, `createdAt`, `updatedAt`. The builder assigns the id, preserves `createdAt` on convert, stamps `updatedAt`, and attaches the Date meta. Display tags are derived from the effects and are not sent.

---

<!-- pack-trace: jutsu.md @f9fa8cc '3. Effects and tags (shared schema)' -->
## 3. Effects and tags (shared schema)

The `effects[]` object schema is identical to the AI jutsu schema. Use the **verified effect-object schema in `21_GUIDE_ai_enemy.md` section 7.4** (keys: `type`, `power`, `powerPerLevel`, `rounds`, `calculation`, `direction`, `target`, `statTypes`, `generalTypes`, optional `elements` on damage/pierce, cosmetic keys optional). The complete lowercase `type` enum and the per-type direction and calculation rules are in that same section.

The **tag vocabulary in guide 21 section 4** also applies, with one difference: the **AI restrictions do not apply to player jutsu.** Players may use `lifesteal`, `vamp`, and self `move` (movement) jutsu, which AI enemies may not. Everything else (the stacking set, poison and increased-cost global cooldowns, stun being minus 40 AP, the distinction between Vamp / Absorb / Lifesteal) is the same.

---

---

<!-- pack-trace: jutsu.md @f9fa8cc '6. Mass-edit, sweep, and re-equip patterns' -->
## 6. Mass-edit, sweep, and re-equip patterns

The builder's `convert` slot (entity `jutsu`) is the bulk-edit path. As of builder v4.6 it **fetch-merges**: on the first convert of a run it loads the full live jutsu catalog once (`jutsu.getAll`, two passes so **hidden AI jutsu are included**, mapped by id), then for each entry it merges your `data` over the live record, strips the read-only `bloodline` join, preserves the original `createdAt`, and sends `jutsu.update`. It throttles about 2 seconds apart with backoff and is idempotent.

Because it merges over the live record, **a convert entry only needs the fields you are changing.** A description fix is just `{entity:"jutsu", slot:"convert", targetId:"<id>", data:{description:"..."}}`; the builder pulls the rest of the record itself. Full-record `data` still works. The trimmed catalog (`40_INDEX_jutsu.json`) is for finding the target ids, not as convert input. Confirm each save read `json.success`.

**Re-equip after editing a jutsu that is on an AI (stale-equip).** If you modify a jutsu after it has been equipped to an AI, the AI will not use it in combat until it is re-equipped; the equip link is captured at equip time and goes stale on edit. The fix lives in `21_GUIDE_ai_enemy.md`: unequip (`profile.updateAi` with `jutsus: []`), save, then re-equip (`jutsus: [ids]`), save. Any jutsu edit that touches enemy-kit jutsu should be followed by a re-equip pass for the affected AIs.

Two known candidate sweeps over the live catalog (run with the bloodline-ownership caution from doctrine 7, since bloodline jutsu may be user-owned):
- **Placeholder descriptions:** about 267 jutsu carry placeholder description text. A sweep replaces them with real descriptions, in batches, candidate status until accepted, each entry carrying only the new `description`.
- **Placeholder pool costs:** about 24 player-facing jutsu still carry the `0.05` placeholder pool cost (the AI default leaked onto player content). A sweep sets real `chakraCost` / `staminaCost`. Cost values are a balance call.

---

---

<!-- pack-trace: jutsu.md @f9fa8cc '8. QA checklist (before any jutsu push)' -->
## 8. QA checklist (before any jutsu push)

- [ ] `create` payloads preferably carry the COMPLETE field set (section 2), including the three `*ReducePerLvl` numbers and `bloodlineId`/`villageId` as `""` (v4.12 merges defaults under partial creates, but placeholders are not content); `convert` payloads carry only the change (2.3).
- [ ] `name` is unique against the catalog / `getAllNames`; a themed set that collides is prefixed (2.2).
- [ ] `description` and `battleDescription` are both non-empty.
- [ ] `actionCostPerc` is 40 or 60; damage only on 60 (doctrine 1, 4).
- [ ] At most 3 tags (damage counts), 2 preferred.
- [ ] Damage numbers use the player tier scope (38 / 40 / 45 / 50), not the AI curve.
- [ ] Effects use the verified schema (guide 21 section 7.4); every field enum is source-confirmed in `45_DATA_field_schemas.json` (rank ladder D/C/B/A/S/H, 14 weapon values, 5 stat schools, 8 methods, 7 targets).
- [ ] Player pool costs are real, not the `0.05` AI placeholder.
- [ ] Bloodline-linked jutsu are not edited without confirming ownership (doctrine 7).
- [ ] Any edit to an equipped enemy-kit jutsu is followed by a re-equip pass (section 6, guide 21).
- [ ] Push read `json.success` / `json.message`, not just HTTP 200; then confirm the live record is not a blank shell.

---

<!-- pack-trace: jutsu.md @f9fa8cc 'Relocated engine laws (2026-08-28)' -->
## Relocated engine laws (2026-08-28)

Verbatim law text moved out of project knowledge. Stage 3 splices these into the
owning skill reference. Numbers stay canonical against /docs/ENGINE_LAWS.md.

18. **Editing an equipped jutsu severs the combat link** (manifest convert or admin hand-edit alike): unequip -> edit -> re-equip, always. DIAGNOSTIC ORDER (2026-07-31/08-01): a severed link and an inert rule produce an IDENTICAL log signature (rule matches, action does not execute, engine falls through, no error) - check the equip link FIRST before diagnosing rule grammar. The old "self-cast must route through combo actions" reading was this law misattributed; `use_specific_jutsu` + `target: SELF` fires normally (source R55).

20. **[CORRECTED 2026-08-26, materially wrong before] The injectjutsus guard blocks ONE thing: turning `injectableInBattle` off.** Source, `routers/jutsu.ts` update path: the relation lookup runs unconditionally, but the rejection is wrapped in `if (!input.data.injectableInBattle)`, and the error reads "so you cannot disable it." An edit that keeps `injectableInBattle: true` passes with injectors attached. The jutsu is NOT uneditable for life.

    WHY WE BELIEVED OTHERWISE, and why it still bites: `injectableInBattle` is `z.coerce.boolean().prefault(false)`. Any edit that omits the field sends FALSE, trips the guard, and returns a message about injection that reads like a blanket lock. The fix is one field, not a new jutsu. Wrapper jutsu should still be born final and unhidden (the engine requires injected jutsu unhidden, and law 46's publish rule applies), but minting a replacement to escape a "permanent" join was never necessary. The guard covers four injector sources: jutsu, bloodline, skillTree and item.

59. **A jutsu record can be silently reduced to a blank shell** named `New Jutsu - <id>` with default AP 80 and 0.05 costs. The id survives, so no reference breaks and no orphan scan catches it: only a name search or a battle failure reveals it. Refill from the last harvest.

60. **Law 18 has an ORDER, not just a requirement.** Editing an equipped jutsu and re-equipping in the same run is NOT sufficient. The sequence is strictly unequip, then edit, then re-equip.

---

<!-- pack-trace: pipeline.md @f1985e5 '2. Verified tRPC contracts' -->
## 2. Verified tRPC contracts

---

<!-- pack-trace: pipeline.md @f1985e5 '4. id-fetch and capture-first discipline' -->
## 4. id-fetch and capture-first discipline

- Pull live ids from edit URLs (`/manual/ai/edit/[id]`, `/manual/asset/edit/[id]`, the item editor) or from catalog dumps.
- For names to ids, dump the relevant catalog and resolve from the JSON.
- After a builder run, the status rows show `-> <id>` and the idmap holds `srcId -> createdId`; copy those into dependent content (e.g. chest ids into a quest branch reward).
- To verify a new or changed contract, run it once in the editor, capture the call, and confirm `json.success` before building a generator. A 500 with a clear column message (e.g. the `battleDescription` case) still teaches the exact field rule.

---

<!-- pack-trace: pipeline.md @f1985e5 '5. Universal gotcha checklist' -->
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
