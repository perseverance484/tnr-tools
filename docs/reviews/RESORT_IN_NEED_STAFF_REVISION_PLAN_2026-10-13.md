# Resort in Need — Staff-led finishing pass

**Status:** DRAFT FOR DIRECTOR APPROVAL; NOT AN IMPLEMENTATION OR RELEASE AUTHORIZATION.
**Date:** 2026-10-13
**Quest:** `xG0_Jq-amzhFgcLy8BVjw`
**Live baseline:** `harvests/inbox/tnr_results_1791902022789.json` (quest); `harvests/inbox/tnr_results_1791906435820.json` (quest + two full AI user records); `harvests/inbox/tnr_results_1791906972359.json` (AiProfile + two weapons + three jutsu).
**Pinned game source:** `studie-tech/TheNinjaRPG@922d61bbf4897014555463c4084f7ded40be2db7`
**Implementation owner:** Fable / Claude Code in normal TNR content lane. ChatGPT writes this design proposal and independently reviews its prepared patch. The director approves all balance/rewards, publication and game writes.
**Live requests/writes by ChatGPT:** 0 / 0.
**External communication:** The employee receives appreciation only; **no score, breakdown or fault list**, and is not asked to make the changes.

## Preservation requirements

Keep the employee's core story: coastal resort under jellyfish attack, unusual chakra signatures, harbor master/repair diversion, open-sea pursuit, giant chakra beast, sealing resolution, wildlife team report. Keep the existing four voluntary `fail_quest` choices and all battle-loss routes. Do not convert this into a new quest or rewrite major plot beats.

**Already director-ruled:** `maxAttempts: 100`, `maxCompletes: 1`; existing fail branches preserved. Neither is live yet (baseline holds attempts 1). `hidden: true` remains mandatory. Do not publish.

## 1. Quest technical adjustments (already discussed; location access still requires QA)

- `0SvwH` (third jellyfish encounter): `sector: 847`, `longitude: 22`, `latitude: 9` (paired with preceding move node `tTOUQ`). Keep `sectorType: "specific"`, `locationType: "specific"`.
- `nr_5q` (boss): `sector: 919`, `longitude: 21`, `latitude: 18` (paired with preceding move node `mbLvI`). Keep specific location types.
- `maxAttempts: 100`; preserve `maxCompletes: 1`, `retryDelay: "none"`, `attemptDelay: "none"` and every `failObjectiveId` / dialogue refusal edge.
- Verify both destination tiles are usable and the battles actually trigger at the intended points, especially because move + fight share a tile in sector 919. Do not guess map accessibility.
- Keep `consecutiveObjectives: true`, `hidden: true`, existing asset bindings, other gameplay mechanics and all unmentioned quest fields byte-identical to a **fresh** full capture at implementation time.
- Repair grammar/quotation/whitespace. No node count change is planned.

## 2. AI review findings and proposed treatment (director balance choices remain OPEN)

### A. Regular enemy, `1WAgDucRwcwGZ_yQ9r0uN` — "Jellyfish " (trailing space)

- Captured CHUNIN level 50; multipliers 1/1; six equipped jutsu: Static Jolt (100% stun/1r), Forceful Strike, Arc Bolt, Thunder Shockwave (90% stun/2r), Springguard, Weakening Strike. Quest uses 2 / 3 / 2 of this AI in simultaneous fights, with opponent scaling.
- **Preserve first:** keep the existing AI record and shared behavior profile `ePqWnmBprBeubGI3AZg7r` as the starting point. Its ordered rules already contain working damage selection and movement; do not replace it wholesale or toggle the profile.
- **Small optional amendment:** remove repeated copies of identical movement/attack rules only if test evidence shows they cause undesirable turn choices. Focus the first rule on attacking when a damaging jutsu is within valid range, otherwise approach. Retain `includeDefaultRules: true` unless source-tested behavior warrants changing it.
- **D-rank accessibility:** with two or three simultaneous jellyfish, both powerful stuns may produce repeated lockdown. First test the existing kit at lower levels; if necessary, **unequip only Thunder Shockwave** or soften the crowd-control exposure while keeping the rest of the employee's six-jutsu design. Do not edit globally shared jutsu records or quietly change enemy headcounts.
- Preserve current name unless the director explicitly accepts a fresh collision-checked rename. A trailing space is not worth a risky production identity write.

### B. Boss, `msKodzIJSH2J_BO-1FCIN` — "Jelly Chakra Beast"

**Director's revised proposal (2026-10-13; not yet final approval):** preserve the employee's signature **99% damage-reduction** boss tag, but make **any successful Seal tag** the intended counterplay. Lower the boss's base Defence and HP so ordinary follow-up attacks hurt badly while its innate defense is sealed. Preserve the existing AI profile and as much of the kit as possible; make narrow amendments rather than redesigning it as a generic boss.

#### Mechanic check against pinned game source

