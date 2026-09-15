# Godstorm: two-pyramid release plan

**Date:** 2026-09-15  
**Status:** PLANNING ONLY — not an implementation contract, execution manifest, balance approval, or publication authorization.  
**Evidence baseline:** `perseverance484/tnr-tools`, `main` at `6e09b15bb6f3d1c90ba416d14211b533f5b4a367`.  
**Planning owner:** ChatGPT, Release Auditor lead with Content Designer and Art Master review responsibilities.  
**Decision owner:** dauntless / Content Admin.  
**Future implementation owner:** Claude Code / Fable, only after a separately approved implementation brief.

## 1. Authority, scope, and readiness

### Approved direction

Retain **The Marrow Vaults** and **The Stormcourt**. Cut **Dawnless Crown** from this release. Maximize reuse of existing art and content. Keystones are not required: remove obsolete requirements, promises, and reward references; do not create replacement keystones. Chest contents and all reward values remain open Content Admin decisions.

This approval does not authorize image generation, processing, implementation, a game read, a game write, or publication in this session. The only changes authorized here are repository planning documents through the normal ChatGPT branch / pull-request workflow.

### Evidence labels

- **VERIFIED:** present in the pinned repository files and captured record bodies. This is capture-time state, not a claim about the game's current state.
- **PROPOSAL:** recommended future work or design; requires the indicated owner to approve it.
- **OPEN:** a decision or fact not established by the available evidence.
- **GATE:** an acceptance condition that must be demonstrated before release. A gate below is not a claim that the corresponding test ran.

### Readiness assessment

**VERIFIED:** Both retained quest graphs, all 18 retained enemy records, and their associated combat profiles exist in the captures. The release is not starting from an empty content set. Two quest listing images and 13 non-default primary enemy avatars are already assigned. Marrow has seven dialog background assignments backed by three captured background records.

**NOT RELEASE-READY:** The captured quests still describe a three-pyramid, keystone-based progression. Two item references return null. The shared chest has an empty opener table. Early cash-outs and full clears converge on the same quest win node. Scene character arrays are empty throughout the retained graphs. Balance and runtime behavior have not been established by these captures.

There is no defensible single completion percentage: a populated record, a non-default image URL, an approved visual asset, and a successfully tested player path are different completion states. Release readiness is gated, not an average of those states.

## 2. Evidence register and recount method

All links in this section are repository-relative. Resolve them at the baseline SHA above, not at an unspecified future `main`.

| Key | Source | What it establishes |
|---|---|---|
| Q | [Quest capture](../harvests/inbox/tnr_results_1789401726302.json) | Three `quests.get` bodies, including the two retained graphs and the cut Crown graph. Capture file timestamp `2026-09-14T16:02:06.302Z`. |
| A | [AI, item, and background capture](../harvests/inbox/tnr_results_1789402842027.json) | 23 `profile.getAi` bodies, three item lookups, and three background-schema records. Timestamp `2026-09-14T16:20:42.026Z`. |
| P | [Combat-profile and item capture](../harvests/inbox/tnr_results_1789403623148.json) | 23 combat-profile captures and one additional item lookup. Timestamp `2026-09-14T16:33:43.148Z`. This is not a scene-asset catalog. |
| G | [Development workflow](../docs/DEVELOPMENT_WORKFLOW.md), [agent roles](../docs/agents/README.md), [rulings](../docs/RULINGS.md), [content workflow](../docs/workflows/CONTENT_WORKSTREAM.md) | Role split, approved brief and frozen-SHA review, source ownership, and live-game boundaries. |
| V | [Art skill](../skills/producing-tnr-art/SKILL.md), [produced-art ledger](art_produced.md), [art backlog](art_backlog.md) | Processing and QC workflow. The inspected produced-art ledger does not establish a Godstorm source-art delivery inventory. |

The three files report `DONE` / `success`, with full persisted captures. Their journal `entries` arrays are empty and `checks` is null. These are evidence captures, not proof of a passed gameplay or balance test. Count bodies under `captures` once; repeated log summaries are not additional entities.

**Recount procedure used for this plan:** select the two retained quest IDs in Q; enumerate `data.content.objectives`; classify by `task`; read each battle's `opponentAIs`; deduplicate by AI ID; join those IDs to A's `data.userId`; join each `aiProfileId` to P; deduplicate equipped jutsu by `jutsuId`; inspect quest/node image fields separately from scene background IDs and character arrays; resolve referenced reward items and background IDs against A. Do not count the cut quest's enemies or repeated equipment copies as new retained assets.

The counts below are a direct record/graph recount, not inherited infographic totals. This session used connector-based inspection; it did **not** run repository session scripts, `shotlist.py`, manifest validators, art preflight, a local graph validator, a simulator, or a live traversal. A reproducible automated recount from the same pinned files is required in the future implementation handoff. Do not label this document a machine-validated graph report.

### Exact quest identities

| Disposition | Quest ID | Captured name | Captured prerequisite |
|---|---|---|---|
| RETAIN | `2yvE9PUQqlD8lbYNfgX-b` | The Tower of Endless Night: The Marrow Vaults | null |
| RETAIN | `OSADdXqostbyVliCxWk6k` | The Tower of Endless Night: The Stormcourt | `2yvE9PUQqlD8lbYNfgX-b` |
| CUT from release | `VjT93rkmWlWlrdG6Pp46e` | The Tower of Endless Night: Dawnless Crown | `OSADdXqostbyVliCxWk6k` |

