# Godstorm: Marrow Vaults and Stormcourt release plan

Updated: 2026-09-15
Status: STRUCTURAL DIRECTION APPROVED; implementation, final copy, art acceptance, balance, rewards and publication are not complete.
Repository evidence baseline: `perseverance484/tnr-tools@6e09b15bb6f3d1c90ba416d14211b533f5b4a367`.
Planning revision base: `chatgpt/godstorm-two-pyramid-plan@056e484f4af0323198ada48cdc6dd9aecf1e59c8`.
Governing decisions: `docs/RULINGS.md`, RUL-2026-09-15-002 and RUL-2026-09-15-003. This plan owns the operative task requirements; the ledger records decision history.
Copy and scene map: `docs/plans/GODSTORM_STANDALONE_COPY_AND_SCENE_MAP.md`, Draft 2. The filename is retained; the Godstorm locations are connected, not separate sites.

Owner split: dauntless directs, accepts and alone operates the game. Content Admin settles the delegated chest/reward decisions. ChatGPT plans, reviews and supports art. Fable remains the normal manifest/tool implementation owner. This revision changes planning documents only; it is not a live-game action or an executable payload.

## 1. Approved concept separation and connected setting

The user approved the retained structure and directed that Tower of Endless Night be stripped entirely from both retained pyramids. Early cash-out belongs to the separate Tower of Endless Night concept, not these Godstorm quests.

The spatial relationship is now explicit: **one structure, with Marrow Vaults below and Stormcourt above**. The player enters through the lower Vaults. Clearing Marrow opens the passage into the upper Court. Godstorm is separate from Tower of Endless Night; its own two locations are not geographically separated. Do not reintroduce a records-based search for a distant second site or invent another overall structure name.

| Release identity | Battles | Keepers | Final encounter | Successful completion |
| --- | ---: | ---: | --- | --- |
| Marrow Vaults | 25 | 5 | Warden of the Half Eclipse | Clear all 25 battles; gain access to the Court above |
| Stormcourt | 25 | 5 | Sovereign Echo of the Godstorm | Clear all 25 battles; conclude the connected Godstorm release |

Requirements:
- Use the player-facing titles `Marrow Vaults` and `Stormcourt`, without the Tower of Endless Night prefix, subtitle or identity. The shared building is the Godstorm setting, not that separate Tower concept.
- Preserve the existing 25-encounter order and five-keeper grouping in each quest. Retain 50 battles, ten keepers and the existing 18 direct-opponent AI records.
- Remove every early paid withdrawal/cash-out branch from both quests. There is one full-clear ending per pyramid and no alternate successful exit before battle 25.
- Remove accumulated-winnings, gambling/bait, gold-door withdrawal and Tower forfeiture framing from all retained descriptions and outcome text. Ordinary abandon/failure handling is not an early paid completion.
- Retain the two locations' usable story and art as lower Vaults and upper Court within one structure. Marrow's ending opens the way upstairs; Stormcourt's opening continues that ascent. Its finale must end the release, not lead to Crown or the separate Tower concept.
- Dawnless Crown remains outside this release. Do not import its battles or The Endless Night boss.
- Keystones remain unnecessary; remove their stale grants and promises, not replace them with new key items.
- Preserve quest IDs, retained objective IDs, AI records, kits and original artwork wherever possible. Continue using the `battlepyramid` engine type; the concept/name change is not authorization for a schema/type conversion.
- Reserve Tower of Endless Night and its cash-out mechanic separately. Archiving its current evidence is in scope; designing, publishing or operating that separate concept is not.

Preserve the existing Marrow-to-Stormcourt prerequisite. The two quest records remain separate mechanically: this connection adds no travel task, automatic second-quest launch, combined progress tracker, shared resource pool or reward policy. Any such feature requires its own supported implementation and approval. Physical access is expressed in the final vault dialog and first court dialog without adding scene nodes.

This approves structure and spatial progression, not unseen artwork, exact prose, numerical tuning, a daily cap, new checkpoints, inventory clawbacks or publication. Those gates remain explicit below.

## 2. Evidence and status discipline

