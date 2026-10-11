# Crowned Captain — active support behavior

**Status:** DIRECTOR-APPROVED ACTIVATION DIRECTION, RUL-2026-10-11-007. Heal threshold 40 and regular Reflect use are directed; Copy's exact “high IDG” number, native heal-boundary acceptance, final ordering and measured balance remain open. This is a design/test brief, not a manifest.

**Canonical relationship:** `state/ghost_ship_hybrid_kit_proposal.json` remains the unchanged accepted eleven-move membership and historical harness input under RUL003. This companion owns the new support activation direction. Do not alter historical tests or relabel their unapproved heal50/Copy30/Reflect-distance3 experiment.

## Director direction

- **S35 Second Wind:** heal at 40% health, rather than use as an unconditional rotation action.
- **B07 Stolen Form:** copy when an enemy has high Increased Damage Given (IDG).
- **Rebounding Form:** use Reflect in the normal rotation, not only as a low-health response.
- Preserve all eleven jutsu, existing technique mechanics and IDs, Crowned profile/innates, reward drops and the two-battle farming route. No new jutsu, phases, stat adjustments or loot.

## Native candidate for Fable

Prepend these support rules to the prior candidate-remapped offensive chain. Preserve that chain and its default/fallback setting for a controlled comparison. This relative ordering is proposed for testing, not final balance acceptance.

| Order | Technique | Candidate native rule | Meaning and limitation |
| --- | --- | --- | --- |
| 1 | S35 Second Wind | `health_below:40`; `use_specific_jutsu`, SELF | Emergency heal first when available. Native comparison is strictly **below 40% of effective maximum health**; exactly 40% does not trigger. No distance gate. |
| 2 | B07 Stolen Form | `target_has_effect`, increasedamagegiven, **proposed threshold 71**, CLOSEST_OPPONENT; `distance_lower_than:5`; action targets the same opponent | Copy before S31 Clear can remove that target's buffs. The director has not selected the exact Copy threshold. |
| 3 | Rebounding Form | `use_specific_jutsu`, SELF; no health/distance condition | Regular use whenever available, ahead of ordinary attacks. Existing AP/cooldown rules limit use. The historical test's distance3 restriction is not carried forward. |
| 4 onward | Existing offensive chain | Preserve candidate-remapped rules/defaults/fallback | Isolate support activation from other rule changes. |

All unavailable actions fall through. **71+ IDG is a recommendation**, matching Sealwright's established integer threshold; the old experimental 30 was never approved for Crowned Captain. CLOSEST_OPPONENT is a concrete native candidate, not a highest-IDG selector. Test nearest summons and farther buffed players separately.

**Heal boundary:** the user selected 40%; native `health_below` offers a strict integer comparison. Keep 40 in the candidate and disclose the equality difference for acceptance. Do not silently use 41, which would permit healing between 40% and 41%. No engine change is authorized to force inclusive behavior.

## Preserved records and effect scope

Read from `harvests/inbox/tnr_results_1790826836406.json#/captures/10/data/jutsus`, using accepted kit pointers. These are historical captured records, not new live reads.

| Technique | ID | Target / method / range | AP / cooldown | Effect |
| --- | --- | --- | --- | --- |
| Second Wind (S35) | `STu1VHNcfgeC3x-UiQDgt` | SELF / SINGLE / 0 | 40 / 6 | Heal 15% Health |
| Stolen Form (B07) | `VuFuBtE7h5B1nnA2J1lFZ` | OTHER_USER / SINGLE / 4 | 60 / 6 | Copy 100%, rounds3 |
| Rebounding Form (captured Counter Stance) | `T3glZGcSd-jS8G-NB43GR` | SELF / SINGLE / 0 | 40 / 4 | Reflect 35%, rounds2 |

IDG controls when Copy is attempted; the effect copies eligible positive buffs broadly, not exclusively IDG, and does not remove them from the enemy. At the reviewed pin it selects up to four eligible effect types, strongest per type, subject to its persistent per-caster copy budget. Raw IDG conditions do not filter expiry, protected/passive/item origins or copyability; they can trigger an empty Copy. Buff Prevent can stop copying. Consume itself is not a copyable type. Do not claim the full summed IDG always transfers.

Reflect returns eligible damage under native activation and prevention rules. It does **not** subtract the reflected amount from received damage; 35% Reflect is not 35% damage reduction. Preserve every effect field and the captured costs, including Rebounding Form's fractional pool costs. Heal Prevent can block Second Wind.

## Bounded offline tests

Fable owns implementation on a new owned branch; preserve frozen r4 and active-Consume targets. Source candidate: `studie-tech/TheNinjaRPG@585534d7eb21d6f0dd678d5c3eb92662f611d39b` (upstream, deployment unverified). Read the source-drift review before adapting A1 assembly/metrics.

1. Compare captured rules, prior kit/remap-only rules with dormant support, and this support candidate. Hold profile, kit, innate effects, settings, player carriers and placements constant. Label threshold71 and strict-below40 as proposals until accepted.
2. Force heal opportunities at 39.9%, exactly40%, 40.1% and lower health. Assert effective-max-HP basis, actual heal amount, cooldown/AP fallthrough and Heal Prevent. Short fights with zero heal casts do not validate healing.
3. Probe Copy at IDG 30/70/70.5/71/90, summed effects, expired/protected sources, Buff Prevent, existing copy budget and no eligible candidates. Separate condition success from actual buffs copied. Test closest low-IDG summon versus farther high-IDG player, path distance4/5/6 and precedence over S31 when both actions are executable.
4. Exercise Reflect at high/low health and near/far starts, cooldown, expiry, reflected damage and prevention. Confirm no inherited health/range condition keeps it dormant. Measure support AP cost, including heal40 + reflect40 potentially displacing a60AP attack.
5. Compare whole-step damage, fight outcomes/length, normal attack cadence, support-use counts and actual heals/copies/reflections. Report a material difficulty change before tuning; no numeric acceptance tolerance is invented.
6. Preserve real engine preprocessing, no-DB/network isolation, source integrity, fail-closed evidence and two-run reproducibility. Return an exact frozen SHA for independent review, with remaining director decisions explicit.

Historical A1 used heal below50%, Copy IDG30 and Reflect distance3; it recorded Reflect10, Copy5 and Heal0. Those results do not validate this direction. No new runtime tests were executed during this design update.

## Source anchors and boundaries

- New pin `app/src/libs/combat/ai_v2.ts:315–318`: strict health comparison; `360–378`: raw IDG sum and inclusive threshold; `260–261`: closest targeting.
- `app/src/validators/ai.ts:28–32`: positive integer heal-condition value.
- `app/src/libs/combat/tags.ts:247–408` and `app/drizzle/constants.ts:3379–3463`: Copy eligibility, priority, prevention and cap.
- `tags.ts:1654–1711,1789–1820`: Heal and Reflect processing.
- Historical `harness/ghost_ship_stage2/engine/a1_kits.test.ts:231–274` and results section3: prior support experiment and dormant controls.

No live-game request/write, CDN request, credentials, engine edit, art, manifest, publication or regular-Captain change. Sealwright's dual-Clear identity remains intact.
