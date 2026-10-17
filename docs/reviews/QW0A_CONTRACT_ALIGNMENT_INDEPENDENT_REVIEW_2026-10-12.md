# QW-0A independent review — 2026-10-12

**Disposition: ACCEPTED as a report-only `BLOCKED_BY_SOURCE_ADOPTION` outcome.** The decision not to adopt is independently reproduced. This is **not** an `ALIGNED` verdict, a validator fix, source-adoption approval, or permission to start another work package. The follow-up acceptance criteria need the refinements below before becoming an implementation brief.

Lead: Release Auditor. Supporting lens: Engineering Auditor. Lane A, independent review only.

## Exact scope and authority

| Ref | Verified SHA |
| --- | --- |
| Shared `main`; implementation base and merge-base | `4de2668bb947368113683b5cb97e197abc87df27` |
| Approved planning branch `chatgpt/quest-workflow-skyglass-retrospective-20261012` | `c34f7de572337b0d2cfe397b9331502aa6548e27` |
| Reviewed `fable/qw0a-contract-alignment-20261012` snapshot | `5fefb70b88f140c3212d0b9d94209e70be44f2bb` |
| Upstream `studie-tech/TheNinjaRPG` main observed during review | `f8c04d029ea58007bf2947dbddb94c446e15dbb5` |

The Fable commit is a direct child of the verified main. Its entire delta is five new files: `docs/reviews/QW0A_CONTRACT_ALIGNMENT_REPORT.md` and four files under `docs/reviews/qw0a_evidence/`. No code, generated contract, Forge resource, manifest, exception ledger, doctrine, or session projection changed.

The governing plan, QW-0A brief, QW-1 brief, and RUL-2026-10-12-016 were read at the approved planning SHA. They are **not yet on main or the reviewed Fable tree**. Read them with `git show c34f7de572337b0d2cfe397b9331502aa6548e27:<path>`; a missing working-tree file does not revoke the approval or authorize reconstructing it from chat.

Also read the repository router, ChatGPT/Claude guides, development workflow, role files, Fable review/handoff workflows, content-workstream workflow, D-adopt-gate, relevant rulings, and the actual extractor/diff/validator/Forge sources. RUL-2026-10-12-013 through -015 still govern the historical exceptions. RUL-2026-09-08-004 governs law reconciliation.

**Freeze evidence:** a completed report exists at the exact immutable commit above; the remote branch remained at that SHA throughout this review. No associated PR or separate explicit author freeze attestation was found. This review does not assert that Fable has stopped all work. Before integration, confirm the handoff freeze and reverify the branch and main. Any later head requires a separately scoped check.

## Findings and follow-up constraints

### QW0A-R1 — Refine the proposed extractor acceptance criteria before implementation

**Classification:** confirmed report/specification mismatch; medium consequence for the next implementation, not a regression introduced into runtime code.

`QW0A_CONTRACT_ALIGNMENT_REPORT.md:183-191` proposes general array-spread resolution but says a corrected extraction at `bdec2883` should differ from the stamped files only by the basic-element correction. That is too narrow even at the existing atom-comparison level.

The stamped 45e also contains these literal, unresolved spread entries:

| Constant | Stamped members that are expressions, not real members | Pinned source |
| --- | --- | --- |
| `allState` | `...publicState`, `...privateState` | `bdec2883:app/src/libs/combat/constants.ts:126` |
| `damageModifierTypes` | `...damageReductionTypes`, `...damageBoostTypes` | same file, lines 146-166 |

A correct general spread resolver changes these too. The requested `msg()` / `type()` / reward-spread support also repairs omissions already present at the old source pin: `combat.ts:51-57,101,409,704-706`; stamped 45c lacks the corresponding descriptions, inherited direction and reward fields. The current diff tool does not even inventory most of those non-enum union fields.

**Smallest correction:** require a source-cited inventory of all extractor corrections at both pins, separating real upstream changes from corrections to the old extraction. Compare full structural payloads as well as gate atoms. Do not require “only the element correction” or “only G1-G4” as a complete allowed-change list, and do not suppress legitimate corrections to make that list pass. Keep extraction in scratch; adoption remains a separate gate.

### QW0A-R2 — The existing gate has additional blind spots; carry them into the next scoped brief

**Classification:** independently test-proven, pre-existing tooling debt; not caused by this report-only branch.

Fable correctly reports that removing `AllTags.damage.power` is invisible to `schema_diff.py`. Two adjacent cases also reproduce against the exact target:

