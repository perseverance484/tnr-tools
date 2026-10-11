# Ghost Ship: Skyglass Expedition — Six-Ending Quest Graph

**Status:** DIRECTOR-APPROVED STAGE 1 STRUCTURE / dialogue is still draft; not an executable manifest or production approval.  
**Approval:** `RUL-2026-10-10-003` (2026-10-10), approved structural snapshot `7ac886b845b88e76a9fd7206ce0e025d2cfce230`.  
**Source revision:** `perseverance484/tnr-tools@0eb57de20877d266dde666229ae4c68e8fbcf4c0` (verified 2026-10-10).  
**Machine proposal:** `state/ghost_ship_skyglass_graph_patch.json` (same design branch).  
**Predecessor:** `state/ghost_ship_retheme_patch.json` owns all unchanged original objective prose. Its preserve-all-57/keep-edges restriction is explicitly superseded only for this expansion; other operative retheme content stays intact.  
**Lead:** Content Designer / ChatGPT. Director approves structure, narrative and rewards; Fable builds only after a separate technical and content freeze.

## 1. Design intent

Keep the Ghost Ship a self-contained, replayable airborne shinobi expedition. New rooms and decisions are optional where possible, the Oathkeeper-to-Crowned Captain route remains an efficient repeat farm, and the Skyglass Reliquary introduces an exclusive exploration reward path. Crew are **chakra impressions reconstructed by a failing preservation order**, not undead. The final command/mission-nontermination reveal remains with the Crowned Captain.

### Approved foundation preserved

- Existing Gather quest `6Ri-W5TtUrEMWpyYlnf_F` and Hunt quest `HckXVOf-qk6ESU9t5rxLh` retain their respective quest ids and occupation/rank gates.
- All **57 original objective ids** remain. The proposal rewires only **12** existing nodes; the **26** new nodes bring each mirrored quest to **83**. No additional quest record or standalone daily is added.
- Original five endings `w_A, w_B1, w_B2, w_C, w_Co` retain their reward identities, except the previously approved removal of the erroneous `w_Co` fragment-completion roll.
- The secret ending `w_secret` is a mutually exclusive sixth ending. It grants **1 Skyglass Reliquary at 100%**; no boss fragment/Katana drops inside the Reliquary.
- The Oathkeeper correct answer `Time` proceeds directly to `d_helm_oath`. The optional `d_oath_memory` dialog is bypassable; **no extra mandatory farm fight, key or puzzle**.
- Existing 11 Ghost Ship AI identities and the shared-pool migration stay in force. Only **Sealwright** is a new AI proposal, using the pool rather than a bespoke jutsu suite.
- Director reports the two quests currently hidden; October 1 `hidden:false` snapshot is stale for visibility. Require a fresh operator-run capture before any write and preserve hidden state.

## 2. Proposed route map

```text
Ghost Ship appears
├─ Gangplank → Deck Warden + hazards → [NEW: reconstruction at watch]
│                                            └→ MAIN DECK
├─ Hull infiltration → [NEW: Exterior Keel Walk / inspect lift lattice]
│                       → Core Horror → [NEW: Reconstruction Chamber decision]
│                                        ├─ Return to MAIN DECK
│                                        └─ Read hidden impression maintenance plate
│                                            ├─ Wrong seal → archive locks → MAIN DECK
│                                            └─ Quarantine return seal
│                                                → [NEW: Quarantined Archive]
│                                                → [NEW: Sealwright battle]
│                                                → [NEW: Skyglass Reliquary] → w_secret
└─ Oathkeeper parley
    ├─ Wrong answer → Oathkeeper duel → MAIN DECK
    └─ Time → [optional oath history] → HELM GUARD (2 Deck Wardens)
                                     → CROWNED CAPTAIN → w_Co

MAIN DECK (existing)
├─ CHART ROOM → Wayfinder → corrected charts → shore riddle
│               → Sentinel → w_A
├─ HOLD → Arsenal Keeper + hazard → untouched inventory
│         ├─ accessible stores → Deck Warden → w_B1
│         └─ restricted vault → First Blade → w_B2
└─ HELM → 2 Deck Wardens → [optional Command Observation Gallery]
          → THE CAPTAIN → [optional aftermath] → w_C
```

