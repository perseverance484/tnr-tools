# `elementaldamage` weapon damage investigation — 2026-10-20

**Status:** SOURCE-VERIFIED SELECTOR/PARITY MECHANISM; live player reproduction **NOT VERIFIED**. This report is an investigation, not an approved change to elemental balance.

| Field | Value |
| --- | --- |
| Review owner | ChatGPT — Content Designer, Engineering Auditor lens |
| TNR Tools baseline | `main@4e674234d0539b7010c34025034330980a38b196` |
| Inspected game source | `studie-tech/TheNinjaRPG@b836d6931991c9487952cbc093f24e4b0d89c7bc` |
| Introduction | `050bc4b6c8a365cce6ab4807caf011c06511c0ac`, 2026-10-19 |
| Game deployment | NOT VERIFIED; upstream branch is not itself evidence of deployed production SHA |
| Player/item captures or paired logs | NONE supplied; symptom reported by director |
| Live requests / writes | **0 / 0** |
| Tests/builds executed | **None** (source, committed tests, and contracts inspected) |
| Credentials | None |

## Finding F1 — Preferred-element selection can remove previously matching bonuses

**Tier: SOURCE-VERIFIED mechanism; observed reports not yet causally tied to specific items.**

The new authored tag is `DamageTag` minus an editable `elements` list. Combat converts it to **ordinary `damage` with exactly one basic element**, selected in this order: (1) actor's saved `preferredDamageElement`; (2) innate `primaryElement` if basic; (3) Fire. It does not infer the strongest element or consult the actor's active trained element, bloodline, secondary element, bonus magnitudes, or target defenses.