Both retained quests are captured as `hidden:true`, rank S, type `battlepyramid`, required level 70 and maximum level 100, with consecutive objectives enabled. Existing records must not be described as already published merely because prior conversation called them live. The captures do not establish present-day visibility.

### Recounted graph totals

| Graph measure | Marrow, floors 1–5 | Stormcourt, floors 6–10 | Retained total |
|---|---:|---:|---:|
| Objectives | 61 | 61 | 122 |
| Battle nodes (`start_battle`) | 25 | 25 | 50 |
| Regular-enemy encounters | 20 | 20 | 40 |
| Boss encounters | 5 | 5 | 10 |
| Dialog nodes | 34 | 34 | 68 |
| Of which pre-fight dialogs | 25 | 25 | 50 |
| Of which continue/cash-out choices | 4 | 4 | 8 |
| Of which cash-out dialogs | 4 | 4 | 8 |
| Of which full-clear dialogs | 1 | 1 | 2 |
| Fail terminals | 1 | 1 | 2 |
| Win terminals | 1 | 1 | 2 |
| Unique enemy IDs | 9 | 9 | 18 |
| Associated combat profiles | 9 | 9 | 18 |

For floor `f`, the recurring chain is `d<f>_1 → b<f>_1 → d<f>_2 → b<f>_2 → d<f>_3 → b<f>_3 → d<f>_4 → b<f>_4 → d<f>_boss → b<f>_boss`. Floors 1–4 and 6–9 then offer `d<f>_choice`, either advancing or going through `d<f>_cash` to `win`. Floor 5 and floor 10 instead lead to `d5_victory` / `d10_victory`, then `win`. Battle failure leads to `fall`.

The retained battle nodes specify one AI opponent, a win completion outcome, `opponent_scaled_to_user:false`, `keepOriginalPools:false`, and `scaleGains:1`. These field values do not establish the engine's effective pool reset, recovery, or reward behavior; that requires source verification and tests.

## 3. Completed versus remaining, by pyramid

### Marrow Vaults

**Completed in captured records:** Five floors and 25 encounters are authored; the four recurring enemies and five bosses exist; nine associated profiles exist; a quest image is assigned; four of nine primary enemy avatars are non-default; the first floor's seven dialogs have backgrounds; four cash-out branches, a full-clear branch, and fail/win terminals are authored.

**Remaining:** Resolve five default primary avatars; verify/resolve nine default light-avatar fields; map the 27 unwired dialog backgrounds; decide and wire scene characters; remove both explicit Eclipse Keystone claims, the implicit bone-sigil prize, and the null item reference; make full-clear versus cash-out progression truthful; test cash-out rewards, loss, retries, and unlock behavior; complete balance review and all visual/runtime gates.

**Dependency:** Its completion semantics determine whether Stormcourt's existing prerequisite is acceptable. Do not finalize Stormcourt entry copy before that decision.

### Stormcourt

**Completed in captured records:** Five floors and 25 encounters are authored; all nine enemy records and associated profiles exist; all nine primary avatars are non-default; a quest image is assigned; four cash-out branches, a full-clear branch, and fail/win terminals are authored; the prerequisite points to Marrow.

**Remaining:** Map all 34 dialog backgrounds; decide and wire scene characters; verify/resolve nine light-avatar defaults; remove both Aegis Keystone claims, all retained Crown progression promises, the conductor-sigil prize, and the null item reference; make the Sovereign Echo encounter end the released Tower story; test independent-run rewards and progression; finish balance review and visual/runtime gates.

**Dependency:** The final story resolution must be approved before final scene mapping. Otherwise art and scene work will be attached to an ending that still points to a removed third quest.

## 4. Exact retained roster and avatar coverage

Source: Q battle `opponentAIs`, joined to A by `data.userId`. **Custom** means a non-default URL exists in `avatar`; it does not mean the pixels were inspected or accepted. **Default** means the captured default image token is assigned.

