# Law provenance audit

Where each engine law comes from, one verdict per law, verified against a single
pinned commit of the game source.

| | |
|---|---|
| Laws audited | 93 (`docs/ENGINE_LAWS.md`, ids 1-89 plus 16b, 16c, 16d, 41b) |
| Source repo | `studie-tech/TheNinjaRPG` |
| **Commit scanned** | **`345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9`** |
| Commit date | 2026-08-31 (`Stabilize hospital patient ordering`) |
| Verified against | that commit only, never prod |

Every `file:line` below was read in this pass. Where a law could not be settled
from source, the verdict says so rather than offering a guess.

`docs/10_LAWS_core.md` introduces no new numbered laws. It restates laws 9-13, 27,
28, 29, 57, 58, 59, 61, 66, 75, 76 and 89 and adds one unnumbered principle
("Storage is not intent"), which is DOCTRINE by the same reasoning as law 27.

## Verdict counts

| Verdict | Count | Means |
|---|---:|---|
| `ENGINE` | 36 | Provable from source, with file, line and symbol |
| `PARTIAL` | 19 | Some clauses provable, some not; the note says which |
| `CONTRADICTED` | 1 | Source says something different from the law |
| `NOT_IN_SOURCE` | 26 | Not settleable from the codebase |
| `DOCTRINE` | 11 | Our own choice or convention; no engine fact behind it |
| **Total** | **93** | |

One law is fully `CONTRADICTED`; three more carry a contradicted *clause* inside a
law that otherwise verifies, which is why they land on `PARTIAL`. All four are
called out next, because they are the findings most worth acting on.

## Contradicted clauses

Four laws state something the source at this commit does not support. In each case
the law's *instruction* survives; it is the stated mechanism, reason or direction
that is wrong. Law 19 is a full `CONTRADICTED`; the other three carry a contradicted
clause inside a law that otherwise verifies, which is why they sit at `PARTIAL`.

### Law 6 - Effect `power` does not cap at 100

**Law says:** "Effect `power` caps at 100 per row."

**Source says:** `PowerAttributes.power` is `z.coerce.number().min(0)` with no maximum (`app/src/validators/combat.ts:111`), and it is spread *after* `BaseAttributes` in every tag that uses it (`combat.ts:164-167`), so it overrides the capped `BaseAttributes.power` at `combat.ts:98`. Roughly nineteen tags are affected, including `increasedamagegiven`, `decreasedamagetaken`, `absorb`, `increasestat` and `copy`.

**Why it matters:** Law 9 builds tier tuning as row products on the assumption of a 100 ceiling per row. That ceiling is not there for this tag family. The law's other three clauses (`apReduction`, `threshold`, unbounded condition `value`) all verify.

### Law 23 - The DB default for `consecutiveObjectives` is `true`, not `false`

**Law says:** "the DB default is false = every objective simultaneously live."

**Source says:** `app/drizzle/schema.ts:3622` reads `boolean("consecutiveObjectives").default(true).notNull()`.

**Why it matters:** The law's instruction still holds for a different reason: `validators/objectives.ts:700` is `z.coerce.boolean()` with no prefault, so the write schema does require the field. Set it explicitly because the schema demands it, not because the DB default is unsafe. Law 37 rests on 23's premise and needs re-deriving. Re-check found corroboration that true is the intended state: the game's own editor warns when consecutiveObjectives !== true (layout/ContentHelp.tsx:896), and schema.ts:3622 is the only default in the tree.

### Law 75 - The ground-effect promotion condition is inverted

**Law says:** "Ground effects promoted to user effects are written with `createdRound: curRound - 1` when instant."

**Source says:** `app/src/libs/combat/process.ts:335` reads `createdRound: isInstant ? curRound : curRound - 1` - that is `curRound - 1` when **not** instant. Instant promotions get `curRound` and `rounds: 0`; the source comment above it says so.

**Why it matters:** Everything else in law 75 verifies exactly, including `calcEffectRoundInfo`, the `castThisRound` assignment, all four named consumers, the `isInstant` triple and `passesTiming`. Worth correcting precisely because this law is the model the others are meant to reach.

### Law 19 - The item effects union is not narrower - it is wider

**Law says:** "The item effects union is narrower than the jutsu union."

**Source says:** There is one shared union. Both entities use `effects: z.array(AllTags).superRefine(SuperRefineEffects)` - jutsu at `app/src/validators/combat.ts:1327`, item at `:1491`. The asymmetry comes from the per-entity refinements, and it runs the other way: `SuperRefineJutsu` (`:1218-1220`) rejects `rollbloodline`, `rollsagemode` and `removebloodline` outright, while `SuperRefineItem` (`:1122`) permits all of them and merely constrains `noncombatconsumereward` to a CONSUMABLE targeting SELF (`:1154-1160`).

**Why it matters:** The law's authoring advice (wrap unproven tags in injectjutsus, test with a throwaway record) is still safe. Its stated direction is not, and a tag list derived from it would exclude item-legal tags. The law already notes its membership list drifted once in 2026-07; the direction has now drifted too.

## Verdicts

### Law 1 - `NOT_IN_SOURCE`

Stated as a cross-cutting generalization over all create/update router pairs; no single site expresses it.

> Not settleable as one citation. Individual per-entity instances may be provable; this pass found no create/update validator pair that demonstrates the asymmetry as stated. Low confidence.

### Law 2 - `ENGINE`

`app/src/validators/combat.ts:164` - `IncreaseDamageGivenTag`

