# Godstorm: two-pyramid release plan

Prepared: 2026-09-15
Status: PLANNING / awaiting approval of recommendations. Not an executable manifest.
Repository baseline: `perseverance484/tnr-tools@6e09b15bb6f3d1c90ba416d14211b533f5b4a367`
Owner split: dauntless directs and accepts; Content Admin settles the delegated chest/reward decisions; ChatGPT plans, audits and supports art; Fable normally implements manifests/tooling; dauntless alone operates the live game.

## 1. Scope and decision boundary

User-set direction:
- Retain Marrow Vaults and Stormcourt as the two release pyramids.
- Cut Dawnless Crown from release scope and maximize reuse of existing artwork.
- No new keystone assets. This plan proposes removing their obsolete reward references and promises rather than recreating the missing items.
- Complete planning before execution. Chest contents and reward values remain open for Content Admin, with recommendations supplied here.

Recommended implementation scope, not yet accepted:
- Retain the existing 25 battles per retained quest: 50 battles, ten floors, ten keepers in total.
- Retain existing quest IDs, enemy records, kits and objective IDs wherever possible. Do not transplant the additional 25 Dawnless battles into the retained quests.
- Make Sovereign Echo of the Godstorm the release finale. Rewrite the Stormcourt ending to close the story instead of advertising another pyramid.
- Use the four captured background assets before commissioning more environments.
- Give the ten retained keepers scene portraits adapted from existing art where viable; use one verified blank scene-character asset for other dialogs. Eight recurring-guardian portraits are a separate optional expansion.

Removing release scope is not deleting a live record. Archive/exclude Dawnless and preserve recoverable records. No live retirement, rewrite, publishing change or asset generation has been performed by this planning document.

## 2. Evidence, authority and limits

Evidence at the baseline:
- E1: `harvests/inbox/tnr_results_1789401726302.json`, captured 2026-09-14 16:02 UTC. Full quest records for all three original pyramids; `journal.manifestPath` identifies `push/23_godstorm_tower_root_capture.json`.
- E2: `harvests/inbox/tnr_results_1789402842027.json`, captured 2026-09-14 16:20 UTC. Full 23 AI records, their embedded kits/inventories, chest and keystone point reads, and four background records; manifest 24.
- E3: `harvests/inbox/tnr_results_1789403623148.json`, captured 2026-09-14 16:33 UTC. Full 23 associated AI profiles and the old final boss's Heavy Armor; manifest 25.
- E4: `answers/names_asset.json`, 407-row catalog stamped 2026-08-24. Discovery only, not proof of current absence or current validity. It contains existing blank-character candidates.
- E5: original audit on `chatgpt/godstorm-pyramid-final-audit@18e3367a5f45a9d4a81ad0bdec955eb22556a522`, `docs/reviews/REVIEW_2026-09-14_godstorm_tower_final_audit.md`. Historical three-pyramid review, not the new release scope.

Authority/routing: `docs/00_INDEX.md`, `docs/DOCTRINE.md`, `docs/RULINGS.md`, `CHATGPT.md`, `docs/DEVELOPMENT_WORKFLOW.md`, the Content Designer / Release Auditor / Art Director role files, and `docs/workflows/CONTENT_WORKSTREAM.md`, `DIRECTOR_DECISIONS.md`, `ART_PRODUCTION.md`.

Content references: `skills/building-tnr-content/references/quest.md`, `ai.md`, `balance.md`, `item.md` and `pipeline.md`. Production-art authority: `skills/producing-tnr-art/SKILL.md` and `data/25x_DATA_art_spec.json`; use its current targets and processing tools rather than copying remembered constraints.

Additional source inspection pinned to `studie-tech/TheNinjaRPG@31996f1f9cb10dae246740afe273f164a2bb469b`: `app/src/libs/quest.ts` (availability/prerequisite checks and reward collection) and `app/src/layout/Logbook.tsx` (`QuestDialogScene`). This is a source-review pin, not proof of the deployed game's revision and not adoption of regenerated contracts.

