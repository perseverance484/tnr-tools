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

- Live CHUNIN level 50; pools 2,550, stat/pool multipliers 1/1; equipped jutsu: **Static Jolt** (100% stun for 1 round), **Forceful Strike**, **Arc Bolt**, **Thunder Shockwave** (90% stun for 2 rounds), **Springguard**, **Weakening Strike**. Quest uses 2, then 3, then 2 of this same AI in simultaneous groups; all `opponent_scaled_to_user: true`.
- Its actual profile `ePqWnmBprBeubGI3AZg7r` contains repeated movement and `use_highest_power_jutsu`-damage instructions plus fallback rules, `includeDefaultRules: true`. This can be simplified without designing new jutsu.
- **Proposed:** keep recognizable lightning/storm jellyfish identity, and reduce repetitive crowd-control pressure for low-level players. Prefer replacing the **AI's equipped set** with a simple damaging/defensive subset and at most one crowd-control source *only if the director wants one*. Do NOT edit shared jutsu records; other content could use them. A conservative starter subset is `Arc Bolt`, `Forceful Strike`, `Springguard`, `Weakening Strike`; remove both high-probability stuns from this AI's loadout (not from the global jutsu registry).
- **Proposed:** deduplicate and simplify the regular AI rules; prioritize damage in usable range, movement beyond range, and an affordable fallback. Confirm AI-turn behavior and the effects of `includeDefaultRules` against the pinned engine.
- **User decision:** whether to retain the existing 2/3/2 simultaneous headcounts or reduce them for a D-rank / level-1 entry. If headcounts remain, removing stuns from the loadout becomes more important. Do not silently decide.
- Preserve AI username unless a fresh *global* name collision check proves a unique replacement; its trailing space is polish, not worth a hazardous rename.

### B. Boss, `msKodzIJSH2J_BO-1FCIN` — "Jelly Chakra Beast"

- Live JONIN level 100, multipliers **9/9**, HP/CP/SP **45,450**, only equipped jutsu **Event Horizon Gate**. The jutsu is an AOE control/defensive move, not direct damage.
- Boss has **99% decreased damage taken for 100 rounds** plus `weakness` with `dmgModifier: 50`, restricted to two existing **Legendary** sealing swords (Whispering Dawnblade, Masamune) and three jutsu (Danse Macabre, Celestial Sealing, Silent Palm Strike). The latter two are bloodline-specific; Danse Macabre is level-70. The quest itself does not provide those options to the D-rank, level-1 entrant.
- Source `app/src/libs/combat/tags.ts` `calcDmgModifier` matches specific `actionId` against weakness item/jutsu lists and multiplies raw damage by 50. This is **not** a guaranteed defeat; the boss's 99% damage reduction is a separate effect. Do not describe this as a one-hit kill.
- Boss and regular both link `aiProfileId: ePqWnmBprBeubGI3AZg7r`. The profile's `userId` is the **regular** AI. Its rules select actions with effect `damage`; Event Horizon Gate lacks such an effect. The boss consequently lacks a rule that explicitly selects its signature ability. Default backup rules also prioritize damage/movement and do not automatically solve the mismatch. The boss may resort to basic actions; do not claim proven combat behavior without execution evidence.
- **Recommended design:** keep the beast visually and narratively formidable, but make this a normal *scaling combat boss* that the player defeats to weaken, followed by the existing story's sealing aftermath. Do not require rare global swords or specific bloodlines.
- **Proposed AI changes, pending director approval:** replace the near-total 100-round DR and external-item weakness with a modest, short defensive rider if desired; lower the extreme multipliers to an appropriate D-rank scaled baseline (do not adopt numeric values without approval); equip 1–2 existing direct-damage moves that fit the storm-jellyfish theme while keeping Event Horizon Gate as an optional boss signature; give boss **its own**, deliberately ordered rules that can cast that signature move, attack and move sensibly.
- **Critical implementation safety:** the boss currently points at a profile owned by the regular AI. Editing profile `ePqWnmBprBeubGI3AZg7r` to change boss behavior would also affect regular jellyfish. `app/src/server/api/routers/ai.ts` lines 118–157 show that `toggleAiProfile` on a nonnull link *detaches*, and a subsequent toggle when null *creates/relinks* a boss-owned profile when none exists. This would be two operator-owned production writes and must be safely staged, read back between steps, and planned explicitly by Fable rather than performed casually. Do not mutate the shared profile until all dependents are understood.
- **Playtest requirement:** validate representative level-1, level-20, and high-level capped entrant fights, with 2/3 simultaneous regular enemies and boss. Quest's `opponent_scaled_to_user` scales AI level to player then applies AI stats; this does not remove the 9× multiplier or 99% DR hazard.

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
| `TLuVn` | The shadow finally comes into view: a giant jellyfish, overflowing with chakra. You need to weaken it before its power can be sealed. It dives deeper into its domain, and you prepare to follow. |
| `MMv29` | With the creature weakened, you complete the sealing technique. Its chakra fades, and the smaller jellyfish gradually calm and retreat to deeper waters. |
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

1. Director accepts/edits the encounter headcounts, regular stun policy, boss kit/effects/multipliers, and exact reward.
2. Before preparing any quest/AI manifest, **recapture latest full quest + two full AI records + linked AiProfile**, and check possible external AI consumers/quest relations. Account for concurrent unrelated staff edits; abort on drift.
3. Fable authors a **minimal full-record quest edit** preserving every untouched field, a regular AI profile cleanup only if approved, and a **safe, separate** boss-profile reassociation and boss kit/effect edit. Never change player-owned/other content jutsu globally.
4. Run canonical `validate.py`, exact source-backed contract tests and focused quest graph/AI-rule checks; stop on any unapproved contract exception. Source parity currently has known QW-0A drift; do not use generic validation failures as permission to invent a bypass.
5. Present a diff-by-record and review checklist to the director for game push; no agent touches live game. Run all creates/edits hidden; preserve `maxCompletes: 1`.
6. Operator executes approved actions, captures read-back, and playtests the real event while hidden. Publication is a separate explicit user-controlled step.
7. The employee gets a concise appreciative note. No rating or corrections assigned to them.

**Deliverable here:** Proposal only. Neither the proposed numbers nor the boss change is live or approved. This file exists so staff can do the finishing work without bouncing it back to the first-time employee.
