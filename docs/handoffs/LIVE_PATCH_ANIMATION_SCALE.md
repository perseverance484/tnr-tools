# Handoff: Forge livePatch (per-effect animationScale derived from live)

Lane A. Branch `fable/live-patch-animation-scale`, base `f277a6a` (main).

## Why
Job 593 sets `animationScale` 2.5 on the Mother of Echoes' 57 remaining jutsu (~800 KB of effects).
`jutsu.update` takes only full records, and a manifest carrying every effect cannot pass the connector
relay. livePatch lets an edit item say "set the scale on these effects" and has Forge build the full
record from the live read at send time, the way the in-game editor does.

## Behaviour
- Item key `livePatch: {animationScale: <1..3>, assets: [<asset id>, ...]}` on a jutsu/item/bloodline edit.
  Parse refuses: other entities, creates, `data.effects` alongside it, unknown keys, out-of-range scale,
  empty asset list (`forge/src/runner/livepatch.mjs`, `manifest.mjs`).
- Effect i is patched iff one of its appear/static/disappear animations is a listed asset. Every other
  effect and key goes out exactly as live holds it. Effects mixing listed and unlisted clips are scaled
  and counted (`livePatched.mixed` in the journal).
- `_fill` derives effects from the read it already takes after the throttle wait; `targeted 0` FAILS the
  item unsent (wrong target or asset list). An already-patched record is still sent (idempotent); the
  journal's send-less PLANNED -> CONFIRMED guard (Bloodright only) is NOT widened.
- Verify and SENT-reconcile add `livePatchDiffs`: every targeted effect must hold the scale. Reconcile no
  longer reports "no asserted keys" for a livePatch item with empty data.
- `livePatch` is part of the item payloadHash only when present (existing hashes unchanged).

## Review round 1 (ChatGPT at 419b3e74): both P2s fixed
- P2-1: `livePatchDiffs` now reports a diff when the record has no effects array, or no effect uses a
  listed asset; a match needs a non-empty target set all at the scale. Verify and reconcile both use it,
  so a write whose targets vanished resumes as drift/orphan, never VERIFIED. Tests 9 and 11.
- P2-2: suggest mode refuses `livePatch` at parse (the suggestion path builds from planned.data only).
  Test 10.

## Gates
- `node --test forge/test/livepatch.test.mjs`: 11/11.
- `npm test` (forge): 834 tests, 805 pass, 14 fail, 15 skipped - the identical 14 names failing on main here (this checkout lacks the historical fixtures; the reviewer, with them fetched, saw the same 4 on base and head).
- `npm run build` then `node forge/tools/check_bundle_budget.mjs`: raw 486,756/490,000, gzip 117,589/119,000.

## Not done
No live requests from this branch. No browser run. Job 593 manifest is generated separately on main.