Evidence limits:
- The captures show stored content on September 14, not a new live read performed during this plan.
- Non-default image assignment means an existing-art candidate, not fresh proof that the file loads, meets current art specifications, has sufficient source resolution, or has passed visual acceptance.
- CDN image bytes could not be retrieved for fresh pixel inspection in this session. Image recovery, visual comparison and mechanical QC are explicit first-stage work.
- Container checkout could not be established. Session guards, harvest normalization/verification, shotlist generation, validators and playtests have NOT been run in this planning pass. Connector reads support the inventory; the implementation handoff must reproduce it programmatically from E1-E3.
- The older global state projection remains focused on Forsworn work. It is not evidence that these pyramids or their new consolidation are complete. Do not rewrite unrelated global state to hide that distinction.

## 3. Corrections to the previous infographics

The two-pyramid infographic is superseded as an asset census.

1. Original scope: 23 unique AIs, 14 non-default primary avatar assignments, nine defaults.
2. Retained scope: 18 unique AIs, 13 non-default primary avatar assignments, five defaults.
3. Dawnless-only removals: The Suture Priest (existing avatar), The Twinned Reliquary, The Loomwright, Warden of the Severed Dawn and The Endless Night (four defaults).
4. Twinned Reliquary and Loomwright are Dawnless keepers, not Marrow keepers. Do not keep them in the two-pyramid art backlog.
5. The prior seven-missing-avatar count was incorrect. The prior two-new-background and six-scene-portrait counts were unverified design allocations, not engine-derived minimums.
6. Fifty configured battles is not fifty completed playtests. The revised two-pyramid package has not been implemented or certified.
7. Infographic concept panels are not counted as production game assets or approved replacements for captured artwork.

## 4. Current state of each retained pyramid

| Surface | Marrow Vaults | Stormcourt | Remaining work |
| --- | --- | --- | --- |
| Quest root | `2yvE9PUQqlD8lbYNfgX-b` | `OSADdXqostbyVliCxWk6k` | Preserve IDs unless an approved migration requires otherwise |
| Floor range | 1-5 | 6-10 | Recommended retained layout; final scope approval required |
| Battles | 25 configured | 25 configured | Recheck all transitions after edits; then playtest |
| Keepers | 5 | 5 | Retain; tune against approved player targets |
| Unique AI records | 9 | 9 | All have capture evidence; audit kits and behavior, not just existence |
| AI profiles | 9 captured | 9 captured | Rule-to-kit, target, range, cooldown and fallback checks |
| Dialogs | 34 | 34 | Two-pyramid narrative pass and scene wiring |
| Listing image | 1 non-default assignment | 1 non-default assignment | Recover and inspect; reuse |
| Primary AI avatars | 4 assigned, 5 default | 9 assigned, 0 default | Fill five Marrow assignments; inspect all retained art |
| Dedicated background records | 3 captured | 1 captured | Reuse before commissioning new art |
| Explicit dialog backgrounds | 7 of 34 | 0 of 34 | Fill 27 + 34 = 61 missing dialog assignments |
| Explicit dialog characters | 0 of 34 | 0 of 34 | Configure all 68 dialogs with approved portrait or verified blank |
| Voluntary cash-out branches | 4 | 4 | Check payout, terminal state and progression semantics |
| Full-clear payout dialog | 1 | 1 | Remove obsolete keystone references; admin chooses rewards |
| Captured repeat delay | `none` | `daily` | Admin decides intended cadence and limits; verify actual counter semantics |
| Captured limits | maxAttempts 100 / maxCompletes 100 | maxAttempts 100 / maxCompletes 100 | Do not call these an approved daily budget or assume unlimited behavior |
| Captured visibility | hidden true | hidden true | Verify player-facing availability through operator workflow before release |

Each existing retained graph has 34 dialogs, 25 battles and two terminal nodes: 61 objectives, 122 across the pair. The intended retain-in-place plan preserves that count unless a supported full-clear unlock fix requires an approved structural change. E1 is the source for the exact graph and fields.

The current dialog-gated battle/failure-route pattern is reusable. It does not certify the revised story, asset references, repeat limits, reward economics or actual combat difficulty.

## 5. AI and keeper asset inventory

Status below concerns the captured primary `avatar` field. All named scene-character placements remain unwired. Do not infer `avatarLight`, 3D or animation readiness from primary-avatar presence.

### Marrow Vaults

