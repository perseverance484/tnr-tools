# Ghost Ship retained legacy jutsu: post-0056 re-baseline

`state/ghost_ship_legacy_jutsu_conversion.json` pins `protectedRecordSha256` over the October 1
rows. Upstream migration 0056 changed 20 schema columns on every live jutsu record (no mechanic
change), so live rows no longer hash to those values. The conversion packet is an input of the frozen
Stage 2 r4, 3/3 Consume and final-item harnesses, whose M0 evidence records its SHA-256, so it is
left byte-for-byte unchanged. This directory writes the companion
`state/ghost_ship_legacy_jutsu_baseline_push86.json` instead.

| Command | Result |
| --- | --- |
| `python3 harness/ghost_ship_legacy_baseline/build_baseline.py` | writes the packet; fail-closed |
| `python3 harness/ghost_ship_legacy_baseline/build_baseline.py --check` | verifies and refuses a stale packet |
| `python3 harness/ghost_ship_legacy_baseline/selftest.py` | 6 probes: clean copy passes; divergent copy, effect change, non-null new column, presentation drift and missing record are each detected |

The builder proves:
- both capture pins hold;
- every October 1 row still matches the packet hash;
- every push/86 kit copy of each id is identical;
- the October 1 to push/86 delta is exactly the 20-column schema change:
  - 8 removed `required*Offence/Defence`, all null;
  - 11 added columns, all null, except `elementClassification` "None";
  - `statClassification` changed from Highest to None;
- every other field (effects included) is identical, and the presentation still equals the packet's `before`.

The 11 new protected hashes equal those published in
`docs/reviews/GHOST_SHIP_SKYGLASS_CAPTURES_85_86_2026-10-11.md` §2.

`push/90_ghost_ship_skyglass_release.gen.py` refuses to build unless every legacy jutsu edit's
source row hashes to this baseline and the baseline was built from the same push/86 file and
conversion packet.

## Consumer audit (who else holds the eleven jutsu)

push/90 unequips and re-equips the eleven jutsu only on the eleven Ghost Ship AIs (law 18/60). Any
other AI holding one would be left with a severed combat link. All eleven are `jutsuType: AI` and
hidden, so only AI kits can hold them. The audit manifest is therefore the queued, read-only AI census
`push/81`–`push/84`. It point-reads all 535 known AI ids with `profile.getAi` `persist:"full"`, and its
completeness rule is 522 live non-ELDER AIs, the push/80 `profile.getAllAiNames` count. A separate
Ghost Ship manifest would repeat the same reads.

| Command | Result |
| --- | --- |
| `python3 harness/ghost_ship_legacy_baseline/consumer_audit.py <81–84 results…>` | writes `state/ghost_ship_legacy_jutsu_consumer_audit.json`; exit 0 only for CLEAR |
| `python3 harness/ghost_ship_legacy_baseline/consumer_audit_selftest.py` | synthetic CLEAR / CONSUMERS / missing-read / short-count cases |

Verdicts:
- **CLEAR:** all 535 ids read, 522 live non-ELDER, and no non-Ghost-Ship holder.
- **CONSUMERS:** the holders are listed, and push/90 `--final` refuses.
- **INCOMPLETE:** a census id is missing, or the live count differs.

`push/90 --final` requires CLEAR.
