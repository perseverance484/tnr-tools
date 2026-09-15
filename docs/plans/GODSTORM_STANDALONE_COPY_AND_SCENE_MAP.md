# Godstorm: standalone quest copy and scene map

Draft 1 | 2026-09-15 | New copy and image bindings await director acceptance

Structural direction is approved. This is the proposed player-facing copy and scene map, not an executable manifest or a claim that production has changed. Fable remains the implementation owner; dauntless alone operates the game.

## 1. Authority, evidence and proposal boundary

Repository: `perseverance484/tnr-tools`. Governing plan and RUL-2026-09-15-002 at `0c21706a74c80dfa39d33564b101dd42b1bf808e`, branch `chatgpt/godstorm-two-pyramid-plan`. Capture baseline: `6e09b15bb6f3d1c90ba416d14211b533f5b4a367`.

- E1: `harvests/inbox/tnr_results_1789401726302.json`, `captures[1].data` (Marrow), `captures[2].data` (Stormcourt): objective IDs, opponent bindings, original prose and background references. September 14, 16:02 UTC.
- E2: `harvests/inbox/tnr_results_1789402842027.json`: AI identities, primary avatar assignments, embedded kits and background records. September 14, 16:20 UTC.
- E3: `harvests/inbox/tnr_results_1789403623148.json`: associated AI profiles. September 14, 16:33 UTC. No balance recertification is made by this document.
- Art requirements remain with `skills/producing-tnr-art/SKILL.md`, its current specification and `docs/workflows/ART_PRODUCTION.md`. This document does not invent export dimensions or processing rules.

Captured quest prose is the story baseline. An unavailable event sheet is not treated as read. The elder sister's confinement, failed light, stopped clock, moths, binding chains, divided threshold, tribunal, Widow, Candlewright, Herald and siphoned-storm Echo come from that baseline. New descriptive connective details and the revised endings are proposed copy, not automatically canonical lore.

Two substantive narrative additions require acceptance: Marrow's records explicitly identify Stormcourt; defeating Sovereign Echo ends the local storm binding. This draft does not claim that either sister is physically present, rescued, alive or dead; it does not kill a god or settle every Unbroken Thread plot elsewhere.

Regular guardians remain anonymous combatants. No new narrator, sister portrait, illustrated collectible, travel objective or supporting cast is introduced. Stage names below are editorial group labels, not new quest nodes or registered asset names.

## 2. Exact structural delta

| Measure | Captured pair | Draft pair |
|---|---:|---:|
| Battles | 50 | 50 |
| Dialogs | 68 | 52 |
| Terminal nodes | 4 | 4 |
| Total objectives | 122 | 106 |
| Successful routes | Ten alternative payout routes | Two full-clear endings |

Each draft quest retains 25 battles, 25 pre-battle dialogs, one visible victory dialog and two terminal nodes: 53 objectives. Every battle remains directly dialog-gated. Stormcourt's player-facing battle labels restart at 1/25; internal d6 through d10 IDs stay unchanged.

Remove these 16 dialogs from the revised graph, not the evidence archive:
- Marrow: `d1_choice`, `d1_cash`, `d2_choice`, `d2_cash`, `d3_choice`, `d3_cash`, `d4_choice`, `d4_cash`.
- Stormcourt: `d6_choice`, `d6_cash`, `d7_choice`, `d7_cash`, `d8_choice`, `d8_cash`, `d9_choice`, `d9_cash`.

| Intermediate keeper | Old success link | New success link |
|---|---|---|
| b1_boss | d1_choice | d2_1 |
| b2_boss | d2_choice | d3_1 |
| b3_boss | d3_choice | d4_1 |
| b4_boss | d4_choice | d5_1 |
| b6_boss | d6_choice | d7_1 |
| b7_boss | d7_choice | d8_1 |
| b8_boss | d8_choice | d9_1 |
| b9_boss | d9_choice | d10_1 |