| Enemy | Use | Primary avatar | Recommended treatment |
| --- | --- | --- | --- |
| Umbral Reaver | Recurring guardian | Default | Evaluate reuse/adaptation of Umbral Reaver Ascendant art |
| Hollow Lantern | Recurring guardian | Default | Evaluate reuse/adaptation of Hollow Lantern Ascendant art |
| Starless Monk | Recurring guardian | Default | Evaluate reuse/adaptation of Starless Monk Ascendant art |
| Nightveil Sentinel | Recurring guardian | Default | Evaluate reuse/adaptation of Nightveil Sentinel Ascendant art |
| Warden of the First Dark | Floor 1 keeper | Default | Inspect suitable existing source; otherwise one new source serving avatar and scene portrait |
| Keeper of Hushed Hours | Floor 2 keeper | Assigned | Preserve avatar; inspect source for scene-portrait adaptation |
| The Moth Tyrant | Floor 3 keeper | Assigned | Preserve avatar; inspect source for scene-portrait adaptation |
| Chained Chorister | Floor 4 keeper | Assigned | Preserve avatar; inspect source for scene-portrait adaptation |
| Warden of the Half Eclipse | Floor 5 keeper | Assigned | Preserve avatar; inspect source for scene-portrait adaptation |

### Stormcourt

| Enemy | Use | Primary avatar | Recommended treatment |
| --- | --- | --- | --- |
| Hollow Lantern Ascendant | Recurring guardian | Assigned | Reuse; candidate source for base-family avatar |
| Starless Monk Ascendant | Recurring guardian | Assigned | Reuse; candidate source for base-family avatar |
| Nightveil Sentinel Ascendant | Recurring guardian | Assigned | Reuse; candidate source for base-family avatar |
| Umbral Reaver Ascendant | Recurring guardian | Assigned | Reuse; candidate source for base-family avatar |
| The Gloaming Judge | Floor 6 keeper | Assigned | Preserve avatar; inspect source for scene-portrait adaptation |
| Widow of the Waning Moon | Floor 7 keeper | Assigned | Preserve avatar; inspect source for scene-portrait adaptation |
| The Candlewright | Floor 8 keeper | Assigned | Preserve avatar; inspect source for scene-portrait adaptation |
| Herald of the Last Dusk | Floor 9 keeper | Assigned | Preserve avatar; inspect source for scene-portrait adaptation |
| Sovereign Echo of the Godstorm | Floor 10 keeper / proposed release finale | Assigned | Preserve avatar; prioritize scene-portrait adaptation and finale QA |

Four family adaptations are an art-direction proposal, not evidence that the source images can be cleanly extracted or that identical art across tiers has been approved. Keep readable identities; do not quietly change encounter records to make the art fit.

## 6. Background inventory and wiring

| Asset | Captured gameAsset ID | Current explicit use | Proposed use |
| --- | --- | --- | --- |
| marrow vault 1 | `7EmVo6GH5GL4YtQTDrbDR` | d1_1, d1_2, d1_boss, d1_choice | Main vault/interior coverage where pixels and prose agree |
| marrow vault 2 | `oc0cXiMrcG_6kTUwNWRkn` | d1_3, d1_4 | Secondary vault passages/chambers, subject to visual inspection |
| marrow vault 3 | `IykL5XxwFF14BosCblZj8` | d1_cash | Exit/payoff or other compatible scenes, subject to visual inspection |
| StormCourtyard | `cKHhHoboreP88iH5WjDe7` | None in retained Stormcourt graph | Core Stormcourt setting; evaluate all five floors and finale |

Plan zero new background paintings initially. This is a reuse-first production target, not a finding that one Stormcourt image already satisfies every scene. Recover the four images, inspect them individually, then build the complete dialog-to-background map. Condense unnecessary setting changes and adjust prose to the approved environments. Do not commission one background per floor by default.

Acceptance requires explicit valid coverage for all 68 dialogs. The 61 missing assignments are wiring gaps, not 61 new assets. Review the seven current assignments as well. A failed finale/environment fit may justify one bounded additional asset request; it does not automatically restore the previous multi-background wish list.

Use `gameAsset.image` for this surface, not the unrelated `gameAsset.url` field. Quest listing `image` and dialog `image` are not substitutes for `sceneBackground`; node images can be map pins rather than the dialog scenery.

## 7. Scene characters: define the presentation scope before counting new paintings

Observed: neither retained quest supplies scene characters for its 34 dialogs. That is 68 placement decisions, not proof that 68 separate character paintings are needed. Existing avatar URLs do not automatically create scene-character records.