| Pyramid / placement | Enemy | Exact AI ID | Encounter uses | Primary avatar |
|---|---|---|---:|---|
| Marrow regular | Umbral Reaver | `9uDe65Qt90xnT-fM5vJZ7` | 5 | Default |
| Marrow regular | Hollow Lantern | `IG5Mbfi_2lpUTnUU4_XhZ` | 5 | Default |
| Marrow regular | Starless Monk | `qQ6jMh8w6aiyr4pevwDh-` | 5 | Default |
| Marrow regular | Nightveil Sentinel | `YvinZCoMWiz0RY8ZBP5EW` | 5 | Default |
| Floor 1 boss | Warden of the First Dark | `oi4bHe3upEhLkI-ElJuMX` | 1 | Default |
| Floor 2 boss | Keeper of Hushed Hours | `s6LjnqhSW85pIxYRM76Fw` | 1 | Custom |
| Floor 3 boss | The Moth Tyrant | `jGHpkz2pgLu8loti6pZZi` | 1 | Custom |
| Floor 4 boss | Chained Chorister | `QV1PwoQR9JImZL2_fcOsk` | 1 | Custom |
| Floor 5 boss | Warden of the Half Eclipse | `3XMsIV6Yv4jy-uaJAe52f` | 1 | Custom |
| Stormcourt regular | Hollow Lantern Ascendant | `b8PGgZl8zNNr6UdWH9dBv` | 5 | Custom |
| Stormcourt regular | Starless Monk Ascendant | `JU2BgfdcWsBYGeHUgHMi_` | 5 | Custom |
| Stormcourt regular | Nightveil Sentinel Ascendant | `9yLEi0OoYxcIL0a2XYkWk` | 5 | Custom |
| Stormcourt regular | Umbral Reaver Ascendant | `k4qMHSTHHZBVsijP5FJ6E` | 5 | Custom |
| Floor 6 boss | The Gloaming Judge | `axTRSadaZbUepfT40-7cM` | 1 | Custom |
| Floor 7 boss | Widow of the Waning Moon | `HEjtNpXmuU4ShrOOPg8XK` | 1 | Custom |
| Floor 8 boss | The Candlewright | `pln436P8g2ocUBCHavcdb` | 1 | Custom |
| Floor 9 boss | Herald of the Last Dusk | `aL1Gf1JmVaP8iWi2zHJoO` | 1 | Custom |
| Floor 10 boss / proposed release finale | Sovereign Echo of the Godstorm | `i8oFdDcneF7YE-8VpQsu3` | 1 | Custom |

**Coverage:** 13/18 primary avatars are custom and 5/18 default. All 18 `avatarLight` fields are default. The default token is `630cf6e7-c152-4dea-a3ff-821de76d7f5a_default.webp`. Exact assigned primary URLs are preserved in A under the IDs above; no filename or source-art availability is inferred from them.

Marrow regular order rotates across floors: Reaver/Lantern/Monk/Sentinel on floors 1 and 5; Lantern/Monk/Sentinel/Reaver on 2; Monk/Sentinel/Reaver/Lantern on 3; Sentinel/Reaver/Lantern/Monk on 4. Stormcourt uses the analogous four Ascendants: Lantern/Monk/Sentinel/Reaver on 6 and 10, Monk/Sentinel/Reaver/Lantern on 7, Sentinel/Reaver/Lantern/Monk on 8, Reaver/Lantern/Monk/Sentinel on 9.

### Reuse recommendation

**PROPOSAL:** First evaluate each Ascendant's existing portrait as a donor for its base enemy. The four base enemies then require four approved assignments, not necessarily four illustrations. Preserve readable differentiation through existing names, encounter context, and, only if needed, approved derivative crops or color treatment. Do not change the original Ascendant asset in place merely to create a base version.

Warden of the First Dark remains the unmatched primary-avatar gap under that proposal. Search already-owned suitable boss art before commissioning anything. Reusing a Crown-exclusive portrait is permissible only with Content Admin approval that it no longer implies the cut character or encounter. No such donor is established by this plan.

The 18 light-avatar defaults are a client-usage and wiring review, not a request for 18 new portraits. Verify when the client reads that field, whether the primary may safely be reused, and the applicable rendering contract.

### Cut-scope dependency protection

Crown's five exclusive AI IDs are `eQ0ZFD5tnz-3AUuhiMDM1`, `NUAieA1pvwDxPqP6Gug1o`, `PFNdrYN18UhLpoOgmtZPB`, `USswv3kHIdDbTZDv-UkNm`, and `AWldlLlFKOhpeub2JV4Oi`. They are not retained combat requirements. The four Ascendants are shared with Stormcourt and **must not be removed** merely because Crown is cut. Likewise, do not delete shared jutsu, profiles, image files, or the chest by association with the third quest.

**PROPOSAL:** Keep the Crown quest unavailable and exclude it from release entry points and release documentation, preserving its records for possible later reuse. Cutting scope does not require destructive record deletion. A future approved readback must establish its actual visibility and all incoming references before any disposition change.

## 5. Asset inventory: existing, reusable, missing, and unwired

### Recounted inventory matrix

| Surface | Verified existing state | Gap / unresolved state | Recommended treatment |
|---|---|---|---|
| Quest listing images | Two non-empty image URLs, one per retained quest | Pixel quality, correct crop, and URL delivery not tested | Retain unless QC fails; zero assumed new listing illustrations |
| Primary enemy avatars | 13 custom assignments / 18 enemies | Five defaults, all in Marrow | Four counterpart reuse checks, then a donor check for First Dark |
| Light avatars | 18 default fields | Actual client exposure and reuse validity unverified | Field/format review; reuse approved primary where supported |
| Dialog backgrounds | Marrow 7/34 assigned; Stormcourt 0/34 | 61 unwired dialog slots | Reuse/background-map work first, not 61 new backgrounds |
| Existing background records | Three unique records resolved in A | No complete Godstorm/global background catalog | Reuse the three Marrow plates; inventory Stormcourt candidates |
| Other objective backgrounds | All 50 battle fields and four terminal fields empty | Whether these surfaces render/use a background is source-dependent | Verify client contract before requiring art |
| Scene characters | All 122 objective arrays empty; roots also empty | No wired placements; no captured scene-character inventory | Generate a graph-derived placement list; reuse suitable source art or approve intentional blank dialogs |
| Node image fields | Existing generic image token observed in retained dialogs | Generic image usage, literal URL variants, visibility, and suitability require audit | Do not count repeated image slots as unique illustrations |
| Jutsu icons | 13 unique equipped jutsu IDs across 75 assignments; default icons | No non-default icon coverage in these captured equipped records | Existing-icon lookup and shared-record impact review before art or rewiring |
| Chest art | One shared chest record; default image | Suitable existing chest icon not established | Reuse one approved chest icon; new art only if inventory fails |