1. Captured boss has `decreasedamagetaken` **99% / 100 rounds** and an innate `weakness` effect with `dmgModifier: 50`, which currently recognizes two named Legendary swords and three named jutsu. Its equipped signature `Event Horizon Gate` is not a damage attack. It has `statsMultiplier: 9`, `poolsMultiplier: 9` and `maxHealth: 45,450` at stored level 100.
2. **Seal already works on this innate defense without listing item/jutsu IDs.** Pinned `app/src/server/api/routers/combat.ts` lines 3767–3783 realizes a user's `effects` (including the boss's innate tags) with `fromType: "bloodline"`. Pinned `app/src/libs/combat/tags.ts` lines 2589–2624 shows a successful `seal` suppresses active `fromType: "bloodline"` effects for its target. Pinned `app/src/libs/combat/process.ts` lines 2136–2154 skips sealed bloodline percentage DR. This is **source-backed and does not require new engine code**.
3. **Timing:** `getActiveSealEffects` in `process.ts` lines 1636–1637 requires the seal to be active and no longer `isNew`; the first blow landing the seal is not the dramatic follow-up. The increased damage arrives on subsequent attacks after the seal becomes active. A Seal attempt still obeys its own power/chance, duration, and immunity rules; **`elementalseal` is not the same tag**.
4. **Effective DR ceiling:** `app/drizzle/constants.ts` defines `DMG_REDUCTION_CAP = 0.9`, so 99% authored DR does **not** reduce all packets by 99%; normally at least 10% of the system-DR-adjusted base gets through. Removing the innate DR with a successful Seal can therefore produce a dramatic, roughly order-of-magnitude change in ordinary follow-up damage, rather than an unlimited 100× multiplier. Tune survivability and test both sealed and unsealed paths.
5. The current `weakness` tag is an **extra 50× damage multiplier for exact named attacks**, not a mechanic triggered by the `seal` effect itself (`tags.ts` lines 1468–1494). **Recommendation: remove that restricted whitelist effect from this boss** so any `seal` is a viable equal counter; retain the 99% DR effect unchanged. Do not edit those five global items/jutsu.
6. The quest is available from level 1; some entrants may lack access to any Seal. Since the mitigation cap allows damage even without sealing, it is possible to permit an unsealed but slower victory. Test that this path is realistically possible at supported levels. If the director wants Seal to be necessary rather than merely advantageous, the quest must visibly supply a usable Seal source for new characters; that would be a separate proposed gameplay addition, not something to assume exists.

#### Minimal AI/stat amendments, pending director values

- **Defense/HP:** lower the boss's `poolsMultiplier` from **9** to a **candidate 3**, subject to observed kill time. Reduce the Defence share in the six-stat weight distribution to make sealed follow-up damage meaningful; keep the offensive identity where practical. `app/src/server/api/routers/profile.ts` `scaleEditedAi` (lines 4287–4300) reweights AI stats when any combat weight changes; never assume writing an absolute `defence` number persists unchanged. Decide whether to lower `statsMultiplier` from 9 after reviewing effective caps and scaled difficulty; changing only the multiplier also changes offence. No numeric Defence weight or final multiplier has been approved.
- **Keep the boss's jutsu:** retain `Event Horizon Gate`. Equip one existing, affordable **damage** jutsu such as `Arc Bolt` so the already-written damage-selection rules have a valid attack. A second attack such as `Forceful Strike` is optional, not automatically required. Resolve live jutsu IDs from captured nested records; don't copy IDs from prose.
- **Keep the shared AI profile where possible:** both AIs currently reference `ePqWnmBprBeubGI3AZg7r`, owned by the regular Jellyfish. First test the boss with just an added damage jutsu and the existing rules. If the signature move is never selected, a **small `use_specific_jutsu` rule** for the boss's Event Horizon Gate could be added to the existing profile: the regular jellyfish does not have that move, so it should fall through to its current attack behavior, subject to an actual offline behavior test. Rule's target/range and order must be source-validated. Audit every AI sharing the profile before mutating it, and read back after any change. **Do not detach/recreate profiles as the default**; profile splitting is a fallback only if sharing prevents correct, independent behavior.
- **Presentation cue:** the final-beast reveal should hint that sealing breaks its protective chakra field and creates an opening, and the completion dialogue should describe the protected creature becoming vulnerable after the seal is applied. This preserves the original narrative.
- **Player-facing feel:** normal attacks chip away through its defenses; any **successful Seal** disrupts its innate protective tag; attacks during the active seal window inflict substantially greater damage. Keep this transparent in dialogue and avoid requiring the five legacy named counters.

#### Checks before approval

- Source/static verification is not a combat playtest. Test the D-rank fight across entrant levels and **with/without Seal**, including low-power/short-duration Seal and unsuccessful Seal attempts.
- Verify the 99% tag is suppressed during the relevant active seal window in actual combat, then returns when the seal expires. The original DR buff has 100-round duration and need not be recast.
- Test the regular and boss AI behaviors **after** any shared-profile changes. Preserve the two AI identities and the original profile unless a broken interaction is demonstrated.
- No live writes, boss stats, reward or profile changes are authorized by this proposal.

## 3. Copy edits (player-facing text; keep graph untouched)

A concise staff-written copy pass can use the following replacements as working candidates. Confirm they're faithful to the employee's intended story before applying, keep choices and fail edges.