| Disposable change to a stamped contract | Actual result |
| --- | --- |
| Delete non-enum union field `AllTags.damage.power` | exit 0, zero changes |
| Change that field's type from `number` to `string` | exit 0, zero changes |
| Tighten `item.requiredStrength.nullable` from true to false | exit 0, zero changes |

`skills/building-tnr-content/scripts/schema_diff.py:68-92` records only enum members for union fields and records no nullability atoms. Therefore a green diff cannot prove the whole field/type/nullability contract. This is especially relevant to the QW-0A brief's explicit requirement to record those dimensions.

**Smallest correction to follow-up scope:** explicitly cover union field existence and type changes; either add a separately reviewed nullability comparison or retain an explicit manual blocker for that dimension. Do not describe nullability as mechanically checked before that exists. This review does not authorize changing the gate or adopting contracts.

The `now-required` diagnostic also needs careful treatment. A scratch entity gaining a genuinely required `string` field currently exits 1, albeit with the misleading label “optional -> required.” Correct the label without losing rejection of genuinely new required inputs. Distinguish optional/defaulted/preprocessed inputs using source evidence; absence from the old file alone does not make an addition safe.

### Small source-description corrections

- G1 at report line 81: the four damage-given/taken tags **retain** `elements`; they previously inherited it from `IncludeStats`. The removed `statTypes` and `generalTypes` claims stand.
- Q1 at line 90: not all 24 fields use `.prefault(...)`. The `required*Mastery` fields use `makeCappedNullableNumber`; at `585534d7:app/src/validators/base.ts:10-14`, omitted input becomes null through preprocessing. The conclusion that omission is accepted stands; the mechanism should be stated accurately.

These qualifications do not overturn the stop decision or require changing historical exceptions.

## Independently reproduced evidence

All extraction used the reviewed repository tools and exact public source commits. Constructors were extracted first. Source was read, not executed as a game/server. Generated files and probes remained outside the tracked repository.

| Source pin | Invariants | 45c diff | 45d diff | 45e diff |
| --- | --- | --- | --- | --- |
| `bdec2883748f029a0ecb93505adfdcbae6851fe9` | exit 0; 128 variants | exit 0; no atom delta | exit 0; no atom delta | exit 0; no atom delta |
| `585534d7eb21d6f0dd678d5c3eb92662f611d39b` | exit 0; 139 variants | exit 1; 219 breaking | exit 1; 42 breaking | exit 1; 45 breaking |
| `6e4429d65f466b0df9fca3f9917b6dd427df7573` | exit 0; 139 variants | exit 1; 219 breaking | exit 1; 42 breaking | exit 1; 47 breaking |
| `f8c04d029ea58007bf2947dbddb94c446e15dbb5` | exit 0; 139 variants | exit 1; 219 breaking | exit 1; 42 breaking | exit 1; 47 breaking |

- All **939 added/removed atom entries** in the committed release-pin evidence reproduce, accounting for multiline atom values.
- Repeating `--ctors`, `--entities`, and `--constants` with identical release-pin inputs produced byte-identical output. Generated source-drop labels affect metadata hashes; no provenance-bearing output was adopted.
- The release-pin constructor hash reproduces exactly: `afa6468da32cd77921114a2f49541cf74c553ce2e38a82897671391351a3d415`.
- Source inspection supports the reported multiline-Zod, array-spread, cross-file helper and object-spread blind spots, as well as real removed stat/tag fields.
- `validate.py` on historical push/90 reproduces **56 errors / 25 warnings** with stamped contracts and **143 errors / 17 warnings** with the fresh release-pin extraction; both exit 1. A naive adoption makes validation worse.
- A disposable item with `damage.elements=["Fire"]` reproduces the false enum rejection; the otherwise equivalent Ice probe has no element error. This is not a claim that either incomplete probe is a valid full manifest.

| Command / check | Independent result |
| --- | --- |
| Three `push/{90,93,94}_*.validate_exception.py` gates, invoked separately in check mode | exit 0 each; exact 56/25, 4/3, 4/3 ledgers hold |
| Three `node forge/tools/check_manifest.mjs <manifest>` invocations | exit 0 each; zero pre-send problems |
| `cd forge && npm test` | exit 0; **526/526**, including the three post-0056 tests |
| `factory.py --selftest`, cwd skill `data/` | exit 0; 20/20 |
| `validate.py --laws`, same cwd | exit 0; 4 asserted, 0 failed |
| Sector-removal negative fixture / additive positive fixture | exits 1 / 0 as expected |
| Bad-invariants negative fixture | exit 1; 3 invariant errors |
| `build_packs.py --check` | exit 0; packs/TOCs current |
| `lawmap.py <repo>` | exit 0; 0 errors, 5 existing warnings |
| `doctrinemap.py <repo>` | exit 0; 0 errors, 0 warnings |
| `render_doctrine.py --check` | exit 0; projections current |