The 61 unwired dialogs are 27 in Marrow plus 34 in Stormcourt. Across all objectives there are seven non-empty background fields and 115 empty ones. This latter number includes battle and terminal fields and must not be presented as 115 missing scene illustrations.

The 68 dialog nodes include 50 pre-fight opportunities corresponding to the 18 retained enemy identities. These are placement opportunities, not 50 unique characters. Choice/cash-out/ending dialogs may reuse an appropriate retained character or remain empty if approved and consistent with the scene contract. Do not invent a narrator or other new NPC simply to fill an array.

### Exact existing background map

| Record ID | Captured asset name | Current Marrow dialog assignments |
|---|---|---|
| `7EmVo6GH5GL4YtQTDrbDR` | `the_marrow_vaults_the_hollow_descent_floor_background` | `d1_1`, `d1_2`, `d1_boss`, `d1_choice` |
| `oc0cXiMrcG_6kTUwNWRkn` | `the_marrow_vaults_crypt_reliquary_floor_1_background` | `d1_3`, `d1_4` |
| `IykL5XxwFF14BosCblZj8` | `the_marrow_vaults_the_hollow_descent_loot_vault_background` | `d1_cash` |

All three background records have image URLs, type `asset_background`, folder `events`, and null model bodies. A null background model is not evidence that a scene-character model may be omitted.

**PROPOSAL — Marrow:** Reuse descent, reliquary, and loot-vault plates for later-floor dialogs where the described location fits. Build an explicit node-to-asset map after the ending/prose edit, and record any exception. Different floor numbers alone do not justify different paintings.

**PROPOSAL — Stormcourt:** Search existing event/general assets for a readable storm-court or storm-temple environment, then any needed interior/reward/exit variants. A small reusable set is preferable to one background per encounter. The assigned Stormcourt quest image and cut Crown quest image are only possible derivative sources: neither is proven to have suitable dimensions, composition, rights/provenance, or a clean 3:2 crop. Do not stretch a square image to fill a scene.

### Quest and dialog image provenance

Marrow listing image asset token: `Hzww9EQvYURJYKhI50OMAlNnPZ41ev6fCGcFK3hmjX9I8W7d`.

Stormcourt listing image asset token: `Hzww9EQvYURJjkcMeV4XzPI8f1v96qBot0Q3wsUp2nxu7SMb`.

The observed generic dialog token is `Hzww9EQvYURJpIn7vsbKBAOsGCHyl3Sk0mZFrgWPUdjMJ75D`. Marrow uses a CDN URL ending in `.webp`; Stormcourt uses the corresponding literal URL without that suffix. A shared token does not prove both literal URLs serve identical bytes. Audit the actual rendered field and URL behavior in the later authorized visual QA; do not normalize URLs speculatively.

### Jutsu dependency recount

Marrow has 38 equipped-jutsu assignments and Stormcourt 37: 75 total. Deduplication gives 13 IDs, with 12 represented in each pyramid and 11 shared. The 13 IDs are:

```
FeYnH7BBw_usnc1K-TM-J
Nrxc8m9utE9qaD_gWpLgf
wYVY0O5dJ3wmlPzeiasef
taxbZNdm1Q7YL5AxaRssW
Vo8N1luCT0p48y7JzKe84
o-4SCAhJ4LHdCwcBDgJrV
LiVOnYq6qHzjB0XkIIA2e
Cw51Wm_Uy0GiIkiEjlQtn
6UE5jC71Y6nRjobkJ-UTV
3v9c1SHlD2GLPF2HW1_Sc
Pdb2YwvAVQgRBjGYLKzJo
NXOMUTfmkUBnpFYDkfJsD
sokQAE2sk32thwksgDKLv
```

Source selectors: A's retained `data.jutsus[].jutsuId`, `equipped`, and nested `jutsu.image`. Every captured retained jutsu image uses the default token. The nested data also contains shared-pool descriptions explicitly saying balance values await sign-off. Existing equipment is not evidence of accepted tuning.

**PROPOSAL:** Reuse appropriate existing jutsu icons, including canonical counterparts when verified, rather than commission 13 event-specific icons. Before changing a shared jutsu record, identify other consumers. Do not recolor or rebalance a shared record globally solely for this release without approval. If the client does not expose an AI-only icon, Content Admin may approve that specific default as a documented non-blocking exception; do not silently waive all 13.

### New artwork versus processing versus wiring

| Work class | Includes | Does not establish |
|---|---|---|
| Inventory / selection | Find actual source files or captured asset records; prove identity, fit, and permission; assign a donor | That a candidate is already usable |
| New artwork | A genuinely absent or unusable character/background/icon after reuse review | A fixed count inferred from empty fields |
| Processing | Approved crop/key/alpha cleanup/padding/export/compression; format and byte checks; fresh filenames for corrected derivatives | Missing composition, limbs, source resolution, or a new character design |
| Registration / model work | Asset record creation where needed, correct type, applicable structured scene-character model and effects | Automatic equivalence between an AI avatar URL and a scene-character asset |
| Wiring | Exact approved asset IDs / URLs assigned to the proper quest, node, AI, item, or jutsu field | Approval of pixels or runtime rendering |
| QC | Source/spec conformity, dark composite, anatomy/hands, readable silhouettes, actual target-aspect review, field and upload validation | Gameplay or reward approval |