- E1: `harvests/inbox/tnr_results_1789401726302.json`, September 14 16:02 UTC: full quest graphs for the three original roots.
- E2: `harvests/inbox/tnr_results_1789402842027.json`, September 14 16:20 UTC: AI records, embedded kits/items, reward point reads and four background records.
- E3: `harvests/inbox/tnr_results_1789403623148.json`, September 14 16:33 UTC: associated AI profiles and excluded final-boss equipment.
- Discovery only: `answers/names_asset.json` and `harvests/seed/43_INDEX_asset.json`, stamped August 24. A catalog name is not proof of present-day validity or absence.
- Historical planning: this file and `GODSTORM_TWO_PYRAMID_VERIFICATION_NOTES.md` at revision base `11c55562f440e804a546163cb747a9fc8bc7e95c`. Preserve that history; its cash-out policy, ten exit-reward packages and 68-dialog delivery target are superseded.
- Draft 1 at `056e484f4af0323198ada48cdc6dd9aecf1e59c8` is superseded where it treated Stormcourt as a second site discovered through records. Draft 2 replaces that narrative handoff with access upstairs in the same structure.

Authority remains `docs/00_INDEX.md`, `docs/DOCTRINE.md`, `docs/ENGINE_LAWS.md` under the router's evidence rules, `CHATGPT.md`, `docs/DEVELOPMENT_WORKFLOW.md`, applicable role/workflow files and routed content/art specifications. This task changes no doctrine or engine law.

Captured state is not the revised live state. Non-default image assignment is not image QC. A graph count is not a playtest. Source pins used by prior reviews are documented in the verification notes; neither is assumed to be the deployed revision or silently adopted as a regenerated contract.

## 3. Exact planned graph simplification

This is the recommended minimal rewrite implementing the approved no-cash-out structure, not a completed mutation or a substitute for graph validation. The shared-building clarification does not change these targets.

| Graph measure | Existing capture, each | Revised target, each | Revised pair |
| --- | ---: | ---: | ---: |
| Battles | 25 | 25 | 50 |
| Pre-battle dialogs | 25 | 25 | 50 |
| Continue/cash-out choice dialogs | 4 | 0 | 0 |
| Paid-withdrawal payoff dialogs | 4 | 0 | 0 |
| Final-victory dialogs | 1 | 1 | 2 |
| Dialog total | 34 | 26 | 52 |
| Terminal nodes | 2 | 2 | 4 |
| Objective total | 61 | 53 | 106 |

Remove eight cash-out-related dialogs per quest, sixteen total. Migrate any indispensable narrative from those nodes into retained introductions or the victory dialog; do not add replacement filler.

Removal targets in E1:
- Marrow: `d1_choice`, `d1_cash`, `d2_choice`, `d2_cash`, `d3_choice`, `d3_cash`, `d4_choice`, `d4_cash`.
- Stormcourt: `d6_choice`, `d6_cash`, `d7_choice`, `d7_cash`, `d8_choice`, `d8_cash`, `d9_choice`, `d9_cash`.

Reroute the four intermediate keeper wins per quest to the next retained pre-battle dialog: Marrow `b1_boss -> d2_1` through `b4_boss -> d5_1`; Stormcourt `b6_boss -> d7_1` through `b9_boss -> d10_1`. Never link keeper battle directly to the next battle: preserve every dialog shield. Retain `b5_boss -> d5_victory -> win` and `b10_boss -> d10_victory -> win` as the respective successful endings, subject to reward-timing validation.

Keep `fall` and the existing failure routing as the starting implementation shape; review their text and runtime behavior. No new checkpoint/retry mechanism is approved. Extract actual payload IDs programmatically from captures before implementation, rather than copying this planning list into a hand-built mutation.

Old internal floor numbers may remain in stable IDs. Player-facing Stormcourt text must not describe it as floors 6-10 of Tower of Endless Night; local stage/location language and an upstairs connection are compatible. Do not renumber IDs merely for presentation.

Counts assume removal of both choice and withdrawal dialogs without extra replacement nodes. Any necessary structural departure must be explained, recounted and reviewed before handoff.

## 4. Current inventory versus the new delivery target