The four coherence scripts live under `skills/building-tnr-content/scripts/`, not root `scripts/`. Initial reviewer invocations at the wrong path exited 2 and were corrected; they are not product failures. Initial focused Forge execution lacked installed dependencies, and offline npm installation lacked cached packages. The suite was then run using existing local dependencies after verifying an identical lockfile and all installed package versions against it; no dependency or lockfile changed.

The extraction matrix and probe outcomes are also recorded in `docs/reviews/qw0a_review_evidence/verification_2026-10-12.json`.

## Reproduction recipes

Set `R` to a checkout at the reviewed SHA, `S` to a source-only checkout/export at one exact source SHA above, and `O` to an empty scratch directory. These are paths, not instructions to contact the game.

```sh
X="$R/skills/building-tnr-content/scripts"
D="$R/skills/building-tnr-content/data"
python3 "$X/schema_extract.py" "$S" --ctors > "$O/ctors.json"
python3 "$X/schema_extract.py" "$S" --entities > "$O/entities.json"
python3 "$X/schema_extract.py" "$S" --constants > "$O/constants.json"
python3 "$X/schema_extract.py" "$S" --checks > "$O/checks.json"
python3 "$X/schema_diff.py" --invariants "$O/ctors.json" --constants "$O/constants.json"
python3 "$X/schema_diff.py" diff "$D/45c_DATA_constructors.json" "$O/ctors.json"
python3 "$X/schema_diff.py" diff "$D/45d_DATA_entity_schemas.json" "$O/entities.json"
python3 "$X/schema_diff.py" diff "$D/45e_DATA_constants.json" "$O/constants.json"
```

Record each exit separately; a nonzero candidate diff is the expected stop, not permission to suppress it. To reproduce the counterfactual, run from `D`:

```sh
python3 "$X/validate.py" "$R/push/90_ghost_ship_skyglass_release.json"
python3 "$X/validate.py" "$R/push/90_ghost_ship_skyglass_release.json" --ctors "$O/ctors.json" --entities "$O/entities.json" --checks "$O/checks.json"
```

The three blind-spot probes change one field of a disposable JSON copy as specified in QW0A-R2, then run the same `schema_diff.py diff OLD COPY` command. Do not change the stamped files.

## Integration, sequence and remaining decisions

1. The investigation/report is useful, reproducible evidence and may proceed through the normal documentation integration process, with this review's refinements retained. No merge was performed in this session. Reverify live refs and the author freeze before integration.
2. QW-0A **alignment remains blocked**. Prepare any extractor-fidelity and gate-hardening continuation as its own bounded Fable brief, incorporating R1/R2; do not treat section 9 of the author report as automatically approved implementation scope.
3. D-adopt-gate still requires exit 0. Any policy allowing deliberately reviewed removals requires a concrete proposal, a separate ruling, and an intentional change to its canonical owner. No such decision was made here. Historical SHA-scoped content exceptions do not grant contract-adoption permission.
4. **QW-1 remains queued after QW-0A review/integration.** This review does not start it or silently require completion of every possible QW-0 follow-up. At the integration checkpoint, record the residual QW-0 blockers and use the approved QW-1 brief; a changed order needs an explicit decision.
5. QW-0B, other QW-0 follow-ups, QW-2 through QW-5 and Quest Studio integration were not begun. No second authority or task-status system was created.

The only current content roadmap is One Perfect Crop; there is no quest-workflow roadmap/task ID to initialize. This Lane A session therefore follows its approved plan/brief and durable review/handoff. Global September Forge state was read but not updated. `session_open.py` writes `state/digest.json`, so it was not run; equivalent applicable read-only guards were run directly. `session_close.py` was not run.

Rare Jewels remains the separate director-reported chance-based/up-to-three versus historical guaranteed-three discrepancy. No reward source or manifest was changed, no live reconciliation was attempted, and no public reward claim was issued.

**Safety and limits:** zero live-game requests, writes, credentials or CDN contact. No publishing/unhiding, gameplay changes, engine execution, implementation edits or active Fable-branch writes. Git/source retrieval was used. No source pin is established as the deployed production version. This review verifies offline tooling/report claims, not current live content.
