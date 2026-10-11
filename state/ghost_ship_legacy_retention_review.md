# Ghost Ship — selective legacy jutsu retention

**Policy and roster:** APPROVED, `RUL-2026-10-11-001/002`. Keep the eleven legacy jutsu below, including Explosion and six of the awakened/Crowned Captain's seven legacy moves. Retained records receive name/description/battle-description changes only; combat mechanics stay as captured and subsequently verified. Replace genuinely redundant roles with existing shared-pool records.

**Conversion complete for review:** `state/ghost_ship_legacy_jutsu_conversion.json` owns the authored text; `state/ghost_ship_legacy_jutsu_conversion.md` is the readable companion. The director approved this exact eleven-record selection and requested its conversion. Final presentation acceptance, hybrid AI kits, rule arrays and technical freeze remain open. Fable remains implementation owner. No live requests/writes or full write manifest.

**Next design packet:** `state/ghost_ship_hybrid_kit_proposal.md` / `.json` propose exact memberships and shared replacements for all eleven existing enemies. They preserve every original retained/shared membership and explicitly propose adding Rigging Snare/Hollow Timber to Sentinel; those new assignments and substitutions are not automatically approved by this retention ruling.

## Evidence and comparison method

Verified live `main` at `0eb57de20877d266dde666229ae4c68e8fbcf4c0` and design branch at `0dbd54c04f2025a1a652712a9ea6df94e35cf8f5` on 2026-10-11. This proposal follows the local Stage 2 readiness review `407df00a816e77a823ae5c5cad6260ee407c8aae`.

- Full original kits: `harvests/inbox/tnr_results_1790826836406.json`, all 11 Ghost Ship AI captures. **43 distinct equipped jutsu IDs**, of which six already belong to the shared registry and 37 were listed for retirement by the old migration.
- Full pool comparison: all **82 registry IDs** in `skills/building-tnr-content/data/32b_DATA_pool.json`, resolved against full jutsu records in `harvests/inbox/tnr_results_1791583362574.json`. Method, filters and `apReduction` matter; shorthand tags alone are insufficient.
- Crowned Captain has **11 equipped moves: seven legacy plus four already shared**. Recommended retention is six of its seven legacy records. Do not count Counter Stance, Death's Door or Death's Grasp twice because other enemies also use them.
- Comparison distinguishes unique mechanics, unique action-economy combinations, and signature tuning/cadence. A different name or higher plain damage alone does not establish uniqueness. A shared substitute can fill a role without being numerically equivalent; disclose that balance change.
- These are historical captures, not fresh live-state certification. Fresh operator full captures and usage checks remain required before edits.

## Approved eleven

AP/CD/range are captured values, not new tuning. `stun` values below explicitly distinguish its power from AP reduction. Retain the complete original mechanical record, including omitted fields; this summary is not a construction template.