Retain `b5_boss -> d5_victory -> win` and `b10_boss -> d10_victory -> win`. All 50 failure links remain `fall`. Other battle-success links and all opponent configurations stay as captured. Do not change quest type, combat pools, abandonment controls or checkpoint/retry mechanics to implement this copy.

## 3. Asset keys and proposed assignments

These are planning keys, not runtime aliases or fabricated IDs. All proposed matches require actual pixel review. A complete assignment map is not completed visual production.

| Key | Existing/candidate ID | Intended asset and status |
|---|---|---|
| M1 | `7EmVo6GH5GL4YtQTDrbDR` | marrow vault 1; captured, scene fit pending |
| M2 | `oc0cXiMrcG_6kTUwNWRkn` | marrow vault 2; captured, scene fit pending |
| M3 | `IykL5XxwFF14BosCblZj8` | marrow vault 3; captured, final-payoff fit pending |
| S1 | `cKHhHoboreP88iH5WjDe7` | StormCourtyard; shared SkychainMonastery candidate, not dedicated Godstorm art |
| B0 | `Q-_3WA5kibe_8gI2CgTKl` | Blank Character; older catalog candidate, current record and pixels unverified |
| K1 | Not assigned | Warden of the First Dark scene portrait |
| K2 | Not assigned | Keeper of Hushed Hours scene portrait |
| K3 | Not assigned | The Moth Tyrant scene portrait |
| K4 | Not assigned | Chained Chorister scene portrait |
| K5 | Not assigned | Warden of the Half Eclipse scene portrait |
| K6 | Not assigned | The Gloaming Judge scene portrait |
| K7 | Not assigned | Widow of the Waning Moon scene portrait |
| K8 | Not assigned | The Candlewright scene portrait |
| K9 | Not assigned | Herald of the Last Dusk scene portrait |
| K10 | Not assigned | Sovereign Echo of the Godstorm scene portrait |

Find matching existing scene records first; otherwise adapt accepted source images where viable. Nine keeper primary avatars are available as source candidates. First Dark's missing avatar and portrait should share one accepted master. An opaque avatar image is not automatically a valid scene overlay.

Allocation: M1 15 scenes; M2 10; M3 one; S1 26 candidate uses. B0 42 placements; K1-K10 one each. Configure deliberate quest-level background and blank fallbacks only after the selected records and applicable publish guard are verified.

Five captured background bindings survive and are preserved: M1 at d1_1, d1_2, d1_boss; M2 at d1_3, d1_4. Removing d1_choice and d1_cash removes two previously wired scenes. Therefore 47 background bindings remain to add, not 46. M3 is retained artwork even though its old cash-out placement is removed.

Pixel review must check the stopped-clock, moth, chain and divided-threshold settings against M1/M2, and the cleared-prison payoff against M3. S1 must be evaluated against the tribunal, frost, candles and central-dais scenes. Textual detail need not be painted literally, but a visible contradiction fails the match. Inspect other existing compatible plates before adding any commission. No new background painting is committed by this draft.

B0's alternative catalog candidate is `1YXbXYW2wz3GETVMb6DT6`; verify one appropriate blank rather than creating another by default. All ten keeper scene IDs remain unresolved. Do not ship placeholder keys, null IDs or an unapproved blanket replacement for missing portraits.

## 4. Scene-map conventions

The scene tables contain every retained dialog body and its proposed artwork. For each regular pre-battle row `dN_1` through `dN_4`, the single choice is **Advance**, pointing to `bN_1` through `bN_4`. For each `dN_boss`, the single choice is **Confront the keeper**, pointing to `bN_boss`. Final dialog choices are stated separately. These choices introduce no travel or optional exit before completion.

Use the complete scene text in each row as that dialog's `description`. Keep `successDescription` empty for all 52 dialogs. Preserve current objective map-image fields pending their separate validity check; a map image is not a scene background.

The listed encounter name is the full AI identity, even where an older battle description shortened an Ascendant name. Preserve the actual opponentAIs binding from E1 rather than resolving an AI by its name.

## 5. Marrow Vaults

Quest ID: `2yvE9PUQqlD8lbYNfgX-b`.

