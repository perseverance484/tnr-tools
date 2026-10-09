# AI jutsu 82 — re-equip preparation evidence (HOLD)

Task: complete validation and re-equip preparation for the 82 shared-AI-pool jutsu
battle-description pass, with B28 renamed **Backlash Palm**.

- Base: `main@f0bed7435a554d7dff90f057eee5cc89002c25ab`
- Branch: `claude/ai-jutsu-reequip-validation-7ywxag`
- Live-game requests / writes: **0 / 0**. Credentials: none. Only the operator performs live-game actions.
- Upstream source read (public GitHub clone, not the live game): `studie-tech/TheNinjaRPG@2391975994dbd0095e3bf52644ccc02f3fe6f753` (2026-10-08 20:19 +0200).

## Verdict: HOLD (unchanged)

Three named inputs are not available, so the three edit manifests can't be prepared or validated:

| Input | Status |
|---|---|
| `ai_jutsu_battle_descriptions_82_backlash_palm_forge.json` | **Absent.** Not in the working tree, not in any of the 149 remote branches (tree search of every ref), not in any commit (`git log --all -S'Backlash Palm'` is empty), and not in session uploads. |
| `AI_JUTSU_82_REEQUIP_GATEPLAN.md` | **Absent.** Same search, same result. |
| Operator captures of affected AIs | **Not provided.** Committed captures cover only part of the AI universe (see §3). |

The prior "25/25 PASS; 1 prose advisory" result can't be reproduced or audited without the manifest.
The 82 battle descriptions are authored player-facing content, so they are not regenerated here:
final content acceptance is user-owned (CLAUDE.md §10).

## 1. Official validate.py

`skills/building-tnr-content/scripts/validate.py` is the official validator. It **could not be run on the
named manifest** because that manifest is absent. Other runs:

| Command | Result |
|---|---|
| `python3 skills/building-tnr-content/scripts/selfcheck.py --generated skills/building-tnr-content/data` | `0 errors` (factory 20/20; validate.py consumes 16/16 45g blocks; 3 aiProfile fixtures agree with Forge). Note: `generated source: git:studie-tech/TheNinjaRPG@bdec2883 (2026-08-29)`. |
| `python3 …/validate.py push/80_ai_pool_reequip_census_stage1.json` | `capture-only manifest: 83 read(s), zero mutations` / `0 errors, 0 warnings`, exit 0; `--strict` exit 0 |
| Forge `parseManifest` on the same file | ok, 0 items, 83 before-reads, 82 `persist:"full"` |
| `python3 …/validate.py push/79_wayward_blade_anti_kite_edit.json` (control) | `0 errors, 0 warnings`, exit 0 |

**Blind spot:** validate.py checks against contracts generated at upstream `bdec2883`. Those contracts predate the live
stat-model change (§2). A manifest that sends retired stat keys (`ninjutsuOffence`, `preferredStat`, …) passes
validate.py, and the mismatch only shows up as live verify drift (see §2.3). A validate.py PASS is
therefore **not** sufficient evidence for any AI-touching manifest until the contracts are re-adopted.

## 2. Upstream schema drift

### 2.1 Reproduction
I ran the sentinel pipeline from `.github/workflows/regen_schemas.yml` locally:

- Extracting at `c6c3d33` reproduces `state/schema_sentinel.json` exactly (`no drift vs baseline 2026-10-08T13:23:44Z`).
  This shows the local extraction matches CI.
- Extracting at current `2391975`: invariants `5 union(s), 132 variant(s) audited; 0 error(s)`; sentinel check
  `CHANGED 45_constants`, `CHANGED 45_ctors`, `same 45_entities` → drift.
- Incremental `c6c3d33 → 2391975` is **additive only** (exit 0 on all three): 68 ctor additions (element enums
  on the four damage-given/taken tags), 7 `PotencyTagTypes` additions, 0 entity changes.
  Full output: `reports/ai_jutsu_82_reequip/drift_c6c3d33_vs_2391975_incremental.txt`.

### 2.2 Against the adopted contracts (what validate.py and Forge actually use)
`schema_diff.py diff` exits **1 (BREAKING)** for all three files:

| File | Breaking | Full output |
|---|---|---|
| 45c constructors | 121 | `reports/ai_jutsu_82_reequip/drift_adopted_vs_2391975_ctors.txt` |
| 45d entity schemas | 40 | `reports/ai_jutsu_82_reequip/drift_adopted_vs_2391975_entities.txt` |
| 45e constants | 31 | `reports/ai_jutsu_82_reequip/drift_adopted_vs_2391975_constants.txt` |