**New-art budget conclusion:** No fixed new-illustration total is justified by these captures. The four base avatars have identified reuse candidates; First Dark, a Stormcourt scene set, suitable scene-character sources, jutsu icons, and chest art require inventory decisions. Their field gaps are verified; global asset absence is not. Commission only the residual gap after a signed reuse matrix.

Future production must read the current `25x_DATA_art_spec.json` and house style, inspect approved visual references, derive the production shot list from the edited quest graph using the existing tool, and follow the art skill's processing/QC pipeline. Supported full-body or bust scene-character framing must follow the current target contract. Do not upscale a small avatar and call it a finished scene character. Do not count background baked into an avatar as reusable transparency.

## 6. Required quest, prose, and progression changes

### Exact removal and rewrite targets

Source: Q's retained `data` fields and `data.content.objectives` selected by node ID. Item resolution source: A.

| Target | Captured issue | Required disposition |
|---|---|---|
| Marrow `description` | Promises Eclipse Keystone and unlocking Stormcourt | Remove item requirement/prize; describe approved completion-based progression |
| Marrow `successDescription` | Says Eclipse Keystone is claimed | Remove claim; make successful cash-out versus full-clear language truthful |
| Marrow `d5_victory.description` | Player takes a marrow-black bone sigil | Remove implicit substitute-keystone prize; make the path open through events, not an inventory token |
| Marrow `d5_victory.reward_items` | References `1VkKByaLQNDjJUEqiNeic` | Remove this unresolved reference in the future patch; do not create an item to satisfy it |
| Stormcourt `description` | Promises Aegis Keystone and Dawnless Crown unlock | Remove both; identify Stormcourt as the released finale |
| Stormcourt `successDescription` | Says Aegis Keystone is claimed | Remove claim and distinguish cash-out from full clear |
| Stormcourt `d10_victory.description` | Conductor sigil, ten-floor winnings, and Crown above | Replace with complete Tower ending; remove sigil and third-pyramid hook; avoid unproven cross-quest bankroll |
| Stormcourt `d10_victory.reward_items` | References `PPlOpN27RkT0Aw-m9Cfg3` | Remove this unresolved reference; no replacement keystone |
| Stormcourt `win.successDescription` | Crown is still turning above the clouds | Remove sequel/unlock promise; make generic successful-exit text truthful |
| Stormcourt `b10_boss` description/success text | Holds the stair; another gold door glows | Change final encounter framing from stairkeeper to the terminal threat |
| Marrow `win` text and both quests' cash-out text | Shared terminal may imply conquest after an early exit | Use neutral cash-out-safe terminal language; reserve conquest for actual final-boss/full-clear path |
| Release entry points, event prose, guides, older plans/infographics | Possible three-pyramid or keystone instructions outside Q | Search and correct before release; exact external inventory remains open |

The captured retained prose contains four explicit Keystone field references: the two quests' descriptions and success descriptions. Crown is explicitly referenced in three retained Stormcourt fields: `description`, `d10_victory.description`, and `win.successDescription`. The bone and conductor sigils are additional semantic removals even where the word Keystone is absent.

Both unresolved item lookups returned `ok:true` with `data:null`, not a populated item. Their intended identity as keystones is an inference from the surrounding quest copy, not a verified item name. Removal is justified by the approved no-keystone scope and the unresolved references; creating replacements is outside scope.

### Progression decision: full clear versus early cash-out

**VERIFIED:** `d1_cash`–`d4_cash` and `d5_victory` converge on Marrow's same `win`. Stormcourt checks Marrow's quest ID as its prerequisite. Stormcourt's own early cash-outs and final victory also converge on one `win`.

**RISK, NOT YET A PROVEN RUNTIME BUG:** If the prerequisite checks generic successful quest completion, an early Marrow cash-out can satisfy it. Current prose promises unlocking after conquering the fifth vault, which would then be false. A second differently named win node alone may not solve a quest-level completion flag.

**PROPOSAL:** Prefer full Marrow clear as the Stormcourt unlock, without any physical key. First verify the current engine's supported completion/progression representation. Use an existing supported full-clear condition if available; retain appropriate reward-bearing cash-outs without allowing them to masquerade as final victory. Do not invent an unsupported flag or disguise a new token as a non-keystone.

**OPEN Content Admin fallback:** If a full-clear distinction requires unjustified engine work, explicitly approve unlock on any successful Marrow cash-out and rewrite all entry copy accordingly. This is a gameplay decision, not a technical default. Do not ship the current contradictory combination while leaving the choice implicit.

### Proposed complete ending in Stormcourt

The Sovereign Echo remains the final released boss. No additional boss, sixth floor in Stormcourt, replacement Crown quest, keystone, or mandatory new ending illustration is proposed.

**Narrative structure proposal:** Marrow breaks the lower blood-extraction mechanism and opens access to the Stormcourt. Stormcourt reveals that the Echo sustains the remaining connection between the stolen blood and bound storm. Defeating it lets the player sever that connection; the Tower's extraction ritual stops; the route out becomes safe; the released two-pyramid journey ends. Existing references to the sisters remain meaningful rather than becoming setup for a deleted resolution.

