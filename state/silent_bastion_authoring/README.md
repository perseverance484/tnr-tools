# Silent Bastion — complete offline authoring package (`alt99_f4gate`)

**Status: OFFLINE PACKAGE, director-accepted values.** This is not a manifest, not under `push/`, and has no live-game action. RUL-2026-10-15-001 and RUL-2026-10-16-001 to -012 are implemented. Cache names, cache and Beacon rarity, and art are still open; fresh reads, username checks and calibration come before any manifest (`decision_docket.md`). Publication is not authorized.

- **Build contract:** `state/prompt_silent_bastion_complete_authoring.md`.
- **Coordination lock:** `state/silent_bastion_approved_authoring_lock.json`.
- **Selected graph:** `harness/silent_bastion_condensed99/graphs/alt99_f4gate.json`. The composer checks it against the lock's SHA-256 before it builds anything.

## Layout

| Path | What | How it is made |
| --- | --- | --- |
| `design/commanders.json` | The 4 **existing** commander designs translated into the rule DSL. Each rule cites its roster or profile line. Kits, innate effects, exclusives and Countermand are recorded with APPROVED or CANDIDATE status | Hand-translated from `state/silent_bastion_commander_roster.md` and `state/silent_bastion_arakane_ai_profile.md`. Membership and priority order are not redesigned |
| `design/regulars.json` | 16 **new** regular enemies: identity, shared-pool kit, rules (gates computed as range+1), accepted stats | `tools/gen_regulars.py` |
| `design/script.json` | Player-facing text for all 99 objectives, plus the four puzzles with their planted clues and solution logic | `tools/gen_script.py` |
| `design/protocols.json` | Exact-target ledger: Medical, recovery, Security Alert, Combat Protocols (D5 Debuff Prevent 100 / 3r, RUL-2026-10-16-008) | hand-written |
| `design/entry_and_rewards.json` | Quest fields, Beacon, quest-level one-of-two cache choice, and the approved cache contents spec (RUL-2026-10-16-010) | hand-written |
| `sources/source_records.json` | Captured records for every equipped jutsu (76) and the two seed weapons, with capture provenance | `tools/extract_sources.py --engine <pinned export>` |
| `compiled/quest.candidate.json` | The 99-objective quest record. Refs stay symbolic (`@ai:<slot>`, `@item:`, `@jutsu:`) | `tools/compose.py` |
| `compiled/ai_profiles.candidate.json` | 20 AI records + rule sets (≤20 rules, `includeDefaultRules:false`, unconditional `end_turn` last) | `tools/compose.py` |
| `compiled/encounter_ledger.json` | 20 encounter identities, the battle objectives that use them, and their source-mapped kits | `tools/compose.py` |
| `compiled/cache_items.candidate.json` | The two completion caches as item records with their Weighted Cache tables | `tools/compose.py` from `design/entry_and_rewards.json` + the candidate pools file |
| `compiled/story_script.md` | Readable story script keyed to every objective ID | `tools/compose.py` |
| `economy_and_f3.md` | Stat ladder, reward economy, F3 farm math and `scaleGains` options | hand-written |
| `art_shotlist.md` | 20 avatars, scenes and icons. Brief only; no binaries | hand-written |
| `decision_docket.md` | Remaining director items, pre-manifest work, and every resolved ruling | hand-written |

Every generator has `--check`. `harness/silent_bastion_authoring/run.sh` runs them all, then validates natively. Results: `docs/reviews/SILENT_BASTION_AUTHORING_OFFLINE_RESULTS.md`.

```bash
python3 state/silent_bastion_authoring/tools/gen_regulars.py
python3 state/silent_bastion_authoring/tools/gen_script.py
python3 state/silent_bastion_authoring/tools/compose.py
harness/silent_bastion_authoring/run.sh
```

## Rules of the package

- **Commander designs are implemented, not redesigned.** The deviations are all source-forced or candidate-value choices, and each is flagged in `decision_docket.md`:
  - Extermination Order's cooldown is 4 (finding AR1; approved, RUL-2026-10-16-004);
  - Tempest Cleave needs no self-hit floor (TC1);
  - the authored ≤6 gate on the global Worldbreaker Chorus is kept;
  - Veilstep is used with its captured record, Stealth 1 round / cooldown 5 (SRC1; RUL-2026-10-16-007).
- **No fabricated IDs.** Every equipped jutsu ID comes from a committed operator capture, and the two weapons from the pinned upstream seed. New entities (exclusives, Countermand, Beacon, caches, the 20 AIs) are symbolic refs.
- **Never compile the failed `state/silent_bastion_condensed99_candidate.json`** (C1).
- **Nothing here goes under `push/`.** Turning this into a live manifest needs fresh captures, director acceptance of the docket, and an operator-run hidden write.