**name:** Marrow Vaults

**description:** The Unbroken Thread kept the elder sister in these vaults and studied the blood that devoured light. Its guardians still hold the prison. Defeat all twenty-five enemies, including the five keepers, to clear Marrow Vaults and open the route to Stormcourt.

**successDescription:** Marrow Vaults is cleared. Its keepers are defeated, and the route to Stormcourt is open.

### Stage 1: The prison entrance

| Dialog | Battle / enemy | Background | Character | Proposed description |
|---|---|---|---|---|
| d1_1 | 1 / Umbral Reaver | M1 | B0 | Tally-marks cover the entrance to Marrow Vaults: feedings, measurements, years. The Unbroken Thread recorded the elder sister's captivity in a careful administrative hand. An Umbral Reaver still guards the first passage. Whatever became of the jailers, their watch has not ended. |
| d1_2 | 2 / Hollow Lantern | M1 | B0 | Beyond the first guard, a Hollow Lantern waits beside another row of tally-marks. A narrow strip of stone has been rubbed smooth where someone repeatedly counted the days by touch. |
| d1_3 | 3 / Starless Monk | M2 | B0 | The next chamber has no window. A Starless Monk stands before the inner doorway, holding the same watch recorded on the walls outside. |
| d1_4 | 4 / Nightveil Sentinel | M2 | B0 | A Nightveil Sentinel blocks the approach to the keeper's hall. Behind it, the prison records give way to bare stone. No visitor was meant to pass this point. |
| d1_boss | 5 / Warden of the First Dark | M1 | K1 | An armored figure rises from a plain chair at the end of the hall. It was the first guard the Thread set over the elder sister's prison. The Warden of the First Dark takes its place across the passage. |

### Stage 2: The silenced chambers

| Dialog | Battle / enemy | Background | Character | Proposed description |
|---|---|---|---|---|
| d2_1 | 6 / Hollow Lantern | M1 | B0 | Past the fallen Warden, sound begins to fail. Your footsteps disappear a pace behind you. The records call the elder sister stable, compliant, watched. A Hollow Lantern guards the chambers where her silence was kept. |
| d2_2 | 7 / Starless Monk | M1 | B0 | A Starless Monk waits where the passage bends. Its sleeves move as it turns, but you hear no cloth against stone. The silence reaches into every corner of this chamber. |
| d2_3 | 8 / Nightveil Sentinel | M2 | B0 | The same assessment appears on successive records, copied without alteration. A Nightveil Sentinel stands beneath them. Nothing here acknowledges how many years passed between the entries. |
| d2_4 | 9 / Umbral Reaver | M2 | B0 | An Umbral Reaver guards the last approach. Beyond it, a stopped clock marks an hour the records never explain. The silence is deepest near the keeper. |
| d2_boss | 10 / Keeper of Hushed Hours | M1 | K2 | A veiled figure stands beneath the stopped clock, keeping a silence nineteen winters old. The Keeper of Hushed Hours turns toward you. There is no sound as its robes move. |

### Stage 3: The devoured light

| Dialog | Battle / enemy | Background | Character | Proposed description |
|---|---|---|---|---|
| d3_1 | 11 / Starless Monk | M1 | B0 | Beyond the Keeper's chamber, pale mothlight gathers overhead. The insects cling where the elder sister's chakra consumed the light, searching the stone for what is gone. A Starless Monk waits beneath them. |
| d3_2 | 12 / Nightveil Sentinel | M1 | B0 | A Nightveil Sentinel interrupts your path through the pale glow. Moths scatter from its shoulders and settle again on the wall behind it. |
| d3_3 | 13 / Umbral Reaver | M2 | B0 | The light weakens as you approach an Umbral Reaver. The moths avoid the space around it, leaving a dark break in the drifting swarm. |
| d3_4 | 14 / Hollow Lantern | M2 | B0 | A Hollow Lantern keeps the final approach. Above it, the separate points of mothlight begin to gather. Something heavier moves among the wings. |
| d3_boss | 15 / The Moth Tyrant | M1 | K3 | The mothlight closes around a crowned shape. Its wings resemble burnt pages, and its body is swollen with the light it has consumed. The Moth Tyrant descends to meet you. |