### Player-facing route personalities

| Route | Successful-playthrough combat | Distinction |
| --- | --- | --- |
| Oathbound | Two Deck Wardens (one fight), Crowned Captain (one fight) | Fastest Crown/3% Katana farm; optional Oathkeeper/final-order conversations |
| Hull to secret | Core Horror, Sealwright | Investigation, seal puzzle, exclusive Reliquary; no Captain rewards |
| Hull to main deck | Core Horror, then chosen deck-wing fights | Optional engineering/reconstruction discovery before ordinary endings |
| Gangplank to main deck | Deck Warden + hazards, then chosen deck-wing fights | Direct fighting and visibly rebuilding security |
| Chart/cache | Wayfinder + Sentinel after reaching deck | Navigation, chart puzzle, beach cache |
| Accessible hold | Arsenal Keeper + Seal Charge, then Deck Warden | Safer supplies and repetitive-crew tragedy |
| Restricted vault | Arsenal Keeper + Seal Charge, then First Blade | Stronger vault fight and character-driven reward tension |
| Normal helm | Two Deck Wardens, then Captain | Military command mystery, optional systems gallery and aftermath |

No successful playthrough has to explore every branch; the return-player benefit is seeing different sides of the ship rather than completing a single longer linear corridor.

## 3. New node inventory

The machine proposal includes full new node descriptions, choice text, edge targets, scene symbols, and loss/reset fields. This table is an overview, not duplicate authority.

| ID | Type | Scene symbol | Purpose |
| --- | --- | --- | --- |
| `d_security_reconstruction` | dialog | deck | Gangplank guard regenerates immediately; atmosphere |
| `d_keel_cross` | dialog | exterior_keel | Exposure and branching underkeel traversal |
| `d_keel_seals` | dialog | exterior_keel | Optional inspection of lift/return lattice |
| `d_recon_access` | dialog | lower_hull | Post-Horror split to deck or deeper exploration |
| `d_recon_chamber` | dialog | reconstruction | Crew impressions, ordinary memories and player agency |
| `d_recon_test` | dialog | reconstruction | Hidden three-choice maintenance seal puzzle |
| `d_recon_lockout` | dialog | reconstruction | Wrong choice loses the archive opportunity for this run |
| `d_archive_entry` | dialog | quarantined_archive | Unlisted records and preserved Reliquary |
| `d_archive_records` | dialog | quarantined_archive | Optional containment-failure history, no final-order spoiler |
| `d_sealwright` | dialog | quarantined_archive | Secret custodian confrontation |
| `b_sealwright` | start_battle | quarantined_archive | Only new enemy encounter (AI kit yet to be specified) |
| `r_sealwright` | reset_quest | quarantined_archive | Loss retries Sealwright, not whole expedition |
| `d_reliquary_claim` | dialog | quarantined_archive | Reward tension and explicit one-ending commitment |
| `w_secret` | win_quest | quarantined_archive | Secret sixth ending; guaranteed one Reliquary |
| `d_chart_overlay` | dialog | chart_room | Optional Wayfinder chart-correction discovery |
| `d_wrong1_feedback` | dialog | shore_cache | Visible split-cliff wrong-answer explanation |
| `d_wrong2_feedback` | dialog | shore_cache | Visible reef wrong-answer explanation |
| `d_stores_log` | dialog | hold | Choice to inspect repeated untouched inventories |
| `d_stores_memory` | dialog | hold | Optional Arsenal Keeper shore-leave memory |
| `d_first_blade_answer` | dialog | hold | Optional First Blade personal dialog before duel |
| `d_first_blade_departure` | dialog | hold | Optional personal farewell after duel |
| `d_gallery_threshold` | dialog | helm | Normal Captain path gets optional gallery |
| `d_gallery_record` | dialog | command_gallery | Command architecture and incomplete loss-state evidence |
| `d_c_after` | dialog | command_gallery | Optional post-Captain investigation |
| `d_co_after` | dialog | helm | Optional post-Crowned final order recording |
| `d_oath_memory` | dialog | deck | Optional Oathkeeper history, bypassable on farm |