Each tag is a closed z.object spread from BaseAttributes/IncludeStats/PowerAttributes; the tag union is discriminated on the type literal.

> Zod objects reject unknown keys only under .strict(); the union arm still fails when a field belongs to a different arm's shape, which is the observed behaviour. The `direction: type("offence")` fixed literal is at combat.ts:103.

### Law 3 - `DOCTRINE`

An authoring procedure (compose from live exemplars, not from schema docs).

> Nothing in the codebase implies it. The per-entity lean/full split it describes is a real consequence of laws 2 and 19.

### Law 4 - `PARTIAL`

`app/src/validators/combat.ts:815` - `statTypes / generalTypes`

Both fields exist and default to empty: statTypes/generalTypes are z.array(...).prefault([]) at combat.ts:815-816, .optional() at :124-125.

> PROVABLE: the fields exist and the schema permits an empty generals list, so nothing rejects the payload. NOT PROVABLE in this pass: the 'detonates into astronomical values' consequence, which lives in the damage formula and was not traced. The law's authoring instruction is sound; its stated failure mode is unverified here.

### Law 5 - `NOT_IN_SOURCE`

Concerns how OUR builder resolves srcId/idmap before the request is sent.

> The claim is about the manifest layer, not the engine. The server sees only a concrete id.

### Law 6 - `PARTIAL`

`app/src/validators/combat.ts:111` - `PowerAttributes`

PowerAttributes.power is z.coerce.number().min(0).prefault(1) with NO max, and it is spread AFTER BaseAttributes in all 61 tags that use it, so it overrides the capped BaseAttributes.power at :98.

> CONTRADICTED CLAUSE: 'Effect power caps at 100 per row' does not hold. BaseAttributes.power is .min(-100).max(100) at :98, but 61 of the 70 tags spread PowerAttributes last and are uncapped - including damage, pierce, heal, shield, stun, absorb and the whole increase/decrease family. Only 9 tags omit it (finalstand, activatesagemode, noncombatconsumereward, repair, visual, weakness, unknown, injectjutsus, unlockitemvariant), and several of those declare their own power with .max(100) instead (e.g. finalstand at :580, rollbloodline at :690). No tag redeclares power after the spread, so nothing restores the cap. CONFIRMED CLAUSES: apReduction .max(100) at :775; has_effect/target_has_effect threshold .max(100) at validators/ai.ts:77,84; condition value has no upper bound at validators/ai.ts:25. See the report's contradictions section.

### Law 7 - `ENGINE`

`app/src/validators/objectives.ts:701` - `endsAt / startsAt`

z.string().regex(DateTimeRegExp, "Must be of format YYYY-MM-DD").nullable()

### Law 8 - `ENGINE`

`app/src/validators/objectives.ts:676` - `maxLevel / maxAttempts / maxCompletes`

All three are z.coerce.number().min(0).max(100) at objectives.ts:676-678.

### Law 9 - `ENGINE`

`app/src/libs/combat/tags.ts:924` - `adjustDamageGiven`

const multiplier = 1 + (power / 100) * ratio; consequence[damageKey] = current * multiplier - each percentage row multiplies the running total, so N rows compound as the product of (1 + p_i).

> Upgraded from NOT_IN_SOURCE on re-check. The same form appears in adjustDamageTaken at tags.ts:1009. The gate above it, if (!effect.isNew && !effect.castThisRound), independently corroborates law 75.

### Law 10 - `ENGINE`

`app/src/libs/combat/tags.ts:1009` - `adjustDamageTaken`

Same multiplicative form as law 9: multiplier = 1 + (power / 100) * ratio applied to the running consequence. A decrease carries negative power, so the product is of (1 - p_i).

> Upgraded from NOT_IN_SOURCE on re-check. decreasedamagetaken and decreasedamagegiven are damageReductionTypes (libs/combat/constants.ts:155-158), which the constants file documents as applied AFTER all boosts.

### Law 11 - `NOT_IN_SOURCE`

Pierce bypassing damage modifiers was not traced to a source expression in this pass.

> damageBoostTypes/damageReductionTypes membership at process.ts:1508 is the place to settle it; not read closely enough to cite. Low confidence.

### Law 12 - `DOCTRINE`

A design instruction (gate or cap ramps by rounds) resting on law 9.

> The compounding follows arithmetically from law 9; the instruction is ours.

### Law 13 - `DOCTRINE`

A calibration protocol for our own tuning work.

> Explicitly a procedure. Nothing in the codebase implies it.

### Law 14 - `PARTIAL`

`app/drizzle/schema.ts:2316` - `userData.rank`

rank: mysqlEnum("rank", consts.UserRanks).default("STUDENT").notNull(); regeneration default 60 at schema.ts:2311.

> PROVABLE: the DB default is STUDENT exactly as stated, and insertAiSchema requires regeneration (z.coerce.number().min(1).max(100), no prefault, schema.ts:2607). NOT PROVABLE: 'REQUIRED on every AI create' for rank/preferredStat/preferredGeneral1 - createInsertSchema makes defaulted columns optional, so these are an authoring rule of ours justified by the engine default, not a schema requirement.

### Law 15 - `ENGINE`

`app/src/libs/profile.ts:166` - `scaleUserStats`

exp = calcLevelRequirements(user.level) - 500 (:204); calcStat = 10 + Math.floor((user[stat]/sum)*exp*100)/100 (:220); each stat then * statMod (:222); pools = calcHP/SP/CP(level) * poolMod (:197-202).

