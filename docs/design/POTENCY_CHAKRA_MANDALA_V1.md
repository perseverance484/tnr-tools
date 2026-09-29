# TNR Potency Skill Tree — two-skill design, revision 2

**Status:** the progression and five-category direction below are approved by RUL-2026-09-29-002. Hidden Arts are candidates for review. Advanced Arts retain the existing matrix as a review basis; optional generalists remain deferred. This is a design source, not a live-game manifest.

**Date:** 2026-09-29

**Lead:** Content Designer; supporting lenses: UI/UX Reviewer and, when producing showcases, Art Director / Image Production.

**Working branch:** `chatgpt/potency-chakra-mandala-design-20260929`

**Verified main / merge-base:** `1601f072af839402395eeab1326b1228747e0009`

**Verified branch at session start:** `36bc4cc7aa79321e52f8e90584933d5c747497a7`

**Verified upstream TNR main:** `9f01172038dbc412c837a7f97f7451eb87b6a234`

The historical Mandala/V1 filenames remain stable repository pointers. **The radial Mandala presentation and previous rank progression are superseded.** Use the five card-based categories. Historical versions remain in Git; they are not implementation instructions.

Companions: [design graph](POTENCY_CHAKRA_MANDALA_V1_GRAPH.json), [Hidden Arts review roster](POTENCY_HIDDEN_ARTS_ROSTER_V2.md), [source audit and implementation gaps](POTENCY_SOURCE_AUDIT_2026-09-29.md), and `state/workstreams/potency_skill_tree/roadmap.json`.

## 1. Approved progression

| Purchase | Incremental cost | Incremental Percentage Potency | Investment after purchase | Tier |
|---|---:|---:|---|---|
| Skill I | 5 SP | +2.5% | 1/2; 5 SP; +2.5% total | Minor |
| Skill II, requires I | 5 SP | +2.5% | 2/2; 10 SP; +5% total | Major |

A player has **30 Potency SP**: at most six purchases, or three fully completed schools. No travel purchases and no additional breakpoint Potency bonus exist. Minor/Major denotes investment in every school; a **Seal** label is justified only where that breakpoint unlocks another school. Terminal cards use Skill I / Skill II or reviewed thematic skill names.

Allocation shapes include 3 Major; 2 Major + 2 Minor; 1 Major + 4 Minor; or 6 Minor. These are budget shapes, not permission to skip prerequisites. Every selected allocation must also satisfy the graph, including the Foundation investments needed by downstream schools.

**Invariant:** `30 / 5 = 6 purchases`; `6 × 2.5% = +15%` maximum Potency contribution from this tree to one effect. Every purchased skill matches any one effect at most once. Multiple selected tags are a union of distinct tag types, not multiple bonuses to one tag. Multiple matching elements do not multiply a skill's contribution.

Percentage Potency increases the qualifying tag's power proportionally. A power of 20 with +2.5% Potency becomes 20.5 before relevant engine caps; it does not become 22.5. This is not a promise of the same percentage change in final damage/healing after all other combat systems.

## 2. Selector intent and current engine boundary

- All purchases grant `increasepotency`, `calculation: percentage`, `power: 2.5`, `powerPerLevel: 0`, to SELF. These are design values, not a publishable payload.
- Nature and Special Element schools intend to affect **all Potency-supported tags on jutsu of their exact named element**. Basic Fire does not automatically include Crystal, Lava or other descendants. The former resonance lists are removed.
- Disciplines and Specializations affect their listed tags on all jutsu regardless of element, including non-elemental jutsu.
- Hidden/Advanced intersections require both the element scope and the tag scope. Paired-specialization arts target either listed tag independently; they do not create a new interaction or trigger.
- Upstream percentages from matching modifiers **add**, then multiply tag power. Non-jutsu actions are ignored; Potency is snapshotted on subsequent casts.
- **Source mismatch to resolve:** upstream currently tests each effect tag's `elements`, not a jutsu-wide element. Heal and Increase Heal have no element field and fall back to None. Preserve the approved jutsu-level intent without claiming elemental healing already works. See POT-IMPL-02.
- **Absorb:** approved under Sustain, but absent from upstream `PotencyTagTypes`. Assimilation and all Absorb-oriented paths depend on POT-IMPL-01. The name's presence in other engine enums does not establish Potency support.
- **Budget:** upstream has a global maximum of 100 SP and checks global activated-skill expenditure. It does not enforce this tree's separate 30-SP allocation. POT-IMPL-03 must be resolved before implementation.

