# AI Jutsu Battle Description Update — Re-equip Gate Plan

**Repository:** `perseverance484/tnr-tools`  
**Verified baseline:** `main@8f022fa7a23e9059c7120d3043eab1c5d290c782` (2026-10-20)  
**Workstream:** 82 shared-pool AI jutsu (`32b_DATA_pool.json`)  
**Target manifest:** `ai_jutsu_battle_descriptions_82_backlash_palm_forge.json`  
**Target manifest SHA-256:** `373764377a0e4f9dd898d991d3f255811fc8448280ea14039db6aa5b853ff8c8`  
**Status:** **HOLD — NOT CLEARED FOR LIVE FORGE**  
**Live requests/writes:** 0 / 0  
**Owner of live actions:** dauntless only

## Artifact recovery notice

The previously supplied artifacts had no downloadable backing files; their original bytes could not be retrieved from the conversation file service. These are **replacement files** created to restore working downloads. The roster IDs and effect names were rechecked against the live repository, but **the recreated 81 non-B28 combat-log sentences are not claimed to be byte-identical to the previously approved text**. Only the specific Backlash Palm sentence could be recovered from the conversation. The director must review the reconstructed prose against their intended approved version before release.

## Change boundary

- 82 existing `jutsu` entries, `slot: convert`, with literal IDs and only `battleDescription` updates.
- B28 (`ElSK-RCrLjddEUm76FZrs`) additionally renames **Recoil Slam** to **Backlash Palm**.
- The B28 battle line is: `%user slams a chakra-charged palm into %target, infusing them with unstable energy that lashes back whenever they deal damage.`
- No changes to effects, stats, elemental properties, targeting, cost, cooldown, images or existing AI behavior rules are authored by this manifest.
- `%user` appears in every battle line; targeted jutsu also use `%target`; no exclamation marks.
- The repository still names B28 `Recoil Slam`. Align the shared pool reference with an **operator-verified** successful rename later, through its established owner and workflows, rather than preemptively overwriting source evidence.

## Critical engine safety / order

The documented engine law is **unequip → edit → re-equip**, not edit → re-equip. Updating an equipped jutsu can sever a combat link. The law applies to the whole kit; a later ref to the same jutsu ID does not prove that combat has recovered without read-back and test evidence. See `docs/ENGINE_LAWS.md` laws 18 and 60 and `skills/building-tnr-content/references/jutsu.md`.

### Gate 0 — Source and tooling readiness

- Confirm the operator's installed Forge version and its immutable source pin match the intended loader version.
- Run `python3 scripts/validate.py` against the **exact** recovered manifest using the repository's current (not guessed) 45c / 45d / 45g / 45h and pool data, from the documented skill-data working directory. Record full output, zero errors required.
- Reconcile any current schema drift before allowing AI edit payloads. The repository's `docs/DRIFT.md` records upstream contract drift and should not be treated as automatically adopted.
- Check `profile.getAi`, `profile.updateAi`, `jutsu.get`, `jutsu.update` and Forge capture/update behavior against the pinned effective contracts. The captured rows describe live state; generated contracts describe writable shapes.
- Obtain director confirmation of the **reconstructed** 81 battle descriptions (B28 wording and naming already selected in chat).

### Gate 1 — Complete read-only AI roster / dependency census

- Identify **all currently equipped AI jutsu** that match any of the 82 target IDs. The seed `answers/names_ai.json` contains 532 names, but it does not prove live coverage. `profile.getAllAiNames` must be accounted for; Forge summary list capture alone does not expose the complete IDs. Use an operator-controlled full export/capture or a supported complete source that preserves all roster IDs.
- Fetch full `profile.getAi {userId}` for every candidate AI. Preserve authoritative original fields: userId, username, jutsus ordered IDs, items with drop information, rules and aiProfileId, plus any writable fields required by the current update contract.
- Verify no ambiguous duplicate names / ID collisions or stale records. Use IDs for all mappings; do not equate two characters with the same name.
- Produce a deterministic `affected_ai[]` inventory with `aiId`, `originalJutsuIds`, `affectedJutsuIds`, `originalItems`, `rulesRef`, source capture key/hash, and inclusion justification. A missing complete census is **BLOCKING**, not a warning.