Recommended baseline:
- Ten keeper scene portraits: one for each keeper listed in section 5, wired at d1_boss through d10_boss.
- Reuse one verified blank scene-character asset for the remaining 58 atmospheric, guardian, choice and cash-out/victory dialogs.
- Set safe quest-level defaults where needed to satisfy current publish validation and prevent fallback surprises; this does not replace explicit dialog assignments.
- Do not add a narrator, quest-giver, sister portraits or additional cast solely to fill the interface.

Reuse method: nine retained keepers already have primary art. Inspect source size, framing, background separation and identity, then adapt suitable originals as transparent busts. The First Dark source should feed both the missing avatar and its keeper portrait. A cropped square image with its old background left attached is not an accepted scene-character conversion. A too-small source must not be silently upscaled and called complete; use a source-guided redraw only where justified.

Existing blank candidates in the older catalog: `Q-_3WA5kibe_8gI2CgTKl` (Blank Character) and `1YXbXYW2wz3GETVMb6DT6` (Blank Scene Character). Verify the chosen record's current type, image and actual blank output before wiring. Do not create another blank by default and do not treat a catalog name as a valid live reference.

Optional expanded scope: add eight recurring-guardian scene portraits, four per tower. Then 50 pre-battle dialogs can show enemies and 18 other dialogs can use the blank. This is an optional eight-output increase, not the earlier four-portrait estimate for both towers together.

## 8. Exact inventory versus proposed production allocation

| Work category | Confirmed state | Recommended allocation before optional work |
| --- | --- | --- |
| Quest listing images | 2 assigned | Reuse both; no replacement planned |
| Primary AI avatars | 13 assigned / 5 default | Complete five assignments; reuse/adapt family art where approved |
| Scene backgrounds | 4 existing records | Reuse four; zero new paintings planned pending visual fit |
| Dialog background wiring | 7 configured / 61 missing | Review all 68, fill the 61 gaps |
| Keeper scene portraits | 0 wired | Prepare/register/adapt ten, not ten automatically new paintings |
| Other scene-character placements | 0 wired | Reuse one verified blank for 58 dialogs in the baseline |
| Chest icon | Captured chest uses default image | One conditional icon assignment if chest is retained; reuse existing suitable chest art first |
| Keystone art | Excluded by direction | Zero |
| Shared jutsu icons / effect art | Captured kits include default icons; distinct retained-set visual census not closed | Deduplicate by ID and check actual player-visible surfaces before allocating new work |
| Overworld pins / 3D / new animation set | No new requirement established | No new production budget; verify any existing references required by retained kits |

The proposed character-output workload is five avatar completions plus ten keeper portrait outputs, with one existing blank reused. These are 15 delivery/assignment tasks, NOT a verified requirement for 15 newly painted images. A retained chest adds one conditional icon task. New painting count remains unresolved until originals are inspected; conversion viability must not be promised from URLs alone.

A complete visual ledger must also cover the retained unique jutsu images, animation/SFX references and any client use of avatarLight. The earlier total omitted these questions. Do not silently declare them complete, but do not commission a new event-wide jutsu/VFX set either. Shared-pool changes affect other content and need a separately bounded approval. Reuse valid library assets first.

Production requirements remain spec-driven: AI avatars square; backgrounds 3:2; scene-character bust/full framing according to the current spec; correct transparency, resolution, byte budget and fresh filenames for corrected assets. Use the reference selector, inspect individual references, generate one candidate at a time, run raw QC and processing, inspect the in-scene composite, run art preflight, then obtain dauntless acceptance. Record provenance, filenames, dimensions, bytes and accepted use per output.

## 9. Content changes required by the cut

### Marrow Vaults

Preserve the elder-sister vault arc, four recurring guardians, five keepers and cash-out choices. Remove the Eclipse Keystone reward entry and every player-facing promise to obtain or use it. Review quest description, successDescription, d5_victory, win text and any external event references. Explain progression to Stormcourt without an item key. Complete all 34 scene assignments.

### Stormcourt