- [Validator, tag shape](https://github.com/studie-tech/TheNinjaRPG/blob/b836d6931991c9487952cbc093f24e4b0d89c7bc/app/src/validators/combat.ts#L544-L563)
- [Resolver and fallback](https://github.com/studie-tech/TheNinjaRPG/blob/b836d6931991c9487952cbc093f24e4b0d89c7bc/app/src/libs/combat/elementalDamage.ts#L7-L31)
- [Profile preference interface](https://github.com/studie-tech/TheNinjaRPG/blob/b836d6931991c9487952cbc093f24e4b0d89c7bc/app/src/layout/ProfileEdit.tsx#L724-L784)
- [Battle-start preference snapshot](https://github.com/studie-tech/TheNinjaRPG/blob/b836d6931991c9487952cbc093f24e4b0d89c7bc/app/src/server/api/routers/combat.ts#L4235-L4250)

Damage bonuses and reductions explicitly scoped to elements only apply when they overlap the **resolved damage effect's elements**. An authored manual `damage` list may have more than one element; the dynamic tag has just one. The combat engine therefore permits reduced output when the old list matched buffs that the newly resolved element does not. Potency effects may similarly lose element matches on items. The replacement tag does **not** grant an extra damage boost of its own.

- [Element eligibility in modifier matcher](https://github.com/studie-tech/TheNinjaRPG/blob/b836d6931991c9487952cbc093f24e4b0d89c7bc/app/src/libs/combat/tags.ts#L3441-L3470)
- [Actual damage multiplier pipeline](https://github.com/studie-tech/TheNinjaRPG/blob/b836d6931991c9487952cbc093f24e4b0d89c7bc/app/src/libs/combat/process.ts#L2072-L2233)
- [Potency element matching](https://github.com/studie-tech/TheNinjaRPG/blob/b836d6931991c9487952cbc093f24e4b0d89c7bc/app/src/libs/combat/potency.ts#L79-L125)

### Reproduction scenario derivable from committed source/tests

**Setup:** player innate primary Fire; full Elemental Mastery trained/activated Wind; no saved preferred damage element; otherwise identical weapon rows and battle.

| Item / variant | Resolved damage element(s) | Wind mastery +15% applies? | Illustrative raw packet 1,000 (other modifiers held equal) |
| --- | --- | --- | ---: |
| Prior manual `damage`, `elements:["Wind"]` | Wind | Yes | 1,150 |
| New `elementaldamage` with unset preference | Fire (innate fallback) | No | 1,000 |
| New `elementaldamage` with preference set to Wind | Wind | Yes | 1,150 |

The second result is **150 less**, or **13.04% below** the first result. These are **derived illustrative figures, not a captured player hit**. The 15% constant and the Fire/Wind distinction are explicitly covered by the source and [existing Elemental Mastery test](https://github.com/studie-tech/TheNinjaRPG/blob/b836d6931991c9487952cbc093f24e4b0d89c7bc/app/tests/libs/combat/elementalMastery.test.ts). An activated trained element is intentionally distinct from elements supplied by the innate pair/bloodline, making the default mismatch plausible for affected players.

Additional mismatch scenarios: bloodline element-specific buffs separate from innate primary; previously authored *multiple-element* damage tags matching several bonus sources; previously authored advanced elements such as Ice, which cannot be chosen in the new basic-element-only profile preference.

**Severity:** potentially material player-facing regression/expectation mismatch (15% in demonstrated mastery-only scenario, possibly more with multiple buffs). Do not label a confirmed universal engine damage nerf without matched item/player captures.

## Finding F2 — Basic damage resolver path itself appears sound

**Tier: SOURCE-VERIFIED path; actual paired-weapon parity TEST NOT EXECUTED.**

Weapon items use `userItemToAction`, and both available-action prediction and action insertion resolve `elementaldamage` before potency and normal combat processing. `realizeTag` covers passive sources. The new tag inherits the same power, formula/static mode, stats, generals, level scaling and damage modifiers as `DamageTag`. If both rows have identical fields and the **same single resolved element**, source inspection suggests base hit parity; a reproducible lower result under those controlled conditions would warrant a separate engine defect investigation.

- [Item conversion](https://github.com/studie-tech/TheNinjaRPG/blob/b836d6931991c9487952cbc093f24e4b0d89c7bc/app/src/libs/combat/actions.ts#L746-L789)
- [Available actions resolve per actor](https://github.com/studie-tech/TheNinjaRPG/blob/b836d6931991c9487952cbc093f24e4b0d89c7bc/app/src/libs/combat/actions.ts#L338-L347)
- [Cast resolves before potency](https://github.com/studie-tech/TheNinjaRPG/blob/b836d6931991c9487952cbc093f24e4b0d89c7bc/app/src/libs/combat/actions.ts#L1022-L1033)
- [Passive realization](https://github.com/studie-tech/TheNinjaRPG/blob/b836d6931991c9487952cbc093f24e4b0d89c7bc/app/src/libs/combat/tags.ts#L88-L108)

[Current elemental tag tests](https://github.com/studie-tech/TheNinjaRPG/blob/b836d6931991c9487952cbc093f24e4b0d89c7bc/app/tests/libs/combat/elementalDamage.test.ts) assert preferences, separate actor resolution, snapshotting, potency, sealing and elemental modifier matching on a **jutsu** fixture. They do not establish complete **weapon-versus-weapon damage parity** for equivalent item definitions.

## Finding F3 — TNR Tools' generated effect contract is stale

**Tier: SOURCE-VERIFIED generated-file discrepancy; validator effect on new authoring not executed.**

The existing root `45c_DATA_constructors.json` (`_provenance.extracted: 2026-08-30`, game source drop `bdec2883`) contains `unions.AllTags.damage` but **does not have `unions.AllTags.elementaldamage`**. The root `45g_DATA_checks.json` was extracted 2026-09-09 from that older source drop. Therefore TNR Tools' local authoring contracts do not model the Oct-19 tag, even though the newer game source does. This is a **separate builder/manifest readiness issue** rather than an explanation for already-live weapon combat numbers.

Do not hand-edit generated artifacts. Fable should use the established `schema_extract.py --ctors` / `schema_diff.py --invariants` and diff adoption gate from `docs/00_INDEX.md`; then validate that factories, builder, Forge, and validation agree on the new tag before any authoring/push.

## Proposed offline regression matrix for Fable / upstream engine contributor

1. **Parity positive control:** same level-1 WEAPON, identical `power`, `calculation`, `powerPerLevel`, `statTypes`, `generalTypes`, costs and enemy; legacy `damage.elements=["Wind"]` versus `elementaldamage` with preference Wind; assert equal resolved effects and final damage, both with no buffs and with a Wind IDG.
2. **Default regression scenario:** innate Fire, activated trained Wind, preference null; assert dynamic Fire vs manual Wind and exactly the expected 15% mastery difference, preferably through the actual item-action/packet path.
3. **Configured recovery:** same setup with preference explicitly Wind; assert parity restored.
4. **Multi-element semantics:** manual `["Fire","Wind"]` and separate Fire/Wind bonuses vs dynamic one selected element; document known difference (do **not** silently preserve old multi-buff stacking).
5. **Bloodline and advanced element:** Water-specific buff with innate Fire, advanced-element-only manual damage; confirm supported limitations and expected display.
6. **Payload parity controls:** matching `formula` vs `static` values, `generalTypes:["Highest"]`, item level, potency, target reductions, ranked battle; verify no unrelated field was reset during editor migration.
7. **Rendered behavior:** UI tooltip/battle action preview shows exactly which element is resolved; check profile preference changes take effect only in **new** battles.

The available evidence is sufficient to reproduce the *mechanism* offline but **does not identify the user's specific affected live items**, their saved fields, or deployed SHA. A read-only capture of two compared weapon effect rows, player innate/selected/trained elements and one controlled comparison log would tie the mechanism to the actual complaint. Any production capture/live test is **operator-owned**.

## Decision gate / recommended next step

**Director decision required:** Is `elementaldamage` deliberately a **single selected basic element** (current implementation), or should it dynamically choose the **best eligible element** / mimic **old multi-element coverage**? These choices have different stacking and balance consequences. A narrower possible improvement, subject to approval, is changing only the default when preference is unset (e.g. trained element over innate); that still does not recreate multiple-element or advanced-element behavior and changes intended fallback behavior.

**Immediate operator workaround** (if appropriate to advise affected players): set **Edit Profile → Combat Preferences → Primary damage element** to the intended buffed basic element and enter a new battle. This cannot recreate multi-element stacking or advanced elements.

**Next step:** Fable / engine contributor to implement focused offline parity tests, verify controlled captured examples, and propose the smallest correction after the director rules on selection semantics. ChatGPT can independently review the frozen implementation SHA. Do not modify production, live weapons, or source-of-truth balance rules as part of this read-only investigation.

## Named case / operator capture staged 2026-10-20

The director identified **Stormrender** and **Mastered Shūren no Yaiba** on a player using **Godstorm Eclipse**. These exact identities were resolved from `answers/names_item.json` and the `harvests/seed/41_INDEX_item.json` weapon index, and from `docs/design/bloodright/trees/godstorm_eclipse.json`; the bloodline ID is independently present in the previous read-only capture manifest `push/105_bloodright_reference_capture_batch_2.json`.

| Record | Procedure | ID |
| --- | --- | --- |
| Stormrender | `item.get` | `cLXXf8RJv5l9B_gGsYN2a` |
| Mastered Shūren no Yaiba | `item.get` | `DfV_RZr-4mSvuS1E452aj` |
| Godstorm Eclipse | `bloodline.get` | `szai-IgtB7PLubojIIlh-` |

**Operator-ready candidate:** `push/130_elementaldamage_godstorm_three_record_capture.json`, exactly three `capture.before` calls with `persist:"full"`, no after calls, and `items:[]`. Forge's full-persistence allowlist permits both procedures. Static source-contract/readback checks passed; the complete local Forge `check_manifest.mjs` and Python `validate.py` commands were **not executed** in this connector-only session. The manifest is not a captured result; operator execution remains pending.

The proposed Bloodright tree classifies Godstorm Eclipse as **Shadow + Storm**, but that design classification is **not** proof of the active live bloodline's effects; confirm the `bloodline.get` payload. The item capture must determine which weapon currently carries `damage` vs `elementaldamage`, and compare the full fields (not just the effect type). This capture does **not** record the particular player's `preferredDamageElement`, innate primary/secondary, active Elemental Mastery, other gear, or combat outcomes. Avoid declaring an identified personal damage cause until that evidence is independently supplied.

**Capture acceptance:** after the director runs the manifest in Forge, inspect the exported bundle's three per-call `ok` values, `persistOk`, exact IDs, non-null data and effect arrays. A completed job with missing bodies is NOT a successful full capture. Use `harvest.py` to import the exported bundle; confirm both item objects and the bloodline before making player-specific claims. No game mutation is authorized by this capture manifest.

## Focused follow-up — inherent level-100 bloodline damage bonus (2026-10-20)

**Director hypothesis:** The new tag appears not to receive the user's roughly **+40% elemental Increase Damage Given** inherent bloodline bonus. This figure describes the reported level-100 bloodline mechanic and is **not** a measured result for the particular player. The Forge three-record capture above is still pending.

**Important distinction — source-verified selection mismatch, not confirmed application-engine failure:**

1. `app/src/server/api/routers/combat.ts:4525-4545` realizes non-ranked bloodline effects at the user's **level**, sets `fromType:"bloodline"`, and installs them as preloaded effects.
2. `app/src/libs/combat/power.ts` computes effective power as `power + level * powerPerLevel` (with a cap for percentage effects).
3. `app/src/libs/combat/process.ts:2111-2118` separately processes bloodline percentage boosts and multiplies final damage by `1 + effectivePower/100 * matchRatio` **only when the matcher succeeds**. `app/src/libs/combat/tags.ts:3459-3466` sets `matchRatio=0` if the modifier's non-empty `elements` shares no element with the hit.
4. `app/src/libs/combat/elementalDamage.ts:7-31` resolves `elementaldamage` to a single **basic** element from the saved preference, basic innate primary, or Fire. Neither bloodline effects nor trained elements are consulted. `app/drizzle/constants.ts:1145-1178` identifies `Shadow` and `Storm` as **advanced**, not basic elements; the profile selector only accepts the five basics.
5. The Godstorm Eclipse **proposed Bloodright tree**, `docs/design/bloodright/trees/godstorm_eclipse.json`, classifies it as **Shadow + Storm**. This is design/captured-kit interpretation, **not authoritative evidence of the current inherent bloodline effect's exact `elements` field**. That field must be read from the pending `bloodline.get` snapshot.

**Conditional causal conclusion:** If the live Godstorm Eclipse bloodline's inherent +40% `increasedamagegiven` effect is restricted to `["Shadow","Storm"]`, then `elementaldamage` can **never receive that modifier** through the existing matching implementation, even when the player intentionally changes their saved preference: neither advanced element is selectable. A legacy `damage` effect explicitly tagged `["Storm"]`, `["Shadow"]`, or both can match it. This yields exactly the family of player-reported regressions, without requiring a fault in the percentage-multiplication code.

For a single isolated +40% qualifying bloodline bonus and otherwise identical packets, old matching hit **1,400** versus unmatched dynamic hit **1,000**. That is a **28.57% reduction compared with the boosted old hit**, not a demonstrated player log. Other modifiers and weapon fields could change actual outcomes.

**Falsification:** A dynamic effect with the same element as a basic-element-scoped bloodline bonus should still receive that bonus. Existing upstream `app/tests/libs/combat/elementalDamage.test.ts:136-153` checks precisely that for a basic Wind bloodline modifier and verifies a mismatched Fire bonus is not applied. It **does not** cover an advanced-element bloodline and a legacy manually authored advanced-element weapon side by side. Also compare `allowBloodlineDamageIncrease` (default `true` on both `DamageTag` and its `ElementalDamageTag` derivative).

**Operator capture gates (unchanged):** Run `push/130_elementaldamage_godstorm_three_record_capture.json` through Forge only after merging the open PR. Inspect the actual `bloodline.get.effects` rows, including `type`, `elements`, `power`, `powerPerLevel`, and `calculation`; inspect both `item.get.effects` rows, including power/stat/general/element fields. Do **not** presume which weapon has which tag. For final player attribution, separately compare the anonymous player's saved basic preference, innate primary, active trained element, battle type and controlled hits (do not put private player profile data into a Forge full capture). No live-game requests or writes were made by this review.

**Next offline test request:** Add `Storm + Shadow`-only bloodline `increasedamagegiven` fixture at player level 100 to an explicit manual `damage.elements:["Storm"]` weapon versus `elementaldamage` with every legal `BasicElementName`. First assert **current actual behavior**: legacy hit gets boost; dynamic hit does not. Separately propose selection-semantics remedies as user-owned decisions (advanced-element eligibility vs user selection vs best-of-eligible); do not silently turn a bugfix into a universal free 40% bonus.
