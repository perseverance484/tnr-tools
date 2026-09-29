# Potency source audit — 2026-09-29

**Scope:** read-only GitHub/repository research. Source was read, not executed. No TNR production API, browser session, live record, or asset-CDN request was made. No game manifest was authored.

## Verified refs

| Ref | Exact SHA |
|---|---|
| `perseverance484/tnr-tools` main | `1601f072af839402395eeab1326b1228747e0009` |
| Potency design branch at session start | `36bc4cc7aa79321e52f8e90584933d5c747497a7` |
| Local merge-base of the above | `1601f072af839402395eeab1326b1228747e0009` |
| `studie-tech/TheNinjaRPG` main | `9f01172038dbc412c837a7f97f7451eb87b6a234` |

TNR Tools refs were verified through live Git refs; upstream main was verified through the GitHub connector. Upstream files below were fetched at that exact commit. The handoff SHAs happened to remain current; they were not assumed. Existing global session state was a September 20 checkpoint and does not by itself establish September 29 status in unrelated workstreams.

## Source-verified mechanics

All links below are pinned to `9f01172038dbc412c837a7f97f7451eb87b6a234`.

| Source | Finding |
|---|---|
| [combat validator](https://github.com/studie-tech/TheNinjaRPG/blob/9f01172038dbc412c837a7f97f7451eb87b6a234/app/src/validators/combat.ts#L152-L189) | `PotencyTagTypes` has ten tags. `increasepotency` supports percentage calculation, a singular affected tag and an array of elements. Absorb is absent from that accepted selector enum. |
| [Potency resolver](https://github.com/studie-tech/TheNinjaRPG/blob/9f01172038dbc412c837a7f97f7451eb87b6a234/app/src/libs/combat/potency.ts#L54-L145) | Non-jutsu actions are returned unchanged. Active, non-new caster modifiers are selected subject to sealing and stacking. Matching percentage amounts add. Static additions precede the percentage multiplier. Percentage-calculation target tags are capped at 100. |
| [Potency element matching](https://github.com/studie-tech/TheNinjaRPG/blob/9f01172038dbc412c837a7f97f7451eb87b6a234/app/src/libs/combat/potency.ts#L108-L135) | Element matching uses the individual tag's elements, or None if absent/empty. A specific affected tag and selected element are AND. Element arrays match any member. The `none` selector with selected elements means any supported tag matching those elements. |
| [action application](https://github.com/studie-tech/TheNinjaRPG/blob/9f01172038dbc412c837a7f97f7451eb87b6a234/app/src/libs/combat/actions.ts#L945-L980) | Potency resolution happens once before cast effects are inserted, including eligible ground Potency; it is not a retroactive rewrite of previously cast effects. |
| [Absorb schema](https://github.com/studie-tech/TheNinjaRPG/blob/9f01172038dbc412c837a7f97f7451eb87b6a234/app/src/validators/combat.ts#L192-L202) | Absorb is a real percentage-calculation effect with pool selection and element-capable IncludeStats. That does not make it Potency-supported. |
| [Increase Heal schema](https://github.com/studie-tech/TheNinjaRPG/blob/9f01172038dbc412c837a7f97f7451eb87b6a234/app/src/validators/combat.ts#L240-L247), [Heal schema](https://github.com/studie-tech/TheNinjaRPG/blob/9f01172038dbc412c837a7f97f7451eb87b6a234/app/src/validators/combat.ts#L513-L521) | Neither includes an elements field. Standard schema-valid tags therefore cannot match an element-restricted Potency modifier. Unrestricted Heal/Increase Heal Potency still works. |
| [element enums](https://github.com/studie-tech/TheNinjaRPG/blob/9f01172038dbc412c837a7f97f7451eb87b6a234/app/drizzle/constants.ts#L864-L891) | Five basic elements, fifteen Special Elements, plus None. The enum does not encode elemental recipes. |
| [stacking constant](https://github.com/studie-tech/TheNinjaRPG/blob/9f01172038dbc412c837a7f97f7451eb87b6a234/app/drizzle/constants.ts#L1448) | `BATTLE_TAG_STACKING` is true at this pin; do not assume the value cannot change. |
| [skill validator](https://github.com/studie-tech/TheNinjaRPG/blob/9f01172038dbc412c837a7f97f7451eb87b6a234/app/src/validators/combat.ts#L1460-L1472) | Positive integer costs permit 5 SP; prerequisites are a list of IDs. The 1–10 tier field is an ordering/schema field, not a requirement for ten purchases per school. |
| [purchase router](https://github.com/studie-tech/TheNinjaRPG/blob/9f01172038dbc412c837a7f97f7451eb87b6a234/app/src/server/api/routers/skillTree.ts#L170-L230) | Every required skill must be activated. Used points sum activated skills globally and are compared with user.skillPoints. No Potency-specific 30-SP allocation check is present in this path. |
| [global maximum](https://github.com/studie-tech/TheNinjaRPG/blob/9f01172038dbc412c837a7f97f7451eb87b6a234/app/drizzle/constants.ts#L2670) | Global `MAX_SKILL_POINTS` is 100; this is not the approved Potency budget. |
| [skill-tree validator module](https://github.com/studie-tech/TheNinjaRPG/blob/9f01172038dbc412c837a7f97f7451eb87b6a234/app/src/validators/skillTree.ts) | Filtering and folder schemas do not establish a separate folder SP budget. |

## Implementation consequences, not design reversals

**POT-IMPL-01 — Absorb, deferred:** RUL-2026-09-29-003 removes Absorb from the active design, including Sustain/Advanced tag scopes, Assimilation, Hollow Palm and Empty Vessel. Adding upstream support is no longer a dependency for this roster. The source finding remains historical evidence; reintroduction requires a later user decision.

**POT-IMPL-02 — element semantics:** the approved description affects all supported tags on a jutsu of the selected element; the current resolver reads each tag individually. Sibling Fire Damage does not make an elementless Heal tag Fire. Elemental healing candidates and all five Sustain Advanced Arts are therefore incomplete in current upstream. The later implementation brief must define the intended jutsu classification and multi-element behavior, then reconcile validator/runtime handling without silently changing design intent. No metadata propagation or new schema field is assumed here.

**POT-IMPL-03 — 30-SP enforcement:** the +15% invariant depends on limiting this tree to six purchases. The existing global check alone is insufficient. The appropriate budget enforcement mechanism is future implementation work, not an invitation to change the approved 30-SP number.

**Other implementation checks:** skill effects must attach and remain active as intended; Skill II must preserve Skill I and prerequisites; deactivation must not leave an invalid allocation; multi-tag expansion must contribute once per effect; multi-element matching must not double count. The old `rounds:100` candidate is within the validator limit but is not proof of permanent passive duration.

## Element parentage evidence

The prior design commit records eleven named bloodline element-array examples. That research is retained with attribution in the design source; this session does not upgrade it to fresh live-content evidence. Light's two-parent entry is a new approved balance mapping, not a source recipe.

A limited check of upstream [app/data/bloodline.sql](https://github.com/studie-tech/TheNinjaRPG/blob/9f01172038dbc412c837a7f97f7451eb87b6a234/app/data/bloodline.sql) scanned **61 seed rows**. This is an old seed dataset, not a current live census or a complete parentage model. There were no Boil or Metal text occurrences; the Sand occurrence was a record name, not a Sand element-array recipe. This does not prove absence from the live game and does not resolve any of the three mappings.

**Still provisional:** Boil = Fire + Water; Metal = Earth + Lightning; Sand = Earth + Wind. Dust/Sand sharing parents is a proposed tree choice. Do not label either a universally source-defined recipe.

## Boundaries

The mechanical source was verified; proposed Hidden Arts content viability and names were not verified against a current live catalog. No current live-game behavior, installed UI, combat result or release readiness is claimed. GitHub reads are repository research, not live-game requests. **Live-game requests / writes: 0 / 0.**
