# Elemental Damage — Godstorm Eclipse three-record capture findings

**Date:** 2026-10-20  
**Status:** CONFIRMED CONFIGURATION DIFFERENCE; player-specific damage magnitude **NOT YET REPRODUCED**  
**Lead:** Content Designer · Supporting lens: Engineering Auditor

| Reference | Exact pin / observation |
| --- | --- |
| Repository | `perseverance484/tnr-tools` |
| Baseline | `main@383ac0f45bc47004a4a8915f4c724c79b35798f3` |
| Capture | `harvests/inbox/tnr_results_1792478135730.json` (blob `cb6f9c66c38a5669b4913061fe7b904895170ff8`) |
| Capture time / tool | `2026-10-20T06:35:35.728Z` · Forge `0.8.0` |
| Source code reviewed | `studie-tech/TheNinjaRPG@b836d6931991c9487952cbc093f24e4b0d89c7bc` |
| Read scope | `item.get` Stormrender, `item.get` Mastered Shūren no Yaiba, `bloodline.get` Godstorm Eclipse |
| Capture completeness | **PASS**: 3/3 `ok:true`, `rows:1`, `persist:"full"`, `persistOk:true`, non-null record body, exact record identities |
| Manifest operations | `push/130_elementaldamage_godstorm_three_record_capture.json`: `items:[]`, exactly three reads, zero writes |
| Local runtime tests | **NOT RUN**; source and actual committed full captures inspected |
| Review live requests/writes | **0/0** (operator executed Forge capture; not performed by ChatGPT) |
| Credentials | None |

## Verdict

The captured content establishes a **material, independently sufficient configuration difference** between the weapons. **Stormrender has no stat or general selectors on its 30-EP formula damage**, whereas **Mastered Shūren no Yaiba has both `statTypes:["Highest"]` and `generalTypes:["Highest"]`** on its 30-EP formula damage. That makes the two weapons' base damage formulas different even if they receive identical Godstorm bloodline boosts.

This is a **strong source-backed explanation** for the complaint on a stronger player, but its actual contribution and size for the named player's fights are not behavior-proven without their controlled combat logs/stat context. In unusual attacker/defender matchups the advantage term can be ≤1, so do not assert a universal minimum penalty.

## F1 — Godstorm Fire boost is compatible with resolved Elemental Damage

**EVIDENCE: capture + game source; previous Shadow/Storm-only theory is disproven for the actual bloodline.**

The full `bloodline.get` record for Godstorm Eclipse (`szai-IgtB7PLubojIIlh-`) contains **one** inherent damage effect:

```json
{
  "type": "increasedamagegiven",
  "power": 25,
  "powerPerLevel": 0.15,
  "calculation": "percentage",
  "target": "SELF",
  "elements": ["Fire", "Lightning", "None", "Shadow", "Storm", "Water", "Wind"],
  "statTypes": [],
  "generalTypes": []
}
```

At player level 100, its effective bonus is **25 + (100 × 0.15) = 40%**. Crucially, **Fire is explicitly included**, so the director's new report is consistent with the record. A correctly saved Fire preference produces `damage.elements:["Fire"]` from `elementaldamage`. This matches the same Godstorm effect as the old manually tagged `damage` weapon (which also includes Fire). Multiple matching elements of **this single modifier row** do **not** multiply that same row repeatedly: the ratio is a yes/no match for the row.