### Stage 4: The binding chambers

| Dialog | Battle / enemy | Background | Character | Proposed description |
|---|---|---|---|---|
| d4_1 | 16 / Nightveil Sentinel | M1 | B0 | The moths fall back from the next chamber. Ritual chains hang in ordered rows over slabs stained by needles. A low voice recites the binding verses. A Nightveil Sentinel guards the first row. |
| d4_2 | 17 / Umbral Reaver | M1 | B0 | An Umbral Reaver stands among the hanging chains. Their lowest links drag across the slabs, worn smooth by years of use. |
| d4_3 | 18 / Hollow Lantern | M2 | B0 | A Hollow Lantern waits beside the bindings. Each pause in the distant verse is answered by a small movement through the chains. The rite is still being kept. |
| d4_4 | 19 / Starless Monk | M2 | B0 | A Starless Monk blocks the last gap between the chains. The singing continues beyond it, measured and unchanged by the fighting in the outer rooms. |
| d4_boss | 20 / Chained Chorister | M1 | K4 | The singing stops. The chains lift and settle around a hooded figure, each one drawn into position. The Chained Chorister steps forward to defend the binding chamber. |

### Stage 5: The divided threshold

| Dialog | Battle / enemy | Background | Character | Proposed description |
|---|---|---|---|---|
| d5_1 | 21 / Umbral Reaver | M1 | B0 | Past the broken bindings, the final threshold is divided. Cold silver covers one half; the other returns no light. The elder sister's chakra has soaked through the stone. An Umbral Reaver guards the crossing. |
| d5_2 | 22 / Hollow Lantern | M1 | B0 | A Hollow Lantern waits near the silver edge. Its outline sharpens there, then disappears where the darkness touches its robes. |
| d5_3 | 23 / Starless Monk | M2 | B0 | A Starless Monk holds the narrow approach. Behind it, the two halves of the threshold meet without blending. Nothing moves beyond that seam. |
| d5_4 | 24 / Nightveil Sentinel | M2 | B0 | A Nightveil Sentinel is the last guard before the threshold. The marks of confinement end here. Whatever the Thread kept beyond them needed its own keeper. |
| d5_boss | 25 / Warden of the Half Eclipse | M1 | K5 | The Warden of the Half Eclipse stands where silver meets dark, wearing both halves like a mantle. It has been partly consumed by what it guarded. The Warden draws its blade and closes the final passage. |

### Full-clear ending: d5_victory

Background M3; character B0. One choice: **Leave the vaults** -> `win`.

The Warden of the Half Eclipse falls. Beyond the threshold, no guard remains to seal the prison again. The records left in these chambers name a second site of the Thread's work: Stormcourt, where the younger sister's storm was held. The vaults are cleared. You leave to end the work recorded there.

**win.description:** You leave the cleared vaults behind and turn toward Stormcourt.

**win.successDescription:** Marrow Vaults is cleared.

**fall.description:** This attempt ends before Marrow Vaults is cleared.

Keep `fall.successDescription` empty. The visible victory dialog carries the narrative ending; the terminal node is not its substitute. The leave button closes this quest and does not promise an automatic start of Stormcourt.

## 6. Stormcourt

Quest ID: `OSADdXqostbyVliCxWk6k`. Preserve its existing Marrow prerequisite.

**name:** Stormcourt

**description:** The Unbroken Thread bound the younger sister's storm within this court. Its guardians still defend the instruments that held it. Defeat all twenty-five enemies, including the five keepers, and bring down the Sovereign Echo of the Godstorm to end the binding.

**successDescription:** Stormcourt is cleared. The Sovereign Echo is defeated, and the binding is broken.

### Stage 1: The tribunal

