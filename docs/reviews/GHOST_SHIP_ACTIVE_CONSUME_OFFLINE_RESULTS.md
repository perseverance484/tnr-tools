# Ghost Ship / Skyglass — active Consume offline results

**Status: revised item test carriers PASS; production/content freeze remains open.**
Katana15 and Crystal10 execute under the changed active-Consume engine. The old
standalone-Crystal validator blocker is absent for positive-duration Consume at
this pin. Neither result chooses final timing, Crystal economy or balance.

**Authority:** RUL-2026-10-11-005 and the governing
`state/prompt_ghost_ship_skyglass_consume_revalidation.md`, design commit
`46df27172556807ab5bf723b0aa8c1251445ba2e`. Implementation is on
`fable/ghost-ship-active-consume-20261011`; independent frozen-SHA review is pending.
Historical r4 remains `3f825562ea051306a3803f47428b742ae5100011`.

## 1. Executed scope

| Gate | Result | Evidence |
| --- | --- | --- |
| M0 | 482 checks, 0 failed | Unchanged r4 repository verifier; original graph/kit/capture packets |
| CONTRACT | 16 checks, 0 failed | Full candidate Katana and Crystal validation; exact effects; provenance and baseline equality; instant-mode negative control |
| GUARDS | 17 checks, 0 failed | Real imbue/craft eligibility procedures; all 24 rank/rarity cells; weapon-only, non-imbuable, duplicate/slot, occupation, equipped, auction and required-skill cases |
| ACTIVE | 75 checks, 0 failed | Real weapon assembly/actions plus separately labelled processor controls |

Bun: **34 pass, 0 fail, 195 expect() calls, 2 files**. Five negative probes all
enforced. Every gate and source-integrity check exits 0. The full runner was run
twice; M0, CONTRACT, GUARDS, ACTIVE and provenance JSON are byte-identical.
Generated carrier `--check` is current. Evidence is in
`harness/ghost_ship_consume/results/`.

## 2. Derived record boundary

`state/ghost_ship_skyglass_active_consume_carriers.json` is a new, versioned test
packet. Its generator starts from push/85 Night's Testament and the disclosed
Flaming Sword Crystal shape donor. Capture, old-record and design-delta hashes
are embedded and checked. Katana's nine historical ruling/presentation override
fields remain the exact override set; all 65 other fields equal Night's Testament.
The old-to-new Katana record diff is exactly:

| Path | r4 | New test carrier |
| --- | --- | --- |
| `/effects/2/power` | 40 | 15, approved |
| `/effects/2/rounds` | 0 | 3, test input only |

Generated shield lifetime is explicitly 3 in both, now separately labelled an
unapproved test input. No other Katana mechanic/economy field changes. Presentation
nulls are filled by labelled placeholders only for validator/runtime execution.

Crystal has one Consume10 effect, CRYSTAL/WEAPON-only. Full RARE, EPIC and LEGENDARY
carriers validate; this is not a rarity choice. Instant `rounds:0` still fails the
same-array Damage/Pierce companion rule. Synthetic companion controls test that
rule; neither adds damage to the Crystal candidate.

## 3. Runtime findings

- Katana activates Consume on use, not equip. Its granting Pierce hit converts
  15%; different actions in the same round and later rounds also convert 15%.
  In the declared fixture the first shield is 221 HP; later actions add 159 and
  136 HP shields. These are carrier measurements, not promised live amounts.
- Crystal10 composes through actual battle assembly. A weapon with no authored
  damage can grant active Consume, then a later attack earns a shield. The old
  instant-only finding that this recipient was inert does not carry forward.
- Shielded-target controls confirm the pre-shield damage basis; Pierce and
  multi-target controls preserve the expected conversion/aggregation.
- **Same action:** weapon Consume15 plus appended Crystal10 realizes 15%, and
  two distinct Crystal records realize one 10% tag. SELF-tag deduplication remains.
  These are assembly controls, not approval for extra slots or duplicate imbues.
- **Separate casts:** two weapon carriers used three rounds apart can have
  simultaneous Consume10 buffs with durations `[1,3]`, converting at 20%.
  Reapplication creates independently timed buffs. Separately active processor
  sources aggregate up to 100% and use the longest generated-shield duration.
- With the 3/3 carrier, the buff rounds are `[3,3,2,1,absent]` from the cast round
  through +4. A shield earned at +3 remains after Consume expires: its rounds at
  +4/+5/+6 are 3/2/1, and it is gone at +7. Damage after buff expiry earns no shield.
- Clear removes active item Consume and stops subsequent conversion. Existing
  Buff Prevent survives Katana use but **does not suppress Consume** in the
  tested new source. The unchanged immunity blocks new Buff Prevent in the cast
  round and +1/+2; power100 Buff Prevent applies at +3. This records behavior,
  not an engine-correction authorization or balance acceptance.