Relevant source:
- [preferred-element resolution](https://github.com/studie-tech/TheNinjaRPG/blob/b836d6931991c9487952cbc093f24e4b0d89c7bc/app/src/libs/combat/elementalDamage.ts#L7-L31)
- [bloodline realization with player level](https://github.com/studie-tech/TheNinjaRPG/blob/b836d6931991c9487952cbc093f24e4b0d89c7bc/app/src/server/api/routers/combat.ts#L4525-L4545)
- [effective power formula](https://github.com/studie-tech/TheNinjaRPG/blob/b836d6931991c9487952cbc093f24e4b0d89c7bc/app/src/libs/combat/power.ts#L3-L7)
- [element match](https://github.com/studie-tech/TheNinjaRPG/blob/b836d6931991c9487952cbc093f24e4b0d89c7bc/app/src/libs/combat/tags.ts#L3459-L3467)
- [bloodline percentage multiplication](https://github.com/studie-tech/TheNinjaRPG/blob/b836d6931991c9487952cbc093f24e4b0d89c7bc/app/src/libs/combat/process.ts#L2211-L2218)

**Conditional limitation:** The reviewed source does not prove that the reported player's Fire selection was saved and snapshotted in the *relevant* fight. Ranked PvP replaces normal bloodline effects; seals can suppress applicable modifiers. Those remain independent combat-state questions.

**Correction to earlier investigation:** The Bloodright *design proposal* classifies Godstorm Eclipse as Shadow + Storm, but that is not the operative inherent `bloodline.effects` row. The captured row has Fire (and five other elements plus None). Earlier speculation that this case could never match Fire was incorrect.

## F2 — Weapon formula selectors materially differ

**EVIDENCE: both full `item.get` records + source.**

| Field | Stormrender | Mastered Shūren no Yaiba |
| --- | --- | --- |
| ID | `cLXXf8RJv5l9B_gGsYN2a` | `DfV_RZr-4mSvuS1E452aj` |
| Captured rarity | EPIC | LEGENDARY |
| Damage type | `elementaldamage` | `damage` |
| Damage power | `30` | `30` |
| Damage calculation | `formula` | `formula` |
| `statTypes` | **Absent** | `["Highest"]` |
| `generalTypes` | **Absent** | `["Highest"]` |
| `elements` on authored damage | Absent by design (resolves to preference, e.g. Fire) | `["Earth","Fire","Lightning","None","Water","Wind"]` |
| `allowBloodlineDamageIncrease` | `true` | `true` |
| `dmgModifier` | `0` | `0` |
| AP, cooldown, range, costs | 40 AP, 6 cooldown, range 4, 40 CP + 40 SP | **Identical** |

The engine's [`damageCalc`](https://github.com/studie-tech/TheNinjaRPG/blob/b836d6931991c9487952cbc093f24e4b0d89c7bc/app/src/libs/combat/tags.ts#L1398-L1484) sets offence/defence contribution **only if the damage tag has a non-empty `statTypes` array**; it includes user-vs-target general terms **only for selected `generalTypes`**. If both are missing, calculated attack/defense power stays zero and the formula **sets the advantage multiplier to 1**, independent of offensive stats/generals. The attack still scales through the formula's level-based baseline and 30 EP — it is **not** a literal flat 30-point hit.

Mastered Shūren's `statTypes:["Highest"]` is a legacy raw-content marker mapped to `["None"]` during realization, but the array remains **non-empty**, enabling one offence-vs-defence term. Its `generalTypes:["Highest"]` expands to the player's selected strongest generals and participates in the formula. The `statTypes` marker does not itself dynamically pick a stat.

`elementaldamage` **does not intrinsically remove these selectors**: its validator derives from `DamageTag` while omitting only `elements`; [the resolver](https://github.com/studie-tech/TheNinjaRPG/blob/b836d6931991c9487952cbc093f24e4b0d89c7bc/app/src/libs/combat/elementalDamage.ts#L19-L30) spreads the rest of the authored tag unchanged. The selectors are absent from **Stormrender's captured authored effect**. Whether they were lost during its October 20 edit or deliberately excluded is **not established by this capture**.

**This is currently the leading explanation for the reported lower Stormrender damage, not a demonstrated elemental bloodline boost failure.**

## F3 — Secondary effects also differ; these are not otherwise identical weapons

- **Stormrender:** `increasedamagetaken` **20%** for **2 rounds**, enemy-targeted.
- **Mastered Shūren:** `increasedamagegiven` **15%** for **2 rounds**, self-targeted; **plus** enemy-targeted `increasedamagetaken` **15%** for **2 rounds**.
- Mastered Shūren has **three effect tags**, Stormrender **two**.

The extra self damage boost can change damage on later qualifying hits. Modifier timing must be checked in a controlled battle; do **not** assume that a new buff automatically amplifies the hit that created it.

Both first damage rows include `dmgModifier:0`; current source explicitly skips multiplying by a zero-valued `dmgModifier` because it checks truthiness, so this shared field is **not** why one weapon does zero damage.

## Practical conclusion / next gates

1. **Immediate finding to communicate:** The three full reads succeeded; Godstorm at level 100 boosts **Fire by 40%** when the effect is active and matches, and the source should apply it to `elementaldamage` resolving to Fire.
2. **Do not claim root cause proven by combat:** We have not yet measured the affected player's real attack/defense stats, selected generals, equipment, first vs subsequent hits, target defense, or live damage packet. The current source and content explain why different damage is expected.
3. **Fable offline test (no live requests):** use actual captured effect objects, a level-100 Fire-preference user and Godstorm modifier. Compare base output with secondary riders disabled for (A) Stormrender as captured, (B) Stormrender with only `statTypes:["None"]` and `generalTypes:["Highest"]` added as a local test fixture, (C) Mastered as captured, and (D) Mastered with only the tag replaced by `elementaldamage`, preserving selectors. Confirm that B and D converge with C on same resolved Fire before evaluating secondary riders. Test with and without the bloodline, varied opponent defense, and ranked replacement. No content edits authorized.
4. **Director decision for any eventual live item edit:** Is Stormrender intended to use the same offence + Highest-generals scaling as Mastered Shūren, even though one is captured EPIC and the other LEGENDARY? This is balance/content authority, not an automatically approved repair. A minimal **candidate** if parity is desired is to add non-empty `statTypes` and `generalTypes:["Highest"]` to Stormrender's `elementaldamage` effect while retaining dynamic Fire selection and all other fields. Do not submit a mutation without director approval.
5. **Unresolved if difference persists after parity:** Verify battle start after preference selection, actual equipped item levels, attached crystals/modifiers, target, phase of action, and any backend version differences. A read-only content capture cannot prove a full battle state.
6. TNR Tools' older `45c_DATA_constructors.json` still lacks `elementaldamage`. Refresh via the governed extraction and structural-diff path before preparing a future write manifest; this is separate from diagnosing the captured damage behavior.

**Final classification:** SOURCE-VERIFIED content/configuration differential; likely explanation for complaint, **behavior-level attribution PENDING**. Nothing changed in game; live actions and balance remain director-owned.
