# Skyglass Crystal — separate Lane A engine-correction proposal (NOT IMPLEMENTED)

**Historical old-pin proposal — RUL-2026-10-11-005:** Reviewed upstream `585534d7eb21d6f0dd678d5c3eb92662f611d39b` already allows positive-duration Consume without a Damage/Pierce companion. Do not implement this former validator-exemption proposal automatically. Current Crystal is weapon-only Consume10 with active-buff behavior; exact record/runtime revalidation is governed by `state/prompt_ghost_ship_skyglass_consume_revalidation.md`. The original proposal below is retained as historical r4 evidence; no engine correction has been authorized or implemented here.

**Status:** PROPOSAL ONLY. Nothing here has been applied to `studie-tech/TheNinjaRPG`, to a scratch copy of it, or to any TNR manifest. Implementing it needs dauntless's explicit engine-change authorization and an upstream change owner.
**Date:** 2026-10-11. **Author:** Fable (Claude Code), Lane A.
**Evidence:** `harness/ghost_ship_stage2/` gates B1–B3 at engine pin `studie-tech/TheNinjaRPG@cddd7d91c9e6bdebc978ddcb61e5b8a305bd0f93`; results in `harness/ghost_ship_stage2/results/b1.json`, `b2.json`, `b3.json`.
**Design it serves:** RUL-2026-10-10-007. The Skyglass Crystal is a WEAPON-targeted `CRYSTAL` whose only effect is Consume 20%. This proposal does not change that design, add a filler Damage/Pierce tag, or relax the general rule.

## 1. Failing reproducer (gate B1)

`ItemValidatorRawSchema.shape.effects.safeParse([{ type: "consume", power: 20, calculation: "percentage", target: "SELF" }])` fails with exactly one issue:

> `ConsumeTag must be used together with a damage or pierce effect on the same action`

Source: `app/src/validators/combat.ts` `SuperRefineEffects` (consume/vamp branch). It is attached to the item `effects` array (`ItemValidatorRawSchema`, line 1600), so it runs before any item-level refinement can look at `itemType` or `crystalTargetTypes`. The full `ItemValidator` reports the same issue at `effects`. On their own, the tags parse (`shieldRounds` defaults to 3). Adding Damage or Pierce to the same array makes it pass. Vamp-only and Wound-only arrays are rejected by the same companion rule.

The harness test `B1 — Consume-only Crystal…` asserts this rejection and passes today. After a correction it must be changed to assert acceptance for the WEAPON-crystal case only (§4).

## 2. What already works at runtime (gate B2, hypothetical record)

The Crystal record cannot pass the validator, so it was built tag by tag. With that record:

- `processUsersForBattle` composes `[...weapon.effects, ...imbuement.effects]` for an imbuable weapon (`routers/combat.ts`, item loop). The weapon action then carries `consume`.
- The weapon action, run through `performBattleAction`, generates a self shield of `floor(20% × pre-shield damage)` for 3 rounds. It does this for a normal target and a shielded target (same shield, pre-shield basis). With multiple targets, it aggregates into one shield.
- A recipient weapon with no cast-round Damage/Pierce generates no shield. Nothing fails, so the Crystal is silently inert.

No engine change is needed for these runtime paths.

## 3. Runtime finding the director must weigh (not fixed by §4)

`insertAction` (`app/src/libs/combat/actions.ts`, SELF-target branch) realises a SELF tag once per stack key `type-creatorId-targetId-fromType`. The composed array puts weapon effects first. So:

- if the weapon already carries a SELF Consume (measured: Consume 40 + Crystal 20), the Crystal's Consume is **dropped** and the shield is 40%, not 60%;
- two Crystal Consume records on one weapon give 20%, not 40% (occupation.imbueItem already rejects a duplicate crystal ID).

`tags.ts consume()` would add ratios, but only across distinct stack keys. The readiness review's expectation that Consume ratios "add up to 100%" does not hold for one weapon action. The options are director-owned:

