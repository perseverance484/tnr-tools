# Art batch: Skyglass event and Crownhold (79 images)

- **Director, 2026-10-25:** "Draft up a design document for the art director to pull each prompt from and use references. Then a short compact hand off for each image in sequence and I hand you back the approved image."
- **Style (director, 2026-10-25):** every image in this batch is PREMIUM PIXEL ART, the same rendering as the Crownhold/crew avatars. Painted references (the Coffer, the charts, the jutsu exemplar) supply subject, materials and colours only; Arakane's avatar supplies the pixel rendering.
- **Protocol:** `docs/workflows/ISOLATED_ART_GENERATION.md`. One image per fresh session, at most two reference images (never a collage), one candidate at a time. The art director returns the RAW image; Claude Code keys, crops, exports and QCs it (`skills/producing-tnr-art`), then swaps the placeholder in game by manifest.
- **Pixel redraws (#36 to #46):** the event icons already live were painted; each is redrawn as pixel art from its own approved image so the whole set matches (director, 2026-10-25).
- **More pixel art (#47 onward):** the six Skyglass item icons inside the Coffer (redraws), then one scene per location the hunts actually depict (14; the wreck is now beached, and each Foundry room gets its own). Each scene lists the nodes that use it so the quests can be repointed when the art lands. Already pixel art and NOT redrawn: every crew avatar, the four scene portraits, the map structure. Left out: the retired Reliquary and old chests, and the retiring Ghost Ship quest icon.
- **Not in this batch:** Arakane (done, `art/crownhold/avatar_crownhold_arakane.webp`); the Sealwright and Oathkeeper scene portraits (already exist). **Deferred:** the Lastlight hit animation (a vertical strip sprite sheet; its placeholder is KGK: Black Fang Lance's).
- **How a session uses this file:** it is given the link to this file and an image number. It reads that image's section, downloads the reference images from the links there, attaches them in the order given, and runs the prompt exactly as written.
- **Live-game requests/writes:** 0.

## Targets (from `25x_DATA_art_spec.json`)

| Target | Canvas to generate | Key | Delivered |
|---|---|---|---|
| ICON | 1024 x 1024 | lime (magenta when the subject is green or the brief says so) | 256 px webp |
| JUTSU_ICON | 1024 x 1024 | none: designed background allowed (RUL-2026-10-14-001) | 256 px webp |
| AI_AVATAR | 1024 x 1024 | magenta | square webp, up to 1024 px |
| SCENE_BACKGROUND | 1536 x 1024 (3:2) | none | 512 x 341 webp |

## Reference files

Every link is pinned to commit `2a79eb90a053c3aa56a70b5d3823e88069104c40`, so it never changes. A fresh session downloads the images named in its section and attaches them.

| Key | Image link |
|---|---|
| coffer | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-skyglass-coffer.webp |
| foundry_chart | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-chart-drowned-foundry.webp |
| lantern | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-skyglass-signal-beacon.webp |
| crown | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_crown.webp |
| arakane | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp |
| arsenal | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/avatar_ghost_ship_arsenal_keeper.webp |
| bbe | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/style_refs/jutsu_icons/bbe/icon_bbe_sapphire_command_v2.webp |
| gallery | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp |
| helm | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_helm.webp |
| captain_portrait | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp |
| treasury_subject | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/raw/subject_sealed_treasury_painted_v1.png |
| redraw_icon-skyglass-coffer.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-skyglass-coffer.webp |
| redraw_icon-tool-pouch-katon.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-tool-pouch-katon.webp |
| redraw_icon-tool-pouch-wave.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-tool-pouch-wave.webp |
| redraw_icon-tool-pouch-ikazuchi.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-tool-pouch-ikazuchi.webp |
| redraw_icon-tool-pouch-stonefall.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-tool-pouch-stonefall.webp |
| redraw_icon-tool-pouch-zephyrfang.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-tool-pouch-zephyrfang.webp |
| redraw_icon-chart-drowned-foundry.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-chart-drowned-foundry.webp |
| redraw_icon-chart-quarantined-archive.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-chart-quarantined-archive.webp |
| redraw_icon-chart-captains-watch.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-chart-captains-watch.webp |
| redraw_icon-skyglass-signal-beacon.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-skyglass-signal-beacon.webp |
| redraw_icon-armory-requisition.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-armory-requisition.webp |
| redraw_icon_ghost_ship_skyglass_crown.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_crown.webp |
| redraw_icon_ghost_ship_skyglass_crown_fragment.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_crown_fragment.webp |
| redraw_icon_ghost_ship_skyglass_crystal.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_crystal.webp |
| redraw_icon_ghost_ship_skyglass_filament.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_filament.webp |
| redraw_icon_ghost_ship_skyglass_katana.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_katana.webp |
| redraw_icon_ghost_ship_skyglass_serum.webp | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_serum.webp |
| scene_helm | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_helm.webp |
| scene_exterior_keel_walk | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_exterior_keel_walk.webp |
| scene_lower_hull | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_lower_hull.webp |
| scene_hold | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_hold.webp |
| scene_reconstruction_chamber | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_reconstruction_chamber.webp |
| scene_quarantined_archive | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_quarantined_archive.webp |
| scene_cache_site | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_cache_site.webp |
| scene_chart_room | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_chart_room.webp |
| scene_deck_b | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_deck_b.webp |
| scene_command_observation_gallery | https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp |

## Sequence

| # | Image | Target | Key | References | Delivery file |
|---|---|---|---|---|---|
| 1 | Sealed Treasury | ICON | lime | treasury_subject, arakane | `icon-sealed-treasury.webp` |
| 2 | Archive Chart Case | ICON | lime | foundry_chart, arakane | `icon-archive-chart-case.webp` |
| 3 | Chart of the Buried Cache | ICON | lime | foundry_chart, arakane | `icon-chart-buried-cache.webp` |
| 4 | Unmarked Cargo | ICON | lime | coffer, arakane | `icon-unmarked-cargo.webp` |
| 5 | Crownbreaker (badge) | ICON | magenta | arakane, crown | `icon-badge-crownbreaker.webp` |
| 6 | Lastlight (jutsu icon) | JUTSU_ICON | none | bbe, lantern | `icon-jutsu-lastlight.webp` |
| 7 | Foundry Warden (AI avatar) | AI_AVATAR | magenta | arsenal | `avatar_skyglass_foundry_warden.webp` |
| 8 | Master of Arms (commander) | AI_AVATAR | magenta | arakane | `avatar_crownhold_master_of_arms.webp` |
| 9 | Replicant Zero (commander) | AI_AVATAR | magenta | arakane | `avatar_crownhold_replicant_zero.webp` |
| 10 | The Grand Marshal (commander) | AI_AVATAR | magenta | arakane | `avatar_crownhold_the_grand_marshal.webp` |
| 11 | Crownhold Proving Proctor | AI_AVATAR | magenta | arakane | `avatar_crownhold_proving_proctor.webp` |
| 12 | Ordnance Quartermaster | AI_AVATAR | magenta | arakane | `avatar_crownhold_ordnance_quartermaster.webp` |
| 13 | Prototype Lancer Unit | AI_AVATAR | magenta | arakane | `avatar_crownhold_prototype_lancer_unit.webp` |
| 14 | Calibration Duelist | AI_AVATAR | magenta | arakane | `avatar_crownhold_calibration_duelist.webp` |
| 15 | Skyglass Archive Keeper | AI_AVATAR | magenta | arakane | `avatar_crownhold_skyglass_archive_keeper.webp` |
| 16 | Impression Containment Warden | AI_AVATAR | magenta | arakane | `avatar_crownhold_impression_containment_warden.webp` |
| 17 | Unstable Echo Subject | AI_AVATAR | magenta | arakane | `avatar_crownhold_unstable_echo_subject.webp` |
| 18 | Failed Reconstruction Prototype | AI_AVATAR | magenta | arakane | `avatar_crownhold_failed_reconstruction_prototype.webp` |
| 19 | Command Signal Adjutant | AI_AVATAR | magenta | arakane | `avatar_crownhold_command_signal_adjutant.webp` |
| 20 | High Command Staff Tactician | AI_AVATAR | magenta | arakane | `avatar_crownhold_high_command_staff_tactician.webp` |
| 21 | Honor Guard Commandant | AI_AVATAR | magenta | arakane | `avatar_crownhold_honor_guard_commandant.webp` |
| 22 | Strategist's Aide-de-Camp | AI_AVATAR | magenta | arakane | `avatar_crownhold_strategists_aide_de_camp.webp` |
| 23 | Sanctum Vanguard | AI_AVATAR | magenta | arakane | `avatar_crownhold_sanctum_vanguard.webp` |
| 24 | Directive Herald | AI_AVATAR | magenta | arakane | `avatar_crownhold_directive_herald.webp` |
| 25 | Last Watch Executor | AI_AVATAR | magenta | arakane | `avatar_crownhold_last_watch_executor.webp` |
| 26 | Order-Bearer of the Sanctum | AI_AVATAR | magenta | arakane | `avatar_crownhold_order_bearer_of_the_sanctum.webp` |
| 27 | Scene: Crownhold gate | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_gate.webp` |
| 28 | Scene: Armory proving hall | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_proving_hall.webp` |
| 29 | Scene: Ordnance store | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_ordnance_store.webp` |
| 30 | Scene: Test gallery | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_test_gallery.webp` |
| 31 | Scene: Armory command terminal | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_armory_terminal.webp` |
| 32 | Scene: Forge wall | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_forge_wall.webp` |
| 33 | Scene: Archive of impressions | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_archive_of_impressions.webp` |
| 34 | Scene: Vat halls | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_vat_halls.webp` |
| 35 | Scene: Research command terminal | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_research_terminal.webp` |
| 36 | Scene: Reconstruction theatre | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_reconstruction_theatre.webp` |
| 37 | Scene: High Command signal room | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_signal_room.webp` |
| 38 | Scene: Planning hall | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_planning_hall.webp` |
| 39 | Scene: Honor guard corridor | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_honor_guard_corridor.webp` |
| 40 | Scene: High Command terminal | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_high_command_terminal.webp` |
| 41 | Scene: The Grand Marshal's office | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_marshals_office.webp` |
| 42 | Scene: Sanctum gate | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_sanctum_gate.webp` |
| 43 | Scene: Sanctum antechamber | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_antechamber.webp` |
| 44 | Scene: Outer ring and terminal | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_outer_ring.webp` |
| 45 | Scene: Throne room | SCENE_BACKGROUND | none | gallery, captain_portrait | `scene_bg_crownhold_throne_room.webp` |
| 46 | The Last Directive (jutsu icon) | JUTSU_ICON | none | bbe, arakane | `icon-jutsu-the-last-directive.webp` |
| 47 | Extermination Order (jutsu icon) | JUTSU_ICON | none | bbe, arakane | `icon-jutsu-extermination-order.webp` |
| 48 | Countermand (item icon) | ICON | lime | arakane | `icon-countermand.webp` |
| 49 | Skyglass Coffer (pixel redraw) | ICON | lime | redraw_icon-skyglass-coffer.webp, arakane | `icon-skyglass-coffer-pixel.webp` |
| 50 | Katon Tool Pouch (pixel redraw) | ICON | lime | redraw_icon-tool-pouch-katon.webp, arakane | `icon-tool-pouch-katon-pixel.webp` |
| 51 | Wave Tool Pouch (pixel redraw) | ICON | lime | redraw_icon-tool-pouch-wave.webp, arakane | `icon-tool-pouch-wave-pixel.webp` |
| 52 | Ikazuchi Tool Pouch (pixel redraw) | ICON | lime | redraw_icon-tool-pouch-ikazuchi.webp, arakane | `icon-tool-pouch-ikazuchi-pixel.webp` |
| 53 | Stonefall Tool Pouch (pixel redraw) | ICON | lime | redraw_icon-tool-pouch-stonefall.webp, arakane | `icon-tool-pouch-stonefall-pixel.webp` |
| 54 | Zephyrfang Tool Pouch (pixel redraw) | ICON | magenta | redraw_icon-tool-pouch-zephyrfang.webp, arakane | `icon-tool-pouch-zephyrfang-pixel.webp` |
| 55 | Chart of the Drowned Foundry (pixel redraw) | ICON | lime | redraw_icon-chart-drowned-foundry.webp, arakane | `icon-chart-drowned-foundry-pixel.webp` |
| 56 | Chart of the Quarantined Archive (pixel redraw) | ICON | lime | redraw_icon-chart-quarantined-archive.webp, arakane | `icon-chart-quarantined-archive-pixel.webp` |
| 57 | Chart of the Captain's Watch (pixel redraw) | ICON | lime | redraw_icon-chart-captains-watch.webp, arakane | `icon-chart-captains-watch-pixel.webp` |
| 58 | Lastlight Lantern (pixel redraw) | ICON | lime | redraw_icon-skyglass-signal-beacon.webp, arakane | `icon-skyglass-signal-beacon-pixel.webp` |
| 59 | Armory Requisition (pixel redraw) | ICON | lime | redraw_icon-armory-requisition.webp, arakane | `icon-armory-requisition-pixel.webp` |
| 60 | Skyglass Crown (pixel redraw) | ICON | lime | redraw_icon_ghost_ship_skyglass_crown.webp, arakane | `icon_ghost_ship_skyglass_crown_pixel.webp` |
| 61 | Skyglass Crown Fragment (pixel redraw) | ICON | lime | redraw_icon_ghost_ship_skyglass_crown_fragment.webp, arakane | `icon_ghost_ship_skyglass_crown_fragment_pixel.webp` |
| 62 | Skyglass Crystal (pixel redraw) | ICON | lime | redraw_icon_ghost_ship_skyglass_crystal.webp, arakane | `icon_ghost_ship_skyglass_crystal_pixel.webp` |
| 63 | Skyglass Filament (pixel redraw) | ICON | lime | redraw_icon_ghost_ship_skyglass_filament.webp, arakane | `icon_ghost_ship_skyglass_filament_pixel.webp` |
| 64 | Skyglass Katana (pixel redraw) | ICON | lime | redraw_icon_ghost_ship_skyglass_katana.webp, arakane | `icon_ghost_ship_skyglass_katana_pixel.webp` |
| 65 | Skyglass Serum (pixel redraw) | ICON | lime | redraw_icon_ghost_ship_skyglass_serum.webp, arakane | `icon_ghost_ship_skyglass_serum_pixel.webp` |
| 66 | Scene: Wreck keel and hatch | SCENE_BACKGROUND | none | scene_exterior_keel_walk, captain_portrait | `scene_bg_skyglass_wreck_keel.webp` |
| 67 | Scene: Flooded intake | SCENE_BACKGROUND | none | scene_lower_hull, captain_portrait | `scene_bg_skyglass_foundry_intake.webp` |
| 68 | Scene: Cooling racks | SCENE_BACKGROUND | none | scene_hold, captain_portrait | `scene_bg_skyglass_foundry_racks.webp` |
| 69 | Scene: Pour hall | SCENE_BACKGROUND | none | scene_lower_hull, captain_portrait | `scene_bg_skyglass_foundry_pour_hall.webp` |
| 70 | Scene: Crucible chamber | SCENE_BACKGROUND | none | scene_hold, captain_portrait | `scene_bg_skyglass_foundry_crucible.webp` |
| 71 | Scene: Rebuilding lower hull | SCENE_BACKGROUND | none | scene_lower_hull, captain_portrait | `scene_bg_skyglass_lower_hull.webp` |
| 72 | Scene: Reconstruction chamber | SCENE_BACKGROUND | none | scene_reconstruction_chamber, captain_portrait | `scene_bg_skyglass_reconstruction_chamber.webp` |
| 73 | Scene: Quarantined archive | SCENE_BACKGROUND | none | scene_quarantined_archive, captain_portrait | `scene_bg_skyglass_quarantined_archive.webp` |
| 74 | Scene: Night cove landing | SCENE_BACKGROUND | none | scene_cache_site, captain_portrait | `scene_bg_skyglass_cove_landing.webp` |
| 75 | Scene: Chart room | SCENE_BACKGROUND | none | scene_chart_room, captain_portrait | `scene_bg_skyglass_chart_room.webp` |
| 76 | Scene: Open deck in a gale | SCENE_BACKGROUND | none | scene_deck_b, captain_portrait | `scene_bg_skyglass_deck.webp` |
| 77 | Scene: Helm and command dais | SCENE_BACKGROUND | none | scene_helm, captain_portrait | `scene_bg_skyglass_helm.webp` |
| 78 | Scene: Observation gallery | SCENE_BACKGROUND | none | scene_command_observation_gallery, captain_portrait | `scene_bg_skyglass_observation_gallery.webp` |
| 79 | Scene: Three coves and the stone shrine | SCENE_BACKGROUND | none | scene_cache_site, captain_portrait | `scene_bg_skyglass_buried_cache_shore.webp` |

## Prompts

### 1. Sealed Treasury

References (download and attach, in this order):

1. SUBJECT: redraw this exact chest: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/raw/subject_sealed_treasury_painted_v1.png
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Sealed Treasury. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact chest; 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: The Sealed Treasury: redraw the chest in the SUBJECT reference almost exactly (same shape, proportions, iron bands, corner brackets, front hasp, round seal lock with its big faceted pale cyan crystal, and the gold coins and small cyan gem showing at the gap under the lid) as premium pixel art. Shift its colours cooler to fit the set: blue-black wood and blue-grey iron instead of brown and grey.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours as the subject: cool blue-black wood and blue-grey iron, silver-grey metal highlights, ONE accent of pale cyan faceted skyglass with a small glow, cool cyan rim light. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon-sealed-treasury.png.
~~~

### 2. Archive Chart Case

References (download and attach, in this order):

1. CHART FAMILY: shape and materials (painted: redraw as pixel art): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-chart-drowned-foundry.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Archive Chart Case. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. CHART FAMILY: shape and materials (painted: redraw as pixel art); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: The Archive Chart Case: a long cylindrical map case of dark lacquered wood with blackened iron end caps, lying at a slight angle; one end cap is open and the rolled edge of a dark chart with faint pale lines peeks out (the same chart paper as reference 1). Crossed pale paper seal strips bind the middle, with a small iron seal plate set with one faceted pale cyan skyglass bead.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours as the subject: cool blue-black wood and blue-grey iron, silver-grey metal highlights, ONE accent of pale cyan faceted skyglass with a small glow, cool cyan rim light. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon-archive-chart-case.png.
~~~

### 3. Chart of the Buried Cache

References (download and attach, in this order):

1. SHAPE AND LAYOUT (painted: redraw as pixel art): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-chart-drowned-foundry.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Chart of the Buried Cache. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SHAPE AND LAYOUT (painted: redraw as pixel art); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: The Chart of the Buried Cache: the same half-unrolled chart as the reference, sun-faded and salt-stained, sand caught in its folds. Instead of a ship plan, the unrolled part shows a stretch of coastline in faint pale lines with three small coves, older lines faintly visible beneath newer corrections. Beneath a tiny drawn stone shrine above one cove, a single cross mark is picked out in glowing pale cyan skyglass ink; the other two coves stay plain. A frayed rope cord with one faceted pale cyan skyglass bead ties the rolled end.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours as the subject: cool blue-black wood and blue-grey iron, silver-grey metal highlights, ONE accent of pale cyan faceted skyglass with a small glow, cool cyan rim light. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon-chart-buried-cache.png.
~~~

### 4. Unmarked Cargo

References (download and attach, in this order):

1. MATERIAL AND COLOURS (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-skyglass-coffer.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Unmarked Cargo. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. MATERIAL AND COLOURS (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Unmarked Cargo: a plain wooden cargo crate hauled out of the Skyglass wreck, deliberately anonymous. Dark weathered planks, blackened iron corner brackets, wrapped twice in heavy iron chain held by one padlock. Every stencil and marking has been scraped off, leaving pale scratched patches. A thin line of pale cyan skyglass light leaks from one seam.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours as the subject: cool blue-black wood and blue-grey iron, silver-grey metal highlights, ONE accent of pale cyan faceted skyglass with a small glow, cool cyan rim light. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur. No stencil text, no shipping labels.

Return the raw image named raw_icon-unmarked-cargo.png.
~~~

### 5. Crownbreaker (badge)

References (download and attach, in this order):

1. SUBJECT: keep the crown exactly: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp
2. STYLE: icon rendering only: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_crown.webp

~~~text
Draw ONE image for The Ninja RPG: Crownbreaker (badge). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: keep the crown exactly; 2. STYLE: icon rendering only. Follow each reference only for its stated role.

Subject: Crownbreaker: Supreme Commander Arakane's Command Crown at the moment it breaks. Keep the crown from the avatar exactly: the spiked blackened-gold circlet, the halo of floating skyglass blades with the seal ring at the centre, the glowing control threads. The circlet is split down the middle through the seal, the two halves pushed apart; a white-hot crack of light bursts from the broken centre; the blades scatter and tumble outward; the threads are snapped, their loose ends curling and fading. No hands, no figure.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours as the subject: cool blue-black wood and blue-grey iron, silver-grey metal highlights, ONE accent of pale cyan faceted skyglass with a small glow, cool cyan rim light. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon-badge-crownbreaker.png.
~~~

### 6. Lastlight (jutsu icon)

References (download and attach, in this order):

1. STYLE: jutsu icon register: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/style_refs/jutsu_icons/bbe/icon_bbe_sapphire_command_v2.webp
2. MOTIF: the lantern's light: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-skyglass-signal-beacon.webp

~~~text
Draw ONE image for The Ninja RPG: Lastlight (jutsu icon). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: jutsu icon register; 2. MOTIF: the lantern's light. Follow each reference only for its stated role.

Subject: Lastlight: Crownhold's final signal turned into a weapon. One straight beam of pale cyan-white skyglass light fired from a small lantern-shaped flare at the lower left, burning diagonally through the frame; faint ember-red wounds where the beam has cut, fading at the edges.

Style: PREMIUM PIXEL ART jutsu icon (crisp hard-edged pixels, clean dark outlines, flat cel shading, limited palette, no painterly blur), laid out like the attached exemplar: a single bold technique emblem on a designed dark background with the same framing, rendering and detail density; square 1024 x 1024; readable at 125 px. A designed background is allowed (no chroma key needed).
Negative: no text, no letters, no UI, no watermark, no character portrait, no second emblem.

Return the raw image named raw_icon-jutsu-lastlight.png.
~~~

### 7. Foundry Warden (AI avatar)

References (download and attach, in this order):

1. STYLE: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/avatar_ghost_ship_arsenal_keeper.webp

~~~text
Draw ONE image for The Ninja RPG: Foundry Warden (AI avatar). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE. Follow each reference only for its stated role.

Subject: The Foundry Warden: keeper of the drowned skyglass foundry under the wreck's keel. A broad, heavy crewman in a scorched leather smith's apron over Skyglass Project armour, soaked to the knees, seawater dripping; one hand grips a long crucible-tongs polearm, the other a dripping ladle of glowing pale cyan molten skyglass. Crystal slag crusted on his gauntlets. Accent: molten cyan.

Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_skyglass_foundry_warden.png.
~~~

### 8. Master of Arms (commander)

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Master of Arms (commander). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Master of Arms: Division I commander. A forge-wall weapons master in heavy Skyglass armour, two drawn blades, more weapons slung across his back; calm and exacting. Accent: forge-orange. Commanders are larger and more ornate than regular officers but wear no crown.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_master_of_arms.png.
~~~

### 9. Replicant Zero (commander)

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Replicant Zero (commander). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Replicant Zero: Division II commander. A scientist in a long lab coat rebuilding his own left hand out of light; the first successful reconstruction; calm and curious. Accent: pale violet. Commanders are larger and more ornate than regular officers but wear no crown.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_replicant_zero.png.
~~~

### 10. The Grand Marshal (commander)

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: The Grand Marshal (commander). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: The Grand Marshal: Division III commander, called 'The Second'. A senior officer in an unadorned dark greatcoat, hands behind his back; thoughtful and severe; the deputy who could question orders. Accent: muted brass. Commanders are larger and more ornate than regular officers but wear no crown.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_the_grand_marshal.png.
~~~

### 11. Crownhold Proving Proctor

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Crownhold Proving Proctor. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Crownhold Proving Proctor: Division I. An armory proctor in a faded grey drill uniform, a clipboard of stamped trial sheets in one hand, two practice blades at the hip, a whistle on a cord. Accent: drill-yellow.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_proving_proctor.png.
~~~

### 12. Ordnance Quartermaster

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Ordnance Quartermaster. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Ordnance Quartermaster: Division I. A scorched apron over an officer coat, satchels of glowing sealed explosive tags, soot-dark gloves holding a tray of tags. Accent: tag-orange.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_ordnance_quartermaster.png.
~~~

### 13. Prototype Lancer Unit

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Prototype Lancer Unit. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Prototype Lancer Unit: Division I. A half-built lightning-lance automaton fused with its test pilot, exposed capacitor coils, a serial plate reading only a stamped number shape (no legible text). Accent: electric yellow.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_prototype_lancer_unit.png.
~~~

### 14. Calibration Duelist

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Calibration Duelist. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Calibration Duelist: Division I. A duelist in a calibration harness with chakra-measuring rings on both arms and a wind-swept practice sword, apprentice insignia. Accent: wind-green.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_calibration_duelist.png.
~~~

### 15. Skyglass Archive Keeper

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Skyglass Archive Keeper. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Skyglass Archive Keeper: Division II. An archivist rendered in pale blue chakra light, holding a crystal-core ledger, translucent where the reconstruction is incomplete. Accent: archive blue.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_skyglass_archive_keeper.png.
~~~

### 16. Impression Containment Warden

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Impression Containment Warden. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Impression Containment Warden: Division II. A sealed containment suit with a water-filled observation visor and a heavy chain of vat keys. Accent: water teal.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_impression_containment_warden.png.
~~~

### 17. Unstable Echo Subject

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Unstable Echo Subject. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Unstable Echo Subject: Division II. A failed reconstruction glitching between two overlapping silhouettes, shadow chakra leaking from the seams. Accent: shadow violet.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_unstable_echo_subject.png.
~~~

### 18. Failed Reconstruction Prototype

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Failed Reconstruction Prototype. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Failed Reconstruction Prototype: Division II. A hulking earth-bound prototype, crystal growths over a half-formed body, a reconstruction rig bolted to its back. Accent: stone ochre.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_failed_reconstruction_prototype.png.
~~~

### 19. Command Signal Adjutant

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Command Signal Adjutant. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Command Signal Adjutant: Division III. A relay headset, wind-banner semaphore flags in both hands, High Command rank stripes. Accent: signal green.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_command_signal_adjutant.png.
~~~

### 20. High Command Staff Tactician

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: High Command Staff Tactician. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: High Command Staff Tactician: Division III. A campaign map case and a quill of glowing chakra ink, the Grand Marshal's aide's cord on the shoulder. Accent: ink blue.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_high_command_staff_tactician.png.
~~~

### 21. Honor Guard Commandant

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Honor Guard Commandant. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Honor Guard Commandant: Division III. Ceremonial stone-plated armour and a tower shield bearing a plain circled-cross seal. Accent: polished brass.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_honor_guard_commandant.png.
~~~

### 22. Strategist's Aide-de-Camp

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Strategist's Aide-de-Camp. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Strategist's Aide-de-Camp: Division III. Sealed dispatch tubes crackling with lightning, reflective lacquered armour, an aide's sash. Accent: lightning white.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_strategists_aide_de_camp.png.
~~~

### 23. Sanctum Vanguard

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Sanctum Vanguard. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Sanctum Vanguard: Division IV. Obsidian-and-ember Sanctum armour, fire-chakra gauntlets ablaze, a short banner pole on the back. Accent: ember red.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_sanctum_vanguard.png.
~~~

### 24. Directive Herald

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Directive Herald. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Directive Herald: Division IV. Long ceremonial robes, a glowing directive scroll that is rewriting itself, lightning-lit eyes. Accent: lightning gold.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_directive_herald.png.
~~~

### 25. Last Watch Executor

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Last Watch Executor. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Last Watch Executor: Division IV. A tattered night-watch cloak, twin wind glaives, a blank mask stamped with an unreadable seal. Accent: night blue.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_last_watch_executor.png.
~~~

### 26. Order-Bearer of the Sanctum

References (download and attach, in this order):

1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Order-Bearer of the Sanctum. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: Crownhold set (rendering, outline, palette handling; NOT the character or his crown). Follow each reference only for its stated role.

Subject: Order-Bearer of the Sanctum: Division IV. Deep-water Sanctum regalia, a sealed scroll case, a blank unsigned command seal held up. Accent: deep-sea blue.

Continuity (Crownhold): this officer is a reconstructed chakra impression of the Skyglass Project's mountain fortress, not a ghost: luminous cyan seams at the joints and edges, slight translucency, a faint flicker. One thin glowing cyan thread rises from the back of the neck up and out of frame: the Command Crown's control line. Palette: mountain-stone greys, military brass, Skyglass blue-white, plus the one accent named below.
Style: single full-body character avatar, crisp pixel art with clean dark outlines and flat cel shading matching the style reference, front three-quarter view, whole figure inside the frame with a clear margin, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard. Square 1024 x 1024.
Negative: no text, no UI, no watermark, no scenery, no floor, no cast shadow on the magenta, no magenta spill, no second character, no undead imagery (no rot, bones, skulls or grave motifs), no realistic or painterly rendering, no blur, no gradient background, no sheet, no grid.

Return the raw image named raw_avatar_crownhold_order_bearer_of_the_sanctum.png.
~~~

### 27. Scene: Crownhold gate

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Crownhold gate. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A snow-drifted parade ground before an open gate cut into a mountain wall; the gate stands open and unguarded; no banners; deep, unbroken snow; faint cyan light deep inside. (Used by: the fail node, 'you wake outside the gate in the snow'.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_gate.png.
~~~

### 28. Scene: Armory proving hall

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Armory proving hall. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Inside the Experimental Armory: rows of weapon racks humming behind glass, a live-fire trial range with targets, a brass placard by the first rack, cold stone and military brass. (Used by: Division I opening, the Proving Proctor.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_proving_hall.png.
~~~

### 29. Scene: Ordnance store

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Ordnance store. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: An open ordnance store past the trial range: a counter with a ledger, shelves of sealed explosive tags glowing with heat, scorch marks on the stone. (Used by: the Ordnance Quartermaster.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_ordnance_store.png.
~~~

### 30. Scene: Test gallery

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Test gallery. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A narrow test gallery: an empty heavy firing rig bolted to the floor with lightning-scorched clamps and capacitor cables, crackling yellow sparks. (Used by: the Prototype Lancer Unit.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_test_gallery.png.
~~~

### 31. Scene: Armory command terminal

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Armory command terminal. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A glowing Military Command Terminal set into the armory wall beside a sealed door, a maintenance crawlway hatch behind live-fire racks with a three-switch lock. (Used by: Division I terminal, puzzle, protocols.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_armory_terminal.png.
~~~

### 32. Scene: Forge wall

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Forge wall. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: The armory's heart: a towering forge wall hung with every weapon type ever tested, a glowing forge, an anvil, sealed door behind. (Used by: the Master of Arms.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_forge_wall.png.
~~~

### 33. Scene: Archive of impressions

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Archive of impressions. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A library of glass: tall shelves of crystal cores, each holding a faint sleeping light, cold blue air, a reading desk with an open ledger. (Used by: Division II opening, the Archive Keeper.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_archive_of_impressions.png.
~~~

### 34. Scene: Vat halls

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Vat halls. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Halls of tall glowing specimen tanks lit by one tall Skyglass lamp column; chains of vat keys on hooks; one tank cracked and dark. (Used by: the Containment Warden, the Unstable Echo Subject.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_vat_halls.png.
~~~

### 35. Scene: Research command terminal

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Research command terminal. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A command terminal beside the door of the reconstruction theatre, a plaque on the door, a locked maintenance stair behind the specimen tanks. (Used by: Division II terminal, puzzle, protocols.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_research_terminal.png.
~~~

### 36. Scene: Reconstruction theatre

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Reconstruction theatre. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: An operating theatre seen from behind observation glass: a central operating floor ringed by tiered seats, a reconstruction rig of light and crystal over an empty table. (Used by: Replicant Zero.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_reconstruction_theatre.png.
~~~

### 37. Scene: High Command signal room

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: High Command signal room. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A signal room: a long relay board of brass switches and paper tape, a sheet of paper printing itself line by line, maps of borders that no longer exist on the walls; empty of people. (Used by: Division III opening, the Signal Adjutant, and the aftermath; whoever sends the order is NEVER shown.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_signal_room.png.
~~~

### 38. Scene: Planning hall

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Planning hall. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A planning hall set for a war council no one will attend: a long table with campaign maps, empty chairs, an inkwell of glowing chakra ink. (Used by: the Staff Tactician.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_planning_hall.png.
~~~

### 39. Scene: Honor guard corridor

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Honor guard corridor. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A long corridor lined with suits of ceremonial stone-plated armour on stands, a tower shield with a plain circled-cross seal, leading to a closed office door. (Used by: the Honor Guard Commandant.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_honor_guard_corridor.png.
~~~

### 40. Scene: High Command terminal

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: High Command terminal. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A command terminal outside a senior officer's office door, a narrow service corridor beside it, dispatch tubes on a rack. (Used by: Division III terminal, puzzle, protocols.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_high_command_terminal.png.
~~~

### 41. Scene: The Grand Marshal's office

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: The Grand Marshal's office. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A severe, unadorned office: a folding map table, a single chair, a window onto snow, thirty years of annotated orders pinned to the wall. (Used by: the Grand Marshal.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_marshals_office.png.
~~~

### 42. Scene: Sanctum gate

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Sanctum gate. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: The summit: a gate of dark obsidian lit by ember light at the top of a long stair, ember braziers, the Supreme Command banner. (Used by: Division IV opening, the Sanctum Vanguard.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_sanctum_gate.png.
~~~

### 43. Scene: Sanctum antechamber

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Sanctum antechamber. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: An obsidian antechamber with a lectern for a herald's scroll, lightning-blue light on black stone, ember lamps. (Used by: the Directive Herald.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_antechamber.png.
~~~

### 44. Scene: Outer ring and terminal

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Outer ring and terminal. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: The curved night-watch corridor of the Sanctum's outer ring, the last Military Command Terminal glowing in the wall, a sealed door ahead, a maintenance channel grille in the floor. (Used by: the Last Watch Executor, Division IV terminal, puzzle, protocols.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_outer_ring.png.
~~~

### 45. Scene: Throne room

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Throne room. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (it is painted: do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: An obsidian throne room lit by ember light, a tall summit window looking out over a whole mountain range at night, an empty command seat; faint cyan threads of light run from the floor up toward where the commander stands (he is not shown). (Used by: Supreme Commander Arakane.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_crownhold_throne_room.png.
~~~

### 46. The Last Directive (jutsu icon)

References (download and attach, in this order):

1. STYLE: jutsu icon register: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/style_refs/jutsu_icons/bbe/icon_bbe_sapphire_command_v2.webp
2. MOTIF: the Command Crown: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: The Last Directive (jutsu icon). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: jutsu icon register; 2. MOTIF: the Command Crown. Follow each reference only for its stated role.

Subject: The Last Directive: a commander's final order to himself. The Command Crown's seal ring blazing white-gold above a single upright blade planted point-down, an unbreakable shield of light around it.

Style: PREMIUM PIXEL ART jutsu icon (crisp hard-edged pixels, clean dark outlines, flat cel shading, limited palette, no painterly blur), laid out like the attached exemplar: a single bold technique emblem on a designed dark background with the same framing, rendering and detail density; square 1024 x 1024; readable at 125 px. A designed background is allowed (no chroma key needed).
Negative: no text, no letters, no UI, no watermark, no character portrait, no second emblem.

Return the raw image named raw_icon-jutsu-the-last-directive.png.
~~~

### 47. Extermination Order (jutsu icon)

References (download and attach, in this order):

1. STYLE: jutsu icon register: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/style_refs/jutsu_icons/bbe/icon_bbe_sapphire_command_v2.webp
2. MOTIF: the Command Crown: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Extermination Order (jutsu icon). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. STYLE: jutsu icon register; 2. MOTIF: the Command Crown. Follow each reference only for its stated role.

Subject: Extermination Order: a killing command. Seven taut cyan threads converging from the edges onto one point, where a sealed elemental sigil cracks apart.

Style: PREMIUM PIXEL ART jutsu icon (crisp hard-edged pixels, clean dark outlines, flat cel shading, limited palette, no painterly blur), laid out like the attached exemplar: a single bold technique emblem on a designed dark background with the same framing, rendering and detail density; square 1024 x 1024; readable at 125 px. A designed background is allowed (no chroma key needed).
Negative: no text, no letters, no UI, no watermark, no character portrait, no second emblem.

Return the raw image named raw_icon-jutsu-extermination-order.png.
~~~

### 48. Countermand (item icon)

References (download and attach, in this order):

1. SUBJECT AND PIXEL STYLE: the seal tablet at Arakane's belt: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Countermand (item icon). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT AND PIXEL STYLE: the seal tablet at Arakane's belt. Follow each reference only for its stated role.

Subject: Countermand: Crownhold's command seal. The rectangular gold-framed seal tablet that hangs from Arakane's belt, on a short chain, its face carved with a plain circled-cross seal glowing pale cyan.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours as the subject: cool blue-black wood and blue-grey iron, silver-grey metal highlights, ONE accent of pale cyan faceted skyglass with a small glow, cool cyan rim light. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon-countermand.png.
~~~

### 49. Skyglass Coffer (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-skyglass-coffer.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Skyglass Coffer (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Skyglass Coffer: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon-skyglass-coffer-pixel.png.
~~~

### 50. Katon Tool Pouch (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-tool-pouch-katon.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Katon Tool Pouch (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Katon Tool Pouch: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon-tool-pouch-katon-pixel.png.
~~~

### 51. Wave Tool Pouch (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-tool-pouch-wave.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Wave Tool Pouch (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Wave Tool Pouch: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon-tool-pouch-wave-pixel.png.
~~~

### 52. Ikazuchi Tool Pouch (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-tool-pouch-ikazuchi.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Ikazuchi Tool Pouch (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Ikazuchi Tool Pouch: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon-tool-pouch-ikazuchi-pixel.png.
~~~

### 53. Stonefall Tool Pouch (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-tool-pouch-stonefall.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Stonefall Tool Pouch (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Stonefall Tool Pouch: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon-tool-pouch-stonefall-pixel.png.
~~~

### 54. Zephyrfang Tool Pouch (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-tool-pouch-zephyrfang.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Zephyrfang Tool Pouch (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Zephyrfang Tool Pouch: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat magenta chroma key background (#FF00FF) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon-tool-pouch-zephyrfang-pixel.png.
~~~

### 55. Chart of the Drowned Foundry (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-chart-drowned-foundry.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Chart of the Drowned Foundry (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Chart of the Drowned Foundry: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon-chart-drowned-foundry-pixel.png.
~~~

### 56. Chart of the Quarantined Archive (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-chart-quarantined-archive.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Chart of the Quarantined Archive (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Chart of the Quarantined Archive: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon-chart-quarantined-archive-pixel.png.
~~~

### 57. Chart of the Captain's Watch (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-chart-captains-watch.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Chart of the Captain's Watch (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Chart of the Captain's Watch: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon-chart-captains-watch-pixel.png.
~~~

### 58. Lastlight Lantern (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-skyglass-signal-beacon.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Lastlight Lantern (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Lastlight Lantern: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon-skyglass-signal-beacon-pixel.png.
~~~

### 59. Armory Requisition (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/skyglass_event_icons/exports/icon-armory-requisition.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Armory Requisition (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Armory Requisition: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon-armory-requisition-pixel.png.
~~~

### 60. Skyglass Crown (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_crown.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Skyglass Crown (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Skyglass Crown: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon_ghost_ship_skyglass_crown_pixel.png.
~~~

### 61. Skyglass Crown Fragment (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_crown_fragment.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Skyglass Crown Fragment (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Skyglass Crown Fragment: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon_ghost_ship_skyglass_crown_fragment_pixel.png.
~~~

### 62. Skyglass Crystal (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_crystal.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Skyglass Crystal (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Skyglass Crystal: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon_ghost_ship_skyglass_crystal_pixel.png.
~~~

### 63. Skyglass Filament (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_filament.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Skyglass Filament (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Skyglass Filament: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon_ghost_ship_skyglass_filament_pixel.png.
~~~

### 64. Skyglass Katana (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_katana.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Skyglass Katana (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Skyglass Katana: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon_ghost_ship_skyglass_katana_pixel.png.
~~~

### 65. Skyglass Serum (pixel redraw)

References (download and attach, in this order):

1. SUBJECT: redraw this exact icon: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/icon_ghost_ship_skyglass_serum.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/crownhold/avatar_crownhold_arakane.webp

~~~text
Draw ONE image for The Ninja RPG: Skyglass Serum (pixel redraw). Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. SUBJECT: redraw this exact icon; 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Skyglass Serum: redraw the SUBJECT reference almost exactly (same object, shape, proportions, details, colours and accent) as premium pixel art, so it matches the rest of the set. Change nothing about the design.

Style: PREMIUM PIXEL ART game item icon, the same pixel rendering as the PIXEL STYLE reference: crisp hard-edged pixels, clean dark outlines, flat cel shading with a few deliberate highlight steps, limited palette, no anti-aliased blur, no painterly gradients. Colours exactly as the SUBJECT reference. Camera at eye level, 3/4 view, strong readable silhouette at 125 px, centered, single object, small even margin. Square 1024 x 1024, on a true solid flat lime-green chroma key background (#00FF00) covering the entire canvas, not transparent, not checkerboard.
Negative: no text, no letters, no numbers, no UI, no frame, no watermark, no table or surface, no shadow on the background, no glow halo, no second object, no question mark, no painted or smooth illustration look, no blur.

Return the raw image named raw_icon_ghost_ship_skyglass_serum_pixel.png.
~~~

### 66. Scene: Wreck keel and hatch

References (download and attach, in this order):

1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_exterior_keel_walk.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Wreck keel and hatch. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Use the first reference as the starting composition and colour, changed to match this brief exactly: Outside the beached Skyglass warship at night: its split keel lies on wet sand and dark rocks at the waterline, iron bands and timber looming overhead; glowing pale cyan seal channels run along the hull into a low hatch rimmed with cooled crystal, and seawater pours past the hatch into the dark below. (Used by: Drowned Foundry d_arrive; Quarantined Archive d_arrive.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_skyglass_wreck_keel.png.
~~~

### 67. Scene: Flooded intake

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (painted: do not copy its rendering or layout): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_lower_hull.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Flooded intake. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (painted: do not copy its rendering or layout); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A new location: The foundry's intake hall inside the wreck, half flooded: dark water at knee height, empty seal canisters bobbing against the walls, iron pipes and valve wheels, pale cyan light glinting off the water. (Used by: Drowned Foundry d_intake, b_intake.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_skyglass_foundry_intake.png.
~~~

### 68. Scene: Cooling racks

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (painted: do not copy its rendering or layout): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_hold.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Cooling racks. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (painted: do not copy its rendering or layout); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A new location: A long hall of iron cooling racks stacked with freshly cast, glowing pale cyan Skyglass ingots that no one has collected; water at ankle height across the floor; a sealed hatch high on the far wall. (Used by: Drowned Foundry d_racks.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_skyglass_foundry_racks.png.
~~~

### 69. Scene: Pour hall

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (painted: do not copy its rendering or layout): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_lower_hull.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Pour hall. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (painted: do not copy its rendering or layout); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A new location: The pour hall: rows of stone casting moulds wired together with seal charges, an inspector's ledger desk, knee-deep water, and an orange-white crucible glow coming up through iron floor grates from below. (Used by: Drowned Foundry d_hall, b_hall, d_gate.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_skyglass_foundry_pour_hall.png.
~~~

### 70. Scene: Crucible chamber

References (download and attach, in this order):

1. COLOUR AND LIGHTING only (painted: do not copy its rendering or layout): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_hold.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Crucible chamber. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COLOUR AND LIGHTING only (painted: do not copy its rendering or layout); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: A new location: The crucible chamber, the only dry room in the works, kept dry by heat: a great tilting crucible of molten pale cyan Skyglass hung in heavy pouring gear, glowing moulds, steam rising where water seeps in at the edges. (Used by: Drowned Foundry d_crucible, b_warden, d_pour.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_skyglass_foundry_crucible.png.
~~~

### 71. Scene: Rebuilding lower hull

References (download and attach, in this order):

1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_lower_hull.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Rebuilding lower hull. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Use the first reference as the starting composition and colour, changed to match this brief exactly: Below the waterline inside the wreck: the hull is rebuilding itself out of timber and cable that do not belong together, half-formed frames knitting in pale cyan seal light; a ladder down to a severed, pulsing conduit. (Used by: Quarantined Archive d_hull, b_horror, d_conduit.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_skyglass_lower_hull.png.
~~~

### 72. Scene: Reconstruction chamber

References (download and attach, in this order):

1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_reconstruction_chamber.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Reconstruction chamber. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Use the first reference as the starting composition and colour, changed to match this brief exactly: Rows of empty upright frames, each holding a faint human impression in seal light; a three-way seal plate in the centre of the floor. (Used by: Quarantined Archive d_chamber, d_seal1, d_alarm1, b_alarm1.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_skyglass_reconstruction_chamber.png.
~~~

### 73. Scene: Quarantined archive

References (download and attach, in this order):

1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_quarantined_archive.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Quarantined archive. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Use the first reference as the starting composition and colour, changed to match this brief exactly: A narrow sealed archive not on any ship plan: tall index shelves of command records and route sheets, a handle-less door crossed with pale script, containment seals on every cabinet. (Used by: Quarantined Archive d_seal2 onward, alarms 2-3, the Sealwright.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_skyglass_quarantined_archive.png.
~~~

### 74. Scene: Night cove landing

References (download and attach, in this order):

1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_cache_site.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Night cove landing. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Use the first reference as the starting composition and colour, changed to match this brief exactly: A quiet cove at night under a full moon: the Ghost Ship's longboat drawn up on the sand, oars shipped, a lantern on its bow; dark water and the silhouette of the wreck's masts beyond the headland. (Used by: Captain's Watch d_landing.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_skyglass_cove_landing.png.
~~~

### 75. Scene: Chart room

References (download and attach, in this order):

1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_chart_room.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Chart room. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Use the first reference as the starting composition and colour, changed to match this brief exactly: The ship's chart room: a big table buried in charts layered with decades of corrections, route pins and dividers, glowing pale cyan route lines redrawn over older ink. (Used by: Captain's Watch fight 1 (Wayfinder).)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_skyglass_chart_room.png.
~~~

### 76. Scene: Open deck in a gale

References (download and attach, in this order):

1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_deck_b.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Open deck in a gale. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Use the first reference as the starting composition and colour, changed to match this brief exactly: The open upper deck in a rising gale: torn sails cracking, rigging lines singing, empty mess tables lashed down, pale cyan seal light along the rails. (Used by: Captain's Watch fight 2 (First Blade).)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_skyglass_deck.png.
~~~

### 77. Scene: Helm and command dais

References (download and attach, in this order):

1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_helm.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Helm and command dais. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Use the first reference as the starting composition and colour, changed to match this brief exactly: The raised command dais at the helm: the great wheel, core-link seals glowing pale cyan in the floor, the ship's seal sigil on a banner, night sky beyond. (Used by: Captain's Watch fight 3 (the Captain).)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_skyglass_helm.png.
~~~

### 78. Scene: Observation gallery

References (download and attach, in this order):

1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_command_observation_gallery.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Observation gallery. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Use the first reference as the starting composition and colour, changed to match this brief exactly: A viewing gallery above the command deck: tall windows showing the whole ship's glowing seal network repairing itself, storage chests along the walls. (Used by: Captain's Watch endings.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_skyglass_observation_gallery.png.
~~~

### 79. Scene: Three coves and the stone shrine

References (download and attach, in this order):

1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering): https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_bg_ghost_ship_cache_site.webp
2. PIXEL STYLE: rendering only, not the character: https://raw.githubusercontent.com/perseverance484/tnr-tools/2a79eb90a053c3aa56a70b5d3823e88069104c40/art/ghost_ship_skyglass/scene_char_ghost_ship_captain_portrait_b.webp

~~~text
Draw ONE image for The Ninja RPG: Scene: Three coves and the stone shrine. Generate exactly one candidate. Do not crop, key or process it.
References attached: 1. COMPOSITION AND COLOUR base (painted: redraw, do not copy its rendering); 2. PIXEL STYLE: rendering only, not the character. Follow each reference only for its stated role.

Subject: Use the first reference as the starting composition and colour, changed to match this brief exactly: A stretch of night shore with three small coves: a split cliff breaking the tide on the left, an open beach past a reef in the middle, and on the right a small stone shrine on the cliff above a cove, its shadow falling across the sand where the cache is buried. (Used by: The Buried Cache, every node.)

Style: PREMIUM PIXEL ART game scene background, the same pixel rendering as the PIXEL STYLE reference (crisp hard-edged pixels, clean dark outlines, flat cel shading with deliberate highlight steps, limited palette, no painterly blur), wide 3:2 landscape (1536 x 1024), no characters, no people, no text, no UI, no watermark, no frame. Leave the lower-left and lower-right thirds readable: dialog portraits stand there. Palette and lighting as the colour reference: night or dusk, deep blues, Skyglass cyan light.

Return the raw image named raw_scene_bg_skyglass_buried_cache_shore.png.
~~~