- Residual, Poison, Health Drain and Wound controls attribute conversion to each
  original damage caster. Chakra/Stamina drain does not convert. Reflected damage
  uses the defender's Consume; other-caster damage does not inflate the owner's
  shield. Self damage, self-reflection and immediate/deferred recoil are excluded.
- Each generated shield caps at 100,000 HP in explicit oversized-hit controls;
  separate capped shields can coexist at 200,000 total. This is a per-grant cap,
  not a shared total-stack cap or legal-item damage recommendation.
- Katana remains AP40, costs40/40/0, range4 OTHER_USER, cooldown6 and shared GCD3.
  Out-of-range/self-target attempts reject without spending resources.

## 4. Eligibility and proof limits

The occupation procedures are actual pinned engine procedures. Their DB client is
read-only and traps the first write; `fetchUpdatedUser` is explicitly stubbed.
An eligible case therefore means **tested pre-write guards passed and a write was
reached**, not that imbuing persisted. No CAS/concurrency, profile refresh, atomic
crystal consumption or completed crafting transaction is claimed. The 12-Filament
craft carrier reaches its material check only at eligible ranks.

Published-state Katana rejects via `canBeImbued:false`; hidden Katana is not found
by the inventory fetch. Battle assembly also discards imbuements attached to a
non-imbuable recipient. New auction-reserved and missing/inactive-required-skill
Crystal cases reject; an active required skill passes to the trapped write.

Fixed tiles replace secure random spawn; source-default damage settings and
explicit player carriers are not a population model. Processor probes are separate
from real item assembly. No trained elemental/PvP boosts or summons are in these
carriers. The source-drift report assesses preparation, selectors and A1/A2
assumptions; it does not rerun or accept new-pin boss parity.

## 5. Source, isolation and reproduction

Engine: `studie-tech/TheNinjaRPG@585534d7eb21d6f0dd678d5c3eb92662f611d39b`,
162 commits after cddd7d91 (ancestor verified after deepening source history).
`bun.lock` SHA256: `da6602f2550bea9f1baf8508fa82b03d320bfcee269257f36cf25b47f1906c08`.
Both dependency manifests are byte-unchanged. The approved existing frozen install
was reused; no dependency install ran. Runtime: Bun1.4.2, Nodev24.19.0,
Python3.12.14. Node/Python differ from Fable's historical environment and are recorded.

`unshare -rn` is unavailable here. Runs explicitly select the fail-closed seccomp
mode: socket syscalls denied, extra inherited descriptors closed, `env -i`
placeholders only, Bun `--no-env-file --no-install`, no DB. IPv4/IPv6/Unix socket
creation is checked to return EPERM before engine import. Isolation failure cannot
be counted as a passing negative probe. No namespace-isolation claim is made.
All 1,780 pinned app files match git blobs before and after runs; only test files
were added to the export. Neither the checkout nor exported engine code changed.

Exact reusable command (paths identify this execution environment):

```bash
export PATH=/workspace/scratch/55944d57205e/r2-review-runtime/package/bin:$PATH
export TNR_NETWORK_ISOLATION=seccomp
export TNR_ENGINE_SRC=/workspace/scratch/55944d57205e/game-source
export TNR_ENGINE_WORK=/workspace/scratch/55944d57205e/consume-runtime
export TNR_DEPENDENCIES_APP=/workspace/scratch/55944d57205e/r2-review-runtime/engine/app
TNR_OUT=/workspace/scratch/55944d57205e/consume-runtime/final-a harness/ghost_ship_consume/run.sh
harness/ghost_ship_consume/run.sh
python3 harness/ghost_ship_consume/tools/build_item_carriers.py --check
python3 harness/ghost_ship_stage2/tools/build_katana_record.py --check
```

The upstream `tests/libs/combat/consume.test.ts` also passed 30 tests/93 expects
under socket denial before candidate-suite verification. It includes Sage and
positive Diffuse paths beyond this item suite; it does not substitute for item
assembly evidence. Generated source contracts, doctrine and skill files were not
changed or adopted. A preliminary substring-filter run included adjacent development
copies; the final runner uses an explicit suite path and the counts above exclude
them. Final results and provenance come from the final runner, not that prototype.

## 6. Remaining authority gates

Director decisions remain: active Consume duration and generated-shield lifetime;
Consume-on-Consume policy; Crystal rarity/trading/crafting access; Katana prose,
image and animation/SFX. Existing Sealwright order/closing/filler/parity, Crowned
support, nine-AI remap, minion innate IDG and legacy hash re-baseline gates remain.
Fresh operator quest capture precedes any quest edit. Deployment/settings capture
is optional and absent. No engine correction is implemented or automatically required
by the former Crystal blocker at this source pin.

Live requests 0, writes 0, CDN requests 0, credentials none. No browser/client
checks, tuning, art, manifest, quest edits, publication, unhiding or main integration.