**Total new nodes:** 23 `dialog`, 1 `start_battle`, 1 `reset_quest`, 1 `win_quest`. The final graph contains **47 dialogs, 13 battles, 15 reset nodes, 2 collection interactions, and 6 endings**, for 83 nodes in each profession quest.

## 4. Original node rewires

All nodes not listed below retain their original edges. Existing characters, profession differences, scene fields, coordinates and reward arrays are inherited from the full source records unless separately approved.

| Existing ID | Reason for route change |
| --- | --- |
| `b_gang` | Show immediate security reconstruction after the gangplank guard |
| `c_climb` | Make the airborne underkeel traversal visible |
| `b_bilge` | Give Core Horror victory an optional reconstruction chamber detour |
| `d_oathpass` | Keep the Crown farm direct; optional Oathkeeper characterization |
| `d_map` | Optional chart history without extra forced battle |
| `d_riddle` | Put visible feedback dialogs before existing reset nodes |
| `b_qm` | Show continuous inventory without adding another encounter |
| `d_vault` | Offer personal dialogue before First Blade fight |
| `d_claim_B2` | Optional post-vault reflection; unchanged ending/rewards |
| `b_helm` | Offer optional gallery investigation only on normal Captain path |
| `d_claim_C` | Optional Captain aftermath without extra reward |
| `d_claim_Co` | Optional Crowned aftermath without slowing repeat farming |

The new Sealwright battle is immediately dialog-gated by `d_sealwright`, has a loss edge to `r_sealwright`, and the reset returns to the in-flow `d_sealwright` dialog. The two wrong shore-riddle answers now show **visible dialog nodes** before falling through to the original `reset_quest` nodes, whose text is not reliably displayed by the quest client.

## 5. Secret route: decision contract

1. Choose **hull infiltration** at arrival; the existing `c_climb` timed traversal and Core Horror fight remain.
2. After Core Horror, choose to follow the damaged impression conduit rather than the deck ladder.
3. Study the Reconstruction Chamber and answer the seal-line question. Correct choice is the **quarantine return line beneath the frames**; two incorrect choices seal the archive until a future run and return the player to the **main deck**. Incorrect choices do **not** fail the entire quest.
4. Enter the Quarantined Archive; optional suppressed reports provide containment-failure history without disclosing the Crowned Captain's final mission truth.
5. Challenge **Sealwright**; on loss, retry from the Sealwright confrontation dialog. Victory unlocks the Reliquary.
6. Take **one Skyglass Reliquary** and **depart immediately** via `w_secret`. No path from the archive to another win node, and no bonus chest before subsequently defeating the Captain.

**Director-approved behavior:** The fixed maintenance puzzle makes the route discoverable and repeatable. Wrong answers block it for that visit (not forever). This adds secret-route risk without a random gate or daily lockout. If repeat farming later feels tedious, the shortest path skips all optional lore and uses only the core puzzle/dialog flow. No persistent discovery flag is claimed.

## 6. Narrative reveal discipline

- **Arrival:** the vessel materializes airborne, without conventional approach.
- **Gangplank:** the defeated watch reconstructs, showing a defensive system that will not stand down.
- **Exterior keel:** the player experiences gravity, clouds below and the Skyglass lift lattice. Not floating islands or unrelated airborne buildings.
- **Core Horror / Reconstruction Chamber:** damaged reconstructions and ordinary human memories, not biological survival.
- **Quarantined Archive / Sealwright:** the first evidence that someone attempted containment and failed to obtain command authorization. Sealwright knows the fault records, **not** the complete mission termination truth.
- **Oathkeeper / Wayfinder / Arsenal Keeper / First Blade:** preserve each character's humanizing reveal from the approved retheme, including decades of charts, untouched supplies and joy at a truly new duel.
- **Normal Captain / optional gallery:** prove the ship treated its destruction as a condition to override. The final mission order remains inaccessible.
- **Crowned Captain:** Crown reconstructs the highest-fidelity command imprint; the mission never received a termination condition, therefore reconstruction continues. Optional post-boss command record does not let the player permanently stop the vessel.

## 7. Rewards and scene assets