The current supported list is Damage, Increase Damage Given, Decrease Damage Given, Increase Damage Taken, Decrease Damage Taken, Afterburn, Lifesteal, Reflect, Increase Heal and Heal. The design adds Absorb to that intended coverage. Static Potency is not used.

## 3. A — Foundation Schools: eight starters

Every Foundation is directly available. Skill I reaches a Minor unlock; Skill II reaches a Major unlock. Every school costs 10 SP and contributes +5% when complete.

| School | Intended scope | Minor opens | Major opens |
|---|---|---|---|
| Fire | All supported tags on Fire jutsu | Relevant Special Elements and reviewed Hidden Arts | Fire Advanced Arts |
| Water | All supported tags on Water jutsu | Relevant Special Elements and reviewed Hidden Arts | Water Advanced Arts |
| Wind | All supported tags on Wind jutsu | Relevant Special Elements and reviewed Hidden Arts | Wind Advanced Arts |
| Earth | All supported tags on Earth jutsu | Relevant Special Elements and reviewed Hidden Arts | Earth Advanced Arts |
| Lightning | All supported tags on Lightning jutsu | Relevant Special Elements and reviewed Hidden Arts | Lightning Advanced Arts |
| Assault | Damage; Increase Damage Given; Increase Damage Taken; Afterburn, any element | Assault Specializations and reviewed direct Hidden gates | Assault Advanced Arts |
| Guard | Decrease Damage Taken; Decrease Damage Given; Reflect, any element | Guard Specializations and reviewed direct Hidden gates | Guard Advanced Arts |
| Sustain | Heal; Increase Heal; Lifesteal; **Absorb**, any element | Sustain Specializations and reviewed direct Hidden gates | Sustain Advanced Arts |

“Opens” means one prerequisite is satisfied; schools with multiple prerequisites require all of them. Absorb remains an upstream support gap.

## 4. B — Special Elements: fifteen schools

Each targets only its exact Special Element and all supported tags under the intended jutsu-element scope. Each has two 5-SP / +2.5% purchases. Standard entry requires exactly two elemental Foundation Minors: 10 SP before buying the school, 15 total at Minor and 20 total at Major.

The enum defines names, **not recipes**. The evidence below preserves the earlier design review; the cited bloodline examples are carried research, not a fresh live census or proof of universal elemental laws. This session's limited upstream seed check did not resolve the provisional mappings; see the source audit.

| School | Required Foundation Minors | Evidence / decision status |
|---|---|---|
| Ice | Water + Wind | Prior element-array evidence: Teno Yuki / Hyouga Yui |
| Crystal | Fire + Earth | Prior element-array evidence: Sea-Maiden's Kiss |
| Dust | Wind + Earth | Prior element-array evidence: Aerathiel / Windborne Priestess Legacy |
| Shadow | Fire + Lightning | Prior element-array evidence: Shadow Weaver / Tenshin Shoden Yami-Ryu |
| Wood | Water + Earth | Prior element-array evidence: Nature's Blessing / Shinseina Ki |
| Scorch | Fire + Wind | Prior common pattern: Taiyo Kami / Traveling Sun Praiser; not exclusive lore |
| Storm | Water + Lightning | Prior element-array evidence: Arashima / Shinrai Ou |
| Magnet | Wind + Lightning | Prior element-array evidence: Itojinsei |
| Yin-Yang | Fire + Lightning | Prior frequent pattern: Heavenly Sonata / Tenohira Musei; not exclusive lore |
| Lava | Fire + Earth | Prior element-array evidence: Suragu |
| Explosion | Earth + Lightning | Prior element-array evidence: Bakuhatsu |
| Light | **Fire + Lightning** | Approved two-Minor balance revision; prior four-element co-occurrence does not require three Minors |
| Boil | Fire + Water | **Provisional**; no comparable recipe evidence established |
| Metal | Earth + Lightning | **Provisional**; no comparable recipe evidence established |
| Sand | Earth + Wind | **Provisional**; no comparable recipe evidence established |

Dust and Sand share proposed parentage; they still target different elements. `None` is the engine's non-elemental sentinel, not a sixteenth Special Element school. Special Elements are terminal unless a reviewed Hidden Art uses one as a prerequisite. No terminal Seal labels are needed.

