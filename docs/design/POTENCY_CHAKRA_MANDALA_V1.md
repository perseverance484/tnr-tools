# TNR Potency — Chakra Mandala v1

**Status:** director-approved architecture; v1 taxonomy and balance specification  
**TNR Tools baseline:** `1601f072af839402395eeab1326b1228747e0009`  
**Current upstream TNR source inspected:** `9f01172038dbc412c837a7f97f7451eb87b6a234`  

## Frozen architecture

- 30 Potency skill points.
- No travel nodes.
- Every school has 10 ranks.
- Every rank costs 1 SP.
- Every rank grants **+0.5% Percentage Potency** to that school's selector.
- Rank 5 is the **Minor Seal**. Rank 10 is the **Major Seal**.
- Minor/Major seals unlock further schools; they do **not** add a hidden numeric Potency spike.
- If all 30 purchased ranks apply to the same effect, the Mandala contributes at most **+15% Potency**.

That last invariant is the primary balance governor. Wider schools affect more possible jutsu; narrow schools do not receive a larger per-rank number. Specialization becomes powerful by stacking several 0.5% scopes on the same effect.

## Verified engine constraints

The current upstream Potency implementation supports exactly ten affected tags and element selectors, applies Static before summed Percentage Potency, snapshots Potency onto subsequent jutsu casts, and ignores non-jutsu actions. The design therefore standardizes the Mandala on Percentage Potency. Every rank effect should author `increasepotency`, `calculation: percentage`, `power: 0.5`, `powerPerLevel: 0`, `rounds: 100`, `target: SELF`.

Current supported tag set:

Damage, Increase Damage Given, Decrease Damage Given, Increase Damage Taken, Decrease Damage Taken, Afterburn, Lifesteal, Reflect, Increase Heal, Heal.

## Foundation schools

| School | Rank scope | Minor | Major |
|---|---|---|---|
| **Fire** | Any supported Potency tag on **Fire, Crystal, Shadow, Scorch, Yin-Yang, Lava, Light, Boil** jutsu | Ember Seal | Inferno Seal |
| **Water** | Any supported Potency tag on **Water, Ice, Wood, Storm, Boil** jutsu | Current Seal | Tide Seal |
| **Wind** | Any supported Potency tag on **Wind, Ice, Dust, Scorch, Magnet, Light, Sand** jutsu | Gale Seal | Tempest Seal |
| **Earth** | Any supported Potency tag on **Earth, Crystal, Dust, Wood, Lava, Explosion, Metal, Sand** jutsu | Stone Seal | Mountain Seal |
| **Lightning** | Any supported Potency tag on **Lightning, Shadow, Storm, Magnet, Yin-Yang, Explosion, Light, Metal** jutsu | Spark Seal | Thunder Seal |
| **Assault** | Damage, Increase Damage Given, Increase Damage Taken, Afterburn on any element | Striking Seal | Apex Seal |
| **Guard** | Decrease Damage Taken, Decrease Damage Given, Reflect on any element | Ward Seal | Fortress Seal |
| **Sustain** | Heal, Increase Heal, Lifesteal on any element | Pulse Seal | Life Seal |

Foundation Nature schools deliberately resonate with their descendant advanced elements. This prevents the prerequisite ranks used to unlock an Advanced Nature from becoming dead investment.

## Exact-tag specializations

Each requires its parent Discipline at Minor (5 ranks).

| School | Parent | Scope | Minor / Major total cost from zero |
|---|---|---|---:|
| **Impact** | Assault Minor | Damage | 10 / 15 |
| **Momentum** | Assault Minor | Increase Damage Given | 10 / 15 |
| **Pressure** | Assault Minor | Increase Damage Taken | 10 / 15 |
| **Attrition** | Assault Minor | Afterburn | 10 / 15 |
| **Bulwark** | Guard Minor | Decrease Damage Taken | 10 / 15 |
| **Suppression** | Guard Minor | Decrease Damage Given | 10 / 15 |
| **Reversal** | Guard Minor | Reflect | 10 / 15 |
| **Restoration** | Sustain Minor | Heal | 10 / 15 |
| **Grace** | Sustain Minor | Increase Heal | 10 / 15 |
| **Predation** | Sustain Minor | Lifesteal | 10 / 15 |