The tool caps its display at 60 rows. The retained files re-run its own `cmd_diff` with only that display cap lifted,
and the exit codes above come from the unmodified tool. **Nothing was adopted**, per CLAUDE.md §9.

Relevance to this task:

- **Jutsu edit:** `battleDescription` and `name` are unchanged columns. The adopted 45d still lists
  `required{Nin,Gen,Tai,Buki}jutsu{Offence,Defence}`. Upstream removed those columns and made
  `required*Mastery` (plus Bloodline/Sage) **required**. A jutsu edit is safe only through Forge's fetch-merge
  of the *live* record. Any hand-built full payload derived from 45d is wrong.
- **AI edit (unequip/re-equip):** upstream `userData` collapsed the eight per-type stats into `offence`/`defence`.
  `StatTypes.Highest`, `preferredStat` and the `privateState` per-type members are gone. AIs aren't covered by 45d,
  so validate.py can't see this.

### 2.3 Live evidence that the stat change is deployed
`harvests/inbox/tnr_results_1791510874027.json` (Forge 0.5.0, 2026-10-09T01:54Z, Wayward Blade AI edit) ended
with `verdict: "drift"`. The per-type stats and `preferredStat` came back `sent 100 live undefined`, and
`strength/intelligence/willpower/speed` came back `sent 100 live 1460842.5`. `push/79` was then authored with the new keys.
The live game is therefore on the new stat model, and the repository contracts are not.

## 3. Affected jutsu and AI IDs

**Jutsu (pinned from repo):** the 82 jutsu are the shared AI pool, `32b_DATA_pool.json` (82 records:
B×38, S×24, E×17, A×3; the root and skill-data copies are byte-identical). **B28 is currently `Recoil Slam`,
`ElSK-RCrLjddEUm76FZrs`** (r5, gate 6, cd 5, AP 60, `damage 75`, `recoil 15`). After the live rename is
read back, `32_REGISTRY_shared_ai_pool.md` → `32b_DATA_pool.json` must be regenerated through its own workflow,
not hand-edited.

**AIs: not establishable from repository evidence.** Every committed capture (`harvests/inbox`, `harvests/seed`,
`guide-studio/fixtures`) yields kits for only **56** AIs. Of those, 42 hold at least one pool jutsu, covering 50/82 codes.
**B28 is held by no captured AI.** The AI catalog `answers/names_ai.json` is a 532-row seed snapshot (pre-answers).
Candidate list with capture date and source file: `reports/ai_jutsu_82_reequip/repo_capture_ai_kit_candidates.tsv`.
These are leads only, not the census.

Upstream offers no bulk kit read. `profile.getAllAiNames` returns no kits and **excludes rank ELDER**
(`profile.ts:568-583`), so the census needs a `profile.getAi` read per AI.

### Capture prepared (read-only, for the operator)
`push/80_ai_pool_reequip_census_stage1.json` contains 83 reads and zero mutations:
- `profile.getAllAiNames` → the live AI universe for stage 2;
- `jutsu.get` with `persist:"full"` for all 82 pool jutsu → the **before-image and recovery source** for every record
  the jutsu-edit manifest touches.

Stage 2 is generated from stage-1 results: one `profile.getAi` (`persist:"full"`) per AI, plus ELDER AIs from another
source. It is not written yet because it depends on the stage-1 AI list.

## 4. Upstream `updateAi` semantics that bind the three manifests

From `app/src/server/api/routers/profile.ts` (`updateAi`, `updateUserContent`, `scaleEditedAi`) and
`app/src/libs/profile.ts` (`scaleUserStats`) at `2391975`:

1. **Omitted lists delete.** The kit and items are synced by set difference against
   `input.data.jutsus ?? []` and `input.data.items ?? []`. Forge's `mergeAi`
   (`forge/src/runner/recipes.mjs:90-108`) re-sends live jutsus and items (with `dropChancePerc`) whenever the
   manifest omits them, so an unequip entry must send `jutsus: []` and **must not** send `items`.
   (The old builder's hand payload has no such guarantee, so run these through Forge only.)
2. **Every `updateAi` re-runs stat scaling.** `scaleEditedAi` calls `scaleUserStats(edited, "ai", {reweight})`.
   It resets pools, sets `experience` to the level budget, and redistributes the six combat stats. With unchanged stats
   it is a fixed point only when the stored `experience` already equals `calcLevelRequirements(level) - 500`. An AI
   last saved before the stat migration can be **re-scaled on its first touch**, and the Wayward Blade run shows the
   size of that effect. Re-sending the live record can't guarantee "original stats preserved". Only a before/after
   read-back can show it, per AI.
3. **Masteries are rescaled** by `levelBudget / experience` under the same condition.
4. Every update outdates content proposals for the AI and posts to the content Discord feed. That's
   operator-visible noise across N AIs × 2 calls.

## 5. Manifest set (to prepare after the inputs arrive)

Prepare each as a separate file and validate each separately with validate.py and Forge `parseManifest`.
Run them in strict order (laws 18 and 60: unequip → edit → re-equip; same-run re-equip is not enough):

| # | Manifest | Entries | Must carry | Must not carry |
|---|---|---|---|---|
| A | unequip | 1 `ai` edit per affected AI, `targetId` from stage 2 | `jutsus: <live kit minus the affected pool ids>` (or `[]` if the whole kit is affected) | `items`, `rules`, any stat/level/multiplier key, any retired stat key |
| B | jutsu edit | 82 `jutsu` edits by `targetId` | `battleDescription`; `name: "Backlash Palm"` on B28 only | any other field; any `required*Offence/Defence` key |
| C | re-equip | 1 `ai` edit per affected AI | `jutsus: <exact live kit from stage 2, original order>` | same exclusions as A |

`rules` are excluded throughout, so `ai.updateAiProfile` is never called and AI behaviour stays byte-identical.

## 6. Read-back gates

Every gate compares against the committed stage-1/2 capture (the "before image").

- **G0 — before image committed.** The stage-1 and stage-2 results are harvested and committed before A runs. Each AI
  has the `profile.getAi` full record and the `ai.getAiProfile` rules. Each jutsu has the `jutsu.get` full record.
- **G1 — scaling probe.** Run A on **one** affected AI first. Read back. If any of `offence, defence, strength, speed,
  intelligence, willpower, statsMultiplier, poolsMultiplier, level, experience`, or any mastery moves by more than
  Forge's 0.5 tolerance, **stop**. Stat preservation can't be met by this route, and the decision goes to the user.
- **G2 — after A.** For each AI: kit = before-kit minus the affected ids; item ids and `dropChancePerc` identical;
  stats per G1; rules unchanged; `aiProfileId` unchanged.
- **G3 — after B.** For each jutsu: only `battleDescription` changed (and `name` on B28). Every other field is
  deep-equal to the before image. Forge verify verdict is `ok`, never `drift`.
- **G4 — after C.** For each AI: kit set equals the before-kit; items, stats and rules per G2.
- **G5 — combat link.** For one AI per affected archetype (B28 holders first, if any), the operator runs a battle check
  that a rule naming an edited jutsu fires. A severed link and an inert rule look identical in the log (law 18), so
  check equip first.

## 7. Recovery

| Failure point | Recovery |
|---|---|
| A partial | Re-run C from the before-kits for the AIs already unequipped. B has not run, so the links are re-established on unedited jutsu. |
| G1 or G2 stat movement | Stop. Restoring stats needs an `updateAi` that sends the before-image stats, but that call re-scales too (`reweight: true` if they differ), so exact restoration is **not guaranteed**. This is a user decision; don't attempt it automatically. |
| B partial | Re-push the affected jutsu with `battleDescription`/`name` from the before image, then continue to C. C must run regardless: unequipped AIs are inert. |
| C partial | Resume C for the remaining AIs (Forge journal `resume()` reconciles SENT items first). |
| Items lost | Re-send `items` from the before image as `{ids:[itemId], number: dropChancePerc}` (law 69). |

## 8. Open decisions (user-owned)

1. Re-supply the manifest and gate-plan doc (upload, or commit to a branch). Their 82 descriptions are the
   content under review.
2. Run `push/80` (operator). Stage 2 follows from its results.
3. Re-adopt the 45c/45d/45e contracts through the structural-diff gate before relying on validate.py for AI
   manifests (a separate Lane A task: 192 breaking items).
4. If G1 shows re-scaling, choose: accept re-scaled stats, find a non-`updateAi` equip path, or drop the re-equip.

## 9. Not performed

No live-game, browser or session checks. No contract adoption. No change to validate.py, Forge or `32b`.
Manifests A, B and C are not written. Stage-2 capture is not written. `docs/DRIFT.md` was not touched (the workflow owns it).