## 5. C — Specialization Schools: eleven exact-tag schools

Each requires its parent Discipline Minor. Skill I gives +2.5%; Skill II adds +2.5%. Total expenditure including the parent is 10 SP at Minor or 15 SP at Major. Specializations may unlock reviewed Hidden Arts at Minor; their Major purchase need not receive a Seal label.

| Discipline Minor | School | Exact tag, any element |
|---|---|---|
| Assault | Impact | Damage |
| Assault | Momentum | Increase Damage Given |
| Assault | Pressure | Increase Damage Taken |
| Assault | Attrition | Afterburn |
| Guard | Bulwark | Decrease Damage Taken |
| Guard | Suppression | Decrease Damage Given |
| Guard | Reversal | Reflect |
| Sustain | Restoration | Heal |
| Sustain | Grace | Increase Heal |
| Sustain | Predation | Lifesteal |
| Sustain | Assimilation | **Absorb; requires upstream support** |

## 6. D — Hidden Arts: review roster

The [full candidate roster](POTENCY_HIDDEN_ARTS_ROSTER_V2.md) proposes **18 original teachings**: eleven elemental intersections, four Special Element intersections and three paired-specialization arts. It includes meaningful Absorb paths and preserves/refines the previous ten concepts. Names, selectors and unlocks remain reviewable proposals.

| Route | Recursive prerequisites | Total at Hidden I / II |
|---|---:|---:|
| Nature Minor + Specialization Minor, including parent Discipline | 15 SP | 20 / 25 SP |
| Special Element Minor + Discipline Minor, including two Nature Minors | 20 SP | 25 / 30 SP |
| Two Specialization Minors sharing one Discipline | 15 SP | 20 / 25 SP |
| Two Specialization Minors from different Disciplines | 20 SP | 25 / 30 SP |

A standard Special Element Minor + Specialization Minor chain costs 25 SP before buying the Hidden Art. Its Major would cost 35 SP. The proposed four Special Element arts therefore use a direct Discipline Minor gate instead; this is explicitly a candidate unlock decision, not an approved exemption.

Removing Foundation resonance has a cost: these Special Element routes spend 10 SP on basic-element prerequisites that do not boost a pure Special Element effect. Each proposed Special Element art now spans two tag types across disciplines: its completed build gives +10% to the tag inside its prerequisite Discipline and +7.5% to the other. A single-tag version was scope-dominated by completing both parent schools. The paired scopes give a focused tradeoff; review it without changing the approved percentages.

## 7. E — Advanced Arts: Major investment rewards

The retained basis is **five Nature Majors × three Discipline Majors = fifteen distinct intersections**. Entry costs 20 SP; Skill I brings total expenditure to 25 SP, Skill II to 30. They use the same +2.5% purchases, not a larger mastery bonus. Each targets its exact basic element and the parent Discipline's tag set.

| Nature Major | + Assault Major | + Guard Major | + Sustain Major |
|---|---|---|---|
| Fire | Inferno Doctrine | Ashen Aegis | Phoenix Current |
| Water | Riptide Doctrine | Abyssal Aegis | Endless Current |
| Wind | Razor Tempest | Hollow Wind | Breath of Spring |
| Earth | Seismic Doctrine | Mountain Heart | Stoneblood Cycle |
| Lightning | Thunderclap Doctrine | Thunder Aegis | Living Current |

These are retained name/scope candidates for final audit. No two have identical selectors: each changes the element, the discipline, or both. Elemental offense, defense/countering and recovery are represented. Distinct schema selectors alone do not prove useful live content exists for every intersection. All five Sustain Advanced Arts are only partially supported today: Lifesteal can be element-selected; Absorb needs support, and Heal / Increase Heal need elemental-scope reconciliation.

Advanced Arts reward a whole discipline within one element. Hidden Arts should instead support narrower mixed-element specialists or a deliberate paired-tag identity. Example: maxing Impact in a Burning Edge build gives more non-Fire Damage Potency than the Fire Assault Advanced route; maxing Fire instead would produce a scope-dominated alternative. The roster document records this comparison.

**Optional broad schools remain deferred:** Harmony needs an exact scope and affordable Major gate. Three Foundation Majors already consume the entire budget before purchasing it; an any-two-of-five gate is not directly represented by upstream AND-only `requiredSkillIds`. Unbroken Form needs a scope distinct from a duplicate Guard school. The former three-Minor Balanced Form is retained only as deferred history in the graph, not silently promoted into a Major-gated category.