## Advanced Nature schools

Parentage below is **skill-tree topology**, not a declaration that the setting has a universal elemental-combination law. Most links are grounded in current bloodline element co-occurrence; Boil, Metal and Sand remain v1 balance mappings pending a dedicated content census.

| Advanced school | Requires | Resonates from | Current-data note | Major total SP |
|---|---|---|---|---:|
| **Ice** | Water Minor + Wind Minor | Water + Wind | Teno Yuki / Hyouga Yui: Water + Wind + Ice | 20 |
| **Crystal** | Fire Minor + Earth Minor | Fire + Earth | Sea-Maiden’s Kiss: Fire + Earth + Crystal | 20 |
| **Dust** | Wind Minor + Earth Minor | Wind + Earth | Aerathiel / Windborne Priestess Legacy: Wind + Earth + Dust | 20 |
| **Shadow** | Fire Minor + Lightning Minor | Fire + Lightning | Shadow Weaver / Tenshin Shoden Yami-Ryu: Fire + Lightning + Shadow | 20 |
| **Wood** | Water Minor + Earth Minor | Water + Earth | Nature’s Blessing / Shinseina Ki: Water + Earth + Wood | 20 |
| **Scorch** | Fire Minor + Wind Minor | Fire + Wind | Taiyo Kami / Traveling Sun Praiser: Fire + Wind + Scorch | 20 |
| **Storm** | Water Minor + Lightning Minor | Water + Lightning | Arashima / Shinrai Ou: Water + Lightning + Storm | 20 |
| **Magnet** | Wind Minor + Lightning Minor | Wind + Lightning | Itojinsei: Wind + Lightning + Magnet | 20 |
| **Yin-Yang** | Fire Minor + Lightning Minor | Fire + Lightning | Heavenly Sonata / Tenohira Musei: Fire + Lightning + Yin-Yang | 20 |
| **Lava** | Fire Minor + Earth Minor | Fire + Earth | Suragu: Fire + Earth + Lava | 20 |
| **Explosion** | Earth Minor + Lightning Minor | Earth + Lightning | Bakuhatsu: Earth + Lightning + Explosion | 20 |
| **Light** | Fire Minor + Wind Minor + Lightning Minor | Fire + Wind + Lightning | Eyes of the Forsaken King: Fire + Wind + Lightning + Light | 25 |
| **Boil** | Fire Minor + Water Minor | Fire + Water | V1 balance mapping; verify against content census before implementation | 20 |
| **Metal** | Earth Minor + Lightning Minor | Earth + Lightning | V1 balance mapping; verify against content census before implementation | 20 |
| **Sand** | Earth Minor + Wind Minor | Earth + Wind | V1 balance mapping; verify against content census before implementation | 20 |

## Hidden Arts

Hidden Arts are exact **Element × Tag** schools. They require the element's Minor plus the relevant exact-tag specialization Minor. Since the tag specialization itself requires a Discipline Minor, a Hidden Art normally opens after 15 committed SP.

| Hidden Art | Prerequisites | Exact scope | Minor / Major total SP |
|---|---|---|---:|
| **Burning Edge** | Fire Minor + Impact Minor | Fire + Damage | 20 / 25 |
| **Cinder Doctrine** | Fire Minor + Attrition Minor | Fire + Afterburn | 20 / 25 |
| **Riptide Mark** | Water Minor + Pressure Minor | Water + Increase Damage Taken | 20 / 25 |
| **Healing Current** | Water Minor + Restoration Minor | Water + Heal | 20 / 25 |
| **Gale Rhythm** | Wind Minor + Momentum Minor | Wind + Increase Damage Given | 20 / 25 |
| **Quieting Wind** | Wind Minor + Suppression Minor | Wind + Decrease Damage Given | 20 / 25 |
| **Stone Body** | Earth Minor + Bulwark Minor | Earth + Decrease Damage Taken | 20 / 25 |
| **Rooted Grace** | Earth Minor + Grace Minor | Earth + Increase Heal | 20 / 25 |
| **Storm Mirror** | Lightning Minor + Reversal Minor | Lightning + Reflect | 20 / 25 |
| **Predator's Spark** | Lightning Minor + Predation Minor | Lightning + Lifesteal | 20 / 25 |