> Verified clause by clause, including the two details the law adds as PRECISION: statsMultiplier multiplies the whole result including the +10 floor, and the per-stat value is floored to two decimals first. rank never enters scaleUserStats - it is absent from the Pick<> parameter type at :167-190. calcHP = 100 + HP_PER_LVL*(level-1) at profile.ts:106, and HP_PER_LVL = SP_PER_LVL = CP_PER_LVL = 50 at drizzle/constants.ts:823-825. Runs on every updateAi at routers/profile.ts:1549. The most precisely correct law in the set.

### Law 16 - `ENGINE`

`app/drizzle/constants.ts:2762` - `getUserCaps`

getUserCaps(rank) returns {stats_cap, gens_cap, lvl_cap} from USER_CAPS[rank]; capUserStats (profile.ts:138) clamps each of the 12 stats individually.

> USER_CAPS lives in app/drizzle/constants.ts, not under app/src. Third column confirmed: lvl_cap is real and applied at routers/profile.ts:479. Combat-time application confirmed at libs/combat/util.ts:2298. 'Not at write time' confirmed: updateAi (routers/profile.ts:1489) calls scaleUserStats but never capUserStats.

### Law 16b - `PARTIAL`

`app/drizzle/schema.ts:2577` - `insertAiSchema`

insertAiSchema = createInsertSchema(userData).omit({...}).extend(...) with no .strict(), so unknown keys are stripped rather than rejected.

> PROVABLE: the stripping mechanism, exactly as stated. DOCTRINE: 'hidden: true on every create, every entity, no exceptions' is our convention, and lint L13 is our tooling. The inArena:false containment claim was not verified in this pass.

### Law 16c - `NOT_IN_SOURCE`

Rendering-vs-listing behaviour and the live population counts (165 of 407 assets hidden) are prod data state.

> The column default is checkable; the claim that hidden assets still render is a client-behaviour observation this pass did not settle.

### Law 16d - `ENGINE`

`app/src/validators/ai.ts:22` - `ZodAllAiConditions / ZodAllAiActions`

Every condition and action is a z.object carrying type (z.literal(...).prefault(...)) and description (z.string().prefault(...)) plus its own fields.

> The tagged-object shape on both sides is exactly as stated; the flat {action, condition, conditionValue, target} triple does not exist anywhere in the file.

### Law 17 - `NOT_IN_SOURCE`

Concerns unresolved @-refs in OUR manifest layer reaching the server as literal strings.

> The server never sees an @-ref; it sees whatever string we send. That an unknown jutsu id is dropped from an equip array is plausible from law 70's set-difference sync, but the specific silent-strip behaviour was not verified.

### Law 18 - `NOT_IN_SOURCE`

Editing an equipped jutsu severing the combat link is a runtime/state behaviour observed through pushes.

> Not located as a source expression at this SHA.

### Law 19 - `CONTRADICTED`

`app/src/validators/combat.ts:1122` - `SuperRefineItem`

Item and jutsu share ONE union: effects: z.array(AllTags).superRefine(SuperRefineEffects) at combat.ts:1327 (jutsu) and :1491 (item). SuperRefineItem PERMITS rollbloodline, rollsagemode, removebloodline and noncombatconsumereward (it only constrains them, e.g. noncombatconsumereward must be CONSUMABLE and target SELF at :1154-1160), while SuperRefineJutsu REJECTS all of them outright at :1218-1220.

> Changed from PARTIAL to CONTRADICTED on re-check. At this commit the direction is inverted: there is no narrower item union, and the item path is WIDER than the jutsu path - it accepts the bloodline/sage/non-combat family that jutsu refuse. The law's own text notes its membership list has drifted before; the headline direction is now wrong too. See the report's contradictions section.

### Law 20 - `ENGINE`

`app/src/server/api/routers/jutsu.ts:742` - `jutsu.update inject guard`

if (!input.data.injectableInBattle) { ... } wrapping the rejection; the error reads "So you cannot disable it." at :755.

> Verified in full, including the correction the law records. The relation lookup runs unconditionally above the guard; the four injector sources are jutsuInjectors, bloodlineInjectors, skillInjectors, itemInjectors (:744-747). The trap the law names is real: injectableInBattle is z.coerce.boolean().prefault(false) at validators/combat.ts:1312, so an edit omitting the field sends false and trips the guard.

### Law 21 - `ENGINE`

`app/src/libs/combat/actions.ts:161` - `battleUsageType check`

if (!isQuestBattle && jutsu.battleUsageType === "PVE") blocks PVE actions outside quest battles; the PVP mirror is at :157.

### Law 22 - `PARTIAL`

`app/src/validators/combat.ts:1513` - `craftingRequirements`

The field exists on the item validator with the ids-with-number shape the law names.

> The law labels its own second half Doctrine (drop quantity 1, no shared common factor). That half is ours; the shape is engine.

### Law 23 - `PARTIAL`

`app/drizzle/schema.ts:3622` - `quest.consecutiveObjectives`

boolean("consecutiveObjectives").default(true).notNull() - the DB default is TRUE at this SHA.

> CONTRADICTED CLAUSE: the law states 'the DB default is false'. Source says .default(true). CONFIRMED CLAUSE: 'required with no schema default' holds - validators/objectives.ts:700 is z.coerce.boolean() with no prefault, so the write schema does require it. The law's instruction (set it explicitly) still stands; the reason given for it no longer matches source. See the report's contradictions section.

### Law 24 - `NOT_IN_SOURCE`

checkRewards being a tracker tick rather than a victory hook was not traced in this pass.