| Surface | Captured evidence | Planned target/work after simplification |
| --- | --- | --- |
| Quest roots | Marrow `2yvE9PUQqlD8lbYNfgX-b`; Stormcourt `OSADdXqostbyVliCxWk6k` | Same IDs; renamed and reframed |
| Captured visibility | Both hidden true | Reconcile ordinary-player availability; no automatic flip |
| Direct AI/profile inventory | 18 retained opponents and associated profiles captured | Same roster; functional and balance QA still required |
| Primary avatars | 13 non-default / five default | Five missing assignments unchanged by cash-out removal |
| Listing images | Two non-default assignments | Inspect and reuse; remove baked-in Tower branding only if present |
| Background candidates | Three Marrow plates plus shared-library StormCourtyard | Inspect and maximize reuse; no automatic new paintings |
| Current dialog backgrounds | Seven Marrow, zero Stormcourt | Only five of those seven survive the proposed deletion; fill 21 Marrow + 26 Stormcourt = 47 gaps |
| Scene characters | None wired in captured dialogs | 52 dialog assignments, not 68 |
| Keeper-focused portrait option | Ten keeper identities | Ten keeper placements plus 42 blank placements; two main fallbacks |
| Completion reward packages | Ten historical alternative payouts | Two approved full-clear packages needed; values open |
| Revised live implementation | None verified | Source/graph validation, operator changes and full readback pending |

The lower scene counts reduce processing/wiring and QA work, not the number of retained enemy identities. Previously completed registrations and source images are not deleted just because a node using them is removed.

## 5. Retained AI artwork roster

Present means a non-default primary avatar assignment in E2, not fresh visual acceptance.

| Pyramid | AI | Role | Primary avatar |
| --- | --- | --- | --- |
| Marrow | Umbral Reaver | Recurring guardian | Default |
| Marrow | Hollow Lantern | Recurring guardian | Default |
| Marrow | Starless Monk | Recurring guardian | Default |
| Marrow | Nightveil Sentinel | Recurring guardian | Default |
| Marrow | Warden of the First Dark | Keeper 1 | Default |
| Marrow | Keeper of Hushed Hours | Keeper 2 | Present |
| Marrow | The Moth Tyrant | Keeper 3 | Present |
| Marrow | Chained Chorister | Keeper 4 | Present |
| Marrow | Warden of the Half Eclipse | Keeper 5 / Marrow finale | Present |
| Stormcourt | Hollow Lantern Ascendant | Recurring guardian | Present |
| Stormcourt | Starless Monk Ascendant | Recurring guardian | Present |
| Stormcourt | Nightveil Sentinel Ascendant | Recurring guardian | Present |
| Stormcourt | Umbral Reaver Ascendant | Recurring guardian | Present |
| Stormcourt | The Gloaming Judge | Keeper 1 | Present |
| Stormcourt | Widow of the Waning Moon | Keeper 2 | Present |
| Stormcourt | The Candlewright | Keeper 3 | Present |
| Stormcourt | Herald of the Last Dusk | Keeper 4 | Present |
| Stormcourt | Sovereign Echo of the Godstorm | Keeper 5 / release finale | Present |

Reuse proposal: test the four existing Ascendant images for the matching base-enemy avatars. Keep names, kits and distinct records. Pixel approval is still required; shared family artwork is not silently accepted by structural approval. Resolve First Dark from suitable existing art or one new master serving both avatar and scene portrait.

Nine keepers already have primary images to inspect for scene adaptation. Search compatible existing scene records first; otherwise prepare a valid extraction/bust, with a source-guided redraw only when necessary. No additional recurring-guardian portrait set is committed to release scope.

Crown-only enemies stay excluded: The Suture Priest, The Twinned Reliquary, The Loomwright, Warden of the Severed Dawn and The Endless Night. Do not carry the latter's damage-stack/Heavy Armor diagnosis over to Sovereign Echo. Do not delete these records or globally edit shared kits as part of the separation.

## 6. Environment and scene-character work

Existing Marrow background assignments that survive:
- `marrow vault 1` (`7EmVo6GH5GL4YtQTDrbDR`): `d1_1`, `d1_2`, `d1_boss`.
- `marrow vault 2` (`oc0cXiMrcG_6kTUwNWRkn`): `d1_3`, `d1_4`.
- `marrow vault 3` (`IykL5XxwFF14BosCblZj8`): its only captured placement, `d1_cash`, is removed. The artwork remains available; assess whether it fits the passage/stair-access payoff instead of an exit to a separate destination.

`d1_choice` also had plate 1, so seven existing assignments become five, not six. The expected new background-binding work is 47 assignments across 52 dialogs; review the surviving five as well.