| Ending | Role | Reward constraint |
| --- | --- | --- |
| `w_A` | Shore field-cache | Preserve existing Gather/Hunt chest rewards |
| `w_B1` | Accessible stores | Preserve profession-specific chest rewards |
| `w_B2` | First Blade's restricted vault | Preserve vault/chest rewards |
| `w_C` | Normal Captain | Preserve normal helm rewards |
| `w_Co` | Crowned Captain | Preserve oathbound package minus removed completion fragment roll; AI drops 20% Crown fragment and 3% Skyglass Katana independently |
| `w_secret` | Quarantined archive | Guaranteed 1 Skyglass Reliquary; separate internal chest rolls/Filament crafting as approved |

**Existing scene assets reused:** Deck, Lower Hull, Chart Room, Hold, Helm, Shore Cache Site, Oathkeeper portrait, both Captain portraits, and Blank Scene Character.  
**New scenes:** Exterior Keel Walk, Reconstruction Chamber, Quarantined Archive, Command Observation Gallery (all `SCENE_BACKGROUND`, 3:2), plus one Sealwright `SCENE_CHARACTER` portrait (2:3 or 1:1 depending on framing). Sealwright requires a separate 1:1 AI combat avatar.  
**No extra objective map markers or new location coordinates are required in this proposal:** the only `collect_item` nodes remain `c_climb` and `c_dig`, and all new interaction nodes are `dialog` or dialog-gated `start_battle`. All scene refs are symbolic design IDs; a manifest must resolve them to real new/captured records after art approval.

## 8. Structural verification performed

The proposed machine patch was applied in memory to the full captured Gather graph and independently checks:
- **57 preserved + 26 added = 83 nodes**, 12 original rewires.
- Exactly **one root**: `d_intro`.
- **83/83 reachable** through actual success/choice and fail edges.
- Exactly **six reachable end nodes**: `w_A`, `w_B1`, `w_B2`, `w_C`, `w_Co`, `w_secret`.
- DFS over success/choice and failure edges is acyclic; `resetObjectiveId` is intentionally excluded from cycle detection according to engine rules.
- All **13** `start_battle` nodes have an incoming dialog choice.
- All new failures point to an in-flow retry dialog; archived secret descendants terminate only at `w_secret`.
- The oathbound helm segment reaches only `w_Co` and retains exactly **two** combat encounters on its direct path.
- Existing top-level quest schema, source-specific coordinates, reward/equipment records, scene images and updated AI behavior still require a fresh full-record build phase; this is **graph sanity checking**, not Forge `validate.py` or a live-game acceptance test.

## 9. Structural approval and remaining gates

**Approved 2026-10-10:** The director accepted the entire 83-node, six-ending **structural design**, including the 26 additions, 12 original edge rewires, single secret Reliquary ending, wrong-answer quarantine lockout for that run, optional investigation/crew-gallery branches, and direct two-battle Crowned Captain route. The new Sealwright's presence and broad role as quarantine custodian are part of the accepted route. See `RUL-2026-10-10-003`.

**NOT yet approved or frozen:**
- Player-facing descriptions and choice-label wording in the machine patch are **draft prose**. Their IDs, node types, choices/edges and reward endpoint roles are frozen; editorial revision can improve prose without changing routes.
- Sealwright's exact AI kit, AI profile, stats, difficulty, behavior, role tuning and dialogue presentation beyond its approved custodian premise require a dedicated combat/content pass and director approval.
- The Skyglass Katana's exact Legendary weapon cooldown/pool/AP baseline and source-validatable three-effect implementation, and the Crystal's weapon-only 30% Consume engine blocker, need independent technical verification. Rarity/trade questions remain director-owned.
- Scene-asset processing, filenames, art acceptance, and a fresh operator-run capture of the two quests' reported hidden state are required before any manifest or operator-side changes.

**Next step:** develop the Sealwright encounter specification and finish the Stage 2 mechanical/reward gates in the separate reward/combat workstream, then finalize and approve **prose only**, preserving this approved structure. Fable may build a hidden combined manifest **after** the necessary specs and art are frozen. No live-game requests or writes, implementation manifest, publication, or art generation occurred in this design phase.