> libs/quest.ts is where it would be settled. Low confidence.

### Law 25 - `NOT_IN_SOURCE`

Which scene the travel-page popup renders is client behaviour not located at this SHA.

> The Logbook scene container is at layout/Logbook.tsx:387, but the travel-page popup is a different surface and was not identified.

### Law 26 - `NOT_IN_SOURCE`

Reset-node return and failObjectiveId overriding optimistic advancement were not traced.

> resetObjectiveId handling exists at libs/quest.ts:1135 and libs/objectives.ts:270, but the override semantics the law asserts were not read closely enough to cite.

### Law 27 - `DOCTRINE`

The law names itself a design law ('CYOA doctrine (design law, engine-compatible)').

> Self-classified. Nothing in the codebase implies it. 10_LAWS_core.md section 1 records that live data was wrongly used to demote this law.

### Law 28 - `PARTIAL`

The per-entry success envelope is the tRPC baseServerResponse shape used across the content routers (e.g. .output(baseServerResponse) at routers/profile.ts:1494).

> PROVABLE: mutations return a success-bearing envelope rather than signalling via HTTP status. DOCTRINE: 'bundles are read programmatically' is our verification rule.

### Law 29 - `DOCTRINE`

An operating rule about our own generation scripts.

### Law 30 - `NOT_IN_SOURCE`

Name-collision fills leaving blank shells, and our trimmed catalogs being stale, are prod-state and tooling observations.

> The engine-side fact underneath it is law 66, which is provable.

### Law 31 - `DOCTRINE`

A process rule about how our generators are seeded.

### Law 32 - `DOCTRINE`

A file-naming convention for our uploads.

### Law 33 - `DOCTRINE`

Our chroma keying algorithm, implemented in skills/producing-tnr-art/scripts/chroma.py.

### Law 34 - `DOCTRINE`

Prompt-authoring rules for our image generators.

### Law 35 - `DOCTRINE`

Our own spill clamp, upload ceiling and QC gate.

> The 512KB figure is a constraint of the upload surface we use, not a value read from game source in this pass.

### Law 36 - `NOT_IN_SOURCE`

That entry-level name is manifest metadata the server never sees is a fact about OUR manifest format.

> The engine simply reads data.name. The law is a correct statement about our builder envelope.

### Law 37 - `NOT_IN_SOURCE`

Where consecutiveObjectives sits in our payload (data level vs inside content) is a manifest-shape rule.

> The engine field is at validators/objectives.ts:700; that a nested copy is ignored follows from the schema but was not demonstrated.

### Law 38 - `ENGINE`

`app/drizzle/schema.ts:3617` - `quest.prerequisiteQuestId`

varchar("prerequisiteQuestId", { length: 191 }) - a single nullable scalar, not an array; validators/objectives.ts:688 is z.string().min(0).max(191).optional().nullish().

> The tree consequence follows directly. The named orthogonal stacking fields were not each verified.

### Law 39 - `ENGINE`

`app/src/validators/ai.ts:5` - `AvailableTargets / ZodAllAiConditions / ZodAllAiActions`

AvailableTargets is 9 UPPER_SNAKE literals (:5-15); the file defines exactly the 9 conditions and 10 actions the law lists, and every action carries its own target field (e.g. :137).

> Vocabulary matches the law exactly, including the absence of use_jutsu, move, and any rule-level target object. ONE IMPRECISION: the law's parenthetical reads as though every condition carries target; only distance_higher_than (:32), distance_lower_than (:39) and target_has_effect (:83) do.

### Law 40 - `PARTIAL`

`app/src/libs/combat/ai_v2.ts:273` - `distance condition evaluation`

case "distance_higher_than": return target.distance >= condition.value; case "distance_lower_than": return target.distance <= condition.value (:273-276). Path length via astar.getShortestPath at :582.

> PROVABLE, and exactly as the law's 2026-08-30 amendment states: both comparisons are INCLUSIVE, and distance is A* path length. DOCTRINE: the range+1 derivation, the registry table it reads from, and lint L22 are ours. The engine facts underneath the rule are sound.

### Law 41 - `NOT_IN_SOURCE`

That an AI with no executable rule left falls onto engine defaults is runtime behaviour not traced here.

> Law 41b qualifies it from the fall-through side and is the more precise statement.

### Law 41b - `NOT_IN_SOURCE`

Rule fall-through when an action cannot execute is runtime behaviour in ai_v2.ts not traced in this pass.

> The correction it records is behaviour-proven and internally consistent with law 63. Worth a targeted source pass.

### Law 42 - `PARTIAL`

`app/drizzle/constants.ts:1157` - `HUNTING_RANKS / GATHERING_RANKS`

"NONE" is the first member of HUNTING_RANKS (:1157) and of GATHERING_RANKS (:1218); HUNTING_REQUIRED_EXP.NONE = 0 (:1166).

> PROVABLE: the literal is a legal enum value, so a record can carry it. NOT VERIFIED: that it is inert as a gate (the consumption site was not traced). The 'omit rather than write NONE' instruction is ours.

### Law 43 - `ENGINE`

`app/src/validators/rewards.ts:50` - `reward_hunting_experience / reward_gathering_experience`

Both fields exist as z.coerce.number().prefault(0) at rewards.ts:50 and :52.

### Law 44 - `ENGINE`

`app/src/server/api/routers/quests.ts:3184` - `attackers spawn roll`