Preserve the ascendant guardians and five keepers. Remove the Aegis Keystone entry and promises. Rewrite quest description, successDescription, d10_victory and win text so Sovereign Echo is the end of this release. Remove the instruction/promise to enter Dawnless Crown. Integrate only the essential conclusion of the stolen-bloodline/machine arc; do not carry over five more bosses or their art requirements. Correct any language implying one unbroken ten-floor reward bank if the two quest runs actually settle rewards separately. Complete all 34 scene assignments.

### Dawnless and related references

The excluded root is `VjT93rkmWlWlrdG6Pp46e`. Inventory inbound quest grants, prerequisites, event hub/menu links, descriptions and old pending manifests that could restore the three-pyramid version. Preserve source records and captures. Prepare an operator-approved retirement/availability step rather than destructive deletion. An existing hidden flag is not proof that no active player or grant path can reach the record.

Do not delete the five excluded AIs, shared jutsu, or the Suture Priest artwork without an independently verified dependency check and explicit authorization. Bank reusable art, but do not force a mismatched portrait into another keeper to consume every available file.

## 10. Progression and failure semantics: required design/QA decision

E1 routes both voluntary cash-outs and full clears to each quest's shared win_quest node. Stormcourt's prerequisite is Marrow's quest ID. At the inspected source pin, isAvailableUserQuests checks a completed prerequisite quest, not which floor was cleared (`app/src/libs/quest.ts`, prerequisiteCheck).

Therefore do not assume the current prerequisite enforces a floor-5 clear. Early cash-out may satisfy ordinary completion. Verify the exact end-to-end behavior before retaining text that claims a full clear is required.

Recommendation: a full Marrow clear unlocks Stormcourt; voluntary cash-out pays the approved exit reward but does not falsely announce a full clear. Fable must identify the smallest source-supported completion/unlock mechanism, without restoring an item key. If this requires another content marker or an engine change, surface the cost before implementation; do not silently invent a third player-facing pyramid or use an unverified gate. Accepting early-cash-out unlocks is a simpler alternative, but requires an explicit direction decision and matching prose.

Likewise verify what 'lose everything' actually means. Zero quest-node rewards on a loss do not prove that earlier ordinary combat gains or AI item drops are revoked. Prefer defining risk as forfeiture of unclaimed tower cash-out rewards; Content Admin must settle any other intended loss policy. Do not introduce inventory clawbacks.

## 11. Chest and reward decisions: open to Content Admin

Structural cleanup and reward balancing are separate. Remove obsolete keystone references as part of the two-pyramid revision; do not replace them with invented rewards while the reward decision is open.

Captured exit schedule (existing data, NOT approved recommendations):

| Exit within each retained quest | Marrow ryo | Marrow chest chance | Stormcourt ryo | Stormcourt chest chance |
| --- | ---: | ---: | ---: | ---: |
| First keeper / 5 wins | 25,000 | 1% of one | 50,000 | 2% of one |
| Second keeper / 10 wins | 50,000 | 2% of one | 100,000 | 4% of one |
| Third keeper / 15 wins | 75,000 | 3% of one | 150,000 | 6% of one |
| Fourth keeper / 20 wins | 100,000 | 4% of one | 200,000 | 8% of one |
| Full clear / 25 wins | 125,000 | 5% of one | 250,000 | 10% of one |

Marrow pays 25 tokens / 10 prestige at every exit; Stormcourt pays 150 tokens / 60 prestige at every exit. The exits are alternative branches, not five rewards that should all be added together. In reward_items, number is percentage chance and quantity is the amount. E2 also includes chest drops in keeper inventories; include those in total expected-value calculations rather than auditing only quest reward fields.

The shared Endless Night Chest, `HLycjzUcVwKZenBWpd0V-`, is currently a consumable with an empty noncombat reward table, default icon and destroyOnUse true. Do not certify its use as a finished reward, and do not leave a destructible empty reward placeholder in the accepted release.

