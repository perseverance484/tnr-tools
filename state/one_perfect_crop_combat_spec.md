# One Perfect Crop — combat AI/profile specification

**Task:** `content.combat_ai_profiles`  
**Lead:** ChatGPT / Content Designer  
**Implementation owner:** Fable / Claude Code after final freeze  
**Live-game actor:** dauntless only  
**Source branch baseline:** `chatgpt/one-perfect-crop-roadmap-20260911` at `35e8a6f4bebf5abaa1b4f012c55108559002c389` before this file was added.  
**Status:** implementation-exact behavior resolved; AI-record completion remains blocked only on the residual director-owned fields listed below.

## Authority and provenance

This specification translates the frozen One Perfect Crop combat intent in `state/plan_one_perfect_crop_finish.md` and the Road Bandit reuse resolution in `state/one_perfect_crop_bandit_resolution.md` against the current AI contract in `skills/building-tnr-content/references/ai.md`, generated constructors, shared-jutsu pool, and current builder behavior.

It does not authorize any live request. It does not create jutsu, edit shared AI, choose unresolved balance values, or replace the canonical sources above.

## Director ruling: default AI rules

For both One Perfect Crop enemies, set:

- `includeDefaultRules: true`

The engine appends its default catch-all behavior **after** the authored custom rules. For this event, that appended tail provides:

1. use highest-power legal action;
2. movement toward the opponent.

Therefore the custom behavior chain must **not** duplicate highest-power fallback, movement fallback, or anti-exhaust/resource-starvation rules. The default-rule tail owns those cases. This supersedes any earlier working assumption in this task that `includeDefaultRules` should be false or that explicit terminal movement/anti-exhaust rules should be authored.

Practical consequence: all approved kit attacks cost 60 AP. If no authored specific-jutsu rule can execute, the appended default rules handle the legal fallback and movement path; no bespoke exhaustion branch is required.

## Shared combat facts

Both encounters use exactly one enemy and retain the frozen quest-level battle setting `opponent_scaled_to_user: true`.

Shared AI-record contract:

- technical rank: `JONIN`
- element: None / no elemental identity
- stat ratio shape: neutral/even across all twelve stats; no bespoke offensive or defensive bias
- `statsMultiplier: 1`
- `poolsMultiplier: 1`
- `regeneration: 60`
- no passive AI tags/effects
- no bespoke control, healing, shields, buffs, seals, wounds, pierce, poison, charge mechanic, adaptive counterplay, or signature jutsu
- all jutsu are existing shared-pool records; no replacement or event-local jutsu may be minted
- AiProfile: custom ordered rules plus `includeDefaultRules: true`
- custom rules must be constructed from the generated rule constructors rather than hand-authored from memory

All four approved shared jutsu are range 5 and cost 60 AP. A specific-jutsu custom rule therefore uses the canonical `distance_lower_than` range gate at value `6` (range + 1), then the canonical `use_specific_jutsu` action for the literal existing jutsu id. Constructor defaults, including action/condition descriptions and target defaults, should be preserved unless the frozen event contract explicitly requires an override.

## Road Bandit

Create a **new generic Road Bandit AI + its own AiProfile**. Do not edit any shared live AI.

### AI record

Fixed values:

- name/identity: Road Bandit
- rank: `JONIN`
- scale-to-user encounter flag: ON (`opponent_scaled_to_user: true` on the battle objective)
- element: None
- neutral/even twelve-stat ratio shape
- `statsMultiplier: 1`
- `poolsMultiplier: 1`
- `regeneration: 60`
- no passive AI effects/tags
- preferred combat flavor: Bukijutsu
- jutsu loadout, exactly and only:
  - S27 Weakening Strike — `YiRdVytsdxFzZtqkEDs5Q`
  - S41 Steady Strike — `fKvCGRgzGNskgFWocQCAg`
  - S40 Measured Strike — `kkGDat1XWUxhOQ1_T5025`

Residual director-owned AI-record values are listed under **Open director decisions** below. Fable must not infer them.

### AiProfile

Set `includeDefaultRules: true`.

Author exactly these custom priority rules, in this order:

1. **Weakening Strike**
   - condition: `distance_lower_than`, value `6`
   - action: `use_specific_jutsu`, jutsu id `YiRdVytsdxFzZtqkEDs5Q`
2. **Steady Strike**
   - condition: `distance_lower_than`, value `6`
   - action: `use_specific_jutsu`, jutsu id `fKvCGRgzGNskgFWocQCAg`
3. **Measured Strike**
   - condition: `distance_lower_than`, value `6`
   - action: `use_specific_jutsu`, jutsu id `kkGDat1XWUxhOQ1_T5025`

Do **not** author additional custom fallback rules. After these three rules, the engine-appended default chain supplies highest-power legal action and movement.

This implements the frozen design intent — close distance as needed, prefer Weakening Strike, then Steady Strike, then Measured Strike, then ordinary legal fallback — without duplicating engine defaults.

## Harvest Boar

Create a **new Harvest Boar AI + its own AiProfile**.

### AI record

Fixed values:

- name/identity: Harvest Boar
- rank: `JONIN`
- scale-to-user encounter flag: ON (`opponent_scaled_to_user: true` on the battle objective)
- element: None
- neutral/even twelve-stat ratio shape
- `statsMultiplier: 1`
- `poolsMultiplier: 1`
- `regeneration: 60`
- no passive AI effects/tags
- no special charge mechanic
- jutsu loadout, exactly and only:
  - S27 Weakening Strike — `YiRdVytsdxFzZtqkEDs5Q`
  - S42 Forceful Strike — `4TM6iS8P0qgNHsFpALFhg`
  - S41 Steady Strike — `fKvCGRgzGNskgFWocQCAg`

Residual director-owned AI-record values are listed under **Open director decisions** below. Fable must not infer them.

### AiProfile

Set `includeDefaultRules: true`.

Author exactly these custom priority rules, in this order:

1. **Weakening Strike**
   - condition: `distance_lower_than`, value `6`
   - action: `use_specific_jutsu`, jutsu id `YiRdVytsdxFzZtqkEDs5Q`
2. **Forceful Strike**
   - condition: `distance_lower_than`, value `6`
   - action: `use_specific_jutsu`, jutsu id `4TM6iS8P0qgNHsFpALFhg`
3. **Steady Strike**
   - condition: `distance_lower_than`, value `6`
   - action: `use_specific_jutsu`, jutsu id `fKvCGRgzGNskgFWocQCAg`

Do **not** author additional custom fallback rules. After these three rules, the engine-appended default chain supplies highest-power legal action and movement.

## Open director decisions

Current canon does not deterministically fix every field required to create the two AI records. These are content/balance decisions and remain intentionally unresolved.

### Road Bandit

- stored AI `level`
- `preferredGeneral1`
- `preferredGeneral2`
- equipped armor choice: `None` or `AI Light`

`preferredStat` is already fixed as `Bukijutsu` by the approved combat identity.

### Harvest Boar

- stored AI `level`
- `preferredStat`
- `preferredGeneral1`
- `preferredGeneral2`
- equipped armor choice: `None` or `AI Light`

The neutral/even twelve-stat ratio does not itself determine `preferredStat` or preferred generals. Armor is an editor-side identity/mitigation choice and is not inferred from the neutral stat shape.

## Implementation guardrails

- No live-game request in implementation or review.
- No shared AI edits.
- No new jutsu.
- Use the exact literal shared-pool jutsu ids above.
- Keep all creates hidden until the user separately decides to publish/unhide.
- Use generated constructors for AI rule objects; do not hand-author remembered shapes.
- Preserve `includeDefaultRules: true`; do not expand the manifest with redundant highest-power, movement, or anti-exhaust custom rules.
- Preserve one enemy per battle and the frozen hard-fail loss routes in the quest graph.
- Do not treat scale-to-user as permission to guess stored AI `level`; level remains an explicit AI-record input unless the director sets it.

## Completion state

The AiProfile behavior portion of `content.combat_ai_profiles` is fully resolved and implementation-exact.

The overall task remains blocked on the nine director-owned AI-record selections above. Once those values are supplied, this document can be completed without any additional combat-design invention and handed to Fable for manifest implementation after the workstream's final freeze gate.