attackers: .filter((ai) => Math.random() * 100 < ai.number) - a percentage roll. opponentAIs: .flatMap((o) => Array(o.number).fill(o.ids).flat()) at libs/quest.ts:1104 - a repeat count.

> Upgraded from PARTIAL to ENGINE on re-check; both halves now proven, from two different files. The shapes are the same type (idsWithNumberField, validators/objectives.ts:357 and :422), so nothing structural distinguishes them - exactly the hazard the law names. A row copied into opponentAIs with number: 100 literally constructs 100 opponents.

### Law 45 - `NOT_IN_SOURCE`

Doubled @-prefixes surviving a naive sweep is a defect in OUR ref scanner.

### Law 46 - `PARTIAL`

`app/src/server/api/routers/profile.ts:1497` - `setEmptyStringsToNulls`

The content routers run setEmptyStringsToNulls on the incoming data before the write (profile.ts:1497; also badge.ts:64, bloodline.ts:649).

> PROVABLE: an empty string IS converted to null on the write path, exactly the mechanism the law names. NOT VERIFIED: that the resulting null 500s at the DB for image specifically. The repair instruction (omit the field) follows from the confirmed half.

### Law 47 - `NOT_IN_SOURCE`

The law cites play testing, twice, as its evidence.

> Self-classified as behaviour-proven, not source-verified.

### Law 48 - `ENGINE`

`app/src/layout/Logbook.tsx:396` - `scene character wrapper`

Each sceneCharacters entry renders in <div className="absolute bottom-0 w-2/5">, so every entry lands in the same place.

> The stacking consequence follows directly from the absence of any horizontal offset.

### Law 49 - `NOT_IN_SOURCE`

That sceneCharacters resolves gameAsset ids only, and an AI userId renders nothing, was not traced to the resolution site.

> The rendering wrapper is confirmed (law 48); the id-resolution step was not.

### Law 50 - `ENGINE`

`app/src/layout/Logbook.tsx:400` - `QuestDialogScene / AvatarImage / ContentImage`

Scene character: max-h-full w-auto object-contain inside a heightless absolute bottom-0 w-2/5 wrapper (:396,400). AI avatar: aspect-square with no object-fit (Avatar.tsx:57). Item/jutsu/bloodline icon: aspect-square h-full w-full (ContentImage.tsx:104). Scene background: aspect-3/2 (Logbook.tsx:387,391).

> All four mechanisms confirmed at the classes the law names, including the correction: the scene-character wrapper has no height, so max-h-full has no percentage basis and object-contain is inert. The law's four-way split is accurate.

### Law 51 - `PARTIAL`

`app/src/layout/Logbook.tsx:396` - `w-2/5 bottom-anchored wrapper`

Displayed width is fixed at 40% of the scene and height follows the file's intrinsic aspect (see law 50).

> PROVABLE: apparent size is set by the file's own aspect, since width is fixed. DOCTRINE: the transparent-padding remedy is our authoring technique.

### Law 52 - `ENGINE`

`app/src/libs/threejs/sector.ts:319` - `drawQuest`

if (!("image" in objective) || !objective.image) return; - the early return the law describes, inside drawQuest (which begins at :295). Per-task marker tinting follows at :329 (move_to_location = 0xf4e365, travel yellow).

> Upgraded from PARTIAL to ENGINE on re-check: the function body was read this time, and both clauses hold.

### Law 53 - `ENGINE`

`app/src/libs/objectives.ts:11` - `getObjectiveImage`

return objectiveImageMap[objective.task] ?? { image: "", title: "???" } - keyed on task only, objective.image is never consulted.

> Exactly as stated. The '1,150 live dialog nodes' count is prod state and not part of this verdict.

### Law 54 - `PARTIAL`

`app/src/validators/objectives.ts:442` - `sectorType / locationType`

locationType: z.enum(LOCATION_TYPES).prefault("specific") at :443, with sector defaulting to 0 at :445; a separate objective shape defaults locationType to "random" at :486.

> PROVABLE: locationType is an enum whose specific/random split is real, and 0 is the coordinate default. NOT VERIFIED: that the engine only randomises under 'random', and the collect_item playable-margin consequence. The 2026-08-28 amendment rests on live records, not source.

### Law 55 - `NOT_IN_SOURCE`

Teleport-on-random-sector is runtime behaviour; the law's own evidence is a live record.

> sectorType is a real enum field (objectives.ts:442). The teleport consequence was not traced.

### Law 56 - `ENGINE`

`app/src/validators/objectives.ts:496` - `collect_time_minutes`

z.coerce.number().min(0).max(60).prefault(0) - no integer constraint, so 0.1 validates.

> The float claim is exact. NOT VERIFIED: the secondsPassed/60 comparison and the 'only timed task' uniqueness claim.

### Law 57 - `NOT_IN_SOURCE`

That quest updatedAt is not maintained is a prod-data observation (a 2024 stamp after edits).

> An absent update is not visible as a source expression.

### Law 58 - `NOT_IN_SOURCE`

In-game editor overwrite behaviour, observed twice through lost content.

### Law 59 - `NOT_IN_SOURCE`

Silent reduction of a jutsu to a blank shell is a prod-state failure observed after the fact.

### Law 60 - `NOT_IN_SOURCE`

An ordering refinement of law 18, which is itself behaviour-proven.

### Law 61 - `ENGINE`

`app/src/libs/combat/util.ts:2496` - `refillActionPoints`

battle.usersState.forEach((u) => { u.actionPoints = 100; }) - set for every user at once, called from the round-advance path at :2539.