**Required canon decision:** Content Admin must approve exactly what the ending states about the elder sister, the younger sister, and the god. Do not assert that a character is alive, physically freed, dead, reunited, or restored if the retained/event canon does not support it. Resolving the Tower's machinery must not accidentally declare the entire wider Godstorm event over.

**Proposed replacement prose, subject to that canon decision:**

Marrow `d5_victory`:

> The Warden of the Half Eclipse falls. You break the last feeder beneath its threshold, and the marrow-black channels run dry. The vaults can no longer draw on the elder sister's blood. The sealed stair opens into thunder: the remaining conduit is above, in the Stormcourt. You leave the vaults with this run's winnings, not another key to carry.

Stormcourt final-boss setup / success:

> The Sovereign Echo is not guarding another stair. It is the last living shape of the Tower's extraction ritual. Break it, and the circuit joining the stolen blood to the bound storm can finally be severed.

Stormcourt `d10_victory`:

> The Sovereign Echo breaks apart, exposing the conduits inside its ruined armor. You tear them free. Far below, the marrow-black channels go still; overhead, the storm ceases to answer the Unbroken Thread. The Tower can no longer feed on the elder sister's blood or bind the younger sister's god to its machinery. No higher chamber calls you onward. The gates open onto a clearing sky, and you carry this run's winnings out of the silent Tower. The climb is over.

Neutral shared `win` terminal, if early cash-outs still reach it:

> You leave the Tower safely with the winnings secured on this exit.

The precise wording is a proposal, not approved lore. In final player copy, the explicit design-facing phrase about a key in the Marrow sample may be removed once the no-item transition is clear. Full-clear narration belongs on full-clear-only nodes; neutral shared win text must not claim every successful cash-out ended the ritual.

Review `d6_1`, each retained floor's setup, `d10_boss`, `b10_boss`, `d10_victory`, the root descriptions, and success/failure terminals together. Maintain floor numbering 1–10 unless Content Admin requests a broader renumbering; the reduced release does not itself require rewriting every node ID.

## 7. Chest and reward decisions — deliberately open

### Captured configuration, not approved economy

The shared chest is **Waning Godstorm Chest**, item ID `HLycjzUcVwKZenBWpd0V-`. A captures a default image; a donor-gift placeholder description; an opener effect whose `items` array is empty; `destroyOnUse:true`; `hidden:true`; event-item status; and tradability enabled. The same chest is present in the retained bosses' item-drop data. Both full-clear quest dialogs also reference it.

The two null item IDs identified above occur beside chest entries in the final-victory reward arrays. Captured reward entries contain both `number` and `quantity`. Do not interpret `number` as chest count, a percentage, or a guarantee without checking the actual reward contract. Likewise, the captured boss `dropChance:1` must not be called 1% or 100% without verifying its units.

The extra item lookup in P is reference evidence only. It does not approve that item as chest content or prove it is equipped on a retained enemy. No chest contents or payout values are selected in this plan.

### Decision register

| Decision | Owner | Recommendation and rationale |
|---|---|---|
| Chest contents, quantities, weights, guarantees, and exclusions | Content Admin | Prefer an already-supported, bounded reward set. Review expected value and outliers before populating the currently empty opener. No proposed item list or values are approved here. |
| Cash-out and full-clear payout values | Content Admin | Compare reward per attempt/time and success probability across all ten floors. Later floors should justify additional risk without making the first repeatable cash-out the dominant farm. |
| Chest delivery path | Content Admin, engine verification by Fable | Prefer one clearly defined payout/accounting path. Reconcile boss drops with quest cash-outs so rewards cannot be duplicated or contradict loss rules. |
| Loss policy | Content Admin | Keep the promised loss-of-unbanked-winnings rule only if all relevant reward channels implement it. Otherwise revise the promise explicitly. |
| Trade, stack, level requirement, battle-use and opener policy | Content Admin | Match the intended event economy and avoid a consume-on-use empty or invalid chest. Test configured behavior rather than assume individual flags combine correctly. |
| Retry and repeatability | Content Admin | Review the captured mismatch: Marrow `retryDelay:none`, Stormcourt `retryDelay:daily`; both have `attemptDelay:none` and max-attempt/max-completion fields of 100. Choose deliberate access and farming policy, not inherited defaults. |
| Donor-credit description | Content Admin | Replace placeholder flavor with event-appropriate copy, retaining credit only if intentional. |

**Critical QA dependency:** Each retained boss has a chest item-drop entry independently of quest final rewards. If a boss drop is granted immediately and persists through a later loss, the statement that losing yields nothing may be false. That behavior must be established; the capture alone does not prove either escrow or a bug. Audit battle money, experience, and other reward channels as well, not only chest items.

## 8. Structural QA and balance review

### Structural and reference QA

