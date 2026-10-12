# Ghost Ship / Skyglass — results of operator captures push/85 and push/86

**Date:** 2026-10-11. **Author:** Fable (Claude Code). These are read-only capture results. Nothing is written, chosen or tuned here.
**Context:** Stage 2 offline results `docs/reviews/GHOST_SHIP_SKYGLASS_STAGE2_OFFLINE_RESULTS.md` and harness `harness/ghost_ship_stage2/`, both on branch `ccr-71fd390f-0j0g78` (review target `8c19a376b97c4d5099d43e6c7ea9e6eabf057d59`, unchanged). The state packets cited below are on the same branch.

| Run | Bundle | Job | Outcome |
| --- | --- | --- | --- |
| push/85 Legendary Sword baseline | `harvests/inbox/tnr_results_1791727479372.json` | `85-mv3wa2l9`, 2026-10-11T14:04:38Z | DONE / success, 3/3 reads ok and persisted, zero mutations |
| push/86 post-0056 AI recapture | `harvests/inbox/tnr_results_1791727613862.json` | `86-mv3wcul9`, 2026-10-11T14:06:53Z | DONE / success, 22/22 reads ok and persisted, zero mutations |

`harvest.py verify` reports both as capture-only bundles: zero write entries, nothing to verify. Both manifests are archived under `archive/spent-manifests/push-2026-10-11/`.

## 1. push/85 — Legendary Sword baseline (gate C3 input)

All three candidates are full **LEGENDARY / WEAPON / SWORD** records, so all three qualify. The capture chooses nothing. Gate C3 stays **BLOCKED until dauntless accepts exact values**.

| Field | Night's Testament `osJq3k77YPGoFWgof12FQ` | Chakra Sword `oOdkdJixCLy2bW0Gxo5e0` | Masamune `An9G-YkaAonclWsmcpx4E` | Harness carrier (Flaming Sword, EPIC) |
| --- | --- | --- | --- | --- |
| Effects | **Pierce 50** (formula, statTypes None, generals Highest, element **Shadow**, ppl 0) + **immunity buffprevent 2r SELF** | damage 26 (Metal/None) | damage 25 (Metal/None) + seal 55/1r | damage 20 (Fire) + afterburn 20/2r |
| actionCostPerc | 40 | 40 | 40 | 40 |
| cooldown | **6** | 3 | 4 | 4 |
| range / target / method | 4 / OTHER_USER / SINGLE | 3 / OTHER_USER / SINGLE | 3 / OTHER_USER / SINGLE | 4 / OTHER_USER / SINGLE |
| chakra / stamina / health cost | 40 / 40 / 0 | 40 / 40 / 0 | 50 / 50 / 0 | 40 / 40 / 0 |
| per-level cost reducers | 0 / 0 / 0 | 0 / 0 / 0 | **40 / 40** / 0 | 0 / 0 / 0 |
| slot / maxEquips / durability | HAND / 1 / 100 | HAND / 1 / 100 | HAND / 1 / 100 | HAND / 1 / 100 |
| requiredLevel; stat/mastery requirements | 1; all null | 1; all null | 1; all null | 20; legacy columns |
| canBeImbued / maxImbueNumber | **true** / 1 | false / 1 | false / 1 | false / 1 |
| canBeCrafted / craftingExperience | **true** / 2000 | false / 0 | false / 0 | false / 0 |
| canBeTraded | **true** | false | false | false |
| inShop / cost | false / 1 | true / 15,000,000 | true / 10,000,000 | true / 150,000 |
| battleUsageType / hidden / xpToLevel | BOTH / false / 1000 | BOTH / false / 1000 | BOTH / false / 1000 | BOTH / false / 1000 |
| record updatedAt | 2026-10-09 | 2024-03-18 | 2023-11-18 | 2024-02-23 |

Observations for the decision:

- **Night's Testament already carries the Katana's first two approved effects.** It has Pierce 50 (ppl 0) and SELF immunity(buffprevent, 2r). The approved Katana is effectively those two effects plus Consume 40%, with `canBeImbued:false`. Two of its fields contradict the Katana contract or are unselected policy: its Pierce has element **Shadow** (the contract is silent on elements), and it is imbuable, craftable and tradable (the contract requires `canBeImbued:false` and an AI-drop-only source; trading is unselected).
- **Cooldown affects cadence.** With cooldown 6, a Katana swing locks the Katana for 6 rounds. Its Pierce/Consume tags also put other pierce/consume/stun-tag actions on the shared 3-round GCD (harness C2 used the carrier's cooldown 4).
- **Masamune's 40-per-level reducers** take its 50/50 costs to 0 at item level 2 for players. AI users scale on character level.
- **Stored `dmgModifier: 0` is harmless:** all three captured damage/pierce effects store it, and `damageCalc` skips a falsy `dmgModifier`, so 0 behaves like 1.

**Decision needed (dauntless):** choose a baseline record, or a per-field mix, for AP, cooldown, range/target/method, pool and health costs and reducers, slot/durability, requirements, battle usage, and every economy field (cost, shop, craftability, tradability). Also decide whether the Katana's Pierce carries an element. After acceptance, Fable re-runs C2 on the accepted fields and closes C3. The harness's C3 scan assertion ("0 Legendary Swords committed") will also need updating then, because the bundle above now provides three.

## 2. push/86 — post-0056 recapture of the eleven Ghost Ship AIs

| Check (all 11 AIs) | Result |
| --- | --- |
| Live `offence`, `defence`, the four art masteries, bloodline/sage mastery vs the harness's migration-0056 AI-branch conversion of the Oct 1 rows | **Exact match for every AI and every field.** The Stage 2 harness numbers rest on live-equal stats |
| Other numeric profile (level, rank, multipliers, pools, regeneration, generals, preferred generals, elements) | Unchanged |
| `preferredStat` | **Column removed** on live rows (Oct 1 value Bukijutsu for the Captain and Deck Warden). The kit packet's `baselineProfileSummary.preferredStat` is now historical |
| Innate effects (including duplicates) | Identical (SHA-256) |
| Jutsu membership, order, level, equipped | Identical |
| AI profiles (`ai.getAiProfile`, Oct 1 IDs) and profile linkage | Identical; same `aiProfileId` everywhere |
| Regular Captain items | AI Heavy Armor and Cursed Dagger still `equipped:NONE`, drop 1% |
| **Crowned Captain items** | **Changed.** Ghostly Sovereign's Diadem is no longer in inventory. Drop chances: Fragment of the White Crown 1% → **10%**, Cursed Dagger 1% → 0%, AI Heavy Armor 1% → 0%. All still `equipped:NONE`. (The approved design's 20% Skyglass Crown fragment drop is a future write; nothing is changed here.) |
| Embedded jutsu records | Changed **only** in 20 schema columns. Per-type `required*Offence/Defence` were replaced by `required*Mastery`; `bloodlineReskinId`, `reskinParentJutsuId`, `coordinateTargeting` and `elementClassification` were added as null/"None"; `statClassification` changed from `Highest` to `None`. No effect, cost, range, target, cooldown or AP field changed |

**Consequence for the retained-jutsu conversion packet:** `state/ghost_ship_legacy_jutsu_conversion.json` pins `protectedRecordSha256` over the Oct 1 rows. Those hashes **no longer match live** because of the schema columns above, even though no mechanic changed. The fresh protected hashes (same method; every live copy of each ID is identical) are:

| ID | Oct 1 name | Live protected hash | Source pointer (push/86 bundle) |
| --- | --- | --- | --- |
| nCQETf-HNnbRec1OSY2-R | Explosion! | `ef77264288c26b150c02738e82c0b7cd78237ef6025f0c51e9c6042f02985f71` | /captures/2/data/jutsus/0/jutsu |
| ddbIyVtoxdPQwLRXxSBq8 | Ghostly Deep Six | `2d340e93340c5fe7793b5e61fe3f1db2215faa8719e8b3e83caa67f017c4550c` | /captures/10/data/jutsus/2/jutsu |
| X2P22h8ApDmTZHjWpNO87 | Ghostly Final Fathom | `dfc41368c3bdef22f8a1e34c99e194fcfd66e08b530769197f86fc4a1815922a` | /captures/10/data/jutsus/10/jutsu |
| PdD44PGaNv4MN5fOALhAF | Death's Grasp | `1df34aa816a22ddb9dd18a7c8d8fc16071c60dc72fe995a12af5fc921cec4fbd` | /captures/10/data/jutsus/6/jutsu |
| EQ93LX8wvuIAd5u75q_i1 | Ghostly Shipwreck Delusion | `d3afda4866415d16e37e2206d0144ca9ccfcdaf87a5b1350379cd1aad66184af` | /captures/10/data/jutsus/3/jutsu |
| T3glZGcSd-jS8G-NB43GR | Counter Stance | `ed627ce3cc07d9b40e18b9c309a2f40ac11b3bfef300f7ad5da9b9bd3dbdd7b1` | /captures/10/data/jutsus/8/jutsu |
| 0Y10JpChssDwFUxNRk6p3 | Death's Door | `ce8c2eccdfafda0d59ef49ca515729da72038e01e4e15af86f3a4194ed36d090` | /captures/10/data/jutsus/0/jutsu |
| wMcoazoyXaEXViSCn5weF | Ghostly Crossed Out | `0adf972f0d447a47c600169c1051e5ef0cd75cfd3bd73a6f7be342bf5295a9c4` | /captures/6/data/jutsus/7/jutsu |
| 1jXfTgrtGUaSfqTPSSa83 | Ghostly Rigging Snare | `59ed3ebbcf8d52279d10e015a22737609d11d4b45cf06fb81b6ce73d2eaa99d2` | /captures/3/data/jutsus/1/jutsu |
| Jz4Lb55NcpwZn3nUK5PrJ | Ghostly Strangling Weed | `bbf076ae8c6b99561133e6c5d8c63954548cca53ad88180b35b57ce5806db9ad` | /captures/3/data/jutsus/4/jutsu |
| MG9ZujAV8lK7--YxThVbQ | Battle Trance | `dae8c7fc0af8b4a6a85a9a509fc455c347484cff36053be1df70612febbb9bd5` | /captures/9/data/jutsus/2/jutsu |

Any eventual presentation edit must be built from these fresh rows, not from the Oct 1 records. Updating the packet itself, and re-pointing the kit packet and M0 at the fresh bundle, is a separate change for the packet owner. It is not done here, so the frozen review target stays as reviewed.

## 3. Safety record

Agent live-game requests 0, writes 0. Both captures were operator-run, read-only Forge 0.5.0 point reads. No credentials were used or seen. No manifest, engine, art or record changes.