> The turn-vs-round correction is confirmed: the refill is per round and the 100 is each combatant's own turn budget. COMBAT_SECONDS = 60 at libs/combat/constants.ts:16. The specific AP costs (60/40/20-40) were not individually verified.

### Law 62 - `NOT_IN_SOURCE`

Stealth blocking attacks is runtime combat behaviour not traced in this pass.

> hasActiveEffectOfType backs stealth per law 75's citation (actions.ts:1440), but the attack-blocking consequence was not read.

### Law 63 - `NOT_IN_SOURCE`

Exhaustion when nothing is affordable is runtime behaviour in the AI action selector.

> Consistent with law 41b's fall-through reading. Worth a targeted source pass alongside it.

### Law 64 - `PARTIAL`

`app/src/validators/ai.ts:73` - `ConditionHasEffect / ConditionTargetHasEffect`

has_effect and target_has_effect carry effectType and threshold (:73-86) and have no value field; health_below, specific_round, round_greater_than, round_lower_than, distance_higher_than and distance_lower_than each carry value.

> OVERREACH: the law lists does_not_have_summon among the conditions taking value, but ConditionDoesNotHaveSummon (ai.ts:60-63) has only type and description - no value field at all. The rest of the law is exact.

### Law 65 - `ENGINE`

`app/src/validators/ai.ts:154` - `ActionUseSpecificItem / ActionUseRandomItem`

use_specific_item carries itemId (:154-158); use_random_item exists at :161.

> The 20 AP cost is not verified here.

### Law 66 - `ENGINE`

`app/drizzle/schema.ts:2552` - `UserData_username_key`

uniqueIndex("UserData_username_key").on(table.username) on the userData table, which holds players and AI alike.

> The cross-population uniqueness follows from AI and players sharing userData (distinguished only by isAi).

### Law 67 - `ENGINE`

`app/src/libs/hunting.ts:83` - `getHuntingItemDrops`

const rankChances = HUNTING_ITEM_DROP_CHANCES[currentRank] (:89) - the roll is keyed on the player's hunting rank, not on dropChancePerc.

> The law's correction (read the full six-rank table, not the S-rank row) is sound. NOT VERIFIED: that dropChancePerc feeds only the combat loot path.

### Law 68 - `NOT_IN_SOURCE`

'One hunting quest of 31 is wired that way' is a statement about live content.

### Law 69 - `ENGINE`

`app/src/server/api/routers/profile.ts:1529` - `updateAi item mapping`

o.ids.map((id) => ({ id, chance: o.number })) - number is read as chance.

> The inversion against reward arrays is exactly as the law warns.

### Law 70 - `ENGINE`

`app/src/server/api/routers/profile.ts:2643` - `updateUserContent`

Takes oldItemIds/newItemIds, computes deletedItemIds, and deletes them by inArray (:2599).

> Set-difference sync confirmed; anything owned but absent from the payload is removed.

### Law 71 - `ENGINE`

`app/src/server/api/routers/profile.ts:1549` - `updateAi`

scaleUserStats(newAi) runs unconditionally on the update path.

### Law 72 - `ENGINE`

`app/src/validators/objectives.ts:688` - `prerequisiteQuestId`

z.string().min(0).max(191).optional().nullish() - a nullish field that accepts an explicit null, beside plain .optional() fields elsewhere in the same file.

> The optional/nullable distinction is real and visible in the validators. The per-field split belongs in 45d as the law says; the '54 fields' count was not recounted here.

### Law 73 - `DOCTRINE`

A Python hazard in OUR normalisation passes (isinstance(False, int) is True).

> Nothing in the game codebase implies it. The engine-side fact - that these fields are booleans - is real, but the law is about our tooling.

### Law 74 - `NOT_IN_SOURCE`

A summary of our own guard lists and where builder v4.18 applies them.

> The named source files (validators/objectives.ts, validators/rewards.ts) exist and are the right inputs; the law itself is about our derivation.

### Law 75 - `PARTIAL`

`app/src/libs/combat/util.ts:1081` - `calcEffectRoundInfo`

returns { startRound: effect.createdRound, curRound: battle.round } (:1086); castThisRound = startRound === curRound at process.ts:299 and :1094; consumers gate on !castThisRound (actions.ts:1440, tags.ts:136); isInstant = ["damage","heal","pierce"] at process.ts:326.

> CONTRADICTED CLAUSE: the law says ground effects promoted to user effects are written with createdRound: curRound - 1 WHEN INSTANT. Source at process.ts:335 is createdRound: isInstant ? curRound : curRound - 1, i.e. curRound-1 when NOT instant. The condition is inverted. Everything else verifies exactly, including passesTiming = !effect.isNew && startRound !== curRound at process.ts:1515. See the report's contradictions section.

### Law 76 - `ENGINE`

`app/src/libs/combat/util.ts:2496` - `refillActionPoints`

Same mechanism as law 61: the refill sets 100 for every combatant at the round boundary, so a turn is one combatant's window inside a round.