| Field / node | Proposed replacement |
| --- | --- |
| Quest description | Resort guests report repeated jellyfish attacks along the shoreline. Wildlife teams have noticed unusual chakra signatures in the creatures' attacks and request shinobi assistance. |
| `89nzR` | The wildlife team reports that the jellyfish are using attacks resembling jutsu. Unable to contain them safely, the team asks you to investigate the source. |
| `l5Miv` | After the fight, you sense that something is watching from offshore. A massive, nearly translucent shape slips beneath the waves. You spot a marina down the peninsula and head there to find a boat. |
| `1N_w9` | "You're asking me to chase a sea monster? Not many boats are fast enough for that, and fewer captains would take the risk." |
| `8YT8K` | "The best shipwrights I know are in Akasumi. They should have the tools I need to repair the boat." |
| `zZkf5` description | Find the shipwrights' tools in Akasumi. *(Keep `move_to_location` rather than inventing a collection inventory mechanic.)* |
| `mnCZD` | As you approach the creature's last known location, the chakra trail grows stronger. The harbor master follows your directions until more jellyfish rise from the sea to attack the boat. |
| `TLuVn` | The giant jellyfish rises from the depths, protected by a dense layer of chakra. Sealing techniques may disrupt its protection and leave it vulnerable. It dives deeper into its domain, and you prepare to follow. |
| `MMv29` | With the beast's protective chakra disrupted, you defeat it and complete the seal. As its power fades, the smaller jellyfish calm and retreat into deeper waters. |
| `td-XJ` description | Return to the wildlife team. |
| Quest-level `successDescription` | You report the outcome to the wildlife team, who thank you for containing the chakra beast. With the swarm retreating into deeper waters, the beaches are safe again. |

- Existing `l5Miv` choice: "Boat’s make me seasick." → "Boats make me seasick." Keep its `jF6G_` route.
- Existing `8YT8K` choice: "Sound's like work I don't wanna do." → "Sounds like work I don't want to do." Keep its `jF6G_` route.
- Existing `TLuVn` choice: "Dawn special underwater breathing gear to seal the beast away." → "Don the underwater breathing gear and pursue the beast." Keep the win path.
- Normalize punctuation and remove leading/trailing whitespace in all dialogue choices; correct quote balancing, apostrophes, run-on sentences and `jutsu’s` → `jutsu`.
- Fill empty *objective descriptions* with clear, short tasks where displayed. Preserve scene assets and endings unless the director approves otherwise.
- No em dashes in player-facing dialogue. No new map artwork or character sprites are prerequisites for this pass.

## 4. Completion reward (director must approve before build)

Captured quest and all objectives currently award **zero** exp, money, tokens, prestige, clan points, items and jutsu. There are no AI item drops in the two captured inventories.

Recommended **one-time, no-chase-item reward** rather than elaborate new reward assets. Existing canonical D-rank mission baseline (`skills/building-tnr-content/data/48_DATA_mission_profiles.json`): **173 EXP, 1,100 ryo, 100 tokens, 14 prestige, 100 clan points**. Because this event includes substantial travel and four fights and event rewards are not mission-boosted, a *candidate* is **2× the EXP/ryo/prestige baseline** with unchanged tokens/clan points: **346 EXP, 2,200 ryo, 100 tokens, 28 prestige, 100 clan points** at quest completion only. **Not approved** and not a binding doctrine for other events. No new item, recipe, drop-rate or raid economy.

Alternate director choices: exact D mission baseline; rewardless introductory story explicitly labeled as such. Do not quietly pick one.

## 5. Gates for implementing and accepting

1. Director accepts/edits the **any-Seal counterplay**, boss `poolsMultiplier`/Defence-weight proposals, offensive attack kit, shared-profile minimal rule adjustments, regular crowd control and exact reward values. Do not infer approval merely because a possibility was discussed.
2. Before preparing any quest/AI write manifest, **recapture fresh full quest + both AI records + the linked profile**. Check other AI consumers of that profile and concurrent staff edits. Abort on unexplained drift.
3. Fable prepares a minimal full-record quest update preserving all unmentioned fields, a carefully staged boss AI stat/effect/jutsu edit, and a shared-profile edit **only if shown necessary**. Preserve existing profile links, names, quest fail routes and `maxAttempts: 100 / maxCompletes: 1` intent. No new profile by default. Never edit player-owned/global jutsu or items.
4. Canonical `validate.py`, contract checks, quest graph checks and focused AI rule tests must pass. Known contract-validation drift remains a separate concern, not grounds for silent bypass.
5. Diff each record for the director; operator alone initiates live writes. Everything stays hidden until explicit publication approval.
6. After approved operator-run changes, capture live read-back and playtest **both ordinary and sealed boss behavior** (including the active seal timing window, damage protection returning on expiry, and low-level players without Seal).
7. Staff sends employee an encouraging proposal/summary of refinements, without score or blame; staff owns the implementation work.

**Deliverable here:** Proposal only. No boss stats, rewards, weakness rewrite, quest updates or profile changes are live or finally approved. The author retains credit for the original story and encounter concept.