`StormCourtyard` (`cKHhHoboreP88iH5WjDe7`) is a captured SkychainMonastery asset, not dedicated Godstorm art, and is unwired. Inspect it and other library candidates such as AbbotsBellDais, SummitShrine and SkychainOpening before commissioning. Candidate catalogs remain discovery evidence only. Do not alter shared original assets to force a match.

Plan zero new environment paintings initially, conditional on actual fit. The connected-setting clarification adds no new art commission: compose the lower-vault to upper-court transition within the existing ending and opening scenes. Preserve suitable architecture while removing unrelated Tower branding. Image suitability remains unverified until pixel review.

Recommended scene-character scope remains ten keeper portraits plus one verified blank utility. With the simplified graphs, wire ten keeper introductions and 42 other dialogs; use deliberate background and blank-character quest fallbacks. Verify current render and publish guards against the implementation pin. Filling dialog characters alone must not be assumed to satisfy every publication guard.

Blank candidates: `Q-_3WA5kibe_8gI2CgTKl` and `1YXbXYW2wz3GETVMb6DT6`. Verify type, image and actual blank pixels before reuse. Use the current art skill/spec for framing, format, resolution, transparency, byte budget, fresh filenames, visual QC and acceptance. A primary avatar with a painted backdrop is not automatically a scene-character file.

## 7. Full content-separation pass

Inspect both quest names, descriptions, success descriptions, every retained objective's text, choice labels, battle success/failure/flee/draw text, final victory and terminal text, plus entry menus/hubs and promotional material that serve these quests.

Remove or rewrite:
- Tower of Endless Night and its title shorthand, not the approved shared-building relationship between the Godstorm locations.
- Paid early withdrawal, accumulated winnings, gold doors, betting nerve, climbing for a larger cash-out and total-banked-fortune forfeiture.
- Keystone claims, inventory-key progression and Crown continuation.
- Stormcourt floor references that identify it as part of the separate Tower concept.
- Draft 1's records-to-a-second-site explanation and departure to another location. The final vault threshold instead opens the way upstairs.
- A finale that resolves only an intermediate stage of the removed Tower story.

Retain appropriate Godstorm characters and plot material as a coherent lower-prison/upper-binding story in one structure. Draft the new Stormcourt ending around defeating Sovereign Echo and refer back to the cleared Vaults below. Do not merely replace the word Tower while retaining the abandoned cash-out motivation. Exact prose remains subject to acceptance.

Reuse the two listing images if the actual pixels fit and contain no unwanted title text. Historical capture names, stable IDs, raw evidence, Git history and internal filenames do not require a bulk rename. New player-facing documents must use Marrow Vaults and Stormcourt, not Tower 1-2.

Important shared-item issue: `Endless Night Chest` (`HLycjzUcVwKZenBWpd0V-`) is itself Tower-branded. No final Godstorm reward package may leave that player-facing dependency unaddressed. Content Admin must select an existing suitable neutral/Godstorm reward, approve a safe rename/reuse after a full consumer review, approve a distinct reward identity, or omit the chest. Do not globally rename the shared item or assume existing player copies and the separate Tower concept are unaffected. Preserve useful chest art where available; do not select a new reward name implicitly.

## 8. Progression and legacy players

For new runs, deleting every early successful exit allows the retained Marrow prerequisite to represent the intended full 25-battle clear, subject to source validation and regression tests. No separate full-clear marker or replacement key is required merely to distinguish early cash-out from full clear once those alternative success paths are gone.

The previous debate between early-withdrawal unlocking and a new full-clear marker is superseded for new runs. Do not remove the existing Marrow prerequisite or add a new one without a separate decision. Express the approved upward progression through the revised ending and opening; do not add an automatic quest launch or travel objective by implication.

Historical successful completions may have been earned through old cash-outs. Do not silently revoke them or reset player records. If strict retrospective full-clear eligibility is required, surface that as a separate operator decision with migration consequences. Active trackers can also point to the sixteen removed dialogs: prepare an explicit protected transition before changing production graphs, even though retained IDs stay stable.

Review loss, flee, draw, abandon and resume behavior. Preserve normal engine behavior unless separately approved; removing paid withdrawals is not authorization to remove ordinary abandon controls, create checkpoints, promise resumability, confiscate inventory, or claw back combat gains.

