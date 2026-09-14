# Godstorm — Tower of Endless Night 1–3 readiness audit

Date: 2026-09-14
Role: ChatGPT / Release Auditor (supporting lenses: Content Designer, Art Director)
Base main SHA: `c02beb97e7fc481c3db0fc6cc2d2af744657d258`
Audit branch: `chatgpt/godstorm-pyramid-readiness`

## Scope

Finalization review for the three live Godstorm battle-pyramid quests:

- `VjT93rkmWlWlrdG6Pp46e` — The Tower of Endless Night: Dawnless Crown
- `2yvE9PUQqlD8lbYNfgX-b` — The Tower of Endless Night: The Marrow Vaults
- `OSADdXqostbyVliCxWk6k` — The Tower of Endless Night: The Stormcourt

User reports the three pyramids, AI, and quests are active. Live-game operation remains user-owned. This review performs no live mutations.

## Preliminary verdict

**AMBER — live, but not final-certified.**

The current repository is sufficient to identify the three quest roots and establish the canonical QA rules, but it does not yet contain fresh full live read-backs of the active quest graphs and all directly referenced combat/art content. Final balance, structural, and visual sign-off therefore remains open.

Do not equate seed-catalog values with current live state. Under `docs/00_INDEX.md`, fresh captures govern live-record assertions.

## Evidence established before fresh capture

- All three quest roots are present in the seed quest catalog as S-rank, level 70–100 `battlepyramid` quests.
- Seed visibility/hidden values are not authoritative for current live state and conflict with the user's report that the quests are active; this is a capture requirement, not a release conclusion.
- Asset discovery catalog contains obvious bespoke candidates `marrow vault 1`, `marrow vault 2`, `marrow vault 3`, and `StormCourtyard`.
- No asset-name search hit containing `Dawn` was found. This does **not** prove Dawnless Crown lacks art; the live quest may point to an asset under another name or URL.
- The latest upstream contract drift at base main affects farming-item fields rather than quest/AI/battle-pyramid structure and is not presently a Godstorm blocker.

## Canonical structural QA requirement

Per `skills/building-tnr-content/references/quest.md`, every `start_battle` objective in a battle pyramid must be gated by its preceding dialog, and loss/failure must route back to the corresponding battle stage. The audit must reject any graph that permits floors to co-activate, skip, or fall through incorrectly.

## Capture authorization and manifest

The user approved capture for the three quests and all related content. The capture is intentionally split into two read-only phases so that related entity IDs are derived from authoritative quest records rather than guessed from catalog names.

### Phase 1 — root quest read-back

Manifest: `push/23_godstorm_tower_root_capture.json`

It contains exactly three `quests.get` full-persist reads and zero mutation items.

Purpose:
- capture current quest metadata;
- capture objective graphs and ordering/gates;
- discover exact AI/opponent references;
- discover exact reward references;
- discover exact scene/game-asset references;
- provide the closure set for phase 2.

### Phase 2 — related-content closure capture

Generate only after the phase-1 harvest is committed. Follow every direct reference in the three captured roots and full-persist the applicable records, including as present:

- AI/user records;
- AI profiles;
- jutsu used by those AI;
- referenced reward items/bloodlines;
- referenced game assets;
- any other direct entity IDs required to establish the pyramid's actual combat or presentation state.

Do not expand scope from thematic/name similarity alone. The legacy `Emergency Hunt: Godstorm` is not automatically part of this audit.

## QA gates after capture

### Quest graph / functional gate

For each tower:
- verify current `type`, rank, level bounds, active/hidden state, and requirements;
- inspect objective ordering and lock/gate semantics;
- prove each battle floor is dialog-gated;
- prove loss/failure loops back to the intended battle stage;
- prove no simultaneous unintended floor activation or skip path;
- prove final completion path and rewards are reachable once and only as intended;
- verify scene/background asset references resolve.

### Combat / AI balance gate

For every referenced opponent:
- verify level, HP/CP/stat profile, and progression across floors;
- inspect AI profile and jutsu kit together rather than rating raw stats alone;
- identify sustain, control, burst, status/immunity, resource, or action-economy combinations that create non-obvious spikes;
- compare Tower 1 → Tower 2 → Tower 3 progression and intra-tower boss spikes against captured live S-rank / equivalent references where available;
- inspect reward progression against encounter burden.

Balance/reward changes are recommendations only until the user approves them.

### Visual gate

For each quest/floor presentation surface:
- identify exact currently wired asset and native placement/crop;
- distinguish intentional reuse from missing/default art;
- inspect readability at native scale and likely crop states;
- build an art contract and brief for each genuinely missing or insufficient image;
- generate and QA replacements only after current wiring is known.

Current likely investigation priority is Dawnless Crown because no obvious `Dawn`-named candidate appears in the asset discovery catalog, followed by verification that the three Marrow assets and `StormCourtyard` are actually wired to the intended stages.

## Readiness axes

| Axis | Current status | Reason |
| --- | --- | --- |
| Live activation | User-reported live | Must not be re-operated by reviewer |
| Quest graph correctness | Unverified | Fresh full root capture pending |
| AI functional state | User-reported active | Exact referenced records/capture pending |
| Balance | Not final-QA'd | Requires captured graph + related AI/profile/jutsu closure |
| Visual coverage | Partial/unverified | Bespoke catalog candidates exist; live wiring/native QA pending |
| Rewards | Unverified | Fresh quest read-back pending; user owns final balance |
| Final acceptance | **Not yet** | Structural + combat + visual evidence gates still open |

## Safest next sequence

1. User/operator executes the read-only `push/23_godstorm_tower_root_capture.json` through the normal protected capture workflow and commits the harvest/result evidence.
2. ChatGPT derives the exact related-content closure set from those three records and authors the zero-mutation phase-2 capture manifest.
3. User/operator executes phase 2 and commits the result evidence.
4. ChatGPT performs the full structural, balance, reward, and visual wiring audit and produces explicit recommended adjustments.
5. User decides balance/reward/art-direction changes and publishing/final acceptance.
6. Any approved content mutation is handed to the normal implementation owner under `docs/DEVELOPMENT_WORKFLOW.md`; live execution remains user-owned.

## Current blocker statement

No defensible final-product readiness percentage or final balance verdict should be issued before the two-stage fresh capture closes the evidence gap. Present classification is **AMBER / live but not final-certified**.
