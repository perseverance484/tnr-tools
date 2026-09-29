# Potency Hidden Arts roster v2 — candidate for review

**Status:** proposal only. No candidate name, selector or unlock below is newly approved by being in this document. No Hidden Arts poster may be generated before dauntless reviews the roster, effects and unlocks.

Governing progression: [design](POTENCY_CHAKRA_MANDALA_V1.md), [graph](POTENCY_CHAKRA_MANDALA_V1_GRAPH.json), RUL-2026-09-29-002. Each school has Skill I and Skill II, each 5 SP / +2.5% Percentage Potency; 10 SP / +5% at completion. These schools are terminal. Neither purchase receives a decorative Seal name.

## Recommended roster: 18 candidates

Eleven elemental teachings preserve complete tag coverage, four Special Element arts add distinct identities, and three paired-specialization arts support medical, drain/absorption and counter-pressure builds. This is a curated roster, not an element-by-tag matrix. Names suggest teachings, but grant no extra mechanics. Identity notes are internal design rationale, not poster prose.

Every listed prerequisite is **Minor / Skill I**. Prerequisites are AND. Total costs below include all recursive prerequisites once, then the Hidden Art purchase(s). Already-owned shared prerequisites are not charged twice.

## Elemental teachings

| Hidden Art | Required Minors | Potency selector | Total SP at I / II | Source gap |
|---|---|---|---:|---|
| **Burning Edge** | Fire + Impact | Fire × Damage | 20 / 25 | None specific to these tags |
| **Cinder Sutra** | Fire + Attrition | Fire × Afterburn | 20 / 25 | None specific to these tags |
| **Riptide Mark** | Water + Pressure | Water × Increase Damage Taken | 20 / 25 | None specific to these tags |
| **Veiled Mending** | Water + Restoration | Water × Heal | 20 / 25 | Elemental healing |
| **Gale Step** | Wind + Momentum | Wind × Increase Damage Given | 20 / 25 | None specific to these tags |
| **Hush Veil** | Wind + Suppression | Wind × Decrease Damage Given | 20 / 25 | None specific to these tags |
| **Stone Body** | Earth + Bulwark | Earth × Decrease Damage Taken | 20 / 25 | None specific to these tags |
| **Rooted Grace** | Earth + Grace | Earth × Increase Heal | 20 / 25 | Elemental healing |
| **Thunder Mirror** | Lightning + Reversal | Lightning × Reflect | 20 / 25 | None specific to these tags |
| **Pulse Thief** | Lightning + Predation | Lightning × Lifesteal | 20 / 25 | None specific to these tags |
| **Hollow Palm** | Earth + Assimilation | Earth × Absorb | 20 / 25 | Absorb support |

## Special Element teachings

| Hidden Art | Required Minors | Potency selector | Total SP at I / II | Source gap |
|---|---|---|---:|---|
| **Glass Lotus** | Crystal + Guard | Crystal × Reflect + Increase Damage Taken | 25 / 30 | None specific to these tags |
| **Black Thread** | Shadow + Sustain | Shadow × Lifesteal + Decrease Damage Given | 25 / 30 | None specific to these tags |
| **Winter Shroud** | Ice + Guard | Ice × Decrease Damage Given + Afterburn | 25 / 30 | None specific to these tags |
| **Furnace Vein** | Lava + Assault | Lava × Afterburn + Lifesteal | 25 / 30 | None specific to these tags |

## Paired-specialization teachings

| Hidden Art | Required Minors | Potency selector | Total SP at I / II | Source gap |
|---|---|---|---:|---|
| **Borrowed Breath** | Restoration + Grace | Any element × Heal + Increase Heal | 20 / 25 | None specific to these tags |
| **Empty Vessel** | Predation + Assimilation | Any element × Lifesteal + Absorb | 20 / 25 | Absorb support |
| **Returning Needle** | Pressure + Reversal | Any element × Increase Damage Taken + Reflect | 25 / 30 | None specific to these tags |

“None specific” means the exact tag selector is supported at the source pin, not that a current live jutsu exists or that the entire tree is implementation-ready. Every elemental selector retains the per-tag versus jutsu-wide distinction in the source audit. Every school also depends on the 30-SP budget implementation.

## Naming and thematic rationale