## 8. Checked allocation examples

Numbers below are **skills purchased**, not SP or old ranks. Every I costs 5 SP; every II costs 10 SP cumulatively.

| Allocation | SP | Qualifying effect contribution |
|---|---:|---|
| Fire I + Assault I + Impact I | 15 | Fire Damage +7.5% |
| Fire II + Assault II + Sustain II | 30 | Fire Assault/Sustain tags +10%; Fire Guard tags +5%, subject to source gaps |
| Fire II + Assault II + Inferno Doctrine II | 30 | Fire Assault tags +15%; other Fire tags +5%; non-Fire Assault tags +5% |
| Fire I + Assault I + Impact II + Burning Edge II | 30 | Fire Damage +15%; non-Fire Damage +7.5% |
| Water I + Wind I + Ice II + Guard II | 30 | Pure Ice Guard tag +10%; Water/Wind provide no inherited Ice bonus |
| Fire I + Earth I + Crystal I + Guard I + Glass Lotus II | 30 | Pure Crystal Reflect +10%; Crystal Increase Damage Taken +7.5% |
| Fire I + Water I + Wind I + Earth I + Lightning I + Assault I | 30 | Valid six-Minor spread; a pure basic-element Damage tag gets +5% |

The +15% maximum is a selector-overlap ceiling, not a guarantee for every build. It also does not cap other sources outside the Potency tree or replace engine caps on affected tag power.

## 9. Card presentation contract

Use the approved dark navy-black ninja scenery, subdued gold ornamental border, parchment explanation band and aligned, uniform cards. Elemental schools use their own accents; Assault red, Guard blue, Sustain green. Preserve moonlit mountain/pagoda/village silhouettes and a mature, restrained palette.

- Foundation: eight large cards in a symmetrical layout.
- Special Elements: fifteen uniform cards, exact element, scope, unlocks and investment.
- Specialization: three grouped columns for Assault, Guard and Sustain. Sustain now has four cards. Align card dimensions and row rhythm; do not stretch the three Guard cards to create uneven heights or invent a fourth school.
- Hidden/Advanced: settle roster and unlocks before freezing card text and producing imagery.
- Every card uses `0/2`, `1/2`, `2/2`, or two unambiguous purchase slots. Show Skill I / 5 SP / +2.5% / Minor and Skill II / 5 SP / +2.5% / Major. At completion show +5% total.
- Distinguish a locked school, an available unpurchased school, and a completed school. Show every prerequisite and its current tier; distinguish individual skill cost from total school and path cost.
- Reserve Seal labels for actual outgoing unlocks. No inspirational text, proverbs, fake quotes, slogans, decorative prose or character action filler.
- The previous three showcase images are style references only; their progression text must be replaced before reuse. No previous image is asserted to have been regenerated or reviewed here.
- Showcase art is a design deliverable, not a live-game asset. The explicit showcase text/border request governs this task; production icon prohibitions do not erase that request.

## 10. Implementation and acceptance gates

1. User review of Hidden Arts roster/effects/unlocks, Advanced Arts purpose and optional additions, final names and provisional Special Element topology.
2. Resolve Absorb support, jutsu-versus-tag elemental matching (especially healing), and actual enforcement of the 30-SP budget. Do not drop intended coverage to make a manifest validate.
3. Verify content viability of each intended element/tag intersection from suitable repository evidence; no live census is claimed here.
4. Future implementation must represent Skill II as requiring Skill I and school entry as an AND of the listed I/II purchases. Stable graph IDs are design IDs, not live record IDs.
5. Expand multi-tag scopes into distinct singular `affectedTag` modifiers. Never combine overlapping wildcard and exact-tag modifiers from one purchase in a way that breaks the +2.5%-per-effect invariant.
6. Reverify stacking, skill-effect attachment, duration, deactivation/prerequisite behavior and multi-element deduplication before implementation. The legacy 100-round value was an authoring candidate, not a verified permanent passive contract.
7. Visual approval follows mechanical text review. Implementation brief, manifests, hidden readback and publishing require their own authorized work. Fable remains the normal implementation owner.

Structural audit results are recorded in [validation](POTENCY_V2_VALIDATION_2026-09-29.md). A budget-valid graph is not proof of implementation readiness or user acceptance. **Live-game requests / writes: 0 / 0.**