## Pinnacle Doctrines

A Pinnacle requires a **Nature Major + Discipline Major**. The two prerequisites cost 20 SP; maxing the 10-rank Pinnacle consumes the remaining 10 exactly. This is the prestige `10 / 10 / 10` build.

| Nature | Assault | Guard | Sustain |
|---|---|---|---|
| **Fire** | Inferno Doctrine | Ashen Aegis | Phoenix Current |
| **Water** | Riptide Doctrine | Abyssal Aegis | Endless Current |
| **Wind** | Razor Tempest | Hollow Wind | Breath of Spring |
| **Earth** | Seismic Doctrine | Mountain Heart | Stoneblood Cycle |
| **Lightning** | Thunderclap Doctrine | Thunder Aegis | Living Current |

Each Pinnacle rank applies +0.5% to the parent Discipline's tags **restricted to the exact base element**. Example: `Inferno Doctrine` boosts Damage, Increase Damage Given, Increase Damage Taken and Afterburn only on Fire jutsu.

## Generalist route

**Balanced Form** requires Assault Minor + Guard Minor + Sustain Minor (15 SP). Its ranks apply +0.5% to all ten supported Potency tags, regardless of element. At 10 Balanced Form ranks the build has spent 25 SP and may place the remaining 5 into any school. This is deliberately broad but remains under the same 0.5% per purchased rank invariant.

## Example 30-SP builds

- **Triple Major:** Fire 10 / Assault 10 / Sustain 10. Fire offensive and sustain effects stack two schools; everything else keeps one axis.
- **Pinnacle:** Fire 10 / Assault 10 / Inferno Doctrine 10. Fire Assault tags receive +15%; Fire Guard/Sustain tags receive +5%; non-Fire Assault tags receive +5%.
- **Advanced Nature:** Water 5 / Wind 5 / Ice 10 / Guard 10. Ice Guard tags receive +15% because Water and Wind both resonate into Ice.
- **Hidden Art specialist:** Fire 5 / Assault 5 / Impact 5 / Burning Edge 10 / Guard 5. Fire Damage receives +12.5%; other Fire tags get +2.5%; all Assault tags get +2.5%.
- **Six Minors:** six schools at rank 5. Extremely flexible; no single selector can exceed +15%.
- **Generalist:** Assault 5 / Guard 5 / Sustain 5 / Balanced Form 10 / one 5-rank school. Broad +7.5% on all supported tags before the final school's overlap.

## Implementation boundary

The current upstream skill system supports integer `costSkillPoints` and AND-style `requiredSkillIds`, so the prerequisite topology can be represented. However, current upstream also has a global `MAX_SKILL_POINTS = 100`; it does **not** currently enforce a 30-point sub-budget for one folder/Mandala. If the wider game is not changing to 30 total points, enforcing this design as a 30-SP Mandala requires a separate implementation decision.

Current upstream `BATTLE_TAG_STACKING` is `true`, which allows identical +0.5% rank effects to stack. This is a source-pinned assumption and should be regression-tested before implementation.

## V1 validation

- Schools: **59** (advanced_nature 15, foundation_discipline 3, foundation_nature 5, hidden_art 10, pinnacle_doctrine 15, tag_specialization 10, tri_discipline 1).
- Dependency cycles: **none**.
- Unsupported tag/element selectors: **none**.
- Schools with a Major reachable inside 30 SP: **59 / 59**.
- Errors: **0**.
- Warnings: **0**.

Boil, Metal and Sand parentage should be rechecked against the final content census before implementation. All other listed advanced links have an explicit current bloodline-data example noted above.