- **Burning Edge:** A concealed cutting school focused on Fire Damage.
- **Cinder Sutra:** An ember-retention teaching focused on Fire Afterburn. Replaces the previous candidate name **Cinder Doctrine**.
- **Riptide Mark:** A pressure-point marking school focused on Water Increase Damage Taken.
- **Veiled Mending:** A hidden field-medic teaching focused on Water Heal. Replaces the previous candidate name **Healing Current**.
- **Gale Step:** A breath-and-footwork teaching focused on Wind Increase Damage Given; grants no movement. Replaces the previous candidate name **Gale Rhythm**.
- **Hush Veil:** A force-dampening veil teaching focused on Wind Decrease Damage Given; grants no silence or stealth. Replaces the previous candidate name **Quieting Wind**.
- **Stone Body:** A body-conditioning school focused on Earth Decrease Damage Taken.
- **Rooted Grace:** A stabilizing chakra teaching focused on Earth Increase Heal.
- **Thunder Mirror:** A returning-force school focused on Lightning Reflect; Lightning is distinct from Storm. Replaces the previous candidate name **Storm Mirror**.
- **Pulse Thief:** A pulse-siphoning school focused on Lightning Lifesteal; grants no separate theft effect. Replaces the previous candidate name **Predator's Spark**.
- **Hollow Palm:** A receptive palm teaching focused on Earth Absorb.
- **Glass Lotus:** A crystal counter-pressure school strengthening Crystal Reflect and Increase Damage Taken independently.
- **Black Thread:** A concealed draining-and-weakening school strengthening Shadow Lifesteal and Decrease Damage Given independently; grants no tether or stealth.
- **Winter Shroud:** A cold suppression-and-attrition school strengthening Ice Decrease Damage Given and Afterburn independently; grants no freeze or stun.
- **Furnace Vein:** A heat-and-recovery school strengthening Lava Afterburn and Lifesteal independently; damage over time does not automatically trigger extra recovery.
- **Borrowed Breath:** A field-medic school strengthening Heal and Increase Heal independently across all jutsu.
- **Empty Vessel:** A recovery-through-contact school strengthening Lifesteal and Absorb independently across all jutsu.
- **Returning Needle:** A counter-pressure school strengthening Increase Damage Taken and Reflect independently; reflection does not automatically inflict vulnerability.

## Unlock and balance review

1. **Elemental teaching:** Nature I + Discipline I + Specialization I costs 15 SP. Hidden I brings the total to 20; Hidden II to 25. The final 5 SP can broaden the build or deepen a prerequisite.
2. **Special Element teaching:** two Nature I purchases + Special Element I + Discipline I cost 20 SP. Hidden I costs 25 total; Hidden II 30. Requiring a Specialization I on top would make completion cost 35. The proposed direct Discipline gate avoids that unreachable completion without a discount or extra numerical reward. This gate is a proposal for review.
3. **Shared-discipline pair:** Sustain I + two Sustain specializations I costs 15 SP; the completed Hidden Art costs 25. Borrowed Breath and Empty Vessel use this route.
4. **Cross-discipline pair:** Assault I + Guard I + Pressure I + Reversal I costs 20 SP; completed Returning Needle costs 30. It boosts its two tag types independently; it does not attach one to the other.

**Opportunity cost and purpose:** the revised Foundations do not resonate into Special Elements. Fire I + Earth I + Crystal I + Guard I + Glass Lotus II costs 30 SP and gives pure Crystal Reflect **+10%**, Crystal Increase Damage Taken **+7.5%**. Fire/Earth prerequisites still affect only their own elements. Each proposed Special Element art gives +10% to its tag inside the prerequisite Discipline and +7.5% to its tag outside it in the minimal full build.

The first single-tag drafts failed a dominance check: replacing Hidden I/II with Special Element II and Discipline II gave the same focused bonus with wider coverage. The revised two-tag identities deliberately cross disciplines. For example, completing Crystal and Guard gives Crystal Reflect +10% but Crystal Increase Damage Taken +5%; Glass Lotus trades some broad coverage for the additional +2.5% to the latter. This preserves the approved purchase values while giving the school a distinct purpose. The added tags and unlocks remain proposals for review.

**Hidden versus Advanced:** Fire I + Assault I + Impact II + Burning Edge II costs 30 SP and gives Fire Damage +15%, while non-Fire Damage gets +7.5%. Fire II + Assault II + Inferno Doctrine II gives all Fire Assault tags +15% but non-Fire Damage +5%. Hidden investment can favor an exact tag across multiple elements; Advanced investment favors a whole discipline within one element. Upgrading Fire instead of Impact in the first build loses that distinction and is dominated in scope by the Advanced route. Do not market that allocation as an extra-power reward.

**General invariant:** the paired arts use a union of distinct tags, not duplicate contributions to the same tag. A purchased skill can contribute only +2.5% to one effect even if two selected elements match it. Six purchases therefore stay at or below +15%.

## Coverage and holds

- All eleven design-intended tags appear; Absorb has both Hollow Palm and Empty Vessel.
- All five Nature Foundations have an elemental teaching. The four Special Element choices serve different cross-discipline tag pairs; coverage of all fifteen elements is not a quota.
- Veiled Mending and Rooted Grace remain design candidates behind the elemental-healing implementation gap. Hollow Palm and Empty Vessel require Absorb support.
- No Boil, Metal or Sand prerequisite is needed by this draft; their provisional topology does not silently become a Hidden Art dependency.
- No fresh live content census was authorized or performed. Each proposed element/tag intersection requires a repository capture/content-viability check before implementation. Names such as Mark, Step, Veil and Needle do not add debuffs, movement, stealth, weapon restrictions or triggers.
- No three-way prerequisite is added merely for prestige. A proposed triple must still permit both purchases within 30 SP and justify its entry cost under the same +2.5% rule.

## Review gate and subsequent showcase

Review the roster size, renamed legacy candidates, exact selectors, the four Special Element gates and their +10% / +7.5% cross-discipline tradeoff. Keep the two source gaps visible. Final names, unlocks, balance and acceptance remain dauntless's.

After review, prepare exact mechanical card text in the approved dark navy/gold/parchment shell. Do not put identity notes, slogans or invented quotes on cards. Every card shows I and II, 5 SP and +2.5% each, 0/2 investment and +5% at 2/2. A legible multi-sheet treatment is preferable if eighteen cards cannot fit without small text; layout and final art direction are still to be reviewed. No image has been generated for this revision.