### Gate 2 — Backup and pre-change checks

- Archive immutable full-record captures of all 82 jutsu and every affected AI/profile. Confirm capture completeness and hashes; zero unverified reads.
- Compare affected AI jutsu IDs and item relationships against their original full captures. Detect missing or unexpected kit links before edits.
- Stage **three independent, validated Forge manifests**, all constructed from captured live records and the current schema. Do not pre-author AI edit rows from seed catalogs.

### Gate 3 — Operator-executed unequip

- In the **first** manifest, unequip only the 82 target jutsu IDs from every affected AI while preserving unrelated equipped jutsu, items, stats, behavior rules and all other writable fields. The concrete update shape is driven by full `profile.getAi` captures and the live validator, not by guessed defaults.
- Explicitly record whether preserving unrelated jutsu during the operation is supported. If not, document and approve a temporary complete unequip with a guaranteed restoration source.
- Verify each AI's post-unequip list matches the intended temporary set **before** executing the jutsu edit manifest. Any failure or partial success: STOP and reconcile; never blindly replay.

### Gate 4 — Operator-executed jutsu update

- Import `ai_jutsu_battle_descriptions_82_backlash_palm_forge.json` only after Gate 3 is verified.
- Verify each `jutsu.update` returned actual application success and `jutsu.get` read-back matches exactly the intended battle description; B28 name should be `Backlash Palm`.
- If the engine rejects a copied legacy record because its fields have drifted, stop and correct the effective contract or conversion strategy; do not bypass preflight or invent fields.

### Gate 5 — Operator-executed re-equip

- Restore each AI's **original ordered jutsu IDs** from Gate 1, keeping untouched items, stats, rules and the original profile relationship. Use an independently validated manifest.
- Read back every affected AI; compare sorted + ordered relationships (as applicable) against the pre-change inventory. Require no missing kit entries and no unintended extras.
- Verify at least one representative battle per risk class (self-buff, targeted damage, debuff, summon, boss signature) with gameplay-safe operator observation. A successful mutation response is not proof that the jutsu actually fires.

### Gate 6 — Closeout and rollback

- Archive all source snapshots, validation output, exact-SHA manifests, receipts, failed/successful read-backs and any corrections.
- For any failed gate, reconcile **actual persisted state** before retrying. Rollback for a jutsu is a new validated `convert` generated from the preserved original record; never assume a partial run is atomic. Then restore AI equipment from the immutable snapshots.
- Update roster/source registry for the confirmed B28 rename through normal repository ownership, without mutating historical capture records.
- The director alone accepts completion and authorizes any live action or publishing decisions.

## Known constraints / findings

1. **External artifact loss:** earlier generated files could not be downloaded. This recovery manifest is not an exact previously approved byte copy.
2. **Existing pool reference:** code B28 still appears as `Recoil Slam` on current main; the convert changes the live name but does not alter repository registry data.
3. **Source-of-truth split:** a capture is evidence of actual existing AI kits; a generated contract is evidence of allowed shapes.
4. **Version drift:** current schema may differ from the pinned/extracted schema. Disagreements must be surfaced, not blended.
5. **AI census incomplete:** repository examples identify some known AI kit usage, but do not establish all affected enemy IDs. No auto-generated unequip or re-equip manifest is ready.
6. **Official validator NOT_RUN:** scoped structure checks passed locally on the reconstructed file; these are not a substitute for repository `validate.py`.

## Recovered sample and local QC

- Reconstructed manifest: 82 entries, 82 unique 21-character target IDs, every entry scoped to `battleDescription` except B28, which also updates `name`.
- Source pool: `skills/building-tnr-content/data/32b_DATA_pool.json` at `main@8f022fa7`.
- `12/12 local scoped checks passed. Full repo validation: NOT_RUN.
- Live-game requests: 0; writes: 0; credentials: none.
