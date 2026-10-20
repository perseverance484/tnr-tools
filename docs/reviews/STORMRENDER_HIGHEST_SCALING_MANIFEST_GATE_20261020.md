# Stormrender scaling repair — manifest and compatibility gate (2026-10-20)

> **Amended 2026-10-20 (PR #76): the RED tooling blocker below is resolved; the rest of this report stands.** Forge 0.8.1 and the skill contracts are re-derived at `studie-tech/TheNinjaRPG@85cecaebf4ada2e265a18a1405f63c9637443275` (RUL-2026-10-20-001), both now know `elementaldamage`, and on push/131 `node forge/tools/check_manifest.mjs` reports 0 pre-send problems and `validate.py` 0 errors, 0 warnings. See `docs/handoffs/STORMRENDER_FORGE_REPIN_6524D0F.md`. The manifest is unchanged. **Before execution, the operator must still take a fresh capture of Stormrender and confirm its effects have not changed since 2026-10-20 06:35 UTC** (last section below). Merging code does not approve a live run.

**Status:** MANIFEST STAGED / **NOT FOR OPERATOR EXECUTION YET**  
**Lead:** Content Designer; Engineering Auditor review lens  
**Authority:** Director approved an item-specific correction: "Create manifest to add Highest to both fields." No additional balance edits were approved.

| Field | Pin or scope |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Base | `main@383ac0f45bc47004a4a8915f4c724c79b35798f3` |
| Game source validated by inspection | `studie-tech/TheNinjaRPG@6524d0fbd7c0b80ecfd28ca63e9c4becdfb210eb` |
| Last full live capture | `harvests/inbox/tnr_results_1792478135730.json`, blob `cb6f9c66c38a5669b4913061fe7b904895170ff8`, captured 2026-10-20 06:35:35 UTC |
| Target | Stormrender: `cLXXf8RJv5l9B_gGsYN2a`; captured item update stamp `2026-10-20T05:25:50.002Z` |
| Staged manifest | `push/131_stormrender_highest_scaling_suggestion.json` |
| Delivery mode | Forge `mode:"suggest"`: submit one item correction for review, **not a direct live edit** |
| Repo writes | ChatGPT-owned `chatgpt/*` branch only |
| Live requests / live writes | **0 / 0** from ChatGPT; the earlier three-record capture was operator-executed |
| Credentials | None |

## Scope assertion and content preservation

The new manifest's one item asserts only the top-level `data.effects` field. That field contains an exact copy of both captured effect objects, with **only two added fields** on `effects[0]`:

| Subfield | Captured | Staged |
| --- | --- | --- |
| `effects[0].type` | `elementaldamage` | unchanged |
| `effects[0].statTypes` | absent | `["None"]` (source-normalized equivalent of requested Highest) |
| `effects[0].generalTypes` | absent | `["Highest"]` |
| `effects[0].power` | 30 | unchanged |
| `effects[0].calculation` | formula | unchanged |
| `effects[0].allowBloodlineDamageIncrease` | true | unchanged |
| `effects[1]` | 20% `increasedamagetaken` / 2 rounds | byte-equivalent object, unchanged |
| Other item columns | Forge `item.get` live record | unchanged via field-limited fetch-merge |

**Why `statTypes:["None"]` instead of literal `["Highest"]`:** At the latest game-source pin, `app/src/validators/combat.ts:156-169` transforms `Highest` into `None` on parsing the stat selector. The combat `damageCalc` at `app/src/libs/combat/tags.ts:1438-1447` enables the Offence/Defence term when `statTypes` is **nonempty**; the marker's spelling doesn't choose a stat. Source `realizeTag` at `app/src/libs/combat/tags.ts:105-109` also maps older authored `Highest` to `None` at runtime. Thus `["None"]` is the operational equivalent of legacy `["Highest"]`, and avoids a false Forge post-write drift when the server stores canonical `None`. General selector `Highest` is retained literally and dynamically resolves the actor's strongest generals.

**Important:** Captured legacy Mastered Shūren still contains raw `statTypes:["Highest"]`; it is not proof the current server will persist that spelling on a new item update. The new manifest deliberately targets equivalent game *behavior*, not byte-identical legacy raw values.

## Blocking tooling contract discrepancy — **RED**

- Forge `forge/src/runner/nested.json` is generated from game pin `94f9d84c770004172ba423ada3d6710849acc451`. Its `effects` discriminator map **does not contain `elementaldamage`**.
- `forge/src/runner/validate.mjs:210-214` rejects any effect whose type is absent from that map: expected preview/pre-send failure is **`effects[0]: unknown effect type "elementaldamage" at the pin`**.
- `forge/src/core/core.mjs:193-199` performs the same validator check while selecting the manifest. `skipPreflight` is NOT a bypass; it does not suppress this fail-closed nested validation.
- Skill-generated `skills/building-tnr-content/data/45c_DATA_constructors.json` and `45g_DATA_checks.json` are also from old game source and lack this new tag. The required `validate.py` cannot certify this manifest against stale generated shapes.
- **DO NOT** hand-edit generated `nested.json` or `45c/45g`, rename the tag to `damage`, bypass validation, or ask the director to run a known-refused manifest.

**Next Fable-owned tooling gate:** Refresh source-derived effect contracts by the documented extraction, invariants/diff, and Forge derivation workflows, with regression tests for an item edit preserving an existing `elementaldamage` effect and adding `statTypes:["None"]` and `generalTypes:["Highest"]`. Match generated and runtime pinning, and confirm `validate.py` and `node forge/tools/check_manifest.mjs` both pass on the staged manifest **with zero errors**, including any interaction with old generated check tables. Re-test ordinary `damage` with `Highest` and new `elementaldamage` path. Do not include a game mutation in that tooling work.

## Validation and release state

| Check | Result |
| --- | --- |
| Target identity and 2/2 original effects from exact Forge full capture | **PASS** (connector-read evidence) |
| Only two added properties to the original damage effect | **PASS** (programmatic deep-copy/remove-and-compare) |
| No increase to raw power, no changed riders, no item-wide field edits | **PASS** (programmatic assertions) |
| One suggest item, no captures or other mutating entries | **PASS** (programmatic assertions) |
| JSON serialize/parse roundtrip | **PASS** |
| Current pinned Forge nested-discriminator gate | **FAIL** by direct contract and implementation read (expected refusal; browser not executed) |
| Canonical `validate.py` | **NOT RUN** (not zero-error certified; current 45c is stale) |
| Local Forge `check_manifest.mjs` | **NOT RUN** (requires repository runtime checkout; expected nested failure) |
| Browser/production suggested, approved, or updated | **NOT RUN** |

The manifest must remain a **draft/blocked PR** until the two required offline validators pass after governed tooling refresh. A passing Forge suggestion run means the desk received the proposal; actual applied content needs review-approval and a fresh `item.get` verification. Because this manifest replaces the entire `effects` array from a captured snapshot, check that the current Stormrender effects have not changed since 2026-10-20 06:35 UTC before executing; Forge's suggest-time stale protection checks changes *after submission*, not changes between snapshot and submission.

**Operator decision gate:** The exact requested damage-scaling parity is approved, but normal content-review approval and execution remain operator-owned. Nothing about the manifest approves a generalized `elementaldamage` buff or edits other weapons.