| Option | Effect | Engine change |
| --- | --- | --- |
| Accept | A Crystal on a weapon that already has Consume does nothing. Today no approved recipient has its own Consume. | none |
| Restrict eligibility | Add an imbue guard that rejects a Consume crystal on a recipient whose effects already contain Consume. Message the player. | small (occupation router) |
| Allow stacking | Exempt `consume` from the SELF dedupe so ratios add (capped at 100%). | broader; touches every multi-Consume action. Not recommended without a game-wide review |

## 4. Minimal validator correction (recommended shape)

Scope the exemption to a WEAPON-targeted CRYSTAL and to Consume only. Leave Vamp and Wound, every other item type, crystals that target other item types, and all jutsu, bloodline, sage-mode and skill-tree arrays exactly as they are.

Sketch only (not applied, not compiled):

```ts
// validators/combat.ts
export const SuperRefineEffects = (
  effects: ZodAllTags[],
  ctx: z.RefinementCtx,
  opts: { allowStandaloneConsume?: boolean } = {},
) => {
  effects.forEach((e) => {
    // ...unchanged branches...
    } else if (e.type === "vamp" || e.type === "consume") {
      if (e.type === "consume" && opts.allowStandaloneConsume) return;
      // ...unchanged companion check...
    }
  });
};

// ItemValidatorRawSchema: keep per-tag parsing on the array, move the cross-tag
// refinement to the object so it can see itemType/crystalTargetTypes.
effects: z.array(AllTags),

export const ItemValidator = ItemValidatorRawSchema
  .superRefine((data, ctx) =>
    SuperRefineEffects(data.effects, ctx, {
      allowStandaloneConsume:
        data.itemType === "CRYSTAL" && data.crystalTargetTypes === "WEAPON",
    }),
  )
  .superRefine(SuperRefineBase)
  .superRefine(SuperRefineItem)
  .superRefine(refineItemEconomy);
```

Notes for the implementer:

- `ItemValidatorRawSchema` is also used directly by the item editor page (`app/[shell]/manual/item/edit/[itemid]/page.tsx`) and content review (`libs/contentReview/entities.ts` uses `keysOf(ItemValidatorRawSchema)`). Moving the refinement must keep those surfaces validating, for example by having them use `ItemValidator`, or the editor would silently stop reporting companion errors. Issue paths should stay under `effects`.
- Do not use a generic "CRYSTAL may do anything" exemption. A Consume crystal targeting ARMOR or ACCESSORY would never see a damage tag at runtime.
- Optional, separately decided: an imbue-time guard that rejects a Consume-only crystal on a recipient with no Damage/Pierce. Today such a crystal is silently inert (§2).

## 5. Required regression coverage

The reproducer must flip, and everything else must stay rejected:

1. CRYSTAL + `crystalTargetTypes: "WEAPON"` + `[consume 20]` → accepted by `ItemValidator`.
2. Still rejected for `[consume]` alone: CRYSTAL with `crystalTargetTypes` ARMOR / ACCESSORY / null; WEAPON, ARMOR and CONSUMABLE items; jutsu (`JutsuValidator`); bloodline (`BloodlineValidator`); sage-mode and skill-tree arrays.
3. Still rejected: Vamp-only and Wound-only arrays everywhere, including WEAPON crystals.
4. Unchanged: upstream `tests/libs/combat/consume.test.ts`, vamp/wound tests and `clear_cleanse_regression.test.ts`.
5. Integration (port of harness B2): imbuable weapon + Crystal through `processUsersForBattle` → weapon action → 20% shield; shielded target uses the pre-shield basis; multiple targets aggregate; no-damage recipient gives no shield; `canBeImbued:false` recipient drops legacy imbuements at assembly.
6. Guards (port of harness B3): WEAPON-only, non-imbuable recipient, duplicate crystal, equipped recipient, CRAFTING-only occupation, rank/rarity table.
7. Whatever §3 decides, a test asserting the chosen Consume-on-Consume behaviour.

## 6. Out of scope

No Crystal rarity, tradability or crafting-accessibility choice (director). No change to the 3% Reliquary roll or the 12-Filament recipe. No manifest. The stale rank labels in the imbuing error string ("Apprentice" for EPIC, "Master" for LEGENDARY, against the real Master/Forgemaster thresholds) are an unrelated upstream wording defect. It is noted here only.