| Test group | Required evidence |
|---|---|
| Graph identity and scope | Recount 61 nodes per retained quest; unique node IDs; exactly the 50 intended opponent references; no accidental inclusion of Crown-exclusive encounters. Explain every intentional node-count change. |
| Reachability and termination | Starting node reaches each intended floor; every choice destination exists; all battle failures reach a valid fail terminal; cash-outs terminate; both full clears terminate; no dead ends, unintended cycles, or implicit Crown continuation. |
| Progression | Demonstrate Marrow early cash-out, full clear, loss, repeat clear, and already-completed-account behavior against Stormcourt entry. Include the approved full-clear or generic-success decision and actual engine evidence. |
| Reward references | No unresolved item IDs; no replacement keystones; valid opener contents after Admin decision; schema-correct reward units; all referenced reward records resolve. |
| Reward accounting | Cash-out pays once; full-clear pays once; retries/refresh/reconnect cannot duplicate; loss after a boss matches policy; boss drops and quest rewards do not bypass escrow or double-count. |
| Battle state | Verify `keepOriginalPools`, effective health/chakra/stamina initialization and carryover, healing between fights, cooldown persistence, death/flee/disconnect outcomes, and re-entry. |
| Profile/equipment binding | Every retained AI uses its intended profile; each rule's selected jutsu is equipped and legal; movement and fallback remain usable; default rules do not unintentionally override the authored behavior. |
| Scene references | Every approved background and character ID resolves; character models satisfy current schema; no unrelated donor identity leaks through a reused asset; intentional blanks are documented. |
| Rendering | Quest image, generic dialog image, scene background, scene character, primary/light avatar, jutsu icon, and chest icon tested in the client surfaces that actually consume them. Check actual target aspect and small/mobile readability. |
| Text and cut-scope sweep | No Eclipse/Aegis Keystone promises, implicit prize-sigil gates, Crown unlock instructions, floors 11–15 release promises, or false conquest messages on early exits. Retain shared Ascendants. |
| Publication and rollback | Correct visibility/entry points, no premature Crown exposure, before/after evidence for authorized writes, and tested restoration procedures for changed records. |

The former three-pyramid infographics and guides are derivative surfaces. They must be updated only from the reduced graph and signed asset matrix; they are not authoritative inputs to this recount.

### Balance observations from captures

**VERIFIED:** The regular Marrow enemies have captured health/chakra/stamina pools of 9,100. Marrow boss pools rise through 9,300, 9,500, 9,700, 9,900, and 10,100. The four Ascendants have 10,100, followed by Stormcourt boss pools of 10,300 through 11,100 in steps of 200. These are record values, not measured effective battle pools. For example, Umbral Reaver is level 90 with stats and pools multipliers of 2. The quests admit levels 70–100 and their opponents are not scaled to the user.

**Implications to test, not conclusions:** A smooth pool ladder does not establish a smooth difficulty ladder. Effective stats, multipliers, jutsu costs, control effects, priority rules, player healing, and the cumulative length of 25 fights can dominate. The Ascendants repeat five times each; different portraits and higher pools alone may not create distinct tactical progression.

P establishes authored combat profiles, including jutsu selection, combos, range conditions, movement, fallback behavior, and default rules. Check whether earlier conditions repeatedly win priority and starve later combos or defensive/self-buff actions. A configured rule is not proof that it executes.

### Proposed balance test matrix and acceptance method

Use representative legal player builds at levels 70, 85, and 100, spanning Ninjutsu, Genjutsu, Taijutsu, and Bukijutsu where the content is intended to support them. Include baseline-access equipment as well as a strong build; do not certify a level-70 entry point using only a fully optimized level-100 account. Content Admin chooses the intended audience and acceptable difficulty, clear rate, run duration, resource attrition, and reward-efficiency bounds before tuning.

For each archetype, compare entry, floor-boss, and late-run pressure; trace health/chakra/stamina, turns, damage/control patterns, rule selection, recovery opportunities, cash-out choices, and failure causes. Specifically compare Marrow's final boss to Stormcourt's opening Ascendants and the floor-9 boss to the Sovereign Echo. Test repeated runs for the approved retry rules. Report distributions and representative failure traces rather than a single lucky clear.

Review existing jutsu effect descriptions marked placeholder or pending sign-off, zero-cost versus nonzero-cost skills, range/cooldown interactions, buffs/debuffs, and any shared-pool consumer impact. Prefer a small scoped tuning diff after diagnosis; do not redesign 18 working enemies merely because a balance pass is needed.

No numeric combat tuning, loot table, reward value, target win rate, or release difficulty is ratified here. No live balance run is requested in this planning session.

## 9. Ordered completion plan, dependencies, and owners

Owner labels denote responsibility, not authorization to start. ChatGPT leads design and independent release review. Fable leads future implementation and reproducible technical validation. Art Master responsibility covers selection, processing, and visual evidence. Content Admin approves content, economy, balance, and final art. dauntless is the live operator.