## 9. Content Admin reward packet

Status remains OPEN. The packet now needs TWO full-clear reward specifications, not ten cash-out tiers. Sharing one physical structure does not combine these packages or settle their values.

Historical full-clear values from E1, for review only:

| Quest | Ryo | Tokens | Prestige | Chest roll |
| --- | ---: | ---: | ---: | --- |
| Marrow | 125,000 | 25 | 10 | 5% chance of one old chest |
| Stormcourt | 250,000 | 150 | 60 | 10% chance of one old chest |

Do not sum removed withdrawal rewards into these values or transfer Crown's payouts automatically. Early payout fields disappear with their branches; this is not approval of the surviving amounts.

E2 records an empty old chest reward table, default icon and destroyOnUse true. Some enemy inventories also contain chest drops. Audit all grant channels, including these, when eliminating Tower-branded rewards. A final reward must not be an empty consumable.

Recommendations, not finalized values:
- Evaluate two completion packages against full 25-battle clear time, intended challenge and allowed completion frequency.
- Prefer meaningful reliable rewards with an optional bonus, using approved existing items/art before new reward content.
- Keep reward timing legible: one full-clear package per pyramid, no early paid exit. Separate ordinary combat gains and any approved per-enemy loot from that completion package.
- Consider a consistent capped daily rewarded-clear cadence; approve period, completion count and attempt policy together. Do not assume the string daily alone imposes one successful clear per day.
- Resolve the old chest's identity and shared-consumer impact before any rename or replacement. Include existing player copies in the decision.
- Keep exact ryo, tokens, prestige, chest contents/chances/quantities, rarity, trade rules, ordinary boss drops and cadence open for Content Admin.

These decisions do not block original-art recovery or non-reward drafting. They block executable reward changes and final release acceptance. No earlier generic reward recommendation becomes approved merely because the structure was approved.

## 10. Remaining visual dependencies

Five primary-avatar assignments, ten keeper-portrait delivery targets and 52 scene mappings are different work units, not one number of newly painted images. The two quest images and four background candidates are reuse inputs; a blank is one reusable asset, not 42 new assets.

Close the retained-kit icon, effect/animation, SFX, actual summon and alternate-avatar client-use census before freezing the visual budget. Some shared kit images are defaults; neither universal replacement nor zero remaining work is justified without this check. Shared record changes need consumer/ownership review.

Chest art remains zero or one conditional assignment after the reward identity decision. Keystone art remains zero. No new map-pin family, 3D set or recurring-guardian portrait expansion is presumed. Any original commissions follow source recovery, a reuse pilot and final art approval.

## 11. Ordered work and owners

| Step | Owner | Deliverable / gate |
| --- | --- | --- |
| 1. Record direction | ChatGPT | This plan and RUL-2026-09-15-002/003; structure and spatial relationship approved, not implementation |
| 2. Reproduce the revised inventory | Fable extracts; ChatGPT reviews | Exact retained ID joins; verify sixteen removal targets and eight reroutes; reproduce 106 objectives / 52 dialogs / 47 missing background bindings; resolve auxiliary visual dependencies |
| 3. Register approved coordination | Planning owner | Existing workstream tooling creates/validates task roadmap and packets; no hand-edited generated projections |
| 4. Recover originals and test reuse | ChatGPT; dauntless accepts | One keeper scene adaptation and one family-avatar reuse example pass target QC; inspect backgrounds and listing images |
| 5. Review connected Godstorm copy and storyboard | ChatGPT; dauntless accepts | Draft 2 in the copy/scene-map file; lower Vaults, upstairs handoff, upper Court and complete finale; 52-scene map; entry/reference cleanup inventory |
| 6. Finish accepted visual outputs | ChatGPT art lane | Five avatar gaps closed by approved reuse/new sources; ten keeper portraits or eligible records; verified blank; accepted background selections and file/provenance ledger |
| 7. Audit retained combat | ChatGPT; Fable source/fixture support | All 18 rule/profile/kit joins, target/range/cooldown/AP/fallback checks, effective stats/pools/equipment and shared-dependency findings; approved correction proposals |
| 8. Approve rewards | Content Admin; dauntless | Two full-clear specifications, cadence/attempt limits, chest identity and all drop channels; no unapproved numerical defaults |
| 9. Build reviewed correction package | Fable implements; ChatGPT independently reviews | Factory/validator-backed payloads; preserved data/IDs; no accidental kit renormalization; exact-SHA handoff; preimage, active-player and recovery plan |
| 10. Operator apply and readback | dauntless | Fresh before-state checks; approved protected writes; complete persisted readbacks compared to intended changes |
| 11. Calibration and acceptance | Operator/testers; ChatGPT reviews | Both 25-battle traversals, retained outliers, failure/re-entry, legacy completion, mobile render and reward tests; corrections revalidated/read back |
| 12. Release | dauntless following Content Admin go-ahead | Final accepted Godstorm-only availability, Crown exclusion, no obsolete Tower cash-out entry points or labels, durable closeout evidence |

