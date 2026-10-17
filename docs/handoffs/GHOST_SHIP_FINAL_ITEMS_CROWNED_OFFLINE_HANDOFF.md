# Handoff — Ghost Ship / Skyglass final 2/2 items + Crowned Captain support (Fable → ChatGPT review)

Format: `docs/workflows/IMPLEMENTATION_HANDOFF.md`. Results: `docs/reviews/GHOST_SHIP_FINAL_ITEMS_CROWNED_OFFLINE_RESULTS.md`.

## Repository / refs

- Repository: `perseverance484/tnr-tools`.
- Implementation branch: `fable/ghost-ship-final-items-crowned-20261011` (new, single writer: Fable).
- Base: design head `fd7f021762940f11c3896c70b2af3bc53f7711dc` (`coord/ghost-ship-combat-item-decisions-20261011`). It was delivered as `ghost-ship-crowned-support-approved.bundle` (SHA-256 `8aac7e271ed8cfc27e497c71f6ad1c9da460a80491d2be11e14a992281a8fdb4`, prerequisite `3f825562…`); `git bundle verify` passed and `FETCH_HEAD` equalled `fd7f0217…`.
- Head: the commit that adds this file. Its exact SHA is in the delivery message. Review that SHA, not the branch name.
- Remote state verified at start: `main` `50f980f08dfcc798723c26243b9399cc0a97911a`; `ccr-71fd390f-0j0g78` at r4 `3f825562…`; `fable/ghost-ship-active-consume-20261011` at `fcd79e5a…`, which the user authorized pushing from the earlier bundle during this session.
- Not modified: frozen r4, the 3/3 package `fcd79e5a…`, the `coord/` design branch, `chatgpt/*`, and the global September Forge state.

## Scope

**Added:**
- `harness/ghost_ship_final/`: a versioned successor of the 3/3 harness, with:
  - the final record builder;
  - the CONTRACT/GUARDS/ACTIVE suites at 2/2;
  - the new CROWNED suite;
  - the runner, tools and self-tests;
  - committed results and provenance.
- `state/ghost_ship_skyglass_final_item_records.json`: the derived final Katana/Crystal candidate records, with field provenance, unapproved Crystal carrier fields and exact historical diffs.
- `docs/reviews/GHOST_SHIP_FINAL_ITEMS_CROWNED_OFFLINE_RESULTS.md` and this file.

**Modified (status pointers only):**
- `state/ghost_ship_skyglass_reward_decisions.md`: open gate 1 now points at this evidence, and a gate 4 for the unapproved Crystal carrier values was added.
- `state/ghost_ship_skyglass_crowned_support_behavior.md`: an "offline test status" pointer. No approved value changed.

## Verification (exact)

- Historical reproduction first: `harness/ghost_ship_consume/run.sh` → 34 pass / 0 fail / 195 expect(). All four evidence files are byte-identical to `fcd79e5a…`.
- `python3 harness/ghost_ship_final/tools/build_final_items.py --check` → current. The 3/3 builder `--check` → current.
- `harness/ghost_ship_final/run.sh` (twice) → exit 0:
  - M0 482/0;
  - `bun test` 45 pass / 0 fail / 220 expect() across 3 files;
  - evidence CONTRACT 19/0, GUARDS 24/0, ACTIVE 81/0, CROWNED 36/0, all clean;
  - negative probes 5/5 enforced;
  - 1,780 pinned engine files unchanged before and after.
- The two runs produced byte-identical `m0/contract/guards/active/crowned.json`.
- Doctrine, law, pack and generated-contract gates do not apply: no `skills/`, doctrine or generated file changed.

## Source / runtime

Engine `studie-tech/TheNinjaRPG@585534d7eb21d6f0dd678d5c3eb92662f611d39b` (upstream, deployment unverified), exported with `git archive`. `bun.lock` sha256 `da6602f2…1906c08`. The existing approved frozen install was reused; no install was run. Bun 1.4.2, Node v22.22.0, Python 3.13.16.

Isolation: **unshare mode** (`unshare -rn` was available here) plus seccomp socket denial. Socket preflight passed. The environment is an `env -i` allowlist, and Bun runs with `--no-env-file --no-install`. No database is used.

## Findings to attack hardest

1. **2/2 lifetimes** (engine round advancement):
   - The buff is present at offsets 0–2 and gone at +3. The final eligible hit is at +2 and the first ineligible hit at +3.
   - The +2 shield lasts to +4.
2. **Overlap observation:** at 2/2 the 3-round shared Consume GCD outlasts the buff. A second Crystal weapon becomes usable only at +3 and converts 10%, not 20%. The overlap decision stays deferred; nothing was restricted.
3. **Non-craftable proof:** the final Crystal is rejected as "not craftable" even with the old recipe restored and the materials held. With only the flag flipped, the same inputs reach the first write (a transaction). The stub gained read-only `userQuests: []` and `completedQuests: []` profile fields, which the post-guard craft path reads.
4. **Trade is schema/record evidence only.** No auction procedure was executed.
5. **Crowned support:**
   - The strict 40 boundary (engine ratio exactly 40 does not heal).
   - IDG ≥ 71 is inclusive.
   - Copy is broad, does not remove the opponent's buffs, and can be empty for expired, protected or item sources.
   - CLOSEST_OPPONENT targeting lets a low-IDG summon block Copy.
   - Reflect returns damage without reducing it.
   - In fights, tempo is lower and survivability higher when hurt; outcomes are unchanged in these fixtures.
6. **Fixture limits:**
   - Injected effects and HP fractions.
   - Fixed placements and source-default damage settings.
   - Historical player carriers; single-opponent deterministic seeds.
   - The DDT sign normalisation seen during Copy processing (40 → −40 stored) is engine behaviour, recorded as evidence.

## Open decisions (not settled here)

- Crowned rule order and selector, and acceptance of the measured tempo/survivability change.
- The 14 unapproved Crystal carrier values.
- Katana and Crystal presentation and art.
- Filament trading and use.
- The deferred Consume overlap.
- The Sealwright behaviour proposal (not accepted; not tested).
- The nine-AI remap, minion IDG, legacy hash re-baseline, deployment/settings capture, and a fresh operator quest capture before edits.

## Not done

Live-game requests 0, writes 0, CDN 0, credentials none. No browser or client checks. No engine edit, tuning, art, manifest, publication, unhiding or quest edit. No integration into `main`. Independent frozen-SHA review is required.