| Open decision | Recommendation | Acceptance requirement |
| --- | --- | --- |
| Chest retained or replaced | Retain one shared chest only if its contents justify it; otherwise use approved direct rewards | Explicit decision before reward manifest |
| Chest contents | Reuse existing relevant non-profession-exclusive materials/consumables, with a modest reliable base and an optional rare bonus | Admin chooses exact IDs, amounts, rarity and probabilities; all references verified |
| Reward cadence | A clearly capped daily paid completion per pyramid; set attempt policy separately | Verify actual counter/delay behavior, not just the string daily |
| Exit incentive | Reward deeper progress with stronger meaningful payouts and a clear full-clear premium | Approve ryo/tokens/prestige and chest chances for all ten exits |
| Flat tokens/prestige | Prefer depth scaling rather than identical full token/prestige value at first exit | Admin confirms final curve |
| AI chest drops | Prefer one clear cash-out reward channel, or explicitly budget and explain retained keeper drops | No duplicate/unbudgeted reward channel; loss copy matches behavior |
| Removed Dawnless rewards | Do not automatically move its larger payouts into Stormcourt | Any compensation/reallocation is separately approved |
| Existing player chest copies | Decide whether filling the existing item updates old copies intentionally and whether any notice is needed | No silent assumption about previously awarded inventory |

These decisions can stay open during story drafting, asset recovery and art adaptation. They cannot remain open at final reward validation or release acceptance. No numerical recommendations in this table authorize a live edit.

## 12. Combat QA and calibration plan

Static QA for all 18 retained AIs:
- Join each battle opponent to its AI record and aiProfileId; join every rule action/combo to the equipped kit and relevant item.
- Check empty/missing/unreachable kit slots, action targeting, SELF versus opponent actions, distance thresholds versus ranges, cooldowns, AP compatibility, combo fallback and default-rule interference.
- Account for actual level/rank caps, normalized stats, pool multipliers, equipment and passive effects without double-multiplying stored values.
- Review crowd-control/denial uptime, unavoidable openings, kiting behavior and healing windows. Check the complete kit rather than raw HP alone.
- Deduplicate shared content and bound any proposed edit's effect on other quests/events.

Calibration after operator approval:
- Declare representative player loadouts inside the current level-70-to-100 eligibility band, including ordinary and stronger/endgame builds. Record stats, equipment, relevant bloodline/kit and mitigation.
- Exercise all eight guardian archetypes and ten keepers, with special attention to the first Marrow keeper, the transition into Stormcourt, Warden of the Half Eclipse and Sovereign Echo.
- Record damage spikes, fight length, control lockouts, resource pressure, success/failure and counterplay. Repeat outliers before recommending changes.
- Choose exact balance targets with the user/Content Admin; do not invent a win-rate target or tune only against a heavily mitigated tank.

The removed Endless Night's Shadow multiplier/Heavy Armor calibration is not a retained-release blocker. Do not carry its x6/x9.6 warning into the two-pyramid status card as if Sovereign Echo were the same AI. Retained bosses still require their own QA.

## 13. Work packages, order, ownership and gates

All execution packages below remain PLANNED until the user approves the plan and inputs are reproducible. Captures are available; revised implementation and acceptance are not complete.

| Step | Work | Owner | Depends on | Required output / completion gate |
| --- | --- | --- | --- | --- |
| 1 | Reproduce retained inventory; recover originals; audit shared jutsu/effect visual dependencies | Fable evidence extraction + ChatGPT audit/art review | E1-E3 | ID-deduplicated roster; complete node ledger; original-file metadata/provenance; unresolved image/reference list |
| 2 | Set retained battle count, finale, unlock/cash-out policy and portrait scope | dauntless with ChatGPT | This plan | Explicit decisions; no art or engine policy settled accidentally |
| 3 | Pilot existing-art reuse | ChatGPT art support + dauntless acceptance | Recovered files and art direction | One retained-keeper scene adaptation and one base-family avatar reuse example; render/QC proves the reuse route |
| 4 | Draft two-pyramid story and retirement/reference changes | ChatGPT content collaboration; Fable implementation later | Step 2 | Revised descriptions/ending, no keystone promises, no third-pyramid continuation, preserved node IDs where possible |
| 5 | Produce accepted visual outputs and full wiring map | ChatGPT art support | Steps 1-3 | Five avatar completions; ten keeper portrait outputs in proposed baseline; verified blank; all 68 dialog mappings; each asset accepted/QC'd |
| 6 | Review retained combat and progression semantics | ChatGPT independent audit; Fable source/fixture support | Step 1 and scope decisions | Rule/kit report, cap/pool review, cash-out/full-clear and loss semantics, declared calibration plan |
| 7 | Set chest/reward/repeatability specification | Content Admin; dauntless final authority | Current reward audit | Exact approved reward table, chest behavior, cadence/limits and all drop channels |
| 8 | Author correction manifests and operator plan | Fable | Approved content, accepted art, resolved reward/balance decisions | Factory/validator-generated payloads; narrow field scope; capture-before/after; rollback/preimage and active-player handling |
| 9 | Independently review exact payload SHA and run offline gates | ChatGPT review; Fable fixes | Step 8 | Zero unresolved blocker; manifest validation; reference closure; art preflight; no accidental kit/reward/visibility changes |
| 10 | Operator applies approved changes and commits readback | dauntless | Step 9 | Per-record success plus full persisted post-write captures; source-to-live diff; no echo-only certification |
| 11 | Operator-approved combat calibration and mobile acceptance; correction loop if needed | dauntless / testers; ChatGPT audits evidence | Updated captured content | Both full runs, exits, failure outcomes, unlock policy, repeat limits and actual scene rendering meet decisions |
| 12 | Final acceptance, availability/publishing and durable closeout | dauntless following Content Admin go-ahead | All previous gates | Two-pyramid player-facing release verified; Dawnless excluded; accepted release snapshot and post-publication smoke evidence |