| # | Existing legacy record | Keep rationale and closest pool comparison | AP / CD / range |
| --- | --- | --- | --- |
| 1 | **Explosion!** `nCQETf-HNnbRec1OSY2-R` | ALL-method Pierce 120 (`dmgModifier:2`, `residualModifier:0`), self-destruction and enemy 60-AP reduction for 2 rounds. No global action reproduces the complete hazard. Retain original record; the former new-clone plan is superseded. | 100 / 3 / 5 |
| 2 | **Ghostly Deep Six** `ddbIyVtoxdPQwLRXxSBq8` | A **40-AP** package of DDG40%, IDT40% and healing reduction60%, all 3 rounds. B12 lacks IDT and costs60AP; B13 lacks DDG and adds damage/stat reduction. Preserves the debuff-plus-attack turn. | 40 / 6 / 4 |
| 3 | **Ghostly Final Fathom** `X2P22h8ApDmTZHjWpNO87` | Damage70 + Stun100 with **60 AP reduction/3r** + Seal100/3r. B16 has damage60, **20 AP reduction/2r**, Seal2r and CD10. Retain the awakened signature's actual lockout and cadence. | 60 / 6 / 4 |
| 4 | **Death's Grasp** `PdD44PGaNv4MN5fOALhAF` | Damage50 + Move Prevent100/2r + static Drain505/2r from **Health, Chakra and Stamina**. B15 has no root or Health drain; B05 likewise does not reproduce this package. | 60 / 8 / 5 |
| 5 | **Ghostly Shipwreck Delusion** `EQ93LX8wvuIAd5u75q_i1` | ALL-method Damage72 + Stun100 with 20 AP reduction/2r, **CD3**. B17 has the same broad effect family but CD10. Retention preserves signature cadence, not a novel tag combination. | 60 / 3 / 5 |
| 6 | **Counter Stance** `T3glZGcSd-jS8G-NB43GR` | SELF Reflect35%/2r for **40AP**, allowing a normal attack in the same turn. B34 is a 60AP attack-plus-reflect action; it cannot substitute for that turn structure. Used by Oathkeeper, Sentinel and Crowned Captain. | 40 / 4 / 0 |
| 7 | **Death's Door** `0Y10JpChssDwFUxNRk6p3` | IDG80% + Highest offense Stat30%, 99r. B18 covers the long-duration buff role but changes filters, potency and CD2→6. **Tuning-sensitive retention recommendation**, not a claim that the underlying buff family is absent. Preserves both Captains' ramp identity. | 40 / 2 / 0 |
| 8 | **Ghostly Crossed Out** `wMcoazoyXaEXViSCn5weF` | Metal Damage100 + Seal90/2r, without stun. B16 adds AP reduction; B11 replaces damage with other debuffs. Preserve the narrower suppression tool. | 60 / 4 / 4 |
| 9 | **Ghostly Rigging Snare** `1jXfTgrtGUaSfqTPSSa83` | Damage100 + Move Prevent100/1r. The shared EE02 root attack adds stun/AP reduction and changes duration/cadence. Preserve a simple damaging restraint without that extra control. | 60 / 2 / 4 |
| 10 | **Ghostly Strangling Weed** `Jz4Lb55NcpwZn3nUK5PrJ` | Wood Damage100 + static Drain250/2r from Health/Chakra/Stamina, without the root of Death's Grasp. B05/B15 drain Chakra/Stamina only. Preserve the Core Horror's simpler attrition action. | 60 / 2 / 3 |
| 11 | **Battle Trance** `MG9ZujAV8lK7--YxThVbQ` | A pure SELF Highest-offense Stat25%/2r stance. B20/B38 add a separate IDG effect and broaden the stat/general package. Lower-priority keep if preserving that clean, single-buff role matters. | 40 / 5 / 0 |

Except Explosion and Shipwreck, these actions are SINGLE method; the self stances target SELF and offensive records target OTHER_USER. Keep all original effects, cost fields, selectors, target/friendly-fire flags, modifiers, durations and cooldowns. “Stun100” must never be rewritten as 100 AP reduction.

### Crowned Captain coverage

Retain the six approved legacy records Deep Six, Final Fathom, Death's Grasp, Shipwreck Delusion, Counter Stance and Death's Door. Its seventh legacy record, **Sharpened Focus**, is an ordinary offensive stance suitable for a disclosed shared-pool replacement.

Its other four moves already are shared records: **S31 Unraveling Strike, B14 Cataclysm Detonation, S35 Second Wind, B07 Stolen Form**. They can remain equipped without becoming new legacy exceptions. Do not rename global records as part of event-local retheming.

This retains ten of the current eleven Crowned moves if its current shared actions are retained; that is a proposed kit-preservation outcome, not an approved final rule array. The captured innate IDG60%/99r is separate from the jutsu and is not removed by this proposal.

## Earlier alternatives; not part of the approved eleven

The director accepted the eleven above. These alternatives record the earlier comparison only; substituting them now requires a new decision.

- **Ghostly Sand-Choke** can replace Strangling Weed in the shortlist if Sentinel's Sand identity is the stronger priority: same three-pool250 drain/2r, Sand damage, CD3/range4 instead of Wood/CD2/range3. Keeping both is an elemental/encounter-identity choice, not two independent mechanical discoveries.
- **Ghostly Grasp of the Buried** can replace Rigging Snare if the Sand variant is preferred. It has the same damage/root/cadence with Sand added. Again, do not call both mechanically irreplaceable solely to reach twelve.
- Eleven meets the approximate target. There is no requirement to pad to twelve or give every enemy a retained custom technique.

## Replaceable families and necessary caveats