| Dialog | Battle / enemy | Background | Character | Proposed description |
|---|---|---|---|---|
| d6_1 | 1 / Hollow Lantern Ascendant | S1 | B0 | At Stormcourt, pressure bears down before the first thunderclap. Scorched marks spread across the stone at the height of a young girl. This is where the Thread held the younger sister's storm. A Hollow Lantern Ascendant guards the approach to the tribunal. |
| d6_2 | 2 / Starless Monk Ascendant | S1 | B0 | A Starless Monk Ascendant waits along the tribunal approach. A voice almost forms inside the thunder, then breaks apart before you can distinguish a word. |
| d6_3 | 3 / Nightveil Sentinel Ascendant | S1 | B0 | A Nightveil Sentinel Ascendant holds the next crossing. Its outline remains steady in a gust that drives rain sideways across the court. |
| d6_4 | 4 / Umbral Reaver Ascendant | S1 | B0 | An Umbral Reaver Ascendant blocks the way to the Judge. The fighting has not disturbed the figure waiting beyond it. The gavel remains raised. |
| d6_boss | 5 / The Gloaming Judge | S1 | K6 | A robed figure waits with a dark gavel. This tribunal heard a girl say that the thunder spoke, then ruled her mad. The Gloaming Judge turns from its empty hearing to confront you. |

### Stage 2: The mourning court

| Dialog | Battle / enemy | Background | Character | Proposed description |
|---|---|---|---|---|
| d7_1 | 6 / Starless Monk Ascendant | S1 | B0 | Beyond the tribunal, frost traces the sheltered edges of the court. A waning crescent shows through the cloud. A Starless Monk Ascendant stands between you and the veiled figure waiting beneath it. |
| d7_2 | 7 / Nightveil Sentinel Ascendant | S1 | B0 | A Nightveil Sentinel Ascendant guards the cold stone. Meltwater runs a short distance from its feet before freezing again in the joints. |
| d7_3 | 8 / Umbral Reaver Ascendant | S1 | B0 | An Umbral Reaver Ascendant advances across the frost. Behind it, the veiled figure remains still. Only the pale edges of her blades move in the wind. |
| d7_4 | 9 / Hollow Lantern Ascendant | S1 | B0 | A Hollow Lantern Ascendant keeps the Widow's approach. The air grows colder as you near it, and the next peal of thunder arrives thin and distant. |
| d7_boss | 10 / Widow of the Waning Moon | S1 | K7 | The frost parts around the Widow of the Waning Moon. She has kept her mourning for what the Thread took long before your arrival. She lifts two blades of fading moonlight and faces you. |

### Stage 3: The extinguished flames

| Dialog | Battle / enemy | Background | Character | Proposed description |
|---|---|---|---|---|
| d8_1 | 11 / Nightveil Sentinel Ascendant | S1 | B0 | Beyond the Widow, old wax fills the joints between the stones. Rows of spent candles lean against one another, their wicks drowned by rain. A Nightveil Sentinel Ascendant guards the surviving work. |
| d8_2 | 12 / Umbral Reaver Ascendant | S1 | B0 | An Umbral Reaver Ascendant waits among the dead candles. Small sheltered flames persist farther ahead, relit as quickly as the weather extinguishes them. |
| d8_3 | 13 / Hollow Lantern Ascendant | S1 | B0 | A Hollow Lantern Ascendant guards a line of candle stubs. Wax has hardened around their bases in layers, each failed lighting buried beneath the next. |
| d8_4 | 14 / Starless Monk Ascendant | S1 | B0 | A Starless Monk Ascendant keeps the last approach to the light-keeper. Beyond it, wax is being worked around a fresh wick. The hands do not stop when you arrive. |
| d8_boss | 15 / The Candlewright | S1 | K8 | The Candlewright turns from its work, crusted in old wax and crowned with small flames. The Thread charged it with holding back the girl's weather. It is still tending the candles after every flame around it has failed. |

### Stage 4: The last warning

