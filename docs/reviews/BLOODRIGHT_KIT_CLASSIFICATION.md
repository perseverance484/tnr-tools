# Bloodright bonuses vs kit element classification (2026-10-18)

**Finding (engine-verified):** under the current engine, a Bloodright potency bonus reaches a kit
jutsu's effect row only when that row lists the tree's element, or when the jutsu's
`elementClassification` equals it (`resolvePotencyTags`, `app/src/libs/combat/potency.ts`,
TheNinjaRPG `94f9d84`). Every captured kit jutsu has `elementClassification: "None"`. Most buff and
debuff rows carry no elements, while damage rows usually do.

| Measure (25 naming-pass trees, 130 tree × bonus-tag pairs) | Today | After setting kit `elementClassification` to the bloodline element |
|---|---:|---:|
| Bonus tags that reach no kit row | 71 | 2 (Shiroi Youso's `None` placeholder) |
| Node bonuses affected | 201 of 300 skills' bonuses | 4 |

Example: Taiyo Kami (the accepted exemplar) only has working Damage bonuses today. Its Afterburn,
DDT, DDG and IDT bonuses reach nothing.

**Reproduce (offline; runs the game's own function, no live requests):**

```sh
# GAME = a checkout of studie-tech/TheNinjaRPG at 94f9d84
cp scripts/bloodright_engine/potency_entry.ts $GAME/app/zz_potency_entry.ts
node scripts/bloodright_engine/build_engine.mjs $GAME $GAME/app/zz_potency_entry.ts /tmp/engine.mjs
node scripts/bloodright_engine/probe_coverage.mjs /tmp/engine.mjs
```

The kit data is `docs/design/bloodright/balance/kits_from_reference_captures.json`. It is extracted from
the reference-library capture results (`push/101`, `push/104`–`108`, `harvests/inbox/tnr_results_179221*.json`).

## Side effects of setting `elementClassification` (source-read)

- **Access:** `checkJutsuElements` (`libs/train.ts`) treats a classification as an extra requirement.
  Each of the 25 bloodlines' own effects already grant its tree element (captured `bloodline.get`), so
  owners keep access.
- **Elemental Seal** (`libs/combat/actions.ts`) affects 60-AP jutsu that are classified or carry
  elements. One kit jutsu becomes newly sealable: Shinseina Ki "Wood Style: Wood Warrior Summon".
- **Search:** element filters (`routers/jutsu.ts`) start listing the classified jutsu.

## The `None` placeholder (correction to RUL-2026-10-17-004)

`affectedElements: ["None"]` matches every effect row without elements, on any jutsu the player casts,
including jutsu outside the kit. It is broad, not neutral.

## AI equips

122 kit jutsu need the edit. Per the 2026-10-12 full AI census, 38 of them are equipped on 46 AIs.
Editing an equipped jutsu severs the AI's link (laws 18 and 60), so the AIs need
unequip → edit → re-equip. The gates, recovery and `updateAi` re-scaling hazards follow
`docs/reviews/AI_JUTSU_82_REEQUIP_EVIDENCE.md` (branch `claude/ai-jutsu-reequip-validation-7ywxag`).
Stage 1 (read-only) is `push/109`–`110`.