Steps 4-8 can progress in parallel when their inputs are stable. Fable remains implementation owner; this documentation update does not take over that lane or authorize a live run. The exact copy and proposed 52-scene map remain acceptance work, with source-file recovery and census verification in parallel.

## 12. Acceptance tests

- Scope: one Godstorm structure with lower Vaults and upper Court, represented by two titled 25-battle/five-keeper quests; no reachable paid early exit; no Crown continuation.
- Graph: one intended start per quest; every battle immediately dialog-gated; all pointers valid; intermediate keeper wins reach the next dialog, not another battle; only the final clear reaches success. Verify the expected 53 objectives per quest or document an approved deviation.
- References: no surviving edge or UI choice points to any of the sixteen removed dialogs; no alternative reward-bearing early-win path exists.
- Legacy safety: active trackers referencing removed nodes are handled by an approved operator procedure; historical completions are not silently revoked; old manifests cannot restore cash-outs.
- Outcomes: wins, loss/flee/draw, abandon, retries and reload/resume behave as specified; no partial clear awards the final package; no new inventory forfeiture mechanic.
- Progression: test no Marrow completion, incomplete/failed Marrow run, a new full Marrow clear and legacy completion flags against the preserved Stormcourt prerequisite. No unapproved auto-launch or travel task is introduced by the upstairs narrative.
- Visuals: all 18 primary avatars, two listing images and 52 dialog scenes resolve to accepted assets; ten keeper/42 blank assignments under the proposed portrait scope; deliberate quest fallbacks; all 47 missing background bindings closed; the third Marrow plate reassessed for the upstairs handoff, not treated as deleted art.
- Copy: lower entry -> cleared Vaults -> open passage upward -> Court finale is coherent. Remove Tower identity, early cash-out framing and the separate-site explanation from retained copy. Inspect image pixels for baked-in branding without commissioning replacements automatically.
- Rewards: two accepted completion packages; all item references valid; no empty consumable or unreviewed shared-item rename; chance versus quantity and ordinary enemy drops accounted for; actual period/attempt limits verified.
- Combat: test representative eligible, intermediate and endgame loadouts; record damage, control, resources, turns, outcome and clear time. Calibrate retained bosses, not the excluded Endless Night boss. Exact targets remain user-owned.
- Data: art-only edits preserve stats, kit, profile and unrelated fields; full before/after comparison; source contracts reconciled before payload building; publishing remains a separate operator step.

## 13. Execution limits and history

This revision used live GitHub refs and the current committed planning/copy documents, not live-game requests. A local Git access attempt failed on DNS; no clone or repository session guards, harvest-normalization run, graph validator, image QC, game simulation or live playtest was completed in this turn. Graph and asset targets are unchanged by this narrative revision and still require reproduction against the captured graphs and eventual Fable payload. No script execution is implied by structural or spatial approval.

Before building, reconcile the applicable source contracts and source-version disagreements noted by prior reviews. Before a production write, refresh the affected record preimages and halt on unexpected drift. Preserve historical captures and original artwork. Do not bulk-rename internal evidence to erase its Tower provenance.

The earlier cash-out planning version remains retrievable at `11c55562f440e804a546163cb747a9fc8bc7e95c`. Its 68-dialog art map, eight paid withdrawals, ten exit rewards and unresolved early-cash-out unlock choice are historical, not current release requirements. The second-site narrative remains retrievable in Draft 1 at `056e484f4af0323198ada48cdc6dd9aecf1e59c8` but is superseded by the connected setting. The separate Tower of Endless Night concept remains reserved; this revision neither implements nor publishes it.