| Legacy family | Existing pool role | Consequence to disclose |
| --- | --- | --- |
| Plain damage attacks, including Knotted Lash, Cutlass Slash, Grapeshot Volley, Tarred Harpoon and elemental variants | Standard/elemental damage pool | Original 100EP and short cooldowns are not new mechanics. Pool substitution changes damage/cadence and may change elements; compare final kit balance. |
| Boarding Hook / Powder Flash / Undertow Chain | S08 Numbing Shot family | Damage plus chance-based AP reduction exists. Preserve awareness of different AP-reduction values and elements; not exact numerical replacement. |
| Measured Verdict / Thunderhead Brand | S04 Opening Strike family | Damage + IDT exists. S33 is ALL-method in full records and must not silently replace a SINGLE attack. |
| Guarded Stance / Braced Stance / Sharpened Focus | EE03 Stoneward / EW03 Springguard / EA03 Windlash Focus roles | Plain DDT/Absorb/IDG stances are covered. Full effect filters and values differ; elemental names do not establish actual element restrictions. |
| Vault-Breaker | EA04/EL04 pure Pierce family | Plain Pierce exists. B33 adds IDT, so it is not an identical substitute; the numerical reduction must be deliberate. |

Light Barrier (B39), Worldbreaker Chorus (B17), Cataclysm Detonation (B14), Stolen Form (B07), Unraveling Strike (S31), and Second Wind (S35) are the six already-shared IDs in the 43-record inventory. They are neither bespoke duplicates to delete nor newly retained exceptions.

### Redrawn Course is not yet evidence of a functioning unique cooldown mechanic

`Ghostly Redrawn Course` (`yjsfRGaY1rUwG3FUWeHUW`) contains Damage100 Shadow and `increasecooldown:1`, but the captured effect has no `actionsAffected` or `rounds`. At game source `cddd7d91c9e6bdebc978ddcb61e5b8a305bd0f93`, `app/src/validators/combat.ts:365–371` defines selected **basic-action** cooldown adjustment; `app/src/libs/combat/actions.ts:400–414` applies it via `parsed.actionsAffected?.forEach`. With no selected actions, the rider appears inert at that pin. No runtime test was run.

Do not describe this as delaying all jutsu or count it as a proven unique attack. Repair would be a mechanics change, outside the approved rename-only retention policy. Leave it out of the shortlist pending a separate decision if the concept is desired.

## Effect on Stage 2 and implementation ownership

1. The former wholesale shared-pool migration and blanket 37-record retirement plan are superseded. Its numeric AI profiles and loot directives remain evidence/constraints except where later decisions already override them.
2. Retain Explosion's original record; its authored new name is **Core Rupture**, not an instruction to create a duplicate shared jutsu. Renames still need fresh record/dependency checks so other consumers are known.
3. The retained roster is approved. Review its authored presentation text and select per-enemy hybrid kits. Approval to keep a record does not automatically add it to enemies that never used it.
4. Death's Door, Death's Grasp and Battle Trance affect the **regular Captain** too. Fable must freeze that revised comparator before final Sealwright parity. The previous B19/B14/B17/B05/S31/B33 all-shared comparator is now historical, not final authority.
5. Sealwright's seven shared jutsu and intentional double Clear are unchanged. Item packages B/C can continue; compare Sealwright against the newly accepted Captain kit once settled.
6. Retained mechanics must survive field-by-field comparison of before/after records, including absent fields. Do not normalize omitted `generalTypes` or silently repair malformed riders. Existing equip-link edit hazards still require the repository's unequip/edit/re-equip workflow at the eventual user-run implementation stage.
7. “Replace/remove” here means retirement from the Ghost Ship kits. Database deletion remains gated on proof of no external consumers; no deletion manifest is authorized or built by this review.

Names, descriptions and battle text have been converted in `state/ghost_ship_legacy_jutsu_conversion.json` and await final presentation acceptance. That file supersedes `supersededJutsuRetheme` for these eleven IDs. Seal is described according to verified engine semantics, not generic “all techniques disabled” prose.

**Current outcome:** eleven-record roster approved and text conversion authored. Offline replay preserves all non-presentation fields across all eleven records. Final presentation acceptance and revised hybrid AI rules remain open. No live requests/writes, engine changes, art work, remote publication or implementation manifest.