| Order / ID | Work package | Owner | Dependencies | Done when |
|---|---|---|---|---|
| 1 / GS-01 | Approve the reduced release contract and record open decisions | Content Admin; ChatGPT records | This plan | Two retained IDs, Crown exclusion, no keystones, and non-authorized future work are explicit |
| 2 / GS-02 | Verify progression/reward engine semantics from canonical source; reproduce the capture recount | Fable after approved brief; ChatGPT reviews | GS-01 | Evidence for completion flags, reward units, boss-drop accounting, pool behavior, and exact graph/asset counts |
| 3 / GS-03 | Decide full-clear unlock, retry policy, loss/accounting policy, ending canon, and economy | Content Admin | GS-02 for mechanics-dependent choices | Decision log has owners and approvals; chest contents and values are selected by Admin, not inferred |
| 4 / GS-04 | Freeze the retained prose/graph edit specification | ChatGPT Content Designer; Content Admin approves | GS-03 | Exact fields/nodes, complete Stormcourt ending, neutral cash-out terminals, no obsolete keys/Crown promises |
| 5 / GS-05 | Build reuse inventory and graph-derived visual assignment plan | Art Master + Fable tooling; Content Admin accepts | GS-04; existing captures may be inventoried earlier | Each logical requirement maps to approved existing art, a processing task, an explicit blank exception, or a justified residual new-art request |
| 6 / GS-06 | Produce only residual assets and process/register approved derivatives | Art owner; Fable for asset/model records | GS-05 plus separate production authorization | Correct filenames, source provenance, dimensions/bytes, dark-composite/anatomy QC, required models, and acceptance evidence |
| 7 / GS-07 | Implement content-only patches and wiring on a Fable branch | Fable | Approved implementation brief; GS-04/05; relevant GS-06 deliveries | Small scoped diffs for retained quests, approved AI/icon references, chest decisions, and Crown exclusion; no unrelated global asset changes |
| 8 / GS-08 | Run offline structural/reference checks and balance/source review | Fable; independent ChatGPT audit | GS-07 | All feasible automated gates pass; failures fixed; open runtime claims clearly listed |
| 9 / GS-09 | Return frozen-SHA review package | Fable → dauntless → ChatGPT | GS-08 | Exact SHA, changed-file list, tests, deviations, asset ledger, decisions, manifest review, and rollback plan |
| 10 / GS-10 | Separately authorize and perform controlled live verification | dauntless operates; Content Admin authorizes; ChatGPT reviews evidence | Approved review and explicit game-operation authorization | Fresh captures/readbacks and approved tests establish actual state and behavior; any mutations separately reviewed |
| 11 / GS-11 | Final content/balance/art sign-off and publication decision | Content Admin / dauntless | All release gates below | Approved two-pyramid release, correct entry points, Crown unavailable, complete Stormcourt ending |
| 12 / GS-12 | Reconcile evidence and derivative release materials | Fable for writers; ChatGPT for review | GS-10/11 outcomes | Repository state regenerated through approved writers; guides and counts match delivered content; unresolved exceptions remain explicit |

**Parallelism:** Asset-source inventory and technical semantics review can proceed independently after an approved brief. Final artwork selection/wiring depends on the frozen ending and scene map. Numerical balance and economy decisions can proceed in parallel with visual processing, but release requires both. Do not let art work conceal unresolved progression or reward defects.

The concise implementation brief required by `RUL-2026-09-08-006` should be created only after the necessary decisions are made. It should reference this plan rather than copying it as an unreviewed manifest. This planning document does not start Fable, enqueue jobs, or grant permission to make game requests.

## 10. Release gates and present status

| Gate | Required sign-off / proof | Present assessment |
|---|---|---|
| G0 Scope | Approved retained IDs, Crown cut, no replacement keystones | Direction approved; future implementation not authorized |
| G1 Narrative and progression | Complete Stormcourt ending; approved full-clear/cash-out semantics; no obsolete progression promises | BLOCKED |
| G2 Reward integrity | Null item refs removed; chest configured by Admin; reward units, loss, boss drops, idempotency, and repeatability verified | BLOCKED |
| G3 Structural integrity | Reproducible graph/ref audit; no dead paths or broken bindings; all cut-scope dependencies protected | Captures reviewed; automated and runtime proof outstanding |
| G4 Visual readiness | Signed reuse matrix; no unapproved exposed defaults; backgrounds/characters wired or explicitly waived; source and render QC | BLOCKED by assignments, inventory, and acceptance evidence |
| G5 Combat readiness | Effective-stat and profile review; representative balance evidence against Admin-approved targets | NOT ESTABLISHED |
| G6 Implementation review | Approved brief, frozen SHA, passing available tests, manifest/rollback review, explicit deviations | NOT STARTED |
| G7 Operational readiness | Separately authorized fresh evidence; correct publication state and entry points; operator approval | NOT AUTHORIZED in this session |

**Release recommendation:** Do not publish based on asset completion alone. The shortest safe path is to close progression and reward semantics, approve the terminal Stormcourt story, reuse the existing visual set aggressively, patch only the resulting gaps, then prove structural, combat, visual, and operational gates in that order.

## 11. Handoff and preservation notes

Session bootstrap reviewed the live repository's `CHATGPT.md`, `state/active-context.md`, `state/status.json`, `docs/00_INDEX.md`, `docs/RULINGS.md`, `docs/DEVELOPMENT_WORKFLOW.md`, and `docs/agents/README.md`, plus the relevant role/workflow and art documents. The active-state projection predates the Godstorm captures; it is not evidence that these records are missing or published.

Governance, verified engine behavior, generated field/asset contracts, captured record state, approved design decisions, and proposals retain their separate authority. This plan does not turn an engine hypothesis into an engine law or a recommendation into a user ruling.

Preserve this document and the approved scope ruling on a `chatgpt/*` branch for normal pull-request review. Do not merge directly to `main`, edit the captured evidence, alter generated operational dashboards by hand, or silently delete Crown/shared records. No image generation, image processing, content implementation, game request, or publication was performed to create this plan.