| Dialog | Battle / enemy | Background | Character | Proposed description |
|---|---|---|---|---|
| d9_1 | 16 / Umbral Reaver Ascendant | S1 | B0 | Past the Candlewright, the wind circles the court instead of crossing it. Every gust returns toward the central dais. An Umbral Reaver Ascendant guards the first break in that circling current. |
| d9_2 | 17 / Hollow Lantern Ascendant | S1 | B0 | A Hollow Lantern Ascendant holds the next passage. Behind it, something strikes a low note that you feel through the wet stone before you hear it. |
| d9_3 | 18 / Starless Monk Ascendant | S1 | B0 | A Starless Monk Ascendant waits where the gusts meet. The pressure pulls at your clothes from opposing directions. The sound ahead resolves into a horn. |
| d9_4 | 19 / Nightveil Sentinel Ascendant | S1 | B0 | A Nightveil Sentinel Ascendant stands before the Herald. Beyond it, a storm-wreathed figure lifts a war horn toward the central dais. |
| d9_boss | 20 / Herald of the Last Dusk | S1 | K9 | The Herald of the Last Dusk sets the horn to its lips. Its call draws an answer from the storm binding at the center of the court. The Herald steps into your path as the note fades. |

### Stage 5: The storm binding

| Dialog | Battle / enemy | Background | Character | Proposed description |
|---|---|---|---|---|
| d10_1 | 21 / Hollow Lantern Ascendant | S1 | B0 | The Herald's horn is silent. Ahead, an eye of still air surrounds the central dais while rain races around its edge. A Hollow Lantern Ascendant guards the instruments that hold the storm in place. |
| d10_2 | 22 / Starless Monk Ascendant | S1 | B0 | A Starless Monk Ascendant waits beside the binding instruments. Violet light passes between them, and the pressure rises each time the current reaches the dais. |
| d10_3 | 23 / Nightveil Sentinel Ascendant | S1 | B0 | A Nightveil Sentinel Ascendant guards the still air. Beyond it, empty armor stands upright. Lightning moves beneath the plates where a body should be. |
| d10_4 | 24 / Umbral Reaver Ascendant | S1 | B0 | An Umbral Reaver Ascendant closes the last approach. The voice inside the thunder comes from the armor behind it. Nothing remains between you and the source except this final guard. |
| d10_boss | 25 / Sovereign Echo of the Godstorm | S1 | K10 | The Sovereign Echo of the Godstorm moves from the dais: empty armor held upright by pressure and violet lightning. It wears the younger sister's siphoned storm like a body. The cry in its helm swells as it takes the field. |

### Full-clear ending: d10_victory

Background S1; character B0. One choice: **Leave Stormcourt** -> `win`.

The Sovereign Echo collapses. Lightning leaves the empty armor, and the pressure lifts from the court. The remaining binding instruments fall silent. For the first time since you entered, the thunder carries no voice. The Thread's prison and storm binding are both broken. Rain falls through Stormcourt without being drawn back toward the dais. You leave no keeper behind.

**win.description:** You leave Stormcourt as the rain settles over the silent court.

**win.successDescription:** Stormcourt is cleared. The binding is broken.

**fall.description:** This attempt ends before Stormcourt is cleared.

Keep `fall.successDescription` empty. No shared Tower, further pyramid, named reward item or new collectible is promised in this ending. Its local-binding resolution is proposed for acceptance, not an assertion about the fate of a deity or either sister.

## 7. Battle labels and outcome fields

For each of the 50 pre-battle rows above, set its paired battle's `description` to the following exact format, substituting the row's local battle number and full enemy name:

`Battle {number}/25: {enemy}.`

Examples: `b1_1` = `Battle 1/25: Umbral Reaver.`; `b5_boss` = `Battle 25/25: Warden of the Half Eclipse.`; `b6_1` = `Battle 1/25: Hollow Lantern Ascendant.`; `b10_boss` = `Battle 25/25: Sovereign Echo of the Godstorm.` The scene tables supply all 50 substitutions; no names or old global floor numbers are inferred during implementation.

Replace the four outcome fields on every battle with the scoped text below. This is copy specification, not authorization to alter outcome matching, routing, gains or drops.