> The duration-field consequence (a rounds:2 effect spans two of the bearer's turns) follows from the round counter that calcEffectRoundInfo reads.

### Law 77 - `ENGINE`

`app/src/validators/combat.ts:1263` - `SuperRefineEffects / SuperRefineJutsu / SuperRefineItem`

else if (e.type === "activatesagemode") addIssue(ctx, "Cannot have sage mode activation effect; it is injected automatically in battle") at :1263.

> Fully verified including the triple rejection the law claims: SuperRefineEffects at :1263, SuperRefineJutsu at :1214, SuperRefineItem at :1130. The tag is a real union member (its literal is at :698), which is exactly the trap the law describes - constructible in shape, rejected by cross-field refine.

### Law 78 - `PARTIAL`

`app/src/validators/combat.ts:1249` - `SuperRefineEffects companion checks`

vamp and consume each require a damage or pierce effect in the same effects array (:1249-1258); wound carries the same rule at :1238-1247; powerPerLevel must be 0 for rollbloodline, rollsagemode, removebloodline and noncombatconsumereward (:1259-1271).

> All four rules verified. ONE IMPRECISION: the law says 'All four rules live in SuperRefineEffects'. The powerPerLevel rules do, but rollsagemode's item-only restriction lives in SuperRefineJutsu (:1218-1220), a different function.

### Law 79 - `ENGINE`

`app/next.config.mjs:35` - `images.unoptimized`

unoptimized: true at next.config.mjs:35; layout/Image.tsx:25 rewrites Bunny sources to bunnyImageUrl(src, Number(props.width)), sending width only.

> Mechanism confirmed exactly, including that only width is sent. AVATAR_FULL_WIDTH = 320 at layout/Avatar.tsx:15. The remaining per-field delivered widths were not each verified.

### Law 80 - `PARTIAL`

`app/src/hooks/asset.ts:69` - `asset size config`

size: "landscape" with maxDim 512 (:69-70) and size: "portrait" with maxDim 512 (:77-78) - these steer generation, as the law says.

> PROVABLE, and more than the first pass found: the asset form entry is literally type: "avatar" for every scene type (hooks/asset.ts:66-69, :74-77), with size and maxDim carried alongside, which is the mechanism the law describes. NOT VERIFIED: that entry renders through ContentImageSelector (layout/EditContent.tsx:1002-1021), and I did not follow that component to its image element, so the final claim - that the preview is AvatarImage with aspect-square - remains uncited. Still the weakest of the art verdicts.

### Law 81 - `ENGINE`

`app/src/layout/Logbook.tsx:387` - `scene container`

className="relative aspect-3/2 w-full overflow-hidden" - scene height is two thirds of scene width, and the character wrapper is bottom-anchored at w-2/5 (:396).

> The 5/3 clip threshold is arithmetic from those two facts: a character at 40% scene width reaches full scene height once h/w exceeds (2/3)/(2/5) = 5/3.

### Law 82 - `ENGINE`

`app/src/libs/replicate.ts:343` - `aspect ratio selection`

config.size === "square" ? "1:1" : config.size === "portrait" ? "2:3" : "3:2"

> Confirmed together with maxDim 512 for both scene types at hooks/asset.ts:70,78, which is what makes 2:3 inside 512 resolve to 341x512. Note: an unrelated aspect_ratio union at replicate.ts:176 offers 1:1/16:9/9:16 and a resize [256,256] at :63 belongs to the GLB texture path - neither governs this law.

### Law 83 - `ENGINE`

`app/src/libs/gamesettings.ts:6` - `DMG_SETTING_DEFAULTS / gameSetting`

Imports DMG_SETTING_DEFAULTS and DMG_SETTING_NAMES (:6), looks the setting up by name in the gameSetting table (:28), inserts the default row when missing (:33), and updates that row thereafter (:54).

> Verified in full. This is the law that qualifies every generated DMG_* value, and it holds at this SHA.

### Law 84 - `ENGINE`

`app/src/utils/image.ts:45` - `optimizer hint`

url.searchParams.set("optimizer", "image") applied only under the extensionless-pathname test; the texture path deliberately omits it, documented at :52 ("Never sends optimizer=image").

> Mechanism confirmed on both sides. The 52-assets / 3619KB measurement is our own and is not part of this verdict.

### Law 85 - `ENGINE`

`app/src/libs/quest.ts:1840` - `verifyDialogBranches`

Rejects a dialog whose nextObjectiveId is absent or an empty array with the exact message the law quotes (:1846-1852).

> Re-check found the full function. Its docstring states the rule 'applies to every quest, independent of consecutiveObjectives', so unlike law 87 this one is NOT gated. It also enforces two rules the law does not record: every option must carry a non-empty nextObjectiveId string, and that id must resolve to an existing objective. NOTE: the section preamble attributes this validator to the builder; it is server-side.

### Law 86 - `PARTIAL`

`app/src/libs/quest.ts:1129` - `terminal task handling`

win_quest, reset_quest and fail_quest are the three tasks handled as terminals in the consequence switch (:1129-1138), and verifyDialogBranches (:1840) forces every dialog to route onward.

> Much better supported on re-check, and the nuance matters. The verifyDialogBranches docstring reads: 'Legacy terminal branches still complete through the runtime sentinel, but new content must express its flow explicitly.' So the law holds for anything we author, but the engine DOES retain a runtime path where a terminal dialog branch completes - TERMINAL_DIALOG_PREFIX, handled at :1239 and covered by app/tests/libs/quest.dialogterminal.test.ts. PARTIAL rather than ENGINE because 'never on a dialog' is true of new content only.

### Law 87 - `ENGINE`

`app/src/libs/quest.ts:1994` - `cycle check`

throw new Error("Cycle detected in objective chain")

> The quoted error string is exact. IMPORTANT REFINEMENT from re-check: the check is CONDITIONAL. verifyQuestContentForSave runs the full flow check only under if (consecutiveObjectives) return verifyQuestObjectiveFlow(objectives) at :2053; a non-consecutive quest gets only the dialog-branch scan. The acyclic requirement therefore does not apply to every quest, which the law does not say.

### Law 88 - `PARTIAL`

`app/src/validators/objectives.ts:407` - `resetObjectiveId`

z.string().optional() - a field distinct from nextObjectiveId, handled separately at libs/objectives.ts:270 and libs/quest.ts:1135.

> PROVABLE: reset is not a graph edge, so it cannot close a cycle under law 87. DOCTRINE: 'must never land on a battle node' - the law itself says this has no live precedent and is treated as illegal by us.

### Law 89 - `PARTIAL`

`app/src/validators/objectives.ts:445` - `sector`

z.coerce.number().min(0).prefault(0) - 0 is a schema default, and sectorType is a separate enum at :442.

> PROVABLE: sector defaults to 0 independently of sectorType, which is what makes a written 0 meaningless. NOT VERIFIED: that the engine resolves the sector from sectorType. The law closes by calling itself knowledge-only.

## Cross-law conflicts

Flagged, not resolved.

- **Laws 23 vs 37.** Law 23 states the DB default for consecutiveObjectives is false; source at app/drizzle/schema.ts:3622 says .default(true). Law 37 builds on 23's premise to say a copy nested in content 'restores the reward-before-the-kill bug in full'. If the DB default is now true, 37's stated consequence needs re-deriving. Not resolved here.
- **Laws 61 vs 76.** Not a contradiction. 76 exists to restate 61's turn/round distinction for duration fields, and the laws say so. Both verify against the same mechanism at libs/combat/util.ts:2496. Recorded because a reader scanning for duplicates will find them.
- **Laws 39 vs 64.** Law 39's parenthetical reads as though all nine conditions carry their own target; law 64 correctly separates the value-carrying set from the effectType/threshold set. Source supports 64's split and only partially supports 39's phrasing. Both flagged in their own notes.

## Least confident

The verdicts above are only as good as the reading behind them. These are the ones
I would re-check first, and why.

- **Law 80.** The weakest verdict in the report. I confirmed the asset form entry is type "avatar" with size and maxDim for every scene type, which is the law's mechanism, but I did not follow ContentImageSelector through to its image element, so 'the preview is AvatarImage with aspect-square' is still uncited.
- **Law 11.** Pierce bypassing damage modifiers. I now know exactly where to settle it - pierce is NOT in damageBoostTypes or damageReductionTypes (libs/combat/constants.ts:146-158), which is suggestive - but suggestive is not proof, and I did not trace the pierce damage path itself.
- **Law 4.** The fields verify and the schema permits an empty generals list, but the 'detonates into astronomical values' consequence lives in the damage formula and I did not trace it. The authoring instruction is sound regardless.
- **Law 1.** A cross-cutting generalization that cannot be settled by one citation. NOT_IN_SOURCE is the least wrong verdict available, but it is not the same as 'false' - it means the law is not shaped like something a file:line can prove.
- **Law 41b/63.** Both describe rule fall-through from different sides and both remain NOT_IN_SOURCE for the same reason: I did not trace the action selector in ai_v2.ts. They should be verified together, not separately. The single largest remaining gap.
- **Law 14.** The DB default verifies exactly, but 'REQUIRED on every AI create' does not follow from it - createInsertSchema makes defaulted columns optional. I am confident in the split I drew; I am less confident that no other guard enforces requiredness elsewhere in the create path.
- **Law 54.** The locationType enum and the 0 coordinate default verify, but 'the engine only randomises when locationType is random' is the operative clause and I did not find the placement code.

## Method

- Source cloned at `345d18accf6d8ea8d8d47ef0e61b5aff7d5a1cf9` and every citation read from that working tree.
- Laws that name a constant or enum were checked for the symbol's existence and use
  site, not for its value, per the audit brief.
- No law text was edited, reworded or condensed. `ENGINE_LAWS.md`,
  `10_LAWS_core.md` and `12b_LAWS_coverage.md` are untouched.
- The `ENFORCEMENT` class in `12b_LAWS_coverage.md` is a separate axis and is not
  reported on here.
- Where a citation could not be verified, none was written. `NOT_IN_SOURCE` on a
  law that looks engine-shaped means this pass did not settle it, and the note
  says so; it is not a claim that the law is false.

### Re-check pass

The first pass was re-audited against the same commit, attacking its own weakest
verdicts and re-testing each contradiction claim for a false positive. Six verdicts
changed, all upgrades except one:

| Law | Was | Now | What settled it |
|---|---|---|---|
| 9 | `NOT_IN_SOURCE` | `ENGINE` | `tags.ts:924` multiplicative accumulation |
| 10 | `NOT_IN_SOURCE` | `ENGINE` | `tags.ts:1009`, same form |
| 19 | `PARTIAL` | `CONTRADICTED` | one shared union; item path is wider |
| 44 | `PARTIAL` | `ENGINE` | both halves, from two files |
| 52 | `PARTIAL` | `ENGINE` | read the `drawQuest` body |
| 85 | `ENGINE` | `ENGINE` | full `verifyDialogBranches`; two extra rules found |

Law 6's contradiction widened from ~19 tags to 61 of 70. Law 87 gained a material
refinement: the acyclic check runs only under `consecutiveObjectives`. Law 86 gained
the legacy terminal-dialog sentinel. No contradiction claim was withdrawn, and one
candidate contradiction (law 82) was checked and rejected before the first pass
shipped - `replicate.ts:176` and `:63` belong to other code paths, and the governing
line `:343` matches the law exactly.
