# Potency revision 2.1 validation — 2026-09-29

**Result:** structural PASS. This is a design-data audit, not an engine test, live validation, final balance approval or authorization to implement.

Graph SHA-256: `310181c9457ce7267368f334ea9f21c3f4458a48b3a09bed2eb7b2e92c70f022`

Upstream source pin: `9f01172038dbc412c837a7f97f7451eb87b6a234`

Input design branch for this amendment: `664437382ba33a16023ad8e2feae12d90371336f`

## Results

| Check | Result |
|---|---|
| School count by category | Foundation 8; Special Elements 15; Specialization 10; Hidden Arts 16; Advanced Arts 15 |
| Distinct school IDs | 64 / 64 |
| Purchases | Exactly I and II per school; each 5 SP and +2.5%; II requires I |
| Dependency cycles / unresolved references | 0 / 0 |
| Schools with Major reachable within 30 SP | 64 / 64, counting recursive prerequisites once |
| Foundation roots / exact Nature scopes | Eight roots; five exact basic-element scopes, no inherited Special Elements |
| Special Elements | All fifteen enum members; two Foundation Minors each; None excluded |
| Light | Fire Minor + Lightning Minor |
| Provisional mappings | Boil, Metal, Sand remain flagged |
| Hidden coverage | All ten supported tags covered; names/unlocks are proposals |
| Advanced Arts duplicate selectors | 0 among fifteen retained element/discipline intersections |
| Unsupported tag accounting | Active scopes use the upstream ten-tag set; Absorb and its dependent schools are deferred |
| Elemental healing accounting | Heal / Increase Heal element gap flagged on every affected school |
| Fake terminal Seals | 0; every displayed Seal label has outgoing unlocks |
| Legacy progression fields | No rank-count, per-rank cost, per-rank potency, or rank-threshold fields remain in the graph |
| Allocation assertions | Ten passed, including +7.5%, +15%, Special Element +10%, paired-tag and multi-element examples |
| Special Element tradeoff comparisons | Four passed: each revised pair improves one scope and loses breadth relative to parent completion; no claim of exhaustive dominance analysis |
| Rejected longer Special Element route | 35 SP to finish when both Special Element and Specialization Minors are required |
| Errors | 0 structural errors |

## Method and reproduction

A session-local Python audit parsed the graph and the pinned upstream validators/constants. It checked the exact two-purchase shape; compared current tags and element names with source; walked every dependency with cycle detection; recursively unioned ancestor school purchases using the maximum required I/II count for a shared ancestor; multiplied the resulting count by 5; and checked the recorded Minor/Major totals for every school. It also reconstructed outgoing unlock lists and checked Seal labels against them.

For each allocation in the design examples and additional paired-tag cases, the audit checked prerequisites and the 30-SP budget, then summed `2.5 × purchases` for each matching school. A school matched an effect once when its tag union contained that tag and its element filter was empty or intersected the supplied elements. This is design arithmetic; the source's per-tag matching distinction is recorded separately. The audit also confirmed that elemental Heal/Increase Heal selectors do not match the source fallback None, while unrestricted Restoration does.

The overlap ceiling follows without exhaustive enumeration: every purchase costs 5, every purchase contributes at most 2.5 to a given effect, and the budget is 30. Therefore there can be at most six qualifying contributions and their sum is at most 15. A valid Fire II / Assault II / Inferno Doctrine II allocation attains the ceiling under the intended selectors. No claim of enumerating every allocation is made.

The ten assertions cover:

- Fire I / Assault I / Impact I: Fire Damage 7.5.
- Fire II / Assault II / Inferno Doctrine II: Fire Damage 15.
- Fire I / Assault I / Impact II / Burning Edge II: Fire Damage 15 and Water Damage 7.5.
- Water I / Wind I / Ice II / Guard II: pure Ice Reflect 10.
- Fire I / Earth I / Crystal I / Guard I / Glass Lotus II: pure Crystal Reflect 10.
- Sustain I / Restoration I / Grace I / Borrowed Breath II: Heal 10.
- Assault I / Guard I / Pressure I / Reversal I / Returning Needle II: Reflect 10.
- Five Nature Minors / Assault I: Fire Damage 5.
- Fire II / Assault II / Inferno Doctrine II on a Fire-and-Water effect: 15, with no within-purchase duplication.

Absorb, Assimilation, Hollow Palm and Empty Vessel were removed from active scopes, prerequisites and outgoing unlocks under RUL-2026-09-29-003. No replacement school was added.

## Limits and pending acceptance

Two implementation gaps remain: jutsu-wide versus per-tag elemental semantics, particularly healing; and enforcement of a separate 30-SP allocation. Passive attachment/duration, deactivation behavior and current content viability still need implementation review. The graph includes candidates and must not be treated as a game manifest. Hidden/Advanced names, selectors and unlocks are not approved by this audit.

Repository session guards: lawmap has 0 errors and 5 pre-existing warnings; doctrine projections and reference packs/TOCs are current. An initial sparse-checkout omission of builder_bundle.js caused a missing-file guard error; materializing the existing tracked file resolved it without editing tooling. No tests or game source were executed against production. No new inbox/live-state validation was performed. Potency roadmap validation and its generated projections pass. Repository-wide workstream validation found missing unrelated One Perfect Crop files in the sparse checkout; automatic approval review rejected fetching those files as outside this task. That broader validation was left incomplete. No unrelated content was fetched to satisfy it.

**Live-game requests / writes: 0 / 0. Hidden Arts images generated: 0.**