| Scope | Field | Exact replacement |
|---|---|---|
| 40 regular battles | successDescription | The guardian falls. You can advance. |
| Eight intermediate keepers | successDescription | The keeper falls. The next passage is clear. |
| b5_boss and b10_boss | successDescription | The last keeper falls. |
| All 25 Marrow battles | failDescription | You are defeated. Marrow Vaults remains uncleared. |
| All 25 Marrow battles | drawDescription | The battle ends in a draw. Marrow Vaults remains uncleared. |
| All 25 Marrow battles | fleeDescription | You disengage before clearing Marrow Vaults. |
| All 25 Stormcourt battles | failDescription | You are defeated. Stormcourt remains uncleared. |
| All 25 Stormcourt battles | drawDescription | The battle ends in a draw. Stormcourt remains uncleared. |
| All 25 Stormcourt battles | fleeDescription | You disengage before clearing Stormcourt. |

Keep `completionOutcome`, `keepOriginalPools`, scaling, opponent arrays, failure targets and all other combat configuration unchanged unless separately approved. The wording promises neither an inventory clawback nor a checkpoint, heal or resumable run. Retained dialog `successDescription` fields remain empty.

## 8. Review and implementation boundaries

### Rewards and branded shared items

This copy promises no item, amount, currency, completion frequency or new drop channel. Content Admin must supply two full-clear packages and approve a neutral/Godstorm reward identity. The old shared Endless Night Chest must not be silently renamed: check every consumer, all enemy drop channels and existing inventory implications. Do not ship empty consumable rewards or blindly carry over unapproved historical final payouts. Reward fields are intentionally absent from this authoring specification.

### External records and player state

After copy acceptance, identify actual hub/menu records, grants, descriptions and links that serve these quests. No specific external record is claimed edited or exhaustively inventoried here. Remove the discarded concept from the released route without bulk-renaming evidence, stable IDs, source filenames or history. No new wrapper quest is requested.

Existing trackers can reference the sixteen removed dialogs; prior withdrawals may have set successful-completion flags. Fable must provide a bounded operator transition/recovery plan. Do not revoke completions or reset inventories automatically. The preserved Marrow ID supplies the existing Stormcourt prerequisite for new full clears, subject to source and runtime verification.

### Artwork and unperformed checks

All image matches remain proposed until original-file recovery, record validation, pixel inspection and art-pipeline acceptance. The five default-avatar assignments remain separate work. Regular-guardian prose does not require additional scene portraits. Shared jutsu/effect/alternate-avatar visual dependencies remain their bounded inventory task.

No local repository clone, repository validator, factory, harvest normalization, graph-derived production shotlist, art preflight, pixel review, engine simulation or live playtest was completed for this authoring pass. This is an editorial map built from read source records, not a generated production shotlist. Before implementation, reproduce the mapping from the untruncated captures and validate the exact Fable payload SHA against the agreed source/contracts.

Local consistency checks over the authored draft passed: 52 unique dialogs; 50 battle rows; 18 opponent IDs; 16 removal targets; eight reroutes; one start and 53 nodes per quest; valid pointers; one direct dialog predecessor per battle; every success path traverses its 25 battles in order; only final victory dialogs lead to win; 50 failure links lead to fall; no removed node remains; ten keeper and 42 blank assignments; background allocation 15/10/1/26; five surviving captured background bindings preserved. Proposed player-facing strings contain no discarded branding, key promise, paid-withdrawal terminology or old Stormcourt floor labels. These are authored-model checks, not a game certification.

## 9. Acceptance checkpoint

Review the 52 dialog bodies, two listing descriptions and outcome text. The two substantive narrative choices are the explicit records-to-Stormcourt link and the binding-breaking finale. Approving copy does not approve uninspected images, exact rewards or live operation.

After acceptance: prove artwork reuse, supply actual accepted scene-character IDs, close reward decisions, and have Fable construct independently reviewed, validated changes. The operator then applies the approved package and supplies full readback. This draft does not merge main, generate artwork, create a mutation manifest or change production.