Parallel work: after inventory/scope, story drafting, reuse pilots, static combat QA and admin reward deliberation may proceed independently. A pending chest decision need not stop art work. No production write occurs until its own decision and validation gates are satisfied.

After plan acceptance, register the workstream through the existing `state/workstreams/<slug>/roadmap.json` mechanism, point tasks at this document and the committed evidence, run content_workstream.py validate/render, and create the normal `state/prompt_<task>.md` implementation brief. Do not hand-author generated ROADMAP.md or mark unvalidated packets READY. This planning commit intentionally does not claim that the workstream initializer or generated projections have been run.

## 14. Acceptance test matrix

| Area | Required checks |
| --- | --- |
| Graph | Exactly the approved two roots and battle count; one intended start each; all pointers resolve; every battle gated; all 50 configured failure routes inspected; no accidental activation or skipped floor |
| Exit paths | All eight voluntary cash-out paths and two full-clear paths; rewards paid only on the selected route and not twice; correct completion descriptions |
| Failure | Lose, flee, draw, abandon and reload behavior as supported; no stray reward-bearing path; wording matches retained combat gains/drop behavior |
| Unlocks | New eligible player, below-level player, early Marrow cash-out, full Marrow clear and repeat attempts; intended Stormcourt eligibility; no unintended Dawnless entry/grant |
| Visuals | Two listing images; 18 non-default accepted primary avatars; 68 valid dialog backgrounds; 68 explicit portrait/blank choices; no stretch, clipped heads, visible cutout backgrounds or unresolved references |
| Shared visual dependencies | Player-visible jutsu icons/effect references accounted for; every deferred cosmetic gap explicit and accepted, not hidden by a total |
| Economy | Ten approved exit payouts; chest expectation and all AI drops included; actual daily/attempt limits proven; no default/empty reward placeholder |
| Combat | Declared-loadout evidence; retained final boss and tier transitions calibrated; no empty kit, wrong self-target or unexplained difficulty spike |
| Mobile | Correct Forge version for any execution, clear run/result status; real quest scenes on the operator/player viewport; no reliance on square asset-editor previews |
| Data safety | Fresh preimages; preserved IDs/unaffected fields; active-run migration handling; recoverable retirement; stale contradictory manifests excluded; independent post-write diffs |
| Publishing | Last captured hidden flags reconciled with actual intended availability; separate explicit operator decision; two-pyramid post-publication smoke |

Source/server fixture tests and live operator tests are different evidence. A graph inventory does not stand in for playtesting; art-field presence does not stand in for image QC; success status does not stand in for a full readback.

## 15. Release gate and next decision

The release is ready only when the approved two-pyramid scope is actually implemented, its references and reward rules are valid, the agreed visual coverage is accepted and wired, combat/progression tests pass, and the operator accepts the readback and player-facing availability.

Recommended next approval package: keep the existing 50 battles and ten keepers; finish at Sovereign Echo; attempt reuse of the four backgrounds; complete the five missing avatar assignments; use ten adapted keeper portraits plus a shared blank; leave chest/reward values with Content Admin. The unlock/full-clear policy and viability of image reuse must remain visible rather than being assumed.

No new game request, mutation manifest, live change or generated artwork is authorized by this document alone.
